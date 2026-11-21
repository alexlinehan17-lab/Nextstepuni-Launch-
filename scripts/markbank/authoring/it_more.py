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
import it_scheme                                                 # noqa: E402

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
    it_scheme.confirm_headings(ask.parts[0], text)
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
    it_scheme.confirm_headings(part, text)
    ws = it_writing.Scheme(year, level)
    ws.check(part.directive, *part.answers, *[t for t, _m in part.rungs])
    language = it_all.answer_language(level, text)
    # Under the headings the scheme prints, where it prints more than one
    # (2018 Higher A Q5: "Sportspeople", "Families").
    answers = ([a if h is None else f'{h} — {a}' for h, group in part.groups for a in group]
               if part.groups else list(part.answers))
    rows = [{'id': f'r-{k}', 'kind': 'criterion', 'verbatim': a, 'marks': None}
            for k, a in enumerate(answers, start=1)]
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
    # 2017 Higher B1 3(b) "Any two of 6 marks (3+3)": four alternatives, each
    # printed on its own line ending in "/", which the reader welded into one.
    (2017, 'hl', 'B1', 3, 'b'): {
        'claimMax': 2, 'perOption': 3,
        'options': ['Non cercare sua madre', 'imparare a vivere da solo', 'non cercare la narratrice',
                    'comportarsi come vorrebbe sua madre'],
        'check': ['smettere cercando/ non la cercare/ non cercare più nemmeno me 2m partial answer'],
        'contextNote': ('The scheme also pays part marks for a shorter answer: “smettere cercando/ non la '
                        'cercare/ non cercare più nemmeno me” 2 marks (“2m partial answer”).')},
    # 2024 Higher B2B 1(b) "Any two of the following 6 marks": each answer is
    # printed in two halves at 3 marks each ("Sembrava un guitto (3m) truccato
    # per una parte da fantasma (3m)"), and any two halves earn the 6.
    (2024, 'hl', 'B2B', 1, 'b'): {
        'claimMax': 2, 'perOption': 3,
        'options': ['Sembrava un guitto', 'truccato per una parte da fantasma',
                    'Aveva una piega amara nella bocca', 'uno sguardo stanco e implorante',
                    '(Il ritratto di Roscio) (era) ingrandito a proporzioni naturali',
                    'lugubremente ritoccato e alluttato (nel vestito e cavatta)'],
        'check': ['guitto 1m', '(sembrava) fantasma 1m', 'truccato 1m'],
        'contextNote': ('The scheme prints each answer in two halves at 3 marks each. It also pays part '
                        'marks for a shorter answer: “guitto” 1 mark; “(sembrava) fantasma” 1 mark; '
                        '“truccato” 1 mark.')},
    # 2024 Ordinary A2 1(b): "One of 5 marks" over the stem "The carrozzine
    # per disabili are", which the reader welded to the first answer.
    (2024, 'ol', 'A2', 1, 'b'): {
        'claimMax': 1, 'perOption': 5,
        'options': ['(Specialised) beach wheelchairs,', 'Larger than (conventional) wheelchairs',
                    'Often very colourful wheelchairs', 'Wheelchairs that have very big (inflatable) wheels',
                    'Submersible wheelchairs', 'Wheelchairs that move freely/roll easily on the sand'],
        'check': ['The carrozzine per disabili are', 'They are wheelchairs 3 mark', 'They are big/colourful 2 marks'],
        'contextNote': ('The scheme also pays part marks for a shorter answer: “They are wheelchairs” 3 marks; '
                        '“They are big/colourful” 2 marks. Each answer completes the scheme’s “The carrozzine '
                        'per disabili are”.')},
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
             if (year, level) == (2023, 'hl') else o['options'][0], *o.get('check', []))
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
                  'contextNote': (f'{it_all.language_note(language)} ' + (
                      o['contextNote'] if 'contextNote' in o else f'The scheme prints "{o["note"]}".'))}],
        'notes': (f'The scheme prints the tariff as {ask.parts[0].notation!r}; the paper '
                  f'prints this ask on page {page}.'),
    }
    source = it_all.source_material(P, section, language, level, year)
    if source:
        card['sourceMaterial'] = source
    cards[:] = [c for c in cards if c['id'] != card['id']]      # replaces the generic reader's card
    cards.append(card)


