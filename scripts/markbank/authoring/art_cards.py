#!/usr/bin/env python3
"""Build the complete 2021–2025 Art Mark Bank corpus.

The question papers supply the exact prompts.  The marking schemes supply the
published component allocations (2021–2022) and descriptor bands (2023–2025).
The separate SEC illustration sheets remain page images from Paper Trail; the
script records only their official file identity and page number.

One outer question number is not one Mark Bank card.  A card is one separately
marked printed task that a student can practise on its own.  Lettered parts and
the two tasks separated by the legacy paper's standalone "and" are split.  A
fixed list of named works, artists, buildings or movements is expanded so each
printed choice becomes a real revision card.  A finite "choose N" list is
expanded into every valid combination.  The four-criterion Section B/C essay
remains intact because the SEC applies that rubric holistically.

The complete corpus is therefore 462 cards across ten papers:

  * Higher Level:   72 + 68 + 26 + 26 + 30 = 222 cards
  * Ordinary Level: 78 + 75 + 26 + 26 + 35 = 240 cards

Run:

    python3 scripts/markbank/authoring/art_cards.py
    python3 scripts/markbank/authoring/art_cards.py --check

The generated runtime JSON and census are committed because the source PDFs
are deliberately gitignored.
"""

from __future__ import annotations

import argparse
import itertools
import json
import os
import re
import sys
import unicodedata
from dataclasses import dataclass
from typing import Any, Iterable

import fitz


ROOT = os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))))
PAPER_ROOT = os.path.join(ROOT, 'examiner-reports', 'art', 'papers')
SCHEME_ROOT = os.path.join(ROOT, 'examiner-reports', 'art', 'schemes')
OUT = os.path.join(ROOT, 'components', 'MarkBank', 'cards', 'art', 'authored.json')
CENSUS_OUT = os.path.join(ROOT, 'scripts', 'markbank', 'authored', 'art-census.json')

YEARS = tuple(range(2021, 2026))
LEVELS = ('higher', 'ordinary')
LEVEL_SHORT = {'higher': 'hl', 'ordinary': 'ol'}
LEVEL_REF = {'higher': 'HL', 'ordinary': 'OL'}

EXPECTED_QUESTIONS_BY_YEAR_LEVEL = {
    (2021, 'higher'): 20,
    (2021, 'ordinary'): 21,
    (2022, 'higher'): 20,
    (2022, 'ordinary'): 21,
    (2023, 'higher'): 19,
    (2023, 'ordinary'): 19,
    (2024, 'higher'): 19,
    (2024, 'ordinary'): 19,
    (2025, 'higher'): 19,
    (2025, 'ordinary'): 19,
}

EXPECTED_CARDS_BY_YEAR_LEVEL = {
    (2021, 'higher'): 72,
    (2021, 'ordinary'): 78,
    (2022, 'higher'): 68,
    (2022, 'ordinary'): 75,
    (2023, 'higher'): 26,
    (2023, 'ordinary'): 26,
    (2024, 'higher'): 26,
    (2024, 'ordinary'): 26,
    (2025, 'higher'): 30,
    (2025, 'ordinary'): 35,
}

# A fixed choice printed by the SEC materially changes the knowledge a student
# must retrieve, so it gets its own practice card. Open choices such as "one
# named work" cannot be exhaustively enumerated and remain one card. Labels are
# kept exactly as printed; the short key exists only to make a stable card id.
PRINTED_CHOICES: dict[tuple[int, str, int], tuple[tuple[str, str], ...]] = {
    (2021, 'higher', 4): (
        ('castletown-house', 'Castletown House'),
        ('casino-at-marino', 'Casino at Marino'),
        ('custom-house-dublin', 'Custom House, Dublin'),
    ),
    (2021, 'higher', 7): (
        ('john-henry-foley', 'John Henry Foley (1818-1874)'),
        ('harry-clarke', 'Harry Clarke (1889-1931)'),
        ('nano-reid', 'Nano Reid (1900-1981)'),
        ('francis-bacon', 'Francis Bacon (1909-1992)'),
        ('tony-omalley', 'Tony O’Malley (1913-2003)'),
        ('rowan-gillespie', 'Rowan Gillespie (b.1953)'),
        ('alice-maher', 'Alice Maher (b.1956)'),
    ),
    (2021, 'higher', 14): (
        ('jan-van-eyck', 'Jan van Eyck (c.1390-1441)'),
        ('el-greco', 'El Greco (1541-1614)'),
        ('ingres', 'Jean-Auguste-Dominique Ingres (1780-1867)'),
        ('paul-gauguin', 'Paul Gauguin (1848-1903)'),
        ('henry-moore', 'Henry Moore (1898-1986)'),
    ),
    (2021, 'higher', 15): (
        ('baroque', 'Baroque'),
        ('rococo', 'Rococo'),
        ('cubism', 'Cubism'),
        ('futurism', 'Futurism'),
    ),
    (2021, 'ordinary', 4): (
        ('castletown-house', 'Castletown House'),
        ('casino-at-marino', 'Casino at Marino'),
    ),
    (2021, 'ordinary', 7): (
        ('james-arthur-oconnor', 'James Arthur O’Connor (1792-1841)'),
        ('walter-osborne', 'Walter Osborne (1859-1903)'),
        ('nano-reid', 'Nano Reid (1900-1981)'),
        ('oisin-kelly', 'Oisín Kelly (1915-1981)'),
        ('edward-delaney', 'Edward Delaney (1930-2009)'),
        ('rowan-gillespie', 'Rowan Gillespie (b.1953)'),
        ('alice-maher', 'Alice Maher (b.1956)'),
    ),
    (2021, 'ordinary', 14): (
        ('arnolfini-portrait', '‘The Arnolfini Portrait’ by Jan van Eyck (c.1390-1441)'),
        ('taking-of-christ', '‘The Taking of Christ’ by Caravaggio (1571-1610)'),
        ('night-watch', '‘Night Watch’ by Rembrandt van Rijn (1606-1669)'),
        ('van-goghs-bedroom', '‘Van Gogh’s Bedroom in Arles’ by Vincent van Gogh (1853-1890)'),
        ('madame-matisse-green-line', '‘Portrait of Madame Matisse. The Green Line, 1905’ by Henri Matisse (1869-1954)'),
    ),
    (2022, 'higher', 7): (
        ('james-barry', 'James Barry (1741-1806)'),
        ('daniel-maclise', 'Daniel Maclise (1806-1870)'),
        ('jack-b-yeats', 'Jack B. Yeats (1871-1957)'),
        ('mary-swanzy', 'Mary Swanzy (1882-1978)'),
        ('tony-omalley', 'Tony O’Malley (1913-2003)'),
        ('robert-ballagh', 'Robert Ballagh (b.1943)'),
        ('colin-davidson', 'Colin Davidson (b.1968)'),
    ),
    (2022, 'higher', 14): (
        ('paolo-uccello', 'Paolo Uccello (c.1397-1475)'),
        ('diego-velazquez', 'Diego Velázquez (1599-1660)'),
        ('jmw-turner', 'J.M.W. Turner (1775-1851)'),
        ('edvard-munch', 'Edvard Munch (1863-1944)'),
        ('pablo-picasso', 'Pablo Picasso (1881-1973)'),
    ),
    (2022, 'higher', 15): (
        ('international-gothic', 'International Gothic'),
        ('impressionism', 'Impressionism'),
        ('die-brucke', 'Die Brücke'),
        ('surrealism', 'Surrealism'),
    ),
    (2022, 'ordinary', 7): (
        ('daniel-maclise', 'Daniel Maclise (1806-1870)'),
        ('jack-b-yeats', 'Jack B. Yeats (1871-1957)'),
        ('paul-henry', 'Paul Henry (1876-1958)'),
        ('harry-clarke', 'Harry Clarke (1889-1931)'),
        ('louis-le-brocquy', 'Louis le Brocquy (1916-2012)'),
        ('martin-gale', 'Martin Gale (b.1949)'),
        ('geraldine-oneill', 'Geraldine O’Neill (b.1971)'),
    ),
    (2022, 'ordinary', 14): (
        ('mary-magdalene', '‘Mary Magdalene’ by Donatello (c.1386-1466)'),
        ('girl-with-a-pearl-earring', '‘Girl with a Pearl Earring’ by Johannes Vermeer (1632-1675)'),
        ('death-of-marat', '‘The Death of Marat’ by Jacques-Louis David (1748-1825)'),
        ('bar-at-the-folies-bergere', '‘A Bar at the Folies-Bergère’ by Edouard Manet (1832-1883)'),
        ('the-scream', '‘The Scream’ by Edvard Munch (1863-1944)'),
    ),
    (2025, 'higher', 12): (
        ('fauvism', 'Fauvism'),
        ('expressionism', 'Expressionism'),
        ('cubism', 'Cubism'),
        ('bauhaus', 'Bauhaus'),
        ('surrealism', 'Surrealism'),
    ),
}

