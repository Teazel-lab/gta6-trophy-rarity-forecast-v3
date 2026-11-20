#!/usr/bin/env python3
"""Parse our Exophase trophy-page recordings into contest-shaped reads and pseudo-cases (stdlib only).

A recording is `_rec/page-YYYYMMDDTHHMMSSZ.html.gz`; the filename time is the read time (UTC). Markup used:
  - overview strip: `<strong>36,080</strong> <span>Players Tracked</span>` (same for Trophies Earned, Total Trophies);
  - one `<li class="... award [secret]" data-award-id=.. data-average="7.99" data-points="15">` per trophy, holding
    `award-title` (<a>name</a>), `award-description`, an `exo-icon-trophy-<tier>` icon and `award-average`
    (`7.99% (..)`).
A page counts only if it parses whole: players tracked, Total Trophies, and exactly that many rows with name and rate.

CLI: python3 tools/exo.py --rec _rec --cut <iso> --target <iso> --out <dir> [--prefix _kit/input/p01.in]
writes <dir>/<id>.in and <dir>/<id>.ans.json.
"""

import argparse
import gzip
import html
import json
import re
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

SCHEMA = "makefun/gta6-trophies-case/v1"
LEVELS = [0.05, 0.25, 0.5, 0.75, 0.95]
GAME = {
    "name": "Grand Theft Auto VI",
    "platform": "PS5",
    "release_date": "2026-11-19",
    "source": "https://www.exophase.com/game/grand-theft-auto-vi-psn/trophies/",
}
PSN_POINTS = {"platinum": 300, "gold": 90, "silver": 30, "bronze": 15}
SLOT_MINUTES = 10

_FILE = re.compile(r"^page-(\d{8}T\d{6})Z\.html\.gz$")
_LI = re.compile(r'<li\s+class="([^"]*\baward\b[^"]*)"([^>]*)>')
_TITLE = re.compile(r'award-title[^>]*>\s*(?:<a[^>]*>)?(.*?)(?:</a>|</div>)', re.S)
_DESC = re.compile(r'award-description[^>]*>(.*?)</div>', re.S)
_TIER = re.compile(r"exo-icon-trophy-(platinum|gold|silver|bronze)")
_RATE = re.compile(r'award-average.*?>\s*(\d{1,3}(?:\.\d+)?)%', re.S)
_ATTR_AVG = re.compile(r'data-average="(\d{1,3}(?:\.\d+)?)"')
_TAG = re.compile(r"<[^>]+>")


def parse_iso(s):
    """ISO 8601 UTC ('...Z', optional fraction) -> aware datetime."""
    return datetime.fromisoformat(s.replace("Z", "+00:00")).astimezone(timezone.utc)


def iso(dt, millis=False):
    dt = dt.astimezone(timezone.utc)
    if millis:
        return dt.strftime("%Y-%m-%dT%H:%M:%S.") + f"{dt.microsecond // 1000:03d}Z"
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")


def _text(fragment):
    return re.sub(r"\s+", " ", html.unescape(_TAG.sub("", fragment))).strip()


def _stat(page, label):
    m = re.search(r"<strong>\s*([\d,]+)\s*</strong>\s*<span>\s*" + re.escape(label) + r"\s*</span>", page)
    return int(m.group(1).replace(",", "")) if m else None


def parse_page(page):
    """HTML text -> {"players_tracked","trophies_earned","rates","trophies"} or None if it does not parse whole."""
    players = _stat(page, "Players Tracked")
    total = _stat(page, "Total Trophies")
    earned = _stat(page, "Trophies Earned")
    if players is None or total is None or total <= 0:
        return None
    heads = list(_LI.finditer(page))
    if len(heads) != total:
        return None
    trophies, rates = [], []
    for k, m in enumerate(heads):
        end = heads[k + 1].start() if k + 1 < len(heads) else len(page)
        body = page[m.end():end]
        cut = body.find("</li>")
        if cut >= 0:
            body = body[:cut]
        title, desc, tier = _TITLE.search(body), _DESC.search(body), _TIER.search(body)
        rate = _RATE.search(body) or _ATTR_AVG.search(m.group(2))
        if not title or not tier or not rate:
            return None
        name = _text(title.group(1))
        value = float(rate.group(1))
        if not name or not 0 <= value <= 100:
            return None
        trophies.append({
            "id": k + 1,
            "name": name,
            "description": _text(desc.group(1)) if desc else "",
            "tier": tier.group(1),
            "points": PSN_POINTS[tier.group(1)],
            "secret": "secret" in m.group(1).split(),
        })
        rates.append(value)
    return {"players_tracked": players, "trophies_earned": earned, "rates": rates, "trophies": trophies}


