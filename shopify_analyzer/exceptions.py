"""Exception classes for the Shopify Store Analyzer SDK."""


class ShopifyAnalyzerError(Exception):
    """Base exception for all SDK errors."""


class AuthenticationError(ShopifyAnalyzerError):
    """Raised when the Apify API token is missing or invalid."""


class ActorRunError(ShopifyAnalyzerError):
    """Raised when the actor run fails on Apify infrastructure."""


class ActorTimeoutError(ShopifyAnalyzerError):
    """Raised when the actor run does not finish within the allowed timeout."""
