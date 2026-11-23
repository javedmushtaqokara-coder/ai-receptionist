# Miami Kitchen & Bath: validation (2026-11-23, version 1)

| Check | Result | Evidence |
|---|---|---|
| Agent exists (name, voice, languages, timezone) | ✅ retell-Sloane, en-US and es-419, America/New_York | `build/validation/get-agent.txt` |
| Agent published | ✅ version 1 (latest published) | `build/validation/agent-versions.txt` |
| Model | ✅ gpt-6.1-sol ultrafast, backup gemini-3.8-flash | `build/validation/get-retell-llm.txt` |
| Functions registered | ✅ check_availability, book_appointment, find_bookings, reschedule_booking, cancel_booking, end_call | `get-retell-llm.txt` |
| Cal.com authenticates | ✅ `success: true` | (same connection as Cowboy Air) |
| Cal.com read-only check | ✅ the estimate type returns slots in Miami hours | `build/validation/calcom-slots.txt` |
| Lead fields | ✅ 15 post-call fields | `get-agent.txt` |
| `notify-owner` function | ⚠️ needs the Vercel token and Resend key | none |
| Phone number | ❌ "This item requires a card on file" | `build/api/create-phone-number.response.txt` |
| Simulation batch (13 cases) | ⚠️ cases created; run refused: "Credit balance exhausted" | `build/api/create-batch-test.response.txt` |
| Voice test page | ⚠️ blocked by credits (and by Vercel, for a cloud link) | `build/test-page.json` |
| Shared Cal.com account | ⚠️ bookings from both clients block each other's slots | see `REPORT.md` |
