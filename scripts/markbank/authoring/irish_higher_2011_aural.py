#!/usr/bin/env python3
"""Reviewed 2011 Higher aural paper (Triail Chluastuisceana): new cards, no legacy component.

Before 2012 the Higher listening test is its own component, LC001ALPA00IV (100 marc, Dé Luain 13 Meitheamh 4.30–5.10),
not part of Páipéar 1. Paper PDF 1–8 (1 the cover with the examiner's box, 2 the Treoracha, 3–4 Cuid A's three
announcements, 5–7 Cuid B's three conversations, each in two míreanna, 8 Cuid C's three news pieces) and the combined
LC001ALP000IV scheme's aural pages (PDF 20 the tariffs, 21–24 the recording's script "Téipscript 2011"), reviewed on
2026-11-05. Counts are assertions, not corpus-completeness proof.

The 2011 scheme prints NO answer key for the listening test: PDF 20 prints each section's tariff ("Fógra 1: 2 marc × 5
= 10 marc" … "Píosa 3: 2 marc × 3 = 6 mharc"), Tuiscint 90 and Cumas Gaeilge 10; PDF 21–24 print the script only, and
PDF 25–28 are blank. So, as 2012 Ordinary did, every printed question is its own criterion at its section's tariff
(2 marks), its guidance the paper's printed question and that tariff line, its one row the question itself, claimed
whole ([0, 2]); the card's note carries the fixed UNPRINTED_ANSWER sentence, and nothing is taken from the script as an
answer. The Cumas Gaeilge 10 is one award for the whole test; it is described on every card and never split.

Glyph audit (read from the font of every span): the scheme's PDF 20 draws the multiplication sign of every tariff line
with SymbolMT U+F0B4 (9 spans), read as "×" (irish_lifted.symbol_text); the aural paper prints no symbol-font span.

The card unit follows the reviewed 2012–2026 listening components: one card per printed segment (Fógra; Comhrá mír;
Píosa), 12 cards carrying all 45 printed questions. `main` writes
components/MarkBank/cards/irish/higher-2011-aural-authored.json with its review record.
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
FILE = 'LC001ALPA00IV'
SCHEME_FILE = 'LC001ALP000IV'
OUT = ROOT / 'components/MarkBank/cards/irish/higher-2011-aural-authored.json'
SOURCE_REVIEW = ROOT / 'scripts/markbank/authored/irish-higher-2011-aural-source-review.json'
REVIEWED_AT = '2026-11-05'
PAPER_SHA = '1203d9475cc398703f2436270d1e63e9c9f3cb589d4b9102eb48e166c5c42844'
SCHEME_SHA = 'b5f7c77e673759308a08e4a8cdef08000045789921a3c64278c739bb510783b0'
DIRECTIVE = re.compile(r'rogha|roghna|Freagair|Ainmnigh|Luaigh|\bnó\b|dhá phointe|dhá rud|dhá ch|dhá bh|dhá ph|an dá|'
                       r'amháin|\bdhá\b|Tabhair', re.I)
AUDIO_URL = 'https://www.examinations.ie/archive/exampapers/2011/LC001ZLP017IV.mp3'
SOURCE_NOTE = 'Shown page-for-page from the official examination paper; swipe to move between pages.'
SCHEME_GLYPHS = {(5, 'Wingdings-Regular', ''): 1, (5, 'SymbolMT', ''): 5, (6, 'SymbolMT', ''): 3,
                 (10, 'SymbolMT', ''): 2, (14, 'SymbolMT', ''): 1, (20, 'SymbolMT', ''): 9,
                 (24, 'SymbolMT', ''): 3}
UNPRINTED = 'The scheme prints no answer for this part.'
NO_KEY = ('The 2011 scheme prints each listening section’s tariff (PDF 20) and the recording’s script (PDF 21–24), but no answer '
          'key: each printed question is claimed whole at its 2 marks, and nothing is taken from the script as an answer.')
LANGUAGE = ('Scheme PDF 20: Tuiscint 90 + Cumas Gaeilge 10 = 100. The 10 marks for Irish are one award for the whole test, '
            'never inside a single card.')


def clean(text):
    return re.sub(r'\s+', ' ', symbol_text(text)).strip()


def comparable(text):
    return re.sub(r'[^\w]+', '', text.lower())


# Glyphs the text layer mis-decodes, keyed by (font, character) and read from the rendered page.
GLYPHS = {('SymbolMT', '\uf0b4'): '×'}


def page_text(page):
    """A scheme page's text with the audited glyph repairs applied, span by span."""
    return '\n'.join(''.join(GLYPHS.get((span['font'], char['c']), char['c']) for span in line['spans'] for char in span['chars'])
                     for block in page.get_text('rawdict')['blocks'] for line in block.get('lines', []))


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


