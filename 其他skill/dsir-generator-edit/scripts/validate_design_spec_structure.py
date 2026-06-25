import sys
from pathlib import Path

text = Path(sys.argv[1]).read_text(encoding='utf-8')
required = [
    '## 页面语义摘要',
    '## 主任务',
    '## 区域与语义块',
    '## 内容模型',
    '## 关键状态与交互提示',
    '## 设计判断与待确认项',
]
for item in required:
    assert item in text, f'missing section: {item}'
for bad in ['## page_shell_specs', '## region_specs', '## module_specs', '## state_specs', '## interaction_specs']:
    assert bad not in text, f'design-spec should remain human-facing, found: {bad}'
print('DESIGN_SPEC_STRUCTURE_VALID')
