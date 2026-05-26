/**
 * AI 智能舆情分析助手
 * 悬浮球 + 问答面板，全局共享，所有页面引入此文件即可
 * 三种触发模式：
 *   1. 列表页批量操作 → window.aiAssistantOpenWithData(dataArray)
 *   2. 点击面板预置问题
 *   3. 用户直接输入提问
 */
(function () {
  'use strict';

  /* ════════════════════════════ CSS ════════════════════════════ */
  const CSS = `
  #ai-ball {
    position: fixed; bottom: 80px; right: 28px;
    width: 58px; height: 58px; border-radius: 50%;
    background: transparent; box-shadow: none;
    cursor: pointer; z-index: 9998;
    display: flex; align-items: center; justify-content: center;
    user-select: none; transition: filter .2s, transform .15s;
  }
  #ai-ball:hover { filter: brightness(1.08) drop-shadow(0 4px 10px rgba(0,0,0,0.22)); transform: scale(1.07); }
  #ai-ball.ai-dragging { transition: none; filter: brightness(1.06); }
  #ai-ball svg { pointer-events: none; }
  #ai-ball .ai-badge {
    position: absolute; top: -2px; right: -2px;
    width: 18px; height: 18px; border-radius: 50%;
    background: #e04040; border: 2px solid #fff;
    font-size: 9px; font-weight: 800; color: #fff;
    display: flex; align-items: center; justify-content: center;
    font-family: "PingFang SC","Microsoft YaHei UI",sans-serif;
  }

  #ai-panel {
    position: fixed; top: 0; right: 0;
    width: 400px; height: 100vh;
    background: #fff; border-radius: 0;
    box-shadow: -4px 0 28px rgba(26,44,82,0.14);
    border-left: 1px solid rgba(43,97,240,0.1);
    z-index: 9999; display: flex; flex-direction: column; overflow: hidden;
    opacity: 0; transform: translateX(24px); pointer-events: none;
    transition: opacity .22s, transform .22s;
    font-family: "PingFang SC","Lantinghei SC","Microsoft YaHei UI",sans-serif;
  }
  #ai-panel.ai-open { opacity: 1; transform: translateX(0); pointer-events: all; }

  /* ── Header ── */
  .ai-ph {
    display: flex; align-items: center; gap: 10px;
    padding: 12px 14px; border-bottom: 1px solid rgba(122,145,184,0.12);
    flex: 0 0 auto; cursor: move; user-select: none;
  }
  .ai-ph-avatar {
    width: 36px; height: 36px; border-radius: 50%; flex: 0 0 36px;
    background: linear-gradient(135deg, #2b61f0, #7ab0ff);
    display: flex; align-items: center; justify-content: center;
  }
  .ai-ph-info { flex: 1; }
  .ai-ph-info strong { font-size: 13px; color: #1e2d45; font-weight: 800; display: block; }
  .ai-ph-info span { font-size: 11px; color: #9eb0c6; }
  .ai-ph-btn {
    width: 28px; height: 28px; border: none; background: transparent;
    border-radius: 7px; color: #9eb0c6; cursor: pointer;
    display: flex; align-items: center; justify-content: center;
    transition: background .15s, color .15s;
  }
  .ai-ph-btn:hover { background: rgba(43,97,240,0.08); color: #2b61f0; }

  /* ── Body ── */
  .ai-pb {
    flex: 1 1 auto; overflow-y: auto; overflow-x: hidden;
    display: flex; flex-direction: column;
  }
  .ai-pb::-webkit-scrollbar { width: 3px; }
  .ai-pb::-webkit-scrollbar-thumb { background: rgba(122,145,184,0.22); border-radius: 999px; }

  /* ── Welcome ── */
  .ai-welcome { padding: 16px 14px 12px; }
  .ai-welcome-hero {
    background: linear-gradient(135deg, #eef3ff 0%, #f5f9ff 100%);
    border: 1px solid rgba(43,97,240,0.1); border-radius: 14px;
    padding: 16px; margin-bottom: 12px;
  }
  .ai-welcome-hero h3 { font-size: 15px; font-weight: 800; color: #1e2d45; margin: 0 0 5px; }
  .ai-welcome-hero p { font-size: 12px; color: #6b7c95; margin: 0 0 12px; line-height: 1.65; }
  .ai-caps { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; }
  .ai-cap {
    background: #fff; border: 1px solid rgba(43,97,240,0.1); border-radius: 10px;
    padding: 10px 12px; cursor: pointer; transition: border-color .15s, box-shadow .15s;
  }
  .ai-cap:hover { border-color: rgba(43,97,240,0.3); box-shadow: 0 2px 10px rgba(43,97,240,0.1); }
  .ai-cap-label { font-size: 12px; font-weight: 700; color: #1e2d45; margin-bottom: 2px; }
  .ai-cap-sub { font-size: 11px; color: #9eb0c6; }

  .ai-presets-label { font-size: 12px; font-weight: 700; color: #1e2d45; margin-bottom: 8px; }
  .ai-preset-list { display: flex; flex-direction: column; gap: 6px; }
  .ai-preset-item {
    display: flex; align-items: center; justify-content: space-between;
    padding: 10px 12px; border-radius: 8px;
    border: 1px solid rgba(122,145,184,0.16); background: #fafcff;
    cursor: pointer; font-size: 13px; color: #3a4d68;
    transition: border-color .15s, background .15s, color .15s;
  }
  .ai-preset-item:hover { background: rgba(43,97,240,0.04); border-color: rgba(43,97,240,0.22); color: #2b61f0; }
  .ai-preset-item svg { color: #c5cdd9; flex: 0 0 14px; margin-left: 8px; }

  /* ── Chat ── */
  .ai-chat { padding: 12px 12px; display: flex; flex-direction: column; gap: 14px; }

  .ai-ctx-card {
    margin: 0 14px 4px;
    background: rgba(43,97,240,0.04); border: 1px solid rgba(43,97,240,0.14);
    border-radius: 10px; padding: 10px 12px; font-size: 12px; color: #4a5c7a;
  }
  .ai-ctx-title {
    font-weight: 700; color: #2b61f0; margin-bottom: 6px;
    display: flex; align-items: center; gap: 5px;
  }
  .ai-ctx-row { padding: 3px 0; border-bottom: 1px solid rgba(43,97,240,0.08); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
  .ai-ctx-row:last-child { border-bottom: none; }

  .ai-msg { display: flex; flex-direction: column; gap: 4px; }
  .ai-msg.user { align-items: flex-end; }
  .ai-msg.bot  { align-items: flex-start; }
  .ai-bubble {
    max-width: 86%; padding: 10px 13px; border-radius: 12px;
    font-size: 13px; line-height: 1.7; white-space: pre-wrap; word-break: break-word;
  }
  .ai-msg.user .ai-bubble { background: #2b61f0; color: #fff; border-bottom-right-radius: 4px; }
  .ai-msg.bot  .ai-bubble {
    background: #f4f7ff; color: #1e2d45;
    border: 1px solid rgba(43,97,240,0.08); border-bottom-left-radius: 4px;
  }
  .ai-msg-time { font-size: 11px; color: #9eb0c6; }

  .ai-typing-wrap { display: flex; align-items: flex-start; }
  .ai-typing {
    display: flex; gap: 5px; padding: 12px 14px;
    background: #f4f7ff; border-radius: 12px; border-bottom-left-radius: 4px;
    border: 1px solid rgba(43,97,240,0.08);
  }
  .ai-typing span {
    width: 7px; height: 7px; border-radius: 50%; background: #2b61f0;
    animation: ai-bounce 1.1s ease-in-out infinite;
  }
  .ai-typing span:nth-child(2) { animation-delay: .18s; }
  .ai-typing span:nth-child(3) { animation-delay: .36s; }
  @keyframes ai-bounce {
    0%,60%,100% { transform: translateY(0); opacity:.5; }
    30%          { transform: translateY(-6px); opacity:1; }
  }

  /* ── Robot eye glow ── */
  @keyframes ai-eye-glow {
    0%,100% { opacity: 0.9; }
    50%     { opacity: 0.3; }
  }
  .ai-robot-eye  { animation: ai-eye-glow 2.4s ease-in-out infinite; }
  .ai-robot-eye2 { animation: ai-eye-glow 2.4s ease-in-out infinite; animation-delay: 1.2s; }

  /* ── Input ── */
  .ai-input-area {
    flex: 0 0 auto; padding: 10px 12px;
    border-top: 1px solid rgba(122,145,184,0.1); background: #fff;
  }
  .ai-input-box {
    display: flex; align-items: flex-end; gap: 8px;
    padding: 8px 10px; border-radius: 10px;
    border: 1px solid rgba(43,97,240,0.2); background: #f8fbff;
    transition: border-color .2s;
  }
  .ai-input-box:focus-within { border-color: rgba(43,97,240,0.4); }
  .ai-input-box textarea {
    flex: 1; border: none; background: transparent; resize: none;
    font: inherit; font-size: 13px; color: #1e2d45; outline: none;
    min-height: 52px; max-height: 120px; line-height: 1.6;
  }
  .ai-input-box textarea::placeholder { color: #9eb0c6; }
  .ai-send {
    width: 30px; height: 30px; flex: 0 0 30px;
    border-radius: 8px; background: #2b61f0; border: none; color: #fff;
    display: flex; align-items: center; justify-content: center;
    cursor: pointer; transition: background .15s;
  }
  .ai-send:hover { background: #1a4ed4; }
  .ai-send:disabled { background: #c0ceea; cursor: default; }
  .ai-tool-row { display: flex; align-items: center; gap: 6px; margin-top: 7px; }
  .ai-tool-pill {
    display: flex; align-items: center; gap: 4px;
    padding: 4px 10px; border-radius: 999px;
    border: 1px solid rgba(122,145,184,0.18); background: #fff;
    font-size: 11px; color: #6b7c95; cursor: pointer; font-weight: 600;
    font-family: inherit; transition: all .15s;
  }
  .ai-tool-pill:hover, .ai-tool-pill.on { background: rgba(43,97,240,0.08); color: #2b61f0; border-color: rgba(43,97,240,0.25); }
  .ai-clear-btn {
    margin-left: auto; font-size: 11px; color: #c5cdd9;
    background: none; border: none; cursor: pointer; font-family: inherit;
    padding: 2px 6px;
  }
  .ai-clear-btn:hover { color: #9eb0c6; }

  /* ── Mode Tabs ── */
  .ai-mode-tabs {
    display: flex; gap: 4px; padding: 8px 12px 0;
    border-top: 1px solid rgba(122,145,184,0.1); background: #fff;
  }
  .ai-mode-tab {
    flex: 1; padding: 6px 2px; border-radius: 6px;
    border: 1px solid rgba(122,145,184,0.15); background: #f4f7fc;
    font: inherit; font-size: 11px; font-weight: 600; color: #7a91b8;
    cursor: pointer; transition: all .15s; white-space: nowrap;
  }
  .ai-mode-tab:hover { background: rgba(43,97,240,0.07); color: #2b61f0; border-color: rgba(43,97,240,0.2); }
  .ai-mode-tab.active { background: rgba(43,97,240,0.12); color: #1a4ed4; border-color: rgba(43,97,240,0.3); }

  /* ── AI助手 button injected into list pages ── */
  .btn-ai-asst {
    display: inline-flex; align-items: center; gap: 5px;
    padding: 5px 12px; border-radius: 7px;
    border: 1px solid rgba(43,97,240,0.25); background: rgba(43,97,240,0.07);
    color: #2b61f0; font-size: 12px; font-weight: 700;
    cursor: pointer; transition: all .15s; font-family: inherit;
    white-space: nowrap;
  }
  .btn-ai-asst:hover {
    background: rgba(43,97,240,0.13); border-color: rgba(43,97,240,0.4);
    box-shadow: 0 2px 8px rgba(43,97,240,0.16);
  }
  `;

  const styleEl = document.createElement('style');
  styleEl.textContent = CSS;
  document.head.appendChild(styleEl);

  /* ════════════════════════════ STATE ════════════════════════════ */
  const S = {
    open: false,
    inChat: false,
    streaming: false,
    deepThink: false,
    webSearch: false,
    contextData: null,
  };

  /* ════════════════════════════ FLOATING BALL ════════════════════════════ */
  const ball = document.createElement('div');
  ball.id = 'ai-ball';
  ball.innerHTML = `
    <div style="width:58px;height:58px;border-radius:50%;background:conic-gradient(from 263deg,#d940fb,#7c4dff,#2979ff,#00b0d8,#26c87a,#c8dc30,#ff9800,#f44336,#e91e8c,#d940fb);display:flex;align-items:center;justify-content:center;filter:drop-shadow(0 3px 8px rgba(0,0,0,0.22))">
      <div style="width:46px;height:46px;background:#fff;border-radius:14px;display:flex;align-items:center;justify-content:center;gap:6px">
        <div style="width:11px;height:13px;background:#18102e;border-radius:5px"></div>
        <div style="width:11px;height:13px;background:#18102e;border-radius:5px"></div>
      </div>
    </div>
    <div class="ai-badge">AI</div>
  `;
  document.body.appendChild(ball);

  /* ── Drag logic ── */
  let dragging = false, offX = 0, offY = 0, wasMoved = false;

  ball.addEventListener('mousedown', function (e) {
    if (e.button !== 0) return;
    dragging = true; wasMoved = false;
    const r = ball.getBoundingClientRect();
    offX = e.clientX - r.left; offY = e.clientY - r.top;
    ball.classList.add('ai-dragging');
    e.preventDefault();
  });

  document.addEventListener('mousemove', function (e) {
    if (!dragging) return;
    wasMoved = true;
    const x = Math.max(0, Math.min(e.clientX - offX, window.innerWidth  - ball.offsetWidth));
    const y = Math.max(0, Math.min(e.clientY - offY, window.innerHeight - ball.offsetHeight));
    ball.style.left = x + 'px'; ball.style.top = y + 'px';
    ball.style.right = 'auto'; ball.style.bottom = 'auto';
  });

  document.addEventListener('mouseup', function () {
    if (!dragging) return;
    dragging = false;
    ball.classList.remove('ai-dragging');
    if (!wasMoved) togglePanel(); // click → open/close
  });

  /* ════════════════════════════ PANEL ════════════════════════════ */
  const panel = document.createElement('div');
  panel.id = 'ai-panel';
  panel.innerHTML = `
    <div class="ai-ph" id="ai-ph">
      <div class="ai-ph-avatar" style="background:conic-gradient(from 263deg,#d940fb,#7c4dff,#2979ff,#00b0d8,#26c87a,#c8dc30,#ff9800,#f44336,#e91e8c,#d940fb)">
        <div style="width:28px;height:28px;background:#fff;border-radius:9px;display:flex;align-items:center;justify-content:center;gap:4px">
          <div style="width:7px;height:8px;background:#18102e;border-radius:3px"></div>
          <div style="width:7px;height:8px;background:#18102e;border-radius:3px"></div>
        </div>
      </div>
      <div class="ai-ph-info">
        <strong>智能舆情分析助手</strong>
        <span>AI · 在线</span>
      </div>
      <button class="ai-ph-btn" id="ai-min-btn" title="最小化">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none"><path d="M5 12H19" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>
      </button>
      <button class="ai-ph-btn" id="ai-close-btn" title="关闭">
        <svg width="13" height="13" viewBox="0 0 24 24" fill="none"><path d="M6 18L18 6M6 6l12 12" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>
      </button>
    </div>

    <div class="ai-pb" id="ai-pb">
      <!-- 欢迎页 -->
      <div class="ai-welcome" id="ai-welcome">
        <div class="ai-welcome-hero">
          <h3>您好，我是智能舆情分析助手！</h3>
          <p>通过自然语言对话，为您提供一站式的深度分析服务。我具备以下核心能力：</p>
          <div class="ai-caps">
            <div class="ai-cap" data-preset="帮我梳理一下当前舆情热点事件">
              <div class="ai-cap-label">社会舆情问答</div>
              <div class="ai-cap-sub">社会事件、热点话题等</div>
            </div>
            <div class="ai-cap" data-preset="请对当前监测数据进行全流程智能分析">
              <div class="ai-cap-label">全流程智能分析</div>
              <div class="ai-cap-sub">从查理解到深度分析</div>
            </div>
            <div class="ai-cap" data-preset="请从多维度洞察当前舆情数据">
              <div class="ai-cap-label">多维度数据洞察</div>
              <div class="ai-cap-sub">媒体观点、事件走势等</div>
            </div>
            <div class="ai-cap" data-preset="请将当前舆情分析结果可视化总结">
              <div class="ai-cap-label">可视化总结</div>
              <div class="ai-cap-sub">将数据转化为图表分析</div>
            </div>
          </div>
        </div>
        <div class="ai-presets-label">您也可以这样问我：</div>
        <div class="ai-preset-list">
          <div class="ai-preset-item" data-preset="近24小时舆情速递">
            近24小时舆情速递
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none"><path d="M9 18l6-6-6-6" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>
          </div>
          <div class="ai-preset-item" data-preset="总结某事件在社交平台上网民的情绪分布">
            总结某事件在社交平台上网民的情绪分布
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none"><path d="M9 18l6-6-6-6" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>
          </div>
          <div class="ai-preset-item" data-preset="新疆棉的风险分析与研判建议">
            新疆棉的风险分析与研判建议
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none"><path d="M9 18l6-6-6-6" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>
          </div>
          <div class="ai-preset-item" data-preset="大埔宏福苑大火事件概述与舆情分析">
            大埔宏福苑大火事件概述与舆情分析
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none"><path d="M9 18l6-6-6-6" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>
          </div>
        </div>
      </div>

      <!-- 对话区 -->
      <div class="ai-chat" id="ai-chat" style="display:none;"></div>
    </div>

    <!-- 功能模式切换 -->
    <div class="ai-mode-tabs">
      <button class="ai-mode-tab active">AI问答</button>
      <button class="ai-mode-tab">事件分析</button>
    </div>
    <!-- 输入区 -->
    <div class="ai-input-area">
      <div class="ai-input-box">
        <textarea id="ai-ta" rows="3" placeholder="需要我做什么？可输入舆情事件，快速掌握传播趋势"></textarea>
        <button class="ai-send" id="ai-send">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none">
            <path d="M22 2L11 13M22 2l-7 20-4-9-9-4 20-7z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </button>
      </div>
      <div class="ai-tool-row">
        <button class="ai-tool-pill" id="ai-deep">
          <svg width="12" height="12" viewBox="0 0 24 24" fill="none"><circle cx="12" cy="12" r="9" stroke="currentColor" stroke-width="1.8"/><path d="M12 7v5l3 3" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></svg>
          深度思考
        </button>
        <button class="ai-tool-pill" id="ai-web">
          <svg width="12" height="12" viewBox="0 0 24 24" fill="none"><circle cx="12" cy="12" r="9" stroke="currentColor" stroke-width="1.8"/><path d="M2 12h20M12 2c-2 3-3 6-3 10s1 7 3 10M12 2c2 3 3 6 3 10s-1 7-3 10" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></svg>
          联网搜索
        </button>
        <button class="ai-clear-btn" id="ai-clear">清空对话</button>
      </div>
    </div>
  `;
  document.body.appendChild(panel);

  /* ── Panel header cursor set to default (no drag) ── */
  const ph = document.getElementById('ai-ph');
  ph.style.cursor = 'default';

  /* ════════════════════════════ OPEN / CLOSE ════════════════════════════ */
  /* 点击遮罩关闭面板 */
  const overlay = document.createElement('div');
  overlay.id = 'ai-overlay';
  overlay.style.cssText = 'position:fixed;inset:0;right:400px;z-index:9998;display:none;cursor:default;';
  overlay.addEventListener('click', function () { closePanel(); });
  document.body.appendChild(overlay);

  function openPanel() {
    if (S.open) return;
    S.open = true;
    positionPanel();
    panel.classList.add('ai-open');
    overlay.style.display = 'block';
  }
  function closePanel() {
    S.open = false;
    panel.classList.remove('ai-open');
    overlay.style.display = 'none';
  }
  function togglePanel() {
    S.open ? closePanel() : openPanel();
  }

  function positionPanel() {
    // Panel is fixed at top:0, right:0, full height — no positioning needed
  }

  document.getElementById('ai-close-btn').addEventListener('click', closePanel);
  document.getElementById('ai-min-btn').addEventListener('click', closePanel);

  /* ════════════════════════════ TOOL TOGGLES ════════════════════════════ */
  document.getElementById('ai-deep').addEventListener('click', function () {
    S.deepThink = !S.deepThink;
    this.classList.toggle('on', S.deepThink);
  });
  document.getElementById('ai-web').addEventListener('click', function () {
    S.webSearch = !S.webSearch;
    this.classList.toggle('on', S.webSearch);
  });
  panel.querySelectorAll('.ai-mode-tab').forEach(function (btn) {
    btn.addEventListener('click', function () {
      panel.querySelectorAll('.ai-mode-tab').forEach(function (b) { b.classList.remove('active'); });
      btn.classList.add('active');
    });
  });
  document.getElementById('ai-clear').addEventListener('click', function () {
    S.inChat = false; S.contextData = null;
    document.getElementById('ai-welcome').style.display = '';
    const chat = document.getElementById('ai-chat');
    chat.style.display = 'none'; chat.innerHTML = '';
    // Remove any ctx card
    const ctx = panel.querySelector('.ai-ctx-card');
    if (ctx) ctx.remove();
  });

  /* ════════════════════════════ PRESET CLICK ════════════════════════════ */
  panel.addEventListener('click', function (e) {
    var preset = e.target.closest('[data-preset]');
    if (preset) submitMessage(preset.dataset.preset);
  });

  /* ════════════════════════════ TEXTAREA ════════════════════════════ */
  var ta = document.getElementById('ai-ta');
  ta.addEventListener('input', function () {
    this.style.height = 'auto';
    this.style.height = Math.min(this.scrollHeight, 80) + 'px';
  });
  ta.addEventListener('keydown', function (e) {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      var v = this.value.trim();
      if (v) submitMessage(v);
    }
  });
  document.getElementById('ai-send').addEventListener('click', function () {
    var v = ta.value.trim();
    if (v) submitMessage(v);
  });

  /* ════════════════════════════ ENTER CHAT ════════════════════════════ */
  function enterChat(ctxHtml) {
    S.inChat = true;
    document.getElementById('ai-welcome').style.display = 'none';
    var chat = document.getElementById('ai-chat');
    chat.style.display = 'flex';

    if (ctxHtml) {
      // Insert context card before chat area
      var existing = panel.querySelector('.ai-ctx-card');
      if (!existing) {
        var card = document.createElement('div');
        card.className = 'ai-ctx-card';
        card.innerHTML = ctxHtml;
        var pb = document.getElementById('ai-pb');
        pb.insertBefore(card, chat);
      }
    }
  }

  /* ════════════════════════════ SUBMIT MESSAGE ════════════════════════════ */
  function submitMessage(text) {
    if (!text || S.streaming) return;
    if (!S.open) openPanel();
    if (!S.inChat) enterChat(null);

    var chat = document.getElementById('ai-chat');
    var now  = new Date().toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' });

    // User bubble
    var uDiv = document.createElement('div');
    uDiv.className = 'ai-msg user';
    uDiv.innerHTML = '<div class="ai-bubble">' + esc(text) + '</div><div class="ai-msg-time">' + now + '</div>';
    chat.appendChild(uDiv);

    // Typing indicator
    var tDiv = document.createElement('div');
    tDiv.className = 'ai-msg bot ai-typing-wrap';
    tDiv.innerHTML = '<div class="ai-typing"><span></span><span></span><span></span></div>';
    chat.appendChild(tDiv);
    scrollBottom();

    // Clear input
    ta.value = ''; ta.style.height = 'auto';
    S.streaming = true;

    var delay = S.deepThink ? 2400 : 900;
    setTimeout(function () {
      tDiv.remove();
      var resp = generateResponse(text);
      var bDiv = document.createElement('div');
      bDiv.className = 'ai-msg bot';
      var bubble = document.createElement('div');
      bubble.className = 'ai-bubble';
      var timeEl = document.createElement('div');
      timeEl.className = 'ai-msg-time';
      timeEl.textContent = new Date().toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' });
      bDiv.appendChild(bubble);
      bDiv.appendChild(timeEl);
      chat.appendChild(bDiv);
      scrollBottom();
      streamText(bubble, resp, function () { S.streaming = false; scrollBottom(); });
    }, delay);
  }

  /* ════════════════════════════ STREAM TEXT ════════════════════════════ */
  function streamText(el, text, done) {
    var chars = Array.from(text), i = 0;
    el.textContent = '';
    var iv = setInterval(function () {
      if (i >= chars.length) { clearInterval(iv); if (done) done(); return; }
      var chunk = Math.floor(Math.random() * 2) + 1;
      el.textContent += chars.slice(i, i + chunk).join('');
      i += chunk;
      scrollBottom();
    }, 48);
  }

  function scrollBottom() {
    var pb = document.getElementById('ai-pb');
    pb.scrollTop = pb.scrollHeight;
  }

  function esc(str) {
    var d = document.createElement('div');
    d.textContent = str; return d.innerHTML;
  }

  /* ════════════════════════════ MOCK LLM RESPONSES ════════════════════════════ */
  function generateResponse(text) {
    // Demo mode: always return 香港大埔宏福苑大火 report
    S.contextData = null;
    return '【香港大埔宏福苑大火事件舆情分析报告】\n事件类型：突发公共安全事件 · 风险等级：■■■■□ 高风险（4.3/5）\n报告时间：2025年11月26日 15:20\n━━━━━━━━━━━━━━━━━━━━\n\n一、事件概述\n2025年11月26日下午约14:51，香港大埔区大埔墟宏福苑一幢高层住宅外墙棚架突发起火，浓烟迅速蔓延，现场视频在社交平台迅速扩散。香港消防处接报后约8分钟内到达现场，共调派7辆消防车及47名消防员全力处置，明火于04:15完全扑灭，历时约1.5小时。\n\n据香港消防处初步通报：事故造成2人轻伤，另有数十名居民已紧急疏散。起火原因正由消防处调查总队介入调查，初步怀疑为外墙棚架电焊施工引发，最终结论尚待公布。起火楼栋外墙正进行大规模维修工程，承建商于凌晨施工安排引发居民强烈质疑，相关棚架搭建安全是否符合屋宇署规范已引发舆论高度关注。\n\n二、数据概览\n▸ 监测信息总量：7.8万条（事发后6小时内）\n▸ 综合热度指数：88.6 / 100（高位，持续攀升中）\n▸ 情感分布：负面 67.3% / 中性 24.1% / 正面 8.6%\n▸ Facebook话题阅读量：1.1亿（截至报告时间）\n▸ 连登讨论区帖子量：2,800+帖（高峰排名第2位）\n\n三、传播分析\n▸ 起爆平台：Facebook（现场视频于03:01首发，30分钟内传播破圈）\n▸ 主要渠道：Facebook（44%）> 连登/高登（22%）> Instagram（18%）> 微博（10%）> 其他（6%）\n▸ 高峰时段：07:00—09:00（早高峰信息量占全天47%）\n▸ 关键传播节点：3名粉丝超10万的港系KOL于03:30前已转发现场视频\n▸ 本地媒体：香港01、星岛日报、明报于06:00前均已发布图文报道\n▸ 湾区媒体跟进：南方都市报、广州日报于08:00同步转载，关注消防处置表现\n▸ 境外媒体：Reuters中文、BBC中文同步跟进，暂未出现明显负面放大\n\n四、关键声音\n▸ 【主要负面声音】\n  · 居民质疑施工单位深夜作业引发安全事故，追责承建商与屋宇署监管失职（占负面41%）\n  · 棚架搭建安全标准存漏洞，引申至全港楼宇维修工程安全监管议题（29%）\n  · 部分网民质疑消防处接报至到场的响应时间（18%）\n  · 深夜浓烟导致居民疏散困难，批评大厦缺乏有效预警机制（12%）\n\n▸ 【主要中立声音】\n  · 记录现场救援过程，转播消防员专业行动\n  · 科普火灾逃生知识（相关内容互动量较高）\n\n▸ 【主要正面声音】\n  · 肯定消防处人员响应速度及专业处置表现\n  · 感谢邻居在凌晨互相呼救、协助疏散的善举\n\n五、风险预警\n▸ 短期风险（24h内）：消防处调查结论与屋宇署表态将引发第二波舆论浪潮\n▸ 中期风险（72h内）：若调查指向承建商违规施工，问责舆情将持续升温\n▸ 长期风险：事件极可能引发全港「楼宇维修棚架安全」议题连锁讨论，存在政策层面舆论压力\n▸ 谣言预警：已发现1条不实信息流传（虚报伤亡数字），需立即介入处置\n\n六、引导建议（面向紫荆杂志社编辑记者）\n① 报道角度：以消防处专业响应与居民邻里互助为主线，突显香港社会韧性与应急能力，避免过度聚焦伤亡数字引发情绪化二次传播\n② 深度选题：调查香港楼宇维修工程安全监管机制，以本次棚架起火为切入点，采访屋宇署官员与建造业议会，梳理现行制度防线与监管盲点\n③ 引导策略：在Facebook与Instagram平台主动发布消防安全科普内容，借助本次事件热度占位正向议题，引导公众关注由恐慌转向行动（申报楼宇检查、了解疏散须知）\n④ 时机建议：在消防处发布调查初步结论后（预计24—48小时内），第一时间跟进发布解读稿，确保紫荆在权威解读赛道抢占首发位置\n⑤ 后续跟踪：持续监测屋宇署整改承诺落实情况，规划「事件一个月后」回访选题，保持读者黏性与议题热度';
    // Legacy branches archived below (unreachable)
    if (S.contextData && S.contextData.length > 0) {
      var n = S.contextData.length;
      var ts = new Date().toLocaleString('zh-CN', {year:'numeric',month:'2-digit',day:'2-digit',hour:'2-digit',minute:'2-digit'});
      var resp = '【批量数据深度分析报告】\n共分析 ' + n + ' 条数据 · 生成时间：' + ts + '\n━━━━━━━━━━━━━━━━━━━━\n\n';
      resp += '一、基本研判\n';
      resp += '▸ 风险等级：■■■□□ 中高风险（3.4/5）\n';
      resp += '▸ 综合热度：78.2 / 100（已超高风险阈值75）\n';
      resp += '▸ 影响范围：全国性议题，一线城市传播密度最高\n\n';
      resp += '二、情感倾向分析\n';
      resp += '▸ 负面情绪：61.2%（高于预警阈值60%）\n';
      resp += '▸ 中性情绪：26.8%\n';
      resp += '▸ 正面情绪：12.0%\n';
      resp += '负面主要集中于：政策执行质疑（43%）、处置效率不满（31%）、机构公信力质疑（26%）\n\n';
      resp += '三、传播特征分析\n';
      resp += '▸ 传播速度：峰值期每小时新增4,200+条，属高传播速率事件\n';
      resp += '▸ 渠道占比：微博（42%）> 微信（28%）> 抖音（18%）> 其他（12%）\n';
      resp += '▸ 关键节点：3个百万粉账号已转发，存在二次扩散风险\n';
      resp += '▸ 境外联动：路透社、BBC中文网已有跟进，需高度关注\n\n';
      resp += '四、风险预测\n';
      resp += '▸ 24h内：热度维持高位，日增幅预计15-25%\n';
      resp += '▸ 72h内：若无官方回应，负面将持续积累，存在爆发风险\n';
      resp += '▸ 长期：该议题具有周期性复发特征，需建立长效监测机制\n\n';
      resp += '五、处置建议（按优先级）\n';
      resp += '① 即时（0-2h）：发布官方声明，明确表态，阻断负面蔓延\n';
      resp += '② 短期（2-12h）：协调权威媒体发布深度解读，逐一澄清误解\n';
      resp += '③ 中期（12-24h）：联系主要平台标注虚假信息，降低算法推荐权重\n';
      resp += '④ 持续（24h后）：建立专项监测方案，每日生成舆情简报直至热度回落';
      S.contextData = null;
      return resp;
    }

    var t = text;

    if (/新能源汽车|舆情走势|近三天/.test(t)) {
      return '【"新能源汽车"三日舆情走势分析报告】\n监测周期：近3日 · 信息总量：12.4万条\n━━━━━━━━━━━━━━━━━━━━\n\n一、整体态势\n三日呈"低开—高峰—回落"走势，综合热度日均76.3（高关注区间）。\n\n二、分日详情\n\n【第1日】信息量：3.2万 / 风险：低\n▸ 话题聚焦品牌降价竞争，情绪以讨论为主\n▸ 情感：正面32% / 中性45% / 负面23%\n▸ 主要声音：消费者对价格战持续期望，媒体分析市场格局\n\n【第2日】信息量：5.8万 ↑81% / 风险：高危\n▸ 头部品牌道路安全事故，抖音播放量突破8000万\n▸ 情感：正面9% / 中性44% / 负面47%\n▸ 关键节点：@央视新闻、@人民日报跟进，15个大V转发\n▸ 境外联动：路透社发布英文报道，标题带负面倾向\n\n【第3日】信息量：3.4万 ↓41% / 风险：中\n▸ 厂家声明并启动召回，舆论部分平息\n▸ 情感：正面21% / 中性52% / 负面27%\n▸ 仍有12.4%声音对召回诚意持质疑\n\n三、传播路径\n事故视频（抖音）→ 大V转发（微博）→ 主流媒体跟进 → 境外媒体引用\n3个账号贡献总传播量38%（均为科技/汽车垂类大V）\n\n四、风险研判\n▸ 短期：召回执行进展将成新一轮舆情触发点，需提前预案\n▸ 中期：连带类比讨论已出现，行业整体形象存受损风险\n\n五、处置建议\n① 推动厂家公开披露召回进展，定期发布满意度报告\n② 行业协会发声，强调国内新能源整体安全标准\n③ 加大正向内容生产，以数据对比展示安全指标\n④ 建立境外媒体专项监测，防范跨语言舆情反扑';
    }

    if (/情绪分布|网民情绪/.test(t)) {
      return '【网民情绪深度分布分析报告】\n分析样本：48,621条有效互动 · 置信度：92.4%\n━━━━━━━━━━━━━━━━━━━━\n\n一、整体情绪分布\n▸ 负面情绪：48.3%（↑12.6% vs. 前7日均值）\n▸ 中性情绪：34.1%\n▸ 正面情绪：17.6%（↓8.3% vs. 前7日均值）\n\n二、负面情绪细分\n▸ 质疑与不信任：34.2%（针对机构公信力、信息透明度）\n▸ 不满与愤怒：28.7%（对处置速度与力度）\n▸ 焦虑与恐慌：21.4%（涉及自身利益关联者）\n▸ 嘲讽与戏谑：15.7%（以段子、表情包形式传播）\n\n三、平台情绪对比\n微博：负面55% / 中性28% / 正面17%（情绪最激化）\n抖音：负面61% / 中性23% / 正面16%（短视频放大效应强）\n知乎：负面32% / 中性52% / 正面16%（理性程度最高）\n微信：负面38% / 中性47% / 正面15%（理性分析文章多）\nB站：负面29% / 中性44% / 正面27%（年轻群体相对理性）\n\n四、关键意见群体画像\n▸ 强负面群体（22.1%）：30-45岁城市中产，表达欲强，影响力高\n▸ 沉默多数（41.3%）：以转发为主，情绪易受大V影响\n▸ 积极引导群体（8.4%）：官方媒体粉丝、行业从业者，质量高覆盖面有限\n\n五、情绪演化预测\n若12小时内无官方有力回应，负面情绪预计升至55-60%\n\n六、处置建议\n① 优先在微博、抖音负面高发平台部署官方回应\n② 针对"质疑与不信任"情绪，核心策略为信息公开透明\n③ 激活知乎、微信平台理性意见领袖，形成舆论对冲\n④ 对嘲讽类内容保持适当克制，避免引发二次放大';
    }

    if (/新疆棉|风险分析|研判建议/.test(t)) {
      return '【涉"新疆棉"舆情风险分析与研判报告】\n评估时间：当前 · 综合风险等级：中高（4.1/5）\n━━━━━━━━━━━━━━━━━━━━\n\n一、议题现状\n"新疆棉"议题已形成固化跨平台、跨国界舆论生态，月均活跃约2.1万条，具有突发性高峰特征，与企业选择、赛事联名、政治事件高度联动。\n\n二、主要风险维度\n\n【境外叙事风险】等级：高\n▸ 西方主流媒体已构建稳定"人权问题"叙事框架\n▸ 美联社、BBC、路透社年均发布相关报道超600篇\n▸ 境外NGO组织借助报告形式持续扩大影响\n▸ 预警：涉新疆议题与国际赛事、知名品牌联动时，传播呈指数级增长\n\n【国内舆情风险】等级：中\n▸ 民族主义情绪与品牌抵制行为高度捆绑\n▸ "支持国货"与"抵制外资"情绪并存，部分行为趋于非理性\n▸ 自媒体蹭热点普遍，低质量内容加剧信息噪音\n\n【企业连带风险】等级：中高\n▸ 任何品牌供应链涉新疆棉，均面临境外媒体点名可能\n▸ 部分企业表态不当导致国内外双向舆情夹攻\n\n三、近期触发风险点预测\n▸ 即将到来的某国际峰会可能再度将新疆议题推至外交前台\n▸ 国内某头部服装品牌新品发布，声明措辞不当将引发连锁反应\n\n四、研判建议（分级）\n\n【政府层面】\n① 主动组织外国记者实地参访，提升信息透明度\n② 在国际多边论坛系统阐述新疆棉纺织业实际情况\n\n【企业层面】\n① 预先梳理供应链信息，制定标准应对话术\n② 避免在敏感节点发布相关联名内容\n\n【监测层面】\n① 建立境外媒体"早发现"机制，在报道发酵至国内前完成预警\n② 设置中英文双语双轨监测方案';
    }

    if (/概述|基本情况|事件|梳理|热点|当前/.test(t)) {
      return '【当前舆情热点事件基本情况报告】\n报告时间：' + new Date().toLocaleString('zh-CN', {month:'2-digit',day:'2-digit',hour:'2-digit',minute:'2-digit'}) + '\n━━━━━━━━━━━━━━━━━━━━\n\n一、事件性质界定\n本轮舆情属于【政策类关联舆情事件】，涉及社会公众权益感知，具有广泛动员能力。\n综合关注度评分：81/100（高关注区间）\n\n二、事件时间轴\n▸ T+0（初现）：事件相关信息零散出现于抖音、微博，UGC内容为主\n▸ T+3h（发酵）：2名粉丝超50万意见领袖先后转发，话题量加速增长\n▸ T+8h（爆发）：微博话题阅读量突破5000万，登上热搜前10\n▸ T+12h（当前）：主流媒体跟进报道，官方尚未发布正式回应\n\n三、核心议题分布\n▸ 事件真实性争议（35%）：质疑方与支持方观点对立\n▸ 责任归因讨论（28%）：聚焦相关机构责任边界\n▸ 政策执行层面批评（22%）：连带历史类似事件对比\n▸ 解决方案征集（15%）：部分用户提出建设性意见\n\n四、当前阶段判断\n▸ 所处阶段：【传播峰值期】，处置黄金窗口\n▸ 峰值预测：若无官方介入，热度将在3-6小时内继续攀升\n▸ 衰减节点：官方发布有效声明后，24-48小时内进入消退期\n\n五、紧急处置建议\n① 立即：组建应急响应小组，启动24小时值守\n② 2小时内：发布官方初步声明，阻断情绪蔓延\n③ 12小时内：发布详细调查报告，回应核心争议点\n④ 持续：委托权威第三方参与评估，增强公众信任';
    }

    if (/互动趋势/.test(t)) {
      return '【互动趋势深度分析报告】\n统计周期：近48小时 · 数据来源：微博/微信/抖音/知乎\n━━━━━━━━━━━━━━━━━━━━\n\n一、总体互动量\n近48小时总互动：214.7万次（↑168% vs. 事件前基准值）\n▸ 转发：56.3万（↑214%）— 圈层穿透能力强\n▸ 评论：98.7万（↑173%）— 主动表达意愿高\n▸ 点赞：59.7万（↑108%）— 情感共鸣中高\n▸ 收藏：12.8万（↑89%）— 用户有持续跟踪意愿\n\n二、互动峰值时段\n▸ 第一峰值：昨日19:30—21:00（占48h总量31%）\n  触发：下班高峰 + 大V集中转发 + 算法推荐叠加\n▸ 第二峰值：昨日22:30—23:00（占48h总量11%）\n  触发：某媒体深度报道发布，引发二次讨论\n\n三、互动质量分析\n▸ 原创内容比例：18.4%（低质量转发占主流）\n▸ 长文评论（>100字）：23.7%（深度参与）\n▸ 前100条高赞评论中，负面内容占71%\n▸ 异常账号嫌疑：约3.2%互动存在高频重复特征\n\n四、跨平台对比\n微博：98.4万 ↑201% （转发/评论/话题）\n抖音：67.2万 ↑187% （视频评论/弹幕/合拍）\n微信：32.1万 ↑94%  （公众号留言/朋友圈）\n知乎：17.0万 ↑143% （长问答/深度分析）\n\n五、未来趋势预测\n若官方24h内发布有效回应：互动量预计12-18h后快速回落\n若官方保持沉默：明日14:00-18:00将出现第三次峰值（周期性规律），风险等级将升至高危';
    }

    if (/媒体曝光/.test(t)) {
      return '【媒体曝光矩阵趋势分析报告】\n统计时间：近72小时\n━━━━━━━━━━━━━━━━━━━━\n\n一、整体曝光量\n72小时内相关报道总量：4,826篇/条\n曝光趋势：呈"爬坡—陡升—平台"三阶段曲线\n\n二、分媒体类型分析\n\n【中央级媒体】\n▸ 人民日报：2篇（基调：正向引导，聚焦积极应对侧面）\n▸ 新华社：3篇（中性客观，提供事实背景）\n▸ 央视新闻：1则推送（触达中老年群体为主）\n▸ 定性：中央媒体报道克制，基调稳健，为官方提供舆论缓冲\n\n【商业媒体与自媒体】\n▸ 腾讯/今日头条：推荐素材128篇，标题情绪化程度较高\n▸ 澎湃新闻：深度调查1篇，阅读46万，评论2,800+，负面引导明显\n▸ 头部自媒体（10万+）：23篇，批评性视角为主，论据相对充分\n\n【境外媒体】\n▸ 路透社：英文报道2篇，引用未经核实"知情人士"信源\n▸ BBC中文：1篇，带有惯用负面叙事框架\n▸ 彭博社：1篇财经角度分析，影响投资者情绪\n▸ 境外媒体国内二次传播量约4,200次，处于监控临界值\n\n三、报道情感极性\n负面：48.2% · 中性：38.7% · 正面：13.1%\n\n四、媒体应对建议\n① 向澎湃、财新等高影响力媒体提供独家深度资料，引导报道角度\n② 对路透社等失实内容，通过官方外文账号发布声明回应\n③ 协调行业协会发布联合声明，增加正面报道来源多元化';
    }

    if (/可视化|图表/.test(t)) {
      return '【舆情可视化分析摘要】\n━━━━━━━━━━━━━━━━━━━━\n\n📊 情感极性分布\n负面 48.3% ██████████▒▒▒▒▒▒▒▒▒▒\n中性 34.1% ███████▒▒▒▒▒▒▒▒▒▒▒▒▒\n正面 17.6% ████▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒\n\n📈 72小时信息量趋势\n第1个12h：3,200条（基础量）\n第2个12h：8,700条 ↑172%（开始发酵）\n第3个12h：15,400条 ↑77%（爆发峰值）\n第4个12h：12,800条 ↓17%（高位回落）\n第5个12h：9,200条 ↓28%（进入消退）\n第6个12h：7,100条 ↓23%（趋于平稳）\n\n📱 平台来源分布\n微   博：42% ████████████\n微   信：28% ████████\n抖   音：18% █████\n新闻网站：8%  ██\n其   他：4%  █\n\n🗺️ 地域热度 Top 5\n1. 广东省：93.2\n2. 北京市：88.7\n3. 上海市：85.4\n4. 浙江省：79.1\n5. 江苏省：74.8\n\n⏰ 活跃时段\n最高峰：19:00-21:00（日均量38%）\n次高峰：12:00-13:00（日均量22%）\n低谷期：02:00-07:00（日均量4%）\n\n注：正式接入大模型后将以交互式图表动态渲染。';
    }

    if (/全流程|深度分析|智能分析/.test(t)) {
      return '【全流程舆情智能分析报告】\n置信度：91.3% · 生成时间：' + new Date().toLocaleString('zh-CN', {month:'2-digit',day:'2-digit',hour:'2-digit',minute:'2-digit'}) + '\n━━━━━━━━━━━━━━━━━━━━\n\n一、监测阶段\n▸ 覆盖平台：28个主流平台（含10个境外平台）\n▸ 关键词命中：87组监测词条，有效数据累计12.4万条\n▸ 数据质量：去重后有效样本率82.6%，机器账号过滤率17.4%\n\n二、分析阶段\n▸ NLP情感分析：基于中文BERT模型，准确率92.4%\n▸ 传播图谱：识别核心传播节点213个，关键路径7条\n▸ 内容聚类：12.4万条归纳为14个议题簇，Top3覆盖总量71%\n▸ 意见领袖：发现47个高影响力账号（粉丝>10万），蓝V认证12个\n\n三、研判阶段\n▸ 当前热度：78.4/100（已超高风险阈值75）\n▸ 风险等级：中高（4.1/5），需立即介入\n▸ 横向对比：与近12个月同类事件相比，传播速度快于均值67%\n▸ AI预测：未来24h热度将在75-85区间内运行（80%置信区间）\n▸ 关键风险时段：明日14:00-17:00为下次峰值高发窗口\n\n四、处置阶段（建议方案）\n▸ 紧急（0-2h）：官方初步声明（建议200-400字，用词经情绪分析优化）\n▸ 重要（2-8h）：协调人民日报、新华社发布深度解读，形成权威矩阵\n▸ 常规（8-24h）：在微博、抖音部署原生内容引导，稀释负面内容占比\n▸ 长效（24h后）：建立专项监测，每6小时输出一次舆情快报\n\n五、效果预测\n方案落地后：预计72h内热度回落至50以下，负面情绪降至35%以内\n（参考：历史同类事件处置成功率76%）';
    }

    if (/多维度|数据洞察/.test(t)) {
      return '【多维度舆情数据洞察报告】\n━━━━━━━━━━━━━━━━━━━━\n\n一、时间维度\n▸ 工作日峰值：07:30-08:30（通勤）/ 12:00-13:00（午休）/ 19:00-22:00（晚间）\n▸ 周末特征：信息量↓35%，但单条内容互动量更高\n▸ 节假日效应：敏感议题传播速度加快，需提前启动假日值班机制\n▸ 当前时点评估：19:00-22:00传播效率是其余时段的2.8倍\n\n二、地域维度\n一线城市：介入早，意见领袖密集，情绪更多元理性\n二线城市：转发行为活跃，情绪更极化，是负面快速扩散主要区域\n三四线城市：参与量少，但一旦介入群体化特征明显\n地域敏感性Top3：广东（涉港澳）/ 新疆西藏（涉民族宗教）/ 东北（涉工业）\n\n三、群体维度\n▸ 高校学生（18-24岁）：参与活跃，情绪化表达倾向高，易受群体压力\n▸ 城市中产（25-40岁）：负面评价主力，逻辑性强，难以简单情绪引导\n▸ 退休群体（55岁+）：通过微信朋友圈传播，核实能力弱，易被谣言利用\n▸ 行业从业者：关注度高声量小，是专业辟谣的重要力量\n\n四、内容维度\n▸ 传播效率：短视频（3.6x）> 图文（1.8x）> 纯文字（1.0x）\n▸ 标题情绪化内容点击率比平和标题高187%\n▸ 内容寿命：视频72h / 图文36h / 纯文字12h\n▸ 本次事件检测到4条主要谣言，共传播23,400次，已锁定源头账号\n\n五、综合建议\n① 在工作日19:00前完成关键声明发布，利用高峰期扩大正向覆盖\n② 优先在广东、浙江、北京开展属地化回应，遏制地域扩散\n③ 针对城市中产，采用数据+案例的理性沟通策略\n④ 部署短视频形式辟谣内容，在抖音、B站进行正向内容占位';
    }

    if (/大埔|宏福苑|大火|火灾|火警/.test(t)) {
      return '【大埔宏福苑大火事件舆情分析报告】\n事件类型：突发公共安全事件 · 风险等级：■■■■□ 高风险（4.3/5）\n报告时间：2025年11月27日 14:22\n━━━━━━━━━━━━━━━━━━━━\n\n一、事件概述\n2025年11月26日约14:52，广东省梅州市大埔县大埔镇宏福苑居民楼B座发生火灾。起火楼层为3楼，火势迅速蔓延至4至7楼，现场浓烟弥漫。消防部门接警后于约10分钟内到达现场，调派5辆消防车、32名消防员全力处置，明火于04:15完全扑灭，历时约1.5小时。\n\n据官方初步通报：事故造成9人遇难、14人受伤（其中3人伤势较重），另有数十名居民紧急疏散。起火原因已由消防调查部门介入开展调查，初步排査电气线路老化所致可能性较高，最终结论尚待公布。\n\n事发楼栋建于2003年，属早期商品住宅，小区整体消防设施存在一定老化问题，楼道逃生通道部分堵塞情况已引发舆论关注。\n\n二、数据概览\n▸ 监测信息总量：7.8万条（事发后6小时内）\n▸ 综合热度指数：88.6 / 100（高位，持续攀升中）\n▸ 情感分布：负面 67.3% / 中性 24.1% / 正面 8.6%\n▸ 微博话题#大埔宏福苑火灾#阅读量：2.3亿（截至报告时间）\n▸ 微博热搜峰值排名：第3位（持续约4小时）\n\n三、传播分析\n▸ 起爆平台：抖音（现场视频于02:58首发，30分钟内播放量破500万）\n▸ 主要渠道：抖音（44%）> 微博（33%）> 微信（16%）> 其他（7%）\n▸ 高峰时段：06:00—09:00（早高峰信息量占全天47%）\n▸ 关键传播节点：3名粉丝超百万的粤系大V 03:30前已转发现场视频\n▸ 主流媒体：南方日报、羊城晚报、新京报于06:00前均已发布图文报道\n▸ 央媒跟进：人民日报客户端、央视新闻于07:30发布现场图文，定性较为克制\n▸ 境外媒体：香港01、星岛日报同步跟进，暂未出现明显负面放大\n\n四、关键声音\n▸ 【主要负面声音】\n  · 居民楼消防设施老化"无人管"，追责物业与监管部门（占负面39%）\n  · 逃生通道被堵引发公众恐慌，引申至全国社区消防隐患话题（27%）\n  · 伤亡人数信息不一致，质疑官方通报透明度（21%）\n  · 深夜发生、人员熟睡，批评消防演练覆盖不足（13%）\n\n▸ 【主要中立声音】\n  · 记录现场救援过程，转播消防员行动\n  · 科普火灾逃生知识（相关内容互动量较高）\n\n▸ 【主要正面声音】\n  · 肯定消防员响应速度及专业处置\n  · 感谢邻居在凌晨互相呼救的善举\n\n五、风险预警\n▸ 短期风险（24h内）：伤亡人数更新、遇难者身份披露将引发第二波情绪爆发\n▸ 中期风险（72h内）：若调查结论指向消防验收/物业管理失职，问责舆情将持续升温\n▸ 长期风险：事件极可能引发全国性"老旧小区消防隐患"议题连锁讨论，存在政策舆论压力\n▸ 谣言预警：已发现2条不实信息流传（虚报死亡人数、伪造"幸存者"采访视频），需立即介入处置\n\n六、处置建议\n① 即时（0-2h）：地方政府于今日上午发布正式新闻发布会，公布权威伤亡数据，阻断谣言\n② 短期（2-12h）：积极披露救援进展、伤者救治情况及遇难者家属安置方案，回应"透明度"质疑\n③ 中期（12-48h）：将消防调查进展纳入定期通报，避免信息真空引发二次舆情\n④ 专项行动：组织全市老旧住宅消防安全自查，并公开时间表，将负面舆情转化为治理行动能量\n⑤ 谣言处置：联系微博、抖音平台对已识别的2条不实信息进行标注下架，并发布辟谣声明';
    }

    // Generic fallback
    return '【智能分析回复】\n问题：' + text.slice(0, 30) + (text.length > 30 ? '…' : '') + '\n━━━━━━━━━━━━━━━━━━━━\n\n已接收您的提问，正基于当前舆情数据库进行匹配分析。\n\n初步判断：该议题当前关注度处于中等偏上水平（热度指数约62/100），在近期同话题讨论中呈活跃态势。\n\n建议您进一步明确以下分析维度，以获得更精准的报告：\n▸ 时间范围（近24h / 近7天 / 近30天）\n▸ 重点平台（全平台 / 微博 / 微信 / 抖音）\n▸ 分析重点（情感分布 / 传播路径 / 风险研判 / 处置建议）\n\n快捷指令参考：\n• "分析走势" → 话题热度趋势报告\n• "情绪分布" → 网民情感分布分析\n• "全流程分析" → 综合深度分析报告\n• "风险研判" → 综合风险等级评估';
  }

  /* ════════════════════════════ MODE 1: OPEN WITH DATA ════════════════════════════ */
  window.addEventListener('ai:open-with-data', function (e) {
    var data = (e.detail && e.detail.length) ? e.detail : [];
    S.contextData = data.length ? data : null;

    openPanel();

    if (!S.inChat) {
      var ctxHtml = '';
      if (data.length > 0) {
        ctxHtml  = '<div class="ai-ctx-title">';
        ctxHtml += '<svg width="12" height="12" viewBox="0 0 24 24" fill="none"><path d="M9 5H7C5.9 5 5 5.9 5 7V19C5 20.1 5.9 21 7 21H17C18.1 21 19 20.1 19 19V7C19 5.9 18.1 5 17 5H15M9 5C9 5.6 9.4 6 10 6H14C14.6 6 15 5.6 15 5M9 5C9 4.4 9.4 4 10 4H14C14.6 4 15 4.4 15 5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>';
        ctxHtml += '已选择 ' + data.length + ' 条数据进行分析</div>';
        ctxHtml += data.slice(0, 3).map(function (d) { return '<div class="ai-ctx-row">' + esc(d) + '</div>'; }).join('');
        if (data.length > 3) ctxHtml += '<div class="ai-ctx-row" style="color:#9eb0c6">…等共 ' + data.length + ' 条</div>';
      }
      enterChat(ctxHtml || null);
    }

    var q = data.length > 0
      ? '请对这 ' + data.length + ' 条数据进行深度分析，包括情感倾向、传播特征和风险研判'
      : '请分析当前页面的舆情数据';
    submitMessage(q);
  });

  /* ── Public API ── */
  window.aiAssistantOpenWithData = function (dataArray) {
    window.dispatchEvent(new CustomEvent('ai:open-with-data', { detail: dataArray || [] }));
  };
  window.aiAssistantToggle = togglePanel;
  window.aiAssistantOpen  = openPanel;

})();