# A closed "choose N" instruction is a different kind of selectable route.
# The first corpus sweep handled only choose-one lists and therefore collapsed
# the ten pairs printed for 2025 OL Q4(a) into one card. Keep the pool and N
# explicit so the expansion is mechanically complete (n choose k), rather than
# relying on another hand-authored list of combinations.
TASK_COMBINATION_CHOICES: dict[
    tuple[int, str, int, str], tuple[int, tuple[tuple[str, str], ...]]
] = {
    (2025, 'ordinary', 4, 'a'): (2, (
        ('colour', 'colour'),
        ('texture', 'texture'),
        ('line', 'line'),
        ('pattern', 'pattern'),
        ('shape', 'shape'),
    )),
}

# This is a finite printed pool, but it is not a choose-one instruction. Two
# artists may use the same medium, different media, or several media, so
# enumerating subsets would manufacture restrictions the paper does not make.
# Keeping the reviewed exception beside the expanding pools makes every closed
# list a deliberate decision and lets the audit fail on an unreviewed one.
REVIEWED_NON_ENUMERABLE_POOLS: dict[tuple[int, str, int], str] = {
    (2025, 'higher', 19): (
        'The question permits any media across two artists; it does not require '
        'one fixed medium or one fixed subset.'),
}

# Selection words do not always define a finite bank of distinct exam routes.
# Record the remaining occurrences so a new ``choose``/``either`` directive
# cannot enter silently, while these reviewed open or logistical choices stay
# faithful to the paper instead of being over-expanded.
REVIEWED_OPEN_SELECTIONS: dict[tuple[int, str, int], str] = {
    (2021, 'ordinary', 16): (
        '"Either online or in person" changes how the gallery was visited, '
        'not the knowledge or marked task.'),
    (2022, 'ordinary', 13): (
        'The candidate chooses any Picasso work they studied; the paper prints '
        'no finite work list to enumerate.'),
    (2022, 'ordinary', 16): (
        '"Either online or in person" changes how the gallery was visited, '
        'not the knowledge or marked task.'),
}

# Page numbers are one-based within the separate official illustration PDF.
# Every binding below was checked visually against the rendered sheet.
ILLUSTRATION_PAGES: dict[tuple[int, str], dict[int, int]] = {
    (2021, 'higher'): {
        2: 1, 5: 1, 6: 1, 17: 1, 20: 1,
        10: 2, 11: 2, 12: 2, 13: 2,
    },
    (2021, 'ordinary'): {
        1: 1, 2: 1, 5: 1, 6: 1, 18: 1, 19: 1, 20: 1,
        9: 2, 10: 2, 11: 2, 12: 2,
    },
    (2022, 'higher'): {
        2: 1, 3: 1, 5: 1, 6: 1, 17: 1, 18: 1, 19: 1,
        10: 2, 11: 2, 12: 2,
    },
    (2022, 'ordinary'): {
        3: 1, 5: 1, 6: 1, 18: 1, 19: 1, 21: 1,
        8: 2, 9: 2, 10: 2, 12: 2,
    },
    (2023, 'higher'): {1: 1, 7: 1, 2: 2, 4: 2, 6: 2},
    (2023, 'ordinary'): {1: 1, 7: 1, 3: 2, 5: 2, 6: 2},
    (2024, 'higher'): {1: 1, 7: 1, 2: 2, 4: 2, 6: 2},
    (2024, 'ordinary'): {1: 1, 7: 1, 3: 2, 4: 2, 5: 2},
    (2025, 'higher'): {1: 1, 7: 1, 2: 2, 4: 2, 6: 2},
    (2025, 'ordinary'): {1: 1, 7: 1, 2: 2, 4: 2, 5: 2},
}

LONG_TOPIC = {
    8: 'art-4-0', 9: 'art-4-1', 10: 'art-4-2',
    11: 'art-4-3', 12: 'art-4-4', 13: 'art-4-5',
    14: 'art-5-0', 15: 'art-5-1', 16: 'art-5-2',
    17: 'art-5-3', 18: 'art-5-4', 19: 'art-5-5',
}

# Classification here is editorial, not inferred from marks. These are the
# papers' actual content focus, checked question by question against the
# canonical Art content areas. An explicit table avoids filing "work outside
# their usual environments" under Art and the Environment merely because the
# word "environment" happens to appear in an artist-residency question.
CURRENT_SHORT_TOPICS: dict[tuple[int, str, int], str] = {}
for _year, _level, _topics in (
    (2023, 'higher', ('art-6-1', 'art-6-1', 'art-6-2', 'art-6-3', 'art-6-0', 'art-6-1', 'art-6-3')),
    (2023, 'ordinary', ('art-6-1', 'art-6-0', 'art-6-2', 'art-6-0', 'art-6-1', 'art-6-1', 'art-6-1')),
    (2024, 'higher', ('art-6-1', 'art-6-1', 'art-6-0', 'art-6-1', 'art-6-0', 'art-6-3', 'art-6-2')),
    (2024, 'ordinary', ('art-6-1', 'art-6-0', 'art-6-1', 'art-6-2', 'art-6-2', 'art-6-1', 'art-6-3')),
    (2025, 'higher', ('art-6-3', 'art-6-1', 'art-6-0', 'art-6-1', 'art-6-0', 'art-6-1', 'art-6-1')),
    (2025, 'ordinary', ('art-6-2', 'art-6-2', 'art-6-0', 'art-6-1', 'art-6-1', 'art-6-0', 'art-6-1')),
):
    for _number, _topic in enumerate(_topics, start=1):
        CURRENT_SHORT_TOPICS[(_year, _level, _number)] = _topic

