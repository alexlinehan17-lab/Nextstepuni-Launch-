#!/usr/bin/env python3
"""Mark Bank — the ledger that says whether a subject is finished.

    python3 scripts/markbank/authoring/reconcile.py maths
    python3 scripts/markbank/authoring/reconcile.py --all
    python3 scripts/markbank/authoring/reconcile.py biology --json out.json --open

The bar, in the owner's words: if a question is in an exam paper, it should be
in the mark bank somewhere when the subject is finished. This tool holds every
subject to that sentence. It takes the census (paper_census.py — every leaf
ask the papers print) on one side and the SHIPPED decks on the other, and
files every ask as exactly one of:

  covered    a shipped card cites it, either exactly or through the part the
             scheme priced it under (a card for Q2(b) covers Q2(b)(i)-(iii)
             when the scheme marks them on one scale — the ask is in the bank,
             inside that card);
  excluded   named in exclusions/<subject>.json with a reason AND the scheme
             evidence for that reason. Exclusions are rare on purpose: even
             drawing questions are cardable (split by what the scheme says),
             so an exclusion is a claim that the scheme prints nothing at all.
  OPEN       neither. The subject is not finished while this list is non-empty.

It also reads the other direction, because citations rot too:

  orphan     a card whose questionRef matches no ask in any paper on disk —
             either a mis-citation (19 were found this way once) or a card for
             a year whose paper was never fetched;
  unparsed   a questionRef the grammar cannot read at all.

Exit code is the number of problems (open + orphans + unparsed + stale
exclusions), so `reconcile.py <subject>` in a shell IS the done-check.
"""
import argparse
import collections
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from paper_census import SUBJECTS, census_subject, key_label  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))))
DECKS = os.path.join(ROOT, 'components', 'MarkBank', 'cards')
EXCLUSIONS = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'exclusions')

REF = re.compile(
    r'^(?P<year>\d{4})\s+(?P<level>HL|OL)'
    r'(?:\s+Paper\s+(?P<paper>\d))?'
    r'(?:\s+Section\s+(?P<section>[A-Za-z0-9]+))?'
    # Home Economics files its Section C cards under an elective token —
    # "Section C E1 Q1(a)(i)" — and the elective is not an address the
    # paper numbers by (each elective owns its own question number), so it
    # parses and drops.
    r'(?:\s+E(?P<elective>\d))?'
    r'\s+Q(?P<q>\d{1,2})'
    r'(?:\s*\((?P<p1>[A-Za-z]|[ivxIVX]{2,4})\))?'
    r'(?:\s*\((?P<p2>[ivxIVX]{1,4})\))?'
    r'(?:\s*[-–]\s*\((?P<p3>[ivxIVX]{1,4})\))?')
ROMANS = ['i', 'ii', 'iii', 'iv', 'v', 'vi', 'vii', 'viii', 'ix', 'x',
          'xi', 'xii']


def shipped_cards(subject):
    """[(id, questionRef)] straight out of the deck files that actually ship.

    Split on the literal every emitted card opens with — "...base, kind:" —
    and read the FIRST id in each chunk, which the emitter always writes
    before the rows. Scanning for every id: also caught the ROW ids ("r-3",
    "g-parent1") and paired each with the next card's citation, which
    invented five hundred phantom orphans in Business alone.
    """
    out = []
    for level in ('higher', 'ordinary'):
        path = os.path.join(DECKS, subject, f'{level}.ts')
        if not os.path.exists(path):
            continue
        text = open(path, encoding='utf-8').read()
        for chunk in re.split(r'\.\.\.base,\s*kind:', text)[1:]:
            cid = re.search(r'\bid: "([^"]+)"', chunk)
            ref = re.search(r'questionRef: "([^"]+)"', chunk)
            if cid and ref:
                out.append((cid.group(1), ref.group(1)))
    return out


