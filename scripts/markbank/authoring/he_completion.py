#!/usr/bin/env python3
"""Complete the paper-census gaps in Home Economics.

The 2016-2020 schemes reprint each paper ask immediately before its marking
content.  This module joins those two independent documents by a run of six
words, then lifts answer rows only from the scheme block which follows the
matched ask.  It never manufactures answer wording.

The target set is deliberately count-pinned.  Older sittings were absent from
the original authoring pass; the short list after 2020 is the reviewed set of
gaps left by the existing scripts.  A paper-parser change therefore stops this
script instead of silently changing the deck it owns.
"""
from __future__ import annotations

import itertools
import json
import os
import re
import subprocess
import sys
import unicodedata
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from paper_census import ROMANS, census_sections, key_label, leaves_of  # noqa: E402


DIR = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(DIR)))
VERIFY = os.path.join(DIR, 'verify-claims.mjs')

# Every paper leaf in these sittings is a completion target.  The counts are
# the visual-paper-sweep ratchet: recover_heads=True restored the numbered asks
# which the flat PDF blocks had hidden, and these numbers must not drift.
OLDER_COUNTS = {
    (2016, 'hl'): 51, (2016, 'ol'): 49,
    # 2017 HL is 48: a room number inside the Q1(a) bungalow plan used to be
    # counted as a phantom ``Q2``, leaving the three real roman tasks under it.
    (2017, 'hl'): 48, (2017, 'ol'): 51,
    (2018, 'hl'): 49, (2018, 'ol'): 53,
    (2019, 'hl'): 51, (2019, 'ol'): 53,
    (2020, 'hl'): 49, (2020, 'ol'): 53,
}

# These are the census gaps left by the existing 2021-2025 scripts at the time
# of the completion sweep.  They are addresses, not inferred from the current
# deck, so rebuilding remains deterministic after the authored file changes.
RECENT_TARGETS = {
    (2021, 'hl'): {'Section B Q2(a)', 'Section B Q3(b)'},
    (2021, 'ol'): {'Section A Q14', 'Section B Q1(a)', 'Section B Q2(b)',
                   'Section B Q3(a)'},
    (2022, 'ol'): {'Section A Q14', 'Section B Q1(a)', 'Section B Q2(a)',
                   'Section B Q2(b)', 'Section B Q3(a)'},
    (2023, 'hl'): {'Section B Q2(b)', 'Section B Q3(b)',
                   'Section C Q2(c)(ii)'},
    (2023, 'ol'): {'Section A Q14', 'Section B Q1(a)', 'Section B Q2(a)',
                   'Section B Q2(b)'},
    (2024, 'hl'): {'Section B Q1(d)', 'Section B Q4(b)'},
    (2024, 'ol'): {'Section B Q2(a)', 'Section B Q2(b)'},
    (2025, 'hl'): {'Section B Q2(c)'},
    (2025, 'ol'): {'Section A Q14', 'Section B Q1(a)', 'Section B Q2(a)',
                   'Section B Q2(b)'},
}

# These roman asks are printed under one parent total and the scheme marks the
# pair on that shared scale.  A parent card is the honest boundary: it keeps the
# related asks together and reconcile.py deliberately lets that shallow
# citation cover the printed children beneath it.
COMBINED_TOTALS = {
    (2016, 'ol', 'B', 3, 'b'): 20,
    (2017, 'ol', 'B', 3, 'b'): 16,
    (2018, 'ol', 'B', 2, 'a'): 20,
    (2019, 'hl', 'B', 2, 'b'): 20,
    (2019, 'ol', 'B', 2, 'c'): 12,
    (2019, 'ol', 'B', 3, 'b'): 18,
    (2019, 'ol', 'B', 4, 'b'): 20,
    (2020, 'ol', 'B', 2, 'a'): 16,
    (2020, 'ol', 'B', 5, 'a'): 25,
}

