c = open(r'c:\Pros\ZJ0512\事件分析\事件管理\index.html', encoding='utf-8').read()
ids_to_check = ['toastStack', 'appShell', 'menuButton', 'mobileMask', 'cardGrid', 'createButton', 'sortSelect', 'templateSelect', 'searchInput', 'searchCount']
for id in ids_to_check:
    found = ('id="%s"' % id) in c
    print(f'{id}: {"FOUND" if found else "MISSING"}')
