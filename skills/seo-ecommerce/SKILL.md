---
name: seo-ecommerce
description: >
  E-commerce marketplace intelligence via DataForSEO Merchant API. Analyzes
  product listings on Google Shopping and Amazon, compares seller pricing,
  identifies marketplace keyword gaps, and checks price competitiveness.
  Use when user says "ecommerce", "product listing", "Google Shopping",
  "Amazon products", "marketplace SEO", "price comparison", "product SEO",
  "shopping feed", or "merchant data".
user-invokable: true
argument-hint: "[command] [keyword|product_id]"
license: MIT
allowed-tools: Read, Grep, Glob, Bash, WebFetch, Write
compatibility: "Requires DataForSEO Merchant API module"
metadata:
  author: AgriciDaniel
  version: "1.8.0"
  category: seo
---

# E-commerce Marketplace Intelligence

Analyze product visibility, pricing, and competitive position across
Google Shopping and Amazon using the DataForSEO Merchant API.

## Prerequisites

Requires the DataForSEO extension with the **Merchant API module** activated.
Check availability: verify `DATAFORSEO_USERNAME` and `DATAFORSEO_PASSWORD` are set
and Merchant module is enabled on your account.

## Cost Configuration

**Reference:** Load `references/merchant-api-endpoints.md` for endpoint details.
**Cost tracking:** Use `python3 scripts/dataforseo_costs.py check --command merchant-products`
before every API call. Merchant API calls are in the `warn_modules` list and
always require user confirmation.

## Quick Reference

| Command | What it does |
|---------|-------------|
| `/seo ecommerce analyze <keyword>` | Product listing analysis on Google Shopping / Amazon |
| `/seo ecommerce keyword-gap <domain> <keyword>` | Marketplace vs organic visibility gap |
| `/seo ecommerce price-check <product_id>` | Seller price competitiveness analysis |

---

## Sub-Skills

### 1. `analyze_product_listing`

Fetch and analyze product data from Google Shopping or Amazon for a keyword.

**Workflow:**
1. Run cost check: `python3 scripts/dataforseo_costs.py check --command merchant-products --limit 20`
2. If approved, fetch: `python3 scripts/dataforseo_merchant.py products "<keyword>" --marketplace google --limit 20`
3. Optionally also fetch Amazon: `python3 scripts/dataforseo_merchant.py products "<keyword>" --marketplace amazon --limit 20`
4. Analyze results:
   - Price distribution (min, max, median, percentiles)
   - Seller landscape (top sellers by frequency, rating distribution)
   - Review volume correlation with ranking position
   - Brand concentration (% of results dominated by top brands)
5. If user's domain detected in results, highlight their position

**Output:**
- Product listing table (rank, title, price, rating, reviews, seller)
- Pricing analysis (distribution stats, outliers)
- Seller landscape summary
- Competitive positioning recommendations

### 2. `marketplace_keyword_gap`

Compare a domain's product visibility in Google Shopping vs organic SERP.

**Workflow:**
1. Fetch Google Shopping results for the keyword: `scripts/dataforseo_merchant.py products`
2. Fetch organic SERP for the same keyword: `scripts/dataforseo_costs.py check --command serp` then use SERP API
3. Compare:
   - Products visible in organic but NOT in Shopping → missed marketplace revenue
   - Products visible in Shopping but NOT in organic → content opportunity
   - Products visible in both → fullest visibility, benchmark position
4. For Amazon: repeat with `--marketplace amazon`

**Output:**
- Visibility gap table (keyword, organic position, Shopping position, gap type)
- Revenue opportunity estimation based on search volume
- Actionable feed optimization recommendations

### 3. `price_competitiveness_check`

For a specific product, fetch all sellers and analyze pricing position.

**Workflow:**
1. Fetch sellers: `python3 scripts/dataforseo_merchant.py sellers <product_id>`
2. Calculate:
   - Price percentile position of the target seller
   - Price delta vs lowest, average, and median
   - Shipping cost impact on total price competitiveness
   - MAP (Minimum Advertised Price) violation detection signals
3. Fetch product specs for enriched comparison: `scripts/dataforseo_merchant.py specs`

**Output:**
- Seller comparison table (rank, seller, price, condition, shipping)
- Price percentile chart description
- Competitiveness score (0-100)
- Pricing strategy recommendations

---

## Schema Enrichment

When analyzing e-commerce pages alongside the `seo-schema` skill:
- Auto-populate `Product.offers.price` from live Merchant API data
- Add `Product.offers.seller` information
- Inject product specs as `Product.additionalProperty` entries
- Validate pricing accuracy: compare page schema price vs marketplace price

**Note:** Schema must reflect the business's OWN product data. Competitor pricing
is reported separately but never injected into the business's schema.

---

## Cross-Platform Analysis

### Google Shopping vs Amazon

| Dimension | Google Shopping | Amazon |
|-----------|----------------|--------|
| Pricing model | Free + Paid listings | Marketplace fees |
| Feed source | Merchant Center | Seller Central |
| Review system | Aggregated from web | Amazon-native |
| Schema impact | Product schema → free listings | A+ Content → SEO |
| API endpoint | `merchant/google/products` | `merchant/amazon/products` |

When both marketplaces are analyzed, provide a cross-platform comparison table
showing price differences, seller overlap, and review volume disparities.

---

## Reference Files

Load on-demand:
- `references/merchant-api-endpoints.md`: API endpoint details, params, response fields, costs

---

## Output

Generate `ECOMMERCE-ANALYSIS-{keyword}.md` with:

1. **Product Listing Table** (top 20 by relevance)
2. **Pricing Analysis** (distribution, median, percentiles)
3. **Seller Landscape** (top sellers, frequency, ratings)
4. **Marketplace Keyword Gap** (if domain provided)
5. **Price Competitiveness Score** (if product_id provided)
6. **Schema Recommendations** (Product, Offer, AggregateRating enrichment)
7. **Top 10 Prioritized Actions** (Critical > High > Medium > Low)
8. **Cost Report** (DataForSEO credits consumed)

---

## Error Handling

| Scenario | Action |
|----------|--------|
| Merchant API module not activated | Report clearly. Suggest activating the module in DataForSEO dashboard. Fall back to organic-only analysis. |
| No products found for keyword | Try broader keyword. Report "no Shopping results" and suggest product feed optimization if the user sells this product. |
| Product ID invalid for sellers/specs | Report the error. Suggest re-running products search to get valid product IDs. |
| Amazon not available in location | Report location restriction. Default to Google Shopping. |
