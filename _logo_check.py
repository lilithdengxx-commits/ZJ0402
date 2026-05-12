with open(r'c:\Pros\ZJ0512\首页\index.html', 'r', encoding='utf-8') as f:
    txt = f.read()

m = '<div class="topbar-brand">'
idx = txt.find(m)
print('topbar-brand at:', idx)
end = txt.find('</div>', idx + len(m))
inner = txt[idx+len(m):end]
print('inner length:', len(inner))
print('inner[:200]:', inner[:200])
