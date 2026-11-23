---
name: research-business-type
description: Research a client's type of business before building their AI receptionist. Works out what calls to that kind of business sound like, what callers ask for, what they book and what gets transferred. Drafts the call flow, prompt and functions, then asks the owner at most six questions they can answer. Run at the start of every client build, after the voice platform has been researched.
---

# Research a business type

Goal: arrive at the owner with a nearly finished receptionist, so the only
questions left are facts about their business that no research can find.

Inputs: the owner's description of the client, plus the platform map in
`/docs/<platform>/CAPABILITIES.md`. Read that map first; never re-research
the platform here.

## Output layout

```
/docs/business-types/<type>.md     reusable knowledge about this kind of business
/clients/<client>/brief.md         what the owner said, and later their answers
/clients/<client>/draft/
  call-flow.md                     the call flow
  prompt.md                        the draft receptionist prompt
  functions.md                     the tools and functions needed
  questions.md                     the questions for the owner (six at most)
```

Use kebab-case for `<type>` and `<client>`, for example `hvac`,
`dental-clinic`, `smile-dental-clinic`.

## Steps

### 1. Write the brief

Save everything the owner said about the client to
`/clients/<client>/brief.md`: the name, the business type, location, website,
and anything else given. If the client has a website, read it: hours,
services, prices, service area and booking links often answer questions
before they're asked. Record what came from the site.

### 2. Research the business type (reuse the cache)

If `/docs/business-types/<type>.md` exists, read it and skip to step 3. Add
anything new you learn on this build.

Otherwise research the industry (web search, industry guides, competitors'
sites, review sites, answering-service scripts for that trade) and write
`/docs/business-types/<type>.md` with these sections:

1. **What calls sound like:** who calls (new customers, existing ones,
   suppliers, spam), typical mood (calm, stressed, emergency), the terms
   callers use, and a short sample of 3–5 realistic call openings.
2. **Call mix:** the most common reasons for calling, ranked, with a rough
   share of each.
3. **What callers ask:** the common questions and what a good answer needs
   (prices, hours, area covered, insurance accepted, timings).
4. **What gets booked:** appointment types, how long each takes, the details
   needed to book (name, phone, address, problem, equipment, insurance), and
   the booking or field-service software this trade commonly uses.
5. **What gets transferred or escalated:** emergencies, angry customers,
   billing disputes, existing jobs, sales leads above a certain size, and
   anything legally sensitive.
6. **Emergencies and after hours:** what counts as urgent in this trade and
   how such calls are normally handled.
7. **Rules and risks:** licensing, safety, privacy (for example HIPAA for
   medical), and things the receptionist must never say or promise (diagnoses,
   firm quotes, legal advice).
8. **Sources** with the date checked.

### 3. Draft the call flow

Write `/clients/<client>/draft/call-flow.md`: the greeting; how intent is
identified; one branch for each common call reason (answer, book, take a
message, transfer); the emergency path; the after-hours path; and the close.
Mark each step with the platform feature it uses.

### 4. Draft the prompt

Write `/clients/<client>/draft/prompt.md` following the platform's prompting
guidance in `/docs/<platform>/CAPABILITIES.md`. Default to a single-prompt
agent. Include identity and tone, the business facts, what to do for each
call type, booking rules, transfer and emergency rules, what never to say,
and how to close. Write `[[OWNER: ...]]` placeholders for facts still
unknown, and fill in sensible defaults for everything else.

### 5. Draft the functions

Write `/clients/<client>/draft/functions.md`, a table with one row per
function or tool: its name, what it does, the native platform feature or
integration that covers it, its inputs and outputs, and **whether a custom
function is needed** (with the reason, from section 10 of the platform map).
Also list the post-call analysis fields to capture and how the owner gets
notified about messages.

### 6. Ask the owner (six questions max)

Gather every remaining `[[OWNER: ...]]` placeholder and turn them into **six
questions at most** in `/clients/<client>/draft/questions.md`, then ask
them.

- **Only ask what the owner knows:** their hours, services and prices, who
  takes transfers and on what number, what counts as an emergency for them,
  how they want bookings handled, which booking or CRM software they use,
  and the tone they want.
- **Never ask technical questions.** Models, voices, prompts, tools, APIs,
  hosting and platform settings are Claude's decisions.
- Don't ask what the research, the website or a sensible default already
  answers. List those defaults as assumptions instead.
- Combine related facts into one question, and give an example answer so
  the owner can reply quickly.
- Order the questions by how much they change the build.

Show the owner a short summary of the planned receptionist with the
questions, so they can correct anything that's wrong.

### 7. After the answers

Save the answers to `brief.md`, fill in the drafts, and continue with the
build. Anything still unknown becomes an assumption in the final report.
