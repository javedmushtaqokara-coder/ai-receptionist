"""Build the Retell LLM update for Miami Kitchen & Bath (prompt + Cal.com tools).

Usage: python3 -I make_llm_update.py > api/update-retell-llm.request.json
No secrets in here.
"""
import json
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
PROMPT = (HERE.parent / "draft" / "prompt.md").read_text()
APP = "app_7fc8a1b6f0116745fda3fbfd"   # Cal.com connection in Retell (shared account)
EVENT = "8039591"                       # "Miami Kitchen & Bath Free In-Home Estimate"
TZ = "America/New_York"
LOCAL = "as a local Miami time in ISO 8601 format (YYYY-MM-DDTHH:MM:SS), without converting to UTC."


def s(desc=None, const=None, enum=None):
    p = {"type": "string"}
    if const is not None:
        p["const"] = const
    if desc:
        p["description"] = desc
    if enum:
        p["enum"] = enum
    return p


def obj(props, req):
    return {"type": "object", "properties": props, "required": req}


def tool(name, template, params, description, msg):
    return {"type": "integration_app", "name": name, "app_id": APP, "provider": "calcom",
            "app_tool_template_name": template, "parameters": params, "description": description,
            "speak_during_execution": True, "execution_message_description": msg,
            "execution_message_type": "prompt", "speak_after_execution": True}


tools = [
    tool("check_availability", "check_calcom_availability",
         [obj({"event_type_id": s(const=EVENT),
               "start_time": s("Start of the window to search, " + LOCAL),
               "end_time": s("End of the window, usually 3 to 5 days after the start, " + LOCAL),
               "timezone": s(const=TZ)}, ["event_type_id", "start_time", "end_time", "timezone"])],
         "Check open times for the free in-home estimate. Call before offering any times.",
         "Briefly say you're checking the calendar, in the caller's language."),
    tool("book_appointment", "book_calcom_appointment",
         [obj({"event_type_id": s(const=EVENT)}, ["event_type_id"]),
          obj({"time": s("The visit start time the caller agreed to, " + LOCAL),
               "timezone": s(const=TZ),
               "attendee_language": s("es if the caller is speaking Spanish, otherwise en.", enum=["en", "es"]),
               "name": s("The caller's full name."),
               "email": s("The caller's email, confirmed by spelling it back."),
               "attendeePhoneNumber": s("The caller's confirmed phone number in E.164 format, e.g. +13055551234."),
               "projectAddress": s("The full project address including city."),
               "notes": s("Project summary: type, property and building, timeline, budget, how they heard about us.")},
              ["time", "timezone", "name", "email", "attendeePhoneNumber", "projectAddress"])],
         "Book the free in-home estimate after the caller chose a time and gave name, phone, address and email.",
         "Briefly say you're booking it now, in the caller's language."),
    tool("find_bookings", "list_calcom_bookings",
         [obj({"attendee_email": s("The email the caller booked with, confirmed by spelling it back."),
               "start_time": s("Start of the search, normally the start of today, " + LOCAL),
               "end_time": s("End of the search, normally 30 days after today, " + LOCAL),
               "timezone": s(const=TZ)}, ["attendee_email", "start_time", "end_time", "timezone"])],
         "Find the caller's upcoming visits by the email they booked with. Use before rescheduling or cancelling.",
         "Briefly say you're looking up their visit, in the caller's language."),
    tool("reschedule_booking", "reschedule_calcom_booking",
         [obj({"booking_uid": s("The booking_uid of the visit the caller confirmed, from find_bookings."),
               "start": s("The new start time the caller agreed to, " + LOCAL),
               "timezone": s(const=TZ),
               "reschedule_reason": s("A short reason for rescheduling.")}, ["booking_uid", "start", "timezone"])],
         "Move a confirmed visit to a new time the caller agreed to. Check availability first.",
         "Briefly say you're moving it now, in the caller's language."),
    tool("cancel_booking", "cancel_calcom_booking",
         [obj({"booking_uid": s("The booking_uid of the visit the caller confirmed, from find_bookings."),
               "cancellation_reason": s("A short reason for cancelling.")}, ["booking_uid", "cancellation_reason"])],
         "Cancel a visit after the caller confirmed which one and that they want to cancel.",
         "Briefly say you're cancelling it now, in the caller's language."),
    {"type": "end_call", "name": "end_call",
     "description": "End the call after saying goodbye, or when the caller is clearly spam."},
]

json.dump({"general_prompt": PROMPT, "general_tools": tools}, sys.stdout, indent=2)
