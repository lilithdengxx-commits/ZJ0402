"""
5 changes to 热点榜单/index.html:
1. "高/中/低危" → "高/中/低" in risk tags (tighter label)
2. Fixed card height for 平台热榜 (equal to 领域热点)
3. Remove p-time (上榜时间) from non-enhanced platform cards
4. 香港总榜: add one platform logo after each title
5. 领域热点: replace rk-p text with mini logo badge
"""
import re

FILE = r'c:\Pros\ZJ0512\监测预警\热点榜单\index.html'
with open(FILE, 'r', encoding='utf-8') as f:
    html = f.read()

# ─────────────────────────────────────────────────────────────────
# Change 1: 高危→高, 中危→中, 低危→低  (risk-tag text only)
# ─────────────────────────────────────────────────────────────────
html = html.replace('>高危<', '>高<')
html = html.replace('>中危<', '>中<')
html = html.replace('>低危<', '>低<')

# ─────────────────────────────────────────────────────────────────
# Change 2 + 5 support: New CSS block
# ─────────────────────────────────────────────────────────────────
new_css = """
/* ---- 固定卡片高度 ---- */
.plat-card{height:380px;overflow-y:auto;}
.plat-card .plat-head{position:sticky;top:0;z-index:2;background:#f8fafd;}
.cat-col{height:380px;overflow-y:auto;}
.cat-col .cat-head{position:sticky;top:0;z-index:2;background:#f8fafd;}
.cat-col .rank-hdr{position:sticky;top:36px;z-index:1;background:#f8fafd;}

/* ---- 平台 mini-logo pills ---- */
.plat-pill{display:inline-flex;align-items:center;justify-content:center;padding:1px 5px;border-radius:4px;font-size:9px;font-weight:800;white-space:nowrap;vertical-align:middle;margin-left:4px;line-height:14px;flex-shrink:0}
.pp-lk{background:#ffd700;color:#333}
.pp-hkgd{background:#1890ff;color:#fff}
.pp-hk01{background:#003087;color:#fff}
.pp-yh{background:#7b0099;color:#fff}
.pp-gg{background:#fff;color:#4285f4;border:1px solid rgba(66,133,244,0.4)}
.pp-wb{background:#e6162d;color:#fff}
.pp-dy{background:#161823;color:#fff}
.pp-bd{background:#2932e1;color:#fff}
"""
html = html.replace('@media(max-width:1400px)', new_css + '@media(max-width:1400px)', 1)

# ─────────────────────────────────────────────────────────────────
# Change 3: Remove <div class="p-time">...</div> from non-enhanced cards
# (LIHKG, 香港高登, 香港01, 雅虎, Google – they still have p-time divs)
# ─────────────────────────────────────────────────────────────────
html = re.sub(r'<div class="p-time">[^<]*</div>', '', html)

# ─────────────────────────────────────────────────────────────────
# Change 4: 香港总榜 – add one HK platform logo after risk-tag per row
# Current structure (香港总榜 t-title rows, NOT the 内地总榜 t-body rows):
#   <div class="total-row"><div class="t-num ...">N</div>
#     <div class="t-title">TITLE</div>
#     <span class="risk-tag total-risk ...">X</span></div>
# We rotate through 5 HK platform logos
# ─────────────────────────────────────────────────────────────────
HK_LOGOS = [
    '<span class="plat-pill pp-lk">LK</span>',
    '<span class="plat-pill pp-hkgd">高登</span>',
    '<span class="plat-pill pp-hk01">01</span>',
    '<span class="plat-pill pp-yh">Y!</span>',
    '<span class="plat-pill pp-gg">G</span>',
]

# Find the 香港总榜 block, then patch its total-rows
hk_block_pattern = re.compile(
    r'(<!-- 香港总榜 -->.*?)(?=<!-- LIHKG -->)',
    re.DOTALL
)
m = hk_block_pattern.search(html)
if m:
    block = m.group(1)
    # Find all total-rows that have t-title (not t-body, which is 内地总榜 style)
    row_pat = re.compile(
        r'(<div class="total-row"><div class="t-num[^"]*">\d+</div><div class="t-title">)(.*?)(</div><span class="risk-tag total-risk [^"]*">[^<]*</span></div>)'
    )
    idx = [0]
    def add_hk_logo(m2):
        logo = HK_LOGOS[idx[0] % len(HK_LOGOS)]
        idx[0] += 1
        return m2.group(1) + m2.group(2) + m2.group(3)[:-len('</div>')] + logo + '</div>'
    new_block = row_pat.sub(add_hk_logo, block)
    html = html[:m.start()] + new_block + html[m.end():]
else:
    print("WARNING: 香港总榜 block not found")

# ─────────────────────────────────────────────────────────────────
# Change 5: 领域热点 – replace rk-p text with mini logo pill
# Current: <div class="rk-p">LIHKG</div>
#          <div class="rk-p">香港01</div>  etc.
# ─────────────────────────────────────────────────────────────────
PLAT_PILL_MAP = {
    'LIHKG':   '<span class="plat-pill pp-lk">LK</span>',
    'LIHKG连登': '<span class="plat-pill pp-lk">LK</span>',
    '香港高登': '<span class="plat-pill pp-hkgd">高登</span>',
    '香港01':   '<span class="plat-pill pp-hk01">01</span>',
    '雅虎新闻': '<span class="plat-pill pp-yh">Y!</span>',
    'Google趋势': '<span class="plat-pill pp-gg">G</span>',
    '微博热搜': '<span class="plat-pill pp-wb">微</span>',
    '抖音热搜': '<span class="plat-pill pp-dy">抖</span>',
    '百度热搜': '<span class="plat-pill pp-bd">百</span>',
}

def replace_rkp(m):
    name = m.group(1).strip()
    pill = PLAT_PILL_MAP.get(name)
    if pill:
        return f'<div class="rk-p">{pill}</div>'
    return m.group(0)

html = re.sub(r'<div class="rk-p">([^<]+)</div>', replace_rkp, html)

# ─────────────────────────────────────────────────────────────────
# Write
# ─────────────────────────────────────────────────────────────────
with open(FILE, 'w', encoding='utf-8') as f:
    f.write(html)

print("Done – all 5 changes applied.")