# A handful of schemes communicate the answer through ticks, a compact table,
# or drawing criteria.  The flat semicolon parser quite rightly finds no prose
# list there.  These rows are still copied from the official scheme text; the
# truth-value notes record the visually inspected tick column and are not
# presented as purported verbatim scheme wording.
MANUAL_ROWS = {
    (2016, 'hl', 'C', 2, 'a', 'ii'): [
        {'verbatim': 'Sketch = 5 marks, Design = 4 marks'},
    ],
    (2018, 'ol', 'A', 1, None, None): [
        {'verbatim': 'Iron is essential for the manufacture of haemoglobin in the blood.',
         'contextNote': 'TRUE — the official scheme ticks the True column.'},
        {'verbatim': 'Anaemia is caused by lack of iron in the diet.',
         'contextNote': 'TRUE — the official scheme ticks the True column.'},
        {'verbatim': 'A diet rich in fibre assists the absorption of iron.',
         'contextNote': 'FALSE — the official scheme ticks the False column.'},
    ],
    (2018, 'ol', 'A', 7, None, None): [
        {'verbatim': 'Sugar is used as a preservative when making jam.',
         'contextNote': 'TRUE — the official scheme ticks the True column.'},
        {'verbatim': 'Quick freezing results in the formation of large ice crystals within the food cell.',
         'contextNote': 'FALSE — the official scheme ticks the False column.'},
        {'verbatim': 'Chutney is made by boiling fruit and / or vegetables with sugar, vinegar and spices.',
         'contextNote': 'TRUE — the official scheme ticks the True column.'},
    ],
    (2019, 'hl', 'C', 2, 'a', 'ii'): [
        {'verbatim': 'Sketch: 4 marks (graded 4:2:0)'},
        {'verbatim': 'Description: 6 marks (graded 6:4:2:0)'},
    ],
    (2020, 'hl', 'A', 4, None, None): [
        {'verbatim': 'Poor blood clotting Vitamin K, Vitamin C, Vitamin D,'},
        {'verbatim': 'Neural tube defects Vitamin B (folate), Vitamin B12,'},
        {'verbatim': 'Night blindness Vitamin A.'},
    ],
    (2020, 'hl', 'C', 2, 'a', 'i'): [
        {'verbatim': 'Sketch: 4 marks (graded 4:3:2:1:0)'},
        {'verbatim': 'Description: 6 marks (graded 6:4:2:0)'},
    ],
    (2020, 'ol', 'B', 2, 'c', None): [
        {'verbatim': 'Breakfast Lunch Dinner Orange juice Carrot and Lentil soup with Melon *** brown bread *** Porridge with low fat milk *** Vegetable stir fry with *** Low fat strawberry yoghurt brown rice Low fat fruit smoothie *** *** Tea/coffee/water Apple Fresh fruit salad Glass of low fat milk Low fat milk/water'},
    ],
    (2023, 'ol', 'A', 14, None, None): [
        {'verbatim': 'drip dry',
         'contextNote': 'The first printed care symbol.'},
        {'verbatim': 'do not tumble dry',
         'contextNote': 'The second printed care symbol.'},
    ],
}

QUESTION_FIGURES = {
    (2016, 'ol', 'B', 1, 'a', None):
        'home-economics-2016-ol-paper-p06-art',
    (2016, 'ol', 'C', 2, 'a', 'i'):
        'home-economics-2016-ol-paper-p10-art',
    (2017, 'hl', 'A', 8, None, None):
        'home-economics-2017-hl-paper-p04-art',
    (2017, 'hl', 'C', 2, 'a', 'i'):
        'home-economics-2017-hl-paper-p10-art',
    (2017, 'ol', 'C', 2, 'a', 'i'):
        'home-economics-2017-ol-paper-p10-art',
    (2018, 'hl', 'A', 1, None, None):
        'home-economics-2018-hl-paper-p02-art',
    (2018, 'hl', 'A', 6, None, None):
        'home-economics-2018-hl-paper-p03-art',
    (2018, 'ol', 'A', 11, None, None):
        'home-economics-2018-ol-paper-p05-art',
    (2018, 'ol', 'B', 1, 'a', 'i'):
        'home-economics-2018-ol-paper-p06-art',
    (2018, 'ol', 'C', 1, 'a', 'i'):
        'home-economics-2018-ol-paper-p09-art',
    (2018, 'ol', 'C', 2, 'a', 'i'):
        'home-economics-2018-ol-paper-p10-art',
    (2019, 'hl', 'B', 1, 'a', None):
        'home-economics-2019-hl-paper-p06-art',
    (2019, 'ol', 'C', 2, 'a', 'i'):
        'home-economics-2019-ol-paper-p10-art',
    (2020, 'ol', 'C', 2, 'a', 'i'):
        'home-economics-2020-ol-paper-p06-art',
    (2022, 'ol', 'B', 1, 'a', None):
        'home-economics-2022-ol-paper-p02-art',
    (2023, 'ol', 'B', 1, 'a', None):
        'home-economics-2023-ol-paper-p02-art',
    (2023, 'ol', 'A', 14, None, None):
        'home-economics-2023-ol-answerbook-p07-art',
    (2025, 'ol', 'B', 1, 'a', None):
        'home-economics-2025-ol-paper-p02-art',
}

