# Fix e4/e5/e6 viewpoints - add type + supportRate + extra entries
c = open(r'c:\Pros\ZJ0512\监测预警\AI智能推荐\index.html', encoding='utf-8').read()

replacements = [
    (
        # e4
        '                viewpoints: [\n'
        '                    { text: "此次破案规模史无前例，充分体现了执法部门的专业能力。", platform: "新闻资讯", sentiment: "positive" },\n'
        '                    { text: "案件背后的利益链条盘根错节，单靠海关难以根绝。", platform: "Telegram", sentiment: "negative" },\n'
        '                    { text: "走私路线长期存在，监管漏洞亟需从制度层面填补。", platform: "短视频", sentiment: "negative" }\n'
        '                ],',

        '                viewpoints: [\n'
        '                    { text: "此次破案规模史无前例，充分体现了执法部门的专业能力。", platform: "新闻资讯", sentiment: "positive", type: "expert", supportRate: 79 },\n'
        '                    { text: "案件背后的利益链条盘根错节，单靠海关难以根绝。", platform: "Telegram", sentiment: "negative", type: "netizen", supportRate: 84 },\n'
        '                    { text: "走私路线长期存在，监管漏洞亟需从制度层面填补。", platform: "短视频", sentiment: "negative", type: "netizen", supportRate: 88 },\n'
        '                    { text: "联合执法机制需进一步深化，跨部门数据共享是关键。", platform: "新闻资讯", sentiment: "neutral", type: "expert", supportRate: 67 },\n'
        '                    { text: "司法惩处力度是否足够形成震慑，仍有待观察。", platform: "论坛", sentiment: "neutral", type: "expert", supportRate: 72 },\n'
        '                    { text: "灰产团伙渗透程度令人震惊，本地治安令人担忧。", platform: "Telegram", sentiment: "negative", type: "netizen", supportRate: 76 }\n'
        '                ],',
        'e4'
    ),
    (
        # e5
        '                viewpoints: [\n'
        '                    { text: "杂志的专题策划触角敏锐，节选虽片面但引发关注有其价值。", platform: "Threads", sentiment: "neutral" },\n'
        '                    { text: "自媒体断章取义严重扭曲了文章立意，机构应积极澄清。", platform: "短视频", sentiment: "negative" }\n'
        '                ],',

        '                viewpoints: [\n'
        '                    { text: "杂志的专题策划触角敏锐，节选虽片面但引发关注有其价值。", platform: "Threads", sentiment: "neutral", type: "expert", supportRate: 62 },\n'
        '                    { text: "自媒体断章取义严重扭曲了文章立意，机构应积极澄清。", platform: "短视频", sentiment: "negative", type: "netizen", supportRate: 83 },\n'
        '                    { text: "机构内容一旦进入二次传播链，原始语境极易失真。", platform: "新闻资讯", sentiment: "neutral", type: "expert", supportRate: 75 },\n'
        '                    { text: "青年读者更信任自媒体解读而非机构原文，这是信任危机。", platform: "Threads", sentiment: "negative", type: "netizen", supportRate: 69 },\n'
        '                    { text: "专题报道需配套完整的事实说明文档，以应对片段化传播。", platform: "新闻资讯", sentiment: "neutral", type: "expert", supportRate: 81 },\n'
        '                    { text: "机构不回应只会让流言越演越烈，必须主动出击。", platform: "短视频", sentiment: "negative", type: "netizen", supportRate: 78 }\n'
        '                ],',
        'e5'
    ),
    (
        # e6
        '                viewpoints: [\n'
        '                    { text: "大型传媒集团投入数字化转型，是整个行业的趋势性信号。", platform: "LinkedIn", sentiment: "neutral" },\n'
        '                    { text: "重金招聘数字岗位，可能对本地媒体人才市场造成抽血效应。", platform: "短视频", sentiment: "negative" }\n'
        '                ],',

        '                viewpoints: [\n'
        '                    { text: "大型传媒集团投入数字化转型，是整个行业的趋势性信号。", platform: "LinkedIn", sentiment: "neutral", type: "expert", supportRate: 77 },\n'
        '                    { text: "重金招聘数字岗位，可能对本地媒体人才市场造成抽血效应。", platform: "短视频", sentiment: "negative", type: "netizen", supportRate: 70 },\n'
        '                    { text: "数字实验室能否产出商业价值，关键在于内容变现模式。", platform: "LinkedIn", sentiment: "neutral", type: "expert", supportRate: 68 },\n'
        '                    { text: "本地小型媒体将面临更大人才流失压力，难以竞争。", platform: "短视频", sentiment: "negative", type: "netizen", supportRate: 65 },\n'
        '                    { text: "可借鉴竞对布局思路，尽快启动差异化数字内容战略。", platform: "LinkedIn", sentiment: "neutral", type: "expert", supportRate: 74 },\n'
        '                    { text: "该集团招聘薪酬远超市场均价，吸引力极强。", platform: "短视频", sentiment: "neutral", type: "netizen", supportRate: 59 }\n'
        '                ],',
        'e6'
    ),
]

c2 = c
for old, new, name in replacements:
    if old in c2:
        c2 = c2.replace(old, new, 1)
        print(f'{name}: replaced OK')
    else:
        print(f'{name}: NOT FOUND - checking...')
        # Try to find partial match
        snippet = old[:80]
        idx = c2.find(snippet)
        print(f'  First 80 chars found at: {idx}')

open(r'c:\Pros\ZJ0512\监测预警\AI智能推荐\index.html', 'w', encoding='utf-8').write(c2)
print('Done')
