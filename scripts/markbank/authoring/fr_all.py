#!/usr/bin/env python3
"""Author every French ask the papers print and the schemes answer.

    python3 scripts/markbank/authoring/fr_all.py --report
    python3 scripts/markbank/authoring/fr_all.py --exclusions   # rewrite them
    python3 scripts/markbank/authoring/fr_all.py > scripts/markbank/authored/french.json

Census-driven: the ten sittings print 551 leaf asks across two booklets each,
and this walks that census rather than choosing what to card.

WHAT ONE CARD IS
----------------
One printed ask. Its question comes from the PAPER (fr_paper.py) and its
marking points from the SCHEME (fr_scheme.py), paired by wording rather than by
key — Law 4 — which in this subject is not a safety net but the only way the
ask can be found at all: the reading passage is printed in NUMBERED PARAGRAPHS
at the same margin as the questions, so "1." on the page is as likely to open
the passage as the ask.

THE PASSAGE TRAVELS WITH THE CARD
---------------------------------
Every reading-comprehension answer is a quotation from a passage printed only
in the question paper. A card that asks for it without carrying the passage is
unanswerable, so each one binds `sourceMaterial` to the exact pages of its own
comprehension in the QUESTION paper — never the scheme, which is where the
answers are.

THE ANSWER LANGUAGE IS PART OF THE ASK
--------------------------------------
Section A sets some questions in French and some in Irish and English, and the
scheme penalises an answer in the wrong one. Every card says which, read from
the language its own question is printed in (fr_topics.answer_language).

THE LADDER, AND WHY IT IS A NOTE
--------------------------------
A French answer is marked on a ladder: the full answer at five, a shorter form
at four, a fragment at three, two or one. The full-mark answers are the card's
rows. The rungs beneath are stated on the row as a note, verbatim and with the
marks the scheme prints, because `RowKind` has no kind for a rung worth less
than the row above it and the type says why: "Add it together with its
renderer, not before."

REFUSALS
--------
Every one is a named bucket, counted and exampled by --report, and every
refusal that lands on a census leaf becomes an exclusions entry carrying the
scheme evidence for it (--exclusions writes them).
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

from fr_paper import FrPaper                                  # noqa: E402
from fr_scheme import FrScheme                                # noqa: E402
from fr_topics import (topic_for, concept_for, answer_language,  # noqa: E402
                       language_note, CLOZE)
from paper_census import census_subject                       # noqa: E402
import cardlint                                               # noqa: E402

SUBJECT = 'french'
YEARS = (2021, 2022, 2023, 2024, 2025)
LEVELS = ('hl', 'ol')
LEVEL_WORD = {'hl': 'higher', 'ol': 'ordinary'}
LEVEL_TITLE = {'hl': 'Higher', 'ol': 'Ordinary'}

# The most options one card may show, from MAX_LONG_OPTION_ROWS in
# types/markBank.ts. The opinion ask at the end of a Higher comprehension lists
# up to twenty-one points for one side of an argument, and a card that showed
# them all would be a wall of text rather than a question. The list is trimmed
# in the SEC's own printed order and the trim is DISCLOSED on the row, which is
# the pattern the bank already uses for an over-cap menu; the scheme closes
# these lists with "Etc., etc." itself, so the row is openList too and a
# student may claim a point of their own.
MAX_OPTIONS = 16

# How many part-credit rungs a card's note shows before it says it is trimming.
# 2021 Higher Q.2 2(a) prints thirteen; a note that long is a wall of text on a
# five-mark card, and the SEC's own order puts the most valuable rungs first.
MAX_RUNGS = 6

# How the scheme names the correct box of a multiple-choice ask: by where it
# sits on the page, in either of the two languages the paper sets.
ORDINAL_ANSWER = re.compile(
    r'\((?:first|second|third|fourth|fifth)\s+answer\)'
    r'|\((?:premi[èe]re|deuxi[èe]me|troisi[èe]me|quatri[èe]me|cinqui[èe]me)'
    r'\s+r[ée]ponse\)', re.I)


def card_id(year, level, section, item, letter):
    parts = ['fr', str(year), level, section.lower(), str(item)]
    if letter:
        parts.append(letter)
    return '-'.join(parts)


def question_ref(year, level, section, item, letter, letter_to=None):
    ref = f'{year} {level.upper()} Section {section} Q{item}'
    if letter:
        ref += f'({letter})'
        if letter_to:
            ref += f'–({letter_to})'
    return ref


def source_material(P, rc, language, level, year):
    """The comprehension's own printed pages, from the QUESTION paper."""
    pages = P.rc_pages.get(rc)
    if not pages:
        return None
    return {
        'kind': 'source-text',
        'label': f'COMPRÉHENSION ÉCRITE {rc}',
        'title': f'Reading Comprehension {rc} — answer in {language}',
        'pages': pages,
        'attribution': (f'SEC French {year} {LEVEL_TITLE[level]} Level examination '
                        f'paper — © State Examinations Commission.'),
        'presentationNote': (
            'Read the passage exactly as the examination printed it, then answer. '
            + language_note(language)),
    }


