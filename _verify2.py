with open(r'c:\Pros\ZJ0512\首页\index.html', 'r', encoding='utf-8') as f:
    txt = f.read()

s = txt.find('<header class="global-topbar">')
e = txt.find('</header>', s) + len('</header>')
full = txt[s:e]
print(f'Header total length: {len(full)}')
# Print line lengths
for i, ln in enumerate(full.split('\n')):
    print(f'  line {i}: {len(ln)} chars | {ln[:80]}')
