#!/usr/bin/env python3
"""Reviewed 2011 Higher Paper 1 (Ceapadóireacht agus Léamhthuiscint): new cards, no legacy component.

Before 2012 the Higher listening test is a component of its own (irish_higher_2011_aural.py) and the reading comprehension
sits in Páipéar 1, so the 2011 Páipéar 1 (LC001ALP100IV, 170 marc) is Ceist 1 Ceapadóireacht 100 (one of A Aiste (a)–(c),
B Scéal (a)–(b), C Alt Nuachtáin / Irise (a)–(b), D Díospóireacht / Óráid (a)–(b)) and Ceist 2 Léamhthuiscint 70 (A
“Tamall ag múineadh na Gaeilge sa Pholainn” and B “Máire Mhic Róibín – Duine de Laochra na hÉireann”, 35 each: five
questions of (a) 3 and (b) 4). Paper PDF 1–8 (1 cover, 2 the Treoracha, 3 the composition titles, 4–5 passage A and its
questions, 6–7 passage B and its questions, 8 blank) and the Páipéar I pages of the combined LC001ALP000IV scheme (PDF 3–14)
reviewed on 2026-11-05. Counts are assertions, not corpus-completeness proof.

The composition is marked Ionramháil Ábhair 20 + Cumas Gaeilge 80 (PDF 3–5), as one unit, with an 80-mark grade table
(PDF 4) and a 20-mark band table (PDF 5); no Stíl mark, no S1–S4 grades and no page of short / off-title reductions.

The reading key (PDF 5–14) opens with its rules: every answer is Eolas + Ionramháil, “2 + 1 = 2 marc ar eolas cruinn + 1
marc ar ionramháil nó 2 + 0 … toisc go raibh an freagra ceart ach é tógtha díreach ón léamhthuiscint”, and a two-point
answer “4 marc ar an bhfreagra: 2 marc + 1 marc + 1 marc P1 + P2 + Ionramháil”. It then restates each part with its tariff
and its split, “(3 mharc) (2+1)”, “(4 mharc) (2+1+1)”, “Pointe amháin(2+1)”, “3 mharc gan ionramháil”, “(2+2) gan
ionramháil. (Eachtra=2 mharc) (Míniú=2 mharc)”, “(2+1+1) (Eachtra+Míniú+Ionramháil)”, and A 3(b) prints its own
“Dhá thréith =1+1 (gan ionramháil) 2 mharc gan ionramháil=céard is bun leis na tréithe”. Under each it prints the answers
quoted from the passage, then the same answers in other words, and some partial or refused answers at a price (“= 3 - 1 =
2 mharc”, “= 1 + 1 = 2 mharc”, “= 0”). Each term of a part's split is a criterion of its own (Eolas, P1 + P2, Ionramháil,
Eachtra, Míniú, the two traits and what underlies them), its guidance the restated part and the key's lines for that term,
one to a line (answers.ts reads them: the quoted answers are rows, the reworded ones samples). The passage's Gaeilge
deduction (“[Gaeilge lochtach: 0 - 3 a bhaint den iomlán a gnóthaíodh.]”, E(35) − Gge.(0-3)) applies once to each
passage's total and is carried in the card notes, never as a criterion of one part.

Cards: the 20 printed reading parts (R-A-1-a … R-B-5-b), the 10 printed reading questions whole (R-A-1 … R-B-5, each
part's criteria together), and one 100-mark card per printed composition title (W-A-a … W-D-b).

Glyph repair (read from the font of every span and the rendered page, not guessed): the scheme's Ábhar band table on PDF 5
draws its first band “Ionramháil an-mhaith ar fad → sármhaith” with Wingdings-Regular U+F0E0, read as “→”; its rule bullets
on PDF 5, 6, 10 and 14 are SymbolMT U+F0B7 (•); the aural tariffs on PDF 20 draw × with SymbolMT U+F0B4. The paper's boxed
section headings on pages 3, 4 and 6 are flanked by SymbolMT dashes (U+F02D); no card or selection line reads them. Passage
pages 4–7 set two columns whose text layer interleaves glyph runs; the paper's lines are read from each glyph's position
(irish_foundation_2011.spatial_text). `main` writes components/MarkBank/cards/irish/higher-2011-p1-authored.json with its
review record, and the searchable scheme text examiner-reports/irish/schemes/2011-hl.md.
"""
from __future__ import annotations
import argparse
import collections
import hashlib
import json
import re
from pathlib import Path
from irish_lifted import scheme_words_in, symbol_text
from irish_foundation_2011 import spatial_text

ROOT = Path(__file__).resolve().parents[3]
FILE = 'LC001ALP100IV'
SCHEME_FILE = 'LC001ALP000IV'
OUT = ROOT / 'components/MarkBank/cards/irish/higher-2011-p1-authored.json'
SCHEME_MD = ROOT / 'examiner-reports/irish/schemes/2011-hl.md'
SOURCE_REVIEW = ROOT / 'scripts/markbank/authored/irish-higher-2011-p1-source-review.json'
REVIEWED_AT = '2026-11-05'
PAPER_SHA = '210ba6909b768d0b1970cc6bee72d8ca53197bf76919280d238b95e61df76691'
SCHEME_SHA = 'b5f7c77e673759308a08e4a8cdef08000045789921a3c64278c739bb510783b0'
DIRECTIVE = re.compile(r'rogha|roghna|Freagair|Cuir tic|Ainmnigh|Luaigh|\bchoose\b|\beither\b|\bany\b|one of|\bnó\b|dhá phointe|trí phointe|'
                       r'dhá rud|dó/di|Cuir ciorcal|dhá thagairt|dhá ch|dhá dh|an dá|ceann amháin|amháin|\bdhá\b', re.I)
