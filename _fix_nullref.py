# -*- coding: utf-8 -*-
"""修复 menuButton/mobileMask null 引用问题"""
import re, os

# 已手工修复的文件
already_fixed = {'事件分析/事件管理/index.html'}

files = [
    '事件分析/事件管理/事件分析详情/index.html',
    '事件分析/事件管理/创建分析/index.html',
    '处置引导/选题线索池/index.html',
    '智能检索/index.html',
    '监测预警/AI智能推荐/index.html',
]

# 匹配 menuButton.addEventListener... mobileMask.addEventListener 块（宽松匹配）
PATTERN = re.compile(
    r'(\s*)(menuButton\.addEventListener\("click".*?);'
    r'(\s*menuButton\.addEventListener\("keydown",.*?\}\s*\}\s*\);)'
    r'(\s*)(mobileMask\.addEventListener\("click",.*?\}\s*\);)',
    re.S
)

def wrap_null_guards(content):
    def replacer(m):
        indent = m.group(1).lstrip('\n') or '        '
        menu_click = m.group(1) + m.group(2) + ';'
        menu_keydown = m.group(3)
        mask_click = m.group(4) + m.group(5)

        result = (
            m.group(1) + 'if (menuButton) {\n'
            + '    ' + indent + m.group(2).strip() + ';\n'
            + '    ' + indent + m.group(3).strip() + '\n'
            + indent + '}\n'
            + m.group(4) + 'if (mobileMask) {\n'
            + '    ' + indent + m.group(5).strip() + '\n'
            + indent + '}'
        )
        return result
    return PATTERN.sub(replacer, content)

for f in files:
    path = f
    if not os.path.exists(path):
        print(f'SKIP (not found): {f}')
        continue
    c = open(path, encoding='utf-8').read()
    if 'if (menuButton)' in c:
        print(f'ALREADY FIXED: {f}')
        continue
    if 'menuButton.addEventListener' not in c:
        print(f'NO MATCH: {f}')
        continue
    new_c = wrap_null_guards(c)
    if new_c == c:
        print(f'NO CHANGE (pattern mismatch): {f}')
        continue
    open(path, 'w', encoding='utf-8').write(new_c)
    print(f'FIXED: {f}')
