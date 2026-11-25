# Retell: capability map

Researched 2026-11-23 from the full docs (`raw/llms-full.txt`, about 360 pages),
the OpenAPI spec (`raw/openapi.yaml`), and read-only calls against the live account.
Sources and checksums are in `SOURCE.md`.

## 1. Account snapshot (2026-11-23)

| Item | Value |
|---|---|
| Workspace | "Alpha Hvac Ai agents" (`org_eQKaV66Y6jddE1Jt`) |
| API key name | "Cluade Receptionist" |
| Agents | 1, "Single-Prompt Agent" (`agent_323c10a73a68ce2166900c6966`): an untouched default, voice `retell-Cimo`, model `gpt-5.6-terra` |
| Phone numbers | none |
| Knowledge bases | none |
| Integrations (apps) | none connected |
| Concurrency | 20 calls (burst up to 60) |

## 2. API basics

- Base URL: `https://api.retellai.com`
- Auth: `Authorization: Bearer $RETELL_API_KEY`
- **Key test:** `GET /get-api-key-info` returns the workspace and key name. `GET /list-voices` also works.
- **Current list endpoints** (the old ones return 400 "Deprecated API usage"):

| Resource | Use this | Not this (retired) |
|---|---|---|
| Agents | `POST /v2/list-agents` (JSON body, `{}` for all) | `GET /list-agents` |
| Phone numbers | `GET` or `POST /v2/list-phone-numbers` | `GET /list-phone-numbers` |
| Retell LLMs | `GET /v2/list-retell-llms` | `GET /list-retell-llms` |
| Conversation flows | `GET /v2/list-conversation-flows` | old v1 |
| Calls | `POST /v3/list-calls` | |
| Chats | `POST /v3/list-chats` | |
| Agent versions | `GET /list-agent-versions/{id}` | `GET /get-agent-versions` |
| Knowledge bases | `GET /list-knowledge-bases` (still v1, plain array) | |

- Lists return `{items, has_more}`, paged with `pagination_key`.
- Calls: `POST /v2/create-phone-call`, `POST /v3/create-web-call`, `GET /v2/get-call/{id}`.

## 3. Building an agent

An agent has two parts: the **response engine** (the brain) and the **agent** (voice, telephony and behaviour settings).

**Agent types** (`response_engine.type`):
- `retell-llm` (single prompt): **the default for receptionists.** Retell's own guidance is to start here and move to a flow only when one prompt can't cope.
- `conversation-flow`: nodes and transitions. Use it when strict, compliance-style ordering is needed.
- `custom-llm`: our own LLM server over WebSocket. Avoid; it can only be tested with real audio calls.
- Multi-prompt is **deprecated**: creation ends 2026-12-15 and editing ends 2027-02-01. Never use it.

**Build sequence:**
1. `POST /create-retell-llm` with `general_prompt`, `begin_message`, `start_speaker` (`agent` for a receptionist), `general_tools`, `knowledge_base_ids`, `default_dynamic_variables`, and `model`/`model_config`. Returns `llm_id`.
2. `POST /create-agent` with `response_engine: {type: "retell-llm", llm_id}`, `agent_name`, `voice_id`, `language`, `timezone`, `webhook_url`, `post_call_analysis_data`, `boosted_keywords`, `end_call_after_silence_ms`, `max_call_duration_ms`, `voicemail_option`, `enable_dnc_detection`, `pronunciation_dictionary`, and `handbook_config`.
3. Edit with `PATCH /update-retell-llm/{llm_id}` and `PATCH /update-agent/{agent_id}`. These edit the draft.
4. `POST /publish-agent-version/{agent_id}` to publish. The older `publish-agent` was deprecated 2026-07-20.
5. Versions and tags: `POST /create-agent-version/{id}`, `PATCH /update-agent-root/{id}` for the `prod`/`staging` tags. Phone numbers can point at a tag.

