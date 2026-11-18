#!/usr/bin/env python3
"""Reviewed 2016 Ordinary Paper 2 (Léamhthuiscint agus Litríocht), carded new.

Paper PDF 1–12 and the Paper 2 pages of the combined LC001GLP000IV scheme (PDF 12–24,
plus 25 modified marking) reviewed on 2026-11-04. Counts are assertions, not
corpus-completeness proof. Same method as irish_ordinary_2018_p2.py and
irish_ordinary_2019_p2.py.

No 2016 Ordinary card existed before. `build` cards the component the way the reviewed
2018–2025 Ordinary Paper 2s are carded: the ten whole reading questions (each part its
own 5-mark criterion), the nine literature questions (each printed sub-question its own
criterion, the 0–4 Gaeilge deduction once), and the practice cards beside them: every
reading part (20), the five printed sub-questions of 2A(a) Dís, every prescribed-poetry
sub-question (6) and the four printed questions inside 3A(b)(i) An Spailpín Fánach.

2016's layout is 2018's and 2019's: “FREAGAIR GACH CEIST (1, 2 AGUS 3).” Ceist 1 is
Léamhthuiscint A and B (both); Ceist 2 is A (Prós Ainmnithe) or B (Prós Roghnach) and
Ceist 3 is A (Filíocht Ainmnithe) or B (Filíocht Roghnach), each section printing two
questions, (a) and (b), both to be answered (“Freagair (a) agus (b) anseo.”). 2A(a) is
Dís with five sub-questions the scheme prices one by one; 2A(b) is the prescribed film
Cáca Milis or the prescribed play An Lasair Choille: they file under different Atlas
headings, so each is its own card; 2B(a) is an optional short story (theme 3 + four
points 20 + title and author 2) and 2B(b) an optional film or an optional play under
one heading with one scheme, so one card carries both printed alternatives (the
2026-10-12 decision, commit 7da1a0819). 3A is Géibheann and An Spailpín Fánach, whose
(i) prints four questions (a)–(d) at 2 each; 3B(a) asks for a modern poem and 3B(b) an
old one. Each literature card carries the printed choice and “Freagair (a) agus (b)
anseo.” as its task check (choice is not a route; no card combines two questions), and
the section's printed box heading with, for B, the printed restriction as its lead-in.

The scheme's text layer stores each page's boxed heading (“CEIST 1 (A + B) -
LÉAMHTHUISCINT - 100 marc”, “A – (50 marc)” …) with the page body; `Scheme` removes
those exact strings so no heading lands inside an answer key. 2016 prints no general
literature note (“Níl sé i gceist … freagraí samplacha …”), so each literature criterion
carries its own scheme slice alone.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import re
from pathlib import Path
from irish_lifted import PUA, scheme_words_in, symbol_text

ROOT = Path(__file__).resolve().parents[3]
YEAR = 2016
FILE = 'LC001GLP200IV'
SCHEME_FILE = 'LC001GLP000IV'
OUT = ROOT / 'components/MarkBank/cards/irish/ordinary-2016-p2-authored.json'
SOURCE_REVIEW = ROOT / 'scripts/markbank/authored/irish-ordinary-2016-p2-source-review.json'
REVIEWED_AT = '2026-11-04'
PAPER_SHA = 'cd8e5899d3a010a3e28a10cbf8be3793cf3a063687056f065e29c9f4d704f77d'
SCHEME_SHA = '1c65b9d7d98fec191c5669837f96fbe7f28f0d55c55fc72f42e3c53009b67cd8'
DIRECTIVE = re.compile(r'rogha|roghna|Freagair|Luaigh|Ainmnigh|\bnó\b|dhá phointe|dhá rud|dhá bh|dhá dh|dhá ch|dhá fh|dhá th|dhá ph|dhá sh|'
                       r'\ban dá\b|ceann amháin|pointe amháin|amháin|\bdhá\b', re.I)
SOURCE_NOTE = 'Shown page-for-page from the official examination paper; swipe to move between pages.'
ATTRIBUTION = '© State Examinations Commission.'
# Boxed page headings the 2016 scheme's text layer stores with the page body (exact strings, each printed once).
FURNITURE = ('CEIST 1 (A + B) - LÉAMHTHUISCINT - 100 marc', 'A – (50 marc)', 'B – (50 marc)',
             'CEIST 2 PRÓS – AINMNITHE nó ROGHNACH – (50 marc)', 'A – PRÓS AINMNITHE – (50 marc)', 'B – PRÓS ROGHNACH – (50 marc)',
             'CEIST 3 FILÍOCHT – AINMNITHE nó ROGHNACH – (50 marc)', 'A – FILÍOCHT AINMNITHE – (50 marc)', 'B – FILÍOCHT ROGHNACH – (50 marc)')
FURNITURE_PATTERN = re.compile('|'.join(r'\s*' + re.escape(h) + r'(?=\s|$)\s*' for h in sorted(FURNITURE, key=len, reverse=True)))
# The literature language note, printed with a closing full stop on the prose pages and without one on the poetry pages.
LANG_LIT = re.compile(r'\[Gaeilge lochtach: 0-4 a bhaint den iomlán a gnóthaíodh\.?\]')


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
        pages |= {int(m.group(1)) for m in re.finditer(r'⟦(\d+)⟧([^⟦]*)', raw) if clean(m.group(2)) not in ('', 'nó')}
        return clean(re.sub(r'⟦\d+⟧', ' ', raw)), sorted(pages)


def before_language_note(text):
    return re.split(r'\[\s*Gaeilge lochtach', text)[0].strip()


def language_note(text):
    """The language note a literature answer prints after its key (with or without its closing full stop)."""
    found = LANG_LIT.findall(text)
    assert len(found) == 1, (len(found), text[-120:])
    return found[0]


def split_at(text, cuts, slug):
    idx = [text.index(cut) for cut in cuts]
    assert idx == sorted(idx), slug
    return [text[a:b].strip() for a, b in zip(idx, idx[1:] + [len(text)])]


# Two points priced first-correct 3, second 2: “3 mharc + 2 mharc = 5 mharc”, or the bare “5 mharc” followed by
# “An chéad … atá ceart = 3 mharc; an dara … atá ceart = 2 mharc”.
TWO_POINTS = re.compile(r'3 mharc \+ 2 mharc|; [Aa]n dara [^=;]+ atá ceart = 2 mharc')

# (q, part, paper prompt, scheme anchor)
PASSAGES = {
    'A': dict(title='Laoch ag Imeacht agus Laoch ag Teacht', pages=[4, 5], topic='irish-3-0', start='⟦12⟧', notes_end='1. (a)',
              end='Nóta: Gearrfar pionós i ngeall ar iomarcaíocht. Léireofar', parts=[
        ('1', 'a', '(a) Cathain a fuair Maureen O’Hara bás? (Alt 1)', '1. (a) Cathain a fuair Maureen'),
        ('1', 'b', '(b) Cén fáth a raibh Saoirse Ronan á moladh go mór sna meáin chumarsáide? (Alt 1)', '(b) Cén fáth a raibh Saoirse Ronan'),
        ('2', 'a', '(a) Cad a thosaigh Maureen O’Hara agus í an-óg? (Alt 2)', '2. (a) Cad a thosaigh Maureen'),
        ('2', 'b', '(b) Cén pháirt thábhachtach a bhí ag Charles Laughton i saol Maureen mar aisteoir? (Alt 2)', '(b) Cén pháirt thábhachtach'),
        ('3', 'a', '(a) Cén dá chontae ina ndearnadh cuid mhór den scannán The Quiet Man? (Alt 3)', '3. (a) Cén dá chontae'),
        ('3', 'b', '(b) Scríobh síos dhá chúis ar éirigh go maith leis an scannán The Quiet Man sna Stáit Aontaithe. (Alt 3)', '(b) Scríobh síos dhá chúis ar éirigh'),
        ('4', 'a', '(a) Cad a rinne Saoirse Ronan nuair a bhí sí trí bliana d’aois? (Alt 4)', '4. (a) Cad a rinne Saoirse Ronan'),
        ('4', 'b', '(b) Cad a dúirt Saoirse tar éis di an scannán Atonement a dhéanamh? (Alt 4)', '(b) Cad a dúirt Saoirse'),
        ('5', 'a', '(a) Tabhair dhá phíosa eolais faoi shaol Eilis Lacey in Brooklyn sula dtagann drochscéal as Éirinn. (Alt 5)', '5. (a) Tabhair dhá phíosa eolais faoi shaol Eilis'),
        ('5', 'b', '(b) Cad a dhéanann Eilis ag deireadh an scannáin Brooklyn? (Alt 5)', '(b) Cad a dhéanann Eilis')]),
    'B': dict(title='Ceiliúradh i gCathair Phort Láirge', pages=[6, 7], topic='irish-3-1', start='⟦15⟧', notes_end='1. (a)',
              end='Nóta: Gearrfar pionós i ngeall ar iomarcaíocht. Léireofar', parts=[
        ('1', 'a', '(a) Scríobh síos dhá chúis ar roghnaigh na Lochlannaigh ceantar Phort Láirge mar áit chónaithe. (Alt 1)', '1. (a) Scríobh síos dhá chúis ar roghnaigh'),
        ('1', 'b', '(b) Cad atá le feiceáil sa mhúsaem i dTúr Raghnaill anois? (Alt 1)', '(b) Cad atá le feiceáil sa mhúsaem'),
        ('2', 'a', '(a) Cén fáth ar inis John Condon bréag faoina aois? (Alt 2)', '2. (a) Cén fáth ar inis John Condon'),
        ('2', 'b', '(b) Cad a tharla do John Condon i gcath Ypres? (Alt 2)', '(b) Cad a tharla do John Condon'),
        ('3', 'a', '(a) Cad atá ar siúl sa Fhrainc na laethanta seo? (Alt 3)', '3. (a) Cad atá ar siúl sa Fhrainc'),
        ('3', 'b', '(b) Cad a rinne John O’Shea sa bhliain 1998? (Alt 3)', '(b) Cad a rinne John O’Shea'),
        ('4', 'a', '(a) Tabhair dhá phíosa eolais faoin bhféile mhór “Spraoi” i bPort Láirge. (Alt 4)', '4. (a) Tabhair dhá phíosa eolais faoin bhféile'),
        ('4', 'b', '(b) Cén fáth a mbeidh imeachtaí cuimhneacháin ar siúl i bPort Láirge i mbliana? (Alt 4)', '(b) Cén fáth a mbeidh imeachtaí'),
        ('5', 'a', '(a) Cén fáth a dtagadh a lán cuairteoirí go dtí an mhonarcha criostail i bPort Láirge? (Alt 5)', '5. (a) Cén fáth a dtagadh'),
        ('5', 'b', '(b) Cad a tharla don mhonarcha criostail sa bhliain 2009? (Alt 5)', '(b) Cad a tharla don mhonarcha')]),
}

# Printed lines (paper PDF 3, 8–12).
PROSE_CHOICE = 'Freagair A (Prós Ainmnithe) nó B (Prós Roghnach).'
POETRY_CHOICE = 'Freagair A (Filíocht Ainmnithe) nó B (Filíocht Roghnach).'
BOTH = 'Freagair (a) agus (b) anseo.'
FILM_OR_PLAY = 'Freagair an cheist thíos faoin scannán Cáca Milis nó faoin dráma An Lasair Choille.'
OPTIONAL_FILM_OR_PLAY = 'Freagair an cheist thíos faoin scannán roghnach nó faoin dráma roghnach.'
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

# 2A(a) Dís: printed sub-questions the scheme prices at 5 each (the paper prints only the question's (25 marc)).
DIS = ('prose-2a-a', 'P-2A-a', 'a', 'Dís', 'irish-4-4', 'Freagair na ceisteanna seo a leanas faoin ngearrscéal Dís.', [
    ('i', 'Cén fáth a raibh bean Sheáin míshásta le Seán i dtús an ghearrscéil?', '(i) Cén fáth a raibh bean Sheáin'),
    ('ii', 'Cén toradh a bhí ar an suirbhé, de réir an eolais ar an bpáipéar?', '(ii) Cén toradh a bhí ar an suirbhé'),
    ('iii', 'Conas a mhothaigh bean Sheáin an mhaidin ar tháinig bean an tsuirbhé chuig an teach? Tabhair dhá chúis ar mhothaigh sí mar sin.',
     '(iii) Conas a mhothaigh bean Sheáin'),
    ('iv', 'Scríobh síos dhá phíosa eolais fúithi féin a d’inis bean an tsuirbhé do bhean Sheáin.', '(iv) Scríobh síos dhá phíosa eolais fúithi'),
    ('v', 'Ar thaitin Seán leat sa ghearrscéal seo? Tabhair dhá fháth le do fhreagra.', '(v) Ar thaitin Seán leat')],
    '(a) Dís Freagair na ceisteanna seo a leanas', '(b) Freagair an cheist thíos faoin scannán Cáca Milis')
# 2A(b): the prescribed film or the prescribed play, a card each: (slug, atlas, title, topic, printed question lines, scheme start, scheme end)
FILM_PLAY_2A = [
    ('prose-2a-b-caca-milis', 'P-2A-b-caca-milis', 'Cáca Milis', 'irish-4-6',
     ['Tabhair cuntas ar na príomhimeachtaí (príomhrudaí) a tharlaíonn sa scannán Cáca Milis ón uair a thagann Paul isteach ar an traein '
      'go dtí deireadh an scannáin.'],
     'Cáca Milis Tabhair cuntas ar na príomhimeachtaí', 'NÓ An Lasair Choille'),
    ('prose-2a-b-an-lasair-choille', 'P-2A-b-an-lasair-choille', 'An Lasair Choille', 'irish-4-8',
     ['Tabhair cuntas ar na príomhimeachtaí (príomhrudaí) a tharlaíonn sa dráma An Lasair Choille ón uair a thagann Míoda isteach i dteach '
      'Mhicil go dtí deireadh an dráma.'],
     'An Lasair Choille Tabhair cuntas ar na príomhimeachtaí', 'Níl cead aon ábhar a bhaineann le Prós Ainmnithe'),
]
# 2B(a): (paper lines, scheme start, scheme end, [(id, label, marks, cut-before)])
PROSE_2B_A = (['(a) Maidir le gearrscéal roghnach a ndearna tú staidéar air le linn do chúrsa, cad é an príomhthéama sa ghearrscéal sin, dar leat? '
               'Tabhair cuntas ar na príomhimeachtaí (príomhrudaí) a tharlaíonn sa ghearrscéal a léiríonn an príomhthéama sin. (23 marc)',
               'Ní mór teideal an ghearrscéil sin, mar aon le hainm an údair, a scríobh síos go cruinn. (2 mharc)'],
              '(a) Maidir le gearrscéal roghnach', '(b) Freagair an cheist thíos faoin scannán roghnach',
              [('priomhthema', 'An príomhthéama', 3, None), ('eolas', 'Na príomhimeachtaí', 20, '4 phointe eolais ag teastáil'),
               ('teideal', 'Teideal + ainm an údair', 2, 'Ní mór teideal')])
# 2B(b): the optional film or the optional play, one card with both printed alternatives.
PROSE_2B_B_LINES = [
    '(b) ' + OPTIONAL_FILM_OR_PLAY,
    'Maidir le scannán roghnach a ndearna tú staidéar air le linn do chúrsa, tabhair cuntas ar na príomhimeachtaí (príomhrudaí) a tharlaíonn sa scannán sin. (23 marc)',
    'Ní mór teideal an scannáin sin, mar aon le hainm an scríbhneora, a scríobh síos go cruinn. (2 mharc)',
    'NÓ',
    'Maidir le dráma roghnach a ndearna tú staidéar air le linn do chúrsa, tabhair cuntas ar na príomhimeachtaí (príomhrudaí) a tharlaíonn sa dráma sin. (23 marc)',
    'Ní mór teideal an dráma sin, mar aon le hainm an scríbhneora, a scríobh síos go cruinn. (2 mharc)']
# 3A: (slug, atlas, page, title, [(label, paper prompt, marks, scheme cut)], scheme start, scheme end)
POETRY_3A = [
    ('poetry-3a-a', 'F-3A-a', 10, 'Géibheann', [
        ('i', 'Tabhair dhá phointe eolais i d’fhocail féin faoin íomhá (faoin bpictiúr) den ainmhí a fhaighimid sna línte 1-8 den dán.', 8,
         '(i) Tabhair dhá phointe eolais i d’fhocail féin faoin íomhá'),
        ('ii', 'Cén sórt saoil atá ag an ainmhí anois? Tabhair dhá phointe eolais i d’fhocail féin faoin saol sin.', 8, '(ii) Cén sórt saoil'),
        ('iii', 'An bhfuil trua agat don ainmhí sa dán seo? Cuir fáthanna le do fhreagra. (Is leor dhá fháth.)', 9, '(iii) An bhfuil trua agat')],
     '(a) Géibheann (i)', '(b) An Spailpín Fánach (i)'),
    ('poetry-3a-b', 'F-3A-b', 11, 'An Spailpín Fánach', [
        ('i', '(a) Cén uair a bhíonn an spailpín “ag siúl an drúchta” i véarsa a haon?\n(b) Scríobh síos an dá uirlis a gheobhaidh an spailpín i véarsa a haon.\n'
              '(c) Cad a dhéanadh an spailpín i gCarraig na Siúire i véarsa a dó?\n(d) Cén rud a bhíonn á rá ag na daoine i nDurlas i véarsa a dó?', 8,
         '(i) (a) Cén uair a bhíonn an spailpín'),
        ('ii', 'Cén t-eolas a thugann an file dúinn faoi mhargadh na saoire i véarsa a trí? (Is leor dhá phointe eolais i d’fhocail féin.)', 8,
         '(ii) Cén t-eolas a thugann an file'),
        ('iii', 'Scríobh síos an mothúchán is láidre sa dán, dar leat. Tabhair dhá shampla, i d’fhocail féin, den mhothúchán sin sa dán.', 9,
         '(iii) Scríobh síos an mothúchán is láidre')],
     '(b) An Spailpín Fánach (i)', 'Níl cead aon ábhar a bhaineann le Filíocht Ainmnithe'),
]
POEM_TOPICS = {'poetry-3a-a': 'irish-5-2', 'poetry-3a-b': 'irish-5-1'}
# 3A(b)(i) prints four questions (a)–(d) at 2 each: (slug, sub-question) -> [(letter, scheme question, marks, next cut)]
SLOTS_3A = {
    ('poetry-3a-b', 'i'): [('a', 'Cén uair a bhíonn an spailpín “ag siúl an drúchta” i véarsa a haon?', 2, '(b) Scríobh síos an dá uirlis'),
                           ('b', 'Scríobh síos an dá uirlis a gheobhaidh an spailpín i véarsa a haon.', 2, '(c) Cad a dhéanadh an spailpín'),
                           ('c', 'Cad a dhéanadh an spailpín i gCarraig na Siúire i véarsa a dó?', 2, '(d) Cén rud a bhíonn'),
                           ('d', 'Cén rud a bhíonn á rá ag na daoine i nDurlas i véarsa a dó?', 2, None)],
}
POETRY_3B = [
    ('poetry-3b-a', 'F-3B-a', [
        '(i) Maidir le dán roghnach nua-aimseartha amháin a ndearna tú staidéar air le linn do chúrsa, scríobh síos i d’fhocail féin, príomhsmaointe an dáin. (9 marc)',
        '(ii) Cén t-atmaisféar atá sa dán seo, dar leat? Tabhair dhá shampla den atmaisféar sin sa dán. (7 marc)',
        '(iii) An maith leat an dán seo? Cuir fáthanna le do fhreagra. (Is leor dhá fháth.) (7 marc)'],
     '(a) (i) Maidir le dán roghnach nua-aimseartha', '(b) (i) Maidir le dán roghnach seanaimseartha', ['(ii) Cén t-atmaisféar', '(iii) An maith leat', 'Ní mór teideal an dáin']),
    ('poetry-3b-b', 'F-3B-b', [
        '(i) Maidir le dán roghnach seanaimseartha amháin a ndearna tú staidéar air le linn do chúrsa, cad is téama don dán sin, dar leat? '
        'Tabhair dhá phointe eolais i d’fhocail féin faoin téama sin sa dán. (9 marc)',
        '(ii) Scríobh síos an íomhá (an pictiúr) is mó a thaitníonn leat sa dán. Tabhair dhá phointe eolais faoin íomhá (faoin bpictiúr) sin sa dán. (7 marc)',
        '(iii) Cad é an mothúchán is láidre sa dán, dar leat? Tabhair dhá phointe eolais faoin mothúchán sin sa dán. (7 marc)'],
     '(b) (i) Maidir le dán roghnach seanaimseartha', None, ['(ii) Scríobh síos an íomhá', '(iii) Cad é an mothúchán', 'Ní mór teideal an dáin']),
]
TITLE_LINE = 'Ní mór teideal an dáin sin, mar aon le hainm an fhile, a scríobh síos go cruinn. (2 mharc)'

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
    s = Scheme(doc, 12, 24)
    assert s.removed == len(FURNITURE), s.removed
    assert not PUA.search(s.text), 'private-use glyph left in the scheme text'
    assert 'Níl sé i gceist a chur in iúl' not in s.text, '2016 prints no general literature note'
    lang_read = '[Gaeilge lochtach: 0 - 5 a bhaint den iomlán a gnóthaíodh.]'
    assert s.text.count(lang_read) == 2
    for letter, passage in PASSAGES.items():
        page_text = ' '.join(texts[p - 1] for p in passage['pages'])
        assert in_order(passage['title'], page_text), letter
        after = s.text.index(passage['start'])
        # Each passage prints one note above Ceist 1 (the penalty note only with the mark boxes at the end).
        notes = s.chunk('Nóta: Má tá dhá phointe eolais i gceist', passage['notes_end'], after)[0]
        assert notes == ('Nóta: Má tá dhá phointe eolais i gceist, tá 3 mharc ar an gcéad cheann atá ceart agus 2 mharc ar an '
                         'dara ceann atá ceart.'), notes
        assert in_order(passage['title'], s.text[after:after + 300]), letter
        passage['notes'] = notes
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
            permitted = [0, 3, 5] if (two or '= 3 mharc' in chunk) else [0, 5]
            resolved.append((q, part, prompt, chunk, spages, two, permitted))
        passage['resolved'] = resolved
    # Dís, Cáca Milis, An Lasair Choille, 2B(a), the 2B film and play, both 3A poems, 3B(a), 3B(b): ten, the prose
    # pages printing a closing full stop, the poetry pages none.
    assert len(LANG_LIT.findall(s.text)) == 10 and s.text.count('gnóthaíodh.]') == 2 + 6, (len(LANG_LIT.findall(s.text)), s.text.count('gnóthaíodh.]'))
    slug, atlas, letter, title, topic, intro, subs, start, end = DIS
    for line in [intro, title] + [p for _, p, _ in subs]:
        assert in_order(line, texts[7]), (slug, line[:40])
    for line in [FILM_OR_PLAY] + [x for item in FILM_PLAY_2A for x in [item[2]] + item[4]]:
        assert in_order(line, texts[7]), line[:50]
    for line in PROSE_2B_A[0] + PROSE_2B_B_LINES:
        assert in_order(line, texts[8]), line[:50]
    for slug3, atlas3, page, title3, subs3, start3, end3 in POETRY_3A:
        assert in_order(title3, texts[page - 1]), slug3
        for label, prompt, marks, cut in subs3:
            assert in_order(prompt.replace('\n', ' ') + f' ({marks} marc)', texts[page - 1]), (slug3, label)
    for slug4, atlas4, prompts, start4, end4, cuts4 in POETRY_3B:
        for line in prompts + [TITLE_LINE]:
            assert in_order(line, texts[11]), (slug4, line[:50])
    assert comparable(texts[11]).count(comparable(TITLE_LINE)) == 2
    for page, line in [(3, 'FREAGAIR GACH CEIST (1, 2 AGUS 3).'), (8, PROSE_CHOICE), (8, BOTH), (8, BOX_2A), (8, FILM_OR_PLAY), (9, BOX_2B),
                       (9, NO_PRESCRIBED_PROSE), (9, BOTH), (9, OPTIONAL_FILM_OR_PLAY), (10, POETRY_CHOICE), (10, BOTH), (10, BOX_3A), (12, BOX_3B),
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


def dis_pieces(m):
    slug, atlas, letter, title, topic, intro, subs, start, end = DIS
    whole, spages = m['s'].chunk(start, end)
    lang = language_note(whole)
    whole = before_language_note(whole)
    pieces = split_at(whole, [cut for _, _, cut in subs], slug)
    for (label, _, _), piece in zip(subs, pieces):
        assert '(5 mharc)' in piece, (slug, label)
    # The last piece ends at the question's printed total, which belongs to the whole answer, not to (v).
    assert pieces[-1].endswith('(25 marc)'), pieces[-1][-40:]
    pieces[-1] = pieces[-1][:-len('(25 marc)')].strip()
    return pieces, spages, lang


def poem_pieces(m, slug, subs, start, end):
    whole, spages = m['s'].chunk(start, end)
    lang = language_note(whole)
    whole = before_language_note(whole)
    pieces = split_at(whole, [cut for _, _, _, cut in subs], slug)
    for (label, _, marks, _), piece in zip(subs, pieces):
        assert f'({marks} marc)' in piece or (slug, label) in SLOTS_3A, (slug, label, piece[:60])
    return pieces, spages, lang


def slot_pieces(piece, slots):
    out = []
    for sub, question, marks, nxt in slots:
        start_at = piece.index(question)
        slot = piece[start_at:piece.index(nxt, start_at) if nxt else len(piece)].strip()
        # 2016 prints each question's price bare (“2 mharc”), then “Freagraí Samplacha:”.
        assert re.search(r'Freagraí [Ss]amplacha:', slot) and f'{question} {marks} mharc' in slot, (sub, slot[:80])
        out.append((sub, slot))
    return out


def slot_permitted(slot, marks):
    """0, the slot's mark, and every partial price its key prints (“Go moch = 1 mharc”)."""
    return sorted({0, marks} | {int(v) for v in re.findall(r'= (\d) mharc', slot) if int(v) <= marks})


