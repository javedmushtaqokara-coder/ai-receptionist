# Cowboy Air receptionist: build report (2026-11-23)

## Built

- **Receptionist "Jessie"**: Retell agent `agent_806433bde282144f7d62420ddd`
  ("Cowboy Air Receptionist"), **published** (version 0). Voice
  retell-Marissa, English (US), Dallas time.
- **Brain**: Retell LLM `llm_a030cf49052392c221d26fbb9f6d`. Primary model
  gpt-6.1-sol on the ultrafast tier, with fast fallback to gemini-3.8-flash.
  The script is in `draft/prompt.md`.
- **Booking, reschedule and cancel**: Cal.com connected natively
  (`app_7fc8a1b6f0116745fda3fbfd`, auth ✅). I created a new **"Cowboy Air
  Service Visit"** appointment type (`8035996`) with its own working hours
  **"Cowboy Air Hours"** (`2683659`): Mon–Fri 8:30–5 and Sat 9–1, Central
  time. Visits are one hour, booked at least an hour ahead and up to 30 days
  out. Each booking captures name, email, phone, service address and the
  problem. Cal.com emails the caller a confirmation.
- **FAQ**: everything from cowboyair.com: hours, the 14 DFW cities, all
  services, published price ranges, discounts, financing, licence, team, and
  the site's FAQ answers.
- **After hours**: Jessie knows when the office is closed, says when it
  reopens, still books and takes messages, and treats emergencies as urgent
  messages. Gas smell, smoke or a CO alarm always gets "leave the home, call
  911" first.
- **Messages**: 9 post-call fields on every call (name, callback number,
  address, reason, urgency, outcome, needs callback, after hours,
  unanswered question).
- **Tests**: 11 simulation test cases saved in Retell, with Cal.com mocked.
- **Shared research**: `docs/business-types/hvac.md` for future HVAC clients.

## Assumed

- Persona name "Jessie", friendly Texan tone, female American voice.
- Prices are given as the site's **"typical DFW ranges"** ($89–149
  diagnostic, $150–250 after-hours premium), never as Cowboy Air's own
  fixed fees.
- One visit per one-hour slot; visits start Mon–Fri 9 AM–4 PM and Sat 9 AM–noon.
  Sunday ("by appointment") isn't bookable; Jessie takes a message.
- Callers must give an email to book, because Cal.com requires one and it's
  how Jessie finds visits to change or cancel. Callers with no email get a
  callback message instead.
- Emergencies become urgent messages (no live transfer), because no on-call
  number is known yet.
- No call transfers to a person yet, for the same reason.
- Model chosen without timing (see `build/model-choice.md`).
- Fallback number for the new line: (214) 570-1540. **Change this if the
  main line will be forwarded to Jessie**, otherwise calls could loop.
- I added the new Cal.com appointment type and hours. The two existing
  appointment types in that Cal.com account (which use New York and Karachi
  time settings) were left untouched.

## Couldn't do

1. **Retell has no credits and no card.** That blocks the phone number, test
   calls, the simulation tests and model timing. To fix:
   1. Log in at retellai.com.
   2. Go to **Billing**.
   3. Add a card.
   4. Buy credits ($20 is plenty for testing).
   5. Tell me "done".
2. **Messages don't reach you yet.** Retell can't send email, so this needs
   one small function on Vercel. To fix:
   1. vercel.com: sign up, then **Settings**, **Tokens**, **Create**, and paste it here.
   2. resend.com: sign up, then **API Keys**, **Create**, and paste it here.
   Until then, messages are in Retell's **Call History**, with the summary
   and the 9 fields.
3. **The six owner questions** in `draft/questions.md` (phone line,
   emergencies, exact prices, where messages go, capacity, holidays).

## Three test calls

### 1. AC out: book a visit
Call as: a homeowner in Dallas whose AC is blowing warm air.
Say: "Hi, my AC's blowing warm air since this morning. Can somebody come out?"
Expect: Jessie checks the calendar, offers up to three times, takes your name, phone, address and email (spelled back), and books it.
Check after: the booking in Cal.com and the confirmation email.

### 2. After-hours emergency
Call as: someone calling Saturday night, 88°F inside, an elderly parent at home.
Say: "It's 88 degrees in here and my elderly mom lives with me. The AC just died."
Expect: urgent handling; name, phone and address taken; "the on-call team will call you back"; the after-hours premium mentioned; no exact time promised.
Check after: Call History shows urgency = emergency.

### 3. Price curveball
Call as: a shopper comparing companies.
Say: "Just give me a price, how much to replace my AC?"
Expect: the $5,000–$12,000 typical range, no firm quote, and an offer of the free in-home estimate with the Manual J sizing.
Check after: no booking unless you accepted one.