def load_reads(rec_dir):
    """Every recording that parses whole, oldest first: (reads, trophies of the newest read).

    Each read: {"slot","at","players_tracked","trophies_earned","rates"} plus "_names" (its trophy names in order).
    """
    reads, trophies = [], []
    for path in sorted(Path(rec_dir).iterdir()):
        m = _FILE.match(path.name)
        if not m:
            continue
        at = datetime.strptime(m.group(1), "%Y%m%dT%H%M%S").replace(tzinfo=timezone.utc)
        try:
            with gzip.open(path, "rt", encoding="utf-8", errors="replace") as f:
                parsed = parse_page(f.read())
        except (OSError, EOFError):
            parsed = None
        if parsed is None:
            print(f"exo: {path.name} does not parse whole, skipped", file=sys.stderr)
            continue
        slot = at.replace(minute=at.minute - at.minute % SLOT_MINUTES, second=0, microsecond=0)
        reads.append({
            "slot": iso(slot),
            "at": iso(at, millis=True),
            "players_tracked": parsed["players_tracked"],
            "trophies_earned": parsed["trophies_earned"],
            "rates": parsed["rates"],
            "_names": [t["name"] for t in parsed["trophies"]],
        })
        trophies = parsed["trophies"]
    reads.sort(key=lambda r: r["at"])
    return reads, trophies


def _public(read, n):
    rates = list(read["rates"][:n]) + [None] * max(0, n - len(read["rates"]))
    return {k: read[k] for k in ("slot", "at", "players_tracked", "trophies_earned")} | {"rates": rates}


def make_case(reads, trophies, cut_at, target, prefix_history=None, case_id=None):
    """(case, answer): a kit-schema case holding only reads strictly before cut_at; answer = first read at/after target.

    reads/trophies as load_reads returns them. prefix_history: a kit case dict (e.g. _kit/input/p01.in) whose reads
    before our first read are prepended, their rates mapped by trophy id. The case's trophies are the ones its last
    read lists. answer is None when no read at or after target exists.
    """
    cut_dt, target_dt = parse_iso(cut_at), parse_iso(target)
    before = [r for r in reads if parse_iso(r["at"]) < cut_dt]
    if before:
        n = len(before[-1]["rates"])
        case_trophies = [dict(t) for t in trophies[:n]]
        if [t["name"] for t in case_trophies] != before[-1]["_names"][:n]:
            raise ValueError("the trophy list changed after the case's last read; pass that read's list")
    else:
        case_trophies = [dict(t) for t in (prefix_history or {}).get("trophies", [])]
        n = len(case_trophies)
    history = []
    if prefix_history:
        first = parse_iso(before[0]["at"]) if before else cut_dt
        pid = [t["id"] for t in prefix_history["trophies"]]
        for r in prefix_history["history"]:
            if parse_iso(r["at"]) >= min(first, cut_dt):
                continue
            by_id = dict(zip(pid, r["rates"]))
            history.append({k: r[k] for k in ("slot", "at", "players_tracked", "trophies_earned")}
                           | {"rates": [by_id.get(t["id"]) for t in case_trophies]})
    history += [_public(r, n) for r in before]
    if not history:
        raise ValueError("no read before the cut")
    cid = case_id or "x" + cut_dt.strftime("%m%d%H%M") + "t" + target_dt.strftime("%m%d%H%M")
    case = {
        "schema": SCHEMA,
        "id": cid,
        "at": iso(cut_dt),
        "horizon_minutes": round((target_dt - cut_dt) / timedelta(minutes=1)),
        "target": iso(target_dt),
        "levels": LEVELS,
        "game": dict(GAME),
        "trophies": case_trophies,
        "history": history,
        "notes": "Pseudo-case cut from our own recordings of the Exophase page (plus the kit's launch-night reads "
                 "when prefixed). `history` holds every read before `at`, oldest first; `rates` follows `trophies`.",
    }
    answer = None
    for r in reads:
        if parse_iso(r["at"]) >= target_dt and len(r["rates"]) >= n and r["_names"][:n] == [t["name"] for t in case_trophies]:
            answer = {
                "id": cid,
                "target": iso(target_dt),
                "answer_at": r["at"],
                "players_tracked": r["players_tracked"],
                "rates": {str(t["id"]): r["rates"][i] for i, t in enumerate(case_trophies)},
            }
            break
    return case, answer


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--rec", default="_rec")
    ap.add_argument("--cut", required=True, help="checkpoint, ISO 8601 UTC")
    ap.add_argument("--target", required=True, help="target, ISO 8601 UTC")
    ap.add_argument("--out", required=True)
    ap.add_argument("--prefix", help="kit case whose launch-night reads are prepended (e.g. _kit/input/p01.in)")
    ap.add_argument("--id", help="case id (default derived from cut and target)")
    a = ap.parse_args()
    reads, trophies = load_reads(a.rec)
    prefix = json.loads(Path(a.prefix).read_text(encoding="utf-8")) if a.prefix else None
    case, answer = make_case(reads, trophies, a.cut, a.target, prefix, a.id)
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    (out / f"{case['id']}.in").write_text(json.dumps(case, separators=(",", ":")) + "\n", encoding="utf-8")
    msg = f"{case['id']}: {len(case['history'])} reads, {len(case['trophies'])} trophies, horizon {case['horizon_minutes']} min"
    if answer:
        (out / f"{case['id']}.ans.json").write_text(json.dumps(answer, separators=(",", ":")) + "\n", encoding="utf-8")
        msg += f", answer read at {answer['answer_at']}"
    else:
        msg += ", NO answer read at or after the target"
    print(msg)


if __name__ == "__main__":
    main()
