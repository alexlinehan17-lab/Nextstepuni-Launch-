#!/usr/bin/env python3
"""Reviewed 2013 Ordinary Paper 2 (Léamhthuiscint agus Litríocht), carded new.

Paper PDF 1–12 and the Paper 2 pages of the combined LC001GLP000IV scheme (PDF 15–28,
plus 29 modified marking) reviewed on 2026-11-05. Counts are assertions, not
corpus-completeness proof. Same method as irish_ordinary_2014_p2.py and, for 2A(a)'s two
prescribed texts and 2B(a)'s optional film or play, irish_ordinary_2017_p2.py.

No 2013 Ordinary card existed before. `build` cards the component the way the reviewed
2014–2026 Ordinary Paper 2s are carded: the ten whole reading questions (each part its
own 5-mark criterion), the nine literature questions (each printed sub-question or
point its own criterion, the 0–4 Gaeilge deduction once), and the practice cards beside
them: every reading part (20), the five printed points of each 2A(a) text (10), every
prescribed-poetry sub-question (6) and the four printed questions inside each poem's
(i) (8).

2013's layout is 2014's: “FREAGAIR GACH CEIST (1, 2 AGUS 3).” Ceist 1 is Léamhthuiscint
A and B (both); Ceist 2 is A (Prós Ainmnithe) or B (Prós Roghnach) and Ceist 3 is A
(Filíocht Ainmnithe) or B (Filíocht Roghnach), each section printing two questions, (a)
and (b), both to be answered (“Freagair (a) agus (b) anseo.”). 2A(a) prints the
prescribed short film Cáca Milis or the prescribed short play An Lasair Choille, each a
summary covering five printed points, which the scheme prices “5 phointe eolais agus 5
mharc ar gach pointe eolais”: under different Atlas headings, a card each (the 2017 form),
every printed point its own 5-mark criterion and practice card (as 2014's Hurlamaboc).
2A(b) is Dís, one 25-mark question. 2B(a) is an optional film or an optional play, which
the scheme marks alike (23 for five points at 5, 5, 5, 4, 4; title 1 + writer 1): one card
carrying both printed alternatives. 2B(b) is an optional short story (protagonist 1 +
five points 22 + title and author 2). 3A is Mo ghrá-sa (idir lúibíní) and An Spailpín
Fánach, each (i) printing four questions (a)–(d) at 2; 3B(a) asks for a modern poem and
3B(b) an old one (“sean-aimseartha”). Each literature card carries the printed choice and
“Freagair (a) agus (b) anseo.” as its task check (choice is not a route; no card combines
two questions), and the section's printed box heading with, for B, the printed
restriction as its lead-in.

The scheme draws its bullets in the SymbolMT font, which the text layer gives as the
private-use U+F0B7; `page_text` reads each span with its font, as irish_ordinary_2013_p1.py
does. The text layer stores each page's boxed heading (“CEIST 1 (A + B) - LÉAMHTHUISCINT -
100 marc”, “A (50 marc)” …) with the page body; `Scheme` removes those exact strings so no
heading lands inside an answer key. 2013 prints no note above the reading questions (each
part prints its own price) and no general literature note, so each criterion carries its
own scheme slice alone.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import re
from pathlib import Path
from irish_lifted import PUA, scheme_words_in, symbol_text

ROOT = Path(__file__).resolve().parents[3]
YEAR = 2013
FILE = 'LC001GLP200IV'
SCHEME_FILE = 'LC001GLP000IV'
OUT = ROOT / 'components/MarkBank/cards/irish/ordinary-2013-p2-authored.json'
SOURCE_REVIEW = ROOT / 'scripts/markbank/authored/irish-ordinary-2013-p2-source-review.json'
REVIEWED_AT = '2026-11-05'
PAPER_SHA = 'cbd576879c6864a3cc8816ca7c04698a7c4d7159dc25529e8cb794dc31252a0c'
SCHEME_SHA = '52406fccffb57cc291d43ab1c4d7ae89fea9dbf246e702125c567bbbccfeeff1'
DIRECTIVE = re.compile(r'rogha|roghna|Freagair|Luaigh|Ainmnigh|\bnó\b|dhá phointe|dhá rud|dhá bh|dhá dh|dhá ch|dhá fh|dhá th|dhá ph|dhá sh|'
                       r'\ban dá\b|ceann amháin|pointe amháin|amháin|\bdhá\b', re.I)
SOURCE_NOTE = 'Shown page-for-page from the official examination paper; swipe to move between pages.'
ATTRIBUTION = '© State Examinations Commission.'
# The scheme's SymbolMT glyphs: U+F0B7 draws its bullet (PDF 15–20).
SYMBOL_FONT = {'': '•', ' ': ' '}
# Boxed page headings the 2013 scheme's text layer stores with the page body (exact strings, each printed once).
FURNITURE = ('Páipéar II (200 marc)', 'CEIST 1 (A + B) - LÉAMHTHUISCINT - 100 marc', 'A (50 marc)', 'B (50 marc)',
             'CEIST 2 PRÓS - AINMNITHE nó ROGHNACH (50 marc)', 'A - PRÓS AINMNITHE - (50 marc)', 'B PRÓS ROGHNACH (50 marc)',
             'CEIST 3 FILÍOCHT - AINMNITHE nó ROGHNACH (50 marc)', 'A - FILÍOCHT AINMNITHE - (50 marc)', 'B – FILÍOCHT ROGHNACH – (50 marc)')
FURNITURE_PATTERN = re.compile('|'.join(r'\s*' + re.escape(h) + r'(?=\s|$)\s*' for h in sorted(FURNITURE, key=len, reverse=True)))
# The literature language note, printed ten times with an en dash and a closing full stop.
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
    """The page's text with each SymbolMT glyph as the character it draws (every glyph is one SYMBOL_FONT reviewed)."""
    lines = []
    for block in page.get_text('dict')['blocks']:
        for line in block.get('lines', []):
            parts = []
            for span in line['spans']:
                text = span['text']
                if span['font'] == 'SymbolMT':
                    assert all(c in SYMBOL_FONT for c in text), ('Unreviewed scheme glyph', page.number + 1, repr(text))
                    text = ''.join(SYMBOL_FONT[c] for c in text)
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
        pages |= {int(m.group(1)) for m in re.finditer(r'⟦(\d+)⟧([^⟦]*)', raw) if clean(m.group(2)) not in ('', 'nó', 'NÓ')}
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


