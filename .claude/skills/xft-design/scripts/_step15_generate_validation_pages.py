#!/usr/bin/env python3
from __future__ import annotations

import copy
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
        "nav": ["员工台账", "成员花名册", "成员列表"],
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


def load_shell() -> tuple[str, str]:
    shell_html = SHELL_PATH.read_text(encoding="utf-8")
    shell_style = extract_style_block(shell_html)
    shell_body = re.search(r"<body>(.*)</body>", shell_html, re.S).group(1)
    return shell_style, shell_body


def load_component_style() -> str:
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


def read_asset(relative_path: str) -> str:
    return (SKILL / relative_path).read_text(encoding="utf-8")


def replace_once(text: str, old: str, new: str) -> str:
    return text.replace(old, new, 1)


def asset_map(decision: dict) -> dict[str, dict]:
    return {asset["asset_id"]: asset for asset in decision.get("selected_assets", [])}


def sanitize_decision_for_comment(decision: dict) -> dict:
    safe = json.loads(json.dumps(decision, ensure_ascii=False))
    if isinstance(safe.get("recipe"), dict):
        safe["recipe"].pop("slot_output", None)
    for key in ("required_assets", "optional_assets", "selected_assets", "assets", "read_order"):
        values = safe.get(key)
        if not isinstance(values, list):
            continue
        for item in values:
            if isinstance(item, dict):
                item.pop("insert_slot", None)
    return safe


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


def build_decision_comment(decision: dict) -> str:
    return "<!-- CONTENT_ASSET_DECISION\n" + json.dumps(sanitize_decision_for_comment(decision), ensure_ascii=False, indent=2) + "\n-->"


def render_employee_required(asset_id: str, decision: dict) -> str:
    asset = asset_map(decision)[asset_id]
    html = read_asset(asset["html_path"])

    if asset_id == "region.page-header.basic":
        html = html.replace("页面标题", "员工花名册")
        html = html.replace(
            "说明当前页面的业务目标、使用范围和关键注意事项。",
            "统一维护员工信息、在职状态和组织归属，支持筛选、新增成员和查看详情；批量操作与详情抽屉按需触发。",
        )
    elif asset_id == "region.filter-bar.basic":
        html = html.replace("关键词", "成员关键词")
        html = html.replace("请输入关键词", "请输入姓名 / 手机号 / 成员编号")
        html = replace_once(html, "状态", "在职状态")
        html = replace_once(html, "请选择状态", "全部状态")
        html = html.replace("类型", "所属部门")
        html = html.replace("请选择类型", "华东销售一部 / 渠道运营组")
    elif asset_id == "region.table-toolbar.basic":
        html = html.replace("列表标题", "成员列表")
        html = html.replace("共 128 条", "共 128 名成员")
        html = replace_once(html, "导出", "导出当前筛选结果")
        html = replace_once(html, "新建", "新增成员")
    elif asset_id == "region.data-table.basic":
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
        <tr>
          <td>林清妍</td>
          <td>品牌市场部</td>
          <td>137 2222 1046</td>
          <td><span class="status-tag status-info">待入职</span></td>
          <td><span class="table-action">查看详情</span></td>
        </tr>
      </tbody>
    </table>""",
            html,
            flags=re.S,
        )
    elif asset_id == "region.pagination.basic":
        html = html.replace("共 128 条", "共 128 名成员")
    return html


def render_employee_page(decision: dict) -> tuple[dict, str, str]:
    page_asset_ids = [
        "region.page-header.basic",
        "region.filter-bar.basic",
        "region.table-toolbar.basic",
        "region.data-table.basic",
        "region.pagination.basic",
    ]
    page_html = "\n".join(render_employee_required(asset_id, decision) for asset_id in page_asset_ids)
    filtered = copy.deepcopy(decision)
    filtered["state_variant"] = "default_list"
    filtered["selected_assets"] = [asset for asset in filtered["selected_assets"] if asset["asset_id"] in page_asset_ids]
    filtered["assets"] = list(filtered["selected_assets"])
    filtered["optional_assets"] = []
    filtered["read_order"] = [item for item in filtered["read_order"] if item["asset_id"] in page_asset_ids]
    filtered["suppressed_optional_assets"] = ["module.batch-action-footer", "overlay.detail-drawer"]
    filtered["support_css"] = ["assets/content-assets/_support/region-support.css"]
    return filtered, page_html, ""


def render_approval_page(decision: dict) -> tuple[dict, str, str]:
    asset_index = asset_map(decision)
    blocks: list[str] = []
    for asset_id in [
        "region.page-header.with-actions",
        "region.detail-summary.basic",
        "module-approval-flow-basic",
        "region.detail-info-section.basic",
        "module-operation-log-basic",
        "module-related-table-basic",
    ]:
        html = read_asset(asset_index[asset_id]["html_path"])
        if asset_id == "region.page-header.with-actions":
            html = html.replace("页面标题", "差旅报销审批详情")
            html = html.replace(
                "说明当前页面的业务目标、使用范围和关键注意事项。",
                "查看差旅报销单据的基础信息、审批流、附件和操作记录，并支持审批处理。",
            )
            html = replace_once(html, "次要操作", "退回申请")
            html = replace_once(html, "主操作", "通过审批")
        elif asset_id == "region.detail-summary.basic":
            html = html.replace("状态", "审批状态")
            html = html.replace("已完成", "审批中")
            html = html.replace("负责人", "当前处理人")
            html = html.replace("张三", "李倩")
            html = html.replace("发起时间", "提交时间")
            html = html.replace("业务编号", "报销单号")
            html = html.replace("NO.20260615001", "BX-20260624-018")
        elif asset_id == "module-approval-flow-basic":
            html = html.replace("审批流程", "审批流")
            html = html.replace("查看流转记录", "查看完整流转")
        elif asset_id == "region.detail-info-section.basic":
            html = html.replace("基础信息", "报销基础信息")
            html = html.replace("字段名称", "申请人", 1)
            html = html.replace("字段内容", "王晨逸", 1)
            html = html.replace("字段名称", "所属部门", 1)
            html = html.replace("字段内容", "战略客户部", 1)
            html = html.replace("字段名称", "出差城市", 1)
            html = html.replace("字段内容", "上海 -> 深圳", 1)
            html = html.replace("字段名称", "报销金额", 1)
            html = html.replace("字段内容", "¥ 8,420.00", 1)
        elif asset_id == "module-operation-log-basic":
            html = html.replace("操作记录", "审批操作记录")
        elif asset_id == "module-related-table-basic":
            html = html.replace("关联数据", "关联报销明细")
            html = html.replace("查看全部", "查看全部明细")
        blocks.append(html)

    attachment_viewer = """
