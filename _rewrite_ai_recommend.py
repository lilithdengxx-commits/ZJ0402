# -*- coding: utf-8 -*-
import sys

with open(r'c:\Pros\ZJ0512\监测预警\AI智能推荐\index.html', 'r', encoding='utf-8') as f:
    content = f.read()

orig_len = len(content)

# ===========================================================================
# 1. CSS: Insert new styles before /* @@TOP-NAV-OVERRIDE@@ */
# ===========================================================================
new_css = r"""/* Event cards */
.event-card{position:relative;padding:16px 16px 0;border-bottom:1px solid rgba(122,145,184,0.1);transition:background 0.12s}
.event-card:hover{background:rgba(43,97,240,0.025)}
.event-card:last-child{border-bottom:none}
.event-tag-row{display:flex;align-items:center;gap:5px;flex-wrap:wrap;margin-bottom:7px}
.event-title-btn{display:block;width:100%;text-align:left;border:none;background:none;padding:0;cursor:pointer;font:inherit}
.event-title-btn .event-title{font-size:clamp(14px,0.95vw,17px);font-weight:700;color:#182033;line-height:1.35;margin:0 0 8px}
.event-title-btn:hover .event-title{color:var(--primary)}
.event-meta-row{display:flex;align-items:center;gap:8px;flex-wrap:wrap;padding-bottom:14px}
.event-meta-item{display:inline-flex;align-items:center;gap:4px;font-size:12px;color:#7d8da4}
.event-source-count{display:inline-flex;align-items:center;gap:4px;padding:2px 8px;border-radius:999px;background:#f2f5fb;border:1px solid rgba(122,145,184,0.12);font-size:11px;color:#5a7099;font-weight:600}
.tag.risk-high{color:#c0392b;background:rgba(233,78,78,0.1);border-color:rgba(233,78,78,0.18)}
.tag.risk-medium{color:#a06b00;background:rgba(255,205,104,0.18);border-color:rgba(215,138,0,0.18)}
.tag.risk-low{color:#0f9360;background:rgba(31,209,122,0.1);border-color:rgba(31,209,122,0.18)}
/* Drawer */
.drawer-overlay{position:fixed;inset:0;background:rgba(17,24,39,0.3);backdrop-filter:blur(2px);opacity:0;visibility:hidden;transition:opacity 0.2s,visibility 0.2s;z-index:200}
.drawer-overlay.open{opacity:1;visibility:visible}
.event-drawer{position:fixed;top:0;right:0;bottom:0;width:min(540px,94vw);background:#fff;box-shadow:-4px 0 32px rgba(26,44,82,0.14);transform:translateX(100%);transition:transform 0.26s cubic-bezier(0.4,0,0.2,1);z-index:210;display:flex;flex-direction:column;overflow:hidden}
.event-drawer.open{transform:translateX(0)}
.drawer-header{flex:0 0 auto;display:flex;align-items:center;gap:10px;padding:14px 16px;border-bottom:1px solid rgba(122,145,184,0.12);background:#fff}
.drawer-title-text{flex:1 1 auto;font-size:14px;font-weight:700;color:#1e2d45;line-height:1.4;overflow:hidden;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical}
.drawer-close-btn{flex:0 0 auto;width:30px;height:30px;border:1px solid rgba(122,145,184,0.16);border-radius:8px;background:#fff;color:#7a8ea8;font-size:18px;display:flex;align-items:center;justify-content:center;cursor:pointer;transition:background 0.15s,color 0.15s}
.drawer-close-btn:hover{background:#f0f4fb;color:#1e2d45}
.drawer-body{flex:1 1 auto;overflow-y:auto;padding:0}
.drawer-body::-webkit-scrollbar{width:4px}
.drawer-body::-webkit-scrollbar-thumb{background:rgba(0,0,0,0.1);border-radius:999px}
.drawer-section{padding:16px 18px;border-bottom:1px solid rgba(122,145,184,0.1)}
.drawer-section:last-child{border-bottom:none}
.drawer-section-title{display:flex;align-items:center;gap:7px;font-size:13px;font-weight:700;color:#38507a;margin-bottom:12px}
.drawer-section-title::before{content:"";width:3px;height:14px;border-radius:2px;background:var(--primary);flex-shrink:0}
.drawer-risk-bar{display:flex;align-items:center;gap:8px;padding:10px 14px;border-radius:10px;background:#f8fafd;border:1px solid rgba(122,145,184,0.1);margin-bottom:10px;flex-wrap:wrap}
.drawer-ai-summary{font-size:14px;line-height:1.7;color:#3a4d67;background:rgba(43,97,240,0.04);border-left:3px solid var(--primary);padding:10px 14px;border-radius:0 8px 8px 0;margin-bottom:10px}
.drawer-tag-row{display:flex;flex-wrap:wrap;gap:5px}
.drawer-tag{display:inline-flex;align-items:center;padding:3px 10px;border-radius:999px;background:rgba(43,97,240,0.07);border:1px solid rgba(43,97,240,0.12);color:#3a6abf;font-size:12px;font-weight:500}
.drawer-viewpoint-item{display:flex;gap:8px;padding:8px 0;border-bottom:1px solid rgba(122,145,184,0.08)}
.drawer-viewpoint-item:last-child{border-bottom:none}
.drawer-viewpoint-platform{font-size:11px;font-weight:700;color:#7a8ea8;min-width:52px;padding-top:2px;flex-shrink:0}
.drawer-viewpoint-text{flex:1 1 auto;font-size:13px;line-height:1.6;color:#3a4d67}
.drawer-viewpoint-sentiment{font-size:10px;font-weight:700;padding:1px 6px;border-radius:999px;flex-shrink:0;margin-top:2px;align-self:flex-start}
.drawer-viewpoint-sentiment.negative{color:#c0392b;background:rgba(233,78,78,0.1)}
.drawer-viewpoint-sentiment.positive{color:#0f9360;background:rgba(31,209,122,0.1)}
.drawer-viewpoint-sentiment.neutral{color:#a06b00;background:rgba(255,205,104,0.18)}
.drawer-suggestion-item{display:flex;align-items:flex-start;gap:8px;padding:5px 0;font-size:13px;line-height:1.6;color:#3a4d67}
.drawer-suggestion-num{flex:0 0 20px;width:20px;height:20px;border-radius:50%;background:rgba(43,97,240,0.1);color:var(--primary);font-size:11px;font-weight:700;display:flex;align-items:center;justify-content:center;margin-top:1px}
.drawer-article-item{display:flex;align-items:flex-start;gap:8px;padding:8px 0;border-bottom:1px solid rgba(122,145,184,0.08)}
.drawer-article-item:last-child{border-bottom:none}
.drawer-article-title{flex:1 1 auto;font-size:13px;font-weight:500;color:#1e2d45;line-height:1.5}
.drawer-article-meta{display:flex;align-items:center;gap:5px;margin-top:3px;flex-wrap:wrap}
.drawer-article-meta span{font-size:11px;color:#9ab0c8}
/* Timeline */
.timeline-list{padding:0;list-style:none;margin:0;position:relative}
.timeline-list::before{content:"";position:absolute;left:6px;top:6px;bottom:6px;width:2px;background:linear-gradient(to bottom,rgba(43,97,240,0.3),rgba(43,97,240,0.06));border-radius:1px}
.timeline-item{position:relative;padding:0 0 14px 24px}
.timeline-item:last-child{padding-bottom:0}
.timeline-item::before{content:"";position:absolute;left:2px;top:5px;width:10px;height:10px;border-radius:50%;background:#fff;border:2.5px solid var(--primary);box-sizing:border-box}
.timeline-time{font-size:11px;font-weight:700;color:#8fa4be;margin-bottom:2px}
.timeline-desc{font-size:13px;line-height:1.55;color:#3a4d67}
/* Domain L2 chips */
.domain-l1-strip{display:flex;align-items:center;gap:6px;flex:1 1 0;min-width:0;overflow-x:auto;scrollbar-width:none}
.domain-l1-strip::-webkit-scrollbar{display:none}
.domain-l2-row{display:flex;align-items:center;gap:5px;flex-wrap:wrap;padding:8px 0 4px;border-top:1px solid rgba(122,145,184,0.1);margin-top:8px}
.chip.l2{font-size:12px;padding:3px 9px;background:rgba(43,97,240,0.04);border-color:rgba(43,97,240,0.1);color:#5a7099}
.chip.l2.active{background:rgba(43,97,240,0.12);border-color:rgba(43,97,240,0.3);color:var(--primary);font-weight:600}
.chip.parent-active{border-color:rgba(43,97,240,0.3);color:var(--primary);background:rgba(43,97,240,0.06)}
/* Stats bars */
.stats-bar-list{display:flex;flex-direction:column;gap:8px}
.stats-bar-item{display:grid;grid-template-columns:80px 1fr 28px;align-items:center;gap:6px}
.stats-bar-name{font-size:12px;font-weight:500;color:#3a4d67;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.stats-bar-track{height:6px;border-radius:999px;background:rgba(122,145,184,0.1);overflow:hidden}
.stats-bar-fill{height:100%;border-radius:999px;background:linear-gradient(90deg,#7ab2ff,#2f6bff);transition:width 0.4s ease}
.stats-bar-fill.org{background:linear-gradient(90deg,#4bd19a,#12a87a)}
.stats-bar-count{font-size:11px;font-weight:700;color:#8fa4be;text-align:right}
/* High freq content chips */
.highfreq-tags{display:flex;flex-wrap:wrap;gap:6px 8px}
.highfreq-tag{display:inline-flex;align-items:center;gap:4px;padding:5px 11px;border-radius:999px;border:1px solid rgba(122,145,184,0.14);background:rgba(255,255,255,0.84);font-size:13px;color:#4a6a9a;font-weight:400;box-shadow:0 2px 6px rgba(26,44,82,0.04)}
.highfreq-tag strong{font-size:10px;font-weight:700;padding-left:2px}
"""