DIAGRAM_FIGURES = {
    (2016, 'hl', 'A', 7, None, None): {
        'figureKey': 'home-economics-2016-hl-paper-p04-art',
        'labelKey': [
            {'letter': 'A', 'meaning': 'vacuole',
             'askedInThisQuestion': True},
            {'letter': 'B', 'meaning': 'nucleus',
             'askedInThisQuestion': True},
            {'letter': 'C',
             'meaning': 'granular cytoplasm / food vacuole / food reserve',
             'askedInThisQuestion': True},
        ],
    },
}

TOKEN = re.compile(r"[^\W_]+(?:['’][^\W_]+)?", re.UNICODE)
SECTION_HEAD = r'^Section {section}(?:\s+\d+\s+(?:or\s+\d+\s+)?marks)?\s*$'
TOTAL = re.compile(r'(?:⟨)?\((\d{1,2})\s*(?:marks?)?\)(?:⟩)?', re.I)
PAGE = re.compile(r'^##\s*Page\s*\d+\s*$', re.I)
TRAILING_ETC = re.compile(r'[,;:\s]*(?:etc\.?|or\s+any\s+other\s+valid\s+answer)\s*$', re.I)
TARIFF_ONLY = re.compile(
    r'^(?:\d+\s*(?:points?|functions?|factors?|ways?|reasons?|examples?|'
    r'guidelines?|items?|types?|methods?|advantages?|disadvantages?|classes?|'
    r'sources?|meals?|menus?|foods?|products?|vitamins?|marks?)?'
    r'(?:\s*\([^)]*\))?\s*'
    r'(?:@|x|×)\s*\d+\s*marks?(?:\s+each)?'
    r'|\d+\s+marks?(?:\s+each)?'
    r'|(?:name|description|account|example|reason|function)\s*:\s*\d+\s*marks?'
    r')(?:\s*\([^)]*graded[^)]*\))?(?:\s*[,;+].*)?$', re.I)
TARIFF_PREFIX = re.compile(
    r'^(?:(?:\d+\s*(?:points?|functions?|factors?|ways?|reasons?|examples?|'
    r'guidelines?|items?|types?|methods?|advantages?|disadvantages?|classes?|'
    r'sources?|meals?|menus?|vitamins?|foods?|products?)?'
    r'(?:\s*\([^)]*\))?\s*(?:@|x|×)\s*\d+\s*marks?'
    r'(?:\s+each)?(?:\s*\([^)]*\))?[,.:;\s]*)+)', re.I)
QUESTIONISH = re.compile(
    r'^(?:\(?[a-zivx]+\)?\s*)?(?:state|explain|outline|describe|discuss|name|'
    r'identify|evaluate|comment|compare|differentiate|suggest|give|list|write|'
    r'complete|indicate|what|how|why|using|with reference|in relation)\b', re.I)
FURNITURE = re.compile(
    r'^(?:Leaving Certificate|Home Economics|Section\s+[A-C]|Elective\s+\d|'
    r'Question\s+\d|Answer\s+(?:any|question)|Candidates?\b|Write your answer|'
    r'Accept\b|Grading\s+Table|Annotations?\b)', re.I)
