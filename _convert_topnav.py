"""
把所有页面的左侧边栏导航改为顶部导航栏。
- 移除 <aside class="sidebar">
- 将 <header class="global-topbar"> 替换为含 logo + 导航 + 操作按钮的新顶栏
- 注入 CSS override（追加进已有 <style> 块末尾）
"""
import os, glob

ROOT = r'c:\Pros\ZJ0512'

# ─── 小图标 (14×14) ───────────────────────────────────────────────────────────
ICON_HOME    = '<svg viewBox="0 0 24 24" fill="none" width="14" height="14"><path d="M3 9L12 3L21 9V20H15V14H9V20H3V9Z" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/></svg>'
ICON_MONITOR = '<svg viewBox="0 0 24 24" fill="none" width="14" height="14"><path d="M3 3h18v12H3V3zM8 21h8M12 15v6" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>'
ICON_INCIDENT= '<svg viewBox="0 0 24 24" fill="none" width="14" height="14"><path d="M5 18L9 13L12 15L18 8L19 18H5Z" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/></svg>'
ICON_SEARCH  = '<svg viewBox="0 0 24 24" fill="none" width="14" height="14"><circle cx="11" cy="11" r="7" stroke="currentColor" stroke-width="1.8"/><path d="M20 20L16 16" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></svg>'
ICON_HANDLE  = '<svg viewBox="0 0 24 24" fill="none" width="14" height="14"><path d="M12 4V20M4 12H20" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></svg>'
ICON_BOOK    = '<svg viewBox="0 0 24 24" fill="none" width="14" height="14"><path d="M6 5H18V19H6V5ZM9 9H15M9 13H15" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></svg>'
ICON_AGENT   = '<svg viewBox="0 0 24 24" fill="none" width="14" height="14"><rect x="4" y="4" width="16" height="16" rx="2" stroke="currentColor" stroke-width="1.8"/><path d="M8 9h8M8 13h5" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></svg>'
ICON_CHEVRON = '<svg class="chevron" viewBox="0 0 24 24" fill="none" width="10" height="10"><path d="M6 9L12 15L18 9" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>'
SITAWARE_ICO = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none"><circle cx="12" cy="12" r="3" fill="currentColor"/><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/><path d="M12 6C9.24 6 7 8.24 7 11" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/><path d="M12 8.5C10.62 8.5 9.5 9.62 9.5 11" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg>'
STAR_ICO     = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none"><path d="M12 17.4L6.12 20.5L7.24 13.93L2.48 9.3L9.06 8.34L12 2.4L14.94 8.34L21.52 9.3L16.76 13.93L17.88 20.5L12 17.4Z" stroke="currentColor" stroke-width="1.5" stroke-linejoin="round"/></svg>'
BELL_ICO     = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none"><path d="M6 17H18L17 11C17 8.24 14.76 6 12 6C9.24 6 7 8.24 7 11L6 17Z" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/><path d="M10 19C10.4 20.2 11.1 20.8 12 20.8C12.9 20.8 13.6 20.2 14 19" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg>'
TASK_ICO     = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none"><rect x="5" y="3" width="14" height="18" rx="2" stroke="currentColor" stroke-width="1.6"/><path d="M9 3h6v2a1 1 0 01-1 1h-4a1 1 0 01-1-1V3z" stroke="currentColor" stroke-width="1.6"/><path d="M9 12h6M9 16h4" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg>'

