# ASO Best Practices

> Load this reference when auditing app store listings or planning ASO strategy.

## Platform Field Limits

### Google Play

| Field | Limit | ASO Impact |
|-------|-------|-----------|
| Title | 50 chars | High — primary ranking signal |
| Short description | 80 chars | Medium — visible in search results |
| Long description | 4,000 chars | Medium — keyword indexing |
| Package name | 150 chars | Low — set at creation, cannot change |
| Developer name | 64 chars | Low |
| Screenshots | 4–8 per device type | High — conversion rate impact |
| Feature graphic | 1024×500 px | Medium — Play Store header |
| Icon | 512×512 px | Medium — click-through rate |
| Promo video | YouTube link (30s–2min) | Medium — engagement |
| Tags | Up to 5 | Medium — categorization |

### Apple App Store

| Field | Limit | ASO Impact |
|-------|-------|-----------|
| Title | 30 chars | High — primary ranking signal |
| Subtitle | 30 chars | High — visible under title, indexed |
| Keywords field | 100 chars (comma-separated) | High — hidden field, indexed for search |
| Description | 4,000 chars | Low — NOT indexed for search |
| Promotional text | 170 chars | Low — not indexed, rotatable |
| Screenshots | 3–10 per device | High — conversion rate |
| App preview video | Up to 3, 15–30s each | Medium |
| Icon | 1024×1024 px | Medium |
| In-app purchases | 20 promoted | Low |

## Ranking Factor Weights (Industry Consensus)

| Factor | Google Play | Apple App Store |
|--------|------------|----------------|
| Title keywords | 25% | 30% |
| Short desc / Subtitle | 15% | 20% |
| Long desc / Keywords field | 10% | 15% |
| Rating (average) | 15% | 10% |
| Review volume | 10% | 5% |
| Download velocity | 10% | 10% |
| Update frequency | 5% | 5% |
| Uninstall rate | 5% | — |
| Engagement (DAU/MAU) | 5% | 5% |

## Keyword Density Recommendations

### Title
- Include primary keyword once, naturally
- Brand name + primary keyword is ideal format
- Example: "Calm - Meditation & Sleep" (keyword: meditation)

### Short Description (Google Play) / Subtitle (Apple)
- Include 1-2 secondary keywords
- Keep readable — conversion matters more than keyword stuffing

### Long Description (Google Play)
- Target keyword appears 3-5 times (natural density ~0.5-1%)
- First 3 lines are most impactful (visible before "Read more")
- Use bullet points for scannability

### Keywords Field (Apple Only)
- Use all 100 characters — no spaces after commas
- Don't repeat words from title or subtitle (Apple already indexes those)
- Use singular forms (Apple matches both singular and plural)
- Don't include "app" or the category name

## Screenshot Best Practices

- First 2 screenshots are "above the fold" in search results — most critical
- Show core features, not onboarding screens
- Include text overlays explaining benefits (not features)
- Use device-appropriate dimensions

| Device | Dimensions |
|--------|-----------|
| iPhone 6.7" | 1290 × 2796 |
| iPhone 6.5" | 1284 × 2778 |
| iPad Pro 12.9" | 2048 × 2732 |
| Android Phone | 1080 × 1920 (min) |
| Android Tablet | 1200 × 1920 (min) |

## Review Impact

- Rating < 3.5★: significant negative impact on conversion and ranking
- Rating 4.0-4.5★: optimal range (perceived as reliable)
- Rating > 4.8★: may trigger "too good" skepticism but improves ranking
- Review velocity matters: consistent weekly reviews > burst of reviews
- Response to reviews improves rating trend over time

## Localization Priority

For maximum reach with minimum effort:

| Priority | Languages | Coverage |
|----------|-----------|----------|
| P0 | English (US) | ~25% of global app users |
| P1 | Chinese (Simplified), Japanese, Korean | +20% |
| P2 | Spanish, Portuguese, French, German | +15% |
| P3 | Russian, Arabic, Hindi, Indonesian | +10% |

## DataForSEO App Data API Endpoints

| Endpoint | Purpose | Cost |
|----------|---------|------|
| `app_data/google/app_searches/task_post` | Keyword search on Google Play | $0.001 (std) |
| `app_data/apple/app_searches/task_post` | Keyword search on App Store | $0.001 (std) |
| `app_data/google/app_list/task_post` | Category/collection list | $0.001 (std) |
| `app_data/google/app_info/task_post` | Single app details | $0.002 (live) |
| `app_data/apple/app_info/task_post` | Single app details | $0.002 (live) |
| `app_data/google/app_reviews/task_post` | App reviews | $0.001 (std) |
| `app_data/apple/app_reviews/task_post` | App reviews | $0.001 (std) |