anchor_css = '/* @@TOP-NAV-OVERRIDE@@ */'
assert anchor_css in content, "CSS anchor not found"
content = content.replace(anchor_css, new_css + anchor_css, 1)
print("1. CSS inserted OK")

# ===========================================================================
# 2. HTML: Replace domain-card chip-strip with L1+L2 structure
# ===========================================================================
old_domain_card = '''                <div class="domain-card">
                    <div class="panel-heading">
                        <div class="panel-title">
                            <span class="dot"></span>
                            <span>关注领域</span>
                        </div>
                        <div class="chip-strip" id="categoryChips"></div>
                    </div>
                </div>'''

new_domain_card = '''                <div class="domain-card">
                    <div class="panel-heading">
                        <div class="panel-title">
                            <span class="dot"></span>
                            <span>关注领域</span>
                        </div>
                        <div class="domain-l1-strip" id="domainL1Chips"></div>
                    </div>
                    <div class="domain-l2-row" id="domainL2Row" style="display:none"></div>
                </div>'''

assert old_domain_card in content, "domain-card HTML not found"
content = content.replace(old_domain_card, new_domain_card, 1)
print("2. domain-card HTML replaced OK")

# ===========================================================================
# 3. HTML: Add drawer before toast-stack
# ===========================================================================
old_toast = '    <div class="toast-stack" id="toastStack" aria-live="polite"></div>'
new_drawer_toast = '''    <div class="drawer-overlay" id="drawerOverlay"></div>
    <aside class="event-drawer" id="eventDrawer" role="dialog" aria-modal="true" aria-hidden="true">
        <div class="drawer-header">
            <span class="drawer-title-text" id="drawerTitle"></span>
            <button class="drawer-close-btn" id="drawerClose" aria-label="关闭抽屉">\u00d7</button>
        </div>
        <div class="drawer-body" id="drawerBody"></div>
    </aside>
    <div class="toast-stack" id="toastStack" aria-live="polite"></div>'''

assert old_toast in content, "toast-stack HTML not found"
content = content.replace(old_toast, new_drawer_toast, 1)
print("3. Drawer HTML inserted OK")

# ===========================================================================
# 4. JS: Replace recommendationData array + categoryOrder + state + refs + funcs
#    through end of categoryCounts(), keeping formatDate onwards
# ===========================================================================
script_anchor = '    <script>\n        const recommendationData = ['
format_date_anchor = '        function formatDate(dateTime) {'
assert script_anchor in content, "script anchor not found"
assert format_date_anchor in content, "formatDate anchor not found"

script_start = content.index(script_anchor)
format_date_start = content.index(format_date_anchor)

