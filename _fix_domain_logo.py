"""Move plat-pill from end of rk-t to before the title text, in 领域热点 block only."""
import re

FILE = r'c:\Pros\ZJ0512\监测预警\热点榜单\index.html'
with open(FILE, 'r', encoding='utf-8') as f:
    html = f.read()

tp1_start = html.find('<!-- Tab 2: 领域热点 -->')
tp1_end   = html.find('<!-- Tab 3: 热榜预警 -->')
block     = html[tp1_start:tp1_end]

# Pattern: <div class="rk-t">TEXT[optional risk-tag]<span class="plat-pill ...">LABEL</span></div>
# Move plat-pill to immediately after <div class="rk-t">
pat = re.compile(
    r'(<div class="rk-t">)'
    r'(.*?)'
    r'(<span class="plat-pill [^"]+">.*?</span>)'
    r'(</div>)',
    re.DOTALL
)

def move_pill_left(m):
    return m.group(1) + m.group(3) + m.group(2) + m.group(4)

new_block = pat.sub(move_pill_left, block)
html = html[:tp1_start] + new_block + html[tp1_end:]

with open(FILE, 'w', encoding='utf-8') as f:
    f.write(html)

changed = sum(1 for a, b in zip(block.split('\n'), new_block.split('\n')) if a != b)
print(f'Done. {changed} lines updated.')
