# -*- coding: utf-8 -*-
"""Rebuild 首页/index.html with new hero+search+analysis layout."""
import re

with open(r'c:\Pros\ZJ0512\首页\index.html', 'r', encoding='utf-8') as f:
    original = f.read()

# ----- extract original head (CSS) and topbar -----
style_end = original.find('</style>')
main_start = original.find('<main class=')

head_css   = original[:style_end]          # everything up to (not including) </style>
topbar_str = original[style_end:main_start] # </style>…<header>…<!-- Main Content -->

# Strip any previous HOME PAGE REDESIGN CSS that may be in head_css
marker = '/* \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500 HOME PAGE REDESIGN'
m_pos = head_css.find(marker)
if m_pos == -1:
    # Try the escaped-quote version from broken previous run
    marker2 = '/* \\u2500'
    m_pos2 = head_css.find('HOME PAGE REDESIGN')
    if m_pos2 != -1:
        head_css = head_css[:head_css.rfind('/*', 0, m_pos2)]
else:
    head_css = head_css[:m_pos]

# ----- new CSS -----
NEW_CSS = '''
/* ─────────────── HOME PAGE REDESIGN ─────────────── */
.main-area.home-main{padding:0!important;background:#eef1f8}
/* Hero */
.hero-section{position:relative;background:linear-gradient(180deg,#ffffff 0%,#e6edf8 100%);overflow:hidden;display:flex;flex-direction:column;align-items:center;padding:40px 40px 0}
.hero-bg{position:absolute;bottom:0;left:50%;transform:translateX(-50%);pointer-events:none}
/* App Icons */
.app-icons-row{display:flex;justify-content:center;align-items:flex-start;gap:52px;position:relative;z-index:2;margin-bottom:36px;flex-wrap:nowrap}
.app-icon-item{display:flex;flex-direction:column;align-items:center;gap:9px;cursor:pointer;text-decoration:none;transition:transform 0.2s ease}.app-icon-item:hover{transform:translateY(-5px)}
.app-icon-box{width:68px;height:68px;border-radius:18px;display:flex;align-items:center;justify-content:center;box-shadow:0 8px 24px rgba(0,0,0,0.12),0 2px 6px rgba(0,0,0,0.07)}.app-icon-box svg{width:32px;height:32px}
.app-icon-name{font-size:13px;color:#1e2d45;font-weight:500;white-space:nowrap;text-align:center}
/* Search Card */
.search-card{width:100%;max-width:920px;background:#fff;border-radius:16px 16px 0 0;box-shadow:0 -4px 24px rgba(26,44,82,0.09);position:relative;z-index:2}
.search-card-inner{padding:22px 32px 0}
/* Tabs */
.s-tabs{display:flex;gap:2px;margin-bottom:18px;border-bottom:2px solid rgba(122,145,184,0.1);padding-bottom:0}
.s-tab{padding:9px 22px;border-radius:8px 8px 0 0;font-size:14px;font-weight:600;color:#6b7c95;cursor:pointer;border:none;background:transparent;transition:all 0.15s;position:relative;bottom:-2px;border-bottom:2px solid transparent}
.s-tab.active{background:var(--primary,#2b61f0);color:#fff;border-radius:8px 8px 0 0;border-bottom-color:transparent}
.s-tab:not(.active):hover{color:var(--primary,#2b61f0);background:rgba(43,97,240,0.05)}
/* Time Filter */
.time-filter-row{display:flex;align-items:center;gap:6px;margin-bottom:14px}
.t-btn{padding:5px 14px;border-radius:999px;border:1px solid rgba(122,145,184,0.25);background:transparent;font-size:13px;color:#6b7c95;cursor:pointer;font-family:inherit;transition:all 0.15s}.t-btn.active{background:rgba(43,97,240,0.1);border-color:var(--primary,#2b61f0);color:var(--primary,#2b61f0);font-weight:600}.t-btn:hover:not(.active){background:rgba(43,97,240,0.04)}
/* Search Input */
.s-input-row{display:flex;background:#f4f7fd;border-radius:10px;border:1.5px solid rgba(43,97,240,0.14);overflow:hidden;margin-bottom:8px;transition:border-color 0.15s}.s-input-row:focus-within{border-color:var(--primary,#2b61f0)}
.s-input-row input{flex:1;border:none;background:transparent;padding:14px 18px;font-size:15px;color:#1e2d45;outline:none}.s-input-row input::placeholder{color:#a0b0c8}
.s-btn{padding:0 28px;border:none;font-size:14px;font-weight:700;cursor:pointer;display:flex;align-items:center;gap:7px;white-space:nowrap;flex-shrink:0;font-family:inherit;transition:background 0.15s}
.s-btn.normal{background:var(--primary,#2b61f0);color:#fff}.s-btn.normal:hover{background:var(--primary-deep,#1a4ed4)}
.s-btn.ai{background:linear-gradient(135deg,#6d28d9,#9356e0);color:#fff}.s-btn.ai:hover{background:linear-gradient(135deg,#5b21b6,#7c3aed)}
.s-adv{text-align:right;font-size:12px;color:var(--primary,#2b61f0);cursor:pointer;padding:0 0 18px;font-weight:500}.s-adv:hover{text-decoration:underline}
/* Report Form */
.report-wrap{padding-bottom:0}
.report-main-box{border:1.5px solid rgba(43,97,240,0.18);border-radius:12px;padding:16px 20px;background:#f8faff;margin-bottom:10px}
.rpt-row1{display:flex;align-items:center;flex-wrap:wrap;gap:8px;font-size:14px;color:#1e2d45;margin-bottom:12px}
.rpt-subject{border:none;border-bottom:1.5px solid var(--primary,#2b61f0);background:transparent;font-size:14px;color:var(--primary,#2b61f0);font-weight:700;min-width:80px;max-width:180px;padding:2px 4px;outline:none;font-family:inherit}
.rpt-date-chip{display:inline-flex;align-items:center;gap:4px;padding:3px 10px;border:1px solid rgba(43,97,240,0.3);border-radius:6px;color:var(--primary,#2b61f0);font-size:13px;cursor:pointer;background:rgba(43,97,240,0.04);white-space:nowrap}
.rpt-desc{width:100%;border:none;background:transparent;font-size:13px;color:#6b7c95;outline:none;resize:none;min-height:36px;font-family:inherit}
.rpt-char-count{text-align:right;font-size:11px;color:#c0ccdc;margin-top:4px}
.rpt-footer{display:flex;align-items:center;gap:10px;flex-wrap:wrap;padding:10px 0 0}
.rpt-footer-btn{display:flex;align-items:center;gap:5px;font-size:13px;color:#5a6a82;cursor:pointer;border:none;background:transparent;padding:4px 10px;border-radius:6px;font-family:inherit;transition:background 0.12s}.rpt-footer-btn:hover{background:rgba(43,97,240,0.05)}
.rpt-select{font-size:13px;color:#5a6a82;border:none;background:transparent;cursor:pointer;padding:4px 8px;border-radius:6px;font-family:inherit}
.rpt-toggle-wrap{display:flex;align-items:center;gap:6px;font-size:13px;color:#5a6a82}
.rpt-toggle{width:36px;height:20px;border-radius:999px;background:var(--primary,#2b61f0);position:relative;cursor:pointer;display:inline-block;flex-shrink:0}.rpt-toggle::after{content:"";position:absolute;width:16px;height:16px;border-radius:50%;background:#fff;top:2px;right:2px;transition:right 0.15s;box-shadow:0 1px 3px rgba(0,0,0,0.2)}
.rpt-spacer{flex:1}
.rpt-send{width:36px;height:36px;border-radius:50%;background:var(--primary,#2b61f0);border:none;display:flex;align-items:center;justify-content:center;cursor:pointer;flex-shrink:0;transition:background 0.15s}.rpt-send:hover{background:var(--primary-deep,#1a4ed4)}
/* Report History */
.rpt-hist{padding:6px 0 18px}
.rpt-hist-hd{display:flex;align-items:center;justify-content:space-between;font-size:12px;color:#8a9ab8;margin-bottom:10px}
.rpt-hist-more{color:var(--primary,#2b61f0);cursor:pointer;font-weight:600}.rpt-hist-more:hover{text-decoration:underline}
.rpt-hist-row{display:flex;gap:10px;flex-wrap:wrap}
.rpt-hist-item{display:flex;align-items:center;gap:8px;padding:10px 14px;background:#f4f7fd;border:1px solid rgba(122,145,184,0.18);border-radius:8px;cursor:pointer;transition:all 0.15s;width:240px;flex:0 0 240px}
.rpt-hist-item:hover{background:#fff;border-color:rgba(43,97,240,0.25);box-shadow:0 2px 8px rgba(43,97,240,0.07)}
.rhi-ico{width:32px;height:32px;background:rgba(43,97,240,0.1);border-radius:6px;display:flex;align-items:center;justify-content:center;flex:0 0 32px}
.rhi-body{min-width:0;flex:1}
.rhi-tag{display:inline-block;font-size:10px;padding:1px 5px;border-radius:3px;background:rgba(43,97,240,0.08);color:var(--primary,#2b61f0);font-weight:700;margin-bottom:3px}
.rhi-title{font-size:13px;font-weight:600;color:#1e2d45;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;max-width:140px}
.rhi-meta{font-size:11px;color:#a0b0c8}
.rhi-status{font-size:11px;display:flex;align-items:center;gap:3px;margin-top:2px}
.rhi-status.done{color:#12a87a}.rhi-status.gen{color:#c47d10}
.rhi-dot{width:6px;height:6px;border-radius:50%;flex:0 0 6px}.rhi-status.done .rhi-dot{background:#12a87a}.rhi-status.gen .rhi-dot{background:#c47d10}
/* Analysis Section */
.analysis-section{padding:20px 40px 48px;background:#eef1f8}
.analysis-top{display:flex;align-items:center;justify-content:space-between;margin-bottom:14px}
.analysis-title{font-size:15px;font-weight:800;color:#1e2d45;display:flex;align-items:center;gap:8px}.analysis-title::before{content:"";width:4px;height:16px;border-radius:2px;background:var(--primary,#2b61f0);flex:0 0 4px}
.analysis-cards{display:grid;grid-template-columns:1fr 1.15fr 1.5fr;gap:14px}
.a-card{background:#fff;border:1px solid rgba(122,145,184,0.12);border-radius:12px;box-shadow:0 1px 6px rgba(26,44,82,0.05);overflow:hidden}
.a-card-hd{padding:12px 16px;border-bottom:1px solid rgba(122,145,184,0.08);display:flex;align-items:center;justify-content:space-between}
.a-card-title{font-size:13px;font-weight:700;color:#1e2d45}
.a-card-body{padding:14px 16px}
.df-row{display:flex;gap:6px}.df-btn{padding:3px 10px;border-radius:4px;border:1px solid rgba(122,145,184,0.2);font-size:12px;color:#6b7c95;cursor:pointer;background:transparent;font-family:inherit;transition:all 0.12s}.df-btn.active{background:var(--primary,#2b61f0);color:#fff;border-color:var(--primary,#2b61f0)}
/* Hot List */
.hot-item{display:flex;align-items:flex-start;padding:7px 0;border-bottom:1px solid rgba(122,145,184,0.07);gap:8px;cursor:pointer}.hot-item:last-child{border-bottom:none}.hot-item:hover .hot-txt{color:var(--primary,#2b61f0)}
.hot-rank{font-size:13px;font-weight:800;color:#c0ccdc;width:16px;flex:0 0 16px;text-align:center;padding-top:2px}
.hot-rank.t{color:#e04040}.hot-txt{flex:1;font-size:13px;color:#1e2d45;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.hot-heat{display:flex;align-items:center;gap:3px;font-size:12px;font-weight:700;color:#e04040;flex-shrink:0}
.hot-heat-num{color:#2b61f0}
'''

