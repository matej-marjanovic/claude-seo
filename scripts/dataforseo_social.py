#!/usr/bin/env python3
"""DataForSEO Social Media API client for social signal analysis.

Fetches Pinterest pin counts, Reddit discussions, and Facebook shares via
the DataForSEO Social Media endpoints (Business Data API). Also uses
Content Analysis API for trend discovery.

Usage:
    dataforseo_social.py signals <url> [--platform pinterest|reddit|all]
    dataforseo_social.py reddit-opportunities <keyword> [--limit 10]
    dataforseo_social.py pinterest-trends <keyword> [--limit 10]
    dataforseo_social.py aggregate <url> [--limit 5]

Environment:
    DATAFORSEO_USERNAME  — API login
    DATAFORSEO_PASSWORD  — API password
"""

import argparse
import json
import os
import sys

try:
    import requests
except ImportError:
    print("Error: 'requests' package required. Install: pip install requests",
          file=sys.stderr)
    sys.exit(1)

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

BASE_URL = "https://api.dataforseo.com/v3"


def _get_auth():
    """Get DataForSEO credentials from environment."""
    username = os.environ.get("DATAFORSEO_USERNAME", "")
    password = os.environ.get("DATAFORSEO_PASSWORD", "")
    if not username or not password:
        print("Error: Set DATAFORSEO_USERNAME and DATAFORSEO_PASSWORD",
              file=sys.stderr)
        sys.exit(1)
    return (username, password)


def _post_live(endpoint, payload, auth):
    """Send a live POST request and return response data."""
    url = f"{BASE_URL}/{endpoint}"
    resp = requests.post(url, json=[payload], auth=auth, timeout=30)
    resp.raise_for_status()
    data = resp.json()

    if data.get("status_code") != 20000:
        msg = data.get("status_message", "Unknown error")
        print(json.dumps({"error": msg, "status_code": data.get("status_code")}))
        sys.exit(1)

    return data


def cmd_signals(args):
    """Fetch social engagement signals for a URL."""
    auth = _get_auth()
    platforms = (["pinterest", "reddit"]
                 if args.platform == "all" else [args.platform])

    all_results = {}

    for platform in platforms:
        endpoint = f"business_data/social_media/{platform}/live"
        payload = {"targets": [args.url]}

        data = _post_live(endpoint, payload, auth)

        if args.json:
            all_results[platform] = data
        else:
            from dataforseo_normalize import normalize_social
            print(normalize_social(data, platform=platform))
            print()

    if args.json:
        print(json.dumps(all_results, indent=2))


def cmd_reddit_opportunities(args):
    """Discover Reddit threads for content opportunity identification.

    Uses the Content Analysis API to find Reddit discussions about a keyword,
    then analyzes engagement patterns to identify content gaps.
    """
    auth = _get_auth()

    # Use Content Analysis search to find Reddit discussions
    endpoint = "content_analysis/search/live"
    payload = {
        "keyword": args.keyword,
        "search_mode": "as_is",
        "limit": args.limit,
        "filters": [
            "page_type", "=", "reddit_comments"
        ],
        "order_by": ["social_metrics.reddit.topic_info.comments_count,desc"],
    }

    data = _post_live(endpoint, payload, auth)

    if args.json:
        print(json.dumps(data, indent=2))
        return

    # Extract and format Reddit opportunities
    items = _extract_items(data)
    if not items:
        print("_No Reddit discussions found for this keyword._\n")
        return

    print(f"### Reddit Opportunities for \"{args.keyword}\"\n")
    print("| Subreddit | Title | Comments | Score | Content Gap |")
    print("| --- | --- | --- | --- | --- |")

    for item in items[:args.limit]:
        url_data = item.get("url", "")
        # Try to extract subreddit from URL
        subreddit = "—"
        if "reddit.com/r/" in str(url_data):
            parts = str(url_data).split("/r/")
            if len(parts) > 1:
                subreddit = "r/" + parts[1].split("/")[0]

        title = (item.get("title", "") or "")[:80]
        comments = item.get("social_metrics", {}).get(
            "reddit", {}).get("topic_info", {}).get(
            "comments_count", "—")
        score = item.get("social_metrics", {}).get(
            "reddit", {}).get("topic_info", {}).get("score", "—")

        # Identify content gap type
        gap = "Question" if "?" in title else "Discussion"
        if any(w in title.lower()
               for w in ["help", "how", "recommend", "best", "looking for"]):
            gap = "Intent Signal"

        print(f"| {subreddit} | {title} | {comments} | {score} | {gap} |")

    print(f"\n_Found {len(items)} Reddit discussions. "
          f"Focus on 'Intent Signal' threads for content gap opportunities._\n")


