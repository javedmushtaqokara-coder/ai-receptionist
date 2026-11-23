# Cowboy Air: validation (2026-11-23)

Evidence is in `build/validation/` and `build/api/`.

| Check | Result | Evidence |
|---|---|---|
| Agent exists (name, voice, language, timezone) | ✅ Cowboy Air Receptionist, retell-Marissa, en-US, America/Chicago | `get-agent.txt` |
| Agent published | ✅ version 0 published | `agent-versions.txt` |
| Model | ✅ gpt-6.1-sol ultrafast, backup gemini-3.8-flash | `get-retell-llm.txt` |
| No `[[OWNER]]` placeholders left in the prompt | ✅ (defaults used, listed as assumptions) | `get-retell-llm.txt` |
| Functions registered | ✅ check_availability, book_appointment, find_bookings, reschedule_booking, cancel_booking, end_call | `get-retell-llm.txt` |
| Cal.com authenticates | ✅ `success: true` | `test-app-auth.txt` |
| Cal.com read-only check | ✅ the Cowboy Air Service Visit type returns slots in Dallas hours | `calcom-slots.txt` |
| Custom function `notify-owner` | ⚠️ not built: needs the Vercel token and Resend key | none |
| Webhook on agent | ⚠️ none yet (comes with `notify-owner`) | `get-agent.txt` |
| Phone number attached | ❌ purchase refused: "This item requires a card on file" | `api/create-phone-number.response.txt` |
| Simulation batch (11 cases) | ⚠️ cases created; run refused: "Credit balance exhausted" | `api/create-batch-test.response.txt` |
| Model timing | ⚠️ refused: "Credit balance exhausted" | `build/model-choice.md` |
| Voice test page | ⚠️ settings ready (`build/test-page.json`); calls refused until credits are added, and a cloud session needs Vercel to give you a link | template tested earlier: loads and shows the credit error |
