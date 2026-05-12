with open(r'c:\Pros\ZJ0512\首页\index.html', 'r', encoding='utf-8') as f:
    txt = f.read()

# Check topbar
s = txt.find('<header class="global-topbar">')
e = txt.find('</header>', s) + len('</header>')
snippet = txt[s:e]
with open(r'c:\Pros\ZJ0512\_verify.txt', 'w', encoding='utf-8') as f:
    for ln in snippet.split('\n'):
        if len(ln) < 250:
            f.write(ln + '\n')

# Check sidebar removed
has_sidebar = '<aside class="sidebar">' in txt
has_marker  = '@@TOP-NAV-OVERRIDE@@' in txt
print(f'sidebar removed: {not has_sidebar}')
print(f'CSS injected:    {has_marker}')
print(f'topbar-brand:    {"topbar-brand" in txt}')
print(f'top-nav:         {"top-nav-item" in txt}')
