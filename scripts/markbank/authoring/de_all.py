#!/usr/bin/env python3
"""Author every German ask the papers print and the schemes answer.

    python3 scripts/markbank/authoring/de_all.py --report
    python3 scripts/markbank/authoring/de_all.py --exclusions   # rewrite them
    python3 scripts/markbank/authoring/de_all.py > scripts/markbank/authored/german.json

Census-driven: the ten sittings print 540 leaf asks across two booklets each,
and this walks that census rather than choosing what to card.

WHAT ONE CARD IS
----------------
One printed ask. Its question comes from the PAPER (de_paper.py) and its
marking points from the SCHEME (de_scheme.py), paired by wording rather than by
key — Law 4 — because the paper prints every ask TWICE, in Irish and in
English, and the one the scheme marks is the one whose wording it reprints.
Twenty asks reprint no wording at all: the Ordinary paragraph-headings,
matching and true/false questions are answered by a key ("2 d 3 a 4 c 5 f 6 b")
and nothing else, so those pair on the printed ADDRESS, which is then the only
thing both documents state — and the card says so in its own notes.

THE PASSAGE TRAVELS WITH THE CARD
---------------------------------
Every reading answer is a manipulation of a passage printed only in the
question paper. A card that asks for it without carrying the passage is
unanswerable, so each one binds `sourceMaterial` to the exact pages of its own
TEXT in the QUESTION paper — never the scheme, which is where the answers are.

THE ANSWER LANGUAGE IS PART OF THE ASK, AND IT IS NOT A SUBJECT CONSTANT
------------------------------------------------------------------------
TEXT I's first question is answered in German and its second, third and fourth
in English or Irish. The paper prints the instruction between them and the
scheme prices the difference — "Answers in language not specified = half
marks" — so the language rides on each card, read from the language its own
question is printed in.

THE DESCENDING LADDER IS THE TARIFF, NOT A NOTE
-----------------------------------------------
"(Any THREE details: 7 marks: 3, 2, 2)" pays three, two and two, in that order.
That is `MarkRow.group.perOptionSteps`, which exists for exactly this, so no new
RowKind is invented and no card claims a flat 7/3 the SEC never wrote.

REFUSALS
--------
Every one is a named bucket, counted and exampled by --report, and every
refusal that lands on a census leaf becomes an exclusions entry carrying the
evidence for it (--exclusions writes them).
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

from de_paper import DePaper                                   # noqa: E402
from de_scheme import DeScheme                                 # noqa: E402
from de_topics import (topic_for, concept_for, language_note,   # noqa: E402
                       TEXT_TITLE)
from paper_census import census_subject                        # noqa: E402
import cardlint                                                # noqa: E402

SUBJECT = 'german'
YEARS = (2021, 2022, 2023, 2024, 2025)
LEVELS = ('hl', 'ol')
LEVEL_WORD = {'hl': 'higher', 'ol': 'ordinary'}
LEVEL_TITLE = {'hl': 'Higher', 'ol': 'Ordinary'}

# The most options one card may show, from MAX_LONG_OPTION_ROWS in
# types/markBank.ts. A German comprehension prints up to twenty-five accepted
# points for one four-mark ask, and a card showing them all would be a wall of
# text rather than a question. The list is trimmed in the SEC's own printed
# order and the trim is DISCLOSED on the row, which is the pattern the bank
# already uses for an over-cap menu.
MAX_OPTIONS = 16

UNIT_NAME = {'T1': 'TEXT I', 'T2': 'TEXT II', 'T3': 'TEXT III'}

# The words an English instruction is built from. Used for ONE thing: the
# Ordinary paragraph-headings, matching and true/false questions print their
# instruction and then the TABLE the student works on, in the same printed
# column, so the block carries both — and the half of the table that falls in
# that column reads as noise under the question. The instruction is in English
# and the table is in German, so the instruction ends at the first line
# carrying no English word at all. The table itself is not lost: it is on the
# examination pages the card already binds as its source material.
# 'a' is deliberately absent: the matching table's own halves are lettered
# "a." to "f." and a bare "a" let "a. in einer amerikanischen Großstadt zu"
# pass as an English instruction line.
INSTRUCTION_WORDS = {
    'the', 'an', 'of', 'to', 'and', 'or', 'for', 'is', 'are', 'your',
    'you', 'which', 'what', 'following', 'each', 'by', 'with', 'from', 'on',
    'at', 'that', 'this', 'these', 'answer', 'answers', 'box', 'boxes',
    'letters', 'letter', 'correct', 'write', 'writing', 'put', 'tick',
    'indicate', 'check', 'choose', 'explain', 'complete', 'based', 'case',
    'doubt', 'all', 'cases', 'paragraph', 'paragraphs', 'heading', 'headings',
    'briefly', 'means', 'statements', 'appropriate', 'provided', 'below',
    'corresponds', 'correspond', 'numbers', 'sentences', 'article', 'given',
    'suitable', 'numbered', 'belongs', 'together', 'english', 'whether',
    'irish', 'german', 'text', 'also', 'again', 'one', 'two', 'three',
}


# The answer rules the paper prints beside the question so a candidate can
# write on them. They are the answer space, not the ask.
ANSWER_RULE = re.compile(r'_{3,}')
# A Wingdings bullet, which reaches the text layer as a private-use codepoint.
# It is a printed BULLET, not a word: the SEC sets its worked example behind
# one and the glyph gate would refuse the card for carrying an unrepairable
# character.
PRIVATE_USE = re.compile(r'[\ue000-\uf8ff]')


def clean_question(text):
    """The printed question, without the blank answer rules or bullet glyphs."""
    return re.sub(r'[ \t]{2,}', ' ',
                  PRIVATE_USE.sub(' ', ANSWER_RULE.sub(' ', text or ''))).strip()


def instruction_only(printed):
    """The printed instruction, without the table printed beneath it."""
    kept = []
    for line in printed.split('\n'):
        words = {w.strip(".,;:!?()").lower() for w in line.split()}
        if kept and not (words & INSTRUCTION_WORDS):
            break
        kept.append(line)
    return '\n'.join(kept).strip() or printed



def card_id(year, level, unit, q, letter, roman):
    parts = ['de', str(year), level, unit.lower(), str(q)]
    if letter:
        parts.append(letter)
    if roman:
        parts.append(roman)
    return '-'.join(parts)


def question_ref(year, level, unit, q, letter, roman=None):
    ref = f'{year} {level.upper()} Section {unit} Q{q}' if q is not None \
        else f'{year} {level.upper()} Section {unit} Q'
    if letter:
        ref += f'({letter})'
    if roman:
        ref += f'({roman})'
    return ref


def reading_source(P, unit, language, level, year):
    """The TEXT's own printed pages, from the QUESTION paper."""
    pages = P.unit_pages.get(unit)
    if not pages:
        return None
    return {
        'kind': 'source-text',
        'label': TEXT_TITLE.get(unit, unit),
        'title': f'{UNIT_NAME.get(unit, unit)} — answer in {language}',
        'pages': pages,
        'attribution': (f'SEC German {year} {LEVEL_TITLE[level]} Level examination '
                        f'paper — © State Examinations Commission.'),
        'presentationNote': (
            'Read the passage exactly as the examination printed it, then answer. '
            + language_note(language)),
    }


