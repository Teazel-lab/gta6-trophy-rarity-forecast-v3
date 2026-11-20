#!/usr/bin/env python3
"""Rolling pseudo-checkpoint backtest on our Exophase recordings (stdlib only, deterministic).

python3 tools/backtest.py --rec _rec [--entry <dir> ...] [--builtin persistence curve] [--json <file>]
                          [--prefix _kit/input/p01.in]

1. tools/exo.py load_reads -> every recording that parses whole; runs of identical reads (same players tracked,
   trophies earned, rates and trophy list) collapse into one refresh STATE, dated by when it was first seen.
2. For every ordered pair of states A < B: a pseudo-case cut 1 s after A was first seen (history = the kit's
   launch-night prefix + every read before the cut, so the checkpoint has just seen A), target = B's first-seen time,
   answer = state B. That is exactly the final's situation: forecast the next refresh(es) from the latest one.
3. Every entry (run as the grader does, via tools/bench.py run_entry) and the builtins (bench.py persistence/curve)
   are scored with bench.py's pinball (logit scale). Each case's loss is the mean over its trophy x level items and
   every case weighs the same, like the single final case.

Report per horizon bucket (<6 h, 6-12 h, 12-24 h, >24 h), overall, and 'longest' (cases whose horizon is at least
90% of the longest available): n, mean loss, 90% coverage, typical miss = mean |logit(answer) - logit(q50)| over trophies
(the median is uninformative: most trophies do not move between refreshes);
then each entry minus each builtin, paired per case (mean difference, cases won = strictly lower loss).
Rerun after new recordings: the pairs are rebuilt from whatever _rec holds.
"""

import argparse
import json
import sys
import tempfile
from datetime import timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import bench  # noqa: E402
import exo  # noqa: E402

BUCKETS = [("<6h", 0, 6), ("6-12h", 6, 12), ("12-24h", 12, 24), (">24h", 24, float("inf"))]
LONGEST_FRACTION = 0.9


def states(reads):
    """Distinct refresh states, oldest first: {"first": iso of the first read, "read": that read, "reads": count}."""
    out = []
    for r in reads:
        key = (r["players_tracked"], r["trophies_earned"], tuple(r["rates"]), tuple(r["_names"]))
        if out and out[-1]["key"] == key:
            out[-1]["reads"] += 1
            continue
        out.append({"key": key, "first": r["at"], "read": r, "reads": 1})
    return out


def score_case(case, q, ans):
    """(mean pinball over items, coverage of the 5-95 band, list of |logit miss| of the median)."""
    loss, items, cover, miss = 0.0, 0, 0, []
    for t in case["trophies"]:
        y = ans.get(str(t["id"]))
        if y is None:
            continue
        qs = q[t["id"]]
        for tau, v in zip(bench.LEVELS, qs):
            loss += bench.pinball(y, v, tau)
            items += 1
        cover += qs[0] <= y <= qs[4]
        miss.append(abs(bench.logit(y) - bench.logit(qs[2])))
    n = len(miss)
    return (loss / items if items else None), (cover / n if n else None), miss


def mean(xs):
    return sum(xs) / len(xs) if xs else None


def r6(x):
    return None if x is None else round(x, 6)


def summarize(rows, names):
    """rows: per-case dicts -> {name: {n, loss, cov90, miss}} plus paired differences."""
    out = {"n": len(rows), "models": {}, "paired": {}}
    for n in names:
        cells = [r["models"][n] for r in rows]
        out["models"][n] = {
            "loss": r6(sum(c["loss"] for c in cells) / len(cells)) if cells else None,
            "cov90": r6(sum(c["cov90"] for c in cells) / len(cells)) if cells else None,
            "miss": r6(mean([m for c in cells for m in c["miss"]])),
            "invalid": sum(not c["valid"] for c in cells),
        }
    for e in names:
        if e.startswith("builtin:"):
            continue
        for b in names:
            if not b.startswith("builtin:"):
                continue
            d = [r["models"][e]["loss"] - r["models"][b]["loss"] for r in rows]
            out["paired"][f"{e} vs {b}"] = {
                "mean_diff": r6(sum(d) / len(d)) if d else None,
                "wins": sum(x < 0 for x in d),
                "n": len(d),
            }
    return out


def fmt(x, spec):
    return "-" if x is None else format(x, spec)


