import re
c = open(r'c:\Pros\ZJ0512\事件分析\事件管理\index.html', encoding='utf-8').read()

# 1. info-avg-sidebar: 152px -> 220px
c = c.replace(
    '.info-avg-sidebar{flex:0 0 152px;',
    '.info-avg-sidebar{flex:0 0 220px;'
)

# 2. info-avg-body min-height: 210 -> 240
c = c.replace(
    '.info-avg-body{display:flex;gap:0;padding:12px 16px 16px;min-height:210px}',
    '.info-avg-body{display:flex;gap:0;padding:12px 16px 16px;min-height:240px}'
)

# 3. sentiment-body min-height: 200 -> 280
c = c.replace(
    '.sentiment-body{display:flex;gap:0;padding:12px 16px 16px;align-items:flex-start;min-height:200px}',
    '.sentiment-body{display:flex;gap:0;padding:12px 16px 16px;align-items:flex-start;min-height:280px}'
)

# 4. wordcloud-area height: 190 -> 260
c = c.replace(
    '.wordcloud-area{position:relative;height:190px;overflow:hidden}',
    '.wordcloud-area{position:relative;height:260px;overflow:hidden}'
)

# 5. peak-stats-grid: 360px -> 440px
c = c.replace(
    '.peak-stats-grid{flex:0 0 360px;',
    '.peak-stats-grid{flex:0 0 440px;'
)

# 6. Scale up wordcloud font sizes (multiply roughly by 1.25-1.4)
wc_map = {
    'font-size:28px': 'font-size:36px',
    'font-size:30px': 'font-size:40px',
    'font-size:24px': 'font-size:30px',
    'font-size:20px': 'font-size:26px',
    'font-size:18px': 'font-size:23px',
    'font-size:17px': 'font-size:22px',
    'font-size:15px': 'font-size:19px',
}
# Only scale within the wordcloud-area HTML block
wc_start = c.find('<div class="wordcloud-area">')
wc_end = c.find('</div>', wc_start) + 6
wc_block = c[wc_start:wc_end]
for old, new in wc_map.items():
    wc_block = wc_block.replace(old, new)
c = c[:wc_start] + wc_block + c[wc_end:]

open(r'c:\Pros\ZJ0512\事件分析\事件管理\index.html', 'w', encoding='utf-8').write(c)
print('Done')
print('info-avg-sidebar 220px:', 'flex:0 0 220px' in c)
print('sentiment min-height 280:', 'min-height:280px' in c)
print('wordcloud 260px:', 'height:260px' in c)
print('peak-stats 440px:', 'flex:0 0 440px' in c)
print('wc 36px:', 'font-size:36px' in c)
