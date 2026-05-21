"""
Analyze stores and export the flattened results to CSV.

Drop into Excel, Google Sheets, Numbers, or import into a database.

    pip install -r requirements.txt
    export APIFY_API_TOKEN=apify_api_xxxxxx
    python examples/export_to_csv.py > stores.csv
"""

import csv
import sys

from shopify_analyzer import ShopifyAnalyzerClient


STORES = [
    "https://allbirds.com",
    "https://gymshark.com",
    "https://colourpop.com",
]

COLUMNS = [
    "domain",
    "monthly_visits",
    "monthly_revenue_usd_est",
    "annualized_revenue_usd_est",
    "avg_order_value",
    "price_median",
    "products_on_sale_pct",
    "avg_discount_pct",
    "new_products_30d",
    "estimated_brand_age_years",
    "estimated_founded_year",
    "customer_segment",
    "marketing_channel_mix",
    "dropshipper_risk_score",
    "dropshipper_risk_bucket",
    "tech_stack_count",
    "tech_stack",
    "google_tag_manager",
    "facebook_pixel",
    "instagram_handle",
    "free_shipping_threshold_usd",
    "active_promo_codes",
    "hreflangs_count",
    "international_expansion_score",
]


def flatten(rec: dict) -> dict:
    traffic = rec.get("traffic") or {}
    revenue = rec.get("revenue_estimate") or {}
    tracking = rec.get("tracking_ids") or {}
    socials = rec.get("socials") or {}
    ann = rec.get("announcement") or {}
    tech = rec.get("tech_stack") or []
    promo = ann.get("active_promo_codes") or []
    return {
        "domain": rec.get("domain"),
        "monthly_visits": traffic.get("monthly_visits"),
        "monthly_revenue_usd_est": revenue.get("monthly_revenue_usd_est"),
        "annualized_revenue_usd_est": revenue.get("annualized_revenue_usd_est"),
        "avg_order_value": rec.get("avg_order_value"),
        "price_median": rec.get("price_median"),
        "products_on_sale_pct": rec.get("products_on_sale_pct"),
        "avg_discount_pct": rec.get("avg_discount_pct"),
        "new_products_30d": rec.get("new_products_30d"),
        "estimated_brand_age_years": rec.get("estimated_brand_age_years"),
        "estimated_founded_year": rec.get("estimated_founded_year"),
        "customer_segment": rec.get("customer_segment"),
        "marketing_channel_mix": rec.get("marketing_channel_mix"),
        "dropshipper_risk_score": rec.get("dropshipper_risk_score"),
        "dropshipper_risk_bucket": rec.get("dropshipper_risk_bucket"),
        "tech_stack_count": len(tech),
        "tech_stack": "; ".join(tech),
        "google_tag_manager": tracking.get("google_tag_manager"),
        "facebook_pixel": tracking.get("facebook_pixel"),
        "instagram_handle": socials.get("instagram"),
        "free_shipping_threshold_usd": ann.get("free_shipping_threshold_usd"),
        "active_promo_codes": "; ".join(promo) if isinstance(promo, list) else promo,
        "hreflangs_count": rec.get("hreflangs_count"),
        "international_expansion_score": rec.get("international_expansion_score"),
    }


def main() -> None:
    client = ShopifyAnalyzerClient()
    results = client.analyze(STORES, max_concurrency=5)

    writer = csv.DictWriter(sys.stdout, fieldnames=COLUMNS)
    writer.writeheader()
    for r in results:
        if not r.get("success"):
            continue
        writer.writerow(flatten(r))


if __name__ == "__main__":
    main()
