"""
Quickstart: analyze a single Shopify store.

    pip install -r requirements.txt
    export APIFY_API_TOKEN=apify_api_xxxxxx
    python examples/quickstart.py
"""

from shopify_analyzer import ShopifyAnalyzerClient


def main() -> None:
    client = ShopifyAnalyzerClient()  # picks up APIFY_API_TOKEN from env

    store = "https://allbirds.com"
    rec = client.analyze_one(store)

    print(f"\n=== {rec['domain']} ===\n")

    traffic = rec.get("traffic") or {}
    revenue = rec.get("revenue_estimate") or {}

    print(f"Monthly visits:    {traffic.get('monthly_visits') or '-':,}")
    print(f"Monthly revenue:   ${revenue.get('monthly_revenue_usd_est') or 0:,}")
    print(f"Annualized:        ${revenue.get('annualized_revenue_usd_est') or 0:,}")
    print(f"AOV:               ${rec.get('avg_order_value') or 0}")
    print(f"Brand age:         {rec.get('estimated_brand_age_years') or '-'} years")
    print(f"Customer segment:  {rec.get('customer_segment') or '-'}")
    print(f"Marketing mix:     {rec.get('marketing_channel_mix') or '-'}")

    print(f"\nTech stack ({len(rec.get('tech_stack') or [])}):")
    for app in rec.get("tech_stack") or []:
        print(f"  - {app}")

    tracking = rec.get("tracking_ids") or {}
    if tracking:
        print(f"\nTracking IDs:")
        for k, v in tracking.items():
            print(f"  - {k}: {v}")

    ann = rec.get("announcement") or {}
    if ann:
        print(f"\nActive promo:")
        for k, v in ann.items():
            print(f"  - {k}: {v}")

    print(f"\nDropshipper risk:  {rec.get('dropshipper_risk_score', 0)}/100 "
          f"({rec.get('dropshipper_risk_bucket', '?')})")
    for reason in rec.get("dropshipper_signals") or []:
        print(f"  • {reason}")


if __name__ == "__main__":
    main()
