"""
Quickstart: analyze a single Shopify store.

    pip install shopify-store-analyzer
    export APIFY_API_TOKEN=apify_api_xxxxxx
    python examples/quickstart.py
"""

import json

from shopify_analyzer import ShopifyAnalyzerClient


def main() -> None:
    client = ShopifyAnalyzerClient()  # picks up APIFY_API_TOKEN from env

    store = "https://allbirds.com"
    rec = client.analyze_one(store, product_sample_size=10, max_concurrency=1)

    # Preserve the Actor's actual fields and nulls. Missing traffic, contacts or
    # estimates are unknown; they must not become zero or crash the first run.
    print(json.dumps(rec, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
