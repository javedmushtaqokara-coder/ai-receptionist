---
name: build-receptionist
description: Build, configure, publish and deploy a client's AI receptionist on the voice platform, then attach a phone number. Run after research-business-type has produced the drafts and the owner has answered the questions. Prefers native integrations, writes custom functions only when nothing native exists (deployed to Vercel), picks the newest fast model, and saves everything to the client's folder.
---

# Build a receptionist

## 0. Ground rules

- **Read first:** `/docs/<platform>/CAPABILITIES.md`, the cached industry file
  `/docs/business-types/<type>.md`, and everything in `/clients/<client>/`
  (`brief.md` and `draft/`). Build from those, not from memory.
- **Native first:** use a built-in tool or native integration whenever one
  covers the need (see section 10 of the capability map). Write a custom
  function **only** when nothing native exists.
- **Library:** assemble the receptionist from the skills in
  `.claude/skills/receptionist-*`. Each has the prompt block, tool config,
  custom fallback and test cases for one job:
  - `receptionist-faq` (every build)
  - `receptionist-transfer` (every build)
  - `receptionist-after-hours` (every build)
  - `receptionist-lead-capture` (every build)
  - `receptionist-booking` (when the business takes appointments)
  - `receptionist-cancel-reschedule` (when bookings can be changed)
- **No technical questions** to the owner. Decide, and record it as an assumption.
- **When the owner has to do something** (sign in, pay, forward their phone,
  register SMS), walk them through it in plain English, TL;DR size:
  numbered steps, one action per line, no jargon, at most about six lines.
  Then carry on with everything that doesn't depend on it.
- **Secrets** only go in `.env`, never in the client folder or the repository.

## 1. Plan

Write `/clients/<client>/build/plan.md`: which library skills apply, every
tool with its source (native tool, native integration, or custom function),
and what the owner must do. Then follow the order below.

## 2. Pick the model (newest fast model, never an older default)

1. List the platform's current models. For Retell: the `LLMModel` enum in
   `docs/retell/raw/openapi.yaml`. If the change check in `SOURCE.md` shows
   the docs changed, re-download first. Also read the docs' latency guidance.
2. Shortlist the **newest generation** of each provider's small and fast
   models. Drop anything deprecated or scheduled for replacement (section 12
   of the capability map).
3. Measure. If the platform publishes per-model latency, use it. Retell
   doesn't, so time it: create the LLM with the real prompt, then call
   `POST /agent-playground-completion/{agent_id}` 3 times per candidate with
   a typical caller turn, switching the model between runs. Record the median
   in seconds.
4. Choose the fastest candidate that also gets the tool calls right in the
   test suite (step 7). Enable the speed tier (`tier: "fast"`, or
   `ultrafast` where the model supports it) and add a fast fallback
   (`model_config.backup`, about 1500 ms) on a second fast model.
5. Record the candidates, timings and choice in `build/model-choice.md`.

## 3. Connect integrations

For each native integration in the plan:
- **Connects by API key** (for example Cal.com, Calendly, GoHighLevel,
  HubSpot, Notion): ask the owner for the key once, in plain English with
  where to find it. Save it to `.env` as `<PROVIDER>_API_KEY`, create the app
  (`POST /create-app`), and confirm with `POST /test-app-auth/{app_id}`.
- **Needs the owner to sign in** (Google Calendar, Zoho, Zendesk, and other
  OAuth providers): give the owner the steps, wait for the connection to
  appear in `GET /list-apps`, and build the rest meanwhile.
- Get each tool's input schema with `POST /get-app-tool-schema/{app_id}`
  before adding it to the agent.

## 4. Custom functions (only when nothing is native)

- Deploy each one to **Vercel** as a serverless function, one Vercel
  project per client named `<client>-receptionist`. Keep the source in
  `/clients/<client>/functions/`: `api/<function>.js`, `package.json` and
  `vercel.json`.
- **Vercel token:** if `VERCEL_TOKEN` isn't in `.env`, ask the owner once, with
  the steps: vercel.com, then Settings, then Tokens, then Create, then paste
  it here. Save it to `.env` as `VERCEL_TOKEN` and reuse it for every client
  after that.
- Deploy through the Vercel REST API (`POST https://api.vercel.com/v13/deployments`
  with the files inline, `target: "production"`), with secrets set as project
  environment variables (`POST /v10/projects/{id}/env`). If the network
  blocks `api.vercel.com`, allow it in the cloud environment (the owner
  approves on a card).
- Every function must verify `X-Retell-Signature`, return in under 5 seconds,
  return a short JSON result the agent can read aloud, and fail softly with
  a message the agent can use.
- Test each function with `curl` before attaching it to the agent.

## 5. Create the agent

1. Knowledge base, if the facts don't fit in the prompt:
   `POST /create-knowledge-base`.
2. Response engine: `POST /create-retell-llm` with the final prompt (the
   draft with the owner's answers filled in, plus the library prompt
   blocks), `begin_message`, `start_speaker: "agent"`, `model_config` from
   step 2, `general_tools` from the library skills, and
   `default_dynamic_variables`.
3. Agent: `POST /create-agent` with `agent_name` set to "<Client> Receptionist",
   a platform voice that fits the brand (`GET /list-voices`), `language`,
   `timezone`, `post_call_analysis_data` (from lead capture),
   `webhook_url` (if a notification function exists), `boosted_keywords`
   (the business name, staff names and service terms), `enable_dnc_detection`,
   `end_call_after_silence_ms`, and `max_call_duration_ms`.
4. Save every request and response (with secrets removed) to
   `/clients/<client>/build/api/`, and the IDs to `build/ids.json`.

## 6. Test before publishing

1. Create one simulation test case per library test scenario
   (`POST /create-test-case-definition`), then run them as a batch
   (`POST /create-batch-test`) and read the results.
2. Fix the prompt or tools and re-run until everything passes. Save the
   results to `build/test-results.md`.

## 7. Publish and attach a number

1. `POST /publish-agent-version/{agent_id}`.
2. Phone number:
   - Default: buy a local number in the client's area code
     (`POST /create-phone-number` with `area_code`, `inbound_agents`, and
     `fallback_number` set to the business's real line).
   - If it fails because there's no payment method or KYC, walk the owner
     through adding one, then retry.
   - To keep the client's existing number, tell the owner how to forward
     calls from it to the new number (plain English, for their carrier).
3. Offer the owner one real test call to the number.

## 8. Save and report

- The client folder must end up with: `brief.md`, `draft/`, `build/`
  (`plan.md`, `model-choice.md`, `ids.json`, `api/`, `test-results.md`),
  `functions/` (if any), and `REPORT.md`.
- `REPORT.md` has three sections: **Built** (agent, number, tools,
  functions, with IDs and links), **Assumed**, and **Couldn't do** (each with
  plain-English steps for the owner).
- Commit and push. Never commit `.env`.
