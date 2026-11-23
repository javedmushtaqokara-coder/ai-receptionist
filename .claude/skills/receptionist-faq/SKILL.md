---
name: receptionist-faq
description: Receptionist library skill for answering common questions (hours, services, prices, location, service area, payment, policies) accurately, with no hallucination. Used in every build.
---

# FAQ

## What it does

The receptionist answers the questions in the industry file's "What callers
ask" section from the business's own facts, and says "I'll have someone
confirm that" for anything it doesn't know.

## Where the facts live (native, never custom)

- **Small business (default):** put the facts directly in the prompt under
  `## Business facts`. This is the fastest and most reliable option, and works
  well up to about 1,500 words.
- **Lots of content** (big price list, many locations, long policies):
  create a knowledge base (`POST /create-knowledge-base` with
  `knowledge_base_texts` and/or `knowledge_base_urls` of the client's site,
  `enable_auto_refresh: true`) and attach it with `knowledge_base_ids`.
- If the client keeps the facts in Google Drive or Notion and wants edits to
  sync, use that native knowledge-base integration.
- Sources for the facts: the owner's answers, then the client's website,
  then the industry file. Record each in `brief.md`.

## Prompt block

```
## Business facts
Name: [business]   Address: [address]   Service area: [area]
Hours: [hours, by day]   Timezone: [tz]
Services and prices: [list, with "from" prices or "varies, we'll quote"]
Payment: [methods]   Policies: [cancellation, warranty, deposits]

## Answering questions
- Answer only from the business facts above. If something isn't covered, say you'll have the team confirm, and offer to take a message.
- Give prices exactly as listed. Never estimate a job cost, diagnose a problem, or promise a time that isn't booked.
- Keep answers to one or two sentences, then ask if there's anything else, or steer toward booking.
- For "are you open now?", compare {{current_time}} with the hours.
```

## Post-call fields

`questions_asked` (text), `unanswered_question` (text, empty if none).
Review unanswered questions after launch and add the answers to the facts.

## Test cases

1. Caller asks the hours on a specific day. Pass: correct hours.
2. Caller asks for a price that isn't listed. Pass: no number invented; offers a quote or message.
3. Caller asks "Do you service [town outside the area]?". Pass: correct no, and an alternative if there is one.
4. Caller asks for a diagnosis ("Why is my AC blowing warm?"). Pass: no diagnosis; offers a technician visit.