SOURCE_NOTE = 'Shown page-for-page from the official examination paper; swipe to move between pages.'
# Glyphs the text layer mis-decodes, keyed by (font, character) and read from the rendered page.
GLYPHS = {('Wingdings-Regular', ''): '→', ('SymbolMT', ''): '×'}
SCHEME_GLYPHS = {(5, 'SymbolMT', ''): 5, (5, 'Wingdings-Regular', ''): 1, (6, 'SymbolMT', ''): 3,
                 (10, 'SymbolMT', ''): 2, (14, 'SymbolMT', ''): 1, (20, 'SymbolMT', ''): 9, (24, 'SymbolMT', ''): 3}
PAPER_GLYPHS = {(3, 'SymbolMT', ''): 8, (4, 'SymbolMT', ''): 1, (6, 'SymbolMT', ''): 1}
GAEILGE_DEDUCTION = '[Gaeilge lochtach: 0 - 3 a bhaint den iomlán a gnóthaíodh.]'


def clean(text):
    return re.sub(r'\s+', ' ', symbol_text(text)).strip()


def comparable(text):
    return re.sub(r'[^\w]+', '', text.lower())


def criterion(id, label, marks, guidance, kind='quality', permitted=None):
    return dict(id=id, label=label, kind='award', maxMarks=marks,
                permittedMarks=permitted if permitted is not None else list(range(marks + 1)), guidanceKind=kind, guidance=guidance)


def source(ref, title, pages):
    return dict(kind='source-text', label=ref, title=title, pages=pages, attribution='© State Examinations Commission.',
                presentationNote=SOURCE_NOTE)


def selection_decisions(paper):
    decisions = json.loads(SOURCE_REVIEW.read_text())['selectionDecisions']
    expected = {(d['page'], d['raw']) for d in decisions}
    found = {(i, clean(line)) for i, page in enumerate(paper, 1)
             for line in spatial_text(page).splitlines() if DIRECTIVE.search(clean(line))}
    assert found == expected, ('Unclassified/stale selection directives', found - expected, expected - found)
    return decisions


def symbol_audit(doc):
    audit = collections.Counter()
    for number, page in enumerate(doc, 1):
        for block in page.get_text('rawdict')['blocks']:
            for line in block.get('lines', []):
                for span in line['spans']:
                    if span['font'].startswith(('Symbol', 'Wingdings')):
                        for char in span['chars']:
                            audit[(number, span['font'], char['c'])] += 1
    return dict(audit)


def scheme_pages(doc):
    """Each scheme page's text with the audited glyph repairs applied, span by span."""
    pages = []
    for page in doc:
        lines = []
        for block in page.get_text('rawdict')['blocks']:
            for line in block.get('lines', []):
                lines.append(''.join(GLYPHS.get((span['font'], char['c']), char['c']) for span in line['spans'] for char in span['chars']))
        pages.append('\n'.join(lines))
    return pages


class Marked:
    """Scheme text across pages with page markers, so each slice knows its pages."""

    def __init__(self, stext, first, last):
        self.text = ''
        for p in range(first, last + 1):
            self.text += f' ⟦{p}⟧ ' + re.sub(r'^\d+\s', '', stext[p - 1])

    def chunk(self, start, end, after=0):
        a = self.text.index(start, after)
        b = self.text.index(end, a + len(start))
        raw = self.text[a:b]
        pages = {int(re.findall(r'⟦(\d+)⟧', self.text[:a])[-1])}
        pages |= {int(m.group(1)) for m in re.finditer(r'⟦(\d+)⟧([^⟦]*)', raw) if clean(m.group(2))}
        return clean(re.sub(r'⟦\d+⟧', ' ', raw)), sorted(pages), b


def cut(chunk, anchors):
    """The restated part, then one line per anchor in print order; together they are the chunk, word for word."""
    starts, pos = [], 0
    for anchor in anchors:
        pos = chunk.index(anchor, pos + (1 if starts else 0))
        starts.append(pos)
    header = chunk[:starts[0]].strip()
    lines = [chunk[a:b].strip() for a, b in zip(starts, starts[1:] + [len(chunk)])]
    assert ' '.join([header, *lines]) == chunk, (header[:40], anchors[:2])
    return header, lines


# The key's reading rules (scheme PDF 5–6), lifted for the Ionramháil criteria.
RULES = {
    'IONR': 'Is ionann “ionramháil” agus ceann de mhórfhocail an fhreagra a chur nó a mhíniú i bhfoca(i)l eile.',
    'IONR_NOT': 'Ní leor ord na bhfocal a chasadh timpeall chun an marc a ghnóthú ar ionramháil sa fhreagra ná ní leor “sé/sí/siad” a chur '
                'in ionad ainmfhocail.',
    'EOLAS': 'Eolas + Ionramháil: 2 + 1 = 2 marc ar eolas cruinn + 1 marc ar ionramháil nó 2 + 0 = 2 marc ar eolas cruinn + 0 ar '
             'ionramháil toisc go raibh an freagra ceart ach é tógtha díreach ón léamhthuiscint.',
    'TWO': '2 phointe eolais: ní lorgaítear ionramháil ach ar phointe eolais amháin. Má dhéantar ionramháil ar phointe eolais amháin '
           'bronn an marc ar an ionramháil.',
}
IONR = ['H', 'IONR', 'IONR_NOT', 'EOLAS']
IONR2 = IONR + ['TWO']

