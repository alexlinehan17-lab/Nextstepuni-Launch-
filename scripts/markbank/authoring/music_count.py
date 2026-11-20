#!/usr/bin/env python3
"""An independent count of a Music sitting's printed asks (Law 1: the paper is
the denominator, never the reader). Counts the part labels each listening
booklet's text layer prints at the start of a line ("(a)", "(b)", "(i)" ...)
and the composing questions, then sets the count beside the reading file's.
A difference is a hypothesis to check against the page, never a verdict
(answer-slot rows, true/false statements and choices print labels too).

    python3 music_count.py <reading file>
"""
import json
import os
import re
import sys

import fitz

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
LABEL = re.compile(r'^\(([a-z]|i{1,3}|iv|v|vi{0,3}|ix|x)\)')


def labels(pdf):
    out = []
    q = None
    for i, pg in enumerate(fitz.open(pdf)):
        for line in pg.get_text().split('\n'):
            line = line.strip()
            m = re.match(r'^Question (\d)\b', line)
            if m:
                q = int(m.group(1))
            m = LABEL.match(line)
            if m and q:
                out.append((q, m.group(1), i + 1))
    return out


def main(path):
    data = json.load(open(path, encoding='utf-8'))
    tag = f"{data['year']}-{'hl' if data['level'] == 'higher' else 'ol'}"
    asks = data['asks']
    for kind, comp in (('listening', '008'), ('composing', '006'), ('elective', '007')):
        pdf = os.path.join(ROOT, 'examiner-reports/music/papers', f'{tag}-{comp}-paper.pdf')
        if data.get('deferred'):
            pdf = os.path.join(ROOT, 'paper-trail-corpus/deferredexams', str(data['year']),
                               f"LC067{'A' if data['level'] == 'higher' else 'G'}LP{comp}EV.pdf")
        if not os.path.exists(pdf):
            continue
        read = [a for a in asks if a['paper'] == kind]
        found = labels(pdf)
        words = sum(len(p.get_text().split()) for p in fitz.open(pdf))
        print(f'{kind}: reading {len(read)} asks; text layer prints {len(found)} part labels ({words} words)')
        if kind == 'listening':
            by_q = {}
            for q, lab, page in found:
                by_q.setdefault(q, []).append(f'{lab}@{page}')
            for q in sorted(by_q):
                mine = [a['address'] for a in read if re.match(rf'Q{q}\b', a['address'])]
                print(f'  Q{q}: labels {" ".join(by_q[q])}')
                print(f'       reading {" ".join(mine)}')


if __name__ == '__main__':
    main(sys.argv[1])
