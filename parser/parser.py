import json

from ics import Calendar


def parse_ics_to_json(ics_file_path):
    with open(ics_file_path, "r") as file:
        ics_content = file.read()

    calendar = Calendar(ics_content)
    calendar_data = {
        "events": [],
    }

    for event in calendar.events:
        event_details = {
            "name": event.name,
            "begin": event.begin.isoformat() if event.begin else None,
            "begin_timezone": (
                str(event.begin.tzinfo) if event.begin and event.begin.tzinfo else None
            ),
            "end": event.end.isoformat() if event.end else None,
            "end_timezone": (
                str(event.end.tzinfo) if event.end and event.end.tzinfo else None
            ),
            "duration": str(event.duration) if event.duration else None,
            "location": event.location,
            "description": event.description,
            "created": event.created.isoformat() if event.created else None,
            "last_modified": (
                event.last_modified.isoformat() if event.last_modified else None
            ),
            "uid": event.uid,
            "url": event.url,
            "organizer": str(event.organizer) if event.organizer else None,
            "organizer_email": (
                event.organizer.email
                if event.organizer and hasattr(event.organizer, "email")
                else None
            ),
            "attendees": (
                [str(attendee) for attendee in event.attendees]
                if event.attendees
                else None
            ),
            "categories": list(event.categories) if event.categories else None,
            "status": event.status,
            "transparent": event.transparent,
            "alarms": [str(alarm) for alarm in event.alarms] if event.alarms else None,
            "classification": event.classification,
        }
        calendar_data["events"].append(event_details)

    return json.dumps(calendar_data, indent=4)


# Usage
ics_file_path = "/home/aashish/Documents/ics/parser/calendar.ics"
json_output = parse_ics_to_json(ics_file_path)
print(json_output)
