# Cowboy Air: functions

| Function | What it does | Source | Inputs → outputs | Custom? |
|---|---|---|---|---|
| `check_availability` | Open visit times | Cal.com integration `check_calcom_availability` (event type 8035996) | start/end window → `available_slots` | No |
| `book_appointment` | Books a visit | Cal.com `book_calcom_appointment` | time, name, email, phone, service address, notes → booking | No |
| `find_bookings` | Finds the caller's visits | Cal.com `list_calcom_bookings` | **email** and window → bookings | No |
| `reschedule_booking` | Moves a visit | Cal.com `reschedule_calcom_booking` | booking_uid, new start → result | No |
| `cancel_booking` | Cancels a visit | Cal.com `cancel_calcom_booking` | booking_uid, reason → result | No |
| `end_call` | Hangs up | Retell built-in | none | No |
| FAQ | Answers questions | Business facts in the prompt | none | No |
| After-hours behaviour | Closed or open logic, emergency path | Prompt with `{{current_time}}` and agent timezone `America/Chicago` | none | No |
| Message capture | Name, number, reason, urgency, outcome | Retell post-call analysis (9 fields) | Saved on every call | No |
| `notify-owner` | Emails the office each message and emergency | Vercel function on the `call_analyzed` webhook, sending via Resend | Signed webhook → email | **Yes.** Retell has no email tool. **Not built yet:** needs the Vercel token and Resend key. |

Confirmations to callers: Cal.com emails the booking confirmation itself, so
no SMS or A2P registration is needed.

Native limit: the Cal.com lookup works by **email only**, so changing or
cancelling a visit means asking the caller for the email they booked with.
A custom "find by phone number" function would remove that step. It's not
needed for launch.
