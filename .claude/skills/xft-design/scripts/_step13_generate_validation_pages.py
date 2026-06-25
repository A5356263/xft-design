#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
SKILL = ROOT / ".claude" / "skills" / "xft-design"
OUTPUT = ROOT / "output"
SEARCH_SCRIPT = SKILL / "scripts" / "search_content_assets.py"
CHECK_SCRIPT = SKILL / "scripts" / "check_skill_output.py"
DATA_DIR = SKILL / "data" / "content-assets"
SHELL_PATH = SKILL / "assets" / "shells" / "admin-side-shell.html"
TOKENS_PATH = SKILL / "design-systems" / "tokens.css"
COMPONENTS_PATH = SKILL / "design-systems" / "components.html"

CASES = [
    {
        "name": "employee-roster",
        "title": "员工花名册",
        "filename": "employee-roster-validation-2026-06-25-v2.html",
        "query": "员工花名册列表页，支持筛选、批量导出、新增成员、查看详情",
        "nav": ["员工台账", "成员花名册", "批量导出"],
    },
    {
        "name": "approval-detail",
        "title": "差旅报销审批详情",
        "filename": "approval-detail-validation-2026-06-25-v2.html",
        "query": "审批详情页，包含基础信息、审批流、附件、操作记录",
        "nav": ["审批中心", "待办审批", "审批详情"],
    },
    {
        "name": "settings-config",
        "title": "参数配置中心",
        "filename": "settings-config-validation-2026-06-25-v2.html",
        "query": "参数配置设置页，包含左侧锚点、设置分组、状态和配置操作",
        "nav": ["系统设置", "参数中心", "参数配置"],
    },
    {
        "name": "member-edit-modal",
        "title": "成员信息编辑",
        "filename": "member-edit-modal-validation-2026-06-25-v2.html",
        "query": "弹窗编辑成员信息",
        "nav": ["员工台账", "成员花名册", "成员编辑弹窗"],
    },
]


def decode_output(raw: bytes) -> str:
    for encoding in ("utf-8", "utf-8-sig", "gbk"):
        try:
            return raw.decode(encoding)
        except UnicodeDecodeError:
            continue
    return raw.decode("utf-8", errors="ignore")


def extract_style_block(html: str) -> str:
    match = re.search(r"<style>(.*?)</style>", html, re.S)
    return match.group(1).strip() if match else ""


def shell_parts() -> tuple[str, str, str]:
    shell_html = SHELL_PATH.read_text(encoding="utf-8")
    shell_style = extract_style_block(shell_html)
    shell_body = re.search(r"<body>(.*)</body>", shell_html, re.S).group(1)
    return shell_html, shell_style, shell_body


def components_style() -> str:
    return extract_style_block(COMPONENTS_PATH.read_text(encoding="utf-8"))


def read_support_css(paths: list[str]) -> str:
    seen: set[str] = set()
    blocks: list[str] = []
    for rel_path in paths:
        if not rel_path or rel_path in seen:
            continue
        seen.add(rel_path)
        css_path = SKILL / rel_path
        if css_path.exists():
            blocks.append(css_path.read_text(encoding="utf-8"))
    return "\n\n".join(blocks)


def run_decision(query: str) -> dict:
    raw = subprocess.check_output(
        ["python", str(SEARCH_SCRIPT), query, "--data-dir", str(DATA_DIR)],
        cwd=ROOT,
    )
    return json.loads(decode_output(raw))


def replace_once(text: str, old: str, new: str) -> str:
    return text.replace(old, new, 1)


