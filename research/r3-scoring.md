# R3 — scoring, house baselines, what beats them

Cut used below: last recording `page-20261120T174029Z` (2026-11-20T17:40:29Z), target 2026-11-26T00:00Z. Horizon 7,579.5 min = 5.264 days. Random-walk scale `0.5*sqrt(d) = 1.147` logit. Official f00 horizon is shorter (6,510 min, scale `1.063`); medians below do not depend on that, spreads do. These `_rec` files are our pages, not the house tape. Launch-night rows are from `p01` (8 identical reads, 638 players, through 03:00Z Nov 19).

There is no trophy named Chapter 5. Story rows are prologue id 2, Chapter 1–4 ids 3–6, final mission id 7 (gold), platinum id 1.

## Design checklist

1. Prize bar is the best of three house losses on f00 only. Practice ~1.51 is the launch-night refresh against a 90-minute band. Do not fit p00/p01.
2. Score is the mean of 275 pinball items (55 trophies × 5 levels), 6 decimals. One trophy whose five quantiles are each off by L on average moves the contest loss by L/55. A 4-logit median miss on Chapter 1 is worth ~0.08. Parking the prologue on a point mass, if it stays at 100, is worth ~0.002.
3. Validity first: one `trophies` key, one row per case trophy, exact `{id,q}` with five finite non-decreasing numbers in [0,100], ≤ 65,536 bytes, under 8 s, identical bytes on the two graded runs. An invalid case is rescored as “every quantile = last rate” and the entry is below every valid entry and wins nothing.
4. Start from persistence. Add drift only on trophies whose earners are actually climbing (Chapter 1–2 and the other clear risers). A logit-vs-`ln(1+hours)` line through one refresh jump is the curve baseline, and it is the forecast to beat, not the forecast to copy.
5. Keep Chapter order: prologue ≥ Ch1 ≥ Ch2 ≥ Ch3 ≥ Ch4 ≥ final mission ≥ platinum. The curve’s medians (91, 90, 1.5, 0.02, 0.02) almost tie Ch1 with Ch2.
6. Flat printed rates stay flat under the curve (rmse 0). One printed uptick does not. Treat 0.01/0.02/0.03 moves as quantization until several refreshes agree. Spend the wide tail on the upside; `q ≤ 0.01` scores the same as 0.01.
7. Symmetric Gaussian `s` is what both numerical baselines and the house AI emit. Floor trophies and the prologue are atoms. A right tail with the median left on the atom beats a wide symmetric band when most of the mass does not jump.
8. Calibrate the 90% band on backtests at a long horizon. Two refreshes, five hours apart, do not identify a 5-day slope. Widen past `z=1.645` only where a jump mixture is plausible (story end is reachable in 168 h; platinum at ~200 h is not). The loss surface punishes a too-narrow Gaussian harder than a mildly wide one, and punishes a 2× Gaussian harder than a coverage miss on a handful of trophies.
9. The house AI is frozen at 2026-11-21T09:30Z and replayed onto f00. Our program sees reads through 11:30Z. Beat it with skew, clamp-aware atoms, monotone story rates, and those extra reads. Assume its forecast is valid.
10. Determinism: no clock, no RNG, no network; sorted files; fixed rounding; stdlib only.

## What the final scores

- Answer: first valid house read with slot in `[2026-11-26T00:00Z, 01:00Z)` that still lists every f00 trophy. Recorder is every 10 min through 01:10Z. No such read → final not graded, no prize. The page shows Exophase’s last refresh, so the answer can be hours older than the slot.
- f00 checkpoint 2026-11-21T11:30Z, target +6,510 min. History = every valid house read before `at`, oldest first. First recorder: every 30 min from 2026-11-18T23:50Z. Final recorder: every 10 min. Up to 3 tries; valid only if the page parses whole (names, rates, players tracked, count matches Total Trophies).
- Trophy `id` is position in Exophase’s list (1 = platinum “Vice Got a Price!”). The case lists whatever the last read lists (55 at open: 1 platinum, 2 gold, 6 silver, 46 bronze). `rates[i]` lines up with that list; null if that read lacked the trophy. An insert ahead of the end renumbers positions. Extra trophies after the cutoff are not rows in f00. The answering read has to contain each f00 trophy.
- Clamp before every logit, for `y` and for `q`: `[0.01, 99.99]`. Printed 0.00 and 0.01 are the same scored point. Printed 100 and 99.99 are the same scored point. `logit(0.01) = -ln(9999) = -9.21024`.
- Item loss `2 * max(τ d, (τ-1) d)` with `d = logit(y) - logit(q)`. If `q < y`, pay `2τ|d|`; if `q > y`, pay `2(1-τ)|d|`. A point forecast (five equal quantiles) scores mean absolute logit error. Rank is this mean to 6 decimals. Exact ties: lower mean wall time over the two runs (integer ms), then earlier receipt. Coverage and typical miss do not rank.
- Run cap: 8 s, 1 CPU, 1024 MB, 64 processes, no network, stdlib only. Two runs must match byte for byte or the entry is scored from the first run and not ranked.

