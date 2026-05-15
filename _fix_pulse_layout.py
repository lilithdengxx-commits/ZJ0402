f = r'c:\Pros\ZJ0512\事件分析\事件管理\事件分析详情\index.html'
c = open(f, encoding='utf-8').read()

# ── 1. CSS 替换（整块 ev-pulse-* 样式）──────────────────────────────────
OLD_CSS = '''        /* ── 事件脉络：左时间轴 + 右文章 ── */
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
        .ev-pulse-card-meta { font-size: 11px; color: #90a0b5; line-height: 1.6; }'''

NEW_CSS = '''        /* ── 事件脉络：左时间轴 + 右文章 ── */
        .ev-pulse-wrap { display: grid; grid-template-columns: 200px minmax(0,1fr); gap: 0; align-items: start; }
        /* 左侧时间轴 */
        .ev-pulse-axis { position: relative; display: flex; flex-direction: column; }
        .ev-pulse-axis::before { content:""; position:absolute; top:0; bottom:0; left:14px; width:2px; background:rgba(122,145,184,0.16); z-index:0; }
        .ev-pulse-node { position: relative; display: flex; gap: 12px; align-items: flex-start; cursor: pointer; padding: 0 16px 0 0; margin-bottom: 0; min-height: 0; }
        .ev-pulse-node-left { display: flex; flex-direction: column; align-items: center; flex-shrink: 0; width: 28px; padding-top: 3px; }
        .ev-pulse-dot { width: 10px; height: 10px; border-radius: 50%; background: rgba(180,195,215,0.6); border: 2px solid #fff; box-shadow: 0 0 0 2px rgba(122,145,184,0.2); transition: background .15s, transform .15s; flex-shrink: 0; position: relative; z-index: 1; }
        .ev-pulse-node.positive .ev-pulse-dot { background: #4ec65f; box-shadow: 0 0 0 2px rgba(78,198,95,0.25); }
        .ev-pulse-node.warning .ev-pulse-dot { background: #f0a500; box-shadow: 0 0 0 2px rgba(255,166,0,0.25); }
        .ev-pulse-node.danger .ev-pulse-dot { background: #e04040; box-shadow: 0 0 0 2px rgba(255,82,82,0.25); }
        .ev-pulse-node.active .ev-pulse-dot { transform: scale(1.4); }
        .ev-pulse-connector { flex: 1; width: 2px; background: rgba(122,145,184,0.14); min-height: 28px; }
        .ev-pulse-node-right { display: flex; flex-direction: column; gap: 3px; padding: 0 0 20px; flex: 1; min-width: 0; }
        .ev-pulse-time { font-size: 11px; font-weight: 700; color: #30496f; line-height: 1.4; }
        .ev-pulse-excerpt { font-size: 12px; color: #54667f; line-height: 1.5; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; }
        .ev-pulse-source { font-size: 11px; color: #90a0b5; }
        .ev-pulse-node.active .ev-pulse-time { color: var(--primary); }
        /* 右侧文章列表 */
        .ev-pulse-articles { display: flex; flex-direction: column; gap: 0; padding-left: 14px; }
        .ev-pulse-card { padding: 14px 0; border-bottom: 1px solid rgba(122,145,184,0.1); display: grid; gap: 6px; cursor: pointer; transition: opacity .15s; }
        .ev-pulse-card:last-child { border-bottom: none; }
        .ev-pulse-card:hover .ev-pulse-card-title { color: var(--primary); }
        .ev-pulse-card.active .ev-pulse-card-title { color: var(--primary); }
        .ev-pulse-card-title { font-size: 14px; font-weight: 700; color: #1e2d45; line-height: 1.55; }
        .ev-pulse-card-row { display: flex; align-items: center; gap: 8px; flex-wrap: wrap; }
        .ev-pulse-src { font-size: 11px; color: #90a0b5; }
        .ev-sentiment { display: inline-flex; align-items: center; height: 20px; padding: 0 8px; border-radius: 4px; font-size: 11px; font-weight: 700; }
        .ev-sentiment.neutral { background: rgba(255,166,0,0.12); color: #b27400; }
        .ev-sentiment.negative { background: rgba(255,82,82,0.1); color: #d54343; }
        .ev-sentiment.positive { background: rgba(78,198,95,0.1); color: #36933e; }
        .ev-pulse-card-time { font-size: 11px; color: #90a0b5; }'''

