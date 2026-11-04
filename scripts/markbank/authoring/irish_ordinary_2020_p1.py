#!/usr/bin/env python3
"""Reviewed 2020 Ordinary Paper 1 (Cluastuiscint agus Ceapadóireacht), carded new.

Paper PDF 1–8 (2020 prints no answer booklet: Cuid A on page 3, the composition
Treoracha on page 6, the titles on page 7, page 8 blank) and the Paper 1 pages of the
combined LC001GLP000IV scheme (PDF 1–11 and 27–28 modified marking) reviewed on
2026-11-04. Scheme PDF 12–26 belong to Paper 2; 29–32 are blank. Counts are
assertions, not corpus-completeness proof. Same layout and method as
irish_ordinary_2021_p1.py: Fógra a hAon is a printed grid of four unnumbered
questions whose answers the scheme prints after Fógra a Dó, the language deduction
is printed only on PDF 3, and the composition scheme has no symbol page and no
short-attempt columns.

No 2020 card existed before. `build` cards the component the way the reviewed
2021–2025 Ordinary Paper 1s are carded: six listening segment cards (the Bank plays
one recording section as one exercise), each printed question its own 3-mark
criterion with its lifted scheme slice, and the nine printed composition titles as
50-mark cards. “Freagair do rogha dhá cheann de A, B, C, D” is a choice, not a route:
each title is its own card and carries the printed instruction as its task check; no
two-section combination cards. `main` writes the card file.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import re
from pathlib import Path
from irish_lifted import PUA, scheme_words_in, symbol_text

ROOT = Path(__file__).resolve().parents[3]
YEAR = 2020
FILE = 'LC001GLP100IV'
SCHEME_FILE = 'LC001GLP000IV'
OUT = ROOT / 'components/MarkBank/cards/irish/ordinary-2020-p1-authored.json'
SOURCE_REVIEW = ROOT / 'scripts/markbank/authored/irish-ordinary-2020-p1-source-review.json'
REVIEWED_AT = '2026-11-04'
PAPER_SHA = 'db0fa4f0fc63d22c5eccd79b92f6fdd4b804dc62cb8f5aa95221dc108f93bea2'
SCHEME_SHA = '6214b57105f533f4650c8acf7082d19a6fdf8cf5df08d8e53b966050a5984d41'
AUDIO_URL = 'https://www.examinations.ie/archive/exampapers/2020/LC001ZLP017IV.mp3'
DIRECTIVE = re.compile(r'rogha|roghna|Freagair|Cuir tic|Ainmnigh|Luaigh|\bnó\b|dhá phointe|dhá rud|dó/di|ceann amháin|amháin|\bdhá\b', re.I)
SOURCE_NOTE = 'Shown page-for-page from the official examination paper; swipe to move between pages.'
LANGUAGE = ('Scheme PDF 3: “Bainfear ó 0 go 6 ar chaighdeán na Gaeilge.” This 0–6 deduction applies once to the whole '
            'listening section (Tuiscint 60 − Cumas Gaeilge 0–6), never inside a single question.')
HEADINGS = re.compile(r'\s*(FÓGRA A DÓ \(12 mharc\)|Cuid B \(24 marc\) COMHRÁ A hAON \(12 mharc\) An Chéad Mhír|An Dara Mír|'
                      r'COMHRÁ A DÓ \(12 mharc\) An Chéad Mhír|Cuid C \(12 mharc\) PÍOSA A hAON \(6 mharc\)|PÍOSA A DÓ \(6 mharc\))\s*$')
# The scheme's text layer splits one printed tariff word (PDF 8, Comhrá a hAon, An Dara Mír, Ceist 2): the page prints "3 mharc".
SPLIT_WORD = ('3 mha rc', '3 mharc')


def clean(text):
    return re.sub(r'\s+', ' ', symbol_text(text)).strip()


def comparable(text):
    return re.sub(r'[^\w]+', '', text.lower())


def criterion(id, label, marks, guidance, kind='quality', permitted=None):
    return dict(id=id, label=label, kind='award', maxMarks=marks, permittedMarks=permitted or list(range(marks + 1)),
                guidanceKind=kind, guidance=guidance)


def source(ref, pages):
    return dict(kind='source-text', label=ref, title=f'Gaeilge Gnáthleibhéal {YEAR} · Páipéar 1 · {ref}', pages=pages,
                attribution='© State Examinations Commission.', presentationNote=SOURCE_NOTE)


def selection_decisions(paper):
    decisions = json.loads(SOURCE_REVIEW.read_text())['selectionDecisions']
    expected = {(d['page'], d['raw']) for d in decisions}
    found = {(i, clean(line)) for i, page in enumerate(paper, 1)
             for line in page.get_text().splitlines() if DIRECTIVE.search(clean(line))}
    assert found == expected, ('Unclassified/stale selection directives', found - expected, expected - found)
    return decisions


class Marked:
    def __init__(self, doc, first, last):
        self.text = ''
        for p in range(first, last + 1):
            self.text += f' ⟦{p}⟧ ' + re.sub(r'^\d+\s', '', clean(doc[p - 1].get_text()))

    def split(self, starts, stop, strip=None):
        """Slice at each start; `strip` removes trailing furniture (headings) BEFORE pages are counted."""
        out, cursor = [], 0
        for i, start in enumerate(starts):
            a = self.text.index(start, cursor)
            b = self.text.index(starts[i + 1], a + len(start)) if i + 1 < len(starts) else self.text.index(stop, a)
            raw = self.text[a:b]
            if strip:
                raw = strip(raw)
            pages = {int(re.findall(r'⟦(\d+)⟧', self.text[:a])[-1])}
            pages |= {int(m.group(1)) for m in re.finditer(r'⟦(\d+)⟧([^⟦]*)', raw) if clean(m.group(2))}
            out.append((clean(re.sub(r'⟦\d+⟧', ' ', raw)), sorted(pages)))
            cursor = a + len(start)
        return out


# (key, card suffix, ref, paper page, topic, [(criterion id, label, paper prompt, scheme anchor, marks)])
SEGMENTS = [
    ('L-A-F1', 'a-f1', 'Cuid A · Fógra a hAon', 3, 'irish-1-0', [
        # A grid ("Líon isteach an t-eolas atá á lorg sa ghreille anseo."): four unnumbered printed questions.
        ('g1', 'Greille 1', 'Cén stáisiún raidió a chuir amach an fógra seo?', 'Cén stáisiún raidió a chuir amach', 3),
        ('g2', 'Greille 2', 'Cén dáta a chuirfear tús leis an gclár nua?', 'Cén dáta a chuirfear tús', 3),
        ('g3', 'Greille 3', 'Scríobh síos lá amháin a bheidh an clár nua ar siúl gach seachtain.', 'Scríobh síos lá amháin a bheidh an clár nua', 3),
        ('g4', 'Greille 4', 'Cén sórt ceoil a bheidh ann sa stiúideo?', 'Cén sórt ceoil a bheidh ann', 3)]),
    ('L-A-F2', 'a-f2', 'Cuid A · Fógra a Dó', 3, 'irish-1-0', [
        ('q1a', 'Ceist 1(a)', 'Cén Ollscoil a sheol an tionscnamh nua?', '1. (a) Cén Ollscoil a sheol', 3),
        ('q1b', 'Ceist 1(b)', 'Cad is ainm don tionscnamh nua seo?', '(b) Cad is ainm don tionscnamh', 3),
        ('q2a', 'Ceist 2(a)', 'Cén cineál cúrsaí a chuireann an tionscnamh seo ar fáil?', '2. (a) Cén cineál cúrsaí', 3),
        ('q2b', 'Ceist 2(b)', 'Cá fhad a mhaireann gach cúrsa?', '(b) Cá fhad a mhaireann', 3)]),
    ('L-B-C1', 'b-c1', 'Cuid B · Comhrá a hAon', 4, 'irish-1-1', [
        ('m1-q1', 'An Chéad Mhír · Ceist 1', 'Conas a mhothaíonn Pól faoi láthair?', '1. Conas a mhothaíonn Pól', 3),
        ('m1-q2', 'An Chéad Mhír · Ceist 2', 'Cén sórt ranganna a chuir na múinteoirí Eacnamaíocht Bhaile ar siúl?', '2. Cén sórt ranganna', 3),
        ('m2-q1', 'An Dara Mír · Ceist 1', 'Cad a bhí ar siúl do na scoláirí sóisearacha ar an lá aclaíochta?', '1. Cad a bhí ar siúl do na scoláirí', 3),
        ('m2-q2', 'An Dara Mír · Ceist 2', 'Scríobh síos rud amháin a chuireann brú mór ar na scoláirí dara leibhéal, dar le hÚna.', '2. Scríobh síos rud amháin a chuireann brú', 3)]),
    ('L-B-C2', 'b-c2', 'Cuid B · Comhrá a Dó', 4, 'irish-1-1', [
        ('m1-q1', 'An Chéad Mhír · Ceist 1', 'Cá bhfuil Ionad Cultúrtha an Phiarsaigh?', '1. Cá bhfuil Ionad Cultúrtha', 3),
        ('m1-q2', 'An Chéad Mhír · Ceist 2', 'Cén sórt Gaeilge a bhí ag teastáil don phost?', '2. Cén sórt Gaeilge', 3),
        ('m2-q1', 'An Dara Mír · Ceist 1', 'Cén áit ina ceantar dúchais a mbíodh Orla ag obair sa samhradh?', '1. Cén áit ina ceantar dúchais', 3),
        ('m2-q2', 'An Dara Mír · Ceist 2', 'Cad a tharla i mí Aibreáin sa cheantar tuaithe ina bhfuil Orla ina cónaí?', '2. Cad a tharla i mí Aibreáin', 3)]),
    ('L-C-P1', 'c-p1', 'Cuid C · Píosa a hAon', 5, 'irish-1-2', [
        ('q1', 'Ceist 1', 'Cén bhliain a rugadh Mary Elmes?', '1. Cén bhliain a rugadh', 3),
        ('q2', 'Ceist 2', 'Cár oibrigh Mary Elmes le linn an Chogaidh Chathartha sa Spáinn?', '2. Cár oibrigh Mary Elmes', 3)]),
    ('L-C-P2', 'c-p2', 'Cuid C · Píosa a Dó', 5, 'irish-1-2', [
        ('q1', 'Ceist 1', 'Cén ról a bhí ag Siya Kolisi ar fhoireann rugbaí na hAfraice Theas?', '1. Cén ról a bhí ag Siya', 3),
        ('q2', 'Ceist 2', 'Scríobh síos rud amháin a thaispeánann go raibh muintir Siya bocht le linn a óige.', '2. Scríobh síos rud amháin a thaispeánann', 3)]),
]
GRID = 'Líon isteach an t-eolas atá á lorg sa ghreille anseo.'
# The questions each card prints, in the 2021–2025 segment-card form (listeningQuestionGroups in SessionScreen.tsx).
SEGMENT_TEXT = {
    'L-A-F1': lambda qs: ' '.join([GRID] + [q[2] for q in qs]),
    'L-A-F2': lambda qs: f'1. (a) {qs[0][2]} (b) {qs[1][2]} 2. (a) {qs[2][2]} (b) {qs[3][2]}',
    'L-B-C1': lambda qs: f'An Chéad Mhír 1. {qs[0][2]} 2. {qs[1][2]} An Dara Mír 1. {qs[2][2]} 2. {qs[3][2]}',
    'L-B-C2': lambda qs: f'An Chéad Mhír 1. {qs[0][2]} 2. {qs[1][2]} An Dara Mír 1. {qs[2][2]} 2. {qs[3][2]}',
    'L-C-P1': lambda qs: f'1. {qs[0][2]} 2. {qs[1][2]}',
    'L-C-P2': lambda qs: f'1. {qs[0][2]} 2. {qs[1][2]}',
}
GROUPS = {
    'A': ('GIOTA LEANÚNACH / BLAG', 'irish-2-6', 'Scríobh giota leanúnach nó blag (leathleathanach nó mar sin) ar cheann amháin de na hábhair seo.', [
        ('i', 'An ceol is fearr liom.'), ('ii', 'Na rudaí a chuireann imní orm.'), ('iii', 'Saoire iontach a bhí agam.')]),
    'B': ('SCÉAL', 'irish-2-3', 'Ceap scéal (leathleathanach nó mar sin) a mbeadh ceann amháin de na sleachta seo a leanas oiriúnach mar thús leis.', [
        ('i', 'Dhúisigh mé i lár na hoíche. Bhí mé i leaba i mbarda ospidéil …'),
        ('ii', 'Bhuail m’fhón póca. D’fhreagair mé an fón …')]),
    'C': ('LITIR / RÍOMHPHOST', 'irish-2-8', None, [
        ('i', 'Thug duine cáiliúil cuairt ar do scoil le déanaí agus labhair an duine sin leis na scoláirí.\n'
              'Scríobh an litir / an ríomhphost (leathleathanach nó mar sin) a chuirfeá chuig cara leat ag insint dó / di faoin gcuairt sin agus faoin gcaint a rinne an duine sin faoina s(h)aol.'),
        ('ii', 'Bhí tú ag cluiche mór le déanaí. Bhí an fhoireann is fearr leat ag imirt.\n'
               'Scríobh an litir / an ríomhphost (leathleathanach nó mar sin) a chuirfeá chuig do dheartháir / do dheirfiúr ag insint dó / di faoin gcluiche mór sin agus faoin seans a fuair tú bualadh leis an imreoir is fearr leat.')]),
    'D': ('COMHRÁ', 'irish-2-9', None, [
        ('i', 'Níl tú sásta leis an airgead póca a thugann do thuismitheoirí duit gach seachtain.\n'
              'Scríobh an comhrá (leathleathanach nó mar sin) a bheadh agat le do thuismitheoirí faoin ábhar sin.'),
        ('ii', 'Tá do rogha cúrsaí tríú leibhéal déanta agat ar fhoirm an CAO.\n'
               'Scríobh an comhrá (leathleathanach nó mar sin) a bheadh agat le do thuismitheoirí faoi do chéad rogha.')]),
}
# Task checks: the 2021–2025 requirement lines (irish_lifted.printed_tasks gives each its printed sentence or English).
LISTENING_REQUIREMENTS = ['Éist leis an taifeadadh oifigiúil.', 'Freagair gach mír atá priontáilte ar an gcárta.']
COMPOSITION_REQUIREMENTS = ['Freagair do rogha dhá cheann de A, B, C, D anseo.', 'Lean an fhoirm scríbhneoireachta a iarrtar sa cheist.',
                            'Coinnigh ceangal cinnte leanúnach idir an teideal agus an t-ábhar.', 'Leathleathanach nó mar sin.']

_MATERIAL = None


def material():
    global _MATERIAL
    if _MATERIAL:
        return _MATERIAL
    import fitz
    paper_path = ROOT / f'paper-trail-corpus/exampapers/{YEAR}/{FILE}.pdf'
    scheme_path = ROOT / f'paper-trail-corpus/markingschemes/{YEAR}/{SCHEME_FILE}.pdf'
    assert hashlib.sha256(paper_path.read_bytes()).hexdigest() == PAPER_SHA, 'Paper changed: repeat visual review'
    assert hashlib.sha256(scheme_path.read_bytes()).hexdigest() == SCHEME_SHA, 'Scheme changed: repeat visual review'
    paper, scheme = fitz.open(paper_path), fitz.open(scheme_path)
    texts = [clean(p.get_text()) for p in paper]
    stext = [clean(p.get_text()) for p in scheme]
    listening = Marked(scheme, 7, 9)
    assert listening.text.count(SPLIT_WORD[0]) == 1
    listening.text = listening.text.replace(*SPLIT_WORD)

    def furniture(raw):
        # The next section's printed heading precedes the following question; it must not add a page.
        while True:
            trimmed = HEADINGS.sub('', re.sub(r'(\s*⟦\d+⟧\s*)+$', '', raw))
            if trimmed == raw:
                return raw
            raw = trimmed
    segments = [(key, suffix, ref, page, topic, list(qs)) for key, suffix, ref, page, topic, qs in SEGMENTS]
    questions = [q for seg in segments for q in seg[5]]
    assert len({q[3] for q in questions}) == len(questions)
    # The scheme prints the Fógra a hAon grid answers after Fógra a Dó (PDF 7), so the slices are cut in the
    # scheme's printed order and returned to the paper's; the key ends where the scheme's mark-total boxes begin.
    ordered = sorted(questions, key=lambda q: listening.text.index(q[3]))
    cut = dict(zip([q[3] for q in ordered], listening.split([q[3] for q in ordered], 'Eolas (60) = Gaeilge (0-6) = Móriomlán (60) =', furniture)))
    assert [q[3] for q in ordered][4:8] == [q[3] for q in questions][:4], 'grid answers expected after Fógra a Dó'
    for seg in segments:
        for i, (cid, label, prompt, anchor, marks) in enumerate(seg[5]):
            chunk, pages = cut[anchor]
            assert comparable(prompt) in comparable(texts[seg[3] - 1]), (seg[0], cid)
            assert chunk.endswith('mharc') and '3 mharc' in chunk and marks == 3, (seg[0], cid, chunk[-60:])
            assert not re.search(r'Cuid [BC] \(|COMHRÁ|PÍOSA|FÓGRA', chunk), (seg[0], cid, chunk[-80:])
            seg[5][i] = (cid, label, prompt, chunk, pages, marks)
    assert sum(len(seg[5]) for seg in segments) == 20 and sum(q[5] for seg in segments for q in seg[5]) == 60
    assert comparable(GRID) in comparable(texts[2])
    # The 2020 scheme prints no general listening note and the language deduction only on PDF 3.
    assert 'Níor chóir a mheas' not in ' '.join(stext[6:9]) and 'Bainfear ó 0 go 6 ar chaighdeán na Gaeilge.' in stext[2]
    assert 'Bainfear' not in ' '.join(stext[6:9])
    intro = {
        'A': 'Cloisfidh tú dhá fhógra raidió sa chuid seo. Cloisfidh tú gach fógra díobh faoi dhó. Beidh sos ann leis na freagraí a scríobh tar éis na chéad éisteachta agus tar éis an dara héisteacht.',
        'B': 'Cloisfidh tú dhá chomhrá sa chuid seo. Cloisfidh tú gach comhrá díobh faoi dhó. Cloisfidh tú an comhrá ó thosach deireadh an chéad uair. Ansin cloisfidh tú ina dhá mhír é. Beidh sos ann leis na freagraí a scríobh tar éis gach míre díobh.',
        'C': 'Cloisfidh tú dhá phíosa nuachta sa chuid seo. Cloisfidh tú gach píosa díobh faoi dhó. Beidh sos ann leis na freagraí a scríobh tar éis na chéad éisteachta agus tar éis an dara héisteacht.'}
    for part, page in [('A', 3), ('B', 4), ('C', 5)]:
        assert comparable(intro[part]) in comparable(texts[page - 1]), part

    # 2020: marking on PDF 10, the 40-mark table on PDF 11, no symbol page and no short-attempt columns.
    # The marking text ends where the printed score boxes and the boxed section heading begin.
    marking = stext[9][stext[9].index('Freagair do rogha dhá cheann'):].split('T (Tasc) (2) = Á (Ábhar) (8) = G (Gaeilge) (40) =', 1)[0].strip()
    assert marking.endswith('ag bun na n-iarrachtaí ceapadóireachta.'), marking[-80:]
    table40 = re.sub(r'^\d+\s', '', stext[10])
    smm = re.sub(r'^\d+\s', '', stext[27])
    assert 'Cuid II' not in marking and 'Tasc = 2 mharc' in marking and 'Ábhar = 8 marc' in marking and 'Cumas Gaeilge = 40 marc' in marking
    assert '34-40' in smm and '0-3' in smm and '95% 38' in table40 and 'M F1 F2 F3' not in ' '.join(stext[9:12])
    head = ('Treoracha d’iarrthóirí\n'
            'Ní mór do na hiarrthóirí cúram a dhéanamh de chruinneas na teanga. Caillfear marcanna má bhítear faillitheach ann. '
            'Ní mór ceangal cinnte leanúnach a bheith ann idir an teideal a roghnaítear agus an t-ábhar a scríobhtar.\n\n'
            'Freagair do rogha dhá cheann de A, B, C, D anseo.')
    assert all(comparable(line) in comparable(texts[5]) for line in head.split('\n\n')[0].splitlines())
    assert comparable(head.split('\n\n')[1]) in comparable(texts[6])
    for group, (form, _, instruction, titles) in GROUPS.items():
        assert comparable(f'{group} – {form} – (50 marc)') in comparable(texts[6]), group
        for roman, title in titles:
            for line in ([instruction] if instruction else []) + title.splitlines():
                assert comparable(line) in comparable(texts[6]), (group, roman, line[:40])
    _MATERIAL = dict(paper=paper, texts=texts, segments=segments, head=head, intro=intro,
                     composition=dict(marking=marking, table40=table40, smm=smm),
                     decisions=selection_decisions(paper))
    return _MATERIAL


def build():
    m = material()
    cards = []
    audio = dict(kind='source-audio', title=f'Triail Chluastuisceana {YEAR}', playbackUrl=AUDIO_URL, secFileid='LC001ZLP017IV.mp3',
                 canonicalUrl=AUDIO_URL, attribution='© State Examinations Commission.',
                 presentationNote='Play the official recording and use the section heading on this card to follow the correct part.')
    for key, suffix, ref, page, topic, questions in m['segments']:
        criteria = []
        for cid, label, prompt, chunk, pages, marks in questions:
            values = {0, 3} | {int(v) for v in re.findall(r'= (\d) mharc', chunk)} | {int(v) for v in re.findall(r'(?<![=\d])\s(\d) mharc', chunk)}
            criteria.append(criterion(cid, label, marks, [chunk], 'exact', permitted=sorted(v for v in values if v <= marks)))
        pages = sorted({p for q in questions for p in q[4]})
        cards.append(dict(
            id=f'irish-{YEAR}-ol-p1-listening-{suffix}', year=YEAR, level='ordinary', paper=1, section='1',
            questionRef=f'{YEAR} OL Paper 1 Cluastuiscint {ref}', questionText=SEGMENT_TEXT[key](questions),
            totalMarks=sum(c['maxMarks'] for c in criteria), topicId=topic, conceptId=f'irish-listening-{suffix}',
            paperPage=page, schemePage=pages[0], taskRequirements=LISTENING_REQUIREMENTS, criteria=criteria,
            markingGuideNote=f'The listed responses and tariffs come from the {YEAR} SEC marking scheme; equivalent wording with the same meaning is accepted. '
                             'Each printed question is marked at its own published 3-mark tariff. ' + LANGUAGE,
            audioMaterial=dict(audio, label=ref), paperFileid=FILE, atlasQuestionId=key, reviewedAt=REVIEWED_AT,
            reviewedPaperPages=[page], schemeFileid=SCHEME_FILE, schemePages=pages, sourceMaterial=source(f'Cluastuiscint {ref}', [page])))
    c = m['composition']
    for group, (form, topic, instruction, titles) in GROUPS.items():
        for roman, title in titles:
            body = m['head'] + f'\n\n{group} · {form} (50 marc)\n' + (instruction + '\n' if instruction else '') + f'({roman}) {title}'
            cards.append(dict(
                id=f'irish-{YEAR}-ol-p1-composition-{group.lower()}-{roman}', year=YEAR, level='ordinary', paper=1, section='1',
                questionRef=f'{YEAR} OL Paper 1 Ceapadóireacht {group}({roman})', questionText=body, totalMarks=50, topicId=topic,
                conceptId=f'irish-composition-{group.lower()}', paperPage=7, schemePage=10, taskRequirements=COMPOSITION_REQUIREMENTS,
                criteria=[criterion('tasc', 'An Tasc', 2, [c['marking'].split('An tÁbhar (8 marc)')[0]], permitted=[0, 2]),
                          criterion('abhar', 'An tÁbhar', 8, [c['marking'].split('An tÁbhar (8 marc)', 1)[1].split('An Cumas Gaeilge (40 marc)')[0]]),
                          criterion('gaeilge', 'An Cumas Gaeilge', 40, [c['marking'].split('An Cumas Gaeilge (40 marc)', 1)[1], c['table40'],
                                    'Scéim Mharcála Mhodhnaithe (scheme PDF 27–28): eligible candidates are assessed on named grammar features (bands 34–40 … 0–3); spelling is not counted.'])],
                markingGuideNote=f'Whole 50-mark composition: Tasc 2, Ábhar 8, Cumas Gaeilge 40. The {YEAR} scheme prints the 40-mark table (scheme PDF 11) '
                                 'and, for modified marking, the bands 34–40 … 0–3 (PDF 28), so the Cumas Gaeilge award can take any value from 0 to 40. '
                                 'The letter or email and its recipient wording (C), the conversation partner (D), and the dó/di and s(h)aol forms, are flexible forms inside one response, not separate routes.',
                paperFileid=FILE, atlasQuestionId=f'W-{group}-{roman}', reviewedAt=REVIEWED_AT, reviewedPaperPages=[6, 7],
                schemeFileid=SCHEME_FILE, schemePages=[10, 11], sourceMaterial=source(f'Ceapadóireacht {group}({roman})', [6, 7])))
    assert len(cards) == 15 and len({x['id'] for x in cards}) == 15 and len({x['atlasQuestionId'] for x in cards}) == 15
    for card in cards:
        assert sum(cr['maxMarks'] for cr in card['criteria']) == card['totalMarks'], card['id']
        for cr in card['criteria']:
            assert cr['guidance'] and all(not PUA.search(g) and 'Siombailí' not in g for g in cr['guidance']), (card['id'], cr['id'])
    sr = json.loads(SOURCE_REVIEW.read_text())
    listening_ids = [x['id'] for x in cards if '-listening-' in x['id']]
    composition_ids = [x['id'] for x in cards if '-composition-' in x['id']]
    review = dict(year=YEAR, level='ordinary', paperFileid=FILE + '.pdf', schemeFileid=SCHEME_FILE + '.pdf',
                  paperSha256=PAPER_SHA, schemeSha256=SCHEME_SHA,
                  reviewedPaperPages=list(range(1, 9)), reviewedSchemePages=sr['reviewedSchemePages'], schemeScope=sr['schemeScope'],
                  reviewDate=REVIEWED_AT, status='reviewed', fullPaperAndApplicableSchemeVisualSweep=True, selectionDecisions=m['decisions'],
                  cardIds=listening_ids + composition_ids, listeningSegmentCardIds=listening_ids, compositionRouteCardIds=composition_ids,
                  printedListeningQuestions=20, examStructure=dict(listening=60, composition=100, total=160),
                  nonPoolDecisions=sr['nonPoolDecisions'], openIssues=[], audio=sr['audio'], caveats=sr['sourceFindings'],
                  choicePolicy='Choice is not a route: each printed composition title is one card carrying the printed choose-two instruction; no combination cards.',
                  boundaries='6 listening segment cards carrying all 20 printed questions as separate criteria (3 each) (60); '
                             '9 composition titles at 50 (answer any two; no combination cards).')
    return dict(review=review, cards=cards)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    data = build()
    scheme_words_in(data)  # guidance, question and task checks carry the SEC's words only (irish_lifted.py)
    import fitz
    scheme = fitz.open(ROOT / f'paper-trail-corpus/markingschemes/{YEAR}/{SCHEME_FILE}.pdf')
    # The searchable scheme text the provenance checks read (as 2026 writes its own).
    scheme_md = f'# Gaeilge Gnáthleibhéal {YEAR} — SEC marking scheme (Páipéar 1 agus 2)\n\n' + '\n\n'.join(
        f'## PDF page {i + 1}\n\n' + p.get_text() for i, p in enumerate(scheme))
    outputs = {OUT: json.dumps(data, ensure_ascii=False, indent=2) + '\n',
               ROOT / f'examiner-reports/irish/schemes/{YEAR}-ol.md': '\n'.join(line.rstrip() for line in scheme_md.splitlines()).rstrip() + '\n'}
    for path, value in outputs.items():
        if args.check:
            assert path.exists() and path.read_text() == value, f'Stale output: {path}'
        else:
            path.write_text(value)
    print(f"Irish Ordinary {YEAR} Paper 1: {len(data['cards'])} reviewed cards (20 printed listening questions, 9 titles); the archive remains incomplete.")


if __name__ == '__main__':
    main()
