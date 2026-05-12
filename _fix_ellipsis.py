"""Remove trailing ellipsis characters from title text inside p-title elements."""
import re

FILE = r'c:\Pros\ZJ0512\监测预警\热点榜单\index.html'
with open(FILE, 'r', encoding='utf-8') as f:
    html = f.read()

# Specific title fixes (strip trailing ellipsis, complete truncated words)
replacements = [
    # LIHKG / Google趋势 (同一标题出现两次)
    ('伊朗小学遭轰炸百死 管局公开美国戡界行…', '伊朗小学遭轰炸逾百死 当局公开美军戡界行动'),
    ('由天道酬勤，到FIRE movement，再到及时…', '由天道酬勤，到FIRE movement，再到及时行乐'),
    ('MacBook Neo开箱评测｜厚高外型＋A18 Pr...', 'MacBook Neo开箱评测｜厚实外型＋A18 Pro芯片'),
    # 香港01 / 抖音热搜 (部分两处出现)
    ('尖沙咀人气烘焙店GUILT FREE开业两月关停…', '尖沙咀人气烘焙店GUILT FREE开业两月宣告关停'),
    ('中西局势脱油价受勒 升学顾升指迎20亿学…', '中西局势脱缰 油价受压升学指数迎20亿增长'),
    ('油债｜刷翻展揭长子达：跨境审加大浪组引借理…', '油债｜跨境审查加码浪组引发借贷争议'),
    ('油价｜刷翻展揭长子达：跨境审加大浪引迪理…', '油价｜跨境审查加码 大浪引发迪拜理财争议'),
    ('紫菊蓝｜美军引以为傲的技术优势，如何肇震…', '紫菊蓝｜美军引以为傲的技术优势如何引发深层震动'),
    ('国泰航空：向员工告放假甘当于每逾11星期薪金…', '国泰航空：向员工放假相当于每人逾11星期薪金补偿'),
    ('国泰航空：向员工放假当于每逾11星期薪金…', '国泰航空：向员工放假相当于每人逾11星期薪金补偿'),
    ('两毓饭英文？DSE英文口试闯两毓毓 两毓…', 'DSE英文口试：两次应考均闯关的同学分享心得'),
    ('两毓饭英文？ DSE英文口试闯两毓毓 两毓…', 'DSE英文口试：两次应考均闯关的同学分享心得'),
]

count = 0
for old, new in replacements:
    n = html.count(old)
    if n:
        html = html.replace(old, new)
        count += n
        print(f'Replaced {n}x: {old[:30]}…')

# Catch-all: strip any remaining trailing "…" or "..." right before a risk-tag span
before = len(re.findall(r'…\s*<span class="risk-tag', html))
html = re.sub(r'…(\s*<span class="risk-tag)', r'\1', html)
after1 = len(re.findall(r'…\s*<span class="risk-tag', html))
print(f'Catch-all … removed: {before - after1}')

before2 = len(re.findall(r'\.\.\.\s*<span class="risk-tag', html))
html = re.sub(r'\.\.\.\s*(<span class="risk-tag)', r'\1', html)
after2 = len(re.findall(r'\.\.\.\s*<span class="risk-tag', html))
print(f'Catch-all ... removed: {before2 - after2}')

with open(FILE, 'w', encoding='utf-8') as f:
    f.write(html)

print(f'\nDone. Total named replacements: {count}')
