"""Three Home Economics cards recovered from tables the flat extraction lost.

Each was held because the scheme prints its marking points in a table and the
markdown reads ACROSS the row, so a cell's text was never contiguous. The cells
were always recoverable -- PyMuPDF reads them with the columns intact -- and
append-scheme-tables.py now puts them in the scheme markdown, so they pass
provenance. Every option below is one cell, exactly as the SEC printed it.
"""
import json
import re
import sys
from pathlib import Path

import pymupdf

sys.path.insert(0, str(Path(__file__).resolve().parent))
from he_lib import anyN, card, emit

ROOT = Path(__file__).resolve().parents[3]
cards = []


def table(pdf: str, page_needle: str, cell_needle: str):
    """The first table on the page holding page_needle that contains cell_needle."""
    doc = pymupdf.open(ROOT / 'examiner-reports' / 'home-economics' / pdf)
    for page in doc:
        if page_needle not in page.get_text():
            continue
        for strategy in ('lines', 'text'):
            try:
                found = page.find_tables(strategy=strategy).tables
            except Exception:
                continue
            for t in found:
                data = t.extract()
                if any(cell_needle in (c or '') for row in data for c in row):
                    return [[re.sub(r'\s+', ' ', (c or '')).strip() for c in row] for row in data]
    raise SystemExit(f'table not found: {pdf} / {cell_needle}')


def column(data, idx, skip_header=True):
    return [row[idx] for row in (data[1:] if skip_header else data)
            if idx < len(row) and row[idx]]


# ── 2022 HL Q1(a)(ii) — floor covering and its properties ───────────────────
t = table('2022-marking-scheme.pdf', 'Floor covering', 'Tiles ceramic')
cards.append(card(
    'he-2022-hl-sc-q1aii-properties', 2022, 'higher', 'home-economics-3-4',
    'floor-covering-name-and-properties',
    '2022 HL Section C E1 Q1(a)(ii) - name and properties',
    'Name a suitable floor covering for a home office and give its properties.',
    'name 2 marks (graded 2:1:0); properties 3 points @ 2 marks (graded 2:0)', 8,
    [anyN('r-1', 'Name of the floor covering', 2, 1, 2, column(t, 0)[:14],
          'Name one, 2 marks. A home office is a room you sit and work in for hours, so warmth and '
          'quiet matter more than in a hall - carpet, cork and wood read better here than ceramic or '
          'stone, and the properties row has to agree with whatever you name.'),
     anyN('r-2', 'Properties of the floor covering', 6, 3, 2, column(t, 1)[:14],
          'Three properties at 2 marks each, graded 2:0 - all or nothing per property, so be specific. '
          'The options are listed in the same order as the coverings above, and the scheme gives both '
          'sides for most of them: hard-wearing and easy to clean, but cold underfoot and chips easily.')],
    'Fixed: naming is priced at 2 and the properties at 6. Both rows are the scheme\'s own table columns, '
    'in the same order, so the properties can be matched to the covering named.',
    stem='‘Working from home in separate home offices can improve work-life balance.’ (The Irish Times, 2021)',
    tariff_kind='fixed', section='C'))

# ── 2023 HL Q1(b)(i) — properties of light ──────────────────────────────────
t = table('2023-marking-scheme.pdf', 'Explanation', 'Reflected')
cards.append(card(
    'he-2023-hl-sc-q1bi', 2023, 'higher', 'home-economics-3-5',
    'properties-of-light-and-their-use',
    '2023 HL Section C E1 Q1(b)(i)',
    'Describe four properties of light and give an example of how each property is used in the home.',
    'name 4 @ 2 marks; description 4 @ 2 marks; example 4 @ 1 mark', 20,
    [anyN('r-1', 'Name of the property', 8, 4, 2, column(t, 0)[:14],
          'Four properties at 2 marks each. Five are offered and you need four, so the only one you can '
          'afford to leave out is the one you cannot explain.'),
     anyN('r-2', 'Description of the property', 8, 4, 2, column(t, 1)[:14],
          'Four descriptions at 2 marks each, listed in the same order as the names above. Each is one '
          'sentence of physics - light bounces, scatters, is absorbed, splits, or bends - and saying '
          'what the surface does to the ray is what earns the 2.'),
     anyN('r-3', 'Example of its use in the home', 4, 4, 1, column(t, 2)[:14],
          'Four examples at 1 mark each, graded on the example alone, and again in the same order. These '
          'are the cheapest marks in the question: a mirror, net curtains, dark painted walls, a '
          'chandelier, glass bricks.')],
    'Fixed: the scheme prices naming at 8, description at 8 and examples at 4. The three rows are the '
    'scheme\'s own table columns in the same order, so a property, its explanation and its example line up.',
    stem='‘Lighting can transform a room.’', tariff_kind='fixed', section='C'))

# ── 2025 HL Q3(a) — food poisoning bacteria ─────────────────────────────────
t = table('2025-marking-scheme.pdf', 'Salmonella', 'Listeria')
cards.append(card(
    'he-2025-hl-sb-q3a', 2025, 'higher', 'home-economics-0-4',
    'food-poisoning-bacteria',
    '2025 HL Section B Q3(a)',
    'Identify one food poisoning bacteria you have studied and, in relation to the bacteria identified, '
    'refer to: source; high risk foods; factors affecting growth; food poisoning symptoms.',
    'name 1 @ 2 marks; source 1 @ 2 marks; high risk foods 2 @ 2 marks; factors affecting growth '
    '3 @ 2 marks; symptoms 2 @ 2 marks (graded 2:1:0)', 18,
    [anyN('r-1', 'Name of the bacteria', 2, 1, 2, column(t, 0)[:14],
          'Name one, 2 marks. Five are offered and every later row must match the one you name, so pick '
          'the one you know the sources and symptoms for. Salmonella is the fullest in the scheme.'),
     anyN('r-2', 'Source', 2, 1, 2, column(t, 1)[:14],
          'One source at 2 marks, listed in the same order as the names above. Source is where the '
          'bacteria LIVES - intestines and excreta, soil, the nose and throat - not the food it ends up in.'),
     anyN('r-3', 'High risk foods', 4, 2, 2, column(t, 2)[:14],
          'Two foods at 2 marks each. High risk means moist, protein-rich and handled - raw or '
          'undercooked meat and poultry, unpasteurised dairy, cooked rice, sliced cold meats.'),
     anyN('r-4', 'Factors affecting growth', 6, 3, 2, column(t, 3)[:14],
          'Three factors at 2 marks each - the biggest row at 6 marks. The scheme sets them out under '
          'the same headings for every bacteria: food, temperature, moisture, pH, oxygen and time. Give '
          'the heading AND the value, not just the word.'),
     anyN('r-5', 'Food poisoning symptoms', 4, 2, 2, column(t, 4)[:14],
          'Two symptoms at 2 marks each. Diarrhoea, nausea and vomiting are common to all five, so they '
          'are always safe - the distinguishing ones are worth knowing, like the severe effects of '
          'Clostridium botulinum.')],
    'Fixed: the scheme prices five named strands at 2, 2, 4, 6 and 4. Every row is one column of the '
    'scheme\'s own table, in the same order, so all five can be matched to the bacteria named.',
    stem='‘Everyone has the right to safe food.’ (www.fsai.ie)',
    tariff_kind='fixed', section='B'))

emit(cards)
