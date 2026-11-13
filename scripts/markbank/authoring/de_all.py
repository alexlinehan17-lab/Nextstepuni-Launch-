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
from de_scheme import (DeScheme, scheme_grid, GRID_ASK, _language_of,  # noqa: E402
                       scheme_field_table, FIELD_ASK, read_rate)
from paper_census import census_de                             # noqa: E402
from de_topics import (topic_for, concept_for, language_note,   # noqa: E402
                       TEXT_TITLE)
from paper_census import census_subject                        # noqa: E402
import de_listen                                               # noqa: E402
import de_writing                                              # noqa: E402
import cardlint                                                # noqa: E402

SUBJECT = 'german'
YEARS = (2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026)
LEVELS = ('hl', 'ol')
# The sittings whose reading and grammar asks are carded, and those whose
# listening asks are (de_listen.py, answered from the SEC recording). A sitting
# opts in once its cards have been read against its scheme, one commit each.
READING_CARDED = {(y, l) for y in (2021, 2022, 2023, 2024, 2025) for l in ('hl', 'ol')} | {
    (2026, 'hl'), (2026, 'ol'), (2020, 'hl'), (2020, 'ol'), (2019, 'hl'), (2019, 'ol'), (2018, 'hl'), (2018, 'ol'), (2017, 'hl'), (2017, 'ol'), (2016, 'hl'), (2016, 'ol'), (2015, 'hl'), (2015, 'ol'), (2014, 'hl')}
LISTENING_CARDED = {(2014, 'hl'), (2015, 'ol'), (2015, 'hl'), (2016, 'ol'), (2016, 'hl'), (2017, 'ol'), (2017, 'hl'), (2018, 'ol'), (2018, 'hl'), (2019, 'ol'), (2019, 'hl'), (2020, 'ol'), (2020, 'hl'), (2026, 'hl'), (2026, 'ol'), (2025, 'hl'), (2025, 'ol'), (2024, 'hl'), (2024, 'ol'), (2023, 'hl'), (2023, 'ol'), (2022, 'hl'), (2022, 'ol'), (2021, 'hl'), (2021, 'ol')}
# The sittings whose written production (Äußerung zum Thema, Schriftliche
# Produktion) is carded on the scheme's grid (de_writing.py), with the printed
# lower expression scale and, at Ordinary, the fill-in phrases as their own card.
WRITING_CARDED = {(2014, 'hl'), (2015, 'ol'), (2015, 'hl'), (2016, 'ol'), (2016, 'hl'), (2017, 'ol'), (2017, 'hl'), (2018, 'ol'), (2018, 'hl'), (2019, 'ol'), (2019, 'hl'), (2020, 'ol'), (2020, 'hl'), (2026, 'ol'), (2026, 'hl'), (2025, 'ol'), (2025, 'hl'), (2024, 'ol'), (2024, 'hl'), (2023, 'ol'), (2023, 'hl'), (2022, 'ol'), (2022, 'hl'), (2021, 'ol'), (2021, 'hl')}
# The SEC's deferred sittings carded (2022 Higher, the only one the archive
# holds: paper_census.DE_DEFERRED_PAPERS): ids "de-2022-hl-deferred-…",
# cited "… — Deferred sitting", on the deferred booklets, scheme and recording.
DEFERRED_CARDED = {(2022, 'hl')}
# The sittings whose uncarded listening and writing asks are refused with
# evidence (exclusions/german.json): the five the bank was first built on.
# Every other sitting's uncarded asks stay OPEN in the census until carded.
REFUSED_SITTINGS = {(y, l) for y in (2021, 2022, 2023, 2024, 2025) for l in ('hl', 'ol')}
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
    # The Higher matching task's German instruction (2016): "Welche
    # Satzhälften passen zusammen? Tragen Sie die passenden Buchstaben …"
    'welche', 'satzhälften', 'passen', 'zusammen', 'tragen', 'buchstaben',
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
    """The printed question, without the blank answer rules or bullet glyphs,
    nor the head of the tick table under it ("Fíor / True Bréagach / False",
    2014 Ordinary)."""
    text = re.sub(r'\s*Fíor\s*/\s*True\s+Bréagach\s*/\s*False\s*$', '', text or '')
    return re.sub(r'[ \t]{2,}', ' ',
                  PRIVATE_USE.sub(' ', ANSWER_RULE.sub(' ', text))).strip()


