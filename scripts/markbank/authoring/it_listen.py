#!/usr/bin/env python3
"""Italian listening: the Listening Comprehension Test as Mark Bank cards.

    python3 scripts/markbank/authoring/it_listen.py 2025 hl     # read one sitting

Every Italian recording 2010-2026 is in the SEC archive (SOURCES.md, 18 Nov 2026),
one file a year for both levels, bound from data/italianAudio.json. So every
printed listening ask is a card, scored on its own (review pack 1, treatment D):

  * its QUESTION is the booklet's English column: the right-hand column of the
    Irish/English booklet, read row by row (fr_paper._rows);
  * Section A is eight multiple-choice asks at 2 marks ("16 marks 8x2"). The
    booklet prints the four options; the scheme prints the same four and sets
    the right one in BOLD, which is the only place it says which one is right.
    The answer is read from the font of the scheme's own span, and a question
    whose scheme does not set exactly one option in bold is refused, never
    guessed;
  * Section B is three dialogues, priced in the same block grammar as the
    reading sections ("Any two of 4 marks (2+2)", bullets, the lesser answers
    under a row of tildes), so it_scheme reads them and it_all's row builder
    turns them into rows. Paper and scheme are paired on the dialogue and the
    ORDER inside it, under the check that both print the same number of asks.

Nothing here writes a question or an answer: questions are the booklet's, rows
the scheme's, and the stem is the booklet's own instruction for its section.
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
sys.path.insert(0, HERE)

import pymupdf                                                   # noqa: E402
from fr_paper import _rows                                       # noqa: E402
import it_paper as IP                                            # noqa: E402
from it_scheme import ItScheme, schemes_dir                      # noqa: E402
from it_rows import split_priced                                 # noqa: E402

AUDIO = os.path.join(ROOT, 'data', 'italianAudio.json')
SECTION_A_TOPIC = 'italian-3-1'      # Aural — News Items / Statements
DIALOGUE_TOPIC = 'italian-3-0'       # Aural — Conversations
LEVEL_WORD = {'hl': 'higher', 'ol': 'ordinary'}
LEVEL_TITLE = {'hl': 'Higher', 'ol': 'Ordinary'}
OPTION = re.compile(r'^\(\s*([a-e])\s*\)\s*(.*)$')
# The scheme's options: "(a) a house for sale" (2024-2026) or "a) a hotel" (2023).
KEY_OPTION = re.compile(r'^\(?\s*([a-e])\s*\)\s*(.*)$')
# "Dialogue 3." alone, or with its title on the same line ("Dialogue 3.
# Interview with Paola Lombardi", 2020 Higher).
DIALOGUE = re.compile(r'^Dialogue\s+(\d)\s*(?:\.\s*(.*))?$', re.I)


def recording(year):
    for row in json.load(open(AUDIO, encoding='utf-8')):
        if row['year'] == year:
            return dict(row['source'])
    return None


class Booklet:
    """The listening booklet's English column: Section A and the dialogues."""

    def __init__(self, year, level):
        self.year, self.level = year, level
        self.path = os.path.join(IP.papers_dir(), f'{year}-{level}-A00-paper.pdf')
        self.section_a = {}       # n -> {'stem', 'options': [(letter, text)], 'page'}
        self.dialogues = {}       # d -> {'title': str, 'asks': {n: {'text', 'page'}}}
        self.rubric = {'A': [], 'B': []}
        self._read()

    def _read(self):
        section = None
        dialogue = None
        cur = None                # the dict a continuation line extends
        width = IP.ItPaper._page_width(self.path)
        self.gap = {'A': False, 'B': False}
        for pno, groups in _rows(self.path):
            for _x, side, text in groups:
                s = IP._clean(text)
                if not s or IP.FURNITURE.match(s):
                    continue
                # The page footer "Iodáilis ‐ Ardleibhéal" and the back cover
                # "Higher level Italian Monday 24 June 12:10 – 12:50" (2021-
                # 2024): read after a question they would join its text.
                if re.match(r'^(?:Iodáilis\s*[‐\-–]\s*(?:Ard|Gnáth)leibh|(?:[‐\-–]\s*)?(?:Higher|Ordinary) level Italian\b)', s, re.I):
                    continue
                # The pages after the last dialogue (a notes page, a blank
                # page, the back cover) end the booklet: read on, their lines
                # would join the last question.
                if section == 'B' and dialogue == 3 and self.dialogues[3]['asks'] and re.match(
                        r'^(?:You may use this page|Leathanach Bán|Blank Page|Leaving Certificate Examination\s*[‐\-–]'
                        r'|Scrúdú na hArdteistiméireachta\s*[‐\-–]|(?:[‐\-–]\s*)?(?:Higher|Ordinary) level$)', s, re.I):
                    return
                # A row the column finder could not split reads as 'L'; the
                # English column is the right half of the sheet.
                if _x >= 0.45 * width:
                    side = 'R'
                if side != 'R':
                    # "Comhrá 2. Dialogue 2." welded into one group (2018,
                    # 2020 Higher): the English head still opens the dialogue.
                    wd = re.search(r'\bDialogue\s+(\d)\s*\.', s)
                    if wd and section == 'B':
                        dialogue = int(wd.group(1))
                        self.dialogues[dialogue] = {'title': [], 'asks': {}}
                        cur = self.dialogues[dialogue]['title']
                        continue
                    # The English number welded onto the END of the Irish line
                    # beside it — 2021 Higher Dialogue 1 prints "Luaigh dhá
                    # ghníomhaíocht atá sé i gceist 4." with the English
                    # question, without its "4.", on the right: the number
                    # opens that question.
                    tail = re.search(r'\s(\d{1,2})\s*\.\s*$', s)
                    # The same in Section A (2018 Ordinary 6. and 8.).
                    if tail and section == 'A' and int(tail.group(1)) == max(self.section_a or [0]) + 1:
                        n = int(tail.group(1))
                        self.section_a[n] = {'stem': [], 'options': [], 'page': pno + 1}
                        cur = self.section_a[n]['stem']
                        continue
                    if tail and section == 'B' and dialogue is not None:
                        n = int(tail.group(1))
                        if n == max(self.dialogues[dialogue]['asks'] or [0]) + 1:
                            ask = {'text': [], 'page': pno + 1}
                            self.dialogues[dialogue]['asks'][n] = ask
                            cur = ask['text']
                            continue
                    # An Irish line welded to the English beside it ("… cuir
                    # ciorcal what you consider the most appropriate") hides an
                    # English line: the section's instruction is cut before it.
                    if section in ('A', 'B') and re.search(r'\b(?:what|the|you|each|will|answer)\b', s):
                        if (section == 'A' and not self.section_a) or (section == 'B' and dialogue is None):
                            self.gap[section] = True
                    continue
                if re.fullmatch(r'SECTION\s+A', s):
                    section, cur = 'A', None
                    continue
                if re.fullmatch(r'SECTION\s+B', s):
                    section, cur = 'B', None
                    continue
                m = DIALOGUE.match(s)
                if m and section == 'B':
                    dialogue = int(m.group(1))
                    self.dialogues[dialogue] = {'title': [m.group(2)] if m.group(2) else [], 'asks': {}}
                    cur = self.dialogues[dialogue]['title']
                    continue
                m = IP.NUM_MARK.match(s)
                if m and section == 'A':
                    n = int(m.group(1))
                    self.section_a[n] = {'stem': [m.group(3).strip()],
                                         'options': [], 'page': pno + 1}
                    cur = self.section_a[n]['stem']
                    continue
                if m and section == 'B' and dialogue is not None:
                    n = int(m.group(1))
                    ask = {'text': [m.group(3).strip()], 'page': pno + 1}
                    self.dialogues[dialogue]['asks'][n] = ask
                    cur = ask['text']
                    continue
                m = OPTION.match(s)
                if m and section == 'A' and self.section_a:
                    q = self.section_a[max(self.section_a)]
                    q['options'].append([m.group(1), m.group(2).strip()])
                    cur = q['options'][-1]
                    continue
                if section in ('A', 'B') and not self.section_a and section == 'A':
                    if not self.gap['A']:
                        self.rubric['A'].append(s)
                    continue
                if section == 'B' and dialogue is None:
                    if not self.gap['B']:
                        self.rubric['B'].append(s)
                    continue
                if cur is None:
                    continue
                if isinstance(cur, list) and len(cur) == 2 and isinstance(cur[0], str) \
                        and len(cur[0]) == 1:
                    cur[1] = f'{cur[1]} {s}'.strip()
                else:
                    cur.append(s)


