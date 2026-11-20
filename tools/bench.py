#!/usr/bin/env python3
"""Local grader for gta6-trophy-rarity-forecast-01 pseudo-cases (stdlib only).

python3 tools/bench.py --cases <dir> [--entry <entry_dir> ...] [--builtin persistence curve]

<dir> holds <id>.in cases and, where known, <id>.ans.json ({"rates": {"<trophy id>": rate}}), as tools/exo.py writes
them. Each entry runs as `python3 -P -s <entry_dir>/main.py`, one case per run, 8 s timeout, and its output is
validated as RULES.txt requires; an invalid case is scored as the last-read rates and flagged. Cases with no answer
are run and validated but not scored.

Builtins (the two house baselines, in-process):
  persistence  q = logistic(logit(last rate) + z * 0.5 * sqrt(days)), rounded to 4 dp.
  curve        per trophy, least squares of logit(rate) on ln(1 + hours since 2026-11-19T00:00Z) over the reads in
               the 24 h before the checkpoint, read at the target; spread = sqrt(rw^2 + resid^2), rw the
               persistence spread and resid the fit's residual standard error sqrt(SSR / (n - 2)); fewer than 3
               reads (or no spread in time) -> persistence. The house source is not in the kit: the window anchor,
               the quadrature and the n - 2 are OUR reading of the rules' one-sentence description.
"""

import argparse
import json
import math
import os
import subprocess
import sys
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path

LEVELS = [0.05, 0.25, 0.5, 0.75, 0.95]
Z = [-1.645, -0.674, 0, 0.674, 1.645]
SIGMA = 0.5
EPOCH = datetime(2026, 11, 19, tzinfo=timezone.utc)
TIMEOUT_S = 8
MAX_BYTES = 65536
TIERS = ["platinum", "gold", "silver", "bronze"]


def clamp(x):
    return min(99.99, max(0.01, x))


def logit(pct):
    c = clamp(pct)
    return math.log(c / (100 - c))


def inv(l):
    return 100 / (1 + math.exp(-l))


def round4(x):
    return math.floor(x * 10000 + 0.5) / 10000


def pinball(y, q, tau):
    d = logit(y) - logit(q)
    return 2 * max(tau * d, (tau - 1) * d)


def parse_iso(s):
    return datetime.fromisoformat(s.replace("Z", "+00:00")).astimezone(timezone.utc)


# ---------- the two house baselines ----------

def persistence(case):
    last = case["history"][-1]["rates"]
    s = SIGMA * math.sqrt(case["horizon_minutes"] / 1440)
    return {t["id"]: [round4(inv(logit(last[i] if last[i] is not None else 0) + z * s)) for z in Z]
            for i, t in enumerate(case["trophies"])}


def curve(case):
    out = persistence(case)
    at = parse_iso(case["at"])
    rw = SIGMA * math.sqrt(case["horizon_minutes"] / 1440)

    def x_of(dt):
        return math.log(max(1e-9, 1 + (dt - EPOCH).total_seconds() / 3600))

    window = [(x_of(parse_iso(r["at"])), r["rates"]) for r in case["history"]
              if (at - parse_iso(r["at"])).total_seconds() <= 86400]
    xt = x_of(parse_iso(case["target"]))
    for i, t in enumerate(case["trophies"]):
        pts = [(x, logit(r[i])) for x, r in window if i < len(r) and r[i] is not None]
        n = len(pts)
        if n < 3:
            continue
        mx = sum(x for x, _ in pts) / n
        my = sum(y for _, y in pts) / n
        sxx = sum((x - mx) ** 2 for x, _ in pts)
        if sxx <= 1e-12:
            continue
        b = sum((x - mx) * (y - my) for x, y in pts) / sxx
        a = my - b * mx
        ssr = sum((y - a - b * x) ** 2 for x, y in pts)
        s = math.sqrt(rw * rw + ssr / (n - 2))
        out[t["id"]] = [round4(inv(a + b * xt + z * s)) for z in Z]
    return out


BUILTINS = {"persistence": persistence, "curve": curve}


# ---------- validation and scoring ----------

def _no_constant(name):
    raise ValueError(f"non-finite number {name}")


def validate(path, case):
    """(quantiles by trophy id, None) or (None, reason)."""
    if not path.exists() or path.is_symlink() or not path.is_file():
        return None, "output missing or not a regular file"
    raw = path.read_bytes()
    if len(raw) > MAX_BYTES:
        return None, f"output is {len(raw)} bytes"
    try:
        doc = json.loads(raw.decode("utf-8"), parse_constant=_no_constant)
    except (ValueError, RecursionError) as e:
        return None, f"not UTF-8 JSON ({e})"
    if not isinstance(doc, dict) or set(doc) != {"trophies"} or not isinstance(doc["trophies"], list):
        return None, "not an object with exactly the key `trophies` (a list)"
    want = {t["id"] for t in case["trophies"]}
    got = {}
    for row in doc["trophies"]:
        if not isinstance(row, dict) or set(row) != {"id", "q"}:
            return None, "a row is not exactly {id, q}"
        tid, q = row["id"], row["q"]
        if isinstance(tid, bool) or not isinstance(tid, int) or tid not in want or tid in got:
            return None, f"bad or repeated id {tid!r}"
        if not isinstance(q, list) or len(q) != 5:
            return None, f"trophy {tid}: q is not five numbers"
        for j, v in enumerate(q):
            if isinstance(v, bool) or not isinstance(v, (int, float)) or not math.isfinite(v) or not 0 <= v <= 100:
                return None, f"trophy {tid}: q[{j}] is not a finite number in 0..100"
            if j and v < q[j - 1]:
                return None, f"trophy {tid}: quantiles decrease"
        got[tid] = [float(v) for v in q]
    if set(got) != want:
        return None, f"{len(want - set(got))} trophies have no row"
    return got, None


