#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
import json
import os
import re
from datetime import datetime, timedelta
from collections import OrderedDict
import tempfile

def debug_print(*args, **kwargs):
    """Print with timestamp for better GitHub Actions logs."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}]", *args, **kwargs)

def get_debug_dir():
    """Get the directory for debug files."""
    # Use a subdirectory in the system's temp directory
    debug_dir = os.path.join(tempfile.gettempdir(), "prayer_times_debug")
    os.makedirs(debug_dir, exist_ok=True)
    return debug_dir

def load_existing_times():
    """Load existing prayer times from file if it exists."""
    try:
        with open("../data/prayers/prayer_times.json", 'r', encoding='utf-8') as f:
            data = json.load(f)
            debug_print("Successfully loaded existing prayer times")
            return data
    except FileNotFoundError:
        debug_print("No existing prayer times file found")
        return None
    except json.JSONDecodeError as e:
        debug_print(f"Error decoding existing prayer times: {e}")
        return None

def times_have_changed(old_times, new_times):
    """Compare prayer times while ignoring last_updated field."""
    if not old_times or not new_times:
        debug_print("No old times or new times available, considering as changed")
        return True
        
    old_copy = old_times.copy()
    new_copy = new_times.copy()
    
    # Remove last_updated field for comparison
    old_copy.pop('last_updated', None)
    new_copy.pop('last_updated', None)
    
    has_changed = old_copy != new_copy
    if has_changed:
        debug_print("Prayer times have changed:")
        debug_print("Old times:", json.dumps(old_copy, indent=2))
        debug_print("New times:", json.dumps(new_copy, indent=2))
    else:
        debug_print("Prayer times are unchanged")
    
    return has_changed

def scrape_prayer_times():
    url = "https://mawaqit.net/fr/dzematlozana"
    masjid_id = "dzematlozana"
    
    try:
        debug_print(f"Fetching prayer times for {masjid_id}...")
        
        # Make a request to the masjid page
        response = requests.get(f"https://mawaqit.net/fr/{masjid_id}")
        debug_print(f"Response status code: {response.status_code}")
        
        # Save the HTML response for debugging in temp directory
        debug_dir = get_debug_dir()
        html_file = os.path.join(debug_dir, "last_response.html")
        with open(html_file, "w", encoding="utf-8") as f:
            f.write(response.text)
            debug_print(f"Saved HTML response to {html_file} ({len(response.text)} bytes)")
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Look for the JavaScript variable 'confData' which contains all prayer times
            script = soup.find('script', string=re.compile(r'var confData = (.*?);', re.DOTALL))
            
            if script:
                # Extract the JSON data
                mawaqit = re.search(r'var confData = (.*?);', script.string, re.DOTALL)
                
                if mawaqit:
                    # Parse the JSON data
                    conf_data_json = mawaqit.group(1)
                    conf_data = json.loads(conf_data_json)
                    debug_print("Successfully parsed confData JSON")
                    
                    # Save the full confData for debugging
                    conf_data_file = os.path.join(debug_dir, "full_conf_data.json")
                    with open(conf_data_file, 'w', encoding='utf-8') as f:
                        json.dump(conf_data, f, indent=2, ensure_ascii=False)
                        debug_print(f"Saved full configuration data to {conf_data_file}")
                    
                    # Extract today's prayer times
                    times = conf_data.get("times", [])
                    sunrise = conf_data.get("shuruq", "")
                    
                    # Extract Jumua (Friday prayer) time
                    jumua = conf_data.get("jumua", "")
                    
                    # Get current date to find the correct iqama times
                    today = datetime.now()
                    debug_print(f"Current date: {today}")
                    day = today.day
                    month = today.month - 1  # Arrays are 0-indexed
                    
                    # Get iqama calendar which contains the minutes to add to each prayer time
                    iqama_calendar = conf_data.get("iqamaCalendar", [])
                    iqama_today = None
                    
                    if iqama_calendar and len(iqama_calendar) > month:
                        month_data = iqama_calendar[month]
                        if str(day) in month_data:
                            iqama_today = month_data[str(day)]
                            debug_print(f"Found iqama times for today: {iqama_today}")
                    
                    # Format the prayer times in our desired structure
                    prayer_times = {
                        "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M"),
                        "sunrise": {"time": sunrise} if sunrise else {},
                        "fajr": {"time": times[0]} if len(times) > 0 else {},
                        "dhuhr": {"time": times[1]} if len(times) > 1 else {},
                        "asr": {"time": times[2]} if len(times) > 2 else {},
                        "maghrib": {"time": times[3]} if len(times) > 3 else {},
                        "isha": {"time": times[4]} if len(times) > 4 else {},
                        "jumua": {"time": jumua} if jumua else {},
                    }
                    
                    # Add iqama times for each prayer if available
                    if iqama_today and len(iqama_today) >= 5:
                        prayer_names = ["fajr", "dhuhr", "asr", "maghrib", "isha"]
                        
                        for i, prayer in enumerate(prayer_names):
                            if i < len(iqama_today) and prayer in prayer_times and prayer_times[prayer]:
                                minutes_to_add = iqama_today[i].replace("+", "")
                                try:
                                    # Calculate iqama time by adding minutes to prayer time
                                    prayer_time = datetime.strptime(prayer_times[prayer]["time"], "%H:%M")
                                    iqama_time = prayer_time + timedelta(minutes=int(minutes_to_add))
                                    prayer_times[prayer]["iqama"] = iqama_time.strftime("%H:%M")
                                    debug_print(f"Calculated {prayer} iqama time: {prayer_times[prayer]['iqama']}")
                                except (ValueError, TypeError) as e:
                                    debug_print(f"Error calculating iqama time for {prayer}: {e}")
                                    pass
                    
                    debug_print(f"Final prayer times: {json.dumps(prayer_times, indent=2)}")
                    return prayer_times, debug_dir
                else:
                    debug_print("Failed to extract confData JSON")
            else:
                debug_print("Script containing confData not found")
        else:
            debug_print(f"Failed to fetch page, status code: {response.status_code}")
            
        # Return error state if we couldn't get the data
        error_response = {
            "error": "Failed to extract prayer times",
            "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M")
        }
        debug_print(f"Returning error response: {error_response}")
        return error_response, debug_dir
            
    except Exception as e:
        debug_print(f"Error scraping prayer times: {e}")
        return {
            "error": str(e),
            "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M")
        }, debug_dir

def save_prayer_times(prayer_times):
    if prayer_times:
        # Create output directory if it doesn't exist
        data_dir = "../data/prayers"
        os.makedirs(data_dir, exist_ok=True)
        output_file = os.path.join(data_dir, "prayer_times.json")
        
        # Load existing times to check for changes
        existing_times = load_existing_times()
        
        if times_have_changed(existing_times, prayer_times):
            debug_print(f"Saving prayer times to {output_file}")
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(prayer_times, f, indent=4, ensure_ascii=False)
            
            # Verify the file was written
            if os.path.exists(output_file):
                debug_print(f"Successfully saved prayer times to {output_file}")
                file_size = os.path.getsize(output_file)
                debug_print(f"File size: {file_size} bytes")
                return True
            else:
                debug_print(f"Error: Failed to write to {output_file}")
                return False
        else:
            debug_print("Prayer times haven't changed, skipping save")
            return False
    return False

if __name__ == "__main__":
    debug_print("Starting prayer times scraper")
    prayer_times, debug_dir = scrape_prayer_times()
    save_prayer_times(prayer_times)
    debug_print(f"Scraper finished. Debug files are in: {debug_dir}") 