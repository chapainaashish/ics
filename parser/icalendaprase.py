import json
from datetime import date, datetime

from icalendar import Calendar


def parse_ics_to_json(ics_file_path):
    with open(ics_file_path, "r") as file:
        ics_content = file.read()

    calendar = Calendar.from_ical(ics_content)
    calendar_data = {"events": []}

    for component in calendar.walk():
        if component.name == "VEVENT":
            begin = component.get("dtstart").dt
            end = component.get("dtend").dt if component.get("dtend") else None

            event_details = {
                "name": str(component.get("summary")),
                "begin": (
                    begin.isoformat()
                    if isinstance(begin, datetime)
                    else begin.isoformat() + "T00:00:00"
                ),
                "begin_timezone": (
                    str(begin.tzinfo)
                    if isinstance(begin, datetime) and begin.tzinfo
                    else None
                ),
                "end": (
                    end.isoformat()
                    if isinstance(end, datetime)
                    else (end.isoformat() + "T00:00:00" if end else None)
                ),
                "end_timezone": (
                    str(end.tzinfo)
                    if isinstance(end, datetime) and end.tzinfo
                    else None
                ),
                "duration": (
                    str(component.get("duration"))
                    if component.get("duration")
                    else None
                ),
                "location": str(component.get("location")),
                "description": str(component.get("description")),
                "created": (
                    component.get("created").dt.isoformat()
                    if component.get("created")
                    else None
                ),
                "last_modified": (
                    component.get("last-modified").dt.isoformat()
                    if component.get("last-modified")
                    else None
                ),
                "uid": str(component.get("uid")),
                "url": str(component.get("url")),
                "organizer": str(component.get("organizer")),
                "organizer_email": (
                    component.get("organizer").params["CN"]
                    if component.get("organizer")
                    and "CN" in component.get("organizer").params
                    else None
                ),
                "attendees": (
                    [str(attendee) for attendee in component.get("attendee")]
                    if component.get("attendee")
                    else None
                ),
                "categories": (
                    list(component.get("categories"))
                    if component.get("categories")
                    else None
                ),
                "status": str(component.get("status")),
                "transparent": str(component.get("transp")),
                "alarms": (
                    [str(alarm) for alarm in component.get("valarm")]
                    if component.get("valarm")
                    else None
                ),
                "classification": str(component.get("class")),
            }
            calendar_data["events"].append(event_details)

    return json.dumps(calendar_data, indent=4)


# Usage
ics_file_path = "/home/aashish/Documents/ics/parser/calendar.ics"
json_output = parse_ics_to_json(ics_file_path)
print(json_output)
