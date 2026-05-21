"""
Side-by-side comparison of competing Shopify stores.

Useful for pitch decks, niche research, or "should we copy this brand?" calls.

    export APIFY_API_TOKEN=apify_api_xxxxxx
    python examples/compare_competitors.py
"""

from shopify_analyzer import ShopifyAnalyzerClient


COMPETITORS = [
    "https://allbirds.com",
    "https://rothys.com",
    "https://atomsshoes.com",
]


def fmt_money(v) -> str:
    if v is None or v == 0:
        return "—"
    return f"${v:,.0f}"


def fmt_int(v) -> str:
    if v is None or v == 0:
        return "—"
    return f"{v:,}"


def main() -> None:
    client = ShopifyAnalyzerClient()
    results = client.analyze(COMPETITORS, max_concurrency=5)
    results = [r for r in results if r.get("success")]
    if not results:
        print("No successful results.")
        return

    rows = [
        ("Domain",          [r["domain"] for r in results]),
        ("Founded",         [r.get("estimated_founded_year") or "—" for r in results]),
        ("Visits/mo",       [fmt_int((r.get("traffic") or {}).get("monthly_visits")) for r in results]),
        ("Revenue/mo",      [fmt_money((r.get("revenue_estimate") or {}).get("monthly_revenue_usd_est")) for r in results]),
        ("Annualized",      [fmt_money((r.get("revenue_estimate") or {}).get("annualized_revenue_usd_est")) for r in results]),
        ("AOV",             [fmt_money(r.get("avg_order_value")) for r in results]),
        ("Median price",    [fmt_money(r.get("price_median")) for r in results]),
        ("Customer seg",    [r.get("customer_segment") or "—" for r in results]),
        ("Marketing mix",   [r.get("marketing_channel_mix") or "—" for r in results]),
        ("Tech stack",      [str(len(r.get("tech_stack") or [])) for r in results]),
        ("Sale products %", [str(r.get("products_on_sale_pct") or "—") for r in results]),
        ("Risk bucket",     [r.get("dropshipper_risk_bucket") or "—" for r in results]),
    ]

    col_w = 18
    print()
    print(f"{'Metric':<{col_w}} | " + " | ".join(f"{r['domain'][:col_w]:<{col_w}}" for r in results))
    print("-" * (col_w + 3 + (col_w + 3) * len(results)))
    for label, values in rows[1:]:  # skip the first row (domain header)
        print(f"{label:<{col_w}} | " + " | ".join(f"{str(v)[:col_w]:<{col_w}}" for v in values))


if __name__ == "__main__":
    main()
