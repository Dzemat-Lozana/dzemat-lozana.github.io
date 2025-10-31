#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
import json
import os
import re
from datetime import datetime, timedelta

def get_repo_root():
    """Get the repository root directory."""
    if os.path.basename(os.getcwd()) == 'scripts':
        return os.path.dirname(os.getcwd())
    return os.getcwd()

def load_existing_times():
    """Load existing prayer times from file if it exists."""
    try:
        file_path = os.path.join(get_repo_root(), "data", "prayers", "prayer_times.json")
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return None

def times_have_changed(old_times, new_times):
    """Compare prayer times while ignoring last_updated field."""
    if not old_times or not new_times:
        return True
        
    old_copy = old_times.copy()
    new_copy = new_times.copy()
    
    old_copy.pop('last_updated', None)
    new_copy.pop('last_updated', None)
    
    return old_copy != new_copy

def scrape_prayer_times():
    url = "https://mawaqit.net/fr/dzematlozana"
    masjid_id = "dzematlozana"
    
    try:
        print(f"Fetching prayer times for {masjid_id}...")
        response = requests.get(f"https://mawaqit.net/fr/{masjid_id}")
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            script = soup.find('script', string=re.compile(r'let confData = ', re.DOTALL))

            if script:
                mawaqit = re.search(r'let confData = ({.*?});', script.string, re.DOTALL)
                
                if mawaqit:
                    conf_data = json.loads(mawaqit.group(1))
                    
                    times = conf_data.get("times", [])
                    sunrise = conf_data.get("shuruq", "")
                    jumua = conf_data.get("jumua", "")
                    
                    today = datetime.now()
                    day = today.day
                    month = today.month - 1
                    
                    iqama_calendar = conf_data.get("iqamaCalendar", [])
                    iqama_today = None
                    
                    if iqama_calendar and len(iqama_calendar) > month:
                        month_data = iqama_calendar[month]
                        if str(day) in month_data:
                            iqama_today = month_data[str(day)]
                    
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
                    
                    if iqama_today and len(iqama_today) >= 5:
                        prayer_names = ["fajr", "dhuhr", "asr", "maghrib", "isha"]
                        
                        for i, prayer in enumerate(prayer_names):
                            if i < len(iqama_today) and prayer in prayer_times and prayer_times[prayer]:
                                minutes_to_add = iqama_today[i].replace("+", "")
                                try:
                                    prayer_time = datetime.strptime(prayer_times[prayer]["time"], "%H:%M")
                                    iqama_time = prayer_time + timedelta(minutes=int(minutes_to_add))
                                    prayer_times[prayer]["iqama"] = iqama_time.strftime("%H:%M")
                                except (ValueError, TypeError):
                                    pass
                    
                    return prayer_times
                
        return {
            "error": "Failed to extract prayer times",
            "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M")
        }
            
    except Exception as e:
        return {
            "error": str(e),
            "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M")
        }

def save_prayer_times(prayer_times):
    if prayer_times:
        data_dir = os.path.join(get_repo_root(), "data", "prayers")
        os.makedirs(data_dir, exist_ok=True)
        output_file = os.path.join(data_dir, "prayer_times.json")
        
        existing_times = load_existing_times()
        
        if times_have_changed(existing_times, prayer_times):
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(prayer_times, f, indent=4, ensure_ascii=False)
            print(f"Prayer times updated and saved")
            return True
        else:
            print("Prayer times unchanged")
            return False
    return False

if __name__ == "__main__":
    prayer_times = scrape_prayer_times()
    save_prayer_times(prayer_times) 