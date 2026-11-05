#!/usr/bin/env python3
"""Reviewed 2014 Ordinary Paper 2 (Léamhthuiscint agus Litríocht), carded new.

Paper PDF 1–12 and the Paper 2 pages of the combined LC001GLP000IV scheme (PDF 12–23,
plus 24 modified marking) reviewed on 2026-11-05. Counts are assertions, not
corpus-completeness proof. Same method as irish_ordinary_2016_p2.py.

No 2014 Ordinary card existed before. `build` cards the component the way the reviewed
2016–2025 Ordinary Paper 2s are carded: the ten whole reading questions (each part its
own 5-mark criterion), the eight literature questions (each printed sub-question its own
criterion, the 0–4 Gaeilge deduction once), and the practice cards beside them: every
reading part (20), the five printed points of 2A(a) Hurlamaboc, every prescribed-poetry
sub-question (6) and the four printed questions inside 3A(a)(i) Géibheann.

2014's layout is 2016's: “FREAGAIR GACH CEIST (1, 2 AGUS 3).” Ceist 1 is Léamhthuiscint
A and B (both); Ceist 2 is A (Prós Ainmnithe) or B (Prós Roghnach) and Ceist 3 is A
(Filíocht Ainmnithe) or B (Filíocht Roghnach), each section printing two questions, (a)
and (b), both to be answered (“Freagair (a) agus (b) anseo.”). 2A(a) Hurlamaboc asks for
a summary covering five printed points, “Luaigh na pointí seo: (i) … (v)”, and the scheme
prices it “5 phointe eolais agus 5 mharc ar gach pointe eolais”: each printed point is
its own 5-mark criterion and practice card, as the 2016 Dís sub-questions are. 2A(b) is
Oisín i dTír na nÓg alone (no film or play); 2B(a) is an optional novel extract
(protagonist 1 + five points 22 + title and author 2) and 2B(b) an optional folk tale
(five points 23 + title 2). 3A is Géibheann, whose (i) prints four questions (a)–(d) at 2
each, and Colscaradh; 3B(a) asks for a modern poem by a woman and 3B(b) one by a man.
Each literature card carries the printed choice and “Freagair (a) agus (b) anseo.” as its
task check (choice is not a route; no card combines two questions), and the section's
printed box heading with, for B, the printed restriction as its lead-in.

The scheme draws its bullets in the SymbolMT font (the glyph 'x') and one space inside text as
Calibri's glyph 3 (U+0003, PDF 13); `page_text` reads each span with its font, as
irish_ordinary_2014_p1.py does. The text layer stores each page's
boxed heading (“CEIST 1 (A + B) - LÉAMHTHUISCINT - 100 marc”, “A (50 marc)” …) with the
page body; `Scheme` removes those exact strings so no heading lands inside an answer key.
2014 prints no note above the reading questions (each part prints its own split) and no
general literature note, so each criterion carries its own scheme slice alone.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import re
from pathlib import Path
from irish_lifted import PUA, scheme_words_in, symbol_text

ROOT = Path(__file__).resolve().parents[3]
YEAR = 2014
FILE = 'LC001GLP200IV'
SCHEME_FILE = 'LC001GLP000IV'
OUT = ROOT / 'components/MarkBank/cards/irish/ordinary-2014-p2-authored.json'
SOURCE_REVIEW = ROOT / 'scripts/markbank/authored/irish-ordinary-2014-p2-source-review.json'
REVIEWED_AT = '2026-11-05'
PAPER_SHA = '6411dc24c9591b142117751f10da553afd9e7dbc1bce403942435bbda9a443d4'
SCHEME_SHA = 'c81408cfd36cef0f7ae4633e06a546ef0d23ea1ad2ded33a519c61c02dd5b09a'
DIRECTIVE = re.compile(r'rogha|roghna|Freagair|Luaigh|Ainmnigh|\bnó\b|dhá phointe|dhá rud|dhá bh|dhá dh|dhá ch|dhá fh|dhá th|dhá ph|dhá sh|'
                       r'\ban dá\b|ceann amháin|pointe amháin|amháin|\bdhá\b', re.I)
SOURCE_NOTE = 'Shown page-for-page from the official examination paper; swipe to move between pages.'
ATTRIBUTION = '© State Examinations Commission.'
# The scheme's SymbolMT glyphs: 'x' draws its bullet (PDF 12–15).
SYMBOL_FONT = {'x': '•', ' ': ' '}
# Boxed page headings the 2014 scheme's text layer stores with the page body (exact strings, each printed once).
FURNITURE = ('Páipéar II (200 marc)', 'CEIST 1 (A + B) - LÉAMHTHUISCINT - 100 marc', 'A (50 marc)', 'B (50 marc)',
             'CEIST 2 PRÓS - AINMNITHE nó ROGHNACH (50 marc)', 'A - PRÓS AINMNITHE - (50 marc)', 'B - PRÓS ROGHNACH - (50 marc)',
             'CEIST 3 FILÍOCHT - AINMNITHE nó ROGHNACH (50 marc)', 'A - FILÍOCHT AINMNITHE - (50 marc)', 'B – FILÍOCHT ROGHNACH – (50 marc)')
FURNITURE_PATTERN = re.compile('|'.join(r'\s*' + re.escape(h) + r'(?=\s|$)\s*' for h in sorted(FURNITURE, key=len, reverse=True)))
# The literature language note, printed eight times with an en dash and a closing full stop.
LANG_LIT_TEXT = '[Gaeilge lochtach: 0 – 4 a bhaint den iomlán a gnóthaíodh.]'
LANG_LIT = re.compile(re.escape(LANG_LIT_TEXT))
# The examiner's instruction closing 3A and 3B (where to show the marks in the answer book): no candidate's answer.
EXAMINER_NOTE = 'Nóta: Caithfidh an Scrúdaitheoir an marc don Ábhar'


def clean(text):
    return re.sub(r'\s+', ' ', symbol_text(text)).strip()


def comparable(text):
    return re.sub(r'[^\w]+', '', text.lower())


def in_order(prompt, text):
    return re.search('.*?'.join(re.escape(comparable(w)) for w in prompt.split() if comparable(w)), comparable(text))


def page_text(page):
    """The page's text with each SymbolMT glyph as the character it draws (every glyph is one SYMBOL_FONT reviewed) and each
    Calibri glyph-3 space as a space."""
    lines = []
    for block in page.get_text('dict')['blocks']:
        for line in block.get('lines', []):
            parts = []
            for span in line['spans']:
                text = span['text']
                if span['font'] == 'SymbolMT':
                    assert all(c in SYMBOL_FONT for c in text), ('Unreviewed scheme glyph', page.number + 1, repr(text))
                    text = ''.join(SYMBOL_FONT[c] for c in text)
                # Calibri draws a space as glyph 3, which the text layer gives as U+0003 (PDF 13 “Is\x03i nGaeltacht”).
                text = text.replace('\x03', ' ')
                parts.append(text)
            lines.append(''.join(parts))
    return '\n'.join(lines)


def criterion(id, label, marks, guidance, kind='exact', permitted=None, deduction=False):
    return dict(id=id, label=label, kind='deduction' if deduction else 'award', maxMarks=marks,
                permittedMarks=permitted or list(range(marks + 1)), guidanceKind=kind, guidance=guidance)


def selection_decisions(paper):
    decisions = json.loads(SOURCE_REVIEW.read_text())['selectionDecisions']
    expected = {(d['page'], d['raw']) for d in decisions}
    found = {(i, clean(line)) for i, page in enumerate(paper, 1)
             for line in page.get_text().splitlines() if DIRECTIVE.search(clean(line))}
    assert found == expected, ('Unclassified/stale selection directives', found - expected, expected - found)
    return decisions


class Scheme:
    """Scheme pages joined with page markers so every chunk knows the PDF pages it spans."""

    def __init__(self, doc, first, last):
        self.text = ''
        self.removed = 0
        for p in range(first, last + 1):
            body = re.sub(r'^\d+\s', '', clean(page_text(doc[p - 1])))
            body, n = FURNITURE_PATTERN.subn(' ', body)
            self.removed += n
            self.text += f' ⟦{p}⟧ ' + clean(body)

    def chunk(self, start, end=None, after=0):
        i = self.text.index(start, after)
        j = self.text.index(end, i + len(start)) if end else len(self.text)
        raw = self.text[i:j]
        pages = {int(re.findall(r'⟦(\d+)⟧', self.text[:i])[-1])}
        pages |= {int(m.group(1)) for m in re.finditer(r'⟦(\d+)⟧([^⟦]*)', raw) if clean(m.group(2)) not in ('', 'nó')}
        return clean(re.sub(r'⟦\d+⟧', ' ', raw)), sorted(pages)


def before_language_note(text):
    return re.split(r'\[\s*Gaeilge lochtach', text)[0].strip()


def language_note(text):
    """The language note a literature answer prints after its key."""
    found = LANG_LIT.findall(text)
    assert len(found) == 1, (len(found), text[-120:])
    return found[0]


def split_at(text, cuts, slug):
    idx = [text.index(cut) for cut in cuts]
    assert idx == sorted(idx), slug
    return [text[a:b].strip() for a, b in zip(idx, idx[1:] + [len(text)])]


# Two points priced first-correct 3, second 2: “3 mharc + 2 mharc”.
TWO_POINTS = re.compile(r'3 mharc \+ 2 mharc')
READING_END = '[Gaeilge lochtach: 0 - 5'

# (q, part, paper prompt, scheme anchor)
PASSAGES = {
    'A': dict(title='Sibéal Davitt – Rinceoir ar an Sean-Nós', pages=[4, 5], topic='irish-3-0', start='⟦12⟧', parts=[
        ('1', 'a', '(a) Cén fáth a ritheann Sibéal ceardlanna rince ar an sean-nós i mBaile Átha Cliath? (Alt 1)', '1. (a) Cén fáth a ritheann Sibéal'),
        ('1', 'b', '(b) Cén post atá ag Sibéal ar an gclár Imeall? (Alt 1)', '(b) Cén post atá ag Sibéal'),
        ('2', 'a', '(a) Cár rugadh Sibéal? (Alt 2)', '2. (a) Cár rugadh Sibéal'),
        ('2', 'b', '(b) Ainmnigh an dá scoil ar fhreastail Sibéal orthu. (Alt 2)', '(b) Ainmnigh an dá scoil'),
        ('3', 'a', '(a) Céard iad na hábhair a ndearna Sibéal staidéar orthu i gColáiste na Tríonóide? (Alt 3)', '3. (a) Céard iad na hábhair'),
        ('3', 'b', '(b) Scríobh síos dhá phíosa eolais faoina céad scannán. (Alt 3)', '(b) Scríobh síos dhá phíosa eolais faoina céad scannán'),
        ('4', 'a', '(a) Cá háit is mó a mbíonn an rince ar an sean-nós ar siúl? (Alt 4)', '4. (a) Cá háit is mó'),
        ('4', 'b', '(b) Tabhair dhá phíosa eolais faoin rince Gaelach. (Alt 4)', '(b) Tabhair dhá phíosa eolais faoin rince Gaelach'),
        ('5', 'a', '(a) Cén chosúlacht mhór a fheiceann Sibéal idir an rince agus an scannánaíocht? (Alt 5)', '5. (a) Cén chosúlacht mhór'),
        ('5', 'b', '(b) Cén cúrsa atá á dhéanamh ag Sibéal faoi láthair? (Alt 5)', '(b) Cén cúrsa atá á dhéanamh')]),
    'B': dict(title='Brian Ó Drisceoil - Laoch Mór Rugbaí', pages=[6, 7], topic='irish-3-1', start='⟦14⟧', parts=[
        ('1', 'a', '(a) Cár rugadh Brian Ó Drisceoil? (Alt 1)', '1. (a) Cár rugadh Brian Ó Drisceoil'),
        ('1', 'b', '(b) Cén comórtas a bhuaigh foireann Bhriain sa bhliain 1998? (Alt 1)', '(b) Cén comórtas a bhuaigh foireann Bhriain'),
        ('2', 'a', '(a) Cén fáth ar bhliain thábhachtach í 1999 do Bhrian Ó Drisceoil? (Alt 2)', '2. (a) Cén fáth ar bhliain thábhachtach'),
        ('2', 'b', '(b) Cad a bhuaigh Éire in 2009 nuair a bhí Brian Ó Drisceoil ina chaptaen? (Alt 2)', '(b) Cad a bhuaigh Éire in 2009'),
        ('3', 'a', '(a) Cad a tharla do Bhrian sa chéad chluiche i gcoinne na All Blacks in 2005? (Alt 3)', '3. (a) Cad a tharla do Bhrian sa chéad chluiche'),
        ('3', 'b', '(b) Cén fáth a raibh fearg ar a lán de lucht leanúna an rugbaí anuraidh? (Alt 3)', '(b) Cén fáth a raibh fearg'),
        ('4', 'a', '(a) Luaigh dhá scil atá ag Brian mar imreoir. (Alt 4)', '4. (a) Luaigh dhá scil'),
        ('4', 'b', '(b) Cén fáth ar bhronn Comhairle Cathrach Bhaile Átha Cliath Saoirse na Cathrach air? (Alt 4)', '(b) Cén fáth ar bhronn Comhairle'),
        ('5', 'a', '(a) Scríobh síos rud amháin a tharla ar an ócáid speisialta do Bhrian ar an gcéad lá de Shamhain 2013. (Alt 5)',
         '5. (a) Scríobh síos rud amháin'),
        ('5', 'b', '(b) Luaigh plean amháin atá ag Brian nuair a éireoidh sé as an rugbaí. (Alt 5)', '(b) Luaigh plean amháin')]),
}

# Printed lines (paper PDF 3, 4, 8–12).
PROSE_CHOICE = 'Freagair A (Prós Ainmnithe) nó B (Prós Roghnach).'
POETRY_CHOICE = 'Freagair A (Filíocht Ainmnithe) nó B (Filíocht Roghnach).'
BOTH = 'Freagair (a) agus (b) anseo.'
BOX_2A, BOX_2B = 'A – PRÓS AINMNITHE – (50 marc)', 'B – PRÓS ROGHNACH – (50 marc)'
BOX_3A, BOX_3B = 'A – FILÍOCHT AINMNITHE – (50 marc)', 'B – FILÍOCHT ROGHNACH – (50 marc)'
NO_PRESCRIBED_PROSE = 'Níl cead aon ábhar a bhaineann le Prós Ainmnithe a úsáid sna freagraí ar an bPrós Roghnach.'
NO_PRESCRIBED_POETRY = 'Níl cead aon ábhar a bhaineann le Filíocht Ainmnithe a úsáid sna freagraí ar an bhFilíocht Roghnach.'
STEM_2B = BOX_2B + '\n' + NO_PRESCRIBED_PROSE
STEM_3B = BOX_3B + '\n' + NO_PRESCRIBED_POETRY
# The 2023 builders' requirement lines; irish_lifted.printed_tasks gives each its English.
LIT = ['Freagair gach fochuid atá priontáilte sa rogha seo.', 'Úsáid tagairtí cruinne agus ábhartha don téacs.']
READING_PART = ['Léigh an sliocht iomlán a ghabhann leis an gceist. Freagair an chuid atá luaite ar an gcárta.', 'Úsáid an t-alt a luaitear.']
READING_WHOLE = ['Léigh an sliocht oifigiúil a ghabhann leis an gceist.', 'Freagair gach fochuid agus cloígh leis an alt a luaitear.']

# 2A(a) Hurlamaboc: a summary covering five printed points; the scheme reprints them and prices the answer once,
# “5 phointe eolais agus 5 mharc ar gach pointe eolais” (each point 2 bare + 3 development).
HURLAMABOC = ('prose-2a-a', 'P-2A-a', 'a', 'Hurlamaboc', 'irish-4-5',
              ['Tabhair achoimre ar na heachtraí is mó sa ghiota as an úrscéal Hurlamaboc.', 'Luaigh na pointí seo:'], [
    ('i', 'Cén fáth a mbeidh cóisir mhór i dteach Albright?'),
    ('ii', 'Déan cur síos ar Phól, fear céile Lisín.'),
    ('iii', 'Conas a réitíonn Ruán, an mac is sine, lena mháthair, Lisín?'),
    ('iv', 'Cad iad na hullmhúcháin a dhéanann Lisín don chóisir?'),
    ('v', 'Conas a chaitheann Lisín a cuid ama de ghnáth?')],
    '(a) Hurlamaboc Tabhair achoimre', '(b) Oisín i dTír na nÓg')
EACH_POINT = ('5 phointe eolais agus 5 mharc ar gach pointe eolais. (5 mharc = 2 mharc ar lomphointe eolais agus 3 mharc ar '
              'fhorbairt.)')
# 2A(b) Oisín i dTír na nÓg: the printed quotation (with its printed source line), then the question.
OISIN = ('prose-2a-b', 'P-2A-b', 'b', 'Oisín i dTír na nÓg', 'irish-4-1',
         ['“Ansin shuigh Oisín i bhfianaise Phádraig agus na cléire gur inis sé a scéal ar Thír na nÓg agus ar Niamh Chinn Óir '
          'a mheall ón Fhiann é.”', 'Oisín i dTír na nÓg',
          'Déan cur síos ar na scéalta a d’inis Oisín don slua faoi Thír na nÓg agus faoi Niamh Chinn Óir.'],
         '(b) Oisín i dTír na nÓg', 'Níl cead aon ábhar a bhaineann le Prós Ainmnithe')
# 2B: (slug, atlas, title, paper lines, scheme start, scheme end, [(id, label, marks, cut-before, kind, permitted)])
PROSE_2B = [
    ('prose-2b-a', 'P-2B-a', 'Giota as úrscéal roghnach',
     ['(a) Maidir le giota as úrscéal roghnach a ndearna tú staidéar air le linn do chúrsa, ainmnigh an príomhcharachtar (an phríomhphearsa) '
      'ann. Tabhair cuntas ar na himeachtaí (rudaí) a tharlaíonn don phríomhcharachtar (don phríomhphearsa) sa ghiota sin. (23 marc)',
      'Ní mór teideal an úrscéil sin, mar aon le hainm an údair, a scríobh síos go cruinn. (2 mharc)'],
     '(a) Maidir le giota as úrscéal roghnach', '(b) Maidir le scéal béaloidis roghnach',
     [('priomhcharachtar', 'Ainm an phríomhcharachtair', 1, 'Ainm an phríomhcharachtair', 'indicative', [0, 1]),
      ('eolas', 'Na himeachtaí', 22, '5 phointe eolais ag teastáil', 'indicative', None),
      ('teideal', 'Teideal + ainm an údair', 2, 'Ní mór teideal an úrscéil sin, mar aon le hainm an údair, a scríobh síos go soiléir.', 'exact', [0, 1, 2])]),
    ('prose-2b-b', 'P-2B-b', 'Scéal béaloidis roghnach',
     ['(b) Maidir le scéal béaloidis roghnach a ndearna tú staidéar air le linn do chúrsa, tabhair cuntas ar na príomhimeachtaí (príomhrudaí) '
      'a tharlaíonn sa scéal sin. (23 marc)',
      'Ní mór teideal an scéil bhéaloidis sin a scríobh síos go cruinn. (2 mharc)'],
     '(b) Maidir le scéal béaloidis roghnach', 'Freagair (a) agus (b) anseo. (a) Géibheann',
     [('eolas', 'Na príomhimeachtaí', 23, '5 phointe eolais ag teastáil', 'indicative', None),
      ('teideal', 'Teideal an scéil bhéaloidis', 2, 'Teideal an scéil bhéaloidis = 2 mharc', 'exact', [0, 2])]),
]
# 3A: (slug, atlas, page, title, topic, [(label, paper prompt, marks, scheme cut, printed price in the key)], scheme start, scheme end)
POETRY_3A = [
    ('poetry-3a-a', 'F-3A-a', 10, 'Géibheann', 'irish-5-2', [
        ('i', '(a) Cad as don ainmhí seo?\n(b) Cad a fheiceann an t-ainmhí trí leathshúil?\n(c) Cé a thagann ag féachaint ar an ainmhí anois?\n'
              '(d) Luaigh an rud is mó a theastaíonn ón ainmhí anois.', 8, '(i) (a) Cad as don ainmhí seo?', '(2 mharc)'),
        ('ii', 'Inis i d’fhocail féin, cén saghas ainmhí é an t-ainmhí seo. (Is leor dhá phointe eolais.)', 8,
         '(ii) Inis i d’fhocail féin, cén saghas ainmhí', '(2 phointe eolais ar 4 mharc an ceann)'),
        ('iii', 'Scríobh síos an mothúchán is láidre sa dán dar leat. Tabhair dhá shampla den mhothúchán sin sa dán.', 9,
         '(iii) Scríobh síos an mothúchán is láidre', 'Dhá shampla den mhothúchán = 4 mharc + 4 mharc')],
     '(a) Géibheann (i)', '(b) Colscaradh (i)'),
    ('poetry-3a-b', 'F-3A-b', 11, 'Colscaradh', 'irish-5-5', [
        ('i', 'Cad is téama don dán Colscaradh (thíos), dar leat? Tabhair dhá phointe eolais faoin téama sin sa dán.', 8,
         '(i) Cad is téama don dán Colscaradh', 'Dhá phointe eolais faoin téama sin = 3 mharc + 3 mharc'),
        ('ii', 'Inis i d’fhocail féin, cén saghas duine í an bhean sa dán. (Is leor dhá phointe eolais.)', 8,
         '(ii) Inis i d’fhocail féin, cén saghas duine', 'Dhá phointe eolais = 4 mharc + 4 mharc'),
        ('iii', 'An maith leat an dán seo? Cuir fáthanna le do fhreagra. (Is leor dhá fháth.)', 9,
         '(iii) An maith leat an dán seo?', 'dhá fháth = (4 mharc + 4 mharc)')],
     '(b) Colscaradh (i)', EXAMINER_NOTE),
]
# 3A(a)(i) prints four questions (a)–(d) at 2 each: (slug, sub-question) -> [(letter, scheme question, marks, next cut)]
SLOTS_3A = {
    ('poetry-3a-a', 'i'): [('a', 'Cad as don ainmhí seo?', 2, '(b) Cad a fheiceann'),
                           ('b', 'Cad a fheiceann an t-ainmhí trí leathshúil?', 2, '(c) Cé a thagann'),
                           ('c', 'Cé a thagann ag féachaint ar an ainmhí anois?', 2, '(d) Luaigh an rud'),
                           ('d', 'Luaigh an rud is mó a theastaíonn ón ainmhí anois.', 2, None)],
}
POETRY_3B = [
    ('poetry-3b-a', 'F-3B-a', 'a bean', [
        '(i) Maidir le dán roghnach nua-aimseartha amháin a scríobh bean agus a ndearna tú staidéar air le linn do chúrsa, inis i d’fhocail '
        'féin, cad iad príomhsmaointe an dáin. (7 marc)',
        '(ii) Luaigh dhá íomhá (dhá phictiúr) atá sa dán. Déan cur síos i d’fhocail féin ar an dá íomhá (ar an dá phictiúr) sin sa dán. (7 marc)',
        '(iii) Scríobh síos an mothúchán is láidre sa dán dar leat. Tabhair dhá shampla den mhothúchán sin sa dán. (9 marc)'],
     '(a) (i) Maidir le dán roghnach nua-aimseartha amháin a scríobh bean', '(b) (i) Maidir le dán roghnach nua-aimseartha amháin a scríobh fear',
     ['(ii) Luaigh dhá íomhá', '(iii) Scríobh síos an mothúchán', 'Ní mór teideal an dáin']),
    ('poetry-3b-b', 'F-3B-b', 'a fear', [
        '(i) Maidir le dán roghnach nua-aimseartha amháin a scríobh fear agus a ndearna tú staidéar air le linn do chúrsa, inis i d’fhocail '
        'féin, cad is téama don dán sin, dar leat. Tabhair dhá phointe eolais faoin téama sin sa dán. (7 marc)',
        '(ii) Cén t-atmaisféar atá sa dán seo, dar leat? Tabhair dhá shampla den atmaisféar sin sa dán. (7 marc)',
        '(iii) An maith leat an dán seo? Cuir fáthanna le do fhreagra. (Is leor dhá fháth.) (9 marc)'],
     '(b) (i) Maidir le dán roghnach nua-aimseartha amháin a scríobh fear', EXAMINER_NOTE,
     ['(ii) Cén t-atmaisféar', '(iii) An maith leat', 'Ní mór teideal an dáin']),
]
TITLE_LINE = 'Ní mór teideal an dáin sin, mar aon le hainm an fhile, a scríobh síos go cruinn. (2 mharc)'
# Each 3B key closes with the question's total and a direction for the whole answer.
TOTAL_3B = 'Iomlán (25 marc)'
TREOIR_3B = 'Treoir: Má roghnaítear dán seanaimseartha, bronnfar 0 ar an bhfreagra.'

_MATERIAL = None


def material():
    global _MATERIAL
    if _MATERIAL:
        return _MATERIAL
    import fitz
    paper_path = ROOT / f'paper-trail-corpus/exampapers/{YEAR}/{FILE}.pdf'
    scheme_path = ROOT / f'paper-trail-corpus/markingschemes/{YEAR}/{SCHEME_FILE}.pdf'
    assert hashlib.sha256(paper_path.read_bytes()).hexdigest() == PAPER_SHA, 'Paper changed: repeat visual review'
    assert hashlib.sha256(scheme_path.read_bytes()).hexdigest() == SCHEME_SHA, 'Scheme changed: repeat visual review'
    paper, doc = fitz.open(paper_path), fitz.open(scheme_path)
    texts = [clean(p.get_text()) for p in paper]
    s = Scheme(doc, 12, 23)
    assert s.removed == len(FURNITURE), s.removed
    assert not PUA.search(s.text), 'private-use glyph left in the scheme text'
    assert 'Níl sé i gceist a chur in iúl' not in s.text, '2014 prints no general literature note'
    assert 'Nóta: Má tá dhá phointe eolais' not in s.text, '2014 prints no note above the reading questions'
    lang_read = '[Gaeilge lochtach: 0 - 5 a bhaint den iomlán a gnóthaíodh.]'
    assert s.text.count(lang_read) == 2
    assert s.text.count(EXAMINER_NOTE) == 2
    for letter, passage in PASSAGES.items():
        page_text_ = ' '.join(texts[p - 1] for p in passage['pages'])
        assert in_order(passage['title'], page_text_), letter
        after = s.text.index(passage['start'])
        resolved = []
        anchors = [p[3] for p in passage['parts']]
        for index, (q, part, prompt, anchor) in enumerate(passage['parts']):
            assert in_order(prompt, page_text_), (letter, q, part)
            # The last part ends where the passage's language deduction and penalty note begin.
            nxt = anchors[index + 1] if index + 1 < len(anchors) else READING_END
            chunk, spages = s.chunk(anchor, nxt, after)
            after = s.text.index(anchor, after) + 1
            assert chunk.startswith(anchor) and in_order(prompt, chunk), (letter, q, part)
            assert '5 mharc' in chunk and '50 marc' not in chunk and 'LÉAMHTHUISCINT' not in chunk and 'Gearrfar' not in chunk, (letter, q, part, chunk[:80])
            two = bool(TWO_POINTS.search(chunk))
            permitted = [0, 3, 5] if (two or '= 3 mharc' in chunk) else [0, 5]
            resolved.append((q, part, prompt, chunk, spages, two, permitted))
        passage['resolved'] = resolved
    # Hurlamaboc, Oisín, 2B(a), 2B(b), Géibheann, Colscaradh, 3B(a), 3B(b): eight.
    assert len(LANG_LIT.findall(s.text)) == 8, len(LANG_LIT.findall(s.text))
    slug, atlas, letter, title, topic, intro, points, start, end = HURLAMABOC
    for line in [title] + intro + [p for _, p in points] + ['(25 marc)']:
        assert in_order(line, texts[7]), (slug, line[:40])
    reprint = s.chunk(start, end)[0]
    assert all(f'({label}) {p}' in reprint for label, p in points) and reprint.count(EACH_POINT) == 1, slug
    slug, atlas, letter, title, topic, lines, start, end = OISIN
    assert in_order(f'({letter}) {title} ' + ' '.join(lines) + ' (25 marc)', texts[7]), slug
    for slug2, atlas2, title2, lines2, start2, end2, parts2 in PROSE_2B:
        for line in lines2:
            assert in_order(line, texts[8]), (slug2, line[:50])
    for slug3, atlas3, page, title3, topic3, subs3, start3, end3 in POETRY_3A:
        assert in_order(title3, texts[page - 1]), slug3
        for label, prompt, marks, cut, price in subs3:
            assert in_order(f'({label}) ' + prompt.replace('\n', ' ') + f' ({marks} marc)', texts[page - 1]), (slug3, label)
    for slug4, atlas4, writer, prompts, start4, end4, cuts4 in POETRY_3B:
        for line in prompts + [TITLE_LINE]:
            assert in_order(line, texts[11]), (slug4, line[:50])
    assert comparable(texts[11]).count(comparable(TITLE_LINE)) == 2
    for page, line in [(3, 'FREAGAIR GACH CEIST (1, 2 AGUS 3).'), (4, 'Freagair A agus B anseo.'), (8, PROSE_CHOICE), (8, BOTH), (8, BOX_2A),
                       (9, BOX_2B), (9, NO_PRESCRIBED_PROSE), (9, BOTH), (10, POETRY_CHOICE), (10, BOTH), (10, BOX_3A), (12, BOX_3B),
                       (12, NO_PRESCRIBED_POETRY), (12, BOTH)]:
        assert comparable(line) in comparable(texts[page - 1]), (page, line)
    _MATERIAL = dict(paper=paper, texts=texts, s=s, lang_read=lang_read, decisions=selection_decisions(paper))
    return _MATERIAL


def deduction(note):
    return criterion('gaeilge-deduction', 'Gaeilge lochtach', 4, [note], 'quality', deduction=True)


def reading_note(m):
    return 'Scheme: “' + m['lang_read'] + '” — one deduction from each passage total (50), never inside a single part.'


def source(label, title, pages):
    return dict(kind='source-text', label=label, title=title, pages=pages, attribution=ATTRIBUTION, presentationNote=SOURCE_NOTE)


def hurlamaboc_key(m):
    """The scheme's reprint of each printed point, and the one tariff it prints for all five, then its language note."""
    slug, atlas, letter, title, topic, intro, points, start, end = HURLAMABOC
    whole, spages = m['s'].chunk(start, end)
    lang = language_note(whole)
    whole = before_language_note(whole)
    pieces = split_at(whole, [f'({label}) {p}' for label, p in points], slug)
    # Each printed point's reprint is its own line; the last one runs on into the question's total and the tariff.
    lines = [f'({label}) {p}' for label, p in points]
    assert all(piece == line for piece, line in zip(pieces[:-1], lines[:-1])), pieces
    assert pieces[-1] == f'{lines[-1]} (25 marc) {EACH_POINT}', pieces[-1]
    return lines, spages, lang


