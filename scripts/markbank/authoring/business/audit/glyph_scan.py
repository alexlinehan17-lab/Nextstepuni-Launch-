"""Scan Business card data for ligature, private-use and broken-subset code points."""
import json, re, sys, collections
BAD = re.compile(r'[Ā-ͯЀ-῿Ⰰ-ⷿ-ﬀ-ﭏ￰-￿]')
def walk(node, path, out):
    if isinstance(node, dict):
        for k, v in node.items(): walk(v, path + [str(k)], out)
    elif isinstance(node, list):
        for i, v in enumerate(node): walk(v, path + [str(i)], out)
    elif isinstance(node, str):
        for m in BAD.finditer(node):
            out.append(('/'.join(path), m.group(), node[max(0, m.start()-30):m.end()+30]))
hits = []
for f in ['scripts/markbank/authored/business.json', 'components/MarkBank/cards/business/rubric-authored.json',
          'components/MarkBank/cards/business/route-pools.json', 'scripts/markbank/card-corrections.json']:
    d = json.load(open(f))
    if f.endswith('card-corrections.json'):
        d = {k: v for k, v in d.items() if 'business' in k.lower()} if isinstance(d, dict) else d
    walk(d, [f], hits)
for f in ['components/MarkBank/cards/business/higher.ts', 'components/MarkBank/cards/business/ordinary.ts']:
    for i, line in enumerate(open(f, encoding='utf-8'), 1):
        for m in BAD.finditer(line):
            hits.append((f'{f}:{i}', m.group(), line[max(0, m.start()-30):m.end()+30].strip()))
c = collections.Counter(h[1] for h in hits)
print('total', len(hits), {f'U+{ord(k):04X} {k}': v for k, v in c.items()})
for h in hits[:int(sys.argv[1]) if len(sys.argv) > 1 else 60]:
    print(h)
