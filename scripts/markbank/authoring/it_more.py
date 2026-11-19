#!/usr/bin/env python3
"""Card more Italian sittings WITHOUT regenerating the live ones.

    python3 scripts/markbank/authoring/it_more.py 2026 hl --write

it_all.py authored the 350 live cards of 2021-2025 and no longer reproduces
four of them byte for byte (it-2023-hl-b1-4-b, it-2024-hl-a-3-a,
it-2024-hl-b1-4-b, it-2024-hl-b2b-2-a lose their last printed option when
regenerated; the live cards are right). So the live file is APPEND-ONLY: this
script reads authored/italian.json, builds every card one sitting needs —
reading (it_all's builder), listening (it_listen), writing and essays
(it_writing) and the reading asks the generic grammar refuses (READING_LADDERS
below) — keeps every live card exactly as it is, appends the new ones, and
drops the sitting's old exclusions once nothing in it is left uncarded.
"""
import argparse
import json
import os
import sys

DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, DIR)
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(DIR)))

import it_all                                                    # noqa: E402
import it_listen                                                 # noqa: E402
import it_writing                                                # noqa: E402
from it_paper import ItPaper                                     # noqa: E402
from it_rows import split_priced                                 # noqa: E402
from it_scheme import ItScheme                                   # noqa: E402

AUTHORED = os.path.join(ROOT, 'scripts', 'markbank', 'authored', 'italian.json')
EXCLUSIONS = os.path.join(DIR, 'exclusions', 'italian.json')

# "Any three of 5 marks (0,1,3,5)*": the scheme's printed scale for a point
# worth five, "5- mark scale 0,3,5 0,1,3,5 0,3,5,7", on an ask that wants three
# answers. The scale IS the price of the first, second and third answer:
# 1, then 2 more, then 2 more. Read off the printed head, never divided.
READING_LADDERS = {
    (2025, 'hl', 'A', 3, 'b'): ('Any three of 5 marks (0,1,3,5)*', [0, 1, 3, 5]),
    (2026, 'hl', 'B1', 3, None): ('Three of: 7 marks (0,3,5,7) *', [0, 3, 5, 7]),
}


def ladder_card(P, S, year, level, section, item, letter, cards):
    head, scale = READING_LADDERS[(year, level, section, item, letter)]
    ask = next(a for a in S.asks if (a.section, a.item, a.letter) == (section, item, letter))
    text, page = next((t, pg) for sec, it, le, t, pg in P.asks()
                      if (sec, it, le) == (section, item, letter))
    steps = [b - a for a, b in zip(scale, scale[1:])]
    assert sum(steps) == ask.total
    ws = it_writing.Scheme(year, level)
    ws.check(head, *ask.parts[0].answers)
    language = it_all.answer_language(level, text)
    card = {
        'id': it_all.card_id(year, level, section, item, letter),
        'subjectId': 'italian', 'level': it_all.LEVEL_WORD[level], 'year': year,
        'section': it_all.CARD_SECTION[section[0]],
        'topicId': it_all.topic_for(level, section),
        'conceptId': it_all.concept_for(text),
        'questionRef': it_all.question_ref(year, level, section, item, letter),
        'questionText': text, 'tariffModel': {'kind': 'fixed'}, 'totalMarks': ask.total,
        'rows': [{'id': 'r-1', 'kind': 'anyN',
                  'verbatim': 'The answers the scheme accepts in full', 'marks': None,
                  'group': {'claimMax': len(steps), 'perOption': max(steps),
                            'perOptionSteps': steps,
                            'options': list(ask.parts[0].answers)},
                  'contextNote': (f'{it_all.language_note(language)} The scheme prints '
                                  f'"{head}": its scale gives {", ".join(map(str, scale))} '
                                  'marks for none, one, two and three answers.')}],
        'notes': (f'The scheme prints the tariff as {head!r}; the paper prints this ask on '
                  f'page {page} of the question booklet.'),
    }
    source = it_all.source_material(P, section, language, level, year)
    if source:
        card['sourceMaterial'] = source
    cards.append(card)


