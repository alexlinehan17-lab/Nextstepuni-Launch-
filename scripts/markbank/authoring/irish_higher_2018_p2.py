#!/usr/bin/env python3
"""Reviewed 2018 Higher Paper 2 (Léamhthuiscint agus Litríocht): new cards, no legacy component.

Paper PDF 1–12 (page 3 the Treoracha, 4–7 the two reading passages with their questions,
8 prose, 9 poetry with An Spailpín Fánach, 10 additional literature, 11 the poem A Chlann,
12 blank) and the Paper 2 pages of the combined LC001ALP000IV scheme (PDF 16–36, plus 37
modified marking) reviewed on 2026-11-04. Counts are assertions, not corpus-completeness proof.

The card shapes follow the reviewed 2020–2026 Higher Paper 2 components: every printed
reading question is a whole card with one criterion per published part, each published
part is also a practice card, two independent one-mark answers expose their own slots,
order-dependent 2 + 1 items stay whole, and the two 6-mark halves of A 6(b) (two reasons)
expose their own slots. B 6(b) is the reaction-and-two-points shape of 2021 B 6(b): one
part with the reaction 2 and points 5 + 5 as its criteria. 2018 prints two prescribed prose
texts under 2A (the film Cáca Milis or the play An Lasair Choille: a card each, as their
Atlas headings differ), one optional film-or-play 2B (one card carrying both printed
alternatives), one prescribed poem (3A An Spailpín Fánach), one optional poem from before
1850 (3B) and six Q4 options; each is one card with its printed sub-questions as criteria
and one shared 5-mark Gaeilge award.

2018's scheme layout differs from 2020's: the 2A questions, their "Eolas = 25 marc" and
their Eolas/Gaeilge band table sit on PDF 25, and each prescribed text's supporting notes
follow on its own page (26, 27) ending at the examiner's panel "Eolas (25) = Gaeilge (5) =";
2B (PDF 28) prints its question and Treoir, then the marking-panel note ("Nóta: Caithfidh an
Scrúdaitheoir …") and its own band table; the poems end at that note, after which the text
layer stores the Gaeilge table (and on PDF 30 the Marc as 4 table of 3A(ii)); Q4A–E print no
"Eolas = 35 marc" line of their own (the Treoracha and the band table on PDF 33 price them);
4F ends at "Ní mór don Scrúdaitheoir an marc ar Eolas as 35 marc …", after which its Marc as
7 and Marc as 4 tables are stored. Boxed headings are removed by exact match.
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
OUT = ROOT / 'components/MarkBank/cards/irish/higher-2018-p2-authored.json'
SOURCE_REVIEW = ROOT / 'scripts/markbank/authored/irish-higher-2018-p2-source-review.json'
REVIEWED_AT = '2026-11-04'
PAPER_SHA = 'b3efaba3dab0db1d1f9dfbedf598990f16641590b5dd710f2faa4e717a06fa64'
SCHEME_SHA = '0c731bc9ccf61600238aa36ec5473ab4713d0d60cb6233fd5d2782e8d9c8c7a3'
DIRECTIVE = re.compile(r'rogha|roghna|Freagair|Luaigh|Ainmnigh|\bnó\b|dhá phointe|dhá rud|dhá bh|dhá dh|dhá ch|dhá fh|dhá th|'
                       r'ceann amháin|pointe amháin|\bdhá\b|an dá\b|amháin', re.I)
SOURCE_NOTE = 'Shown page-for-page from the official examination paper; swipe to move between pages.'
# Boxed page headings the 2018 text layer stores inside the literature pages; exact strings only.
FURNITURE = ('– PRÓS AINMNITHE nó PRÓS ROGHNACH – (30 marc)', '– FILÍOCHT AINMNITHE nó FILÍOCHT ROGHNACH – (30 marc)')
# The examiner's marking-panel note that closes 2B and each poem answer: the boundary of the answer's own text.
PANEL = 'Nóta: Caithfidh an Scrúdaitheoir'
GAEILGE_TABLE = re.compile(r'Gaeilge \(5 mharc\) Sárchumas.*?Cumas lag/an-lag maidir leis na príomhghnéithe de cheart na teanga \(gramadach, comhréir, struchtúr, deilbhíocht\) 1')
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
    # The marks a single-answer part can earn: 0, the full tariff and every partial the scheme prints for it,
    # including the deficient-answer reduction "tá an freagra easnamhach (2-1)" (A 4(b)(ii)).
    values = re.findall(r'= (\d+) mh?arc', chunk) + re.findall(r'bronntar (\d+) mh?arc', chunk) + re.findall(r'\((\d+) mh?arc\)', chunk)
    values += [int(a) - int(b) for a, b in re.findall(r'easnamhach \((\d+)-(\d+)\)', chunk)]
    return sorted({0, marks} | {int(v) for v in values if int(v) <= marks})


def material():
    import fitz
    paper_path = ROOT / f'paper-trail-corpus/exampapers/2018/{FILE}.pdf'
    scheme_path = ROOT / f'paper-trail-corpus/markingschemes/2018/{SCHEME_FILE}.pdf'
    assert hashlib.sha256(paper_path.read_bytes()).hexdigest() == PAPER_SHA, 'Paper changed: repeat visual review'
    assert hashlib.sha256(scheme_path.read_bytes()).hexdigest() == SCHEME_SHA, 'Scheme changed: repeat visual review'
    paper, doc = fitz.open(paper_path), fitz.open(scheme_path)
    texts = [clean(p.get_text()) for p in paper]
    s = Scheme(doc, 16, 36)
    # The marking instructions, from their first rule (their heading "Treoracha do mharcáil na léamhthuisceana" is a title)
    # to the boxed section heading that the text layer stores after them.
    general = s.chunk('Tá Ceist 1 – 5 ar cómharc', 'Páipéar II (200 marc)')[0]
    assert general.endswith('sa fhreagarleabhar.'), general[-60:]
    # (q, part, paper prompt, scheme anchor, marks, mode, printed tariff). Each passage ends where the examiner's
    # marking panel for 6(b) begins ("C1 (2) + P1 (4) = …", "Tuairim = 2 mharc … Ceist 6 (b) (12) =").
    passages = {
        'A': dict(title='Scéalta ó na Daonáirimh', pages=[4, 5], topic='irish-3-0', end='C1 (2) + P1 (4) = C2 (2) + P2 (4) =', parts=[
            ('1', 'a', '(a) Cad is daonáireamh ann? Tabhair dhá phointe eolais. (Alt 1)', '1. (a) Cad is daonáireamh ann?', 3, 'ordered', '{3 mharc: 2 mharc + 1 mharc}'),
            ('1', 'bi', '(b) (i) Cén fáth a raibh ar Mhuire agus ar Iósaf filleadh ar bhaile a sinsear, Beithil? (Alt 1)', '(b) (i) Cén fáth a raibh ar Mhuire', 2, None, '{2 mharc}'),
            ('1', 'bii', '(ii) Tabhair an dá chúis a ndearnadh gach aon cheann de na daonáirimh sin. (Alt 1)', '(ii) Tabhair an dá chúis a ndearnadh', 2, 'slots', '{2 mharc: 1 mharc + 1 mharc}'),
            ('2', 'a', '(a) Scríobh síos an dá rud a rinne na háiritheoirí i ndaonáireamh 1821. (Alt 2)', '2. (a) Scríobh síos an dá rud a rinne na háiritheoirí', 3, 'ordered', '{3 mharc: 2 mharc + 1 mharc}'),
            ('2', 'bi', '(b) (i) Luaigh rud amháin a thaispeánann go ndearnadh daonáireamh 1841 ar bhealach níos proifisiúnta ná mar a rinneadh na cinn a bhí ann roimhe sin. (Alt 2)', '(b) (i) Luaigh rud amháin a thaispeánann', 2, None, '{2 mharc}'),
            ('2', 'bii', '(ii) Cén t‐eolas breise a bailíodh i ndaonáireamh 1841? (Alt 2)', '(ii) Cén t-eolas breise a bailíodh', 2, None, '{2 mharc}'),
            ('3', 'a', '(a) Luaigh dhá chúis ar taifid luachmhara iad tuairisceáin na ndaonáireamh éagsúil. (Alt 3)', '3. (a) Luaigh dhá chúis ar taifid luachmhara', 3, 'ordered', '{3 mharc: 2 mharc + 1 mharc}'),
            ('3', 'bi', '(b) (i) Cén tábhacht a bhaineann le daonáirimh na mblianta 1841 agus 1861? (Alt 3)', '(b) (i) Cén tábhacht a bhaineann le daonáirimh', 2, None, '{2 mharc}'),
            ('3', 'bii', '(ii) Cén fáth nach ndearnadh aon daonáireamh sa bhliain 1921? (Alt 3)', '(ii) Cén fáth nach ndearnadh aon daonáireamh', 2, None, '{2 mharc}'),
            ('4', 'a', '(a) Tabhair dhá phointe eolais faoi na náisiúnaigh choigríche in Éirinn. (Alt 4)', '4. (a) Tabhair dhá phointe eolais faoi na náisiúnaigh', 3, 'ordered', '{3 mharc: 2 mharc + 1 mharc}'),
            ('4', 'bi', '(b) (i) Cad iad na himpleachtaí atá ag an titim sa daonra i gcontaetha áirithe san iarthar agus san iarthuaisceart do sholáthar seirbhísí sna ceantair sin? (Alt 4)', '(b) (i) Cad iad na himpleachtaí', 2, None, '{2 mharc}'),
            ('4', 'bii', '(ii) Tá daonra na hÉireann ag dul in aois. Cén dúshlán a chruthaíonn sé sin don rialtas? (Alt 4)', '(ii) Tá daonra na hÉireann ag dul in aois.', 2, None, '{2 mharc}'),
            ('5', 'a', '(a) Cén fhianaise atá i ndaonáireamh 2016 go bhfuil borradh faoi gheilleagar na hÉireann arís? Tabhair dhá phointe eolais. (Alt 5)', '5. (a) Cén fhianaise atá i ndaonáireamh 2016', 3, 'ordered', '{3 mharc: 2 mharc + 1 mharc}'),
            ('5', 'bi', '(b) (i) Cén t‐eolas spéisiúil a d’fhoilsigh an Phríomh‐Oifig Staidrimh faoin tslí a dtéann daoine chuig a n‐ionad oibre? (Alt 5)', '(b) (i) Cén t-eolas spéisiúil', 2, None, '{2 mharc}'),
            ('5', 'bii', '(ii) Cén tábhacht do mhuintir na hÉireann a bhainfidh leis an daonáireamh a bheidh ar siúl i ngach ballstát den Aontas Eorpach sa bhliain 2021? (Alt 5)', '(ii) Cén tábhacht do mhuintir na hÉireann', 2, None, '{2 mharc}'),
            ('6', 'a', '(a) Aimsigh sampla den bhriathar saor san Aimsir Fháistineach in Alt 4 agus sampla de bhreischéim na haidiachta in Alt 5.', '6. (a) Aimsigh sampla den bhriathar saor san Aimsir Fháistineach', 3, 'grammar', '{3 mharc: 2 mharc + 1 mharc}'),
            ('6', 'b', '(b) Bunaithe ar an eolas sa sliocht thuas, déan plé, i d’fhocail féin, ar dhá chúis ar scríobh an t‐údar an sliocht seo. (Is leor 60 focal.)', '(b) Bunaithe ar an eolas sa sliocht thuas, déan plé, i d’fhocail féin, ar dhá chúis', 12, 'reasons', 'Dhá chúis = 6 mharc + 6 mharc')]),
        'B': dict(title='2018 ‐ Ceiliúradh ar an Oidhreacht Chultúrtha agus ar an nGaeilge', pages=[6, 7], topic='irish-3-1',
                  end='Tuairim = 2 mharc Pointe eolais 1 = 5 mharc Pointe eolais 2 = 5 mharc Ceist 6 (b) (12) =', parts=[
            ('1', 'a', '(a) Cén sainmhíniú ar ‘oidhreacht chultúrtha’ atá i ráiteas misin an Choimisiúin Eorpaigh? Tabhair dhá phointe eolais. (Alt 1)', '1. (a) Cén sainmhíniú ar ‘oidhreacht chultúrtha’', 3, 'ordered', '{3 mharc: 2 mharc + 1 mharc}'),
            ('1', 'bi', '(b) (i) Cén deis a thabharfaidh na himeachtaí speisialta do phobail na dtíortha éagsúla? (Alt 1)', '(b) (i) Cén deis a thabharfaidh na himeachtaí', 2, None, '{2 mharc}'),
            ('1', 'bii', '(ii) Cén cúram reachtúil atá ar an gComhairle Oidhreachta in Éirinn? (Alt 1)', '(ii) Cén cúram reachtúil', 2, None, '{2 mharc}'),
            ('2', 'a', '(a) Cad is Láithreán Oidhreachta Domhanda ann? (Alt 2)', '2. (a) Cad is Láithreán Oidhreachta Domhanda ann?', 3, 'ordered', '{3 mharc: 2 mharc + 1 mharc}'),
            ('2', 'bi', '(b) (i) Luaigh pointe amháin eolais faoi Chnuasach Bhéaloideas Éireann atá i gColáiste na hOllscoile, Baile Átha Cliath. (Alt 2)', '(b) (i) Luaigh pointe amháin eolais faoi Chnuasach', 2, None, '{2 mharc}'),
            ('2', 'bii', '(ii) Scríobh síos pointe amháin eolais faoin Ogham. (Alt 2)', '(ii) Scríobh síos pointe amháin eolais faoin Ogham.', 2, None, '{2 mharc}'),
            ('3', 'a', '(a) Luaigh dhá aidhm atá le Bliain na Gaeilge in 2018. (Alt 3)', '3. (a) Luaigh dhá aidhm atá le Bliain na Gaeilge', 3, 'ordered', '{3 mharc: 2 mharc + 1 mharc}'),
            ('3', 'bi', '(b) (i) Cén fáth a raibh cibear‐Ghaeltacht, Trasna na dTonnta, ar bun ar feadh seachtaine i mí Eanáir? (Alt 3)', '(b) (i) Cén fáth a raibh cibear-Ghaeltacht', 2, None, '{2 mharc}'),
            ('3', 'bii', '(ii) Cén t‐údar imní atá ann i gcás na Gaeilge? (Alt 3)', '(ii) Cén t-údar imní', 2, None, '{2 mharc}'),
            ('4', 'a', '(a) Tabhair dhá chúis a raibh an phíobaireacht ag dul i léig in Éirinn sna seascaidí. (Alt 4)', '4. (a) Tabhair dhá chúis a raibh an phíobaireacht', 3, 'ordered', '{3 mharc: 2 mharc + 1 mharc}'),
            ('4', 'bi', '(b) (i) Cén fáth ar bunaíodh an eagraíocht Na Píobairí Uilleann sa bhliain 1968? (Alt 4)', '(b) (i) Cén fáth ar bunaíodh an eagraíocht', 2, None, '{2 mharc}'),
            ('4', 'bii', '(ii) Cad a léiríonn comhartha aitheantais UNESCO? (Alt 4)', '(ii) Cad a léiríonn comhartha aitheantais UNESCO?', 2, None, '{2 mharc}'),
            ('5', 'a', '(a) Luaigh dhá shlí ar féidir leis an athrú aeráide dul i gcion go fisiceach ar an oidhreacht chultúrtha. (Alt 5)', '5. (a) Luaigh dhá shlí', 3, 'ordered', '{3 mharc: 2 mharc + 1 mharc}'),
            ('5', 'bi', '(b) (i) Cén ról a bhíonn ag na treoraithe ar na láithreáin oidhreachta? (Alt 5)', '(b) (i) Cén ról a bhíonn ag na treoraithe', 2, None, '{2 mharc}'),
            ('5', 'bii', '(ii) Cén toradh fadtéarmach a bhfuil bunaitheoirí Bhliain Eorpach na hOidhreachta Cultúrtha ag súil leis? (Alt 5)', '(ii) Cén toradh fadtéarmach', 2, None, '{2 mharc}'),
            ('6', 'a', '(a) Aimsigh sampla d’ainmfhocal firinscneach sa tuiseal ginideach uatha in Alt 3 agus sampla den bhriathar saor san Aimsir Láithreach in Alt 5.', '6. (a) Aimsigh sampla d’ainmfhocal firinscneach', 3, 'grammar', '{3 mharc: 2 mharc + 1 mharc}'),
            ('6', 'b', '(b) Conas a chuaigh an sliocht seo i bhfeidhm ort? Tabhair dhá phointe eolais i d’fhocail féin, as an sliocht, mar thacaíocht le do fhreagra. (Is leor 60 focal.)', '(b) Conas a chuaigh an sliocht seo i bhfeidhm ort?', 12, 'opinion', '{2 mharc + 5 mharc + 5 mharc}')]),
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
            assert 'Ag bun Léamhthuiscint' not in chunk and 'Páipéar II' not in chunk and 'Ceist 2 PRÓS' not in chunk, (letter, q, part)
            resolved.append((q, part, prompt, anchor, marks, mode, chunk, spages))
        passage['resolved'] = resolved
    assert sum(len(p['resolved']) for p in passages.values()) == 34
    note5 = s.chunk('Nóta: I gcás na gceisteanna 2 (Prós)', 'Nóta: Níl na nótaí tacaíochta seo uileghabhálach')[0]
    notes = s.chunk('Nóta: Níl na nótaí tacaíochta seo uileghabhálach', 'Freagair Ceist 2A (Prós Ainmnithe)')[0]
    gaeilge_table = GAEILGE_TABLE.search(s.text, s.page(30)).group(0)
    # 2A's band table (PDF 25) and 2B's (PDF 28) print the Eolas and Gaeilge columns side by side; their wording differs.
    prose_table = s.chunk('Catagóir Eolas (25 marc) Gaeilge (5 mharc)', '– PRÓS AINMNITHE nó PRÓS ROGHNACH – (30 marc)')[0]
    table28 = s.chunk('Catagóir Eolas (25 marc) Gaeilge (5 mharc)', '⟦29⟧', s.page(28))[0]
    table35 = s.chunk('Catagóir Eolas (35 marc) Gaeilge (5 mharc)', '⟦34⟧', s.page(33))[0]
    general4 = s.chunk('Treoracha: Iarrtar ar na hiarrthóirí plé a dhéanamh ar an ráiteas', 'Eolas (35) = Gaeilge (5) =', s.page(33))[0]
    assert all(x in gaeilge_table for x in ['Sárchumas', 'Cumas lag/an-lag']) and '22-25' in prose_table and '0-9' in prose_table
    assert '22-25' in table28 and '0-9' in table28 and table28 != prose_table
    assert '30-35' in table35 and '0-13' in table35 and general4.endswith('sa fhreagarleabhar.') and '35 marc' in general4
    assert note5.endswith('ar Ghaeilge.') and notes.endswith('de réir a bhfiúntais.')
    return dict(paper=paper, texts=texts, s=s, general=general, passages=passages, note5=note5, notes=notes,
                gaeilge_table=gaeilge_table, prose_table=prose_table, table28=table28, table35=table35, general4=general4,
                decisions=selection_decisions(paper))


READING_REQUIREMENTS = ['Léigh an sliocht iomlán a ghabhann leis an gceist. Freagair an chuid atá luaite ar an gcárta.',
                        'Úsáid an t-alt a luaitear. Glacfar le focail an tsleachta nó le do chuid focal féin, ach ní mór 6(b) a fhreagairt i d’fhocail féin.']
WHOLE_REQUIREMENTS = ['Léigh an sliocht oifigiúil a ghabhann leis an gceist.', 'Freagair gach fochuid agus cloígh leis an alt a luaitear.',
                      'Bain úsáid as do chuid focal féin nuair a iarrtar ort é.']
LIT_REQUIREMENTS = ['Freagair gach cuid den cheist atá priontáilte.', 'Úsáid tagairtí cruinne agus ábhartha don téacs.']
PART_NOTE = ('SEC allocation for this task. Alternative correct answers in the scheme are answers to one task, not extra task routes. '
             'Whole questions and their practice parts are overlapping exercises; their marks are not added to infer the paper total.')
LABELS = {'a': '(a) Freagra', 'bi': '(b)(i) Freagra', 'bii': '(b)(ii) Freagra', 'grammar': '(a) Freagra',
          'reason-1': '(b) Cúis 1', 'reason-2': '(b) Cúis 2',
          'opinion': '(b) Tuairim', 'point-1': '(b) Pointe eolais 1', 'point-2': '(b) Pointe eolais 2'}
# The two 6-mark halves of A 6(b): (criterion id prefix, label, English practice focus).
HALVES = {'reasons': ('reason', 'Cúis', 'One of the two reasons the writer wrote the extract, discussed in your own words (reason {slot}, 6 marks)')}


def part_criteria(part, marks, mode, chunk, general):
    if mode in HALVES:
        key, label, _ = HALVES[mode]
        return [criterion(f'{key}-1', f'{label} 1', 6, [chunk, general]), criterion(f'{key}-2', f'{label} 2', 6, [chunk, general])]
    if mode == 'opinion':
        # "Tuairim a léiriú = 2 mharc / Pointe eolais 1 = 5 mharc / Pointe eolais 2 = 5 mharc" (B 6(b)), as 2021 B 6(b).
        return [criterion('opinion', 'Tuairim', 2, [chunk, general]), criterion('point-1', 'Pointe eolais 1', 5, [chunk]),
                criterion('point-2', 'Pointe eolais 2', 5, [chunk])]
    if mode in ('ordered', 'grammar'):
        return [criterion('grammar' if mode == 'grammar' else part, 'Freagra', marks, [chunk, general], permitted=[0, 2, 3])]
    if mode == 'slots':
        # "{2 mharc: 1 mharc + 1 mharc}": either answer alone earns 1, even where the accepted list prints no per-answer marks.
        return [criterion(part, 'Freagra', marks, [chunk, general], permitted=[0, 1, 2])]
    return [criterion(part, 'Freagra', marks, [chunk, general], permitted=printed_values(chunk, marks))]


def split_parts(whole, cuts, caps):
    i2 = whole.index(cuts[0]); i3 = whole.index(cuts[1], i2)
    pieces = [whole[:i2].strip(), whole[i2:i3].strip(), whole[i3:].strip()]
    for piece, cap in zip(pieces, caps):
        assert cap in piece, cap
    return pieces


def stored_after(s, table, boundary, page):
    """A band table the text layer stores after the answer's closing note on `page`, before the next page."""
    at = s.text.index(table, s.text.index(boundary, s.page(page)))
    end = s.text.find(f'⟦{page + 1}⟧')
    assert at < (end if end > 0 else len(s.text)), table
    return table


