# -*- coding: utf-8 -*-
import re

with open(r'c:\Pros\ZJ0512\监测预警\AI智能推荐\index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# ── 1. Add name fields to expert viewpoints ──

replacements = [
    # e1 旧楼火灾
    (
        '{ text: "旧式住宅楼棚架整改工作长期滞后，此次起火是制度性问题。", platform: "新闻资讯", sentiment: "negative", type: "expert", supportRate: 82 }',
        '{ text: "旧式住宅楼棚架整改工作长期滞后，此次起火是制度性问题。", platform: "新闻资讯", sentiment: "negative", type: "expert", supportRate: 82, name: "李志豪（安全工程师）" }'
    ),
    (
        '{ text: "当局需尽快制定强制性棚架检验周期制度，防患于未然。", platform: "新闻资讯", sentiment: "negative", type: "expert", supportRate: 76 }',
        '{ text: "当局需尽快制定强制性棚架检验周期制度，防患于未然。", platform: "新闻资讯", sentiment: "negative", type: "expert", supportRate: 76, name: "陈国明（建筑专家）" }'
    ),
    (
        '{ text: "消防处与房屋署协作顺畅，应急机制值得肖定。", platform: "Facebook", sentiment: "positive", type: "expert", supportRate: 58 }',
        '{ text: "消防处与房屋署协作顺畅，应急机制值得肖定。", platform: "Facebook", sentiment: "positive", type: "expert", supportRate: 58, name: "张文明（消防顾问）" }'
    ),
    # e2 高才通
    (
        '{ text: "收紧门槛有助提高人才质量，是合理的政策微调。", platform: "新闻资讯", sentiment: "positive", type: "expert", supportRate: 54 }',
        '{ text: "收紧门槛有助提高人才质量，是合理的政策微调。", platform: "新闻资讯", sentiment: "positive", type: "expert", supportRate: 54, name: "林慧敏（人才政策学者）" }'
    ),
    (
        '{ text: "外媒引述未经证实，当局应尽快澄清消除误解。", platform: "微博", sentiment: "neutral", type: "expert", supportRate: 79 }',
        '{ text: "外媒引述未经证实，当局应尽快澄清消除误解。", platform: "微博", sentiment: "neutral", type: "expert", supportRate: 79, name: "王德华（传播学教授）" }'
    ),
    (
        '{ text: "政策调整需结合劳动市场数据评估，不应急于收紧门槛。", platform: "新闻资讯", sentiment: "neutral", type: "expert", supportRate: 71 }',
        '{ text: "政策调整需结合劳动市场数据评估，不应急于收紧门槛。", platform: "新闻资讯", sentiment: "neutral", type: "expert", supportRate: 71, name: "黄建国（经济学家）" }'
    ),
    # e3 无感通关
    (
        '{ text: "技术系统需公开接受第三方隐私影响评估，方可全面推行。", platform: "新闻资讯", sentiment: "neutral", type: "expert", supportRate: 69 }',
        '{ text: "技术系统需公开接受第三方隐私影响评估，方可全面推行。", platform: "新闻资讯", sentiment: "neutral", type: "expert", supportRate: 69, name: "刘晓东（数据隐私专家）" }'
    ),
    (
        '{ text: "通关效率提升有助于大湾区互联互通，经济效益显著。", platform: "新闻资讯", sentiment: "positive", type: "expert", supportRate: 74 }',
        '{ text: "通关效率提升有助于大湾区互联互通，经济效益显著。", platform: "新闻资讯", sentiment: "positive", type: "expert", supportRate: 74, name: "陈志远（经济分析师）" }'
    ),
    (
        '{ text: "数据跨境流动缺乏明确的法律保障，存在隐患。", platform: "微博", sentiment: "negative", type: "expert", supportRate: 61 }',
        '{ text: "数据跨境流动缺乏明确的法律保障，存在隐患。", platform: "微博", sentiment: "negative", type: "expert", supportRate: 61, name: "蔡明华（法律顾问）" }'
    ),
    # e4 走私快艇
    (
        '{ text: "此次破案规模史无前例，充分体现了执法部门的专业能力。", platform: "新闻资讯", sentiment: "positive", type: "expert", supportRate: 79 }',
        '{ text: "此次破案规模史无前例，充分体现了执法部门的专业能力。", platform: "新闻资讯", sentiment: "positive", type: "expert", supportRate: 79, name: "林国强（执法研究员）" }'
    ),
    (
        '{ text: "联合执法机制需进一步深化，跨部门数据共享是关键。", platform: "新闻资讯", sentiment: "neutral", type: "expert", supportRate: 67 }',
        '{ text: "联合执法机制需进一步深化，跨部门数据共享是关键。", platform: "新闻资讯", sentiment: "neutral", type: "expert", supportRate: 67, name: "张伟雄（安全顾问）" }'
    ),
    (
        '{ text: "司法惩处力度是否足够形成震慑，仍有待观察。", platform: "论坛", sentiment: "neutral", type: "expert", supportRate: 72 }',
        '{ text: "司法惩处力度是否足够形成震慑，仍有待观察。", platform: "论坛", sentiment: "neutral", type: "expert", supportRate: 72, name: "李建明（法学教授）" }'
    ),
    # e5 杂志社
    (
        '{ text: "杂志的专题策划触角敏锐，节选虽片面但引发关注有其价值。", platform: "Threads", sentiment: "neutral", type: "expert", supportRate: 62 }',
        '{ text: "杂志的专题策划触角敏锐，节选虽片面但引发关注有其价值。", platform: "Threads", sentiment: "neutral", type: "expert", supportRate: 62, name: "陈美琳（传媒学者）" }'
    ),
    (
        '{ text: "机构内容一旦进入二次传播链，原始语境极易失真。", platform: "新闻资讯", sentiment: "neutral", type: "expert", supportRate: 75 }',
        '{ text: "机构内容一旦进入二次传播链，原始语境极易失真。", platform: "新闻资讯", sentiment: "neutral", type: "expert", supportRate: 75, name: "刘志华（新闻研究员）" }'
    ),
    (
        '{ text: "专题报道需配套完整的事实说明文档，以应对片段化传播。", platform: "新闻资讯", sentiment: "neutral", type: "expert", supportRate: 81 }',
        '{ text: "专题报道需配套完整的事实说明文档，以应对片段化传播。", platform: "新闻资讯", sentiment: "neutral", type: "expert", supportRate: 81, name: "黄晓燕（媒体顾问）" }'
    ),
    # e6 数字实验室
    (
        '{ text: "大型传媒集团投入数字化转型，是整个行业的趋势性信号。", platform: "LinkedIn", sentiment: "neutral", type: "expert", supportRate: 77 }',
        '{ text: "大型传媒集团投入数字化转型，是整个行业的趋势性信号。", platform: "LinkedIn", sentiment: "neutral", type: "expert", supportRate: 77, name: "林思齐（媒体战略分析师）" }'
    ),
    (
        '{ text: "数字实验室能否产出商业价值，关键在于内容变现模式。", platform: "LinkedIn", sentiment: "neutral", type: "expert", supportRate: 68 }',
        '{ text: "数字实验室能否产出商业价值，关键在于内容变现模式。", platform: "LinkedIn", sentiment: "neutral", type: "expert", supportRate: 68, name: "张建明（数字媒体专家）" }'
    ),
    (
        '{ text: "可借鉴竞对布局思路，尽快启动差异化数字内容战略。", platform: "LinkedIn", sentiment: "neutral", type: "expert", supportRate: 74 }',
        '{ text: "可借鉴竞对布局思路，尽快启动差异化数字内容战略。", platform: "LinkedIn", sentiment: "neutral", type: "expert", supportRate: 74, name: "陈志豪（媒体运营顾问）" }'
    ),
    # e7 创科
    (
        '{ text: "大湾区政策协同为港澳科研提供了前所未有的发展空间。", platform: "微信", sentiment: "positive", type: "expert", supportRate: 80 }',
        '{ text: "大湾区政策协同为港澳科研提供了前所未有的发展空间。", platform: "微信", sentiment: "positive", type: "expert", supportRate: 80, name: "林志远（科技政策专家）" }'
    ),
    (
        '{ text: "政策框架已具雏形，执行层面的落地机制有待细化。", platform: "新闻资讯", sentiment: "neutral", type: "expert", supportRate: 73 }',
        '{ text: "政策框架已具雏形，执行层面的落地机制有待细化。", platform: "新闻资讯", sentiment: "neutral", type: "expert", supportRate: 73, name: "陈建国（产业经济学家）" }'
    ),
    (
        '{ text: "产学研合作落地案例仍偏少，政策落地速度需提速。", platform: "新闻资讯", sentiment: "neutral", type: "expert", supportRate: 69 }',
        '{ text: "产学研合作落地案例仍偏少，政策落地速度需提速。", platform: "新闻资讯", sentiment: "neutral", type: "expert", supportRate: 69, name: "黄明辉（科研合作顾问）" }'
    ),
]

for old, new in replacements:
    if old in content:
        content = content.replace(old, new)
        print(f'✓ Replaced: {old[:40]}...')
    else:
        print(f'✗ NOT FOUND: {old[:60]}...')

# ── 2. Update renderVp to show expert name & remove platform ──
old_render = '''const renderVp = list => list.map(v => `
                                <div class="drawer-viewpoint-item">
                                    <div style="display:flex;align-items:flex-start;justify-content:space-between;gap:8px;margin-bottom:5px">
                                        <div class="drawer-viewpoint-text" style="margin-bottom:0">${v.text}</div>
                                        <span class="drawer-viewpoint-sentiment ${v.sentiment}" style="flex-shrink:0">${v.sentiment === "positive" ? "\\u6b63\\u9762" : v.sentiment === "negative" ? "\\u8d1f\\u9762" : "\\u4e2d\\u7acb"}</span>
                                    </div>
                                    <div style="display:flex;align-items:center;gap:8px">
                                        <div class="drawer-viewpoint-platform">${v.platform}</div>
                                        <div style="flex:1;height:3px;border-radius:2px;background:rgba(122,145,184,0.12)"><div style="height:100%;border-radius:2px;background:var(--primary);width:${v.supportRate||0}%"></div></div>
                                        <span style="font-size:11px;color:#7a91b0;font-weight:600;min-width:28px;text-align:right">${v.supportRate||0}%</span>
                                    </div>
                                </div>`).join("");'''

new_render = '''const renderVp = list => list.map(v => `
                                <div class="drawer-viewpoint-item">
                                    ${v.type === "expert" && v.name ? `<div style="font-size:11px;font-weight:700;color:#4a6fa5;margin-bottom:3px">${v.name}</div>` : ''}
                                    <div style="display:flex;align-items:flex-start;justify-content:space-between;gap:8px;margin-bottom:5px">
                                        <div class="drawer-viewpoint-text" style="margin-bottom:0">${v.text}</div>
                                        <span class="drawer-viewpoint-sentiment ${v.sentiment}" style="flex-shrink:0">${v.sentiment === "positive" ? "\\u6b63\\u9762" : v.sentiment === "negative" ? "\\u8d1f\\u9762" : "\\u4e2d\\u7acb"}</span>
                                    </div>
                                    <div style="display:flex;align-items:center;gap:8px">
                                        <div style="flex:1;height:3px;border-radius:2px;background:rgba(122,145,184,0.12)"><div style="height:100%;border-radius:2px;background:var(--primary);width:${v.supportRate||0}%"></div></div>
                                        <span style="font-size:11px;color:#7a91b0;font-weight:600;min-width:28px;text-align:right">${v.supportRate||0}%</span>
                                    </div>
                                </div>`).join("");'''

if old_render in content:
    content = content.replace(old_render, new_render)
    print('✓ renderVp updated')
else:
    print('✗ renderVp NOT FOUND - trying partial match...')
    # Try to find what's there
    idx = content.find('const renderVp')
    if idx >= 0:
        print('Found renderVp at index', idx)
        print(repr(content[idx:idx+600]))

with open(r'c:\Pros\ZJ0512\监测预警\AI智能推荐\index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print('\nDone.')
