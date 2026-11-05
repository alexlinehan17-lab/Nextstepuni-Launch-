#!/usr/bin/env python3
"""Reviewed 2015 Higher Paper 2 (Léamhthuiscint agus Litríocht): new cards, no legacy component.

Paper PDF 1–12 (page 2 a pointer to the instructions, 3 the Treoracha, 4–7 the two reading
passages with their questions, 8 prose, 9 poetry with Colscaradh, 10 additional literature,
11 the poem Colmáin, 12 blank) and the Paper 2 pages of the combined LC001ALP000IV scheme
(PDF 16–29, the general grading table and modified marking on 29; 30–31 blank) reviewed on
2026-11-05. Counts are assertions, not corpus-completeness proof.

The reading cards follow the reviewed 2016–2026 Higher Paper 2 components: every printed
reading question is a whole card with one criterion per published part, each published part
is also a practice card, three independent one-mark pairs (A 1(b)(ii) and B 2(b)(i), priced
1 mharc + 1 mharc; A 5(b)(i), priced “{2 mharc} (2 phointe eolais) {1 mharc + 1 mharc}”)
expose their own slots, and order-dependent 2 + 1 items stay whole. Both 6(b) answers are the
2 + 5 + 5 shape of 2017 B 6(b): A an opinion 2 and two reasons with an example each (Cúis 2 +
Sampla 3), B the genre 2 and two traits with an example each (Tréith 2 + Sampla 3); the 5s
count only with the opinion or the genre, so each 6(b) stays one part.

2015's literature is 2018's shape: 2A prints two prescribed texts (the film Cáca Milis or the
play An Lasair Choille: a card each, as their Atlas headings differ) under one shared Treoir,
2B one optional film-or-play question (a card per alternative, as the scheme marks them differently:
the film Tréithe agus Léiriú 25, the play Príomhthéama 2 + Forbairt 23), one prescribed poem
(3A Colscaradh), one optional modern poem (3B) and six Q4 options (4F Colmáin); each is one
card with its printed sub-questions as criteria and one shared 5-mark Gaeilge award. The
scheme prints no band tables: each prose and poetry answer ends at the examiner's note “Ní mór
don Scrúdaitheoir an marc ar eolas as 25 marc …”, Q4A–E print nothing of their own (the Ceist 4
Treoracha price them, “an t-eolas a mharcáil as 35 marc”), and the one grading table, “Grádú
Marcála sna Ceisteanna” (PDF 29: grades A–D for every total from 200 to 5), is carried with
the 5-mark Gaeilge note on every literature card's Gaeilge criterion. Boxed headings are
removed by exact match.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import re
from pathlib import Path
from irish_lifted import scheme_words_in, symbol_text

ROOT = Path(__file__).resolve().parents[3]
FILE = 'LC001ALP200IV'
SCHEME_FILE = 'LC001ALP000IV'
OUT = ROOT / 'components/MarkBank/cards/irish/higher-2015-p2-authored.json'
SOURCE_REVIEW = ROOT / 'scripts/markbank/authored/irish-higher-2015-p2-source-review.json'
REVIEWED_AT = '2026-11-05'
PAPER_SHA = '98586d0bcbe2999a84c68f3c4463eedebb862a40a130cd5de8b8fd03825d3caa'
SCHEME_SHA = 'afb5cf50e6362a8d91a7d369fbac857375471192bab3fb53badbbc91c12e6fe1'
DIRECTIVE = re.compile(r'rogha|roghna|Freagair|Luaigh|Ainmnigh|\bnó\b|dhá phointe|dhá rud|dhá bh|dhá dh|dhá ch|dhá fh|dhá th|'
                       r'ceann amháin|pointe amháin|\bdhá\b|an dá\b|amháin', re.I)
SOURCE_NOTE = 'Shown page-for-page from the official examination paper; swipe to move between pages.'
# Boxed page headings the 2015 text layer stores inside the literature pages; exact strings only.
FURNITURE = ('– PRÓS AINMNITHE nó PRÓS ROGHNACH – (30 marc)', '– FILÍOCHT AINMNITHE nó FILÍOCHT ROGHNACH – (30 marc)',
             '– LITRÍOCHT BHREISE – (40 marc)')
# The examiner's marking-panel note that closes each prose and poetry answer: the boundary of the answer's own text.
PANEL = 'Ní mór don Scrúdaitheoir an marc ar eolas as 25 marc'


def clean(text):
    return re.sub(r'\s+', ' ', symbol_text(text)).strip()


def unbox(text):
    for heading in FURNITURE:
        text = text.replace(heading, ' ')
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


class Scheme:
    """Scheme pages joined with page markers so every chunk knows the PDF pages it spans."""

    def __init__(self, doc, first, last):
        self.text = ''
        for p in range(first, last + 1):
            self.text += f' ⟦{p}⟧ ' + re.sub(r'^\d+\s', '', clean(doc[p - 1].get_text()))

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
    # The marks a single-answer part can earn: 0, the full tariff and every partial the scheme prints for it.
    values = re.findall(r'= (\d+) mh?arc', chunk) + re.findall(r'bronntar (\d+) mh?arc', chunk) + re.findall(r'\((\d+) mh?arc\)', chunk)
    values += [int(a) - int(b) for a, b in re.findall(r'easnamhach \((\d+)-(\d+)\)', chunk)]
    return sorted({0, marks} | {int(v) for v in values if int(v) <= marks})


def material():
    import fitz
    paper_path = ROOT / f'paper-trail-corpus/exampapers/2015/{FILE}.pdf'
    scheme_path = ROOT / f'paper-trail-corpus/markingschemes/2015/{SCHEME_FILE}.pdf'
    assert hashlib.sha256(paper_path.read_bytes()).hexdigest() == PAPER_SHA, 'Paper changed: repeat visual review'
    assert hashlib.sha256(scheme_path.read_bytes()).hexdigest() == SCHEME_SHA, 'Scheme changed: repeat visual review'
    paper, doc = fitz.open(paper_path), fitz.open(scheme_path)
    texts = [clean(p.get_text()) for p in paper]
    assert texts[11].endswith('Leathanach Bán') and len(texts) == 12
    s = Scheme(doc, 16, 29)
    # The marking instructions, from their first rule (their heading "Treoracha do mharcáil na léamhthuisceana" is a title)
    # to the boxed section heading that the text layer stores after them.
    general = s.chunk('Tá Ceist 1 – 5 ar cómharc', 'Páipéar II (200 marc)')[0]
    assert general.endswith('sa fhreagarleabhar.'), general[-60:]
    # (q, part, paper prompt, scheme anchor, marks, mode, printed tariff). Each passage ends at the scheme's instruction
    # for its cover totals ("Ag bun Léamhthuiscint A/B, léirigh na marcanna mar seo: …").
    passages = {
        'A': dict(title='Cuir Comhairle ar an Óige', pages=[4, 5], topic='irish-3-0', end='Ag bun Léamhthuiscint A', parts=[
            ('1', 'a', '(a) Luaigh dhá phointe eolais faoi na ceannairí óga a bhailigh le chéile ag comhdháil OYW i mBaile Átha Cliath in 2014. (Alt 1)', '1. (a) Luaigh dhá phointe eolais faoi na ceannairí óga', 3, 'ordered', '{3 mharc: 2 mharc + 1 mharc}'),
            ('1', 'bi', '(b) (i) Cén deis a thugann an chomhdháil bhliantúil do na ceannairí óga? (Alt 1)', '(b) (i) Cén deis a thugann', 2, None, '{2 mharc}'),
            ('1', 'bii', '(ii) Scríobh síos dhá cheist dhomhanda a pléadh ag na comhdhálacha éagsúla. (Alt 1)', '(b) (ii) Scríobh síos dhá cheist dhomhanda', 2, 'slots', '{1 mharc + 1 mharc}'),
            ('2', 'a', '(a) Cad iad na hathruithe a chonaic Kate Robertson i ndiaidh ré an Apartheid san Afraic Theas? (Alt 2)', '2. (a) Cad iad na hathruithe a chonaic', 3, 'ordered', '{2 mharc + 1 mharc}'),
            ('2', 'bi', '(b) (i) Cad a chreideann Robertson agus Jones faoin aos óg? (Alt 2)', '(b) (i) Cad a chreideann Robertson', 2, None, '{2 mharc}'),
            ('2', 'bii', '(ii) Cén moladh a thugann David Jones do chuideachtaí? (Alt 2)', '(b) (ii) Cén moladh a thugann', 2, None, '{2 mharc}'),
            ('3', 'a', '(a) Ní mór do na hiarratasóirí critéir áirithe a shásamh le freastal ar chomhdháil OYW. Scríobh síos dhá cheann de na critéir sin. (Alt 3)', '3. (a) Ní mór do na hiarratasóirí', 3, 'ordered', '{2 mharc + 1 mharc}'),
            ('3', 'bi', '(b) (i) Luaigh rud amháin a dhéanann na Comhairleoirí ag na comhdhálacha. (Alt 3)', '(b) (i) Luaigh rud amháin a dhéanann', 2, None, '{2 mharc}'),
            ('3', 'bii', '(ii) Cad a d’impigh Mary Robinson ar na toscairí óga a dhéanamh? (Alt 3)', '(b) (ii) Cad a d’impigh Mary Robinson', 2, None, '{2 mharc}'),
            ('4', 'a', '(a) Cad a dhéanann Ambasadóirí de chuid OYW nuair a fhilleann siad abhaile i ndiaidh na gcomhdhálacha? (Alt 4)', '4. (a) Cad a dhéanann Ambasadóirí', 3, 'ordered', '{2 mharc + 1 mharc}'),
            # The scheme's reprint of 4(b)(i) reads "ata" (the paper: "atá").
            ('4', 'bi', '(b) (i) Cén socrú atá déanta ag an eagraíocht Foodcloud leis na hollmhargaí? (Alt 4)', '(b) (i) Cén socrú ata déanta', 2, None, '{2 mharc}'),
            ('4', 'bii', '(ii) Scríobh síos toradh amháin a bhíonn ar obair Foodcloud. (Alt 4)', '(b) (ii) Scríobh síos toradh amháin', 2, None, '{2 mharc}'),
            ('5', 'a', '(a) Luaigh dhá rud a dúirt Yeonmi Park faoin rialtas sa Chóiré Thuaidh le linn a hóige. (Alt 5)', '5. (a) Luaigh dhá rud a dúirt Yeonmi', 3, 'ordered', '{2 mharc + 1 mharc}'),
            ('5', 'bi', '(b) (i) Cad a léirigh na scannáin ón iarthar do mhuintir na Cóiré Thuaidh? (Alt 5)', '(b) (i) Cad a léirigh na scannáin', 2, 'slots', '{2 mharc} (2 phointe eolais) {1 mharc + 1 mharc}'),
            ('5', 'bii', '(ii) Cén rud a bhfuil Yeonmi ag súil leis? (Alt 5)', '(b) (ii) Cén rud a bhfuil Yeonmi', 2, None, '{2 mharc}'),
            ('6', 'a', '(a) Aimsigh sampla d’ainmfhocal firinscneach sa ghinideach uatha in Alt 1 agus sampla de bhriathar san Aimsir Láithreach in Alt 5.', '6. (a) Aimsigh sampla d’ainmfhocal firinscneach', 3, 'grammar', '{2 mharc + 1 mharc}'),
            ('6', 'b', '(b) Bunaithe ar an eolas sa sliocht thuas, an eagraíocht mhaith í an eagraíocht OYW, dar leat? Tabhair dhá chúis le do fhreagra agus bíodh sampla amháin as an sliocht mar thacaíocht le gach cúis a luann tú. (Bíodh an freagra i d’fhocail féin. Is leor 60 focal.)', '(b) Bunaithe ar an eolas sa sliocht thuas', 12, 'opinion',
             'Tuairim (2) ► 2 mharc T = Cúis 1 (2 mharc) + Sampla 1 (3 mharc) ► 5 mharc C (1) + S (1) = Cúis 2 (2 mharc) + Sampla 2 (3 mharc) ► 5 mharc C (2) + S (2) =')]),
        'B': dict(title='Cruachás na ndaoine gan dídean', pages=[6, 7], topic='irish-3-1', end='Ag bun Léamhthuiscint B', parts=[
            ('1', 'a', '(a) Tabhair dhá phointe eolais faoin gcéad Luan de mhí na Nollag. (Alt 1)', '1. (a) Tabhair dhá phointe eolais faoin gcéad Luan', 3, 'ordered', '{2 mharc + 1 mharc}'),
            ('1', 'bi', '(b) (i) Cad a dúradh sna tuairiscí faoi chruachás na ndaoine gan dídean in 2014? (Alt 1)', '(b) (i) Cad a dúradh sna tuairiscí', 2, None, '{2 mharc}'),
            # The scheme's reprint of 1(b)(ii) reads "tráchtáirí" and "(Alt1)" (the paper: "tráchtairí", "(Alt 1)").
            ('1', 'bii', '(ii) Cén fáth a raibh na tráchtairí ag rá go raibh feabhas ag teacht ar gheilleagar na tíre? (Alt 1)', '(b) (ii) Cén fáth a raibh na tráchtáirí', 2, None, '{2 mharc}'),
            ('2', 'a', '(a) Scríobh síos dhá phointe eolais a bhí le fáil sa suirbhé a rinneadh oíche an 11 Samhain. (Alt 2)', '2. (a) Scríobh síos dhá phointe eolais a bhí le fáil', 3, 'ordered', '{2 mharc + 1 mharc}'),
            ('2', 'bi', '(b) (i) Cé a bhí i láthair ag an gcruinniú speisialta a d’eagraigh an Rialtas? (Alt 2)', '(b) (i) Cé a bhí i láthair', 2, 'slots', '{1 mharc + 1 mharc}'),
            ('2', 'bii', '(ii) Cén gheallúint a thug an Rialtas ag an gcruinniú sin? (Alt 2)', '(b) (ii) Cén gheallúint', 2, None, '{2 mharc}'),
            ('3', 'a', '(a) Luaigh dhá rud a tharlaíonn uaireanta sa teaghlach agus a fhágann duine gan dídean. (Alt 3)', '3. (a) Luaigh dhá rud a tharlaíonn', 3, 'ordered', '{2 mharc + 1 mharc}'),
            ('3', 'bi', '(b) (i) Cén fáth a dtiteann saol duine as a chéile uaireanta nuair a bhíonn meabhairghalar air? (Alt 3)', '(b) (i) Cén fáth a dtiteann saol duine', 2, None, '{2 mharc}'),
            ('3', 'bii', '(ii) Cén fáth a bhfuil dídean éigeandála de dhíth anois ar theaghlaigh iomlána? (Alt 3)', '(b) (ii) Cén fáth a bhfuil dídean éigeandála', 2, None, '{2 mharc}'),
            ('4', 'a', '(a) Cabhraíonn eagraíochtaí carthanachta ar bhealaí praiticiúla le daoine gan dídean. Luaigh dhá cheann de na bealaí sin. (Alt 4)', '4. (a) Cabhraíonn eagraíochtaí carthanachta', 3, 'ordered', '{2 mharc + 1 mharc}'),
            ('4', 'bi', '(b) (i) Cén fáth ar bunaíodh an Peter McVerry Trust? (Alt 4)', '(b) (i) Cén fáth ar bunaíodh', 2, None, '{2 mharc}'),
            ('4', 'bii', '(ii) Luaigh rud amháin a deir an tAthair Peter McVerry faoi na hógánaigh. (Alt 4)', '(b) (ii) Luaigh rud amháin a deir', 2, None, '{2 mharc}'),
            ('5', 'a', '(a) Luaigh dhá bheartas atá i straitéis an Rialtais a foilsíodh sa bhliain 2013. (Alt 5)', '5. (a) Luaigh dhá bheartas', 3, 'ordered', '{2 mharc + 1 mharc}'),
            ('5', 'bi', '(b) (i) Faigheann daoine áirithe locht ar straitéis an Rialtais. Cad a mholann siad siúd? (Alt 5)', '(b) (i) Faigheann daoine áirithe locht', 2, None, '{2 mharc}'),
            ('5', 'bii', '(ii) Cén aidhm de chuid Fhorógra na Poblachta a luann an t-údar? (Alt 5)', '(b) (ii) Cén aidhm de chuid Fhorógra', 2, None, '{2 mharc}'),
            ('6', 'a', '(a) Aimsigh sampla den bhriathar saor san Aimsir Chaite in Alt 2 agus sampla den bhriathar saor san Aimsir Fháistineach in Alt 5.', '6. (a) Aimsigh sampla den bhriathar saor san Aimsir Chaite', 3, 'grammar', '{2 mharc + 1 mharc}'),
            ('6', 'b', '(b) Cén cineál (genre) scríbhneoireachta lena mbaineann an sliocht seo? Luaigh dhá thréith a bhaineann leis an gcineál seo scríbhneoireachta. Aimsigh sampla amháin de gach ceann den dá thréith sin sa sliocht. (Bíodh an freagra i d’fhocail féin. Is leor 60 focal.)', '(b) Cén cineál (genre) scríbhneoireachta', 12, 'genre',
             'Cineál (genre) scríbhneoireachta = 2 mharc C(2) = Tréith 1 (2 mharc) + Sampla 1 (3 mharc) ► 5 mharc T1 (2) + S1 (3) = Tréith 2 (2 mharc) + Sampla 2 (3 mharc) ► 5 mharc T2 (2) + S2 (3) =')]),
    }
    start_b = s.text.index('Léamhthuiscint B – 50 marc')
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
            assert 'Léamhthuiscint B –' not in chunk and 'Nóta: I gcás na gceisteanna' not in chunk, (letter, q, part)
            assert 'Ag bun Léamhthuiscint' not in chunk and 'Páipéar II' not in chunk and 'Ceist 2 PRÓS' not in chunk, (letter, q, part)
            resolved.append((q, part, prompt, anchor, marks, mode, chunk, spages))
        passage['resolved'] = resolved
    assert sum(len(p['resolved']) for p in passages.values()) == 34
    note5 = s.chunk('Nóta: I gcás na gceisteanna 2 (Prós)', 'Freagair Ceist 2A (Prós Ainmnithe) nó Ceist 2B (Prós Roghnach).')[0]
    # PDF 29: the general grading instruction and the grade-to-mark table for every total (the scheme's only grading
    # for Ceisteanna 2–4; it prints no literature band table this year), before the modified-marking (SMM) note.
    grading = s.chunk('Grádú Marcála sna Ceisteanna', 'Socruithe Réasúnta agus Scéim Mharcála Mhodhnaithe', s.page(29))[0]
    general4 = s.chunk('Treoracha : Iarrtar ar na hiarrthóirí plé a dhéanamh ar an ráiteas', 'Eolas (35) = Gaeilge (5) =', s.page(28))[0]
    assert note5.endswith('ar Ghaeilge.') and '25 ar Eolas agus 5 ar Ghaeilge' in note5
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
          'opinion': '(b) Tuairim', 'reason-1': '(b) Cúis 1', 'reason-2': '(b) Cúis 2',
          'genre': '(b) Cineál', 'trait-1': '(b) Tréith 1', 'trait-2': '(b) Tréith 2'}


def part_criteria(part, marks, mode, chunk, general):
    if mode == 'opinion':
        # "Tuairim (2) ► 2 mharc … Cúis 1 (2 mharc) + Sampla 1 (3 mharc) ► 5 mharc … Cúis 2 … ► 5 mharc" (A 6(b)).
        return [criterion('opinion', 'Tuairim', 2, [chunk, general]), criterion('reason-1', 'Cúis 1', 5, [chunk]),
                criterion('reason-2', 'Cúis 2', 5, [chunk])]
    if mode == 'genre':
        # "Cineál (genre) scríbhneoireachta = 2 mharc … Tréith 1 (2 mharc) + Sampla 1 (3 mharc) ► 5 mharc … Tréith 2 …" (B 6(b)).
        return [criterion('genre', 'Cineál', 2, [chunk, general]), criterion('trait-1', 'Tréith 1', 5, [chunk]),
                criterion('trait-2', 'Tréith 2', 5, [chunk])]
    if mode in ('ordered', 'grammar'):
        return [criterion('grammar' if mode == 'grammar' else part, 'Freagra', marks, [chunk, general], permitted=[0, 2, 3])]
    if mode == 'slots':
        # "{1 mharc + 1 mharc}" / "{2 mharc} (2 phointe eolais) {1 mharc + 1 mharc}": either answer alone earns 1.
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
            id=f'irish-2015-hl-p2-{slug}', year=2015, level='higher', paper=2, section='2',
            atlasQuestionId=key, questionRef=f'2015 HL Paper 2 {ref}', questionText=prompt,
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
    six_b = {'A': '6(b) is one response: the opinion 2 and two reasons with an example from the passage each, 5 + 5 (reason 2 + example 3), in the candidate’s own words; reasons and examples are accepted only with an opinion stated.',
             'B': '6(b) is one response: the genre 2 and two of its traits with an example from the passage each, 5 + 5 (trait 2 + example 3), in the candidate’s own words; traits and examples are accepted only with the genre correctly named.'}
    slot_notes = {('A', '1'): 'The scheme prices the two global issues 1 mharc + 1 mharc independently; this card practises one of them. ',
                  ('A', '5'): 'The scheme prices this part “{2 mharc} (2 phointe eolais) {1 mharc + 1 mharc}”: two points at 1 mark each; this card practises one of them. ',
                  ('B', '2'): 'The scheme prices the two groups 1 mharc + 1 mharc independently; this card practises one of them. '}
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
            if mode == 'slots':
                for slot in (1, 2):
                    add(f'R-{letter}-{q}-{part}-{slot}', f'reading-{letter.lower()}-q{q}-{part}-{slot}', f'Léamhthuiscint {letter} · Ceist {label} · Freagra {slot}',
                        text, topic, passage['pages'], spages, [criterion(f'{part}-{slot}', f'Freagra {slot}', 1, [chunk, m['general']])],
                        READING_REQUIREMENTS, slot_notes[(letter, q)] + PART_NOTE,
                        None, source, practiceFocus=f'One of the two answers (answer {slot}, 1 mark)')
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
    choice2a = 'Freagair an cheist thíos ar an scannán Cáca Milis nó ar an dráma An Lasair Choille.'
    stem2a = head2 + '\n2A. Prós Ainmnithe'
    # One Treoir after both prescribed questions prices them (PDF 24); its closing note is the only 25-mark price.
    treoir2a, tpages = s.chunk('Treoir: An ráiteas a phlé', 'Eolas (25) = Gaeilge (5) =', s.page(24))
    assert tpages == [24] and treoir2a.endswith('a thaispeáint sa fhreagarleabhar.') and PANEL in treoir2a
    prescribed = [
        # (key, slug, ref, topic, scheme reprint start, scheme reprint end, option as printed)
        ('P-2A-caca-milis', 'prose-2a-caca-milis', 'Prós 2A · Cáca Milis', 'irish-4-6', 'Cáca Milis “Ní duine deas', 'nó An Lasair Choille',
         'Cáca Milis\n“Ní duine deas í Catherine sa scannán Cáca Milis, rud atá soiléir ón gcaoi a gcaitheann sí le Paul agus iad ar an traein.”\nDéan plé ar an ráiteas sin. (30 marc)'),
        ('P-2A-an-lasair-choille', 'prose-2a-an-lasair-choille', 'Prós 2A · An Lasair Choille', 'irish-4-8', 'An Lasair Choille “Tugtar léargas', 'Treoir: An ráiteas a phlé',
         'An Lasair Choille\n“Tugtar léargas dúinn sa dráma An Lasair Choille ar chruachás Shéamais agus ar an tionchar a bhíonn ag Micil air.”\nDéan plé ar an ráiteas sin. (30 marc)'),
    ]
    prose_note = ('One complete SEC response: Eolas 25 and a single shared 5-mark Gaeilge award. The scheme prints one Treoir for both prescribed '
                  'texts and no supporting notes or band table; its general grading table (PDF 29) converts a grade to a mark.')
    for key, slug, ref, topic, qstart, qend, option in prescribed:
        prompt = choice2a + '\n\n' + option
        for line in [*stem2a.splitlines(), *prompt.splitlines()]:
            if line:
                assert in_order(line, texts[7]), (key, line)
        # The scheme reprints the question (on the card already); its marking text is the shared Treoir after both.
        question, qpages = s.chunk(qstart, qend, s.page(24))
        assert qpages == [24] and all(in_order(line, question) for line in option.splitlines()), (key, 'scheme reprint differs from the paper')
        add(key, slug, ref, prompt, topic, [8], [24, 29],
            [criterion('eolas', 'Eolas', 25, [treoir2a, m['grading']], 'indicative'), gaeilge()],
            LIT_REQUIREMENTS, prose_note, source=('Prós', ref.split(' · ', 1)[1], [8]), stem=stem2a)
    # 2B: the optional film and the optional play are two printed alternatives the scheme marks differently (the film
    # "Tréithe agus Léiriú (25)", the play "Príomhthéama (2) = Forbairt (23)"), so each is a card (coordinator ruling,
    # batch 6; BRIEF rule 5), both under the one optional-prose Atlas heading.
    stem2b = head2 + '\n2B. Prós Roghnach\nNíl cead aon ábhar a bhaineann le Prós Ainmnithe a úsáid i bhfreagra ar an bPrós Roghnach.'
    choice_line = 'Freagair an cheist thíos ar an scannán roghnach nó ar an dráma roghnach.'
    film_q = ('Maidir leis an scannán roghnach a ndearna tú staidéar air le linn do chúrsa, cad iad tréithe an phríomhcharachtair (na príomhphearsan) sa scannán? '
              'Déan plé ar an léiriú a dhéantar ar na tréithe sin ó thús deireadh an scannáin.\n'
              'Ní mór teideal an scannáin sin, mar aon le hainm an scríbhneora, a scríobh síos go cruinn. (30 marc)')
    play_q = ('Maidir leis an dráma roghnach a ndearna tú staidéar air le linn do chúrsa, cad é príomhthéama an dráma sin? '
              'Déan plé ar an bhforbairt a dhéantar ar an bpríomhthéama sin ó thús deireadh an dráma.\n'
              'Ní mór teideal an dráma sin, mar aon le hainm an scríbhneora, a scríobh síos go cruinn. (30 marc)')
    for line in [*stem2b.splitlines(), choice_line, *film_q.splitlines(), 'nó', *play_q.splitlines()]:
        if line:
            assert in_order(line, texts[7]), ('P-2B', line)
    # The scheme reprints each alternative (on the card already); its marking text is the panel and note after each:
    # the film "Tréithe agus Léiriú (25)" with its one-trait cap (PDF 24–25), the play "Príomhthéama (2) = Forbairt (23)",
    # then the examiner's note closing Ceist 2B ("… an marc ar eolas as 25 marc …"), which governs either alternative.
    question2b = s.chunk('2B. Prós Roghnach', 'Tréithe agus Léiriú (25)', s.page(24))[0] + ' ' + s.chunk('nó Maidir leis an dráma roghnach', 'Príomhthéama (2) =', s.page(25))[0]
    assert all(in_order(re.sub(r'\s*\(30 marc\)$', '', line), question2b) for line in [*film_q.splitlines(), *play_q.splitlines()]), 'P-2B scheme reprint differs from the paper'
    choice2b = s.chunk(choice_line, 'Maidir leis an scannán roghnach', s.page(24))[0]
    film, fpages = s.chunk('Tréithe agus Léiriú (25)', 'nó Maidir leis an dráma roghnach', s.page(24))
    play, ppages = s.chunk('Príomhthéama (2) = Forbairt (23)', 'Ní mór don Scrúdaitheoir an marc ar eolas', s.page(25))
    note2b, npages = s.chunk('Ní mór don Scrúdaitheoir an marc ar eolas', 'Eolas (25) = Gaeilge (5) =', s.page(25))
    assert choice2b == choice_line and fpages == [24, 25] and film.endswith('marcáil an t-eolas as 14 mharc.')
    assert ppages == [25] and play == 'Príomhthéama (2) = Forbairt (23) =', play
    assert npages == [25] and note2b.endswith('a thaispeáint sa fhreagarleabhar.')
    add('P-2B-scannan', 'prose-2b-scannan', 'Prós 2B · Scannán roghnach', choice_line + '\n\n' + film_q, 'irish-4-7', [8], [24, 25, 29],
        [criterion('eolas', 'Eolas', 25, [choice2b, film, note2b, m['grading']], 'indicative'), gaeilge()], LIT_REQUIREMENTS,
        'One complete SEC response: Eolas 25 and a single shared 5-mark Gaeilge award. The scheme prices the optional film as Tréithe agus '
        'Léiriú 25, with Eolas out of 14 where only one trait is discussed and illustrated; the play, the other printed alternative of 2B, '
        'is priced differently and has its own card. Its general grading table (PDF 29) converts a grade to a mark.',
        source=('Prós', 'Scannán roghnach', [8]), stem=stem2b)
    add('P-2B-drama', 'prose-2b-drama', 'Prós 2B · Dráma roghnach', choice_line + '\n\n' + play_q, 'irish-4-7', [8], [25, 29],
        [criterion('eolas', 'Eolas', 25, [choice2b, play, note2b, m['grading']], 'indicative'), gaeilge()], LIT_REQUIREMENTS,
        'One complete SEC response: Eolas 25 and a single shared 5-mark Gaeilge award. The scheme prices the optional play as Príomhthéama 2 '
        '+ Forbairt 23; the film, the other printed alternative of 2B, is priced differently and has its own card. Its general grading table '
        '(PDF 29) converts a grade to a mark.',
        source=('Prós', 'Dráma roghnach', [8]), stem=stem2b)

    poems = [
        ('F-3A', 'poetry-3a', 'Filíocht 3A · Colscaradh', 'irish-5-5', '3A. Filíocht Ainmnithe (i)', 26, head3 + '\n3A. Filíocht Ainmnithe', [
            '(i) “Tá codarsnacht idir dhá thuiscint dhifriúla ar an bpósadh sa dán Colscaradh (thíos).” É sin a phlé. (15 mharc)',
            '(ii) Cad é an mothúchán is mó a mhúsclaíonn an dán seo ionat féin? (Is leor pointe amháin eolais as an dán mar thacaíocht le do fhreagra.) (6 mharc)',
            '(iii) Cé a chum an dán seo? Scríobh nóta gairid ar shaol agus ar shaothar an fhile. (9 marc)']),
        ('F-3B', 'poetry-3b', 'Filíocht 3B · Dán nua-aimseartha roghnach', 'irish-5-6', '3B. Filíocht Roghnach Níl cead', 27,
         head3 + '\n3B. Filíocht Roghnach\nNíl cead aon ábhar a bhaineann le Filíocht Ainmnithe a úsáid i bhfreagra ar an bhFilíocht Roghnach.', [
            '(i) Maidir le dán nua-aimseartha roghnach a ndearna tú staidéar air le linn do chúrsa, cad é príomhthéama an dáin? Déan plé gairid ar fhorbairt an phríomhthéama sin ó thús deireadh an dáin. (15 mharc)',
            '(ii) Cad é an mothúchán is mó a mhúsclaíonn an dán seo ionat féin? (Is leor pointe amháin eolais as an dán mar thacaíocht le do fhreagra.) (6 mharc)',
            '(iii) Cé a chum an dán seo? Scríobh nóta gairid ar shaol agus ar shaothar an fhile. (9 marc)']),
    ]
    for key, slug, ref, topic, start, page, stem, parts in poems:
        for line in [*stem.splitlines(), *parts]:
            assert in_order(line, texts[8]), (key, line[:40])
        whole, spages = s.chunk(start, PANEL, s.page(page))
        assert spages == [page] and 'Eolas (25) =' not in whole and 'Gaeilge (5)' not in whole, key
        pieces = split_parts(whole, ['(ii) Cad é an mothúchán is mó', '(iii) Cé a chum an dán seo?'], ['Eolas = 13 mharc', 'Eolas = 5 mharc', 'Eolas = 7 marc'])
        add(key, slug, ref, '\n'.join(parts), topic, [9], [page, 29],
            [criterion('eolas-i', '(i) Eolas', 13, [pieces[0], m['grading']], 'indicative'), criterion('eolas-ii', '(ii) Eolas', 5, [pieces[1]], 'indicative'),
             criterion('eolas-iii', '(iii) Eolas', 7, [pieces[2]], 'indicative'), gaeilge()], LIT_REQUIREMENTS,
            'One complete SEC response with one shared five-mark Gaeilge award. The paper prints (i) 15, (ii) 6 and (iii) 9; the scheme assesses '
            'Eolas 13, 5 (1 + 4) and 7 (1 + 2 + 2 + 2) with the conditions shown, plus Gaeilge 5 once. Supporting notes are indicative rather than exhaustive.',
            source=('Filíocht', ref.split(' · ', 1)[1], [9]), stem=stem)

    head4 = 'Freagair do rogha ceann amháin as Ceist 4 (A, B, C, D, E nó F) thíos.'
    options = [
        ('X-4A', 'literature-4-a', '4A. An Triail', 'irish-6-0',
         '4A. An Triail\n“A muintir féin – a máthair agus a deartháireacha, Liam agus Seán – is cúis le cuid mhór den fhulaingt i saol Mháire sa dráma An Triail.”\n'
         'Déan plé ar an ráiteas sin. (40 marc)'),
        ('X-4B', 'literature-4-b', '4B. A Thig Ná Tit Orm', 'irish-6-1',
         '4B. A Thig Ná Tit Orm\n“Ba iad an ceol agus an chaid (an pheil) an dá chaitheamh aimsire ab fhearr le Maidhc Dainín agus é ag fás aníos sa Ghaeltacht.”\n'
         'Déan plé ar an ráiteas sin. (40 marc)'),
        ('X-4C', 'literature-4-c', '4C. Tóraíocht Dhiarmada agus Ghráinne', 'irish-6-2',
         '4C. Tóraíocht Dhiarmada agus Ghráinne\n“An grá, an t-éad agus an díoltas – is iad na mothúcháin seo is cúis leis na heachtraí sa Tóraíocht.”\n'
         'Déan plé ar an ráiteas sin. (40 marc)'),
        ('X-4D', 'literature-4-d', '4D. Gafa', 'irish-6-3',
         '4D. Gafa\n“Tá an imní agus an t-uaigneas ag líonadh chroí na máthar, Eithne, sa sliocht as an úrscéal Gafa.”\nDéan plé ar an ráiteas sin. (40 marc)'),
        ('X-4E', 'literature-4-e', '4E. Canary Wharf', 'irish-6-4',
         '4E. Canary Wharf\n“Sa scéal Cosaint Sonraí, tá léiriú éifeachtach ar an dearcadh difriúil atá ag Leanóra agus ag Gráinne ar an saol agus ar an obair.”\n'
         'Déan plé ar an ráiteas sin. (40 marc)'),
    ]
    for key, slug, ref, topic, prompt in options:
        assert all(in_order(line, texts[9]) for line in prompt.splitlines()), key
        # The scheme prints no text of its own for 4A–4E: the Treoracha (PDF 28) price each as Eolas 35 assessed as a unit.
        add(key, slug, f'Litríocht {ref}', head4 + '\n\n' + prompt, topic, [10], [28, 29],
            [criterion('eolas', 'Eolas', 35, [m['general4'], m['grading']], 'indicative'), gaeilge()], LIT_REQUIREMENTS,
            'One complete SEC response: Eolas 35 assessed as a unit with a single shared 5-mark Gaeilge award. The 2015 scheme prints no notes for '
            '4A–4E beyond the Treoracha for Ceist 4; its general grading table (PDF 29) converts a grade to a mark.')
    whole, spages = s.chunk('4F. Dánta Breise – Colmáin', 'Ní mór don Scrúdaitheoir an marc ar eolas as 35 marc', s.page(28))
    assert spages == [28]
    # The scheme does not reprint the three lines 4F(ii) asks about; its (ii) is "Míniú = 8 marc" alone.
    pieces = split_parts(whole, ['(ii) A bhfuil i gceist leis na línte seo a mhíniú', '(iii) Cén t-atmaisféar atá sa dán seo'],
                         ['Eolas = 19 marc', 'Míniú = 8 marc', 'Eolas = 8 marc'])
    f_prompt = ('4F. Dánta Breise – Colmáin\nFreagair (i), (ii) agus (iii) thíos.\n'
                '(i) Cad é príomhthéama an dáin Colmáin (thall), dar leat? Déan plé ar an léiriú a dhéantar ar an bpríomhthéama sin ó thús deireadh an dáin. (20 marc)\n'
                '(ii) A bhfuil i gceist leis na línte seo a mhíniú:\nSa deireadh, lá buí Bealtaine le luí gréine,\n'
                'chinn sé léim an cholmáin a thabhairt ó leac na fuinneoige\nleis na heiteoga a bhí in easbaidh air…faraoir. (10 marc)\n'
                '(iii) Cén t-atmaisféar atá sa dán seo, dar leat? Is leor dhá phointe eolais. Bíodh tagairtí cruinne agat do théacs an dáin i do fhreagra. (10 marc)')
    assert all(in_order(line, texts[9]) for line in f_prompt.splitlines())
    add('X-4F', 'literature-4-f', 'Litríocht 4F · Dánta Breise – Colmáin', head4 + '\n\n' + f_prompt, 'irish-6-9', [10, 11], [28, 29],
        [criterion('eolas-i', '(i) Eolas', 19, [pieces[0], m['grading']], 'indicative'), criterion('eolas-ii', '(ii) Eolas', 8, [pieces[1]], 'indicative'),
         criterion('eolas-iii', '(iii) Eolas', 8, [pieces[2]], 'indicative'), gaeilge()], LIT_REQUIREMENTS,
        'One complete SEC response: the paper prints (i) 20, (ii) 10 and (iii) 10; the scheme assesses Eolas 19 (2 + 17), Míniú 8 and 8 (2 + 3 + 3) '
        'plus one shared 5-mark Gaeilge award. Supporting notes are indicative rather than exhaustive.',
        source=('Dánta Breise', 'Colmáin', [10, 11]))

    reading = [c for c in cards if '-reading-' in c['id']]
    literature = [c for c in cards if '-reading-' not in c['id']]
    assert len(reading) == 52 and len(literature) == 12, (len(reading), len(literature))
    assert len({c['id'] for c in cards}) == len(cards) == 64 and len({c['atlasQuestionId'] for c in cards}) == 64
    assert sum(c['totalMarks'] for c in cards if re.fullmatch(r'R-[AB]-\d', c['atlasQuestionId'])) == 100
    for card in cards:
        assert sum(c['maxMarks'] for c in card['criteria']) == card['totalMarks'], card['id']
        for c in card['criteria']:
            assert c['guidance'] and all(not re.search('[-]', g) for g in c['guidance']), (card['id'], c['id'])
            assert all(h not in g for h in FURNITURE for g in c['guidance']), (card['id'], c['id'])
    sr = json.loads(SOURCE_REVIEW.read_text())
    whole = [c['id'] for c in reading if re.fullmatch(r'R-[AB]-\d', c['atlasQuestionId'])]
    review = dict(year=2015, level='higher', paperFileid=FILE + '.pdf', schemeFileid=SCHEME_FILE + '.pdf',
                  paperSha256=PAPER_SHA, schemeSha256=SCHEME_SHA,
                  reviewedPaperPages=list(range(1, 13)), reviewedSchemePages=sr['reviewedSchemePages'], schemeScope=sr['schemeScope'],
                  reviewDate=REVIEWED_AT, status='reviewed', fullPaperAndApplicableSchemeVisualSweep=True, selectionDecisions=m['decisions'],
                  readingWholeCardIds=whole, readingPracticeCardIds=[c['id'] for c in reading if c['id'] not in whole],
                  literatureRouteCardIds=[c['id'] for c in literature],
                  examStructure=dict(readingA=50, readingB=50, prose=30, poetry=30, additionalLiterature=40, total=200),
                  nonPoolDecisions=sr['nonPoolDecisions'], openIssues=[], caveats=sr['sourceFindings'],
                  boundaries='12 whole reading questions with 34 published parts and 6 independent one-mark answer slots; '
                             '2 prescribed prose routes (2A Cáca Milis or An Lasair Choille), 2 optional prose routes (2B scannán or dráma), 2 poetry and 6 additional-literature routes.')
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
    print(f"Irish Higher 2015 Paper 2: {len(data['cards'])} reviewed reading and literature cards; the archive remains incomplete.")


if __name__ == '__main__':
    main()