<section class="module-card" data-module="approval-attachment-viewer">
  <div class="module-header">
    <div>
      <div class="module-title">审批附件</div>
      <div class="module-meta">默认展示随单附件，供审批人预览、下载和查看，不进入上传或补正语义。</div>
    </div>
  </div>
  <div class="module-body">
    <div class="file-list">
      <div class="file-item">
        <div class="file-main">
          <div class="file-name">差旅发票汇总.pdf</div>
          <div class="file-meta">PDF · 2.1MB · 最近上传：2026-06-24 09:28</div>
        </div>
        <div class="file-actions">
          <span class="table-action">预览</span>
          <span class="table-action">下载</span>
          <span class="table-action">查看</span>
        </div>
      </div>
      <div class="file-item">
        <div class="file-main">
          <div class="file-name">费用明细.xlsx</div>
          <div class="file-meta">Excel · 860KB · 最近上传：2026-06-24 09:29</div>
        </div>
        <div class="file-actions">
          <span class="table-action">预览</span>
          <span class="table-action">下载</span>
          <span class="table-action">查看</span>
        </div>
      </div>
    </div>
  </div>
</section>"""
    blocks.append(attachment_viewer)

    filtered = copy.deepcopy(decision)
    filtered["selected_assets"] = [asset for asset in filtered["selected_assets"] if asset["asset_id"] != "module-upload-file-basic"]
    filtered["assets"] = list(filtered["selected_assets"])
    filtered["optional_assets"] = [asset for asset in filtered["optional_assets"] if asset["asset_id"] != "module-upload-file-basic"]
    filtered["read_order"] = [item for item in filtered["read_order"] if item["asset_id"] != "module-upload-file-basic"]
    filtered["semantic_override"] = {"approval_attachment_region": "view_download_preview"}
    return filtered, "\n".join(blocks), ""


def render_settings_page(decision: dict) -> tuple[dict, str, str]:
    asset_index = asset_map(decision)
    header = read_asset(asset_index["region.page-header.basic"]["html_path"])
    header = header.replace("页面标题", "参数配置中心")
    header = header.replace(
        "说明当前页面的业务目标、使用范围和关键注意事项。",
        "集中管理参数配置、状态开关和配置操作，左侧锚点与右侧分组保持一一对应。",
    )

    layout = """