def selection_decisions(paper):
    decisions = json.loads(SOURCE_REVIEW.read_text())['selectionDecisions']
    expected = {(d['page'], d['raw']) for d in decisions}
    found = {(i, clean(line)) for i, page in enumerate(paper, 1)
             for line in page.get_text().splitlines() if DIRECTIVE.search(clean(line))}
    assert found == expected, ('Unclassified/stale selection directives', found - expected, expected - found)
    return decisions


# (key, id suffix, ref, paper page, topic, scheme tariff line, [(n, printed question)])
SEGMENTS = [
    ('L-A-F1', 'a-f1', 'Cuid A · Fógra a hAon', 3, 'irish-1-0', 'Fógra 1: 2 marc × 5 = 10 marc', [
        ('1a', '1. (a) Cén eagraíocht atá ag fógairt an phoist seo?'),
        ('1b', '(b) Ainmnigh dhá áit i nGaeltacht Chiarraí atá luaite.'),
        ('2', '2. Luaigh cúram amháin a bheidh ar an duine a cheapfar.'),
        ('3a', '3. (a) Luaigh cáilíocht amháin is gá a bheith ag an duine seo.'),
        ('3b', '(b) Cén dá rud is ceart a chur chuig an Rúnaí?')]),
    ('L-A-F2', 'a-f2', 'Cuid A · Fógra a Dó', 3, 'irish-1-0', 'Fógra 2: 2 marc × 5 = 10 marc', [
        ('1', '1. Cad atá á sheoladh agus cathain a sheolfar é?'),
        ('2a', '2. (a) Cén saghas comhlachta é Seol – Maith thú?'),
        ('2b', '(b) Cé mhéad téarma a bhfuil aistriú le fáil orthu?'),
        ('3a', '3. (a) Cén saghas ruda é focalgaeilge.ie?'),
        ('3b', '(b) Cé a thug moladh mór don obair seo?')]),
    ('L-A-F3', 'a-f3', 'Cuid A · Fógra a Trí', 4, 'irish-1-0', 'Fógra 3: 2 marc × 5 = 10 marc', [
        ('1', '1. Cé uaidh ar tháinig an fógra seo?'),
        ('2a', '2. (a) Cá mbeidh an lá spóirt ar siúl?'),
        ('2b', '(b) Luaigh comórtas amháin a bheidh ar siúl.'),
        ('3a', '3. (a) Cé a chuirfidh na duaiseanna ar fáil?'),
        ('3b', '(b) Luaigh imeacht pléisiúir amháin a bheidh ar siúl.')]),
    ('L-B-C1-M1', 'b-c1-first', 'Cuid B · Comhrá a hAon · An Chéad Mhír', 5, 'irish-1-1', 'Comhrá 1: 2 marc × 6 = 12 mharc', [
        ('1', '1. Cén rud a bhfuil deireadh leis, dar le hAindriú?'),
        ('2', '2. Luaigh rud amháin as a dtiocfaidh jabanna, dar le hAindriú.'),
        ('3', '3. Tabhair píosa amháin eolais a luann Síle faoi na daoine óga.')]),
    ('L-B-C1-M2', 'b-c1-second', 'Cuid B · Comhrá a hAon · An Dara Mír', 5, 'irish-1-1', 'Comhrá 1: 2 marc × 6 = 12 mharc', [
        ('1', '1. Cén seanfhocal a luann Aindriú?'),
        ('2a', '2. (a) Luaigh dhá bhuntáiste a bhaineann leis an Astráil, dar le Síle.'),
        ('2b', '(b) Luaigh dhá bhuntáiste a bhaineann leis an mbaile, dar le hAindriú.')]),
    ('L-B-C2-M1', 'b-c2-first', 'Cuid B · Comhrá a Dó · An Chéad Mhír', 6, 'irish-1-1', 'Comhrá 2: 2 marc × 8 = 16 mharc', [
        ('1', '1. Cé hiad na daoine i dteaghlach Mháire atá tugtha do na cláir seo?'),
        ('2', '2. Cathain ba mhaith le Pádraig páirt a ghlacadh sna cláir seo?'),
        ('3a', '3. (a) Cén deis a thugann na cláir seo do dhaoine, dar le Máire?'),
        ('3b', '(b) Cén dream daoine a chuireann as do Mháire?')]),
    ('L-B-C2-M2', 'b-c2-second', 'Cuid B · Comhrá a Dó · An Dara Mír', 6, 'irish-1-1', 'Comhrá 2: 2 marc × 8 = 16 mharc', [
        ('1', '1. Cén rud is ceart a rá glan amach le hiomaitheoirí, dar le Pádraig?'),
        ('2a', '2. (a) Cad a bhíonn ar siúl ag cuid de na moltóirí uaireanta, dar le Máire?'),
        ('2b', '(b) Cén fáth a raibh Simon Cowell ar tí tosú ag magadh faoi Susan Boyle, dar le Pádraig?'),
        ('3', '3. Cad a chuir deireadh leis an magadh, dar le Máire?')]),
    ('L-B-C3-M1', 'b-c3-first', 'Cuid B · Comhrá a Trí · An Chéad Mhír', 7, 'irish-1-1', 'Comhrá 3: 2 marc × 6 = 12 mharc', [
        ('1a', '1. (a) Cá bhfuair athair Des Bishop bás agus cén galar a bhí air, dar le Ciarán?'),
        ('1b', '(b) Cén fáth ar bronntanas ó Neamh é Des Bishop do na heagraíochtaí Gaeilge, dar le Nóirín?'),
        ('2', '2. Cé mhéad ama a thóg sé ar Des Bishop máistreacht a fháil ar an nGaeilge, dar le Nóirín?')]),
    ('L-B-C3-M2', 'b-c3-second', 'Cuid B · Comhrá a Trí · An Dara Mír', 7, 'irish-1-1', 'Comhrá 3: 2 marc × 6 = 12 mharc', [
        ('1', '1. Cén difear atá idir Des Bishop agus an bheirt chainteoirí maidir le foghlaim na Gaeilge de, dar le Nóirín?'),
        ('2', '2. Tabhair píosa amháin eolais faoi choláiste Gaeilge a thaitneodh le Nóirín.'),
        ('3', '3. Tabhair dhá phíosa eolais faoin múinteoir nua Gaeilge, dar le Ciarán.')]),
    ('L-C-P1', 'c-p1', 'Cuid C · Píosa a hAon', 8, 'irish-1-2', 'Píosa 1: 2 marc × 3 = 6 mharc', [
        ('1', '1. Cár léiríodh an dráma nua le Micheál Ó Conghaile?'),
        ('2a', '2. (a) Luaigh dhá chineál leabhar atá scríofa ag Micheál.'),
        ('2b', '(b) Cár cuireadh aithne ar na haisteoirí a ghlac páirt sa dráma?')]),
    ('L-C-P2', 'c-p2', 'Cuid C · Píosa a Dó', 8, 'irish-1-2', 'Píosa 2: 2 marc × 4 = 8 marc', [
        ('1', '1. Cé dó ar tugadh onóir an tseachtain seo caite?'),
        ('2', '2. Conas a tharla gur tháinig sé go dtí an Clochán Liath a chéaduair?'),
        ('3a', '3. (a) Cá háit a mbíodh a chlinicí aige sa Chlochán Liath?'),
        ('3b', '(b) Cá bhfuil a sheomraí aige le fada anois?')]),
    ('L-C-P3', 'c-p3', 'Cuid C · Píosa a Trí', 8, 'irish-1-2', 'Píosa 3: 2 marc × 3 = 6 mharc', [
        ('1', '1. Cén post atá faighte ag Ritchie Ó hEadhra i Loch Garman?'),
        ('2', '2. Cén aithne a bheadh ag daoine ar Ritchie roimhe seo?'),
        ('3', '3. Cad a eagróidh Ritchie i Loch Garman gach samhradh as seo amach?')]),
]
# The section heads printed on the paper above each segment's first question.
HEADS = {3: ['Cloisfidh tú trí cinn d’fhógraí raidió sa chuid seo.', 'FÓGRA A hAON', 'FÓGRA A DÓ'], 4: ['FÓGRA A TRÍ'],
         5: ['Cloisfidh tú trí cinn de chomhráite sa chuid seo.', 'COMHRÁ A hAON', 'An Chéad Mhír', 'An Dara Mír'],
         6: ['COMHRÁ A DÓ'], 7: ['COMHRÁ A TRÍ'], 8: ['Cloisfidh tú trí cinn de phíosaí nuachta raidió/teilifíse sa chuid seo.',
                                                       'PÍOSA A hAON', 'PÍOSA A DÓ', 'PÍOSA A TRÍ']}


