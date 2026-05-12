with open(r'c:\Pros\ZJ0512\首页\index.html', 'r', encoding='utf-8') as f:
    txt = f.read()
pos = txt.find('<div class="sidebar-nav-area">')
snippet = txt[pos:pos+600]
with open(r'c:\Pros\ZJ0512\_out.txt', 'w', encoding='utf-8') as f:
    f.write(snippet)
print('done')