# ─── CSS 注入（追加到已有 <style> 块末尾，用 MARKER 防重复） ─────────────────
MARKER = '/* @@TOP-NAV-OVERRIDE@@ */'
TOPNAV_CSS = f"""{MARKER}
.app-shell{{display:flex!important;flex-direction:column!important;min-height:100vh!important}}
.sidebar{{display:none!important}}
.global-topbar{{display:flex!important;align-items:center!important;flex-wrap:nowrap!important;height:auto!important;min-height:56px!important;overflow:visible!important;padding:0!important;gap:0!important;position:sticky;top:0;z-index:100;background:#fff;border-bottom:1px solid rgba(122,145,184,0.14);box-shadow:0 1px 4px rgba(26,44,82,0.06)}}
.topbar-module-label,.topbar-spacer,.topbar-left,.topbar-right,.topbar-parent,.topbar-sep,.topbar-label,.topbar-current{{display:none!important}}
.main-area{{grid-column:unset!important;grid-row:unset!important;flex:1 1 auto!important;overflow-y:auto!important;min-height:0!important}}
.topbar-brand{{display:flex;align-items:center;justify-content:center;height:56px;width:194px;flex:0 0 194px;border-right:1px solid rgba(122,145,184,0.1);padding:0 14px;overflow:hidden}}
.top-nav{{display:flex;align-items:stretch;height:56px;padding:0 2px;flex:1 1 auto;overflow:visible;min-width:0}}
.top-nav-item{{position:relative;display:inline-flex;align-items:center;gap:6px;height:56px;padding:0 16px;font-size:13px;font-weight:600;color:#5a6a82;text-decoration:none;cursor:pointer;user-select:none;white-space:nowrap;transition:color .15s;border-bottom:2.5px solid transparent;flex-shrink:0;box-sizing:border-box}}
.top-nav-item:hover{{color:var(--primary,#2b61f0)}}
.top-nav-item.active{{color:var(--primary,#2b61f0);border-bottom-color:var(--primary,#2b61f0)}}
.top-nav-item svg:not(.chevron){{opacity:.7;transition:opacity .15s}}
.top-nav-item:hover svg:not(.chevron),.top-nav-item.active svg:not(.chevron){{opacity:1}}
.chevron{{opacity:.4;transition:transform .2s;margin-left:1px;flex-shrink:0}}
.has-dropdown:hover>.chevron{{transform:rotate(180deg)}}
.top-dropdown{{display:none;position:absolute;top:100%;left:0;min-width:166px;background:#fff;border:1px solid rgba(122,145,184,0.15);border-radius:10px;box-shadow:0 8px 24px rgba(26,44,82,0.12);padding:6px;z-index:500;flex-direction:column;gap:1px}}
.has-dropdown:hover>.top-dropdown{{display:flex}}
.top-dropdown a{{display:flex;align-items:center;padding:8px 12px;border-radius:7px;font-size:13px;font-weight:500;color:#2c3e56;text-decoration:none;transition:background .12s,color .12s;white-space:nowrap}}
.top-dropdown a:hover{{background:rgba(43,97,240,0.06);color:var(--primary,#2b61f0)}}
.top-dropdown a.active{{background:rgba(43,97,240,0.09);color:var(--primary,#2b61f0);font-weight:700}}
.topbar-actions{{display:flex;align-items:center;gap:8px;padding:0 14px 0 6px;flex-shrink:0;height:56px}}
"""


