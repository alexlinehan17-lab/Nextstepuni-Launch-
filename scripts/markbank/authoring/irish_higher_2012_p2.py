#!/usr/bin/env python3
"""Reviewed 2012 Higher Paper 2 (Léamhthuiscint agus Litríocht): new cards, no legacy component.

Paper PDF 1–12 (page 2 a pointer to the instructions, 3 the Treoracha, 4–5 Léamhthuiscint A "Curadh Oilimpeach a
Dearmadadh" with its questions, 6–7 Léamhthuiscint B "An Sonas agus an Donas in Salvador", 8 prose, 9 poetry with An
tEarrach Thiar, 10 additional literature, 11 the poem A Chlann, 12 blank) and the Paper 2 pages of the combined
LC001ALP000IV scheme (PDF 16–26) reviewed on 2026-11-05. Counts are assertions, not corpus-completeness proof.

2012's reading questions print two parts each, not three: (a) and a (b) that asks two questions in one line ("(b) Cén
t-éacht …? Cén rud stairiúil …? (Alt 1)"), with no (i)/(ii). The scheme marks the two questions of (b) separately, as
"(b) (1)" and "(b) (2)", and its section rule prices them (PDF 16: "Tá trí mharc ag dul ar chuid (a). Tá dhá chuid i gceist
(b) …", P1(2) and P2(2)). So every printed question is a whole card, each printed part (a) and (b) is a practice card, and
(b)'s two questions are two 2-mark criteria of that card, as the scheme marks them. 6(a) prices two grammar answers, the
first right 2 and the second 1; A 6(b) is one 12-mark answer; B 6(b) prints the genre question and the traits question in one
(b), which the scheme marks as (b)(1) the genre 2 and (b)(2) two traits with an example each, T1 + S1 5 and T2 + S2 5.

The reading key prints prices in a short unit wherever a line ends ("=3m.", "”3m", "=(3-1)=2m.", "= (3-1 marc)", "S1= 1m",
"”1+1m", "T1 + S1 (5m) =") and no tariff for most parts; it lists accepted answers as quotations, some numbered "(1) … (2) …".
Its deductions for an answer not put into the third person ("(3-1m) mura bhfuil an 3ú pearsa ann.", "Gan an 3ú pearsa (2-1m)",
B 1(a), 1(b)(2), 4(b)(2); the PDF 16 rule names those three) and for an over-long or deficient answer ("=(3-1) iomarcach.",
"(3-1m),freagra easnamhach.") are printed partials. The literature scheme reprints each question with its Eolas tariff and
nothing else: 2A and 2B ("Déan plé gairid air sin.", and the note "Caithfidh an Scrúdaitheoir an marc as 25 (Ábhar) agus as 5
(Gaeilge) a thaispeáint", printed once after both), 3A and 3B "(14 marc)", "(4 marc)", "(7 marc)" (the paper prints 14, 6, 10
with Gaeilge), Ceist 4A–4E "(35 marc)" and 4F "(3 marc)" + "(16 marc)", "(8 marc)", "(8 marc)". PDF 22's NB prices Gaeilge 5 for
every literature question. PDF 25 prints three notes for Ceisteanna 2–4 after the poem A Chlann (1: A Chlann is not an optional
poem for 3B; 2: answers must address the question asked, and a summary is marked a bare C; 3: examiners should think in grades
and use the ready reckoner, "an réríomhaire (cf lch 25)"); PDF 26 is that grade-to-mark table ("Grádú Marcála sna Ceisteanna",
grades A–D for totals 200 to 5), printed on its own page after Ceist 4. It is carried as printed with the notes and never read
for rows: the judged totals it alone could scale stay one row each.

No glyph repair is needed on PDF 16–26 or on the paper: neither prints a symbol-font span (the scheme's SymbolMT and Wingdings
glyphs are on PDF 3 and 15, Paper 1). 3B's scheme reprint writes "nua­aimseartha" with a soft hyphen, outside every slice.
"""
from __future__ import annotations
import argparse
import collections
import hashlib
import json
import re
from pathlib import Path
from irish_lifted import scheme_words_in, symbol_text

ROOT = Path(__file__).resolve().parents[3]
FILE = 'LC001ALP200IV'
SCHEME_FILE = 'LC001ALP000IV'
OUT = ROOT / 'components/MarkBank/cards/irish/higher-2012-p2-authored.json'
SOURCE_REVIEW = ROOT / 'scripts/markbank/authored/irish-higher-2012-p2-source-review.json'
REVIEWED_AT = '2026-11-05'
PAPER_SHA = '8b776b452b88f412d8e89c22e6876987dcb94519c0963782c7df3302ebea85b5'
SCHEME_SHA = '890fe382628c17197ac926200f9aa46f63114852daf6eaad87242b482fafcd3f'
DIRECTIVE = re.compile(r'rogha|roghna|Freagair|Luaigh|Ainmnigh|\bnó\b|dhá phointe|dhá rud|dhá bh|dhá dh|dhá ch|dhá fh|dhá th|'
                       r'ceann amháin|pointe amháin|\bdhá\b|an dá\b|amháin', re.I)
