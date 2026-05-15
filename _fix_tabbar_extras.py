import re

f = r'c:\Pros\ZJ0512\事件分析\事件管理\index.html'
c = open(f, encoding='utf-8').read()

# ── 1. CSS: add tab-bar-spacer / tab-bar-extras after .ev-expand-btn,.ev-add-btn line
OLD_CSS = '.ev-expand-btn,.ev-add-btn{display:inline-flex;align-items:center;gap:5px;height:32px;padding:0 12px;border-radius:8px;font-size:13px;cursor:pointer;white-space:nowrap}'
NEW_CSS = OLD_CSS + """
.tab-bar-spacer{flex:1 1 auto}
.tab-bar-extras{display:flex;align-items:center;gap:8px;padding:0 10px 0 6px}"""
assert c.count(OLD_CSS) == 1, f'CSS match: {c.count(OLD_CSS)}'
c = c.replace(OLD_CSS, NEW_CSS)

# ── 2. Tab bar HTML: add spacer + extras (search + expand)
OLD_TABBAR = '''                    <button class="page-tab-btn" data-tab="shared-events">分享事件</button>
                </div>'''
NEW_TABBAR = '''                    <button class="page-tab-btn" data-tab="shared-events">分享事件</button>
                    <div class="tab-bar-spacer"></div>
                    <div class="tab-bar-extras" id="tabBarExtras" style="display:none">
                        <div class="ev-search-box" style="width:180px">
                            <svg width="13" height="13" viewBox="0 0 24 24" fill="none"><circle cx="11" cy="11" r="7" stroke="currentColor" stroke-width="1.8"/><path d="M16.5 16.5L21 21" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></svg>
                            <input type="text" placeholder="请输入事件名称">
                            <span style="font-size:11px;color:var(--text-faint);white-space:nowrap">0/100</span>
                        </div>
                        <button class="ev-expand-btn">展开<svg width="12" height="12" viewBox="0 0 24 24" fill="none"><path d="M6 9L12 15L18 9" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg></button>
                    </div>
                </div>'''
assert c.count(OLD_TABBAR) == 1, f'tabbar match: {c.count(OLD_TABBAR)}'
c = c.replace(OLD_TABBAR, NEW_TABBAR)

# ── 3. Remove ev-search-box block from all 3 panels + ev-expand-btn from ev-list-right
SEARCH_BLOCK = '''                        <div class="ev-search-box">
                            <svg width="13" height="13" viewBox="0 0 24 24" fill="none"><circle cx="11" cy="11" r="7" stroke="currentColor" stroke-width="1.8"/><path d="M16.5 16.5L21 21" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></svg>
                            <input type="text" placeholder="请输入事件名称">
                            <span style="font-size:11px;color:var(--text-faint);white-space:nowrap">0/100</span>
                        </div>
                        <div class="ev-list-right">'''
NEW_SEARCH_BLOCK = '                        <div class="ev-list-right">'
n = c.count(SEARCH_BLOCK)
print(f'search block matches: {n}')
c = c.replace(SEARCH_BLOCK, NEW_SEARCH_BLOCK)

# ev-expand-btn (normal, in AI / 分享)
EXPAND_NORMAL = '                            <button class="ev-expand-btn">展开<svg width="12" height="12" viewBox="0 0 24 24" fill="none"><path d="M6 9L12 15L18 9" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg></button>\n'
n = c.count(EXPAND_NORMAL)
print(f'expand normal matches: {n}')
c = c.replace(EXPAND_NORMAL, '')

# ev-expand-btn (my-list-only variant, in 我的事件)
EXPAND_MY = '                            <button class="ev-expand-btn my-list-only">展开<svg width="12" height="12" viewBox="0 0 24 24" fill="none"><path d="M6 9L12 15L18 9" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg></button>\n'
n = c.count(EXPAND_MY)
print(f'expand my-list-only matches: {n}')
c = c.replace(EXPAND_MY, '')

# ── 4. initTabs JS: show/hide tabBarExtras on tab switch
OLD_INIT = '''                    var target = btn.getAttribute('data-tab');
                    tabBtns.forEach(function(b) { b.classList.remove('active'); });
                    tabPanels.forEach(function(p) { p.classList.remove('active'); });
                    btn.classList.add('active');
                    var panel = document.getElementById('panel-' + target);
                    if (panel) { panel.classList.add('active'); }'''
NEW_INIT = '''                    var target = btn.getAttribute('data-tab');
                    tabBtns.forEach(function(b) { b.classList.remove('active'); });
                    tabPanels.forEach(function(p) { p.classList.remove('active'); });
                    btn.classList.add('active');
                    var panel = document.getElementById('panel-' + target);
                    if (panel) { panel.classList.add('active'); }
                    var extras = document.getElementById('tabBarExtras');
                    if (extras) { extras.style.display = target === 'situation' ? 'none' : 'flex'; }'''
assert c.count(OLD_INIT) == 1, f'initTabs match: {c.count(OLD_INIT)}'
c = c.replace(OLD_INIT, NEW_INIT)

open(f, 'w', encoding='utf-8').write(c)
print('done')
