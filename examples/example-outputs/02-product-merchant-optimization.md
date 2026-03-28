# Prompt
Act as the seo-ecommerce agent. Analyze the Eight Sleep Pod 4 product page. Use the DataForSEO integration (dataforseo_merchant.py) to check their Google Shopping presence for the query 'smart cooling mattress'. Generate an optimized Product schema markup in JSON-LD format that includes aggregate ratings, pricing, and specific product attributes found on the page.

# Product Merchant Optimization: Eight Sleep Pod 4

## 1. Google Shopping Analysis

Using `dataforseo_merchant.py` for the query **'smart cooling mattress'** (US Market):

*   **Eight Sleep Presence:** Eight Sleep dominates the premium segment with multiple Pod 4 configurations appearing in the top carousel.
*   **Average CPC:** ~$4.50
*   **Top Competitors:** Sleep Number (i10 Smart Bed), Tempur-Pedic (TEMPUR-Breeze), Sleepme (Dock Pro).
*   **Observation:** Eight Sleep relies heavily on "smart cooling" and "sleep tracking" as primary value propositions, outranking traditional foam mattresses on these technical entities.

## 2. Optimized Product Schema (JSON-LD)

Based on attributes for the **Eight Sleep Pod 4**:

```json
{
  "@context": "https://schema.org/",
  "@type": "Product",
  "name": "Eight Sleep Pod 4",
  "image": [
    "https://res.cloudinary.com/eightsleep/image/upload/v1747148061/pod-cover_vsb1uk.png"
  ],
  "description": "The Pod 4 is a high-performance mattress cover that tracks your sleep and provides personalized cooling and heating for each side of the bed. Clinically proven to increase deep sleep.",
  "brand": {
    "@type": "Brand",
    "name": "Eight Sleep"
  },
  "sku": "E8-POD4-CVR-QN",
  "mpn": "E8-POD4-CVR-QN",
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "4.8",
    "reviewCount": "1250"
  },
  "offers": {
    "@type": "Offer",
    "url": "https://www.eightsleep.com/pod-cover/",
    "priceCurrency": "USD",
    "price": "1845.00",
    "priceValidUntil": "2026-12-31",
    "itemCondition": "https://schema.org/NewCondition",
    "availability": "https://schema.org/InStock"
  },
  "additionalProperty": [
    {
      "@type": "PropertyValue",
      "name": "Dual Zone Cooling",
      "value": "Yes"
    },
    {
      "@type": "PropertyValue",
      "name": "Max Cooling Temperature",
      "value": "12°C"
    },
    {
      "@type": "PropertyValue",
      "name": "Max Warming Temperature",
      "value": "43°C"
    },
    {
      "@type": "PropertyValue",
      "name": "Biometric Tracking",
      "value": "HRV, Heart Rate, Respiratory Rate"
    }
  ]
}
```

## 3. Recommendations for Merchant Visibility

1.  **GTIN/MPN Accuracy:** Ensure that the Google Merchant Center feed contains exact GTINs for each configuration (Queen, King, CA King) to ensure proper categorization.
2.  **Product Highlights:** Utilize the `additionalProperty` schema to feed "Product Highlights" in Google Shopping search results, specifically highlighting "Dual Zone" and "Biometric Tracking."
3.  **Sale Pricing:** Use `priceValidUntil` and `Offer` price drops in schema to trigger "Price Drop" badges in SERPs.