SOURCE_NOTE = 'Shown page-for-page from the official examination paper; swipe to move between pages.'
# Every symbol-font span of the paper and of the scheme's Paper 2 pages (PDF 16–26): none.
SCHEME_GLYPHS = {(3, 'SymbolMT', '\uf0b4'): 6, (15, 'Wingdings-Regular', '\uf0e0'): 1}


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


def symbol_audit(doc):
    audit = collections.Counter()
    for number, page in enumerate(doc, 1):
        for block in page.get_text('rawdict')['blocks']:
            for line in block.get('lines', []):
                for span in line['spans']:
                    if span['font'].startswith(('Symbol', 'Wingdings')):
                        for char in span['chars']:
                            audit[(number, span['font'], char['c'])] += 1
    return dict(audit)


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
        pages |= {int(m.group(1)) for m in re.finditer(r'⟦(\d+)⟧([^⟦]*)', raw) if clean(m.group(2))}
        return clean(re.sub(r'⟦\d+⟧', ' ', raw)), sorted(pages)

    def page(self, number):
        return self.text.index(f'⟦{number}⟧')


def printed_values(chunk, marks):
    """The marks one answer can earn: 0, the full tariff and every price and partial the key prints for it ("=3m", "”2m",
    "S1= 1m", "1+1m" and its first point, "=(3-1)=2m", "(3-1m)", "(2-1 m)", "= 0 m")."""
    values = {0, marks}
    for a, b in re.findall(r'(\d)\s*\+\s*(\d)\s*m\b', chunk):
        values |= {int(a), int(a) + int(b)}
    for a, b in re.findall(r'\((\d)\s*-\s*(\d)\s*(?:m|marc)?\s*\)', chunk):
        values.add(int(a) - int(b))
    values |= {int(v) for v in re.findall(r'(?<![\d+\-])(\d)\s*m\b', chunk)}
    return sorted(v for v in values if v <= marks)