# Each printed part: (question, part, paper prompt, scheme anchor, line anchors, criteria). A criterion is (id, label, marks,
# permitted marks, the lines it carries: 'H' the restated part, an index into the part's lines, or a rule above).
A = [
    ('1', 'a', '(a) Cén taithí a bhí ag an údar ar an bPolainn? (Alt 1) (3 mharc)', '1 (a) Cén taithí',
     ['“go raibh mí caite', 'Chaith sé mí/tamall'],
     [('a-eolas', '(a) Eolas', 2, [0, 2], ['H', 0, 1]), ('a-ionramhail', '(a) Ionramháil', 1, [0, 1], IONR)]),
    ('1', 'b', '(b) Luaigh dhá bhuntáiste a bhainfeadh an t-údar as an bpost a bheith aige. (Alt 1) (4 mharc)', '1 (b) Luaigh dhá bhuntáiste',
     ['(i) “Tugadh', '(ii) “Bhí spéis', '(iii) “B’fhurasta', '(iv) “Chuirfinn', '(v) “D’fhoghlaimeoinn', '(vi) “Bheinn i mo chónaí',
      '(vii) “Bheinn neamhspleách', '(i) Fuair sé', '(ii) Thaitin', '(iii) Bheadh sé ábalta', '(iv) Bhlaisfeadh', '(v) D’fhoghlaimeodh',
      '(vi) Bheadh sé ina chónaí', '(vii) Bheadh sé saor'],
     [('b-pointi', '(b) P1 + P2', 3, [0, 2, 3], ['H', *range(14)]), ('b-ionramhail', '(b) Ionramháil', 1, [0, 1], IONR2)]),
    ('2', 'a', '(a) Cén fáth a bhfuil an Ghaeilge á múineadh in KUL? (Alt 2) (3 mharc)', '2 (a) Cén fáth a bhfuil',
     ['“Ag deireadh', 'Mar chuid de chéim', '“Bíonn ar na mic léinn', '(Ní mór tagairt'],
     [('a-eolas', '(a) Eolas', 2, [0, 2], ['H', 0, 1, 2, 3]), ('a-ionramhail', '(a) Ionramháil', 1, [0, 1], IONR)]),
    # The scheme restates 2(b) without "(Alt 2)"; the card shows the paper's question.
    ('2', 'b', '(b) Luaigh dhá dhearcadh atá ag na Polannaigh faoi fhoghlaim na Gaeilge. (Alt 2) (4 mharc)', '2 (b) Luaigh dhá dhearcadh',
     ['(i) “Cheap', '(ii) “Bhí daoine', '(iii) “daoine a dúirt', '(iv) “Le fírinne', '(v) “Is é an córas', '(i) Mheas', '(ii) Bhí mic léinn',
      '(iii) D’admhaigh', '(iv) Ceapann', '(v) Is é fuaimniú'],
     [('b-pointi', '(b) P1 + P2', 3, [0, 2, 3], ['H', *range(10)]), ('b-ionramhail', '(b) Ionramháil', 1, [0, 1], IONR2)]),
    ('3', 'a', '(a) Luaigh cosúlacht amháin idir Vársá agus Baile Átha Cliath. (Alt 3) (3 mharc)', '3 (a) Luaigh cosúlacht',
     ['(i) “Leagadh', '(Cáiliú amháin', '(Mura mbíonn', '“Leagadh formhór', '(ii) “Dála', '“Tá an-chuid', '“Tá “an oidhreacht'],
     [('a-eolas', '(a) Eolas', 3, [0, 3], ['H', *range(7)])]),
    # The scheme restates 3(b) as "muintir naPolainne" and prints no tariff after it; its own two headings price it.
    ('3', 'b', '(b) Luaigh dhá thréith a bhaineann le muintir na Polainne, agus luaigh céard is bun leis na tréithe sin, dar leis an údar. '
               '(Alt 3) (4 mharc)', '3 (b) Luaigh dhá thréith',
     ['Dhá thréith =1+1', '2 mharc gan ionramháil=', '“an cairdeas', 'Is dócha go bhfuil', '“an oidhreacht shaibhir Chríostaí”is bun'],
     [('b-treithe', '(b) Dhá thréith', 2, [0, 1, 2], ['H', 0, 2, 3]), ('b-bun', '(b) Céard is bun leis na tréithe', 2, [0, 2], [1, 4])]),
    ('4', 'a', '(a) Cá bhfuil cathair Lublin suite? (Alt 4) (3 mharc)', '4 (a) Cá bhfuil cathair',
     ['Tá Lublin “in oirthear', 'Tá Lublin sa Pholainn', 'Tá Lublin in oirthear na tíre'],
     [('a-eolas', '(a) Eolas', 3, [0, 2, 3], ['H', 0, 1, 2])]),
    # The scheme writes the Pope "Eoin Pól 11"; the card shows the paper's "Eoin Pól II".
    ('4', 'b', '(b) Luaigh dhá phointe eolais faoin bPápa Eoin Pól II. (Alt 4) (4 mharc)', '4 (b) Luaigh dhá phointe eolais faoin',
     ['(i) “Ba san ollscoil', '(ii) “Thug an Pápa', '(iii) “In Ollscoil', '(i) D’oibrigh', '(ii) Bhí sé ar thaobh', '(iii) Bhí sé ag obair'],
     [('b-pointi', '(b) P1 + P2', 3, [0, 2, 3], ['H', *range(6)]), ('b-ionramhail', '(b) Ionramháil', 1, [0, 1], IONR2)]),
    ('5', 'a', '(a) Cad a thug an t-údar faoi deara faoi iompar na ndéagóirí ar an tsráid? (Alt 5) (3 mharc)', '5 (a) Cad a thug an t-údar',
     ['(i) “Bíonn siad an-chiúin', '(ii) “Bíonn siad ag cogarnaíl', '(iii) “Bíonn siad an-aireach', '(i) Fanann', '(ii) Labhrann',
      '(iii) Bíonn siad an-chúramach'],
     [('a-eolas', '(a) Eolas', 2, [0, 2], ['H', *range(6)]), ('a-ionramhail', '(a) Ionramháil', 1, [0, 1], IONR)]),
    ('5', 'b', '(b) Cad a tharla san ollmhargadh lá agus cén míniú a fuair an t-údar ar an eachtra? (Alt 5) (4 mharc)',
     '5 (b) Cad a tharla san ollmhargadh',
     ['(Eachtra=2 mharc)', '(Míniú=2 mharc)', '“Chonaic mé bean', 'Dhá chuid san eachtra:', '“Ghéill sé slí', 'Iompar na mná',
      'Míniú: Pointe eolais', '(i) “ré an chumannachais” agus “ciúnna', '(ii) “ré an chumannachais” agus “riachtanais', '(iii) “ciúnna fada',
      'Gan an eachtra cheart'],
     [('b-eachtra', '(b) Eachtra', 2, [0, 1, 2], ['H', 0, 2, 3, 4, 5]), ('b-miniu', '(b) Míniú', 2, [0, 1, 2], [1, 6, 7, 8, 9, 10])]),
]
B = [
    # The scheme restates 1(a) "Cé a bheidh …"; the card shows the paper's "Cé a bheadh".
    ('1', 'a', '(a) Cé a bheadh i dteideal an ghradaim An Phearsa is Mó i Stair na hÉireann? (Alt 1) (3 mharc)', '1 (a) Cé a bheidh',
     ['“James Connolly', '(tá gá leis', 'Níos lú ná cúigear'],
     [('a-eolas', '(a) Eolas', 3, [0, 1, 3], ['H', 0, 1, 2])]),
    ('1', 'b', '(b) Luaigh eachtra amháin óna tréimhse mar Uachtarán a bhfuil cuimhne air agus cén míniú a bhí ag an údar ar a himeacht ó '
               'chuimhne daoine? (Alt 1) (4 mharc)', '1 (b) Luaigh eachtra amháin',
     ['(i) “Tá cuimhne ar fud', '(ii) “Tá caint go fóill', '(i) Chuaigh sí', '(ii) Thosaigh Máire', '“Tá cuimhne ar fud', '“Tá cuimhne ar fud',
      '“Tá cuimhne ar fud', '“Tá cuimhne ar fud', '“Tá caint go fóill', 'Míniú = 1 mharc', '“Ní raibh Máire Mhic Róibín sa nuacht in Éirinn',
      '“Ní raibh Máire Mhic Róibín sa nuacht” =', '“D’éirigh sí as', 'Tá sí “i mbun dualgais mar', 'Tá sí “i mbun dualgais leis', 'Níor luadh'],
     [('b-eachtra', '(b) Eachtra', 2, [0, 2], ['H', *range(9)]), ('b-miniu', '(b) Míniú', 1, [0, 1], list(range(9, 16))),
      ('b-ionramhail', '(b) Ionramháil', 1, [0, 1], IONR2)]),
    # The scheme restates 2(a) with "David McWilliams"; the card shows the paper's "David Mc Williams".
    ('2', 'a', '(a) Cén rud faoi Mháire Mhic Róibín is mó a thug clár David Mc Williams chun cuimhne fúithi? (Alt 2) (3 mharc)',
     '2 (a) Cén rud faoi Mháire', ['“Chuir David', 'D’oibrigh sí ar feadh'],
     [('a-eolas', '(a) Eolas', 2, [0, 2], ['H', 0, 1]), ('a-ionramhail', '(a) Ionramháil', 1, [0, 1], IONR)]),
    ('2', 'b', '(b) Luaigh cúis aighnis a bhí ag Máire (i) lena tuismitheoirí; (ii) le Bardas Bhaile Átha Cliath. (Alt 2) (4 mharc)',
     '2 (b) Luaigh cúis aighnis', ['(i) “Phós sí', '(ii) Bhí sí “i gcoimhlint', '(i) Ba Phrotastúnach', '(ii) Throid sí'],
     [('b-pointi', '(b) P1 + P2', 3, [0, 2, 3], ['H', *range(4)]), ('b-ionramhail', '(b) Ionramháil', 1, [0, 1], IONR2)]),
    ('3', 'a', '(a) Conas a d’athraigh Máire Mhic Róibín stair an dlí in Éirinn? (Alt 3) (3 mharc)', '3 (a) Conas a d’athraigh',
     ['“Chuir Máire'], [('a-eolas', '(a) Eolas', 3, [0, 3], ['H', 0])]),
    ('3', 'b', '(b) Luaigh dhá shampla de na cearta a bhuaigh Máire Mhic Róibín do mhná os comhair na gCúirteanna Eorpacha. (Alt 3) (4 mharc)',
     '3 (b) Luaigh dhá shampla de na cearta',
     ['(i) “Bhain sí amach', '(“Bhain sí amach', '(ii) “an ceart a bheith', '(i) Bhuaigh sí an ceart do mhná liúntais',
      '(ii) Bhuaigh sí an ceart do mhná a bheith'],
     [('b-pointi', '(b) P1 + P2', 3, [0, 2, 3], ['H', *range(5)]), ('b-ionramhail', '(b) Ionramháil', 1, [0, 1], IONR2)]),
    ('4', 'a', '(a) Cén fáth ar thairg Kofi Anann an post mar Ardchoimisinéir um Chearta Daonna do Mháire Mhic Róibín? (Alt 4) (3 mharc)',
     '4 (a) Cén fáth ar thairg', ['“Chreid Kofi', 'Cheap Kofi'],
     [('a-eolas', '(a) Eolas', 2, [0, 2], ['H', 0, 1]), ('a-ionramhail', '(a) Ionramháil', 1, [0, 1], IONR)]),
    ('4', 'b', '(b) Luaigh dhá shampla den chaoi ar thaispeáin Máire Mhic Róibín a neamhspleáchas mar Ardchoimisinéir um Chearta Daonna. '
               '(Alt 4) (4 mharc)', '4 (b) Luaigh dhá shampla den chaoi',
     ['(i) “Le linn cuairte', '(ii) “Is minic', '(iii) “Sa bhliain 2001', '(iv) “Cháin Máire', '(i) Nuair a bhí sí', '(ii) Rinne sí gearán',
      '(iii) Bhí sí i gceannas', '(iv) Labhair sí'],
     [('b-pointi', '(b) P1 + P2', 3, [0, 2, 3], ['H', *range(8)]), ('b-ionramhail', '(b) Ionramháil', 1, [0, 1], IONR2)]),
    ('5', 'a', '(a) Conas a léirigh an tUachtarán Obama a mheas ar Mháire Mhic Róibín? (Alt 5) (3 mharc)', '5 (a) Conas a léirigh',
     ['“Bhronn Barack Obama an gradam is airde i Meiriceá uirthi-Bonn', '“Bhronn Barack Obama an gradam is airde i Meiriceá uirthi” =',
      '“Bhronn Barack Obama Bonn', '“Sa bhliain 2007'],
     [('a-eolas', '(a) Eolas', 3, [0, 3], ['H', *range(4)])]),
    # The paper prints "(Dhá pointe)." (the scheme "(Dhá phointe)"); the card shows the paper's.
    ('5', 'b', '(b) Cén obair a bhíonn ar siúl ag Máire Mhic Róibín leis na Elders? (Dhá pointe). (Alt 5) (4 mharc)', '5 (b) Cén obair a bhíonn',
     ['(i) “Tá sé mar aidhm', '(ii) “Faoi láthair', '(i) Sé an cuspóir', '(ii) Anois, tá na Elders'],
     [('b-pointi', '(b) P1 + P2', 3, [0, 2, 3], ['H', *range(4)]), ('b-ionramhail', '(b) Ionramháil', 1, [0, 1], IONR2)]),
]
PASSAGES = {
    'A': dict(title='Tamall ag múineadh na Gaeilge sa Pholainn', pages=[4, 5], topic='irish-3-0', parts=A,
              start='Léamhthuiscint 2A', stop='• 10 bhfomharc le suimiú'),
    'B': dict(title='Máire Mhic Róibín – Duine de Laochra na hÉireann', pages=[6, 7], topic='irish-3-1', parts=B,
              start='Léamhthuiscint 2B', stop='• Suimigh an 10 bhfomharc'),
}


