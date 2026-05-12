"""
修复所有 HTML 文件中侧边栏导航，使用最新结构：
1. 去掉「民意与满意度调查」和「市民留言板」
2. 去掉「事件研判」分组，「事件分析」和「智能体编报」变为独立一级
3. 监测预警内部：AI智能推荐 > 热点榜单 > 舆情监测 > 预警查询
"""
import os

ROOT = r'c:\Pros\ZJ0512'

# ─── SVG 图标 ────────────────────────────────────────────────
ICON_HOME     = '<svg viewBox="0 0 24 24" fill="none"><path d="M3 9L12 3L21 9V20H15V14H9V20H3V9Z" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/></svg>'
ICON_MONITOR  = '<svg viewBox="0 0 24 24" fill="none"><path d="M3 3h18v12H3V3zM8 21h8M12 15v6" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>'
ICON_INCIDENT = '<svg viewBox="0 0 24 24" fill="none"><path d="M5 18L9 13L12 15L18 8L19 18H5Z" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/></svg>'
ICON_SEARCH   = '<svg viewBox="0 0 24 24" fill="none"><circle cx="11" cy="11" r="7" stroke="currentColor" stroke-width="1.8"/><path d="M20 20L16 16" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></svg>'
ICON_HANDLE   = '<svg viewBox="0 0 24 24" fill="none"><path d="M12 4V20M4 12H20" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></svg>'
ICON_SURVEY   = '<svg viewBox="0 0 24 24" fill="none"><path d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 012-2h2a2 2 0 012 2M9 12h6M9 16h4" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></svg>'
ICON_MSG      = '<svg viewBox="0 0 24 24" fill="none"><path d="M21 15a2 2 0 01-2 2H7l-4 4V5a2 2 0 012-2h14a2 2 0 012 2v10z" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/></svg>'
ICON_BOOK     = '<svg viewBox="0 0 24 24" fill="none"><path d="M6 5H18V19H6V5ZM9 9H15M9 13H15" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></svg>'
ICON_AGENT    = '<svg viewBox="0 0 24 24" fill="none"><rect x="4" y="4" width="16" height="16" rx="2" stroke="currentColor" stroke-width="1.8"/><path d="M8 9h8M8 13h5" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></svg>'


def build_nav(prefix, active_group, active_item):
    """构建完整导航 HTML，注入到 sidebar-nav-area 内部。"""
    def gc(name):
        return 'nav-group active' if name == active_group else 'nav-group'
    def ic(name):
        return 'nav-item active' if name == active_item else 'nav-item'

    lines = [
        # ── 首页（独立一级）
        f'<section class="{gc("首页")}">',
        f'  <a class="nav-toplevel-link" href="{prefix}首页/index.html">{ICON_HOME}<span>首页</span></a>',
        f'</section>',

        # ── 监测预警（分组）
        f'<section class="{gc("监测预警")}">',
        f'  <div class="nav-group-title" onclick="toggleGroup(this)"><div class="title-left">{ICON_MONITOR}<span>监测预警</span></div><small>›</small></div>',
        f'  <div class="nav-items">',
        f'    <a class="{ic("AI智能推荐")}" href="{prefix}监测预警/AI智能推荐/index.html"><span>AI智能推荐</span></a>',
        f'    <a class="{ic("热点榜单")}" href="{prefix}监测预警/热点榜单/index.html"><span>热点榜单</span></a>',
        f'    <a class="{ic("舆情监测")}" href="{prefix}监测预警/关键对象监测/index.html"><span>舆情监测</span></a>',
        f'    <a class="{ic("预警查询")}" href="{prefix}监测预警/预警查询/index.html"><span>预警查询</span></a>',
        f'  </div>',
        f'</section>',

        # ── 事件分析（独立一级）
        f'<section class="{gc("事件分析")}">',
        f'  <a class="nav-toplevel-link" href="{prefix}事件分析/事件管理/index.html">{ICON_INCIDENT}<span>事件分析</span></a>',
        f'</section>',

        # ── 智能体编报（独立一级）
        f'<section class="{gc("智能体编报")}">',
        f'  <a class="nav-toplevel-link" href="{prefix}智能体编报/index.html">{ICON_AGENT}<span>智能体编报</span></a>',
        f'</section>',

        # ── 智能检索（独立一级）
        f'<section class="{gc("智能检索")}">',
        f'  <a class="nav-toplevel-link" href="{prefix}智能检索/index.html">{ICON_SEARCH}<span>智能检索</span></a>',
        f'</section>',

        # ── 处置引导（分组）
        f'<section class="{gc("处置引导")}">',
        f'  <div class="nav-group-title" onclick="toggleGroup(this)"><div class="title-left">{ICON_HANDLE}<span>处置引导</span></div><small>›</small></div>',
        f'  <div class="nav-items">',
        f'    <a class="{ic("传播引导策略")}" href="{prefix}处置引导/传播引导策略/index.html"><span>传播引导策略</span></a>',
        f'    <a class="{ic("选题线索池")}" href="{prefix}处置引导/选题线索池/index.html"><span>选题线索池</span></a>',
        f'    <div class="nav-item"><span>选题看板</span></div>',
        f'    <a class="{ic("多稿合并工具")}" href="{prefix}处置引导/多稿合并工具/index.html"><span>多稿合并工具</span></a>',
        f'    <a class="{ic("舆情复盘分析")}" href="{prefix}处置引导/舆情复盘分析/index.html"><span>舆情复盘分析</span></a>',
        f'  </div>',
        f'</section>',

        # ── 知识库（分组）
        f'<section class="{gc("知识库")}">',
        f'  <div class="nav-group-title" onclick="toggleGroup(this)"><div class="title-left">{ICON_BOOK}<span>知识库</span></div><small>›</small></div>',
        f'  <div class="nav-items">',
        f'    <a class="{ic("热点话题案例库")}" href="{prefix}知识库/热点话题案例库/index.html"><span>热点话题案例库</span></a>',
        f'    <div class="nav-item"><span>宣传引导策略库</span></div>',
        f'    <div class="nav-item"><span>决策报告知识库</span></div>',
        f'    <div class="nav-item"><span>重点关注对象库</span></div>',
        f'    <div class="nav-item"><span>行业术语与本体知识库</span></div>',
        f'  </div>',
        f'</section>',
    ]
    return '\n    '.join(lines)


