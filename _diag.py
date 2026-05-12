import re
with open(r'c:\Pros\ZJ0512\监测预警\热点榜单\index.html', 'r', encoding='utf-8') as f:
    txt = f.read()

marker = '<div class="sidebar-nav-area">'
idx = txt.find(marker)
if idx >= 0:
    print("Found at", idx)
    print(txt[idx:idx+1500])
else:
    print("NOT FOUND")
    # show all nav-group occurrences
    for m in re.finditer(r'nav-group', txt):
        print(m.start(), txt[m.start()-30:m.start()+60])
