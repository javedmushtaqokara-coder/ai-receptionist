---
name: validate-receptionist
description: Validate a client's receptionist after every build. Confirms the agent, functions, integrations and phone number are live, runs the simulation tests, builds and opens a voice-orb test page (a Retell web call in the browser), writes the final report, and gives the owner three test-call scenarios for the business type. Run at the end of every build-receptionist run, and after any change to a live receptionist.
---

# Validate a receptionist

Input: `/clients/<client>/build/ids.json` and `build/plan.md` from the build.
Use the platform API with the key in `.env`, following
`/docs/<platform>/CAPABILITIES.md`. Record every check as ✅ pass, ❌ fail
(with the reason), or ⚠️ needs the owner. **Never report a check as passed
without the API response that shows it.**

## 1. Checks

Run them all, even after a failure, and save the evidence (responses with
secrets removed) to `/clients/<client>/build/validation/`.

**Agent**
- `GET /get-agent/{agent_id}`: exists, and has the right voice, language,
  timezone, `webhook_url` and `post_call_analysis_data`.
- `GET /list-agent-versions/{agent_id}`: a published version exists, and
  it's the one the phone number and the `prod` tag use.
- `GET /get-retell-llm/{llm_id}`: the model matches `build/model-choice.md`,
  and the prompt has no `[[OWNER: ...]]` placeholders left.

**Functions registered**
- Every tool in `plan.md` appears in the LLM's `general_tools` with the
  right type and name. List any extra or missing tools.
- Each custom function on Vercel: an unsigned request returns 401, which
  proves it's deployed and checking signatures. A signed sample request
  returns the expected JSON in under 5 seconds.
- The `notify-owner` webhook: a signed sample `call_analyzed` payload sends
  one test message. Ask the owner to confirm it arrived.

**Integrations authenticate**
- `GET /list-apps`, then `POST /test-app-auth/{app_id}` for every app the
  agent uses: each must return `success: true`.
- A read-only call through each integration where one exists (for example
  check availability for tomorrow). Never create, change or cancel real
  records while validating.

**Phone number**
- `GET /get-phone-number/{number}`: the inbound agents include this agent,
  and `fallback_number` is set.

## 2. Simulation test

- Run the full batch again: every test case from the library skills, plus
  the three owner scenarios from step 5, saved as test cases
  (`POST /create-batch-test`, then poll `GET /get-batch-test/{id}` and read
  `GET /v2/list-test-runs/{id}`).
- Record the pass rate and, for each failure, the criterion, a transcript
  excerpt, and a likely fix. Fix what's in Claude's control (prompt, tool
  descriptions) and re-run once. Report the rest.

## 3. Voice test page (voice orb)

The template is in `test-page/` next to this file:
- `index.html`: the orb page, using Retell's browser SDK (`RetellClient`,
  version pinned, loaded from jsDelivr).
- `proxy.mjs`: keeps the Retell API key on the server. The page sends a
  one-time access code instead, and only web-call endpoints for this one
  agent are allowed.
- `server.mjs`: the local server, no `npm install` needed.
- `api/retell.mjs` and `vercel.json`: the same server as a Vercel function.

Steps:
1. Write `/clients/<client>/build/test-page.json` with `agent_id`,
   `business_name`, `agent_name`, and `scenarios` (the three from step 5,
   each with `title`, `say` and `expect`).
2. Open it:
   - **Session running on the owner's computer** (local or Remote Control):
     start `node .claude/skills/validate-receptionist/test-page/server.mjs clients/<client>`
     in the background. It picks a free access code, prints the link and
     opens the browser.
   - **Cloud session** (the owner can't reach this container's localhost):
     deploy `index.html`, `proxy.mjs`, `api/` and `vercel.json` (not
     `server.mjs`) to Vercel as `<client>-voice-test`. Set project
     environment variables `RETELL_API_KEY`, `ACCESS_CODE` (random, 32 hex
     characters) and `TEST_PAGE_CONFIG`. Give the owner
     `https://<deployment>/#code=<ACCESS_CODE>`. The access code is the only
     protection, so share the link with no one else, and delete the project
     once the receptionist is approved.
   - Inside the cloud container, Node needs `NODE_USE_ENV_PROXY=1` and
     `NODE_EXTRA_CA_CERTS=/root/.ccr/ca-bundle.crt` to reach Retell, and the
     jsDelivr CDN may be blocked. That only affects Claude's own checks.
3. Check the page yourself with Playwright, using a fake microphone and
   `--use-fake-ui-for-media-stream`: the title loads, tapping the orb
   reaches "Live", and the transcript shows after "End call". A web call
   costs per-minute call fees, so keep it under 20 seconds.
4. If the call is refused (for example "Credit balance exhausted"), the
   page shows the reason. Report it as ⚠️ with plain-English steps.

## 4. Report

Write `/clients/<client>/VALIDATION.md` (the checklist with evidence links),
then update `/clients/<client>/REPORT.md`:

- **Built:** agent name and ID, phone number, model, every tool (native or
  custom), integrations, functions with their URLs, and the test page link.
- **Assumed:** every default chosen without asking the owner.
- **Couldn't do:** each ❌ or ⚠️ item with plain-English, TL;DR-size steps
  for the owner (numbered, one action per line).
- **Simulation results:** the pass rate and what was fixed.

## 5. Three test-call scenarios

From `/docs/business-types/<type>.md` and this client's setup, write three
scenarios the owner can act out on a real call or on the test page:

1. **Bread and butter:** the most common call for this business, ending in
   a booking or answer.
2. **Pressure test:** an emergency or upset caller, which should end in a
   transfer or an urgent message.
3. **Curveball:** something the receptionist must not do, such as a
   question it can't answer, a request for a firm quote or diagnosis, or an
   after-hours call.

Format each one, at most five lines:
```
### 1. <title>
Call as: <who you are, e.g. "a homeowner whose AC stopped this morning">
Say: "<first sentence to say>"
Expect: <what a good receptionist does>
Check after: <where to see the result, e.g. the booking in Google Calendar or the lead email>
```

Put them in `REPORT.md`, in `test-page.json`, and in the final message to
the owner.

## 6. Final message to the owner

Keep it short: the phone number and test link first, then the three
scenarios, then "Couldn't do" with the owner's steps. Commit and push
(never `.env`).