def material():
    import fitz
    paper_path = ROOT / f'paper-trail-corpus/exampapers/2012/{FILE}.pdf'
    scheme_path = ROOT / f'paper-trail-corpus/markingschemes/2012/{SCHEME_FILE}.pdf'
    assert hashlib.sha256(paper_path.read_bytes()).hexdigest() == PAPER_SHA, 'Paper changed: repeat visual review'
    assert hashlib.sha256(scheme_path.read_bytes()).hexdigest() == SCHEME_SHA, 'Scheme changed: repeat visual review'
    paper, doc = fitz.open(paper_path), fitz.open(scheme_path)
    assert symbol_audit(paper) == {} and symbol_audit(doc) == SCHEME_GLYPHS, 'Symbol glyphs changed: repeat the glyph review'
    texts = [clean(p.get_text()) for p in paper]
    s = Scheme(doc, 16, 26)
    # The marking instructions, from their first rule (their heading "Treoracha do mharcáil na léamhthuisceana" is a title)
    # to Léamhthuiscint A's heading.
    general = s.chunk('Tá Ceist 1 – 5 ar cómharc', 'Léamhthuiscint 2A')[0]
    assert general.endswith('ar an bpáipéar scrúdaithe.') and '7 marc ar gach ceann' in general and 'P1(2) =2' in general, general[-80:]
    # (q, part, paper prompt, [(criterion, scheme anchor, marks)]). Each passage ends at the examiner's totals line for it.
    A = [
        ('1', 'a', '(a) In aimsir na sean-Ghréige, céard í teist an fhíorlaoich?', [('a', '1 (a) In aimsir na sean-Ghréige', 3)]),
        ('1', 'b', '(b) Cén t-éacht a rinne Jim Thorpe a cheiliúrfar tráth na gCluichí Oilimpeacha i mbliana? Cén rud stairiúil a bhain leis an éacht seo? (Alt 1)',
         [('b-1', '1 (b) (1) Cén t-éacht', 2), ('b-2', '1 (b) (2) Cén rud stairiúil', 2)]),
        ('2', 'a', '(a) Conas a tharla sé go raibh fuil Indiach i Jim Thorpe?', [('a', '2 (a) Conas a tharla sé', 3)]),
        ('2', 'b', '(b) Cén spórt a bhfacthas cumas lúthchleasaíochta Jim ann den chéad uair? Cén fáth a ndeachaigh Jim go Carlisle? (Alt 2)',
         [('b-1', '2 (b) (1) Cén spórt', 2), ('b-2', '2 (b) (2) Cén fáth a ndeachaigh Jim go Carlisle', 2)]),
        ('3', 'a', '(a) Cad a rinne Jim a tharraing spéis thraenálaithe na scoile in Carlisle air den chéad uair?', [('a', '3 (a) Cad a rinne Jim', 3)]),
        # The scheme reprints (b)'s second question "Cén dhá shlí …"; the card shows the paper's "Cén dá shlí".
        ('3', 'b', '(b) Cén fáth a ndeachaigh Jim go Carolina? Cén dá shlí dhifriúla ar caitheadh le Jim in Carolina? (Alt 3)',
         [('b-1', '3 (b) (1) Cén fáth a ndeachaigh Jim go Carolina', 2), ('b-2', '3 (b) (2) Cén dhá shlí', 2)]),
        ('4', 'a', '(a) Cén rud a cuireadh i leith Jim nuair a bhuaigh sé an Peantatlan agus an Deacatlan i Stócólm?', [('a', '4 (a) Cén rud a cuireadh', 3)]),
        ('4', 'b', '(b) Conas a thacaigh a chomhiomaitheoirí le Jim i Stócólm? Cén fáth, dar lena lucht leanúna, ar gearradh pionós ar Jim i Stócólm? (Alt 4)',
         [('b-1', '4 (b) (1) Conas a thacaigh', 2), ('b-2', '4 (b) (2) Cén fáth, dar lena lucht', 2)]),
        # The scheme reprints 5(a) without "Oilimpeacha?"; the card shows the paper's question.
        ('5', 'a', '(a) Conas a chaith Jim a shaol i Meiriceá i ndiaidh na gCluichí Oilimpeacha?', [('a', '5 (a) Conas a chaith Jim', 3)]),
        ('5', 'b', '(b) Cén fáth ar bhronn Coiste Idirnáisiúnta na gCluichí Oilimpeacha (IOC) na boinn óir a bhuaigh Jim ar a chlann ar deireadh? Cathain a tharla an bronnadh sin? (Alt 5)',
         [('b-1', '5 (b) (1) Cén fáth ar bhronn', 2), ('b-2', '5(b) (2) Cathain a tharla', 2)]),
        ('6', 'a', '(a) Aimsigh ainmfhocal sa ghinideach iolra in alt 1 agus briathar saor san aimsir chaite in alt 5.', [('grammar', '6 (a) Aimsigh ainmfhocal', 3)]),
        ('6', 'b', '(b) Cad a léiríonn an sliocht seo faoi dhearcadh phobal Mheiriceá agus faoi dhearcadh an IOC ar dhaoine mar Jim Thorpe sa chéad seo caite? '
                   '(Bíodh an freagra i d’fhocail féin. Ní gá níos mó ná 60 focal a scríobh.)', [('eolas', '6 (b) Cad a léiríonn', 12)]),
    ]
    B = [
        ('1', 'a', '(a) Cad ba chúis leis an íomhá dhiúltach a bhí ag an údar den saol sna favelas?', [('a', '1 (a) Cad ba chúis', 3)]),
        ('1', 'b', '(b) Cén tréith de chuid mhuintir Tancredo Neves a mheall an t-údar? Cén fáth ar bheartaigh sé fanacht leo? (Alt 1)',
         [('b-1', '1 (b) (1) Cén tréith', 2), ('b-2', '1 (b) (2) Cén fáth ar bheartaigh', 2)]),
        ('2', 'a', '(a) Cén chaoi ar fhulaing na bundúchasaigh in Salvador ag lámha na bPortaingéalach?', [('a', '2 (a) Cén chaoi ar fhulaing', 3)]),
        ('2', 'b', '(b) Cén chaoi ar tháinig na favelas ar an saol? Cén fáth a bhfuil fás mór fúthu sa lá atá inniu ann? (Alt 2)',
         [('b-1', '2 (b) (1) Cén chaoi ar tháinig', 2), ('b-2', '2 (b) (2) Cén fáth a bhfuil fás', 2)]),
        ('3', 'a', '(a) Cén fáth a ndeir tuismitheoirí Nilton nach favela é Loteamento?', [('a', '3 (a) Cén fáth a ndeir', 3)]),
        ('3', 'b', '(b) Céard iad na rudaí is luachmhaire ag muintir Shalvador, dar leis an údar? Cén bunús atá le spioradáltacht mhuintir Shalvador, dar leis? (Alt 3)',
         [('b-1', '3 (b) (1) Céard iad na rudaí', 2), ('b-2', '3.(b) (2) Cén bunús', 2)]),
        # The scheme reprints 4(a) "Cén chaoi ar iobartaigh …"; the card shows the paper's "íobartaigh".
        ('4', 'a', '(a) Cén chaoi ar íobartaigh de chuid an impiriúlachais iad na hAfra-Bhrasaíligh in Salvador?', [('a', '4 (a) Cén chaoi ar iobartaigh', 3)]),
        ('4', 'b', '(b) Céard iad na haingil choimhdeachta a luaigh Bruno leis an údar? Cén fáth a n-oireann na haingil choimhdeachta sin don údar, dar leis féin? (Alt 4)',
         [('b-1', '4 (b) (1) Céard iad na haingil', 2), ('b-2', '4 (b) (2) Cén fáth a n-oireann', 2)]),
        ('5', 'a', '(a) Cén “fhírinne ghránna” atá ag baint leis an áit?', [('a', '5 (a) Cén “fhírinne ghránna”', 3)]),
        ('5', 'b', '(b) Cén dearcadh atá ag muintir Thancredo Neves ar an oideachas? Cén chaoi a léiríonn Nueza agus a mhac Tony an dearcadh seo? (Alt 5)',
         [('b-1', '5 (b)(1) Cén dearcadh', 2), ('b-2', '5 (b)(2) Cén chaoi a léiríonn', 2)]),
        ('6', 'a', '(a) Aimsigh briathar saor san aimsir láithreach in alt 5 agus ainmfhocal sa ghinideach uatha in alt 1.', [('grammar', '6.(a) Aimsigh briathar saor', 3)]),
        ('6', 'b', '(b) Cén cineál (genre) litríochta lena mbaineann an sliocht seo? Luaigh dhá thréith a bhaineann leis an gcineál seo litríochta. '
                   'Aimsigh sampla amháin de na tréithe sin sa sliocht. (Bíodh an freagra i d’fhocail féin. Ní gá níos mó ná 60 focal a scríobh.)',
         [('genre', '6.(b)(1) Cén cineál (genre)', 2), ('traits', '6.(b)(2) Luaigh dhá thréith', 10)]),
    ]
    passages = {
        'A': dict(title='Curadh Oilimpeach a Dearmadadh', pages=[4, 5], topic='irish-3-0', parts=A, six='(15 mharc)',
                  start='Léamhthuiscint 2A', end='Suimigh anois na marcanna agus léirigh mar seo. Ceist 1 A (50) ='),
        'B': dict(title='An Sonas agus an Donas in Salvador', pages=[6, 7], topic='irish-3-1', parts=B, six='(15 marc)',
                  start='Léamhthuiscint 2B', end='Ag bun Léamhthuiscint B, seo mar a léirítear na marcanna;'),
    }
    for letter, passage in passages.items():
        page_text = ' '.join(texts[p - 1] for p in passage['pages'])
        anchors = [(q, part, cid, anchor, marks) for q, part, _, crits in passage['parts'] for cid, anchor, marks in crits]
        pos = s.text.index(passage['start'])
        chunks = {}
        for index, (q, part, cid, anchor, marks) in enumerate(anchors):
            here = s.text.index(anchor, pos)
            following = anchors[index + 1][3] if index + 1 < len(anchors) else passage['end']
            chunk, spages = s.chunk(anchor, following, pos)
            pos = here + 1
            assert 'Suimigh' not in chunk and 'Léamhthuiscint 2B' not in chunk and 'Ag bun' not in chunk and 'CEIST 2' not in chunk, (letter, q, cid)
            chunks[(q, cid)] = (chunk, spages)
        for q, part, prompt, crits in passage['parts']:
            assert in_order(prompt, page_text), (letter, q, part)
        passage['chunks'] = chunks
        assert in_order(passage['six'], texts[passage['pages'][1] - 1]), letter
    assert sum(len(p['parts']) for p in passages.values()) == 24
    six_a = passages['A']['chunks'][('6', 'eolas')][0]
    assert six_a.endswith('An IOC i bhfábhar amaitéarachais, bonn, éagóir, cúiteamh.') and 'marcáil an freagra as 8 marc' in six_a, six_a[-120:]
    traits = passages['B']['chunks'][('6', 'traits')][0]
    assert traits.endswith('10 mharc, mion bhriseadh le léiriú mar seo, T1 + S1 (5m) = T2+ S2 (5m) ='), traits
    nb = s.chunk('NB: I gcás na gceisteanna 2 (Prós)', 'Freagair A (Prós Ainmnithe) nó B (Prós Roghnach).')[0]
    assert nb.endswith('35 ar Eolas agus 5 ar Ghaeilge.'), nb[-60:]
    notes = s.chunk('2. Sna freagraí ar an bPrós', '⟦26⟧', s.page(25))[0]
    note_one = s.chunk('1. Níl cead A Chlann (4F)', '2. Sna freagraí', s.page(25))[0]
    assert notes.endswith('agus iad ag teacht ar chinneadh faoi cad is fiú freagra.') and 'úsáid a bhaint as an réríomhaire (cf lch 25)' in notes, notes[-90:]
    assert note_one == '1. Níl cead A Chlann (4F) a úsáid mar dán roghnach i gCeist 3(b).', note_one
    grading = s.chunk('Grádú Marcála sna Ceisteanna', None, s.page(26))[0]
    assert grading.endswith('D 7 7 6 6 5 5 4 4 4 3 3 2') and 'GRÁD 200 160 100' in grading and 'ansin cinneadh ar an marc.' in grading, grading[-60:]
    # The prose note printed once after both 2A and 2B, then 2B's own two rules.
    nota2 = s.chunk('Nóta: Caithfidh an Scrúdaitheoir an marc as 25 (Ábhar)', 'Ní bhronnfar marcanna', s.page(22))[0]
    rules2b = s.chunk('Ní bhronnfar marcanna ar theidil', '⟦23⟧', s.page(22))[0]
    assert nota2.endswith('sna hionaid chuí ar an bhfreagarleabhar.') and rules2b.endswith('nach bhfuil na téacsanna sin in úsáid i gCeist 4'), rules2b[-60:]
    return dict(paper=paper, texts=texts, s=s, general=general, passages=passages, nb=nb, notes=notes, note_one=note_one, grading=grading,
                nota2=nota2, rules2b=rules2b, decisions=selection_decisions(paper))


