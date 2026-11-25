# Perfect X Hair: validation (2026-11-25)

Workspace: "Salon Caling agent" (`org_dANbZtcNFZ1SA6as`), key `RETELL_API_KEY_SALON`.

| Check | Result | Evidence |
|---|---|---|
| Right workspace | ✅ `get-api-key-info` returns "Salon Caling agent" | session log |
| Agent exists (name, voice, language, timezone) | ✅ retell-Chloe, en-US, America/Toronto | `build/validation/get-agent.txt` |
| Agent published | ✅ version 0 | `build/validation/agent-versions.txt` |
| Model | ✅ gpt-6.1-sol ultrafast, backup gemini-3.8-flash | `build/validation/get-retell-llm.txt` |
| Functions registered | ✅ check_availability and book for cut, colour and bleach; find_bookings, reschedule_booking, cancel_booking, end_call | `get-retell-llm.txt` |
| Cal.com authenticates (salon workspace) | ✅ `success: true` | `build/validation/test-app-auth.txt` |
| Booking fields | ✅ location menu (4 locations), service, stylist | session log |
| Call fields | ✅ 11 | `get-agent.txt` |
| Phone number | ❌ "This item requires a card on file" | `build/api/create-phone-number.response.txt` |
| Playground and simulation (10 cases) | ⚠️ "Credit balance exhausted" | `build/validation/playground-1.txt`, `build/api/create-batch-test.response.txt` |
| `notify-owner` function | ⚠️ needs the Vercel token and Resend key | none |
| Voice test page | ⚠️ blocked by credits; `build/test-page.json` ready | none |
