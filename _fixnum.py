FILE = r'c:\Pros\ZJ0512\监测预警\热点榜单\index.html'
with open(FILE,'r',encoding='utf-8') as f: html=f.read()
before = html.count('t-numNone')
html = html.replace('class="t-numNone"', 'class="t-num"')
after = html.count('t-numNone')
with open(FILE,'w',encoding='utf-8') as f: f.write(html)
print(f'Fixed {before} occurrences, {after} remaining')