READING_REQUIREMENTS = ['Léigh an sliocht iomlán a ghabhann leis an gceist. Freagair an chuid atá luaite ar an gcárta.',
                        'Úsáid an t-alt a luaitear. Glacfar le focail an tsleachta nó le do chuid focal féin, ach ní mór 6(b) a fhreagairt i d’fhocail féin.']
WHOLE_REQUIREMENTS = ['Léigh an sliocht oifigiúil a ghabhann leis an gceist.', 'Freagair gach fochuid agus cloígh leis an alt a luaitear.',
                      'Bain úsáid as do chuid focal féin nuair a iarrtar ort é.']
LIT_REQUIREMENTS = ['Freagair gach cuid den cheist atá priontáilte.', 'Úsáid tagairtí cruinne agus ábhartha don téacs.']
PART_NOTE = ('SEC allocation for this task. Alternative correct answers in the scheme are answers to one task, not extra task routes. '
             'Whole questions and their practice parts are overlapping exercises; their marks are not added to infer the paper total.')
B_NOTE = ('The paper prints (b) as one part asking two questions; the scheme marks them separately, (b)(1) and (b)(2), 2 marks each '
          '(its section rule, PDF 16), so each is a criterion of this card. ')
LABELS = {'a': '(a) Freagra', 'b-1': '(b)(1) Freagra', 'b-2': '(b)(2) Freagra', 'grammar': '(a) Freagra', 'eolas': '(b) Freagra',
          'genre': '(b)(1) Cineál', 'trait-1': '(b)(2) Tréith 1 + Sampla 1', 'trait-2': '(b)(2) Tréith 2 + Sampla 2'}


