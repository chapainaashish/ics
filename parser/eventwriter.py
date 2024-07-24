import json
from datetime import date, datetime

from icalendar import Calendar


def format_value(value):
    if isinstance(value, datetime):
        return value.strftime("%Y-%m-%dT%H:%M:%S")
    elif isinstance(value, date):
        return value.strftime("%Y-%m-%d")
    elif isinstance(value, (list, tuple)):
        return [format_value(v) for v in value]
    elif isinstance(value, dict):
        return {k: format_value(v) for k, v in value.items()}
    elif hasattr(value, "to_ical"):
        return (
            value.to_ical().decode()
            if isinstance(value.to_ical(), bytes)
            else value.to_ical()
        )
    return value

def get_attendees(attendees, role, partstat=None):
    result = []
    if isinstance(attendees, str):
        if role in ["REQ-PARTICIPANT", "OPT-PARTICIPANT"]:
            if partstat is None or partstat == "NEEDS-ACTION":
                result.append(attendees.replace("mailto:", ""))
    else:
        if not isinstance(attendees, list):
            attendees = [attendees]

        for attendee in attendees:
            attendee_role = attendee.params.get("ROLE", "REQ-PARTICIPANT")
            if attendee_role == role:
                status = attendee.params.get("PARTSTAT", "NEEDS-ACTION")
                if partstat is None or status == partstat:
                    result.append(attendee.to_ical().decode().replace("mailto:", ""))

    return ";".join(result) if all(isinstance(a, str) for a in result) else result

def rearrange_name(name):
    if "," in name:
        parts = name.split(",")
        return f"{parts[1].strip()} {parts[0].strip()}"
    return name

def get_attendee_names(attendees, role, partstat=None):
    result = []
    if isinstance(attendees, str):
        if role in ["REQ-PARTICIPANT", "OPT-PARTICIPANT"]:
            if partstat is None or partstat == "NEEDS-ACTION":
                result.append(attendees.replace("mailto:", ""))
    else:
        if not isinstance(attendees, list):
            attendees = [attendees]

        for attendee in attendees:
            attendee_role = attendee.params.get("ROLE", "REQ-PARTICIPANT")
            if attendee_role == role:
                status = attendee.params.get("PARTSTAT", "NEEDS-ACTION")
                if partstat is None or status == partstat:
                    name = attendee.params.get("CN", "")
                    rearranged_name = rearrange_name(name)
                    result.append(rearranged_name)

    return ";".join(result) if all(isinstance(a, str) for a in result) else result