def cmd_pinterest_trends(args):
    """Analyze Pinterest engagement for a keyword or domain.

    Uses Content Analysis to find Pinterest-engaged content for a topic.
    """
    auth = _get_auth()

    endpoint = "content_analysis/search/live"
    payload = {
        "keyword": args.keyword,
        "search_mode": "as_is",
        "limit": args.limit,
        "order_by": ["social_metrics.pinterest.pins,desc"],
    }

    data = _post_live(endpoint, payload, auth)

    if args.json:
        print(json.dumps(data, indent=2))
        return

    items = _extract_items(data)
    if not items:
        print("_No Pinterest-engaged content found._\n")
        return

    print(f"### Pinterest Trends for \"{args.keyword}\"\n")
    print("| URL | Pins | Title | Content Type |")
    print("| --- | --- | --- | --- |")

    for item in items[:args.limit]:
        url = (item.get("url", "") or "")[:60]
        pins = item.get("social_metrics", {}).get(
            "pinterest", {}).get("pins", "—")
        title = (item.get("title", "") or "")[:50]
        page_type = item.get("page_type", "—")

        print(f"| {url} | {pins} | {title} | {page_type} |")

    print(f"\n_Top {min(len(items), args.limit)} pages by Pinterest engagement. "
          f"Analyze image formats and visual styles of top-pinned content._\n")


def cmd_aggregate(args):
    """Aggregate social signals across platforms for a URL."""
    auth = _get_auth()
    platforms = ["pinterest", "reddit"]

    print(f"### Social Signal Aggregate for {args.url}\n")
    print("| Platform | Metric | Value |")
    print("| --- | --- | --- |")

    total_signals = 0

    for platform in platforms:
        endpoint = f"business_data/social_media/{platform}/live"
        payload = {"targets": [args.url]}

        try:
            data = _post_live(endpoint, payload, auth)
            items = _extract_items(data)

            if items and len(items) > 0:
                item = items[0]
                if platform == "pinterest":
                    pins = item.get("pinterest_pins", 0) or 0
                    print(f"| Pinterest | Pins | {pins} |")
                    total_signals += pins
                elif platform == "reddit":
                    shares = item.get("reddit_shares", 0) or 0
                    print(f"| Reddit | Shares | {shares} |")
                    total_signals += shares
            else:
                print(f"| {platform.title()} | — | No data |")
        except Exception:
            print(f"| {platform.title()} | — | Error |")

    # Social presence score (simple heuristic)
    if total_signals == 0:
        score = 0
    elif total_signals < 10:
        score = 20
    elif total_signals < 50:
        score = 40
    elif total_signals < 200:
        score = 60
    elif total_signals < 1000:
        score = 80
    else:
        score = 95

    print(f"\n**Social Presence Score:** {score}/100 "
          f"(total signals: {total_signals})\n")


def _extract_items(data):
    """Extract items from DataForSEO response."""
    if not isinstance(data, dict):
        return []
    tasks = data.get("tasks", [])
    for task in tasks:
        results = task.get("result", [])
        if isinstance(results, list):
            for result in results:
                if isinstance(result, dict) and "items" in result:
                    return result.get("items", [])
    return []


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="DataForSEO Social Media API client"
    )
    parser.add_argument(
        "--platform", default="all",
        choices=["pinterest", "reddit", "all"],
        help="Social platform (default: all)"
    )
    parser.add_argument(
        "--limit", type=int, default=10,
        help="Max results (default: 10)"
    )
    parser.add_argument(
        "--json", action="store_true",
        help="Output raw JSON"
    )

    sub = parser.add_subparsers(dest="command", required=True)

    p_sig = sub.add_parser("signals", help="Fetch social signals for a URL")
    p_sig.add_argument("url", help="Target URL")

    p_red = sub.add_parser("reddit-opportunities",
                           help="Find Reddit content opportunities")
    p_red.add_argument("keyword", help="Search keyword")

    p_pin = sub.add_parser("pinterest-trends",
                           help="Analyze Pinterest engagement trends")
    p_pin.add_argument("keyword", help="Search keyword")

    p_agg = sub.add_parser("aggregate",
                           help="Aggregate social signals across platforms")
    p_agg.add_argument("url", help="Target URL")

    args = parser.parse_args()
    cmds = {
        "signals": cmd_signals,
        "reddit-opportunities": cmd_reddit_opportunities,
        "pinterest-trends": cmd_pinterest_trends,
        "aggregate": cmd_aggregate,
    }
    cmds[args.command](args)


if __name__ == "__main__":
    main()
