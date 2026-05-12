"""
Comprehensive layout & data changes to 热点榜单/index.html:

1a. 内地总榜: risk-tag right after title; swap chg/heat positions; dur to far right
1b. 香港总榜: risk-tag + plat-pill inline right after title
1c. 微博/抖音/百度: heat moves to title line right side; dur/chg below; chg before dur
2.  领域热点: merge plat-pill into rk-t (right after risk-tag), remove rk-p column
    - remove rank-hdr "平台" span, grid becomes 24px 1fr
3.  Pad all cards to 10 items (LIHKG, 高登, 香港01, 雅虎, 百度 → +4 each)
"""
import re

FILE = r'c:\Pros\ZJ0512\监测预警\热点榜单\index.html'
with open(FILE, 'r', encoding='utf-8') as f:
    html = f.read()

# ═══════════════════════════════════════════════════════════════
# CSS changes
# ═══════════════════════════════════════════════════════════════

# 1. Remove margin-left:auto from .total-risk (no longer needed)
html = html.replace('.total-risk{margin-left:auto;flex-shrink:0}', '.total-risk{flex-shrink:0}')

# 2. Update rank-row / rank-hdr grid (2 columns, no platform column)
html = html.replace(
    '.rank-hdr{display:grid;grid-template-columns:24px 1fr 60px;padding:4px 10px;font-size:11px;font-weight:700;color:var(--text-faint);border-bottom:1px solid rgba(122,145,184,0.06)}',
    '.rank-hdr{display:grid;grid-template-columns:24px 1fr;padding:4px 10px;font-size:11px;font-weight:700;color:var(--text-faint);border-bottom:1px solid rgba(122,145,184,0.06)}'
)
html = html.replace(
    '.rank-row{display:grid;grid-template-columns:24px 1fr 60px;padding:6px 10px;align-items:center;border-bottom:1px solid rgba(122,145,184,0.05);transition:background 0.12s;cursor:pointer}',
    '.rank-row{display:grid;grid-template-columns:24px 1fr;padding:6px 10px;align-items:center;border-bottom:1px solid rgba(122,145,184,0.05);transition:background 0.12s;cursor:pointer}'
)

# 3. Add new CSS classes
new_css = """
/* ---- 内地总榜右栏 ---- */
.t-right{display:flex;flex-direction:column;align-items:flex-end;gap:2px;flex:0 0 auto;padding-left:6px}
.t-right .t-heat{font-size:11px;color:#f5502a;font-weight:700;white-space:nowrap}
.t-right .t-dur{font-size:10px;color:var(--text-faint);white-space:nowrap}
/* ---- 香港总榜 title wrap ---- */
.t-tw{flex:1;min-width:0;display:flex;align-items:flex-start;gap:4px;flex-wrap:nowrap}
.t-tw .t-title{flex:1;min-width:0}
/* ---- 热搜 title row ---- */
.p-title-row{display:flex;align-items:flex-start;gap:4px;min-width:0}
.p-title-row .p-title{flex:1;min-width:0}
.p-tr-heat{font-size:11px;color:#f5502a;font-weight:700;white-space:nowrap;flex:0 0 auto;padding-top:1px}
/* ---- 领域热点 rk-t inline logo ---- */
.rk-t .plat-pill{margin-left:2px}
"""
html = html.replace('/* ---- 固定卡片高度 ---- */', new_css + '/* ---- 固定卡片高度 ---- */', 1)

# ═══════════════════════════════════════════════════════════════
# 1a. 内地总榜: restructure rows
#   Current: [t-body: [t-title-row: title+risk] [t-meta-row: logos+heat+dur]] [t-chg]
#   Want:    [t-body: [t-title-row: title+risk] [t-meta-row: logos+t-chg]]    [t-right: heat+dur]
# ═══════════════════════════════════════════════════════════════
def rewrite_inland_row(m):
    num_cls = m.group(1) or ''   # e.g. " n1" or ""
    num_val = m.group(2)   # e.g. "1"
    title   = m.group(3)
    risk_cls = m.group(4)  # e.g. "risk-hi"
    risk_lbl = m.group(5)  # e.g. "高"
    logos   = m.group(6)   # full logos span
    heat    = m.group(7)   # e.g. "8.6万"
    dur     = m.group(8)   # e.g. "1.2小时"
    chg_cls = m.group(9)   # e.g. "chg-new"
    chg_val = m.group(10)  # e.g. "NEW"
    return (
        f'<div class="total-row">'
        f'<div class="t-num{num_cls}">{num_val}</div>'
        f'<div class="t-body">'
        f'<div class="t-title-row"><div class="t-title">{title}</div>'
        f'<span class="risk-tag total-risk {risk_cls}">{risk_lbl}</span></div>'
        f'<div class="t-meta-row">{logos}'
        f'<span class="t-chg {chg_cls}">{chg_val}</span></div>'
        f'</div>'
        f'<div class="t-right">'
        f'<span class="t-heat">🔥 {heat}</span>'
        f'<span class="t-dur">⏱ 在榜{dur}</span>'
        f'</div></div>'
    )

