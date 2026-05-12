# -*- coding: utf-8 -*-
import re

files = ['监测预警/热点榜单/index.html', '事件分析/事件管理/index.html']
for f in files:
    c = open(f, encoding='utf-8').read()
    tag = '<div class="topbar-actions">'
    i = c.find(tag)
    if i >= 0:
        print('===', f)
        print(c[i:i+800])
        print()
    else:
        print(f, ': NOT FOUND')
