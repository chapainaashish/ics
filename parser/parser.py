import json

from ics import Calendar


def parse_ics_to_json(ics_file_path):
    with open(ics_file_path, "r") as file:
        ics_content = file.read()

    calendar = Calendar(ics_content)
    calendar_data = {
        "events": [],
        "todos": [],
        "journals": [],
        "free_busy": [],
        "timezones": [],
        "alarms": [],
    }

    for event in calendar.events:
        event_details = {
            "name": event.name,
            "begin": event.begin.isoformat(),
            "end": event.end.isoformat() if event.end else None,
            "location": event.location,
            "description": event.description,
            "organizer": event.organizer if hasattr(event, "organizer") else None,
            "attendees": (
                [attendee for attendee in event.attendees]
                if hasattr(event, "attendees")
                else None
            ),
        }
        calendar_data["events"].append(event_details)

    # for todo in calendar.todos:
    #     todo_details = {
    #         "name": todo.name,
    #         "due": todo.due.isoformat() if todo.due else None,
    #         "status": todo.status,
    #         "description": todo.description,
    #     }
    #     calendar_data["todos"].append(todo_details)

    # for journal in calendar.journals:
    #     journal_details = {
    #         "date": journal.date.isoformat() if journal.date else None,
    #         "summary": journal.summary,
    #         "description": journal.description,
    #     }
    #     calendar_data["journals"].append(journal_details)

    # for freebusy in calendar.free_busy:
    #     freebusy_details = {
    #         "start": freebusy.start.isoformat(),
    #         "end": freebusy.end.isoformat(),
    #         "freebusy": freebusy.freebusy,
    #     }
    #     calendar_data["free_busy"].append(freebusy_details)

    # for timezone in calendar.timezones:
    #     timezone_details = {
    #         "tzid": timezone.tzid,
    #         "offset_from": timezone.offset_from,
    #         "offset_to": timezone.offset_to,
    #         "tzname": timezone.tzname,
    #     }
    #     calendar_data["timezones"].append(timezone_details)

    # for alarm in calendar.alarms:
    #     alarm_details = {
    #         "action": alarm.action,
    #         "trigger": alarm.trigger.isoformat() if alarm.trigger else None,
    #         "description": alarm.description,
    #     }
    #     calendar_data["alarms"].append(alarm_details)

    return json.dumps(calendar_data, indent=4)


# Usage
ics_file_path = "/home/aashish/Documents/ics/parser/calendar.ics"
json_output = parse_ics_to_json(ics_file_path)
print(json_output)