def _fragment_of(part, whole):
    """True where `part` is a line cut out of the longer printed `whole`."""
    a, b = ' '.join(part.split()), ' '.join(whole.split())
    # (Or one cut at its start: "level education. What did Antonia Mandel
    # decide to do …?" out of "According to Text III, young people have to
    # make big decisions when they start third level education. …", 2016
    # Ordinary — the scheme reprints only the second sentence.)
    # (Or the title alone of a longer instruction: "Was passt zusammen?" over
    # "Unten sehen Sie zwei Reihen von Satzhälften …", 2014 Higher.)
    return len(a) < len(b) and a in b and (not re.search(r'[.?!)]$', a)
                                           or bool(re.match(r'^[a-zäöüß]', a))
                                           or (b.startswith(a) and len(a.split()) <= 4
                                               and len(b) > len(a) + 40))


def instruction_only(printed):
    """The printed instruction, without the table printed beneath it."""
    kept = []
    for line in printed.split('\n'):
        words = {w.strip(".,;:!?()").lower() for w in line.split()}
        # A German instruction wrapped mid-sentence carries none of the
        # English instruction words, but its sentence is not finished: "…
        # Sätze bilden, die auf dem Inhalt von Text II" / "basieren. …"
        # (2017 Higher).
        # Nor does the one German noun that ends an English one: "Give a
        # detailed description of Johannes’s" / "Liveprüfung." (2015 Higher).
        unfinished = kept and not re.search(r'[.?!:)]\s*$', kept[-1]) and (
            re.match(r'^[a-zäöüß]', line) or re.fullmatch(r'[A-ZÄÖÜ][\wäöüß’-]+\.\s*', line))
        if kept and not (words & INSTRUCTION_WORDS) and not unfinished:
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
            if (year, level) in READING_CARDED:
                _reading(P, S, year, level, cards, refuse, pairs, by_address)
                if S.refused_leaves:
                    _grids(P, S, year, level, cards, set(census_de(SUBJECT, year, level)[0]))
                _grammar(P, S, year, level, cards, refuse)
            if (year, level) in WRITING_CARDED:
                cards.extend(de_writing.cards(year, level, card_id, question_ref, concept_for))
            elif (year, level) in REFUSED_SITTINGS:
                _written(P, year, level, refuse)
            if (year, level) in LISTENING_CARDED:
                cards.extend(de_listen.cards(year, level, refuse, card_id, question_ref,
                                             concept_for))
            elif (year, level) in REFUSED_SITTINGS:
                _listening(P, year, level, refuse)
    for year, level in sorted(DEFERRED_CARDED, reverse=True):
        import de_written
        from paper_census import census_german_deferred
        paper = next(p for p in census_german_deferred() if (p['year'], p['level']) == (year, level))
        keys = [tuple(x['key']) for x in paper['leaves']]
        cards.extend(de_written.cards(year, level, 'deferred', card_id, question_ref, concept_for,
                                      refuse, keys))
        cards.extend(de_written.grammar_cards(year, level, 'deferred', card_id, question_ref,
                                              concept_for, refuse))
        cards.extend(de_writing.cards(year, level, card_id, question_ref, concept_for, 'deferred'))
        cards.extend(de_listen.cards(year, level, refuse, card_id, question_ref, concept_for,
                                     'deferred'))
    return cards, refused, examples, excluded, pairs, by_address


