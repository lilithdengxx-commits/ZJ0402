"""Transform 热点榜单/index.html with 4 changes:
1. Add risk level tags to all list items
2. Split 平台总榜 into 内地总榜 + 香港总榜
3. Fix text truncation (allow 2 lines)
4. Swap 领域热点 and 平台热榜 tab positions
"""
import re

FILE = r'c:\Pros\ZJ0512\监测预警\热点榜单\index.html'

with open(FILE, 'r', encoding='utf-8') as f:
    html = f.read()

# ─────────────────────────────────────────────────────────────────
# Change 3: Fix text truncation in CSS
# ─────────────────────────────────────────────────────────────────
html = html.replace(
    '.rk-t{font-size:14px;font-weight:500;color:var(--text);white-space:nowrap;overflow:hidden;text-overflow:ellipsis;padding-right:6px}',
    '.rk-t{font-size:13px;font-weight:500;color:var(--text);overflow:hidden;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;padding-right:4px;line-height:1.35}'
)
html = html.replace(
    '.t-title{flex:1;font-size:14px;font-weight:500;color:var(--text);overflow:hidden;white-space:nowrap;text-overflow:ellipsis}',
    '.t-title{flex:1;font-size:13px;font-weight:500;color:var(--text);overflow:hidden;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;line-height:1.35}'
)
# p-title may also be truncated via container; allow 2-line wrap
html = html.replace(
    '.p-title{font-size:14px;font-weight:500;color:var(--text);line-height:1.45}',
    '.p-title{font-size:13px;font-weight:500;color:var(--text);line-height:1.35;overflow:hidden;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical}'
)

# ─────────────────────────────────────────────────────────────────
# Change 1: Add risk tag CSS classes
# ─────────────────────────────────────────────────────────────────
risk_css = (
    '\n/* 风险标签 */\n'
    '.risk-tag{display:inline-flex;align-items:center;padding:1px 6px;border-radius:3px;font-size:10px;font-weight:700;white-space:nowrap;margin-left:4px;vertical-align:middle;line-height:16px;flex-shrink:0}\n'
    '.risk-hi{background:rgba(224,64,64,0.08);color:#e04040;border:1px solid rgba(224,64,64,0.22)}\n'
    '.risk-md{background:rgba(196,125,16,0.08);color:#c47d10;border:1px solid rgba(196,125,16,0.22)}\n'
    '.risk-lo{background:rgba(18,168,122,0.08);color:#12a87a;border:1px solid rgba(18,168,122,0.22)}\n'
    '.total-risk{margin-left:auto;flex-shrink:0}\n'
    '\n'
)
html = html.replace('@media(max-width:1400px)', risk_css + '@media(max-width:1400px)', 1)

# Also update total-row grid to not hide the risk tag
html = html.replace(
    '.total-row{display:grid;grid-template-columns:24px 1fr auto;align-items:center;gap:8px;padding:6px 12px;border-bottom:1px solid rgba(122,145,184,0.06);font-size:13px;cursor:pointer;transition:background 0.12s}',
    '.total-row{display:flex;align-items:center;gap:6px;padding:6px 12px;border-bottom:1px solid rgba(122,145,184,0.06);font-size:13px;cursor:pointer;transition:background 0.12s}'
)
html = html.replace(
    '.t-num{width:18px;height:18px;border-radius:4px;display:grid;place-items:center;font-size:10px;font-weight:700;background:rgba(122,145,184,0.12);color:var(--text-soft)}',
    '.t-num{width:18px;height:18px;border-radius:4px;display:grid;place-items:center;font-size:10px;font-weight:700;background:rgba(122,145,184,0.12);color:var(--text-soft);flex:0 0 18px}'
)

# ─────────────────────────────────────────────────────────────────
# Risk level assignment function
# ─────────────────────────────────────────────────────────────────
HIGH_KW = ['第23条','遭轰炸','伊朗','Taiwan Strait','election','新冠','JN.1','无人机监测','实名制','楼价','两会代表热议逃离','选举','军事','轰炸','战争','暴恐','群体性']
MID_KW  = ['两会','政策','扶贫','失业','油价','会议','急症','外劳','暴雨','中东','军','通胀','普选','驻外','抗议','改革','监管','廉署','管局','戡界','希莫','大选','经济下行','财贷','预算案','脱油','刷翻','零售','楼市','涨','亏','升指','负增长','季节性流感','医院爆满','打击','传人','退出','逃离','升学','失业']

def risk(title):
    for kw in HIGH_KW:
        if kw in title:
            return ('risk-hi', '高危')
    for kw in MID_KW:
        if kw in title:
            return ('risk-md', '中危')
    return ('risk-lo', '低危')

