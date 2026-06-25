# 执行风险与禁止事项

## 最大风险

### 1. 把资产接入做成纯文档

错误做法：只把 `references` 放进去，不复制 HTML（超文本标记语言）资产。

正确做法：必须复制 `assets/content-assets/`，否则 AI（人工智能）仍然会瞎写布局。

### 2. 把旧 page-block 当主路径

错误做法：继续优先使用 `assets/page-blocks.html`。

正确做法：旧 page-block 只能 fallback（兜底），主路径必须是内容资产检索。

### 3. 没有校验路径

错误做法：脚本返回了 `html_path`，但真实文件不存在。

正确做法：检索后必须验证 `read_order` 中的路径存在。

### 4. 重写 shell

错误做法：为了适配内容区，改 `assets/shells/admin-side-shell.html`。

正确做法：内容资产必须适配 shell，不允许 shell 适配内容资产。

## 禁止事项

- 禁止删除旧资产。
- 禁止改 token（令牌）。
- 禁止自造随机 class（类名）。
- 禁止让 AI 读取全部资产后自行判断。
- 禁止无 `CONTENT_ASSET_DECISION` 直接生成 HTML。