def _join(spans):
    """A row's text: spans in reading order, a space between two spans unless
    the second abuts the first ("A" + "n earthquake", 2018 Higher)."""
    out, prev = '', None
    for sp in sorted(spans, key=lambda sp: sp['bbox'][0]):
        t = sp['text'].strip()
        if prev is not None:
            out += '' if sp['bbox'][0] - prev['bbox'][2] < 0.6 and not sp['text'][:1].isspace() \
                and not prev['text'][-1:].isspace() else ' '
        out += t
        prev = sp
    return out


def section_a_key(year, level):
    """(marks a question, {question: (letter, scheme words or None)}) for Section A.

    The two levels print the key two ways. Ordinary prints the letter alone —
    "1. (a)", "2. (a)" — under "Section A 24 marks (8x3)". Higher reprints each
    question and its four options and sets the right one in BOLD under "16
    marks (8x2)"; the bold is in the span's own font name ("Calibri,Bold").
    A question with no letter and not exactly one bold option is left out of
    the key, and its card is refused.
    """
    path = os.path.join(schemes_dir(), f'{year}-{level}.pdf')
    key, bold, per = {}, {}, None
    q = None
    started = False
    with pymupdf.open(path) as doc:
        for page in doc:
            # An option's letter may be a line of its own with its words on
            # the same baseline as the next line ("(a)" and "The North", 2018
            # Higher): that pair is one row. Nothing else is joined.
            rows = []
            for block in page.get_text('dict')['blocks']:
                for line in block.get('lines', []):
                    spans = [sp for sp in line['spans'] if sp['text'].strip()]
                    if not spans:
                        continue
                    y = round(line['bbox'][3], 1)
                    if (rows and abs(rows[-1][0] - y) < 2
                            and re.fullmatch(r'\(\s*[a-e]\s*\)', _join(rows[-1][1]))):
                        rows[-1][1].extend(spans)
                    else:
                        rows.append([y, spans])
            for _y, spans in rows:
                    text = _join(spans)
                    if not started:
                        started = bool(re.match(r'LISTENING\s+COMPREHENSION', text, re.I))
                        if not started:
                            continue
                    m = re.search(r'8\s*[xX×]\s*(\d)', text)
                    if m and per is None:
                        per = int(m.group(1))
                    if re.match(r'(?:SECTION|Section)\s+B\b', text):
                        for n, found in bold.items():
                            if len(found) == 1 and n not in key:
                                key[n] = found[0]
                        return per, key
                    m = re.match(r'^(\d)\s*\.\s*(.*)$', text)
                    if m:
                        q = int(m.group(1))
                        lone = re.fullmatch(r'\(\s*([a-e])\s*\)', m.group(2).strip())
                        if lone:
                            key[q] = (lone.group(1), None)
                        continue
                    m = KEY_OPTION.match(text)
                    if m and q is not None:
                        body = [sp for sp in spans
                                if not re.fullmatch(r'\(?\s*[a-e]\s*\)', sp['text'].strip())]
                        # The option's words are bold: wholly, or a word set
                        # bold after its first letter ("A" + "n earthquake",
                        # 2018 Higher) - most of the words' letters bold.
                        nb = sum(len(sp['text'].strip()) for sp in body if 'Bold' in sp['font'])
                        nall = sum(len(sp['text'].strip()) for sp in body)
                        if body and nb * 2 > nall:
                            bold.setdefault(q, []).append(
                                (m.group(1), ' '.join(m.group(2).split())))
    return per, key


