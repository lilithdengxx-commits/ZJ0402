"""Move plat-pill from end of t-title to before the title text, in 香港总榜 block only."""
import re

FILE = r'c:\Pros\ZJ0512\监测预警\热点榜单\index.html'
with open(FILE, 'r', encoding='utf-8') as f:
    html = f.read()

hk_start = html.find('<!-- 香港总榜 -->')
hk_end   = html.find('<!-- LIHKG -->')
hk_block = html[hk_start:hk_end]

# Pattern: <div class="t-title">TITLE_TEXT[optional risk-tag]<span class="plat-pill ...">LABEL</span></div>
# Move plat-pill to right after opening <div class="t-title">
pat = re.compile(
    r'(<div class="t-title">)'           # group 1: opening tag
    r'(.*?)'                              # group 2: title text (+ optional risk-tag)
    r'(<span class="plat-pill [^"]+">.*?</span>)'  # group 3: plat-pill
    r'(</div>)',                          # group 4: closing tag
    re.DOTALL
)

def move_pill_left(m):
    return m.group(1) + m.group(3) + m.group(2) + m.group(4)

new_block = pat.sub(move_pill_left, hk_block)
html = html[:hk_start] + new_block + html[hk_end:]

with open(FILE, 'w', encoding='utf-8') as f:
    f.write(html)

print('Done. Changes:')
for line in new_block.split('\n'):
    if 'plat-pill' in line:
        print(' ', line.strip()[:120])