CONTENT_FREE = re.compile(
    r'^(?:name|account|description|function|example|reason|advantage|disadvantage|'
    r'cause|effect|method|type|class|source|factor|guideline)s?\s*:?[\s.]*$', re.I)
BARE_ENUMERATOR = re.compile(r'^[\d()ivxlcdm.\s–—-]+$', re.I)
NUMERIC_TARIFF = re.compile(
    r'(?:\b\d+\s*marks?(?:\s+each)?\b'
    r'|\bmarks?\s*[:=@x×]?\s*\d+\b'
    r'|(?:@|x|×)\s*\d+\s*marks?(?:\s+each)?\b)', re.I)
TABLE_HEADING_WORDS = {
    'protein', 'proteins', 'food', 'source', 'sources', 'example', 'examples',
    'class', 'classes', 'type', 'types', 'true', 'false', 'function',
    'functions', 'property', 'properties', 'cause', 'effect', 'measure',
    'nutrient', 'nutrients', 'process', 'temperature', 'time', 'organ',
    'enzyme', 'symbol', 'information', 'name', 'description', 'account',
}


def _token(text: str) -> str:
    return unicodedata.normalize('NFKD', text).encode(
        'ascii', 'ignore').decode().casefold()


def token_offsets(text: str):
    return [(_token(m.group()), m.start(), m.end()) for m in TOKEN.finditer(text)
            if _token(m.group())]


def candidates(question: str, haystack, width=6):
    needle = [x[0] for x in token_offsets(question)[:width]]
    words = [x[0] for x in haystack]
    if len(needle) < width:
        return []
    return [i for i in range(len(words) - width + 1)
            if words[i:i + width] == needle]


def flexible_candidates(question: str, haystack):
    """Locate a prompt whose paper and scheme differ by a word or glyph.

    The official schemes commonly change ``give`` to ``state``, render a tick
    as ``9`` instead of ``✓``, or place the first half of a compound prompt
    on a separate line.  An exact run elsewhere in the opening paper wording
    is still document-to-document evidence; prefer the longest run and never
    go below four words (or the whole prompt when it is shorter).
    """
    qwords = [x[0] for x in token_offsets(question)]
    words = [x[0] for x in haystack]
    if not qwords:
        return []
    floor = min(4, len(qwords))
    for width in range(min(6, len(qwords)), floor - 1, -1):
        for offset in range(0, min(18, len(qwords) - width + 1)):
            needle = qwords[offset:offset + width]
            found = [i for i in range(len(words) - width + 1)
                     if words[i:i + width] == needle]
            if found:
                return found
    return []


def natural(key):
    return (key[1], key[2] or '',
            ROMANS.index(key[3]) if key[3] in ROMANS else 99)


def slug(text: str, limit=9):
    stop = {'a', 'an', 'and', 'the', 'of', 'to', 'in', 'for', 'on', 'with',
            'each', 'following', 'one', 'two', 'three', 'four', 'give', 'state',
            'explain', 'outline', 'describe', 'discuss', 'name'}
    words = [_token(m.group()) for m in TOKEN.finditer(text)]
    words = [w for w in words if w and w not in stop][:limit]
    return '-'.join(words) or 'paper-task'


