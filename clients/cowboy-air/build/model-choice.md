# Model choice

**Chosen:** primary `gpt-6.1-sol` on the `ultrafast` tier, with fast fallback
to `gemini-3.8-flash` (standard tier) after 1,500 ms.

## How it was chosen

- Model list: the `LLMModel` enum in Retell's API spec (checked 2026-11-23).
- Retell publishes no per-model latency numbers. Its guidance: smaller and
  faster models, a short prompt, the fast tier, and fast fallback.
- `gpt-6.1-sol` is the only model Retell allows on the `ultrafast` tier
  ("much faster response generation"), which makes it the platform's fastest
  configured option. The backup is from a different provider, in case
  OpenAI is slow or down.
- **Not timed yet.** The planned timing (3 playground turns per shortlisted
  model) was refused with `402 Credit balance exhausted`.

## To do once credits are added

Time `gpt-6.1-sol` (ultrafast), `gpt-6.2-sol`, `gpt-6-luna`,
`claude-5.5-haiku`, `gemini-3.8-flash` and the `gemini-4-*` models with
`POST /agent-playground-completion/agent_806433bde282144f7d62420ddd`. Keep
the fastest one that passes the test batch.
