# -*- coding: utf-8 -*-
with open(r'c:\Pros\ZJ0512\监测预警\AI智能推荐\index.html', 'r', encoding='utf-8') as f:
    content = f.read()

old_mk = '''        function mk(id,t,di,dl,d2,risk,sc,dt,snt,snl,sum){
            var rm={high:"高风险",medium:"中风险",low:"低风险"};
            return{id:id,title:t,domainId:di,domainLabel:dl,domainL2:d2,riskLevel:risk,riskLabel:rm[risk]||"中风险",
                articleCount:Math.max(2,Math.floor(sc/25)),platforms:["新闻资讯","微博"],
                score:sc,dateTime:dt,read:false,queued:false,sentiment:snt,sentimentLabel:snl,
                summary:sum,analysis:"AI持续监测中，建议关注后续进展。",
                persons:[],orgs:[],
                topics:[d2||dl,"舆情动态"],
                viewpoints:[{text:"事件持续受到各方关注。",platform:"新闻资讯",sentiment:snt}],
                suggestions:["持续监测事件动态","做好舆情研判预案"],
                timeline:[{time:dt.slice(5,16).replace("T"," "),desc:"事件进入AI监测视野，自动标记待阅。"}],
                articles:[{id:parseInt(id.replace(/\\D/g,""))*10,title:t,platform:"新闻资讯",sentiment:snt,sentimentLabel:snl,dateTime:dt}]};
        }'''

