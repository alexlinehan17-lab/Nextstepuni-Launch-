#!/usr/bin/env python3
"""Reviewed 2014 Higher Paper 2 (Léamhthuiscint agus Litríocht): new cards, no legacy component.

Paper PDF 1–12 (page 2 a pointer to the instructions, 3 the Treoracha, 4–5 Léamhthuiscint A
"Nelson Mandela: Laoch ar Lár" with its questions, 6–7 Léamhthuiscint B "Súil Siar ar 2013", 8 prose,
9 poetry with An Spailpín Fánach, 10 additional literature, 11 the poem Fill Arís, 12 blank) and the
Paper 2 pages of the combined LC001ALP000IV scheme (PDF 16–30, plus 31 modified marking) reviewed on
2026-11-05. Counts are assertions, not corpus-completeness proof.

The reading cards follow the reviewed 2016–2026 Higher Paper 2 components: every printed reading
question is a whole card with one criterion per published part, each published part is also a
practice card, and the two 6-mark halves of each 6(b) (A: two traits, each named 2 + its example 4,
as 2023 A 6(b); B: two worries from Ailt 2 and 3, each named 2 + its cause 4) expose their own slots.
2014 prices its (a) parts in two ways: "{2 mharc + 1 mharc}" (two items, first correct 2 and the other
1: 0/2/3) and a single "{3 mharc}" answer with printed partials (2(a), 3(a), 5(a) in A; 4(a) in B).
No part is priced "1 mharc + 1 mharc", so there are no one-mark slots.

The literature is 2016's shape. 2A (Dís) and 2B (an optional short story) each print three headings
with "do rogha dhá cheann"; the scheme prints no supporting notes, only the rule "Dhá cheann le
freagairt - an ceann is fearr a mharcáil as 13 mharc agus an ceann eile a mharcáil as 12 mharc". Each is
one card carrying all three printed headings with the scheme's two Eolas marks (the better answer 13,
the other 12) and the shared Gaeilge 5 (coordinator-approved for 2016: a printed choice priced as a
whole). 3A (An Spailpín Fánach) prices Eolas 13 + 5 (1 + 4) + 7 (2 + 3 + 2); 3B (an optional poem from
before 1850) 13 (2 + 11) + 5 (1 + 4) + 7 (2 + 3 + 2). Ceist 4A–4E print no text of their own in the
scheme: the Treoracha on PDF 29 price each as Eolas 35 and Gaeilge 5, assessed as a unit. 4F (Fill
Arís) prices Eolas 19 (2 + 17) + 8 + 8 (4 + 4). The scheme prints no Gaeilge band table for Ceisteanna
2–4; the general grading table on PDF 30 ("Grádú Marcála sna Ceisteanna") converts a grade to a mark
for every total.

Glyph repair (read from the font of every span and the rendered page, not guessed): the reading
answers' list marks on PDF 17–22 are a Calibri-Bold glyph the text layer returns as U+0372 and the page
draws as a dash bullet, read as "•"; the 6(b) mark panels on PDF 19 and 23 print "►" as a
TimesNewRomanPSMT glyph returned as "Ź", read as "►". Every Calibri and symbol-font span is audited.
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
OUT = ROOT / 'components/MarkBank/cards/irish/higher-2014-p2-authored.json'
SOURCE_REVIEW = ROOT / 'scripts/markbank/authored/irish-higher-2014-p2-source-review.json'
REVIEWED_AT = '2026-11-05'
PAPER_SHA = '2d118c00cc0a63bc63873f43f943b041bd9d94030869ce69e51f8501bb004a36'
SCHEME_SHA = 'b7b4d9da51f4bbbbeffc853a5457b799c54fe4294e7f9d983a7ec9c355187a4a'
DIRECTIVE = re.compile(r'rogha|roghna|Freagair|Luaigh|Ainmnigh|\bnó\b|dhá phointe|dhá rud|dhá bh|dhá dh|dhá ch|dhá fh|dhá th|'
                       r'ceann amháin|pointe amháin|\bdhá\b|an dá\b|amháin', re.I)
SOURCE_NOTE = 'Shown page-for-page from the official examination paper; swipe to move between pages.'
# Glyphs the text layer mis-decodes, keyed by (font, character) and read from the rendered page.
GLYPHS = {('Calibri-Bold', 'Ͳ'): '•', ('TimesNewRomanPSMT', 'Ź'): '►', ('SymbolMT', 'x'): '•'}
GLYPH_AUDIT = {(17, 'Calibri-Bold', 'Ͳ'): 15, (18, 'Calibri-Bold', 'Ͳ'): 20, (19, 'Calibri-Bold', 'Ͳ'): 10,
               (20, 'Calibri-Bold', 'Ͳ'): 11, (21, 'Calibri-Bold', 'Ͳ'): 14, (22, 'Calibri-Bold', 'Ͳ'): 8,
               (19, 'TimesNewRomanPSMT', 'Ź'): 2, (23, 'TimesNewRomanPSMT', 'Ź'): 2,
               (3, 'SymbolMT', 'u'): 6, (14, 'SymbolMT', 'x'): 11, (31, 'SymbolMT', 'x'): 4}
# The examiner's score boxes inside the 6(b) panels ("T (1) + S (1) =", "Á (2) + C (2) =") and the boxed page headings the
# text layer stores inside the literature pages; exact strings only.
FURNITURE = ('T (1) + S (1) =', 'T (2) + S (2) =', 'Á (1) + C (1) =', 'Á (2) + C (2) =')
# The examiner's marking-panel note that closes each prose answer: the boundary of the answer's own text.
PANEL = 'Nóta: Caithfidh an Scrúdaitheoir'
CHOOSE_TWO = 'Dhá cheann le freagairt - an ceann is fearr a mharcáil as 13 mharc agus an ceann eile a mharcáil as 12 mharc.'
POETRY_END = 'Ní mór don Scrúdaitheoir an marc ar eolas as 25 marc'


def clean(text):
    return re.sub(r'\s+', ' ', symbol_text(text)).strip()


def unbox(text):
    for box in FURNITURE:
        text = text.replace(box, ' ')
    return clean(text)


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


def scheme_pages(doc):
    """Each scheme page's text with the audited glyph repairs applied, span by span."""
    audit = collections.Counter()
    pages = []
    for number, page in enumerate(doc, 1):
        lines = []
        for block in page.get_text('rawdict')['blocks']:
            for line in block.get('lines', []):
                out = ''
                for span in line['spans']:
                    for char in span['chars']:
                        if span['font'].startswith('Symbol') or (span['font'], char['c']) in GLYPHS:
                            audit[(number, span['font'], char['c'])] += 1
                        out += GLYPHS.get((span['font'], char['c']), char['c'])
                lines.append(out)
        pages.append('\n'.join(lines))
    assert dict(audit) == GLYPH_AUDIT, ('Symbol glyphs changed: repeat the glyph review', dict(audit))
    return pages


