import re

with open(r'c:\Pros\ZJ0512\首页\index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# ── 1. 去掉 hero-bg（雷达背景）和 app-icons-row 整块 ──
content = re.sub(
    r'\s*<!-- Radar Background SVG -->.*?</div>\s*\n\s*<!-- App Shortcut Icons -->.*?</div><!-- /app-icons-row -->',
    '',
    content,
    flags=re.DOTALL
)

# ── 2. 英雄区上边距缩小（没有图标了无需大padding） ──
content = content.replace(
    'padding:72px 0 0',
    'padding:36px 0 0'
)

# ── 3. 在 analysis-cards 前插入数据统计看板 ──
stat_board = '''      <!-- ── 数据统计看板 ── -->
      <div class="stat-board">
        <div class="sb-card sb-blue">
          <div class="sb-icon">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none"><path d="M4 6h16M4 10h16M4 14h10" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/><circle cx="18" cy="17" r="3" stroke="currentColor" stroke-width="1.6"/><path d="M20.5 19.5L22 21" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg>
          </div>
          <div class="sb-body">
            <div class="sb-label">今日信息量</div>
            <div class="sb-value">128,547</div>
            <div class="sb-trend up">↑ 较昨日 +12.3%</div>
          </div>
        </div>
        <div class="sb-card sb-orange">
          <div class="sb-icon">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none"><path d="M12 3C7.03 3 3 7.03 3 12s4.03 9 9 9 9-4.03 9-9-4.03-9-9-9z" stroke="currentColor" stroke-width="1.7"/><path d="M12 8v4l2.5 2.5" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"/></svg>
          </div>
          <div class="sb-body">
            <div class="sb-label">预警触发</div>
            <div class="sb-value">23<span class="sb-unit">次</span></div>
            <div class="sb-trend down">↑ 较昨日 +5 次</div>
          </div>
        </div>
        <div class="sb-card sb-green">
          <div class="sb-icon">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none"><rect x="3" y="3" width="8" height="8" rx="1.5" stroke="currentColor" stroke-width="1.7"/><rect x="13" y="3" width="8" height="8" rx="1.5" stroke="currentColor" stroke-width="1.7"/><rect x="3" y="13" width="8" height="8" rx="1.5" stroke="currentColor" stroke-width="1.7"/><rect x="13" y="13" width="8" height="8" rx="1.5" stroke="currentColor" stroke-width="1.7"/></svg>
          </div>
          <div class="sb-body">
            <div class="sb-label">活跃监测方案</div>
            <div class="sb-value">12<span class="sb-unit">个</span></div>
            <div class="sb-trend neutral">本月新增 3 个</div>
          </div>
        </div>
        <div class="sb-card sb-purple">
          <div class="sb-icon">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none"><circle cx="12" cy="8" r="4" stroke="currentColor" stroke-width="1.7"/><path d="M4 20c0-4 3.58-7 8-7s8 3 8 7" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"/><path d="M16 11l1.5 1.5L21 9" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"/></svg>
          </div>
          <div class="sb-body">
            <div class="sb-label">已处置舆情</div>
            <div class="sb-value">8<span class="sb-unit">件</span></div>
            <div class="sb-trend up">↑ 处置率 88.9%</div>
          </div>
        </div>
        <div class="sb-card sb-red">
          <div class="sb-icon">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none"><path d="M12 4C8.13 4 5 7.13 5 11c0 2.87 1.65 5.35 4.06 6.61L9 21h6l-.06-3.39C17.35 16.35 19 13.87 19 11c0-3.87-3.13-7-7-7z" stroke="currentColor" stroke-width="1.7" stroke-linejoin="round"/><path d="M10 21h4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>
          </div>
          <div class="sb-body">
            <div class="sb-label">舆情热度指数</div>
            <div class="sb-value">81.2</div>
            <div class="sb-trend down">↑ 较昨日 +3.4</div>
          </div>
        </div>
      </div><!-- /stat-board -->

'''
content = content.replace(
    '      <div class="analysis-cards">',
    stat_board + '      <div class="analysis-cards">'
)

# ── 4. 添加 stat-board CSS ──
stat_css = '''/* Stat Board */
.stat-board{display:grid;grid-template-columns:repeat(5,1fr);gap:12px;margin-bottom:16px}
.sb-card{background:#fff;border-radius:12px;border:1px solid rgba(122,145,184,0.12);box-shadow:0 1px 6px rgba(26,44,82,0.05);padding:14px 16px;display:flex;align-items:center;gap:14px;position:relative;overflow:hidden}
.sb-card::before{content:'';position:absolute;top:0;left:0;right:0;height:3px;border-radius:12px 12px 0 0}
.sb-blue::before{background:linear-gradient(90deg,#2b61f0,#7ab0ff)}
.sb-orange::before{background:linear-gradient(90deg,#f97316,#fbbf24)}
.sb-green::before{background:linear-gradient(90deg,#10b981,#34d399)}
.sb-purple::before{background:linear-gradient(90deg,#7c3aed,#a855f7)}
.sb-red::before{background:linear-gradient(90deg,#e04040,#f87171)}
.sb-icon{width:44px;height:44px;border-radius:12px;display:flex;align-items:center;justify-content:center;flex:0 0 44px}
.sb-blue .sb-icon{background:rgba(43,97,240,0.1);color:#2b61f0}
.sb-orange .sb-icon{background:rgba(249,115,22,0.1);color:#f97316}
.sb-green .sb-icon{background:rgba(16,185,129,0.1);color:#10b981}
.sb-purple .sb-icon{background:rgba(124,58,237,0.1);color:#7c3aed}
.sb-red .sb-icon{background:rgba(224,64,64,0.1);color:#e04040}
.sb-body{min-width:0;flex:1}
.sb-label{font-size:12px;color:#6b7c95;font-weight:500;margin-bottom:4px;white-space:nowrap}
.sb-value{font-size:22px;font-weight:800;color:#1e2d45;line-height:1.1;white-space:nowrap}
.sb-unit{font-size:13px;font-weight:600;color:#6b7c95;margin-left:2px}
.sb-trend{font-size:11px;margin-top:4px;white-space:nowrap}
.sb-trend.up{color:#10b981}.sb-trend.down{color:#e04040}.sb-trend.neutral{color:#6b7c95}
'''
content = content.replace('/* Analysis Section */', stat_css + '/* Analysis Section */')

with open(r'c:\Pros\ZJ0512\首页\index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print('Done.')
c = open(r'c:\Pros\ZJ0512\首页\index.html', encoding='utf-8').read()
checks = [
    ('app-icons-row', False, '图标行已删除'),
    ('stat-board', True, '统计看板已添加'),
    ('sb-blue', True, '看板CSS已添加'),
    ('padding:36px 0 0', True, '顶部padding已缩小'),
    ('今日信息量', True, '统计卡片内容'),
]
for kw, should_exist, label in checks:
    found = kw in c
    ok = found == should_exist
    print(f'  {"✓" if ok else "✗"} {label}')
