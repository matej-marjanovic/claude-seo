# Example 1: E-commerce performance audit (Eight Sleep)

## Original prompt

> Act as the seo-technical and seo-performance agents. Run a comprehensive technical SEO audit on https://www.eightsleep.com/pod-cover/. First, use the pagespeed_check.py and crux_history.py scripts to analyze their Core Web Vitals for mobile users. Then, use parse_html.py to check their heading structure. Finally, provide actionable recommendations to improve their Largest Contentful Paint (LCP) for a Shopify/headless storefront.

## Generated output

### Script execution (this environment)

**`pagespeed_check.py` (mobile, JSON)** — PageSpeed Insights returned a quota error (shared API key / rate limits):

```json
{
  "url": "https://www.eightsleep.com/pod-cover/",
  "psi": {
    "mobile": {
      "error": "PSI rate limit exceeded (240 QPM / 25,000 QPD). Wait and retry."
    }
  },
  "crux": null,
  "error": "PSI rate limit exceeded (240 QPM / 25,000 QPD). Wait and retry."
}
```

**`crux_history.py` (PHONE)** — Requires a Google API key (`GOOGLE_API_KEY` or config):  
`Error: API key required. Use --api-key or configure GOOGLE_API_KEY.`

**`parse_html.py`** — Page fetched with `fetch_page.py`, then parsed. Summary of heading structure:

| Element | Finding |
|--------|---------|
| **Title** | Eight Sleep \| Bed and Blanket Cooling System |
| **H1 count** | 3 — "Sleep the way you were meant to", "Sleep changed.", "Life changed." |
| **H2** | 22 headings (includes product pillars: Pod 5, Temperature, Sound, Elevation, Alarms, Sleep Metrics, testimonials, install section) |
| **H3** | 131 headings (deep feature grid; many repeated blocks for feature lists) |
| **Word count** | ~3,504 |
| **Canonical** | `https://www.eightsleep.com/pod-cover/` |

Full JSON extract is large; the pattern above is what a technical audit would flag first.

### Actionable LCP recommendations (Shopify / headless)

1. **Hero LCP element** — Ensure the largest above-the-fold image (or video poster) uses **priority/preload**, modern formats (AVIF/WebP), and dimensions to avoid layout thrash. On headless stacks, avoid loading full marketing carousels before the hero is painted.
2. **Third-party and tag weight** — Defer non-critical analytics, chat, and A/B snippets below the fold or after `requestIdleCallback` / interaction.
3. **Font strategy** — Subset fonts, use `font-display: swap` or optional, and avoid blocking CSS from the critical path.
4. **Server / CDN** — Strong TTFB and edge caching for HTML and hero assets; for Shopify, review app embeds and theme sections that inject render-blocking scripts.
5. **Re-run CWV** — With `GOOGLE_API_KEY` set, re-run `pagespeed_check.py` and `crux_history.py` to get lab + field LCP numbers and trend lines.

---

*Note: Full PSI/CrUX numbers require API access and quota; heading data was produced from a live fetch at generation time.*