class Scheme:
    """Scheme pages joined with page markers so every chunk knows the PDF pages it spans."""

    def __init__(self, stext, first, last):
        self.text = ''
        for p in range(first, last + 1):
            self.text += f' ⟦{p}⟧ ' + re.sub(r'^\d+\s', '', clean(stext[p - 1]))

    def chunk(self, start, end=None, after=0):
        i = self.text.index(start, after)
        j = self.text.index(end, i + len(start)) if end else len(self.text)
        raw = self.text[i:j]
        pages = {int(re.findall(r'⟦(\d+)⟧', self.text[:i])[-1])}
        pages |= {int(m.group(1)) for m in re.finditer(r'⟦(\d+)⟧([^⟦]*)', raw) if clean(m.group(2)) not in ('', 'nó')}
        return unbox(re.sub(r'⟦\d+⟧', ' ', raw)), sorted(pages)

    def page(self, number):
        return self.text.index(f'⟦{number}⟧')


def printed_values(chunk, marks):
    # The marks a single-answer part can earn: 0, the full tariff and every partial the scheme prints for it,
    # including a deduction from the full tariff printed as "2-1 gan aon bhriathar" / "3-2 (easnamhach)".
    values = re.findall(r'= ?(\d+) mh?arc', chunk) + re.findall(r'bronntar (\d+) mh?arc', chunk) + re.findall(r'\((\d+) mh?arc\)', chunk)
    values += [int(a) - int(b) for a, b in re.findall(r'(?<![\d/])([1-9]) ?- ?([1-9])(?![\d/])', chunk) if int(a) == marks]
    return sorted({0, marks} | {int(v) for v in values if int(v) <= marks})


