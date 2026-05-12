"""
Add heat value / on-chart duration / rank-change / platform-logo clusters
to: 内地总榜 + 微博热搜 + 抖音热搜 + 百度热搜
"""
import re

FILE = r'c:\Pros\ZJ0512\监测预警\热点榜单\index.html'
with open(FILE, 'r', encoding='utf-8') as f:
    html = f.read()

# ─────────────────────────────────────────────────────────────────
# 1.  New CSS
# ─────────────────────────────────────────────────────────────────
new_css = """
/* ---- 内地总榜增强 ---- */
.total-row{align-items:flex-start!important}
.t-body{flex:1;min-width:0;display:flex;flex-direction:column;gap:3px}
.t-title-row{display:flex;align-items:flex-start;gap:4px;min-width:0}
.t-meta-row{display:flex;align-items:center;gap:5px;flex-wrap:wrap}
.t-logos{display:flex;gap:2px;align-items:center}
.t-logo{width:14px;height:14px;border-radius:3px;font-size:8px;font-weight:800;display:grid;place-items:center;flex:0 0 14px;line-height:1}
.t-logo-wb{background:#e6162d;color:#fff}
.t-logo-dy{background:#161823;color:#fff}
.t-logo-bd{background:#2932e1;color:#fff}
.t-heat{font-size:11px;color:#f5502a;font-weight:700;white-space:nowrap}
.t-dur{font-size:10px;color:var(--text-faint);white-space:nowrap}
.t-chg{font-size:10px;font-weight:700;padding:1px 5px;border-radius:3px;white-space:nowrap;flex-shrink:0;align-self:flex-start;margin-top:2px}
.t-chg.chg-up{color:#12a87a;background:rgba(18,168,122,0.10)}
.t-chg.chg-dn{color:#e04040;background:rgba(224,64,64,0.10)}
.t-chg.chg-new{color:#2b61f0;background:rgba(43,97,240,0.10)}
/* ---- 热搜增强 (微博/抖音/百度) ---- */
.p-body{flex:1;min-width:0;display:flex;flex-direction:column;gap:2px}
.p-meta-row{display:flex;align-items:center;gap:5px;flex-wrap:wrap;margin-top:2px}
.p-heat{font-size:11px;color:#f5502a;font-weight:700;white-space:nowrap}
.p-dur{font-size:10px;color:var(--text-faint);white-space:nowrap}
.p-chg{font-size:10px;font-weight:700;padding:1px 5px;border-radius:3px;white-space:nowrap}
.p-chg.chg-up{color:#12a87a;background:rgba(18,168,122,0.10)}
.p-chg.chg-dn{color:#e04040;background:rgba(224,64,64,0.10)}
.p-chg.chg-new{color:#2b61f0;background:rgba(43,97,240,0.10)}
"""
html = html.replace('@media(max-width:1400px)', new_css + '@media(max-width:1400px)', 1)

# ─────────────────────────────────────────────────────────────────
# Helper builders
# ─────────────────────────────────────────────────────────────────
LOGO_MAP = {
    'wb': '<span class="t-logo t-logo-wb">微</span>',
    'dy': '<span class="t-logo t-logo-dy">抖</span>',
    'bd': '<span class="t-logo t-logo-bd">百</span>',
}

def logos(plats):
    return '<span class="t-logos">' + ''.join(LOGO_MAP[p] for p in plats) + '</span>'

def t_chg(v):
    if v == 'NEW':  return '<span class="t-chg chg-new">NEW</span>'
    if v[0] == '↑': return f'<span class="t-chg chg-up">{v}</span>'
    if v[0] == '↓': return f'<span class="t-chg chg-dn">{v}</span>'
    return ''

def p_chg(v):
    if v == 'NEW':  return '<span class="p-chg chg-new">NEW</span>'
    if v[0] == '↑': return f'<span class="p-chg chg-up">{v}</span>'
    if v[0] == '↓': return f'<span class="p-chg chg-dn">{v}</span>'
    return ''

def total_row(num, nc, title, rc, rl, plats, heat, dur, ch):
    nc_str = f' {nc}' if nc else ''
    return (
        f'              <div class="total-row">'
        f'<div class="t-num{nc_str}">{num}</div>'
        f'<div class="t-body">'
        f'<div class="t-title-row"><div class="t-title">{title}</div>'
        f'<span class="risk-tag total-risk {rc}">{rl}</span></div>'
        f'<div class="t-meta-row">{logos(plats)}'
        f'<span class="t-heat">🔥 {heat}</span>'
        f'<span class="t-dur">⏱ 在榜{dur}</span>'
        f'</div></div>'
        f'{t_chg(ch)}</div>'
    )

