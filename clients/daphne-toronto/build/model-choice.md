# Model choice: Daphne (2026-11-25), the first build with credits

**Chosen:** `gpt-6-luna` on the fast tier, with fast fallback to
`claude-5.5-haiku` (standard tier, a different provider) after 1,500 ms.

## Speed test

3 playground turns per model on Ava's real prompt and tools (one question,
one reservation request that calls `check_availability`, one menu
question). Times are the full round trip through Retell's API from Canada,
in seconds. Raw data: `model-timing.json` and `model-timing-2.json`.

| Model | Tier | Runs | Median |
|---|---|---|---|
| **gpt-6-luna** | fast | 0.82 / 1.76 / 0.92 | **0.92** |
| gpt-6-luna | standard | 1.06 / 1.99 / 0.86 | 1.06 |
| gpt-6.2-sol | fast | 1.10 / 2.33 / 1.13 | 1.13 |
| gpt-6.1-terra | fast | 1.09 / 2.42 / 1.17 | 1.17 |
| claude-5.5-haiku | standard | 1.31 / 2.54 / 1.38 | 1.38 |
| gpt-6.1-sol | ultrafast | 1.70 / 3.38 / 1.97 | 1.97 |
| gpt-6.1-sol | fast | 1.55 / 4.33 / 2.35 | 2.35 |
| gemini-4-hydrogen | standard | 1.96 / 4.15 / 2.74 | 2.74 |
| gemini-3.8-flash | standard | 2.17 / 5.21 / 5.61 | 5.21 |
| gemini-4-carbon | standard | 4.15 / 6.19 / 7.00 | 6.19 |
| gemini-4-neon | standard | 4.67 / 26.83 / 8.28 | 8.28 |

Claude and Gemini models only offer the standard tier. All models called the
calendar tool correctly on the reservation turn.

## Quality test (10 simulation cases)

| Run | Model | Pass | Fail | Error |
|---|---|---|---|---|
| 1 | luna, first prompt | 7 | 2 | 1 |
| 2 | luna, fixes 1 | 6 | 3 | 1 |
| 3 | gpt-6.2-sol, strict prompt | 8 | 1 | 1 |
| 4 | **luna, strict prompt** | **9** | 1 | 0 |

The fixes that mattered: a "golden rule" never to book, change or cancel in
the same turn as asking a question; to ask for the email before searching;
to offer rebooking after a cancel; and to offer to move a booking when the
guest will be over 15 minutes late. The remaining failure (after hours) is a
test artifact: Retell fills `{{current_time}}` with the real time, which was
during dinner service, so the agent correctly didn't say "closed". That
test's criteria were then fixed.

## Lesson for every build

The "ultrafast" model assumed for the earlier agents is about 2× slower
than gpt-6-luna. Re-time and switch Cowboy Air, Miami Kitchen & Bath and
Perfect X Hair once their workspace keys work again.
