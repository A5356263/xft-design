---
name: xft-design
version: "8.0"
description: Convert enterprise B-end requirements into UI schema and template assignments by retrieving existing design system resources and fixed local templates.
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

This skill is a constrained UI structure compiler.

It is not:
- a free-form HTML generator
- a workflow engine
- a runtime orchestration layer
- a system that lets AI invent UI spacing, size, or class names

Its job is:

`Requirement -> Intent Tags -> Page Decomposition -> Retrieval -> Schema -> Template Assignment -> HTML Assembly Plan`

## Core Rule

HTML structure must come from existing local resources only:
- `design-systems/`
- `templates/`
- reusable base assets such as `assets/shells/`, `assets/icons/`, `assets/runtime/`

AI may:
- understand requirements
- extract stable structure tags
- decide page decomposition
- retrieve the right local template or shell
- fill copy and schema placeholders

AI may not:
- invent spacing rules
- invent visual sizes
- invent new utility classes
- write a custom module when a local template should be used instead
- turn this skill back into the old content-asset orchestration architecture

## Stable Flow

1. Read requirement text.
2. Read optional `page_spec.md`.
3. Parse stable intent tags.
4. Decompose requirement into one or more page nodes.
5. Retrieve local design system references and template candidates.
6. Compile a minimal schema.
7. Assign fixed local templates.
8. Produce an HTML assembly plan.

## Boundaries

- Keep `design-systems/` unchanged unless explicitly requested.
- Templates are independent from `design-systems/`.
- Retrieval configuration should prefer CSV registries.
- Python should carry orchestration and validation only.
- If old Python logic is tied to the previous business architecture, delete it instead of adapting it.

## Current Skeleton

Current working skeleton:
- `pipeline/intent_parser.py`
- `pipeline/page_decomposer.py`
- `pipeline/retrieval_engine.py`
- `pipeline/schema_compiler.py`
- `pipeline/template_registry.py`
- `pipeline/html_assembler.py`
- `scripts/vnext_run.py`

Current registry inputs:
- `data/retrieval/intent-tags.csv`
- `data/retrieval/page-routes.csv`
- `data/retrieval/retrieval-rules.csv`
- `data/retrieval/template-registry.csv`

## Output Expectation

At this stage the skill must be able to output:
- normalized intent tags
- decomposed page list
- retrieval context
- schema skeleton
- template assignment list
- html assembly plan

Final HTML rendering can be completed later after the new template system is filled in.