def part_criteria(cid, marks, chunk, general):
    if cid == 'grammar':
        # "[Bronn 2 mharc ar an gcéad cheann atá ceart agus 1 mharc ar an dara ceann.]": 0, the first right 2, both 3.
        return [criterion('grammar', 'Freagra', marks, [chunk, general], permitted=[0, 2, 3])]
    if cid == 'eolas':
        # A 6(b): one judged 12-mark answer; the scheme caps an answer naming one view at 8 and a bare retelling at 7.
        return [criterion('eolas', 'Freagra', marks, [chunk, general], 'indicative')]
    if cid == 'genre':
        return [criterion('genre', 'Cineál', marks, [chunk, general], permitted=[0, 2])]
    if cid == 'traits':
        # "T1 + S1 (5m) = T2+ S2 (5m) =": each trait with its example 5, the scheme printing no split between them.
        return [criterion('trait-1', 'Tréith 1 + Sampla 1', 5, [chunk]), criterion('trait-2', 'Tréith 2 + Sampla 2', 5, [chunk])]
    return [criterion(cid, 'Freagra', marks, [chunk, general], permitted=printed_values(chunk, marks))]


def build():
    m = material()
    texts, s = m['texts'], m['s']
    cards = []

    def add(key, slug, ref, prompt, topic, pages, scheme_pages, criteria, requirements, note, extra_topics=None, source=None, **extra):
        cards.append(dict(
            id=f'irish-2012-hl-p2-{slug}', year=2012, level='higher', paper=2, section='2',
            atlasQuestionId=key, questionRef=f'2012 HL Paper 2 {ref}', questionText=prompt,
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
    six_b = {'A': '6(b) is one judged answer of 12 marks on both views (the American public’s and the IOC’s), in the candidate’s own words; '
                  'the scheme marks an answer naming only one of them out of 8 and a bare retelling out of 7.',
             'B': '6(b) is the genre 2 (wherever the answer names it) and two of its traits with an example from the passage each, 5 + 5, '
                  'in the candidate’s own words.'}
    for letter, passage in m['passages'].items():
        topic = passage['topic']
        source = (f'Léamhthuiscint {letter}', passage['title'], passage['pages'])
        by_question = {}
        for q, part, prompt, crits in passage['parts']:
            label = f'{q}({part})'
            text = f'{label} ' + re.sub(r'^\([a-z]\)\s*', '', prompt)
            mode = crits[0][0]
            here = 'irish-3-3' if mode == 'grammar' else topic
            criteria = [c for cid, _, marks in crits for c in part_criteria(cid, marks, *m['passages'][letter]['chunks'][(q, cid)][:1], m['general'])]
            spages = sorted({p for cid, _, _ in crits for p in passage['chunks'][(q, cid)][1]})
            note = (B_NOTE if part == 'b' and q != '6' else '') + PART_NOTE
            card = add(f'R-{letter}-{q}-{part}', f'reading-{letter.lower()}-q{q}-{part}', f'Léamhthuiscint {letter} · Ceist {label}', text, here,
                       passage['pages'], spages, criteria, READING_REQUIREMENTS, note, [topic] if mode == 'grammar' else None, source)
            by_question.setdefault(q, []).append((part, prompt, card))
        for q, parts in by_question.items():
            crits = [dict(c) for _, _, card in parts for c in card['criteria']]
            for c in crits:
                c['label'] = LABELS[c['id']]
            add(f'R-{letter}-{q}', f'reading-{letter.lower()}-q{q}', f'Léamhthuiscint {letter} · Ceist {q}',
                f'{q}. ' + ' '.join(p for _, p, _ in parts) + (' (7 marc)' if q != '6' else f' {passage["six"]}'), topic, passage['pages'],
                sorted({p for _, _, c in parts for p in c['schemePages']}), crits, WHOLE_REQUIREMENTS,
                'Complete printed question. Score each published part separately using these SEC allocations.'
                + (' Two-answer grammar is one 0/2/3 placement; ' + six_b[letter] if q == '6' else ' (b) asks two questions, marked 2 + 2.'),
                ['irish-3-3'] if q == '6' else None, source)
            assert cards[-1]['totalMarks'] == (15 if q == '6' else 7), (letter, q)

    # ---- Ceisteanna 2–4: An Litríocht -------------------------------------------------------
    gaeilge = lambda: criterion('gaeilge', 'Gaeilge', 5, [m['nb'], m['notes'], m['grading']], 'quality')
    head2 = 'Freagair Ceist 2A nó Ceist 2B thíos.'
    head3 = 'Freagair Ceist 3A nó Ceist 3B thíos:'
    stem2 = 'PRÓS AINMNITHE nó PRÓS ROGHNACH\n' + head2
    prose_note = ('One complete SEC response: Eolas 25 (the scheme’s “an marc as 25 (Ábhar)”, judged as a whole) and a single shared 5-mark '
                  'Gaeilge award. The scheme prints no supporting notes or band table for this question; its literature notes and general '
                  'grading table (PDF 25–26) are carried as printed.')
    prose = [
        ('P-2A', 'prose-2a', 'Prós 2A · Hurlamaboc', 'irish-4-5', '2A “Sa sliocht seo', 'B - PRÓS ROGHNACH -',
         '2A\n“Sa sliocht seo as an úrscéal Hurlamaboc, léiríonn iompar agus dearcadh Lisín go leor gnéithe suimiúla den saol nua-aimseartha.”\n'
         'Déan plé gairid air sin. (30 marc)', []),
        ('P-2B', 'prose-2b', 'Prós 2B · Úrscéal roghnach', 'irish-4-7', '2B Maidir leis an sliocht', 'Nóta: Caithfidh an Scrúdaitheoir',
         '2B\nMaidir leis an sliocht as an úrscéal roghnach a ndearna tú staidéar air le linn do chúrsa, déan plé gairid ar an bpríomhthéama atá ann, '
         'agus ar fhorbairt an phríomhthéama sin sa sliocht.\nNí mór teideal an úrscéil sin, mar aon le hainm an údair, a scríobh síos go cruinn. (30 marc)',
         [m['rules2b']]),
    ]
    for key, slug, ref, topic, start, end, prompt, extra_rules in prose:
        for line in [*stem2.splitlines(), *prompt.splitlines()]:
            assert in_order(line, texts[7]), (key, line[:40])
        # The scheme reprints the question; its marking text is the note after both questions (and 2B's two rules after it).
        question, qpages = s.chunk(start, end, s.page(22))
        assert all(in_order(re.sub(r'\s*\(30 marc\)$', '', line), question) for line in prompt.splitlines()), (key, 'scheme reprint differs')
        add(key, slug, ref, prompt, topic, [8], [22, 25, 26],
            # The grade table is printed without its note's closing bracket ("(Féach an scéim ghrádaithe … ar lch. eile."); here it would
            # be read as a direction, so it is carried on the card's Gaeilge criterion only.
            [criterion('eolas', 'Eolas', 25, [question, m['nota2'], *extra_rules], 'indicative'), gaeilge()],
            LIT_REQUIREMENTS, prose_note, source=('Prós', ref.split(' · ', 1)[1], [8]), stem=stem2)

    poems = [
        ('F-3A', 'poetry-3a', 'Filíocht 3A · An tEarrach Thiar', 'irish-5-3', '3A (i) “Baineann an file', 'An tEarrach Thiar 1 Fear ag glanadh', head3 + '\n3A', [
            '(i) “Baineann an file úsáid éifeachtach as íomhánna agus as fuaimeanna chun a bhfuil ina chroí istigh a nochtadh dúinn sa dán An tEarrach Thiar (thíos).” '
            'Déan plé gairid ar an ráiteas sin. (14 marc)',
            '(ii) Críochnaíonn gach véarsa leis an líne “San Earrach thiar”. Cén éifeacht a bhaineann le hathrá na bhfocal sin, dar leat? (6 marc)',
            '(iii) Scríobh nóta gairid ar shaol agus ar shaothar an fhile seo. (10 marc)'],
         ['(ii) Críochnaíonn gach véarsa', '(iii) Scríobh nóta gairid'], ['(14 marc)', '(4 marc)', '(7 marc)'], [9], []),
        ('F-3B', 'poetry-3b', 'Filíocht 3B · Dán nua-aimseartha roghnach', 'irish-5-6', '(i) Déan plé gairid ar éifeacht', '⟦24⟧',
         head3 + '\n3B\nMaidir le dán nua-aimseartha a ndearna tú staidéar air le linn do chúrsa,', [
            '(i) Déan plé gairid ar éifeacht na húsáide a bhaineann an file as dhá ghné díobh seo a leanas: (a) na híomhánna; (b) an t-atmaisféar; '
            '(c) an friotal. (14 marc)',
            '(ii) Léirigh mar a chuaigh an dán i bhfeidhm ort. (6 marc)',
            '(iii) Scríobh nóta gairid ar shaol agus ar shaothar an fhile a chum an dán a roghnaigh tú. (10 marc)'],
         ['(ii) Léirigh mar a chuaigh', '(iii) Scríobh nóta gairid'], ['(14 marc)', '(4 marc)', '(7 marc)'], [9], [m['note_one']]),
    ]
    for key, slug, ref, topic, start, end, stem, parts, cuts, caps, paper_pages, extra_notes in poems:
        for line in [*stem.splitlines(), *parts]:
            assert in_order(line, texts[8]), (key, line[:40])
        whole, spages = s.chunk(start, end, s.page(23))
        i2 = whole.index(cuts[0]); i3 = whole.index(cuts[1], i2)
        pieces = [whole[:i2].strip(), whole[i2:i3].strip(), whole[i3:].strip()]
        for piece, cap in zip(pieces, caps):
            assert piece.endswith(cap), (key, piece[-30:])
        add(key, slug, ref, '\n'.join(parts), topic, paper_pages, sorted(set(spages) | {25, 26}),
            [criterion('eolas-i', '(i) Eolas', 14, [pieces[0], *extra_notes, m['grading']], 'indicative'),
             criterion('eolas-ii', '(ii) Eolas', 4, [pieces[1]], 'indicative'),
             criterion('eolas-iii', '(iii) Eolas', 7, [pieces[2]], 'indicative'), gaeilge()], LIT_REQUIREMENTS,
            'One complete SEC response with one shared five-mark Gaeilge award. The paper prints (i) 14, (ii) 6 and (iii) 10; the scheme '
            'reprints each sub-question with its Eolas tariff, 14, 4 and 7, and prints no notes for them, plus Gaeilge 5 once.',
            source=('Filíocht', ref.split(' · ', 1)[1], paper_pages), stem=stem)

    head4 = 'Freagair do rogha ceann amháin as Ceist 4 (A, B, C, D, E nó F) thíos:'
    options = [
        ('X-4A', 'literature-4-a', '4A. An Triail', 'irish-6-0',
         '4A. An Triail\n“Fulaingt Mháire Uí Chathasaigh agus fimíneacht na sochaí ina leith is mó a léirítear sa dráma An Triail.”\n'
         'Déan plé ar an ráiteas sin. (40 marc)'),
        ('X-4B', 'literature-4-b', '4B. A Thig ná Tit Orm', 'irish-6-1',
         '4B. A Thig ná Tit Orm\nDéan plé ar an dá ghné den chur síos ar shaol an údair agus é ag fás aníos sa Ghaeltacht is mó a chuaigh i bhfeidhm ort. (40 marc)'),
        ('X-4C', 'literature-4-c', '4C. Tóraíocht Dhiarmada agus Ghráinne', 'irish-6-2',
         '4C. Tóraíocht Dhiarmada agus Ghráinne\n“Is iad gliceas agus scéiméireacht Ghráinne is cúis le himeachtaí na Tóraíochta.”\n'
         'Déan plé ar an ráiteas sin. (40 marc)'),
        ('X-4D', 'literature-4-d', '4D. Gafa', 'irish-6-3',
         '4D. Gafa\n“Is éifeachtach an léiriú a thugtar dúinn ar intinn shuaite na máthar, Eithne, sa sliocht as an úrscéal Gafa.”\n'
         'Déan plé ar an ráiteas sin. (40 marc)'),
        ('X-4E', 'literature-4-e', '4E. Canary Wharf', 'irish-6-4',
         '4E. Canary Wharf\n“Sa scéal Cúrsaí Eitilte, léiríonn Orna Ní Choileáin go héifeachtach dúinn na baic agus na castaí a chuirtear in aghaidh Theo '
         'agus é ag iarraidh dul chun bualadh lena ghrá Alana in Montréal.”\nDéan plé gairid ar an ráiteas sin. (40 marc)'),
    ]
    starts = ['4A. An Triail', '4B. A Thig ná Tit Orm', '4C. Tóraíocht Dhiarmada', '4D. Gafa', '4E. Canary Wharf', '4F. Dánta Breise']
    for index, (key, slug, ref, topic, prompt) in enumerate(options):
        assert all(in_order(line, texts[9]) for line in prompt.splitlines()), key
        # The scheme reprints each question with its Eolas tariff "(35 marc)" and prints no text of its own for 4A–4E.
        question, qpages = s.chunk(starts[index], starts[index + 1], s.page(24))
        assert question.endswith('(35 marc)') and in_order(re.sub(r'\s*\(40 marc\)$', '', prompt.splitlines()[-1]), question), key
        add(key, slug, f'Litríocht {ref}', head4 + '\n\n' + prompt, topic, [10], sorted(set(qpages) | {25, 26}),
            [criterion('eolas', 'Eolas', 35, [question, m['grading']], 'indicative'), gaeilge()], LIT_REQUIREMENTS,
            'One complete SEC response: Eolas 35 assessed as a unit with a single shared 5-mark Gaeilge award. The 2012 scheme reprints the '
            'question with its Eolas tariff and prints no notes for 4A–4E beyond the literature notes and general grading table (PDF 25–26).')
    whole, spages = s.chunk('(i) Cad é príomhthéama an dáin A Chlann', 'A Chlann 1 Dá bhféadfainn', s.page(24))
    i2 = whole.index('(ii) A bhfuil i gceist'); i3 = whole.index('(iii) Cén mothú', i2)
    pieces = [whole[:i2].strip(), whole[i2:i3].strip(), whole[i3:].strip()]
    assert pieces[0].endswith('ó thús go deireadh an dáin. (16 marc)') and '? (3 marc)' in pieces[0], pieces[0]
    assert pieces[1].endswith('(8 marc)') and pieces[2].endswith('(8 marc)'), pieces
    cut = pieces[0].index('? (3 marc)') + len('? (3 marc)')
    theme, development = pieces[0][:cut].strip(), pieces[0][cut:].strip()
    assert theme.startswith('(i) Cad é príomhthéama') and development.startswith('Déan plé ar an gcaoi') and development.endswith('(16 marc)')
    f_prompt = ('4F. Dánta Breise - A Chlann\nFreagair na trí cheist seo a leanas:\n'
                '(i) Cad é príomhthéama an dáin A Chlann (thall), dar leat? Déan plé ar an gcaoi a ndéantar léiriú ar an bpríomhthéama sin '
                'ó thús go deireadh an dáin. (20 marc)\n'
                '(ii) A bhfuil i gceist leis na línte seo a mhíniú:\nDá bhféadfainn, dhéanfainn rud daoibh\nNár dheineas riamh dom féin -\n'
                'Mhaithfinn daoibh gach peaca\n’s d’agróinn cogadh ar phéin! (10 marc)\n'
                '(iii) Cén mothú is mó a mhúscail dearcadh na máthar ionat féin? (Is leor dhá phointe eolais.) (10 marc)')
    assert all(in_order(line, texts[9]) for line in f_prompt.splitlines())
    add('X-4F', 'literature-4-f', 'Litríocht 4F · Dánta Breise – A Chlann', head4 + '\n\n' + f_prompt, 'irish-6-8', [10, 11],
        sorted(set(spages) | {25, 26}),
        # (i) prints its two questions each with its own Eolas tariff, "(3 marc)" and "(16 marc)": a criterion each.
        [criterion('eolas-i-1', '(i) Príomhthéama', 3, [theme, m['grading']], 'indicative'),
         criterion('eolas-i-2', '(i) Léiriú', 16, [development], 'indicative'), criterion('eolas-ii', '(ii) Eolas', 8, [pieces[1]], 'indicative'),
         criterion('eolas-iii', '(iii) Eolas', 8, [pieces[2]], 'indicative'), gaeilge()], LIT_REQUIREMENTS,
        'One complete SEC response: the paper prints (i) 20, (ii) 10 and (iii) 10; the scheme reprints them with their Eolas tariffs, '
        '(i) 3 (the main theme) + 16 (its development), (ii) 8 and (iii) 8, plus one shared 5-mark Gaeilge award.',
        source=('Dánta Breise', 'A Chlann', [10, 11]))

    reading = [c for c in cards if '-reading-' in c['id']]
    literature = [c for c in cards if '-reading-' not in c['id']]
    assert len(reading) == 36 and len(literature) == 10, (len(reading), len(literature))
    assert len({c['id'] for c in cards}) == len(cards) == 46 and len({c['atlasQuestionId'] for c in cards}) == 46
    assert sum(c['totalMarks'] for c in cards if re.fullmatch(r'R-[AB]-\d', c['atlasQuestionId'])) == 100
    for card in cards:
        assert sum(c['maxMarks'] for c in card['criteria']) == card['totalMarks'], card['id']
        for c in card['criteria']:
            assert c['guidance'] and all(not re.search('[\ue000-\uf8ff\xad]', g) for g in c['guidance']), (card['id'], c['id'])
    sr = json.loads(SOURCE_REVIEW.read_text())
    whole_ids = [c['id'] for c in reading if re.fullmatch(r'R-[AB]-\d', c['atlasQuestionId'])]
    review = dict(year=2012, level='higher', paperFileid=FILE + '.pdf', schemeFileid=SCHEME_FILE + '.pdf',
                  paperSha256=PAPER_SHA, schemeSha256=SCHEME_SHA,
                  reviewedPaperPages=list(range(1, 13)), reviewedSchemePages=sr['reviewedSchemePages'], schemeScope=sr['schemeScope'],
                  reviewDate=REVIEWED_AT, status='reviewed', fullPaperAndApplicableSchemeVisualSweep=True, selectionDecisions=m['decisions'],
                  readingWholeCardIds=whole_ids, readingPracticeCardIds=[c['id'] for c in reading if c['id'] not in whole_ids],
                  literatureRouteCardIds=[c['id'] for c in literature],
                  examStructure=dict(readingA=50, readingB=50, prose=30, poetry=30, additionalLiterature=40, total=200),
                  nonPoolDecisions=sr['nonPoolDecisions'], openIssues=[], caveats=sr['sourceFindings'],
                  boundaries='12 whole reading questions with 24 published parts ((a) and (b); each (b) asks two questions, marked 2 + 2); '
                             '2 prose (2A Hurlamaboc, 2B an optional novel extract), 2 poetry and 6 additional-literature routes.')
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
    print(f"Irish Higher 2012 Paper 2: {len(data['cards'])} reviewed reading and literature cards; the archive remains incomplete.")


if __name__ == '__main__':
    main()