def topic_for(key, question):
    section, q, _, _ = key
    t = _token(question)
    if section == 'C':
        if q == 1:
            if re.search(r'interior|colour|room|furniture|design principle', t):
                return 'home-economics-3-4'
            if re.search(r'energy|insulat|emission|sustainab|efficien', t):
                return 'home-economics-3-6'
            if re.search(r'house|housing|planning permission|accommodation|site', t):
                return 'home-economics-3-3'
            return 'home-economics-3-5'
        if q == 2:
            return ('home-economics-3-7' if re.search(
                r'fabric|fibre|textile|weav|knit|finish', t)
                    else 'home-economics-3-8')
        if re.search(r'poverty|unemploy|income|deprivation', t):
            return 'home-economics-3-9'
        if re.search(r'educat|school|achievement|initiative|training', t):
            return 'home-economics-3-10'
        return 'home-economics-3-11'

    rules = [
        (r'protein|amino acid|peptide|deamination', 'home-economics-0-5'),
        (r'carbohydrate|sugar|starch|fibre|cellulose', 'home-economics-0-6'),
        (r'lipid|fat|cholesterol|fatty acid', 'home-economics-0-7'),
        (r'vitamin|mineral|calcium|iron|sodium|water|anaemia|osteoporosis',
         'home-economics-0-8'),
        (r'meat|fish|milk|cheese|egg|cereal|vegetable|fruit|yoghurt|food commodity',
         'home-economics-0-9'),
        (r'food poison|haccp|bacteria|spoil|hygiene|preserv|contamin|micro-organ',
         'home-economics-0-4'),
        (r'cook|heat|sauce|pastry|gelatin|emulsion|foam|ferment|culinary',
         'home-economics-0-2'),
        (r'menu|meal|diet|health|vegetarian|vegan|obesity|coeliac|diabetes',
         'home-economics-0-1'),
        (r'food industr|packag|additive|bord bia|sensory|product development',
         'home-economics-0-11'),
        (r'consumer|retail|shop|sale of goods|complaint|credit act|label|symbol',
         'home-economics-1-2'),
        (r'income|budget|saving|mortgage|insurance|assurance|credit|finance|mabs',
         'home-economics-1-1'),
        (r'appliance|electric|refriger|microwave|technology|energy',
         'home-economics-1-3'),
        (r'environment|pollution|renewable|sustainab', 'home-economics-1-5'),
        (r'textile|fabric|laundry|detergent|care symbol', 'home-economics-1-4'),
        (r'marriage|divorce|separation|family life cycle|will',
         'home-economics-2-1'),
        (r'older|elderly|ageing|grandparent', 'home-economics-2-3'),
        (r'education|work|employment|leisure', 'home-economics-2-2'),
        (r'family|gender role|sociological|child', 'home-economics-2-0'),
    ]
    for pattern, topic in rules:
        if re.search(pattern, t):
            return topic
    return 'home-economics-1-0'


class SchemeJoin:
    def __init__(self, year, level, targets, texts):
        self.year, self.level = year, level
        self.path = os.path.join(
            ROOT, 'examiner-reports', 'home-economics', 'schemes',
            f'{year}-{level}.md')
        raw = open(self.path, encoding='utf-8', errors='ignore').read()
        self.raw = raw.split('<!-- pdf-block-order', 1)[0]
        choices = []
        for section in 'ABC':
            choices.append([m.start() for m in re.finditer(
                SECTION_HEAD.format(section=section), self.raw, re.M | re.I)])
        if any(not c for c in choices):
            raise AssertionError(f'{year} {level}: scheme has no A/B/C boundary')

        # Cover pages also list the section totals.  Pick the ordered A/B/C
        # triple which contains the most independently paper-confirmed prompts.
        best = (-1, None)
        for a, b, c in itertools.product(*choices):
            if not a < b < c:
                continue
            bounds = {'A': (a, b), 'B': (b, c), 'C': (c, len(self.raw))}
            score = 0
            for key in targets:
                start, end = bounds[key[0]]
                score += bool(candidates(texts[key], token_offsets(
                    self.raw[start:end])))
            if score > best[0]:
                best = score, bounds
        if best[1] is None:
            raise AssertionError(f'{year} {level}: no ordered scheme sections')
        self.bounds = best[1]
        # Section C is followed by an independently assessed Food Studies
        # coursework scheme.  It is not a continuation of the final elective;
        # without this stop the last card acquired page numbers and coursework
        # criteria as purported answer rows.
        c_start, c_end = self.bounds['C']
        coursework = re.search(
            r'(?im)^.*(?:MARKING SCHEME.*)?HOME ECONOMICS.*$\n'
            r'.*FOOD STUDIES COURSEWORK|^FOOD STUDIES COURSEWORK\s*$',
            self.raw[c_start:c_end])
        if coursework:
            self.bounds['C'] = (c_start, c_start + coursework.start())
        self.locations = self._locations(targets, texts)

    def _locations(self, targets, texts):
        out = {}
        for section in 'ABC':
            start, end = self.bounds[section]
            haystack = token_offsets(self.raw[start:end])
            previous = -1
            for key in sorted((k for k in targets if k[0] == section), key=natural):
                found = [i for i in candidates(texts[key], haystack)
                         if i > previous]
                if not found:
                    found = [i for i in flexible_candidates(texts[key], haystack)
                             if i > previous]
                if not found:
                    continue
                at = found[0]
                # A flexible anchor can begin after the scheme's first word
                # (``give``/``state`` is the usual difference).  Rewind to the
                # start of that official line so the chunk retains the full
                # examiner wording and its tariff.
                relative = haystack[at][1]
                line_start = self.raw.rfind('\n', start, start + relative) + 1
                out[key] = max(start, line_start)
                previous = at
        return out

    def chunks(self):
        out = {}
        by_section = defaultdict(list)
        for key, at in self.locations.items():
            by_section[key[0]].append((at, key))
        for section, located in by_section.items():
            located.sort()
            for i, (start, key) in enumerate(located):
                end = (located[i + 1][0] if i + 1 < len(located)
                       else self.bounds[section][1])
                out[key] = self.raw[start:end]
        return out