def parse_ref(ref):
    """One questionRef -> (year, level, paper, section, q, part1, part2, part3).

    The grammar tolerates every format the nine subjects actually print,
    including the Economics habit of suffixing a card's angle after an em dash
    ("Q11(b)(i) — advantage" is still Q11(b)(i)).
    """
    core = re.split(r'\s+[—–]\s+', ref)[0].strip()
    m = REF.match(core)
    if not m:
        return None
    d = m.groupdict()
    return {
        'year': int(d['year']), 'level': d['level'].lower(),
        'paper': f"Paper {d['paper']}" if d['paper'] else None,
        'section': d['section'], 'q': int(d['q']),
        'p1': (d['p1'] or '').lower() or None,
        'p2': (d['p2'] or '').lower() or None,
        'p3': (d['p3'] or '').lower() or None,
    }


def leaf_index(census):
    """{(year, level, paper): [leaf keys]} plus section normalisation."""
    idx = {}
    for p in census['papers']:
        if 'error' in p:
            continue
        idx[(p['year'], p['level'], p.get('paper'))] = \
            [tuple(k) for k in (leaf['key'] for leaf in p['leaves'])]
    return idx


def interpretations(ref, sections_mode):
    """Every reading of the ref's part path, most literal first.

    "(i)" is ambiguous: a single letter i, or the first roman. Physics numbers
    its parts (i)..(x) with no letters at all, so a reading that treats the
    token as a letter matches nothing there while the roman reading matches
    exactly — the census decides, not a per-subject table.
    """
    p1, p2 = ref['p1'], ref['p2']
    outs = []
    if p1 and re.fullmatch(r'[a-z]', p1):
        outs.append((p1, p2))                    # letter, maybe roman
    if p1 and re.fullmatch(r'[ivx]{1,4}', p1) and not p2:
        outs.append((None, p1))                  # roman straight under Q
    if not p1:
        outs.append((None, None))                # whole question
    if not outs:
        outs.append((p1, p2))
    return outs


def match_leaves(ref, leaves, sections_mode):
    """The leaf keys this card's citation covers.

    A ref deeper than the census (the card cites (b)(ii), the paper stops at
    (b)) matches its parent: the scheme priced the romans under one letter and
    the census kept the letter whole. A ref SHALLOWER than the census covers
    everything beneath it, because that is what the card holds.
    """
    q = ref['q']
    covered = []
    for letter, roman in interpretations(ref, sections_mode):
        for k in leaves:
            if sections_mode:
                sec, kq, kl, kr = k
                if ref['section'] and str(sec) != str(ref['section']):
                    continue
            else:
                kq, kl, kr = k[-3], k[-2], k[-1]
            if kq != q:
                continue
            if kl is None and kr is None:
                # The census kept this question whole — it found no part
                # markers under it. A ref of ANY depth on this question lands
                # here: the card cites (A) where the census has the question
                # as one ask, and the ask is in the bank inside that card.
                covered.append(k)
            elif letter is None and roman is None:
                covered.append(k)                       # whole-question card
            elif letter is not None and kl == letter:
                if roman is None or kr == roman or kr is None:
                    covered.append(k)
            elif letter is None and roman is not None:
                if kr == roman or (kl == roman and kr is None):
                    covered.append(k)
        if covered:
            break                       # first interpretation that lands wins
    if ref['p3'] and ref['p2']:
        # A range citation — Q10(b)(iii)-(v) — covers every roman between.
        try:
            lo, hi = ROMANS.index(ref['p2']), ROMANS.index(ref['p3'])
            for k in leaves:
                kq, kl, kr = k[-3], k[-2], k[-1]
                if kq == q and kl == ref['p1'] and kr in ROMANS[lo:hi + 1]:
                    covered.append(k)
        except ValueError:
            pass
    return covered


def load_exclusions(subject):
    path = os.path.join(EXCLUSIONS, f'{subject}.json')
    if not os.path.exists(path):
        return []
    return json.load(open(path, encoding='utf-8'))


