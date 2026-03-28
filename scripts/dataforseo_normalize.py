#!/usr/bin/env python3
"""DataForSEO JSON-to-Markdown normalizer.

Converts raw DataForSEO API responses into compact Markdown tables that
minimize token usage when passed to LLM agents. Used as a library by
other DataForSEO scripts and as a standalone CLI.

Usage (CLI):
    dataforseo_normalize.py --module merchant --input response.json
    dataforseo_normalize.py --module reviews --input response.json --max-rows 10
    dataforseo_normalize.py --module app_data --input response.json
    dataforseo_normalize.py --module social --input response.json

Usage (library):
    from dataforseo_normalize import normalize_merchant, normalize_reviews
    md = normalize_merchant(json_data)
"""

import argparse
import json
import sys
from typing import Any


# ---------------------------------------------------------------------------
# Generic helpers
# ---------------------------------------------------------------------------

def _trunc(text: str, max_len: int = 120) -> str:
    """Truncate text to *max_len* chars, appending '…' if trimmed."""
    if not text:
        return ""
    text = str(text).replace("\n", " ").replace("\r", "").strip()
    if len(text) <= max_len:
        return text
    return text[: max_len - 1] + "…"


def _fmt_price(value: Any, currency: str = "USD") -> str:
    """Format a price value with currency symbol."""
    if value is None:
        return "N/A"
    try:
        num = float(value)
        return f"${num:,.2f}" if currency == "USD" else f"{num:,.2f} {currency}"
    except (ValueError, TypeError):
        return str(value)


def _fmt_number(value: Any) -> str:
    """Format a numeric value with appropriate precision."""
    if value is None:
        return "N/A"
    try:
        num = float(value)
        if num == int(num):
            return f"{int(num):,}"
        return f"{num:,.1f}"
    except (ValueError, TypeError):
        return str(value)


def _fmt_rating(value: Any) -> str:
    """Format a rating value (0-5 scale)."""
    if value is None:
        return "—"
    try:
        return f"{float(value):.1f}★"
    except (ValueError, TypeError):
        return str(value)


def _fmt_date(value: Any) -> str:
    """Shorten ISO timestamp to YYYY-MM-DD."""
    if not value:
        return "—"
    s = str(value)
    return s[:10] if len(s) >= 10 else s


def _safe_get(obj: dict, *keys: str, default: Any = None) -> Any:
    """Safely traverse nested dict keys."""
    current = obj
    for k in keys:
        if isinstance(current, dict):
            current = current.get(k, default)
        else:
            return default
    return current


def json_to_table(data: list[dict], columns: list[tuple[str, str]],
                  max_rows: int = 20) -> str:
    """Convert a list of dicts into a Markdown table.

    Args:
        data: List of row dicts.
        columns: List of (key, header_label) tuples.
        max_rows: Maximum rows to include.

    Returns:
        Markdown table string.
    """
    if not data:
        return "_No data available._\n"

    rows = data[:max_rows]
    headers = [label for _, label in columns]
    header_line = "| " + " | ".join(headers) + " |"
    sep_line = "| " + " | ".join("---" for _ in columns) + " |"

    lines = [header_line, sep_line]
    for row in rows:
        cells = []
        for key, _ in columns:
            val = row.get(key, "—")
            cells.append(str(val) if val is not None else "—")
        lines.append("| " + " | ".join(cells) + " |")

    if len(data) > max_rows:
        lines.append(f"\n_Showing {max_rows} of {len(data)} results._")

    return "\n".join(lines) + "\n"


def truncate_for_context(markdown: str, max_chars: int = 8000) -> str:
    """Truncate Markdown output to fit context window budget.

    Preserves headers and top rows, truncates from the bottom.
    """
    if len(markdown) <= max_chars:
        return markdown
    # Keep the first max_chars characters, find last complete line
    truncated = markdown[:max_chars]
    last_newline = truncated.rfind("\n")
    if last_newline > 0:
        truncated = truncated[:last_newline]
    return truncated + "\n\n_…output truncated to fit context window._\n"


# ---------------------------------------------------------------------------
# Module-specific normalizers
# ---------------------------------------------------------------------------