LEGACY_TOPIC_OVERRIDES = {
    (2021, 'higher', 2): 'art-5-0',
    (2021, 'ordinary', 4): 'art-5-3',
    (2021, 'ordinary', 11): 'art-4-2',
    (2021, 'ordinary', 13): 'art-4-4',
    (2021, 'ordinary', 16): 'art-6-0',
    (2021, 'ordinary', 17): 'art-6-1',
    (2021, 'ordinary', 18): 'art-6-1',
    (2021, 'ordinary', 19): 'art-6-3',
    (2021, 'ordinary', 20): 'art-6-2',
    (2021, 'ordinary', 21): 'art-6-1',
    (2022, 'ordinary', 16): 'art-6-0',
    (2022, 'ordinary', 17): 'art-6-1',
    (2022, 'ordinary', 18): 'art-6-1',
    (2022, 'ordinary', 19): 'art-6-1',
    (2022, 'ordinary', 20): 'art-6-3',
    (2022, 'ordinary', 21): 'art-6-1',
}

LEGACY_IRISH_TOPIC_KEYWORDS: tuple[tuple[str, tuple[str, ...]], ...] = (
    ('art-5-3', ('georgian', 'custom house', 'townhouse', 'country house')),
    ('art-5-2', ('late medieval', 'romanesque church in ireland', 'gothic church in ireland')),
    ('art-5-1', (
        'early christian', 'insular', 'book of kells', 'high cross', 'ardagh chalice',
        'tara brooch', 'chalice', 'reliquary', 'monastic', 'religious metal',
    )),
    ('art-5-0', (
        'newgrange', 'megalithic', 'stone age', 'bronze age', 'iron age', 'celt',
        'turoe stone', 'pre-christian', 'gold artefact', 'gorget', 'passage grave',
    )),
    ('art-5-5', (
        'contemporary irish', 'public sculpture', 'b.19', 'b. 19', 'post 1960',
        'maurice harron', 'robert ballagh', 'colin davidson', 'dorothy cross',
    )),
    ('art-5-4', (
        'irish artist', 'irish painting', 'harry clarke', 'jack b. yeats', 'jack b yeats',
        'william john leech', 'mary swanzy', 'tony o’malley', "tony o'malley",
        'daniel maclise', 'james barry', 'st gobnait', 'modernism in ireland',
    )),
)

EUROPE_TOPIC_KEYWORDS: tuple[tuple[str, tuple[str, ...]], ...] = (
    ('art-4-0', ('romanesque', 'gothic', 'cathedral', 'gislebertus')),
    ('art-4-1', (
        'renaissance', 'mannerism', 'giotto', 'botticelli', 'michelangelo', 'leonardo',
        'raphael', 'uccello', 'donatello', 'primavera', 'mona lisa',
    )),
    ('art-4-2', ('baroque', 'bernini', 'caravaggio', 'rembrandt', 'velázquez', 'velazquez')),
    ('art-4-3', (
        'realism', 'impressionism', 'post-impressionism', 'millet', 'manet', 'monet',
        'renoir', 'degas', 'van gogh', 'cézanne', 'cezanne',
    )),
    ('art-4-4', (
        'modernism', 'fauvism', 'expressionism', 'cubism', 'bauhaus', 'surrealism',
        'die brücke', 'die brucke', 'munch', 'picasso', 'mondrian',
    )),
    ('art-4-5', ('post 1960', 'pop art', 'conceptual art', 'performance art', 'installation art')),
)

TODAYS_WORLD_TOPIC_KEYWORDS: tuple[tuple[str, tuple[str, ...]], ...] = (
    ('art-6-3', (
        'environment', 'outdoor', 'site-specific', 'site specific', 'public park',
        'green space', 'urban', 'bridge', 'architecture', 'building', 'wellbeing',
    )),
    ('art-6-2', (
        'social commentary', 'message', 'comic book', 'graphic novel', 'poster',
        'communicate ideas', 'political', 'advertising',
    )),
    ('art-6-0', (
        'gallery', 'museum', 'arts centre', 'exhibition', 'artist-in-residence',
        'artist in residence', 'career of an artist', 'sketchbook', 'curator',
    )),
    ('art-6-1', (
        'product design', 'fashion', 'costume', 'ceramic', 'embroidery', 'materials',
        'media', 'photograph', 'painting', 'sculpture', 'car design', 'typography',
        'furniture', 'container', 'laptop bag',
    )),
)

SPACE_CHARS = ('\xa0', '\u2007', '\u202f')
LIGATURES = {
    '\u00ad': '', '\ufb00': 'ff', '\ufb01': 'fi', '\ufb02': 'fl',
    '\ufb03': 'ffi', '\ufb04': 'ffl',
}


def clean_unicode(value: str) -> str:
    for char in SPACE_CHARS:
        value = value.replace(char, ' ')
    for bad, good in LIGATURES.items():
        value = value.replace(bad, good)
    return (value.replace('‐', '-').replace('‑', '-').replace('‒', '-')
            .replace('−', '-').replace('–', '–'))


def compact(value: str) -> str:
    return re.sub(r'\s+', ' ', clean_unicode(value)).strip()


def comparable(value: str) -> str:
    value = unicodedata.normalize('NFKC', clean_unicode(value)).lower()
    value = value.replace('’', "'").replace('‘', "'").replace('ʼ', "'")
    return re.sub(r'[^\w]+', ' ', value, flags=re.UNICODE).strip()


def paper_path(year: int, level: str) -> str:
    return os.path.join(PAPER_ROOT, f'{year}-{LEVEL_SHORT[level]}-paper.pdf')


def scheme_path(year: int, level: str) -> str:
    return os.path.join(SCHEME_ROOT, f'{year}-{LEVEL_SHORT[level]}.pdf')


def expected_numbers(year: int, level: str) -> list[int]:
    return list(range(1, EXPECTED_QUESTIONS_BY_YEAR_LEVEL[(year, level)] + 1))


def paper_fileid(level: str) -> str:
    return f"LC014{'A' if level == 'higher' else 'G'}LP000EV"


def illustration_fileid(level: str) -> str:
    return f"LC014{'A' if level == 'higher' else 'G'}LP004BV"


