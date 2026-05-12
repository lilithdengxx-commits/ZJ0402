import glob, os
ROOT = r'c:\Pros\ZJ0512'
MARKER = '<div class="sidebar-nav-area">'
bad = []
for fp in sorted(glob.glob(ROOT + r'\**\*.html', recursive=True)):
    with open(fp, 'r', encoding='utf-8') as f:
        txt = f.read()
    idx = txt.find(MARKER)
    if idx < 0:
        print('NO_NAV', os.path.relpath(fp, ROOT))
        continue
    chunk = txt[idx:idx+5000]
    has_mon = '监测预警' in chunk
    label = 'OK  ' if has_mon else 'BAD '
    if not has_mon:
        bad.append(fp)
    print(label, os.path.relpath(fp, ROOT))

print(f'\n共 {len(bad)} 个文件需要修复')
