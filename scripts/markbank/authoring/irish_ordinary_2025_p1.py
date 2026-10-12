#!/usr/bin/env python3
"""Reviewed 2025 Ordinary Paper 1 (Cluastuiscint agus Ceapadóireacht).

Paper PDF 1–16 and the Paper 1 pages of the combined LC001GLP000IV scheme
(PDF 1–13 and 30–31 modified marking) visually reviewed on 2026-10-11. Scheme PDF
14–29 belong to Paper 2. Counts are assertions, not corpus-completeness proof.

The legacy generator already ships 15 cards for this component: six listening
segment cards and the nine composition titles. Their IDs are kept and the six
segments stay the listening card unit (the Bank plays one recording section as one
exercise). `apply_legacy_review` (called by irish_cards.py) joins them to Atlas,
marks each of the 20 printed listening questions as its own 3-mark criterion and
lifts the 2025 composition scheme. `build` adds the 30 two-section selections
printed by “Freagair do rogha dhá cheann de A, B, C, D” beside the legacy file.
"""
from __future__ import annotations
import argparse
import copy
import hashlib
import itertools
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
FILE = 'LC001GLP100IV'
SCHEME_FILE = 'LC001GLP000IV'
OUT = ROOT / 'components/MarkBank/cards/irish/ordinary-2025-p1-authored.json'
SOURCE_REVIEW = ROOT / 'scripts/markbank/authored/irish-ordinary-2025-p1-source-review.json'
REVIEWED_AT = '2026-10-11'
PAPER_SHA = 'f0a9c0dfe1ee9fd67ecef6274050bfffca0114f7c634bb69a4a35e7db03bf212'
SCHEME_SHA = '709a6ffc8a0c6c700ff4132993a2058363ac028f0dca21ae23eef0fa26f95831'
DIRECTIVE = re.compile(r'rogha|roghna|Freagair|Cuir tic|Ainmnigh|Luaigh|\bnó\b|dhá phointe|dhá rud|dó/di|ceann amháin|amháin', re.I)
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
    return dict(kind='source-text', label=ref, title=f'Gaeilge Gnáthleibhéal 2025 · Páipéar 1 · {ref}', pages=pages,
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
    paper_path = ROOT / f'paper-trail-corpus/exampapers/2025/{FILE}.pdf'
    scheme_path = ROOT / f'paper-trail-corpus/markingschemes/2025/{SCHEME_FILE}.pdf'
    assert hashlib.sha256(paper_path.read_bytes()).hexdigest() == PAPER_SHA, 'Paper changed: repeat visual review'
    assert hashlib.sha256(scheme_path.read_bytes()).hexdigest() == SCHEME_SHA, 'Scheme changed: repeat visual review'
    paper, scheme = fitz.open(paper_path), fitz.open(scheme_path)
    texts = [clean(p.get_text()) for p in paper]
    stext = [clean(p.get_text()) for p in scheme]
    # (key, legacy suffix, ref, paper page, topic, [(criterion id, label, paper prompt, scheme anchor)])
    segments = [
        ('L-A-F1', 'a-f1', 'Cuid A · Fógra a hAon', 3, 'irish-1-0', [
            ('q1a', 'Ceist 1(a)', 'Cén stáisiún raidió a chuir amach an fógra seo?', '1. (a) Cén stáisiún raidió'),
            ('q1b', 'Ceist 1(b)', 'Cén t‐ainm a bheidh ar an gclár nua?', '(b) Cén t-ainm a bheidh'),
            ('q2a', 'Ceist 2(a)', 'Cén t‐am a chraolfar an clár nua gach Aoine?', '2. (a) Cén t-am a chraolfar'),
            ('q2b', 'Ceist 2(b)', 'Cén sórt ceoil a bheidh sa stiúideo?', '(b) Cén sórt ceoil')]),
        ('L-A-F2', 'a-f2', 'Cuid A · Fógra a Dó', 3, 'irish-1-0', [
            ('q1a', 'Ceist 1(a)', 'Cén grúpa múinteoirí a chuir amach an fógra seo?', '1. (a) Cén grúpa múinteoirí'),
            ('q1b', 'Ceist 1(b)', 'Cé mhéad scoláire atá á lorg chun páirt a ghlacadh i dtionscadal suimiúil?', '(b) Cé mhéad scoláire'),
            ('q2a', 'Ceist 2(a)', 'Cad a scríobhfaidh na scoláirí ar thorthaí a gcuid oibre?', '2. (a) Cad a scríobhfaidh'),
            ('q2b', 'Ceist 2(b)', 'Cén lá a bheidh an cruinniú ar siúl?', '(b) Cén lá a bheidh')]),
        ('L-B-C1', 'b-c1', 'Cuid B · Comhrá a hAon', 4, 'irish-1-1', [
            ('m1-q1', 'An Chéad Mhír · Ceist 1', 'Cén áit sa bhaile mór a bhfuil Seán ag obair go lánaimseartha mar theagascóir?', '1. Cén áit sa bhaile mór'),
            ('m1-q2', 'An Chéad Mhír · Ceist 2', 'Cén t‐am a thosaíonn Seán ag obair dhá mhaidin sa tseachtain?', '2. Cén t-am a thosaíonn'),
            ('m2-q1', 'An Dara Mír · Ceist 1', 'Cén cluiche a imríonn Aoife leis an gclub áitiúil?', '1. Cén cluiche a imríonn'),
            ('m2-q2', 'An Dara Mír · Ceist 2', 'Cén táille speisialta atá ar fáil do mhic léinn do bhallraíocht trí mhí?', '2. Cén táille speisialta')]),
        ('L-B-C2', 'b-c2', 'Cuid B · Comhrá a Dó', 4, 'irish-1-1', [
            ('m1-q1', 'An Chéad Mhír · Ceist 1', 'Cá fhad a chaith Liam agus a thuismitheoirí in Sydney?', '1. Cá fhad a chaith Liam'),
            ('m1-q2', 'An Chéad Mhír · Ceist 2', 'Cén áit a mbuaileann deirfiúr Liam le hÉireannaigh eile in Sydney?', '2. Cén áit a mbuaileann'),
            ('m2-q1', 'An Dara Mír · Ceist 1', 'Cén áit in Éirinn a bhfuil Maria ina cónaí anois?', '1. Cén áit in Éirinn'),
            ('m2-q2', 'An Dara Mír · Ceist 2', 'Cén uirlis cheoil a sheinneann Maria?', '2. Cén uirlis cheoil')]),
        ('L-C-P1', 'c-p1', 'Cuid C · Píosa a hAon', 5, 'irish-1-2', [
            ('q1', 'Ceist 1', 'Cé a sheol ‘an Scéim Éarlaise agus Aisíoca’ i mí Feabhra na bliana seo caite?', '1. Cé a sheol'),
            ('q2', 'Ceist 2', 'Scríobh síos áit amháin ina bhfuil na meaisíní speisialta ar fáil chun buidéil phlaisteacha fholmha agus cannaí alúmanaim folmha a chur isteach iontu.', '2. Scríobh síos áit amháin')]),
        ('L-C-P2', 'c-p2', 'Cuid C · Píosa a Dó', 5, 'irish-1-2', [
            ('q1', 'Ceist 1', 'Cad atá sa chartlann nua atá curtha ar fáil ag Gael Linn?', '1. Cad atá sa chartlann'),
            ('q2', 'Ceist 2', 'Cén bhliain a bunaíodh Gael Linn?', '2. Cén bhliain a bunaíodh')]),
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
        for i, (cid, label, prompt, anchor) in enumerate(seg[5]):
            chunk, pages = next(chunks)
            assert comparable(prompt) in comparable(texts[seg[3] - 1]), (seg[0], cid)
            assert chunk.endswith('mharc') and '3 mharc' in chunk, (seg[0], cid, chunk[-60:])
            seg[5][i] = (cid, label, prompt, chunk, pages)
    assert sum(len(seg[5]) for seg in segments) == 20
    general = 'Nóta (scheme PDF 7): ' + stext[6].split('Nóta:', 1)[1].split('Cuid A (24 marc)', 1)[0].strip()
    assert general.endswith('chomh maith.')

    marking = stext[9][stext[9].index('Freagair do rogha dhá cheann'):]
    symbols, table40, table_short = [re.sub(r'^\d+\s', '', t) for t in stext[10:13]]
    smm = re.sub(r'^\d+\s', '', stext[30])
    marking = re.sub(r'\s+\d+$', '', marking)
    assert 'Tasc = 2 mharc' in marking and 'Ábhar = 8 marc' in marking and 'Cumas Gaeilge = 40 marc' in marking
    assert all(x in table_short for x in ['M F1 F2 F3', '38 34 29 19 10']) and '34-40' in smm and '95% 38' in table40
    head = ('Treoracha: Ní mór do na hiarrthóirí cúram a dhéanamh de chruinneas na teanga. Caillfear marcanna má bhítear faillitheach ann. '
            'Ní mór ceangal cinnte leanúnach a bheith ann idir an teideal a roghnaítear agus an t‐ábhar a scríobhtar.\n\n'
            'Freagair do rogha dhá cheann de A, B, C, D anseo.')
    groups = {
        'A': ('Giota Leanúnach/Blag', 'Scríobh giota leanúnach nó blag (leathleathanach nó mar sin) ar cheann amháin de na hábhair seo.', [
            ('i', 'Siopadóireacht.'), ('ii', 'Áit shuimiúil.'), ('iii', 'Pearsa spóirt a thaitníonn go mór liom.')]),
        'B': ('Scéal', 'Ceap scéal (leathleathanach nó mar sin) a mbeadh ceann amháin de na sleachta seo a leanas oiriúnach mar thús leis.', [
            ('i', 'Bhí sceitimíní áthais orm. D’éirigh liom dhá thicéad a fháil don cheolchoirm …'),
            ('ii', 'Is cuimhin liom go maith an lá sin. Tháinig athrú mór ar mo shaol an lá sin …')]),
        'C': ('Litir/Ríomhphost', None, [
            ('i', 'D’eagraigh Comhairle na nDaltaí a lán imeachtaí i do scoil i rith na bliana. Bhí tú féin páirteach i gcuid de na himeachtaí sin.\nScríobh an litir/an ríomhphost (leathleathanach nó mar sin) a chuirfeá chuig cara leat ag insint dó/di faoi na himeachtaí a d’eagraigh Comhairle na nDaltaí agus faoin bpáirt a ghlac tú féin i gcuid de na himeachtaí sin.'),
            ('ii', 'Thit sneachta trom i do cheantar le déanaí. Ní raibh tú féin ná do mhuintir ábalta bogadh amach as bhur gceantar féin ar feadh cúpla lá.\nScríobh an litir/an ríomhphost (leathleathanach nó mar sin) a chuirfeá chuig cara leat ag insint dó/di faoin titim shneachta sin agus faoi mar a chaith tú féin agus do mhuintir na laethanta nuair a bhí sneachta trom ann.')]),
        'D': ('Comhrá', None, [
            ('i', 'Léigh tú féin agus do chara blag ar líne. Cheap tú go raibh an blag suimiúil ach níor aontaigh do chara leat. Scríobh an comhrá (leathleathanach nó mar sin) a bheadh agat le do chara faoin ábhar sin.'),
            ('ii', 'Tá post páirtaimseartha agat agus tú i mbliain na hArdteistiméireachta. Níl do thuismitheoirí sásta faoin méid ama a chaitheann tú ag obair i do phost. Scríobh an comhrá (leathleathanach nó mar sin) a bheadh agat le do thuismitheoirí faoin ábhar sin.')]),
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
    """Join the 15 retained legacy cards to Atlas and lift the 2025 scheme (IDs, totals and topics unchanged)."""
    m = material()
    by_id = {c['id']: c for c in cards}
    stamped = []
    for key, suffix, ref, page, topic, questions in m['segments']:
        card = by_id[f'irish-2025-ol-p1-listening-{suffix}']
        assert card['topicId'] == topic and card['totalMarks'] == 3 * len(questions), card['id']
        criteria = []
        for cid, label, prompt, chunk, pages in questions:
            values = {int(v) for v in re.findall(r'= (\d) mharc', chunk)}
            criteria.append(criterion(cid, label, 3, [chunk, m['general']], 'exact', permitted=sorted({0, 3} | values)))
        pages = sorted({p for q in questions for p in q[4]})
        card.update(atlasQuestionId=key, reviewedAt=REVIEWED_AT, reviewedPaperPages=[page], paperPage=page,
                    schemePage=pages[0], schemePages=pages, sourceMaterial=source(f'Cluastuiscint {ref}', [page]), criteria=criteria,
                    markingGuideNote='The listed responses and tariffs come from the 2025 SEC marking scheme; equivalent wording with the same meaning is accepted. '
                                     'Each printed question is marked at its own published 3-mark tariff. ' + LANGUAGE)
        stamped.append(card['id'])
    c = m['composition']
    for group, (form, instruction, titles) in m['groups'].items():
        for roman, title in titles:
            card = by_id[f'irish-2025-ol-p1-composition-{group.lower()}-{roman}']
            body = m['head'] + f'\n\n{group} · {form} (50 marc)\n' + (instruction + '\n' if instruction else '') + f'({roman}) {title}'
            card.update(atlasQuestionId=f'W-{group}-{roman}', reviewedAt=REVIEWED_AT, reviewedPaperPages=[7], paperPage=7,
                        schemePage=10, schemePages=[10, 11, 12, 13],
                        questionText=body + f'\n\nAn rogha don chárta seo: {group}({roman}).',
                        sourceMaterial=source(f'Ceapadóireacht {group}({roman})', [7]),
                        taskRequirements=['Lean an fhoirm scríbhneoireachta a iarrtar sa cheist.',
                                          'Coinnigh ceangal cinnte leanúnach idir an teideal agus an t-ábhar.', 'Leathleathanach nó mar sin.'],
                        criteria=[criterion('tasc', 'An Tasc', 2, [c['marking'].split('An tÁbhar (8 marc)')[0]], permitted=[0, 2]),
                                  criterion('abhar', 'An tÁbhar', 8, [c['marking'].split('An tÁbhar (8 marc)', 1)[1].split('An Cumas Gaeilge (40 marc)')[0]], 'indicative'),
                                  criterion('gaeilge', 'An Cumas Gaeilge', 40, [c['marking'].split('An Cumas Gaeilge (40 marc)', 1)[1], c['symbols'], c['table40'], c['table_short'],
                                            'Scéim Mharcála Mhodhnaithe (scheme PDF 30–31): eligible candidates are assessed on named grammar features (bands 34–40 … 0–3); spelling is not counted.'])],
                        markingGuideNote='Whole 50-mark composition: Tasc 2, Ábhar 8, Cumas Gaeilge 40. Short attempts use the published M/F1/F2/F3 columns (36/30/20/10) on scheme PDF 13, '
                                         'so the Cumas Gaeilge award can take any value from 0 to 40. The letter or email (C) and the conversation partner (D) are flexible forms inside one response, not separate routes.')
            assert card['totalMarks'] == 50
            stamped.append(card['id'])
    assert len(stamped) == 15
    return cards, stamped


def build(legacy_cards):
    """The 30 printed two-section selections, built from the reviewed legacy titles."""
    m = material()
    by_id = {c['id']: c for c in legacy_cards}
    singles = {g: [by_id[f'irish-2025-ol-p1-composition-{g.lower()}-{t[0]}'] for t in v[2]] for g, v in m['groups'].items()}
    cards = []
    for g1, g2 in itertools.combinations('ABCD', 2):
        for m1, m2 in itertools.product(singles[g1], singles[g2]):
            members = [m1, m2]
            key = '-'.join(x['atlasQuestionId'].removeprefix('W-') for x in members)
            criteria = []
            for x in members:
                prefix = x['atlasQuestionId'].lower().removeprefix('w-') + '-'
                for old in x['criteria']:
                    cc = copy.deepcopy(old)
                    cc['id'] = prefix + cc['id']
                    cc['label'] = x['questionRef'].removeprefix('2025 OL Paper 1 ') + ' · ' + cc['label']
                    criteria.append(cc)
            topics = list(dict.fromkeys(t for x in members for t in [x['topicId'], *x.get('additionalTopicIds', [])]))
            ref = ' + '.join(x['questionRef'].removeprefix('2025 OL Paper 1 ') for x in members)
            cards.append(dict(
                id='irish-2025-ol-p1-composition-' + key.lower(), year=2025, level='ordinary', paper=1, section='1',
                atlasQuestionId=f'W-{key}', questionRef=f'2025 OL Paper 1 {ref}',
                questionText='Freagair do rogha dhá cheann de A, B, C, D anseo.\n\nAn rogha don chárta seo: ' + ref + '\n\n' +
                             '\n\n'.join(x['questionRef'].removeprefix('2025 OL Paper 1 ') + '\n' + x['questionText'].split('\n\n')[2] for x in members),
                totalMarks=100, topicId=topics[0], **({'additionalTopicIds': topics[1:]} if topics[1:] else {}),
                conceptId='irish-ol-p1-composition-' + key.lower(), paperFileid=FILE, schemeFileid=SCHEME_FILE,
                schemePage=10, schemePages=[10, 11, 12, 13], reviewedAt=REVIEWED_AT, reviewedPaperPages=[7],
                taskRequirements=[r for x in members for r in x['taskRequirements']], criteria=criteria,
                markingGuideNote='One permitted printed selection: two whole 50-mark compositions from two different sections. '
                                 'Each keeps its own Tasc, Ábhar and Cumas Gaeilge awards; alternative routes are not added together.',
                sourceMaterial=source(f'Ceapadóireacht {ref}', [7]), memberCardIds=[x['id'] for x in members]))
    assert len(cards) == 30 and all(sum(c['maxMarks'] for c in card['criteria']) == 100 for card in cards)
    sr = json.loads(SOURCE_REVIEW.read_text())
    legacy = [f'irish-2025-ol-p1-listening-{s[1]}' for s in m['segments']] + [
        f'irish-2025-ol-p1-composition-{g.lower()}-{t[0]}' for g, v in m['groups'].items() for t in v[2]]
    review = dict(year=2025, level='ordinary', paperFileid=FILE + '.pdf', schemeFileid=SCHEME_FILE + '.pdf',
                  paperSha256=PAPER_SHA, schemeSha256=SCHEME_SHA,
                  reviewedPaperPages=list(range(1, 17)), reviewedSchemePages=sr['reviewedSchemePages'], schemeScope=sr['schemeScope'],
                  reviewDate=REVIEWED_AT, status='reviewed', fullPaperAndApplicableSchemeVisualSweep=True, selectionDecisions=m['decisions'],
                  legacyCardIds=legacy, listeningSegmentCardIds=legacy[:6], compositionRouteCardIds=legacy[6:],
                  pairedRouteCardIds=[c['id'] for c in cards], printedListeningQuestions=20,
                  examStructure=dict(listening=60, composition=100, total=160),
                  nonPoolDecisions=sr['nonPoolDecisions'], openIssues=[], audio=sr['audio'], caveats=sr['sourceFindings'],
                  boundaries='6 retained listening segment cards carrying all 20 printed questions as separate 3-mark criteria (60); '
                             '9 retained composition titles at 50; 30 two-section selections at 100.')
    return dict(review=review, cards=cards)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    legacy = json.loads((ROOT / 'components/MarkBank/cards/irish/authored.json').read_text())['cards']
    assert all(c.get('atlasQuestionId') for c in legacy if c['id'].startswith('irish-2025-ol-p1-')), 'Run irish_cards.py first'
    data = build(legacy)
    content = json.dumps(data, ensure_ascii=False, indent=2) + '\n'
    if args.check:
        assert OUT.exists() and OUT.read_text() == content, f'Stale output: {OUT}'
    else:
        OUT.write_text(content)
    print(f"Irish Ordinary 2025 Paper 1: {len(data['cards'])} added selections (+15 retained legacy cards); the archive remains incomplete.")


if __name__ == '__main__':
    main()
