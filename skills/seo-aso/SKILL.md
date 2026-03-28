---
name: seo-aso
description: >
  App Store Optimization (ASO) skill via DataForSEO App Data API. Tracks
  app keyword rankings on Google Play and Apple App Store, analyzes
  competitor apps, and audits store listings against ASO best practices.
  Use when user says "ASO", "app store optimization", "app ranking",
  "Google Play SEO", "Apple App Store", "app keywords", or "mobile app".
user-invokable: true
argument-hint: "[command] [keyword|app_id]"
license: MIT
allowed-tools: Read, Grep, Glob, Bash, WebFetch, Write
compatibility: "Requires DataForSEO App Data API module"
metadata:
  author: AgriciDaniel
  version: "1.8.0"
  category: seo
---

# App Store Optimization (ASO)

Analyze app visibility, keyword rankings, and store listing quality on
Google Play and Apple App Store using the DataForSEO App Data API.

## Prerequisites

Requires the DataForSEO extension with the **App Data API module** activated.
Check availability: verify `DATAFORSEO_USERNAME` / `DATAFORSEO_PASSWORD` are set
and App Data module is enabled on your account.

## Cost Configuration

**Reference:** Load `references/aso-best-practices.md` for platform-specific guidance.
**Cost tracking:** Use `python3 scripts/dataforseo_costs.py check --command app-search`
before API calls. App Data calls are in the `warn_modules` list.

## Quick Reference

| Command | What it does |
|---------|-------------|
| `/seo aso search <keyword>` | App keyword ranking on Google Play / App Store |
| `/seo aso analyze <app_id>` | Competitor analysis for a specific app |
| `/seo aso audit <app_id>` | Store listing optimization audit |

---

## Sub-Skills

### 1. `app_keyword_tracking`

Search Google Play or Apple App Store for a keyword and track which apps rank.

**Workflow:**
1. Cost check: `python3 scripts/dataforseo_costs.py check --command app-search --limit 20`
2. If approved, call DataForSEO App Searches endpoint via MCP or REST:
   - Google Play: `app_data/google/app_searches/task_post`
   - Apple: `app_data/apple/app_searches/task_post`
3. Parameters: `keyword`, `location_code=2840`, `language_code=en`, `depth=20`
4. Normalize results: app title, developer, rating, reviews count, installs, price
5. If target app provided, highlight its position in results

**Output:**
- Ranked app listing table
- Keyword-to-app visibility matrix (if multiple keywords)
- Position tracking recommendations

### 2. `app_competitor_analysis`

Given an app ID, fetch detailed info and compare with category peers.

**Workflow:**
1. Fetch target app info via App Info endpoint: `app_data/google/app_info/task_post`
2. Fetch category list via App List endpoint (same category): `app_data/google/app_list/task_post`
3. Compare across dimensions:
   - Rating (average, distribution)
   - Review count (total, velocity)
   - Update frequency (last_update_date)
   - Size and version
   - Price model (free/paid/freemium)
4. Generate competitive landscape table

**Output:**
- App comparison table (target vs top 5 competitors)
- Feature gap analysis
- Rating and review velocity comparison
- Update cadence assessment

### 3. `store_listing_optimization`

Audit an app's store listing against ASO best practices.

**Workflow:**
1. Fetch app info via App Info endpoint
2. Score each element against platform-specific limits:

| Element | Google Play | Apple App Store | Weight |
|---------|------------|----------------|--------|
| Title | 50 chars max | 30 chars max | 20% |
| Short description | 80 chars max | Subtitle: 30 chars | 15% |
| Long description | 4,000 chars | 4,000 chars | 15% |
| Screenshots | Min 4, up to 8 | Min 3, up to 10 | 15% |
| Icon | 512×512 px | 1024×1024 px | 5% |
| Rating | ≥4.0 target | ≥4.0 target | 15% |
| Review volume | Relative to category | Relative to category | 10% |
| Update recency | Within 90 days | Within 90 days | 5% |

3. Check keyword presence in title, short description, and long description
4. Evaluate screenshot quality signals (count, ordering)
5. Assess review health: volume, velocity, sentiment (via LLM analysis)
6. Generate ASO Score (0-100) with dimension breakdown

**Output:**
- ASO Score (0-100) with per-dimension breakdown
- Field-by-field audit table
- Keyword density analysis
- Screenshot optimization recommendations
- Prioritized action items (Critical > High > Medium > Low)

---

## Schema Integration

When an app also has a web presence, recommend `MobileApplication` schema:
- Use templates from `schema/templates.json` (MobileApplication iOS/Android entries)
- Cross-reference app metadata with website schema for entity consistency
- Ensure `downloadUrl`, `operatingSystem`, `applicationCategory` match across platforms

---

## Cross-Skill Delegation

- For website SEO: recommend `/seo page <url>` or `/seo audit <url>`
- For keyword research: recommend `/seo dataforseo keywords <seed>`
- For schema validation: recommend `/seo schema <url>`
- For content quality (app landing page): recommend `/seo content <url>`

---

## Reference Files

Load on-demand:
- `references/aso-best-practices.md`: Platform limits, ranking factors, localization guidance

---

## Output

Generate `ASO-AUDIT-{app_name}.md` with:

1. **ASO Score** (0-100) with dimension breakdown
2. **App Info Table** (title, developer, rating, reviews, installs, category)
3. **Keyword Rankings** (keywords tracked and positions)
4. **Competitor Comparison** (top 5 by category)
5. **Listing Audit** (field-by-field compliance check)
6. **Top 10 Prioritized Actions** (Critical > High > Medium > Low)
7. **Cost Report** (DataForSEO credits consumed)

---

## Error Handling

| Scenario | Action |
|----------|--------|
| App Data module not activated | Report clearly. Fall back to manual store listing review via WebFetch. |
| App ID not found | Suggest searching by keyword first to find correct app_id. |
| Apple data unavailable | Some Apple endpoints are more restricted. Report and fall back to Google Play. |
| No reviews for sentiment | Report insufficient data. Score review dimension as "N/A". |