inland_row_pat = re.compile(
    r'<div class="total-row">'
    r'<div class="t-num( n\d)?">(\d+)</div>'
    r'<div class="t-body">'
    r'<div class="t-title-row"><div class="t-title">([^<]+)</div>'
    r'<span class="risk-tag total-risk (risk-\w+)">([^<]+)</span></div>'
    r'<div class="t-meta-row">(<span class="t-logos">.*?</span>)'
    r'<span class="t-heat">🔥 ([^<]+)</span>'
    r'<span class="t-dur">⏱ 在榜([^<]+)</span>'
    r'</div></div>'
    r'<span class="t-chg (chg-\w+)">([^<]+)</span>'
    r'</div>',
    re.DOTALL
)

# Only apply to 内地总榜 block
hk_start = html.find('<!-- 香港总榜 -->')
inland_block = html[:hk_start]
rest = html[hk_start:]
inland_block = inland_row_pat.sub(rewrite_inland_row, inland_block)
html = inland_block + rest

# ═══════════════════════════════════════════════════════════════
# 1b. 香港总榜: inline risk-tag + plat-pill after title
#   Current: [t-num] [t-title] [risk-tag total-risk] [plat-pill]
#   Want:    [t-num] [t-tw: [t-title] [risk-tag] [plat-pill]]
# ═══════════════════════════════════════════════════════════════
def rewrite_hk_row(m):
    num_cls  = m.group(1) or ''
    num_val  = m.group(2)
    title    = m.group(3)
    risk_cls = m.group(4)
    risk_lbl = m.group(5)
    pill_cls = m.group(6)
    pill_lbl = m.group(7)
    return (
        f'<div class="total-row">'
        f'<div class="t-num{num_cls}">{num_val}</div>'
        f'<div class="t-tw">'
        f'<div class="t-title">{title}</div>'
        f'<span class="risk-tag {risk_cls}">{risk_lbl}</span>'
        f'<span class="plat-pill {pill_cls}">{pill_lbl}</span>'
        f'</div></div>'
    )

# Find 香港总榜 block, transform within it
hk_lihkg = html.find('<!-- LIHKG -->')
hk_block = html[html.find('<!-- 香港总榜 -->'):hk_lihkg]
rest2 = html[hk_lihkg:]

hk_row_pat = re.compile(
    r'<div class="total-row">'
    r'<div class="t-num( n\d)?">(\d+)</div>'
    r'<div class="t-title">([^<]+)</div>'
    r'<span class="risk-tag total-risk (risk-\w+)">([^<]+)</span>'
    r'<span class="plat-pill (pp-\w+)">([^<]+)</span>'
    r'</div>'
)
hk_block = hk_row_pat.sub(rewrite_hk_row, hk_block)
html = html[:html.find('<!-- 香港总榜 -->')] + hk_block + rest2

# ═══════════════════════════════════════════════════════════════
# 1c. 微博/抖音/百度: heat to title line, chg before dur in meta-row
#   Current p-body: [p-title: text+risk] [p-meta-row: heat+dur+chg]
#   Want p-body:    [p-title-row: [p-title: text+risk] [p-tr-heat]] [p-meta-row: chg+dur]
# ═══════════════════════════════════════════════════════════════
def rewrite_search_item(m):
    num_val  = m.group(1)
    title    = m.group(2)
    risk_cls = m.group(3)
    risk_lbl = m.group(4)
    heat     = m.group(5)
    dur      = m.group(6)
    chg_cls  = m.group(7)
    chg_val  = m.group(8)
    return (
        f'<div class="plist-item"><span class="p-num">{num_val}</span>'
        f'<div class="p-body">'
        f'<div class="p-title-row">'
        f'<div class="p-title">{title}<span class="risk-tag {risk_cls}">{risk_lbl}</span></div>'
        f'<span class="p-tr-heat">🔥 {heat}</span>'
        f'</div>'
        f'<div class="p-meta-row">'
        f'<span class="p-chg {chg_cls}">{chg_val}</span>'
        f'<span class="p-dur">⏱ 在榜{dur}</span>'
        f'</div></div></div>'
    )

