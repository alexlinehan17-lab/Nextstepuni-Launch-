"""Trim drafted crops that run down into page furniture (page footers, [OVER, a bare page number)
or long blank space below the last line of their part.

usage: python3 scripts/markbank/agricultural-science-audit/footer_trim.py <module> <year> <fileid> [--write]

A region piece is shortened to 0.008 below the last text line it holds above the furniture.
Rewritten lines get a "  # ... page footer" comment so regioncheck.py treats them as hand-set.
Without --write it only prints what it would change.
"""
import importlib
import re
import sys

import fitz

sys.path.insert(0, 'scripts/markbank/authoring')
module, year, fileid = sys.argv[1:4]
write = '--write' in sys.argv
FURNITURE = re.compile(r'^(page\s*\|?\s*\d+(\s*of\s*\d+)?|\[over\]?|\d{1,2}|blank page)$', re.I)


def lines(pdf):
    out = {}
    with fitz.open(pdf) as d:
        for i, pg in enumerate(d, start=1):
            H = pg.rect.height
            rows = []
            for b in pg.get_text('dict')['blocks']:
                for l in b.get('lines', []):
                    t = ' '.join(''.join(s['text'] for s in l['spans']).split())
                    if t:
                        rows.append((l['bbox'][1] / H, l['bbox'][3] / H, t))
            # Images count as content, so a trim never cuts a photograph below the last line of text.
            rows += [(info['bbox'][1] / H, info['bbox'][3] / H, '<image>') for info in pg.get_image_info()]
            out[i] = rows
    return out


src = {'paper': lines(f'paper-trail-corpus/exampapers/{year}/{fileid}'), 'scheme': lines(f'paper-trail-corpus/markingschemes/{year}/{fileid}')}
mod = importlib.import_module(module)
path = f'scripts/markbank/authoring/{module}.py'
text = open(path).read()
changed = 0
for ref, (pp, sp) in mod.REGIONS.items():
    new = {}
    for side, pieces in (('paper', pp), ('scheme', sp)):
        out = []
        for piece in pieces:
            p, (x0, y0, x1, y1) = piece['p'], piece['r']
            inside = [r for r in src[side][p] if r[0] >= y0 - 0.002 and r[1] <= y1 + 0.004]
            furniture = [r for r in inside if FURNITURE.match(r[2])]
            content = [r for r in inside if not FURNITURE.match(r[2])]
            if furniture and content and max(r[1] for r in content) < min(r[0] for r in furniture):
                y1 = round(max(r[1] for r in content) + 0.008, 3)
            out.append((p, y0, y1, x0, x1))
        new[side] = out
    old = [(q['p'], q['r'][1], q['r'][3], q['r'][0], q['r'][2]) for q in pp] + [(q['p'], q['r'][1], q['r'][3], q['r'][0], q['r'][2]) for q in sp]
    if old == new['paper'] + new['scheme']:
        continue
    fmt = lambda ps: ', '.join(f'({p}, {y0:.3f}, {y1:.3f})' if (x0, x1) == (0, 1) else f'({p}, {y0}, {y1}, {x0}, {x1})' for p, y0, y1, x0, x1 in ps)
    line = f"    '{ref}': (P({fmt(new['paper'])}), P({fmt(new['scheme'])})),"
    start = text.index('REGIONS = {')
    end = text.index('\n}\n', start)
    m = re.compile(r"^    '" + re.escape(ref) + r"': \(P.*$", re.M).search(text, start, end)
    comment = m.group(0).split('  # ', 1)[1] if '  # ' in m.group(0) else ''
    note = (comment + '; ' if comment else '') + 'trimmed above the page footer'
    print(f'{ref}:\n  was {m.group(0).strip()}\n  now {line.strip()}')
    text = text[:m.start()] + line + '  # ' + note + text[m.end():]
    changed += 1
if write:
    open(path, 'w').write(text)
print(changed, 'region(s)', 'rewritten' if write else 'would change')
