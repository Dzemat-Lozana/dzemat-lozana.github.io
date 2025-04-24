import os
import json
import datetime
from pathlib import Path
import facebook  # python-facebook-api package
import re
import yaml

def slugify(text):
    """Convert text to URL-friendly slug"""
    # Convert to lowercase and replace spaces with hyphens
    text = text.lower().replace(' ', '-')
    # Remove special characters
    text = re.sub(r'[^a-z0-9-]', '', text)
    # Remove multiple consecutive hyphens
    text = re.sub(r'-+', '-', text)
    return text.strip('-')

def clean_text(text):
    """Clean text from problematic characters"""
    if not text:
        return ""
    # Replace smart quotes with regular quotes
    text = text.replace('"', '"').replace('"', '"')
    text = text.replace(''', "'").replace(''', "'")
    # Replace other problematic characters
    text = text.replace('\u2028', '\n').replace('\u2029', '\n')
    # Remove any null bytes
    text = text.replace('\x00', '')
    return text

def get_facebook_events():
    # Initialize the Graph API with your access token
    access_token = os.environ.get('FACEBOOK_ACCESS_TOKEN')
    if not access_token:
        raise ValueError("Facebook access token not found in environment variables")
    
    graph = facebook.GraphAPI(access_token)
    
    # Facebook page ID for dzemat.lozana
    page_id = '722364147859407'
    
    try:
        # Get events from the page
        events = graph.get_connections(
            page_id,
            'events',
            fields='id,name,description,start_time,end_time,place,cover'
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
        'title': clean_text(event['name']),
        'date': event_date.strftime('%Y-%m-%dT%H:%M:%S%z'),
        'draft': False,
        'description': clean_text(event.get('description', '')),
        'eventDate': event_date.strftime('%Y-%m-%dT%H:%M:%S%z'),
        'location': clean_text(event.get('place', {}).get('name', '')),
        'facebook_id': event['id'],
        'weight': 30
    }
    
    # Add cover image if available
    if 'cover' in event and 'source' in event['cover']:
        hugo_event['image'] = event['cover']['source']
    
    if 'end_time' in event:
        end_date = datetime.datetime.strptime(
            event['end_time'],
            '%Y-%m-%dT%H:%M:%S%z'
        )
        hugo_event['endDate'] = end_date.strftime('%Y-%m-%dT%H:%M:%S%z')
    
    return hugo_event

def create_event_file(event_data, file_path, lang):
    """Create event file with front matter and content"""
    # Create directory if it doesn't exist
    file_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Prepare front matter data
    front_matter_data = {k: v for k, v in event_data.items()}
    
    # Create front matter using PyYAML
    front_matter = yaml.safe_dump(front_matter_data, allow_unicode=True, sort_keys=False)
    
    # Add description as content
    content = clean_text(event_data.get('description', ''))
    
    # Add Facebook event link at the end
    fb_link = f"\n\n---\n\nPlus d'informations sur [Facebook](https://facebook.com/events/{event_data['facebook_id']})" if lang == 'fr' else f"\n\n---\n\nViše informacija na [Facebook-u](https://facebook.com/events/{event_data['facebook_id']})"
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write('---\n')
        f.write(front_matter)
        f.write('---\n\n')
        f.write(content)
        f.write(fb_link)

def main():
    # Create events directory if it doesn't exist
    events_dir = Path('data/events')
    events_dir.mkdir(parents=True, exist_ok=True)
    
    # Get existing events
    existing_events = {}
    if (events_dir / 'events.json').exists():
        with open(events_dir / 'events.json', 'r', encoding='utf-8') as f:
            existing_events = json.load(f)
    
    # Fetch new events
    fb_events = get_facebook_events()
    new_events = {}
    
    for event in fb_events:
        hugo_event = create_hugo_event(event)
        new_events[event['id']] = hugo_event
        
        # Create event files in content/events/YEAR/MONTH/slug structure
        event_date = datetime.datetime.strptime(
            event['start_time'],
            '%Y-%m-%dT%H:%M:%S%z'
        )
        
        # Create slug from event name
        slug = slugify(event['name'])
        
        # Create path structure
        event_path = Path('content/events') / str(event_date.year) / f"{event_date.month:02d}" / slug
        
        # Create both language versions
        for lang in ['bs', 'fr']:
            file_path = event_path / f"index.{lang}.md"
            create_event_file(hugo_event, file_path, lang)
    
    # Update events (this will handle both new events and updates)
    existing_events.update(new_events)
    
    # Write updated events to file
    with open(events_dir / 'events.json', 'w', encoding='utf-8') as f:
        json.dump(existing_events, f, ensure_ascii=False, indent=2)

if __name__ == '__main__':
    main() 