def material():
    """Lifted paper prompts and scheme text."""
    import fitz
    paper_path = ROOT / f'paper-trail-corpus/exampapers/2011/{FILE}.pdf'
    scheme_path = ROOT / f'paper-trail-corpus/markingschemes/2011/{SCHEME_FILE}.pdf'
    assert hashlib.sha256(paper_path.read_bytes()).hexdigest() == PAPER_SHA, 'Paper changed: repeat visual review'
    assert hashlib.sha256(scheme_path.read_bytes()).hexdigest() == SCHEME_SHA, 'Scheme changed: repeat visual review'
    paper, scheme = fitz.open(paper_path), fitz.open(scheme_path)
    assert symbol_audit(scheme) == SCHEME_GLYPHS and symbol_audit(paper) == PAPER_GLYPHS, 'Symbol glyphs changed: repeat the glyph review'
    texts = [clean(spatial_text(p)) for p in paper]
    raw = scheme_pages(scheme)
    stext = [clean(t) for t in raw]
    assert not any(re.search('[-]', t) for t in stext[:14]), 'Unrepaired glyph on Páipéar I'

    # ---- Composition (scheme PDF 3–5) ------------------------------------------------------------------------------------
    page3 = re.sub(r'^\d+\s', '', stext[2])
    assert page3.startswith('PÁIPÉAR I (170 marc) CEIST 1 - CEAPADÓIREACHT - 100 marc { (a) Ionramháil Ábhair = 20 marc } (b) Cumas Gaeilge = 80 marc'), page3[:140]
    note = page3[page3.index('Nóta: Caithfidh an Scrúdaitheoir'):page3.index('AN CHEAPADÓIREACHT')].strip()
    unit = page3[page3.index('Gnéithe a bhaineann leis an marcáil'):page3.index('Cumas Gaeilge (80marc)')].strip()
    gaeilge_text = page3[page3.index('Cumas Gaeilge (80marc)'):page3.index('20 + 80 = 100')].strip()
    table80 = re.sub(r'^\d+\s', '', stext[3])
    page5 = re.sub(r'^\d+\s', '', stext[4])
    abhar = page5[:page5.index('CEIST 2 - LÉAMHTHUISCINT')].strip()
    assert note.endswith('ag bun na hiarrachta ceapadóireachta.') and unit.endswith('mar aonad.'), (note[-60:], unit[-60:])
    assert gaeilge_text.endswith('mionbhotúin ghramadaí.'), gaeilge_text[-60:]
    assert all(x in table80 for x in ['76-80', '64-67', '52-55', '40-42', '28-31', '16-19', '4-7', '0-3']), table80[-80:]
    assert abhar.startswith('Ionramháil Ábhair = (20 marc)') and abhar.endswith('F/NG 0, 1, 2, 3, 4 marc'), abhar[-60:]
    assert all(x in abhar for x in ['→ sármhaith A 17, 18, 19, 20 marc', '14, 15, 16', '11, 12, 13', '8, 9, 10', '5, 6, 7'])
    # 2011 prints neither S1–S4 grades, a Stíl mark, a page of short / off-title reductions nor a modified marking scheme.
    assert not any(re.search(r'\bS[1-4]\b|róghearr|Easnamhach i gcás|Stíl|pro-rata', t) for t in stext[:14])
    assert not any('Mhodhnaithe' in t for t in stext)
    head = ('Treoracha d’iarrthóirí\n'
            'Ní mór do na hiarrthóirí cúram a dhéanamh de chruinneas na teanga. Caillfear marcanna má bhítear faillitheach ann.\n\n'
            'Ceist 1\nCEAPADÓIREACHT 100 MARC\nFreagair do rogha CEANN AMHÁIN de A, B, C nó D anseo thíos.\n'
            'Nóta: Is leor 500-600 focal mar fhreagra i gcás ar bith.')
    treoracha, choice = head.split('\n\n')
    assert all(comparable(line) in comparable(texts[1]) for line in treoracha.splitlines())
    assert all(comparable(line) in comparable(texts[2]) for line in choice.splitlines())
    groups = {
        'A': ('AISTE', 'Scríobh AISTE ar CHEANN AMHÁIN de na hábhair seo.', 'irish-2-0', [
            ('a', 'An caidreamh sóisialta in aois an idirlín.'), ('b', 'Cearta páistí.'), ('c', 'Ceannairí an phobail.')]),
        'B': ('SCÉAL', 'Ceap SCÉAL a mbeadh do rogha CEANN AMHÁIN díobh seo oiriúnach mar theideal air.', 'irish-2-3', [
            ('a', 'Dílseacht.'), ('b', 'Is fearr go mall ná go brách.')]),
        'C': ('ALT NUACHTÁIN / IRISE', 'Freagair do rogha CEANN AMHÁIN díobh seo.', 'irish-2-1', [
            ('a', 'Chuir tú agallamh ar dhaoine óga ó thíortha iasachta faoin saol a bhí acu le roinnt blianta anuas in Éirinn.\n'
                  'Scríobh alt, bunaithe ar an agallamh sin, d’iris na scoile.'),
            ('b', 'Tá comórtas i nuachtán Gaeilge ag lorg ailt ar an ábhar seo a leanas:\nMo rogha duine mar Uachtarán na hÉireann.\n'
                  'Scríobh an t-alt a chuirfeá isteach ar an gcomórtas.')]),
        'D': ('DÍOSPÓIREACHT / ÓRÁID', 'Freagair do rogha CEANN AMHÁIN díobh seo.', None, [
            ('a', 'Scríobh an chaint a dhéanfá i ndíospóireacht scoile ar son an rúin seo a leanas nó ina aghaidh:\n'
                  'Is deacair a bheith dóchasach as an todhchaí in Éirinn.'),
            ('b', 'Labhair tú le cumann carthanachta i do cheantar féin ar an ábhar thíos:\nDualgas an Stáit i leith ár seandaoine.\n'
                  'Scríobh an óráid a thug tú don chumann.')]),
    }
    for group, (form, instruction, _, titles) in groups.items():
        assert comparable(f'{group} {form} 100 marc') in comparable(texts[2]), group
        for letter, title in titles:
            assert all(comparable(line) in comparable(texts[2]) for line in [instruction, *title.splitlines()]), (group, letter)

    # ---- Reading (scheme PDF 5–14) ---------------------------------------------------------------------------------------
    key = Marked(stext, 5, 14)
    rules = {name: line for name, line in RULES.items()}
    rule_text = clean(re.sub(r'⟦\d+⟧', ' ', key.text[:key.text.index('A (35 mharc)')]))
    assert all(line in rule_text for line in rules.values()), [k for k, v in rules.items() if v not in rule_text]
    assert '4 marc ar an bhfreagra: 2 marc + 1 marc + 1 marc P1 + P2 + Ionramháil' in rule_text
    assert key.text.count(GAEILGE_DEDUCTION) == 2 and 'E(35) = Gge.(0-3) = -' in key.text
    assert comparable('Léigh an sliocht seo a leanas agus freagair na ceisteanna a ghabhann leis.') in comparable(texts[3])
    assert comparable('BÍODH NA FREAGRAÍ I D’FHOCAIL FÉIN, OIREAD AGUS IS FÉIDIR LEAT.') in comparable(texts[5])
    for letter, passage in PASSAGES.items():
        pages = passage['pages']
        assert comparable(passage['title']) in comparable(texts[pages[0] - 1]), letter
        questions = ' '.join(texts[p - 1] for p in pages)
        pos = key.text.index(passage['start'])
        anchors = [part[3] for part in passage['parts']]
        cuts = []
        for index, (q, p, prompt, anchor, line_anchors, crits) in enumerate(passage['parts']):
            assert comparable(f'{q} {prompt}' if p == 'a' else prompt) in comparable(questions), (letter, q, p)
            end = anchors[index + 1] if index + 1 < len(anchors) else passage['stop']
            chunk, spages, pos = key.chunk(anchor, end, pos)
            assert not re.search(r'Léamhthuiscint 2|E\(35\)|Suimigh|bhfomharc|Gaeilge lochtach', chunk), (letter, q, p, chunk[-60:])
            header, lines = cut(chunk, line_anchors)
            used = sorted(ref for *_, refs in crits for ref in refs if isinstance(ref, int))
            assert used == list(range(len(lines))), (letter, q, p, 'every line of the key goes to exactly one criterion')
            cuts.append((q, p, prompt, header, lines, spages, crits))
        passage['cuts'] = cuts
    decisions = selection_decisions(paper)
    return dict(decisions=decisions, head=head, groups=groups, rules=rules,
                composition=dict(note=note, unit=unit, gaeilge=[gaeilge_text, table80], abhar=abhar), raw=raw)