def plist_item(num, title, rc, rl, heat, dur, ch):
    return (
        f'              <div class="plist-item"><span class="p-num">{num}</span>'
        f'<div class="p-body">'
        f'<div class="p-title">{title}<span class="risk-tag {rc}">{rl}</span></div>'
        f'<div class="p-meta-row">'
        f'<span class="p-heat">🔥 {heat}</span>'
        f'<span class="p-dur">⏱ 在榜{dur}</span>'
        f'{p_chg(ch)}'
        f'</div></div></div>'
    )

# ─────────────────────────────────────────────────────────────────
# 2.  内地总榜
# ─────────────────────────────────────────────────────────────────
inland_items = [
    ('n1','十四届全国人大四次会议议程公布',      'risk-hi','高危',['wb','dy','bd'],'8.6万','1.2小时','NEW'),
    ('n2','代表建议设定3000亿元高速免费额度',    'risk-md','中危',['wb','bd'],    '6.8万','0.5小时','↑3'),
    ('n3','12306回应乘客在普速铁路上用排插',    'risk-lo','低危',['wb','dy'],    '5.4万','2.1小时','↓1'),
    ('',  '2026全国两会为什么格外重要',          'risk-md','中危',['bd','wb'],    '4.9万','3.0小时','↑2'),
    ('',  '驻日大使馆提醒：防范日本「撞人族」',  'risk-md','中危',['wb','dy'],    '4.2万','0.8小时','↑1'),
    ('',  '雷军2026两会议题引发广泛关注',        'risk-md','中危',['wb','bd'],    '3.8万','1.5小时','↓2'),
    ('',  '北京今日迎来今年第一场大雪',          'risk-lo','低危',['wb','dy'],    '3.1万','4.2小时','↑1'),
    ('',  '山东修高铁站挖出5亿年前化石石海',    'risk-lo','低危',['wb','dy'],    '2.7万','2.8小时','↓1'),
    ('',  '政协委员建议高中纳入义务教育',        'risk-md','中危',['wb','bd'],    '2.3万','1.0小时','NEW'),
    ('',  '代表委员议建立提案落地落实机制',      'risk-md','中危',['wb'],         '1.9万','3.4小时','↑2'),
]

inland_rows = '\n'.join(
    total_row(i+1, nc, t, rc, rl, pl, h, d, ch)
    for i, (nc, t, rc, rl, pl, h, d, ch) in enumerate(inland_items)
)

new_inland_card = (
    '            <!-- 内地总榜 -->\n'
    '            <div class="plat-card">\n'
    '              <div class="plat-head"><span class="plat-icon" style="background:linear-gradient(135deg,#e04040,#c47d10);color:#fff;font-size:10px;font-weight:800">内</span>内地总榜</div>\n'
    + inland_rows + '\n'
    '            </div>'
)

m = re.search(
    r'            <!-- 内地总榜 -->\n            <div class="plat-card">.*?</div>(?=\n            <!-- 香港总榜 -->)',
    html, re.DOTALL
)
if m:
    html = html[:m.start()] + new_inland_card + html[m.end():]
else:
    print("ERROR: 内地总榜 block not found")

# ─────────────────────────────────────────────────────────────────
# 3.  微博热搜
# ─────────────────────────────────────────────────────────────────
weibo_items = [
    ('美国比人升左希莫德旺大事点重斩行人理？',   'risk-md','中危','5.2万','0.3小时','NEW'),
    ('2026年3月 足球女将 Season 2（2）',          'risk-lo','低危','4.1万','1.5小时','↑2'),
    ('泻桥直播正式做香港人 下月全港香港身份证',  'risk-lo','低危','3.7万','2.2小时','↓1'),
    ('MacBook Neo开箱评测｜厚高外型＋A18 Pr...', 'risk-lo','低危','3.2万','0.9小时','↑1'),
    ('热制ion9 能够到指境 建造大家起返来拍',      'risk-lo','低危','2.9万','1.8小时','↓2'),
    ('刘美：看着谷爱凌的人「很虚伪」',            'risk-lo','低危','2.5万','3.1小时','↑3'),
    ('两会代表热议逃离身份证实名制问题',          'risk-hi','高危','2.2万','0.6小时','NEW'),
    ('雷军2026两会建议引局关注',                  'risk-md','中危','1.9万','2.4小时','↓1'),
    ('山东修高鐵站挖出5亿年前化石百岚',          'risk-lo','低危','1.6万','4.0小时','↑1'),
    ('政協委员建议高中纳入义务教育',              'risk-lo','低危','1.3万','1.2小时','↓3'),
]

weibo_rows = '\n'.join(plist_item(i+1, *d) for i, d in enumerate(weibo_items))
new_weibo_card = (
    '            <div class="plat-card">\n'
    '              <div class="plat-head"><span class="plat-icon" style="background:#e6162d;color:#fff;font-size:12px">微</span>微博热搜</div>\n'
    + weibo_rows + '\n'
    '            </div>'
)

