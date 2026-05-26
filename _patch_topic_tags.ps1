$file = "c:\Pros\ZJ0521\监测预警\热点榜单\index.html"
$enc  = [Text.Encoding]::UTF8
$c    = [IO.File]::ReadAllText($file, $enc)

# ── 1. 注入 CSS ──────────────────────────────────────────────
if (-not $c.Contains('/* topic-tags */')) {
$css = @"
/* topic-tags */
.tt{display:inline-flex;align-items:center;padding:0 5px;border-radius:3px;font-size:9px;font-weight:700;white-space:nowrap;flex-shrink:0;line-height:16px;margin-left:2px;vertical-align:middle}
.tt-社会民生{background:rgba(99,102,241,.10);color:#4848b8;border:1px solid rgba(99,102,241,.22)}
.tt-政务政策{background:rgba(220,38,38,.09);color:#b01a1a;border:1px solid rgba(220,38,38,.20)}
.tt-国际新闻{background:rgba(8,145,178,.09);color:#056890;border:1px solid rgba(8,145,178,.22)}
.tt-财经商业{background:rgba(5,150,105,.09);color:#066845;border:1px solid rgba(5,150,105,.22)}
.tt-医疗卫生{background:rgba(2,132,199,.09);color:#055890;border:1px solid rgba(2,132,199,.22)}
.tt-教育就业{background:rgba(124,58,237,.09);color:#5018a8;border:1px solid rgba(124,58,237,.22)}
.tt-旅游出行{background:rgba(217,119,6,.09);color:#885000;border:1px solid rgba(217,119,6,.22)}
.tt-文化艺术{background:rgba(219,39,119,.09);color:#981058;border:1px solid rgba(219,39,119,.22)}
.tt-国际{background:rgba(100,116,139,.09);color:#3a4858;border:1px solid rgba(100,116,139,.22)}
.tt-香港{background:rgba(43,97,240,.09);color:#1535a0;border:1px solid rgba(43,97,240,.22)}
.tt-大陆{background:rgba(224,64,64,.09);color:#981818;border:1px solid rgba(224,64,64,.22)}
.tt-澳门{background:rgba(18,168,122,.09);color:#085840;border:1px solid rgba(18,168,122,.22)}
.tt-离岛区,.tt-中西区,.tt-东区,.tt-南区,.tt-湾仔区,.tt-九龙城区,.tt-观塘区,.tt-深水埗区,.tt-黄大仙区,.tt-油尖旺区,.tt-葵青区,.tt-北区,.tt-西贡区,.tt-沙田区,.tt-大埔区,.tt-荃湾区,.tt-屯门区,.tt-元朗区{background:rgba(43,97,240,.07);color:#0f2888;border:1px solid rgba(43,97,240,.18)}
"@
    $c = $c.Replace('</style>', $css + "`n</style>")
}

# ── 2. 打标签辅助函数 ──────────────────────────────────────────
function T($dm, $ar) {
    return "<span class=`"tt tt-$dm`">$dm</span><span class=`"tt tt-$ar`">$ar</span>"
}
function Patch($title, $dm, $ar) {
    $old = "$title</div>"
    $new = "$title</div>$(T $dm $ar)"
    return $old, $new
}

$pairs = @(
    # ── 内地总榜 ──
    (Patch '十四届全国人大四次会议议程公布'     '政务政策' '大陆'),
    (Patch '代表建议设定3000亿元高速免费额度'   '政务政策' '大陆'),
    (Patch '12306回应乘客在普速铁路上用排插'    '社会民生' '大陆'),
    (Patch '2026全国两会为什么格外重要'         '政务政策' '大陆'),
    (Patch '驻日大使馆提醒：防范日本「撞人族」' '国际新闻' '国际'),
    (Patch '雷军2026两会议题引发广泛关注'       '政务政策' '大陆'),
    (Patch '北京今日迎来今年第一场大雪'         '社会民生' '大陆'),
    (Patch '山东修高铁站挖出5亿年前化石石海'    '社会民生' '大陆'),
    (Patch '政协委员建议高中纳入义务教育'       '教育就业' '大陆'),
    (Patch '代表委员议建立提案落地落实机制'     '政务政策' '大陆'),
    # ── 香港热榜 ──
    (Patch '港铁票价调整方案今日正式公布'                   '社会民生' '香港'),
    (Patch '《基本法》第23条立法公众咨询结果出炉'           '政务政策' '香港'),
    (Patch '新冠变异株JN.1感染个案增加 呼吁接种疫苗'        '医疗卫生' '香港'),
    (Patch '香港迪士尼「魔雪奇缘」新园区盛大开幕'           '文化艺术' '离岛区'),
    (Patch '季节性流感踏入高峰期公立医院病房爆满'           '医疗卫生' '香港'),
    (Patch 'LIHKG热议：伊朗小学遭轰炸管局公开'             '国际新闻' '国际'),
    (Patch '跨境学童全面恢复面授课堂'                       '教育就业' '香港'),
    (Patch '驻外经贸办积极斡纠对香港不实报道'               '政务政策' '香港'),
    (Patch 'DSE中学文凭试今日放榜 多名状元出炉'             '教育就业' '香港'),
    (Patch '巴塞尔艺术展(Art Basel)香港展会盛大开幕'        '文化艺术' '香港'),
    # ── 香港异见榜 ──
    (Patch '《苹果日报》数字复刊计划曝光 拟于海外正式发布'  '社会民生' '国际'),
    (Patch '多国政府联署谴责香港新闻自由持续恶化'           '国际新闻' '国际'),
    (Patch '前立法会议员被捕 国际特赦组织发紧急声明'        '政务政策' '香港'),
    (Patch '流亡民主派联合发表声明 呼吁国际制裁官员'        '国际新闻' '国际'),
    (Patch '美国国会通过决议要求追责《国安法》执行者'       '政务政策' '国际'),
    (Patch '英国法院裁定延长香港异见人士庇护权'             '政务政策' '国际'),
    (Patch '驻港外国记者协会报告：新闻自由急剧倒退'         '社会民生' '香港'),
    (Patch '海外港人就《基本法》廿三条立法发起请愿活动'     '政务政策' '国际'),
    (Patch '国际人权组织揭发在囚民主派人士遭虐待指控'       '国际新闻' '国际'),
    (Patch '流亡港人在英国筹办「香港之声」论坛引关注'       '社会民生' '国际'),
    # ── LIHKG 连登 ──
    (Patch '伊朗小学遭轰炸逾百死 当局公开美军戡界行动'      '国际新闻' '国际'),
    (Patch '荣枯死亡 nba 有缘友拾83分超越Kobe'              '文化艺术' '国际'),
    (Patch '大家辜负 低物感但早d退休'                       '社会民生' '香港'),
    (Patch 'MacBook Neo开箱评测｜厚实外型＋A18 Pro芯片'      '财经商业' '国际'),
    (Patch '热制ion9 能够到指境 建造大家起返来拍'            '财经商业' '香港'),
    (Patch '由天道酬勤，到FIRE movement，再到及时行乐'       '社会民生' '香港'),
    (Patch '本港新能源车注册数量持续攀升'                   '财经商业' '香港'),
    (Patch '全港跑步比赛2026年度赛程公布'                   '社会民生' '香港'),
    (Patch '政府就最低工资水平展开新一轮咨询'               '政务政策' '香港'),
    (Patch '电费调整计划引发市民广泛讨论'                   '社会民生' '香港'),
    # ── 香港高登 ──
    (Patch '美国比人升左希莫德旺大事重点斩行人理？'          '国际新闻' '国际'),
    (Patch '2026年3月 足球女将 Season 2（2）'               '文化艺术' '香港'),
    (Patch '泻桥直播正式做香港人 下月全港香港身份证'         '社会民生' '香港'),
    (Patch '【美国实】疑幽暗人FIVE GUYS好吃好吃?'            '文化艺术' '国际'),
    (Patch '成日都做盘算日经结有同理行人理？T'               '财经商业' '香港'),
    (Patch '刘美：看着谷爱凌的人「很虚伪」'                 '文化艺术' '国际'),
    (Patch '本港失业率维持低位 就业市场稳定'                '教育就业' '香港'),
    (Patch '港大研究：本港青年置业意愿持续下降'             '社会民生' '香港'),
    (Patch '新界东北发展区首批居民开始迁入'                 '社会民生' '北区'),
    (Patch '政府拟扩大夜间经济措施至更多地区'               '财经商业' '香港'),
    # ── 香港01 ──
    (Patch '尖沙咀人气烘焙店GUILT FREE开业两月宣告关停'      '财经商业' '油尖旺区'),
    (Patch '中西局势脱缰 油价受压升学指数迎20亿增长'         '财经商业' '国际'),
    (Patch '油债｜跨境审查加码浪组引发借贷争议'              '财经商业' '香港'),
    (Patch '紫菊蓝｜美军引以为傲的技术优势如何引发深层震动'  '国际新闻' '国际'),
    (Patch '国泰航空：向员工放假相当于每人逾11星期薪金补偿'  '财经商业' '香港'),
    (Patch 'DSE英文口试：两次应考均闯关的同学分享心得'       '教育就业' '香港'),
    (Patch '渔护署指今年候鸟迁徙数量创新高'                 '社会民生' '香港'),
    (Patch '葵涌货柜码头自动化改造进入新阶段'               '财经商业' '葵青区'),
    (Patch '食物安全中心发现进口食品含违禁添加剂'           '医疗卫生' '香港'),
    (Patch '港府宣布延长防疫隔离政策检讨期限'               '政务政策' '香港'),
    # ── 雅虎新闻 ──
    (Patch '能源搭棚翻 泛滥副成灾'                          '财经商业' '香港'),
    (Patch '「套匙程」激震 副副刷副旁边据撞推客'             '社会民生' '香港'),
    (Patch 'AI聪明狂潮 大模型股爱炒热点'                    '财经商业' '国际'),
    (Patch '两投行传人 退出竞赛关于IPO'                     '财经商业' '国际'),
    (Patch '中东黑火暗温 道指涨479回款'                     '国际新闻' '国际'),
    (Patch '各地填充始 建OpenClaw产业'                      '财经商业' '国际'),
    (Patch '港元兑美元触及弱方兑换保证水平'                 '财经商业' '香港'),
    (Patch '零售商呼吁政府推出更多消费刺激措施'             '财经商业' '香港'),
    (Patch '本港首季GDP增速超预期经济学家上调预测'           '财经商业' '香港'),
    (Patch '港股通南向资金连续五日净买入'                   '财经商业' '香港'),
    # ── Google 趋势 ──
    (Patch 'Hong Kong election results spark global debate'  '政务政策' '国际'),
    (Patch 'DeepSeek AI 超越 ChatGPT 成为全球搜索热词'       '财经商业' '国际'),
    (Patch 'Taiwan Strait tensions escalate amid military drills' '国际新闻' '国际'),
    (Patch '中国内地春节旅游人次创历史新高'                 '旅游出行' '大陆'),
    # ── 微博热搜（独有标题）──
    (Patch '美国比人升左希莫德旺大事点重斩行人理？'          '国际新闻' '国际'),
    (Patch '两会代表热议逃离身份证实名制问题'               '政务政策' '大陆'),
    (Patch '雷军2026两会建议引局关注'                       '政务政策' '大陆'),
    (Patch '山东修高鐵站挖出5亿年前化石百岚'                '社会民生' '大陆'),
    (Patch '政協委员建议高中纳入义务教育'                   '教育就业' '大陆'),
    # ── 抖音热搜（独有标题）──
    (Patch '油价｜跨境审查加码 大浪引发迪拜理财争议'         '财经商业' '国际'),
    (Patch '两会代表热议提案如何落地实施'                   '政务政策' '大陆'),
    (Patch '香港教育改革动态：新课程标准将长'               '教育就业' '香港'),
    (Patch 'DeepSeek 底底是什么？香港年轻人炸了'             '财经商业' '香港'),
    (Patch '香港达人分享日本生活体验引关注'                 '旅游出行' '香港'),
    # ── 百度热搜（独有标题）──
    (Patch '北京地铁新线年底开通首班车时间调整'             '社会民生' '大陆'),
    (Patch '国产新能源汽车出口首次突破百万辆'               '财经商业' '大陆'),
    (Patch '教育部通知：今年高考报名人数创历史新高'          '教育就业' '大陆'),
    (Patch '春季踏青出行指南：十大热门景区推荐'             '旅游出行' '大陆')
)

# ── 3. 批量替换 ───────────────────────────────────────────────
$count = 0
foreach ($pair in $pairs) {
    $old = $pair[0]; $new = $pair[1]
    if ($c.Contains($old)) {
        $c = $c.Replace($old, $new)
        $count++
    } else {
        Write-Warning "NOT FOUND: $old"
    }
}

[IO.File]::WriteAllText($file, $c, $enc)
Write-Host "Done. $count titles tagged."
