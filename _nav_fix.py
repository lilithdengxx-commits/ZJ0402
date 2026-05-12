# -*- coding: utf-8 -*-
import os, glob, re

ROOT = r'c:\Pros\ZJ0512'

ICON_FJ = '<svg viewBox="0 0 24 24" fill="none"><path d="M5 18L9 13L12 15L18 8L19 18H5Z" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/></svg>'
ICON_ZN = '<svg viewBox="0 0 24 24" fill="none"><rect x="4" y="4" width="16" height="16" rx="2" stroke="currentColor" stroke-width="1.8"/><path d="M8 9h8M8 13h5" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></svg>'

# 匹配整个事件研判区块（处理 active/非active 两种情况）
PATTERN = re.compile(
    r'( +)<section class="nav-group(?: active)?">\s*\n'
    r'\s+<div class="nav-group-title"[^>]*>.*?<span>事件研判</span>.*?</div>\s*\n'
    r'\s+<div class="nav-items">\s*\n'
    r'\s+<a class="nav-item(?: active)?" href="([^"]+)"><span>事件分析</span></a>\s*\n'
    r'\s+<a class="nav-item(?: active)?" href="([^"]+)"><span>智能体编报</span></a>\s*\n'
    r'\s+</div>\s*\n'
    r'\s+</section>',
    re.DOTALL
)

cnt = 0
for fp in sorted(glob.glob(ROOT + r'\**\*.html', recursive=True)):
    with open(fp, 'r', encoding='utf-8') as f:
        txt = f.read()

    def make_replacement(m):
        indent = m.group(1)
        href_fj = m.group(2)
        href_zn = m.group(3)
        # 判断哪个是当前活跃页
        orig = m.group(0)
        fj_active = ' active' if 'nav-item active" href="' + href_fj in orig else ''
        zn_active = ' active' if 'nav-item active" href="' + href_zn in orig else ''
        sec_fj = f'{indent}<section class="nav-group{fj_active}">\n{indent}  <a class="nav-toplevel-link" href="{href_fj}">{ICON_FJ}<span>事件分析</span></a>\n{indent}</section>'
        sec_zn = f'{indent}<section class="nav-group{zn_active}">\n{indent}  <a class="nav-toplevel-link" href="{href_zn}">{ICON_ZN}<span>智能体编报</span></a>\n{indent}</section>'
        return sec_fj + '\n' + sec_zn

    new_txt = PATTERN.sub(make_replacement, txt)

    if new_txt != txt:
        with open(fp, 'w', encoding='utf-8') as f:
            f.write(new_txt)
        print(f'  v {os.path.relpath(fp, ROOT)}')
        cnt += 1

print(f'\n共更新 {cnt} 个文件')
