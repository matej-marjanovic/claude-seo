# Prompt
Act as the seo-image-gen agent. Based on Magic Spoon's playful, high-protein cereal brand identity, use the Banana extension to generate 3 optimized hero image concepts suitable for a new 'Keto-Friendly Breakfast' landing page. Include the exact alt text and descriptive filenames I should use for these images to maximize Google Images traffic.

# SEO-Optimized Hero Image Generation: Magic Spoon

## 1. Image Concept Strategy
Based on the brand's identity, the generated images should maintain a high-saturation, playful aesthetic while clearly highlighting the "Keto-Friendly" and "High Protein" product attributes.

### Concept 1: The Macro-Focused Cereal Bowl
*   **Visual:** Extreme close-up of the cereal pieces in a colorful bowl, with milk splashing. The "0g Sugar" and "13g Protein" labels are clearly visible on the box in the background.
*   **Filename:** `keto-friendly-breakfast-cereal-bowl.webp`
*   **Alt Text:** "Close-up of Magic Spoon high-protein, keto-friendly cereal in a colorful bowl with milk splash."

### Concept 2: The Healthy Morning Routine
*   **Visual:** A lifestyle shot of a modern, bright kitchen with a Magic Spoon bowl next to a cup of black coffee. The sunlight highlights the product's vibrant purple packaging.
*   **Filename:** `healthy-keto-breakfast-morning-routine.webp`
*   **Alt Text:** "Bright morning kitchen scene featuring a bowl of Magic Spoon keto cereal and coffee, representing a healthy low-carb breakfast."

### Concept 3: The Variety Pack Explosion
*   **Visual:** A dynamic, slightly floating arrangement of various Magic Spoon flavors (Fruity, Cocoa, Peanut Butter) exploding from their boxes, set against a solid pastel yellow background.
*   **Filename:** `magic-spoon-cereal-variety-pack-flavors.webp`
*   **Alt Text:** "Explosion of various Magic Spoon keto cereal flavors showing Fruity, Cocoa, and Peanut Butter boxes for a high-protein breakfast variety pack."

## 2. Technical Image Optimization Guide
To maximize the SEO value of these assets, implement the following:

1.  **Format:** Deliver all hero assets in **WebP** for the best balance of quality and performance.
2.  **Compression:** Use **AVIF** for mobile users to further reduce the payload while maintaining brand-critical color accuracy.
3.  **Lazy Loading:** Hero images should NEVER be lazy-loaded. Set `loading="eager"` and use a pre-load link in the document head.
4.  **Schema Markup:** Wrap these images in `ImageObject` schema within the landing page's JSON-LD to ensure they are properly indexed in Google Images.