def material():
    import fitz
    paper_path = ROOT / f'paper-trail-corpus/exampapers/2011/{FILE}.pdf'
    scheme_path = ROOT / f'paper-trail-corpus/markingschemes/2011/{SCHEME_FILE}.pdf'
    assert hashlib.sha256(paper_path.read_bytes()).hexdigest() == PAPER_SHA, 'Aural paper changed: repeat visual review'
    assert hashlib.sha256(scheme_path.read_bytes()).hexdigest() == SCHEME_SHA, 'Scheme changed: repeat visual review'
    paper, scheme = fitz.open(paper_path), fitz.open(scheme_path)
    assert symbol_audit(paper) == {} and symbol_audit(scheme) == SCHEME_GLYPHS, 'Symbol glyphs changed: repeat the glyph review'
    texts = [clean(p.get_text()) for p in paper]
    stext = [clean(page_text(p)) for p in scheme]
    tariffs = stext[19]
    # PDF 20: the aural's marks, its sections' tariffs and nothing else; PDF 21–24 the script; PDF 25–28 blank.
    assert tariffs.startswith('18 CLUASTUISCINT (100 marc) { (i) Tuiscint = 90 marc }'), tariffs[:80]
    assert '(ii) Cumas Gaeilge = 10 marc' in tariffs and '(iii) Iomlán = 100 marc' in tariffs
    assert stext[20].startswith('19 Téipscript 2011 Fógra a hAon') and all(not t for t in stext[24:28])
    assert not any(re.search(r'=\s*\d+\s*m?h?arc\b|\(\d\)', t) for t in stext[20:24]), 'the script prints a price'
    for _, _, _, page, _, line, questions in SEGMENTS:
        compact = re.sub(r'\s+', ' ', tariffs)
        assert line in compact, line
        for n, question in questions:
            assert comparable(question) in comparable(texts[page - 1]), (page, n)
            # The question is printed once, on the paper only: the scheme never reprints it.
            assert comparable(question.split(' ', 1)[1] if question[0].isdigit() else question) not in comparable(' '.join(stext)), (page, n)
        for head in HEADS.get(page, []):
            assert comparable(head) in comparable(texts[page - 1]), (page, head)
    assert sum(len(q) for *_, q in SEGMENTS) == 45
    assert 'Caithfidh do chuid freagraí uile sa triail seo a bheith i nGaeilge, ach amháin nuair nach gá sin.' in texts[1]
    return dict(texts=texts, tariffs=tariffs, decisions=selection_decisions(paper))