Other useful agent settings: `timezone` (needed for after-hours logic), `ambient_sound`, `interruption_sensitivity`, `responsiveness`, `voice_speed`, `fallback_voice_ids` (required when using third-party voices), `data_storage_setting` and `pii_config` (privacy), and `guardrail_config`.

Voices: `GET /list-voices` (Retell platform voices are tuned for phone audio), `POST /search-community-voice`, `POST /add-community-voice`, `POST /clone-voice`.

## 4. Native tools (`general_tools[].type` on the Retell LLM)

| Type | What it does |
|---|---|
| `end_call` | Hang up when the conversation is done |
| `transfer_call` | Send the call to a human by E.164 number or SIP URI. Cold, warm, or agentic warm (an AI briefs the human first). Phone calls only, not web calls. |
| `agent_swap` | Hand the call to another Retell agent (for example a Spanish-language agent) |
| `press_digit` | Navigate phone menus on outbound calls |
| `send_sms` | Text the caller or another number mid-call (see section 6 for the SMS limits) |
| `extract_dynamic_variable` | Capture typed values (name, date, and so on) into variables |
| `code` | Run JavaScript in Retell's sandbox, with `fetch()` but no secrets and no LLM arguments (reads only `dv` and `metadata`), 5–60 s timeout |
| `custom` | Call **our** HTTPS endpoint with LLM-filled arguments. Signed with `X-Retell-Signature` (HMAC-SHA256 of the body). Body is `{name, call, args}`. Timeout 1–600 s (default 120). |
| `integration_app` | Call a connected provider's tool (CRM, calendar, helpdesk); Retell handles that provider's API and auth |
| `mcp` | Call tools on a remote MCP server |
| `bridge_transfer`, `cancel_transfer` | Used inside agentic warm transfers |
| `escalate_chat` | Chat agents only |

Built-in dynamic variables include `{{current_time}}`, `{{current_hour}}`, `{{current_calendar}}`, `{{user_number}}`, `{{agent_number}}`, `{{direction}}`, and `{{call_id}}`. Use these to answer "are you open now?" without any custom code.

## 5. Native integrations

List the catalog live with `GET /list-app-templates`. Connect with `POST /create-app`, check with `POST /test-app-auth/{app_id}`, and get a tool's input schema with `POST /get-app-tool-schema/{app_id}`. Then add the tool to the agent as `{type: "integration_app", app_id, app_tool_template_name, ...}`.

| Provider | Type | Tools | How it connects |
|---|---|---|---|
| Google Calendar | calendar | check availability, book, list, get, reschedule, cancel | **Owner signs in** (OAuth) |
| Cal.com | calendar | check availability, book, list, get, reschedule, cancel | **By API** with a Cal.com API key, or owner OAuth |
| Calendly | calendar | check availability, book, list, get, cancel (no reschedule) | **By API** with a personal access token |
| GoHighLevel | CRM + calendar | contacts, tags, opportunities, tasks, notes, **check availability, book, reschedule, cancel** | **By API** with a Private Integration token plus Location ID (`tenant_id`) |
| HubSpot | CRM | contacts, deals, companies, tasks, notes, log call | **By API** with a private app token |
| Salesforce | CRM | contacts, leads, accounts, opportunities, cases, tasks, notes, SOQL | **By API** with an External Client App client ID and secret, plus instance URL |
| Zoho CRM | CRM | contacts, deals, tasks, notes, log call | **Owner signs in** (OAuth) |
| Dynamics 365 | CRM | contacts, tasks, notes, log call | **Owner signs in** (OAuth) |
| Monday.com | CRM | items, updates | **Owner signs in** (OAuth) |
| Zendesk | support | users, tickets, comments | **Owner signs in** (OAuth) |
| Google Drive, OneDrive | knowledge base | syncs files into a knowledge base every 24 h | **Owner signs in** (OAuth) |
| Notion | knowledge base | syncs pages into a knowledge base | **By API** with an internal integration token |