new_data_block = r"""    <script>
        const domainHierarchy = [
            { id: "all", label: "全部", children: [] },
            { id: "hot-topic", label: "热点议题综合", children: ["立选", "地区治理", "社会调查", "政府动态", "八项规定"] },
            { id: "domain-dynamic", label: "领域动态综合", children: ["两岸", "青年", "创科", "法律", "医卫", "网安", "会计", "教育"] },
            { id: "person-dynamic", label: "人物动态综合", children: ["政府官员", "立法会", "人大政协", "知名人士", "区议会"] },
            { id: "hot-general", label: "热点综合", children: ["管制动态", "案件关注", "热点事件", "社评个评", "调查报告", "国安关注", "外部动向"] },
            { id: "institution", label: "机构舆情", children: [] },
            { id: "competitor", label: "竞对动态", children: [] },
            { id: "industry", label: "行业舆情", children: [] },
            { id: "hk-incident", label: "涉港澳突发事件", children: [] }
        ];

        const eventData = [
            {
                id: "e1",
                title: "大埔宏福苑棚架起火事件持续发酵，消防响应与居民安置受关注",
                domainId: "hk-incident", domainLabel: "涉港澳突发事件", domainL2: null,
                riskLevel: "high", riskLabel: "高风险",
                articleCount: 3, platforms: ["Facebook", "新闻资讯", "短视频"],
                score: 96, dateTime: "2026-03-30T14:12:10", read: false, queued: true,
                sentiment: "negative", sentimentLabel: "负面",
                summary: "高层住宅外墙棚架起火并伴随大量黑烟，视频迅速扩散，评论区聚焦消防响应速度与居民转移。",
                analysis: "事件在20分钟内热度抬升接近200%，具备突发性与强烈视觉冲击，极易被二次剪辑传播。建议立即抓取权威通报，结合区域安全主题组织后续跟进。",
                persons: [{ name: "消防处发言人", role: "官方", count: 4 }, { name: "大埔区议员", role: "政界", count: 2 }],
                orgs: [{ name: "香港消防处", type: "政府", count: 6 }, { name: "大埔区议会", type: "政府", count: 2 }, { name: "房屋署", type: "政府", count: 2 }],
                topics: ["棚架安全", "消防响应", "居民安置", "突发事件", "香港灾情"],
                viewpoints: [
                    { text: "消防队到场时间不到5分钟，处置得当，居民有序撤离。", platform: "Facebook", sentiment: "positive" },
                    { text: "旧式住宅楼棚架整改工作长期滞后，此次起火是制度性问题。", platform: "新闻资讯", sentiment: "negative" },
                    { text: "视频画面触目惊心，希望当局彻查棚架安全标准执行情况。", platform: "短视频", sentiment: "negative" }
                ],
                suggestions: ["立即抓取消防处及房屋署权威通报，形成事实核心口径", "组织棚架安全监管专题报道，补充制度背景降低误读空间", "关注受影响居民安置进展，跟踪后续处理结果"],
                timeline: [
                    { time: "03-30 09:15", desc: "多名居民发现外墙棚架起火，第一批视频上传社交平台" },
                    { time: "03-30 09:22", desc: "消防处出动多辆消防车到场扑救，同时疏散楼层居民" },
                    { time: "03-30 09:45", desc: "明火被扑灭，伤亡初步核实为零，消防处发出简短通报" },
                    { time: "03-30 10:10", desc: "二次剪辑视频在短视频平台爆发式传播，热度大幅抬升" },
                    { time: "03-30 11:30", desc: "区议员到场关注，呼吁当局全面检查辖区旧楼棚架安全" },
                    { time: "03-30 14:12", desc: "新闻资讯平台深度稿件发布，聚焦棚架监管制度漏洞" }
                ],
                articles: [
                    { id: 101, title: "大埔宏福苑外墙棚架突发起火，现场视频迅速扩散", platform: "Facebook", sentiment: "negative", sentimentLabel: "负面", dateTime: "2026-03-30T09:22:00" },
                    { id: 102, title: "消防处：大埔棚架火警明火受控，无人受伤", platform: "新闻资讯", sentiment: "neutral", sentimentLabel: "中立", dateTime: "2026-03-30T09:50:00" },
                    { id: 103, title: "【深度】香港旧楼棚架安全监管为何长期滞后", platform: "新闻资讯", sentiment: "negative", sentimentLabel: "负面", dateTime: "2026-03-30T14:12:10" }
                ]
            },
            {
                id: "e2",
                title: "高才通续签门槛收紧传闻扩散，人才政策敏感期舆情明显分化",
                domainId: "hot-topic", domainLabel: "热点议题综合", domainL2: "地区治理",
                riskLevel: "medium", riskLabel: "中风险",
                articleCount: 3, platforms: ["新闻资讯", "微博", "论坛"],
                score: 79, dateTime: "2026-03-30T13:46:00", read: false, queued: false,
                sentiment: "neutral", sentimentLabel: "中立",
                summary: "外媒引述消息称高才通续签门槛或将收紧，资讯账号与论坛围绕人才吸引力、行业准入和区域竞争展开激烈讨论。",
                analysis: "该议题已与人才政策、地区发展预期和公平性讨论耦合，情绪呈现明显分化。建议同步整理政策原文、历次调整口径与专家观点，降低误读空间。",
                persons: [{ name: "劳工及福利局局长", role: "政府官员", count: 3 }, { name: "人力资源专家", role: "专家", count: 2 }],
                orgs: [{ name: "劳工及福利局", type: "政府", count: 5 }, { name: "外媒机构", type: "媒体", count: 3 }, { name: "港专业及资深行政人员协会", type: "行业协会", count: 2 }],
                topics: ["高才通", "人才政策", "续签门槛", "区域竞争", "政策敏感"],
                viewpoints: [
                    { text: "收紧门槛有助提高人才质量，是合理的政策微调。", platform: "新闻资讯", sentiment: "positive" },
                    { text: "政策不稳定信号会打击高端人才赴港意愿，适得其反。", platform: "论坛", sentiment: "negative" },
                    { text: "外媒引述未经证实，当局应尽快澄清消除误解。", platform: "微博", sentiment: "neutral" }
                ],
                suggestions: ["整理高才通政策原文及历次调整记录，提供事实对照", "约访人力资源专家提供中立视角，稳定讨论氛围", "监测外媒后续跟进，防止误读进一步放大"],
                timeline: [
                    { time: "03-30 07:00", desc: "某外媒引述匿名消息发布报道，指高才通续签门槛或将收紧" },
                    { time: "03-30 08:30", desc: "资讯账号二次传播，微博和论坛讨论量快速攀升" },
                    { time: "03-30 10:00", desc: "香港本地媒体开始跟进，局方暂未回应" },
                    { time: "03-30 13:46", desc: "各方讨论呈明显分化，误读风险持续上升" }
                ],
                articles: [
                    { id: 201, title: "外媒引述消息称高才通续签门槛或将收紧，引发高关注争议", platform: "新闻资讯", sentiment: "neutral", sentimentLabel: "中立", dateTime: "2026-03-30T13:46:00" },
                    { id: 202, title: "高才通政策再调整？各方回应不一，业界忧虑人才流失", platform: "论坛", sentiment: "negative", sentimentLabel: "负面", dateTime: "2026-03-30T11:00:00" },
                    { id: 203, title: "港府人才政策连续调整，区域人才竞争格局深度分析", platform: "微博", sentiment: "neutral", sentimentLabel: "中立", dateTime: "2026-03-30T09:20:00" }
                ]
            },
            {
                id: "e3",
                title: "深圳湾口岸\u201c无感通关\u201d传播势能稳定，数据隐私担忧同步浮现",
                domainId: "hot-topic", domainLabel: "热点议题综合", domainL2: "社会调查",
                riskLevel: "medium", riskLabel: "中风险",
                articleCount: 2, platforms: ["微博", "小红书"],
                score: 74, dateTime: "2026-03-30T12:58:00", read: true, queued: false,
                sentiment: "neutral", sentimentLabel: "中立",
                summary: "微博与小红书围绕口岸智能识别、跨境便利化和个人数据授权边界展开激烈互动，观点分化明显。",
                analysis: "该话题兼具技术治理与民生体验双重属性，传播势能稳定且具延展性。建议从政策说明、技术保障和公众感知三个角度构建报道框架。",
                persons: [{ name: "深圳市边检总站发言人", role: "官方", count: 3 }, { name: "数据隐私专家", role: "专家", count: 2 }],
                orgs: [{ name: "深圳边检总站", type: "政府", count: 4 }, { name: "小红书平台", type: "平台", count: 2 }],
                topics: ["无感通关", "数据隐私", "智能识别", "跨境便利", "技术治理"],
                viewpoints: [
                    { text: "无感通关大幅减少排队时间，跨境居民受益明显。", platform: "小红书", sentiment: "positive" },
                    { text: "生物识别数据收集边界不清，公民有权知晓数据如何使用。", platform: "微博", sentiment: "negative" }
                ],
                suggestions: ["从政策文本和技术方案层面厘清数据收集范围与授权机制", "邀请数据隐私专家解读，减少公众不安情绪", "关注后续推广计划，评估舆情走向"],
                timeline: [
                    { time: "03-30 08:00", desc: "官方媒体发布\u201c无感通关\u201d试行方案报道" },
                    { time: "03-30 09:30", desc: "小红书跨境用户分享体验，正面反馈居多" },
                    { time: "03-30 11:00", desc: "微博数据隐私讨论兴起，负面情绪占比上升" },
                    { time: "03-30 12:58", desc: "观点形成明显分化，传播势能持续稳定" }
                ],
                articles: [
                    { id: 301, title: "深圳湾口岸拟试行\u201c无感通关\u201d，数据隐私讨论同步升温", platform: "微博", sentiment: "neutral", sentimentLabel: "中立", dateTime: "2026-03-30T12:58:00" },
                    { id: 302, title: "无感通关体验分享：排队从40分钟缩短至5分钟", platform: "小红书", sentiment: "positive", sentimentLabel: "正面", dateTime: "2026-03-30T10:20:00" }
                ]
            },
            {
                id: "e4",
                title: "海关破获最大宗走私快艇案，黑帮利益链叙事扩散引发治安质疑",
                domainId: "hot-general", domainLabel: "热点综合", domainL2: "案件关注",
                riskLevel: "high", riskLabel: "高风险",
                articleCount: 3, platforms: ["新闻资讯", "Telegram", "短视频"],
                score: 91, dateTime: "2026-03-30T11:44:00", read: false, queued: false,
                sentiment: "negative", sentimentLabel: "负面",
                summary: "案件相关报道在Telegram群组、论坛与短视频平台持续扩散，讨论焦点从案情延伸至跨境灰产与监管漏洞。",
                analysis: "治安议题叠加涉黑叙事后，容易引发对区域安全能力的质疑。建议围绕执法链条、案件背景和制度补洞做结构化拆解，提升信息可信度。",
                persons: [{ name: "香港海关关长", role: "政府官员", count: 4 }, { name: "案件主犯（匿名）", role: "涉案人员", count: 3 }],
                orgs: [{ name: "香港海关", type: "政府", count: 7 }, { name: "跨境走私团伙", type: "犯罪组织", count: 5 }, { name: "警务处", type: "政府", count: 2 }],
                topics: ["走私快艇", "跨境灰产", "黑帮利益链", "监管漏洞", "区域安全"],
                viewpoints: [
                    { text: "此次破案规模史无前例，充分体现了执法部门的专业能力。", platform: "新闻资讯", sentiment: "positive" },
                    { text: "案件背后的利益链条盘根错节，单靠海关难以根绝。", platform: "Telegram", sentiment: "negative" },
                    { text: "走私路线长期存在，监管漏洞亟需从制度层面填补。", platform: "短视频", sentiment: "negative" }
                ],
                suggestions: ["围绕执法链条进行结构化报道，突出制度建设成效", "提示受众核实信息来源，防止夸大性叙事扩散", "关注后续司法进展，跟进主要嫌疑人处理结果"],
                timeline: [
                    { time: "03-30 07:00", desc: "海关发布官方通稿，公布历来最大宗走私快艇案侦破详情" },
                    { time: "03-30 08:00", desc: "新闻资讯平台广泛转载，涉黑叙事开始在Telegram圈子扩散" },
                    { time: "03-30 09:30", desc: "短视频平台二次创作跟进，制造更强视觉冲击" },
                    { time: "03-30 11:44", desc: "讨论焦点从案情转向灰产生态，对监管能力的质疑声音增多" }
                ],
                articles: [
                    { id: 401, title: "海关破获历来最大宗走私快艇案，黑帮利益链词云发酵", platform: "新闻资讯", sentiment: "negative", sentimentLabel: "负面", dateTime: "2026-03-30T11:44:00" },
                    { id: 402, title: "走私快艇案主犯落网：揭秘跨境灰产运作方式", platform: "Telegram", sentiment: "negative", sentimentLabel: "负面", dateTime: "2026-03-30T09:10:00" },
                    { id: 403, title: "百亿货值走私案始末，海关如何布局三年终破获", platform: "短视频", sentiment: "neutral", sentimentLabel: "中立", dateTime: "2026-03-30T10:30:00" }
                ]
            },
            {
                id: "e5",
                title: "机构舆情：杂志社专题策划遭自媒体断章取义，讨论度持续抬升",
                domainId: "institution", domainLabel: "机构舆情", domainL2: null,
                riskLevel: "medium", riskLabel: "中风险",
                articleCount: 2, platforms: ["Threads", "短视频"],
                score: 82, dateTime: "2026-03-30T14:12:10", read: true, queued: false,
                sentiment: "negative", sentimentLabel: "负面",
                summary: "自媒体账号围绕专题文章节选、职场观察和地区就业现状进行再传播，已在青年用户与媒体从业者群体中形成集中讨论。",
                analysis: "系统识别到该话题对机构公信力与选题导向均有影响，存在被断章取义和跨平台放大的可能。建议及时补充事实背景，形成编辑口径，并关注外部媒体跟进转载。",
                persons: [{ name: "杂志社主编（匿名）", role: "媒体人", count: 3 }, { name: "青年就业专家", role: "专家", count: 2 }],
                orgs: [{ name: "目标杂志社", type: "媒体", count: 6 }, { name: "相关自媒体账号", type: "自媒体", count: 4 }],
                topics: ["专题策划", "青年就业", "机构公信力", "断章取义", "跨平台扩散"],
                viewpoints: [
                    { text: "杂志的专题策划触角敏锐，节选虽片面但引发关注有其价值。", platform: "Threads", sentiment: "neutral" },
                    { text: "自媒体断章取义严重扭曲了文章立意，机构应积极澄清。", platform: "短视频", sentiment: "negative" }
                ],
                suggestions: ["及时补充专题文章完整背景，形成编辑官方口径", "联系主要转载自媒体沟通修正传播内容", "关注外部媒体是否跟进转载，防止进一步失真"],
                timeline: [
                    { time: "03-30 10:00", desc: "自媒体账号节选专题文章片段发布，引发初步互动" },
                    { time: "03-30 11:30", desc: "青年用户和媒体从业者群体形成讨论热潮" },
                    { time: "03-30 13:00", desc: "Threads热帖显示断章取义版本传播量超过原文" },
                    { time: "03-30 14:12", desc: "机构尚未作出官方回应，讨论度继续攀升" }
                ],
                articles: [
                    { id: 501, title: "Threads热帖指向杂志社专题策划与青年就业议题，讨论度快速抬升", platform: "Threads", sentiment: "negative", sentimentLabel: "负面", dateTime: "2026-03-30T14:12:10" },
                    { id: 502, title: "媒体内容遭断章取义：自媒体传播生态下机构如何维护公信力", platform: "短视频", sentiment: "negative", sentimentLabel: "负面", dateTime: "2026-03-30T12:30:00" }
                ]
            },
            {
                id: "e6",
                title: "竞对传媒集团成立数字实验室，招聘信号被解读为区域媒体布局升级",
                domainId: "competitor", domainLabel: "竞对动态", domainL2: null,
                riskLevel: "medium", riskLabel: "中风险",
                articleCount: 2, platforms: ["短视频", "LinkedIn"],
                score: 68, dateTime: "2026-03-30T10:22:00", read: false, queued: false,
                sentiment: "neutral", sentimentLabel: "中立",
                summary: "招聘帖显示实验室重点布局短视频主编、数据编辑和行业运营岗位，被视为区域媒体布局升级信号。",
                analysis: "竞争媒体的人才动作容易被外界解读为业务重心调整。建议跟进其公开战略口径，并评估对本地媒体生态与人才流向的影响。",
                persons: [{ name: "传媒集团CEO（匿名）", role: "高管", count: 2 }, { name: "数字实验室负责人（匿名）", role: "高管", count: 2 }],
                orgs: [{ name: "目标传媒集团", type: "媒体", count: 6 }, { name: "南部发展数字实验室", type: "媒体", count: 3 }],
                topics: ["数字实验室", "媒体竞争", "人才布局", "短视频战略", "区域媒体"],
                viewpoints: [
                    { text: "大型传媒集团投入数字化转型，是整个行业的趋势性信号。", platform: "LinkedIn", sentiment: "neutral" },
                    { text: "重金招聘数字岗位，可能对本地媒体人才市场造成抽血效应。", platform: "短视频", sentiment: "negative" }
                ],
                suggestions: ["持续跟进竞对集团公开战略动态和人才引进进展", "评估本地媒体人才流失风险，调整留才策略", "提取竞对数字化布局中的可借鉴经验"],
                timeline: [
                    { time: "03-30 08:00", desc: "竞对集团官方发布\u201c南部发展数字实验室\u201d成立公告" },
                    { time: "03-30 09:00", desc: "招聘信息在行业社群流传，引发同行关注" },
                    { time: "03-30 10:22", desc: "短视频和LinkedIn平台讨论集中，解读为战略升级信号" }
                ],
                articles: [
                    { id: 601, title: "某大型传媒集团成立\u201c南部发展数字实验室\u201d，招聘信息受关注", platform: "短视频", sentiment: "neutral", sentimentLabel: "中立", dateTime: "2026-03-30T10:22:00" },
                    { id: 602, title: "传媒数字化浪潮下的竞争格局：谁在布局南部市场", platform: "LinkedIn", sentiment: "neutral", sentimentLabel: "中立", dateTime: "2026-03-30T09:00:00" }
                ]
            },
            {
                id: "e7",
                title: "区域创科生态综合舆情：科研人才政策与产业协同引发广泛讨论",
                domainId: "domain-dynamic", domainLabel: "领域动态综合", domainL2: "创科",
                riskLevel: "medium", riskLabel: "中风险",
                articleCount: 3, platforms: ["微信", "微博", "新闻资讯"],
                score: 71, dateTime: "2026-03-30T08:30:00", read: false, queued: false,
                sentiment: "neutral", sentimentLabel: "中立",
                summary: "围绕粤港澳大湾区创科政策协同、科研人才待遇和产学研合作模式，各平台持续出现高互动讨论。",
                analysis: "创科议题兼具政策、人才和产业三重属性，正面情绪主导但对执行层面仍存期待。建议关注政策落地细节，结合具体案例深化报道。",
                persons: [{ name: "创科及工业局局长", role: "政府官员", count: 3 }, { name: "大湾区科研专家", role: "专家", count: 2 }],
                orgs: [{ name: "创科及工业局", type: "政府", count: 4 }, { name: "香港科技大学", type: "高校", count: 3 }, { name: "大湾区产业联盟", type: "行业组织", count: 2 }],
                topics: ["创科政策", "科研人才", "大湾区协同", "产学研合作", "产业布局"],
                viewpoints: [
                    { text: "大湾区政策协同为港澳科研提供了前所未有的发展空间。", platform: "微信", sentiment: "positive" },
                    { text: "政策框架已具雏形，执行层面的落地机制有待细化。", platform: "新闻资讯", sentiment: "neutral" },
                    { text: "科研人才薪酬待遇与内地竞争城市相比仍有差距。", platform: "微博", sentiment: "negative" }
                ],
                suggestions: ["跟踪具体政策落地案例，将宏观政策与微观叙事结合", "采访成功落户大湾区的科研人才，增加可读性", "关注产学研对接进展，挖掘具体合作成果"],
                timeline: [
                    { time: "03-29 16:00", desc: "创科及工业局发布最新政策解读，新增科研人才激励措施" },
                    { time: "03-30 07:00", desc: "微信公众号广泛转发，正面情绪主导初期讨论" },
                    { time: "03-30 08:00", desc: "微博出现对执行层面细节的追问和期待声音" },
                    { time: "03-30 08:30", desc: "综合讨论热度趋于稳定，议题延展性强" }
                ],
                articles: [
                    { id: 701, title: "创科及工业局新政解读：大湾区科研协同再升级", platform: "微信", sentiment: "positive", sentimentLabel: "正面", dateTime: "2026-03-30T07:00:00" },
                    { id: 702, title: "从香港科大看大湾区产学研合作模式", platform: "新闻资讯", sentiment: "neutral", sentimentLabel: "中立", dateTime: "2026-03-30T08:00:00" },
                    { id: 703, title: "科研人才薪酬调查：港澳与内地竞争城市差距几何", platform: "微博", sentiment: "negative", sentimentLabel: "负面", dateTime: "2026-03-30T08:30:00" }
                ]
            }
        ];

        const state = {
            domainL1: "all",
            domainL2: null,
            query: "",
            period: "today",
            showInsights: true,
            showAdvanced: false,
            sentimentFilter: "全部"
        };

        const domainL1ChipsNode = document.getElementById("domainL1Chips");
        const domainL2Row = document.getElementById("domainL2Row");
        const contentGrid = document.getElementById("contentGrid");
        const feedNode = document.getElementById("feed");
        const insightsSidebar = document.getElementById("insightsSidebar");
        const insightToggle = document.getElementById("insightToggle");
        const toolbarCaption = document.getElementById("toolbarCaption");
        const searchInput = document.getElementById("searchInput");
        const periodSelect = document.getElementById("periodSelect");
        const filterToggle = document.getElementById("filterToggle");
        const advancedFilters = document.getElementById("advancedFilters");
        const resetButton = document.getElementById("resetButton");
        const toastStack = document.getElementById("toastStack");
        const appShell = document.getElementById("appShell");
        const mobileMask = document.getElementById("mobileMask");
        const drawerOverlay = document.getElementById("drawerOverlay");
        const eventDrawer = document.getElementById("eventDrawer");
        const drawerTitle = document.getElementById("drawerTitle");
        const drawerBody = document.getElementById("drawerBody");
        const drawerClose = document.getElementById("drawerClose");
        const cluePoolAiStorageKey = "zj0330-topic-clue-pool-ai-v1";

        function readJsonStorage(key, fallback = []) {
            try { const raw = window.localStorage.getItem(key); return raw ? JSON.parse(raw) : fallback; }
            catch (e) { return fallback; }
        }
        function writeJsonStorage(key, value) {
            try { window.localStorage.setItem(key, JSON.stringify(value)); return true; }
            catch (e) { return false; }
        }
        function buildClueEntry(ev) {
            return { id: `ai-event-${ev.id}`, sourceId: ev.id, sourceType: "ai-event", originPage: "AI\u667a\u80fd\u63a8\u8350", title: ev.title, summary: ev.summary, analysis: ev.analysis, domain: ev.domainLabel, domainL2: ev.domainL2, riskLevel: ev.riskLevel, riskLabel: ev.riskLabel, dateTime: ev.dateTime, addedAt: new Date().toISOString(), status: "pending", statusLabel: "\u5f85\u6536\u5f55" };
        }
        function loadClueEntries() { return readJsonStorage(cluePoolAiStorageKey, []); }
        function saveClueEntries(entries) { writeJsonStorage(cluePoolAiStorageKey, entries); }
        function syncQueuedFromStorage() {
            const queuedIds = new Set(loadClueEntries().map(e => String(e.sourceId)));
            eventData.forEach(ev => { ev.queued = queuedIds.has(String(ev.id)); });
        }
        function upsertClueEntry(ev) {
            const entry = buildClueEntry(ev);
            const entries = loadClueEntries();
            const idx = entries.findIndex(e => String(e.sourceId) === String(ev.id));
            if (idx >= 0) { entries[idx] = { ...entry, addedAt: entries[idx].addedAt || entry.addedAt, status: entries[idx].status || entry.status, statusLabel: entries[idx].statusLabel || entry.statusLabel }; }
            else { entries.unshift(entry); }
            saveClueEntries(entries);
        }
        function removeClueEntry(evId) { saveClueEntries(loadClueEntries().filter(e => String(e.sourceId) !== String(evId))); }

        function inSelectedPeriod(item) {
            if (state.period === "all") return true;
            const diffHours = (new Date("2026-03-30T18:00:00") - new Date(item.dateTime)) / 36e5;
            if (state.period === "today") return diffHours <= 24;
            if (state.period === "48h") return diffHours <= 48;
            return diffHours <= 168;
        }
        function matchesSearch(ev) {
            const query = state.query.trim().toLowerCase();
            if (!query) return true;
            const src = [ev.title, ev.summary, ev.analysis, ev.domainLabel, ev.domainL2 || "", (ev.topics || []).join(" "), ev.platforms.join(" ")].join(" ").toLowerCase();
            return src.includes(query);
        }
        function matchesAdvanced(ev) {
            if (state.sentimentFilter !== "\u5168\u90e8" && ev.sentimentLabel !== state.sentimentFilter) return false;
            return true;
        }
        function baseFilteredEvents() {
            return eventData.filter(ev => inSelectedPeriod(ev) && matchesSearch(ev) && matchesAdvanced(ev));
        }
        function visibleEvents() {
            const base = baseFilteredEvents();
            if (state.domainL1 === "all") return base;
            return base.filter(ev => {
                if (ev.domainId !== state.domainL1) return false;
                if (state.domainL2 && ev.domainL2 !== state.domainL2) return false;
                return true;
            });
        }
        function domainCounts() {
            const base = baseFilteredEvents();
            const counts = { all: base.length };
            domainHierarchy.forEach(d => { if (d.id !== "all") counts[d.id] = 0; });
            base.forEach(ev => { if (counts[ev.domainId] !== undefined) counts[ev.domainId]++; });
            return counts;
        }

"""

