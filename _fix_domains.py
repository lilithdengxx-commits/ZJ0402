# -*- coding: utf-8 -*-
import re

with open(r'c:\Pros\ZJ0512\监测预警\AI智能推荐\index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# ─────────────────────────────────────────────────────────────
# 1. Replace domainHierarchy
# ─────────────────────────────────────────────────────────────
old_hierarchy = '''        const domainHierarchy = [
            { id: "hot-topic", label: "热点议题", children: ["立选", "地区治理", "社会调查", "政府动态", "八项规定", "热点问题", "社会热点"] },
            { id: "domain-dynamic", label: "领域动态", children: ["两岸", "青年", "创科", "法律", "医卫", "网安", "会计", "教育"] },
            { id: "person-dynamic", label: "人物动态", children: ["政府官员", "立法会", "人大政协", "知名人士", "区议会", "关键人"] },
            { id: "hot-general", label: "热点事件", children: ["管制动态", "案件关注", "热点事件", "社评个评", "调查报告", "国安关注", "外部动向"] },
            { id: "special-monitor", label: "专项监测", children: ["机构舆情", "竞对动态", "行业舆情"] },
            { id: "key-focus", label: "关键关注", children: ["涉港澳突发事件", "关键部门", "关键事件"] }
        ];'''

new_hierarchy = '''        const domainHierarchy = [
            { id: "key-focus", label: "关键关注", children: ["涉港澳突发事件", "关键部门", "关键事件", "案件关注"] },
            { id: "special-monitor", label: "行业洞察", children: ["机构舆情", "竞对动态", "行业业态"] },
            { id: "hot-topic", label: "热点议题", children: ["立选", "地区治理", "政府动态", "八项规定", "民意调研"] },
            { id: "domain-dynamic", label: "领域动态", children: ["两岸关系", "青年发展", "科创产业", "法律法治", "医疗卫生", "网络安全", "财会财税", "教育文教"] },
            { id: "person-dynamic", label: "人物动态", children: ["政府官员", "立法会议员", "人大代表", "区议会议员", "知名人士", "关键重点人"] }
        ];'''

if old_hierarchy in content:
    content = content.replace(old_hierarchy, new_hierarchy)
    print('✓ domainHierarchy replaced')
else:
    print('✗ domainHierarchy NOT FOUND')

# ─────────────────────────────────────────────────────────────
# 2. Rename special-monitor label in event data
# ─────────────────────────────────────────────────────────────
content = content.replace('domainLabel: "专项监测"', 'domainLabel: "行业洞察"')
content = content.replace('"专项监测","竞对动态"', '"行业洞察","竞对动态"')
content = content.replace('"专项监测","机构舆情"', '"行业洞察","机构舆情"')
content = content.replace('"专项监测","行业舆情"', '"行业洞察","行业业态"')
print('✓ special-monitor label renamed to 行业洞察')

# ─────────────────────────────────────────────────────────────
# 3. Remap hot-general events → key-focus / 案件关注
# ─────────────────────────────────────────────────────────────
# Detailed event e4
content = content.replace(
    'domainId: "hot-general", domainLabel: "热点综合", domainL2: "案件关注"',
    'domainId: "key-focus", domainLabel: "关键关注", domainL2: "案件关注"'
)
# All mk() generated hot-general events → key-focus / 案件关注
def remap_hotgeneral(text):
    return re.sub(r'"hot-general","热点综合","[^"]*"', '"key-focus","关键关注","案件关注"', text)

before = content.count('"hot-general"')
content = remap_hotgeneral(content)
after = content.count('"hot-general"')
print(f'✓ hot-general remapped: {before - after} occurrences replaced')

# ─────────────────────────────────────────────────────────────
# 4. Update domain-dynamic L2 labels (old short → new full)
# ─────────────────────────────────────────────────────────────
l2_renames = [
    ('"domain-dynamic","领域动态综合","两岸"',   '"domain-dynamic","领域动态综合","两岸关系"'),
    ('"domain-dynamic","领域动态综合","青年"',   '"domain-dynamic","领域动态综合","青年发展"'),
    ('"domain-dynamic","领域动态综合","创科"',   '"domain-dynamic","领域动态综合","科创产业"'),
    ('"domain-dynamic","领域动态综合","法律"',   '"domain-dynamic","领域动态综合","法律法治"'),
    ('"domain-dynamic","领域动态综合","医卫"',   '"domain-dynamic","领域动态综合","医疗卫生"'),
    ('"domain-dynamic","领域动态综合","网安"',   '"domain-dynamic","领域动态综合","网络安全"'),
    ('"domain-dynamic","领域动态综合","会计"',   '"domain-dynamic","领域动态综合","财会财税"'),
    ('"domain-dynamic","领域动态综合","教育"',   '"domain-dynamic","领域动态综合","教育文教"'),
    # Also the detailed e7 event
    ('domainL2: "创科"', 'domainL2: "科创产业"'),
]
for old, new in l2_renames:
    cnt = content.count(old)
    content = content.replace(old, new)
    if cnt:
        print(f'✓ {old[:40]} → {new.split(",")[-1]}  ({cnt}x)')

# ─────────────────────────────────────────────────────────────
# 5. Update person-dynamic L2 labels
# ─────────────────────────────────────────────────────────────
person_renames = [
    ('"person-dynamic","人物动态综合","立法会"',   '"person-dynamic","人物动态综合","立法会议员"'),
    ('"person-dynamic","人物动态综合","人大政协"', '"person-dynamic","人物动态综合","人大代表"'),
    ('"person-dynamic","人物动态综合","区议会"',   '"person-dynamic","人物动态综合","区议会议员"'),
    ('"person-dynamic","人物动态综合","关键人"',   '"person-dynamic","人物动态综合","关键重点人"'),
]
for old, new in person_renames:
    cnt = content.count(old)
    content = content.replace(old, new)
    if cnt:
        print(f'✓ {old.split(",")[-1].strip()} → {new.split(",")[-1]}  ({cnt}x)')

# ─────────────────────────────────────────────────────────────
# 6. Update hot-topic L2 labels
# ─────────────────────────────────────────────────────────────
topic_renames = [
    ('"hot-topic","热点议题综合","社会调查"', '"hot-topic","热点议题综合","民意调研"'),
    ('"hot-topic","热点议题综合","热点问题"', '"hot-topic","热点议题综合","民意调研"'),
    ('"hot-topic","热点议题综合","社会热点"', '"hot-topic","热点议题综合","民意调研"'),
]
for old, new in topic_renames:
    cnt = content.count(old)
    content = content.replace(old, new)
    if cnt:
        print(f'✓ {old.split(",")[-1].strip()} → 民意调研  ({cnt}x)')

# Fix e3 detailed event domainL2
content = content.replace('domainL2: "社会调查"', 'domainL2: "民意调研"')
print('✓ e3 domainL2 社会调查 → 民意调研')

# ─────────────────────────────────────────────────────────────
# 7. Update default domainL1 to key-focus (first in new order)
# ─────────────────────────────────────────────────────────────
content = content.replace(
    'domainL1: "hot-topic",',
    'domainL1: "key-focus",'
)
print('✓ default domainL1 changed to key-focus')

with open(r'c:\Pros\ZJ0512\监测预警\AI智能推荐\index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print('\nAll done.')