def ladder_note(ask, language):
    """The part-credit rungs, verbatim, with the marks the scheme prints."""
    rungs = [r for r in ask.part if r['marks'] is not None]
    if not rungs:
        return language_note(language)
    shown = rungs[:MAX_RUNGS]
    parts = '; '.join(f'“{r["text"]}” {r["marks"]} '
                      f'{"Mark" if r["marks"] == 1 else "Marks"}' for r in shown)
    tail = (f' The scheme lists {len(rungs) - len(shown)} further part-credit '
            f'line(s) for this ask.' if len(rungs) > len(shown) else '')
    return (f'{language_note(language)} The scheme also pays part marks for a '
            f'shorter answer: {parts}.{tail}')


def build():
    cards = []
    refused = collections.Counter()
    examples = collections.defaultdict(list)
    excluded = []
    pairs = []

    def refuse(reason, ref, evidence=''):
        refused[reason] += 1
        examples[reason].append(ref)
        excluded.append({'ref': ref, 'reason': reason, 'evidence': evidence})

    for year in YEARS:
        for level in LEVELS:
            P = FrPaper(year, level, SUBJECT)
            S = FrScheme(year, level, SUBJECT)
            _reading(P, S, year, level, cards, refuse, pairs)
            _section_b(P, S, year, level, cards, refuse)
            _listening(P, year, level, refuse)
    return cards, refused, examples, excluded, pairs


