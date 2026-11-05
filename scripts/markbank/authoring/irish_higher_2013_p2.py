#!/usr/bin/env python3
"""Reviewed 2013 Higher Paper 2 (Léamhthuiscint agus Litríocht): new cards, no legacy component.

Paper PDF 1–12 (page 2 a pointer to the instructions, 3 the Treoracha, 4–5 Léamhthuiscint A
"Steve Jobs: Fiontraí agus Fealsamh" with its questions, 6–7 Léamhthuiscint B "Raidió na Gaeltachta:
40 Bliain ar an Aer", 8 prose, 9 poetry with Mo ghrá-sa (idir lúibíní), 10 additional literature,
11 the poem Éiceolaí, 12 blank) and the Paper 2 pages of the combined LC001ALP000IV scheme (PDF 15–28,
plus 29 modified marking) reviewed on 2026-11-05. Counts are assertions, not corpus-completeness proof.

The reading cards follow the reviewed 2014–2026 Higher Paper 2 components: every printed reading
question is a whole card with one criterion per published part, and each published part is also a
practice card. 2013 prices its (a) parts in two ways: two points ordered 2 + 1 ("{3 mharc: 2 mharc+1
mharc}", "{3 mharc, 2 mharc +1 mharc }", A 1(a), 3(a), 5(a), B 4(a)) and a single "{3 mharc}" answer
(the rest; A 2(a) prints its own partial "{3-1 =2 mharc mura mbíonn ach rud amháin luaite.}"). B 2(b)(ii)
prices two groups "{2 mharc, 1 mharc+1 mharc}" independently, so each answer has a practice card of its
own (as 2015 B 2(b)(i)). A 6(b) prices two reasons for the candidate's view, each with an example,
"Fáth 1 + Sampla 1 = 6 mharc" and "Fáth 2 + Sampla 2 = 6 mharc", independently (each half a practice
card, as 2017 A 6(b)); B 6(b) prices the genre 2 and two of its traits with an example each, 5 + 5,
which count only with the genre named ("Gan an cinéal (genre) scríbhneoireachta ainmnithe i gceart, ní
ghlacfar leis an bhfreagra."), so it stays one part (as 2015 B 6(b)).

The literature is 2016's shape. 2A (Oisín i dTír na nÓg) and 2B (an optional folk tale) each print three
headings with "do rogha dhá cheann"; the scheme prints no supporting notes, only the rule "Dhá cheann le
freagairt-an ceann is fearr a mharcáil as 13 mharc agus an ceann eile a mharcáil as 12 mharc". Each is
one card carrying all three printed headings with the scheme's two Eolas marks (the better answer 13, the
other 12) and the shared Gaeilge 5 (coordinator-approved for 2014–2016: a printed choice priced as a
whole). 3A (Mo ghrá-sa (idir lúibíní)) prices Eolas 13 + 5 + 7 (1 + 4 + 2); 3B (an optional modern poem)
13 (3 + 10) + 5 (1 + 4) + 7 (1 + 4 + 2). Ceist 4A–4E print no text of their own in the scheme: the
Treoracha on PDF 27 price each as Eolas 35 and Gaeilge 5, assessed as a unit. 4F (Éiceolaí) prices Eolas
19 (2 + 17) + 8 + 8 (4 + 4). The scheme prints no Gaeilge band table for Ceisteanna 2–4; the general
grading table on PDF 28 ("Grádú Marcála sna Ceisteanna", after Ceist 4, naming no question) converts a
grade to a mark for every total. It is carried as printed and never read for rows: the judged totals it
alone could scale (3A(i) Eolas 13, 3B(i) "Cur síos air = 10 marc", 4F(i) "Léiriú ar an bpríomhthéama =
17 marc", 4F(ii) 8) stay one row each.

Glyph repair (read from the font of every span and the rendered page, not guessed): the reading answers'
list marks on PDF 16–21 are a Calibri-Bold glyph the text layer returns as U+2010 alone on its line and
the page draws as a dash bullet, read as "•" (as 2014's Calibri-Bold list mark); the SymbolMT bullets on
PDF 16 (U+F0B7) are read as "•". Every Calibri-Bold U+2010 and every symbol-font span is audited.
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
OUT = ROOT / 'components/MarkBank/cards/irish/higher-2013-p2-authored.json'
SOURCE_REVIEW = ROOT / 'scripts/markbank/authored/irish-higher-2013-p2-source-review.json'
REVIEWED_AT = '2026-11-05'
PAPER_SHA = '28d1bd2262fc363a8562095ceada01b151266d8ded4c7211d4dd3132c70715a4'
SCHEME_SHA = 'f45b87933de3652ddfbfe8044fb9b7367c58a6a55742316b6d6b2d311c8b1f4b'
DIRECTIVE = re.compile(r'rogha|roghna|Freagair|Luaigh|Ainmnigh|\bnó\b|dhá phointe|dhá rud|dhá bh|dhá dh|dhá ch|dhá fh|dhá th|'
                       r'ceann amháin|pointe amháin|\bdhá\b|an dá\b|amháin', re.I)
SOURCE_NOTE = 'Shown page-for-page from the official examination paper; swipe to move between pages.'
# Glyphs the text layer mis-decodes, keyed by (font, character) and read from the rendered page.
GLYPHS = {('Calibri-Bold', '‐'): '•', ('SymbolMT', ''): '•'}
GLYPH_AUDIT = {(16, 'Calibri-Bold', '‐'): 9, (17, 'Calibri-Bold', '‐'): 18, (18, 'Calibri-Bold', '‐'): 7,
               (19, 'Calibri-Bold', '‐'): 13, (20, 'Calibri-Bold', '‐'): 17, (21, 'Calibri-Bold', '‐'): 12,
               (3, 'SymbolMT', ''): 6, (16, 'SymbolMT', ''): 3, (29, 'SymbolMT', ''): 4}
# The examiner's score boxes inside the 6(b) panels ("F 1 + S 1 (6) =", "Léiriú: C (2) =", "Léiriú: T 1 + S 1 (5) ="); exact
# strings only.
FURNITURE = ('F 1 + S 1 (6) =', 'F 2 + S 2 (6) =', 'Léiriú: C (2) =', 'Léiriú: T 1 + S 1 (5) =', 'Léiriú: T 2 + S 2 (5) =')
# The examiner's marking-panel note that closes each prose answer: the boundary of the answer's own text.
PANEL = 'Nóta: Caithfidh an Scrúdaitheoir'
CHOOSE_TWO = 'Dhá cheann le freagairt-an ceann is fearr a mharcáil as 13 mharc agus an ceann eile a mharcáil as 12 mharc.'
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
                # The Calibri-Bold list mark stands alone on its line; it is never part of a word.
                assert '‐' not in out, (number, out)
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
    # including a deduction from the full tariff printed as "{3-1 =2 mharc …}" / "( 2- 1 mharc=1 mharc easnamhach)".
    values = re.findall(r'= ?(\d+) mh?arc', chunk) + re.findall(r'\((\d+) mh?arc\)', chunk)
    values += [int(a) - int(b) for a, b in re.findall(r'(?<![\d/])([1-9]) ?- ?([1-9])(?![\d/])', chunk) if int(a) == marks]
    return sorted({0, marks} | {int(v) for v in values if int(v) <= marks})


def material():
    import fitz
    paper_path = ROOT / f'paper-trail-corpus/exampapers/2013/{FILE}.pdf'
    scheme_path = ROOT / f'paper-trail-corpus/markingschemes/2013/{SCHEME_FILE}.pdf'
    assert hashlib.sha256(paper_path.read_bytes()).hexdigest() == PAPER_SHA, 'Paper changed: repeat visual review'
    assert hashlib.sha256(scheme_path.read_bytes()).hexdigest() == SCHEME_SHA, 'Scheme changed: repeat visual review'
    paper, doc = fitz.open(paper_path), fitz.open(scheme_path)
    texts = [clean(p.get_text()) for p in paper]
    s = Scheme(scheme_pages(doc), 15, 29)
    # The marking instructions, from their first rule (their heading "Treoracha do mharcáil na léamhthuisceana" is a title)
    # to Léamhthuiscint A's heading.
    general = s.chunk('Tá Ceist 1 – 5 ar cómharc', 'Léamhthuiscint A 1 (a)')[0]
    assert general.endswith('sa fhreagarleabhar.') and '7 marc ar gach ceann' in general, general[-60:]
    # (q, part, paper prompt, scheme anchor, marks, mode, printed tariff). Each passage ends where the examiner's totals line
    # for it begins ("Suimigh anois na marcanna agus léirigh mar seo iad. Ceist 1 A (50) =").
    passages = {
        'A': dict(title='Steve Jobs: Fiontraí agus Fealsamh', pages=[4, 5], topic='irish-3-0',
                  end='Suimigh anois na marcanna agus léirigh mar seo iad. Ceist 1 A (50) =', parts=[
            ('1', 'a', '(a) Luaigh dhá phointe eolais a thugann le fios go bhfuil déagóirí an lae inniu gafa go mór leis an nuatheicneolaíocht. (Alt 1)', '1 (a) Luaigh dhá phointe eolais a thugann le fios', 3, 'ordered', '{3 mharc: 2 mharc+1 mharc}'),
            ('1', 'bi', '(b) (i) Cén úsáid a bhaineann tuismitheoirí agus seantuismitheoirí as Skype? (Alt 1)', '(b) (i) Cén úsáid a bhaineann', 2, None, '{2mharc}'),
            ('1', 'bii', '(ii) Cad as ar fhás an dul chun cinn sa chumarsáid le tríocha bliain anuas? (Alt 1)', '(ii) Cad as ar fhás an dul chun cinn', 2, None, '{2 mharc}'),
            ('2', 'a', '(a) Cár baineadh úsáid as bogearraí an chomhlachta ríomhaireachta NeXT? (Alt 2)', '2 (a) Cár baineadh úsáid', 3, None, '{3-1 =2 mharc mura mbíonn ach rud amháin luaite.}'),
            ('2', 'bi', '(b) (i) Luaigh fáth amháin ar tugadh Athair na Réabhlóide Digití ar Jobs. (Alt 2)', '(b) (i) Luaigh fáth amháin ar tugadh', 2, None, '{2 mharc}'),
            ('2', 'bii', '(ii) Cén moladh a thug an tUachtarán Obama do Jobs ar lá a bháis? (Alt 2)', '(ii) Cén moladh a thug', 2, None, '{2mharc}'),
            ('3', 'a', '(a) Luaigh dhá phointe eolais faoina thuismitheoirí uchtála. (Alt 3)', '3 (a) Luaigh dhá phointe eolais faoina', 3, 'ordered', '{2 mharc +1mharc}'),
            ('3', 'bi', '(b) (i) Cad a dhéanadh an leaid óg agus a athair uchtála sa gharáiste? (Alt 3)', '3 (b) (i) Cad a dhéanadh', 2, None, '{2 mharc}'),
            ('3', 'bii', '(ii) Luaigh cúis amháin nach raibh Jobs sona ar scoil. (Alt 3)', '(ii) Luaigh cúis amháin nach raibh', 2, None, '{2 mharc}'),
            ('4', 'a', '(a) Luaigh pointe amháin eolais faoi stíl bhainistíochta Jobs. (Alt 4)', '4 (a) Luaigh pointe amháin eolais faoi stíl', 3, None, '{3 mharc}'),
            ('4', 'bi', '(b) (i) Cén fáth ar thionóil sé cruinniú gach maidin Luain? (Alt 4)', '(b) (i) Cén fáth ar thionóil', 2, None, '{2 mharc}'),
            # The scheme reprints this part "Cén fath ar thug Jobs óráidí?"; the card shows the paper's "fáth".
            ('4', 'bii', '(ii) Cén fáth ar thug Jobs óráidí? (Alt 4)', '(ii) Cén fath ar thug Jobs', 2, None, '{2 mharc}'),
            ('5', 'a', '(a) Cad iad na hábhair chainte a bhí ag Jobs in Ollscoil Stanford? (Alt 5)', '5 (a) Cad iad na hábhair chainte', 3, 'ordered', '{3 mharc, 2 mharc +1 mharc }'),
            ('5', 'bi', '(b) (i) Cén chomhairle a chuir sé ar na mic léinn in Ollscoil Stanford? (Alt 5)', '(b) (i) Cén chomhairle a chuir', 2, None, '{2 mharc}'),
            ('5', 'bii', '(ii) Cén dearcadh a bhí aige ar dhúshláin agus ar dheacrachtaí an tsaoil? (Alt 5)', '(ii) Cén dearcadh a bhí aige', 2, None, '{2 mharc}'),
            ('6', 'a', '(a) Aimsigh briathar saor san aimsir chaite in Alt 2 agus ainmfhocal sa ghinideach iolra in Alt 3.', '6 (a) Aimsigh briathar saor', 3, 'grammar', '( 3 mharc- 2 mharc + 1 mharc)'),
            ('6', 'b', '(b) Bunaithe ar an eolas sa sliocht thuas, an dtaitníonn Steve Jobs leat mar dhuine? Tabhair dhá fháth le do fhreagra. (Bíodh an freagra i d’fhocail féin. Is leor 60 focal.)',
             '(b) Bunaithe ar an eolas atá sa sliocht thuas', 12, 'reasons', 'An mharcáil = 6 mharc +6 mharc')]),
        'B': dict(title='Raidió na Gaeltachta: 40 Bliain ar an Aer', pages=[6, 7], topic='irish-3-1',
                  end='Suimigh anois na marcanna agus léirigh mar seo iad. Ceist 1 B (50) =', parts=[
            ('1', 'a', '(a) Cén fáth a raibh an bhliain 2012 an-speisialta do Raidió na Gaeltachta? (Alt 1)', '1 (a) Cén fáth a raibh an bhliain 2012', 3, None, '{3 mharc}'),
            ('1', 'bi', '(b) (i) Cén deis a thug an raidió áitiúil seo do mhuintir na Gaeltachta? (Alt 1)', '(b) (i) Cén deis a thug', 2, None, '{2 mharc}'),
            ('1', 'bii', '(ii) Luaigh ábhar amháin cainte a bhí ag an gcúigear craoltóirí ar an gclár speisialta. (Alt 1)', '(ii) Luaigh ábhar amháin cainte', 2, None, '{2 mharc}'),
            ('2', 'a', '(a) Tabhair pointe amháin eolais faoi cheantar Chonamara sular bunaíodh Raidió na Gaeltachta. (Alt 2)', '2 (a) Tabhair pointe amháin eolais faoi cheantar', 3, None, '{3 mharc}'),
            ('2', 'bi', '(b) (i) Luaigh rud amháin a bhí á lorg ag Gluaiseacht Chearta Sibhialta na Gaeltachta. (Alt 2)', '(b) (i) Luaigh rud amháin a bhí á lorg', 2, None, '{2 mharc}'),
            ('2', 'bii', '(ii) Cén dá dhream a raibh an raidió áitiúil Gaeilge le freastal orthu? (Alt 2)', '(ii) Cén dá dhream', 2, 'slots', '{2 mharc, 1 mharc+1 mharc}'),
            ('3', 'a', '(a) Luaigh deacracht amháin a bhí ag an tseirbhís agus í ag tosú. (Alt 3)', '3 (a) Luaigh deacracht amháin', 3, None, '{3 mharc}'),
            ('3', 'bi', '(b) (i) Luaigh pointe amháin eolais faoi bheoshruth Raidió na Gaeltachta. (Alt 3)', '(b) (i) Luaigh pointe amháin eolais faoi bheoshruth', 2, None, '{2 mharc}'),
            ('3', 'bii', '(ii) Cén t-athrú a tháinig ar uaireanta craolta Raidió na Gaeltachta ar an gcéad lá de Dheireadh Fómhair 2001? (Alt 3)', '(ii) Cén t-athrú a tháinig', 2, None, '{2 mharc}'),
            ('4', 'a', '(a) Luaigh dhá phointe eolais faoin tseirbhís nuachta a chuireann Raidió na Gaeltachta ar fáil. (Alt 4)', '4 (a) Luaigh dhá phointe eolais faoin tseirbhís', 3, 'ordered', '{3 mharc, 2 mharc+1 mharc}'),
            ('4', 'bi', '(b) (i) Cá bhfuil éisteoirí Raidió na Gaeltachta le fáil anois? (Alt 4)', '(b) (i) Cá bhfuil éisteoirí', 2, None, '{2 mharc}'),
            ('4', 'bii', '(ii) Luaigh gné amháin d’obair an stáisiúin a mhol an tUachtarán. (Alt 4)', '(ii) Luaigh gné amháin d’obair', 2, None, '{2 mharc}'),
            ('5', 'a', '(a) Cén fáth a mbeidh sé dian airgead a fháil leis an stáisiún a choimeád sa siúl? (Alt 5)', '5 (a) Cén fáth a mbeidh sé dian', 3, None, '{3 mharc}'),
            ('5', 'bi', '(b) (i) Tabhair píosa amháin eolais faoi úsáid an Bhéarla anois ar Raidió na Gaeltachta. (Alt 5)', '(b) (i) Tabhair píosa amháin eolais faoi úsáid', 2, None, '{2 mharc}'),
            ('5', 'bii', '(ii) Cá lorgófar airgead don stáisiún má ghearrtar siar ar an airgead poiblí? (Alt 5)', '(ii) Cá lorgófar airgead', 2, None, '{2 mharc}'),
            ('6', 'a', '(a) Aimsigh uimhir phearsanta in Alt 1 agus ainmfhocal firinscneach sa ghinideach uatha in Alt 3.', '6 (a) Aimsigh uimhir phearsanta', 3, 'grammar', '{3 mharc, 2 mharc+1 mharc}'),
            ('6', 'b', '(b) Cén cineál (genre) scríbhneoireachta lena mbaineann an sliocht seo? Luaigh dhá thréith a bhaineann leis an gcineál seo scríbhneoireachta. Aimsigh sampla amháin de gach ceann den dá thréith sin sa sliocht. (Bíodh an freagra i d’fhocail féin. Is leor 60 focal.)',
             '(b) Cén cineál (genre) scríbhneoireachta', 12, 'genre', 'Cineál (genre) scríbhneoireachta= 2 mharc')]),
    }
    start_b = s.text.index('Léamhthuiscint B 1 (a)')
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
            assert 'Ceist 1 A (50)' not in chunk and 'Léamhthuiscint B 1' not in chunk and 'NB: I gcás na gceisteanna' not in chunk, (letter, q, part)
            assert 'Suimigh' not in chunk and 'Páipéar II' not in chunk and 'Ceist 2 - PRÓS' not in chunk, (letter, q, part)
            assert '‐' not in chunk and not any(box in chunk for box in FURNITURE), (letter, q, part)
            resolved.append((q, part, prompt, anchor, marks, mode, chunk, spages))
        passage['resolved'] = resolved
    assert sum(len(p['resolved']) for p in passages.values()) == 34
    six_a = passages['A']['resolved'][-1][6]
    assert 'Fáth 1 + Sampla 1 = 6 mharc, Fáth 2 + Sampla 2 = 6 mharc,' in six_a and six_a.endswith('ní bhronnfar níos mó ná 3 mharc as 6 mharc ar an bhfreagra.)'), six_a[-200:]
    six_b = passages['B']['resolved'][-1][6]
    assert ('Cineál (genre) scríbhneoireachta= 2 mharc Tréith 1 + sampla as an sliocht = 5 mharc Tréith 2 + sampla as an sliocht = 5 mharc '
            'Gan an cinéal (genre) scríbhneoireachta ainmnithe i gceart, ní ghlacfar leis an bhfreagra.') in six_b, six_b[-400:]
    assert six_b.endswith('• píosa iriseoireachta • insint / cur síos ar…'), six_b[-80:]
    note5 = s.chunk('NB: I gcás na gceisteanna 2 (Prós)', 'Freagair Ceist 2A (Prós Ainmnithe) nó Ceist 2B (Prós Roghnach).')[0]
    # PDF 28: the general grading instruction and the grade-to-mark table for every total (the scheme's only grading
    # for Ceisteanna 2–4; it prints no literature band table this year). It is printed after Ceist 4 and names no question.
    grading = s.chunk('Grádú Marcála sna Ceisteanna', '⟦29⟧', s.page(28))[0]
    general4 = s.chunk('Treoracha : Iarrtar ar na hiarrthóirí plé a dhéanamh ar an ráiteas', 'Eolas (35) = Gaeilge (5) =', s.page(27))[0]
    assert note5.endswith('agus 5 ar Ghaeilge.') and '25 ar Eolas agus 5 ar Ghaeilge' in note5, note5[-80:]
    assert grading.endswith('D 7 7 6 6 5 5 4 4 4 3 3 2') and 'GRÁD 200 160 100' in grading and 'ansin cinneadh ar an marc.' in grading
    assert '(Féach an scéim ghrádaithe sa Cheapadóireacht ar lch. eile.)' in grading
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
          'reason-1': '(b) Fáth 1', 'reason-2': '(b) Fáth 2', 'genre': '(b) Cineál', 'trait-1': '(b) Tréith 1', 'trait-2': '(b) Tréith 2'}
# The two independent 6-mark halves of A 6(b): (criterion id prefix, label, English practice focus).
HALVES = {'reasons': ('reason', 'Fáth', 'One of the two reasons for your view of Steve Jobs as a person, with an example from the passage, in your own words (reason {slot}, 6 marks)')}
# The ordered two-point (a) parts: 0, the first point 2, both 3, and A 3(a)'s printed deficient answer at 1.
ORDERED = {('A', '1'): [0, 2, 3], ('A', '3'): [0, 1, 2, 3], ('A', '5'): [0, 2, 3], ('B', '4'): [0, 2, 3]}


def part_criteria(letter, q, part, marks, mode, chunk, general):
    if mode in HALVES:
        key, label, _ = HALVES[mode]
        return [criterion(f'{key}-1', f'{label} 1', 6, [chunk, general]), criterion(f'{key}-2', f'{label} 2', 6, [chunk, general])]
    if mode == 'genre':
        # "Cineál (genre) scríbhneoireachta= 2 mharc … Tréith 1 + sampla as an sliocht = 5 mharc … Tréith 2 …" (B 6(b)).
        return [criterion('genre', 'Cineál', 2, [chunk, general]), criterion('trait-1', 'Tréith 1', 5, [chunk]),
                criterion('trait-2', 'Tréith 2', 5, [chunk])]
    if mode == 'ordered':
        return [criterion(part, 'Freagra', marks, [chunk, general], permitted=ORDERED[(letter, q)])]
    if mode == 'grammar':
        return [criterion('grammar', 'Freagra', marks, [chunk, general], permitted=[0, 2, 3])]
    if mode == 'slots':
        # "{2 mharc, 1 mharc+1 mharc} • Na pobail Ghaeltachta (1 mharc) + Gaeilgeoirí (ar fud na tíre) (1 mharc)": either answer alone earns 1.
        return [criterion(part, 'Freagra', marks, [chunk, general], permitted=[0, 1, 2])]
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
            id=f'irish-2013-hl-p2-{slug}', year=2013, level='higher', paper=2, section='2',
            atlasQuestionId=key, questionRef=f'2013 HL Paper 2 {ref}', questionText=prompt,
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
    six_b = {'A': '6(b) prices two reasons for the candidate’s view of Steve Jobs, 6 marks each (a reason with an example from the passage), '
                  'in the candidate’s own words; a bare retelling of the text earns at most 3 of the 6.',
             'B': '6(b) is one response: the genre 2 and two of its traits with an example from the passage each, 5 + 5, in the candidate’s own '
                  'words; traits and examples are accepted only with the genre correctly named.'}
    slot_note = 'The scheme prices the two groups 1 mharc + 1 mharc independently; this card practises one of them. '
    for letter, passage in m['passages'].items():
        topic = passage['topic']
        source = (f'Léamhthuiscint {letter}', passage['title'], passage['pages'])
        by_question = {}
        for q, part, prompt, anchor, marks, mode, chunk, spages in passage['resolved']:
            label = f'{q}({part[0]})' + (f'({part[1:]})' if len(part) > 1 else '')
            text = f'{label} ' + re.sub(r'^(\([a-z]+\)\s*)+', '', prompt)
            here = 'irish-3-3' if mode == 'grammar' else topic
            card = add(f'R-{letter}-{q}-{part}', f'reading-{letter.lower()}-q{q}-{part}', f'Léamhthuiscint {letter} · Ceist {label}', text, here,
                       passage['pages'], spages, part_criteria(letter, q, part, marks, mode, chunk, m['general']), READING_REQUIREMENTS, PART_NOTE,
                       [topic] if mode == 'grammar' else None, source)
            by_question.setdefault(q, []).append((part, prompt, card))
            if mode in HALVES:
                key, half, focus = HALVES[mode]
                for slot in (1, 2):
                    add(f'R-{letter}-{q}-{part}-{slot}', f'reading-{letter.lower()}-q{q}-{part}-{slot}', f'Léamhthuiscint {letter} · Ceist {label} · {half} {slot}',
                        text, topic, passage['pages'], spages, [criterion(f'{key}-{slot}', f'{half} {slot}', 6, [chunk, m['general']])],
                        READING_REQUIREMENTS, 'The scheme prices the two reasons 6 + 6 independently; this card practises one of them. ' + PART_NOTE,
                        None, source, practiceFocus=focus.format(slot=slot))
            if mode == 'slots':
                for slot in (1, 2):
                    add(f'R-{letter}-{q}-{part}-{slot}', f'reading-{letter.lower()}-q{q}-{part}-{slot}', f'Léamhthuiscint {letter} · Ceist {label} · Freagra {slot}',
                        text, topic, passage['pages'], spages, [criterion(f'{part}-{slot}', f'Freagra {slot}', 1, [chunk, m['general']])],
                        READING_REQUIREMENTS, slot_note + PART_NOTE, None, source, practiceFocus=f'One of the two answers (answer {slot}, 1 mark)')
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
                   'table (PDF 28) converts a grade to a mark. A heading alone has no printed price, so the card is the whole question.')
    prose = [
        ('P-2A', 'prose-2a', 'Prós 2A · Oisín i dTír na nÓg', 'irish-4-1', '2A. Prós Ainmnithe Maidir leis an scéal béaloidis', 23,
         head2 + '\n2A. Prós Ainmnithe',
         'Maidir leis an scéal béaloidis Oisín i dTír na nÓg, déan plé gairid ar do rogha dhá cheann de na ceannteidil seo a leanas:\n'
         '(i) An pháirt a ghlacann Niamh Chinn Óir sa scéal.\n'
         '(ii) Cruachás Oisín ón uair a d’fhág sé Tír na nÓg.\n'
         '(iii) An tréith bhéaloidis is mó a thaitníonn leat sa scéal. (Tabhair dhá fháth le do fhreagra.) (30 marc)'),
        ('P-2B', 'prose-2b', 'Prós 2B · Scéal béaloidis roghnach', 'irish-4-7', '2B. Prós Roghnach Níl cead', 23,
         head2 + '\n2B. Prós Roghnach\nNíl cead aon ábhar a bhaineann le Prós Ainmnithe a úsáid i bhfreagra ar an bPrós Roghnach.',
         'Maidir le scéal béaloidis roghnach a ndearna tú staidéar air le linn do chúrsa, déan plé gairid ar do rogha dhá cheann de na ceannteidil seo a leanas:\n'
         '(i) Saol an phríomhcharachtair (na príomhphearsan) sa scéal.\n'
         '(ii) Críoch an scéil.\n'
         '(iii) An tréith bhéaloidis is mó a thaitníonn leat sa scéal. (Tabhair dhá fháth le do fhreagra.)\n'
         'Ní mór teideal an scéil bhéaloidis sin a scríobh síos go cruinn. (30 marc)'),
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
        ('F-3A', 'poetry-3a', 'Filíocht 3A · Mo ghrá-sa (idir lúibíní)', 'irish-5-4', '3A. Filíocht Ainmnithe (i)', 24, head3 + '\n3A. Filíocht Ainmnithe', [
            '(i) “Tugann an file cur síos éifeachtach greannmhar dúinn ar an bhfear sa dán Mo ghrá-sa (idir lúibíní) (thíos).” É sin a phlé. (15 mharc)',
            '(ii) Cén éifeacht a bhaineann le húsáid lúibíní sa dán seo? (Is leor pointe amháin eolais.) (6 mharc)',
            '(iii) Cé a chum an dán seo? Scríobh nóta gairid ar shaol agus ar shaothar an fhile. (9 marc)'],
         ['(ii) Cén éifeacht a bhaineann le húsáid lúibíní', '(iii) Cé a chum an dán seo?'],
         ['( Eolas = 13 mharc)', 'Pointe amháin eolais a mharcáil as 5 mharc', 'Saothar an fhile = 2 mharc'], [9]),
        ('F-3B', 'poetry-3b', 'Filíocht 3B · Dán nua-aimseartha roghnach', 'irish-5-6', '3B. Filíocht Roghnach Níl cead', 24,
         head3 + '\n3B. Filíocht Roghnach\nNíl cead aon ábhar a bhaineann le Filíocht Ainmnithe a úsáid i bhfreagra ar an bhFilíocht Roghnach.', [
            '(i) Maidir le dán nua-aimseartha roghnach a ndearna tú staidéar air le linn do chúrsa, cad é príomhthéama an dáin? Déan cur síos ar an gcaoi a gcuirtear an príomhthéama in iúl dúinn. (15 mharc)',
            '(ii) Cad é an mothú is láidre sa dán, dar leat? Luaigh fáth amháin le do fhreagra. (6 mharc)',
            '(iii) Cé a chum an dán seo? Scríobh nóta gairid ar shaol agus ar shaothar an fhile. (9 marc)'],
         ['(ii) Cad é an mothú is láidre sa dán', '(iii) Cé a chum an dán seo?'],
         ['Cur síos air = 10 marc', 'Fáth = 4 mharc', 'Saothar an fhile = 2 mharc'], [9]),
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
         '4A. An Triail\nDéan plé ar an bpáirt a ghlacann Pádraig Mac Cárthaigh sa dráma An Triail agus ar an tionchar atá aige ar shaol Mháire Ní Chathasaigh. (40 marc)'),
        ('X-4B', 'literature-4-b', '4B. A Thig Ná Tit Orm', 'irish-6-1',
         '4B. A Thig Ná Tit Orm\n“Faighimid léiriú suimiúil ar chúrsaí scoile agus ar chaitheamh aimsire sa Ghaeltacht nuair a bhí an t-údar ag fás aníos ann.”\n'
         'Déan plé ar an ráiteas sin. (40 marc)'),
        ('X-4C', 'literature-4-c', '4C. Tóraíocht Dhiarmada agus Ghráinne', 'irish-6-2',
         '4C. Tóraíocht Dhiarmada agus Ghráinne\n“Tá sárléiriú le fáil sa Tóraíocht ar thréithe agus ar iompar Fhinn Mhic Cumhaill.”\n'
         'Déan plé ar an ráiteas sin. (40 marc)'),
        ('X-4D', 'literature-4-d', '4D. Gafa', 'irish-6-3',
         '4D. Gafa\n“Tugtar léargas éifeachtach dúinn ar fhulaingt na máthar, Eithne, sa sliocht as an úrscéal Gafa.”\n'
         'Déan plé ar an ráiteas sin. (40 marc)'),
        ('X-4E', 'literature-4-e', '4E. Canary Wharf', 'irish-6-4',
         '4E. Canary Wharf\n“Tá léiriú éifeachtach ar iompar agus ar mheon Ultain sa scéal Saineolaí Teicneolaí.”\n'
         'Déan plé ar an ráiteas sin. (40 marc)'),
    ]
    for key, slug, ref, topic, prompt in options:
        assert all(in_order(line, texts[9]) for line in prompt.splitlines()), key
        # The scheme reprints each question on PDF 26 and prints no text of its own for 4A–4E: the Treoracha (PDF 27) price each
        # as Eolas 35 assessed as a unit.
        assert in_order(prompt.splitlines()[1], s.chunk(ref, None, s.page(26))[0][:600]), key
        add(key, slug, f'Litríocht {ref}', head4 + '\n\n' + prompt, topic, [10], [26, 27, 28],
            [criterion('eolas', 'Eolas', 35, [m['general4'], m['grading']], 'indicative'), gaeilge()], LIT_REQUIREMENTS,
            'One complete SEC response: Eolas 35 assessed as a unit with a single shared 5-mark Gaeilge award. The 2013 scheme prints no notes for '
            '4A–4E beyond the Treoracha for Ceist 4; its general grading table (PDF 28) converts a grade to a mark.')
    whole, spages = s.chunk('Ceist 4F-Dánta Breise-Éiceolaí', 'Eolas (35) =', s.page(27))
    pieces = split_parts(whole, ['(ii) A bhfuil i gceist leis na línte ón dán a mhíniú', '(iii) Dhá fháth'],
                         ['Léiriú ar an bpríomhthéama = 17 marc', 'a mhíniú = 8 marc', 'Fáth 2 = 4 mharc'])
    pieces[0] = re.sub(r'^Ceist 4F-Dánta Breise-Éiceolaí\s*', '', pieces[0])
    assert pieces[0].startswith('(i) Príomhthéama an dáin = 2 mharc'), pieces[0][:60]
    assert pieces[2].endswith('Ní mór don scrúdaitheoir an mionbhriseadh marcanna a léiriú sa fhreagarleabhar.'), pieces[2][-80:]
    f_prompt = ('4F. Dánta Breise – Éiceolaí\nFreagair (i), (ii) agus (iii) thíos.\n'
                '(i) Cad é príomhthéama an dáin Éiceolaí (thall), dar leat? Déan plé gairid ar an gcaoi a ndéantar léiriú ar an bpríomhthéama sin ó thús deireadh an dáin. '
                '(Pléigh dhá theicníc fhileata, ar a laghad, i do fhreagra.) (20 marc)\n'
                '(ii) A bhfuil i gceist leis na línte seo a mhíniú:\nCuirim feochadáin chuici ar an ngaoth.\n'
                'Téann mo sheilidí de sciuird oíche ag ithe a cuid leitíse.\nSíneann na driseacha agamsa a gcosa faoin bhfál.\n'
                'Is ar an bhféar aici siúd a dhéanann mo chaorthainnse\ncuileanna glasa a thál. (10 marc)\n'
                '(iii) An teideal oiriúnach ar an dán é “Éiceolaí”, dar leat? Tabhair dhá fháth le do fhreagra. (10 marc)')
    assert all(in_order(line, texts[9]) for line in f_prompt.splitlines())
    add('X-4F', 'literature-4-f', 'Litríocht 4F · Dánta Breise – Éiceolaí', head4 + '\n\n' + f_prompt, 'irish-6-10', [10, 11],
        sorted(set(spages) | {26, 28}),
        [criterion('eolas-i', '(i) Eolas', 19, [pieces[0], m['grading']], 'indicative'), criterion('eolas-ii', '(ii) Eolas', 8, [pieces[1]], 'indicative'),
         criterion('eolas-iii', '(iii) Eolas', 8, [pieces[2]], 'indicative'), gaeilge()], LIT_REQUIREMENTS,
        'One complete SEC response: the paper prints (i) 20, (ii) 10 and (iii) 10; the scheme assesses Eolas 19 (2 + 17), 8 and 8 (4 + 4) '
        'plus one shared 5-mark Gaeilge award. Supporting notes are indicative rather than exhaustive.',
        source=('Dánta Breise', 'Éiceolaí', [10, 11]))

    reading = [c for c in cards if '-reading-' in c['id']]
    literature = [c for c in cards if '-reading-' not in c['id']]
    assert len(reading) == 50 and len(literature) == 10, (len(reading), len(literature))
    assert len({c['id'] for c in cards}) == len(cards) == 60 and len({c['atlasQuestionId'] for c in cards}) == 60
    assert sum(c['totalMarks'] for c in cards if re.fullmatch(r'R-[AB]-\d', c['atlasQuestionId'])) == 100
    for card in cards:
        assert sum(c['maxMarks'] for c in card['criteria']) == card['totalMarks'], card['id']
        for c in card['criteria']:
            assert c['guidance'] and all(not re.search('[-‐]', g) for g in c['guidance']), (card['id'], c['id'])
            assert all(h not in g for h in FURNITURE for g in c['guidance']), (card['id'], c['id'])
    sr = json.loads(SOURCE_REVIEW.read_text())
    whole = [c['id'] for c in reading if re.fullmatch(r'R-[AB]-\d', c['atlasQuestionId'])]
    review = dict(year=2013, level='higher', paperFileid=FILE + '.pdf', schemeFileid=SCHEME_FILE + '.pdf',
                  paperSha256=PAPER_SHA, schemeSha256=SCHEME_SHA,
                  reviewedPaperPages=list(range(1, 13)), reviewedSchemePages=sr['reviewedSchemePages'], schemeScope=sr['schemeScope'],
                  reviewDate=REVIEWED_AT, status='reviewed', fullPaperAndApplicableSchemeVisualSweep=True, selectionDecisions=m['decisions'],
                  readingWholeCardIds=whole, readingPracticeCardIds=[c['id'] for c in reading if c['id'] not in whole],
                  literatureRouteCardIds=[c['id'] for c in literature],
                  examStructure=dict(readingA=50, readingB=50, prose=30, poetry=30, additionalLiterature=40, total=200),
                  nonPoolDecisions=sr['nonPoolDecisions'], openIssues=[], caveats=sr['sourceFindings'],
                  boundaries='12 whole reading questions with 34 published parts, 2 six-mark A 6(b) reason slots and 2 one-mark B 2(b)(ii) answer slots; '
                             '2 prose (2A Oisín i dTír na nÓg, 2B an optional folk tale; each choose two of three headings), 2 poetry and 6 additional-literature routes.')
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
    print(f"Irish Higher 2013 Paper 2: {len(data['cards'])} reviewed reading and literature cards; the archive remains incomplete.")


if __name__ == '__main__':
    main()
