f = r'c:\Pros\ZJ0512\事件分析\事件管理\事件分析详情\index.html'
c = open(f, encoding='utf-8').read()

# ── 1. CSS: 新增时间轴左右布局、网民观点环图 CSS ──────────────────────────
OLD_CSS = '''        .bar-track {
            height: 10px;
            border-radius: 999px;
            background: rgba(226, 233, 246, 0.92);
            overflow: hidden;
        }

        .bar-fill {
            height: 100%;
            border-radius: inherit;
            background: var(--primary);
        }'''

NEW_CSS = '''        .bar-track {
            height: 10px;
            border-radius: 999px;
            background: rgba(226, 233, 246, 0.92);
            overflow: hidden;
        }

        .bar-fill {
            height: 100%;
            border-radius: inherit;
            background: var(--primary);
        }

        /* ── 事件脉络：左时间轴 + 右文章 ── */
        .ev-pulse-wrap { display: grid; grid-template-columns: 160px minmax(0,1fr); gap: 0; min-height: 320px; }
        .ev-pulse-axis { position: relative; padding: 4px 0; }
        .ev-pulse-axis::before { content:""; position:absolute; top:0; bottom:0; left:50%; width:2px; background:rgba(122,145,184,0.16); transform:translateX(-50%); }
        .ev-pulse-node { position: relative; display: flex; flex-direction: column; align-items: center; cursor: pointer; padding: 10px 0; }
        .ev-pulse-dot { width: 12px; height: 12px; border-radius: 50%; background: rgba(122,145,184,0.3); border: 2px solid #fff; box-shadow: 0 0 0 2px rgba(122,145,184,0.2); transition: background .15s; flex-shrink: 0; position: relative; z-index: 1; }
        .ev-pulse-node.positive .ev-pulse-dot { background: #36933e; box-shadow: 0 0 0 2px rgba(78,198,95,0.2); }
        .ev-pulse-node.warning .ev-pulse-dot { background: #b27400; box-shadow: 0 0 0 2px rgba(255,166,0,0.2); }
        .ev-pulse-node.danger .ev-pulse-dot { background: #d54343; box-shadow: 0 0 0 2px rgba(255,82,82,0.2); }
        .ev-pulse-node.active .ev-pulse-dot { transform: scale(1.35); }
        .ev-pulse-time { margin-top: 5px; font-size: 10px; color: #90a0b5; text-align: center; line-height: 1.3; white-space: nowrap; }
        .ev-pulse-articles { display: flex; flex-direction: column; gap: 8px; padding: 4px 0 4px 14px; overflow-y: auto; max-height: 460px; }
        .ev-pulse-card { padding: 10px 14px; border-radius: 8px; border: 1px solid rgba(122,145,184,0.12); background: rgba(247,250,255,0.9); display: grid; gap: 6px; cursor: pointer; transition: border-color .15s; }
        .ev-pulse-card:hover { border-color: rgba(43,97,240,0.22); }
        .ev-pulse-card.active { border-color: rgba(43,97,240,0.3); background: rgba(43,97,240,0.04); }
        .ev-pulse-card-top { display: flex; align-items: center; gap: 8px; }
        .ev-pulse-card-title { font-size: 13px; font-weight: 700; color: #213049; line-height: 1.5; }
        .ev-pulse-card-meta { font-size: 11px; color: #90a0b5; line-height: 1.6; }

        /* ── rank/post 卡片缩短 ── */
        .rank-item, .post-item { padding: 8px 12px; gap: 4px; }

        /* ── 网民观点：环图+列表 ── */
        .opinion-wrap { display: grid; grid-template-columns: 200px minmax(0,1fr); gap: 20px; align-items: start; }
        .opinion-donut-wrap { display: flex; flex-direction: column; align-items: center; gap: 12px; }
        .opinion-donut { width: 160px; height: 160px; border-radius: 50%; position: relative; display: grid; place-items: center; flex-shrink: 0; }
        .opinion-donut::before { content:""; position:absolute; inset:32px; border-radius:50%; background:#fff; box-shadow: inset 0 0 0 1px rgba(122,145,184,0.08); }
        .opinion-donut-legend { display: grid; gap: 6px; width: 100%; }
        .opinion-donut-legend-item { display: flex; align-items: center; gap: 6px; font-size: 11px; color: #54667f; }
        .opinion-donut-legend-item .dot { width: 8px; height: 8px; border-radius: 50%; flex-shrink: 0; }
        .opinion-right-list { display: grid; gap: 8px; }
        .opinion-right-item { display: grid; gap: 4px; padding: 10px 14px; border-radius: 8px; border: 1px solid rgba(122,145,184,0.1); background: rgba(247,250,255,0.9); }
        .opinion-right-title { font-size: 13px; font-weight: 700; color: #213049; line-height: 1.5; }
        .opinion-right-detail { font-size: 12px; color: #5a6c87; line-height: 1.6; }
        .opinion-right-tag { display: inline-flex; align-items: center; height: 20px; padding: 0 8px; border-radius: 999px; font-size: 10px; font-weight: 700; background: rgba(43,97,240,0.08); color: var(--primary); }'''

