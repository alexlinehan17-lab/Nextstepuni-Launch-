#!/usr/bin/env python3
"""Author every Spanish ask the papers print and the schemes answer.

    python3 scripts/markbank/authoring/es_all.py --report
    python3 scripts/markbank/authoring/es_all.py --exclusions   # rewrite them
    python3 scripts/markbank/authoring/es_all.py > scripts/markbank/authored/spanish.json

Census-driven: the ten sittings print 653 leaf asks across three booklets each,
and this walks that census rather than choosing what to card.

WHAT ONE CARD IS
----------------
One printed ask. Its question comes from the PAPER (es_paper.py) and its
marking points from the SCHEME (es_scheme.py). The two are joined on the three
things they both print — the address, the text's own TITLE and the tariff — and
the census checks all three (Law 4: join on whatever BOTH documents print; the
Spanish scheme never reprints the question, so align.py has nothing to score).

THE TEXT TRAVELS WITH THE CARD, FROM THE BOOKLET IT WAS PRINTED IN
------------------------------------------------------------------
Every reading answer is drawn from a text, so each card binds `sourceMaterial`
to the exact pages of its own text. For Section A that is the question paper.
For HIGHER SECTION B it is not: the article is printed on a two-page LOOSE
SHEET with its own SEC file id, and the paper says so — "The questions refer to
the text on the loose sheet provided separately." Those cards carry
`sourceLabel: 'Section B'`, which build-deck.mjs resolves against Paper Trail's
index into `sourceMaterial.sourceFileid`. A card that let it default to the
question paper would open a student on the page of QUESTIONS about an article
they cannot see, silently — the corruption `types/markBank.ts` warns about on
that very field.

THE ANSWER LANGUAGE IS PART OF THE ASK
--------------------------------------
Spanish sets some questions in Spanish and some in English, and both schemes
head every section "Questions must be answered in the language indicated on the
examination paper" — at Ordinary with the penalty spelled out, 50% of the marks
for a whole question in the wrong language and nothing at all for a sub-part.
Every card says which language is wanted and quotes that rule verbatim.

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

from es_paper import EsPaper                                   # noqa: E402
from es_scheme import EsScheme, ref_for                        # noqa: E402
from es_topics import (topic_for, concept_for, answer_language,  # noqa: E402
                       language_note, SAYS_SPANISH, SAYS_ENGLISH)
from paper_census import census_subject                        # noqa: E402

SUBJECT = 'spanish'
YEARS = tuple(range(2010, 2027))
LEVELS = ('hl', 'ol')
# The sittings carded so far, one commit each. A sitting is added here only
# once its cards have been read against the paper and the scheme.
CARDED = {(y, l) for y in (2021, 2022, 2023, 2024, 2025) for l in LEVELS} | {
    (2026, 'hl'), (2026, 'ol'), (2020, 'ol'), (2020, 'hl'),
    (2019, 'hl'),
    (2019, 'ol'),
    (2018, 'hl'),
    (2018, 'ol'),
    (2017, 'hl'),
    (2017, 'ol'),
    (2016, 'hl'),
    (2016, 'ol'),
    (2015, 'hl'),
    (2015, 'ol'),
    (2014, 'hl'),
    (2014, 'ol'),
    (2013, 'hl'),
    (2013, 'ol'),
    (2012, 'hl'),
    (2012, 'ol'),
}
# The 2021-2025 sittings shipped before this lane. Their cards keep the shapes
# they shipped with until a reviewed change re-cuts them; every later sitting
# gets the claimable shapes below from its first commit.
FROZEN_SHAPES = {(y, l) for y in (2021, 2022, 2023, 2024, 2025) for l in LEVELS}
# The sittings whose "direction" asks (Higher A1a Q5, A1b Q4) are carded with
# the scheme's own direction on an unprinted row. 2021-2025 still exclude them.
DIRECTION_CARDED = {(2026, 'hl'), (2020, 'hl'), (2025, 'hl'), (2024, 'hl'), (2023, 'hl'), (2022, 'hl'), (2021, 'hl'), (2019, 'hl'), (2018, 'hl'), (2017, 'hl'), (2016, 'hl'), (2015, 'hl'), (2014, 'hl'), (2013, 'hl'), (2012, 'hl')}
# The sittings whose Listening Comprehension Test is carded: each ask with the
# official SEC recording (data/spanishAudio.json, verified), scored on its own
# as French listening is (coordinator ruling, 11 Nov 2026).
LISTENING_CARDED = {(2026, 'hl'), (2026, 'ol'), (2020, 'hl'), (2020, 'ol'), (2025, 'hl'), (2025, 'ol'), (2024, 'hl'), (2024, 'ol'), (2023, 'hl'), (2023, 'ol'), (2022, 'hl'), (2022, 'ol'), (2021, 'hl'), (2021, 'ol'), (2019, 'hl'), (2019, 'ol'), (2018, 'hl'), (2018, 'ol'), (2017, 'hl'), (2017, 'ol'), (2016, 'hl'), (2016, 'ol'), (2015, 'hl'), (2015, 'ol'), (2014, 'hl'), (2014, 'ol'), (2013, 'hl'), (2013, 'ol'), (2012, 'hl'), (2012, 'ol')}
# The sittings whose written production (Higher B Q5 and Section C, Ordinary
# Section B) is carded on the scheme's own marking grid (es_writing.py), in the
# French writing-rubric shape (coordinator ruling, 11 Nov 2026).
WRITING_CARDED = {(2026, 'hl'), (2026, 'ol'), (2020, 'hl'), (2020, 'ol'), (2025, 'hl'), (2025, 'ol'), (2024, 'hl'), (2024, 'ol'), (2023, 'hl'), (2023, 'ol'), (2022, 'hl'), (2022, 'ol'), (2021, 'hl'), (2021, 'ol'), (2019, 'hl'), (2019, 'ol'), (2018, 'hl'), (2018, 'ol'), (2017, 'hl'), (2017, 'ol'), (2016, 'hl'), (2016, 'ol'), (2015, 'hl'), (2015, 'ol'), (2014, 'hl'), (2014, 'ol'), (2013, 'hl'), (2013, 'ol'), (2012, 'hl'), (2012, 'ol')}

# The one row text a card may carry that is not a slice of the scheme, from
# UNPRINTED_ANSWER in types/markBank.ts (build-deck.mjs refuses any other).
UNPRINTED = 'The scheme prints no answer for this part.'
# "[Any mark from 0 to 6 may be awarded for this question]": the scheme prints
# every value from 0 to 6 as a mark the examiner may give.
ANY_MARK = re.compile(r'\bAny mark from (\d{1,2}) to (\d{1,2})\b', re.I)
LEVEL_WORD = {'hl': 'higher', 'ol': 'ordinary'}
LEVEL_TITLE = {'hl': 'Higher', 'ol': 'Ordinary'}

# The most options one card may show, from MAX_LONG_OPTION_ROWS in
# types/markBank.ts. Nothing in this corpus reaches it — the longest menu the
# Spanish scheme prints is nine — but the ceiling is stated so a later sitting
# is trimmed with disclosure rather than shipped as a wall of text.
MAX_OPTIONS = 16
# The most marking rows a `fixed` card may carry, from MAX_ROWS via rowCapFor
# in types/markBank.ts. A part listing more separate answers than this is
# refused rather than trimmed: trimming would delete answers the SEC pays for.
MAX_ROWS = 5

# The scheme's own direction to the examiner standing where an answer would be.
# "Discussion on any three relevant points" prices a 12-mark essay and states
# nothing a student can check themselves against; "[Any mark from 0 to 6 may be
# awarded for this question]" prices a rewriting task the same way.
DIRECTION_ONLY = re.compile(
    r'^Discussion on any\b|^Any mark from\b|^Marks? awarded\b'
    # 2020 prints the direction on Q.5's own head: "= 12 marks for any four
    # relevant points (12m)".
    r'|^for any \w+ relevant points\b'
    # 2012 Higher literature Q3 and Q4: "Any 3 relevant points taken from
    # lines 9 – 16. (4 +3 + 3 marks)".
    r'|^Any \d relevant points\b', re.I)

# The section a card is filed under, which SecCardBase types as a single
# letter. The section TOKEN in a citation carries more than that — "A1a" is
# Section A's literature route — so the two are kept apart deliberately.
CARD_SECTION = {'A1a': 'A', 'A1b': 'A', 'A2': 'A', 'A': 'A', 'B': 'B', 'C': 'C'}

GRID_EVIDENCE = {
    'B': ('the scheme answers this ask with a BAND GRID and nothing else — '
          '"CONTENT/COMMUNICATION 25 marks · TOP · High level of coherence · '
          'Clear argumentation · Communicative intention fulfilled … BOTTOM · '
          'Lack of coherence", and the same again for Language. Those are the '
          'qualities of a piece of writing, not answers, and a card would ask '
          'a student to tick "Idiomatic Spanish" as something they were '
          'supposed to have written.'),
    'C': ('the scheme answers this ask with a BAND GRID and nothing else — '
          '"6 marks: Communicative intention fulfilled. Verbs must be correct '
          'for full marks. · 4-5 marks: Communicative intention more or less '
          'fulfilled … 0 marks: No communication of message." Those are the '
          'qualities of a piece of writing, not answers.'),
}

AUDIO_EVIDENCE = (
    'the ask can only be answered from the recording. The Listening '
    'Comprehension Test is a separate SEC booklet whose own instructions read '
    '"This will be played three times: first right through, then in two '
    'segments with a long pause after each segment, and finally, right through '
    'again", and neither the booklet nor the marking scheme prints a word of '
    'what is said — this subject\'s scheme carries no CD script at all. No '
    'verified playback copy of the SEC recording is bound to this deck, so the '
    'card would be unanswerable from what it shows.')


def card_id(year, level, section, q, letter, roman):
    parts = ['es', str(year), level, section.lower()]
    if q is not None:
        parts.append(str(q))
    if letter:
        parts.append(letter)
    if roman:
        parts.append(roman)
    return '-'.join(parts)


def _task_line(region):
    """The region's own printed instruction, without the text beneath it.

    Read down from the question head and stopped at the first line that names
    a language — which is what the instruction exists to do — or at the text's
    own first numbered paragraph. Four lines at most: past that the paper has
    stopped instructing and started printing the article.
    """
    out = []
    for raw in region.lead_lines[:4]:
        s = re.sub(r'^(?:QUESTION|Question|Q)\s*\.?\s*\d\s*\.?\s*', '', raw)
        s = re.sub(r'\(\s*\d{1,3}\s*marks?\s*\)', '', s, flags=re.I).strip()
        if not s:
            continue
        if re.match(r'^\d{1,2}\s*\.', s):
            break
        out.append(s)
        if SAYS_SPANISH.search(s) or SAYS_ENGLISH.search(s):
            break
    return ' '.join(' '.join(out).split())


def _old_instruction(region):
    """A 2010-2020 question's own printed instruction, without its number.

    The old papers head a comprehension "1. Lee este artículo sobre el
    alpinismo y contesta las preguntas en ESPAÑOL. (50 marks)", where the 2021
    layout prints "Question 1" on a line of its own; _task_line stops at the
    numbered line and finds nothing. The head is read up to its marks.
    """
    out = []
    for n, raw in enumerate(region.lead_lines[:3]):
        line = re.sub(r'^\d\s*\.\s*', '', raw) if n == 0 else raw
        cut = re.search(r'\(\s*\d{1,3}\s*marks?\s*\)', line, re.I)
        if cut:
            out.append(line[:cut.start()].strip())
            break
        out.append(line)
    else:
        return ''
    return ' '.join(' '.join(out).split())


def _old_region_lead(region, S, section, q):
    """Name a 2010-2020 text by the title the PAPER prints above it.

    The old papers set titles in mixed case ("Tocando el cielo con las
    manos"), which the reader's capitals test does not take for a title. The
    scheme prints the same title on its question head — "Question 1. Tocando el
    cielo con las manos (50 marks)" — so the paper's line that equals it is the
    title: the join is on what both documents print, and the words are the
    paper's.
    """
    if region.title:
        return
    want = S.titles.get((section if section != 'A1a' else section, q))
    if not want:
        return
    fold = lambda t: ' '.join(re.sub(r'[^\w ]', ' ', t.casefold()).split())
    for line in region.lead_lines:
        if fold(line) == fold(want):
            region.title = line
            return


def _stem_text(block):
    """A question's printed head, with its own tariff taken off.

    "(15 marks)" is printed beside the head on the paper; leaving it on the
    stem puts a tariff where the card already shows one.
    """
    text = ' '.join((block.text or '').split())
    return re.sub(r'\s*\(\s*\d{1,3}\s*marks?\s*\)\s*', ' ', text, flags=re.I).strip()


# 2020 Higher: the paper says "See Loose Insert", and the SEC never published the
# English-version loose sheet (examinations.ie answers 404 for LC012ALP015EV
# and LC012ALPO15EV; the Paper Trail index lists no 2020 EV "Section B"). It did
# publish the Irish-version sheet, LC012ALP015IV — "Page 7 of 16/Lch 7 de 16",
# headed "SECTION B / ROINN B" as the English sheets of other years are, and
# carrying the article itself in Spanish: "LA MODA RÁPIDA", the title the 2020
# scheme heads its Section B answers with. Read from that sheet, never from the
# question paper, whose page 7 is blank but for the pointer.
BORROWED_INSERT = {2020: 'LC012ALP015IV'}


def source_material(P, token, region, language, level, year):
    """The pages this card's text is printed on, in the booklet that prints it."""
    if token == 'B' and level == 'hl' and not P.insert_pages and year in BORROWED_INSERT:
        fileid = BORROWED_INSERT[year]
        path = os.path.join(ROOT, 'paper-trail-corpus', 'exampapers', str(year),
                            f'{fileid}.pdf')
        import pymupdf
        with pymupdf.open(path) as doc:
            text = ' '.join(doc[0].get_text().split())
            pages = list(range(1, doc.page_count + 1))
        title = region.title or ''
        assert title and title in text, (year, title)
        return {
            'kind': 'source-text',
            # The source line says which print the student is reading
            # (coordinator ruling, 11 Nov 2026).
            'label': 'SECTION B — IRISH-VERSION LOOSE SHEET',
            'title': f'{title} — answer in {language}',
            'pages': pages,
            'sourceFileid': fileid,
            'attribution': (f'SEC Spanish {year} Higher Level examination — Section B '
                            f'text, printed on the loose sheet supplied with the paper '
                            f'(Irish-version sheet). © State Examinations Commission.'),
            'presentationNote': (
                'The SEC published this year\'s loose sheet only with the '
                'Irish-version paper. The article on it is the Spanish text the '
                'questions refer to; read it exactly as it was printed, then answer.'),
        }
    if token == 'B' and level == 'hl' and P.insert_pages:
        return {
            'kind': 'source-text',
            'label': 'SECTION B — LOOSE SHEET',
            'title': f'{P.insert_title or "Section B text"} — answer in {language}',
            'pages': list(P.insert_pages),
            # Resolved by build-deck.mjs from Paper Trail's index, never typed:
            # this document is NOT the question paper, and defaulting to the
            # paper's own id would open the wrong booklet.
            'sourceLabel': 'Section B',
            'attribution': (f'SEC Spanish {year} {LEVEL_TITLE[level]} Level '
                            f'examination — Section B text, printed on the loose '
                            f'sheet supplied with the paper. '
                            f'© State Examinations Commission.'),
            'presentationNote': (
                'The examination supplies this text on a separate loose sheet. '
                'Read it exactly as it was printed, then answer.'),
        }
    pages = region.text_pages or region.pages
    if not pages:
        return None
    # The text's own name, as the paper heads it: the article's title where it
    # prints one, and Higher Section A's prescribed-literature line — "1. (a)
    # Prescribed Literature: Gabriel García Márquez: Relato de un náufrago." —
    # where it prints prose with no title at all.
    head = re.sub(r'^(?:1\s*\.\s*)?\(\s*[ab]\s*\)\s*', '',
                  region.lead_lines[0] if region.lead_lines else '')
    title = (region.title or (head if head.lower().startswith('prescribed')
                              else '') or _task_line(region)
             or 'Reading comprehension').rstrip(' .:;,')
    return {
        'kind': 'source-text',
        'label': 'READING COMPREHENSION',
        'title': f'{title[:80]} — answer in {language}',
        'pages': list(pages),
        'attribution': (f'SEC Spanish {year} {LEVEL_TITLE[level]} Level examination '
                        f'paper — © State Examinations Commission.'),
        'presentationNote': ('Read the text exactly as the examination printed '
                             'it, then answer.'),
    }


def build():
    cards = []
    refused = collections.Counter()
    examples = collections.defaultdict(list)
    excluded = []

    def refuse(reason, ref, evidence=''):
        refused[reason] += 1
        examples[reason].append(ref)
        excluded.append({'ref': ref, 'reason': reason, 'evidence': evidence})

    for year in YEARS:
        for level in LEVELS:
            if (year, level) in CARDED:
                _sitting(year, level, cards, refuse)
    return cards, refused, examples, excluded


def _sitting(year, level, cards, refuse):
    P = EsPaper(year, level, SUBJECT)
    S = EsScheme(year, level, SUBJECT)
    by_key = S.by_key()
    grids = S.grids
    leaves = P.leaves()

    if (year, level) in LISTENING_CARDED:
        _listening(year, level, P, S, cards, refuse)
    else:
        for q, letter, text, _page in P.aural_asks():
            ref = ref_for(year, level, 'L', q, letter, None)
            refuse('the ask needs the recording, which no card can carry', ref,
                   f'{year} {level.upper()} Listening Comprehension Test, '
                   f'Question {q}: {AUDIO_EVIDENCE}')

    whole_carded = set()
    for key in sorted(leaves, key=lambda k: tuple(str(x) for x in k)):
        section, q, letter, roman = key
        text, token, block = leaves[key]
        ref = ref_for(year, level, section, q, letter, roman)
        region = P.regions[token]
        if (section, q) in whole_carded:
            continue

        if section in ('B', 'C') and (
                key in grids or (section, q, None, None) in grids
                or (section, q, letter, None) in grids):
            if (year, level) in WRITING_CARDED:
                if level == 'hl' and section == 'B':
                    # One card for the printed choice of statements.
                    whole_carded.add((section, q))
                    letter = None
                card = _writing(year, level, P, section, q, letter)
                cards.append(card)
                continue
            line = (grids.get(key) or grids.get((section, q, letter, None))
                    or grids.get((section, q, None, None)))
            refuse('the scheme prints a band grid for this ask, not an answer',
                   ref, f'{year} {level.upper()} scheme, "{line}": '
                        f'{GRID_EVIDENCE[section]}')
            continue

        ask = by_key.get(key)
        if ask is None:
            # A part the scheme priced under its parent: Higher Section A's
            # journalistic Q.4 is one 6-mark ask whose two phrases the paper
            # prints as (a) and (b).
            ask = by_key.get((section, q, None, None)) \
                or by_key.get((section, None, letter, None))
        if ask is None:
            refuse('the scheme prices no answer for this printed ask', ref,
                   f'{year} {level.upper()} scheme: no entry addresses '
                   f'{ref.split(" ", 2)[2]}')
            continue
        if ask.fault:
            refuse('the two halves of the printed tariff disagree, so neither '
                   'can be trusted and the ask cannot be priced', ref,
                   f'{year} {level.upper()} scheme, {ask.section} Q{ask.q}: '
                   f'{ask.fault}')
            continue

        stem_block = region.stems().get(q if section != 'A2' else letter)
        stem = _stem_text(stem_block) if stem_block else ''
        instruction = _task_line(region)
        if P.old:
            _old_region_lead(region, S, section, q)
            instruction = instruction or _old_instruction(region)
        if not stem and level == 'ol':
            stem = instruction
        question = block.printed if block else text

        language = answer_language(question, stem, instruction)
        rule = S.unit_rules.get(CARD_SECTION.get(section, 'A'))
        rows = _rows_for(ask, language, rule,
                         stepped=(year, level) not in FROZEN_SHAPES)
        if rows is None and (year, level) in DIRECTION_CARDED:
            rows = _direction_rows(ask, language, rule)
            if rows is not None and ask.key != key:
                # The scheme prices the QUESTION, and the paper prints its
                # parts as a choice — "Explica … una de las frases siguientes:
                # (a) … O (b) …". A printed choice is one card, cited at the
                # question the scheme priced; every part it prints goes on it.
                whole_carded.add((section, q))
                letter = roman = None
                ref = ref_for(year, level, section, q, None, None)
                parts = [(k, v) for k, v in sorted(leaves.items(),
                                                   key=lambda kv: tuple(str(x) for x in kv[0]))
                         if k[0] == section and k[1] == q]
                pieces = []
                for n, (k, (t, _tok, b)) in enumerate(parts):
                    body = (b.printed if b else t).strip()
                    # The paper prints the "O" between the two alternatives on
                    # the first one's baseline; it goes on a line of its own.
                    body = re.sub(r'\s+O$', '', body)
                    if n:
                        pieces.append('O')
                    pieces.append(f'({k[2]}) {body}')
                question = '\n'.join(pieces)
        if rows is None:
            refuse('the scheme states a direction to the examiner where the '
                   'answer would be, not an answer', ref,
                   f'{year} {level.upper()} scheme, {ask.section} Q{ask.q}'
                   f'{ask.letter or ""}: '
                   f'"{(ask.points[0][0] if ask.points else "; ".join(ask.notes))[:140]}"')
            continue
        if isinstance(rows, str):
            refuse(rows, ref, f'{year} {level.upper()} scheme, {ask.section} '
                              f'Q{ask.q}{ask.letter or ""}, tariff '
                              f'{"+".join(map(str, ask.terms or []))}')
            continue

        # The prescribed text is named on the paper's own HEAD line — "(a)
        # Prescribed Literature: Gabriel García Márquez: Relato de un
        # náufrago." — and nowhere else. Matching against the whole region
        # lead searched the EXTRACT too, and eight cards were filed under El
        # medallón perdido because the word "medalla" happens to appear in the
        # náufrago passage.
        head = region.lead_lines[0] if region.lead_lines else ''
        topic = topic_for(level, section,
                          head if section == 'A1a'
                          else (region.title or instruction))
        if topic is None:
            refuse('the paper does not name which prescribed text it has set, '
                   'so the card cannot be filed against one', ref,
                   f'{year} {level.upper()} paper, Section A Question 1(a): '
                   f'"{region.lead[:110]}"')
            continue

        card = {
            'id': card_id(year, level, section, q, letter, roman),
            'subjectId': SUBJECT,
            'level': LEVEL_WORD[level],
            'year': year,
            'section': CARD_SECTION[section],
            'topicId': topic,
            'conceptId': concept_for(question),
            'questionRef': ref,
            'questionText': question,
            'tariffModel': {'kind': 'fixed'},
            'totalMarks': ask.total,
            'rows': rows,
            'notes': (
                f'The scheme prices this ask '
                f'{"+".join(map(str, ask.terms or [])) or ask.total} marks; the paper prints '
                f'it on page {block.page + 1 if block else region.pages[0]} of '
                f'the question booklet.'),
        }
        if stem and len(stem) >= 15 and stem != question:
            card['stem'] = stem
        source = source_material(P, token, region, language, level, year)
        if source:
            card['sourceMaterial'] = source
        cards.append(card)


AUDIO = os.path.join(ROOT, 'data', 'spanishAudio.json')
AURAL_FILEID = {'hl': 'LC012ALPA00EV.pdf', 'ol': 'LC012GLPA00EV.pdf'}
# Wingdings 0xFC, the tick the listening booklet prints in "Tick (✓) the
# correct answer"; its text layer carries the private-use code point.
TICK = '\uf0fc'


def _listening_rule(S):
    """The scheme's own language rule for the listening test, verbatim: the
    lines between "LISTENING COMPREHENSION (80 MARKS)" and its first item
    ("All answers must be in English." and the penalty for answering in
    Spanish)."""
    out, on = [], False
    for line in S.lines:
        s_ = ' '.join(line.split())
        if not on:
            on = bool(re.match(r'^LISTENING\s+COMPREHENSION\b', s_, re.I))
            continue
        if not s_ or s_.startswith('## Page'):
            continue
        if re.match(r'^\d\s*\.', s_):
            break
        out.append(s_)
    return ' '.join(out)


def _listening(year, level, P, S, cards, refuse):
    """One card per listening ask, answered from the official recording.

    The ask is the booklet's, set out line by line as printed (a tick-box ask
    keeps its options, which become the card's printed choices); the marking
    rows are the scheme's, read by es_scheme like the reading asks; the head
    the booklet prints above the question (the kind of recording, how often it
    is played, the item's title) is the stem; and the recording is the SEC's
    own, bound from data/spanishAudio.json, where every year's file is pinned
    by size, duration and hash.
    """
    from es_atlas import tags_for
    with open(AUDIO, encoding='utf-8') as fh:
        recording = next(r for r in json.load(fh) if r['year'] == year)
    fileid = AURAL_FILEID[level]
    assert fileid in recording['paperFileids'], (year, fileid)
    tags = tags_for(year, LEVEL_WORD[level], fileid)
    heads = P.aural_heads()
    rule = _listening_rule(S)
    by_key = S.by_key()
    for q, letter, lines, page in P.aural_ask_lines():
        ref = ref_for(year, level, 'L', q, letter, None)
        ask = by_key.get(('L', q, letter, None))
        if ask is None or ask.fault:
            refuse('the scheme prices no answer for this listening ask', ref,
                   f'{year} {level.upper()} scheme, listening Q{q}({letter}): '
                   f'{ask.fault if ask else "no entry"}')
            continue
        rows = _rows_for(ask, 'English', rule, stepped=True)
        if not isinstance(rows, list):
            refuse(rows or 'the scheme states a direction to the examiner where the '
                   'answer would be, not an answer', ref,
                   f'{year} {level.upper()} scheme, listening Q{q}({letter})')
            continue
        # A rule fragment the text layer leaves on its own line ("]") is not
        # printed matter of the ask.
        lines = [l.replace(TICK, '✓') for l in lines if re.search(r'\w', l)]
        choices = None
        tick = next((i for i, l in enumerate(lines) if re.match(r'^Tick\b', l)), None)
        if tick is None:
            # 2014 Ordinary sets "Tick the correct answer:" on the question's
            # own line ("How many workers …? Tick the correct answer:").
            tick = next((i for i, l in enumerate(lines)
                         if re.search(r'\bTick the correct answer[:.]\s*$', l)), None)
        if tick is None and 3 <= len(lines) <= 6 and lines[0].rstrip().endswith('?'):
            # … and prints Q4(b)'s three boxes with no instruction at all:
            # the printed lines under the question are its choices where the
            # scheme's answer is one of them.
            said = {re.sub(r'[\W_]+', ' ', t).strip().lower() for t, _m in (ask.points or [])}
            if any(re.sub(r'[\W_]+', ' ', l).strip().lower() in said for l in lines[1:]):
                tick = 0
        if tick is not None:
            choices = lines[tick + 1:]
            assert 2 <= len(choices) <= 5, (ref, lines)
        question = '\n'.join(lines)
        head_lines, _head_page = heads.get(q, ([], page))
        tag = tags.get(str(q))
        if tag is None:
            refuse('the Topic Atlas holds no question for this listening item', ref,
                   f'{year} {level.upper()} {fileid}: no Atlas question {q}')
            continue
        kind = re.match(r'^([A-ZÁÉÍÓÚÑ ]+):', head_lines[0]) if head_lines else None
        title = next((l for l in head_lines if l.isupper() and len(l) > 8
                      and not re.match(r'^[A-ZÁÉÍÓÚÑ ]+:', l)
                      and not l.startswith('(')),
                     kind.group(1).strip() if kind else f'Question {q}')
        card = {
            'id': card_id(year, level, 'L', q, letter, None),
            'subjectId': SUBJECT,
            'level': LEVEL_WORD[level],
            'year': year,
            'section': 'L',
            'topicId': tag['primary'],
            'conceptId': concept_for(lines[0]),
            'questionRef': ref,
            'questionText': question,
            'tariffModel': {'kind': 'fixed'},
            'totalMarks': ask.total,
            'rows': rows,
            'notes': (f'The scheme prices this ask '
                      f'{"+".join(map(str, ask.terms or [])) or ask.total} marks; the '
                      f'listening booklet prints it on page {page}.'),
            'stem': ' '.join(' '.join(head_lines).split()),
            'sourceMaterial': {
                'kind': 'source-text',
                'label': 'LISTENING COMPREHENSION TEST',
                'title': f'Question {q} — {title}'[:90],
                'pages': [page],
                # Resolved by build-deck.mjs from Paper Trail's index: the
                # listening booklet is its own SEC document.
                'sourceLabel': 'Aural Paper',
                'attribution': (f'SEC Spanish {year} {LEVEL_TITLE[level]} Level '
                                f'Listening Comprehension Test — © State '
                                f'Examinations Commission.'),
                'presentationNote': ('The question page of the listening booklet. '
                                     'Play the recording, then answer.'),
            },
            'audioMaterial': {**recording['source'],
                              'label': f'Question {q} · listening'},
        }
        if choices:
            card['questionChoices'] = choices
        cards.append(card)


# Which writing task a printed alternative is: the paper names it ("Write a
# diary entry", "Leave her a note", "Complete … the dialogue", "write a
# letter/email"), and each has its own published topic.
WRITING_TOPIC = (
    (re.compile(r'\bdiary\b', re.I), 'spanish-6-3'),
    (re.compile(r'\bnote\b', re.I), 'spanish-6-4'),
    (re.compile(r'\bdialogue\b', re.I), 'spanish-6-1'),
    (re.compile(r'\bletter\b|\be-?mail\b', re.I), 'spanish-6-2'),
)
ORDINALS = ('First', 'Second', 'Third', 'Fourth', 'Fifth')


def _writing(year, level, P, section, q, letter):
    """A written-production ask as a rubric card on the scheme's own grid."""
    import es_writing as W
    t = W.task(P, section, q, letter)
    ref = ref_for(year, level, section, q, letter, None)
    level_title = LEVEL_TITLE[level]
    practice = ['Write your answer in Spanish, then place it on the published grid. '
                'You are marked on this task alone, and where it asks you to choose '
                'statements, turns or points, on the ones you chose.']
    if level == 'hl' and section == 'B':
        g = W.grid_b5(year, level)
        topic = 'spanish-6-0'
        rubric = {'system': 'french', 'taskRequirements': g['requirements'],
                  'criteria': g['criteria'], 'markingGuideNote': ''}
        practice.append('Choose a band for Content/Communication and one for Language, '
                        'then the mark within each band.')
        pages = g['pages']
    else:
        if level == 'hl':
            g = W.grid_c(year, level, q, letter)
            requirements = (g['lead'] + g['option'][1:] + g['criteriaHead'][1:] + g['ladder']
                            + g['notes'] + g['direction'])
            note = '\n'.join(g['guidelines'])
        else:
            g = W.grid_ol_b(year, level, q, letter)
            requirements = g['lead'] + g['ladder']
            note = '\n'.join(g['section'])
        topic = next(tid for rx, tid in WRITING_TOPIC if rx.search(t['question'][:200]))
        unit = 'turn' if topic == 'spanish-6-1' else 'point'
        if g.get('global'):
            # 2021 and 2022 Higher mark the diary or note as a whole: "apply a
            # global mark to the best FOUR according to the criteria below".
            unit = 'piece'
            # Labelled "Global": the panel adds "mark" ("Global mark").
            criteria = [{'id': 'global', 'label': 'Global', 'maxMarks': g['per'],
                         'permittedMarks': list(range(g['per'] + 1)), 'guidance': []}]
        else:
            criteria = [{'id': f'{unit}-{i}', 'label': f'{ORDINALS[i - 1]} {unit}',
                         'maxMarks': g['per'], 'permittedMarks': list(range(g['per'] + 1)),
                         'guidance': []} for i in range(1, g['n'] + 1)]
        assert g['n'] * g['per'] == g['total'], (ref, g['n'], g['per'], g['total'])
        rubric = {'system': 'french', 'taskRequirements': requirements,
                  'criteria': criteria, 'markingGuideNote': note}
        practice.append('Place the whole piece on the scheme\'s bands above.' if unit == 'piece'
                        else f'Mark each {unit} you wrote on its own against the scheme\'s '
                             f'ladder above.')
        pages = g['pages']
    rubric['practiceNotes'] = practice
    total = sum(c['maxMarks'] for c in rubric['criteria'])
    card = {
        'id': card_id(year, level, section, q, letter, None),
        'kind': 'rubric',
        'subjectId': SUBJECT,
        'level': LEVEL_WORD[level],
        'year': year,
        'section': CARD_SECTION[section],
        'topicId': topic,
        'conceptId': concept_for(t['question']),
        'questionRef': ref,
        'questionText': t['question'],
        'totalMarks': total,
        'rubric': rubric,
        'schemePages': pages,
    }
    if t['stem']:
        card['stem'] = t['stem']
    if level == 'hl' and section == 'B':
        # The opinion piece is linked to the article it follows.
        region = P.regions['B']
        card['sourceMaterial'] = source_material(P, 'B', region, 'Spanish', level, year)
    else:
        card['sourceMaterial'] = {
            'kind': 'source-text',
            'label': 'WRITTEN PRODUCTION',
            'title': f'Section {section} Question {q}{f" ({letter})" if letter else ""} '
                     f'— answer in Spanish',
            'pages': t['pages'],
            'attribution': (f'SEC Spanish {year} {level_title} Level examination '
                            f'paper — © State Examinations Commission.'),
            'presentationNote': 'The task exactly as the examination printed it.',
        }
    return card


def _direction_rows(ask, language, rule):
    """The one unprinted row for an ask whose scheme prints a direction.

    Higher A1a Q5 ("Discussion on any three relevant points", 4 + 4 + 4) and
    A1b Q4 ("Any mark from 0 to 6 may be awarded for this question") are asks
    the scheme prices without printing an answer. Every printed ask gets a card
    (Alex, 2026-10-28): its one row says the scheme prints no answer, its note
    quotes what the scheme prints instead, and the marks a student may place
    themselves on are the values the scheme prints — every value from 0 to 6
    where it says "Any mark from 0 to 6", and 0, 4, 8, 12 where it prices
    three points at 4 each. Never a value it does not print.
    """
    if ask.total is None:
        return None
    printed = [t for t, _m in (ask.points or [])] + list(ask.notes or [])
    lines = [' '.join(l.split()) for l in (ask.answer_lines or []) if l and l.strip()]
    if len(ask.points or []) == 1 and len(lines) > 1:
        # Quoted line by line, as the scheme sets them: 2017 Higher prints
        # "for any 4 relevant points" / "Discussion of one character 3 + 3m"
        # / "Discussion of second character 3 + 3m" / …, a line going on in
        # lower case being the one before it wrapped.
        quoted_lines = []
        for l in lines:
            if quoted_lines and l[:1].islower():
                quoted_lines[-1] = f'{quoted_lines[-1]} {l}'
            else:
                quoted_lines.append(l)
        printed = quoted_lines + list(ask.notes or [])
    if not printed:
        return None
    m = next((ANY_MARK.search(t) for t in printed if ANY_MARK.search(t)), None)
    if m:
        lo, hi = int(m.group(1)), int(m.group(2))
        if (lo, hi) != (0, ask.total):
            return None
        steps = list(range(lo, hi + 1))
    elif ask.terms and len(ask.terms) > 1:
        # 4 + 4 + 4 places at 0, 4, 8, 12; 2012's 4 + 3 + 3 at 0, 4, 7, 10,
        # the first point paid 4 as the scheme's order prints it.
        steps = [0]
        for t in ask.terms:
            steps.append(steps[-1] + t)
    else:
        return None
    if steps[-1] != ask.total:
        return None
    quoted = ' and '.join(f'“{t}”' for t in printed)
    tariff = (ask.head_notation or '').strip()
    note = f'The scheme prints no answer for this ask. In its place it prints {quoted}'
    if tariff:
        note += f', under the tariff “{tariff}”'
    note += '. ' + language_note(language, rule)
    return [{'id': 'r-1', 'kind': 'criterion', 'verbatim': UNPRINTED,
             'marks': ask.total, 'unprinted': True, 'permittedMarks': steps,
             'contextNote': note}]


# A label the scheme prints in front of each of several answers on one line:
# "Who?: A recently-married couple Where?: Sitting-room …", "Day: Friday
# Date: 19th June", "Max.: 30 Min.: 23".
ANSWER_LABEL = re.compile(r'\s+(?=[A-Z][a-z]{1,8}\.?\??:\s)')
ROMAN_MARK = re.compile(r'\s*\((?:i|ii|iii|iv|v)\)\s*')


# 2016-2019 also print the figure alone: "Las colas [3] y los retrasos [2] (en las
# fronteras de los países) (3+2m)" (2018 Ordinary Q1(h)).
PRICE_BRACKET = re.compile(r'\[\s*(\d{1,2})\s*(?:m(?:arks?)?)?\s*\]')
NOTE_BRACKET = re.compile(r'\[(?!\s*\d{1,2}\s*(?:m(?:arks?)?)?\s*\])[^\]]*\]')


def _bracketed(raw, text, marks):
    """[(component, marks)] where the scheme prices part of ONE answer in a
    square bracket, or None.

    "He has been successful [1m] with very difficult cases; … (2+2m)": the
    first answer is worth 2 and its first half alone 1. "Reconstruction [1m]
    and transplants [1m] of feet/ hands/ legs/ fingers/ toes (2+1m)": the
    brackets price two components and the rest of the answer takes the rest of
    its tariff. The answer is found in the part's printed lines with its
    brackets in place; each bracket closes a component priced at the bracket's
    own figure, and what follows the last bracket is priced at what the
    answer's printed tariff leaves. Never a split the scheme does not print.
    """
    if not raw or not PRICE_BRACKET.search(raw):
        return None
    clean = NOTE_BRACKET.sub(' ', raw)
    gap = r'\s*(?:\[\s*\d{1,2}\s*(?:m(?:arks?)?)?\s*\]\s*)?'
    words = text.split()
    m = re.search(gap.join(map(re.escape, words)) + r'(?:\s*\[\s*\d{1,2}\s*(?:m(?:arks?)?)?\s*\])?',
                  clean)
    if not m or not PRICE_BRACKET.search(m.group(0)):
        return None
    segs = PRICE_BRACKET.split(m.group(0))
    parts = [(' '.join(segs[i].split()).strip(' ,;'), int(segs[i + 1]))
             for i in range(0, len(segs) - 1, 2)]
    rest = ' '.join(segs[-1].split()).strip(' ,;.')
    used = sum(n for _t, n in parts)
    if rest and used == marks and parts and re.fullmatch(r'\([^()]*\)', rest):
        # Words the scheme accepts but does not require, printed after the
        # last bracket: they belong to the last component ("… y los retrasos
        # [2] (en las fronteras de los países)").
        parts[-1] = (f'{parts[-1][0]} {rest}', parts[-1][1])
    elif rest:
        if marks - used <= 0:
            return None
        parts.append((rest, marks - used))
    elif used != marks:
        return None
    if len(parts) < 2 or not all(t for t, _n in parts):
        return None
    return parts


# 2016-2019 also price a component of ONE answer in a ROUND bracket set inside
# the line: "Thousands of Cubans lined the quay (1m) full of joy (1m) making
# everyone feel welcome in their country (1m). (3m)" (2017 Higher Q1(b)).
PRICE_ROUND = re.compile(r'\(\s*(\d{1,2}(?:\s*\+\s*\d{1,2})*)\s*m\s*\)')


def _round_components(ask):
    """[(component, [terms])] where the scheme prices the parts of one answer
    in round brackets inside its printed line, or None.

    Each bracket closes a component at its own figures ("(1 + 1m)" is one
    component worth 1 and 1 more); what follows the last bracket is priced at
    what the part's printed tariff leaves: 2018 Higher Q1(a) "People share
    their food with pets (2m) (for example) Two of: (a bit of) bread, omelette
    or chicken (so they can taste it too) (4m)" is 2, and the 2 the tariff
    leaves.
    """
    raw = ' '.join((ask.raw or '').split())
    if not raw or not PRICE_ROUND.search(raw) or ask.total is None:
        return None
    if len(ask.points or []) > 1:
        return None        # answers the scheme already prices one to a line
    if (not ask.quota and ask.points and len(ask.terms or []) > 1
            and _separate_answers(ask.points[0][0], len(ask.terms))):
        return None        # answers the line's own separators already cut apart
    segs = PRICE_ROUND.split(raw)
    parts = []
    for i in range(0, len(segs) - 1, 2):
        text = segs[i].strip(' ,;')
        terms = [int(t) for t in re.findall(r'\d{1,2}', segs[i + 1])]
        if not text:
            return None
        parts.append((text, terms))
    rest = segs[-1].strip(' ,;.')
    used = sum(sum(t) for _x, t in parts)
    if rest:
        if ask.total - used <= 0:
            return None
        parts.append((rest, [ask.total - used]))
    elif used != ask.total:
        return None
    if len(parts) < 2:
        return None
    return parts


def _round_component_row(ask, parts, note):
    """One criterion row: each component claimed at the values its own
    bracket prints, the row at their sums."""
    out = []
    for i, (text, terms) in enumerate(parts, start=1):
        steps = [0]
        for t in terms:
            steps.append(steps[-1] + t)
        out.append({'id': f'p{i}', 'verbatim': text, 'marks': steps[-1], 'permittedMarks': steps})
    sums = {0}
    for p in out:
        sums = {x + y for x in sums for y in p['permittedMarks']}
    return [{'id': 'r-1', 'kind': 'criterion', 'verbatim': ' '.join(t for t, _n in parts),
             'marks': ask.total, 'permittedMarks': sorted(sums), 'parts': out,
             'contextNote': note}]


def _component_row(rid, text, marks, parts, note=None):
    """One answer whose components are claimed on their own printed marks."""
    sums = {0}
    for _t, n in parts:
        sums |= {x + n for x in sums}
    row = {'id': rid, 'kind': 'criterion', 'verbatim': text, 'marks': marks,
           'permittedMarks': sorted(sums),
           'parts': [{'id': f'p{i}', 'verbatim': t, 'marks': n, 'permittedMarks': [0, n]}
                     for i, (t, n) in enumerate(parts, start=1)]}
    if note:
        row['contextNote'] = note
    return row


INLINE_COUNT = re.compile(r'\b(?:one|two|three|four|five)\s+of\s*\)?\s*:', re.I)


def _separate_answers(text, n):
    """The n answers one printed line holds, cut where the scheme separates
    them, or None where it prints one answer whose marks it splits.

    Tried in order, and taken only where the cut gives exactly as many pieces
    as the tariff has terms: the scheme's semicolons ("Water; electricity;
    toilets; showers (1+1+1+1m)"); a label before each answer ("Max: 27 Min:
    18 (2+2m)"); romans ("(i) has the most days of sun in Europe (ii) cheap
    (2+1m)"); commas ("Children, elderly, people with illnesses (2+2+2m)").
    Each piece is a slice of the scheme's line, never reworded.

    A line that states a count of its own is never cut inside the list the
    count is over: 2019 Higher listening Q1(a) "150 members (including) two
    of: men, women and children (2+2m)" pays the count over the list after it,
    and a cut at the comma would make "men" one answer and "women and
    children" another. A cut BEFORE the count stands: 2021 Higher listening
    Q4(d) "It was eaten at the time (of the book); (made) with two of: …".
    """
    counted = INLINE_COUNT.search(text)
    cuts = (
        [p.strip() for p in text.split(';')],
        ANSWER_LABEL.split(text),
        ROMAN_MARK.split(text),
        [p.strip() for p in text.split(',')],
        # "Tennis and skiing (2+2m)": two one-word answers. Only where every
        # piece is a word or two; "Reconstruction and transplants of feet"
        # is one answer.
        [p for p in text.split(' and ')] if all(
            len(p.split()) <= 2 for p in text.split(' and ')) else [],
        # Whole sentences, each closed by its full stop: 2019 Higher listening
        # Q7(a) "It is the series that has won the most awards in the history
        # of television." / "It is a cultural phenomenon (of the 21st
        # Century). (2+1m)".
        re.split(r'(?<=\.)\s+(?=[A-Z])', text) if text.rstrip().endswith('.') else [],
        # Last, and only on a line with no comma and no "and": slashes, where
        # they part exactly as many answers as the tariff prices. 2013 Higher
        # listening Q3(c) "Share a flat/ do the shopping/ manage money
        # (1+1+1 marks)"; but "in her shops and online/ internet (2+2)" is
        # one answer's two words, and its "and" gives that away.
        [p for p in text.split('/')] if not re.search(r',|\band\b', text) else [],
    )
    for pieces in cuts:
        # A roman cut leaves the comma that closed the answer before it: "(i)
        # It will cost half the price, (ii) no stress/ without stress (1+1m)".
        pieces = [p.strip().rstrip(',').strip() for p in pieces if p and p.strip()]
        # … and the "and" before the next answer: 2014 Ordinary Q5(c) "(i) she
        # had a very bad voice and (ii) they also thought she was crazy."
        pieces = [re.sub(r'\s+(?:and|y)$', '', p) for p in pieces]
        if counted and not INLINE_COUNT.search(pieces[-1] if pieces else ''):
            continue
        if len(pieces) == n:
            return pieces
    return None


def _rows_for(ask, language, rule, stepped=False):
    """The card's marking rows, or None (a direction) or a refusal string.

    Every non-zero partial the scheme prints ("[degree = 2m]") is then made
    claimable on the row it belongs to (_claimable_partials).
    """
    partials = _partials(ask)
    rows = _rows_core(ask, language, rule, stepped,
                      skip_notes={note for note, _p, whole in partials if whole})
    if partials and isinstance(rows, list):
        rows = _claimable_partials(ask, rows, partials)
    if stepped and isinstance(rows, list):
        rows = _menu_component_partials(ask, rows)
    return rows


def _menu_component_partials(ask, rows):
    """A menu answer the scheme prices in part inside its own line: 2013
    Higher Section B Q4(a) "- it is sometimes hidden [1] by the use of
    stimulants / sedatives" in a "Two of:" menu at 2 each. The slice before
    the bracket is one more option of the menu at the bracket's price
    (optionMarks), as a partial printed in a note already is
    (_claimable_partials). A menu paid in descending steps has no price per
    option to set it against, and is left as it is."""
    raw = ' '.join((ask.raw or '').split())
    if not PRICE_BRACKET.search(raw):
        return rows
    out = []
    for row in rows:
        g = row.get('group')
        if row.get('kind') != 'anyN' or not g or g.get('perOptionSteps'):
            out.append(row)
            continue
        marks = list(g.get('optionMarks') or [g['perOption']] * len(g['options']))
        extra = []
        for option, price in zip(g['options'], marks):
            words = option.split()
            gap = r'\s*(?:\[\s*\d{1,2}\s*(?:m(?:arks?)?)?\s*\][,;]?\s*)?'
            m = re.search(gap.join(re.escape(w.rstrip(',;')) + r'[,;]?' for w in words), raw)
            if not m:
                continue
            # Each bracket inside the answer closes a part of it; the slice up
            # to it is worth what the brackets up to it add to. 2020 Higher B
            # Q4(c) "One of: - To buy less [2m], we all have a lot of clothes
            # that we don't use [2m]; we should always consider … [1m]" offers
            # "To buy less" at 2 and "To buy less, we all have … use" at 4.
            seg, run = m.group(0), 0
            for b in PRICE_BRACKET.finditer(seg):
                if b.end() >= len(seg.rstrip(' .')):
                    break       # a price at the answer's end is its own
                run += int(b.group(1))
                part = ' '.join(PRICE_BRACKET.sub(' ', seg[:b.start()]).split()).strip(' ,;')
                part = re.sub(r'\s+([,;])', r'\1', part)
                if part and 0 < run < price:
                    extra.append((part, run))
        if extra:
            g = dict(g)
            g['options'] = list(g['options']) + [t for t, _n in extra]
            g['optionMarks'] = marks + [n for _t, n in extra]
            g['perOption'] = max(g['optionMarks'])
            row = {**row, 'group': g}
        out.append(row)
    return out


# A partial the scheme prices in a bracket: "degree = 2m", "studying hard =
# 2m", "to understand the language =1m". Read up to its price; what follows it
# ("if only correct information given") is a condition, kept quoted.
# 2013 prints the figure alone: "[alarm =1]".
PARTIAL = re.compile(r'^\s*(.*?\S)\s*=\s*(\d{1,2})\s*(?:m(?:arks?)?\b)?\s*(.*)$', re.I)
ORDER_NOTE = re.compile(r'first correct answer|for the first', re.I)
STOPWORDS = {'the', 'and', 'with', 'that', 'this', 'their', 'they', 'them', 'from', 'about',
             'have', 'into', 'there', 'were', 'what', 'when', 'only', 'more', 'than'}


def _words(text):
    return {w for w in re.findall(r'[a-záéíóúñü]+', text.lower()) if len(w) > 3 and w not in STOPWORDS}


def _partials(ask):
    """[(note, [(answer, marks)], whole)]: every NON-ZERO partial a note prices.

    A note that only orders a menu's tariff ("[First correct answer = 2m]") is
    not one. A zero ("[largest = 0m]") is the scheme ruling an answer out: it
    stays a note on the row. `whole` is whether the note is nothing but
    priced partials, so it need not also be quoted.
    """
    out = []
    notes = list(ask.notes or [])
    for k, note in enumerate(notes):
        if ORDER_NOTE.search(note):
            continue
        # A lead-in printed on the line above a partial ("If only answering:"
        # / "[there is a necessity to build more domes = 1m]") is the partial's
        # own condition: it travels with it as one option.
        flat = ' '.join((ask.raw or '').split())
        lead = next((n for n in notes if n.rstrip().endswith(':')
                     and f'{" ".join(n.split())} [{" ".join(note.split())}' in flat), '')
        parsed, whole = [], True
        for piece in [p for p in note.split(';') if p.strip()]:
            m = PARTIAL.match(piece)
            if not m:
                whole = False
                continue
            text, marks, tail = m.group(1).strip(), int(m.group(2)), m.group(3).strip()
            if tail or not marks:
                whole = False
            if marks:
                parsed.append((f'{lead} {text}' if lead else text, marks))
        if parsed:
            out.append((note, parsed, whole))
            if lead and whole:
                out.append((lead, [], True))
    return out


def _claimable_partials(ask, rows, partials):
    """The rows with every non-zero partial claimable (coordinator ruling, 12 Nov
    2026): the answer it belongs to becomes a one-pick group of the full answer
    at its price and each printed partial at its own (optionMarks), counted
    once at the best one claimed. A partial for a menu's answer is one more
    option of the menu at its own price.

    Which answer a partial belongs to is read from where the scheme prints it:
    straight after an answer, it is that answer's ("A recognised qualification;
    [degree = 2m] to understand how …"); after the last answer, it is the one it
    shares words with ("[to understand the language = 1m]"), or, sharing none
    and priced like every answer, an alternative to any of them ("Metro; bus
    (3+3m) [airport = 3m]"), or else the last answer's.
    """
    rows = [dict(r) for r in rows]
    # One answer per printed line, where a frozen card read two printed answers
    # as one ("(Several) zones … cameras (installed)" / "There was a problem
    # with the alarm" (2+2m)) and a partial belongs to one of them.
    if (len(rows) == 1 and rows[0]['kind'] == 'point' and ask.terms and len(ask.terms) > 1
            and ask.answer_lines and len(ask.answer_lines) == len(ask.terms)):
        note = rows[0].get('contextNote')
        rows = [{'id': f'r-{i}', 'kind': 'point', 'verbatim': text, 'marks': marks,
                 **({'contextNote': note} if i == 1 and note else {})}
                for i, (text, marks) in enumerate(zip(ask.answer_lines, ask.terms), start=1)]
    raw = ' '.join((ask.raw or '').split())
    for note, parsed, _whole in partials:
        if not parsed:
            continue
        at = raw.find(' '.join(note.split()))
        starts = [raw.find(' '.join(str(r.get('verbatim'))[:25].split())) for r in rows]
        before = [i for i, st in enumerate(starts) if 0 <= st < at]
        target = before[-1] if before else len(rows) - 1
        if len(rows) > 1 and target == len(rows) - 1:
            shared = [len(_words(r.get('verbatim') or '') & _words(' '.join(t for t, _m in parsed)))
                      for r in rows]
            prices = {r.get('marks') for r in rows}
            if max(shared) > 0:
                target = shared.index(max(shared))
            elif (all(r['kind'] == 'point' for r in rows) and len(prices) == 1
                    and all(m == next(iter(prices)) for _t, m in parsed)):
                # An alternative to any one of the answers: one menu of them all.
                price = next(iter(prices))
                note_ = next((r.get('contextNote') for r in rows if r.get('contextNote')), None)
                rows = [{'id': 'r-1', 'kind': 'anyN', 'verbatim': 'The answers the scheme accepts',
                         'marks': None, **({'contextNote': note_} if note_ else {}),
                         'group': {'claimMax': len(rows), 'perOption': price,
                                   'options': [r['verbatim'] for r in rows] + [t for t, _m in parsed]}}]
                continue
        row = rows[target]
        if row['kind'] == 'anyN':
            g = dict(row['group'])
            assert not g.get('perOptionSteps'), (ask, 'a partial beside a descending tariff')
            marks = g.get('optionMarks') or [g['perOption']] * len(g['options'])
            g['options'] = list(g['options']) + [t for t, _m in parsed]
            g['optionMarks'] = list(marks) + [m for _t, m in parsed]
            g['perOption'] = max(g['optionMarks'])
            row['group'] = g
        else:
            # A point, or one answer placed at its printed split ("Sunnier (day)
            # with clear (skies) (2+1m) [Sun = 2m]"): the one-pick group carries
            # the full answer and the printed partial, each at its price.
            assert row['kind'] in ('point', 'criterion') and not row.get('parts'), (ask, row)
            full = row['marks']
            assert all(m <= full for _t, m in parsed), (ask, parsed, full)
            rows[target] = {'id': row['id'], 'kind': 'anyN', 'verbatim': 'The answers the scheme accepts',
                            'marks': None, **({'contextNote': row['contextNote']} if row.get('contextNote') else {}),
                            'group': {'claimMax': 1, 'perOption': full,
                                      'options': [row['verbatim']] + [t for t, _m in parsed],
                                      'optionMarks': [full] + [m for _t, m in parsed]}}
    return rows


def _rows_core(ask, language, rule, stepped=False, skip_notes=()):
    """The card's marking rows, or None (a direction) or a refusal string."""
    note = language_note(language, rule)
    notes = [n for n in (ask.notes or []) if n not in skip_notes]
    if stepped or ask.bracket_parts:
        # A bracket that only states a price ("[2m]", "[1+1m]") is already on
        # the row as its marks; quoting it again says nothing.
        notes = [n for n in notes if not re.fullmatch(
            r'\s*\d{1,2}(?:\s*\+\s*\d{1,2})*\s*(?:m(?:arks?)?)?\s*', n, re.I)]
    if notes:
        note += (' The scheme adds: '
                 + '; '.join(f'“{n}”' for n in notes[:3]) + '.')
    if ask.total is None or not ask.terms:
        return None
    if stepped:
        parts = _round_components(ask)
        if parts:
            return _round_component_row(ask, parts, note)
    if ask.quota:
        if not ask.options:
            return None
        lead = list(ask.lead_points or [])
        terms = ask.terms[len(lead):]
        if stepped and len(terms) == 1 and ask.quota > 1:
            # "Three of: - accommodation - (qualified) instructor - … (3m)"
            # (2022 Higher listening Q1(c); 2023 Q4(c)): the scheme prices the
            # three answers together and prints no split. Paid at the printed
            # value only, when the third is claimed: never an inferred 1 + 1 + 1.
            terms = [0] * (ask.quota - 1) + terms
        if len(terms) != ask.quota:
            return ('the scheme asks for a number of answers its tariff does '
                    'not price')
        options = ask.options[:MAX_OPTIONS]
        if len(options) < ask.quota:
            return 'the scheme prices more answers than it states'
        group = {'claimMax': ask.quota, 'perOption': terms[0],
                 'options': options}
        if len(set(terms)) > 1:
            # A descending tariff — "[First correct answer=4m]" then 3 and 3 —
            # is paid step by step, and perOptionSteps is the field the
            # renderer and the tariff gate both read.
            group['perOptionSteps'] = list(terms)
        contextNote = note
        if len(ask.options) > MAX_OPTIONS:
            contextNote += (f' The scheme lists {len(ask.options) - MAX_OPTIONS} '
                            f'further accepted answer(s) beyond the ones shown.')
        # A required answer the scheme prices ahead of the menu is its own
        # claim row, never one of the menu's options.
        lead_rows = [{'id': f'r-{i}', 'kind': 'point', 'verbatim': text,
                      'marks': marks, **({'contextNote': note} if i == 1 else {})}
                     for i, (text, marks) in enumerate(lead, start=1)]
        return lead_rows + [{'id': f'r-{len(lead) + 1}', 'kind': 'anyN',
                 'verbatim': 'The answers the scheme accepts',
                 'marks': None,
                 **({'contextNote': contextNote} if not lead else {}),
                 'group': group}]
    if not ask.points:
        return None
    if any(DIRECTION_ONLY.match(text) for text, _m in ask.points):
        return None
    points = list(ask.points)
    # (A shipped card too: its printed component prices are claimable,
    # coordinator ruling of 12 Nov 2026 — 2025 Higher Q2(b)(ii).)
    if len(points) == 1 and ask.bracket_parts:
        # One answer priced in bracketed components: one row, each component
        # claimed on its own marks, the row scoring their sum.
        parts = [{'id': f'p{i}', 'verbatim': text, 'marks': marks,
                  'permittedMarks': [0, marks]}
                 for i, (text, marks) in enumerate(ask.bracket_parts, start=1)]
        sums = {0}
        for _t, m in ask.bracket_parts:
            sums |= {x + m for x in sums}
        # The row reads as its components do: 2018 Higher listening Q4(a)
        # prices "(i) Instagram has … [1m]" and "(ii) It is the most …
        # [2m]", and its numbering stays where the scheme prints it.
        return [{'id': 'r-1', 'kind': 'criterion',
                 'verbatim': ' '.join(t for t, _m in ask.bracket_parts),
                 'marks': ask.total, 'permittedMarks': sorted(sums),
                 'parts': parts, 'contextNote': note}]
    if stepped and len(points) == 1 and not ask.bracket_parts:
        parts = _bracketed(ask.raw, points[0][0], ask.total)
        if parts and not (len(ask.terms or []) > 1 and _separate_answers(points[0][0], len(ask.terms))):
            return [_component_row('r-1', points[0][0], ask.total, parts, note)]
    if stepped and len(points) == 1 and ask.terms and len(ask.terms) > 1:
        text = points[0][0]
        pieces = _separate_answers(text, len(ask.terms))
        if pieces:
            # Several answers on one printed line, each priced: "Water;
            # electricity; toilets; showers (1+1+1+1m)". The semicolons are
            # the scheme's own separators, so each answer is its own claim row.
            points = list(zip(pieces, ask.terms))
        else:
            # ONE answer whose marks the scheme splits: "In the last ten years
            # and especially during the pandemic (3+3m)". A student who had
            # half of it earns half, so the row is placed at the values the
            # scheme prints — 0, 3, 6 — never all-or-nothing, and never at a
            # value it does not print.
            steps = [0]
            for t in ask.terms:
                steps.append(steps[-1] + t)
            return [{'id': 'r-1', 'kind': 'criterion', 'verbatim': text,
                     'marks': ask.total, 'permittedMarks': steps,
                     'contextNote': note}]
    if len(points) > MAX_ROWS:
        return 'the scheme states more separate answers than one card may show'
    if sum(m or 0 for _t, m in points) != ask.total:
        return 'the scheme\'s answers do not add up to the tariff it prints'
    rows = []
    for i, (text, marks) in enumerate(points, start=1):
        parts = _bracketed(ask.raw, text, marks) if stepped and len(points) > 1 else None
        if parts:
            rows.append(_component_row(f'r-{i}', text, marks, parts,
                                       note if i == 1 else None))
            continue
        rows.append({'id': f'r-{i}', 'kind': 'point', 'verbatim': text, 'marks': marks,
                     **({'contextNote': note} if i == 1 else {})})
    return rows


# ---------------------------------------------------------------- report ----
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--report', action='store_true')
    ap.add_argument('--exclusions', action='store_true',
                    help='rewrite exclusions/spanish.json from the refusals')
    ap.add_argument('--all', action='store_true')
    args = ap.parse_args()
    cards, refused, examples, excluded = build()

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
        rows = sum(len(c['rows']) for c in cards)
        opts = sum(len(r['group']['options']) for c in cards for r in c['rows']
                   if r.get('group'))
        print(f'{rows} marking rows holding {opts} stated answer(s)')
        by_topic = collections.Counter(c['topicId'] for c in cards)
        for tid, n in sorted(by_topic.items()):
            print(f'   {tid:12} {n}')
        by_lang = collections.Counter(
            'Spanish' if 'answered in Spanish' in c['rows'][0].get('contextNote', '')
            else 'English' for c in cards)
        print(f'   answer language: {dict(by_lang)}')
        by_source = collections.Counter(
            (c.get('sourceMaterial') or {}).get('sourceLabel', 'question paper')
            for c in cards)
        print(f'   source booklet: {dict(by_source)}')
        for reason, n in refused.most_common():
            print(f'   {n:4} REFUSED  {reason}')
            for e in examples[reason][:40 if args.all else 3]:
                print(f'             {e}')
        return 0

    json.dump(cards, sys.stdout, ensure_ascii=False, indent=1)
    return 0


if __name__ == '__main__':
    sys.exit(main())
