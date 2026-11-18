#!/usr/bin/env python3
"""Reviewed 2025 Higher Paper 1 (Cluastuiscint agus Ceapadóireacht).

Paper PDF 1–20 and the Paper 1 pages of the combined LC001ALP000IV scheme
(PDF 1–17 and 48) visually reviewed on 2026-10-11. Scheme PDF 18–47 belong to
Paper 2. Counts are assertions, not corpus-completeness proof.

The legacy generator already ships 17 cards for this component: eight
whole-segment listening cards and the nine composition titles. Their IDs are
kept and they remain the card unit (the Bank plays one recording section as one
exercise, so separate question cards would duplicate prompts). `apply_legacy_review`
(called by irish_cards.py) joins them to Atlas, gives every printed listening
question its own criterion at its published 2 or 2 + 2 tariff, and replaces the
marking text with the lifted 2025 scheme. `main` writes the component review.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
FILE = 'LC001ALP100IV'
SCHEME_FILE = 'LC001ALP000IV'
OUT = ROOT / 'scripts/markbank/authored/irish-higher-2025-p1-component-review.json'
SOURCE_REVIEW = ROOT / 'scripts/markbank/authored/irish-higher-2025-p1-source-review.json'
REVIEWED_AT = '2026-10-11'
PAPER_SHA = '3a1df85fa8485182c3c0d96551dd3a0a72293d6ab1c31156a253129508777bfb'
SCHEME_SHA = '2b4f503260b2bcb3704a3f428bee88bbcccd8746b2a2b58208142cf7e6ff1550'
DIRECTIVE = re.compile(r'rogha|roghna|Freagair|Cuir tic|Ainmnigh|Luaigh|\bchoose\b|\beither\b|\bany\b|one of|\bnó\b|dhá phointe|trí phointe|dhá rud|dó/di|Cuir ciorcal|dhá thagairt|dhá ch|dhá dh|an dá|ceann amháin|amháin|\bdhá\b', re.I)
AUDIO_URL = 'https://www.examinations.ie/archive/exampapers/2025/LC001ZLP017IV.mp3'
SOURCE_NOTE = 'Shown page-for-page from the official examination paper; swipe to move between pages.'
LANGUAGE = ('Scheme PDF 3 and 11: “Bainfear ó 0 go 3 ar chaighdeán na Gaeilge.” This 0–3 deduction applies once to the whole '
            'listening section (Tuiscint 60 − Cumas Gaeilge 0–3), never inside a single card.')


def clean(text):
    return re.sub(r'\s+', ' ', text).strip()


def comparable(text):
    return re.sub(r'[^\w]+', '', text.lower())


def criterion(id, label, marks, guidance, kind='quality'):
    return dict(id=id, label=label, kind='award', maxMarks=marks, permittedMarks=list(range(marks + 1)),
                guidanceKind=kind, guidance=guidance)


def source(ref, pages):
    return dict(kind='source-text', label=ref, title=f'Gaeilge Ardleibhéal 2025 · Páipéar 1 · {ref}', pages=pages,
                attribution='© State Examinations Commission.', presentationNote=SOURCE_NOTE)


def selection_decisions(paper):
    decisions = json.loads(SOURCE_REVIEW.read_text())['selectionDecisions']
    expected = {(d['page'], d['raw']) for d in decisions}
    found = {(i, clean(line)) for i, page in enumerate(paper, 1)
             for line in page.get_text().splitlines() if DIRECTIVE.search(clean(line))}
    assert found == expected, ('Unclassified/stale selection directives', found - expected, expected - found)
    return decisions


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


_MATERIAL = None


def material():
    """Lifted paper prompts and scheme text, shared by the legacy review and the additions."""
    global _MATERIAL
    if _MATERIAL:
        return _MATERIAL
    import fitz
    paper_path = ROOT / f'paper-trail-corpus/exampapers/2025/{FILE}.pdf'
    scheme_path = ROOT / f'paper-trail-corpus/markingschemes/2025/{SCHEME_FILE}.pdf'
    assert hashlib.sha256(paper_path.read_bytes()).hexdigest() == PAPER_SHA, 'Paper changed: repeat visual review'
    assert hashlib.sha256(scheme_path.read_bytes()).hexdigest() == SCHEME_SHA, 'Scheme changed: repeat visual review'
    paper, scheme = fitz.open(paper_path), fitz.open(scheme_path)
    texts = [clean(p.get_text()) for p in paper]
    stext = [clean(p.get_text()) for p in scheme]
    listening = Marked(scheme, 7, 11)
    # (key, legacy id suffix, ref, heading, paper page, topic, part, total, [(n, paper prompt, marks, scheme anchor)])
    segments = [
        ('L-A-F1', 'a-f1', 'Cuid A · Fógra a hAon', 'FÓGRA A hAON', 3, 'irish-1-0', 'A', 10, [
            ('1a', '1. (a) Cé a chuir amach an fógra seo?', 2, '1. (a) Cé a chuir amach an fógra seo?'),
            ('1b', '(b) Cén dáta a chuirfear tús leis an gclár nua?', 2, '(b) Cén dáta a chuirfear tús'),
            ('2', '2. Scríobh síos dhá rud a bheidh le cloisteáil ar an gclár.', 4, '2. Scríobh síos dhá rud a bheidh le cloisteáil'),
            ('3', '3. Cén ról a bheidh ag Máire Treasa Ní Dhubhghaill sa chlár seo?', 2, '3. Cén ról a bheidh ag Máire Treasa')]),
        ('L-A-F2', 'a-f2', 'Cuid A · Fógra a Dó', 'FÓGRA A DÓ', 3, 'irish-1-0', 'A', 8, [
            ('1', '1. Cé a chuir amach an fógra seo?', 2, 'FÓGRA A DÓ (8 marc) 1. Cé a chuir amach an fógra seo?'),
            ('2a', '2. (a) Cad air a ndéanfaidh na scoláirí taighde mar chuid den tionscadal seo?', 2, '2. (a) Cad air a ndéanfaidh na scoláirí taighde'),
            ('2b', '(b) Scríobh síos rud amháin a dhéanfaidh na scoláirí nuair a bheidh an taighde críochnaithe acu.', 2, '(b) Scríobh síos rud amháin a dhéanfaidh na scoláirí'),
            ('3', '3. Cén t‐am a bheidh an cruinniú ar siúl Déardaoin seo chugainn?', 2, '3. Cén t-am a bheidh an cruinniú')]),
        ('L-B-C1-M1', 'b-c1-first', 'Cuid B · Comhrá a hAon · An Chéad Mhír', 'COMHRÁ A hAON\nAn Chéad Mhír', 4, 'irish-1-1', 'B', 8, [
            ('1', '1. Cén post lánaimseartha atá faighte ag Seán?', 2, '1. Cén post lánaimseartha'),
            ('2', '2. Scríobh síos an dá chineál oibre a bhíonn ar siúl ag Seán.', 4, '2. Scríobh síos an dá chineál oibre'),
            ('3', '3. Luaigh cúis amháin a dtaitníonn an post le Seán.', 2, '3. Luaigh cúis amháin a dtaitníonn')]),
        ('L-B-C1-M2', 'b-c1-second', 'Cuid B · Comhrá a hAon · An Dara Mír', 'COMHRÁ A hAON\nAn Dara Mír', 4, 'irish-1-1', 'B', 6, [
            ('1', '1. Scríobh síos an dá chúis nár lean Aoife ar aghaidh leis an gcleachtadh coirp nuair a bhí séasúr na camógaíochta thart anuraidh.', 4, '1. Scríobh síos an dá chúis nár lean Aoife'),
            ('2', '2. Cén táille bhallraíochta speisialta atá ar fáil do mhic léinn?', 2, '2. Cén táille bhallraíochta')]),
        ('L-B-C2-M1', 'b-c2-first', 'Cuid B · Comhrá a Dó · An Chéad Mhír', 'COMHRÁ A DÓ\nAn Chéad Mhír', 5, 'irish-1-1', 'B', 8, [
            ('1', '1. Cá fhad atá deirfiúr Liam ina cónaí in Sydney?', 2, '1. Cá fhad atá deirfiúr Liam'),
            ('2', '2. Scríobh síos an dá chúis ar imigh deirfiúr Liam go dtí an Astráil.', 4, '2. Scríobh síos an dá chúis ar imigh'),
            ('3', '3. Tabhair fáth amháin a ndeir Liam gur mór an chabhair í an teicneolaíocht dá deirfiúr in Sydney.', 2, '3. Tabhair fáth amháin a ndeir Liam')]),
        ('L-B-C2-M2', 'b-c2-second', 'Cuid B · Comhrá a Dó · An Dara Mír', 'COMHRÁ A DÓ\nAn Dara Mír', 5, 'irish-1-1', 'B', 6, [
            ('1', '1. Cá bhfuil Maria, an bhean Bhrasaíleach, ag obair i Luimneach?', 2, '1. Cá bhfuil Maria'),
            ('2', '2. Luaigh dhá rud a léiríonn gur bean ar leith í Maria, an bhean Bhrasaíleach, dar le hÁine.', 4, '2. Luaigh dhá rud a léiríonn')]),
        ('L-C-P1', 'c-p1', 'Cuid C · Píosa a hAon', 'PÍOSA A hAON', 6, 'irish-1-2', 'C', 6, [
            ('1', '1. Cathain a sheol an rialtas ‘an Scéim Éarlaise agus Aisíoca’?', 2, '1. Cathain a sheol an rialtas'),
            ('2', '2. Cá gcuireann an custaiméir an buidéal plaisteach folamh nó an canna alúmanaim folamh?', 2, '2. Cá gcuireann an custaiméir'),
            ('3', '3. Scríobh síos toradh fiúntach amháin a chreideann an rialtas a bheidh ar an scéim seo.', 2, '3. Scríobh síos toradh fiúntach')]),
        ('L-C-P2', 'c-p2', 'Cuid C · Píosa a Dó', 'PÍOSA A DÓ', 6, 'irish-1-2', 'C', 8, [
            ('1', '1. Cén eagraíocht a chuir an chartlann nua grianghraf ar fáil le gairid?', 2, '1. Cén eagraíocht a chuir an chartlann'),
            ('2', '2. Cén fáth ar bunaíodh an eagraíocht sin?', 2, '2. Cén fáth ar bunaíodh an eagraíocht'),
            ('3', '3. Scríobh síos dhá imeacht ag ar tógadh na grianghraif atá sa chartlann.', 4, '3. Scríobh síos dhá imeacht')]),
    ]
    anchors = [q[3] for seg in segments for q in seg[8]]
    heading = re.compile(r'\s*(FÓGRA A DÓ \(8 marc\)|CUID B \(28 marc\) COMHRÁ A hAON \(14 mharc\) An Chéad Mhír|An Dara Mír|COMHRÁ A DÓ \(14 mharc\) An Chéad Mhír|CUID C \(14 mharc\) PÍOSA A hAON \(6 mharc\)|PÍOSA A DÓ \(8 marc\))\s*$')

    def furniture(raw):
        # The next segment's printed heading precedes the following question; it must not add a page.
        while True:
            trimmed = heading.sub('', re.sub(r'(\s*⟦\d+⟧\s*)+$', '', raw))
            if trimmed == raw:
                return raw
            raw = trimmed
    chunks = iter(listening.split(anchors, 'Bainfear ó 0 go 3 ar chaighdeán na Gaeilge.', furniture))
    for seg in segments:
        assert sum(q[2] for q in seg[8]) == seg[7], seg[0]
        for i, (n, prompt, marks, anchor) in enumerate(seg[8]):
            chunk, pages = next(chunks)
            # Drop the next segment's printed heading that precedes the following question.
            chunk = re.sub(r'^FÓGRA A DÓ \(8 marc\) ', '', chunk)
            assert comparable(prompt) in comparable(texts[seg[4] - 1]), (seg[0], n)
            assert (f'{marks // 2} mharc + {marks // 2} mharc' if marks == 4 else '2 mharc') in chunk, (seg[0], n, chunk[:80])
            seg[8][i] = (n, prompt, marks, chunk, pages)
    intro = {
        'A': 'Cuid A\nCloisfidh tú dhá fhógra sa chuid seo. Cloisfidh tú gach fógra díobh faoi dhó. Beidh sos ann leis na freagraí a scríobh tar éis na chéad éisteachta agus tar éis an dara héisteacht.',
        'B': 'Cuid B\nCloisfidh tú dhá chomhrá sa chuid seo. Cloisfidh tú gach comhrá díobh faoi dhó. Cloisfidh tú an comhrá ó thosach deireadh an chéad uair. Ansin cloisfidh tú ina dhá mhír é. Beidh sos ann leis na freagraí a scríobh tar éis gach míre díobh.',
        'C': 'Cuid C\nCloisfidh tú dhá phíosa nuachta sa chuid seo. Cloisfidh tú gach píosa díobh faoi dhó. Beidh sos ann leis na freagraí a scríobh tar éis na chéad éisteachta agus tar éis an dara héisteacht.'}
    for part, page in [('A', 3), ('B', 4), ('C', 6)]:
        assert comparable(intro[part].split('\n', 1)[1]) in comparable(texts[page - 1]), part

    # Composition (scheme PDF 12–17, SMM 48).
    marking = stext[11].split('An Mharcáil:', 1)[1].strip()
    stil = stext[13].split('Stíl chuí scríbhneoireachta (5 mharc)', 1)[1].split('Ionramháil Ábhair (15 mharc)', 1)[0].strip()
    abhar = stext[13].split('Ionramháil Ábhair (15 mharc)', 1)[1].strip()
    gaeilge = [stext[14][stext[14].index('Cumas Gaeilge (80 marc)'):].strip(), stext[15]]
    graded = stext[16][stext[16].index('An Grádú Marcála'):].strip()
    marking = marking.removesuffix('Cuid II An Cheapadóireacht 100 marc').strip()
    marking, stil, abhar, graded = [re.sub(r'\s+\d+$', '', t) for t in [marking, stil, abhar, graded]]
    gaeilge = [re.sub(r'\s+\d+$', '', re.sub(r'^\d+\s', '', g)) for g in gaeilge]
    assert all(x in abhar for x in ['13, 14, 15', '11, 12', '9, 10', '6, 7, 8', '3, 4, 5', '0, 1, 2'])
    assert all(x in gaeilge[1] for x in ['76-80', '64-67', '52-55', '40-43', '28-31', '16-19', '0-7'])
    assert all(x in graded for x in ['S1', 'S2', 'S3', 'S4', '(68)', '(56)', '(44)', '(54)', 'A (a), A (d), A (e) agus C (b)'])
    head = ('Freagair do rogha CEANN AMHÁIN de A, B nó C anseo thíos.\n'
            'Treoracha: Ní gá níos mó ná 500‐600 focal nó mar sin a scríobh i gcás ar bith.\n'
            'Ní mór do na hiarrthóirí cúram a dhéanamh de chruinneas na teanga. Caillfear marcanna má bhítear faillitheach ann.\n'
            'Ní mór ceangal cinnte leanúnach a bheith ann idir an teideal a roghnaítear agus an t‐ábhar a scríobhtar.')
    groups = {
        'A': ('AISTE nó ALT NUACHTÁIN/IRISE', 'Scríobh AISTE nó ALT NUACHTÁIN/IRISE ar cheann amháin de na hábhair seo.', [
            ('a', 'Daoine a bhfuil meas agam orthu.'), ('b', 'Éire – an tír mhaith í le cónaí inti?'),
            ('c', 'An comhshaol – ábhar imní do phobail an domhain.'), ('d', 'Polaiteoirí agus cúrsaí polaitíochta ar fud an domhain.'),
            ('e', 'Scéalta móra nuachta na linne seo.')]),
        'B': ('SCÉAL', 'Ceap SCÉAL a mbeadh do rogha ceann amháin díobh seo oiriúnach mar theideal air.', [
            ('a', 'Dóchas.'), ('b', 'Is ait an mac an saol.')]),
        'C': ('DÍOSPÓIREACHT/ÓRÁID', 'Freagair do rogha ceann amháin díobh seo.', [
            ('a', 'Scríobh an chaint a dhéanfá i ndíospóireacht scoile ar son an rúin seo a leanas nó ina aghaidh:\nBíonn saol maith ag daoine óga sa lá atá inniu ann.'),
            ('b', 'Iarradh ort píosa cainte a dhéanamh ar chlár raidió ar an ábhar seo a leanas:\nNa deiseanna agus na dúshláin a bhaineann leis an Intleacht Shaorga.\nScríobh an píosa cainte a dhéanfá ar an ábhar sin.')]),
    }
    for group, (_, instruction, titles) in groups.items():
        for letter, title in titles:
            assert all(comparable(line) in comparable(texts[6]) for line in [instruction, *title.splitlines()]), (group, letter)
    assert all(comparable(line) in comparable(texts[6]) for line in head.splitlines()[1:])
    decisions = selection_decisions(paper)
    _MATERIAL = dict(decisions=decisions, paper=paper, scheme=scheme, texts=texts, segments=segments, intro=intro, head=head, groups=groups,
                     composition=dict(marking=marking, stil=stil, abhar=abhar, gaeilge=gaeilge, graded=graded))
    return _MATERIAL


COMPOSITION_REASONS = {
    'A': 'AISTE nó ALT NUACHTÁIN/IRISE is a choice of writing form inside one response, marked by the same Stíl/Ábhar/Gaeilge scheme; it is not a separate route.',
    'B': 'Each printed title is a separate route; the story itself is open.',
    'C': '“ar son … nó ina aghaidh” is the speaker’s stance inside one speech; both stances are marked identically.'}
S4_TITLES = {('A', 'a'), ('A', 'd'), ('A', 'e'), ('C', 'b')}


def apply_legacy_review(cards):
    """Join the 17 retained legacy cards to Atlas and lift their 2025 scheme text (IDs unchanged)."""
    m = material()
    by_id = {c['id']: c for c in cards}
    stamped = []
    for key, suffix, ref, heading, page, topic, part, total, questions in m['segments']:
        card = by_id[f'irish-2025-hl-p1-listening-{suffix}']
        assert card['totalMarks'] == total and card['topicId'] == topic, card['id']
        pages = sorted({p for q in questions for p in q[4]})
        card.update(atlasQuestionId=key, reviewedAt=REVIEWED_AT, reviewedPaperPages=[page], paperPage=page,
                    schemePage=pages[0], schemePages=pages, sourceMaterial=source(f'Cluastuiscint {ref}', [page]),
                    markingGuideNote='The listed responses and tariffs come from the 2025 SEC marking scheme; equivalent wording with the same meaning is accepted. '
                                     'Each printed question is marked at its own published tariff (2, or 2 + 2 for two points). ' + LANGUAGE)
        criteria = []
        for n, prompt, marks, chunk, _ in questions:
            partial = '= 1 mharc' in chunk
            cr = criterion(f'q{n}', f'Ceist {n[0]}' + (f'({n[1]})' if len(n) > 1 else ''), marks, [chunk], 'exact')
            cr['permittedMarks'] = (list(range(marks + 1)) if partial else list(range(0, marks + 1, 2)))
            criteria.append(cr)
        card['criteria'] = criteria
        stamped.append(card['id'])
    c = m['composition']
    for group, (form, instruction, titles) in m['groups'].items():
        for letter, title in titles:
            card = by_id[f'irish-2025-hl-p1-composition-{group.lower()}-{letter}']
            s4 = ([f'S4 applies to this title: “Easnamhach i gcás A (a), A (d), A (e) agus C (b)” — Stíl (5) Ábhar (10) Gaeilge (54).']
                  if (group, letter) in S4_TITLES else [])
            card.update(atlasQuestionId=f'W-{group}-{letter}', reviewedAt=REVIEWED_AT, reviewedPaperPages=[7], paperPage=7,
                        schemePage=12, schemePages=[12, 13, 14, 15, 16, 17],
                        questionText=m['head'] + f'\n\n{group} · {form} (100 marc)\n{instruction}\n\n({letter}) {title}\n\nAn rogha don chárta seo: {group}({letter}).',
                        sourceMaterial=source(f'Ceapadóireacht {group}({letter})', [7]),
                        taskRequirements=['Lean an fhoirm scríbhneoireachta a iarrtar sa cheist.',
                                          'Coinnigh ceangal cinnte leanúnach idir an teideal agus an t-ábhar.', 'Timpeall 500–600 focal.'],
                        criteria=[criterion('stil', 'Stíl chuí scríbhneoireachta', 5, [c['stil'], c['graded']]),
                                  criterion('abhar', 'Ionramháil Ábhair', 15, [c['abhar'], c['marking']]),
                                  criterion('gaeilge', 'Cumas Gaeilge', 80, c['gaeilge'] + [
                                      'Scéim Mharcála Mhodhnaithe (scheme PDF 48): for eligible candidates spelling and the listed grammar features are not counted in the 80-mark Cumas Gaeilge award.'] + s4)],
                        markingGuideNote='Whole 100-mark composition: Stíl 5, Ionramháil Ábhair 15, Cumas Gaeilge 80, assessed as one unit. '
                                         'Deficient-length attempts use the printed S1–S4 grades. ' + COMPOSITION_REASONS[group])
            assert card['totalMarks'] == 100
            stamped.append(card['id'])
    assert len(stamped) == 17
    for card in cards:
        if card['id'] in stamped:
            for cr in card['criteria']:
                assert all(not re.search('[-]', g) for g in cr['guidance']), (card['id'], cr['id'])
    return cards, stamped


def review(cards=None):
    """The component review record; the inventory reads it beside authored.json."""
    m = material()
    sr = json.loads(SOURCE_REVIEW.read_text())
    listening = [f'irish-2025-hl-p1-listening-{seg[1]}' for seg in m['segments']]
    composition = [f'irish-2025-hl-p1-composition-{g.lower()}-{t[0]}' for g, v in m['groups'].items() for t in v[2]]
    return dict(year=2025, level='higher', paperFileid=FILE + '.pdf', schemeFileid=SCHEME_FILE + '.pdf',
                paperSha256=PAPER_SHA, schemeSha256=SCHEME_SHA,
                reviewedPaperPages=list(range(1, 21)), reviewedSchemePages=sr['reviewedSchemePages'],
                schemeScope=sr['schemeScope'], reviewDate=REVIEWED_AT, status='reviewed',
                fullPaperAndApplicableSchemeVisualSweep=True, selectionDecisions=m['decisions'],
                cardIds=listening + composition, listeningSegmentCardIds=listening, compositionRouteCardIds=composition,
                printedListeningQuestions=sum(len(seg[8]) for seg in m['segments']),
                examStructure=dict(listening=60, composition=100, total=160),
                nonPoolDecisions=sr['nonPoolDecisions'], openIssues=[], audio=sr['audio'], caveats=sr['sourceFindings'],
                boundaries='8 retained listening segment cards carrying all 24 printed questions as separate criteria at 2 or 2 + 2 (60); '
                           '9 retained composition title routes at 100 each (choose one).')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    data = review()
    content = json.dumps(data, ensure_ascii=False, indent=2) + '\n'
    if args.check:
        assert OUT.exists() and OUT.read_text() == content, f'Stale output: {OUT}'
    else:
        OUT.write_text(content)
    print(f"Irish Higher 2025 Paper 1: {len(data['cardIds'])} retained cards reviewed ({data['printedListeningQuestions']} printed listening questions); the archive remains incomplete.")


if __name__ == '__main__':
    main()