def question_total_card(P, S, year, level, section, item, letter, cards):
    """An ask whose scheme names how many answers it wants but prints no
    split of its total between them ("Any two of the following" over a bare
    "5 marks"): CARD-STANDARD section 5 - the printed total, self-assessed,
    with the scheme's answers as criteria and its lesser answers quoted."""
    ask = next(a for a in S.asks if (a.section, a.item, a.letter) == (section, item, letter))
    text, page = next((t, pg) for sec, it, le, t, pg in P.asks()
                      if (sec, it, le) == (section, item, letter))
    part = ask.parts[0]
    ws = it_writing.Scheme(year, level)
    ws.check(part.directive, *part.answers, *[t for t, _m in part.rungs])
    language = it_all.answer_language(level, text)
    rows = [{'id': f'r-{k}', 'kind': 'criterion', 'verbatim': a, 'marks': None}
            for k, a in enumerate(part.answers, start=1)]
    lesser = '; '.join(f'{t} {m}m' for t, m in part.rungs)
    split = (f' and the split ({"+".join(map(str, part.split))}), which do not agree'
             if part.split and part.claim and len(part.split) != part.claim else '')
    rows[0]['contextNote'] = (f'{it_all.language_note(language)} The scheme prints '
                              f'"{part.directive}"{split} for {ask.total} marks and does not say what '
                              'one answer is worth: judge your answer against the total.'
                              + (f' It also accepts, for less: {lesser}.' if lesser else ''))
    card = {
        'id': it_all.card_id(year, level, section, item, letter),
        'subjectId': 'italian', 'level': it_all.LEVEL_WORD[level], 'year': year,
        'section': it_all.CARD_SECTION[section[0]],
        'topicId': it_all.topic_for(level, section),
        'conceptId': it_all.concept_for(text),
        'questionRef': it_all.question_ref(year, level, section, item, letter),
        'questionText': text, 'tariffModel': {'kind': 'questionTotal'}, 'totalMarks': ask.total,
        'rows': rows,
        'notes': (f'The scheme prints the tariff as {part.notation!r} under '
                  f'{part.directive!r}; the paper prints this ask on page {page}.'),
    }
    source = it_all.source_material(P, section, language, level, year)
    if source:
        card['sourceMaterial'] = source
    cards.append(card)


TOTAL_ONLY = ('the scheme asks for more answers than its printed tariff divides into',
              'the scheme prints a count and a split that disagree')

# Asks whose scheme prints its accepted answers as ONE line of alternatives
# cut by slashes, with the rate after them: 2023 Higher Section A Q4(b) "Two of
# 4 marks" over "Stimolando/catturando/monitorando/osservando/apportando (2
# marks each)". Each alternative is a cut of that line (checked present).
READING_OPTIONS = {
    (2023, 'hl', 'A', 4, 'b'): {
        'claimMax': 2, 'perOption': 2,
        'options': ['Stimolando', 'catturando', 'monitorando', 'osservando', 'apportando'],
        'note': 'Two of 4 marks: Stimolando/catturando/monitorando/osservando/apportando (2 marks each)'},
}