# Two points priced first-correct 3, second 2: “3 mharc + 2 mharc”, printed with or without spaces round the plus.
TWO_POINTS = re.compile(r'3 mharc ?\+ ?2 mharc')
READING_END = '[Gaeilge lochtach: 0 - 5'
# The scheme's note under Reading A 3(a) on the paper's misprint “Bualadh” (for “Buaileadh”): how to mark the answers.
MISPRINT_NOTE = 'Nóta: De bharr earráide ar an scrúdpháipéar'

# (q, part, paper prompt, scheme anchor)
PASSAGES = {
    'A': dict(title='JFK in Éirinn – Caoga Bliain Ó Shin', pages=[4, 5], topic='irish-3-0', start='⟦15⟧', parts=[
        ('1', 'a', '(a) Cén cuairteoir tábhachtach a tháinig chuig an tír seo i mí an Mheithimh 1963? (Alt 1)', '1. (a) Cén cuairteoir tábhachtach'),
        ('1', 'b', '(b) Cé mhéad ama a chaith sé sa tír seo? (Alt 1)', '(b) Cé mhéad ama a chaith sé'),
        ('2', 'a', '(a) Cén áit in Éirinn a raibh cónaí ar ghaolta an Uachtaráin? (Alt 2)', '2. (a) Cén áit in Éirinn'),
        ('2', 'b', '(b) Cad a rinne an tUachtarán i gcistin a chol ceathrair, Mary Ryan? (Alt 2)', '(b) Cad a rinne an tUachtarán i gcistin'),
        ('3', 'a', '(a) Cad a tharla dá bhád patróil, PT-109? (Alt 3)', '3. (a) Cad a tharla dá bhád patróil'),
        ('3', 'b', '(b) Luaigh dhá fháth ar cheap daoine nach mbeadh seans aige an post mar Uachtarán a fháil. (Alt 3)',
         '(b) Luaigh dhá fháth ar cheap daoine'),
        ('4', 'a', '(a) Cad a tharla in Dallas i 1963? (Alt 4)', '4. (a) Cad a tharla in Dallas'),
        ('4', 'b', '(b) Luaigh rud amháin a rinne sé mar Uachtarán agus rud amháin nár éirigh leis a dhéanamh. (Alt 4)',
         '(b) Luaigh rud amháin a rinne sé mar Uachtarán'),
        ('5', 'a', '(a) Cén dá rud a thóg Patrick Kennedy leis go Meiriceá? (Alt 5)', '5. (a) Cén dá rud a thóg Patrick Kennedy'),
        ('5', 'b', '(b) Cad air a bhfuil muintir Loch Garman ag smaoineamh i mbliana? (Alt 5)', '(b) Cad air a bhfuil muintir Loch Garman')]),
    'B': dict(title='Fionnuala Britton – Lúthchleasaí Órga na hÉireann', pages=[6, 7], topic='irish-3-1', start='⟦19⟧', parts=[
        ('1', 'a', '(a) Cad a bhuaigh Fionnuala Britton Dé Domhnaigh, 9 Nollaig 2012? (Alt 1)', '1. (a) Cad a bhuaigh Fionnuala Britton'),
        ('1', 'b', '(b) Tabhair dhá phíosa eolais faoin aimsir an lá sin. (Alt 1)', '(b) Tabhair dhá phíosa eolais faoin aimsir'),
        ('2', 'a', '(a) Cad a rinne Fionnuala nuair a bhí sí seacht mbliana d’aois? (Alt 2)', '2. (a) Cad a rinne Fionnuala nuair'),
        ('2', 'b', '(b) Luaigh dhá spórt a d’imir Fionnuala agus í ar an gColáiste Doiminiceach. (Alt 2)', '(b) Luaigh dhá spórt a d’imir'),
        ('3', 'a', '(a) Cén cúrsa a rinne Fionnuala ar an ollscoil? (Alt 3)', '3. (a) Cén cúrsa a rinne Fionnuala'),
        ('3', 'b', '(b) Cén dá rud ba ghnách le Fionnuala a dhéanamh ag an deireadh seachtaine nuair a bhíodh sí ar an ollscoil? (Alt 3)',
         '(b) Cén dá rud ba ghnách le Fionnuala'),
        ('4', 'a', '(a) Cá ndeachaigh Fionnuala ag traenáil nuair a d’fhág sí an ollscoil? (Alt 4)', '4. (a) Cá ndeachaigh Fionnuala'),
        ('4', 'b', '(b) Cén áit ar chríochnaigh sí i gcraobhrás an deich míle méadar sna Cluichí Oilimpeacha in 2012? (Alt 4)',
         '(b) Cén áit ar chríochnaigh sí'),
        ('5', 'a', '(a) Cén dá aidhm atá ag Fionnuala anois? (Alt 5)', '5. (a) Cén dá aidhm'),
        ('5', 'b', '(b) Cé mhéad míle a ritheann Fionnuala gach seachtain? (Alt 5)', '(b) Cé mhéad míle a ritheann')]),
}