content = content[:script_start] + new_data_block + content[format_date_start:]
print("4. Data/state/refs/filter funcs replaced OK")

# ===========================================================================
# 5. Replace renderCategories() with renderDomains()
# ===========================================================================
rc_start = content.index('        function renderCategories() {')
# Find end: next function definition
bt_start = content.index('        function buildTrendChart(items) {')
old_render_cats = content[rc_start:bt_start]

new_render_domains = """        function renderDomains() {
            const counts = domainCounts();
            domainL1ChipsNode.innerHTML = domainHierarchy.map(d => {
                const isActive = state.domainL1 === d.id;
                const isParentActive = isActive && state.domainL2;
                return `<button class="chip ${isActive ? (isParentActive ? "parent-active" : "active") : ""}" type="button" data-l1="${d.id}">
                    <span>${d.label}</span><span class="chip-count">${counts[d.id] !== undefined ? counts[d.id] : ""}</span>
                </button>`;
            }).join("");
            const activeDomain = domainHierarchy.find(d => d.id === state.domainL1);
            if (activeDomain && activeDomain.children.length > 0) {
                domainL2Row.style.display = "flex";
                const opts = [{ label: "全部子级", value: null }, ...activeDomain.children.map(c => ({ label: c, value: c }))];
                domainL2Row.innerHTML = opts.map(c => `
                    <button class="chip l2 ${state.domainL2 === c.value ? "active" : ""}" type="button" data-l2="${c.value || ""}">
                        <span>${c.label}</span>
                    </button>`).join("");
            } else {
                domainL2Row.style.display = "none";
                domainL2Row.innerHTML = "";
            }
        }

"""
content = content[:rc_start] + new_render_domains + content[bt_start:]
print("5. renderDomains() replaced OK")

