#!/usr/bin/env python3
"""Reviewed 2026 Ordinary Paper 1 (Cluastuiscint agus Ceapadóireacht).

Paper PDF 1–16 and the Paper 1 pages of the combined LC001GLP100IV scheme
(PDF 1–13, 34–35 modified marking, 36–40 blank) visually reviewed on 2026-10-11.
Counts are assertions, not corpus-completeness proof. Each printed listening
question is one 3-mark card (the reader groups a recording section's cards);
the nine printed composition titles are whole 50-mark routes, and the closed
“any two of A, B, C, D” instruction is expanded mechanically into its 30 full
100-mark selections (one title from each of two different sections).
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
SCHEME_FILE = 'LC001GLP100IV'
OUT = ROOT / 'components/MarkBank/cards/irish/ordinary-2026-p1-authored.json'
SOURCE_REVIEW = ROOT / 'scripts/markbank/authored/irish-ordinary-2026-p1-source-review.json'
REVIEWED_AT = '2026-10-11'
DIRECTIVE = re.compile(r'rogha|roghna|Freagair|Cuir tic|Ainmnigh|Luaigh|\bchoose\b|\beither\b|\bany\b|one of|\bnó\b|dhá phointe|trí phointe|dhá rud|dó/di|Cuir ciorcal|dhá thagairt|dhá ch|dhá dh|an dá|ceann amháin|amháin', re.I)
AUDIO_URL = 'https://www.examinations.ie/archive/exampapers/2026/LC001ZLP017IV.mp3'


def clean(text):
    return re.sub(r'\s+', ' ', text).strip()


def comparable(text):
    return re.sub(r'[^\w]+', '', text.lower())


def criterion(id, label, marks, guidance, kind='quality', permitted=None):
    return dict(id=id, label=label, kind='award', maxMarks=marks, permittedMarks=permitted or list(range(marks + 1)),
                guidanceKind=kind, guidance=guidance)


def selection_decisions(paper):
    decisions = json.loads(SOURCE_REVIEW.read_text())['selectionDecisions']
    expected = {(d['page'], d['raw']) for d in decisions}
    found = {(i, clean(line)) for i, page in enumerate(paper, 1)
             for line in page.get_text().splitlines() if DIRECTIVE.search(clean(line))}
    assert found == expected, ('Unclassified/stale selection directives', found - expected, expected - found)
    return decisions


def chunks(text, starts, stop=None):
    out, rest = [], text
    for i, start in enumerate(starts):
        assert start in rest, start
        rest = rest[rest.index(start):]
        end = starts[i + 1] if i + 1 < len(starts) else stop
        part = rest[:rest.index(end)] if end else rest
        out.append(re.sub(r'\s*(\d\.\s*\([ab]\)|\d\.|\([ab]\)|An Dara Mír|An Dara Mír \d\.)\s*$', '', clean(part)))
        rest = rest[len(part):] if end else ''
    return out


def build():
    import fitz
    paper_path = ROOT / f'paper-trail-corpus/exampapers/2026/{FILE}.pdf'
    scheme_path = ROOT / f'paper-trail-corpus/markingschemes/2026/{SCHEME_FILE}.pdf'
    assert hashlib.sha256(paper_path.read_bytes()).hexdigest() == 'a8daeeef20366ea4ab134dd62f9e327ddb0301035e0d9f5b540e484ce839f820', 'Paper changed: repeat visual review'
    assert hashlib.sha256(scheme_path.read_bytes()).hexdigest() == '5cd471bc9b0b782f6f6e84ac41531a1716ff7e2790c94925ad321d8a82a76117', 'Scheme changed: repeat visual review'
    paper = fitz.open(paper_path)
    scheme = fitz.open(scheme_path)
    texts = [clean(p.get_text()) for p in paper]
    stext = [clean(p.get_text()) for p in scheme]
    cards = []

    def add(key, slug, ref, prompt, topic, pages, scheme_pages, criteria, requirements, note, extra_topics=None, **extra):
        card = dict(id=f'irish-2026-ol-p1-{slug}', year=2026, level='ordinary', paper=1, section='1',
                    atlasQuestionId=key, questionRef=f'2026 OL Paper 1 {ref}', questionText=prompt,
                    totalMarks=sum(c['maxMarks'] for c in criteria), topicId=topic,
                    **({'additionalTopicIds': extra_topics} if extra_topics else {}),
                    conceptId=f'irish-ol-p1-{slug}', paperFileid=FILE, schemeFileid=SCHEME_FILE,
                    schemePage=scheme_pages[0], schemePages=scheme_pages, reviewedAt=REVIEWED_AT,
                    reviewedPaperPages=pages, taskRequirements=requirements, criteria=criteria, markingGuideNote=note,
                    sourceMaterial=dict(kind='source-text', label=ref, title=f'Gaeilge Gnáthleibhéal 2026 · Páipéar 1 · {ref}',
                                        pages=pages, attribution='© State Examinations Commission.',
                                        presentationNote='Original examination pages from the official question paper.'),
                    **extra)
        cards.append(card)
        return card

    # ---- Cuid I: An Chluastuiscint (60) -------------------------------------------------
    language = ('Scheme PDF 3 and 9: “Bainfear ó 0 go 6 ar chaighdeán na Gaeilge.” This 0–6 deduction applies once to the whole '
                'listening section (Tuiscint 60 − Cumas Gaeilge 0–6), never inside a single card.')
    a = stext[6].split('FÓGRA A hAON (12 mharc)', 1)[1]
    f1 = chunks(a.split('FÓGRA A DÓ (12 mharc)', 1)[0], ['Cén duine ón trucail', 'Scríobh síos lá amháin', 'Cé mhéad san uair', 'Cad é an dáta deireanach'])
    f2 = chunks(a.split('FÓGRA A DÓ (12 mharc)', 1)[1], ['Cén coláiste i mBaile', 'Cén deontas', 'Cad a bheidh le déanamh', 'Cén áit sa choláiste'])
    b = stext[7].split('COMHRÁ A hAON (12 mharc)', 1)[1]
    c1, c2 = b.split('COMHRÁ A DÓ (12 mharc)', 1)
    c1q = chunks(c1, ['Cad a bhris Pól', 'Cad a bhí ar siúl sa chlubtheach', 'Cén cineál saoire', 'Cad a bhí ar Phól a chur ar fáil'])
    c2q = chunks(c2, ['Cén uirlis a sheinn', 'Conas a mhothaigh Sinéad', 'Cé a bheartaigh dul', 'Cén saghas banna ceoil'])
    c = stext[8].split('PÍOSA A hAON (6 mharc)', 1)[1]
    p1 = chunks(c.split('PÍOSA A DÓ (6 mharc)', 1)[0], ['Cén cineál cláir teilifíse', 'Cén t-am a chraoltar'])
    p2 = chunks(c.split('PÍOSA A DÓ (6 mharc)', 1)[1], ['Cén oíche speisialta', 'Cad a d’imir daoine'], stop='Bainfear ó 0 go 6')
    intro = {
        'A': 'Cuid A\nCloisfidh tú dhá fhógra sa chuid seo. Cloisfidh tú gach fógra díobh faoi dhó. Beidh sos ann leis na freagraí a scríobh tar éis na chéad éisteachta agus tar éis an dara héisteacht.',
        'B': 'Cuid B\nCloisfidh tú dhá chomhrá sa chuid seo. Cloisfidh tú gach comhrá díobh faoi dhó. Cloisfidh tú an comhrá ó thosach deireadh an chéad uair. Ansin cloisfidh tú ina dhá mhír é. Beidh sos ann leis na freagraí a scríobh tar éis gach míre díobh.',
        'C': 'Cuid C\nCloisfidh tú dhá phíosa nuachta sa chuid seo. Cloisfidh tú gach píosa díobh faoi dhó. Beidh sos ann leis na freagraí a scríobh tar éis na chéad éisteachta agus tar éis an dara héisteacht.'}
    segments = [
        ('L-A-F1', 'listening-a-f1', 'Cuid A · Fógra a hAon', 'FÓGRA A hAON', 3, 'irish-1-0', 'A', 7, [
            ('1a', '1. (a) Cén duine ón trucail chaife Sos Beag a chuir amach an fógra seo?', f1[0]),
            ('1b', '1. (b) Scríobh síos lá amháin a bheidh an t‐oibrí barista ag obair.', f1[1]),
            ('2a', '2. (a) Cé mhéad san uair a thuillfidh an t‐oibrí barista?', f1[2]),
            ('2b', '2. (b) Cad é an dáta deireanach le haghaidh na n‐iarratas?', f1[3])]),
        ('L-A-F2', 'listening-a-f2', 'Cuid A · Fógra a Dó', 'FÓGRA A DÓ', 3, 'irish-1-0', 'A', 7, [
            ('1a', '1. (a) Cén coláiste i mBaile Átha Cliath a chuir amach an fógra seo?', f2[0]),
            ('1b', '1. (b) Cén deontas a bheidh ar fáil do gach mac léinn a gheobhaidh áit ar an scéim seo?', f2[1]),
            ('2a', '2. (a) Cad a bheidh le déanamh ag na hiarratasóirí a bhainfidh áit amach ar an ngearrliosta?', f2[2]),
            ('2b', '2. (b) Cén áit sa choláiste a bhfuil gach eolas faoin scéim seo ar fáil?', f2[3])]),
        ('L-B-C1-M1', 'listening-b-c1-first', 'Cuid B · Comhrá a hAon · An Chéad Mhír', 'COMHRÁ A hAON\nAn Chéad Mhír', 4, 'irish-1-1', 'B', 8, [
            ('1', '1. Cad a bhris Pól coicís ó shin?', c1q[0]), ('2', '2. Cad a bhí ar siúl sa chlubtheach an oíche sin?', c1q[1])]),
        ('L-B-C1-M2', 'listening-b-c1-second', 'Cuid B · Comhrá a hAon · An Dara Mír', 'COMHRÁ A hAON\nAn Dara Mír', 4, 'irish-1-1', 'B', 8, [
            ('1', '1. Cén cineál saoire i ndeisceart na Fraince a bhí beartaithe ag Pól agus ag a chairde?', c1q[2]),
            ('2', '2. Cad a bhí ar Phól a chur ar fáil don chomhlacht taistil mar fhianaise ar an ngortú?', c1q[3])]),
        ('L-B-C2-M1', 'listening-b-c2-first', 'Cuid B · Comhrá a Dó · An Chéad Mhír', 'COMHRÁ A DÓ\nAn Chéad Mhír', 4, 'irish-1-1', 'B', 8, [
            ('1', '1. Cén uirlis a sheinn Sinéad sa chraobhchomórtas faoi ocht mbliana déag?', c2q[0]), ('2', '2. Conas a mhothaigh Sinéad ar an stáitse?', c2q[1])]),
        ('L-B-C2-M2', 'listening-b-c2-second', 'Cuid B · Comhrá a Dó · An Dara Mír', 'COMHRÁ A DÓ\nAn Dara Mír', 4, 'irish-1-1', 'B', 8, [
            ('1', '1. Cé a bheartaigh dul in éineacht le Sinéad chun an réalta cheoil Ed Sheeran a fheiceáil?', c2q[2]),
            ('2', '2. Cén saghas banna ceoil a sháraigh an churiarracht dhomhanda Guinness?', c2q[3])]),
        ('L-C-P1', 'listening-c-p1', 'Cuid C · Píosa a hAon', 'PÍOSA A hAON', 5, 'irish-1-2', 'C', 9, [
            ('1', '1. Cén cineál cláir teilifíse é Ros na Rún?', p1[0]), ('2', '2. Cén t‐am a chraoltar Ros na Rún ar TG4 gach Máirt agus Déardaoin?', p1[1])]),
        ('L-C-P2', 'listening-c-p2', 'Cuid C · Píosa a Dó', 'PÍOSA A DÓ', 5, 'irish-1-2', 'C', 9, [
            ('1', '1. Cén oíche speisialta a bhí ar siúl den chéad uair ar an aonú lá is fiche de mhí na Samhna anuraidh?', p2[0]),
            ('2', '2. Cad a d’imir daoine i gclubanna áirithe ar an oíche speisialta sin?', p2[1])]),
    ]
    audio = dict(kind='source-audio', title='Triail Chluastuisceana 2026', playbackUrl=AUDIO_URL, secFileid='LC001ZLP017IV.mp3',
                 canonicalUrl=AUDIO_URL, attribution='© State Examinations Commission.',
                 presentationNote='Official Higher and Ordinary Level recording (one recording for the whole listening test). Play the part named on the card.')
    requirements = ['Éist leis an taifeadadh oifigiúil.', 'Freagair i nGaeilge, ach amháin nuair nach gá sin.']
    for key, slug, ref, heading, page, topic, part, spage, questions in segments:
        for n, prompt, chunk in questions:
            assert comparable(prompt.split(' ', 1)[1]) in comparable(texts[page - 1]), (key, n)
            assert '3 mharc' in chunk and comparable(re.sub(r'^\d\. (\([ab]\) )?', '', prompt)[:25]) in comparable(chunk), (key, n, chunk[:60])
            add(f'{key}-{n}', f'{slug}-q{n}', f'{ref} · Ceist {n[0]}' + (f'({n[1]})' if len(n) > 1 else ''),
                intro[part] + '\n\n' + heading + '\n' + prompt, topic, [page], [spage],
                [criterion('eolas', 'Tuiscint / Eolas', 3, [chunk], 'exact')], requirements,
                'One printed question at its published 3-mark tariff. Listed answers come from the 2026 SEC scheme. ' + language,
                audioMaterial=dict(audio, label=ref))
    listening = [c for c in cards]
    assert len(listening) == 20 and sum(c['totalMarks'] for c in listening) == 60

    # ---- Cuid II: An Cheapadóireacht (2 × 50) ----------------------------------------------
    s10 = stext[9].split(' ', 1)[1]
    marking = s10[s10.index('Freagair do rogha dhá cheann'):]
    symbols = stext[10].split(' ', 1)[1]
    table40 = stext[11].split(' ', 1)[1]
    table_short = stext[12].split(' ', 1)[1]
    smm = stext[34].split(' ', 1)[1]
    assert 'Tasc = 2 mharc' in marking and 'Ábhar = 8 marc' in marking and 'Cumas Gaeilge = 40 marc' in marking
    assert all(x in table_short for x in ['M F1 F2 F3', '38 34 29 19 10']) and '34-40' in smm
    head = ('Treoracha: Ní mór do na hiarrthóirí cúram a dhéanamh de chruinneas na teanga. Caillfear marcanna má bhítear faillitheach ann. '
            'Ní mór ceangal cinnte leanúnach a bheith ann idir an teideal a roghnaítear agus an t‐ábhar a scríobhtar.\n\n'
            'Freagair do rogha dhá cheann de A, B, C, D anseo.')
    groups = {
        'A': ('Giota Leanúnach/Blag', 'Scríobh giota leanúnach nó blag (leathleathanach nó mar sin) ar cheann amháin de na hábhair seo.', 'irish-2-6', ['irish-2-2'], [
            ('i', 'Duine tábhachtach i mo shaol.'), ('ii', 'An caitheamh aimsire is fearr liom.'), ('iii', 'Saoire iontach.')]),
        'B': ('Scéal', 'Ceap scéal (leathleathanach nó mar sin) a mbeadh ceann amháin de na sleachta seo a leanas oiriúnach mar thús leis.', 'irish-2-3', None, [
            ('i', 'D’fhéach mé ar théacs ar m’fhón. Tháinig fearg orm nuair a léigh mé é …'),
            ('ii', 'D’fhreagair mé an fón. Léim mo chroí le háthas nuair a dúirt an bainisteoir liom go raibh an post faighte agam …')]),
        'C': ('Litir/Ríomhphost', None, 'irish-2-8', None, [
            ('i', 'Bhog tú féin agus do mhuintir go teach nua i gceantar eile le déanaí.\nScríobh an litir/an ríomhphost (leathleathanach nó mar sin) a chuirfeá chuig cara leat ag insint dó/di faoin teach nua agus faoi na háiseanna atá sa cheantar nua.'),
            ('ii', 'Tá tú i do bhall de chlub spóirt agus d’eagraigh sibh seó faisin le déanaí chun airgead a bhailiú don chlub. Scríobh an litir/an ríomhphost (leathleathanach nó mar sin) a chuirfeá chuig cara leat ag insint dó/di faoin seó faisin sin agus faoi na rudaí a rinne an club leis an airgead a bhailigh sibh.')]),
        'D': ('Comhrá', None, 'irish-2-9', None, [
            ('i', 'Ba mhaith leat cead a bheith agat d’fhón póca a úsáid ar scoil. Ní aontaíonn do chara leat.\nScríobh an comhrá (leathleathanach nó mar sin) a bheadh agat le do chara faoin ábhar sin.'),
            ('ii', 'Thaitin sraith ar Netflix leatsa ach níor thaitin an tsraith sin le do chara.\nScríobh an comhrá (leathleathanach nó mar sin) a bheadh agat le do chara faoin ábhar sin.')]),
    }
    singles = {}
    for group, (form, instruction, topic, extra_topics, titles) in groups.items():
        for roman, title in titles:
            for line in ([instruction] if instruction else []) + title.splitlines():
                assert comparable(line) in comparable(texts[6]), (group, roman, line[:40])
            body = head + f'\n\n{group} · {form} (50 marc)\n' + (instruction + '\n' if instruction else '') + f'({roman}) {title}'
            singles.setdefault(group, []).append(add(
                f'W-{group}-{roman}', f'composition-{group.lower()}-{roman}', f'Ceapadóireacht {group}({roman})', body + f'\n\nAn rogha don chárta seo: {group}({roman}).',
                topic, [7], [10, 11, 12, 13], [
                    criterion('tasc', 'An Tasc', 2, [marking.split('An tÁbhar (8 marc)')[0]], permitted=[0, 2]),
                    criterion('abhar', 'An tÁbhar', 8, [marking.split('An tÁbhar (8 marc)', 1)[1].split('An Cumas Gaeilge (40 marc)')[0]], 'indicative'),
                    criterion('gaeilge', 'An Cumas Gaeilge', 40, [marking.split('An Cumas Gaeilge (40 marc)', 1)[1], symbols, table40, table_short,
                                                                    'Scéim Mharcála Mhodhnaithe (scheme PDF 34–35): eligible candidates are assessed on named grammar features (bands 34–40 … 0–3); spelling is not counted.'])],
                ['Lean an fhoirm scríbhneoireachta a iarrtar sa cheist.', 'Coinnigh ceangal cinnte leanúnach idir an teideal agus an t-ábhar.', 'Leathleathanach nó mar sin.'],
                'Whole 50-mark composition: Tasc 2, Ábhar 8, Cumas Gaeilge 40. Short attempts use the published M/F1/F2/F3 columns (36/30/20/10) on scheme PDF 13. '
                'The letter or email (C) and the conversation partner (D) are flexible forms inside one response, not separate routes.', extra_topics))

    def combine(members):
        key = '-'.join(m['atlasQuestionId'].removeprefix('W-') for m in members)
        criteria = []
        for m in members:
            prefix = m['atlasQuestionId'].lower().removeprefix('w-') + '-'
            for old in m['criteria']:
                cc = copy.deepcopy(old)
                cc['id'] = prefix + cc['id']
                cc['label'] = m['questionRef'].removeprefix('2026 OL Paper 1 ') + ' · ' + cc['label']
                criteria.append(cc)
        topics = list(dict.fromkeys(t for m in members for t in [m['topicId'], *m.get('additionalTopicIds', [])]))
        ref = ' + '.join(m['questionRef'].removeprefix('2026 OL Paper 1 ') for m in members)
        return add(f'W-{key}', 'composition-' + key.lower(), ref,
                   'Freagair do rogha dhá cheann de A, B, C, D anseo.\n\nAn rogha don chárta seo: ' + ref + '\n\n' +
                   '\n\n'.join(m['questionRef'].removeprefix('2026 OL Paper 1 ') + '\n' + m['questionText'].split('\n\n')[2] for m in members),
                   topics[0], [7], [10, 11, 12, 13], criteria, [r for m in members for r in m['taskRequirements']],
                   'One permitted printed selection: two whole 50-mark compositions from two different sections. Each keeps its own Tasc, Ábhar and Cumas Gaeilge awards; alternative routes are not added together.',
                   topics[1:], memberCardIds=[m['id'] for m in members])

    for g1, g2 in itertools.combinations('ABCD', 2):
        for m1, m2 in itertools.product(singles[g1], singles[g2]):
            combine([m1, m2])

    decisions = selection_decisions(paper)
    pairs = [c for c in cards if 'memberCardIds' in c]
    assert len(pairs) == 30 and {c['totalMarks'] for c in pairs} == {100}
    assert len(cards) == 59 and len({c['id'] for c in cards}) == 59
    for card in cards:
        for cr in card['criteria']:
            assert cr['guidance'] and all(not re.search('[-]', g) for g in cr['guidance']), (card['id'], cr['id'])
    sr = json.loads(SOURCE_REVIEW.read_text())
    review = dict(year=2026, level='ordinary', paperFileid=FILE + '.pdf', schemeFileid=SCHEME_FILE + '.pdf',
                  paperSha256=hashlib.sha256(paper_path.read_bytes()).hexdigest(), schemeSha256=hashlib.sha256(scheme_path.read_bytes()).hexdigest(),
                  reviewedPaperPages=list(range(1, 17)), reviewedSchemePages=sr['reviewedSchemePages'], schemeScope=sr['schemeScope'],
                  reviewDate=REVIEWED_AT, status='reviewed', fullPaperAndApplicableSchemeVisualSweep=True, selectionDecisions=decisions,
                  listeningQuestionCardIds=[c['id'] for c in listening],
                  compositionRouteCardIds=[c['id'] for c in cards if c['atlasQuestionId'].startswith('W-') and 'memberCardIds' not in c],
                  pairedRouteCardIds=[c['id'] for c in pairs],
                  examStructure=dict(listening=60, composition=100, total=160),
                  nonPoolDecisions=sr['nonPoolDecisions'], openIssues=[], audio=sr['audio'], caveats=sr['sourceFindings'],
                  boundaries='20 listening questions at 3 marks (60); 9 composition title routes at 50; 30 full two-section selections at 100.')
    return dict(review=review, cards=cards)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    data = build()
    content = json.dumps(data, ensure_ascii=False, indent=2) + '\n'
    if args.check:
        assert OUT.exists() and OUT.read_text() == content, f'Stale output: {OUT}'
    else:
        OUT.write_text(content)
    print(f"Irish Ordinary 2026 Paper 1: {len(data['cards'])} reviewed task/route cards; the archive remains incomplete.")


if __name__ == '__main__':
    main()
