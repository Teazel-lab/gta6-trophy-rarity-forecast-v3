"""Structural launch-curve forecaster for Exophase trophy earn rates (standard library only, deterministic).

Everything is done in logit units on the scoring scale (rates clamped to 0.01..99.99 percent).

  median = last refreshed rate + slope * dx,   dx = ln(1 + h_target) - ln(1 + h_last_state)

h is hours since 2026-11-19T00:00Z and "state" is one Exophase refresh (a run of identical reads). The slope is a class
prior (how launch curves of long story games behave in week one) blended with a damped, down-weighted measured slope.
Story trophies still on the pre-release floor get a "wave" level derived from the deepest chapter the public has
reached. Quantiles are skewed around the median (separate lower/upper scales per class) and widen like sqrt(dx).
No answers are keyed by trophy id: classes come from tier/description keywords plus the current rate level.
"""

import math
import re
from datetime import datetime, timezone

LEVELS = [0.05, 0.25, 0.5, 0.75, 0.95]
EPOCH = datetime(2026, 11, 19, tzinfo=timezone.utc)

# Reference dx at which the class bands below are quoted: the final's horizon (h ~58 -> 168).
DX_REF = 1.05
# Inner quantiles (25/75) sit at this fraction of the 5/95 offset: a little inside the Gaussian 0.41 = heavier tails.
INNER = 0.40

# class -> (prior slope in logit per ln-hour, 5% offset below the median, 95% offset above it, both at DX_REF).
# Slopes are the research priors; upside is wider than downside because progression (the weekend) can jump while
# dilution by new tracked players is bounded (~ -0.7 logit per doubling).
CLASSES = {
    "early": (1.0, 1.1, 1.4),     # first gate / first activities, already >= 5%
    "mid": (1.3, 1.2, 1.7),       # mid story, 0.3..5%
    "late": (1.4, 2.0, 2.6),      # story trophies still near the pre-release floor: thin tail, huge residual
    "endgame": (0.1, 1.0, 2.0),   # platinum, 100%, collect-all / huge counters: stays on the floor, long right tail
    "small": (0.8, 1.2, 1.7),     # small optional task that the public is already earning
    "counter": (0.7, 1.2, 1.6),   # medium counter that is already moving
    "cfloor": (0.6, 1.5, 2.4),    # counter still on the floor
    "gated": (1.3, 1.8, 2.7),     # optional task still on the floor: gated behind story the public has not reached
}

# Wave factors: a chapter j steps past the deepest "live" chapter is expected, by the target, near
# live_rate_now * WAVE[j-1] (today's finishers of the live gate reach the next gates, diluted by new players).
WAVE = [0.40, 0.08, 0.05, 0.03]
LIVE_RATE = 0.3          # percent: a chain trophy at or above this is being earned by the public
MEDIAN_CAP = 75.0        # soft ceiling for any non-automatic trophy's median (hunter-site ceilings are 70-90%)


def clamp(pct):
    return min(99.99, max(0.01, pct))


def logit(pct):
    c = clamp(pct)
    return math.log(c / (100 - c))


def inv(l):
    if l >= 0:
        return 100 / (1 + math.exp(-l))
    e = math.exp(l)
    return 100 * e / (1 + e)


def round4(x):
    """Half-up to 4 decimals, whole numbers as ints (same as the starter / JavaScript Math.round)."""
    scaled = x * 10000
    whole = math.floor(scaled)
    if scaled - whole >= 0.5:
        whole += 1
    value = whole / 10000
    return int(value) if value.is_integer() else value


def hours(iso):
    dt = datetime.fromisoformat(str(iso).replace("Z", "+00:00"))
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return (dt - EPOCH).total_seconds() / 3600


def lx(h):
    return math.log(1 + max(0.0, h))


def _num(v):
    return float(v) if isinstance(v, (int, float)) and not isinstance(v, bool) and math.isfinite(v) else None


def refresh_states(history, n):
    """Collapse runs of identical reads into states: {h (first seen), players, rates[n]}."""
    states = []
    for read in history:
        if not isinstance(read, dict):
            continue
        raw = read.get("rates")
        raw = raw if isinstance(raw, list) else []
        rates = [_num(raw[i]) if i < len(raw) else None for i in range(n)]
        if all(r is None for r in rates):
            continue
        if states:   # a read that lacks a trophy repeats its last print: no fake refresh from a null
            rates = [states[-1]["rates"][i] if r is None else r for i, r in enumerate(rates)]
        try:
            h = hours(read.get("at"))
        except (ValueError, TypeError):
            continue
        players = _num(read.get("players_tracked"))
        if states and states[-1]["players"] == players and states[-1]["rates"] == rates:
            continue
        states.append({"h": h, "players": players, "rates": rates})
    return states


