#!/usr/bin/env python3
"""Reviewed 2024 Ordinary Paper 1 (Cluastuiscint agus Ceapadóireacht).

Paper PDF 1–16 and the Paper 1 pages of the combined LC001GLP000IV scheme
(PDF 1–13 and 33–34 modified marking) visually reviewed on 2026-10-12. Scheme PDF
14–32 belong to Paper 2. Counts are assertions, not corpus-completeness proof.
Same method as irish_ordinary_2025_p1.py; Fógra a Dó Ceist 2 is one 3 + 3 question.

The legacy generator already ships 15 cards for this component: six listening
segment cards and the nine composition titles. Their IDs are kept and the six
segments stay the listening card unit (the Bank plays one recording section as one
exercise). `apply_legacy_review` (called by irish_cards.py) joins them to Atlas,
marks each of the 19 printed listening questions as its own criterion (3, or 3 + 3) and
lifts the 2024 composition scheme. “Freagair do rogha dhá cheann de A, B, C, D” is
a choice, not a route: each title keeps its own card and carries the instruction in
its task requirements; no two-section combination cards are published (each
composition is marked on its own 50). `main` writes the component review.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
FILE = 'LC001GLP100IV'
SCHEME_FILE = 'LC001GLP000IV'
OUT = ROOT / 'scripts/markbank/authored/irish-ordinary-2024-p1-component-review.json'
SOURCE_REVIEW = ROOT / 'scripts/markbank/authored/irish-ordinary-2024-p1-source-review.json'
REVIEWED_AT = '2026-10-12'
PAPER_SHA = '38e1df71f9ac5e8091174867e45b544fd6715b2052e57cc24b4a756fb962f142'
SCHEME_SHA = '954e2a1e867a0926326bf5273db46fca631cbd0437a1c62c0da677c0ff39fcbe'
DIRECTIVE = re.compile(r'rogha|roghna|Freagair|Cuir tic|Ainmnigh|Luaigh|\bnó\b|dhá phointe|dhá rud|dó/di|ceann amháin|amháin|\bdhá\b', re.I)
SOURCE_NOTE = 'Shown page-for-page from the official examination paper; swipe to move between pages.'
LANGUAGE = ('Scheme PDF 3 and 9: “Bainfear ó 0 go 6 ar chaighdeán na Gaeilge.” This 0–6 deduction applies once to the whole '
            'listening section (Tuiscint 60 − Cumas Gaeilge 0–6), never inside a single question.')
HEADINGS = re.compile(r'\s*(FÓGRA A DÓ \(12 mharc\)|Cuid B \(24 marc\) COMHRÁ A hAON \(12 mharc\) An Chéad Mhír|An Dara Mír|'
                      r'COMHRÁ A DÓ \(12 mharc\) An Chéad Mhír|Cuid C \(12 mharc\) PÍOSA A hAON \(6 mharc\)|PÍOSA A DÓ \(6 mharc\))\s*$')


def clean(text):
    return re.sub(r'\s+', ' ', text).strip()


def comparable(text):
    return re.sub(r'[^\w]+', '', text.lower())


def criterion(id, label, marks, guidance, kind='quality', permitted=None):
    return dict(id=id, label=label, kind='award', maxMarks=marks, permittedMarks=permitted or list(range(marks + 1)),
                guidanceKind=kind, guidance=guidance)


def source(ref, pages):
    return dict(kind='source-text', label=ref, title=f'Gaeilge Gnáthleibhéal 2024 · Páipéar 1 · {ref}', pages=pages,
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
        """Slice at each start; `strip` removes trailing furniture (headings, symbol tables) BEFORE pages are counted."""
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


_MATERIAL = None


def material():
    global _MATERIAL
    if _MATERIAL:
        return _MATERIAL
    import fitz
    paper_path = ROOT / f'paper-trail-corpus/exampapers/2024/{FILE}.pdf'
    scheme_path = ROOT / f'paper-trail-corpus/markingschemes/2024/{SCHEME_FILE}.pdf'
    assert hashlib.sha256(paper_path.read_bytes()).hexdigest() == PAPER_SHA, 'Paper changed: repeat visual review'
    assert hashlib.sha256(scheme_path.read_bytes()).hexdigest() == SCHEME_SHA, 'Scheme changed: repeat visual review'
    paper, scheme = fitz.open(paper_path), fitz.open(scheme_path)
    texts = [clean(p.get_text()) for p in paper]
    stext = [clean(p.get_text()) for p in scheme]
    # (key, legacy suffix, ref, paper page, topic, [(criterion id, label, paper prompt, scheme anchor, marks)])
    segments = [
        ('L-A-F1', 'a-f1', 'Cuid A · Fógra a hAon', 3, 'irish-1-0', [
            ('q1a', 'Ceist 1(a)', 'Cén duine i gColáiste na Carraige atá ag labhairt leis na scoláirí san fhógra seo?', '1. (a) Cén duine', 3),
            ('q1b', 'Ceist 1(b)', 'Cé mhéad scoláire atá roghnaithe mar bhaill den choiste le haghaidh Gaelbhratach?', '(b) Cé mhéad scoláire', 3),
            ('q2a', 'Ceist 2(a)', 'Cad a bheidh ar siúl i Seomra na Gaeilge ag am lóin gach Céadaoin?', '2. (a) Cad a bheidh ar siúl', 3),
            ('q2b', 'Ceist 2(b)', 'Cathain a bhronnfar Gaelbhratach ar an scoil má éiríonn lena n‐iarrachtaí?', '(b) Cathain a bhronnfar', 3)]),
        ('L-A-F2', 'a-f2', 'Cuid A · Fógra a Dó', 3, 'irish-1-0', [
            ('q1a', 'Ceist 1(a)', 'Cén stiúrthóir a chuir amach an fógra seo?', '1. (a) Cén stiúrthóir', 3),
            ('q1b', 'Ceist 1(b)', 'Cén áit sa mhúsaem a mbeidh an cuairteoir ábalta féachaint ar mhíreanna físe d’imreoirí mór le rá i mbun gaiscí ar an bpáirc imeartha?', '(b) Cén áit sa mhúsaem', 3),
            ('q2', 'Ceist 2', 'Luaigh dhá áit a fheicfidh an cuairteoir ar an turas timpeall na staide.', '2. Luaigh dhá áit', 6)]),
        ('L-B-C1', 'b-c1', 'Cuid B · Comhrá a hAon', 4, 'irish-1-1', [
            ('m1-q1', 'An Chéad Mhír · Ceist 1', 'Cén tír ina raibh Aoife agus a teaghlach ar saoire?', '1. Cén tír ina raibh', 3),
            ('m1-q2', 'An Chéad Mhír · Ceist 2', 'Cad a dúirt Aoife faoi na hionaid turasóireachta go léir?', '2. Cad a dúirt Aoife', 3),
            ('m2-q1', 'An Dara Mír · Ceist 1', 'Scríobh síos áit amháin inar cuireadh lóistín ar fáil do dhaoine a theith ó dhainséar.', '1. Scríobh síos áit amháin inar', 3),
            ('m2-q2', 'An Dara Mír · Ceist 2', 'Luaigh cineál amháin aimsire a tharlaíonn níos minice sa tír seo anois.', '2. Luaigh cineál amháin', 3)]),
        ('L-B-C2', 'b-c2', 'Cuid B · Comhrá a Dó', 4, 'irish-1-1', [
            ('m1-q1', 'An Chéad Mhír · Ceist 1', 'Cén áit sa bhaile mór ar chodail Áine agus grúpa scoláirí óna scoil amuigh?', '1. Cén áit sa bhaile mór', 3),
            ('m1-q2', 'An Chéad Mhír · Ceist 2', 'Cén duine i scoil Áine a oibríonn go deonach le Focus Ireland?', '2. Cén duine i scoil Áine', 3),
            ('m2-q1', 'An Dara Mír · Ceist 1', 'Cár bhailigh Áine agus an grúpa scoláirí óna scoil le chéile ag leathuair tar éis a ceathair?', '1. Cár bhailigh Áine', 3),
            ('m2-q2', 'An Dara Mír · Ceist 2', 'Cé mhéad airgid a bhailigh Áine agus an grúpa scoláirí óna scoil don charthanas Focus Ireland?', '2. Cé mhéad airgid', 3)]),
        ('L-C-P1', 'c-p1', 'Cuid C · Píosa a hAon', 5, 'irish-1-2', [
            ('q1', 'Ceist 1', 'Cathain a d’eagraigh an grúpa Sábháilteacht ar Líne do Pháistí an tionscnamh speisialta?', '1. Cathain a d’eagraigh', 3),
            ('q2', 'Ceist 2', 'Cad air a gcaitheann líon ard daoine an iomarca ama de réir taighde a rinneadh le déanaí?', '2. Cad air a gcaitheann', 3)]),
        ('L-C-P2', 'c-p2', 'Cuid C · Píosa a Dó', 5, 'irish-1-2', [
            ('q1', 'Ceist 1', 'Cé mhéad clár a bhí sa tsraith theilifíse Bláth na hÓige?', '1. Cé mhéad clár', 3),
            ('q2', 'Ceist 2', 'Cá bhfuil Stiúideo Cuan?', '2. Cá bhfuil Stiúideo Cuan?', 3)]),
    ]
    listening = Marked(scheme, 7, 9)
    def furniture(raw):
        # PDF 7 extracts its annotation-symbol table after Fógra a hAon; section headings precede the next question.
        raw = re.sub(r'\s*Siombailí Anótála Cur Síos Arna Léiriú[^⟦]*', ' ', raw)
        while True:
            trimmed = HEADINGS.sub('', re.sub(r'(\s*⟦\d+⟧\s*)+$', '', raw))
            if trimmed == raw:
                return raw
            raw = trimmed
    chunks = iter(listening.split([q[3] for seg in segments for q in seg[5]], 'Bainfear ó 0 go 6 ar chaighdeán na Gaeilge.', furniture))
    for seg in segments:
        for i, (cid, label, prompt, anchor, marks) in enumerate(seg[5]):
            chunk, pages = next(chunks)
            assert comparable(prompt) in comparable(texts[seg[3] - 1]), (seg[0], cid)
            assert chunk.endswith('mharc') and ('3 mharc + 3 mharc' if marks == 6 else '3 mharc') in chunk, (seg[0], cid, chunk[-60:])
            seg[5][i] = (cid, label, prompt, chunk, pages, marks)
    assert sum(len(seg[5]) for seg in segments) == 19 and sum(q[5] for seg in segments for q in seg[5]) == 60
    general = 'Nóta (scheme PDF 7): ' + stext[6].split('Nóta:', 1)[1].split('Cuid A (24 marc)', 1)[0].strip()
    assert general.endswith('chomh maith.')

    marking = stext[9][stext[9].index('Freagair do rogha dhá cheann'):]
    symbols, table40, table_short = [re.sub(r'^\d+\s', '', t) for t in stext[10:13]]
    smm = re.sub(r'^\d+\s', '', stext[33])
    marking = re.sub(r'\s+\d+$', '', marking)
    assert 'Tasc = 2 mharc' in marking and 'Ábhar = 8 marc' in marking and 'Cumas Gaeilge = 40 marc' in marking
    assert all(x in table_short for x in ['M F1 F2 F3', '38 34 29 19 10']) and '34-40' in smm and '95% 38' in table40
    head = ('Treoracha: Ní mór do na hiarrthóirí cúram a dhéanamh de chruinneas na teanga. Caillfear marcanna má bhítear faillitheach ann. '
            'Ní mór ceangal cinnte leanúnach a bheith ann idir an teideal a roghnaítear agus an t-ábhar a scríobhtar.\n\n'
            'Freagair do rogha dhá cheann de A, B, C, D anseo.')
    assert comparable(head.split('\n\n')[0].removeprefix('Treoracha: ')) in comparable(texts[5]) and comparable(head.split('\n\n')[1]) in comparable(texts[6])
    groups = {
        'A': ('Giota Leanúnach/Blag', 'Scríobh giota leanúnach nó blag (leathleathanach nó mar sin) ar cheann amháin de na hábhair seo.', [
            ('i', 'Pearsa cheoil a thaitníonn go mór liom.'), ('ii', 'Saol an scoláire sa séú bliain.'), ('iii', 'Eachtra a tharla i mo cheantar.')]),
        'B': ('Scéal', 'Ceap scéal (leathleathanach nó mar sin) a mbeadh ceann amháin de na sleachta seo a leanas oiriúnach mar thús leis.', [
            ('i', 'Ar deireadh, tháinig an ríomhphost ón mbainisteoir. Léigh mé go cúramach é. Léim mo chroí le háthas …'),
            ('ii', 'Tráthnóna dorcha geimhridh a bhí ann. Tháinig mé den traein ag an stáisiún mícheart. Bhí mé i bponc …')]),
        'C': ('Litir/Ríomhphost', None, [
            ('i', 'D’eagraigh do bhliainghrúpa imeachtaí do Sheachtain na Gaeilge sa scoil.\nScríobh an litir/an ríomhphost (leathleathanach nó mar sin) a chuirfeá chuig cara leat ag insint dó/di faoi na himeachtaí a d’eagraigh sibh agus faoi dhuine cáiliúil a thug cuairt ar an scoil le linn na seachtaine.'),
            ('ii', 'Bhí post páirtaimseartha agat i rith laethanta saoire an tsamhraidh.\nScríobh an litir/an ríomhphost (leathleathanach nó mar sin) a chuirfeá chuig cara leat ag insint dó/di faoin obair a rinne tú agus faoi mar a chaith tú an t-airgead a thuill tú.')]),
        'D': ('Comhrá', None, [
            ('i', 'Tá scannán á dhéanamh i do cheantar agus tá daoine óga á lorg chun páirt a ghlacadh ann.\nScríobh an comhrá (leathleathanach nó mar sin) a bheadh agat le do chara faoin ábhar sin.'),
            ('ii', 'Caitheann tú a lán ama le do chairde ag an deireadh seachtaine agus ní dhéanann tú mórán staidéir. Níl do thuismitheoirí sásta leat. Scríobh an comhrá (leathleathanach nó mar sin) a bheadh agat le do thuismitheoirí faoin ábhar sin.')]),
    }
    for group, (_, instruction, titles) in groups.items():
        for roman, title in titles:
            for line in ([instruction] if instruction else []) + title.splitlines():
                assert comparable(line) in comparable(texts[6]), (group, roman, line[:40])
    _MATERIAL = dict(paper=paper, texts=texts, segments=segments, head=head, groups=groups, general=general,
                     composition=dict(marking=marking, symbols=symbols, table40=table40, table_short=table_short, smm=smm),
                     decisions=selection_decisions(paper))
    return _MATERIAL


def apply_legacy_review(cards):
    """Join the 15 retained legacy cards to Atlas and lift the 2024 scheme (IDs, totals and topics unchanged).

    schemeFileid names the Ordinary scheme: without it the Atlas answer map falls
    back to the Higher scheme file."""
    m = material()
    by_id = {c['id']: c for c in cards}
    stamped = []
    for key, suffix, ref, page, topic, questions in m['segments']:
        card = by_id[f'irish-2024-ol-p1-listening-{suffix}']
        assert card['topicId'] == topic and card['totalMarks'] == sum(q[5] for q in questions), card['id']
        criteria = []
        for cid, label, prompt, chunk, pages, marks in questions:
            values = {0, 3} | {int(v) for v in re.findall(r'= (\d) mharc', chunk)}
            # A 3 + 3 question scores each point on the printed scale (3, or 2 for a partial).
            permitted = sorted(values if marks == 3 else {a + b for a in values for b in values if a + b <= marks})
            criteria.append(criterion(cid, label, marks, [chunk, m['general']], 'exact', permitted=permitted))
        pages = sorted({p for q in questions for p in q[4]})
        card.update(atlasQuestionId=key, reviewedAt=REVIEWED_AT, reviewedPaperPages=[page], paperPage=page, schemeFileid=SCHEME_FILE,
                    schemePage=pages[0], schemePages=pages, sourceMaterial=source(f'Cluastuiscint {ref}', [page]), criteria=criteria,
                    markingGuideNote='The listed responses and tariffs come from the 2024 SEC marking scheme; equivalent wording with the same meaning is accepted. '
                                     'Each printed question is marked at its own published tariff (3, or 3 + 3 for two places). ' + LANGUAGE)
        stamped.append(card['id'])
    c = m['composition']
    for group, (form, instruction, titles) in m['groups'].items():
        for roman, title in titles:
            card = by_id[f'irish-2024-ol-p1-composition-{group.lower()}-{roman}']
            body = m['head'] + f'\n\n{group} · {form} (50 marc)\n' + (instruction + '\n' if instruction else '') + f'({roman}) {title}'
            card.update(atlasQuestionId=f'W-{group}-{roman}', reviewedAt=REVIEWED_AT, reviewedPaperPages=[7], paperPage=7, schemeFileid=SCHEME_FILE,
                        schemePage=10, schemePages=[10, 11, 12, 13],
                        questionText=body + f'\n\nAn rogha don chárta seo: {group}({roman}).',
                        sourceMaterial=source(f'Ceapadóireacht {group}({roman})', [7]),
                        taskRequirements=['Freagair do rogha dhá cheann de A, B, C, D anseo.', 'Lean an fhoirm scríbhneoireachta a iarrtar sa cheist.',
                                          'Coinnigh ceangal cinnte leanúnach idir an teideal agus an t-ábhar.', 'Leathleathanach nó mar sin.'],
                        criteria=[criterion('tasc', 'An Tasc', 2, [c['marking'].split('An tÁbhar (8 marc)')[0]], permitted=[0, 2]),
                                  criterion('abhar', 'An tÁbhar', 8, [c['marking'].split('An tÁbhar (8 marc)', 1)[1].split('An Cumas Gaeilge (40 marc)')[0]], 'indicative'),
                                  criterion('gaeilge', 'An Cumas Gaeilge', 40, [c['marking'].split('An Cumas Gaeilge (40 marc)', 1)[1], c['symbols'], c['table40'], c['table_short'],
                                            'Scéim Mharcála Mhodhnaithe (scheme PDF 33–34): eligible candidates are assessed on named grammar features (bands 34–40 … 0–3); spelling is not counted.'])],
                        markingGuideNote='Whole 50-mark composition: Tasc 2, Ábhar 8, Cumas Gaeilge 40. Short attempts use the published M/F1/F2/F3 columns (36/30/20/10) on scheme PDF 13, '
                                         'so the Cumas Gaeilge award can take any value from 0 to 40. The letter or email (C) and the conversation partner (D) are flexible forms inside one response, not separate routes.')
            assert card['totalMarks'] == 50
            stamped.append(card['id'])
    assert len(stamped) == 15
    return cards, stamped


def review():
    """The component review record; the inventory reads it beside authored.json."""
    m = material()
    sr = json.loads(SOURCE_REVIEW.read_text())
    legacy = [f'irish-2024-ol-p1-listening-{s[1]}' for s in m['segments']] + [
        f'irish-2024-ol-p1-composition-{g.lower()}-{t[0]}' for g, v in m['groups'].items() for t in v[2]]
    return dict(year=2024, level='ordinary', paperFileid=FILE + '.pdf', schemeFileid=SCHEME_FILE + '.pdf',
                paperSha256=PAPER_SHA, schemeSha256=SCHEME_SHA,
                reviewedPaperPages=list(range(1, 17)), reviewedSchemePages=sr['reviewedSchemePages'], schemeScope=sr['schemeScope'],
                reviewDate=REVIEWED_AT, status='reviewed', fullPaperAndApplicableSchemeVisualSweep=True, selectionDecisions=m['decisions'],
                cardIds=legacy, listeningSegmentCardIds=legacy[:6], compositionRouteCardIds=legacy[6:], printedListeningQuestions=19,
                examStructure=dict(listening=60, composition=100, total=160),
                nonPoolDecisions=sr['nonPoolDecisions'], openIssues=[], audio=sr['audio'], caveats=sr['sourceFindings'],
                boundaries='6 retained listening segment cards carrying all 19 printed questions as separate criteria (3, or 3 + 3) (60); '
                           '9 retained composition titles at 50 (answer any two; no combination cards).')


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
    print(f"Irish Ordinary 2024 Paper 1: {len(data['cardIds'])} retained cards reviewed (19 printed listening questions); the archive remains incomplete.")


if __name__ == '__main__':
    main()
