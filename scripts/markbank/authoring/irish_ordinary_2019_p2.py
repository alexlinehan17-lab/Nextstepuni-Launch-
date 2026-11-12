#!/usr/bin/env python3
"""Reviewed 2019 Ordinary Paper 2 (Léamhthuiscint agus Litríocht), carded new.

Paper PDF 1–12 and the Paper 2 pages of the combined LC001GLP000IV scheme (PDF 13–30,
plus 31 modified marking) reviewed on 2026-11-04. Counts are assertions, not
corpus-completeness proof. Same method as irish_ordinary_2020_p2.py.

No 2019 Ordinary card existed before. `build` cards the component the way the reviewed
2020–2025 Ordinary Paper 2s are carded: the ten whole reading questions (each part its
own 5-mark criterion), the nine literature questions (each printed sub-question its own
criterion, the 0–4 Gaeilge deduction once), and the practice cards beside them: every
reading part (20), the five printed sub-questions of 2A(a) Hurlamaboc and every
prescribed-poetry sub-question (6).

2019's layout: “FREAGAIR GACH CEIST (1, 2 AGUS 3).” Ceist 1 is Léamhthuiscint A and B
(both); Ceist 2 is A (Prós Ainmnithe) or B (Prós Roghnach) and Ceist 3 is A (Filíocht
Ainmnithe) or B (Filíocht Roghnach), each section printing two questions, (a) and (b),
both to be answered (“Freagair (a) agus (b) anseo.”). 2A(b) is the prescribed film
Cáca Milis or the prescribed play An Lasair Choille: they file under different Atlas
headings, so each is its own card; 2B(b) is an optional film or an optional play under one
heading with one scheme, so one card carries both printed alternatives (the 2026-10-12
decision, commit 7da1a0819). Each literature card carries the printed choice and
“Freagair (a) agus (b) anseo.” as its task check (choice is not a route; no card combines
two questions), and the section's printed box heading (“A – PRÓS AINMNITHE – (50 marc)” …)
with, for B, the printed restriction as its lead-in.

The scheme's text layer stores each page's boxed heading (“CEIST 1 (A + B) ‐
LÉAMHTHUISCINT ‐ 100 marc”, “B– (50 marc)” …) with the page body; `Scheme` removes
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
YEAR = 2019
FILE = 'LC001GLP200IV'
SCHEME_FILE = 'LC001GLP000IV'
OUT = ROOT / 'components/MarkBank/cards/irish/ordinary-2019-p2-authored.json'
SOURCE_REVIEW = ROOT / 'scripts/markbank/authored/irish-ordinary-2019-p2-source-review.json'
REVIEWED_AT = '2026-11-04'
PAPER_SHA = '030c3571373b988601f1af06e4765f85efd815a06d13f4a41c9002d20f976b3f'
SCHEME_SHA = 'a7017d809af34bbb4b44f9a6f990046d0b4d3698df47683eaeda5fdcc061eeb6'
DIRECTIVE = re.compile(r'rogha|roghna|Freagair|Luaigh|Ainmnigh|\bnó\b|dhá phointe|dhá rud|dhá bh|dhá dh|dhá ch|dhá fh|dhá th|dhá ph|dhá sh|'
                       r'\ban dá\b|ceann amháin|pointe amháin|amháin|\bdhá\b', re.I)
SOURCE_NOTE = 'Shown page-for-page from the official examination paper; swipe to move between pages.'
ATTRIBUTION = '© State Examinations Commission.'
# Boxed page headings the 2019 scheme's text layer stores with the page body (exact strings, each printed once).
FURNITURE = ('CEIST 1 (A + B) ‐ LÉAMHTHUISCINT ‐ 100 marc', 'A – (50 marc)', 'B– (50 marc)',
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


# (q, part, paper prompt, scheme anchor)
PASSAGES = {
    'A': dict(title='Micheál D. Ó hUiginn', pages=[4, 5], topic='irish-3-0', start='⟦13⟧', notes_end='1. (a) Scríobh síos dhá chumhacht',
              end='Nóta: Gearrfar pionós i ngeall ar iomarcaíocht. Léireofar', parts=[
        ('1', 'a', '(a) Scríobh síos dhá chumhacht atá ag Uachtarán na hÉireann. (Alt 1)', '1. (a) Scríobh síos dhá chumhacht'),
        ('1', 'b', '(b) Cén bua mór a bhí ag Micheál D. Ó hUiginn i dtoghchán na hUachtaránachta i mí Dheireadh Fómhair 2018? (Alt 1)', '(b) Cén bua mór a bhí ag Micheál'),
        ('2', 'a', '(a) Scríobh síos dhá phíosa eolais faoi Mhicheál D. Ó hUiginn mar Aire Ealaíon, Cultúir agus Gaeltachta. (Alt 2)', '2. (a) Scríobh síos dhá phíosa eolais faoi Mhicheál'),
        ('2', 'b', '(b) Conas a thuill Micheál D. Ó hUiginn cáil in Éirinn agus ar fud an domhain? (Alt 2)', '(b) Conas a thuill Micheál'),
        ('3', 'a', '(a) Scríobh síos dhá chúis a bhfuil na cuairteanna stáit agus na cuairteanna oifigiúla a dhéanann an tUachtarán thar lear tábhachtach. (Alt 3)',
         '3. (a) Scríobh síos dhá chúis a bhfuil na cuairteanna'),
        ('3', 'b', '(b) Cén fáth a molann an tUachtarán Ó hUiginn ‘Taispeántas an Eolaí Óig agus na Teicneolaíochta’? (Alt 3)', '(b) Cén fáth a molann an tUachtarán'),
        ('4', 'a', '(a) Luaigh dhá rud a chreideann an tUachtarán Ó hUiginn faoi na laochra spóirt. (Alt 4)', '4. (a) Luaigh dhá rud a chreideann'),
        ('4', 'b', '(b) Cén fáth a n‐eagraíonn an tUachtarán cóisirí gairdín gach bliain? (Alt 4)', '(b) Cén fáth a n‐eagraíonn'),
        ('5', 'a', '(a) Cén fhís atá ag an Uachtarán Ó hUiginn d’Éirinn sna seacht mbliana atá romhainn amach? (Alt 5)', '5. (a) Cén fhís atá ag an Uachtarán'),
        ('5', 'b', '(b) Cén rud is mó a ghoilleann ar an Uachtarán Ó hUiginn faoi láthair? (Alt 5)', '(b) Cén rud is mó a ghoilleann')]),
    'B': dict(title='Oireachtas na Samhna ‐ Príomhfhéile na nGael', pages=[6, 7], topic='irish-3-1', start='⟦16⟧',
              notes_end='1. (a) Tabhair dhá phíosa eolais faoi chéadfhéile', end='Nóta: Gearrfar pionós i ngeall ar iomarcaíocht. Léireofar', parts=[
        ('1', 'a', '(a) Tabhair dhá phíosa eolais faoi chéadfhéile an Oireachtais sa bhliain 1897. (Alt 1)', '1. (a) Tabhair dhá phíosa eolais faoi chéadfhéile'),
        ('1', 'b', '(b) Scríobh síos an dá chúis a dtagann pobal na Gaeilge le chéile ag Oireachtas na Samhna. (Alt 1)', '(b) Scríobh síos an dá chúis a dtagann'),
        ('2', 'a', '(a) Luaigh dhá phíosa eolais faoi chomórtas Chorn Uí Riada. (Alt 2)', '2. (a) Luaigh dhá phíosa eolais faoi chomórtas'),
        ('2', 'b', '(b) Cén fáth a bhfuil na comórtais liteartha tábhachtach? (Alt 2)', '(b) Cén fáth a bhfuil na comórtais liteartha'),
        ('3', 'a', '(a) Scríobh síos dhá rud a dhéanann Helen Ní Shé mar láithreoir ar an irischlár, An Saol ó Dheas. (Alt 3)', '3. (a) Scríobh síos dhá rud a dhéanann Helen'),
        ('3', 'b', '(b) Cén obair a dhéanann Caitlín Nic Aoidh ar TG4? (Alt 3)', '(b) Cén obair a dhéanann Caitlín'),
        ('4', 'a', '(a) Scríobh síos dhá rud faoin turas farraige a rinne an cúigear fear sa tsraith theilifíse, Camino an tSáile. (Alt 4)',
         '4. (a) Scríobh síos dhá rud faoin turas farraige'),
        ('4', 'b', '(b) Tabhair dhá phíosa eolais faoin scannán Song of Granite. (Alt 4)', '(b) Tabhair dhá phíosa eolais faoin scannán Song'),
        ('5', 'a', '(a) Cén fáth a mbíonn RTÉ Raidió na Gaeltachta, TG4 agus meáin Ghaeilge eile i láthair ag Oireachtas na Samhna? (Alt 5)', '5. (a) Cén fáth a mbíonn RTÉ'),
        ('5', 'b', '(b) Cad a chuireann an aip de chuid TG4, MOLSCÉAL, ar fáil? (Alt 5)', '(b) Cad a chuireann an aip')]),
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

# 2A(a) Hurlamaboc: printed sub-questions at 5 each (the paper prints only the question's (25 marc)).
HURLAMABOC = ('prose-2a-a', 'P-2A-a', 'a', 'Hurlamaboc', 'irish-4-5', 'Freagair na ceisteanna thíos faoin ngiota as an úrscéal Hurlamaboc.', [
    ('i', 'Scríobh síos dhá rud faoi Ruán, mac Lisín.', '(i) Scríobh síos dhá rud faoi Ruán'),
    ('ii', 'Tabhair dhá phointe eolais faoi na hullmhúcháin atá déanta ag Lisín don chóisir.', '(ii) Tabhair dhá phointe eolais faoi na hullmhúcháin'),
    ('iii', 'Scríobh síos dhá shlí a ndearna Pól a chuid airgid.', '(iii) Scríobh síos dhá shlí'),
    ('iv', 'Luaigh dhá phointe eolais faoi na mná eile ar Ascaill na Fuinseoige.', '(iv) Luaigh dhá phointe eolais faoi na mná eile'),
    ('v', '‘Bhí Lisín gnóthach, ina ball de mhórán eagraíochtaí agus clubanna.’ Scríobh síos dhá phointe eolais faoin gcuid sin de shaol Lisín.',
     '(v) ‘Bhí Lisín gnóthach')],
    '(a) Hurlamaboc Freagair na ceisteanna thíos', '(b) Cáca Milis (25 marc)')
# 2A(b): the prescribed film or the prescribed play, a card each: (slug, atlas, title, topic, printed question lines, scheme start, scheme end)
FILM_PLAY_2A = [
    ('prose-2a-b-caca-milis', 'P-2A-b-caca-milis', 'Cáca Milis', 'irish-4-6',
     ['Tá Catherine ina suí sa charráiste traenach nuair a shuíonn an fear dall, Paul, os a comhair amach sa scannán Cáca Milis.',
      'Tabhair cuntas ar na rudaí a tharlaíonn ón uair a shuíonn Paul os comhair Catherine go dtí deireadh an scannáin.'],
     '(b) Cáca Milis (25 marc)', 'NÓ An Lasair Choille'),
    ('prose-2a-b-an-lasair-choille', 'P-2A-b-an-lasair-choille', 'An Lasair Choille', 'irish-4-8',
     ['Tá dhá bhliain déag caite ag Séamas ag tabhairt aire do Mhicil, an seanfhear, sa dráma An Lasair Choille.',
      'Tabhair cuntas ar an gcineál saoil atá ag Séamas agus é ag tabhairt aire do Mhicil.'],
     'An Lasair Choille Tá dhá bhliain déag', 'Níl cead aon ábhar a bhaineann le Prós Ainmnithe'),
]
# 2B(a): (paper lines, scheme start, scheme end, [(id, label, marks, cut-before)])
PROSE_2B_A = (['(a) Maidir le giota as úrscéal roghnach a ndearna tú staidéar air le linn do chúrsa, ainmnigh an phearsa (an carachtar) is tábhachtaí sa ghiota. '
               'Tabhair cuntas ar na heachtraí is mó a tharlaíonn don duine sin sa ghiota. (23 marc)',
               'Ní mór teideal an úrscéil sin, mar aon le hainm an údair, a scríobh síos go cruinn. (2 mharc)'],
              '(a) Maidir le giota as úrscéal roghnach', '(b) Maidir le scannán roghnach',
              [('priomhphearsa', 'An phearsa is tábhachtaí a lua', 1, None), ('eolas', 'Na heachtraí is mó', 22, 'Na heachtraí is mó a tharlaíonn'),
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
    ('poetry-3a-a', 'F-3A-a', 10, 'An Spailpín Fánach', [
        ('i', 'Déan cur síos, i d’fhocail féin, ar an íomhá (ar an bpictiúr) den spailpín a thugann an file dúinn i véarsa a haon, línte 1‐4, den dán seo. (Is leor dhá phointe eolais.)', 8,
         '(i) Déan cur síos, i d’fhocail féin, ar an íomhá'),
        ('ii', 'Tabhair dhá phointe eolais, i d’fhocail féin, faoin spailpín agus é ‘ar mhargadh na saoire’ i véarsa a trí.', 8,
         '(ii) Tabhair dhá phointe eolais, i d’fhocail féin, faoin spailpín'),
        ('iii', 'An bhfuil trua agat don spailpín sa dán seo? Cuir fáthanna le do fhreagra. (Is leor dhá fháth.)', 9, '(iii) An bhfuil trua agat')],
     '(a) An Spailpín Fánach (25 marc)', '(b) Colscaradh (i)'),
    ('poetry-3a-b', 'F-3A-b', 11, 'Colscaradh', [
        ('i', 'Inis i d’fhocail féin, cén saghas duine é an fear sa dán. (Is leor dhá phointe eolais.)', 8, '(i) Inis i d’fhocail féin'),
        ('ii', 'Scríobh síos, i d’fhocail féin, na príomhsmaointe atá i véarsa a dó. (Is leor dhá phointe eolais.)', 8, '(ii) Scríobh síos, i d’fhocail féin, na príomhsmaointe'),
        ('iii', 'An maith leat an dán seo? Cuir fáthanna le do fhreagra. (Is leor dhá fháth.)', 9, '(iii) An maith leat an dán seo?')],
     '(b) Colscaradh (i)', 'Níl cead aon ábhar a bhaineann le Filíocht Ainmnithe'),
]
POEM_TOPICS = {'poetry-3a-a': 'irish-5-1', 'poetry-3a-b': 'irish-5-5'}
POETRY_3B = [
    ('poetry-3b-a', 'F-3B-a', [
        '(i) Maidir le dán seanaimseartha roghnach (dán a cumadh sa tréimhse roimh 1850) a ndearna tú staidéar air le linn do chúrsa, scríobh síos i d’fhocail féin, príomhsmaointe an dáin. (9 marc)',
        '(ii) Cén íomhá (pictiúr) is mó a thaitníonn leat sa dán? Mínigh an íomhá (an pictiúr) sin, i d’fhocail féin. (Is leor dhá phointe eolais.) (7 marc)',
        '(iii) Scríobh síos an mothúchán is láidre sa dán, dar leat. Tabhair dhá shampla den mhothúchán sin sa dán. (7 marc)'],
     '(a) (i) Maidir le dán seanaimseartha', '(b) (i) Maidir le dán nua‐aimseartha', ['(ii) Cén íomhá', '(iii) Scríobh síos an mothúchán', 'Ní mór teideal an dáin']),
    ('poetry-3b-b', 'F-3B-b', [
        '(i) Maidir le dán nua‐aimseartha roghnach a ndearna tú staidéar air le linn do chúrsa, scríobh síos príomhthéama an dáin sin, dar leat. '
        'Tabhair dhá phointe eolais, i d’fhocail féin, faoin bpríomhthéama sin sa dán. (9 marc)',
        '(ii) Cén t‐atmaisféar atá sa dán seo, dar leat? Tabhair dhá shampla den atmaisféar sin sa dán. (7 marc)',
        '(iii) An maith leat an dán seo? Cuir fáthanna le do fhreagra. (Is leor dhá fháth.) (7 marc)'],
     '(b) (i) Maidir le dán nua‐aimseartha', None, ['(ii) Cén t‐atmaisféar', '(iii) An maith leat', 'Ní mór teideal an dáin']),
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
    s = Scheme(doc, 13, 30)
    assert s.removed == len(FURNITURE), s.removed
    assert not PUA.search(s.text), 'private-use glyph left in the scheme text'
    lang_read = '[Gaeilge lochtach: 0 ‐ 5 a bhaint den iomlán a gnóthaíodh]'
    assert s.text.count(lang_read) == 2
    for letter, passage in PASSAGES.items():
        page_text = ' '.join(texts[p - 1] for p in passage['pages'])
        assert in_order(passage['title'], page_text), letter
        after = s.text.index(passage['start'])
        # Each passage prints one note above Ceist 1 (2019 prints the iomarcaíocht note only after Ceist 5(b)).
        notes = s.chunk('Nóta: Má tá dhá phointe eolais i gceist', passage['notes_end'], after)[0]
        assert notes == ('Nóta: Má tá dhá phointe eolais i gceist, tá 3 mharc ar an gcéad cheann atá ceart agus 2 mharc ar an '
                         'dara ceann atá ceart.'), notes
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
            two = '3 mharc + 2 mharc' in chunk or '= 2 mharc' in chunk
            permitted = [0, 3, 5] if (two or '= 3 mharc' in chunk) else [0, 5]
            resolved.append((q, part, prompt, chunk, spages, two, permitted))
        passage['resolved'] = resolved
    # The literature note is printed twice (above 2A on PDF 19 and above 3A on PDF 26), word for word.
    lit_note = s.chunk('Nóta: Níl sé i gceist a chur in iúl go bhfuil na freagraí samplacha', 'Freagair (a) agus (b) anseo.')[0]
    assert s.chunk('Nóta: Níl sé i gceist a chur in iúl go bhfuil na freagraí samplacha', 'Freagair (a) agus (b) anseo.',
                   s.text.index('⟦26⟧'))[0] == lit_note
    lang_lit = '[Gaeilge lochtach: 0‐4 a bhaint den iomlán a gnóthaíodh]'
    # Hurlamaboc, An Lasair Choille, 2B(a), the 2B film and play, both 3A poems, 3B(a), 3B(b); Cáca Milis prints it with a closing full stop.
    assert s.text.count(lang_lit) == 9 and s.text.count(lang_lit[:-1] + '.]') == 1, s.text.count(lang_lit)
    slug, atlas, letter, title, topic, intro, subs, start, end = HURLAMABOC
    for line in [intro, title] + [p for _, p, _ in subs]:
        assert in_order(line, texts[7]), (slug, line[:40])
    for line in [FILM_OR_PLAY] + [x for item in FILM_PLAY_2A for x in [item[2]] + item[4]]:
        assert in_order(line, texts[7]), line[:50]
    for line in PROSE_2B_A[0] + PROSE_2B_B_LINES:
        assert in_order(line, texts[8]), line[:50]
    for slug3, atlas3, page, title3, subs3, start3, end3 in POETRY_3A:
        assert in_order(title3, texts[page - 1]), slug3
        for label, prompt, marks, cut in subs3:
            assert in_order(prompt + f' ({marks} marc)', texts[page - 1]), (slug3, label)
    for slug4, atlas4, prompts, start4, end4, cuts4 in POETRY_3B:
        for line in prompts + [TITLE_LINE]:
            assert in_order(line, texts[11]), (slug4, line[:50])
    assert comparable(texts[11]).count(comparable(TITLE_LINE)) == 2
    for page, line in [(3, 'FREAGAIR GACH CEIST (1, 2 AGUS 3).'), (8, PROSE_CHOICE), (8, BOTH), (8, BOX_2A), (8, FILM_OR_PLAY), (9, BOX_2B),
                       (9, NO_PRESCRIBED_PROSE), (9, BOTH), (9, OPTIONAL_FILM_OR_PLAY), (10, POETRY_CHOICE), (10, BOTH), (10, BOX_3A), (12, BOX_3B),
                       (12, NO_PRESCRIBED_POETRY), (12, BOTH)]:
        assert comparable(line) in comparable(texts[page - 1]), (page, line)
    _MATERIAL = dict(paper=paper, texts=texts, s=s, lang_read=lang_read, lit_note=lit_note, lang_lit=lang_lit,
                     decisions=selection_decisions(paper))
    return _MATERIAL


def deduction(m):
    return criterion('gaeilge-deduction', 'Gaeilge lochtach', 4, [m['lang_lit']], 'quality', deduction=True)


def reading_note(m):
    return 'Scheme: “' + m['lang_read'] + '” — one deduction from each passage total (50), never inside a single part.'


def source(label, title, pages):
    return dict(kind='source-text', label=label, title=title, pages=pages, attribution=ATTRIBUTION, presentationNote=SOURCE_NOTE)


def sub_permitted(piece, marks):
    """“3 mharc + 2 mharc”: first correct point 3, second 2 (0/3/5); other sub-questions keep the full range."""
    return [0, 3, 5] if (marks == 5 and '3 mharc + 2 mharc' in piece) else None


def hurlamaboc_pieces(m):
    slug, atlas, letter, title, topic, intro, subs, start, end = HURLAMABOC
    whole, spages = m['s'].chunk(start, end)
    whole = before_language_note(whole)
    pieces = split_at(whole, [cut for _, _, cut in subs], slug)
    for (label, _, _), piece in zip(subs, pieces):
        assert '(5 mharc)' in piece, (slug, label)
    return pieces, sorted(set(spages) | {19})


def poem_pieces(m, slug, subs, start, end):
    whole, spages = m['s'].chunk(start, end)
    whole = before_language_note(whole)
    pieces = split_at(whole, [cut for _, _, _, cut in subs], slug)
    for (label, _, marks, _), piece in zip(subs, pieces):
        assert f'({marks} marc)' in piece, (slug, label, piece[:60])
    return pieces, sorted(set(spages) | {26})


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

    note, lang = m['lit_note'], m['lang_lit']
    sub_note = 'One printed sub-question at its published tariff. ' + LIT_DEDUCTION_NOTE
    question_lit = []
    # ---- Ceist 2A: Hurlamaboc (five sub-questions), then Cáca Milis or An Lasair Choille -------------
    slug, atlas, letter, title, topic, intro, subs, start, end = HURLAMABOC
    pieces, spages = hurlamaboc_pieces(m)
    src = source('Prós Ainmnithe', title, [8])
    add(atlas, slug, 'Prose 2A(a)', f'({letter}) {title}\n{intro}\n' + '\n'.join(f'({l}) {p}' for l, p, _ in subs) + '\n(25 marc)',
        topic, [8], spages,
        [criterion(f'eolas-{label}', f'({label}) Eolas', 5, [piece, note], 'indicative', permitted=sub_permitted(piece, 5))
         for (label, _, _), piece in zip(subs, pieces)] + [deduction(m)], [PROSE_CHOICE, BOTH] + LIT,
        'One complete SEC response: five printed sub-questions at 5 each, then the 0–4 Gaeilge deduction once. '
        'The sample answers are indicative rather than exhaustive.', src, concept=f'irish-prose-2a-{topic}', stem=BOX_2A)
    question_lit.append(cards[-1]['id'])
    for slug_b, atlas_b, title_b, topic_b, lines_b, start_b, end_b in FILM_PLAY_2A:
        chunk, bpages = m['s'].chunk(start_b, end_b)
        assert '5 phointe eolais agus 5 mharc ar gach pointe eolais' in chunk, slug_b
        other = 'An Lasair Choille' if title_b == 'Cáca Milis' else 'Cáca Milis'
        add(atlas_b, slug_b, f'Prós 2A(b) · {title_b}', f'(b) {FILM_OR_PLAY}\n{title_b}\n' + '\n'.join(lines_b) + ' (25 marc)', topic_b, [8],
            sorted(set(bpages) | {19}),
            [criterion('eolas', 'Eolas', 25, [before_language_note(chunk), note], 'indicative'), deduction(m)], [PROSE_CHOICE, BOTH, FILM_OR_PLAY] + LIT[1:],
            WHOLE_PROSE_NOTE + f' 2A(b) offers Cáca Milis or An Lasair Choille; this card is {title_b} (the other printed question, {other}, is its own card).',
            source('Prós Ainmnithe', title_b, [8]), concept=f'irish-ol-p2-{slug_b}', stem=BOX_2A)
        question_lit.append(cards[-1]['id'])

    # ---- Ceist 2B: Prós Roghnach (a) the optional novel extract and (b) the optional film or play --------
    lines2, start2, end2, parts = PROSE_2B_A
    chunk2, spages2 = m['s'].chunk(start2, end2)
    chunk2 = before_language_note(chunk2)
    cuts = [0] + [chunk2.index(cut) for _, _, _, cut in parts[1:]]
    bits = [chunk2[a:b].strip() for a, b in zip(cuts, cuts[1:] + [len(chunk2)])]
    crits = [criterion(cid, label, marks, [bit], 'exact' if cid == 'teideal' else 'indicative',
                       permitted=None if cid == 'eolas' else sorted({0, marks} | {int(v) for v in re.findall(r'= (\d) mharc', bit)}))
             for (cid, label, marks, _), bit in zip(parts, bits)]
    assert crits[-1]['guidance'][0].endswith('(2 mharc)'), crits[-1]['guidance'][0][-60:]
    add('P-2B-a', 'prose-2b-a', 'Prose 2B(a)', '\n'.join(lines2), 'irish-4-7', [9], spages2, crits + [deduction(m)],
        [PROSE_CHOICE, NO_PRESCRIBED_PROSE, BOTH] + LIT[1:],
        'One complete SEC response: ' + ', '.join(f'{label} {marks}' for _, label, marks, _ in parts) +
        ', then the 0–4 Gaeilge deduction once. The optional text is open content chosen by the candidate; the scheme prints no sample '
        'points for it, so its points are judged on merit against these allocations (indicative rather than exhaustive).',
        source('Prós Roghnach', 'Giota as úrscéal roghnach', [9]), concept='irish-prose-2b-irish-4-7', stem=STEM_2B)
    question_lit.append(cards[-1]['id'])
    film, fpages = m['s'].chunk('(b) Maidir le scannán roghnach', 'NÓ Maidir le dráma roghnach')
    play, ppages = m['s'].chunk('Maidir le dráma roghnach', 'Freagair A (Filíocht Ainmnithe)')
    # Each alternative's key is its 23-mark allocation, then its printed title line (2 mharc), then the language note.
    film, play = before_language_note(film), before_language_note(play)
    film_eolas, film_title = film[:film.index('Ní mór teideal an scannáin')].strip(), film[film.index('Ní mór teideal an scannáin'):]
    play_eolas, play_title = play[:play.index('Ní mór teideal an dráma')].strip(), play[play.index('Ní mór teideal an dráma'):]
    for bit, cap in [(film_eolas, '(23 marc)'), (play_eolas, '(23 marc)'), (film_title, '(2 mharc)'), (play_title, '(2 mharc)')]:
        assert cap in bit, (cap, bit[-60:])
    add('P-2B-b', 'prose-2b-b', 'Prose 2B(b)', '\n'.join(PROSE_2B_B_LINES), 'irish-4-7', [9], sorted(set(fpages) | set(ppages)),
        [criterion('eolas', 'Príomhimeachtaí', 23, [film_eolas, play_eolas], 'indicative'),
         criterion('teideal', 'Teideal + ainm an scríbhneora', 2, [film_title, play_title], 'exact', permitted=[0, 1, 2]), deduction(m)],
        [PROSE_CHOICE, NO_PRESCRIBED_PROSE, BOTH, OPTIONAL_FILM_OR_PLAY] + LIT[1:],
        'One complete SEC response about an optional film or an optional play (the same scheme for both): 23 for five points (5, 5, 5, 4, 4) '
        'and 2 for the exact title and writer, then the 0–4 Gaeilge deduction once. The text is open content chosen by the candidate '
        '(indicative rather than exhaustive).',
        source('Prós Roghnach', 'Scannán nó dráma roghnach', [9]), concept='irish-prose-2b-irish-4-7', stem=STEM_2B)
    question_lit.append(cards[-1]['id'])

    # ---- Ceist 3A: An Spailpín Fánach and Colscaradh -------------------------------------------------
    poem_parts = {}
    for slug3, atlas3, page, title3, subs3, start3, end3 in POETRY_3A:
        pieces3, spages3 = poem_pieces(m, slug3, subs3, start3, end3)
        poem_parts[slug3] = (pieces3, spages3)
        crits = [criterion(f'eolas-{label}', f'({label}) Eolas', marks, [piece, note], 'indicative')
                 for (label, _, marks, _), piece in zip(subs3, pieces3)]
        prompt = '\n'.join(f'({label}) {p}' + f' ({marks} marc)' for label, p, marks, _ in subs3)
        add(atlas3, slug3, f'Poetry 3A({atlas3[-1]})', f'({atlas3[-1]}) {title3}\n' + prompt, POEM_TOPICS[slug3], [page], spages3, crits + [deduction(m)],
            [POETRY_CHOICE, BOTH] + LIT,
            'One complete SEC response: (i) 8, (ii) 8, (iii) 9 at their printed tariffs, then the 0–4 Gaeilge deduction once. '
            'The sample points are indicative rather than exhaustive; lines lifted straight from the poem without the candidate’s own words earn 2 + 2.',
            source('Filíocht Ainmnithe', title3, [page]), concept=f'irish-poetry-3a-{POEM_TOPICS[slug3]}', stem=BOX_3A)
        question_lit.append(cards[-1]['id'])

    # ---- Ceist 3B: Filíocht Roghnach (a) the pre-1850 poem and (b) the modern poem ---------------------
    for slug4, atlas4, prompts, start4, end4, cuts4 in POETRY_3B:
        chunk4, spages4 = m['s'].chunk(start4, end4, m['s'].text.index('⟦29⟧'))
        chunk4 = before_language_note(chunk4)
        idx = [0] + [chunk4.index(cut) for cut in cuts4]
        bits = [chunk4[a:b].strip() for a, b in zip(idx, idx[1:] + [len(chunk4)])]
        for bit, cap in zip(bits, ['(9 marc)', '(7 marc)', '(7 marc)', '(2 mharc)']):
            assert cap in bit, (slug4, cap)
        crits = [criterion('eolas-i', '(i) Eolas', 9, [bits[0]], 'indicative'), criterion('eolas-ii', '(ii) Eolas', 7, [bits[1]], 'indicative'),
                 criterion('eolas-iii', '(iii) Eolas', 7, [bits[2]], 'indicative'),
                 criterion('teideal', 'Teideal + ainm an fhile', 2, [bits[3]], 'exact', permitted=[0, 1, 2])]
        old = atlas4.endswith('a')
        add(atlas4, slug4, f'Poetry 3B({atlas4[-1]})', f'({atlas4[-1]}) ' + '\n'.join(prompts + [TITLE_LINE]), 'irish-5-6', [12], spages4,
            crits + [deduction(m)], [POETRY_CHOICE, NO_PRESCRIBED_POETRY, BOTH] + LIT,
            'One complete SEC response: (i) 9, (ii) 7, (iii) 7, poem and poet 2, then the 0–4 Gaeilge deduction once. '
            + ('3B(a) asks for an old poem (composed before 1850). ' if old else '3B(b) asks for a modern poem. ')
            + 'The optional poem is open content; the printed allocations are judged on merit (indicative rather than exhaustive).',
            source('Filíocht Roghnach', f'3B({atlas4[-1]}) · Dán roghnach', [12]),
            concept='irish-poetry-3b-irish-5-6', stem=STEM_3B)
        question_lit.append(cards[-1]['id'])

    # ---- Practice: the five Hurlamaboc sub-questions and every prescribed-poetry sub-question ----------
    src = source('Prós Ainmnithe', title, [8])
    for (label, prompt, _), piece in zip(subs, pieces):
        # The paper prints no per-sub-question tariff for 2A(a); the scheme prices each at (5 mharc).
        add(f'{atlas}-{label}', f'{slug}-{label}', f'Prós 2A({letter}) · {title} · ({label})', f'({letter}) {title}\n{intro}\n({label}) {prompt}',
            topic, [8], spages, [criterion('eolas', 'Eolas', 5, [piece, note], 'indicative', permitted=sub_permitted(piece, 5))],
            [PROSE_CHOICE, BOTH] + LIT[1:], sub_note, src, stem=BOX_2A)
        practice_ids.append(cards[-1]['id'])
    for slug3, atlas3, page, title3, subs3, start3, end3 in POETRY_3A:
        pieces3, spages3 = poem_parts[slug3]
        topic3 = POEM_TOPICS[slug3]
        src3 = source('Filíocht Ainmnithe', title3, [page])
        head = f'({atlas3[-1]}) {title3}\n'
        for (label, prompt, marks, _), piece in zip(subs3, pieces3):
            add(f'{atlas3}-{label}', f'{slug3}-{label}', f'Filíocht 3A({atlas3[-1]}) · {title3} · ({label})', head + f'({label}) {prompt} ({marks} marc)',
                topic3, [page], spages3, [criterion('eolas', 'Eolas', marks, [piece, note], 'indicative')],
                [POETRY_CHOICE, BOTH] + LIT[1:], sub_note, src3, stem=BOX_3A)
            practice_ids.append(cards[-1]['id'])

    assert len(whole_ids) == 10 and len(question_lit) == 9 and len(practice_ids) == 31, (len(whole_ids), len(question_lit), len(practice_ids))
    assert len(cards) == 50 and len({c['id'] for c in cards}) == 50 and len({c['atlasQuestionId'] for c in cards}) == 50
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
                              '2A(b) An Lasair Choille, 2B(a), 2B(b), 3A(a), 3A(b), 3B(a), 3B(b)); the 5 printed 2A(a) Hurlamaboc sub-questions and '
                              'the 6 prescribed-poetry sub-questions.'))
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
    print(f"Irish Ordinary {YEAR} Paper 2: {len(data['cards'])} reviewed cards (19 printed questions, 31 practice parts); the archive remains incomplete.")


if __name__ == '__main__':
    main()
