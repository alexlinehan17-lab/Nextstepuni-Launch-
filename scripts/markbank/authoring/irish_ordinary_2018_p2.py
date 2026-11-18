#!/usr/bin/env python3
"""Reviewed 2018 Ordinary Paper 2 (Léamhthuiscint agus Litríocht), carded new.

Paper PDF 1–12 and the Paper 2 pages of the combined LC001GLP000IV scheme (PDF 13–26,
plus 27 modified marking) reviewed on 2026-11-04. Counts are assertions, not
corpus-completeness proof. Same method as irish_ordinary_2020_p2.py.

No 2018 Ordinary card existed before. `build` cards the component the way the reviewed
2020–2025 Ordinary Paper 2s are carded: the ten whole reading questions (each part its
own 5-mark criterion), the eight literature questions (each printed sub-question its own
criterion, the 0–4 Gaeilge deduction once), and the practice cards beside them: every
reading part (20), the five printed sub-questions of 2A(a) Oisín i dTír na nÓg, every
prescribed-poetry sub-question (6) and the four printed questions inside 3A(a)(i)
Mo ghrá-sa (idir lúibíní).

2018's layout is 2020's: “FREAGAIR GACH CEIST (1, 2 AGUS 3).” Ceist 1 is Léamhthuiscint
A and B (both); Ceist 2 is A (Prós Ainmnithe) or B (Prós Roghnach) and Ceist 3 is A
(Filíocht Ainmnithe) or B (Filíocht Roghnach), each section printing two questions, (a)
and (b), both to be answered (“Freagair (a) agus (b) anseo.”). The texts rotate: 2A(a)
is Oisín with five sub-questions and 2A(b) Dís one 25-mark question (2020 the reverse);
3A is Mo ghrá-sa and Géibheann; 2B(a) is the folk tale and 2B(b) the short story, whose
23 marks are one block of five points (no separate theme mark). Each literature card
carries the printed choice and “Freagair (a) agus (b) anseo.” as its task check (choice
is not a route; no card combines two questions), and the section's printed box heading
with, for B, the printed restriction as its lead-in.

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
YEAR = 2018
FILE = 'LC001GLP200IV'
SCHEME_FILE = 'LC001GLP000IV'
OUT = ROOT / 'components/MarkBank/cards/irish/ordinary-2018-p2-authored.json'
SOURCE_REVIEW = ROOT / 'scripts/markbank/authored/irish-ordinary-2018-p2-source-review.json'
REVIEWED_AT = '2026-11-04'
PAPER_SHA = '197c9864592999a477854dfb25c157f451ebc33370d70b11c7c70f7cb14bbab6'
SCHEME_SHA = '53ed52f631d106673b1414040b0f9bae217434712b1c2984e2e03338f84f7ced'
DIRECTIVE = re.compile(r'rogha|roghna|Freagair|Luaigh|Ainmnigh|\bnó\b|dhá phointe|dhá rud|dhá bh|dhá dh|dhá ch|dhá fh|dhá th|dhá ph|dhá sh|'
                       r'\ban dá\b|ceann amháin|pointe amháin|amháin|\bdhá\b', re.I)
SOURCE_NOTE = 'Shown page-for-page from the official examination paper; swipe to move between pages.'
ATTRIBUTION = '© State Examinations Commission.'
# Boxed page headings the 2018 scheme's text layer stores with the page body (exact strings, each printed once).
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
        pages |= {int(m.group(1)) for m in re.finditer(r'⟦(\d+)⟧([^⟦]*)', raw) if clean(m.group(2)) not in ('', 'nó')}
        return clean(re.sub(r'⟦\d+⟧', ' ', raw)), sorted(pages)


def before_language_note(text):
    return re.split(r'\[\s*Gaeilge lochtach', text)[0].strip()


def split_at(text, cuts, slug):
    idx = [text.index(cut) for cut in cuts]
    assert idx == sorted(idx), slug
    return [text[a:b].strip() for a, b in zip(idx, idx[1:] + [len(text)])]


# Two points priced first-correct 3, second 2: “3 mharc + 2 mharc = 5 mharc”, or (Reading B 1(b)) the bare
# “5 mharc” followed by “An chéad … atá ceart = 3 mharc; an dara … atá ceart = 2 mharc”.
TWO_POINTS = re.compile(r'3 mharc \+ 2 mharc|; an dara [^=;]+ atá ceart = 2 mharc')

# (q, part, paper prompt, scheme anchor)
PASSAGES = {
    'A': dict(title='Éire an Lae Inniu', pages=[4, 5], topic='irish-3-0', start='⟦13⟧', notes_end='1. (a)',
              end='Nóta: Gearrfar pionós i ngeall ar iomarcaíocht. Léireofar', parts=[
        ('1', 'a', '(a) Scríobh síos dhá chúis a raibh blianta deacra ag muintir na hÉireann nuair a tharla an cúlú eacnamaíochta. (Alt 1)', '1. (a) Scríobh síos dhá chúis a raibh blianta deacra'),
        ('1', 'b', '(b) Cén fáth a bhfuil na seirbhísí poiblí ag feabhsú arís? (Alt 1)', '(b) Cén fáth a bhfuil na seirbhísí poiblí'),
        ('2', 'a', '(a) Cén fáth a raibh sé ina lá stairiúil nuair a bhuaigh Paul agus Gary Ó Donnabháin boinn airgid sna Cluichí Oilimpeacha in 2016? (Alt 2)', '2. (a) Cén fáth a raibh sé ina lá stairiúil'),
        ('2', 'b', '(b) Scríobh síos dhá phíosa eolais faoi ‘Stripe’, an córas íocaíochta ar líne. (Alt 2)', '(b) Scríobh síos dhá phíosa eolais faoi ‘Stripe’'),
        ('3', 'a', '(a) Cén seans a thugann an saoroideachas do gach duine sa tír seo? (Alt 3)', '3. (a) Cén seans a thugann an saoroideachas'),
        ('3', 'b', '(b) Tabhair dhá bhealach ar féidir le scoláirí a dtallanna a fhorbairt taobh amuigh den seomra ranga. (Alt 3)', '(b) Tabhair dhá bhealach ar féidir le scoláirí'),
        ('4', 'a', '(a) Cén fáth a bhfuil Bliain na Gaeilge ar siúl in 2018? (Alt 4)', '4. (a) Cén fáth a bhfuil Bliain na Gaeilge'),
        ('4', 'b', '(b) Tabhair dhá shampla d’úsáid na Gaeilge ar líne. (Alt 4)', '(b) Tabhair dhá shampla d’úsáid na Gaeilge'),
        ('5', 'a', '(a) Scríobh síos dhá cheann de na fadhbanna atá sa tír fós. (Alt 5)', '5. (a) Scríobh síos dhá cheann de na fadhbanna'),
        ('5', 'b', '(b) Cén baol atá ann don tír seo nuair a fhágfaidh an Bhreatain an tAontas Eorpach? (Alt 5)', '(b) Cén baol atá ann don tír seo')]),
    'B': dict(title='Caitríona Perry: Craoltóir, Láithreoir agus Údar', pages=[6, 7], topic='irish-3-1', start='⟦16⟧', notes_end='1. (a)',
              end='Nóta: Gearrfar pionós i ngeall ar iomarcaíocht. Léireofar', parts=[
        ('1', 'a', '(a) Cén obair a rinne Caitríona Perry in Washington mar chomhfhreagraí RTÉ? (Alt 1)', '1. (a) Cén obair a rinne Caitríona Perry'),
        ('1', 'b', '(b) Scríobh síos dhá phíosa eolais faoin rud neamhghnách a tharla do Chaitríona in oifig Uachtarán na Stát Aontaithe sa Teach Bán. (Alt 1)', '(b) Scríobh síos dhá phíosa eolais faoin rud neamhghnách'),
        ('2', 'a', '(a) Cad a rinne Caitríona in Ollscoil Chathair Bhaile Átha Cliath? (Alt 2)', '2. (a) Cad a rinne Caitríona in Ollscoil'),
        ('2', 'b', '(b) Cén staidéar a rinne Caitríona mar chuid dá cúrsa iarchéime? (Alt 2)', '(b) Cén staidéar a rinne Caitríona'),
        ('3', 'a', '(a) Luaigh dhá chúis a raibh saol oibre Chaitríona i Meiriceá deacair. (Alt 3)', '3. (a) Luaigh dhá chúis a raibh saol oibre'),
        ('3', 'b', '(b) Cén fáth a bhfuair Caitríona moladh mór sa bhliain 2015? (Alt 3)', '(b) Cén fáth a bhfuair Caitríona moladh mór'),
        ('4', 'a', '(a) Cad a rinne Caitríona nuair a bhí an feachtas uachtaránachta deireanach ar siúl i Meiriceá? (Alt 4)', '4. (a) Cad a rinne Caitríona nuair a bhí an feachtas'),
        ('4', 'b', '(b) Tabhair dhá chúis ar bhuaigh Trump toghchán na huachtaránachta, de réir an chuntais i leabhar Chaitríona. (Alt 4)', '(b) Tabhair dhá chúis ar bhuaigh Trump'),
        ('5', 'a', '(a) Cad a dhéanann Caitríona Perry agus Keelin Shanley in RTÉ anois? (Alt 5)', '5. (a) Cad a dhéanann Caitríona Perry agus Keelin'),
        ('5', 'b', '(b) Scríobh síos dhá rud a dhéanann Caitríona nuair a bhíonn am saor aici. (Alt 5)', '(b) Scríobh síos dhá rud a dhéanann Caitríona')]),
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

# 2A(a) Oisín i dTír na nÓg: printed sub-questions at 5 each (the paper prints only the question's (25 marc)).
OISIN = ('prose-2a-a', 'P-2A-a', 'a', 'Oisín i dTír na nÓg', 'irish-4-1', 'Freagair na ceisteanna thíos faoin scéal béaloidis Oisín i dTír na nÓg.', [
    ('i', 'Cén fáth ar tháinig Niamh Chinn Óir go hÉirinn?', '(i) Cén fáth ar tháinig Niamh Chinn Óir'),
    ('ii', 'Tabhair dhá rud a d’inis Niamh Chinn Óir d’Oisín faoi Thír na nÓg.', '(ii) Tabhair dhá rud a d’inis Niamh'),
    ('iii', 'Scríobh síos dhá rud a tharla chomh luath agus a shroich Niamh Chinn Óir agus Oisín Tír na nÓg le chéile den chéad uair.', '(iii) Scríobh síos dhá rud a tharla chomh luath'),
    ('iv', 'Cad a dúirt Niamh Chinn Óir le hOisín nuair a bhí an t-each bán á thabhairt aici dó chun filleadh ar Éirinn?', '(iv) Cad a dúirt Niamh Chinn Óir'),
    ('v', 'Luaigh dhá chúis ar mhaith le Naomh Pádraig Oisín a thabhairt leis ar a thurais ar fud na hÉireann.', '(v) Luaigh dhá chúis ar mhaith le Naomh Pádraig')],
    '(a) Oisín i dTír na nÓg Freagair na ceisteanna thíos', '(b) Dís (25 marc)')
# 2A(b) Dís: one 25-mark question.
DIS = ('prose-2a-b', 'P-2A-b', 'b', 'Dís', 'irish-4-4',
       '“Féach ansan. Toradh suirbhé a deineadh. Deirtear ann go bhfuil an ceathrú cuid de mhná pósta na tíre míshona, míshásta. Táimse ansan, ina measc.” Dís\n'
       'Déan cur síos ar an gcomhrá idir Seán agus a bhean chéile faoin suirbhé an tráthnóna sin.',
       '(b) Dís (25 marc)', 'Níl cead aon ábhar a bhaineann le Prós Ainmnithe')
# 2B: (slug, atlas, paper lines, scheme start, scheme end, [(id, label, marks, cut-before)], source title)
PROSE_2B = [
    ('prose-2b-a', 'P-2B-a', ['(a) Maidir le scéal béaloidis roghnach a ndearna tú staidéar air le linn do chúrsa, ainmnigh an phríomhphearsa (an príomhcharachtar) sa scéal. '
                              'Tabhair cuntas ar na heachtraí is mó a tharlaíonn don duine sin ó thús go deireadh an scéil. (23 marc)',
                              'Ní mór teideal an scéil bhéaloidis sin a scríobh síos go cruinn. (2 mharc)'],
     '(a) Maidir le scéal béaloidis roghnach', '(b) Maidir le gearrscéal roghnach',
     [('priomhphearsa', 'An phríomhphearsa a ainmniú', 1, None), ('eolas', 'Na heachtraí is mó', 22, 'Na heachtraí is mó a tharlaíonn'),
      ('teideal', 'Teideal an scéil bhéaloidis', 2, 'Ní mór teideal')], 'Scéal béaloidis roghnach'),
    ('prose-2b-b', 'P-2B-b', ['(b) Maidir le gearrscéal roghnach a ndearna tú staidéar air le linn do chúrsa, tabhair cuntas ar na príomhimeachtaí (príomhrudaí) '
                              'a tharlaíonn sa ghearrscéal sin. (23 marc)',
                              'Ní mór teideal an ghearrscéil sin, mar aon le hainm an údair, a scríobh síos go cruinn. (2 mharc)'],
     '(b) Maidir le gearrscéal roghnach', 'Freagair A (Filíocht Ainmnithe)',
     [('eolas', 'Na príomhimeachtaí', 23, None), ('teideal', 'Teideal + ainm an údair', 2, 'Ní mór teideal')], 'Gearrscéal roghnach'),
]
# 3A: (slug, atlas, page, title, [(label, paper prompt, marks, scheme cut)], scheme start, scheme end)
POETRY_3A = [
    ('poetry-3a-a', 'F-3A-a', 10, 'Mo ghrá-sa (idir lúibíní)', [
        ('i', '(a) Cá mbíonn bláth na n-airní ag fás?\n(b) Cathain a fhásfaidh nóiníní as cluasa an fhir?\n(c) Cén cur síos a dhéanann an file ar shúile an fhir?\n'
              '(d) Scríobh síos rud amháin a deir an file faoi ghruaig an fhir.', 8, '(i) (a) Cá mbíonn bláth na n-airní'),
        ('ii', 'Scríobh síos an mothúchán is láidre sa dán, dar leat. Tabhair dhá shampla, i d’fhocail féin, den mhothúchán sin sa dán.', 9,
         '(ii) Scríobh síos an mothúchán is láidre'),
        ('iii', 'An maith leat an dán seo? Cuir fáthanna le do fhreagra. (Is leor dhá fháth.)', 8, '(iii) An maith leat an dán seo?')],
     '(a) Mo ghrá-sa (idir lúibíní) (25 marc)', '(b) Géibheann (25 marc)'),
    ('poetry-3a-b', 'F-3A-b', 11, 'Géibheann', [
        ('i', 'Cén mothúchán is mó a thaispeánann an t-ainmhí sna línte 1-8 den dán Géibheann, dar leat? '
              'Tabhair dhá phointe eolais, i d’fhocail féin, faoin mothúchán sin sna línte 1-8.', 9, '(i) Cén mothúchán is mó a thaispeánann'),
        ('ii', 'Déan cur síos, i d’fhocail féin, ar an íomhá (ar an bpictiúr) den ainmhí a fhaighimid sna línte 9-12 den dán. (Is leor dhá phointe eolais.)', 8,
         '(ii) Déan cur síos, i d’fhocail féin'),
        ('iii', 'Cén t-eolas a fhaighimid sna línte 13-17 faoi na daoine a fheiceann an t-ainmhí anois? (Is leor dhá phointe eolais i d’fhocail féin.)', 8,
         '(iii) Cén t-eolas a fhaighimid')],
     '(b) Géibheann (25 marc)', 'Níl cead aon ábhar a bhaineann le Filíocht Ainmnithe'),
]
POEM_TOPICS = {'poetry-3a-a': 'irish-5-4', 'poetry-3a-b': 'irish-5-2'}
# Where the scheme says lines lifted from the poem without the candidate's own words earn 2 + 2.
LIFTED_LINES = {'poetry-3a-a': '(ii)', 'poetry-3a-b': '(iii)'}
# 3A(a)(i) prints four questions (a)–(d) at 2 each: (slug, sub-question) -> [(letter, scheme question, marks, next cut)]
SLOTS_3A = {
    ('poetry-3a-a', 'i'): [('a', 'Cá mbíonn bláth na n-airní ag fás?', 2, '(b) Cathain a fhásfaidh'),
                           ('b', 'Cathain a fhásfaidh nóiníní as cluasa an fhir?', 2, '(c) Cén cur síos'),
                           ('c', 'Cén cur síos a dhéanann an file ar shúile an fhir?', 2, '(d) Scríobh síos rud amháin'),
                           ('d', 'Scríobh síos rud amháin a deir an file faoi ghruaig an fhir.', 2, None)],
}
SLOT_PERMITTED = {('poetry-3a-a', 'i'): [0, 2, 4, 6, 8]}
POETRY_3B = [
    ('poetry-3b-a', 'F-3B-a', [
        '(i) Maidir le dán roghnach nua-aimseartha amháin a ndearna tú staidéar air le linn do chúrsa, scríobh síos príomhthéama an dáin sin, dar leat. '
        'Tabhair dhá phointe eolais, i d’fhocail féin, faoin téama sin sa dán. (9 marc)',
        '(ii) Scríobh síos an mothúchán is láidre sa dán, dar leat. Tabhair dhá shampla den mhothúchán sin sa dán. (7 marc)',
        '(iii) An maith leat an dán seo? Cuir fáthanna le do fhreagra. (Is leor dhá fháth.) (7 marc)'],
     '(a) (i) Maidir le dán roghnach nua-aimseartha', '(b) (i) Maidir le dán roghnach nua-aimseartha', ['(ii) Scríobh síos an mothúchán', '(iii) An maith leat', 'Ní mór teideal an dáin']),
    ('poetry-3b-b', 'F-3B-b', [
        '(i) Maidir le dán roghnach nua-aimseartha amháin a ndearna tú staidéar air le linn do chúrsa agus nár úsáid tú i gcuid (a) thuas, '
        'scríobh síos i d’fhocail féin, príomhsmaointe an dáin. (9 marc)',
        '(ii) Mínigh, i d’fhocail féin, an íomhá (an pictiúr) is mó a thaitníonn leat sa dán. (Is leor dhá phointe eolais.) (7 marc)',
        '(iii) Cén t-atmaisféar atá sa dán seo, dar leat? Scríobh síos dhá phointe eolais, i d’fhocail féin, faoin atmaisféar sin sa dán. (7 marc)'],
     '(b) (i) Maidir le dán roghnach nua-aimseartha', None, ['(ii) Mínigh, i d’fhocail féin', '(iii) Cén t-atmaisféar', 'Ní mór teideal an dáin']),
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
    s = Scheme(doc, 13, 26)
    assert s.removed == len(FURNITURE), s.removed
    assert not PUA.search(s.text), 'private-use glyph left in the scheme text'
    assert 'Léirigh mionbhriseadh' not in s.text, '2018 prints no literature mark-panel line'
    lang_read = '[Gaeilge lochtach: 0 - 5 a bhaint den iomlán a gnóthaíodh]'
    assert s.text.count(lang_read) == 2
    for letter, passage in PASSAGES.items():
        page_text = ' '.join(texts[p - 1] for p in passage['pages'])
        after = s.text.index(passage['start'])
        # 2018 prints one note above each passage's Ceist 1 (the penalty note only with the mark boxes at the end).
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
            permitted = [0, 3, 5] if (two or '= 3 mharc' in chunk) else [0, 5]
            resolved.append((q, part, prompt, chunk, spages, two, permitted))
        passage['resolved'] = resolved
    # The literature note is printed twice (above 2A on PDF 19 and above 3A on PDF 23), word for word.
    lit_note = s.chunk('Nóta: Níl sé i gceist a chur in iúl go bhfuil na freagraí samplacha', 'Freagair (a) agus (b) anseo.')[0]
    assert s.chunk('Nóta: Níl sé i gceist a chur in iúl go bhfuil na freagraí samplacha', 'Freagair (a) agus (b) anseo.',
                   s.text.index('⟦23⟧'))[0] == lit_note
    lang_lit = '[Gaeilge lochtach: 0-4 a bhaint den iomlán a gnóthaíodh]'
    # Oisín, Dís, 2B(a), 2B(b), Mo ghrá-sa, Géibheann, 3B(a), 3B(b): eight, all printed alike.
    assert s.text.count(lang_lit) == 8 and s.text.count(lang_lit[:-1] + '.]') == 0, s.text.count(lang_lit)
    slug, atlas, letter, title, topic, intro, subs, start, end = OISIN
    for line in [intro, title] + [p for _, p, _ in subs]:
        assert in_order(line, texts[7]), (slug, line[:40])
    slug, atlas, letter, title, topic, prompt, start, end = DIS
    assert in_order(title, texts[7]) and in_order(prompt, texts[7]), slug
    for slug, atlas, lines, start, end, parts, title in PROSE_2B:
        for line in lines:
            assert in_order(line, texts[8]), (slug, line[:50])
    for slug, atlas, page, title, subs, start, end in POETRY_3A:
        assert in_order(title, texts[page - 1]), slug
        for label, prompt, marks, cut in subs:
            assert in_order(prompt.replace('\n', ' ') + f' ({marks} marc)', texts[page - 1]), (slug, label)
    for slug, atlas, prompts, start, end, cuts in POETRY_3B:
        for line in prompts + [TITLE_LINE]:
            assert in_order(line, texts[11]), (slug, line[:50])
    assert comparable(texts[11]).count(comparable(TITLE_LINE)) == 2
    for page, line in [(3, 'FREAGAIR GACH CEIST (1, 2 AGUS 3).'), (8, PROSE_CHOICE), (8, BOTH), (8, BOX_2A), (9, BOX_2B), (9, NO_PRESCRIBED_PROSE), (9, BOTH),
                       (10, POETRY_CHOICE), (10, BOTH), (10, BOX_3A), (12, BOX_3B), (12, NO_PRESCRIBED_POETRY), (12, BOTH)]:
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


def oisin_pieces(m):
    slug, atlas, letter, title, topic, intro, subs, start, end = OISIN
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
        assert f'({marks} marc)' in piece or (slug, label) in SLOTS_3A, (slug, label, piece[:60])
    return pieces, sorted(set(spages) | {23})


def slot_pieces(piece, slots):
    out = []
    for sub, question, marks, nxt in slots:
        start_at = piece.index(question)
        slot = piece[start_at:piece.index(nxt, start_at) if nxt else len(piece)].strip()
        assert re.search(r'Freagraí [Ss]amplacha:', slot) and f'({marks} mharc)' in slot, (sub, slot[:60])
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

    note, lang = m['lit_note'], m['lang_lit']
    sub_note = 'One printed sub-question at its published tariff. ' + LIT_DEDUCTION_NOTE
    question_lit = []
    # ---- Ceist 2A: Oisín i dTír na nÓg (five sub-questions) and Dís ------------------------------------
    slug, atlas, letter, title, topic, intro, subs, start, end = OISIN
    pieces, spages = oisin_pieces(m)
    src = source('Prós Ainmnithe', title, [8])
    requirements = [PROSE_CHOICE, BOTH] + LIT
    add(atlas, slug, 'Prose 2A(a)', f'({letter}) {title}\n{intro}\n' + '\n'.join(f'({l}) {p}' for l, p, _ in subs) + '\n(25 marc)',
        topic, [8], spages,
        [criterion(f'eolas-{label}', f'({label}) Eolas', 5, [piece, note], 'indicative', permitted=sub_permitted(piece, 5))
         for (label, _, _), piece in zip(subs, pieces)] + [deduction(m)], requirements,
        'One complete SEC response: five printed sub-questions at 5 each, then the 0–4 Gaeilge deduction once. '
        'The sample answers are indicative rather than exhaustive.', src, concept=f'irish-prose-2a-{topic}', stem=BOX_2A)
    question_lit.append(cards[-1]['id'])
    slug_d, atlas_d, letter_d, title_d, topic_d, prompt_d, start_d, end_d = DIS
    chunk, dspages = m['s'].chunk(start_d, end_d)
    assert '5 phointe eolais agus 5 mharc ar gach pointe eolais' in chunk
    add(atlas_d, slug_d, 'Prose 2A(b)', f'({letter_d}) {title_d}\n{prompt_d}\n(25 marc)', topic_d, [8], sorted(set(dspages) | {19}),
        [criterion('eolas', 'Eolas', 25, [before_language_note(chunk), note], 'indicative'), deduction(m)], [PROSE_CHOICE, BOTH] + LIT[1:],
        WHOLE_PROSE_NOTE, source('Prós Ainmnithe', title_d, [8]), concept=f'irish-prose-2a-{topic_d}', stem=BOX_2A)
    question_lit.append(cards[-1]['id'])

    # ---- Ceist 2B: Prós Roghnach (a) and (b) ------------------------------------------------------------
    for slug2, atlas2, lines, start2, end2, parts, title2 in PROSE_2B:
        chunk2, spages2 = m['s'].chunk(start2, end2)
        chunk2 = before_language_note(chunk2)
        cuts = [0] + [chunk2.index(cut) for _, _, _, cut in parts[1:]]
        bits = [chunk2[a:b].strip() for a, b in zip(cuts, cuts[1:] + [len(chunk2)])]
        crits = [criterion(cid, label, marks, [bit], 'exact' if cid == 'teideal' else 'indicative',
                           permitted=None if cid == 'eolas' else sorted({0, marks} | {int(v) for v in re.findall(r'= (\d) mharc', bit)}))
                 for (cid, label, marks, _), bit in zip(parts, bits)]
        assert crits[-1]['guidance'][0].endswith('(2 mharc)'), (slug2, crits[-1]['guidance'][0][-60:])
        add(atlas2, slug2, f'Prose 2B({atlas2[-1]})', '\n'.join(lines), 'irish-4-7', [9], spages2, crits + [deduction(m)],
            [PROSE_CHOICE, NO_PRESCRIBED_PROSE, BOTH] + LIT[1:],
            'One complete SEC response: ' + ', '.join(f'{label} {marks}' for _, label, marks, _ in parts) +
            ', then the 0–4 Gaeilge deduction once. The optional text is open content chosen by the candidate; the scheme prints no sample '
            'points for it, so its points are judged on merit against these allocations (indicative rather than exhaustive).',
            source('Prós Roghnach', title2, [9]), concept='irish-prose-2b-irish-4-7', stem=STEM_2B)
        question_lit.append(cards[-1]['id'])

    # ---- Ceist 3A: Mo ghrá-sa (idir lúibíní) and Géibheann ------------------------------------------------
    poem_parts = {}
    for slug3, atlas3, page, title3, subs3, start3, end3 in POETRY_3A:
        pieces3, spages3 = poem_pieces(m, slug3, subs3, start3, end3)
        poem_parts[slug3] = (pieces3, spages3)
        crits = [criterion(f'eolas-{label}', f'({label}) Eolas', marks, [piece, note], 'indicative', permitted=SLOT_PERMITTED.get((slug3, label)))
                 for (label, _, marks, _), piece in zip(subs3, pieces3)]
        prompt = '\n'.join(f'({label}) {p}' + f' ({marks} marc)' for label, p, marks, _ in subs3)
        add(atlas3, slug3, f'Poetry 3A({atlas3[-1]})', f'({atlas3[-1]}) {title3}\n' + prompt, POEM_TOPICS[slug3], [page], spages3, crits + [deduction(m)],
            [POETRY_CHOICE, BOTH] + LIT,
            'One complete SEC response: ' + ', '.join(f'({label}) {marks}' for label, _, marks, _ in subs3) +
            ' at their printed tariffs, then the 0–4 Gaeilge deduction once. The sample points are indicative rather than exhaustive; in '
            f'{LIFTED_LINES[slug3]} the scheme gives lines lifted straight from the poem without the candidate’s own words 2 + 2.',
            source('Filíocht Ainmnithe', title3, [page]), concept=f'irish-poetry-3a-{POEM_TOPICS[slug3]}', stem=BOX_3A)
        question_lit.append(cards[-1]['id'])

    # ---- Ceist 3B: Filíocht Roghnach (a) and (b) --------------------------------------------------------
    for slug4, atlas4, prompts, start4, end4, cuts4 in POETRY_3B:
        chunk4, spages4 = m['s'].chunk(start4, end4, m['s'].text.index('⟦25⟧'))
        chunk4 = before_language_note(chunk4)
        idx = [0] + [chunk4.index(cut) for cut in cuts4]
        bits = [chunk4[a:b].strip() for a, b in zip(idx, idx[1:] + [len(chunk4)])]
        for bit, cap in zip(bits, ['(9 marc)', '(7 marc)', '(7 marc)', '(2 mharc)']):
            assert cap in bit, (slug4, cap)
        crits = [criterion('eolas-i', '(i) Eolas', 9, [bits[0]], 'indicative'), criterion('eolas-ii', '(ii) Eolas', 7, [bits[1]], 'indicative'),
                 criterion('eolas-iii', '(iii) Eolas', 7, [bits[2]], 'indicative'),
                 criterion('teideal', 'Teideal + ainm an fhile', 2, [bits[3]], 'exact', permitted=[0, 1, 2])]
        add(atlas4, slug4, f'Poetry 3B({atlas4[-1]})', f'({atlas4[-1]}) ' + '\n'.join(prompts + [TITLE_LINE]), 'irish-5-6', [12], spages4,
            crits + [deduction(m)], [POETRY_CHOICE, NO_PRESCRIBED_POETRY, BOTH] + LIT,
            'One complete SEC response: (i) 9, (ii) 7, (iii) 7, poem and poet 2, then the 0–4 Gaeilge deduction once. '
            'The optional poem is open content; 3B(b) asks for a modern poem not used in 3B(a). The printed allocations are judged on merit '
            '(indicative rather than exhaustive).',
            source('Filíocht Roghnach', f'3B({atlas4[-1]}) · Dán roghnach', [12]),
            concept='irish-poetry-3b-irish-5-6', stem=STEM_3B)
        question_lit.append(cards[-1]['id'])

    # ---- Practice: the five Oisín sub-questions, every prescribed-poetry sub-question, 3A(a)(i)(a)–(d) ----
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
            slots = SLOTS_3A.get((slug3, label))
            add(f'{atlas3}-{label}', f'{slug3}-{label}', f'Filíocht 3A({atlas3[-1]}) · {title3} · ({label})', head + f'({label}) {prompt} ({marks} marc)',
                topic3, [page], spages3,
                [criterion('eolas', 'Eolas', marks, [piece, note], 'indicative', permitted=SLOT_PERMITTED.get((slug3, label)))],
                [POETRY_CHOICE, BOTH] + LIT[1:], sub_note, src3, stem=BOX_3A)
            practice_ids.append(cards[-1]['id'])
            if slots:
                printed = dict(re.findall(r'\(([a-d])\) ([^\n]+)', prompt))
                for (sub, slot), (_, _, smarks, _) in zip(slot_pieces(piece, slots), slots):
                    add(f'{atlas3}-{label}-{sub}', f'{slug3}-{label}-{sub}', f'Filíocht 3A({atlas3[-1]}) · {title3} · ({label})({sub})',
                        head + f'({label}) ({sub}) {printed[sub]}', topic3, [page], spages3,
                        [criterion('eolas', 'Freagra', smarks, [slot], 'indicative', permitted=list(range(0, smarks + 1, 2)))], [POETRY_CHOICE, BOTH] + LIT[1:],
                        f'One printed question inside 3A({atlas3[-1]})({label}), at its printed ({smarks} mharc). ' + LIT_DEDUCTION_NOTE, src3, stem=BOX_3A)
                    practice_ids.append(cards[-1]['id'])

    assert len(whole_ids) == 10 and len(question_lit) == 8 and len(practice_ids) == 35, (len(whole_ids), len(question_lit), len(practice_ids))
    assert len(cards) == 53 and len({c['id'] for c in cards}) == 53 and len({c['atlasQuestionId'] for c in cards}) == 53
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
                  boundaries=('10 whole reading questions with their 20 published parts; 8 literature questions; the 5 printed 2A(a) Oisín i dTír na nÓg '
                              'sub-questions, the 6 prescribed-poetry sub-questions and the 4 printed questions inside 3A(a)(i).'))
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