def build():
    m = material()
    texts, s = m['texts'], m['s']
    cards = []

    def add(key, slug, ref, prompt, topic, pages, scheme_pages, criteria, requirements, note, extra_topics=None, source=None, **extra):
        cards.append(dict(
            id=f'irish-2018-hl-p2-{slug}', year=2018, level='higher', paper=2, section='2',
            atlasQuestionId=key, questionRef=f'2018 HL Paper 2 {ref}', questionText=prompt,
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
    six_b = {'A': '6(b) prices two reasons, 6 marks each (naming the reason 2 + its discussion with information from the passage 4), in the candidate’s own words.',
             'B': '6(b) is one response: the reaction 2 and two supported points 5 + 5, in the candidate’s own words.'}
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
                        READING_REQUIREMENTS, 'The scheme prices the two halves 6 + 6 independently (named 2 + discussed 4); this card practises one of them. ' + PART_NOTE,
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
    choice2a = 'Freagair an cheist thíos ar an scannán Cáca Milis nó ar an dráma An Lasair Choille.'
    prose_note = ('One complete SEC response: 25 Eolas and a single shared 5-mark Gaeilge award. Supporting notes are indicative rather than exhaustive. '
                  'The printed band table gives the Eolas and Gaeilge columns side by side.')
    prescribed = [
        # (key, slug, ref, topic, question-page start, question-page end, notes start, notes page)
        ('P-2A-caca-milis', 'prose-2a-caca-milis', 'Prós 2A · Cáca Milis', 'irish-4-6',
         'Cáca Milis “Is duine faoi mhíchumas', 'nó An Lasair Choille', 'Nótaí Tacaíochta Cáca Milis', 26,
         'Cáca Milis\n“Is duine faoi mhíchumas é Paul sa scannán Cáca Milis, ach ní thuilleann sé mórán trua dá chás ón lucht féachana.”\nDéan plé ar an ráiteas sin. (30 marc)'),
        ('P-2A-an-lasair-choille', 'prose-2a-an-lasair-choille', 'Prós 2A · An Lasair Choille', 'irish-4-8',
         'An Lasair Choille “Tá léiriú sa dráma An Lasair Choille', 'Catagóir Eolas (25 marc)', 'Lasair Choille “Tá léiriú sa dráma Lasair Choille', 27,
         'An Lasair Choille\n“Tá léiriú sa dráma An Lasair Choille ar an gcineál duine é Micil, an cláiríneach, agus ar an tionchar a bhíonn aige ar Shéamas.”\nDéan plé ar an ráiteas sin. (30 marc)'),
    ]
    stem2a = head2 + '\n2A. Prós Ainmnithe'
    for key, slug, ref, topic, qstart, qend, nstart, npage, option in prescribed:
        prompt = choice2a + '\n\n' + option
        for line in [*stem2a.splitlines(), *prompt.splitlines()]:
            if line:
                assert in_order(line, texts[7]), (key, line)
        question, qpages = s.chunk(qstart, qend, s.page(25))
        notes_text, npages = s.chunk(nstart, 'Eolas (25) = Gaeilge (5) =', s.page(npage))
        assert question.endswith('Eolas = 25 marc') and qpages == [25] and npages == [npage], key
        add(key, slug, ref, prompt, topic, [8], sorted({25, npage}),
            [criterion('eolas', 'Eolas', 25, [clean(question + ' ' + notes_text), m['prose_table'], m['notes']], 'indicative'), gaeilge()],
            LIT_REQUIREMENTS, prose_note, source=('Prós', ref.split(' · ', 1)[1], [8]), stem=stem2a)
    # 2B: one card carries both printed alternatives (an optional film or an optional play file under one Atlas heading).
    stem2b = head2 + '\n2B. Prós Roghnach\nNíl cead aon ábhar a bhaineann le Prós Ainmnithe a úsáid i bhfreagra ar an bPrós Roghnach.'
    prompt2b = ('Freagair an cheist thíos ar an scannán roghnach nó ar an dráma roghnach.\n\n'
                'Maidir leis an scannán roghnach a ndearna tú staidéar air le linn do chúrsa, roghnaigh an príomhcharachtar (an phríomhphearsa) sa scannán sin. '
                'Déan plé ar an léargas a thugtar dúinn ar thréithe agus ar iompar an duine sin ó thús deireadh an scannáin.\n'
                'Ní mór teideal an scannáin sin, mar aon le hainm an scríbhneora, a scríobh síos go cruinn. (30 marc)\n\nnó\n\n'
                'Maidir leis an dráma roghnach a ndearna tú staidéar air le linn do chúrsa, roghnaigh an príomhcharachtar (an phríomhphearsa) sa dráma sin. '
                'Déan plé ar an léargas a thugtar dúinn ar thréithe agus ar iompar an duine sin ó thús deireadh an dráma.\n'
                'Ní mór teideal an dráma sin, mar aon le hainm an scríbhneora, a scríobh síos go cruinn. (30 marc)')
    for line in [*stem2b.splitlines(), *prompt2b.splitlines()]:
        if line:
            assert in_order(line, texts[7]), ('P-2B', line)
    # The scheme reprints the question (on the card already); its own marking text for 2B is the Treoir after it.
    question2b = s.chunk('2B. Prós Roghnach', 'Treoir: An príomhcharachtar', s.page(28))[0]
    assert all(in_order(line, question2b) for line in prompt2b.splitlines() if line), 'P-2B scheme reprint differs from the paper'
    chunk2b, pages2b = s.chunk('Treoir: An príomhcharachtar', PANEL, s.page(28))
    assert chunk2b.endswith('mar a léirítear sa téacs iad.') and 'Catagóir' not in chunk2b and pages2b == [28]
    stored_after(s, m['table28'], PANEL, 28)
    add('P-2B', 'prose-2b', 'Prós 2B · Scannán nó dráma roghnach', prompt2b, 'irish-4-7', [8], [28],
        [criterion('eolas', 'Eolas', 25, [chunk2b, m['table28'], m['notes']], 'indicative'), gaeilge()], LIT_REQUIREMENTS,
        prose_note + ' The scheme prices 2B as 25 Eolas and 5 Gaeilge in its band table and marking note (PDF 28); the film and the play are two printed alternatives of one route.',
        source=('Prós', 'Scannán nó dráma roghnach', [8]), stem=stem2b)

    poems = [
        ('F-3A', 'poetry-3a', 'Filíocht 3A · An Spailpín Fánach', 'irish-5-1', '3A. Filíocht Ainmnithe (i)', 29, head3 + '\n3A. Filíocht Ainmnithe', [
            '(i) “Tá brón agus bród an spailpín le feiceáil go soiléir sa dán An Spailpín Fánach (thíos).” É sin a phlé. (15 mharc)',
            '(ii) Conas a chuaigh an dán seo i bhfeidhm ort? (Is leor pointe amháin eolais as an dán mar thacaíocht le do fhreagra.) (6 mharc)',
            '(iii) Cén mheadaracht atá sa dán seo? Scríobh pointe amháin eolais faoin meadaracht seo agus léirigh do fhreagra le sampla cruinn ón dán. (9 marc)'],
         ['(ii) Conas a chuaigh an dán seo i bhfeidhm ort?', '(iii) Cén mheadaracht atá sa dán seo?'], 30),
        ('F-3B', 'poetry-3b', 'Filíocht 3B · Dán seanaimseartha roghnach', 'irish-5-6', '3B. Filíocht Roghnach Níl cead', 31,
         head3 + '\n3B. Filíocht Roghnach\nNíl cead aon ábhar a bhaineann le Filíocht Ainmnithe a úsáid i bhfreagra ar an bhFilíocht Roghnach.', [
            '(i) Maidir le dán seanaimseartha roghnach (dán a cumadh sa tréimhse roimh 1850) a ndearna tú staidéar air le linn do chúrsa, scríobh síos príomhthéama an dáin. Déan plé ar an léiriú a thugtar ar an bpríomhthéama sin ó thús deireadh an dáin. (15 mharc)',
            '(ii) Conas a chuaigh an dán seo i bhfeidhm ort? (Is leor pointe amháin eolais as an dán mar thacaíocht le do fhreagra.) (6 mharc)',
            '(iii) Scríobh síos an teicníc fhileata is mó a thaitníonn leat sa dán. Scríobh dhá phointe eolais faoin teicníc sin. (9 marc)',
            'Ní mór teideal an dáin sin, mar aon le hainm an fhile, a scríobh síos go cruinn.'],
         ['(ii) Conas a chuaigh an dán seo i bhfeidhm ort?', '(iii) Scríobh síos an teicníc fhileata'], None),
    ]
    for key, slug, ref, topic, start, page, stem, parts, cuts, marc4_page in poems:
        for line in [*stem.splitlines(), *parts]:
            assert in_order(line, texts[8]), (key, line[:40])
        whole, spages = s.chunk(start, PANEL, s.page(page))
        assert not GAEILGE_TABLE.search(whole) and 'Eolas (25) =' not in whole, key
        pieces = split_parts(whole, cuts, ['Eolas = 13 mharc', 'Eolas = 5 mharc', 'Eolas = 7 marc'])
        if marc4_page:
            # 3A: the Cur síos (13 mharc) table of (i) sits before (ii); the Marc as 4 table of (ii)'s point is stored
            # after the marking-panel note at the foot of PDF 30.
            assert 'Catagóir Cur síos (13 mharc)' in pieces[0]
            pieces[1] = clean(pieces[1] + ' ' + stored_after(s, MARC4_TABLE, PANEL, marc4_page))
            spages = sorted(set(spages) | {marc4_page})
        else:
            # 3B prints its Marc as 11 table inside (i) and its Marc as 4 table inside (ii).
            assert 'Catagóir Marc as 11' in pieces[0]
        assert MARC4_TABLE in pieces[1] and MARC4_TABLE not in pieces[0] + pieces[2], key
        add(key, slug, ref, '\n'.join(parts), topic, [9], sorted(set(spages) | ({32} if key == 'F-3B' else set())),
            [criterion('eolas-i', '(i) Eolas', 13, [pieces[0]], 'indicative'), criterion('eolas-ii', '(ii) Eolas', 5, [pieces[1]], 'indicative'),
             criterion('eolas-iii', '(iii) Eolas', 7, [pieces[2]], 'indicative'), gaeilge()], LIT_REQUIREMENTS,
            'One complete SEC response with one shared five-mark Gaeilge award. The paper prints (i) 15, (ii) 6 and (iii) 9; the scheme assesses '
            'Eolas 13, 5 and 7 with the conditions shown, plus Gaeilge 5 once. Supporting notes are indicative rather than exhaustive.',
            source=('Filíocht', ref.split(' · ', 1)[1], [9]), stem=stem)

    head4 = 'Freagair do rogha ceann amháin as Ceist 4 (A, B, C, D, E nó F) thíos.'
    options = [
        ('X-4A', 'literature-4-a', '4A. An Triail', 'irish-6-0', '4A. An Triail', 'Catagóir Eolas (35 marc)',
         '4A. An Triail\n“Tugtar léargas sa dráma An Triail ar an gcaoi chruálach mhíthrócaireach ar caitheadh le máthair neamhphósta in Éirinn sna seascaidí.”\nDéan plé ar an ráiteas sin. (40 marc)'),
        ('X-4B', 'literature-4-b', '4B. A Thig Ná Tit Orm', 'irish-6-1', '4B. A Thig Ná Tit Orm', '4C. Tóraíocht Dhiarmada',
         '4B. A Thig Ná Tit Orm\n“Sa dírbheathaisnéis A Thig Ná Tit Orm, tugann Maidhc Dainín cuntas spéisiúil dúinn ar na daoine ina theaghlach agus sa phobal timpeall air.”\nDéan plé ar an ráiteas sin. (40 marc)'),
        ('X-4C', 'literature-4-c', '4C. Tóraíocht Dhiarmada agus Ghráinne', 'irish-6-2', '4C. Tóraíocht Dhiarmada', '4D. Gafa',
         '4C. Tóraíocht Dhiarmada agus Ghráinne\n“Tugtar léiriú éifeachtach dúinn ar an bpáirt thábhachtach a bhí ag na carachtair (na pearsana) Aonghus an Bhrogha agus Muadhán sa Tóraíocht.”\nDéan plé ar an ráiteas sin. (40 marc)'),
        ('X-4D', 'literature-4-d', '4D. Gafa', 'irish-6-3', '4D. Gafa', '4E. Canary Wharf',
         '4D. Gafa\n“Tá an t‐amhras agus an míshuaimhneas le brath go minic sa chaidreamh idir na carachtair (na pearsana) éagsúla sa sliocht as an úrscéal Gafa.”\nDéan plé ar an ráiteas sin. (40 marc)'),
        ('X-4E', 'literature-4-e', '4E. Canary Wharf', 'irish-6-4', '4E. Canary Wharf', '4F. Dánta Breise',
         '4E. Canary Wharf\n“Is duine amhrasach míshásta é Ultan sa scéal Saineolaí Teicneolaí.”\nDéan plé ar an ráiteas sin. (40 marc)'),
    ]
    for key, slug, ref, topic, start, end, prompt in options:
        assert all(in_order(line, texts[9]) for line in prompt.splitlines()), key
        chunk, spages = s.chunk(start, end, s.page(33))
        assert 'Treoir:' in chunk and 'Catagóir' not in chunk and 'Gaeilge (5 mharc)' not in chunk, key
        add(key, slug, f'Litríocht {ref}', head4 + '\n\n' + prompt, topic, [10], sorted(set(spages) | {33}),
            [criterion('eolas', 'Eolas', 35, [chunk, m['general4'], m['table35']], 'indicative'), gaeilge()], LIT_REQUIREMENTS,
            'One complete SEC response: Eolas 35 assessed as a unit with a single shared 5-mark Gaeilge award. Supporting notes are indicative rather than exhaustive.'
            + (' Where the scheme prints “Eolas (35-10) (25) =”, an answer that discusses only one of the required people is deficient and loses 10 of the 35.'
               if 'Eolas (35-10) (25) =' in chunk else ''))
    closing4f = 'Ní mór don Scrúdaitheoir an marc ar Eolas as 35 marc'
    whole, spages = s.chunk('4F. Dánta Breise – A Chlann', closing4f, s.page(35))
    pieces = split_parts(whole, ['(ii) A bhfuil i gceist leis na línte seo a mhíniú', '(iii) An teideal oiriúnach ar an dán é'],
                         ['Eolas = 19 marc', 'Míniú = 7 marc', 'Eolas = 9 marc'])
    assert 'Catagóir Eolas (19 marc)' in pieces[0] and 'Catagóir' not in pieces[1] + pieces[2]
    # The Marc as 7 table prices (ii)'s 7-mark explanation and the Marc as 4 table (iii)'s two 4-mark reasons; the text
    # layer stores both after the closing note at the foot of PDF 36.
    pieces[1] = clean(pieces[1] + ' ' + stored_after(s, MARC7_TABLE, closing4f, 36))
    pieces[2] = clean(pieces[2] + ' ' + stored_after(s, MARC4_TABLE, closing4f, 36))
    f_prompt = ('4F. Dánta Breise – A Chlann\nFreagair (i), (ii) agus (iii) thíos.\n'
                '(i) Déan plé ar an gcaoi a léirítear grá na máthar dá clann agus an imní atá uirthi fúthu sa dán A Chlann (thall). (20 marc)\n'
                '(ii) A bhfuil i gceist leis na línte seo a mhíniú: (10 marc)\nNí liomsa bhúr mbrionglóidí ná bhúr mbealaí,\n'
                'Ná ní liom bhúr smaointe ná bhúr ndearcadh!\nNíl baint agam le rogha bhúr gcroí –\n'
                '(iii) An teideal oiriúnach ar an dán é, A Chlann, dar leat? Tabhair dhá fháth le do fhreagra. (10 marc)')
    assert all(in_order(line, texts[9]) for line in f_prompt.splitlines())
    add('X-4F', 'literature-4-f', 'Litríocht 4F · Dánta Breise – A Chlann', head4 + '\n\n' + f_prompt, 'irish-6-8', [10, 11],
        sorted(set(spages) | {33, 36}),
        [criterion('eolas-i', '(i) Eolas', 19, [pieces[0], m['general4']], 'indicative'), criterion('eolas-ii', '(ii) Eolas', 7, [pieces[1]], 'indicative'),
         criterion('eolas-iii', '(iii) Eolas', 9, [pieces[2]], 'indicative'), gaeilge()], LIT_REQUIREMENTS,
        'One complete SEC response: the paper prints (i) 20, (ii) 10 and (iii) 10; the scheme assesses Eolas 19, 7 and 9 (1 + 4 + 4 for the answer and its two reasons) '
        'plus one shared 5-mark Gaeilge award. Supporting notes are indicative rather than exhaustive.',
        source=('Dánta Breise', 'A Chlann', [10, 11]))

    reading = [c for c in cards if '-reading-' in c['id']]
    literature = [c for c in cards if '-reading-' not in c['id']]
    assert len(reading) == 50 and len(literature) == 11, (len(reading), len(literature))
    assert len({c['id'] for c in cards}) == len(cards) == 61 and len({c['atlasQuestionId'] for c in cards}) == 61
    assert sum(c['totalMarks'] for c in cards if re.fullmatch(r'R-[AB]-\d', c['atlasQuestionId'])) == 100
    for card in cards:
        assert sum(c['maxMarks'] for c in card['criteria']) == card['totalMarks'], card['id']
        for c in card['criteria']:
            assert c['guidance'] and all(not re.search('[-]', g) for g in c['guidance']), (card['id'], c['id'])
            assert all(h not in g for h in FURNITURE for g in c['guidance']), (card['id'], c['id'])
    sr = json.loads(SOURCE_REVIEW.read_text())
    whole = [c['id'] for c in reading if re.fullmatch(r'R-[AB]-\d', c['atlasQuestionId'])]
    review = dict(year=2018, level='higher', paperFileid=FILE + '.pdf', schemeFileid=SCHEME_FILE + '.pdf',
                  paperSha256=PAPER_SHA, schemeSha256=SCHEME_SHA,
                  reviewedPaperPages=list(range(1, 13)), reviewedSchemePages=sr['reviewedSchemePages'], schemeScope=sr['schemeScope'],
                  reviewDate=REVIEWED_AT, status='reviewed', fullPaperAndApplicableSchemeVisualSweep=True, selectionDecisions=m['decisions'],
                  readingWholeCardIds=whole, readingPracticeCardIds=[c['id'] for c in reading if c['id'] not in whole],
                  literatureRouteCardIds=[c['id'] for c in literature],
                  examStructure=dict(readingA=50, readingB=50, prose=30, poetry=30, additionalLiterature=40, total=200),
                  nonPoolDecisions=sr['nonPoolDecisions'], openIssues=[], caveats=sr['sourceFindings'],
                  boundaries='12 whole reading questions with 34 published parts, 2 independent one-mark answer slots and 2 six-mark 6(b) slots; '
                             '3 prose (2A Cáca Milis, 2A An Lasair Choille, 2B film or play), 2 poetry and 6 additional-literature routes.')
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
    print(f"Irish Higher 2018 Paper 2: {len(data['cards'])} reviewed reading and literature cards; the archive remains incomplete.")


if __name__ == '__main__':
    main()