def is_furniture(line: str, year: int) -> bool:
    value = compact(line)
    if not value:
        return False
    patterns = (
        rf'^Leaving Certificate Examination,?\s*{year}\b',
        r'^Art\s*[-–]\s*(?:Visual Studies|History and Appreciation)',
        r'^Section\s+[ABC]\s+(?:Today.s world|Europe and the wider world|Ireland and its place)',
        r'^Section\s+(?:I|II|III)\s*[-–]',
        r'^Answer any five questions in this section\.?$',
        r'^Answer one question from this section\.?$',
        r'^Optional (?:Planning|Answer) Space',
        r'^Additional Answer Space',
        r'^Label all work clearly',
        r'^Answer for Question\s*$',
        r'^Do not hand this up\.?$',
        r'^This document will not be returned',
        r'^State Examinations Commission\.?$',
        r'^Coimisiún na Scrúduithe Stáit$',
        r'^\d{1,2}$',
    )
    return any(re.search(pattern, value, re.I) for pattern in patterns)


@dataclass
class PagedPaper:
    text: str
    starts: list[tuple[int, int]]

    def page_for(self, offset: int) -> int:
        page = 1
        for start, number in self.starts:
            if start > offset:
                break
            page = number
        return page


def paper_text(path: str, year: int) -> PagedPaper:
    document = fitz.open(path)
    chunks: list[str] = []
    starts: list[tuple[int, int]] = []
    cursor = 0
    for page_number, page in enumerate(document, start=1):
        kept: list[str] = []
        for raw in clean_unicode(page.get_text('text', sort=True)).splitlines():
            line = raw.strip()
            if is_furniture(line, year):
                continue
            # Empty answer-space labels add no part of the ask.
            if re.fullmatch(r'Heading\s+[12]:', compact(line), re.I):
                continue
            kept.append(line)
        chunk = '\n'.join(kept)
        starts.append((cursor, page_number))
        chunks.append(chunk)
        cursor += len(chunk) + 2
    return PagedPaper('\n\n'.join(chunks), starts)


def clean_prompt(value: str) -> str:
    value = clean_unicode(value)
    # The final question has no following question marker to stop its slice.
    # Cut at the first back-matter heading rather than absorbing credits,
    # copyright notices and blank-page instructions into Q19/Q20/Q21.
    value = re.split(
        r'(?mi)^\s*(?:There is no examination material on this page|'
        r'Do not write on this page|Acknowledgements|Copyright notice)\b',
        value,
        maxsplit=1,
    )[0]
    value = re.sub(r'(?m)^\s*10\s+marks\s*$', '', value, flags=re.I)
    value = re.sub(r'(?m)^\s*(?:50|100|150)\s+marks\s*$', '', value, flags=re.I)
    value = re.sub(r'(?m)^\s*Answer any five questions in this section\.?\s*$', '', value, flags=re.I)
    value = re.sub(r'(?m)^\s*Answer one question from this section\.?\s*$', '', value, flags=re.I)
    # Protect structural tokens before unwrapping the PDF's visual line breaks.
    # In particular, "part (a) above" is prose, not a new compulsory part.
    value = re.sub(r'(?m)^\s*[•]\s*', '\n@@BULLET@@ ', value)
    value = re.sub(r'(?mi)^\s*(\([abc]\))\s+', r'\n@@PART@@\1 ', value)
    value = re.sub(r'(?mi)^\s*and\s*$', '\n@@AND@@\n', value)
    value = re.sub(r'[ \t]+', ' ', value)
    value = re.sub(r'\s*\n\s*', ' ', value)
    value = value.replace('@@BULLET@@ ', '\n• ')
    value = value.replace('@@PART@@', '\n')
    value = value.replace('@@AND@@', '\nand')
    value = re.sub(r'\s+([?.!,;:])', r'\1', value)
    value = re.sub(r'[ \t]+\n', '\n', value)
    value = re.sub(r'\n[ \t]+', '\n', value)
    value = re.sub(r'\n{2,}', '\n', value)
    return value.strip()


def extract_questions(year: int, level: str) -> dict[int, dict[str, Any]]:
    paged = paper_text(paper_path(year, level), year)
    if year <= 2022:
        pattern = re.compile(r'(?m)^\s*(\d{1,2})\.\s+')
    else:
        pattern = re.compile(r'(?mi)^\s*Question\s+(\d{1,2})\b\s*')
    matches = list(pattern.finditer(paged.text))
    numbers = [int(match.group(1)) for match in matches]
    expected = expected_numbers(year, level)
    if numbers != expected:
        raise AssertionError(
            f'{year} {level}: paper questions {numbers}, expected {expected}')

    out: dict[int, dict[str, Any]] = {}
    for index, match in enumerate(matches):
        number = int(match.group(1))
        end = matches[index + 1].start() if index + 1 < len(matches) else len(paged.text)
        prompt = clean_prompt(paged.text[match.end():end])
        if len(prompt) < 20:
            raise AssertionError(f'{year} {level} Q{number}: implausibly short prompt {prompt!r}')
        out[number] = {
            'questionText': prompt,
            # `^\s*` may begin in the blank space at the end of the preceding
            # PDF page.  The end of the heading is unambiguously on this one.
            'paperPage': paged.page_for(match.end()),
        }
    return out


def nonempty_cells(row: Iterable[Any]) -> list[str]:
    return [compact(str(cell)) for cell in row if cell is not None and compact(str(cell))]


def legacy_scheme(year: int, level: str) -> dict[int, dict[str, Any]]:
    document = fitz.open(scheme_path(year, level))
    found: dict[int, dict[str, Any]] = {}
    for page_number, page in enumerate(document, start=1):
        for table in page.find_tables().tables:
            rows = table.extract()
            if not rows:
                continue
            heading = ' '.join(nonempty_cells(rows[0]))
            match = re.search(r'Q\.(\d{1,2})\b', heading)
            if not match:
                continue
            number = int(match.group(1))
            criteria: list[dict[str, Any]] = []
            current: dict[str, Any] | None = None
            for row in rows[1:]:
                cells = list(row) + [None] * (4 - len(row))
                label = compact(str(cells[0] or ''))
                guidance = compact(str(cells[1] or ''))
                marks_text = compact(str(cells[2] or ''))
                note = compact(str(cells[3] or ''))
                if guidance.lower().startswith('total'):
                    continue
                if label:
                    if not re.fullmatch(r'[A-E]', label):
                        continue
                    current = {
                        'id': label.lower(),
                        'label': f'Part {label}',
                        'maxMarks': 0,
                        'permittedMarks': [],
                        'guidance': [],
                    }
                    criteria.append(current)
                if current is None or not guidance or not re.fullmatch(r'\d+', marks_text):
                    continue
                marks = int(marks_text)
                current['maxMarks'] += marks
                current['guidance'].append(guidance)
                if note:
                    current['guidance'].append(f'SEC note: {note}')
            for criterion in criteria:
                criterion['permittedMarks'] = list(range(criterion['maxMarks'] + 1))
            total = sum(criterion['maxMarks'] for criterion in criteria)
            if total != 50:
                raise AssertionError(
                    f'{year} {level} Q{number}: legacy scheme totals {total}, not 50')
            found[number] = {'schemePage': page_number, 'criteria': criteria}

    expected = expected_numbers(year, level)
    if sorted(found) != expected:
        raise AssertionError(
            f'{year} {level}: legacy scheme questions {sorted(found)}, expected {expected}')
    return found


