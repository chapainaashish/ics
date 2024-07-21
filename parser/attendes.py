import json

from icalendar import Calendar


def parse_ics(file_path):
    with open(file_path, "r") as file:
        cal = Calendar.from_ical(file.read())

    events = []

    for component in cal.walk():
        if component.name == "VEVENT":
            event_info = {
                "summary": component.get("summary"),
                "start": component.get("dtstart").dt.isoformat(),
                "end": component.get("dtend").dt.isoformat(),
                "attendees": {
                    "all": [],
                    "accepted": [],
                    "declined": [],
                    "tentative": [],
                },
            }

            attendees = component.get("attendee")
            if attendees:
                if not isinstance(attendees, list):
                    attendees = [attendees]

                for attendee in attendees:
                    email = str(attendee)
                    role = attendee.params.get("ROLE", "REQ-PARTICIPANT")
                    status = attendee.params.get("PARTSTAT", "NEEDS-ACTION")

                    attendee_info = {"email": email, "role": role, "status": status}

                    # Categorize attendee based on status
                    if status == "ACCEPTED":
                        event_info["attendees"]["accepted"].append(attendee_info)
                    elif status == "DECLINED":
                        event_info["attendees"]["declined"].append(attendee_info)
                    elif status == "TENTATIVE":
                        event_info["attendees"]["tentative"].append(attendee_info)

                    # Include all attendees in the general list
                    event_info["attendees"]["all"].append(attendee_info)

            events.append(event_info)

    return events


def print_events(events):
    print(json.dumps(events, indent=4))


# Example usage:
file_path = "/home/aashish/Documents/ics/parser/calendar2.ics"

events_data = parse_ics(file_path)
print_events(events_data)