def scheme_dialogues(year, level):
    """{dialogue: [scheme Ask, …]} read with the reading sections' grammar."""
    S = ItScheme(year, level)
    saved = S.asks
    S.asks = []
    for token, unit, start, end, _total in S._sections():
        if token in ('LB1', 'LB2', 'LB3'):
            S._read_asks(token, unit, start + 1, end, S._split_on(start))
    found = {}
    for a in S.asks:
        found.setdefault(int(a.section[2]), []).append(a)
    S.asks = saved
    return S, found


ELEMENTS = re.compile(r'\belements?\b', re.I)
BULLET = re.compile(r'^[•●▪■]\s*')


def _flat(text):
    return ' '.join(text.split())


def _scheme_text(S):
    return _flat(' '.join(S.lines))


def _repair_bullets(S, ask):
    """Bulleted answers the reader filed as lesser answers.

    A listening ask may print its full answers as bullets each carrying its own
    value — "Any two of 4 marks" over "• It is an initiative for bike lovers
    (2)" — and a line ending in ONE bracketed mark reads, in the reading
    grammar, as a lesser answer worth that. A BULLETED line worth exactly what
    one answer of the directive is worth is a full answer; its words are taken
    from the scheme line itself, with only the trailing "(2)" removed.
    """
    for part in ask.parts:
        if part.claim is None or not part.total or part.total % part.claim:
            continue
        each = part.total // part.claim
        keep, moved = [], []
        for text, value in part.rungs:
            if BULLET.match(text) and value == each:
                line = next((l.strip() for l in S.lines
                             if _flat(l).startswith(_flat(text))), None)
                body = re.sub(r'\s*\(\s*\d\s*\)\s*$', '', line or text)
                moved.append(BULLET.sub('', body).strip())
            else:
                keep.append((text, value))
        if moved:
            def at(a):
                return next((i for i, l in enumerate(S.lines)
                             if _flat(BULLET.sub('', l.strip())).startswith(_flat(a)[:30])), 10**6)
            part.answers = sorted(list(part.answers) + moved, key=at)
            part.rungs = keep