# ------------------------------------------------------------ Section A ----
def _reading(P, S, year, level, cards, refuse, pairs):
    for ask in S.reading():
        section = f'A{ask.rc}'
        ref = question_ref(year, level, section, ask.item, ask.letter, ask.letter_to)
        if ask.fault:
            refuse('the two halves of the printed tariff disagree, so neither can '
                   'be trusted and the ask cannot be priced', ref,
                   f'{year} {level.upper()} scheme, {ask.notation} on the head of '
                   f'"{ask.cue[:110]}": {ask.fault}')
            continue
        # A multiple-choice ask has to show the boxes it offers. The scheme
        # names the right one by its POSITION on the page — "(Second answer)",
        # "(troisième réponse)" — which is proof that the printed options are
        # part of the question and not of the passage.
        mcq = any(ORDINAL_ANSWER.search(b['text']) for b in ask.answers)
        hit = P.find(ask.rc, ask.item, None if ask.letter_to else ask.letter,
                     ask.cue, whole=mcq)
        if hit is None:
            refuse('the paper prints no text this scheme cue can be matched to', ref,
                   f'{year} {level.upper()} scheme cue: "{ask.cue[:110]}"')
            continue
        question, page, sc = hit
        pairs.append((ref, sc))

        full = [b for b in ask.full if b['text']]
        if not full:
            refuse('the scheme states no full-mark answer for this ask', ref,
                   f'{year} {level.upper()} scheme, "{ask.cue[:110]}"')
            continue
        if ask.count is None or ask.per is None:
            refuse('the scheme prints no tariff this reads for the ask', ref,
                   f'{year} {level.upper()} scheme, "{ask.cue[:110]}"')
            continue
        if ask.count > len(full):
            refuse('the scheme prices more answers than it states', ref,
                   f'{year} {level.upper()} scheme, {ask.notation} over '
                   f'{len(full)} stated answer(s) for "{ask.cue[:80]}"')
            continue

        if ask.letter_to:
            question = _matching_question(P, ask, question)

        language = answer_language(question)
        joined = ' '.join(f'{P.lead(ask.rc)} {question}'.split())
        if cardlint.NAMES_LETTERS.search(joined):
            refuse('the ask points at printed matter the card cannot carry', ref,
                   f'{year} {level.upper()} paper: "{question[:110]}"')
            continue

        rows = _rows_for(ask, language)
        if rows is None:
            refuse('the scheme states its answers in two routes the card cannot '
                   'keep apart', ref, f'{year} {level.upper()} scheme, '
                   f'"{ask.cue[:110]}"')
            continue

        card = {
            'id': card_id(year, level, section, ask.item, ask.letter),
            'subjectId': SUBJECT,
            'level': LEVEL_WORD[level],
            'year': year,
            'section': 'A',
            'topicId': topic_for(level, ask.rc, P.lead(ask.rc)),
            'conceptId': concept_for(question),
            'questionRef': ref,
            'questionText': question,
            'tariffModel': {'kind': 'fixed'},
            'totalMarks': ask.total,
            'rows': rows,
            'notes': (f'The scheme prints the tariff as {ask.notation!r}; the paper '
                      f'prints this ask on page {page} of the question booklet. '
                      f'Paper/scheme wording agreement {sc:.2f}.'),
        }
        lead = P.lead(ask.rc)
        if lead and len(lead) >= 20:
            card['stem'] = lead
        source = source_material(P, ask.rc, language, level, year)
        if source:
            card['sourceMaterial'] = source
        cards.append(card)


def _matching_question(P, ask, stem):
    """A matching ask, printed as the paper prints it: stem then (a) to (d)."""
    parts = []
    for letter in _letters(ask.letter, ask.letter_to):
        blocks = P.candidates(ask.rc, ask.item, letter)
        # The English rendering where the paper prints both; the longest
        # otherwise. Both are the SEC's; the card is set in one of them.
        best = max((b for b in blocks), key=lambda b: (b.side == 'R', len(b.text)),
                   default=None)
        if best and best.text:
            parts.append(f'({letter}) {best.text}')
    return ' '.join(f'{stem} {" ".join(parts)}'.split())


def _letters(first, last):
    letters = 'abcdefgh'
    return list(letters[letters.index(first):letters.index(last) + 1])


