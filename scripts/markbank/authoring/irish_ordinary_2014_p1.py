#!/usr/bin/env python3
"""Reviewed 2014 Ordinary Paper 1 (Cluastuiscint agus Ceapadóireacht), carded new.

Paper PDF 1–8 (2014 prints no answer booklet: Cuid A on page 3, the composition
Treoracha on page 6, the titles on page 7, page 8 blank) and the Paper 1 pages of the
combined LC001GLP000IV scheme (PDF 1–11 and 24 modified marking) reviewed on
2026-11-05. Scheme PDF 12–23 belong to Paper 2; 25–27 are blank and 28 empty. Counts
are assertions, not corpus-completeness proof. Same layout and method as
irish_ordinary_2016_p1.py, with the differences the 2014 scheme prints: the key (PDF
8–10) prints the Fógra a hAon grid above Fógra a Dó, but its text layer gives Fógra a
Dó's four questions first; the grid's answers carry no “=” (“(Raidió na) Gaeltachta
3 mharc”), its fourth row prints its parts' prices under the answer (“061 (1 mharc) +
92917 (2 mharc)”), Fógra a Dó 1(b) prints its tariff at the right of its answer's line,
and Cuid C's answers carry no price of their own (“3 mharc Fiche nó 20”); and the
composition marking (PDF 11) prints Cumas Gaeilge as
(i) Stór Gaeilge 40% and (ii) beachtas 50% agus litriú 10%, no 40-mark table, and a
modified-marking page (PDF 24) with no bands.

No 2014 Ordinary card existed before. `build` cards the component the way the reviewed
2016–2025 Ordinary Paper 1s are carded: six listening segment cards (the Bank plays
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
YEAR = 2014
FILE = 'LC001GLP100IV'
SCHEME_FILE = 'LC001GLP000IV'
OUT = ROOT / 'components/MarkBank/cards/irish/ordinary-2014-p1-authored.json'
SCHEME_MD = ROOT / f'examiner-reports/irish/schemes/{YEAR}-ol.md'
SOURCE_REVIEW = ROOT / 'scripts/markbank/authored/irish-ordinary-2014-p1-source-review.json'
REVIEWED_AT = '2026-11-05'
PAPER_SHA = '37170c1852ae17aac6b07c2fde02be38e18b3ccce1972afbcc656f91844bad3c'
SCHEME_SHA = 'c81408cfd36cef0f7ae4633e06a546ef0d23ea1ad2ded33a519c61c02dd5b09a'
AUDIO_URL = 'https://www.examinations.ie/archive/exampapers/2014/LC001ZLP017IV.mp3'
DIRECTIVE = re.compile(r'rogha|roghna|Freagair|Cuir tic|Ainmnigh|Luaigh|\bnó\b|dhá phointe|dhá rud|dó/di|ceann amháin|amháin|\bdhá\b', re.I)
SOURCE_NOTE = 'Shown page-for-page from the official examination paper; swipe to move between pages.'
LANGUAGE = ('Scheme PDF 4: “Bainfear ó 0 go 6 ar chaighdeán na Gaeilge.” This 0–6 deduction applies once to the whole '
            'listening section (Tuiscint 60 − Cumas Gaeilge 0–6), never inside a single question.')
HEADINGS = re.compile(r'\s*(FÓGRA A DÓ \(12 mharc\)|Cuid B \(24 marc\) COMHRÁ A hAON \(12 mharc\) An Chéad Mhír|An Dara Mír|'
                      r'COMHRÁ A DÓ \(12 mharc\) An Chéad Mhír|Cuid C \(12 mharc\) PÍOSA A hAON \(6 mharc\)|PÍOSA A DÓ \(6 mharc\))\s*$')
# The scheme's text layer gives its SymbolMT glyphs as Latin letters: the multiplication sign of the tariff page (PDF 4) as
# “u” and the answer bullets (Paper 2) as “x”; Adobe Symbol draws them as × and •.
SYMBOL_FONT = {'u': '×', 'x': '•', ' ': ' '}


def clean(text):
    return re.sub(r'\s+', ' ', symbol_text(text)).strip()


def comparable(text):
    return re.sub(r'[^\w]+', '', text.lower())


def page_text(page):
    """The page's text with each SymbolMT glyph as the character it draws (every glyph is one SYMBOL_FONT reviewed) and each
    Calibri glyph-3 space as a space."""
    lines = []
    for block in page.get_text('dict')['blocks']:
        for line in block.get('lines', []):
            parts = []
            for span in line['spans']:
                text = span['text']
                if span['font'] == 'SymbolMT':
                    assert all(c in SYMBOL_FONT for c in text), ('Unreviewed scheme glyph', page.number + 1, repr(text))
                    text = ''.join(SYMBOL_FONT[c] for c in text)
                # Calibri draws a space as glyph 3, which the text layer gives as U+0003 (PDF 13 “Is\x03i nGaeltacht”).
                text = text.replace('\x03', ' ')
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
        # A grid ("Líon isteach an t-eolas atá á lorg sa ghreille anseo."): four unnumbered printed questions.
        ('g1', 'Greille 1', 'Cén stáisiún raidió atá luaite san fhógra?', 'Cén stáisiún raidió atá luaite', 3),
        ('g2', 'Greille 2', 'Cén Ollscoil atá ag lorg rúnaí?', 'Cén Ollscoil atá ag lorg rúnaí', 3),
        ('g3', 'Greille 3', 'Cé mhéad lá de laethanta saoire a bheidh le fáil?', 'Cé mhéad lá de laethanta saoire', 3),
        ('g4', 'Greille 4', 'Cén uimhir theileafóin atá ag an Ollscoil?', 'Cén uimhir theileafóin', 3)]),
    ('L-A-F2', 'a-f2', 'Cuid A · Fógra a Dó', 3, 'irish-1-0', [
        ('q1a', 'Ceist 1(a)', 'Cathain a thosóidh Sceideal Spóirt an tSamhraidh ar TG4?', '1. (a) Cathain a thosóidh', 3),
        ('q1b', 'Ceist 1(b)', 'Cén t-ainm a bheidh ar an gclár speisialta a chraolfar ar leathuair tar éis a sé?', '(b) Cén t-ainm a bheidh ar an gclár', 3),
        ('q2a', 'Ceist 2(a)', 'Cén comórtas a imreofar in Wimbledon?', '2. (a) Cén comórtas', 3),
        ('q2b', 'Ceist 2(b)', 'Cén t-am a thosóidh an craoladh beo as Wimbledon gach lá?', '(b) Cén t-am a thosóidh', 3)]),
    ('L-B-C1', 'b-c1', 'Cuid B · Comhrá a hAon', 4, 'irish-1-1', [
        ('m1-q1', 'An Chéad Mhír · Ceist 1', 'Cén scrúdú cainte a bhí ag Áine inniu?', '1. Cén scrúdú cainte', 3),
        ('m1-q2', 'An Chéad Mhír · Ceist 2', 'Luaigh rud amháin a deir Áine faoin scrúdaitheoir.', '2. Luaigh rud amháin a deir Áine', 3),
        ('m2-q1', 'An Dara Mír · Ceist 1', 'Cathain a bheidh iPad ag na daltaí sa chéad bhliain i scoil Áine?', '1. Cathain a bheidh iPad', 3),
        ('m2-q2', 'An Dara Mír · Ceist 2', 'Cad atá le críochnú ag Pól roimh an lá amárach?', '2. Cad atá le críochnú', 3)]),
    ('L-B-C2', 'b-c2', 'Cuid B · Comhrá a Dó', 4, 'irish-1-1', [
        ('m1-q1', 'An Chéad Mhír · Ceist 1', 'Cathain a bhí Oíche na nGradam ar siúl sa scoil?', '1. Cathain a bhí Oíche na nGradam', 3),
        ('m1-q2', 'An Chéad Mhír · Ceist 2', 'Cén post a bhí ag Seán ar Chomhairle na Mac Léinn?', '2. Cén post a bhí ag Seán', 3),
        ('m2-q1', 'An Dara Mír · Ceist 1', 'Cén lá a bhíodh an lón sláintiúil acu sa cheaintín?', '1. Cén lá a bhíodh an lón', 3),
        ('m2-q2', 'An Dara Mír · Ceist 2', 'Cad a tugadh do gach scoláire sular imíodar ar saoire don samhradh?', '2. Cad a tugadh do gach scoláire', 3)]),
    ('L-C-P1', 'c-p1', 'Cuid C · Píosa a hAon', 5, 'irish-1-2', [
        ('q1', 'Ceist 1', 'Cé mhéad bliain atá Raidió na Life ar an aer?', '1. Cé mhéad bliain atá Raidió', 3),
        ('q2', 'Ceist 2', 'Scríobh síos saghas amháin cláir a chraoltar ar Raidió na Life.', '2. Scríobh síos saghas amháin cláir', 3)]),
    ('L-C-P2', 'c-p2', 'Cuid C · Píosa a Dó', 5, 'irish-1-2', [
        ('q1', 'Ceist 1', 'Cá fhad a chaithfidh na mic léinn ar na hOileáin Fhilipíneacha?', '1. Cá fhad a chaithfidh', 3),
        ('q2', 'Ceist 2', 'Cé mhéad airgid atá le tabhairt acu don obair thógála?', '2. Cé mhéad airgid', 3)]),
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
        ('i', 'An tír is fearr liom.'), ('ii', 'Mo chairde.'), ('iii', 'Is aoibhinn liom an ceol.')]),
    'B': ('SCÉAL', 'irish-2-3', 'Ceap scéal (leathleathanach nó mar sin) a mbeidh ceann amháin de na sleachta seo a leanas oiriúnach mar thús leis.', [
        ('i', 'Bhí mé féin agus mo chara ag siúl sna sléibhte. Go tobann, thit ceo trom timpeall orainn. Bhíomar i dtrioblóid …'),
        ('ii', 'Bhí mé amuigh ag rith. Bhuail mé le mo chara. Bhí fearg an domhain air / uirthi …')]),
    'C': ('LITIR / RÍOMHPHOST', 'irish-2-8', None, [
        ('i', 'Bhí tú ar fhoireann na scoile a bhuaigh cluiche mór le déanaí.\n'
              'Scríobh an litir / an ríomhphost (leathleathanach nó mar sin) a chuirfeá chuig cara leat ag insint dó / di faoin gcluiche '
              'agus faoin gcóisir (faoin bhféasta) a bhí agaibh i ndiaidh an chluiche.'),
        ('ii', 'Tá an Ardteistiméireacht críochnaithe agat agus tá tú ag fágáil na scoile.\n'
               'Scríobh an litir / an ríomhphost (leathleathanach nó mar sin) a chuirfeá chuig an bpríomhoide ag gabháil buíochais leis / léi '
               'agus ag déanamh cur síos ar an am a chaith tú sa scoil.')]),
    'D': ('COMHRÁ', 'irish-2-9', None, [
        ('i', 'Ceapann do thuismitheoirí go gcaitheann tú an iomarca ama ar Facebook.\n'
              'Tá siad míshásta leat mar níl tú ag déanamh staidéir don Ardteistiméireacht.\n'
              'Scríobh an comhrá (leathleathanach nó mar sin) a bheadh agat le do thuismitheoirí faoi sin.'),
        ('ii', 'Bhí tú féin agus do chara ag comhrá le chéile faoi chlár teilifíse.\n'
               'Thaitin an clár teilifíse leat ach níor thaitin sé le do chara.\n'
               'Scríobh an comhrá (leathleathanach nó mar sin) a bheadh agat le do chara faoi sin.')]),
}
# Task checks: the 2021–2025 requirement lines (irish_lifted.printed_tasks gives each its printed sentence or English).
LISTENING_REQUIREMENTS = ['Éist leis an taifeadadh oifigiúil.', 'Freagair gach mír atá priontáilte ar an gcárta.']
COMPOSITION_REQUIREMENTS = ['Freagair do rogha dhá cheann de A, B, C, D anseo.', 'Lean an fhoirm scríbhneoireachta a iarrtar sa cheist.',
                            'Coinnigh ceangal cinnte leanúnach idir an teideal agus an t-ábhar.', 'Leathleathanach nó mar sin.']

_MATERIAL = None


def permitted_marks(chunk, marks):
    """The marks a question can take: 0, its full tariff, and every price its key prints for an answer, “= 2 mharc” or
    the grid's “061 (1 mharc) + 92917 (2 mharc)”."""
    values = {0, marks} | {int(v) for v in re.findall(r'= ?(\d) mharc', chunk)} | {int(v) for v in re.findall(r'\((\d) mharc\)', chunk)}
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
    # The key runs PDF 8–10 (PDF 8 opens with the end of the Cuid C transcript); every anchor below is printed once there.
    listening = Marked(scheme, 8, 10)

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
    # The 2014 key's text layer gives Fógra a Dó's four questions before the Fógra a hAon grid's (PDF 8; the page prints the grid
    # above them), then the paper's order.
    ordered = sorted(questions, key=lambda q: listening.text.index(q[3]))
    assert [q[3] for q in ordered[:8]] == [q[3] for q in segments[1][5] + segments[0][5]], 'expected Fógra a Dó, then the grid'
    assert ordered[8:] == [q for seg in segments[2:] for q in seg[5]], 'scheme key expected in the paper order after Cuid A'
    assert listening.text.index(GRID) < listening.text.index(ordered[0][3])
    cut = dict(zip([q[3] for q in ordered], listening.split([q[3] for q in ordered], 'Eolas (60) =', furniture)))
    for seg in segments:
        for i, (cid, label, prompt, anchor, marks) in enumerate(seg[5]):
            chunk, pages = cut[anchor]
            assert comparable(prompt) in comparable(texts[seg[3] - 1]), (seg[0], cid)
            assert '3 mharc' in chunk, (seg[0], cid, chunk[-60:])
            assert not re.search(r'Cuid [BC] \(|COMHRÁ|PÍOSA|FÓGRA|Téipscript', chunk), (seg[0], cid, chunk[-80:])
            seg[5][i] = (cid, label, prompt, chunk, pages, marks)
    assert sum(len(seg[5]) for seg in segments) == 20 and sum(q[5] for seg in segments for q in seg[5]) == 60
    assert comparable(GRID) in comparable(texts[2])
    # PDF 4 prices Cuid A and B “3 mharc × 4 = 12 mharc” for each extract and Cuid C “3 mharc × 2 = 6 mharc”.
    assert stext[3].count('3 mharc × 4 = 12 mharc') == 4 and stext[3].count('3 mharc × 2 = 6 mharc') == 2, stext[3][:300]
    # The 2014 scheme prints no general listening note and the language deduction only on PDF 4.
    assert 'Níor chóir a mheas' not in ' '.join(stext[7:10]) and 'Bainfear ó 0 go 6 ar chaighdeán na Gaeilge.' in stext[3]
    assert 'Bainfear' not in ' '.join(stext[7:10])
    intro = {
        'A': 'Cloisfidh tú dhá fhógra raidió sa chuid seo. Cloisfidh tú gach fógra díobh faoi dhó. Beidh sos ann leis na freagraí a scríobh tar éis na chéad éisteachta agus tar éis an dara héisteacht.',
        'B': 'Cloisfidh tú dhá chomhrá sa chuid seo. Cloisfidh tú gach comhrá díobh faoi dhó. Cloisfidh tú an comhrá ó thosach deireadh an chéad uair. Ansin cloisfidh tú ina dhá mhír é. Beidh sos ann leis na freagraí a scríobh tar éis gach míre díobh.',
        'C': 'Cloisfidh tú dhá phíosa nuachta sa chuid seo. Cloisfidh tú gach píosa díobh faoi dhó. Beidh sos ann leis na freagraí a scríobh tar éis na chéad éisteachta agus tar éis an dara héisteacht.'}
    for part, page in [('A', 3), ('B', 4), ('C', 5)]:
        assert comparable(intro[part]) in comparable(texts[page - 1]), part

    # 2014: marking on PDF 11 in printed blocks (the tariffs; the Cumas Gaeilge definition, (i) Stór Gaeilge 40% and (ii)
    # beachtas 50% agus litriú 10%; the bracketed content note; the examiner's Nóta; and a bracketed Nóta on the “Gaeilge
    # Lochtach” of the questions that follow, i.e. Paper 2), no 40-mark table, no symbol page and no short-attempt columns.
    marking = stext[10][stext[10].index('Freagair do rogha dhá cheann'):]
    tariffs, rest = marking.split(' Cumas Gaeilge = (i) ', 1)
    cumas, rest = rest.split(' [Gearrfar pionós', 1)
    content, rest = rest.split('] Nóta: ', 1)
    nota, lochtach = rest.split(' [Nóta: Maidir le', 1)
    tariffs, cumas = tariffs.strip(), 'Cumas Gaeilge = (i) ' + cumas.strip()
    content, nota = '[Gearrfar pionós' + content + ']', 'Nóta: ' + nota.strip()
    assert tariffs.endswith('Leathleathanach nó breis: Tasc = 2 mharc Ábhar = 8 marc = 50 marc x 2 Cumas Gaeilge = 40 marc = 100 marc'), tariffs
    assert cumas.endswith('(= 50%) agus litriú (= 10%).') and '(= 40%)' in cumas, cumas[-60:]
    assert content == '[Gearrfar pionós ar iarrachtaí ceapadóireachta nach bhfuil ad rem.]', content
    assert nota.endswith('ag bun na n-iarrachtaí ceapadóireachta.'), nota[-80:]
    # The last bracketed note defines “Gaeilge Lochtach” for the questions after it (Paper 2's deductions), not composition marking.
    assert lochtach.startswith(' ‘Gaeilge Lochtach’ a luaitear leis na ceisteanna ina dhiaidh seo') and lochtach.endswith('40% : 60%]'), lochtach[:80]
    smm = stext[23]
    assert smm.startswith('22 Scéim Mharcála Mhodhnaithe') and 'Páipéar 1: Ceist 2: An Cheapadóireacht - an measúnú ar Chumas Gaeilge as 40 marc.' in smm
    # No 40-mark table and no modified-marking bands anywhere in the 2014 scheme (PDF 12 is Paper 2).
    assert '95%' not in ' '.join(stext) and '34-40' not in ' '.join(stext) and stext[11].startswith('10 Páipéar II')
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
                conceptId=f'irish-composition-{group.lower()}', paperPage=7, schemePage=11, taskRequirements=COMPOSITION_REQUIREMENTS,
                # 2014 prints no headed Tasc/Ábhar sections: the tariff block prices the task, the bracketed note is the
                # scheme's content guidance, and the Cumas Gaeilge definition and the Nóta go with Gaeilge.
                criteria=[criterion('tasc', 'An Tasc', 2, [c['tariffs']], permitted=[0, 2]),
                          criterion('abhar', 'An tÁbhar', 8, [c['content']]),
                          # The definition and the Nóta are two printed blocks (the Ábhar note sits between them), kept as two
                          # lines: joined, the lift post-pass can read the seam as a run the scheme never prints and drop it.
                          criterion('gaeilge', 'An Cumas Gaeilge', 40, [c['cumas'], c['nota']])],
                markingGuideNote=f'Whole 50-mark composition: Tasc 2, Ábhar 8, Cumas Gaeilge 40. The {YEAR} scheme prints no 40-mark table: '
                                 'Cumas Gaeilge is judged on its printed aspects, (i) the range and richness of the candidate’s Irish (40%) and '
                                 '(ii) accuracy in the main features of correct Irish (50%) and spelling (10%), so the award can take any value from 0 to 40. '
                                 'Scéim Mharcála Mhodhnaithe (scheme PDF 24): for eligible candidates, spelling and certain grammar features are not '
                                 'penalised in this 40-mark assessment; the scheme prints no bands for it. '
                                 'The letter or email (C) and the dó/di, leis/léi wording are flexible forms inside one response, not separate routes.',
                paperFileid=FILE, atlasQuestionId=f'W-{group}-{roman}', reviewedAt=REVIEWED_AT, reviewedPaperPages=[6, 7],
                schemeFileid=SCHEME_FILE, schemePages=[11], sourceMaterial=source(f'Ceapadóireacht {group}({roman})', [6, 7])))
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
    # The searchable scheme text the provenance checks read (as 2016, 2018, 2020 and 2026 write their own), with its
    # SymbolMT glyphs and Calibri glyph-3 spaces read as `page_text` reads them.
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