# Printed lines (paper PDF 3, 4, 8–12).
PROSE_CHOICE = 'Freagair A (Prós Ainmnithe) nó B (Prós Roghnach).'
POETRY_CHOICE = 'Freagair A (Filíocht Ainmnithe) nó B (Filíocht Roghnach).'
BOTH = 'Freagair (a) agus (b) anseo.'
BOX_2A, BOX_2B = 'A – PRÓS AINMNITHE – (50 marc)', 'B – PRÓS ROGHNACH – (50 marc)'
BOX_3A, BOX_3B = 'A – FILÍOCHT AINMNITHE – (50 marc)', 'B – FILÍOCHT ROGHNACH – (50 marc)'
NO_PRESCRIBED_PROSE = 'Níl cead aon ábhar a bhaineann le Prós Ainmnithe a úsáid i bhfreagra ar an bPrós Roghnach.'
NO_PRESCRIBED_POETRY = 'Níl cead aon ábhar a bhaineann le Filíocht Ainmnithe a úsáid i bhfreagra ar an bhFilíocht Roghnach.'
STEM_2B = BOX_2B + '\n' + NO_PRESCRIBED_PROSE
STEM_3B = BOX_3B + '\n' + NO_PRESCRIBED_POETRY
FILM_OR_PLAY = 'Freagair na ceisteanna thíos ar an ngearrscannán Cáca Milis nó ar an ngearrdhráma An Lasair Choille.'
# The 2023 builders' requirement lines; irish_lifted.printed_tasks gives each its English.
LIT = ['Freagair gach fochuid atá priontáilte sa rogha seo.', 'Úsáid tagairtí cruinne agus ábhartha don téacs.']
READING_PART = ['Léigh an sliocht iomlán a ghabhann leis an gceist. Freagair an chuid atá luaite ar an gcárta.', 'Úsáid an t-alt a luaitear.']
READING_WHOLE = ['Léigh an sliocht oifigiúil a ghabhann leis an gceist.', 'Freagair gach fochuid agus cloígh leis an alt a luaitear.']

# 2A(a): the prescribed short film or the prescribed short play, a card each, each a summary covering five printed points the
# scheme reprints and prices once, “5 phointe eolais agus 5 mharc ar gach pointe eolais” (each point 2 bare + 3 development).
# (slug, atlas, title, topic, summary line, [(label, printed point)], scheme start, scheme end)
PRESCRIBED_2A = [
    ('prose-2a-a-caca-milis', 'P-2A-a-caca-milis', 'Cáca Milis', 'irish-4-6',
     'Tabhair achoimre ar na heachtraí is mó sa ghearrscannán Cáca Milis.', [
         ('i', 'Déan cur síos ar an gcaint idir Catherine agus a máthair, Theresa, sa charr.'),
         ('ii', 'Déan cur síos ar Paul.'),
         ('iii', 'Cén scéal a insíonn Paul do Catherine faoi bheith ar an raidió?'),
         ('iv', 'Cad a tharlaíonn idir Catherine agus Paul sa charráiste traenach?'),
         ('v', 'Cad a tharlaíonn ag deireadh an ghearrscannáin?')],
     'Cáca Milis Tabhair achoimre', 'NÓ An Lasair Choille Tabhair achoimre'),
    ('prose-2a-a-an-lasair-choille', 'P-2A-a-an-lasair-choille', 'An Lasair Choille', 'irish-4-8',
     'Tabhair achoimre ar na heachtraí is mó sa ghearrdhráma An Lasair Choille.', [
         ('i', 'An chaint a dhéanann Séamas agus Micil ag tús an ghearrdhráma.'),
         ('ii', 'An scéal atá ag Míoda agus an chaint a dhéanann sí féin agus Séamas le chéile.'),
         ('iii', 'Cad a tharlaíonn do Mhíoda ag deireadh an ghearrdhráma?'),
         ('iv', 'Cén pháirt atá ag Binncheol sa ghearrdhráma agus cad a tharlaíonn dó ag an deireadh?'),
         ('v', 'Luaigh fáth amháin a dtaitníonn Micil leat nó fáth amháin nach dtaitníonn Micil leat.')],
     'An Lasair Choille Tabhair achoimre', '(b) Dís'),
]
POINTS_INTRO = 'Luaigh na pointí seo:'
# The tariff each text's key prints under its points: the same sentence, then the split, which the play's key prints with a
# space inside its opening bracket (“( 5 mharc= …”).
EACH_POINT = re.compile(r'5 phointe eolais agus 5 mharc ar gach pointe eolais\. \( ?5 mharc= 2 mharc ar lomphointe eolais agus 3 mharc ar fhorbairt\.\)')
# 2A(b) Dís: the printed quotation (with its printed source word), then the question.
DIS = ('prose-2a-b', 'P-2A-b', 'b', 'Dís', 'irish-4-4',
       ['“Lánúin cois tine tráthnóna...Leanbh ina chodladh sa phram.” Dís',
        'Déan cur síos ar an gcomhrá idir Seán agus a bhean chéile an tráthnóna sin.'],
       '(b) Dís', 'Níl cead aon ábhar a bhaineann le Prós Ainmnithe')
