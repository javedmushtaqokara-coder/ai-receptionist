# Daphne restaurant host: build report (2026-11-25)

## Built

- **Host "Ava"**: Retell agent `agent_c7c0705c10eb4d31a7556aef7e` ("Daphne
  Host") in the **"Test Calling Agent"** workspace, **published version 1**.
  Voice retell-Marissa, English, Toronto time. Speech recognition is primed
  with dish names.
- **Brain**: LLM `llm_2f2b2078d3b4720cf2e963a370fa` (version 1).
  **gpt-6-luna**, chosen by a real speed test (0.92 s median, the fastest of
  11), with backup claude-5.5-haiku. See `build/model-choice.md`.
- **Restaurant functions**, chosen from market research
  (`docs/business-types/restaurant.md`):
  1. **Reservations** in Cal.com: "Daphne Table Reservation" (`8071891`), 90
     minutes, a slot every 30 minutes, **4 tables per slot**. Hours "Daphne
     Reservation Hours" (`2694949`): lunch Mon–Fri 11:30–3, brunch Sat–Sun
     10:30–3, dinner Sun–Thu 5–10 and Fri–Sat 5–11. Each booking records
     party size (1–8), seating preference (dining room, patio, bar or
     lounge), occasion and allergies. Cal.com emails the confirmation.
  2. **Change and cancel** a reservation (found by email). After a cancel,
     Ava always offers to rebook.
  3. **Menu and FAQ**: the full lunch, brunch, dinner, dessert, happy hour
     and drinks menus with prices, all hours, address, vegetarian options.
  4. **Allergies**: Ava never guarantees a dish is allergen-free; she notes
     the allergy and says the kitchen will confirm.
  5. **Private dining (over 8 guests)**: an event lead (date, headcount,
     occasion, budget, contact) for the events team, or the website form.
  6. **Running late**: a note for the host; tables are held 15 minutes, and
     Ava offers to move the reservation.
  7. **Messages**: manager, lost and found, gift cards, jobs, vendors. Press
     gets pr@inkentertainment.com.
  8. **After hours**: Ava says when they reopen and still books and answers.
- **11 call fields** (call type, outcome, party size, reservation time,
  allergies or occasion, event details, unanswered question, and more).
- **Tests**: 10 simulation cases. **9 of 10 pass** on the live version.
- **Voice orb test page**: tested with a real web call; it went **live in
  0.85 s** (screenshot at `build/validation/voice-orb-live.png`). The
  container can't carry real audio, so the conversation itself needs a test
  from your laptop or phone.

## Assumed

- English only. Persona "Ava".
- Phone bookings may use up to 4 tables per 30-minute slot; tables run 90
  minutes. Last seatings fall out of those: 1:30 PM for lunch and brunch,
  8:30 PM Sunday to Thursday, 9:30 PM Friday and Saturday.
- Parking, dress code, take-out, corkage and patio season aren't on the
  site, so Ava says the team will confirm.
- Fallback number for the new line: 416-203-1414. **Change this if that
  line will be forwarded to Ava.**

## Couldn't do

1. **No phone number yet.** This workspace has credits but **no card**:
   "This item requires a card on file". To fix: log in at retellai.com,
   switch to **Test Calling Agent**, go to **Billing**, add a card, and tell
   me "done".
2. **OpenTable**: Daphne's real reservation book. Cal.com bookings don't
   appear there, so the host must copy them in (or Ava only takes requests).
   OpenTable's API is partner-only.
3. **Shared Cal.com account (4 clients)**: bookings block each other. Each
   client needs their own account.
4. **Messages and event leads by email** need the Vercel token and Resend key.
5. **Six owner questions** in `draft/questions.md`.

## Three test calls

### 1. Book a table
Say: "Hi, do you have a table for four this Friday around 7?"
Expect: Ava checks the book, offers the closest times, takes name, phone, email, seating and allergies, books it, and reads it back.
Check after: the reservation in Cal.com shows the party size and notes.

### 2. Big group
Say: "I'm planning a dinner for 15 people next month."
Expect: no booking; Ava explains the events team handles groups over 8 and takes date, headcount, occasion, budget and contact.
Check after: Call History shows call_type = private_event.

### 3. Curveball: allergy
Say: "Is the burger completely gluten-free? My friend has celiac."
Expect: no guarantee; Ava offers to note the allergy so the kitchen can go over safe options.
Check after: the transcript has no "it's safe" or "it's gluten-free".
