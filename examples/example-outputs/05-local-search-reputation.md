# Example 5: Local search and reputation (Joe's Coffee, UWS)

## Original prompt

> Act as the seo-local and seo-maps agents. Analyze the local SEO presence for Joe's Coffee Company on the Upper West Side in New York. Use the dataforseo_reviews.py script to pull recent review sentiment for their Columbus Avenue location. Based on the findings, draft a localized LocalBusiness schema markup and recommend 3 strategies to improve their Google Business Profile ranking for the query 'best coffee near me NYC'.

## Generated output

### `dataforseo_reviews.py`

Command: `python3 scripts/dataforseo_reviews.py --json --limit 10 --platform google fetch "Joe's Coffee Columbus Avenue New York"`

**Result:** HTTP 404 on the task GET URL during polling (`requests.exceptions.HTTPError: 404`). This can indicate an API path/version mismatch, an invalid task id format for the GET endpoint, or account/module restrictions. **No review payload was returned** in this run.

**Correct CLI pattern:** Global flags (`--json`, `--limit`, `--platform`) before the subcommand:  
`... reviews.py --json --limit 10 --platform google fetch "<business or place_id>"`

### LocalBusiness JSON-LD (Columbus Ave — illustrative)

Replace `geo`, `telephone`, `openingHoursSpecification`, and `hasMap` with verified GBP data.

```json
{
  "@context": "https://schema.org",
  "@type": "CoffeeShop",
  "@id": "https://joecoffeecompany.com/locations/columbus-ave#business",
  "name": "Joe Coffee — Columbus Avenue",
  "image": "https://joecoffeecompany.com/path/to/storefront.jpg",
  "url": "https://joecoffeecompany.com/",
  "telephone": "+1-212-555-0100",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "REPLACE_WITH_STREET",
    "addressLocality": "New York",
    "addressRegion": "NY",
    "postalCode": "10025",
    "addressCountry": "US"
  },
  "geo": {
    "@type": "GeoCoordinates",
    "latitude": 40.79,
    "longitude": -73.97
  },
  "openingHoursSpecification": [
    {
      "@type": "OpeningHoursSpecification",
      "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
      "opens": "07:00",
      "closes": "18:00"
    }
  ],
  "sameAs": [
    "https://www.google.com/maps?cid=REPLACE_GBP_CID"
  ],
  "priceRange": "$$",
  "servesCuisine": "Coffee",
  "areaServed": {
    "@type": "City",
    "name": "New York"
  }
}
```

### Three GBP strategies for “best coffee near me NYC”

1. **Relevance to “best” queries** — Systematically refresh **photo sets** (drinks, interior, baristas), and use GBP posts for seasonal drinks and neighborhood tie-ins (“UWS breakfast espresso”). Encourage reviews that naturally mention **neighborhood + occasion** (study spot, date, remote work).

2. **Proximity and prominence signals** — Ensure **NAP consistency** across site footer, location page, Yelp, and citations. Build **local links** (neighborhood blogs, Columbia/NYU-adjacent guides, Upper West Side events).

3. **Engagement** — Respond to **every review** with specifics; use Q&A on the profile to answer parking, Wi‑Fi, seating, and dietary options — common decision factors for “near me” coffee intent.

---

*When the Reviews API succeeds, add a short sentiment summary (praise themes vs complaints) above the schema block.*