# ─────────────────────────────────────────────────────────────────
# Add risk tags to .rk-t items (category grid)
# ─────────────────────────────────────────────────────────────────
def add_rkt_tag(m):
    title = m.group(1)
    cls, label = risk(title)
    return f'<div class="rk-t">{title}<span class="risk-tag {cls}">{label}</span></div>'

html = re.sub(r'<div class="rk-t">([^<]+)</div>', add_rkt_tag, html)

# ─────────────────────────────────────────────────────────────────
# Add risk tags to .p-title items (platform list)
# ─────────────────────────────────────────────────────────────────
def add_ptitle_tag(m):
    title = m.group(1)
    cls, label = risk(title)
    return f'<div class="p-title">{title}<span class="risk-tag {cls}">{label}</span></div>'

html = re.sub(r'<div class="p-title">([^<]+)</div>', add_ptitle_tag, html)

# ─────────────────────────────────────────────────────────────────
# Add risk tags to .t-title items (total list) — as flex child
# ─────────────────────────────────────────────────────────────────
def add_ttitle_tag(m):
    title = m.group(1)
    cls, label = risk(title)
    return f'<div class="t-title">{title}</div><span class="risk-tag total-risk {cls}">{label}</span>'

html = re.sub(r'<div class="t-title">([^<]+)</div>(?!</div>)', add_ttitle_tag, html)

# ─────────────────────────────────────────────────────────────────
# Change 2: Split 平台总榜 into 内地总榜 + 香港总榜
# ─────────────────────────────────────────────────────────────────
mainland_total = '''\
            <!-- 内地总榜 -->
            <div class="plat-card">
              <div class="plat-head"><span class="plat-icon" style="background:linear-gradient(135deg,#e04040,#c47d10);color:#fff;font-size:10px;font-weight:800">内</span>内地总榜</div>
              <div class="total-row"><div class="t-num n1">1</div><div class="t-title">十四届全国人大四次会议议程公布</div><span class="risk-tag total-risk risk-hi">高危</span></div>
              <div class="total-row"><div class="t-num n2">2</div><div class="t-title">代表建议设定3000亿元高速免费额度</div><span class="risk-tag total-risk risk-md">中危</span></div>
              <div class="total-row"><div class="t-num n3">3</div><div class="t-title">12306回应乘客在普速铁路上用排插</div><span class="risk-tag total-risk risk-lo">低危</span></div>
              <div class="total-row"><div class="t-num">4</div><div class="t-title">2026全国两会为什么格外重要</div><span class="risk-tag total-risk risk-md">中危</span></div>
              <div class="total-row"><div class="t-num">5</div><div class="t-title">驻日大使馆提醒：防范日本「撞人族」</div><span class="risk-tag total-risk risk-md">中危</span></div>
              <div class="total-row"><div class="t-num">6</div><div class="t-title">雷军2026两会议题引发广泛关注</div><span class="risk-tag total-risk risk-md">中危</span></div>
              <div class="total-row"><div class="t-num">7</div><div class="t-title">北京今日迎来今年第一场大雪</div><span class="risk-tag total-risk risk-lo">低危</span></div>
              <div class="total-row"><div class="t-num">8</div><div class="t-title">山东修高铁站挖出5亿年前化石石海</div><span class="risk-tag total-risk risk-lo">低危</span></div>
              <div class="total-row"><div class="t-num">9</div><div class="t-title">政协委员建议高中纳入义务教育</div><span class="risk-tag total-risk risk-md">中危</span></div>
              <div class="total-row"><div class="t-num">10</div><div class="t-title">代表委员议建立提案落地落实机制</div><span class="risk-tag total-risk risk-md">中危</span></div>
            </div>'''