def material():
    import fitz
    paper_path = ROOT / f'paper-trail-corpus/exampapers/2014/{FILE}.pdf'
    scheme_path = ROOT / f'paper-trail-corpus/markingschemes/2014/{SCHEME_FILE}.pdf'
    assert hashlib.sha256(paper_path.read_bytes()).hexdigest() == PAPER_SHA, 'Paper changed: repeat visual review'
    assert hashlib.sha256(scheme_path.read_bytes()).hexdigest() == SCHEME_SHA, 'Scheme changed: repeat visual review'
    paper, doc = fitz.open(paper_path), fitz.open(scheme_path)
    texts = [clean(p.get_text()) for p in paper]
    s = Scheme(scheme_pages(doc), 16, 31)
    # The marking instructions, from their first rule (their heading "Treoracha do mharcáil na léamhthuisceana" is a title)
    # to Léamhthuiscint A's heading.
    general = s.chunk('Tá Ceist 1 – 5 ar cómharc', 'Léamhthuiscint A - 50 marc')[0]
    assert general.endswith('sa fhreagarleabhar.'), general[-60:]
    # (q, part, paper prompt, scheme anchor, marks, mode, printed tariff). Each passage ends where the examiner's totals line
    # for it begins ("Ag bun Léamhthuiscint A, léirigh na marcanna mar seo :").
    passages = {
        'A': dict(title='Nelson Mandela: Laoch ar Lár', pages=[4, 5], topic='irish-3-0',
                  end='Ag bun Léamhthuiscint A, léirigh na marcanna', parts=[
            ('1', 'a', '(a) Cén fáth nárbh aon údar mór iontais é bás Nelson Mandela anuraidh? (Alt 1)', '1 (a) Cén fáth nárbh aon údar mór iontais', 3, 'ordered', '3 mharc: 2 mharc + 1 mharc'),
            ('1', 'bi', '(b) (i) Conas a scaipeadh scéal a bháis go tapa ar na meáin chumarsáide? (Alt 1)', '(b) (i) Conas a scaipeadh scéal a bháis', 2, None, '{2 mharc}'),
            ('1', 'bii', '(ii) Luaigh slí amháin ar tugadh moladh do Nelson Mandela i ndiaidh a bháis. (Alt 1)', '(ii) Luaigh slí amháin ar tugadh moladh', 2, None, '{2 mharc}'),
            ('2', 'a', '(a) Cén fáth ar tugadh an t-ainm ‘Nelson’ air nuair a chuaigh sé ar scoil? (Alt 2)', '2 (a) Cén fáth ar tugadh an t-ainm', 3, None, '{3 mharc}'),
            ('2', 'bi', '(b) (i) Cad a rinne Mandela agus a chara sa bhliain 1952? (Alt 2)', '(b) (i) Cad a rinne Mandela agus a chara', 2, None, '{2 mharc}'),
            ('2', 'bii', '(ii) Cén cosc a bhí i bhfeidhm faoi dhlíthe an Apartheid? (Alt 2)', '(ii) Cén cosc a bhí i bhfeidhm', 2, None, '{2 mharc}'),
            ('3', 'a', '(a) Cén fáth ar bunaíodh an African National Congress (ANC)? (Alt 3)', '3 (a) Cén fáth ar bunaíodh', 3, None, '{3 mharc}'),
            ('3', 'bi', '(b) (i) Luaigh pointe amháin eolais faoi shlad Sharpeville i 1960. (Alt 3)', '(b) (i) Luaigh pointe amháin eolais faoi shlad Sharpeville', 2, None, '{2 mharc}'),
            ('3', 'bii', '(ii) Luaigh pointe amháin eolais faoi phríosúnacht saoil Nelson Mandela. (Alt 3)', '(ii) Luaigh pointe amháin eolais faoi phríosúnacht', 2, None, '{2 mharc}'),
            ('4', 'a', '(a) Cén fáth ar chosúil go leanfadh córas an Apartheid go ceann i bhfad? (Luaigh dhá phointe eolais.) (Alt 4)', '4 (a) Cén fáth ar chosúil go leanfadh', 3, 'ordered', '{2 mharc + 1 mharc}'),
            ('4', 'bi', '(b) (i) Cad a rinne roinnt oibrithe óga de chuid Dunnes Stores sna hochtóidí? (Alt 4)', '(b) (i) Cad a rinne roinnt oibrithe óga', 2, None, '{2 mharc}'),
            ('4', 'bii', '(ii) Cad a rinne F. W. de Klerk nuair a rinneadh Uachtarán de? (Alt 4)', '(ii) Cad a rinne F.W. de Klerk', 2, None, '{2 mharc}'),
            ('5', 'a', '(a) Cad a tharla ar 27 Aibreán 1994? (Alt 5)', '5 (a) Cad a tharla ar an 27 Aibreán 1994?', 3, None, '{3 mharc}'),
            ('5', 'bi', '(b) (i) Cén sprioc a chuir Nelson Mandela roimhe? (Alt 5)', '(b) (i) Cén sprioc a chuir Nelson Mandela', 2, None, '{2 mharc}'),
            ('5', 'bii', '(ii) Luaigh aidhm amháin atá le ‘Mandela Day’ ar 18 Iúil. (Alt 5)', '(ii) Luaigh aidhm amháin atá le', 2, None, '{2 mharc}'),
            ('6', 'a', '(a) Aimsigh sampla den Mhodh Coinníollach in Alt 3 agus sampla den bhriathar saor san Aimsir Chaite in Alt 4.', '6 (a) Aimsigh sampla den Mhodh Coinníollach', 3, 'grammar', '{ 2 mharc + 1 mharc}'),
            ('6', 'b', '(b) Bunaithe ar an eolas sa sliocht thuas, luaigh dhá thréith a bhain le Mandela, dar leat. Aimsigh sampla amháin de gach ceann den dá thréith sin sa sliocht. (Bíodh an freagra i d’fhocail féin. Is leor 60 focal.)',
             '(b) Bunaithe ar an eolas sa sliocht thuas', 12, 'traits', '{12 mharc}')]),
        'B': dict(title='Súil Siar ar 2013', pages=[6, 7], topic='irish-3-1',
                  end='Ag bun Léamhthuiscint B, léirigh na marcanna', parts=[
            ('1', 'a', '(a) Luaigh dhá shampla den phleanáil don todhchaí a dhéanfadh duine óg atá ag tosú amach ar aistear na beatha. (Alt 1)', '1 (a) Luaigh dhá shampla den phleanáil', 3, 'ordered', '{2 mharc + 1mharc}'),
            ('1', 'bi', '(b) (i) Cén t-ullmhú a rinne tú don scrúdú seo, dar leis an údar? (Alt 1)', '(b) (i) Cén t-ullmhú a rinne tú', 2, None, '{2 mharc}'),
            # The scheme reprints this part's paragraph as "(Alt 2)"; the card shows the paper's "(Alt 1)".
            ('1', 'bii', '(ii) Tabhair pointe amháin eolais faoi na heachtraí a tharla sa tréimhse idir 1912 agus 1922. (Alt 1)', '(ii) Tabhair pointe amháin eolais faoi na heachtraí', 2, None, '{2 mharc}'),
            ('2', 'a', '(a) Tabhair dhá phíosa eolais faoi Chomhrá 24/7. (Alt 2)', '2 (a) Tabhair dhá phíosa eolais faoi Chomhrá', 3, 'ordered', '{2 mharc + 1 mharc}'),
            ('2', 'bi', '(b) (i) Cad a rinne an spásaire, Chris Hadfield, i mí Feabhra? (Alt 2)', '(b) (i) Cad a rinne an spásaire', 2, None, '{2 mharc}'),
            ('2', 'bii', '(ii) Cén fáth ar fhógair an Coimisinéir Teanga go raibh sé chun éirí as a phost? (Alt 2)', '(ii) Cén fáth ar fhógair an Coimisinéir Teanga', 2, None, '{2 mharc}'),
            ('3', 'a', '(a) Luaigh dhá phointe eolais faoi obair na Triúrachta in Éirinn. (Alt 3)', '3 (a) Luaigh dhá phointe eolais faoi obair na Triúrachta', 3, 'ordered', '{2 mharc + 1 mharc}'),
            ('3', 'bi', '(b) (i) Cén fáth ar reáchtáil Fáilte Éireann an Tóstal in 2013? (Alt 3)', '(b) (i) Cén fáth ar reáchtáil Fáilte Éireann', 2, None, '{2 mharc}'),
            ('3', 'bii', '(ii) Cad ba chúis le hardú meanman mhuintir na hÉireann? (Alt 3)', '(ii) Cad ba chúis le hardú meanman', 2, None, '{2 mharc}'),
            ('4', 'a', '(a) Cén aidhm atá leis an gcomórtas LivCom? (Alt 4)', '4 (a) Cén aidhm atá leis an gcomórtas LivCom?', 3, None, '{3 mharc}'),
            ('4', 'bi', '(b) (i) Luaigh pointe amháin eolais faoin moladh a tugadh do phobal Inis Oírr ag an searmanas. (Alt 4)', '(b) (i) Luaigh pointe amháin eolais faoin moladh', 2, None, '{2 mharc}'),
            ('4', 'bii', '(ii) Luaigh cúis imní amháin atá ag muintir oileáin Árann faoi láthair. (Alt 4)', '(ii) Luaigh cúis imní amháin', 2, None, '{2 mharc}'),
            ('5', 'a', '(a) Luaigh difríocht amháin agus cosúlacht amháin idir saothar Seamus Heaney agus saothar Mhaidhc Dainín Uí Shé. (Alt 5)', '5 (a) Luaigh difríocht amháin agus cosúlacht amháin', 3, 'ordered', '{2 mharc + 1 mharc}'),
            ('5', 'bi', '(b) (i) Conas a chaith an tAthair Alec Reid cuid mhór dá shaol i dTuaisceart Éireann? (Alt 5)', '(b) (i) Conas a chaith an tAthair Alec Reid', 2, None, '{2 mharc}'),
            ('5', 'bii', '(ii) Cén íomhá atá le feiceáil sna grianghraif chlúiteacha den Athair Alec Reid? (Alt 5)', '(ii) Cén íomhá atá le feiceáil', 2, None, '{2 mharc}'),
            ('6', 'a', '(a) Aimsigh sampla d’ainmfhocal sa ghinideach iolra in Alt 1 agus sampla de bhriathar san Aimsir Fháistineach in Alt 3.', '6 (a) Aimsigh sampla d’ainmfhocal sa ghinideach iolra', 3, 'grammar', '{2 mharc + 1 mharc}'),
            ('6', 'b', '(b) Sna hailt 2 agus 3, déanann an t-údar cur síos ar rudaí éagsúla atá ag cur imní ar dhaoine áirithe. Scríobh síos dhá ábhar imní éagsúla a luaitear sna hailt sin agus cúis a luaitear le gach ceann de na hábhair imní sin. (Bíodh an freagra i d’fhocail féin. Is leor 60 focal.)',
             '(b) Sna hailt 2 agus 3, déanann an t-údar', 12, 'worries', 'Léirigh an mionbhriseadh marcanna mar seo a leanas:')]),
    }
    start_b = s.text.index('Léamhthuiscint B - 50 marc')
    for letter, passage in passages.items():
        page_text = ' '.join(texts[p - 1] for p in passage['pages'])
        anchors = [p[3] for p in passage['parts']]
        resolved = []
        pos = start_b if letter == 'B' else 0
        for index, (q, part, prompt, anchor, marks, mode, tariff) in enumerate(passage['parts']):
            assert in_order(prompt, page_text), (letter, q, part)
            # Anchors are searched forward from the previous part so repeated stems resolve in printed order.
            here = s.text.index(anchor, pos)
            assert letter == 'B' or here < start_b, (letter, q, part)
            chunk, spages = s.chunk(anchor, anchors[index + 1] if index + 1 < len(anchors) else passage['end'], pos)
            pos = here + 1
            assert tariff in chunk, (letter, q, part, chunk[:90])
            assert 'C1A (50)' not in chunk and 'Léamhthuiscint B - 50' not in chunk and 'NB: I gcás na gceisteanna' not in chunk, (letter, q, part)
            assert 'Ag bun Léamhthuiscint' not in chunk and 'Páipéar II' not in chunk and 'Ceist 2 - PRÓS' not in chunk, (letter, q, part)
            assert 'Ͳ' not in chunk and 'Ź' not in chunk, (letter, q, part)
            resolved.append((q, part, prompt, anchor, marks, mode, chunk, spages))
        passage['resolved'] = resolved
    assert sum(len(p['resolved']) for p in passages.values()) == 34
    six_a = passages['A']['resolved'][-1][6]
    assert 'Tréith 1 ( 2 mharc) + Sampla 1 ( 4 mharc) ► 6 mharc Tréith 2 ( 2 mharc) + Sampla 2 ( 4 mharc) ► 6 mharc' in six_a, six_a[:300]
    six_b = passages['B']['resolved'][-1][6]
    assert 'Ábhar imní 1 ( 2 mharc) + Cúis 1 ( 4 mharc) ► 6 mharc Ábhar imní 2 ( 2 mharc) + Cúis 2 ( 4 mharc) ► 6 mharc' in six_b, six_b[:300]
    note5 = s.chunk('NB: I gcás na gceisteanna 2 (Prós)', 'Freagair Ceist 2A (Prós Ainmnithe) nó Ceist 2B (Prós Roghnach).')[0]
    # PDF 30: the general grading instruction and the grade-to-mark table for every total (the scheme's only grading
    # for Ceisteanna 2–4; it prints no literature band table this year).
    grading = s.chunk('Grádú Marcála sna Ceisteanna', '⟦31⟧', s.page(30))[0]
    general4 = s.chunk('Treoracha : Iarrtar ar na hiarrthóirí plé a dhéanamh ar an ráiteas', 'Eolas (35) = Gaeilge (5) =', s.page(29))[0]
    assert note5.endswith('agus 5 ar Ghaeilge.') and '25 ar Eolas agus 5 ar Ghaeilge' in note5, note5[-80:]
    assert grading.endswith('D 7 7 6 6 5 5 4 4 4 3 3 2') and 'GRÁD 200 160 100' in grading and 'ansin cinneadh ar an marc.' in grading
    assert general4.endswith('sa fhreagarleabhar.') and 'an t-eolas a mharcáil as 35 marc agus an Ghaeilge san iarracht a mheas as 5 mharc' in general4
    return dict(paper=paper, texts=texts, s=s, general=general, passages=passages, note5=note5, grading=grading,
                general4=general4, decisions=selection_decisions(paper))