# Cards whose rows the reader cannot settle, set here from the printed lines
# (each piece asserted in the scheme): the review of 20 Nov.
READING_ROWS = {
    # 2025 Ordinary A2 Q5 "5 marks (5x1) (Any five of eight elements)" over
    # one printed sentence: the scheme does not list the eight elements, so
    # the five marks are judged against the sentence.
    (2025, 'ol', 'A2', 5, None): {
        'tariff': 'questionTotal',
        'rows': [{'id': 'r-1', 'kind': 'criterion', 'marks': None,
                  'verbatim': ('To facilitate inclusive and accessible walking/in nature (events)so that the '
                               'disabled can walk and enjoy nature without (the necessity of) a guide'),
                  'contextNote': ('The scheme prints “5 marks (5x1)” and “(Any five of eight elements)”: '
                                  'one mark for each element of this answer you give, up to five. It does '
                                  'not list the eight elements: judge your answer against the 5 marks.')}],
        'check': ['5 marks (5x1)', '(Any five of eight elements)']},
    # 2019 Ordinary A2 Q4 "10 marks (5+5)": one answer for families, one for
    # shops ("The following answers can only be used for one category").
    (2019, 'ol', 'A2', 4, None): {
        'tariff': 'fixed',
        'rows': [{'id': 'r-1', 'kind': 'anyN', 'marks': None,
                  'verbatim': 'Families — the answers the scheme accepts',
                  'group': {'claimMax': 1, 'perOption': 5, 'options': [
                      'To save money [3] on their shopping [2]', 'To reduce their waste [2] charges [2]',
                      'To carry out their civic duty', '*To educate family members']},
                  'contextNote': ('The scheme prints these answers under “Families:”, and “*Educate can only '
                                  'be used once”. It also pays part marks for a shorter answer: “To help the '
                                  'environment” 3 marks; “To work with the community” 1 mark; “To make a '
                                  'difference” 1 mark; “Promotion” 1 mark; “Education” 1 mark. The scheme '
                                  'prints: “The following '
                                  'answers can only be used for one category”.')},
                 {'id': 'r-2', 'kind': 'anyN', 'marks': None,
                  'verbatim': 'Shops — the answers the scheme accepts',
                  'group': {'claimMax': 1, 'perOption': 5, 'options': [
                      'To increase their customers numbers / To be seen as being more environmentally friendly',
                      '*To educate the community']},
                  'contextNote': 'The scheme prints these answers under “Shops:”.'}],
        'check': ['Families: To save money', 'Shops: To increase', '*Educate can only be used once',
                  'The following answers can only be used for one category', '(To help the environment 3 marks)',
                  '(To work with the community 1 mark)', '(To make a difference 1 mark)', '(Promotion 1 mark)',
                  '(Education 1 mark)']},
    # 2016 Ordinary B1 Q4 prices each detail "2 marks (1+1)", and its one
    # shorter answer "(They are of a part-time nature 1 mark)* only if not
    # mentioned above" is offered once, on the first detail, so it counts once.
    (2016, 'ol', 'B1', 4, None): {
        'tariff': 'fixed',
        'rows': [{'id': 'r-1', 'kind': 'point', 'marks': 2, 'verbatim': 'You work four hours a day',
                  'contextNote': ('The scheme also pays part marks for a shorter answer: “They are of a '
                                  'part-time nature” 1 mark (“* only if not mentioned above”).')},
                 {'id': 'r-2', 'kind': 'point', 'marks': 2, 'verbatim': 'You work three days a week',
                  'contextNote': ('The shorter answer “They are of a part-time nature” counts once, on the '
                                  'first detail.')}],
        'check': ['(They are of a part-time nature 1 mark)* only if not mentioned above']},
}