def normalize_merchant(json_data: dict, max_rows: int = 20,
                       marketplace: str = "google") -> str:
    """Normalize Merchant API product/seller responses to Markdown.

    Handles both Google Shopping and Amazon product data.
    """
    items = _extract_items(json_data)
    if not items:
        return "_No merchant data returned._\n"

    rows = []
    for item in items[:max_rows]:
        row = {
            "rank": _safe_get(item, "rank_group", default="—"),
            "title": _trunc(_safe_get(item, "title", default=""), 80),
            "price": _fmt_price(
                _safe_get(item, "price", "current", default=None)
                or _safe_get(item, "price", default=None),
                _safe_get(item, "price", "currency", default="USD")
                or _safe_get(item, "currency", default="USD"),
            ),
            "rating": _fmt_rating(_safe_get(item, "rating", "value",
                                            default=None)
                                  or _safe_get(item, "rating", default=None)),
            "reviews": _fmt_number(_safe_get(item, "rating", "reviews_count",
                                             default=None)
                                   or _safe_get(item, "reviews_count",
                                                default=None)),
            "seller": _trunc(_safe_get(item, "seller", default="")
                             or _safe_get(item, "marketplace", default=""), 30),
            "url": _trunc(_safe_get(item, "url", default=""), 60),
        }
        rows.append(row)

    title = ("Google Shopping" if marketplace == "google"
             else "Amazon" if marketplace == "amazon"
             else marketplace.title())
    header = f"### {title} Product Listings\n\n"
    table = json_to_table(rows, [
        ("rank", "#"),
        ("title", "Product"),
        ("price", "Price"),
        ("rating", "Rating"),
        ("reviews", "Reviews"),
        ("seller", "Seller"),
        ("url", "URL"),
    ], max_rows=max_rows)

    return header + table


def normalize_merchant_sellers(json_data: dict, max_rows: int = 20) -> str:
    """Normalize Merchant API sellers response to Markdown."""
    items = _extract_items(json_data)
    if not items:
        return "_No seller data returned._\n"

    rows = []
    for item in items[:max_rows]:
        row = {
            "rank": _safe_get(item, "position", default="—"),
            "seller": _trunc(_safe_get(item, "title", default="")
                             or _safe_get(item, "seller_name", default=""), 40),
            "price": _fmt_price(_safe_get(item, "price", "current",
                                          default=None)
                                or _safe_get(item, "price", default=None)),
            "condition": _safe_get(item, "condition", default="—"),
            "shipping": _safe_get(item, "delivery_info", default="—"),
            "url": _trunc(_safe_get(item, "url", default=""), 60),
        }
        rows.append(row)

    header = "### Seller Comparison\n\n"
    table = json_to_table(rows, [
        ("rank", "#"),
        ("seller", "Seller"),
        ("price", "Price"),
        ("condition", "Condition"),
        ("shipping", "Shipping"),
        ("url", "URL"),
    ], max_rows=max_rows)

    return header + table


def normalize_reviews(json_data: dict, platform: str = "google",
                      max_rows: int = 20) -> str:
    """Normalize Reviews API response to Markdown.

    Works for Google, Trustpilot, and Tripadvisor reviews.
    """
    items = _extract_items(json_data)
    if not items:
        return f"_No {platform} reviews returned._\n"

    rows = []
    for item in items[:max_rows]:
        row = {
            "date": _fmt_date(_safe_get(item, "timestamp", default=None)
                              or _safe_get(item, "time_ago", default=None)
                              or _safe_get(item, "datetime", default=None)),
            "rating": _fmt_rating(_safe_get(item, "rating", "value",
                                            default=None)
                                  or _safe_get(item, "rating", default=None)),
            "text": _trunc(_safe_get(item, "review_text", default="")
                           or _safe_get(item, "text", default=""), 120),
            "author": _trunc(_safe_get(item, "profile_name", default="")
                             or _safe_get(item, "author", default="")
                             or _safe_get(item, "reviewer", default=""), 25),
            "response": "✅" if _safe_get(item, "owner_answer", default=None)
                        or _safe_get(item, "response", default=None)
                        else "—",
        }
        rows.append(row)

    title = platform.title()
    header = f"### {title} Reviews\n\n"
    table = json_to_table(rows, [
        ("date", "Date"),
        ("rating", "Rating"),
        ("author", "Author"),
        ("text", "Review"),
        ("response", "Response"),
    ], max_rows=max_rows)

    return header + table


def normalize_review_summary(reviews: list[dict],
                             platform: str = "all") -> str:
    """Generate a review health summary from normalized review data."""
    if not reviews:
        return "_No reviews available for summary._\n"

    total = len(reviews)
    ratings = []
    for r in reviews:
        val = (_safe_get(r, "rating", "value", default=None)
               or _safe_get(r, "rating", default=None))
        if val is not None:
            try:
                ratings.append(float(val))
            except (ValueError, TypeError):
                pass

    avg_rating = sum(ratings) / len(ratings) if ratings else 0
    five_star = sum(1 for r in ratings if r >= 4.5)
    one_star = sum(1 for r in ratings if r <= 1.5)

    lines = [
        f"### Review Health Summary ({platform.title()})\n",
        f"| Metric | Value |",
        f"| --- | --- |",
        f"| Total Reviews | {total} |",
        f"| Average Rating | {avg_rating:.1f}★ |",
        f"| 5-Star Rate | {five_star}/{total} ({five_star/total*100:.0f}%) |"
        if total > 0 else "",
        f"| 1-Star Rate | {one_star}/{total} ({one_star/total*100:.0f}%) |"
        if total > 0 else "",
        "",
    ]
    return "\n".join(line for line in lines if line is not None) + "\n"


