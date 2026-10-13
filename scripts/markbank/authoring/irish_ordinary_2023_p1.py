#!/usr/bin/env python3
"""Reviewed 2023 Ordinary Paper 1 (Cluastuiscint agus Ceapadóireacht).

Paper PDF 1–16 and the Paper 1 pages of the combined LC001GLP000IV scheme
(PDF 1–13 and 33–34 modified marking) visually reviewed on 2026-10-13. Scheme PDF
14–32 belong to Paper 2. Counts are assertions, not corpus-completeness proof.
Same method as irish_ordinary_2024_p1.py; Fógra a Dó Ceist 2 is one 3 + 3 question.
The directive scan also catches every “dhá” count line.

The legacy generator already ships 15 cards for this component: six listening
segment cards and the nine composition titles. Their IDs are kept and the six
segments stay the listening card unit (the Bank plays one recording section as one
exercise). `apply_legacy_review` (called by irish_cards.py) joins them to Atlas,
marks each of the 19 printed listening questions as its own criterion (3, or 3 + 3) and
lifts the 2023 composition scheme. “Freagair do rogha dhá cheann de A, B, C, D” is
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
OUT = ROOT / 'scripts/markbank/authored/irish-ordinary-2023-p1-component-review.json'
SOURCE_REVIEW = ROOT / 'scripts/markbank/authored/irish-ordinary-2023-p1-source-review.json'
REVIEWED_AT = '2026-10-13'
PAPER_SHA = 'ab22a0c2680b17586215f51d13b58c7bb28b88fbcc9685752a8d19951275a2da'
SCHEME_SHA = '5b37330f65f494e8a6442adf9983032df870f310a39fdfecc9c2eef2faed5ad8'
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
    return dict(kind='source-text', label=ref, title=f'Gaeilge Gnáthleibhéal 2023 · Páipéar 1 · {ref}', pages=pages,
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
    paper_path = ROOT / f'paper-trail-corpus/exampapers/2023/{FILE}.pdf'
    scheme_path = ROOT / f'paper-trail-corpus/markingschemes/2023/{SCHEME_FILE}.pdf'
    assert hashlib.sha256(paper_path.read_bytes()).hexdigest() == PAPER_SHA, 'Paper changed: repeat visual review'
    assert hashlib.sha256(scheme_path.read_bytes()).hexdigest() == SCHEME_SHA, 'Scheme changed: repeat visual review'
    paper, scheme = fitz.open(paper_path), fitz.open(scheme_path)
    texts = [clean(p.get_text()) for p in paper]
    stext = [clean(p.get_text()) for p in scheme]
    # (key, legacy suffix, ref, paper page, topic, [(criterion id, label, paper prompt, scheme anchor, marks)])
    segments = [
        ('L-A-F1', 'a-f1', 'Cuid A · Fógra a hAon', 3, 'irish-1-0', [
            ('q1a', 'Ceist 1(a)', 'Cén bhliain a sheol Gaelchultúr club leabhar ar líne?', '1. (a) Cén bhliain a sheol', 3),
            ('q1b', 'Ceist 1(b)', 'Scríobh síos cineál amháin leabhair a roghnaítear mar leabhar na míosa.', '(b) Scríobh síos cineál amháin leabhair', 3),
            ('q2a', 'Ceist 2(a)', 'Cén suíomh gréasáin ar féidir leis na baill leabhar na míosa a cheannach air?', '2. (a) Cén suíomh gréasáin', 3),
            ('q2b', 'Ceist 2(b)', 'Cá fhad a thógann sé clárú don chlub leabhar seo ar líne?', '(b) Cá fhad a thógann sé', 3)]),
        ('L-A-F2', 'a-f2', 'Cuid A · Fógra a Dó', 3, 'irish-1-0', [
            ('q1a', 'Ceist 1(a)', 'Cén ollscoil a chuir amach an fógra seo?', '1. (a) Cén ollscoil', 3),
            ('q1b', 'Ceist 1(b)', 'Cén t-am a dtosóidh na cainteanna an lá sin?', '(b) Cén t-am a dtosóidh', 3),
            ('q2', 'Ceist 2', 'Luaigh dhá áit a fheicfidh na scoláirí ar an turas timpeall an champais.', '2. Luaigh dhá áit', 6)]),
        ('L-B-C1', 'b-c1', 'Cuid B · Comhrá a hAon', 4, 'irish-1-1', [
            ('m1-q1', 'An Chéad Mhír · Ceist 1', 'Cén t-ainm atá ar an ngrúpa timpeallachta áitiúil a d’eagraigh an glantachán trá?', '1. Cén t-ainm atá ar an ngrúpa', 3),
            ('m1-q2', 'An Chéad Mhír · Ceist 2', 'Cén cineál bruscair is mó a bhailigh siad ar an trá?', '2. Cén cineál bruscair', 3),
            ('m2-q1', 'An Dara Mír · Ceist 1', 'Cá raibh Íde coicís ó shin?', '1. Cá raibh Íde', 3),
            ('m2-q2', 'An Dara Mír · Ceist 2', 'Scríobh síos rud amháin a deir Íde a d’fhág a lán daoine ina ndiaidh nuair a bhí siad ag imeacht abhaile maidin Dé Luain.', '2. Scríobh síos rud amháin a deir Íde', 3)]),
        ('L-B-C2', 'b-c2', 'Cuid B · Comhrá a Dó', 4, 'irish-1-1', [
            ('m1-q1', 'An Chéad Mhír · Ceist 1', 'Cén uair a tháinig Gráinne ar ais ó Mhaidrid?', '1. Cén uair a tháinig Gráinne', 3),
            ('m1-q2', 'An Chéad Mhír · Ceist 2', 'Cá fhad a mhaireadh na ranganna Spáinnise gach maidin?', '2. Cá fhad a mhaireadh', 3),
            ('m2-q1', 'An Dara Mír · Ceist 1', 'Luaigh áit amháin a dtéadh Gráinne agus Maria ar an Satharn.', '1. Luaigh áit amháin', 3),
            ('m2-q2', 'An Dara Mír · Ceist 2', 'Scríobh síos an rud nach bhfuil Gráinne ag tnúth leis.', '2. Scríobh síos an rud nach bhfuil', 3)]),
        ('L-C-P1', 'c-p1', 'Cuid C · Píosa a hAon', 5, 'irish-1-2', [
            ('q1', 'Ceist 1', 'Cén áit i mBaile Átha Cliath a raibh Gradaim Phodchraoltaí na hÉireann ar siúl?', '1. Cén áit i mBaile Átha Cliath', 3),
            ('q2', 'Ceist 2', 'Cá gcraoltar an podchraoladh Gaeilge An Spota Dubh?', '2. Cá gcraoltar', 3)]),
        ('L-C-P2', 'c-p2', 'Cuid C · Píosa a Dó', 5, 'irish-1-2', [
            ('q1', 'Ceist 1', 'Cathain a fuair Pelé bás?', '1. Cathain a fuair Pelé bás?', 3),
            ('q2', 'Ceist 2', 'Cén aois a bhí ag Pelé nuair a d’imir sé i gCorn an Domhain den chéad uair?', '2. Cén aois a bhí ag Pelé', 3)]),
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
    # The boxed section heading is stored after the page body; it is not part of the marking text.
    marking = marking.removesuffix('Cuid II An Cheapadóireacht 100 marc').strip()
    assert 'Cuid II' not in marking
    assert 'Tasc = 2 mharc' in marking and 'Ábhar = 8 marc' in marking and 'Cumas Gaeilge = 40 marc' in marking
    assert all(x in table_short for x in ['M F1 F2 F3', '38 34 29 19 10']) and '34-40' in smm and '95% 38' in table40
    head = ('Treoracha: Ní mór do na hiarrthóirí cúram a dhéanamh de chruinneas na teanga. Caillfear marcanna má bhítear faillitheach ann. '
            'Ní mór ceangal cinnte leanúnach a bheith ann idir an teideal a roghnaítear agus an t-ábhar a scríobhtar.\n\n'
            'Freagair do rogha dhá cheann de A, B, C, D anseo.')
    assert comparable(head.split('\n\n')[0].removeprefix('Treoracha: ')) in comparable(texts[5]) and comparable(head.split('\n\n')[1]) in comparable(texts[6])
    groups = {
        'A': ('Giota Leanúnach/Blag', 'Scríobh giota leanúnach nó blag (leathleathanach nó mar sin) ar cheann amháin de na hábhair seo.', [
            ('i', 'An áit is fearr liom ar domhan.'), ('ii', 'Na rudaí a chuireann brón orm.'), ('iii', 'Bronntanas iontach a fuair mé.')]),
        'B': ('Scéal', 'Ceap scéal (leathleathanach nó mar sin) a mbeadh ceann amháin de na sleachta seo a leanas oiriúnach mar thús leis.', [
            ('i', 'Bhí gach rud i mo mhála agam. Bhí mé réidh le himeacht. Go tobann, bhuail an fón …'),
            ('ii', 'Bhí an dioscó ar siúl san óstán. Níor tugadh cead isteach dom. Bhí mé i gcruachás …')]),
        'C': ('Litir/Ríomhphost', None, [
            ('i', 'Bhí ceolchoirm ar siúl i halla na scoile le déanaí. Ghlac tú féin páirt sa cheolchoirm sin.\nScríobh an litir/an ríomhphost (leathleathanach nó mar sin) a chuirfeá chuig do dheartháir/do dheirfiúr ag insint dó/di faoin gceolchoirm sin agus faoin airgead a bhailigh sibh.'),
            ('ii', 'Bhog teaghlach ó thír eile isteach i do cheantar le déanaí. Scríobh an litir/an ríomhphost (leathleathanach nó mar sin) a chuirfeá chuig cara leat ag insint dó/di faoin teaghlach sin agus faoin gcineál saoil atá acu anseo in Éirinn.')]),
        'D': ('Comhrá', None, [
            ('i', 'Tá post páirtaimseartha agat. Ceapann do thuismitheoirí go bhfuil tú ag sábháil cuid den airgead a thuilleann tú ach caitheann tú an t-airgead go léir.\nScríobh an comhrá (leathleathanach nó mar sin) a bheadh agat le do thuismitheoirí faoin ábhar sin.'),
            ('ii', 'Tá tairiscintí CAO díreach faighte agat féin agus ag do chara. Fuair tú féin do chéad rogha ach ní bhfuair do chara an cúrsa a bhí ag teastáil uaidh/uaithi. Scríobh an comhrá (leathleathanach nó mar sin) a bheadh agat le do chara faoin ábhar sin.')]),
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
    """Join the 15 retained legacy cards to Atlas and lift the 2023 scheme (IDs, totals and topics unchanged).

    schemeFileid names the Ordinary scheme: without it the Atlas answer map falls
    back to the Higher scheme file."""
    m = material()
    by_id = {c['id']: c for c in cards}
    stamped = []
    for key, suffix, ref, page, topic, questions in m['segments']:
        card = by_id[f'irish-2023-ol-p1-listening-{suffix}']
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
                    markingGuideNote='The listed responses and tariffs come from the 2023 SEC marking scheme; equivalent wording with the same meaning is accepted. '
                                     'Each printed question is marked at its own published tariff (3, or 3 + 3 for two places). ' + LANGUAGE)
        stamped.append(card['id'])
    c = m['composition']
    for group, (form, instruction, titles) in m['groups'].items():
        for roman, title in titles:
            card = by_id[f'irish-2023-ol-p1-composition-{group.lower()}-{roman}']
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
                                         'so the Cumas Gaeilge award can take any value from 0 to 40. The letter or email and its recipient wording (C), and the dó/di and uaidh/uaithi forms, are flexible forms inside one response, not separate routes.')
            assert card['totalMarks'] == 50
            stamped.append(card['id'])
    assert len(stamped) == 15
    return cards, stamped


def review():
    """The component review record; the inventory reads it beside authored.json."""
    m = material()
    sr = json.loads(SOURCE_REVIEW.read_text())
    legacy = [f'irish-2023-ol-p1-listening-{s[1]}' for s in m['segments']] + [
        f'irish-2023-ol-p1-composition-{g.lower()}-{t[0]}' for g, v in m['groups'].items() for t in v[2]]
    return dict(year=2023, level='ordinary', paperFileid=FILE + '.pdf', schemeFileid=SCHEME_FILE + '.pdf',
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
    print(f"Irish Ordinary 2023 Paper 1: {len(data['cardIds'])} retained cards reviewed (19 printed listening questions); the archive remains incomplete.")


if __name__ == '__main__':
    main()