def render_asset(asset: dict, case_name: str) -> str:
    html = (SKILL / asset["html_path"]).read_text(encoding="utf-8")

    if case_name == "employee-roster":
        if asset["asset_id"] == "region.page-header.basic":
            html = html.replace("页面标题", "员工花名册")
            html = html.replace(
                "说明当前页面的业务目标、使用范围和关键注意事项。",
                "统一维护员工信息、在职状态和组织归属，支持筛选、批量导出、新增成员和查看详情。",
            )
        elif asset["asset_id"] == "region.filter-bar.basic":
            html = html.replace("关键词", "成员关键词")
            html = html.replace("请输入关键词", "请输入姓名 / 手机号 / 成员编号")
            html = replace_once(html, "状态", "在职状态")
            html = replace_once(html, "请选择状态", "全部状态")
            html = html.replace("类型", "所属部门")
            html = html.replace("请选择类型", "全部部门")
        elif asset["asset_id"] == "region.table-toolbar.basic":
            html = html.replace("列表标题", "成员列表")
            html = html.replace("共 128 条", "共 128 名成员")
            html = replace_once(html, "导出", "批量导出")
            html = replace_once(html, "新建", "新增成员")
        elif asset["asset_id"] == "region.data-table.basic":
            html = re.sub(
                r"<table class=\"data-table\">.*?</table>",
                """<table class="data-table">
      <thead>
        <tr>
          <th>成员姓名</th>
          <th>所属部门</th>
          <th>手机号</th>
          <th>在职状态</th>
          <th>操作</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>陈语安</td>
          <td>华东销售一部</td>
          <td>138 0000 2048</td>
          <td><span class="status-tag status-success">在职</span></td>
          <td><span class="table-action">查看详情</span></td>
        </tr>
        <tr>
          <td>周柏廷</td>
          <td>渠道运营组</td>
          <td>139 0000 6612</td>
          <td><span class="status-tag status-warning">试用中</span></td>
          <td><span class="table-action">查看详情</span></td>
        </tr>
      </tbody>
    </table>""",
                html,
                flags=re.S,
            )
        elif asset["asset_id"] == "region.pagination.basic":
            html = html.replace("共 128 条", "共 128 名成员")
        elif asset["asset_id"] == "module.batch-action-footer":
            html = html.replace(
                "已选择 <strong>12</strong> 名成员",
                "已选择 <strong>12</strong> 名成员，准备统一导出与状态调整",
            )
    elif case_name == "approval-detail":
        if asset["asset_id"] == "region.page-header.with-actions":
            html = html.replace("页面标题", "差旅报销审批详情")
            html = html.replace(
                "说明当前页面的业务目标、使用范围和关键注意事项。",
                "查看差旅报销单据的基础信息、审批流、附件和操作记录，并支持审批处理。",
            )
            html = replace_once(html, "次要操作", "退回申请")
            html = replace_once(html, "主操作", "通过审批")
        elif asset["asset_id"] == "region.detail-summary.basic":
            html = html.replace("状态", "审批状态")
            html = html.replace("已完成", "审批中")
            html = html.replace("负责人", "当前处理人")
            html = html.replace("张三", "李倩")
            html = html.replace("发起时间", "提交时间")
            html = html.replace("业务编号", "报销单号")
            html = html.replace("NO.20260615001", "BX-20260624-018")
        elif asset["asset_id"] == "module-approval-flow-basic":
            html = html.replace("审批流程", "审批流")
            html = html.replace("查看流转记录", "查看完整流转")
        elif asset["asset_id"] == "region.detail-info-section.basic":
            html = html.replace("基础信息", "报销基础信息")
            html = html.replace("字段名称", "申请人", 1)
            html = html.replace("字段内容", "王晨逸", 1)
            html = html.replace("字段名称", "所属部门", 1)
            html = html.replace("字段内容", "战略客户部", 1)
            html = html.replace("字段名称", "出差城市", 1)
            html = html.replace("字段内容", "上海 -> 深圳", 1)
            html = html.replace("字段名称", "报销金额", 1)
            html = html.replace("字段内容", "¥ 8,420.00", 1)
        elif asset["asset_id"] == "module-operation-log-basic":
            html = html.replace("操作记录", "审批操作记录")
        elif asset["asset_id"] == "module-upload-file-basic":
            html = html.replace("上传文件", "审批附件")
            html = html.replace(
                "支持拖拽或点击上传，上传后在下方展示文件状态。",
                "展示当前报销单据随附的发票、行程单和补充说明。",
            )
            html = html.replace("将文件拖到此处，或点击上传", "附件预览与补充材料")
            html = html.replace(
                "支持 PDF、Excel、图片，单个文件不超过 20MB",
                "支持发票图片、PDF 和 Excel 附件，保留最近上传版本。",
            )
            html = html.replace("选择文件", "补传附件")
        elif asset["asset_id"] == "module-related-table-basic":
            html = html.replace("关联数据", "关联报销明细")
            html = html.replace("查看全部", "查看全部明细")
    elif case_name == "settings-config":
        if asset["asset_id"] == "region.page-header.basic":
            html = html.replace("页面标题", "参数配置中心")
            html = html.replace(
                "说明当前页面的业务目标、使用范围和关键注意事项。",
                "集中管理参数配置、状态开关和配置操作，左侧锚点与右侧分组保持一一对应。",
            )
        elif asset["asset_id"] == "region.settings-layout.anchor":
            html = html.replace("基础设置", "基础参数")
            html = html.replace("通知设置", "状态策略")
            html = html.replace("权限设置", "配置操作")
            html = html.replace("设置项标题", "默认同步规则")
            html = html.replace(
                "说明配置项开启或关闭后的影响。",
                "控制成员数据与组织架构的默认同步频率，并说明变更后的生效范围。",
            )
            html = html.replace("配置", "立即调整")
        elif asset["asset_id"] == "region.setting-section.basic":
            html = html.replace("设置分组标题", "状态与操作策略")
            html = html.replace("设置项标题", "允许成员批量导入", 1)
            html = html.replace(
                "设置项说明文案，解释开启或关闭后的影响。",
                "开启后允许管理员通过模板一次性导入成员资料。",
                1,
            )
            html = html.replace("设置项标题", "异常同步提醒", 1)
            html = html.replace(
                "设置项说明文案。",
                "同步异常时向系统管理员发送站内通知，并保留处理入口。",
                1,
            )
            html = html.replace("配置", "配置规则")
    elif case_name == "member-edit-modal" and asset["asset_id"] == "OV_MODAL_FUNCTIONAL":
        html = html.replace("功能操作", "编辑成员信息")
        html = html.replace(
            "适用于短流程表单、简单编辑或信息补充。",
            "在当前列表上下文中快速编辑成员基础信息，不跳转到完整创建页或编辑页。",
        )
        html = re.sub(
            r"<div class=\"form-grid\">.*?</div>\s*</div>\s*<footer",
            """<div class="form-grid">
          <div class="form-field">
            <label class="field-label">成员姓名</label>
            <input class="input" value="陈语安" />
          </div>
          <div class="form-field">
            <label class="field-label">所属部门</label>
            <div class="select-control">华东销售一部</div>
          </div>
          <div class="form-field">
            <label class="field-label">手机号</label>
            <input class="input" value="138 0000 2048" />
          </div>
          <div class="form-field">
            <label class="field-label">在职状态</label>
            <div class="select-control">在职</div>
          </div>
        </div>
      </div>
      <footer""",
            html,
            flags=re.S,
        )
        html = html.replace("取消", "取消编辑")
        html = html.replace("确定", "保存成员信息")

    return html