# ===========================================================================
# 6. Replace buildSentimentChart + buildWordCloud with new stat functions
# ===========================================================================
bsc_start = content.index('        function buildSentimentChart(items) {')
ri_start = content.index('        function renderInsights(items) {')
old_charts = content[bsc_start:ri_start]

new_stat_funcs = """        function buildPersonStats(events) {
            const personMap = new Map();
            events.forEach(ev => { (ev.persons || []).forEach(p => { if (!personMap.has(p.name)) personMap.set(p.name, { role: p.role, count: 0 }); personMap.get(p.name).count += p.count; }); });
            const persons = [...personMap.entries()].sort((a, b) => b[1].count - a[1].count).slice(0, 8);
            if (!persons.length) return `<div class="insight-empty">\u6682\u65e0\u4eba\u7269\u7edf\u8ba1\u6570\u636e\u3002</div>`;
            const max = persons[0][1].count;
            return `<div class="stats-bar-list">${persons.map(([name, info]) => `
                <div class="stats-bar-item">
                    <div class="stats-bar-name" title="${name}">${name}</div>
                    <div class="stats-bar-track"><div class="stats-bar-fill" style="width:${(info.count / max * 100).toFixed(0)}%"></div></div>
                    <div class="stats-bar-count">${info.count}</div>
                </div>`).join("")}</div>`;
        }

        function buildOrgStats(events) {
            const orgMap = new Map();
            events.forEach(ev => { (ev.orgs || []).forEach(o => { if (!orgMap.has(o.name)) orgMap.set(o.name, { type: o.type, count: 0 }); orgMap.get(o.name).count += o.count; }); });
            const orgs = [...orgMap.entries()].sort((a, b) => b[1].count - a[1].count).slice(0, 8);
            if (!orgs.length) return `<div class="insight-empty">\u6682\u65e0\u673a\u6784\u7edf\u8ba1\u6570\u636e\u3002</div>`;
            const max = orgs[0][1].count;
            return `<div class="stats-bar-list">${orgs.map(([name, info]) => `
                <div class="stats-bar-item">
                    <div class="stats-bar-name" title="${name}">${name}</div>
                    <div class="stats-bar-track"><div class="stats-bar-fill org" style="width:${(info.count / max * 100).toFixed(0)}%"></div></div>
                    <div class="stats-bar-count">${info.count}</div>
                </div>`).join("")}</div>`;
        }

        function buildHighFreqContent(events) {
            const topicMap = new Map();
            events.forEach(ev => { (ev.topics || []).forEach(t => { topicMap.set(t, (topicMap.get(t) || 0) + 1); }); });
            const topics = [...topicMap.entries()].sort((a, b) => b[1] - a[1]).slice(0, 16);
            if (!topics.length) return `<div class="insight-empty">\u6682\u65e0\u9ad8\u9891\u5173\u8054\u5185\u5bb9\u3002</div>`;
            const palette = ["#2f6bff", "#22b5c8", "#4b7abb", "#12a87a", "#e0870a", "#7c4dff", "#e04040", "#4289d8"];
            return `<div class="highfreq-tags">${topics.map(([topic, cnt], i) => `
                <span class="highfreq-tag" style="color:${palette[i % palette.length]};border-color:${palette[i % palette.length]}33;">${topic}<strong>${cnt}</strong></span>`).join("")}</div>`;
        }

"""
content = content[:bsc_start] + new_stat_funcs + content[ri_start:]
print("6. Stat functions replaced OK")