def parse_range(value: str) -> list[int]:
    numbers = [int(number) for number in re.findall(r'\d+', value)]
    if len(numbers) == 1:
        return numbers
    if len(numbers) == 2:
        return list(range(numbers[0], numbers[1] + 1))
    raise AssertionError(f'cannot read Art descriptor range {value!r}')


def parse_short_table(table: Any) -> list[dict[str, Any]]:
    rows = table.extract()
    criteria: list[dict[str, Any]] = []
    for index, row in enumerate(rows):
        cells = nonempty_cells(row)
        if len(cells) != 1 or not re.search(r'\([ab]\)', cells[0], re.I):
            continue
        guidance = cells[0]
        band_header = nonempty_cells(rows[index + 1]) if index + 1 < len(rows) else []
        band_ranges = nonempty_cells(rows[index + 2]) if index + 2 < len(rows) else []
        marks_cell = next((cell for cell in band_header if re.search(r'\d+\s*Marks?', cell, re.I)), None)
        if marks_cell is None or len(band_ranges) < 3:
            raise AssertionError(f'incomplete Art short-answer descriptor table: {rows!r}')
        maximum = int(re.search(r'\d+', marks_cell).group())
        ranges = [parse_range(value) for value in band_ranges[:3]]
        if sorted({mark for band in ranges for mark in band}) != list(range(maximum + 1)):
            raise AssertionError(f'Art descriptor bands do not cover 0–{maximum}: {ranges}')
        letter = re.search(r'\(([ab])\)', guidance, re.I).group(1).lower()
        criteria.append({
            'id': letter,
            'label': f'Part ({letter})',
            'maxMarks': maximum,
            'permittedMarks': list(range(maximum + 1)),
            'guidance': [guidance],
            'bandMarks': {'low': ranges[0], 'moderate': ranges[1], 'high': ranges[2]},
        })
    if len(criteria) != 2 or sum(item['maxMarks'] for item in criteria) != 10:
        raise AssertionError(f'invalid Section A table: {criteria!r}')
    return criteria


def current_short_scheme(year: int, level: str) -> dict[int, dict[str, Any]]:
    document = fitz.open(scheme_path(year, level))
    found: dict[int, dict[str, Any]] = {}
    for page_number, page in enumerate(document, start=1):
        question_numbers = [int(number) for number in re.findall(
            r'(?mi)^\s*Question\s+(\d{1,2})\s*$', clean_unicode(page.get_text('text', sort=True)))]
        question_numbers = [number for number in question_numbers if 1 <= number <= 7]
        if not question_numbers:
            continue
        candidate_tables = []
        for table in page.find_tables().tables:
            rows = table.extract()
            flattened = '\n'.join(cell for row in rows for cell in nonempty_cells(row))
            if re.search(r'\([ab]\)', flattened, re.M) and 'Low' in flattened and 'High' in flattened:
                candidate_tables.append(table)
        if len(candidate_tables) != len(question_numbers):
            raise AssertionError(
                f'{year} {level} scheme p.{page_number}: {question_numbers} but '
                f'{len(candidate_tables)} short-answer tables')
        for number, table in zip(question_numbers, candidate_tables):
            found[number] = {
                'schemePage': page_number,
                'criteria': parse_short_table(table),
            }
    if sorted(found) != list(range(1, 8)):
        raise AssertionError(
            f'{year} {level}: Section A scheme questions {sorted(found)}, expected 1–7')
    return found


def section_for(year: int, number: int) -> str:
    if year <= 2022:
        if number <= 7:
            return '1'
        if number <= 15:
            return '2'
        return '3'
    if number <= 7:
        return 'A'
    if number <= 13:
        return 'B'
    return 'C'


def topic_for(year: int, level: str, number: int, prompt: str) -> str:
    if year >= 2023 and number >= 8:
        return LONG_TOPIC[number]
    if year >= 2023:
        return CURRENT_SHORT_TOPICS[(year, level, number)]
    override = LEGACY_TOPIC_OVERRIDES.get((year, level, number))
    if override:
        return override
    text = comparable(prompt)
    if year <= 2022 and number <= 7:
        for topic, keywords in LEGACY_IRISH_TOPIC_KEYWORDS:
            if any(comparable(keyword) in text for keyword in keywords):
                return topic
        return 'art-5-4'
    if year <= 2022 and number <= 15:
        matches = [topic for topic, keywords in EUROPE_TOPIC_KEYWORDS
                   if any(comparable(keyword) in text for keyword in keywords)]
        return matches[0] if len(set(matches)) == 1 else 'art-4-6'
    for topic, keywords in TODAYS_WORLD_TOPIC_KEYWORDS:
        if any(comparable(keyword) in text for keyword in keywords):
            return topic
    return 'art-6-4'


def task_requirements(prompt: str) -> list[str]:
    """Lift the paper's own asks into a no-marks task checklist."""
    lines = prompt.splitlines()
    requirement_bullets = [
        compact(line[2:]) for line in lines
        if line.startswith('• ') and re.match(
            r'^(?:Refer|Include|Discuss|Describe|Give|Use|Name|Compare|Explain)\b',
            compact(line[2:]), re.I)
    ]
    if requirement_bullets:
        lead = compact(' '.join(line for line in lines if not line.startswith('• ')))
        return [lead, *requirement_bullets]

    # Choice lists (artists, movements, buildings) belong inside their parent
    # requirement. They are not eight separate boxes a student must tick.
    text = prompt.replace('\n• ', '; ')
    part_matches = list(re.finditer(r'(?m)^\([abc]\)\s+', text, re.I))
    if part_matches:
        requirements: list[str] = []
        preamble = compact(text[:part_matches[0].start()])
        # Keep a substantive instruction before (a), but not a contextual claim.
        if re.match(r'^(?:Answer|Choose|Name|Identify)\b', preamble, re.I):
            requirements.append(preamble)
        for index, match in enumerate(part_matches):
            end = part_matches[index + 1].start() if index + 1 < len(part_matches) else len(text)
            requirements.append(compact(text[match.start():end]))
        return [item for item in requirements if item]

    chunks = [compact(chunk) for chunk in text.split('\n') if compact(chunk)]
    if len(chunks) > 1:
        return [re.sub(r'^and\s+', '', chunk, flags=re.I) for chunk in chunks]

    # Legacy questions use a standalone "and" between compulsory parts.
    chunks = [compact(chunk) for chunk in re.split(
        r'\s+and\s+(?=(?:Briefly|Outline|Illustrate|Name|Describe|Discuss))',
        prompt, flags=re.I) if compact(chunk)]
    return [re.sub(r'^and\s+', '', chunk, flags=re.I) for chunk in chunks]


