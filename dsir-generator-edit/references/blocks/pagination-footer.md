# `pagination_footer（分页底部块）`

## 定义

用于表达结果集合的分页、页大小切换和结果数量提示。

## 语义目标

- 切换结果页
- 表达当前结果规模
- 控制每页条数

## 允许出现的区域

- `primary_content（主内容区）`

## 最小语义载荷

- `total_count（总数）`
- `page_slice（页切片）`
- `page_size_options（页大小选项）`

## 使用的 `content model（内容模型）`

- `pagination_context（分页上下文）`

## 能力范围

- `page_switching（翻页）`
- `page_size_switching（页大小切换）`
- `result_summary（结果摘要）`

## 已确认变体

- 当前首批不单独定义固定变体

## 不应混入的内容

- 表格主体
- 筛选条件
- 业务主动作

## 常见搭配

- `record_table（记录表格块）`
