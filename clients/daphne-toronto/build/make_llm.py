"""Build the Retell LLM request body for Daphne.

Usage: python3 -I make_llm.py <calcom_app_id_in_workspace> > api/create-retell-llm.request.json
No secrets in here.
"""
import json
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
PROMPT = (HERE.parent / "draft" / "prompt.md").read_text()
APP = sys.argv[1]
EVENT = "8071891"          # Cal.com "Daphne Table Reservation" (90 min, 4 tables per slot)
TZ = "America/Toronto"
LOCAL = "as a local Toronto time in ISO 8601 format (YYYY-MM-DDTHH:MM:SS), without converting to UTC."


def s(desc=None, const=None, enum=None, typ="string"):
    p = {"type": typ}
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


tools = [
    tool("check_availability", "check_calcom_availability",
         [obj({"event_type_id": s(const=EVENT),
               "start_time": s("Start of the window, usually the start of the requested day, " + LOCAL),
               "end_time": s("End of the window, usually the end of the requested day, " + LOCAL),
               "timezone": s(const=TZ)}, ["event_type_id", "start_time", "end_time", "timezone"])],
         "Check open reservation times. Call before offering any times.",
         "Let me check our book for you."),
    tool("book_reservation", "book_calcom_appointment",
         [obj({"event_type_id": s(const=EVENT)}, ["event_type_id"]),
          obj({"time": s("The reservation time the guest agreed to, " + LOCAL),
               "timezone": s(const=TZ),
               "name": s("The guest's full name."),
               "email": s("The guest's email, confirmed by spelling it back."),
               "attendeePhoneNumber": s("The guest's confirmed phone number in E.164 format, e.g. +14165551234."),
               "partySize": s("Number of guests as digits, 1 to 8, e.g. '4'."),
               "seating": s("Seating preference.", enum=["No preference", "Dining room", "Patio", "Bar or lounge"]),
               "notes": s("Occasion, allergies or other requests.")},
              ["time", "timezone", "name", "email", "attendeePhoneNumber", "partySize"])],
         "Book a table after the guest chose a time and gave name, phone, email and party size.",
         "Booking that for you now."),
    tool("find_reservations", "list_calcom_bookings",
         [obj({"attendee_email": s("The email the guest booked with, confirmed by spelling it back."),
               "start_time": s("Start of the search, normally the start of today, " + LOCAL),
               "end_time": s("End of the search, normally 60 days after today, " + LOCAL),
               "timezone": s(const=TZ)}, ["attendee_email", "start_time", "end_time", "timezone"])],
         "Find the guest's upcoming reservations by the email they booked with.",
         "Let me find your reservation."),
    tool("change_reservation", "reschedule_calcom_booking",
         [obj({"booking_uid": s("The booking_uid of the reservation the guest confirmed, from find_reservations."),
               "start": s("The new time the guest agreed to, " + LOCAL),
               "timezone": s(const=TZ),
               "reschedule_reason": s("Short reason, including any new party size.")}, ["booking_uid", "start", "timezone"])],
         "Move a confirmed reservation to a new time the guest agreed to. Check availability first.",
         "Updating that now."),
    tool("cancel_reservation", "cancel_calcom_booking",
         [obj({"booking_uid": s("The booking_uid of the reservation the guest confirmed, from find_reservations."),
               "cancellation_reason": s("A short reason for cancelling.")}, ["booking_uid", "cancellation_reason"])],
         "Cancel a reservation after the guest confirmed which one and that they want to cancel.",
         "Cancelling that now."),
    {"type": "end_call", "name": "end_call",
     "description": "End the call after saying goodbye, or when the caller is clearly spam."},
]

json.dump({
    "model_config": {"type": "cascading",
                     "primary": {"model": "gpt-6.1-sol", "tier": "ultrafast"},
                     "backup": {"model": "gemini-3.8-flash", "tier": "standard", "kick_in_timeout_ms": 1500}},
    "start_speaker": "agent",
    "begin_message": "Good day, thank you for calling DAPHNE, this is Ava. How can I help you?",
    "general_prompt": PROMPT,
    "general_tools": tools,
}, sys.stdout, indent=2)
