c = open(r'c:\Pros\ZJ0512\监测预警\AI智能推荐\index.html', encoding='utf-8').read()

# Fix 1: remove duplicate riskFilter listener
dup = "        document.querySelectorAll(\"input[name='riskFilter']\").forEach(r => {\n            r.addEventListener(\"change\", e => { state.riskFilter = e.target.value; render(); });\n        });\n        document.querySelectorAll(\"input[name='riskFilter']\").forEach(r => {\n            r.addEventListener(\"change\", e => { state.riskFilter = e.target.value; render(); });\n        });"
fix1 = "        document.querySelectorAll(\"input[name='riskFilter']\").forEach(r => {\n            r.addEventListener(\"change\", e => { state.riskFilter = e.target.value; render(); });\n        });"
c2 = c.replace(dup, fix1, 1)
print('Fix1 dup riskFilter:', c2 != c)

# Fix 2: resetButton - add riskFilter reset
old_reset = "            state.period = \"today\"; state.showAdvanced = false; state.sentimentFilter = \"\\u5168\\u90e8\";\n            searchInput.value = \"\"; periodSelect.value = \"today\";\n            document.querySelector(\"input[name='sentimentFilter'][value='\\u5168\\u90e8']\").checked = true;\n            render();"
new_reset = "            state.period = \"today\"; state.showAdvanced = false; state.sentimentFilter = \"\\u5168\\u90e8\"; state.riskFilter = \"\\u5168\\u90e8\";\n            searchInput.value = \"\"; periodSelect.value = \"today\";\n            document.querySelector(\"input[name='sentimentFilter'][value='\\u5168\\u90e8']\").checked = true;\n            document.querySelector(\"input[name='riskFilter'][value='\\u5168\\u90e8']\").checked = true;\n            render();"
c3 = c2.replace(old_reset, new_reset, 1)
print('Fix2 resetButton:', c3 != c2)

# Fix 3: ai-panel row3 - move ovMeta inline
old_panel = '<div class="ai-panel" style="margin:0"><span class="ai-indicator"></span><span class="ai-label">\\u4e8b\\u4ef6\\u6982\\u89c8</span><span class="ai-body">${ev.summary}</span>${ovMeta ? `<div class="ov-meta">${ovMeta}</div>` : \'\'}</div>'
new_panel = '<div class="ai-panel" style="margin:0;display:flex;align-items:flex-start"><span class="ai-indicator"></span><span class="ai-label">\\u4e8b\\u4ef6\\u6982\\u89c8</span><span class="ai-body" style="flex:1 1 0;min-width:0">${ev.summary}</span>${ovMeta ? `<span class="ov-meta-inline" style="flex-shrink:0;margin-left:12px;display:flex;align-items:center;gap:4px;flex-wrap:wrap">${ovMeta}</span>` : \'\'}</div>'
c4 = c3.replace(old_panel, new_panel, 1)
print('Fix3 ai-panel row3:', c4 != c3)

open(r'c:\Pros\ZJ0512\监测预警\AI智能推荐\index.html', 'w', encoding='utf-8').write(c4)
print('Written.')
