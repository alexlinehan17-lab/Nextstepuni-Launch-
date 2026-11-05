#!/usr/bin/env python3
"""Reviewed 2015 Ordinary Paper 2 (Léamhthuiscint agus Litríocht), carded new.

Paper PDF 1–12 and the Paper 2 pages of the combined LC001GLP000IV scheme (PDF 12–20,
plus 21 with the closing 3B note and the modified marking) reviewed on 2026-11-05.
Counts are assertions, not corpus-completeness proof. Same method as
irish_ordinary_2016_p2.py and irish_ordinary_2017_p2.py.

No 2015 Ordinary card existed before. `build` cards the component the way the reviewed
2016–2026 Ordinary Paper 2s are carded: the ten whole reading questions (each part its
own 5-mark criterion), the eight literature questions (each printed sub-question its own
criterion where the scheme prices it, the 0–4 Gaeilge deduction once), and the practice
cards beside them: every reading part (20), every prescribed-poetry sub-question (6) and
the four printed questions inside 3A(b)(i) An tEarrach Thiar.

2015's layout is 2016's and 2017's: “FREAGAIR GACH CEIST (1, 2 AGUS 3).” Ceist 1 is
Léamhthuiscint A and B (both); Ceist 2 is A (Prós Ainmnithe) or B (Prós Roghnach) and
Ceist 3 is A (Filíocht Ainmnithe) or B (Filíocht Roghnach), each section printing two
questions, (a) and (b), both to be answered (“Freagair (a) agus (b) anseo.”). 2A(a) is
Oisín i dTír na nÓg, a summary that must cover five printed points (i)–(v); the scheme
prices the summary as five points (7, 7, 7, 2, 2), never one printed point, so it is one
25-mark card and its points are not carded apart. 2A(b) is Hurlamaboc, one 25-mark
question priced the same way. 2B(a) is an optional folk tale (23 + title 2) and 2B(b) an
optional novel extract (23 + title and author 2). 3A is Mo ghrá-sa (idir lúibíní) and An
tEarrach Thiar, whose (i) prints four questions (a)–(d) at 2 each; 3B(a) asks for a
modern poem by a woman and 3B(b) one by a man. 2015 prints no film or play question.
Each literature card carries the printed choice and “Freagair (a) agus (b) anseo.” as
its task check (choice is not a route; no card combines two questions), and the
section's printed box heading with, for B, the printed restriction as its lead-in.

The scheme's text layer stores each page's boxed heading (“Páipéar II (200 marc)”,
“CEIST 1 (A + B) - LÉAMHTHUISCINT -100 marc”, “A – (50 marc)” …) with the page body;
`Scheme` removes those exact strings so no heading lands inside an answer key. 2015
prints no general literature note and no two-point note above the reading passages, so
each criterion carries its own scheme slice alone.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import re
from pathlib import Path
from irish_lifted import PUA, scheme_words_in, symbol_text

ROOT = Path(__file__).resolve().parents[3]
YEAR = 2015
FILE = 'LC001GLP200IV'
SCHEME_FILE = 'LC001GLP000IV'
OUT = ROOT / 'components/MarkBank/cards/irish/ordinary-2015-p2-authored.json'
SOURCE_REVIEW = ROOT / 'scripts/markbank/authored/irish-ordinary-2015-p2-source-review.json'
REVIEWED_AT = '2026-11-05'
PAPER_SHA = '6b3fe307053a05bffe819c8f0b177150216b45eaf4c184a4949556bf73f16aa9'
SCHEME_SHA = '48dda60cd9b804a0c7b41dc8e265a05835fff88c9e8dc8564f084fbfe173621d'
DIRECTIVE = re.compile(r'rogha|roghna|Freagair|Luaigh|Ainmnigh|\bnó\b|dhá phointe|dhá rud|dhá bh|dhá dh|dhá ch|dhá fh|dhá th|dhá ph|dhá sh|'
                       r'\ban dá\b|ceann amháin|pointe amháin|amháin|\bdhá\b', re.I)
SOURCE_NOTE = 'Shown page-for-page from the official examination paper; swipe to move between pages.'
ATTRIBUTION = '© State Examinations Commission.'
# Boxed page headings the 2015 scheme's text layer stores with the page body (exact strings, each printed once).
FURNITURE = ('Páipéar II (200 marc)', 'CEIST 1 (A + B) - LÉAMHTHUISCINT -100 marc', 'A – (50 marc)', 'B – (50 marc)',
             'CEIST 2 PRÓS – AINMNITHE nó ROGHNACH – (50 marc)', 'A – PRÓS AINMNITHE – (50 marc)', 'B – PRÓS ROGHNACH – (50 marc)',
             'CEIST 3 FILÍOCHT – AINMNITHE nó ROGHNACH – (50 marc)', 'A – FILÍOCHT AINMNITHE – (50 marc)', 'B – FILÍOCHT ROGHNACH – (50 marc)')
FURNITURE_PATTERN = re.compile('|'.join(r'\s*' + re.escape(h) + r'(?=\s|$)\s*' for h in sorted(FURNITURE, key=len, reverse=True)))


def clean(text):
    return re.sub(r'\s+', ' ', symbol_text(text)).strip()


def comparable(text):
    return re.sub(r'[^\w]+', '', text.lower())


def in_order(prompt, text):
    return re.search('.*?'.join(re.escape(comparable(w)) for w in prompt.split() if comparable(w)), comparable(text))


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
            body = re.sub(r'^\d+\s', '', clean(doc[p - 1].get_text()))
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


def split_at(text, cuts, slug):
    idx = [text.index(cut) for cut in cuts]
    assert idx == sorted(idx), slug
    return [text[a:b].strip() for a, b in zip(idx, idx[1:] + [len(text)])]


# Two points priced first-correct 3, second 2: “3 mharc + 2 mharc”, or the bare “5 mharc” followed by
# “An chéad … atá ceart = 3 mharc; an dara … atá ceart = 2 mharc”.
TWO_POINTS = re.compile(r'3 mharc \+ 2 mharc|; an dara [^=;]+ atá ceart = 2 mharc')

# (q, part, paper prompt, scheme anchor)
PASSAGES = {
    'A': dict(title='Rory McIlroy - Galfaire na Bliana 2014', pages=[4, 5], topic='irish-3-0', start='⟦12⟧',
              end='Nóta: Gearrfar pionós i ngeall ar iomarcaíocht. Léireofar', parts=[
        ('1', 'a', '(a) Tabhair dhá phíosa eolais faoin mbliain iontach a bhí ag an ngalfaire Rory McIlroy in 2014. (Alt 1)',
         '1. (a) Tabhair dhá phíosa eolais faoin mbliain'),
        ('1', 'b', '(b) Cén gaisce atá déanta ag Rory mar ghalfaire Eorpach? (Alt 1)', '(b) Cén gaisce atá déanta'),
        ('2', 'a', '(a) Scríobh síos dhá rud a chabhraigh go mór le Rory galf a chleachtadh nuair a bhí sé óg. (Alt 2)',
         '2. (a) Scríobh síos dhá rud a chabhraigh'),
        ('2', 'b', '(b) Cad a rinne Rory sa bhliain 2007? (Alt 2)', '(b) Cad a rinne Rory sa bhliain 2007'),
        ('3', 'a', '(a) Is breá le lucht na meán Rory. Cén fáth? (Alt 3)', '3. (a) Is breá le lucht na meán'),
        ('3', 'b', '(b) Cén scór a bhí ag Rory nuair a bhuaigh sé Craobh Oscailte na Stát Aontaithe? (Alt 3)', '(b) Cén scór a bhí ag Rory'),
        ('4', 'a', '(a) Cá dtéann Rory nuair a bhíonn am saor aige? (Alt 4)', '4. (a) Cá dtéann Rory'),
        ('4', 'b', '(b) Cad a dúirt Rory go poiblí sna meáin tamall ó shin? (Alt 4)', '(b) Cad a dúirt Rory go poiblí'),
        ('5', 'a', '(a) Luaigh dhá chúis a bhfuil Rory an-saibhir anois. (Alt 5)', '5. (a) Luaigh dhá chúis'),
        ('5', 'b', '(b) Cén obair a dhéanann The Rory Foundation? (Alt 5)', '(b) Cén obair a dhéanann The Rory Foundation')]),
    'B': dict(title='Hillary Clinton agus Rás 2016 chuig an Teach Bán', pages=[6, 7], topic='irish-3-1', start='⟦14⟧',
              end='Nóta: Gearrfar pionós i ngeall ar iomarcaíocht. Léireofar', parts=[
        ('1', 'a', '(a) Cad a dhéanann muintir Stáit Aontaithe Mheiriceá i mí na Samhna gach ceathrú bliain? (Alt 1)', '1. (a) Cad a dhéanann muintir'),
        ('1', 'b', '(b) Ainmnigh an dá phríomhpháirtí polaitíochta sna Stáit Aontaithe. (Alt 1)', '(b) Ainmnigh an dá phríomhpháirtí'),
        ('2', 'a', '(a) Cathain a rugadh Hillary Rodham? (Alt 2)', '2. (a) Cathain a rugadh'),
        ('2', 'b', '(b) Cén fáth ar fhág Hillary Rodham an páirtí Poblachtach? (Alt 2)', '(b) Cén fáth ar fhág Hillary'),
        ('3', 'a', '(a) Scríobh síos dhá phíosa eolais faoi Arkansas. (Alt 3)', '3. (a) Scríobh síos dhá phíosa eolais faoi Arkansas'),
        ('3', 'b', '(b) Luaigh an dá rud a rinne Hillary chun cúrsaí oideachais a fheabhsú in Arkansas. (Alt 3)', '(b) Luaigh an dá rud a rinne Hillary'),
        ('4', 'a', '(a) Cén obair a rinne Hillary nuair a bhí sí mar Chéad-Bhean Mheiriceá? (Alt 4)', '4. (a) Cén obair a rinne Hillary'),
        ('4', 'b', '(b) Scríobh síos dhá rud a thaispeánann gur cara dílis d’Éirinn í Hillary. (Alt 4)', '(b) Scríobh síos dhá rud a thaispeánann'),
        ('5', 'a', '(a) Cad a theastaigh ó Hillary a dhéanamh i Samhain 2008? (Alt 5)', '5. (a) Cad a theastaigh ó Hillary'),
        ('5', 'b', '(b) Cén obair a dhéanann Rúnaí Stáit Mheiriceá? (Alt 5)', '(b) Cén obair a dhéanann Rúnaí Stáit')]),
}

# Printed lines (paper PDF 3, 8–12).
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

# 2A: (slug, atlas, letter, title, topic, [printed lines], scheme start, scheme end). Both are priced as five points,
# “7 marc an ceann ar thrí phointe eolais agus 2 mharc ar an dá cheann eile”, never per printed point.
OISIN = ('prose-2a-a', 'P-2A-a', 'a', 'Oisín i dTír na nÓg', 'irish-4-1', [
    'Tabhair achoimre ar na heachtraí is mó sa scéal béaloidis Oisín i dTír na nÓg. Luaigh na pointí seo san achoimre:',
    '(i) Déan cur síos ar an gcuma a bhí ar Niamh Chinn Óir nuair a tháinig sí ag lorg Oisín.',
    '(ii) Cén t-eolas a thug Niamh Chinn Óir d’Oisín faoi Thír na nÓg?',
    '(iii) Cén sórt saoil a bhí ag Oisín leis na Fianna sular imigh sé go Tír na nÓg?',
    '(iv) Cén t-eolas atá sa scéal faoi na páistí a bhí ag Niamh Chinn Óir agus Oisín?',
    '(v) Déan cur síos ar an timpiste a tharla d’Oisín nuair a d’fhill sé ó Thír na nÓg.'],
    '(a) Oisín i dTír na nÓg', '(b) Hurlamaboc')
HURLAMABOC = ('prose-2a-b', 'P-2A-b', 'b', 'Hurlamaboc', 'irish-4-5', [
    '“Fiche bliain ó shin a pósadh Lisín agus Pól. Bheadh an ócáid iontach á ceiliúradh acu i gceann seachtaine. Bhí an teaghlach ar fad ag tnúth leis.” '
    'Hurlamaboc',
    'Déan cur síos ar shaol Lisín ón uair a phós sí Pól agus ar na hullmhúcháin a bhí déanta aici don cheiliúradh (don chóisir).'],
    '(b) Hurlamaboc', 'Níl cead aon ábhar a bhaineann le Prós Ainmnithe')
FIVE_POINTS = ('5 phointe eolais: 7 marc an ceann ar thrí phointe eolais agus 2 mharc ar an dá cheann eile. (7 marc = 5 mharc ar lomphointe eolais '
               'agus 2 mharc ar fhorbairt) (2 mharc = 1 mharc ar lomphointe eolais agus 1 mharc ar fhorbairt)')
# 2B: (slug, atlas, printed lines, scheme start, scheme end, eolas cut, title cut, title label, title permitted, focus)
PROSE_2B = [
    ('prose-2b-a', 'P-2B-a', [
        '(a) Maidir le scéal béaloidis roghnach a ndearna tú staidéar air le linn do chúrsa, déan cur síos ar an gcineál duine é an '
        'príomhcharachtar (an phríomhphearsa) sa scéal agus ar na rudaí is mó a tharlaíonn don duine sin sa scéal. (23 marc)',
        'Ní mór teideal an scéil bhéaloidis sin a scríobh síos go cruinn. (2 mharc)'],
     '(a) Maidir le scéal béaloidis roghnach', '(b) Maidir le giota as úrscéal roghnach', 'Treoir:', 'Ní mór teideal an scéil bhéaloidis',
     'Teideal an scéil bhéaloidis', [0, 2], 'Scéal béaloidis roghnach'),
    ('prose-2b-b', 'P-2B-b', [
        '(b) Maidir le giota as úrscéal roghnach a ndearna tú staidéar air le linn do chúrsa, tabhair cuntas ar na príomhimeachtaí (príomhrudaí) '
        'a tharlaíonn sa ghiota sin. (23 marc)',
        'Ní mór teideal an úrscéil sin, mar aon le hainm an údair, a scríobh síos go cruinn. (2 mharc)'],
     '(b) Maidir le giota as úrscéal roghnach', 'Freagair A (Filíocht Ainmnithe)', '5 phointe eolais:', 'Ní mór teideal an úrscéil',
     'Teideal + ainm an údair', [0, 1, 2], 'Giota as úrscéal roghnach'),
]
SEVEN_FIVE_TWO = ('5 phointe eolais: 7 marc ar an gcéad dá phointe eolais, 5 mharc ar an tríú pointe eolais agus 2 mharc ar an dá cheann eile.')
# 3A: (slug, atlas, page, title, [(label, paper prompt, marks, scheme cut)], scheme start, scheme end)
POETRY_3A = [
    ('poetry-3a-a', 'F-3A-a', 10, 'Mo ghrá-sa (idir lúibíní)', [
        # The scheme prints this prompt without “(thíos)”; the card shows the paper's print.
        ('i', 'Cad is téama don dán Mo ghrá-sa (idir lúibíní) (thíos), dar leat? Tabhair dhá phointe eolais i d’fhocail féin faoin téama sin sa dán.', 8,
         '(i) Cad is téama don dán'),
        ('ii', 'Scríobh síos íomhá (pictiúr) amháin ón dán atá greannmhar, dar leat. Mínigh an íomhá (an pictiúr) sin i d’fhocail féin.', 8,
         '(ii) Scríobh síos íomhá (pictiúr) amháin'),
        ('iii', 'An maith leat an dán seo? Cuir fáthanna le do fhreagra. (Is leor dhá fháth.)', 9, '(iii) An maith leat an dán seo?')],
     '(a) Mo ghrá-sa (idir lúibíní)', '(b) An tEarrach Thiar'),
    ('poetry-3a-b', 'F-3A-b', 11, 'An tEarrach Thiar', [
        ('i', '(a) Cén obair atá ar siúl ag an bhfear i véarsa a haon?\n(b) Cén sórt fuaime atá ann i véarsa a haon?\n'
              '(c) Conas atá an aimsir i véarsa a dó?\n(d) Cá bhfuil na mná i véarsa a trí?', 8, '(i) (a) Cén obair atá ar siúl'),
        ('ii', 'Déan cur síos, i d’fhocail féin, ar an bpictiúr den churrach a thugann an file dúinn i véarsa a ceathair. (Is leor dhá phointe eolais.)', 8,
         '(ii) Déan cur síos, i d’fhocail féin'),
        ('iii', 'An maith leat an dán seo? Cuir fáthanna le do fhreagra. (Is leor dhá fháth.)', 9, '(iii) An maith leat an dán seo?')],
     '(b) An tEarrach Thiar', 'Nóta: Caithfidh an Scrúdaitheoir an marc don Ábhar'),
]
POEM_TOPICS = {'poetry-3a-a': 'irish-5-4', 'poetry-3a-b': 'irish-5-3'}
# What each poem's scheme says of lines lifted straight from the poem (English notes; the scheme lines are in the guidance).
LIFTED_LINES = {'poetry-3a-a': 'in (i) the scheme gives apt lines lifted straight from the poem without the candidate’s own words 2 + 2 (0 if the theme '
                               'is not named either), and in (ii) such lines as the explanation 3',
                'poetry-3a-b': 'in (ii) the scheme gives apt lines lifted straight from the poem without the candidate’s own words 2 + 2, and each '
                               'question in (i) quotes the verse line that answers it'}
# Printed questions inside one printed sub-question: (slug, sub-question) -> [(letter, scheme question, marks, printed caption, next cut)]
SLOTS_3A = {
    ('poetry-3a-b', 'i'): [('a', 'Cén obair atá ar siúl ag an bhfear i véarsa a haon?', 2, '(2 mharc)', '(b) Cén sórt fuaime'),
                           ('b', 'Cén sórt fuaime atá ann i véarsa a haon?', 2, '(2 mharc)', '(c) Conas atá an aimsir'),
                           ('c', 'Conas atá an aimsir i véarsa a dó?', 2, '(2 mharc)', '(d) Cá bhfuil na mná'),
                           ('d', 'Cá bhfuil na mná i véarsa a trí?', 2, '(2 mharc)', None)],
}
SLOT_PERMITTED = {('poetry-3a-b', 'i'): [0, 2, 4, 6, 8]}
POETRY_3B = [
    ('poetry-3b-a', 'F-3B-a', [
        '(i) Maidir le dán roghnach nua-aimseartha amháin a scríobh bean agus a ndearna tú staidéar air le linn do chúrsa, cad is téama don dán sin, '
        'dar leat? Tabhair dhá phointe eolais i d’fhocail féin faoin téama sin sa dán. (8 marc)',
        '(ii) Luaigh íomhá (pictiúr) amháin ón dán atá suimiúil, dar leat. Mínigh an íomhá (an pictiúr) sin i d’fhocail féin. (6 mharc)',
        '(iii) An maith leat an dán seo? Cuir fáthanna le do fhreagra. (Is leor dhá fháth.) (9 marc)'],
     '(a) (i) Maidir le dán roghnach nua-aimseartha amháin a scríobh bean', '(b) (i) Maidir le dán roghnach nua-aimseartha amháin a scríobh fear',
     ['(ii) Luaigh íomhá (pictiúr)', '(iii) An maith leat', 'Ní mór teideal an dáin']),
    ('poetry-3b-b', 'F-3B-b', [
        '(i) Maidir le dán roghnach nua-aimseartha amháin a scríobh fear agus a ndearna tú staidéar air le linn do chúrsa, scríobh síos i d’fhocail '
        'féin príomhsmaointe an dáin. (8 marc)',
        '(ii) Cad é an mothúchán is láidre sa dán, dar leat? Tabhair dhá shampla den mhothúchán sin sa dán. (6 mharc)',
        '(iii) An maith leat an dán seo? Cuir fáthanna le do fhreagra. (Is leor dhá fháth.) (9 marc)'],
     '(b) (i) Maidir le dán roghnach nua-aimseartha amháin a scríobh fear', None, ['(ii) Cad é an mothúchán', '(iii) An maith leat', 'Ní mór teideal an dáin']),
]
TITLE_LINE = 'Ní mór teideal an dáin sin, mar aon le hainm an fhile, a scríobh síos go cruinn. (2 mharc)'
# The literature language note, printed word for word (with its closing full stop) under all eight answers.
LANG = '[Gaeilge lochtach: 0 - 4 a bhaint den iomlán a gnóthaíodh.]'

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
    # PDF 21 holds only the closing 3B note (printed after 3A on PDF 19 too) and the modified marking.
    s = Scheme(doc, 12, 20)
    assert s.removed == len(FURNITURE), s.removed
    assert not PUA.search(s.text), 'private-use glyph left in the scheme text'
    assert 'Níl sé i gceist a chur in iúl' not in s.text, '2015 prints no general literature note'
    assert 'Nóta: Má tá dhá phointe eolais i gceist' not in s.text, '2015 prints no two-point note above the passages'
    lang_read = '[Gaeilge lochtach: 0 - 5 a bhaint den iomlán a gnóthaíodh.]'
    assert s.text.count(lang_read) == 2
    assert s.text.count(LANG) == 8, s.text.count(LANG)
    for letter, passage in PASSAGES.items():
        page_text = ' '.join(texts[p - 1] for p in passage['pages'])
        assert in_order(passage['title'], texts[passage['pages'][0] - 1]), letter
        after = s.text.index(passage['start'])
        assert in_order(passage['title'], s.text[after:after + 300]), letter
        resolved = []
        anchors = [p[3] for p in passage['parts']]
        for index, (q, part, prompt, anchor) in enumerate(passage['parts']):
            assert in_order(prompt, page_text), (letter, q, part)
            # The last part ends where the scheme's penalty instructions and mark boxes begin.
            nxt = anchors[index + 1] if index + 1 < len(anchors) else passage['end']
            chunk, spages = s.chunk(anchor, nxt, after)
            after = s.text.index(anchor, after) + 1
            assert '5 mharc' in chunk and '50 marc' not in chunk and 'LÉAMHTHUISCINT' not in chunk and 'Léireofar' not in chunk, (letter, q, part, chunk[:80])
            two = bool(TWO_POINTS.search(chunk))
            # A printed 3-mark partial (“= 3 mharc”, “bronn 3 mharc air”) allows 0/3/5.
            permitted = [0, 3, 5] if (two or '= 3 mharc' in chunk) else [0, 5]
            resolved.append((q, part, prompt, chunk, spages, two, permitted))
        passage['resolved'] = resolved
    for item in (OISIN, HURLAMABOC):
        slug, atlas, letter, title, topic, lines, start, end = item
        for line in [title] + lines:
            assert in_order(line, texts[7]), (slug, line[:50])
    for slug, atlas, lines, start, end, eolas_cut, title_cut, *_ in PROSE_2B:
        for line in lines:
            assert in_order(line, texts[8]), (slug, line[:50])
    for slug3, atlas3, page, title3, subs3, start3, end3 in POETRY_3A:
        assert in_order(title3, texts[page - 1]), slug3
        for label, prompt, marks, cut in subs3:
            assert in_order(prompt.replace('\n', ' ') + f' ({marks} marc)', texts[page - 1]), (slug3, label)
    for slug4, atlas4, prompts, start4, end4, cuts4 in POETRY_3B:
        for line in prompts + [TITLE_LINE]:
            assert in_order(line, texts[11]), (slug4, line[:50])
    assert comparable(texts[11]).count(comparable(TITLE_LINE)) == 2
    for page, line in [(3, 'FREAGAIR GACH CEIST (1, 2 AGUS 3).'), (4, 'Freagair A agus B anseo.'), (8, PROSE_CHOICE), (8, BOTH), (8, BOX_2A),
                       (9, BOX_2B), (9, NO_PRESCRIBED_PROSE), (9, BOTH), (10, POETRY_CHOICE), (10, BOTH), (10, BOX_3A), (12, BOX_3B),
                       (12, NO_PRESCRIBED_POETRY), (12, BOTH)]:
        assert comparable(line) in comparable(texts[page - 1]), (page, line)
    _MATERIAL = dict(paper=paper, texts=texts, s=s, lang_read=lang_read, decisions=selection_decisions(paper))
    return _MATERIAL


def deduction():
    return criterion('gaeilge-deduction', 'Gaeilge lochtach', 4, [LANG], 'quality', deduction=True)


def reading_note(m):
    return 'Scheme: “' + m['lang_read'] + '” — one deduction from each passage total (50), never inside a single part.'


def source(label, title, pages):
    return dict(kind='source-text', label=label, title=title, pages=pages, attribution=ATTRIBUTION, presentationNote=SOURCE_NOTE)


def answer_key(m, start, end, key_start, lines):
    """The scheme restates the printed question before its key (2B restates the title line beside its price): assert the
    restatement, return the key alone."""
    whole, spages = m['s'].chunk(start, end)
    assert LANG in whole, start
    whole = before_language_note(whole)
    restated, key = whole[:whole.index(key_start)], whole[whole.index(key_start):]
    assert in_order(lines[0], restated), (start, lines[0][:50])
    for line in lines:
        assert in_order(line, whole), (start, line[:50])
    return key, spages


def poem_pieces(m, slug, subs, start, end):
    whole, spages = m['s'].chunk(start, end)
    assert LANG in whole, slug
    whole = before_language_note(whole)
    pieces = split_at(whole, [cut for _, _, _, cut in subs], slug)
    for (label, _, marks, _), piece in zip(subs, pieces):
        assert f'({marks} marc)' in piece or (slug, label) in SLOTS_3A, (slug, label, piece[:60])
    return pieces, spages


def slot_pieces(piece, slots):
    out = []
    for sub, question, marks, caption, nxt in slots:
        start_at = piece.index(question)
        slot = piece[start_at:piece.index(nxt, start_at) if nxt else len(piece)].strip()
        assert re.search(r'Freagraí [Ss]amplacha:', slot) and caption in slot, (sub, slot[:60])
        out.append((sub, slot))
    return out


WHOLE_PROSE_NOTE = ('One complete SEC response: five points, three at 7 (5 for the bare point + 2 for development) and two at 2 (1 + 1); the 0–4 '
                    'Gaeilge deduction applies once to this whole 25-mark answer. The scheme prints no sample points, so the answer is judged on merit '
                    'against that allocation.')
LIT_DEDUCTION_NOTE = 'The 0–4 Gaeilge deduction applies once to this whole 25-mark answer, never inside one sub-question.'


def build():
    m = material()
    cards = []

    def add(key, slug, ref, prompt, topic, pages, scheme_pages, criteria, requirements, note, src, concept=None, stem=None):
        cards.append(dict(
            id=f'irish-{YEAR}-ol-p2-{slug}', year=YEAR, level='ordinary', paper=2, section='2',
            atlasQuestionId=key, questionRef=f'{YEAR} OL Paper 2 {ref}', **({'stem': stem} if stem else {}), questionText=prompt,
            totalMarks=sum(c['maxMarks'] for c in criteria if c['kind'] == 'award'), topicId=topic,
            conceptId=concept or f'irish-ol-p2-{slug}', paperFileid=FILE, paperPage=pages[0], schemeFileid=SCHEME_FILE,
            schemePage=scheme_pages[0], schemePages=scheme_pages, reviewedAt=REVIEWED_AT, reviewedPaperPages=pages,
            taskRequirements=requirements, criteria=criteria, markingGuideNote=note, sourceMaterial=src))

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
    # ---- Ceist 2A: (a) Oisín i dTír na nÓg, (b) Hurlamaboc, each priced as five points -----------------
    for item, extra, reqs in ((OISIN, ' The five printed points (i)–(v) are what the summary must cover; the scheme prices the summary as five points, '
                                      'not each printed point.', LIT), (HURLAMABOC, '', LIT[1:])):
        slug, atlas, letter, title, topic, lines, start, end = item
        key, kpages = answer_key(m, start, end, '5 phointe eolais:', [title] + lines)
        assert key == FIVE_POINTS, (slug, key)
        add(atlas, slug, f'Prós 2A({letter}) · {title}', f'({letter}) {title}\n' + '\n'.join(lines) + '\n(25 marc)', topic, [8], kpages,
            [criterion('eolas', 'Eolas', 25, [key], 'indicative'), deduction()], [PROSE_CHOICE, BOTH] + reqs,
            WHOLE_PROSE_NOTE + extra, source('Prós Ainmnithe', title, [8]), concept=f'irish-prose-2a-{topic}', stem=BOX_2A)
        question_lit.append(cards[-1]['id'])

    # ---- Ceist 2B: Prós Roghnach (a) the optional folk tale, (b) the optional novel extract --------------------
    for slug, atlas, lines, start, end, eolas_cut, title_cut, title_label, title_permitted, focus in PROSE_2B:
        key, kpages = answer_key(m, start, end, eolas_cut, lines)
        eolas, teideal = key[:key.index(title_cut)].strip(), key[key.index(title_cut):]
        assert SEVEN_FIVE_TWO in eolas and teideal.startswith(lines[1]), (slug, teideal[:60])
        add(atlas, slug, f'Prose 2B({slug[-1]})', '\n'.join(lines), 'irish-4-7', [9], kpages,
            [criterion('eolas', 'Eolas', 23, [eolas], 'indicative'),
             criterion('teideal', title_label, 2, [teideal], 'exact', permitted=title_permitted), deduction()],
            [PROSE_CHOICE, NO_PRESCRIBED_PROSE, BOTH] + LIT[1:],
            'One complete SEC response: 23 for five points (7, 7, 5, 2, 2: the bare point and its development) and 2 for the exact title'
            + (' and author' if slug == 'prose-2b-b' else '') + ', then the 0–4 Gaeilge deduction once. The optional text is open content chosen by '
            'the candidate; the scheme prints no sample points for it, so its points are judged on merit against these allocations.',
            source('Prós Roghnach', focus, [9]), concept='irish-prose-2b-irish-4-7', stem=STEM_2B)
        question_lit.append(cards[-1]['id'])

    # ---- Ceist 3A: Mo ghrá-sa (idir lúibíní) and An tEarrach Thiar ---------------------------------------
    poem_parts = {}
    for slug3, atlas3, page, title3, subs3, start3, end3 in POETRY_3A:
        pieces3, spages3 = poem_pieces(m, slug3, subs3, start3, end3)
        poem_parts[slug3] = (pieces3, spages3)
        crits = [criterion(f'eolas-{label}', f'({label}) Eolas', marks, [piece], 'indicative', permitted=SLOT_PERMITTED.get((slug3, label)))
                 for (label, _, marks, _), piece in zip(subs3, pieces3)]
        prompt = '\n'.join(f'({label}) {p}' + f' ({marks} marc)' for label, p, marks, _ in subs3)
        add(atlas3, slug3, f'Poetry 3A({atlas3[-1]})', f'({atlas3[-1]}) {title3}\n' + prompt, POEM_TOPICS[slug3], [page], spages3, crits + [deduction()],
            [POETRY_CHOICE, BOTH] + LIT,
            'One complete SEC response: ' + ', '.join(f'({label}) {marks}' for label, _, marks, _ in subs3) +
            ' at their printed tariffs, then the 0–4 Gaeilge deduction once. The sample points are indicative rather than exhaustive; '
            f'{LIFTED_LINES[slug3]}.',
            source('Filíocht Ainmnithe', title3, [page]), concept=f'irish-poetry-3a-{POEM_TOPICS[slug3]}', stem=BOX_3A)
        question_lit.append(cards[-1]['id'])

    # ---- Ceist 3B: Filíocht Roghnach (a) and (b) --------------------------------------------------------
    for slug4, atlas4, prompts, start4, end4, cuts4 in POETRY_3B:
        chunk4, spages4 = m['s'].chunk(start4, end4, m['s'].text.index('⟦20⟧'))
        assert LANG in chunk4, slug4
        chunk4 = before_language_note(chunk4)
        idx = [0] + [chunk4.index(cut) for cut in cuts4]
        bits = [chunk4[a:b].strip() for a, b in zip(idx, idx[1:] + [len(chunk4)])]
        for bit, cap in zip(bits, ['(8 marc)', '(6 mharc)', '(9 marc)', '(2 mharc)']):
            assert cap in bit, (slug4, cap)
        crits = [criterion('eolas-i', '(i) Eolas', 8, [bits[0]], 'indicative'), criterion('eolas-ii', '(ii) Eolas', 6, [bits[1]], 'indicative'),
                 criterion('eolas-iii', '(iii) Eolas', 9, [bits[2]], 'indicative'),
                 criterion('teideal', 'Teideal + ainm an fhile', 2, [bits[3]], 'exact', permitted=[0, 1, 2])]
        add(atlas4, slug4, f'Poetry 3B({atlas4[-1]})', f'({atlas4[-1]}) ' + '\n'.join(prompts + [TITLE_LINE]), 'irish-5-6', [12], spages4,
            crits + [deduction()], [POETRY_CHOICE, NO_PRESCRIBED_POETRY, BOTH] + LIT,
            'One complete SEC response: (i) 8, (ii) 6, (iii) 9, poem and poet 2, then the 0–4 Gaeilge deduction once. '
            'The optional poem is open content; 3B(a) asks for a modern poem written by a woman and 3B(b) one written by a man. The printed '
            'allocations are judged on merit (indicative rather than exhaustive).',
            source('Filíocht Roghnach', f'3B({atlas4[-1]}) · Dán roghnach', [12]),
            concept='irish-poetry-3b-irish-5-6', stem=STEM_3B)
        question_lit.append(cards[-1]['id'])

    # ---- Practice: every prescribed-poetry sub-question and the printed questions inside ----------------
    for slug3, atlas3, page, title3, subs3, start3, end3 in POETRY_3A:
        pieces3, spages3 = poem_parts[slug3]
        topic3 = POEM_TOPICS[slug3]
        src3 = source('Filíocht Ainmnithe', title3, [page])
        head = f'({atlas3[-1]}) {title3}\n'
        for (label, prompt, marks, _), piece in zip(subs3, pieces3):
            slots = SLOTS_3A.get((slug3, label))
            add(f'{atlas3}-{label}', f'{slug3}-{label}', f'Filíocht 3A({atlas3[-1]}) · {title3} · ({label})', head + f'({label}) {prompt} ({marks} marc)',
                topic3, [page], spages3,
                [criterion('eolas', 'Eolas', marks, [piece], 'indicative', permitted=SLOT_PERMITTED.get((slug3, label)))],
                [POETRY_CHOICE, BOTH] + LIT[1:], sub_note, src3, stem=BOX_3A)
            practice_ids.append(cards[-1]['id'])
            if slots:
                printed = dict(re.findall(r'\(([a-d])\) ([^\n]+)', prompt))
                for (sub, slot), (_, _, smarks, caption, _) in zip(slot_pieces(piece, slots), slots):
                    add(f'{atlas3}-{label}-{sub}', f'{slug3}-{label}-{sub}', f'Filíocht 3A({atlas3[-1]}) · {title3} · ({label})({sub})',
                        head + f'({label}) ({sub}) {printed[sub]}', topic3, [page], spages3,
                        [criterion('eolas', 'Freagra', smarks, [slot], 'indicative', permitted=[0, smarks])], [POETRY_CHOICE, BOTH] + LIT[1:],
                        f'One printed question inside 3A({atlas3[-1]})({label}), at its printed {caption}. ' + LIT_DEDUCTION_NOTE, src3, stem=BOX_3A)
                    practice_ids.append(cards[-1]['id'])

    assert len(whole_ids) == 10 and len(question_lit) == 8 and len(practice_ids) == 30, (len(whole_ids), len(question_lit), len(practice_ids))
    assert len(cards) == 48 and len({c['id'] for c in cards}) == 48 and len({c['atlasQuestionId'] for c in cards}) == 48
    for card in cards:
        assert sum(c['maxMarks'] for c in card['criteria'] if c['kind'] == 'award') == card['totalMarks'], card['id']
        for c in card['criteria']:
            assert c['guidance'] and all(not re.search('Siombailí Anótála|50 marc|Léirigh mionbhriseadh', g) and not PUA.search(g) for g in c['guidance']), (card['id'], c['id'])
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
                  boundaries=('10 whole reading questions with their 20 published parts; 8 literature questions; the 6 prescribed-poetry '
                              'sub-questions and the 4 printed questions inside 3A(b)(i). Oisín i dTír na nÓg’s five printed points are not carded '
                              'apart: the scheme prices the summary as five points, never one printed point.'))
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
    print(f"Irish Ordinary {YEAR} Paper 2: {len(data['cards'])} reviewed cards (18 printed questions, 30 practice parts); the archive remains incomplete.")


if __name__ == '__main__':
    main()
