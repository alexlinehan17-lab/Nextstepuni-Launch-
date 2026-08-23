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

HEAD = re.compile(
    r'^(?P<year>\d{4})\s+(?P<level>HL|OL)'
    r'(?:\s+Paper\s+(?P<paper>\d))?'
    r'(?:\s+Section\s+(?P<section>[A-Za-z0-9]+))?'
    # Home Economics files Section C under an elective token ("Section C E1
    # Q1(a)(i)"); the elective is not an address the paper numbers by.
    r'(?:\s+E(?P<elective>\d))?'
    r'\s+(?:Q(?P<q>\d{1,2})(?P<alt>-alt)?|(?P<abq>ABQ))')
# What may follow the question number: part tokens, separated by commas,
# "and", or a range dash. "Q3(c)(i), (ii)" covers two romans; "Q6(a)–(e)"
# covers five letters; "Q9(vii)–(viii)" two romans with no letter above them.
PART_TOKEN = re.compile(r'\s*(?:\(\s*([A-Za-z]{1,4})\s*\)|([\u2013\u2014-])|(,|\band\b))')
ROMANS = ['i', 'ii', 'iii', 'iv', 'v', 'vi', 'vii', 'viii', 'ix', 'x',
          'xi', 'xii']
LETTERS = 'abcdefghijkl'


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


def _classify(tok):
    """letter or roman? A lone i/v/x is a roman FIRST; the census decides the
    rest at match time (Physics numbers parts (i)..(x) with no letters)."""
    t = tok.lower()
    if len(t) == 1 and t in LETTERS and t not in 'ivx':
        return 'letter'
    if all(c in 'ivx' for c in t):
        return 'roman'
    return 'letter' if len(t) == 1 else None


