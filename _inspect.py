import os
files = [r'首页\index.html', r'处置引导\传播引导策略\index.html']
for f in files:
    fp = os.path.join(r'c:\Pros\ZJ0512', f)
    with open(fp, 'r', encoding='utf-8') as fh:
        txt = fh.read()
    s = txt.find('<header class="global-topbar">')
    e = txt.find('</header>', s) + len('</header>')
    snippet = txt[s:e]
    with open(r'c:\Pros\ZJ0512\_topbar_check.txt', 'a', encoding='utf-8') as out:
        out.write(f'=== {f} ===\n')
        for ln in snippet.split('\n'):
            if len(ln) < 300:
                out.write(ln + '\n')
        out.write('\n')
print('done')