READING_REQUIREMENTS = ['Léigh an sliocht iomlán a ghabhann leis an gceist. Freagair an chuid atá luaite ar an gcárta.',
                        'Úsáid an t-alt a luaitear. Glacfar le focail an tsleachta nó le do chuid focal féin, ach ní mór 6(b) a fhreagairt i d’fhocail féin.']
WHOLE_REQUIREMENTS = ['Léigh an sliocht oifigiúil a ghabhann leis an gceist.', 'Freagair gach fochuid agus cloígh leis an alt a luaitear.',
                      'Bain úsáid as do chuid focal féin nuair a iarrtar ort é.']
LIT_REQUIREMENTS = ['Freagair gach cuid den cheist atá priontáilte.', 'Úsáid tagairtí cruinne agus ábhartha don téacs.']
PART_NOTE = ('SEC allocation for this task. Alternative correct answers in the scheme are answers to one task, not extra task routes. '
             'Whole questions and their practice parts are overlapping exercises; their marks are not added to infer the paper total.')
LABELS = {'a': '(a) Freagra', 'bi': '(b)(i) Freagra', 'bii': '(b)(ii) Freagra', 'grammar': '(a) Freagra',
          'trait-1': '(b) Tréith 1', 'trait-2': '(b) Tréith 2', 'worry-1': '(b) Ábhar imní 1', 'worry-2': '(b) Ábhar imní 2'}