new_mk = r'''        function mk(id,t,di,dl,d2,risk,sc,dt,snt,snl,sum){
            var rm={high:"高风险",medium:"中风险",low:"低风险"};
            var snMap={"positive":"正面","negative":"负面","neutral":"中立"};
            // ── domain-aware person/org pools ──
            var personPool={
                "key-focus":[{name:"值班指挥官",role:"官方",count:4},{name:"现场负责人",role:"官方",count:3}],
                "hot-topic":[{name:"政策研究专家",role:"专家",count:3},{name:"立法会议员",role:"政界",count:2}],
                "domain-dynamic":[{name:"领域专家学者",role:"专家",count:3},{name:"行业协会代表",role:"行业",count:2}],
                "person-dynamic":[{name:"政府官员（匿名）",role:"政府",count:4},{name:"知名人士",role:"公众",count:2}],
                "special-monitor":[{name:"业界资深人士",role:"行业",count:3},{name:"媒体观察员",role:"媒体",count:2}]
            };
            var orgPool={
                "key-focus":[{name:"相关政府部门",type:"政府",count:5},{name:"应急响应机构",type:"政府",count:3},{name:"本地媒体",type:"媒体",count:2}],
                "hot-topic":[{name:"政策制定部门",type:"政府",count:4},{name:"立法机构",type:"政府",count:3},{name:"咨询委员会",type:"机构",count:2}],
                "domain-dynamic":[{name:"主管部门",type:"政府",count:4},{name:"行业协会",type:"行业",count:3},{name:"研究机构",type:"学术",count:2}],
                "person-dynamic":[{name:"所属政府机构",type:"政府",count:5},{name:"相关委员会",type:"政府",count:3}],
                "special-monitor":[{name:"相关媒体机构",type:"媒体",count:6},{name:"监管机构",type:"政府",count:3},{name:"行业联盟",type:"行业",count:2}]
            };
            // ── viewpoint templates by sentiment ──
            var expPos=["该政策方向符合整体发展需要，执行层面有待持续跟进。","从专业角度看，此举具有积极的示范意义。","相关安排符合实际情况，是合理的政策选择。"];
            var expNeg=["现行机制存在明显的制度性漏洞，需从根本上加以改进。","当前处理方式恐难有效化解问题，建议尽快重新评估。","相关政策缺乏充分的事前评估，实施风险不可低估。"];
            var expNeu=["目前情况仍存在多种解读空间，建议继续收集更多数据后再作判断。","此议题涉及多方利益，需平衡各方诉求后审慎推进。","从现有信息来看，局势走向尚不明朗，持续观察为宜。"];
            var netPos=["整体方向是对的，希望当局加快推进落地。","对相关安排表示认可，期待后续有更多配套措施。","感受到明显的改善，希望持续推进。"];
            var netNeg=["当局处理方式令人失望，迟迟未见实质行动。","普通市民承受着实际影响，官方却反应迟缓，难以接受。","问题一再被拖延，对相关部门感到不满。"];
            var netNeu=["希望当局尽快给出明确说法，消除公众疑虑。","暂时保持观望，等待更多官方信息发布。","此事仍有待进一步了解，目前判断为时尚早。"];
            var expNames=["李明远（政策分析师）","陈志华（领域专家）","林建国（资深研究员）","黄思雅（学术顾问）","张伟明（行业专家）"];
            var expPlatforms=["新闻资讯","微博","论坛"];
            var netPlatforms=["微博","论坛","Facebook","短视频","小红书"];
            var idx=parseInt(id.replace(/\D/g,""))||1;
            var eArr=snt==="positive"?expPos:(snt==="negative"?expNeg:expNeu);
            var nArr=snt==="positive"?netPos:(snt==="negative"?netNeg:netNeu);
            var sug1=risk==="high"?"立即启动应急舆情响应，组织权威信息快速发布":risk==="medium"?"密切关注事态发展，提前准备多套应对方案":"保持常规监测频率，定期汇总舆情动态";
            var sug2=snt==="negative"?"主动发布权威信息，回应公众关切，降低误读风险":snt==="positive"?"及时跟进正面进展，放大有效的舆论引导效果":"梳理各方主要观点，形成多角度综合报告";
            var sug3="持续跟踪"+( d2||dl)+"领域相关动态，评估后续影响走向";
            var t1Offset=Math.max(1,Math.floor(sc/40));
            var t2Offset=Math.max(2,Math.floor(sc/30));
            var t3Offset=Math.max(3,Math.floor(sc/25));
            var baseDate=dt.slice(0,10);var baseTime=dt.slice(11,16);
            var hrs=parseInt(baseTime.split(":")[0]);
            function pad(n){return n<10?"0"+n:String(n);}
            var tl=[
                {time:baseDate.slice(5)+" "+pad(Math.max(0,hrs-t3Offset))+":00",desc:"相关信息开始在网络平台出现，初步引发讨论。",platform:"新闻资讯",author:"媒体记者"},
                {time:baseDate.slice(5)+" "+pad(Math.max(0,hrs-t2Offset))+":30",desc:"话题在微博、论坛等平台快速传播，互动量持续攀升。",platform:"微博",author:"各方用户"},
                {time:baseDate.slice(5)+" "+pad(Math.max(0,hrs-t1Offset))+":00",desc:"主流媒体跟进报道，权威声音介入，讨论趋于深化。",platform:"新闻资讯",author:"主流媒体"},
                {time:baseDate.slice(5)+" "+baseTime,desc:"舆情热度进入峰值区间，AI系统完成高优先级标记。",platform:"综合平台",author:"各方"}
            ];
            var arts=[
                {id:idx*10,title:t,platform:"新闻资讯",sentiment:snt,sentimentLabel:snl,dateTime:dt},
                {id:idx*10+1,title:"【深度】"+t.slice(0,20)+"背后的多方解读",platform:"微博",sentiment:"neutral",sentimentLabel:"中立",dateTime:dt.replace("T"," ").slice(0,16).replace(" ","T")+"00"}
            ];
            var ps=personPool[di]||personPool["hot-topic"];
            var os=orgPool[di]||orgPool["hot-topic"];
            var vps=[
                {text:eArr[idx%3],platform:expPlatforms[idx%3],sentiment:snt,type:"expert",supportRate:55+idx%35,name:expNames[idx%5]},
                {text:eArr[(idx+1)%3],platform:expPlatforms[(idx+1)%3],sentiment:"neutral",type:"expert",supportRate:50+(idx+2)%30,name:expNames[(idx+2)%5]},
                {text:nArr[idx%3],platform:netPlatforms[idx%5],sentiment:snt,type:"netizen",supportRate:60+idx%30},
                {text:nArr[(idx+1)%3],platform:netPlatforms[(idx+2)%5],sentiment:snt==="positive"?"neutral":snt,type:"netizen",supportRate:55+(idx+3)%35},
                {text:nArr[(idx+2)%3],platform:netPlatforms[(idx+3)%5],sentiment:"neutral",type:"netizen",supportRate:45+(idx+1)%30}
            ];
            return{id:id,title:t,domainId:di,domainLabel:dl,domainL2:d2,riskLevel:risk,riskLabel:rm[risk]||"中风险",
                articleCount:Math.max(2,Math.floor(sc/25)),platforms:["新闻资讯","微博"],
                score:sc,dateTime:dt,read:false,queued:false,sentiment:snt,sentimentLabel:snl,
                summary:sum,analysis:"该议题当前传播热度"+( risk==="high"?"较高，需重点关注":risk==="medium"?"中等，建议持续跟踪":"偏低，维持常规监测")+
                    "，情绪倾向"+snl+"。建议结合"+( d2||dl)+"领域背景深化研判，做好多场景预案。",
                persons:ps,orgs:os,
                topics:[d2||dl,"舆情动态","政策研判","媒体关注"],
                viewpoints:vps,
                suggestions:[sug1,sug2,sug3],
                timeline:tl,
                articles:arts};
        }'''

if old_mk in content:
    content = content.replace(old_mk, new_mk)
    print('✓ mk() function replaced')
else:
    print('✗ mk() NOT FOUND - checking partial...')
    idx = content.find('function mk(id,t,di,dl')
    if idx >= 0:
        print('Found at', idx)
        print(repr(content[idx:idx+200]))

with open(r'c:\Pros\ZJ0512\监测预警\AI智能推荐\index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print('Done.')