- Integration tool calls time out after 3–14 s depending on the tool. The prompt must say what to do when a lookup fails.
- The built-in Cal.com "Check Availability"/"Book Calendar" tools were retired in 2026. Use the Cal.com **integration** instead.
- CRM contact sync and post-call write-back: `GET`/`POST /update-crm-config`, `POST /run-sync-job`.

## 6. Phone numbers

- **Buy:** `POST /create-phone-number` with `area_code`, `country_code` (US or CA only), `toll_free`, `number_provider` (`twilio`, `telnyx` or `bandwidth`), `inbound_agents`, `outbound_agents`, `nickname`, `fallback_number`, and `inbound_webhook_url`.
  - **Needs a payment method** on the workspace, and KYC for outbound calling and SMS. These are owner or dashboard tasks.
  - Cost: $2/month for a local number, $5/month for toll-free (plus $0.06/min inbound on toll-free).
  - Some new numbers have a 2-minute hold on outbound calls. Inbound works right away.
- **Import** an existing number over SIP: `POST /import-phone-number` (needs `phone_number` and `termination_uri`). Guides exist for Twilio, Telnyx, Vonage, and others.
- **Keep the client's existing number:** have the client forward calls to the Retell number. This needs no API work, only a carrier setting on the client's side.
- **Bind agents:** `inbound_agents` / `outbound_agents` lists (weighted, which allows A/B tests). The single-agent fields were removed 2026-03-31.
- **Safety net:** set `fallback_number` to the business's real line. It's used when concurrency is full, or for **Backup mode**, which pauses the AI and forwards all calls (a dashboard toggle).
- **Inbound webhook** (`inbound_webhook_url`): our endpoint can pick the agent, inject variables, or `reject: true` a call. It has a 10 s timeout. This is a hosted endpoint, so it counts as custom.
- **SMS:**
  - Sending from **Retell's SMS-approved pool** works without registration, but the message is a **fixed Retell template that can't be customised**.
  - Sending custom texts from the client's own number needs **A2P 10DLC registration** (business profile, brand, campaign) and a Twilio number. Telnyx and Bandwidth numbers can't register for SMS yet.

## 7. Knowledge bases and variables

- `POST /create-knowledge-base` (multipart) with `knowledge_base_name`, `knowledge_base_texts` (title and text), `knowledge_base_files`, `knowledge_base_urls`, and `enable_auto_refresh`. Add sources later with `POST /add-knowledge-base-sources/{id}`. Attach it through `knowledge_base_ids` on the LLM.
- Put the business facts (hours, services, prices, FAQs) in the knowledge base or in the prompt. For a small business the facts usually fit in the prompt itself, which is faster and more reliable than retrieval.
- Dynamic variables: `{{name}}` in prompts and tools, defaults in `default_dynamic_variables`, set per call through `retell_llm_dynamic_variables` or the inbound webhook.

## 8. Testing

| Method | Through the API? | Notes |
|---|---|---|
| Playground completion | ✅ `POST /agent-playground-completion/{agent_id}`: send the conversation, get the agent's next reply | Fastest check of prompt and tool choice |
| Simulation test cases | ✅ `POST /create-test-case-definition` (`user_prompt` = simulated caller, `metrics` = success criteria, `tool_mocks`, `dynamic_variables`) | Graded pass or fail. Text only. |
| Batch tests | ✅ `POST /create-batch-test` (`test_case_definition_ids`, `response_engine`), then `GET /get-batch-test/{id}` and `GET /v2/list-test-runs/{id}` | Regression suite |
| Web call | ⚠️ `POST /v3/create-web-call` returns an access token, but someone has to talk through the browser SDK | Real audio |
| Phone call | ⚠️ `POST /v2/create-phone-call` from our Retell number to the owner's phone | Real carrier audio, transfers, DTMF. Costs per minute. |