def total_for(key, question, chunk):
    if key[0] == 'A':
        return 6
    found = [int(n) for n in TOTAL.findall(chunk) if 0 < int(n) <= 80]
    if found:
        return found[0]
    found = [int(n) for n in TOTAL.findall(question) if 0 < int(n) <= 80]
    return found[-1] if found else None


def answer_start(chunk):
    # A printed total closes the task wording.  Where the paper omits one,
    # the first explicit tariff line is the equally strong boundary.
    total = TOTAL.search(chunk)
    if total and total.start() < 3000:
        return total.end()
    tariff = re.search(
        r'(?im)^.*?(?:\d+\s*(?:points?|functions?|factors?|ways?|reasons?|'
        r'examples?|guidelines?|items?|types?|methods?|classes?|sources?)?\s*'
        r'(?:@|x|×)\s*\d+\s*marks?|(?:name|description)\s*:\s*\d+\s*marks?).*$',
        chunk[:3000])
    return tariff.end() if tariff else 0


def proposed_rows(question, chunk):
    body = chunk[answer_start(chunk):]
    lines = []
    for line in body.splitlines():
        line = PAGE.sub('', line).strip()
        if (not line or FURNITURE.match(line) or TARIFF_ONLY.match(line)
                or BARE_ENUMERATOR.match(line)):
            continue
        line = TARIFF_PREFIX.sub('', line).strip()
        if line:
            lines.append(line)
    # PDF-to-markdown line breaks are typographic wrapping, not marking-point
    # boundaries.  Flatten first and split on the examiner's semicolons; this
    # keeps "nutritive value in / dishes" as one answer instead of two bogus
    # rows. A long prose point may still contain several full sentences, which
    # are safe secondary boundaries.
    body = ' '.join(lines)
    proposals = []
    pieces = []
    for group in body.split(';'):
        group = ' '.join(group.split()).strip()
        if len(group) <= 520:
            pieces.append(group)
        else:
            pieces.extend(re.split(r'(?<=[.!?])\s+(?=[A-Z(])', group))
    for piece in pieces:
        text = ' '.join(piece.split()).strip(' •\t')
        text = TARIFF_PREFIX.sub('', text).strip()
        embedded_tariffs = list(NUMERIC_TARIFF.finditer(text))
        if embedded_tariffs:
            text = text[embedded_tariffs[-1].end():].strip(' ,;:()')
            for _ in range(4):
                cleaned = re.sub(
                    r'^(?:each\b|\(?graded\s*(?:\([\d:]+\)|[\d:]+\)?)'
                    r'|[x×]\s*\d+\b)'
                    r'[),:;\s]*', '', text, flags=re.I)
                if cleaned == text:
                    break
                text = cleaned
        # The next elective route sometimes follows the final marking point
        # on the same extracted line.  It is a new paper task, never part of
        # this answer row.
        text = re.split(
            r'\s+(?:and|or)\s+\d+\.\([a-z]\)\s+',
            text, maxsplit=1)[0].strip()
        text = re.sub(
            r'^\(\d+\s+(?:points?|references?|strateg(?:y|ies))\b[^)]*\)\s*',
            '', text, flags=re.I)
        text = TRAILING_ETC.sub('', text).strip(' ,;:')
        text = TRAILING_ETC.sub('', text).strip(' ,;:')
        text = re.sub(r'\s+\d+\.?\s*$', '', text).strip()
        text = re.sub(r'\s+\([a-zivx]+\)?\s*$', '', text, flags=re.I).strip()
        if not text or len(text) > 520 or len(text) < 2:
            continue
        words = {_token(m.group()) for m in TOKEN.finditer(text)}
        if (TARIFF_ONLY.match(text)
                or FURNITURE.match(text) or CONTENT_FREE.match(text)
                or BARE_ENUMERATOR.match(text)
                or re.fullmatch(r'marks?(?:\s+each)?', text, re.I)
                or (words and words <= TABLE_HEADING_WORDS)):
            continue
        if QUESTIONISH.match(text):
            continue
        # Do not hand the prompt back as its own answer where a missing total
        # left answer_start at zero.
        qwords = [_token(m.group()) for m in TOKEN.finditer(question)][:7]
        pwords = [_token(m.group()) for m in TOKEN.finditer(text)][:7]
        if len(qwords) >= 5 and pwords[:5] == qwords[:5]:
            continue
        canonical = _token(text)
        if canonical and canonical not in {_token(p) for p in proposals}:
            proposals.append(text)
    return proposals


