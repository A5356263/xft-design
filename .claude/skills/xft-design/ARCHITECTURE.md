# XFT Design Skill Architecture

## Purpose

This document is for maintainers of the skill.

It defines asset boundaries, ownership, and decision rules. It is not the main execution prompt for page-generation AI.

## Core Principle

Do not mix:
- user/product constraints
- asset architecture rules
- long-term maintenance rules

with:
- short execution instructions for page-generation AI

`SKILL.md` is the AI execution entry.

This file is the maintenance and architecture contract.

## Asset Responsibilities

### `design-systems/`

Owns:
- design tokens
- visual language
- spacing scale
- color system
- typography rules
- base component reference language

Does not own:
- business page templates
- region-level product layouts
- page-specific interaction behavior

### `templates/`

Owns:
- page templates
- region templates
- overlay templates
- product-shape HTML structure
- template-local capability constraints

Rules:
- region templates may embed their own `<style>` blocks
- page templates should usually stay light and focus on composition
- templates are product assets, not loose snippets
- if a template has stable structural capabilities, they should be declared as registered metadata, not hidden in assembler constants

Examples of template capability metadata:
- `base_capacity`
- `has_expand`
- other future template-level fixed behavior switches

Current rule:
- `filter-bar` first-row capacity and expand support belong to template metadata, not Python constants

### `templates/styles/foundation.css`

Owns only:
- cross-template shared base styles
- basic control classes
- generic card, section, and table foundation
- shared responsive helpers

Must not own:
- `filter-bar`-specific layout
- `action-bar`-specific layout
- `table-region`-specific layout
- any region’s product personality

### `assets/runtime/`

Owns:
- reusable registered interactions
- behavior behind `data-*` contracts

Rules:
- prefer `runtime.basic` first
- templates declare contracts such as `data-collapse-toggle` or `data-overlay-open`
- runtime implements those contracts

Must not become:
- a page-specific glue-code dump
- a place for ad hoc one-off behavior unless it is promoted into a reusable registered capability

### `pipeline/`

Owns:
- parsing
- retrieval
- schema compilation
- template assignment
- slot injection
- style aggregation
- reading registered template capabilities
- output validation

Must not own:
- primary visual definition of templates
- free-form module generation
- ad hoc layout invention
- hidden template product rules that are not registered in assets

Rules:
- `pipeline` may read template metadata from registry and apply it during assembly
- `pipeline` may compute instance values needed by a template, such as a current page label-width variable
- `pipeline` must not become the source of truth for template shape decisions that can live in template assets or registry

### `AI`

AI may:
- understand specs
- retrieve registered assets
- rewrite registered slots
- choose among registered page, region, overlay, shell, runtime, and icon assets

AI must not:
- invent spacing systems
- invent class names
- invent new JS behavior in generated pages
- choose unregistered interaction patterns
- rewrite fixed template structure outside allowed slots

## Decision Rules

### Where should a new style change go?

Use this order:

1. `design-systems/`
   - if the change affects shared visual language, tokens, or global component rules
2. `foundation.css`
   - if the change is shared by many templates and is still generic
3. template-local `<style>`
   - if the change is region-specific, page-specific, or product-shape-specific

Default:
- layout, spacing rhythm, and structure of a specific region belong in that region template

### Where should a new interaction go?

Use this order:

1. reuse `runtime.basic`
2. extend runtime as a reusable registered capability
3. update template contracts to use that runtime capability

Do not:
- place private JS directly inside a template
- let page-generation AI invent glue code for one page

Default for region interactions:
- if a region can use an existing `data-*` contract from `runtime.basic`, reuse it
- if not, promote a new reusable runtime capability first
- do not move region interaction policy into `pipeline`

### Where should a template rule go?

Use this order:

1. template HTML or template-local `<style>`
   - for fixed structure, layout rhythm, and region-local visual behavior
2. template registry metadata
   - for stable template capabilities that affect assembly but are not free-form user content
3. `pipeline`
   - only to read metadata, calculate per-instance values, and inject registered slots

Examples:
- `filter-bar` first-row field capacity -> template registry metadata
- `filter-bar` label/control spacing -> template-local `<style>`
- `filter-bar` current label width for one page instance -> computed by `pipeline` and injected as a constrained variable
- `filter-bar` expand/collapse click behavior -> `runtime.basic`

## Template Authoring Rules

- A template should be directly previewable.
- Region templates should show most of their real UI without relying on assembler-defined visuals.
- Only registered slots may be rewritten by AI.
- Fixed dimensions, spacing scales, and class systems should remain stable.
- Template markup can expose `data-*` hooks, but behavior implementation belongs to runtime.
- Region-local primitives may exist inside a template without becoming retrieval-level assets.

Example:
- `filter-bar` may own an internal `field-item / field-label / field-control` primitive
- that primitive is part of the region template contract, not an independently retrieved module

## Reference Links

- AI execution entry: [SKILL.md](./SKILL.md)
- Template directory notes: [templates/README.md](./templates/README.md)