def _ladder_rows(S, ask):
    """An answer the scheme scores by HOW MANY of its elements are given.

    "1 to 2 elements = 2 marks / 3 elements 3 marks / 4 elements 4 marks / 5
    elements 6 marks" under one stated answer: the scheme prices the answer by
    a ladder it does not cut into rows. The card shows the stated answer(s) as
    criteria and the ladder verbatim, and is self-assessed against the printed
    total (`questionTotal`, CARD-STANDARD section 2).
    """
    part = ask.parts[0]
    if not any(ELEMENTS.search(t) for t, _v in part.rungs) and \
            not any(ELEMENTS.search(a) for a in part.answers):
        return None
    answers = [a for a in part.answers if not ELEMENTS.search(a)]
    ladder = [_flat(l) for l in S.lines if ELEMENTS.search(l)
              and re.search(r'\d\s*(?:to\s*\d\s*)?elements?', l)]
    # the ladder lines that belong to THIS ask: the first run after its answers
    start = next((i for i, l in enumerate(S.lines) if answers
                  and _flat(BULLET.sub('', l.strip())).startswith(_flat(answers[-1])[:40])),
                 None)
    run = []
    if start is not None:
        for l in S.lines[start + 1:start + 12]:
            if ELEMENTS.search(l):
                run.append(_flat(l))
            elif run:
                break
    rows = [{'id': f'r-{k}', 'kind': 'criterion', 'verbatim': a, 'marks': None}
            for k, a in enumerate(answers, start=1)]
    if not rows or not run:
        return None
    rows[0]['contextNote'] = ('The scheme gives marks for this answer by how many of '
                              'its elements are given: ' + '; '.join(run) + '.')
    return rows


def _sentences(text):
    """The instruction up to its last full stop: never a sentence cut short."""
    text = ' '.join(text.split())
    end = text.rfind('.')
    return text[:end + 1] if end > 0 else ''


