import json

import ics


def parse_icalendar(file_path):
    with open(file_path, "r") as file:
        calendar_data = file.read()

    calendar = ics.Calendar(calendar_data)
    events = calendar.events

    event_list = []

    for event in events:
        event_details = {
            "UID": getattr(event, "uid", None),
            "Class": getattr(event, "classification", None),
            "Created": (
                event.created.strftime("%Y-%m-%dT%H:%M:%S")
                if getattr(event, "created", None)
                else None
            ),
            "DTStamp": (
                event.dtstamp.strftime("%Y-%m-%dT%H:%M:%S")
                if getattr(event, "dtstamp", None)
                else None
            ),
            "Last-Modified": (
                event.last_modified.strftime("%Y-%m-%dT%H:%M:%S")
                if getattr(event, "last_modified", None)
                else None
            ),
            "Location": getattr(event, "location", None),
            "Organizer": {
                "CN": (
                    event.organizer.common_name
                    if getattr(event, "organizer", None)
                    else None
                ),
                "mail": (
                    event.organizer.email if getattr(event, "organizer", None) else None
                ),
            },
            "NameEvent": getattr(event, "name", None),
            "Description": getattr(event, "description", None),
            "Time_Zone_ID": getattr(event, "timezone", None),
            "Begin_Time": (
                event.begin.strftime("%Y-%m-%dT%H:%M:%S")
                if getattr(event, "begin", None)
                else None
            ),
            "End_Time": (
                event.end.strftime("%Y-%m-%dT%H:%M:%S")
                if getattr(event, "end", None)
                else None
            ),
            "Duration": str(getattr(event, "duration", None)),
            "RRule": getattr(event, "rrule", None),
            "Sequence": getattr(event, "sequence", None),
            "Status": getattr(event, "status", None),
            "Transp_Time": getattr(event, "transparency", None),
            "BusyStatus_OTL": event.extra("X-MICROSOFT-CDO-BUSYSTATUS"),
            "IntendedBusyStatus_OTL": event.extra("X-MICROSOFT-CDO-INTENDEDSTATUS"),
            "MandatoryAttendee": {
                "mail": {
                    "ALL": ";".join(
                        [
                            attendee.email
                            for attendee in event.attendees
                            if attendee.role == "REQ-PARTICIPANT"
                        ]
                    ),
                    "ACPT": ";".join(
                        [
                            attendee.email
                            for attendee in event.attendees
                            if attendee.role == "REQ-PARTICIPANT"
                            and attendee.participation_status == "ACCEPTED"
                        ]
                    ),
                    "DECN": ";".join(
                        [
                            attendee.email
                            for attendee in event.attendees
                            if attendee.role == "REQ-PARTICIPANT"
                            and attendee.participation_status == "DECLINED"
                        ]
                    ),
                    "TENT": ";".join(
                        [
                            attendee.email
                            for attendee in event.attendees
                            if attendee.role == "REQ-PARTICIPANT"
                            and attendee.participation_status == "TENTATIVE"
                        ]
                    ),
                },
                "CN": {
                    "ALL": ";".join(
                        [
                            attendee.common_name
                            for attendee in event.attendees
                            if attendee.role == "REQ-PARTICIPANT"
                        ]
                    ),
                    "ACPT": ";".join(
                        [
                            attendee.common_name
                            for attendee in event.attendees
                            if attendee.role == "REQ-PARTICIPANT"
                            and attendee.participation_status == "ACCEPTED"
                        ]
                    ),
                    "DECN": ";".join(
                        [
                            attendee.common_name
                            for attendee in event.attendees
                            if attendee.role == "REQ-PARTICIPANT"
                            and attendee.participation_status == "DECLINED"
                        ]
                    ),
                    "TENT": ";".join(
                        [
                            attendee.common_name
                            for attendee in event.attendees
                            if attendee.role == "REQ-PARTICIPANT"
                            and attendee.participation_status == "TENTATIVE"
                        ]
                    ),
                },
            },
            "OptionalAttendee_mail": {
                "mail": {
                    "ALL": ";".join(
                        [
                            attendee.email
                            for attendee in event.attendees
                            if attendee.role == "OPT-PARTICIPANT"
                        ]
                    ),
                    "ACPT": ";".join(
                        [
                            attendee.email
                            for attendee in event.attendees
                            if attendee.role == "OPT-PARTICIPANT"
                            and attendee.participation_status == "ACCEPTED"
                        ]
                    ),
                    "DECN": ";".join(
                        [
                            attendee.email
                            for attendee in event.attendees
                            if attendee.role == "OPT-PARTICIPANT"
                            and attendee.participation_status == "DECLINED"
                        ]
                    ),
                    "TENT": ";".join(
                        [
                            attendee.email
                            for attendee in event.attendees
                            if attendee.role == "OPT-PARTICIPANT"
                            and attendee.participation_status == "TENTATIVE"
                        ]
                    ),
                },
                "CN": {
                    "ALL": ";".join(
                        [
                            attendee.common_name
                            for attendee in event.attendees
                            if attendee.role == "OPT-PARTICIPANT"
                        ]
                    ),
                    "ACPT": ";".join(
                        [
                            attendee.common_name
                            for attendee in event.attendees
                            if attendee.role == "OPT-PARTICIPANT"
                            and attendee.participation_status == "ACCEPTED"
                        ]
                    ),
                    "DECN": ";".join(
                        [
                            attendee.common_name
                            for attendee in event.attendees
                            if attendee.role == "OPT-PARTICIPANT"
                            and attendee.participation_status == "DECLINED"
                        ]
                    ),
                    "TENT": ";".join(
                        [
                            attendee.common_name
                            for attendee in event.attendees
                            if attendee.role == "OPT-PARTICIPANT"
                            and attendee.participation_status == "TENTATIVE"
                        ]
                    ),
                },
            },
            "Alarm": None,
        }

        if getattr(event, "alarms", None):
            alarm = event.alarms[0]
            event_details["Alarm"] = {
                "Trigger": (
                    alarm.trigger.strftime("%Y-%m-%dT%H:%M:%S")
                    if getattr(alarm, "trigger", None)
                    else None
                ),
                "Action": getattr(alarm, "action", None),
                "Description": getattr(alarm, "description", None),
            }

        event_list.append(event_details)

    return event_list


# Example usage
file_path = "/home/aashish/Documents/ics/parser/calendar.ics"
events = parse_icalendar(file_path)
print(json.dumps(events, indent=4))