def normalize_app_data(json_data: dict, max_rows: int = 20) -> str:
    """Normalize App Data API responses (search/list/info) to Markdown."""
    items = _extract_items(json_data)
    if not items:
        return "_No app data returned._\n"

    rows = []
    for item in items[:max_rows]:
        row = {
            "rank": _safe_get(item, "rank_group", default="—"),
            "title": _trunc(_safe_get(item, "title", default=""), 50),
            "developer": _trunc(_safe_get(item, "developer", default="")
                                or _safe_get(item, "author", default=""), 25),
            "rating": _fmt_rating(_safe_get(item, "rating", default=None)),
            "reviews": _fmt_number(_safe_get(item, "reviews_count",
                                             default=None)),
            "installs": _safe_get(item, "installs", default="—"),
            "price": _fmt_price(_safe_get(item, "price", default=0)),
            "category": _trunc(_safe_get(item, "category", default=""), 20),
        }
        rows.append(row)

    header = "### App Store Results\n\n"
    table = json_to_table(rows, [
        ("rank", "#"),
        ("title", "App"),
        ("developer", "Developer"),
        ("rating", "Rating"),
        ("reviews", "Reviews"),
        ("installs", "Installs"),
        ("price", "Price"),
        ("category", "Category"),
    ], max_rows=max_rows)

    return header + table


def normalize_app_info(json_data: dict) -> str:
    """Normalize a single app's detailed info to Markdown."""
    items = _extract_items(json_data)
    if not items:
        return "_No app info returned._\n"

    app = items[0] if isinstance(items, list) else items

    lines = [
        "### App Details\n",
        "| Field | Value |",
        "| --- | --- |",
        f"| Title | {_safe_get(app, 'title', default='—')} |",
        f"| Developer | {_safe_get(app, 'developer', default='—')} |",
        f"| Rating | {_fmt_rating(_safe_get(app, 'rating', default=None))} |",
        f"| Reviews | {_fmt_number(_safe_get(app, 'reviews_count', default=None))} |",
        f"| Installs | {_safe_get(app, 'installs', default='—')} |",
        f"| Price | {_fmt_price(_safe_get(app, 'price', default=0))} |",
        f"| Category | {_safe_get(app, 'category', default='—')} |",
        f"| Last Updated | {_fmt_date(_safe_get(app, 'last_update_date', default=None))} |",
        f"| Version | {_safe_get(app, 'version', default='—')} |",
        f"| Content Rating | {_safe_get(app, 'content_rating', default='—')} |",
        "",
    ]

    desc = _safe_get(app, "description", default="")
    if desc:
        lines.append(f"**Description:** {_trunc(desc, 300)}\n")

    return "\n".join(lines) + "\n"


def normalize_social(json_data: dict, platform: str = "all",
                     max_rows: int = 20) -> str:
    """Normalize Social Media API responses to Markdown.

    Handles Pinterest, Reddit, and Facebook data.
    """
    items = _extract_items(json_data)
    if not items:
        return f"_No {platform} social data returned._\n"

    if platform == "pinterest" or _is_pinterest(items):
        return _normalize_pinterest(items, max_rows)
    elif platform == "reddit" or _is_reddit(items):
        return _normalize_reddit(items, max_rows)
    else:
        return _normalize_social_generic(items, platform, max_rows)


def _normalize_pinterest(items: list[dict], max_rows: int = 20) -> str:
    """Normalize Pinterest social media data."""
    rows = []
    for item in items[:max_rows]:
        row = {
            "url": _trunc(_safe_get(item, "url", default="")
                          or _safe_get(item, "page_url", default=""), 60),
            "pins": _fmt_number(_safe_get(item, "pinterest_pins",
                                          default=None)
                                or _safe_get(item, "pins_count",
                                             default=None)),
            "repins": _fmt_number(_safe_get(item, "repins_count",
                                            default=None)),
        }
        rows.append(row)

    header = "### Pinterest Signals\n\n"
    table = json_to_table(rows, [
        ("url", "URL"),
        ("pins", "Pins"),
        ("repins", "Repins"),
    ], max_rows=max_rows)

    return header + table