def build():
    cards = []
    refused = collections.Counter()
    examples = collections.defaultdict(list)
    excluded = []
    pairs = []
    by_address = []

    def refuse(reason, ref, evidence=''):
        refused[reason] += 1
        examples[reason].append(ref)
        excluded.append({'ref': ref, 'reason': reason, 'evidence': evidence})

    for year in YEARS:
        for level in LEVELS:
            P = DePaper(year, level, SUBJECT)
            S = DeScheme(year, level, SUBJECT)
            _reading(P, S, year, level, cards, refuse, pairs, by_address)
            _grammar(P, S, year, level, cards, refuse)
            _written(P, year, level, refuse)
            _listening(P, year, level, refuse)
    return cards, refused, examples, excluded, pairs, by_address


# ------------------------------------------------------------- reading ----
def _reading(P, S, year, level, cards, refuse, pairs, by_address):
    credit = {unit: P.credit(unit) for unit in P.unit_pages if unit.startswith('T')}
    for ask in S.reading():
        ref = question_ref(year, level, ask.unit, ask.q, ask.letter, ask.roman)
        hit = P.find(ask.unit, ask.q, ask.letter, ask.roman, ask.cue)
        by_key = False
        if hit is None:
            hit = P.by_key(ask.unit, ask.q, ask.letter, ask.roman)
            by_key = True
            if hit is not None:
                hit = (instruction_only(hit[0]), hit[1], hit[2])
        if hit is None:
            refuse('the paper prints no block this scheme ask can be matched to',
                   ref, f'{year} {level.upper()} scheme cue: "{ask.cue[:110]}"')
            continue
        question, page, score = hit
        question = clean_question(question)
        if by_key:
            by_address.append(ref)
        else:
            pairs.append((ref, score))

        rows = _rows_for(ask)
        if isinstance(rows, str):
            refuse(rows, ref, f'{year} {level.upper()} scheme, tariff '
                              f'"{ask.notation}" over {len(ask.answers)} stated '
                              f'answer(s) for "{ask.cue[:80]}"')
            continue
        if cardlint.NAMES_LETTERS.search(question):
            refuse('the ask points at printed matter the card cannot carry', ref,
                   f'{year} {level.upper()} paper: "{question[:110]}"')
            continue

        rows[0]['contextNote'] = ' '.join(
            [language_note(ask.language)]
            + ([rows[0]['contextNote']] if rows[0].get('contextNote') else [])
            + [n for n in ask.notes]).strip()
        source = reading_source(P, ask.unit, ask.language, level, year)
        note = (f'The scheme reaches this ask by splitting {UNIT_NAME.get(ask.unit, ask.unit)}'
                f' down to it and prices it {ask.total}, as {ask.notation!r}; '
                f'the paper prints it on page {page} of the question booklet.')
        note += (' The scheme reprints no wording for this ask — it prints only '
                 'the answer key — so paper and scheme are paired on the printed '
                 'address they both state, and the table the question works on '
                 'is on the examination pages carried with this card.' if by_key
                 else f' Paper/scheme wording agreement {score:.2f}.')
        card = {
            'id': card_id(year, level, ask.unit, ask.q, ask.letter, ask.roman),
            'subjectId': SUBJECT,
            'level': LEVEL_WORD[level],
            'year': year,
            'section': ask.unit,
            'topicId': topic_for(ask.unit, credit.get(ask.unit)),
            'conceptId': concept_for(ask.cue or question),
            'questionRef': ref,
            'questionText': question,
            'tariffModel': {'kind': 'fixed'},
            'totalMarks': ask.total,
            'rows': rows,
            'notes': note,
        }
        if source:
            card['sourceMaterial'] = source
        cards.append(card)