def build():
    m = material()
    cards = []
    audio = dict(kind='source-audio', title='Triail Chluastuisceana 2011', playbackUrl=AUDIO_URL, secFileid='LC001ZLP017IV.mp3',
                 canonicalUrl=AUDIO_URL, attribution='© State Examinations Commission.',
                 presentationNote='Play the official recording and use the section heading on this card to follow the correct part.')
    for key, suffix, ref, page, topic, line, questions in SEGMENTS:
        criteria = [dict(id=f'q{n}', label=f'Ceist {n[0]}' + (f'({n[1]})' if len(n) > 1 else ''), kind='award', maxMarks=2,
                         permittedMarks=[0, 2], guidanceKind='exact', tariffOnly=True, guidance=[question, line])
                    for n, question in questions]
        cards.append(dict(
            id=f'irish-2011-hl-listening-{suffix}', year=2011, level='higher', paper=1, section='A',
            questionRef=f'2011 HL Cluastuiscint {ref}', questionText=' '.join(q for _, q in questions),
            totalMarks=2 * len(questions), topicId=topic, conceptId=f'irish-listening-{suffix}', paperFileid=FILE,
            schemeFileid=SCHEME_FILE, paperPage=page, schemePage=20, schemePages=[20], atlasQuestionId=key,
            reviewedAt=REVIEWED_AT, reviewedPaperPages=[page],
            taskRequirements=['Éist leis an taifeadadh oifigiúil.', 'Freagair gach mír atá priontáilte ar an gcárta.'],
            criteria=criteria,
            markingGuideNote=f'Each printed question is marked at its section’s published tariff (2 marks), from the 2011 SEC marking scheme. '
                             f'{UNPRINTED} {NO_KEY} {LANGUAGE}',
            audioMaterial=dict(audio, label=ref),
            sourceMaterial=dict(kind='source-text', label=f'Cluastuiscint {ref}', title=f'Gaeilge Ardleibhéal 2011 · Triail Chluastuisceana · {ref}',
                                pages=[page], attribution='© State Examinations Commission.', presentationNote=SOURCE_NOTE)))
    assert len(cards) == 12 and sum(len(c['criteria']) for c in cards) == 45 and sum(c['totalMarks'] for c in cards) == 90
    assert len({c['id'] for c in cards}) == len(cards) and len({c['atlasQuestionId'] for c in cards}) == len(cards)
    for card in cards:
        assert sum(cr['maxMarks'] for cr in card['criteria']) == card['totalMarks'], card['id']
        for cr in card['criteria']:
            assert all(not re.search('[-]', g) for g in cr['guidance']), (card['id'], cr['id'])
    sr = json.loads(SOURCE_REVIEW.read_text())
    review = dict(year=2011, level='higher', paperFileid=FILE + '.pdf', schemeFileid=SCHEME_FILE + '.pdf',
                  paperSha256=PAPER_SHA, schemeSha256=SCHEME_SHA, reviewedPaperPages=list(range(1, 9)),
                  reviewedSchemePages=sr['reviewedSchemePages'], schemeScope=sr['schemeScope'], reviewDate=REVIEWED_AT,
                  status='reviewed', fullPaperAndApplicableSchemeVisualSweep=True, selectionDecisions=m['decisions'],
                  cardIds=[c['id'] for c in cards], listeningSegmentCardIds=[c['id'] for c in cards], readingWholeCardIds=[],
                  printedListeningQuestions=45, examStructure=dict(listening=90, language=10, total=100),
                  nonPoolDecisions=sr['nonPoolDecisions'], openIssues=[], audio=sr['audio'], caveats=sr['sourceFindings'],
                  boundaries='12 listening segment cards (three announcements, three conversations in two míreanna each, three news '
                             'pieces) carrying all 45 printed questions as separate 2-mark criteria (90); Cumas Gaeilge 10 for the whole test.')
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
    print(f"Irish Higher 2011 aural: {len(data['cards'])} reviewed cards (45 printed listening questions); the archive remains incomplete.")


if __name__ == '__main__':
    main()