# The two 6-mark halves of 6(b): (criterion id prefix, label, English practice focus).
HALVES = {'traits': ('trait', 'Tréith', 'One of the two traits of Mandela, with an example of it from the passage, in your own words (trait {slot}, 6 marks)'),
          'worries': ('worry', 'Ábhar imní', 'One of the two worries mentioned in Ailt 2 and 3, with the cause given for it, in your own words (worry {slot}, 6 marks)')}


def part_criteria(part, marks, mode, chunk, general):
    if mode in HALVES:
        key, label, _ = HALVES[mode]
        return [criterion(f'{key}-1', f'{label} 1', 6, [chunk, general]), criterion(f'{key}-2', f'{label} 2', 6, [chunk, general])]
    if mode in ('ordered', 'grammar'):
        # B 1(a) prints a one-mark penalty on its first answer ("pionós (-1 mharc) má fhágtar “romhat” sa fhreagra"), which reaches 1.
        penalty = [1] if 'pionós (-1 mharc)' in chunk else []
        return [criterion('grammar' if mode == 'grammar' else part, 'Freagra', marks, [chunk, general], permitted=sorted([0, 2, 3] + penalty))]
    return [criterion(part, 'Freagra', marks, [chunk, general], permitted=printed_values(chunk, marks))]


def split_parts(whole, cuts, caps):
    i2 = whole.index(cuts[0]); i3 = whole.index(cuts[1], i2)
    pieces = [whole[:i2].strip(), whole[i2:i3].strip(), whole[i3:].strip()]
    for piece, cap in zip(pieces, caps):
        assert cap in piece, cap
    return pieces