def parse_ref(ref):
    """One questionRef -> head fields + every part path it names.

    The grammar tolerates every format the nine subjects print, including the
    Economics habit of suffixing a card's angle after an em dash
    ("Q11(b)(i) — advantage" is still Q11(b)(i)) and compound citations
    ("Q4(ii), (iii)"; "Q6(a)–(e)"), which cover every path they name.
    """
    core = re.split(r'\s+[\u2014\u2013-]\s+', ref)[0].strip()
    m = HEAD.match(core)
    if not m:
        return None
    d = m.groupdict()
    q = 'ABQ' if d['abq'] else int(d['q'])
    if d['alt'] and isinstance(q, int):
        q = -q
    paths, cur_letter, cur_roman, dash = [], None, None, False
    pos = m.end()
    while pos < len(core):
        t = PART_TOKEN.match(core, pos)
        if not t:
            break
        pos = t.end()
        tok, is_dash, is_sep = t.group(1), t.group(2), t.group(3)
        if is_dash:
            dash = True
            continue
        if is_sep:
            continue
        cls = _classify(tok)
        tok = tok.lower()
        if cls == 'letter':
            if dash and cur_letter and cur_roman is None:
                lo, hi = LETTERS.index(cur_letter), LETTERS.index(tok)
                for x in LETTERS[lo + 1:hi + 1]:
                    paths.append((x, None))
            else:
                paths.append((tok, None))
            cur_letter, cur_roman, dash = tok, None, False
        elif cls == 'roman':
            if dash and cur_roman in ROMANS and tok in ROMANS:
                lo, hi = ROMANS.index(cur_roman), ROMANS.index(tok)
                for x in ROMANS[lo + 1:hi + 1]:
                    paths.append((cur_letter, x))
            elif paths and paths[-1] == (cur_letter, None) and cur_letter:
                paths[-1] = (cur_letter, tok)
            else:
                paths.append((cur_letter, tok))
            cur_roman, dash = tok, False
        else:
            break
    if not paths:
        paths = [(None, None)]
    return {
        'year': int(d['year']), 'level': d['level'].lower(),
        'paper': f"Paper {d['paper']}" if d['paper'] else None,
        'section': d['section'], 'q': q, 'paths': paths,
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


def _paths_with_fallback(ref):
    """Each cited path, plus the letter reading of an ambiguous lone roman.

    "(i)" parses as a roman first; if the census never printed that roman the
    token may be the ninth LETTER (Chemistry's Q4 runs (a)-(l)), so the letter
    reading is tried second — the census decides, not a per-subject table.
    """
    out = [ref['paths']]
    flipped = [( (r, None) if r and not l and len(r) == 1 else (l, r) )
               for l, r in ref['paths']]
    if flipped != ref['paths']:
        out.append(flipped)
    return out


def match_leaves(ref, leaves, sections_mode):
    """The leaf keys this card's citation covers.

    A ref deeper than the census (the card cites (b)(ii), the paper stops at
    (b)) matches its parent: the scheme priced the romans under one letter and
    the census kept the letter whole. A ref SHALLOWER than the census covers
    everything beneath it, because that is what the card holds.
    """
    q = ref['q']
    for paths in _paths_with_fallback(ref):
        covered = []
        for letter, roman in paths:
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
                    # The census kept this question whole — a ref of ANY depth
                    # on it lands here: the ask is in the bank, inside the card.
                    covered.append(k)
                elif letter is None and roman is None:
                    covered.append(k)                   # whole-question card
                elif letter is not None and kl == letter:
                    if roman is None or kr == roman or kr is None:
                        covered.append(k)
                elif letter is None and roman is not None:
                    if kr == roman or (kl == roman and kr is None):
                        covered.append(k)
        if covered:
            return covered
    # Roman-major questions (Physics) sometimes gain a letter in the CITATION
    # that the paper never prints as a key — the census demoted it as an
    # enumeration. When the question has no lettered keys at all, the roman
    # alone is the address.
    for letter, roman in ref['paths']:
        if letter and roman:
            covered = [k for k in leaves
                       if k[-3] == q and k[-2] is None and k[-1] == roman
                       and not any(o[-3] == q and o[-2] for o in leaves)]
            if covered:
                return covered
    return []


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


BASELINE = os.path.join(ROOT, 'scripts', 'markbank', 'coverage-baseline.json')


def baseline_check(results):
    """Coverage is a ratchet: it may only move up, and only deliberately.

    The committed baseline records covered/leaves/cards per subject. A deck
    change that drops coverage — a card deleted, a citation broken, a build
    gate silently eating cards — fails here until someone regenerates the
    baseline WITH the drop in front of them. The paired test in
    test/markBankCoverage.test.ts pins deck card counts to this file, so the
    baseline cannot simply go stale: any deck change forces a regeneration,
    and regeneration runs this ledger.
    """
    if not os.path.exists(BASELINE):
        return [f'no baseline at {BASELINE} — run with --baseline write']
    base = json.load(open(BASELINE, encoding='utf-8'))
    problems = []
    for r in results:
        b = base.get(r['subject'])
        if not b:
            problems.append(f"{r['subject']}: not in baseline")
            continue
        if r['covered'] < b['covered']:
            problems.append(f"{r['subject']}: covered fell {b['covered']} -> "
                            f"{r['covered']} — a paper ask lost its card")
        if len(r['orphans']) > b['orphans']:
            problems.append(f"{r['subject']}: orphans grew {b['orphans']} -> "
                            f"{len(r['orphans'])} — a citation broke")
    return problems


def baseline_write(results):
    data = {r['subject']: {
        'leaves': r['leaves'], 'covered': r['covered'], 'open': r['open'],
        'orphans': len(r['orphans']), 'cards': r['cards'],
        'coveragePct': r['coveragePct'],
    } for r in results}
    with open(BASELINE, 'w', encoding='utf-8') as fh:
        json.dump(data, fh, indent=1, sort_keys=True)
        fh.write('\n')
    print(f'baseline written: {BASELINE}')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('subject', nargs='?')
    ap.add_argument('--all', action='store_true')
    ap.add_argument('--json')
    ap.add_argument('--open', action='store_true',
                    help='list every open ask, paper by paper')
    ap.add_argument('--baseline', choices=['write', 'check'],
                    help='write or enforce the coverage ratchet')
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
    if args.baseline == 'write':
        baseline_write(results)
    elif args.baseline == 'check':
        bad = baseline_check(results)
        for b in bad:
            print(f'RATCHET: {b}')
        problems += len(bad)
    sys.exit(min(problems, 120))


if __name__ == '__main__':
    main()
