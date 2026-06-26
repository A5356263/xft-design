# XFT Content Assets Semantic Refactor Exec Patch

## Purpose

This file is a lightweight execution patch for:

- `_planning/CODEX-XFT-CONTENT-ASSETS-SEMANTIC-REFACTOR.md`

It does not replace the original document.
It narrows execution scope, reduces drift, and fixes missing constraints before implementation.

## Hard Decisions

1. `assets/content-assets/layouts/` is a required new top-level structure.
2. `layout` is a formal asset layer in this round, not a temporary tag.
3. This round is a semantic reorganization and targeted asset upgrade, not a full rewrite.
4. Existing assets that already satisfy the target structure should be reused or upgraded in place.
5. New assets are added only when the current asset cannot satisfy the target semantic boundary.

## Execution Scope

### In Scope

```text
.claude/skills/xft-design/assets/content-assets/regions
.claude/skills/xft-design/assets/content-assets/modules
.claude/skills/xft-design/assets/content-assets/layouts
.claude/skills/xft-design/assets/content-assets/overlays
.claude/skills/xft-design/assets/content-assets/states
.claude/skills/xft-design/assets/content-assets/_support
.claude/skills/xft-design/data/content-assets/content-assets.csv
.claude/skills/xft-design/data/content-assets/recipe-asset-map.csv
.claude/skills/xft-design/data/content-assets/asset-keywords.csv
.claude/skills/xft-design/data/content-assets/asset-rules.csv
.claude/skills/xft-design/data/content-assets/support-css-manifest.csv
```

### Out of Scope

```text
.claude/skills/xft-design/assets/content-assets/component-combos
.claude/skills/xft-design/assets/content-assets/feedback
.claude/skills/xft-design/assets/shells
.claude/skills/xft-design/assets/runtime
.claude/skills/xft-design/design-systems
.claude/skills/xft-design/scripts/search_icons.py
.claude/skills/xft-design/data/icons.csv
.claude/skills/xft-design/assets/icons
```

### Touch Only If Required For Compatibility

```text
.claude/skills/xft-design/SKILL.md
.claude/skills/xft-design/scripts/search_content_assets.py
.claude/skills/xft-design/scripts/check_skill_output.py
```

Compatibility edits are allowed only if the new `layout` layer or support CSS manifest cannot be consumed by the current engine without a minimal patch.

## Layer Rules

### Region

- Stable page area with clear page-level placement.
- Must be complete HTML, not placeholder wrappers.
- May contain internal layout, but layout is not its primary identity.

### Module

- Reusable business unit with stable semantic meaning.
- Should remain meaningful outside a single page.

### Layout

- Cross-region spatial composition pattern.
- Must not become a grab bag for ordinary region internals.
- Formal directory:

```text
.claude/skills/xft-design/assets/content-assets/layouts/
```

- Formal `asset_layer` value:

```text
layout
```

### Overlay

- Mounted to overlay slot only.
- Includes modal, drawer, confirm-style carriers.

### State

- Whole-page or in-region display state.
- Includes empty, loading, result, exception, progress-like states.

## Execution Method

Each candidate asset must be classified into one of:

- `keep`
- `upgrade`
- `replace`
- `new`
- `legacy`

Rules:

1. `keep`
   Existing asset already matches target semantics and structure.
2. `upgrade`
   Existing asset keeps identity but needs stronger HTML completeness or CSS cleanup.
3. `replace`
   Existing asset name or folder stays logically related, but the actual file should be superseded by a new standard asset.
4. `new`
   Asset does not exist and must be added.
5. `legacy`
   Old asset remains on disk temporarily but must no longer be preferred by new recipe mappings.

## Data Rules

This round must keep the retrieval method engineering-driven.

- `content-assets.csv` is the source of truth for layer, type, variant, path, and support CSS linkage.
- `asset-keywords.csv` must reflect the new semantic names.
- `asset-rules.csv` must reflect any layer-specific constraints, especially for `layout`.
- `recipe-asset-map.csv` must point new recipes and existing recipes to the correct layer-specific assets.

Do not rely on prose-only guidance in `SKILL.md` to bridge missing asset semantics.

## Layout Handling Rule

For this round:

1. Existing layout-like files under `regions/` may remain temporarily on disk.
2. But new standard mappings should point to files under `assets/content-assets/layouts/` when the asset is truly a layout.
3. If an old region file is actually a layout, reclassify it in data first, then decide whether to move or supersede the file.
4. Avoid mass file moving before data classification is clear.

This keeps the round lighter and reduces breakage.

## Validation Path

Use current project path conventions.

- Generated HTML outputs live under:

```text
output/
```

- Validation scripts:

```text
.claude/skills/xft-design/scripts/search_content_assets.py
.claude/skills/xft-design/scripts/search_icons.py
.claude/skills/xft-design/scripts/check_skill_output.py
```

Do not use legacy `examples/` output assumptions in this round.

## Acceptance Gates

Before calling this round done, confirm:

1. `assets/content-assets/layouts/` exists and is used by data mappings.
2. The new or reclassified assets are reflected in `content-assets.csv`.
3. Support CSS manifest covers any newly introduced layer-level support files.
4. No required recipe points to an invalid asset path.
5. Existing retrieval output remains parseable JSON.
6. Real HTML output validation still works with `check_skill_output.py`.

## Start Order

1. Create `layouts/` structure and classify current layout-like assets.
2. Build the asset diff list: `keep / upgrade / replace / new / legacy`.
3. Patch CSV mappings to reflect the new semantic layer model.
4. Upgrade or add HTML assets and support CSS in the smallest possible set.
5. Run retrieval and path validation.
6. Generate and validate real pages only after mappings are stable.
