# Example 4: Entity and NLP content optimization (PostHog)

## Original prompt

> Use the nlp_analyze.py script to analyze the top 5 ranking pages for 'self-hosted product analytics'. Compare those NLP entities against PostHog's current landing page. Provide a brief outlining the missing entities and semantic keywords they need to add to their content to improve topical authority.

## Generated output

### `nlp_analyze.py` on PostHog homepage

Command: `python3 scripts/nlp_analyze.py --url https://posthog.com/ --json`

**Result:** No Google Cloud Natural Language API key configured:

```json
{
  "text_length": 4039,
  "language": "en",
  "entities": [],
  "sentiment": null,
  "categories": [],
  "moderation": [],
  "error": "No API key. Set GOOGLE_API_KEY or add 'api_key' to config.",
  "source_url": "https://posthog.com/",
  "extracted_text_length": 4039
}
```

**Next step for full workflow:** Set `GOOGLE_API_KEY` with Natural Language API enabled, then run `nlp_analyze.py --url` on each of the top 5 SERP URLs for `self-hosted product analytics` and diff entity lists.

### Brief: likely entity and semantic gaps (expert inference)

For a query like **self-hosted product analytics**, ranking pages often cluster around:

**Entities / concepts to cover explicitly**

- Self-hosting, on-prem, VPC / private cloud, air-gapped or compliance-heavy deployments
- Event pipeline, SDKs, API, data export to warehouse (Snowflake, BigQuery, Redshift)
- GDPR, HIPAA, SOC2 (only if accurate for the product)
- Competitor/alternative framing: Matomo, Plausible, Umami, OpenTelemetry, “build your own”
- Session replay, feature flags, experimentation — if part of the same stack story

**Semantic phrases to weave in (examples)**

- “deploy on your own infrastructure”
- “customer-owned data” / “data residency”
- “open source analytics” + “hosting options”
- “product analytics without sending data to third-party SaaS”

**Content moves**

- Add a dedicated section or page that maps **deployment models** (cloud vs self-hosted) to buyer questions.
- Use comparison tables that name **direct alternatives** in the self-hosted space (not only big SaaS incumbents).
- Add **schema-appropriate** FAQs (implementation time, scaling, upgrades) to capture related questions.

Re-run NLP comparison after edits to confirm entity coverage moves toward the SERP centroid.
