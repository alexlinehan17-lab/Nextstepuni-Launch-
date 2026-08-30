#!/usr/bin/env python3
"""Everything needed to card one open Chemistry part, in one place.

    python3 scripts/markbank/authoring/chem_scout.py [--year 2022] [--level hl]
                                                     [--limit 20] [--with-points]

reconcile says Chemistry has 123 open asks. That number alone is not
actionable: an ask is open either because the scheme says nothing liftable, or
-- far more often in this subject -- because the parser that read the scheme
filed the answer under a key that does not match the paper's numbering. The
2023 Higher scheme heads its answers "QUESTION 3" where Scheme's QHEAD expects
"Q3", so its markdown parse is empty for the whole paper; and SchemePdf takes
its question number from whichever block last looked like a heading, so the
numbered marking preamble claims a Question 4 and most of Sections A and B end
up filed under its Q4 and Q8 letters.

So this prints, per open ask:

  * the PAPER's wording -- the question a student is actually set,
  * what each of the two scheme parsers returns AT that key, and
  * every key in either parser whose text contains a phrase from the paper's
    own wording, which is what finds the answer when the key is wrong.

The last one is the point. Anchoring on the paper's own words makes the pairing
self-confirming: if the anchor is found, the block returned is provably the one
that answers this ask. Page adjacency and key equality are both hypotheses;
this is evidence.

Nothing here decides anything, and nothing here writes a card.
"""
import argparse
import collections
import os
import re
import sys

DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, DIR)

import paper as PP                                          # noqa: E402
import reconcile as R                                       # noqa: E402
from scheme import Scheme                                   # noqa: E402
from scheme_pdf import SchemePdf                            # noqa: E402

LABEL = re.compile(r'Q(\d+)(?:\(([a-z]+)\))?(?:\(([a-z]+)\))?$')


def anchors(question, sizes=(9, 7, 5)):
    """Phrases from the paper's wording to look the scheme up by.

    A scheme reprints or paraphrases the ask above its answer, but loosely, and
    the reworded part is nearly always the START -- that is where the cue sits.
    So slide a window across the whole question rather than trying prefixes.
    """
    words = re.sub(r'\s+', ' ', question or '').split()
    out = []
    for size in sizes:
        for i in range(0, max(1, len(words) - size + 1)):
            phrase = ' '.join(words[i:i + size])
            if len(phrase) >= 18 and phrase not in out:
                out.append(phrase)
    return out


FOOTER = re.compile(r'(Higher|Ordinary)\s+Level\s+Chemistry\s+20\d\d(\s+Page)?'
                    r'|Chemistry\s+20\d\d\s+(Higher|Ordinary)\s+Level', re.I)
MARK_ONLY = re.compile(r'^[\s()\[\]0-9\u00d7+.,/\u2013-]*$')


def squash(s):
    return re.sub(r'[^a-z0-9]', '', (s or '').lower())


def answer_body(points):
    """The marking points with the furniture stripped, or None if that is all
    they were.

    A key can carry a running page footer and nothing else -- 2022 HL Q8(b)(ii)
    and Q11(a)(vi) both return "Higher Level Chemistry 2022 Page" -- and a
    triage that counts characters calls that an answer. It also has to discount
    the mark cell and the examiner's bracketed aside, because "(6)" alone is
    what the scheme prints against a part whose answer is a DRAWING.

    This is a filter, not a verdict. It cannot tell a whole answer from half of
    one: 2021 OL Q8(b)(ii) asks what is added to ethene in reactions A and B,
    and the scheme text at that key names only B. Read the ask beside the
    points before carding either.
    """
    body = []
    for pt in points or []:
        t = FOOTER.sub(' ', pt)
        t = re.sub(r'\((?:\d+\s*[\u00d7+]\s*)?\d+\)', ' ', t)
        t = re.sub(r'\[[^\]]*\]', ' ', t)
        t = ' '.join(t.split())
        if t and not MARK_ONLY.match(t):
            body.append(t)
    if not body:
        return None
    blob = ' '.join(body)
    if len(re.findall(r'[A-Za-z]{2,}', blob)) < 2:
        return None
    toks = blob.split()
    if toks and sum(1 for t in toks if len(t) <= 2) / len(toks) > 0.6:
        return None       # figure labels: "H H H H H H"
    return blob


def search(readers, question):
    """Every (parser, key) whose marking points contain a phrase from the ask."""
    probes = [squash(a) for a in anchors(question)[:60] if a]
    hits = []
    for name, S in readers:
        try:
            paths = list(S.paths())
        except Exception:                                    # noqa: BLE001
            continue
        for key in paths:
            try:
                pts = S.points(*key)
            except Exception:                                # noqa: BLE001
                continue
            blob = squash(' '.join(pts))
            if not blob:
                continue
            for p in probes:
                if p and p in blob:
                    hits.append((name, key, pts))
                    break
    return hits


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--year', type=int)
    ap.add_argument('--level')
    ap.add_argument('--limit', type=int, default=0)
    ap.add_argument('--with-points', action='store_true',
                    help='print the marking points at the exact key too')
    args = ap.parse_args()

    r = R.reconcile_subject('chemistry')
    papers, readers, shown = {}, {}, 0
    for p in r['papers']:
        if args.year and p['year'] != args.year:
            continue
        if args.level and p['level'] != args.level:
            continue
        for label in p.get('open', []):
            m = LABEL.match(label.strip())
            if not m:
                print(f'!! open label not parsed: {label!r}')
                continue
            q = int(m.group(1))
            letter, roman = m.group(2), m.group(3)
            if letter and re.fullmatch(r'[ivx]+', letter) and not roman:
                letter, roman = None, letter
            yr, lv = p['year'], p['level']

            P = papers.setdefault((yr, lv), PP.Paper('chemistry', yr, lv))
            try:
                qtext = P.text(q, letter, roman) or ''
            except Exception as exc:                         # noqa: BLE001
                qtext = f'<paper reader: {type(exc).__name__}: {exc}>'

            if (yr, lv) not in readers:
                pair = []
                for name, cls in (('md', Scheme), ('pdf', SchemePdf)):
                    try:
                        pair.append((name, cls('chemistry', yr, lv)))
                    except Exception as exc:                 # noqa: BLE001
                        print(f'   [{name} reader unavailable for {yr} {lv}: {exc}]')
                readers[(yr, lv)] = pair

            print('=' * 100)
            print(f'OPEN    {yr} {lv.upper()} {label}')
            print(f'PAPER   {qtext[:300]}')
            if args.with_points:
                for name, S in readers[(yr, lv)]:
                    try:
                        pts = S.points(q, letter, roman)
                    except Exception:                        # noqa: BLE001
                        pts = None
                    print(f'AT KEY  [{name}] {pts if pts else "<nothing at this key>"}')
            hits = search(readers[(yr, lv)], qtext)
            if not hits:
                print('FOUND   <no scheme block contains the paper\'s wording>')
            for name, key, pts in hits[:3]:
                print(f'FOUND   [{name}] key={key}')
                for pt in pts[:6]:
                    print(f'          - {pt[:150]}')
            shown += 1
            if args.limit and shown >= args.limit:
                print('=' * 100)
                print(f'{shown} open ask(s) shown')
                return
    print('=' * 100)
    print(f'{shown} open ask(s) shown')


if __name__ == '__main__':
    main()