Text tests are billed per message, and voice tests per minute at production rates.

**Default test plan for every build:** create 5–8 simulation test cases (happy path, booking, after hours, transfer request, angry caller, out-of-scope question, wrong number) and run them as a batch. Then ask the owner to call the number once.

## 9. Webhooks and post-call analysis

- Agent `webhook_url` and `webhook_events` (`call_started`, `call_ended`, `call_analyzed`). Verify with `X-Retell-Signature`.
- `post_call_analysis_data`: custom fields (text, boolean, enum, number) extracted after every call, such as caller name, reason, urgency, and whether a callback is needed. Results appear in `GET /v2/get-call/{id}` and the `call_analyzed` webhook.
- Alert rules (dashboard) can email or webhook on metric thresholds, but they're not per-call notifications.

## 10. Where a custom function is needed

| Receptionist need | Native way | Custom needed when |
|---|---|---|
| Answer FAQs (hours, services, prices) | Prompt or knowledge base | Never |
| "Are you open now?" | `{{current_time}}` plus agent `timezone` | Never |
| Book, reschedule, cancel appointments | Cal.com, Calendly, Google Calendar or GoHighLevel integration | The client uses **any other system** (ServiceTitan, Housecall Pro, Jobber, Acuity, Square, Mindbody, Jane, Vagaro, and so on), so a `custom` function to that system's API is needed |
| Look up or save the caller in a CRM | HubSpot, Salesforce, GoHighLevel, Zoho, Dynamics or Monday | Any other CRM, or a spreadsheet: use `custom`, or `code` for keyless public APIs |
| Transfer to a person | `transfer_call` | Routing by staff schedule or on-call roster: a `custom` function returns the number, then a dynamic transfer |
| **Take a message and notify the owner** | Post-call analysis captures the message | **Always.** Retell has **no email tool**, and SMS with custom text needs A2P registration. Notifying the owner needs a `custom` endpoint or `call_analyzed` webhook receiver that sends the email or SMS. Owner SMS through A2P is the no-server alternative. |
| Text the caller a confirmation | `send_sms` | Custom wording without A2P registration isn't possible. Either register A2P, or use a custom endpoint with another SMS provider. |
| Emergency or after-hours routing | Prompt rules plus `transfer_call` to an on-call number | Complex rules (holiday calendars, rotating on-call): use the inbound webhook or a `custom` function |
| Block spam or unwanted numbers | `enable_dnc_detection`, fraud protection | Allow or deny lists: inbound webhook with `reject: true` |
| Take payments | None | Always custom, and avoid it: card details on calls raise PCI issues. Send a payment link by SMS instead. |

**Code tool vs custom function:** the `code` tool runs in Retell with no server to host. But it gets no LLM-filled arguments and must not hold secrets. Anything that needs an API key or caller-supplied values is a `custom` function, which needs a small hosted endpoint, such as a serverless function.

## 11. Dashboard-only, or needs the owner

- **OAuth integrations** (Google Calendar, Zoho, Dynamics, Monday, Zendesk, Google Drive, OneDrive): the owner signs in once on the Integrations page.
- **Payment method and KYC:** needed before buying numbers, calling out, or sending SMS.
- **A2P 10DLC SMS registration** (business documents).
- **Pre-call and post-call workflow functions:** the docs say these are dashboard-only (as of August 2026). The API spec does show `pre_session_tools`/`post_session_tools` on the agent, so **try the API first** and fall back to the dashboard.
- **Backup mode** toggle, branded or verified caller ID, and alert rules.

## 12. Gotchas and deprecations

**Learned on builds (2026-11-23):**
- **Published response engines are locked.** `PATCH /update-retell-llm` on a
  published LLM returns 400 "Cannot update published LLM". To change a live
  agent: `POST /create-agent-version/{agent_id}` with `{"base_version": N}`,
  which returns a draft whose `response_engine.version` is N+1. Then
  `PATCH /update-retell-llm/{llm_id}?version=N+1`, then
  `POST /publish-agent-version/{agent_id}` with `{"version": N+1}`.
