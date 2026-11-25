# Restaurant (full-service, upscale casual and fine dining)

Last checked: 2026-11-25. Sources: Claude's industry knowledge of restaurant
host-stand calls and of what AI phone hosts for restaurants typically handle
(reservations, FAQs, large parties, take-out, messages), plus the first
client's site (daphnetoronto.com). Add to this file on later restaurant
builds.

## 1. What calls sound like

- **Who calls:** guests wanting a table (by far the most), guests with an
  existing reservation (change, cancel, running late), people with
  questions (hours, menu, dietary, parking, dress code), event planners
  (birthdays, corporate, buy-outs), and lost and found, gift cards, job
  seekers, vendors, press and spam.
- **When:** peaks just before lunch and from 4–7 PM, exactly when staff are
  busiest. Missed calls are missed covers, which is the main reason
  restaurants use AI phone hosts.
- **Mood:** quick and practical. Callers want an answer in under a minute.
- **Sample openings:**
  1. "Hi, do you have a table for four tonight around 7?"
  2. "Can I move my reservation from Friday to Saturday?"
  3. "Do you have gluten-free options?"
  4. "We're running 15 minutes late for our 7:30."
  5. "I'm planning a birthday dinner for 20 people next month."

## 2. Call mix

| Reason | Share |
|---|---|
| New reservation | 40–50% |
| Change, cancel or running late | 15–20% |
| Hours, location, parking, menu and price questions | 15–20% |
| Dietary and allergy questions | 5–10% |
| Large parties and private events | 5–10% |
| Take-out or delivery, gift cards, lost and found, jobs, vendors | the rest |

## 3. The functions a restaurant phone agent needs

1. **Reservations: book, change, cancel.** Party size, date, time, name,
   phone, seating preference, occasion, allergies. Offer nearby times if the
   requested time is full.
2. **Menu and FAQ:** hours by meal period, address and transit, parking,
   menu items and prices, happy hour, patio, dress code, kids, corkage, gift
   cards.
3. **Dietary and allergies:** describe dishes from the menu, but never
   guarantee a dish is allergen-free. Note the allergy on the reservation
   and say the server and kitchen will confirm.
4. **Large parties and private events:** above the table limit, capture the
   lead (date, headcount, budget, occasion, contact) for the events team, or
   point to the events form.
5. **Running late:** note it. Tables are usually held for about 15 minutes.
6. **Messages:** a manager request, complaints, lost and found, gift cards,
   jobs, vendors, press (often to a separate email).
7. **After hours:** still take and change reservations, and answer
   questions.
8. **Take-out and delivery:** only if the restaurant offers it. Usually
   point to the delivery apps rather than taking orders by phone.

## 4. Reservation systems

OpenTable, Resy, Tock, SevenRooms, Yelp Guest Manager. Private events often
use Tripleseat. None of these has a native Retell integration (as of
2026-11), and their APIs are partner-only. The options are: book in a
separate calendar (such as Cal.com) that staff copy into the main book;
take reservation requests; or build a custom function once API access is
granted. Make sure staff know which one applies, to avoid double booking.

## 5. What gets transferred or escalated

Complaints about a recent visit, billing disputes, urgent same-day changes
to large parties, press, and anything about allergies that needs the
kitchen.

## 6. Rules and risks

- Never guarantee that a dish is free of an allergen, or that a specific
  table or seating will be available. Note the request instead.
- Never promise to hold a table beyond the policy, or to waive deposits.
- Don't take card numbers over the phone.
- For alcohol questions, follow local rules (no promotions to minors).
