"""Build the Retell LLM request body for Cowboy Air.

Usage: python3 -I make_llm.py <model> > llm.json
Reads draft/prompt.md next to this folder. No secrets in here.
"""
import json
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
PROMPT = (HERE.parent / "draft" / "prompt.md").read_text()
MODEL = sys.argv[1]
BACKUP = sys.argv[2] if len(sys.argv) > 2 else None

APP = "app_7fc8a1b6f0116745fda3fbfd"   # Cal.com connection in Retell
EVENT = "8035996"                       # Cal.com "Cowboy Air Service Visit"
TZ = "America/Chicago"
LOCAL_DT = "as a local Dallas time in ISO 8601 format (YYYY-MM-DDTHH:MM:SS), without converting to UTC."


def obj(props, required):
    return {"type": "object", "properties": props, "required": required}


def s(desc=None, const=None):
    p = {"type": "string"}
    if const is not None:
        p["const"] = const
    if desc:
        p["description"] = desc
    return p


def cal_tool(name, template, params, description, wait_msg, response_variables=None):
    t = {
        "type": "integration_app",
        "name": name,
        "app_id": APP,
        "provider": "calcom",
        "app_tool_template_name": template,
        "parameters": params,
        "description": description,
        "speak_during_execution": True,
        "execution_message_description": wait_msg,
        "execution_message_type": "static_text",
        "speak_after_execution": True,
    }
    if response_variables:
        t["response_variables"] = response_variables
    return t


tools = [
    cal_tool(
        "check_availability", "check_calcom_availability",
        [obj({
            "event_type_id": s(const=EVENT),
            "start_time": s("Start of the window to search, " + LOCAL_DT),
            "end_time": s("End of the window to search, usually 3 to 5 days after the start, " + LOCAL_DT),
            "timezone": s(const=TZ),
        }, ["event_type_id", "start_time", "end_time", "timezone"])],
        "Check open service-visit times. Call this before offering any times.",
        "Let me check the schedule for you.",
    ),
    cal_tool(
        "book_appointment", "book_calcom_appointment",
        [
            obj({"event_type_id": s(const=EVENT)}, ["event_type_id"]),
            obj({
                "time": s("The visit start time the caller agreed to, " + LOCAL_DT),
                "timezone": s(const=TZ),
                "name": s("The caller's full name."),
                "email": s("The caller's email address, confirmed by spelling it back."),
                "attendeePhoneNumber": s("The caller's confirmed phone number in E.164 format, e.g. +12145551234."),
                "serviceAddress": s("The full service address including city."),
                "notes": s("One line describing the problem or the visit type, plus anything the tech should know (gate code, pets)."),
            }, ["time", "timezone", "name", "email", "attendeePhoneNumber", "serviceAddress"]),
        ],
        "Book a service visit after the caller has chosen a time and given name, phone, service address and email.",
        "Booking that for you now.",
    ),
    cal_tool(
        "find_bookings", "list_calcom_bookings",
        [obj({
            "attendee_email": s("The email address the caller booked with, confirmed by spelling it back."),
            "start_time": s("Start of the search window, normally the start of today, " + LOCAL_DT),
            "end_time": s("End of the search window, normally 30 days after today, " + LOCAL_DT),
            "timezone": s(const=TZ),
        }, ["attendee_email", "start_time", "end_time", "timezone"])],
        "Find the caller's upcoming visits by the email they booked with. Use before rescheduling or cancelling.",
        "Let me pull up your appointment.",
    ),
    cal_tool(
        "reschedule_booking", "reschedule_calcom_booking",
        [obj({
            "booking_uid": s("The booking_uid of the visit the caller confirmed, from find_bookings."),
            "start": s("The new start time the caller agreed to, " + LOCAL_DT),
            "timezone": s(const=TZ),
            "reschedule_reason": s("A short reason for rescheduling."),
        }, ["booking_uid", "start", "timezone"])],
        "Move a confirmed visit to a new time the caller agreed to. Check availability first.",
        "Moving that for you now.",
    ),
    cal_tool(
        "cancel_booking", "cancel_calcom_booking",
        [obj({
            "booking_uid": s("The booking_uid of the visit the caller confirmed, from find_bookings."),
            "cancellation_reason": s("A short reason for cancelling."),
        }, ["booking_uid", "cancellation_reason"])],
        "Cancel a visit after the caller has confirmed which one and that they want to cancel.",
        "Cancelling that now.",
    ),
    {
        "type": "end_call",
        "name": "end_call",
        "description": "End the call after saying goodbye, or when the caller is clearly spam or has hung up.",
    },
]

model_config = {"type": "cascading", "primary": {"model": MODEL, "tier": "fast"}}
if BACKUP:
    model_config["backup"] = {"model": BACKUP, "tier": "standard", "kick_in_timeout_ms": 1500}

body = {
    "model_config": model_config,
    "start_speaker": "agent",
    "begin_message": "Thanks for calling Cowboy Air Condition and Heating, this is Jessie. How can I help you today?",
    "general_prompt": PROMPT,
    "general_tools": tools,
}
json.dump(body, sys.stdout, indent=2)
