#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
import json
import os
import re
from datetime import datetime, timedelta
from collections import OrderedDict

def scrape_prayer_times():
    url = "https://mawaqit.net/fr/dzematlozana"
    masjid_id = "dzematlozana"
    
    try:
        print(f"Fetching prayer times for {masjid_id}...")
        
        # Make a request to the masjid page
        response = requests.get(f"https://mawaqit.net/fr/{masjid_id}")
        
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
                    
                    # Create a directory for saving the data
                    os.makedirs("../data/prayers", exist_ok=True)
                    
                    # Save the full confData for reference
                    with open("../data/prayers/full_conf_data.json", 'w', encoding='utf-8') as f:
                        json.dump(conf_data, f, indent=2, ensure_ascii=False)
                    
                    # Extract today's prayer times
                    times = conf_data.get("times", [])
                    sunrise = conf_data.get("shuruq", "")
                    
                    # Extract Jumua (Friday prayer) time
                    jumua = conf_data.get("jumua", "")
                    
                    # Get current date to find the correct iqama times
                    today = datetime.now()
                    day = today.day
                    month = today.month - 1  # Arrays are 0-indexed
                    
                    # Get iqama calendar which contains the minutes to add to each prayer time
                    iqama_calendar = conf_data.get("iqamaCalendar", [])
                    iqama_today = None
                    
                    if iqama_calendar and len(iqama_calendar) > month:
                        month_data = iqama_calendar[month]
                        if str(day) in month_data:
                            iqama_today = month_data[str(day)]
                    
                    # Format the prayer times in our desired structure
                    prayer_times = {
                        "last_updated": str(datetime.now()),
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
                                except (ValueError, TypeError):
                                    pass
                    
                    print(f"Found prayer times: {prayer_times}")
                    return prayer_times
                else:
                    print("Failed to extract confData JSON")
            else:
                print("Script containing confData not found.")
                
                # Save the raw HTML for debugging
                with open("../data/prayers/debug_last_html.html", "w", encoding="utf-8") as f:
                    f.write(soup.prettify())
        else:
            print(f"Failed to fetch page, status code: {response.status_code}")
            
        # Return error state if we couldn't get the data
        return {
            "error": "Failed to extract prayer times",
            "last_updated": str(datetime.now())
        }
            
    except Exception as e:
        print(f"Error scraping prayer times: {e}")
        return {
            "error": str(e),
            "last_updated": str(datetime.now())
        }

def save_prayer_times(prayer_times):
    if prayer_times:
        # Create output directory if it doesn't exist
        os.makedirs("../data/prayers", exist_ok=True)
        
        # Save to JSON file
        output_file = "../data/prayers/prayer_times.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(prayer_times, f, indent=4, ensure_ascii=False)
        
        print(f"Prayer times saved to {output_file}")
        return True
    return False

if __name__ == "__main__":
    prayer_times = scrape_prayer_times()
    save_prayer_times(prayer_times) 