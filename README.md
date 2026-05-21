# Shopify Store Analyzer — Python SDK

> **Get revenue estimates, traffic data, tech stack, brand age & dropshipper risk for any Shopify store via a single API call.**

Python client for the [Shopify Store Analyzer Apify Actor](https://apify.com/apivault_labs/shopify-store-analyzer) — extract **40+ business intelligence signals** from any Shopify store using only public data sources.

[![Apify Actor](https://img.shields.io/badge/Apify-Actor-blue?logo=apify)](https://apify.com/apivault_labs/shopify-store-analyzer)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/)
[![PyPI-friendly](https://img.shields.io/badge/install-pip-success)](#installation)

---

## What it does

For any Shopify store URL, this actor returns a single rich JSON record combining **9 public data sources** + **40+ derived intelligence signals**.

A direct, pay-per-use alternative to:
- [StoreLeads.app](https://storeleads.app) ($29/mo)
- [Commerce Inspector](https://commerceinspector.com) ($10/mo)
- [SimilarWeb Pro](https://www.similarweb.com)
- [BuiltWith](https://builtwith.com)

**Pricing:** $0.01 per store analyzed. No monthly subscription, no credits expiring, no rate limits.

---

## Quick start

```python
from shopify_analyzer import ShopifyAnalyzerClient

client = ShopifyAnalyzerClient(api_token="apify_api_xxxxxx")

result = client.analyze_one("https://allbirds.com")

print(f"Revenue:       ${result['revenue_estimate']['monthly_revenue_usd_est']:,}/mo")
print(f"Traffic:       {result['traffic']['monthly_visits']:,} visits/mo")
print(f"Brand age:     {result['estimated_brand_age_years']} years")
print(f"Tech stack:    {', '.join(result['tech_stack'])}")
print(f"Risk score:    {result['dropshipper_risk_score']}/100 ({result['dropshipper_risk_bucket']})")
```

Output:
```
Revenue:       $6,629,788/mo
Traffic:       3,608,048 visits/mo
Brand age:     10.4 years
Tech stack:    Google Analytics, Shop Pay, Apple Pay
Risk score:    50/100 (high)
```

---

## Installation

```bash
pip install git+https://github.com/apivault-labs/shopify-store-analyzer-python.git
```

Or clone and use directly:

```bash
git clone https://github.com/apivault-labs/shopify-store-analyzer-python.git
cd shopify-store-analyzer-python
pip install -r requirements.txt
```

Requires Python 3.9+ and the [`requests`](https://pypi.org/project/requests/) library.

---

## Get your API token (free)

1. Sign up at [apify.com](https://apify.com) — free tier includes $5 monthly credits, no card required
2. Go to [Account → Integrations](https://console.apify.com/account/integrations)
3. Copy your Personal API token

```bash
export APIFY_API_TOKEN=apify_api_xxxxxxxxxxxxxxxxxxxxxxxx
```

Or pass it explicitly:

```python
client = ShopifyAnalyzerClient(api_token="apify_api_xxxxxx")
```

---

## What you get for $0.01 per store

### 💰 Revenue & Traffic
- Estimated **monthly revenue** (visits × CR × AOV)
- **Annualized revenue** projection
- Monthly visits + 3-month trend (via SimilarWeb)
- Global rank, country rank, category rank
- Bounce rate, page per visit, avg time on site
- Top 5 countries by traffic share
- Top 10 keywords with search volume + CPC

### 📊 Product Intelligence
- Product count, AOV, price range
- New products in 7 / 30 / 90 days (velocity)
- Discount aggressiveness (% on sale + avg discount %)
- Vendor concentration, product types
- Inventory health (% in stock)
- **Top 20 product tags** (niche detection)
- **Duplicate description ratio** (dropshipper signal)
- Likely best-sellers (top 5 by image count)

### 🛠️ Tech Stack (60+ apps detected)
Klaviyo, Yotpo, Judge.me, ReCharge, Gorgias, AfterShip, PageFly, Shogun, Hotjar, Triple Whale, Northbeam, Algolia, Rebuy, Smile.io, Loox, Stamped, Okendo, Junip, Bold, Postscript, Attentive, Drift, Tidio, Re:amaze, Lucky Orange, Crazy Egg, Mouseflow, Refersion, ShipStation, ShipBob, Spocket, AutoDS, CJ Dropshipping, Oberlo, Dsers, Printful, Klarna, Afterpay, Sezzle, Affirm, Shop Pay, Apple Pay, Google Pay, PayPal — and more.

### 🎯 Tracking IDs (unique feature)
Public advertising IDs for **brand-network mapping**:
- Google Tag Manager (`GTM-XXXXXX`)
- GA4 (`G-XXXXXXXX`), Universal Analytics (`UA-X-X`)
- Facebook Pixel ID
- TikTok Pixel ID
- Pinterest Tag, Snapchat Pixel
- Klaviyo public key
- Hotjar Site ID, Intercom App ID, Microsoft Clarity ID

> Same FB Pixel on two different stores = same operator. Detect parallel brand operations.

### 📢 Active Promo & Announcement Bar
- Free shipping threshold (`$35`, `$50`, `$100`, or 0 for universal)
- Active promo codes (`SUMMER25`, `SAVE10`)
- Current discount % shown on the banner
- Announcement bar text

### ⏱️ Brand Age
- Earliest Wayback Machine snapshot
- Earliest SSL certificate (via crt.sh)
- Estimated brand age in years
- Estimated founding year
- Shopify CDN store ID (sequential, lower = older)

### 🌍 International Expansion
- All `hreflang` languages detected
- Currency switcher / country selector flags
- International expansion score (0–100)

### 🧠 Derived Intelligence
- **Customer segment** — mass-market / mid-market / premium / luxury
- **Marketing channel mix** — search-driven / social-driven / paid-driven / brand-driven / email-driven / mixed
- **Dropshipper risk score** (0–100) with explained signals

### 📱 Social & Contact
- Instagram, Facebook, Twitter/X, TikTok, YouTube, Pinterest, LinkedIn handles
- Public emails and phones from homepage

### 🌐 Sitemap totals
Real product / page / collection / blog counts (not just sample).

---

## Examples

See the [`examples/`](examples) folder for full code:

| File | What it does |
|---|---|
| [`quickstart.py`](examples/quickstart.py) | Analyze one store, print key metrics |
| [`bulk_analyze.py`](examples/bulk_analyze.py) | Analyze 50+ stores in parallel |
| [`find_dropshippers.py`](examples/find_dropshippers.py) | Filter stores by risk score |
| [`export_to_csv.py`](examples/export_to_csv.py) | Save results to CSV / Excel |
| [`compare_competitors.py`](examples/compare_competitors.py) | Side-by-side competitor comparison |
| [`monitor_changes.py`](examples/monitor_changes.py) | Track stores over time, detect changes |

---

## API reference

### `ShopifyAnalyzerClient(api_token=None, timeout=600)`

| Param | Type | Description |
|---|---|---|
| `api_token` | `str` | Apify API token. Falls back to `APIFY_API_TOKEN` env var. |
| `timeout` | `int` | Max seconds to wait for analysis. Default 600 (10 min). |

### `client.analyze(store_urls, conversion_rate=2.5, product_sample_size=250, ...)`

Analyze multiple stores synchronously.

| Param | Type | Default | Description |
|---|---|---|---|
| `store_urls` | `list[str]` | required | Shopify store URLs (full or bare domain) |
| `conversion_rate` | `float` | 2.5 | % for revenue formula. Industry: 2.5%, fashion: 1.5–2%, electronics: 1%, impulse: 3–4% |
| `product_sample_size` | `int` | 250 | Max products to sample (0 = full catalog) |
| `max_concurrency` | `int` | 3 | Parallel stores to analyze |

Plus boolean toggles to skip data sources for speed:

| Flag | Default | Effect |
|---|---|---|
| `extract_traffic` | `True` | Pull SimilarWeb data |
| `extract_brand_age` | `True` | Wayback Machine + crt.sh lookups |
| `extract_tech_stack` | `True` | Detect 60+ apps + tracking IDs |
| `extract_promo` | `True` | Free shipping, promo codes, announcement |
| `extract_international` | `True` | hreflang + currency switcher |
| `extract_sitemap` | `True` | Sitemap totals |
| `extract_derived_signals` | `True` | Risk score, customer segment, marketing mix |

Returns: `list[dict]` — one record per store.

### `client.analyze_one(store_url, **kwargs)`

Convenience wrapper for single-store analysis. Returns one `dict`.

---

## Sample output

```json
{
  "domain": "allbirds.com",
  "myshopify_handle": "weareallbirds.myshopify.com",
  "currency": "USD",
  "cdn_store_id": "1104/4168",
  "tech_stack": ["Google Analytics", "Shop Pay", "Apple Pay"],
  "tracking_ids": {
    "google_tag_manager": "TH8KRSBJ"
  },
  "announcement": {
    "announcement_discount_pct": 30,
    "announcement_bar_text": "30% off your order when you spend $150+. Discount automatically applied at checkout."
  },
  "socials": {
    "instagram": "allbirds",
    "tiktok": "weareallbirds"
  },
  "price_min": 3.0, "price_max": 99.0, "price_median": 39.0,
  "avg_order_value": 58.50,
  "products_on_sale_pct": 98.0,
  "avg_discount_pct": 53.0,
  "avg_images_per_product": 2.5,
  "unique_tags_count": 285,
  "top_tags": [
    {"tag": "collection:apr26", "count": 100},
    {"tag": "shoprunner", "count": 100}
  ],
  "duplicate_description_pct": 89.0,
  "new_products_30d": 100,
  "sitemap_products": 980,
  "hreflangs_count": 85,
  "international_expansion_score": 70,
  "estimated_brand_age_years": 10.4,
  "estimated_founded_year": 2015,
  "traffic": {
    "monthly_visits": 3608048,
    "global_rank": 10716,
    "category_rank": 127,
    "top_countries": [{"country_code": "US", "share": 0.87}]
  },
  "revenue_estimate": {
    "monthly_revenue_usd_est": 6629788,
    "annualized_revenue_usd_est": 79557456,
    "conversion_rate_used_pct": 2.5
  },
  "customer_segment": "mid-market",
  "marketing_channel_mix": "search-driven (58%)",
  "dropshipper_risk_score": 50,
  "dropshipper_risk_bucket": "high"
}
```

---

## Use cases

### 🥇 Dropshipping competitor research
Verify a competitor's revenue **before** copying their niche. Find legit brands (`dropshipper_risk_bucket: "low"`) with `revenue > $1M/mo` and study their tech stack.

### 🥈 B2B lead generation for Shopify apps
Find stores **without** your app (e.g. no Klaviyo → email automation pitch). Filter by revenue tier for enterprise prospects. Get founder emails and social handles in one call.

### 🥉 Investment due diligence
Verify claimed revenue. Cross-check brand age via Wayback + SSL. Spot paid-driven marketing (high CAC) vs brand-driven (sustainable).

### 🎯 Agency prospecting
- Old themes → pitch redesign
- Low `page_per_visit` → pitch CRO
- Low `international_expansion_score` → pitch geo-expansion
- High `dropshipper_risk_score` → skip (won't convert)

### 📊 Market research
Track 100+ competitors weekly. Compare AOV, velocity, tech stack across a niche.

### 🔍 Brand network detection
Use `tracking_ids` to detect domains sharing the same Facebook Pixel or GTM container — same operator behind multiple brands.

---

## Pricing

Pay only for what you analyze:

| Volume | Cost |
|---|---|
| 1 store | $0.01 |
| 100 stores | $1.00 |
| 1,000 stores | $10.00 |
| 10,000 stores | $100.00 |

Free Apify tier includes ~$5 monthly credit — analyze ~500 stores per month for free.

---

## How it works

All data sources are **public and free** — no logins, no proxies, no extra API keys:

1. `/products.json` — Shopify's public catalog API
2. `/collections.json` — public collections
3. `/sitemap.xml` — recursive child sitemaps for real totals
4. **Homepage HTML** — tech stack, socials, meta, tracking IDs, announcement bar
5. **SimilarWeb public API** — undocumented but stable
6. **Wayback Machine** — first snapshot date
7. **crt.sh** — earliest SSL cert (certificate transparency logs)
8. **hreflang scan** — international targeting
9. **Schema.org JSON-LD** — aggregateRating

Revenue formula:
```
revenue = monthly_visits × conversion_rate × AOV
AOV = median_price × 1.5  (industry heuristic for items per order)
```

---

## FAQ

**Q: Will it work on every Shopify store?**
A: Yes — every store with `/products.json` enabled (the default). Some stores hide their catalog; for those you still get tech stack, socials, traffic, brand age.

**Q: How accurate is the revenue estimate?**
A: For stores with 100K+ monthly visits: usually within ±25% of public revenue. Smaller stores: less reliable due to SimilarWeb sampling. Treat as order-of-magnitude.

**Q: Can it detect Shopify Plus stores?**
A: Yes, via the `likely_shopify_plus` boolean.

**Q: What if SimilarWeb has no data?**
A: Traffic / revenue fields will be null, but you still get all product, tech, brand age, and signal data.

**Q: Is the dropshipper risk score reliable?**
A: It's a heuristic. Scores 50+ almost always indicate dropshippers. Under 25 = legit brands. 25–50 = manual review.

**Q: Can I run this without Apify?**
A: This package is a thin wrapper around the hosted actor. The actor handles infrastructure, retries, parallelism. Self-hosted scraping at scale is a separate undertaking.

---

## Related Apify actors

- [Shopify Product Scraper](https://apify.com/apivault_labs/shopify-product-scraper) — extract full catalogs
- [WooCommerce Store Analyzer](https://apify.com/apivault_labs/woocommerce-store-analyzer) — same intelligence for WooCommerce
- [Domain Intelligence Scraper](https://apify.com/apivault_labs/domain-intelligence-scraper) — WHOIS, DNS, SSL, subdomains
- [WordPress Plugin Directory Scraper](https://apify.com/apivault_labs/wordpress-plugins-scraper) — 60K+ plugins

See [all actors by apivault_labs](https://apify.com/apivault_labs).

---

## License

MIT — see [LICENSE](LICENSE).

This client is open source. The underlying Apify actor is a paid service ($0.01/store).

---

## Keywords

`shopify-scraper` `shopify-store-analyzer` `shopify-revenue-estimator` `shopify-intelligence` `shopify-api` `storeleads-alternative` `commerce-inspector-alternative` `similarweb-alternative` `ecommerce-intelligence` `dropshipper-detection` `competitive-intelligence` `web-scraping` `apify` `apify-actor` `python-sdk` `shopify-tech-stack` `shopify-tracking-ids` `shopify-revenue-api` `shopify-traffic-estimation` `lead-generation` `b2b-leads`