def traceable(year, level, claims):
    if not claims:
        return set()
    path = os.path.join('examiner-reports', 'home-economics', 'schemes',
                        f'{year}-{level}.md')
    proc = subprocess.run(
        ['node', VERIFY], cwd=ROOT, text=True, capture_output=True,
        input=json.dumps({'scheme': path, 'claims': claims}))
    if proc.returncode:
        raise RuntimeError(proc.stderr.strip() or 'verify-claims failed')
    return set(json.loads(proc.stdout)['ok'])


def card_id(year, level, key):
    section, q, letter, roman = key
    tail = f'q{q}' + (letter or '') + (roman or '')
    return f'he-{year}-{level}-s{section.lower()}-{tail}'


def clean_question(text):
    text = re.split(
        r'\b(?:Answerbook for Sections|Instructions Questions for Sections|'
        r'Start each question on a new page|Blank Page)\b', text, maxsplit=1)[0]
    text = re.sub(r'_{3,}', ' ', text)
    return ' '.join(text.split()).strip()


def make_card(year, level, key, question, total, rows):
    long_level = 'higher' if level == 'hl' else 'ordinary'
    made_rows = []
    for i, row in enumerate(rows, start=1):
        if isinstance(row, str):
            row = {'verbatim': row}
        made_rows.append({
            'id': f'r-{i}', 'kind': row.get('kind', 'point'),
            'verbatim': row['verbatim'], 'marks': None,
            **({'contextNote': row['contextNote']} if row.get('contextNote') else {}),
        })
    card = {
        'id': card_id(year, level, key),
        'topicId': topic_for(key, question),
        'conceptId': slug(question),
        'level': long_level,
        'year': year,
        'subjectId': 'home-economics',
        'section': key[0],
        'questionRef': f'{year} {level.upper()} {key_label(key)}',
        'questionText': clean_question(question),
        'stem': '',
        'figureKey': '',
        'labelKey': [],
        'tariffModel': {'kind': 'questionTotal'},
        'totalMarks': total,
        'rows': made_rows,
        'notes': ('Paper prompt joined to the official scheme by its opening '
                  'word run; the scheme prices the task as a whole, so no '
                  'per-row values are invented.'),
    }
    qfigure = QUESTION_FIGURES.get((year, level, *key))
    if qfigure:
        card['questionFigureKey'] = qfigure
    diagram = DIAGRAM_FIGURES.get((year, level, *key))
    if diagram:
        card.update(diagram)
    return card