# ----- new main HTML -----
NEW_MAIN = '''  <main class="main-area home-main">

    <!-- ═══ HERO SECTION ═══ -->
    <section class="hero-section">

      <!-- Radar Background SVG -->
      <div class="hero-bg">
        <svg width="960" height="380" viewBox="0 0 960 380" fill="none" xmlns="http://www.w3.org/2000/svg">
          <circle cx="480" cy="380" r="90"  stroke="rgba(43,97,240,0.07)" stroke-width="1.5" fill="none"/>
          <circle cx="480" cy="380" r="170" stroke="rgba(43,97,240,0.06)" stroke-width="1.5" fill="none"/>
          <circle cx="480" cy="380" r="250" stroke="rgba(43,97,240,0.05)" stroke-width="1.5" fill="none"/>
          <circle cx="480" cy="380" r="340" stroke="rgba(43,97,240,0.04)" stroke-width="1.5" fill="none"/>
          <circle cx="480" cy="380" r="430" stroke="rgba(43,97,240,0.03)" stroke-width="1.5" fill="none"/>
          <circle cx="480" cy="380" r="7" fill="rgba(43,97,240,0.25)"/>
          <circle cx="480" cy="380" r="14" stroke="rgba(43,97,240,0.12)" stroke-width="1.5" fill="none"/>
        </svg>
      </div>

      <!-- App Shortcut Icons -->
      <div class="app-icons-row">

        <!-- AI智能推荐 -->
        <a class="app-icon-item" href="../监测预警/AI智能推荐/index.html">
          <div class="app-icon-box" style="background:linear-gradient(140deg,#7c3aed,#a855f7)">
            <svg viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
              <circle cx="16" cy="16" r="7" stroke="white" stroke-width="1.8" fill="none"/>
              <path d="M16 6v3M16 23v3M6 16h3M23 16h3" stroke="white" stroke-width="1.8" stroke-linecap="round"/>
              <path d="M9.2 9.2l2.1 2.1M20.7 20.7l2.1 2.1M9.2 22.8l2.1-2.1M20.7 11.3l2.1-2.1" stroke="white" stroke-width="1.5" stroke-linecap="round"/>
              <circle cx="16" cy="16" r="2.5" fill="white"/>
            </svg>
          </div>
          <span class="app-icon-name">AI智能推荐</span>
        </a>

        <!-- 热点榜单 -->
        <a class="app-icon-item" href="../监测预警/热点榜单/index.html">
          <div class="app-icon-box" style="background:linear-gradient(140deg,#0ea5e9,#2b61f0)">
            <svg viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M8 24V18M13 24V14M18 24V10M23 24V6" stroke="white" stroke-width="2" stroke-linecap="round"/>
              <path d="M20 8c0 3-2.5 5-4 6.5C14.5 16 14 17.5 14 19" stroke="rgba(255,255,255,0.65)" stroke-width="1.5" stroke-linecap="round"/>
            </svg>
          </div>
          <span class="app-icon-name">热点榜单</span>
        </a>

        <!-- 事件分析 -->
        <a class="app-icon-item" href="../事件分析/事件管理/index.html">
          <div class="app-icon-box" style="background:linear-gradient(140deg,#f43f5e,#e04040)">
            <svg viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M6 22 L11 15 L16 18 L22 10 L26 13" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              <circle cx="22" cy="9" r="4" stroke="white" stroke-width="1.5" fill="none"/>
              <circle cx="22" cy="9" r="1.5" fill="white"/>
              <path d="M6 26h20" stroke="white" stroke-width="1.5" stroke-linecap="round" opacity="0.5"/>
            </svg>
          </div>
          <span class="app-icon-name">事件分析</span>
        </a>

        <!-- 智能体编报 -->
        <a class="app-icon-item" href="../智能体编报/index.html">
          <div class="app-icon-box" style="background:linear-gradient(140deg,#4f46e5,#6366f1)">
            <svg viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
              <rect x="8" y="4" width="16" height="20" rx="2.5" stroke="white" stroke-width="1.8" fill="none"/>
              <path d="M12 10h8M12 14h8M12 18h5" stroke="white" stroke-width="1.5" stroke-linecap="round" opacity="0.85"/>
              <circle cx="23" cy="23" r="5" fill="rgba(255,255,255,0.18)" stroke="white" stroke-width="1.5"/>
              <path d="M21 23h4M23 21v4" stroke="white" stroke-width="1.5" stroke-linecap="round"/>
            </svg>
          </div>
          <span class="app-icon-name">智能体编报</span>
        </a>

        <!-- 选题线索池 -->
        <a class="app-icon-item" href="../处置引导/选题线索池/index.html">
          <div class="app-icon-box" style="background:linear-gradient(140deg,#059669,#10b981)">
            <svg viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M16 4c-4.4 0-8 3.6-8 8 0 3 1.6 5.5 4 7v3h8v-3c2.4-1.5 4-4 4-7 0-4.4-3.6-8-8-8z" stroke="white" stroke-width="1.8" fill="none"/>
              <path d="M12 22h8M13 25h6" stroke="white" stroke-width="1.5" stroke-linecap="round" opacity="0.75"/>
              <circle cx="16" cy="13" r="2.5" fill="white"/>
            </svg>
          </div>
          <span class="app-icon-name">选题线索池</span>
        </a>

        <!-- 热点话题案例库 -->
        <a class="app-icon-item" href="../知识库/热点话题案例库/index.html">
          <div class="app-icon-box" style="background:linear-gradient(140deg,#0d9488,#14b8a6)">
            <svg viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
              <rect x="5" y="7" width="10" height="19" rx="1.5" stroke="white" stroke-width="1.8" fill="none"/>
              <rect x="17" y="7" width="10" height="19" rx="1.5" stroke="white" stroke-width="1.8" fill="none"/>
              <path d="M8 11h4M8 14.5h4M8 18h4" stroke="white" stroke-width="1.4" stroke-linecap="round" opacity="0.8"/>
              <path d="M20 11h4M20 14.5h4M20 18h4" stroke="white" stroke-width="1.4" stroke-linecap="round" opacity="0.8"/>
            </svg>
          </div>
          <span class="app-icon-name">热点话题案例库</span>
        </a>

      </div><!-- /app-icons-row -->

      <!-- Search Card -->
      <div class="search-card">
        <div class="search-card-inner">

          <!-- Tabs -->
          <div class="s-tabs">
            <button class="s-tab active" id="stab-comp" onclick="switchSTab(event,'comp')">综合搜索</button>
            <button class="s-tab" id="stab-ai"   onclick="switchSTab(event,'ai')">智能搜索</button>
            <button class="s-tab" id="stab-rpt"  onclick="switchSTab(event,'rpt')">生成报告</button>
          </div>

          <!-- Panel: 综合搜索 -->
          <div class="search-panel-content" id="panel-comp">
            <div class="time-filter-row">
              <button class="t-btn" onclick="switchTime(this)">今天</button>
              <button class="t-btn active" onclick="switchTime(this)">近24小时</button>
              <button class="t-btn" onclick="switchTime(this)">近3天</button>
              <button class="t-btn" onclick="switchTime(this)">近7天</button>
              <button class="t-btn" onclick="switchTime(this)">自定义</button>
            </div>
            <div class="s-input-row">
              <input type="text" placeholder="请输入关键词，支持空格分隔"/>
              <button class="s-btn normal">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none"><circle cx="11" cy="11" r="7" stroke="white" stroke-width="2"/><path d="M16.5 16.5L21 21" stroke="white" stroke-width="2" stroke-linecap="round"/></svg>
                搜索
              </button>
            </div>
            <div class="s-adv">高级配置</div>
          </div>

          <!-- Panel: 智能搜索 -->
          <div class="search-panel-content" id="panel-ai" style="display:none">
            <div class="time-filter-row">
              <button class="t-btn" onclick="switchTime(this)">今天</button>
              <button class="t-btn active" onclick="switchTime(this)">近24小时</button>
              <button class="t-btn" onclick="switchTime(this)">近3天</button>
              <button class="t-btn" onclick="switchTime(this)">近7天</button>
              <button class="t-btn" onclick="switchTime(this)">自定义</button>
            </div>
            <div class="s-input-row">
              <svg viewBox="0 0 24 24" fill="none" width="20" height="20" style="flex-shrink:0;margin-left:16px;color:#9356e0"><circle cx="12" cy="12" r="4" stroke="currentColor" stroke-width="1.8"/><path d="M12 2v2M12 20v2M2 12h2M20 12h2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M4.93 19.07l1.41-1.41M17.66 6.34l1.41-1.41" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>
              <input type="text" placeholder="说说你想找什么？AI帮你解析"/>
              <button class="s-btn ai">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none"><path d="M12 2l2 6h6l-5 4 2 6-5-4-5 4 2-6-5-4h6z" fill="white"/></svg>
                搜索
              </button>
            </div>
            <div class="s-adv">高级配置</div>
          </div>

          <!-- Panel: 生成报告 -->
          <div class="search-panel-content" id="panel-rpt" style="display:none">
            <div class="report-wrap">
              <div class="report-main-box">
                <div class="rpt-row1">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" style="color:#9356e0;flex-shrink:0"><path d="M12 2l2 6h6l-5 4 2 6-5-4-5 4 2-6-5-4h6z" fill="currentColor"/></svg>
                  <span>请帮我生成一份关于</span>
                  <input class="rpt-subject" type="text" placeholder="事件/主题"/>
                  <span>的报告。 报告时间范围：</span>
                  <span class="rpt-date-chip">
                    <svg width="13" height="13" viewBox="0 0 24 24" fill="none"><rect x="3" y="4" width="18" height="17" rx="2" stroke="currentColor" stroke-width="1.8"/><path d="M3 9h18" stroke="currentColor" stroke-width="1.5"/><path d="M8 2v3M16 2v3" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>
                    2026-05-05 00:00:00 日
                  </span>
                  <span>至</span>
                  <span class="rpt-date-chip">
                    <svg width="13" height="13" viewBox="0 0 24 24" fill="none"><rect x="3" y="4" width="18" height="17" rx="2" stroke="currentColor" stroke-width="1.8"/><path d="M3 9h18" stroke="currentColor" stroke-width="1.5"/><path d="M8 2v3M16 2v3" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>
                    2026-05-12 15:00:05 日
                  </span>
                </div>
                <textarea class="rpt-desc" rows="2" placeholder="您可输入更多报告要求，如站在xx视角，重点分析该事件带来的负面风险等"></textarea>
                <div class="rpt-char-count">0/1000</div>
                <div class="rpt-footer">
                  <button class="rpt-footer-btn">
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none"><circle cx="12" cy="12" r="9" stroke="currentColor" stroke-width="1.8"/><path d="M2 12h20" stroke="currentColor" stroke-width="1.5"/><path d="M12 2c-3 3-4 7-4 10s1 7 4 10" stroke="currentColor" stroke-width="1.5"/><path d="M12 2c3 3 4 7 4 10s-1 7-4 10" stroke="currentColor" stroke-width="1.5"/></svg>
                    联网搜索
                  </button>
                  <select class="rpt-select"><option>中文</option><option>English</option></select>
                  <div class="rpt-toggle-wrap">
                    <span>智能规划</span>
                    <span class="rpt-toggle"></span>
                  </div>
                  <div class="rpt-spacer"></div>
                  <button class="rpt-send">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none"><path d="M22 2L11 13" stroke="white" stroke-width="2" stroke-linecap="round"/><path d="M22 2L15 22l-4-9-9-4 20-7z" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
                  </button>
                </div>
              </div>
              <!-- History -->
              <div class="rpt-hist">
                <div class="rpt-hist-hd">
                  <span>
                    <svg width="12" height="12" viewBox="0 0 24 24" fill="none" style="vertical-align:-1px;margin-right:4px"><circle cx="12" cy="12" r="9" stroke="currentColor" stroke-width="1.8"/><path d="M12 7v5l3 3" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></svg>
                    历史记录
                  </span>
                  <a class="rpt-hist-more" href="#">前往报告中心 &rsaquo;</a>
                </div>
                <div class="rpt-hist-row">
                  <div class="rpt-hist-item">
                    <div class="rhi-ico">
                      <svg width="16" height="16" viewBox="0 0 24 24" fill="none"><rect x="4" y="3" width="16" height="18" rx="2" stroke="#2b61f0" stroke-width="1.8"/><path d="M8 9h8M8 13h6" stroke="#2b61f0" stroke-width="1.5" stroke-linecap="round"/></svg>
                    </div>
                    <div class="rhi-body">
                      <div class="rhi-tag">事件报告</div>
                      <div class="rhi-title">关于榴莲报告</div>
                      <div class="rhi-meta">2026-05-10 16:49</div>
                      <div class="rhi-status gen"><span class="rhi-dot"></span>报告生成中</div>
                    </div>
                  </div>
                  <div class="rpt-hist-item">
                    <div class="rhi-ico">
                      <svg width="16" height="16" viewBox="0 0 24 24" fill="none"><rect x="4" y="3" width="16" height="18" rx="2" stroke="#2b61f0" stroke-width="1.8"/><path d="M8 9h8M8 13h6" stroke="#2b61f0" stroke-width="1.5" stroke-linecap="round"/></svg>
                    </div>
                    <div class="rhi-body">
                      <div class="rhi-tag">事件报告</div>
                      <div class="rhi-title">关于榴莲退款报告</div>
                      <div class="rhi-meta">2026-05-10 14:01</div>
                      <div class="rhi-status done"><span class="rhi-dot"></span>已完成</div>
                    </div>
                  </div>
                </div>
              </div>
            </div><!-- /report-wrap -->
          </div><!-- /panel-rpt -->

        </div><!-- /search-card-inner -->
      </div><!-- /search-card -->

    </section><!-- /hero-section -->

    <!-- ═══ ANALYSIS SECTION ═══ -->
    <section class="analysis-section">

      <div class="analysis-top">
        <div class="analysis-title">近24小时领域分析</div>
        <select class="t-btn" style="appearance:auto;padding:5px 12px;font-size:12px;color:#6b7c95;border-radius:6px">
          <option>近24小时</option>
          <option>近3天</option>
          <option>近7天</option>
        </select>
      </div>

      <div class="analysis-cards">

        <!-- 领域分布 Donut -->
        <div class="a-card">
          <div class="a-card-hd"><span class="a-card-title">领域分布</span></div>
          <div class="a-card-body" style="display:flex;align-items:center;justify-content:center;padding:10px 8px">
            <svg id="donut-svg" width="220" height="200" viewBox="0 0 220 200"></svg>
          </div>
        </div>

        <!-- 领域热点 -->
        <div class="a-card">
          <div class="a-card-hd">
            <span class="a-card-title">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" style="vertical-align:-2px;margin-right:3px"><path d="M12 2c0 5-6 8-6 13a6 6 0 0012 0c0-5-6-8-6-13z" fill="#f97316" opacity="0.85"/><circle cx="12" cy="18" r="2" fill="white"/></svg>
              领域热点
            </span>
            <div class="df-row">
              <button class="df-btn active" onclick="switchDf(this)">全国</button>
              <button class="df-btn" onclick="switchDf(this)">北京</button>
            </div>
          </div>
          <div class="a-card-body" style="padding-top:6px;padding-bottom:6px">
            <div class="hot-item"><span class="hot-rank t">1</span><span class="hot-txt">2008年5月12日四川汶川特大地震</span><span class="hot-heat"><svg width="12" height="12" viewBox="0 0 24 24" fill="#e04040"><path d="M12 2c0 5-6 8-6 13a6 6 0 0012 0c0-5-6-8-6-13z"/></svg><span class="hot-heat-num">199958</span></span></div>
            <div class="hot-item"><span class="hot-rank t">2</span><span class="hot-txt">湖南衡阳居民楼火灾致5死2伤，事故...</span><span class="hot-heat"><svg width="12" height="12" viewBox="0 0 24 24" fill="#e04040"><path d="M12 2c0 5-6 8-6 13a6 6 0 0012 0c0-5-6-8-6-13z"/></svg><span class="hot-heat-num">71112</span></span></div>
            <div class="hot-item"><span class="hot-rank t">3</span><span class="hot-txt">腾讯宣布微信访客和已读功能已烊死...</span><span class="hot-heat"><svg width="12" height="12" viewBox="0 0 24 24" fill="#e04040"><path d="M12 2c0 5-6 8-6 13a6 6 0 0012 0c0-5-6-8-6-13z"/></svg><span class="hot-heat-num">57741</span></span></div>
            <div class="hot-item"><span class="hot-rank">4</span><span class="hot-txt">5月银行存款计息未出新规</span><span class="hot-heat"><svg width="12" height="12" viewBox="0 0 24 24" fill="#e04040"><path d="M12 2c0 5-6 8-6 13a6 6 0 0012 0c0-5-6-8-6-13z"/></svg><span class="hot-heat-num">50644</span></span></div>
            <div class="hot-item"><span class="hot-rank">5</span><span class="hot-txt">2008年5月12日汶川特大地震，中国...</span><span class="hot-heat"><svg width="12" height="12" viewBox="0 0 24 24" fill="#e04040"><path d="M12 2c0 5-6 8-6 13a6 6 0 0012 0c0-5-6-8-6-13z"/></svg><span class="hot-heat-num">49260</span></span></div>
            <div class="hot-item"><span class="hot-rank">6</span><span class="hot-txt">汶川地震失去双腿舞者廖智生四胎</span><span class="hot-heat"><svg width="12" height="12" viewBox="0 0 24 24" fill="#e04040"><path d="M12 2c0 5-6 8-6 13a6 6 0 0012 0c0-5-6-8-6-13z"/></svg><span class="hot-heat-num">44925</span></span></div>
          </div>
        </div>

        <!-- 领域趋势 -->
        <div class="a-card">
          <div class="a-card-hd"><span class="a-card-title">领域趋势</span></div>
          <div class="a-card-body" style="padding:10px 12px">
            <canvas id="trend-canvas" width="420" height="170" style="width:100%;height:170px"></canvas>
          </div>
        </div>

      </div><!-- /analysis-cards -->
    </section><!-- /analysis-section -->

  </main>'''

