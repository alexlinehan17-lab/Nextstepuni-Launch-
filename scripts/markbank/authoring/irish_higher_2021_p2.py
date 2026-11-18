#!/usr/bin/env python3
"""Reviewed 2021 Higher Paper 2 (Léamhthuiscint agus Litríocht).

Paper PDF 1–16 and the Paper 2 pages of the combined LC001ALP000IV scheme (PDF 17–49,
plus 50 modified marking) reviewed on 2026-11-04. Counts are assertions, not
corpus-completeness proof. Same method as irish_higher_2023_p2.py.

The legacy generator already ships 26 cards for this component: the twelve whole
reading questions and the fourteen literature routes. Their IDs are kept.
`apply_legacy_review` (called by irish_cards.py) joins them to Atlas and replaces their
marking with the lifted 2021 scheme (each reading part and each poetry and 4F
sub-question keeps its own published tariff). `build` adds every published reading part
as a practice card, plus the independent 1 + 1 answer slots and the 6 + 6 trait slots,
beside the legacy file.

2021 differs from 2023 in its scheme layout: reading starts on PDF 17 with the
marking instructions; the prose and additional-literature band tables print Eolas and
Gaeilge side by side; every literature answer closes with the examiner's marking-panel
note ("Nóta: Caithfidh an Scrúdaitheoir …"), after which the text layer stores the
Marc as 4/3/5/7 tables of the sub-questions above. Léamhthuiscint A 6(b) asks for two
traits (6 + 6) and Léamhthuiscint B 6(b) for a response (2) and two points (5 + 5).
The 2021 boxed headings ("Ceist 4 LITRÍOCHT BHREISE (40 marc)", "– PRÓS AINMNITHE nó
PRÓS ROGHNACH – (30 marc)" …) are removed here by exact match (FURNITURE).
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
OUT = ROOT / 'components/MarkBank/cards/irish/higher-2021-p2-authored.json'
SOURCE_REVIEW = ROOT / 'scripts/markbank/authored/irish-higher-2021-p2-source-review.json'
REVIEWED_AT = '2026-11-04'
PAPER_SHA = '4c2a95b59493aed0bef9ca4298116de2757008bf5c148f84d631b4d18b58e239'
SCHEME_SHA = '7482066da1b9dbe0494b79c1d769008484c9e28f106d83f3858bf02a310bc337'
DIRECTIVE = re.compile(r'rogha|roghna|Freagair|Luaigh|Ainmnigh|\bnó\b|dhá phointe|dhá rud|dhá bh|dhá dh|dhá ch|dhá fh|dhá th|'
                       r'ceann amháin|pointe amháin|\bdhá\b|an dá\b|amháin', re.I)
SOURCE_NOTE = 'Shown page-for-page from the official examination paper; swipe to move between pages.'
# Boxed page headings the 2021 text layer stores inside the literature pages; exact strings only.
FURNITURE = ('Ceist 2 PRÓS (30 marc)', 'Ceist 3 FILÍOCHT (30 marc)', 'Ceist 4 LITRÍOCHT BHREISE (40 marc)',
             '– PRÓS AINMNITHE nó PRÓS ROGHNACH – (30 marc)', '– FILÍOCHT AINMNITHE nó FILÍOCHT ROGHNACH – (30 marc)')
# The examiner's marking-panel note that closes each literature answer: the boundary of the answer's own text.
PANEL = 'Nóta: Caithfidh an Scrúdaitheoir'


def clean(text):
    return re.sub(r'\s+', ' ', symbol_text(text)).strip()


def unbox(text):
    for heading in FURNITURE:
        text = text.replace(heading, ' ')
    return clean(text)


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
        return unbox(re.sub(r'⟦\d+⟧', ' ', raw)), sorted(pages)

    def page(self, number):
        return self.text.index(f'⟦{number}⟧')


GAEILGE_TABLE = re.compile(r'Gaeilge \(5 mharc\) Sárchumas.*?Cumas lag/an-lag maidir leis na príomhghnéithe de cheart na teanga \(gramadach, comhréir, struchtúr, deilbhíocht\) 1')
# Band tables the text layer stores away from the sub-question they price.
PLE_TABLE = re.compile(r'Catagóir (?:An plé|Plé) \(1[13] mharc\) Marcanna .*?Lag/An-lag Eolas an-bhearnach, an-mhíchruinn agus an-lochtach 0-[35]')
MARC4_TABLE = 'Catagóir Marc as 4 Sármhaith 4 An-mhaith 3 Maith 2 Measartha 1 Lag/An-lag 0'
MARC3_TABLE = 'Catagóir Marc as 3 Sármhaith 3 An-mhaith/Maith 2 Measartha 1 Lag/An-lag 0'
MARC7_TABLE = 'Catagóir Marc as 7 Sár-mhaith 6-7 An-mhaith 5 Maith 4 Measartha 3 Lag/An-lag 0-2'
MARC54_TABLE = 'Catagóir Marc as 5 Marc as 4 Sármhaith 5 4 An-mhaith 4 3 Maith 3 2 Measartha 2 1 Lag/An-lag 0-1 0'
EOLAS17_TABLE = re.compile(r'Catagóir Eolas \(17 marc\) Sármhaith .*?Lag/An-lag Eolas an-bhearnach, an-mhíchruinn agus an-lochtach 0-5')


def printed_values(chunk, marks):
    values = re.findall(r'= (\d+) mh?arc', chunk) + re.findall(r'bronntar (\d+) mh?arc', chunk)
    return sorted({0, marks} | {int(v) for v in values if int(v) <= marks})


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
    s = Scheme(doc, 17, 49)
    # The marking instructions, from their first rule (their heading "Treoracha do mharcáil na Léamhthuisceana:" is a title).
    general = s.chunk('Tá Ceist 1 – 5 ar cómharc', 'Ceist 1 LÉAMHTHUISCINT (50 marc)')[0]
    # (q, part, paper prompt, scheme anchor, marks, mode, printed tariff). Each passage ends where the examiner's
    # marking panel for 6(b) begins ("T1 (2) + S1 (4) = …", "C (2) = P1 (5) = …").
    passages = {
        'A': dict(title='John Hume – Laoch na Síochána', pages=[4, 5], topic='irish-3-0', end='T1 (2) + S1 (4) = T2 (2) + S2 (4) =', parts=[
            ('1', 'a', '(a) Cén moladh a tugadh do John Hume nuair a fógraíodh a bhás ar an 3 Lúnasa 2020? (Alt 1)', '1. (a) Cén moladh a tugadh', 3, None, '{3 mharc}'),
            ('1', 'bi', '(b) (i) Scríobh síos cúis amháin ar bronnadh Duais Nobel na Síochána ar John Hume sa bhliain 1998. (Alt 1)', '(b) (i) Scríobh síos cúis amháin ar bronnadh', 2, None, '{2 mharc}'),
            ('1', 'bii', '(ii) Cén cur chuige a chothaigh Martin Luther King san fheachtas chun cearta sibhialta a bhaint amach do dhaoine gorma? (Alt 1)', '(ii) Cén cur chuige a chothaigh', 2, None, '{2 mharc}'),
            ('2', 'a', '(a) Scríobh síos dhá phointe eolais faoi thuismitheoirí John Hume. (Alt 2)', '2. (a) Scríobh síos dhá phointe eolais faoi thuismitheoirí', 3, 'ordered', '{3 mharc: 2 mharc + 1 mharc}'),
            ('2', 'bi', '(b) (i) Tabhair pointe amháin eolais faoi oideachas dara leibhéal John Hume. (Alt 2)', '(b) (i) Tabhair pointe amháin eolais faoi oideachas', 2, None, '{2 mharc}'),
            ('2', 'bii', '(ii) Luaigh dhá phointe eolais faoin bpobal náisiúnach i gcathair Dhoire nuair a d’fhill John abhaile sa bhliain 1957. (Alt 2)', '(ii) Luaigh dhá phointe eolais faoin bpobal', 2, 'slots', '{1 mharc + 1 mharc}'),
            ('3', 'a', '(a) Scríobh síos dhá chúis a mbeadh cathair Dhoire oiriúnach mar láthair don ollscoil nua. (Alt 3)', '3. (a) Scríobh síos dhá chúis a mbeadh', 3, 'ordered', '{3 mharc: 2 mharc + 1 mharc}'),
            ('3', 'bi', '(b) (i) Cén fáth ar bunaíodh an Derry Development Association? (Alt 3)', '(b) (i) Cén fáth ar bunaíodh', 2, None, '{2 mharc}'),
            ('3', 'bii', '(ii) Cén aidhm a bhí ag Gluaiseacht na gCeart Sibhialta i dTuaisceart Éireann? (Alt 3)', '(ii) Cén aidhm a bhí ag Gluaiseacht', 2, None, '{2 mharc}'),
            ('4', 'a', '(a) Cén dearcadh polaitiúil a bhí ag Hume agus ag an SDLP ar thodhchaí an tuaiscirt? (Alt 4)', '4. (a) Cén dearcadh polaitiúil', 3, None, '{3 mharc}'),
            ('4', 'bi', '(b) (i) Cén fáth ar thosaigh John Hume cainteanna rúnda le Gerry Adams sa bhliain 1986? (Alt 4)', '(b) (i) Cén fáth ar thosaigh John Hume', 2, None, '{2 mharc}'),
            ('4', 'bii', '(ii) Cén toradh a bhí ar na cainteanna síochána idir John Hume agus Gerry Adams? (Alt 4)', '(ii) Cén toradh a bhí ar na cainteanna', 2, None, '{2 mharc}'),
            ('5', 'a', '(a) Scríobh síos dhá rud a dúirt an tUachtarán Bill Clinton ina óráid nuair a thug sé cuairt ar chathair Dhoire i 1995. (Alt 5)', '5. (a) Scríobh síos dhá rud a dúirt', 3, 'ordered', '{3 mharc: 2 mharc + 1 mharc}'),
            ('5', 'bi', '(b) (i) Cad a dúirt John Hume i ráiteas agus é ag machnamh ar a shaol sa pholaitíocht? (Alt 5)', '(b) (i) Cad a dúirt John Hume i ráiteas', 2, None, '{2 mharc}'),
            ('5', 'bii', '(ii) Luaigh dhá rud a dúirt mac John Hume faoina athair ag Aifreann a shochraide. (Alt 5)', '(ii) Luaigh dhá rud a dúirt mac', 2, 'slots', '{2 mharc: 1 mharc + 1 mharc}'),
            ('6', 'a', '(a) Aimsigh sampla de bhriathar sa Mhodh Coinníollach in Alt 3 agus sampla den bhriathar saor san Aimsir Chaite in Alt 5.', '6. (a) Aimsigh sampla de bhriathar sa Mhodh', 3, 'grammar', '{3 mharc: 2 mharc + 1 mharc}'),
            ('6', 'b', '(b) Bunaithe ar an eolas sa sliocht thuas, déan plé ar dhá thréith de chuid John Hume, dar leat. Bíodh sampla amháin ón sliocht agat, i d’fhocail féin, ag tacú le gach tréith a luann tú i do fhreagra. (Is leor 60 focal.)', '(b) Bunaithe ar an eolas sa sliocht thuas, déan plé', 12, 'traits', '{6 mharc + 6 mharc}')]),
        'B': dict(title='Scéalta ón mbliain 2020', pages=[6, 7], topic='irish-3-1', end='C (2) = P1 (5) = P2 (5) =', parts=[
            ('1', 'a', '(a) Tabhair dhá phointe eolais faoin mBreatimeacht. (Alt 1)', '1. (a) Tabhair dhá phointe eolais faoin mBreatimeacht', 3, 'ordered', '{3 mharc: 2 mharc + 1 mharc}'),
            ('1', 'bi', '(b) (i) Cén fáth ar thosaigh na léirsithe ag tacú leis an ngluaiseacht Black Lives Matter? (Alt 1)', '(b) (i) Cén fáth ar thosaigh na léirsithe', 2, None, '{2 mharc}'),
            ('1', 'bii', '(ii) Luaigh pointe amháin eolais faoi thoghadh Kamala Harris, an Leas‐Uachtarán nua ar Stáit Aontaithe Mheiriceá. (Alt 1)', '(ii) Luaigh pointe amháin eolais faoi thoghadh', 2, None, '{2 mharc}'),
            ('2', 'a', '(a) Scríobh síos dhá phointe eolais faoin easpa dídine sa tír seo, de réir na dtuairiscí sa nuacht le linn 2020. (Alt 2)', '2. (a) Scríobh síos dhá phointe eolais faoin easpa dídine', 3, 'ordered', '{3 mharc: 2 mharc + 1 mharc}'),
            ('2', 'bi', '(b) (i) Luaigh dhá bheartas de chuid an rialtais chun dul i ngleic le fadhb na heaspa dídine. (Alt 2)', '(b) (i) Luaigh dhá bheartas', 2, 'slots', '{2 mharc: 1 mharc + 1 mharc}'),
            ('2', 'bii', '(ii) Scríobh síos toradh fiúntach amháin a bhfuiltear ag súil leis ar bheartais an rialtais. (Alt 2)', '(ii) Scríobh síos toradh fiúntach', 2, None, '{2 mharc}'),
            ('3', 'a', '(a) Cén phríomhfhreagracht atá ar Chomhairle Slándála na Náisiún Aontaithe? (Alt 3)', '3. (a) Cén phríomhfhreagracht', 3, None, '{3 mharc}'),
            ('3', 'bi', '(b) (i) Luaigh dhá chuspóir a bhíonn le misin choimeádta síochána na Náisiún Aontaithe. (Alt 3)', '(b) (i) Luaigh dhá chuspóir', 2, 'slots', '{2 mharc = 1 mharc + 1 mharc}'),
            ('3', 'bii', '(ii) Cén sprioc a bheidh ag rialtas na hÉireann agus suíochán acu ar Chomhairle Slándála na Náisiún Aontaithe, dar le Leo Varadkar? (Alt 3)', '(ii) Cén sprioc a bheidh ag rialtas', 2, None, '{2 mharc}'),
            ('4', 'a', '(a) Cén fáth ar scríobh David Attenborough an leabhar A Life on Our Planet? (Alt 4)', '4. (a) Cén fáth ar scríobh David Attenborough', 3, None, '{3 mharc}'),
            ('4', 'bi', '(b) (i) Cad a deir David Attenborough faoi éin farraige an domhain? (Alt 4)', '(b) (i) Cad a deir David Attenborough', 2, None, '{2 mharc}'),
            ('4', 'bii', '(ii) Scríobh síos dhá chúis a bhfuil gá le toil na rialtas agus na bpobal uile ar fud an domhain, dar le David Attenborough. (Alt 4)', '(ii) Scríobh síos dhá chúis a bhfuil gá', 2, 'slots', '{2 mharc = 1 mharc + 1 mharc}'),
            ('5', 'a', '(a) Cén stádas a bheidh ag an nGaeilge san Aontas Eorpach faoin mbliain 2022? (Alt 5)', '5. (a) Cén stádas a bheidh ag an nGaeilge', 3, None, '{3 mharc}'),
            ('5', 'bi', '(b) (i) Cén fáth ar eagraíodh seimineáir agus ceardlanna ar líne i rith 2020? (Alt 5)', '(b) (i) Cén fáth ar eagraíodh seimineáir', 2, None, '{2 mharc}'),
            ('5', 'bii', '(ii) Luaigh dhá chúis a gcuirtear an comórtas Aistritheoirí Óga ar siúl. (Alt 5)', '(ii) Luaigh dhá chúis a gcuirtear', 2, 'slots', '{2 mharc: 1 mharc + 1 mharc}'),
            ('6', 'a', '(a) Aimsigh sampla den bhriathar saor san Aimsir Fháistineach in Alt 2 agus sampla d’ainmfhocal firinscneach sa tuiseal ginideach uatha in Alt 3.', '6. (a) Aimsigh sampla den bhriathar saor', 3, 'grammar', '{3 mharc: 2 mharc + 1 mharc}'),
            ('6', 'b', '(b) Conas a chuaigh an sliocht seo i bhfeidhm ort? Tabhair dhá phointe eolais, i d’fhocail féin, as an sliocht, mar thacaíocht le do fhreagra. (Is leor 60 focal.)', '(b) Conas a chuaigh an sliocht seo i bhfeidhm ort?', 12, 'opinion', 'C (2) = 2 mharc')]),
    }
    start_b = s.text.index('LÉAMHTHUISCINT B (50 marc)')
    for letter, passage in passages.items():
        page_text = ' '.join(texts[p - 1] for p in passage['pages'])
        anchors = [p[3] for p in passage['parts']]
        resolved = []
        pos = start_b if letter == 'B' else 0
        for index, (q, part, prompt, anchor, marks, mode, tariff) in enumerate(passage['parts']):
            assert in_order(prompt, page_text), (letter, q, part)
            # Anchors are searched forward from the previous part so repeated stems resolve in printed order.
            here = s.text.index(anchor, pos)
            assert letter == 'B' or here < start_b, (letter, q, part)
            chunk, spages = s.chunk(anchor, anchors[index + 1] if index + 1 < len(anchors) else passage['end'], pos)
            pos = here + 1
            assert tariff in chunk, (letter, q, part, chunk[:90])
            assert 'Siombailí' not in chunk and 'LÉAMHTHUISCINT B' not in chunk and 'Nóta: I gcás na gceisteanna' not in chunk, (letter, q, part)
            resolved.append((q, part, prompt, anchor, marks, mode, chunk, spages))
        passage['resolved'] = resolved
    assert sum(len(p['resolved']) for p in passages.values()) == 34
    note5 = s.chunk('Nóta: I gcás na gceisteanna 2 (Prós)', 'Nóta: Níl na nótaí tacaíochta seo uileghabhálach')[0]
    notes = s.chunk('Nóta: Níl na nótaí tacaíochta seo uileghabhálach', 'Freagair Ceist 2A (Prós Ainmnithe)')[0]
    poetry_notes = s.chunk('Nóta: Níl na nótaí tacaíochta seo uileghabhálach', '3A. Filíocht Ainmnithe', s.page(32))[0]
    gaeilge_table = GAEILGE_TABLE.search(s.text, s.page(30)).group(0)
    # The prose and additional-literature band tables print the Eolas and Gaeilge columns side by side.
    prose_table = s.chunk('Catagóir Eolas (25 marc) Gaeilge (5 mharc)', 'Ceist 2 PRÓS (30 marc)')[0]
    table35 = s.chunk('Catagóir Eolas (35 marc) Gaeilge (5 mharc)', 'Ceist 4 LITRÍOCHT BHREISE (40 marc)')[0]
    general4 = s.chunk('Treoracha: Iarrtar ar na hiarrthóirí plé a dhéanamh ar an ráiteas', 'Eolas (35) = Gaeilge (5) = C4 (40) =', s.page(40))[0]
    assert all(x in gaeilge_table for x in ['Sárchumas', 'Cumas lag/an-lag']) and '22-25' in prose_table and '0-9' in prose_table
    assert '30-35' in table35 and '0-13' in table35 and general4.endswith('sa fhreagarleabhar.')
    assert note5.endswith('ar Ghaeilge.') and notes.endswith('atá iontu.') and poetry_notes.endswith('atá iontu.')
    _MATERIAL = dict(paper=paper, texts=texts, s=s, general=general, passages=passages, note5=note5, notes=notes, poetry_notes=poetry_notes,
                     gaeilge_table=gaeilge_table, prose_table=prose_table, table35=table35, general4=general4,
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
        return [criterion('grammar' if mode == 'grammar' else part, 'Freagra', marks, [chunk, general], permitted=[0, 2, 3])]
    return [criterion(part, 'Freagra', marks, [chunk, general], permitted=printed_values(chunk, marks))]


def gaeilge(m):
    return criterion('gaeilge', 'Gaeilge', 5, [m['gaeilge_table'], m['note5']], 'quality')


def literature_answer(s, start, page, extra=()):
    """One literature answer: from its printed start to the examiner's marking-panel note, its tables moved home."""
    whole, spages = s.chunk(start, PANEL, s.page(page))
    whole = re.sub(r'^nó ', '', GAEILGE_TABLE.sub(' ', whole)).strip()
    assert 'Gaeilge (5 mharc)' not in whole and 'Eolas (25) =' not in whole, start
    return whole, spages


