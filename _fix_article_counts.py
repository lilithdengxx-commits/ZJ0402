# -*- coding: utf-8 -*-
import re

with open(r'c:\Pros\ZJ0512\监测预警\AI智能推荐\index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# ─────────────────────────────────────────────────────────────
# 1. 更新 e1-e7 的 articleCount 并扩展 articles 数组
# ─────────────────────────────────────────────────────────────

extra_articles = {
    "e1": {
        "new_count": 7,
        "new_ac_line": "                articleCount: 3, platforms: [\"Facebook\", \"新闻资讯\", \"短视频\"],",
        "new_ac_repl": "                articleCount: 7, platforms: [\"Facebook\", \"新闻资讯\", \"短视频\", \"微博\"],",
        "old_articles": """                    { id: 101, title: "大埔宏福苑外墙棚架突发起火，现场视频迅速扩散", platform: "Facebook", sentiment: "negative", sentimentLabel: "负面", dateTime: "2026-03-30T09:22:00" },
                    { id: 102, title: "消防处：大埔棚架火警明火受控，无人受伤", platform: "新闻资讯", sentiment: "neutral", sentimentLabel: "中立", dateTime: "2026-03-30T09:50:00" },
                    { id: 103, title: "【深度】香港旧楼棚架安全监管为何长期滞后", platform: "新闻资讯", sentiment: "negative", sentimentLabel: "负面", dateTime: "2026-03-30T14:12:10" }""",
        "new_articles": """                    { id: 101, title: "大埔宏福苑外墙棚架突发起火，现场视频迅速扩散", platform: "Facebook", sentiment: "negative", sentimentLabel: "负面", dateTime: "2026-03-30T09:22:00" },
                    { id: 102, title: "消防处：大埔棚架火警明火受控，无人受伤", platform: "新闻资讯", sentiment: "neutral", sentimentLabel: "中立", dateTime: "2026-03-30T09:50:00" },
                    { id: 103, title: "【深度】香港旧楼棚架安全监管为何长期滞后", platform: "新闻资讯", sentiment: "negative", sentimentLabel: "负面", dateTime: "2026-03-30T14:12:10" },
                    { id: 104, title: "棚架起火事件引发居民安全忧虑，多区业主关注同类隐患", platform: "微博", sentiment: "negative", sentimentLabel: "负面", dateTime: "2026-03-30T11:00:00" },
                    { id: 105, title: "区议员要求当局公布全港旧楼棚架安全检查报告", platform: "新闻资讯", sentiment: "neutral", sentimentLabel: "中立", dateTime: "2026-03-30T12:30:00" },
                    { id: 106, title: "大埔起火短片二次剪辑版本持续发酵，平台流量攀升", platform: "短视频", sentiment: "negative", sentimentLabel: "负面", dateTime: "2026-03-30T10:15:00" },
                    { id: 107, title: "房屋署回应棚架安全质疑：已启动紧急排查程序", platform: "新闻资讯", sentiment: "neutral", sentimentLabel: "中立", dateTime: "2026-03-30T15:00:00" }""",
    },
    "e2": {
        "new_count": 6,
        "new_ac_line": "                articleCount: 3, platforms: [\"新闻资讯\", \"微博\", \"论坛\"],",
        "new_ac_repl": "                articleCount: 6, platforms: [\"新闻资讯\", \"微博\", \"论坛\"],",
        "old_articles": """                    { id: 201, title: "外媒引述消息称高才通续签门槛或将收紧，引发高关注争议", platform: "新闻资讯", sentiment: "neutral", sentimentLabel: "中立", dateTime: "2026-03-30T13:46:00" },
                    { id: 202, title: "高才通政策再调整？各方回应不一，业界忧虑人才流失", platform: "论坛", sentiment: "negative", sentimentLabel: "负面", dateTime: "2026-03-30T11:00:00" },
                    { id: 203, title: "港府人才政策连续调整，区域人才竞争格局深度分析", platform: "微博", sentiment: "neutral", sentimentLabel: "中立", dateTime: "2026-03-30T09:20:00" }""",
        "new_articles": """                    { id: 201, title: "外媒引述消息称高才通续签门槛或将收紧，引发高关注争议", platform: "新闻资讯", sentiment: "neutral", sentimentLabel: "中立", dateTime: "2026-03-30T13:46:00" },
                    { id: 202, title: "高才通政策再调整？各方回应不一，业界忧虑人才流失", platform: "论坛", sentiment: "negative", sentimentLabel: "负面", dateTime: "2026-03-30T11:00:00" },
                    { id: 203, title: "港府人才政策连续调整，区域人才竞争格局深度分析", platform: "微博", sentiment: "neutral", sentimentLabel: "中立", dateTime: "2026-03-30T09:20:00" },
                    { id: 204, title: "在港高才通持有人反应：等待官方正式澄清，心情忐忑", platform: "论坛", sentiment: "negative", sentimentLabel: "负面", dateTime: "2026-03-30T10:30:00" },
                    { id: 205, title: "劳工局：目前无任何关于高才通收紧的政策决定", platform: "新闻资讯", sentiment: "neutral", sentimentLabel: "中立", dateTime: "2026-03-30T14:30:00" },
                    { id: 206, title: "人才政策敏感期：各界建议当局加强信息透明度", platform: "微博", sentiment: "neutral", sentimentLabel: "中立", dateTime: "2026-03-30T12:00:00" }""",
    },
    "e3": {
        "new_count": 5,
        "new_ac_line": "                articleCount: 2, platforms: [\"微博\", \"小红书\"],",
        "new_ac_repl": "                articleCount: 5, platforms: [\"微博\", \"小红书\", \"新闻资讯\"],",
        "old_articles": """                    { id: 301, title: "深圳湾口岸拟试行\\u201c无感通关\\u201d，数据隐私讨论同步升温", platform: "微博", sentiment: "neutral", sentimentLabel: "中立", dateTime: "2026-03-30T12:58:00" },
                    { id: 302, title: "无感通关体验分享：排队从40分钟缩短至5分钟", platform: "小红书", sentiment: "positive", sentimentLabel: "正面", dateTime: "2026-03-30T10:20:00" }""",
        "new_articles": """                    { id: 301, title: "深圳湾口岸拟试行\\u201c无感通关\\u201d，数据隐私讨论同步升温", platform: "微博", sentiment: "neutral", sentimentLabel: "中立", dateTime: "2026-03-30T12:58:00" },
                    { id: 302, title: "无感通关体验分享：排队从40分钟缩短至5分钟", platform: "小红书", sentiment: "positive", sentimentLabel: "正面", dateTime: "2026-03-30T10:20:00" },
                    { id: 303, title: "口岸生物识别数据安全：法律专家解析授权边界", platform: "新闻资讯", sentiment: "neutral", sentimentLabel: "中立", dateTime: "2026-03-30T11:30:00" },
                    { id: 304, title: "跨境居民热议无感通关：方便是方便，就是担心数据", platform: "小红书", sentiment: "neutral", sentimentLabel: "中立", dateTime: "2026-03-30T09:00:00" },
                    { id: 305, title: "官方回应数据安全疑虑：系统已通过安全评估", platform: "新闻资讯", sentiment: "positive", sentimentLabel: "正面", dateTime: "2026-03-30T14:00:00" }""",
    },
    "e4": {
        "new_count": 8,
        "new_ac_line": "                articleCount: 3, platforms: [\"新闻资讯\", \"Telegram\", \"短视频\"],",
        "new_ac_repl": "                articleCount: 8, platforms: [\"新闻资讯\", \"Telegram\", \"短视频\", \"论坛\"],",
        "old_articles": """                    { id: 401, title: "海关破获历来最大宗走私快艇案，黑帮利益链词云发酵", platform: "新闻资讯", sentiment: "negative", sentimentLabel: "负面", dateTime: "2026-03-30T11:44:00" },
                    { id: 402, title: "走私快艇案主犯落网：揭秘跨境灰产运作方式", platform: "Telegram", sentiment: "negative", sentimentLabel: "负面", dateTime: "2026-03-30T09:10:00" },
                    { id: 403, title: "百亿货值走私案始末，海关如何布局三年终破获", platform: "短视频", sentiment: "neutral", sentimentLabel: "中立", dateTime: "2026-03-30T10:30:00" }""",
        "new_articles": """                    { id: 401, title: "海关破获历来最大宗走私快艇案，黑帮利益链词云发酵", platform: "新闻资讯", sentiment: "negative", sentimentLabel: "负面", dateTime: "2026-03-30T11:44:00" },
                    { id: 402, title: "走私快艇案主犯落网：揭秘跨境灰产运作方式", platform: "Telegram", sentiment: "negative", sentimentLabel: "负面", dateTime: "2026-03-30T09:10:00" },
                    { id: 403, title: "百亿货值走私案始末，海关如何布局三年终破获", platform: "短视频", sentiment: "neutral", sentimentLabel: "中立", dateTime: "2026-03-30T10:30:00" },
                    { id: 404, title: "走私团伙跨境作案路线曝光，港深两地警方联合响应", platform: "新闻资讯", sentiment: "negative", sentimentLabel: "负面", dateTime: "2026-03-30T08:30:00" },
                    { id: 405, title: "Telegram频道转发案件细节，灰产叙事持续放大", platform: "Telegram", sentiment: "negative", sentimentLabel: "负面", dateTime: "2026-03-30T10:00:00" },
                    { id: 406, title: "海关关长记者会回应：已移交律政司提出检控", platform: "新闻资讯", sentiment: "neutral", sentimentLabel: "中立", dateTime: "2026-03-30T13:00:00" },
                    { id: 407, title: "治安议题热搜：走私快艇案引发市民对港口管理的质疑", platform: "论坛", sentiment: "negative", sentimentLabel: "负面", dateTime: "2026-03-30T12:00:00" },
                    { id: 408, title: "专家分析走私快艇案：跨境协作执法机制亟待升级", platform: "新闻资讯", sentiment: "neutral", sentimentLabel: "中立", dateTime: "2026-03-30T14:00:00" }""",
    },
    "e5": {
        "new_count": 6,
        "new_ac_line": "                articleCount: 2, platforms: [\"Threads\", \"短视频\"],",
        "new_ac_repl": "                articleCount: 6, platforms: [\"Threads\", \"短视频\", \"新闻资讯\"],",
        "old_articles": """                    { id: 501, title: "Threads热帖指向杂志社专题策划与青年就业议题，讨论度快速抬升", platform: "Threads", sentiment: "negative", sentimentLabel: "负面", dateTime: "2026-03-30T14:12:10" },
                    { id: 502, title: "媒体内容遭断章取义：自媒体传播生态下机构如何维护公信力", platform: "短视频", sentiment: "negative", sentimentLabel: "负面", dateTime: "2026-03-30T12:30:00" }""",
        "new_articles": """                    { id: 501, title: "Threads热帖指向杂志社专题策划与青年就业议题，讨论度快速抬升", platform: "Threads", sentiment: "negative", sentimentLabel: "负面", dateTime: "2026-03-30T14:12:10" },
                    { id: 502, title: "媒体内容遭断章取义：自媒体传播生态下机构如何维护公信力", platform: "短视频", sentiment: "negative", sentimentLabel: "负面", dateTime: "2026-03-30T12:30:00" },
                    { id: 503, title: "杂志社专题原文与自媒体节选版本对比：差距在哪里", platform: "新闻资讯", sentiment: "neutral", sentimentLabel: "中立", dateTime: "2026-03-30T13:00:00" },
                    { id: 504, title: "青年就业议题热传：读者反馈原文立意与流传版本相距甚远", platform: "Threads", sentiment: "negative", sentimentLabel: "负面", dateTime: "2026-03-30T11:00:00" },
                    { id: 505, title: "机构编辑回应断章取义质疑：已在官方渠道补充完整背景", platform: "短视频", sentiment: "neutral", sentimentLabel: "中立", dateTime: "2026-03-30T15:00:00" },
                    { id: 506, title: "传播学者：片段化传播是当前机构媒体面临的结构性挑战", platform: "新闻资讯", sentiment: "neutral", sentimentLabel: "中立", dateTime: "2026-03-30T16:00:00" }""",
    },
    "e6": {
        "new_count": 5,
        "new_ac_line": "                articleCount: 2, platforms: [\"短视频\", \"LinkedIn\"],",
        "new_ac_repl": "                articleCount: 5, platforms: [\"短视频\", \"LinkedIn\", \"新闻资讯\"],",
        "old_articles": """                    { id: 601, title: "某大型传媒集团成立\\u201c南部发展数字实验室\\u201d，招聘信息受关注", platform: "短视频", sentiment: "neutral", sentimentLabel: "中立", dateTime: "2026-03-30T10:22:00" },
                    { id: 602, title: "传媒数字化浪潮下的竞争格局：谁在布局南部市场", platform: "LinkedIn", sentiment: "neutral", sentimentLabel: "中立", dateTime: "2026-03-30T09:00:00" }""",
        "new_articles": """                    { id: 601, title: "某大型传媒集团成立\\u201c南部发展数字实验室\\u201d，招聘信息受关注", platform: "短视频", sentiment: "neutral", sentimentLabel: "中立", dateTime: "2026-03-30T10:22:00" },
                    { id: 602, title: "传媒数字化浪潮下的竞争格局：谁在布局南部市场", platform: "LinkedIn", sentiment: "neutral", sentimentLabel: "中立", dateTime: "2026-03-30T09:00:00" },
                    { id: 603, title: "数字实验室招聘岗位解析：短视频主编、数据编辑薪酬曝光", platform: "LinkedIn", sentiment: "neutral", sentimentLabel: "中立", dateTime: "2026-03-30T08:30:00" },
                    { id: 604, title: "业界反应：竞争对手大手笔投入数字转型，本地媒体压力加大", platform: "新闻资讯", sentiment: "negative", sentimentLabel: "负面", dateTime: "2026-03-30T11:00:00" },
                    { id: 605, title: "传媒集团数字化战略深度解读：南部布局背后的商业逻辑", platform: "新闻资讯", sentiment: "neutral", sentimentLabel: "中立", dateTime: "2026-03-30T12:00:00" }""",
    },
    "e7": {
        "new_count": 7,
        "new_ac_line": "                articleCount: 3, platforms: [\"微信\", \"微博\", \"新闻资讯\"],",
        "new_ac_repl": "                articleCount: 7, platforms: [\"微信\", \"微博\", \"新闻资讯\"],",
        "old_articles": """                    { id: 701, title: "创科及工业局新政解读：大湾区科研协同再升级", platform: "微信", sentiment: "positive", sentimentLabel: "正面", dateTime: "2026-03-30T07:00:00" },
                    { id: 702, title: "从香港科大看大湾区产学研合作模式", platform: "新闻资讯", sentiment: "neutral", sentimentLabel: "中立", dateTime: "2026-03-30T08:00:00" },
                    { id: 703, title: "科研人才薪酬调查：港澳与内地竞争城市差距几何", platform: "微博", sentiment: "negative", sentimentLabel: "负面", dateTime: "2026-03-30T08:30:00" }""",
        "new_articles": """                    { id: 701, title: "创科及工业局新政解读：大湾区科研协同再升级", platform: "微信", sentiment: "positive", sentimentLabel: "正面", dateTime: "2026-03-30T07:00:00" },
                    { id: 702, title: "从香港科大看大湾区产学研合作模式", platform: "新闻资讯", sentiment: "neutral", sentimentLabel: "中立", dateTime: "2026-03-30T08:00:00" },
                    { id: 703, title: "科研人才薪酬调查：港澳与内地竞争城市差距几何", platform: "微博", sentiment: "negative", sentimentLabel: "负面", dateTime: "2026-03-30T08:30:00" },
                    { id: 704, title: "大湾区科研人才新政细则出台，港澳配额有望增加", platform: "微信", sentiment: "positive", sentimentLabel: "正面", dateTime: "2026-03-30T06:00:00" },
                    { id: 705, title: "香港科技大学与内地高校联合实验室正式挂牌", platform: "新闻资讯", sentiment: "positive", sentimentLabel: "正面", dateTime: "2026-03-30T07:30:00" },
                    { id: 706, title: "科研人才谈大湾区体验：机会多，但申请流程仍需优化", platform: "微博", sentiment: "neutral", sentimentLabel: "中立", dateTime: "2026-03-30T08:00:00" },
                    { id: 707, title: "产学研合作案例盘点：哪些香港项目在大湾区落地成功", platform: "新闻资讯", sentiment: "positive", sentimentLabel: "正面", dateTime: "2026-03-30T09:00:00" }""",
    },
}

for eid, data in extra_articles.items():
    # Update articleCount line
    if data["new_ac_line"] in content:
        content = content.replace(data["new_ac_line"], data["new_ac_repl"])
        print(f'✓ {eid} articleCount → {data["new_count"]}')
    else:
        print(f'✗ {eid} articleCount line NOT FOUND')

    # Replace articles array content
    if data["old_articles"] in content:
        content = content.replace(data["old_articles"], data["new_articles"])
        print(f'✓ {eid} articles expanded')
    else:
        print(f'✗ {eid} articles NOT FOUND')

# ─────────────────────────────────────────────────────────────
# 2. Update mk() articleCount formula + generate matching articles
# ─────────────────────────────────────────────────────────────
old_ac = "articleCount:Math.max(2,Math.floor(sc/25)),platforms:[\"新闻资讯\",\"微博\"],"
new_ac = "articleCount:Math.min(9,Math.max(3,Math.floor(sc/12))),platforms:[\"新闻资讯\",\"微博\",\"论坛\"],"
if old_ac in content:
    content = content.replace(old_ac, new_ac)
    print('✓ mk() articleCount formula updated')
else:
    print('✗ mk() articleCount formula NOT FOUND')

old_arts = "                articles:[{id:parseInt(id.replace(/\\D/g,\"\"))*10,title:t,platform:\"新闻资讯\",sentiment:snt,sentimentLabel:snl,dateTime:dt}]};"
new_arts = r"""                articles:(function(){
                    var base=parseInt(id.replace(/\D/g,""))*10;
                    var cnt=Math.min(9,Math.max(3,Math.floor(sc/12)));
                    var pls=["新闻资讯","微博","论坛","短视频","Facebook","小红书","Telegram","微信","LinkedIn"];
                    var snlMap={"positive":"正面","negative":"负面","neutral":"中立"};
                    var tpls=[
                        t,
                        "【跟进】"+t.slice(0,18)+"最新进展",
                        "深度解析："+t.slice(0,16)+"背后的多重因素",
                        "各方回应："+t.slice(0,15)+"争议持续发酵",
                        "专家解读：如何看待"+t.slice(0,12)+"的影响",
                        "数据报告："+t.slice(0,14)+"舆情热度分析",
                        "评论："+t.slice(0,16)+"折射出哪些深层问题",
                        "当局回应"+t.slice(0,12)+"相关质疑",
                        "综述："+t.slice(0,14)+"各方立场全梳理"
                    ];
                    var sentArr=snt==="negative"?["negative","negative","neutral","negative","neutral","negative","negative","neutral","neutral"]:
                                snt==="positive"?["positive","positive","neutral","positive","neutral","positive","neutral","positive","neutral"]:
                                ["neutral","neutral","negative","neutral","positive","neutral","negative","neutral","positive"];
                    var result=[];
                    for(var i=0;i<cnt;i++){
                        var s=sentArr[i]||"neutral";
                        result.push({id:base+i,title:tpls[i]||tpls[0],platform:pls[i%pls.length],sentiment:s,sentimentLabel:snlMap[s]||"中立",dateTime:dt});
                    }
                    return result;
                })()}; """
if old_arts in content:
    content = content.replace(old_arts, new_arts)
    print('✓ mk() articles generation updated')
else:
    print('✗ mk() articles NOT FOUND, trying partial...')
    idx = content.find('articles:[{id:parseInt')
    if idx >= 0:
        print('Found at', idx, repr(content[idx:idx+200]))

with open(r'c:\Pros\ZJ0512\监测预警\AI智能推荐\index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print('\nAll done.')