assert c.count(OLD_CSS) == 1, f'CSS match: {c.count(OLD_CSS)}'
c = c.replace(OLD_CSS, NEW_CSS)

# ── 2. HTML: 事件脉络 – 改名+新结构 ──────────────────────────────────────
OLD_TL_HTML = '''                    <section class="panel">
                        <div class="panel-head">
                            <strong>事件脉络时间轴</strong>
                            <span>按传播影响排序</span>
                        </div>
                        <div class="timeline-list" id="timelineList"></div>
                    </section>

                    <div class="dual-grid">
                        <section class="panel">
                            <div class="panel-head">
                                <strong>高频信息点</strong>
                                <span>词频统计</span>
                            </div>
                            <div class="bar-list" id="keywordList"></div>
                        </section>

                        <section class="panel">
                            <div class="panel-head">
                                <strong>敏感议题分布</strong>
                                <span>重点关注</span>
                            </div>
                            <div class="bar-list" id="issueList"></div>
                        </section>
                    </div>'''

NEW_TL_HTML = '''                    <section class="panel">
                        <div class="panel-head">
                            <strong>事件脉络</strong>
                            <span>按传播影响排序</span>
                        </div>
                        <div class="ev-pulse-wrap">
                            <div class="ev-pulse-axis" id="evPulseAxis"></div>
                            <div class="ev-pulse-articles" id="evPulseArticles"></div>
                        </div>
                    </section>'''

assert c.count(OLD_TL_HTML) == 1, f'TL HTML match: {c.count(OLD_TL_HTML)}'
c = c.replace(OLD_TL_HTML, NEW_TL_HTML)

# ── 3. HTML: 网民观点 – 改为带环图结构 ──────────────────────────────────
OLD_OPINION_HTML = '''                        <section class="panel">
                            <div class="panel-head">
                                <strong>网民观点</strong>
                                <span>建议优先跟踪</span>
                            </div>
                            <div class="opinion-list" id="focusList"></div>
                        </section>'''

NEW_OPINION_HTML = '''                        <section class="panel">
                            <div class="panel-head">
                                <strong>网民观点</strong>
                                <span>建议优先跟踪</span>
                            </div>
                            <div class="opinion-wrap">
                                <div class="opinion-donut-wrap">
                                    <div class="opinion-donut" id="opinionDonut"></div>
                                    <div class="opinion-donut-legend" id="opinionDonutLegend"></div>
                                </div>
                                <div class="opinion-right-list" id="focusList"></div>
                            </div>
                        </section>'''

assert c.count(OLD_OPINION_HTML) == 1, f'Opinion HTML match: {c.count(OLD_OPINION_HTML)}'
c = c.replace(OLD_OPINION_HTML, NEW_OPINION_HTML)

# ── 4. JS: 替换 timelineList.innerHTML + keywordList + issueList 渲染为新时间轴逻辑 ──
OLD_JS_TL = '''            timelineList.innerHTML = profile.timeline.map((item) => `
                <article class="timeline-item">
                    <div class="timeline-top">
                        <span class="state-badge ${escapeHtml(item.state)}">${item.state === "positive" ? "关注" : item.state === "warning" ? "预警" : "高危"}</span>
                        <span class="timeline-meta">${escapeHtml(item.time)}</span>
                    </div>
                    <div class="timeline-title">${escapeHtml(item.title)}</div>
                    <div class="timeline-meta">${escapeHtml(item.meta)}</div>
                </article>
            `).join("");

            keywordList.innerHTML = profile.keywords.map((item) => `
                <div class="bar-item">
                    <div class="bar-top"><span>${escapeHtml(item.name)}</span><span>${item.value}</span></div>
                    <div class="bar-track"><div class="bar-fill" style="width:${item.value}%;"></div></div>
                </div>
            `).join("");

            issueList.innerHTML = profile.issues.map((item) => `
                <div class="bar-item">
                    <div class="bar-top"><span>${escapeHtml(item.name)}</span><span>${item.value}</span></div>
                    <div class="bar-track"><div class="bar-fill" style="width:${item.value}%;background:linear-gradient(90deg,#ff944d,#ffcf5f);"></div></div>
                </div>
            `).join("");'''

