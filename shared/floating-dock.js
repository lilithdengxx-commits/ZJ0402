/**
 * Floating Dock — 右侧悬浮快捷入口
 * 包含：舆情日历 / 预警中心 / AI 助手
 * 所有页面引入此文件即可，路径自动推算，无需手动配置。
 * 依赖：ai-assistant.js（同 shared/ 目录），需在本文件之前引入。
 */
(function () {
  'use strict';

  /* ══════════════════════════════════════════════════
     1. 路径推算（利用 document.currentScript.src）
  ══════════════════════════════════════════════════ */
  var _cs = document.currentScript;
  var _src = _cs ? _cs.src : '';
  var _base = '';
  if (_src) {
    var _si = _src.lastIndexOf('/shared/');
    if (_si !== -1) _base = _src.substring(0, _si + 1);
    // e.g.  file:///C:/Pros/ZJ0521/
  }
  // 目标页绝对路径
  var ALERT_URL = _base + '\u76d1\u6d4b\u9884\u8b66/\u9884\u8b66\u4e2d\u5fc3/index.html'; // 监测预警/预警中心
  var CAL_URL   = _base + '\u8206\u60c5\u65e5\u5386/index.html';                           // 舆情日历

  /* ══════════════════════════════════════════════════
     2. 当前页检测（自身页隐藏对应按钮）
  ══════════════════════════════════════════════════ */
  var _path = '';
  try { _path = decodeURIComponent(location.pathname); } catch (e) { _path = location.pathname; }
  var _isAlert = _path.indexOf('\u9884\u8b66\u4e2d\u5fc3') !== -1; // 预警中心
  var _isCal   = _path.indexOf('\u8206\u60c5\u65e5\u5386') !== -1; // 舆情日历
  var _isBigScreen = _path.indexOf('\u5927\u5c4f') !== -1;          // 态势感知大屏：不显示 Dock
  if (_isBigScreen) return;

  /* ══════════════════════════════════════════════════
     3. CSS
  ══════════════════════════════════════════════════ */
  var CSS = [
    '#app-dock-wrap{',
      'position:fixed;right:0;top:78%;transform:translateY(-50%);',
      'z-index:9997;user-select:none;',
    '}',
    /* 收起把手：绝对定位，不影响父容器高度，始终锚定右边缘 */
    '#dock-handle{',
      'position:absolute;right:0;top:0;',
      'width:26px;height:68px;',
      'background:#fff;border-radius:10px 0 0 10px;',
      'box-shadow:-3px 0 14px rgba(26,44,82,.16);',
      'display:flex;align-items:center;justify-content:center;',
      'cursor:pointer;color:#7a91b8;',
      'opacity:0;pointer-events:none;',
      'transition:background .15s,color .15s,opacity .18s;',
    '}',
    '#dock-handle:hover{background:#eef3ff;color:#2b61f0;}',
    /* 收起状态 */
    '#app-dock-wrap.dock-collapsed{pointer-events:none;}',
    '#app-dock-wrap.dock-collapsed #dock-handle{opacity:1;pointer-events:auto;}',
    '#app-dock-wrap.dock-collapsed #dock-items{',
      'transform:translateX(calc(100% + 4px));opacity:0;pointer-events:none;',
    '}',
    /* 展开面板 */
    '#dock-items{',
      'display:flex;flex-direction:column;align-items:center;',
      'gap:10px;padding:10px 10px;',
      'background:rgba(255,255,255,0.96);backdrop-filter:blur(10px);',
      'border-radius:14px 0 0 14px;',
      'box-shadow:-4px 0 24px rgba(26,44,82,.15);',
      'transition:transform .22s cubic-bezier(.4,0,.2,1),opacity .22s;',
      'transform-origin:right center;',
    '}',
    /* 收起按钮 */
    '.dock-toggle{',
      'width:30px;height:30px;border-radius:50%;',
      'background:#f0f4ff;border:1px solid rgba(43,97,240,.15);',
      'display:flex;align-items:center;justify-content:center;',
      'cursor:pointer;color:#7a91b8;transition:background .15s,color .15s;',
    '}',
    '.dock-toggle:hover{background:rgba(43,97,240,.1);color:#2b61f0;}',
    /* 功能按钮 */
    '.dock-btn{',
      'width:48px;height:48px;border-radius:14px;',
      'display:flex;align-items:center;justify-content:center;',
      'cursor:pointer;position:relative;text-decoration:none;',
      'box-shadow:0 3px 14px rgba(26,44,82,.18);',
      'transition:transform .15s,box-shadow .15s;',
      'border:none;padding:0;',
    '}',
    '.dock-btn:hover{transform:translateY(-2px);box-shadow:0 7px 20px rgba(26,44,82,.24);}',
    /* Tooltip */
    '.dock-tip{',
      'position:absolute;right:58px;top:50%;transform:translateY(-50%);',
      'background:#1e2d45;color:#fff;font-size:12px;',
      'font-family:"PingFang SC","Microsoft YaHei UI",sans-serif;',
      'padding:5px 10px;border-radius:6px;',
      'white-space:nowrap;opacity:0;pointer-events:none;transition:opacity .15s;',
    '}',
    '.dock-tip::after{',
      'content:"";position:absolute;left:100%;top:50%;transform:translateY(-50%);',
      'border:5px solid transparent;border-left-color:#1e2d45;',
    '}',
    '.dock-btn:hover .dock-tip{opacity:1;}',
    /* 颜色主题 */
    '.dock-btn-ai{background:linear-gradient(145deg,#5b8df7,#8b6bf0);}',
    '.dock-btn-alert{background:linear-gradient(145deg,#7b6cf6,#5043d1);}',
    '.dock-btn-cal{background:linear-gradient(145deg,#ffb74a,#ff8138);}',
    /* 隐藏原 ai-ball，由 Dock 代理 */
    '#ai-ball{display:none!important;}',
  ].join('');

  /* ══════════════════════════════════════════════════
     4. SVG 图标
  ══════════════════════════════════════════════════ */
  var SVG_L = '<svg width="13" height="13" viewBox="0 0 24 24" fill="none">'
    + '<path d="M15 18l-6-6 6-6" stroke="currentColor" stroke-width="2.5"'
    + ' stroke-linecap="round" stroke-linejoin="round"/></svg>';
  var SVG_R = '<svg width="13" height="13" viewBox="0 0 24 24" fill="none">'
    + '<path d="M9 18l6-6-6-6" stroke="currentColor" stroke-width="2.5"'
    + ' stroke-linecap="round" stroke-linejoin="round"/></svg>';
  var SVG_AI
    = '<svg width="26" height="26" viewBox="0 0 40 40" fill="none">'
    + '<rect x="5" y="12" width="30" height="22" rx="7" fill="white" opacity=".95"/>'
    + '<circle cx="14" cy="23" r="3.5" fill="#5b8df7"/>'
    + '<circle cx="26" cy="23" r="3.5" fill="#8b6bf0"/>'
    + '<rect x="15" y="7" width="10" height="6" rx="2.5" fill="white" opacity=".9"/>'
    + '<rect x="18.5" y="4" width="3" height="4" rx="1.5" fill="white" opacity=".88"/>'
    + '<rect x="10" y="29" width="6" height="2.5" rx="1.25" fill="#8b6bf0" opacity=".5"/>'
    + '<rect x="24" y="29" width="6" height="2.5" rx="1.25" fill="#5b8df7" opacity=".5"/>'
    + '</svg>';
  var SVG_ALERT
    = '<svg width="24" height="24" viewBox="0 0 24 24" fill="none">'
    + '<path d="M12 3C12 3 6 8 6 14h12c0-6-6-11-6-11Z"'
    + ' stroke="white" stroke-width="1.7" stroke-linejoin="round" fill="none"/>'
    + '<path d="M4 14h16" stroke="white" stroke-width="1.7" stroke-linecap="round"/>'
    + '<path d="M10 17c0 1.1.9 2 2 2s2-.9 2-2"'
    + ' stroke="white" stroke-width="1.7" stroke-linecap="round"/>'
    + '<circle cx="12" cy="6.5" r="1.2" fill="white"/>'
    + '</svg>';
  var SVG_CAL
    = '<svg width="24" height="24" viewBox="0 0 24 24" fill="none">'
    + '<rect x="3" y="4" width="18" height="18" rx="2" stroke="white" stroke-width="1.7"/>'
    + '<path d="M16 2v4M8 2v4M3 10h18" stroke="white" stroke-width="1.7" stroke-linecap="round"/>'
    + '<rect x="7" y="14" width="2.5" height="2.5" rx="0.6" fill="white"/>'
    + '<rect x="11" y="14" width="2.5" height="2.5" rx="0.6" fill="white"/>'
    + '<rect x="15" y="14" width="2.5" height="2.5" rx="0.6" fill="white"/>'
    + '</svg>';

  /* ══════════════════════════════════════════════════
     5. 构建 DOM
  ══════════════════════════════════════════════════ */
  function buildDock() {
    if (document.getElementById('app-dock-wrap')) return; // 防重复

    // Style
    var st = document.createElement('style');
    st.textContent = CSS;
    document.head.appendChild(st);

    // 外层容器
    var wrap = document.createElement('div');
    wrap.id = 'app-dock-wrap';

    // 收起把手
    var handle = document.createElement('div');
    handle.id = 'dock-handle';
    handle.title = '\u5c55\u5f00'; // 展开
    handle.innerHTML = SVG_L;
    handle.addEventListener('click', _dockExpand);
    wrap.appendChild(handle);

    // 展开面板
    var items = document.createElement('div');
    items.id = 'dock-items';

    // 收起按钮
    var tog = document.createElement('div');
    tog.className = 'dock-toggle';
    tog.title = '\u6536\u8d77'; // 收起
    tog.innerHTML = SVG_R;
    tog.addEventListener('click', _dockCollapse);
    items.appendChild(tog);

    // AI 助手
    var btnAI = document.createElement('div');
    btnAI.className = 'dock-btn dock-btn-ai';
    btnAI.innerHTML = '<span class="dock-tip">AI \u52a9\u624b</span>' + SVG_AI;
    btnAI.addEventListener('click', _dockAiClick);
    items.appendChild(btnAI);

    // 预警中心（自身页隐藏）
    if (!_isAlert) {
      var btnAlert = document.createElement('a');
      btnAlert.className = 'dock-btn dock-btn-alert';
      btnAlert.href = ALERT_URL;
      btnAlert.innerHTML = '<span class="dock-tip">\u9884\u8b66\u4e2d\u5fc3</span>' + SVG_ALERT;
      items.appendChild(btnAlert);
    }

    // 舆情日历（自身页隐藏）
    if (!_isCal) {
      var btnCal = document.createElement('a');
      btnCal.className = 'dock-btn dock-btn-cal';
      btnCal.href = CAL_URL;
      btnCal.innerHTML = '<span class="dock-tip">\u8206\u60c5\u65e5\u5386</span>' + SVG_CAL;
      items.appendChild(btnCal);
    }

    wrap.appendChild(items);
    document.body.appendChild(wrap);

    // 恢复持久化状态
    if (localStorage.getItem('dockCollapsed') === '1') {
      wrap.classList.add('dock-collapsed');
    }

    // 监听 AI 面板开关，向左让位
    _watchPanel(wrap, 0);

    // 移除顶栏舆情日历图标按钮（如存在）
    _removeCalTopbarBtn();
  }

  /* ══════════════════════════════════════════════════
     6. AI 面板联动
  ══════════════════════════════════════════════════ */
  function _watchPanel(wrap, retries) {
    var panel = document.getElementById('ai-panel');
    if (!panel) {
      if (retries < 20) setTimeout(function () { _watchPanel(wrap, retries + 1); }, 300);
      return;
    }
    new MutationObserver(function () {
      wrap.style.right = panel.classList.contains('ai-open') ? '404px' : '0';
    }).observe(panel, { attributes: true, attributeFilter: ['class'] });
  }

  /* ══════════════════════════════════════════════════
     7. 移除顶栏舆情日历按钮
  ══════════════════════════════════════════════════ */
  function _removeCalTopbarBtn() {
    var links = document.querySelectorAll('.topbar-actions a.icon-button');
    for (var i = 0; i < links.length; i++) {
      var raw = links[i].getAttribute('href') || '';
      if (raw.indexOf('\u8206\u60c5\u65e5\u5386') !== -1) {
        links[i].parentNode.removeChild(links[i]);
        break;
      }
    }
  }

  /* ══════════════════════════════════════════════════
     8. 全局控制函数（供内联 onclick 调用）
  ══════════════════════════════════════════════════ */
  function _dockCollapse() {
    var w = document.getElementById('app-dock-wrap');
    if (w) w.classList.add('dock-collapsed');
    localStorage.setItem('dockCollapsed', '1');
  }
  function _dockExpand() {
    var w = document.getElementById('app-dock-wrap');
    if (w) w.classList.remove('dock-collapsed');
    localStorage.setItem('dockCollapsed', '0');
  }
  function _dockAiClick() {
    var ball = document.getElementById('ai-ball');
    if (ball) ball.click();
  }
  window.dockCollapse = _dockCollapse;
  window.dockExpand   = _dockExpand;
  window.dockAiClick  = _dockAiClick;

  /* ══════════════════════════════════════════════════
     9. 启动
  ══════════════════════════════════════════════════ */
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', buildDock);
  } else {
    buildDock();
  }
})();