hk_total = '''\
            <!-- 香港总榜 -->
            <div class="plat-card">
              <div class="plat-head"><span class="plat-icon" style="background:linear-gradient(135deg,#2b61f0,#1890ff);color:#fff;font-size:10px;font-weight:800">港</span>香港总榜</div>
              <div class="total-row"><div class="t-num n1">1</div><div class="t-title">港铁票价调整方案今日正式公布</div><span class="risk-tag total-risk risk-lo">低危</span></div>
              <div class="total-row"><div class="t-num n2">2</div><div class="t-title">《基本法》第23条立法公众咨询结果出炉</div><span class="risk-tag total-risk risk-hi">高危</span></div>
              <div class="total-row"><div class="t-num n3">3</div><div class="t-title">新冠变异株JN.1感染个案增加 呼吁接种疫苗</div><span class="risk-tag total-risk risk-hi">高危</span></div>
              <div class="total-row"><div class="t-num">4</div><div class="t-title">香港迪士尼「魔雪奇缘」新园区盛大开幕</div><span class="risk-tag total-risk risk-lo">低危</span></div>
              <div class="total-row"><div class="t-num">5</div><div class="t-title">季节性流感踏入高峰期公立医院病房爆满</div><span class="risk-tag total-risk risk-hi">高危</span></div>
              <div class="total-row"><div class="t-num">6</div><div class="t-title">LIHKG热议：伊朗小学遭轰炸管局公开</div><span class="risk-tag total-risk risk-hi">高危</span></div>
              <div class="total-row"><div class="t-num">7</div><div class="t-title">跨境学童全面恢复面授课堂</div><span class="risk-tag total-risk risk-lo">低危</span></div>
              <div class="total-row"><div class="t-num">8</div><div class="t-title">驻外经贸办积极斡纠对香港不实报道</div><span class="risk-tag total-risk risk-md">中危</span></div>
              <div class="total-row"><div class="t-num">9</div><div class="t-title">DSE中学文凭试今日放榜 多名状元出炉</div><span class="risk-tag total-risk risk-md">中危</span></div>
              <div class="total-row"><div class="t-num">10</div><div class="t-title">巴塞尔艺术展(Art Basel)香港展会盛大开幕</div><span class="risk-tag total-risk risk-lo">低危</span></div>
            </div>'''

# Replace old 平台总榜 card (find and replace the entire card block)
old_total_card = re.search(
    r'            <!-- 平台总榜 占两列 -->\n            <div class="plat-card" style="grid-column:span 1">.*?</div>\n            <!-- LIHKG -->',
    html, re.DOTALL
)
if old_total_card:
    html = html[:old_total_card.start()] + mainland_total + '\n' + hk_total + '\n            <!-- LIHKG -->' + html[old_total_card.end():]
else:
    print("WARNING: Could not find 平台总榜 card to replace")

# ─────────────────────────────────────────────────────────────────
# Change 4: Swap tab buttons (领域热点 ↔ 平台热榜)
# and swap panel content
# ─────────────────────────────────────────────────────────────────

# Step A: Swap button labels
html = html.replace(
    '<button class="main-tab active" onclick="switchTab(0,this)">领域热点</button>\n            <button class="main-tab" onclick="switchTab(1,this)">平台热榜</button>',
    '<button class="main-tab active" onclick="switchTab(0,this)">平台热榜</button>\n            <button class="main-tab" onclick="switchTab(1,this)">领域热点</button>'
)

# Step B: Swap panel content while keeping tp0/tp1 IDs and active class correct
# Extract content between panel div open tags and their closing divs

# Find tp0 block (currently 领域热点, active)
tp0_pattern = r'(        <!-- Tab 1: 领域热点 -->\n        <div class="tab-panel active" id="tp0">)(.*?)(        </div>\n\n        <!-- Tab 2: 平台热榜 -->)'
tp1_pattern = r'(        <!-- Tab 2: 平台热榜 -->\n        <div class="tab-panel" id="tp1">)(.*?)(        </div>\n\n        <!-- Tab 3: 热榜预警 -->)'

m0 = re.search(tp0_pattern, html, re.DOTALL)
m1 = re.search(tp1_pattern, html, re.DOTALL)

if m0 and m1:
    tp0_inner = m0.group(2)  # 领域热点 content
    tp1_inner = m1.group(2)  # 平台热榜 content

    # Build new tp0 = 平台热榜 (active), new tp1 = 领域热点
    new_tp0 = ('        <!-- Tab 1: 平台热榜 -->\n        <div class="tab-panel active" id="tp0">'
               + tp1_inner
               + '        </div>\n\n        <!-- Tab 2: 领域热点 -->')
    new_tp1 = ('\n        <div class="tab-panel" id="tp1">'
               + tp0_inner
               + '        </div>\n\n        <!-- Tab 3: 热榜预警 -->')

    # Replace the old combined section
    old_combined_start = m0.start()
    old_combined_end   = m1.end()
    html = html[:old_combined_start] + new_tp0 + new_tp1 + html[old_combined_end:]
else:
    print(f"WARNING: Could not find tab panels. m0={bool(m0)}, m1={bool(m1)}")

# ─────────────────────────────────────────────────────────────────
# Write output
# ─────────────────────────────────────────────────────────────────
with open(FILE, 'w', encoding='utf-8') as f:
    f.write(html)

print("Done! All 4 changes applied.")
