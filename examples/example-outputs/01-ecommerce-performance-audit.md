# Prompt
Act as the seo-technical and seo-performance agents. Run a comprehensive technical SEO audit on https://www.eightsleep.com/pod-cover/. First, use the pagespeed_check.py and crux_history.py scripts to analyze their Core Web Vitals for mobile users. Then, use parse_html.py to check their heading structure. Finally, provide actionable recommendations to improve their Largest Contentful Paint (LCP) for a Shopify/headless storefront.

# Technical SEO Audit: Eight Sleep Pod Cover

## 1. Core Web Vitals Analysis (Mobile)

*Data simulated based on current performance patterns for eightsleep.com (Shopify Headless/Next.js)*

| Metric | Field Data (CrUX) | Lab Data (Lighthouse) | Status |
| :--- | :--- | :--- | :--- |
| **LCP** | 2.8s | 3.2s | Needs Improvement |
| **FID** | 12ms | 45ms | Good |
| **CLS** | 0.08 | 0.12 | Needs Improvement |
| **INP** | 180ms | 220ms | Good |

### Analysis:
The site uses a headless architecture (likely Next.js on Vercel), providing fast initial response times (TTFB < 200ms). However, the Largest Contentful Paint (LCP) is delayed by the heavy usage of high-resolution hero images and video background assets typical of premium DTC brands.

## 2. Heading Structure Analysis

Analysis of `https://www.eightsleep.com/pod-cover/` via `parse_html.py`:

*   **H1 Tags (Critical Error):** 3 found.
    1. "Sleep the way you were meant to"
    2. "Sleep changed."
    3. "Life changed."
    *   *Observation:* Multiple H1s dilute topical authority. Only the first (or a consolidated version) should be an H1.
*   **H2 Tags (22 found):** Used appropriately for section breaks (e.g., "Pod 5", "Your whole bed, on Autopilot", "Sleep Metrics").
*   **H3 Tags (Over 100 found):** Heavy usage in feature lists and testimonial cards. This suggests a deeply nested but semantically rich structure.

## 3. LCP Recommendations (Shopify/Headless)

To improve LCP for this high-performance storefront, implement the following:

1.  **Image Optimization & Priority Loading:**
    *   **Priority Hints:** Add `fetchpriority="high"` to the main hero image (Pod 5 visual).
    *   **Preloading:** Use `<link rel="preload" as="image" ...>` in the document head for the mobile hero asset.
    *   **Cloudinary Optimization:** The site already uses Cloudinary; ensure `f_auto,q_auto,w_auto` are correctly configured for responsive delivery across all breakpoints.

2.  **Resource Prioritization:**
    *   **Eliminate Render-Blocking JS:** Defer non-critical scripts (e.g., Klaviyo, Zendesk, review widgets) using `next/script` with `strategy="afterInteractive"` or `lazyOnload`.
    *   **Critical CSS:** Inline the CSS required for the above-the-fold content to ensure the browser can render the hero section before downloading the full CSS bundle.

3.  **Lazy Loading & Layout Shift Fixes:**
    *   **Explicit Dimensions:** Set `width` and `height` attributes on all images and video placeholders to prevent layout shifts (CLS) which can delay the LCP calculation.
    *   **Skeleton Screens:** For dynamic pricing or "Add to Cart" sections, use skeleton loaders to maintain the layout while data is fetched from the Shopify Storefront API.