# ------------------------------------------------------------- reading ----
def _reading(P, S, year, level, cards, refuse, pairs, by_address):
    credit = {unit: P.credit(unit) for unit in P.unit_pages if unit.startswith('T')}
    for ask in S.reading():
        field_note = None
        ref = question_ref(year, level, ask.unit, ask.q, ask.letter, ask.roman)
        hit = P.find(ask.unit, ask.q, ask.letter, ask.roman, ask.cue)
        by_key = False
        whole = P.by_key(ask.unit, ask.q, ask.letter, ask.roman) if hit is not None else None
        if whole is not None and _fragment_of(hit[0], whole[0]):
            # The scheme reprints one sentence of a longer printed instruction
            # ("Welche Satzhälften passen zusammen?") and the match is the
            # paper line holding it, cut mid-sentence ("von Text II basieren.
            # Welche Satzhälften passen zusammen? Tragen Sie die passenden"):
            # the ask is the whole block the paper prints at its address.
            hit = (' '.join(whole[0].split()), whole[1], hit[2])
        if hit is None:
            hit = P.by_key(ask.unit, ask.q, ask.letter, ask.roman)
            by_key = True
            if hit is not None:
                hit = (instruction_only(hit[0]), hit[1], hit[2])
            # The scheme splits a question the paper prints whole, its parts
            # the answer fields under it: "Who is giving away a barbecue party
            # and for whom? (Introduction)" over "Who?" and "For whom?" (2013
            # Ordinary), priced "(a) 2 marks; (b) 1 mark". The paper's own
            # "(a)" at this address is a page later, inside another question
            # ("für alle." under question 4's "Das Gewinnspiel ist ___"): the
            # question printed at the number is the ask.
            whole_q = P.by_key(ask.unit, ask.q, None, ask.roman) if ask.letter else None
            if (hit is not None and whole_q is not None and whole_q[1] < hit[1]
                    and not any(b.side == 'R' for b in P.candidates(ask.unit, ask.q, ask.letter, ask.roman))):
                hit = (instruction_only(whole_q[0]), whole_q[1], whole_q[2])
                # The answer field this part is: "Cé? / Who?____" is (a).
                fields = [f for b in P.candidates(ask.unit, ask.q, None, ask.roman) if b.side == 'L'
                          for f in re.findall(r'/\s*([A-Z][\w ]{0,20}\?)\s*_', ' '.join(b.lines))]
                at = 'abcdefgh'.index(ask.letter)
                if at < len(fields):
                    field_note = f'This part is the answer the paper asks for under “{fields[at]}”.'
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
        grid = (scheme_grid(year, level, [n for g in ask.segments for n in g['steps']])
                if GRID_ASK.search(ask.cue or '') else None)
        if grid:
            # The table's own column heads, read into the ask as its last
            # words, are not the question.
            cut = GRID_ASK.search(question)
            if cut:
                question = question[:cut.end()] + '.'
            # An answer grid (2018 Ordinary TEXT II Q1): a column per person,
            # a row per field, each cell priced. One row per column, its cells
            # the parts, "field — answer" as the scheme sets them.
            rows = [{'id': f'r-{n}', 'kind': 'criterion', 'verbatim': name,
                     'marks': sum(m for _l, _a, m in cells),
                     'permittedMarks': list(range(sum(m for _l, _a, m in cells) + 1)),
                     'parts': [{'id': f'p{k}', 'verbatim': f'{label} — {answer}', 'marks': m,
                                'permittedMarks': list(range(m + 1))}
                               for k, (label, answer, m) in enumerate(cells, start=1)],
                     **({'contextNote': 'The scheme answers this in a table, a column for each '
                                        'person and a row for each field; each column is one '
                                        'row here, each of its cells a part at its printed mark.'}
                        if n == 1 else {})}
                    for n, (name, cells) in enumerate(grid, start=1)]
        table = (scheme_field_table(year, level, ask.cue, ask.total)
                 if isinstance(rows, str) and FIELD_ASK.search(ask.cue or '') else None)
        if table:
            # A field table (2013 Ordinary TEXT II Q1): one row per field, a
            # priced answer as "field — answer", a rated list as a menu.
            rows = _field_rows(table)
        if isinstance(rows, str):
            refuse(rows, ref, f'{year} {level.upper()} scheme, tariff '
                              f'"{ask.notation}" over {len(ask.answers)} stated '
                              f'answer(s) for "{ask.cue[:80]}"')
            continue
        if cardlint.NAMES_LETTERS.search(question):
            refuse('the ask points at printed matter the card cannot carry', ref,
                   f'{year} {level.upper()} paper: "{question[:110]}"')
            continue

        # A note naming points the first list does not have — "(Allow: “Give
        # tents to people in need” if points 5-8 not given)" under the eight
        # "Solutions" of 2023 Higher, whose "Why" list has five — belongs to
        # the list that has them.
        placed = []
        for i, seg in enumerate(ask.segments, start=1):
            if i == 1 or not seg.get('answers'):
                continue
            home = next((r for r in rows if r['id'] == f'r-{i}' or r['id'].startswith(f'r-{i}-')), None)
            for n in seg.get('notes_here', []):
                if home is not None and n in ask.notes and n not in placed:
                    home['contextNote'] = ' '.join(x for x in (home.get('contextNote'), n) if x)
                    placed.append(n)
        for n in ask.notes:
            if n in placed:
                continue
            pts = re.search(r'\bpoints?\s+\d{1,2}\s*[-–]\s*(\d{1,2})\b', n)
            size = lambda r: len((r.get('group') or {}).get('options', []))  # noqa: E731
            home = next((r for r in rows[1:] if pts and size(rows[0]) < int(pts.group(1)) <= size(r)), None)
            if home is not None:
                home['contextNote'] = ' '.join(x for x in (home.get('contextNote'), n) if x)
                placed.append(n)
        rows[0]['contextNote'] = ' '.join(
            [language_note(ask.language)]
            + ([rows[0]['contextNote']] if rows[0].get('contextNote') else [])
            + [n for n in ask.notes if n not in placed]).strip()
        if field_note:
            rows[0]['contextNote'] = f"{rows[0]['contextNote']} {field_note}"
        # A priced alternative the scheme prints beside an answer is a claim of
        # its own, paid in place of that answer (optionOf), as in listening.
        rows = de_listen._partials(rows)
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
        label = seg['label']
        if len(options) == 1 < len(steps):
            # One answer pricing its own components under a split naming
            # them: "(i) 2 marks: 1, 1" over "To travel to Africa (1) when
            # he is 18. (1)" (2019 Ordinary) — each claimed at its price.
            parts = de_listen._components(options[0])
            alt = _component_alternative(ask, parts)
            if alt:
                # … and the scheme's own cheaper form of one component under
                # it: "He is not invited (3) to Tatjana's (1) birthday (1)
                # party (1)" / "N.B.: He is not going (1) to Tatjana's (1) …"
                # (2016 Ordinary). Each component a claim at its price, the
                # alternative a partial of the one it replaces (optionOf), as
                # 2025 Ordinary's "in summer".
                note, k, (alt_w, alt_m) = alt
                ask.notes.remove(note)
                marks = [m for _w, m in parts] + [alt_m]
                rows.append({'id': f'r-{i}', 'kind': 'anyN',
                             'verbatim': 'The answers the scheme accepts in full', 'marks': None,
                             'group': {'claimMax': len(parts), 'perOption': max(marks),
                                       'options': [w for w, _m in parts] + [alt_w],
                                       'optionMarks': marks,
                                       'optionOf': [None] * len(parts) + [k]},
                             'contextNote': (f'The scheme prints this answer as “{options[0]}” and, '
                                             f'under it, “{note}”: “{alt_w}” is paid in place of '
                                             f'“{parts[k][0]}”, never beside it.')})
                continue
            if parts and ([m for _w, m in parts] == steps or (
                    len(steps) > 1 and sum(m for _w, m in parts) == sum(steps))):
                rows.append({'id': f'r-{i}', 'kind': 'criterion',
                             'verbatim': options[0], 'marks': sum(steps),
                             **({'contextNote': f'The scheme heads this answer “{label}”.'}
                                if label else {}),
                             'permittedMarks': list(range(sum(steps) + 1)),
                             'parts': [{'id': f'p{k}', 'verbatim': w, 'marks': m,
                                        'permittedMarks': list(range(m + 1))}
                                       for k, (w, m) in enumerate(parts, start=1)]})
                continue
        whole = len(steps) == 1 and len(options) > 1
        if 1 < len(options) < len(steps) or whole:
            # Several answers, each pricing itself, whose prices in order are
            # the split: "(b) 6 marks: 1, 1, 1, 1, 2" over "He is going to
            # Croatia (1) for his LC trip/ Abi-tour (1) and … (1) with his
            # family (1)" and "Work experience/an internship / become a
            # journalist. (2)" (2017 Ordinary). Every answer is required.
            own = []
            for a in answers:
                parts = de_listen._components(a['text'])
                own.append(('parts', a['text'], parts) if parts else
                           ('point', a['text'], [(a['text'], a['marks'])]) if a.get('marks') else None)
            prices = [m for _k, _t, ps in own for _w, m in ps] if all(own) else None
            # (Or the head prints the whole only, "(6 marks)", over "Nicolas:
            # Food (1) and drink (1)", "Merle: …", "Björn: …", 2017 Ordinary:
            # every answer required where their own prices make the whole and
            # each is less than it.)
            if prices and (prices == steps or (whole and sum(prices) == steps[0]
                                               and all(sum(m for _w, m in ps) < steps[0]
                                                       for _k, _t, ps in own))):
                heads = seg.get('labels') or []
                for k, (kind, text, ps) in enumerate(own, start=1):
                    note = (f'The scheme heads this answer “{heads[k - 1]}”.'
                            if len(heads) == len(own) and heads[k - 1] else None)
                    row = {'id': f'r-{i}-{k}', 'kind': 'criterion' if kind == 'parts' else 'point',
                           'verbatim': text, 'marks': sum(m for _w, m in ps),
                           **({'contextNote': note} if note else {})}
                    if kind == 'parts':
                        row['permittedMarks'] = list(range(row['marks'] + 1))
                        row['parts'] = [{'id': f'p{j}', 'verbatim': w, 'marks': m,
                                         'permittedMarks': list(range(m + 1))}
                                        for j, (w, m) in enumerate(ps, start=1)]
                    rows.append(row)
                continue
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
            parts = de_listen._components(options[0])
            if parts and sum(m for _w, m in parts) == steps[0]:
                # One answer the scheme prices in its own components — "Three
                # years (1) ago (1)" — each claimed at its printed mark.
                rows.append({'id': f'r-{i}', 'kind': 'criterion',
                             'verbatim': options[0], 'marks': steps[0],
                             **({'contextNote': f'The scheme heads this answer “{label}”.'}
                                if label else {}),
                             'permittedMarks': list(range(steps[0] + 1)),
                             'parts': [{'id': f'p{k}', 'verbatim': w, 'marks': m,
                                        'permittedMarks': list(range(m + 1))}
                                       for k, (w, m) in enumerate(parts, start=1)]})
                continue
            # The answer's restated price with the scheme's asides after it:
            # "… beside hers. (2) (She found out where he lives only=1 mark)
            # (He lives next door=0)" (2019 Higher). The asides are notes —
            # and a priced one the alternative claimed in its place.
            tail = re.fullmatch(r'(.+?)\s*\(\s*(\d{1,2})\s*(?:marks?)?\s*\)\s*((?:\([^()]*\)\s*)+)',
                                options[0])
            asides = None
            if tail and int(tail.group(2)) == steps[0]:
                options[0] = tail.group(1).strip()
                asides = ' '.join(tail.group(3).split())
            note = ' '.join(x for x in (f'The scheme heads this answer “{label}”.' if label else '',
                                        asides or '') if x)
            rows.append({'id': f'r-{i}', 'kind': 'point',
                         'verbatim': options[0], 'marks': steps[0],
                         **({'contextNote': note} if note else {})})
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
        elif seg.get('labels') and any(seg['labels']):
            heads = '”, “'.join(dict.fromkeys(x for x in seg['labels'] if x))
            if all(re.match(r'^\([a-h]\) ', x) for x in seg['labels'] if x):
                # Lettered categories (2015 Ordinary TEXT III Q3): what the
                # answer may draw from them is the scheme's own N.B., quoted.
                notes.append(f'The scheme prints these under the headings “{heads}”, '
                             f'in the order shown.')
            else:
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


