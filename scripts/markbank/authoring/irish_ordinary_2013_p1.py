#!/usr/bin/env python3
"""Reviewed 2013 Ordinary Paper 1 (Cluastuiscint agus Ceapadóireacht), carded new.

Paper PDF 1–8 (2013 prints no answer booklet: Cuid A on page 3, the composition
Treoracha on page 6, the titles on page 7, page 8 blank) and the Paper 1 pages of the
combined LC001GLP000IV scheme (PDF 1–14 and 29 modified marking) reviewed on
2026-11-05. Scheme PDF 15–28 belong to Paper 2; 30–31 are blank and 32 empty. Counts
are assertions, not corpus-completeness proof. Same layout and method as
irish_ordinary_2014_p1.py, with the differences the 2013 scheme prints: the tariffs and
the only print of the 0–6 language deduction are on PDF 5 (whose Cuid C line misprints
its total as “20 marc (Eolas)” above “6 + 6 = 12 mharc”); the transcript runs PDF 6–10
and the key PDF 11–13, in the paper's order (the Fógra a hAon grid first); the grid's
second row prices its two answers “2 mharc + 1 mharc”, Comhrá a Dó An Chéad Mhír 2 prints
“2 mharc+1 mharc=3 mharc” and Píosa a hAon 2 prints a 1-mark partial (“Dún na nGall 1
mharc”); the scheme sets its multiplication sign (PDF 5 and 14) and its answer bullets
(Paper 2) in SymbolMT, which the text layer gives as the private-use U+F0B4 and U+F0B7;
and the composition marking (PDF 14) prints the Cumas Gaeilge definition in brackets
((i) Stór Gaeilge 40%, (ii) beachtas 50% agus litriú 10%), no 40-mark table, and a
modified-marking page (PDF 29) with no bands.

No 2013 Ordinary card existed before. `build` cards the component the way the reviewed
2014–2025 Ordinary Paper 1s are carded: six listening segment cards (the Bank plays
one recording section as one exercise), each printed question its own criterion with
its lifted scheme slice, and the nine printed composition titles as 50-mark cards.
“Freagair do rogha dhá cheann de A, B, C, D” is a choice, not a route: each title is
its own card and carries the printed instruction as its task check; no two-section
combination cards. `main` writes the card file.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import re
from pathlib import Path
from irish_lifted import PUA, scheme_words_in, symbol_text

ROOT = Path(__file__).resolve().parents[3]
YEAR = 2013
FILE = 'LC001GLP100IV'
SCHEME_FILE = 'LC001GLP000IV'
OUT = ROOT / 'components/MarkBank/cards/irish/ordinary-2013-p1-authored.json'
SCHEME_MD = ROOT / f'examiner-reports/irish/schemes/{YEAR}-ol.md'
SOURCE_REVIEW = ROOT / 'scripts/markbank/authored/irish-ordinary-2013-p1-source-review.json'
REVIEWED_AT = '2026-11-05'
PAPER_SHA = 'bf0982de0c76e921cd319b16eac0e6a71a7cdabc693b0dfba61b95c0c95d5797'
SCHEME_SHA = '52406fccffb57cc291d43ab1c4d7ae89fea9dbf246e702125c567bbbccfeeff1'
AUDIO_URL = 'https://www.examinations.ie/archive/exampapers/2013/LC001ZLP017IV.mp3'
DIRECTIVE = re.compile(r'rogha|roghna|Freagair|Cuir tic|Ainmnigh|Luaigh|\bnó\b|dhá phointe|dhá rud|dó/di|ceann amháin|amháin|\bdhá\b', re.I)
SOURCE_NOTE = 'Shown page-for-page from the official examination paper; swipe to move between pages.'
LANGUAGE = ('Scheme PDF 5: “Bainfear ó 0 go 6 ar chaighdeán na Gaeilge.” This 0–6 deduction applies once to the whole '
            'listening section (Tuiscint 60 − Cumas Gaeilge 0–6), never inside a single question.')
HEADINGS = re.compile(r'\s*(FÓGRA A DÓ \(12 mharc\)|Cuid B \(24 marc\) COMHRÁ A hAON \(12 mharc\) An Chéad Mhír|An Dara Mír|'
                      r'COMHRÁ A DÓ \(12 mharc\) An Chéad Mhír|Cuid C \(12 mharc\) PÍOSA A hAON \(6 mharc\)|PÍOSA A DÓ \(6 mharc\))\s*$')
# The scheme's text layer gives its SymbolMT glyphs as private-use code points: the multiplication sign of the tariff
# pages (PDF 5 and 14) as U+F0B4 and the answer bullets (Paper 2, PDF 15–20; PDF 29) as U+F0B7; Adobe Symbol draws them as
# × and •.
SYMBOL_FONT = {'\uf0b4': '×', '\uf0b7': '•', ' ': ' '}


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


def criterion(id, label, marks, guidance, kind='quality', permitted=None):
    return dict(id=id, label=label, kind='award', maxMarks=marks, permittedMarks=permitted or list(range(marks + 1)),
                guidanceKind=kind, guidance=guidance)


def source(ref, pages):
    return dict(kind='source-text', label=ref, title=f'Gaeilge Gnáthleibhéal {YEAR} · Páipéar 1 · {ref}', pages=pages,
                attribution='© State Examinations Commission.', presentationNote=SOURCE_NOTE)


def selection_decisions(paper):
    decisions = json.loads(SOURCE_REVIEW.read_text())['selectionDecisions']
    expected = {(d['page'], d['raw']) for d in decisions}
    found = {(i, clean(line)) for i, page in enumerate(paper, 1)
             for line in page.get_text().splitlines() if DIRECTIVE.search(clean(line))}
    assert found == expected, ('Unclassified/stale selection directives', found - expected, expected - found)
    return decisions


class Marked:
    def __init__(self, doc, first, last):
        self.text = ''
        for p in range(first, last + 1):
            self.text += f' ⟦{p}⟧ ' + re.sub(r'^\d+\s', '', clean(page_text(doc[p - 1])))

    def split(self, starts, stop, strip=None):
        """Slice at each start; `strip` removes trailing furniture (headings) BEFORE pages are counted."""
        out, cursor = [], 0
        for i, start in enumerate(starts):
            a = self.text.index(start, cursor)
            b = self.text.index(starts[i + 1], a + len(start)) if i + 1 < len(starts) else self.text.index(stop, a)
            raw = self.text[a:b]
            if strip:
                raw = strip(raw)
            pages = {int(re.findall(r'⟦(\d+)⟧', self.text[:a])[-1])}
            pages |= {int(m.group(1)) for m in re.finditer(r'⟦(\d+)⟧([^⟦]*)', raw) if clean(m.group(2))}
            out.append((clean(re.sub(r'⟦\d+⟧', ' ', raw)), sorted(pages)))
            cursor = a + len(start)
        return out


# (key, card suffix, ref, paper page, topic, [(criterion id, label, paper prompt, scheme anchor, marks)])
SEGMENTS = [
    ('L-A-F1', 'a-f1', 'Cuid A · Fógra a hAon', 3, 'irish-1-0', [
        # A grid ("Líon isteach an t-eolas atá á lorg sa ghreille anseo."): four unnumbered printed questions, the second asking
        # for two answers on the printed lines (i) and (ii).
        ('g1', 'Greille 1', 'Cathain a bheidh an comórtas Scléip ar siúl?', 'Cathain a bheidh an comórtas Scléip', 3),
        ('g2', 'Greille 2', 'Breac síos dhá rannóg a bheidh sa chomórtas.', 'Breac síos dhá rannóg', 3),
        ('g3', 'Greille 3', 'Cén táille iontrála atá ar gach rannóg?', 'Cén táille iontrála', 3),
        ('g4', 'Greille 4', 'Cad é an dáta deireanach le haghaidh iontrálacha?', 'Cad é an dáta deireanach', 3)]),
    ('L-A-F2', 'a-f2', 'Cuid A · Fógra a Dó', 3, 'irish-1-0', [
        ('q1a', 'Ceist 1(a)', 'Cén fáth a bhfuil na daoine ag fulaingt san Afraic?', '1. (a) Cén fáth a bhfuil na daoine', 3),
        ('q1b', 'Ceist 1(b)', 'Cathain a bheidh an turas rothaíochta urraithe ar siúl?', '(b) Cathain a bheidh an turas rothaíochta', 3),
        ('q2a', 'Ceist 2(a)', 'Cá mbeidh an oíche eolais ar siúl?', '2. (a) Cá mbeidh an oíche eolais', 3),
        ('q2b', 'Ceist 2(b)', 'Cé mhéad airgid nár mhór do dhuine a bhailiú?', '(b) Cé mhéad airgid nár mhór', 3)]),
    ('L-B-C1', 'b-c1', 'Cuid B · Comhrá a hAon', 4, 'irish-1-1', [
        ('m1-q1', 'An Chéad Mhír · Ceist 1', 'Cén t-ábhar san Ardteistiméireacht atá fós le déanamh ag Seán?', '1. Cén t-ábhar san Ardteistiméireacht', 3),
        ('m1-q2', 'An Chéad Mhír · Ceist 2', 'Cad a cheap Orla den pháipéar Bitheolaíochta?', '2. Cad a cheap Orla', 3),
        ('m2-q1', 'An Dara Mír · Ceist 1', 'Cá raibh Seán ag obair go páirtaimseartha an samhradh seo caite?', '1. Cá raibh Seán ag obair', 3),
        ('m2-q2', 'An Dara Mír · Ceist 2', 'Cad a dhéanfaidh Seán anocht?', '2. Cad a dhéanfaidh Seán anocht', 3)]),
    ('L-B-C2', 'b-c2', 'Cuid B · Comhrá a Dó', 4, 'irish-1-1', [
        ('m1-q1', 'An Chéad Mhír · Ceist 1', 'Cén t-am a shroich Síle aerfort Bhaile Átha Cliath maidin Dé Sathairn?', '1. Cén t-am a shroich Síle', 3),
        # Two answers on the printed lines (i) and (ii); one question.
        ('m1-q2', 'An Chéad Mhír · Ceist 2', 'Cén dá rud a deir Síle go raibh sí ag brath orthu san óstán?', '2. Cén dá rud a deir Síle', 3),
        ('m2-q1', 'An Dara Mír · Ceist 1', 'Cé mhéad duine a maraíodh i rith hairicín Sandy?', '1. Cé mhéad duine a maraíodh', 3),
        ('m2-q2', 'An Dara Mír · Ceist 2', 'Cá raibh pictiúr den siorc le feiceáil, dar le Colm?', '2. Cá raibh pictiúr den siorc', 3)]),
    ('L-C-P1', 'c-p1', 'Cuid C · Píosa a hAon', 5, 'irish-1-2', [
        ('q1', 'Ceist 1', 'Cé mhéad leathanach atá sa bhliainiris?', '1. Cé mhéad leathanach', 3),
        ('q2', 'Ceist 2', 'Cá bhfuil an bhliainiris ar díol?', '2. Cá bhfuil an bhliainiris', 3)]),
    ('L-C-P2', 'c-p2', 'Cuid C · Píosa a Dó', 5, 'irish-1-2', [
        ('q1', 'Ceist 1', 'Cén lá a raibh Aonach na Nollag ar siúl?', '1. Cén lá a raibh Aonach na Nollag', 3),
        ('q2', 'Ceist 2', 'Cé mhéad bliain atá ann ó bunaíodh Cór Chúil Aodha?', '2. Cé mhéad bliain atá ann', 3)]),
]
GRID = 'Líon isteach an t-eolas atá á lorg sa ghreille anseo.'
# The questions each card prints, in the 2021–2025 segment-card form (listeningQuestionGroups in SessionScreen.tsx).
SEGMENT_TEXT = {
    'L-A-F1': lambda qs: ' '.join([GRID] + [q[2] for q in qs]),
    'L-A-F2': lambda qs: f'1. (a) {qs[0][2]} (b) {qs[1][2]} 2. (a) {qs[2][2]} (b) {qs[3][2]}',
    'L-B-C1': lambda qs: f'An Chéad Mhír 1. {qs[0][2]} 2. {qs[1][2]} An Dara Mír 1. {qs[2][2]} 2. {qs[3][2]}',
    'L-B-C2': lambda qs: f'An Chéad Mhír 1. {qs[0][2]} 2. {qs[1][2]} An Dara Mír 1. {qs[2][2]} 2. {qs[3][2]}',
    'L-C-P1': lambda qs: f'1. {qs[0][2]} 2. {qs[1][2]}',
    'L-C-P2': lambda qs: f'1. {qs[0][2]} 2. {qs[1][2]}',
}
GROUPS = {
    'A': ('GIOTA LEANÚNACH / BLAG', 'irish-2-6', 'Scríobh giota leanúnach nó blag (leathleathanach nó mar sin) ar cheann amháin de na hábhair seo.', [
        ('i', 'Scannán a chonaic mé le déanaí.'), ('ii', 'Mo cheantar dúchais.'), ('iii', 'Is aoibhinn liom an deireadh seachtaine.')]),
    'B': ('SCÉAL', 'irish-2-3', 'Ceap scéal (leathleathanach nó mar sin) a mbeidh ceann amháin de na sleachta seo a leanas oiriúnach mar thús leis.', [
        ('i', 'Thit an pláta ina smidiríní ar an urlár. Bhí sicín rósta, glasraí agus prátaí i ngach áit. Las m’aghaidh le náire …'),
        ('ii', 'Bhí mo thuismitheoirí as baile. Tháinig mo chairde go léir chuig mo theach. Thosaigh an chóisir (an féasta) …')]),
    'C': ('LITIR / RÍOMHPHOST', 'irish-2-8', None, [
        ('i', 'Ghlac tú páirt i dtrialacha don seó nua tallainne ar RTÉ.\n'
              'Scríobh an litir / an ríomhphost (leathleathanach nó mar sin) a chuirfeá chuig cara leat ag insint dó / di faoi na trialacha '
              'agus faoi conas a d’éirigh leat iontu.'),
        ('ii', 'Fuair tú ceachtanna tiomána mar bhronntanas ó d’uncail / ó d’aintín.\n'
               'Scríobh an litir / an ríomhphost (leathleathanach nó mar sin) a chuirfeá chuige / chuici ag gabháil buíochais leis / léi '
               'agus ag insint dó / di conas a d’éirigh leat sa chéad cheacht.')]),
    'D': ('COMHRÁ', 'irish-2-9', None, [
        ('i', 'Tá plean agat árasán a fháil ar cíos sa chathair le do chairde an bhliain seo chugainn nuair a bheidh tú ar an gcoláiste '
              'tríú leibhéal.\n'
              'Scríobh an comhrá (leathleathanach nó mar sin) a bheadh agat le do thuismitheoirí faoi sin.'),
        ('ii', 'Ba mhaith leat dul ar saoire go dtí an Spáinn le do chairde tar éis na hArdteistiméireachta ach b’fhearr le do chara '
               'fanacht in Éirinn.\n'
               'Scríobh an comhrá (leathleathanach nó mar sin) a bheadh agat le do chara faoi sin.')]),
}
# Task checks: the 2021–2025 requirement lines (irish_lifted.printed_tasks gives each its printed sentence or English).
LISTENING_REQUIREMENTS = ['Éist leis an taifeadadh oifigiúil.', 'Freagair gach mír atá priontáilte ar an gcárta.']
COMPOSITION_REQUIREMENTS = ['Freagair do rogha dhá cheann de A, B, C, D anseo.', 'Lean an fhoirm scríbhneoireachta a iarrtar sa cheist.',
                            'Coinnigh ceangal cinnte leanúnach idir an teideal agus an t-ábhar.', 'Leathleathanach nó mar sin.']

_MATERIAL = None


def permitted_marks(chunk, marks):
    """The marks a question can take: 0, its full tariff, and every price its key prints for an answer: “=3 mharc”, the bare
    partial “Dún na nGall 1 mharc”, and the first term of a split “2 mharc + 1 mharc” (the first correct answer 2, both 3);
    the split's second term is the second answer's addition, never a mark on its own."""
    values = {0, marks} | {int(v) for v in re.findall(r'= ?(\d) mharc', chunk)} | {int(v) for v in re.findall(r'(?<![=+\d])\s(\d) mharc', chunk)}
    return sorted(v for v in values if v <= marks)


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
    texts = [clean(p.get_text()) for p in paper]
    stext = [clean(page_text(p)) for p in scheme]
    # The key runs PDF 11–13 (the transcript ends on PDF 10); every anchor below is printed once there.
    listening = Marked(scheme, 11, 13)

    def furniture(raw):
        # The next section's printed heading precedes the following question; it must not add a page.
        while True:
            trimmed = HEADINGS.sub('', re.sub(r'(\s*⟦\d+⟧\s*)+$', '', raw))
            if trimmed == raw:
                return raw
            raw = trimmed
    segments = [(key, suffix, ref, page, topic, list(qs)) for key, suffix, ref, page, topic, qs in SEGMENTS]
    questions = [q for seg in segments for q in seg[5]]
    assert len({q[3] for q in questions}) == len(questions)
    for q in questions:
        assert listening.text.count(q[3]) == 1, ('anchor not printed exactly once', q[3])
    # The 2013 key prints the questions in the paper's order, the Fógra a hAon grid first (PDF 11).
    ordered = sorted(questions, key=lambda q: listening.text.index(q[3]))
    assert ordered == questions, 'scheme key expected in the paper order'
    assert listening.text.index(GRID) < listening.text.index(ordered[0][3])
    cut = dict(zip([q[3] for q in ordered], listening.split([q[3] for q in ordered], 'Eolas (60) =', furniture)))
    for seg in segments:
        for i, (cid, label, prompt, anchor, marks) in enumerate(seg[5]):
            chunk, pages = cut[anchor]
            assert comparable(prompt) in comparable(texts[seg[3] - 1]), (seg[0], cid)
            # Every answer prints its price; the grid's second row prints only its split (“2 mharc + 1 mharc”).
            assert '3 mharc' in chunk or (seg[0], cid) == ('L-A-F1', 'g2') and chunk.endswith('2 mharc + 1 mharc'), (seg[0], cid, chunk[-60:])
            assert not re.search(r'Cuid [BC] \(|COMHRÁ|PÍOSA|FÓGRA|Téipscript', chunk), (seg[0], cid, chunk[-80:])
            seg[5][i] = (cid, label, prompt, chunk, pages, marks)
    assert sum(len(seg[5]) for seg in segments) == 20 and sum(q[5] for seg in segments for q in seg[5]) == 60
    assert comparable(GRID) in comparable(texts[2])
    # PDF 5 prices Cuid A and B “3 mharc × 4 = 12 mharc” for each extract and Cuid C “3 mharc × 2 = 6 mharc”; its Cuid C
    # line misprints the part's total as “20 marc (Eolas)” above the printed sum “6 + 6 = 12 mharc”.
    assert stext[4].count('3 mharc × 4 = 12 mharc') == 4 and stext[4].count('3 mharc × 2 = 6 mharc') == 2, stext[4][:300]
    assert 'Cuid C: Píosa 1: 20 marc (Eolas)' in stext[4] and '6 + 6 = 12 mharc 24 + 24 + 12 = 60' in stext[4]
    # The 2013 scheme prints no general listening note and the language deduction only on PDF 5 (and in the modified-marking
    # list, PDF 29).
    assert 'Níor chóir a mheas' not in ' '.join(stext[10:13]) and 'Bainfear ó 0 go 6 ar chaighdeán na Gaeilge.' in stext[4]
    assert 'Bainfear' not in ' '.join(stext[10:13])
    intro = {
        'A': 'Cloisfidh tú dhá fhógra raidió sa chuid seo. Cloisfidh tú gach fógra díobh faoi dhó. Beidh sos ann leis na freagraí a scríobh tar éis na chéad éisteachta agus tar éis an dara héisteacht.',
        'B': 'Cloisfidh tú dhá chomhrá sa chuid seo. Cloisfidh tú gach comhrá díobh faoi dhó. Cloisfidh tú an comhrá ó thosach deireadh an chéad uair. Ansin cloisfidh tú ina dhá mhír é. Beidh sos ann leis na freagraí a scríobh tar éis gach míre díobh.',
        'C': 'Cloisfidh tú dhá phíosa nuachta sa chuid seo. Cloisfidh tú gach píosa díobh faoi dhó. Beidh sos ann leis na freagraí a scríobh tar éis na chéad éisteachta agus tar éis an dara héisteacht.'}
    for part, page in [('A', 3), ('B', 4), ('C', 5)]:
        assert comparable(intro[part]) in comparable(texts[page - 1]), part

    # 2013: marking on PDF 14 in printed blocks (the tariffs; the bracketed Cumas Gaeilge definition, (i) Stór Gaeilge 40% and
    # (ii) beachtas 50% agus litriú 10%; the bracketed content note; the examiner's Nóta; and a bracketed Nóta on the “Gaeilge
    # Lochtach” of the questions that follow, i.e. Paper 2), no 40-mark table, no symbol page and no short-attempt columns.
    marking = stext[13][stext[13].index('Freagair do rogha dhá cheann'):]
    tariffs, rest = marking.split(' [Cumas Gaeilge = (i) ', 1)
    cumas, rest = rest.split(' [Gearrfar pionós', 1)
    content, rest = rest.split('] Nóta: ', 1)
    nota, lochtach = rest.split(' [Nóta: Maidir le', 1)
    tariffs, cumas = tariffs.strip(), '[Cumas Gaeilge = (i) ' + cumas.strip()
    content, nota = '[Gearrfar pionós' + content + ']', 'Nóta: ' + nota.strip()
    assert tariffs.endswith('Leathleathanach nó breis: Tasc = 2 mharc Ábhar = 8 marc = 50 marc × 2 Cumas Gaeilge = 40 marc = 100 marc'), tariffs
    assert cumas.endswith('(= 50%) agus litriú (= 10%).]') and '(= 40%)' in cumas, cumas[-60:]
    assert content == '[Gearrfar pionós ar iarrthóirí mura mbeidh na hiarrachtaí ceapadóireachta ad rem.]', content
    assert nota.endswith('ag bun na n-iarrachtaí ceapadóireachta.'), nota[-80:]
    # The last bracketed note defines “Gaeilge Lochtach” for the questions after it (Paper 2's deductions), not composition marking.
    assert lochtach.startswith(' ‘Gaeilge Lochtach’ a luaitear leis na ceisteanna ina dhiaidh seo') and lochtach.endswith('40% : 60%]'), lochtach[:80]
    smm = stext[28]
    assert smm.startswith('27 Scéim Mharcála Mhodhnaithe') and 'Páipéar 1:Ceist 2:An Cheapadóireacht –an measúnú ar Chumas Gaeilge as 40 marc.' in smm, smm[:400]
    # No 40-mark table and no modified-marking bands anywhere in the 2013 scheme (PDF 15 is Paper 2).
    assert '95%' not in ' '.join(stext) and '34-40' not in ' '.join(stext) and stext[14].startswith('13 Páipéar II')
    head = ('Treoracha d’iarrthóirí\n'
            'Ní mór do na hiarrthóirí cúram a dhéanamh de chruinneas na teanga. Caillfear marcanna má bhítear faillitheach ann. '
            'Ní mór ceangal cinnte leanúnach a bheith ann idir an teideal a roghnaítear agus an t-ábhar a scríobhtar.\n\n'
            'Freagair do rogha dhá cheann de A, B, C, D anseo.')
    assert all(comparable(line) in comparable(texts[5]) for line in head.split('\n\n')[0].splitlines())
    assert comparable(head.split('\n\n')[1]) in comparable(texts[6])
    for group, (form, _, instruction, titles) in GROUPS.items():
        assert comparable(f'{group} – {form} – (50 marc)') in comparable(texts[6]), group
        for roman, title in titles:
            for line in ([instruction] if instruction else []) + title.splitlines():
                assert comparable(line) in comparable(texts[6]), (group, roman, line[:40])
    _MATERIAL = dict(paper=paper, texts=texts, segments=segments, head=head, intro=intro,
                     composition=dict(tariffs=tariffs, cumas=cumas, content=content, nota=nota),
                     decisions=selection_decisions(paper))
    return _MATERIAL


def build():
    m = material()
    cards = []
    audio = dict(kind='source-audio', title=f'Triail Chluastuisceana {YEAR}', playbackUrl=AUDIO_URL, secFileid='LC001ZLP017IV.mp3',
                 canonicalUrl=AUDIO_URL, attribution='© State Examinations Commission.',
                 presentationNote='Play the official recording and use the section heading on this card to follow the correct part.')
    for key, suffix, ref, page, topic, questions in m['segments']:
        criteria = []
        for cid, label, prompt, chunk, pages, marks in questions:
            criteria.append(criterion(cid, label, marks, [chunk], 'exact', permitted=permitted_marks(chunk, marks)))
        pages = sorted({p for q in questions for p in q[4]})
        cards.append(dict(
            id=f'irish-{YEAR}-ol-p1-listening-{suffix}', year=YEAR, level='ordinary', paper=1, section='1',
            questionRef=f'{YEAR} OL Paper 1 Cluastuiscint {ref}', questionText=SEGMENT_TEXT[key](questions),
            totalMarks=sum(c['maxMarks'] for c in criteria), topicId=topic, conceptId=f'irish-listening-{suffix}',
            paperPage=page, schemePage=pages[0], taskRequirements=LISTENING_REQUIREMENTS, criteria=criteria,
            markingGuideNote=f'The listed responses and tariffs come from the {YEAR} SEC marking scheme; equivalent wording with the same meaning is accepted. '
                             'Each printed question is marked at its own published tariff (3 marks). ' + LANGUAGE,
            audioMaterial=dict(audio, label=ref), paperFileid=FILE, atlasQuestionId=key, reviewedAt=REVIEWED_AT,
            reviewedPaperPages=[page], schemeFileid=SCHEME_FILE, schemePages=pages, sourceMaterial=source(f'Cluastuiscint {ref}', [page])))
    c = m['composition']
    for group, (form, topic, instruction, titles) in GROUPS.items():
        for roman, title in titles:
            body = m['head'] + f'\n\n{group} · {form} (50 marc)\n' + (instruction + '\n' if instruction else '') + f'({roman}) {title}'
            cards.append(dict(
                id=f'irish-{YEAR}-ol-p1-composition-{group.lower()}-{roman}', year=YEAR, level='ordinary', paper=1, section='1',
                questionRef=f'{YEAR} OL Paper 1 Ceapadóireacht {group}({roman})', questionText=body, totalMarks=50, topicId=topic,
                conceptId=f'irish-composition-{group.lower()}', paperPage=7, schemePage=14, taskRequirements=COMPOSITION_REQUIREMENTS,
                # 2013 prints no headed Tasc/Ábhar sections: the tariff block prices the task, the bracketed note is the
                # scheme's content guidance, and the Cumas Gaeilge definition and the Nóta go with Gaeilge.
                criteria=[criterion('tasc', 'An Tasc', 2, [c['tariffs']], permitted=[0, 2]),
                          criterion('abhar', 'An tÁbhar', 8, [c['content']]),
                          # The definition and the Nóta are two printed blocks (the Ábhar note sits between them), kept as two
                          # lines: joined, the lift post-pass can read the seam as a run the scheme never prints and drop it.
                          criterion('gaeilge', 'An Cumas Gaeilge', 40, [c['cumas'], c['nota']])],
                markingGuideNote=f'Whole 50-mark composition: Tasc 2, Ábhar 8, Cumas Gaeilge 40. The {YEAR} scheme prints no 40-mark table: '
                                 'Cumas Gaeilge is judged on its printed aspects, (i) the range and richness of the candidate’s Irish (40%) and '
                                 '(ii) accuracy in the main features of correct Irish (50%) and spelling (10%), so the award can take any value from 0 to 40. '
                                 'Scéim Mharcála Mhodhnaithe (scheme PDF 29): for eligible candidates, spelling and certain grammar features are not '
                                 'penalised in this 40-mark assessment; the scheme prints no bands for it. '
                                 'The letter or email (C) and the dó/di, leis/léi wording are flexible forms inside one response, not separate routes.',
                paperFileid=FILE, atlasQuestionId=f'W-{group}-{roman}', reviewedAt=REVIEWED_AT, reviewedPaperPages=[6, 7],
                schemeFileid=SCHEME_FILE, schemePages=[14], sourceMaterial=source(f'Ceapadóireacht {group}({roman})', [6, 7])))
    assert len(cards) == 15 and len({x['id'] for x in cards}) == 15 and len({x['atlasQuestionId'] for x in cards}) == 15
    for card in cards:
        assert sum(cr['maxMarks'] for cr in card['criteria']) == card['totalMarks'], card['id']
        for cr in card['criteria']:
            assert cr['guidance'] and all(not PUA.search(g) and 'Siombailí' not in g for g in cr['guidance']), (card['id'], cr['id'])
    sr = json.loads(SOURCE_REVIEW.read_text())
    listening_ids = [x['id'] for x in cards if '-listening-' in x['id']]
    composition_ids = [x['id'] for x in cards if '-composition-' in x['id']]
    review = dict(year=YEAR, level='ordinary', paperFileid=FILE + '.pdf', schemeFileid=SCHEME_FILE + '.pdf',
                  paperSha256=PAPER_SHA, schemeSha256=SCHEME_SHA,
                  reviewedPaperPages=list(range(1, 9)), reviewedSchemePages=sr['reviewedSchemePages'], schemeScope=sr['schemeScope'],
                  reviewDate=REVIEWED_AT, status='reviewed', fullPaperAndApplicableSchemeVisualSweep=True, selectionDecisions=m['decisions'],
                  cardIds=listening_ids + composition_ids, listeningSegmentCardIds=listening_ids, compositionRouteCardIds=composition_ids,
                  printedListeningQuestions=20, examStructure=dict(listening=60, composition=100, total=160),
                  nonPoolDecisions=sr['nonPoolDecisions'], openIssues=[], audio=sr['audio'], caveats=sr['sourceFindings'],
                  choicePolicy='Choice is not a route: each printed composition title is one card carrying the printed choose-two instruction; no combination cards.',
                  boundaries='6 listening segment cards carrying all 20 printed questions as separate criteria, each at 3 (60); '
                             '9 composition titles at 50 (answer any two; no combination cards).')
    return dict(review=review, cards=cards)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    data = build()
    scheme_words_in(data)  # guidance, question and task checks carry the SEC's words only (irish_lifted.py)
    import fitz
    scheme = fitz.open(ROOT / f'paper-trail-corpus/markingschemes/{YEAR}/{SCHEME_FILE}.pdf')
    # The searchable scheme text the provenance checks read (as 2014, 2016, 2018, 2020 and 2026 write their own), with its
    # SymbolMT glyphs read as `page_text` reads them.
    scheme_md = f'# Gaeilge Gnáthleibhéal {YEAR} — SEC marking scheme (Páipéar 1 agus 2)\n\n' + '\n\n'.join(
        f'## PDF page {i + 1}\n\n' + page_text(p) for i, p in enumerate(scheme))
    outputs = {OUT: json.dumps(data, ensure_ascii=False, indent=2) + '\n',
               SCHEME_MD: '\n'.join(line.rstrip() for line in scheme_md.splitlines()).rstrip() + '\n'}
    for path, value in outputs.items():
        if args.check:
            assert path.exists() and path.read_text() == value, f'Stale output: {path}'
        else:
            path.write_text(value)
    print(f"Irish Ordinary {YEAR} Paper 1: {len(data['cards'])} reviewed cards (20 printed listening questions, 9 titles); the archive remains incomplete.")


if __name__ == '__main__':
    main()
