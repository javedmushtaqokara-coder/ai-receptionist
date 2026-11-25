# Perfect X Hair receptionist: build report (2026-11-25)

## Built

- **Receptionist "Mina"**: Retell agent `agent_4138b73cd738d82f0bcc5c4978`
  ("Perfect X Hair Receptionist") in the **"Salon Caling agent"** workspace,
  **published** (version 0). Voice retell-Chloe, English, Toronto time. Speech
  recognition is primed with all stylist names, the four locations, and perm
  and colour terms.
- **Brain**: Retell LLM `llm_083468f49992019b3089ec8f94c0`. gpt-6.1-sol on
  the ultrafast tier, with fast fallback to gemini-3.8-flash. The script is in
  `draft/prompt.md`.
- **Booking**: Cal.com connected inside the salon workspace
  (`app_06a9fa90da4521b68f3e038b`, auth ✅), with hours **"Perfect X Hair
  Hours"** (`2692015`): Mon–Thu 11–7 and Fri–Sun 10–8 Toronto time.
  Three appointment types, which Mina picks from the service:
  - Cut & Style, 1 hour (`8062514`)
  - Colour or Perm, 3 hours, $50 deposit (`8062515`)
  - Bleach, Balayage or Highlights, 5 hours, $100 deposit (`8062517`)

  Each booking records the **location** (one of the four), the exact
  **service**, the **preferred stylist**, name, phone and email. Cal.com
  emails the confirmation.
- **Reschedule and cancel**: found by booking email. Under 48 hours' notice,
  Mina mentions the late fee and deposit and offers to reschedule first.
- **FAQ**: the full price menu (about 50 services), all 4 locations with
  parking and subway directions, the stylists at each location and their
  specialities, every policy (deposits, cancellation, no-shows, late, no
  cash, no extensions, satisfaction guarantee), and the online shop code.
- **After hours, running late, and messages**: Mina says when the salon
  opens, still books and changes appointments, and takes messages (redo
  requests, gift cards, fees, a specific stylist, jobs).
- **Call fields**: 11 fields per call (call type, outcome, location,
  service, stylist, late cancellation, message, and more).
- **Tests**: 10 simulation test cases saved, with Cal.com mocked.
- **Shared research**: `docs/business-types/hair-salon.md`.

## Assumed

- Persona "Mina", English only.
- Service lengths: 1, 3 or 5 hours, based on the site's deposit tiers. The
  site doesn't list colour or perm durations.
- A "preferred stylist" is recorded, not guaranteed. The salon confirms it.
- Bookings are at least 2 hours ahead and up to 30 days out.
- Fallback number for the new line: 437-870-7250. **Change this if that
  line will be forwarded to Mina**, otherwise calls could loop.
- Roy and Zena (from Instagram) are listed at Yorkville. Zena isn't on the
  team page, so Mina doesn't offer her.

## Couldn't do

1. **The salon workspace has no credits and no card either**, so there's no
   phone number, no test calls and no simulation run. To fix, inside the
   **Salon** workspace:
   1. Log in at retellai.com.
   2. Switch to the Salon workspace.
   3. Go to **Billing**.
   4. Add a card and buy credits.
   5. Tell me "done".
2. **Vagaro conflict.** The salon really books in Vagaro (per stylist, with
   deposits). Cal.com bookings don't reach Vagaro, so a chair could be
   double-booked. In a single Cal.com account, one booking also blocks that
   time at all four locations. Decide with the owner (question 2): requests
   only for now, or booking through Vagaro (needs a custom function and
   Vagaro API access).
3. **Shared Cal.com account**: three clients now share it, so each client
   needs their own.
4. **Messages to the salon**: needs the Vercel token and Resend key (same as
   the other clients).
5. **Six owner questions** in `draft/questions.md`.

## Three test calls

### 1. Book a digital perm
Call as: a client who wants Sophia at Yorkville.
Say: "Hi, I'd like a digital perm and cut at Yorkville with Sophia this Friday."
Expect: 3-hour slots checked; booked with Yorkville, "Digital Perm + Cut" and Sophia; the $50 deposit and confirmation email mentioned.
Check after: the booking in Cal.com shows the location, service and stylist.

### 2. Late cancellation
Call as: Grace, with an appointment tomorrow.
Say: "I need to cancel my appointment tomorrow."
Expect: found by email and confirmed; the 48-hour policy and fee mentioned; rescheduling offered first.
Check after: Call History shows late_cancellation = true.

### 3. Curveball: extensions
Call as: someone with tape-in extensions.
Say: "Can you do my colour with my extensions still in?"
Expect: Mina politely explains extensions must be removed first, then offers to book.
Check after: no booking unless you accepted one.
