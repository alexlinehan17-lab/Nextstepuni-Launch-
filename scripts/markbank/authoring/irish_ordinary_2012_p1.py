#!/usr/bin/env python3
"""Reviewed 2012 Ordinary Paper 1 (Cluastuiscint agus Ceapadóireacht), carded new.

Paper PDF 1–8 (2012 prints no answer booklet: Cuid A on page 3, B on 4, C on 5, the
composition Treoracha on page 6, the titles on page 7, page 8 blank) and the Paper 1
pages of the combined LC001GLP000IV scheme (PDF 1–8, and 14 Socruithe Réasúnta)
reviewed on 2026-11-05. Scheme PDF 9–13 belong to Paper 2; 15 and 16 are empty. Counts
are assertions, not corpus-completeness proof. Same card shapes as
irish_ordinary_2013_p1.py, with what the 2012 scheme prints instead:

- no listening key. The scheme prints each section's tariff (PDF 4–5: “Fógra 1: 3 marc ×
  4 = 12 marc”, “Comhrá 1: 3 marc × 4 = 12 mharc”, “Píosa 1: 3 marc × 2 = 6 mharc” …), the
  0–6 language deduction (PDF 5) and the recording's script (PDF 5–8), and no answer for
  any question. Each printed question is still its own criterion at its printed 3 marks
  (every printed ask gets a card): its guidance is the question as the paper prints it,
  then the section's printed tariff; the card says in English that the scheme prints no
  answer for this part. Nothing is taken from the script: choosing the sentence that
  answers a question would be writing a key the SEC never printed.
- the multiplication sign of the tariff pages (PDF 4, 5 and 8) is a SymbolMT glyph, which
  the text layer gives as the private-use U+F0B4 (and PDF 14's bullets as U+F0B7);
  `page_text` reads each span with its font, as 2013's builder does.
- composition marking on PDF 8 in 2013's printed blocks (the tariffs; the bracketed
  Cumas Gaeilge definition, (i) Stór Gaeilge 40%, (ii) beachtas 50% agus litriú 10%; the
  bracketed content note; the examiner's Nóta; and a bracketed Nóta on the “Gaeilge
  Lochtach” of the Paper 2 questions after it), no 40-mark table, and its heading
  misprinting the section as “120 MARC” (the paper prints 100, and the scheme's own
  tariffs add to 100). PDF 14 prints the Socruithe Réasúnta instruction (spelling and
  certain grammar features not counted for candidates granted it), with no bands.

No 2012 Ordinary card existed before. `build` cards the component the way the reviewed
2013–2025 Ordinary Paper 1s are carded: six listening segment cards (the Bank plays one
recording section as one exercise), each printed question its own criterion, and the nine
printed composition titles as 50-mark cards. “Freagair do rogha dhá cheann de A, B, C, D”
is a choice, not a route: each title is its own card and carries the printed instruction
as its task check; no two-section combination cards. `main` writes the card file.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import re
from pathlib import Path
from irish_lifted import PUA, scheme_words_in, symbol_text

ROOT = Path(__file__).resolve().parents[3]
YEAR = 2012
FILE = 'LC001GLP100IV'
SCHEME_FILE = 'LC001GLP000IV'
OUT = ROOT / 'components/MarkBank/cards/irish/ordinary-2012-p1-authored.json'
SCHEME_MD = ROOT / f'examiner-reports/irish/schemes/{YEAR}-ol.md'
SOURCE_REVIEW = ROOT / 'scripts/markbank/authored/irish-ordinary-2012-p1-source-review.json'
REVIEWED_AT = '2026-11-05'
PAPER_SHA = 'c0d17998b5482062b5bdd4179faf1fa1a011aa0e0fb141a14e5fc4af03fd24fb'
SCHEME_SHA = 'be4c4acab9de2f39e527fd72d22df0741ec5e464a301f481c49aee8c62e65af8'
# The 2012 common recording is filed with a letter O, not a zero, in its name (“…ZLPO17IV”); the zero spelling is not served.
AUDIO_FILE = 'LC001ZLPO17IV.mp3'
AUDIO_URL = f'https://www.examinations.ie/archive/exampapers/{YEAR}/{AUDIO_FILE}'
DIRECTIVE = re.compile(r'rogha|roghna|Freagair|Cuir tic|Ainmnigh|Luaigh|\bnó\b|dhá phointe|dhá rud|dó/di|ceann amháin|amháin|\bdhá\b', re.I)
SOURCE_NOTE = 'Shown page-for-page from the official examination paper; swipe to move between pages.'
UNPRINTED_ANSWER = 'The scheme prints no answer for this part.'  # types/markBank.ts
LANGUAGE = ('Scheme PDF 5: “Bainfear ó 0 go 6 ar chaighdeán na Gaeilge.” This 0–6 deduction applies once to the whole '
            'listening section (Tuiscint 60 − Cumas Gaeilge 0–6), never inside a single question.')
NO_KEY = (f'{UNPRINTED_ANSWER} The {YEAR} scheme prints each listening section’s tariff (3 marks a question, PDF 4–5) and the '
          'recording’s script (PDF 5–8), but no answer key: each printed question is claimed whole at its 3 marks, and nothing '
          'is taken from the script as an answer.')
# The scheme's text layer gives its SymbolMT glyphs as private-use code points: the multiplication sign of the tariff pages
# (PDF 4, 5 and 8) as U+F0B4 and the Socruithe Réasúnta bullets (PDF 14) as U+F0B7; Adobe Symbol draws them as × and •.
SYMBOL_FONT = {'': '×', '': '•', ' ': ' '}


def clean(text):
    return re.sub(r'\s+', ' ', symbol_text(text)).strip()


def comparable(text):
    return re.sub(r'[^\w]+', '', text.lower())


def page_text(page):
    """The page's text with each SymbolMT glyph as the character it draws (every glyph is one SYMBOL_FONT reviewed)."""
    lines = []
    for block in page.get_text('dict')['blocks']:
        for line in block.get('lines', []):
            parts = []
            for span in line['spans']:
                text = span['text']
                if span['font'] == 'SymbolMT':
                    assert all(c in SYMBOL_FONT for c in text), ('Unreviewed scheme glyph', page.number + 1, repr(text))
                    text = ''.join(SYMBOL_FONT[c] for c in text)
                parts.append(text)
            lines.append(''.join(parts))
    return '\n'.join(lines)


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