def target_sitting(year, level):
    parts, texts, _ = census_sections('home-economics', year, level)
    leaves = leaves_of(parts)
    if (year, level) in OLDER_COUNTS:
        expected = OLDER_COUNTS[(year, level)]
        if len(leaves) != expected:
            raise AssertionError(
                f'{year} {level}: census drifted {expected} -> {len(leaves)} leaves')
        targets = leaves
    else:
        wanted = RECENT_TARGETS[(year, level)]
        lookup = {key_label(k): k for k in leaves}
        missing = wanted - set(lookup)
        if missing:
            raise AssertionError(f'{year} {level}: target(s) absent: {sorted(missing)}')
        targets = [lookup[label] for label in sorted(wanted)]
    return targets, texts


def build():
    cards, held = [], []
    sittings = list(OLDER_COUNTS) + list(RECENT_TARGETS)
    for year, level in sittings:
        targets, texts = target_sitting(year, level)
        joined = SchemeJoin(year, level, targets, texts)
        chunks = joined.chunks()
        proposals = {key: proposed_rows(texts[key], chunks[key])
                     for key in joined.locations}
        manual_here = {
            key: MANUAL_ROWS[(year, level, *key)]
            for key in targets if (year, level, *key) in MANUAL_ROWS
        }
        all_claims = list(dict.fromkeys(
            [claim for rows in proposals.values() for claim in rows]
            + [row['verbatim'] for rows in manual_here.values()
               for row in rows]))
        good = traceable(year, level, all_claims)
        combined = {}
        for spec, combined_total in COMBINED_TOTALS.items():
            if spec[:2] != (year, level):
                continue
            _, _, section, q, letter = spec
            children = sorted(
                (key for key in targets
                 if key[:3] == (section, q, letter) and key[3]),
                key=natural)
            if len(children) < 2:
                raise AssertionError(
                    f'{year} {level} {section} Q{q}({letter}): '
                    'combined boundary lost its children')
            parent = (section, q, letter, None)
            combined[parent] = (children, combined_total)
        child_to_parent = {
            child: parent for parent, (children, _) in combined.items()
            for child in children
        }
        for key in targets:
            if key in child_to_parent:
                parent = child_to_parent[key]
                children, combined_total = combined[parent]
                if key != children[0]:
                    continue
                parent_intro = texts.get(parent, '')
                pieces = ([parent_intro] if parent_intro else []) + [
                    f'({child[3]}) {texts[child]}' for child in children]
                question = ' '.join(pieces)
                rows = []
                for child in children:
                    chunk = chunks.get(child)
                    # If a chunk contains only its prompt, answer_start is zero
                    # and proposed_rows can mistake that fragment for content.
                    if chunk and answer_start(chunk):
                        rows.extend(proposals.get(child, []))
                rows = [row for row in dict.fromkeys(rows) if row in good][:12]
                if not rows:
                    held.append((year, level, parent,
                                 'no traceable content row recovered'))
                    continue
                cards.append(make_card(
                    year, level, parent, question, combined_total, rows))
                continue
            chunk = chunks.get(key)
            if chunk is None:
                held.append((year, level, key, 'paper prompt not found in scheme'))
                continue
            total = total_for(key, texts[key], chunk)
            if key in manual_here:
                rows = [row for row in manual_here[key]
                        if row['verbatim'] in good]
            else:
                rows = [row for row in proposals[key] if row in good][:12]
            if total is None:
                held.append((year, level, key, 'no independently printed part total'))
                continue
            if not rows:
                held.append((year, level, key, 'no traceable content row recovered'))
                continue
            cards.append(make_card(year, level, key, texts[key], total, rows))
        print(f'{year} {level}: {sum(c["year"] == year and c["level"].startswith("h" if level == "hl" else "o") for c in cards)} cards; '
              f'{sum(h[0] == year and h[1] == level for h in held)} held', file=sys.stderr)
    for year, level, key, why in held:
        print(f'HELD {year} {level} {key_label(key)} — {why}', file=sys.stderr)
    return cards


if __name__ == '__main__':
    print(json.dumps(build(), ensure_ascii=False, indent=1))
