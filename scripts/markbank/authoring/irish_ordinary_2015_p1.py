#!/usr/bin/env python3
"""Reviewed 2015 Ordinary Paper 1 (Cluastuiscint agus Ceapadóireacht), carded new.

Paper PDF 1–8 (2015 prints no answer booklet: Cuid A on page 3, the composition
Treoracha on page 6, the titles on page 7, page 8 blank) and the Paper 1 pages of the
combined LC001GLP000IV scheme (PDF 1–11 and 21 modified marking) reviewed on
2026-11-05. Scheme PDF 12–21 belong to Paper 2 (its last Nóta tops PDF 21); 22–24 are
blank. Counts are assertions, not corpus-completeness proof. Same method as
irish_ordinary_2016_p1.py, with the differences the 2015 scheme prints: the listening
tariffs and the only print of the 0–6 language deduction are on PDF 4; the transcript
runs PDF 5–7 and the key PDF 8–10, in the paper's order (the Fógra a hAon grid first);
Fógra a Dó prints four 3-mark questions (1(a), 1(b), 2(a), 2(b)); Comhrá a hAon An Dara
Mír 2 ends on its printed rule for a half answer (“… bronn 2 mharc air”), not on a
price; the composition marking (PDF 11) prints the (i) Cumas Gaeilge and (ii) Beachtas
definitions in the ratio 40% : 60%, a bracketed content note without “leanúnach”, and no
40-mark table; and the modified-marking page (PDF 21) prints no 40-mark bands.

No 2015 Ordinary card existed before. `build` cards the component the way the reviewed
2016–2025 Ordinary Paper 1s are carded: six listening segment cards (the Bank plays
one recording section as one exercise), each printed question its own 3-mark
criterion with its lifted scheme slice, and the nine printed composition titles as
50-mark cards. “Freagair do rogha dhá cheann de A, B, C, D” is a choice, not a route:
each title is its own card and carries the printed instruction as its task check; no
two-section combination cards. `main` writes the card file.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import re
from pathlib import Path
from irish_lifted import PUA, scheme_words_in, symbol_text

ROOT = Path(__file__).resolve().parents[3]
YEAR = 2015
FILE = 'LC001GLP100IV'
SCHEME_FILE = 'LC001GLP000IV'
OUT = ROOT / 'components/MarkBank/cards/irish/ordinary-2015-p1-authored.json'
SCHEME_MD = ROOT / f'examiner-reports/irish/schemes/{YEAR}-ol.md'
SOURCE_REVIEW = ROOT / 'scripts/markbank/authored/irish-ordinary-2015-p1-source-review.json'
REVIEWED_AT = '2026-11-05'
PAPER_SHA = '51f754e68f480d6e3c6931987462b73e9b9e868a7a25ff25f1c714f3d1e259c5'
SCHEME_SHA = '48dda60cd9b804a0c7b41dc8e265a05835fff88c9e8dc8564f084fbfe173621d'
AUDIO_URL = 'https://www.examinations.ie/archive/exampapers/2015/LC001ZLP017IV.mp3'
DIRECTIVE = re.compile(r'rogha|roghna|Freagair|Cuir tic|Ainmnigh|Luaigh|\bnó\b|dhá phointe|dhá rud|dó/di|ceann amháin|amháin|\bdhá\b', re.I)
SOURCE_NOTE = 'Shown page-for-page from the official examination paper; swipe to move between pages.'
LANGUAGE = ('Scheme PDF 4: “Bainfear ó 0 go 6 ar chaighdeán na Gaeilge.” This 0–6 deduction applies once to the whole '
            'listening section (Tuiscint 60 − Cumas Gaeilge 0–6), never inside a single question.')
HEADINGS = re.compile(r'\s*(FÓGRA A DÓ \(12 mharc\)|Cuid B \(24 marc\) COMHRÁ A hAON \(12 mharc\) An Chéad Mhír|An Dara Mír|'
                      r'COMHRÁ A DÓ \(12 mharc\) An Chéad Mhír|Cuid C \(12 mharc\) PÍOSA A hAON \(6 mharc\)|PÍOSA A DÓ \(6 mharc\))\s*$')


def clean(text):
    return re.sub(r'\s+', ' ', symbol_text(text)).strip()


def comparable(text):
    return re.sub(r'[^\w]+', '', text.lower())


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
            self.text += f' ⟦{p}⟧ ' + re.sub(r'^\d+\s', '', clean(doc[p - 1].get_text()))

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
        ('g1', 'Greille 1', 'Cén t-ainm a bheidh ar an gclár nua ar Raidió Fáilte?', 'Cén t-ainm a bheidh ar an gclár nua', 3),
        ('g2', 'Greille 2', 'Cén tráthnóna a bheidh an clár nua ar siúl?', 'Cén tráthnóna a bheidh an clár nua', 3),
        ('g3', 'Greille 3', 'Cén saghas ceoil a bheidh le cloisteáil ar an gclár nua?', 'Cén saghas ceoil a bheidh le cloisteáil', 3),
        ('g4', 'Greille 4', 'Luaigh ceann amháin de na duaiseanna a bhronnfar.', 'Luaigh ceann amháin de na duaiseanna', 3)]),
    ('L-A-F2', 'a-f2', 'Cuid A · Fógra a Dó', 3, 'irish-1-0', [
        ('q1a', 'Ceist 1(a)', 'Cá fhad a mhairfidh an cúrsa seo?', '1. (a) Cá fhad a mhairfidh', 3),
        ('q1b', 'Ceist 1(b)', 'Cén contae ina bhfuil Gleann Cholm Cille?', '(b) Cén contae ina bhfuil', 3),
        ('q2a', 'Ceist 2(a)', 'Cén mhí a bheidh an cúrsa seo ag tosú?', '2. (a) Cén mhí a bheidh an cúrsa', 3),
        ('q2b', 'Ceist 2(b)', 'Cén costas a bheidh ar an gcúrsa seo?', '(b) Cén costas a bheidh', 3)]),
    ('L-B-C1', 'b-c1', 'Cuid B · Comhrá a hAon', 4, 'irish-1-1', [
        ('m1-q1', 'An Chéad Mhír · Ceist 1', 'Cathain a fuair scoil Dhónaill an Bhratach Ghlas?', '1. Cathain a fuair scoil Dhónaill', 3),
        ('m1-q2', 'An Chéad Mhír · Ceist 2', 'Cé a bhí ar an gCoiste Glas i scoil Dhónaill?', '2. Cé a bhí ar an gCoiste Glas', 3),
        ('m2-q1', 'An Dara Mír · Ceist 1', 'Scríobh síos rud amháin a athchúrsáladh i scoil Dhónaill.', '1. Scríobh síos rud amháin a athchúrsáladh', 3),
        ('m2-q2', 'An Dara Mír · Ceist 2', 'Cad a bheidh an Coiste Glas i scoil Dhónaill ag iarraidh a shábháil an bhliain seo chugainn?', '2. Cad a bheidh an Coiste Glas', 3)]),
    ('L-B-C2', 'b-c2', 'Cuid B · Comhrá a Dó', 4, 'irish-1-1', [
        ('m1-q1', 'An Chéad Mhír · Ceist 1', 'Cá raibh Orla ar saoire an samhradh seo?', '1. Cá raibh Orla ar saoire', 3),
        ('m1-q2', 'An Chéad Mhír · Ceist 2', 'Cén fáth ar fhág uncail Orla Éire sna hochtóidí?', '2. Cén fáth ar fhág uncail Orla', 3),
        ('m2-q1', 'An Dara Mír · Ceist 1', 'Cén obair a bhí ar siúl ag Seán in Éirinn?', '1. Cén obair a bhí ar siúl ag Seán', 3),
        ('m2-q2', 'An Dara Mír · Ceist 2', 'Cé mhéad páiste atá ag uncail Orla?', '2. Cé mhéad páiste', 3)]),
    ('L-C-P1', 'c-p1', 'Cuid C · Píosa a hAon', 5, 'irish-1-2', [
        ('q1', 'Ceist 1', 'Cá háit i gConamara a bhfuil Teach an Phiarsaigh?', '1. Cá háit i gConamara', 3),
        ('q2', 'Ceist 2', 'Cad iad na huaireanta a bhíonn Teach an Phiarsaigh ar oscailt i rith an tsamhraidh?', '2. Cad iad na huaireanta', 3)]),
    ('L-C-P2', 'c-p2', 'Cuid C · Píosa a Dó', 5, 'irish-1-2', [
        ('q1', 'Ceist 1', 'Cén mhí a thosaigh an tseirbhís nuachta trí Ghaeilge ar líne?', '1. Cén mhí a thosaigh an tseirbhís', 3),
        ('q2', 'Ceist 2', 'Scríobh síos saghas amháin scéil atá le fáil ar an tseirbhís nuachta seo.', '2. Scríobh síos saghas amháin scéil', 3)]),
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
        ('i', 'Breithlá iontach a bhí agam.'), ('ii', 'Pearsa spóirt a thaitníonn go mór liom.'), ('iii', 'Rudaí a chuireann áthas orm.')]),
    'B': ('SCÉAL', 'irish-2-3', 'Ceap scéal (leathleathanach nó mar sin) a mbeidh ceann amháin de na sleachta seo a leanas oiriúnach mar thús leis.', [
        ('i', 'D’fhéach mé ar m’fhón póca. Léigh mé an téacs ó mo chara. Níor chreid mé mo shúile …'),
        ('ii', 'Bhí mé ag tiomáint síos an bóthar. Stop na gardaí mé. Bhí mé i dtrioblóid ...')]),
    'C': ('LITIR / RÍOMHPHOST', 'irish-2-8', None, [
        ('i', 'Tá tú díreach tar éis teacht abhaile ón ospidéal.\n'
              'Scríobh an litir / an ríomhphost (leathleathanach nó mar sin) a chuirfeá chuig cara leat ag insint dó / di cén fáth a raibh tú san ospidéal agus ag cur síos ar an am a chaith tú san ospidéal.'),
        ('ii', 'Bhí tú ag ceolchoirm le déanaí.\n'
               'Scríobh an litir / an ríomhphost (leathleathanach nó mar sin) a chuirfeá chuig cara leat ag insint dó / di faoi na hullmhúcháin a rinne tú roimh an gceolchoirm agus faoi na rudaí a tharla ag an gceolchoirm.')]),
    'D': ('COMHRÁ', 'irish-2-9', None, [
        ('i', 'Tá torthaí na hArdteistiméireachta díreach faighte agat. Tá do thuismitheoirí sásta le do thorthaí.\n'
              'Scríobh an comhrá (leathleathanach nó mar sin) a bheadh agat le do thuismitheoirí faoi sin.'),
        ('ii', 'Tá an scoil díreach oscailte tar éis laethanta saoire an tsamhraidh. Buaileann tú le cara leat nach bhfaca tú i rith an tsamhraidh.\n'
               'Scríobh an comhrá (leathleathanach nó mar sin) a bheadh agat le do chara faoi laethanta saoire an tsamhraidh.')]),
}
# Task checks: the 2021–2025 requirement lines (irish_lifted.printed_tasks gives each its printed sentence or English).
LISTENING_REQUIREMENTS = ['Éist leis an taifeadadh oifigiúil.', 'Freagair gach mír atá priontáilte ar an gcárta.']
COMPOSITION_REQUIREMENTS = ['Freagair do rogha dhá cheann de A, B, C, D anseo.', 'Lean an fhoirm scríbhneoireachta a iarrtar sa cheist.',
                            'Coinnigh ceangal cinnte leanúnach idir an teideal agus an t-ábhar.', 'Leathleathanach nó mar sin.']

_MATERIAL = None


def permitted_marks(chunk, marks):
    """The marks a question can take: 0, its full tariff, and every price its key prints, including the price its
    printed rule gives a half answer (“Ceann amháin den dá rud … i gceart, bronn 2 mharc air”)."""
    values = {0, 3} | {int(v) for v in re.findall(r'= ?(\d) mharc', chunk)} | {int(v) for v in re.findall(r'(?<![=\d])\s(\d) mharc', chunk)}
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
    stext = [clean(p.get_text()) for p in scheme]
    # The key runs PDF 8–10 after the transcript (PDF 5–7); every anchor below is printed once in PDF 8–10.
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
    # 2015 prints the key in the paper's order (the Fógra a hAon grid first, on PDF 8); the key ends where the
    # scheme's mark-total boxes begin.
    ordered = sorted(questions, key=lambda q: listening.text.index(q[3]))
    assert ordered == questions, 'scheme key expected in the paper order'
    assert listening.text.index(GRID) < listening.text.index(questions[0][3])
    cut = dict(zip([q[3] for q in ordered], listening.split([q[3] for q in ordered], 'Eolas (60) = Gaeilge (0-6) = Móriomlán (60) =', furniture)))
    for seg in segments:
        for i, (cid, label, prompt, anchor, marks) in enumerate(seg[5]):
            chunk, pages = cut[anchor]
            assert comparable(prompt) in comparable(texts[seg[3] - 1]), (seg[0], cid)
            # Every key ends on a price, except Comhrá a hAon An Dara Mír 2, whose rule for a half answer ends it
            # (“Ceann amháin den dá rud (leictreachas nó teas) i gceart, bronn 2 mharc air”).
            assert re.search(r'mharc$', chunk) or chunk.endswith('bronn 2 mharc air'), (seg[0], cid, chunk[-60:])
            assert '3 mharc' in chunk and marks == 3, (seg[0], cid)
            assert not re.search(r'Cuid [BC] \(|COMHRÁ|PÍOSA|FÓGRA|Téipscript', chunk), (seg[0], cid, chunk[-80:])
            seg[5][i] = (cid, label, prompt, chunk, pages, marks)
    assert sum(len(seg[5]) for seg in segments) == 20 and sum(q[5] for seg in segments for q in seg[5]) == 60
    assert comparable(GRID) in comparable(texts[2])
    # PDF 4 prices every section "3 mharc × N"; the 0–6 language deduction is printed there and nowhere in the key.
    assert re.search(r'Fógra 2: 3 mharc × 4 = 12 mharc', stext[3]), stext[3][:200]
    assert 'Níor chóir a mheas' not in ' '.join(stext[7:10]) and 'Bainfear ó 0 go 6 ar chaighdeán na Gaeilge.' in stext[3]
    assert 'Bainfear' not in ' '.join(stext[7:10])
    intro = {
        'A': 'Cloisfidh tú dhá fhógra raidió sa chuid seo. Cloisfidh tú gach fógra díobh faoi dhó. Beidh sos ann leis na freagraí a scríobh tar éis na chéad éisteachta agus tar éis an dara héisteacht.',
        'B': 'Cloisfidh tú dhá chomhrá sa chuid seo. Cloisfidh tú gach comhrá díobh faoi dhó. Cloisfidh tú an comhrá ó thosach deireadh an chéad uair. Ansin cloisfidh tú ina dhá mhír é. Beidh sos ann leis na freagraí a scríobh tar éis gach míre díobh.',
        'C': 'Cloisfidh tú dhá phíosa nuachta sa chuid seo. Cloisfidh tú gach píosa díobh faoi dhó. Beidh sos ann leis na freagraí a scríobh tar éis na chéad éisteachta agus tar éis an dara héisteacht.'}
    for part, page in [('A', 3), ('B', 4), ('C', 5)]:
        assert comparable(intro[part]) in comparable(texts[page - 1]), part

    # 2015: marking on PDF 11 in four printed blocks (tariffs; the (i) Cumas Gaeilge / (ii) Beachtas definitions with their
    # 40% : 60% ratio; the bracketed content note; the examiner's Nóta), no 40-mark table, no symbol page and no
    # short-attempt columns. The marking text ends where the printed score boxes begin.
    marking = stext[10][stext[10].index('Freagair do rogha dhá cheann'):].split('T (Tasc) (2) = Á (Ábhar) (8) = G (Gaeilge) (40) =', 1)[0].strip()
    tariffs, rest = marking.split(' (i) Cumas Gaeilge = ', 1)
    cumas, rest = rest.split(' [Ní mór ceangal cinnte', 1)
    content, nota = rest.split('] Nóta: ', 1)
    tariffs, cumas, content, nota = tariffs.strip(), '(i) Cumas Gaeilge = ' + cumas.strip(), '[Ní mór ceangal cinnte' + content + ']', 'Nóta: ' + nota.strip()
    assert tariffs.endswith('Tasc = 2 mharc Ábhar = 8 marc = 50 marc x 2 Cumas Gaeilge = 40 marc = 100 marc'), tariffs
    assert cumas.endswith('[(i) agus (ii) sa chóimheas 40% : 60%]') and '(ii) Beachtas = Cruinneas' in cumas, cumas[-60:]
    # 2015's content note prints no "leanúnach" (the paper's Treoracha do).
    assert content == ('[Ní mór ceangal cinnte a bheith idir an teideal a roghnaítear agus an t-ábhar a scríobhtar. '
                       'Gearrfar pionós ar iarrachtaí ceapadóireachta nach bhfuil ad rem.]'), content
    assert nota.endswith('ag bun na n-iarrachtaí ceapadóireachta.'), nota[-80:]
    smm = re.sub(r'^\d+\s', '', stext[20])
    assert 'Cuid II' not in marking and 'An tÁbhar (8 marc)' not in marking and 'Tá 8 marc ag dul don ábhar' not in marking
    # PDF 21's modified marking names the composition's 40-mark assessment but prints no bands for it.
    assert 'An Cheapadóireacht - An measúnú ar Chumas Gaeilge as 40 marc.' in smm and '34-40' not in smm and 'M F1 F2 F3' not in stext[10]
    # No 40-mark table anywhere in the 2015 Paper 1 pages (PDF 12 is Paper 2).
    assert '95%' not in ' '.join(stext[:12]) and stext[11].startswith('10 Páipéar II')
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
                assert line in texts[6], (group, roman, line[:40])
    _MATERIAL = dict(paper=paper, texts=texts, segments=segments, head=head, intro=intro,
                     composition=dict(tariffs=tariffs, cumas=cumas, content=content, nota=nota, smm=smm),
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
                             'Each printed question is marked at its own published 3-mark tariff. ' + LANGUAGE,
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
                # 2015 prints no headed Tasc/Ábhar sections: the tariff block prices the task, the bracketed note is the
                # scheme's content guidance, and the Cumas Gaeilge / Beachtas definitions and the Nóta go with Gaeilge.
                criteria=[criterion('tasc', 'An Tasc', 2, [c['tariffs']], permitted=[0, 2]),
                          criterion('abhar', 'An tÁbhar', 8, [c['content']]),
                          # The definitions and the Nóta are two printed blocks, kept as two lines: joined, the lift post-pass
                          # reads "60%] Nóta:" as a seam and drops it (as on the 2016 and 2017 cards).
                          criterion('gaeilge', 'An Cumas Gaeilge', 40, [c['cumas'], c['nota'],
                                    'Scéim Mharcála Mhodhnaithe (scheme PDF 21): for eligible candidates, spelling and certain grammar features are not penalised in the 40-mark Cumas Gaeilge assessment; no bands are printed.'])],
                markingGuideNote=f'Whole 50-mark composition: Tasc 2, Ábhar 8, Cumas Gaeilge 40. The {YEAR} scheme prints no 40-mark table and no 40-mark bands: '
                                 'Cumas Gaeilge is judged on its two printed aspects, (i) Cumas Gaeilge and (ii) Beachtas, in the ratio 40% : 60%, '
                                 'so the Cumas Gaeilge award can take any value from 0 to 40. '
                                 'The letter or email (C) and the dó/di wording are flexible forms inside one response, not separate routes.',
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
                  boundaries='6 listening segment cards carrying all 20 printed questions as separate criteria (3 each) (60); '
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
    # The searchable scheme text the provenance checks read (as 2016-2020 and 2026 write their own).
    scheme_md = f'# Gaeilge Gnáthleibhéal {YEAR} — SEC marking scheme (Páipéar 1 agus 2)\n\n' + '\n\n'.join(
        f'## PDF page {i + 1}\n\n' + p.get_text() for i, p in enumerate(scheme))
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