def cards(year, level, refuse, row_for, concept_for):
    """Every listening card for one sitting; refusals go to `refuse`."""
    B = Booklet(year, level)
    audio = recording(year)
    out = []
    lvl = level.upper()
    title = LEVEL_TITLE[level]
    if audio is None:
        for n in sorted(B.section_a):
            refuse('no recording is bound for this year', f'{year} {lvl} Section LA Q{n}')
        return out

    def source(section_word, n, page):
        return {
            'kind': 'source-text', 'label': 'LISTENING COMPREHENSION TEST',
            'title': f'{section_word} — Question {n}', 'pages': [page],
            'sourceLabel': 'Aural Paper',
            'attribution': (f'SEC Italian {year} {title} Level Listening '
                            'Comprehension Test — © State Examinations Commission.'),
            'presentationNote': ('The question page of the listening booklet. '
                                 'Play the recording, then answer.'),
        }

    def audio_for(label):
        a = dict(audio)
        a['label'] = f'{label} · listening'
        return a

    per, key = section_a_key(year, level)
    # The Section A instruction's last sentence ("Choose what you consider the
    # most appropriate answer to each question below and indicate your choice
    # by circling …") loses a printed line in the booklet's text layer in
    # every 2025-2026 booklet, so the stem stops before it: what is shown is
    # complete and the paper's own.
    stem_a = _sentences(' '.join(B.rubric['A']).split(' Choose ')[0])
    for n in sorted(B.section_a):
        q = B.section_a[n]
        ref = f'{year} {lvl} Section LA Q{n}'
        if n not in key or per is None:
            refuse('the scheme does not print which option of this multiple choice '
                   'it accepts in a form this reads (a letter, or one option in bold)',
                   ref, f'{year} {lvl} scheme, Section A Q{n}')
            continue
        letter, answer = key[n]
        options = [' '.join(t.split()) for _l, t in q['options']]
        printed = dict((l, ' '.join(t.split())) for l, t in q['options'])
        letter_only = answer is None
        if letter_only:
            # Ordinary prints the key as the letter alone, "1. (a)": that line is
            # the scheme's whole answer, and the row is that line. The option's
            # words are the booklet's and are on the card as its choices.
            if letter not in printed:
                refuse('the scheme accepts a letter the booklet does not print',
                       ref, f'{year} {lvl} scheme, Section A Q{n}: ({letter})')
                continue
            answer = f'{n}. ({letter})'
        out.append({
            'id': f'it-{year}-{level}-la-{n}',
            'subjectId': 'italian', 'level': LEVEL_WORD[level], 'year': year,
            'section': 'L', 'topicId': SECTION_A_TOPIC,
            'conceptId': concept_for(' '.join(q['stem']) + ' ' + answer),
            'questionRef': ref,
            'questionText': ' '.join(' '.join(q['stem']).split()) + ''.join(
                f'\n({l}) {" ".join(t.split())}' for l, t in q['options']),
            'questionChoices': options,
            'tariffModel': {'kind': 'fixed'}, 'totalMarks': per,
            'rows': [{'id': 'r-1', 'kind': 'point', 'verbatim': answer, 'marks': per,
                      'contextNote': (f'The scheme accepts option ({letter}) only.' if letter_only
                                      else 'The scheme sets the right option in bold: '
                                      f'({letter}).')}],
            'notes': (f'The scheme prices Section A "8x{per}": {per} marks a question; '
                      f'the listening booklet prints this ask on page {q["page"]}.'),
            'stem': stem_a,
            'sourceMaterial': source('Section A', n, q['page']),
            'audioMaterial': audio_for('Section A'),
        })

    S, scheme = scheme_dialogues(year, level)
    stem_b = _sentences(' '.join(B.rubric['B']))
    for d in sorted(B.dialogues):
        asks = B.dialogues[d]['asks']
        priced = scheme.get(d, [])
        head = ' '.join(B.dialogues[d]['title'])
        by_item = {a.item: a for a in priced}
        missing = [n for n in sorted(asks) if n not in by_item]
        if len(asks) < len(priced):
            for n in sorted(by_item):
                refuse('the booklet prints fewer asks in this dialogue than the scheme '
                       'prices, so the booklet reader lost one', f'{year} {lvl} Section LB{d} Q{n}',
                       f'paper {len(asks)}, scheme {len(priced)}')
            continue
        if len(asks) != len(priced) and not all(
                (year, level, d, n) in OVERRIDES and 'total' in OVERRIDES[(year, level, d, n)]
                for n in missing):
            for n in sorted(asks):
                refuse('the booklet and the scheme print a different number of asks '
                       'in this dialogue, so they cannot be paired by order',
                       f'{year} {lvl} Section LB{d} Q{n}',
                       f'paper {len(asks)}, scheme {len(priced)}')
            continue
        # Equal counts pair in printed order; where the reader lost a scheme
        # ask its number is supplied by an OVERRIDES entry (with its printed
        # total) and every other ask pairs on its own printed number.
        pairs = (list(zip(sorted(asks), priced)) if len(asks) == len(priced)
                 else [(n, by_item.get(n)) for n in sorted(asks)])
        for n, ask in pairs:
            ref = f'{year} {lvl} Section LB{d} Q{n}'
            text = ' '.join(' '.join(asks[n]['text']).split())
            if ask is None:
                o = OVERRIDES[(year, level, d, n)]
                ask = type('Lost', (), {'total': o['total'], 'fault': None, 'parts': [],
                                        'item': n})()
            if ask.total is None or ask.fault:
                refuse('the scheme prints no tariff this reads for the ask', ref,
                       f'{year} {lvl} scheme, Dialogue {d} ask {ask.item}')
                continue
            override = OVERRIDES.get((year, level, d, n))
            if ask.parts:
                _repair_bullets(S, ask)
            ladder = None if (override or not ask.parts) else _ladder_rows(S, ask)
            tariff = {'kind': 'fixed'}
            rows = []
            bad = None
            part0 = ask.parts[0] if ask.parts else None
            components = (part0 is not None and len(ask.parts) == 1 and not part0.directive and part0.split
                          and len(part0.split) == len(part0.answers) > 1
                          and sum(part0.split) == ask.total)
            if override:
                rows = _override_rows(S, override, ref)
            elif components:
                # "7 marks (1+1+2+3)" over four bullets: ONE answer the scheme
                # cuts into four printed components, each worth its term.
                rows = [{'id': f'r-{k}', 'kind': 'point', 'verbatim': a, 'marks': m}
                        for k, (a, m) in enumerate(zip(part0.answers, part0.split), start=1)]
            elif ladder:
                rows, tariff = ladder, {'kind': 'questionTotal'}
            for k, part in enumerate([] if (override or ladder or components)
                                     else ask.parts, start=1):
                row = row_for(part, k, ask)
                if isinstance(row, str):
                    bad = row
                    break
                row.pop('_trimmed', None)
                rows.append(row)
            if bad:
                refuse(bad, ref, f'{year} {lvl} scheme, Dialogue {d} ask {ask.item}: '
                                 f'{ask.parts[0].notation!r}')
                continue
            rows[0]['contextNote'] = (rows[0].get('contextNote', '') +
                                      ' Answer in English or Irish.').strip()
            out.append({
                'id': f'it-{year}-{level}-lb{d}-{n}',
                'subjectId': 'italian', 'level': LEVEL_WORD[level], 'year': year,
                'section': 'L', 'topicId': DIALOGUE_TOPIC,
                'conceptId': concept_for(text),
                'questionRef': ref, 'questionText': text,
                'tariffModel': tariff, 'totalMarks': ask.total,
                'rows': rows,
                'notes': (f'The scheme prints the tariff as '
                          f'{"; ".join(p.notation for p in ask.parts) or str(ask.total) + " marks"!r}; the '
                          f'listening booklet prints this ask on page {asks[n]["page"]}.'),
                'stem': f'Dialogue {d}. {head}. {stem_b}'.replace('..', '.'),
                'sourceMaterial': source(f'Dialogue {d}', n, asks[n]['page']),
                'audioMaterial': audio_for(f'Dialogue {d}'),
            })
    return [split_priced(c) for c in out]


