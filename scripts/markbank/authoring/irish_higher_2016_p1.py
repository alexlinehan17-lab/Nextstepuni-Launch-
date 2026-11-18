#!/usr/bin/env python3
"""Reviewed 2016 Higher Paper 1 (Cluastuiscint agus Ceapadóireacht): new cards, no legacy component.

Paper PDF 1–8 (2016 prints no answer booklet: the cover carries the instructions, Cuid A
starts on page 2, the composition Treoracha sit on page 6 and the choice and titles on
page 7; page 8 is blank) and the Paper 1 pages of the combined LC001ALP000IV scheme
(PDF 1–15 and 31) reviewed on 2026-11-04. Scheme PDF 16–30 belong to Paper 2; PDF 32 is
empty. Counts are assertions, not corpus-completeness proof. Same layout as 2018
(irish_higher_2018_p1.py) with these differences: the listening answers run PDF 7–10 and
the cover-mark table is PDF 11; Fógra a hAon prints five questions and Fógra a Dó three
(its Ceist 2 at 2 + 2), Comhrá a Dó's second mír two (its Ceist 1 at 2 + 2) and each Píosa
three; the composition marking is PDF 12–15 with no S1–S4 grades and no page of short /
off-title reductions (the off-title pro-rata note sits inside the Cumas Gaeilge text on PDF
14), and the 80-mark table ends at N/G íseal 0-3. The modified marking scheme is PDF 31.

The card unit follows the reviewed 2018–2025 components: one card per printed listening
segment (Fógra, Comhrá mír, Píosa), each printed question its own criterion at its
published 2 or 2 + 2 tariff, and one whole 100-mark card per printed composition title
(choose one of A, B, C; no combination cards). `main` writes the card file
components/MarkBank/cards/irish/higher-2016-p1-authored.json with its review record.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import re
from pathlib import Path
from irish_lifted import scheme_words_in, symbol_text

ROOT = Path(__file__).resolve().parents[3]
FILE = 'LC001ALP100IV'
SCHEME_FILE = 'LC001ALP000IV'
OUT = ROOT / 'components/MarkBank/cards/irish/higher-2016-p1-authored.json'
SCHEME_MD = ROOT / 'examiner-reports/irish/schemes/2016-hl.md'
SOURCE_REVIEW = ROOT / 'scripts/markbank/authored/irish-higher-2016-p1-source-review.json'
REVIEWED_AT = '2026-11-04'
PAPER_SHA = '8fa9a8c959f27a2692d29c48457024f4e8dd7b640fd1dbd04f761aec9872046f'
SCHEME_SHA = 'f3b2e8729023ab943d91df9d413a569e38917cd560db1af6a665ef901f7f6057'
DIRECTIVE = re.compile(r'rogha|roghna|Freagair|Cuir tic|Ainmnigh|Luaigh|\bchoose\b|\beither\b|\bany\b|one of|\bnó\b|dhá phointe|trí phointe|dhá rud|dó/di|Cuir ciorcal|dhá thagairt|dhá ch|dhá dh|an dá|ceann amháin|amháin|\bdhá\b', re.I)
AUDIO_URL = 'https://www.examinations.ie/archive/exampapers/2016/LC001ZLP017IV.mp3'
SOURCE_NOTE = 'Shown page-for-page from the official examination paper; swipe to move between pages.'
LANGUAGE = ('Scheme PDF 3: “Bainfear ó 0 go 3 ar chaighdeán na Gaeilge.” This 0–3 deduction applies once to the whole '
            'listening section (Tuiscint 60 − Cumas Gaeilge 0–3), never inside a single card.')


def clean(text):
    return re.sub(r'\s+', ' ', symbol_text(text)).strip()


def comparable(text):
    return re.sub(r'[^\w]+', '', text.lower())


def criterion(id, label, marks, guidance, kind='quality'):
    return dict(id=id, label=label, kind='award', maxMarks=marks, permittedMarks=list(range(marks + 1)),
                guidanceKind=kind, guidance=guidance)


def source(ref, pages):
    return dict(kind='source-text', label=ref, title=f'Gaeilge Ardleibhéal 2016 · Páipéar 1 · {ref}', pages=pages,
                attribution='© State Examinations Commission.', presentationNote=SOURCE_NOTE)


def selection_decisions(paper):
    decisions = json.loads(SOURCE_REVIEW.read_text())['selectionDecisions']
    expected = {(d['page'], d['raw']) for d in decisions}
    found = {(i, clean(line)) for i, page in enumerate(paper, 1)
             for line in page.get_text().splitlines() if DIRECTIVE.search(clean(line))}
    assert found == expected, ('Unclassified/stale selection directives', found - expected, expected - found)
    return decisions


class Marked:
    """Scheme text across pages with page markers, so each slice knows its pages."""

    def __init__(self, doc, first, last):
        self.text = ''
        for p in range(first, last + 1):
            body = re.sub(r'^\d+\s', '', clean(doc[p - 1].get_text()))
            self.text += f' ⟦{p}⟧ ' + body

    def split(self, starts, stop, strip=None):
        """Slice at each start; `strip` removes trailing headings BEFORE pages are counted."""
        out, cursor = [], 0
        for i, start in enumerate(starts):
            a = self.text.index(start, cursor)
            b = self.text.index(starts[i + 1], a + len(start)) if i + 1 < len(starts) else self.text.index(stop, a)
            raw = strip(self.text[a:b]) if strip else self.text[a:b]
            pages = {int(re.findall(r'⟦(\d+)⟧', self.text[:a])[-1])}
            pages |= {int(m.group(1)) for m in re.finditer(r'⟦(\d+)⟧([^⟦]*)', raw) if clean(m.group(2))}
            out.append((clean(re.sub(r'⟦\d+⟧', ' ', raw)), sorted(pages)))
            cursor = b
        return out


def material():
    """Lifted paper prompts and scheme text."""
    import fitz
    paper_path = ROOT / f'paper-trail-corpus/exampapers/2016/{FILE}.pdf'
    scheme_path = ROOT / f'paper-trail-corpus/markingschemes/2016/{SCHEME_FILE}.pdf'
    assert hashlib.sha256(paper_path.read_bytes()).hexdigest() == PAPER_SHA, 'Paper changed: repeat visual review'
    assert hashlib.sha256(scheme_path.read_bytes()).hexdigest() == SCHEME_SHA, 'Scheme changed: repeat visual review'
    paper, scheme = fitz.open(paper_path), fitz.open(scheme_path)
    texts = [clean(p.get_text()) for p in paper]
    stext = [clean(p.get_text()) for p in scheme]
    listening = Marked(scheme, 7, 11)
    # (key, id suffix, ref, paper page, topic, part, total, [(n, paper prompt, marks, scheme anchor)])
    segments = [
        ('L-A-F1', 'a-f1', 'Cuid A · Fógra a hAon', 2, 'irish-1-0', 'A', 10, [
            ('1a', '1. (a) Cén eagraíocht a chuir an fógra seo amach?', 2, '1. (a) Cén eagraíocht a chuir an fógra seo amach?'),
            ('1b', '(b) Cén dáta a bheidh an lá speisialta seo ar siúl?', 2, '(b) Cén dáta a bheidh an lá speisialta'),
            ('2a', '2. (a) Cad is aidhm leis an lá seo do scoláirí dara leibhéal?', 2, '2. (a) Cad is aidhm leis an lá seo'),
            ('2b', '(b) Cén táille a bheidh le híoc ag gach scoláire?', 2, '(b) Cén táille a bheidh le híoc'),
            ('3', '3. Cén úsáid a bhainfear as an airgead a bhaileofar?', 2, '3. Cén úsáid a bhainfear')]),
        ('L-A-F2', 'a-f2', 'Cuid A · Fógra a Dó', 2, 'irish-1-0', 'A', 8, [
            ('1a', '1. (a) Cén cúrsa céime atá luaite san fhógra?', 2, '1. (a) Cén cúrsa céime'),
            ('1b', '(b) Cá bhfuil Acadamh na hOllscolaíochta suite?', 2, '(b) Cá bhfuil Acadamh na hOllscolaíochta'),
            ('2', '2. Scríobh síos an dá scil a mhúinfear i rith an chúrsa.', 4, '2. Scríobh síos an dá scil')]),
        ('L-B-C1-M1', 'b-c1-first', 'Cuid B · Comhrá a hAon · An Chéad Mhír', 3, 'irish-1-1', 'B', 8, [
            # The scheme reprints the question as "Cen fáth" (no fada); the card shows the paper's "Cén fáth".
            ('1', '1. Cén fáth a bhfuil aiféala ar Sheán anois i ndiaidh na scrúduithe?', 2, '1. Cen fáth a bhfuil aiféala'),
            ('2', '2. Luaigh an dá bhuntáiste a bhaineann leis an Idirbhliain, dar le Clíona.', 4, '2. Luaigh an dá bhuntáiste'),
            ('3', '3. Cá fhad a chaith Clíona sa Ghaeltacht i mBaile Bhuirne?', 2, '3. Cá fhad a chaith Clíona')]),
        ('L-B-C1-M2', 'b-c1-second', 'Cuid B · Comhrá a hAon · An Dara Mír', 3, 'irish-1-1', 'B', 6, [
            ('1', '1. Cén chuimhne is mó atá ag Clíona ar an Idirbhliain?', 2, '1. Cén chuimhne is mó'),
            ('2', '2. Bhí feachtas bailithe airgid ar siúl i scoil Chlíona. Cé mhéad airgid a bailíodh?', 2, '2. Bhí feachtas bailithe airgid'),
            ('3', '3. Scríobh síos ceann amháin de na himeachtaí a eagraíodh i scoil Chlíona chun airgead a bhailiú.', 2, '3. Scríobh síos ceann amháin')]),
        ('L-B-C2-M1', 'b-c2-first', 'Cuid B · Comhrá a Dó · An Chéad Mhír', 4, 'irish-1-1', 'B', 8, [
            ('1', '1. Cad a bhí ar siúl ag Máire ag an gclub rugbaí aréir?', 2, '1. Cad a bhí ar siúl ag Máire'),
            ('2', '2. Cén fáth a raibh Máire an-neirbhíseach?', 2, '2. Cén fáth a raibh Máire'),
            ('3', '3. Bhí comórtas Chorn an Domhain sa rugbaí go hiontach, dar le Liam. Tabhair dhá chúis lena thuairim.', 4, '3. Bhí comórtas Chorn an Domhain')]),
        ('L-B-C2-M2', 'b-c2-second', 'Cuid B · Comhrá a Dó · An Dara Mír', 4, 'irish-1-1', 'B', 6, [
            ('1', '1. Scríobh síos dhá chúis nach raibh imreoirí na hÉireann go léir ar fáil don chluiche i gcoinne na hAirgintíne, dar le Máire.', 4, '1. Scríobh síos dhá chúis nach raibh'),
            ('2', '2. Cén chéim a thosaigh Paul O’Connell in Ollscoil Luimnigh?', 2, '2. Cén chéim a thosaigh')]),
        ('L-C-P1', 'c-p1', 'Cuid C · Píosa a hAon', 5, 'irish-1-2', 'C', 8, [
            ('1', '1. Cad a cheadaigh Aire Stáit na Gaeltachta don ghrúpa, An Crann Óg?', 2, '1. Cad a cheadaigh Aire Stáit'),
            ('2', '2. Cén fáth ar chuir an comharchumann áitiúil campa samhraidh ar siúl do dhaoine óga?', 2, '2. Cén fáth ar chuir an comharchumann'),
            ('3', '3. Luaigh dhá phointe eolais faoin mbliain ghnóthach a bhí ag an ngrúpa seo sa bhliain 2015.', 4, '3. Luaigh dhá phointe eolais faoin mbliain')]),
        ('L-C-P2', 'c-p2', 'Cuid C · Píosa a Dó', 5, 'irish-1-2', 'C', 6, [
            ('1', '1. Cár rugadh Micheál Ó Cearna?', 2, '1. Cár rugadh'),
            ('2', '2. Cén fáth ar moladh Micheál Ó Cearna nuair a fuair sé bás?', 2, '2. Cén fáth ar moladh'),
            ('3', '3. Luaigh gné amháin de shaol na n-oileánach atá le feiceáil sna taispeántais san ionad seo.', 2, '3. Luaigh gné amháin')]),
    ]
    anchors = [q[3] for seg in segments for q in seg[7]]
    heading = re.compile(r'\s*(FÓGRA A DÓ \(8 marc\)|CUID B \(28 marc\) COMHRÁ A hAON \(14 mharc\) An Chéad Mhír|An Dara Mír|COMHRÁ A DÓ \(14 mharc\) An Chéad Mhír|CUID C \(14 mharc\) PÍOSA A hAON \(8 marc\)|PÍOSA A DÓ \(6 mharc\))\s*$')

    def furniture(raw):
        # The next segment's printed heading precedes the following question; it must not add a page.
        while True:
            trimmed = heading.sub('', re.sub(r'(\s*⟦\d+⟧\s*)+$', '', raw))
            if trimmed == raw:
                return raw
            raw = trimmed
    # 2016 prints the language deduction only on PDF 3; the answer key ends where the cover-mark table begins (PDF 11).
    chunks = iter(listening.split(anchors, 'Léirigh na marcanna mar seo ar chlúdach na Cluastuisceana:', furniture))
    for seg in segments:
        assert sum(q[2] for q in seg[7]) == seg[6], seg[0]
        for i, (n, prompt, marks, anchor) in enumerate(seg[7]):
            chunk, pages = next(chunks)
            assert 'Siombailí' not in chunk and 'Anótála' not in chunk and 'Léirigh na marcanna' not in chunk, (seg[0], n)
            assert not re.search(r'FÓGRA A|COMHRÁ A|PÍOSA A|CUID [ABC]|An Dara Mír|An Chéad Mhír', chunk), (seg[0], n, chunk[-60:])
            assert comparable(prompt) in comparable(texts[seg[3] - 1]), (seg[0], n)
            assert (f'{marks // 2} mharc + {marks // 2} mharc' if marks == 4 else '2 mharc') in chunk, (seg[0], n, chunk[:80])
            seg[7][i] = (n, prompt, marks, chunk, pages)
    for page, line in [(2, 'Cloisfidh tú dhá fhógra raidió sa chuid seo.'), (3, 'Cloisfidh tú dhá chomhrá sa chuid seo.'),
                       (5, 'Cloisfidh tú dhá phíosa nuachta sa chuid seo.')]:
        assert comparable(line) in comparable(texts[page - 1]), page
    assert 'Bainfear ó 0 go 3 ar chaighdeán na Gaeilge.' in stext[2]
    # The cover table (PDF 11) prints the segment totals the cards carry.
    cover = stext[10]
    assert all(x in cover for x in ['Fógra 1 10 marc', 'Fógra 2 8 marc', 'Comhrá 1 14 mharc', 'Comhrá 2 14 mharc', 'Píosa 1 8 marc', 'Píosa 2 6 mharc', 'Iomlán 60 marc'])

    # Composition (scheme PDF 12–15; SMM on PDF 31).
    # The marking text ends where the printed score boxes and the boxed section heading begin.
    marking = stext[11].split('An Mharcáil:', 1)[1].split('Stíl (5) = Ábhar (15) = Gaeilge (80) =', 1)[0].strip()
    assert marking.endswith('ag bun na hiarrachta ceapadóireachta.'), marking[-80:]
    stil = stext[12].split('Stíl chuí scríbhneoireachta (5 mharc):', 1)[1].split('Ionramháil Ábhair (15 mharc):', 1)[0].strip()
    abhar = stext[12].split('Ionramháil Ábhair (15 mharc):', 1)[1].strip()
    gaeilge = [stext[13][stext[13].index('Cumas Gaeilge (80 marc)'):].strip(), stext[14]]
    marking, stil, abhar = [re.sub(r'\s+\d+$', '', t) for t in [marking, stil, abhar]]
    gaeilge = [re.sub(r'\s+\d+$', '', re.sub(r'^\d+\s', '', g)) for g in gaeilge]
    assert stil.startswith('Stíl (5 mharc) = 5 mharc') and abhar.startswith('Tuairimí, smaointe')
    assert all(x in abhar for x in ['13, 14, 15', '11, 12', '9, 10', '6, 7, 8', '3, 4, 5', '0, 1, 2'])
    assert gaeilge[0].endswith('go hiondúil, bíonn coibhneas idir na marcanna.') and 'pionós pro-rata' in gaeilge[0]
    assert all(x in gaeilge[1] for x in ['76-80', '64-67', '52-55', '40-43', '28-31', '16-19', '4-7', '0-3'])
    # 2016 prints neither S1–S4 grades nor a page of short / off-title reductions.
    assert not any(re.search(r'\bS[1-4]\b|róghearr|Easnamhach i gcás', t) for t in stext[11:15])
    smm = stext[30]
    assert 'Scéim Mharcála Mhodhnaithe' in smm and 'Páipéar 1: An Cheapadóireacht – An Cumas Gaeilge (80 marc)' in smm
    # Paper page 6 prints the Treoracha; page 7 the choice and the length note, then the titles.
    head = ('Treoracha d’iarrthóirí\n'
            'Ní mór do na hiarrthóirí cúram a dhéanamh de chruinneas na teanga. Caillfear marcanna má bhítear faillitheach ann.\n'
            'Ní mór ceangal cinnte leanúnach a bheith ann idir an teideal a roghnaítear agus an t-ábhar a scríobhtar.\n\n'
            'Freagair do rogha CEANN AMHÁIN de A, B nó C anseo thíos.\n'
            'Nóta: Ní gá níos mó ná 500-600 focal nó mar sin a scríobh i gcás ar bith.')
    groups = {
        'A': ('AISTE nó ALT NUACHTÁIN / IRISE', 'Scríobh AISTE NÓ ALT NUACHTÁIN / IRISE ar CHEANN AMHÁIN de na hábhair seo.', 'irish-2-0', [
            ('a', 'Fadhb mhór idirnáisiúnta sa lá atá inniu ann.'), ('b', 'Saol na tuaithe in Éirinn faoi láthair.'),
            ('c', 'Cultúr na ndaoine óga.'), ('d', 'Éireannaigh agus an imirce inniu.'),
            ('e', 'Comóradh Éirí Amach na Cásca 1916.')]),
        'B': ('SCÉAL', 'Ceap SCÉAL a mbeadh do rogha CEANN AMHÁIN díobh seo oiriúnach mar theideal air.', 'irish-2-3', [
            ('a', 'Iontas.'), ('b', 'Is fearr an tsláinte ná na táinte.')]),
        'C': ('DÍOSPÓIREACHT / ÓRÁID', 'Freagair do rogha CEANN AMHÁIN díobh seo.', None, [
            ('a', 'Scríobh an chaint a dhéanfá i ndíospóireacht scoile ar son an rúin seo a leanas nó ina aghaidh:\nBíonn saol breá ag na daoine aosta in Éirinn.'),
            ('b', 'Tá tú i do Theachta Dála nua. Iarradh ort píosa cainte a dhéanamh ar chlár raidió ar an ábhar seo:\nNa pleananna atá agam do mo théarma sa Dáil nua.\nScríobh an píosa cainte a dhéanfá ar an ábhar sin.')]),
    }
    for group, (_, instruction, _, titles) in groups.items():
        for letter, title in titles:
            assert all(comparable(line) in comparable(texts[6]) for line in [instruction, *title.splitlines()]), (group, letter)
    treoracha, choice = head.split('\n\n')
    assert all(comparable(line) in comparable(texts[5]) for line in treoracha.splitlines())
    assert all(comparable(line) in comparable(texts[6]) for line in choice.splitlines())
    decisions = selection_decisions(paper)
    return dict(decisions=decisions, paper_path=paper_path, scheme_path=scheme_path, texts=texts, segments=segments, head=head,
                groups=groups, composition=dict(marking=marking, stil=stil, abhar=abhar, gaeilge=gaeilge))


COMPOSITION_REASONS = {
    'A': 'AISTE nó ALT NUACHTÁIN / IRISE is a choice of writing form inside one response, marked by the same Stíl/Ábhar/Gaeilge scheme; it is not a separate route.',
    'B': 'Each printed title is a separate route; the story itself is open.',
    'C': '“ar son … nó ina aghaidh” is the speaker’s stance inside one speech; both stances are marked identically.'}


def build():
    m = material()
    cards = []
    audio = dict(kind='source-audio', title='Triail Chluastuisceana 2016', playbackUrl=AUDIO_URL, secFileid='LC001ZLP017IV.mp3',
                 canonicalUrl=AUDIO_URL, attribution='© State Examinations Commission.',
                 presentationNote='Play the official recording and use the section heading on this card to follow the correct part.')
    for key, suffix, ref, page, topic, part, total, questions in m['segments']:
        criteria = []
        for n, prompt, marks, chunk, _ in questions:
            partial = '= 1 mharc' in chunk
            cr = criterion(f'q{n}', f'Ceist {n[0]}' + (f'({n[1]})' if len(n) > 1 else ''), marks, [chunk], 'exact')
            cr['permittedMarks'] = (list(range(marks + 1)) if partial else list(range(0, marks + 1, 2)))
            criteria.append(cr)
        pages = sorted({p for q in questions for p in q[4]})
        cards.append(dict(
            id=f'irish-2016-hl-p1-listening-{suffix}', year=2016, level='higher', paper=1, section='1',
            questionRef=f'2016 HL Paper 1 Cluastuiscint {ref}', questionText=' '.join(q[1] for q in questions),
            totalMarks=total, topicId=topic, conceptId=f'irish-listening-{suffix}', paperFileid=FILE, schemeFileid=SCHEME_FILE,
            paperPage=page, schemePage=pages[0], schemePages=pages, atlasQuestionId=key, reviewedAt=REVIEWED_AT, reviewedPaperPages=[page],
            taskRequirements=['Éist leis an taifeadadh oifigiúil.', 'Freagair gach mír atá priontáilte ar an gcárta.'],
            criteria=criteria,
            markingGuideNote='The listed responses and tariffs come from the 2016 SEC marking scheme; equivalent wording with the same meaning is accepted. '
                             'Each printed question is marked at its own published tariff (2, or 2 + 2 for two points). ' + LANGUAGE,
            audioMaterial=dict(audio, label=ref), sourceMaterial=source(f'Cluastuiscint {ref}', [page])))
    c = m['composition']
    for group, (form, instruction, topic, titles) in m['groups'].items():
        for letter, title in titles:
            cards.append(dict(
                id=f'irish-2016-hl-p1-composition-{group.lower()}-{letter}', year=2016, level='higher', paper=1, section='1',
                questionRef=f'2016 HL Paper 1 Ceapadóireacht {group}({letter})',
                questionText=m['head'] + f'\n\n{group} · {form} (100 marc)\n{instruction}\n\n({letter}) {title}',
                totalMarks=100, topicId=topic or ('irish-2-4' if letter == 'a' else 'irish-2-5'), conceptId=f'irish-composition-{group.lower()}',
                paperFileid=FILE, schemeFileid=SCHEME_FILE, paperPage=7, schemePage=12, schemePages=[12, 13, 14, 15],
                atlasQuestionId=f'W-{group}-{letter}', reviewedAt=REVIEWED_AT, reviewedPaperPages=[6, 7],
                taskRequirements=['Lean an fhoirm scríbhneoireachta a iarrtar sa cheist.',
                                  'Coinnigh ceangal cinnte leanúnach idir an teideal agus an t-ábhar.', 'Timpeall 500–600 focal.'],
                criteria=[criterion('stil', 'Stíl chuí scríbhneoireachta', 5, [c['stil']]),
                          criterion('abhar', 'Ionramháil Ábhair', 15, [c['abhar'], c['marking']]),
                          criterion('gaeilge', 'Cumas Gaeilge', 80, c['gaeilge'] + [
                              'Scéim Mharcála Mhodhnaithe (scheme PDF 31): for eligible candidates spelling and the listed grammar features are not counted in the 80-mark Cumas Gaeilge award.'])],
                markingGuideNote='Whole 100-mark composition: Stíl 5, Ionramháil Ábhair 15, Cumas Gaeilge 80, assessed as one unit. '
                                 'The 2016 scheme prints no separate reductions for a short attempt; its note on material that is not to the title '
                                 '(a pro-rata penalty on Ábhar and Gaeilge) is part of the Cumas Gaeilge guidance (scheme PDF 14). ' + COMPOSITION_REASONS[group],
                sourceMaterial=source(f'Ceapadóireacht {group}({letter})', [6, 7])))
    listening = [card for card in cards if '-listening-' in card['id']]
    composition = [card for card in cards if '-composition-' in card['id']]
    assert len(listening) == 8 and sum(len(card['criteria']) for card in listening) == 25
    assert sum(card['totalMarks'] for card in listening) == 60 and len(composition) == 9
    assert len({card['id'] for card in cards}) == len(cards) == 17
    for card in cards:
        assert sum(cr['maxMarks'] for cr in card['criteria']) == card['totalMarks'], card['id']
        for cr in card['criteria']:
            assert cr['guidance'] and all(not re.search('[-]', g) for g in cr['guidance']), (card['id'], cr['id'])
    sr = json.loads(SOURCE_REVIEW.read_text())
    review = dict(year=2016, level='higher', paperFileid=FILE + '.pdf', schemeFileid=SCHEME_FILE + '.pdf',
                  paperSha256=PAPER_SHA, schemeSha256=SCHEME_SHA,
                  reviewedPaperPages=list(range(1, 9)), reviewedSchemePages=sr['reviewedSchemePages'],
                  schemeScope=sr['schemeScope'], reviewDate=REVIEWED_AT, status='reviewed',
                  fullPaperAndApplicableSchemeVisualSweep=True, selectionDecisions=m['decisions'],
                  cardIds=[card['id'] for card in cards],
                  listeningSegmentCardIds=[card['id'] for card in listening],
                  compositionRouteCardIds=[card['id'] for card in composition],
                  printedListeningQuestions=sum(len(card['criteria']) for card in listening),
                  examStructure=dict(listening=60, composition=100, total=160),
                  nonPoolDecisions=sr['nonPoolDecisions'], openIssues=[], audio=sr['audio'], caveats=sr['sourceFindings'],
                  boundaries='8 listening segment cards carrying all 25 printed questions as separate criteria at 2 or 2 + 2 (60); '
                             '9 composition title routes at 100 each (choose one).')
    return dict(review=review, cards=cards)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    data = build()
    scheme_words_in(data)  # guidance carries the SEC's words only; question and task checks the paper's (irish_lifted.py)
    import fitz
    scheme = fitz.open(ROOT / f'paper-trail-corpus/markingschemes/2016/{SCHEME_FILE}.pdf')
    # The searchable scheme text the provenance checks read (as 2018–2020 and 2026 write their own).
    scheme_md = '# Gaeilge Ardleibhéal 2016 — SEC marking scheme (Páipéar 1 agus 2)\n\n' + '\n\n'.join(
        f'## PDF page {i + 1}\n\n' + p.get_text() for i, p in enumerate(scheme))
    outputs = {OUT: json.dumps(data, ensure_ascii=False, indent=2) + '\n',
               SCHEME_MD: '\n'.join(line.rstrip() for line in scheme_md.splitlines()).rstrip() + '\n'}
    for path, value in outputs.items():
        if args.check:
            assert path.exists() and path.read_text() == value, f'Stale output: {path}'
        else:
            path.write_text(value)
    print(f"Irish Higher 2016 Paper 1: {len(data['cards'])} reviewed cards ({data['review']['printedListeningQuestions']} printed listening questions); the archive remains incomplete.")


if __name__ == '__main__':
    main()
