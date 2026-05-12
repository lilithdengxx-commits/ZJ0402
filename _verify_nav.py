# -*- coding: utf-8 -*-
import re
files = [
    ('首页/index.html', '首页'),
    ('监测预警/关键对象监测/index.html', '方案监测页'),
    ('智能体编报/index.html', '智能体编报页'),
    ('处置引导/传播引导策略/index.html', '传播引导策略页'),
]
for f, label in files:
    c = open(f, encoding='utf-8').read()
    nav_start = c.find('<nav class="top-nav">')
    nav_end = c.find('</nav>', nav_start)
    nav = c[nav_start:nav_end]
    spans = re.findall(r'<span>([^<]+)</span>', nav)
    print(f'[{label}] nav labels: {spans}')

