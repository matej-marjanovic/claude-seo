# Plan: Execute Claude SEO Example Prompts

## Objective
The objective is to execute the 11 example prompts listed in `examples/Claude-SEO-Example-Prompts.md`, generate their respective SEO insights, and save the results in a new `examples/example-outputs/` directory. Each prompt will have its own markdown file containing the original prompt and the resulting analysis.

## Scope & Impact
- **Scope:** 11 specific SEO scenarios (E-commerce, SaaS, Local SEO, ASO/YouTube, Visual SEO, and Search Console/GA4 ops).
- **Impact:** Provides a set of real-world examples for users to understand the plugin's capabilities. No changes to existing source code or logic.

## Key Context
- **Tooling:** All executions will use the project's `.venv` and the provided Python scripts in the `scripts/` directory.
- **MCP Servers:** Some prompts rely on the `dataforseo` MCP server, which is currently connected and configured.
- **Extensions:** Some prompts (e.g., Image Gen) rely on the `banana` extension, which is registered but not configured with an API key (the user opted not to). I will note this in the output if it cannot be executed.

## Implementation Steps

### Phase 1: Preparation
1. Create the directory: `examples/example-outputs/`.

### Phase 2: Execution & Output Generation
For each of the following prompts from `examples/Claude-SEO-Example-Prompts.md`:

1.  **01-ecommerce-performance-audit.md**: Performance check for eightsleep.com.
2.  **02-product-merchant-optimization.md**: Merchant analysis for eightsleep.com.
3.  **03-programmatic-content-roadmap.md**: Content plan for posthog.com.
4.  **04-entity-nlp-optimization.md**: NLP analysis for posthog.com.
5.  **05-local-search-reputation.md**: Local SEO for Joe's Coffee.
6.  **06-aso-keyword-expansion.md**: ASO analysis for AllTrails.
7.  **07-youtube-video-seo.md**: YouTube analysis for AllTrails.
8.  **08-visual-analysis.md**: Visual audit for magicspoon.com.
9.  **09-seo-optimized-assets.md**: Asset concepts for magicspoon.com.
10. **10-traffic-drop-diagnosis.md**: GSC analysis (requires authentication, simulate if necessary).
11. **11-ga4-cross-referencing.md**: GA4 and GSC cross-referencing (requires authentication, simulate if necessary).

## Verification & Testing
1. Check that all 11 files exist in `examples/example-outputs/`.
2. Review the files for accuracy and clarity.
