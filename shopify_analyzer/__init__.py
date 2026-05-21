"""
Shopify Store Analyzer — Python SDK

Official Python client for the apivault_labs/shopify-store-analyzer Apify actor.
Get revenue estimates, traffic data, tech stack, brand age and dropshipper risk
for any Shopify store via a single API call.

Quick start:

    from shopify_analyzer import ShopifyAnalyzerClient

    client = ShopifyAnalyzerClient(api_token="apify_api_xxxxxx")
    result = client.analyze_one("https://allbirds.com")

    print(result["revenue_estimate"]["monthly_revenue_usd_est"])

See https://github.com/apivault-labs/shopify-store-analyzer-python for full docs.
"""

from .client import ShopifyAnalyzerClient
from .exceptions import (
    ShopifyAnalyzerError,
    AuthenticationError,
    ActorRunError,
    ActorTimeoutError,
)

__version__ = "0.1.0"
__all__ = [
    "ShopifyAnalyzerClient",
    "ShopifyAnalyzerError",
    "AuthenticationError",
    "ActorRunError",
    "ActorTimeoutError",
]
