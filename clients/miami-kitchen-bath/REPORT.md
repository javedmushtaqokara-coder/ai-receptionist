# Miami Kitchen & Bath receptionist: build report (2026-11-23)

## Built

- **Receptionist "Sofia"**: Retell agent `agent_8dbfe430b1b3ca97d80f655042`
  ("Miami Kitchen & Bath Receptionist"), **published** (version 0).
  **Bilingual English and Spanish** (`en-US` and `es-419`): she answers in
  the caller's language. Voice retell-Sloane, Miami (Eastern) time.
- **Brain**: Retell LLM `llm_796b38572c5ff953ba5b65878b5f`. gpt-6.1-sol on
  the ultrafast tier, with fast fallback to gemini-3.8-flash (same choice and
  reasoning as Cowboy Air). The script is in `draft/prompt.md`.
- **Answering questions**: everything from the site: services, the 5-step
  process, all 25 Miami-Dade areas, price ranges from their cost guide and
  FAQs, timelines, the full warranty terms, licensing and permits, hours,
  reviews, and Adam.
- **Free estimate requests (lead capture)**: Sofia qualifies each caller:
  name, phone, email, project, property and condo building, area, timeline,
  budget, best visit times, and how they heard about the company. She
  promises a callback within one business day, which is the site's own
  promise.
- **Existing clients, warranty and urgent leaks**: details taken; leaks get
  "shut off the main valve" and are marked urgent.
- **After hours**: says the office is closed and when it reopens, and still
  takes the full request.
- **Lead fields**: 15 fields recorded on every call (project type, timeline,
  budget, language, urgency, and more).
- **Tests**: 9 simulation test cases saved, including a Spanish-only caller,
  price pressure, the wall-removal question, a warranty claim and a leak.
- **Shared research**: `docs/business-types/kitchen-bath-remodeling.md`.

## Assumed

- **No calendar booking.** No calendar was given, and remodelers confirm
  visits by phone. Sofia takes the request and the team calls back.
- Persona "Sofia"; voice retell-Sloane, accepted by Retell for English and
  Spanish.
- Hours Mon–Fri 8–6 and Sat 9–3, from the site's business data (the pages
  themselves don't show hours).
- Price ranges are given as the site's planning estimates, never as quotes.
- Leads outside Miami-Dade are taken for the team to confirm, not refused.
- No live transfers, since no number is known yet.
- Fallback number for the new line: (305) 423-8277. **Change this if that
  line will be forwarded to Sofia**, otherwise calls could loop.

## Couldn't do

1. **Retell needs a card and credits.** This is the same block as Cowboy
   Air: no phone number, no test calls, no simulation run. To fix:
   1. Log in at retellai.com.
   2. Go to **Billing**.
   3. Add a card.
   4. Buy credits.
   5. Tell me "done".
2. **Leads don't reach the owner yet.** This needs the Vercel token and
   Resend key (asked once; shared with Cowboy Air). Until then, leads are in
   Retell **Call History**.
3. **The six owner questions** in `draft/questions.md`.

## Three test calls

### 1. Kitchen estimate in a condo
Call as: a Brickell condo owner planning a kitchen remodel.
Say: "Hi, I want to redo my kitchen in my Brickell condo. Do you do free estimates?"
Expect: the free consultation offered; name, phone, project, building, timeline and visit times collected; "the team will call within one business day".
Check after: Call History shows call_type = new_estimate_request.

### 2. Spanish-speaking caller
Call as: a Hialeah homeowner who speaks only Spanish.
Say: "Hola, quiero cambiar mi bañera por una ducha. ¿Cuánto cuesta más o menos?"
Expect: the whole call in Spanish; the $8,000–$40,000+ range as an estimate only; the request taken.
Check after: language = spanish.

### 3. Curveball: the wall
Call as: a homeowner wanting open concept.
Say: "Can I take out the wall between my kitchen and living room?"
Expect: no yes or no; she explains it's assessed at the free visit and offers to book.
Check after: no structural advice in the transcript.
