#!/usr/bin/env python3
"""Reviewed 2014 Higher Paper 1 (Cluastuiscint agus Ceapadóireacht): new cards, no legacy component.

Paper PDF 1–8 (the paper is the answer booklet for Cuid I: the cover carries the instructions and the
examiner's totals box, Cuid A starts on page 2, the composition Treoracha sit on page 6 and the choice
and titles on page 7; page 8 is blank) and the Paper 1 pages of the combined LC001ALP000IV scheme
(PDF 1–15 and 31) reviewed on 2026-11-05. Scheme PDF 16–30 belong to Paper 2; PDF 32 is empty. Counts
are assertions, not corpus-completeness proof. Same layout as 2016 (irish_higher_2016_p1.py) with
these differences: the cover tariffs are on PDF 3; the listening transcript runs PDF 4–7 and the
answers PDF 7–12 (from "Cuid A ( 18 marc)" on PDF 7 to the cover-mark lines on PDF 12); Fógra a hAon
prints four questions (Ceist 2 at 2 + 2), Fógra a Dó four, Comhrá a hAon's first mír three (its
Ceist 2 at 2 + 2) and its second three, Comhrá a Dó's first mír three and its second three (its
Ceist 1 at 2 + 2), Píosa a hAon three and Píosa a Dó three (its Ceist 3 at 2 + 2); the composition
marking is PDF 12–15 with no S1–S4 grades and no page of short / off-title reductions (the off-title
pro-rata note sits inside the Cumas Gaeilge text on PDF 14), and the 80-mark table ends at N/G íseal
0-3. The modified marking scheme is PDF 31.

Glyph repair (read from the font of every span, not guessed): the scheme's Cumas Gaeilge bullets on
PDF 14 (and the SMM list on PDF 31) are SymbolMT code 0x78, which the text layer returns as "x" and the
page draws as a bullet; they are read as "•". The cover tariffs on PDF 3 use SymbolMT 0x75 ("u", drawn
×); no card reads PDF 3's table.

The card unit follows the reviewed 2016–2026 components: one card per printed listening segment
(Fógra, Comhrá mír, Píosa), each printed question its own criterion at its published 2 or 2 + 2
tariff, and one whole 100-mark card per printed composition title (choose one of A, B, C; no
combination cards). `main` writes components/MarkBank/cards/irish/higher-2014-p1-authored.json with
its review record, and the searchable scheme text examiner-reports/irish/schemes/2014-hl.md.
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
OUT = ROOT / 'components/MarkBank/cards/irish/higher-2014-p1-authored.json'
SCHEME_MD = ROOT / 'examiner-reports/irish/schemes/2014-hl.md'
SOURCE_REVIEW = ROOT / 'scripts/markbank/authored/irish-higher-2014-p1-source-review.json'
REVIEWED_AT = '2026-11-05'
PAPER_SHA = 'ae10d72e0e780ecae2cc666eac9fb6b35d4a3a01b885deddb46927e5c32244fd'
SCHEME_SHA = 'b7b4d9da51f4bbbbeffc853a5457b799c54fe4294e7f9d983a7ec9c355187a4a'
DIRECTIVE = re.compile(r'rogha|roghna|Freagair|Cuir tic|Ainmnigh|Luaigh|\bchoose\b|\beither\b|\bany\b|one of|\bnó\b|dhá phointe|trí phointe|dhá rud|dó/di|Cuir ciorcal|dhá thagairt|dhá ch|dhá dh|an dá|ceann amháin|amháin|\bdhá\b', re.I)
AUDIO_URL = 'https://www.examinations.ie/archive/exampapers/2014/LC001ZLP017IV.mp3'
SOURCE_NOTE = 'Shown page-for-page from the official examination paper; swipe to move between pages.'
LANGUAGE = ('Scheme PDF 3: “Bainfear ó 0 go 3 ar chaighdeán na Gaeilge.” This 0–3 deduction applies once to the whole '
            'listening section (Tuiscint 60 − Cumas Gaeilge 0–3), never inside a single card.')
# Glyphs the text layer mis-decodes, keyed by (font, character) and read from the rendered page: SymbolMT 0x78 draws
# the Cumas Gaeilge list bullet (PDF 14, 31). Every SymbolMT span in the scheme is audited in `scheme_pages`.
GLYPHS = {('SymbolMT', 'x'): '•'}
GLYPH_AUDIT = {(3, 'SymbolMT', 'u'): 6, (14, 'SymbolMT', 'x'): 11, (31, 'SymbolMT', 'x'): 4}


def clean(text):
    return re.sub(r'\s+', ' ', symbol_text(text)).strip()


def comparable(text):
    return re.sub(r'[^\w]+', '', text.lower())


def criterion(id, label, marks, guidance, kind='quality'):
    return dict(id=id, label=label, kind='award', maxMarks=marks, permittedMarks=list(range(marks + 1)),
                guidanceKind=kind, guidance=guidance)


def source(ref, pages):
    return dict(kind='source-text', label=ref, title=f'Gaeilge Ardleibhéal 2014 · Páipéar 1 · {ref}', pages=pages,
                attribution='© State Examinations Commission.', presentationNote=SOURCE_NOTE)


def selection_decisions(paper):
    decisions = json.loads(SOURCE_REVIEW.read_text())['selectionDecisions']
    expected = {(d['page'], d['raw']) for d in decisions}
    found = {(i, clean(line)) for i, page in enumerate(paper, 1)
             for line in page.get_text().splitlines() if DIRECTIVE.search(clean(line))}
    assert found == expected, ('Unclassified/stale selection directives', found - expected, expected - found)
    return decisions


def scheme_pages(doc):
    """Each scheme page's text with the audited glyph repairs applied (span by span, so no letter x is touched)."""
    audit = collections.Counter()
    pages = []
    for number, page in enumerate(doc, 1):
        lines = []
        for block in page.get_text('rawdict')['blocks']:
            for line in block.get('lines', []):
                out = ''
                for span in line['spans']:
                    for char in span['chars']:
                        if span['font'].startswith('Symbol'):
                            audit[(number, span['font'], char['c'])] += 1
                        out += GLYPHS.get((span['font'], char['c']), char['c'])
                lines.append(out)
        pages.append('\n'.join(lines))
    assert dict(audit) == GLYPH_AUDIT, ('Symbol glyphs changed: repeat the glyph review', dict(audit))
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


