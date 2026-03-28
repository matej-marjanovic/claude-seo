# Example 7: YouTube video SEO strategy (AllTrails / hiking gear)

## Original prompt

> Use the Youtube.py script to analyze the top 5 ranking videos for 'beginner hiking gear guide'. Break down their title structures, description formats, and tag optimizations. Propose a YouTube SEO strategy for AllTrails' official channel to rank for this query, including a suggested video title, description, and timestamp chapters.

## Generated output

### Script note

The repository provides `scripts/youtube_search.py` (not `Youtube.py`).  
Command: `python3 scripts/youtube_search.py search "beginner hiking gear guide" --limit 5 --json`

**Result without API key:**

```json
{
  "query": "beginner hiking gear guide",
  "videos": [],
  "total_results": 0,
  "error": "No API key. Set GOOGLE_API_KEY or add 'api_key' to config."
}
```

With `GOOGLE_API_KEY` and YouTube Data API v3 enabled, you would pull titles, descriptions, channel names, and view counts for the top results.

### Typical patterns for “beginner hiking gear guide” SERP (expert pattern analysis)

**Titles**

- Often include **year** or “ultimate / essential / beginner” + **numbered lists** (“10 things”, “5 mistakes”).
- Power words: **cheap vs worth it**, **budget**, **ultralight**, **women’s / men’s** splits for CTR.

**Descriptions**

- First **2 lines** repeat the primary keyword and promise (hook + CTA).
- **Amazon or brand links** to gear lists; **chapters** in description or as YouTube chapters.
- **Hashtags**: 2–3 max, mixed broad (#hiking) and specific (#hikinggear).

**Tags**

- Mix of **head** (hiking gear), **torso** (beginner hiking), **long-tail** (what to bring first hike).
- Competitor-adjacent tags used sparingly (trail names, seasons).

### AllTrails channel strategy

**Angle:** Pair **gear education** with **trail readiness** — maps, offline use, safety, and planning in the app (without turning the video into a pure ad).

**Suggested title**

`Beginner Hiking Gear Guide (2026) — 10 Essentials + What to Skip`

**Suggested description (template)**

```
New to hiking? This beginner hiking gear guide covers the 10 essentials, budget picks, and common mistakes—plus how to use offline trail maps when you lose signal.

0:00 Why gear matters for beginners
1:20 Footwear & socks
3:10 Daypack & hydration
5:35 Navigation & offline maps (AllTrails tip)
8:00 Layers & weather
10:20 Safety & first aid
12:45 Budget vs upgrade picks
15:30 What NOT to buy yet

DISCLAIMER: Gear choices depend on terrain and season—always check local conditions.

#hiking #hikinggear #beginnerhiking
```

**Timestamp chapters** — Mirror the list above in YouTube Studio → Chapters.

**Tags (examples)**  
beginner hiking gear, hiking essentials, day hike packing list, hiking for beginners, trail maps offline, hiking safety, budget hiking gear

---

*Re-run `youtube_search.py` with API access to replace this section with live top-5 competitor titles and stats.*
