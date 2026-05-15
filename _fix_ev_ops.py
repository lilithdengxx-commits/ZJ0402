c = open(r'c:\Pros\ZJ0512\事件分析\事件管理\index.html', encoding='utf-8').read()

# 1. Change ai-bdg 'A' to star+AI
old_bdg = '<span class="ai-bdg">A</span>'
new_bdg = ('<span class="ai-bdg">'
           '<svg width="8" height="8" viewBox="0 0 24 24" fill="white" style="margin-right:1px;opacity:.9">'
           '<path d="M12 2L9.5 9.5H2L7.5 14L5.5 22L12 17.5L18.5 22L16.5 14L22 9.5H14.5Z"/>'
           '</svg>AI</span>')
c = c.replace(old_bdg, new_bdg)

# 2. ops buttons per panel
old_btn = '<td><button class="ops-dot-btn">\u00b7\u00b7\u00b7</button></td>'
ai_new_btn = ('<td><div class="ops-wrap">'
              '<button class="ops-dot-btn ops-toggle">\u00b7\u00b7\u00b7</button>'
              '<div class="ops-menu">'
              '<button type="button">\u590d\u5236</button>'
              '<button type="button">\u5206\u4eab</button>'
              '</div></div></td>')
shared_new_btn = ('<td><div class="ops-wrap">'
                  '<button class="ops-dot-btn ops-toggle">\u00b7\u00b7\u00b7</button>'
                  '<div class="ops-menu">'
                  '<button type="button">\u590d\u5236</button>'
                  '<button type="button">\u5206\u4eab</button>'
                  '<button type="button" style="color:#e04040">\u5220\u9664</button>'
                  '</div></div></td>')

panel_ai_start = c.find('id="panel-ai-events"')
panel_ai_end = c.find('id="panel-my-events"')
panel_shared_start = c.find('id="panel-shared-events"')
panel_shared_end = c.find('</section>\n        </main>')

ai_block = c[panel_ai_start:panel_ai_end].replace(old_btn, ai_new_btn)
shared_block = c[panel_shared_start:panel_shared_end].replace(old_btn, shared_new_btn)

c2 = c[:panel_ai_start] + ai_block + c[panel_ai_end:panel_shared_start] + shared_block + c[panel_shared_end:]

open(r'c:\Pros\ZJ0512\事件分析\事件管理\index.html', 'w', encoding='utf-8').write(c2)
print('AI ops replaced:', ai_block.count('ops-wrap'))
print('Shared ops replaced:', shared_block.count('ops-wrap'))
print('AI badge replaced:', c2.count(new_bdg))
