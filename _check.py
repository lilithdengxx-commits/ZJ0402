with open(r'c:\Pros\ZJ0512\首页\index.html', 'r', encoding='utf-8') as f:
    txt = f.read()
MARKER = '<div class="sidebar-nav-area">'
pos = txt.find(MARKER)
print('pos:', pos)
print(txt[pos:pos+800])