m = re.search(
    r'            <div class="plat-card">\n              <div class="plat-head"><span class="plat-icon" style="background:#e6162d[^"]*"[^/]*/span>微博热搜</div>.*?</div>(?=\n            <!-- 抖音热搜 -->)',
    html, re.DOTALL
)
if m:
    html = html[:m.start()] + new_weibo_card + html[m.end():]
else:
    print("ERROR: 微博热搜 block not found")

# ─────────────────────────────────────────────────────────────────
# 4.  抖音热搜
# ─────────────────────────────────────────────────────────────────
douyin_items = [
    ('尖沙咀人气烘焙店GUILT FREE开业两月关停…',   'risk-lo','低危','6.3万','0.5小时','NEW'),
    ('中西局势脱油价受勒 升学顾升指迎20亿学…',    'risk-md','中危','5.1万','1.2小时','↑1'),
    ('油价｜刷翻展揭长子达：跨境审加大浪引迪理…', 'risk-md','中危','4.4万','2.0小时','↓1'),
    ('紫菊蓝｜美军引以为傲的技术优势，如何肇震…', 'risk-md','中危','3.8万','0.7小时','↑2'),
    ('国泰航空：向员工放假当于每逾11星期薪金…',   'risk-lo','低危','3.2万','3.5小时','↓1'),
    ('两毓饭英文？DSE英文口试闯两毓毓 两毓…',     'risk-lo','低危','2.7万','1.9小时','↑1'),
    ('两会代表热议提案如何落地实施',               'risk-md','中危','2.3万','0.4小时','NEW'),
    ('香港教育改革动态：新课程标准将长',           'risk-md','中危','1.9万','2.8小时','↓2'),
    ('DeepSeek 底底是什么？香港年轻人炸了',       'risk-lo','低危','1.5万','1.3小时','↑3'),
    ('香港达人分享日本生活体验引关注',             'risk-lo','低危','1.1万','3.7小时','↓1'),
]

douyin_rows = '\n'.join(plist_item(i+1, *d) for i, d in enumerate(douyin_items))
new_douyin_card = (
    '            <!-- 抖音热搜 -->\n'
    '            <div class="plat-card">\n'
    '              <div class="plat-head"><span class="plat-icon" style="background:#000;color:#fff;font-size:12px">🎵</span>抖音热搜</div>\n'
    + douyin_rows + '\n'
    '            </div>'
)

m = re.search(
    r'            <!-- 抖音热搜 -->\n            <div class="plat-card">.*?</div>(?=\n            <!-- 百度热搜 -->)',
    html, re.DOTALL
)
if m:
    html = html[:m.start()] + new_douyin_card + html[m.end():]
else:
    print("ERROR: 抖音热搜 block not found")

# ─────────────────────────────────────────────────────────────────
# 5.  百度热搜
# ─────────────────────────────────────────────────────────────────
baidu_items = [
    ('能源搭棚翻 泛滥副成灾',             'risk-lo','低危','7.2万','2.1小时','↑1'),
    ('「套匙程」激震 副副刷副旁边据撞推客','risk-lo','低危','5.8万','0.8小时','↑2'),
    ('AI聪明狂潮 大模型股爱炒热点',       'risk-lo','低危','4.6万','1.5小时','↓1'),
    ('两投行传人 退出竞赛关于IPO',         'risk-md','中危','3.4万','3.2小时','↑1'),
    ('中东黑火暗温 道指涨479回款',         'risk-md','中危','2.9万','0.6小时','NEW'),
    ('各地填充始 建OpenClaw产业',          'risk-lo','低危','2.1万','4.1小时','↓2'),
]

baidu_rows = '\n'.join(plist_item(i+1, *d) for i, d in enumerate(baidu_items))
new_baidu_card = (
    '            <!-- 百度热搜 -->\n'
    '            <div class="plat-card" style="grid-column:span 1">\n'
    '              <div class="plat-head"><span class="plat-icon" style="background:#2932e1;color:#fff;font-size:10px;font-weight:800">百</span>百度热搜</div>\n'
    + baidu_rows + '\n'
    '            </div>'
)

m = re.search(
    r'            <!-- 百度热搜 -->\n            <div class="plat-card" style="grid-column:span 1">.*?</div>(?=\n          </div>)',
    html, re.DOTALL
)
if m:
    html = html[:m.start()] + new_baidu_card + html[m.end():]
else:
    print("ERROR: 百度热搜 block not found")

# ─────────────────────────────────────────────────────────────────
# Write
# ─────────────────────────────────────────────────────────────────
with open(FILE, 'w', encoding='utf-8') as f:
    f.write(html)

print("Done – 内地总榜 + 微博/抖音/百度 enhanced.")
