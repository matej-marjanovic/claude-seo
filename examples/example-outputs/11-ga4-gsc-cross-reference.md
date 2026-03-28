# Example 11: GA4 and GSC cross-reference (bounce vs technical issues)

## Original prompt

> Use the ga4_report.py script to identify which organic landing pages had the highest bounce rate over the last week. Cross-reference those URLs with gsc_inspect.py to ensure there are no mobile usability errors or indexing issues causing the poor user experience.

## Generated output

### `ga4_report.py`

Requires GA4 Data API access (`google-analytics-data`) and OAuth / service account with Viewer on the property.

Example: `python3 scripts/ga4_report.py --property YOUR_GA4_PROPERTY_ID --report organic --days 7 --json`

**Run in this environment (placeholder property, no client):**

```json
{
  "property": "123456789",
  "report": "organic_traffic",
  "date_range": null,
  "totals": {},
  "daily_data": [],
  "top_pages": [],
  "quota_tokens_used": null,
  "error": "Could not build GA4 client. Ensure the service account has Viewer access in GA4 Admin > Property Access Management."
}
```

**Workflow when configured**

1. Pull **organic landing pages** for the last 7 days with **bounce rate** (or engagement rate in GA4’s newer model — prefer `engagementRate` / `averageSessionDuration` as complements).
2. Sort by **sessions** (statistical significance) among pages with **worst bounce or lowest engagement**.
3. Take the top N URLs (e.g., 10–20).

### `gsc_inspect.py`

For each URL, run URL Inspection (requires GSC credentials):

`python3 scripts/gsc_inspect.py --site-url sc-domain:example.com --json "https://example.com/path"`

Check the JSON for:

- **Indexing state** — excluded, duplicate, crawled not indexed.
- **Mobile usability** — errors reported via Search Console.
- **Rich results / enhancements** — video, breadcrumb, etc.

### How to read the cross-reference

| Pattern | Likely cause |
|---------|----------------|
| High bounce + **Crawled — currently not indexed** | Quality or duplication signals; fix content uniqueness and internal links. |
| High bounce + **Page is indexed** + mobile errors | UX/rendering; fix viewport, tap targets, intrusive interstitials. |
| High bounce + **good GSC** | Content–intent mismatch, slow LCP, or misleading title/snippet; test SERP rewrite and on-page H1 alignment. |

---

*Configure `~/.config/claude-seo/google-api.json` and OAuth per `scripts/google_auth.py` before expecting non-empty GA4/GSC outputs.*
