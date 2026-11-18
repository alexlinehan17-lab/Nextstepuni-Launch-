#!/usr/bin/env python3
"""Reviewed 2012 Higher Paper 1 (Cluastuiscint agus Ceapadóireacht): new cards, no legacy component.

Paper PDF 1–8 (the paper is the answer booklet for Cuid I: the cover carries the instructions, Cuid A is on
page 2, B on 3–4, C on 5, the composition Treoracha and the examiner's box sit on page 6 and the choice and
titles on page 7; page 8 is blank) and the Paper 1 pages of the combined LC001ALP000IV scheme (PDF 1–15)
reviewed on 2026-11-05. Scheme PDF 16–26 belong to Paper 2 and PDF 27–28 are blank; 2012 prints no
modified marking scheme. Counts are assertions, not corpus-completeness proof.

Layout differences from 2013 (irish_higher_2013_p1.py): the cover tariffs and the language deduction are on
PDF 3 ("2 marc × 5", "× 4", "× 7", "× 7", "× 3", "× 4"); the listening transcript runs PDF 4–6 and the answers
PDF 7–12, two columns per question (accepted answers, then those refused at 0). The answer key prints its
tariffs and prices with no unit: each question's tariff in brackets after it ("(2)", "(2 + 2)", "(2+2)"), each
answer "= 2", "= 0", "= 1 + 1" (a start and an end, 1 each), "= 2 + 2" (both points of a two-point question)
and once "= 2m". Fógra a hAon prints four questions (Ceist 2 at 2 + 2), Fógra a Dó four (the paper numbers its
last "4."; the scheme "3."), Comhrá a hAon's first mír three and its second four, Comhrá a Dó's first mír three
(its 1(a) at 2 + 2) and its second three, Píosa a hAon three and Píosa a Dó four (28). The composition is
marked Ionramháil Ábhair 20 + Cumas Gaeilge 80 (PDF 13–15), with no Stíl mark, no S1–S4 grades and no page of
short / off-title reductions (the off-title pro-rata note sits inside the Cumas Gaeilge text on PDF 13); its
choice is one of four groups, A–D.

Glyph repair (read from the font of every span and the rendered page, not guessed): the Ábhar band table on
PDF 15 draws its first band "Ionramháil an-mhaith ar fad → sármhaith" with Wingdings-Regular U+F0E0, read as
"→"; the cover tariffs on PDF 3 draw × with SymbolMT U+F0B4, read as "×" (no card reads PDF 3's table beyond its
printed totals; the searchable scheme text carries both repairs). The paper's composition box headings on page 7 are flanked by SymbolMT dashes (U+F02D); no
card or selection line reads them. Comhrá a Dó's key (PDF 10) prints a boxed caution "Cúramach" with an arrow
to the An Chéad Mhír heading; the text layer sets it after the last answer on the page, so it is cut from
1(a)'s answers by exact match (examiner furniture, like the score boxes) and recorded in the review.

The card unit follows the reviewed 2013–2026 components: one card per printed listening segment (Fógra, Comhrá
mír, Píosa), each printed question its own criterion at its published 2 or 2 + 2 tariff (a 1-mark partial is
allowed only where the scheme prints one for that question), and one whole 100-mark card per printed
composition title (choose one of A, B, C, D; no combination cards). `main` writes
components/MarkBank/cards/irish/higher-2012-p1-authored.json with its review record, and the searchable scheme
text examiner-reports/irish/schemes/2012-hl.md.
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
OUT = ROOT / 'components/MarkBank/cards/irish/higher-2012-p1-authored.json'
SCHEME_MD = ROOT / 'examiner-reports/irish/schemes/2012-hl.md'
SOURCE_REVIEW = ROOT / 'scripts/markbank/authored/irish-higher-2012-p1-source-review.json'
REVIEWED_AT = '2026-11-05'
PAPER_SHA = '2299651635484a921493291bea07f6d16697a1f3dbbd07e4270d8f655a512549'
SCHEME_SHA = '890fe382628c17197ac926200f9aa46f63114852daf6eaad87242b482fafcd3f'
DIRECTIVE = re.compile(r'rogha|roghna|Freagair|Cuir tic|Ainmnigh|Luaigh|\bchoose\b|\beither\b|\bany\b|one of|\bnó\b|dhá phointe|trí phointe|dhá rud|dó/di|Cuir ciorcal|dhá thagairt|dhá ch|dhá dh|an dá|ceann amháin|amháin|\bdhá\b', re.I)
# The SEC archive serves the 2012 listening test as LC001ZLPO17IV.mp3 (letter O); the zero spelling other years use is 404.
AUDIO_URL = 'https://www.examinations.ie/archive/exampapers/2012/LC001ZLPO17IV.mp3'
SOURCE_NOTE = 'Shown page-for-page from the official examination paper; swipe to move between pages.'
LANGUAGE = ('Scheme PDF 3: “Bainfear ó 0 go 3 ar chaighdeán na Gaeilge.” This 0–3 deduction applies once to the whole '
            'listening section (Tuiscint 60 − Cumas Gaeilge 0–3), never inside a single card.')
# Glyphs the text layer mis-decodes, keyed by (font, character) and read from the rendered page.
GLYPHS = {('Wingdings-Regular', '\uf0e0'): '→', ('SymbolMT', '\uf0b4'): '×'}
SCHEME_GLYPHS = {(3, 'SymbolMT', '\uf0b4'): 6, (15, 'Wingdings-Regular', '\uf0e0'): 1}
PAPER_GLYPHS = {(7, 'SymbolMT', '\uf02d'): 8}
# The boxed caution beside Comhrá a Dó's An Chéad Mhír heading (PDF 10), set by the text layer after 1(a)'s answers.
CAUTION = 'Cúramach'


def clean(text):
    return re.sub(r'\s+', ' ', symbol_text(text)).strip()


def comparable(text):
    return re.sub(r'[^\w]+', '', text.lower())


def criterion(id, label, marks, guidance, kind='quality'):
    return dict(id=id, label=label, kind='award', maxMarks=marks, permittedMarks=list(range(marks + 1)),
                guidanceKind=kind, guidance=guidance)


def source(ref, pages):
    return dict(kind='source-text', label=ref, title=f'Gaeilge Ardleibhéal 2012 · Páipéar 1 · {ref}', pages=pages,
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
                    if span['font'].startswith(('Symbol', 'Wingdings')):
                        for char in span['chars']:
                            audit[(number, span['font'], char['c'])] += 1
    return dict(audit)


def scheme_pages(doc):
    """Each scheme page's text with the audited glyph repairs applied, span by span."""
    pages = []
    for page in doc:
        lines = []
        for block in page.get_text('rawdict')['blocks']:
            for line in block.get('lines', []):
                lines.append(''.join(GLYPHS.get((span['font'], char['c']), char['c']) for span in line['spans'] for char in span['chars']))
        pages.append('\n'.join(lines))
    return pages