def public_states(states):
    """Drop pre-release states (tracked players < 10% of the latest): they sit across the launch dilution break."""
    if not states:
        return states
    latest = states[-1]["players"] or 0
    kept = [s for s in states if (s["players"] or 0) >= 0.1 * latest]
    return kept if kept else states[-1:]


_CHAPTER = re.compile(r"\bchapter\s+(\d+)\b", re.I)
_NAMED = re.compile(r"^Complete [A-Z][^\d]*$")
_COUNT = re.compile(r"(\$?)(\d[\d,]*)")


def keyword_kind(trophy):
    """Kind from tier and text only: ('chapter', n) | ('final',) | ('mission',) | ('endgame',) | ('counter',) | ('other',)."""
    desc = str(trophy.get("description") or "")
    low = desc.lower()
    if str(trophy.get("tier") or "").lower() == "platinum" or "100%" in low or "all trophies" in low:
        return ("endgame",)
    m = _CHAPTER.search(low)
    if m and "complete" in low:
        return ("chapter", int(m.group(1)))
    if "final mission" in low:
        # "the final mission for <stranger>" is an optional strand finale, not the story's end.
        return ("other",) if " for " in low else ("final",)
    counts = [(c[0], int(c[1].replace(",", ""))) for c in _COUNT.findall(desc) if c[1].replace(",", "")]
    big = any(not money and v >= 50 for money, v in counts)
    if big or re.search(r"\b(all|every|each)\b", low):
        return ("endgame",)   # collect-all / huge counter (demoted to 'counter' below if the rate says it is easy)
    if counts:
        return ("counter",)
    if _NAMED.match(desc):
        return ("mission",)   # "Complete <Mission Title>." : a named story mission
    return ("other",)


def pick_class(kind, rate):
    """Model class from keyword kind + current level (percent)."""
    k = kind[0]
    if k in ("chapter", "final", "mission"):
        return "early" if rate >= 5 else "mid" if rate >= LIVE_RATE else "late"
    if k == "endgame":
        # A "collect 100" that many players already have is a medium counter, not endgame.
        return "endgame" if rate <= 0.1 else "counter"
    if k == "counter":
        return "cfloor" if rate <= 0.05 else "counter"
    return "early" if rate >= 5 else "small" if rate > 0.05 else "gated"


def measured_slope(pub, i, x_last):
    """(slope, weight): damped logit slope of trophy i over the recent public states, and how much to trust it.

    Two-point slope from the oldest public state within 0.6 ln-hours of the last one (a long baseline averages the
    refresh-to-refresh bursts). It is halved (launch slopes decay; Friday's fell ~5x between refreshes) and its weight
    grows with the baseline and with the earner count (few earners = 0.01-grid quantization, not signal).
    """
    pts = [(lx(s["h"]), s["rates"][i], s["players"]) for s in pub if s["rates"][i] is not None]
    pts = [p for p in pts if p[0] >= x_last - 0.6]
    if len(pts) < 2:
        return 0.0, 0.0
    (x0, r0, _), (x1, r1, n1) = pts[0], pts[-1]
    span = x1 - x0
    if span <= 1e-6:
        return 0.0, 0.0
    slope = max(-1.0, min(4.0, (logit(r1) - logit(r0)) / span)) * 0.5
    earners = min(r0, r1) / 100 * (n1 or 0)
    weight = min(0.5, span / (span + 0.5)) * earners / (earners + 30)
    return slope, weight


