#!/usr/bin/env python3
"""Reviewed 2024 Ordinary Paper 2 (Léamhthuiscint agus Litríocht).

Paper PDF 1–16 and the Paper 2 pages of the combined LC001GLP000IV scheme
(PDF 14–32, plus 33 modified marking) visually reviewed on 2026-10-12. Counts are
assertions, not corpus-completeness proof. Same method as irish_ordinary_2025_p2.py.

The legacy generator already ships 22 cards for this component: the ten whole
reading questions and the twelve literature options. Their IDs, totals and topics
are kept. `apply_legacy_review` (called by irish_cards.py) joins them to Atlas and
replaces their marking with the lifted 2024 scheme. `build` adds every reading part
(20), the printed sub-questions of 2A(a) Dís and 2A(b) Oisín i dTír na nÓg (10),
every prescribed-poetry sub-question (9) with the four 3A(b)(i) questions, and the
An Lasair Choille option of 2A(c).

Choice is not a route: “Freagair do rogha dhá cheann as (a), (b) nó (c)” sits in
each option's task requirements; no card combines two options. Inside 2A(c) the
film Cáca Milis and the play An Lasair Choille are different syllabus texts with
their own sample answers, so each keeps its own card (the legacy 2A(c) card becomes
Cáca Milis). Inside 2B(c) the optional film and optional play share one grid and one
topic, so they stay one card with both printed alternatives.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
FILE = 'LC001GLP200IV'
SCHEME_FILE = 'LC001GLP000IV'
OUT = ROOT / 'components/MarkBank/cards/irish/ordinary-2024-p2-authored.json'
SOURCE_REVIEW = ROOT / 'scripts/markbank/authored/irish-ordinary-2024-p2-source-review.json'
REVIEWED_AT = '2026-10-12'
PAPER_SHA = 'a126af58bc3b01962e0fd11e2d742fc415c9de6220c4f8b4bf0300be1fa91a9e'
SCHEME_SHA = '954e2a1e867a0926326bf5273db46fca631cbd0437a1c62c0da677c0ff39fcbe'
DIRECTIVE = re.compile(r'rogha|roghna|Freagair|Luaigh|Ainmnigh|\bnó\b|dhá phointe|dhá rud|dhá bh|dhá dh|dhá ch|dhá fh|dhá th|dhá ph|dhá sh|'
                       r'\ban dá\b|ceann amháin|pointe amháin|amháin', re.I)
SOURCE_NOTE = 'Shown page-for-page from the official examination paper; swipe to move between pages.'
ATTRIBUTION = '© State Examinations Commission.'


def clean(text):
    return re.sub(r'\s+', ' ', text).strip()


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
        for p in range(first, last + 1):
            self.text += f' ⟦{p}⟧ ' + re.sub(r'^\d+\s', '', clean(doc[p - 1].get_text()).replace('', '•'))

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


# (q, part, paper prompt, scheme anchor)
PASSAGES = {
    'A': dict(title='Oileán agus Ionad an Bhlascaoid Mhóir', pages=[4, 5], topic='irish-3-0', start='⟦15⟧', parts=[
        ('1', 'a', '(a) Cén fáth ar osclaíodh Ionad an Bhlascaoid Mhóir? (Alt 1)', '1. (a) Cén fáth ar osclaíodh'),
        ('1', 'b', '(b) Tabhair dhá phíosa eolais faoin ardán féachana atá suite ar shuíomh an ionaid. (Alt 1)', '(b) Tabhair dhá phíosa eolais faoin ardán'),
        ('2', 'a', '(a) Scríobh síos dhá chineál oibre a bhíodh ar siúl ag na fir. (Alt 2)', '2. (a) Scríobh síos dhá chineál oibre'),
        ('2', 'b', '(b) Cén nós a bhíodh ag muintir an oileáin sna hoícheanta? (Alt 2)', '(b) Cén nós a bhíodh'),
        ('3', 'a', '(a) Scríobh síos dhá bhealach a gcuireadh cúrsaí aimsire isteach ar mhuintir an Bhlascaoid Mhóir. (Alt 3)', '3. (a) Scríobh síos dhá bhealach'),
        ('3', 'b', '(b) Tabhair dhá fháth ar fhág na daoine óga an Blascaod Mór. (Alt 3)', '(b) Tabhair dhá fháth ar fhág'),
        ('4', 'a', '(a) Cén fáth a raibh an lucht léinn ón iasacht tábhachtach? (Alt 4)', '4. (a) Cén fáth a raibh an lucht léinn'),
        ('4', 'b', '(b) Cén oidhreacht is tábhachtaí a d’fhág Peig Sayers ina diaidh? (Alt 4)', '(b) Cén oidhreacht is tábhachtaí'),
        ('5', 'a', '(a) Cad a dúirt an tUasal Leo Varadkar ina óráid in Ionad an Bhlascaoid Mhóir i mí Mheán Fómhair seo caite? (Alt 5)', '5. (a) Cad a dúirt an tUasal'),
        ('5', 'b', '(b) Cén plean atá ag Oifig na nOibreacha Poiblí faoi láthair? (Alt 5)', '(b) Cén plean atá ag Oifig')]),
    'B': dict(title='Mearfhaisean', pages=[6, 7], topic='irish-3-1', start='⟦17⟧', parts=[
        ('1', 'a', '(a) Cad is brí leis an téarma ‘mearfhaisean’? (Alt 1)', '1. (a) Cad is brí leis an téarma'),
        ('1', 'b', '(b) Scríobh síos dhá phíosa eolais faoi na héadaí a dhéantar i dtionscal an mhearfhaisin. (Alt 1)', '(b) Scríobh síos dhá phíosa eolais faoi na héadaí'),
        ('2', 'a', '(a) Cad a dhéanann déantóirí an mhearfhaisin go luath i ndiaidh na seónna móra faisin? (Alt 2)', '2. (a) Cad a dhéanann déantóirí'),
        ('2', 'b', '(b) Luaigh an dá rud a tharlaíonn mar chuid den chomhoibriú idir branda éadaí agus tionchaire faisin. (Alt 2)', '(b) Luaigh an dá rud a tharlaíonn'),
        ('3', 'a', '(a) Scríobh síos dhá phíosa eolais a léiríonn go gcaitear go dona leis na hoibrithe sna monarchana mearfhaisin go minic. (Alt 3)', '3. (a) Scríobh síos dhá phíosa eolais a léiríonn'),
        ('3', 'b', '(b) Tabhair dhá shlí a ndéanann tionscal an mhearfhaisin dochar don timpeallacht. (Alt 3)', '(b) Tabhair dhá shlí a ndéanann'),
        ('4', 'a', '(a) Scríobh síos dhá rud a mholtar do dhaoine a dhéanamh chun an méid dochair atá a nósanna faisin ag déanamh don timpeallacht a laghdú. (Alt 4)', '4. (a) Scríobh síos dhá rud a mholtar'),
        ('4', 'b', '(b) Cén sórt duine a roghnaíodh do gach clár sa tsraith Éadaí SOS? (Alt 4)', '(b) Cén sórt duine'),
        ('5', 'a', '(a) Tabhair an dá bhuntáiste a bhaineann le héadaí athláimhe a cheannach ar www.thriftify.ie. (Alt 5)', '5. (a) Tabhair an dá bhuntáiste'),
        ('5', 'b', '(b) Cad a iarrtar ar dhearthóirí óga a dhéanamh chun cur isteach ar an gcomórtas Junk Kouture? (Alt 5)', '(b) Cad a iarrtar ar dhearthóirí')]),
}

HEAD2A = 'Freagair 2A (Prós Ainmnithe) nó 2B (Prós Roghnach).\n2A Prós Ainmnithe — Freagair do rogha dhá cheann as (a), (b) nó (c) thíos.'
HEAD2B = ('Freagair 2A (Prós Ainmnithe) nó 2B (Prós Roghnach).\n2B Prós Roghnach — Níl cead aon ábhar a bhaineann le Prós Ainmnithe a úsáid sna '
          'freagraí ar an bPrós Roghnach. Freagair do rogha dhá cheann as (a), (b) nó (c) thíos.')
HEAD3A = 'Freagair 3A (Filíocht Ainmnithe) nó 3B (Filíocht Roghnach).\n3A Filíocht Ainmnithe — Freagair do rogha dhá cheann as (a), (b) nó (c).'
HEAD3B = ('Freagair 3A (Filíocht Ainmnithe) nó 3B (Filíocht Roghnach).\n3B Filíocht Roghnach — Níl cead aon ábhar a bhaineann le Filíocht Ainmnithe a '
          'úsáid sna freagraí ar an bhFilíocht Roghnach. Freagair do rogha dhá cheann as (a), (b) nó (c) thíos. Níl cead an dán roghnach céanna '
          'a úsáid faoi dhó sna freagraí ar (a), (b) nó (c) thíos.')
CHOOSE = 'Freagair do rogha dhá cheann as (a), (b) nó (c) thíos.'
CHOOSE_3A = 'Freagair do rogha dhá cheann as (a), (b) nó (c).'
FILM_OR_PLAY = 'Freagair an cheist thíos faoin scannán Cáca Milis nó faoin dráma An Lasair Choille.'
OPT_FILM_OR_PLAY = 'Freagair an cheist thíos faoin scannán roghnach nó faoin dráma roghnach.'
NO_PRESCRIBED_PROSE = 'Níl cead aon ábhar a bhaineann le Prós Ainmnithe a úsáid sna freagraí ar an bPrós Roghnach.'
NO_PRESCRIBED_POETRY = 'Níl cead aon ábhar a bhaineann le Filíocht Ainmnithe a úsáid sna freagraí ar an bhFilíocht Roghnach.'
SAME_POEM = 'Níl cead an dán roghnach céanna a úsáid faoi dhó sna freagraí ar (a), (b) nó (c) thíos.'
LIT = ['Freagair gach fochuid atá priontáilte sa rogha seo.', 'Úsáid tagairtí cruinne agus ábhartha don téacs.']
READING_PART = ['Léigh an sliocht iomlán a ghabhann leis an gceist. Freagair an chuid atá luaite ar an gcárta.', 'Úsáid an t-alt a luaitear.']
READING_WHOLE = ['Léigh an sliocht oifigiúil a ghabhann leis an gceist.', 'Freagair gach fochuid agus cloígh leis an alt a luaitear.']

# Prescribed prose with printed sub-questions: (slug, atlas, letter, title, topic, intro, [(label, paper prompt, scheme cut)], scheme start, scheme end)
PROSE_SUBS = [
    ('prose-2a-a', 'P-2A-a', 'a', 'Dís', 'irish-4-4', 'Freagair na ceisteanna thíos faoin ngearrscéal Dís.', [
        ('i', 'Luaigh dhá chúis a raibh bean Sheáin míshásta le Seán i dtús an ghearrscéil.', '(i) Luaigh dhá chúis'),
        ('ii', 'Cén toradh a bhí ar an suirbhé, de réir an eolais ar an bpáipéar?', '(ii) Cén toradh'),
        ('iii', 'Tabhair dhá phointe eolais faoi bhean an tsuirbhé.', '(iii) Tabhair dhá phointe eolais faoi bhean'),
        ('iv', 'Cén plean a bhí ag bean Sheáin dá leanbh féin agus í ag déanamh ionadaíochta do bhean an tsuirbhé?', '(iv) Cén plean'),
        ('v', 'Ar thaitin Seán leat sa ghearrscéal seo? Tabhair dhá fháth le do fhreagra.', '(v) Ar thaitin Seán')],
     '(a) Dís', '(b) Oisín i dTír na nÓg'),
    ('prose-2a-b', 'P-2A-b', 'b', 'Oisín i dTír na nÓg', 'irish-4-1', 'Freagair na ceisteanna thíos faoin scéal béaloidis Oisín i dTír na nÓg.', [
        ('i', 'Tabhair dhá phointe eolais faoin eachtra a tharla i nGleann na Smól.', '(i) Tabhair dhá phointe eolais faoin eachtra'),
        ('ii', 'Cén fáth ar tháinig Niamh Chinn Óir go hÉirinn?', '(ii) Cén fáth ar tháinig Niamh'),
        ('iii', 'Cén fáth a raibh brón ar Oisín agus é ag imeacht le Niamh Chinn Óir go Tír na nÓg?', '(iii) Cén fáth a raibh brón'),
        ('iv', 'Scríobh síos dhá phointe eolais faoin saol a bhí ag Oisín agus ag Niamh Chinn Óir i dTír na nÓg.', '(iv) Scríobh síos dhá phointe eolais faoin saol'),
        ('v', 'Tabhair dhá rud a thaispeáin go raibh Naomh Pádraig cineálta le hOisín i ndeireadh a shaoil.', '(v) Tabhair dhá rud a thaispeáin')],
     '(b) Oisín i dTír na nÓg', '(c) Freagair an cheist faoin scannán Cáca Milis'),
]
# 2A(c): one printed 25-mark question per text. (slug, atlas, title, topic, paper prompt, scheme start, scheme end)
PROSE_2A_C = [
    ('prose-2a-c', 'P-2A-c-caca-milis', 'Cáca Milis', 'irish-4-6',
     'Tabhair cuntas ar na rudaí a tharlaíonn sa charráiste traenach ón uair a théann an fear dall, Paul, ar bord na traenach go dtí deireadh an scannáin. (25 marc)',
     'Cáca Milis (25 marc)', 'nó An Lasair Choille (25 marc)'),
    ('prose-2a-c-an-lasair-choille', 'P-2A-c-an-lasair-choille', 'An Lasair Choille', 'irish-4-8',
     'Tabhair cuntas ar na rudaí a tharlaíonn ón uair a thagann Míoda isteach i dteach Mhicil go dtí deireadh an dráma. (25 marc)',
     'An Lasair Choille (25 marc)', 'Níl cead aon ábhar a bhaineann le Prós Ainmnithe'),
]
# Optional prose (2B): (slug, atlas, paper lines, scheme start, scheme end, [(id, label, marks, cut-before)], source title)
PROSE_2B = [
    ('prose-2b-a', 'P-2B-a', ['(a) Maidir le gearrscéal roghnach a ndearna tú staidéar air le linn do chúrsa, scríobh síos príomhthéama an ghearrscéil sin, dar leat. Tabhair cuntas ar na heachtraí is mó a léiríonn an príomhthéama sin sa ghearrscéal. (23 marc)',
                              'Ní mór teideal an ghearrscéil sin, mar aon le hainm an údair, a scríobh síos go cruinn. (2 mharc)'],
     '(a) Maidir le gearrscéal roghnach', '(b) Maidir le scéal béaloidis roghnach',
     [('priomhthema', 'An príomhthéama a lua', 1, None), ('eolas', 'Na heachtraí is mó', 22, 'Na heachtraí is mó'),
      ('teideal', 'Teideal + ainm an údair', 2, 'Ní mór teideal')], 'Gearrscéal roghnach'),
    ('prose-2b-b', 'P-2B-b', ['(b) Maidir le scéal béaloidis roghnach a ndearna tú staidéar air le linn do chúrsa, ainmnigh an phríomhphearsa (an príomhcharachtar) sa scéal sin. Tabhair cuntas ar na heachtraí is mó a tharlaíonn don duine sin ó thús go deireadh an scéil. (23 marc)',
                              'Ní mór teideal an scéil béaloidis sin a scríobh síos go cruinn. (2 mharc)'],
     '(b) Maidir le scéal béaloidis roghnach', '2B – PRÓS ROGHNACH',
     [('priomhphearsa', 'An phríomhphearsa a ainmniú', 1, None), ('eolas', 'Na heachtraí is mó', 22, 'Na heachtraí is mó'),
      ('teideal', 'Teideal an scéil béaloidis', 2, 'Ní mór teideal')], 'Scéal béaloidis roghnach'),
]
PROSE_2B_C_LINES = [
    '(c) Freagair an cheist thíos faoin scannán roghnach nó faoin dráma roghnach.',
    'Maidir le scannán roghnach a ndearna tú staidéar air le linn do chúrsa, tabhair cuntas ar na príomhimeachtaí (príomhrudaí) a tharlaíonn sa scannán sin. (23 marc)',
    'Ní mór teideal an scannáin sin, mar aon le hainm an scríbhneora, a scríobh síos go cruinn. (2 mharc)',
    'nó',
    'Maidir le dráma roghnach a ndearna tú staidéar air le linn do chúrsa, tabhair cuntas ar na príomhimeachtaí (príomhrudaí) a tharlaíonn sa dráma sin. (23 marc)',
    'Ní mór teideal an dráma sin, mar aon le hainm an scríbhneora, a scríobh síos go cruinn. (2 mharc)']
# Prescribed poetry (3A): (slug, atlas, page, title, [(label, paper prompt, marks, scheme cut)], scheme start, scheme end)
POETRY_3A = [
    ('poetry-3a-a', 'F-3A-a', 10, 'Colscaradh', [
        ('i', 'Tabhair dhá phointe eolais, i d’fhocail féin, faoin sórt saoil phósta a theastaíonn ón bhfear i véarsa a haon den dán.', 8, '(i) Tabhair dhá phointe eolais'),
        ('ii', 'Déan cur síos, i d’fhocail féin, ar dhá rud a theastaíonn ón mbean ina saol pósta i véarsa a dó.', 8, '(ii) Déan cur síos'),
        ('iii', 'Scríobh síos an mothúchán is láidre atá sa dán, dar leat.\nTabhair dhá shampla, i d’fhocail féin, den mhothúchán sin sa dán.', 9, '(iii) Scríobh síos an mothúchán')],
     '(a) Colscaradh', '(b) An Spailpín Fánach'),
    ('poetry-3a-b', 'F-3A-b', 11, 'An Spailpín Fánach', [
        ('i', '(a) Cad a dhéanann an spailpín ‘go moch ar maidin’ i véarsa a haon?\n(b) Cad a dhéanfaidh an spailpín nuair a éireoidh sé as obair an spailpín i véarsa a haon?\n'
              '(c) Céard a dhéanadh an spailpín i gCarraig na Siúire i véarsa a dó?\n(d) Cad a deir na daoine i nDurlas nuair a fheiceann siad an spailpín i véarsa a dó?', 8, '(i) (a) Cad a dhéanann'),
        ('ii', 'Scríobh síos dhá phointe eolais, i d’fhocail féin, faoi mhargadh na saoire i véarsa a trí.', 8, '(ii) Scríobh síos dhá phointe eolais'),
        ('iii', 'Cén saghas duine é an spailpín, dar leat?\nTabhair dhá fháth, i d’fhocail féin, le do fhreagra.', 9, '(iii) Cén saghas duine')],
     '(b) An Spailpín Fánach', '(c) Géibheann'),
    ('poetry-3a-c', 'F-3A-c', 12, 'Géibheann', [
        ('i', 'Scríobh síos, dhá phointe eolais, i d’fhocail féin, faoin gcineál saoil a bhí ag an ainmhí sna línte 1-8 den dán.', 8, '(i) Scríobh síos, dhá phointe eolais'),
        ('ii', 'Tabhair dhá phointe eolais, i d’fhocail féin, faoin íomhá (faoin bpictiúr) den ainmhí a fhaighimid sna línte 9-17 den dán.', 8, '(ii) Tabhair dhá phointe eolais'),
        ('iii', 'An maith leat an dán seo?\nTabhair dhá fháth, i d’fhocail féin, le do fhreagra.', 9, '(iii) An maith leat')],
     '(c) Géibheann', '3B – FILÍOCHT ROGHNACH'),
]
POEM_TOPICS = {'poetry-3a-a': 'irish-5-5', 'poetry-3a-b': 'irish-5-1', 'poetry-3a-c': 'irish-5-2'}
# 3A(b)(i) prints four 2-mark questions (a)–(d).
SLOTS_3A_B = [('a', 'Cad a dhéanann an spailpín ‘go moch ar maidin’ i véarsa a haon?', '(b) Cad a dhéanfaidh'),
              ('b', 'Cad a dhéanfaidh an spailpín nuair a éireoidh sé as obair an spailpín i véarsa a haon?', '(c) Céard a dhéanadh'),
              ('c', 'Céard a dhéanadh an spailpín i gCarraig na Siúire i véarsa a dó?', '(d) Cad a deir'),
              ('d', 'Cad a deir na daoine i nDurlas nuair a fheiceann siad an spailpín i véarsa a dó?', None)]
POETRY_3B = [
    ('poetry-3b-a', 'F-3B-a', [
        '(i) Maidir le dán nua-aimseartha roghnach a ndearna tú staidéar air le linn do chúrsa, scríobh síos i d’fhocail féin, príomhsmaointe an dáin. (9 marc)',
        '(ii) Cén íomhá (pictiúr) is mó a thaitníonn leat sa dán? Mínigh an íomhá (an pictiúr) sin i d’fhocail féin. (Is leor dhá phointe eolais.) (7 marc)',
        '(iii) Scríobh síos an mothúchán is láidre atá sa dán, dar leat. Tabhair dhá shampla, i d’fhocail féin, den mhothúchán sin sa dán. (7 marc)'],
     '(a) (i) Maidir le dán nua-aimseartha', '(b) (i) Maidir le dán seanaimseartha', ['(ii) Cén íomhá', '(iii) Scríobh síos an mothúchán', 'Ní mór teideal an dáin']),
    ('poetry-3b-b', 'F-3B-b', [
        '(i) Maidir le dán seanaimseartha roghnach (dán a cumadh sa tréimhse roimh 1850) a ndearna tú staidéar air le linn do chúrsa, scríobh síos príomhthéama an dáin sin, dar leat. Tabhair dhá phointe eolais, i d’fhocail féin, faoin bpríomhthéama sin sa dán. (9 marc)',
        '(ii) Roghnaigh íomhá (pictiúr) amháin a úsáideann an file sa dán seo. Scríobh síos dhá phointe eolais, i d’fhocail féin, faoin íomhá (faoin bpictiúr) sin. (7 marc)',
        '(iii) Cén t-atmaisféar atá sa dán seo, dar leat? Tabhair dhá shampla den atmaisféar sin sa dán. (7 marc)'],
     '(b) (i) Maidir le dán seanaimseartha', '(c) (i) Maidir le dán nua-aimseartha', ['(ii) Roghnaigh íomhá', '(iii) Cén t-atmaisféar', 'Ní mór teideal an dáin']),
    ('poetry-3b-c', 'F-3B-c', [
        '(i) Maidir le dán nua-aimseartha roghnach a ndearna tú staidéar air le linn do chúrsa, scríobh síos príomhthéama an dáin sin, dar leat. Tabhair dhá phointe eolais, i d’fhocail féin, faoin bpríomhthéama sin sa dán. (9 marc)',
        '(ii) Luaigh an íomhá (an pictiúr) is fearr leat sa dán. Mínigh an íomhá (an pictiúr) sin i d’fhocail féin. (Is leor dhá phointe eolais.) (7 marc)',
        '(iii) An maith leat an dán seo? Tabhair dhá fháth, i d’fhocail féin, le do fhreagra. (7 marc)'],
     '(c) (i) Maidir le dán nua-aimseartha', None, ['(ii) Luaigh an íomhá', '(iii) An maith leat', 'Ní mór teideal an dáin']),
]
TITLE_LINE = 'Ní mór teideal an dáin sin, mar aon le hainm an fhile, a scríobh síos go cruinn. (2 mharc)'

_MATERIAL = None


def material():
    global _MATERIAL
    if _MATERIAL:
        return _MATERIAL
    import fitz
    paper_path = ROOT / f'paper-trail-corpus/exampapers/2024/{FILE}.pdf'
    scheme_path = ROOT / f'paper-trail-corpus/markingschemes/2024/{SCHEME_FILE}.pdf'
    assert hashlib.sha256(paper_path.read_bytes()).hexdigest() == PAPER_SHA, 'Paper changed: repeat visual review'
    assert hashlib.sha256(scheme_path.read_bytes()).hexdigest() == SCHEME_SHA, 'Scheme changed: repeat visual review'
    paper, doc = fitz.open(paper_path), fitz.open(scheme_path)
    texts = [clean(p.get_text()) for p in paper]
    s = Scheme(doc, 14, 32)
    lang_read = '[Gaeilge lochtach: 0 - 5 a bhaint den iomlán a gnóthaíodh]'
    assert s.text.count(lang_read) == 2
    for letter, passage in PASSAGES.items():
        page_text = ' '.join(texts[p - 1] for p in passage['pages'])
        after = s.text.index(passage['start'])
        # Each passage prints its own two notes above Ceist 1; the page-14 copy sits beside the annotation key.
        notes = s.chunk('Nóta: Má tá dhá phointe eolais i gceist', '1. (a)', after)[0]
        assert notes.endswith('Nóta: Gearrfar pionós i ngeall ar iomarcaíocht.') and 'Siombailí' not in notes, notes
        passage['notes'] = notes
        resolved = []
        anchors = [p[3] for p in passage['parts']]
        for index, (q, part, prompt, anchor) in enumerate(passage['parts']):
            assert in_order(prompt, page_text), (letter, q, part)
            nxt = anchors[index + 1] if index + 1 < len(anchors) else lang_read
            chunk, spages = s.chunk(anchor, nxt, after)
            after = s.text.index(anchor, after) + 1
            assert '5 mharc' in chunk, (letter, q, part, chunk[:80])
            two = '3 mharc + 2 mharc' in chunk
            permitted = [0, 3, 5] if (two or '= 3 mharc' in chunk) else [0, 5]
            resolved.append((q, part, prompt, chunk, spages, two, permitted))
        passage['resolved'] = resolved
    lit_note = s.chunk('Nóta: Níl sé i gceist a chur in iúl go bhfuil na freagraí samplacha', 'Freagair do rogha dhá cheann')[0]
    lang_lit = '[Gaeilge lochtach: 0-4 a bhaint den iomlán a gnóthaíodh]'
    assert s.text.count(lang_lit) == 14, s.text.count(lang_lit)  # 2A 4 (incl. both 2A(c) texts), 2B 4 (incl. film and play), 3A 3, 3B 3
    for slug, atlas, letter, title, topic, intro, subs, start, end in PROSE_SUBS:
        for line in [intro, title] + [p for _, p, _ in subs]:
            assert in_order(line, texts[7]), (slug, line[:40])
    for slug, atlas, title, topic, prompt, start, end in PROSE_2A_C:
        assert in_order(prompt.removesuffix(' (25 marc)'), texts[7]) and in_order(FILM_OR_PLAY, texts[7]), slug
    for slug, atlas, lines, start, end, parts, title in PROSE_2B:
        for line in lines:
            assert in_order(re.sub(r' \((23|25) marc\)$| \(2 mharc\)$', '', line), texts[8]), (slug, line[:50])
    for line in PROSE_2B_C_LINES:
        assert in_order(line, texts[8]), line[:50]
    for slug, atlas, page, title, subs, start, end in POETRY_3A:
        for label, prompt, marks, cut in subs:
            assert in_order(prompt.replace('\n', ' '), texts[page - 1]), (slug, label)
    for slug, atlas, prompts, start, end, cuts in POETRY_3B:
        for line in prompts + [TITLE_LINE]:
            assert in_order(line, texts[12]), (slug, line[:50])
    assert comparable(texts[12]).count(comparable(TITLE_LINE)) == 3
    for line in (NO_PRESCRIBED_PROSE, CHOOSE, OPT_FILM_OR_PLAY):
        assert comparable(line) in comparable(texts[8]), line
    for line in (NO_PRESCRIBED_POETRY, CHOOSE, SAME_POEM):
        assert comparable(line) in comparable(texts[12]), line
    assert comparable(CHOOSE) in comparable(texts[7]) and comparable(CHOOSE_3A) in comparable(texts[9])
    _MATERIAL = dict(paper=paper, texts=texts, s=s, lang_read=lang_read, lit_note=lit_note, lang_lit=lang_lit,
                     decisions=selection_decisions(paper))
    return _MATERIAL


def deduction(m):
    return criterion('gaeilge-deduction', 'Gaeilge lochtach', 4, [m['lang_lit'] + ' — applied once to this whole 25-mark answer.'], 'quality', deduction=True)


def reading_note(m):
    return 'Scheme: “' + m['lang_read'] + '” — one deduction from each passage total (50), never inside a single part.'


def source(label, title, pages):
    return dict(kind='source-text', label=label, title=title, pages=pages, attribution=ATTRIBUTION, presentationNote=SOURCE_NOTE)


def sub_permitted(piece, marks):
    """“3 mharc + 2 mharc”: first correct point 3, second 2 (0/3/5); other sub-questions keep the full range."""
    return [0, 3, 5] if (marks == 5 and '3 mharc + 2 mharc' in piece) else None


def prose_pieces(m, slug, subs, start, end):
    whole, spages = m['s'].chunk(start, end)
    whole = before_language_note(whole)
    pieces = split_at(whole, [cut for _, _, cut in subs], slug)
    for (label, _, _), piece in zip(subs, pieces):
        assert '(5 mharc)' in piece, (slug, label)
    return pieces, sorted(set(spages) | {20})


def poem_pieces(m, slug, subs, start, end):
    whole, spages = m['s'].chunk(start, end)
    whole = before_language_note(whole)
    pieces = split_at(whole, [cut for _, _, _, cut in subs], slug)
    for (label, _, marks, _), piece in zip(subs, pieces):
        assert f'({marks} marc)' in piece or (label == 'i' and piece.count('(2 mharc)') == 4), (slug, label, piece[:60])
    return pieces, sorted(set(spages) | {27})


def apply_legacy_review(cards):
    """Lift the 2024 scheme onto the 22 retained legacy cards (IDs, totals and topics unchanged)."""
    m = material()
    by_id = {c['id']: c for c in cards}
    stamped = []

    def stamp(card_id, atlas, pages, scheme_pages, criteria, note, requirements, **extra):
        card = by_id[card_id]
        card.update(atlasQuestionId=atlas, reviewedAt=REVIEWED_AT, reviewedPaperPages=pages, schemeFileid=SCHEME_FILE,
                    schemePage=scheme_pages[0], schemePages=scheme_pages, criteria=criteria, markingGuideNote=note,
                    taskRequirements=requirements, **extra)
        assert sum(c['maxMarks'] for c in criteria if c['kind'] == 'award') == card['totalMarks'], card_id
        assert not any('Siombailí Anótála' in g for c in criteria for g in c['guidance']), card_id
        stamped.append(card_id)
        return card

    # Reading: the frozen Atlas identities 1–5 (A) and 6–10 (B) are the whole questions.
    for letter, passage in PASSAGES.items():
        by_q = {}
        for q, part, prompt, chunk, spages, two, permitted in passage['resolved']:
            by_q.setdefault(q, []).append((part, chunk, spages, permitted))
        for q, parts in by_q.items():
            card_id = f'irish-2024-ol-p2-reading-{letter.lower()}-q{q}'
            assert in_order(by_id[card_id]['questionText'], ' '.join(m['texts'][p - 1] for p in passage['pages'])), card_id
            crits = [criterion(part, f'({part}) Freagra', 5, [chunk, passage['notes']], permitted=permitted) for part, chunk, _, permitted in parts]
            stamp(card_id, str(int(q) + (5 if letter == 'B' else 0)), passage['pages'], sorted({p for *_, sp, _ in parts for p in sp}), crits,
                  'Retained complete printed question: (a) 5 + (b) 5, each scored separately at its SEC allocation. ' + reading_note(m),
                  READING_WHOLE)

    note = m['lit_note']
    for slug, atlas, letter, title, topic, intro, subs, start, end in PROSE_SUBS:
        assert by_id[f'irish-2024-ol-p2-{slug}']['topicId'] == topic, slug
        pieces, spages = prose_pieces(m, slug, subs, start, end)
        crits = [criterion(f'eolas-{label}', f'({label}) Eolas', 5, [piece, note], 'indicative', permitted=sub_permitted(piece, 5))
                 for (label, _, _), piece in zip(subs, pieces)]
        stamp(f'irish-2024-ol-p2-{slug}', atlas, [8], spages, crits + [deduction(m)],
              'One complete SEC response: five printed sub-questions at 5 each, then the 0–4 Gaeilge deduction once. '
              'The sample answers are indicative rather than exhaustive.',
              [CHOOSE] + LIT, questionText=HEAD2A + f'\n({letter}) {intro}\n{title}\n' + '\n'.join(f'({l}) {p}' for l, p, _ in subs) + '\n(25 marc)',
              sourceMaterial=source('Prós Ainmnithe', title, [8]))

    slug, atlas, title, topic, prompt, start, end = PROSE_2A_C[0]
    assert by_id[f'irish-2024-ol-p2-{slug}']['topicId'] == topic, slug
    chunk, spages = m['s'].chunk(start, end)
    assert '5 phointe eolais agus 5 mharc ar gach pointe eolais' in chunk, slug
    stamp(f'irish-2024-ol-p2-{slug}', atlas, [8], sorted(set(spages) | {20}),
          [criterion('eolas', 'Eolas', 25, [before_language_note(chunk), note], 'indicative'), deduction(m)],
          'One complete SEC response: five points at 5 (2 for the bare point + 3 for development); the 0–4 Gaeilge deduction applies once. '
          'The sample points are indicative rather than exhaustive. 2A(c) offers Cáca Milis or An Lasair Choille; this card is Cáca Milis.',
          [CHOOSE, FILM_OR_PLAY] + LIT[1:], questionText=HEAD2A + f'\n(c) {FILM_OR_PLAY}\n{title}\n{prompt}',
          sourceMaterial=source('Prós Ainmnithe', title, [8]))

    for slug, atlas, lines, start, end, parts, title in PROSE_2B:
        chunk, spages = m['s'].chunk(start, end)
        chunk = before_language_note(chunk)
        cuts = [0] + [chunk.index(cut) for _, _, _, cut in parts[1:]]
        pieces = [chunk[a:b].strip() for a, b in zip(cuts, cuts[1:] + [len(chunk)])]
        # Naming, theme and account depend on the candidate's chosen text (indicative); the title marks are exact.
        crits = [criterion(cid, label, marks, [piece], 'exact' if cid == 'teideal' else 'indicative',
                           permitted=None if cid == 'eolas' else sorted({0, marks} | {int(v) for v in re.findall(r'= (\d) mharc', piece)}))
                 for (cid, label, marks, _), piece in zip(parts, pieces)]
        assert crits[-1]['guidance'][0].endswith('(2 mharc)'), slug
        stamp(f'irish-2024-ol-p2-{slug}', atlas, [9], spages, crits + [deduction(m)],
              'One complete SEC response: ' + ', '.join(f'{label} {marks}' for _, label, marks, _ in parts) +
              ', then the 0–4 Gaeilge deduction once. The optional text is open content chosen by the candidate; the scheme prints no sample '
              'points for it, so its points are judged on merit against these allocations (indicative rather than exhaustive).',
              [CHOOSE, NO_PRESCRIBED_PROSE] + LIT[1:], questionText=HEAD2B + '\n' + '\n'.join(lines),
              sourceMaterial=source('Prós Roghnach', title, [9]))

    # 2B(c): an optional film or an optional play, one grid and one topic, so one card carries both printed alternatives.
    chunk, spages = m['s'].chunk('(c) Freagair an cheist thíos faoin scannán roghnach', '3A – FILÍOCHT AINMNITHE')
    film, play = chunk.split(' nó Maidir le dráma roghnach', 1)
    play = 'Maidir le dráma roghnach' + play
    halves = [before_language_note(film), before_language_note(play)]
    accounts = [h[:h.rindex('Ní mór teideal')].strip() for h in halves]
    titles = [h[h.rindex('Ní mór teideal'):].strip() for h in halves]
    assert all('Príomhimeachtaí (príomhrudaí) = 23 marc' in a for a in accounts) and all(t.endswith('(2 mharc)') for t in titles)
    stamp('irish-2024-ol-p2-prose-2b-c', 'P-2B-c', [9], spages,
          [criterion('eolas', 'Príomhimeachtaí', 23, accounts, 'indicative'),
           criterion('teideal', 'Teideal + ainm an scríbhneora', 2, titles, 'exact', permitted=[0, 1, 2]), deduction(m)],
          'One complete SEC response about an optional film or an optional play (the same scheme for both): 23 for five points '
          '(5, 5, 5, 4, 4) and 2 for the exact title and writer, then the 0–4 Gaeilge deduction once. The text is open content '
          'chosen by the candidate (indicative rather than exhaustive).',
          [CHOOSE, NO_PRESCRIBED_PROSE, OPT_FILM_OR_PLAY] + LIT[1:], questionText=HEAD2B + '\n' + '\n'.join(PROSE_2B_C_LINES),
          sourceMaterial=source('Prós Roghnach', 'Scannán nó dráma roghnach', [9]))

    for slug, atlas, page, title, subs, start, end in POETRY_3A:
        assert by_id[f'irish-2024-ol-p2-{slug}']['topicId'] == POEM_TOPICS[slug], slug
        pieces, spages = poem_pieces(m, slug, subs, start, end)
        crits = [criterion(f'eolas-{label}', f'({label}) Eolas', marks, [piece, note], 'indicative',
                           permitted=[0, 2, 4, 6, 8] if (slug, label) == ('poetry-3a-b', 'i') else None)
                 for (label, _, marks, _), piece in zip(subs, pieces)]
        prompt = '\n'.join(f'({label}) {p}' + f' ({marks} marc)' for label, p, marks, _ in subs)
        stamp(f'irish-2024-ol-p2-{slug}', atlas, [page], spages, crits + [deduction(m)],
              'One complete SEC response: (i) 8, (ii) 8, (iii) 9 at their printed tariffs, then the 0–4 Gaeilge deduction once. '
              'The sample points are indicative rather than exhaustive; lines lifted straight from the poem without the candidate’s own words earn 2 + 2.',
              [CHOOSE_3A] + LIT, questionText=HEAD3A + f'\n({atlas[-1]}) {title}\n' + prompt,
              sourceMaterial=source('Filíocht Ainmnithe', title, [page]))

    for slug, atlas, prompts, start, end, cuts in POETRY_3B:
        chunk, spages = m['s'].chunk(start, end, m['s'].text.index('⟦31⟧'))
        chunk = before_language_note(chunk)
        idx = [0] + [chunk.index(cut) for cut in cuts]
        pieces = [chunk[a:b].strip() for a, b in zip(idx, idx[1:] + [len(chunk)])]
        for piece, cap in zip(pieces, ['(9 marc)', '(7 marc)', '(7 marc)', '(2 mharc)']):
            assert cap in piece, (slug, cap)
        crits = [criterion('eolas-i', '(i) Eolas', 9, [pieces[0]], 'indicative'), criterion('eolas-ii', '(ii) Eolas', 7, [pieces[1]], 'indicative'),
                 criterion('eolas-iii', '(iii) Eolas', 7, [pieces[2]], 'indicative'),
                 criterion('teideal', 'Teideal + ainm an fhile', 2, [pieces[3]], 'exact')]
        stamp(f'irish-2024-ol-p2-{slug}', atlas, [13], spages, crits + [deduction(m)],
              'One complete SEC response: (i) 9, (ii) 7, (iii) 7, poem and poet 2, then the 0–4 Gaeilge deduction once. '
              'The optional poem is open content; the same poem may not be used twice. The printed allocations are judged on merit '
              '(indicative rather than exhaustive).',
              [CHOOSE, NO_PRESCRIBED_POETRY, SAME_POEM] + LIT, questionText=HEAD3B + f'\n({atlas[-1]}) ' + '\n'.join(prompts + [TITLE_LINE]),
              sourceMaterial=source('Filíocht Roghnach', f'3B({atlas[-1]}) · Dán roghnach', [13]))
    assert len(stamped) == 22
    return cards, stamped


def build():
    m = material()
    cards = []

    def add(key, slug, ref, prompt, topic, pages, scheme_pages, criteria, requirements, note, src):
        cards.append(dict(
            id=f'irish-2024-ol-p2-{slug}', year=2024, level='ordinary', paper=2, section='2',
            atlasQuestionId=key, questionRef=f'2024 OL Paper 2 {ref}', questionText=prompt,
            totalMarks=sum(c['maxMarks'] for c in criteria if c['kind'] == 'award'), topicId=topic,
            conceptId=f'irish-ol-p2-{slug}', paperFileid=FILE, schemeFileid=SCHEME_FILE,
            schemePage=scheme_pages[0], schemePages=scheme_pages, reviewedAt=REVIEWED_AT, reviewedPaperPages=pages,
            taskRequirements=requirements, criteria=criteria, markingGuideNote=note, sourceMaterial=src))

    for letter, passage in PASSAGES.items():
        src = source(f'Léamhthuiscint {letter}', passage['title'], passage['pages'])
        for q, part, prompt, chunk, spages, two, permitted in passage['resolved']:
            add(f'R-{letter}-{q}-{part}', f'reading-{letter.lower()}-q{q}-{part}', f'Léamhthuiscint {letter} · Ceist {q}({part})',
                f'{q}{prompt}', passage['topic'], passage['pages'], spages,
                [criterion(part, 'Freagra', 5, [chunk, passage['notes']], permitted=permitted)], READING_PART,
                'SEC allocation for this part' + (': first correct point 3, second 2 (0/3/5).' if two else '.') + ' ' + reading_note(m), src)

    note, lang = m['lit_note'], m['lang_lit']
    sub_note = f'One printed sub-question at its published tariff. Scheme: “{lang}” applies to the whole 25-mark answer, never inside one sub-question.'
    for slug, atlas, letter, title, topic, intro, subs, start, end in PROSE_SUBS:
        pieces, spages = prose_pieces(m, slug, subs, start, end)
        src = source('Prós Ainmnithe', title, [8])
        for (label, prompt, _), piece in zip(subs, pieces):
            add(f'{atlas}-{label}', f'{slug}-{label}', f'Prós 2A({letter}) · {title} · ({label})', HEAD2A + f'\n({letter}) {intro}\n{title}\n({label}) {prompt} (5 marc)',
                topic, [8], spages, [criterion('eolas', 'Eolas', 5, [piece, note], 'indicative', permitted=sub_permitted(piece, 5))],
                [CHOOSE] + LIT[1:], sub_note, src)

    slug, atlas, title, topic, prompt, start, end = PROSE_2A_C[1]
    chunk, spages = m['s'].chunk(start, end)
    assert '5 phointe eolais agus 5 mharc ar gach pointe eolais' in chunk, slug
    add(atlas, slug, f'Prós 2A(c) · {title}', HEAD2A + f'\n(c) {FILM_OR_PLAY}\n{title}\n{prompt}', topic, [8], sorted(set(spages) | {20}),
        [criterion('eolas', 'Eolas', 25, [before_language_note(chunk), note], 'indicative'), deduction(m)],
        [CHOOSE, FILM_OR_PLAY] + LIT[1:],
        'One complete SEC response: five points at 5 (2 for the bare point + 3 for development); the 0–4 Gaeilge deduction applies once. '
        'The sample points are indicative rather than exhaustive. 2A(c) offers Cáca Milis or An Lasair Choille; this card is An Lasair Choille.',
        source('Prós Ainmnithe', title, [8]))

    for slug, atlas, page, title, subs, start, end in POETRY_3A:
        pieces, spages = poem_pieces(m, slug, subs, start, end)
        topic = POEM_TOPICS[slug]
        src = source('Filíocht Ainmnithe', title, [page])
        head = HEAD3A + f'\n({atlas[-1]}) {title}\n'
        for (label, prompt, marks, _), piece in zip(subs, pieces):
            add(f'{atlas}-{label}', f'{slug}-{label}', f'Filíocht 3A({atlas[-1]}) · {title} · ({label})', head + f'({label}) {prompt} ({marks} marc)',
                topic, [page], spages,
                [criterion('eolas', 'Eolas', marks, [piece, note], 'indicative', permitted=[0, 2, 4, 6, 8] if (slug, label) == ('poetry-3a-b', 'i') else None)],
                [CHOOSE_3A] + LIT[1:], sub_note, src)
            if (slug, label) == ('poetry-3a-b', 'i'):
                for sub, question, nxt in SLOTS_3A_B:
                    start_at = piece.index(question)
                    slot = piece[start_at:piece.index(nxt, start_at) if nxt else len(piece)].strip()
                    assert 'Freagraí:' in slot and '(2 mharc)' in slot, (sub, slot[:60])
                    add(f'{atlas}-i-{sub}', f'{slug}-i-{sub}', f'Filíocht 3A(b) · {title} · (i)({sub})', head + f'(i) ({sub}) {question}',
                        topic, [page], spages, [criterion('eolas', 'Freagra', 2, [slot], 'exact', permitted=[0, 2])], [CHOOSE_3A] + LIT[1:],
                        f'One printed 2-mark question inside 3A(b)(i). Scheme: “{lang}” applies to the whole 25-mark answer.', src)

    assert len(cards) == 44 and len({c['id'] for c in cards}) == 44 and len({c['atlasQuestionId'] for c in cards}) == 44
    # Boxed page headings inside lifted keys (irish_furniture.py): exact strings only, count pinned.
    from irish_furniture import strip_card
    assert sum(strip_card(card) for card in cards) == 2
    for card in cards:
        for c in card['criteria']:
            assert c['guidance'] and all(not re.search('[-]|Siombailí Anótála', g) for g in c['guidance']), (card['id'], c['id'])
    sr = json.loads(SOURCE_REVIEW.read_text())
    legacy = ([f'irish-2024-ol-p2-reading-{l}-q{q}' for l in 'ab' for q in range(1, 6)]
              + [f'irish-2024-ol-p2-prose-{k}' for k in ['2a-a', '2a-b', '2a-c', '2b-a', '2b-b', '2b-c']]
              + [f'irish-2024-ol-p2-poetry-{k}' for k in ['3a-a', '3a-b', '3a-c', '3b-a', '3b-b', '3b-c']])
    review = dict(year=2024, level='ordinary', paperFileid=FILE + '.pdf', schemeFileid=SCHEME_FILE + '.pdf',
                  paperSha256=PAPER_SHA, schemeSha256=SCHEME_SHA,
                  reviewedPaperPages=list(range(1, 17)), reviewedSchemePages=sr['reviewedSchemePages'], schemeScope=sr['schemeScope'],
                  reviewDate=REVIEWED_AT, status='reviewed', fullPaperAndApplicableSchemeVisualSweep=True, selectionDecisions=m['decisions'],
                  practiceCardIds=[c['id'] for c in cards], legacyCardIds=legacy, readingWholeCardIds=legacy[:10],
                  examStructure=dict(readingA=50, readingB=50, prose=50, poetry=50, total=200),
                  nonPoolDecisions=sr['nonPoolDecisions'], openIssues=[], caveats=sr['sourceFindings'],
                  choicePolicy=('Choice is not a route: each printed option of 2A, 2B, 3A and 3B is one card carrying the choose-two instruction; '
                                'no combination cards. Inside 2A(c) the two prescribed texts (different topics) are separate cards; inside 2B(c) '
                                'the optional film and play share one grid and topic and stay one card.'),
                  boundaries=('10 retained whole reading questions with their 20 published parts; 12 retained literature options plus the An Lasair '
                              'Choille option of 2A(c); the 10 printed 2A(a)/(b) sub-questions, the 9 prescribed-poetry sub-questions and the '
                              '4 printed 3A(b)(i) questions.'))
    return dict(review=review, cards=cards)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    data = build()
    content = json.dumps(data, ensure_ascii=False, indent=2) + '\n'
    if args.check:
        assert OUT.exists() and OUT.read_text() == content, f'Stale output: {OUT}'
    else:
        OUT.write_text(content)
    print(f"Irish Ordinary 2024 Paper 2: {len(data['cards'])} added practice cards (+22 retained legacy cards); the archive remains incomplete.")


if __name__ == '__main__':
    main()