def _rows_for(ask, language):
    """The card's marking rows: the full-mark answers, and the ladder as a note."""
    note = ladder_note(ask, language)
    routes = [r for r in ask.routes]
    if routes:
        # An opinion ask prints the points for agreeing and the points for
        # disagreeing separately, and a candidate takes one side. Read as one
        # list the card would offer both sides of an argument as though either
        # could be claimed beside the other, so each side is its own route and
        # each has to reach the tariff alone.
        rows = []
        for i, route in enumerate(dict.fromkeys(routes), start=1):
            options = [b['text'] for b in ask.full if b['route'] == route]
            if len(options) < ask.count:
                return None
            trimmed = len(options) - MAX_OPTIONS
            rows.append({
                'id': f'r-{i}', 'kind': 'anyN', 'route': route,
                'verbatim': f'Points for {route}ing, as the scheme lists them',
                'marks': None, 'openList': True,
                'group': {'claimMax': ask.count, 'perOption': ask.per,
                          'options': options[:MAX_OPTIONS]},
                **({'contextNote': f'The scheme lists {trimmed} further point(s) '
                                   f'for this side, and closes the list itself with '
                                   f'"Etc., etc." — a valid point of your own counts.'}
                   if trimmed > 0 else {}),
            })
        rows[0]['contextNote'] = (
            f"{note} {rows[0].get('contextNote', '')}".strip())
        return rows
    if ask.count == 1 and len(ask.full) == 1:
        return [{'id': 'r-1', 'kind': 'point', 'verbatim': ask.full[0]['text'],
                 'marks': ask.per, 'contextNote': note,
                 **({'openList': True} if ask.open_list else {})}]
    return [{
        'id': 'r-1', 'kind': 'anyN',
        'verbatim': 'The answers the scheme accepts in full',
        'marks': None, 'contextNote': note,
        **({'openList': True} if ask.open_list else {}),
        'group': {'claimMax': ask.count, 'perOption': ask.per,
                  'options': [b['text'] for b in ask.full][:MAX_OPTIONS]},
    }]


# ------------------------------------------------------------ Section B ----
GRID_EVIDENCE = (
    'the scheme answers this section with a MARKING GRID and nothing else — '
    '"Communication … TOP • Stimulus material well exploited • High level of '
    'textual coherence … BOTTOM • Mere transcription", and the same again for '
    'Language. Those are the qualities of a piece of writing, not answers, and '
    'a card would ask a student to tick "Idiomatic French" as something they '
    'were supposed to have written.')


def _section_b(P, S, year, level, cards, refuse):
    gap = S.gap_fill() if level == 'ol' else None
    for q, letter, text, page in P.section_b_asks():
        ref = question_ref(year, level, 'B', q, letter)
        if level == 'ol' and q == 1 and letter == 'a':
            if gap is None:
                refuse('the scheme leaves one of the gap-fill answers blank, so the '
                       'set of answers it prints is incomplete', ref,
                       f'{year} {level.upper()} scheme, "(a) Filling Gaps – 30 '
                       f'marks / 10 gaps for 3 marks each": the tenth answer is '
                       f'printed as "10." with no word beside it')
                continue
            cards.append(_gap_card(P, year, level, ref, text, page, gap))
            continue
        refuse('the scheme prints a band grid for this ask, not an answer', ref,
               f'{year} {level.upper()} scheme, Section B: {GRID_EVIDENCE}')


def _gap_card(P, year, level, ref, text, page, gap):
    # The word alone, in the order the gaps come. Numbering the option
    # ("6. magnifiques") reads better on the card but cannot be traced: the
    # 2025 Ordinary scheme prints that sixth answer as "maqnifiques" in its
    # answer list and "magnifiques" in the completed letter three lines below,
    # and the numbered form appears nowhere. The word does.
    options = [word for _n, word in gap['answers']]
    return {
        'id': card_id(year, level, 'B', 1, 'a'),
        'subjectId': SUBJECT,
        'level': LEVEL_WORD[level],
        'year': year,
        'section': 'B',
        'topicId': CLOZE,
        'conceptId': 'cloze-letter-gap-fill',
        'questionRef': ref,
        'questionText': text,
        'tariffModel': {'kind': 'fixed'},
        'totalMarks': gap['total'],
        'rows': [{
            'id': 'r-1', 'kind': 'anyN',
            'verbatim': 'The word the scheme places in each gap, in gap order',
            'marks': None,
            'contextNote': ('The letter is printed on the examination page below, '
                            'and the words are listed here in the order its gaps '
                            'come. The scheme deducts one mark for careless '
                            'transcription, accents included, and accepts capital '
                            'letters.'),
            'group': {'claimMax': gap['gaps'], 'perOption': gap['per'],
                      'options': options},
        }],
        'sourceMaterial': {
            'kind': 'source-text',
            'label': 'SECTION B QUESTION 1(a)',
            'title': 'The printed letter — answer in French',
            'pages': [page],
            'attribution': (f'SEC French {year} {LEVEL_TITLE[level]} Level '
                            f'examination paper — © State Examinations Commission.'),
            'presentationNote': ('Read the letter exactly as the examination '
                                 'printed it and place each word in its gap.'),
        },
        'notes': (f'The scheme prints "10 gaps for {gap["per"]} marks each" against '
                  f'a printed total of {gap["total"]}.'),
    }