def replace_sidebar_nav_area(content, new_nav_inner):
    """找到 <div class="sidebar-nav-area"> ... </div> 并替换内部内容。"""
    marker = '<div class="sidebar-nav-area">'
    start = content.find(marker)
    if start == -1:
        return content, False

    # 深度计数找匹配的 </div>
    pos = start + len(marker)
    depth = 1
    end_div_pos = -1
    while pos < len(content) and depth > 0:
        next_open  = content.find('<div', pos)
        next_close = content.find('</div>', pos)
        if next_close == -1:
            return content, False
        if next_open != -1 and next_open < next_close:
            ch = content[next_open + 4] if next_open + 4 < len(content) else ''
            if ch in ' \t\n\r>':
                depth += 1
            pos = next_open + 4
        else:
            depth -= 1
            if depth == 0:
                end_div_pos = next_close + 6
                break
            pos = next_close + 6

    if end_div_pos == -1:
        return content, False

    new_block = f'{marker}\n    {new_nav_inner}\n    </div>'
    result = content[:start] + new_block + content[end_div_pos:]
    return result, True


# ─── 文件列表：(路径, prefix, active_group, active_item) ────
FILES = [
    ('首页/index.html',                               '../',     '首页',       ''),
    ('监测预警/AI智能推荐/index.html',               '../../', '监测预警',    'AI智能推荐'),
    ('监测预警/信息监测/index.html',                 '../../', '监测预警',    ''),        # 已从导航移除但文件还在
    ('监测预警/关键对象监测/index.html',             '../../', '监测预警',    '舆情监测'),
    ('监测预警/热点榜单/index.html',                 '../../', '监测预警',    '热点榜单'),
    ('监测预警/预警查询/index.html',                 '../../', '监测预警',    '预警查询'),
    ('事件分析/事件管理/index.html',                 '../../', '事件分析',    ''),
    ('事件分析/事件管理/创建分析/index.html',        '../../../','事件分析',   ''),
    ('事件分析/事件管理/事件分析详情/index.html',    '../../../','事件分析',   ''),
    ('智能体编报/index.html',                         '../',     '智能体编报', ''),
    ('处置引导/传播引导策略/index.html',             '../../', '处置引导',    '传播引导策略'),
    ('处置引导/选题线索池/index.html',               '../../', '处置引导',    '选题线索池'),
    ('处置引导/多稿合并工具/index.html',             '../../', '处置引导',    '多稿合并工具'),
    ('处置引导/舆情复盘分析/index.html',             '../../', '处置引导',    '舆情复盘分析'),
    ('处置引导/舆情复盘分析/复盘详情/index.html',    '../../../','处置引导',   '舆情复盘分析'),
    ('处置引导/舆情复盘分析/新建复盘任务/index.html','../../../','处置引导',   '舆情复盘分析'),
    ('智能检索/index.html',                          '../',    '智能检索',    ''),
    ('知识库/热点话题案例库/index.html',             '../../', '知识库',      '热点话题案例库'),
]

ok_count = 0
fail_count = 0

for rel, prefix, active_group, active_item in FILES:
    fp = os.path.join(ROOT, rel)
    if not os.path.exists(fp):
        print(f'SKIP (not found): {rel}')
        continue
    with open(fp, 'r', encoding='utf-8') as f:
        content = f.read()

    nav_html = build_nav(prefix, active_group, active_item)
    new_content, changed = replace_sidebar_nav_area(content, nav_html)

    if not changed:
        print(f'FAIL (no sidebar-nav-area): {rel}')
        fail_count += 1
        continue

    with open(fp, 'w', encoding='utf-8') as f:
        f.write(new_content)
    ok_count += 1
    print(f'OK  {rel}')

print(f'\n完成: {ok_count} 成功, {fail_count} 失败')