def forecast(case):
    trophies = case["trophies"]
    n = len(trophies)
    states = refresh_states(case.get("history") or [], n)
    if not states:
        raise ValueError("no usable read")
    pub = public_states(states)
    last = states[-1]
    try:
        h_target = hours(case["target"])
    except (KeyError, ValueError, TypeError):
        h_target = hours(case["at"]) + float(case["horizon_minutes"]) / 60
    x_last = lx(last["h"])
    dx = max(0.0, lx(h_target) - x_last)
    width = math.sqrt(max(dx, 0.06) / DX_REF)   # bands widen like sqrt(dx); never collapse at tiny horizons
    ramp = min(1.0, dx) ** 2                    # structural wave: a multi-day cohort effect, ~0 within hours

    # Latest known rate per trophy (a read may lack a trophy: fall back to older states, else 0 like the starter).
    rate = []
    for i in range(n):
        r = next((s["rates"][i] for s in reversed(states) if s["rates"][i] is not None), 0.0)
        rate.append(min(100.0, max(0.0, r)))

    kinds = [keyword_kind(t) for t in trophies]
    auto = [r >= 99.5 for r in rate]            # prologue / automatic: an atom at 100
    cls = [pick_class(kinds[i], rate[i]) for i in range(n)]
    cap = logit(MEDIAN_CAP)

    med = [0.0] * n
    for i in range(n):
        prior = CLASSES[cls[i]][0]
        slope, w = measured_slope(pub, i, x_last)
        med[i] = min(max(cap, logit(rate[i])), logit(rate[i]) + ((1 - w) * prior + w * slope) * dx)

    # Story chain in play order: chapters by number, then the final mission.
    chain = sorted((i for i in range(n) if kinds[i][0] == "chapter" and not auto[i]), key=lambda i: (kinds[i][1], i))
    chain += [i for i in range(n) if kinds[i][0] == "final" and not auto[i]]
    # Wave: chapters past the deepest live one are still printing the handful of pre-release finishers; by the target
    # the public cohort that holds the live gate today has moved on. Lift their medians toward that level.
    for pos, i in enumerate(chain):
        wave = 0.0
        for back in range(1, min(pos, len(WAVE)) + 1):
            j = chain[pos - back]
            if rate[j] >= LIVE_RATE:
                wave = max(wave, rate[j] * WAVE[back - 1])
        if wave > 0 and logit(wave) > med[i]:
            med[i] += ramp * (logit(wave) - med[i])
    for a, b in zip(chain, chain[1:]):          # later gates cannot outrun earlier ones
        med[b] = min(med[b], med[a])

    # Named story missions: place each between the chapters by its current rate and average that with its own drift.
    anchors = sorted((logit(rate[i]), med[i]) for i in chain)
    if anchors:
        for i in range(n):
            if kinds[i][0] != "mission" or auto[i]:
                continue
            c = logit(rate[i])
            if c > anchors[-1][0]:
                continue                         # ahead of the first chapter: its own early-gate drift stands
            tied = [m for a, m in anchors if abs(a - c) < 1e-9]
            if tied:
                interp = sum(tied) / len(tied)
            elif c < anchors[0][0]:
                interp = anchors[0][1]
            else:
                lo = max(p for p in anchors if p[0] < c)
                hi = min(p for p in anchors if p[0] > c)
                interp = lo[1] + (hi[1] - lo[1]) * (c - lo[0]) / (hi[0] - lo[0])
            med[i] = 0.5 * (med[i] + interp)

    rows = []
    for i in range(n):
        if auto[i]:
            # Stays at 100 unless a few new accounts are tracked before finishing the opener: q05 a hair below.
            q = [min(rate[i], 99.97), 100.0, 100.0, 100.0, 100.0] if rate[i] >= 99.995 else None
            if q is None:
                l = logit(rate[i])
                q = [inv(l - 1.0 * width), inv(l - 0.3 * width), rate[i], inv(l + 0.5 * width), 100.0]
        else:
            _, lo, hi = CLASSES[cls[i]]
            m = med[i]
            q = [inv(m - lo * width), inv(m - lo * width * INNER), inv(m), inv(m + hi * width * INNER),
                 inv(m + hi * width)]
        rows.append(q)

    # Chain structure on every quantile: prologue >= Ch1 >= ... >= final mission >= platinum.
    top = [i for i in range(n) if auto[i]]
    plat = [i for i in range(n) if str(trophies[i].get("tier") or "").lower() == "platinum" and not auto[i]]
    order = chain + plat[:1]
    for a, b in zip(order, order[1:]):
        rows[b] = [min(x, y) for x, y in zip(rows[b], rows[a])]
    if top:
        ceiling = rows[top[0]]
        for i in order:
            rows[i] = [min(x, y) for x, y in zip(rows[i], ceiling)]

    out = []
    for i in range(n):
        q, prev = [], 0.0
        for v in rows[i]:
            v = min(100.0, max(prev, 0.0, v))    # finite, in range, non-decreasing
            q.append(round4(v))
            prev = v
        out.append({"id": int(trophies[i]["id"]), "q": q})
    out.sort(key=lambda r: r["id"])
    return {"trophies": out}
