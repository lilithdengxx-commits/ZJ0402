"""
Across all HTML files:
1. rename risk-hi label "高" → "重要"
2. remove risk-md spans (中) and risk-lo spans (低) entirely
"""
import re, glob, os

FILES = glob.glob(r'c:\Pros\ZJ0512\**\*.html', recursive=True)

# Pattern to remove: <span class="risk-tag [anything] risk-md [anything]">中</span>
#                    <span class="risk-tag [anything] risk-lo [anything]">低</span>
remove_pat = re.compile(
    r'<span\s+class="[^"]*risk-(?:md|lo)[^"]*">[^<]*</span>'
)

# Pattern to rename: any risk-tag with risk-hi, content = 高
rename_pat = re.compile(
    r'(<span\s+class="[^"]*risk-hi[^"]*">)高(</span>)'
)

total_removed = 0
total_renamed = 0

for path in FILES:
    with open(path, 'r', encoding='utf-8') as f:
        html = f.read()

    n_remove = len(remove_pat.findall(html))
    html = remove_pat.sub('', html)

    n_rename = len(rename_pat.findall(html))
    html = rename_pat.sub(r'\1重要\2', html)

    if n_remove or n_rename:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(html)
        rel = os.path.relpath(path, r'c:\Pros\ZJ0512')
        print(f'{rel}: removed {n_remove} mid/lo tags, renamed {n_rename} hi tags')
        total_removed += n_remove
        total_renamed += n_rename

print(f'\nTotal: {total_removed} removed, {total_renamed} renamed')