# 2B(a): the optional film or the optional play, one card with both printed alternatives (the scheme marks them alike).
PROSE_2B_A_LINES = [
    '(a) Maidir le scannán roghnach a ndearna tú staidéar air le linn do chúrsa, tabhair achoimre ar na heachtraí is mó ann. (23 marc)',
    'Ní mór teideal an scannáin sin, mar aon le hainm an scríbhneora, a scríobh síos go soiléir. (2 mharc)',
    'NÓ',
    'Maidir le dráma roghnach a ndearna tú staidéar air le linn do chúrsa, tabhair achoimre ar na heachtraí is mó ann. (23 marc)',
    'Ní mór teideal an dráma sin, mar aon le hainm an údair, a scríobh síos go soiléir. (2 mharc)']
# 2B(a) criteria inside each alternative's key: (id, label, marks, cut-before).
PROSE_2B_A_PARTS = [('eolas', 'Na heachtraí is mó', 23, '5 phointe eolais ag teastáil'), ('teideal', 'Teideal + ainm an scríbhneora / an údair', 2, 'Ní mór teideal')]
# 2B(b): the optional short story (protagonist 1, five points 22, title and author 2).
PROSE_2B_B = (['(b) Maidir le gearrscéal roghnach a ndearna tú staidéar air le linn do chúrsa, ainmnigh an príomhcharachtar (an phríomhphearsa) ann. '
               'Tabhair cuntas ar an bpríomhcharachtar (ar an bpríomhphearsa) ó thús deireadh an ghearrscéil. (23 marc)',
               'Ní mór teideal an ghearrscéil sin, mar aon le hainm an údair, a scríobh síos go soiléir. (2 mharc)'],
              '(b) Maidir le gearrscéal roghnach', 'Freagair (a) agus (b) anseo. Mo ghrá-sa',
              [('priomhcharachtar', 'An príomhcharachtar', 1, 'An príomhcharachtar (an phríomhphearsa) = 1 mharc'),
               ('eolas', 'Cuntas ar an bpríomhcharachtar', 22, 'Cuntas ar an bpríomhcharachtar'),
               ('teideal', 'Teideal + ainm an údair', 2, 'Ní mór teideal')])
