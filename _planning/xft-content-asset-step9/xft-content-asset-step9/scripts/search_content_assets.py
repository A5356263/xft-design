#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
XFT 内容资产检索原型。

用途：
- 根据用户需求选择 page_type、recipe_id。
- 根据 recipe-asset-map 补齐必选资产。
- 根据关键词和规则选择可选资产。
- 输出 CONTENT_ASSET_DECISION JSON，供 skill 工作流读取。

注意：这是 Step 9 的可执行原型。Codex 接入项目时可直接复制到
.claude/skills/xft-design/scripts/search_content_assets.py，并根据实际目录微调 DATA_DIR。
"""
from __future__ import annotations

import argparse
import csv
import json
import math
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"


def read_csv(path: Path) -> List[Dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def normalize(text: Any) -> str:
    return str(text or "").lower().strip()


def tokenize(text: Any) -> List[str]:
    """中文友好的轻量 token（词元）切分。"""
    raw = normalize(text)
    if not raw:
        return []
    parts = re.split(r"[\s,，;；/、>｜|:：()（）\[\]{}<>《》\-]+", raw)
    tokens: List[str] = []
    for part in parts:
        if not part:
            continue
        tokens.append(part)
        # 中文连续文本没有空格，补 2/3 字符 ngram（片段）提高命中率。
        if re.search(r"[\u4e00-\u9fff]", part) and len(part) >= 3:
            for n in (2, 3):
                tokens.extend(part[i : i + n] for i in range(0, len(part) - n + 1))
    return [t for t in tokens if len(t) >= 2]


class BM25:
    def __init__(self, docs: List[str], k1: float = 1.5, b: float = 0.75):
        self.k1 = k1
        self.b = b
        self.docs_tokens = [tokenize(d) for d in docs]
        self.doc_lens = [len(d) for d in self.docs_tokens]
        self.avgdl = sum(self.doc_lens) / len(self.doc_lens) if self.doc_lens else 0
        self.idf: Dict[str, float] = {}
        df: Counter[str] = Counter()
        for doc in self.docs_tokens:
            for token in set(doc):
                df[token] += 1
        n_docs = len(self.docs_tokens)
        for token, freq in df.items():
            self.idf[token] = math.log((n_docs - freq + 0.5) / (freq + 0.5) + 1)

    def scores(self, query: str) -> List[float]:
        query_tokens = tokenize(query)
        out: List[float] = []
        for doc, doc_len in zip(self.docs_tokens, self.doc_lens):
            tf = Counter(doc)
            score = 0.0
            for token in query_tokens:
                if token not in self.idf:
                    continue
                freq = tf[token]
                denom = freq + self.k1 * (1 - self.b + self.b * doc_len / (self.avgdl or 1))
                score += self.idf[token] * (freq * (self.k1 + 1)) / (denom or 1)
            out.append(score)
        return out


def weighted_doc(row: Dict[str, str], fields: Iterable[str]) -> str:
    return " ".join(row.get(f, "") for f in fields)


def keyword_bonus(query: str, row: Dict[str, str], fields: Iterable[str], weight: float = 1.0) -> float:
    """直接子串命中奖励，弥补中文分词不稳定。"""
    q_tokens = set(tokenize(query))
    text = normalize(" ".join(row.get(f, "") for f in fields))
    score = 0.0
    for token in q_tokens:
        if token and token in text:
            score += weight
    return score


def negative_penalty(query: str, row: Dict[str, str], field: str = "negative_keywords") -> float:
    q = normalize(query)
    negs = tokenize(row.get(field, ""))
    if any(n in q for n in negs):
        return -100.0
    return 0.0


def rank_rows(query: str, rows: List[Dict[str, str]], fields: List[str], max_results: int = 5) -> List[Tuple[float, Dict[str, str]]]:
    if not rows:
        return []
    docs = [weighted_doc(r, fields) for r in rows]
    bm25 = BM25(docs)
    bm25_scores = bm25.scores(query)
    ranked: List[Tuple[float, Dict[str, str]]] = []
    for row, bm25_score in zip(rows, bm25_scores):
        score = bm25_score + keyword_bonus(query, row, fields, 1.5) + negative_penalty(query, row)
        try:
            score += float(row.get("priority", 0)) / 100.0
        except ValueError:
            pass
        ranked.append((score, row))
    ranked.sort(key=lambda x: x[0], reverse=True)
    return [item for item in ranked[:max_results] if item[0] > 0]


def load_data(data_dir: Path) -> Dict[str, List[Dict[str, str]]]:
    return {
        "page_router": read_csv(data_dir / "page-type-router.csv"),
        "recipes": read_csv(data_dir / "recipe-rules.csv"),
        "recipe_asset_map": read_csv(data_dir / "recipe-asset-map.csv"),
        "assets": read_csv(data_dir / "content-assets.csv"),
        "rules": read_csv(data_dir / "asset-rules.csv"),
        "keywords": read_csv(data_dir / "asset-keywords.csv"),
        "support_css": read_csv(data_dir / "support-css-manifest.csv"),
    }



def explicit_page_type(query: str) -> str | None:
    q = normalize(query)
    # 明确页面名优先。注意“查看详情”只是列表页常见操作，不等于详情页。
    if any(k in q for k in ["列表页", "表格页", "台账", "花名册", "数据管理", "查询页"]):
        if not any(k in q for k in ["详情页", "审批详情页", "单据详情页"]):
            return "TablePage"
    if any(k in q for k in ["详情页", "审批详情页", "单据详情页", "查看页"]):
        return "DetailPage"
    if any(k in q for k in ["表单页", "新建页", "创建页", "申请页", "提单"]):
        return "CreatePage"
    if any(k in q for k in ["编辑页", "修改页", "维护页"]):
        return "EditPage"
    if any(k in q for k in ["设置页", "配置页", "参数配置", "权限配置", "公式配置"]):
        return "SettingsPage"
    if any(k in q for k in ["首页", "工作台", "仪表盘", "看板"]):
        return "HomePage"
    if any(k in q for k in ["报表页", "统计分析", "查询报表"]):
        return "ReportPage"
    return None

def select_page_route(query: str, data: Dict[str, List[Dict[str, str]]]) -> Dict[str, str]:
    explicit = explicit_page_type(query)
    routers = data["page_router"]
    if explicit:
        routers = [r for r in routers if r.get("page_type") == explicit] or data["page_router"]
    ranked = rank_rows(query, routers, ["match_keywords", "page_type", "recipe_id", "notes"], 5)
    if ranked:
        return ranked[0][1]
    return {"page_type": "TablePage", "recipe_id": "recipe.table.basic", "scope": "Full Page", "shell": "admin-side-shell"}



def explicit_recipe_id(query: str, page_type: str) -> str | None:
    q = normalize(query)
    if page_type == "TablePage":
        if any(k in q for k in ["卡片表格", "卡片列表", "图文列表"]):
            return "recipe.table.card"
        if any(k in q for k in ["可编辑表格", "行内编辑", "批量录入", "明细维护"]):
            return "recipe.table.editable"
        if any(k in q for k in ["父子", "主从", "左树右表", "树表", "左侧树"]):
            return "recipe.table.parent-child"
        if any(k in q for k in ["汇总", "总览", "指标+表格"]):
            return "recipe.table.summary"
        if any(k in q for k in ["多栏表格", "复杂表格", "宽表"]):
            return "recipe.table.multi-column"
        if any(k in q for k in ["列表页", "表格页", "花名册", "台账", "数据管理"]):
            return "recipe.table.basic"
    if page_type == "CreatePage":
        if any(k in q for k in ["分步", "步骤", "多步骤"]):
            return "recipe.form.step"
    if page_type == "SettingsPage":
        if any(k in q for k in ["公式", "公式配置", "公式编辑"]):
            # 当前没有专用 recipe 时仍回退设置页基础配方，模块由可选资产补齐。
            return "recipe.settings.basic"
    return None

def select_recipe(query: str, page_type: str, preferred_recipe_id: str, data: Dict[str, List[Dict[str, str]]]) -> Dict[str, str]:
    recipes = [r for r in data["recipes"] if r.get("page_type") == page_type]
    explicit_recipe = explicit_recipe_id(query, page_type) or preferred_recipe_id
    for row in recipes:
        if row.get("recipe_id") == explicit_recipe:
            return row
    ranked = rank_rows(query, recipes, ["recipe_name", "keywords", "default_region_order", "required_regions", "optional_modules"], 5)
    if ranked:
        return ranked[0][1]
    for row in data["recipes"]:
        if row.get("recipe_id") == preferred_recipe_id:
            return row
    return {"recipe_id": preferred_recipe_id, "page_type": page_type, "recipe_name": preferred_recipe_id}


def assets_by_id(data: Dict[str, List[Dict[str, str]]]) -> Dict[str, Dict[str, str]]:
    return {r.get("asset_id", ""): r for r in data["assets"] if r.get("asset_id")}


def select_required_assets(recipe_id: str, data: Dict[str, List[Dict[str, str]]]) -> List[Dict[str, Any]]:
    asset_index = assets_by_id(data)
    rows = [r for r in data["recipe_asset_map"] if r.get("recipe_id") == recipe_id]
    rows.sort(key=lambda r: int(r.get("asset_order") or 999))
    selected = []
    for r in rows:
        asset = asset_index.get(r.get("candidate_asset_id", ""))
        if not asset:
            selected.append({"asset_id": r.get("candidate_asset_id"), "status": "missing", "reason": "recipe_required_but_not_found"})
            continue
        selected.append({
            "asset_id": asset.get("asset_id"),
            "asset_name": asset.get("asset_name"),
            "asset_layer": asset.get("asset_layer"),
            "asset_type": asset.get("asset_type"),
            "variant": asset.get("variant"),
            "html_path": asset.get("html_path"),
            "css_path": asset.get("css_path"),
            "slot": r.get("slot") or asset.get("slots"),
            "required": (r.get("required", "").lower() == "true"),
            "reason": r.get("notes", "recipe asset map"),
        })
    return selected


def select_optional_assets(query: str, recipe: Dict[str, str], required_ids: set[str], data: Dict[str, List[Dict[str, str]]]) -> List[Dict[str, Any]]:
    page_type = recipe.get("page_type", "")
    candidates = [a for a in data["assets"] if a.get("page_type") in (page_type, "Any", "") and a.get("asset_id") not in required_ids]
    ranked = rank_rows(query, candidates, ["asset_name", "keywords", "conditions", "validation", "notes"], 12)
    optional = []
    for score, asset in ranked:
        if score < 2:
            continue
        optional.append({
            "asset_id": asset.get("asset_id"),
            "asset_name": asset.get("asset_name"),
            "asset_layer": asset.get("asset_layer"),
            "asset_type": asset.get("asset_type"),
            "variant": asset.get("variant"),
            "html_path": asset.get("html_path"),
            "css_path": asset.get("css_path"),
            "slot": asset.get("slots"),
            "required": False,
            "score": round(score, 3),
            "reason": "keyword/rule matched optional asset",
        })
    return optional[:8]


def matched_rules(query: str, page_type: str, asset_ids: set[str], data: Dict[str, List[Dict[str, str]]]) -> List[Dict[str, str]]:
    rows = []
    for r in data["rules"]:
        if r.get("page_type") not in (page_type, "Any", ""):
            continue
        if r.get("asset_id") and r.get("asset_id") not in asset_ids:
            continue
        rows.append(r)
    ranked = rank_rows(query, rows, ["rule_name", "rule", "keywords", "recommended_position"], 20)
    return [r for score, r in ranked]


def support_css_paths(assets: List[Dict[str, Any]]) -> List[str]:
    seen = []
    for asset in assets:
        css = asset.get("css_path")
        if css and css not in seen:
            seen.append(css)
    return seen


def build_decision(query: str, data_dir: Path = DATA_DIR) -> Dict[str, Any]:
    data = load_data(data_dir)
    route = select_page_route(query, data)
    page_type = route.get("page_type", "TablePage")
    recipe = select_recipe(query, page_type, route.get("recipe_id", ""), data)
    required = select_required_assets(recipe.get("recipe_id", ""), data)
    required_ids = {a.get("asset_id", "") for a in required}
    optional = select_optional_assets(query, recipe, required_ids, data)
    all_assets = required + optional
    asset_ids = {a.get("asset_id", "") for a in all_assets}
    rules = matched_rules(query, page_type, asset_ids, data)

    return {
        "decision_type": "CONTENT_ASSET_DECISION",
        "query": query,
        "scope": route.get("scope", "Full Page"),
        "page_type": page_type,
        "shell": route.get("shell", "admin-side-shell"),
        "page_block": route.get("page_block", "None"),
        "recipe": {
            "recipe_id": recipe.get("recipe_id"),
            "recipe_name": recipe.get("recipe_name"),
            "default_region_order": recipe.get("default_region_order"),
            "slot_output": recipe.get("slot_output", "PAGE_CONTENT_SLOT"),
            "validation": recipe.get("validation", ""),
        },
        "assets": all_assets,
        "support_css": support_css_paths(all_assets),
        "matched_rules": [
            {
                "rule_id": r.get("rule_id"),
                "asset_id": r.get("asset_id"),
                "rule_type": r.get("rule_type"),
                "rule": r.get("rule"),
                "recommended_position": r.get("recommended_position"),
            }
            for r in rules[:12]
        ],
        "unsupported": [a for a in all_assets if a.get("status") == "missing"],
        "hard_checks": [
            "必须读取 recipe 中的 required assets。",
            "必须读取 support_css 中列出的 CSS。",
            "HTML 生成时不得自造区域布局类名。",
            "缺失资产进入 unsupported，不得现场发明。",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Search XFT content assets and output CONTENT_ASSET_DECISION JSON.")
    parser.add_argument("query", help="用户页面需求")
    parser.add_argument("--data-dir", default=str(DATA_DIR), help="数据表目录")
    parser.add_argument("--pretty", action="store_true", help="格式化 JSON 输出")
    args = parser.parse_args()

    decision = build_decision(args.query, Path(args.data_dir))
    print(json.dumps(decision, ensure_ascii=False, indent=2 if args.pretty else None))


if __name__ == "__main__":
    main()