class Marked:
    """Scheme text across pages with page markers, so each slice knows its pages."""

    def __init__(self, stext, first, last):
        self.text = ''
        for p in range(first, last + 1):
            body = re.sub(r'^\d+\s', '', stext[p - 1])
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


def printed_marks(chunk, marks):
    """The marks a question can earn: 0, its tariff, the single prices its answers print ("= 2", "= 1", "= 2m") and the
    totals of the split prices ("= 1 + 1", "= 1 + 0", "= 2 + 2", the welded "= 1 + 09 go dtí 4.05" read as 1 + 0)."""
    values = {0, marks}
    for a, b in re.findall(r'=\s*(\d)\s*\+\s*(\d)', chunk):
        values |= {int(a), int(a) + int(b)}
    values |= {int(v) for v in re.findall(r'=\s*(\d)(?!\s*\+)(?:m\b)?', chunk)}
    return sorted(v for v in values if v <= marks)


def material():
    """Lifted paper prompts and scheme text."""
    import fitz
    paper_path = ROOT / f'paper-trail-corpus/exampapers/2012/{FILE}.pdf'
    scheme_path = ROOT / f'paper-trail-corpus/markingschemes/2012/{SCHEME_FILE}.pdf'
    assert hashlib.sha256(paper_path.read_bytes()).hexdigest() == PAPER_SHA, 'Paper changed: repeat visual review'
    assert hashlib.sha256(scheme_path.read_bytes()).hexdigest() == SCHEME_SHA, 'Scheme changed: repeat visual review'
    paper, scheme = fitz.open(paper_path), fitz.open(scheme_path)
    assert symbol_audit(scheme) == SCHEME_GLYPHS and symbol_audit(paper) == PAPER_GLYPHS, 'Symbol glyphs changed: repeat the glyph review'
    texts = [clean(p.get_text()) for p in paper]
    stext = [clean(t) for t in scheme_pages(scheme)]
    # The answers run PDF 7–12; the composition heading on PDF 13 is the stop.
    listening = Marked(stext, 7, 13)
    # (key, id suffix, ref, paper page, topic, part, total, [(n, paper prompt, marks, scheme anchor)])
    segments = [
        ('L-A-F1', 'a-f1', 'Cuid A · Fógra a hAon', 2, 'irish-1-0', 'A', 10, [
            ('1a', '1. (a) Cén scoil atá i gceist san fhógra seo?', 2, '1. (a) Cén scoil atá i gceist'),
            # The scheme reprints this question "Cé mhéad daltaí atá ag freastal …"; the card shows the paper's "dalta".
            ('1b', '(b) Cé mhéad dalta atá ag freastal ar an scoil i láthair na huaire?', 2, '(b) Cé mhéad daltaí atá ag freastal'),
            ('2', '2. Luaigh dhá cháilíocht nach mór a bheith ag iarrthóirí:', 4, '2. Luaigh dhá cháilíocht'),
            ('3', '3. Cad é an dáta deireanach le haghaidh na n-iarratas?', 2, '3. Cad é an dáta deireanach')]),
        ('L-A-F2', 'a-f2', 'Cuid A · Fógra a Dó', 2, 'irish-1-0', 'A', 8, [
            ('1', '1. Cad air a ndearnadh ceiliúradh speisialta?', 2, '1. Cad air a ndearnadh'),
            ('2a', '2. (a) Cén fáth ar eagraíodh an ócáid seo?', 2, '2. (a) Cén fáth ar eagraíodh'),
            ('2b', '(b) Cad a rinne daltaí ó bhunscoileanna Chorca Dhuibhne i rith na hócáide?', 2, '(b) Cad a rinne daltaí ó bhunscoileanna'),
            # The paper numbers this question "4." (it prints no 3 in Fógra a Dó); the scheme numbers it "3.".
            ('4', '4. Ainmnigh an leabhar a bhfuil leagan Iodáilise de ar fáil.', 2, '3. Ainmnigh an leabhar')]),
        ('L-B-C1-M1', 'b-c1-first', 'Cuid B · Comhrá a hAon · An Chéad Mhír', 3, 'irish-1-1', 'B', 6, [
            ('1', '1. Luaigh pointe amháin eolais a bhí sa taighde, dar le Máire', 2, '1. Luaigh pointe amháin eolais a bhí sa taighde'),
            ('2', '2. Cén locht a fhaigheann Rónán ar an taighde?', 2, '2. Cén locht a fhaigheann'),
            ('3', '3. Luaigh rud amháin a chonaic Rónán sa taighde a bhí spéisiúil, dar leis.', 2, '3. Luaigh rud amháin a chonaic Rónán')]),
        ('L-B-C1-M2', 'b-c1-second', 'Cuid B · Comhrá a hAon · An Dara Mír', 3, 'irish-1-1', 'B', 8, [
            ('1', '1. Luaigh tuairim amháin a bhí ag na daoine óga faoin scoil, dar leis an taighde.', 2, '1. Luaigh tuairim amháin'),
            ('2', '2. Cén rud atá difriúil san Eoraip, dar le Máire?', 2, '2. Cén rud atá difriúil'),
            ('3a', '3. (a) Cén lá scoile atá ag Rónán faoi láthair?', 2, '3. (a) Cén lá scoile'),
            # The scheme reprints this question "… faoin athrú san amchlár?"; the card shows the paper's.
            ('3b', '(b) Cén fáth nach gá do Rónán a bheith buartha faoi athrú san amhchlár?', 2, '(b) Cén fáth nach gá do Rónán')]),
        ('L-B-C2-M1', 'b-c2-first', 'Cuid B · Comhrá a Dó · An Chéad Mhír', 4, 'irish-1-1', 'B', 8, [
            # The paper prints "Ronnie Dealney" here (scheme and the paper's later questions "Delaney"); the card shows the paper's.
            ('1a', '1. (a) Luaigh dhá phointe eolais faoi ghaisce Ronnie Dealney sna cluichí Oilimpeacha.', 4, '1. (a) Luaigh dhá phointe eolais faoi ghaisce'),
            ('1b', '(b) Cén fáth ar thug bua Delaney ardú meanman do na Gaeil?', 2, '(b) Cén fáth ar thug bua Delaney'),
            ('2', '2. Cár rugadh Ronnie Delaney?', 2, '2. Cár rugadh Ronnie Delaney')]),
        ('L-B-C2-M2', 'b-c2-second', 'Cuid B · Comhrá a Dó · An Dara Mír', 4, 'irish-1-1', 'B', 6, [
            ('1', '1. Conas a chuir Ronnie Delaney suim sa lúthchleasaíocht ar dtús?', 2, '1. Conas a chuir Ronnie Delaney'),
            ('2', '2. Cén fáth a ndeachaigh Ronnie Delaney go hOllscoil Villanova?', 2, '2. Cén fáth a ndeachaigh Ronnie Delaney'),
            # The paper prints "lúthcleasaíocht" here; the scheme reprints "lúthchleasaíocht". The card shows the paper's.
            ('3', '3. Cén fáth arbh éigean do Ronnie Delaney éirí as an lúthcleasaíocht agus é óg?', 2, '3. Cén fáth arbh éigean')]),
        ('L-C-P1', 'c-p1', 'Cuid C · Píosa a hAon', 5, 'irish-1-2', 'C', 6, [
            ('1', '1. Cár seoladh an leabhar “The Waves of Tory”?', 2, '1. Cár seoladh an leabhar'),
            # The scheme reprints this question "Cén post ata …"; the card shows the paper's "atá".
            ('2', '2. Cén post atá ag Jim Hunter?', 2, '2. Cén post ata ag Jim Hunter'),
            ('3', '3. Luaigh tréith amháin de mhuintir Thoraí, dar leis an údar.', 2, '3. Luaigh tréith amháin de mhuintir Thoraí')]),
        ('L-C-P2', 'c-p2', 'Cuid C · Píosa a Dó', 5, 'irish-1-2', 'C', 8, [
            ('1', '1. Cé atá ag déanamh na dtairiscintí?', 2, '1. Cé atá ag déanamh na dtairiscintí'),
            ('2', '2. Cad é aidhm an tionscnaimh seo?', 2, '2. Cad é aidhm an tionscnaimh'),
            ('3a', '3. (a) Cad a bheidh daoine ábalta a dhéanamh de bharr an córas leathanbhanda a bheith ann?', 2, '3. (a) Cad a bheidh daoine ábalta'),
            ('3b', '(b) Cén uimhir theileafóin atá luaite?', 2, '(b) Cén uimhir theileafóin')]),
    ]
    anchors = [q[3] for seg in segments for q in seg[7]]
    heading = re.compile(r'\s*(FÓGRA A DÓ|Cuid B COMHRÁ a hAON An Chéad Mhír|An Dara Mír|COMHRÁ A DÓ An Chéad Mhír|'
                         r'Cuid C PÍOSA A hAON|PÍOSA A DÓ)\s*$')

    def furniture(raw):
        # The next segment's printed heading precedes the following question; it must not add a page.
        while True:
            trimmed = heading.sub('', re.sub(r'(\s*⟦\d+⟧\s*)+$', '', raw))
            if trimmed == raw:
                return raw
            raw = trimmed
    # The transcript (PDF 4–6) prints no numbered question; the key opens on PDF 7 with Fógra a hAon's Ceist 1(a) and no heading.
    assert listening.text.index(anchors[0]) == listening.text.index('⟦7⟧') + len('⟦7⟧ ')
    chunks = iter(listening.split(anchors, 'CEIST 1 - CEAPADÓIREACHT', furniture))
    for seg in segments:
        assert sum(q[2] for q in seg[7]) == seg[6], seg[0]
        for i, (n, prompt, marks, anchor) in enumerate(seg[7]):
            chunk, pages = next(chunks)
            if (seg[0], n) == ('L-B-C2-M1', '1a'):
                # The boxed caution (PDF 10) falls between 1(a)'s answers in the text layer: cut by exact match.
                assert chunk.count(f'soicind = 2 {CAUTION} curiarracht') == 1, chunk
                chunk = chunk.replace(f' {CAUTION} ', ' ')
            assert CAUTION not in chunk and 'CEAPADÓIREACHT' not in chunk and 'Téipscript' not in chunk, (seg[0], n)
            assert not re.search(r'FÓGRA|COMHRÁ|PÍOSA|Cuid [ABC]\b|An Dara Mír|An Chéad Mhír', chunk), (seg[0], n, chunk[-60:])
            assert comparable(prompt) in comparable(texts[seg[3] - 1]), (seg[0], n)
            assert re.search(r'\(2 ?\+ ?2\)' if marks == 4 else r'\? ?\(2\)|\. ?\(2\)', chunk), (seg[0], n, chunk[:90])
            assert not re.search(r'\d\s*m?h?arc\b', chunk), (seg[0], n)  # 2012's key prints no unit
            seg[7][i] = (n, prompt, marks, chunk, pages)
    for page, line in [(2, 'Cloisfidh tú dhá fhógra raidió sa chuid seo.'), (3, 'Cloisfidh tú dhá chomhrá sa chuid seo.'),
                       (5, 'Cloisfidh tú dhá phíosa nuachta sa chuid seo.')]:
        assert comparable(line) in comparable(texts[page - 1]), page
    assert 'Bainfear ó 0 go 3 ar chaighdeán na Gaeilge' in stext[2]
    # The cover table (PDF 3) prints the segment totals the cards carry (2 marc × 5, 4, 7, 7, 3, 4).
    assert all(x in stext[2] for x in ['2 marc × 5', '2 marc × 3', '2 marc × 4', '2 marc × 7', '= 10 marc', '= 8 marc', '= 14 mharc', '= 6 mharc', '18 marc (Eolas)', '28 marc (Eolas)',
                                       '14 marc (Eolas)', 'Tuiscint = 60 marc'])

    # Composition (scheme PDF 13–15). PDF 13 prints the two marks, the examiner's note and the Cumas Gaeilge text (with the
    # off-title pro-rata note), ending at its printed sum "20 + 80 = 100"; PDF 14 the 80-mark table; PDF 15 the Ábhar text and bands.
    page13 = re.sub(r'^\d+\s', '', stext[12])
    assert page13.startswith('CEIST 1 - CEAPADÓIREACHT - 100 marc { (a) Ionramháil Ábhair = 20 marc } (b) Cumas Gaeilge = 80 marc'), page13[:120]
    note = page13[page13.index('Nóta: Caithfidh an Scrúdaitheoir'):page13.index('AN CHEAPADÓIREACHT')].strip()
    unit = page13[page13.index('Gnéithe a bhaineann leis an marcáil'):page13.index('Cumas Gaeilge (80marc)')].strip()
    gaeilge_text = page13[page13.index('Cumas Gaeilge (80marc)'):page13.index('20 + 80 = 100')].strip()
    table80 = re.sub(r'^\d+\s', '', stext[13])
    abhar = re.sub(r'^\d+\s', '', stext[14])
    assert note.endswith('ag bun na hiarrachta ceapadóireachta.') and unit.endswith('mar aonad.'), (note[-60:], unit[-60:])
    assert gaeilge_text.endswith('go ngearrfar pionós pro-rata ar an ábhar agus ar an nGaeilge.') and 'Cuimhnigh ar an treoir seo ón scrúdpháipéar' in gaeilge_text
    assert all(x in table80 for x in ['76-80', '64-67', '52-55', '40-42', '28-31', '16-19', '4-7', '0-3']), table80[-80:]
    assert abhar.startswith('Ionramháil Ábhair = (20 marc)') and abhar.endswith('F/NG 0, 1, 2, 3, 4 marc'), abhar[-60:]
    assert all(x in abhar for x in ['→ sármhaith A 17, 18, 19, 20 marc', '14, 15, 16', '11, 12, 13', '8, 9, 10', '5, 6, 7'])
    # 2012 prints neither S1–S4 grades, a Stíl mark, a page of short / off-title reductions nor a modified marking scheme.
    assert not any(re.search(r'\bS[1-4]\b|róghearr|Easnamhach i gcás|Stíl', t) for t in stext[:15])
    assert not any('Mhodhnaithe' in t for t in stext)
    assert all(t == '' for t in stext[26:28])
    # Paper page 6 prints the Treoracha; page 7 the choice and the length note, then the titles.
    head = ('Treoracha d’iarrthóirí\n'
            'Ní mór do na hiarrthóirí cúram a dhéanamh de chruinneas na teanga. Caillfear marcanna má bhítear faillitheach ann.\n'
            'Ní mór ceangal cinnte leanúnach a bheith ann idir an teideal a roghnaítear agus an t-ábhar a scríobhtar.\n\n'
            'Freagair do rogha CEANN AMHÁIN de A, B, C nó D anseo thíos.\n'
            'Nóta: Ní gá níos mó ná 500-600 focal nó mar sin a scríobh i gcás ar bith.')
    groups = {
        'A': ('AISTE', 'Scríobh AISTE ar CHEANN AMHÁIN de na hábhair seo.', 'irish-2-0', [
            ('a', 'An Ghéarchéim sa chóras sláinte: Mo réiteach uirthi.'), ('b', 'Éire an lae inniu: Tír fháilteach oscailte í.'),
            ('c', 'An Choiriúlacht in Éirinn inniu: Bagairt mhór na linne seo.')]),
        'B': ('SCÉAL', 'Ceap SCÉAL a mbeadh do rogha CEANN AMHÁIN díobh seo oiriúnach mar theideal air.', 'irish-2-3', [
            ('a', 'Dóchas.'), ('b', 'Is ina dhiaidh a chéile a thógtar na caisleáin.')]),
        'C': ('ALT NUACHTÁIN / IRISE', 'Freagair do rogha CEANN AMHÁIN díobh seo.', 'irish-2-1', [
            # The paper prints "Leigh tú alt" (for "Léigh"); the card shows the paper's.
            ('a', 'Leigh tú alt i gceann de na nuachtáin laethúla á rá gur dream leisciúil iad an t-aos óg. Chuir an t-alt fearg ort.\n'
                  'Scríobh an freagra a chuirfeá chuig eagarthóir an nuachtáin ar an ábhar sin.'),
            ('b', 'Chuir tú agallamh ar Uachtarán Chumann Lúthchleas Gael (GAA). Labhair sibh faoi na dúshláin agus faoi na féidireachtaí atá roimh an eagraíocht.\n'
                  'Scríobh an t-alt a bheadh agat bunaithe ar an agallamh sin.')]),
        'D': ('DÍOSPÓIREACHT / ÓRÁID', 'Freagair do rogha CEANN AMHÁIN díobh seo.', None, [
            ('a', 'Scríobh an chaint a dhéanfá i ndíospóireacht scoile ar son an rúin seo a leanas nó ina aghaidh:\n'
                  'Ba chóir d’Éireannaigh a bheith níos measartha ina gcuid ólacháin.'),
            ('b', 'Tá tusa ar tí an scoil a fhágáil. Iarrtar ort píosa cainte a dhéanamh leis na tuismitheoirí, leis na múinteoirí agus leis na daltaí ar an ábhar:\n'
                  'Fiúntas na scoile seo.\nScríobh an píosa cainte a dhéanfá ag an gcruinniú sin.')]),
    }
    for group, (form, instruction, _, titles) in groups.items():
        assert comparable(form) in comparable(texts[6]), group
        for letter, title in titles:
            assert all(comparable(line) in comparable(texts[6]) for line in [instruction, *title.splitlines()]), (group, letter)
    treoracha, choice = head.split('\n\n')
    assert all(comparable(line) in comparable(texts[5]) for line in treoracha.splitlines())
    assert all(comparable(line) in comparable(texts[6]) for line in choice.splitlines())
    decisions = selection_decisions(paper)
    return dict(decisions=decisions, paper_path=paper_path, scheme_path=scheme_path, texts=texts, segments=segments, head=head,
                groups=groups, composition=dict(note=note, unit=unit, gaeilge=[gaeilge_text, table80], abhar=abhar))