# Asks whose answer the scheme prints ON its head line, wrapped across two
# lines, so the reading grammar (which takes what precedes the first tariff as
# a directive) cannot see it. Each option is a cut of the scheme's own line,
# checked present in the scheme before it is used, never typed.
OVERRIDES = {
    # "1. (Last) May 4 marks", the first line under the Dialogue 3 head, lost
    # by the reader.
    (2022, 'ol', 3, 1): {'total': 4, 'points': [('(Last) May', 4)]},
    # "8. Go to the mountains (4) 6 marks" then "Any two of" three bullets at (1).
    (2022, 'hl', 3, 8): {'rows': [
        {'kind': 'point', 'verbatim': 'Go to the mountains', 'marks': 4},
        {'kind': 'anyN', 'verbatim': 'The answers the scheme accepts in full', 'marks': None,
         'group': {'claimMax': 2, 'perOption': 1, 'options': [
             'Rest/Relax/Spend few days- some time', 'To see different/new landscapes',
             'Take a break/from the sea']},
         'contextNote': 'Any two of'}]},
    # Asks the reading grammar loses at a page foot or under a wrapped answer;
    # each carries its printed total, and its rows are cuts of the scheme.
    (2024, 'ol', 1, 4): {'total': 4, 'points': [('(Only) this morning', 4)],
                         'note': ['(After her dentist’s appointment 2 marks)']},
    (2023, 'ol', 3, 5): {'total': 4, 'points': [
        ('(Around) 7 pm/The Italians finish work late (Later than the Irish)', 4)],
        'note': ['(In the evening 1 mark)']},
    # "Under 15 and (3) over 60 (3) years of age": two components priced
    # inside one line, the line's last words after the second price.
    (2025, 'hl', 3, 4): {'points': [('Under 15', 3), ('over 60', 3)],
                         'note': ['Under 15 and (3) over 60 (3) years of age']},
    # "(Many) language schools (1) universities (1) have decided to use her
    # app (in their courses)" with its third "(1)" on a line of its own.
    (2026, 'hl', 2, 4): {'points': [('(Many) language schools', 1), ('universities', 1),
                                    ('have decided to use her app (in their courses)', 1)]},
    (2026, 'ol', 1, 1): {
        'claimMax': 2, 'perOption': 4,
        'options': ['Emotional/nervous', 'a little nervous/excited', 'worried'],
        'note': ['(any two elements)', '(If just one emotion is given and if another reason also given – allow an additional 1 mark only. Reasons - It’s the first time /Living together (is not easy)/(Facing) other people’s habits/ Language barriers)']},
    # "4 marks" printed on the line ABOVE "8. His family (1) for at least
    # (1m) two (1) weeks(1) (1+1+1+1)", so the reader never prices the ask.
    (2018, 'hl', 3, 8): {'total': 4, 'points': [('His family', 1), ('for at least', 1),
                                                ('two', 1), ('weeks', 1)],
                         'note': ['His family (1) for at least (1m) two (1) weeks(1) (1+1+1+1)']},
    (2026, 'ol', 2, 4): {
        'claimMax': 4, 'perOption': 2,
        'options': ['A (prizewinning) app', 'to practice/learn', 'their verbs',
                    'in (the) Italian (language)', 'interactively/with exercises'],
        'note': ['Any four of these five points']},
}


