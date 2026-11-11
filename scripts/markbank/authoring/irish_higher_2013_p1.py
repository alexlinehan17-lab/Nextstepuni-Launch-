#!/usr/bin/env python3
"""Reviewed 2013 Higher Paper 1 (Cluastuiscint agus Ceapadóireacht): new cards, no legacy component.

Paper PDF 1–8 (the paper is the answer booklet for Cuid I: the cover carries the instructions and the
examiner's totals box, Cuid A is on page 2, B on 3–4, C on 5, the composition Treoracha sit on page 6
and the choice and titles on page 7; page 8 is blank) and the Paper 1 pages of the combined
LC001ALP000IV scheme (PDF 1–14 and 29) reviewed on 2026-11-05. Scheme PDF 15–28 belong to Paper 2,
PDF 29 prints the modified marking scheme, and PDF 30–32 are blank. Counts are assertions, not
corpus-completeness proof.

Layout differences from 2014 (irish_higher_2014_p1.py): the cover tariffs and the language deduction
are on PDF 3; the listening transcript runs PDF 4–7 and the answers PDF 8–11 (from "Cuid A ( 18 marc)"
on PDF 8 to Píosa a Dó's last answer at the foot of PDF 11; 2013 prints no cover-mark lines); every
listening question is worth 2 marks ("2 mharc × 5", "× 4", "× 7", "× 7", "× 4", "× 3" on PDF 3):
Fógra a hAon prints five questions, Fógra a Dó four, Comhrá a hAon's first mír three and its second
four, Comhrá a Dó's first mír four and its second three, Píosa a hAon four and Píosa a Dó three (30).
Comhrá a Dó's first-mír Ceist 3 and Píosa a Dó's Ceist 2 (two services, two goods) are priced
"1 mharc + 1 mharc" within their 2 marks. The composition marking is PDF 12–14 (Ionramháil Ábhair
bands and Cumas Gaeilge on PDF 13, with the off-title pro-rata note; the 80-mark table on PDF 14),
with no S1–S4 grades and no page of short / off-title reductions.

Glyph audit (read from the font of every span, not guessed): the cover tariffs on PDF 3 draw the
multiplication sign as SymbolMT U+F0B4; no card reads PDF 3's table beyond its printed totals. The
paper's composition box headings on page 7 are flanked by SymbolMT dashes (U+F02D); they sit only in
the raw selection-decision lines.

The card unit follows the reviewed 2014–2026 components: one card per printed listening segment
(Fógra, Comhrá mír, Píosa), each printed question its own criterion at its published 2-mark tariff
(a 1-mark partial is allowed only where the scheme prints one for that question), and one whole
100-mark card per printed composition title (choose one of A, B, C; no combination cards). `main`
writes components/MarkBank/cards/irish/higher-2013-p1-authored.json with its review record, and the
searchable scheme text examiner-reports/irish/schemes/2013-hl.md.
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
FILE = 'LC001ALP100IV'
SCHEME_FILE = 'LC001ALP000IV'
OUT = ROOT / 'components/MarkBank/cards/irish/higher-2013-p1-authored.json'
SCHEME_MD = ROOT / 'examiner-reports/irish/schemes/2013-hl.md'
SOURCE_REVIEW = ROOT / 'scripts/markbank/authored/irish-higher-2013-p1-source-review.json'
REVIEWED_AT = '2026-11-05'
PAPER_SHA = 'bae74067b7e11207c29017d4a836a3b0983020b365b7804853b8338ddd1bfbe6'
SCHEME_SHA = 'f45b87933de3652ddfbfe8044fb9b7367c58a6a55742316b6d6b2d311c8b1f4b'
DIRECTIVE = re.compile(r'rogha|roghna|Freagair|Cuir tic|Ainmnigh|Luaigh|\bchoose\b|\beither\b|\bany\b|one of|\bnó\b|dhá phointe|trí phointe|dhá rud|dó/di|Cuir ciorcal|dhá thagairt|dhá ch|dhá dh|an dá|ceann amháin|amháin|\bdhá\b', re.I)
AUDIO_URL = 'https://www.examinations.ie/archive/exampapers/2013/LC001ZLP017IV.mp3'
SOURCE_NOTE = 'Shown page-for-page from the official examination paper; swipe to move between pages.'
LANGUAGE = ('Scheme PDF 3: “Bainfear ó 0 go 3 ar chaighdeán na Gaeilge.” This 0–3 deduction applies once to the whole '
            'listening section (Tuiscint 60 − Cumas Gaeilge 0–3), never inside a single card.')
# Every symbol-font glyph in the scheme and the paper, by (PDF page, font, character): the cover's multiplication signs
# (PDF 3), the Calibri/Symbol list bullets of Paper 2 and the SMM (PDF 16, 29), and the paper's box-heading dashes (page 7).
SCHEME_GLYPHS = {(3, 'SymbolMT', ''): 6, (16, 'SymbolMT', ''): 3, (29, 'SymbolMT', ''): 4}
PAPER_GLYPHS = {(7, 'SymbolMT', ''): 6}


def clean(text):
    return re.sub(r'\s+', ' ', symbol_text(text)).strip()


def comparable(text):
    return re.sub(r'[^\w]+', '', text.lower())


def criterion(id, label, marks, guidance, kind='quality'):
    return dict(id=id, label=label, kind='award', maxMarks=marks, permittedMarks=list(range(marks + 1)),
                guidanceKind=kind, guidance=guidance)


def source(ref, pages):
    return dict(kind='source-text', label=ref, title=f'Gaeilge Ardleibhéal 2013 · Páipéar 1 · {ref}', pages=pages,
                attribution='© State Examinations Commission.', presentationNote=SOURCE_NOTE)


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
                    if span['font'].startswith('Symbol'):
                        for char in span['chars']:
                            audit[(number, span['font'], char['c'])] += 1
    return dict(audit)


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
    paper_path = ROOT / f'paper-trail-corpus/exampapers/2013/{FILE}.pdf'
    scheme_path = ROOT / f'paper-trail-corpus/markingschemes/2013/{SCHEME_FILE}.pdf'
    assert hashlib.sha256(paper_path.read_bytes()).hexdigest() == PAPER_SHA, 'Paper changed: repeat visual review'
    assert hashlib.sha256(scheme_path.read_bytes()).hexdigest() == SCHEME_SHA, 'Scheme changed: repeat visual review'
    paper, scheme = fitz.open(paper_path), fitz.open(scheme_path)
    assert symbol_audit(scheme) == SCHEME_GLYPHS and symbol_audit(paper) == PAPER_GLYPHS, 'Symbol glyphs changed: repeat the glyph review'
    texts = [clean(p.get_text()) for p in paper]
    stext = [clean(p.get_text()) for p in scheme]
    # The answers run PDF 8–11; PDF 12 (Cuid II) is the stop.
    listening = Marked(scheme, 8, 12)
    # (key, id suffix, ref, paper page, topic, part, total, [(n, paper prompt, marks, scheme anchor)])
    segments = [
        ('L-A-F1', 'a-f1', 'Cuid A · Fógra a hAon', 2, 'irish-1-0', 'A', 10, [
            ('1a', '1. (a) Cén t-ainm atá ar an gcomórtas a bheidh ar siúl?', 2, '1. (a) Cén t-ainm atá ar an gcomórtas'),
            ('1b', '(b) Cén sórt comórtais é?', 2, '(b) Cén sórt comórtais é ?'),
            ('2a', '2. (a) Luaigh grúpa amháin daltaí a bhfuil an comórtas dírithe orthu.', 2, '2. (a) Luaigh grúpa amháin daltaí'),
            ('2b', '(b) Cé mhéad rannóg a bheidh sa chomórtas?', 2, '(b) Cé mhéad rannóg'),
            ('3', '3. Conas is féidir eolas a fháil faoin gcomórtas?', 2, '3. Conas is féidir eolas a fháil')]),
        ('L-A-F2', 'a-f2', 'Cuid A · Fógra a Dó', 2, 'irish-1-0', 'A', 8, [
            ('1', '1. Cén fáth a bhfuil an t-airgead seo á bhailiú?', 2, '1. Cén fáth a bhfuil an t-airgead'),
            ('2a', '2. (a) Cad a bheidh ar siúl ar an naoú lá de Bhealtaine?', 2, '2. (a) Cad a bheidh ar siúl ar an naoú lá'),
            ('2b', '(b) Cad a bheidh ar siúl oíche Dé Céadaoin seo chugainn?', 2, '(b) Cad a bheidh ar siúl oíche Dé Céadaoin'),
            ('3', '3. Conas a úsáidfear an t-airgead?', 2, '3. Conas a úsáidfear an t-airgead')]),
        ('L-B-C1-M1', 'b-c1-first', 'Cuid B · Comhrá a hAon · An Chéad Mhír', 3, 'irish-1-1', 'B', 6, [
            ('1', '1. Cad a rinne Orla inniu?', 2, '1. Cad a rinne Orla inniu?'),
            ('2', '2. Cén cúrsa ba mhaith le hOrla a dhéanamh san Ollscoil?', 2, '2. Cén cúrsa ba mhaith le hOrla'),
            # The scheme reprints this question as "… aon fhadhb ag Seán go leor pointí a fháil"; the card shows the paper's.
            ('3', '3. Luaigh cúis amháin nach mbeidh aon fhadhb ag Seán na pointí a fháil, dar le hOrla.', 2, '3. Luaigh cúis amháin nach mbeidh aon fhadhb')]),
        ('L-B-C1-M2', 'b-c1-second', 'Cuid B · Comhrá a hAon · An Dara Mír', 3, 'irish-1-1', 'B', 8, [
            ('1', '1. Cad ba mhaith le Seán a fháil don samhradh?', 2, '1. Cad ba mhaith le Seán'),
            ('2', '2. Luaigh fáth amháin nach mbeidh sé éasca ar thuismitheoirí Sheáin an bhliain seo chugainn.', 2, '2. Luaigh fáth amháin nach mbeidh sé éasca'),
            ('3a', '3. (a) Cén rud is mó a chruthaíonn fadhbanna do mhic léinn ollscoile, dar le hOrla?', 2, '3. (a) Cén rud is mó a chruthaíonn'),
            ('3b', '(b) Cad a mholann Orla do Sheán a dhéanamh?', 2, '(b) Cad a mholann Orla')]),
        ('L-B-C2-M1', 'b-c2-first', 'Cuid B · Comhrá a Dó · An Chéad Mhír', 4, 'irish-1-1', 'B', 8, [
            ('1a', '1. (a) Cén scéal a chuala Colm ar an nuacht faoi na heitiltí idir Éirinn agus Nua-Eabhrac?', 2, '1. (a) Cén scéal a chuala Colm'),
            ('1b', '(b) Luaigh rud amháin a deir Síle faoin aimsir a tháinig le hairicín Sandy.', 2, '(b) Luaigh rud amháin a deir Síle'),
            ('2', '2. Tabhair píosa amháin eolais faoin droch-chaoi a bhí ar Manhattan, dar le Síle.', 2, '2. Tabhair píosa amháin eolais'),
            ('3', '3. Luaigh dhá sheirbhís nach raibh ar fáil san óstán.', 2, '3. Luaigh dhá sheirbhís')]),
        ('L-B-C2-M2', 'b-c2-second', 'Cuid B · Comhrá a Dó · An Dara Mír', 4, 'irish-1-1', 'B', 6, [
            ('1', '1. Luaigh rud amháin a chonaic Síle nuair a d’fhéach sí amach an fhuinneog.', 2, '1. Luaigh rud amháin a chonaic Síle'),
            ('2', '2. Cén luach damáiste a rinneadh, dar le Colm?', 2, '2. Cén luach damáiste'),
            ('3', '3. Cén fáth a raibh an stáisiún núicléach dúnta ag an am?', 2, '3. Cén fáth a raibh an stáisiún núicléach')]),
        ('L-C-P1', 'c-p1', 'Cuid C · Píosa a hAon', 5, 'irish-1-2', 'C', 8, [
            ('1', '1. Cad a seoladh aréir?', 2, '1. Cad a seoladh aréir?'),
            ('2', '2. Luaigh gné amháin de shaol an chontae a bhfuil alt faoi sa leabhar.', 2, '2. Luaigh gné amháin de shaol an chontae'),
            ('3a', '3. (a) Cad a rinne Rory Kavanagh agus a chomhimreoirí Meán Fómhair seo caite?', 2, '3 (a) Cad a rinne Rory Kavanagh'),
            ('3b', '(b) Cén praghas atá ar an leabhar seo?', 2, '(b) Cén praghas atá ar an leabhar')]),
        ('L-C-P2', 'c-p2', 'Cuid C · Píosa a Dó', 5, 'irish-1-2', 'C', 6, [
            ('1', '1. Cad a bhí ar siúl i gCúil Aodha Dé Domhnaigh seo caite?', 2, '1. Cad a bhí ar siúl i gCúil Aodha'),
            ('2', '2. Luaigh dhá earra a bhí ar díol ar na seastáin.', 2, '2. Luaigh dhá earra'),
            ('3', '3. Cén fáth a bhfuil Cór Chúil Aodha ag ceiliúradh i mbliana?', 2, '3. Cén fáth a bhfuil Cór Chúil Aodha')]),
    ]
    anchors = [q[3] for seg in segments for q in seg[7]]
    heading = re.compile(r'\s*(Fógra a Dó \(8 marc\)|Cuid B \( 28 marc\) Comhrá a hAon \(14 mharc\) An Chéad Mhír|An Dara Mír|'
                         r'Comhrá A Dó \(14 mharc\) An Chéad Mhír|Cuid C \(14 mharc\) Píosa A hAon \(8 marc\)|Píosa A Dó \(6 mharc\))\s*$')

    def furniture(raw):
        # The next segment's printed heading precedes the following question; it must not add a page.
        while True:
            trimmed = heading.sub('', re.sub(r'(\s*⟦\d+⟧\s*)+$', '', raw))
            if trimmed == raw:
                return raw
            raw = trimmed
    # The transcript (PDF 4–7) prints no numbered question, so the first anchor is the key's own Fógra a hAon Ceist 1(a).
    assert listening.text.index(anchors[0]) > listening.text.index('Cuid A ( 18 marc) Fógra a hAon ( 10 marc)')
    # 2013 prints the language deduction only on PDF 3 and no cover-mark lines: the key ends where Cuid II begins (PDF 12).
    chunks = iter(listening.split(anchors, 'Cuid II - CEAPADÓIREACHT - 100 marc', furniture))
    # The two questions the scheme prices "1 mharc + 1 mharc" within their 2 marks.
    split_two = {('L-B-C2-M1', '3'), ('L-C-P2', '2')}
    for seg in segments:
        assert sum(q[2] for q in seg[7]) == seg[6], seg[0]
        for i, (n, prompt, marks, anchor) in enumerate(seg[7]):
            chunk, pages = next(chunks)
            assert 'Cuid II' not in chunk and 'Téipscript' not in chunk, (seg[0], n)
            assert not re.search(r'Fógra a (?:hAon|Dó) \(|Comhrá [aA] (?:hAon|Dó) \(|Píosa [aA] (?:hAon|Dó) \(|Cuid [ABC] \(|An Dara Mír|An Chéad Mhír', chunk), (seg[0], n, chunk[-60:])
            assert comparable(prompt) in comparable(texts[seg[3] - 1]), (seg[0], n)
            if (seg[0], n) in split_two:
                assert '1 mharc + 1 mharc' in chunk, (seg[0], n, chunk[:80])
            elif (seg[0], n) == ('L-B-C2-M1', '1b'):
                # Síle's weather: the noun 1 mark + its qualifier 1 mark, printed "Gálaí = 1m + cáiliú (móra) = 1 mharc".
                assert len(re.findall(r'= ?1m ?\+ ?cáiliú', chunk)) == 3, chunk[:120]
            else:
                assert '2 mharc' in chunk, (seg[0], n, chunk[:80])
            seg[7][i] = (n, prompt, marks, chunk, pages)
    for page, line in [(2, 'Cloisfidh tú dhá fhógra raidió sa chuid seo.'), (3, 'Cloisfidh tú dhá chomhrá sa chuid seo.'),
                       (5, 'Cloisfidh tú dhá phíosa nuachta sa chuid seo.')]:
        assert comparable(line) in comparable(texts[page - 1]), page
    assert 'Bainfear ó 0 go 3 ar chaighdeán na Gaeilge.' in stext[2]
    # The cover table (PDF 3) prints the segment totals the cards carry (2 mharc × 5, 4, 7, 7, 4, 3).
    assert all(x in stext[2] for x in ['10 marc', '8 marc', '14 mharc', '6 mharc', '18 marc (Eolas)', '28 marc (Eolas)',
                                       '14 mharc (Eolas)', 'Tuiscint = 60 marc'])

    # Composition (scheme PDF 12–14; SMM on PDF 29).
    # The marking text on PDF 12 ends where the printed score boxes begin ("Stíl (5) = Ábhar (15) = …").
    marking = stext[11].split('An Mharcáil:', 1)[1].split('Stíl (5) = Ábhar (15) = Gaeilge (80) =', 1)[0].strip()
    assert marking.endswith('ag bun na hiarrachta ceapadóireachta.'), marking[-80:]
    stil = stext[11].split('Stíl chuí scríbhneoireachta (5 mharc):', 1)[1].split('Ionramháil Ábhair (15 mharc):', 1)[0].strip()
    # Ionramháil Ábhair starts at the foot of PDF 12 and its bands and note are on PDF 13, above Cumas Gaeilge (80marc); the
    # Cumas Gaeilge text (with the off-title pro-rata note) ends PDF 13 and its 80-mark table is PDF 14.
    abhar = (stext[11].split('Ionramháil Ábhair (15 mharc):', 1)[1].strip() + ' '
             + re.sub(r'^\d+\s', '', stext[12]).split('Cumas Gaeilge (80marc)', 1)[0].strip())
    gaeilge = [stext[12][stext[12].index('Cumas Gaeilge (80marc)'):].strip(), stext[13]]
    marking, stil, abhar = [re.sub(r'\s+\d+$', '', t) for t in [marking, stil, abhar]]
    gaeilge = [re.sub(r'\s+\d+$', '', re.sub(r'^\d+\s', '', g)) for g in gaeilge]
    assert stil.startswith('Stíl (5 mharc) = 5 mharc') and stil.endswith('Déantar é seo a mheas faoi Ábhar (15 mharc).'), stil[-60:]
    assert abhar.startswith('Tuairimí, smaointe') and abhar.endswith('iarracht an iarrthóra mar aonad.'), abhar[-60:]
    assert all(x in abhar for x in ['13,14,15', '11,12', '9,10', '6,7,8', '3,4,5', '0,1,2'])
    assert gaeilge[0].endswith('pro-rata ar an ábhar agus ar an nGaeilge.') and 'Cuimhnigh ar an treoir seo ón scrúdpháipéar' in gaeilge[0], gaeilge[0][-80:]
    assert all(x in gaeilge[1] for x in ['76-80', '64-67', '52-55', '40-43', '28-31', '16-19', '4-7', '0-3'])
    # 2013 prints neither S1–S4 grades nor a page of short / off-title reductions.
    assert not any(re.search(r'\bS[1-4]\b|róghearr|Easnamhach i gcás', t) for t in stext[11:14])
    smm = stext[28]
    assert 'Scéim Mharcála Mhodhnaithe' in smm and 'Páipéar 1: An Cheapadóireacht –An Cumas Gaeilge (80 marc)' in smm
    assert all(t == 'Leathanach Bán' for t in stext[29:31]) and stext[31] == ''
    # Paper page 6 prints the Treoracha; page 7 the choice and the length note, then the titles.
    head = ('Treoracha d’iarrthóirí\n'
            'Ní mór do na hiarrthóirí cúram a dhéanamh de chruinneas na teanga. Caillfear marcanna má bhítear faillitheach ann.\n'
            'Ní mór ceangal cinnte leanúnach a bheith ann idir an teideal a roghnaítear agus an t-ábhar a scríobhtar.\n\n'
            'Freagair do rogha CEANN AMHÁIN de A, B nó C anseo thíos.\n'
            'Nóta: Ní gá níos mó ná 500-600 focal nó mar sin a scríobh i gcás ar bith.')
    groups = {
        'A': ('AISTE nó ALT NUACHTÁIN / IRISE', 'Scríobh AISTE NÓ ALT NUACHTÁIN / IRISE ar CHEANN AMHÁIN de na hábhair seo.', 'irish-2-0', [
            ('a', 'Rudaí sa saol a théann i bhfeidhm orm.'), ('b', 'Imirce as Éirinn sa lá atá inniu ann.'),
            ('c', 'Cúrsaí na timpeallachta – mar atá agus mar a bheidh.'), ('d', 'Réaltaí spóirt an lae inniu.'),
            ('e', 'Éire mar ionad saoire.')]),
        'B': ('SCÉAL', 'Ceap SCÉAL a mbeadh do rogha CEANN AMHÁIN díobh seo oiriúnach mar theideal air.', 'irish-2-3', [
            ('a', 'Sonas.'), ('b', 'Is minic a bhíonn ciúin ciontach.')]),
        'C': ('DÍOSPÓIREACHT / ÓRÁID', 'Freagair do rogha CEANN AMHÁIN díobh seo.', None, [
            ('a', 'Scríobh an chaint a dhéanfá i ndíospóireacht scoile ar son an rúin seo a leanas nó ina aghaidh:\nNíl na polaiteoirí ag stiúradh chúrsaí na hÉireann mar is ceart.'),
            ('b', 'Iarradh ort píosa cainte a dhéanamh ag cruinniú de Chomhairle na Mac Léinn sa scoil seo agatsa ar an ábhar:\nAn Córas Oideachais in Éirinn inniu.\nScríobh an píosa cainte a dhéanfá ag an gcruinniú sin.')]),
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
    audio = dict(kind='source-audio', title='Triail Chluastuisceana 2013', playbackUrl=AUDIO_URL, secFileid='LC001ZLP017IV.mp3',
                 canonicalUrl=AUDIO_URL, attribution='© State Examinations Commission.',
                 presentationNote='Play the official recording and use the section heading on this card to follow the correct part.')
    for key, suffix, ref, page, topic, part, total, questions in m['segments']:
        criteria = []
        for n, prompt, marks, chunk, _ in questions:
            # A 1-mark partial only where the scheme prints one for this question ("= 1 mharc", "1 mharc + 1 mharc").
            partial = bool(re.search(r'=\s*1 mharc|1 mharc \+ 1 mharc', chunk))
            cr = criterion(f'q{n}', f'Ceist {n[0]}' + (f'({n[1]})' if len(n) > 1 else ''), marks, [chunk], 'exact')
            cr['permittedMarks'] = (list(range(marks + 1)) if partial else list(range(0, marks + 1, 2)))
            criteria.append(cr)
        pages = sorted({p for q in questions for p in q[4]})
        cards.append(dict(
            id=f'irish-2013-hl-p1-listening-{suffix}', year=2013, level='higher', paper=1, section='1',
            questionRef=f'2013 HL Paper 1 Cluastuiscint {ref}', questionText=' '.join(q[1] for q in questions),
            totalMarks=total, topicId=topic, conceptId=f'irish-listening-{suffix}', paperFileid=FILE, schemeFileid=SCHEME_FILE,
            paperPage=page, schemePage=pages[0], schemePages=pages, atlasQuestionId=key, reviewedAt=REVIEWED_AT, reviewedPaperPages=[page],
            taskRequirements=['Éist leis an taifeadadh oifigiúil.', 'Freagair gach mír atá priontáilte ar an gcárta.'],
            criteria=criteria,
            markingGuideNote='The listed responses and tariffs come from the 2013 SEC marking scheme; equivalent wording with the same meaning is accepted. '
                             'Each printed question is marked at its own published 2-mark tariff (1 + 1 where the scheme splits it for two points). ' + LANGUAGE,
            audioMaterial=dict(audio, label=ref), sourceMaterial=source(f'Cluastuiscint {ref}', [page])))
    c = m['composition']
    for group, (form, instruction, topic, titles) in m['groups'].items():
        for letter, title in titles:
            cards.append(dict(
                id=f'irish-2013-hl-p1-composition-{group.lower()}-{letter}', year=2013, level='higher', paper=1, section='1',
                questionRef=f'2013 HL Paper 1 Ceapadóireacht {group}({letter})',
                questionText=m['head'] + f'\n\n{group} · {form} (100 marc)\n{instruction}\n\n({letter}) {title}',
                totalMarks=100, topicId=topic or ('irish-2-4' if letter == 'a' else 'irish-2-5'), conceptId=f'irish-composition-{group.lower()}',
                paperFileid=FILE, schemeFileid=SCHEME_FILE, paperPage=7, schemePage=12, schemePages=[12, 13, 14],
                atlasQuestionId=f'W-{group}-{letter}', reviewedAt=REVIEWED_AT, reviewedPaperPages=[6, 7],
                taskRequirements=['Lean an fhoirm scríbhneoireachta a iarrtar sa cheist.',
                                  'Coinnigh ceangal cinnte leanúnach idir an teideal agus an t-ábhar.', 'Timpeall 500–600 focal.'],
                criteria=[criterion('stil', 'Stíl chuí scríbhneoireachta', 5, [c['stil']]),
                          criterion('abhar', 'Ionramháil Ábhair', 15, [c['abhar'], c['marking']]),
                          criterion('gaeilge', 'Cumas Gaeilge', 80, c['gaeilge'] + [
                              'Scéim Mharcála Mhodhnaithe (scheme PDF 29): for eligible candidates spelling and the listed grammar features are not counted in the 80-mark Cumas Gaeilge award.'])],
                markingGuideNote='Whole 100-mark composition: Stíl 5, Ionramháil Ábhair 15, Cumas Gaeilge 80, assessed as one unit. '
                                 'The 2013 scheme prints no separate reductions for a short attempt; its note on material that is not to the title '
                                 '(a pro-rata penalty on Ábhar and Gaeilge) is part of the Cumas Gaeilge guidance (scheme PDF 13). ' + COMPOSITION_REASONS[group],
                sourceMaterial=source(f'Ceapadóireacht {group}({letter})', [6, 7])))
    listening = [card for card in cards if '-listening-' in card['id']]
    composition = [card for card in cards if '-composition-' in card['id']]
    assert len(listening) == 8 and sum(len(card['criteria']) for card in listening) == 30
    assert sum(card['totalMarks'] for card in listening) == 60 and len(composition) == 9
    assert len({card['id'] for card in cards}) == len(cards) == 17
    for card in cards:
        assert sum(cr['maxMarks'] for cr in card['criteria']) == card['totalMarks'], card['id']
        for cr in card['criteria']:
            assert cr['guidance'] and all(not re.search('[-]', g) for g in cr['guidance']), (card['id'], cr['id'])
    sr = json.loads(SOURCE_REVIEW.read_text())
    review = dict(year=2013, level='higher', paperFileid=FILE + '.pdf', schemeFileid=SCHEME_FILE + '.pdf',
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
                  boundaries='8 listening segment cards carrying all 30 printed questions as separate 2-mark criteria (60); '
                             '9 composition title routes at 100 each (choose one).')
    return dict(review=review, cards=cards)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    data = build()
    scheme_words_in(data)  # guidance carries the SEC's words only; question and task checks the paper's (irish_lifted.py)
    import fitz
    scheme = fitz.open(ROOT / f'paper-trail-corpus/markingschemes/2013/{SCHEME_FILE}.pdf')
    # The searchable scheme text the provenance checks read (as 2014–2020 and 2026 write their own).
    scheme_md = '# Gaeilge Ardleibhéal 2013 — SEC marking scheme (Páipéar 1 agus 2)\n\n' + '\n\n'.join(
        f'## PDF page {i + 1}\n\n' + p.get_text() for i, p in enumerate(scheme))
    outputs = {OUT: json.dumps(data, ensure_ascii=False, indent=2) + '\n',
               SCHEME_MD: '\n'.join(line.rstrip() for line in scheme_md.splitlines()).rstrip() + '\n'}
    for path, value in outputs.items():
        if args.check:
            assert path.exists() and path.read_text() == value, f'Stale output: {path}'
        else:
            path.write_text(value)
    print(f"Irish Higher 2013 Paper 1: {len(data['cards'])} reviewed cards ({data['review']['printedListeningQuestions']} printed listening questions); the archive remains incomplete.")


if __name__ == '__main__':
    main()
