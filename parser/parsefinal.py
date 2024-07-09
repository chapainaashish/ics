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


def get_attendees(attendees, role, partstat=None):
    result = []
    if isinstance(attendees, str):
        return attendees.replace("mailto:", "")
    for attendee in attendees:
        if isinstance(attendee, str):
            result.append(attendee.replace("mailto:", ""))
        elif attendee.params.get("ROLE") == role:
            if partstat is None or attendee.params.get("PARTSTAT") == partstat:
                result.append(attendee.to_ical().decode().replace("mailto:", ""))
    return (
        ";".join(result)
        if all(isinstance(attendee, str) for attendee in result)
        else result
    )


def get_attendee_names(attendees, role, partstat=None):
    result = []
    if isinstance(attendees, str):
        return attendees.replace("mailto:", "")
    for attendee in attendees:
        if isinstance(attendee, str):
            result.append(attendee.replace("mailto:", ""))
        elif attendee.params.get("ROLE") == role:
            if partstat is None or attendee.params.get("PARTSTAT") == partstat:
                result.append(attendee.params["CN"])
    return (
        ";".join(result)
        if all(isinstance(attendee, str) for attendee in result)
        else result
    )


def parse_icalendar(file_path):
    with open(file_path, "rb") as file:
        calendar = Calendar.from_ical(file.read())

    event_list = []

    for component in calendar.walk():
        if component.name == "VEVENT":
            attendees = component.get("ATTENDEE", [])
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
                "Begin_Time": format_value(component.get("DTSTART")),
                "End_Time": format_value(component.get("DTEND")),
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
                "Categories": format_value(component.get("CATEGORIES")),
                "Recurrence-ID": format_value(component.get("RECURRENCE-ID")),
            }

            event_list.append(event_details)

    return event_list


# Example usage
file_path = "/home/aashish/Documents/ics/parser/calendar6.ics"
events = parse_icalendar(file_path)
print(json.dumps(events, indent=4))