def poem_pieces(m, slug, subs, start, end):
    whole, spages = m['s'].chunk(start, end)
    lang = language_note(whole)
    whole = before_language_note(whole)
    pieces = split_at(whole, [cut for _, _, _, cut, _ in subs], slug)
    for (label, _, marks, _, price), piece in zip(subs, pieces):
        assert price in piece, (slug, label, piece[:60])
    return pieces, spages, lang


def slot_pieces(piece, slots):
    out = []
    for sub, question, marks, nxt in slots:
        start_at = piece.index(question)
        slot = piece[start_at:piece.index(nxt, start_at) if nxt else len(piece)].strip()
        # 2014 prints each question's price in brackets (“(2 mharc)”), then “Freagraí samplacha:”.
        assert re.search(r'Freagraí samplacha:', slot) and f'{question} ({marks} mharc)' in slot, (sub, slot[:80])
        out.append((sub, slot))
    return out


def slot_permitted(slot, marks):
    """0, the slot's mark, and every partial price its key prints."""
    return sorted({0, marks} | {int(v) for v in re.findall(r'= (\d) mharc', slot) if int(v) <= marks})


WHOLE_PROSE_NOTE = ('One complete SEC response: five points at 5 (2 for the bare point + 3 for development); the 0–4 Gaeilge deduction applies once '
                    'to this whole 25-mark answer. The answer is judged on merit against that allocation.')
