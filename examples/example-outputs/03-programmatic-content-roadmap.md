# Example 3: Programmatic content roadmap (PostHog)

## Original prompt

> Act as the seo-plan and seo-programmatic agents. Generate a 3-month programmatic SEO content plan for posthog.com targeting 'product analytics' and 'open source session replay' keywords. Use the keyword_planner.py script to fetch search volumes for these core terms, and suggest 10 high-intent, bottom-of-funnel comparison pages (e.g., 'PostHog vs [Competitor]').

## Generated output

### `keyword_planner.py` (volume)

Command: `python3 scripts/keyword_planner.py volume "product analytics,open source session replay" --json`

**Result:** Google Ads client could not be built in this environment (`google-ads` library and/or Ads API config missing). JSON error payload:

```json
{
  "keywords": [],
  "error": "Could not build Google Ads client."
}
```

**To run for real volumes:** Install `google-ads`, add `ads_developer_token`, `ads_customer_id`, and OAuth paths per `scripts/keyword_planner.py` header, then re-run `volume` or `ideas`.

### 3-month programmatic plan (illustrative)

**Month 1 — Foundation**

- Publish hub: `/product-analytics` and `/session-replay` with clear definitions, use cases, and internal links to comparison pages.
- Ship 3 comparison pages: PostHog vs Amplitude, vs Mixpanel, vs Heap (feature matrix + pricing framing + open-source angle where true).

**Month 2 — Scale comparisons + templates**

- Add 4 comparisons: vs Pendo, vs FullStory, vs LogRocket, vs Matomo (position open source + self-host + CDP overlap honestly).
- Programmatic component: one JSON or CMS-driven “vs” template (meta title pattern: `PostHog vs {{Competitor}}: {{Primary differentiator}}`).

**Month 3 — Long-tail and proof**

- Remaining 3 comparisons: vs Plausible (if relevant to scope), vs GA4, vs “build vs buy” for analytics stacks.
- Add mini-tools or embeddable diagrams (funnels, replay privacy) that earn links and support head terms.

### Ten high-intent comparison page ideas

1. PostHog vs Amplitude — warehouse / ownership / pricing
2. PostHog vs Mixpanel — event model and governance
3. PostHog vs Heap — autocapture vs explicit tracking
4. PostHog vs FullStory — session replay + product analytics
5. PostHog vs LogRocket — engineering vs growth buyer
6. PostHog vs Pendo — product analytics vs in-app guides
7. PostHog vs Matomo — open source analytics positioning
8. PostHog vs Google Analytics 4 — privacy, self-host, event limits
9. PostHog vs OpenReplay — open source session replay niche
10. PostHog vs “CDP + analytics” bundles — when to consolidate vs best-of-breed

Each page should include: honest feature table, migration notes, pricing dimension, and a primary CTA (trial / docs / book demo).