COMPOSITION_REASONS = {
    'A': 'Each printed essay title is a separate route.',
    'B': 'Each printed title is a separate route; the story itself is open.',
    'C': 'Each printed article task is a separate route.',
    'D': '“ar son … nó ina aghaidh” is the speaker’s stance inside one speech; both stances are marked identically.'}
SPLIT_NOTES = {
    'eolas-ionramhail': 'The key prices this part (2+1): Eolas 2 for the information and Ionramháil 1 for putting it in other words; an '
                        'answer lifted straight from the passage earns 2 + 0 (its rule, scheme PDF 5). Each is a criterion of this card.',
    'pointi-ionramhail': 'The key prices this part (2+1+1): P1 2 and P2 1 for two points and Ionramháil 1 on one of them (scheme PDF 6, '
                         '“2 marc + 1 marc + 1 marc P1 + P2 + Ionramháil”). Each is a criterion of this card.',
    'eolas': 'The key prices this part at 3 with no Ionramháil mark (“gan ionramháil”).',
    'treithe-bun': 'The key prices this part as two traits at 1 + 1 and what underlies them at 2, with no Ionramháil mark; each is a '
                   'criterion of this card.',
    'eachtra-miniu': 'The key prices this part (2+2) with no Ionramháil mark: Eachtra 2 (its two parts, 1 + 1) and Míniú 2 (one point, '
                     '1 + 1), and awards nothing for the Míniú without the right Eachtra. Each is a criterion of this card.',
    'eachtra-miniu-ionramhail': 'The key prices this part (2+1+1): Eachtra 2, Míniú 1 and Ionramháil 1. Each is a criterion of this card.',
}
READING_NOTE = ('Answers quoted from the passage are the rows; the key’s own-words versions of them are samples. The key deducts 0–3 '
                'for faulty Irish from each passage’s total (“' + GAEILGE_DEDUCTION + '”, E(35) − Gge.(0-3)); it applies once to the '
                'whole passage, never inside a single card.')