# A note the reader cannot quote whole: (card id, the text it wrote, the
# printed text), each printed piece asserted in the scheme.
NOTE_FIXES = {
    # 2017 Higher B1 Q5: shorter answers priced for a 7-mark or a 6-mark point.
    'it-2017-hl-b1-5': (r'The scheme also pays part marks for a shorter answer: .*?(?= The scheme prints:)',
                        'The scheme prints for shorter answers: “He has not been very thorough in his search for '
                        'his missing mother 5m (*7m full answer) or 4m (*6m full answer)”; “His mother left him '
                        'without telling him where she was going 3m (*7m full answer) or 2m (*6m full answer)”; '
                        '“He speaks in a negative tone about her 3m (7m full answer) or 2m (*6m full ( answer)”.',
                        ['He has not been very thorough in his search for his missing mother 5m (*7m full answer) '
                         'or 4m (*6m full answer)', 'His mother left him without telling him where she was going 3m '
                         '(*7m full answer) or 2m (*6m full answer)', 'He speaks in a negative tone about her 3m (7m '
                         'full answer) or 2m (*6m full ( answer)']),
    # 2017 Ordinary B2 Q4: the condition runs on to the next printed line.
    'it-2017-ol-b2-4': (r'The scheme also prints: “\(The answers .*?”\.',
                        'The scheme also prints: “(The answers “For six months after purchase” or “In the next six '
                        'months” will only be acceptable as an answer in Question 4. if not used already as an '
                        'answer in Question 3)”.',
                        ['will only be acceptable as an answer in Question 4. if not used already as an answer in '
                         'Question 3)']),
}


def _reading_rows(year, level, reading):
    import re as _re
    for (y, lvl, section, item, letter), o in READING_ROWS.items():
        if (y, lvl) != (year, level):
            continue
        cid = it_all.card_id(year, level, section, item, letter)
        card = next(c for c in reading if c['id'] == cid)
        it_writing.Scheme(year, level).check(*o['check'], *[
            p.split(' — ')[-1] for r in o['rows'] for p in ([r['verbatim']] if r['kind'] != 'anyN' else [])],
            *[x for r in o['rows'] for x in (r.get('group') or {}).get('options', [])])
        rows = [dict(r) for r in o['rows']]
        language = it_all.answer_language(level, card['questionText'])
        rows[0]['contextNote'] = f"{it_all.language_note(language)} {rows[0].get('contextNote', '')}".strip()
        card['rows'], card['tariffModel'] = rows, {'kind': o['tariff']}


# A shorter answer printed with a condition on the line under it, which the
# reader joined into ONE OPTION, so it read as a full answer: the option goes,
# and the note quotes it with its condition, as the reader quotes a starred one.
OPTION_TO_NOTE = {
    # 2016 Ordinary B1 3(b): "(Flexible /enthusiastic/motivated 1 mark)" over
    # "but only if it is the only answer given out of four possibilities )".
    'it-2016-ol-b1-3-b': (
        '(Flexible /enthusiastic/motivated 1 mark) but only if it is the only answer given out of four '
        'possibilities )',
        '“Be available to go on business trips” 1 mark.',
        '“Be available to go on business trips” 1 mark; “Flexible /enthusiastic/motivated” 1 mark. The scheme '
        'adds to the shorter answer “Flexible /enthusiastic/motivated”: “but only if it is the only answer given '
        'out of four possibilities )”.',
        ['(Flexible /enthusiastic/motivated 1 mark)', 'but only if it is the only answer given out of four '
         'possibilities )']),
}


def _note_fixes(cards, year, level):
    import re as _re
    for cid, (option, old, new, pieces) in OPTION_TO_NOTE.items():
        card = next((c for c in cards if c['id'] == cid), None)
        if card is None:
            continue
        it_writing.Scheme(year, level).check(*pieces)
        options = card['rows'][0]['group']['options']
        assert option in options, (cid, options)
        options.remove(option)
        note = card['rows'][0].get('contextNote', '')
        assert note.count(old) == 1, (cid, note)
        card['rows'][0]['contextNote'] = note.replace(old, new)
    for cid, (pattern, printed, pieces) in NOTE_FIXES.items():
        card = next((c for c in cards if c['id'] == cid), None)
        if card is None:
            continue
        it_writing.Scheme(year, level).check(*pieces)
        note = card['rows'][0].get('contextNote', '')
        fixed, n = _re.subn(pattern, printed, note, count=1)
        assert n == 1, (cid, note)
        card['rows'][0]['contextNote'] = fixed


