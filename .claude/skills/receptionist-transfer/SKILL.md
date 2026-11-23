---
name: receptionist-transfer
description: Receptionist library skill for transferring callers to a human (owner, staff, departments, emergency on-call) with the right rules and a safe fallback. Used in every build.
---

# Transfer

## What it does

The receptionist hands the call to a real person when the industry file and
owner say it should: emergencies, angry callers, existing jobs, billing
disputes, or a caller who insists on a human. If nobody answers, it takes a
message.

## Tool (native)

Retell `transfer_call` in `general_tools`. Phone calls only; it doesn't work
on web calls.

```json
{
  "type": "transfer_call",
  "name": "transfer_to_staff",
  "description": "Transfer the caller to a team member. Use only for the reasons listed under Transfers.",
  "transfer_destination": { "type": "predefined", "number": "+1XXXXXXXXXX" },
  "transfer_option": {
    "type": "warm_transfer",
    "transfer_ring_duration_ms": 25000,
    "private_handoff_option": { "type": "prompt", "prompt": "Briefly tell the staff member who is calling and why." },
    "on_hold_music": "ringtone"
  },
  "speak_during_execution": true,
  "execution_message_description": "Tell the caller you're connecting them now."
}
```

- **Default:** warm transfer, so staff hear who is calling and why before
  they're connected.
- Use **cold transfer** if the owner says just put them through.
- **Several destinations** (sales, service, emergency on-call): one
  `transfer_call` tool per destination, each with its own name and reason.
- **Routing that depends on a roster or schedule:** a custom Vercel function
  `get_on_call_number` returns the number, stored as a dynamic variable,
  and the transfer uses `{"type": "inferred", "prompt": "Transfer to {{on_call_number}}"}`.
- Set the phone number's `fallback_number` to the business line as well. It's
  used if the AI is overloaded or in Backup mode.

## Prompt block

```
## Transfers
- Transfer only when: [reasons from the owner and the industry file, e.g. a gas smell or no heat in freezing weather, an angry caller, a question about an existing job, or the caller asks for a person twice].
- Before transferring, say who you're connecting them to. Don't put a caller on hold without telling them.
- Outside [transfer hours], don't transfer. Follow the after-hours rules.
- If the transfer fails or nobody answers, apologise, take a message, and mark it urgent if it is.
```

## Post-call fields

`transferred` (boolean), `transfer_reason` (text).

## Test cases

Simulation tests can't place a real transfer. Mock the tool and check the decision.

1. Caller says it's an emergency (trade-specific). Pass: transfers to the emergency or on-call destination immediately.
2. Caller asks for a person once with a simple question. Pass: tries to help first; transfers if they ask again.
3. Transfer fails. Pass: apology, message taken, marked urgent.
4. Real phone test (one, at the end): the transfer rings the staff number and the handoff summary is heard.