PART_NOTE = 'Whole questions and their practice parts are overlapping exercises; their marks are not added to infer the paper total.'
# The paper's "BÍODH NA FREAGRAÍ I D’FHOCAIL FÉIN, OIREAD AGUS IS FÉIDIR LEAT." sits in the interleaved text layer of the passage
# pages, where the lift check cannot read it; the task check gives it in English.
READING_TASKS = ['Read the whole extract that goes with the question.', 'Use the paragraph the question names.',
                 'Answer in your own words as far as you can, as the paper asks for both passages.']


def split_kind(crits):
    ids = [cid.split('-', 1)[1] for cid, *_ in crits]
    return '-'.join(ids)


def build():
    m = material()
    cards = []

    def add(**card):
        cards.append(dict(year=2011, level='higher', paper=1, paperFileid=FILE, schemeFileid=SCHEME_FILE, reviewedAt=REVIEWED_AT, **card))
        return cards[-1]

    c = m['composition']
    for group, (form, instruction, topic, titles) in m['groups'].items():
        for letter, title in titles:
            add(id=f'irish-2011-hl-p1-composition-{group.lower()}-{letter}', section='1', questionRef=f'2011 HL Paper 1 Ceapadóireacht {group}({letter})',
                questionText=m['head'] + f'\n\n{group} · {form} (100 marc)\n{instruction}\n\n({letter}) {title}',
                totalMarks=100, topicId=topic or ('irish-2-4' if letter == 'a' else 'irish-2-5'), conceptId=f'irish-composition-{group.lower()}',
                paperPage=3, schemePage=3, schemePages=[3, 4, 5], atlasQuestionId=f'W-{group}-{letter}', reviewedPaperPages=[2, 3],
                taskRequirements=['Write in the form the question asks for.', 'Nóta: Is leor 500-600 focal mar fhreagra i gcás ar bith.'],
                criteria=[criterion('abhar', 'Ionramháil Ábhair', 20, [c['abhar'], c['note'], c['unit']]),
                          criterion('gaeilge', 'Cumas Gaeilge', 80, c['gaeilge'])],
                markingGuideNote='Whole 100-mark composition: Ionramháil Ábhair 20 and Cumas Gaeilge 80, assessed as one unit (scheme PDF 3–5); '
                                 'the 2011 scheme prints no Stíl mark and no separate reductions for a short or off-title attempt. '
                                 + COMPOSITION_REASONS[group],
                sourceMaterial=source(f'Ceapadóireacht {group}({letter})', f'Gaeilge Ardleibhéal 2011 · Páipéar 1 · Ceapadóireacht {group}({letter})', [2, 3]))

    rules = m['rules']
    for letter, passage in PASSAGES.items():
        topic, pages = passage['topic'], passage['pages']
        material_ = source(f'Léamhthuiscint {letter}', passage['title'], pages)
        by_question = collections.defaultdict(list)
        for q, p, prompt, header, lines, spages, crits in passage['cuts']:
            criteria = []
            for cid, label, marks, permitted, refs in crits:
                guidance = [header if ref == 'H' else lines[ref] if isinstance(ref, int) else rules[ref] for ref in refs]
                criteria.append(criterion(cid, label, marks, guidance, 'exact', permitted))
            scheme_pages = sorted(set(spages) | ({5, 6} if any('IONR' in refs for *_, refs in crits) else set()))
            kind = split_kind(crits)
            label = f'{q}({p})'
            card = add(id=f'irish-2011-hl-p1-reading-{letter.lower()}-q{q}-{p}', section='1', atlasQuestionId=f'R-{letter}-{q}-{p}',
                       questionRef=f'2011 HL Paper 1 Léamhthuiscint {letter} · Ceist {label}', questionText=f'{label} ' + prompt[4:],
                       totalMarks=sum(cr['maxMarks'] for cr in criteria), topicId=topic, conceptId=f'irish-hl-p1-reading-{letter.lower()}-q{q}-{p}',
                       schemePage=scheme_pages[0], schemePages=scheme_pages, reviewedPaperPages=pages, taskRequirements=READING_TASKS,
                       criteria=criteria, markingGuideNote=f'{SPLIT_NOTES[kind]} {READING_NOTE} {PART_NOTE}', sourceMaterial=material_)
            assert card['totalMarks'] == (3 if p == 'a' else 4), card['id']
            by_question[q].append((p, prompt, card, kind))
        for q, parts in by_question.items():
            assert [p for p, *_ in parts] == ['a', 'b'], (letter, q)
            add(id=f'irish-2011-hl-p1-reading-{letter.lower()}-q{q}', section='1', atlasQuestionId=f'R-{letter}-{q}',
                questionRef=f'2011 HL Paper 1 Léamhthuiscint {letter} · Ceist {q}', questionText=f'{q} ' + ' '.join(prompt for _, prompt, _, _ in parts),
                totalMarks=7, topicId=topic, conceptId=f'irish-hl-p1-reading-{letter.lower()}-q{q}',
                schemePage=min(card['schemePage'] for _, _, card, _ in parts),
                schemePages=sorted({page for _, _, card, _ in parts for page in card['schemePages']}), reviewedPaperPages=pages,
                taskRequirements=READING_TASKS, criteria=[dict(cr) for _, _, card, _ in parts for cr in card['criteria']],
                markingGuideNote='Complete printed question: (a) 3 and (b) 4. Score each published term separately using these SEC allocations. '
                                 + ' '.join(f'({p}) {SPLIT_NOTES[kind]}' for p, _, _, kind in parts) + f' {READING_NOTE}',
                sourceMaterial=material_)
            assert sum(cr['maxMarks'] for cr in cards[-1]['criteria']) == 7, (letter, q)

    composition = [card for card in cards if '-composition-' in card['id']]
    parts = [card for card in cards if '-reading-' in card['id'] and re.search(r'-q\d-[ab]$', card['id'])]
    whole = [card for card in cards if '-reading-' in card['id'] and re.search(r'-q\d$', card['id'])]
    assert len(composition) == 9 and len(parts) == 20 and len(whole) == 10 and len(cards) == 39
    assert sum(card['totalMarks'] for card in parts) == 70 and sum(card['totalMarks'] for card in whole) == 70
    assert len({card['id'] for card in cards}) == len(cards) and len({card['atlasQuestionId'] for card in cards}) == len(cards)
    for card in cards:
        assert sum(cr['maxMarks'] for cr in card['criteria']) == card['totalMarks'], card['id']
        assert len({cr['id'] for cr in card['criteria']}) == len(card['criteria']), card['id']
        for cr in card['criteria']:
            assert cr['guidance'] and all(not re.search('[-]', g) for g in cr['guidance']), (card['id'], cr['id'])
            assert min(cr['permittedMarks']) == 0 and max(cr['permittedMarks']) == cr['maxMarks'], (card['id'], cr['id'])
    sr = json.loads(SOURCE_REVIEW.read_text())
    review = dict(year=2011, level='higher', paperFileid=FILE + '.pdf', schemeFileid=SCHEME_FILE + '.pdf',
                  paperSha256=PAPER_SHA, schemeSha256=SCHEME_SHA,
                  reviewedPaperPages=list(range(1, 9)), reviewedSchemePages=sr['reviewedSchemePages'],
                  schemeScope=sr['schemeScope'], reviewDate=REVIEWED_AT, status='reviewed',
                  fullPaperAndApplicableSchemeVisualSweep=True, selectionDecisions=m['decisions'],
                  cardIds=[card['id'] for card in cards],
                  compositionRouteCardIds=[card['id'] for card in composition],
                  readingPracticeCardIds=[card['id'] for card in parts],
                  readingWholeCardIds=[card['id'] for card in whole],
                  printedReadingQuestions=len(parts),
                  examStructure=dict(composition=100, reading=70, total=170),
                  nonPoolDecisions=sr['nonPoolDecisions'], openIssues=[], caveats=sr['sourceFindings'],
                  boundaries='9 composition title routes at 100 each (choose one of A, B, C, D); the 20 printed reading parts '
                             '(A and B, 1(a)–5(b)) each a card with one criterion per term of its printed split, and the 10 printed '
                             'questions whole (7 each).')
    return dict(review=review, cards=cards), m['raw']


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    data, raw = build()
    scheme_words_in(data)  # guidance carries the SEC's words only; question and task checks the paper's (irish_lifted.py)
    # The searchable scheme text the provenance checks read (as 2012–2020 and 2026 write their own), glyphs repaired.
    scheme_md = '# Gaeilge Ardleibhéal 2011 — SEC marking scheme (Páipéar I, Páipéar II agus an Chluastuiscint)\n\n' + '\n\n'.join(
        f'## PDF page {i + 1}\n\n' + symbol_text(text) for i, text in enumerate(raw))
    outputs = {OUT: json.dumps(data, ensure_ascii=False, indent=2) + '\n',
               SCHEME_MD: '\n'.join(line.rstrip() for line in scheme_md.splitlines()).rstrip() + '\n'}
    for path, value in outputs.items():
        if args.check:
            assert path.exists() and path.read_text() == value, f'Stale output: {path}'
        else:
            path.write_text(value)
    print(f"Irish Higher 2011 Paper 1: {len(data['cards'])} reviewed cards ({data['review']['printedReadingQuestions']} printed reading parts); "
          'the archive remains incomplete.')


if __name__ == '__main__':
    main()
