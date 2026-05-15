c = open(r'c:\Pros\ZJ0512\事件分析\事件管理\index.html', encoding='utf-8').read()
lines = c.splitlines()
for i in range(1982, min(len(lines), 2010)):
    print(f'L{i+1}: {lines[i][:120]}')