def _rows_for(ask):
    """The card's marking rows — one per printed segment of the ask.

    A segment is a named half of one ask ("How:" over a two-mark list, "What:"
    over another); most asks have one. They are ROWS, not `route`s: a route
    locks the others when claimed, and these are both answered.
    """
    rows = []
    for i, seg in enumerate(ask.segments, start=1):
        steps = seg['steps']
        answers = seg['answers']
        options = [a['text'] for a in answers]
        if len(options) < len(steps):
            return 'the scheme prices more answers than it states'
        if not options:
            return 'the scheme states no answer for this ask'
        # An ordered ANSWER KEY, not a menu: the Ordinary true/false and
        # multiple-choice questions answer five printed statements with five
        # one-word answers, and several of the five are the same word. Offered
        # as a pick-list the card would show "True / False / False / False /
        # True" with nothing to attach each to. Where the scheme numbers the
        # key it is numbered here; where it does not — the true/false list is
        # printed as five bare words — each answer becomes its own row, in the
        # order the examination prints the statements it answers.
        if ask.exhaustive and len(options) == len(steps) and (
                len(set(options)) != len(options)
                or all(len(o) <= 4 for o in options)):
            if all(a.get('n') for a in answers):
                options = [f"{a['n']} — {a['text']}" for a in answers]
            else:
                for j, (a, marks) in enumerate(zip(answers, steps), start=1):
                    rows.append({
                        'id': f'r-{i}-{j}', 'kind': 'point',
                        'verbatim': a['text'], 'marks': marks,
                        'contextNote': (f'The answer to statement {j}, in the '
                                        f'order the examination prints them.'),
                    })
                continue
        label = seg['label']
        if len(steps) == 1 and len(options) == 1:
            rows.append({'id': f'r-{i}', 'kind': 'point',
                         'verbatim': options[0], 'marks': steps[0],
                         **({'contextNote': f'The scheme heads this answer “{label}”.'}
                            if label else {})})
            continue
        trimmed = len(options) - MAX_OPTIONS
        group = {'claimMax': len(steps), 'perOption': steps[0],
                 'options': options[:MAX_OPTIONS]}
        if len(set(steps)) > 1:
            # A descending ladder: "(Any THREE details: 7 marks: 3, 2, 2)".
            group['perOptionSteps'] = steps
        notes = []
        if label:
            notes.append(f'The scheme heads this list “{label}”.')
        elif seg.get('labels'):
            heads = '”, “'.join(dict.fromkeys(seg['labels']))
            notes.append(f'The scheme prints these under the headings “{heads}”, '
                         f'in the order shown; the paper says an answer may draw '
                         f'on any of them.')
        if len(steps) == len(options) and trimmed <= 0 and ask.exhaustive:
            notes.append('The scheme pays every one of these; none is optional.')
        if trimmed > 0:
            notes.append(f'The scheme lists {trimmed} further accepted answer(s) '
                         f'for this ask, in the order it prints them; a valid '
                         f'answer of your own counts.')
        rows.append({
            'id': f'r-{i}', 'kind': 'anyN',
            'verbatim': (f'{label}: the answers the scheme accepts' if label
                         else 'The answers the scheme accepts in full'),
            'marks': None, 'group': group,
            **({'openList': True} if trimmed > 0 else {}),
            **({'contextNote': ' '.join(notes)} if notes else {}),
        })
    return rows


