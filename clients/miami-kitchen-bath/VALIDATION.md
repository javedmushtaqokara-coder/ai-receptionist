# Miami Kitchen & Bath: validation (2026-11-23)

| Check | Result | Evidence |
|---|---|---|
| Agent exists (name, voice, languages, timezone) | ✅ retell-Sloane, en-US and es-419, America/New_York | `build/validation/get-agent.txt` |
| Agent published | ✅ version 0 | `build/validation/agent-versions.txt` |
| Model | ✅ gpt-6.1-sol ultrafast, backup gemini-3.8-flash | `build/validation/get-retell-llm.txt` |
| Functions registered | ✅ end_call (no integrations requested) | `get-retell-llm.txt` |
| Integrations | n/a (none requested) | none |
| Lead fields | ✅ 15 post-call fields | `get-agent.txt` |
| `notify-owner` function | ⚠️ needs the Vercel token and Resend key | none |
| Phone number | ❌ "This item requires a card on file" | `build/api/create-phone-number.response.txt` |
| Simulation batch (9 cases) | ⚠️ cases created; run refused: "Credit balance exhausted" | `build/api/create-batch-test.response.txt` |
| Voice test page | ⚠️ `build/test-page.json` ready; blocked by credits (and by Vercel, for a cloud link) | none |
