f = r'c:\Pros\ZJ0512\事件分析\事件管理\index.html'
old = '<button type="button">分析详情</button><button type="button">复制</button><button type="button" style="color:#e04040">删除</button>'
new = '<button type="button">复制</button><button type="button">分享</button><button type="button" style="color:#e04040">删除</button>'
c = open(f, encoding='utf-8').read()
n = c.count(old)
print('matches:', n)
open(f, 'w', encoding='utf-8').write(c.replace(old, new))
print('done')
