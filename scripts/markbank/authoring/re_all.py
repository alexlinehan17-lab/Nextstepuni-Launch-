#!/usr/bin/env python3
"""Author every Religious Education ask the paper prints and the scheme prices.

    python3 scripts/markbank/authoring/re_all.py --report    # counts, refusals
    python3 scripts/markbank/authoring/re_all.py > scripts/markbank/authored/religious-education.json

Census-driven. The papers print 288 asks across 2021-2025 and the schemes
answer every one of them, so this walks the census and refuses, loudly, rather
than choosing what to card.

WHAT ONE CARD IS
----------------
One printed ask. Its question comes from the PAPER (re_paper.py), its marking
points from the SCHEME (re_scheme.py), and the two are paired by wording as
well as by key — Law 4 — which in this subject agrees on all 288 pairs at a
score no lower than 0.50. The paper's printed tariff and the scheme's printed
tariff also agree on all 288, which is the cross-document check that says the
pairing is real.

THE TARIFF: `questionTotal`, always
-----------------------------------
Every ask carries ONE printed mark — 20M, 40M, 80M, or "20M x 2" meaning two
answers at twenty. Not one of the corpus's 799 content bullets carries a mark
of its own. So the marks live on the question and the rows carry `marks: null`,
which is exactly what `questionTotal` means and what the session screen already
says out loud: "the scheme does not divide those marks between its parts — so
no invented per-point values are shown." Giving a row a value here would be the
sixth guessed tariff in this bank's history.

"• Etc." — WHAT A CARD DOES WITH IT
------------------------------------
The scheme closes most of its lists with a bullet reading only "Etc.". That is
the SEC saying the list is not exhaustive, not a marking point: shipping it as
one would put the word "Etc." in front of a student as something to have
written. So the bullet is DROPPED, and the fact it carried is kept — every row
of an ask whose list ended that way is marked `openList`, which is the card
model's own field for "the scheme's list is non-exhaustive" and which turns on
the session's "I wrote a different valid point" path. An "etc." INSIDE a
bullet stays where the examiner put it: that is the bullet's own wording.

REFUSALS
--------
Every one is a named bucket, counted and exampled by --report:
  * the paper prints no text for the ask;
  * the scheme prints no tariff for it (never guessed);
  * the scheme states no marking points under its criteria heading;
  * a marking point cannot be traced back to the scheme markdown the build
    checks against;
  * the ask points at printed matter no card can carry.
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

from re_paper import RePaper                                 # noqa: E402
from re_scheme import ReScheme, GRID_WORDS                   # noqa: E402
from re_topics import SECTIONS, topic_for, concept_for       # noqa: E402
from align import bag, score                                 # noqa: E402
import cardlint                                              # noqa: E402

YEARS = (2021, 2022, 2023, 2024, 2025)
LEVELS = ('hl', 'ol')
LEVEL_WORD = {'hl': 'higher', 'ol': 'ordinary'}

# The pairing floor. align.py's own default is 0.55 for a wording-only join;
# here the key agrees as well, so the floor is the evidence threshold below
# which the pair would be resting on the key alone — which Law 4 forbids.
PAIR_FLOOR = 0.40


def card_id(year, level, key):
    section, q, letter, roman = key
    parts = ['re', str(year), level, section.lower()]
    if q is not None:
        parts.append(str(q))
    parts.append(letter)
    if roman:
        parts.append(roman)
    return '-'.join(parts)


def question_ref(year, level, key):
    section, q, letter, roman = key
    ref = f'{year} {level.upper()} Section {section} Q'
    if q is not None:
        ref += str(q)
    ref += f'({letter})'
    if roman:
        ref += f'({roman})'
    return ref


def build(verbose=False):
    cards = []
    refused = collections.Counter()
    examples = collections.defaultdict(list)
    pairs = []

    def refuse(reason, ref):
        refused[reason] += 1
        examples[reason].append(ref)

    for year in YEARS:
        for level in LEVELS:
            P = RePaper(year, level)
            S = ReScheme(year, level)
            pkeys = list(P.asks)
            pbags = [bag(P.asks[k]) for k in pkeys]

            for sec, q, letter, roman, line, why in S.refused:
                refuse(why, f'{year} {level} {sec} {q or ""}{letter}{roman or ""}')

            for ask in S.asks:
                key = ask.key
                ref = question_ref(year, level, key)
                question = P.asks.get(key)
                if not question:
                    refuse('the paper prints no text for this ask', ref)
                    continue

                # Law 4: the pairing is EARNED. The scheme reprints the ask it
                # is marking, so scoring that reprint against every ask on the
                # paper says whether this key's pairing is the best one — a
                # key join alone is what once handed Biology Q6(a) the answers
                # to Q7.
                cue = bag(ask.cue)
                ranked = sorted(((score(cue, pb), k) for k, pb in zip(pkeys, pbags)),
                                key=lambda t: t[0], reverse=True)
                best, best_key = ranked[0] if ranked else (0.0, None)
                own = next((s for s, k in ranked if k == key), 0.0)
                if best_key != key or own < PAIR_FLOOR:
                    refuse('the scheme cue matches another ask better than its own',
                           f'{ref} (own {own:.2f}, best {best:.2f})')
                    continue
                pairs.append((ref, own))

                topic = topic_for(ask.section)
                if not topic:
                    refuse('the paper section is not a syllabus section', ref)
                    continue

                points = [p for p in ask.points if not GRID_WORDS.search(p)]
                if len(points) != len(ask.points):
                    refuse('a marking point carried band-grid wording', ref)
                    continue
                if not points:
                    refuse('the scheme states no marking points for this ask', ref)
                    continue

                stem = P.stem(key)
                joined = ' '.join(f'{stem or ""} {question}'.split())
                # Card lint's own gates, applied before the card is written.
                # This subject has no figures at all — the measurement found
                # every image in the papers to be SEC header furniture or
                # credited clipart — so an ask that points at printed matter
                # is one no card can carry.
                if (cardlint.FIG_REF.search(joined)
                        and not cardlint.SELF_WORK.search(joined)
                        and not cardlint.NO_DEPENDENCY.search(joined)) \
                        or cardlint.NAMES_LETTERS.search(joined):
                    refuse('the ask points at printed matter the card cannot carry', ref)
                    continue

                context = ' '.join(x for x in ([ask.lead] + ask.notes) if x).strip()
                rows = []
                for i, point in enumerate(points, start=1):
                    row = {'id': f'r-{i}', 'kind': 'point',
                           'verbatim': point, 'marks': None}
                    if ask.open_list:
                        # The scheme's own "• Etc." — the list is not
                        # exhaustive, and the student may claim a point of
                        # their own that the examiner would have paid for.
                        row['openList'] = True
                    if i == 1 and context:
                        row['contextNote'] = context
                    rows.append(row)

                card = {
                    'id': card_id(year, level, key),
                    'subjectId': 'religious-education',
                    'level': LEVEL_WORD[level],
                    'year': year,
                    'section': ask.section,
                    'topicId': topic,
                    'conceptId': concept_for(question),
                    'questionRef': ref,
                    'questionText': question,
                    'tariffModel': {'kind': 'questionTotal'},
                    'totalMarks': ask.total,
                    'rows': rows,
                    'notes': (f'The scheme prints the tariff as {ask.notation!r} and '
                              f'divides it between no marking point; the paper prints '
                              f'{P.marks.get(key)} marks for the same ask.'),
                }
                if stem and len(stem) >= 20:
                    card['stem'] = stem
                cards.append(card)
    return cards, refused, examples, pairs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--report', action='store_true')
    ap.add_argument('--all', action='store_true',
                    help='with --report, list every refusal rather than three')
    args = ap.parse_args()
    cards, refused, examples, pairs = build()
    if args.report:
        from paper_census import census_subject
        census = census_subject('religious-education')
        total = sum(p['leafCount'] for p in census['papers'])
        print(f'{len(cards)} card(s) against {total} paper asks '
              f'({100 * len(cards) / total:.1f}%)')
        worst = min(pairs, key=lambda t: t[1]) if pairs else None
        if worst:
            print(f'pairing: {len(pairs)} pairs, weakest {worst[0]} at {worst[1]:.2f}')
        rows = sum(len(c['rows']) for c in cards)
        openl = sum(1 for c in cards if c['rows'][0].get('openList'))
        print(f'{rows} marking rows, {openl} card(s) whose scheme list ends "Etc."')
        by_section = collections.Counter(c['topicId'] for c in cards)
        for tid, n in sorted(by_section.items()):
            print(f'   {tid:6} {SECTIONS[tid[-1].upper()][:48]:<50} {n}')
        for reason, n in refused.most_common():
            print(f'   {n:4} REFUSED  {reason}')
            for e in examples[reason][:60 if args.all else 3]:
                print(f'             {e}')
        return 0
    json.dump(cards, sys.stdout, ensure_ascii=False, indent=1)
    return 0


if __name__ == '__main__':
    sys.exit(main())
