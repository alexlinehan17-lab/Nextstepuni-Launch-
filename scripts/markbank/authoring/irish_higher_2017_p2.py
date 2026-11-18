#!/usr/bin/env python3
"""Reviewed 2017 Higher Paper 2 (Léamhthuiscint agus Litríocht): new cards, no legacy component.

Paper PDF 1–12 (page 3 the Treoracha, 4–7 the two reading passages with their questions,
8 prose, 9 poetry with Géibheann, 10 additional literature, 11 the poem Éiceolaí, 12 blank)
and the Paper 2 pages of the combined LC001ALP000IV scheme (PDF 16–30, plus 31 modified
marking) reviewed on 2026-11-04. Counts are assertions, not corpus-completeness proof.

The card shapes follow the reviewed 2018–2026 Higher Paper 2 components: every printed
reading question is a whole card with one criterion per published part, each published
part is also a practice card, two independent one-mark answers expose their own slots
(A 1(b)(i) and B 2(b)(i), both priced 1 mharc + 1 mharc), order-dependent 2 + 1 items stay
whole, and the two 6-mark halves of A 6(b) (two reasons) expose their own slots. B 6(b) is
the reaction-and-two-points shape of 2018 B 6(b): one part with the reaction 2 and points
5 + 5 as its criteria. B 4(a) is one 3-mark answer with printed partials (2 and 1), not a
2 + 1 pair. 2017 prints one prescribed and one optional prose text (2A the novel extract
Hurlamaboc, 2B an optional novel extract), one prescribed and one optional poem (3A
Géibheann, 3B an optional modern poem) and six Q4 options (4F Éiceolaí); each is one card
with its printed sub-questions as criteria and one shared 5-mark Gaeilge award.

2017's scheme prints no per-question band tables (2018–2020 print one under each prose and
Q4 answer and Gaeilge/Marc tables under the poems). Each literature answer is its question,
its "Eolas = N marc" line, its Treoir and any printed price split, ending at the examiner's
marking-panel note ("Nóta: Caithfidh an Scrúdaitheoir …"); Q4A–E print no "Eolas = 35 marc"
of their own (the Ceist 4 Treoracha price them: "an t-eolas a mharcáil as 35 marc"). The one
grading table the scheme prints, "Grádú Marcála sna Freagraí" (PDF 30: the Sármhaith,
An-mhaith, Maith and Measartha marks for every answer total from 200 to 5), is carried with
the 5-mark Gaeilge note on every literature card's Gaeilge criterion. Boxed headings are
removed by exact match.
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
OUT = ROOT / 'components/MarkBank/cards/irish/higher-2017-p2-authored.json'
SOURCE_REVIEW = ROOT / 'scripts/markbank/authored/irish-higher-2017-p2-source-review.json'
REVIEWED_AT = '2026-11-04'
PAPER_SHA = '203ab3a6525f27ff42afa31f69250ff6342e78a392c4fe919abc4feab442eaaf'
SCHEME_SHA = '89b6756b0744f1389252008b8093e7f9dbb1043c0bacdb95810d3e5ffa7526df'
DIRECTIVE = re.compile(r'rogha|roghna|Freagair|Luaigh|Ainmnigh|\bnó\b|dhá phointe|dhá rud|dhá bh|dhá dh|dhá ch|dhá fh|dhá th|'
                       r'ceann amháin|pointe amháin|\bdhá\b|an dá\b|amháin', re.I)
SOURCE_NOTE = 'Shown page-for-page from the official examination paper; swipe to move between pages.'
# Boxed page headings the 2017 text layer stores inside the literature pages; exact strings only.
FURNITURE = ('– PRÓS AINMNITHE nó PRÓS ROGHNACH – (30 marc)', '– FILÍOCHT AINMNITHE nó FILÍOCHT ROGHNACH – (30 marc)',
             '– LITRÍOCHT BHREISE – (40 marc)')
# The examiner's marking-panel note that closes each prose and poetry answer: the boundary of the answer's own text.
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


def printed_values(chunk, marks):
    # The marks a single-answer part can earn: 0, the full tariff and every partial the scheme prints for it.
    values = re.findall(r'= (\d+) mh?arc', chunk) + re.findall(r'bronntar (\d+) mh?arc', chunk) + re.findall(r'\((\d+) mh?arc\)', chunk)
    values += [int(a) - int(b) for a, b in re.findall(r'easnamhach \((\d+)-(\d+)\)', chunk)]
    return sorted({0, marks} | {int(v) for v in values if int(v) <= marks})


def material():
    import fitz
    paper_path = ROOT / f'paper-trail-corpus/exampapers/2017/{FILE}.pdf'
    scheme_path = ROOT / f'paper-trail-corpus/markingschemes/2017/{SCHEME_FILE}.pdf'
    assert hashlib.sha256(paper_path.read_bytes()).hexdigest() == PAPER_SHA, 'Paper changed: repeat visual review'
    assert hashlib.sha256(scheme_path.read_bytes()).hexdigest() == SCHEME_SHA, 'Scheme changed: repeat visual review'
    paper, doc = fitz.open(paper_path), fitz.open(scheme_path)
    texts = [clean(p.get_text()) for p in paper]
    s = Scheme(doc, 16, 30)
    # The marking instructions, from their first rule (their heading "Treoracha do mharcáil na léamhthuisceana" is a title)
    # to the boxed section heading that the text layer stores after them.
    general = s.chunk('Tá Ceist 1 – 5 ar cómharc', 'Páipéar II (200 marc)')[0]
    assert general.endswith('sa fhreagarleabhar.'), general[-60:]
    # (q, part, paper prompt, scheme anchor, marks, mode, printed tariff). Each passage ends where the examiner's
    # marking panel for 6(b) begins ("C(1) (2) + P1 (4) = …", "Tuairim = 2 mharc … Ceist 6 (b) (12) =").
    passages = {
        'A': dict(title='TG4 – Fiche Bliain ag Fás', pages=[4, 5], topic='irish-3-0', end='C(1) (2) + P1 (4) = C(2) (2) + P2 (4) =', parts=[
            ('1', 'a', '(a) Cén fáth a raibh bunú Theilifís na Gaeilge ina chéim mhór chun cinn don Ghaeilge? Tabhair dhá phointe eolais. (Alt 1)', '1. (a) Cén fáth a raibh bunú Theilifís na Gaeilge', 3, 'ordered', '{3 mharc: 2 mharc + 1 mharc}'),
            ('1', 'bi', '(b) (i) Scríobh síos dhá cheann de na hábhair chomhrá a bhí ag na haíonna ar an gclár speisialta. (Alt 1)', '(b) (i) Scríobh síos dhá cheann de na hábhair chomhrá', 2, 'slots', '{1 mharc + 1 mharc = 2 mharc}'),
            ('1', 'bii', '(ii) Conas a samhlaíodh obair TG4 ar an gclár speisialta? (Alt 1)', '(ii) Conas a samhlaíodh obair TG4', 2, None, '{2 mharc}'),
            ('2', 'a', '(a) Tabhair dhá chúis ar éirigh pobal na Gaeilge míshásta leis an tseirbhís Ghaeilge a bhí ar fáil ar Theilifís Éireann. (Alt 2)', '2. (a) Tabhair dhá chúis ar éirigh pobal na Gaeilge', 3, 'ordered', '{3 mharc: 2 mharc + 1 mharc}'),
            ('2', 'bi', '(b) (i) Cén tuiscint nua a bhí ag teacht chun cinn ó dheireadh na seascaidí ar aghaidh? (Alt 2)', '(b) (i) Cén tuiscint nua', 2, None, '{2 mharc}'),
            ('2', 'bii', '(ii) Conas a chabhraigh an tseirbhís nua teilifíse S4C le stádas na Breatnaise? (Alt 2)', '(ii) Conas a chabhraigh an tseirbhís nua teilifíse S4C', 2, None, '{2 mharc}'),
            ('3', 'a', '(a) Tabhair dhá phointe eolais faoin mbaint lárnach a bhí ag Micheál D. Ó hUiginn le bunú an stáisiúin. (Alt 3)', '3. (a) Tabhair dhá phointe eolais faoin mbaint lárnach', 3, 'ordered', '{3 mharc: 2 mharc + 1 mharc}'),
            ('3', 'bi', '(b) (i) Cén tábhacht a bhaineann le TG4 i saol na Gaeilge, dar leis an Uachtarán? Tabhair pointe amháin eolais. (Alt 3)', '(b) (i) Cén tábhacht a bhaineann le TG4', 2, None, '{2 mharc}'),
            ('3', 'bii', '(ii) Cad atá riachtanach má tá an Ghaeilge le buanú, dar leis an Uachtarán? (Alt 3)', '(ii) Cad atá riachtanach', 2, None, '{2 mharc}'),
            ('4', 'a', '(a) Luaigh dhá phointe eolais faoi na cláir nuachta a thaispeántar ar TG4. (Alt 4)', '4. (a) Luaigh dhá phointe eolais faoi na cláir nuachta', 3, 'ordered', '{3 mharc: 2 mharc + 1 mharc}'),
            ('4', 'bi', '(b) (i) Cén bhaint a bhí ag TG4 leis an bhfeachtas olltoghchánaíochta a bhí ar siúl sa bhliain 2011? (Alt 4)', '(b) (i) Cén bhaint a bhí ag TG4', 2, None, '{2 mharc}'),
            ('4', 'bii', '(ii) Cén cuntas spéisiúil a thug Hector sa tsraith Hector Central, a craoladh an geimhreadh seo caite? (Alt 4)', '(ii) Cén cuntas spéisiúil a thug Hector', 2, None, '{2 mharc}'),
            ('5', 'a', '(a) Scríobh síos dhá bhua de chuid TG4 a mhol an tArd‐Stiúrthóir nua, Alan Esslemont. (Alt 5)', '5. (a) Scríobh síos dhá bhua de chuid TG4', 3, 'ordered', '{3 mharc: 2 mharc + 1 mharc}'),
            ('5', 'bi', '(b) (i) Cén dúshlán is mó atá roimh TG4, dar leis an Ard‐Stiúrthóir nua? (Alt 5)', '(b) (i) Cén dúshlán is mó atá roimh TG4', 2, None, '{2 mharc}'),
            ('5', 'bii', '(ii) Cén t‐athrú a thiocfaidh ar mhodhanna oibre TG4 feasta? (Alt 5)', '(ii) Cén t-athrú a thiocfaidh', 2, None, '{2 mharc}'),
            ('6', 'a', '(a) Aimsigh sampla den bhriathar saor san Aimsir Láithreach in Alt 1 agus sampla de bhriathar san Aimsir Fháistineach in Alt 5.', '6. (a) Aimsigh sampla den bhriathar saor san Aimsir Láithreach', 3, 'grammar', '{3 mharc: 2 mharc + 1 mharc}'),
            ('6', 'b', '(b) Bunaithe ar an eolas sa sliocht thuas, déan plé, i d’fhocail féin, ar dhá chúis ar scríobh an t‐údar an sliocht seo. (Is leor 60 focal.)', '(b) Bunaithe ar an eolas sa sliocht thuas, déan plé, i d’fhocail féin, ar dhá chúis', 12, 'reasons', 'Dhá chúis = 6 mharc + 6 mharc')]),
        'B': dict(title='An Cogadh sa tSiria agus Géarchéim na nDídeanaithe', pages=[6, 7], topic='irish-3-1',
                  end='Tuairim = 2 mharc Pointe eolais 1 = 5 mharc Pointe eolais 2 = 5 mharc Ceist 6 (b) (12) =', parts=[
            ('1', 'a', '(a) Luaigh dhá thoradh atá ar an gcogadh cathartha sa tSiria. (Alt 1)', '1. (a) Luaigh dhá thoradh', 3, 'ordered', '{3 mharc: 2 mharc + 1 mharc}'),
            ('1', 'bi', '(b) (i) Cén íomhá sna meáin a tharraing aird an domhain ar uafás an chogaidh chathartha seo? (Alt 1)', '(b) (i) Cén íomhá sna meáin', 2, None, '{2 mharc}'),
            ('1', 'bii', '(ii) Cad a deir an t‐údar faoi ghéarchéim na ndídeanaithe Siriacha? (Alt 1)', '(ii) Cad a deir an t-údar faoi ghéarchéim', 2, None, '{2 mharc}'),
            ('2', 'a', '(a) Tabhair dhá chúis ar thosaigh grúpaí éagsúla ag léirsiú in aghaidh Uachtarán na Siria, Bashar al‐Assad, sa bhliain 2011. (Alt 2)', '2. (a) Tabhair dhá chúis ar thosaigh grúpaí', 3, 'ordered', '{3 mharc: 2 mharc + 1 mharc}'),
            ('2', 'bi', '(b) (i) Scríobh síos dhá rud a deir na Náisiúin Aontaithe faoi dhaoine ar gach taobh den aighneas sa tSiria. (Alt 2)', '(b) (i) Scríobh síos dhá rud a deir na Náisiúin Aontaithe', 2, 'slots', '{1 mharc + 1 mharc}'),
            ('2', 'bii', '(ii) Tabhair pointe amháin eolais faoin tionchar atá ag an gcogaíocht chruálach ar phobal Aleppo. (Alt 2)', '(ii) Tabhair pointe amháin eolais faoin tionchar', 2, None, '{2 mharc}'),
            ('3', 'a', '(a) Luaigh dhá chonstaic a bhíonn le sárú ag na dídeanaithe agus iad ag iarraidh turas farraige a eagrú. (Alt 3)', '3. (a) Luaigh dhá chonstaic', 3, 'ordered', '{3 mharc: 2 mharc + 1 mharc}'),
            ('3', 'bi', '(b) (i) Scríobh síos fadhb amháin a bhíonn ag na dídeanaithe ag na hionaid seiceála ar na teorainneacha idir na tíortha éagsúla. (Alt 3)', '(b) (i) Scríobh síos fadhb amháin', 2, None, '{2 mharc}'),
            ('3', 'bii', '(ii) Tabhair pointe amháin eolais a léiríonn go bhfuil na cúinsí maireachtála go hainnis i gcampaí na ndídeanaithe. (Alt 3)', '(ii) Tabhair pointe amháin eolais a léiríonn', 2, None, '{2 mharc}'),
            ('4', 'a', '(a) Cén turas éachtach a rinne Nujeen Mustafa go dtí an Ghearmáin? (Alt 4)', '4. (a) Cén turas éachtach', 3, None, '{3 mharc}'),
            ('4', 'bi', '(b) (i) Cén fáth nach bhfuair Nujeen oideachas foirmiúil sa tSiria? (Alt 4)', '(b) (i) Cén fáth nach bhfuair Nujeen', 2, None, '{2 mharc}'),
            ('4', 'bii', '(ii) Cén mana atá ag Nujeen? (Alt 4)', '(ii) Cén mana atá ag Nujeen?', 2, None, '{2 mharc}'),
            ('5', 'a', '(a) Luaigh dhá phointe eolais faoin nGorta Mór in Éirinn. (Alt 5)', '5. (a) Luaigh dhá phointe eolais faoin nGorta Mór', 3, 'ordered', '{3 mharc: 2 mharc + 1 mharc}'),
            ('5', 'bi', '(b) (i) Cén teachtaireacht faoi na dídeanaithe a bhí ag George Clooney ina óráid? (Alt 5)', '(b) (i) Cén teachtaireacht faoi na dídeanaithe', 2, None, '{2 mharc}'),
            ('5', 'bii', '(ii) Luaigh an aidhm atá le Lá Domhanda na nDídeanaithe. (Alt 5)', '(ii) Luaigh an aidhm atá le Lá Domhanda', 2, None, '{2 mharc}'),
            ('6', 'a', '(a) Aimsigh sampla de bhriathar sa Mhodh Coinníollach in Alt 2 agus sampla d’ainmfhocal firinscneach sa tuiseal ginideach uatha in Alt 5.', '6. (a) Aimsigh sampla de bhriathar sa Mhodh Coinníollach', 3, 'grammar', '{3 mharc: 2 mharc + 1 mharc}'),
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
    note5 = s.chunk('Nóta: I gcás na gceisteanna 2 (Prós)', 'Freagair Ceist 2A (Prós Ainmnithe)')[0]
    gradu, gpages = s.chunk('Grádú Marcála sna Freagraí')
    general4 = s.chunk('Treoracha: Iarrtar ar na hiarrthóirí plé a dhéanamh ar an ráiteas', 'Eolas (35) = Gaeilge (5) =', s.page(27))[0]
    assert note5.endswith('ar Ghaeilge.') and gpages == [30] and general4.endswith('sa fhreagarleabhar.') and '35 marc' in general4
    # The grading table prices every total the answers use: its first block runs 200 … 18, its second 17 … 5.
    assert gradu.startswith('Grádú Marcála sna Freagraí Catagóir 200 160 100') and 'Catagóir 17 16 14 13 12 11 10 9 8 7 6 5' in gradu
    assert gradu.endswith('Measartha 7 7 6 6 5 5 4 4 4 3 3 2'), gradu[-60:]
    return dict(paper=paper, texts=texts, s=s, general=general, passages=passages, note5=note5, gradu=gradu, general4=general4,
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
        # "Tuairim a léiriú = 2 mharc / Pointe eolais 1 = 5 mharc / Pointe eolais 2 = 5 mharc" (B 6(b)), as 2018 B 6(b).
        return [criterion('opinion', 'Tuairim', 2, [chunk, general]), criterion('point-1', 'Pointe eolais 1', 5, [chunk]),
                criterion('point-2', 'Pointe eolais 2', 5, [chunk])]
    if mode in ('ordered', 'grammar'):
        return [criterion('grammar' if mode == 'grammar' else part, 'Freagra', marks, [chunk, general], permitted=[0, 2, 3])]
    if mode == 'slots':
        # "{1 mharc + 1 mharc (= 2 mharc)}": either answer alone earns 1, even where the accepted list prints no per-answer marks.
        return [criterion(part, 'Freagra', marks, [chunk, general], permitted=[0, 1, 2])]
    return [criterion(part, 'Freagra', marks, [chunk, general], permitted=printed_values(chunk, marks))]


def split_parts(whole, cuts, caps):
    i2 = whole.index(cuts[0]); i3 = whole.index(cuts[1], i2)
    pieces = [whole[:i2].strip(), whole[i2:i3].strip(), whole[i3:].strip()]
    for piece, cap in zip(pieces, caps):
        assert cap in piece, cap
    return pieces


def build():
    m = material()
    texts, s = m['texts'], m['s']
    cards = []

    def add(key, slug, ref, prompt, topic, pages, scheme_pages, criteria, requirements, note, extra_topics=None, source=None, **extra):
        cards.append(dict(
            id=f'irish-2017-hl-p2-{slug}', year=2017, level='higher', paper=2, section='2',
            atlasQuestionId=key, questionRef=f'2017 HL Paper 2 {ref}', questionText=prompt,
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
    slot_notes = {('A', '1'): 'The scheme prices the two answers 1 mharc + 1 mharc = 2 mharc independently; this card practises one of them. ',
                  ('B', '2'): 'The scheme prices the two things 1 mharc + 1 mharc independently; this card practises one of them. '}
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
                        READING_REQUIREMENTS, slot_notes[(letter, q)] + PART_NOTE,
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
    # 2017 prints no Gaeilge band table: the 5-mark Gaeilge note (PDF 24) and the scheme's one grading table (PDF 30) price it.
    gaeilge = lambda: criterion('gaeilge', 'Gaeilge', 5, [m['note5'], m['gradu']], 'quality')
    head2 = 'Freagair Ceist 2A (Prós Ainmnithe) nó Ceist 2B (Prós Roghnach) thíos.'
    head3 = 'Freagair Ceist 3A (Filíocht Ainmnithe) nó Ceist 3B (Filíocht Roghnach) thíos.'
    prose = [
        ('P-2A', 'prose-2a', 'Prós 2A · Hurlamaboc', 'irish-4-5', '2A. Prós Ainmnithe', 24,
         head2 + '\n2A. Prós Ainmnithe',
         'Freagair an cheist thíos faoin ngiota as an úrscéal Hurlamaboc.\n\n'
         '“Is bean í Lisín atá i gceannas ar a saol féin, ar a teaghlach agus ar a teach.”\nDéan plé ar an ráiteas sin. (30 marc)'),
        ('P-2B', 'prose-2b', 'Prós 2B · Úrscéal roghnach', 'irish-4-7', '2B. Prós Roghnach', 24,
         head2 + '\n2B. Prós Roghnach\nNíl cead aon ábhar a bhaineann le Prós Ainmnithe a úsáid i bhfreagra ar an bPrós Roghnach.',
         'Maidir leis an ngiota as an úrscéal roghnach a ndearna tú staidéar air le linn do chúrsa, ainmnigh an príomhcharachtar '
         '(an phríomhphearsa) sa ghiota. Déan plé ar an bpáirt atá ag an bpríomhcharachtar (ag an bpríomhphearsa) sin sa ghiota.\n\n'
         'Ní mór teideal an úrscéil sin, mar aon le hainm an údair, a scríobh síos go cruinn. (30 marc)'),
    ]
    for key, slug, ref, topic, start, page, stem, prompt in prose:
        for line in [*stem.splitlines(), *prompt.splitlines()]:
            if line:
                assert in_order(line, texts[7]), (key, line)
        answer, spages = s.chunk(start, PANEL, s.page(page))
        assert 'Eolas = 25 marc' in answer and 'Treoir:' in answer and 'Eolas (25) =' not in answer and spages == [page], key
        add(key, slug, ref, prompt, topic, [8], spages,
            [criterion('eolas', 'Eolas', 25, [answer], 'indicative'), gaeilge()], LIT_REQUIREMENTS,
            'One complete SEC response: 25 Eolas and a single shared 5-mark Gaeilge award. The scheme prints the Eolas mark and its Treoir; '
            'it prints no band table for the answer, and its one grading table (PDF 30) is shown with the Gaeilge award.',
            source=('Prós', ref.split(' · ', 1)[1], [8]), stem=stem)

    poems = [
        ('F-3A', 'poetry-3a', 'Filíocht 3A · Géibheann', 'irish-5-2', '3A. Filíocht Ainmnithe', 25, head3 + '\n3A. Filíocht Ainmnithe', [
            '(i) “Úsáideann an file codarsnacht shoiléir chun dhá phictiúr (íomhá) den ainmhí a chur os ár gcomhair sa dán Géibheann (thíos).” É sin a phlé. (15 mharc)',
            '(ii) Conas a chuaigh an dán seo i bhfeidhm ort? (Is leor pointe amháin eolais as an dán mar thacaíocht le do fhreagra.) (6 mharc)',
            '(iii) Cé a chum an dán seo? Scríobh nóta gairid ar shaol agus ar shaothar an fhile seo. (9 marc)']),
        ('F-3B', 'poetry-3b', 'Filíocht 3B · Dán nua-aimseartha roghnach', 'irish-5-6', '3B. Filíocht Roghnach', 26,
         head3 + '\n3B. Filíocht Roghnach\nNíl cead aon ábhar a bhaineann le Filíocht Ainmnithe a úsáid i bhfreagra ar an bhFilíocht Roghnach.', [
            '(i) Maidir le dán nua‐aimseartha roghnach a ndearna tú staidéar air le linn do chúrsa, cén príomhthéama atá sa dán, dar leat? Déan plé ar an gcaoi a gcuirtear an príomhthéama sin os ár gcomhair sa dán. (15 mharc)',
            '(ii) Conas a chuaigh an dán seo i bhfeidhm ort? (Is leor pointe amháin eolais as an dán mar thacaíocht le do fhreagra.) (6 mharc)',
            '(iii) Cé a chum an dán seo? Scríobh nóta gairid ar shaol agus ar shaothar an fhile seo. (9 marc)']),
    ]
    for key, slug, ref, topic, start, page, stem, parts in poems:
        for line in [*stem.splitlines(), *parts]:
            assert in_order(line, texts[8]), (key, line[:40])
        whole, spages = s.chunk(start, PANEL, s.page(page))
        assert spages == [page] and 'Eolas (25) =' not in whole, key
        pieces = split_parts(whole, ['(ii) Conas a chuaigh an dán seo i bhfeidhm ort?', '(iii) Cé a chum an dán seo?'],
                             ['Eolas = 13 mharc', 'Eolas = 5 mharc', 'Eolas = 7 marc'])
        # (ii) prices the reaction 1 + one point 4; (iii) the poet's name 1 + three points of life and work at 2 each.
        assert 'Mar a chuaigh an dán seo i bhfeidhm ort = 1 mharc' in pieces[1] and 'Pointe amháin eolais = 4 mharc' in pieces[1], key
        assert 'Saol agus saothar an fhile = 2 mharc + 2 mharc + 2 mharc = 6 mharc' in pieces[2], key
        add(key, slug, ref, '\n'.join(parts), topic, [9], spages,
            [criterion('eolas-i', '(i) Eolas', 13, [pieces[0]], 'indicative'), criterion('eolas-ii', '(ii) Eolas', 5, [pieces[1]], 'indicative'),
             criterion('eolas-iii', '(iii) Eolas', 7, [pieces[2]], 'indicative'), gaeilge()], LIT_REQUIREMENTS,
            'One complete SEC response with one shared five-mark Gaeilge award. The paper prints (i) 15, (ii) 6 and (iii) 9; the scheme assesses '
            'Eolas 13, 5 and 7 with the splits shown, plus Gaeilge 5 once.',
            source=('Filíocht', ref.split(' · ', 1)[1], [9]), stem=stem)

    head4 = 'Freagair do rogha ceann amháin as Ceist 4 (A, B, C, D, E nó F) thíos.'
    options = [
        ('X-4A', 'literature-4-a', '4A. An Triail', 'irish-6-0', '4A. An Triail', '4B. A Thig Ná Tit Orm',
         '4A. An Triail\n“Léirítear Pádraig Mac Cárthaigh mar fhear atá bréagach agus mícharthanach sa dráma An Triail.”\nDéan plé ar an ráiteas sin. (40 marc)'),
        ('X-4B', 'literature-4-b', '4B. A Thig Ná Tit Orm', 'irish-6-1', '4B. A Thig Ná Tit Orm', '4C. Tóraíocht Dhiarmada',
         '4B. A Thig Ná Tit Orm\nDéan plé ar an dá thréith is mó, dar leat, a bhaineann le Maidhc Dainín mar a léirítear iad sa dírbheathaisnéis A Thig Ná Tit Orm. (40 marc)'),
        ('X-4C', 'literature-4-c', '4C. Tóraíocht Dhiarmada agus Ghráinne', 'irish-6-2', '4C. Tóraíocht Dhiarmada', '4D. Gafa',
         '4C. Tóraíocht Dhiarmada agus Ghráinne\n“Is laoch cróga dílis é Diarmaid mar a léirítear sa Tóraíocht é.”\nDéan plé ar an ráiteas sin. (40 marc)'),
        ('X-4D', 'literature-4-d', '4D. Gafa', 'irish-6-3', '4D. Gafa', '4E. Canary Wharf',
         '4D. Gafa\n“Tá léiriú éifeachtach ar an gcaidreamh idir Eoin agus a thuismitheoirí, Eithne agus Breandán, sa sliocht as an úrscéal Gafa.”\nDéan plé ar an ráiteas sin. (40 marc)'),
        ('X-4E', 'literature-4-e', '4E. Canary Wharf', 'irish-6-4', '4E. Canary Wharf', '4F. Dánta Breise',
         '4E. Canary Wharf\n“Sa scéal Cosaint Sonraí, tá tionchar mór ag iompar Leanóra agus ag cás mhuintir Hilliard ar Ghráinne.”\nDéan plé ar an ráiteas sin. (40 marc)'),
    ]
    for key, slug, ref, topic, start, end, prompt in options:
        assert all(in_order(line, texts[9]) for line in prompt.splitlines()), key
        chunk, spages = s.chunk(start, end, s.page(27))
        assert 'Gaeilge (5 mharc)' not in chunk and 'Eolas = 35 marc' not in chunk, key
        assert ('Treoir:' in chunk) != (key == 'X-4B'), key  # 4B prints its marking (Blocmharcáil, the deficient box, Samplaí) instead
        add(key, slug, f'Litríocht {ref}', head4 + '\n\n' + prompt, topic, [10], sorted(set(spages) | {27}),
            [criterion('eolas', 'Eolas', 35, [chunk, m['general4']], 'indicative'), gaeilge()], LIT_REQUIREMENTS,
            'One complete SEC response: Eolas 35 assessed as a unit with a single shared 5-mark Gaeilge award. 2017 prints no “Eolas = 35 marc” line '
            'for 4A–4E; the Ceist 4 Treoracha price the answer (“an t-eolas a mharcáil as 35 marc”).'
            + (' Where the scheme prints “Eolas (35-10) (25) =”, an answer that discusses only one of the two traits is deficient and loses 10 of the 35.'
               if 'Eolas (35-10) (25) =' in chunk else ''))
    closing4f = 'Ní mór don Scrúdaitheoir an marc ar Eolas as 35 marc'
    whole, spages = s.chunk('4F. Dánta Breise – Éiceolaí', closing4f, s.page(28))
    pieces = split_parts(whole, ['(ii) Cad é an mothúchán is mó atá sa dán seo', '(iii) A bhfuil i gceist leis na línte seo a mhíniú'],
                         ['Eolas = 19 marc', 'Eolas = 8 marc', 'Míniú = 8 marc'])
    assert 'Príomhthéama an dáin a lua = 2 mharc' in pieces[0] and 'Léiriú ar an gcodarsnacht = 17 marc' in pieces[0]
    assert 'An mothúchán a ainmniú = 2 mharc' in pieces[1] and 'Pointe Eolais 2 = 3 mharc' in pieces[1]
    f_prompt = ('4F. Dánta Breise – Éiceolaí\nFreagair (i), (ii) agus (iii) thíos.\n'
                '(i) “Baineann an file úsáid as an gcodarsnacht chun príomhthéama an dáin a chur os ár gcomhair sa dán Éiceolaí (thall).” Déan plé ar an ráiteas sin. (20 marc)\n'
                '(ii) Cad é an mothúchán is mó atá sa dán seo, dar leat? Is leor dhá phointe eolais faoin mothúchán sin. '
                'Bíodh tagairtí cruinne agat do théacs an dáin i do fhreagra. (10 marc)\n'
                '(iii) A bhfuil i gceist leis na línte seo a mhíniú:\nTá bean béal dorais a choinneodh a gairdín faoi smacht\n'
                'ach ní fada go mbainfimid deireadh dúil dá misneach. (10 marc)')
    assert all(in_order(line, texts[9]) for line in f_prompt.splitlines())
    add('X-4F', 'literature-4-f', 'Litríocht 4F · Dánta Breise – Éiceolaí', head4 + '\n\n' + f_prompt, 'irish-6-10', [10, 11],
        sorted(set(spages) | {27}),
        [criterion('eolas-i', '(i) Eolas', 19, [pieces[0], m['general4']], 'indicative'), criterion('eolas-ii', '(ii) Eolas', 8, [pieces[1]], 'indicative'),
         criterion('eolas-iii', '(iii) Eolas', 8, [pieces[2]], 'indicative'), gaeilge()], LIT_REQUIREMENTS,
        'One complete SEC response: the paper prints (i) 20, (ii) 10 and (iii) 10; the scheme assesses Eolas 19 (theme 2 + contrast 17), '
        '8 (the emotion 2 + two points 3 + 3) and 8 (the explanation) plus one shared 5-mark Gaeilge award. Supporting notes are indicative rather than exhaustive.',
        source=('Dánta Breise', 'Éiceolaí', [10, 11]))

    reading = [c for c in cards if '-reading-' in c['id']]
    literature = [c for c in cards if '-reading-' not in c['id']]
    assert len(reading) == 52 and len(literature) == 10, (len(reading), len(literature))
    assert len({c['id'] for c in cards}) == len(cards) == 62 and len({c['atlasQuestionId'] for c in cards}) == 62
    assert sum(c['totalMarks'] for c in cards if re.fullmatch(r'R-[AB]-\d', c['atlasQuestionId'])) == 100
    for card in cards:
        assert sum(c['maxMarks'] for c in card['criteria']) == card['totalMarks'], card['id']
        for c in card['criteria']:
            assert c['guidance'] and all(not re.search('[-]', g) for g in c['guidance']), (card['id'], c['id'])
            assert all(h not in g for h in FURNITURE for g in c['guidance']), (card['id'], c['id'])
    sr = json.loads(SOURCE_REVIEW.read_text())
    whole = [c['id'] for c in reading if re.fullmatch(r'R-[AB]-\d', c['atlasQuestionId'])]
    review = dict(year=2017, level='higher', paperFileid=FILE + '.pdf', schemeFileid=SCHEME_FILE + '.pdf',
                  paperSha256=PAPER_SHA, schemeSha256=SCHEME_SHA,
                  reviewedPaperPages=list(range(1, 13)), reviewedSchemePages=sr['reviewedSchemePages'], schemeScope=sr['schemeScope'],
                  reviewDate=REVIEWED_AT, status='reviewed', fullPaperAndApplicableSchemeVisualSweep=True, selectionDecisions=m['decisions'],
                  readingWholeCardIds=whole, readingPracticeCardIds=[c['id'] for c in reading if c['id'] not in whole],
                  literatureRouteCardIds=[c['id'] for c in literature],
                  examStructure=dict(readingA=50, readingB=50, prose=30, poetry=30, additionalLiterature=40, total=200),
                  nonPoolDecisions=sr['nonPoolDecisions'], openIssues=[], caveats=sr['sourceFindings'],
                  boundaries='12 whole reading questions with 34 published parts, 4 independent one-mark answer slots (A 1(b)(i), B 2(b)(i)) '
                             'and 2 six-mark 6(b) slots; 2 prose, 2 poetry and 6 additional-literature routes.')
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
    print(f"Irish Higher 2017 Paper 2: {len(data['cards'])} reviewed reading and literature cards; the archive remains incomplete.")


if __name__ == '__main__':
    main()
