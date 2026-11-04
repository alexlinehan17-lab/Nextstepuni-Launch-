#!/usr/bin/env python3
"""Reviewed 2020 Higher Paper 2 (Léamhthuiscint agus Litríocht): new cards, no legacy component.

Paper PDF 1–12 (page 3 the Treoracha, 4–7 the two reading passages with their questions,
8 prose, 9 poetry, 10–11 additional literature, 12 blank) and the Paper 2 pages of the
combined LC001ALP000IV scheme (PDF 17–41, plus 42 modified marking) reviewed on
2026-11-04. Counts are assertions, not corpus-completeness proof.

The card shapes follow the reviewed 2021–2026 Higher Paper 2 components: every printed
reading question is a whole card with one criterion per published part, each published
part is also a practice card, two independent one-mark answers expose their own slots,
order-dependent 2 + 1 items stay whole, and the two 6-mark halves of each 6(b) expose
their own slots. 2020 prints one prescribed and one optional prose text (2A Hurlamaboc,
2B the optional novel extract), one prescribed and one optional poem (3A Mo ghrá-sa
(idir lúibíní), 3B a modern optional poem) and six Q4 options; each is one card with
its printed sub-questions as criteria and one shared 5-mark Gaeilge award.

2020's scheme layout is the 2021 one (irish_higher_2021_p2.py): reading starts on PDF 17
with the marking instructions; the prose and Q4 band tables print the Eolas and Gaeilge
columns side by side; each literature answer closes with the examiner's marking-panel
note ("Nóta: Caithfidh an Scrúdaitheoir …"), after which the text layer stores the
Marc as 4 table of the sub-question above; the boxed headings are removed by exact match.
Léamhthuiscint A 6(b) prices two aims and B 6(b) two reasons, each 6 (named 2 + supported 4).
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
OUT = ROOT / 'components/MarkBank/cards/irish/higher-2020-p2-authored.json'
SOURCE_REVIEW = ROOT / 'scripts/markbank/authored/irish-higher-2020-p2-source-review.json'
REVIEWED_AT = '2026-11-04'
PAPER_SHA = 'dbfa52390ed43c0a2c246608581641cb3d2d488ced8eef391e9eaf3f7ebfdeb0'
SCHEME_SHA = '1ff42c9a919d800be993fff761c719f4376fa2825e9401b50b31e69d3636bf82'
DIRECTIVE = re.compile(r'rogha|roghna|Freagair|Luaigh|Ainmnigh|\bnó\b|dhá phointe|dhá rud|dhá bh|dhá dh|dhá ch|dhá fh|dhá th|'
                       r'ceann amháin|pointe amháin|\bdhá\b|an dá\b|amháin', re.I)
SOURCE_NOTE = 'Shown page-for-page from the official examination paper; swipe to move between pages.'
# Boxed page headings the 2020 text layer stores inside the literature pages; exact strings only.
FURNITURE = ('Ceist 2 PRÓS (30 marc)', 'Ceist 3 FILÍOCHT (30 marc)', 'Ceist 4 LITRÍOCHT BHREISE (40 marc)',
             '– PRÓS AINMNITHE nó PRÓS ROGHNACH – (30 marc)', '– FILÍOCHT AINMNITHE nó FILÍOCHT ROGHNACH – (30 marc)')
# The examiner's marking-panel note that closes each literature answer: the boundary of the answer's own text.
PANEL = 'Nóta: Caithfidh an Scrúdaitheoir'
GAEILGE_TABLE = re.compile(r'Gaeilge \(5 mharc\) Sárchumas.*?Cumas lag/an-lag maidir leis na príomhghnéithe de cheart na teanga \(gramadach, comhréir, struchtúr, deilbhíocht\) 1')
PLE_TABLE = re.compile(r'Catagóir Plé \(11 mharc\) Marcanna .*?Lag/An-lag Eolas an-bhearnach, an-mhíchruinn agus an-lochtach 0-3')
EOLAS19_TABLE = re.compile(r'Catagóir Eolas \(19 marc\) Sármhaith .*?Lag/An-lag Eolas an-bhearnach, an-mhíchruinn agus an-lochtach 0-7')
MARC4_TABLE = 'Catagóir Marc as 4 Sármhaith 4 An-mhaith 3 Maith 2 Measartha 1 Lag/An-lag 0'
MARC7_TABLE = 'Catagóir Marc as 7 Sármhaith 6-7 An-mhaith 5 Maith 4 Measartha 3 Lag/An-lag 0-2'


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


def printed_values(chunk, marks):
    # "… faoi leith (2 mharc) in imeacht tréimhse áirithe ama (1 mharc) = 3 mharc" (A 1(a)): an answer's printed split.
    values = re.findall(r'= (\d+) mh?arc', chunk) + re.findall(r'bronntar (\d+) mh?arc', chunk) + re.findall(r'\((\d+) mh?arc\)', chunk)
    return sorted({0, marks} | {int(v) for v in values if int(v) <= marks})


def material():
    import fitz
    paper_path = ROOT / f'paper-trail-corpus/exampapers/2020/{FILE}.pdf'
    scheme_path = ROOT / f'paper-trail-corpus/markingschemes/2020/{SCHEME_FILE}.pdf'
    assert hashlib.sha256(paper_path.read_bytes()).hexdigest() == PAPER_SHA, 'Paper changed: repeat visual review'
    assert hashlib.sha256(scheme_path.read_bytes()).hexdigest() == SCHEME_SHA, 'Scheme changed: repeat visual review'
    paper, doc = fitz.open(paper_path), fitz.open(scheme_path)
    texts = [clean(p.get_text()) for p in paper]
    s = Scheme(doc, 17, 41)
    # The marking instructions, from their first rule (their heading "Treoracha do mharcáil na Léamhthuisceana:" is a title)
    # to the boxed section heading that the text layer stores after them.
    general = s.chunk('Tá Ceist 1 – 5 ar cómharc', 'Páipéar II (200 marc)')[0]
    assert general.endswith('sa fhreagarleabhar.'), general[-60:]
    # (q, part, paper prompt, scheme anchor, marks, mode, printed tariff). Each passage ends where the examiner's
    # marking panel for 6(b) begins ("A1 (2) + S1 (4) = …", "C1 (2) + P1 (4) = …").
    passages = {
        'A': dict(title='An tAthrú Aeráide', pages=[4, 5], topic='irish-3-0', end='A1 (2) + S1 (4) = A2 (2) + S2 (4) =', parts=[
            ('1', 'a', '(a) Cad atá i gceist leis an téarma ‘athrú aeráide’, dar leis na heolaithe aeráide? (Alt 1)', '1. (a) Cad atá i gceist leis an téarma', 3, None, '{3 mharc}'),
            ('1', 'bi', '(b) (i) Cad iad na hathruithe atá le tabhairt faoi deara ar na patrúin aimsire sa samhradh in Éirinn anois? (Alt 1)', '(b) (i) Cad iad na hathruithe', 2, 'slots', '{2 mharc: 1 mharc + 1 mharc}'),
            ('1', 'bii', '(ii) Cén chúis atá leis an athrú aeráide, dar le formhór na n-eolaithe aeráide? (Alt 1)', '(ii) Cén chúis atá leis an athrú aeráide', 2, None, '{2 mharc}'),
            ('2', 'a', '(a) Cén chúis a bhí leis an athrú aeráide sa sean-am agus cén chúis atá leis an athrú aeráide sa lá atá inniu ann? (Alt 2)', '2. (a) Cén chúis a bhí leis', 3, 'ordered', '{3 mharc: 2 mharc + 1 mharc}'),
            ('2', 'bi', '(b) (i) Cad a tharlaíonn nuair a dhóitear breoslaí iontaise mar fhoinse fuinnimh? (Alt 2)', '(b) (i) Cad a tharlaíonn nuair', 2, None, '{2 mharc}'),
            ('2', 'bii', '(ii) Luaigh dhá fháth a bhfuil cúrsaí iompair ag cur leis an athrú aeráide. (Alt 2)', '(ii) Luaigh dhá fháth', 2, 'slots', '{2 mharc: 1 mharc + 1 mharc}'),
            ('3', 'a', '(a) Conas a chabhraíonn na foraoisí, go háirithe na foraoisí trópaiceacha, leis an bpláinéad a fhuarú? (Alt 3)', '3. (a) Conas a chabhraíonn', 3, None, '{3 mharc}'),
            ('3', 'bi', '(b) (i) Cén tionchar a bhíonn ag leagan na gcrann ar an atmaisféar? (Alt 3)', '(b) (i) Cén tionchar a bhíonn', 2, None, '{2 mharc}'),
            ('3', 'bii', '(ii) Scríobh síos an dá rud a astaíonn ocsaíd nítriúil agus meatán i gcúrsaí talmhaíochta. (Alt 3)', '(ii) Scríobh síos an dá rud a astaíonn', 2, 'slots', '{2 mharc: 1 mharc + 1 mharc}'),
            ('4', 'a', '(a) Luaigh dhá rud a dúirt Greta Thunberg le seasca ceannaire domhanda ag Cruinniú Mullaigh na Náisiún Aontaithe faoin athrú aeráide. (Alt 4)', '4. (a) Luaigh dhá rud a dúirt Greta', 3, 'ordered', '{3 mharc: 2 mharc + 1 mharc}'),
            ('4', 'bi', '(b) (i) Cén fáth a raibh an t-aos óg ag léirsiú i dtíortha éagsúla ar fud an domhain ar an 20 Meán Fómhair 2019? (Alt 4)', '(b) (i) Cén fáth a raibh an t-aos óg', 2, None, '{2 mharc}'),
            ('4', 'bii', '(ii) Cén fáth ar mhol na toscairí óga ag Tionól Aeráide na nÓg go n-eagrófaí feachtas náisiúnta? (Alt 4)', '(ii) Cén fáth ar mhol na toscairí', 2, None, '{2 mharc}'),
            ('5', 'a', '(a) Scríobh síos an dá sprioc atá leagtha amach i bPlean Gnímh an Rialtais don Aeráid a seoladh i mí an Mheithimh 2019. (Alt 5)', '5. (a) Scríobh síos an dá sprioc', 3, 'ordered', '{3 mharc: 2 mharc + 1 mharc}'),
            ('5', 'bi', '(b) (i) Cén beartas atá sa phlean maidir le foinsí fuinnimh an leictreachais agus an teasa? (Alt 5)', '(b) (i) Cén beartas atá sa phlean', 2, None, '{2 mharc}'),
            ('5', 'bii', '(ii) Scríobh síos dhá rud atá luaite sa phlean maidir le cúrsaí taistil. (Alt 5)', '(ii) Scríobh síos dhá rud atá luaite', 2, 'slots', '{2 mharc: 1 mharc + 1 mharc}'),
            ('6', 'a', '(a) Aimsigh sampla de bhreischéim na haidiachta in Alt 1 agus sampla den bhriathar saor san Aimsir Fháistineach in Alt 5.', '6. (a) Aimsigh sampla de bhreischéim', 3, 'grammar', '{3 mharc: 2 mharc + 1 mharc}'),
            ('6', 'b', '(b) Bunaithe ar an eolas sa sliocht thuas, déan plé, i d’fhocail féin, ar dhá aidhm a bhí ag an údar, dar leat, nuair a scríobh sé an sliocht seo. Bíodh tagairt amháin ón sliocht agat, i d’fhocail féin, ag tacú le gach aidhm a luann tú i do fhreagra. (Is leor 60 focal.)', '(b) Bunaithe ar an eolas sa sliocht thuas, déan plé, i d’fhocail féin, ar dhá aidhm', 12, 'aims', '{6 mharc + 6 mharc}')]),
        'B': dict(title='An Ghaeilge agus Saol na Gaeilge', pages=[6, 7], topic='irish-3-1', end='C1 (2) + P1 (4) = C2 (2) + P2 (4) =', parts=[
            ('1', 'a', '(a) Cén fáth ar bunaíodh an eagraíocht trasteorann, Foras na Gaeilge, i mí na Nollag 1999? (Alt 1)', '1. (a) Cén fáth ar bunaíodh', 3, None, '{3 mharc}'),
            ('1', 'bi', '(b) (i) Cén bhaint atá ag Foras na Gaeilge le ról na sé cheanneagraíocht Ghaeilge? (Alt 1)', '(b) (i) Cén bhaint atá ag Foras', 2, None, '{2 mharc}'),
            ('1', 'bii', '(ii) Scríobh síos an dá chúis a gcuireann Foras na Gaeilge scéimeanna scríbhneoireachta ar fáil. (Alt 1)', '(ii) Scríobh síos an dá chúis a gcuireann', 2, 'slots', '{2 mharc: 1 mharc + 1 mharc}'),
            ('2', 'a', '(a) Cad a bhíonn i gceist nuair a aithnítear teanga a bheith ag forbairt sa ré dhigiteach? (Alt 2)', '2. (a) Cad a bhíonn i gceist', 3, None, '{3 mharc}'),
            ('2', 'bi', '(b) (i) Cén fáth a ndeirtear gur áiseanna tábhachtacha iad na foclóirí atá ar fáil ar líne? (Alt 2)', '(b) (i) Cén fáth a ndeirtear gur áiseanna', 2, None, '{2 mharc}'),
            ('2', 'bii', '(ii) Luaigh dhá rud a bhíonn ar fáil ar an suíomh peig.ie. (Alt 2)', '(ii) Luaigh dhá rud a bhíonn ar fáil', 2, 'slots', '{2 mharc: 1 mharc + 1 mharc}'),
            ('3', 'a', '(a) Tabhair dhá chúis a raibh tábhacht ar leith ag baint le bunú Chomórtas Peile na Gaeltachta caoga bliain ó shin. (Alt 3)', '3. (a) Tabhair dhá chúis a raibh tábhacht', 3, 'ordered', '{3 mharc: 2 mharc + 1 mharc}'),
            ('3', 'bi', '(b) (i) Scríobh síos dhá phointe eolais faoin turas a rinne grúpa d’fhir óga as Corca Dhuibhne go Gaeltacht Thír Chonaill ar an 4 Eanáir 1969. (Alt 3)', '(b) (i) Scríobh síos dhá phointe eolais faoin turas', 2, 'slots', '{2 mharc: 1 mharc + 1 mharc}'),
            ('3', 'bii', '(ii) Cén fáth a bhfuil Comórtas Peile na Gaeltachta ina fhéile thábhachtach sa lá atá inniu ann? (Alt 3)', '(ii) Cén fáth a bhfuil Comórtas Peile', 2, None, '{2 mharc}'),
            ('4', 'a', '(a) Luaigh an dá chúis ar bronnadh ‘Gradam Saoil’ ar an amhránaí, Máire Ní Bhraonáin, ag na RTÉ Folk Awards anuraidh. (Alt 4)', '4. (a) Luaigh an dá chúis ar bronnadh', 3, 'ordered', '{3 mharc: 2 mharc + 1 mharc}'),
            ('4', 'bi', '(b) (i) Scríobh síos dhá rud a tharla don ghrúpa Clannad de thairbhe an amhráin ‘Theme from Harry’s Game’. (Alt 4)', '(b) (i) Scríobh síos dhá rud a tharla', 2, 'slots', '{2 mharc: 1 mharc + 1 mharc}'),
            ('4', 'bii', '(ii) Cad a léiríonn comhartha aitheantais UNESCO faoi Chruitireacht na hÉireann? (Alt 4)', '(ii) Cad a léiríonn comhartha', 2, None, '{2 mharc}'),
            ('5', 'a', '(a) Cén aidhm atá ag an tionscadal dúchas.ie? (Alt 5)', '5. (a) Cén aidhm atá ag an tionscadal', 3, None, '{3 mharc}'),
            ('5', 'bi', '(b) (i) Cén deis a thugann an Pop Up Gaeltacht do dhaoine? (Alt 5)', '(b) (i) Cén deis a thugann an Pop Up', 2, None, '{2 mharc}'),
            ('5', 'bii', '(ii) Scríobh síos dhá thoradh fhadtéarmacha a bhfuiltear ag súil leo ón bhfiontar gteic. (Alt 5)', '(ii) Scríobh síos dhá thoradh', 2, 'slots', '{2 mharc: 1 mharc + 1 mharc}'),
            ('6', 'a', '(a) Aimsigh sampla d’ainmfhocal sa tuiseal ginideach iolra in Alt 2 agus sampla den bhriathar saor san Aimsir Láithreach in Alt 5.', '6. (a) Aimsigh sampla d’ainmfhocal', 3, 'grammar', '{3 mharc: 2 mharc + 1 mharc}'),
            ('6', 'b', '(b) Bunaithe ar an eolas sa sliocht thuas, déan plé, i d’fhocail féin, ar dhá chúis ar scríobh an t-údar an sliocht seo, dar leat. Bíodh tagairt amháin ón sliocht agat, i d’fhocail féin, ag tacú le gach cúis a luann tú i do fhreagra. (Is leor 60 focal.)', '(b) Bunaithe ar an eolas sa sliocht thuas, déan plé, i d’fhocail féin, ar dhá chúis', 12, 'reasons', 'Dhá chúis = 6 mharc + 6 mharc')]),
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
            assert 'Ag bun Léamhthuiscint' not in chunk and 'Páipéar II' not in chunk, (letter, q, part)
            resolved.append((q, part, prompt, anchor, marks, mode, chunk, spages))
        passage['resolved'] = resolved
    assert sum(len(p['resolved']) for p in passages.values()) == 34
    note5 = s.chunk('Nóta: I gcás na gceisteanna 2 (Prós)', 'Nóta: Níl na nótaí tacaíochta seo uileghabhálach')[0]
    notes = s.chunk('Nóta: Níl na nótaí tacaíochta seo uileghabhálach', 'Freagair Ceist 2A (Prós Ainmnithe)')[0]
    gaeilge_table = GAEILGE_TABLE.search(s.text, s.page(31)).group(0)
    # The prose and additional-literature band tables print the Eolas and Gaeilge columns side by side.
    prose_table = s.chunk('Catagóir Eolas (25 marc) Gaeilge (5 mharc)', 'Ceist 2 PRÓS (30 marc)')[0]
    table35 = s.chunk('Catagóir Eolas (35 marc) Gaeilge (5 mharc)', 'Ceist 4 LITRÍOCHT BHREISE (40 marc)')[0]
    general4 = s.chunk('Treoracha: Iarrtar ar na hiarrthóirí plé a dhéanamh ar an ráiteas', 'Eolas (35) = Gaeilge (5) = C4 (40) =', s.page(33))[0]
    assert all(x in gaeilge_table for x in ['Sárchumas', 'Cumas lag/an-lag']) and '22-25' in prose_table and '0-9' in prose_table
    assert '30-35' in table35 and '0-13' in table35 and general4.endswith('sa fhreagarleabhar.')
    assert note5.endswith('ar Ghaeilge.') and notes.endswith('atá iontu.')
    return dict(paper=paper, texts=texts, s=s, general=general, passages=passages, note5=note5, notes=notes,
                gaeilge_table=gaeilge_table, prose_table=prose_table, table35=table35, general4=general4,
                decisions=selection_decisions(paper))


READING_REQUIREMENTS = ['Léigh an sliocht iomlán a ghabhann leis an gceist. Freagair an chuid atá luaite ar an gcárta.',
                        'Úsáid an t-alt a luaitear. Glacfar le focail an tsleachta nó le do chuid focal féin, ach ní mór 6(b) a fhreagairt i d’fhocail féin.']
WHOLE_REQUIREMENTS = ['Léigh an sliocht oifigiúil a ghabhann leis an gceist.', 'Freagair gach fochuid agus cloígh leis an alt a luaitear.',
                      'Bain úsáid as do chuid focal féin nuair a iarrtar ort é.']
LIT_REQUIREMENTS = ['Freagair gach cuid den cheist atá priontáilte.', 'Úsáid tagairtí cruinne agus ábhartha don téacs.']
PART_NOTE = ('SEC allocation for this task. Alternative correct answers in the scheme are answers to one task, not extra task routes. '
             'Whole questions and their practice parts are overlapping exercises; their marks are not added to infer the paper total.')
LABELS = {'a': '(a) Freagra', 'bi': '(b)(i) Freagra', 'bii': '(b)(ii) Freagra', 'grammar': '(a) Freagra',
          'aim-1': '(b) Aidhm 1', 'aim-2': '(b) Aidhm 2', 'reason-1': '(b) Cúis 1', 'reason-2': '(b) Cúis 2'}
# The two 6-mark halves of 6(b): (criterion id prefix, label, English practice focus).
HALVES = {'aims': ('aim', 'Aidhm', 'One of the two aims of the writer, discussed with one reference from the extract in your own words (aim {slot}, 6 marks)'),
          'reasons': ('reason', 'Cúis', 'One of the two reasons the writer wrote the extract, discussed with one reference from it in your own words (reason {slot}, 6 marks)')}


def part_criteria(part, marks, mode, chunk, general):
    if mode in HALVES:
        key, label, _ = HALVES[mode]
        return [criterion(f'{key}-1', f'{label} 1', 6, [chunk, general]), criterion(f'{key}-2', f'{label} 2', 6, [chunk, general])]
    if mode in ('ordered', 'grammar'):
        return [criterion('grammar' if mode == 'grammar' else part, 'Freagra', marks, [chunk, general], permitted=[0, 2, 3])]
    if mode == 'slots':
        # "{2 mharc: 1 mharc + 1 mharc}": either answer alone earns 1, even where the accepted list prints no per-answer marks.
        return [criterion(part, 'Freagra', marks, [chunk, general], permitted=[0, 1, 2])]
    return [criterion(part, 'Freagra', marks, [chunk, general], permitted=printed_values(chunk, marks))]


def literature_answer(s, start, page, table=None):
    """One literature answer: from its printed start to the examiner's marking-panel note, the band tables removed."""
    whole, spages = s.chunk(start, PANEL, s.page(page))
    whole = GAEILGE_TABLE.sub(' ', whole.replace(table, ' ') if table else whole).strip()
    assert 'Gaeilge (5 mharc)' not in whole and 'Eolas (25) =' not in whole and 'Eolas (35) =' not in whole, start
    return clean(whole), spages