def select_printed_choice(prompt: str, choices: tuple[tuple[str, str], ...],
                          selected: str) -> str:
    """Keep one fixed SEC bullet choice while preserving its printed task.

    The final bullet often continues straight into the instruction (for example
    ``Alice Maher ... Describe and discuss``).  Its suffix therefore belongs to
    every selected variant, not only to the final option in the source list.
    """
    labels = [label for _, label in choices]
    lines = prompt.splitlines()
    matched: list[tuple[int, str]] = []
    for index, line in enumerate(lines):
        if not line.startswith('• '):
            continue
        body = line[2:]
        label = next((candidate for candidate in labels if body.startswith(candidate)), None)
        if label is not None:
            matched.append((index, label))
    # The 2025 HL Modernism alternatives are printed inline rather than as a
    # bullet list. Turn that one printed choice into an explicit standalone
    # practice prompt while retaining every following instruction verbatim.
    if not matched:
        inline = ', '.join(labels[:-1]) + f', {labels[-1]}'
        marker = f'one of the following: {inline}'
        if marker in prompt:
            return prompt.replace(marker, selected, 1)
        return prompt
    if [label for _, label in matched] != labels:
        raise AssertionError(f'printed Art choices do not match paper text: {labels!r}')
    first, last = matched[0][0], matched[-1][0]
    last_body = lines[last][2:]
    tail = last_body[len(labels[-1]):]
    selected_line = f'• {selected}{tail}'
    return '\n'.join([*lines[:first], selected_line, *lines[last + 1:]]).strip()


def task_combination_variants(year: int, level: str, number: int,
                              suffix: str) -> tuple[tuple[str, str], ...]:
    """Return every printed choose-N combination for one marked task."""
    spec = TASK_COMBINATION_CHOICES.get((year, level, number, suffix))
    if spec is None:
        return ()
    choose, items = spec
    if choose <= 0 or choose > len(items):
        raise AssertionError(
            f'{year} {level} Q{number}({suffix}): invalid choose-{choose} pool')
    return tuple(
        ('-'.join(slug for slug, _ in selected),
         ' and '.join(label for _, label in selected))
        for selected in itertools.combinations(items, choose)
    )


def select_task_combination(prompt: str, selected: str) -> str:
    """Make one finite heading combination explicit in the printed task."""
    marker = re.compile(
        r'using any two of the following headings:\s*'
        r'colour,\s*texture,\s*line,\s*pattern,\s*shape', re.I)
    replacement = f'using the following two printed headings: {selected}'
    revised, count = marker.subn(replacement, prompt, count=1)
    if count != 1:
        raise AssertionError(
            f'closed Art task combination did not match paper text: {prompt!r}')
    return revised


def audit_closed_choice_directives(year: int, level: str,
                                   questions: dict[int, dict[str, Any]]) -> None:
    """Fail if a finite printed choice pool has not been classified.

    Counts and hand-written choice maps can agree while both omit the same
    directive. This check starts from the raw extracted paper wording and makes
    every choose-one, choose-N or non-enumerable closed pool explicit.
    """
    seen_choose_one: set[tuple[int, str, int]] = set()
    seen_non_enumerable: set[tuple[int, str, int]] = set()
    seen_open_selection: set[tuple[int, str, int]] = set()
    seen_combinations: set[tuple[int, str, int, str]] = set()
    for number, question in questions.items():
        prompt = question['questionText']
        outer_key = (year, level, number)
        choose_one = re.search(r'\bone of the following\b', prompt, re.I)
        if choose_one and outer_key not in PRINTED_CHOICES:
            raise AssertionError(
                f'{year} {level} Q{number}: unreviewed choose-one directive')
        if choose_one:
            seen_choose_one.add(outer_key)

        if re.search(r'any two of the following', prompt, re.I):
            units = split_printed_tasks(prompt)
            matching = [unit for unit in units
                        if re.search(r'any two of the following', unit['questionText'], re.I)]
            if len(matching) != 1:
                raise AssertionError(
                    f'{year} {level} Q{number}: choose-two directive has no unique task')
            key = (*outer_key, matching[0]['suffix'])
            if key not in TASK_COMBINATION_CHOICES:
                raise AssertionError(
                    f'{year} {level} Q{number}: unreviewed choose-two directive')
            seen_combinations.add(key)

        # "Any of" without a number is not automatically a choose-one pool.
        # It must either be expanded above or carry a reviewed explanation.
        if re.search(r'\bany of the following\b', prompt, re.I):
            if outer_key not in REVIEWED_NON_ENUMERABLE_POOLS:
                raise AssertionError(
                f'{year} {level} Q{number}: unreviewed any-of directive')
            seen_non_enumerable.add(outer_key)

        # Catch selection language beyond the three known closed-list forms.
        # A question is classified if it is expanded at the outer level, has
        # a task-level combination, or carries a reviewed open-choice reason.
        if re.search(
                r'\b(?:choose|select|either|any\s+(?:one|two|three|four|five|six|seven|eight|nine|ten)'
                r'|answer\s+\w+\s+of)\b', prompt, re.I):
            has_task_combination = any(
                key[:3] == outer_key for key in TASK_COMBINATION_CHOICES)
            if (outer_key not in PRINTED_CHOICES
                    and not has_task_combination
                    and outer_key not in REVIEWED_OPEN_SELECTIONS):
                raise AssertionError(
                    f'{year} {level} Q{number}: unreviewed selection directive')
            if outer_key in REVIEWED_OPEN_SELECTIONS:
                seen_open_selection.add(outer_key)

    expected_choose_one = {
        key for key in PRINTED_CHOICES if key[:2] == (year, level)
    }
    if seen_choose_one != expected_choose_one:
        raise AssertionError(
            f'{year} {level}: stale choose-one review keys '
            f'{sorted(expected_choose_one - seen_choose_one)!r}')
    expected_combinations = {
        key for key in TASK_COMBINATION_CHOICES if key[:2] == (year, level)
    }
    if seen_combinations != expected_combinations:
        raise AssertionError(
            f'{year} {level}: stale task-combination review keys '
            f'{sorted(expected_combinations - seen_combinations)!r}')
    expected_non_enumerable = {
        key for key in REVIEWED_NON_ENUMERABLE_POOLS if key[:2] == (year, level)
    }
    if seen_non_enumerable != expected_non_enumerable:
        raise AssertionError(
            f'{year} {level}: stale non-enumerable review keys '
            f'{sorted(expected_non_enumerable - seen_non_enumerable)!r}')
    expected_open = {
        key for key in REVIEWED_OPEN_SELECTIONS if key[:2] == (year, level)
    }
    if seen_open_selection != expected_open:
        raise AssertionError(
            f'{year} {level}: stale open-selection review keys '
            f'{sorted(expected_open - seen_open_selection)!r}')


