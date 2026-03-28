#!/usr/bin/env python3
"""DataForSEO Merchant API client for e-commerce marketplace intelligence.

Fetches product listings, seller comparisons, product specs, and reviews
from Google Shopping and Amazon via the DataForSEO Merchant API.

Usage:
    dataforseo_merchant.py products <keyword> [--marketplace google|amazon]
    dataforseo_merchant.py sellers <product_id> [--marketplace google]
    dataforseo_merchant.py specs <product_id> [--marketplace google]
    dataforseo_merchant.py reviews <product_id> [--marketplace google]

Environment:
    DATAFORSEO_USERNAME  — API login
    DATAFORSEO_PASSWORD  — API password
"""

import argparse
import json
import os
import sys
import time

try:
    import requests
except ImportError:
    print("Error: 'requests' package required. Install: pip install requests",
          file=sys.stderr)
    sys.exit(1)

# Lazy import of normalizer (same directory)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

BASE_URL = "https://api.dataforseo.com/v3"

# Endpoint mapping: (marketplace, command) -> endpoint path
ENDPOINTS = {
    ("google", "products"): "merchant/google/products/task_post",
    ("google", "products_get"): "merchant/google/products/task_get/advanced",
    ("google", "sellers"): "merchant/google/sellers/task_post",
    ("google", "sellers_get"): "merchant/google/sellers/task_get/advanced",
    ("google", "specs"): "merchant/google/product_spec/task_post",
    ("google", "specs_get"): "merchant/google/product_spec/task_get/advanced",
    ("google", "reviews"): "merchant/google/product_reviews/task_post",
    ("google", "reviews_get"): "merchant/google/product_reviews/task_get/advanced",
    ("amazon", "products"): "merchant/amazon/products/task_post",
    ("amazon", "products_get"): "merchant/amazon/products/task_get/advanced",
    ("amazon", "sellers"): "merchant/amazon/sellers/task_post",
    ("amazon", "sellers_get"): "merchant/amazon/sellers/task_get/advanced",
    ("amazon", "reviews"): "merchant/amazon/reviews/task_post",
    ("amazon", "reviews_get"): "merchant/amazon/reviews/task_get/advanced",
}


def _get_auth():
    """Get DataForSEO credentials from environment."""
    username = os.environ.get("DATAFORSEO_USERNAME", "")
    password = os.environ.get("DATAFORSEO_PASSWORD", "")
    if not username or not password:
        print("Error: Set DATAFORSEO_USERNAME and DATAFORSEO_PASSWORD",
              file=sys.stderr)
        sys.exit(1)
    return (username, password)


def _post_task(endpoint, payload, auth):
    """Submit a task to DataForSEO and return task ID."""
    url = f"{BASE_URL}/{endpoint}"
    resp = requests.post(url, json=[payload], auth=auth, timeout=30)
    resp.raise_for_status()
    data = resp.json()

    if data.get("status_code") != 20000:
        msg = data.get("status_message", "Unknown error")
        print(json.dumps({"error": msg, "status_code": data.get("status_code")}))
        sys.exit(1)

    tasks = data.get("tasks", [])
    if not tasks:
        print(json.dumps({"error": "No tasks returned"}))
        sys.exit(1)

    return tasks[0].get("id")