def _component_alternative(ask, parts):
    """(note, index, (words, marks)) where a note under a components answer
    prints the same answer with ONE component cheaper, else None."""
    if not parts:
        return None
    for note in ask.notes:
        m = re.match(r'^N\.?\s?B\.?:?\s*(.+)$', note)
        alt = de_listen._components(m.group(1)) if m else None
        if not alt or len(alt) != len(parts):
            continue
        differ = [k for k, (a, b) in enumerate(zip(alt, parts)) if a[0] != b[0]]
        if (len(differ) == 1 and alt[differ[0]][1] < parts[differ[0]][1]
                and all(a[1] == b[1] for k, (a, b) in enumerate(zip(alt, parts)) if k not in differ)):
            return note, differ[0], alt[differ[0]]
    return None


def _field_rows(table):
    """The rows of a field-table card: a field whose answer prices itself
    ("Train (1)") is "field — answer" at that price; a field answered by a
    rate over a numbered list is that list as a menu, the field its heading."""
    rows = []
    for field, answer in table:
        name = re.sub(r'\s*\(\s*\d{1,2}\s*marks?\s*\)\s*$', '', field).rstrip(' :')
        steps, _cnt = read_rate(answer[0]) if answer else (None, None)
        if steps is None and answer and re.search(r':\s*\d{1,2}\s*marks?\s*:', answer[0]):
            steps, _cnt = read_rate(answer[0].split(':', 1)[1].strip())
        if steps is not None:
            options, cur = [], None
            for line in answer[1:]:
                m = re.match(r'^\d{1,2}\.\s*(.+)$', line)
                if m:
                    options.append(m.group(1).strip())
                elif options:
                    options[-1] = f'{options[-1]} {line}'
            rows.append({'id': f'r-{len(rows) + 1}', 'kind': 'anyN',
                         'verbatim': f'{name}: the answers the scheme accepts', 'marks': None,
                         'group': {'claimMax': len(steps), 'perOption': max(steps), 'options': options,
                                   **({'perOptionSteps': steps} if len(set(steps)) > 1 else {})},
                         'contextNote': f'The scheme heads this list “{name}” and prices it “{answer[0]}”.'})
            continue
        text = ' '.join(answer)
        m = re.match(r'^(.*?)\s*\(\s*(\d{1,2})\s*\)\s*$', text)
        if not m:
            return 'the scheme answers this in a table this cannot read'
        rows.append({'id': f'r-{len(rows) + 1}', 'kind': 'point',
                     'verbatim': f'{name} — {m.group(1)}', 'marks': int(m.group(2))})
    rows[0]['contextNote'] = ('The scheme answers this in a table, a row for each field; each '
                              'field is one row here, at its printed mark.'
                              + (f" {rows[0]['contextNote']}" if rows[0].get('contextNote') else ''))
    return rows


