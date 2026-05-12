import re
FILE = r'c:\Pros\ZJ0512\监测预警\热点榜单\index.html'
with open(FILE,'r',encoding='utf-8') as f:
    html = f.read()

print('LIHKG:', len(re.findall(r'plist-item', html[html.find('LIHKG'):html.find('高登')])))
print('高登:', len(re.findall(r'plist-item', html[html.find('香港高登'):html.find('香港01')])))
print('香港01:', len(re.findall(r'plist-item', html[html.find('香港01'):html.find('雅虎新闻')])))
print('雅虎:', len(re.findall(r'plist-item', html[html.find('雅虎新闻'):html.find('Google')])))
baidu_block = html[html.find('百度热搜'):][:4000]
print('百度:', len(re.findall(r'plist-item', baidu_block)))
print('rk-p remaining:', html.count('class="rk-p"'))
idx = html.find('rank-hdr')
print('rank-hdr snippet:', html[idx:idx+80])
print('t-right:', 't-right' in html)
print('p-title-row:', 'p-title-row' in html)
print('p-tr-heat:', 'p-tr-heat' in html)
idx2 = html.find('内地总榜')
row1 = html[idx2:idx2+800]
idx3 = row1.find('t-right')
print('内地总榜 t-right snippet:', row1[idx3:idx3+80] if idx3>0 else 'NOT FOUND')
idx4 = html.find('香港总榜')
hk1 = html[idx4:idx4+400]
print('香港总榜 first row has t-tw:', 't-tw' in hk1)
