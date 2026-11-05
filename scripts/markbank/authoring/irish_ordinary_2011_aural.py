#!/usr/bin/env python3
"""Reviewed 2011 Ordinary Triail Chluastuisceana (the listening test, its own paper in 2011), carded new.

Paper PDF 1–4 (LC001GLPA00IV, a four-page answer booklet: the examiner's box and Cuid A's first announcement on page 1,
Fógra a Dó, Fógra a Trí and Comhrá a hAon's first mír on 2, Comhrá a hAon's second mír to Comhrá a Trí's first on 3,
Comhrá a Trí's second mír and Cuid C on 4) and the listening page of the combined LC001GLP000IV scheme (PDF 10)
reviewed on 2026-11-05. Scheme PDF 3–4 belong to Páipéar I, 5–9 to Páipéar II, 11 prints the Socruithe Réasúnta
instruction and 12 is empty. Counts are assertions, not corpus-completeness proof.

Before 2012 the listening test was a paper of its own (“TRIAIL CHLUASTUISCEANA (120 marc)”) sat after Páipéar I, with
three items in each part: Cuid A three announcements, Cuid B three conversations (each in two míreanna), Cuid C three
radio/television pieces. The 2011 Ordinary scheme prints no listening key at all: PDF 10 prints, for each item, the
tariffs of its questions in print order (“Fógra a hAon 4 + 2 + 6 + 2”, … “Comhrá a Dó 3 + 3 + 3 + 6 + 3 + 6”, …
“Píosa a Trí 2 + 4”), and the one 0–12 language deduction for the whole test. So each printed question is its own
criterion at the price its place in that line gives it (the first addend prices the first printed question of the
item, and so on; every line's count matches its item's printed questions and the lines add to 120); its guidance is
the question as the paper prints it and the item's tariff line; its one row is that question, claimed whole (no
partial is printed), and the criterion is `tariffOnly`: the scheme prints the tariff and no answer. The card says so
in English (UNPRINTED_ANSWER). Nothing is taken from anywhere else as an answer.

No 2011 Ordinary card existed before. `build` cards the test the way the reviewed 2012–2026 Ordinary listening is
carded: one card per printed item (the Bank plays one recording item as one exercise), each printed question its own
criterion. The 2011 Atlas files this paper under the pre-2012 keys “1”, “2”, “3” (one per Cuid); the item keys are
2012's (“L-A-F1” … “L-C-P3”), which do not clash. `main` writes the card file.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import re
from pathlib import Path
from irish_lifted import PUA, scheme_words_in, symbol_text

ROOT = Path(__file__).resolve().parents[3]
YEAR = 2011
FILE = 'LC001GLPA00IV'
SCHEME_FILE = 'LC001GLP000IV'
OUT = ROOT / 'components/MarkBank/cards/irish/ordinary-2011-aural-authored.json'
SOURCE_REVIEW = ROOT / 'scripts/markbank/authored/irish-ordinary-2011-aural-source-review.json'
REVIEWED_AT = '2026-11-05'
PAPER_SHA = '187f6a5098bd6e11d6a991d7c7abd9f5c913b5ee245539596fd5ebd02c12942e'
SCHEME_SHA = '6e73ff5b1d21c777f7d39b3731cb7d7e6b0156fe6043c00f4fea9291032e0ad3'
AUDIO_FILE = 'LC001ZLP017IV.mp3'
AUDIO_URL = f'https://www.examinations.ie/archive/exampapers/{YEAR}/{AUDIO_FILE}'
DIRECTIVE = re.compile(r'rogha|roghna|Freagair|Cuir tic|Ainmnigh|Luaigh|\bnó\b|dhá phointe|dhá rud|dó/di|ceann amháin|amháin|\bdhá\b', re.I)
SOURCE_NOTE = 'Shown page-for-page from the official examination paper; swipe to move between pages.'
UNPRINTED_ANSWER = 'The scheme prints no answer for this part.'  # types/markBank.ts
LANGUAGE_LINE = '[Gaeilge lochtach : 0 – 12 a bhaint den iomlán a gnóthaíodh]'
LANGUAGE = (f'Scheme PDF 10: “{LANGUAGE_LINE}” This 0–12 deduction applies once to the whole listening test (120), never '
            'inside a single question.')
NO_KEY = (f'{UNPRINTED_ANSWER} The {YEAR} scheme prints each item’s question tariffs in print order (PDF 10) and no answer '
          'key: each printed question is claimed whole at its own printed price.')
# The scheme's SymbolMT glyphs (U+F0B4 ×, U+F0B7 •) sit on PDF 3, 5, 6, 8, 9 and 11; none on the listening page.
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


def criterion(id, label, marks, guidance):
    # Claimed whole: the scheme prints the question's price and no partial and no answer (coordinator, batch 7: "Tariff").
    return dict(id=id, label=label, kind='award', maxMarks=marks, permittedMarks=[0, marks], guidanceKind='exact',
                guidance=guidance, tariffOnly=True)


def source(ref, pages):
    return dict(kind='source-text', label=ref, title=f'Gaeilge Gnáthleibhéal {YEAR} · Triail Chluastuisceana · {ref}', pages=pages,
                attribution='© State Examinations Commission.', presentationNote=SOURCE_NOTE)


def selection_decisions(paper):
    decisions = json.loads(SOURCE_REVIEW.read_text())['selectionDecisions']
    expected = {(d['page'], d['raw']) for d in decisions}
    found = {(i, clean(line)) for i, page in enumerate(paper, 1)
             for line in page.get_text().splitlines() if DIRECTIVE.search(clean(line))}
    assert found == expected, ('Unclassified/stale selection directives', found - expected, expected - found)
    return decisions


GRID = 'Líon isteach an t-eolas atá á lorg sa ghreille anseo.'
# (key, card suffix, ref, paper pages, topic, the item's tariff line (scheme PDF 10), [(criterion id, label, paper prompt)])
SEGMENTS = [
    ('L-A-F1', 'a-f1', 'Cuid A · Fógra a hAon', [1], 'irish-1-0', 'Fógra a hAon 4 + 2 + 6 + 2', [
        # A grid: four unnumbered printed questions.
        ('g1', 'Greille 1', 'Cén dream a chuir an fógra seo amach?'),
        ('g2', 'Greille 2', 'Cén Ghaeltacht atá luaite anseo?'),
        ('g3', 'Greille 3', 'Rud amháin is gá a bheith ag duine don phost seo.'),
        ('g4', 'Greille 4', 'Cén baile a bhfuil Coiste Forbartha na Gaeltachta ann?')]),
    ('L-A-F2', 'a-f2', 'Cuid A · Fógra a Dó', [2], 'irish-1-0', 'Fógra a Dó 4 + 2 + 6 + 2', [
        ('q1a', 'Ceist 1(a)', 'Cad a bheidh á sheoladh in oifigí Fhoras na Gaeilge?'),
        ('q1b', 'Ceist 1(b)', 'Cá bhfuil oifigí an Fhorais?'),
        ('q2a', 'Ceist 2(a)', 'Cé mhéad téarma atá aistrithe ó Bhéarla go Gaeilge?'),
        ('q2b', 'Ceist 2(b)', 'Cé a thug moladh mór don rud nua seo?')]),
    ('L-A-F3', 'a-f3', 'Cuid A · Fógra a Trí', [2], 'irish-1-0', 'Fógra a Trí 4 + 4 + 2 + 4', [
        ('g1', 'Greille 1', 'Cén lá a bheidh an lá spóirt ar siúl?'),
        ('g2', 'Greille 2', 'Cén áit a mbeidh sé ar siúl?'),
        ('g3', 'Greille 3', 'Cad é an táille iontrála do dhaoine fásta?'),
        ('g4', 'Greille 4', 'Luaigh imeacht pléisiúir amháin a bheidh ar siúl.')]),
    ('L-B-C1', 'b-c1', 'Cuid B · Comhrá a hAon', [2, 3], 'irish-1-1', 'Comhrá a hAon 4+ 4 + 4 + 4', [
        ('m1-q1', 'An Chéad Mhír · Ceist 1', 'Cé mhéad lá atá an rialtas nua in oifig, dar le hAindriú?'),
        ('m1-q2', 'An Chéad Mhír · Ceist 2', 'Cá bhfuil na daoine óga ag dul, dar le Síle?'),
        ('m2-q1', 'An Dara Mír · Ceist 1', 'Conas atá ag éirí leis an gcuid is mó de na hÉireannaigh óga a fhágann an tír, dar le Síle?'),
        ('m2-q2', 'An Dara Mír · Ceist 2', 'Luaigh buntáiste amháin a bhaineann leis an mbaile, dar le hAindriú.')]),
    ('L-B-C2', 'b-c2', 'Cuid B · Comhrá a Dó', [3], 'irish-1-1', 'Comhrá a Dó 3 + 3 + 3 + 6 + 3 + 6', [
        # The first mír is a grid of four unnumbered printed questions; the second mír two numbered ones.
        ('m1-g1', 'An Chéad Mhír · Greille 1', 'Clár amháin atá luaite anseo.'),
        ('m1-g2', 'An Chéad Mhír · Greille 2', 'Oíche amháin a mbíonn na cláir theilifíse seo ar siúl.'),
        ('m1-g3', 'An Chéad Mhír · Greille 3', 'Cén uirlis cheoil a sheinneann Pádraig?'),
        ('m1-g4', 'An Chéad Mhír · Greille 4', 'Cé hiad na daoine nach maith le Máire iad?'),
        ('m2-q1', 'An Dara Mír · Ceist 1', 'Cén fáth nach maith le Máire na daoine sin ar an teilifís?'),
        ('m2-q2', 'An Dara Mír · Ceist 2', 'Cén fáth a raibh Simon Cowell ar tí tosú ag magadh faoi Susan Boyle, dar le Pádraig?')]),
    ('L-B-C3', 'b-c3', 'Cuid B · Comhrá a Trí', [3, 4], 'irish-1-1', 'Comhrá a Trí 4 + 2 + 4 + 2', [
        ('m1-q1', 'An Chéad Mhír · Ceist 1', 'Cén fáth ar chuir Des Bishop na seónna ar ceal, dar le Ciarán?'),
        ('m1-q2', 'An Chéad Mhír · Ceist 2', 'Cén aois a bhí Des Bishop nuair a tháinig sé go hÉirinn, dar le Ciarán?'),
        ('m2-q1', 'An Dara Mír · Ceist 1', 'Cé mhéad ama a thóg sé ar Des Bishop an Ghaeilge a fhoghlaim, dar le Nóirín?'),
        ('m2-q2', 'An Dara Mír · Ceist 2', 'Tabhair píosa amháin eolais faoin múinteoir nua Gaeilge.')]),
    ('L-C-P1', 'c-p1', 'Cuid C · Píosa a hAon', [4], 'irish-1-2', 'Píosa a hAon 2 + 4 + 4 + 4', [
        ('g1', 'Greille 1', 'An chathair inar léiríodh an dráma.'),
        ('g2', 'Greille 2', 'Rud amháin a scríobh Micheál roimhe seo.'),
        ('g3', 'Greille 3', 'An t-ainm atá ar an sobaldráma.'),
        ('g4', 'Greille 4', 'An dáta a dtosóidh Féile Ealaíon na Gaillimhe.')]),
    ('L-C-P2', 'c-p2', 'Cuid C · Píosa a Dó', [4], 'irish-1-2', 'Píosa a Dó 2 + 4', [
        ('q1', 'Ceist 1', 'Cén post atá ag Peadar Mac Suibhne?'),
        ('q2', 'Ceist 2', 'Cé mhéad bliain atá caite aige ag obair ar an Chlochán Liath?')]),
    ('L-C-P3', 'c-p3', 'Cuid C · Píosa a Trí', [4], 'irish-1-2', 'Píosa a Trí 2 + 4', [
        ('q1', 'Ceist 1', 'Cén contae a mbeidh Ritchie Ó hEadhra ag obair ann?'),
        ('q2', 'Ceist 2', 'Luaigh ceann amháin de na himeachtaí Gaeilge atá sé i gceist ag Ritchie a eagrú.')]),
]
# The questions each card prints, in the 2021–2025 segment-card form (listeningQuestionGroups in SessionScreen.tsx).
SEGMENT_TEXT = {
    'L-A-F1': lambda qs: ' '.join([GRID] + [q[2] for q in qs]),
    'L-A-F2': lambda qs: f'1. (a) {qs[0][2]} (b) {qs[1][2]} 2. (a) {qs[2][2]} (b) {qs[3][2]}',
    'L-A-F3': lambda qs: ' '.join([GRID] + [q[2] for q in qs]),
    'L-B-C1': lambda qs: f'An Chéad Mhír 1. {qs[0][2]} 2. {qs[1][2]} An Dara Mír 1. {qs[2][2]} 2. {qs[3][2]}',
    'L-B-C2': lambda qs: f'An Chéad Mhír {GRID} ' + ' '.join(q[2] for q in qs[:4]) + f' An Dara Mír 1. {qs[4][2]} 2. {qs[5][2]}',
    'L-B-C3': lambda qs: f'An Chéad Mhír 1. {qs[0][2]} 2. {qs[1][2]} An Dara Mír 1. {qs[2][2]} 2. {qs[3][2]}',
    'L-C-P1': lambda qs: ' '.join([GRID] + [q[2] for q in qs]),
    'L-C-P2': lambda qs: f'1. {qs[0][2]} 2. {qs[1][2]}',
    'L-C-P3': lambda qs: f'1. {qs[0][2]} 2. {qs[1][2]}',
}
INTRO = {
    'A': 'Cloisfidh tú trí cinn d’fhógraí raidió sa chuid seo. Cloisfidh tú gach fógra díobh faoi dhó. Beidh sos ann leis na '
         'freagraí a scríobh tar éis na chéad éisteachta agus tar éis an dara héisteacht.',
    'B': 'Cloisfidh tú trí cinn de chomhráite sa chuid seo. Cloisfidh tú gach comhrá díobh trí huaire. Cloisfidh tú an comhrá ó '
         'thosach deireadh an chéad uair. Ansin cloisfidh tú é ina dhá mhír. Beidh sos ann leis na freagraí a scríobh tar éis gach '
         'míre díobh. Ina dhiaidh sin cloisfidh tú an comhrá ó thosach deireadh arís.',
    'C': 'Cloisfidh tú trí cinn de phíosaí raidió/teilifíse sa chuid seo. Cloisfidh tú gach píosa díobh faoi dhó. Beidh sos ann '
         'leis na freagraí a scríobh tar éis na chéad éisteachta agus tar éis an dara héisteacht.',
}
LISTENING_REQUIREMENTS = ['Éist leis an taifeadadh oifigiúil.', 'Freagair gach mír atá priontáilte ar an gcárta.']

_MATERIAL = None


def addends(line):
    return [int(v) for v in re.findall(r'\d+', line)]


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
    assert len(paper) == 4 and len(scheme) == 12
    texts = [clean(p.get_text()) for p in paper]
    stext = [clean(page_text(p)) for p in scheme]
    listening = stext[9]
    assert listening.startswith('8 - CLUASTUISCINT - (120 marc) Cuid A :'), listening[:60]
    assert listening.endswith(LANGUAGE_LINE), listening[-80:]
    assert 'TRIAIL CHLUASTUISCEANA (120 marc)' in texts[0]
    # Each item's tariff line is printed once on PDF 10, in item order; its count is the item's printed questions.
    at = 0
    for key, suffix, ref, pages, topic, tariff, questions in SEGMENTS:
        assert listening.count(tariff) == 1 and listening.index(tariff) > at, (key, tariff)
        at = listening.index(tariff)
        assert len(addends(tariff.split(' a ', 1)[1].split(' ', 1)[1])) == len(questions), key
        page_words = comparable(' '.join(texts[p - 1] for p in pages))
        for cid, label, prompt in questions:
            assert comparable(prompt) in page_words, (key, cid)
    assert sum(sum(addends(t.split(' a ', 1)[1].split(' ', 1)[1])) for *_, t, _ in SEGMENTS) == 120
    assert sum(len(q) for *_, q in SEGMENTS) == 34
    # No answer key anywhere: the scheme prints the tariffs, and no listening question of the paper is reprinted in it.
    for *_, questions in SEGMENTS:
        for cid, label, prompt in questions:
            assert comparable(prompt) not in comparable(' '.join(stext)), ('a listening question reprinted in the scheme', prompt)
    for part, page in [('A', 1), ('B', 2), ('C', 4)]:
        assert comparable(INTRO[part]) in comparable(texts[page - 1]), part
    assert sum(comparable(t).count(comparable(GRID)) for t in texts) == 4  # Fógra a hAon, Fógra a Trí, Comhrá a Dó, Píosa a hAon
    _MATERIAL = dict(paper=paper, texts=texts, decisions=selection_decisions(paper))
    return _MATERIAL


def build():
    m = material()
    cards = []
    audio = dict(kind='source-audio', title=f'Triail Chluastuisceana {YEAR}', playbackUrl=AUDIO_URL, secFileid=AUDIO_FILE,
                 canonicalUrl=AUDIO_URL, attribution='© State Examinations Commission.',
                 presentationNote='Play the official recording and use the section heading on this card to follow the correct part.')
    for key, suffix, ref, pages, topic, tariff, questions in SEGMENTS:
        prices = addends(tariff.split(' a ', 1)[1].split(' ', 1)[1])
        # Each criterion carries its own printed question first, then its item's printed tariff line, whose addend in the
        # question's print place is its price.
        criteria = [criterion(cid, label, price, [prompt, tariff]) for (cid, label, prompt), price in zip(questions, prices)]
        cards.append(dict(
            id=f'irish-{YEAR}-ol-listening-{suffix}', year=YEAR, level='ordinary', paper=1, section='1',
            questionRef=f'{YEAR} OL Cluastuiscint {ref}', questionText=SEGMENT_TEXT[key](questions),
            totalMarks=sum(c['maxMarks'] for c in criteria), topicId=topic, conceptId=f'irish-listening-{suffix}',
            paperPage=pages[0], schemePage=10, taskRequirements=LISTENING_REQUIREMENTS, criteria=criteria,
            markingGuideNote=f'Each printed question is marked at its own published tariff ({tariff.split(" ", 3)[-1]}, in print order), '
                             f'from the {YEAR} SEC marking scheme. ' + NO_KEY + ' ' + LANGUAGE,
            audioMaterial=dict(audio, label=ref), paperFileid=FILE, atlasQuestionId=key, reviewedAt=REVIEWED_AT,
            reviewedPaperPages=pages, schemeFileid=SCHEME_FILE, schemePages=[10], sourceMaterial=source(f'Cluastuiscint {ref}', pages)))
    assert len(cards) == 9 and len({x['id'] for x in cards}) == 9 and len({x['atlasQuestionId'] for x in cards}) == 9
    assert sum(x['totalMarks'] for x in cards) == 120
    for card in cards:
        assert sum(cr['maxMarks'] for cr in card['criteria']) == card['totalMarks'], card['id']
        for cr in card['criteria']:
            assert cr['guidance'] and all(not PUA.search(g) for g in cr['guidance']), (card['id'], cr['id'])
    sr = json.loads(SOURCE_REVIEW.read_text())
    review = dict(year=YEAR, level='ordinary', paperFileid=FILE + '.pdf', schemeFileid=SCHEME_FILE + '.pdf',
                  paperSha256=PAPER_SHA, schemeSha256=SCHEME_SHA,
                  reviewedPaperPages=list(range(1, 5)), reviewedSchemePages=sr['reviewedSchemePages'], schemeScope=sr['schemeScope'],
                  reviewDate=REVIEWED_AT, status='reviewed', fullPaperAndApplicableSchemeVisualSweep=True, selectionDecisions=m['decisions'],
                  cardIds=[x['id'] for x in cards], listeningSegmentCardIds=[x['id'] for x in cards],
                  printedListeningQuestions=34, examStructure=dict(listening=120, total=120),
                  nonPoolDecisions=sr['nonPoolDecisions'], openIssues=[], audio=sr['audio'], caveats=sr['sourceFindings'],
                  boundaries='9 listening item cards (three announcements, three conversations, three pieces) carrying all 34 printed '
                             'questions as separate criteria at their printed prices (120; the scheme prints no answer key).')
    return dict(review=review, cards=cards)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    data = build()
    scheme_words_in(data)  # guidance, question and task checks carry the SEC's words only (irish_lifted.py)
    content = json.dumps(data, ensure_ascii=False, indent=2) + '\n'
    if args.check:
        assert OUT.exists() and OUT.read_text() == content, f'Stale output: {OUT}'
    else:
        OUT.write_text(content)
    print(f"Irish Ordinary {YEAR} Triail Chluastuisceana: {len(data['cards'])} reviewed cards (34 printed questions); the archive remains incomplete.")


if __name__ == '__main__':
    main()
