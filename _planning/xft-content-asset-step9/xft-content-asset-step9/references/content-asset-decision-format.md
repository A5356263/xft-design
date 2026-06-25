# CONTENT_ASSET_DECISION 输出格式

## 标准格式

```json
{
  "decision_type": "CONTENT_ASSET_DECISION",
  "query": "员工花名册列表页，支持筛选、批量导出和详情抽屉",
  "scope": "Full Page",
  "page_type": "TablePage",
  "shell": "admin-side-shell",
  "page_block": "ListPageBlock",
  "recipe": {
    "recipe_id": "recipe.table.basic",
    "recipe_name": "基础表格页",
    "default_region_order": "page-header>filter-bar>table-toolbar>data-table>pagination",
    "slot_output": "PAGE_CONTENT_SLOT",
    "validation": "必须包含表格区和分页；筛选区操作包含查询与重置"
  },
  "assets": [
    {
      "asset_id": "region.page-header.basic",
      "asset_name": "基础页面头部",
      "asset_layer": "region",
      "html_path": "assets/regions/page-header/basic.html",
      "css_path": "assets/regions/_region-support.css",
      "slot": "PAGE_CONTENT_SLOT",
      "required": true,
      "reason": "标题/说明/主操作"
    }
  ],
  "support_css": [
    "assets/regions/_region-support.css"
  ],
  "matched_rules": [
    {
      "rule_id": "toolbar-action-order",
      "asset_id": "region.table-toolbar.basic",
      "rule_type": "composition",
      "rule": "工具栏左侧放标题或统计，右侧放操作。",
      "recommended_position": "after:filter-bar"
    }
  ],
  "unsupported": [],
  "hard_checks": [
    "必须读取 recipe 中的 required assets。",
    "HTML 生成时不得自造区域布局类名。"
  ]
}
```

## 执行约束

Agent 生成页面前必须先输出该结构。  
只有 `assets[].html_path` 中列出的文件允许被读取。  
只有 `support_css[]` 中列出的 CSS 允许追加读取。  