# 3A: (slug, atlas, page, title, topic, [(label, paper prompt, marks, scheme cut, printed price in the key)], scheme start, scheme end)
POETRY_3A = [
    ('poetry-3a-a', 'F-3A-a', 10, 'Mo ghrá-sa (idir lúibíní)', 'irish-5-4', [
        ('i', '(a) Cad a deir an file faoin bhfear i véarsa a haon?\n(b) Cá bhfásfaidh na nóiníní?\n(c) Céard atá mícheart le súile an fhir?\n'
              '(d) Cad iad na torthaí a thugann an fear don fhile?', 8, '(i) (a) Cad a deir an file', '(2 mharc)'),
        ('ii', 'Inis i d’fhocail féin, cén saghas duine é an fear? (Is leor dhá phointe eolais.)', 8,
         '(ii) Inis i d’fhocail féin, cén saghas duine', '(2 phointe eolais ar 4 mharc an ceann)'),
        ('iii', 'Luaigh rud amháin a thaitin leat agus rud amháin nár thaitin leat faoin dán seo.', 9,
         '(iii) Luaigh rud amháin a thaitin leat', '(5 mharc ar an gceann is fearr + 4 mharc ar an gceann eile)')],
     'Mo ghrá-sa (idir lúibíní) (a) (i)', 'An Spailpín Fánach (b) (i)'),
    ('poetry-3a-b', 'F-3A-b', 11, 'An Spailpín Fánach', 'irish-5-1', [
        ('i', '(a) Cad a dhéanann an file “go moch ar maidin”?\n(b) Luaigh dhá áit ina mbíodh an spailpín.\n'
              '(c) Cad a chloiseann an spailpín na daoine á rá nuair a théann sé go Durlas?\n(d) Cén cheist a bhíonn ag “bodairí na tíre”?', 8,
         '(i) (a) Cad a dhéanann an file', '(2 mharc)'),
        ('ii', 'Inis i d’fhocail féin, cén sórt saoil a bhí ag an spailpín? (Is leor dhá phointe eolais.)', 8,
         '(ii) Inis i d’fhocail féin, cén sórt saoil', '= (4 mharc +4 mharc)'),
        ('iii', 'An maith leat an dán seo? Cuir fáthanna le do fhreagra. (Is leor dhá fháth.)', 9,
         '(iii) An maith leat an dán seo?', 'Is maith / Ní maith = (1 mharc) + dhá fháth = (4 mharc + 4 mharc)')],
     'An Spailpín Fánach (b) (i)', EXAMINER_NOTE),
]
# Each poem's (i) prints four questions (a)–(d) at 2 each: (slug, sub-question) -> [(letter, scheme question, marks, next cut)]
SLOTS_3A = {
    ('poetry-3a-a', 'i'): [('a', 'Cad a deir an file faoin bhfear i véarsa a haon?', 2, '(b) Cá bhfásfaidh'),
                           ('b', 'Cá bhfásfaidh na nóiníní?', 2, '(c) Céard atá mícheart'),
                           ('c', 'Céard atá mícheart le súile an fhir?', 2, '(d) Cad iad na torthaí'),
                           ('d', 'Cad iad na torthaí a thugann an fear don fhile?', 2, None)],
    ('poetry-3a-b', 'i'): [('a', 'Cad a dhéanann an file “go moch ar maidin”?', 2, '(b) Luaigh dhá áit'),
                           ('b', 'Luaigh dhá áit ina mbíodh an spailpín.', 2, '(c) Cad a chloiseann'),
                           ('c', 'Cad a chloiseann an spailpín na daoine á rá nuair a théann sé go Durlas?', 2, '(d) Cén cheist'),
                           ('d', 'Cén cheist a bhíonn ag “bodairí na tíre”?', 2, None)],
}
POETRY_3B = [
    ('poetry-3b-a', 'F-3B-a', 'nua-aimseartha', [
        '(i) Maidir le dán roghnach nua-aimseartha amháin a ndearna tú staidéar air le linn do chúrsa, inis i d’fhocail féin, cad is téama '
        'don dán sin, dar leat? (7 marc)',
        '(ii) Roghnaigh dhá íomhá (phictiúr) a úsáideann an file sa dán seo agus déan cur síos orthu i d’fhocail féin. (8 marc)',
        '(iii) Luaigh rud amháin a thaitin leat agus rud amháin nár thaitin leat faoin dán seo. (8 marc)'],
     '(a) (i) Maidir le dán roghnach nua-aimseartha amháin', '(b) (i) Maidir le dán roghnach sean-aimseartha',
     ['(ii) Roghnaigh dhá íomhá', '(iii) Luaigh rud amháin', 'Ní mór teideal an dáin'], (7, 8, 8)),
    ('poetry-3b-b', 'F-3B-b', 'sean-aimseartha', [
        '(i) Maidir le dán roghnach sean-aimseartha amháin a ndearna tú staidéar air le linn do chúrsa, inis i d’fhocail féin, cad iad '
        'príomhsmaointe an dáin? (8 marc)',
        '(ii) Cén mothú is mó atá sa dán, dar leat? Cuir fáthanna le do fhreagra. (Is leor dhá fháth.) (6 mharc)',
        '(iii) An maith leat an dán seo? Cuir fáthanna le do fhreagra. (Is leor dhá fháth.) (9 marc)'],
     '(b) (i) Maidir le dán roghnach sean-aimseartha', EXAMINER_NOTE,
     ['(ii) Cén mothú is mó', '(iii) An maith leat an dán seo?', 'Ní mór teideal an dáin'], (8, 6, 9)),
]
TITLE_LINE = 'Ní mór teideal an dáin sin, mar aon le hainm an fhile, a scríobh síos go soiléir. (2 mharc)'

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
    s = Scheme(doc, 15, 28)
    assert s.removed == len(FURNITURE), s.removed
    assert not PUA.search(s.text), 'private-use glyph left in the scheme text'
    assert 'Níl sé i gceist a chur in iúl' not in s.text, '2013 prints no general literature note'
    assert 'Nóta: Má tá dhá phointe eolais' not in s.text, '2013 prints no note above the reading questions'
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
            # Every part prints its 5, or its split (B 1(b), B 3(b): “3 mharc+2 mharc”), or (A 4(b)) its two answers' prices 3 and 2.
            assert ('5 mharc' in chunk or TWO_POINTS.search(chunk)
                    or (letter, q, part) == ('A', '4', 'b') and '= 3 mharc' in chunk and '= 2 mharc' in chunk), (letter, q, part)
            assert '50 marc' not in chunk and 'LÉAMHTHUISCINT' not in chunk and 'Gearrfar' not in chunk, (letter, q, part, chunk[:80])
            two = bool(TWO_POINTS.search(chunk))
            permitted = [0, 3, 5] if (two or '= 3 mharc' in chunk) else [0, 5]
            # A 3(a): the scheme's note on the paper's misprint is its own printed block, after the answers.
            lines = [chunk]
            if MISPRINT_NOTE in chunk:
                assert (letter, q, part) == ('A', '3', 'a')
                at = chunk.index(MISPRINT_NOTE)
                lines = [chunk[:at].strip(), chunk[at:]]
                assert lines[1].endswith('Ná cuir an earraíd seo san áireamh agus tú ag measúnú chaighdéan Gaeilge na bhfreagraí.'), lines[1][-80:]
            resolved.append((q, part, prompt, lines, spages, two, permitted))
        passage['resolved'] = resolved
    # Cáca Milis, An Lasair Choille, Dís, the 2B film, the 2B play, 2B(b), Mo ghrá-sa, An Spailpín Fánach, 3B(a), 3B(b): ten.
    assert len(LANG_LIT.findall(s.text)) == 10, len(LANG_LIT.findall(s.text))
    assert in_order(FILM_OR_PLAY, texts[7]) and in_order(FILM_OR_PLAY, s.text)
    for slug, atlas, title, topic, summary, points, start, end in PRESCRIBED_2A:
        for line in [title, summary, POINTS_INTRO] + [f'({label}) {p}' for label, p in points] + ['(25 marc)']:
            assert in_order(line, texts[7]), (slug, line[:40])
    slug, atlas, letter, title, topic, lines, start, end = DIS
    assert in_order(f'({letter}) {title} ' + ' '.join(lines) + ' (25 marc)', texts[7]), slug
    for line in PROSE_2B_A_LINES + PROSE_2B_B[0]:
        assert in_order(line, texts[8]), line[:50]
    for slug3, atlas3, page, title3, topic3, subs3, start3, end3 in POETRY_3A:
        assert in_order(title3, texts[page - 1]), slug3
        for label, prompt, marks, cut, price in subs3:
            assert in_order(f'({label}) ' + prompt.replace('\n', ' ') + f' ({marks} marc)', texts[page - 1]), (slug3, label)
    for slug4, atlas4, kind4, prompts, start4, end4, cuts4, marks4 in POETRY_3B:
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


def prescribed_key(m, slug, title, points, start, end):
    """The scheme's reprint of each printed point, and the one tariff it prints for all five, then its language note."""
    whole, spages = m['s'].chunk(start, end)
    lang = language_note(whole)
    whole = before_language_note(whole)
    pieces = split_at(whole, [f'({label}) {p}' for label, p in points], slug)
    # Each printed point's reprint is its own line; the last one runs on into the question's total and the tariff.
    lines = [f'({label}) {p}' for label, p in points]
    assert all(piece == line for piece, line in zip(pieces[:-1], lines[:-1])), pieces
    tail = pieces[-1][len(lines[-1]):].strip()
    assert pieces[-1].startswith(lines[-1]) and tail.startswith('(25 marc) ') and EACH_POINT.fullmatch(tail[len('(25 marc) '):]), pieces[-1]
    return lines, tail[len('(25 marc) '):], spages, lang


