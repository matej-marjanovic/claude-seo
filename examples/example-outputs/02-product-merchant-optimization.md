# Example 2: Product and merchant optimization (Eight Sleep / Google Shopping)

## Original prompt

> Act as the seo-ecommerce agent. Analyze the Eight Sleep Pod 4 product page. Use the DataForSEO integration (dataforseo_merchant.py) to check their Google Shopping presence for the query 'smart cooling mattress'. Generate an optimized Product schema markup in JSON-LD format that includes aggregate ratings, pricing, and specific product attributes found on the page.

## Generated output

### DataForSEO Merchant API (`dataforseo_merchant.py`)

Command attempted (correct global-flag order for this CLI):

`python3 scripts/dataforseo_merchant.py --json --limit 5 --marketplace google products "smart cooling mattress"`

**Result:** `{"error": "Task In Queue."}` — the Merchant module uses async task posting; in this run the client exited before results were ready (queue/processing). With a successful response, you would normalize or inspect Shopping titles, prices, and seller cards for Eight Sleep vs competitors.

**Setup:** `DATAFORSEO_USERNAME` and `DATAFORSEO_PASSWORD` must be set; the Merchant module must be enabled on the DataForSEO account.

### Product JSON-LD (illustrative template)

Below is **example** JSON-LD for a mattress cooling product line. **Replace** `sku`, `price`, `priceCurrency`, `availability`, `aggregateRating`, and `url` with values from your live PDP and Merchant Center feed. Only include `aggregateRating` if you have compliant, crawlable ratings on the page.

```json
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "Eight Sleep Pod — Cooling & Heating Sleep System",
  "description": "Temperature-controlled sleep system with dual-zone cooling and heating, sleep tracking, and smart alarms. Fits your existing mattress.",
  "image": [
    "https://www.eightsleep.com/path/to/hero-1200.jpg",
    "https://www.eightsleep.com/path/to/lifestyle-1200.jpg"
  ],
  "sku": "POD-COVER-REPLACE",
  "brand": {
    "@type": "Brand",
    "name": "Eight Sleep"
  },
  "category": "Home & Garden > Bedding > Mattress Toppers",
  "offers": {
    "@type": "Offer",
    "url": "https://www.eightsleep.com/pod-cover/",
    "priceCurrency": "USD",
    "price": "0.00",
    "availability": "https://schema.org/InStock",
    "itemCondition": "https://schema.org/NewCondition",
    "seller": {
      "@type": "Organization",
      "name": "Eight Sleep"
    }
  },
  "additionalProperty": [
    {
      "@type": "PropertyValue",
      "name": "Temperature range",
      "value": "Cools to 55°F, warms to 110°F (per marketing copy — verify)"
    },
    {
      "@type": "PropertyValue",
      "name": "Zones",
      "value": "Dual-zone climate control"
    },
    {
      "@type": "PropertyValue",
      "name": "Compatibility",
      "value": "Works with existing mattress"
    },
    {
      "@type": "PropertyValue",
      "name": "Features",
      "value": "Sleep tracking, snoring detection, smart alarms, elevation (verify per SKU)"
    }
  ],
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "4.7",
    "reviewCount": "1234"
  }
}
```

**Merchant + schema checklist**

- Align `price`, `availability`, and `sku` with **Google Merchant Center** feed.
- Expose ratings only if they match **visible** on-page review content and policy.
- Use `hasMerchantReturnPolicy` / `shippingDetails` when implementing full Shopping structured data per Google docs.
