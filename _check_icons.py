# -*- coding: utf-8 -*-
import re, os

files = [
    '首页/index.html',
    '监测预警/AI智能推荐/index.html',
    '监测预警/信息监测/index.html',
    '监测预警/关键对象监测/index.html',
    '监测预警/热点榜单/index.html',
    '监测预警/预警查询/index.html',
    '事件分析/事件管理/index.html',
    '事件分析/事件管理/创建分析/index.html',
    '事件分析/事件管理/事件分析详情/index.html',
    '智能体编报/index.html',
    '处置引导/传播引导策略/index.html',
    '处置引导/选题线索池/index.html',
    '处置引导/多稿合并工具/index.html',
    '处置引导/舆情复盘分析/index.html',
    '处置引导/舆情复盘分析/复盘详情/index.html',
    '处置引导/舆情复盘分析/新建复盘任务/index.html',
    '智能检索/index.html',
    '知识库/热点话题案例库/index.html',
]
for f in files:
    c = open(f, encoding='utf-8').read()
    m = re.search(r'class="topbar-actions"(.*?)</header>', c, re.S)
    if m:
        snippet = re.sub(r'\s+', ' ', m.group(1))
        has_task = '\u4efb\u52a1\u4e2d\u5fc3' in snippet
        has_star_btn = 'title="\u6536\u85cf"' in snippet
        has_bell_msg = 'title="\u6d88\u606f"' in snippet
        print(f'{f}: task_center={has_task}, star_btn={has_star_btn}, msg_bell={has_bell_msg}')
    else:
        print(f'{f}: topbar-actions NOT FOUND\n')