# (key, card suffix, ref, paper page, topic, the section's printed tariff (scheme PDF), [(criterion id, label, paper prompt)])
SEGMENTS = [
    ('L-A-F1', 'a-f1', 'Cuid A · Fógra a hAon', 3, 'irish-1-0', ('Fógra 1: 3 marc × 4 = 12 marc', 4), [
        # A grid (“Líon isteach an t-eolas atá á lorg sa ghreille anseo.”): four unnumbered printed questions.
        ('g1', 'Greille 1', 'Cén post atá i gceist san fhógra seo?'),
        ('g2', 'Greille 2', 'Cén contae ina bhfuil an scoil seo suite?'),
        ('g3', 'Greille 3', 'Cé mhéad dalta atá ag freastal ar an scoil seo?'),
        ('g4', 'Greille 4', 'Cad é an lá deireanach le haghaidh iarratas?')]),
    ('L-A-F2', 'a-f2', 'Cuid A · Fógra a Dó', 3, 'irish-1-0', ('Fógra 2: 3 marc × 4 = 12 marc', 4), [
        ('q1a', 'Ceist 1(a)', 'Cathain a rinneadh an ceiliúradh speisialta?'),
        ('q1b', 'Ceist 1(b)', 'Tabhair píosa amháin eolais faoi Dhara Ó Cinnéide.'),
        ('q2a', 'Ceist 2(a)', 'Cén leabhar as ar léigh na daltaí scoile?'),
        ('q2b', 'Ceist 2(b)', 'Cén tír a bhfuil ceangal láidir aici le Corca Dhuibhne?')]),
    ('L-B-C1', 'b-c1', 'Cuid B · Comhrá a hAon', 4, 'irish-1-1', ('Comhrá 1: 3 marc × 4 = 12 mharc', 4), [
        ('m1-q1', 'An Chéad Mhír · Ceist 1', 'Cén uair a cuireadh amach an taighde seo?'),
        ('m1-q2', 'An Chéad Mhír · Ceist 2', 'Cén áit ar cheart seans a bheith ag daoine óga a dhul?'),
        ('m2-q1', 'An Dara Mír · Ceist 1', 'Luaigh rud amháin a deirtear faoi dhaoine óga sa taighde seo.'),
        ('m2-q2', 'An Dara Mír · Ceist 2', 'Cad é an lá scoile atá ag Rónán faoi láthair?')]),
    ('L-B-C2', 'b-c2', 'Cuid B · Comhrá a Dó', 4, 'irish-1-1', ('Comhrá 2: 3 marc × 4 = 12 mharc', 4), [
        ('m1-q1', 'An Chéad Mhír · Ceist 1', 'Cá raibh an searmanas speisialta seo ar siúl?'),
        ('m1-q2', 'An Chéad Mhír · Ceist 2', 'Cé mhéad ama a thóg sé ar Ronnie Delaney an rás sin 1500 méadar a rith?'),
        ('m2-q1', 'An Dara Mír · Ceist 1', 'Cén post a bhí ag athair Ronnie Delaney?'),
        ('m2-q2', 'An Dara Mír · Ceist 2', 'Cén chuid dá chorp a ghortaigh Ronnie Delaney?')]),
    ('L-C-P1', 'c-p1', 'Cuid C · Píosa a hAon', 5, 'irish-1-2', ('Píosa 1: 3 marc × 2 = 6 mharc', 5), [
        ('q1', 'Ceist 1', 'Cathain a seoladh an leabhar Waves of Tory?'),
        # The paper misprints “fhilleann” as “fhillleann”: kept as printed.
        ('q2', 'Ceist 2', 'Cathain a fhillleann an t-údar ar Thoraí?')]),
    ('L-C-P2', 'c-p2', 'Cuid C · Píosa a Dó', 5, 'irish-1-2', ('Píosa 2: 3 marc × 2 = 6 marc', 5), [
        ('q1', 'Ceist 1', 'Cé mhéad seomra a bheidh sna tithe nua?'),
        ('q2', 'Ceist 2', 'Cén uimhir theileafóin atá ag Oifigí an Chomharchumainn?')]),
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
    'A': ('GIOTA LEANÚNACH / BLAG', 'irish-2-6', 'Scríobh giota leanúnach nó blag ar cheann amháin de na hábhair seo.', [
        ('i', 'Mo laethanta ar scoil.'), ('ii', 'Saoire iontach a bhí agam.'), ('iii', 'An teilifís – is breá liom é.')]),
    'B': ('SCÉAL', 'irish-2-3', 'Ceap scéal a mbeidh ceann amháin de na sleachta seo a leanas oiriúnach mar thús leis.', [
        # The paper prints “Léim mo chroi” without the fada on “chroí”: kept as printed.
        ('i', 'Chonaic mé an liathróid ag teacht i mo threo. D’fhéach mé timpeall orm, ní raibh aon duine in aice liom. Léim mo chroi le háthas…'),
        ('ii', '“Uisce! Uisce! Tabhair dom uisce,” arsa mise os ard….')]),
    'C': ('LITIR / RÍOMHPHOST', 'irish-2-8', None, [
        ('i', 'Tá tú ag caitheamh dhá mhí saoire ag taisteal le do chlann san Astráil.\n'
              'Scríobh an litir/ríomhphost a chuirfeá chuig cara leat ag insint dó/di faoi na rudaí éagsúla a tharla agus tú san Astráil.'),
        ('ii', 'Chuala tú polaiteoir ar an teilifís agus é ag gearán / ag tabhairt amach faoi dhaoine óga.\n'
               'Scríobh an litir/ríomhphost a chuirfeá chuige faoi na rudaí a dúirt sé.')]),
    'D': ('COMHRÁ', 'irish-2-9', None, [
        ('i', 'Ba bhreá leat dul go dtí scannán sa chathair ach níl do chara cinnte.\n'
              'Scríobh an comhrá a bheadh idir an bheirt agaibh, ó bhéal nó ar líne, faoin ábhar sin.'),
        ('ii', 'An cheist mhór: Cad a dhéanfaidh tú tar éis na hArdteistiméireachta?\n'
               'Scríobh an comhrá a bheadh agat le do thuismitheoirí faoi sin.')]),
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
    stext = [clean(page_text(p)) for p in scheme]
    assert len(paper) == 8 and len(scheme) == 16
    # The listening tariffs: each section's line printed once on PDF 4–5, with the part totals and the 0–6 deduction.
    for key, suffix, ref, page, topic, (tariff, spage), questions in SEGMENTS:
        assert stext[spage - 1].count(tariff) == 1, (key, tariff)
        for cid, label, prompt in questions:
            assert comparable(prompt) in comparable(texts[page - 1]), (key, cid)
    assert sum(len(q) for *_, q in SEGMENTS) == 20
    assert 'Cuid A: 24 marc (Eolas)' in stext[3] and 'Cuid B: 24 marc (Eolas)' in stext[3] and '12 + 12 = 24 marc' in stext[3]
    # PDF 5's Cuid C line misprints the part's total as “20 marc (Eolas)” above “6 + 6+ = 12 mharc” (as 2013's scheme does).
    assert 'Cuid C: 20 marc (Eolas)' in stext[4] and '6 + 6+ = 12 mharc 24 + 24 + 12 = 60' in stext[4]
    assert 'Bainfear ó 0 go 6 ar chaighdeán na Gaeilge .' in stext[4]
    # No answer key anywhere: the script runs PDF 5–8 (Fógra 1 to Píosa 2), and no listening question of the paper is reprinted.
    assert stext[4].index('CUID A Fógra 1') > stext[4].index('Bainfear') and 'Píosa 2 Tá Comharchumann Inis Meáin' in stext[6]
    assert stext[7].index('glaoigh ar oifigí an Chomharchumainn ag (098) 40267.') < stext[7].index('CEIST 2 - CEAPADÓIREACHT')
    for *_, questions in SEGMENTS:
        for cid, label, prompt in questions:
            assert comparable(prompt) not in comparable(' '.join(stext)), ('a listening question reprinted in the scheme', prompt)
    assert comparable(GRID) in comparable(texts[2])
    intro = {
        'A': 'Cloisfidh tú dhá fhógra raidió sa chuid seo. Cloisfidh tú gach fógra díobh faoi dhó. Beidh sos ann leis na freagraí a scríobh tar éis na chéad éisteachta agus tar éis an dara héisteacht.',
        'B': 'Cloisfidh tú dhá chomhrá sa chuid seo. Cloisfidh tú gach comhrá díobh faoi dhó. Cloisfidh tú an comhrá ó thosach deireadh an chéad uair. Ansin cloisfidh tú ina dhá mhír é. Beidh sos ann leis na freagraí a scríobh tar éis gach míre díobh.',
        'C': 'Cloisfidh tú dhá phíosa nuachta sa chuid seo. Cloisfidh tú gach píosa díobh faoi dhó. Beidh sos ann leis na freagraí a scríobh tar éis na chéad éisteachta agus tar éis an dara héisteacht.'}
    for part, page in [('A', 3), ('B', 4), ('C', 5)]:
        assert comparable(intro[part]) in comparable(texts[page - 1]), part

    # 2012: composition marking on PDF 8 in printed blocks (2013's layout): the tariffs; the bracketed Cumas Gaeilge definition,
    # (i) Stór Gaeilge 40% and (ii) beachtas 50% agus litriú 10%; the bracketed content note; the examiner's Nóta; and a bracketed
    # Nóta on the “Gaeilge Lochtach” of the questions that follow (Paper 2). No 40-mark table, no short-attempt columns.
    assert 'CEIST 2 - CEAPADÓIREACHT - 120 MARC Freagair do rogha dhá cheann' in stext[7]
    marking = stext[7][stext[7].index('Freagair do rogha dhá cheann'):]
    tariffs, rest = marking.split(' [Cumas Gaeilge = (i) ', 1)
    cumas, rest = rest.split(' [Gearrfar pionós', 1)
    content, rest = rest.split('] Nóta: ', 1)
    nota, lochtach = rest.split(' [Nóta: Maidir le', 1)
    tariffs, cumas = tariffs.strip(), '[Cumas Gaeilge = (i) ' + cumas.strip()
    content, nota = '[Gearrfar pionós' + content + ']', 'Nóta: ' + nota.strip()
    assert tariffs.endswith('Leathleathanach nó breis: Tasc = 2 mharc Ábhar = 8 marc = 50 marc × 2 Cumas Gaeilge = 40 marc = 100 marc'), tariffs
    assert cumas.endswith('(= 50%) agus litriú (= 10%).]') and '(= 40%)' in cumas, cumas[-60:]
    assert content == '[Gearrfar pionós ar iarrthóirí mura mbeidh na hiarrachtaí ceapadóireachta ad rem.]', content
    # The examiner's Nóta misprints “Tasc” as “Tásc”: kept as printed.
    assert nota.startswith('Nóta: Caithfidh an Scrúdaitheoir an marc a bhronntar as 2 (Tásc)') and nota.endswith('ag bun na n-iarrachtaí ceapadóireachta.'), nota
    assert lochtach.startswith(' ‘Gaeilge Lochtach’ a luaitear leis na ceisteanna ina dhiaidh seo') and lochtach.endswith('40% : 60%]'), lochtach[:80]
    # PDF 14: the Socruithe Réasúnta instruction (spelling and certain grammar features not counted), no bands; PDF 15–16 empty.
    assert stext[13].startswith('12 Socruithe Réasúnta') and 'ach amháin nach mbeidh an litriú ná gnéithe áirithe den ghramadach san áireamh' in stext[13]
    assert not stext[14] and not stext[15]
    assert '95%' not in ' '.join(stext) and '34-40' not in ' '.join(stext)
    head = ('Treoracha d’iarrthóirí\n'
            'Ní mór do na hiarrthóirí cúram a dhéanamh de chruinneas na teanga. Caillfear marcanna má bhítear faillitheach ann. '
            'Ní mór ceangal cinnte leanúnach a bheith ann idir an teideal a roghnaítear agus an t-ábhar a scríobhtar.\n\n'
            'Freagair do rogha dhá cheann de A, B, C, D anseo. Ní mór leathleathanach nó mar sin a scríobh sa dá fhreagra.')
    assert all(comparable(line) in comparable(texts[5]) for line in head.split('\n\n')[0].splitlines())
    assert comparable(head.split('\n\n')[1]) in comparable(texts[6])
    for group, (form, _, instruction, titles) in GROUPS.items():
        assert comparable(f'{group} – {form} – (50 marc)') in comparable(texts[6]), group
        for roman, title in titles:
            for line in ([instruction] if instruction else []) + title.splitlines():
                assert comparable(line) in comparable(texts[6]), (group, roman, line[:40])
    _MATERIAL = dict(paper=paper, texts=texts, head=head, intro=intro,
                     composition=dict(tariffs=tariffs, cumas=cumas, content=content, nota=nota),
                     decisions=selection_decisions(paper))
    return _MATERIAL


def build():
    m = material()
    cards = []
    audio = dict(kind='source-audio', title=f'Triail Chluastuisceana {YEAR}', playbackUrl=AUDIO_URL, secFileid=AUDIO_FILE,
                 canonicalUrl=AUDIO_URL, attribution='© State Examinations Commission.',
                 presentationNote='Play the official recording and use the section heading on this card to follow the correct part.')
    for key, suffix, ref, page, topic, (tariff, spage), questions in SEGMENTS:
        # The criterion carries its own printed question first, then the only price the scheme prints for it (the section's
        # “3 marc × N” line); the scheme prints no answer, so the question is claimed whole at its 3 marks (0 or 3).
        # The scheme prints only the tariff for these questions: the chip says "Tariff" (coordinator, batch 7).
        criteria = [dict(criterion(cid, label, 3, [prompt, tariff], 'exact', permitted=[0, 3]), tariffOnly=True) for cid, label, prompt in questions]
        cards.append(dict(
            id=f'irish-{YEAR}-ol-p1-listening-{suffix}', year=YEAR, level='ordinary', paper=1, section='1',
            questionRef=f'{YEAR} OL Paper 1 Cluastuiscint {ref}', questionText=SEGMENT_TEXT[key](questions),
            totalMarks=sum(c['maxMarks'] for c in criteria), topicId=topic, conceptId=f'irish-listening-{suffix}',
            paperPage=page, schemePage=spage, taskRequirements=LISTENING_REQUIREMENTS, criteria=criteria,
            markingGuideNote=f'Each printed question is marked at its own published tariff (3 marks), from the {YEAR} SEC marking scheme. '
                             + NO_KEY + ' ' + LANGUAGE,
            audioMaterial=dict(audio, label=ref), paperFileid=FILE, atlasQuestionId=key, reviewedAt=REVIEWED_AT,
            reviewedPaperPages=[page], schemeFileid=SCHEME_FILE, schemePages=[spage], sourceMaterial=source(f'Cluastuiscint {ref}', [page])))
    c = m['composition']
    for group, (form, topic, instruction, titles) in GROUPS.items():
        for roman, title in titles:
            body = m['head'] + f'\n\n{group} · {form} (50 marc)\n' + (instruction + '\n' if instruction else '') + f'({roman}) {title}'
            cards.append(dict(
                id=f'irish-{YEAR}-ol-p1-composition-{group.lower()}-{roman}', year=YEAR, level='ordinary', paper=1, section='1',
                questionRef=f'{YEAR} OL Paper 1 Ceapadóireacht {group}({roman})', questionText=body, totalMarks=50, topicId=topic,
                conceptId=f'irish-composition-{group.lower()}', paperPage=7, schemePage=8, taskRequirements=COMPOSITION_REQUIREMENTS,
                # 2012 prints no headed Tasc/Ábhar sections: the tariff block prices the task, the bracketed note is the
                # scheme's content guidance, and the Cumas Gaeilge definition and the Nóta go with Gaeilge (two printed blocks,
                # two lines, as 2013).
                criteria=[criterion('tasc', 'An Tasc', 2, [c['tariffs']], permitted=[0, 2]),
                          criterion('abhar', 'An tÁbhar', 8, [c['content']]),
                          criterion('gaeilge', 'An Cumas Gaeilge', 40, [c['cumas'], c['nota']])],
                markingGuideNote=f'Whole 50-mark composition: Tasc 2, Ábhar 8, Cumas Gaeilge 40. The {YEAR} scheme prints no 40-mark table: '
                                 'Cumas Gaeilge is judged on its printed aspects, (i) the range and richness of the candidate’s Irish (40%) and '
                                 '(ii) accuracy in the main features of correct Irish (50%) and spelling (10%), so the award can take any value from 0 to 40. '
                                 'Socruithe Réasúnta (scheme PDF 14): for candidates granted reasonable accommodations, spelling and certain grammar '
                                 'features are not counted; the scheme prints no bands for it. '
                                 'The letter or email (C) and the dó/di wording are flexible forms inside one response, not separate routes.',
                paperFileid=FILE, atlasQuestionId=f'W-{group}-{roman}', reviewedAt=REVIEWED_AT, reviewedPaperPages=[6, 7],
                schemeFileid=SCHEME_FILE, schemePages=[8], sourceMaterial=source(f'Ceapadóireacht {group}({roman})', [6, 7])))
    assert len(cards) == 15 and len({x['id'] for x in cards}) == 15 and len({x['atlasQuestionId'] for x in cards}) == 15
    for card in cards:
        assert sum(cr['maxMarks'] for cr in card['criteria']) == card['totalMarks'], card['id']
        for cr in card['criteria']:
            assert cr['guidance'] and all(not PUA.search(g) for g in cr['guidance']), (card['id'], cr['id'])
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
                  boundaries='6 listening segment cards carrying all 20 printed questions as separate criteria, each at 3 (60; the scheme prints no '
                             'answer key); 9 composition titles at 50 (answer any two; no combination cards).')
    return dict(review=review, cards=cards)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    data = build()
    scheme_words_in(data)  # guidance, question and task checks carry the SEC's words only (irish_lifted.py)
    import fitz
    scheme = fitz.open(ROOT / f'paper-trail-corpus/markingschemes/{YEAR}/{SCHEME_FILE}.pdf')
    # The searchable scheme text the provenance checks read (as 2013, 2014, 2016, 2018, 2020 and 2026 write their own), with its
    # SymbolMT glyphs read as `page_text` reads them.
    scheme_md = f'# Gaeilge Gnáthleibhéal {YEAR} — SEC marking scheme (Páipéar 1 agus 2)\n\n' + '\n\n'.join(
        f'## PDF page {i + 1}\n\n' + page_text(p) for i, p in enumerate(scheme))
    outputs = {OUT: json.dumps(data, ensure_ascii=False, indent=2) + '\n',
               SCHEME_MD: '\n'.join(line.rstrip() for line in scheme_md.splitlines()).rstrip() + '\n'}
    for path, value in outputs.items():
        if args.check:
            assert path.exists() and path.read_text() == value, f'Stale output: {path}'
        else:
            path.write_text(value)
    print(f"Irish Ordinary {YEAR} Paper 1: {len(data['cards'])} reviewed cards (20 printed listening questions, 9 titles); the archive remains incomplete.")


if __name__ == '__main__':
    main()