## Persistence at this cut

Median = last printed rate (100 stays 100 in the input; the logit uses 99.99). Quantiles use `z ∈ {-1.645,-0.674,0,0.674,1.645}` and half-up 4 d.p., same program as `starter/main.py`. Checked against the rules’ worked row: last rate 1.10% at the official horizon is `[0.1931, 0.5403, 1.1, 2.2264, 6.0088]`.

| id | trophy | launch 638 | 11:10Z | last | persist q05, q50, q95 (this cut) | same median, official 6,510 min q95 |
|---|---|---:|---:|---:|---|---:|
| 2 | prologue, Gone Fishing | 100 | 100 | 100 | 99.934, 99.99, 99.9985 | 99.9983 |
| 3 | Chapter 1 | 1.25 | 7.99 | 11.98 | 2.02, 11.98, 47.32 | 43.89 |
| 4 | Chapter 2 | 1.10 | 0.90 | 1.71 | 0.263, 1.71, 10.30 | 9.09 |
| 5 | Chapter 3 | 1.10 | 0.02 | 0.03 | 0.0045, 0.03, 0.198 | 0.172 |
| 6 | Chapter 4 | 1.10 | 0.02 | 0.02 | 0.0030, 0.02, 0.132 | 0.115 |
| 7 | final mission | 1.10 | 0.02 | 0.02 | 0.0030, 0.02, 0.132 | 0.115 |
| 1 | platinum | 0.63 | 0.00 | 0.01 | 0.0015, 0.01, 0.066 | 0.058 |

Launch-night 1.10% on Ch2–final is 7 of 638 pre-release accounts. The public refresh (rules: 3,868 players by 04:30Z, every rate except 100% down) diluted them to the floor. They have not come back. Persistence is the right median on Ch4, the final mission, and platinum until a later refresh moves them, and the wrong median if Chapter 1 keeps climbing: its 95% quantile still ends near 44–47%.

Players 36,080 → 44,161 and trophies earned 45,648 → 60,923 between 11:10Z and 15:59Z. Chapter 1 earners ~2,883 → ~5,291. Chapter 2 ~325 → ~755. Chapter 3 ~7 → ~13. Rates rose while the denominator grew 22%. Over this afternoon, progression outran inflow. The dilution that knocked launch-night rates down is a different regime, and it sits outside the curve’s 24 h window (below).

## Curve baseline at this cut

Rule text: for each trophy, OLS of `logit(rate)` on `ln(1 + hours since 2026-11-19T00:00Z)` over reads in the last 24 h; evaluate the line at the target; spread is “the random walk’s above and the fit’s residual combined”; under 3 reads, copy persistence. The `+` versus quadrature is not specified. On these data the residual rmse is 0 to 0.058 logit, against a random-walk term of 1.147, so the two readings differ by ≤ 0.06 logit. Medians do not depend on it. Bands below use `s = 1.147 + rmse`.

`x` at the cut is 3.754; at the target, `ln(169) = 5.130`; the line is extrapolated `Δx = 1.376` past the last point. The two refreshes themselves are only `Δx ≈ 0.14` apart. The fit is identified on a window about one tenth of the distance it is then asked to cover.

Last-24 h window starts 2026-11-19T17:40Z. The newest `p01` read is 38.7 h before the cut, so all 8 identical launch-night rows are outside it. The 04:30Z public refresh is outside it too. The curve, cut now, never sees the dilution crash. It sees only the post-launch rise.

