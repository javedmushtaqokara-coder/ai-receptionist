# Cowboy Air: call flow

```
Greeting: "Thanks for calling Cowboy Air Condition & Heating, this is Jessie. How can I help you today?"   [begin_message]
 │
 ├─ Danger (gas smell, smoke, fire, CO alarm) → leave the home and call 911 first          [prompt: Safety]
 │
 ├─ Repair / tune-up / estimate → booking                                                  [receptionist-booking]
 │    check_availability → offer 3 slots → name, phone, address, email, problem
 │    → book_appointment → read back → Cal.com emails the confirmation
 │    (outside area / no email / booking fails → take a message)
 │
 ├─ Change or cancel a visit                                                               [receptionist-cancel-reschedule]
 │    email → find_bookings → confirm → reschedule_booking or cancel_booking
 │
 ├─ Question (hours, area, prices, discounts, financing, sizing) → FAQ                     [receptionist-faq]
 │
 ├─ Emergency (no AC with heat risk, no heat in freezing weather, ceiling leak, breaker) → urgent message  [receptionist-after-hours]
 │
 ├─ Wants a person, complaint, warranty, billing, commercial → message                     [receptionist-lead-capture]
 │
 └─ Close: "Anything else?" → thanks → end_call                                            [end_call]

Every call → post-call analysis (name, number, reason, urgency, booking outcome, summary).
Office closed ({{current_time}} vs hours) → say so and when it reopens, then still help.
```