def build_topbar(prefix, active_group, active_item, logo_svg):
    def nac(name):
        return 'top-nav-item active' if name == active_group else 'top-nav-item'
    def nac_dd(name):
        return 'top-nav-item has-dropdown active' if name == active_group else 'top-nav-item has-dropdown'
    def dac(name):
        return ' class="active"' if name == active_item else ''

    mon_dd = (
        f'<div class="top-dropdown">'
        f'<a href="{prefix}监测预警/AI智能推荐/index.html"{dac("AI智能推荐")}>AI智能推荐</a>'
        f'<a href="{prefix}监测预警/热点榜单/index.html"{dac("热点榜单")}>热点榜单</a>'
        f'<a href="{prefix}监测预警/关键对象监测/index.html"{dac("方案监测")}>方案监测</a>'
        f'<a href="{prefix}监测预警/预警查询/index.html"{dac("预警查询")}>预警查询</a>'
        f'</div>'
    )
    han_dd = (
        f'<div class="top-dropdown">'
        f'<a href="{prefix}处置引导/传播引导策略/index.html"{dac("传播引导策略")}>传播引导策略</a>'
        f'<a href="{prefix}处置引导/选题线索池/index.html"{dac("选题线索池")}>选题线索池</a>'
        f'<a href="#">选题看板</a>'
        f'<a href="{prefix}处置引导/多稿合并工具/index.html"{dac("多稿合并工具")}>多稿合并工具</a>'
        f'<a href="{prefix}处置引导/舆情复盘分析/index.html"{dac("舆情复盘分析")}>舆情复盘分析</a>'
        f'</div>'
    )
    kb_dd = (
        f'<div class="top-dropdown">'
        f'<a href="{prefix}知识库/热点话题案例库/index.html"{dac("热点话题案例库")}>热点话题案例库</a>'
        f'<a href="#">宣传引导策略库</a>'
        f'<a href="#">决策报告知识库</a>'
        f'<a href="#">重点关注对象库</a>'
        f'<a href="#">行业术语与本体知识库</a>'
        f'</div>'
    )

    return (
        '<header class="global-topbar">\n'
        f'  <div class="topbar-brand">{logo_svg}</div>\n'
        f'  <nav class="top-nav">\n'
        f'    <a class="{nac("首页")}" href="{prefix}首页/index.html">{ICON_HOME}<span>首页</span></a>\n'
        f'    <div class="{nac_dd("舆情监测")}">{ICON_MONITOR}<span>舆情监测</span>{ICON_CHEVRON}{mon_dd}</div>\n'
        f'    <a class="{nac("智能检索")}" href="{prefix}智能检索/index.html">{ICON_SEARCH}<span>智能检索</span></a>\n'
        f'    <a class="{nac("事件分析")}" href="{prefix}事件分析/事件管理/index.html">{ICON_INCIDENT}<span>事件分析</span></a>\n'
        f'    <a class="{nac("AI编报")}" href="{prefix}智能体编报/index.html">{ICON_AGENT}<span>AI编报</span></a>\n'
        f'    <div class="{nac_dd("选题策划")}">{ICON_HANDLE}<span>选题策划</span>{ICON_CHEVRON}{han_dd}</div>\n'
        f'    <div class="{nac_dd("知识库")}">{ICON_BOOK}<span>知识库</span>{ICON_CHEVRON}{kb_dd}</div>\n'
        f'  </nav>\n'
        f'  <div class="topbar-actions">\n'
        f'    <a class="topbar-sitaware-btn" href="#" title="态势感知">{SITAWARE_ICO}<span>态势感知</span></a>\n'
        f'    <button class="icon-button badge-btn" title="消息">{BELL_ICO}<span class="badge">3</span></button>\n'
        f'    <button class="icon-button" title="任务中心">{TASK_ICO}</button>\n'
        f'    <div class="avatar"><div class="avatar-badge">管</div><strong>管理员</strong></div>\n'
        f'  </div>\n'
        '</header>'
    )


def extract_logo(content):
    """从 .brand 或 .topbar-brand div 提取 SVG"""
    for marker in ['<div class="topbar-brand">', '<div class="brand">']:
        start = content.find(marker)
        if start != -1:
            inner_start = start + len(marker)
            inner_end   = content.find('</div>', inner_start)
            if inner_end != -1:
                svg = content[inner_start:inner_end].strip()
                if svg:
                    return svg
    return ''


def remove_sidebar(content):
    start = content.find('<aside class="sidebar">')
    if start == -1:
        return content
    pos   = start + len('<aside class="sidebar">')
    depth = 1
    while pos < len(content) and depth > 0:
        no = content.find('<aside', pos)
        nc = content.find('</aside>', pos)
        if nc == -1:
            return content
        if no != -1 and no < nc:
            depth += 1
            pos = no + 6
        else:
            depth -= 1
            if depth == 0:
                return content[:start] + content[nc + len('</aside>'):]
            pos = nc + 8
    return content


def replace_topbar(content, new_topbar):
    # 支持 global-topbar 和 topbar 两种类名
    for cls in ['<header class="global-topbar">', '<header class="topbar">']:
        start = content.find(cls)
        if start != -1:
            end = content.find('</header>', start)
            if end != -1:
                return content[:start] + new_topbar + content[end + len('</header>'):]
    return content