# A full answer the scheme reader joined to the lesser answer printed under it
# (the full answer's line ends without a stop, so it read as wrapped): the two
# printed lines, the joined string asserted exactly, so the split fires on
# nothing else. 2018 Higher B2A 3(b) "(b) 4 marks" prints the full answer and
# then two lesser answers at 3m and 2m, with no "≈" row between.
UNWELD = {
    (2018, 'hl', 'B2A', 3, 'b'): ('Di ricordare ai giovani/ai figli le paure che i loro non hanno',
                                  'Di ricordarci le paure che i giovani/figli non hanno'),
}


def _unweld(S, year, level):
    for (y, lvl, section, item, letter), (full, lesser) in UNWELD.items():
        if (y, lvl) != (year, level):
            continue
        ask = next(a for a in S.asks if (a.section, a.item, a.letter) == (section, item, letter))
        part = ask.parts[0]
        welded = f'{full} {lesser}'
        assert not part.answers and part.rungs and part.rungs[0][0] == welded, (y, section, item, part.rungs)
        it_writing.Scheme(year, level).check(full, lesser)
        part.answers = [full]
        part.rungs = [(lesser, part.rungs[0][1])] + part.rungs[1:]


# A second priced component the reader takes for a lesser answer because it
# is worth less than the first: 2018 Ordinary B Question 4 ask 3 prices "2nd
# prize A gift-card (1m) to download (1m) music (1m) 3 marks" and "3rd prize A
# book (1m) written your favourite / Writer/ of your choice (1m) 2 marks", and
# the question's printed 10 marks need both. The component's line, its
# marks, and the reader's state are all asserted, and the section's own
# arithmetic is re-run.
SPLIT_PARTS = {
    (2018, 'ol', 'B4', 3, None): ('3rd prize A book (1m) written your favourite Writer/ of your choice (1m)', 2),
}


def _split_parts(S, year, level):
    import copy
    for (y, lvl, section, item, letter), (text, marks) in SPLIT_PARTS.items():
        if (y, lvl) != (year, level):
            continue
        ask = next(a for a in S.asks if (a.section, a.item, a.letter) == (section, item, letter))
        p = ask.parts[0]
        assert len(ask.parts) == 1 and len(p.rungs) == 1 and p.rungs[0][1] == marks \
            and text.startswith(p.rungs[0][0]), (section, item, p.rungs)
        it_writing.Scheme(year, level).check(f'{text} {marks} marks')
        q = copy.copy(p)
        q.total, q.split, q.claim, q.directive = marks, None, None, None
        q.stated, q.answers, q.rungs, q.notation = text, [text], [], f'{marks} marks'
        q.seq = q.lead = q.groups = None     # its one answer is the line above, nothing held aside
        p.rungs = []
        ask.parts = [p, q]
        ask.total = p.total + q.total
        asks = [a for a in S.asks if a.section == section]
        if sum(a.total for a in asks) == S.section_totals.get(section):
            for a in asks:
                if a.fault and a.fault.startswith(f'section {section} prices its items'):
                    a.fault = None


# The card each SEC misprint repaired in it_scheme.MISPRINTS touches: the card
# says what the scheme printed and how it is read, in its first row's note.
# (2022 Ordinary B2 Q1 is a live card on main and is never regenerated: Phase 4.)
MISPRINT_CARDS = {
    'it-2026-hl-lb3-7': '7. Any two of: 4 (2+2) marks',
    'it-2018-ol-a1-2': '2 Any two of: 4 marks (2+2)',
    'it-2017-ol-lb3-4': '4. Two required 4 mharc (3+1)',
    'it-2017-ol-lb3-7': '7. Two required 6 (4+2)',
}


