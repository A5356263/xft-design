---
name: xft-design
version: "9.0"
description: Convert enterprise B-end requirements into constrained page, region, overlay, shell, runtime, and icon assignments from fixed local assets.
triggers:
  - B端页面
  - 后台页面
  - 表格页
  - 详情页
  - 表单页
  - 弹窗
  - 管理后台
---

# XFT Design Skill

## Positioning

This skill is a constrained prototype generator for enterprise B-end pages.

It is not:
- a free-form HTML generator
- a visual invention engine
- a custom JS authoring workflow
- a system that lets AI invent spacing, size, class names, or runtime behavior

It works like this:

`Requirement -> Intent Tags -> Page Decomposition -> Retrieval -> Schema -> Template Assignment -> HTML Assembly Plan`

For maintenance and asset-boundary rules, see [ARCHITECTURE.md](./ARCHITECTURE.md).

## Inputs

The skill reads:
- requirement text
- optional structured `page_spec.md`
- fixed local resources from:
  - `design-systems/`
  - `templates/`
  - `assets/shells/`
  - `assets/runtime/`
  - `assets/icons/`
  - `data/retrieval/*.csv`

## Stable Flow

1. Read requirement text.
2. Read optional `page_spec.md`.
3. Parse stable intent tags.
4. Decompose the requirement into one or more page nodes.
5. Retrieve page, region, overlay, shell, runtime, and icon candidates from CSV registries.
6. Compile a minimal schema.
7. Assign fixed local templates.
8. Assemble preview HTML from registered assets only.

## Retrieval Order

Always resolve assets in this order:

1. `page-routes.csv`
2. page template from `template-registry.csv`
3. `region-routes.csv`
4. `overlay-routes.csv`
5. `shell-registry.csv`
6. `runtime-registry.csv`
7. `icon-registry.csv`

## What AI May Do

AI may:
- understand requirement intent
- derive stable tags and signals
- choose page decomposition from registered rules
- retrieve registered page, region, overlay, shell, runtime, and icon assets
- fill registered copy and slot content
- hide or show registered regions based on signals

## What AI Must Not Do

AI must not:
- invent new page structure outside registered templates
- invent spacing, size, layout scales, or utility classes
- rewrite template CSS structure or class naming systems
- inject new JS behavior when a registered runtime should be used
- create page-specific interaction code ad hoc
- bypass registered slots from `data/retrieval/rewrite-slots.csv`

## Runtime And Template Rules

- Reuse registered runtime behavior first.
- Use `runtime.basic` for supported interactions such as:
  - collapse
  - overlay open and close
  - tabs
  - anchor
  - switch
- Template HTML may declare only registered `data-*` interaction contracts.
- If a requirement exceeds current runtime capability, do not improvise JS in the generated page.

## Current Working Skeleton

- `pipeline/intent_parser.py`
- `pipeline/page_decomposer.py`
- `pipeline/retrieval_engine.py`
- `pipeline/schema_compiler.py`
- `pipeline/template_registry.py`
- `pipeline/html_assembler.py`
- `scripts/vnext_run.py`

## Current Registry Inputs

- `data/retrieval/intent-tags.csv`
- `data/retrieval/page-routes.csv`
- `data/retrieval/region-routes.csv`
- `data/retrieval/overlay-routes.csv`
- `data/retrieval/template-registry.csv`
- `data/retrieval/rewrite-slots.csv`
- `data/retrieval/shell-registry.csv`
- `data/retrieval/runtime-registry.csv`
- `data/retrieval/icon-registry.csv`

## Output Expectation

The skill should be able to output:
- normalized intent tags
- decomposed page list
- retrieval context
- schema skeleton
- template assignment list
- HTML assembly plan
- previewable HTML pages from registered assets
