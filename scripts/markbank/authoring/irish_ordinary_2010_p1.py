"""Reviewed 2010 Ordinary Páipéar I (Ceapadóireacht agus Léamhthuiscint), carded new.

Paper PDF 1–8 (LC001GLP100IV: instructions on page 1, Ceist 1 Ceapadóireacht on 2, Ceist 2 Léamhthuiscint A on 3 and
B on 4; pages 5–8 print “Leathanach Bán”) and the Páipéar I pages of the combined LC001GLP000EV scheme (PDF 3–4, and
11 Socruithe Réasúnta; the file is named EV, its text is the Irish scheme) reviewed on 2026-11-05. Scheme PDF 5–9
belong to Páipéar II and 10 to the listening test (irish_ordinary_2010_p2.py, irish_ordinary_2010_aural.py). Counts are
assertions, not corpus-completeness proof.

Before 2012, Páipéar I (220 marc) is the composition and the reading, and the listening test is a paper of its own:

- Ceist 1 Ceapadóireacht (120): “Freagair do rogha dhá cheann de A, B, C, D anseo.”, each at 60: A giota leanúnach
  (three titles), B scéal (two openings), C litir (two), D comhrá (two). The scheme (PDF 3, its notes running onto PDF
  4) prices each piece Tasc 3, Ábhar 9, Cumas Gaeilge 48 (“= 60 marc × 2 = 120 marc”) in 2011's printed blocks: the
  tariffs; the bracketed Cumas Gaeilge definition, (i) Stór Gaeilge 40% and (ii) beachtas 50% agus litriú 10%; the
  bracketed content note; the examiner's Nóta (misprinting “Tasc” as “Tásc”); a bracketed Nóta on the “Gaeilge
  Lochtach” of the questions after it. No 48-mark table.
- Ceist 2 Léamhthuiscint (100): A (the weather, “Agus anois an Aimsir …”) and B (Raidió Rí-Rá, “Craoladh Digiteach”),
  five questions each at 10. The scheme (PDF 4) prints no answers: each question's asks restated in a line and one
  price for the whole question (“1. (a) Grúpa amháin daoine a chuireann spéis san aimsir (b) An toradh a bheadh ar
  aimsir thirim a leanfadh ar feadh i bhfad = 10 marc”). Each question is one card with one 10-mark criterion whose
  guidance is that line, claimed whole (0 or 10): splitting it between (a) and (b) would be a price the SEC never
  printed. `tariffOnly`: the chip says “Tariff”.

The pages are read glyph by glyph (`paper_lines`, as 2011's tiled pages need): the two passage columns are kept apart,
so every prompt is asserted against the page as printed.

No 2010 Ordinary card existed before. `build` cards the nine composition titles as 60-mark cards (choice is not a
route: each title carries the printed choose-two instruction; no combination cards) and the ten reading questions.
The 2010 Atlas files this paper under the pre-2012 keys R-A, R-B and W-A … W-D; the card keys are 2011's (W-A-i …,
R-A-1 …), which do not clash. `main` writes the card file and the searchable scheme text examiner-reports/irish/schemes/
2010-ol.md.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import re
from pathlib import Path
from irish_lifted import PUA, scheme_words_in, symbol_text

ROOT = Path(__file__).resolve().parents[3]
YEAR = 2010
FILE = 'LC001GLP100IV'
SCHEME_FILE = 'LC001GLP000EV'
OUT = ROOT / 'components/MarkBank/cards/irish/ordinary-2010-p1-authored.json'
SCHEME_MD = ROOT / f'examiner-reports/irish/schemes/{YEAR}-ol.md'
SOURCE_REVIEW = ROOT / 'scripts/markbank/authored/irish-ordinary-2010-p1-source-review.json'
REVIEWED_AT = '2026-11-05'
PAPER_SHA = '0893ef63546910af7e38afae234819002284e2a7692b6272e71be9122baa6ceb'
SCHEME_SHA = '5dbf2d23c447f46e35a9704197612a59f99c11fb8c559e509e3e794d03e08081'
DIRECTIVE = re.compile(r'rogha|roghna|Freagair|Cuir tic|Ainmnigh|Luaigh|\bnó\b|dhá phointe|dhá rud|dó/di|ceann amháin|amháin|\bdhá\b', re.I)
SOURCE_NOTE = 'Shown page-for-page from the official examination paper; swipe to move between pages.'
ATTRIBUTION = '© State Examinations Commission.'
UNPRINTED_ANSWER = 'The scheme prints no answer for this part.'  # types/markBank.ts
LANG_READ = '[Gaeilge lochtach: 0 - 5 a bhaint den iomlán a gnóthaíodh.]'
REDUNDANCY = '[Gearrfar pionós i ngeall ar iomarcaíocht]'
READ_NOTA = ('Nóta: Taispeánfar go soiléir na marcanna a ghnóthaíonn iarrthóirí as an mbuneolas a aimsiú, na marcanna a bhaintear i '
             'ngeall ar an nGaeilge a bheith lochtach agus na marcanna a bhaintear i ngeall ar iomarcaíocht san ionad cuí ar an bhfreagarleabhar.')
# The scheme's SymbolMT glyphs: U+F0B4 (×, PDF 3, 5–9) and U+F0B7 (•, PDF 11).
SYMBOL_FONT = {'': '×', '': '•', ' ': ' '}


def clean(text):
    return re.sub(r'\s+', ' ', symbol_text(text)).strip()


def comparable(text):
    return re.sub(r'[^\w]+', '', text.lower())


def in_order(prompt, text):
    return re.search('.*?'.join(re.escape(comparable(w)) for w in prompt.split() if comparable(w)), comparable(text))


def paper_lines(page):
    """The page's printed lines, read glyph by glyph (2011's tiled reader): a glyph the text layer repeats at (almost) the same
    origin is drawn once, and a gap wider than a word space starts a new column segment."""
    chars = []
    for block in page.get_text('rawdict')['blocks']:
        for line in block.get('lines', []):
            for span in line['spans']:
                for c in span['chars']:
                    chars.append((c['origin'][0], c['origin'][1], c['c'], c['bbox'][2]))
    rows = {}
    for x, y, c, x1 in chars:
        rows.setdefault(round(y), []).append((x, c, x1))
    out = []
    for y in sorted(rows):
        kept = []
        for x, c, x1 in sorted(rows[y]):
            if any(abs(x - kx) < 1.5 and kc == c for kx, kc, _ in kept[-3:]):
                continue
            kept.append((x, c, x1))
        segment, prev = [], None
        for x, c, x1 in kept:
            if prev is not None and x - prev > 9 and segment:
                out.append(clean(''.join(segment)))
                segment = []
            segment.append(c)
            prev = x1
        if segment:
            out.append(clean(''.join(segment)))
    return [line for line in out if line]


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


def criterion(id, label, marks, guidance, kind='quality', permitted=None, tariff_only=False):
    return dict(id=id, label=label, kind='award', maxMarks=marks, permittedMarks=permitted or list(range(marks + 1)),
                guidanceKind=kind, guidance=guidance, **({'tariffOnly': True} if tariff_only else {}))


def source(label, title, pages):
    return dict(kind='source-text', label=label, title=title, pages=pages, attribution=ATTRIBUTION, presentationNote=SOURCE_NOTE)


def selection_decisions(paper):
    decisions = json.loads(SOURCE_REVIEW.read_text())['selectionDecisions']
    expected = {(d['page'], d['raw']) for d in decisions}
    found = {(i, line) for i, page in enumerate(paper, 1) for line in paper_lines(page) if DIRECTIVE.search(line)}
    assert found == expected, ('Unclassified/stale selection directives', found - expected, expected - found)
    return decisions


HEAD = ('Ní mór do na hiarrthóirí cúram a dhéanamh de chruinneas na teanga. Caillfear marcanna má bhítear faillitheach ann.\n\n'
        'Freagair do rogha dhá cheann de A, B, C, D anseo.')
GROUPS = {
    'A': ('GIOTA LEANÚNACH', 'irish-2-6', 'Scríobh giota leanúnach (leathleathanach nó mar sin) ar cheann amháin de na hábhair seo:', [
        ('i', 'An áit is fearr liom in Éirinn.'), ('ii', 'Duine cáiliúil a thaitníonn go mór liom.'), ('iii', 'Draíocht an cheoil.')]),
    'B': ('SCÉAL', 'irish-2-3', 'Ceap scéal (leathleathanach nó mar sin) a mbeidh ceann amháin de na sleachta seo a leanas oiriúnach mar thús leis.', [
        ('i', 'Chonaic mé an liathróid ag teacht i mo threo. D’fhéach mé timpeall orm, ní raibh aon duine in aice liom. Léim mo chroí le háthas …'),
        ('ii', 'Bhí brón orm gur thóg mé mo chara liom ar saoire mar bhí sé/sí ag gearán an t-am go léir.')]),
    'C': ('LITIR', 'irish-2-8', None, [
        ('i', 'Tá teach ósta nua oscailte ag do thuismitheoirí agus tá post samhraidh ar fáil sa chistin ann.\n'
              'Scríobh an litir (leathleathanach nó mar sin) a chuirfeá chuig cara leat ag insint dó/di faoin bpost agus ag moladh dó/di '
              'iarratas a chur isteach ar an bpost sin.'),
        ('ii', 'Tá tú féin agus do chara ag iarraidh airgead a bhailiú chun seandaoine a thabhairt ar saoire.\n'
               'Scríobh an litir (leathleathanach nó mar sin) a chuirfeá chuig iarscoláire saibhir ó do scoil ag lorg airgid air/uirthi.')]),
    'D': ('COMHRÁ', 'irish-2-9', None, [
        ('i', 'Ba mhaith le do rang damhsa mór a chur ar siúl i halla na scoile ag deireadh na bliana.\n'
              'Níl an príomhoide róchinnte faoin smaoineamh. Scríobh an comhrá (leathleathanach nó mar sin) a bheadh idir an bheirt agaibh '
              'faoin ábhar sin.'),
        ('ii', 'Is maith leat féachaint ar na cláir réaltachta mar X Factor ar an teilifís ach is fearr le do chara na cláir spóirt.\n'
               'Scríobh an comhrá (leathleathanach nó mar sin) a bheadh idir an bheirt agaibh faoi sin.')]),
}
# (letter, title, paper page, topic, [(q, paper prompt lines, scheme start, scheme price as printed)])
PASSAGES = {
    'A': ('Agus anois an Aimsir …', 3, 'irish-3-0', [
        ('1', ['(a) Luaigh grúpa amháin daoine a chuireann spéis san aimsir. (Alt 1)',
               '(b) Cén toradh a bheadh ar aimsir thirim a leanfadh ar feadh i bhfad? (Alt 1)'], '1. (a) Grúpa amháin', '= 10 marc'),
        ('2', ['(a) Luaigh rud amháin a thaispeánann go bhfuil an aimsir ag athrú. (Alt 2)',
               '(b) Cén dochar a dhéanann drochaimsir sa samhradh in Éirinn? (Alt 2)'], '2. (a) Rud amháin', '= 10 marc'),
        ('3', ['(a) Luaigh rud maith amháin a dhéanann an bháisteach. (Alt 3)', '(b) Is maith le daoine uisce. Tabhair sampla amháin. (Alt 3)'],
         '3. (a) Rud maith', '= 10 marc'),
        ('4', ['Luaigh dhá dhrochrud a bhain leis an aimsir in Éirinn in 2009. (Alt 4)'], '4. Dhá dhrochrud', '= 10 marc'),
        ('5', ['Luaigh dhá athrú a chaithfimid a dhéanamh sna blianta atá ag teacht. (Alt 5)'], '5. Dhá athrú', '= 10 marc')]),
    'B': ('Craoladh Digiteach – Todhchaí an Raidió Gaeilge?', 4, 'irish-3-1', [
        ('1', ['Cá raibh Raidió Rí-Rá á chraoladh roimh thús mhí an Mhárta seo caite? (Alt 1)'], '1. An áit', '= 10 marc'),
        ('2', ['Cén difríocht a bhí idir Raidió Rí-Rá agus stáisiúin ar nós Today FM, Spin 103.8 nó RTÉ 2FM? (Alt 2)'], '2. An difríocht', '= 10 marc'),
        ('3', ['Cén fáth a raibh seans ag daoine óga taitneamh a bhaint as an gclár “Nocht ag a hOcht”? (Alt 3)'], '3. An fáth', '= 10 marc'),
        ('4', ['Luaigh na tíortha lasmuigh d’Éirinn ina raibh éisteoirí ag Raidió Rí-Rá. (Alt 4)'], '4. Na tíortha', '= 10 marc'),
        ('5', ['(a) Cén stáisiún raidió in Éirinn atá ag craoladh ar an gcóras digiteach anois?',
               '(b) Cad a tharlóidh má éiríonn go maith leis an gcóras digiteach in Éirinn? (Alt 5)'], '5. (a) An stáisiún', '= 10 marc')]),
}
COMPOSITION_REQUIREMENTS = ['Freagair do rogha dhá cheann de A, B, C, D anseo.', 'Lean an fhoirm scríbhneoireachta a iarrtar sa cheist.',
                            'Coinnigh ceangal cinnte leanúnach idir an teideal agus an t-ábhar.', 'Leathleathanach nó mar sin.']
READING_WHOLE = ['Léigh an sliocht oifigiúil a ghabhann leis an gceist.', 'Freagair gach fochuid agus cloígh leis an alt a luaitear.']

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
    assert len(paper) == 8 and len(scheme) == 12
    lines = [paper_lines(p) for p in paper]
    texts = [' '.join(l) for l in lines]
    stext = [clean(page_text(p)) for p in scheme]
    assert not PUA.search(' '.join(stext[2:4])), 'private-use glyph left in the scheme text'
    # Page 1: the paper's instructions; 5–8 “Leathanach Bán”.
    assert 'PÁIPÉAR I' in texts[0] and '(220 marc)' in texts[0] and 'Ceist 1 agus Ceist 2 a fhreagairt.' in texts[0]
    assert comparable(HEAD.split('\n\n')[0]) in comparable(texts[0])
    assert texts[4:] == ['Leathanach Bán'] * 4

    # Composition (paper page 2; scheme PDF 3–4).
    assert 'CEIST 1 – CEAPADÓIREACHT– [120 marc]' in texts[1] and HEAD.split('\n\n')[1] in texts[1]
    for group, (form, _, instruction, titles) in GROUPS.items():
        assert f'{group} – {form} – (60 marc)' in texts[1], group
        for roman, title in titles:
            for line in ([instruction] if instruction else []) + title.splitlines():
                assert in_order(line, texts[1]), (group, roman, line[:40])
    # The composition's marking runs from PDF 3 onto PDF 4 (its Nóta and the Gaeilge Lochtach note), up to Ceist 2.
    page4 = re.sub(r'^3 ', '', stext[3])
    marking = stext[2][stext[2].index('Freagair do rogha dhá cheann'):] + ' ' + page4[:page4.index('CEIST 2 (A + B)')].strip()
    tariffs, rest = marking.split(' [Cumas Gaeilge = (i) ', 1)
    cumas, rest = rest.split(' [Gearrfar pionós', 1)
    content, rest = rest.split('] Nóta: ', 1)
    nota, lochtach = rest.split(' [Nóta: Maidir le', 1)
    tariffs, cumas = tariffs.strip(), '[Cumas Gaeilge = (i) ' + cumas.strip()
    content, nota = '[Gearrfar pionós' + content + ']', 'Nóta: ' + nota.strip()
    assert tariffs == ('Freagair do rogha dhá cheann de A, B, C, D anseo. I gcás A, B, C, agus D (Dhá cheann le freagairt) '
                       'Leathleathanach nó breis: Tasc = 3 marc Ábhar = 9 marc = 60 marc × 2 = 120 marc Cumas Gaeilge = 48 marc'), tariffs
    assert cumas.endswith('(= 50%) agus litriú (= 10%).]') and '(= 40%)' in cumas, cumas[-60:]
    assert content == '[Gearrfar pionós ar iarrthóirí mura mbeidh na hiarrachtaí ceapadóireachta ad rem.]', content
    # The examiner's Nóta misprints “Tasc” as “Tásc”: kept as printed.
    assert nota.startswith('Nóta: Caithfidh an Scrúdaitheoir an marc a bhronntar as 3 (Tásc)') and nota.endswith('ag bun na n-iarrachtaí ceapadóireachta.'), nota
    assert lochtach.startswith(' ‘Gaeilge Lochtach’ a luaitear leis na ceisteanna ina dhiaidh seo') and lochtach.endswith('40% : 60%]'), lochtach[:80]
    assert 'Sármhaith' not in ' '.join(stext) and '95%' not in ' '.join(stext)

    # Reading (paper pages 3–4; scheme PDF 4): a restatement and one price per question, no answers.
    reading = {}
    read = page4[page4.index('CEIST 2 (A + B)'):]
    assert read.startswith('CEIST 2 (A + B) - LÉAMHTHUISCINT - 100 marc Freagair A agus B anseo. A (50 marc) 1. (a)'), read[:80]
    # One 0–5 deduction under each passage; B's redundancy penalty and the closing Nóta after B's.
    assert read.count(LANG_READ) == 2 and read.endswith(LANG_READ + ' ' + REDUNDANCY + ' ' + READ_NOTA), read[-200:]
    assert not re.search(r'Freagraí|Freagra:|Samplaí|samplacha|féideartha|•', read)
    for letter, (title, page, topic, questions) in PASSAGES.items():
        assert title in lines[page - 1], letter
        assert f'{letter} – (50 marc)' in lines[page - 1] and 'Léigh an sliocht seo a leanas agus freagair na ceisteanna ar fad a ghabhann leis.' in lines[page - 1]
        after = read.index(f'{letter} (50 marc)')
        out = []
        for index, (q, prompt, start, price) in enumerate(questions):
            assert in_order(f'{q}. ' + ' '.join(prompt) + ' 10 marc', texts[page - 1]), (letter, q)
            end = questions[index + 1][2] if index + 1 < len(questions) else LANG_READ
            i = read.index(start, after)
            chunk = read[i:read.index(end, i + 1)].strip()
            after = i + 1
            assert chunk.endswith(price) and chunk.count('=') == 1, (letter, q, chunk)
            out.append((q, prompt, chunk))
        reading[letter] = out
    _MATERIAL = dict(paper=paper, texts=texts, reading=reading,
                     composition=dict(tariffs=tariffs, cumas=cumas, content=content, nota=nota),
                     decisions=selection_decisions(paper))
    return _MATERIAL


READING_NOTE = ('One SEC price for the whole question (10); the scheme restates what each part asks and does not split the price between them, '
                'so the question is claimed whole (0 or 10). ' + UNPRINTED_ANSWER + ' Scheme: “' + LANG_READ + '” — one deduction from each '
                'passage total (50), never inside a single question; “' + REDUNDANCY + '” for redundancy, likewise.')


def build():
    m = material()
    cards = []
    c = m['composition']
    for group, (form, topic, instruction, titles) in GROUPS.items():
        for roman, title in titles:
            body = HEAD + f'\n\n{group} · {form} (60 marc)\n' + (instruction + '\n' if instruction else '') + f'({roman}) {title}'
            cards.append(dict(
                id=f'irish-{YEAR}-ol-p1-composition-{group.lower()}-{roman}', year=YEAR, level='ordinary', paper=1, section='1',
                questionRef=f'{YEAR} OL Paper 1 Ceapadóireacht {group}({roman})', questionText=body, totalMarks=60, topicId=topic,
                conceptId=f'irish-composition-{group.lower()}', paperPage=2, schemePage=3, taskRequirements=COMPOSITION_REQUIREMENTS,
                # 2010 prints 2011's blocks: the tariff block prices the task, the bracketed note is the scheme's content guidance,
                # and the Cumas Gaeilge definition and the Nóta go with Gaeilge (two printed blocks, two lines).
                criteria=[criterion('tasc', 'An Tasc', 3, [c['tariffs']], permitted=[0, 3]),
                          criterion('abhar', 'An tÁbhar', 9, [c['content']]),
                          criterion('gaeilge', 'An Cumas Gaeilge', 48, [c['cumas'], c['nota']])],
                markingGuideNote=f'Whole 60-mark composition: Tasc 3, Ábhar 9, Cumas Gaeilge 48. The {YEAR} scheme prints no 48-mark table: '
                                 'Cumas Gaeilge is judged on its printed aspects, (i) the range and richness of the candidate’s Irish (40%) and '
                                 '(ii) accuracy in the main features of correct Irish (50%) and spelling (10%), so the award can take any value from 0 to 48. '
                                 'Socruithe Réasúnta (scheme PDF 11): for candidates granted reasonable accommodations, spelling and certain grammar '
                                 'features are not counted; the scheme prints no bands for it.',
                paperFileid=FILE, atlasQuestionId=f'W-{group}-{roman}', reviewedAt=REVIEWED_AT, reviewedPaperPages=[1, 2],
                schemeFileid=SCHEME_FILE, schemePages=[3], sourceMaterial=source(f'Ceapadóireacht {group}({roman})',
                                                                                 f'Gaeilge Gnáthleibhéal {YEAR} · Páipéar 1 · Ceapadóireacht {group}({roman})', [1, 2])))
    composition_ids = [x['id'] for x in cards]
    whole_ids = []
    for letter, (title, page, topic, _) in PASSAGES.items():
        src = source(f'Léamhthuiscint {letter}', title, [page])
        for q, prompt, chunk in m['reading'][letter]:
            label = '(a) + (b)' if len(prompt) == 2 else 'Freagra'
            cards.append(dict(
                id=f'irish-{YEAR}-ol-p1-reading-{letter.lower()}-q{q}', year=YEAR, level='ordinary', paper=1, section='1',
                atlasQuestionId=f'R-{letter}-{q}', questionRef=f'{YEAR} OL Paper 1 Léamhthuiscint {letter} · Ceist {q}',
                questionText=f'{q}. ' + ' '.join(prompt), totalMarks=10, topicId=topic, conceptId=f'irish-reading-{letter.lower()}-q{q}',
                paperFileid=FILE, paperPage=page, schemeFileid=SCHEME_FILE, schemePage=4, schemePages=[4], reviewedAt=REVIEWED_AT,
                reviewedPaperPages=[page], taskRequirements=READING_WHOLE,
                criteria=[criterion('eolas', label, 10, [chunk], kind='exact', permitted=[0, 10], tariff_only=True)],
                markingGuideNote=READING_NOTE, sourceMaterial=src))
            whole_ids.append(cards[-1]['id'])
    assert len(composition_ids) == 9 and len(whole_ids) == 10
    assert len(cards) == 19 and len({x['id'] for x in cards}) == 19 and len({x['atlasQuestionId'] for x in cards}) == 19
    for card in cards:
        assert sum(cr['maxMarks'] for cr in card['criteria']) == card['totalMarks'], card['id']
        for cr in card['criteria']:
            assert cr['guidance'] and all(not PUA.search(g) for g in cr['guidance']), (card['id'], cr['id'])
    sr = json.loads(SOURCE_REVIEW.read_text())
    review = dict(year=YEAR, level='ordinary', paperFileid=FILE + '.pdf', schemeFileid=SCHEME_FILE + '.pdf',
                  paperSha256=PAPER_SHA, schemeSha256=SCHEME_SHA,
                  reviewedPaperPages=list(range(1, 9)), reviewedSchemePages=sr['reviewedSchemePages'], schemeScope=sr['schemeScope'],
                  reviewDate=REVIEWED_AT, status='reviewed', fullPaperAndApplicableSchemeVisualSweep=True, selectionDecisions=m['decisions'],
                  cardIds=composition_ids + whole_ids, compositionRouteCardIds=composition_ids, readingWholeCardIds=whole_ids,
                  examStructure=dict(composition=120, readingA=50, readingB=50, total=220),
                  nonPoolDecisions=sr['nonPoolDecisions'], openIssues=[], caveats=sr['sourceFindings'],
                  choicePolicy='Choice is not a route: each printed composition title is one card carrying the printed choose-two instruction; no combination cards.',
                  boundaries='9 composition titles at 60 (answer any two; no combination cards); 10 whole reading questions (each one '
                             '10-mark price, not split between its parts; the scheme prints no answers).')
    return dict(review=review, cards=cards)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    data = build()
    scheme_words_in(data)  # guidance, question and task checks carry the SEC's words only (irish_lifted.py)
    import fitz
    scheme = fitz.open(ROOT / f'paper-trail-corpus/markingschemes/{YEAR}/{SCHEME_FILE}.pdf')
    # The searchable scheme text the provenance checks read, with its SymbolMT glyphs read as `page_text` reads them.
    scheme_md = f'# Gaeilge Gnáthleibhéal {YEAR} — SEC marking scheme (Páipéar I, Páipéar II agus an Triail Chluastuisceana)\n\n' + '\n\n'.join(
        f'## PDF page {i + 1}\n\n' + page_text(p) for i, p in enumerate(scheme))
    outputs = {OUT: json.dumps(data, ensure_ascii=False, indent=2) + '\n',
               SCHEME_MD: '\n'.join(line.rstrip() for line in scheme_md.splitlines()).rstrip() + '\n'}
    for path, value in outputs.items():
        if args.check:
            assert path.exists() and path.read_text() == value, f'Stale output: {path}'
        else:
            path.write_text(value)
    print(f"Irish Ordinary {YEAR} Paper 1: {len(data['cards'])} reviewed cards (9 titles, 10 reading questions); the archive remains incomplete.")


if __name__ == '__main__':
    main()