def _grid_rows(grid):
    """The rows of an answer-grid card: per column, its fixed cells as one
    criterion ("field — answer" parts at their marks), and each cell that
    prints a choice of its own as a menu at its own rate."""
    rows = []
    for name, cells in grid:
        fixed = [c for c in cells if c[1] is not None]
        if fixed:
            marks = sum(m for _l, _a, m in fixed)
            rows.append({'id': f'r-{len(rows) + 1}', 'kind': 'criterion', 'verbatim': name,
                         'marks': marks, 'permittedMarks': list(range(marks + 1)),
                         'parts': [{'id': f'p{k}', 'verbatim': f'{label} — {answer}', 'marks': m,
                                    'permittedMarks': list(range(m + 1))}
                                   for k, (label, answer, m) in enumerate(fixed, start=1)]})
        for label, _none, (rate, steps, answers) in (c for c in cells if c[1] is None):
            group = {'claimMax': len(steps), 'perOption': steps[0], 'options': answers}
            if len(set(steps)) > 1:
                group['perOptionSteps'] = steps
            rows.append({'id': f'r-{len(rows) + 1}', 'kind': 'anyN',
                         'verbatim': f'{name} — {label} the answers the scheme accepts',
                         'marks': None, 'group': group,
                         'contextNote': f'The scheme prints, in {name}’s column: “{rate}”.'})
    rows[0]['contextNote'] = ' '.join(x for x in (
        'The scheme answers this in a table, a column for each person and a row for each field; '
        'each column is a row here, each of its cells a part at its printed mark, and a cell '
        'that prints a choice of its own is a list.', rows[0].get('contextNote')) if x)
    return rows


