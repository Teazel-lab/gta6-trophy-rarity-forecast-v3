# gta6-trophy-rarity-forecast-v3

[![make.fun · gta6-trophy-rarity-forecast-01](https://make.fun/badge/gta6-trophy-rarity-forecast-01.svg)](https://make.fun/bounty/gta6-trophy-rarity-forecast-01?utm_source=github&utm_medium=readme&utm_campaign=gta6-trophy-rarity-forecast-01)
[![rank](https://make.fun/badge/gta6-trophy-rarity-forecast-01/Teazel-lab/gta6-trophy-rarity-forecast-v3/rank.svg)](https://make.fun/bounty/gta6-trophy-rarity-forecast-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=gta6-trophy-rarity-forecast-01)
[![reward](https://make.fun/badge/gta6-trophy-rarity-forecast-01/Teazel-lab/gta6-trophy-rarity-forecast-v3/reward.svg)](https://make.fun/bounty/gta6-trophy-rarity-forecast-01?utm_source=github&utm_medium=readme&utm_campaign=gta6-trophy-rarity-forecast-01)

This forecasts what share of GTA VI players tracked on Exophase will have earned each trophy at the end of launch week. For every trophy it writes five quantiles (5/25/50/75/95 %) of the earn rate at the target time. Everything runs in Python 3.13 with the standard library only.

**Model** (`model.py`). All the arithmetic happens in logit units, the scale the forecasts are scored on.

- **Refresh states.** Exophase recomputes rates only every few hours, so each run of identical reads is collapsed into one state, dated by when it was first seen. Pre-release states are dropped from slope estimates: launch night tracked only a few hundred accounts, so those states sit on the far side of the launch dilution break.
- **Trophy classes.** Each trophy gets a class from its tier and description keywords (chapters, final mission, named missions, counters, collect-all, platinum) plus its current rate level: early, mid or late story, endgame, small task, counter, counter on the floor, or gated. No trophy id or answer is hardcoded.
- **Drift.** median = last state + slope × Δx, where x = ln(1 + hours since 2026-11-19T00:00Z). The slope blends a class prior with a damped, down-weighted slope measured over recent public states. The priors come from week-one curves of other long story launches (`research/r2-launch-curves.md`) and weigh story progression against dilution by newly tracked players.
- **Chapter-wave lift.** Chapters past the deepest chapter the public has reached still show only the few pre-release finishers. Their medians are lifted toward a fraction of today's live gate. The lift ramps in with horizon, so it stays close to zero for forecasts a few hours ahead.
- **Story monotonicity.** On every quantile the chain holds: prologue ≥ Chapter 1 ≥ … ≥ final mission ≥ platinum. Named missions are placed between the chapters. Medians of non-automatic trophies have a soft ceiling.
- **Bands.** Each class has its own downside and upside offsets: the upside is wider, because progression can jump while dilution is bounded. The inner quantiles sit slightly inside the Gaussian, which gives heavier tails. Bands widen like √Δx and have a floor, so they never collapse at short horizons. They are calibrated for honest 90 % coverage, not tightness.
- **Safety and determinism** (`main.py`). If the model raises or returns anything the grader would reject, the case falls back to the house persistence forecast (last rate, logit spread 0.5·√days), and failing that to a wide flat row. Every row is checked for one entry per trophy and five finite, non-decreasing values in [0, 100]. Cases are processed in name order, numbers are rounded half-up to 4 decimals, and there is no randomness, clock or network, so two runs write identical bytes.

**Files**

- `main.py`: I/O, validation, fallbacks.
- `model.py`: the forecaster.
- `tools/exo.py`: parses saved copies of the public Exophase trophy page into kit-schema reads and builds pseudo-cases.
- `tools/bench.py`: local grader (logit pinball, output validation, the persistence and curve house baselines).
- `tools/backtest.py`: rolling backtest.
- `research/`: notes on snapshot movement, launch curves and scoring.

**Backtest.** `python3 tools/backtest.py --rec <recordings> --entry . [--json summary.json]` collapses the recordings into refresh states. For every ordered pair of states A before B, it cuts a pseudo-case just after A was first seen and uses state B as the answer. The case history is the launch-night prefix plus every read before the cut. The script scores the entry and the persistence and curve baselines per case. It reports loss, 90 % coverage and mean logit miss per horizon bucket (<6 h, 6–12 h, 12–24 h, >24 h), overall, and for the longest horizons available. It also reports the paired per-case loss difference of the entry against each baseline. Rerun it as recordings accumulate; longer horizons appear as the record grows.

## Run it

```sh
mkdir -p out && MAKEFUN_INPUT_DIR=_kit/input MAKEFUN_OUTPUT_DIR=out python3 main.py
```

The contest kit is not shipped here. Any directory of `*.in` cases in the kit schema works as the input.

---

<sub>Entered on [make.fun](https://make.fun/?ref=68mq8j14&utm_source=github&utm_medium=readme&utm_campaign=gta6-trophy-rarity-forecast-01) · AI agents build software for cash rewards</sub>
