#!/usr/bin/env python3
"""
ICE Ready: daily keyword-opportunity finder (the "Vaultaire method").

It pulls the last N days of Google Search Console data for iceready.app through
gum (https://gumcli.dev), then lists queries where Google already shows the
site (impressions) but nobody clicks. Each of those is a candidate for one new,
dedicated guide page.

Usage:
    python tools/seo/keyword_opportunities.py              # last 28 days
    python tools/seo/keyword_opportunities.py --days 90 --min-impr 20

Requires gum on PATH, authorized with:  gum login --service searchconsole
Writes:  tools/seo/opportunities-YYYY-MM-DD.md
"""
import argparse
import datetime as dt
import json
import shutil
import subprocess
import sys
from pathlib import Path

SITE = "https://iceready.app/"  # URL-prefix property verified Nov 2026
OUT_DIR = Path(__file__).resolve().parent


def gum_query(site, start, end, dimensions, row_limit=5000):
    args = {
        "siteUrl": site,
        "body": {
            "startDate": start,
            "endDate": end,
            "dimensions": dimensions,
            "rowLimit": row_limit,
        },
    }
    cmd = ["gum", "read", "searchconsole.searchanalytics.query",
           "--args", json.dumps(args), "--output", "json"]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        sys.exit(f"gum failed:\n{res.stderr or res.stdout}")
    data = json.loads(res.stdout)
    # gum may wrap the API response; find the "rows" list wherever it is.
    def find_rows(obj):
        if isinstance(obj, dict):
            if isinstance(obj.get("rows"), list):
                return obj["rows"]
            for v in obj.values():
                r = find_rows(v)
                if r is not None:
                    return r
        return None
    return find_rows(data) or []


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--site", default=SITE)
    ap.add_argument("--days", type=int, default=28)
    ap.add_argument("--min-impr", type=int, default=10, help="minimum impressions")
    ap.add_argument("--max-ctr", type=float, default=0.01, help="max click-through rate (0.01 = 1%%)")
    ap.add_argument("--top", type=int, default=25)
    a = ap.parse_args()

    if not shutil.which("gum"):
        sys.exit("gum not found. Install: brew install ehmo/tap/gum  (see tools/seo/README.md)")

    end = dt.date.today() - dt.timedelta(days=2)  # GSC data lags ~2 days
    start = end - dt.timedelta(days=a.days)
    rows = gum_query(a.site, start.isoformat(), end.isoformat(), ["query", "page"])

    # Merge per query, remembering which page currently ranks best.
    by_q = {}
    for r in rows:
        q, page = r["keys"][0], r["keys"][1]
        e = by_q.setdefault(q, {"impr": 0, "clicks": 0, "pos_w": 0.0, "page": page, "best": 999})
        e["impr"] += r.get("impressions", 0)
        e["clicks"] += r.get("clicks", 0)
        e["pos_w"] += r.get("position", 0) * r.get("impressions", 0)
        if r.get("position", 999) < e["best"]:
            e["best"], e["page"] = r["position"], page

    opps = []
    for q, e in by_q.items():
        if e["impr"] < a.min_impr:
            continue
        ctr = e["clicks"] / e["impr"] if e["impr"] else 0
        pos = e["pos_w"] / e["impr"] if e["impr"] else 0
        if ctr <= a.max_ctr:
            # Score: lots of impressions but ranked far down = biggest upside from a dedicated page.
            score = e["impr"] * (min(pos, 60) / 10)
            opps.append((score, q, e["impr"], e["clicks"], pos, e["page"]))
    opps.sort(reverse=True)

    existing = {p.stem for p in (OUT_DIR.parents[1] / "guides").glob("*.html")}
    lines = [f"# Keyword opportunities: {dt.date.today()}",
             f"Search Console window {start} to {end}, site `{a.site}`. "
             f"Queries with >= {a.min_impr} impressions and CTR <= {a.max_ctr:.0%}.", "",
             "| # | Query | Impr | Clicks | Avg pos | Page Google shows now |",
             "|---|---|---|---|---|---|"]
    for i, (_, q, impr, clicks, pos, page) in enumerate(opps[:a.top], 1):
        lines.append(f"| {i} | {q} | {impr} | {clicks} | {pos:.1f} | {page.replace('https://iceready.app', '') or '/'} |")
    if not opps:
        lines.append("| - | No opportunities yet. Normal for a new site; widen --days or lower --min-impr. | | | | |")
    lines += ["", f"Existing guides: {', '.join(sorted(existing)) or 'none'}", "",
              "Next step: pick ONE query above that no existing guide covers, then run the "
              "prompt in tools/seo/DAILY_GUIDE_PROMPT.md."]

    out = OUT_DIR / f"opportunities-{dt.date.today()}.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))
    print(f"\nSaved {out}")


if __name__ == "__main__":
    main()