<div class="settings-layout" data-xft-region="settings-layout" data-xft-variant="anchor">
  <aside class="settings-anchor">
    <div class="settings-anchor-item is-active">基础参数</div>
    <div class="settings-anchor-item">状态策略</div>
    <div class="settings-anchor-item">立即调整操作</div>
  </aside>
  <div>
    <section class="settings-section">
      <div class="settings-section-title">基础参数</div>
      <div class="setting-item">
        <div class="setting-main">
          <div class="setting-title">默认同步规则</div>
          <div class="setting-description">生效范围：成员基础资料、部门归属和岗位信息。<br />修改影响：调整后影响新同步任务的频率与重试顺序。<br />最近变更：2026-06-20 由系统管理员更新为“每日 02:00 自动同步”。</div>
        </div>
        <div class="setting-status"><button class="btn btn-secondary" type="button">立即调整</button></div>
      </div>
      <div class="setting-item">
        <div class="setting-main">
          <div class="setting-title">字段冲突处理</div>
          <div class="setting-description">生效范围：成员手机号、工号和邮箱的重复校验。<br />修改影响：切换为“人工确认优先”后，冲突记录会进入待处理队列。<br />最近变更：2026-06-18 新增“保留旧值并提醒”策略。</div>
        </div>
        <div class="setting-status"><button class="btn btn-secondary" type="button">配置规则</button></div>
      </div>
    </section>
    <section class="settings-section" data-xft-region="setting-section" data-xft-variant="basic">
      <div class="settings-section-title">状态策略</div>
      <div class="setting-item">
        <div class="setting-main">
          <div class="setting-title">允许成员批量导入</div>
          <div class="setting-description">生效范围：运营、HR 和系统管理员角色。<br />修改影响：开启后允许通过模板一次性导入成员资料，并进入异步校验流程。<br />最近变更：2026-06-23 已将模板字段扩展到 24 项。</div>
        </div>
        <div class="setting-status"><button class="switch is-checked" type="button"><span class="switch-handle"></span></button></div>
      </div>
      <div class="setting-item">
        <div class="setting-main">
          <div class="setting-title">异常同步提醒</div>
          <div class="setting-description">生效范围：成员同步失败、字段缺失和重复数据。<br />修改影响：开启后向系统管理员发送站内通知，并保留处理入口。<br />最近变更：2026-06-24 新增“仅提醒负责人”选项。</div>
        </div>
        <div class="setting-status"><button class="btn btn-secondary" type="button">配置规则</button></div>
      </div>
    </section>
    <section class="settings-section" data-xft-region="setting-section" data-xft-variant="basic">
      <div class="settings-section-title">立即调整操作</div>
      <div class="setting-item">
        <div class="setting-main">
          <div class="setting-title">重跑成员同步</div>
          <div class="setting-description">生效范围：最近 24 小时内失败的成员同步任务。<br />修改影响：会重新执行字段映射与冲突校验，并生成新的任务日志。<br />最近变更：2026-06-25 09:40 有 3 个失败任务待重跑。</div>
        </div>
        <div class="setting-status"><button class="btn btn-primary" type="button">立即执行</button></div>
      </div>
      <div class="setting-item">
        <div class="setting-main">
          <div class="setting-title">导出当前参数快照</div>
          <div class="setting-description">生效范围：当前参数中心全部分组。<br />修改影响：导出后可用于审计留档或跨环境对比。<br />最近变更：2026-06-22 已支持导出最近修改人信息。</div>
        </div>
        <div class="setting-status"><button class="btn btn-secondary" type="button">导出快照</button></div>
      </div>
    </section>
  </div>
</div>"""

    filtered = copy.deepcopy(decision)
    filtered["semantic_override"] = {"anchor_sections": ["基础参数", "状态策略", "立即调整操作"]}
    return filtered, "\n".join([header, layout]), ""


def render_modal_overlay() -> str:
    return """