def options_card(P, S, year, level, section, item, letter, cards):
    o = READING_OPTIONS[(year, level, section, item, letter)]
    ask = next(a for a in S.asks if (a.section, a.item, a.letter) == (section, item, letter))
    text, page = next((t, pg) for sec, it, le, t, pg in P.asks()
                      if (sec, it, le) == (section, item, letter))
    ws = it_writing.Scheme(year, level)
    ws.check(*o['options'], 'Stimolando/catturando/monitorando/osservando/apportando (2 marks each)'
             if (year, level) == (2023, 'hl') else o['options'][0])
    assert o['claimMax'] * o['perOption'] == ask.total
    language = it_all.answer_language(level, text)
    card = {
        'id': it_all.card_id(year, level, section, item, letter),
        'subjectId': 'italian', 'level': it_all.LEVEL_WORD[level], 'year': year,
        'section': it_all.CARD_SECTION[section[0]],
        'topicId': it_all.topic_for(level, section),
        'conceptId': it_all.concept_for(text),
        'questionRef': it_all.question_ref(year, level, section, item, letter),
        'questionText': text, 'tariffModel': {'kind': 'fixed'}, 'totalMarks': ask.total,
        'rows': [{'id': 'r-1', 'kind': 'anyN',
                  'verbatim': 'The answers the scheme accepts in full', 'marks': None,
                  'group': {'claimMax': o['claimMax'], 'perOption': o['perOption'],
                            'options': o['options']},
                  'contextNote': f'{it_all.language_note(language)} The scheme prints "{o["note"]}".'}],
        'notes': (f'The scheme prints the tariff as {ask.parts[0].notation!r}; the paper '
                  f'prints this ask on page {page}.'),
    }
    source = it_all.source_material(P, section, language, level, year)
    if source:
        card['sourceMaterial'] = source
    cards.append(card)


def sitting(year, level):
    P = ItPaper(year, level)
    S = ItScheme(year, level)
    cards, refused = [], []

    def refuse(reason, ref, evidence=''):
        refused.append({'ref': ref, 'reason': reason, 'evidence': evidence})

    reading = []
    it_all._reading(P, S, year, level, reading, refuse)
    for key in READING_LADDERS:
        if key[:2] == (year, level):
            ladder_card(P, S, year, level, *key[2:], reading)
            ref = it_all.question_ref(year, level, key[2], key[3], key[4])
            refused[:] = [r for r in refused if r['ref'] != ref]
    for key in READING_OPTIONS:
        if key[:2] == (year, level):
            options_card(P, S, year, level, *key[2:], reading)
            ref = it_all.question_ref(year, level, key[2], key[3], key[4])
            refused[:] = [r for r in refused if r['ref'] != ref]
    for r in [r for r in refused if r['reason'].startswith(TOTAL_ONLY)]:
        key = next((sec, it, le) for sec, it, le, _t, _p in P.asks()
                   if it_all.question_ref(year, level, sec, it, le) == r['ref'])
        question_total_card(P, S, year, level, *key, reading)
        refused.remove(r)
    cards += [split_priced(c) for c in reading]
    cards += it_listen.cards(year, level, refuse, it_all._row_for, it_all.concept_for)
    cards += it_writing.higher(year) if level == 'hl' else it_writing.ordinary(year)
    return cards, refused


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('year', type=int)
    ap.add_argument('level')
    ap.add_argument('--write', action='store_true')
    args = ap.parse_args()
    live = json.load(open(AUTHORED, encoding='utf-8'))
    ids = {c['id'] for c in live}
    cards, refused = sitting(args.year, args.level)
    new = [c for c in cards if c['id'] not in ids]
    kept = len(cards) - len(new)
    print(f'{args.year} {args.level.upper()}: {len(cards)} cards built, {kept} already live '
          f'(kept as they are), {len(new)} new; {len(refused)} refused')
    for r in refused:
        print('  REFUSED', r['ref'], '|', r['reason'])
    if refused or not args.write:
        return 1 if refused else 0
    with open(AUTHORED, 'w', encoding='utf-8') as fh:
        json.dump(live + new, fh, ensure_ascii=False, indent=1)
    excl = json.load(open(EXCLUSIONS, encoding='utf-8'))
    prefix = f'{args.year} {args.level.upper()} '
    left = [e for e in excl if not e['ref'].startswith(prefix)]
    with open(EXCLUSIONS, 'w', encoding='utf-8') as fh:
        json.dump(left, fh, ensure_ascii=False, indent=1)
        fh.write('\n')
    print(f'wrote {len(live) + len(new)} cards; exclusions {len(excl)} -> {len(left)}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
