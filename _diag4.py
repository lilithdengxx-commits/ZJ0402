import os
ROOT = r'c:\Pros\ZJ0512'

# 检查事件分析的 app-shell 和 main-area 样式
fp = os.path.join(ROOT, r'事件分析\事件管理\index.html')
with open(fp, 'r', encoding='utf-8') as f:
    txt = f.read()

# 找 app-shell 原始 CSS
import re
styles = re.findall(r'\.app-shell\{[^}]+\}', txt)
mains  = re.findall(r'\.main-area\{[^}]+\}', txt)
with open(r'c:\Pros\ZJ0512\_diag4.txt', 'w', encoding='utf-8') as f:
    f.write('app-shell styles:\n')
    for s in styles:
        f.write('  ' + s + '\n')
    f.write('\nmain-area styles:\n')
    for s in mains:
        f.write('  ' + s + '\n')

    # 检查 main-area 标签
    idx = txt.find('class="main-area"')
    f.write(f'\nmain-area tag: {txt[idx-5:idx+60]}\n')
    
    # 智能体编报的 topbar 结构
    fp2 = os.path.join(ROOT, r'智能体编报\index.html')
    with open(fp2, 'r', encoding='utf-8') as f2:
        txt2 = f2.read()
    s2 = txt2.find('<header')
    e2 = txt2.find('</header>', s2) + len('</header>')
    snippet = txt2[s2:e2]
    f.write('\n=== 智能体编报 header ===\n')
    for ln in snippet.split('\n'):
        if len(ln) < 200:
            f.write(ln + '\n')

print('done')