def _override_rows(S, o, ref):
    text = _scheme_text(S)
    if 'rows' in o:
        for row in o['rows']:
            for piece in [row.get('verbatim')] + (row.get('group') or {}).get('options', []):
                if piece and piece != 'The answers the scheme accepts in full':
                    assert _flat(piece) in text, f'{ref}: {piece!r} is not in the scheme'
        return [dict(r, id=f'r-{k}') for k, r in enumerate(o['rows'], start=1)]
    for piece in o.get('options', []) + o.get('note', []) + [p for p, _m in o.get('points', [])]:
        assert _flat(piece) in text, f'{ref}: {piece!r} is not in the scheme'
    if 'points' in o:
        rows = [{'id': f'r-{k}', 'kind': 'point', 'verbatim': p, 'marks': m}
                for k, (p, m) in enumerate(o['points'], start=1)]
        if o.get('note'):
            rows[0]['contextNote'] = ' '.join(o['note'])
        return rows
    return [{'id': 'r-1', 'kind': 'anyN',
             'verbatim': 'The answers the scheme accepts in full', 'marks': None,
             'group': {'claimMax': o['claimMax'], 'perOption': o['perOption'],
                       'options': o['options']},
             'contextNote': ' '.join(o['note'])}]


def main():
    year, level = int(sys.argv[1]), sys.argv[2]
    B = Booklet(year, level)
    print('Section A rubric:', ' '.join(B.rubric['A'])[:120])
    for n, q in sorted(B.section_a.items()):
        print(f'  A{n} p{q["page"]} {" ".join(q["stem"])!r} {[o[0] for o in q["options"]]}')
    print('key:', section_a_key(year, level))
    for d, v in sorted(B.dialogues.items()):
        print(f'  Dialogue {d}: {" ".join(v["title"])!r} asks {sorted(v["asks"])}')
    _S, sch = scheme_dialogues(year, level)
    print('scheme dialogues:', {d: [(a.item, a.total) for a in v] for d, v in sch.items()})


if __name__ == '__main__':
    main()