def split_parts(whole, cuts, caps):
    i2 = whole.index(cuts[0]); i3 = whole.index(cuts[1], i2)
    pieces = [whole[:i2].strip(), whole[i2:i3].strip(), whole[i3:].strip()]
    for piece, cap in zip(pieces, caps):
        assert cap in piece, cap
    return pieces


def after_panel(s, table, page):
    """A band table the text layer stores after the marking-panel note at the foot of the answer on `page`."""
    at = s.text.index(table, s.text.index(PANEL, s.page(page)))
    end = s.text.find(f'⟦{page + 1}⟧')
    assert at < (end if end > 0 else len(s.text)), table
    return table


def build():
    m = material()
    texts, s = m['texts'], m['s']
    cards = []

    def add(key, slug, ref, prompt, topic, pages, scheme_pages, criteria, requirements, note, extra_topics=None, source=None, **extra):
        cards.append(dict(
            id=f'irish-2020-hl-p2-{slug}', year=2020, level='higher', paper=2, section='2',
            atlasQuestionId=key, questionRef=f'2020 HL Paper 2 {ref}', questionText=prompt,
            totalMarks=sum(c['maxMarks'] for c in criteria), topicId=topic,
            **({'additionalTopicIds': extra_topics} if extra_topics else {}),
            conceptId=f'irish-hl-p2-{slug}', paperFileid=FILE, schemeFileid=SCHEME_FILE,
            schemePage=scheme_pages[0], schemePages=scheme_pages, reviewedAt=REVIEWED_AT, reviewedPaperPages=pages,
            taskRequirements=requirements, criteria=criteria, markingGuideNote=note,
            sourceMaterial=dict(kind='source-text', label=source[0] if source else ref, title=source[1] if source else ref,
                                pages=source[2] if source else pages, attribution='© State Examinations Commission.',
                                presentationNote=SOURCE_NOTE),
            **extra))
        return cards[-1]

    # ---- Ceist 1: Léamhthuiscint A agus B (100) ---------------------------------------
    six_b = {'A': '6(b) prices two aims, 6 marks each (naming the aim 2 + its support from the passage 4), in the candidate’s own words.',
             'B': '6(b) prices two reasons, 6 marks each (naming the reason 2 + its discussion with a reference from the passage 4), in the candidate’s own words.'}
    for letter, passage in m['passages'].items():
        topic = passage['topic']
        source = (f'Léamhthuiscint {letter}', passage['title'], passage['pages'])
        by_question = {}
        for q, part, prompt, anchor, marks, mode, chunk, spages in passage['resolved']:
            label = f'{q}({part[0]})' + (f'({part[1:]})' if len(part) > 1 else '')
            text = f'{label} ' + re.sub(r'^(\([a-z]+\)\s*)+', '', prompt)
            here = 'irish-3-3' if mode == 'grammar' else topic
            card = add(f'R-{letter}-{q}-{part}', f'reading-{letter.lower()}-q{q}-{part}', f'Léamhthuiscint {letter} · Ceist {label}', text, here,
                       passage['pages'], spages, part_criteria(part, marks, mode, chunk, m['general']), READING_REQUIREMENTS, PART_NOTE,
                       [topic] if mode == 'grammar' else None, source)
            by_question.setdefault(q, []).append((part, prompt, card))
            if mode == 'slots':
                for slot in (1, 2):
                    add(f'R-{letter}-{q}-{part}-{slot}', f'reading-{letter.lower()}-q{q}-{part}-{slot}', f'Léamhthuiscint {letter} · Ceist {label} · Freagra {slot}',
                        text, topic, passage['pages'], spages, [criterion(f'{part}-{slot}', f'Freagra {slot}', 1, [chunk, m['general']])],
                        READING_REQUIREMENTS, 'The scheme prices the two answers 1 mharc + 1 mharc independently; this card practises one of them. ' + PART_NOTE,
                        None, source, practiceFocus=f'One of the two answers (answer {slot}, 1 mark)')
            if mode in HALVES:
                key, half, focus = HALVES[mode]
                for slot in (1, 2):
                    add(f'R-{letter}-{q}-{part}-{slot}', f'reading-{letter.lower()}-q{q}-{part}-{slot}', f'Léamhthuiscint {letter} · Ceist {label} · {half} {slot}',
                        text, topic, passage['pages'], spages, [criterion(f'{key}-{slot}', f'{half} {slot}', 6, [chunk, m['general']])],
                        READING_REQUIREMENTS, 'The scheme prices the two halves 6 + 6 independently (named 2 + supported 4); this card practises one of them. ' + PART_NOTE,
                        None, source, practiceFocus=focus.format(slot=slot))
        for q, parts in by_question.items():
            crits = [dict(c) for _, _, card in parts for c in card['criteria']]
            for c in crits:
                c['label'] = LABELS[c['id']]
            add(f'R-{letter}-{q}', f'reading-{letter.lower()}-q{q}', f'Léamhthuiscint {letter} · Ceist {q}',
                f'{q}. ' + ' '.join(p for _, p, _ in parts) + (' (7 marc)' if q != '6' else ' (15 mharc)'), topic, passage['pages'],
                sorted({p for _, _, c in parts for p in c['schemePages']}), crits, WHOLE_REQUIREMENTS,
                'Complete printed question. Score each published part separately using these SEC allocations.'
                + (' Two-answer grammar is one 0/2/3 placement; ' + six_b[letter] if q == '6' else ''),
                ['irish-3-3'] if q == '6' else None, source)
            assert cards[-1]['totalMarks'] == (15 if q == '6' else 7), (letter, q)
            assert in_order(f'({7 if q != "6" else 15} m', texts[passage['pages'][1] - 1]), (letter, q)

    # ---- Ceisteanna 2–4: An Litríocht -------------------------------------------------------
    gaeilge = lambda: criterion('gaeilge', 'Gaeilge', 5, [m['gaeilge_table'], m['note5']], 'quality')
    head2 = 'Freagair Ceist 2A (Prós Ainmnithe) nó Ceist 2B (Prós Roghnach) thíos.'
    head3 = 'Freagair Ceist 3A (Filíocht Ainmnithe) nó Ceist 3B (Filíocht Roghnach) thíos.'
    prose = [
        ('P-2A', 'prose-2a', 'Prós 2A · Hurlamaboc', 'irish-4-5', '2A. Prós Ainmnithe', 26,
         head2 + '\n2A. Prós Ainmnithe',
         'Freagair an cheist thíos faoin ngiota as an úrscéal Hurlamaboc.\n\nHurlamaboc\n'
         '“Bhí caithréim bainte amach ag Lisín agus a lán le ceiliúradh ag a clann, dar léi féin.”\nDéan plé ar an ráiteas sin. (30 marc)'),
        ('P-2B', 'prose-2b', 'Prós 2B · Úrscéal roghnach', 'irish-4-7', '2B. Prós Roghnach', 28,
         head2 + '\n2B. Prós Roghnach\nNíl cead aon ábhar a bhaineann le Prós Ainmnithe a úsáid i bhfreagra ar an bPrós Roghnach.',
         'Maidir leis an ngiota as an úrscéal roghnach a ndearna tú staidéar air le linn do chúrsa, ainmnigh an príomhcharachtar '
         '(an phríomhphearsa) sa ghiota. Déan plé ar an bpáirt atá ag an bpríomhcharachtar (ag an bpríomhphearsa) sin sa ghiota.\n\n'
         'Ní mór teideal an úrscéil sin, mar aon le hainm an údair, a scríobh síos go cruinn. (30 marc)'),
    ]
    assert s.chunk('Catagóir Eolas (25 marc) Gaeilge (5 mharc)', '⟦29⟧', s.page(28))[0] == m['prose_table'], 'PDF 28 prose table differs from PDF 26'
    for key, slug, ref, topic, start, page, stem, prompt in prose:
        for line in [*stem.splitlines(), *prompt.splitlines()]:
            if line:
                assert in_order(line, texts[7]), (key, line)
        # 2A's band table is stored inside its answer (PDF 26); 2B's identical copy follows its marking-panel note (PDF 28).
        chunk, spages = literature_answer(s, start, page, m['prose_table'])
        assert 'Eolas = 25 marc' in chunk and 'Catagóir Eolas (25 marc)' not in chunk, key
        add(key, slug, ref, prompt, topic, [8], sorted(set(spages) | {26}),
            [criterion('eolas', 'Eolas', 25, [chunk, m['prose_table'], m['notes']], 'indicative'), gaeilge()], LIT_REQUIREMENTS,
            'One complete SEC response: 25 Eolas and a single shared 5-mark Gaeilge award. Supporting notes are indicative rather than exhaustive. '
            'The printed band table gives the Eolas and Gaeilge columns side by side.',
            source=('Prós', ref.split(' · ', 1)[1], [8]), stem=stem)

    poems = [
        ('F-3A', 'poetry-3a', 'Filíocht 3A · Mo ghrá-sa (idir lúibíní)', 'irish-5-4', '3A. Filíocht Ainmnithe', 29, head3 + '\n3A. Filíocht Ainmnithe', [
            '(i) Cad é príomhthéama an dáin Mo ghrá-sa (idir lúibíní) (thíos), dar leat? Déan plé ar na híomhánna a úsáideann an file sa dán chun an príomhthéama sin a léiriú. (15 mharc)',
            '(ii) An teideal oiriúnach ar an dán é Mo ghrá-sa (idir lúibíní), dar leat? (Is leor pointe amháin eolais as an dán mar thacaíocht le do fhreagra.) (6 mharc)',
            '(iii) Cé a chum an dán seo? Scríobh nóta gairid ar shaol agus ar shaothar an fhile sin. (9 marc)'],
         ['(ii) An teideal oiriúnach', '(iii) Cé a chum an dán seo?'], 30),
        ('F-3B', 'poetry-3b', 'Filíocht 3B · Dán roghnach', 'irish-5-6', '3B. Filíocht Roghnach', 31,
         head3 + '\n3B. Filíocht Roghnach\nNíl cead aon ábhar a bhaineann le Filíocht Ainmnithe a úsáid i bhfreagra ar an bhFilíocht Roghnach.', [
            '(i) Maidir le dán nua-aimseartha roghnach a ndearna tú staidéar air le linn do chúrsa, scríobh síos príomhthéama an dáin, dar leat. Déan plé ar an léiriú a thugtar ar an bpríomhthéama sin ó thús deireadh an dáin. (15 mharc)',
            '(ii) An bhfuil teideal an dáin oiriúnach do phríomhthéama an dáin, dar leat? (Is leor pointe amháin eolais as an dán mar thacaíocht le do fhreagra.) (6 mharc)',
            '(iii) Cé a chum an dán seo? Scríobh nóta gairid ar shaol agus ar shaothar an fhile sin. (9 marc)'],
         ['(ii) An bhfuil teideal an dáin', '(iii) Cé a chum an dán seo?'], None),
    ]
    for key, slug, ref, topic, start, page, stem, parts, cuts, marc4_page in poems:
        for line in [*stem.splitlines(), *parts]:
            assert in_order(line, texts[8]), (key, line[:40])
        whole, spages = literature_answer(s, start, page)
        pieces = split_parts(whole, cuts, ['Eolas = 13 mharc', 'Eolas = 5 mharc', 'Eolas = 7 marc'])
        # The Plé band table prices (i); the text layer stores it after (ii)'s conditions.
        found = PLE_TABLE.search(pieces[1])
        assert found and not PLE_TABLE.search(pieces[0]) and not PLE_TABLE.search(pieces[2]), key
        pieces[1] = clean(pieces[1][:found.start()] + ' ' + pieces[1][found.end():])
        pieces[0] = clean(pieces[0] + ' ' + found.group(0))
        if marc4_page:
            # 3A: the Marc as 4 table of (ii)'s point is stored after the marking-panel note at the foot of PDF 30.
            pieces[1] = clean(pieces[1] + ' ' + after_panel(s, MARC4_TABLE, marc4_page))
            spages = sorted(set(spages) | {marc4_page})
        assert MARC4_TABLE in pieces[1] and MARC4_TABLE not in pieces[0] + pieces[2], key
        add(key, slug, ref, '\n'.join(parts), topic, [9], sorted(set(spages)),
            [criterion('eolas-i', '(i) Eolas', 13, [pieces[0]], 'indicative'), criterion('eolas-ii', '(ii) Eolas', 5, [pieces[1]], 'indicative'),
             criterion('eolas-iii', '(iii) Eolas', 7, [pieces[2]], 'indicative'), gaeilge()], LIT_REQUIREMENTS,
            'One complete SEC response with one shared five-mark Gaeilge award. The paper prints (i) 15, (ii) 6 and (iii) 9; the scheme assesses '
            'Eolas 13, 5 and 7 with the conditions shown, plus Gaeilge 5 once. Supporting notes are indicative rather than exhaustive.',
            source=('Filíocht', ref.split(' · ', 1)[1], [9]), stem=stem)

    head4 = 'Freagair do rogha ceann amháin as Ceist 4 (A, B, C, D, E nó F) thíos.'
    options = [
        ('X-4A', 'literature-4-a', '4A. An Triail', 'irish-6-0', '4A. An Triail', '4B. A Thig Ná Tit Orm',
         '4A. An Triail\n“Cé a deir gur tír Chríostaí í seo?” arsa Seáinín an Mhótair agus é ag tagairt do chás an chailín óig, Máire Ní Chathasaigh sa dráma An Triail.\nDéan plé ar an ráiteas sin. (40 marc)'),
        ('X-4B', 'literature-4-b', '4B. A Thig Ná Tit Orm', 'irish-6-1', '4B. A Thig Ná Tit Orm', '4C. Tóraíocht Dhiarmada',
         '4B. A Thig Ná Tit Orm\n“Sa dírbheathaisnéis A Thig Ná Tit Orm, tugann Maidhc Dainín cuntas spéisiúil dúinn ar chúrsaí scolaíochta agus ar chúrsaí caitheamh aimsire agus é ag fás aníos sa Ghaeltacht.”\nDéan plé ar an ráiteas sin. (40 marc)'),
        ('X-4C', 'literature-4-c', '4C. Tóraíocht Dhiarmada agus Ghráinne', 'irish-6-2', '4C. Tóraíocht Dhiarmada', '4D. Gafa',
         '4C. Tóraíocht Dhiarmada agus Ghráinne\n“Tugtar léiriú éifeachtach dúinn ar thréithe Ghráinne agus ar an bpáirt atá aici sa Tóraíocht.”\nDéan plé ar an ráiteas sin. (40 marc)'),
        ('X-4D', 'literature-4-d', '4D. Gafa', 'irish-6-3', '4D. Gafa', '4E. Canary Wharf',
         '4D. Gafa\n“Is léir nach spéis le Breandán cruachás a mhic, Eoin, ná todhchaí a phósta le hEithne sa sliocht as an úrscéal Gafa.”\nDéan plé ar an ráiteas sin. (40 marc)'),
        ('X-4E', 'literature-4-e', '4E. Canary Wharf', 'irish-6-4', '4E. Canary Wharf', '4F. Dánta Breise',
         '4E. Canary Wharf\n“Sa scéal Cúrsa Eitilte, tugtar léiriú éifeachtach dúinn ar na deacrachtaí a bhí ag Theo agus an t-ádh a bhí air ag deireadh an scéil.”\nDéan plé ar an ráiteas sin. (40 marc)'),
    ]
    for key, slug, ref, topic, start, end, prompt in options:
        assert all(in_order(line, texts[9]) for line in prompt.splitlines()), key
        chunk, spages = s.chunk(start, end, s.page(34))
        assert 'Eolas = 35 marc' in chunk and 'Gaeilge (5 mharc)' not in chunk and 'Catagóir Eolas (35 marc)' not in chunk, key
        add(key, slug, f'Litríocht {ref}', head4 + '\n\n' + prompt, topic, [10], sorted(set(spages) | {33}),
            [criterion('eolas', 'Eolas', 35, [chunk, m['general4'], m['table35']], 'indicative'), gaeilge()], LIT_REQUIREMENTS,
            'One complete SEC response: Eolas 35 assessed as a unit with a single shared 5-mark Gaeilge award. Supporting notes are indicative rather than exhaustive.')
    whole, spages = literature_answer(s, '4F. Dánta Breise – Fill Arís', 39)
    pieces = split_parts(whole, ['(ii) A bhfuil i gceist leis na línte seo a mhíniú', '(iii) Cén mothúchán is mó'],
                         ['Eolas = 19 marc', 'Míniú = 7 marc', 'Eolas = 9 marc'])
    assert EOLAS19_TABLE.search(pieces[0])
    # The Marc as 7 table prices (ii)'s 7-mark explanation; the text layer stores it after (iii)'s tariffs.
    assert MARC7_TABLE in pieces[2] and MARC7_TABLE not in pieces[1]
    pieces[2] = clean(pieces[2].replace(MARC7_TABLE, ' '))
    pieces[1] = clean(pieces[1] + ' ' + MARC7_TABLE)
    # The Marc as 4 table of (iii)'s two points is stored after the marking-panel note at the foot of PDF 41.
    pieces[2] = clean(pieces[2] + ' ' + after_panel(s, MARC4_TABLE, 41))
    f_prompt = ('4F. Dánta Breise – Fill Arís\nFreagair (i), (ii) agus (iii) thíos.\n'
                '(i) Cén chomhairle a chuireann an file ar an léitheoir sa dán Fill Arís (thall), dar leat? Déan plé ar an léiriú a thugtar ar an gcomhairle sin ó thús deireadh an dáin. (20 marc)\n'
                '(ii) A bhfuil i gceist leis na línte seo a mhíniú:\nFill arís ar do chuid,\nNigh d’intinn is nigh\nDo theanga a chuaigh ceangailte i gcomhréiribh\nʼBhí bunoscionn le d’éirim: (10 marc)\n'
                '(iii) Cén mothúchán is mó a léiríonn an file sa dán seo, dar leat? Is leor dhá phointe eolais faoin mothúchán sin. Bíodh tagairtí cruinne agat do théacs an dáin i do fhreagra. (10 marc)')
    assert all(in_order(line, texts[9]) for line in f_prompt.splitlines())
    add('X-4F', 'literature-4-f', 'Litríocht 4F · Dánta Breise – Fill Arís', head4 + '\n\n' + f_prompt, 'irish-6-7', [10, 11],
        sorted(set(spages) | {33, 41}),
        [criterion('eolas-i', '(i) Eolas', 19, [pieces[0], m['general4']], 'indicative'), criterion('eolas-ii', '(ii) Eolas', 7, [pieces[1]], 'indicative'),
         criterion('eolas-iii', '(iii) Eolas', 9, [pieces[2]], 'indicative'), gaeilge()], LIT_REQUIREMENTS,
        'One complete SEC response: the paper prints (i) 20, (ii) 10 and (iii) 10; the scheme assesses Eolas 19, 7 and 9 (1 + 4 + 4 for the feeling and its two points) '
        'plus one shared 5-mark Gaeilge award. Supporting notes are indicative rather than exhaustive.',
        source=('Dánta Breise', 'Fill Arís', [10, 11]))

    reading = [c for c in cards if '-reading-' in c['id']]
    literature = [c for c in cards if '-reading-' not in c['id']]
    assert len(reading) == 68 and len(literature) == 10, (len(reading), len(literature))
    assert len({c['id'] for c in cards}) == len(cards) == 78 and len({c['atlasQuestionId'] for c in cards}) == 78
    assert sum(c['totalMarks'] for c in cards if re.fullmatch(r'R-[AB]-\d', c['atlasQuestionId'])) == 100
    for card in cards:
        assert sum(c['maxMarks'] for c in card['criteria']) == card['totalMarks'], card['id']
        for c in card['criteria']:
            assert c['guidance'] and all(not re.search('[-]', g) for g in c['guidance']), (card['id'], c['id'])
            assert all(h not in g for h in FURNITURE for g in c['guidance']), (card['id'], c['id'])
    sr = json.loads(SOURCE_REVIEW.read_text())
    whole = [c['id'] for c in reading if re.fullmatch(r'R-[AB]-\d', c['atlasQuestionId'])]
    review = dict(year=2020, level='higher', paperFileid=FILE + '.pdf', schemeFileid=SCHEME_FILE + '.pdf',
                  paperSha256=PAPER_SHA, schemeSha256=SCHEME_SHA,
                  reviewedPaperPages=list(range(1, 13)), reviewedSchemePages=sr['reviewedSchemePages'], schemeScope=sr['schemeScope'],
                  reviewDate=REVIEWED_AT, status='reviewed', fullPaperAndApplicableSchemeVisualSweep=True, selectionDecisions=m['decisions'],
                  readingWholeCardIds=whole, readingPracticeCardIds=[c['id'] for c in reading if c['id'] not in whole],
                  literatureRouteCardIds=[c['id'] for c in literature],
                  examStructure=dict(readingA=50, readingB=50, prose=30, poetry=30, additionalLiterature=40, total=200),
                  nonPoolDecisions=sr['nonPoolDecisions'], openIssues=[], caveats=sr['sourceFindings'],
                  boundaries='12 whole reading questions with 34 published parts, 18 independent one-mark answer slots and 4 six-mark 6(b) slots; '
                             '2 prose, 2 poetry and 6 additional-literature routes.')
    return dict(review=review, cards=cards)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    data = build()
    scheme_words_in(data)  # guidance carries the SEC's words only; question and task checks the paper's (irish_lifted.py)
    content = json.dumps(data, ensure_ascii=False, indent=2) + '\n'
    if args.check:
        assert OUT.exists() and OUT.read_text() == content, f'Stale output: {OUT}'
    else:
        OUT.write_text(content)
    print(f"Irish Higher 2020 Paper 2: {len(data['cards'])} reviewed reading and literature cards; the archive remains incomplete.")


if __name__ == '__main__':
    main()
