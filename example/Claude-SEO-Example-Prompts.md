# **🚀 claude-seo: Example Prompts & Workflows**

This library contains practical, real-world examples demonstrating the full capabilities of the claude-seo plugin. These examples are tailored for mid-sized businesses, startups, local chains, and e-commerce brands, ensuring the workflows are directly applicable to scaling companies.

## **🛒 1\. E-commerce & Technical SEO**

**Target Profile:** Mid-to-Large D2C Brands (e.g., [Eight Sleep](https://www.eightsleep.com))

**Capabilities Showcased:** Core Web Vitals, Google Merchant Center, Technical Parsing, Schema Generation.

**Prompt Example 1: The E-commerce Performance Audit**

"Act as the seo-technical and seo-performance agents. Run a comprehensive technical SEO audit on https://www.eightsleep.com/pod-cover/. First, use the pagespeed\_check.py and crux\_history.py scripts to analyze their Core Web Vitals for mobile users. Then, use parse\_html.py to check their heading structure. Finally, provide actionable recommendations to improve their Largest Contentful Paint (LCP) for a Shopify/headless storefront."

**Prompt Example 2: Product & Merchant Optimization**

"Act as the seo-ecommerce agent. Analyze the Eight Sleep Pod 4 product page. Use the DataForSEO integration (dataforseo\_merchant.py) to check their Google Shopping presence for the query 'smart cooling mattress'. Generate an optimized Product schema markup in JSON-LD format that includes aggregate ratings, pricing, and specific product attributes found on the page."

## **💻 2\. B2B SaaS & Content Strategy**

**Target Profile:** B2B SaaS & Open Source (e.g., [PostHog](https://posthog.com))

**Capabilities Showcased:** Keyword Planning, NLP Analysis, Programmatic SEO, Competitor Analysis.

**Prompt Example 3: Programmatic Content Roadmap**

"Act as the seo-plan and seo-programmatic agents. Generate a 3-month programmatic SEO content plan for posthog.com targeting 'product analytics' and 'open source session replay' keywords. Use the keyword\_planner.py script to fetch search volumes for these core terms, and suggest 10 high-intent, bottom-of-funnel comparison pages (e.g., 'PostHog vs \[Competitor\]')."

**Prompt Example 4: Entity & NLP Content Optimization**

"Use the nlp\_analyze.py script to analyze the top 5 ranking pages for 'self-hosted product analytics'. Compare those NLP entities against PostHog's current landing page. Provide a brief outlining the missing entities and semantic keywords they need to add to their content to improve topical authority."

## **☕ 3\. Local SEO & Google Maps**

**Target Profile:** Multi-location Local Businesses (e.g., [Joe's Coffee Company NYC](https://joecoffeecompany.com/))

**Capabilities Showcased:** Google Maps optimization, Review Sentiment, Local Schema.

**Prompt Example 5: Local Search & Reputation Analysis**

"Act as the seo-local and seo-maps agents. Analyze the local SEO presence for Joe's Coffee Company on the Upper West Side in New York. Use the dataforseo\_reviews.py script to pull recent review sentiment for their Columbus Avenue location. Based on the findings, draft a localized LocalBusiness schema markup and recommend 3 strategies to improve their Google Business Profile ranking for the query 'best coffee near me NYC'."

## **📱 4\. App Store Optimization (ASO) & YouTube**

**Target Profile:** Consumer Mobile Apps (e.g., [AllTrails](https://www.alltrails.com/))

**Capabilities Showcased:** App Store Optimization, YouTube Search, Social SEO.

**Prompt Example 6: ASO Keyword Expansion**

"Act as the seo-aso agent. Analyze the primary keyword 'hiking trail maps' for the iOS App Store and Google Play Store. Suggest an optimized App Title (max 30 characters), Subtitle, and a backend keyword list for the AllTrails app to maximize their visibility against competitors like Strava and Komoot."

**Prompt Example 7: YouTube Video SEO Strategy**

"Use the Youtube.py script to analyze the top 5 ranking videos for 'beginner hiking gear guide'. Break down their title structures, description formats, and tag optimizations. Propose a YouTube SEO strategy for AllTrails' official channel to rank for this query, including a suggested video title, description, and timestamp chapters."

## **🎨 5\. Visual SEO & AI Image Generation**

**Target Profile:** Modern CPG / Food & Beverage (e.g., [Magic Spoon](https://magicspoon.com/))

**Capabilities Showcased:** Screenshot Capture, Visual Layout Analysis, Gemini Image Generation.

**Prompt Example 8: Above-the-Fold Visual Analysis**

"Use capture\_screenshot.py to grab the homepage of https://magicspoon.com and run it through analyze\_visual.py. Evaluate their above-the-fold layout, Call-to-Action placement, and visual hierarchy. Based on your findings, what layout adjustments would improve their conversion rate and SEO engagement metrics?"

**Prompt Example 9: Generating SEO-Optimized Assets**

"Act as the seo-image-gen agent. Based on Magic Spoon's playful, high-protein cereal brand identity, use the Banana extension to generate 3 optimized hero image concepts suitable for a new 'Keto-Friendly Breakfast' landing page. Include the exact alt text and descriptive filenames I should use for these images to maximize Google Images traffic."

## **📈 6\. Search Console & Indexing Operations**

**Target Profile:** Digital Publishers & Content Sites (e.g., [The Athletic](https://theathletic.com/))

**Capabilities Showcased:** GSC API integration, Indexing API, Query Inspection.

**Prompt Example 10: Traffic Drop Diagnosis & Re-indexing**

"Use the gsc\_query.py script to pull the top 20 queries driving traffic to the 'Premier League News' directory over the last 30 days. Identify any articles with high impressions but a CTR below 2%. For the lowest performing article, rewrite the Title Tag and Meta Description to improve CTR, and then trigger the indexing\_notify.py script to immediately notify Google of the updated URL."

**Prompt Example 11: Google Analytics 4 (GA4) Cross-Referencing**

"Use the ga4\_report.py script to identify which organic landing pages had the highest bounce rate over the last week. Cross-reference those URLs with gsc\_inspect.py to ensure there are no mobile usability errors or indexing issues causing the poor user experience."