- `publish-agent-version` needs `{"version": N}` in the body.
- Cal.com apps need `tenant_url: "cal.com"` (or `cal.eu`) on `create-app`.
- The Cal.com booking tool's fields come from the event type's booking
  fields (resolved by `get-app-tool-schema` round 2). Email is always
  required, and `list_calcom_bookings` searches by attendee email only.
- One Cal.com account shared by two clients: bookings on any event type
  block slots on all of them. Give each client their own account.
- A new account with no credits returns 402 "Credit balance exhausted" for
  playground, simulation, batch tests and web calls. Buying a number returns
  402 "requires a card on file". Creating and publishing agents works
  without credits.
- Multilingual: `language: ["en-US","es-419"]` with `retell-Sloane` is accepted.

**Learned on builds (2026-11-25):**
- **Model speed (playground round trip, median of 3, Toronto agent):**
  gpt-6-luna fast 0.92 s · gpt-6-luna standard 1.06 · gpt-6.2-sol fast 1.13
  · gpt-6.1-terra fast 1.17 · claude-5.5-haiku 1.38 · gpt-6.1-sol ultrafast
  1.97 · gemini-4-hydrogen 2.74 · gemini-3.8-flash 5.21 · gemini-4-carbon 6.19
  · gemini-4-neon 8.28. **Start with gpt-6-luna (fast), with backup
  claude-5.5-haiku**, then confirm with the build's own timing and batch tests.
  Details: `clients/daphne-toronto/build/model-choice.md`.
- **Tiers:** `fast` is offered on the GPT models; Claude and Gemini models
  accept only `standard`; `ultrafast` only on gpt-6.1-sol.
- **Small models act too early.** They need an explicit rule: "never book,
  change or cancel in the same turn you ask a question; wait for yes; never
  search before the email is confirmed". With that rule, luna went from 7/10
  to 9/10.
- `{{current_time}}` is a system variable: a test case's
  `dynamic_variables.current_time` does **not** override it. Write
  after-hours test criteria that hold either way.
- Simulated callers have no `{{user_number}}`; set
  `dynamic_variables.user_number` in test cases.
- `PUT /update-test-case-definition/{id}` takes partial bodies (metrics,
  dynamic_variables, tool_mocks).
- Cal.com **seated** event types (`seats.seatsPerTimeSlot`) work for
  restaurants (several tables per slot); a "number" booking field is exposed
  to Retell as a string.
- **Web calls through our own proxy:** with `RetellClient({ baseURL })` the
  SDK also sends WebRTC signaling to
  `<baseURL>/webrtc-proxy/<call_id>/v1/webrtc/sessions[/<id>]` (POST, PATCH,
  DELETE) with the call's own access token. Pass those through unchanged. The
  test page's `proxy.mjs` does this.
- Workspace API keys can stop working ("Invalid API Key") if the owner
  deletes them; ask for a new key, and check `get-api-key-info` before every
  build.

- Retired 400-error endpoints: `GET /list-agents`, `GET /list-chat-agents`, `GET /list-phone-numbers` and other v1 lists, `GET /get-agent-versions`, and `publish-agent`.
- Multi-prompt agents: creation ends **2026-12-15**.
- Model replacements happen automatically. Gemini 2.5 Pro becomes gemini-3.8-flash on **2026-11-29**, and GPT Realtime moves to 2.1 on **2027-01-19**. Legacy model fields are removed **2027-01-31**. Set models through `model_config`, not the legacy fields.
- `Update Call` only works on ended calls. Use `PATCH /v2/update-live-call/{id}` during a call.
- Custom functions can't reach localhost or private IPs. The endpoint must be public HTTPS.
- Transfers don't work on web calls. Test them with a real phone call.
- Third-party voices need `fallback_voice_ids`.