Reads we can actually put in that window: 10 pages, two refreshes. Six copies at 36,080 players (11:10–12:03Z), four at 44,161 (15:59–17:40Z). OLS weights each copy equally. A refresh that sits on the page longer pulls the intercept toward itself. Inside a copy-run the rate is constant while `x` still increases, which adds a negative within-plateau covariance and flattens the slope versus a two-point line through the refresh centroids. With only ~1 h of copies on each side of a 4 h gap, that flatten is small (Chapter 1 slope 3.13 vs 3.22; median 91.2 vs 92.3).

If the house’s 10-minute tape held the same two pages from 11:10 to 15:50 (29 reads) and 16:00 to 17:40 (11 reads), Chapter 1’s OLS median moves from 91.2 to 90.4, Chapter 2 from 90.2 to 88.9, Chapter 3 from 1.48 to 1.36, and a 0.01→0.02 tick from 13.9 to 12.2. Still the same failure. We do not have the house’s true last 24 h (nothing before 11:10Z, and our own gap 12:03–15:59Z).

| id | last | curve median | curve q05–q95 (`s = rw+rmse`) | persist median |
|---|---:|---:|---|---:|
| 2 prologue | 100 | 99.99 (scores as 100) | 99.934 – 99.9985 | 100 |
| 3 Ch1 | 11.98 | 91.23 | 59.7 – 98.6 | 11.98 |
| 4 Ch2 | 1.71 | 90.22 | 56.1 – 98.5 | 1.71 |
| 5 Ch3 | 0.03 | 1.48 | 0.215 – 9.49 | 0.03 |
| 6 Ch4 | 0.02 | 0.02 | 0.003 – 0.132 | 0.02 |
| 7 final | 0.02 | 0.02 | 0.003 – 0.132 | 0.02 |
| 1 platinum | 0.01 | 0.01 | 0.0015 – 0.066 | 0.01 |

26 trophies printed the same rate on both refreshes (slope 0, curve = persistence). 29 rose, 0 fell. Of the 34 trophies now ≤ 0.02:

- unchanged, or 0.00→0.01 (8 trophies; both clamp to 0.01): curve median stays on the floor
- 0.02→0.03 (Chapter 3 and two others): median 1.48
- 0.01→0.02 (one trophy): median 13.9
- 0.02→0.04 (two trophies): median 24.4

Other risers the same line sends far above the last print: Trust 4.26→89, fishing 13.30→66, “Whip It Good” 1.70→72. Mean |logit(curve median) − logit(last)| across all 55 is 1.59; the median trophy is 0 (the flats). The contest loss is the mean, so the flats are 26 free ties with persistence and the extrapolated third is where the curve either wins big or loses big.

Where persistence is the weak one: Chapter 1 at 12% with a 95% cap near 45%, while earners nearly doubled in five hours and the story’s first chapter fits in a weekend (50–80 h for the whole story, ~168 h on the clock by the target). Chapter 2’s 95% cap near 9–10% has the same shape, one chapter behind. Where the curve is the weak one: Chapter 1–2 medians near 90%, any one-tick floor trophy, and a Chapter 2 median that has caught Chapter 1. Where they agree, and a play-time prior disagrees: Chapter 4, the final mission, and anything else stuck at 0.02. A 50–80 h story is finishable by 26 Nov for players putting in long days; both baselines put the 95% quantile at 0.13% (about 60 people if the denominator stayed 44k). Platinum at ~200 h is longer than the 168 h from 19 Nov 00:00Z to the target, and both baselines leaving it at 0.01 with a 95% quantile near 0.06% is the sensible one. The prologue has been 100% at 638, 36k, and 44k players.

## Pinball, width, clamp

Expected mean item loss when the truth is Gaussian on the logit scale with scale `σ` and the forecast is the same center with scale `s` (house `z`, the factor of 2 included):

| s/σ | 0.25 | 0.50 | 0.75 | 1 | 1.25 | 1.50 | 2 | 4 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| E[loss]/σ | 0.647 | 0.555 | 0.509 | 0.496 | 0.505 | 0.528 | 0.594 | 0.963 |

Minimum at `s = σ`. At a fixed ratio, too narrow costs more than too wide (0.50× is +0.058σ, 1.50× is +0.031σ). 2× costs +0.097σ. On a truth with `σ ≈ 1.15`, doubling every band costs about 0.11 on the contest loss. One outer quantile short by D logits costs `1.9 D / 275 ≈ 0.0069 D`. Ten trophies each missing the 95% quantile by 1 logit cost ~0.07. So: hit the real width, and add tail mass for jumps. A uniformly doubled Gaussian gives away more than a few coverage misses.

