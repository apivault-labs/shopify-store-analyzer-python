# Shopify Store Analyzer — Python SDK

Python client for [Shopify Store Analyzer on Apify](https://apify.com/apivault_labs/shopify-store-analyzer). Runs public URL analysis using your own Apify API token and returns Dataset records. Actor ID: `apivault_labs~shopify-store-analyzer`.

```bash
pip install shopify-store-analyzer
```

```python
from shopify_analyzer import ShopifyAnalyzer

# Reads APIFY_API_TOKEN from your environment.
client = ShopifyAnalyzer()
rows = client.analyze(["https://boody.com.au"], product_sample_size=10)
```

Published package: [PyPI, version 0.1.0](https://pypi.org/project/shopify-store-analyzer/). This version supports URL analysis and its legacy full output; it does not expose the newer discovery modes or output presets. Use the [Actor API/input reference](https://apify.com/apivault_labs/shopify-store-analyzer/input-schema) for those options.

## Data and costs

Contacts appear only when publicly found. Catalog samples are not complete store inventories. Estimates and scores are research assumptions, not verified sales or ownership. Inspect `data_quality`, run `SUMMARY` and `ERRORS` for source limits; missing fields are unknown. Shared tracking IDs do not establish common ownership.

Current Actor pricing is shown on the [Apify pricing page](https://apify.com/apivault_labs/shopify-store-analyzer/pricing). As checked on 19 October 2026, Dataset rows cost $4–15 per 1,000 by plan, plus a $0.0005 start event and user-paid platform/proxy usage. The SDK's legacy `estimate_cost()` uses a fixed $0.01 per store and must not be used as a current quote. Source rate limits and partial results can occur.

## Other integrations

- [n8n community node on npm](https://www.npmjs.com/package/n8n-nodes-apivault-shopify-analyzer)
- [n8n node source](https://github.com/apivault-labs/apivault-labs/tree/main/community-nodes/n8n-nodes-apivault-shopify-analyzer) — install on supported self-hosted n8n; Cloud availability requires separate verification.
- [Hosted Actor MCP](https://mcp.apify.com?tools=apivault_labs/shopify-store-analyzer) — requires Apify authentication.

The repository's examples are illustrative; compare their inputs with the current Actor schema before running a paid batch.

<!-- apivault-integrations:start -->
## Hosted Actor and integrations

- [Run Shopify Store Analyzer — No Login, Apps, Emails & Phones on Apify](https://apify.com/apivault_labs/shopify-store-analyzer).
- [Current pricing and usage terms](https://apify.com/apivault_labs/shopify-store-analyzer/pricing).
- [n8n community package: n8n-nodes-apivault-shopify-analyzer](https://www.npmjs.com/package/n8n-nodes-apivault-shopify-analyzer).
- [n8n source and usage](https://github.com/apivault-labs/n8n-nodes-apivault-shopify-analyzer).
- [n8n source and usage](https://github.com/apivault-labs/apivault-labs/tree/main/community-nodes/n8n-nodes-apivault-shopify-analyzer).

An Apify account and API token are required. Hosted Actor/platform charges apply. npm publication is not n8n verification or confirmation of n8n Cloud availability.
<!-- apivault-integrations:end -->