LIT_DEDUCTION_NOTE = 'The 0–4 Gaeilge deduction applies once to this whole 25-mark answer, never inside one sub-question.'


def build():
    m = material()
    cards = []

    def add(key, slug, ref, prompt, topic, pages, scheme_pages, criteria, requirements, note, src, concept=None, stem=None, focus=None):
        cards.append(dict(
            id=f'irish-{YEAR}-ol-p2-{slug}', year=YEAR, level='ordinary', paper=2, section='2',
            atlasQuestionId=key, questionRef=f'{YEAR} OL Paper 2 {ref}', **({'stem': stem} if stem else {}), questionText=prompt,
            totalMarks=sum(c['maxMarks'] for c in criteria if c['kind'] == 'award'), topicId=topic,
            conceptId=concept or f'irish-ol-p2-{slug}', paperFileid=FILE, paperPage=pages[0], schemeFileid=SCHEME_FILE,
            schemePage=scheme_pages[0], schemePages=scheme_pages, reviewedAt=REVIEWED_AT, reviewedPaperPages=pages,
            taskRequirements=requirements, criteria=criteria, markingGuideNote=note, sourceMaterial=src,
            **({'practiceFocus': focus} if focus else {})))

    # ---- Ceist 1: Léamhthuiscint A and B (whole questions first, then their parts) -----------------
    whole_ids, practice_ids = [], []
    for letter, passage in PASSAGES.items():
        src = source(f'Léamhthuiscint {letter}', passage['title'], passage['pages'])
        by_q = {}
        for q, part, prompt, chunk, spages, two, permitted in passage['resolved']:
            by_q.setdefault(q, []).append((part, prompt, chunk, spages, permitted))
        for q, parts in by_q.items():
            text = f'{q}. ' + ' '.join(prompt for _, prompt, *_ in parts)
            crits = [criterion(part, f'({part}) Freagra', 5, [chunk], permitted=permitted) for part, _, chunk, _, permitted in parts]
            # The frozen Atlas identities 1–5 (A) and 6–10 (B) are the whole questions.
            add(str(int(q) + (5 if letter == 'B' else 0)), f'reading-{letter.lower()}-q{q}', f'Léamhthuiscint {letter} · Ceist {q}', text,
                passage['topic'], passage['pages'], sorted({p for *_, sp, _ in parts for p in sp}), crits, READING_WHOLE,
                'Complete printed question: (a) 5 + (b) 5, each scored separately at its SEC allocation. ' + reading_note(m), src,
                concept=f'irish-reading-{letter.lower()}-q{q}')
            whole_ids.append(cards[-1]['id'])
    for letter, passage in PASSAGES.items():
        src = source(f'Léamhthuiscint {letter}', passage['title'], passage['pages'])
        for q, part, prompt, chunk, spages, two, permitted in passage['resolved']:
            add(f'R-{letter}-{q}-{part}', f'reading-{letter.lower()}-q{q}-{part}', f'Léamhthuiscint {letter} · Ceist {q}({part})',
                f'{q}{prompt}', passage['topic'], passage['pages'], spages,
                [criterion(part, 'Freagra', 5, [chunk], permitted=permitted)], READING_PART,
                'SEC allocation for this part' + (': first correct point 3, second 2 (0/3/5).' if two else '.') + ' ' + reading_note(m), src)
            practice_ids.append(cards[-1]['id'])

    sub_note = 'One printed sub-question at its published tariff. ' + LIT_DEDUCTION_NOTE
    question_lit = []
    # ---- Ceist 2A: Hurlamaboc (five printed points), then Oisín i dTír na nÓg ----------------------
    slug, atlas, letter, title, topic, intro, points, start, end = HURLAMABOC
    lines, hpages, h_lang = hurlamaboc_key(m)
    head = f'({letter}) {title}\n' + '\n'.join(intro)
    src = source('Prós Ainmnithe', title, [8])
    add(atlas, slug, 'Prose 2A(a)', head + '\n' + '\n'.join(f'({l}) {p}' for l, p in points) + '\n(25 marc)', topic, [8], hpages,
        [criterion(f'eolas-{label}', f'({label}) Eolas', 5, [line, EACH_POINT], 'indicative') for (label, _), line in zip(points, lines)]
        + [deduction(h_lang)], [PROSE_CHOICE, BOTH] + LIT,
        'One complete SEC response: a summary covering the five printed points, each a point of information at 5 (2 for the bare point + 3 '
        'for development), then the 0–4 Gaeilge deduction once. The scheme prints no sample answers for Hurlamaboc; each point is judged on '
        'merit against that split.', src, concept=f'irish-prose-2a-{topic}', stem=BOX_2A)
    question_lit.append(cards[-1]['id'])
    slug_o, atlas_o, letter_o, title_o, topic_o, lines_o, start_o, end_o = OISIN
    chunk_o, opages = m['s'].chunk(start_o, end_o)
    assert chunk_o.endswith(f'(25 marc) {EACH_POINT} {LANG_LIT_TEXT}'), chunk_o[-160:]
    lang_o = language_note(chunk_o)
    add(atlas_o, slug_o, f'Prós 2A({letter_o}) · {title_o}', f'({letter_o}) {title_o}\n' + '\n'.join(lines_o) + ' (25 marc)', topic_o, [8], opages,
        [criterion('eolas', 'Eolas', 25, [before_language_note(chunk_o)], 'indicative'), deduction(lang_o)], [PROSE_CHOICE, BOTH] + LIT[1:],
        WHOLE_PROSE_NOTE, source('Prós Ainmnithe', title_o, [8]), concept=f'irish-prose-2a-{topic_o}', stem=BOX_2A)
    question_lit.append(cards[-1]['id'])

    # ---- Ceist 2B: Prós Roghnach (a) an optional novel extract and (b) an optional folk tale -----------
    for slug2, atlas2, title2, lines2, start2, end2, parts2 in PROSE_2B:
        chunk2, spages2 = m['s'].chunk(start2, end2)
        lang2 = language_note(chunk2)
        chunk2 = before_language_note(chunk2)
        # The key reprints the question and its title line first; the marking text begins at the first criterion's cut.
        cuts = [chunk2.index(part[3]) for part in parts2]
        assert cuts == sorted(cuts), slug2
        reprint = chunk2[:cuts[0]].strip()
        assert all(in_order(line, reprint) for line in lines2), (slug2, reprint[:80])
        bits = [chunk2[a:b].strip() for a, b in zip(cuts, cuts[1:] + [len(chunk2)])]
        crits = []
        for (cid, label, marks, _, kind, permitted), bit in zip(parts2, bits):
            guidance = [bit]
            if cid == 'teideal' and slug2 == 'prose-2b-b':
                # The folk tale's title is priced after its points; its printed requirement line is in the reprint.
                guidance = [lines2[1], bit]
            crits.append(criterion(cid, label, marks, guidance, kind, permitted=permitted))
        add(atlas2, slug2, f'Prose 2B({atlas2[-1]})', '\n'.join(lines2), 'irish-4-7', [9], spages2, crits + [deduction(lang2)],
            [PROSE_CHOICE, NO_PRESCRIBED_PROSE, BOTH] + LIT[1:],
            'One complete SEC response: ' + ', '.join(f'{label} {marks}' for _, label, marks, *_ in parts2) +
            ', then the 0–4 Gaeilge deduction once. The optional text is open content chosen by the candidate; the scheme prints no sample '
            'points for it, so its points are judged on merit against these allocations (indicative rather than exhaustive).',
            source('Prós Roghnach', title2, [9]), concept='irish-prose-2b-irish-4-7', stem=STEM_2B)
        question_lit.append(cards[-1]['id'])

    # ---- Ceist 3A: Géibheann and Colscaradh ------------------------------------------------------------
    poem_parts = {}
    for slug3, atlas3, page, title3, topic3, subs3, start3, end3 in POETRY_3A:
        pieces3, spages3, lang3 = poem_pieces(m, slug3, subs3, start3, end3)
        poem_parts[slug3] = (pieces3, spages3, lang3)
        crits = [criterion(f'eolas-{label}', f'({label}) Eolas', marks, [piece], 'indicative')
                 for (label, _, marks, _, _), piece in zip(subs3, pieces3)]
        prompt = '\n'.join(f'({label}) {p}' + f' ({marks} marc)' for label, p, marks, _, _ in subs3)
        add(atlas3, slug3, f'Poetry 3A({atlas3[-1]})', f'({atlas3[-1]}) {title3}\n' + prompt, topic3, [page], spages3, crits + [deduction(lang3)],
            [POETRY_CHOICE, BOTH] + LIT,
            'One complete SEC response: ' + ', '.join(f'({label}) {marks}' for label, _, marks, _, _ in subs3) +
            ' at their printed tariffs, then the 0–4 Gaeilge deduction once. The sample answers are indicative rather than exhaustive; '
            'lines lifted straight from the poem without the candidate’s own words earn 2 + 2 where the scheme says so.',
            source('Filíocht Ainmnithe', title3, [page]), concept=f'irish-poetry-3a-{topic3}', stem=BOX_3A)
        question_lit.append(cards[-1]['id'])

    # ---- Ceist 3B: Filíocht Roghnach (a) a modern poem by a woman and (b) one by a man -------------------
    for slug4, atlas4, writer, prompts, start4, end4, cuts4 in POETRY_3B:
        chunk4, spages4 = m['s'].chunk(start4, end4, m['s'].text.index('⟦22⟧'))
        lang4 = language_note(chunk4)
        chunk4 = before_language_note(chunk4)
        # The key closes with the question's total and the direction for an old poem, after the title's price.
        assert chunk4.endswith(f'(2 mharc) {TOTAL_3B} {TREOIR_3B}'), chunk4[-120:]
        chunk4 = chunk4[:-len(f'{TOTAL_3B} {TREOIR_3B}')].strip()
        idx = [0] + [chunk4.index(cut) for cut in cuts4]
        bits = [chunk4[a:b].strip() for a, b in zip(idx, idx[1:] + [len(chunk4)])]
        for bit, cap in zip(bits, ['(7 marc)', '(7 marc)', '(9 marc)', '(2 mharc)']):
            assert bit.endswith(cap), (slug4, cap, bit[-40:])
        crits = [criterion('eolas-i', '(i) Eolas', 7, [bits[0], TREOIR_3B], 'indicative'), criterion('eolas-ii', '(ii) Eolas', 7, [bits[1]], 'indicative'),
                 criterion('eolas-iii', '(iii) Eolas', 9, [bits[2]], 'indicative'),
                 criterion('teideal', 'Teideal + ainm an fhile', 2, [bits[3]], 'exact', permitted=[0, 1, 2])]
        add(atlas4, slug4, f'Poetry 3B({atlas4[-1]})', f'({atlas4[-1]}) ' + '\n'.join(prompts + [TITLE_LINE]), 'irish-5-6', [12], spages4,
            crits + [deduction(lang4)], [POETRY_CHOICE, NO_PRESCRIBED_POETRY, BOTH] + LIT,
            'One complete SEC response: (i) 7, (ii) 7, (iii) 9, poem and poet 2, then the 0–4 Gaeilge deduction once. '
            f'3B({atlas4[-1]}) asks for a modern poem written by {"a woman" if writer == "a bean" else "a man"}; the scheme’s Treoir gives an old '
            'poem 0 for the whole answer. The optional poem is open content; the printed allocations are judged on merit (indicative rather '
            'than exhaustive).',
            source('Filíocht Roghnach', f'3B({atlas4[-1]}) · Dán roghnach', [12]),
            concept='irish-poetry-3b-irish-5-6', stem=STEM_3B)
        question_lit.append(cards[-1]['id'])

    # ---- Practice: the five Hurlamaboc points, every prescribed-poetry sub-question, 3A(a)(i)(a)–(d) -----
    for (label, prompt), line in zip(points, lines):
        add(f'{atlas}-{label}', f'{slug}-{label}', f'Prós 2A({letter}) · {title} · ({label})', head + f'\n({label}) {prompt}',
            topic, [8], hpages, [criterion('eolas', 'Eolas', 5, [line, EACH_POINT], 'indicative')],
            [PROSE_CHOICE, BOTH] + LIT[1:],
            'One of the five printed points the summary covers, at the scheme’s 5 for each point of information. ' + LIT_DEDUCTION_NOTE,
            src, stem=BOX_2A, focus=f'Point ({label}) of the five the summary must cover (5 marks: 2 for the bare point, 3 for developing it)')
        practice_ids.append(cards[-1]['id'])
    for slug3, atlas3, page, title3, topic3, subs3, start3, end3 in POETRY_3A:
        pieces3, spages3, _ = poem_parts[slug3]
        src3 = source('Filíocht Ainmnithe', title3, [page])
        head3 = f'({atlas3[-1]}) {title3}\n'
        for (label, prompt, marks, _, _), piece in zip(subs3, pieces3):
            slots = SLOTS_3A.get((slug3, label))
            add(f'{atlas3}-{label}', f'{slug3}-{label}', f'Filíocht 3A({atlas3[-1]}) · {title3} · ({label})', head3 + f'({label}) {prompt} ({marks} marc)',
                topic3, [page], spages3, [criterion('eolas', 'Eolas', marks, [piece], 'indicative')],
                [POETRY_CHOICE, BOTH] + LIT[1:], sub_note, src3, stem=BOX_3A)
            practice_ids.append(cards[-1]['id'])
            if slots:
                printed = dict(re.findall(r'\(([a-d])\) ([^\n]+)', prompt))
                for (sub, slot), (_, _, smarks, _) in zip(slot_pieces(piece, slots), slots):
                    add(f'{atlas3}-{label}-{sub}', f'{slug3}-{label}-{sub}', f'Filíocht 3A({atlas3[-1]}) · {title3} · ({label})({sub})',
                        head3 + f'({label}) ({sub}) {printed[sub]}', topic3, [page], spages3,
                        [criterion('eolas', 'Freagra', smarks, [slot], 'indicative', permitted=slot_permitted(slot, smarks))], [POETRY_CHOICE, BOTH] + LIT[1:],
                        f'One printed question inside 3A({atlas3[-1]})({label}), at its printed {smarks} mharc. ' + LIT_DEDUCTION_NOTE, src3, stem=BOX_3A)
                    practice_ids.append(cards[-1]['id'])

    assert len(whole_ids) == 10 and len(question_lit) == 8 and len(practice_ids) == 35, (len(whole_ids), len(question_lit), len(practice_ids))
    assert len(cards) == 53 and len({c['id'] for c in cards}) == 53 and len({c['atlasQuestionId'] for c in cards}) == 53
    for card in cards:
        assert sum(c['maxMarks'] for c in card['criteria'] if c['kind'] == 'award') == card['totalMarks'], card['id']
        for c in card['criteria']:
            assert c['guidance'] and all(not re.search('Scrúdaitheoir|Iomlán|50 marc|Gearrfar|Taispeánfar', g) and not PUA.search(g) for g in c['guidance']), (card['id'], c['id'])
    sr = json.loads(SOURCE_REVIEW.read_text())
    review = dict(year=YEAR, level='ordinary', paperFileid=FILE + '.pdf', schemeFileid=SCHEME_FILE + '.pdf',
                  paperSha256=PAPER_SHA, schemeSha256=SCHEME_SHA,
                  reviewedPaperPages=list(range(1, 13)), reviewedSchemePages=sr['reviewedSchemePages'], schemeScope=sr['schemeScope'],
                  reviewDate=REVIEWED_AT, status='reviewed', fullPaperAndApplicableSchemeVisualSweep=True, selectionDecisions=m['decisions'],
                  practiceCardIds=practice_ids, questionCardIds=whole_ids + question_lit, readingWholeCardIds=whole_ids,
                  examStructure=dict(readingA=50, readingB=50, prose=50, poetry=50, total=200),
                  nonPoolDecisions=sr['nonPoolDecisions'], openIssues=[], caveats=sr['sourceFindings'],
                  choicePolicy=('Choice is not a route: Ceist 2 and Ceist 3 are each A or B, and each section prints two questions, (a) and (b), both '
                                'to be answered; every printed question is one card carrying the printed choice and “Freagair (a) agus (b) anseo.”; '
                                'no combination cards.'),
                  boundaries=('10 whole reading questions with their 20 published parts; 8 literature question cards (2A(a) Hurlamaboc, '
                              '2A(b) Oisín i dTír na nÓg, 2B(a), 2B(b), 3A(a) Géibheann, 3A(b) Colscaradh, 3B(a), 3B(b)); the 5 printed '
                              '2A(a) points, the 6 prescribed-poetry sub-questions and the 4 printed questions inside 3A(a)(i).'))
    return dict(review=review, cards=cards)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    data = build()
    scheme_words_in(data)  # guidance, question and task checks carry the SEC's words only (irish_lifted.py)
    content = json.dumps(data, ensure_ascii=False, indent=2) + '\n'
    if args.check:
        assert OUT.exists() and OUT.read_text() == content, f'Stale output: {OUT}'
    else:
        OUT.write_text(content)
    print(f"Irish Ordinary {YEAR} Paper 2: {len(data['cards'])} reviewed cards (18 printed questions, 35 practice parts); the archive remains incomplete.")


if __name__ == '__main__':
    main()
