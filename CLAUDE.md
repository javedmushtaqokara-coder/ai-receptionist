# AI Receptionist Business — Build Master Rules

This folder is an AI receptionist business. The owner describes a client;
Claude is the build master and researches, builds, and deploys that client's
AI receptionist from start to finish.

## Workflow for every new client

1. **Research first.** Before building anything, research:
   - The platform(s) the receptionist will run on (phone/voice, web chat,
     WhatsApp, booking or CRM integrations, and so on).
   - The client's business type: common caller questions, booking flows,
     industry vocabulary, compliance concerns, and after-hours expectations.
   Check `/docs` first. Only research what is missing or out of date.
   - Platform: the `research-voice-platform` skill (see "Platform research").
   - Business type: the `research-business-type` skill, run at the start of
     **every** client build. It covers what calls to that kind of business
     sound like, what callers ask for, what they book and what gets
     transferred. It drafts the call flow, prompt and functions in
     `/clients/<client>/draft/`, caches the industry knowledge in
     `/docs/business-types/<type>.md`, and ends with the owner questions.

2. **Ask the owner only what they know.** Ask only after the drafts exist,
   so the questions cover just the gaps that research couldn't fill.
   - Ask at most **six questions** per client.
   - Ask only about business facts the owner knows: hours, services,
     prices, tone, how to handle bookings, who gets escalations, and so on.
   - **Never ask technical questions.** Platform choice, architecture,
     models, prompts, integrations, hosting, and configuration are Claude's
     decisions. Pick sensible defaults and record them as assumptions.

3. **Build and deploy** with the `build-receptionist` skill. It reads `/docs`
   and the industry research first, and assembles the receptionist from the
   library skills below. It uses native integrations whenever they exist,
   writes custom functions only when nothing native does (deployed to
   Vercel), and picks the platform's newest fast model after checking the
   model list and timing them, never an older default. It then creates,
   configures, tests and publishes the agent, attaches a phone number, and
   saves everything to the client's folder.

4. **Validate and report** with the `validate-receptionist` skill, after
   **every** build and every change to a live receptionist. It confirms the
   agent exists, functions are registered, integrations authenticate and the
   number is attached; runs the simulation tests; builds and opens the
   voice-orb test page (a Retell web call in the browser); writes the report
   (built, assumed, couldn't do); and gives the owner three test-call
   scenarios for the business type. A build isn't finished until it has run.

## Skills

| Skill | When |
|---|---|
| `research-voice-platform` | A new platform is connected, or its docs changed |
| `research-business-type` | Start of every client build |
| `build-receptionist` | After the owner answers the questions |
| `validate-receptionist` | After every build or change: checks, simulation, voice test page, report, three test calls |
| `receptionist-faq` | Every build: answer questions from the business facts |
| `receptionist-transfer` | Every build: hand calls to a human |
| `receptionist-after-hours` | Every build: closed hours, holidays, emergencies |
| `receptionist-lead-capture` | Every build: take messages, notify the owner |
| `receptionist-booking` | The business takes appointments |
| `receptionist-cancel-reschedule` | Callers can change their bookings |

All skills are in `.claude/skills/`. Add new receptionist abilities to the
library as `receptionist-<ability>` instead of writing them into one client.

## When the owner has to do something

If anything requested can't be finished without the owner doing a step
(signing in, paying, giving a key, forwarding a phone, registering SMS),
walk them through it in **plain English, TL;DR size**: numbered steps, one
action per line, no jargon, about six lines at most. Carry on with
everything else in the meantime.

## Keys Claude may ask for (once each)

Ask once, in plain English with where to find it, save it to `.env`, and
reuse it for every client:
- `VERCEL_TOKEN`: for deploying custom functions
- `RESEND_API_KEY`: for emailing the owner messages and leads
- A client's integration key (Cal.com, Calendly, GoHighLevel, HubSpot, and
  so on): per client, when its booking or CRM system needs one

## Folder structure

```
/CLAUDE.md          this file
/clients/<client>/  one folder per client; everything for that client lives here
/docs/<platform>/   cached platform knowledge, shared across clients
/docs/business-types/<type>.md  cached industry knowledge, shared across clients
```

- **One folder per client in `/clients`**, named in kebab-case after the
  business (for example `/clients/smile-dental-clinic`). Nothing
  client-specific goes outside that folder.
- Each client folder should contain at least:
  - `brief.md`: the business details and the owner's answers
  - `receptionist/`: prompts, configuration, scripts, and the knowledge base
  - `REPORT.md`: the final report for that build

## Platform knowledge cache (`/docs`)

- Save useful platform research to `/docs`, one file per platform or topic
  (for example `/docs/vapi.md`, `/docs/twilio.md`, `/docs/dental-practices.md`).
- Include setup steps, API notes, limits, pricing, gotchas, and the date
  the information was checked.
- Reuse these files on later builds and update them when they are stale or wrong.

## Platforms and API keys

Whenever the owner gives a platform and an API key:

1. **Save the key to `.env`** in this folder (for example `RETELL_API_KEY=...`).
   `.env` is listed in `.gitignore`. Never commit it, and never write the key
   into any other file, including docs, reports or client folders.
2. **Use the platform's REST API** directly, with `curl` or short scripts that
   load the key from `.env`.
3. **Test the key with one API call** right away. Use a harmless read-only
   endpoint, report whether it worked, and record the platform and its working
   test endpoint in `/docs/<platform>.md`.

4. **Research the platform** with the `research-voice-platform` skill
   (`.claude/skills/research-voice-platform/`).

## Platform research

- Run the `research-voice-platform` skill **whenever a new platform is
  connected**. It reads the platform's full docs, maps what it does natively
  and how to set each thing up through the API (integrations, tools, phone
  numbers, testing), flags where a custom function is needed, and saves it all
  to `/docs/<platform>/`.
- **Re-run it only if the docs change.** Its first step compares checksums
  against `/docs/<platform>/SOURCE.md` and stops if nothing changed.
- Before every client build, read `/docs/<platform>/CAPABILITIES.md` instead
  of the live docs.

## Platforms in use

- **Voice: Retell** (`RETELL_API_KEY` in `.env`). Capability map:
  `/docs/retell/CAPABILITIES.md`.

## Final report (every build)

End every build with a report, saved to `/clients/<client>/REPORT.md` and
summarised to the owner, with three sections:

- **Built:** what was created and deployed, with links or locations.
- **Assumed:** every decision or default Claude made without asking.
- **Couldn't do:** anything left unfinished or blocked, why, and what is
  needed to finish it (for example missing accounts, credentials, or access).