def _grids(P, S, year, level, cards, keys):
    """Cards for the reading asks the scheme answers with a GRID the reader
    refused (2016 Ordinary TEXT II Q1, 2015 Ordinary TEXT II Q3): found by
    the grid's own column-head line in the refused block, believed only where
    every column adds to the share it prints and the columns to the ask."""
    have = {c['id'] for c in cards}
    credit = {unit: P.credit(unit) for unit in P.unit_pages if unit.startswith('T')}
    for key, (total, _clause, block) in sorted(S.refused_leaves.items(), key=str):
        unit, q, letter, roman = key
        if not unit.startswith('T') or key not in keys or card_id(year, level, *key) in have:
            continue
        grid = None
        for line in [b.strip() for b in block if b.strip()][:6]:
            grid = scheme_grid(year, level, None, header=line)
            if grid:
                break
        if not grid or sum((m if a is not None else sum(m[1])) for _n, cells in grid
                           for _l, a, m in cells) != total:
            continue
        hit = P.by_key(unit, q, letter, roman)
        if hit is None:
            continue
        text, page, _s = hit
        flat = ' '.join(text.split())
        cut = GRID_ASK.search(flat)
        end = flat.find('.', cut.end()) + 1 if cut else 0
        question = clean_question(flat[:end or cut.end()] if cut else instruction_only(text))
        rows = _grid_rows(grid)
        language = _language_of(question, None)
        rows[0]['contextNote'] = f"{language_note(language)} {rows[0]['contextNote']}"
        card = {
            'id': card_id(year, level, unit, q, letter, roman),
            'subjectId': SUBJECT, 'level': LEVEL_WORD[level], 'year': year, 'section': unit,
            'topicId': topic_for(unit, credit.get(unit)),
            'conceptId': concept_for(question),
            'questionRef': question_ref(year, level, unit, q, letter, roman),
            'questionText': question,
            'tariffModel': {'kind': 'fixed'},
            'totalMarks': total,
            'rows': rows,
            'notes': (f'The scheme answers this ask with a table, read by its columns; it prices '
                      f'the ask {total}, and each column the share it prints over itself.'),
        }
        source = reading_source(P, unit, language, level, year)
        if source:
            card['sourceMaterial'] = source
        cards.append(card)


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
            (f'The scheme prints no mark on these lines; it prices the question '
             f'"{ask.notation}" and says: "{ask.notes[0]}". '
             if ask.notes else
             (f'Every gap is answered; the scheme reprints each sentence with the '
             f'right preposition {"in bold" if ask.bold == "bold" else "circled"}, '
             f'prices them together, "{ask.notation}", '
             f'and each answer is shown here after its sentence\'s opening words. ')
             if ask.bold else
             f'Every gap is answered; the scheme prints no mark on these lines and '
             f'prices them together, "{ask.notation}". '
             if ask.by_rate else
             'Every gap is answered; the scheme prints the mark it pays on each. ')
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
            'notes': ((f'The paper sets questions 1 and 2 here and a candidate '
                       f'answers both; the scheme prices question {q} '
                       f'{ask.total}, as {ask.notation!r}.')
                      if S.grammar_compulsory else
                      (f'The paper sets question 1 OR question 2 here and this is '
                       f'alternative {q}; the scheme prices it {ask.total}, as '
                       f'{ask.notation!r}.')),
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
