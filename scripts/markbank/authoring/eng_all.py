#!/usr/bin/env python3
"""Author every Engineering part the scheme states and prices.

    python3 scripts/markbank/authoring/eng_all.py            # emit JSON
    python3 scripts/markbank/authoring/eng_all.py --report   # counts, refusals

Census-driven, like Computer Science: 806 asks is too many to enumerate by
hand, and every card is the scheme's own text against the paper's own ask.

WHAT THE TARIFF NOTATION MEANS, and the deck convention each maps to. All four
are the paper's own arithmetic; none is inferred.

  "Any two @ 8 + 8"      the candidate picks two from the scheme's list and
  "Any three parts @ 5"  each is worth the same -> an anyN row whose group is
                         the list, claimMax two, perOption eight.

  "3 + 2" with as many   the scheme has priced each point in turn -> one row
  points as terms        per point carrying its own mark.

  "3 + 2" with MORE      the split is ORDERED, not per point: the question
  points than terms      asks for two safety precautions, the scheme lists
                         five, and the first answer given earns 3 and the
                         second 2. Which point it is does not decide its
                         value, so per-row values do not exist -- orderedSplit,
                         rows carrying none, exactly as Chemistry's "ANY TWO:
                         (3 + 2)" already does.

  "5" with one point     one row at five.
  "5" with several       the points are alternatives and any one earns the
                         five -> an alt row.

REFUSALS, each the rule already in force elsewhere:

  * the ask is an option the candidate chooses BETWEEN, not a question. The
    papers print those with roman markers -- "Select any two of the plastic
    materials listed below: (i) Polyvinyl Chloride (PVC), (ii) Nylon," -- and
    the census counts them as leaves because that is what they look like.
  * the scheme states nothing at this key or above it,
  * it prints no tariff that reads one way,
  * the wording files under no syllabus topic.
"""
import argparse
import collections
import json
import os
import re
import sys

DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, DIR)
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(DIR)))

import reconcile as R                                       # noqa: E402
from paper_census import census_subject                     # noqa: E402
from lib import Author, Refused                             # noqa: E402
from eng_scheme import EngScheme                            # noqa: E402
from eng_topics import topic_for, concept_for               # noqa: E402
import cardlint                                             # noqa: E402

MAX_ROWS = 12
# An "ask" that is really one of the options the question lists. It has no
# sentence in it: "Nylon,", "Full hybrid;", "Ferdinand Porsche", "Basin".
NOT_AN_ASK = re.compile(r'^[^.?!]{0,40}[,;.]?$')
# The examiner talking to the examiner rather than stating an answer.
CREDIT_RULE = re.compile(
    r'^(?:award|allow|accept|max\b|total\b|note:|any other|or\b)', re.I)


def looks_like_an_ask(text):
    t = ' '.join((text or '').split())
    if not t:
        return False
    if len(re.findall(r'[a-z]{3,}', t)) < 4:
        return False
    return not NOT_AN_ASK.match(t) or len(t) > 45


def cardable(points):
    """The marking points a card may claim, the examiner's asides removed."""
    out = []
    for p in points:
        t = ' '.join(p.split())
        if len(t) < 3 or CREDIT_RULE.match(t):
            continue
        out.append(t)
    return out


def cardable_indexed(points):
    """(index, text) into the SCHEME's own list, not into a filtered copy.

    lib.card rebuilds its candidates from the scheme and `use` selects into
    that, so a filtered copy would silently shift every index past the first
    thing removed -- the fault that put a lead-in on nineteen Computer Science
    cards.
    """
    out = []
    for i, p in enumerate(points):
        t = ' '.join(p.split())
        if len(t) < 3 or CREDIT_RULE.match(t):
            continue
        out.append((i, t))
    return out


def resolve(S, q, letter, roman):
    """The nearest PRICED key at or above this leaf, and what it covers.

    Requiring the points and the tariff at the SAME key found 56 cards in 806
    asks, because at Ordinary Level the two are almost never at the same
    depth: the scheme prices the letter and answers its romans.
    """
    for key in ((q, letter, roman), (q, letter, None), (q, None, None)):
        if S.tariff(*key):
            keep = cardable_indexed(S.points_under(*key))
            if keep:
                return key, keep
    return None, []