def _misprint_notes(cards, year, level):
    from it_scheme import MISPRINTS
    fixes = dict(MISPRINTS.get((year, level), ()))
    for c in cards:
        old = MISPRINT_CARDS.get(c['id'])
        if old is None:
            continue
        assert old in fixes, (c['id'], old)
        note = (f'The scheme prints this line as "{old}", an SEC misprint; it is read as '
                f'"{fixes[old]}", which the printed total of its section confirms.')
        row = c['rows'][0]
        row['contextNote'] = f"{row['contextNote']} {note}" if row.get('contextNote') else note
    for cid, old in MISPRINT_CARDS.items():
        if cid.startswith(f'it-{year}-{level}-'):
            assert any(c['id'] == cid for c in cards), f'{cid}: no such card to carry its misprint note'


# Reading asks whose scheme prices an answer in printed pieces the reader
# cannot cut: 2018 Higher A 1(b) prints its first two pieces on the line that
# carries the tariff ("Fare delle aree giochi/ campi da gioco (1m) in tutti i
# quartieri (1m) 5 marks"), which the reader takes for a heading; A 3(a) prints
# five pieces at (1) under "(1+1+1+1+1)" and the reader takes the first,
# "Perché il bel clima (1m)", for a shorter answer. The pieces as printed, each
# checked against the scheme with split brackets ("(1+1+1+2)") ignored, as the
# build's provenance form ignores them; the scheme's shorter answers quoted.
READING_POINTS = {
    # 2017 Ordinary A2 4(a) prints its answer on the head line and the next,
    # "The (percentage) increase (1) in cyclists (2) 5 marks" / "since 2011
    # (2) (until today)": three priced pieces.
    (2017, 'ol', 'A2', 4, 'a'): {
        'points': [('The (percentage) increase', 1), ('in cyclists', 2), ('since 2011', 2)],
        'lesser': [('2011', 1)],
        'note': 'The scheme prints the last piece as “since 2011 (2) (until today)”.'},
    # 2016 Ordinary B3 Q1 prints its answer on the head line and the next,
    # "30% off on all books (in the collection), 3 marks (1+1+1)" / "until
    # the 13th of November": three elements at one mark each.
    (2016, 'ol', 'B3', 1, None): {
        'points': [('30% off', 1), ('on all books (in the collection),', 1), ('until the 13th of November', 1)],
        'lesser': []},
    (2018, 'hl', 'A', 1, 'b'): {
        'points': [('Fare delle aree giochi/ campi da gioco', 1), ('in tutti i quartieri', 1),
                   ('soprattutto nelle periferie/ nelle zone', 1),
                   ('in cui la qualità delle infrastrutture è scadente/ per migliorarle urbanisticamente/ '
                    'per farle diventare luoghi dove socializzare', 2)],
        'lesser': []},
    (2018, 'hl', 'A', 3, 'a'): {
        'points': [('Perché il bel clima', 1), ('Permette di fare sport/fare esercizio/allenarsi', 1),
                   ('all’aperto/all’aria aperta/ en plein air', 1), ('tutto l’anno', 1),
                   ('senza spendere soldi', 1)],
        'lesser': [('Il tutto a costo zero', 1)]},
    # "(b) 5 marks" over "Potrebbero usare il bonus per recarsi a teatro (2) e
    # assistere ai balletti (1)" and "Perché i biglietti sono cari (2)": three
    # priced pieces (2+1+2); "Perché è caro 2m" its shorter answer.
    # "1. (a) 8 marks" over "Chi I diciottenni /chi ha compiuto 18 anni (2) nel
    # 2016 (2) (2+2+2+2)" and "Come funziona registrarsi entro il 31 gennaio 2017
    # (2) e utilizzarlo entro la fine del 2017 (2)": four pieces at 2 under the
    # scheme's own labels, written "<label> — <point>" (the build traces the point).
    (2017, 'hl', 'A', 1, 'a'): {
        'points': [('Chi — I diciottenni /chi ha compiuto 18 anni', 2), ('Chi — nel 2016', 2),
                   ('Come funziona — registrarsi entro il 31 gennaio 2017', 2),
                   ('Come funziona — e utilizzarlo entro la fine del', 2)],
        'lesser': [],
        # The last piece ends on a line of its own, "2017 (2)", which the
        # build's comparable text drops as a marks-only line: the row is the
        # traceable cut and the printed ending is quoted here.
        'note': 'The scheme prints the last piece as “e utilizzarlo entro la fine del” over “2017 (2)”.'},
    (2017, 'hl', 'A', 4, 'b'): {
        'points': [('Potrebbero usare il bonus per recarsi a teatro', 2), ('e assistere ai balletti', 1),
                   ('Perché i biglietti sono cari', 2)],
        'lesser': [('Perché è caro', 2)]},
}


