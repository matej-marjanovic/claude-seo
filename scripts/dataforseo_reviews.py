#!/usr/bin/env python3
"""DataForSEO Reviews API client for cross-platform review intelligence.

Fetches reviews from Google, Trustpilot, and Tripadvisor. Computes review
velocity, formats reviews for LLM-based sentiment analysis, and generates
cross-platform comparison tables.

Usage:
    dataforseo_reviews.py fetch <business> [--platform google|trustpilot|tripadvisor|all]
    dataforseo_reviews.py velocity <business> [--window 90]
    dataforseo_reviews.py sentiment <business> [--platform google] [--limit 20]
    dataforseo_reviews.py compare <business>

Environment:
    DATAFORSEO_USERNAME  — API login
    DATAFORSEO_PASSWORD  — API password
"""

import argparse
import json
import os
import sys
import time
from datetime import datetime, timedelta

try:
    import requests
except ImportError:
    print("Error: 'requests' package required. Install: pip install requests",
          file=sys.stderr)
    sys.exit(1)

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

BASE_URL = "https://api.dataforseo.com/v3"

# Platform to endpoint mapping
PLATFORM_ENDPOINTS = {
    "google": {
        "post": "business_data/google/reviews/task_post",
        "get": "business_data/google/reviews/task_get/advanced",
        "id_param": "place_id",  # or "keyword"
    },
    "trustpilot": {
        "post": "business_data/trustpilot/reviews/task_post",
        "get": "business_data/trustpilot/reviews/task_get/advanced",
        "id_param": "domain",
    },
    "tripadvisor": {
        "post": "business_data/tripadvisor/reviews/task_post",
        "get": "business_data/tripadvisor/reviews/task_get/advanced",
        "id_param": "url",
    },
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
    """Submit a task to DataForSEO."""
    url = f"{BASE_URL}/{endpoint}"
    resp = requests.post(url, json=[payload], auth=auth, timeout=30)
    resp.raise_for_status()
    data = resp.json()

    if data.get("status_code") != 20000:
        msg = data.get("status_message", "Unknown error")
        print(json.dumps({"error": msg}))
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
            continue
        elif tasks and tasks[0].get("status_code", 0) >= 40000:
            msg = tasks[0].get("status_message", "Task failed")
            print(json.dumps({"error": msg}))
            sys.exit(1)

    print(json.dumps({"error": "Timeout waiting for results"}))
    sys.exit(1)


def _extract_items(data):
    """Extract items from DataForSEO response."""
    tasks = data.get("tasks", [])
    for task in tasks:
        results = task.get("result", [])
        if isinstance(results, list):
            for result in results:
                if isinstance(result, dict) and "items" in result:
                    return result.get("items", [])
    return []


def fetch_reviews(business, platform, limit, auth):
    """Fetch reviews from a single platform."""
    config = PLATFORM_ENDPOINTS.get(platform)
    if not config:
        return {"platform": platform, "error": f"Unsupported platform: {platform}",
                "items": []}

    payload = {
        config["id_param"]: business,
        "depth": limit,
    }

    if platform == "google":
        # Google also accepts keyword-based search
        if not business.startswith("ChI") and not business.startswith("0x"):
            payload = {"keyword": business, "depth": limit}

    task_id = _post_task(config["post"], payload, auth)
    data = _get_results(config["get"], task_id, auth)
    items = _extract_items(data)

    return {"platform": platform, "items": items, "raw": data}


def cmd_fetch(args):
    """Fetch reviews from specified platform(s)."""
    auth = _get_auth()
    platforms = (["google", "trustpilot", "tripadvisor"]
                 if args.platform == "all" else [args.platform])

    for platform in platforms:
        result = fetch_reviews(args.business, platform, args.limit, auth)

        if args.json:
            print(json.dumps(result["raw"], indent=2))
        else:
            from dataforseo_normalize import normalize_reviews
            print(normalize_reviews(result["raw"], platform=platform,
                                    max_rows=args.limit))
            print()


def cmd_velocity(args):
    """Calculate review velocity (reviews per month)."""
    auth = _get_auth()
    platforms = (["google", "trustpilot", "tripadvisor"]
                 if args.platform == "all" else [args.platform])

    print("### Review Velocity Analysis\n")

    for platform in platforms:
        result = fetch_reviews(args.business, platform, args.limit, auth)
        items = result.get("items", [])

        if not items:
            print(f"**{platform.title()}:** No reviews found\n")
            continue

        # Parse timestamps and calculate velocity
        dates = []
        for item in items:
            ts = (item.get("timestamp") or item.get("datetime")
                  or item.get("time_ago"))
            if ts:
                try:
                    if isinstance(ts, str) and len(ts) >= 10:
                        dates.append(datetime.fromisoformat(ts[:10]))
                except (ValueError, TypeError):
                    pass

        if len(dates) < 2:
            print(f"**{platform.title()}:** Insufficient date data "
                  f"({len(dates)} reviews with dates)\n")
            continue

        dates.sort()
        window_start = datetime.now() - timedelta(days=args.window)
        recent = [d for d in dates if d >= window_start]
        months = args.window / 30.0

        velocity = len(recent) / months if months > 0 else 0

        # 18-day rule check
        gaps = []
        for i in range(1, len(dates)):
            gap = (dates[i] - dates[i - 1]).days
            gaps.append(gap)
        max_gap = max(gaps) if gaps else 0
        avg_gap = sum(gaps) / len(gaps) if gaps else 0

        # Check 18-day rule (Google may flag businesses with
        # review gaps > 18 days)
        eighteen_day_pass = max_gap <= 18

        print(f"**{platform.title()}:**")
        print(f"| Metric | Value |")
        print(f"| --- | --- |")
        print(f"| Reviews in last {args.window} days | {len(recent)} |")
        print(f"| Velocity (reviews/month) | {velocity:.1f} |")
        print(f"| Max gap between reviews | {max_gap} days |")
        print(f"| Avg gap between reviews | {avg_gap:.0f} days |")
        print(f"| 18-day rule compliance | "
              f"{'✅ Pass' if eighteen_day_pass else '❌ Fail — gap > 18 days'} |")
        print()


def cmd_sentiment(args):
    """Output reviews formatted for LLM sentiment analysis.

    Instead of calling the DataForSEO Content Analysis API, this outputs
    the review text in a structured format that the LLM agent can analyze
    directly. This saves ~$0.02/call vs the API approach.
    """
    auth = _get_auth()
    result = fetch_reviews(args.business, args.platform, args.limit, auth)
    items = result.get("items", [])

    if not items:
        print("_No reviews found for sentiment analysis._")
        return

    print(f"### {args.platform.title()} Reviews for LLM Sentiment Analysis\n")
    print("Analyze the following reviews. For each, classify sentiment as "
          "POSITIVE, NEUTRAL, or NEGATIVE. Then provide:\n"
          "1. Overall sentiment distribution (%)\n"
          "2. Top 3 positive themes\n"
          "3. Top 3 negative themes\n"
          "4. Actionable recommendations\n")
    print("---\n")

    for i, item in enumerate(items[:args.limit], 1):
        rating = (item.get("rating", {}).get("value")
                  if isinstance(item.get("rating"), dict)
                  else item.get("rating", "?"))
        text = (item.get("review_text", "") or item.get("text", "")).strip()
        author = (item.get("profile_name", "") or item.get("author", "")
                  or "Anonymous")
        date = item.get("timestamp", item.get("datetime", ""))
        if date and len(str(date)) >= 10:
            date = str(date)[:10]

        if text:
            # Truncate very long reviews but keep more than table truncation
            if len(text) > 500:
                text = text[:497] + "…"
            print(f"**Review {i}** | Rating: {rating}★ | By: {author} "
                  f"| Date: {date}")
            print(f"> {text}\n")

    print("---\n_Analyze the reviews above and provide sentiment summary._\n")


def cmd_compare(args):
    """Cross-platform review comparison."""
    auth = _get_auth()
    platforms = ["google", "trustpilot", "tripadvisor"]

    print("### Cross-Platform Review Comparison\n")
    print("| Platform | Reviews | Avg Rating | Response Rate |")
    print("| --- | --- | --- | --- |")

    for platform in platforms:
        try:
            result = fetch_reviews(args.business, platform, args.limit, auth)
            items = result.get("items", [])
        except Exception:
            print(f"| {platform.title()} | _Error_ | — | — |")
            continue

        if not items:
            print(f"| {platform.title()} | 0 | — | — |")
            continue

        ratings = []
        responded = 0
        for item in items:
            val = (item.get("rating", {}).get("value")
                   if isinstance(item.get("rating"), dict)
                   else item.get("rating"))
            if val is not None:
                try:
                    ratings.append(float(val))
                except (ValueError, TypeError):
                    pass
            if (item.get("owner_answer") or item.get("response")):
                responded += 1

        avg = sum(ratings) / len(ratings) if ratings else 0
        resp_rate = (f"{responded / len(items) * 100:.0f}%"
                     if items else "—")

        print(f"| {platform.title()} | {len(items)} | "
              f"{avg:.1f}★ | {resp_rate} |")

    print()


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="DataForSEO Reviews API client"
    )
    parser.add_argument(
        "--platform", default="google",
        choices=["google", "trustpilot", "tripadvisor", "all"],
        help="Review platform (default: google)"
    )
    parser.add_argument(
        "--limit", type=int, default=40,
        help="Max reviews to fetch (default: 40)"
    )
    parser.add_argument(
        "--json", action="store_true",
        help="Output raw JSON"
    )
    parser.add_argument(
        "--window", type=int, default=90,
        help="Velocity analysis window in days (default: 90)"
    )

    sub = parser.add_subparsers(dest="command", required=True)

    p_fetch = sub.add_parser("fetch", help="Fetch reviews")
    p_fetch.add_argument("business", help="Business name, place_id, or domain")

    p_vel = sub.add_parser("velocity", help="Review velocity analysis")
    p_vel.add_argument("business", help="Business name or place_id")

    p_sent = sub.add_parser("sentiment",
                            help="Reviews formatted for LLM sentiment")
    p_sent.add_argument("business", help="Business name or place_id")

    p_comp = sub.add_parser("compare", help="Cross-platform comparison")
    p_comp.add_argument("business", help="Business name")

    args = parser.parse_args()
    cmds = {
        "fetch": cmd_fetch,
        "velocity": cmd_velocity,
        "sentiment": cmd_sentiment,
        "compare": cmd_compare,
    }
    cmds[args.command](args)


if __name__ == "__main__":
    main()
