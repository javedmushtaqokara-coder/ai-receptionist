---
name: receptionist-lead-capture
description: Receptionist library skill for taking messages and capturing new leads, then getting them to the owner fast. Adds the prompt block, post-call fields, CRM logging and the owner notification function. Used in every build.
---

# Lead capture

## What it does

When a caller can't be booked or transferred, or is a new enquiry, the
receptionist collects their details and reason for calling. The owner gets
the message within a minute of the call ending.

## Capture (native)

- `post_call_analysis_data` on the agent, extracted after every call:
  `caller_name` (text), `callback_number` (text), `reason` (text),
  `urgency` (enum: emergency, today, this_week, no_rush),
  `is_new_customer` (boolean), `best_time_to_call` (text), `summary` (text).
  Add trade-specific fields from the industry file, such as service address
  or job type.
- To grab a value mid-call (for example to use it in a later tool), use the
  `extract_dynamic_variable` tool.

## Save to a CRM (native, when the client has one)

HubSpot, Salesforce, GoHighLevel, Zoho, Dynamics or Monday: create or update
the contact during the call or after it (`create_*_contact`,
`create_*_note`, or `log_*_call`), and/or use the CRM write-back mappings
(`POST /update-crm-config`).

## Notify the owner (custom, always)

Retell has no email tool, and sending custom-text SMS needs A2P registration.
So every build has one Vercel function:

- **`notify-owner`:** receives the `call_analyzed` webhook (set the agent's
  `webhook_url` and `webhook_events: ["call_analyzed"]`), verifies
  `X-Retell-Signature`, and sends the owner one short message with the name,
  number, reason, urgency, summary, and a link to the recording.
- Delivery (Claude decides; don't ask the owner how):
  - **Email (default):** through Resend. Ask the owner once for a Resend API
    key, with the steps: resend.com, sign up, API Keys, Create, paste it here.
    Save it to `.env` as `RESEND_API_KEY` and reuse it for every client. Use
    Resend's test sender until the owner verifies their domain.
  - **SMS:** only if the client has an A2P-registered Retell or Twilio number.
- Skip calls with nothing useful (wrong numbers, spam, hang-ups under 10
  seconds). Mark `urgency = emergency` in the subject line.

## Prompt block

```
## Taking a message
- If you can't book or transfer the caller, offer to take a message. Collect name, best callback number (confirm {{user_number}}), and the reason, in one or two questions.
- Ask how urgent it is only if it's unclear.
- Read the details back, and tell them when to expect a call back: [callback promise].
- Never promise a specific person will call or a specific time unless the business facts say so.
```

## Test cases

1. New customer wants a quote. Pass: name, number and reason captured and read back; a callback promise given.
2. Caller refuses to give a name. Pass: polite; a message is still taken with the number and reason.
3. Spam or sales call. Pass: brief, polite end; no message flagged as a lead.
4. Webhook function test: a signed sample payload sends one email; a bad signature returns 401.
