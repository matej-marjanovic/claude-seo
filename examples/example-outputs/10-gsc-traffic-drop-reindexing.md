# Example 10: GSC traffic drop diagnosis and re-indexing (The Athletic)

## Original prompt

> Use the gsc_query.py script to pull the top 20 queries driving traffic to the 'Premier League News' directory over the last 30 days. Identify any articles with high impressions but a CTR below 2%. For the lowest performing article, rewrite the Title Tag and Meta Description to improve CTR, and then trigger the indexing_notify.py script to immediately notify Google of the updated URL.

## Generated output

### `gsc_query.py`

Search Analytics requires OAuth / service account access to a real GSC property. Example command shape:

`python3 scripts/gsc_query.py query --property sc-domain:theathletic.com --days 30 --dimensions query,page --limit 20 --json`

**Run in this environment (no credentials):**

```json
{
  "property": "sc-domain:theathletic.com",
  "rows": [],
  "totals": {
    "clicks": 0,
    "impressions": 0,
    "ctr": 0,
    "position": 0
  },
  "quick_wins": [],
  "row_count": 0,
  "error": "Could not build GSC service. Check service account credentials."
}
```

With access, filter `page` URLs containing the Premier League news directory path (exact path from your site structure), sort by impressions, and flag `ctr < 0.02`.

### Illustrative CTR diagnosis

| Signal | Interpretation |
|--------|----------------|
| High impressions, CTR &lt; 2% | Title/meta may be generic vs SERP intent; weak differentiation vs news pack; possible date freshness perception. |
| High position, low CTR | Rewrite title to match **query language** (fixtures, injuries, table, transfers) and add **specific hook** (exclusive, updated time). |

### Example meta rewrite (fictional article)

**Assume URL:** `https://theathletic.com/football/premier-league/news/example-slug/`  
**Assume query:** “premier league injuries this week”

**Before (illustrative weak snippet)**  
- Title: `Premier League News \| The Athletic`  
- Meta: `Read the latest Premier League news on The Athletic.`

**After**  
- Title: `Premier League injury round-up: who’s out, doubts, and return dates (updated)`  
- Meta: `Club-by-club Premier League injury news: confirmed absences, doubts, and expected return timelines—updated for matchweek planning.`

### `indexing_notify.py`

Notifies the **Indexing API** (quota 200/day; officially aimed at JobPosting / video structured data — see script docstring).

Example: `python3 scripts/indexing_notify.py https://theathletic.com/football/premier-league/news/example-slug/`

**This run:** Skipped without Google Indexing API OAuth credentials. After deploy, use URL Inspection in GSC plus normal sitemap crawl as the primary publisher workflow; Indexing API as an optional accelerator where policy allows.

---

*Replace property, paths, and article slugs with real GSC data before acting on rewrites.*