def _normalize_reddit(items: list[dict], max_rows: int = 20) -> str:
    """Normalize Reddit social media data."""
    rows = []
    for item in items[:max_rows]:
        row = {
            "subreddit": _safe_get(item, "subreddit", default="—"),
            "title": _trunc(_safe_get(item, "title", default=""), 60),
            "score": _fmt_number(_safe_get(item, "score", default=None)
                                 or _safe_get(item, "reddit_shares",
                                              default=None)),
            "comments": _fmt_number(_safe_get(item, "comments_count",
                                              default=None)),
            "author": _safe_get(item, "author", default="—"),
            "permalink": _trunc(_safe_get(item, "permalink", default=""), 50),
        }
        rows.append(row)

    header = "### Reddit Signals\n\n"
    table = json_to_table(rows, [
        ("subreddit", "Subreddit"),
        ("title", "Title"),
        ("score", "Score"),
        ("comments", "Comments"),
        ("author", "Author"),
        ("permalink", "Link"),
    ], max_rows=max_rows)

    return header + table


def _normalize_social_generic(items: list[dict], platform: str,
                              max_rows: int = 20) -> str:
    """Normalize generic social media data."""
    rows = []
    for item in items[:max_rows]:
        row = {
            "url": _trunc(_safe_get(item, "url", default="")
                          or _safe_get(item, "page_url", default=""), 60),
            "metric": (_safe_get(item, "social_media_tag", default="")
                       or platform),
            "value": _fmt_number(
                _safe_get(item, "count", default=None)
                or _safe_get(item, "shares", default=None)
                or _safe_get(item, "engagement", default=None)
            ),
        }
        rows.append(row)

    header = f"### {platform.title()} Signals\n\n"
    table = json_to_table(rows, [
        ("url", "URL"),
        ("metric", "Metric"),
        ("value", "Value"),
    ], max_rows=max_rows)

    return header + table


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _extract_items(json_data: dict) -> list[dict]:
    """Extract the items array from a DataForSEO response.

    DataForSEO responses nest results under tasks[0].result[0].items
    or similar paths. This tries common patterns.
    """
    if not isinstance(json_data, dict):
        if isinstance(json_data, list):
            return json_data
        return []

    # Direct items key
    if "items" in json_data and isinstance(json_data["items"], list):
        return json_data["items"]

    # tasks[].result[].items
    tasks = json_data.get("tasks", [])
    for task in tasks:
        results = task.get("result", [])
        if isinstance(results, list):
            for result in results:
                if isinstance(result, dict) and "items" in result:
                    return result.get("items", [])

    # Flat result array
    if "result" in json_data:
        result = json_data["result"]
        if isinstance(result, list):
            if result and isinstance(result[0], dict) and "items" in result[0]:
                return result[0].get("items", [])
            return result

    return []


def _is_pinterest(items: list[dict]) -> bool:
    """Detect if items are Pinterest data."""
    if not items:
        return False
    sample = items[0]
    return ("pinterest_pins" in sample or "pins_count" in sample
            or "repins_count" in sample)


def _is_reddit(items: list[dict]) -> bool:
    """Detect if items are Reddit data."""
    if not items:
        return False
    sample = items[0]
    return ("subreddit" in sample or "reddit_shares" in sample
            or "permalink" in sample)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="DataForSEO JSON-to-Markdown normalizer"
    )
    parser.add_argument(
        "--module",
        required=True,
        choices=["merchant", "merchant_sellers", "reviews", "review_summary",
                 "app_data", "app_info", "social"],
        help="DataForSEO module to normalize",
    )
    parser.add_argument(
        "--input",
        required=True,
        help="Path to JSON response file (or '-' for stdin)",
    )
    parser.add_argument(
        "--max-rows",
        type=int,
        default=20,
        help="Maximum rows to include (default: 20)",
    )
    parser.add_argument(
        "--platform",
        default="google",
        help="Platform hint for reviews/social (google, trustpilot, "
             "tripadvisor, pinterest, reddit)",
    )
    parser.add_argument(
        "--marketplace",
        default="google",
        choices=["google", "amazon"],
        help="Marketplace for merchant module (default: google)",
    )
    parser.add_argument(
        "--max-chars",
        type=int,
        default=8000,
        help="Max output chars for context window safety (default: 8000)",
    )

    args = parser.parse_args()

    # Read input
    if args.input == "-":
        raw = sys.stdin.read()
    else:
        with open(args.input) as f:
            raw = f.read()

    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON input: {e}", file=sys.stderr)
        sys.exit(1)

    # Dispatch to normalizer
    normalizers = {
        "merchant": lambda d: normalize_merchant(d, args.max_rows,
                                                 args.marketplace),
        "merchant_sellers": lambda d: normalize_merchant_sellers(d,
                                                                 args.max_rows),
        "reviews": lambda d: normalize_reviews(d, args.platform,
                                               args.max_rows),
        "review_summary": lambda d: normalize_review_summary(
            _extract_items(d), args.platform),
        "app_data": lambda d: normalize_app_data(d, args.max_rows),
        "app_info": lambda d: normalize_app_info(d),
        "social": lambda d: normalize_social(d, args.platform, args.max_rows),
    }

    output = normalizers[args.module](data)
    output = truncate_for_context(output, args.max_chars)
    print(output)


if __name__ == "__main__":
    main()