def split_parts(whole, cuts, caps):
    i2 = whole.index(cuts[0]); i3 = whole.index(cuts[1], i2)
    pieces = [whole[:i2].strip(), whole[i2:i3].strip(), whole[i3:].strip()]
    for piece, cap in zip(pieces, caps):
        assert cap in piece, cap
    return pieces


def move(pieces, table, home):
    """Return a band table the text layer stores beside another sub-question to the sub-question it prices."""
    table = table if isinstance(table, str) else None
    for k in range(len(pieces)):
        if k != home and table and table in pieces[k]:
            pieces[k] = clean(pieces[k].replace(table, ' '))
            pieces[home] = clean(pieces[home] + ' ' + table)
            return pieces
    return pieces


def apply_legacy_review(cards):
    """Lift the 2021 scheme onto the 26 retained legacy cards (IDs, totals and topics unchanged)."""
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
             'B': '6(b) is one response: the reaction 2 and two supported points 5 + 5, in the candidate’s own words.'}
    for letter, passage in m['passages'].items():
        by_q = {}
        for q, part, prompt, anchor, marks, mode, chunk, spages in passage['resolved']:
            by_q.setdefault(q, []).append((part, marks, mode, chunk, spages))
        for q, parts in by_q.items():
            crits = [c for part, marks, mode, chunk, _ in parts for c in part_criteria(q, part, marks, mode, chunk, m['general'])]
            for c in crits:
                c['label'] = LABELS[c['id']]
            n = str(int(q) + (6 if letter == 'B' else 0))
            card = by_id[f'irish-2021-hl-p2-reading-{letter.lower()}-q{q}']
            assert card['topicId'] == passage['topic'], card['id']
            stamp(card['id'], n, passage['pages'], sorted({p for *_, sp in parts for p in sp}), crits,
                  'Retained complete printed question. Score each published part separately using these SEC allocations.'
                  + (' Two-answer grammar is one 0/2/3 placement; ' + six_b[letter] if q == '6' else ''),
                  ['Léigh an sliocht oifigiúil a ghabhann leis an gceist.', 'Freagair gach fochuid agus cloígh leis an alt a luaitear.',
                   'Bain úsáid as do chuid focal féin nuair a iarrtar ort é.'])

    s, notes, prose_table = m['s'], m['notes'], m['prose_table']
    lit_requirements = ['Freagair gach cuid den cheist atá priontáilte.', 'Úsáid tagairtí cruinne agus ábhartha don téacs.']
    prose = [('prose-2a-a', 'P-2A-a', '(a) Oisín i dTír na nÓg', 28, None),
             ('prose-2a-b', 'P-2A-b', 'nó (b) Dís', 29, None),
             ('prose-2b-a', 'P-2B-a', '(a) Maidir le scéal béaloidis roghnach', 30, ('Catagóir 13 mharc 12 mharc', 'Gaeilge (5 mharc)')),
             ('prose-2b-b', 'P-2B-b', 'nó (b) Maidir le gearrscéal roghnach', 31, ('Catagóir An plé (23 marc)', '⟦32⟧'))]
    for slug, atlas, start, page, table in prose:
        chunk, spages = literature_answer(s, start, page)
        assert 'Eolas = 25 marc' in chunk, slug
        lines = [chunk]
        if table:
            band, bpages = s.chunk(table[0], table[1], s.page(page))
            lines.append(band)
            spages = sorted(set(spages) | set(bpages))
        card = by_id[f'irish-2021-hl-p2-{slug}']
        stamp(card['id'], atlas, [8], sorted(set(spages) | {27}),
              [criterion('eolas', 'Eolas', 25, lines + [prose_table, notes], 'indicative'), gaeilge(m)],
              'One complete SEC response: 25 Eolas and a single shared 5-mark Gaeilge award. Supporting notes are indicative rather than exhaustive. '
              'The printed band table gives the Eolas and Gaeilge columns side by side.', lit_requirements)

    poems = [('poetry-3a-a', 'F-3A-a', [9], '(a) Géibheann (i)', 32, ['(ii) An teideal oiriúnach', '(iii) Cé a chum an dán seo?'],
              [(MARC4_TABLE, 1)], ['Eolas = 13 mharc', 'Eolas = 5 mharc', 'Eolas = 7 marc'], []),
             ('poetry-3a-b', 'F-3A-b', [10], '(b) An Spailpín Fánach (i)', 34, ['(ii) Cén mothúchán is mó', '(iii) Cén mheadaracht'],
              [], ['Eolas = 13 mharc', 'Eolas = 5 mharc', 'Eolas = 7 marc'], [(MARC4_TABLE, 35, 1)]),
             ('poetry-3b-a', 'F-3B-a', [11], '(a) (i) Maidir le dán nua-aimseartha roghnach', 37, ['(ii) An bhfuil teideal an dáin', '(iii) Cé a chum an dán seo?'],
              [], ['Eolas = 13 mharc', 'Eolas = 5 mharc', 'Eolas = 7 marc'], []),
             ('poetry-3b-b', 'F-3B-b', [11], '(b) (i) Maidir le dán seanaimseartha roghnach', 38, ['(ii) Cén mothúchán is mó', '(iii) Cén teicníc fhileata'],
              [], ['Eolas = 13 mharc', 'Eolas = 5 mharc', 'Eolas = 7 marc'], [(MARC4_TABLE, 39, 1), (MARC3_TABLE, 39, 2)])]
    for slug, atlas, pages, start, page, cuts, inside, caps, after in poems:
        whole, spages = literature_answer(s, start, page)
        pieces = split_parts(whole, cuts, caps)
        for table, home in inside:
            pieces = move(pieces, table, home)
        for table, tpage, home in after:
            # Stored after the marking-panel note at the foot of the answer: it prices the sub-question named.
            at = s.text.index(table, s.page(tpage))
            assert at < s.page(tpage + 1), (slug, table)
            pieces[home] = clean(pieces[home] + ' ' + table)
            spages = sorted(set(spages) | {tpage})
        assert PLE_TABLE.search(pieces[0]) and not PLE_TABLE.search(pieces[1]) and not PLE_TABLE.search(pieces[2]), slug
        assert MARC4_TABLE in pieces[1] and MARC4_TABLE not in pieces[0] + pieces[2], slug
        card = by_id[f'irish-2021-hl-p2-{slug}']
        stamp(card['id'], atlas, pages, sorted(set(spages)),
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
        chunk, spages = s.chunk(start, end, s.page(40))
        # 4A's text carries the section's shared Eolas/Gaeilge band table: it is the section's, given to every option.
        chunk = clean(chunk.replace(m['table35'], ' '))
        assert 'Eolas = 35 marc' in chunk and 'Gaeilge (5 mharc)' not in chunk, slug
        card = by_id[f'irish-2021-hl-p2-{slug}']
        stamp(card['id'], atlas, [12], sorted(set(spages) | {40}),
              [criterion('eolas', 'Eolas', 35, [chunk, m['general4'], m['table35']], 'indicative'), gaeilge(m)],
              'One complete SEC response: Eolas 35 assessed as a unit with a single shared 5-mark Gaeilge award. Supporting notes are indicative rather than exhaustive.',
              lit_requirements)
    whole, spages = literature_answer(s, '4F. Dánta Breise', 46)
    pieces = split_parts(whole, ['(ii) A bhfuil i gceist leis na línte seo a mhíniú', '(iii) Cén t-atmaisféar'],
                         ['Eolas = 19 marc', 'Míniú = 7 marc', 'Eolas = 9 marc'])
    assert EOLAS17_TABLE.search(pieces[0])
    for table, home in [(MARC7_TABLE, 1), (MARC54_TABLE, 2)]:
        at = s.text.index(table, s.page(48))
        assert at < s.page(49), table
        pieces[home] = clean(pieces[home] + ' ' + table)
    stamp('irish-2021-hl-p2-literature-4-f', 'X-4F', [12, 13], sorted(set(spages) | {48}),
          [criterion('eolas-i', '(i) Eolas', 19, [pieces[0], m['general4']], 'indicative'), criterion('eolas-ii', '(ii) Eolas', 7, [pieces[1]], 'indicative'),
           criterion('eolas-iii', '(iii) Eolas', 9, [pieces[2]], 'indicative'), gaeilge(m)],
          'One complete SEC response: the paper prints (i) 20, (ii) 10 and (iii) 10; the scheme assesses Eolas 19, 7 and 9 (5 + 4 for the two points) '
          'plus one shared 5-mark Gaeilge award. Supporting notes are indicative rather than exhaustive.', lit_requirements)
    assert len(stamped) == 26
    for card_id in stamped:
        for c in by_id[card_id]['criteria']:
            assert c['guidance'] and all(not re.search('[-]', g) for g in c['guidance']), (card_id, c['id'])
            assert all(h not in g for h in FURNITURE for g in c['guidance']), (card_id, c['id'])
    return cards, stamped


def build():
    m = material()
    cards = []

    def add(key, slug, ref, prompt, topic, pages, scheme_pages, criteria, note, extra_topics=None, title=None, focus=None):
        cards.append(dict(
            id=f'irish-2021-hl-p2-{slug}', year=2021, level='higher', paper=2, section='2',
            atlasQuestionId=key, questionRef=f'2021 HL Paper 2 {ref}', questionText=prompt,
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
    assert len(cards) == 48 and len({c['id'] for c in cards}) == 48
    for card in cards:
        for c in card['criteria']:
            assert c['guidance'] and all(not re.search('[-]', g) for g in c['guidance']), (card['id'], c['id'])
    sr = json.loads(SOURCE_REVIEW.read_text())
    legacy = ([f'irish-2021-hl-p2-reading-{l}-q{q}' for l in 'ab' for q in range(1, 7)]
              + [f'irish-2021-hl-p2-prose-{k}' for k in ['2a-a', '2a-b', '2b-a', '2b-b']]
              + [f'irish-2021-hl-p2-poetry-{k}' for k in ['3a-a', '3a-b', '3b-a', '3b-b']]
              + [f'irish-2021-hl-p2-literature-4-{k}' for k in 'abcdef'])
    review = dict(year=2021, level='higher', paperFileid=FILE + '.pdf', schemeFileid=SCHEME_FILE + '.pdf',
                  paperSha256=PAPER_SHA, schemeSha256=SCHEME_SHA,
                  reviewedPaperPages=list(range(1, 17)), reviewedSchemePages=sr['reviewedSchemePages'], schemeScope=sr['schemeScope'],
                  reviewDate=REVIEWED_AT, status='reviewed', fullPaperAndApplicableSchemeVisualSweep=True, selectionDecisions=m['decisions'],
                  readingPracticeCardIds=[c['id'] for c in cards], legacyCardIds=legacy, readingWholeCardIds=legacy[:12],
                  examStructure=dict(readingA=50, readingB=50, prose=30, poetry=30, additionalLiterature=40, total=120),
                  nonPoolDecisions=sr['nonPoolDecisions'], openIssues=[], caveats=sr['sourceFindings'],
                  boundaries='12 retained whole reading questions with 34 published parts, 12 independent one-mark answer slots and 2 six-mark trait slots; '
                             '4 retained prose, 4 poetry and 6 additional-literature routes.')
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
    print(f"Irish Higher 2021 Paper 2: {len(data['cards'])} added reading cards (+26 retained legacy cards); the archive remains incomplete.")


if __name__ == '__main__':
    main()
