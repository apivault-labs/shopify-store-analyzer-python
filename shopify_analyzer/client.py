"""
ShopifyAnalyzerClient — thin synchronous wrapper around the Apify
``apivault_labs/shopify-store-analyzer`` actor.

The actor handles all heavy work (HTTP, parallelism, retries) on Apify
infrastructure. This client only forwards inputs, polls until the run
finishes, then downloads the dataset.

Usage:

    from shopify_analyzer import ShopifyAnalyzerClient

    client = ShopifyAnalyzerClient(api_token="apify_api_xxxxxx")
    rec = client.analyze_one("https://allbirds.com")
    print(rec["revenue_estimate"]["monthly_revenue_usd_est"])
"""

from __future__ import annotations

import os
import time
from typing import Any, Iterable

import requests

from .exceptions import (
    ActorRunError,
    ActorTimeoutError,
    AuthenticationError,
    ShopifyAnalyzerError,
)


ACTOR_ID = "apivault_labs~shopify-store-analyzer"
APIFY_API_BASE = "https://api.apify.com/v2"

# Run states reported by Apify
TERMINAL_OK = {"SUCCEEDED"}
TERMINAL_FAIL = {"FAILED", "TIMED-OUT", "ABORTED"}


class ShopifyAnalyzerClient:
    """Synchronous client for the Shopify Store Analyzer Apify actor.

    Parameters
    ----------
    api_token : str, optional
        Apify Personal API token. If omitted, falls back to the
        ``APIFY_API_TOKEN`` environment variable.
    timeout : int, optional
        Maximum seconds to wait for an actor run to finish. Default 600.
    poll_interval : float, optional
        Seconds between status polls. Default 3.
    base_url : str, optional
        Override the Apify API base URL (mostly for testing).
    """

    def __init__(
        self,
        api_token: str | None = None,
        timeout: int = 600,
        poll_interval: float = 3.0,
        base_url: str = APIFY_API_BASE,
    ):
        token = api_token or os.environ.get("APIFY_API_TOKEN")
        if not token:
            raise AuthenticationError(
                "Apify API token is required. Pass api_token='apify_api_...' "
                "or set the APIFY_API_TOKEN environment variable. "
                "Get a token at https://console.apify.com/account/integrations"
            )
        self._token = token
        self._timeout = int(timeout)
        self._poll_interval = float(poll_interval)
        self._base_url = base_url.rstrip("/")
        self._session = requests.Session()
        self._session.headers.update({
            "Authorization": f"Bearer {self._token}",
            "Content-Type": "application/json",
            "User-Agent": "shopify-analyzer-python/0.1.0",
        })

    # ------------------------------------------------------------------ public

    def analyze(
        self,
        store_urls: Iterable[str],
        *,
        conversion_rate: float = 2.5,
        product_sample_size: int = 250,
        max_concurrency: int = 3,
        actor_timeout_secs: int = 300,
        extract_products: bool = True,
        extract_velocity: bool = True,
        extract_collections: bool = True,
        extract_sitemap: bool = True,
        extract_traffic: bool = True,
        extract_revenue_estimate: bool = True,
        extract_tech_stack: bool = True,
        extract_socials: bool = True,
        extract_contact: bool = True,
        extract_shopify_meta: bool = True,
        extract_international: bool = True,
        extract_reviews_aggregate: bool = True,
        extract_brand_age: bool = True,
        extract_derived_signals: bool = True,
        extract_promo: bool = True,
    ) -> list[dict[str, Any]]:
        """Run the actor synchronously and return a list of result records.

        See the README for the full output schema. Each item in the returned
        list is a dict describing one analyzed store.
        """
        urls = [u for u in store_urls if u]
        if not urls:
            raise ValueError("store_urls must contain at least one non-empty URL")

        payload = {
            "storeUrls": list(urls),
            "conversionRate": float(conversion_rate),
            "productSampleSize": int(product_sample_size),
            "maxConcurrency": int(max_concurrency),
            "extractProducts": extract_products,
            "extractVelocity": extract_velocity,
            "extractCollections": extract_collections,
            "extractSitemap": extract_sitemap,
            "extractTraffic": extract_traffic,
            "extractRevenueEstimate": extract_revenue_estimate,
            "extractTechStack": extract_tech_stack,
            "extractSocials": extract_socials,
            "extractContact": extract_contact,
            "extractShopifyMeta": extract_shopify_meta,
            "extractInternational": extract_international,
            "extractReviewsAggregate": extract_reviews_aggregate,
            "extractBrandAge": extract_brand_age,
            "extractDerivedSignals": extract_derived_signals,
            "extractPromo": extract_promo,
        }

        run_id = self._start_run(payload, actor_timeout_secs=actor_timeout_secs)
        run = self._wait_for_run(run_id)
        return self._fetch_dataset(run["defaultDatasetId"])

    def analyze_one(self, store_url: str, **kwargs: Any) -> dict[str, Any]:
        """Convenience wrapper for a single-store analysis.

        Returns the first (and only) record. Raises ``ActorRunError`` if no
        record is produced (e.g. the URL is not a Shopify store).
        """
        results = self.analyze([store_url], **kwargs)
        if not results:
            raise ActorRunError(
                f"Actor returned no records for {store_url!r} — "
                "the URL might not be a Shopify store."
            )
        return results[0]

    def estimate_cost(self, store_count: int) -> float:
        """Return the estimated USD cost for analyzing `store_count` stores."""
        return round(store_count * 0.01, 4)

    # ------------------------------------------------------------------ private

    def _start_run(self, payload: dict[str, Any], actor_timeout_secs: int) -> str:
        url = f"{self._base_url}/acts/{ACTOR_ID}/runs"
        params = {"timeout": int(actor_timeout_secs)}
        try:
            r = self._session.post(url, params=params, json=payload, timeout=30)
        except requests.RequestException as e:
            raise ShopifyAnalyzerError(f"Failed to start actor run: {e}") from e

        if r.status_code == 401:
            raise AuthenticationError(
                "Apify rejected the API token. Generate a new one at "
                "https://console.apify.com/account/integrations"
            )
        if r.status_code >= 400:
            raise ActorRunError(
                f"Apify returned HTTP {r.status_code} when starting run: {r.text[:300]}"
            )

        data = r.json().get("data") or {}
        run_id = data.get("id")
        if not run_id:
            raise ActorRunError(f"Apify response missing run id: {r.text[:300]}")
        return run_id

    def _wait_for_run(self, run_id: str) -> dict[str, Any]:
        url = f"{self._base_url}/actor-runs/{run_id}"
        deadline = time.time() + self._timeout
        while True:
            try:
                r = self._session.get(url, timeout=30)
            except requests.RequestException as e:
                raise ShopifyAnalyzerError(f"Failed to poll run status: {e}") from e

            if r.status_code >= 400:
                raise ActorRunError(
                    f"Apify returned HTTP {r.status_code} when polling run: {r.text[:300]}"
                )

            run = r.json().get("data") or {}
            status = run.get("status")
            if status in TERMINAL_OK:
                return run
            if status in TERMINAL_FAIL:
                raise ActorRunError(
                    f"Actor run {run_id} ended with status={status}: "
                    f"{run.get('statusMessage') or '(no message)'}"
                )

            if time.time() > deadline:
                raise ActorTimeoutError(
                    f"Actor run {run_id} did not finish within {self._timeout}s "
                    f"(last status={status}). The run may still be running on Apify; "
                    "increase `timeout=` or fetch the dataset manually."
                )

            time.sleep(self._poll_interval)

    def _fetch_dataset(self, dataset_id: str) -> list[dict[str, Any]]:
        url = f"{self._base_url}/datasets/{dataset_id}/items"
        params = {"clean": "true", "format": "json"}
        try:
            r = self._session.get(url, params=params, timeout=120)
        except requests.RequestException as e:
            raise ShopifyAnalyzerError(f"Failed to download dataset: {e}") from e

        if r.status_code >= 400:
            raise ActorRunError(
                f"Apify returned HTTP {r.status_code} when fetching dataset: "
                f"{r.text[:300]}"
            )

        try:
            data = r.json()
        except ValueError as e:
            raise ActorRunError(f"Apify dataset is not valid JSON: {e}") from e

        if not isinstance(data, list):
            raise ActorRunError(
                f"Unexpected dataset payload (not a list): {type(data).__name__}"
            )
        return data
