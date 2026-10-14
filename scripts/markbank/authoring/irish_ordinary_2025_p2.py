#!/usr/bin/env python3
"""Reviewed 2025 Ordinary Paper 2 (Léamhthuiscint agus Litríocht).

Paper PDF 1–16 and the Paper 2 pages of the combined LC001GLP000IV scheme
(PDF 14–29, plus 30 modified marking) visually reviewed on 2026-10-12. Counts are
assertions, not corpus-completeness proof.

The legacy generator already ships 22 cards for this component: the ten whole
reading questions and the twelve literature options. Their IDs, totals and topics
are kept. `apply_legacy_review` (called by irish_cards.py) joins them to Atlas and
replaces their marking with the lifted 2025 scheme: each reading part and each
poetry sub-question keeps its own published tariff, and the optional answers keep
their naming, theme and title marks. `build` adds every reading part (20), every
prescribed-poetry sub-question (9) and the three printed 3A(a)(i) questions as
practice cards beside the legacy file.

Choice is not a route: “Freagair do rogha dhá cheann as (a), (b) nó (c)” sits in
each option's task requirements; no card combines two options.
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
OUT = ROOT / 'components/MarkBank/cards/irish/ordinary-2025-p2-authored.json'
SOURCE_REVIEW = ROOT / 'scripts/markbank/authored/irish-ordinary-2025-p2-source-review.json'
REVIEWED_AT = '2026-10-12'
PAPER_SHA = '30241c45f630f7a0c4b35f744d2902ad8ff0a9f59183d109f62521da556d0c63'
SCHEME_SHA = '709a6ffc8a0c6c700ff4132993a2058363ac028f0dca21ae23eef0fa26f95831'
DIRECTIVE = re.compile(r'rogha|roghna|Freagair|Luaigh|Ainmnigh|\bnó\b|dhá phointe|dhá rud|dhá bh|dhá dh|dhá ch|dhá fh|dhá th|dhá ph|dhá sh|'
                       r'\ban dá\b|ceann amháin|pointe amháin|amháin|\bdhá\b', re.I)
SOURCE_NOTE = 'Shown page-for-page from the official examination paper; swipe to move between pages.'
ATTRIBUTION = '© State Examinations Commission.'
# The scheme's text layer splits one printed word (“ceann”, visually checked on PDF 23).
TEXT_REPAIRS = [('an cea nn ar an gcéad trí', 'an ceann ar an gcéad trí')]


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
        for broken, printed in TEXT_REPAIRS:
            assert self.text.count(broken) == 1, broken
            self.text = self.text.replace(broken, printed)

    def chunk(self, start, end=None, after=0):
        i = self.text.index(start, after)
        j = self.text.index(end, i + len(start)) if end else len(self.text)
        raw = self.text[i:j]
        pages = {int(re.findall(r'⟦(\d+)⟧', self.text[:i])[-1])}
        pages |= {int(m.group(1)) for m in re.finditer(r'⟦(\d+)⟧([^⟦]*)', raw) if clean(m.group(2)) not in ('', 'nó')}
        return clean(re.sub(r'⟦\d+⟧', ' ', raw)), sorted(pages)


def before_language_note(text):
    return re.split(r'\[\s*Gaeilge lochtach', text)[0].strip()


# (q, part, paper prompt, scheme anchor)
PASSAGES = {
    'A': dict(title='Na Cluichí Oilimpeacha agus Parailimpeacha, 2024', pages=[4, 5], topic='irish-3-0', start='⟦15⟧', parts=[
        ('1', 'a', '(a) Cén rud faoi shearmanas oscailte na gCluichí Oilimpeacha i bPáras a bhí difriúil le blianta eile? (Alt 1)', '1. (a) Cén rud faoi shearmanas'),
        ('1', 'b', '(b) Cad a tharla don choire a raibh an bhladhm Oilimpeach ar lasadh istigh ann? (Alt 1)', '(b) Cad a tharla don choire'),
        ('2', 'a', '(a) Scríobh síos an dá phíosa eolais faoi líon na lúthchleasaithe a bhí ar fhoireann Oilimpeach na hÉireann a seoladh chuig na Cluichí Oilimpeacha i bPáras in 2024. (Alt 2)', '2. (a) Scríobh síos an dá phíosa'),
        ('2', 'b', '(b) Luaigh dhá rud a bhí ar na lúthchleasaithe a dhéanamh chun cáiliú do na Cluichí Oilimpeacha ina rogha spóirt. (Alt 2)', '(b) Luaigh dhá rud a bhí ar na lúthchleasaithe'),
        ('3', 'a', '(a) Cén fáth a bhfuil áit faoi leith bainte amach ag an rámhaí Paul O’Donovan i stair na gCluichí Oilimpeacha sa tír seo? (Alt 3)', '3. (a) Cén fáth a bhfuil áit faoi leith'),
        ('3', 'b', '(b) Scríobh síos dhá phíosa eolais a thugtar faoin ngleacaí Rhys McClenaghan ag na Cluichí Oilimpeacha i bPáras. (Alt 3)', '(b) Scríobh síos dhá phíosa eolais a thugtar'),
        ('4', 'a', '(a) Cad a chinntigh clúdach fairsing RTÉ ar na Cluichí Oilimpeacha do mhuintir na hÉireann sa bhaile? (Alt 4)', '4. (a) Cad a chinntigh'),
        ('4', 'b', '(b) Conas a rinne Kellie Harrington agus a lucht leanúna ceiliúradh sa staid nuair a fógraíodh í mar sheaimpín Oilimpeach ag deireadh na troda? (Alt 4)', '(b) Conas a rinne Kellie'),
        ('5', 'a', '(a) Cén fáth a raibh bród ar mhuintir na hÉireann as lúthchleasaithe Parailimpeacha na tíre seo ag na Cluichí Parailimpeacha i bPáras anuraidh? (Alt 5)', '5. (a) Cén fáth a raibh bród'),
        ('5', 'b', '(b) Conas a chabhróidh an infheistíocht bhreise ón rialtas leis na lúthchleasaithe agus iad ag iarraidh cáiliú do na Cluichí Oilimpeacha agus Parailimpeacha in 2028? (Alt 5)', '(b) Conas a chabhróidh')]),
    'B': dict(title='Páirc an Fhionnuisce', pages=[6, 7], topic='irish-3-1', start='⟦17⟧', parts=[
        ('1', 'a', '(a) Cén fáth a bhfuil cáil ar Pháirc an Fhionnuisce sa lá atá inniu ann? (Alt 1)', '1. (a) Cén fáth a bhfuil cáil'),
        ('1', 'b', '(b) Luaigh dhá rud a rinneadh faoi phlean Decimus Burton i bPáirc an Fhionnuisce. (Alt 1)', '(b) Luaigh dhá rud a rinneadh'),
        ('2', 'a', '(a) Cén úsáid a baineadh as Dún na hArmlainne fadó? (Alt 2)', '2. (a) Cén úsáid'),
        ('2', 'b', '(b) Scríobh síos dhá phíosa eolais faoi Zú Bhaile Átha Cliath atá suite i bPáirc an Fhionnuisce. (Alt 2)', '(b) Scríobh síos dhá phíosa eolais faoi Zú'),
        ('3', 'a', '(a) Scríobh síos dhá phíosa eolais faoi na tailte atá i bPáirc an Fhionnuisce. (Alt 3)', '3. (a) Scríobh síos dhá phíosa eolais faoi na tailte'),
        ('3', 'b', '(b) Luaigh dhá chúis a dtagann a lán daoine go Páirc an Fhionnuisce. (Alt 3)', '(b) Luaigh dhá chúis'),
        ('4', 'a', '(a) Scríobh síos dhá phíosa eolais faoi chuairt an Phápa Eoin Pól II ar Pháirc an Fhionnuisce i mí Mheán Fómhair 1979. (Alt 4)', '4. (a) Scríobh síos dhá phíosa eolais faoi chuairt'),
        ('4', 'b', '(b) Tabhair dhá phíosa eolais faoi imeachtaí spóirt i bPáirc an Fhionnuisce. (Alt 4)', '(b) Tabhair dhá phíosa eolais faoi imeachtaí'),
        ('5', 'a', '(a) Scríobh síos an dá rud a iarrtar ar chuairteoirí a dhéanamh mar chuid den fheachtas speisialta chun na fianna a chosaint sa pháirc. (Alt 5)', '5. (a) Scríobh síos an dá rud'),
        ('5', 'b', '(b) Luaigh dhá rud atá i bpleananna Oifig na nOibreacha Poiblí chun cúrsaí sábháilteachta sa pháirc a fheabhsú. (Alt 5)', '(b) Luaigh dhá rud atá i bpleananna')]),
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
NO_PRESCRIBED_PROSE = 'Níl cead aon ábhar a bhaineann le Prós Ainmnithe a úsáid sna freagraí ar an bPrós Roghnach.'
NO_PRESCRIBED_POETRY = 'Níl cead aon ábhar a bhaineann le Filíocht Ainmnithe a úsáid sna freagraí ar an bhFilíocht Roghnach.'
SAME_POEM = 'Níl cead an dán roghnach céanna a úsáid faoi dhó sna freagraí ar (a), (b) nó (c) thíos.'
LIT = ['Freagair gach fochuid atá priontáilte sa rogha seo.', 'Úsáid tagairtí cruinne agus ábhartha don téacs.']
READING_PART = ['Léigh an sliocht iomlán a ghabhann leis an gceist. Freagair an chuid atá luaite ar an gcárta.', 'Úsáid an t-alt a luaitear.']
READING_WHOLE = ['Léigh an sliocht oifigiúil a ghabhann leis an gceist.', 'Freagair gach fochuid agus cloígh leis an alt a luaitear.']

# Prescribed prose (2A): one printed 25-mark question each. (slug, atlas, paper lines, scheme start, scheme end, source title)
PROSE_2A = [
    ('prose-2a-a', 'P-2A-a', ['(a) Freagair an cheist thíos faoin ngearrscéal Dís.', 'Dís',
                              '‘Tá sé ansan anois os comhair do dhá shúl. Mise duine des na mná a bhí sa tsuirbhé sin.’',
                              'Déan cur síos ar an gcomhrá a bhí idir Seán agus a bhean chéile an tráthnóna sin. (25 marc)'],
     '(a) Dís', '(b) Oisín i dTír na nÓg', 'Dís'),
    ('prose-2a-b', 'P-2A-b', ['(b) Freagair an cheist thíos faoin scéal béaloidis Oisín i dTír na nÓg.', 'Oisín i dTír na nÓg',
                              '‘Shil na deora frasa anuas le grua Oisín agus phóg sé a athair go caoin.’',
                              'Déan cur síos ar an saghas saoil a bhí ag Oisín ón uair a d’fhág sé Fionn agus na Fianna go dtí deireadh an scéil. (25 marc)'],
     '(b) Oisín i dTír na nÓg', '(c) Hurlamaboc', 'Oisín i dTír na nÓg'),
    ('prose-2a-c', 'P-2A-c', ['(c) Freagair an cheist thíos faoin ngiota as an úrscéal Hurlamaboc.', 'Hurlamaboc',
                              '‘Fiche bliain ó shin a pósadh Lisín agus Pól. Bheadh an ócáid iontach á ceiliúradh acu i gceann seachtaine.’',
                              'Déan cur síos ar an gcineál saoil a bhí ag Lisín ó pósadh í fiche bliain ó shin. (25 marc)'],
     '(c) Hurlamaboc', 'Níl cead aon ábhar a bhaineann le Prós Ainmnithe', 'Hurlamaboc'),
]
# Optional prose (2B): (slug, atlas, paper lines, scheme start, scheme end, [(id, label, marks, cut-before)])
PROSE_2B = [
    ('prose-2b-a', 'P-2B-a', ['(a) Maidir le gearrscéal roghnach a ndearna tú staidéar air le linn do chúrsa, tabhair cuntas ar na príomhimeachtaí (príomhrudaí) a tharlaíonn sa ghearrscéal sin. (23 marc)',
                              'Ní mór teideal an ghearrscéil sin, mar aon le hainm an údair, a scríobh síos go cruinn. (2 mharc)'],
     '(a) Maidir le gearrscéal roghnach', '(b) Maidir le scéal béaloidis roghnach',
     [('eolas', 'Príomhimeachtaí', 23, None), ('teideal', 'Teideal + ainm an údair', 2, 'Ní mór teideal')], 'Gearrscéal roghnach'),
    ('prose-2b-b', 'P-2B-b', ['(b) Maidir le scéal béaloidis roghnach a ndearna tú staidéar air le linn do chúrsa, ainmnigh an phríomhphearsa (an príomhcharachtar) sa scéal béaloidis sin. Tabhair cuntas ar na heachtraí is mó a tharlaíonn don duine sin ó thús go deireadh an scéil. (23 marc)',
                              'Ní mór teideal an scéil béaloidis sin a scríobh síos go cruinn. (2 mharc)'],
     '(b) Maidir le scéal béaloidis roghnach', '2B PRÓS ROGHNACH',
     [('priomhphearsa', 'An phríomhphearsa a ainmniú', 1, None), ('eolas', 'Na heachtraí is mó', 22, 'Na heachtraí is mó'),
      ('teideal', 'Teideal an scéil béaloidis', 2, 'Ní mór teideal')], 'Scéal béaloidis roghnach'),
    ('prose-2b-c', 'P-2B-c', ['(c) Maidir le giota as úrscéal roghnach a ndearna tú staidéar air le linn do chúrsa, scríobh síos príomhthéama an ghiota sin, dar leat. Tabhair cuntas ar na heachtraí is mó a léiríonn an príomhthéama sin sa ghiota. (23 marc)',
                              'Ní mór teideal an úrscéil sin, mar aon le hainm an údair, a scríobh síos go cruinn. (2 mharc)'],
     '(c) Maidir le giota as úrscéal roghnach', '3A FILÍOCHT AINMNITHE',
     [('priomhthema', 'An príomhthéama a lua', 1, None), ('eolas', 'Na heachtraí is mó', 22, 'Na heachtraí is mó'),
      ('teideal', 'Teideal + ainm an údair', 2, 'Ní mór teideal')], 'Giota as úrscéal roghnach'),
]
# Prescribed poetry (3A): (slug, atlas, page, title, sub-questions [(label, paper prompt, marks, scheme cut)], scheme start, scheme end)
POETRY_3A = [
    ('poetry-3a-a', 'F-3A-a', 10, 'Mo ghrá-sa (idir lúibíní)', [
        ('i', '(a) Cén bláth a luann an file i véarsa a haon?\n(b) Cad a deir an file faoi na nóiníní i véarsa a dó?\n(c) Scríobh síos dhá rud a deir an file faoi ghruaig an fhir i véarsa a ceathair.', 8, '(i) (a) Cén bláth'),
        ('ii', 'Scríobh síos dhá phointe eolais, i d’fhocail féin, faoi shúile an fhir i véarsa a trí den dán.', 8, '(ii) Scríobh síos dhá phointe eolais'),
        ('iii', 'Tabhair dhá phointe eolais, i d’fhocail féin, faoin íomhá (faoin bpictiúr) den fhear a thugann an file dúinn i véarsa a cúig den dán.', 9, '(iii) Tabhair dhá phointe eolais')],
     '(a) Mo ghrá-sa (idir lúibíní)', '(b) An tEarrach Thiar'),
    ('poetry-3a-b', 'F-3A-b', 11, 'An tEarrach Thiar', [
        ('i', 'Déan cur síos, i d’fhocail féin, ar an íomhá (ar an bpictiúr) den fhear a thugann an file dúinn i véarsa a dó den dán. (Is leor dhá phointe eolais.)', 8, '(i) Déan cur síos'),
        ('ii', 'Scríobh síos, i d’fhocail féin, dhá phointe eolais faoi na mná i véarsa a trí.', 8, '(ii) Scríobh síos, i d’fhocail féin'),
        ('iii', 'Tabhair dhá phointe eolais, i d’fhocail féin, faoin íomhá (faoin bpictiúr) den churrach a thugann an file dúinn i véarsa a ceathair.', 9, '(iii) Tabhair dhá phointe eolais')],
     '(b) An tEarrach Thiar', '(c) Colscaradh'),
    ('poetry-3a-c', 'F-3A-c', 12, 'Colscaradh', [
        ('i', 'Déan cur síos, i d’fhocail féin, ar dhá rud a theastaíonn ón bhfear ina shaol pósta i véarsa a haon den dán.', 8, '(i) Déan cur síos'),
        ('ii', 'Tabhair dhá phointe eolais, i d’fhocail féin, faoin gcineál duine í an bhean i véarsa a dó.', 8, '(ii) Tabhair dhá phointe eolais'),
        ('iii', 'An maith leat an dán seo? Tabhair dhá fháth, i d’fhocail féin, le do fhreagra.', 9, '(iii) An maith leat')],
     '(c) Colscaradh', '3B FILÍOCHT ROGHNACH'),
]
# 3A(a)(i) prints three questions: (a) 2, (b) 2, (c) 2 + 2.
SLOTS_3A_A = [('a', 'Cén bláth a luann an file i véarsa a haon?', 2, '(b) Cad a deir', [0, 2]),
              ('b', 'Cad a deir an file faoi na nóiníní i véarsa a dó?', 2, '(c) Scríobh síos dhá rud', [0, 2]),
              ('c', 'Scríobh síos dhá rud a deir an file faoi ghruaig an fhir i véarsa a ceathair.', 4, None, [0, 2, 4])]
# Optional poetry (3B): (slug, atlas, sub-question prompts, scheme start, scheme end, cuts, caps)
POETRY_3B = [
    ('poetry-3b-a', 'F-3B-a', [
        '(i) Maidir le dán nua‐aimseartha roghnach a ndearna tú staidéar air le linn do chúrsa, scríobh síos príomhthéama an dáin sin, dar leat. Tabhair dhá phointe eolais, i d’fhocail féin, faoin bpríomhthéama sin sa dán. (9 marc)',
        '(ii) Luaigh íomhá (pictiúr) amháin as an dán atá suimiúil, dar leat. Tabhair dhá phointe eolais, i d’fhocail féin, faoin íomhá (faoin bpictiúr) sin. (7 marc)',
        '(iii) Cén t‐atmaisféar atá sa dán seo, dar leat? Tabhair dhá shampla den atmaisféar sin sa dán. (7 marc)'],
     '(a) (i) Maidir le dán nua-aimseartha', '(b) (i) Maidir le dán nua-aimseartha', ['(ii) Luaigh íomhá', '(iii) Cén t-atmaisféar', 'Ní mór teideal an dáin']),
    ('poetry-3b-b', 'F-3B-b', [
        '(i) Maidir le dán nua‐aimseartha roghnach a ndearna tú staidéar air le linn do chúrsa, scríobh síos príomhthéama an dáin sin, dar leat. Tabhair dhá phointe eolais, i d’fhocail féin, faoin bpríomhthéama sin sa dán. (9 marc)',
        '(ii) Scríobh síos an mothúchán is láidre atá sa dán, dar leat. Tabhair dhá shampla, i d’fhocail féin, den mhothúchán sin sa dán. (7 marc)',
        '(iii) Scríobh síos an rud is mó a thaitníonn leat sa dán seo. Tabhair dhá fháth, i d’fhocail féin, le do fhreagra. (7 marc)'],
     '(b) (i) Maidir le dán nua-aimseartha', '(c) (i) Maidir le dán nua-aimseartha', ['(ii) Scríobh síos an mothúchán', '(iii) Scríobh síos an rud', 'Ní mór teideal an dáin']),
    ('poetry-3b-c', 'F-3B-c', [
        '(i) Maidir le dán nua‐aimseartha roghnach a ndearna tú staidéar air le linn do chúrsa, scríobh síos, i d’fhocail féin, príomhsmaointe an dáin sin. (9 marc)',
        '(ii) Roghnaigh íomhá (pictiúr) amháin a úsáideann an file sa dán seo. Mínigh an íomhá (an pictiúr) sin i d’fhocail féin. (Is leor dhá phointe eolais.) (7 marc)',
        '(iii) An maith leat an dán seo? Tabhair dhá fháth, i d’fhocail féin, le do fhreagra. (7 marc)'],
     '(c) (i) Maidir le dán nua-aimseartha', None, ['(ii) Roghnaigh íomhá', '(iii) An maith leat', 'Ní mór teideal an dáin']),
]
TITLE_LINE = 'Ní mór teideal an dáin sin, mar aon le hainm an fhile, a scríobh síos go cruinn. (2 mharc)'
# The legacy routes' topics; the sub-question cards inherit them.
POEM_TOPICS = {'poetry-3a-a': 'irish-5-4', 'poetry-3a-b': 'irish-5-3', 'poetry-3a-c': 'irish-5-5'}

_MATERIAL = None


def material():
    global _MATERIAL
    if _MATERIAL:
        return _MATERIAL
    import fitz
    paper_path = ROOT / f'paper-trail-corpus/exampapers/2025/{FILE}.pdf'
    scheme_path = ROOT / f'paper-trail-corpus/markingschemes/2025/{SCHEME_FILE}.pdf'
    assert hashlib.sha256(paper_path.read_bytes()).hexdigest() == PAPER_SHA, 'Paper changed: repeat visual review'
    assert hashlib.sha256(scheme_path.read_bytes()).hexdigest() == SCHEME_SHA, 'Scheme changed: repeat visual review'
    paper, doc = fitz.open(paper_path), fitz.open(scheme_path)
    texts = [clean(p.get_text()) for p in paper]
    s = Scheme(doc, 14, 29)
    lang_read = '[Gaeilge lochtach: 0 - 5 a bhaint den iomlán a gnóthaíodh]'
    assert s.text.count(lang_read) == 2
    for letter, passage in PASSAGES.items():
        page_text = ' '.join(texts[p - 1] for p in passage['pages'])
        after = s.text.index(passage['start'])
        # Each passage prints its own two notes above Ceist 1 (PDF 15 and 17); the page-14 copy sits beside the annotation key.
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
    assert s.text.count(lang_lit) == 12
    for page, lines in [(8, [l for p in PROSE_2A for l in p[2]]), (9, [l for p in PROSE_2B for l in p[2]])]:
        for line in lines:
            assert in_order(re.sub(r' \((23|25) marc\)$| \(2 mharc\)$', '', line), texts[page - 1]), (page, line[:50])
    for slug, atlas, page, title, subs, start, end in POETRY_3A:
        for label, prompt, marks, cut in subs:
            assert in_order(prompt.replace('\n', ' '), texts[page - 1]), (slug, label)
    for slug, atlas, prompts, start, end, cuts in POETRY_3B:
        for line in prompts + [TITLE_LINE]:
            assert in_order(line, texts[12]), (slug, line[:50])
    assert comparable(TITLE_LINE) in comparable(texts[12]) and comparable(texts[12]).count(comparable(TITLE_LINE)) == 3
    for line in (NO_PRESCRIBED_PROSE, CHOOSE):
        assert comparable(line) in comparable(texts[8]), line
    for line in (NO_PRESCRIBED_POETRY, CHOOSE, SAME_POEM):
        assert comparable(line) in comparable(texts[12]), line
    assert comparable(CHOOSE_3A) in comparable(texts[9])
    _MATERIAL = dict(paper=paper, texts=texts, s=s, lang_read=lang_read, lit_note=lit_note,
                     lang_lit=lang_lit, decisions=selection_decisions(paper))
    return _MATERIAL


def deduction(m):
    return criterion('gaeilge-deduction', 'Gaeilge lochtach', 4, [m['lang_lit'] + ' — applied once to this whole 25-mark answer.'], 'quality', deduction=True)


def reading_note(m):
    return ('Scheme: “' + m['lang_read'] + '” — one deduction from each passage total (50), never inside a single part.')


def source(label, title, pages):
    return dict(kind='source-text', label=label, title=title, pages=pages, attribution=ATTRIBUTION, presentationNote=SOURCE_NOTE)


def prescribed_poem(m, slug, subs, start, end):
    """The whole poem chunk and one scheme piece per printed sub-question (language note removed)."""
    s = m['s']
    whole, spages = s.chunk(start, end)
    whole = before_language_note(whole)
    cuts = [whole.index(cut) for _, _, _, cut in subs]
    assert cuts == sorted(cuts) and cuts[0] > 0, slug
    pieces = [whole[a:b].strip() for a, b in zip(cuts, cuts[1:] + [len(whole)])]
    for (label, _, marks, _), piece in zip(subs, pieces):
        assert f'({marks} marc)' in piece or (label == 'i' and '(2 mharc + 2 mharc)' in piece), (slug, label, piece[:60])
    return pieces, spages


def apply_legacy_review(cards):
    """Lift the 2025 scheme onto the 22 retained legacy cards (IDs, totals and topics unchanged)."""
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
            card_id = f'irish-2025-ol-p2-reading-{letter.lower()}-q{q}'
            assert in_order(by_id[card_id]['questionText'], ' '.join(m['texts'][p - 1] for p in passage['pages'])), card_id
            crits = [criterion(part, f'({part}) Freagra', 5, [chunk, passage['notes']], permitted=permitted) for part, chunk, _, permitted in parts]
            stamp(card_id, str(int(q) + (5 if letter == 'B' else 0)), passage['pages'], sorted({p for *_, sp, _ in parts for p in sp}), crits,
                  'Retained complete printed question: (a) 5 + (b) 5, each scored separately at its SEC allocation. ' + reading_note(m),
                  READING_WHOLE)

    s, note = m['s'], m['lit_note']
    for slug, atlas, lines, start, end, title in PROSE_2A:
        chunk, spages = s.chunk(start, end)
        chunk = before_language_note(chunk)
        assert '5 phointe eolais agus 5 mharc ar gach pointe eolais' in chunk, slug
        stamp(f'irish-2025-ol-p2-{slug}', atlas, [8], sorted(set(spages) | {20}),
              [criterion('eolas', 'Eolas', 25, [chunk, note], 'indicative'), deduction(m)],
              'One complete SEC response: five points at 5 (2 for the bare point + 3 for development); the 0–4 Gaeilge deduction applies once. '
              'The sample points are indicative rather than exhaustive.',
              [CHOOSE] + LIT[1:], questionText=HEAD2A + '\n' + '\n'.join(lines), sourceMaterial=source('Prós Ainmnithe', title, [8]))

    for slug, atlas, lines, start, end, parts, title in PROSE_2B:
        chunk, spages = s.chunk(start, end)
        chunk = before_language_note(chunk)
        cuts = [0] + [chunk.index(cut) for _, _, _, cut in parts[1:]]
        pieces = [chunk[a:b].strip() for a, b in zip(cuts, cuts[1:] + [len(chunk)])]
        # Printed values only: a 1-mark naming/theme award is 0/1; a title worth “= 2 mharc” on its own is 0/2;
        # title 1 + author 1 allows 0/1/2. The account itself is indicative (full range).
        # Naming, theme and account depend on the candidate's chosen text (indicative); the title marks are exact.
        crits = [criterion(cid, label, marks, [piece], 'exact' if cid == 'teideal' else 'indicative',
                           permitted=None if cid == 'eolas' else sorted({0, marks} | {int(v) for v in re.findall(r'= (\d) mharc', piece)}))
                 for (cid, label, marks, _), piece in zip(parts, pieces)]
        for c in crits:
            if c['id'] == 'teideal':
                assert c['guidance'][0].endswith('(2 mharc)'), (slug, c['guidance'])
        stamp(f'irish-2025-ol-p2-{slug}', atlas, [9], spages, crits + [deduction(m)],
              'One complete SEC response: ' + ', '.join(f'{label} {marks}' for _, label, marks, _ in parts) +
              ', then the 0–4 Gaeilge deduction once. The optional text is open content chosen by the candidate; the scheme prints no sample '
              'points for it, so its points are judged on merit against these allocations (indicative rather than exhaustive).',
              [CHOOSE, NO_PRESCRIBED_PROSE] + LIT[1:], questionText=HEAD2B + '\n' + '\n'.join(lines),
              sourceMaterial=source('Prós Roghnach', title, [9]))

    for slug, atlas, page, title, subs, start, end in POETRY_3A:
        assert by_id[f'irish-2025-ol-p2-{slug}']['topicId'] == POEM_TOPICS[slug], slug
        pieces, spages = prescribed_poem(m, slug, subs, start, end)
        crits = [criterion(f'eolas-{label}', f'({label}) Eolas', marks, [piece, note], 'indicative',
                           permitted=[0, 2, 4, 6, 8] if (slug, label) == ('poetry-3a-a', 'i') else None)
                 for (label, _, marks, _), piece in zip(subs, pieces)]
        prompt = '\n'.join(f'({label}) {p}' + f' ({marks} marc)' for label, p, marks, _ in subs)
        stamp(f'irish-2025-ol-p2-{slug}', atlas, [page], spages, crits + [deduction(m)],
              'One complete SEC response: (i) 8, (ii) 8, (iii) 9 at their printed tariffs, then the 0–4 Gaeilge deduction once. '
              'The sample points are indicative rather than exhaustive; lines lifted straight from the poem without the candidate’s own words earn 2 + 2.',
              [CHOOSE_3A] + LIT, questionText=HEAD3A + f'\n({atlas[-1]}) {title}\n' + prompt,
              sourceMaterial=source('Filíocht Ainmnithe', title, [page]))

    for slug, atlas, prompts, start, end, cuts in POETRY_3B:
        chunk, spages = s.chunk(start, end, s.text.index('⟦28⟧'))
        chunk = before_language_note(chunk)
        idx = [0] + [chunk.index(cut) for cut in cuts]
        pieces = [chunk[a:b].strip() for a, b in zip(idx, idx[1:] + [len(chunk)])]
        for piece, cap in zip(pieces, ['(9 marc)', '(7 marc)', '(7 marc)', '(2 mharc)']):
            assert cap in piece, (slug, cap)
        crits = [criterion('eolas-i', '(i) Eolas', 9, [pieces[0]], 'indicative'), criterion('eolas-ii', '(ii) Eolas', 7, [pieces[1]], 'indicative'),
                 criterion('eolas-iii', '(iii) Eolas', 7, [pieces[2]], 'indicative'),
                 criterion('teideal', 'Teideal + ainm an fhile', 2, [pieces[3]], 'exact')]
        stamp(f'irish-2025-ol-p2-{slug}', atlas, [13], spages, crits + [deduction(m)],
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
            id=f'irish-2025-ol-p2-{slug}', year=2025, level='ordinary', paper=2, section='2',
            atlasQuestionId=key, questionRef=f'2025 OL Paper 2 {ref}', questionText=prompt,
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

    note = m['lit_note']
    for slug, atlas, page, title, subs, start, end in POETRY_3A:
        pieces, spages = prescribed_poem(m, slug, subs, start, end)
        topic = POEM_TOPICS[slug]
        src = source('Filíocht Ainmnithe', title, [page])
        head = HEAD3A + f'\n({atlas[-1]}) {title}\n'
        for (label, prompt, marks, _), piece in zip(subs, pieces):
            add(f'{atlas}-{label}', f'{slug}-{label}', f'Filíocht 3A({atlas[-1]}) · {title} · ({label})', head + f'({label}) {prompt} ({marks} marc)',
                topic, [page], spages,
                [criterion('eolas', 'Eolas', marks, [piece, note], 'indicative', permitted=[0, 2, 4, 6, 8] if (slug, label) == ('poetry-3a-a', 'i') else None)],
                [CHOOSE_3A] + LIT[1:], f'One printed sub-question at its published {marks}-mark tariff. Scheme: “{m["lang_lit"]}” applies to the whole '
                '25-mark answer, never inside one sub-question.', src)
            if (slug, label) == ('poetry-3a-a', 'i'):
                for sub, question, marks_sub, nxt, permitted in SLOTS_3A_A:
                    start_at = piece.index(f'({sub}) {question}' if sub != 'a' else question)
                    slot = piece[start_at:piece.index(nxt, start_at) if nxt else len(piece)].strip()
                    assert 'Freagraí:' in slot and (f'({marks_sub} mharc)' in slot or '(2 mharc + 2 mharc)' in slot), (sub, slot[:60])
                    add(f'{atlas}-i-{sub}', f'{slug}-i-{sub}', f'Filíocht 3A(a) · {title} · (i)({sub})', head + f'(i) ({sub}) {question}',
                        topic, [page], spages, [criterion('eolas', 'Freagra', marks_sub, [slot], 'exact', permitted=permitted)], [CHOOSE_3A] + LIT[1:],
                        f'One printed {marks_sub}-mark question inside 3A(a)(i). Scheme: “{m["lang_lit"]}” applies to the whole 25-mark answer.', src)

    assert len(cards) == 32 and len({c['id'] for c in cards}) == 32 and len({c['atlasQuestionId'] for c in cards}) == 32
    for card in cards:
        for c in card['criteria']:
            assert c['guidance'] and all(not re.search('[\uf000-\uf0ff]|Siombailí Anótála', g) for g in c['guidance']), (card['id'], c['id'])
    sr = json.loads(SOURCE_REVIEW.read_text())
    legacy = ([f'irish-2025-ol-p2-reading-{l}-q{q}' for l in 'ab' for q in range(1, 6)]
              + [f'irish-2025-ol-p2-prose-{k}' for k in ['2a-a', '2a-b', '2a-c', '2b-a', '2b-b', '2b-c']]
              + [f'irish-2025-ol-p2-poetry-{k}' for k in ['3a-a', '3a-b', '3a-c', '3b-a', '3b-b', '3b-c']])
    review = dict(year=2025, level='ordinary', paperFileid=FILE + '.pdf', schemeFileid=SCHEME_FILE + '.pdf',
                  paperSha256=PAPER_SHA, schemeSha256=SCHEME_SHA,
                  reviewedPaperPages=list(range(1, 17)), reviewedSchemePages=sr['reviewedSchemePages'], schemeScope=sr['schemeScope'],
                  reviewDate=REVIEWED_AT, status='reviewed', fullPaperAndApplicableSchemeVisualSweep=True, selectionDecisions=m['decisions'],
                  practiceCardIds=[c['id'] for c in cards], legacyCardIds=legacy, readingWholeCardIds=legacy[:10],
                  examStructure=dict(readingA=50, readingB=50, prose=50, poetry=50, total=200),
                  nonPoolDecisions=sr['nonPoolDecisions'], openIssues=[], caveats=sr['sourceFindings'],
                  choicePolicy='Choice is not a route: each printed option of 2A, 2B, 3A and 3B is one card carrying the choose-two instruction; no combination cards.',
                  boundaries='10 retained whole reading questions with their 20 published parts; 12 retained literature options (3 prescribed prose, '
                             '3 optional prose, 3 prescribed poems, 3 optional poems) with the 9 prescribed-poetry sub-questions and the 3 printed 3A(a)(i) questions.')
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
    print(f"Irish Ordinary 2025 Paper 2: {len(data['cards'])} added practice cards (+22 retained legacy cards); the archive remains incomplete.")


if __name__ == '__main__':
    main()
