# Daphne: validation (2026-11-25, version 1)

Workspace "Test Calling Agent" (`org_fn1ZqnGmkpiYIRyX`), key `RETELL_API_KEY_TEST`.

| Check | Result | Evidence |
|---|---|---|
| Agent exists and is published | ✅ version 1 is the latest published | `build/validation/agent-versions.txt` |
| Model | ✅ gpt-6-luna fast, backup claude-5.5-haiku (timed: 0.92 s median) | `build/model-choice.md` |
| Functions registered | ✅ check_availability, book_reservation, find_reservations, change_reservation, cancel_reservation, end_call | `build/api/create-retell-llm.request.json` |
| Cal.com authenticates (this workspace) | ✅ `success: true` | session log |
| Reservation slots | ✅ lunch, brunch and dinner hours, 4 tables per slot | session log |
| Simulation batch | ✅ 9 of 10 pass (the remaining one was a test artifact, since fixed) | `build/validation/test-runs-luna-strict.txt` |
| Voice orb page (web call) | ✅ went live in 0.85 s through the local proxy; audio not testable in the container | `build/validation/voice-orb-live.png` |
| Phone number | ❌ "This item requires a card on file" | `build/api/create-phone-number.response.txt` |
| Owner notifications | ⚠️ needs the Vercel token and Resend key | none |