def _get_results(endpoint, task_id, auth, max_wait=60):
    """Poll for task results."""
    url = f"{BASE_URL}/{endpoint}/{task_id}"
    for _ in range(max_wait // 3):
        time.sleep(3)
        resp = requests.get(url, auth=auth, timeout=30)
        resp.raise_for_status()
        data = resp.json()

        tasks = data.get("tasks", [])
        if tasks and tasks[0].get("status_code") == 20000:
            results = tasks[0].get("result", [])
            if results:
                return data
        elif tasks and tasks[0].get("status_code") == 40601:
            # Still processing
            continue
        elif tasks and tasks[0].get("status_code", 0) >= 40000:
            msg = tasks[0].get("status_message", "Task failed")
            print(json.dumps({"error": msg}))
            sys.exit(1)

    print(json.dumps({"error": "Timeout waiting for results"}))
    sys.exit(1)


def cmd_products(args):
    """Search for products on Google Shopping or Amazon."""
    auth = _get_auth()
    marketplace = args.marketplace
    endpoint_post = ENDPOINTS.get((marketplace, "products"))
    endpoint_get = ENDPOINTS.get((marketplace, "products_get"))

    if not endpoint_post:
        print(json.dumps({"error": f"Unsupported marketplace: {marketplace}"}))
        sys.exit(1)

    payload = {
        "keyword": args.query,
        "location_code": args.location,
        "language_code": args.language,
        "depth": args.limit,
    }

    task_id = _post_task(endpoint_post, payload, auth)
    data = _get_results(endpoint_get, task_id, auth)

    if args.json:
        print(json.dumps(data, indent=2))
    else:
        from dataforseo_normalize import normalize_merchant
        print(normalize_merchant(data, max_rows=args.limit,
                                 marketplace=marketplace))


def cmd_sellers(args):
    """Get sellers for a specific product."""
    auth = _get_auth()
    marketplace = args.marketplace
    endpoint_post = ENDPOINTS.get((marketplace, "sellers"))
    endpoint_get = ENDPOINTS.get((marketplace, "sellers_get"))

    if not endpoint_post:
        print(json.dumps({"error": f"Sellers not available for {marketplace}"}))
        sys.exit(1)

    payload = {
        "product_id": args.product_id,
        "location_code": args.location,
        "language_code": args.language,
    }

    task_id = _post_task(endpoint_post, payload, auth)
    data = _get_results(endpoint_get, task_id, auth)

    if args.json:
        print(json.dumps(data, indent=2))
    else:
        from dataforseo_normalize import normalize_merchant_sellers
        print(normalize_merchant_sellers(data, max_rows=args.limit))


def cmd_specs(args):
    """Get product specifications."""
    auth = _get_auth()
    endpoint_post = ENDPOINTS.get((args.marketplace, "specs"))
    endpoint_get = ENDPOINTS.get((args.marketplace, "specs_get"))

    if not endpoint_post:
        print(json.dumps({"error": "Specs only available for Google Shopping"}))
        sys.exit(1)

    payload = {
        "product_id": args.product_id,
        "location_code": args.location,
        "language_code": args.language,
    }

    task_id = _post_task(endpoint_post, payload, auth)
    data = _get_results(endpoint_get, task_id, auth)
    print(json.dumps(data, indent=2))


def cmd_reviews(args):
    """Get product reviews from marketplace."""
    auth = _get_auth()
    marketplace = args.marketplace
    endpoint_post = ENDPOINTS.get((marketplace, "reviews"))
    endpoint_get = ENDPOINTS.get((marketplace, "reviews_get"))

    if not endpoint_post:
        print(json.dumps({"error": f"Reviews not available for {marketplace}"}))
        sys.exit(1)

    payload = {
        "product_id": args.product_id,
        "location_code": args.location,
        "language_code": args.language,
        "depth": args.limit,
    }

    task_id = _post_task(endpoint_post, payload, auth)
    data = _get_results(endpoint_get, task_id, auth)

    if args.json:
        print(json.dumps(data, indent=2))
    else:
        from dataforseo_normalize import normalize_reviews
        print(normalize_reviews(data, platform=marketplace,
                                max_rows=args.limit))


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="DataForSEO Merchant API client"
    )
    parser.add_argument(
        "--marketplace", default="google",
        choices=["google", "amazon"],
        help="Marketplace to query (default: google)"
    )
    parser.add_argument(
        "--location", type=int, default=2840,
        help="Location code (default: 2840 = US)"
    )
    parser.add_argument(
        "--language", default="en",
        help="Language code (default: en)"
    )
    parser.add_argument(
        "--limit", type=int, default=20,
        help="Max results (default: 20)"
    )
    parser.add_argument(
        "--json", action="store_true",
        help="Output raw JSON instead of Markdown"
    )

    sub = parser.add_subparsers(dest="command", required=True)

    p_prod = sub.add_parser("products", help="Search products")
    p_prod.add_argument("query", help="Search keyword")

    p_sell = sub.add_parser("sellers", help="Get sellers for a product")
    p_sell.add_argument("product_id", help="Product ID from products search")

    p_spec = sub.add_parser("specs", help="Get product specifications")
    p_spec.add_argument("product_id", help="Product ID")

    p_rev = sub.add_parser("reviews", help="Get product reviews")
    p_rev.add_argument("product_id", help="Product ID")

    args = parser.parse_args()
    cmds = {
        "products": cmd_products,
        "sellers": cmd_sellers,
        "specs": cmd_specs,
        "reviews": cmd_reviews,
    }
    cmds[args.command](args)


if __name__ == "__main__":
    main()
