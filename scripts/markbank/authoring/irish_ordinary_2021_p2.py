#!/usr/bin/env python3
"""Reviewed 2021 Ordinary Paper 2 (Léamhthuiscint agus Litríocht).

Paper PDF 1–16 and the Paper 2 pages of the combined LC001GLP000IV scheme (PDF 12–30,
plus 31–32 modified marking) reviewed on 2026-11-04. Counts are assertions, not
corpus-completeness proof. Same method as irish_ordinary_2023_p2.py.

The 2021 paper was adjusted (150 marks): both reading passages (100) and two literature
questions at 25 from Roinn na Litríochta (50), chosen as the paper prints on page 3.

The legacy generator already ships 22 cards for this component: the ten whole reading
questions and the twelve literature options. Their IDs, totals and topics are kept.
`apply_legacy_review` (called by irish_cards.py) joins them to Atlas and replaces their
marking with the lifted 2021 scheme. `build` adds every reading part (20), the five
printed sub-questions of 2A(a) Hurlamaboc, every prescribed-poetry sub-question (9),
and the An Lasair Choille option of 2A(b).

Choice is not a route: the literature instruction sits in each option's task
requirements; no card combines two options. Inside 2A(b) the film Cáca Milis and the
play An Lasair Choille are different syllabus texts with their own sample answers, so
each keeps its own card (the legacy 2A(b) card is Cáca Milis). Inside 2B(b) the optional
film and optional play share one scheme, so they stay one card with both alternatives.

The scheme's text layer stores each page's boxed heading (“CEIST 1 (A + B) - LÉAMHTHUISCINT
- 100 marc”, “A – (50 marc)”, “2B – PRÓS ROGHNACH” …) at the end or head of the page;
`Scheme` removes them so no heading lands inside an answer key.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import re
from pathlib import Path
from irish_lifted import scheme_words_in, symbol_text

ROOT = Path(__file__).resolve().parents[3]
FILE = 'LC001GLP200IV'
SCHEME_FILE = 'LC001GLP000IV'
OUT = ROOT / 'components/MarkBank/cards/irish/ordinary-2021-p2-authored.json'
SOURCE_REVIEW = ROOT / 'scripts/markbank/authored/irish-ordinary-2021-p2-source-review.json'
REVIEWED_AT = '2026-11-04'
PAPER_SHA = '8f89837075781146bb6304ee1b90c150ea2e2bbead4a049b461c4e94544266c1'
SCHEME_SHA = 'b66d6097fa351c6038776c1e7d8c41ca2f5b6597aa131c8dc7a7d6272697cf9c'
DIRECTIVE = re.compile(r'rogha|roghna|Freagair|Luaigh|Ainmnigh|\bnó\b|dhá phointe|dhá rud|dhá bh|dhá dh|dhá ch|dhá fh|dhá th|dhá ph|dhá sh|'
                       r'\ban dá\b|ceann amháin|pointe amháin|amháin|\bdhá\b', re.I)
SOURCE_NOTE = 'Shown page-for-page from the official examination paper; swipe to move between pages.'
ATTRIBUTION = '© State Examinations Commission.'
# Boxed page headings, extracted after (or before) each page's body.
FURNITURE = re.compile(r'\s*(?:CEIST 1 \(A \+ B\) - LÉAMHTHUISCINT - 100 marc|[AB] – \(50 marc\)|'
                       r'[23][AB] – (?:PRÓS|FILÍOCHT) (?:AINMNITHE|ROGHNACH))\s*')


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
            body, n = FURNITURE.subn(' ', body)
            self.removed += n
            self.text += f' ⟦{p}⟧ ' + clean(body)

    def chunk(self, start, end=None, after=0):
        i = self.text.index(start, after)
        j = self.text.index(end, i + len(start)) if end else len(self.text)
        raw = self.text[i:j]
        pages = {int(re.findall(r'⟦(\d+)⟧', self.text[:i])[-1])}
        pages |= {int(m.group(1)) for m in re.finditer(r'⟦(\d+)⟧([^⟦]*)', raw) if clean(m.group(2)) not in ('', 'nó')}
        return clean(re.sub(r'⟦\d+⟧', ' ', raw)), sorted(pages)

    def page(self, number):
        return self.text.index(f'⟦{number}⟧')


def before_language_note(text):
    return re.split(r'\[\s*Gaeilge lochtach', text)[0].strip()


def split_at(text, cuts, slug):
    idx = [text.index(cut) for cut in cuts]
    assert idx == sorted(idx), slug
    return [text[a:b].strip() for a, b in zip(idx, idx[1:] + [len(text)])]


PENALTY = 'Nóta: Gearrfar pionós i ngeall ar iomarcaíocht. Léireofar'
# (q, part, paper prompt, scheme anchor)
PASSAGES = {
    'A': dict(title='An Nua-theicneolaíocht agus an Ghaeilge', pages=[4, 5], topic='irish-3-0', start=12, notes_end='An Nua-theicneolaíocht agus an Ghaeilge 1. (a)', parts=[
        ('1', 'a', '(a) Tabhair dhá úsáid a bhaintear as an idirlíon. (Alt 1)', '1. (a) Tabhair dhá úsáid'),
        ('1', 'b', '(b) Scríobh síos dhá bhuntáiste a bhaineann leis an bhfón cliste. (Alt 1)', '(b) Scríobh síos dhá bhuntáiste'),
        ('2', 'a', '(a) Scríobh síos dhá rud a dhéanann daoine ar na líonraí sóisialta éagsúla. (Alt 2)', '2. (a) Scríobh síos dhá rud a dhéanann'),
        ('2', 'b', '(b) Luaigh dhá phíosa eolais faoi YouTube. (Alt 2)', '(b) Luaigh dhá phíosa eolais faoi YouTube'),
        ('3', 'a', '(a) Cad is féidir le lucht féachana TG4 ar fud an domhain a fháil ar Sheinnteoir TG4? (Alt 3)', '3. (a) Cad is féidir le lucht féachana'),
        ('3', 'b', '(b) Conas atá a fhios againn go bhfuil www.tuairisc.ie ag dul ó neart go neart? (Alt 3)', '(b) Conas atá a fhios againn'),
        ('4', 'a', '(a) Scríobh síos dhá úsáid a bhaineann eagraíochtaí Gaeilge as na meáin shóisialta. (Alt 4)', '4. (a) Scríobh síos dhá úsáid a bhaineann'),
        ('4', 'b', '(b) Cén fáth a n‐eagraíonn Conradh na Gaeilge Lá na Meán Sóisialta mar chuid de Sheachtain na Gaeilge? (Alt 4)', '(b) Cén fáth a n-eagraíonn'),
        ('5', 'a', '(a) Scríobh síos dhá rud atá le fáil ar shuíomh an fhoclóra Béarla‐Gaeilge, www.foclóir.ie. (Alt 5)', '5. (a) Scríobh síos dhá rud atá le fáil'),
        ('5', 'b', '(b) Cad atá ar fáil ar an suíomh gréasáin www.dúchas.ie? (Alt 5)', '(b) Cad atá ar fáil ar an suíomh')]),
    'B': dict(title='Scéalta ó shaol an spóirt in 2020', pages=[6, 7], topic='irish-3-1', start=15, notes_end='1. (a)', parts=[
        ('1', 'a', '(a) Scríobh síos an dá ghaisce a rinne an rothaí proifisiúnta Éireannach, Sam Bennett, sa rás mór rothaíochta, an Tour de France, Dé Domhnaigh, 20 Meán Fómhair 2020. (Alt 1)', '1. (a) Scríobh síos an dá ghaisce'),
        ('1', 'b', '(b) Tabhair dhá chúis mhórtais a bhí ag an réalta spóirt, Katie Taylor, in 2020. (Alt 1)', '(b) Tabhair dhá chúis mhórtais'),
        ('2', 'a', '(a) Luaigh dhá phíosa eolais faoin gcaoi ar éirigh le foireann sacair Phoblacht na hÉireann i gCorn an Domhain i 1990. (Alt 2)', '2. (a) Luaigh dhá phíosa eolais faoin gcaoi'),
        ('2', 'b', '(b) Scríobh síos an dá chúis ar moladh Caoimhín Kelleher, cúl báire fhoireann sacair Learphoill, i ndiaidh an chluiche in aghaidh Ajax. (Alt 2)', '(b) Scríobh síos an dá chúis ar moladh'),
        ('3', 'a', '(a) Cén gaisce a rinne foireann sinsir Bhaile Átha Cliath i bpeil na bhfear i mí na Nollag seo caite? (Alt 3)', '3. (a) Cén gaisce a rinne'),
        ('3', 'b', '(b) Cén fáth a bhfuil ainm an iarthráchtaire, Micheál Ó Muircheartaigh, luaite i Leabhar Curiarrachtaí Guinness? (Alt 3)', '(b) Cén fáth a bhfuil ainm an iarthráchtaire'),
        ('4', 'a', '(a) Cad a tharla i bPáirc an Chrócaigh ag cluiche peile idir Tiobraid Árann agus Baile Átha Cliath ar an 21 Samhain 1920? (Alt 4)', '4. (a) Cad a tharla i bPáirc an Chrócaigh'),
        ('4', 'b', '(b) Scríobh síos dhá rud a tharla ag an searmanas cuimhneacháin i bPáirc an Chrócaigh ar an 21 Samhain anuraidh. (Alt 4)', '(b) Scríobh síos dhá rud a tharla ag an searmanas'),
        ('5', 'a', '(a) Tabhair dhá rud atá ar fáil san iris nua Cuaille a sheol Cumann Lúthchleas Gael. (Alt 5)', '5. (a) Tabhair dhá rud atá ar fáil san iris'),
        ('5', 'b', '(b) Luaigh dhá phíosa eolais a tugadh faoi na laochra spóirt sa tsraith Laochra Gael ar TG4. (Alt 5)', '(b) Luaigh dhá phíosa eolais a tugadh')]),
}

# The literature choice the paper prints on page 3, and the restrictions it prints above 2B (page 10) and 3B (page 14).
CHOOSE = 'Freagair dhá cheist as an roinn seo.'
NO_PRESCRIBED_PROSE = 'Níl cead aon ábhar a bhaineann le Prós Ainmnithe a úsáid sna freagraí ar an bPrós Roghnach.'
NO_PRESCRIBED_POETRY = 'Níl cead aon ábhar a bhaineann le Filíocht Ainmnithe a úsáid sna freagraí ar an bhFilíocht Roghnach.'
FILM_OR_PLAY = 'Freagair an cheist thíos faoin scannán Cáca Milis nó faoin dráma An Lasair Choille.'
OPT_FILM_OR_PLAY = 'Freagair an cheist thíos faoin scannán roghnach nó faoin dráma roghnach.'
LIT = ['Freagair gach fochuid atá priontáilte sa rogha seo.', 'Úsáid tagairtí cruinne agus ábhartha don téacs.']
READING_PART = ['Léigh an sliocht iomlán a ghabhann leis an gceist. Freagair an chuid atá luaite ar an gcárta.', 'Úsáid an t-alt a luaitear.']
READING_WHOLE = ['Léigh an sliocht oifigiúil a ghabhann leis an gceist.', 'Freagair gach fochuid agus cloígh leis an alt a luaitear.']

HURLAMABOC = ('prose-2a-a', 'P-2A-a', 'Hurlamaboc', 'irish-4-5', 'Freagair na ceisteanna thíos faoin ngiota as an úrscéal Hurlamaboc.', [
    ('i', 'Cén fáth a mbeidh cóisir i dteach Albright?', '(i) Cén fáth a mbeidh cóisir'),
    ('ii', 'Déan cur síos ar na hullmhúcháin atá déanta ag Lisín don chóisir.', '(ii) Déan cur síos ar na hullmhúcháin'),
    ('iii', 'Tabhair dhá phointe eolais faoi na mná eile ar Ascaill na Fuinseoige.', '(iii) Tabhair dhá phointe eolais'),
    ('iv', 'Scríobh síos dhá phointe eolais faoi Phól, fear céile Lisín.', '(iv) Scríobh síos dhá phointe eolais'),
    ('v', '‘Bean ghnóthach ba ea Lisín agus bhí a lán rudaí eile ar siúl aici taobh amuigh den teach.’\nScríobh síos dhá phointe eolais faoin gcuid sin de shaol Lisín.', '(v) ‘Bean ghnóthach')],
    '(a) Hurlamaboc (25 marc)', '(b) Cáca Milis (25 marc)')
# 2A(b): one printed 25-mark question per text. (slug, atlas, title, topic, paper prompt, scheme start, scheme end)
PROSE_2A_B = [
    ('prose-2a-b', 'P-2A-b-caca-milis', 'Cáca Milis', 'irish-4-6',
     'Tabhair cuntas ar na rudaí a tharlaíonn ón uair a shuíonn an fear dall, Paul, os comhair Catherine sa charráiste traenach go dtí deireadh an scannáin. (25 marc)',
     '(b) Cáca Milis (25 marc)', 'nó An Lasair Choille (25 marc)'),
    ('prose-2a-b-an-lasair-choille', 'P-2A-b-an-lasair-choille', 'An Lasair Choille', 'irish-4-8',
     'Tabhair cuntas ar an gcineál saoil atá ag an bhfear óg, Séamas, agus é ag tabhairt aire don seanfhear, Micil, sa dráma An Lasair Choille. (25 marc)',
     'nó An Lasair Choille (25 marc)', '(c) Dís (25 marc)'),
]
DIS = ('prose-2a-c', 'P-2A-c', 'Dís', 'irish-4-4', 'Freagair an cheist thíos faoin ngearrscéal Dís.',
       '‘’Sheáin?...Cuir síos an páipéar agus bí ag caint liom,’ arsa a bhean chéile leis.\nDéan cur síos ar an gcomhrá idir Seán agus a bhean chéile an tráthnóna sin sa ghearrscéal Dís. (25 marc)',
       '(c) Dís (25 marc)', 'Níl cead aon ábhar a bhaineann le Prós Ainmnithe')
# Optional prose (2B): (slug, atlas, paper lines, scheme start, scheme end, [(id, label, marks, cut-before)], source title)
PROSE_2B = [
    ('prose-2b-a', 'P-2B-a', ['(a) Maidir le giota as úrscéal roghnach a ndearna tú staidéar air le linn do chúrsa, ainmnigh an phríomhphearsa (an príomhcharachtar) sa ghiota sin. Tabhair cuntas ar na heachtraí is mó a tharlaíonn don duine sin sa ghiota. (23 marc)',
                              'Ní mór teideal an úrscéil sin, mar aon le hainm an údair, a scríobh síos go cruinn. (2 mharc)'],
     '(a) Maidir le giota as úrscéal roghnach', '(b) Freagair an cheist thíos faoin scannán roghnach',
     [('priomhphearsa', 'An phríomhphearsa a ainmniú', 1, None), ('eolas', 'Na heachtraí is mó', 22, 'Na heachtraí is mó a tharlaíonn don duine sin ='),
      ('teideal', 'Teideal + ainm an údair', 2, 'Ní mór teideal')], 'Giota as úrscéal roghnach'),
    ('prose-2b-c', 'P-2B-c', ['(c) Maidir le gearrscéal roghnach a ndearna tú staidéar air le linn do chúrsa, scríobh síos príomhthéama an ghearrscéil sin, dar leat. Tabhair cuntas ar na heachtraí is mó a léiríonn an príomhthéama sin sa ghearrscéal. (23 marc)',
                              'Ní mór teideal an ghearrscéil sin, mar aon le hainm an údair, a scríobh síos go cruinn. (2 mharc)'],
     '(c) Maidir le gearrscéal roghnach', None,
     [('priomhthema', 'An príomhthéama a lua', 1, None), ('eolas', 'Na heachtraí is mó', 22, 'Na heachtraí is mó a léiríonn an príomhthéama sin ='),
      ('teideal', 'Teideal + ainm an údair', 2, 'Ní mór teideal')], 'Gearrscéal roghnach'),
]
PROSE_2B_B_LINES = [
    '(b) Freagair an cheist thíos faoin scannán roghnach nó faoin dráma roghnach.',
    'Maidir le scannán roghnach a ndearna tú staidéar air le linn do chúrsa, tabhair cuntas ar na príomhimeachtaí (príomhrudaí) a tharlaíonn sa scannán sin. (23 marc)',
    'Ní mór teideal an scannáin sin, mar aon le hainm an scríbhneora, a scríobh síos go cruinn. (2 mharc)',
    'nó',
    'Maidir le dráma roghnach a ndearna tú staidéar air le linn do chúrsa, tabhair cuntas ar na príomhimeachtaí (príomhrudaí) a tharlaíonn sa dráma sin. (23 marc)',
    'Ní mór teideal an dráma sin, mar aon le hainm an scríbhneora, a scríobh síos go cruinn. (2 mharc)']
# Prescribed poetry (3A): (slug, atlas, page, title, [(label, paper prompt, marks, scheme cut)], scheme start, scheme end)
POETRY_3A = [
    ('poetry-3a-a', 'F-3A-a', 11, 'An Spailpín Fánach', [
        ('i', 'Déan cur síos, i d’fhocail féin, ar an íomhá (ar an bpictiúr) den spailpín a thugtar dúinn i véarsa a haon den dán. (Is leor dhá phointe eolais.)', 8, '(i) Déan cur síos'),
        ('ii', 'Cén t‐eolas a thugtar dúinn faoi shaol an spailpín i véarsa a dó?\n(Is leor dhá phointe eolais, i d’fhocail féin.)', 8, '(ii) Cén t-eolas a thugtar'),
        ('iii', 'Conas a mhothaíonn an spailpín agus é ‘ar mhargadh na saoire’ i véarsa a trí?\nTabhair dhá fháth, i d’fhocail féin, a mothaíonn an spailpín mar sin.', 9, '(iii) Conas a mhothaíonn')],
     '(a) An Spailpín Fánach (25 marc)', '(b) Mo ghrá-sa (idir lúibíní) (25 marc)'),
    ('poetry-3a-b', 'F-3A-b', 12, 'Mo ghrá‐sa (idir lúibíní)', [
        ('i', 'Scríobh síos dhá phointe eolais, i d’fhocail féin, a thugann an file dúinn faoin bhfear sna línte 1‐12 den dán.', 8, '(i) Scríobh síos dhá phointe eolais'),
        ('ii', 'Cad a deir an file faoi ghruaig an fhir sna línte 13‐16 den dán?\n(Is leor dhá phointe eolais, i d’fhocail féin.)', 8, '(ii) Cad a deir an file'),
        ('iii', 'Cén cineál duine é an fear sna línte 17‐21 den dán?\nCuir fáthanna, i d’fhocail féin, le do fhreagra. (Is leor dhá fháth.)', 9, '(iii) Cén cineál duine')],
     '(b) Mo ghrá-sa (idir lúibíní) (25 marc)', '(c) Géibheann (25 marc)'),
    ('poetry-3a-c', 'F-3A-c', 13, 'Géibheann', [
        ('i', 'Déan cur síos, i d’fhocail féin, ar an gcineál saoil atá ag an ainmhí sna línte 1‐8 den dán. (Is leor dhá phointe eolais.)', 8, '(i) Déan cur síos'),
        ('ii', 'Conas a mhothaíonn an t‐ainmhí sna línte 9‐17 den dán, dar leat?\nTabhair dhá fháth, i d’fhocail féin, a mothaíonn an t‐ainmhí mar sin.', 8, '(ii) Conas a mhothaíonn'),
        ('iii', 'An maith leat an dán seo? Cuir fáthanna le do fhreagra. (Is leor dhá fháth.)', 9, '(iii) An maith leat')],
     '(c) Géibheann (25 marc)', 'Níl cead aon ábhar a bhaineann le Filíocht Ainmnithe'),
]
POEM_TOPICS = {'poetry-3a-a': 'irish-5-1', 'poetry-3a-b': 'irish-5-4', 'poetry-3a-c': 'irish-5-2'}
POETRY_3B = [
    ('poetry-3b-a', 'F-3B-a', [
        '(i) Maidir le dán seanaimseartha roghnach (dán a cumadh sa tréimhse roimh 1850) a ndearna tú staidéar air le linn do chúrsa, scríobh síos i d’fhocail féin, príomhsmaointe an dáin. (9 marc)',
        '(ii) Cén íomhá (pictiúr) is mó a thaitníonn leat sa dán? Mínigh an íomhá (an pictiúr) sin i d’fhocail féin. (Is leor dhá phointe eolais.) (7 marc)',
        '(iii) Scríobh síos an mothúchán is láidre sa dán, dar leat. Tabhair dhá shampla den mhothúchán sin sa dán. (7 marc)'],
     '(a) (i) Maidir le dán seanaimseartha', '(b) (i) Maidir le dán nua-aimseartha', ['(ii) Cén íomhá', '(iii) Scríobh síos an mothúchán', 'Ní mór teideal an dáin']),
    ('poetry-3b-b', 'F-3B-b', [
        '(i) Maidir le dán nua‐aimseartha roghnach a ndearna tú staidéar air le linn do chúrsa, scríobh síos príomhthéama an dáin sin, dar leat. Tabhair dhá phointe eolais, i d’fhocail féin, faoin bpríomhthéama sin sa dán. (9 marc)',
        '(ii) Luaigh íomhá (pictiúr) amháin ón dán atá suimiúil, dar leat. Mínigh an íomhá (an pictiúr) sin i d’fhocail féin. (Is leor dhá phointe eolais.) (7 marc)',
        '(iii) Déan cur síos ar an mothúchán is láidre sa dán, dar leat. Is leor dhá phointe eolais. (7 marc)'],
     '(b) (i) Maidir le dán nua-aimseartha', '(c) (i) Maidir le dán nua-aimseartha', ['(ii) Luaigh íomhá', '(iii) Déan cur síos', 'Ní mór teideal an dáin']),
    ('poetry-3b-c', 'F-3B-c', [
        '(i) Maidir le dán nua‐aimseartha roghnach a ndearna tú staidéar air le linn do chúrsa agus nár úsáid tú i gcuid (b) thuas, scríobh síos i d’fhocail féin, príomhsmaointe an dáin. (9 marc)',
        '(ii) Cén t‐atmaisféar atá sa dán seo, dar leat? Tabhair dhá shampla den atmaisféar sin sa dán. (7 marc)',
        '(iii) An maith leat an dán seo? Cuir fáthanna le do fhreagra. (Is leor dhá fháth.) (7 marc)'],
     '(c) (i) Maidir le dán nua-aimseartha', None, ['(ii) Cén t-atmaisféar', '(iii) An maith leat', 'Ní mór teideal an dáin']),
]
TITLE_LINE = 'Ní mór teideal an dáin sin, mar aon le hainm an fhile, a scríobh síos go cruinn. (2 mharc)'

_MATERIAL = None


def material():
    global _MATERIAL
    if _MATERIAL:
        return _MATERIAL
    import fitz
    paper_path = ROOT / f'paper-trail-corpus/exampapers/2021/{FILE}.pdf'
    scheme_path = ROOT / f'paper-trail-corpus/markingschemes/2021/{SCHEME_FILE}.pdf'
    assert hashlib.sha256(paper_path.read_bytes()).hexdigest() == PAPER_SHA, 'Paper changed: repeat visual review'
    assert hashlib.sha256(scheme_path.read_bytes()).hexdigest() == SCHEME_SHA, 'Scheme changed: repeat visual review'
    paper, doc = fitz.open(paper_path), fitz.open(scheme_path)
    texts = [clean(p.get_text()) for p in paper]
    s = Scheme(doc, 12, 30)
    # CEIST 1 (A + B) and A on PDF 12; B on 15; 2A on 18; 2B on 23; 3A on 25; 3B on 29.
    assert s.removed == 7, s.removed
    lang_read = '[Gaeilge lochtach: 0 - 5 a bhaint den iomlán a gnóthaíodh]'
    assert s.text.count(lang_read) == 2
    for letter, passage in PASSAGES.items():
        page_text = ' '.join(texts[p - 1] for p in passage['pages'])
        after = s.page(passage['start'])
        # Each passage prints its own two notes above Ceist 1.
        notes = s.chunk('Nóta: Má tá dhá phointe eolais i gceist', passage['notes_end'], after)[0]
        if letter == 'A':
            notes = notes.removesuffix(passage['title']).strip()
        assert notes.endswith('Nóta: Gearrfar pionós i ngeall ar iomarcaíocht.') and 'Siombailí' not in notes, notes
        passage['notes'] = notes
        resolved = []
        anchors = [p[3] for p in passage['parts']]
        for index, (q, part, prompt, anchor) in enumerate(passage['parts']):
            assert in_order(prompt, page_text), (letter, q, part)
            nxt = anchors[index + 1] if index + 1 < len(anchors) else PENALTY
            chunk, spages = s.chunk(anchor, nxt, after)
            after = s.text.index(anchor, after) + 1
            assert '5 mharc' in chunk and '50 marc' not in chunk and 'LÉAMHTHUISCINT' not in chunk, (letter, q, part, chunk[:80])
            two = '3 mharc + 2 mharc' in chunk
            permitted = [0, 3, 5] if (two or '= 3 mharc' in chunk) else [0, 5]
            resolved.append((q, part, prompt, chunk, spages, two, permitted))
        passage['resolved'] = resolved
    lit_note = s.chunk('Nóta: Níl sé i gceist a chur in iúl go bhfuil na freagraí samplacha', '(a) Hurlamaboc (25 marc)')[0]
    lang_lit = '[Gaeilge lochtach: 0-4 a bhaint den iomlán a gnóthaíodh]'
    # 2A 3 (Dís prints the note with a closing full stop), 2B 4 (novel, film, play, short story), 3A 3, 3B 3.
    assert s.text.count(lang_lit) == 13 and s.text.count(lang_lit[:-1] + '.]') == 1, s.text.count(lang_lit)
    slug, atlas, title, topic, intro, subs, start, end = HURLAMABOC
    for line in [intro, title] + [p for _, p, _ in subs]:
        assert in_order(line.replace('\n', ' '), texts[8]), (slug, line[:40])
    for slug, atlas, title, topic, prompt, start, end in PROSE_2A_B:
        assert in_order(prompt.removesuffix(' (25 marc)'), texts[8]) and in_order(FILM_OR_PLAY, texts[8]), slug
    assert in_order(DIS[4], texts[8]) and in_order(DIS[5].replace('\n', ' ').removesuffix(' (25 marc)'), texts[8])
    for slug, atlas, lines, start, end, parts, title in PROSE_2B:
        for line in lines:
            assert in_order(re.sub(r' \((23|25) marc\)$| \(2 mharc\)$', '', line), texts[9]), (slug, line[:50])
    for line in PROSE_2B_B_LINES:
        assert in_order(line, texts[9]), line[:50]
    for slug, atlas, page, title, subs, start, end in POETRY_3A:
        for label, prompt, marks, cut in subs:
            assert in_order(prompt.replace('\n', ' '), texts[page - 1]), (slug, label)
    for slug, atlas, prompts, start, end, cuts in POETRY_3B:
        for line in prompts + [TITLE_LINE]:
            assert in_order(line, texts[13]), (slug, line[:50])
    assert comparable(texts[13]).count(comparable(TITLE_LINE)) == 3
    assert comparable(CHOOSE) in comparable(texts[2])
    assert comparable(NO_PRESCRIBED_PROSE) in comparable(texts[9]) and comparable(OPT_FILM_OR_PLAY) in comparable(texts[9])
    assert comparable(NO_PRESCRIBED_POETRY) in comparable(texts[13])
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


def prose_pieces(m, subs, start, end):
    whole, spages = m['s'].chunk(start, end)
    whole = before_language_note(whole)
    pieces = split_at(whole, [cut for _, _, cut in subs], 'Hurlamaboc')
    for (label, _, _), piece in zip(subs, pieces):
        assert '(5 mharc)' in piece, label
    return pieces, sorted(set(spages) | {18})


def poem_pieces(m, slug, subs, start, end):
    whole, spages = m['s'].chunk(start, end)
    whole = before_language_note(whole)
    pieces = split_at(whole, [cut for _, _, _, cut in subs], slug)
    for (label, _, marks, _), piece in zip(subs, pieces):
        assert f'({marks} marc)' in piece, (slug, label, piece[:60])
    return pieces, sorted(set(spages) | {25})


def whole_prose(m, start, end):
    chunk, spages = m['s'].chunk(start, end)
    assert '5 phointe eolais agus 5 mharc ar gach pointe eolais' in chunk, start
    return before_language_note(chunk), sorted(set(spages) | {18})


WHOLE_PROSE_NOTE = ('One complete SEC response: five points at 5 (2 for the bare point + 3 for development); the 0–4 Gaeilge deduction applies once. '
                    'The sample points are indicative rather than exhaustive.')


def apply_legacy_review(cards):
    """Lift the 2021 scheme onto the 22 retained legacy cards (IDs, totals and topics unchanged)."""
    m = material()
    by_id = {c['id']: c for c in cards}
    stamped = []

    def stamp(card_id, atlas, pages, scheme_pages, criteria, note, requirements, **extra):
        card = by_id[card_id]
        card.update(atlasQuestionId=atlas, reviewedAt=REVIEWED_AT, reviewedPaperPages=pages, schemeFileid=SCHEME_FILE,
                    schemePage=scheme_pages[0], schemePages=scheme_pages, criteria=criteria, markingGuideNote=note,
                    taskRequirements=requirements, **extra)
        assert sum(c['maxMarks'] for c in criteria if c['kind'] == 'award') == card['totalMarks'], card_id
        assert not any('Siombailí Anótála' in g or '50 marc' in g or 'LÉAMHTHUISCINT' in g for c in criteria for g in c['guidance']), card_id
        stamped.append(card_id)
        return card

    # Reading: the frozen Atlas identities 1–5 (A) and 6–10 (B) are the whole questions.
    for letter, passage in PASSAGES.items():
        by_q = {}
        for q, part, prompt, chunk, spages, two, permitted in passage['resolved']:
            by_q.setdefault(q, []).append((part, chunk, spages, permitted))
        for q, parts in by_q.items():
            card_id = f'irish-2021-ol-p2-reading-{letter.lower()}-q{q}'
            assert by_id[card_id]['topicId'] == passage['topic'], card_id
            assert in_order(by_id[card_id]['questionText'], ' '.join(m['texts'][p - 1] for p in passage['pages'])), card_id
            crits = [criterion(part, f'({part}) Freagra', 5, [chunk, passage['notes']], permitted=permitted) for part, chunk, _, permitted in parts]
            stamp(card_id, str(int(q) + (5 if letter == 'B' else 0)), passage['pages'], sorted({p for *_, sp, _ in parts for p in sp}), crits,
                  'Retained complete printed question: (a) 5 + (b) 5, each scored separately at its SEC allocation. ' + reading_note(m),
                  READING_WHOLE)

    note = m['lit_note']
    slug, atlas, title, topic, intro, subs, start, end = HURLAMABOC
    assert by_id[f'irish-2021-ol-p2-{slug}']['topicId'] == topic, slug
    pieces, spages = prose_pieces(m, subs, start, end)
    crits = [criterion(f'eolas-{label}', f'({label}) Eolas', 5, [piece, note], 'indicative', permitted=sub_permitted(piece, 5))
             for (label, _, _), piece in zip(subs, pieces)]
    stamp(f'irish-2021-ol-p2-{slug}', atlas, [9], spages, crits + [deduction(m)],
          'One complete SEC response: five printed sub-questions at 5 each, then the 0–4 Gaeilge deduction once. '
          'The sample answers are indicative rather than exhaustive.',
          [CHOOSE] + LIT, questionText=f'(a) {intro}\n{title}\n' + '\n'.join(f'({l}) {p}' for l, p, _ in subs) + '\n(25 marc)',
          sourceMaterial=source('Prós Ainmnithe', title, [9]))

    slug, atlas, title, topic, prompt, start, end = PROSE_2A_B[0]
    assert by_id[f'irish-2021-ol-p2-{slug}']['topicId'] == topic, slug
    chunk, spages = whole_prose(m, start, end)
    stamp(f'irish-2021-ol-p2-{slug}', atlas, [9], spages,
          [criterion('eolas', 'Eolas', 25, [chunk, note], 'indicative'), deduction(m)],
          WHOLE_PROSE_NOTE + ' 2A(b) offers Cáca Milis or An Lasair Choille; this card is Cáca Milis.',
          [CHOOSE, FILM_OR_PLAY] + LIT[1:], questionText=f'(b) {FILM_OR_PLAY}\n{title}\n{prompt}',
          sourceMaterial=source('Prós Ainmnithe', title, [9]))

    slug, atlas, title, topic, intro, prompt, start, end = DIS
    assert by_id[f'irish-2021-ol-p2-{slug}']['topicId'] == topic, slug
    chunk, spages = whole_prose(m, start, end)
    stamp(f'irish-2021-ol-p2-{slug}', atlas, [9], spages,
          [criterion('eolas', 'Eolas', 25, [chunk, note], 'indicative'), deduction(m)], WHOLE_PROSE_NOTE,
          [CHOOSE] + LIT[1:], questionText=f'(c) {intro}\n{title}\n{prompt}', sourceMaterial=source('Prós Ainmnithe', title, [9]))

    for slug, atlas, lines, start, end, parts, title in PROSE_2B:
        chunk, spages = m['s'].chunk(start, end, m['s'].page(23)) if end else m['s'].chunk(start, '⟦25⟧', m['s'].page(24))
        chunk = before_language_note(chunk)
        cuts = [0] + [chunk.index(cut) for _, _, _, cut in parts[1:]]
        pieces = [chunk[a:b].strip() for a, b in zip(cuts, cuts[1:] + [len(chunk)])]
        # Naming and account depend on the candidate's chosen text (indicative); the title marks are exact.
        crits = [criterion(cid, label, marks, [piece], 'exact' if cid == 'teideal' else 'indicative',
                           permitted=None if cid == 'eolas' else sorted({0, marks} | {int(v) for v in re.findall(r'= (\d) mharc', piece)}))
                 for (cid, label, marks, _), piece in zip(parts, pieces)]
        assert crits[-1]['guidance'][0].endswith('(2 mharc)'), slug
        stamp(f'irish-2021-ol-p2-{slug}', atlas, [10], spages, crits + [deduction(m)],
              'One complete SEC response: ' + ', '.join(f'{label} {marks}' for _, label, marks, _ in parts) +
              ', then the 0–4 Gaeilge deduction once. The optional text is open content chosen by the candidate; the scheme prints no sample '
              'points for it, so its points are judged on merit against these allocations (indicative rather than exhaustive).',
              [CHOOSE, NO_PRESCRIBED_PROSE] + LIT[1:], questionText='\n'.join(lines), stem=NO_PRESCRIBED_PROSE,
              sourceMaterial=source('Prós Roghnach', title, [10]))

    # 2B(b): an optional film or an optional play, one scheme, so one card carries both printed alternatives.
    chunk, spages = m['s'].chunk('(b) Freagair an cheist thíos faoin scannán roghnach', '(c) Maidir le gearrscéal roghnach')
    film, play = chunk.split(' nó Maidir le dráma roghnach', 1)
    play = 'Maidir le dráma roghnach' + play
    halves = [before_language_note(film), before_language_note(play)]
    accounts = [h[:h.rindex('Ní mór teideal')].strip() for h in halves]
    titles = [h[h.rindex('Ní mór teideal'):].strip() for h in halves]
    assert all('Na príomhimeachtaí (príomhrudaí) = 23 marc' in a for a in accounts) and all(t.endswith('(2 mharc)') for t in titles)
    stamp('irish-2021-ol-p2-prose-2b-b', 'P-2B-b', [10], spages,
          [criterion('eolas', 'Príomhimeachtaí', 23, accounts, 'indicative'),
           criterion('teideal', 'Teideal + ainm an scríbhneora', 2, titles, 'exact', permitted=[0, 1, 2]), deduction(m)],
          'One complete SEC response about an optional film or an optional play (the same scheme for both): 23 for five points '
          '(5, 5, 5, 4, 4) and 2 for the exact title and writer, then the 0–4 Gaeilge deduction once. The text is open content '
          'chosen by the candidate (indicative rather than exhaustive).',
          [CHOOSE, NO_PRESCRIBED_PROSE, OPT_FILM_OR_PLAY] + LIT[1:], questionText='\n'.join(PROSE_2B_B_LINES), stem=NO_PRESCRIBED_PROSE,
          sourceMaterial=source('Prós Roghnach', 'Scannán nó dráma roghnach', [10]))

    for slug, atlas, page, title, subs, start, end in POETRY_3A:
        assert by_id[f'irish-2021-ol-p2-{slug}']['topicId'] == POEM_TOPICS[slug], slug
        pieces, spages = poem_pieces(m, slug, subs, start, end)
        crits = [criterion(f'eolas-{label}', f'({label}) Eolas', marks, [piece, note], 'indicative')
                 for (label, _, marks, _), piece in zip(subs, pieces)]
        prompt = '\n'.join(f'({label}) {p}' + f' ({marks} marc)' for label, p, marks, _ in subs)
        stamp(f'irish-2021-ol-p2-{slug}', atlas, [page], spages, crits + [deduction(m)],
              'One complete SEC response: (i) 8, (ii) 8, (iii) 9 at their printed tariffs, then the 0–4 Gaeilge deduction once. '
              'The sample points are indicative rather than exhaustive; lines lifted straight from the poem without the candidate’s own words earn 2 + 2.',
              [CHOOSE] + LIT, questionText=f'({atlas[-1]}) {title}\n' + prompt,
              sourceMaterial=source('Filíocht Ainmnithe', title, [page]))

    for slug, atlas, prompts, start, end, cuts in POETRY_3B:
        chunk, spages = m['s'].chunk(start, end, m['s'].page(29)) if end else m['s'].chunk(start, None, m['s'].page(29))
        chunk = before_language_note(chunk)
        idx = [0] + [chunk.index(cut) for cut in cuts]
        pieces = [chunk[a:b].strip() for a, b in zip(idx, idx[1:] + [len(chunk)])]
        for piece, cap in zip(pieces, ['(9 marc)', '(7 marc)', '(7 marc)', '(2 mharc)']):
            assert cap in piece, (slug, cap)
        crits = [criterion('eolas-i', '(i) Eolas', 9, [pieces[0]], 'indicative'), criterion('eolas-ii', '(ii) Eolas', 7, [pieces[1]], 'indicative'),
                 criterion('eolas-iii', '(iii) Eolas', 7, [pieces[2]], 'indicative'),
                 criterion('teideal', 'Teideal + ainm an fhile', 2, [pieces[3]], 'exact')]
        stamp(f'irish-2021-ol-p2-{slug}', atlas, [14], spages, crits + [deduction(m)],
              'One complete SEC response: (i) 9, (ii) 7, (iii) 7, poem and poet 2, then the 0–4 Gaeilge deduction once. '
              'The optional poem is open content. The printed allocations are judged on merit (indicative rather than exhaustive).',
              [CHOOSE, NO_PRESCRIBED_POETRY] + LIT, questionText=f'({atlas[-1]}) ' + '\n'.join(prompts + [TITLE_LINE]), stem=NO_PRESCRIBED_POETRY,
              sourceMaterial=source('Filíocht Roghnach', f'3B({atlas[-1]}) · Dán roghnach', [14]))
    assert len(stamped) == 22
    for card_id in stamped:
        for c in by_id[card_id]['criteria']:
            assert c['guidance'] and all(not re.search('[-]', g) for g in c['guidance']), (card_id, c['id'])
    return cards, stamped


def build():
    m = material()
    cards = []

    def add(key, slug, ref, prompt, topic, pages, scheme_pages, criteria, requirements, note, src):
        cards.append(dict(
            id=f'irish-2021-ol-p2-{slug}', year=2021, level='ordinary', paper=2, section='2',
            atlasQuestionId=key, questionRef=f'2021 OL Paper 2 {ref}', questionText=prompt,
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
    slug, atlas, title, topic, intro, subs, start, end = HURLAMABOC
    pieces, spages = prose_pieces(m, subs, start, end)
    src = source('Prós Ainmnithe', title, [9])
    for (label, prompt, _), piece in zip(subs, pieces):
        add(f'{atlas}-{label}', f'{slug}-{label}', f'Prós 2A(a) · {title} · ({label})', f'(a) {intro}\n{title}\n({label}) {prompt} (5 marc)',
            topic, [9], spages, [criterion('eolas', 'Eolas', 5, [piece, note], 'indicative', permitted=sub_permitted(piece, 5))],
            [CHOOSE] + LIT[1:], sub_note, src)

    slug, atlas, title, topic, prompt, start, end = PROSE_2A_B[1]
    chunk, spages = whole_prose(m, start, end)
    add(atlas, slug, f'Prós 2A(b) · {title}', f'(b) {FILM_OR_PLAY}\n{title}\n{prompt}', topic, [9], spages,
        [criterion('eolas', 'Eolas', 25, [chunk, note], 'indicative'), deduction(m)],
        [CHOOSE, FILM_OR_PLAY] + LIT[1:],
        WHOLE_PROSE_NOTE + ' 2A(b) offers Cáca Milis or An Lasair Choille; this card is An Lasair Choille.',
        source('Prós Ainmnithe', title, [9]))

    for slug, atlas, page, title, subs, start, end in POETRY_3A:
        pieces, spages = poem_pieces(m, slug, subs, start, end)
        topic = POEM_TOPICS[slug]
        src = source('Filíocht Ainmnithe', title, [page])
        for (label, prompt, marks, _), piece in zip(subs, pieces):
            add(f'{atlas}-{label}', f'{slug}-{label}', f'Filíocht 3A({atlas[-1]}) · {title} · ({label})', f'({atlas[-1]}) {title}\n({label}) {prompt} ({marks} marc)',
                topic, [page], spages, [criterion('eolas', 'Eolas', marks, [piece, note], 'indicative')],
                [CHOOSE] + LIT[1:], sub_note, src)

    assert len(cards) == 35 and len({c['id'] for c in cards}) == 35 and len({c['atlasQuestionId'] for c in cards}) == 35
    for card in cards:
        for c in card['criteria']:
            assert c['guidance'] and all(not re.search('[-]|Siombailí Anótála|50 marc', g) for g in c['guidance']), (card['id'], c['id'])
    sr = json.loads(SOURCE_REVIEW.read_text())
    legacy = ([f'irish-2021-ol-p2-reading-{l}-q{q}' for l in 'ab' for q in range(1, 6)]
              + [f'irish-2021-ol-p2-prose-{k}' for k in ['2a-a', '2a-b', '2a-c', '2b-a', '2b-b', '2b-c']]
              + [f'irish-2021-ol-p2-poetry-{k}' for k in ['3a-a', '3a-b', '3a-c', '3b-a', '3b-b', '3b-c']])
    review = dict(year=2021, level='ordinary', paperFileid=FILE + '.pdf', schemeFileid=SCHEME_FILE + '.pdf',
                  paperSha256=PAPER_SHA, schemeSha256=SCHEME_SHA,
                  reviewedPaperPages=list(range(1, 17)), reviewedSchemePages=sr['reviewedSchemePages'], schemeScope=sr['schemeScope'],
                  reviewDate=REVIEWED_AT, status='reviewed', fullPaperAndApplicableSchemeVisualSweep=True, selectionDecisions=m['decisions'],
                  practiceCardIds=[c['id'] for c in cards], legacyCardIds=legacy, readingWholeCardIds=legacy[:10],
                  examStructure=dict(readingA=50, readingB=50, literature=50, total=150),
                  nonPoolDecisions=sr['nonPoolDecisions'], openIssues=[], caveats=sr['sourceFindings'],
                  choicePolicy=('Choice is not a route: each printed option of 2A, 2B, 3A and 3B is one card carrying the choose-two instruction; '
                                'no combination cards. Inside 2A(b) the two prescribed texts (different topics) are separate cards; inside 2B(b) '
                                'the optional film and play share one scheme and stay one card.'),
                  boundaries=('10 retained whole reading questions with their 20 published parts; 12 retained literature options plus the An Lasair '
                              'Choille option of 2A(b); the 5 printed 2A(a) Hurlamaboc sub-questions and the 9 prescribed-poetry sub-questions.'))
    return dict(review=review, cards=cards)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    data = build()
    scheme_words_in(data)  # guidance carries the SEC's words only (irish_lifted.py)
    content = json.dumps(data, ensure_ascii=False, indent=2) + '\n'
    if args.check:
        assert OUT.exists() and OUT.read_text() == content, f'Stale output: {OUT}'
    else:
        OUT.write_text(content)
    print(f"Irish Ordinary 2021 Paper 2: {len(data['cards'])} added practice cards (+22 retained legacy cards); the archive remains incomplete.")


if __name__ == '__main__':
    main()
