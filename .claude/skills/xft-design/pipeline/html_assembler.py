"""Assemble V0.2 prototype outputs from page and region templates."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT.parents[2] / "output"
MOJIBAKE_MARKERS = (
    "\u95b2\u5d87\u7586",
    "\u93cc\u30e8\ue1d7",
    "\u93c7\u6751\ue63f\u7edb\u6da2\u20ac",
    "\u93c0\u60f0\u6363\u7edb\u6da2\u20ac",
    "\u6fee\u64b3\u6095",
    "\u93b5\u5b2b\u6e80\u9359",
    "\u7487\u75af\u7ded\u934f\u30e5",
    "\u7487\u70fd\u20ac\u590b\u5ae8",
    "\u9352\u6d98\u7f13\u93c3\u5815\u68ff",
    "\u93b4\u612c\u61b3\u8930\u6391\u7758",
    "\ufffd",
)
COPY = {
    "filter_more": "更多筛选",
    "filter_less": "收起筛选",
    "reset": "重置",
    "query": "查询",
    "table_actions": "操作",
    "pagination_total": "共 135 条",
    "pagination_prev": "上一页",
    "pagination_next": "下一页",
    "cancel": "取消",
    "confirm": "确认",
}
TABLE_QUERY_HINTS = {
    "editable": ("可编辑", "编辑", "editable", "inline edit"),
    "selection": ("批量", "batch", "勾选", "selection"),
    "empty": ("空态", "无数据", "empty"),
    "no_pagination": ("无分页", "不分页", "none pagination"),
    "copy": ("复制", "copy"),
    "remove": ("删除", "remove", "delete"),
    "import": ("导入", "import", "上传", "upload"),
    "export": ("导出", "export", "下载", "download"),
    "refresh": ("刷新", "refresh"),
    "column_settings": ("列设置", "column settings"),
    "density": ("密度", "density"),
}
GENERIC_TABLE_SCENE = {
    "filter_fields": [
        {"label": "姓名", "kind": "search", "placeholder": "请输入姓名"},
        {"label": "手机号", "kind": "text", "placeholder": "请输入手机号"},
        {"label": "部门", "kind": "select", "placeholder": "请选择部门"},
        {"label": "状态", "kind": "status", "placeholder": "请选择状态"},
    ],
    "advanced_fields": [
        {"label": "创建时间", "kind": "text", "placeholder": "请选择时间范围"},
        {"label": "成员归属", "kind": "member", "placeholder": "请选择成员"},
    ],
    "quick_filters": ["全部", "待处理", "已启用"],
    "default_columns": ["姓名", "手机号", "部门", "角色", "状态"],
    "default_rows": [
        ["王琳", "138****1024", "华东运营", "运营主管", "已启用"],
        ["张弛", "139****6632", "渠道增长", "数据分析", "待审核"],
    ],
    "editable_columns": ["日期", "项目", "数量", "负责人", "状态"],
    "editable_rows": [
        ["2026-06-28", "费用预算", "12", "王琳", "草稿"],
        ["2026-06-29", "商户补贴", "20", "张弛", "已保存"],
    ],
    "detail_blocks": [("字段一", "示例值"), ("字段二", "示例值")],
    "form_fields": [{"label": "字段一", "placeholder": "请输入字段一", "kind": "text"}],
    "footer_actions": [{"label": "确认", "role": "primary"}],
    "copy_options": ["授权组织", "授权功能"],
    "target_tags": ["用户 A", "用户 B", "用户 C"],
    "result_summary": "复制完成，成功 3 人，失败 0 人。",
    "result_groups": [
        {"title": "新增子管理员（2）", "items": ["用户 A / 138****2101", "用户 B / 137****6623"]},
        {"title": "权限已覆盖（1）", "items": ["用户 C / 136****7741"]},
    ],
    "source_text": "复制来源：王琳 / 138****1024",
    "overlay_title_copy": "复制子管理员权限",
    "overlay_title_result": "复制结果",
    "result_footer_note": "关闭弹窗后返回列表并刷新展示结果。",
    "page_description": "在列表中查看、筛选并发起页面级操作。",
}


def slugify(text: str) -> str:
    base = re.sub(r"\s+", "-", text.strip().lower())
    base = re.sub(r"[^a-z0-9\u4e00-\u9fff-]+", "-", base)
    return re.sub(r"-{2,}", "-", base).strip("-") or "xft-v0"


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _extract_style_blocks(html: str) -> tuple[list[str], str]:
    blocks = re.findall(r"<style[^>]*>(.*?)</style>", html, flags=re.S | re.I)
    stripped = re.sub(r"<style[^>]*>.*?</style>\s*", "", html, flags=re.S | re.I)
    return [block.strip() for block in blocks if block.strip()], stripped


def _extract_component_styles() -> str:
    html = _read_text(ROOT / "design-systems" / "components.html")
    match = re.search(r"<style[^>]*>(.*?)</style>", html, flags=re.S | re.I)
    return match.group(1).strip() if match else ""


def _inject_styles(shell_html: str, style_blocks: list[str]) -> str:
    seen: set[str] = set()
    merged: list[str] = []
    for block in style_blocks:
        if not block or block in seen:
            continue
        seen.add(block)
        merged.append(block)
    insertion = "".join(f"\n  <style>\n{block}\n  </style>" for block in merged)
    return shell_html.replace("</title>", "</title>" + insertion, 1)


def _inject_runtime(shell_html: str, shell_id: str, runtime_path: Path) -> str:
    if shell_id == "shell.admin-side":
        return shell_html
    runtime_js = _read_text(runtime_path)
    return shell_html.replace("</body>", f"  <script>\n{runtime_js}\n  </script>\n</body>", 1)


def _replace_tokens(html: str, replacements: dict[str, str]) -> str:
    for key, value in replacements.items():
        html = html.replace(f"{{{{{key}}}}}", value)
    return html


def _replace_slot_block(html: str, slot_name: str, content: str) -> str:
    pattern = re.compile(
        rf'(<(?P<tag>[a-z0-9]+)(?P<attrs>[^>]*\bdata-slot="{re.escape(slot_name)}"[^>]*)>)(?P<body>.*?)(</(?P=tag)>)',
        flags=re.S | re.I,
    )
    match = pattern.search(html)
    if not match:
        return html
    return html[: match.start()] + match.group(1) + content + match.group(5) + html[match.end() :]


def _remove_slot_block(html: str, slot_name: str) -> str:
    pattern = re.compile(
        rf'<(?P<tag>[a-z0-9]+)(?P<attrs>[^>]*\bdata-slot="{re.escape(slot_name)}"[^>]*)>.*?</(?P=tag)>\s*',
        flags=re.S | re.I,
    )
    return pattern.sub("", html)


def _render_icon(icon: dict[str, str]) -> str:
    path = ROOT / icon.get("path", "")
    return _read_text(path) if path.exists() else ""

def _render_button(label: str, *, tone: str = "default", icon: str = "", attrs: str = "") -> str:
    cls = "xftv0-button"
    if tone == "primary":
        cls += " xftv0-button-primary"
    elif tone == "subtle":
        cls += " xftv0-button-subtle"
    icon_html = f'<span class="xftv0-icon">{icon}</span>' if icon else ""
    return f'<button class="{cls}" type="button"{attrs}>{icon_html}{label}</button>'


def _render_link_action(label: str, *, icon: str = "", attrs: str = "") -> str:
    icon_html = f'<span class="xftv0-icon">{icon}</span>' if icon else ""
    return f'<button class="xftv0-table-region-link" type="button"{attrs}>{icon_html}{label}</button>'


def _render_filter_field(field: dict[str, str]) -> str:
    kind = field["kind"]
    label = field["label"]
    placeholder = field["placeholder"]
    if kind in {"select", "status", "member"}:
        control = f'<select class="xftv0-select"><option>{placeholder}</option></select>'
    else:
        input_type = "number" if kind == "number" else "text"
        control = f'<input class="xftv0-input" type="{input_type}" placeholder="{placeholder}" />'
    return (
        '<div class="xftv0-filter-region-field-item">'
        f'<span class="xftv0-filter-region-field-label">{label}</span>'
        f'<div class="xftv0-filter-region-field-control">{control}</div>'
        "</div>"
    )


def _render_filter_fields(fields: list[dict[str, str]]) -> str:
    return "".join(_render_filter_field(field) for field in fields)


def _render_quick_filters(items: list[str]) -> str:
    return "".join(f'<button class="xftv0-chip" type="button">{item}</button>' for item in items)


def _get_template_int(template: dict[str, str], key: str, default: int) -> int:
    raw_value = (template.get(key) or "").strip()
    if not raw_value:
        return default
    try:
        return int(raw_value)
    except ValueError:
        return default


def _get_template_bool(template: dict[str, str], key: str, default: bool) -> bool:
    raw_value = (template.get(key) or "").strip().lower()
    if not raw_value:
        return default
    if raw_value in {"true", "1", "yes"}:
        return True
    if raw_value in {"false", "0", "no"}:
        return False
    return default


def _split_filter_fields(
    base_fields: list[dict[str, str]],
    advanced_fields: list[dict[str, str]],
    base_capacity: int,
) -> tuple[list[dict[str, str]], list[dict[str, str]], bool]:
    visible_base_fields = base_fields[:base_capacity]
    overflow_base_fields = base_fields[base_capacity:]
    expanded_fields = overflow_base_fields + advanced_fields
    has_expandable_fields = bool(expanded_fields)
    return visible_base_fields, expanded_fields, has_expandable_fields


def _compute_filter_label_width(fields: list[dict[str, str]]) -> int:
    max_chars = max((len(field.get("label", "").strip()) for field in fields), default=2)
    return max(48, min(112, max_chars * 16 + 8))


def _render_filter_toggle(panel_id: str) -> str:
    return (
        f'<button class="xftv0-filter-region-toggle-button" type="button" data-collapse-toggle="{panel_id}" aria-expanded="false">'
        f'<span class="xftv0-filter-region-toggle-collapsed">{COPY["filter_more"]}</span>'
        f'<span class="xftv0-filter-region-toggle-expanded">{COPY["filter_less"]}</span>'
        '<span class="xftv0-filter-region-toggle-arrow">▼</span>'
        "</button>"
    )


def _render_filter_action_set(*, show_filter_actions: bool, has_advanced_toggle: bool, panel_id: str, expanded: bool = False) -> str:
    parts: list[str] = []
    if show_filter_actions:
        parts.append(_render_button(COPY["reset"]))
        parts.append(_render_button(COPY["query"], tone="primary"))
    if has_advanced_toggle and (not expanded or show_filter_actions or has_advanced_toggle):
        parts.append(_render_filter_toggle(panel_id))
    return "".join(parts)


def _render_action_group(actions: list[dict[str, str]], icons: dict[str, str], primary_label: str) -> str:
    parts: list[str] = []
    if primary_label:
        parts.append(_render_button(primary_label, tone="primary", icon=icons.get("plus", "")))
    for action in actions:
        parts.append(_render_button(action["label"], icon=icons.get(action["icon"], "")))
    return "".join(parts)


def _render_table_columns(columns: list[str], *, show_selection: bool, include_actions: bool) -> str:
    cells: list[str] = []
    if show_selection:
        cells.append('<th class="xftv0-table-region-select-col"><input type="checkbox" /></th>')
    cells.extend(f"<th>{label}</th>" for label in columns)
    if include_actions:
        cells.append(f"<th>{COPY['table_actions']}</th>")
    return f"<tr>{''.join(cells)}</tr>"


def _render_editable_control(kind: str, value: str) -> str:
    if kind == "select":
        return f'<select class="xftv0-table-region-select"><option>{value}</option></select>'
    return f'<input class="xftv0-table-region-input" type="text" value="{value}" />'


def _render_table_rows(context: dict[str, Any], icons: dict[str, str]) -> str:
    rows: list[str] = []
    include_actions = bool(context["row_actions"])
    editable_mode = context["table_mode"] == "editable"
    editable_fields = context["editable_fields"]
    for row in context["sample_rows"]:
        cells: list[str] = []
        if context["show_selection"]:
            cells.append('<td class="xftv0-table-region-select-col"><input type="checkbox" /></td>')
        for index, value in enumerate(row):
            if editable_mode and index < len(editable_fields):
                cells.append(f"<td>{_render_editable_control(editable_fields[index], value)}</td>")
            else:
                cells.append(f"<td>{value}</td>")
        if include_actions:
            actions = "".join(
                _render_link_action(
                    action["label"],
                    icon=icons.get(action["icon"], ""),
                    attrs=' data-overlay-open="copy-modal"' if action["id"] == "copy" else "",
                )
                for action in context["row_actions"]
            )
            cells.append(f'<td><div class="xftv0-table-region-actions">{actions}</div></td>')
        rows.append(f"<tr>{''.join(cells)}</tr>")
    return "".join(rows)


def _render_pagination(mode: str) -> str:
    if mode == "none":
        return ""
    return (
        f"<span>{COPY['pagination_total']}</span>"
        '<div class="xftv0-table-region-pagination-controls">'
        f'<button class="xftv0-table-region-page-button" type="button">{COPY["pagination_prev"]}</button>'
        '<span class="xftv0-table-region-page-current">1</span>'
        f'<button class="xftv0-table-region-page-button" type="button">{COPY["pagination_next"]}</button>'
        "</div>"
    )


def _render_detail_blocks(context: dict[str, Any]) -> str:
    return "".join(
        f'<div class="xftv0-description-item"><span class="xftv0-description-label">{label}</span><span class="xftv0-description-value">{value}</span></div>'
        for label, value in context.get("detail_blocks", [])
    )


def _render_form_fields(context: dict[str, Any]) -> str:
    parts = []
    for field in context.get("form_fields", []):
        kind = field.get("kind", "text")
        if kind == "select":
            control = f'<select class="xftv0-select"><option>{field["placeholder"]}</option></select>'
        elif kind == "textarea":
            control = f'<textarea class="xftv0-textarea" placeholder="{field["placeholder"]}"></textarea>'
        else:
            control = f'<input class="xftv0-input" type="text" placeholder="{field["placeholder"]}" />'
        width_class = " xftv0-form-field-wide" if field.get("wide") else ""
        parts.append(f'<div class="xftv0-field{width_class}"><span class="xftv0-field-label">{field["label"]}</span>{control}</div>')
    return "".join(parts)


def _render_footer_actions(context: dict[str, Any]) -> str:
    buttons = []
    for action in context.get("footer_actions", []):
        tone = "primary" if action["role"] == "primary" else "default"
        buttons.append(_render_button(action["label"], tone=tone))
    return "".join(buttons)


def _render_copy_options(options: list[str]) -> str:
    return "".join(f'<label class="xftv0-checkbox-chip"><input type="checkbox" checked />{item}</label>' for item in options)


def _render_target_tags(items: list[str]) -> str:
    return "".join(f'<span class="xftv0-target-tag">{item}</span>' for item in items)


def _render_result_groups(groups: list[dict[str, Any]]) -> str:
    blocks = []
    for group in groups:
        items = "".join(f"<li>{item}</li>" for item in group.get("items", []))
        blocks.append(
            f'<section class="xftv0-result-group"><h3 class="xftv0-result-group-title">{group["title"]}</h3><ol class="xftv0-result-list">{items}</ol></section>'
        )
    return "".join(blocks)


def _has_any(text: str, *tokens: str) -> bool:
    return any(token in text for token in tokens)


def _infer_table_mode(schema: dict[str, Any]) -> str:
    query = schema.get("query", "").lower()
    tags = set(schema.get("intent_tags", []))
    if "editable" in tags and _has_any(query, *TABLE_QUERY_HINTS["editable"]):
        return "editable"
    return "basic"


def _build_scene_context(schema: dict[str, Any], page: dict[str, Any]) -> dict[str, Any]:
    query = schema.get("query", "").lower()
    title = schema.get("title", schema.get("query", "XFT V0"))
    signals = dict(schema.get("signals", {}))
    table_mode = _infer_table_mode(schema)
    show_selection = _has_any(query, *TABLE_QUERY_HINTS["selection"])
    table_state = "empty" if _has_any(query, *TABLE_QUERY_HINTS["empty"]) else "default"
    pagination_mode = "none" if _has_any(query, *TABLE_QUERY_HINTS["no_pagination"]) else "page"

    row_actions = [
        {"id": "view", "label": "查看", "icon": "info-circle"},
        {"id": "edit", "label": "编辑", "icon": "edit"},
    ]
    if schema.get("scene") == "copy_permission" or _has_any(query, *TABLE_QUERY_HINTS["copy"]):
        row_actions.insert(0, {"id": "copy", "label": "复制", "icon": "copy"})
    if _has_any(query, *TABLE_QUERY_HINTS["remove"]):
        row_actions.append({"id": "remove", "label": "删除", "icon": "delete"})

    filter_fields = [field.copy() for field in GENERIC_TABLE_SCENE["filter_fields"]]
    advanced_fields = [field.copy() for field in GENERIC_TABLE_SCENE["advanced_fields"]]
    quick_filters = list(GENERIC_TABLE_SCENE["quick_filters"]) if signals.get("quick_filtering") else []

    secondary_actions: list[dict[str, str]] = []
    if signals.get("top_secondary_actions"):
        if _has_any(query, *TABLE_QUERY_HINTS["import"]):
            secondary_actions.append({"label": "导入", "icon": "upload"})
        if _has_any(query, *TABLE_QUERY_HINTS["export"]):
            secondary_actions.append({"label": "导出", "icon": "download"})
        if _has_any(query, *TABLE_QUERY_HINTS["remove"]):
            secondary_actions.append({"label": "删除", "icon": "delete"})

    utility_actions: list[dict[str, str]] = []
    if signals.get("top_utility_actions"):
        if _has_any(query, *TABLE_QUERY_HINTS["refresh"]):
            utility_actions.append({"label": "刷新", "icon": ""})
        if _has_any(query, *TABLE_QUERY_HINTS["column_settings"]):
            utility_actions.append({"label": "列设置", "icon": "setting"})
        if _has_any(query, *TABLE_QUERY_HINTS["density"]):
            utility_actions.append({"label": "密度", "icon": ""})

    if schema.get("scene") == "copy_permission":
        signals["base_filtering"] = True
        signals["top_primary_action"] = True
        signals["top_secondary_actions"] = True
        signals["top_utility_actions"] = True
        quick_filters = []
        secondary_actions = [{"label": "导出", "icon": "download"}]
        utility_actions = [{"label": "列设置", "icon": "setting"}]
        show_selection = True

    primary_label = "新增子管理员" if schema.get("scene") == "copy_permission" else ("新增" if signals.get("top_primary_action") else "")
    show_batch_actions = show_selection and _has_any(query, *TABLE_QUERY_HINTS["selection"])
    batch_actions = [{"label": "批量导出", "icon": "download"}] if show_batch_actions else []

    sample_columns = list(GENERIC_TABLE_SCENE["default_columns"])
    sample_rows = [row[:] for row in GENERIC_TABLE_SCENE["default_rows"]]
    editable_fields = ["text", "select", "number"] if table_mode == "editable" else []
    if table_mode == "editable":
        sample_columns = list(GENERIC_TABLE_SCENE["editable_columns"])
        sample_rows = [row[:] for row in GENERIC_TABLE_SCENE["editable_rows"]]
    if table_state == "empty":
        sample_rows = []

    return {
        "page_title": "子管理员权限复制" if schema.get("scene") == "copy_permission" else title,
        "page_description": GENERIC_TABLE_SCENE["page_description"],
        "page_badge": "V0.2",
        "filter_fields": filter_fields if signals.get("base_filtering") else [],
        "filter_actions": [COPY["query"], COPY["reset"]] if signals.get("filtering") else [],
        "quick_filters": quick_filters,
        "show_quick_filters": bool(quick_filters),
        "has_advanced_toggle": signals.get("advanced_filtering", False),
        "advanced_fields": advanced_fields if signals.get("advanced_filtering") else [],
        "advanced_fields_visible": signals.get("advanced_filtering", False),
        "show_filter_actions": bool(signals.get("filtering")),
        "toolbar_primary": primary_label,
        "show_primary_group": bool(primary_label or secondary_actions),
        "toolbar_secondary_actions": secondary_actions,
        "show_batch_actions": show_batch_actions,
        "selection_status_text": "已选 3 项" if show_batch_actions else "",
        "toolbar_batch_actions": batch_actions,
        "toolbar_utility_actions": utility_actions,
        "show_utility_group": bool(utility_actions),
        "table_mode": table_mode,
        "table_columns": sample_columns,
        "sample_rows": sample_rows,
        "row_actions": row_actions,
        "show_selection": show_selection,
        "table_state": table_state,
        "pagination_mode": pagination_mode,
        "editable_fields": editable_fields,
        "detail_blocks": list(GENERIC_TABLE_SCENE["detail_blocks"]),
        "form_fields": [field.copy() for field in GENERIC_TABLE_SCENE["form_fields"]],
        "footer_actions": [action.copy() for action in GENERIC_TABLE_SCENE["footer_actions"]],
        "copy_options": list(GENERIC_TABLE_SCENE["copy_options"]),
        "target_tags": list(GENERIC_TABLE_SCENE["target_tags"]),
        "result_summary": GENERIC_TABLE_SCENE["result_summary"],
        "result_groups": [{"title": group["title"], "items": list(group["items"])} for group in GENERIC_TABLE_SCENE["result_groups"]],
        "source_text": GENERIC_TABLE_SCENE["source_text"],
        "overlay_title_copy": GENERIC_TABLE_SCENE["overlay_title_copy"],
        "overlay_title_result": GENERIC_TABLE_SCENE["overlay_title_result"],
        "result_footer_note": GENERIC_TABLE_SCENE["result_footer_note"],
    }


def _load_template_with_styles(relative_path: str) -> tuple[list[str], str]:
    return _extract_style_blocks(_read_text(ROOT / relative_path))


def _render_region(region: dict[str, Any], page: dict[str, Any], schema: dict[str, Any], context: dict[str, Any]) -> tuple[list[str], str]:
    styles, template = _load_template_with_styles(region["template"]["template_path"])
    template_id = region["template"]["template_id"]
    icons = {icon.get("semantic_name"): _render_icon(icon) for icon in page.get("icons", [])}

    if template_id == "region.page-header":
        return styles, _replace_tokens(
            template,
            {
                "page_title": context["page_title"],
                "page_description": context["page_description"],
                "page_badge": context["page_badge"],
            },
        )
    if template_id == "region.filter-bar":
        base_capacity = max(1, _get_template_int(region["template"], "base_capacity", 2))
        template_has_expand = _get_template_bool(region["template"], "has_expand", True)
        advanced_panel_id = f"xftv0-filter-advanced-{page['page_id']}"
        label_width = _compute_filter_label_width(context["filter_fields"] + context["advanced_fields"])
        visible_base_fields, expanded_fields, has_expandable_fields = _split_filter_fields(
            context["filter_fields"],
            context["advanced_fields"],
            base_capacity,
        )
        has_expandable_fields = template_has_expand and has_expandable_fields
        html = _replace_tokens(
            template,
            {
                "advanced_panel_id": advanced_panel_id,
                "filter_region_style": f"--xftv0-filter-label-width: {label_width}px;",
            },
        )
        html = _replace_slot_block(html, "base_fields_slot", _render_filter_fields(visible_base_fields))
        base_actions = _render_filter_action_set(
            show_filter_actions=context["show_filter_actions"],
            has_advanced_toggle=has_expandable_fields,
            panel_id=advanced_panel_id,
        )
        html = _replace_slot_block(html, "actions_slot", base_actions) if base_actions else _remove_slot_block(html, "actions_slot")
        html = _replace_slot_block(html, "quick_filters", _render_quick_filters(context["quick_filters"])) if context["show_quick_filters"] else _remove_slot_block(html, "quick_filters")
        if has_expandable_fields:
            html = _replace_slot_block(html, "expanded_fields_slot", _render_filter_fields(expanded_fields))
            html = _replace_slot_block(
                html,
                "expanded_actions_slot",
                _render_filter_action_set(
                    show_filter_actions=context["show_filter_actions"],
                    has_advanced_toggle=True,
                    panel_id=advanced_panel_id,
                    expanded=True,
                ),
            )
        else:
            html = _remove_slot_block(html, "advanced_panel_slot")
        return styles, html
    if template_id == "region.action-bar":
        primary_html = ""
        if context["show_primary_group"]:
            primary_html = _render_action_group(context["toolbar_secondary_actions"], icons, context["toolbar_primary"]) or ""
        batch_html = ""
        if context["show_batch_actions"]:
            batch_html = (
                f'<span class="xftv0-action-region-status">{context["selection_status_text"]}</span>'
                f'<div class="xftv0-button-row">'
                f'{"".join(_render_button(action["label"], tone="subtle", icon=icons.get(action["icon"], "")) for action in context["toolbar_batch_actions"])}'
                "</div>"
            )
        utility_html = "".join(_render_button(action["label"], tone="subtle", icon=icons.get(action["icon"], "")) for action in context["toolbar_utility_actions"]) if context["show_utility_group"] else ""
        html = _replace_slot_block(template, "primary_group_slot", primary_html)
        html = _replace_slot_block(html, "batch_group_slot", batch_html)
        html = _replace_slot_block(html, "utility_group_slot", utility_html)
        return styles, html
    if template_id == "region.table-region":
        include_actions = bool(context["row_actions"])
        html = _remove_slot_block(template, "table_state_slot") if context["table_state"] != "empty" else template
        html = _replace_slot_block(
            html,
            "table_columns",
            _render_table_columns(context["table_columns"], show_selection=context["show_selection"], include_actions=include_actions),
        )
        html = _replace_slot_block(html, "table_rows", _render_table_rows(context, icons))
        html = _replace_slot_block(html, "pagination_slot", _render_pagination(context["pagination_mode"])) if context["pagination_mode"] != "none" else _remove_slot_block(html, "pagination_slot")
        return styles, html
    if template_id == "region.detail-section":
        return styles, template.replace("<!-- detail_blocks -->", _render_detail_blocks(context))
    if template_id == "region.form-section":
        return styles, template.replace("<!-- form_fields -->", _render_form_fields(context))
    if template_id == "region.footer-actions":
        return styles, template.replace("<!-- footer_actions -->", _render_footer_actions(context))
    if template_id == "region.result-panel":
        icon = next((item for item in page.get("icons", []) if item.get("semantic_name") == "check-circle"), {})
        return styles, _replace_tokens(
            template.replace("<!-- result_groups -->", _render_result_groups(context["result_groups"])),
            {"result_icon": _render_icon(icon), "result_summary": context["result_summary"]},
        )
    return styles, template


def _render_overlay(overlay: dict[str, Any], page: dict[str, Any], schema: dict[str, Any], context: dict[str, Any]) -> tuple[list[str], str]:
    styles, template = _load_template_with_styles(overlay["template"]["template_path"])
    template_id = overlay["template"]["template_id"]
    if template_id == "overlay.copy-modal":
        html = _replace_tokens(template, {"overlay_title": context["overlay_title_copy"], "source_text": context["source_text"]})
        html = html.replace("<!-- copy_options -->", _render_copy_options(context["copy_options"]))
        html = html.replace("<!-- target_tags -->", _render_target_tags(context["target_tags"]))
        html = html.replace(
            "<!-- overlay_actions -->",
            _render_button(COPY["cancel"], attrs=" data-overlay-close")
            + _render_button(COPY["confirm"], tone="primary", attrs=' data-overlay-open="result-modal"'),
        )
        return styles, html
    if template_id == "overlay.result-modal":
        result_styles, result_template = _render_region(
            {"template": {"template_id": "region.result-panel", "template_path": "templates/regions/result-panel.html"}},
            page,
            schema,
            context,
        )
        html = _replace_tokens(template, {"overlay_title": context["overlay_title_result"], "result_footer_note": context["result_footer_note"]})
        return styles + result_styles, html.replace("<!-- result_panel_slot -->", result_template)
    return styles, template


def _wrap_table_section(html: str) -> str:
    if not html.strip():
        return ""
    return f'<section class="xftv0-page-card xftv0-page-section">{html}</section>'


def _render_page(page: dict[str, Any], schema: dict[str, Any]) -> tuple[list[str], str]:
    page_styles, template = _load_template_with_styles(page["page_template"]["template_path"])
    context = _build_scene_context(schema, page)
    slot_html = {"header_slot": "", "filter_slot": "", "action_slot": "", "main_slot": "", "footer_slot": ""}
    collected_styles = list(page_styles)
    for region in page.get("regions", []):
        region_styles, region_html = _render_region(region, page, schema, context)
        collected_styles.extend(region_styles)
        slot_html[region["slot_id"]] = region_html

    if page["page_template"]["template_id"] == "page.table":
        for slot_id in ("header_slot", "filter_slot", "action_slot", "main_slot"):
            template = template.replace(f"<!-- {slot_id} -->", _wrap_table_section(slot_html[slot_id]))
        return collected_styles, template

    for slot_id, html in slot_html.items():
        template = template.replace(f"<!-- {slot_id} -->", html)
    return collected_styles, template


def _assemble_shell(page: dict[str, Any], page_html: str, overlay_html: str, title: str, style_blocks: list[str]) -> str:
    shell = page["shell"]
    shell_html = _read_text(ROOT / shell["path"])
    shell_html = _inject_styles(shell_html, style_blocks)
    shell_html = _inject_runtime(shell_html, shell["shell_id"], ROOT / page["runtime"]["path"])
    shell_html = shell_html.replace("<title>Enterprise Admin Side Shell</title>", f"<title>{title}</title>")
    shell_html = shell_html.replace("<title>Blank Shell</title>", f"<title>{title}</title>")
    shell_html = shell_html.replace("<!-- PAGE_CONTENT_SLOT -->", page_html)
    shell_html = shell_html.replace("<!-- CONTENT_SLOT -->", page_html)
    shell_html = shell_html.replace("<!-- OVERLAY_SLOT -->", overlay_html)
    return shell_html


def _build_page_file_name(page: dict[str, Any]) -> str:
    return f"{page['page_id']}.html"


def _build_index_html(bundle: dict[str, Any], slug: str, style_blocks: list[str]) -> str:
    links = []
    for page in bundle["pages"]:
        links.append(f'<li><a href="./pages/{_build_page_file_name(page)}">{page["page_id"]}</a> <span>({page["page_type"]})</span></li>')
    content = (
        '<section class="xftv0-page xftv0-page-card xftv0-page-section">'
        f'<h1 class="xftv0-page-title">{slug}</h1>'
        '<p class="xftv0-page-desc">XFT Design V0 output index.</p>'
        f'<ol>{"".join(links)}</ol>'
        "</section>"
    )
    shell = {"shell_id": "shell.blank", "path": bundle["index_shell"]["path"], "runtime": {"path": "assets/runtime/basic-interactions.js"}}
    shell_html = _read_text(ROOT / shell["path"])
    shell_html = _inject_styles(shell_html, style_blocks)
    shell_html = _inject_runtime(shell_html, shell["shell_id"], ROOT / shell["runtime"]["path"])
    shell_html = shell_html.replace("<title>Blank Shell</title>", f"<title>{slug} Prototype Index</title>")
    shell_html = shell_html.replace("<!-- CONTENT_SLOT -->", content)
    shell_html = shell_html.replace("<!-- OVERLAY_SLOT -->", "")
    return shell_html


def _validate_output(html: str) -> list[str]:
    issues = []
    if "PAGE_CONTENT_SLOT" in html or "OVERLAY_SLOT" in html or "CONTENT_SLOT" in html:
        issues.append("unreplaced_shell_slot")
    sanitized_html = re.sub(r'style="--xftv0-filter-label-width:\s*\d+px;"', "", html)
    if "style=" in sanitized_html:
        issues.append("inline_style_detected")
    for bad in ("custom-", "random-", "new-"):
        if bad in html:
            issues.append(f"disallowed_class_prefix:{bad}")
    hit = next((marker for marker in MOJIBAKE_MARKERS if marker in html), None)
    if hit:
        issues.append(f"mojibake_detected:{hit.encode('unicode_escape').decode()}")
    return issues


def assemble_html_plan(*, schema: dict[str, Any], bundle: dict[str, Any]) -> dict[str, Any]:
    slug = slugify(schema.get("title", schema.get("query", "xft-v0")))
    output_root = OUTPUT_DIR / slug
    pages_dir = output_root / "pages"
    output_root.mkdir(parents=True, exist_ok=True)
    pages_dir.mkdir(parents=True, exist_ok=True)

    base_styles = [
        _read_text(ROOT / "design-systems" / "tokens.css"),
        _extract_component_styles(),
        _read_text(ROOT / "templates" / "styles" / "foundation.css"),
    ]

    manifest_pages = []
    validation_notes = []

    for page in bundle["pages"]:
        page_styles, page_html = _render_page(page, schema)
        context = _build_scene_context(schema, page)
        overlay_styles: list[str] = []
        overlay_html_parts: list[str] = []
        for overlay in page.get("overlays", []):
            styles, html = _render_overlay(overlay, page, schema, context)
            overlay_styles.extend(styles)
            overlay_html_parts.append(html)
        final_html = _assemble_shell(
            page,
            page_html,
            "".join(overlay_html_parts),
            f"{context['page_title']} - {page['page_type']}",
            base_styles + page_styles + overlay_styles,
        )
        file_name = _build_page_file_name(page)
        (pages_dir / file_name).write_text(final_html, encoding="utf-8")
        validation_notes.extend(_validate_output(final_html))
        manifest_pages.append(
            {
                "page_id": page["page_id"],
                "page_type": page["page_type"],
                "file": f"pages/{file_name}",
                "shell": page["shell"]["shell_id"],
                "runtime": page["runtime"]["runtime_id"],
                "page_template": page["page_template"]["template_id"],
                "region_templates": [region["template_id"] for region in page["regions"]],
                "overlays": [overlay["template_id"] for overlay in page["overlays"]],
                "icons": [icon["semantic_name"] for icon in page["icons"]],
                "rewrite_targets": [slot["slot_id"] for slot in page["rewrite_slots"]],
            }
        )

    index_html = _build_index_html(bundle, slug, base_styles)
    (output_root / "index.html").write_text(index_html, encoding="utf-8")
    manifest = {
        "title": schema.get("title", schema.get("query", "XFT V0")),
        "slug": slug,
        "scene": schema.get("scene", "generic"),
        "pages": manifest_pages,
        "unsupported": bundle.get("unsupported", []),
        "validation": {"issues": validation_notes},
    }
    (output_root / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")

    return {
        "decision_type": "HTML_ASSEMBLY_PLAN",
        "status": "ready",
        "output_root": str(output_root),
        "pages": manifest_pages,
        "index": str(output_root / "index.html"),
        "manifest": str(output_root / "manifest.json"),
        "unsupported": bundle.get("unsupported", []),
        "validation": manifest["validation"],
    }
