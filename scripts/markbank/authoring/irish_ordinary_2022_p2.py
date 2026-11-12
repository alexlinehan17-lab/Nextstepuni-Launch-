#!/usr/bin/env python3
"""Reviewed 2022 Ordinary Paper 2 (Léamhthuiscint agus Litríocht).

Paper PDF 1–16 and the Paper 2 pages of the combined LC001GLP000IV scheme
(PDF 15–31, plus 32–33 modified marking) reviewed on 2026-11-04. Counts are
assertions, not corpus-completeness proof. Same method as irish_ordinary_2023_p2.py
and irish_ordinary_2024_p2.py.

The legacy generator already ships 22 cards for this component: the ten whole
reading questions and the twelve literature options. Their IDs, totals and topics
are kept. `apply_legacy_review` (called by irish_cards.py) joins them to Atlas and
replaces their marking with the lifted 2022 scheme. `build` adds every reading part
(20), the five printed sub-questions of 2A(a) Oisín i dTír na nÓg, every
prescribed-poetry sub-question (9) and the eight printed 2-mark questions inside
3A(a)(i) An tEarrach Thiar and 3A(c)(ii) An Spailpín Fánach.

2022 differs from 2023 in its literature layout. The paper prints no “Freagair 2A … nó
2B …” or “Freagair do rogha dhá cheann …” lines: the instructions page (PDF 3) prints
“Freagair dhá cheist as an roinn seo.” and the allowed combinations, and each option
card carries that instruction in its task requirements (choice is not a route; no
card combines two options). Each section's printed box heading (“2A – PRÓS
AINMNITHE” …) and, for 2B and 3B, the printed restriction (“Níl cead aon ábhar …”) are
the card's lead-in (stem). 2A(b) Hurlamaboc and 2A(c) Dís are one 25-mark question each;
2A(c) offers no second text in 2022. 3B(b) asks for a second modern poem “nár úsáid tú
i gcuid (a) thuas”, inside its own question.

The scheme's text layer stores each page's boxed heading (“A – (50 marc)”, “2A – PRÓS
AINMNITHE” …) with the page body; `Scheme` removes those exact strings so no heading
lands inside an answer key.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import re
from pathlib import Path
from irish_lifted import PUA, printed_lead_in, scheme_words_in, symbol_text

ROOT = Path(__file__).resolve().parents[3]
FILE = 'LC001GLP200IV'
SCHEME_FILE = 'LC001GLP000IV'
OUT = ROOT / 'components/MarkBank/cards/irish/ordinary-2022-p2-authored.json'
SOURCE_REVIEW = ROOT / 'scripts/markbank/authored/irish-ordinary-2022-p2-source-review.json'
REVIEWED_AT = '2026-11-04'
PAPER_SHA = 'cc19ef968f2fd9f119879ec14e146adbac472058c3895695f8a4e4b38ef285a1'
SCHEME_SHA = 'c93ce0ad1ecd0cd4f7014f31a0c128d49076fd75040efd4c3d18bd369c5ec926'
DIRECTIVE = re.compile(r'rogha|roghna|Freagair|Luaigh|Ainmnigh|\bnó\b|dhá phointe|dhá rud|dhá bh|dhá dh|dhá ch|dhá fh|dhá th|dhá ph|dhá sh|'
                       r'\ban dá\b|ceann amháin|pointe amháin|amháin|\bdhá\b', re.I)
SOURCE_NOTE = 'Shown page-for-page from the official examination paper; swipe to move between pages.'
ATTRIBUTION = '© State Examinations Commission.'
# Boxed page headings the 2022 scheme's text layer stores with the page body (exact strings, count pinned).
FURNITURE = ('CEIST 1 (A + B) - LÉAMHTHUISCINT - 100 marc', 'A – (50 marc)', 'B – (50 marc)',
             '2A – PRÓS AINMNITHE', '2B – PRÓS ROGHNACH', '3A – FILÍOCHT AINMNITHE', '3B – FILÍOCHT ROGHNACH')
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


# (q, part, paper prompt, scheme anchor)
PASSAGES = {
    'A': dict(title='Uimhir a Sé, Sráid Fhearchair, Baile Átha Cliath', pages=[4, 5], topic='irish-3-0', start='⟦16⟧', parts=[
        ('1', 'a', '(a) Tabhair dhá phíosa eolais faoi Hans Blackwood. (Alt 1)', '1. (a) Tabhair dhá phíosa eolais faoi Hans'),
        ('1', 'b', '(b) Scríobh síos dhá phíosa eolais faoin mbaint a bhí ag John Henry Newman le hUimhir a Sé. (Alt 1)', '(b) Scríobh síos dhá phíosa eolais faoin mbaint'),
        ('2', 'a', '(a) Cén fáth ar eagraigh ceannaire Shinn Féin, Art Ó Gríofa, cainteanna in Uimhir a Sé? (Alt 2)', '2. (a) Cén fáth ar eagraigh'),
        ('2', 'b', '(b) Luaigh dhá phíosa eolais faoi Uimhir a Sé le linn Éirí Amach na Cásca i 1916. (Alt 2)', '(b) Luaigh dhá phíosa eolais faoi Uimhir a Sé'),
        ('3', 'a', '(a) Cad a tharla ag comhdháil in Uimhir a Sé i mí na Nollag 1916? (Alt 3)', '3. (a) Cad a tharla ag comhdháil'),
        ('3', 'b', '(b) Scríobh síos dhá rud a rinne Sinn Féin in Uimhir a Sé tar éis a mbua san olltoghchán. (Alt 3)', '(b) Scríobh síos dhá rud a rinne Sinn Féin'),
        ('4', 'a', '(a) Tabhair dhá phíosa eolais faoi Mhicheál Ó Coileáin. (Alt 4)', '4. (a) Tabhair dhá phíosa eolais faoi Mhicheál'),
        ('4', 'b', '(b) Cén fáth ar chaith Coláiste Mhuire dhá bhliain in Uimhir a Sé? (Alt 4)', '(b) Cén fáth ar chaith Coláiste Mhuire'),
        ('5', 'a', '(a) Luaigh dhá phíosa eolais faoi Chlub Chonradh na Gaeilge. (Alt 5)', '5. (a) Luaigh dhá phíosa eolais faoi Chlub'),
        ('5', 'b', '(b) Scríobh síos dhá rud atá i bplean nua Chonradh na Gaeilge don teach. (Alt 5)', '(b) Scríobh síos dhá rud atá i bplean')]),
    'B': dict(title='An Ceol', pages=[6, 7], topic='irish-3-1', start='⟦18⟧', parts=[
        ('1', 'a', '(a) Scríobh síos dhá shampla den úsáid a bhaintear as cineálacha éagsúla ceoil ar ócáidí difriúla. (Alt 1)', '1. (a) Scríobh síos dhá shampla'),
        ('1', 'b', '(b) Tabhair dhá chúis a bhfuil an ceol tábhachtach i saol na ndaoine. (Alt 1)', '(b) Tabhair dhá chúis a bhfuil an ceol'),
        ('2', 'a', '(a) Luaigh dhá chúis a mbaineann lucht déanta scannán úsáid as an gceol. (Alt 2)', '2. (a) Luaigh dhá chúis a mbaineann'),
        ('2', 'b', '(b) Cén fáth ar eagraíodh ceolchoirm Live Aid sa bhliain 1985? (Alt 2)', '(b) Cén fáth ar eagraíodh ceolchoirm'),
        ('3', 'a', '(a) Tabhair dhá phíosa eolais faoin gcláirseach. (Alt 3)', '3. (a) Tabhair dhá phíosa eolais faoin gcláirseach'),
        ('3', 'b', '(b) Scríobh síos dhá rud faoi Fhleadh Cheoil na hÉireann. (Alt 3)', '(b) Scríobh síos dhá rud faoi Fhleadh'),
        ('4', 'a', '(a) Scríobh síos dhá bhealach ar thuill an grúpa ceoil The Chieftains clú agus cáil idirnáisiúnta don cheol Gaelach. (Alt 4)', '4. (a) Scríobh síos dhá bhealach ar thuill'),
        ('4', 'b', '(b) Cén tionchar a bhí ag an seó Riverdance ar an rince Gaelach? (Alt 4)', '(b) Cén tionchar a bhí ag an seó'),
        ('5', 'a', '(a) Luaigh dhá bhealach a bhfuil daoine ábalta an ceol a fháil go héasca ar an idirlíon. (Alt 5)', '5. (a) Luaigh dhá bhealach a bhfuil'),
        ('5', 'b', '(b) Scríobh síos dhá mhíbhuntáiste atá ag baint leis an teicneolaíocht do thionscal an cheoil agus do cheoltóirí. (Alt 5)', '(b) Scríobh síos dhá mhíbhuntáiste')]),
}

# Printed lines (paper PDF 3, 9, 10, 11–13, 14).
CHOOSE = 'Freagair dhá cheist as an roinn seo.'
BOX_2A, BOX_2B, BOX_3A, BOX_3B = '2A – PRÓS AINMNITHE', '2B – PRÓS ROGHNACH', '3A – FILÍOCHT AINMNITHE', '3B – FILÍOCHT ROGHNACH'
NO_PRESCRIBED_PROSE = 'Níl cead aon ábhar a bhaineann le Prós Ainmnithe a úsáid sna freagraí ar an bPrós Roghnach.'
NO_PRESCRIBED_POETRY = 'Níl cead aon ábhar a bhaineann le Filíocht Ainmnithe a úsáid sna freagraí ar an bhFilíocht Roghnach.'
STEM_2B = BOX_2B + '\n' + NO_PRESCRIBED_PROSE
STEM_3B = BOX_3B + '\n' + NO_PRESCRIBED_POETRY
# The 2023 builders' requirement lines; irish_lifted.printed_tasks gives each its English.
LIT = ['Freagair gach fochuid atá priontáilte sa rogha seo.', 'Úsáid tagairtí cruinne agus ábhartha don téacs.']
READING_PART = ['Léigh an sliocht iomlán a ghabhann leis an gceist. Freagair an chuid atá luaite ar an gcárta.', 'Úsáid an t-alt a luaitear.']
READING_WHOLE = ['Léigh an sliocht oifigiúil a ghabhann leis an gceist.', 'Freagair gach fochuid agus cloígh leis an alt a luaitear.']

# Prescribed prose with printed sub-questions: (slug, atlas, letter, title, topic, intro, [(label, paper prompt, scheme cut)], scheme start, scheme end)
PROSE_SUBS = [
    ('prose-2a-a', 'P-2A-a', 'a', 'Oisín i dTír na nÓg', 'irish-4-1', 'Freagair na ceisteanna thíos faoin scéal béaloidis Oisín i dTír na nÓg.', [
        ('i', 'Scríobh síos dhá athrú a tháinig ar Oisín nuair a thit sé den each bán i nGleann na Smól.', '(i) Scríobh síos dhá athrú'),
        ('ii', 'Luaigh dhá rud a d’inis Niamh Chinn Óir d’Oisín faoi Thír na nÓg.', '(ii) Luaigh dhá rud'),
        ('iii', 'Cén fáth a raibh brón ar Oisín agus é ag imeacht le Niamh Chinn Óir go Tír na nÓg?', '(iii) Cén fáth a raibh brón'),
        ('iv', 'Scríobh síos dhá phointe eolais faoin saol a bhí ag Oisín agus ag Niamh Chinn Óir i dTír na nÓg.', '(iv) Scríobh síos dhá phointe eolais'),
        ('v', 'Conas a chabhraigh Naomh Pádraig le hOisín tar éis dó filleadh ar Éirinn?', '(v) Conas a chabhraigh')],
     '(a) Oisín i dTír na nÓg (25 marc)', '(b) Hurlamaboc (25 marc)'),
]
# Prescribed prose printed as one 25-mark question: (slug, atlas, letter, title, topic, intro, paper prompt, scheme start, scheme end)
PROSE_WHOLE = [
    ('prose-2a-b', 'P-2A-b', 'b', 'Hurlamaboc', 'irish-4-5', 'Freagair an cheist thíos faoin ngiota as an úrscéal Hurlamaboc.',
     '‘Bhí an chuma ar Lisín go raibh sí ina hógbhean fós … ní raibh sí riamh díomhaoin.’\n'
     'Déan cur síos ar Lisín agus ar an gcineál saoil a bhí aici. (25 marc)',
     '(b) Hurlamaboc (25 marc)', '(c) Dís (25 marc)'),
    ('prose-2a-c', 'P-2A-c', 'c', 'Dís', 'irish-4-4', 'Freagair an cheist thíos faoin ngearrscéal Dís.',
     '‘Féach ansan. Toradh suirbhé a deineadh. Deirtear ann go bhfuil an ceathrú cuid de mhná pósta na tíre míshona, míshásta. '
     'Táimse ansan, ina measc.’\nDéan cur síos ar shaol bhean Sheáin agus ar na fáthanna a raibh sí míshona, míshásta. (25 marc)',
     '(c) Dís (25 marc)', 'Níl cead aon ábhar a bhaineann le Prós Ainmnithe'),
]
# Optional prose (2B): (slug, atlas, paper lines, scheme start, scheme end, [(id, label, marks, cut-before)], source title)
PROSE_2B = [
    ('prose-2b-a', 'P-2B-a', ['(a) Maidir le scéal béaloidis roghnach a ndearna tú staidéar air le linn do chúrsa, tabhair cuntas ar na príomhimeachtaí (príomhrudaí) a tharlaíonn sa scéal. (23 marc)',
                              'Ní mór teideal an scéil bhéaloidis sin a scríobh síos go cruinn. (2 mharc)'],
     '(a) Maidir le scéal béaloidis roghnach', '(b) Maidir le giota as úrscéal roghnach',
     [('eolas', 'Na príomhimeachtaí', 23, None), ('teideal', 'Teideal an scéil bhéaloidis', 2, 'Ní mór teideal')], 'Scéal béaloidis roghnach'),
    ('prose-2b-b', 'P-2B-b', ['(b) Maidir le giota as úrscéal roghnach a ndearna tú staidéar air le linn do chúrsa, ainmnigh an phríomhphearsa (an príomhcharachtar) sa ghiota sin. Déan cur síos ar an gcineál saoil atá ag an duine sin sa ghiota. (23 marc)',
                              'Ní mór teideal an úrscéil sin, mar aon le hainm an údair, a scríobh síos go cruinn. (2 mharc)'],
     '(b) Maidir le giota as úrscéal roghnach', '(c) Maidir le gearrscéal roghnach',
     [('priomhphearsa', 'An phríomhphearsa a ainmniú', 1, None), ('eolas', 'An cineál saoil', 22, 'An cineál saoil atá ag an duine sin ='),
      ('teideal', 'Teideal + ainm an údair', 2, 'Ní mór teideal')], 'Giota as úrscéal roghnach'),
    ('prose-2b-c', 'P-2B-c', ['(c) Maidir le gearrscéal roghnach a ndearna tú staidéar air le linn do chúrsa, ainmnigh an phríomhphearsa (an príomhcharachtar) sa ghearrscéal sin. Tabhair cuntas ar na heachtraí is mó a tharlaíonn don duine sin sa ghearrscéal. (23 marc)',
                              'Ní mór teideal an ghearrscéil sin, mar aon le hainm an údair, a scríobh síos go cruinn. (2 mharc)'],
     '(c) Maidir le gearrscéal roghnach', '(a) An tEarrach Thiar (25 marc)',
     [('priomhphearsa', 'An phríomhphearsa a ainmniú', 1, None), ('eolas', 'Na heachtraí is mó', 22, 'Na heachtraí is mó a a tharlaíonn don duine sin ='),
      ('teideal', 'Teideal + ainm an údair', 2, 'Ní mór teideal')], 'Gearrscéal roghnach'),
]
# Prescribed poetry (3A): (slug, atlas, page, title, [(label, paper prompt, marks, scheme cut)], scheme start, scheme end)
POETRY_3A = [
    ('poetry-3a-a', 'F-3A-a', 11, 'An tEarrach Thiar', [
        ('i', '(a) Cén séasúr atá i gceist sa dán seo?\n(b) Conas atá an aimsir i véarsa a haon?\n(c) Cad atá á dhéanamh ag an bhfear i véarsa a dó?\n'
              '(d) Tabhair pointe amháin eolais faoi na mná i véarsa a trí.', 8, '(i) (a) Cén séasúr'),
        ('ii', 'Déan cur síos, i d’fhocail féin, ar an íomhá (ar an bpictiúr) den churrach a thugann an file dúinn i véarsa a ceathair. (Is leor dhá phointe eolais.)', 8, '(ii) Déan cur síos'),
        ('iii', 'An bhfuil an file sásta sa dán seo, dar leat? Tabhair dhá fháth, i d’fhocail féin, le do fhreagra.', 9, '(iii) An bhfuil an file sásta')],
     '(a) An tEarrach Thiar (25 marc)', '(b) Colscaradh (25 marc)'),
    ('poetry-3a-b', 'F-3A-b', 12, 'Colscaradh', [
        ('i', 'Déan cur síos, i d’fhocail féin, ar dhá íomhá (dhá phictiúr) den phósadh a bhí in aigne an fhir i véarsa a haon.', 8, '(i) Déan cur síos'),
        ('ii', 'Scríobh síos, i d’fhocail féin, na príomhsmaointe atá i véarsa a dó. (Is leor dhá phointe eolais.)', 8, '(ii) Scríobh síos'),
        ('iii', 'Scríobh síos an mothúchán is láidre sa dán, dar leat. Tabhair dhá shampla, i d’fhocail féin, den mhothúchán sin sa dán.', 9, '(iii) Scríobh síos an mothúchán')],
     '(b) Colscaradh (25 marc)', '(c) An Spailpín Fánach (25 marc)'),
    ('poetry-3a-c', 'F-3A-c', 13, 'An Spailpín Fánach', [
        ('i', 'Cén t‐eolas a thugtar dúinn faoin spailpín i véarsa a haon den dán? (Is leor dhá phointe eolais, i d’fhocail féin.)', 8, '(i) Cén t-eolas'),
        ('ii', '(a) Cén rud a bhíonn á rá ag na daoine i nDurlas i véarsa a dó?\n(b) Cén fáth nach dteastaíonn ón spailpín dul go Caiseal i véarsa a trí?\n'
               '(c) Cá mbíodh an spailpín ina shuí agus é ‘ar mhargadh na saoire’ i véarsa a trí?\n(d) Cén cheist a chuireadh ‘bodairí na tíre’ ar an spailpín i véarsa a trí?', 8, '(ii) (a) Cén rud a bhíonn'),
        ('iii', 'An maith leat an dán seo? Tabhair dhá fháth, i d’fhocail féin, le do fhreagra.', 9, '(iii) An maith leat')],
     '(c) An Spailpín Fánach (25 marc)', 'Níl cead aon ábhar a bhaineann le Filíocht Ainmnithe'),
]
POEM_TOPICS = {'poetry-3a-a': 'irish-5-3', 'poetry-3a-b': 'irish-5-5', 'poetry-3a-c': 'irish-5-1'}
# 3A(a)(i) and 3A(c)(ii) each print four 2-mark questions (a)–(d): (slug, sub-question, [(letter, scheme question, next cut)])
SLOTS_3A = {
    ('poetry-3a-a', 'i'): [('a', 'Cén séasúr atá i gceist sa dán seo?', '(b) Conas atá an aimsir'),
                           ('b', 'Conas atá an aimsir i véarsa a haon?', '(c) Cad atá á dhéanamh'),
                           ('c', 'Cad atá á dhéanamh ag an bhfear i véarsa a dó?', '(d) Tabhair pointe amháin'),
                           ('d', 'Tabhair pointe amháin eolais faoi na mná i véarsa a trí.', None)],
    ('poetry-3a-c', 'ii'): [('a', 'Cén rud a bhíonn á rá ag na daoine i nDurlas i véarsa a dó?', '(b) Cén fáth nach dteastaíonn'),
                            ('b', 'Cén fáth nach dteastaíonn ón spailpín dul go Caiseal i véarsa a trí?', '(c) Cá mbíodh'),
                            ('c', 'Cá mbíodh an spailpín ina shuí agus é ‘ar mhargadh na saoire’ i véarsa a trí?', '(d) Cén cheist'),
                            ('d', 'Cén cheist a chuireadh ‘bodairí na tíre’ ar an spailpín i véarsa a trí?', None)],
}
POETRY_3B = [
    ('poetry-3b-a', 'F-3B-a', [
        '(i) Maidir le dán nua‐aimseartha roghnach a ndearna tú staidéar air le linn do chúrsa, scríobh síos i d’fhocail féin, príomhsmaointe an dáin. (9 marc)',
        '(ii) Cén íomhá (pictiúr) is mó a thaitníonn leat sa dán? Mínigh an íomhá (an pictiúr) sin i d’fhocail féin. (Is leor dhá phointe eolais.) (7 marc)',
        '(iii) Scríobh síos an mothúchán is láidre sa dán, dar leat. Tabhair dhá shampla den mhothúchán sin sa dán. (7 marc)'],
     '(a) (i) Maidir le dán nua-aimseartha', '(b) (i) Maidir le dán nua-aimseartha', ['(ii) Cén íomhá', '(iii) Scríobh síos an mothúchán', 'Ní mór teideal an dáin']),
    ('poetry-3b-b', 'F-3B-b', [
        '(i) Maidir le dán nua‐aimseartha roghnach a ndearna tú staidéar air le linn do chúrsa, agus nár úsáid tú i gcuid (a) thuas, scríobh síos príomhthéama an dáin sin. '
        'Tabhair dhá phointe eolais, i d’fhocail féin, faoin bpríomhthéama sin sa dán. (9 marc)',
        '(ii) Cén t‐atmaisféar atá sa dán seo, dar leat? Tabhair dhá shampla den atmaisféar sin sa dán. (7 marc)',
        '(iii) Scríobh síos rud amháin a thaitin leat agus rud amháin nár thaitin leat faoin dán seo. (7 marc)'],
     '(b) (i) Maidir le dán nua-aimseartha', '(c) (i) Maidir le dán seanaimseartha', ['(ii) Cén t-atmaisféar', '(iii) Scríobh síos rud amháin', 'Ní mór teideal an dáin']),
    ('poetry-3b-c', 'F-3B-c', [
        '(i) Maidir le dán seanaimseartha roghnach (dán a cumadh sa tréimhse roimh 1850) a ndearna tú staidéar air le linn do chúrsa, scríobh síos i d’fhocail féin, '
        'príomhsmaointe an dáin. (9 marc)',
        '(ii) Luaigh íomhá (pictiúr) amháin sa dán atá suimiúil, dar leat. Mínigh an íomhá (an pictiúr) sin i d’fhocail féin. (Is leor dhá phointe eolais.) (7 marc)',
        '(iii) An maith leat an dán seo? Tabhair dhá fháth, i d’fhocail féin, le do fhreagra. (7 marc)'],
     '(c) (i) Maidir le dán seanaimseartha', None, ['(ii) Luaigh íomhá', '(iii) An maith leat', 'Ní mór teideal an dáin']),
]
TITLE_LINE = 'Ní mór teideal an dáin sin, mar aon le hainm an fhile, a scríobh síos go cruinn. (2 mharc)'

_MATERIAL = None


def material():
    global _MATERIAL
    if _MATERIAL:
        return _MATERIAL
    import fitz
    paper_path = ROOT / f'paper-trail-corpus/exampapers/2022/{FILE}.pdf'
    scheme_path = ROOT / f'paper-trail-corpus/markingschemes/2022/{SCHEME_FILE}.pdf'
    assert hashlib.sha256(paper_path.read_bytes()).hexdigest() == PAPER_SHA, 'Paper changed: repeat visual review'
    assert hashlib.sha256(scheme_path.read_bytes()).hexdigest() == SCHEME_SHA, 'Scheme changed: repeat visual review'
    paper, doc = fitz.open(paper_path), fitz.open(scheme_path)
    texts = [clean(p.get_text()) for p in paper]
    s = Scheme(doc, 15, 31)
    # CEIST 1 (PDF 15), A – (50 marc) (16), B – (50 marc) (18), 2A (22), 2B (25), 3A (27), 3B (30).
    assert s.removed == 7, s.removed
    assert not PUA.search(s.text), 'private-use glyph left in the scheme text'
    lang_read = '[Gaeilge lochtach: 0 - 5 a bhaint den iomlán a gnóthaíodh]'
    assert s.text.count(lang_read) == 2
    for letter, passage in PASSAGES.items():
        page_text = ' '.join(texts[p - 1] for p in passage['pages'])
        after = s.text.index(passage['start'])
        # Each passage prints its own two notes above Ceist 1; the PDF 15 copy sits beside the annotation key.
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
            assert '5 mharc' in chunk and '50 marc' not in chunk and 'LÉAMHTHUISCINT' not in chunk, (letter, q, part, chunk[:80])
            two = '3 mharc + 2 mharc' in chunk
            permitted = [0, 3, 5] if (two or '= 3 mharc' in chunk) else [0, 5]
            resolved.append((q, part, prompt, chunk, spages, two, permitted))
        passage['resolved'] = resolved
    # The literature note is printed twice (above 2A on PDF 22 and above 3A on PDF 27), word for word.
    lit_note = s.chunk('Nóta: Níl sé i gceist a chur in iúl go bhfuil na freagraí samplacha', '(a) Oisín i dTír na nÓg (25 marc)')[0]
    assert s.chunk('Nóta: Níl sé i gceist a chur in iúl go bhfuil na freagraí samplacha', '(a) An tEarrach Thiar (25 marc)',
                   s.text.index('⟦27⟧'))[0] == lit_note
    lang_lit = '[Gaeilge lochtach: 0-4 a bhaint den iomlán a gnóthaíodh]'
    # 2A 3 (Dís prints the note with a closing full stop), 2B 3, 3A 3, 3B 3.
    assert s.text.count(lang_lit) == 11 and s.text.count(lang_lit[:-1] + '.]') == 1, s.text.count(lang_lit)
    for slug, atlas, letter, title, topic, intro, subs, start, end in PROSE_SUBS:
        for line in [intro, title] + [p for _, p, _ in subs]:
            assert in_order(line, texts[8]), (slug, line[:40])
    for slug, atlas, letter, title, topic, intro, prompt, start, end in PROSE_WHOLE:
        assert in_order(intro, texts[8]) and in_order(title, texts[8]) and in_order(prompt.removesuffix(' (25 marc)'), texts[8]), slug
    for slug, atlas, lines, start, end, parts, title in PROSE_2B:
        for line in lines:
            assert in_order(line, texts[9]), (slug, line[:50])
    for slug, atlas, page, title, subs, start, end in POETRY_3A:
        assert in_order(title, texts[page - 1]), slug
        for label, prompt, marks, cut in subs:
            assert in_order(prompt.replace('\n', ' ') + f' ({marks} marc)', texts[page - 1]), (slug, label)
    for slug, atlas, prompts, start, end, cuts in POETRY_3B:
        for line in prompts + [TITLE_LINE]:
            assert in_order(line, texts[13]), (slug, line[:50])
    assert comparable(texts[13]).count(comparable(TITLE_LINE)) == 3
    assert comparable(CHOOSE) in comparable(texts[2])
    for page, line in [(9, BOX_2A), (10, BOX_2B), (10, NO_PRESCRIBED_PROSE), (11, BOX_3A), (14, BOX_3B), (14, NO_PRESCRIBED_POETRY)]:
        assert comparable(line) in comparable(texts[page - 1]), line
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
    return pieces, sorted(set(spages) | {22})


def poem_pieces(m, slug, subs, start, end):
    whole, spages = m['s'].chunk(start, end)
    whole = before_language_note(whole)
    pieces = split_at(whole, [cut for _, _, _, cut in subs], slug)
    for (label, _, marks, _), piece in zip(subs, pieces):
        assert f'({marks} marc)' in piece or ((slug, label) in SLOTS_3A and piece.count('(2 mharc)') == 4), (slug, label, piece[:60])
    return pieces, sorted(set(spages) | {27})


def whole_prose(m, start, end):
    chunk, spages = m['s'].chunk(start, end)
    assert '5 phointe eolais agus 5 mharc ar gach pointe eolais' in chunk, start
    return before_language_note(chunk), sorted(set(spages) | {22})


def slot_pieces(piece, slots):
    out = []
    for sub, question, nxt in slots:
        start_at = piece.index(question)
        slot = piece[start_at:piece.index(nxt, start_at) if nxt else len(piece)].strip()
        assert 'Freagra:' in slot and '(2 mharc)' in slot, (sub, slot[:60])
        out.append((sub, slot))
    return out


WHOLE_PROSE_NOTE = ('One complete SEC response: five points at 5 (2 for the bare point + 3 for development); the 0–4 Gaeilge deduction applies once. '
                    'The sample points are indicative rather than exhaustive.')
SLOT_PERMITTED = [0, 2, 4, 6, 8]


def apply_legacy_review(cards):
    """Lift the 2022 scheme onto the 22 retained legacy cards (IDs, totals and topics unchanged)."""
    m = material()
    by_id = {c['id']: c for c in cards}
    stamped = []

    def stamp(card_id, atlas, pages, scheme_pages, criteria, note, requirements, **extra):
        card = by_id[card_id]
        card.update(atlasQuestionId=atlas, reviewedAt=REVIEWED_AT, reviewedPaperPages=pages, schemeFileid=SCHEME_FILE,
                    schemePage=scheme_pages[0], schemePages=scheme_pages, criteria=criteria, markingGuideNote=note,
                    taskRequirements=requirements, **extra)
        assert sum(c['maxMarks'] for c in criteria if c['kind'] == 'award') == card['totalMarks'], card_id
        assert not any('Siombailí Anótála' in g or '50 marc' in g or PUA.search(g) for c in criteria for g in c['guidance']), card_id
        stamped.append(card_id)
        return card

    # Reading: the frozen Atlas identities 1–5 (A) and 6–10 (B) are the whole questions.
    for letter, passage in PASSAGES.items():
        by_q = {}
        for q, part, prompt, chunk, spages, two, permitted in passage['resolved']:
            by_q.setdefault(q, []).append((part, chunk, spages, permitted))
        for q, parts in by_q.items():
            card_id = f'irish-2022-ol-p2-reading-{letter.lower()}-q{q}'
            assert by_id[card_id]['topicId'] == passage['topic'], card_id
            assert in_order(by_id[card_id]['questionText'], ' '.join(m['texts'][p - 1] for p in passage['pages'])), card_id
            crits = [criterion(part, f'({part}) Freagra', 5, [chunk, passage['notes']], permitted=permitted) for part, chunk, _, permitted in parts]
            stamp(card_id, str(int(q) + (5 if letter == 'B' else 0)), passage['pages'], sorted({p for *_, sp, _ in parts for p in sp}), crits,
                  'Retained complete printed question: (a) 5 + (b) 5, each scored separately at its SEC allocation. ' + reading_note(m),
                  READING_WHOLE)

    note = m['lit_note']
    for slug, atlas, letter, title, topic, intro, subs, start, end in PROSE_SUBS:
        assert by_id[f'irish-2022-ol-p2-{slug}']['topicId'] == topic, slug
        pieces, spages = prose_pieces(m, slug, subs, start, end)
        crits = [criterion(f'eolas-{label}', f'({label}) Eolas', 5, [piece, note], 'indicative', permitted=sub_permitted(piece, 5))
                 for (label, _, _), piece in zip(subs, pieces)]
        stamp(f'irish-2022-ol-p2-{slug}', atlas, [9], spages, crits + [deduction(m)],
              'One complete SEC response: five printed sub-questions at 5 each, then the 0–4 Gaeilge deduction once. '
              'The sample answers are indicative rather than exhaustive.',
              [CHOOSE] + LIT, stem=BOX_2A,
              questionText=f'({letter}) {intro}\n{title}\n' + '\n'.join(f'({l}) {p}' for l, p, _ in subs) + '\n(25 marc)',
              sourceMaterial=source('Prós Ainmnithe', title, [9]))

    for slug, atlas, letter, title, topic, intro, prompt, start, end in PROSE_WHOLE:
        assert by_id[f'irish-2022-ol-p2-{slug}']['topicId'] == topic, slug
        chunk, spages = whole_prose(m, start, end)
        stamp(f'irish-2022-ol-p2-{slug}', atlas, [9], spages,
              [criterion('eolas', 'Eolas', 25, [chunk, note], 'indicative'), deduction(m)], WHOLE_PROSE_NOTE,
              [CHOOSE] + LIT[1:], stem=BOX_2A, questionText=f'({letter}) {intro}\n{title}\n{prompt}',
              sourceMaterial=source('Prós Ainmnithe', title, [9]))

    for slug, atlas, lines, start, end, parts, title in PROSE_2B:
        assert by_id[f'irish-2022-ol-p2-{slug}']['topicId'] == 'irish-4-7', slug
        chunk, spages = m['s'].chunk(start, end)
        chunk = before_language_note(chunk)
        cuts = [0] + [chunk.index(cut) for _, _, _, cut in parts[1:]]
        pieces = [chunk[a:b].strip() for a, b in zip(cuts, cuts[1:] + [len(chunk)])]
        # Naming and account depend on the candidate's chosen text (indicative); the title marks are exact.
        crits = [criterion(cid, label, marks, [piece], 'exact' if cid == 'teideal' else 'indicative',
                           permitted=None if cid == 'eolas' else sorted({0, marks} | {int(v) for v in re.findall(r'= (\d) mharc', piece)}))
                 for (cid, label, marks, _), piece in zip(parts, pieces)]
        title_piece = crits[-1]['guidance'][0]
        assert title_piece.endswith('(2 mharc)') or title_piece.count('= 1 mharc') == 2, (slug, title_piece[-60:])
        stamp(f'irish-2022-ol-p2-{slug}', atlas, [10], spages, crits + [deduction(m)],
              'One complete SEC response: ' + ', '.join(f'{label} {marks}' for _, label, marks, _ in parts) +
              ', then the 0–4 Gaeilge deduction once. The optional text is open content chosen by the candidate; the scheme prints no sample '
              'points for it, so its points are judged on merit against these allocations (indicative rather than exhaustive).',
              [CHOOSE, NO_PRESCRIBED_PROSE] + LIT[1:], stem=STEM_2B, questionText='\n'.join(lines),
              sourceMaterial=source('Prós Roghnach', title, [10]))

    for slug, atlas, page, title, subs, start, end in POETRY_3A:
        assert by_id[f'irish-2022-ol-p2-{slug}']['topicId'] == POEM_TOPICS[slug], slug
        pieces, spages = poem_pieces(m, slug, subs, start, end)
        crits = [criterion(f'eolas-{label}', f'({label}) Eolas', marks, [piece, note], 'indicative',
                           permitted=SLOT_PERMITTED if (slug, label) in SLOTS_3A else None)
                 for (label, _, marks, _), piece in zip(subs, pieces)]
        prompt = '\n'.join(f'({label}) {p}' + f' ({marks} marc)' for label, p, marks, _ in subs)
        stamp(f'irish-2022-ol-p2-{slug}', atlas, [page], spages, crits + [deduction(m)],
              'One complete SEC response: (i) 8, (ii) 8, (iii) 9 at their printed tariffs, then the 0–4 Gaeilge deduction once. '
              'The sample points are indicative rather than exhaustive; lines lifted straight from the poem without the candidate’s own words earn 2 + 2.',
              [CHOOSE] + LIT, stem=BOX_3A, questionText=f'({atlas[-1]}) {title}\n' + prompt,
              sourceMaterial=source('Filíocht Ainmnithe', title, [page]))

    for slug, atlas, prompts, start, end, cuts in POETRY_3B:
        assert by_id[f'irish-2022-ol-p2-{slug}']['topicId'] == 'irish-5-6', slug
        chunk, spages = m['s'].chunk(start, end, m['s'].text.index('⟦30⟧'))
        chunk = before_language_note(chunk)
        idx = [0] + [chunk.index(cut) for cut in cuts]
        pieces = [chunk[a:b].strip() for a, b in zip(idx, idx[1:] + [len(chunk)])]
        for piece, cap in zip(pieces, ['(9 marc)', '(7 marc)', '(7 marc)', '(2 mharc)']):
            assert cap in piece, (slug, cap)
        crits = [criterion('eolas-i', '(i) Eolas', 9, [pieces[0]], 'indicative'), criterion('eolas-ii', '(ii) Eolas', 7, [pieces[1]], 'indicative'),
                 criterion('eolas-iii', '(iii) Eolas', 7, [pieces[2]], 'indicative'),
                 criterion('teideal', 'Teideal + ainm an fhile', 2, [pieces[3]], 'exact')]
        stamp(f'irish-2022-ol-p2-{slug}', atlas, [14], spages, crits + [deduction(m)],
              'One complete SEC response: (i) 9, (ii) 7, (iii) 7, poem and poet 2, then the 0–4 Gaeilge deduction once. '
              'The optional poem is open content; 3B(b) asks for a modern poem not used in 3B(a). The printed allocations are judged on merit '
              '(indicative rather than exhaustive).',
              [CHOOSE, NO_PRESCRIBED_POETRY] + LIT, stem=STEM_3B, questionText=f'({atlas[-1]}) ' + '\n'.join(prompts + [TITLE_LINE]),
              sourceMaterial=source('Filíocht Roghnach', f'3B({atlas[-1]}) · Dán roghnach', [14]))
    assert len(stamped) == 22
    return cards, stamped


def build():
    m = material()
    cards = []

    def add(key, slug, ref, prompt, topic, pages, scheme_pages, criteria, requirements, note, src, stem=None):
        cards.append(dict(
            id=f'irish-2022-ol-p2-{slug}', year=2022, level='ordinary', paper=2, section='2',
            atlasQuestionId=key, questionRef=f'2022 OL Paper 2 {ref}', **({'stem': stem} if stem else {}), questionText=prompt,
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
        src = source('Prós Ainmnithe', title, [9])
        for (label, prompt, _), piece in zip(subs, pieces):
            # The paper prints no per-sub-question tariff for 2A(a); the scheme prices each at (5 mharc).
            add(f'{atlas}-{label}', f'{slug}-{label}', f'Prós 2A({letter}) · {title} · ({label})', f'({letter}) {intro}\n{title}\n({label}) {prompt}',
                topic, [9], spages, [criterion('eolas', 'Eolas', 5, [piece, note], 'indicative', permitted=sub_permitted(piece, 5))],
                [CHOOSE] + LIT[1:], sub_note, src, stem=BOX_2A)

    for slug, atlas, page, title, subs, start, end in POETRY_3A:
        pieces, spages = poem_pieces(m, slug, subs, start, end)
        topic = POEM_TOPICS[slug]
        src = source('Filíocht Ainmnithe', title, [page])
        head = f'({atlas[-1]}) {title}\n'
        for (label, prompt, marks, _), piece in zip(subs, pieces):
            slots = SLOTS_3A.get((slug, label))
            add(f'{atlas}-{label}', f'{slug}-{label}', f'Filíocht 3A({atlas[-1]}) · {title} · ({label})', head + f'({label}) {prompt} ({marks} marc)',
                topic, [page], spages,
                [criterion('eolas', 'Eolas', marks, [piece, note], 'indicative', permitted=SLOT_PERMITTED if slots else None)],
                [CHOOSE] + LIT[1:], sub_note, src, stem=BOX_3A)
            if slots:
                printed = dict(re.findall(r'\(([a-d])\) ([^\n]+)', prompt))
                for sub, slot in slot_pieces(piece, slots):
                    add(f'{atlas}-{label}-{sub}', f'{slug}-{label}-{sub}', f'Filíocht 3A({atlas[-1]}) · {title} · ({label})({sub})',
                        head + f'({label}) ({sub}) {printed[sub]}', topic, [page], spages,
                        [criterion('eolas', 'Freagra', 2, [slot], 'exact', permitted=[0, 2])], [CHOOSE] + LIT[1:],
                        f'One printed 2-mark question inside 3A({atlas[-1]})({label}). Scheme: “{lang}” applies to the whole 25-mark answer.', src,
                        stem=BOX_3A)

    assert len(cards) == 42 and len({c["id"] for c in cards}) == 42 and len({c["atlasQuestionId"] for c in cards}) == 42
    for card in cards:
        for c in card['criteria']:
            assert c['guidance'] and all(not re.search('Siombailí Anótála|50 marc', g) and not PUA.search(g) for g in c['guidance']), (card['id'], c['id'])
    sr = json.loads(SOURCE_REVIEW.read_text())
    legacy = ([f'irish-2022-ol-p2-reading-{l}-q{q}' for l in 'ab' for q in range(1, 6)]
              + [f'irish-2022-ol-p2-prose-{k}' for k in ['2a-a', '2a-b', '2a-c', '2b-a', '2b-b', '2b-c']]
              + [f'irish-2022-ol-p2-poetry-{k}' for k in ['3a-a', '3a-b', '3a-c', '3b-a', '3b-b', '3b-c']])
    review = dict(year=2022, level='ordinary', paperFileid=FILE + '.pdf', schemeFileid=SCHEME_FILE + '.pdf',
                  paperSha256=PAPER_SHA, schemeSha256=SCHEME_SHA,
                  reviewedPaperPages=list(range(1, 17)), reviewedSchemePages=sr['reviewedSchemePages'], schemeScope=sr['schemeScope'],
                  reviewDate=REVIEWED_AT, status='reviewed', fullPaperAndApplicableSchemeVisualSweep=True, selectionDecisions=m['decisions'],
                  practiceCardIds=[c['id'] for c in cards], legacyCardIds=legacy, readingWholeCardIds=legacy[:10],
                  examStructure=dict(readingA=50, readingB=50, prose=50, poetry=50, total=200),
                  nonPoolDecisions=sr['nonPoolDecisions'], openIssues=[], caveats=sr['sourceFindings'],
                  choicePolicy=('Choice is not a route: each printed option of 2A, 2B, 3A and 3B is one card carrying the printed instruction '
                                '“Freagair dhá cheist as an roinn seo.”; no combination cards. 2A(c) prints one text in 2022 (Dís).'),
                  boundaries=('10 retained whole reading questions with their 20 published parts; 12 retained literature options; '
                              'the 5 printed 2A(a) Oisín i dTír na nÓg sub-questions, the 9 prescribed-poetry sub-questions and the '
                              '8 printed 2-mark questions inside 3A(a)(i) and 3A(c)(ii).'))
    return dict(review=review, cards=cards)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    data = build()
    printed_lead_in(data['cards'])  # the section's printed lines lead in to the question
    scheme_words_in(data)  # guidance carries the SEC's words only (irish_lifted.py)
    content = json.dumps(data, ensure_ascii=False, indent=2) + '\n'
    if args.check:
        assert OUT.exists() and OUT.read_text() == content, f'Stale output: {OUT}'
    else:
        OUT.write_text(content)
    print(f"Irish Ordinary 2022 Paper 2: {len(data['cards'])} added practice cards (+22 retained legacy cards); the archive remains incomplete.")


if __name__ == '__main__':
    main()
