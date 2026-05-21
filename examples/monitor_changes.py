"""
Track a list of Shopify stores over time and detect changes.

Run this on a schedule (cron, GitHub Actions) to monitor:
- New tech-stack additions (new app integrations)
- Revenue trend changes
- Sudden product-velocity spikes
- New promo codes / discount drops

This script saves snapshots to a local JSON file and diffs against
the previous run.

    export APIFY_API_TOKEN=apify_api_xxxxxx
    python examples/monitor_changes.py
"""

import json
import os
import time
from pathlib import Path

from shopify_analyzer import ShopifyAnalyzerClient


WATCH = [
    "https://allbirds.com",
    "https://gymshark.com",
]
SNAPSHOT_FILE = Path("monitor_snapshot.json")


def main() -> None:
    client = ShopifyAnalyzerClient()
    new = client.analyze(WATCH, max_concurrency=5)

    # Build a lookup by domain
    new_by_domain = {r["domain"]: r for r in new if r.get("success")}

    # Previous snapshot (if exists)
    if SNAPSHOT_FILE.exists():
        old_by_domain = {r["domain"]: r for r in json.loads(SNAPSHOT_FILE.read_text())}
    else:
        old_by_domain = {}

    print(f"Tracking {len(new_by_domain)} stores (snapshot: {SNAPSHOT_FILE})\n")

    for domain, new_rec in new_by_domain.items():
        old_rec = old_by_domain.get(domain)
        print(f"=== {domain} ===")
        if not old_rec:
            print("  (first observation, no diff)")
            continue

        # Tech stack diff
        old_tech = set(old_rec.get("tech_stack") or [])
        new_tech = set(new_rec.get("tech_stack") or [])
        added = new_tech - old_tech
        removed = old_tech - new_tech
        if added:
            print(f"  + Added apps:    {', '.join(sorted(added))}")
        if removed:
            print(f"  - Removed apps:  {', '.join(sorted(removed))}")

        # Revenue trend
        old_rev = (old_rec.get("revenue_estimate") or {}).get("monthly_revenue_usd_est") or 0
        new_rev = (new_rec.get("revenue_estimate") or {}).get("monthly_revenue_usd_est") or 0
        if old_rev and new_rev:
            delta = (new_rev - old_rev) / old_rev * 100
            arrow = "↑" if delta > 0 else "↓"
            print(f"  Revenue:       ${old_rev:,.0f} {arrow} ${new_rev:,.0f}  ({delta:+.1f}%)")

        # New promo codes
        old_promo = set((old_rec.get("announcement") or {}).get("active_promo_codes") or [])
        new_promo = set((new_rec.get("announcement") or {}).get("active_promo_codes") or [])
        if new_promo - old_promo:
            print(f"  + New promo:     {', '.join(new_promo - old_promo)}")

        # Risk score change
        old_risk = old_rec.get("dropshipper_risk_score") or 0
        new_risk = new_rec.get("dropshipper_risk_score") or 0
        if old_risk != new_risk:
            print(f"  Risk score:    {old_risk} → {new_risk}")
        print()

    # Persist new snapshot
    SNAPSHOT_FILE.write_text(json.dumps(list(new_by_domain.values()), indent=2))
    print(f"Snapshot saved → {SNAPSHOT_FILE}")


if __name__ == "__main__":
    main()