def material():
    """Lifted paper prompts and scheme text."""
    import fitz
    paper_path = ROOT / f'paper-trail-corpus/exampapers/2014/{FILE}.pdf'
    scheme_path = ROOT / f'paper-trail-corpus/markingschemes/2014/{SCHEME_FILE}.pdf'
    assert hashlib.sha256(paper_path.read_bytes()).hexdigest() == PAPER_SHA, 'Paper changed: repeat visual review'
    assert hashlib.sha256(scheme_path.read_bytes()).hexdigest() == SCHEME_SHA, 'Scheme changed: repeat visual review'
    paper, scheme = fitz.open(paper_path), fitz.open(scheme_path)
    texts = [clean(p.get_text()) for p in paper]
    stext = [clean(t) for t in scheme_pages(scheme)]
    listening = Marked(stext, 7, 12)
    # (key, id suffix, ref, paper page, topic, part, total, [(n, paper prompt, marks, scheme anchor)])
    segments = [
        ('L-A-F1', 'a-f1', 'Cuid A · Fógra a hAon', 2, 'irish-1-0', 'A', 10, [
            ('1', '1. Cad atá á lorg ag Ollscoil Luimnigh?', 2, '1. Cad atá á lorg ag Ollscoil Luimnigh?'),
            ('2', '2. Luaigh dhá cháilíocht atá riachtanach don phost seo.', 4, '2. Luaigh dhá cháilíocht'),
            ('3a', '3. (a) Cad iad na huaireanta oibre sa phost?', 2, '3. (a) Cad iad na huaireanta oibre'),
            ('3b', '(b) Luaigh slí amháin le heolas a fháil faoin bpost seo.', 2, '(b) Luaigh slí amháin le heolas')]),
        ('L-A-F2', 'a-f2', 'Cuid A · Fógra a Dó', 2, 'irish-1-0', 'A', 8, [
            ('1', '1. Cad a thosóidh ar TG4 Dé Luain seo chugainn?', 2, '1. Cad a thosóidh ar TG4'),
            ('2a', '2. (a) Cad a bheidh ar siúl sa Bhrasaíl sa samhradh?', 2, '2. (a) Cad a bheidh ar siúl sa Bhrasaíl'),
            ('2b', '(b) Luaigh rud amháin a bheidh ar an gclár speisialta ar leathuair tar éis a sé.', 2, '(b) Luaigh rud amháin a bheidh ar an gclár'),
            ('3', '3. Cén dáta a thosóidh comórtas leadóige Wimbledon?', 2, '3. Cén dáta a thosóidh')]),
        ('L-B-C1-M1', 'b-c1-first', 'Cuid B · Comhrá a hAon · An Chéad Mhír', 3, 'irish-1-1', 'B', 8, [
            ('1', '1. Cén fáth a bhfuil Áine tuirseach?', 2, '1. Cén fáth a bhfuil Áine tuirseach?'),
            ('2', '2. Luaigh dhá rud a deir Pól faoina chuid laethanta san ollscoil i mbliana.', 4, '2. Luaigh dhá rud a deir Pól'),
            ('3', '3. Luaigh rud amháin a deir Áine faoi na ceisteanna a chuir an scrúdaitheoir.', 2, '3. Luaigh rud amháin a deir Áine')]),
        ('L-B-C1-M2', 'b-c1-second', 'Cuid B · Comhrá a hAon · An Dara Mír', 3, 'irish-1-1', 'B', 6, [
            ('1', '1. Cad é an t-ábhar cainte ba spéisiúla a bhí ag Áine leis an scrúdaitheoir?', 2, '1. Cad é an t-ábhar cainte'),
            ('2', '2. Cad a deir Áine faoi Facebook agus faoi na líonraí sóisialta?', 2, '2. Cad a deir Áine faoi Facebook'),
            ('3', '3. Cá bhfuil Pól ag dul anois?', 2, '3. Cá bhfuil Pól ag dul anois?')]),
        ('L-B-C2-M1', 'b-c2-first', 'Cuid B · Comhrá a Dó · An Chéad Mhír', 4, 'irish-1-1', 'B', 6, [
            ('1', '1. Cén gradam a bhuaigh Seán sa scoil aréir?', 2, '1. Cén gradam a bhuaigh Seán'),
            ('2', '2. Cén club a d’eagraigh Comhairle na Mac Léinn sa scoil le bliain anuas?', 2, '2. Cén club a d’eagraigh'),
            ('3', '3. Scríobh síos pointe amháin a luann Orla faoi dhéagóirí na laethanta seo.', 2, '3. Scríobh síos pointe amháin a luann Orla')]),
        ('L-B-C2-M2', 'b-c2-second', 'Cuid B · Comhrá a Dó · An Dara Mír', 4, 'irish-1-1', 'B', 8, [
            ('1', '1. Luaigh dhá imeacht a chuirtí ar siúl ag am lóin Dé Máirt agus Déardaoin.', 4, '1. Luaigh dhá imeacht a chuirtí'),
            ('2', '2. Scríobh síos rud amháin nach mbíodh cead ag na scoláirí a thabhairt isteach sa cheaintín Dé Céadaoin.', 2, '2. Scríobh síos rud amháin nach mbíodh'),
            ('3', '3. Luaigh ábhar amháin atá sa nuachtlitir a tugadh do gach scoláire roimh shaoire an tsamhraidh.', 2, '3. Luaigh ábhar amháin atá sa nuachtlitir')]),
        ('L-C-P1', 'c-p1', 'Cuid C · Píosa a hAon', 5, 'irish-1-2', 'C', 6, [
            ('1', '1. Cén stáisiún raidió a bhí ag ceiliúradh fiche bliain ar an aer in 2013?', 2, '1. Cén stáisiún raidió'),
            ('2', '2. Cén dream daoine ar a bhfuil an stáisiún raidió seo dírithe?', 2, '2. Cén dream daoine'),
            ('3', '3. Luaigh pointe amháin eolais faoi na hoibrithe a bhíonn ag obair leis an stáisiún raidió seo.', 2, '3. Luaigh pointe amháin eolais faoi na hoibrithe')]),
        ('L-C-P2', 'c-p2', 'Cuid C · Píosa a Dó', 5, 'irish-1-2', 'C', 8, [
            ('1', '1. Cé mhéad mac léinn atá imithe go dtí na hOileáin Fhilipíneacha?', 2, '1. Cé mhéad mac léinn'),
            ('2', '2. Luaigh pointe amháin eolais faoin damáiste a rinne an tíofún in 2013.', 2, '2. Luaigh pointe amháin eolais faoin damáiste'),
            ('3', '3. Ainmnigh dhá imeacht a d’eagraigh na mic léinn chun airgead a bhailiú.', 4, '3. Ainmnigh dhá imeacht')]),
    ]
    anchors = [q[3] for seg in segments for q in seg[7]]
    heading = re.compile(r'\s*(Fógra a Dó \(8 marc\)|Cuid B \( 28 marc\) Comhrá a hAon \(14 mharc\) An Chéad Mhír|An Dara Mír|'
                         r'Comhrá A Dó \(14 mharc\) An Chéad Mhír|Cuid C \(14 mharc\) Píosa A hAon \( 6 mharc\)|Píosa A Dó \( 8 marc\))\s*$')

    def furniture(raw):
        # The next segment's printed heading precedes the following question; it must not add a page.
        while True:
            trimmed = heading.sub('', re.sub(r'(\s*⟦\d+⟧\s*)+$', '', raw))
            if trimmed == raw:
                return raw
            raw = trimmed
    # The transcript (PDF 4–7) prints no numbered question, so the first anchor is the key's own Fógra a hAon Ceist 1.
    assert listening.text.index(anchors[0]) > listening.text.index('Cuid A ( 18 marc) Fógra a hAon ( 10 marc)')
    # 2014 prints the language deduction only on PDF 3; the answer key ends where the cover-mark lines begin (PDF 12).
    chunks = iter(listening.split(anchors, 'Léirigh na marcanna mar seo a leanas ar chlúdach na Cluastuisceana:', furniture))
    for seg in segments:
        assert sum(q[2] for q in seg[7]) == seg[6], seg[0]
        for i, (n, prompt, marks, anchor) in enumerate(seg[7]):
            chunk, pages = next(chunks)
            assert 'Siombailí' not in chunk and 'Anótála' not in chunk and 'Léirigh na marcanna' not in chunk, (seg[0], n)
            assert not re.search(r'Fógra a (?:hAon|Dó) \(|Comhrá [aA] (?:hAon|Dó) \(|Píosa [aA] (?:hAon|Dó) \(|Cuid [ABC] \(|An Dara Mír|An Chéad Mhír', chunk), (seg[0], n, chunk[-60:])
            assert comparable(prompt) in comparable(texts[seg[3] - 1]), (seg[0], n)
            assert (f'{marks // 2} mharc + {marks // 2} mharc' if marks == 4 else '2 mharc') in chunk, (seg[0], n, chunk[:80])
            seg[7][i] = (n, prompt, marks, chunk, pages)
    for page, line in [(2, 'Cloisfidh tú dhá fhógra raidió sa chuid seo.'), (3, 'Cloisfidh tú dhá chomhrá sa chuid seo.'),
                       (5, 'Cloisfidh tú dhá phíosa nuachta sa chuid seo.')]:
        assert comparable(line) in comparable(texts[page - 1]), page
    assert 'Bainfear ó 0 go 3 ar chaighdeán na Gaeilge.' in stext[2]
    # The cover tariffs (PDF 3) print the segment totals the cards carry; "u" is the SymbolMT multiplication sign.
    cover = stext[2]
    assert all(x in cover for x in ['2 mharc u 5', '2 mharc u 4', '2 mharc u 7', '2 mharc u 3', '10 marc', '8 marc', '14 mharc', '6 mharc',
                                    '18 marc (Eolas)', '28 marc (Eolas)', '14 mharc (Eolas)', 'Tuiscint = 60 marc'])

    # Composition (scheme PDF 12–15; SMM on PDF 31).
    # The marking text runs to the end of PDF 12; PDF 13 opens with the printed score boxes, cut by exact match.
    marking = stext[11].split('An Mharcáil:', 1)[1].strip()
    assert marking.endswith('ag bun na hiarrachta ceapadóireachta.'), marking[-80:]
    page13 = stext[12]
    assert page13.startswith('11 Stíl (5) = Ábhar (15) = Gaeilge (80) = CII (100) = Gnéithe a bhaineann leis an marcáil'), page13[:120]
    stil = page13.split('Stíl chuí scríbhneoireachta (5 mharc):', 1)[1].split('Ionramháil Ábhair (15 mharc):', 1)[0].strip()
    abhar = page13.split('Ionramháil Ábhair (15 mharc):', 1)[1].strip()
    gaeilge = [stext[13][stext[13].index('Cumas Gaeilge (80 marc)'):].strip(), stext[14]]
    marking, stil, abhar = [re.sub(r'\s+\d+$', '', t) for t in [marking, stil, abhar]]
    gaeilge = [re.sub(r'\s+\d+$', '', re.sub(r'^\d+\s', '', g)) for g in gaeilge]
    assert stil.startswith('Stíl (5 mharc) = 5 mharc') and abhar.startswith('Tuairimí, smaointe')
    assert all(x in abhar for x in ['13,14,15', '11,12', '9,10', '6,7,8', '3,4,5', '0,1,2'])
    assert gaeilge[0].count('•') == 11 and ' x ' not in gaeilge[0]
    assert gaeilge[0].endswith('go ngearrfar pionós pro-rata ar an ábhar agus ar an nGaeilge.') and 'pionós pro-rata' in gaeilge[0]
    assert all(x in gaeilge[1] for x in ['76-80', '64-67', '52-55', '40-43', '28-31', '16-19', '4-7', '0-3'])
    # 2014 prints neither S1–S4 grades nor a page of short / off-title reductions.
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
            ('a', 'Daoine cáiliúla sa lá atá inniu ann.'), ('b', 'Is iad blianta na hóige na blianta is fearr.'),
            ('c', 'An Bochtanas in Éirinn.'), ('d', 'Cearta daonna in Éirinn sa lá atá inniu ann.'),
            ('e', 'Na rudaí atá tábhachtach i mo shaol.')]),
        'B': ('SCÉAL', 'Ceap SCÉAL a mbeadh do rogha CEANN AMHÁIN díobh seo oiriúnach mar theideal air.', 'irish-2-3', [
            ('a', 'Díomá.'), ('b', 'Ní mar a shíltear a bhítear.')]),
        'C': ('DÍOSPÓIREACHT / ÓRÁID', 'Freagair do rogha CEANN AMHÁIN díobh seo.', None, [
            ('a', 'Scríobh an chaint a dhéanfá i ndíospóireacht scoile ar son an rúin seo a leanas nó ina aghaidh:\nTá feabhas le feiceáil ar chúinsí eacnamaíochta na hÉireann faoi láthair.'),
            ('b', 'Iarradh ort píosa cainte a dhéanamh le grúpa ón nGearmáin, atá ar cuairt ar do scoil, ar an ábhar:\nAn tábhacht a bhaineann leis an nGaeilge agus leis an gcultúr Gaelach.\nScríobh an píosa cainte a dhéanfá ar an ábhar sin.')]),
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
    audio = dict(kind='source-audio', title='Triail Chluastuisceana 2014', playbackUrl=AUDIO_URL, secFileid='LC001ZLP017IV.mp3',
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
            id=f'irish-2014-hl-p1-listening-{suffix}', year=2014, level='higher', paper=1, section='1',
            questionRef=f'2014 HL Paper 1 Cluastuiscint {ref}', questionText=' '.join(q[1] for q in questions),
            totalMarks=total, topicId=topic, conceptId=f'irish-listening-{suffix}', paperFileid=FILE, schemeFileid=SCHEME_FILE,
            paperPage=page, schemePage=pages[0], schemePages=pages, atlasQuestionId=key, reviewedAt=REVIEWED_AT, reviewedPaperPages=[page],
            taskRequirements=['Éist leis an taifeadadh oifigiúil.', 'Freagair gach mír atá priontáilte ar an gcárta.'],
            criteria=criteria,
            markingGuideNote='The listed responses and tariffs come from the 2014 SEC marking scheme; equivalent wording with the same meaning is accepted. '
                             'Each printed question is marked at its own published tariff (2, or 2 + 2 for two points). ' + LANGUAGE,
            audioMaterial=dict(audio, label=ref), sourceMaterial=source(f'Cluastuiscint {ref}', [page])))
    c = m['composition']
    for group, (form, instruction, topic, titles) in m['groups'].items():
        for letter, title in titles:
            cards.append(dict(
                id=f'irish-2014-hl-p1-composition-{group.lower()}-{letter}', year=2014, level='higher', paper=1, section='1',
                questionRef=f'2014 HL Paper 1 Ceapadóireacht {group}({letter})',
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
                                 'The 2014 scheme prints no separate reductions for a short attempt; its note on material that is not to the title '
                                 '(a pro-rata penalty on Ábhar and Gaeilge) is part of the Cumas Gaeilge guidance (scheme PDF 14). ' + COMPOSITION_REASONS[group],
                sourceMaterial=source(f'Ceapadóireacht {group}({letter})', [6, 7])))
    listening = [card for card in cards if '-listening-' in card['id']]
    composition = [card for card in cards if '-composition-' in card['id']]
    assert len(listening) == 8 and sum(len(card['criteria']) for card in listening) == 26
    assert sum(card['totalMarks'] for card in listening) == 60 and len(composition) == 9
    assert len({card['id'] for card in cards}) == len(cards) == 17
    for card in cards:
        assert sum(cr['maxMarks'] for cr in card['criteria']) == card['totalMarks'], card['id']
        for cr in card['criteria']:
            assert cr['guidance'] and all(not re.search('[-]', g) for g in cr['guidance']), (card['id'], cr['id'])
    sr = json.loads(SOURCE_REVIEW.read_text())
    review = dict(year=2014, level='higher', paperFileid=FILE + '.pdf', schemeFileid=SCHEME_FILE + '.pdf',
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
                  boundaries='8 listening segment cards carrying all 26 printed questions as separate criteria at 2 or 2 + 2 (60); '
                             '9 composition title routes at 100 each (choose one).')
    return dict(review=review, cards=cards)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    data = build()
    scheme_words_in(data)  # guidance carries the SEC's words only; question and task checks the paper's (irish_lifted.py)
    import fitz
    scheme = fitz.open(ROOT / f'paper-trail-corpus/markingschemes/2014/{SCHEME_FILE}.pdf')
    # The searchable scheme text the provenance checks read (as 2016–2020 and 2026 write their own).
    scheme_md = '# Gaeilge Ardleibhéal 2014 — SEC marking scheme (Páipéar 1 agus 2)\n\n' + '\n\n'.join(
        f'## PDF page {i + 1}\n\n' + p.get_text() for i, p in enumerate(scheme))
    outputs = {OUT: json.dumps(data, ensure_ascii=False, indent=2) + '\n',
               SCHEME_MD: '\n'.join(line.rstrip() for line in scheme_md.splitlines()).rstrip() + '\n'}
    for path, value in outputs.items():
        if args.check:
            assert path.exists() and path.read_text() == value, f'Stale output: {path}'
        else:
            path.write_text(value)
    print(f"Irish Higher 2014 Paper 1: {len(data['cards'])} reviewed cards ({data['review']['printedListeningQuestions']} printed listening questions); the archive remains incomplete.")


if __name__ == '__main__':
    main()