Outer asymmetry is why the narrow band hurts. `q95` too low pays `1.90` per logit; `q95` too high pays `0.10`. Same numbers, swapped, for `q05`. The median pays `1.0` either way. `q25` pays `0.50` if it is low and `1.50` if it is high.

Clamp arithmetic, point forecast, mean of the five items:

- `y=0.02`, `q=0.01`: 0.693 (one tick is `ln(2)` on the logit)
- `y=0.02`, `q=1`: 3.92
- `y=0.01`, `q=0.02`: 0.693
- `y=100`, `q=99.9`: 2.30 (`logit(99.99)−logit(99.9) = 2.303`)

Any `q ≤ 0.01` scores as 0.01. Any `q ≥ 99.99` scores as 99.99. Lowering `q05` from 0.01 to 0 does not change a single item. At the official final spread, persistence’s `q05` is already ≤ 0.01 for 40 of 55 trophies: that quantile is free on a floor outcome and does not insure the upside. The upside from 0.02 to the persistence `q95` of 0.13 is only +1.87 logit. A finishable story trophy that lands at 1% is 3.92 logit above 0.02, and `q95` pays `1.90 × (3.92 − 1.87)`.

Prologue, this cut’s persistence band, if the page still prints 100: mean item loss 0.115, all of it from `q05=99.934` and `q25=99.978`, which sit below the clamp. A point mass at 100 scores 0. If the page prints 99.9 instead, the point mass scores 2.30 and persistence scores 1.35. Break-even versus persistence is about an 11% chance of a 99.9-class dip (and a 89% chance of staying at the clamp). The gain if it stays is 0.002 on the contest loss; the extra damage if it dips to 99.9 is ~0.017. Four observations at 100, through a 69× increase in players tracked, are the evidence for the atom. The band has to be one-sided below 99.99 to be worth writing; the upper three quantiles at 100 are free insurance that pays the cheap `2(1−τ)` side if the rate ever falls.

Realized loss when the median is exactly right and `s = 1.147`, interior rate: about 0.23 on that trophy’s five-mean (the random-walk tax). At 0.01 the lower half of the band clamps away and the tax falls to ~0.12. Chapter 1, if the truth stayed 11.98: persistence ~0.23, curve band ~3.50 (point forecast at 91 would be 4.34). Chapter 2: persistence ~0.23, curve band ~5.44. Those two trophies alone are ~0.15 of contest loss if the curve’s medians are the ones that miss. If Chapter 1 instead lands near 40%, persistence’s median is short by 1.59 logit and its `q95` (47) still covers, while the curve’s entire 60–99 band is above the outcome. The winning row is a median between them and a 90% band that reaches both.

## House AI

One recorded call at 2026-11-21T09:30Z (retry only if the first answer is not a valid forecast), superbot at max reasoning, 64k output tokens. It receives the rules, the format, and every read held at 09:30Z. It returns a median `m` and one logit spread `s` per trophy. Grading replays `q_τ = invlogit(logit(m) + z_τ s)` with no new call, on f00, whose history continues to 11:30Z.

What that interface pushes it toward: a symmetric Gaussian per trophy; medians that lean on the same last-24 h logit line the rules spell out, because that line is in the prompt; spreads that are round and often too tight, because the page sits still between refreshes and the model is told the practice band was simply too narrow for a 90-minute refresh. 55 pairs of numbers fit easily in 64k, so a format failure is unlikely. It can respect chapter order if it notices, and it can ignore duplicate reads if it notices. It cannot emit an atom plus a right tail, and it cannot revise `m` after a refresh in the last two hours.

A structural forecast beats that replay where any of these is true: the last reads before 11:30Z move a riser; a floor trophy’s honest distribution is “stay, with a small chance of a jump” so `q50` stays at the atom and only `q95` travels; the prologue stays at the clamp; Chapter 2 is still far below Chapter 1 on 26 Nov; the final mission is reachable inside 168 h while a `ln(1+h)` slope of 0 says 0.02. It does not beat the AI by quoting a larger single `s` on the AI’s own median.