# ===========================================================================
# 7. Replace renderInsights()
# ===========================================================================
ri_start2 = content.index('        function renderInsights(items) {')
rf_start = content.index('        function renderFeed(items) {')
old_ri = content[ri_start2:rf_start]

new_ri = """        function renderInsights(events) {
            const total = events.length;
            const unreadCount = events.filter(ev => !ev.read).length;
            const queuedCount = events.filter(ev => ev.queued).length;
            const latestItem = total ? [...events].sort((a, b) => new Date(b.dateTime) - new Date(a.dateTime))[0] : null;
            insightsSidebar.innerHTML = `
                <section class="insight-card">
                    <div class="insight-card-header">
                        <div class="insight-card-title"><strong>\u6570\u636e\u6982\u89c8</strong></div>
                        <span class="insight-card-meta">${latestItem ? `\u66f4\u65b0\u81f3 ${formatShortTime(latestItem.dateTime).full}` : "\u6682\u65e0\u66f4\u65b0"}</span>
                    </div>
                    <div class="insight-summary-grid">
                        <div class="summary-item"><span>\u4e8b\u4ef6\u603b\u91cf</span><strong>${total}</strong></div>
                        <div class="summary-item"><span>\u672a\u8bfb\u4e8b\u4ef6</span><strong>${unreadCount}</strong></div>
                        <div class="summary-item"><span>\u7ebf\u7d22\u6c60</span><strong>${queuedCount}</strong></div>
                    </div>
                </section>
                <section class="insight-card">
                    <div class="insight-card-header">
                        <div class="insight-card-title"><strong>\u70ed\u5ea6\u8d8b\u52bf</strong></div>
                        <span class="insight-card-meta">\u5cf0\u503c ${total ? Math.max(...events.map(ev => ev.score)) : 0}</span>
                    </div>
                    ${buildTrendChart(events)}
                </section>
                <section class="insight-card">
                    <div class="insight-card-header">
                        <div class="insight-card-title"><strong>\u4eba\u7269\u7edf\u8ba1</strong></div>
                        <span class="insight-card-meta">\u6309\u51fa\u73b0\u9891\u6b21\u6392\u5e8f</span>
                    </div>
                    ${buildPersonStats(events)}
                </section>
                <section class="insight-card">
                    <div class="insight-card-header">
                        <div class="insight-card-title"><strong>\u673a\u6784\u7edf\u8ba1</strong></div>
                        <span class="insight-card-meta">\u6309\u51fa\u73b0\u9891\u6b21\u6392\u5e8f</span>
                    </div>
                    ${buildOrgStats(events)}
                </section>
                <section class="insight-card">
                    <div class="insight-card-header">
                        <div class="insight-card-title"><strong>\u9ad8\u9891\u5173\u8054\u5185\u5bb9</strong></div>
                        <span class="insight-card-meta">\u8de8\u4e8b\u4ef6\u8bae\u9898\u805a\u5408</span>
                    </div>
                    ${buildHighFreqContent(events)}
                </section>
            `;
        }

"""
content = content[:ri_start2] + new_ri + content[rf_start:]
print("7. renderInsights() replaced OK")

# ===========================================================================
# 8. Replace renderFeed() with renderEvents()
# ===========================================================================
rf_start2 = content.index('        function renderFeed(items) {')
render_start = content.index('        function render() {')
old_rf = content[rf_start2:render_start]