search_item_pat = re.compile(
    r'<div class="plist-item"><span class="p-num">(\d+)</span>'
    r'<div class="p-body"><div class="p-title">([^<]+)'
    r'<span class="risk-tag (risk-\w+)">([^<]+)</span></div>'
    r'<div class="p-meta-row">'
    r'<span class="p-heat">🔥 ([^<]+)</span>'
    r'<span class="p-dur">⏱ 在榜([^<]+)</span>'
    r'<span class="p-chg (chg-\w+)">([^<]+)</span>'
    r'</div></div></div>'
)
html = search_item_pat.sub(rewrite_search_item, html)

# ═══════════════════════════════════════════════════════════════
# 2. 领域热点: merge rk-p into rk-t, remove rk-p, update grid + hdr
# ═══════════════════════════════════════════════════════════════

# Update rank-hdr – remove the "平台" span
html = html.replace(
    '<div class="rank-hdr"><span>排名</span><span>标题</span><span>平台</span></div>',
    '<div class="rank-hdr"><span>排名</span><span>标题</span></div>'
)

# Merge rk-p into rk-t: move plat-pill from rk-p to end of rk-t, remove rk-p div
rkp_pat = re.compile(
    r'(<div class="rk-t">.*?)(</div>)\s*<div class="rk-p">(<span class="plat-pill[^"]*">[^<]+</span>)</div>',
    re.DOTALL
)
def merge_rkp(m):
    return m.group(1) + m.group(3) + m.group(2)

html = rkp_pat.sub(merge_rkp, html)

# ═══════════════════════════════════════════════════════════════
# 3. Pad cards to 10 items
# ═══════════════════════════════════════════════════════════════

# Helper: build plain plist-item (no meta-row for non-enhanced cards)
def plain_item(num, title, risk_cls, risk_lbl):
    return (
        f'              <div class="plist-item"><span class="p-num">{num}</span>'
        f'<div><div class="p-title">{title}'
        f'<span class="risk-tag {risk_cls}">{risk_lbl}</span></div></div></div>'
    )

# Helper: build enhanced plist-item (微博/抖音/百度 style)
def enhanced_item(num, title, risk_cls, risk_lbl, heat, dur, chg_cls, chg_val):
    return (
        f'              <div class="plist-item"><span class="p-num">{num}</span>'
        f'<div class="p-body">'
        f'<div class="p-title-row">'
        f'<div class="p-title">{title}<span class="risk-tag {risk_cls}">{risk_lbl}</span></div>'
        f'<span class="p-tr-heat">🔥 {heat}</span>'
        f'</div>'
        f'<div class="p-meta-row">'
        f'<span class="p-chg {chg_cls}">{chg_val}</span>'
        f'<span class="p-dur">⏱ 在榜{dur}</span>'
        f'</div></div></div>'
    )

# LIHKG +4
lihkg_extra = '\n'.join([
    plain_item(7, '本港新能源车注册数量持续攀升', 'risk-lo', '低'),
    plain_item(8, '全港跑步比赛2026年度赛程公布', 'risk-lo', '低'),
    plain_item(9, '政府就最低工资水平展开新一轮咨询', 'risk-md', '中'),
    plain_item(10, '电费调整计划引发市民广泛讨论', 'risk-md', '中'),
])
html = html.replace(
    '              <div class="plist-item"><span class="p-num">6</span><div><div class="p-title">由天道酬勤，到FIRE movement，再到及时…<span class="risk-tag risk-lo">低</span></div></div></div>\n            </div>\n            <!-- 香港高登 -->',
    '              <div class="plist-item"><span class="p-num">6</span><div><div class="p-title">由天道酬勤，到FIRE movement，再到及时…<span class="risk-tag risk-lo">低</span></div></div></div>\n' + lihkg_extra + '\n            </div>\n            <!-- 香港高登 -->'
)

# 香港高登 +4
hkgd_extra = '\n'.join([
    plain_item(7, '本港失业率维持低位 就业市场稳定', 'risk-lo', '低'),
    plain_item(8, '港大研究：本港青年置业意愿持续下降', 'risk-md', '中'),
    plain_item(9, '新界东北发展区首批居民开始迁入', 'risk-lo', '低'),
    plain_item(10, '政府拟扩大夜间经济措施至更多地区', 'risk-lo', '低'),
])
html = html.replace(
    '              <div class="plist-item"><span class="p-num">6</span><div><div class="p-title">刘美：看着谷爱凌的人「很虚伪」<span class="risk-tag risk-lo">低</span></div></div></div>\n            </div>\n            <!-- 香港01 -->',
    '              <div class="plist-item"><span class="p-num">6</span><div><div class="p-title">刘美：看着谷爱凌的人「很虚伪」<span class="risk-tag risk-lo">低</span></div></div></div>\n' + hkgd_extra + '\n            </div>\n            <!-- 香港01 -->'
)

