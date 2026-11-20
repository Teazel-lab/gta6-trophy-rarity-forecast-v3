# R1 — snapshot movement

Measured 2026-11-20 from `_rec/*.html.gz` (10 files), `_kit/input/p01.in` history, and one Wayback capture. Rates are the percents Exophase prints. Logit is the scoring logit: `ln(p/(1-p))` with the rate clamped to 0.01..99.99 before dividing by 100. Log-time is `x = ln(1+h)` with `h` hours since 2026-11-19T00:00Z, the same clock as the house curve baseline. The target 2026-11-26T00:00Z is `h = 168`, `x = 5.130`.

## Summary

1. The 10 local recordings are two page states. Six files from 11:10:21Z through 12:03:49Z are identical (36,080 players). Four files from 15:59:50Z through 17:40:29Z are identical (44,161 players). Wayback 2026-11-20T13:16:24Z is a third state in between (42,228 players).
2. Launch night in `p01.in` is a single earlier state. All 8 reads (slots 2026-11-18T23:50Z through 2026-11-19T03:00Z) have 638 players, 943 trophies earned, and the same 55 rates. The rules say that page was still unchanged at 04:00Z. The 3,868-player refresh by 04:30Z is described there, and its per-trophy rates are not in the case file, so they are not in the tables below.
3. The HTML has no last-updated time (no `updated`, no `<time>`, no date besides the copyright line 2006–2026). Each row prints a rarity word and an EXP figure beside the percent. EXP is a different series: Gone Fishing stayed 100% while EXP went 73 → 75 → 63, and Chapter 4 stayed 0.02% while EXP went 7,257 → 7,389 → 6,191.
4. Players in the public window: 36,080 → 42,228 → 44,161. That is +6,148 then +1,933, or about 2,930/h then 710/h between the reads we have (+1.61 in `ln(players)` per unit of `x` over the whole window, +2.79 then +0.65). These are changes between Exophase refreshes, so the per-hour figures are snapshot-to-snapshot, not a live arrival rate. Trophies earned: 45,648 → 56,989 → 60,923 (1.27, then 1.35, then 1.38 per tracked player).
5. From the first public state to the last, 26 trophies kept the same printed rate, 20 rose by at most 0.05 points, and 9 rose by more than 0.05. None fell on net. The only dip is The Lone Rider, 0.02 → 0.01 → 0.02. Twenty-five trophies were flat on all three public reads.
6. Moving up, clearly above the 0.01 grid: Chapter 1 (7.99 → 11.10 → 11.98), fishing (10.57 → 12.76 → 13.30), Breakfast Run (2.52 → 3.77 → 4.26), Chapter 2 (0.90 → 1.44 → 1.71), plus vehicles, bowling, and a few activities. Flat: Gone Fishing at 100% on every read including launch night; Chapter 4 and the final mission at 0.02%; most stranger, collectible, and completion trophies at 0.00–0.02%. There is no Chapter 5 trophy. The gold final-mission trophy is id 7.
7. On the clamped logit the public steps for Chapter 1 are +0.363 then +0.086 (+6.43 then +1.25 per unit of `x`). Chapter 2 is +0.475 then +0.175 (+8.42 then +2.54 per `x`). The pace slowed on the second step for 18 of the 19 trophies whose first step was steeper than 0.5 logit per `x`.
8. A least-squares line of clamped logit on `x` through the three public points, read at the target, puts Chapter 1 near 95% and Chapter 2 near 96%. The later segment alone, carried the same way, puts them near 45% and 39%. The line's `x` only runs from 3.588 to 3.714 (4.8 hours); the target is 1.42 further, about twenty times the later gap. Those percents are what the log-time line says, and the deceleration says the line is too steep to treat as the week-ahead rate.
9. Chapter 3 ticked 0.02 → 0.03 and then stayed. Chapter 4 and the final mission have slope 0, so the same line leaves them at 0.02%. Versus launch night, Chapter 1, Chapter 2, Breakfast Run, and fishing are already above the pre-release rates; Chapter 3, Chapter 4, the final mission, the platinum, and 100% completion are still below theirs.
10. A one-tick move (0.01 point) near the floor is about +0.4 to +0.7 logit and a slope near 6–10 per `x` over this gap, which the same extrapolation blows up (Kenton's strand, The Lone Rider). Those slopes are the 0.01 grid. Clamping also makes 0.00 and 0.01 the same logit, so the platinum and the 100% trophy show zero logit movement. At 15:59Z Platinum Club reads 1 while the platinum prints 0.01%; 1/44,161 is 0.0023%, which would print as 0.00 if the percent were the ratio rounded to 2 decimals.

## Observations

| tag | when (UTC) | where | players | trophies earned | platinum club | same page held |
|---|---|---|---:|---:|---:|---|
| L | slots 2026-11-18T23:50Z through 2026-11-19T03:00Z | `p01.in` history, 8 identical reads | 638 | 943 | — | rules: still unchanged at 04:00Z |
| A | 2026-11-20T11:10:21Z | `_rec`, 6 identical files, last 12:03:49Z | 36,080 | 45,648 | 0 | at least 0.89 h |
| W | 2026-11-20T13:16:24Z | Wayback `20261120131624`, status 200 | 42,228 | 56,989 | 0 | one capture |
| B | 2026-11-20T15:59:50Z | `_rec`, 4 identical files, last 17:40:29Z | 44,161 | 60,923 | 1 | at least 1.68 h |

CDX `url=exophase.com/game/grand-theft-auto-vi-psn/trophies/&output=json` returns one row, timestamp 20261120131624, status 200, length 13361 (compressed; the raw body is a full trophy page, 55 rows). The same query restricted to 2026-11-19 returns an empty list. A prefix query for the whole game path timed out with no body. `h` at A, W, B is 35.17, 37.27, 40.00. `x` is 3.5883, 3.6448, 3.7135. Deltas of `x`: A→W 0.0565, W→B 0.0688, B→target 1.416.

Local file spacing is about 10 minutes inside a cluster (gaps 10.0 to 11.8 minutes) with holes in the recording of 3.93 h (12:03Z to 15:59Z) and 1.25 h (15:59Z to 17:14Z). The content itself changed twice in the 4.82 h from A to B: once inside (12:03:49Z, 13:16:24Z] (1.21 h) and once inside (13:16:24Z, 15:59:50Z] (2.72 h). The morning cluster and the evening cluster show no change. That matches a refresh every few hours. Our reads do not pin the refresh to a minute, and the page does not print one.

List order on the page is trophy id. `data-award-id` is 1..55 in that order, and the 55 names match `p01.in` exactly. Id 1 is the platinum.

## Rates

Kinds: `plat` platinum, `prol` Gone Fishing (the only 100% row; no trophy is named Prologue), `ch1`–`ch4` the four chapter trophies, `final` the gold final mission, `100%` the gold 100% completion, `coll` count-the-things trophies (stunts, drones, meditation spots, card sets, WAiNK, challenges, 100 vehicles, the whole map, all garages), `side` everything else, including named missions and stranger strands. No description says Chapter 5.

| id | kind | trophy | L | A | W | B |
|---:|:---|:---|---:|---:|---:|---:|
| 1 | plat | Vice Got a Price! | 0.63 | 0.00 | 0.00 | 0.01 |
| 2 | prol | Just Like Paradise | 100.00 | 100.00 | 100.00 | 100.00 |
| 3 | ch1 | Paradise Lost | 1.25 | 7.99 | 11.10 | 11.98 |
| 4 | ch2 | T\*\*s Ass Drug Money | 1.10 | 0.90 | 1.44 | 1.71 |
| 5 | ch3 | Vice City, Baby! | 1.10 | 0.02 | 0.03 | 0.03 |
| 6 | ch4 | Top Of The World, Ma | 1.10 | 0.02 | 0.02 | 0.02 |
| 7 | final | You Gotta Know When to Get Off | 1.10 | 0.02 | 0.02 | 0.02 |
| 8 | side | Trust | 1.10 | 2.52 | 3.77 | 4.26 |
| 9 | side | Break the Bank | 1.10 | 0.02 | 0.03 | 0.03 |
| 10 | side | Family Matters | 1.10 | 0.02 | 0.02 | 0.02 |
| 11 | side | DWNFALL | 1.10 | 0.02 | 0.02 | 0.02 |
| 12 | side | Hi-Jacked | 1.10 | 0.02 | 0.02 | 0.02 |
| 13 | side | Snow Storm | 1.10 | 0.02 | 0.02 | 0.02 |
| 14 | 100% | A Long Road | 0.63 | 0.00 | 0.00 | 0.01 |
| 15 | coll | Cunning Stunts | 0.63 | 0.00 | 0.00 | 0.01 |
| 16 | side | Master of None | 0.78 | 0.01 | 0.01 | 0.01 |
| 17 | side | The Shootist | 0.63 | 0.01 | 0.01 | 0.01 |
| 18 | coll | Top Fun | 0.63 | 0.00 | 0.00 | 0.01 |
| 19 | side | Earn Cash, Not Kudos | 0.78 | 0.01 | 0.01 | 0.01 |
| 20 | side | Baited My Tackle | 2.04 | 10.57 | 12.76 | 13.30 |
| 21 | side | Stick Fiddler | 0.94 | 1.11 | 1.31 | 1.42 |
| 22 | side | Road to Rehabilitation | 0.78 | 0.01 | 0.01 | 0.01 |
| 23 | side | This Was No Boat Accident | 0.78 | 0.01 | 0.01 | 0.02 |
| 24 | side | The Lone Rider | 0.78 | 0.02 | 0.01 | 0.02 |
| 25 | side | Strangers & Freaks | 0.63 | 0.00 | 0.00 | 0.01 |
| 26 | side | Supply & Demand | 0.63 | 0.01 | 0.01 | 0.01 |
| 27 | side | Spin On This! | 0.78 | 0.01 | 0.01 | 0.01 |
| 28 | coll | Positive Mental Attitude | 0.63 | 0.01 | 0.01 | 0.01 |
| 29 | side | Fair Game | 0.78 | 0.01 | 0.01 | 0.01 |
| 30 | coll | Don't Touch My Deck | 0.63 | 0.00 | 0.00 | 0.01 |
| 31 | coll | You WAiNKer! | 0.63 | 0.00 | 0.00 | 0.01 |
| 32 | coll | One Last Thing | 0.63 | 0.00 | 0.00 | 0.01 |
| 33 | side | Hot Together | 0.94 | 0.19 | 0.27 | 0.31 |
| 34 | side | Retail Therapy | 0.78 | 0.02 | 0.03 | 0.04 |
| 35 | coll | Whip It Good | 1.25 | 1.02 | 1.42 | 1.70 |
| 36 | side | Gunslinger | 0.78 | 0.07 | 0.07 | 0.08 |
| 37 | side | Catch Me If You Can | 0.94 | 0.18 | 0.22 | 0.23 |
| 38 | side | Challenging Tank | 1.57 | 0.17 | 0.19 | 0.20 |
| 39 | side | Sneakthief | 0.94 | 0.03 | 0.04 | 0.04 |
| 40 | side | Maximum Withdrawal | 0.78 | 0.01 | 0.01 | 0.01 |
| 41 | side | A Classic Blitz Play | 0.94 | 0.01 | 0.01 | 0.01 |
| 42 | coll | The Goodtime State | 0.78 | 0.02 | 0.04 | 0.04 |
| 43 | side | Pest Control | 0.78 | 0.01 | 0.01 | 0.01 |
| 44 | side | In The Beginning… | 0.94 | 0.12 | 0.15 | 0.17 |
| 45 | side | Capital Offense | 0.78 | 0.01 | 0.01 | 0.01 |
| 46 | side | Let’s Go Bowling | 0.78 | 0.75 | 1.09 | 1.26 |
| 47 | side | Personal Best | 0.78 | 0.01 | 0.01 | 0.01 |
| 48 | side | Actions Speak Louder | 0.78 | 0.01 | 0.01 | 0.01 |
| 49 | side | Bad Luck, I Guess | 0.78 | 0.01 | 0.01 | 0.01 |
| 50 | side | The Truth Is Out There | 0.78 | 0.44 | 0.64 | 0.72 |
| 51 | side | Ten Pin | 0.78 | 0.04 | 0.05 | 0.06 |
| 52 | side | Dime on the Dollar | 0.78 | 0.01 | 0.01 | 0.01 |
| 53 | side | Treat Yo Self | 0.94 | 0.02 | 0.03 | 0.03 |
| 54 | coll | Little Boxes | 0.78 | 0.01 | 0.01 | 0.01 |
| 55 | side | On the Spot | 0.78 | 0.01 | 0.01 | 0.01 |

## By kind, first public state to last

Up / flat are counts of printed rates. Mean Δlogit is the clamped logit. Mean slope is the 3-point least-squares slope of that logit on `x`.

| kind | n | up | flat | mean Δ points | mean Δlogit | mean slope per `x` |
|---|---:|---:|---:|---:|---:|---:|
| plat | 1 | 1 | 0 | +0.010 | +0.000 | +0.00 |
| prol | 1 | 0 | 1 | +0.000 | +0.000 | +0.00 |
| ch1 | 1 | 1 | 0 | +3.990 | +0.449 | +3.51 |
| ch2 | 1 | 1 | 0 | +0.810 | +0.650 | +5.10 |
| ch3 | 1 | 1 | 0 | +0.010 | +0.406 | +3.12 |
| ch4 | 1 | 0 | 1 | +0.000 | +0.000 | +0.00 |
| final | 1 | 0 | 1 | +0.000 | +0.000 | +0.00 |
| 100% | 1 | 1 | 0 | +0.010 | +0.000 | +0.00 |
| side | 38 | 17 | 21 | +0.156 | +0.167 | +1.33 |
| coll | 9 | 7 | 2 | +0.083 | +0.135 | +1.05 |

`side` mixes a few trophies that are actually moving (Breakfast Run, fishing, arcade, bowling, the cocktail, Hot Together) with a large floor that is flat, so its mean slope is a poor summary. The nine trophies up more than 0.05 points from A to B are ids 3, 4, 8, 20, 21, 33, 35, 46, and 50.

## Logit steps and the log-time line

Δlogit is per refresh, on the clamped scale. Slope is Δlogit / Δ`x`. `ext3` reads the 3-point line at `h = 168`. `ext2` carries only the later slope (W→B) from B's logit to the same `x`. For a flat trophy both equal the clamped rate. For a 0% or 100% rate the clamp forces the logit to `logit(0.01)` or `logit(99.99)`, so a line through the ceiling stays at 99.99 in this column even though the page says 100.

| id | trophy | A | W | B | Δlogit A→W | Δlogit W→B | slope A→W | slope W→B | ols | ext3 | ext2 |
|---:|:---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | Vice Got a Price! | 0.00 | 0.00 | 0.01 | +0.000 | +0.000 | +0.00 | +0.00 | +0.00 | 0.01 | 0.01 |
| 2 | Just Like Paradise | 100.00 | 100.00 | 100.00 | +0.000 | +0.000 | +0.00 | +0.00 | +0.00 | 99.99 | 99.99 |
| 3 | Paradise Lost | 7.99 | 11.10 | 11.98 | +0.363 | +0.086 | +6.43 | +1.25 | +3.51 | 95.34 | 44.58 |
| 4 | T\*\*s Ass Drug Money | 0.90 | 1.44 | 1.71 | +0.475 | +0.175 | +8.42 | +2.54 | +5.10 | 96.17 | 38.83 |
| 5 | Vice City, Baby! | 0.02 | 0.03 | 0.03 | +0.406 | +0.000 | +7.18 | +0.00 | +3.12 | 2.61 | 0.03 |
| 6 | Top Of The World, Ma | 0.02 | 0.02 | 0.02 | +0.000 | +0.000 | +0.00 | +0.00 | +0.00 | 0.02 | 0.02 |
| 7 | You Gotta Know When to Get Off | 0.02 | 0.02 | 0.02 | +0.000 | +0.000 | +0.00 | +0.00 | +0.00 | 0.02 | 0.02 |
| 8 | Trust | 2.52 | 3.77 | 4.26 | +0.416 | +0.127 | +7.36 | +1.85 | +4.25 | 95.05 | 37.99 |
| 14 | A Long Road | 0.00 | 0.00 | 0.01 | +0.000 | +0.000 | +0.00 | +0.00 | +0.00 | 0.01 | 0.01 |
| 20 | Baited My Tackle | 10.57 | 12.76 | 13.30 | +0.213 | +0.048 | +3.77 | +0.69 | +2.03 | 73.75 | 29.05 |
| 21 | Stick Fiddler | 1.11 | 1.31 | 1.42 | +0.168 | +0.082 | +2.97 | +1.19 | +1.96 | 19.11 | 7.20 |
| 33 | Hot Together | 0.19 | 0.27 | 0.31 | +0.352 | +0.139 | +6.24 | +2.02 | +3.85 | 43.07 | 5.12 |
| 35 | Whip It Good | 1.02 | 1.42 | 1.70 | +0.335 | +0.183 | +5.93 | +2.66 | +4.08 | 85.26 | 42.77 |
| 46 | Let’s Go Bowling | 0.75 | 1.09 | 1.26 | +0.377 | +0.147 | +6.68 | +2.13 | +4.11 | 81.82 | 20.75 |
| 50 | The Truth Is Out There | 0.44 | 0.64 | 0.72 | +0.377 | +0.119 | +6.67 | +1.72 | +3.88 | 64.78 | 7.70 |

Story reading of that line. Chapter 1's two slopes are +6.43 and +1.25 logit per `x` (ols +3.51, R² 0.85). Pushed to 26 Nov 00:00Z the three-point line is about 95% and the later slope alone is about 45%, against 11.98% at the last read. Chapter 2: slopes +8.42 and +2.54 (ols +5.10, R² 0.90), line about 96% versus later-slope about 39%, against 1.71% now. Breakfast Run follows Chapter 2 (about 95% vs 38%, now 4.26%). Fishing is slower (slopes +3.77 and +0.69, line about 74% vs later-slope about 29%, now 13.30%). Chapter 3's only movement is one tick, 0.02 to 0.03, on the first step; the later slope is 0, so `ext2` stays 0.03 while `ext3` (2.6%) still smears that single tick across the week. Chapter 4 and the final mission do not move, and the line leaves them at 0.02%. The platinum and 100% completion print 0.00, 0.00, 0.01, which is zero on the clamped logit, so the line stays at 0.01. Gone Fishing stays 100%.

Launch-night rates sit on the other side of the dilution break the rules describe (every rate except the 100% one fell when the count went from 638 to 3,868). Fitting one line from L through B would mix that break with the public rise. On the points we do have, Chapter 1 has already gone from 1.25% at launch to 11.98%, Chapter 2 from 1.10% to 1.71%, and Chapter 3–4 and the final mission from 1.10% down to 0.02–0.03%, where a handful of pre-release earners are now a rounding grain inside a much larger player count (0.02% of 44,161 is about 9 people).

Implied earners if the printed percent were `round(100 * n / players, 2)`, using the band the 2-decimal rounding allows. Chapter 1: about 2,883, then 4,687, then 5,291. Chapter 2: about 325, then 608, then 755. Fishing: about 3,814, then 5,389, then 5,873. Players rose 22.4% from A to B while those earner counts rose about 84%, 132%, and 54%. Completion is outrunning dilution on the early trophies. For a printed 0.02% the rounding band is several people wide, so a flat 0.02% does not pin whether the earner count rose.

## What this does and does not support

The public evidence supports a launch curve that is still steep for the opener and the first activities, and flat for the end of the story. Chapter 1 and the earliest side activities (fishing, Breakfast Run, bowling, finding vehicles) are the trophies whose rates are rising in spite of a growing denominator. Chapter 2 is rising too, an order of magnitude lower. From Chapter 3 onward the main story is still on the floor. A structural split between early-game drift and a near-zero endgame matches these three refreshes. A single log-time slope for every trophy does not: the fast slopes are already smaller on the second refresh, and the floor trophies only twitch by one printed tick.

The extrapolation gap is the practical limit of this sample. Three refreshes cover 4.8 hours, two of them content steps, and the forecast horizon past B is about 128 hours. Using the house curve's `x` over that gap multiplies a slope that we have already seen change by a factor of about five. Any week-ahead number taken from these slopes needs a much wider band than the residual of a three-point line, and the floor trophies need a heavy tail for a jump the 0.01 grid cannot show yet.

