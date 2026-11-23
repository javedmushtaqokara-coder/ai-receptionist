---
name: receptionist-booking
description: Receptionist library skill for booking new appointments during a call. Adds the prompt block, availability and booking tools, custom fallback and tests. Used by build-receptionist when the business takes appointments.
---

# Booking

## What it does

The receptionist checks real availability, offers two or three slots,
collects the details the business needs, books the slot, and confirms it out
loud.

## Pick the tool (native first)

| Client's booking system | Use |
|---|---|
| Google Calendar | `check_google_calendar_availability` and `book_google_calendar_event` (owner signs in) |
| Cal.com | `check_calcom_availability` and `book_calcom_appointment` (API key) |
| Calendly | `check_calendly_availability` and `book_calendly_appointment` (API key) |
| GoHighLevel | `check_ghl_availability` and `book_ghl_appointment` (API key plus Location ID) |
| Anything else (ServiceTitan, Housecall Pro, Jobber, Acuity, Square, Mindbody, and so on) | Custom functions `check_availability` and `book_appointment` on Vercel, calling that system's API |
| No system at all | Default: set up a free Cal.com account for them (the owner signs up; walk them through it). Otherwise use lead capture as a "booking request" and let staff confirm. |

On Retell, native tools go in `general_tools` as
`{type: "integration_app", app_id, provider, app_tool_template_name, ...}`.
Get the inputs from `POST /get-app-tool-schema/{app_id}`. Set fixed values
(calendar or event type IDs, duration) as constants, and let the AI infer the
caller's details. Map useful response fields (booking ID, start time) to
dynamic variables. Turn on `speak_during_execution` with a short line such as
"One moment while I check the calendar."

## Details to collect

Take these from the industry file (`/docs/business-types/<type>.md`): always
full name and callback number (confirm `{{user_number}}` rather than asking
for it), plus what the trade needs. Examples: service address and problem
for home services, new or existing patient for clinics, vehicle for auto
shops.

## Prompt block

```
## Booking appointments
- When the caller wants an appointment, ask what it's for, then check availability before offering times. Never invent times.
- Offer at most three options, nearest first. Say times in the caller's local time, for example "Tuesday at 2 pm".
- Collect: [details for this business]. Confirm the phone number by reading back {{user_number}}.
- Book only after the caller says yes to a specific slot. Then read back the day, time and service.
- If booking fails or no slot suits them, offer to take their details for a callback (lead capture).
- Today is {{current_calendar}}; the time now is {{current_time}}.
```

## Post-call fields

`appointment_booked` (boolean), `appointment_time` (text),
`appointment_type` (text).

## Test cases

1. Caller books the first slot offered. Pass: availability checked before any time was mentioned, booking tool called, details read back.
2. Caller rejects all slots. Pass: no booking; the callback offer is made.
3. Caller asks for "next Tuesday morning". Pass: the right date is resolved and only morning slots are offered.
4. Booking tool returns an error. Pass: the agent apologises and captures details instead.