new_re = """        function renderEvents(events) {
            toolbarCaption.textContent = `\u4e8b\u4ef6\u63a8\u8350 \u00b7 \u5f53\u524d\u663e\u793a ${events.length} \u4e2a\u4e8b\u4ef6`;
            if (!events.length) {
                feedNode.innerHTML = `<div class="empty-state"><strong>\u6682\u65e0\u5339\u914d\u4e8b\u4ef6</strong><span>\u53ef\u4ee5\u5c1d\u8bd5\u653e\u5bbd\u65f6\u95f4\u8303\u56f4\u3001\u53d6\u6d88\u7b5b\u9009\uff0c\u6216\u66f4\u6362\u5173\u952e\u8bcd\u7ee7\u7eed\u68c0\u7d22\u3002</span></div>`;
                return;
            }
            feedNode.innerHTML = events.map((ev, idx) => `
                <article class="event-card" data-id="${ev.id}" data-read="${ev.read}" style="animation-delay:${idx * 0.05}s">
                    <div style="display:flex;align-items:flex-start;gap:10px">
                        <input type="checkbox" class="feed-checkbox" data-id="${ev.id}" style="margin-top:20px;flex-shrink:0;width:15px;height:15px;accent-color:var(--primary);cursor:pointer">
                        <div style="flex:1 1 auto;min-width:0">
                            <div class="event-tag-row">
                                <span class="tag domain"><span class="tag-dot"></span>${ev.domainLabel}</span>
                                ${ev.domainL2 ? `<span class="tag platform">${ev.domainL2}</span>` : ""}
                                <span class="tag risk-${ev.riskLevel}">${ev.riskLabel}</span>
                                ${ev.queued ? `<span class="status-stamp">\u5df2\u52a0\u5165\u7ebf\u7d22\u6c60</span>` : ""}
                            </div>
                            <button class="event-title-btn" type="button" data-action="open-drawer" data-id="${ev.id}">
                                <h2 class="event-title">${ev.title}</h2>
                            </button>
                            <div class="ai-panel" style="margin:0 0 10px"><span class="ai-indicator"></span><span class="ai-label">AI \u7814\u5224</span><span class="ai-body">${ev.summary}</span></div>
                            <div class="event-meta-row">
                                <span class="event-source-count">\u805a\u5408 ${ev.articleCount} \u6761\u4fe1\u606f</span>
                                <span class="event-meta-item">${ev.platforms.join(" \u00b7 ")}</span>
                                <span class="feed-time">${formatDate(ev.dateTime)}</span>
                                <div style="margin-left:auto;display:flex;gap:2px">
                                    <button class="card-action-btn" type="button" data-action="toggle-read" data-id="${ev.id}" title="${ev.read ? "\u6807\u8bb0\u672a\u8bfb" : "\u6807\u8bb0\u5df2\u8bfb"}">\u25cf</button>
                                    <button class="card-action-btn" type="button" data-action="collect" data-id="${ev.id}" title="\u6536\u85cf">\u2605</button>
                                    <button class="card-action-btn" type="button" data-action="toggle-queue" data-id="${ev.id}" title="${ev.queued ? "\u79fb\u51fa\u7ebf\u7d22\u6c60" : "\u52a0\u5165\u7ebf\u7d22\u6c60"}">\uff0b</button>
                                </div>
                            </div>
                        </div>
                    </div>
                </article>
            `).join("");
        }

"""
content = content[:rf_start2] + new_re + content[render_start:]
print("8. renderEvents() replaced OK")

# ===========================================================================
# 9. Replace render() + all event handlers through </script>
# ===========================================================================
render_start2 = content.index('        function render() {')
script_end = content.index('\n</script>')
old_render_handlers = content[render_start2:script_end]