# ------------------------------------------------------ applied grammar ----
def _grammar(P, S, year, level, cards, refuse):
    asks = {a.q: a for a in S.grammar()}
    for q, text, page in P.grammar_alternatives():
        ref = question_ref(year, level, 'AG', q, None)
        ask = asks.get(q)
        if ask is None:
            refuse('the scheme prices no answers for this printed alternative',
                   ref, f'{year} {level.upper()} scheme, ANGEWANDTE GRAMMATIK '
                        f'alternative {q}')
            continue
        rows = _rows_for(ask)
        if isinstance(rows, str):
            refuse(rows, ref, f'{year} {level.upper()} scheme, '
                              f'ANGEWANDTE GRAMMATIK {q}: "{ask.notation}"')
            continue
        rows[0]['contextNote'] = (
            'Every gap is answered; the scheme prints the mark it pays on each. '
            + language_note('German'))
        source = {
            'kind': 'source-text',
            'label': TEXT_TITLE['AG'],
            'title': 'Angewandte Grammatik — the printed exercise',
            'pages': [page],
            'attribution': (f'SEC German {year} {LEVEL_TITLE[level]} Level '
                            f'examination paper — © State Examinations Commission.'),
            'presentationNote': ('Work from the sentences exactly as the '
                                 'examination printed them. ' + language_note('German')),
        }
        extra = P.unit_pages.get('T1')
        card = {
            'id': card_id(year, level, 'AG', q, None, None),
            'subjectId': SUBJECT,
            'level': LEVEL_WORD[level],
            'year': year,
            'section': 'AG',
            'topicId': topic_for('AG', None),
            'conceptId': concept_for(text or ask.cue, 'applied-grammar'),
            'questionRef': ref,
            'questionText': clean_question(text) or ask.cue,
            'tariffModel': {'kind': 'fixed'},
            'totalMarks': ask.total,
            'rows': rows,
            'sourceMaterial': source,
            'notes': (f'The paper sets question 1 OR question 2 here and this is '
                      f'alternative {q}; the scheme prices it {ask.total}, as '
                      f'{ask.notation!r}.'),
        }
        if extra:
            card['additionalSourceMaterials'] = [{
                'kind': 'source-text',
                'label': TEXT_TITLE['T1'],
                'title': 'TEXT I — the passage this exercise is drawn from',
                'pages': extra,
                'attribution': (f'SEC German {year} {LEVEL_TITLE[level]} Level '
                                f'examination paper — © State Examinations Commission.'),
                'presentationNote': ('The exercise cites this passage by section, '
                                     'so it is carried beside it.'),
            }]
        cards.append(card)