def last_rates(case):
    last = case["history"][-1]["rates"]
    return {t["id"]: [float(last[i] if last[i] is not None else 0)] * 5 for i, t in enumerate(case["trophies"])}


def run_entry(entry_dir, case_path, case):
    """(quantiles, valid, note, seconds): one sandboxed-ish run of the entry on one case."""
    with tempfile.TemporaryDirectory() as tmp:
        ind, outd = Path(tmp, "in"), Path(tmp, "out")
        ind.mkdir()
        outd.mkdir()
        (ind / case_path.name).write_bytes(case_path.read_bytes())
        env = dict(os.environ, MAKEFUN_INPUT_DIR=str(ind), MAKEFUN_OUTPUT_DIR=str(outd), PYTHONHASHSEED="0")
        t0 = time.monotonic()
        try:
            p = subprocess.run([sys.executable, "-P", "-s", str(Path(entry_dir).resolve() / "main.py")], env=env,
                               cwd=tmp, capture_output=True, timeout=TIMEOUT_S)
            note = None if p.returncode == 0 else f"exit {p.returncode}: {p.stderr.decode('utf-8', 'replace').strip()[-200:]}"
        except subprocess.TimeoutExpired:
            note = f"ran over {TIMEOUT_S} s"
        secs = time.monotonic() - t0
        q = None
        if note is None:
            q, note = validate(outd / f"{case_path.stem}.out", case)
    if q is None:
        return last_rates(case), False, note, secs
    return q, True, None, secs


class Tally:
    def __init__(self):
        self.loss = {}      # tier -> [sum, items]
        self.miss = [0.0, 0]
        self.cover = [0, 0]
        self.valid = True
        self.notes = []
        self.secs = 0.0

    def add(self, case, q, ans):
        for t in case["trophies"]:
            y = ans.get(str(t["id"]))
            if y is None:
                continue
            qs = q[t["id"]]
            cell = self.loss.setdefault(t["tier"], [0.0, 0])
            for tau, v in zip(LEVELS, qs):
                cell[0] += pinball(y, v, tau)
                cell[1] += 1
            self.miss[0] += abs(y - qs[2])
            self.miss[1] += 1
            self.cover[0] += qs[0] <= y <= qs[4]
            self.cover[1] += 1

    def line(self, name):
        s = sum(c[0] for c in self.loss.values())
        n = sum(c[1] for c in self.loss.values())
        if not n:
            return f"{name:<28} (no scored case)  valid {int(self.valid)}"
        tiers = "  ".join(f"{k} {self.loss[k][0] / self.loss[k][1]:.4f}" for k in TIERS if k in self.loss)
        return (f"{name:<28} loss {s / n:.6f}  miss {self.miss[0] / self.miss[1]:.3f}pp  "
                f"cov90 {self.cover[0] / self.cover[1]:.3f}  valid {int(self.valid)}  | {tiers}")


def worked_example():
    q = [10, 15, 20, 25, 35]
    items = [pinball(y, v, tau) for y in (22, 8) for tau, v in zip(LEVELS, q)]
    loss = sum(items) / len(items)
    inv_loss = (abs(logit(22) - logit(30)) + abs(logit(8) - logit(5))) / 2
    ok = f"{loss:.6f}" == "0.403404" and f"{inv_loss:.5f}" == "0.46023"
    print(f"scorer check (RULES worked example): loss {loss:.6f} (expect 0.403404), invalid-case {inv_loss:.5f} "
          f"(expect 0.46023) -> {'OK' if ok else 'MISMATCH'}")
    return ok


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--cases", required=True)
    ap.add_argument("--entry", action="append", default=[])
    ap.add_argument("--builtin", nargs="*", default=[], choices=sorted(BUILTINS))
    ap.add_argument("--per-case", action="store_true", help="also print one line per case")
    a = ap.parse_args()
    if not worked_example():
        sys.exit(1)
    paths = sorted(Path(a.cases).glob("*.in"))
    if not paths:
        sys.exit(f"no *.in case in {a.cases}")
    names = [f"builtin:{b}" for b in a.builtin] + list(a.entry)
    total = {n: Tally() for n in names}
    scored = 0
    for path in paths:
        case = json.loads(path.read_text(encoding="utf-8"))
        ans_path = path.with_name(path.stem + ".ans.json")
        ans = json.loads(ans_path.read_text(encoding="utf-8"))["rates"] if ans_path.exists() else None
        scored += ans is not None
        if a.per_case:
            print(f"-- {path.stem}: {len(case['history'])} reads, horizon {case['horizon_minutes']} min"
                  + ("" if ans else ", no answer (validity only)"))
        for n in names:
            if n.startswith("builtin:"):
                q, valid, note, secs = BUILTINS[n[8:]](case), True, None, 0.0
            else:
                q, valid, note, secs = run_entry(n, path, case)
            t = total[n]
            t.secs += secs
            if not valid:
                t.valid = False
                t.notes.append(f"{path.stem}: INVALID ({note})")
            one = Tally()
            one.valid = valid
            if ans is not None:
                t.add(case, q, ans)
                one.add(case, q, ans)
            if a.per_case:
                print("   " + one.line(n))
    print(f"== {len(paths)} cases, {scored} scored")
    for n in names:
        print(total[n].line(n) + ("" if n.startswith("builtin:") else f"  [{total[n].secs:.2f}s]"))
        for note in total[n].notes:
            print("   ! " + note)


if __name__ == "__main__":
    main()