COMPOSITION_REASONS = {
    'A': 'Each printed essay title is a separate route.',
    'B': 'Each printed title is a separate route; the story itself is open.',
    'C': 'Each printed article task is a separate route.',
    'D': '“ar son … nó ina aghaidh” is the speaker’s stance inside one speech; both stances are marked identically.'}


def build():
    m = material()
    cards = []
    audio = dict(kind='source-audio', title='Triail Chluastuisceana 2012', playbackUrl=AUDIO_URL, secFileid='LC001ZLPO17IV.mp3',
                 canonicalUrl=AUDIO_URL, attribution='© State Examinations Commission.',
                 presentationNote='Play the official recording and use the section heading on this card to follow the correct part.')
    for key, suffix, ref, page, topic, part, total, questions in m['segments']:
        criteria = []
        for n, prompt, marks, chunk, _ in questions:
            cr = criterion(f'q{n}', f'Ceist {n[0]}' + (f'({n[1]})' if len(n) > 1 else ''), marks, [chunk], 'exact')
            cr['permittedMarks'] = printed_marks(chunk, marks)
            criteria.append(cr)
        pages = sorted({p for q in questions for p in q[4]})
        cards.append(dict(
            id=f'irish-2012-hl-p1-listening-{suffix}', year=2012, level='higher', paper=1, section='1',
            questionRef=f'2012 HL Paper 1 Cluastuiscint {ref}', questionText=' '.join(q[1] for q in questions),
            totalMarks=total, topicId=topic, conceptId=f'irish-listening-{suffix}', paperFileid=FILE, schemeFileid=SCHEME_FILE,
            paperPage=page, schemePage=pages[0], schemePages=pages, atlasQuestionId=key, reviewedAt=REVIEWED_AT, reviewedPaperPages=[page],
            taskRequirements=['Éist leis an taifeadadh oifigiúil.', 'Freagair gach mír atá priontáilte ar an gcárta.'],
            criteria=criteria,
            markingGuideNote='The listed responses and tariffs come from the 2012 SEC marking scheme; equivalent wording with the same meaning is accepted. '
                             'Each printed question is marked at its own published tariff (2, or 2 + 2 for two points); the scheme prints its marks '
                             'without a unit (“= 2”, “= 1 + 1”). ' + LANGUAGE,
            audioMaterial=dict(audio, label=ref), sourceMaterial=source(f'Cluastuiscint {ref}', [page])))
    c = m['composition']
    for group, (form, instruction, topic, titles) in m['groups'].items():
        for letter, title in titles:
            cards.append(dict(
                id=f'irish-2012-hl-p1-composition-{group.lower()}-{letter}', year=2012, level='higher', paper=1, section='1',
                questionRef=f'2012 HL Paper 1 Ceapadóireacht {group}({letter})',
                questionText=m['head'] + f'\n\n{group} · {form} (100 marc)\n{instruction}\n\n({letter}) {title}',
                totalMarks=100, topicId=topic or ('irish-2-4' if letter == 'a' else 'irish-2-5'), conceptId=f'irish-composition-{group.lower()}',
                paperFileid=FILE, schemeFileid=SCHEME_FILE, paperPage=7, schemePage=13, schemePages=[13, 14, 15],
                atlasQuestionId=f'W-{group}-{letter}', reviewedAt=REVIEWED_AT, reviewedPaperPages=[6, 7],
                taskRequirements=['Lean an fhoirm scríbhneoireachta a iarrtar sa cheist.',
                                  'Coinnigh ceangal cinnte leanúnach idir an teideal agus an t-ábhar.', 'Timpeall 500–600 focal.'],
                criteria=[criterion('abhar', 'Ionramháil Ábhair', 20, [c['abhar'], c['note'], c['unit']]),
                          criterion('gaeilge', 'Cumas Gaeilge', 80, c['gaeilge'])],
                markingGuideNote='Whole 100-mark composition: Ionramháil Ábhair 20 and Cumas Gaeilge 80, assessed as one unit; the 2012 scheme '
                                 'prints no Stíl mark and no separate reductions for a short attempt. Its note on material that is not to the title '
                                 '(a pro-rata penalty on Ábhar and Gaeilge) is part of the Cumas Gaeilge guidance (scheme PDF 13). ' + COMPOSITION_REASONS[group],
                sourceMaterial=source(f'Ceapadóireacht {group}({letter})', [6, 7])))
    listening = [card for card in cards if '-listening-' in card['id']]
    composition = [card for card in cards if '-composition-' in card['id']]
    assert len(listening) == 8 and sum(len(card['criteria']) for card in listening) == 28
    assert sum(card['totalMarks'] for card in listening) == 60 and len(composition) == 9
    assert len({card['id'] for card in cards}) == len(cards) == 17
    for card in cards:
        assert sum(cr['maxMarks'] for cr in card['criteria']) == card['totalMarks'], card['id']
        for cr in card['criteria']:
            assert cr['guidance'] and all(not re.search('[\ue000-\uf8ff]', g) for g in cr['guidance']), (card['id'], cr['id'])
    sr = json.loads(SOURCE_REVIEW.read_text())
    review = dict(year=2012, level='higher', paperFileid=FILE + '.pdf', schemeFileid=SCHEME_FILE + '.pdf',
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
                  boundaries='8 listening segment cards carrying all 28 printed questions as separate criteria at 2 or 2 + 2 (60); '
                             '9 composition title routes at 100 each (choose one of A, B, C, D).')
    return dict(review=review, cards=cards)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    data = build()
    scheme_words_in(data)  # guidance carries the SEC's words only; question and task checks the paper's (irish_lifted.py)
    import fitz
    scheme = fitz.open(ROOT / f'paper-trail-corpus/markingschemes/2012/{SCHEME_FILE}.pdf')
    # The searchable scheme text the provenance checks read (as 2013–2020 and 2026 write their own), glyphs repaired.
    scheme_md = '# Gaeilge Ardleibhéal 2012 — SEC marking scheme (Páipéar 1 agus 2)\n\n' + '\n\n'.join(
        f'## PDF page {i + 1}\n\n' + symbol_text(text) for i, text in enumerate(scheme_pages(scheme)))
    outputs = {OUT: json.dumps(data, ensure_ascii=False, indent=2) + '\n',
               SCHEME_MD: '\n'.join(line.rstrip() for line in scheme_md.splitlines()).rstrip() + '\n'}
    for path, value in outputs.items():
        if args.check:
            assert path.exists() and path.read_text() == value, f'Stale output: {path}'
        else:
            path.write_text(value)
    print(f"Irish Higher 2012 Paper 1: {len(data['cards'])} reviewed cards ({data['review']['printedListeningQuestions']} printed listening questions); the archive remains incomplete.")


if __name__ == '__main__':
    main()
