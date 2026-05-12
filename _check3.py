import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

with open(r'c:\Pros\ZJ0512\首页\index.html', 'r', encoding='utf-8') as f:
    txt = f.read()
MARKER = '<div class="sidebar-nav-area">'
pos = txt.find(MARKER)
# 提取完整 nav-area
depth = 1
p = pos + len(MARKER)
end = -1
while p < len(txt) and depth > 0:
    no = txt.find('<div', p)
    nc = txt.find('</div>', p)
    if nc == -1:
        break
    if no != -1 and no < nc and txt[no+4:no+5] in ' \t\n\r>':
        depth += 1
        p = no + 4
    else:
        depth -= 1
        if depth == 0:
            end = nc + 6
            break
        p = nc + 6
nav_html = txt[pos:end] if end > 0 else txt[pos:pos+5000]
# Write to temp file instead
with open(r'c:\Pros\ZJ0512\_nav_dump.txt', 'w', encoding='utf-8') as f:
    f.write(nav_html)
print('Written to _nav_dump.txt, len:', len(nav_html))
