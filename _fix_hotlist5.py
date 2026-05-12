"""
Fix 4 issues:
1. 内地总榜: move risk-tag INSIDE .t-title so it appears right after text
2. 香港总榜: move risk-tag + plat-pill INSIDE .t-title
3. 微博/抖音/百度: push .p-dur to far right via CSS margin-left:auto
4. 领域热点 cat-col: remove fixed 380px height so all 10 items are visible
"""
import re

FILE = r'c:\Pros\ZJ0512\监测预警\热点榜单\index.html'
with open(FILE, 'r', encoding='utf-8') as f:
    html = f.read()

# ═══════════════════════════════════════════════════════
# 3. CSS: push p-dur to far right in meta-row
# ═══════════════════════════════════════════════════════
html = html.replace(
    '.p-dur{font-size:10px;color:var(--text-faint);white-space:nowrap}',
    '.p-dur{font-size:10px;color:var(--text-faint);white-space:nowrap;margin-left:auto}'
)

# ═══════════════════════════════════════════════════════
# 4. CSS: remove fixed height on cat-col so all 10 items display
# ═══════════════════════════════════════════════════════
html = html.replace(
    '.cat-col{height:380px;overflow-y:auto;}',
    '.cat-col{}'
)
# Sticky headers no longer needed without scroll container
html = html.replace(
    '.cat-col .cat-head{position:sticky;top:0;z-index:2;background:#f8fafd;}',
    '.cat-col .cat-head{}'
)
html = html.replace(
    '.cat-col .rank-hdr{position:sticky;top:36px;z-index:1;background:#f8fafd;}',
    '.cat-col .rank-hdr{}'
)

# ═══════════════════════════════════════════════════════
# 1. 内地总榜: move <span class="risk-tag total-risk ..."> inside <div class="t-title">
#    Before: <div class="t-title">TEXT</div><span class="risk-tag total-risk risk-X">L</span></div>
#    After:  <div class="t-title">TEXT<span class="risk-tag total-risk risk-X">L</span></div></div>
# Only in the 内地总榜 block (before 香港总榜)
# ═══════════════════════════════════════════════════════
hk_pos = html.find('<!-- 香港总榜 -->')
inland_block = html[:hk_pos]
rest = html[hk_pos:]

def move_risk_into_title(text):
    # Pattern: </div> immediately followed by <span class="risk-tag total-risk ...">...</span></div>
    # The first </div> closes t-title, second closes t-title-row
    pat = re.compile(
        r'(<div class="t-title">)(.*?)(</div>)'
        r'(<span class="risk-tag total-risk [^"]+">.*?</span>)'
        r'(</div>)',
        re.DOTALL
    )
    def repl(m):
        return m.group(1) + m.group(2) + m.group(4) + m.group(3) + m.group(5)
    return pat.sub(repl, text)

inland_block = move_risk_into_title(inland_block)
html = inland_block + rest

# ═══════════════════════════════════════════════════════
# 2. 香港总榜: move risk-tag + plat-pill inside <div class="t-title">
#    Before: <div class="t-tw"><div class="t-title">TEXT</div><span class="risk-tag ...">R</span><span class="plat-pill ...">P</span></div>
#    After:  <div class="t-tw"><div class="t-title">TEXT<span class="risk-tag ...">R</span><span class="plat-pill ...">P</span></div></div>
# ═══════════════════════════════════════════════════════
lihkg_pos = html.find('<!-- LIHKG -->')
hk_block = html[html.find('<!-- 香港总榜 -->'):lihkg_pos]
before_hk = html[:html.find('<!-- 香港总榜 -->')]
after_lihkg = html[lihkg_pos:]

hk_pat = re.compile(
    r'(<div class="t-tw"><div class="t-title">)(.*?)(</div>)'
    r'(<span class="risk-tag [^"]+">.*?</span>)'
    r'(<span class="plat-pill [^"]+">.*?</span>)'
    r'(</div></div>)',
    re.DOTALL
)
def hk_repl(m):
    return m.group(1) + m.group(2) + m.group(4) + m.group(5) + m.group(3) + m.group(6)

hk_block = hk_pat.sub(hk_repl, hk_block)
html = before_hk + hk_block + after_lihkg

with open(FILE, 'w', encoding='utf-8') as f:
    f.write(html)

print("Done.")
# Verify
with open(FILE, 'r', encoding='utf-8') as f:
    v = f.read()

# Check inland: risk-tag should now be inside t-title (not after </div>)
inland_v = v[v.find('内地总榜'):v.find('香港总榜')]
outside = inland_v.count('</div><span class="risk-tag total-risk')
inside = inland_v.count('<div class="t-title">十四届')
print(f'内地总榜 risk-tag outside t-title: {outside} (should be 0)')

# Check HK: risk-tag inside t-title
hk_v = v[v.find('<!-- 香港总榜 -->'):v.find('<!-- LIHKG -->')]
hk_outside = hk_v.count('</div><span class="risk-tag')
print(f'香港总榜 risk-tag outside t-title: {hk_outside} (should be 0)')

# Check p-dur margin-left:auto
print(f'p-dur margin-left:auto: {"margin-left:auto" in v[v.find(".p-dur"):v.find(".p-dur")+80]}')

# Check cat-col height removed
print(f'cat-col fixed height removed: {"height:380px" not in v[v.find(".cat-col"):v.find(".cat-col")+30]}')