def build_route_comment(decision: dict) -> str:
    return "\n".join(
        [
            "<!-- XFT_ROUTE",
            f"scope: {decision.get('scope', '')}",
            f"page_type: {decision.get('page_type', '')}",
            f"recipe_id: {decision.get('recipe_id', '')}",
            f"shell: {decision.get('shell', '')}",
            f"overlay_type: {decision.get('overlay_type') or 'None'}",
            "-->",
        ]
    )


def sanitize_decision_for_html(decision: dict) -> dict:
    safe = json.loads(json.dumps(decision, ensure_ascii=False))
    recipe = safe.get("recipe")
    if isinstance(recipe, dict):
        recipe.pop("slot_output", None)
    for key in ("required_assets", "optional_assets", "selected_assets", "assets", "read_order"):
        values = safe.get(key)
        if not isinstance(values, list):
            continue
        for item in values:
            if isinstance(item, dict):
                item.pop("insert_slot", None)
    return safe


def build_decision_comment(decision: dict) -> str:
    safe = sanitize_decision_for_html(decision)
    return "<!-- CONTENT_ASSET_DECISION\n" + json.dumps(safe, ensure_ascii=False, indent=2) + "\n-->"


def assemble(case: dict, decision: dict) -> str:
    _, shell_style, shell_body = shell_parts()
    tokens_css = TOKENS_PATH.read_text(encoding="utf-8")
    component_css = components_style()
    support_css = read_support_css(decision.get("support_css", []))
    page_assets = [asset for asset in decision["selected_assets"] if asset.get("insert_slot") == "PAGE_CONTENT_SLOT"]
    overlay_assets = [asset for asset in decision["selected_assets"] if asset.get("insert_slot") == "OVERLAY_SLOT"]

    page_html = "\n".join(render_asset(asset, case["name"]) for asset in page_assets)
    overlay_html = "\n".join(render_asset(asset, case["name"]) for asset in overlay_assets)

    body = shell_body.replace("页面标签", case["nav"][0])
    body = body.replace("当前页面", case["nav"][1])
    body = body.replace("页面标签 B", case["nav"][2])
    body = body.replace("<!-- PAGE_CONTENT_SLOT -->", page_html or '<div class="page-card"></div>')
    body = body.replace("<!-- OVERLAY_SLOT -->", overlay_html)

    return "\n".join(
        [
            "<!DOCTYPE html>",
            build_route_comment(decision),
            '<html lang="zh-CN">',
            "<head>",
            '  <meta charset="UTF-8" />',
            '  <meta name="viewport" content="width=device-width, initial-scale=1.0" />',
            f"  <title>{case['title']}</title>",
            "  <style>",
            tokens_css,
            "  </style>",
            "  <style>",
            component_css,
            "  </style>",
            "  <style>",
            support_css,
            "  </style>",
            "  <style>",
            shell_style,
            "  </style>",
            "</head>",
            "<body>",
            "  " + build_decision_comment(decision).replace("\n", "\n  "),
            body,
            "</body>",
            "</html>",
        ]
    )


