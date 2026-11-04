#!/usr/bin/env python3
"""Reviewed 2022 Higher Paper 2 (Léamhthuiscint agus Litríocht).

Paper PDF 1–16 and the Paper 2 pages of the combined LC001ALP000IV scheme
(PDF 18–50, plus 51 modified marking) reviewed on 2026-11-04. Counts are
assertions, not corpus-completeness proof. Same method as irish_higher_2023_p2.py.

The legacy generator already ships 27 cards for this component: the twelve
whole reading questions and fifteen literature routes. Their IDs are kept.
irish_higher_routes.apply_review (run first by irish_cards.py) already reviewed
the prose routes (2A(a) Cáca Milis and An Lasair Choille, 2A(b), 2B(a), 2B(b))
and 3B(a)/(b); their IDs, texts and route decisions stand. `apply_legacy_review`
joins the reading questions, 3A(a)/(b) and Ceist 4 to Atlas and replaces their
marking with the lifted 2022 scheme (each reading part and each poetry
sub-question keeps its own published tariff), and gives 3B(a)(ii) the scheme's
own pricing slice. `build` adds every published reading part as a practice card,
plus the independent 1 + 1 answer slots and the 6 + 6 trait slots, beside the
legacy file.

2022 shapes: Léamhthuiscint A 6(b) asks for two traits (6 + 6: trait 2 + support
4 each, so two practice slots, as 2023 A); Léamhthuiscint B 6(b) asks how the
extract affected the reader (C 2) with two supported points (5 + 5), which stay
inside one response as in 2023 B. The scheme prints its poetry and Ceist 4 band
tables Eolas and Gaeilge side by side; the text layer reads them row by row.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import re
from pathlib import Path
from irish_lifted import scheme_words_in, symbol_text

ROOT = Path(__file__).resolve().parents[3]
FILE = 'LC001ALP200IV'
SCHEME_FILE = 'LC001ALP000IV'
OUT = ROOT / 'components/MarkBank/cards/irish/higher-2022-p2-authored.json'
SOURCE_REVIEW = ROOT / 'scripts/markbank/authored/irish-higher-2022-p2-source-review.json'
REVIEWED_AT = '2026-11-04'
PAPER_SHA = 'e29b5862e8650455db716de7c58c1c81d7f09f169f482d53d5831027b5637d58'
SCHEME_SHA = '600bdfd6f0a8499687c09a98873aa32915415299e83885186dd1a7ca251ca92c'
# The 2023 pattern: every "dhá"/"an dá" count and every "amháin".
DIRECTIVE = re.compile(r'rogha|roghna|Freagair|Luaigh|Ainmnigh|\bnó\b|dhá phointe|dhá rud|dhá bh|dhá dh|dhá ch|dhá fh|dhá th|'
                       r'ceann amháin|pointe amháin|\bdhá\b|an dá\b|amháin', re.I)
SOURCE_NOTE = 'Shown page-for-page from the official examination paper; swipe to move between pages.'


def clean(text):
    return re.sub(r'\s+', ' ', symbol_text(text)).strip()


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
# Poetry band tables: the text layer stores them after the next sub-question (or after the Gaeilge table);
# each belongs beside the part it prices: the Plé table to (i), the Marc as 5 table to (ii).
PLE_TABLE = re.compile(r'Catagóir (?:An plé|Plé) \(1[13] mharc\) Marcanna .*?Lag/An-lag Eolas an-bhearnach, an-mhíchruinn agus an-lochtach 0-[35]')
BOXES = ['– FILÍOCHT AINMNITHE nó FILÍOCHT ROGHNACH – (30 marc)', 'Ceist 3 FILÍOCHT (30 marc)']
MARC5_TABLE = re.compile(r'Catagóir Marc as 5 Sármhaith 5 An-mhaith 4 Maith 3 Measartha 2 Lag/An-lag 0-1(?! 0)')


def place_tables(pieces):
    """Return each printed band table to the sub-question it sits beside: Plé to (i), Marc as 5 to (ii)."""
    pieces = list(pieces)
    for pattern, home in [(PLE_TABLE, 0), (MARC5_TABLE, 1)]:
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
    paper_path = ROOT / f'paper-trail-corpus/exampapers/2022/{FILE}.pdf'
    scheme_path = ROOT / f'paper-trail-corpus/markingschemes/2022/{SCHEME_FILE}.pdf'
    assert hashlib.sha256(paper_path.read_bytes()).hexdigest() == PAPER_SHA, 'Paper changed: repeat visual review'
    assert hashlib.sha256(scheme_path.read_bytes()).hexdigest() == SCHEME_SHA, 'Scheme changed: repeat visual review'
    paper, doc = fitz.open(paper_path), fitz.open(scheme_path)
    texts = [clean(p.get_text()) for p in paper]
    s = Scheme(doc, 18, 50)
    general = s.chunk('Freagair Léamhthuiscint A nó Léamhthuiscint B. Tá Ceist 1', 'Siombailí Anótála')[0]
    # (q, part, paper prompt, scheme anchor, marks, mode)
    passages = {
        'A': dict(title='Máire Mhac an tSaoi – Laoch ar Lár', pages=[4, 5], topic='irish-3-0', end='LÉAMHTHUISCINT B (50 marc)', parts=[
            ('1', 'a', '(a) Cén nós a bhíonn ag daoine ag deireadh gach bliana? (Alt 1)', '1. (a) Cén nós a bhíonn', 3, None),
            ('1', 'bi', '(b) (i) Scríobh síos rud amháin a dúirt an tUachtarán, Micheál D. Ó hUiginn, nuair a cailleadh Máire Mhac an tSaoi. (Alt 1)', '(b) (i) Scríobh síos rud amháin a dúirt an tUachtarán', 2, None),
            ('1', 'bii', '(ii) Luaigh rud amháin a dúradh sna hailt a foilsíodh in irisí agus i nuachtáin in ómós do Mháire Mhac an tSaoi. (Alt 1)', '(ii) Luaigh rud amháin a dúradh', 2, None),
            ('2', 'a', '(a) Tabhair dhá phointe eolais faoi athair Mháire, Seán Mac an tSaoi. (Alt 2)', '2. (a) Tabhair dhá phointe eolais faoi athair', 3, 'ordered'),
            ('2', 'bi', '(b) (i) Cá bhfios dúinn go raibh cumas intleachta as an ngnách i Máire? (Alt 2)', '(b) (i) Cá bhfios dúinn', 2, None),
            ('2', 'bii', '(ii) Cén fáth arbh éigean do Mháire an plean a bhí aici chun dul ag staidéar in Institut des Hautes Études en Sorbonne i bPáras, a chur ar athlá? (Alt 2)', '(ii) Cén fáth arbh éigean', 2, None),
            ('3', 'a', '(a) Scríobh síos dhá chúis nach ndeachaigh Máire leis an dlí mar ghairm bheatha riamh. (Alt 3)', '3. (a) Scríobh síos dhá chúis nach ndeachaigh', 3, 'ordered'),
            ('3', 'bi', '(b) (i) Cén toradh a bhí ar scrúdú oscailte iomaíoch na Státseirbhíse a rinne Máire? (Alt 3)', '(b) (i) Cén toradh a bhí ar scrúdú', 2, None),
            ('3', 'bii', '(ii) Cén obair a rinne Máire ar feadh trí bliana nuair a d’fhill sí ar Bhaile Átha Cliath as Maidrid? (Alt 3)', '(ii) Cén obair a rinne Máire', 2, None),
            ('4', 'a', '(a) Tabhair dhá shlí ina raibh tionchar mór ag uncail Mháire, an Moinsíneoir Pádraig de Brún, ar a saol ó thaobh na Gaeilge de. (Alt 4)', '4. (a) Tabhair dhá shlí ina raibh tionchar', 3, 'ordered'),
            ('4', 'bi', '(b) (i) Conas a chuir na tréimhsí a chaith Máire i gCorca Dhuibhne lena cumas filíochta? (Alt 4)', '(b) (i) Conas a chuir na tréimhsí', 2, None),
            ('4', 'bii', '(ii) Luaigh rud amháin a dúirt Máire in agallamh san iris Comhar in 2012. (Alt 4)', '(ii) Luaigh rud amháin a dúirt Máire in agallamh', 2, None),
            ('5', 'a', '(a) Cén fáth a ndeirtear go raibh Máire Mhac an tSaoi misniúil ó thaobh téamaí de ina cuid filíochta? (Alt 5)', '5. (a) Cén fáth a ndeirtear', 3, None),
            ('5', 'bi', '(b) (i) Luaigh an dá chúis ar bhain sí úsáid as pearsana ban as traidisiúin litríochta na Gaeilge ina cuid filíochta. (Alt 5)', '(b) (i) Luaigh an dá chúis ar bhain sí', 2, 'slots'),
            ('5', 'bii', '(ii) Cad a spreag Máire chun scríobh faoi Phiaras Feiritéar? (Alt 5)', '(ii) Cad a spreag Máire', 2, None),
            ('6', 'a', '(a) Aimsigh sampla de bhriathar sa Mhodh Coinníollach in Alt 1 agus sampla den bhriathar saor san Aimsir Fháistineach in Alt 5.', '6. (a) Aimsigh sampla de bhriathar sa Mhodh', 3, 'grammar'),
            ('6', 'b', '(b) Bunaithe ar an eolas sa sliocht thuas, déan plé ar dhá thréith de chuid Mháire Mhac an tSaoi, dar leat. Bíodh sampla amháin ón sliocht agat, i d’fhocail féin, ag tacú le gach tréith a luann tú i do fhreagra. (Is leor 60 focal.)', '(b) Bunaithe ar an eolas sa sliocht thuas, déan plé', 12, 'traits')]),
        'B': dict(title='Ceol Traidisiúnta na hÉireann', pages=[6, 7], topic='irish-3-1', end='⟦26⟧', parts=[
            ('1', 'a', '(a) Scríobh síos dhá chúis a bhfuil ár bhféiniúlacht chultúrtha tábhachtach dúinn mar Ghaeil. (Alt 1)', '1. (a) Scríobh síos dhá chúis a bhfuil', 3, 'ordered'),
            ('1', 'bi', '(b) (i) Luaigh pointe amháin eolais faoin bhféile cheoil bhliantúil, Fleadh Cheoil na hÉireann. (Alt 1)', '(b) (i) Luaigh pointe amháin eolais faoin bhféile', 2, None),
            ('1', 'bii', '(ii) Tabhair toradh amháin a bhí ar na seónna Riverdance agus Lord of the Dance. (Alt 1)', '(ii) Tabhair toradh amháin', 2, None),
            ('2', 'a', '(a) Luaigh dhá phointe eolais faoin obair a rinne Conradh na Gaeilge chun an Ghaeilge agus an fhéiniúlacht chultúrtha a chur chun cinn. (Alt 2)', '2. (a) Luaigh dhá phointe eolais faoin obair', 3, 'ordered'),
            ('2', 'bi', '(b) (i) Cén fáth ar bunaíodh Coimisiún Béaloideas Éireann i 1935? (Alt 2)', '(b) (i) Cén fáth ar bunaíodh', 2, None),
            ('2', 'bii', '(ii) Cén tábhacht a bhain leis an obair bhailiúcháin a rinne Séamus Ennis agus bailitheoirí ceoil eile? (Alt 2)', '(ii) Cén tábhacht a bhain', 2, None),
            ('3', 'a', '(a) Cén cóiriú nuálach a chuir Seán Ó Riada ar an gceol traidisiúnta sa scannán Mise Éire? (Alt 3)', '3. (a) Cén cóiriú nuálach', 3, None),
            ('3', 'bi', '(b) (i) Cén bealach nua a d’aimsigh Ó Riada agus Ceoltóirí Chualann leis an gceol traidisiúnta a chur i láthair an phobail? (Alt 3)', '(b) (i) Cén bealach nua', 2, None),
            ('3', 'bii', '(ii) Luaigh rud amháin a léiríonn gur chuir The Chieftains ceol traidisiúnta na hÉireann ar an stáitse idirnáisiúnta. (Alt 3)', '(ii) Luaigh rud amháin a léiríonn', 2, None),
            ('4', 'a', '(a) Scríobh síos dhá phointe eolais faoi thraidisiún na píbe uilleann faoi na 1960idí. (Alt 4)', '4. (a) Scríobh síos dhá phointe eolais faoi thraidisiún', 3, 'ordered'),
            ('4', 'bi', '(b) (i) Tabhair sampla amháin den bhaint a bhí ag Liam Óg Ó Floinn leis an bhfás mór a tháinig ar cháil na píbe uilleann. (Alt 4)', '(b) (i) Tabhair sampla amháin den bhaint', 2, None),
            ('4', 'bii', '(ii) Cén fáth a bhfuil an Phíobaireacht Uilleann agus an Chruitireacht aitheanta ag Eagraíocht Oideachais, Eolaíochta agus Chultúir na Náisiún Aontaithe (UNESCO)? (Alt 4)', '(ii) Cén fáth a bhfuil an Phíobaireacht', 2, None),
            ('5', 'a', '(a) Scríobh síos dhá bhealach a gcabhraíonn forbairtí na teicneolaíochta le cur chun cinn an cheoil thraidisiúnta le blianta beaga anuas. (Alt 5)', '5. (a) Scríobh síos dhá bhealach', 3, 'ordered'),
            ('5', 'bi', '(b) (i) Luaigh dhá chúram atá ar an gComhairle Ealaíon. (Alt 5)', '(b) (i) Luaigh dhá chúram', 2, 'slots'),
            ('5', 'bii', '(ii) Scríobh síos dhá phointe eolais faoi Thaisce Cheol Dúchais Éireann i mBaile Átha Cliath. (Alt 5)', '(ii) Scríobh síos dhá phointe eolais faoi Thaisce', 2, 'slots'),
            ('6', 'a', '(a) Aimsigh sampla den bhriathar saor san Aimsir Chaite in Alt 2 agus sampla d’ainmfhocal baininscneach sa tuiseal ginideach uatha in Alt 5.', '6. (a) Aimsigh sampla den bhriathar saor', 3, 'grammar'),
            ('6', 'b', '(b) Conas a chuaigh an sliocht seo i bhfeidhm ort? Tabhair dhá phointe eolais, i d’fhocail féin, as an sliocht, mar thacaíocht le do fhreagra. (Is leor 60 focal.)', '(b) Conas a chuaigh an sliocht seo', 12, 'opinion')]),
    }
    tariffs = {'traits': '{6 mharc + 6 mharc}', 'opinion': 'C (2) = 2 mharc', 'slots': '{2 mharc: 1 mharc + 1 mharc}',
               'ordered': '{3 mharc: 2 mharc + 1 mharc}', 'grammar': '{3 mharc: 2 mharc + 1 mharc}'}
    # Two parts print the split beside the count instead of inside the brace.
    printed_tariff = {('B', '5', 'a'): '(Dhá bhealach: 2 mharc + 1 mharc) {3 mharc}',
                      ('B', '5', 'bi'): '(Dhá chúram: 1 mharc + 1 mharc) {2 mharc}'}
    start_b = s.text.index('LÉAMHTHUISCINT B (50 marc)')
    for letter, passage in passages.items():
        page_text = ' '.join(texts[p - 1] for p in passage['pages'])
        anchors = [p[3] for p in passage['parts']]
        resolved = []
        pos = start_b if letter == 'B' else 0
        for index, (q, part, prompt, anchor, marks, mode) in enumerate(passage['parts']):
            assert in_order(prompt, page_text), (letter, q, part)
            here = s.text.index(anchor, pos)
            assert letter == 'B' or here < start_b, (letter, q, part)
            chunk, spages = s.chunk(anchor, anchors[index + 1] if index + 1 < len(anchors) else passage['end'], pos)
            pos = here + 1
            assert printed_tariff.get((letter, q, part), tariffs.get(mode, f'{{{marks} mharc}}')) in chunk, (letter, q, part, chunk[:90])
            assert 'Siombailí' not in chunk and 'LÉAMHTHUISCINT B' not in chunk and 'An Litríocht' not in chunk, (letter, q, part)
            resolved.append((q, part, prompt, anchor, marks, mode, chunk, spages))
        passage['resolved'] = resolved
    note5 = s.chunk('Nóta: I gcás na gceisteanna 2 (Prós)', 'Nóta: Níl na nótaí tacaíochta seo uileghabhálach ná críochnúil agus bronnfar marcanna ar phointí bailí')[0]
    poetry_notes = s.chunk('Nóta: Níl na nótaí tacaíochta seo uileghabhálach ná críochnúil agus bronnfar marcanna ar phointí ábhartha', '3A. Filíocht Ainmnithe')[0]
    gaeilge_table = GAEILGE_TABLE.search(s.text, s.text.index('⟦32⟧')).group(0)
    # Ceist 4's notes and its 35-mark table, which the scheme prints beside the Gaeilge column.
    general4 = s.chunk('Treoracha: Iarrtar ar na hiarrthóirí plé a dhéanamh ar an ráiteas', 'Catagóir Eolas (35 marc)', s.text.index('⟦41⟧'))[0]
    assert all(x in gaeilge_table for x in ['Sárchumas', 'Cumas lag/an-lag']) and general4.endswith('as 5 mharc.')
    _MATERIAL = dict(paper=paper, texts=texts, s=s, general=general, passages=passages, note5=note5, poetry_notes=poetry_notes,
                     gaeilge_table=gaeilge_table, general4=general4, decisions=selection_decisions(paper))
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
    """Lift the 2022 scheme onto the retained legacy cards the route review left (IDs, totals and topics unchanged)."""
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
             'B': '6(b) is one response: how the extract affected the reader 2 and two supported points 5 + 5, in the candidate’s own words.'}
    for letter, passage in m['passages'].items():
        by_q = {}
        for q, part, prompt, anchor, marks, mode, chunk, spages in passage['resolved']:
            by_q.setdefault(q, []).append((part, marks, mode, chunk, spages))
        for q, parts in by_q.items():
            card = by_id[f'irish-2022-hl-p2-reading-{letter.lower()}-q{q}']
            assert card['topicId'] == passage['topic'], card['id']
            crits = [c for part, marks, mode, chunk, _ in parts for c in part_criteria(q, part, marks, mode, chunk, m['general'])]
            for c in crits:
                c['label'] = LABELS[c['id']]
            n = str(int(q) + (6 if letter == 'B' else 0))
            stamp(card['id'], n, passage['pages'], sorted({p for *_, sp in parts for p in sp}), crits,
                  'Retained complete printed question. Score each published part separately using these SEC allocations.'
                  + (' Two-answer grammar is one 0/2/3 placement; ' + six_b[letter] if q == '6' else ''),
                  ['Léigh an sliocht oifigiúil a ghabhann leis an gceist.', 'Freagair gach fochuid agus cloígh leis an alt a luaitear.',
                   'Bain úsáid as do chuid focal féin nuair a iarrtar ort é.'])

    s = m['s']
    lit_requirements = ['Freagair gach cuid den cheist atá priontáilte.', 'Úsáid tagairtí cruinne agus ábhartha don téacs.']
    # 3A, prescribed poems: (i) 13, (ii) 5, (iii) 7 plus the shared Gaeilge 5; the paper prints (i) 15, (ii) 6, (iii) 9.
    poems = [('poetry-3a-a', 'F-3A-a', [10], '(a) An tEarrach Thiar (i)', '(b) Colscaradh (i)', ['(ii) Críochnaíonn gach véarsa', '(iii) Cé a chum an dán seo?'], 'irish-5-3'),
             ('poetry-3a-b', 'F-3A-b', [11], '(b) Colscaradh (i)', '3B. Filíocht Roghnach', ['(ii) Cén éifeacht a bhaineann', '(iii) Cé a chum an dán seo?'], 'irish-5-5')]
    for slug, atlas, pages, start, end, cuts, topic in poems:
        card_id = f'irish-2022-hl-p2-{slug}'
        assert by_id[card_id]['topicId'] == topic and by_id[card_id]['totalMarks'] == 30, card_id
        whole, spages = s.chunk(start, end)
        # The printed Gaeilge table can sit between sub-questions; it belongs to the shared award, not to Eolas.
        whole = re.sub(r'^nó ', '', GAEILGE_TABLE.sub(' ', whole)).strip()
        # Scheme PDF 33 stores its boxed section headings inside 3A(a)'s notes; they are page furniture, never marking.
        boxes = [b for b in BOXES if b in whole]
        assert boxes == (BOXES if slug == 'poetry-3a-a' else []), (slug, boxes)
        for box in boxes:
            whole = clean(whole.replace(box, ' '))
        assert 'Gaeilge (5 mharc)' not in whole, slug
        pieces = split_parts(whole, cuts, ['Eolas = 13 mharc', 'Eolas = 5 mharc', 'Eolas = 7 marc'])
        assert PLE_TABLE.search(pieces[0]) and MARC5_TABLE.search(pieces[1]), slug
        assert not MARC5_TABLE.search(pieces[2]) and not PLE_TABLE.search(pieces[2]) and not PLE_TABLE.search(pieces[1]), slug
        stamp(card_id, atlas, pages, sorted(set(spages) | {33}),
              [criterion('eolas-i', '(i) Eolas', 13, [pieces[0], m['poetry_notes']], 'indicative'), criterion('eolas-ii', '(ii) Eolas', 5, [pieces[1]], 'indicative'),
               criterion('eolas-iii', '(iii) Eolas', 7, [pieces[2]], 'indicative'), gaeilge(m)],
              'One complete SEC response with one shared five-mark Gaeilge award. The paper prints (i) 15, (ii) 6 and (iii) 9; the scheme assesses '
              'Eolas 13, 5 and 7 with the conditions shown, plus Gaeilge 5 once. Supporting notes are indicative rather than exhaustive.', lit_requirements)

    # 3B(a)(ii): the route review keeps the whole printed sub-question; the scheme prints its price after the
    # prompt's bracketed "(Is leor pointe amháin eolais … fhreagra)" without a closing full stop, so the criterion
    # carries the scheme's pricing slice from "Eolas = 5 mharc" (the prompt itself is on the card).
    route = by_id['irish-2022-hl-p2-poetry-3b-a']
    assert [c['id'] for c in route['criteria']] == ['eolas-i', 'eolas-ii', 'eolas-iii', 'gaeilge'], route['id']
    ii, _ = s.chunk('Eolas = 5 mharc Pointe amháin eolais = 5 mharc Mar phointe eolais', '(iii) Cé a chum an dán seo?', s.text.index('⟦38⟧'))
    assert ii.endswith('línte cuí an dáin.'), ii[-60:]
    route['criteria'][1]['guidance'] = [ii]
    # Two prose routes open their Eolas slice one word off the scheme's own option heading: An Lasair Choille keeps the
    # separator "nó" before its title, Hurlamaboc starts after "(b) Hurlamaboc". Each becomes the printed heading itself.
    for card_id, old, new in [('irish-2022-hl-p2-prose-2a-a-an-lasair-choille', ' nó An Lasair Choille Eolas = 25 marc', ' An Lasair Choille Eolas = 25 marc'),
                              ('irish-2022-hl-p2-prose-2a-b', ' Eolas = 25 marc ‘Tá léiriú sa ghiota', ' (b) Hurlamaboc Eolas = 25 marc ‘Tá léiriú sa ghiota')]:
        eolas = by_id[card_id]['criteria'][0]
        assert eolas['id'] == 'eolas' and eolas['guidance'][0].count(old) == 1, card_id
        assert new.strip() in s.text, card_id
        eolas['guidance'][0] = eolas['guidance'][0].replace(old, new)

    options = [('literature-4-a', 'X-4A', '4A. An Triail', '4B. A Thig Ná Tit Orm', 'irish-6-0'),
               ('literature-4-b', 'X-4B', '4B. A Thig Ná Tit Orm', '4C. Tóraíocht Dhiarmada', 'irish-6-1'),
               ('literature-4-c', 'X-4C', '4C. Tóraíocht Dhiarmada', '4D. Gafa', 'irish-6-2'),
               ('literature-4-d', 'X-4D', '4D. Gafa', '4E. Canary Wharf', 'irish-6-3'),
               ('literature-4-e', 'X-4E', '4E. Canary Wharf', '4F. Dánta Breise', 'irish-6-4')]
    for slug, atlas, start, end, topic in options:
        card_id = f'irish-2022-hl-p2-{slug}'
        assert by_id[card_id]['topicId'] == topic and by_id[card_id]['totalMarks'] == 40, card_id
        chunk, spages = s.chunk(start, end, s.text.index('⟦42⟧'))
        assert 'Eolas = 35 marc' in chunk and 'Gaeilge (5 mharc)' not in chunk, slug
        stamp(card_id, atlas, [13], sorted(set(spages) | {41}),
              [criterion('eolas', 'Eolas', 35, [chunk, m['general4']], 'indicative'), gaeilge(m)],
              'One complete SEC response: Eolas 35 assessed as a unit with a single shared 5-mark Gaeilge award. Supporting notes are indicative rather than exhaustive.',
              lit_requirements)
    whole, spages = s.chunk('4F. Dánta Breise', None, s.text.index('⟦48⟧'))
    whole = GAEILGE_TABLE.sub(' ', whole).strip()
    pieces = [clean(x) for x in (whole[:whole.index('(ii) Déan cur síos')], whole[whole.index('(ii) Déan cur síos'):whole.index('(iii) Cén mheadaracht')],
                                 whole[whole.index('(iii) Cén mheadaracht'):])]
    for piece, cap in zip(pieces, ['Eolas = 19 marc', 'Eolas = 8 marc', 'Eolas = 8 marc']):
        assert cap in piece, cap
    # 4F(ii)'s point-band grid ("Catagóir Pointe eolais 1 (4 mharc) Pointe eolais 2 (4 mharc) Sár-mhaith 4 4 …") reads as
    # two more 4-mark parts to the tariff cutter, so the criterion stops before it; the printed 4 + 4 is in the note.
    grid = pieces[1].index('Catagóir Pointe eolais 1 (4 mharc) Pointe eolais 2 (4 mharc) Sár-mhaith 4 4')
    pieces[1] = pieces[1][:grid].strip()
    assert by_id['irish-2022-hl-p2-literature-4-f']['topicId'] == 'irish-6-6'
    stamp('irish-2022-hl-p2-literature-4-f', 'X-4F', [13, 14, 15], spages,
          [criterion('eolas-i', '(i) Eolas', 19, [pieces[0], m['general4']], 'indicative'), criterion('eolas-ii', '(ii) Eolas', 8, [pieces[1]], 'indicative'),
           criterion('eolas-iii', '(iii) Eolas', 8, [pieces[2]], 'indicative'), gaeilge(m)],
          'One complete SEC response: the paper prints (i) 20, (ii) 10 and (iii) 10; the scheme assesses Eolas 19, 8 (4 + 4 for the two points) and 8 '
          '(metre 2 + point 4 + example 2) plus one shared 5-mark Gaeilge award. Supporting notes are indicative rather than exhaustive.', lit_requirements)
    assert len(stamped) == 20
    for card_id in stamped + ['irish-2022-hl-p2-poetry-3b-a']:
        for c in by_id[card_id]['criteria']:
            assert c['guidance'] and all(not re.search('[-]', g) for g in c['guidance']), (card_id, c['id'])
    return cards, stamped


def build():
    m = material()
    cards = []

    def add(key, slug, ref, prompt, topic, pages, scheme_pages, criteria, note, extra_topics=None, title=None, focus=None):
        cards.append(dict(
            id=f'irish-2022-hl-p2-{slug}', year=2022, level='higher', paper=2, section='2',
            atlasQuestionId=key, questionRef=f'2022 HL Paper 2 {ref}', questionText=prompt,
            totalMarks=sum(c['maxMarks'] for c in criteria), topicId=topic,
            **({'additionalTopicIds': extra_topics} if extra_topics else {}),
            conceptId=f'irish-hl-p2-{slug}', paperFileid=FILE, schemeFileid=SCHEME_FILE,
            schemePage=scheme_pages[0], schemePages=scheme_pages, reviewedAt=REVIEWED_AT, reviewedPaperPages=pages,
            taskRequirements=READING_REQUIREMENTS, criteria=criteria, markingGuideNote=note,
            sourceMaterial=dict(kind='source-text', label=ref.split(' · ')[0], title=title, pages=pages,
                                attribution='© State Examinations Commission.', presentationNote=SOURCE_NOTE),
            **({'practiceFocus': focus} if focus else {})))

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
                        text, topic, passage['pages'], spages,
                        [criterion(f'{part}-{slot}', f'Freagra {slot}', 1, [chunk, m['general']])],
                        'The scheme prices the two answers 1 mharc + 1 mharc independently; this card practises one of them. ' + PART_NOTE, None, passage['title'],
                        f'One of the two answers (answer {slot}, 1 mark)')
            if mode == 'traits':
                for slot in (1, 2):
                    add(f'R-{letter}-{q}-{part}-{slot}', f'reading-{letter.lower()}-q{q}-{part}-{slot}', f'Léamhthuiscint {letter} · Ceist {label} · Tréith {slot}',
                        text,
                        topic, passage['pages'], spages, [criterion(f'trait-{slot}', f'Tréith {slot}', 6, [chunk, m['general']])],
                        'The scheme prices the two traits 6 + 6 independently (trait 2 + support 4); this card practises one of them. ' + PART_NOTE, None, passage['title'],
                        f'One of the two traits, discussed with one example from the extract in your own words (trait {slot}, 6 marks)')
    assert len(cards) == 42 and len({c['id'] for c in cards}) == 42
    for card in cards:
        for c in card['criteria']:
            assert c['guidance'] and all(not re.search('[-]', g) for g in c['guidance']), (card['id'], c['id'])
    sr = json.loads(SOURCE_REVIEW.read_text())
    legacy = ([f'irish-2022-hl-p2-reading-{l}-q{q}' for l in 'ab' for q in range(1, 7)]
              + [f'irish-2022-hl-p2-prose-{k}' for k in ['2a-a', '2a-a-an-lasair-choille', '2a-b', '2b-a', '2b-b']]
              + [f'irish-2022-hl-p2-poetry-{k}' for k in ['3a-a', '3a-b', '3b-a', '3b-b']]
              + [f'irish-2022-hl-p2-literature-4-{k}' for k in 'abcdef'])
    review = dict(year=2022, level='higher', paperFileid=FILE + '.pdf', schemeFileid=SCHEME_FILE + '.pdf',
                  paperSha256=PAPER_SHA, schemeSha256=SCHEME_SHA,
                  reviewedPaperPages=list(range(1, 17)), reviewedSchemePages=sr['reviewedSchemePages'], schemeScope=sr['schemeScope'],
                  reviewDate=REVIEWED_AT, status='reviewed', fullPaperAndApplicableSchemeVisualSweep=True, selectionDecisions=m['decisions'],
                  readingPracticeCardIds=[c['id'] for c in cards], legacyCardIds=legacy, readingWholeCardIds=legacy[:12],
                  routeReviewedCardIds=legacy[12:17] + legacy[19:21],
                  examStructure=dict(readingA=50, readingB=50, prose=30, poetry=30, additionalLiterature=40, total=200),
                  nonPoolDecisions=sr['nonPoolDecisions'], openIssues=[], caveats=sr['sourceFindings'],
                  boundaries='12 retained whole reading questions with 34 published parts, 6 independent one-mark answer slots and 2 six-mark trait slots; '
                             '5 retained prose, 4 poetry and 6 additional-literature routes.')
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
    print(f"Irish Higher 2022 Paper 2: {len(data['cards'])} added reading cards (+27 retained legacy cards); the archive remains incomplete.")


if __name__ == '__main__':
    main()
