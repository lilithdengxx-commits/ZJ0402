import re

with open(r'c:\Pros\ZJ0512\首页\index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# ── 1. 图标文字：字号加大 + 加粗 ──
content = content.replace(
    '.app-icon-name{font-size:13px;color:#1e2d45;font-weight:500;white-space:nowrap;text-align:center}',
    '.app-icon-name{font-size:15px;color:#1e2d45;font-weight:700;white-space:nowrap;text-align:center}'
)

# ── 2. 分析卡片高度拉齐 ──
content = content.replace(
    '.analysis-cards{display:grid;grid-template-columns:1fr 1fr 1.5fr;gap:14px;align-items:start}',
    '.analysis-cards{display:grid;grid-template-columns:1fr 1fr 1.5fr;gap:14px;align-items:stretch}'
)
content = content.replace(
    '.a-card{background:#fff;border:1px solid rgba(122,145,184,0.12);border-radius:12px;box-shadow:0 1px 6px rgba(26,44,82,0.05);overflow:hidden}',
    '.a-card{background:#fff;border:1px solid rgba(122,145,184,0.12);border-radius:12px;box-shadow:0 1px 6px rgba(26,44,82,0.05);overflow:hidden;display:flex;flex-direction:column}'
)
content = content.replace(
    '.a-card-body{padding:14px 16px}',
    '.a-card-body{padding:14px 16px;flex:1}'
)

# ── 3. 添加智能搜索框 CSS + keyframes ──
smart_css = """
/* ── Home Smart Search Input ── */
.home-si-row{display:flex;align-items:center;min-height:52px;padding:0 10px 0 16px;border-radius:10px;border:1px solid rgba(43,97,240,0.35);background:#fff;margin-bottom:10px;transition:border-color .15s}.home-si-row:focus-within{border-color:var(--primary,#2b61f0);box-shadow:0 0 0 3px rgba(43,97,240,0.08)}
.home-si-label{color:var(--primary,#2b61f0);font-size:14px;font-weight:700;white-space:nowrap;padding-right:14px;border-right:1.5px solid rgba(43,97,240,0.18);margin-right:14px;flex-shrink:0}
.home-si-input{flex:1;border:none;outline:none;background:transparent;color:#1e2d45;font-size:14px;font-family:inherit}.home-si-input::placeholder{color:#95a2b6}
.home-si-btn{position:relative;display:inline-grid;place-items:center;width:34px;height:34px;flex:0 0 34px;border:none;border-radius:50%;overflow:hidden;background:radial-gradient(circle at 30% 30%,#8df5ff 0%,#4d9dff 34%,#5e62ff 68%,#28306f 100%);box-shadow:0 6px 14px rgba(72,109,255,0.3);cursor:pointer;isolation:isolate;margin-left:10px;transition:transform .15s,box-shadow .15s}.home-si-btn:hover{transform:translateY(-2px);box-shadow:0 12px 22px rgba(72,109,255,0.36)}
.home-si-btn::before{content:"";position:absolute;inset:0;border-radius:50%;background:radial-gradient(circle,rgba(255,255,255,0.28) 0%,rgba(255,255,255,0.02) 66%,transparent 74%);animation:hsiPulse 1.9s ease-out infinite;z-index:0}
.home-si-btn::after{content:"";position:absolute;inset:1px;border-radius:50%;border:1px solid rgba(255,255,255,0.3);z-index:0}
.home-si-btn span{position:relative;z-index:1}
.home-si-orbit{position:absolute;inset:4px;border-radius:50%;border:1px solid rgba(255,255,255,0.5);animation:hsiRotate 2.8s linear infinite}
.home-si-core{width:9px;height:9px;border-radius:50%;background:radial-gradient(circle,#fff 0%,#c9f2ff 40%,#7fd5ff 72%,rgba(127,213,255,0.4) 100%);box-shadow:0 0 10px rgba(255,255,255,0.7)}
.home-si-adv{text-align:right;font-size:12px;color:var(--primary,#2b61f0);cursor:pointer;padding:0 0 18px;font-weight:500}.home-si-adv:hover{text-decoration:underline}
@keyframes hsiRotate{to{transform:rotate(360deg)}}
@keyframes hsiPulse{0%{opacity:.7;transform:scale(.85)}60%{opacity:.15;transform:scale(1.15)}100%{opacity:0;transform:scale(1.35)}}
"""
content = content.replace('</style>\n</head>', smart_css + '</style>\n</head>')

# ── 4. 替换 AI智能推荐 icon ──
content = content.replace(
    '''<svg viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
              <circle cx="16" cy="16" r="7" stroke="white" stroke-width="1.8" fill="none"/>
              <path d="M16 6v3M16 23v3M6 16h3M23 16h3" stroke="white" stroke-width="1.8" stroke-linecap="round"/>
              <path d="M9.2 9.2l2.1 2.1M20.7 20.7l2.1 2.1M9.2 22.8l2.1-2.1M20.7 11.3l2.1-2.1" stroke="white" stroke-width="1.5" stroke-linecap="round"/>
              <circle cx="16" cy="16" r="2.5" fill="white"/>
            </svg>''',
    '''<svg viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
              <!-- neural nodes -->
              <circle cx="16" cy="11" r="5" stroke="white" stroke-width="1.8" fill="rgba(255,255,255,0.18)"/>
              <circle cx="9" cy="23" r="3.5" stroke="white" stroke-width="1.5" fill="rgba(255,255,255,0.12)"/>
              <circle cx="23" cy="23" r="3.5" stroke="white" stroke-width="1.5" fill="rgba(255,255,255,0.12)"/>
              <path d="M13.2 14.8L10.8 20.5" stroke="white" stroke-width="1.4" stroke-linecap="round"/>
              <path d="M18.8 14.8L21.2 20.5" stroke="white" stroke-width="1.4" stroke-linecap="round"/>
              <path d="M11.5 23h9" stroke="rgba(255,255,255,0.4)" stroke-width="1.3" stroke-linecap="round"/>
              <circle cx="16" cy="11" r="2" fill="white"/>
              <!-- sparkle -->
              <path d="M25.5 5l.7 1.7 1.8.7-1.8.7L25.5 9.8l-.7-1.7-1.8-.7 1.8-.7z" fill="rgba(255,255,255,0.9)"/>
              <path d="M7 7l.4 1 1.1.4-1.1.4L7 9.8l-.4-1-1.1-.4 1.1-.4z" fill="rgba(255,255,255,0.65)"/>
            </svg>'''
)

# ── 5. 替换热点榜单 icon ──
content = content.replace(
    '''<svg viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M8 24V18M13 24V14M18 24V10M23 24V6" stroke="white" stroke-width="2" stroke-linecap="round"/>
              <path d="M20 8c0 3-2.5 5-4 6.5C14.5 16 14 17.5 14 19" stroke="rgba(255,255,255,0.65)" stroke-width="1.5" stroke-linecap="round"/>
            </svg>''',
    '''<svg viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
              <!-- bars -->
              <rect x="5" y="20" width="5.5" height="8" rx="1.5" fill="rgba(255,255,255,0.45)"/>
              <rect x="13.5" y="14" width="5" height="14" rx="1.5" fill="rgba(255,255,255,0.7)"/>
              <rect x="22" y="8" width="5" height="20" rx="1.5" fill="white"/>
              <!-- flame above tallest bar -->
              <path d="M24.5 5.5c.3 1.2 1.3 2.2 1.3 3.8a2.8 2.8 0 01-5.6 0c0-1.4.5-2.3 1-3.2-.3 1.3 0 2.3.8 3 .15-1 .5-2.3 1.5-3.6z" fill="rgba(255,255,255,0.88)"/>
              <!-- baseline -->
              <path d="M4 27.5h24" stroke="rgba(255,255,255,0.22)" stroke-width="1" stroke-linecap="round"/>
            </svg>'''
)

# ── 6. 替换事件分析 icon ──
content = content.replace(
    '''<svg viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M6 22 L11 15 L16 18 L22 10 L26 13" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              <circle cx="22" cy="9" r="4" stroke="white" stroke-width="1.5" fill="none"/>
              <circle cx="22" cy="9" r="1.5" fill="white"/>
              <path d="M6 26h20" stroke="white" stroke-width="1.5" stroke-linecap="round" opacity="0.5"/>
            </svg>''',
    '''<svg viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
              <!-- target rings -->
              <circle cx="15" cy="15" r="10" stroke="rgba(255,255,255,0.3)" stroke-width="1.3" fill="none"/>
              <circle cx="15" cy="15" r="7" stroke="rgba(255,255,255,0.55)" stroke-width="1.4" fill="none"/>
              <circle cx="15" cy="15" r="4" stroke="white" stroke-width="1.6" fill="rgba(255,255,255,0.15)"/>
              <circle cx="15" cy="15" r="2" fill="white"/>
              <!-- crosshairs -->
              <path d="M15 5v4M15 21v4M5 15h4M21 15h4" stroke="white" stroke-width="1.4" stroke-linecap="round" opacity="0.55"/>
              <!-- arrow from top-right -->
              <path d="M20 8.5L27 5l-1.5 7z" fill="rgba(255,255,255,0.8)"/>
              <path d="M21.5 9 L27 5" stroke="white" stroke-width="1.3" stroke-linecap="round" opacity="0.5"/>
            </svg>'''
)

# ── 7. 替换智能体编报 icon ──
content = content.replace(
    '''<svg viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
              <rect x="8" y="4" width="16" height="20" rx="2.5" stroke="white" stroke-width="1.8" fill="none"/>
              <path d="M12 10h8M12 14h8M12 18h5" stroke="white" stroke-width="1.5" stroke-linecap="round" opacity="0.85"/>
              <circle cx="23" cy="23" r="5" fill="rgba(255,255,255,0.18)" stroke="white" stroke-width="1.5"/>
              <path d="M21 23h4M23 21v4" stroke="white" stroke-width="1.5" stroke-linecap="round"/>
            </svg>''',
    '''<svg viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
              <!-- robot face -->
              <rect x="8.5" y="12" width="15" height="12" rx="3" stroke="white" stroke-width="1.7" fill="rgba(255,255,255,0.12)"/>
              <!-- antenna -->
              <path d="M16 12V8" stroke="white" stroke-width="1.5" stroke-linecap="round"/>
              <circle cx="16" cy="7" r="1.8" fill="white"/>
              <!-- eyes -->
              <circle cx="13" cy="18" r="2" fill="rgba(255,255,255,0.8)" stroke="white" stroke-width="1"/>
              <circle cx="19" cy="18" r="2" fill="rgba(255,255,255,0.8)" stroke="white" stroke-width="1"/>
              <circle cx="13.6" cy="17.6" r=".7" fill="#4f46e5"/>
              <circle cx="19.6" cy="17.6" r=".7" fill="#4f46e5"/>
              <!-- mouth smile -->
              <path d="M13 21.5 Q16 24 19 21.5" stroke="white" stroke-width="1.4" stroke-linecap="round" fill="none"/>
              <!-- ear nubs -->
              <rect x="5.5" y="16" width="3" height="5" rx="1.5" fill="rgba(255,255,255,0.5)"/>
              <rect x="23.5" y="16" width="3" height="5" rx="1.5" fill="rgba(255,255,255,0.5)"/>
            </svg>'''
)

# ── 8. 替换选题线索池 icon ──
content = content.replace(
    '''<svg viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M16 4c-4.4 0-8 3.6-8 8 0 3 1.6 5.5 4 7v3h8v-3c2.4-1.5 4-4 4-7 0-4.4-3.6-8-8-8z" stroke="white" stroke-width="1.8" fill="none"/>
              <path d="M12 22h8M13 25h6" stroke="white" stroke-width="1.5" stroke-linecap="round" opacity="0.75"/>
              <circle cx="16" cy="13" r="2.5" fill="white"/>
            </svg>''',
    '''<svg viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
              <!-- bulb body -->
              <path d="M16 5c-4.2 0-7.5 3.4-7.5 7.5 0 2.9 1.7 5.5 4.2 6.8V22h6.6v-2.7c2.5-1.3 4.2-3.9 4.2-6.8C23.5 8.4 20.2 5 16 5z" stroke="white" stroke-width="1.7" fill="rgba(255,255,255,0.15)" stroke-linejoin="round"/>
              <!-- base rings -->
              <path d="M13 22h6M13.5 24.5h5M14 27h4" stroke="white" stroke-width="1.4" stroke-linecap="round" opacity="0.75"/>
              <!-- filament cross -->
              <path d="M16 10v5M13.5 12.5h5" stroke="white" stroke-width="1.6" stroke-linecap="round"/>
              <!-- sparkles -->
              <path d="M25 6l.5 1.3 1.4.5-1.4.5L25 9.8l-.5-1.5-1.4-.5 1.4-.5z" fill="rgba(255,255,255,0.9)"/>
              <path d="M6 10l.4 1 1.1.4-1.1.4L6 12.8l-.4-1-1.1-.4 1.1-.4z" fill="rgba(255,255,255,0.65)"/>
            </svg>'''
)

# ── 9. 替换热点话题案例库 icon ──
content = content.replace(
    '''<svg viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
              <rect x="5" y="7" width="10" height="19" rx="1.5" stroke="white" stroke-width="1.8" fill="none"/>
              <rect x="17" y="7" width="10" height="19" rx="1.5" stroke="white" stroke-width="1.8" fill="none"/>
              <path d="M8 11h4M8 14.5h4M8 18h4" stroke="white" stroke-width="1.4" stroke-linecap="round" opacity="0.8"/>
              <path d="M20 11h4M20 14.5h4M20 18h4" stroke="white" stroke-width="1.4" stroke-linecap="round" opacity="0.8"/>
            </svg>''',
    '''<svg viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
              <!-- open book pages -->
              <path d="M16 8 C14 7 10 7 7 8.5V25c3-1.5 6.5-1.5 9 0z" stroke="white" stroke-width="1.6" fill="rgba(255,255,255,0.12)" stroke-linejoin="round"/>
              <path d="M16 8 C18 7 22 7 25 8.5V25c-2.5-1.5-6-1.5-9 0z" stroke="white" stroke-width="1.6" fill="rgba(255,255,255,0.18)" stroke-linejoin="round"/>
              <!-- spine -->
              <path d="M16 8v17" stroke="rgba(255,255,255,0.5)" stroke-width="1.2" stroke-linecap="round"/>
              <!-- left page lines -->
              <path d="M9.5 12h4.5M9.5 15h4.5M9.5 18h3" stroke="rgba(255,255,255,0.65)" stroke-width="1.2" stroke-linecap="round"/>
              <!-- right page lines -->
              <path d="M18 12h4.5M18 15h4.5M18 18h3" stroke="rgba(255,255,255,0.65)" stroke-width="1.2" stroke-linecap="round"/>
              <!-- sparkle top right -->
              <path d="M26 5l.5 1.3 1.5.5-1.5.5L26 8.8l-.5-1.5-1.5-.5 1.5-.5z" fill="rgba(255,255,255,0.85)"/>
            </svg>'''
)

# ── 10. 替换 panel-ai 内容 ──
old_panel_ai = '''          <!-- Panel: 智能搜索 -->
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
          </div>'''
new_panel_ai = '''          <!-- Panel: 智能搜索 -->
          <div class="search-panel-content" id="panel-ai" style="display:none">
            <div class="home-si-row">
              <span class="home-si-label">智能搜索</span>
              <input class="home-si-input" type="text" placeholder="请输入检索主题、关键词或事件要素"/>
              <button class="home-si-btn" type="button" aria-label="智能拆分">
                <span class="home-si-orbit"></span>
                <span class="home-si-core"></span>
              </button>
            </div>
            <div class="home-si-adv">高级配置</div>
          </div>'''
content = content.replace(old_panel_ai, new_panel_ai)

# ── 11. 去掉生成报告历史记录区块 ──
content = re.sub(
    r'\n\s*<!-- History -->\s*\n.*?</div>\n\s*</div><!-- /report-wrap -->',
    '\n            </div><!-- /report-wrap -->',
    content,
    flags=re.DOTALL
)

# ── 12. 去掉历史记录相关 CSS ──
content = content.replace(
    '/* Report History */',
    '/* Report History (hidden) */'
)

with open(r'c:\Pros\ZJ0512\首页\index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print('Done. Verifying...')
checks = [
    ('font-size:15px', '图标字号15px'),
    ('font-weight:700', '图标加粗'),
    ('align-items:stretch', '分析卡片拉齐'),
    ('flex-direction:column', 'a-card flex column'),
    ('flex:1', 'a-card-body flex 1'),
    ('home-si-row', '智能搜索框'),
    ('hsiRotate', '动画keyframe'),
    ('home-si-orbit', 'orbit动画'),
    ('neural nodes', 'AI图标'),
    ('flame above tallest bar', '热点图标'),
    ('target rings', '事件分析图标'),
    ('robot face', '编报图标'),
    ('bulb body', '选题图标'),
    ('open book pages', '案例库图标'),
]
all_ok = True
for kw, label in checks:
    ok = kw in content
    print(f'  {"✓" if ok else "✗"} {label}: {kw!r}')
    if not ok:
        all_ok = False
print('All OK' if all_ok else 'Some checks FAILED')
