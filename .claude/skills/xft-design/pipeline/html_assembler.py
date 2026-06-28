"""Assemble V0 prototype outputs from fixed templates."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT.parents[2] / "output"


def slugify(text: str) -> str:
    base = re.sub(r"\s+", "-", text.strip().lower())
    base = re.sub(r"[^a-z0-9\u4e00-\u9fff-]+", "-", base)
    return re.sub(r"-{2,}", "-", base).strip("-") or "xft-v0"


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _extract_style_block(html: str) -> str:
    match = re.search(r"<style[^>]*>(.*?)</style>", html, flags=re.S | re.I)
    return match.group(1).strip() if match else ""


def _inject_styles(shell_html: str, style_blocks: list[str]) -> str:
    insertion = "".join(f"\n  <style>\n{block}\n  </style>" for block in style_blocks if block.strip())
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


def _render_icon(icon: dict[str, str]) -> str:
    path = ROOT / icon.get("path", "")
    return _read_text(path) if path.exists() else ""


def _render_filter_fields() -> str:
    fields = [
        ("姓名", "请输入姓名"),
        ("手机号", "请输入手机号"),
        ("部门", "请选择部门"),
        ("状态", "请选择状态"),
    ]
    parts = []
    for label, placeholder in fields:
        control = (
            f'<input class="xftv0-input" type="text" placeholder="{placeholder}" />'
            if "请选择" not in placeholder
            else f'<select class="xftv0-select"><option>{placeholder}</option></select>'
        )
        parts.append(
            f'<div class="xftv0-field"><span class="xftv0-field-label">{label}</span>{control}</div>'
        )
    return "".join(parts)


def _render_table_columns(columns: list[str]) -> str:
    head = "".join(f"<th>{item}</th>" for item in columns)
    return f"<tr>{head}</tr>"


def _render_table_rows(actions: str, context: dict[str, Any]) -> str:
    rows = context.get("sample_rows", [])
    parts = []
    for row in rows:
        tds = "".join(f"<td>{value}</td>" for value in row)
        parts.append(f"<tr>{tds}<td>{actions}</td></tr>")
    return "".join(parts)


def _render_row_actions(page: dict[str, Any]) -> str:
    icon_map = {icon.get("semantic_name"): _render_icon(icon) for icon in page.get("icons", [])}
    return "".join(
        [
            f'<button class="xftv0-table-link" type="button" data-overlay-open="copy-modal"><span class="xftv0-icon">{icon_map.get("copy","")}</span>复制</button>',
            f'<button class="xftv0-table-link" type="button"><span class="xftv0-icon">{icon_map.get("edit","")}</span>编辑</button>',
            f'<button class="xftv0-table-link" type="button"><span class="xftv0-icon">{icon_map.get("delete","")}</span>移除</button>',
        ]
    )


def _render_detail_blocks(context: dict[str, Any]) -> str:
    parts = []
    for label, value in context.get("detail_blocks", []):
        parts.append(
            f'<div class="xftv0-description-item"><span class="xftv0-description-label">{label}</span><span class="xftv0-description-value">{value}</span></div>'
        )
    return "".join(parts)


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
        parts.append(
            f'<div class="xftv0-field{width_class}"><span class="xftv0-field-label">{field["label"]}</span>{control}</div>'
        )
    return "".join(parts)


def _render_footer_actions(context: dict[str, Any]) -> str:
    buttons = []
    for action in context.get("footer_actions", []):
        cls = "xftv0-button"
        if action["role"] == "primary":
            cls += " xftv0-button-primary"
        elif action["role"] == "danger":
            cls += " xftv0-button-danger"
        buttons.append(f'<button class="{cls}" type="button">{action["label"]}</button>')
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


def _build_scene_context(schema: dict[str, Any], page: dict[str, Any]) -> dict[str, Any]:
    scene = schema.get("scene", "generic")
    title = schema.get("title", schema.get("query", "XFT V0"))
    if scene == "copy_permission":
        return {
            "page_title": "子管理员权限复制",
            "page_description": "在列表中选择来源子管理员，并通过弹窗将授权范围复制给目标用户。",
            "page_badge": "V0 原型",
            "toolbar_title": "子管理员列表",
            "toolbar_primary": "添加子管理员",
            "sample_columns": ["姓名", "手机号", "部门", "可授权组织", "可授权功能"],
            "sample_rows": [
                ["王琳", "138****1024", "华东运营", "门店经营组", "商品管理、活动管理"],
                ["张衡", "139****6632", "渠道增长", "KA 客户组", "订单审批、数据看板"],
            ],
            "detail_blocks": [
                ("复制来源", "王琳 / 138****1024"),
                ("目标用户数", "3 人"),
                ("授权组织", "门店经营组、加盟管理组"),
                ("授权功能", "商品管理、活动管理、订单审批"),
            ],
            "form_fields": [
                {"label": "来源管理员", "placeholder": "请选择来源子管理员", "kind": "select"},
                {"label": "目标用户", "placeholder": "请选择复制对象", "kind": "select"},
                {"label": "复制说明", "placeholder": "请输入备注说明", "kind": "textarea", "wide": True},
            ],
            "footer_actions": [
                {"label": "取消", "role": "secondary"},
                {"label": "确认", "role": "primary"},
            ],
            "copy_options": ["可授权组织", "可授权功能"],
            "target_tags": ["用户 A", "用户 B", "用户 C"],
            "result_summary": "复制完成，成功 3 人，失败 0 人。",
            "result_groups": [
                {"title": "新增子管理员（2）", "items": ["用户 A / 138****2101", "用户 B / 137****6623"]},
                {"title": "权限已叠加（1）", "items": ["用户 C / 136****7741"]},
            ],
            "source_text": "复制来源：王琳 / 138****1024",
            "overlay_title_copy": "复制子管理员权限",
            "overlay_title_result": "复制结果",
            "result_footer_note": "关闭弹窗后返回列表并刷新展示结果。",
        }
    return {
        "page_title": title,
        "page_description": "基于结构化 design spec 生成的 V0 原型页面。",
        "page_badge": "V0 原型",
        "toolbar_title": title,
        "toolbar_primary": "新增",
        "sample_columns": ["字段一", "字段二", "字段三"],
        "sample_rows": [["示例值", "示例值", "示例值"]],
        "detail_blocks": [("字段一", "示例值"), ("字段二", "示例值")],
        "form_fields": [{"label": "字段一", "placeholder": "请输入字段一", "kind": "text"}],
        "footer_actions": [{"label": "确认", "role": "primary"}],
        "copy_options": ["选项 A"],
        "target_tags": ["对象 A"],
        "result_summary": "处理完成。",
        "result_groups": [{"title": "结果", "items": ["示例项"]}],
        "source_text": "来源信息",
        "overlay_title_copy": "确认操作",
        "overlay_title_result": "处理结果",
        "result_footer_note": "关闭后返回页面。",
    }


def _render_region(region: dict[str, Any], page: dict[str, Any], schema: dict[str, Any], context: dict[str, Any]) -> str:
    template = _read_text(ROOT / region["template"]["template_path"])
    template_id = region["template"]["template_id"]
    if template_id == "region.page-header":
        return _replace_tokens(
            template,
            {
                "page_title": context["page_title"],
                "page_description": context["page_description"],
                "page_badge": context["page_badge"],
            },
        )
    if template_id == "region.filter-bar":
        return template.replace("<!-- filter_fields -->", _render_filter_fields())
    if template_id == "region.table-region":
        row_actions = _render_row_actions(page)
        html = _replace_tokens(
            template,
            {
                "toolbar_title": context["toolbar_title"],
                "toolbar_primary": context["toolbar_primary"],
            },
        )
        html = html.replace("<!-- table_columns -->", _render_table_columns(context["sample_columns"] + ["操作"]))
        html = html.replace("<!-- table_rows -->", _render_table_rows(row_actions, context))
        return html
    if template_id == "region.detail-section":
        return template.replace("<!-- detail_blocks -->", _render_detail_blocks(context))
    if template_id == "region.form-section":
        return template.replace("<!-- form_fields -->", _render_form_fields(context))
    if template_id == "region.footer-actions":
        return template.replace("<!-- footer_actions -->", _render_footer_actions(context))
    if template_id == "region.result-panel":
        icon = next((item for item in page.get("icons", []) if item.get("semantic_name") == "check-circle"), {})
        return _replace_tokens(
            template.replace("<!-- result_groups -->", _render_result_groups(context["result_groups"])),
            {
                "result_icon": _render_icon(icon),
                "result_summary": context["result_summary"],
            },
        )
    return template


def _render_overlay(overlay: dict[str, Any], page: dict[str, Any], schema: dict[str, Any], context: dict[str, Any]) -> str:
    template = _read_text(ROOT / overlay["template"]["template_path"])
    template_id = overlay["template"]["template_id"]
    if template_id == "overlay.copy-modal":
        html = _replace_tokens(
            template,
            {
                "overlay_title": context["overlay_title_copy"],
                "source_text": context["source_text"],
            },
        )
        html = html.replace("<!-- copy_options -->", _render_copy_options(context["copy_options"]))
        html = html.replace("<!-- target_tags -->", _render_target_tags(context["target_tags"]))
        html = html.replace(
            "<!-- overlay_actions -->",
            '<button class="xftv0-button" type="button" data-overlay-close>取消</button>'
            '<button class="xftv0-button xftv0-button-primary" type="button" data-overlay-open="result-modal">确认</button>',
        )
        return html
    if template_id == "overlay.result-modal":
        result_panel_template = {
            "template": {"template_id": "region.result-panel", "template_path": "templates/regions/result-panel.html"}
        }
        result_panel = _render_region(result_panel_template, page, schema, context)
        html = _replace_tokens(
            template,
            {
                "overlay_title": context["overlay_title_result"],
                "result_footer_note": context["result_footer_note"],
            },
        )
        return html.replace("<!-- result_panel_slot -->", result_panel)
    return template


def _render_page(page: dict[str, Any], schema: dict[str, Any]) -> str:
    template = _read_text(ROOT / page["page_template"]["template_path"])
    context = _build_scene_context(schema, page)
    slot_html = {"header_slot": "", "filter_slot": "", "main_slot": "", "footer_slot": ""}
    for region in page.get("regions", []):
        slot_html[region["slot_id"]] = _render_region(region, page, schema, context)
    for slot_id, html in slot_html.items():
        template = template.replace(f"<!-- {slot_id} -->", html)
    return template


def _assemble_shell(page: dict[str, Any], page_html: str, overlay_html: str, title: str) -> str:
    shell = page["shell"]
    shell_html = _read_text(ROOT / shell["path"])
    tokens_css = _read_text(ROOT / "design-systems" / "tokens.css")
    components_css = _extract_style_block(_read_text(ROOT / "design-systems" / "components.html"))
    template_css = _read_text(ROOT / "templates" / "styles" / "v0-prototype.css")
    shell_html = _inject_styles(shell_html, [tokens_css, components_css, template_css])
    shell_html = _inject_runtime(shell_html, shell["shell_id"], ROOT / page["runtime"]["path"])
    shell_html = shell_html.replace("<title>Enterprise Admin Side Shell</title>", f"<title>{title}</title>")
    shell_html = shell_html.replace("<title>Blank Shell</title>", f"<title>{title}</title>")
    shell_html = shell_html.replace("<!-- PAGE_CONTENT_SLOT -->", page_html)
    shell_html = shell_html.replace("<!-- CONTENT_SLOT -->", page_html)
    shell_html = shell_html.replace("<!-- OVERLAY_SLOT -->", overlay_html)
    return shell_html


def _build_page_file_name(page: dict[str, Any]) -> str:
    return f"{page['page_id']}.html"


def _build_index_html(bundle: dict[str, Any], slug: str) -> str:
    links = []
    for page in bundle["pages"]:
        title = page["page_id"]
        links.append(
            f'<li><a href="./pages/{_build_page_file_name(page)}">{title}</a> <span>({page["page_type"]})</span></li>'
        )
    content = (
        '<section class="xftv0-page xftv0-page-card xftv0-page-section">'
        f'<h1 class="xftv0-page-title">{slug}</h1>'
        '<p class="xftv0-page-desc">XFT Design V0 输出索引。</p>'
        f'<ol>{"".join(links)}</ol>'
        '</section>'
    )
    shell = {
        "shell_id": "shell.blank",
        "path": bundle["index_shell"]["path"],
        "runtime": {"path": "assets/runtime/basic-interactions.js"},
    }
    shell_html = _read_text(ROOT / shell["path"])
    tokens_css = _read_text(ROOT / "design-systems" / "tokens.css")
    components_css = _extract_style_block(_read_text(ROOT / "design-systems" / "components.html"))
    template_css = _read_text(ROOT / "templates" / "styles" / "v0-prototype.css")
    shell_html = _inject_styles(shell_html, [tokens_css, components_css, template_css])
    shell_html = _inject_runtime(shell_html, shell["shell_id"], ROOT / shell["runtime"]["path"])
    shell_html = shell_html.replace("<title>Blank Shell</title>", f"<title>{slug} Prototype Index</title>")
    shell_html = shell_html.replace("<!-- CONTENT_SLOT -->", content)
    shell_html = shell_html.replace("<!-- OVERLAY_SLOT -->", "")
    return shell_html


def _validate_output(html: str, known_classes: list[str]) -> list[str]:
    issues = []
    if "PAGE_CONTENT_SLOT" in html or "OVERLAY_SLOT" in html or "CONTENT_SLOT" in html:
        issues.append("unreplaced_shell_slot")
    if "style=" in html:
        issues.append("inline_style_detected")
    for bad in ("custom-", "random-", "new-"):
        if bad in html:
            issues.append(f"disallowed_class_prefix:{bad}")
    return issues


def assemble_html_plan(
    *,
    schema: dict[str, Any],
    bundle: dict[str, Any],
) -> dict[str, Any]:
    slug = slugify(schema.get("title", schema.get("query", "xft-v0")))
    output_root = OUTPUT_DIR / slug
    pages_dir = output_root / "pages"
    output_root.mkdir(parents=True, exist_ok=True)
    pages_dir.mkdir(parents=True, exist_ok=True)

    manifest_pages = []
    validation_notes = []

    for page in bundle["pages"]:
        page_html = _render_page(page, schema)
        context = _build_scene_context(schema, page)
        overlay_html = "".join(_render_overlay(overlay, page, schema, context) for overlay in page.get("overlays", []))
        title = f"{context['page_title']} - {page['page_type']}"
        final_html = _assemble_shell(page, page_html, overlay_html, title)
        file_name = _build_page_file_name(page)
        (pages_dir / file_name).write_text(final_html, encoding="utf-8")
        validation_notes.extend(_validate_output(final_html, []))
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

    index_html = _build_index_html(bundle, slug)
    (output_root / "index.html").write_text(index_html, encoding="utf-8")
    manifest = {
        "title": schema.get("title", schema.get("query", "XFT V0")),
        "slug": slug,
        "scene": schema.get("scene", "generic"),
        "pages": manifest_pages,
        "unsupported": bundle.get("unsupported", []),
        "validation": {
            "issues": validation_notes,
        },
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
