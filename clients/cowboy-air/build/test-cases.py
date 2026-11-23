"""Simulation test cases for Cowboy Air. Prints one JSON request body per line.

Usage: python3 -I test-cases.py <llm_id>
Cal.com tools are mocked so no real bookings are made.
"""
import json
import sys

LLM = sys.argv[1]
ENGINE = {"type": "retell-llm", "llm_id": LLM}

SLOTS = json.dumps({"available_slots": ["2026-11-25T09:00:00-06:00", "2026-11-25T10:00:00-06:00", "2026-11-25T13:00:00-06:00", "2026-11-26T09:00:00-06:00"]})
BOOKED = json.dumps({"booking_uid": "test-uid-1", "status": "accepted", "start_time": "2026-11-25T10:00:00-06:00"})
FOUND = json.dumps({"bookings": [{"booking_uid": "test-uid-1", "title": "Cowboy Air Service Visit", "status": "accepted", "start_time": "2026-11-25T10:00:00-06:00", "end_time": "2026-11-25T11:00:00-06:00"}], "count": 1})
NONE = json.dumps({"bookings": [], "count": 0})
OK = json.dumps({"status": "success"})


def mock(tool, output):
    return {"tool_name": tool, "input_match_rule": {"type": "any"}, "output": output}


STD_MOCKS = [mock("check_availability", SLOTS), mock("book_appointment", BOOKED),
             mock("find_bookings", FOUND), mock("reschedule_booking", OK), mock("cancel_booking", OK)]
OPEN = {"current_time": "Tuesday, November 24, 2026 at 10:15 AM CST"}
CLOSED = {"current_time": "Saturday, November 28, 2026 at 10:05 PM CST"}

CASES = [
    ("booking-ac-not-cooling", OPEN, STD_MOCKS,
     "You are Maria Lopez, a homeowner at 4512 Belt Line Road, Dallas, TX 75254. Your phone is +12145550134 and your email is maria.lopez@example.com. Your AC is blowing warm air since this morning. You want someone out as soon as possible. Accept the first time offered. Be friendly.",
     ["The agent called check_availability before mentioning any appointment time.",
      "The agent collected name, phone, service address and email, and spelled the email back.",
      "The agent called book_appointment and then read back the day, time and address.",
      "The agent did not diagnose the problem or quote a firm price."]),
    ("booking-rejects-all-slots", OPEN, STD_MOCKS,
     "You are Tom Reed in Plano. You want a tune-up but only on a Sunday afternoon. Reject every time you're offered.",
     ["The agent did not book anything.",
      "The agent offered to take a message or have the office call back."]),
    ("booking-no-email", OPEN, STD_MOCKS,
     "You are Earl Jenkins, 78, in Mesquite. You need your heater looked at. You don't have an email address and say so when asked.",
     ["The agent did not call book_appointment.",
      "The agent took a message with name, phone and reason so the office can call back to schedule."]),
    ("reschedule-visit", OPEN, STD_MOCKS,
     "You are Maria Lopez. Your email is maria.lopez@example.com. You have a visit tomorrow at 10 AM and want to move it to the following day in the morning.",
     ["The agent asked for the email and called find_bookings before changing anything.",
      "The agent confirmed the existing visit before rescheduling.",
      "The agent called reschedule_booking and read back the new time."]),
    ("cancel-visit", OPEN, STD_MOCKS,
     "You are Maria Lopez, email maria.lopez@example.com. You fixed the problem yourself and want to cancel your visit.",
     ["The agent found the booking with find_bookings and confirmed it.",
      "The agent confirmed the caller wants to cancel before calling cancel_booking.",
      "The agent offered to book another time."]),
    ("reschedule-not-found", OPEN, [mock("find_bookings", NONE)] + STD_MOCKS[:2],
     "You want to reschedule your appointment. Your email is jdoe@example.com. You don't remember when it is.",
     ["The agent did not invent a booking.",
      "The agent offered to take a message for the office."]),
    ("faq-diagnostic-fee", OPEN, STD_MOCKS,
     "You want to know how much it costs just to have someone come look at your AC, and whether they do military discounts.",
     ["The agent gave the $89 to $149 typical diagnostic range and did not present it as a firm price.",
      "The agent said military discounts are available.",
      "The agent offered to book a visit."]),
    ("faq-out-of-area", OPEN, STD_MOCKS,
     "You live in Waco, Texas, and ask whether Cowboy Air can come out.",
     ["The agent did not book a visit in Waco.",
      "The agent explained the Dallas-Fort Worth service area and offered to take details for the office to confirm."]),
    ("after-hours-message", CLOSED, STD_MOCKS,
     "You are Dana Kim. You want a quote for a new mini-split in your garage. Ask if anyone is there.",
     ["The agent said the office is closed and when it reopens.",
      "The agent still helped, by booking a visit or taking a message with name, number and reason."]),
    ("after-hours-emergency", CLOSED, STD_MOCKS,
     "You are Linda Park at 2210 Oak Lawn Ave, Dallas. Phone +12145550199. Your AC died, it's 88 degrees inside and your 80-year-old mother lives with you. You're worried.",
     ["The agent treated the call as an emergency and took name, phone, address and what's happening.",
      "The agent said the on-call team will call back and did not promise an exact time.",
      "The agent mentioned the after-hours premium is disclosed before dispatch."]),
    ("danger-gas-smell", OPEN, STD_MOCKS,
     "You smell gas near your furnace and want someone to come look at the heater.",
     ["The agent's first instruction was to leave the home and call 911 or the gas company."]),
]

for name, dv, mocks, user_prompt, metrics in CASES:
    print(json.dumps({
        "name": "cowboy-air: " + name,
        "response_engine": ENGINE,
        "user_prompt": user_prompt,
        "metrics": metrics,
        "dynamic_variables": dv,
        "tool_mocks": mocks,
    }))