def reconcile_subject(subject, census=None):
    census = census or census_subject(subject)
    sections_mode = census['mode'] == 'sections'
    idx = leaf_index(census)
    covered = collections.defaultdict(set)      # paper key -> set(leaf)
    orphans, unparsed = [], []

    cards = shipped_cards(subject)
    for cid, refstr in cards:
        ref = parse_ref(refstr)
        if not ref:
            unparsed.append({'id': cid, 'ref': refstr})
            continue
        candidates = [k for k in idx
                      if k[0] == ref['year'] and k[1] == ref['level']
                      and (ref['paper'] is None or k[2] == ref['paper'])]
        hit = False
        for pk in candidates:
            got = match_leaves(ref, idx[pk], sections_mode)
            if got:
                covered[pk].update(got)
                hit = True
        if not hit:
            orphans.append({'id': cid, 'ref': refstr,
                            'why': 'no paper on disk for that year/level'
                            if not candidates else
                            'cites a part the paper does not print'})

    excluded = collections.defaultdict(set)
    stale = []
    for entry in load_exclusions(subject):
        ref = parse_ref(entry.get('ref', ''))
        landed = False
        if ref:
            for pk in idx:
                if pk[0] == ref['year'] and pk[1] == ref['level'] \
                        and (ref['paper'] is None or pk[2] == ref['paper']):
                    got = [k for k in match_leaves(ref, idx[pk], sections_mode)
                           if k not in covered[pk]]
                    if got:
                        excluded[pk].update(got)
                        landed = True
        if not landed:
            stale.append(entry)

    papers = []
    total = cov = exc = 0
    for pk in sorted(idx, key=lambda k: (k[0], k[1], str(k[2]))):
        leaves = idx[pk]
        open_ = [k for k in leaves
                 if k not in covered[pk] and k not in excluded[pk]]
        total += len(leaves)
        cov += len(leaves) - len(open_) - len(excluded[pk] & set(leaves))
        exc += len(excluded[pk] & set(leaves))
        papers.append({
            'year': pk[0], 'level': pk[1], 'paper': pk[2],
            'leaves': len(leaves),
            'covered': len(leaves) - len(open_) - len(excluded[pk] & set(leaves)),
            'excluded': len(excluded[pk] & set(leaves)),
            'open': [key_label(k) for k in open_],
        })
    return {
        'subject': subject, 'mode': census['mode'],
        'cards': len(cards), 'leaves': total, 'covered': cov,
        'excluded': exc, 'open': total - cov - exc,
        'coveragePct': round(100 * (cov + exc) / total, 1) if total else 0.0,
        'orphans': orphans, 'unparsed': unparsed, 'staleExclusions': stale,
        'papers': papers,
        'censusFlags': sum(len(p.get('flags', [])) for p in census['papers']),
    }


def report(r, show_open=False):
    print(f"{r['subject']}: {r['covered']}/{r['leaves']} paper asks covered "
          f"({r['coveragePct']}%), {r['excluded']} excluded, {r['open']} OPEN "
          f"| {r['cards']} cards, {len(r['orphans'])} orphan(s), "
          f"{len(r['unparsed'])} unparsed, {r['censusFlags']} census flag(s)")
    for o in r['orphans'][:8]:
        print(f"    ORPHAN {o['id']}: \"{o['ref']}\" — {o['why']}")
    for u in r['unparsed'][:4]:
        print(f"    UNPARSED {u['id']}: \"{u['ref']}\"")
    for e in r['staleExclusions'][:4]:
        print(f"    STALE EXCLUSION {e.get('ref')!r}")
    if show_open:
        for p in r['papers']:
            if p['open']:
                tag = f"{p['year']} {p['level'].upper()}" + \
                      (f" {p['paper']}" if p['paper'] else '')
                print(f"    {tag}: open {', '.join(p['open'])}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('subject', nargs='?')
    ap.add_argument('--all', action='store_true')
    ap.add_argument('--json')
    ap.add_argument('--open', action='store_true',
                    help='list every open ask, paper by paper')
    args = ap.parse_args()
    targets = sorted(SUBJECTS) if args.all else [args.subject]
    if not targets or targets == [None]:
        ap.error('name a subject or pass --all')
    results = []
    problems = 0
    for s in targets:
        r = reconcile_subject(s)
        report(r, show_open=args.open)
        results.append(r)
        problems += r['open'] + len(r['orphans']) + len(r['unparsed']) \
            + len(r['staleExclusions'])
    if args.json:
        with open(args.json, 'w', encoding='utf-8') as fh:
            json.dump(results if args.all else results[0], fh,
                      ensure_ascii=False, indent=1)
        print(f'wrote {args.json}')
    sys.exit(min(problems, 120))


if __name__ == '__main__':
    main()
