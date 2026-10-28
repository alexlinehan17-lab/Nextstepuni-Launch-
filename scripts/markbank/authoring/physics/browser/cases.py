#!/usr/bin/env python3
"""cases.py YEAR LL [YEAR LL ...] -> browser-<name>.json: every Physics card of the sittings that
carries a figure, and one text card in five, as browser cases for browser-cases.mjs.
  python3 cases.py 2026 hl 2026 ol 2025 hl 2025 ol   (name: the sittings joined by '+')"""
import json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..', '..'))
args = sys.argv[1:]
sits = [(args[i], args[i + 1]) for i in range(0, len(args), 2)]
man = {}
for f in ('figures.json', 'figures-physics.json'):
    man.update(json.load(open(os.path.join(ROOT, 'components', 'MarkBank', f))))
deck = {}
for lvl in ('higher', 'ordinary'):
    t = open(os.path.join(ROOT, 'components', 'MarkBank', 'cards', 'physics', f'{lvl}.ts')).read()
    deck.update({i: None for i in re.findall(r'^    id: "([^"]+)"', t, re.M)})
bank = json.load(open(os.path.join(ROOT, 'scripts', 'markbank', 'authored', 'physics.json')))


def snippet(text, n=40):
    """A run of the text the screen shows verbatim: the first run of 3+ plain
    characters between those the renderer may set differently (super/subscripts,
    symbols), without a leading part marker the screen sets apart."""
    runs = [r.strip() for r in re.split(r'[\u00b2\u00b3\u00b9\u2070-\u209f\u221a\n×→/]', text.strip())]
    runs = [re.sub(r'^\((?:[a-l]|[ivx]{1,4})\)\s*', '', r) for r in runs]
    best = next((r for r in runs if len(r) >= 3), max(runs, key=len))
    return best[:n].strip()


cases = []
for y, l in sits:
    cards = [c for c in bank if c['id'].startswith(f'phys-{y}-{l}-') and c['id'] in deck]
    figs = [c for c in cards if c.get('figureKey') or c.get('questionFigureKey')]
    text = [c for c in cards if c not in figs][::5]
    for c in figs + text:
        case = {'id': c['id'], 'ask': '' if c.get('questionFigureKey') else snippet(c['questionText']),
                'answer': snippet(next(r['verbatim'] for r in c['rows'] if r.get('verbatim')), 30)}
        # An answer the question itself prints ("constructive or destructive
        # interference?") cannot be checked as hidden before the reveal.
        if case['answer'] in f"{c.get('stem') or ''} {c['questionText']}":
            case['answerInAsk'] = True
        if c.get('figureKey'):
            src = os.path.basename(man[c['figureKey']]['src'])
            case['solution' if man[c['figureKey']].get('solution') else 'figure'] = src
        if c.get('questionFigureKey'):
            case['questionFigure'] = os.path.basename(man[c['questionFigureKey']]['src'])
        cases.append(case)
name = '+'.join(f'{y}-{l}' for y, l in sits)
out = os.path.join(HERE, f'browser-{name}.json')
json.dump(cases, open(out, 'w'), indent=1, ensure_ascii=False)
print(out, len(cases), 'cases')