assert c.count(OLD_CSS) == 1, f'CSS match: {c.count(OLD_CSS)}'
c = c.replace(OLD_CSS, NEW_CSS)

# ── 2. JS 替换（整块事件脉络渲染函数）──────────────────────────────────────
OLD_JS = '''            // 事件脉络 – 左轴 + 右侧文章
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
                        + '<div class="ev-pulse-time">' + escapeHtml(item.time).replace(" ", "<br>") + '</div>'
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

NEW_JS = '''            // 事件脉络 – 左时间轴 + 右文章
            (function() {
                var axisEl = document.getElementById("evPulseAxis");
                var articlesEl = document.getElementById("evPulseArticles");
                if (!axisEl || !articlesEl) return;
                var tl = profile.timeline;

                // 从 meta 字符串提取平台和情感
                function parsePlatform(meta) {
                    var m = meta.match(/平台[:：]\s*([^\|｜]+)/);
                    return m ? m[1].trim() : "";
                }
                function parseSentiment(meta) {
                    if (/情感[:：]\s*负/.test(meta)) return { cls: "negative", label: "负面" };
                    if (/情感[:：]\s*中/.test(meta)) return { cls: "neutral",  label: "中立" };
                    if (/情感[:：]\s*(正|积极)/.test(meta)) return { cls: "positive", label: "正面" };
                    // 根据 state 推断
                    return { cls: "neutral", label: "中立" };
                }
                function getExcerpt(meta) {
                    // 取第一个 | 之前的文字作为摘要
                    return meta.split(/\|｜/)[0].trim();
                }
                function getSource(meta) {
                    var plat = parsePlatform(meta);
                    var m2 = meta.match(/^([^|｜]+)/);
                    var src = m2 ? m2[1].trim() : "";
                    return plat || src;
                }

                // 左侧时间轴：时间 + 标题摘要 + 来源
                axisEl.innerHTML = tl.map(function(item, i) {
                    var src = getSource(item.meta);
                    var isLast = i === tl.length - 1;
                    return '<div class="ev-pulse-node ' + item.state + (i === 0 ? " active" : "") + '" data-idx="' + i + '">'
                        + '<div class="ev-pulse-node-left">'
                        + '<div class="ev-pulse-dot"></div>'
                        + (isLast ? "" : '<div class="ev-pulse-connector"></div>')
                        + '</div>'
                        + '<div class="ev-pulse-node-right">'
                        + '<div class="ev-pulse-time">' + escapeHtml(item.time) + '</div>'
                        + '<div class="ev-pulse-excerpt">' + escapeHtml(item.title) + '</div>'
                        + (src ? '<div class="ev-pulse-source">' + escapeHtml(src) + '</div>' : '')
                        + '</div>'
                        + '</div>';
                }).join("");

                // 右侧文章列表：标题 + 来源 + 情感badge + 时间
                articlesEl.innerHTML = tl.map(function(item, i) {
                    var sentiment = parseSentiment(item.meta);
                    var platform = parsePlatform(item.meta);
                    return '<div class="ev-pulse-card' + (i === 0 ? " active" : "") + '" data-idx="' + i + '">'
                        + '<div class="ev-pulse-card-title">' + escapeHtml(item.title) + '</div>'
                        + '<div class="ev-pulse-card-row">'
                        + (platform ? '<span class="ev-pulse-src">' + escapeHtml(platform) + '</span><span style="color:#cdd5e0">·</span>' : '')
                        + '<span class="ev-sentiment ' + sentiment.cls + '">' + sentiment.label + '</span>'
                        + '<span style="color:#cdd5e0">·</span>'
                        + '<span class="ev-pulse-card-time">' + escapeHtml(item.time) + '</span>'
                        + '</div>'
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

assert c.count(OLD_JS) == 1, f'JS match: {c.count(OLD_JS)}'
c = c.replace(OLD_JS, NEW_JS)

open(f, 'w', encoding='utf-8').write(c)
print('done')
