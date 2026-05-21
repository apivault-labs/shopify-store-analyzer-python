"""
Filter out dropshippers from a list of candidate Shopify stores.

Useful for:
- Investment due diligence (avoid risky brands)
- Lead generation (skip stores that won't convert)
- Niche research (find legit operators in a category)

    export APIFY_API_TOKEN=apify_api_xxxxxx
    python examples/find_dropshippers.py
"""

from shopify_analyzer import ShopifyAnalyzerClient


CANDIDATES = [
    "https://allbirds.com",
    "https://gymshark.com",
    # Add more candidates here — you can paste 100s
]


def main() -> None:
    client = ShopifyAnalyzerClient()
    results = client.analyze(CANDIDATES, max_concurrency=5)

    legit = []
    medium = []
    risky = []

    for r in results:
        if not r.get("success"):
            continue
        bucket = r.get("dropshipper_risk_bucket")
        if bucket == "low":
            legit.append(r)
        elif bucket == "medium":
            medium.append(r)
        else:
            risky.append(r)

    def _print(group: list[dict], label: str) -> None:
        print(f"\n=== {label} ({len(group)}) ===")
        for r in group:
            score = r.get("dropshipper_risk_score", 0)
            visits = (r.get("traffic") or {}).get("monthly_visits") or 0
            rev = (r.get("revenue_estimate") or {}).get("monthly_revenue_usd_est") or 0
            age = r.get("estimated_brand_age_years") or "?"
            print(f"  {r.get('domain', '?'):<30} risk={score:>3} • "
                  f"{visits:>8,} visits • ${rev:>10,.0f}/mo • age={age}y")
            for reason in (r.get("dropshipper_signals") or [])[:3]:
                print(f"      ↳ {reason}")

    _print(legit, "LEGIT brands (recommended)")
    _print(medium, "MEDIUM risk (manual review)")
    _print(risky, "HIGH risk (likely dropshippers — skip)")


if __name__ == "__main__":
    main()