<div class="xft-overlay-root" data-overlay="functional-modal" data-asset="overlay.modal.functional">
  <div class="xft-overlay-mask"></div>
  <div class="xft-overlay-center">
    <section class="xft-modal-panel" role="dialog" aria-modal="true">
      <header class="xft-modal-header">
        <h2 class="xft-overlay-title">编辑成员信息</h2>
        <button class="btn btn-text" type="button">关闭</button>
      </header>
      <div class="xft-modal-body">
        <p class="xft-overlay-description">在当前列表上下文中快速编辑成员基础信息，保持轻量编辑，不跳转到完整创建页或编辑页。</p>
        <div class="form-grid">
          <div class="form-field">
            <label class="field-label">成员姓名</label>
            <input class="input" value="陈语安" />
          </div>
          <div class="form-field">
            <label class="field-label">所属部门</label>
            <select class="input">
              <option selected>华东销售一部</option>
              <option>渠道运营组</option>
              <option>品牌市场部</option>
            </select>
          </div>
          <div class="form-field">
            <label class="field-label">手机号</label>
            <input class="input" value="138 0000 2048" />
          </div>
          <div class="form-field">
            <label class="field-label">在职状态</label>
            <select class="input">
              <option selected>在职</option>
              <option>试用中</option>
              <option>待入职</option>
            </select>
          </div>
        </div>
      </div>
      <footer class="xft-modal-footer">
        <button class="btn btn-secondary" type="button">取消编辑</button>
        <button class="btn btn-primary" type="button">保存成员信息</button>
      </footer>
    </section>
  </div>
</div>"""


def render_modal_page(decision: dict, employee_decision: dict) -> tuple[dict, str, str]:
    background_filtered, background_html, _ = render_employee_page(employee_decision)
    filtered = copy.deepcopy(decision)
    filtered["background_context"] = "employee_roster"
    filtered["background_context_assets"] = [asset["asset_id"] for asset in background_filtered["selected_assets"]]
    return filtered, background_html, render_modal_overlay()


def prepare_case(case_name: str, decision: dict, employee_decision: dict | None = None) -> tuple[dict, str, str]:
    if case_name == "employee-roster":
        return render_employee_page(decision)
    if case_name == "approval-detail":
        return render_approval_page(decision)
    if case_name == "settings-config":
        return render_settings_page(decision)
    if case_name == "member-edit-modal" and employee_decision is not None:
        return render_modal_page(decision, employee_decision)
    return decision, "", ""


def assemble_page(case: dict, decision: dict, page_html: str, overlay_html: str) -> str:
    shell_style, shell_body = load_shell()
    tokens_css = TOKENS_PATH.read_text(encoding="utf-8")
    component_css = load_component_style()
    support_css = read_support_css(decision.get("support_css", []))

    body = shell_body.replace("页面标签", case["nav"][0], 1)
    body = body.replace("当前页面", case["nav"][1], 1)
    body = body.replace("页面标签 B", case["nav"][2], 1)
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
    decisions = {case["name"]: run_decision(case["query"]) for case in CASES}
    employee_decision = decisions["employee-roster"]

    results = []
    for case in CASES:
        prepared_decision, page_html, overlay_html = prepare_case(case["name"], decisions[case["name"]], employee_decision)
        html = assemble_page(case, prepared_decision, page_html, overlay_html)
        out_path = OUTPUT / case["filename"]
        out_path.write_text(html, encoding="utf-8", newline="\n")
        check = subprocess.run(["python", str(CHECK_SCRIPT), str(out_path)], cwd=ROOT, capture_output=True)
        results.append(
            {
                "name": case["name"],
                "file": str(out_path.relative_to(ROOT)).replace("\\", "/"),
                "recipe_id": prepared_decision.get("recipe_id"),
                "scope": prepared_decision.get("scope"),
                "overlay_type": prepared_decision.get("overlay_type") or None,
                "page_type": prepared_decision.get("page_type"),
                "selected_assets": [asset["asset_id"] for asset in prepared_decision.get("selected_assets", [])],
                "unsupported": prepared_decision.get("unsupported", []),
                "check_exit_code": check.returncode,
                "check_output": decode_output(check.stdout + check.stderr).strip(),
            }
        )

    report_path = OUTPUT / "xft-real-page-validation-step15-2026-06-25.json"
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
