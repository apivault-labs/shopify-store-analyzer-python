"""
Analyze many Shopify stores in one batch.

The actor itself runs them in parallel on Apify infrastructure, so a single
``analyze`` call with many URLs is faster and cheaper than calling the SDK
once per store.

    export APIFY_API_TOKEN=apify_api_xxxxxx
    python examples/bulk_analyze.py
"""

from shopify_analyzer import ShopifyAnalyzerClient


STORES = [
    "https://allbirds.com",
    "https://gymshark.com",
    "https://colourpop.com",
    "https://kyliecosmetics.com",
    "https://fashionnova.com",
    "https://mvmt.com",
    "https://chubbiesshorts.com",
]


def main() -> None:
    client = ShopifyAnalyzerClient(timeout=900)
    print(f"Analyzing {len(STORES)} stores "
          f"(estimated cost: ${client.estimate_cost(len(STORES))})...\n")

    results = client.analyze(
        STORES,
        max_concurrency=5,
        # speed-ups: skip slower data sources if you don't need them
        extract_brand_age=True,    # Wayback + crt.sh — slowest
        extract_traffic=True,       # SimilarWeb — adds ~1-2s per store
    )

    print(f"{'Domain':<25} {'Visits/mo':>12} {'Revenue/mo':>14} {'Risk':>6}")
    print("-" * 60)
    for r in sorted(results, key=lambda x: -((x.get("traffic") or {}).get("monthly_visits") or 0)):
        if not r.get("success"):
            print(f"{r.get('domain', r.get('input_url', '?')):<25} ERROR: {r.get('error')}")
            continue
        traffic = r.get("traffic") or {}
        revenue = r.get("revenue_estimate") or {}
        visits = traffic.get("monthly_visits") or 0
        rev = revenue.get("monthly_revenue_usd_est") or 0
        risk = r.get("dropshipper_risk_bucket", "?")
        print(f"{r.get('domain', '?'):<25} {visits:>12,} {f'${rev:,.0f}':>14} {risk:>6}")


if __name__ == "__main__":
    main()