def poem_pieces(m, slug, subs, start, end):
    whole, spages = m['s'].chunk(start, end)
    lang = language_note(whole)
    whole = before_language_note(whole)
    pieces = split_at(whole, [cut for _, _, _, cut, _ in subs], slug)
    for (label, _, marks, _, price), piece in zip(subs, pieces):
        assert price in piece, (slug, label, piece[:60])
    return pieces, spages, lang


SPLIT = re.compile(r'(\d) mharc \+ (\d) mharc')


def slot_pieces(piece, slots):
    out = []
    for sub, question, marks, nxt in slots:
        start_at = piece.index(question)
        slot = piece[start_at:piece.index(nxt, start_at) if nxt else len(piece)].strip()
        # 2013 prints each question's price in brackets (“(2 mharc)”), then its sample answers (“Freagraí samplacha:”) or its
        # answers with a printed split (“= 1 mharc + 1 mharc”, “(1 mharc + 1 mharc)”).
        assert f'{question} ({marks} mharc)' in slot and (re.search(r'Freagraí samplacha:', slot) or SPLIT.search(slot)), (sub, slot[:80])
        out.append((sub, slot))
    return out


def slot_permitted(slot, marks):
    """0, the slot's mark, and every partial price its key prints (each term of a printed split); a question whose key prints
    only its mark and sample answers takes 0 or its mark (coordinator ruling, 5 November 2026)."""
    values = {0, marks} | {int(v) for v in re.findall(r'= (\d) mharc', slot)}
    values |= {int(v) for split in SPLIT.findall(slot) for v in split}
    return sorted(v for v in values if v <= marks)


