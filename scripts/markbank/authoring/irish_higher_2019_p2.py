#!/usr/bin/env python3
"""Reviewed 2019 Higher Paper 2 (Léamhthuiscint agus Litríocht): new cards, no legacy component.

Paper PDF 1–12 (page 3 the Treoracha, 4–7 the two reading passages with their questions,
8 prose, 9 poetry, 10–11 additional literature, 12 blank) and the Paper 2 pages of the
combined LC001ALP000IV scheme (PDF 18–43, plus 44 modified marking) reviewed on
2026-11-04. Counts are assertions, not corpus-completeness proof.

The card shapes follow the reviewed 2020–2026 Higher Paper 2 components: every printed
reading question is a whole card with one criterion per published part, each published
part is also a practice card, order-dependent 2 + 1 items stay whole, and the two 6-mark
halves of each 6(b) expose their own slots. 2019 prices no part "1 mharc + 1 mharc", so it
has no one-mark answer slots. 2019 prints one prescribed and one optional prose text (2A the
short story Dís, 2B an optional short story), one prescribed and one optional poem (3A An
tEarrach Thiar, 3B a modern optional poem) and six Q4 options (4F Colmáin); each is one card
with its printed sub-questions as criteria and one shared 5-mark Gaeilge award.

2019's scheme layout is 2020's one PDF page later (irish_higher_2020_p2.py): reading starts
on PDF 18 with the marking instructions; the prose and Q4 band tables print the Eolas and
Gaeilge columns side by side, 2A's and 4A's inside their answers and 2B's after its
marking-panel note ("Nóta: Caithfidh an Scrúdaitheoir …"); 3A (i) prints its own "Cur síos
(13 mharc)" table in place and stores (ii)'s Marc as 4 table after the panel note on PDF 32;
3B prints Marc as 11 and Marc as 4 in place; 4F stores (ii)'s Marc as 7 table after (iii)'s
notes. The boxed headings are removed by exact match. Léamhthuiscint A 6(b) prices two
traits and B 6(b) two reasons, each 6 (named 2 + supported 4).
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
OUT = ROOT / 'components/MarkBank/cards/irish/higher-2019-p2-authored.json'
SOURCE_REVIEW = ROOT / 'scripts/markbank/authored/irish-higher-2019-p2-source-review.json'
REVIEWED_AT = '2026-11-04'
PAPER_SHA = 'ea10c9406fbdb581935756d48672a5bb9ccd1f280e36cf90c5dd0b11ee0c3da6'
SCHEME_SHA = 'e7b8cd6073e973e77eaa1a5891a1ce63fb724d08e0d4ec73d099f54a5a9cd3da'
DIRECTIVE = re.compile(r'rogha|roghna|Freagair|Luaigh|Ainmnigh|\bnó\b|dhá phointe|dhá rud|dhá bh|dhá dh|dhá ch|dhá fh|dhá th|'
                       r'ceann amháin|pointe amháin|\bdhá\b|an dá\b|amháin', re.I)
SOURCE_NOTE = 'Shown page-for-page from the official examination paper; swipe to move between pages.'
# Boxed page headings the 2019 text layer stores inside the literature pages; exact strings only.
FURNITURE = ('Ceist 2 PRÓS (30 marc)', 'Ceist 3 FILÍOCHT (30 marc)', 'Ceist 4 LITRÍOCHT BHREISE (40 marc)',
             '– PRÓS AINMNITHE nó PRÓS ROGHNACH – (30 marc)', '– FILÍOCHT AINMNITHE nó FILÍOCHT ROGHNACH – (30 marc)')
# The examiner's marking-panel note that closes each literature answer: the boundary of the answer's own text.
PANEL = 'Nóta: Caithfidh an Scrúdaitheoir'
GAEILGE_TABLE = re.compile(r'Gaeilge \(5 mharc\) Sárchumas.*?Cumas lag/an-lag maidir leis na príomhghnéithe de cheart na teanga \(gramadach, comhréir, struchtúr, deilbhíocht\) 1')
CUR_SIOS_TABLE = re.compile(r'Catagóir Cur síos \(13 mharc\) Marcanna .*?Lag/An-lag Eolas an-bhearnach, an-mhíchruinn agus an-lochtach 0-5')
MARC11_TABLE = 'Catagóir Marc as 11 Sármhaith 10, 11 An-mhaith 8, 9 Maith 6, 7 Measartha 4, 5 Lag/An-lag 0, 1, 2, 3'
EOLAS19_TABLE = re.compile(r'Catagóir Eolas \(19 marc\) Sármhaith .*?Lag/An-lag Eolas an-bhearnach, an-mhíchruinn agus an- ?lochtach 0-7')
MARC4_TABLE = 'Catagóir Marc as 4 Sármhaith 4 An-mhaith 3 Maith 2 Measartha 1 Lag/An-lag 0'
MARC7_TABLE = 'Catagóir Marc as 7 Sár-mhaith 6-7 An-mhaith 5 Maith 4 Measartha 3 Lag/An-lag 0-2'
MARC54_TABLE = 'Catagóir Marc as 5 Marc as 4 Sármhaith 5 4 An-mhaith 4 3 Maith 3 2 Measartha 2 1 Lag/An-lag 0, 1 0'


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
    paper_path = ROOT / f'paper-trail-corpus/exampapers/2019/{FILE}.pdf'
    scheme_path = ROOT / f'paper-trail-corpus/markingschemes/2019/{SCHEME_FILE}.pdf'
    assert hashlib.sha256(paper_path.read_bytes()).hexdigest() == PAPER_SHA, 'Paper changed: repeat visual review'
    assert hashlib.sha256(scheme_path.read_bytes()).hexdigest() == SCHEME_SHA, 'Scheme changed: repeat visual review'
    paper, doc = fitz.open(paper_path), fitz.open(scheme_path)
    texts = [clean(p.get_text()) for p in paper]
    s = Scheme(doc, 18, 43)
    # The marking instructions, from their first rule (their heading "Treoracha do mharcáil na Léamhthuisceana:" is a title)
    # to the boxed section heading that the text layer stores after them.
    general = s.chunk('Tá Ceist 1 – 5 ar cómharc', 'Páipéar II (200 marc)')[0]
    assert general.endswith('sa fhreagarleabhar.'), general[-60:]
    # (q, part, paper prompt, scheme anchor, marks, mode, printed tariff). Each passage ends where the examiner's
    # marking panel for 6(b) begins ("T1 (2) + S1 (4) = …", "C1 (2) + P1 (4) = …").
    passages = {
        'A': dict(title='Constance Markievicz', pages=[4, 5], topic='irish-3-0', end='T1 (2) + S1 (4) = T2 (2) + S2 (4) =', parts=[
            ('1', 'a', '(a) Luaigh dhá rud ab éigean a bheith ag mná le vóta a bheith acu in olltoghchán 1918. (Alt 1)', '1. (a) Luaigh dhá rud ab éigean', 3, 'ordered', '{3 mharc: 2 mharc + 1 mharc}'),
            ('1', 'bi', '(b) (i) Cén aidhm a bhí ag na feisirí tofa a tháinig le chéile sa Chéad Dáil? (Alt 1)', '(b) (i) Cén aidhm a bhí ag na feisirí', 2, None, '{2 mharc}'),
            ('1', 'bii', '(ii) Scríobh síos pointe amháin eolais a léiríonn gur bhain Constance Markievicz áit faoi leith amach i stair na polaitíochta san olltoghchán sin. (Alt 1)', '(ii) Scríobh síos pointe amháin eolais a léiríonn', 2, None, '{2 mharc}'),
            ('2', 'a', '(a) Scríobh síos dhá chaitheamh aimsire a bhí ag Constance Gore‐Booth agus í ag fás aníos i Lios an Daill, Co. Shligigh. (Alt 2)', '2. (a) Scríobh síos dhá chaitheamh aimsire', 3, 'ordered', '{3 mharc: 2 mharc + 1 mharc}'),
            ('2', 'bi', '(b) (i) Conas a léirigh Henry Gore‐Booth go raibh sé báúil lena thionóntaí nuair a bhí gorta ag bagairt orthu sa bhliain 1879? (Alt 2)', '(b) (i) Conas a léirigh Henry', 2, None, '{2 mharc}'),
            ('2', 'bii', '(ii) Cén fáth nach raibh Constance ábalta cúrsa ealaíne a dhéanamh i dtús báire? (Alt 2)', '(ii) Cén fáth nach raibh Constance ábalta', 2, None, '{2 mharc}'),
            ('3', 'a', '(a) Cén dearcadh polaitiúil a léirigh Constance ina céad óráid phoiblí? (Alt 3)', '3. (a) Cén dearcadh polaitiúil', 3, None, '{3 mharc}'),
            ('3', 'bi', '(b) (i) Luaigh sampla amháin a léiríonn go raibh Constance agus a fear céile gníomhach i saol cultúrtha Bhaile Átha Cliath. (Alt 3)', '(b) (i) Luaigh sampla amháin a léiríonn', 2, None, '{2 mharc}'),
            ('3', 'bii', '(ii) Cén fáth a raibh náisiúnaithe ag agóidíocht in Éirinn ag an am sin? (Alt 3)', '(ii) Cén fáth a raibh náisiúnaithe', 2, None, '{2 mharc}'),
            ('4', 'a', '(a) Scríobh síos dhá phointe eolais faoi pháirt Constance Markievicz san fheachtas náisiúnach roimh 1913. (Alt 4)', '4. (a) Scríobh síos dhá phointe eolais faoi pháirt', 3, 'ordered', '{3 mharc: 2 mharc + 1 mharc}'),
            ('4', 'bi', '(b) (i) Cad a rinne Constance sa Fhrithdhúnadh sa bhliain 1913? (Alt 4)', '(b) (i) Cad a rinne Constance sa Fhrithdhúnadh', 2, None, '{2 mharc}'),
            ('4', 'bii', '(ii) Cén pionós a gearradh ar Constance nuair a gabhadh í tar éis Éirí Amach na Cásca 1916? (Alt 4)', '(ii) Cén pionós a gearradh', 2, None, '{2 mharc}'),
            ('5', 'a', '(a) Scríobh síos dhá rud faoi cheapadh na mban mar airí rialtais in Éirinn. (Alt 5)', '5. (a) Scríobh síos dhá rud faoi cheapadh', 3, 'ordered', '{3 mharc: 2 mharc + 1 mharc}'),
            ('5', 'bi', '(b) (i) Cad a dúirt Spéicéir na Parlaiminte in Westminster ag an ócáid chomórtha in ómós do Constance Markievicz i mí Iúil seo caite? (Alt 5)', '(b) (i) Cad a dúirt Spéicéir', 2, None, '{2 mharc}'),
            ('5', 'bii', '(ii) Cén cuspóir atá ag Cácas Parlaiminte na mBan? (Alt 5)', '(ii) Cén cuspóir atá ag Cácas', 2, None, '{2 mharc}'),
            ('6', 'a', '(a) Aimsigh sampla den bhriathar saor san Aimsir Chaite in Alt 2 agus sampla de bhriathar sa Mhodh Coinníollach in Alt 5.', '6. (a) Aimsigh sampla den bhriathar saor san Aimsir Chaite', 3, 'grammar', '{3 mharc: 2 mharc + 1 mharc}'),
            ('6', 'b', '(b) Bunaithe ar an eolas sa sliocht thuas, luaigh dhá thréith a bhain le Constance Markievicz, dar leat. Aimsigh sampla amháin de gach ceann den dá thréith sin sa sliocht. (Bíodh an freagra, i d’fhocail féin. Is leor 60 focal.)', '(b) Bunaithe ar an eolas sa sliocht thuas, luaigh dhá thréith', 12, 'traits', '{6 mharc + 6 mharc}')]),
        'B': dict(title='Taighde agus Taiscéalaíocht sa Spás', pages=[6, 7], topic='irish-3-1', end='C1 (2) + P1 (4) = C2 (2) + P2 (4) =', parts=[
            ('1', 'a', '(a) Rinneadh éacht ceannródaíoch ar an 20 Iúil 1969. Tabhair dhá phointe eolais faoin éacht sin. (Alt 1)', '1. (a) Rinneadh éacht ceannródaíoch', 3, 'ordered', '{3 mharc: 2 mharc + 1 mharc}'),
            ('1', 'bi', '(b) (i) Scríobh síos rud amháin faoi lucht féachana na teilifíse an oíche stairiúil sin. (Alt 1)', '(b) (i) Scríobh síos rud amháin faoi lucht féachana', 2, None, '{2 mharc}'),
            ('1', 'bii', '(ii) Cad iad na chéad fhocail a dúirt Neil Armstrong ar an ngealach? (Alt 1)', '(ii) Cad iad na chéad fhocail', 2, None, '{2 mharc}'),
            ('2', 'a', '(a) Cén fáth ar thosaigh spásrás i lár na gcaogaidí? (Alt 2)', '2. (a) Cén fáth ar thosaigh spásrás', 3, None, '{3 mharc}'),
            ('2', 'bi', '(b) (i) Cad a d’éirigh leis an Rúiseach, Yuri Gagarin, a dhéanamh sa bhliain 1961? (Alt 2)', '(b) (i) Cad a d’éirigh leis an Rúiseach', 2, None, '{2 mharc}'),
            ('2', 'bii', '(ii) Cad a d’fhógair an tUachtarán, John F. Kennedy, sa bhliain 1961? (Alt 2)', '(ii) Cad a d’fhógair an tUachtarán', 2, None, '{2 mharc}'),
            ('3', 'a', '(a) Tabhair dhá chúis a bhfuil borradh faoin taiscéalaíocht sa spás faoi láthair. (Alt 3)', '3. (a) Tabhair dhá chúis a bhfuil borradh', 3, 'ordered', '{3 mharc: 2 mharc + 1 mharc}'),
            ('3', 'bi', '(b) (i) Cad atá ar siúl ag an tuirlingeoir róbatach, InSight, faoi láthair? (Alt 3)', '(b) (i) Cad atá ar siúl ag an tuirlingeoir', 2, None, '{2 mharc}'),
            ('3', 'bii', '(ii) Cad a rinne Chang’e‐4 ar an 3 Eanáir i mbliana? (Alt 3)', '(ii) Cad a rinne Chang’e-4', 2, None, '{2 mharc}'),
            ('4', 'a', '(a) Scríobh síos dhá phointe eolais faoin Stáisiún Spáis Idirnáisiúnta a cuireadh amach sa spás den chéad uair sa bhliain 1998. (Alt 4)', '4. (a) Scríobh síos dhá phointe eolais faoin Stáisiún', 3, 'ordered', '{3 mharc: 2 mharc + 1 mharc}'),
            ('4', 'bi', '(b) (i) Cén bhaint atá ag ÉireComposites le Gníomhaireacht Spáis na hEorpa? (Alt 4)', '(b) (i) Cén bhaint atá ag ÉireComposites', 2, None, '{2 mharc}'),
            ('4', 'bii', '(ii) Cén tionscadal atá ar siúl faoi choimirce Choláiste na hOllscoile, Baile Átha Cliath, faoi láthair? (Alt 4)', '(ii) Cén tionscadal atá ar siúl', 2, None, '{2 mharc}'),
            ('5', 'a', '(a) Luaigh dhá shlí a mbaintear tairbhe as na satailítí. (Alt 5)', '5. (a) Luaigh dhá shlí', 3, 'ordered', '{3 mharc: 2 mharc + 1 mharc}'),
            ('5', 'bi', '(b) (i) Cén chaoi a bhfuil taighde an spáis ag dul i bhfeidhm ar chúrsaí éadaí? (Alt 5)', '(b) (i) Cén chaoi a bhfuil taighde', 2, None, '{2 mharc}'),
            ('5', 'bii', '(ii) Cén locht a fhaightear ar an taiscéalaíocht sa spás uaireanta? (Alt 5)', '(ii) Cén locht a fhaightear', 2, None, '{2 mharc}'),
            ('6', 'a', '(a) Aimsigh sampla den bhriathar saor san Aimsir Fháistineach in Alt 1 agus sampla d’ainmfhocal baininscneach sa tuiseal ginideach uatha in Alt 3.', '6. (a) Aimsigh sampla den bhriathar saor san Aimsir Fháistineach', 3, 'grammar', '{3 mharc: 2 mharc + 1 mharc}'),
            ('6', 'b', '(b) Bunaithe ar an eolas sa sliocht thuas, déan plé, i d’fhocail féin, ar dhá chúis ar scríobh an t‐údar an sliocht seo. (Is leor 60 focal.)', '(b) Bunaithe ar an eolas sa sliocht thuas, déan plé, i d’fhocail féin, ar dhá chúis', 12, 'reasons', 'Dhá chúis = 6 mharc + 6 mharc')]),
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
    # 2019 prices no reading part "{2 mharc: 1 mharc + 1 mharc}": no one-mark answer slots this year.
    assert '1 mharc + 1 mharc}' not in s.text[:s.text.index('Ceist 2 PRÓS (30 marc)')]
    note5 = s.chunk('Nóta: I gcás na gceisteanna 2 (Prós)', 'Nóta: Níl na nótaí tacaíochta seo uileghabhálach')[0]
    notes = s.chunk('Nóta: Níl na nótaí tacaíochta seo uileghabhálach', 'Freagair Ceist 2A (Prós Ainmnithe)')[0]
    gaeilge_table = GAEILGE_TABLE.search(s.text, s.page(33)).group(0)
    # The prose and additional-literature band tables print the Eolas and Gaeilge columns side by side: 2A's (PDF 27)
    # and 4A's (PDF 36) inside the answer, 2B's after its marking-panel note (PDF 30). 2A's and 2B's copies differ by
    # one full stop, so each card carries its own.
    prose_table_a = s.chunk('Catagóir Eolas (25 marc) Gaeilge (5 mharc)', 'Nótaí tacaíochta:', s.page(27))[0]
    prose_table_b = s.chunk('Catagóir Eolas (25 marc) Gaeilge (5 mharc)', 'Ceist 3 FILÍOCHT (30 marc)', s.page(30))[0]
    table35 = s.chunk('Catagóir Eolas (35 marc) Gaeilge (5 mharc)', 'Nótaí tacaíochta:', s.page(36))[0]
    general4 = s.chunk('Treoracha: Iarrtar ar na hiarrthóirí plé a dhéanamh ar an ráiteas', 'Eolas (35) = Gaeilge (5) = C4 (40) =', s.page(36))[0]
    assert all(x in gaeilge_table for x in ['Sárchumas', 'Cumas lag/an-lag'])
    for table in (prose_table_a, prose_table_b):
        assert '22-25' in table and table.endswith('deilbhíocht) 1'), table[-60:]
    assert '30-35' in table35 and '0-13' in table35 and table35.endswith('deilbhíocht) 1') and general4.endswith('sa fhreagarleabhar.')
    assert note5.endswith('ar Ghaeilge.') and notes.endswith('atá iontu.')
    return dict(paper=paper, texts=texts, s=s, general=general, passages=passages, note5=note5, notes=notes,
                gaeilge_table=gaeilge_table, prose_table_a=prose_table_a, prose_table_b=prose_table_b, table35=table35,
                general4=general4, decisions=selection_decisions(paper))


READING_REQUIREMENTS = ['Léigh an sliocht iomlán a ghabhann leis an gceist. Freagair an chuid atá luaite ar an gcárta.',
                        'Úsáid an t-alt a luaitear. Glacfar le focail an tsleachta nó le do chuid focal féin, ach ní mór 6(b) a fhreagairt i d’fhocail féin.']
WHOLE_REQUIREMENTS = ['Léigh an sliocht oifigiúil a ghabhann leis an gceist.', 'Freagair gach fochuid agus cloígh leis an alt a luaitear.',
                      'Bain úsáid as do chuid focal féin nuair a iarrtar ort é.']
LIT_REQUIREMENTS = ['Freagair gach cuid den cheist atá priontáilte.', 'Úsáid tagairtí cruinne agus ábhartha don téacs.']
PART_NOTE = ('SEC allocation for this task. Alternative correct answers in the scheme are answers to one task, not extra task routes. '
             'Whole questions and their practice parts are overlapping exercises; their marks are not added to infer the paper total.')
LABELS = {'a': '(a) Freagra', 'bi': '(b)(i) Freagra', 'bii': '(b)(ii) Freagra', 'grammar': '(a) Freagra',
          'trait-1': '(b) Tréith 1', 'trait-2': '(b) Tréith 2', 'reason-1': '(b) Cúis 1', 'reason-2': '(b) Cúis 2'}
# The two 6-mark halves of 6(b): (criterion id prefix, label, English practice focus).
HALVES = {'traits': ('trait', 'Tréith', 'One of the two traits, discussed with one example from the extract in your own words (trait {slot}, 6 marks)'),
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


def around_table(s, start, page, table):
    """A prose answer to its marking-panel note, as the lines either side of the band table it stores: the table is
    given once on its own, and nothing printed apart is joined ("Eolas = 25 marc" on one side, "Nótaí tacaíochta:" on
    the other side of 2A's table)."""
    whole, spages = s.chunk(start, PANEL, s.page(page))
    lines = [clean(part) for part in whole.split(table)] if table in whole else [whole]
    assert len(lines) <= 2 and all(lines) and not any('Gaeilge (5 mharc)' in line or 'Eolas (25) =' in line for line in lines), start
    return lines, spages

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
            id=f'irish-2019-hl-p2-{slug}', year=2019, level='higher', paper=2, section='2',
            atlasQuestionId=key, questionRef=f'2019 HL Paper 2 {ref}', questionText=prompt,
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
    six_b = {'A': '6(b) prices two traits, 6 marks each (naming the trait 2 + an example of it from the passage 4), in the candidate’s own words.',
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
        ('P-2A', 'prose-2a', 'Prós 2A · Dís', 'irish-4-4', '2A. Prós Ainmnithe', 27, m['prose_table_a'],
         head2 + '\n2A. Prós Ainmnithe',
         'Freagair an cheist thíos ar an ngearrscéal Dís.\n\nDís\n'
         '“Tá léiriú sa ghearrscéal Dís ar shaol agus ar mheon bhean Sheáin.”\nDéan plé ar an ráiteas sin. (30 marc)'),
        ('P-2B', 'prose-2b', 'Prós 2B · Gearrscéal roghnach', 'irish-4-7', '2B. Prós Roghnach', 30, m['prose_table_b'],
         head2 + '\n2B. Prós Roghnach\nNíl cead aon ábhar a bhaineann le Prós Ainmnithe a úsáid i bhfreagra ar an bPrós Roghnach.',
         'Maidir le gearrscéal roghnach a ndearna tú staidéar air le linn do chúrsa, ainmnigh an príomhcharachtar '
         '(an phríomhphearsa) sa ghearrscéal sin. Déan plé ar an léargas a thugtar dúinn ar shaol agus ar mheon an duine sin '
         'ó thús deireadh an ghearrscéil.\n\n'
         'Ní mór teideal an ghearrscéil sin, mar aon le hainm an údair, a scríobh síos go cruinn. (30 marc)'),
    ]
    for key, slug, ref, topic, start, page, table, stem, prompt in prose:
        for line in [*stem.splitlines(), *prompt.splitlines()]:
            if line:
                assert in_order(line, texts[7]), (key, line)
        # 2A's band table is stored inside its answer (PDF 27); 2B's own copy follows its marking-panel note (PDF 30).
        lines, spages = around_table(s, start, page, table)
        assert 'Eolas = 25 marc' in lines[0] and not any('Catagóir Eolas (25 marc)' in line for line in lines), key
        add(key, slug, ref, prompt, topic, [8], sorted(set(spages) | {page}),
            [criterion('eolas', 'Eolas', 25, [*lines, table, m['notes']], 'indicative'), gaeilge()], LIT_REQUIREMENTS,
            'One complete SEC response: 25 Eolas and a single shared 5-mark Gaeilge award. Supporting notes are indicative rather than exhaustive. '
            'The printed band table gives the Eolas and Gaeilge columns side by side.',
            source=('Prós', ref.split(' · ', 1)[1], [8]), stem=stem)

    poems = [
        ('F-3A', 'poetry-3a', 'Filíocht 3A · An tEarrach Thiar', 'irish-5-3', '3A. Filíocht Ainmnithe', 31, head3 + '\n3A. Filíocht Ainmnithe', [
            '(i) “Cuimhní an fhile ar nósanna a bhain le saol an oileáin ina óige atá sa dán An tEarrach Thiar (thíos).” É sin a phlé. (15 mharc)',
            '(ii) Cén mothúchán is mó a mhúsclaíonn an dán seo ionat féin? (Is leor pointe amháin eolais as an dán mar thacaíocht le do fhreagra.) (6 mharc)',
            '(iii) Cé a chum an dán seo? Scríobh nóta gairid ar shaol agus ar shaothar an fhile sin. (9 marc)'],
         ['(ii) Cén mothúchán is mó', '(iii) Cé a chum an dán seo?'], 32),
        ('F-3B', 'poetry-3b', 'Filíocht 3B · Dán roghnach', 'irish-5-6', '3B. Filíocht Roghnach', 34,
         head3 + '\n3B. Filíocht Roghnach\nNíl cead aon ábhar a bhaineann le Filíocht Ainmnithe a úsáid i bhfreagra ar an bhFilíocht Roghnach.', [
            '(i) Maidir le dán nua‐aimseartha roghnach a ndearna tú staidéar air le linn do chúrsa, scríobh síos príomhthéama an dáin. Déan plé ar an léiriú a thugtar ar an bpríomhthéama sin ó thús deireadh an dáin. (15 mharc)',
            '(ii) Cén mothúchán is mó a mhúsclaíonn an dán seo ionat féin? (Is leor pointe amháin eolais as an dán mar thacaíocht le do fhreagra.) (6 mharc)',
            '(iii) Cé a chum an dán seo? Scríobh nóta gairid ar shaol agus ar shaothar an fhile sin. (9 marc)'],
         ['(ii) Cén mothúchán is mó', '(iii) Cé a chum an dán seo?'], None),
    ]
    for key, slug, ref, topic, start, page, stem, parts, cuts, marc4_page in poems:
        for line in [*stem.splitlines(), *parts]:
            assert in_order(line, texts[8]), (key, line[:40])
        whole, spages = literature_answer(s, start, page)
        pieces = split_parts(whole, cuts, ['Eolas = 13 mharc', 'Eolas = 5 mharc', 'Eolas = 7 marc'])
        # (i)'s band table is printed in place: 3A's "Cur síos (13 mharc)", 3B's "Marc as 11".
        table_i = CUR_SIOS_TABLE.search(pieces[0]).group(0) if marc4_page else MARC11_TABLE
        assert table_i in pieces[0] and table_i not in pieces[1] + pieces[2], key
        if marc4_page:
            # 3A: the Marc as 4 table of (ii)'s point is stored after the marking-panel note at the foot of PDF 32.
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
         '4A. An Triail\n“Creideann go leor de na carachtair (na pearsana) sa dráma An Triail nach bhfuil aon mhilleán orthu féin faoi thragóid an chailín óig, Máire Ní Chathasaigh.”\nDéan plé ar an ráiteas sin. (40 marc)'),
        ('X-4B', 'literature-4-b', '4B. A Thig Ná Tit Orm', 'irish-6-1', '4B. A Thig Ná Tit Orm', '4C. Tóraíocht Dhiarmada',
         '4B. A Thig Ná Tit Orm\n“Sa dírbheathaisnéis A Thig Ná Tit Orm, tugann Maidhc Dainín cuntas spéisiúil dúinn ar eachtraí a óige agus ar shaol a mhuintire nuair a bhí sé ag fás aníos sa Ghaeltacht.”\nDéan plé ar an ráiteas sin. (40 marc)'),
        ('X-4C', 'literature-4-c', '4C. Tóraíocht Dhiarmada agus Ghráinne', 'irish-6-2', '4C. Tóraíocht Dhiarmada', '4D. Gafa',
         '4C. Tóraíocht Dhiarmada agus Ghráinne\n“An choimhlint idir na príomhcharachtair (na príomhphearsana), Fionn, Diarmaid agus Gráinne, agus a mianta éagsúla is cúis leis an teannas sa Tóraíocht.”\nDéan plé ar an ráiteas sin. (40 marc)'),
        ('X-4D', 'literature-4-d', '4D. Gafa', 'irish-6-3', '4D. Gafa', '4E. Canary Wharf',
         '4D. Gafa\n“Is iad na bréaga agus an mhímhacántacht sa chaidreamh idir na carachtair (na pearsana) éagsúla is cúis le cuid mhór de na deacrachtaí sa teaghlach sa sliocht as an úrscéal Gafa.”\nDéan plé ar an ráiteas sin. (40 marc)'),
        ('X-4E', 'literature-4-e', '4E. Canary Wharf', 'irish-6-4', '4E. Canary Wharf', '4F. Dánta Breise',
         '4E. Canary Wharf\n“Sa scéal Mil, tugtar léiriú éifeachtach dúinn ar iompar na beirte, Meagan agus Deibí, agus ar an gcasadh gan choinne ag deireadh an scéil.”\nDéan plé ar an ráiteas sin. (40 marc)'),
    ]
    for key, slug, ref, topic, start, end, prompt in options:
        assert all(in_order(line, texts[9]) for line in prompt.splitlines()), key
        chunk, spages = s.chunk(start, end, s.page(36))
        lines = [chunk]
        if key == 'X-4A':
            # 4A's answer carries the section's 35-mark band table (PDF 36); it is the section's, given once below. The text
            # before and after it stays two lines: nothing printed apart is joined.
            before, after = chunk.split(m['table35'])
            lines = [clean(before), clean(after)]
        assert 'Eolas = 35 marc' in lines[0] and not any('Gaeilge (5 mharc)' in line or 'Catagóir Eolas (35 marc)' in line for line in lines), key
        add(key, slug, f'Litríocht {ref}', head4 + '\n\n' + prompt, topic, [10], sorted(set(spages) | {36}),
            [criterion('eolas', 'Eolas', 35, [*lines, m['general4'], m['table35']], 'indicative'), gaeilge()], LIT_REQUIREMENTS,
            'One complete SEC response: Eolas 35 assessed as a unit with a single shared 5-mark Gaeilge award. Supporting notes are indicative rather than exhaustive.')
    whole, spages = literature_answer(s, '4F. Dánta Breise – Colmáin', 41)
    pieces = split_parts(whole, ['(ii) A bhfuil i gceist leis na línte seo a mhíniú', '(iii) Cén tábhacht'],
                         ['Eolas = 19 marc', 'Míniú = 7 marc', 'Eolas = 9 marc'])
    assert EOLAS19_TABLE.search(pieces[0]) and not EOLAS19_TABLE.search(pieces[1] + pieces[2])
    # The Marc as 7 table prices (ii)'s 7-mark explanation; the text layer stores it after (iii)'s notes, before (iii)'s
    # own Marc as 5 / Marc as 4 table for its two points (5 + 4).
    assert MARC7_TABLE in pieces[2] and MARC7_TABLE not in pieces[1] and MARC54_TABLE in pieces[2]
    pieces[2] = clean(pieces[2].replace(MARC7_TABLE, ' '))
    pieces[1] = clean(pieces[1] + ' ' + MARC7_TABLE)
    f_prompt = ('4F. Dánta Breise – Colmáin\nFreagair (i), (ii) agus (iii) thíos.\n'
                '(i) Tugann an file léiriú dúinn ar iompar an chait agus ar chríoch thragóideach an chait sa dán Colmáin (thall).\nDéan plé ar an ráiteas sin. (20 marc)\n'
                '(ii) A bhfuil i gceist leis na línte seo a mhíniú:\nNí fhaca sé a mhacasamhail féin ariamh,\ncat dá dhéanamh, dá dhath, dá dhreach.\n'
                'Ní fhaca sé ach daoine agus colmáin ar an aoirdeacht. (10 marc)\n'
                '(iii) Cén tábhacht, dar leat, a bhaineann leis na colmáin sa dán? Is leor dhá phointe eolais.\nBíodh tagairtí cruinne agat do théacs an dáin i do fhreagra. (10 marc)')
    assert all(in_order(line, texts[9]) for line in f_prompt.splitlines())
    add('X-4F', 'literature-4-f', 'Litríocht 4F · Dánta Breise – Colmáin', head4 + '\n\n' + f_prompt, 'irish-6-9', [10, 11],
        sorted(set(spages) | {36}),
        [criterion('eolas-i', '(i) Eolas', 19, [pieces[0], m['general4']], 'indicative'), criterion('eolas-ii', '(ii) Eolas', 7, [pieces[1]], 'indicative'),
         criterion('eolas-iii', '(iii) Eolas', 9, [pieces[2]], 'indicative'), gaeilge()], LIT_REQUIREMENTS,
        'One complete SEC response: the paper prints (i) 20, (ii) 10 and (iii) 10; the scheme assesses Eolas 19, 7 and 9 (two points, 5 + 4) '
        'plus one shared 5-mark Gaeilge award. Supporting notes are indicative rather than exhaustive.',
        source=('Dánta Breise', 'Colmáin', [10, 11]))

    reading = [c for c in cards if '-reading-' in c['id']]
    literature = [c for c in cards if '-reading-' not in c['id']]
    assert len(reading) == 50 and len(literature) == 10, (len(reading), len(literature))
    assert len({c['id'] for c in cards}) == len(cards) == 60 and len({c['atlasQuestionId'] for c in cards}) == 60
    assert sum(c['totalMarks'] for c in cards if re.fullmatch(r'R-[AB]-\d', c['atlasQuestionId'])) == 100
    for card in cards:
        assert sum(c['maxMarks'] for c in card['criteria']) == card['totalMarks'], card['id']
        for c in card['criteria']:
            assert c['guidance'] and all(not re.search('[-]', g) for g in c['guidance']), (card['id'], c['id'])
            assert all(h not in g for h in FURNITURE for g in c['guidance']), (card['id'], c['id'])
    sr = json.loads(SOURCE_REVIEW.read_text())
    whole = [c['id'] for c in reading if re.fullmatch(r'R-[AB]-\d', c['atlasQuestionId'])]
    review = dict(year=2019, level='higher', paperFileid=FILE + '.pdf', schemeFileid=SCHEME_FILE + '.pdf',
                  paperSha256=PAPER_SHA, schemeSha256=SCHEME_SHA,
                  reviewedPaperPages=list(range(1, 13)), reviewedSchemePages=sr['reviewedSchemePages'], schemeScope=sr['schemeScope'],
                  reviewDate=REVIEWED_AT, status='reviewed', fullPaperAndApplicableSchemeVisualSweep=True, selectionDecisions=m['decisions'],
                  readingWholeCardIds=whole, readingPracticeCardIds=[c['id'] for c in reading if c['id'] not in whole],
                  literatureRouteCardIds=[c['id'] for c in literature],
                  examStructure=dict(readingA=50, readingB=50, prose=30, poetry=30, additionalLiterature=40, total=200),
                  nonPoolDecisions=sr['nonPoolDecisions'], openIssues=[], caveats=sr['sourceFindings'],
                  boundaries='12 whole reading questions with 34 published parts and 4 six-mark 6(b) slots (2019 prices no part 1 + 1); '
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
    print(f"Irish Higher 2019 Paper 2: {len(data['cards'])} reviewed reading and literature cards; the archive remains incomplete.")


if __name__ == '__main__':
    main()
