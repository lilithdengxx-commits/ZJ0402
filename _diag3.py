import os
ROOT = r'c:\Pros\ZJ0512'
files = [
    r'智能体编报\index.html',
    r'处置引导\舆情复盘分析\index.html',
    r'事件分析\事件管理\index.html',
]
out = []
for rel in files:
    fp = os.path.join(ROOT, rel)
    with open(fp, 'r', encoding='utf-8') as f:
        txt = f.read()
    has_new = '@@TOP-NAV-OVERRIDE@@' in txt
    has_header = '<header class="global-topbar">' in txt
    has_sidebar = '<aside class="sidebar">' in txt
    s = txt.find('<header')
    e = txt.find('</header>', s)
    first_line = txt[s:txt.find('\n', s)] if s != -1 else 'NO HEADER'
    out.append(f'=== {rel}')
    out.append(f'  CSS injected:  {has_new}')
    out.append(f'  has sidebar:   {has_sidebar}')
    out.append(f'  header class:  {first_line[:120]}')
    out.append('')

with open(r'c:\Pros\ZJ0512\_diag3.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(out))
print('done')
