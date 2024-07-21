import calendar
import json
from datetime import datetime

from icalendar import Calendar


def format_value(value):
    if isinstance(value, datetime):
        return value.strftime("%Y-%m-%dT%H:%M:%S")
    elif isinstance(value, (list, tuple)):
        return [format_value(v) for v in value]
    elif isinstance(value, dict):
        return {k: format_value(v) for k, v in value.items()}
    elif hasattr(value, "to_ical"):
        return value.to_ical().decode()
    return value


def rearrange_name(name):
    if "," in name:
        parts = name.split(",")
        return f"{parts[1].strip()} {parts[0].strip()}"
    return name


def parse_icalendar(file_path):
    with open(file_path, "rb") as file:
        calendar_data = Calendar.from_ical(file.read())

    event_list = []

    for component in calendar_data.walk():
        if component.name == "VEVENT":
            attendees = component.get("ATTENDEE", [])
            mandatory_attendees = {
                "ALL": set(),
                "ACPT": set(),
                "DECN": set(),
                "TENT": set(),
            }
            optional_attendees = {
                "ALL": set(),
                "ACPT": set(),
                "DECN": set(),
                "TENT": set(),
            }

            for attendee in attendees:
                if isinstance(attendee, str):
                    email = attendee.replace("mailto:", "")
                    role = "REQ-PARTICIPANT"
                    partstat = "NEEDS-ACTION"
                else:
                    email = attendee.to_ical().decode().replace("mailto:", "")
                    role = attendee.params.get("ROLE", "OPT-PARTICIPANT")
                    partstat = attendee.params.get("PARTSTAT", "NEEDS-ACTION")

                if role == "REQ-PARTICIPANT":
                    mandatory_attendees["ALL"].add(email)
                    if partstat == "ACCEPTED":
                        mandatory_attendees["ACPT"].add(email)
                    elif partstat == "DECLINED":
                        mandatory_attendees["DECN"].add(email)
                    elif partstat == "TENTATIVE":
                        mandatory_attendees["TENT"].add(email)
                else:
                    optional_attendees["ALL"].add(email)
                    if partstat == "ACCEPTED":
                        optional_attendees["ACPT"].add(email)
                    elif partstat == "DECLINED":
                        optional_attendees["DECN"].add(email)
                    elif partstat == "TENTATIVE":
                        optional_attendees["TENT"].add(email)

            event_details = {
                "UID": format_value(component.get("UID")),
                "Class": format_value(component.get("CLASS")),
                "Created": format_value(component.get("CREATED")),
                "DTStamp": format_value(component.get("DTSTAMP")),
                "Last-Modified": format_value(component.get("LAST-MODIFIED")),
                "Location": format_value(component.get("LOCATION")),
                "Organizer": {
                    "CN": (
                        format_value(component.get("ORGANIZER").params.get("CN"))
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
                "Time_Zone_ID": format_value(component.get("TZID")),
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
                        "ALL": list(mandatory_attendees["ALL"]),
                        "ACPT": list(mandatory_attendees["ACPT"]),
                        "DECN": list(mandatory_attendees["DECN"]),
                        "TENT": list(mandatory_attendees["TENT"]),
                    },
                },
                "OptionalAttendee": {
                    "mail": {
                        "ALL": list(optional_attendees["ALL"]),
                        "ACPT": list(optional_attendees["ACPT"]),
                        "DECN": list(optional_attendees["DECN"]),
                        "TENT": list(optional_attendees["TENT"]),
                    },
                },
            }

            event_list.append(event_details)

    return event_list


# Example usage
file_path = "/home/aashish/Documents/ics/parser/calendar3.ics"
events = parse_icalendar(file_path)
print(json.dumps(events, indent=4))
