"""Entry point: reads every <id>.in case, writes <id>.out. Python 3.13, standard library only, deterministic.

The forecast comes from model.py (structural launch-curve model). Whatever happens there, a valid file is written:
if the model raises or returns anything the grader would reject, the case falls back to the house persistence
forecast (last rate, logit spread 0.5 * sqrt(days)), and failing even that, to a flat wide row per trophy.
"""

import json
import math
import os
import sys
from pathlib import Path

# The grader's -P leaves this directory off sys.path: put it back so `import model` works.
sys.path.insert(0, str(Path(__file__).resolve().parent))

INPUT_DIR = Path(os.environ.get("MAKEFUN_INPUT_DIR", "/input"))
OUTPUT_DIR = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
Z = [-1.645, -0.674, 0, 0.674, 1.645]
MAX_BYTES = 65536


def round4(x):
    scaled = x * 10000
    whole = math.floor(scaled)
    if scaled - whole >= 0.5:
        whole += 1
    value = whole / 10000
    return int(value) if value.is_integer() else value


def trophy_ids(case):
    return [t["id"] for t in case["trophies"]]


def persistence(case):
    """The house baseline, tolerant of missing fields."""
    ids = trophy_ids(case)
    history = case.get("history") or []
    rates = (history[-1].get("rates") if history else None) or []
    try:
        spread = 0.5 * math.sqrt(max(0.0, float(case.get("horizon_minutes", 0))) / 1440)
    except (TypeError, ValueError):
        spread = 0.5
    rows = []
    for i, tid in enumerate(ids):
        r = rates[i] if i < len(rates) else None
        if not isinstance(r, (int, float)) or isinstance(r, bool) or not math.isfinite(r):
            r = 0.0
        c = min(99.99, max(0.01, r))
        lg = math.log(c / (100 - c))
        rows.append({"id": tid, "q": [round4(100 / (1 + math.exp(-(lg + z * spread)))) for z in Z]})
    return {"trophies": rows}


def valid(forecast, case):
    """True when the forecast is exactly what the rules accept for this case."""
    if not isinstance(forecast, dict) or list(forecast) != ["trophies"] or not isinstance(forecast["trophies"], list):
        return False
    ids = trophy_ids(case)
    rows = forecast["trophies"]
    if len(rows) != len(ids) or sorted(r.get("id") if isinstance(r, dict) else None for r in rows) != sorted(ids):
        return False
    for row in rows:
        if sorted(row) != ["id", "q"] or not isinstance(row["q"], list) or len(row["q"]) != 5:
            return False
        prev = 0.0
        for v in row["q"]:
            if isinstance(v, bool) or not isinstance(v, (int, float)) or not math.isfinite(v):
                return False
            if v < prev or v > 100:
                return False
            prev = v
    return len(encode(forecast)) <= MAX_BYTES


def encode(forecast):
    return (json.dumps(forecast, separators=(",", ":"), allow_nan=False) + "\n").encode("utf-8")


def forecast_case(case):
    try:
        import model
        result = model.forecast(case)
        if valid(result, case):
            return result
    except Exception:
        pass
    try:
        result = persistence(case)
        if valid(result, case):
            return result
    except Exception:
        pass
    # Last resort: a wide flat row per trophy (still a valid file).
    return {"trophies": [{"id": tid, "q": [0.01, 0.05, 0.5, 5, 50]} for tid in trophy_ids(case)]}


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for path in sorted(INPUT_DIR.glob("*.in")):   # name order: two runs write the same bytes
        try:
            case = json.loads(path.read_text(encoding="utf-8"))
            data = encode(forecast_case(case))
        except Exception:
            continue   # unreadable case or no trophy list: nothing valid can be written for it
        (OUTPUT_DIR / f"{path.stem}.out").write_bytes(data)


if __name__ == "__main__":
    main()