# ----- JS -----
NEW_SCRIPT = '''<script>
// Tab switching
function switchSTab(e, id) {
  document.querySelectorAll('.s-tab').forEach(function(t){ t.classList.remove('active'); });
  e.currentTarget.classList.add('active');
  document.querySelectorAll('.search-panel-content').forEach(function(p){ p.style.display='none'; });
  document.getElementById('panel-' + id).style.display = 'block';
}
function switchTime(btn) {
  btn.closest('.time-filter-row').querySelectorAll('.t-btn').forEach(function(b){ b.classList.remove('active'); });
  btn.classList.add('active');
}
function switchDf(btn) {
  btn.closest('.df-row').querySelectorAll('.df-btn').forEach(function(b){ b.classList.remove('active'); });
  btn.classList.add('active');
}
function toggleGroup(el){
  var g = el.closest('.nav-group');
  if(g){ g.classList.toggle('collapsed'); }
}

// Donut Chart
(function renderDonut(){
  var data = [
    {name:'突发事件',pct:0.22,color:'#1e3a5f'},
    {name:'意识形态',pct:0.15,color:'#06b6d4'},
    {name:'民生保障',pct:0.14,color:'#f59e0b'},
    {name:'医疗卫生',pct:0.12,color:'#10b981'},
    {name:'教育管理',pct:0.11,color:'#0d9488'},
    {name:'住房保障',pct:0.10,color:'#f97316'},
    {name:'企业经营',pct:0.09,color:'#7c3aed'},
    {name:'文旅市场',pct:0.07,color:'#6366f1'}
  ];
  var svg = document.getElementById('donut-svg');
  if(!svg) return;
  var cx=110, cy=105, R=72, ri=46;
  var startAngle = -Math.PI/2;
  var html = '';
  data.forEach(function(d){
    var angle = d.pct * 2 * Math.PI;
    var endAngle = startAngle + angle;
    var x1=cx+R*Math.cos(startAngle), y1=cy+R*Math.sin(startAngle);
    var x2=cx+R*Math.cos(endAngle),   y2=cy+R*Math.sin(endAngle);
    var x3=cx+ri*Math.cos(endAngle),  y3=cy+ri*Math.sin(endAngle);
    var x4=cx+ri*Math.cos(startAngle),y4=cy+ri*Math.sin(startAngle);
    var lg = (angle > Math.PI) ? 1 : 0;
    var path='M'+x1.toFixed(2)+' '+y1.toFixed(2)+
             ' A'+R+' '+R+' 0 '+lg+' 1 '+x2.toFixed(2)+' '+y2.toFixed(2)+
             ' L'+x3.toFixed(2)+' '+y3.toFixed(2)+
             ' A'+ri+' '+ri+' 0 '+lg+' 0 '+x4.toFixed(2)+' '+y4.toFixed(2)+' Z';
    html += '<path d="'+path+'" fill="'+d.color+'" stroke="#fff" stroke-width="1.5"/>';
    var mid = startAngle + angle/2;
    var lx=(cx+(R+10)*Math.cos(mid)).toFixed(2), ly=(cy+(R+10)*Math.sin(mid)).toFixed(2);
    var tx=(cx+(R+26)*Math.cos(mid)).toFixed(2), ty=(cy+(R+26)*Math.sin(mid)).toFixed(2);
    var anchor = Math.cos(mid)>0 ? 'start' : 'end';
    html += '<line x1="'+lx+'" y1="'+ly+'" x2="'+tx+'" y2="'+ty+'" stroke="'+d.color+'" stroke-width="1" opacity="0.6"/>';
    html += '<text x="'+tx+'" y="'+(parseFloat(ty)+1).toFixed(2)+'" text-anchor="'+anchor+'" fill="'+d.color+'" font-size="9" font-weight="600" font-family="PingFang SC,Microsoft YaHei,sans-serif">'+d.name+'</text>';
    startAngle = endAngle;
  });
  // Center label
  html += '<text x="'+cx+'" y="'+(cy-5)+'" text-anchor="middle" fill="#1e2d45" font-size="20" font-weight="800" font-family="PingFang SC,Microsoft YaHei,sans-serif">8</text>';
  html += '<text x="'+cx+'" y="'+(cy+12)+'" text-anchor="middle" fill="#6b7c95" font-size="11" font-family="PingFang SC,Microsoft YaHei,sans-serif">领域</text>';
  svg.innerHTML = html;
})();

// Trend Line Chart
(function renderTrend(){
  var canvas = document.getElementById('trend-canvas');
  if(!canvas || !canvas.getContext) return;
  var ratio = window.devicePixelRatio || 1;
  var W = canvas.offsetWidth || 420, H = 170;
  canvas.width = W * ratio; canvas.height = H * ratio;
  var ctx = canvas.getContext('2d');
  ctx.scale(ratio, ratio);
  var pL=38,pR=10,pT=18,pB=36;
  var cW=W-pL-pR, cH=H-pT-pB;
  // 25 data points from 14:00 05-11 to 14:00 05-12 (hourly)
  var vals = [55,48,52,44,38,60,80,65,54,50,58,52,48,42,38,32,30,36,42,48,55,62,60,58,52];
  var maxV=95, minV=0;
  function sx(i){ return pL + (i/(vals.length-1))*cW; }
  function sy(v){ return pT + (1-(v-minV)/(maxV-minV))*cH; }

  // Grid lines
  ctx.strokeStyle='rgba(122,145,184,0.12)'; ctx.lineWidth=1;
  [0,20,40,60,80,95].forEach(function(v){
    var y=sy(v);
    ctx.beginPath(); ctx.moveTo(pL,y); ctx.lineTo(pL+cW,y); ctx.stroke();
    ctx.fillStyle='#9eb0c6'; ctx.font='10px PingFang SC,Microsoft YaHei,sans-serif';
    ctx.textAlign='right'; ctx.fillText(v,pL-5,y+3.5);
  });
  ctx.fillStyle='#9eb0c6'; ctx.font='10px PingFang SC,Microsoft YaHei,sans-serif';
  ctx.textAlign='center'; ctx.fillText('数值',pL-18,pT+2);

  // Vertical marker: 05-12 00:00 is at index 10 (14:00+10h)
  var mxi=10, mxX=sx(mxi);
  ctx.setLineDash([4,4]);
  ctx.strokeStyle='rgba(224,64,64,0.75)'; ctx.lineWidth=1.5;
  ctx.beginPath(); ctx.moveTo(mxX,pT); ctx.lineTo(mxX,pT+cH); ctx.stroke();
  ctx.setLineDash([]);
  ctx.fillStyle='#e04040'; ctx.font='bold 10px PingFang SC,Microsoft YaHei,sans-serif';
  ctx.textAlign='center'; ctx.fillText('05-12',mxX,pT-4);

  // Fill area
  var grad=ctx.createLinearGradient(0,pT,0,pT+cH);
  grad.addColorStop(0,'rgba(43,97,240,0.16)'); grad.addColorStop(1,'rgba(43,97,240,0)');
  ctx.beginPath();
  vals.forEach(function(v,i){ i===0?ctx.moveTo(sx(i),sy(v)):ctx.lineTo(sx(i),sy(v)); });
  ctx.lineTo(sx(vals.length-1),pT+cH); ctx.lineTo(pL,pT+cH); ctx.closePath();
  ctx.fillStyle=grad; ctx.fill();

  // Line
  ctx.strokeStyle='#3b7ef8'; ctx.lineWidth=2; ctx.lineJoin='round'; ctx.lineCap='round';
  ctx.beginPath();
  vals.forEach(function(v,i){ i===0?ctx.moveTo(sx(i),sy(v)):ctx.lineTo(sx(i),sy(v)); });
  ctx.stroke();

  // X-axis labels
  var xIdxs=[0,4,8,10,14,18,24];
  var xT=['14:00','18:00','22:00','02:00','06:00','10:00','14:00'];
  var xS=['05-11','','','05-12','','','05-12'];
  ctx.fillStyle='#9eb0c6'; ctx.font='10px PingFang SC,Microsoft YaHei,sans-serif'; ctx.textAlign='center';
  xIdxs.forEach(function(idx,k){
    if(idx>=vals.length) idx=vals.length-1;
    var x=sx(idx);
    ctx.fillText(xT[k],x,H-pB+12);
    if(xS[k]) ctx.fillText(xS[k],x,H-pB+23);
  });
})();
</script>'''

# ----- compose and write -----
result = head_css + NEW_CSS + topbar_str + NEW_MAIN + '\n' + NEW_SCRIPT + '\n</body>\n</html>'

with open(r'c:\Pros\ZJ0512\首页\index.html', 'w', encoding='utf-8') as f:
    f.write(result)

print('Done. chars:', len(result))
print('hero-section present:', 'hero-section' in result)
print('app-icons-row present:', 'app-icons-row' in result)
print('search-card present:', 'search-card' in result)
print('donut-svg present:', 'donut-svg' in result)
print('trend-canvas present:', 'trend-canvas' in result)