def inject_css(content):
    """替换已有的 CSS 块（如存在），或追加到最后一个 </style> 前"""
    # 先移除旧的注入块
    if MARKER in content:
        start = content.find(MARKER)
        # 找到这段CSS的结束：下一个 </style> 标签
        end = content.find('</style>', start)
        if end != -1:
            content = content[:start] + content[end:]
    # 追加新 CSS
    pos = content.rfind('</style>')
    if pos != -1:
        return content[:pos] + '\n' + TOPNAV_CSS + content[pos:]
    pos = content.find('</head>')
    return content[:pos] + f'<style>{TOPNAV_CSS}</style>\n' + content[pos:]


# ─── 文件列表 ─────────────────────────────────────────────────────────────────
FILES = [
    ('首页/index.html',                               '../',      '首页',       ''),
    ('监测预警/AI智能推荐/index.html',                '../../',   '舆情监测',   'AI智能推荐'),
    ('监测预警/信息监测/index.html',                  '../../',   '舆情监测',   ''),
    ('监测预警/关键对象监测/index.html',              '../../',   '舆情监测',   '方案监测'),
    ('监测预警/热点榜单/index.html',                  '../../',   '舆情监测',   '热点榜单'),
    ('监测预警/预警查询/index.html',                  '../../',   '舆情监测',   '预警查询'),
    ('事件分析/事件管理/index.html',                  '../../',   '事件分析',   ''),
    ('事件分析/事件管理/创建分析/index.html',         '../../../','事件分析',   ''),
    ('事件分析/事件管理/事件分析详情/index.html',     '../../../','事件分析',   ''),
    ('智能体编报/index.html',                         '../',      'AI编报',     ''),
    ('处置引导/传播引导策略/index.html',              '../../',   '选题策划',   '传播引导策略'),
    ('处置引导/选题线索池/index.html',                '../../',   '选题策划',   '选题线索池'),
    ('处置引导/多稿合并工具/index.html',              '../../',   '选题策划',   '多稿合并工具'),
    ('处置引导/舆情复盘分析/index.html',              '../../',   '选题策划',   '舆情复盘分析'),
    ('处置引导/舆情复盘分析/复盘详情/index.html',     '../../../','选题策划',   '舆情复盘分析'),
    ('处置引导/舆情复盘分析/新建复盘任务/index.html', '../../../','选题策划',   '舆情复盘分析'),
    ('智能检索/index.html',                           '../',      '智能检索',   ''),
    ('知识库/热点话题案例库/index.html',              '../../',   '知识库',     '热点话题案例库'),
]

# ─── 先提取 logo ─────────────────────────────────────────────────────────────
# 始终从原始 SVG 文件读取，避免多次运行后内容丢失
logo_svg = ''
svg_src = os.path.join(ROOT, 'svg代码.txt')
if os.path.exists(svg_src):
    with open(svg_src, 'rb') as f:
        logo_svg = f.read().decode('utf-8').strip()
    print(f'Logo: {len(logo_svg)} chars from svg代码.txt')
else:
    # fallback: 从文件中提取
    for rel, *_ in FILES:
        fp = os.path.join(ROOT, rel)
        if os.path.exists(fp):
            with open(fp, 'r', encoding='utf-8') as f:
                logo_svg = extract_logo(f.read())
            if logo_svg:
                print(f'Logo: {len(logo_svg)} chars from {rel}')
                break

if not logo_svg:
    print('WARNING: 未找到 Logo SVG！')

ok = fail = 0
for rel, prefix, active_group, active_item in FILES:
    fp = os.path.join(ROOT, rel)
    if not os.path.exists(fp):
        print(f'SKIP (missing): {rel}')
        continue

    with open(fp, 'r', encoding='utf-8') as f:
        content = f.read()

    new_tb  = build_topbar(prefix, active_group, active_item, logo_svg)
    content = replace_topbar(content, new_tb)
    content = remove_sidebar(content)
    content = inject_css(content)

    with open(fp, 'w', encoding='utf-8') as f:
        f.write(content)
    ok += 1
    print(f'OK  {rel}')

print(f'\n完成: {ok} 成功, {fail} 失败')