def print_group(label, s, names):
    if not s["n"]:
        print(f"{label:<9} n 0")
        return
    for k, n in enumerate(names):
        m = s["models"][n]
        head = f"{label:<9} n {s['n']:>3}" if k == 0 else " " * 15
        bad = f"  INVALID {m['invalid']}" if m["invalid"] else ""
        print(f"{head}  {n:<24} loss {fmt(m['loss'], '.4f')}  cov90 {fmt(m['cov90'], '.3f')}  "
              f"miss {fmt(m['miss'], '.3f')}{bad}")
    for pair, p in s["paired"].items():
        print(f"{'':15}  {pair:<44} diff {fmt(p['mean_diff'], '+.4f')}  wins {p['wins']}/{p['n']}")


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--rec", default="_rec")
    ap.add_argument("--entry", action="append", default=[], help="entry directory holding main.py (repeatable)")
    ap.add_argument("--builtin", nargs="*", default=sorted(bench.BUILTINS), choices=sorted(bench.BUILTINS))
    ap.add_argument("--prefix", default="_kit/input/p01.in", help="kit case whose launch-night reads are prepended")
    ap.add_argument("--json", help="write the summary here")
    ap.add_argument("--per-case", action="store_true", help="also print one line per case")
    a = ap.parse_args()

    reads, trophies = exo.load_reads(a.rec)
    st = states(reads)
    prefix = None
    if Path(a.prefix).is_file():
        prefix = json.loads(Path(a.prefix).read_text(encoding="utf-8"))
    else:
        print(f"backtest: no prefix {a.prefix}, cases start at our first recording", file=sys.stderr)
    names = [f"builtin:{b}" for b in a.builtin] + list(a.entry)
    print(f"{len(reads)} reads -> {len(st)} refresh states: "
          + ", ".join(f"{s['first'][5:16]}Z x{s['reads']}" for s in st))

    rows = []
    with tempfile.TemporaryDirectory() as tmp:
        for i, sa in enumerate(st):
            for sb in st[i + 1:]:
                cut = exo.iso(exo.parse_iso(sa["first"]) + timedelta(seconds=1))
                case, ans = exo.make_case(reads, trophies, cut, sb["first"], prefix)
                if ans is None:
                    continue
                path = Path(tmp, case["id"] + ".in")
                path.write_text(json.dumps(case, separators=(",", ":")) + "\n", encoding="utf-8")
                row = {"id": case["id"], "at": case["at"], "target": case["target"],
                       "horizon_h": round(case["horizon_minutes"] / 60, 3), "models": {}}
                for n in names:
                    if n.startswith("builtin:"):
                        q, valid, note = bench.BUILTINS[n[8:]](case), True, None
                    else:
                        q, valid, note, _ = bench.run_entry(n, path, case)
                    loss, cov, miss = score_case(case, q, ans["rates"])
                    row["models"][n] = {"loss": loss, "cov90": cov, "miss": miss, "valid": valid, "note": note}
                rows.append(row)
    if not rows:
        sys.exit("backtest: fewer than two refresh states, nothing to score")
    rows.sort(key=lambda r: (r["horizon_h"], r["at"]))

    if a.per_case:
        for r in rows:
            cells = "  ".join(f"{n} {r['models'][n]['loss']:.4f}" for n in names)
            print(f"  {r['id']} {r['at'][5:16]}->{r['target'][5:16]} {r['horizon_h']:6.2f}h  {cells}")
            for n in names:
                if r["models"][n]["note"]:
                    print(f"    ! {n}: {r['models'][n]['note']}")

    longest = max(r["horizon_h"] for r in rows)
    groups = [(lab, [r for r in rows if lo <= r["horizon_h"] < hi]) for lab, lo, hi in BUCKETS]
    groups.append(("overall", rows))
    groups.append(("longest", [r for r in rows if r["horizon_h"] >= LONGEST_FRACTION * longest]))
    summary = {"states": len(st), "reads": len(reads), "longest_horizon_h": longest, "groups": {}}
    print(f"{len(rows)} pseudo-cases, horizons {rows[0]['horizon_h']:.2f}-{longest:.2f} h "
          f"(final: {6510 / 60:.1f} h); 'longest' = horizon >= {LONGEST_FRACTION:.0%} of the longest; "
          f"miss = mean |logit miss| of q50")
    for lab, rs in groups:
        s = summarize(rs, names)
        summary["groups"][lab] = s
        print_group(lab, s, names)
    if a.json:
        summary["cases"] = [{"id": r["id"], "at": r["at"], "target": r["target"], "horizon_h": r["horizon_h"],
                             "loss": {n: r6(r["models"][n]["loss"]) for n in names}} for r in rows]
        Path(a.json).write_text(json.dumps(summary, indent=1, sort_keys=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
