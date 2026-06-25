# HTML 装配协议

## 装配原则

结构来自资产，内容来自需求，样式来自 token（令牌）和 support CSS（补充样式）。

## 操作顺序

```text
shell 原文
+ tokens.css
+ shell style
+ components CSS
+ support CSS
+ selected asset HTML
+ 业务字段替换
```

## 禁止事项

- 不得改 shell（壳子）结构。
- 不得把 overlay（覆盖层）插入页面内容区。
- 不得新增未知 class（类名）。
- 不得用 inline style（行内样式）修布局。
- 不得把多个区域合并成一个新结构。
- 不得删除资产里的 data-asset 标识。

## 插槽

| 插槽 | 用途 |
|---|---|
| PAGE_CONTENT_SLOT | 完整页面主体 |
| CONTENT_SLOT | 无壳子或简单页面主体 |
| OVERLAY_SLOT | 弹窗、抽屉、确认框 |
