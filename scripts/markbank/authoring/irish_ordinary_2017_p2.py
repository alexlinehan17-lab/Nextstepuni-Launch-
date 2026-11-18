#!/usr/bin/env python3
"""Reviewed 2017 Ordinary Paper 2 (Léamhthuiscint agus Litríocht), carded new.

Paper PDF 1–12 and the Paper 2 pages of the combined LC001GLP000IV scheme (PDF 13–28,
plus 29 modified marking) reviewed on 2026-11-04. Counts are assertions, not
corpus-completeness proof. Same method as irish_ordinary_2018_p2.py.

No 2017 Ordinary card existed before. `build` cards the component the way the reviewed
2018–2026 Ordinary Paper 2s are carded: the ten whole reading questions (each part its
own 5-mark criterion), the nine literature questions (each printed sub-question its own
criterion, the 0–4 Gaeilge deduction once), and the practice cards beside them: every
reading part (20), the five printed sub-questions of each 2A(a) text (10), every
prescribed-poetry sub-question (6), the two printed questions inside 3A(a)(iii)
Colscaradh and the three inside 3A(b)(i) An tEarrach Thiar.

2017's layout is 2018's: “FREAGAIR GACH CEIST (1, 2 AGUS 3).” Ceist 1 is Léamhthuiscint
A and B (both); Ceist 2 is A (Prós Ainmnithe) or B (Prós Roghnach) and Ceist 3 is A
(Filíocht Ainmnithe) or B (Filíocht Roghnach), each section printing two questions, (a)
and (b), both to be answered (“Freagair (a) agus (b) anseo.”). 2A(a) prints the
prescribed film Cáca Milis or the prescribed play An Lasair Choille, five sub-questions
each, under different Atlas headings: a card each (the 2026 Ordinary form), with every
sub-question a practice card. 2A(b) is Hurlamaboc, one 25-mark question. 2B(a) is an
optional film or an optional play with one scheme for both: one card carrying both
printed alternatives. 2B(b) is a novel extract (theme 3 + four points 20 + title 2).
Each literature card carries the printed choice and “Freagair (a) agus (b) anseo.” as
its task check (choice is not a route; no card combines two questions), and the
section's printed box heading with, for B, the printed restriction as its lead-in.

The scheme's text layer stores each page's boxed heading (“CEIST 1 (A + B) -
LÉAMHTHUISCINT - 100 marc”, “B – (50 marc)” …) with the page body; `Scheme` removes
those exact strings so no heading lands inside an answer key.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import re
from pathlib import Path
from irish_lifted import PUA, scheme_words_in, symbol_text

ROOT = Path(__file__).resolve().parents[3]
YEAR = 2017
FILE = 'LC001GLP200IV'
SCHEME_FILE = 'LC001GLP000IV'
OUT = ROOT / 'components/MarkBank/cards/irish/ordinary-2017-p2-authored.json'
SOURCE_REVIEW = ROOT / 'scripts/markbank/authored/irish-ordinary-2017-p2-source-review.json'
REVIEWED_AT = '2026-11-04'
PAPER_SHA = '8dadf2aeec1dabdfb930cb98aba28fc6cc3602714e7a5920a169d9dcc525e8c3'
SCHEME_SHA = '7d54fc1fa90536c2d4d44610f429a262d67ce0445a4ef173bd00b4f5f44539d7'
DIRECTIVE = re.compile(r'rogha|roghna|Freagair|Luaigh|Ainmnigh|\bnó\b|dhá phointe|dhá rud|dhá bh|dhá dh|dhá ch|dhá fh|dhá th|dhá ph|dhá sh|'
                       r'\ban dá\b|ceann amháin|pointe amháin|amháin|\bdhá\b', re.I)
SOURCE_NOTE = 'Shown page-for-page from the official examination paper; swipe to move between pages.'
ATTRIBUTION = '© State Examinations Commission.'
# Boxed page headings the 2017 scheme's text layer stores with the page body (exact strings, each printed once).
FURNITURE = ('CEIST 1 (A + B) - LÉAMHTHUISCINT - 100 marc', 'A – (50 marc)', 'B – (50 marc)',
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


# Two points priced first-correct 3, second 2: “3 mharc + 2 mharc = 5 mharc”, or the bare “5 mharc” followed by
# “An chéad … atá ceart = 3 mharc; an dara … atá ceart = 2 mharc”.
TWO_POINTS = re.compile(r'3 mharc \+ 2 mharc|; an dara [^=;]+ atá ceart = 2 mharc')

# (q, part, paper prompt, scheme anchor)
PASSAGES = {
    'A': dict(title='Slí an Atlantaigh Fhiáin – Turas a fhanfaidh i do chuimhne', pages=[4, 5], topic='irish-3-0', start='⟦13⟧', notes_end='1. (a)',
              end='Nóta: Gearrfar pionós i ngeall ar iomarcaíocht. Léireofar', parts=[
        ('1', 'a', '(a) Scríobh síos dhá rud faoin turasóireacht in Éirinn sa bhliain 2016. (Alt 1)', '1. (a) Scríobh síos dhá rud faoin turasóireacht'),
        ('1', 'b', '(b) Luaigh dhá shlí a gcuirtear daoine ar an eolas faoi Shlí an Atlantaigh Fhiáin. (Alt 1)', '(b) Luaigh dhá shlí a gcuirtear daoine'),
        ('2', 'a', '(a) Tá a lán rudaí éagsúla le feiceáil ar Shlí an Atlantaigh Fhiáin. Scríobh síos dhá cheann de na rudaí sin. (Alt 2)',
         '2. (a) Tá a lán rudaí éagsúla le feiceáil'),
        ('2', 'b', '(b) Conas atá a fhios againn go bhfuil áit speisialta ag Route 66 i gcultúr Mheiriceá? (Alt 2)', '(b) Conas atá a fhios againn'),
        ('3', 'a', '(a) Scríobh síos dhá chúis a bhfuil clú agus cáil ar Shlí an Atlantaigh Fhiáin anois. (Alt 3)', '3. (a) Scríobh síos dhá chúis a bhfuil clú'),
        ('3', 'b', '(b) Cén fáth a mbronntar bratach ghorm? (Alt 3)', '(b) Cén fáth a mbronntar bratach ghorm'),
        ('4', 'a', '(a) Cén fáth a raibh Sceilg Mhichíl sa nuacht? (Alt 4)', '4. (a) Cén fáth a raibh Sceilg Mhichíl'),
        ('4', 'b', '(b) Tabhair dhá phíosa eolais faoin mainistir ar Sceilg Mhichíl. (Alt 4)', '(b) Tabhair dhá phíosa eolais faoin mainistir'),
        ('5', 'a', '(a) Cén dá bhuntáiste a bhaineann leis an bpas speisialta atá ar fáil do thurasóirí? (Alt 5)', '5. (a) Cén dá bhuntáiste'),
        ('5', 'b', '(b) Cén t-eolas faoi Shlí an Atlantaigh Fhiáin atá le fáil ar an aip speisialta? (Alt 5)', '(b) Cén t-eolas faoi Shlí an Atlantaigh Fhiáin atá le fáil')]),
    'B': dict(title='Kíla – Tríocha Bliain ar an mBóthar', pages=[6, 7], topic='irish-3-1', start='⟦16⟧', notes_end='1. (a)',
              end='Nóta: Gearrfar pionós i ngeall ar iomarcaíocht. Léireofar', parts=[
        ('1', 'a', '(a) Cad a rinne an grúpa ceoil Kíla sa bhliain 1987? (Alt 1)', '1. (a) Cad a rinne an grúpa ceoil Kíla'),
        ('1', 'b', '(b) Cad a theastaigh ó Kíla a dhéanamh nuair a bhí siad ag tosú? (Alt 1)', '(b) Cad a theastaigh ó Kíla'),
        ('2', 'a', '(a) Cén dá rud a bhíodh ar siúl ag na buachaillí agus iad ar scoil? (Alt 2)', '2. (a) Cén dá rud a bhíodh ar siúl'),
        ('2', 'b', '(b) Cén fáth a mbíodh ar bhaill an ghrúpa dul ag buscáil ar na sráideanna? (Alt 2)', '(b) Cén fáth a mbíodh ar bhaill'),
        ('3', 'a', '(a) Cén stíl cheoil atá ag an ngrúpa Kíla? (Alt 3)', '3. (a) Cén stíl cheoil atá ag an ngrúpa'),
        ('3', 'b', '(b) Scríobh síos dhá fháth a mbíonn gach ceolchoirm difriúil. (Alt 3)', '(b) Scríobh síos dhá fháth a mbíonn gach ceolchoirm'),
        ('4', 'a', '(a) Tabhair dhá phíosa eolais faoi Alive Beo, an t-albam nua a d’eisigh Kíla cúpla mí ó shin. (Alt 4)', '4. (a) Tabhair dhá phíosa eolais faoi Alive Beo'),
        ('4', 'b', '(b) Bhí Kíla ag seinm ag dhá fhéile in Éirinn an samhradh seo caite. Scríobh síos ainmneacha an dá fhéile sin. (Alt 4)',
         '(b) Bhí Kíla ag seinm ag dhá fhéile'),
        ('5', 'a', '(a) Cá mbíonn Kíla le cloisteáil na laethanta seo? (Alt 5)', '5. (a) Cá mbíonn Kíla le cloisteáil'),
        ('5', 'b', '(b) Cad atá sa leabhar a chuir Kíla amach sa bhliain 2011? (Alt 5)', '(b) Cad atá sa leabhar a chuir Kíla')]),
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
FILM_OR_PLAY = 'Freagair na ceisteanna thíos faoin scannán Cáca Milis nó faoin dráma An Lasair Choille.'
OPTIONAL_FILM_OR_PLAY = 'Freagair an cheist thíos faoin scannán roghnach nó faoin dráma roghnach.'
# The 2023 builders' requirement lines; irish_lifted.printed_tasks gives each its English.
LIT = ['Freagair gach fochuid atá priontáilte sa rogha seo.', 'Úsáid tagairtí cruinne agus ábhartha don téacs.']
READING_PART = ['Léigh an sliocht iomlán a ghabhann leis an gceist. Freagair an chuid atá luaite ar an gcárta.', 'Úsáid an t-alt a luaitear.']
READING_WHOLE = ['Léigh an sliocht oifigiúil a ghabhann leis an gceist.', 'Freagair gach fochuid agus cloígh leis an alt a luaitear.']

# 2A(a): the prescribed film or the prescribed play, a card each, five printed sub-questions at 5 (the paper prints
# only each text's (25 marc)). (slug, atlas, title, topic, [(label, paper prompt, scheme anchor)], scheme start, scheme end)
PRESCRIBED_2A = [
    ('prose-2a-a-caca-milis', 'P-2A-a-caca-milis', 'Cáca Milis', 'irish-4-6', [
        ('i', 'Tá imní ar mháthair Catherine sa charr. Scríobh síos dhá chúis a bhfuil imní uirthi.', '(i) Tá imní ar mháthair Catherine'),
        ('ii', 'Luaigh dhá rud atá le foghlaim faoi Paul sula suíonn sé síos os comhair Catherine ar an traein.', '(ii) Luaigh dhá rud atá le foghlaim'),
        ('iii', 'Cén t-eolas a thugann Paul do Catherine faoi bheith ar an raidió?', '(iii) Cén t-eolas a thugann Paul'),
        ('iv', 'Déan cur síos ar bhréag amháin a insíonn Catherine do Paul.', '(iv) Déan cur síos ar bhréag amháin'),
        ('v', 'An bhfuil trua agat do Paul sa scannán? Tabhair dhá fháth le do fhreagra.', '(v) An bhfuil trua agat do Paul')],
     'Cáca Milis (25 marc)', 'An Lasair Choille (25 marc)'),
    ('prose-2a-a-an-lasair-choille', 'P-2A-a-an-lasair-choille', 'An Lasair Choille', 'irish-4-8', [
        ('i', 'Cén fáth nach bhfuil Micil, an seanfhear, ábalta codladh ag tús an dráma?', '(i) Cén fáth nach bhfuil Micil'),
        ('ii', 'Cad a cheapann Micil den chomhrá a bhí ag Séamas leis an mBúrcach faoi dhul go Sasana?', '(ii) Cad a cheapann Micil'),
        # The scheme prints this prompt without “síos” (“(iii) Scríobh dhá phíosa eolais …”); the card shows the paper's print.
        ('iii', 'Scríobh síos dhá phíosa eolais faoin saol atá ag Míoda lena hathair, dar léi féin.', '(iii) Scríobh dhá phíosa eolais faoin saol'),
        ('iv', 'Tháinig athair Mhíoda go teach Mhicil agus labhair sé le Míoda agus le Séamas.\nScríobh síos dhá rud a dúirt athair Mhíoda leo.',
         '(iv) Tháinig athair Mhíoda go teach Mhicil'),
        ('v', 'An bhfuil trua agat do Shéamas sa dráma? Tabhair dhá fháth le do fhreagra.', '(v) An bhfuil trua agat do Shéamas')],
     'An Lasair Choille (25 marc)', '(b) Hurlamaboc (25 marc)'),
]
# 2A(b) Hurlamaboc: one 25-mark question.
HURLAMABOC = ('prose-2a-b', 'P-2A-b', 'b', 'Hurlamaboc', 'irish-4-5',
              '“Bhí Lisín sásta … Bhí a lán le ceiliúradh acu.” Hurlamaboc\n'
              'Déan cur síos ar na cúiseanna a raibh Lisín sásta agus ar na rudaí a bhí le ceiliúradh aici féin agus ag muintir Albright.',
              '(b) Hurlamaboc (25 marc)', 'Níl cead aon ábhar a bhaineann le Prós Ainmnithe')
# 2B(a): the optional film or the optional play, one card with both printed alternatives (one scheme for both).
PROSE_2B_A_LINES = [
    '(a) ' + OPTIONAL_FILM_OR_PLAY,
    'Maidir le scannán roghnach a ndearna tú staidéar air le linn do chúrsa, ainmnigh an phearsa (an carachtar) is mó a thaitníonn leat sa scannán. '
    'Tabhair cuntas ar na heachtraí is mó a tharlaíonn don duine sin sa scannán. (23 marc)',
    'Ní mór teideal an scannáin sin, mar aon le hainm an scríbhneora, a scríobh síos go cruinn. (2 mharc)',
    'NÓ',
    'Maidir le dráma roghnach a ndearna tú staidéar air le linn do chúrsa, ainmnigh an phearsa (an carachtar) is mó a thaitníonn leat sa dráma. '
    'Tabhair cuntas ar na heachtraí is mó a tharlaíonn don duine sin sa dráma. (23 marc)',
    'Ní mór teideal an dráma sin, mar aon le hainm an scríbhneora, a scríobh síos go cruinn. (2 mharc)']
# 2B(a) criteria: (id, label, marks, cut-before) inside each alternative's key.
PROSE_2B_A_PARTS = [('priomhphearsa', 'An phearsa is mó a thaitníonn leat', 1, None), ('eolas', 'Na heachtraí is mó', 22, 'Na heachtraí is mó a tharlaíonn'),
                    ('teideal', 'Teideal + ainm an scríbhneora', 2, 'Ní mór teideal')]
# 2B(b): the optional novel extract (theme 3, four points 20, title and author 2).
PROSE_2B_B = (['(b) Maidir le giota as úrscéal roghnach a ndearna tú staidéar air le linn do chúrsa, cad é an príomhthéama sa ghiota sin, dar leat? '
               'Tabhair cuntas ar na príomhimeachtaí (príomhrudaí) a tharlaíonn sa ghiota a léiríonn an príomhthéama sin. (23 marc)',
               'Ní mór teideal an úrscéil sin, mar aon le hainm an údair, a scríobh síos go cruinn. (2 mharc)'],
              '(b) Maidir le giota as úrscéal roghnach', 'Freagair A (Filíocht Ainmnithe)',
              [('priomhthema', 'Príomhthéama an ghiota', 3, None), ('eolas', 'Na príomhimeachtaí', 20, '4 phointe eolais ag teastáil'),
               ('teideal', 'Teideal + ainm an údair', 2, 'Ní mór teideal')])
# 3A: (slug, atlas, page, title, [(label, paper prompt, marks, scheme cut)], scheme start, scheme end)
POETRY_3A = [
    ('poetry-3a-a', 'F-3A-a', 10, 'Colscaradh', [
        ('i', 'Scríobh síos, i d’fhocail féin, na príomhsmaointe atá i véarsa a haon. (Is leor dhá phointe eolais.)', 8,
         '(i) Scríobh síos, i d’fhocail féin, na príomhsmaointe'),
        ('ii', 'Scríobh síos, i d’fhocail féin, dhá rud a bhí ag teastáil ón mbean ina saol i véarsa a dó.', 8, '(ii) Scríobh síos, i d’fhocail féin, dhá rud'),
        ('iii', '(a) Cén réiteach a bhí ag an mbeirt acu ar an bhfadhb?\n(b) An réiteach sásúil é sin, dar leat? Cuir fáthanna le do fhreagra. (Is leor dhá fháth.)', 9,
         '(iii) (a) Cén réiteach')],
     '(a) Colscaradh (25 marc)', '(b) An tEarrach Thiar (25 marc)'),
    ('poetry-3a-b', 'F-3A-b', 11, 'An tEarrach Thiar', [
        ('i', '(a) Cén sórt lae atá ann i véarsa a haon?\n(b) Cad atá ar siúl ag an bhfear i véarsa a dó?\n(c) Tabhair dhá phíosa eolais faoin gcurrach i véarsa a ceathair.', 8,
         '(i) (a) Cén sórt lae'),
        ('ii', 'Déan cur síos, i d’fhocail féin, ar an íomhá (ar an bpictiúr) de na mná a thugann an file dúinn i véarsa a trí. (Is leor dhá phointe eolais.)', 8,
         '(ii) Déan cur síos, i d’fhocail féin'),
        ('iii', 'Scríobh síos an mothúchán is láidre sa dán, dar leat. Tabhair dhá shampla, i d’fhocail féin, den mhothúchán sin sa dán.', 9,
         '(iii) Scríobh síos an mothúchán is láidre')],
     '(b) An tEarrach Thiar (25 marc)', 'Níl cead aon ábhar a bhaineann le Filíocht Ainmnithe'),
]
POEM_TOPICS = {'poetry-3a-a': 'irish-5-5', 'poetry-3a-b': 'irish-5-3'}
# What each poem's scheme says of lines lifted straight from the poem (English notes; the scheme lines are in the guidance).
LIFTED_LINES = {'poetry-3a-a': 'in (i) and (ii) the scheme gives apt lines lifted straight from the verse without the candidate’s own words 2 + 2',
                'poetry-3a-b': 'in (iii) the scheme gives apt lines from the poem without the candidate’s own words 2 + 2, and (i) and (ii) name the verse '
                               'lines that answer them'}
# Printed questions inside one printed sub-question: (slug, sub-question) -> [(letter, scheme question, marks, printed caption, next cut)]
SLOTS_3A = {
    ('poetry-3a-a', 'iii'): [('a', 'Cén réiteach a bhí ag an mbeirt acu ar an bhfadhb?', 2, '(2 mharc)', '(b) An réiteach sásúil'),
                             ('b', 'An réiteach sásúil é sin, dar leat?', 7, '(7 marc)', None)],
    ('poetry-3a-b', 'i'): [('a', 'Cén sórt lae atá ann i véarsa a haon?', 2, '(2 mharc)', '(b) Cad atá ar siúl'),
                           ('b', 'Cad atá ar siúl ag an bhfear i véarsa a dó?', 2, '(2 mharc)', '(c) Tabhair dhá phíosa'),
                           ('c', 'Tabhair dhá phíosa eolais faoin gcurrach i véarsa a ceathair.', 4, '(2 mharc + 2 mharc)', None)],
}
SLOT_PERMITTED = {('poetry-3a-b', 'i'): [0, 2, 4, 6, 8]}
POETRY_3B = [
    ('poetry-3b-a', 'F-3B-a', [
        '(i) Maidir le dán roghnach nua-aimseartha amháin a ndearna tú staidéar air le linn do chúrsa, cad is téama don dán sin, dar leat? '
        'Tabhair dhá phointe eolais i d’fhocail féin faoin téama sin sa dán. (9 marc)',
        '(ii) Cén íomhá (pictiúr) is mó a thaitníonn leat sa dán? Cuir fáthanna le do fhreagra. (Is leor dhá fháth.) (7 marc)',
        '(iii) Cén t-atmaisféar atá sa dán seo, dar leat? Tabhair dhá shampla den atmaisféar sin sa dán. (7 marc)'],
     '(a) (i) Maidir le dán roghnach nua-aimseartha', '(b) (i) Maidir le dán roghnach nua-aimseartha', ['(ii) Cén íomhá (pictiúr)', '(iii) Cén t-atmaisféar', 'Ní mór teideal an dáin']),
    ('poetry-3b-b', 'F-3B-b', [
        '(i) Maidir le dán roghnach nua-aimseartha amháin a ndearna tú staidéar air le linn do chúrsa agus nár úsáid tú i gcuid (a) thuas, '
        'scríobh síos i d’fhocail féin, príomhsmaointe an dáin. (9 marc)',
        '(ii) Scríobh síos an mothúchán is láidre sa dán, dar leat. Tabhair dhá shampla den mhothúchán sin sa dán. (7 marc)',
        '(iii) An maith leat an dán seo? Cuir fáthanna le do fhreagra. (Is leor dhá fháth.) (7 marc)'],
     '(b) (i) Maidir le dán roghnach nua-aimseartha', None, ['(ii) Scríobh síos an mothúchán', '(iii) An maith leat', 'Ní mór teideal an dáin']),
]
TITLE_LINE = 'Ní mór teideal an dáin sin, mar aon le hainm an fhile, a scríobh síos go cruinn. (2 mharc)'
# The literature language note, printed with a closing full stop on the six prose answers and without one on the four poems.
LANG_PROSE = '[Gaeilge lochtach: 0-4 a bhaint den iomlán a gnóthaíodh.]'
LANG_POETRY = '[Gaeilge lochtach: 0-4 a bhaint den iomlán a gnóthaíodh]'

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
    s = Scheme(doc, 13, 28)
    assert s.removed == len(FURNITURE), s.removed
    assert not PUA.search(s.text), 'private-use glyph left in the scheme text'
    assert 'Léirigh mionbhriseadh' not in s.text, '2017 prints no literature mark-panel line'
    lang_read = '[Gaeilge lochtach: 0 - 5 a bhaint den iomlán a gnóthaíodh.]'
    assert s.text.count(lang_read) == 2
    for letter, passage in PASSAGES.items():
        page_text = ' '.join(texts[p - 1] for p in passage['pages'])
        after = s.text.index(passage['start'])
        # 2017 prints one note above each passage's Ceist 1 (the penalty note only with the mark boxes at the end).
        notes = s.chunk('Nóta: Má tá dhá phointe eolais i gceist', passage['notes_end'], after)[0]
        assert notes == 'Nóta: Má tá dhá phointe eolais i gceist, tá 3 mharc ar an gcéad cheann atá ceart agus 2 mharc ar an dara ceann atá ceart.', notes
        assert in_order(passage['title'], texts[passage['pages'][0] - 1]) and in_order(passage['title'], s.text[after:after + 300]), letter
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
            # A printed 3-mark partial (“= 3 mharc”, or A 3(b)'s “… is fiú 3 mharc an freagra.”) allows 0/3/5.
            permitted = [0, 3, 5] if (two or '= 3 mharc' in chunk or 'is fiú 3 mharc' in chunk) else [0, 5]
            resolved.append((q, part, prompt, chunk, spages, two, permitted))
        passage['resolved'] = resolved
    # The literature note is printed twice (below 2A on PDF 23 and below 3A on PDF 27), word for word.
    lit_note = s.chunk('Nóta: Níl sé i gceist a chur in iúl go bhfuil na freagraí thuasluaite', 'Níl cead aon ábhar a bhaineann le Prós Ainmnithe')[0]
    assert lit_note.endswith('de réir a bhfiúntais.'), lit_note[-60:]
    assert s.chunk('Nóta: Níl sé i gceist a chur in iúl go bhfuil na freagraí thuasluaite', 'Níl cead aon ábhar a bhaineann le Filíocht Ainmnithe',
                   s.text.index('⟦27⟧'))[0] == lit_note
    # Cáca Milis, An Lasair Choille, Hurlamaboc, the 2B film, the 2B play and 2B(b): with a full stop; both 3A poems, 3B(a), 3B(b): without.
    assert s.text.count(LANG_PROSE) == 6 and s.text.count(LANG_POETRY) == 4, (s.text.count(LANG_PROSE), s.text.count(LANG_POETRY))
    assert in_order(FILM_OR_PLAY, texts[7]) and in_order(FILM_OR_PLAY, s.text)
    for slug, atlas, title, topic, subs, start, end in PRESCRIBED_2A:
        assert in_order(title, texts[7]), slug
        for label, prompt, cut in subs:
            assert in_order(prompt, texts[7]), (slug, label)
    slug, atlas, letter, title, topic, prompt, start, end = HURLAMABOC
    assert in_order(title, texts[7]) and in_order(prompt, texts[7]), slug
    for line in PROSE_2B_A_LINES + PROSE_2B_B[0]:
        assert in_order(line, texts[8]), line[:50]
    for slug, atlas, page, title, subs, start, end in POETRY_3A:
        assert in_order(title, texts[page - 1]), slug
        for label, prompt, marks, cut in subs:
            assert in_order(prompt.replace('\n', ' ') + f' ({marks} marc)', texts[page - 1]), (slug, label)
    for slug, atlas, prompts, start, end, cuts in POETRY_3B:
        for line in prompts + [TITLE_LINE]:
            assert in_order(line, texts[11]), (slug, line[:50])
    assert comparable(texts[11]).count(comparable(TITLE_LINE)) == 2
    for page, line in [(3, 'FREAGAIR GACH CEIST (1, 2 AGUS 3).'), (8, PROSE_CHOICE), (8, BOTH), (8, BOX_2A), (9, BOX_2B), (9, NO_PRESCRIBED_PROSE), (9, BOTH),
                       (9, OPTIONAL_FILM_OR_PLAY), (10, POETRY_CHOICE), (10, BOTH), (10, BOX_3A), (12, BOX_3B), (12, NO_PRESCRIBED_POETRY), (12, BOTH)]:
        assert comparable(line) in comparable(texts[page - 1]), (page, line)
    _MATERIAL = dict(paper=paper, texts=texts, s=s, lang_read=lang_read, lit_note=lit_note, decisions=selection_decisions(paper))
    return _MATERIAL


def deduction(lang):
    return criterion('gaeilge-deduction', 'Gaeilge lochtach', 4, [lang], 'quality', deduction=True)


def reading_note(m):
    return 'Scheme: “' + m['lang_read'] + '” — one deduction from each passage total (50), never inside a single part.'


def source(label, title, pages):
    return dict(kind='source-text', label=label, title=title, pages=pages, attribution=ATTRIBUTION, presentationNote=SOURCE_NOTE)


def sub_permitted(piece, marks):
    """“3 mharc + 2 mharc”: first correct point 3, second 2 (0/3/5); other sub-questions keep the full range."""
    return [0, 3, 5] if (marks == 5 and '3 mharc + 2 mharc' in piece) else None


def prescribed_pieces(m, slug, subs, start, end):
    whole, spages = m['s'].chunk(start, end)
    assert LANG_PROSE in whole, slug
    whole = before_language_note(whole)
    pieces = split_at(whole, [cut for _, _, cut in subs], slug)
    for (label, _, _), piece in zip(subs, pieces):
        assert '(5 mharc)' in piece, (slug, label)
    return pieces, spages


def poem_pieces(m, slug, subs, start, end):
    whole, spages = m['s'].chunk(start, end)
    assert LANG_POETRY in whole, slug
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


WHOLE_PROSE_NOTE = ('One complete SEC response: five points at 5 (2 for the bare point + 3 for development); the 0–4 Gaeilge deduction applies once '
                    'to this whole 25-mark answer. The sample points are indicative rather than exhaustive.')
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

    note = m['lit_note']
    sub_note = 'One printed sub-question at its published tariff. ' + LIT_DEDUCTION_NOTE
    question_lit = []
    # ---- Ceist 2A: (a) Cáca Milis or An Lasair Choille (a card each, five sub-questions), (b) Hurlamaboc ---------
    prescribed_parts = {}
    for slug, atlas, title, topic, subs, start, end in PRESCRIBED_2A:
        pieces, spages = prescribed_pieces(m, slug, subs, start, end)
        prescribed_parts[slug] = (pieces, spages)
        add(atlas, slug, f'Prós 2A(a) · {title}', f'(a) {FILM_OR_PLAY}\n{title}\n' + '\n'.join(f'({l}) {p}' for l, p, _ in subs) + '\n(25 marc)',
            topic, [8], spages,
            [criterion(f'eolas-{label}', f'({label}) Eolas', 5, [piece, note], 'indicative', permitted=sub_permitted(piece, 5))
             for (label, _, _), piece in zip(subs, pieces)] + [deduction(LANG_PROSE)], [PROSE_CHOICE, BOTH, FILM_OR_PLAY] + LIT,
            'One complete SEC response: five printed sub-questions at 5 each, then the 0–4 Gaeilge deduction once. '
            'The sample answers are indicative rather than exhaustive.', source('Prós Ainmnithe', title, [8]),
            concept=f'irish-prose-2a-{topic}', stem=BOX_2A)
        question_lit.append(cards[-1]['id'])
    slug_h, atlas_h, letter_h, title_h, topic_h, prompt_h, start_h, end_h = HURLAMABOC
    chunk, hpages = m['s'].chunk(start_h, end_h)
    assert '5 phointe eolais agus 5 mharc ar gach pointe eolais' in chunk and LANG_PROSE in chunk
    add(atlas_h, slug_h, 'Prose 2A(b)', f'({letter_h}) {title_h}\n{prompt_h}\n(25 marc)', topic_h, [8], hpages,
        [criterion('eolas', 'Eolas', 25, [before_language_note(chunk), note], 'indicative'), deduction(LANG_PROSE)], [PROSE_CHOICE, BOTH] + LIT[1:],
        WHOLE_PROSE_NOTE, source('Prós Ainmnithe', title_h, [8]), concept=f'irish-prose-2a-{topic_h}', stem=BOX_2A)
    question_lit.append(cards[-1]['id'])

    # ---- Ceist 2B: Prós Roghnach (a) the optional film or play, (b) the optional novel extract ------------------
    film, fpages = m['s'].chunk('Maidir le scannán roghnach a ndearna tú', 'NÓ Maidir le dráma roghnach')
    play, ppages = m['s'].chunk('Maidir le dráma roghnach a ndearna tú', '(b) Maidir le giota as úrscéal roghnach')
    assert LANG_PROSE in film and LANG_PROSE in play
    alternatives = []
    for alt in (before_language_note(film), before_language_note(play)):
        cuts = [0] + [alt.index(cut) for _, _, _, cut in PROSE_2B_A_PARTS[1:]]
        bits = [alt[a:b].strip() for a, b in zip(cuts, cuts[1:] + [len(alt)])]
        assert bits[0].endswith('= 1 mharc') and '= 22 marc' in bits[1] and '(23 marc)' in bits[1] and bits[2].endswith('(2 mharc)'), bits
        alternatives.append(bits)
    # The character line is printed word for word under the film and under the play: lifted once, without the question it
    # follows (the card's question), so the 1-mark criterion reads its own price and not the question's “(25 marc)”.
    character = [bits[0][bits[0].index('An phearsa (an carachtar) is mó a thaitníonn leat'):] for bits in alternatives]
    assert character[0] == character[1] == 'An phearsa (an carachtar) is mó a thaitníonn leat = 1 mharc', character
    guidance = [[character[0]]] + [[alternatives[0][i], alternatives[1][i]] for i in (1, 2)]
    crits = [criterion(cid, label, marks, guidance[i], 'exact' if cid == 'teideal' else 'indicative',
                       permitted=None if cid == 'eolas' else sorted({0, marks} | {int(v) for v in re.findall(r'= (\d) mharc', guidance[i][0])}))
             for i, (cid, label, marks, _) in enumerate(PROSE_2B_A_PARTS)]
    add('P-2B-a', 'prose-2b-a', 'Prose 2B(a)', '\n'.join(PROSE_2B_A_LINES), 'irish-4-7', [9], sorted(set(fpages) | set(ppages)),
        crits + [deduction(LANG_PROSE)], [PROSE_CHOICE, NO_PRESCRIBED_PROSE, BOTH, OPTIONAL_FILM_OR_PLAY] + LIT[1:],
        'One complete SEC response about an optional film or an optional play (the same scheme for both): the most-liked character 1, '
        '22 for the main events in five points (5, 5, 4, 4, 4) and 2 for the exact title and writer, then the 0–4 Gaeilge deduction once. '
        'The text is open content chosen by the candidate (indicative rather than exhaustive).',
        source('Prós Roghnach', 'Scannán nó dráma roghnach', [9]), concept='irish-prose-2b-irish-4-7', stem=STEM_2B)
    question_lit.append(cards[-1]['id'])
    lines2, start2, end2, parts = PROSE_2B_B
    chunk2, spages2 = m['s'].chunk(start2, end2)
    assert LANG_PROSE in chunk2
    chunk2 = before_language_note(chunk2)
    cuts = [0] + [chunk2.index(cut) for _, _, _, cut in parts[1:]]
    bits = [chunk2[a:b].strip() for a, b in zip(cuts, cuts[1:] + [len(chunk2)])]
    crits = [criterion(cid, label, marks, [bit], 'exact' if cid == 'teideal' else 'indicative',
                       permitted=None if cid == 'eolas' else sorted({0, marks} | {int(v) for v in re.findall(r'= (\d) mharc', bit)}))
             for (cid, label, marks, _), bit in zip(parts, bits)]
    assert bits[0].endswith('Príomhthéama an ghiota = 3 mharc') and bits[1].startswith('4 phointe eolais ag teastáil (5 mharc an ceann) = 20 marc'), bits[:2]
    assert crits[-1]['guidance'][0].endswith('(2 mharc)'), crits[-1]['guidance'][0][-60:]
    add('P-2B-b', 'prose-2b-b', 'Prose 2B(b)', '\n'.join(lines2), 'irish-4-7', [9], spages2, crits + [deduction(LANG_PROSE)],
        [PROSE_CHOICE, NO_PRESCRIBED_PROSE, BOTH] + LIT[1:],
        'One complete SEC response: ' + ', '.join(f'{label} {marks}' for _, label, marks, _ in parts) +
        ', then the 0–4 Gaeilge deduction once. The optional text is open content chosen by the candidate; the scheme prints no sample '
        'points for it, so its points are judged on merit against these allocations (indicative rather than exhaustive).',
        source('Prós Roghnach', 'Giota as úrscéal roghnach', [9]), concept='irish-prose-2b-irish-4-7', stem=STEM_2B)
    question_lit.append(cards[-1]['id'])

    # ---- Ceist 3A: Colscaradh and An tEarrach Thiar ----------------------------------------------------
    poem_parts = {}
    for slug3, atlas3, page, title3, subs3, start3, end3 in POETRY_3A:
        pieces3, spages3 = poem_pieces(m, slug3, subs3, start3, end3)
        poem_parts[slug3] = (pieces3, spages3)
        crits = [criterion(f'eolas-{label}', f'({label}) Eolas', marks, [piece, note], 'indicative', permitted=SLOT_PERMITTED.get((slug3, label)))
                 for (label, _, marks, _), piece in zip(subs3, pieces3)]
        prompt = '\n'.join(f'({label}) {p}' + f' ({marks} marc)' for label, p, marks, _ in subs3)
        add(atlas3, slug3, f'Poetry 3A({atlas3[-1]})', f'({atlas3[-1]}) {title3}\n' + prompt, POEM_TOPICS[slug3], [page], spages3, crits + [deduction(LANG_POETRY)],
            [POETRY_CHOICE, BOTH] + LIT,
            'One complete SEC response: ' + ', '.join(f'({label}) {marks}' for label, _, marks, _ in subs3) +
            ' at their printed tariffs, then the 0–4 Gaeilge deduction once. The sample points are indicative rather than exhaustive; '
            f'{LIFTED_LINES[slug3]}.',
            source('Filíocht Ainmnithe', title3, [page]), concept=f'irish-poetry-3a-{POEM_TOPICS[slug3]}', stem=BOX_3A)
        question_lit.append(cards[-1]['id'])

    # ---- Ceist 3B: Filíocht Roghnach (a) and (b) --------------------------------------------------------
    for slug4, atlas4, prompts, start4, end4, cuts4 in POETRY_3B:
        chunk4, spages4 = m['s'].chunk(start4, end4, m['s'].text.index('⟦27⟧'))
        assert LANG_POETRY in chunk4, slug4
        chunk4 = before_language_note(chunk4)
        idx = [0] + [chunk4.index(cut) for cut in cuts4]
        bits = [chunk4[a:b].strip() for a, b in zip(idx, idx[1:] + [len(chunk4)])]
        for bit, cap in zip(bits, ['(9 marc)', '(7 marc)', '(7 marc)', '(2 mharc)']):
            assert cap in bit, (slug4, cap)
        crits = [criterion('eolas-i', '(i) Eolas', 9, [bits[0]], 'indicative'), criterion('eolas-ii', '(ii) Eolas', 7, [bits[1]], 'indicative'),
                 criterion('eolas-iii', '(iii) Eolas', 7, [bits[2]], 'indicative'),
                 criterion('teideal', 'Teideal + ainm an fhile', 2, [bits[3]], 'exact', permitted=[0, 1, 2])]
        add(atlas4, slug4, f'Poetry 3B({atlas4[-1]})', f'({atlas4[-1]}) ' + '\n'.join(prompts + [TITLE_LINE]), 'irish-5-6', [12], spages4,
            crits + [deduction(LANG_POETRY)], [POETRY_CHOICE, NO_PRESCRIBED_POETRY, BOTH] + LIT,
            'One complete SEC response: (i) 9, (ii) 7, (iii) 7, poem and poet 2, then the 0–4 Gaeilge deduction once. '
            'The optional poem is open content; 3B(b) asks for a modern poem not used in 3B(a). The printed allocations are judged on merit '
            '(indicative rather than exhaustive).',
            source('Filíocht Roghnach', f'3B({atlas4[-1]}) · Dán roghnach', [12]),
            concept='irish-poetry-3b-irish-5-6', stem=STEM_3B)
        question_lit.append(cards[-1]['id'])

    # ---- Practice: every 2A(a) sub-question, every prescribed-poetry sub-question and the printed questions inside ----
    for slug, atlas, title, topic, subs, start, end in PRESCRIBED_2A:
        pieces, spages = prescribed_parts[slug]
        src = source('Prós Ainmnithe', title, [8])
        for (label, prompt, _), piece in zip(subs, pieces):
            # The paper prints no per-sub-question tariff for 2A(a); the scheme prices each at (5 mharc).
            add(f'{atlas}-{label}', f'{slug}-{label}', f'Prós 2A(a) · {title} · ({label})', f'(a) {FILM_OR_PLAY}\n{title}\n({label}) {prompt}',
                topic, [8], spages, [criterion('eolas', 'Eolas', 5, [piece, note], 'indicative', permitted=sub_permitted(piece, 5))],
                [PROSE_CHOICE, BOTH, FILM_OR_PLAY] + LIT[1:], sub_note, src, stem=BOX_2A)
            practice_ids.append(cards[-1]['id'])
    for slug3, atlas3, page, title3, subs3, start3, end3 in POETRY_3A:
        pieces3, spages3 = poem_parts[slug3]
        topic3 = POEM_TOPICS[slug3]
        src3 = source('Filíocht Ainmnithe', title3, [page])
        head = f'({atlas3[-1]}) {title3}\n'
        for (label, prompt, marks, _), piece in zip(subs3, pieces3):
            slots = SLOTS_3A.get((slug3, label))
            add(f'{atlas3}-{label}', f'{slug3}-{label}', f'Filíocht 3A({atlas3[-1]}) · {title3} · ({label})', head + f'({label}) {prompt} ({marks} marc)',
                topic3, [page], spages3,
                [criterion('eolas', 'Eolas', marks, [piece, note], 'indicative', permitted=SLOT_PERMITTED.get((slug3, label)))],
                [POETRY_CHOICE, BOTH] + LIT[1:], sub_note, src3, stem=BOX_3A)
            practice_ids.append(cards[-1]['id'])
            if slots:
                printed = dict(re.findall(r'\(([a-d])\) ([^\n]+)', prompt))
                for (sub, slot), (_, _, smarks, caption, _) in zip(slot_pieces(piece, slots), slots):
                    add(f'{atlas3}-{label}-{sub}', f'{slug3}-{label}-{sub}', f'Filíocht 3A({atlas3[-1]}) · {title3} · ({label})({sub})',
                        head + f'({label}) ({sub}) {printed[sub]}', topic3, [page], spages3,
                        [criterion('eolas', 'Freagra', smarks, [slot], 'indicative',
                                   permitted=list(range(0, smarks + 1, 2)) if smarks in (2, 4) else None)], [POETRY_CHOICE, BOTH] + LIT[1:],
                        f'One printed question inside 3A({atlas3[-1]})({label}), at its printed {caption}. ' + LIT_DEDUCTION_NOTE, src3, stem=BOX_3A)
                    practice_ids.append(cards[-1]['id'])

    assert len(whole_ids) == 10 and len(question_lit) == 9 and len(practice_ids) == 41, (len(whole_ids), len(question_lit), len(practice_ids))
    assert len(cards) == 60 and len({c['id'] for c in cards}) == 60 and len({c['atlasQuestionId'] for c in cards}) == 60
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
                                'to be answered; 2A(a)’s two prescribed texts (Cáca Milis, An Lasair Choille) are a card each and 2B(a)’s optional film or '
                                'play is one card; every printed question is one card carrying the printed choice and “Freagair (a) agus (b) anseo.”; '
                                'no combination cards.'),
                  boundaries=('10 whole reading questions with their 20 published parts; 9 literature questions; the 5 printed sub-questions of each '
                              '2A(a) text, the 6 prescribed-poetry sub-questions, the 2 printed questions inside 3A(a)(iii) and the 3 inside 3A(b)(i).'))
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
    print(f"Irish Ordinary {YEAR} Paper 2: {len(data['cards'])} reviewed cards (19 printed questions, 41 practice parts); the archive remains incomplete.")


if __name__ == '__main__':
    main()
