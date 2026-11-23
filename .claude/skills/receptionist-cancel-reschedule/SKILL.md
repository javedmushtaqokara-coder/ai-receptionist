---
name: receptionist-cancel-reschedule
description: Receptionist library skill for cancelling and rescheduling existing appointments during a call. Adds the prompt block, lookup, reschedule and cancel tools, custom fallback and tests. Used by build-receptionist when callers can change bookings.
---

# Cancel and reschedule

## What it does

The receptionist finds the caller's existing booking, confirms it's the right
one, then moves it to a new slot or cancels it, following the business's
cancellation policy.

## Pick the tool (native first)

| Booking system | Find | Move | Cancel |
|---|---|---|---|
| Google Calendar | `list_google_calendar_events` | `reschedule_google_calendar_event` | `cancel_google_calendar_event` |
| Cal.com | `list_calcom_bookings` | `reschedule_calcom_booking` | `cancel_calcom_booking` |
| Calendly | `list_calendly_bookings` | none: cancel, then book a new slot | `cancel_calendly_booking` |
| GoHighLevel | `list_ghl_contact_appointments` | `reschedule_ghl_appointment` | `cancel_ghl_appointment` |
| Anything else | Custom functions `find_booking`, `reschedule_booking` and `cancel_booking` on Vercel |
| No system | Lead capture: take the request and let staff handle it |

Look up by the caller's number (`{{user_number}}`) first. If that finds
nothing, ask for the name and the date of the booking.

## Prompt block

```
## Changing or cancelling an appointment
- Look up the caller's booking by their phone number before asking questions. If several are found, read them back and ask which one.
- Always confirm the booking (day, time, service) before changing it.
- To reschedule: check availability, offer up to three new times, then move the booking. Read back the new time.
- To cancel: state the cancellation policy first: [policy]. Cancel only after a clear yes. Offer to rebook.
- Never cancel or move a booking that doesn't match the caller's phone number or name. Offer a callback instead.
```

## Post-call fields

`booking_changed` (enum: none, rescheduled, cancelled), `new_appointment_time` (text).

## Test cases

1. Caller reschedules to a later slot. Pass: lookup first, original confirmed, new time read back.
2. Caller cancels inside the late-cancellation window. Pass: policy stated before cancelling.
3. No booking found for the number. Pass: asks for name and date; offers a callback if still not found.
4. Caller with two bookings. Pass: reads both and asks which one.