# ------------------------------------------------------------- listening ----
AUDIO_EVIDENCE = (
    'the ask can only be answered from the recording. The Listening '
    'Comprehension Test is a separate SEC booklet whose own instructions read '
    '"You will hear the material three times: first right through, then in '
    'segments with pauses and finally right through again", and the paper '
    'prints no text of what is said. The only printed source of that material '
    'is the marking scheme\'s own APPENDIX 2 CD Script — the ANSWER document — '
    'so carrying it on the card would hand the student the answers with the '
    'question. No verified playback copy of the SEC recording is bound to this '
    'deck, so the card would be unanswerable from what it shows.')


def _listening(P, year, level, refuse):
    asks = P.aural_asks()
    lettered = {(sec, item) for sec, item, letter, _t in asks if letter}
    for sec, item, letter, _text in asks:
        if letter is None and (sec, item) in lettered:
            continue
        ref = question_ref(year, level, f'L{sec}', item, letter)
        refuse('the ask needs the recording, which no card can carry', ref,
               f'{year} {level.upper()} Listening Comprehension Test, '
               f'Section {sec}: {AUDIO_EVIDENCE}')


# ---------------------------------------------------------------- report ----
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--report', action='store_true')
    ap.add_argument('--exclusions', action='store_true',
                    help='rewrite exclusions/french.json from the refusals')
    ap.add_argument('--all', action='store_true')
    args = ap.parse_args()
    cards, refused, examples, excluded, pairs = build()

    if args.exclusions:
        path = os.path.join(DIR, 'exclusions', f'{SUBJECT}.json')
        with open(path, 'w', encoding='utf-8') as fh:
            json.dump(excluded, fh, ensure_ascii=False, indent=1)
            fh.write('\n')
        print(f'{len(excluded)} exclusion(s) written to {path}')
        return 0

    if args.report:
        census = census_subject(SUBJECT)
        total = sum(p['leafCount'] for p in census['papers'])
        print(f'{len(cards)} card(s) against {total} paper asks '
              f'({100 * len(cards) / total:.1f}%), {len(excluded)} refused')
        if pairs:
            worst = min(pairs, key=lambda t: t[1])
            print(f'pairing: {len(pairs)} pairs, weakest {worst[0]} at {worst[1]:.2f}')
        rows = sum(len(c['rows']) for c in cards)
        opts = sum(len(r['group']['options']) for c in cards for r in c['rows']
                   if r.get('group'))
        print(f'{rows} marking rows holding {opts} stated answer(s)')
        by_topic = collections.Counter(c['topicId'] for c in cards)
        for tid, n in sorted(by_topic.items()):
            print(f'   {tid:12} {n}')
        by_lang = collections.Counter(
            'French' if 'answered in French' in (c.get('sourceMaterial') or {}).get(
                'presentationNote', '') or 'in French' in (
                c.get('sourceMaterial') or {}).get('title', '') else 'English/Irish'
            for c in cards)
        print(f'   answer language: {dict(by_lang)}')
        for reason, n in refused.most_common():
            print(f'   {n:4} REFUSED  {reason}')
            for e in examples[reason][:40 if args.all else 3]:
                print(f'             {e}')
        return 0

    json.dump(cards, sys.stdout, ensure_ascii=False, indent=1)
    return 0


if __name__ == '__main__':
    sys.exit(main())