# --------------------------------------------------- written production ----
GRID_EVIDENCE = (
    'the scheme answers this task with a CONTENT AND EXPRESSION GRID and '
    'nothing else — "Content = 13 (A = 3; B = 4; C = 4; Dis. 2)", "Expression = '
    '12", then "A: (3 marks) … Satz 1: 1 mark / Satz 2: 1 mark / Satz 3: 1 '
    'mark" and a four-band scale reading "Vocabulary very inadequate, possibly '
    'with English words and interference from English syntax" up to "Vocabulary '
    'use good – rich, idiomatic and appropriate". Those price the sentences the '
    'candidate writes; they state no answer, and a card would ask a student to '
    'tick "Idiomatic German" as something they were supposed to have written.')


def _written(P, year, level, refuse):
    for unit in ('AT', 'SP'):
        for letter, _text, _page in P.written_alternatives(unit):
            ref = question_ref(year, level, unit, None, letter)
            name = ('Äußerung zum Thema' if unit == 'AT'
                    else 'Schriftliche Produktion')
            refuse('the scheme prints a content-and-expression grid for this '
                   'task, not an answer', ref,
                   f'{year} {level.upper()} scheme, {name}: {GRID_EVIDENCE}')


# ------------------------------------------------------------- listening ----
AUDIO_EVIDENCE = (
    'the ask can only be answered from the recording. The Listening '
    'Comprehension Test is a separate SEC booklet whose own instructions read '
    '"The interview will be played three times: first right through, then in '
    'segments with pauses, and finally right through again", and the booklet '
    'prints no text of what is said. The only printed source of that material '
    'is the marking scheme\'s own transcript, headed "Teil 1" — the ANSWER '
    'document — so carrying it on the card would hand the student the answers '
    'with the question. No verified playback copy of the SEC recording is bound '
    'to this deck, so the card would be unanswerable from what it shows.')


def _listening(P, year, level, refuse):
    for part, item, roman, _text in P.aural_asks():
        ref = question_ref(year, level, f'L{part}', item, None, roman)
        refuse('the ask needs the recording, which no card can carry', ref,
               f'{year} {level.upper()} Listening Comprehension Test, part '
               f'{part}: {AUDIO_EVIDENCE}')


# ---------------------------------------------------------------- report ----
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--report', action='store_true')
    ap.add_argument('--exclusions', action='store_true',
                    help='rewrite exclusions/german.json from the refusals')
    ap.add_argument('--all', action='store_true')
    args = ap.parse_args()
    cards, refused, examples, excluded, pairs, by_address = build()

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
            print(f'pairing: {len(pairs)} by wording, weakest {worst[0]} at '
                  f'{worst[1]:.2f}; {len(by_address)} by printed address')
        rows = sum(len(c['rows']) for c in cards)
        opts = sum(len(r['group']['options']) for c in cards for r in c['rows']
                   if r.get('group'))
        print(f'{rows} marking rows holding {opts} stated answer(s)')
        by_topic = collections.Counter(c['topicId'] for c in cards)
        for tid, n in sorted(by_topic.items()):
            print(f'   {tid:12} {n}')
        by_lang = collections.Counter(
            'German' if 'in German' in (c.get('sourceMaterial') or {}).get('title', '')
            else 'English or Irish' for c in cards)
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
