---
name: receptionist-after-hours
description: Receptionist library skill for behaving correctly outside business hours, on holidays and at weekends, including the emergency path. Used in every build.
---

# After hours

## What it does

The receptionist knows whether the business is open right now. Outside
hours it still answers questions, books where online booking is allowed, and
takes messages. It only escalates true emergencies, by the business's own
rule.

## How (native first)

- Set `timezone` on the agent to the business's timezone (IANA name, such
  as `America/Chicago`).
- The prompt compares `{{current_time}}` and `{{current_calendar}}` with the
  hours in the business facts. No custom code is needed for ordinary
  opening hours.
- Holidays and closures: list the upcoming dates in the business facts
  (update them on request).
- **Custom only when** the rules are complex: rotating on-call rosters,
  holiday calendars that change often, or different agents for day and night.
  Then use a Vercel endpoint as the phone number's `inbound_webhook_url`,
  returning `dynamic_variables` (for example `is_open`, `on_call_number`) or
  `override_agent_id`. It must answer within 10 seconds.

## Prompt block

```
## After hours
- Our hours are in the business facts. Now it is {{current_time}}. Work out whether we're open before deciding what to do.
- When closed: say we're closed and when we reopen, then still help. Answer questions, book an appointment if booking is available, or take a message.
- Emergencies after hours: [owner's rule, e.g. "transfer to the on-call number for no heat, gas smell or flooding" or "give the emergency line and take an urgent message"]. Anything else waits for business hours.
- Never tell a caller someone will call tonight unless the after-hours rule says so.
- Safety first: for danger to life (gas smell, fire, carbon monoxide alarm, medical emergency), tell them to leave or hang up and call 911 or their emergency number before anything else.
```

## Post-call fields

`called_after_hours` (boolean), `after_hours_emergency` (boolean).

## Test cases

Set the time with test `dynamic_variables` or a mocked current time.

1. Saturday 10 pm, routine question. Pass: says closed, gives reopening time, answers, offers a message or booking.
2. After hours, a trade emergency. Pass: follows the owner's emergency rule (transfer or urgent message).
3. After hours, danger to life. Pass: the safety instruction comes first.
4. Weekday during hours. Pass: no "we're closed" message.
