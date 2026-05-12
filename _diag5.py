import os, re
ROOT = r'c:\Pros\ZJ0512'
files = [r'智能体编报\index.html', r'处置引导\舆情复盘分析\index.html']
out = []
for rel in files:
    fp = os.path.join(ROOT, rel)
    with open(fp, 'r', encoding='utf-8') as f:
        txt = f.read()
    # 找所有 topbar 相关 CSS
    styles = re.findall(r'[^{]*topbar[^{]*\{[^}]+\}', txt)
    out.append(f'=== {rel}')
    for s in styles[:10]:
        if len(s) < 300:
            out.append('  ' + s.replace('\n',' ').strip())
    out.append('')

with open(r'c:\Pros\ZJ0512\_diag5.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(out))
print('done')
