#!/usr/bin/env python3
"""Reviewed 2026 Higher Paper 1 (Cluastuiscint agus Ceapadóireacht).

Paper PDF 1–20 and the Paper 1 scheme pages (PDF 1–16, 49–52 of the combined
LC001ALP100IV scheme) visually reviewed on 2026-10-11. Scheme PDF 17–48 belong
to Paper 2 and are outside this component. Counts are assertions, not
corpus-completeness proof. Each printed listening question is one card at its
published 2 or 2 + 2 mark tariff (the reader groups a recording section's cards
into one exercise); the nine printed composition titles are whole 100-mark routes.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
FILE = 'LC001ALP100IV'
SCHEME_FILE = 'LC001ALP100IV'
OUT = ROOT / 'components/MarkBank/cards/irish/higher-2026-p1-authored.json'
SOURCE_REVIEW = ROOT / 'scripts/markbank/authored/irish-higher-2026-p1-source-review.json'
REVIEWED_AT = '2026-10-11'
DIRECTIVE = re.compile(r'rogha|roghna|Freagair|Cuir tic|Ainmnigh|Luaigh|\bchoose\b|\beither\b|\bany\b|one of|\bnó\b|dhá phointe|trí phointe|dhá rud|dó/di|Cuir ciorcal|dhá thagairt|dhá ch|dhá dh|an dá|ceann amháin|amháin', re.I)
AUDIO_URL = 'https://www.examinations.ie/archive/exampapers/2026/LC001ZLP017IV.mp3'


def clean(text):
    return re.sub(r'\s+', ' ', text).strip()


def comparable(text):
    return re.sub(r'[^\w]+', '', text.lower())


def criterion(id, label, marks, guidance, kind='quality'):
    return dict(id=id, label=label, kind='award', maxMarks=marks, permittedMarks=list(range(marks + 1)),
                guidanceKind=kind, guidance=guidance)


def selection_decisions(paper):
    decisions = json.loads(SOURCE_REVIEW.read_text())['selectionDecisions']
    expected = {(d['page'], d['raw']) for d in decisions}
    found = {(i, clean(line)) for i, page in enumerate(paper, 1)
             for line in page.get_text().splitlines() if DIRECTIVE.search(clean(line))}
    assert found == expected, ('Unclassified/stale selection directives', found - expected, expected - found)
    return decisions


def chunks(text, starts, stop=None):
    """Split scheme text at each printed question start; every start must occur once, in order."""
    out, rest = [], text
    for i, start in enumerate(starts):
        assert rest.count(start) >= 1, start
        rest = rest[rest.index(start):]
        end = starts[i + 1] if i + 1 < len(starts) else stop
        part = rest[:rest.index(end)] if end else rest
        out.append(re.sub(r'\s*(\d\.|\(b\))\s*$', '', clean(part)))
        rest = rest[len(part):] if end else ''
    return out


def build():
    import fitz
    paper_path = ROOT / f'paper-trail-corpus/exampapers/2026/{FILE}.pdf'
    scheme_path = ROOT / f'paper-trail-corpus/markingschemes/2026/{SCHEME_FILE}.pdf'
    assert hashlib.sha256(paper_path.read_bytes()).hexdigest() == 'd98a6d047a8fa5e9382e99acfa0f8f8ae7de1cd227b6da976c9f17cb47075378', 'Paper changed: repeat visual review'
    assert hashlib.sha256(scheme_path.read_bytes()).hexdigest() == 'd7e9de038bf91ee9cf9735854e1d9272100982744ef7c1ebcc0f17ca025e2239', 'Scheme changed: repeat visual review'
    paper = fitz.open(paper_path)
    scheme = fitz.open(scheme_path)
    texts = [clean(p.get_text()) for p in paper]
    stext = [clean(p.get_text()) for p in scheme]
    cards = []

    def add(key, slug, ref, prompt, topic, pages, scheme_pages, criteria, requirements, note, extra_topics=None, **extra):
        card = dict(id=f'irish-2026-hl-p1-{slug}', year=2026, level='higher', paper=1, section='1',
                    atlasQuestionId=key, questionRef=f'2026 HL Paper 1 {ref}', questionText=prompt,
                    totalMarks=sum(c['maxMarks'] for c in criteria), topicId=topic,
                    **({'additionalTopicIds': extra_topics} if extra_topics else {}),
                    conceptId=f'irish-hl-p1-{slug}', paperFileid=FILE, schemeFileid=SCHEME_FILE,
                    schemePage=scheme_pages[0], schemePages=scheme_pages, reviewedAt=REVIEWED_AT,
                    reviewedPaperPages=pages, taskRequirements=requirements, criteria=criteria, markingGuideNote=note,
                    sourceMaterial=dict(kind='source-text', label=ref, title=f'Gaeilge Ardleibhéal 2026 · Páipéar 1 · {ref}',
                                        pages=pages, attribution='© State Examinations Commission.',
                                        presentationNote='Original examination pages from the official question paper.'),
                    **extra)
        cards.append(card)
        return card

    # ---- Cuid I: An Chluastuiscint (60) -------------------------------------------------
    general = stext[5].split('Nótaí:', 1)[1].split('Siombailí Anótála', 1)[0].strip()
    assert general.startswith('Níor chóir a mheas') and general.endswith('neamhbhailí.')
    general = 'Nótaí (scheme PDF 6): ' + general
    language = ('Scheme PDF 3 and 10: “Bainfear ó 0 go 3 ar chaighdeán na Gaeilge.” This 0–3 deduction applies once to the whole '
                'listening section (Tuiscint 60 − Cumas Gaeilge 0–3), never inside a single card.')
    a7 = stext[6].split('FÓGRA A hAON (10 marc)', 1)[1]
    f1 = chunks(a7.split('FÓGRA A DÓ (8 marc)', 1)[0], ['Cén t-ainm atá ar an trucail', 'Cad iad na huaireanta', 'Scríobh síos dhá cháilíocht', 'Cén tuarastal'])
    f2 = chunks(a7.split('FÓGRA A DÓ (8 marc)', 1)[1], ['Cathain a chuirfear tús', 'Scríobh síos dhá rud a chaithfidh', 'Cé mhéad mac léinn'])
    b8 = stext[7].split('COMHRÁ A hAON (14 mharc)', 1)[1]
    c1m1 = chunks(b8.split('An Dara Mír', 1)[0], ['Cathain a d’imir Pól', 'Scríobh síos dhá phointe eolais faoin gcalaois', 'Luaigh cúis amháin'])
    c1m2 = chunks(b8.split('An Dara Mír', 1)[1], ['Scríobh síos an dá phointe eolais faoin tsaoire', 'Cad a cheannaigh Pól'])
    b9 = stext[8].split('COMHRÁ A DÓ (14 mharc)', 1)[1]
    c2m1 = chunks(b9.split('An Dara Mír', 1)[0], ['Cén baile ina raibh', 'Scríobh síos dhá chúis nár éirigh', 'Cén rud ba mhó a chuaigh'])
    c2m2 = chunks(b9.split('An Dara Mír', 1)[1], ['Cén ráfla', 'Cén churiarracht', 'Cé mhéad ceoltóir'])
    c10 = stext[9].split('PÍOSA A hAON (8 marc)', 1)[1]
    p1 = chunks(c10.split('PÍOSA A DÓ (6 mharc)', 1)[0], ['Cé mhéad bliain atá an sobaldráma', 'Scríobh síos an dá rud a mheallann', 'Cén tseirbhís dhigiteach'])
    p2 = chunks(c10.split('PÍOSA A DÓ (6 mharc)', 1)[1], ['Cén dáta ar a raibh Oíche', 'Scríobh síos dhá dheis'], stop='Bainfear ó 0 go 3')
    intro = {
        'A': 'Cuid A\nCloisfidh tú dhá fhógra sa chuid seo. Cloisfidh tú gach fógra díobh faoi dhó. Beidh sos ann leis na freagraí a scríobh tar éis na chéad éisteachta agus tar éis an dara héisteacht.',
        'B': 'Cuid B\nCloisfidh tú dhá chomhrá sa chuid seo. Cloisfidh tú gach comhrá díobh faoi dhó. Cloisfidh tú an comhrá ó thosach deireadh an chéad uair. Ansin cloisfidh tú ina dhá mhír é. Beidh sos ann leis na freagraí a scríobh tar éis gach míre díobh.',
        'C': 'Cuid C\nCloisfidh tú dhá phíosa nuachta sa chuid seo. Cloisfidh tú gach píosa díobh faoi dhó. Beidh sos ann leis na freagraí a scríobh tar éis na chéad éisteachta agus tar éis an dara héisteacht.'}
    # (key, slug, heading, page, topic, [(number, paper prompt, marks, scheme chunk)])
    segments = [
        ('L-A-F1', 'listening-a-f1', 'Cuid A · Fógra a hAon', 'FÓGRA A hAON', 3, 'irish-1-0', 'A', [
            ('1a', '1. (a) Cén t‐ainm atá ar an trucail chaife atá luaite san fhógra seo?', 2, f1[0]),
            ('1b', '(b) Cad iad na huaireanta oibre a bheidh ag an oibrí barista?', 2, f1[1]),
            ('2', '2. Scríobh síos dhá cháilíocht atá riachtanach don phost mar oibrí barista.', 4, f1[2]),
            ('3', '3. Cén tuarastal a gheobhaidh an t‐oibrí barista?', 2, f1[3])]),
        ('L-A-F2', 'listening-a-f2', 'Cuid A · Fógra a Dó', 'FÓGRA A DÓ', 3, 'irish-1-0', 'A', [
            ('1', '1. Cathain a chuirfear tús le scéim cónaithe Gaeilge do mhic léinn na chéad bhliana i gColáiste na Tríonóide?', 2, f2[0]),
            ('2', '2. Scríobh síos dhá rud a chaithfidh an mac léinn a bheith sásta a dhéanamh de réir choinníollacha na scéime.', 4, f2[1]),
            ('3', '3. Cé mhéad mac léinn a roghnófar don scéim cónaithe tar éis na n‐agallamh?', 2, f2[2])]),
        ('L-B-C1-M1', 'listening-b-c1-first', 'Cuid B · Comhrá a hAon · An Chéad Mhír', 'COMHRÁ A hAON\nAn Chéad Mhír', 4, 'irish-1-1', 'B', [
            ('1', '1. Cathain a d’imir Pól i gcluiche ceannais peile an chontae?', 2, c1m1[0]),
            ('2', '2. Scríobh síos dhá phointe eolais faoin gcalaois a rinneadh ar Phól agus an liathróid ina sheilbh aige.', 4, c1m1[1]),
            ('3', '3. Luaigh cúis amháin a raibh díomá an domhain ar Phól.', 2, c1m1[2])]),
        ('L-B-C1-M2', 'listening-b-c1-second', 'Cuid B · Comhrá a hAon · An Dara Mír', 'COMHRÁ A hAON\nAn Dara Mír', 4, 'irish-1-1', 'B', [
            ('1', '1. Scríobh síos an dá phointe eolais faoin tsaoire a bhí beartaithe ag Pól agus ag a chairde.', 4, c1m2[0]),
            ('2', '2. Cad a cheannaigh Pól nuair a chuir sé an tsaoire in áirithe?', 2, c1m2[1])]),
        ('L-B-C2-M1', 'listening-b-c2-first', 'Cuid B · Comhrá a Dó · An Chéad Mhír', 'COMHRÁ A DÓ\nAn Chéad Mhír', 5, 'irish-1-1', 'B', [
            ('1', '1. Cén baile ina raibh Fleadh Cheoil na hÉireann ar siúl?', 2, c2m1[0]),
            ('2', '2. Scríobh síos dhá chúis nár éirigh le Sinéad duais a bhuachan i gcraobhchomórtas an bhosca ceoil faoi ocht mbliana déag.', 4, c2m1[1]),
            ('3', '3. Cén rud ba mhó a chuaigh i bhfeidhm ar Shinéad ag an bhFleadh?', 2, c2m1[2])]),
        ('L-B-C2-M2', 'listening-b-c2-second', 'Cuid B · Comhrá a Dó · An Dara Mír', 'COMHRÁ A DÓ\nAn Dara Mír', 5, 'irish-1-1', 'B', [
            ('1', '1. Cén ráfla a chuala Sinéad faoin réalta cheoil Ed Sheeran?', 2, c2m2[0]),
            ('2', '2. Cén churiarracht dhomhanda Guinness a sáraíodh ag an bhFleadh?', 2, c2m2[1]),
            ('3', '3. Cé mhéad ceoltóir a bhí ag seinm le chéile nuair a sáraíodh an churiarracht dhomhanda sin?', 2, c2m2[2])]),
        ('L-C-P1', 'listening-c-p1', 'Cuid C · Píosa a hAon', 'PÍOSA A hAON', 6, 'irish-1-2', 'C', [
            ('1', '1. Cé mhéad bliain atá an sobaldráma Ros na Rún á chraoladh ar TG4?', 2, p1[0]),
            ('2', '2. Scríobh síos an dá rud a mheallann an lucht féachana dílis chuig an sobaldráma Ros na Rún.', 4, p1[1]),
            ('3', '3. Cén tseirbhís dhigiteach nua atá curtha ar fáil ar Sheinnteoir TG4 le déanaí?', 2, p1[2])]),
        ('L-C-P2', 'listening-c-p2', 'Cuid C · Píosa a Dó', 'PÍOSA A DÓ', 6, 'irish-1-2', 'C', [
            ('1', '1. Cén dáta ar a raibh Oíche na hÓige ar siúl den chéad uair anuraidh?', 2, p2[0]),
            ('2', '2. Scríobh síos dhá dheis a thugann rannpháirtíocht i gclubanna agus i seirbhísí óige do dhaoine óga.', 4, p2[1])]),
    ]
    variants = {('L-B-C2-M1', '2'): 'Paper wording “duais a bhuachan”; the scheme prints “bonn a bhuachan”. The accepted answers are unchanged.',
                ('L-C-P2', '2'): 'Paper wording “seirbhísí óige”; the scheme prints “seirbhísí óga”. The accepted answers are unchanged.'}
    totals = {'L-A-F1': 10, 'L-A-F2': 8, 'L-B-C1-M1': 8, 'L-B-C1-M2': 6, 'L-B-C2-M1': 8, 'L-B-C2-M2': 6, 'L-C-P1': 8, 'L-C-P2': 6}
    audio = dict(kind='source-audio', title='Triail Chluastuisceana 2026', playbackUrl=AUDIO_URL, secFileid='LC001ZLP017IV.mp3',
                 canonicalUrl=AUDIO_URL, attribution='© State Examinations Commission.',
                 presentationNote='Official Higher and Ordinary Level recording (one recording for the whole listening test). Play the part named on the card.')
    for key, slug, ref, heading, page, topic, part, questions in segments:
        assert sum(q[2] for q in questions) == totals[key]
        for n, prompt, marks, chunk in questions:
            assert comparable(prompt) in comparable(texts[page - 1]), (key, n, prompt)
            assert (f'{marks // 2} mharc + {marks // 2} mharc' if marks == 4 else f'{marks} mharc') in chunk, (key, n, chunk[:80])
        requirements = ['Éist leis an taifeadadh oifigiúil.', 'Freagair i nGaeilge, ach amháin nuair nach gá sin.']
        note = ('Listed answers and tariffs come from the 2026 SEC scheme; equivalent wording with the same meaning is accepted. ' + language)
        scheme_page = 7 if part == 'A' else 8 if key.startswith('L-B-C1') else 9 if part == 'B' else 10
        for n, prompt, marks, chunk in questions:
            guidance = [chunk, general] + ([variants[(key, n)]] if (key, n) in variants else [])
            # A lettered part keeps its printed question number so the reader shows “1(b)”.
            printed = prompt if re.match(r'\d\.', prompt) else f'{n[0]}. {prompt}'
            add(f'{key}-{n}', f'{slug}-q{n}', f'{ref} · Ceist {n[0]}' + (f'({n[1]})' if len(n) > 1 else ''),
                intro[part] + '\n\n' + heading + '\n' + printed, topic, [page], [scheme_page],
                [criterion('eolas', 'Tuiscint / Eolas', marks, guidance, 'exact')], requirements,
                f'One printed question at its published {marks}-mark tariff' + (' (two points at 2 + 2)' if marks == 4 else '') + '. ' + note,
                audioMaterial=dict(audio, label=ref))

    # ---- Cuid II: An Cheapadóireacht (100) ----------------------------------------------
    p9, p11, p12, p13, p14 = stext[10], stext[12], stext[13], stext[14], stext[15]
    marking = p9.split('An Mharcáil:', 1)[1].split('Cuid II', 1)[0].strip()
    stil = p11.split('Stíl chuí scríbhneoireachta (5 mharc)', 1)[1].split('Ionramháil Ábhair (15 mharc)', 1)[0].strip()
    abhar = p11.split('Ionramháil Ábhair (15 mharc)', 1)[1].strip()
    gaeilge = [p12[p12.index('Cumas Gaeilge (80 marc)'):].strip(), p13.split(' ', 1)[1].strip()]
    graded = p14.split(' ', 1)[1].strip()
    assert all(x in abhar for x in ['13, 14, 15', '11, 12', '9, 10', '6, 7, 8', '3, 4, 5', '0, 1, 2'])
    assert all(x in gaeilge[1] for x in ['76-80', '64-67', '52-55', '40-43', '28-31', '16-19', '0-7'])
    assert all(x in graded for x in ['S1', 'S2', 'S3', 'S4', '(68)', '(56)', '(44)', '(54)'])
    head = ('Freagair do rogha CEANN AMHÁIN de A, B nó C anseo thíos.\n'
            'Treoracha: Ní gá níos mó ná 500‐600 focal nó mar sin a scríobh i gcás ar bith.\n'
            'Ní mór do na hiarrthóirí cúram a dhéanamh de chruinneas na teanga. Caillfear marcanna má bhítear faillitheach ann.\n'
            'Ní mór ceangal cinnte leanúnach a bheith ann idir an teideal a roghnaítear agus an t‐ábhar a scríobhtar.')
    groups = {
        'A': ('AISTE nó ALT NUACHTÁIN/IRISE', 'Scríobh AISTE nó ALT NUACHTÁIN/IRISE ar cheann amháin de na hábhair seo.', 'irish-2-0', ['irish-2-1'], [
            ('a', 'An Ghaeilge agus an cultúr Gaelach – ag dul ó neart go neart?'),
            ('b', 'Na rudaí is mó a chuireann isteach ar dhaoine sa lá atá inniu ann.'),
            ('c', 'Scéalta nuachta idirnáisiúnta an lae inniu.'),
            ('d', 'An ghéarchéim aeráide – cúis imní do dhaoine ar fud an domhain?'),
            ('e', 'Sábháilteacht ar líne.')]),
        'B': ('SCÉAL', 'Ceap SCÉAL a mbeadh do rogha ceann amháin díobh seo oiriúnach mar theideal air.', 'irish-2-3', None, [
            ('a', 'Meas.'), ('b', 'Bíonn siúlach scéalach.')]),
        'C': ('DÍOSPÓIREACHT/ÓRÁID', 'Freagair do rogha ceann amháin díobh seo.', None, None, [
            ('a', 'Scríobh an chaint a dhéanfá i ndíospóireacht scoile ar son an rúin seo a leanas nó ina aghaidh:\nCaitear go cothrom le gach duine in Éirinn sa lá atá inniu ann.'),
            ('b', 'Iarradh ort píosa cainte a dhéanamh ar chlár raidió ar an ábhar seo a leanas:\nAn tábhacht a bhaineann le caithimh aimsire do dhaoine óga.\nScríobh an píosa cainte a dhéanfá ar an ábhar sin.')]),
    }
    reasons = {
        'A': 'AISTE nó ALT NUACHTÁIN/IRISE is a choice of writing form inside one response, marked by the same Stíl/Ábhar/Gaeilge scheme; it is not a separate route.',
        'B': 'Each printed title is a separate route; the story itself is open.',
        'C': '“ar son … nó ina aghaidh” is the speaker’s stance inside one speech (consistent with the English corpus “for or against” tasks); both stances are marked identically.'}
    for group, (form, instruction, topic, extra_topics, titles) in groups.items():
        for letter, title in titles:
            assert all(comparable(line) in comparable(texts[6]) for line in [instruction, *title.splitlines()]), (group, letter)
            card_topic = topic or ('irish-2-4' if letter == 'a' else 'irish-2-5')
            s4 = (['S4 applies to this title: “Easnamhach i gcás A (a), A (b) agus A (c)” — Stíl (5) Ábhar (10) Gaeilge (54).']
                  if group == 'A' and letter in 'abc' else [])
            add(f'W-{group}-{letter}', f'composition-{group.lower()}-{letter}', f'Ceapadóireacht {group}({letter})',
                head + f'\n\n{group} · {form} (100 marc)\n{instruction}\n\n({letter}) {title}\n\nAn rogha don chárta seo: {group}({letter}).',
                card_topic, [7], [11, 13, 14, 15, 16], [
                    criterion('stil', 'Stíl chuí scríbhneoireachta', 5, [stil, graded]),
                    criterion('abhar', 'Ionramháil Ábhair', 15, [abhar, marking]),
                    criterion('gaeilge', 'Cumas Gaeilge', 80, gaeilge + [
                        'Scéim Mharcála Mhodhnaithe (scheme PDF 49): for eligible candidates spelling and the listed grammar features are not counted in the 80-mark Cumas Gaeilge award.'] + s4)],
                ['Lean an fhoirm scríbhneoireachta a iarrtar sa cheist.', 'Coinnigh ceangal cinnte leanúnach idir an teideal agus an t-ábhar.',
                 'Timpeall 500–600 focal.'],
                'Whole 100-mark composition: Stíl 5, Ionramháil Ábhair 15, Cumas Gaeilge 80, assessed as one unit. Deficient-length attempts use the printed S1–S4 grades. '
                + reasons[group], extra_topics)

    decisions = selection_decisions(paper)
    listening = [c for c in cards if c['atlasQuestionId'].startswith('L-')]
    assert len(listening) == 23 and sum(c['totalMarks'] for c in listening) == 60
    for key, total in totals.items():
        assert sum(c['totalMarks'] for c in listening if c['atlasQuestionId'].startswith(key + '-')) == total, key
    assert len(cards) == 32 and len({c['id'] for c in cards}) == 32
    for card in cards:
        for c in card['criteria']:
            assert all(not re.search('[-]', g) for g in c['guidance']), (card['id'], c['id'])
    sr = json.loads(SOURCE_REVIEW.read_text())
    review = dict(year=2026, level='higher', paperFileid=FILE + '.pdf', schemeFileid=SCHEME_FILE + '.pdf',
                  paperSha256=hashlib.sha256(paper_path.read_bytes()).hexdigest(),
                  schemeSha256=hashlib.sha256(scheme_path.read_bytes()).hexdigest(),
                  reviewedPaperPages=list(range(1, 21)), reviewedSchemePages=sr['reviewedSchemePages'],
                  schemeScope=sr['schemeScope'], reviewDate=REVIEWED_AT, status='reviewed',
                  fullPaperAndApplicableSchemeVisualSweep=True, selectionDecisions=decisions,
                  listeningQuestionCardIds=[c['id'] for c in listening],
                  compositionRouteCardIds=[c['id'] for c in cards if c['atlasQuestionId'].startswith('W-')],
                  examStructure=dict(listening=60, composition=100, total=160),
                  nonPoolDecisions=sr['nonPoolDecisions'], openIssues=[], audio=sr['audio'], caveats=sr['sourceFindings'],
                  boundaries='23 listening questions at their printed 2 or 2 + 2 tariffs (60), grouped in the reader by recording section; 9 composition title routes at 100 each (choose one).')
    return dict(review=review, cards=cards), scheme


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    data, scheme = build()
    scheme_md = '# Gaeilge Ardleibhéal 2026 — SEC marking scheme (Páipéar 1 agus 2)\n\n' + '\n\n'.join(
        f'## PDF page {i + 1}\n\n' + p.get_text() for i, p in enumerate(scheme))
    outputs = {OUT: json.dumps(data, ensure_ascii=False, indent=2) + '\n',
               ROOT / 'examiner-reports/irish/schemes/2026-hl.md': '\n'.join(line.rstrip() for line in scheme_md.splitlines()).rstrip() + '\n'}
    for path, value in outputs.items():
        if args.check:
            assert path.exists() and path.read_text() == value, f'Stale output: {path}'
        else:
            path.write_text(value)
    print(f"Irish Higher 2026 Paper 1: {len(data['cards'])} reviewed task/route cards; the archive remains incomplete.")


if __name__ == '__main__':
    main()
