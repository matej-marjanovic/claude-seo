---
name: seo-social-signals
description: >
  Social signal analysis via DataForSEO Social Media and Content Analysis APIs.
  Discovers Reddit content opportunities, analyzes Pinterest engagement trends,
  and measures social presence for URLs. Use when user says "social signals",
  "Reddit SEO", "Pinterest trends", "social media", "reddit opportunities",
  "content gap", or "social presence".
user-invokable: true
argument-hint: "[command] [keyword|url]"
license: MIT
allowed-tools: Read, Grep, Glob, Bash, WebFetch, Write
compatibility: "Requires DataForSEO Business Data API (Social Media endpoints)"
metadata:
  author: AgriciDaniel
  version: "1.8.0"
  category: seo
---

# Social Signal Analysis

Analyze social engagement signals, discover Reddit content opportunities,
and identify Pinterest visual trends using DataForSEO Social Media and
Content Analysis APIs.

## Prerequisites

Uses **Business Data API** (Social Media endpoints) and **Content Analysis API**.
Both are included in standard DataForSEO plans — no additional module activation needed.

## Quick Reference

| Command | What it does |
|---------|-------------|
| `/seo social reddit <keyword>` | Find Reddit discussions and content opportunities |
| `/seo social pinterest <keyword>` | Analyze Pinterest engagement trends |
| `/seo social signals <url>` | Get social signals for a specific URL |
| `/seo social aggregate <url>` | Cross-platform social presence score |

---

## Sub-Skills

### 1. `find_reddit_opportunities`

Discover Reddit threads where target keywords are discussed.

**Workflow:**
1. Cost check: `python3 scripts/dataforseo_costs.py check --command social-reddit`
2. Search for Reddit discussions: `python3 scripts/dataforseo_social.py reddit-opportunities "<keyword>" --limit 10`
3. Analyze results:
   - High-score threads with unanswered questions → content opportunity
   - Subreddits with high membership covering the niche → community targeting
   - Question-format threads → FAQ content ideas
   - "Looking for" or "recommend" threads → product/service opportunity
4. Cross-reference with keyword data to prioritize by search volume

**Output:**
- Reddit opportunity table (subreddit, title, comments, score, gap type)
- Top 5 content ideas from Reddit discussions
- Relevant subreddit list with membership counts
- Integration recommendations for content calendar

**Content Gap Types:**
| Gap Type | Signal | Action |
|----------|--------|--------|
| Question | Thread title contains "?" | Create comprehensive answer content |
| Intent Signal | "help", "recommend", "best", "looking for" | Create comparison or recommendation content |
| Discussion | General topic discussion | Add unique perspective or data |

### 2. `pinterest_trend_analysis`

Analyze Pinterest engagement for a domain or topic.

**Workflow:**
1. Cost check: `python3 scripts/dataforseo_costs.py check --command social-pinterest`
2. Fetch Pinterest trends: `python3 scripts/dataforseo_social.py pinterest-trends "<keyword>" --limit 10`
3. Analyze results:
   - Top-pinned URLs and content types
   - Image format patterns (which visual styles get pinned most)
   - Seasonal engagement patterns
   - Pin-to-page correlation (which content types generate pins)
4. Generate visual content recommendations

**Output:**
- Pinterest trend table (URL, pins, content type)
- Visual format recommendations (dimensions, styles, text overlays)
- Image creation brief for high-engagement formats
- Cross-reference with image optimization (link to `/seo images`)

---

## Social Signal as Content Strategy Input

> **Important disclaimer:** Social signals are NOT direct Google ranking factors.
> This data is used for **content strategy** and **audience insight**, not ranking optimization.

### How Social Data Feeds Other Skills

| Social Signal | Feeds Into | Skill |
|---|---|---|
| Reddit questions | Content topic ideas | `seo-content` |
| Reddit discussions | FAQ and help content | `seo-content` |
| Pinterest engagement | Image format recommendations | `seo-images` |
| Pinterest trends | Visual content calendar | `seo-plan` |
| Reddit + Pinterest as AI sources | GEO citation signals | `seo-geo` |

### AI Search Relevance

Reddit and Pinterest are indexed by AI systems (ChatGPT, Perplexity, Gemini).
Content that performs well on these platforms is more likely to appear in
AI-generated responses. Feed social signal findings into GEO strategy.

---

## Reference Files

No dedicated reference files — social signal analysis is lightweight.
For cost information, see `references/cost-config.md` (loaded by seo-dataforseo).

---

## Output

Generate `SOCIAL-SIGNALS-{keyword}.md` with:

1. **Reddit Opportunities** (top discussions with gap analysis)
2. **Pinterest Trends** (top-pinned content with visual analysis)
3. **Social Presence Score** (0-100 for target URL if provided)
4. **Content Ideas** (derived from social discussions)
5. **Image Recommendations** (derived from Pinterest trends)
6. **Action Items** (prioritized content and visual strategy recommendations)
7. **Cost Report** (DataForSEO credits consumed)

---

## Error Handling

| Scenario | Action |
|----------|--------|
| No Reddit discussions found | Topic may be too niche. Suggest broadening keyword or checking related terms. |
| No Pinterest data | Pinterest may not be relevant for this industry. Focus on Reddit and other signals. |
| Content Analysis API returns empty | Suggest trying alternative keyword variations. |
| Rate limit on social endpoints | Space out requests. Social endpoints are Live-only with no caching. |