NEW_JS_TL = '''            // 事件脉络 – 左轴 + 右侧文章
            (function() {
                var axisEl = document.getElementById("evPulseAxis");
                var articlesEl = document.getElementById("evPulseArticles");
                if (!axisEl || !articlesEl) return;
                var tl = profile.timeline;
                var stateLabel = { positive: "关注", warning: "预警", danger: "高危" };
                var stateBg = { positive: "rgba(78,198,95,0.12)", warning: "rgba(255,166,0,0.14)", danger: "rgba(255,82,82,0.12)" };
                var stateColor = { positive: "#36933e", warning: "#b27400", danger: "#d54343" };
                axisEl.innerHTML = tl.map(function(item, i) {
                    return '<div class="ev-pulse-node ' + item.state + ' ' + (i === 0 ? "active" : "") + '" data-idx="' + i + '">'
                        + '<div class="ev-pulse-dot"></div>'
                        + '<div class="ev-pulse-time">' + escapeHtml(item.time.replace(" ", "<br>")) + '</div>'
                        + '</div>';
                }).join("");
                articlesEl.innerHTML = tl.map(function(item, i) {
                    return '<div class="ev-pulse-card' + (i === 0 ? " active" : "") + '" data-idx="' + i + '">'
                        + '<div class="ev-pulse-card-top">'
                        + '<span class="state-badge ' + item.state + '" style="background:' + stateBg[item.state] + ';color:' + stateColor[item.state] + '">' + stateLabel[item.state] + '</span>'
                        + '<span style="font-size:11px;color:#90a0b5">' + escapeHtml(item.time) + '</span>'
                        + '</div>'
                        + '<div class="ev-pulse-card-title">' + escapeHtml(item.title) + '</div>'
                        + '<div class="ev-pulse-card-meta">' + escapeHtml(item.meta) + '</div>'
                        + '</div>';
                }).join("");
                function setActive(idx) {
                    axisEl.querySelectorAll(".ev-pulse-node").forEach(function(n, i) { n.classList.toggle("active", i === idx); });
                    articlesEl.querySelectorAll(".ev-pulse-card").forEach(function(n, i) { n.classList.toggle("active", i === idx); });
                }
                axisEl.addEventListener("click", function(e) {
                    var node = e.target.closest("[data-idx]"); if (!node) return;
                    setActive(parseInt(node.dataset.idx));
                });
                articlesEl.addEventListener("click", function(e) {
                    var node = e.target.closest("[data-idx]"); if (!node) return;
                    setActive(parseInt(node.dataset.idx));
                });
            })();'''

assert c.count(OLD_JS_TL) == 1, f'JS TL match: {c.count(OLD_JS_TL)}'
c = c.replace(OLD_JS_TL, NEW_JS_TL)

# ── 5. JS: 网民观点 focusList 改为带环图 ──────────────────────────────────
OLD_JS_FOCUS = '''            focusList.innerHTML = profile.focus.map((item) => `
                <article class="focus-item">
                    <div class="opinion-top">
                        <div class="opinion-title">${escapeHtml(item.title)}</div>
                        <div class="opinion-meta">占比 ${item.value.toFixed(2)}%</div>
                    </div>
                    <div class="bar-track"><div class="bar-fill" style="width:${item.value}%;background:linear-gradient(90deg,#ff944d,#ffcf5f);"></div></div>
                    <div class="opinion-meta">${escapeHtml(item.detail)}</div>
                </article>
            `).join("");'''

NEW_JS_FOCUS = '''            // 网民观点环图
            (function() {
                var donutEl = document.getElementById("opinionDonut");
                var legendEl = document.getElementById("opinionDonutLegend");
                var listEl = document.getElementById("focusList");
                if (!donutEl || !legendEl || !listEl) return;
                var focusData = profile.focus;
                var colors = ["#2f6bff","#ff944d","#6dd9c5","#8d6dff","#ff6c6c","#ffc542"];
                var total = focusData.reduce(function(s, d) { return s + d.value; }, 0);
                var segs = []; var acc = 0;
                focusData.forEach(function(d, i) {
                    var pct = d.value / total * 360;
                    segs.push(colors[i % colors.length] + " " + acc + "deg " + (acc + pct).toFixed(2) + "deg");
                    acc += pct;
                });
                donutEl.style.background = "conic-gradient(" + segs.join(",") + ")";
                legendEl.innerHTML = focusData.map(function(d, i) {
                    return '<div class="opinion-donut-legend-item">'
                        + '<span class="dot" style="background:' + colors[i % colors.length] + '"></span>'
                        + '<span>' + escapeHtml(d.title.length > 10 ? d.title.slice(0, 10) + "…" : d.title) + '</span>'
                        + '<span style="margin-left:auto;color:#8594aa;font-size:11px">' + d.value.toFixed(1) + '%</span>'
                        + '</div>';
                }).join("");
                listEl.innerHTML = focusData.map(function(item, i) {
                    return '<div class="opinion-right-item">'
                        + '<div style="display:flex;align-items:center;gap:8px">'
                        + '<span style="font-size:12px;font-weight:700;color:' + colors[i % colors.length] + '">' + (i + 1) + '、</span>'
                        + '<div class="opinion-right-title">' + escapeHtml(item.title) + '</div>'
                        + '</div>'
                        + '<div class="opinion-right-detail">' + escapeHtml(item.detail) + '</div>'
                        + '<span class="opinion-right-tag">' + escapeHtml(item.detail.split("，")[0] || "主要观点") + '</span>'
                        + '</div>';
                }).join("");
            })();'''

assert c.count(OLD_JS_FOCUS) == 1, f'JS Focus match: {c.count(OLD_JS_FOCUS)}'
c = c.replace(OLD_JS_FOCUS, NEW_JS_FOCUS)

open(f, 'w', encoding='utf-8').write(c)
print('done')