def parse_icalendar(file_path):
    with open(file_path, "rb") as file:
        calendar_data = Calendar.from_ical(file.read())

    timezone_map = {}
    event_list = []

    for component in calendar_data.walk():
        if component.name == "VTIMEZONE":
            timezone_id = component.get("TZID")
            timezone_map[timezone_id] = {"standard": [], "daylight": []}
            for sub_component in component.subcomponents:
                if sub_component.name == "STANDARD":
                    timezone_map[timezone_id]["standard"].append(
                        {
                            "DTSTART": format_value(sub_component.get("DTSTART").dt),
                            "TZOFFSETFROM": format_value(
                                sub_component.get("TZOFFSETFROM")
                            ),
                            "TZOFFSETTO": format_value(sub_component.get("TZOFFSETTO")),
                            "RRULE": format_value(sub_component.get("RRULE")),
                        }
                    )
                if sub_component.name == "DAYLIGHT":
                    timezone_map[timezone_id]["daylight"].append(
                        {
                            "DTSTART": format_value(sub_component.get("DTSTART").dt),
                            "TZOFFSETFROM": format_value(
                                sub_component.get("TZOFFSETFROM")
                            ),
                            "TZOFFSETTO": format_value(sub_component.get("TZOFFSETTO")),
                            "RRULE": format_value(sub_component.get("RRULE")),
                        }
                    )

    for component in calendar_data.walk():
        if component.name == "VEVENT":
            attendees = component.get("ATTENDEE", [])

            alarms = []
            for sub_component in component.subcomponents:
                if sub_component.name == "VALARM":
                    alarms.append(
                        {
                            "Trigger": format_value(sub_component.get("TRIGGER")),
                            "Action": format_value(sub_component.get("ACTION")),
                            "Description": format_value(
                                sub_component.get("DESCRIPTION")
                            ),
                        }
                    )

            timezone_id = format_value(component.get("DTSTART").params.get("TZID"))
            event_details = {
                "UID": format_value(component.get("UID")),
                "Class": format_value(component.get("CLASS")),
                "Created": format_value(component.get("CREATED")),
                "DTStamp": format_value(component.get("DTSTAMP")),
                "Last-Modified": format_value(component.get("LAST-MODIFIED")),
                "Location": format_value(component.get("LOCATION")),
                "Organizer": {
                    "CN": (
                        rearrange_name(
                            format_value(component.get("ORGANIZER").params.get("CN"))
                        )
                        if component.get("ORGANIZER")
                        else None
                    ),
                    "mail": (
                        format_value(
                            component.get("ORGANIZER")
                            .to_ical()
                            .decode()
                            .replace("mailto:", "")
                        )
                        if component.get("ORGANIZER")
                        else None
                    ),
                },
                "NameEvent": format_value(component.get("SUMMARY")),
                "Description": format_value(component.get("DESCRIPTION")),
                "Time_Zone_ID": timezone_id,
                "Begin_Time": format_value(component.get("DTSTART").dt),
                "End_Time": format_value(component.get("DTEND").dt),
                "Duration": format_value(component.get("DURATION")),
                "RRule": format_value(component.get("RRULE")),
                "Sequence": format_value(component.get("SEQUENCE")),
                "Status": format_value(component.get("STATUS")),
                "Transp_Time": format_value(component.get("TRANSP")),
                "BusyStatus_OTL": format_value(
                    component.get("X-MICROSOFT-CDO-BUSYSTATUS")
                ),
                "IntendedBusyStatus_OTL": format_value(
                    component.get("X-MICROSOFT-CDO-INTENDEDSTATUS")
                ),
                "MandatoryAttendee": {
                    "mail": {
                        "ALL": format_value(
                            get_attendees(attendees, "REQ-PARTICIPANT")
                        ),
                        "NA": format_value(
                            get_attendees(attendees, "REQ-PARTICIPANT", "NEEDS-ACTION")
                        ),
                        "ACPT": format_value(
                            get_attendees(attendees, "REQ-PARTICIPANT", "ACCEPTED")
                        ),
                        "DECN": format_value(
                            get_attendees(attendees, "REQ-PARTICIPANT", "DECLINED")
                        ),
                        "TENT": format_value(
                            get_attendees(attendees, "REQ-PARTICIPANT", "TENTATIVE")
                        ),
                    },
                    "CN": {
                        "ALL": format_value(
                            get_attendee_names(attendees, "REQ-PARTICIPANT")
                        ),
                        "NA": format_value(
                            get_attendee_names(
                                attendees, "REQ-PARTICIPANT", "NEEDS-ACTION"
                            )
                        ),
                        "ACPT": format_value(
                            get_attendee_names(attendees, "REQ-PARTICIPANT", "ACCEPTED")
                        ),
                        "DECN": format_value(
                            get_attendee_names(attendees, "REQ-PARTICIPANT", "DECLINED")
                        ),
                        "TENT": format_value(
                            get_attendee_names(
                                attendees, "REQ-PARTICIPANT", "TENTATIVE"
                            )
                        ),
                    },
                },
                "OptionalAttendee": {
                    "mail": {
                        "ALL": format_value(
                            get_attendees(attendees, "OPT-PARTICIPANT")
                        ),
                        "NA": format_value(
                            get_attendees(attendees, "OPT-PARTICIPANT", "NEEDS-ACTION")
                        ),
                        "ACPT": format_value(
                            get_attendees(attendees, "OPT-PARTICIPANT", "ACCEPTED")
                        ),
                        "DECN": format_value(
                            get_attendees(attendees, "OPT-PARTICIPANT", "DECLINED")
                        ),
                        "TENT": format_value(
                            get_attendees(attendees, "OPT-PARTICIPANT", "TENTATIVE")
                        ),
                    },
                    "CN": {
                        "ALL": format_value(
                            get_attendee_names(attendees, "OPT-PARTICIPANT")
                        ),
                        "NA": format_value(
                            get_attendee_names(
                                attendees, "OPT-PARTICIPANT", "NEEDS-ACTION"
                            )
                        ),
                        "ACPT": format_value(
                            get_attendee_names(attendees, "OPT-PARTICIPANT", "ACCEPTED")
                        ),
                        "DECN": format_value(
                            get_attendee_names(attendees, "OPT-PARTICIPANT", "DECLINED")
                        ),
                        "TENT": format_value(
                            get_attendee_names(
                                attendees, "OPT-PARTICIPANT", "TENTATIVE"
                            )
                        ),
                    },
                },
                "Alarms": alarms,
            }

            event_list.append(event_details)

    return event_list

file_path = "/home/aashish/Documents/ics/parser/calendar.ics"
events = parse_icalendar(file_path)

# Write to JSON file
json_file_path = "/home/aashish/Documents/ics/parser/calendar_events.json"
with open(json_file_path, "w") as json_file:
    json.dump(events, json_file, indent=4)

print(f"Data successfully written to {json_file_path}")