def rows_for(notation, total, rule, points):
    """(row kind, marks per row, tariff model) for a part, or None to refuse."""
    points = points[:MAX_ROWS]
    if rule:
        n, per = rule
        if n <= len(points):
            return ('anyN', None, {'kind': 'fixed'}, (n, per))
        return None
    terms = [int(x) for x in re.findall(r'\d{1,2}', notation or '')]
    if len(terms) > 1:
        if len(terms) == len(points):
            return ('point', terms, {'kind': 'fixed'}, None)
        if len(points) > len(terms):
            return ('point', None,
                    {'kind': 'orderedSplit', 'notation': notation}, None)
        return None
    if len(points) == 1:
        return ('point', [total], {'kind': 'fixed'}, None)
    return ('alt', [total], {'kind': 'fixed'}, None)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--report', action='store_true')
    ap.add_argument('--all', action='store_true')
    args = ap.parse_args()

    idx = R.leaf_index(census_subject('engineering'))
    cards, refused = [], collections.Counter()
    examples = collections.defaultdict(list)

    for (year, level, _), leaves in sorted(idx.items()):
        A = Author('engineering', year, level)
        S = EngScheme(year, level)
        seen = set()
        for leaf in sorted(leaves):
            q, letter, roman = leaf[0], leaf[1], leaf[2]
            ref = (f'{year} {level.upper()} Q{q}'
                   + (f'({letter})' if letter else '')
                   + (f'({roman})' if roman else ''))
            try:
                ask = A.paper.text(q, letter, roman) or ''
            except Exception:                                # noqa: BLE001
                ask = ''

            def note(reason):
                refused[reason] += 1
                examples[reason].append(f'{ref}: {" ".join(ask.split())[:70]}')

            if not looks_like_an_ask(ask):
                note('an option the question lists, not an ask')
                continue
            key, keep = resolve(S, q, letter, roman)
            points = [t for _, t in keep]
            if not key:
                note('the scheme states and prices nothing at this key or above')
                continue
            if key in seen:
                continue
            lead = S.lead(*key) or ''
            topic, _ = topic_for(f'{ask} {lead}')
            if not topic:
                note('files under no syllabus topic')
                continue
            # Card lint's own two gates, applied BEFORE the card is written
            # rather than after it is flagged. Engineering asks about printed
            # matter constantly -- "Describe, with the aid of a diagram(s), a
            # suitable mechanism", "Identify the crystal structures A, B and
            # C" -- and this subject has had no figure pass yet, so a card
            # that points at a picture it cannot show is refused.
            stem = ''
            try:
                stem = A.paper.stem(q, key[1]) or A.paper.stem(q) or ''
            except Exception:                                # noqa: BLE001
                pass
            # The same join lib.card will make. A part that is only a cue --
            # "Answer any three of the following:" -- hands its ask to the
            # romans beneath it, and the diagram reference arrives from one of
            # THEM: checking the cue alone let three cards through pointing at
            # a mechanism they could not show.
            whole = ask
            if key[2] is None and len(' '.join(ask.split())) < 40:
                # lib.card's own rule, copied so the two agree: the children
                # of the CITED key, which for a whole-question card is every
                # lettered part beneath it.
                kids = sorted((k for k in A.paper.parts
                               if k[0] == q
                               and (k[1] == key[1] if key[1]
                                    else k[1] is not None or k[2])
                               and (k[1], k[2]) != (key[1], key[2])),
                              key=lambda k: (k[1] or '', k[2] or ''))
                whole = ' '.join([ask] + [(A.paper.text(*k) or '') for k in kids])
            joined = ' '.join(f'{stem} {whole}'.split())
            if ((cardlint.FIG_REF.search(joined)
                 and not cardlint.SELF_WORK.search(joined)
                 and not cardlint.NO_DEPENDENCY.search(joined))
                    or cardlint.NAMES_LETTERS.search(joined)):
                note('points at printed matter the card cannot carry')
                continue
            shape = rows_for(S.notation(*key), S.tariff(*key), S.rule(*key),
                             points)
            if not shape:
                note('the printed split does not fit the points stated')
                continue
            kind, marks, model, group = shape
            cid = (f'eng-{year}-{level}-q{q}'
                   + (f'-{key[1]}' if key[1] else '')
                   + (f'-{key[2]}' if key[2] else ''))
            try:
                if kind == 'anyN':
                    n, per = group
                    A.card(*key, topic=topic, concept=concept_for(ask),
                           source='table', card_id=cid,
                           use=[[i for i, _ in keep[:MAX_ROWS]]],
                           marks=[n * per], tariff='fixed',
                           row_kind='anyN', total=n * per,
                           stem=not cardlint.label_junk(stem),
                           notes=f'The scheme prints {S.notation(*key)!r}.')
                elif model['kind'] == 'orderedSplit':
                    # Rows carry no marks and the total is given, which is the
                    # shape lib already has for a scale: `ladder`. Which point
                    # it is does not decide its value, so inventing one per row
                    # is the thing being avoided.
                    A.card(*key, topic=topic, concept=concept_for(ask),
                           source='table', card_id=cid,
                           use=[i for i, _ in keep[:MAX_ROWS]],
                           tariff='orderedSplit', notation=model['notation'],
                           ladder=S.tariff(*key),
                           stem=not cardlint.label_junk(stem))
                else:
                    A.card(*key, topic=topic, concept=concept_for(ask),
                           source='table', card_id=cid,
                           use=[i for i, _ in keep[:MAX_ROWS]],
                           marks=marks, tariff='fixed', total=S.tariff(*key),
                           stem=not cardlint.label_junk(stem))
                seen.add(key)
            except Refused as exc:
                note(str(exc).split(':', 1)[-1].strip()[:60])
        cards.extend(A.cards)

    if args.report:
        total = sum(len(v) for v in idx.values())
        print(f'{len(cards)} card(s) from {total} asks')
        limit = 60 if args.all else 3
        for reason, n in refused.most_common():
            print(f'   {n:4} REFUSED  {reason}')
            for e in examples[reason][:limit]:
                print(f'             {e}')
        return 0
    print(json.dumps(cards, ensure_ascii=False, indent=1))
    return 0


if __name__ == '__main__':
    sys.exit(main())