WHOLE_PROSE_NOTE = ('One complete SEC response: five points at 5 (2 for the bare point + 3 for development); the 0–4 Gaeilge deduction applies once '
                    'to this whole 25-mark answer. The answer is judged on merit against that allocation.')
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
            crits = [criterion(part, f'({part}) Freagra', 5, [chunk, passage['notes']], permitted=permitted) for part, _, chunk, _, permitted in parts]
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
                [criterion(part, 'Freagra', 5, [chunk, passage['notes']], permitted=permitted)], READING_PART,
                'SEC allocation for this part' + (': first correct point 3, second 2 (0/3/5).' if two else '.') + ' ' + reading_note(m), src)
            practice_ids.append(cards[-1]['id'])

    sub_note = 'One printed sub-question at its published tariff. ' + LIT_DEDUCTION_NOTE
    question_lit = []
    # ---- Ceist 2A: Dís (five sub-questions), then Cáca Milis or An Lasair Choille ----------------------
    slug, atlas, letter, title, topic, intro, subs, start, end = DIS
    pieces, spages, dis_lang = dis_pieces(m)
    src = source('Prós Ainmnithe', title, [8])
    add(atlas, slug, 'Prose 2A(a)', f'({letter}) {title}\n{intro}\n' + '\n'.join(f'({l}) {p}' for l, p, _ in subs) + '\n(25 marc)',
        topic, [8], spages,
        [criterion(f'eolas-{label}', f'({label}) Eolas', 5, [piece], 'indicative') for (label, _, _), piece in zip(subs, pieces)]
        + [deduction(dis_lang)], [PROSE_CHOICE, BOTH] + LIT,
        'One complete SEC response: five printed sub-questions at 5 each, each at its printed split, then the 0–4 Gaeilge deduction once. '
        'The scheme prints no sample answers for Dís; answers are judged on merit against those splits.', src,
        concept=f'irish-prose-2a-{topic}', stem=BOX_2A)
    question_lit.append(cards[-1]['id'])
    for slug_b, atlas_b, title_b, topic_b, lines_b, start_b, end_b in FILM_PLAY_2A:
        chunk, bpages = m['s'].chunk(start_b, end_b)
        assert '5 phointe eolais agus 5 mharc ar gach pointe eolais' in chunk, slug_b
        lang_b = language_note(chunk)
        other = 'An Lasair Choille' if title_b == 'Cáca Milis' else 'Cáca Milis'
        add(atlas_b, slug_b, f'Prós 2A(b) · {title_b}', f'(b) {FILM_OR_PLAY}\n{title_b}\n' + '\n'.join(lines_b) + ' (25 marc)', topic_b, [8],
            bpages, [criterion('eolas', 'Eolas', 25, [before_language_note(chunk)], 'indicative'), deduction(lang_b)],
            [PROSE_CHOICE, BOTH, FILM_OR_PLAY] + LIT[1:],
            WHOLE_PROSE_NOTE + f' 2A(b) offers Cáca Milis or An Lasair Choille; this card is {title_b} (the other printed question, {other}, is its own card).',
            source('Prós Ainmnithe', title_b, [8]), concept=f'irish-ol-p2-{slug_b}', stem=BOX_2A)
        question_lit.append(cards[-1]['id'])

    # ---- Ceist 2B: Prós Roghnach (a) the optional short story and (b) the optional film or play --------
    lines2, start2, end2, parts = PROSE_2B_A
    chunk2, spages2 = m['s'].chunk(start2, end2)
    lang2 = language_note(chunk2)
    chunk2 = before_language_note(chunk2)
    cuts = [0] + [chunk2.index(cut) for _, _, _, cut in parts[1:]]
    bits = [chunk2[a:b].strip() for a, b in zip(cuts, cuts[1:] + [len(chunk2)])]
    assert bits[0].endswith('Príomhthéama an ghearrscéil = 3 mharc') and bits[1].startswith('4 phointe eolais ag teastáil (5 mharc an ceann) = 20 marc'), bits[:2]
    crits = [criterion(cid, label, marks, [bit], 'exact' if cid == 'teideal' else 'indicative',
                       permitted=None if cid == 'eolas' else sorted({0, marks} | {int(v) for v in re.findall(r'= (\d) mharc', bit) if int(v) <= marks}))
             for (cid, label, marks, _), bit in zip(parts, bits)]
    assert crits[-1]['guidance'][0].endswith('(2 mharc)'), crits[-1]['guidance'][0][-60:]
    add('P-2B-a', 'prose-2b-a', 'Prose 2B(a)', '\n'.join(lines2), 'irish-4-7', [9], spages2, crits + [deduction(lang2)],
        [PROSE_CHOICE, NO_PRESCRIBED_PROSE, BOTH] + LIT[1:],
        'One complete SEC response: ' + ', '.join(f'{label} {marks}' for _, label, marks, _ in parts) +
        ', then the 0–4 Gaeilge deduction once. The optional text is open content chosen by the candidate; the scheme prints no sample '
        'points for it, so its points are judged on merit against these allocations (indicative rather than exhaustive).',
        source('Prós Roghnach', 'Gearrscéal roghnach', [9]), concept='irish-prose-2b-irish-4-7', stem=STEM_2B)
    question_lit.append(cards[-1]['id'])
    film, fpages = m['s'].chunk('Maidir le scannán roghnach', 'NÓ Maidir le dráma roghnach')
    play, ppages = m['s'].chunk('Maidir le dráma roghnach', 'Freagair A (Filíocht Ainmnithe)')
    # Each alternative's key is its 23-mark allocation, then its printed title line (2 mharc), then the language note.
    film_lang, play_lang = language_note(film), language_note(play)
    assert film_lang == play_lang
    film, play = before_language_note(film), before_language_note(play)
    film_eolas, film_title = film[:film.index('Ní mór teideal an scannáin')].strip(), film[film.index('Ní mór teideal an scannáin'):]
    play_eolas, play_title = play[:play.index('Ní mór teideal an dráma')].strip(), play[play.index('Ní mór teideal an dráma'):]
    for bit, cap in [(film_eolas, '(23 marc)'), (play_eolas, '(23 marc)'), (film_title, '(2 mharc)'), (play_title, '(2 mharc)')]:
        assert cap in bit, (cap, bit[-60:])
    add('P-2B-b', 'prose-2b-b', 'Prose 2B(b)', '\n'.join(PROSE_2B_B_LINES), 'irish-4-7', [9], sorted(set(fpages) | set(ppages)),
        [criterion('eolas', 'Príomhimeachtaí', 23, [film_eolas, play_eolas], 'indicative'),
         criterion('teideal', 'Teideal + ainm an scríbhneora', 2, [film_title, play_title], 'exact', permitted=[0, 1, 2]), deduction(film_lang)],
        [PROSE_CHOICE, NO_PRESCRIBED_PROSE, BOTH, OPTIONAL_FILM_OR_PLAY] + LIT[1:],
        'One complete SEC response about an optional film or an optional play (the same scheme for both): 23 for five points (5, 5, 5, 4, 4) '
        'and 2 for the exact title and writer, then the 0–4 Gaeilge deduction once. The text is open content chosen by the candidate '
        '(indicative rather than exhaustive).',
        source('Prós Roghnach', 'Scannán nó dráma roghnach', [9]), concept='irish-prose-2b-irish-4-7', stem=STEM_2B)
    question_lit.append(cards[-1]['id'])

    # ---- Ceist 3A: Géibheann and An Spailpín Fánach ----------------------------------------------------
    poem_parts = {}
    for slug3, atlas3, page, title3, subs3, start3, end3 in POETRY_3A:
        pieces3, spages3, lang3 = poem_pieces(m, slug3, subs3, start3, end3)
        poem_parts[slug3] = (pieces3, spages3, lang3)
        crits = [criterion(f'eolas-{label}', f'({label}) Eolas', marks, [piece], 'indicative')
                 for (label, _, marks, _), piece in zip(subs3, pieces3)]
        prompt = '\n'.join(f'({label}) {p}' + f' ({marks} marc)' for label, p, marks, _ in subs3)
        add(atlas3, slug3, f'Poetry 3A({atlas3[-1]})', f'({atlas3[-1]}) {title3}\n' + prompt, POEM_TOPICS[slug3], [page], spages3, crits + [deduction(lang3)],
            [POETRY_CHOICE, BOTH] + LIT,
            'One complete SEC response: ' + ', '.join(f'({label}) {marks}' for label, _, marks, _ in subs3) +
            ' at their printed tariffs, then the 0–4 Gaeilge deduction once. The sample answers are indicative rather than exhaustive; '
            'lines lifted straight from the poem without the candidate’s own words earn 2 + 2 where the scheme says so.',
            source('Filíocht Ainmnithe', title3, [page]), concept=f'irish-poetry-3a-{POEM_TOPICS[slug3]}', stem=BOX_3A)
        question_lit.append(cards[-1]['id'])

    # ---- Ceist 3B: Filíocht Roghnach (a) a modern poem and (b) an old poem -----------------------------
    for slug4, atlas4, prompts, start4, end4, cuts4 in POETRY_3B:
        chunk4, spages4 = m['s'].chunk(start4, end4, m['s'].text.index('⟦23⟧'))
        lang4 = language_note(chunk4)
        chunk4 = before_language_note(chunk4)
        idx = [0] + [chunk4.index(cut) for cut in cuts4]
        bits = [chunk4[a:b].strip() for a, b in zip(idx, idx[1:] + [len(chunk4)])]
        for bit, cap in zip(bits, ['(9 marc)', '(7 marc)', '(7 marc)', '(2 mharc)']):
            assert cap in bit, (slug4, cap)
        crits = [criterion('eolas-i', '(i) Eolas', 9, [bits[0]], 'indicative'), criterion('eolas-ii', '(ii) Eolas', 7, [bits[1]], 'indicative'),
                 criterion('eolas-iii', '(iii) Eolas', 7, [bits[2]], 'indicative'),
                 criterion('teideal', 'Teideal + ainm an fhile', 2, [bits[3]], 'exact', permitted=[0, 1, 2])]
        modern = atlas4.endswith('a')
        add(atlas4, slug4, f'Poetry 3B({atlas4[-1]})', f'({atlas4[-1]}) ' + '\n'.join(prompts + [TITLE_LINE]), 'irish-5-6', [12], spages4,
            crits + [deduction(lang4)], [POETRY_CHOICE, NO_PRESCRIBED_POETRY, BOTH] + LIT,
            'One complete SEC response: (i) 9, (ii) 7, (iii) 7, poem and poet 2, then the 0–4 Gaeilge deduction once. '
            + ('3B(a) asks for a modern poem. ' if modern else '3B(b) asks for an old poem. ')
            + 'The optional poem is open content; the printed allocations are judged on merit (indicative rather than exhaustive).',
            source('Filíocht Roghnach', f'3B({atlas4[-1]}) · Dán roghnach', [12]),
            concept='irish-poetry-3b-irish-5-6', stem=STEM_3B)
        question_lit.append(cards[-1]['id'])

    # ---- Practice: the five Dís sub-questions, every prescribed-poetry sub-question, 3A(b)(i)(a)–(d) ----
    src = source('Prós Ainmnithe', title, [8])
    for (label, prompt, _), piece in zip(subs, pieces):
        # The paper prints no per-sub-question tariff for 2A(a); the scheme prices each at (5 mharc).
        add(f'{atlas}-{label}', f'{slug}-{label}', f'Prós 2A({letter}) · {title} · ({label})', f'({letter}) {title}\n{intro}\n({label}) {prompt}',
            topic, [8], spages, [criterion('eolas', 'Eolas', 5, [piece], 'indicative')],
            [PROSE_CHOICE, BOTH] + LIT[1:], sub_note, src, stem=BOX_2A)
        practice_ids.append(cards[-1]['id'])
    for slug3, atlas3, page, title3, subs3, start3, end3 in POETRY_3A:
        pieces3, spages3, _ = poem_parts[slug3]
        topic3 = POEM_TOPICS[slug3]
        src3 = source('Filíocht Ainmnithe', title3, [page])
        head = f'({atlas3[-1]}) {title3}\n'
        for (label, prompt, marks, _), piece in zip(subs3, pieces3):
            slots = SLOTS_3A.get((slug3, label))
            add(f'{atlas3}-{label}', f'{slug3}-{label}', f'Filíocht 3A({atlas3[-1]}) · {title3} · ({label})', head + f'({label}) {prompt} ({marks} marc)',
                topic3, [page], spages3, [criterion('eolas', 'Eolas', marks, [piece], 'indicative')],
                [POETRY_CHOICE, BOTH] + LIT[1:], sub_note, src3, stem=BOX_3A)
            practice_ids.append(cards[-1]['id'])
            if slots:
                printed = dict(re.findall(r'\(([a-d])\) ([^\n]+)', prompt))
                for (sub, slot), (_, _, smarks, _) in zip(slot_pieces(piece, slots), slots):
                    add(f'{atlas3}-{label}-{sub}', f'{slug3}-{label}-{sub}', f'Filíocht 3A({atlas3[-1]}) · {title3} · ({label})({sub})',
                        head + f'({label}) ({sub}) {printed[sub]}', topic3, [page], spages3,
                        [criterion('eolas', 'Freagra', smarks, [slot], 'indicative', permitted=slot_permitted(slot, smarks))], [POETRY_CHOICE, BOTH] + LIT[1:],
                        f'One printed question inside 3A({atlas3[-1]})({label}), at its printed {smarks} mharc. ' + LIT_DEDUCTION_NOTE, src3, stem=BOX_3A)
                    practice_ids.append(cards[-1]['id'])

    assert len(whole_ids) == 10 and len(question_lit) == 9 and len(practice_ids) == 35, (len(whole_ids), len(question_lit), len(practice_ids))
    assert len(cards) == 54 and len({c['id'] for c in cards}) == 54 and len({c['atlasQuestionId'] for c in cards}) == 54
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
                                '2A(b)’s two prescribed questions (Cáca Milis, An Lasair Choille) are a card each and 2B(b)’s optional film or play is one card; '
                                'no combination cards.'),
                  boundaries=('10 whole reading questions with their 20 published parts; 9 literature question cards (2A(a), 2A(b) Cáca Milis, '
                              '2A(b) An Lasair Choille, 2B(a), 2B(b), 3A(a), 3A(b), 3B(a), 3B(b)); the 5 printed 2A(a) Dís sub-questions, '
                              'the 6 prescribed-poetry sub-questions and the 4 printed questions inside 3A(b)(i).'))
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
    print(f"Irish Ordinary {YEAR} Paper 2: {len(data['cards'])} reviewed cards (19 printed questions, 35 practice parts); the archive remains incomplete.")


if __name__ == '__main__':
    main()