WHOLE_PROSE_NOTE = ('One complete SEC response: five points at 5 (2 for the bare point + 3 for development); the 0–4 Gaeilge deduction applies once '
                    'to this whole 25-mark answer. The scheme prints no sample points; the answer is judged on merit against that allocation.')
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
        for q, part, prompt, lines, spages, two, permitted in passage['resolved']:
            by_q.setdefault(q, []).append((part, prompt, lines, spages, permitted))
        for q, parts in by_q.items():
            text = f'{q}. ' + ' '.join(prompt for _, prompt, *_ in parts)
            crits = [criterion(part, f'({part}) Freagra', 5, lines, permitted=permitted) for part, _, lines, _, permitted in parts]
            # The frozen Atlas identities 1–5 (A) and 6–10 (B) are the whole questions.
            add(str(int(q) + (5 if letter == 'B' else 0)), f'reading-{letter.lower()}-q{q}', f'Léamhthuiscint {letter} · Ceist {q}', text,
                passage['topic'], passage['pages'], sorted({p for *_, sp, _ in parts for p in sp}), crits, READING_WHOLE,
                'Complete printed question: (a) 5 + (b) 5, each scored separately at its SEC allocation. ' + reading_note(m), src,
                concept=f'irish-reading-{letter.lower()}-q{q}')
            whole_ids.append(cards[-1]['id'])
    for letter, passage in PASSAGES.items():
        src = source(f'Léamhthuiscint {letter}', passage['title'], passage['pages'])
        for q, part, prompt, lines, spages, two, permitted in passage['resolved']:
            add(f'R-{letter}-{q}-{part}', f'reading-{letter.lower()}-q{q}-{part}', f'Léamhthuiscint {letter} · Ceist {q}({part})',
                f'{q}{prompt}', passage['topic'], passage['pages'], spages,
                [criterion(part, 'Freagra', 5, lines, permitted=permitted)], READING_PART,
                'SEC allocation for this part' + (': first correct point 3, second 2 (0/3/5).' if two else '.') + ' ' + reading_note(m), src)
            practice_ids.append(cards[-1]['id'])

    sub_note = 'One printed sub-question at its published tariff. ' + LIT_DEDUCTION_NOTE
    question_lit = []
    # ---- Ceist 2A: (a) Cáca Milis or An Lasair Choille (a card each, five printed points), (b) Dís -------------
    prescribed = {}
    for slug, atlas, title, topic, summary, points, start, end in PRESCRIBED_2A:
        lines, each, spages, lang = prescribed_key(m, slug, title, points, start, end)
        prescribed[slug] = (lines, each, spages)
        head = f'(a) {FILM_OR_PLAY}\n{title}\n{summary}\n{POINTS_INTRO}'
        add(atlas, slug, f'Prós 2A(a) · {title}', head + '\n' + '\n'.join(f'({l}) {p}' for l, p in points) + '\n(25 marc)', topic, [8], spages,
            [criterion(f'eolas-{label}', f'({label}) Eolas', 5, [line, each], 'indicative') for (label, _), line in zip(points, lines)]
            + [deduction(lang)], [PROSE_CHOICE, BOTH, FILM_OR_PLAY] + LIT,
            'One complete SEC response: a summary covering the five printed points, each a point of information at 5 (2 for the bare point + 3 '
            f'for development), then the 0–4 Gaeilge deduction once. The scheme prints no sample answers for {title}; each point is judged on '
            'merit against that split.', source('Prós Ainmnithe', title, [8]), concept=f'irish-prose-2a-{topic}', stem=BOX_2A)
        question_lit.append(cards[-1]['id'])
    slug_d, atlas_d, letter_d, title_d, topic_d, lines_d, start_d, end_d = DIS
    chunk_d, dpages = m['s'].chunk(start_d, end_d)
    lang_d = language_note(chunk_d)
    key_d = before_language_note(chunk_d)
    assert key_d.endswith('(25 marc) 5 phointe eolais agus 5 mharc ar gach pointe eolais. (5 mharc= 2 mharc ar lomphointe eolais agus 3 mharc ar fhorbairt.)'), key_d[-160:]
    add(atlas_d, slug_d, f'Prós 2A({letter_d}) · {title_d}', f'({letter_d}) {title_d}\n' + '\n'.join(lines_d) + ' (25 marc)', topic_d, [8], dpages,
        [criterion('eolas', 'Eolas', 25, [key_d], 'indicative'), deduction(lang_d)], [PROSE_CHOICE, BOTH] + LIT[1:],
        WHOLE_PROSE_NOTE, source('Prós Ainmnithe', title_d, [8]), concept=f'irish-prose-2a-{topic_d}', stem=BOX_2A)
    question_lit.append(cards[-1]['id'])

    # ---- Ceist 2B: Prós Roghnach (a) the optional film or play, (b) the optional short story -------------------
    film, fpages = m['s'].chunk('Maidir le scannán roghnach a ndearna tú', 'NÓ Maidir le dráma roghnach')
    play, ppages = m['s'].chunk('Maidir le dráma roghnach a ndearna tú', '(b) Maidir le gearrscéal roghnach')
    alternatives = []
    for alt, lead in ((film, PROSE_2B_A_LINES[0][4:]), (play, PROSE_2B_A_LINES[3])):
        language_note(alt)
        alt = before_language_note(alt)
        cuts = [alt.index(cut) for _, _, _, cut in PROSE_2B_A_PARTS]
        reprint = alt[:cuts[0]].strip()
        assert in_order(lead, reprint), reprint[:80]
        bits = [alt[a:b].strip() for a, b in zip(cuts, cuts[1:] + [len(alt)])]
        assert bits[0].startswith('5 phointe eolais ag teastáil (5 mharc an ceann ar an gcéad trí phointe eolais+ 4 mharc an ceann ar an dá phointe eolais eile)'), bits[0]
        assert bits[1].endswith('= 1 mharc (2 mharc)'), bits[1]
        alternatives.append(bits)
    # The film's and the play's points are priced in the same printed words: lifted once. Their title lines differ (“an
    # scannáin … an scríbhneora”, “an dráma … an údair”): both are lifted.
    assert alternatives[0][0] == alternatives[1][0], alternatives
    guidance = [[alternatives[0][0]], [alternatives[0][1], alternatives[1][1]]]
    crits = [criterion(cid, label, marks, guidance[i], 'exact' if cid == 'teideal' else 'indicative',
                       permitted=None if cid == 'eolas' else sorted({0, marks} | {int(v) for v in re.findall(r'= (\d) mharc', guidance[i][0])}))
             for i, (cid, label, marks, _) in enumerate(PROSE_2B_A_PARTS)]
    add('P-2B-a', 'prose-2b-a', 'Prose 2B(a)', '\n'.join(PROSE_2B_A_LINES), 'irish-4-7', [9], sorted(set(fpages) | set(ppages)),
        crits + [deduction(LANG_LIT_TEXT)], [PROSE_CHOICE, NO_PRESCRIBED_PROSE, BOTH] + LIT[1:],
        'One complete SEC response about an optional film or an optional play (the scheme marks both alike): 23 for the main events in five '
        'points (5, 5, 5, 4, 4) and 2 for the title and the writer (1 + 1), then the 0–4 Gaeilge deduction once. The text is open content '
        'chosen by the candidate (indicative rather than exhaustive).',
        source('Prós Roghnach', 'Scannán nó dráma roghnach', [9]), concept='irish-prose-2b-irish-4-7', stem=STEM_2B)
    question_lit.append(cards[-1]['id'])
    lines2, start2, end2, parts2 = PROSE_2B_B
    chunk2, spages2 = m['s'].chunk(start2, end2)
    lang2 = language_note(chunk2)
    chunk2 = before_language_note(chunk2)
    cuts = [chunk2.index(part[3]) for part in parts2]
    assert cuts == sorted(cuts)
    reprint = chunk2[:cuts[0]].strip()
    assert all(in_order(line.replace(' (2 mharc)', ''), reprint) for line in lines2[:1]), reprint[:80]
    bits = [chunk2[a:b].strip() for a, b in zip(cuts, cuts[1:] + [len(chunk2)])]
    assert bits[0] == 'An príomhcharachtar (an phríomhphearsa) = 1 mharc' and bits[2].endswith('Ainm an údair = 1 mharc'), bits
    crits = [criterion(cid, label, marks, [bit], 'exact' if cid in ('teideal', 'priomhcharachtar') else 'indicative',
                       permitted=None if cid == 'eolas' else sorted({0, marks} | {int(v) for v in re.findall(r'= (\d) mharc', bit)}))
             for (cid, label, marks, _), bit in zip(parts2, bits)]
    add('P-2B-b', 'prose-2b-b', 'Prose 2B(b)', '\n'.join(lines2), 'irish-4-7', [9], spages2, crits + [deduction(lang2)],
        [PROSE_CHOICE, NO_PRESCRIBED_PROSE, BOTH] + LIT[1:],
        'One complete SEC response: the main character 1, 22 for an account of that character in five points (5, 5, 4, 4, 4) and 2 for the '
        'title and the author (1 + 1), then the 0–4 Gaeilge deduction once. The optional text is open content chosen by the candidate; the '
        'scheme prints no sample points for it, so its points are judged on merit against these allocations (indicative rather than exhaustive).',
        source('Prós Roghnach', 'Gearrscéal roghnach', [9]), concept='irish-prose-2b-irish-4-7', stem=STEM_2B)
    question_lit.append(cards[-1]['id'])

    # ---- Ceist 3A: Mo ghrá-sa (idir lúibíní) and An Spailpín Fánach -------------------------------------------
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
            ' at their printed tariffs, then the 0–4 Gaeilge deduction once. The sample answers are indicative rather than exhaustive.',
            source('Filíocht Ainmnithe', title3, [page]), concept=f'irish-poetry-3a-{topic3}', stem=BOX_3A)
        question_lit.append(cards[-1]['id'])

    # ---- Ceist 3B: Filíocht Roghnach (a) a modern poem and (b) an old one --------------------------------------
    for slug4, atlas4, kind4, prompts, start4, end4, cuts4, marks4 in POETRY_3B:
        chunk4, spages4 = m['s'].chunk(start4, end4, m['s'].text.index('⟦27⟧'))
        lang4 = language_note(chunk4)
        chunk4 = before_language_note(chunk4)
        idx = [0] + [chunk4.index(cut) for cut in cuts4]
        bits = [chunk4[a:b].strip() for a, b in zip(idx, idx[1:] + [len(chunk4)])]
        for bit, mk in zip(bits, list(marks4) + [2]):
            assert f'({mk} {"mharc" if mk in (2, 6) else "marc"})' in bit, (slug4, mk, bit[-60:])
        assert bits[3] == TITLE_LINE, bits[3]
        crits = [criterion('eolas-i', '(i) Eolas', marks4[0], [bits[0]], 'indicative'),
                 criterion('eolas-ii', '(ii) Eolas', marks4[1], [bits[1]], 'indicative'),
                 criterion('eolas-iii', '(iii) Eolas', marks4[2], [bits[2]], 'indicative'),
                 # 2013 prints the title and poet line with its (2 mharc) and no split: 0 or 2 (coordinator ruling, 5 November 2026).
                 criterion('teideal', 'Teideal + ainm an fhile', 2, [bits[3]], 'exact', permitted=[0, 2])]
        add(atlas4, slug4, f'Poetry 3B({atlas4[-1]})', f'({atlas4[-1]}) ' + '\n'.join(prompts + [TITLE_LINE]), 'irish-5-6', [12], spages4,
            crits + [deduction(lang4)], [POETRY_CHOICE, NO_PRESCRIBED_POETRY, BOTH] + LIT,
            f'One complete SEC response: (i) {marks4[0]}, (ii) {marks4[1]}, (iii) {marks4[2]}, poem and poet 2, then the 0–4 Gaeilge deduction once. '
            f'3B({atlas4[-1]}) asks for {"a modern" if kind4 == "nua-aimseartha" else "an old"} poem (“{kind4}”). The optional poem is open '
            'content; the printed allocations are judged on merit (indicative rather than exhaustive).',
            source('Filíocht Roghnach', f'3B({atlas4[-1]}) · Dán roghnach', [12]),
            concept='irish-poetry-3b-irish-5-6', stem=STEM_3B)
        question_lit.append(cards[-1]['id'])

    # ---- Practice: the five points of each 2A(a) text, every prescribed-poetry sub-question, each (i)(a)–(d) -----
    for slug, atlas, title, topic, summary, points, start, end in PRESCRIBED_2A:
        lines, each, spages = prescribed[slug]
        head = f'(a) {FILM_OR_PLAY}\n{title}\n{summary}\n{POINTS_INTRO}'
        for (label, prompt), line in zip(points, lines):
            add(f'{atlas}-{label}', f'{slug}-{label}', f'Prós 2A(a) · {title} · ({label})', head + f'\n({label}) {prompt}',
                topic, [8], spages, [criterion('eolas', 'Eolas', 5, [line, each], 'indicative')],
                [PROSE_CHOICE, BOTH, FILM_OR_PLAY] + LIT[1:],
                'One of the five printed points the summary covers, at the scheme’s 5 for each point of information. ' + LIT_DEDUCTION_NOTE,
                source('Prós Ainmnithe', title, [8]), stem=BOX_2A,
                focus=f'Point ({label}) of the five the summary must cover (5 marks: 2 for the bare point, 3 for developing it)')
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

    assert len(whole_ids) == 10 and len(question_lit) == 9 and len(practice_ids) == 44, (len(whole_ids), len(question_lit), len(practice_ids))
    assert len(cards) == 63 and len({c['id'] for c in cards}) == 63 and len({c['atlasQuestionId'] for c in cards}) == 63
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
                                'to be answered; 2A(a)’s two prescribed texts (Cáca Milis, An Lasair Choille) are a card each and 2B(a)’s optional film or '
                                'play, which the scheme marks alike, is one card; every printed question is one card carrying the printed choice and '
                                '“Freagair (a) agus (b) anseo.”; no combination cards.'),
                  boundaries=('10 whole reading questions with their 20 published parts; 9 literature questions (2A(a) Cáca Milis, 2A(a) An Lasair '
                              'Choille, 2A(b) Dís, 2B(a), 2B(b), 3A(a) Mo ghrá-sa (idir lúibíní), 3A(b) An Spailpín Fánach, 3B(a), 3B(b)); the 5 '
                              'printed points of each 2A(a) text, the 6 prescribed-poetry sub-questions and the 4 printed questions inside each '
                              'poem’s (i).'))
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
    print(f"Irish Ordinary {YEAR} Paper 2: {len(data['cards'])} reviewed cards (19 printed questions, 44 practice parts); the archive remains incomplete.")


if __name__ == '__main__':
    main()
