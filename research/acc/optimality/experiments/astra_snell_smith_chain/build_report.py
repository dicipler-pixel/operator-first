"""Render this bundle's deliberately simple Markdown using the standard library."""
from pathlib import Path
import html
import re

p = Path(__file__).resolve().parent
lines = (p/'README.md').read_text().splitlines()


def inline(s):
    s = html.escape(s)
    return re.sub(r'\[([^]]+)\]\((https://[^)]+)\)', r'<a href="\2">\1</a>', s)


out = []
i = 0
while i < len(lines):
    line = lines[i]
    if not line.strip():
        i += 1
    elif line.startswith('#'):
        h, text = line.split(' ', 1)
        out.append(f'<h{len(h)}>{inline(text)}</h{len(h)}>')
        i += 1
    elif line.startswith('|'):
        rows = []
        while i < len(lines) and lines[i].startswith('|'):
            row = [x.strip() for x in lines[i].strip('|').split('|')]
            if not all(re.fullmatch(r'[: -]+', x) for x in row):
                rows.append(row)
            i += 1
        out.append('<table>')
        for j, row in enumerate(rows):
            tag = 'th' if j == 0 else 'td'
            out.append('<tr>'+''.join(f'<{tag}>{inline(c)}</{tag}>' for c in row)+'</tr>')
        out.append('</table>')
    elif line.startswith('    '):
        block = []
        while i < len(lines) and lines[i].startswith('    '):
            block.append(lines[i][4:])
            i += 1
        out.append('<pre><code>'+html.escape('\n'.join(block))+'</code></pre>')
    elif line.startswith('- '):
        out.append('<ul>')
        while i < len(lines) and lines[i].startswith('- '):
            out.append('<li>'+inline(lines[i][2:])+'</li>')
            i += 1
        out.append('</ul>')
    else:
        para = []
        while i < len(lines) and lines[i].strip():
            para.append(lines[i])
            i += 1
        out.append('<p>'+inline(' '.join(para))+'</p>')

style = '''body{margin:0;background:#10151d;color:#e7ecf0;font:17px/1.65 system-ui,sans-serif}
main{max-width:950px;margin:auto;padding:40px 28px}h1{font-size:34px;line-height:1.2;color:#edc875}
h2{margin-top:2em;color:#edc875}a{color:#8dcde8}table{border-collapse:collapse;width:100%;font-size:15px;margin:24px 0}
th,td{border-bottom:1px solid #3c4652;padding:10px;text-align:left}th{background:#202a35}
pre{white-space:pre-wrap;overflow-wrap:anywhere;background:#1b2531;padding:18px;border-radius:8px}
code{font-size:14px}p{margin:1em 0}li{margin:8px 0}@media print{body{background:white;color:black}h1,h2{color:#745513}}'''
page = '<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">'
page += '<title>Snell–Smith: testing the chain</title><style>'+style+'</style></head><body><main>'
page += '\n'.join(out)+'</main></body></html>'
assert page.count('<table>') == 2 and '<pre>#' not in page
(p/'report.html').write_text(page)
print('Rendered report with two tables and', page.count('<h2>'), 'sections.')