# 香港01 +4
hk01_extra = '\n'.join([
    plain_item(7, '渔护署指今年候鸟迁徙数量创新高', 'risk-lo', '低'),
    plain_item(8, '葵涌货柜码头自动化改造进入新阶段', 'risk-lo', '低'),
    plain_item(9, '食物安全中心发现进口食品含违禁添加剂', 'risk-md', '中'),
    plain_item(10, '港府宣布延长防疫隔离政策检讨期限', 'risk-md', '中'),
])
html = html.replace(
    '              <div class="plist-item"><span class="p-num">6</span><div><div class="p-title">两毓饭英文？DSE英文口试闯两毓毓 两毓…<span class="risk-tag risk-lo">低</span></div></div></div>\n            </div>\n            <!-- 雅虎新闻 -->',
    '              <div class="plist-item"><span class="p-num">6</span><div><div class="p-title">两毓饭英文？DSE英文口试闯两毓毓 两毓…<span class="risk-tag risk-lo">低</span></div></div></div>\n' + hk01_extra + '\n            </div>\n            <!-- 雅虎新闻 -->'
)

# 雅虎新闻 +4
yahoo_extra = '\n'.join([
    plain_item(7, '港元兑美元触及弱方兑换保证水平', 'risk-md', '中'),
    plain_item(8, '零售商呼吁政府推出更多消费刺激措施', 'risk-lo', '低'),
    plain_item(9, '本港首季GDP增速超预期经济学家上调预测', 'risk-lo', '低'),
    plain_item(10, '港股通南向资金连续五日净买入', 'risk-lo', '低'),
])
html = html.replace(
    '              <div class="plist-item"><span class="p-num">6</span><div><div class="p-title">各地填充始 建OpenClaw产业<span class="risk-tag risk-lo">低</span></div></div></div>\n            </div>\n            <!-- Google趋势 -->',
    '              <div class="plist-item"><span class="p-num">6</span><div><div class="p-title">各地填充始 建OpenClaw产业<span class="risk-tag risk-lo">低</span></div></div></div>\n' + yahoo_extra + '\n            </div>\n            <!-- Google趋势 -->'
)

# 百度热搜 +4
baidu_extra = '\n'.join([
    enhanced_item(7, '北京地铁新线年底开通首班车时间调整', 'risk-lo', '低', '1.8万', '2.3小时', 'chg-up', '↑1'),
    enhanced_item(8, '国产新能源汽车出口首次突破百万辆', 'risk-lo', '低', '1.4万', '3.6小时', 'chg-dn', '↓1'),
    enhanced_item(9, '教育部通知：今年高考报名人数创历史新高', 'risk-md', '中', '1.1万', '1.7小时', 'chg-new', 'NEW'),
    enhanced_item(10, '春季踏青出行指南：十大热门景区推荐', 'risk-lo', '低', '0.9万', '4.8小时', 'chg-up', '↑2'),
])
html = html.replace(
    '              <div class="plist-item"><span class="p-num">6</span><div class="p-body"><div class="p-title-row"><div class="p-title">各地填充始 建OpenClaw产业<span class="risk-tag risk-lo">低</span></div><span class="p-tr-heat">🔥 2.1万</span></div><div class="p-meta-row"><span class="p-chg chg-dn">↓2</span><span class="p-dur">⏱ 在榜4.1小时</span></div></div></div>\n            </div>\n          </div>\n        </div>',
    '              <div class="plist-item"><span class="p-num">6</span><div class="p-body"><div class="p-title-row"><div class="p-title">各地填充始 建OpenClaw产业<span class="risk-tag risk-lo">低</span></div><span class="p-tr-heat">🔥 2.1万</span></div><div class="p-meta-row"><span class="p-chg chg-dn">↓2</span><span class="p-dur">⏱ 在榜4.1小时</span></div></div></div>\n' + baidu_extra + '\n            </div>\n          </div>\n        </div>'
)

# ═══════════════════════════════════════════════════════════════
# Write
# ═══════════════════════════════════════════════════════════════
with open(FILE, 'w', encoding='utf-8') as f:
    f.write(html)

print("Done.")
