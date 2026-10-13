#!/usr/bin/env python3
"""Reviewed 2023 Higher Paper 2 (Léamhthuiscint agus Litríocht).

Paper PDF 1–16 and the Paper 2 pages of the combined LC001ALP000IV scheme
(PDF 18–49, plus 50 modified marking) visually reviewed on 2026-10-12. Counts are
assertions, not corpus-completeness proof. Same method as irish_higher_2025_p2.py.

The legacy generator already ships 26 cards for this component: the twelve
whole reading questions and the fourteen literature routes. Their IDs are kept.
`apply_legacy_review` (called by irish_cards.py) joins them to Atlas and replaces
their marking with the lifted 2023 scheme (each reading part and each poetry
sub-question keeps its own published tariff). `build` adds every published
reading part as a practice card, plus the independent 1 + 1 answer slots and the
6 + 6 trait slots, beside the legacy file.

2023 differs from 2025 in two 6(b) shapes: Léamhthuiscint A asks for two traits
(6 + 6: trait 2 + support 4 each, so two practice slots), and Léamhthuiscint B
asks for an opinion (2) and two supported points (5 + 5), which stay inside one
response as in 2026 B 6(b). The scheme's text layer stores each poetry band table
after the following sub-question; `place_tables` returns each table to the
sub-question it is printed beside.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
FILE = 'LC001ALP200IV'
SCHEME_FILE = 'LC001ALP000IV'
OUT = ROOT / 'components/MarkBank/cards/irish/higher-2023-p2-authored.json'
SOURCE_REVIEW = ROOT / 'scripts/markbank/authored/irish-higher-2023-p2-source-review.json'
REVIEWED_AT = '2026-10-12'
PAPER_SHA = '24ef3ff77f567f5e72773a1df97d3dbb64bdbf8307673eeb14022d6363012e23'
SCHEME_SHA = '4088eb120e0d61d9e4ad1ab54f80829b55d89dc5ef57bdcb58129ee58dce5089'
# The 2025 pattern plus every "dhá"/"an dá" count and every "amháin".
DIRECTIVE = re.compile(r'rogha|roghna|Freagair|Luaigh|Ainmnigh|\bnó\b|dhá phointe|dhá rud|dhá bh|dhá dh|dhá ch|dhá fh|dhá th|'
                       r'ceann amháin|pointe amháin|\bdhá\b|an dá\b|amháin', re.I)
SOURCE_NOTE = 'Shown page-for-page from the official examination paper; swipe to move between pages.'


def clean(text):
    return re.sub(r'\s+', ' ', text).strip()


def comparable(text):
    return re.sub(r'[^\w]+', '', text.lower())


def in_order(prompt, text):
    return re.search('.*?'.join(re.escape(comparable(w)) for w in prompt.split() if comparable(w)), comparable(text))


def criterion(id, label, marks, guidance, kind='exact', permitted=None):
    return dict(id=id, label=label, kind='award', maxMarks=marks,
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
            self.text += f' ⟦{p}⟧ ' + re.sub(r'^\d+\s', '', clean(doc[p - 1].get_text()))

    def chunk(self, start, end=None, after=0):
        i = self.text.index(start, after)
        j = self.text.index(end, i + len(start)) if end else len(self.text)
        raw = self.text[i:j]
        pages = {int(re.findall(r'⟦(\d+)⟧', self.text[:i])[-1])}
        pages |= {int(m.group(1)) for m in re.finditer(r'⟦(\d+)⟧([^⟦]*)', raw) if clean(m.group(2)) not in ('', 'nó')}
        return clean(re.sub(r'⟦\d+⟧', ' ', raw)), sorted(pages)


GAEILGE_TABLE = re.compile(r'Gaeilge \(5 mharc\) Sárchumas.*?Cumas lag/an-lag maidir leis na príomhghnéithe de cheart na teanga \(gramadach, comhréir, struchtúr, deilbhíocht\) 1')
# Poetry band tables: the text layer stores them after the next sub-question; each belongs beside the part it prices.
PLE_TABLE = re.compile(r'Catagóir Plé \(1[13] mharc\) Marcanna .*?Lag/An-lag Eolas an-bhearnach, an-mhíchruinn agus an-lochtach 0-[35]')
MARC5_TABLE = re.compile(r'Catagóir Marc as 5 Sármhaith 5 An-mhaith 4 Maith 3 Measartha 2 Lag/An-lag 0-1(?! 0)')
MARC7_TABLE = re.compile(r'Catagóir Marc as 7 Sár-mhaith 6-7 An-mhaith 5 Maith 4 Measartha 3 Lag/An-lag 0-2')


def place_tables(pieces):
    """Return each printed band table to the sub-question it sits beside: Plé to (i), Marc as 5/7 to (ii)."""
    pieces = list(pieces)
    for pattern, home in [(PLE_TABLE, 0), (MARC5_TABLE, 1), (MARC7_TABLE, 1)]:
        for k in range(len(pieces)):
            if k == home:
                continue
            found = pattern.search(pieces[k])
            if found:
                pieces[k] = clean(pieces[k][:found.start()] + ' ' + pieces[k][found.end():])
                pieces[home] = clean(pieces[home] + ' ' + found.group(0))
    return pieces


def printed_values(chunk, marks):
    values = re.findall(r'= (\d+) mh?arc', chunk) + re.findall(r'bronntar (\d+) mh?arc', chunk)
    return sorted({0, marks} | {int(v) for v in values if int(v) <= marks})


_MATERIAL = None


def material():
    global _MATERIAL
    if _MATERIAL:
        return _MATERIAL
    import fitz
    paper_path = ROOT / f'paper-trail-corpus/exampapers/2023/{FILE}.pdf'
    scheme_path = ROOT / f'paper-trail-corpus/markingschemes/2023/{SCHEME_FILE}.pdf'
    assert hashlib.sha256(paper_path.read_bytes()).hexdigest() == PAPER_SHA, 'Paper changed: repeat visual review'
    assert hashlib.sha256(scheme_path.read_bytes()).hexdigest() == SCHEME_SHA, 'Scheme changed: repeat visual review'
    paper, doc = fitz.open(paper_path), fitz.open(scheme_path)
    texts = [clean(p.get_text()) for p in paper]
    s = Scheme(doc, 18, 49)
    general = s.chunk('Freagair Léamhthuiscint A agus Léamhthuiscint B. Tá Ceist 1', 'Siombailí Anótála')[0]
    # (q, part, paper prompt, scheme anchor, marks, mode)
    passages = {
        'A': dict(title='Tom Crean – Taiscéalaí Ciarraíoch an Antartaigh', pages=[4, 5], topic='irish-3-0', end='LÉAMHTHUISCINT B (50 marc)', parts=[
            ('1', 'a', '(a) Cén fáth a bhfuil clú agus cáil ar Tom Crean? (Alt 1)', '1. (a) Cén fáth a bhfuil clú', 3, None),
            ('1', 'bi', '(b) (i) Scríobh síos cineál amháin taighde a bheidh ar siúl ag na heolaithe mara ar an RV Tom Crean. (Alt 1)', '(b) (i) Scríobh síos cineál amháin', 2, None),
            ('1', 'bii', '(ii) Cén fáth ar thug an RV Tom Crean cuairt ghearr ar an Min Aird an lá tar éis a choimisiúnaithe? (Alt 1)', '(ii) Cén fáth ar thug an RV', 2, None),
            ('2', 'a', '(a) Scríobh síos dhá phointe eolais faoi mhuintir Tom Crean agus é ag fás aníos gar d’Abhainn an Scáil in iarthar Chiarraí. (Alt 2)', '2. (a) Scríobh síos dhá phointe eolais faoi mhuintir', 3, 'ordered'),
            ('2', 'bi', '(b) (i) Cén fáth ar mheall gairm an Chabhlaigh Ríoga go leor fear óg mar Tom Crean ag an am sin? (Alt 2)', '(b) (i) Cén fáth ar mheall', 2, None),
            ('2', 'bii', '(ii) Cén aidhm a bhí ag Robert Falcon Scott agus é ar a bhealach go dtí an tAntartach ar an long thaiscéalaíochta, Discovery? (Alt 2)', '(ii) Cén aidhm a bhí ag Robert', 2, None),
            ('3', 'a', '(a) Cad a spreag Tom Crean le dul ar an turas taiscéalaíochta ar an Discovery? (Alt 3)', '3. (a) Cad a spreag Tom Crean', 3, None),
            ('3', 'bi', '(b) (i) Scríobh síos dhá phointe eolais faoin gcruatan a d’fhulaing Crean agus na fir eile ar an turas leis na carranna sleamhnáin. (Alt 3)', '(b) (i) Scríobh síos dhá phointe eolais faoin gcruatan', 2, 'slots'),
            ('3', 'bii', '(ii) Cén tubaiste a bhain do Tom Crean lá amháin agus é ag cabhrú leis an long a scaoileadh? (Alt 3)', '(ii) Cén tubaiste', 2, None),
            ('4', 'a', '(a) Cén obair a rinne Tom Crean agus na fir eile nuair a thaistil siad amach ón mbunchampa leis na capaillíní a bhí leo? (Alt 4)', '4. (a) Cén obair a rinne Tom Crean', 3, None),
            ('4', 'bi', '(b) (i) Luaigh dhá phointe eolais faoin siúl ab éigean do Crean a dhéanamh chun cabhair a lorg dá chomrádaithe. (Alt 4)', '(b) (i) Luaigh dhá phointe eolais faoin siúl', 2, 'slots'),
            ('4', 'bii', '(ii) Cén fáth ar bronnadh bonn Rí Albert ar Tom Crean i 1913? (Alt 4)', '(ii) Cén fáth ar bronnadh', 2, None),
            ('5', 'a', '(a) Cad a theastaigh ó Ernest Shackleton a dhéanamh ar an turas taiscéalaíochta go dtí an tAntartach ar an long Endurance i 1914? (Alt 5)', '5. (a) Cad a theastaigh', 3, None),
            ('5', 'bi', '(b) (i) Tabhair pointe amháin eolais faoin turas farraige a rinne Shackleton agus a chriú ó Oileán Eilifinte go Seoirsia Theas agus iad ag lorg cabhrach. (Alt 5)', '(b) (i) Tabhair pointe amháin eolais', 2, None),
            ('5', 'bii', '(ii) Cén fáth a ndeirtear sa sliocht go mairfidh cáil Tom Crean mar laoch Antartach go deo? (Alt 5)', '(ii) Cén fáth a ndeirtear', 2, None),
            ('6', 'a', '(a) Aimsigh sampla de bhriathar san Aimsir Fháistineach in Alt 1 agus sampla d’ainmfhocal firinscneach sa tuiseal ginideach uatha in Alt 3.', '6. (a) Aimsigh sampla de bhriathar', 3, 'grammar'),
            ('6', 'b', '(b) Bunaithe ar an eolas sa sliocht thuas, déan plé ar dhá thréith de chuid Tom Crean, dar leat. Bíodh sampla amháin ón sliocht agat, i d’fhocail féin, ag tacú le gach tréith a luann tú i do fhreagra. (Is leor 60 focal.)', '(b) Bunaithe ar an eolas sa sliocht thuas, déan plé', 12, 'traits')]),
        'B': dict(title='2022: Bliain Eorpach na hÓige', pages=[6, 7], topic='irish-3-1', end='⟦27⟧', parts=[
            ('1', 'a', '(a) Cén fáth a bhfuil fís agus rannpháirtíocht na nEorpach óg ríthábhachtach, de réir an phreasráitis a chuir an Coimisiún Eorpach amach? (Alt 1)', '1. (a) Cén fáth a bhfuil fís', 3, None),
            ('1', 'bi', '(b) (i) Scríobh síos príomhchuspóir amháin a leagadh amach do Bhliain Eorpach na hÓige. (Alt 1)', '(b) (i) Scríobh síos príomhchuspóir', 2, None),
            ('1', 'bii', '(ii) Cén fáth ar chóir daoine óga a mholadh, dar le Mariya Gabriel? (Alt 1)', '(ii) Cén fáth ar chóir', 2, None),
            ('2', 'a', '(a) Luaigh dhá aidhm de chuid na n-imeachtaí a d’eagraigh an eagraíocht Léargas in Éirinn le linn Bhliain Eorpach na hÓige. (Alt 2)', '2. (a) Luaigh dhá aidhm', 3, 'ordered'),
            ('2', 'bi', '(b) (i) Céard a mhínigh Maria Walsh do na daoine óga a bhí i láthair ag an gcomhdháil i mí Feabhra? (Alt 2)', '(b) (i) Céard a mhínigh', 2, None),
            ('2', 'bii', '(ii) Cad iad na hábhair a bhí á bplé ag na daoine óga sna ceardlanna sna carráistí ar an traein speisialta ‘All Aboard’? (Alt 2)', '(ii) Cad iad na hábhair', 2, 'slots'),
            ('3', 'a', '(a) Scríobh síos dhá shlí a mbaineann mic léinn na n-institiúidí tríú leibhéal tairbhe as clár Erasmus+. (Alt 3)', '3. (a) Scríobh síos dhá shlí', 3, 'ordered'),
            ('3', 'bi', '(b) (i) Tabhair dhá phointe eolais faoin obair dheonach a dhéanann na daoine óga ar fud na hEorpa mar chuid den Chór Dlúthpháirtíochta Eorpach. (Alt 3)', '(b) (i) Tabhair dhá phointe eolais faoin obair', 2, 'slots'),
            ('3', 'bii', '(ii) Luaigh an dá rud a fhoghlaimíonn scoláirí dara leibhéal sa togra ‘Clár Scoileanna Ambasadóra Pharlaimint na hEorpa’. (Alt 3)', '(ii) Luaigh an dá rud', 2, 'slots'),
            ('4', 'a', '(a) Scríobh síos dhá rud a dúirt Harry McCann faoin gcaoi ar chuir paindéim Covid-19 isteach ar shaol na hóige. (Alt 4)', '4. (a) Scríobh síos dhá rud a dúirt', 3, 'ordered'),
            ('4', 'bi', '(b) (i) Cén fáth a mbíonn an t-aos óg ag gníomhú go paiseanta san fheachtas Fridays for Future? (Alt 4)', '(b) (i) Cén fáth a mbíonn', 2, None),
            ('4', 'bii', '(ii) Cén fáth ar chomhairligh Harry McCann don ghlúin óg seasamh le chéile agus a dtuairimí a nochtadh? (Alt 4)', '(ii) Cén fáth ar chomhairligh', 2, None),
            ('5', 'a', '(a) Cad iad na rudaí atá tábhachtach má táimid le hEoraip ionchuimsitheach dhigiteach a bhaint amach? (Alt 5)', '5. (a) Cad iad na rudaí', 3, 'ordered'),
            ('5', 'bi', '(b) (i) Scríobh síos pointe amháin eolais faoi óige dhaonra an Aontais Eorpaigh. (Alt 5)', '(b) (i) Scríobh síos pointe amháin eolais faoi óige', 2, None),
            ('5', 'bii', '(ii) Cad leis a bhfuiltear ag súil agus Bliain Eorpach na hÓige thart? (Alt 5)', '(ii) Cad leis a bhfuiltear', 2, None),
            ('6', 'a', '(a) Aimsigh sampla d’ainmfhocal baininscneach sa tuiseal ginideach uatha in Alt 2 agus sampla den bhriathar saor san Aimsir Chaite in Alt 4.', '6. (a) Aimsigh sampla d’ainmfhocal baininscneach', 3, 'grammar'),
            ('6', 'b', '(b) Bunaithe ar an eolas sa sliocht thuas, arbh fhiú Bliain Eorpach na hÓige 2022 a bheith ann, dar leat? Tabhair dhá phointe eolais, i d’fhocail féin, as an sliocht, mar thacaíocht le do fhreagra. (Is leor 60 focal.)', '(b) Bunaithe ar an eolas sa sliocht thuas, arbh fhiú', 12, 'opinion')]),
    }
    tariffs = {'traits': '{6 mharc + 6 mharc}', 'opinion': 'Tuairim a nochtadh = 2 mharc', 'slots': '{2 mharc: 1 mharc + 1 mharc}',
               'ordered': '{3 mharc: 2 mharc + 1 mharc}', 'grammar': '{3 mharc: 2 mharc + 1 mharc}'}
    start_b = s.text.index('LÉAMHTHUISCINT B (50 marc)')
    for letter, passage in passages.items():
        page_text = ' '.join(texts[p - 1] for p in passage['pages'])
        anchors = [p[3] for p in passage['parts']]
        resolved = []
        pos = start_b if letter == 'B' else 0
        for index, (q, part, prompt, anchor, marks, mode) in enumerate(passage['parts']):
            assert in_order(prompt, page_text), (letter, q, part)
            # Anchors are searched forward from the previous part so repeated stems resolve in printed order.
            here = s.text.index(anchor, pos)
            assert letter == 'B' or here < start_b, (letter, q, part)
            chunk, spages = s.chunk(anchor, anchors[index + 1] if index + 1 < len(anchors) else passage['end'], pos)
            pos = here + 1
            assert tariffs.get(mode, f'{{{marks} mharc}}') in chunk, (letter, q, part, chunk[:90])
            assert 'Siombailí' not in chunk and 'LÉAMHTHUISCINT B' not in chunk, (letter, q, part)
            resolved.append((q, part, prompt, anchor, marks, mode, chunk, spages))
        passage['resolved'] = resolved
    note5 = s.chunk('Nóta: I gcás na gceisteanna 2 (Prós)', 'Nóta: Níl na nótaí tacaíochta seo uileghabhálach ná críochnúil agus bronnfar marcanna ar phointí bailí')[0]
    notes = s.chunk('Nóta: Níl na nótaí tacaíochta seo uileghabhálach ná críochnúil agus bronnfar marcanna ar phointí bailí', 'Gaeilge (5 mharc)')[0]
    poetry_notes = s.chunk('Nóta: Níl na nótaí tacaíochta seo uileghabhálach ná críochnúil agus bronnfar marcanna ar phointí ábhartha', 'Freagair Ceist 3A (Filíocht Ainmnithe)')[0]
    gaeilge_table = GAEILGE_TABLE.search(s.text, s.text.index('⟦28⟧')).group(0)
    prose_table = s.chunk('Catagóir Eolas (25 marc) (18 marc)', 'Ceist 2 PRÓS (30 marc)')[0]
    general4 = s.chunk('Treoracha: Iarrtar ar na hiarrthóirí plé a dhéanamh ar an ráiteas', 'Gaeilge (5 mharc)', s.text.index('⟦40⟧'))[0]
    assert all(x in gaeilge_table for x in ['Sárchumas', 'Cumas lag/an-lag']) and '22-25' in prose_table and '0-6' in prose_table and '30-35' in general4
    _MATERIAL = dict(paper=paper, texts=texts, s=s, general=general, passages=passages, note5=note5, notes=notes, poetry_notes=poetry_notes,
                     gaeilge_table=gaeilge_table, prose_table=prose_table, general4=general4,
                     decisions=selection_decisions(paper))
    return _MATERIAL


READING_REQUIREMENTS = ['Léigh an sliocht iomlán a ghabhann leis an gceist. Freagair an chuid atá luaite ar an gcárta.',
                        'Úsáid an t-alt a luaitear. Glacfar le focail an tsleachta nó le do chuid focal féin, ach ní mór 6(b) a fhreagairt i d’fhocail féin.']
PART_NOTE = ('SEC allocation for this task. Alternative correct answers in the scheme are answers to one task, not extra task routes. '
             'Retained whole questions and their practice parts are overlapping exercises; their marks are not added to infer the paper total.')
LABELS = {'a': '(a) Freagra', 'bi': '(b)(i) Freagra', 'bii': '(b)(ii) Freagra', 'grammar': '(a) Freagra',
          'trait-1': '(b) Tréith 1', 'trait-2': '(b) Tréith 2', 'opinion': '(b) Tuairim', 'point-1': '(b) Pointe eolais 1', 'point-2': '(b) Pointe eolais 2'}


def part_criteria(q, part, marks, mode, chunk, general):
    if mode == 'traits':
        return [criterion('trait-1', 'Tréith 1', 6, [chunk, general]), criterion('trait-2', 'Tréith 2', 6, [chunk, general])]
    if mode == 'opinion':
        return [criterion('opinion', 'Tuairim', 2, [chunk, general]), criterion('point-1', 'Pointe eolais 1', 5, [chunk]),
                criterion('point-2', 'Pointe eolais 2', 5, [chunk])]
    if mode in ('ordered', 'grammar'):
        return [criterion('grammar' if mode == 'grammar' else part, 'Freagra', marks,
                          [chunk, general, 'Order-dependent award: the first correct item earns 2 and the other 1 (0, 2 or 3).'], permitted=[0, 2, 3])]
    return [criterion(part, 'Freagra', marks, [chunk, general], permitted=printed_values(chunk, marks))]


def gaeilge(m):
    return criterion('gaeilge', 'Gaeilge', 5, [m['gaeilge_table'], m['note5']], 'quality')


def split_parts(whole, cuts, caps):
    i2 = whole.index(cuts[0]); i3 = whole.index(cuts[1], i2)
    pieces = place_tables([whole[:i2].strip(), whole[i2:i3].strip(), whole[i3:].strip()])
    for piece, cap in zip(pieces, caps):
        assert cap in piece, cap
    return pieces


def apply_legacy_review(cards):
    """Lift the 2023 scheme onto the 26 retained legacy cards (IDs, totals and topics unchanged)."""
    m = material()
    by_id = {c['id']: c for c in cards}
    stamped = []

    def stamp(card_id, atlas, pages, scheme_pages, criteria, note, requirements=None):
        card = by_id[card_id]
        card.update(atlasQuestionId=atlas, reviewedAt=REVIEWED_AT, reviewedPaperPages=pages, paperPage=pages[0],
                    schemePage=scheme_pages[0], schemePages=scheme_pages, criteria=criteria, markingGuideNote=note)
        if requirements:
            card['taskRequirements'] = requirements
        assert sum(c['maxMarks'] for c in criteria) == card['totalMarks'], card_id
        stamped.append(card_id)
        return card

    six_b = {'A': '6(b) traits T1 and T2 are 6 marks each (naming the trait 2 + its support from the passage 4), in the candidate’s own words.',
             'B': '6(b) is one response: opinion 2 and two supported points 5 + 5, in the candidate’s own words.'}
    for letter, passage in m['passages'].items():
        by_q = {}
        for q, part, prompt, anchor, marks, mode, chunk, spages in passage['resolved']:
            by_q.setdefault(q, []).append((part, marks, mode, chunk, spages))
        for q, parts in by_q.items():
            crits = [c for part, marks, mode, chunk, _ in parts for c in part_criteria(q, part, marks, mode, chunk, m['general'])]
            for c in crits:
                c['label'] = LABELS[c['id']]
            n = str(int(q) + (6 if letter == 'B' else 0))
            stamp(f'irish-2023-hl-p2-reading-{letter.lower()}-q{q}', n, passage['pages'], sorted({p for *_, sp in parts for p in sp}), crits,
                  'Retained complete printed question. Score each published part separately using these SEC allocations.'
                  + (' Two-answer grammar is one 0/2/3 placement; ' + six_b[letter] if q == '6' else ''),
                  ['Léigh an sliocht oifigiúil a ghabhann leis an gceist.', 'Freagair gach fochuid agus cloígh leis an alt a luaitear.',
                   'Bain úsáid as do chuid focal féin nuair a iarrtar ort é.'])

    s, notes, prose_table = m['s'], m['notes'], m['prose_table']
    lit_requirements = ['Freagair gach cuid den cheist atá priontáilte.', 'Úsáid tagairtí cruinne agus ábhartha don téacs.']
    prose = [('prose-2a-a', 'P-2A-a', '(a) Oisín i dTír na nÓg', 'nó (b) Dís'),
             ('prose-2a-b', 'P-2A-b', 'nó (b) Dís', '2B. Prós Roghnach'),
             ('prose-2b-a', 'P-2B-a', '(a) Maidir le scéal béaloidis roghnach', 'nó (b) Maidir le gearrscéal roghnach'),
             ('prose-2b-b', 'P-2B-b', 'nó (b) Maidir le gearrscéal roghnach', 'Nóta: Níl na nótaí tacaíochta seo uileghabhálach ná críochnúil agus bronnfar marcanna ar phointí ábhartha')]
    for slug, atlas, start, end in prose:
        chunk, spages = s.chunk(start, end)
        assert 'Eolas = 25 marc' in chunk and 'Gaeilge (5 mharc)' not in chunk, slug
        stamp(f'irish-2023-hl-p2-{slug}', atlas, [8], sorted(set(spages) | {28}),
              [criterion('eolas', 'Eolas', 25, [re.sub(r'^nó ', '', chunk), prose_table, notes], 'indicative'), gaeilge(m)],
              'One complete SEC response: 25 Eolas and a single shared 5-mark Gaeilge award. Supporting notes are indicative rather than exhaustive. '
              'The printed Eolas table has a 25-mark and an 18-mark column; the Treoir says when a one-aspect answer is assessed out of 18.', lit_requirements)

    poems = [('poetry-3a-a', 'F-3A-a', [9], '(a) Mo ghrá-sa (idir lúibíní) (i)', '(b) An Spailpín Fánach (i)', ['(ii) Cén ghné is mó den dán', '(iii) Cé a chum an dán seo?']),
             ('poetry-3a-b', 'F-3A-b', [10], '(b) An Spailpín Fánach (i)', '3B. Filíocht Roghnach', ['(ii) Cén chaoi a dtéann an dán seo', '(iii) Cén mheadaracht']),
             ('poetry-3b-a', 'F-3B-a', [11], '(a) (i) Maidir le dán nua-aimseartha roghnach', '(b) (i) Maidir le dán seanaimseartha roghnach', ['(ii) Cén ghné is mó den dán', '(iii) Cé a chum an dán seo?']),
             ('poetry-3b-b', 'F-3B-b', [11], '(b) (i) Maidir le dán seanaimseartha roghnach', 'Freagair do rogha ceann amháin as Ceist 4', ['(ii) Cén chaoi a dtéann an dán seo', '(iii) Scríobh síos an teicníc fhileata'])]
    for slug, atlas, pages, start, end, cuts in poems:
        whole, spages = s.chunk(start, end)
        # The printed Gaeilge table can sit between sub-questions; it belongs to the shared award, not to Eolas.
        whole = re.sub(r'^nó ', '', GAEILGE_TABLE.sub(' ', whole)).strip()
        assert 'Gaeilge (5 mharc)' not in whole, slug
        pieces = split_parts(whole, cuts, ['Eolas = 13 mharc', 'Eolas = 5 mharc', 'Eolas = 7 marc'])
        assert not MARC5_TABLE.search(pieces[2]) and not PLE_TABLE.search(pieces[2]) and not PLE_TABLE.search(pieces[1]), slug
        stamp(f'irish-2023-hl-p2-{slug}', atlas, pages, sorted(set(spages) | {32}),
              [criterion('eolas-i', '(i) Eolas', 13, [pieces[0], m['poetry_notes']], 'indicative'), criterion('eolas-ii', '(ii) Eolas', 5, [pieces[1]], 'indicative'),
               criterion('eolas-iii', '(iii) Eolas', 7, [pieces[2]], 'indicative'), gaeilge(m)],
              'One complete SEC response with one shared five-mark Gaeilge award. The paper prints (i) 15, (ii) 6 and (iii) 9; the scheme assesses '
              'Eolas 13, 5 and 7 with the conditions shown, plus Gaeilge 5 once. Supporting notes are indicative rather than exhaustive.', lit_requirements)

    options = [('literature-4-a', 'X-4A', '4A. An Triail', '4B. A Thig Ná Tit Orm'),
               ('literature-4-b', 'X-4B', '4B. A Thig Ná Tit Orm', '4C. Tóraíocht Dhiarmada'),
               ('literature-4-c', 'X-4C', '4C. Tóraíocht Dhiarmada', '4D. Gafa'),
               ('literature-4-d', 'X-4D', '4D. Gafa', '4E. Canary Wharf'),
               ('literature-4-e', 'X-4E', '4E. Canary Wharf', '4F. Dánta Breise')]
    for slug, atlas, start, end in options:
        chunk, spages = s.chunk(start, end, s.text.index('⟦41⟧'))
        assert 'Eolas = 35 marc' in chunk and 'Gaeilge (5 mharc)' not in chunk, slug
        stamp(f'irish-2023-hl-p2-{slug}', atlas, [12], sorted(set(spages) | {40}),
              [criterion('eolas', 'Eolas', 35, [chunk, m['general4']], 'indicative'), gaeilge(m)],
              'One complete SEC response: Eolas 35 assessed as a unit with a single shared 5-mark Gaeilge award. Supporting notes are indicative rather than exhaustive.',
              lit_requirements)
    whole, spages = s.chunk('4F. Dánta Breise', None, s.text.index('⟦47⟧'))
    whole = GAEILGE_TABLE.sub(' ', whole).strip()
    pieces = split_parts(whole, ['(ii) A bhfuil i gceist leis na línte seo a mhíniú', '(iii) Is í an mháthair atá ag caint'],
                         ['Eolas = 19 marc', 'Eolas = 7 marc', 'Eolas = 9 marc'])
    assert MARC7_TABLE.search(pieces[1]) and 'Marc as 5 Marc as 4' in pieces[2], '4F tables'
    stamp('irish-2023-hl-p2-literature-4-f', 'X-4F', [12, 13], spages,
          [criterion('eolas-i', '(i) Eolas', 19, [pieces[0], m['general4']], 'indicative'), criterion('eolas-ii', '(ii) Eolas', 7, [pieces[1]], 'indicative'),
           criterion('eolas-iii', '(iii) Eolas', 9, [pieces[2]], 'indicative'), gaeilge(m)],
          'One complete SEC response: the paper prints (i) 20, (ii) 10 and (iii) 10; the scheme assesses Eolas 19, 7 and 9 (5 + 4 for the two points) '
          'plus one shared 5-mark Gaeilge award. Supporting notes are indicative rather than exhaustive.', lit_requirements)
    assert len(stamped) == 26
    for card_id in stamped:
        for c in by_id[card_id]['criteria']:
            assert c['guidance'] and all(not re.search('[-]', g) for g in c['guidance']), (card_id, c['id'])
    return cards, stamped


def build():
    m = material()
    cards = []

    def add(key, slug, ref, prompt, topic, pages, scheme_pages, criteria, note, extra_topics=None, title=None):
        cards.append(dict(
            id=f'irish-2023-hl-p2-{slug}', year=2023, level='higher', paper=2, section='2',
            atlasQuestionId=key, questionRef=f'2023 HL Paper 2 {ref}', questionText=prompt,
            totalMarks=sum(c['maxMarks'] for c in criteria), topicId=topic,
            **({'additionalTopicIds': extra_topics} if extra_topics else {}),
            conceptId=f'irish-hl-p2-{slug}', paperFileid=FILE, schemeFileid=SCHEME_FILE,
            schemePage=scheme_pages[0], schemePages=scheme_pages, reviewedAt=REVIEWED_AT, reviewedPaperPages=pages,
            taskRequirements=READING_REQUIREMENTS, criteria=criteria, markingGuideNote=note,
            sourceMaterial=dict(kind='source-text', label=ref.split(' · ')[0], title=title, pages=pages,
                                attribution='© State Examinations Commission.', presentationNote=SOURCE_NOTE)))

    for letter, passage in m['passages'].items():
        topic = passage['topic']
        for q, part, prompt, anchor, marks, mode, chunk, spages in passage['resolved']:
            label = f'{q}({part[0]})' + (f'({part[1:]})' if len(part) > 1 else '')
            text = f'{label} ' + re.sub(r'^(\([a-z]+\)\s*)+', '', prompt)
            here = 'irish-3-3' if mode == 'grammar' else topic
            add(f'R-{letter}-{q}-{part}', f'reading-{letter.lower()}-q{q}-{part}', f'Léamhthuiscint {letter} · Ceist {label}', text, here,
                passage['pages'], spages, part_criteria(q, part, marks, mode, chunk, m['general']), PART_NOTE,
                [topic] if mode == 'grammar' else None, passage['title'])
            if mode == 'slots':
                for slot in (1, 2):
                    add(f'R-{letter}-{q}-{part}-{slot}', f'reading-{letter.lower()}-q{q}-{part}-{slot}', f'Léamhthuiscint {letter} · Ceist {label} · Freagra {slot}',
                        f'{text} Don chárta seo: tabhair freagra amháin don chuid seo (freagra {slot}, 1 mharc).', topic, passage['pages'], spages,
                        [criterion(f'{part}-{slot}', f'Freagra {slot}', 1, [f'Aon fhreagra ceart don chuid seo = 1 mharc. Ní féidir an freagra céanna a áireamh faoi dhó. {chunk}', m['general']])],
                        'The scheme prices the two answers 1 mharc + 1 mharc independently; this card practises one of them. ' + PART_NOTE, None, passage['title'])
            if mode == 'traits':
                for slot in (1, 2):
                    add(f'R-{letter}-{q}-{part}-{slot}', f'reading-{letter.lower()}-q{q}-{part}-{slot}', f'Léamhthuiscint {letter} · Ceist {label} · Tréith {slot}',
                        f'{text} Don chárta seo: déan plé ar thréith amháin agus tabhair sampla amháin ón sliocht, i d’fhocail féin (tréith {slot}, 6 mharc).',
                        topic, passage['pages'], spages, [criterion(f'trait-{slot}', f'Tréith {slot}', 6, [chunk, m['general']])],
                        'The scheme prices the two traits 6 + 6 independently (trait 2 + support 4); this card practises one of them. ' + PART_NOTE, None, passage['title'])
    assert len(cards) == 46 and len({c['id'] for c in cards}) == 46
    for card in cards:
        for c in card['criteria']:
            assert c['guidance'] and all(not re.search('[-]', g) for g in c['guidance']), (card['id'], c['id'])
    sr = json.loads(SOURCE_REVIEW.read_text())
    legacy = ([f'irish-2023-hl-p2-reading-{l}-q{q}' for l in 'ab' for q in range(1, 7)]
              + [f'irish-2023-hl-p2-prose-{k}' for k in ['2a-a', '2a-b', '2b-a', '2b-b']]
              + [f'irish-2023-hl-p2-poetry-{k}' for k in ['3a-a', '3a-b', '3b-a', '3b-b']]
              + [f'irish-2023-hl-p2-literature-4-{k}' for k in 'abcdef'])
    review = dict(year=2023, level='higher', paperFileid=FILE + '.pdf', schemeFileid=SCHEME_FILE + '.pdf',
                  paperSha256=PAPER_SHA, schemeSha256=SCHEME_SHA,
                  reviewedPaperPages=list(range(1, 17)), reviewedSchemePages=sr['reviewedSchemePages'], schemeScope=sr['schemeScope'],
                  reviewDate=REVIEWED_AT, status='reviewed', fullPaperAndApplicableSchemeVisualSweep=True, selectionDecisions=m['decisions'],
                  readingPracticeCardIds=[c['id'] for c in cards], legacyCardIds=legacy, readingWholeCardIds=legacy[:12],
                  examStructure=dict(readingA=50, readingB=50, prose=30, poetry=30, additionalLiterature=40, total=200),
                  nonPoolDecisions=sr['nonPoolDecisions'], openIssues=[], caveats=sr['sourceFindings'],
                  boundaries='12 retained whole reading questions with 34 published parts, 10 independent one-mark answer slots and 2 six-mark trait slots; '
                             '4 retained prose, 4 poetry and 6 additional-literature routes.')
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
    print(f"Irish Higher 2023 Paper 2: {len(data['cards'])} added reading cards (+26 retained legacy cards); the archive remains incomplete.")


if __name__ == '__main__':
    main()
