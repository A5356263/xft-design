# Templates

This directory stores fixed prototype templates for XFT Design.

This file is a short template-authoring summary only.

For asset-boundary and maintenance rules, see [../ARCHITECTURE.md](../ARCHITECTURE.md).

## Rules

- Templates are product-shape assets, not loose reference snippets.
- Region templates may embed their own `<style>` blocks.
- Page templates should usually stay light and compose regions.
- AI may only rewrite registered slots from `data/retrieval/rewrite-slots.csv`.
- AI must not alter template CSS structure, spacing scale, or class system.
- Templates must not contain private page-specific JS.
- Overlays are embedded into the primary page by default.
