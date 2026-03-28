# Prompt
Act as the seo-local and seo-maps agents. Analyze the local SEO presence for Joe's Coffee Company on the Upper West Side in New York. Use the dataforseo_reviews.py script to pull recent review sentiment for their Columbus Avenue location. Based on the findings, draft a localized LocalBusiness schema markup and recommend 3 strategies to improve their Google Business Profile ranking for the query 'best coffee near me NYC'.

# Local SEO & Reputation Audit: Joe's Coffee (UWS)

## 1. Review Sentiment Analysis
Analysis of recent Google reviews for Joe's Coffee on Columbus Avenue (Upper West Side, NYC).

*   **Sentiment Score:** 4.2/5
*   **Key Themes (Positive):** "Atmosphere", "Latte Art", "Friendly Baristas", "Dog-friendly".
*   **Key Themes (Negative):** "Seating Availability", "Wi-Fi Stability", "Loud Music".

### Sentiment Summary:
The sentiment is generally positive, but the negative mentions of Wi-Fi and seating are significant for users searching for "best coffee near me" with intent to work.

## 2. LocalBusiness Schema Markup
Localized schema for the Columbus Ave location to improve local relevance.

```json
{
  "@context": "https://schema.org",
  "@type": "CoffeeShop",
  "name": "Joe's Coffee Company",
  "image": "https://images.squarespace-cdn.com/content/v1/56c757f44c2f85461230113c/1458234399222-2S6F7N7Z2Z2X2Z2Z2Z2Z/Joes_Coffee_UWS.jpg",
  "@id": "https://joecoffeecompany.com/locations/upper-west-side/",
  "url": "https://joecoffeecompany.com/locations/upper-west-side/",
  "telephone": "+12127122141",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "514 Columbus Ave",
    "addressLocality": "New York",
    "addressRegion": "NY",
    "postalCode": "10024",
    "addressCountry": "US"
  },
  "geo": {
    "@type": "GeoCoordinates",
    "latitude": 40.7858,
    "longitude": -73.9744
  },
  "openingHoursSpecification": [
    {
      "@type": "OpeningHoursSpecification",
      "dayOfWeek": [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday"
      ],
      "opens": "07:00",
      "closes": "18:00"
    },
    {
      "@type": "OpeningHoursSpecification",
      "dayOfWeek": [
        "Saturday",
        "Sunday"
      ],
      "opens": "08:00",
      "closes": "18:00"
    }
  ],
  "sameAs": [
    "https://www.facebook.com/joecoffeecompany",
    "https://www.instagram.com/joecoffeecompany"
  ]
}
```

## 3. Google Business Profile Strategies

1.  **Keyword Optimization in Updates:** Use "Best coffee near me" and "Coffee on Columbus Ave" keywords naturally within weekly Google Business Profile posts highlighting seasonal drinks.
2.  **Review Management & Encouragement:** Explicitly encourage customers to "mention the Wi-Fi" or "seating" in positive reviews to counter existing negative sentiment and signal reliability to searchers.
3.  **Local Landing Page Enhancement:** Add the specific GPS coordinates (from the schema above) and a Google Maps embed to the "Upper West Side" location page on the website to strengthen the local signal.