def build():
    m = material()
    texts, s = m['texts'], m['s']
    cards = []

    def add(key, slug, ref, prompt, topic, pages, scheme_pages, criteria, requirements, note, extra_topics=None, source=None, **extra):
        cards.append(dict(
            id=f'irish-2014-hl-p2-{slug}', year=2014, level='higher', paper=2, section='2',
            atlasQuestionId=key, questionRef=f'2014 HL Paper 2 {ref}', questionText=prompt,
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
    six_b = {'A': '6(b) prices two traits of Mandela, 6 marks each (naming the trait 2 + an example of it from the passage 4), in the candidate’s own words.',
             'B': '6(b) prices two worries from Ailt 2 and 3, 6 marks each (naming the worry 2 + the cause the passage gives for it 4), in the candidate’s own words.'}
    for letter, passage in m['passages'].items():
        topic = passage['topic']
        source = (f'Léamhthuiscint {letter}', passage['title'], passage['pages'])
        by_question = {}
        for q, part, prompt, anchor, marks, mode, chunk, spages in passage['resolved']:
            label = f'{q}({part[0]})' + (f'({part[1:]})' if len(part) > 1 else '')
            text = f'{label} ' + re.sub(r'^(\([a-z]+\)\s*)+', '', prompt)
            here = 'irish-3-3' if mode == 'grammar' else topic
            card = add(f'R-{letter}-{q}-{part}', f'reading-{letter.lower()}-q{q}-{part}', f'Léamhthuiscint {letter} · Ceist {label}', text, here,
                       passage['pages'], spages, part_criteria(part, marks, mode, chunk, m['general']), READING_REQUIREMENTS, PART_NOTE,
                       [topic] if mode == 'grammar' else None, source)
            by_question.setdefault(q, []).append((part, prompt, card))
            if mode in HALVES:
                key, half, focus = HALVES[mode]
                for slot in (1, 2):
                    add(f'R-{letter}-{q}-{part}-{slot}', f'reading-{letter.lower()}-q{q}-{part}-{slot}', f'Léamhthuiscint {letter} · Ceist {label} · {half} {slot}',
                        text, topic, passage['pages'], spages, [criterion(f'{key}-{slot}', f'{half} {slot}', 6, [chunk, m['general']])],
                        READING_REQUIREMENTS, 'The scheme prices the two halves 6 + 6 independently (named 2 + developed 4); this card practises one of them. ' + PART_NOTE,
                        None, source, practiceFocus=focus.format(slot=slot))
        for q, parts in by_question.items():
            crits = [dict(c) for _, _, card in parts for c in card['criteria']]
            for c in crits:
                c['label'] = LABELS[c['id']]
            add(f'R-{letter}-{q}', f'reading-{letter.lower()}-q{q}', f'Léamhthuiscint {letter} · Ceist {q}',
                f'{q}. ' + ' '.join(p for _, p, _ in parts) + (' (7 marc)' if q != '6' else ' (15 mharc)'), topic, passage['pages'],
                sorted({p for _, _, c in parts for p in c['schemePages']}), crits, WHOLE_REQUIREMENTS,
                'Complete printed question. Score each published part separately using these SEC allocations.'
                + (' Two-answer grammar is one 0/2/3 placement; ' + six_b[letter] if q == '6' else ''),
                ['irish-3-3'] if q == '6' else None, source)
            assert cards[-1]['totalMarks'] == (15 if q == '6' else 7), (letter, q)
            assert in_order(f'({7 if q != "6" else 15} m', texts[passage['pages'][1] - 1]), (letter, q)

    # ---- Ceisteanna 2–4: An Litríocht -------------------------------------------------------
    gaeilge = lambda: criterion('gaeilge', 'Gaeilge', 5, [m['note5'], m['grading']], 'quality')
    head2 = 'Freagair Ceist 2A (Prós Ainmnithe) nó Ceist 2B (Prós Roghnach) thíos.'
    head3 = 'Freagair Ceist 3A (Filíocht Ainmnithe) nó Ceist 3B (Filíocht Roghnach) thíos.'
    choose_note = ('One complete SEC response: two of the three printed headings answered. The scheme marks the better answer out of 13 and the other '
                   'out of 12 (Eolas 25), plus a single shared 5-mark Gaeilge award; it prints no supporting notes for this question, and its general grading '
                   'table (PDF 30) converts a grade to a mark. A heading alone has no printed price, so the card is the whole question.')
    prose = [
        ('P-2A', 'prose-2a', 'Prós 2A · Dís', 'irish-4-4', '2A. Prós Ainmnithe Maidir leis an ngearrscéal Dís', 24,
         head2 + '\n2A. Prós Ainmnithe',
         'Maidir leis an ngearrscéal Dís, déan plé gairid ar do rogha dhá cheann de na ceannteidil seo a leanas:\n'
         '(i) An léiriú a fhaighimid ar shaol bhean Sheáin sa ghearrscéal.\n'
         '(ii) An tábhacht a bhaineann leis an suirbhé in imeachtaí an ghearrscéil.\n'
         '(iii) An comhrá mar stíl inste sa ghearrscéal. (30 marc)'),
        ('P-2B', 'prose-2b', 'Prós 2B · Gearrscéal roghnach', 'irish-4-7', '2B. Prós Roghnach Níl cead', 24,
         head2 + '\n2B. Prós Roghnach\nNíl cead aon ábhar a bhaineann le Prós Ainmnithe a úsáid i bhfreagra ar an bPrós Roghnach.',
         'Maidir le gearrscéal roghnach a ndearna tú staidéar air le linn do chúrsa, déan plé gairid ar do rogha dhá cheann de na ceannteidil seo a leanas:\n'
         '(i) An fhorbairt a dhéantar ar an bpríomhthéama ó thús deireadh an ghearrscéil.\n'
         '(ii) An t-atmaisféar atá le brath sa ghearrscéal seo.\n'
         '(iii) An ghné is mó de stíl inste an ghearrscéil a chuaigh i bhfeidhm ort. (Tabhair dhá fháth le do fhreagra.)\n'
         'Ní mór teideal an ghearrscéil sin, mar aon le hainm an údair, a scríobh síos go cruinn. (30 marc)'),
    ]
    for key, slug, ref, topic, start, page, stem, prompt in prose:
        for line in [*stem.splitlines(), *prompt.splitlines()]:
            assert in_order(line, texts[7]), (key, line[:40])
        # The scheme reprints the question (on the card already); its own marking text is the choose-two rule after it.
        question, qpages = s.chunk(start, 'Dhá cheann le freagairt', s.page(page))
        assert all(in_order(re.sub(r'\s*\(30 marc\)$', '', line), question) for line in prompt.splitlines()[1:4]), (key, 'scheme reprint differs from the paper')
        rule, rpages = s.chunk('Dhá cheann le freagairt', PANEL, s.text.index(start, s.page(page)))
        assert rule == CHOOSE_TWO, (key, rule)
        add(key, slug, ref, prompt, topic, [8], sorted(set(qpages) | set(rpages)),
            [criterion('eolas-1', 'An ceann is fearr', 13, [rule, m['grading']], 'indicative'),
             criterion('eolas-2', 'An ceann eile', 12, [rule, m['grading']], 'indicative'), gaeilge()],
            LIT_REQUIREMENTS, choose_note, source=('Prós', ref.split(' · ', 1)[1], [8]), stem=stem)

    poems = [
        ('F-3A', 'poetry-3a', 'Filíocht 3A · An Spailpín Fánach', 'irish-5-1', '3A. Filíocht Ainmnithe (i)', 26, head3 + '\n3A. Filíocht Ainmnithe', [
            '(i) “Tugann an file cur síos éifeachtach dúinn ar shaol agus ar chás an spailpín sa dán An Spailpín Fánach (thíos).” É sin a phlé. (15 mharc)',
            '(ii) Cad é an mothúchán is mó sa dán seo, dar leat? (Is leor pointe amháin eolais as an dán mar thacaíocht le do fhreagra.) (6 mharc)',
            '(iii) Cén mheadaracht atá sa dán seo? Scríobh pointe amháin eolais faoin meadaracht seo agus léirigh do fhreagra le sampla cruinn ón dán. (9 marc)'],
         ['(ii) Cad é an mothúchán is mó sa dán seo', '(iii) Cén mheadaracht atá sa dán seo?'], ['( Eolas = 13 mharc)', '(5 mharc)', '(7 marc)'], [9]),
        ('F-3B', 'poetry-3b', 'Filíocht 3B · Dán seanaimseartha roghnach', 'irish-5-6', '3B. Filíocht Roghnach Níl cead', 27,
         head3 + '\n3B. Filíocht Roghnach\nNíl cead aon ábhar a bhaineann le Filíocht Ainmnithe a úsáid i bhfreagra ar an bhFilíocht Roghnach.', [
            '(i) Maidir le dán seanaimseartha roghnach (dán a cumadh sa tréimhse roimh 1850) a ndearna tú staidéar air le linn do chúrsa, cad é príomhthéama an dáin? Déan plé gairid ar an gcaoi a ndéantar forbairt ar an bpríomhthéama sin. (15 mharc)',
            '(ii) Cad é an mothúchán is mó sa dán seo, dar leat? (Is leor pointe amháin eolais as an dán mar thacaíocht le do fhreagra.) (6 mharc)',
            '(iii) Cén ghné den dán is mó a chuaigh i bhfeidhm ort? Scríobh dhá phointe eolais faoin ngné sin. (9 marc)',
            'Ní mór teideal an dáin sin, mar aon le hainm an fhile, a scríobh síos go cruinn.'],
         ['(ii) Cad é an mothúchán is mó sa dán seo', '(iii) Cén ghné den dán'], ['(13 mharc)', '(5 mharc)', '(7 marc)'], [9]),
    ]
    for key, slug, ref, topic, start, page, stem, parts, cuts, caps, paper_pages in poems:
        for line in [*stem.splitlines(), *parts]:
            assert in_order(line, texts[8]), (key, line[:40])
        whole, spages = s.chunk(start, POETRY_END, s.page(page))
        assert 'Eolas (25) =' not in whole and 'Gaeilge (5)' not in whole, key
        pieces = split_parts(whole, cuts, caps)
        add(key, slug, ref, '\n'.join(parts), topic, paper_pages, spages,
            [criterion('eolas-i', '(i) Eolas', 13, [pieces[0], m['grading']], 'indicative'), criterion('eolas-ii', '(ii) Eolas', 5, [pieces[1]], 'indicative'),
             criterion('eolas-iii', '(iii) Eolas', 7, [pieces[2]], 'indicative'), gaeilge()], LIT_REQUIREMENTS,
            'One complete SEC response with one shared five-mark Gaeilge award. The paper prints (i) 15, (ii) 6 and (iii) 9; the scheme assesses '
            'Eolas 13, 5 and 7 with the splits shown, plus Gaeilge 5 once. Supporting notes are indicative rather than exhaustive.',
            source=('Filíocht', ref.split(' · ', 1)[1], paper_pages), stem=stem)

    head4 = 'Freagair do rogha ceann amháin as Ceist 4 (A, B, C, D, E nó F) thíos.'
    options = [
        ('X-4A', 'literature-4-a', '4A. An Triail', 'irish-6-0',
         '4A. An Triail\n“Is spéisiúil an léiriú a dhéantar sa dráma An Triail ar an gcineál duine í Bean Uí Chathasaigh, máthair Mháire, agus ar an gcaoi a gcuireann sí leis an tragóid i saol Mháire.”\n'
         'Déan plé ar an ráiteas sin. (40 marc)'),
        ('X-4B', 'literature-4-b', '4B. A Thig Ná Tit Orm', 'irish-6-1',
         '4B. A Thig Ná Tit Orm\n“Cé go raibh an bochtanas thart timpeall ar Mhaidhc agus é ag fás aníos sa Ghaeltacht bhí spórt agus spraoi ann leis.”\n'
         'Déan plé ar an ráiteas sin. (40 marc)'),
        ('X-4C', 'literature-4-c', '4C. Tóraíocht Dhiarmada agus Ghráinne', 'irish-6-2',
         '4C. Tóraíocht Dhiarmada agus Ghráinne\n“Tugtar léiriú éifeachtach dúinn sa Tóraíocht ar thréithe Dhiarmada agus ar an bpáirt atá ag Diarmaid i bhforbairt an scéil.”\n'
         'Déan plé ar an ráiteas sin. (40 marc)'),
        ('X-4D', 'literature-4-d', '4D. Gafa', 'irish-6-3',
         '4D. Gafa\n“Sa sliocht as an úrscéal Gafa, tugtar léargas éifeachtach dúinn ar chás an déagóra Eoin, agus ar an gcaoi a gcuireann a iompar leis an teannas sa teaghlach.”\n'
         'Déan plé ar an ráiteas sin. (40 marc)'),
        ('X-4E', 'literature-4-e', '4E. Canary Wharf', 'irish-6-4',
         '4E. Canary Wharf\n“Tá cur síos éifeachtach ar aigne Éamoinn agus ar an tionchar a bhí ag caint Phrendergast agus Warrighe air sa scéal Canary Wharf.”\n'
         'Déan plé ar an ráiteas sin. (40 marc)'),
    ]
    for key, slug, ref, topic, prompt in options:
        assert all(in_order(line, texts[9]) for line in prompt.splitlines()), key
        # The scheme reprints each question on PDF 28 and prints no text of its own for 4A–4E: the Treoracha (PDF 29) price each
        # as Eolas 35 assessed as a unit.
        assert in_order(prompt.splitlines()[1], s.chunk(ref, None, s.page(28))[0][:600]), key
        add(key, slug, f'Litríocht {ref}', head4 + '\n\n' + prompt, topic, [10], [28, 29, 30],
            [criterion('eolas', 'Eolas', 35, [m['general4'], m['grading']], 'indicative'), gaeilge()], LIT_REQUIREMENTS,
            'One complete SEC response: Eolas 35 assessed as a unit with a single shared 5-mark Gaeilge award. The 2014 scheme prints no notes for '
            '4A–4E beyond the Treoracha for Ceist 4; its general grading table (PDF 30) converts a grade to a mark.')
    whole, spages = s.chunk('Ceist 4F-Dánta Breise-Fill Arís', 'Eolas (35) =', s.page(29))
    pieces = split_parts(whole, ['(ii) A bhfuil i gceist leis na línte ón dán a mhíniú', '(iii) Léargas ar an bhfile'],
                         ['Forbairt ar an bpríomhthéama = 17 marc', 'a mhíniú = 8 marc', 'Léargas ar an bhfile = 8 marc'])
    pieces[0] = re.sub(r'^Ceist 4F-Dánta Breise-Fill Arís\s*', '', pieces[0])
    assert pieces[0].startswith('(i) Príomhthéama an dáin = 2 mharc'), pieces[0][:60]
    f_prompt = ('4F. Dánta Breise – Fill Arís\nFreagair (i), (ii) agus (iii) thíos.\n'
                '(i) Cad é príomhthéama an dáin Fill Arís (thall), dar leat? Déan plé ar fhorbairt an phríomhthéama sin ó thús deireadh an dáin. (20 marc)\n'
                '(ii) A bhfuil i gceist leis na línte seo a mhíniú:\nDein d’fhaoistin is dein\nSíocháin led ghiniúin féinig\n'
                'Is led thigh-se féin is ná tréig iad,\nNí dual do neach a thigh ná a threabh a thréigean. (10 marc)\n'
                '(iii) Cén léargas a thugtar sa dán ar an bhfile a chum é, dar leat? Is leor dhá phointe eolais. Bíodh tagairtí cruinne agat do théacs an dáin i do fhreagra. (10 marc)')
    assert all(in_order(line, texts[9]) for line in f_prompt.splitlines())
    add('X-4F', 'literature-4-f', 'Litríocht 4F · Dánta Breise – Fill Arís', head4 + '\n\n' + f_prompt, 'irish-6-7', [10, 11],
        sorted(set(spages) | {28, 30}),
        [criterion('eolas-i', '(i) Eolas', 19, [pieces[0], m['grading']], 'indicative'), criterion('eolas-ii', '(ii) Eolas', 8, [pieces[1]], 'indicative'),
         criterion('eolas-iii', '(iii) Eolas', 8, [pieces[2]], 'indicative'), gaeilge()], LIT_REQUIREMENTS,
        'One complete SEC response: the paper prints (i) 20, (ii) 10 and (iii) 10; the scheme assesses Eolas 19 (2 + 17), 8 and 8 (4 + 4) '
        'plus one shared 5-mark Gaeilge award. Supporting notes are indicative rather than exhaustive.',
        source=('Dánta Breise', 'Fill Arís', [10, 11]))

    reading = [c for c in cards if '-reading-' in c['id']]
    literature = [c for c in cards if '-reading-' not in c['id']]
    assert len(reading) == 50 and len(literature) == 10, (len(reading), len(literature))
    assert len({c['id'] for c in cards}) == len(cards) == 60 and len({c['atlasQuestionId'] for c in cards}) == 60
    assert sum(c['totalMarks'] for c in cards if re.fullmatch(r'R-[AB]-\d', c['atlasQuestionId'])) == 100
    for card in cards:
        assert sum(c['maxMarks'] for c in card['criteria']) == card['totalMarks'], card['id']
        for c in card['criteria']:
            assert c['guidance'] and all(not re.search('[-ͲŹ]', g) for g in c['guidance']), (card['id'], c['id'])
            assert all(h not in g for h in FURNITURE for g in c['guidance']), (card['id'], c['id'])
    sr = json.loads(SOURCE_REVIEW.read_text())
    whole = [c['id'] for c in reading if re.fullmatch(r'R-[AB]-\d', c['atlasQuestionId'])]
    review = dict(year=2014, level='higher', paperFileid=FILE + '.pdf', schemeFileid=SCHEME_FILE + '.pdf',
                  paperSha256=PAPER_SHA, schemeSha256=SCHEME_SHA,
                  reviewedPaperPages=list(range(1, 13)), reviewedSchemePages=sr['reviewedSchemePages'], schemeScope=sr['schemeScope'],
                  reviewDate=REVIEWED_AT, status='reviewed', fullPaperAndApplicableSchemeVisualSweep=True, selectionDecisions=m['decisions'],
                  readingWholeCardIds=whole, readingPracticeCardIds=[c['id'] for c in reading if c['id'] not in whole],
                  literatureRouteCardIds=[c['id'] for c in literature],
                  examStructure=dict(readingA=50, readingB=50, prose=30, poetry=30, additionalLiterature=40, total=200),
                  nonPoolDecisions=sr['nonPoolDecisions'], openIssues=[], caveats=sr['sourceFindings'],
                  boundaries='12 whole reading questions with 34 published parts and 4 six-mark 6(b) slots; '
                             '2 prose (2A Dís, 2B an optional short story; each choose two of three headings), 2 poetry and 6 additional-literature routes.')
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
    print(f"Irish Higher 2014 Paper 2: {len(data['cards'])} reviewed reading and literature cards; the archive remains incomplete.")


if __name__ == '__main__':
    main()
