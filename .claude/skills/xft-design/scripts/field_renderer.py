#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Field Renderer: Schema -> Field HTML rendering engine.

Maps abstract field type definitions from a Schema JSON to concrete
component-combo HTML assets, personalizes them, and assembles the
result into a complete form-region segment.

Pipeline: Schema -> Field Registry lookup -> Combo HTML read ->
          Personalize (label/props/required) -> Wrap in form-field ->
          Inject into form-region template slots.
"""
from __future__ import annotations

import csv
import json
import re
from pathlib import Path
from typing import Any, Dict, List, Optional

ROOT = Path(__file__).resolve().parents[1]
ASSETS_DIR = ROOT / "assets" / "content-assets"
DATA_DIR = ROOT / "data" / "content-assets"


def load_field_registry(csv_path: Optional[Path] = None) -> Dict[str, Dict[str, Any]]:
    """Load field-type-registry.csv, return dict keyed by field_type."""
    if csv_path is None:
        csv_path = DATA_DIR / "field-type-registry.csv"
    registry: Dict[str, Dict[str, Any]] = {}
    with open(csv_path, encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            field_type = (row.get("field_type") or "").strip()
            if not field_type:
                continue
            wraps = (row.get("wraps_itself") or "true").strip().lower()
            raw_props = (row.get("default_props") or "{}").strip()
            try:
                default_props = json.loads(raw_props)
            except json.JSONDecodeError:
                default_props = {}
            registry[field_type] = {
                "combo_asset_id": (row.get("combo_asset_id") or "").strip(),
                "combo_html_path": (row.get("combo_html_path") or "").strip(),
                "wraps_itself": wraps == "true",
                "default_props": default_props,
                "validation_rules": (row.get("validation_rules") or "").strip(),
            }
    return registry


def _read_combo_html(registry_entry: Dict[str, Any]) -> str:
    html_path = registry_entry.get("combo_html_path", "")
    full_path = ROOT / html_path
    if not html_path or not full_path.exists():
        raise FileNotFoundError(f"Combo HTML not found: {html_path}")
    return full_path.read_text(encoding="utf-8")


def _merge_props(field: Dict[str, Any], registry_entry: Dict[str, Any]) -> Dict[str, Any]:
    merged = dict(registry_entry.get("default_props", {}))
    merged.update(field.get("props", {}))
    return merged


def _render_standard_field(field: Dict[str, Any], registry_entry: Dict[str, Any]) -> str:
    """Render text, select, textarea, date fields (xft-control-group pattern)."""
    html = _read_combo_html(registry_entry)
    props = _merge_props(field, registry_entry)
    label = field.get("label", "字段名称")

    # Replace label text (between >...< in the label element)
    html = re.sub(
        r'(<label\s+class="field-label"[^>]*>)([^<]*)(</label>)',
        rf"\g<1>{label}\g<3>",
        html,
    )

    # Add is-required class to xft-control-group
    if field.get("required", False):
        if 'class="xft-control-group' in html and "is-required" not in html:
            html = html.replace(
                'class="xft-control-group',
                'class="xft-control-group is-required',
            )

    # Replace placeholder text
    placeholder = props.get("placeholder", "")
    if placeholder:
        html = re.sub(r'placeholder="[^"]*"', f'placeholder="{placeholder}"', html)

    # Handle textarea rows
    if props.get("rows"):
        html = re.sub(r'rows="\d+"', f'rows="{props["rows"]}"', html)

    # Handle field-help: replace or remove
    help_text = props.get("help", "")
    if help_text:
        html = re.sub(
            r'(<div class="field-help">)([^<]*)(</div>)',
            rf"\g<1>{help_text}\g<3>",
            html,
        )
    else:
        html = re.sub(r'<div class="field-help">[^<]*</div>', "", html)

    return html


def _render_select_field(field: Dict[str, Any], registry_entry: Dict[str, Any]) -> str:
    """Render select field with options (same xft-control-group pattern)."""
    html = _read_combo_html(registry_entry)
    props = _merge_props(field, registry_entry)
    label = field.get("label", "字段名称")

    html = re.sub(
        r'(<label\s+class="field-label"[^>]*>)([^<]*)(</label>)',
        rf"\g<1>{label}\g<3>",
        html,
    )

    # Placeholder for select control (the display span)
    placeholder = props.get("placeholder", "请选择")
    html = re.sub(
        r'(<span>)([^<]*)(</span>)',
        rf"\g<1>{placeholder}\g<3>",
        html,
        count=1,
    )

    if field.get("required", False):
        if 'class="xft-control-group' in html and "is-required" not in html:
            html = html.replace(
                'class="xft-control-group',
                'class="xft-control-group is-required',
            )

    help_text = props.get("help", "")
    if help_text:
        html = re.sub(
            r'(<div class="field-help">)([^<]*)(</div>)',
            rf"\g<1>{help_text}\g<3>",
            html,
        )
    else:
        html = re.sub(r'<div class="field-help">[^<]*</div>', "", html)

    return html


def _render_date_field(field: Dict[str, Any], registry_entry: Dict[str, Any]) -> str:
    """Render date picker field."""
    return _render_standard_field(field, registry_entry)


def _render_switch_field(field: Dict[str, Any], registry_entry: Dict[str, Any]) -> str:
    """Render switch setting (setting-item pattern, not xft-control-group)."""
    html = _read_combo_html(registry_entry)
    props = _merge_props(field, registry_entry)
    label = field.get("label", "设置项标题")

    # Replace setting-title with field label
    html = re.sub(
        r'(<div class="setting-title">)([^<]*)(</div>)',
        rf"\g<1>{label}\g<3>",
        html,
    )

    # Replace setting-description
    description = props.get("description", "")
    if description:
        html = re.sub(
            r'(<div class="setting-description">)([^<]*)(</div>)',
            rf"\g<1>{description}\g<3>",
            html,
        )
    else:
        html = re.sub(r'<div class="setting-description">[^<]*</div>', "", html)

    # Handle checked state
    if props.get("checked", False):
        if "is-checked" not in html:
            html = html.replace(
                'class="switch ',
                'class="switch is-checked ',
            )
            if 'class="switch"' in html:
                html = html.replace(
                    'class="switch"',
                    'class="switch is-checked"',
                )
    else:
        html = html.replace(" is-checked", "")

    # Add data-switch attribute for runtime interaction
    if 'data-switch' not in html:
        html = html.replace(
            '<button class="switch',
            '<button data-switch class="switch',
        )

    return html


def _render_multi_select_field(field: Dict[str, Any], registry_entry: Dict[str, Any]) -> str:
    """Render multi-select / checkbox group field."""
    html = _read_combo_html(registry_entry)
    props = _merge_props(field, registry_entry)
    label = field.get("label", "多选字段")

    html = re.sub(
        r'(<label\s+class="field-label"[^>]*>)([^<]*)(</label>)',
        rf"\g<1>{label}\g<3>",
        html,
    )

    if field.get("required", False):
        if 'class="xft-control-group' in html and "is-required" not in html:
            html = html.replace(
                'class="xft-control-group',
                'class="xft-control-group is-required',
            )

    # Generate options from props
    options = props.get("options", ["选项一", "选项二", "选项三"])
    if options:
        option_html_parts: List[str] = []
        for idx, opt in enumerate(options):
            if isinstance(opt, str):
                checked = ' checked' if idx == 0 else ''
                option_html_parts.append(
                    f'<label class="checkbox">'
                    f'<input class="checkbox-input" type="checkbox"{checked} />'
                    f'<span class="checkbox-label">{opt}</span>'
                    f'</label>'
                )
        new_option_list = "\n".join(option_html_parts)
        html = re.sub(
            r'<div class="xft-option-list">.*?</div>',
            f'<div class="xft-option-list">\n{new_option_list}\n</div>',
            html,
            flags=re.DOTALL,
        )

    return html


_FIELD_RENDERERS = {
    "field.text": _render_standard_field,
    "field.textarea": _render_standard_field,
    "field.select": _render_select_field,
    "field.date": _render_date_field,
    "field.switch": _render_switch_field,
    "field.multiSelect": _render_multi_select_field,
}


def render_field(field: Dict[str, Any], registry: Dict[str, Dict[str, Any]]) -> str:
    """Render a single field to its HTML wrapper + personalized combo."""
    field_type = (field.get("type") or "field.text").strip()
    span = field.get("span", 1)

    registry_entry = registry.get(field_type)
    if registry_entry is None:
        return f'<!-- Unknown field type: {field_type} -->'

    renderer = _FIELD_RENDERERS.get(field_type, _render_standard_field)
    inner_html = renderer(field, registry_entry)

    return f'<div class="form-field span-{span}">\n{inner_html}\n</div>'


def render_actions(schema: Dict[str, Any]) -> str:
    """Render action buttons from schema.actions[]. """
    actions = schema.get("actions", [])
    if not actions:
        return (
            '<button class="btn btn-secondary" type="button">取消</button>\n'
            '<button class="btn btn-primary" type="submit">提交</button>'
        )

    parts: List[str] = []
    for action in actions:
        action_type = (action.get("type") or "").strip()
        label = action.get("label", "按钮")
        if action_type == "button.primary":
            parts.append(f'<button class="btn btn-primary" type="submit">{label}</button>')
        elif action_type == "button.secondary":
            parts.append(f'<button class="btn btn-secondary" type="button">{label}</button>')
        elif action_type == "button.danger":
            parts.append(f'<button class="btn btn-danger" type="button">{label}</button>')
        elif action_type == "button.text":
            parts.append(f'<button class="btn btn-text" type="button">{label}</button>')
        else:
            parts.append(f'<button class="btn btn-secondary" type="button">{label}</button>')
    return "\n".join(parts)


def render_section(section: Dict[str, Any], registry: Dict[str, Dict[str, Any]]) -> str:
    """Render one form section (heading + fields wrapped in a section element)."""
    title = section.get("title", "基础信息")
    description = section.get("description", "录入主体字段并完成提交前校验。")
    fields = section.get("fields", [])

    field_html_parts = [render_field(f, registry) for f in fields]
    field_html = "\n".join(field_html_parts)

    return (
        f'<section class="form-section form-section-group">\n'
        f'  <div class="form-section-heading">\n'
        f'    <h2 class="section-title">{title}</h2>\n'
        f'    <p class="section-description">{description}</p>\n'
        f'  </div>\n'
        f'  <div class="form-grid">\n'
        f'{field_html}\n'
        f'  </div>\n'
        f'</section>'
    )


def render_form_region(
    schema: Dict[str, Any],
    base_html_path: Optional[Path] = None,
    registry: Optional[Dict[str, Dict[str, Any]]] = None,
) -> str:
    """
    Full form-region assembly from schema.

    Reads the base.html template, replaces slotted placeholders with
    schema-driven field and action HTML, and sets data-mode.
    """
    if base_html_path is None:
        base_html_path = ASSETS_DIR / "regions" / "form-region" / "base.html"
    if registry is None:
        registry = load_field_registry()

    template = base_html_path.read_text(encoding="utf-8")
    mode = schema.get("mode", "basic")
    sections = schema.get("sections", [])

    # Set data-mode
    template = re.sub(
        r'data-mode="[^"]*"',
        f'data-mode="{mode}"',
        template,
    )

    # Render primary section (first section)
    if sections:
        primary_html = render_section(sections[0], registry)
        # Replace the first form-section-group entirely
        pattern = r'<section class="form-section form-section-group">.*?</section>'
        template = re.sub(pattern, primary_html, template, count=1, flags=re.DOTALL)

    # Render additional sections (for multi mode)
    additional_sections = sections[1:] if len(sections) > 1 else []
    if additional_sections:
        additional_html_parts = [render_section(sec, registry) for sec in additional_sections]
        additional_html = "\n".join(additional_html_parts)
        template = template.replace("<!-- ADDITIONAL_SECTION_SLOT -->", additional_html)
    else:
        # In basic/horizontal mode, hide the additional section slot
        if mode in ("basic", "horizontal"):
            template = template.replace("<!-- ADDITIONAL_SECTION_SLOT -->", "")
        else:
            # In multi mode with no extra sections, leave empty
            template = template.replace("<!-- ADDITIONAL_SECTION_SLOT -->", "")

    # Render actions
    action_html = render_actions(schema)
    template = template.replace("<!-- ACTION_SLOT -->", action_html)

    return template


def render_form_region_from_schema_json(
    schema_json: str,
    base_html_path: Optional[Path] = None,
) -> str:
    """Convenience: parse a JSON string and render the form region."""
    schema = json.loads(schema_json)
    return render_form_region(schema, base_html_path)