new_render_handlers = r"""        function render() {
            const events = visibleEvents();
            renderDomains();
            renderEvents(events);
            if (state.showInsights) renderInsights(events);
            contentGrid.classList.toggle("insights-hidden", !state.showInsights);
            insightsSidebar.hidden = !state.showInsights;
            insightToggle.classList.toggle("active", state.showInsights);
            insightToggle.setAttribute("aria-pressed", String(state.showInsights));
            advancedFilters.classList.toggle("open", state.showAdvanced);
            filterToggle.classList.toggle("active", state.showAdvanced);
        }

        function showToast(message) {
            const toast = document.createElement("div");
            toast.className = "toast";
            toast.textContent = message;
            toastStack.appendChild(toast);
            setTimeout(() => { toast.style.opacity = "0"; toast.style.transform = "translateY(8px)"; toast.style.transition = "opacity 0.2s ease, transform 0.2s ease"; }, 2200);
            setTimeout(() => toast.remove(), 2500);
        }

        function findEvent(id) { return eventData.find(ev => String(ev.id) === String(id)); }

        function openDrawer(evId) {
            const ev = findEvent(evId);
            if (!ev) return;
            drawerTitle.textContent = ev.title;
            const maxP = ev.persons && ev.persons.length ? ev.persons[0].count : 1;
            const maxO = ev.orgs && ev.orgs.length ? ev.orgs[0].count : 1;
            drawerBody.innerHTML = `
                <div class="drawer-section">
                    <div class="drawer-section-title">AI \u7efc\u5408\u7814\u5224</div>
                    <div class="drawer-risk-bar">
                        <span class="tag risk-${ev.riskLevel}">${ev.riskLabel}</span>
                        <span class="tag sentiment-${ev.sentiment}">${ev.sentimentLabel}</span>
                        <span style="font-size:12px;color:#7a8ea8;margin-left:4px">\u805a\u5408 ${ev.articleCount} \u6761 \u00b7 ${ev.platforms.join("\u3001")}</span>
                    </div>
                    <div class="drawer-ai-summary">${ev.analysis}</div>
                    <div class="drawer-tag-row">${(ev.topics || []).map(t => `<span class="drawer-tag">${t}</span>`).join("")}</div>
                </div>
                <div class="drawer-section">
                    <div class="drawer-section-title">\u4f20\u64ad\u70ed\u5ea6\u8d70\u52bf</div>
                    ${buildTrendChart([ev])}
                </div>
                <div class="drawer-section">
                    <div class="drawer-section-title">\u4e8b\u4ef6\u8109\u7edc</div>
                    <ul class="timeline-list">
                        ${(ev.timeline || []).map(t => `
                            <li class="timeline-item">
                                <div class="timeline-time">${t.time}</div>
                                <div class="timeline-desc">${t.desc}</div>
                            </li>`).join("")}
                    </ul>
                </div>
                <div class="drawer-section">
                    <div class="drawer-section-title">\u5173\u952e\u5b9e\u4f53\u8bc6\u522b</div>
                    <div style="margin-bottom:10px">
                        <div style="font-size:12px;font-weight:700;color:#5a7099;margin-bottom:6px">\u4eba\u7269</div>
                        <div class="stats-bar-list">${(ev.persons || []).slice(0, 5).map(p => `
                            <div class="stats-bar-item">
                                <div class="stats-bar-name" title="${p.name}">${p.name}</div>
                                <div class="stats-bar-track"><div class="stats-bar-fill" style="width:${(p.count / maxP * 100).toFixed(0)}%"></div></div>
                                <div class="stats-bar-count">${p.count}</div>
                            </div>`).join("")}</div>
                    </div>
                    <div>
                        <div style="font-size:12px;font-weight:700;color:#5a7099;margin-bottom:6px">\u673a\u6784</div>
                        <div class="stats-bar-list">${(ev.orgs || []).slice(0, 5).map(o => `
                            <div class="stats-bar-item">
                                <div class="stats-bar-name" title="${o.name}">${o.name}</div>
                                <div class="stats-bar-track"><div class="stats-bar-fill org" style="width:${(o.count / maxO * 100).toFixed(0)}%"></div></div>
                                <div class="stats-bar-count">${o.count}</div>
                            </div>`).join("")}</div>
                    </div>
                </div>
                <div class="drawer-section">
                    <div class="drawer-section-title">\u6838\u5fc3\u89c2\u70b9\u805a\u5408</div>
                    ${(ev.viewpoints || []).map(v => `
                        <div class="drawer-viewpoint-item">
                            <div class="drawer-viewpoint-platform">${v.platform}</div>
                            <div class="drawer-viewpoint-text">${v.text}</div>
                            <span class="drawer-viewpoint-sentiment ${v.sentiment}">${v.sentiment === "positive" ? "\u6b63\u9762" : v.sentiment === "negative" ? "\u8d1f\u9762" : "\u4e2d\u7acb"}</span>
                        </div>`).join("")}
                </div>
                <div class="drawer-section">
                    <div class="drawer-section-title">\u5904\u7f6e\u5efa\u8bae</div>
                    ${(ev.suggestions || []).map((s, i) => `
                        <div class="drawer-suggestion-item">
                            <div class="drawer-suggestion-num">${i + 1}</div>
                            <div>${s}</div>
                        </div>`).join("")}
                </div>
                <div class="drawer-section">
                    <div class="drawer-section-title">\u5173\u8054\u4fe1\u606f\uff08${ev.articleCount} \u6761\uff09</div>
                    ${(ev.articles || []).map(a => `
                        <div class="drawer-article-item">
                            <div style="flex:1 1 auto;min-width:0">
                                <div class="drawer-article-title">${a.title}</div>
                                <div class="drawer-article-meta">
                                    <span>${a.platform}</span>
                                    <span>\u00b7</span>
                                    <span class="tag sentiment-${a.sentiment}" style="font-size:10px;padding:0 5px">${a.sentimentLabel}</span>
                                    <span>\u00b7</span>
                                    <span>${formatDate(a.dateTime)}</span>
                                </div>
                            </div>
                            <button class="card-action-btn" type="button" title="\u67e5\u770b\u539f\u6587">\u2197</button>
                        </div>`).join("")}
                </div>
            `;
            drawerOverlay.classList.add("open");
            eventDrawer.classList.add("open");
            eventDrawer.setAttribute("aria-hidden", "false");
            document.body.style.overflow = "hidden";
        }

        function closeDrawer() {
            drawerOverlay.classList.remove("open");
            eventDrawer.classList.remove("open");
            eventDrawer.setAttribute("aria-hidden", "true");
            document.body.style.overflow = "";
        }

        drawerClose.addEventListener("click", closeDrawer);
        drawerOverlay.addEventListener("click", closeDrawer);
        document.addEventListener("keydown", e => { if (e.key === "Escape") closeDrawer(); });

        domainL1ChipsNode.addEventListener("click", e => {
            const chip = e.target.closest(".chip[data-l1]");
            if (!chip) return;
            state.domainL1 = chip.dataset.l1;
            state.domainL2 = null;
            render();
        });

        domainL2Row.addEventListener("click", e => {
            const chip = e.target.closest(".chip[data-l2]");
            if (!chip) return;
            state.domainL2 = chip.dataset.l2 || null;
            render();
        });

        searchInput.addEventListener("input", e => { state.query = e.target.value; render(); });
        periodSelect.addEventListener("change", e => { state.period = e.target.value; render(); });
        filterToggle.addEventListener("click", () => { state.showAdvanced = !state.showAdvanced; render(); });
        insightToggle.addEventListener("click", () => { state.showInsights = !state.showInsights; render(); });

        document.querySelectorAll("input[name='sentimentFilter']").forEach(r => {
            r.addEventListener("change", e => { state.sentimentFilter = e.target.value; render(); });
        });

        resetButton.addEventListener("click", () => {
            state.domainL1 = "all"; state.domainL2 = null; state.query = "";
            state.period = "today"; state.showAdvanced = false; state.sentimentFilter = "\u5168\u90e8";
            searchInput.value = ""; periodSelect.value = "today";
            document.querySelector("input[name='sentimentFilter'][value='\u5168\u90e8']").checked = true;
            render();
            showToast("\u7b5b\u9009\u6761\u4ef6\u5df2\u91cd\u7f6e");
        });

        feedNode.addEventListener("click", e => {
            const btn = e.target.closest("[data-action]");
            if (!btn) return;
            const { action, id } = btn.dataset;
            const ev = findEvent(id);
            if (!ev) return;
            if (action === "open-drawer") { openDrawer(id); return; }
            if (action === "toggle-read") {
                ev.read = !ev.read;
                render();
                showToast(ev.read ? "\u5df2\u6807\u8bb0\u4e3a\u5df2\u8bfb" : "\u5df2\u6062\u590d\u4e3a\u672a\u8bfb");
                return;
            }
            if (action === "toggle-queue") {
                ev.queued = !ev.queued;
                if (ev.queued) upsertClueEntry(ev); else removeClueEntry(ev.id);
                render();
                showToast(ev.queued ? "\u5df2\u52a0\u5165\u7ebf\u7d22\u6c60\uff0c\u53ef\u5728\u9009\u9898\u7ebf\u7d22\u6c60\u67e5\u770b" : "\u5df2\u79fb\u51fa\u7ebf\u7d22\u6c60");
                return;
            }
            if (action === "collect") { showToast("\u5df2\u52a0\u5165\u4e2a\u4eba\u6536\u85cf"); return; }
        });

        mobileMask.addEventListener("click", () => document.body.classList.remove("is-sidebar-open"));

        appShell.addEventListener("click", e => {
            if (e.target.closest("a.nav-item[href]")) {
                if (window.innerWidth <= 1080) document.body.classList.remove("is-sidebar-open");
                return;
            }
            if (e.target.closest(".nav-item")) {
                showToast("\u5f53\u524d\u9636\u6bb5\u4ec5\u751f\u6210\u667a\u80fd\u63a8\u8350\u9875\uff0c\u5176\u4f59\u6a21\u5757\u53ef\u6309\u540c\u4e00\u98ce\u683c\u7ee7\u7eed\u6269\u5c55");
                if (window.innerWidth <= 1080) document.body.classList.remove("is-sidebar-open");
            }
        });

        window.addEventListener("storage", e => { if (e.key === cluePoolAiStorageKey) { syncQueuedFromStorage(); render(); } });

        (function initNavCollapse() {
            document.querySelectorAll(".nav-group-title").forEach(title => {
                title.addEventListener("click", function () { this.closest(".nav-group").classList.toggle("collapsed"); });
            });
        })();

        const selectAllCheckbox = document.getElementById("selectAll");
        if (selectAllCheckbox) {
            selectAllCheckbox.addEventListener("change", () => {
                document.querySelectorAll(".feed-checkbox").forEach(cb => { cb.checked = selectAllCheckbox.checked; });
            });
            feedNode.addEventListener("change", e => {
                if (e.target.classList.contains("feed-checkbox")) {
                    const all = document.querySelectorAll(".feed-checkbox");
                    const checked = document.querySelectorAll(".feed-checkbox:checked");
                    selectAllCheckbox.indeterminate = checked.length > 0 && checked.length < all.length;
                    selectAllCheckbox.checked = checked.length === all.length;
                }
            });
        }

        function openAIForRecommend() {
            const sel = Array.from(document.querySelectorAll(".event-title")).map(t => t.textContent.trim()).slice(0, 6);
            window.aiAssistantOpenWithData(sel);
        }

        function toggleGroup(el) { var g = el.closest(".nav-group"); if (g) g.classList.toggle("collapsed"); }

        syncQueuedFromStorage();
        render();
"""
content = content[:render_start2] + new_render_handlers + '\n' + content[script_end:]
print("9. render() + handlers replaced OK")

with open(r'c:\Pros\ZJ0512\监测预警\AI智能推荐\index.html', 'w', encoding='utf-8') as f:
    f.write(content)

new_len = len(content)
print(f"\nDone! Original: {orig_len} chars, New: {new_len} chars, Delta: +{new_len - orig_len}")
print("Lines:", content.count('\n'))
