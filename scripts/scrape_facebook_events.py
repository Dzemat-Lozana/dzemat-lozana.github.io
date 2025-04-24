import os
import json
import datetime
from pathlib import Path
import facebook  # python-facebook-api package

def get_facebook_events():
    # Initialize the Graph API with your access token
    access_token = os.environ.get('FACEBOOK_ACCESS_TOKEN')
    if not access_token:
        raise ValueError("Facebook access token not found in environment variables")
    
    graph = facebook.GraphAPI(access_token)
    
    # Facebook page ID for dzemat.lozana
    page_id = '722364147859407'  # You might need to replace this with the actual numeric ID
    
    try:
        # Get events from the page
        events = graph.get_connections(
            page_id,
            'events',
            fields='id,name,description,start_time,end_time,place'
        )
        
        return events.get('data', [])
    except facebook.GraphAPIError as e:
        print(f"Error fetching events: {e}")
        return []

def create_hugo_event(event):
    """Convert Facebook event to Hugo event format"""
    event_date = datetime.datetime.strptime(
        event['start_time'], 
        '%Y-%m-%dT%H:%M:%S%z'
    )
    
    # Create Hugo front matter
    hugo_event = {
        'title': event['name'],
        'date': event_date.strftime('%Y-%m-%d'),
        'time': event_date.strftime('%H:%M'),
        'description': event.get('description', ''),
        'location': event.get('place', {}).get('name', ''),
        'facebook_id': event['id'],
        'draft': False
    }
    
    if 'end_time' in event:
        end_date = datetime.datetime.strptime(
            event['end_time'],
            '%Y-%m-%dT%H:%M:%S%z'
        )
        hugo_event['end_time'] = end_date.strftime('%H:%M')
        hugo_event['end_date'] = end_date.strftime('%Y-%m-%d')
    
    return hugo_event

def main():
    # Create events directory if it doesn't exist
    events_dir = Path('data/events')
    events_dir.mkdir(parents=True, exist_ok=True)
    
    # Get existing events
    existing_events = {}
    if (events_dir / 'events.json').exists():
        with open(events_dir / 'events.json', 'r') as f:
            existing_events = json.load(f)
    
    # Fetch new events
    fb_events = get_facebook_events()
    new_events = {}
    
    for event in fb_events:
        hugo_event = create_hugo_event(event)
        new_events[event['id']] = hugo_event
    
    # Update events (this will handle both new events and updates)
    existing_events.update(new_events)
    
    # Write updated events to file
    with open(events_dir / 'events.json', 'w', encoding='utf-8') as f:
        json.dump(existing_events, f, ensure_ascii=False, indent=2)
    
    # Create individual Hugo event files
    content_dir = Path('content/events')
    content_dir.mkdir(parents=True, exist_ok=True)
    
    for event_id, event in existing_events.items():
        event_file = content_dir / f"{event['date']}-{event_id}.md"
        
        # Create Hugo front matter
        front_matter = "---\n"
        for key, value in event.items():
            front_matter += f"{key}: {json.dumps(value)}\n"
        front_matter += "---\n"
        
        # Add description as content if available
        content = event.get('description', '')
        
        with open(event_file, 'w', encoding='utf-8') as f:
            f.write(front_matter)
            f.write('\n')
            f.write(content)

if __name__ == '__main__':
    main() 