def meaningful_preamble(value: str) -> str | None:
    """Retain artwork/context prose but drop a bare ``Answer (a)…`` direction."""
    value = value.strip()
    value = re.sub(
        r'(?i)(?:^|\s+)Answer\s+\(a\)'
        r'(?:\s*,?\s*(?:and\s*)?\(b\))?'
        r'(?:\s*,?\s*(?:and\s*)?\(c\))?'
        r'\.?\s*$',
        '', value).strip()
    return value or None


def split_printed_tasks(prompt: str) -> list[dict[str, Any]]:
    """Split only task boundaries the paper itself prints.

    Lettered parts are independent cards.  On the outgoing paper a standalone
    line containing ``and`` separates two separately marked tasks.  Ordinary
    conjunctions inside a sentence never trigger a split.
    """
    parts = list(re.finditer(r'(?m)^\(([abc])\)\s+', prompt, re.I))
    if parts:
        preamble = meaningful_preamble(prompt[:parts[0].start()])
        return [{
            'suffix': match.group(1).lower(),
            'reference': f'({match.group(1).lower()})',
            'stem': preamble,
            'questionText': prompt[
                match.start():parts[index + 1].start() if index + 1 < len(parts) else len(prompt)
            ].strip(),
        } for index, match in enumerate(parts)]

    linked = re.split(r'(?mi)^\s*and\s+', prompt, maxsplit=1)
    if len(linked) == 2:
        first, second = (chunk.strip() for chunk in linked)
        return [
            {
                'suffix': 'task1',
                'reference': ' · task 1',
                'stem': None,
                'questionText': first,
            },
            {
                'suffix': 'task2',
                'reference': ' · task 2',
                # Exact context from the paper keeps "same period/artist" and
                # similar references meaningful on a standalone review card.
                'stem': first,
                'questionText': second,
            },
        ]

    return [{
        'suffix': 'response',
        'reference': '',
        'stem': None,
        'questionText': prompt.strip(),
    }]


def legacy_criterion_groups(criteria: list[dict[str, Any]],
                            unit_count: int) -> list[list[dict[str, Any]]]:
    """Map the outgoing scheme's named components to printed task boundaries.

    The final component is the sketches allocation and travels with the final
    printed task, where ``Illustrate your answer`` appears.  Multi-component
    first tasks (for example statement + two monuments) remain one card because
    those components mark one continuous printed directive.
    """
    shape = (unit_count, len(criteria))
    boundaries = {
        (1, 4): ((0, 4),),
        (2, 3): ((0, 1), (1, 3)),
        (2, 4): ((0, 2), (2, 4)),
        (2, 5): ((0, 3), (3, 5)),
        (3, 4): ((0, 1), (1, 2), (2, 4)),
    }.get(shape)
    if boundaries is None:
        raise AssertionError(f'unmapped legacy Art task/criterion shape {shape}')
    return [criteria[start:end] for start, end in boundaries]


def compact_requirement(question_text: str) -> str:
    return compact(question_text.replace('\n• ', '; '))


def source_material(year: int, level: str, number: int) -> dict[str, Any] | None:
    page = ILLUSTRATION_PAGES.get((year, level), {}).get(number)
    if page is None:
        return None
    return {
        'kind': 'source-illustration',
        'label': f'ILLUSTRATION SHEET · Q{number}',
        'title': f'Official illustrations for Question {number}',
        'pages': [page],
        'sourceFileid': illustration_fileid(level),
        'attribution': (
            'Official State Examinations Commission illustration sheet; '
            'individual artwork credits are printed on the sheet.'),
        'presentationNote': (
            f'Official {year} SEC examination layout, reproduced page-for-page.'),
    }


def make_outer_card(year: int, level: str, number: int, prompt: dict[str, Any],
                    scheme: dict[str, Any] | None) -> dict[str, Any]:
    current_long = year >= 2023 and number >= 8
    total_marks = 10 if year >= 2023 and number <= 7 else 50
    section = section_for(year, number)
    ref = f'{year} {LEVEL_REF[level]} Q{number}'
    card_id = f'art-{year}-{LEVEL_SHORT[level]}-q{number}'

    if current_long:
        criteria: list[dict[str, Any]] | None = None
        scheme_page: int | list[int] = [22, 23, 24, 25]
    else:
        if scheme is None:
            raise AssertionError(f'{ref}: missing question-specific scheme')
        criteria = scheme['criteria']
        scheme_page = scheme['schemePage']

    source = source_material(year, level, number)
    card: dict[str, Any] = {
        'id': card_id,
        'year': year,
        'level': level,
        'section': section,
        'questionRef': ref,
        'questionText': prompt['questionText'],
        'paperPage': prompt['paperPage'],
        'paperFileid': paper_fileid(level),
        'totalMarks': total_marks,
        'schemePage': scheme_page,
        'topicId': topic_for(year, level, number, prompt['questionText']),
        'conceptId': f'art-{year}-q{number}-{LEVEL_SHORT[level]}',
        'taskRequirements': task_requirements(prompt['questionText']),
        'assessment': (
            'current-long-descriptors' if current_long
            else 'current-short-descriptors' if year >= 2023
            else 'legacy-components'),
    }
    if criteria is not None:
        card['criteria'] = criteria
    if source is not None:
        card['sourceMaterial'] = source
    return card


