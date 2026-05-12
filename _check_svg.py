with open(r'c:\Pros\ZJ0512\svg代码.txt', 'rb') as f:
    svg = f.read().decode('utf-8')

print('SVG len:', len(svg))
print('contains <div:', '<div' in svg)
print('contains </div:', '</div' in svg)
print('contains sidebar-nav-area:', 'sidebar-nav-area' in svg)

# Check for any HTML-like tags
import re
tags = re.findall(r'<[a-zA-Z/][^>]{0,30}>', svg)
unique_tags = set(tags)
print('Unique HTML-like tags found in SVG:')
for t in sorted(unique_tags)[:30]:
    print(' ', repr(t))