def main() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    results = []
    for case in CASES:
        decision = run_decision(case["query"])
        html = assemble(case, decision)
        out_path = OUTPUT / case["filename"]
        out_path.write_text(html, encoding="utf-8", newline="\n")
        check = subprocess.run(["python", str(CHECK_SCRIPT), str(out_path)], cwd=ROOT, capture_output=True)
        results.append(
            {
                "name": case["name"],
                "file": str(out_path.relative_to(ROOT)).replace("\\", "/"),
                "recipe_id": decision.get("recipe_id"),
                "scope": decision.get("scope"),
                "overlay_type": decision.get("overlay_type") or None,
                "page_type": decision.get("page_type"),
                "selected_assets": [asset["asset_id"] for asset in decision.get("selected_assets", [])],
                "unsupported": decision.get("unsupported", []),
                "check_exit_code": check.returncode,
                "check_output": decode_output(check.stdout + check.stderr).strip(),
            }
        )

    report_path = OUTPUT / "xft-real-page-validation-step13-2026-06-25.json"
    report_path.write_text(
        json.dumps({"generated_on": "2026-06-25", "results": results}, ensure_ascii=False, indent=2),
        encoding="utf-8",
        newline="\n",
    )
    print(
        json.dumps(
            {"report": str(report_path.relative_to(ROOT)).replace("\\", "/"), "results": results},
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
