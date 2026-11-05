#!/usr/bin/env python3
"""Reviewed 2010 Higher aural paper (Triail Chluastuisceana): new cards, no legacy component.

Before 2012 the Higher listening test is its own component, LC001ALPA00IV (100 marc, Dé Luain 14 Meitheamh 4.30–5.10),
not part of Páipéar 1. Paper PDF 1–8 (1 the cover with the examiner's box, 2 the Treoracha, 3–4 Cuid A's three
announcements, 5–7 Cuid B's three conversations, each in two míreanna, 8 Cuid C's three news pieces) and the combined
LC001ALP000EV scheme's aural pages (PDF 19 the tariffs, 20–25 the answer key, 26–30 the recording's script "Téipscript
2010"), reviewed on 2026-11-05. The scheme's file is named EV but is printed in Irish. Counts are assertions, not
corpus-completeness proof.

Unlike 2011, the 2010 scheme prints an answer key for the listening test (PDF 20–25): each question restated, then its
accepted and refused answers as bullets priced with the unit "m" ("• Cumann Ailse na hÉireann = 2m", "• Ailse = 1m.",
"• Cártaí leis féin = 0m"), some with a note in brackets ("(ná glac le orr/oir.)", "(cruinneas riachtanach)"). PDF 19 prints
the tariffs: every question 2 marks ("Fógra 1: 2 marc × 5 = 10 marc" … "Píosa 3: 2 marc × 3 = 6 mharc"), Tuiscint 90 and
Cumas Gaeilge 10. Each printed question is its own criterion at 2, its guidance the key's restated question and its
answers, word for word (answers.ts reads the "= 2m" prices as the 2012 Higher key's unit-less prices). The Cumas Gaeilge 10
is one award for the whole test; it is described on every card and never split.

Glyph audit (read from the font of every span): the scheme's PDF 19 draws the multiplication sign of every tariff line with
SymbolMT U+F0B4 (9 spans), read as "×"; the key's bullets on PDF 20–25 are SymbolMT U+F0B7, read as "•"; the aural paper
prints no symbol-font span.

The card unit follows the reviewed 2011–2026 listening components: one card per printed segment (Fógra; Comhrá mír;
Píosa), 12 cards carrying all 45 printed questions. `main` writes components/MarkBank/cards/irish/higher-2010-aural-authored.json
with its review record.
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
SCHEME_FILE = 'LC001ALP000EV'
OUT = ROOT / 'components/MarkBank/cards/irish/higher-2010-aural-authored.json'
SOURCE_REVIEW = ROOT / 'scripts/markbank/authored/irish-higher-2010-aural-source-review.json'
REVIEWED_AT = '2026-11-05'
PAPER_SHA = '2213e17cb61f09072b3aece14a98a6dd1de7781c9eb46814915f277cfd141f6f'
SCHEME_SHA = 'e304dd29af73f46d972385ce1f625bce88a47a20010e63e2853c92ad3fbe0be5'
DIRECTIVE = re.compile(r'rogha|roghna|Freagair|Ainmnigh|Luaigh|\bnó\b|dhá phointe|dhá rud|dhá ch|dhá bh|dhá ph|an dá|'
                       r'amháin|\bdhá\b|Tabhair', re.I)
AUDIO_URL = 'https://www.examinations.ie/archive/exampapers/2010/LC001ZLP017IV.mp3'
SOURCE_NOTE = 'Shown page-for-page from the official examination paper; swipe to move between pages.'
SCHEME_GLYPHS = {(5, 'Wingdings-Regular', ''): 1, (5, 'SymbolMT', ''): 5, (6, 'SymbolMT', ''): 3,
                 (11, 'SymbolMT', ''): 2, (12, 'SymbolMT', ''): 4, (19, 'SymbolMT', ''): 9,
                 (20, 'SymbolMT', ''): 25, (21, 'SymbolMT', ''): 24, (22, 'SymbolMT', ''): 25,
                 (23, 'SymbolMT', ''): 25, (24, 'SymbolMT', ''): 21, (25, 'SymbolMT', ''): 11}
KEY_NOTE = ('The listed responses and their marks come from the 2010 SEC marking scheme (PDF 20–25); equivalent wording with the '
            'same meaning is accepted. Each printed question is marked at its section’s published tariff, 2 marks (PDF 19: '
            '“Fógra 1: 2 marc × 5 = 10 marc” …); the key prints its prices with the unit “m” (“= 2m”, “= 1m”, “= 0m”).')
LANGUAGE = ('Scheme PDF 19: Tuiscint 90 + Cumas Gaeilge 10 = 100. The 10 marks for Irish are one award for the whole test, '
            'never inside a single card.')


def clean(text):
    return re.sub(r'\s+', ' ', symbol_text(text)).strip()


def comparable(text):
    return re.sub(r'[^\w]+', '', text.lower())


# Glyphs the text layer mis-decodes, keyed by (font, character) and read from the rendered page.
GLYPHS = {('SymbolMT', ''): '×', ('SymbolMT', ''): '•', ('Wingdings-Regular', ''): '→'}


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


def printed_marks(chunk, marks):
    """The marks a question can earn: 0, its tariff and the single prices its answers print ("= 2m", "= 1m", "= 0m"), as 2012."""
    return sorted({0, marks} | {int(v) for v in re.findall(r'=\s*(\d)\s*m\b', chunk) if int(v) <= marks})


def selection_decisions(paper):
    decisions = json.loads(SOURCE_REVIEW.read_text())['selectionDecisions']
    expected = {(d['page'], d['raw']) for d in decisions}
    found = {(i, clean(line)) for i, page in enumerate(paper, 1)
             for line in page.get_text().splitlines() if DIRECTIVE.search(clean(line))}
    assert found == expected, ('Unclassified/stale selection directives', found - expected, expected - found)
    return decisions


# (key, id suffix, ref, paper page, topic, scheme tariff line, [(n, printed question, the key's restatement)])
SEGMENTS = [
    ('L-A-F1', 'a-f1', 'Cuid A · Fógra a hAon', 3, 'irish-1-0', 'Fógra 1: 2 marc × 5 = 10 marc', [
        ('1a', '1. (a) Cén cumann atá ag eagrú na siúlóide seo?', '(a) Cén cumann atá ag eagrú na siúlóide seo?'),
        ('1b', '(b) Tabhair píosa amháin eolais a luaitear faoi Mhicheál Ó Muircheartaigh.',
         '(b) Tabhair píosa amháin eolais a luaitear faoi Mhicheál Ó Muircheartaigh.'),
        ('2', '2. Cá háit go díreach a mbeidh an tsiúlóid ar siúl?', 'Cá háit go díreach a mbeidh an tsiúlóid ar siúl?'),
        ('3a', '3. (a) Cén rud nach mór do dhuine a dhéanamh roimh ré le bheith páirteach sa tsiúlóid?',
         '(a) Cén rud nach mór do dhuine a dhéanamh roimh ré le bheith páirteach sa tsiúlóid?'),
        ('3b', '(b) Cad a dhéanfar anocht?', '(b) Cad a dhéanfar anocht?')]),
    ('L-A-F2', 'a-f2', 'Cuid A · Fógra a Dó', 3, 'irish-1-0', 'Fógra 2: 2 marc × 5 = 10 marc', [
        ('1', '1. Cad a bheidh ar siúl i dTigh Clarke ar an 6ú Lúnasa?', 'Cad a bheidh ar siúl i dTigh Clarke ar an 6ú Lúnasa?'),
        ('2a', '2. (a) Céard a bheidh ar siúl ag Micheál Ó Cuaig ar an ócáid?', '(a) Céard a bheidh ar siúl ag Micheál Ó Cuaig ar an ócáid?'),
        ('2b', '(b) Cén aithne a cuireadh ar Chaitlín Maude i dtosach?', '(b) Cén aithne a cuireadh ar Chaitlín Maude i dtosach?'),
        ('3a', '3. (a) Cé a eiseoidh an dlúthdhiosca de chuid amhrán Chaitlín Maude ar an ócáid?',
         '(a) Cé a eiseoidh an dlúthdhiosca de chuid amhrán Chaitlín Maude ar an ócáid?'),
        ('3b', '(b) Luaigh rud amháin eile a bheidh ann mar chuid den ócáid chuimhneacháin.',
         '(b) Luaigh rud amháin eile a bheidh ann mar chuid den ócáid chuimhneacháin.')]),
    ('L-A-F3', 'a-f3', 'Cuid A · Fógra a Trí', 4, 'irish-1-0', 'Fógra 3: 2 marc × 5 = 10 marc', [
        ('1', '1. Cad atá ag bagairt ar an Aetóip arís?', 'Cad atá ag bagairt ar an Aetóip arís?'),
        ('2a', '2. (a) Cad a tharla le trí bliana anuas i ndeisceart na tíre ?', '(a) Cad a tharla le trí bliana anuas i ndeisceart na tíre?'),
        ('2b', '(b) Céard a mheastar is cúis leis an tubaiste seo san Aetóip?', '(b) Céard a mheastar is cúis leis an tubaiste seo san Aetóip?'),
        ('3a', '3. (a) Luaigh dhá rud is gá a chur ar fáil láithreach, dar le Goal.', '(a) Luaigh dhá rud is gá a chur ar fáil láithreach, dar le Goal.'),
        ('3b', '(b) Luaigh slí amháin le airgead a thabhairt.', '(b) Luaigh slí amháin le hairgead a thabhairt.')]),
    ('L-B-C1-M1', 'b-c1-first', 'Cuid B · Comhrá a hAon · An Chéad Mhír', 5, 'irish-1-1', 'Comhrá 1: 2 marc × 6 = 12 mharc', [
        ('1', '1. Cá raibh Síle ag an deireadh seachtaine?', 'Cá raibh Síle ag an deireadh seachtaine?'),
        ('2', '2. Cén fáth nach bhfuair Seán ticéad, dar le Síle?', 'Cén fáth nach bhfuair Seán ticéad, dar le Síle?'),
        ('3', '3. Cé mhéad a d’íoc Síle as an ticéad?', 'Cé mhéad a d’íoc Síle as an ticéad?')]),
    ('L-B-C1-M2', 'b-c1-second', 'Cuid B · Comhrá a hAon · An Dara Mír', 5, 'irish-1-1', 'Comhrá 1: 2 marc × 6 = 12 mharc', [
        ('1', '1. Cá bhfuair deartháir Shíle an ticéad?', 'Cá bhfuair deartháir Shíle an ticéad?'),
        ('2a', '2. (a) Cén imní a bhí ar Shíle faoin bpuball?', '(a) Cén imní a bhí ar Shíle faoin bpuball?'),
        ('2b', '(b) Luaigh áis amháin a bhí ar fáil i mBaile Phoinse.', '(b) Luaigh áis amháin a bhí ar fáil i mBaile Phoinse.')]),
    ('L-B-C2-M1', 'b-c2-first', 'Cuid B · Comhrá a Dó · An Chéad Mhír', 6, 'irish-1-1', 'Comhrá 2: 2 marc × 8 = 16 mharc', [
        ('1', '1. Cad a bheidh ag tosú sa scoil an bhliain seo chugainn?', 'Cad a bheidh ag tosú sa scoil an bhliain seo chugainn?'),
        ('2', '2. Cá fhad a mbeidh Sinéad sa Fhrainc?', 'Cá fhad a mbeidh Sinéad sa Fhrainc?'),
        ('3a', '3. (a) Luaigh rud amháin faoi na hábhair sa choláiste in Nice.', '(a) Luaigh rud amháin faoi na hábhair sa choláiste in Nice.'),
        ('3b', '(b) Cén duine gaolmhar le Sinéad a chuaigh chuig an gcoláiste sin cheana?',
         '(b) Cén duine gaolmhar le Sinéad a chuaigh chuig an gcoláiste sin cheana?')]),
    ('L-B-C2-M2', 'b-c2-second', 'Cuid B · Comhrá a Dó · An Dara Mír', 6, 'irish-1-1', 'Comhrá 2: 2 marc × 8 = 16 mharc', [
        ('1', '1. Cén fáth a ndéanfadh bliain sa Fhrainc maitheas do Phól?', 'Cén fáth a ndéanfadh bliain sa Fhrainc maitheas do Phól?'),
        ('2a', '2. (a) Cad a cheapann tuismitheoirí Shinéad faoin Idirbhliain?', '(a) Cad a cheapann tuismitheoirí Shinéad faoin Idirbhliain?'),
        ('2b', '(b) Cén rud speisialta a dhéanfaidh Pól le linn na hIdirbhliana?', '(b) Cén rud speisialta a dhéanfaidh Pól le linn na hIdirbhliana?'),
        ('3', '3. Cén chéim a dhéanfaidh Sinéad in ollscoil Luimnigh?', 'Cén chéim a dhéanfaidh Sinéad in ollscoil Luimnigh?')]),
    ('L-B-C3-M1', 'b-c3-first', 'Cuid B · Comhrá a Trí · An Chéad Mhír', 7, 'irish-1-1', 'Comhrá 3: 2 marc × 6 = 12 mharc', [
        ('1a', '1. (a) Cé mhéad iris Ghaeilge atá ann do dhéagóirí, dar le Máire?', '(a) Cé mhéad iris Ghaeilge atá ann do dhéagóirí, dar le Máire?'),
        ('1b', '(b) Cén saghas irise a mholann Máire?', '(b) Cén saghas irise a mholann Máire?'),
        ('2', '2. Cén fáth nach mbeadh suim ag foilsitheoir in iris Ghaeilge-Bhéarla a chur i gcló?',
         'Cén fáth nach mbeadh suim ag foilsitheoir in iris Ghaeilge-Bhéarla a chur i gcló?')]),
    ('L-B-C3-M2', 'b-c3-second', 'Cuid B · Comhrá a Trí · An Dara Mír', 7, 'irish-1-1', 'Comhrá 3: 2 marc × 6 = 12 mharc', [
        # The key restates "téacsleabhair" as "téacleabhair" and "Ghaeilge-Bhéarla" as "Ghaeilge –Bhéarla"; the card shows the paper's.
        ('1', '1. Cad a deir Máire faoin ábhar atá i gcuid de na téacsleabhair Ghaeilge faoi láthair?',
         'Cad a deir Máire faoin ábhar atá i gcuid de na téacleabhair Ghaeilge faoi láthair?'),
        ('2', '2. Luaigh fadhb amháin a fheiceann Eoin le hiris Ghaeilge-Bhéarla?', 'Luaigh fadhb amháin a fheiceann Eoin le hiris Ghaeilge –Bhéarla?'),
        ('3', '3. Cén fhadhb a bhain le foilsiú Foinse dar le hEoin?', 'Cén fhadhb a bhain le foilsiú Foinse dar le hEoin?')]),
    ('L-C-P1', 'c-p1', 'Cuid C · Píosa a hAon', 8, 'irish-1-2', 'Píosa 1: 2 marc × 3 = 6 mharc', [
        ('1', '1. Cén saghas comórtais a bhuaigh Crib na nÓg ar Raidió na Gaeltachta?', 'Cén saghas comórtais a bhuaigh Crib na nÓg ar Raidió na Gaeltachta?'),
        ('2a', '2. (a) Céard é Crib na nÓg?', '(a) Céard é Crib na nÓg?'),
        ('2b', '(b) Cén aidhm a bhí leis an gcomórtas ar ghlac Crib na nÓg páirt ann?',
         '(b) Cén aidhm a bhí leis an gcomórtas ar ghlac Crib na nÓg páirt ann?')]),
    ('L-C-P2', 'c-p2', 'Cuid C · Píosa a Dó', 8, 'irish-1-2', 'Píosa 2: 2 marc × 4 = 8 marc', [
        ('1', '1. Cá ndéantar na hearraí atá ar díol i siopa Pagan?', 'Cá ndéantar na hearraí atá ar díol i siopa Pagan?'),
        ('2', '2. Cén rud a raibh tóir ar leith ag daoine óga air?', 'Cén rud a raibh tóir ar leith ag daoine óga air?'),
        ('3a', '3. (a) Luaigh earra amháin a raibh an-éileamh ag na mná air.', '(a) Luaigh earra amháin a raibh an-éileamh ag na mná air.'),
        ('3b', '(b) Cén rud atá beartaithe a chur ar bun go luath?', '(b) Cén rud atá beartaithe a chur ar bun go luath?')]),
    ('L-C-P3', 'c-p3', 'Cuid C · Píosa a Trí', 8, 'irish-1-2', 'Píosa 3: 2 marc × 3 = 6 mharc', [
        ('1', '1. Cé dóibh na scoláireachtaí cónaithe seo?', 'Cé dóibh na scoláireachtaí cónaithe seo?'),
        ('2', '2. Luaigh rud amháin a bhí ar fáil faoin scéim.', 'Luaigh rud amháin a bhí ar fáil faoin scéim.'),
        ('3', '3. Cé mhéad scoláireacht a bronnadh faoin scéim sa bhliain 2010?', 'Cé mhéad scoláireacht a bronnadh faoin scéim sa bhliain 2010?')]),
]
# The section heads printed on the paper above each segment's first question.
HEADS = {3: ['Cloisfidh tú trí cinn d’fhógraí raidió sa chuid seo.', 'FÓGRA A hAON', 'FÓGRA A DÓ'], 4: ['FÓGRA A TRÍ'],
         5: ['Cloisfidh tú trí cinn de chomhráite sa chuid seo.', 'COMHRÁ A hAON', 'An Chéad Mhír', 'An Dara Mír'],
         6: ['COMHRÁ A DÓ'], 7: ['COMHRÁ A TRÍ'], 8: ['Cloisfidh tú trí cinn de phíosaí nuachta raidió/teilifíse sa chuid seo.',
                                                       'PÍOSA A hAON', 'PÍOSA A DÓ', 'PÍOSA A TRÍ']}
# The key's own section headings, which sit between one question's answers and the next question's number.
KEY_FURNITURE = re.compile(r'(?:\s+(?:CUID A|Cuid [BC]|Fógra [aA] (?:hAon|Dó|Trí)|Comhrá [aA] (?:hAon|Dó|Trí)|Píosa a (?:hAon|Dó|Trí)'
                           r'|An Chéad Mhír|An Dara Mír))*\s*$')


def material():
    import fitz
    paper_path = ROOT / f'paper-trail-corpus/exampapers/2010/{FILE}.pdf'
    scheme_path = ROOT / f'paper-trail-corpus/markingschemes/2010/{SCHEME_FILE}.pdf'
    assert hashlib.sha256(paper_path.read_bytes()).hexdigest() == PAPER_SHA, 'Aural paper changed: repeat visual review'
    assert hashlib.sha256(scheme_path.read_bytes()).hexdigest() == SCHEME_SHA, 'Scheme changed: repeat visual review'
    paper, scheme = fitz.open(paper_path), fitz.open(scheme_path)
    assert symbol_audit(paper) == {} and symbol_audit(scheme) == SCHEME_GLYPHS, 'Symbol glyphs changed: repeat the glyph review'
    texts = [clean(p.get_text()) for p in paper]
    stext = [clean(page_text(p)) for p in scheme]
    tariffs = re.sub(r'\s+', ' ', stext[18])
    # PDF 19: the aural's marks and its sections' tariffs; PDF 20–25 the key; PDF 26–30 the script; PDF 31–32 blank.
    assert tariffs.startswith('18 CLUASTUISCINT (100 marc) { (i) Tuiscint = 90 marc }'), tariffs[:80]
    assert '(ii) Cumas Gaeilge = 10 marc' in tariffs and '(iii) Iomlán = 100 marc' in tariffs
    assert stext[25].startswith('25 Triail Chluastuisceana: Téipscript 2010 Fógra a hAon') and not stext[30] and not stext[31]
    key, starts = '', []
    for number in range(20, 26):
        starts.append((len(key), number))
        key += re.sub(r'^\d+\s', '', stext[number - 1]) + ' '
    key = key.strip()
    assert key.startswith('CUID A Fógra a hAon 1 (a) Cén cumann') and key.endswith('• 24 = 2m'), (key[:60], key[-40:])
    # Each chunk opens at its question's printed number where the key prints one ("1 (a) Cén cumann …", "2 Cá háit …", once
    # "1. Cén fáth …"; a (b) carries none), as the 2012 and 2013 keys' chunks do, and runs to the next question's number.
    found, pos = [], 0
    for n, restated in [(n, restated) for *_, questions in SEGMENTS for n, _, restated in questions]:
        start = key.index(restated, pos)
        if len(n) == 1 or n[1] == 'a':
            number = re.search(rf'(?<!\S){n[0]}\.?\s+$', key[pos:start])
            assert number, (n, key[start - 20:start])
            start = pos + number.start()
        found.append((restated, start))
        pos = start + len(restated)
    chunks, pages = {}, {}
    for index, (anchor, start) in enumerate(found):
        end = found[index + 1][1] if index + 1 < len(found) else len(key)
        chunk = KEY_FURNITURE.sub('', key[start:end]).strip()
        assert '•' in chunk and re.search(r'=\s*\d\s*m\b', chunk) and not re.search(r'\s\d$', chunk), anchor
        assert not re.search(r'CUID|Cuid [BC]|Fógra [aA] |Comhrá [aA] |Píosa a |Mhír', chunk), chunk[-60:]
        chunks[anchor] = chunk
        pages[anchor] = sorted({number for offset, number in starts if start <= offset < start + len(chunk)} |
                               {max(number for offset, number in starts if offset <= start)})
    for _, _, _, page, _, line, questions in SEGMENTS:
        assert line in tariffs, line
        for n, question, restated in questions:
            assert comparable(question) in comparable(texts[page - 1]), (page, n)
        for head in HEADS.get(page, []):
            assert comparable(head) in comparable(texts[page - 1]), (page, head)
    assert sum(len(q) for *_, q in SEGMENTS) == 45 and len(chunks) == 45
    assert 'Caithfidh do chuid freagraí uile sa triail seo a bheith i nGaeilge, ach amháin nuair nach gá sin.' in texts[1]
    return dict(texts=texts, chunks=chunks, pages=pages, decisions=selection_decisions(paper))


def build():
    m = material()
    cards = []
    audio = dict(kind='source-audio', title='Triail Chluastuisceana 2010', playbackUrl=AUDIO_URL, secFileid='LC001ZLP017IV.mp3',
                 canonicalUrl=AUDIO_URL, attribution='© State Examinations Commission.',
                 presentationNote='Play the official recording and use the section heading on this card to follow the correct part.')
    # Section "A": the deck maps an Irish sitting's "Aural Paper" to section A; paper stays 1, as 2011's aural cards.
    for key, suffix, ref, page, topic, line, questions in SEGMENTS:
        criteria = [dict(id=f'q{n}', label=f'Ceist {n[0]}' + (f'({n[1]})' if len(n) > 1 else ''), kind='award', maxMarks=2,
                         permittedMarks=printed_marks(m['chunks'][restated], 2), guidanceKind='exact', guidance=[m['chunks'][restated]])
                    for n, _, restated in questions]
        pages = sorted({p for _, _, restated in questions for p in m['pages'][restated]})
        cards.append(dict(
            id=f'irish-2010-hl-listening-{suffix}', year=2010, level='higher', paper=1, section='A',
            questionRef=f'2010 HL Cluastuiscint {ref}', questionText=' '.join(q for _, q, _ in questions),
            totalMarks=2 * len(questions), topicId=topic, conceptId=f'irish-listening-{suffix}', paperFileid=FILE,
            schemeFileid=SCHEME_FILE, paperPage=page, schemePage=pages[0], schemePages=[19, *pages], atlasQuestionId=key,
            reviewedAt=REVIEWED_AT, reviewedPaperPages=[page],
            taskRequirements=['Éist leis an taifeadadh oifigiúil.', 'Freagair gach mír atá priontáilte ar an gcárta.'],
            criteria=criteria,
            markingGuideNote=f'{KEY_NOTE} {LANGUAGE}',
            audioMaterial=dict(audio, label=ref),
            sourceMaterial=dict(kind='source-text', label=f'Cluastuiscint {ref}', title=f'Gaeilge Ardleibhéal 2010 · Triail Chluastuisceana · {ref}',
                                pages=[page], attribution='© State Examinations Commission.', presentationNote=SOURCE_NOTE)))
    assert len(cards) == 12 and sum(len(c['criteria']) for c in cards) == 45 and sum(c['totalMarks'] for c in cards) == 90
    assert len({c['id'] for c in cards}) == len(cards) and len({c['atlasQuestionId'] for c in cards}) == len(cards)
    for card in cards:
        assert sum(cr['maxMarks'] for cr in card['criteria']) == card['totalMarks'], card['id']
        for cr in card['criteria']:
            assert all(not re.search('[-]', g) for g in cr['guidance']), (card['id'], cr['id'])
    sr = json.loads(SOURCE_REVIEW.read_text())
    review = dict(year=2010, level='higher', paperFileid=FILE + '.pdf', schemeFileid=SCHEME_FILE + '.pdf',
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
    print(f"Irish Higher 2010 aural: {len(data['cards'])} reviewed cards (45 printed listening questions); the archive remains incomplete.")


if __name__ == '__main__':
    main()
