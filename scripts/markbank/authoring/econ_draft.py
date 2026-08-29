#!/usr/bin/env python3
"""Propose a card stanza for an excluded Economics ask, for a human to finish.

    python3 scripts/markbank/authoring/econ_draft.py --all
    python3 scripts/markbank/authoring/econ_draft.py "2023 OL Q15(a)(i)"

What this does and does not do
------------------------------
It reads the tariff CELLS the scheme printed and proposes a tariff model from
their shape; it takes the paper's own wording for the question; it names the
scheme slice and the figure keyed to the ask. That is the mechanical part, and
doing it by hand 92 times is how transcription errors get in.

It does NOT decide anything that needs judgement, and it says so in the stanza
it prints:

  * the tariff is PROPOSED. Where the cells do not resolve to one reading it
    refuses and says why, because guessing a tariff is the error this bank has
    made five separate times.
  * the figure is a CANDIDATE. A crop is keyed to the parent question as often
    as to the part, so the same crop is offered to every part of that question
    and only one of them may be about it. Check the alt text against the
    question before binding: five of the first twenty-six matched this way were
    for a different question entirely.
  * topicId, conceptId and the notes are left as TODO. A note that does not
    name the specific trap is worth nothing to a student.

Tariff shapes it understands, all read off the scheme's own cells:
  ['8']                 one response, 8 marks              -> point, fixed
  ['12', '2 @ 6']       two responses at 6                 -> anyN claim 2 per 6
  ['1st@8', '2nd@4']    descending, first 8 then 4         -> anyN steps [8, 4]
  ['3+3+2']             three responses, 3 then 3 then 2   -> anyN steps [3,3,2]
  ['10', '(6+4)']       one response, 10, split disclosed  -> point, fixed
"""
import argparse
import json
import os
import re
import sys

DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, DIR)
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(DIR)))

import paper as PP                              # noqa: E402
from econ_auto import Paper as SchemePaper      # noqa: E402
from econ_backfill_scout import anchors_from, figures_for, REF   # noqa: E402

EXCL = os.path.join(DIR, 'exclusions/economics.json')
FIGS = os.path.join(ROOT, 'components/MarkBank/figures.json')

FILE_FOR = {}   # (year, level, section) -> authoring script


def script_for(year, level, section):
    lv = 'hl' if level == 'higher' else 'ol'
    stem = f'econ_{year}_{lv}' + ('_seca' if section == 'A' else '')
    return f'scripts/markbank/authoring/{stem}.py'


def tariff_from(cells):
    """A tariff model, or a refusal naming what could not be read.

    Every branch here is a shape the schemes actually print. Anything else is
    returned as a refusal rather than rounded to the nearest shape.
    """
    if not cells:
        return None, 'no tariff cell on this part'
    nums = [c.strip() for c in cells]

    # 1st@8 / 2nd@4 — a descending tariff written as ordinals
    steps = []
    for c in nums:
        m = re.fullmatch(r'(\d+)(?:st|nd|rd|th)\s*[@x]\s*(\d+)', c.replace(' ', ''))
        if m:
            steps.append(int(m.group(2)))
    if len(steps) >= 2:
        return dict(kind='steps', steps=steps, total=sum(steps)), None

    # 3+3+2 — a descending tariff written as a sum
    for c in nums:
        m = re.fullmatch(r'\(?(\d+(?:\s*\+\s*\d+){1,5})\)?', c)
        if m and '+' in m.group(1):
            parts = [int(x) for x in re.split(r'\s*\+\s*', m.group(1))]
            if len(parts) >= 2 and len(set(parts)) > 1 or len(parts) >= 3:
                return dict(kind='steps', steps=parts, total=sum(parts)), None

    # N @ M — a flat best-of
    for c in nums:
        m = re.fullmatch(r'(\d+)\s*[@x]\s*(\d+)', c.replace(' ', ''))
        if m:
            n, per = int(m.group(1)), int(m.group(2))
            return dict(kind='anyN', claim=n, per=per, total=n * per), None

    # a lone total
    plain = [int(c) for c in nums if re.fullmatch(r'\d+', c)]
    if len(plain) == 1:
        return dict(kind='point', total=plain[0]), None
    if len(plain) > 1:
        return None, f'{len(plain)} bare totals {plain} — cannot tell which prices this part'
    return None, f'unreadable cells {cells}'


def draft(ref, figs, byref):
    m = REF.match(ref)
    if not m:
        return f'# {ref}: ref not parsed\n'
    year, lvl, sec, q, letter, roman = m.groups()
    year, q = int(year), int(q)
    lv = 'hl' if lvl == 'HL' else 'ol'
    level = 'higher' if lv == 'hl' else 'ordinary'

    P = PP.Paper('economics', year, lv)
    try:
        qtext = ' '.join((P.text(q, letter, roman) or '').split())
    except Exception as exc:                       # noqa: BLE001
        return f'# {ref}: paper reader: {exc}\n'

    S = SchemePaper(year, level, sec) if sec else SchemePaper(year, level)
    part = used = None
    for a in anchors_from(qtext):
        try:
            part, used = S.find(a), a
            break
        except Exception:                          # noqa: BLE001
            continue
    if part is None:
        return f'# {ref}: scheme block not located\n'

    model, refusal = tariff_from(part['cells'])
    cands = figures_for(ref, byref)

    cid = ('econ-%s-%s-%s' % (year, lv, f'q{q}' + (f'-{letter}' if letter else '')
                              + (f'-{roman}' if roman else ''))).lower()
    out = [f'# ── {ref}  cells={part["cells"]}  opts={len(part["options"])}']
    if refusal:
        out.append(f'#    REFUSES: {refusal}')
    out.append(f'#    file: {script_for(year, level, sec)}')
    out.append(f'#    id:   {cid}')
    out.append(f'#    Q:    {qtext[:150]}')
    if model:
        out.append(f'#    tariff proposed: {model}')
    for k in cands[:2]:
        out.append(f'#    figure CANDIDATE {k}')
        out.append(f'#       {(figs.get(k, {}).get("alt") or "")[:150]}')
    for o in part['options'][:6]:
        out.append(f'#    opt: {o[:170]}')
    return '\n'.join(out) + '\n'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('ref', nargs='?')
    ap.add_argument('--all', action='store_true')
    args = ap.parse_args()

    figs = {k: v for k, v in json.load(open(FIGS)).items() if k.startswith('economics-')}
    byref = {}
    for k, v in figs.items():
        r = re.sub(r'\s+', ' ', (v.get('questionRef') or '')).strip()
        if r:
            byref.setdefault(r, []).append(k)

    refs = ([re.sub(r'\s+', ' ', e['ref']).strip() for e in json.load(open(EXCL))]
            if args.all else [args.ref])
    for r in refs:
        print(draft(r, figs, byref))


if __name__ == '__main__':
    main()