def expand_outer_card(outer: dict[str, Any]) -> list[dict[str, Any]]:
    """Expand one numbered question into every useful Mark Bank card."""
    year = outer['year']
    level = outer['level']
    number = int(re.search(r'q(\d+)$', outer['id']).group(1))
    choices = PRINTED_CHOICES.get((year, level, number), ())
    variants: tuple[tuple[str | None, str | None], ...] = (
        tuple((slug, label) for slug, label in choices)
        if choices else ((None, None),)
    )
    expanded: list[dict[str, Any]] = []

    for choice_slug, choice_label in variants:
        prompt = (select_printed_choice(outer['questionText'], choices, choice_label)
                  if choice_label else outer['questionText'])
        units = split_printed_tasks(prompt)
        if outer['assessment'] == 'current-long-descriptors':
            if len(units) != 1:
                raise AssertionError(f"{outer['id']}: long Art essay unexpectedly split")
            criterion_groups: list[list[dict[str, Any]] | None] = [None]
        elif outer['assessment'] == 'current-short-descriptors':
            if len(units) != 2 or len(outer['criteria']) != 2:
                raise AssertionError(f"{outer['id']}: Section A must split into (a) and (b)")
            criterion_groups = [[criterion] for criterion in outer['criteria']]
        else:
            criterion_groups = legacy_criterion_groups(outer['criteria'], len(units))

        if len(units) != len(criterion_groups):
            raise AssertionError(
                f"{outer['id']}: {len(units)} task units but "
                f"{len(criterion_groups)} criterion groups"
            )

        # Alternative choices are parallel ways to earn the question tariff;
        # they must not be added together as though the candidate answers all
        # routes. Verify the one-route tariff before expanding those routes.
        route_marks = sum(
            50 if criteria is None
            else sum(criterion['maxMarks'] for criterion in criteria)
            for criteria in criterion_groups
        )
        if route_marks != outer['totalMarks']:
            label = choice_label or 'only response route'
            raise AssertionError(
                f"{outer['id']} ({label}): split tariff is {route_marks}, "
                f"expected {outer['totalMarks']}")

        for unit, criteria in zip(units, criterion_groups):
            suffix = unit['suffix']
            task_choices = task_combination_variants(year, level, number, suffix)
            task_variants: tuple[tuple[str | None, str | None], ...] = (
                task_choices if task_choices else ((None, None),)
            )
            for task_slug, task_label in task_variants:
                task_variant_index = (
                    next(index for index, (slug, _) in enumerate(task_choices, start=1)
                         if slug == task_slug)
                    if task_slug else None
                )
                question_text = (
                    select_task_combination(unit['questionText'], task_label)
                    if task_label else unit['questionText']
                )
                suffix_parts: list[str] = []
                # Preserve the established id grammar: an unsplit fixed-choice
                # card uses the choice slug directly, while an unsplit current
                # long response keeps the numbered question's base id.
                if (suffix != 'response'
                        or (not choice_slug
                            and outer['assessment'] != 'current-long-descriptors')):
                    suffix_parts.append(suffix)
                if choice_slug:
                    suffix_parts.append(choice_slug)
                # The pre-expansion card id remains attached to the first
                # finite route so a completeness correction never deletes a
                # student's existing review history. Further routes get the
                # descriptive combination slug.
                if task_slug and task_variant_index != 1:
                    suffix_parts.append(task_slug)
                card_suffix = '-'.join(suffix_parts)
                card_id = (outer['id'] if not card_suffix
                           else f"{outer['id']}-{card_suffix}")

                stem_parts: list[str] = []
                stem = unit.get('stem')
                if choice_label and choice_label not in question_text:
                    # A fixed choice is the only context later parts need. Avoid
                    # repeating the whole choice list and its obsolete "answer
                    # (a), (b)…" direction above every standalone card.
                    stem_parts.append(f'Printed choice: {choice_label}')
                elif stem:
                    stem_parts.append(stem)

                reference = f"{outer['questionRef']}{unit['reference']}"
                if choice_slug:
                    choice_index = next(
                        index for index, (slug, _) in enumerate(choices, start=1)
                        if slug == choice_slug)
                    reference += f' · option {choice_index}'
                if task_slug:
                    reference += f' · heading pair {task_variant_index}'

                concept_suffixes = [suffix]
                if choice_slug:
                    concept_suffixes.append(choice_slug)
                if task_slug:
                    concept_suffixes.append(task_slug)
                card = {
                    **outer,
                    'id': card_id,
                    'questionRef': reference,
                    'questionText': question_text,
                    'conceptId': f"{outer['conceptId']}-{'-'.join(concept_suffixes)}",
                    'taskRequirements': [compact_requirement(question_text)],
                }
                if stem_parts:
                    card['stem'] = ' '.join(stem_parts)
                else:
                    card.pop('stem', None)
                if criteria is None:
                    card.pop('criteria', None)
                    card['totalMarks'] = 50
                else:
                    card['criteria'] = criteria
                    card['totalMarks'] = sum(
                        criterion['maxMarks'] for criterion in criteria)
                expanded.append(card)

    return expanded


def build() -> tuple[dict[str, Any], dict[str, Any]]:
    cards: list[dict[str, Any]] = []
    papers: list[dict[str, Any]] = []
    for year in YEARS:
        for level in LEVELS:
            questions = extract_questions(year, level)
            audit_closed_choice_directives(year, level, questions)
            schemes = (legacy_scheme(year, level) if year <= 2022
                       else current_short_scheme(year, level))
            paper_cards: list[dict[str, Any]] = []
            for number in expected_numbers(year, level):
                outer = make_outer_card(
                    year, level, number, questions[number], schemes.get(number))
                for card in expand_outer_card(outer):
                    cards.append(card)
                    paper_cards.append({
                        'number': number,
                        'cardId': card['id'],
                        'questionRef': card['questionRef'],
                        'section': card['section'],
                        'paperPage': card['paperPage'],
                        'totalMarks': card['totalMarks'],
                        'hasIllustration': 'sourceMaterial' in card,
                    })
            expected = EXPECTED_CARDS_BY_YEAR_LEVEL[(year, level)]
            if len(paper_cards) != expected:
                raise AssertionError(f'{year} {level}: built {len(paper_cards)}, expected {expected}')
            papers.append({
                'year': year,
                'level': level,
                'paperFileid': paper_fileid(level),
                'expectedCards': expected,
                'cards': paper_cards,
            })

    if len(cards) != 462 or len({card['id'] for card in cards}) != 462:
        raise AssertionError('Art corpus must contain exactly 462 unique cards')
    if sum(card['level'] == 'higher' for card in cards) != 222:
        raise AssertionError('Art Higher Level corpus must contain 222 cards')
    if sum(card['level'] == 'ordinary' for card in cards) != 240:
        raise AssertionError('Art Ordinary Level corpus must contain 240 cards')

    runtime = {
        'subjectId': 'art',
        'corpus': 'All separately marked written-examination tasks and finite printed routes, 2021–2025',
        'cardCount': 462,
        'cards': cards,
    }
    census = {
        'subjectId': 'art',
        'years': [2021, 2022, 2023, 2024, 2025],
        'levels': ['higher', 'ordinary'],
        'selectionUnit': (
            'One card per separately marked printed task; every fixed named choice and finite '
            'choose-N combination is expanded, while holistic Section B/C essays remain intact.'),
        'expectedCards': {'higher': 222, 'ordinary': 240, 'total': 462},
        'papers': papers,
    }
    return runtime, census


def encoded(value: dict[str, Any]) -> str:
    return json.dumps(value, ensure_ascii=False, indent=2) + '\n'


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    runtime, census = build()
    outputs = ((OUT, runtime), (CENSUS_OUT, census))
    if args.check:
        stale = []
        for path, value in outputs:
            if not os.path.exists(path) or open(path, encoding='utf-8').read() != encoded(value):
                stale.append(os.path.relpath(path, ROOT))
        if stale:
            print('Art generated files are stale: ' + ', '.join(stale), file=sys.stderr)
            return 1
        print('Art authoring check: 462/462 cards match the ten-paper task census.')
        return 0

    for path, value in outputs:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w', encoding='utf-8') as handle:
            handle.write(encoded(value))
    print('Art: authored 462 cards (222 Higher, 240 Ordinary); census 462/462.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