def _reading_points(year, level, reading):
    import re as _re
    ws = it_writing.Scheme(year, level)
    flat_no_split = _re.sub(r'\(\s*\d+(?:\s*\+\s*\d+)+\s*\)', ' ', ws.flat)
    flat_no_split = ' '.join(flat_no_split.split())
    for (y, lvl, section, item, letter), o in READING_POINTS.items():
        if (y, lvl) != (year, level):
            continue
        cid = it_all.card_id(year, level, section, item, letter)
        card = next(c for c in reading if c['id'] == cid)
        for text, _m in o['points'] + o['lesser']:
            point = text.split(' — ')[-1]
            assert it_writing.flat(point) in flat_no_split, f'{cid}: {point!r} is not in the scheme'
        assert sum(m for _t, m in o['points']) == card['totalMarks'], cid
        language = it_all.answer_language(level, card['questionText'])
        rows = [{'id': f'r-1-{k}', 'kind': 'point', 'verbatim': t, 'marks': m}
                for k, (t, m) in enumerate(o['points'], start=1)]
        rows[0]['contextNote'] = it_all.ladder_note(o['lesser'], language) + (
            f" {o['note']}" if o.get('note') else '')
        card['rows'] = rows
        card['tariffModel'] = {'kind': 'fixed'}


# Symbol-font glyphs the Italian schemes print as private-use code points
# (0xF000 + the font's own code), each settled by cropping the glyph from the
# page: Wingdings 0xE8 is the heavy right arrow in 2017 Higher's scheme p. 16
# ("he betrays him ➔ Secret+driving lesson"), the only Italian scheme that
# prints it (every occurrence checked to be Wingdings).
SETTLED_GLYPHS = {'\uf0e8': '➔'}


def _settle_glyphs(value):
    if isinstance(value, str):
        return ''.join(SETTLED_GLYPHS.get(ch, ch) for ch in value)
    if isinstance(value, list):
        return [_settle_glyphs(v) for v in value]
    if isinstance(value, dict):
        return {k: _settle_glyphs(v) for k, v in value.items()}
    return value


def sitting(year, level):
    P = ItPaper(year, level)
    S = ItScheme(year, level)
    _unweld(S, year, level)
    _split_parts(S, year, level)
    cards, refused = [], []

    def refuse(reason, ref, evidence=''):
        refused.append({'ref': ref, 'reason': reason, 'evidence': evidence})

    reading = []
    it_all._reading(P, S, year, level, reading, refuse)
    _reading_points(year, level, reading)
    _reading_rows(year, level, reading)
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
    _misprint_notes(cards, year, level)
    _note_fixes(cards, year, level)
    cards = [_settle_glyphs(c) for c in cards]
    return cards, refused


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('year', type=int)
    ap.add_argument('level')
    ap.add_argument('--write', action='store_true')
    ap.add_argument('--refresh', action='append', default=[],
                    help='rebuild this card in place; only a card this lane added, never one live on main')
    args = ap.parse_args()
    live = json.load(open(AUTHORED, encoding='utf-8'))
    ids = {c['id'] for c in live}
    cards, refused = sitting(args.year, args.level)
    if args.refresh:
        import subprocess
        on_main = {c['id'] for c in json.loads(subprocess.run(
            ['git', 'show', 'origin/main:scripts/markbank/authored/italian.json'],
            cwd=ROOT, capture_output=True, text=True, check=True).stdout)}
        built = {c['id']: c for c in cards}
        for rid in args.refresh:
            assert rid not in on_main, f'{rid} is live on main: live cards are never regenerated'
            assert rid in ids and rid in built, f'{rid}: not in the deck and this sitting both'
            live = [built[rid] if c['id'] == rid else c for c in live]
            print('refreshed', rid)
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
