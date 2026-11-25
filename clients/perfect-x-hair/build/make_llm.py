"""Build the Retell LLM request body for Perfect X Hair.

Usage: python3 -I make_llm.py <calcom_app_id_in_salon_workspace> > api/create-retell-llm.request.json
No secrets in here.
"""
import json
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
PROMPT = (HERE.parent / "draft" / "prompt.md").read_text()
APP = sys.argv[1]
TZ = "America/Toronto"
LOCAL = "as a local Toronto time in ISO 8601 format (YYYY-MM-DDTHH:MM:SS), without converting to UTC."
TYPES = {   # Cal.com event types (shared account)
    "cut": ("8062514", "Cut and style, 1 hour: haircuts, bangs, blowouts, up-dos, Milbon or scalp treatments"),
    "colour": ("8062515", "Colour or perm, 3 hours: colour, root touch-up, gloss, toner, Korean perms, keratin"),
    "bleach": ("8062517", "Bleach, balayage or highlights, 5 hours"),
}
LOCATIONS = ["Yorkville", "Art Gallery", "Yonge & Sheppard", "Yonge & Empress"]


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
            "execution_message_type": "static_text", "speak_after_execution": True}


tools = []
for key, (event, label) in TYPES.items():
    tools.append(tool(
        f"check_availability_{key}", "check_calcom_availability",
        [obj({"event_type_id": s(const=event),
              "start_time": s("Start of the window to search, " + LOCAL),
              "end_time": s("End of the window, usually 3 days after the start, " + LOCAL),
              "timezone": s(const=TZ)}, ["event_type_id", "start_time", "end_time", "timezone"])],
        f"Check open times for: {label}. Call before offering any times for this length of appointment.",
        "Let me check the schedule."))
    tools.append(tool(
        f"book_{key}", "book_calcom_appointment",
        [obj({"event_type_id": s(const=event)}, ["event_type_id"]),
         obj({"time": s("The start time the caller agreed to, " + LOCAL),
              "timezone": s(const=TZ),
              "name": s("The caller's full name."),
              "email": s("The caller's email, confirmed by spelling it back."),
              "attendeePhoneNumber": s("The caller's confirmed phone number in E.164 format, e.g. +14375551234."),
              "salonLocation": s("The salon location the caller chose.", enum=LOCATIONS),
              "service": s("The exact service from the menu, e.g. 'Digital Perm + Cut'."),
              "stylist": s("The caller's preferred stylist, or empty if none."),
              "notes": s("Anything else the stylist should know, e.g. 'needs consultation', hair history.")},
             ["time", "timezone", "name", "email", "attendeePhoneNumber", "salonLocation", "service"])],
        f"Book: {label}. Use after the caller chose a time and gave name, phone and email.",
        "Booking that for you now."))

tools += [
    tool("find_bookings", "list_calcom_bookings",
         [obj({"attendee_email": s("The email the caller booked with, confirmed by spelling it back."),
               "start_time": s("Start of the search, normally the start of today, " + LOCAL),
               "end_time": s("End of the search, normally 30 days after today, " + LOCAL),
               "timezone": s(const=TZ)}, ["attendee_email", "start_time", "end_time", "timezone"])],
         "Find the caller's upcoming appointments by the email they booked with. Use before rescheduling or cancelling.",
         "Let me pull up your appointment."),
    tool("reschedule_booking", "reschedule_calcom_booking",
         [obj({"booking_uid": s("The booking_uid of the appointment the caller confirmed, from find_bookings."),
               "start": s("The new start time the caller agreed to, " + LOCAL),
               "timezone": s(const=TZ),
               "reschedule_reason": s("A short reason for rescheduling.")}, ["booking_uid", "start", "timezone"])],
         "Move a confirmed appointment to a new time the caller agreed to. Check availability first.",
         "Moving that for you now."),
    tool("cancel_booking", "cancel_calcom_booking",
         [obj({"booking_uid": s("The booking_uid of the appointment the caller confirmed, from find_bookings."),
               "cancellation_reason": s("A short reason for cancelling.")}, ["booking_uid", "cancellation_reason"])],
         "Cancel an appointment after the caller confirmed which one and that they want to cancel.",
         "Cancelling that now."),
    {"type": "end_call", "name": "end_call",
     "description": "End the call after saying goodbye, or when the caller is clearly spam."},
]

json.dump({
    "model_config": {"type": "cascading",
                     "primary": {"model": "gpt-6.1-sol", "tier": "ultrafast"},
                     "backup": {"model": "gemini-3.8-flash", "tier": "standard", "kick_in_timeout_ms": 1500}},
    "start_speaker": "agent",
    "begin_message": "Hi, thank you for calling PERFECT X HAIR, this is Mina. How can I help you today?",
    "general_prompt": PROMPT,
    "general_tools": tools,
}, sys.stdout, indent=2)
