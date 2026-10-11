#!/usr/bin/env python3
"""Reviewed 2010 Foundation written paper. Counts are assertions, not corpus-completeness proof.

2010 written pages 1–16, aural pages 1–8 and scheme pages 1–17 visually reviewed
(sweep 2026-10-08, re-checked against the rendered pages 2026-10-11).
Source hashes and classified raw selection directives guard the reviewed sources.
The separate listening paper (LC001BLPA00IV) is a recorded source gap: the official
Foundation recording is unavailable, so it has no cards, transcript or substitute audio.
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
FILE = 'LC001BLP100IV'
AURAL_FILE = 'LC001BLPA00IV'
SCHEME_FILE = 'LC001BLP000IV'
OUT = ROOT / 'components/MarkBank/cards/irish/foundation-2010-authored.json'
SOURCE_REVIEW = ROOT / 'scripts/markbank/authored/irish-foundation-2010-source-review.json'
DIRECTIVE = re.compile(r'rogha|roghna|Freagair|Cuir tic|Ainmnigh|Luaigh|\bchoose\b|\beither\b|\bany\b|one of|\bnó\b|dhá phointe|trí phointe|dhá rud|dheartháir|dheirfiúr|dó / d[ií]|dó/di|Cuir ciorcal|dhá thagairt', re.I)


def clean(text):
    return re.sub(r'\s+', ' ', text).strip()


def comparable(text):
    return re.sub(r'[^\w]+', '', text.lower())


def criterion(id, label, marks, guidance, exact=False):
    return dict(id=id, label=label, kind='award', maxMarks=marks,
                permittedMarks=[0, marks] if exact else list(range(marks + 1)),
                guidanceKind='exact-answer' if exact else 'quality', guidance=guidance)


def scheme_text(page):
    # Visually verified Symbol-font bullet, arrow and division sign; original PDF unchanged.
    return page.get_text().translate({0xf0b7: '•', 0xf0ae: '→', 0xf0b8: '÷'})


def selection_decisions(papers):
    decisions = json.loads(SOURCE_REVIEW.read_text())['selectionDecisions']
    expected = {(d['paperFileid'], d['page'], d['raw']) for d in decisions}
    found = {(name, i, clean(line)) for name, paper in papers.items() for i, page in enumerate(paper, 1)
             for line in page.get_text().splitlines() if DIRECTIVE.search(clean(line))}
    assert found == expected, ('Unclassified/stale selection directives', found - expected, expected - found)
    return decisions


def build():
    import fitz
    paper_path = ROOT / f'paper-trail-corpus/exampapers/2010/{FILE}.pdf'
    aural_path = ROOT / f'paper-trail-corpus/exampapers/2010/{AURAL_FILE}.pdf'
    scheme_path = ROOT / f'paper-trail-corpus/markingschemes/2010/{SCHEME_FILE}.pdf'
    for path, sha in [(paper_path, '7553abaa485b8b68ac585887e55e58522ad9597392fe85940289e167293fea1b'),
                      (aural_path, 'e6e21527a147acb955fd6485c970724127f7fc60976b15b0288f3c26693938d3'),
                      (scheme_path, 'a29bb58dc74195783c6e67b36ea6eea22b027aa838907c014a2d26a18f410be0')]:
        assert hashlib.sha256(path.read_bytes()).hexdigest() == sha, f'Changed source {path.name}: repeat visual review'
    paper = fitz.open(paper_path)
    aural = fitz.open(aural_path)
    scheme = fitz.open(scheme_path)
    texts = [clean(p.get_text()) for p in paper]
    cards = []

    def add(key, section, ref, prompt, topic, exam_topics, pages, scheme_pages, criteria,
            requirements=None, note=None, **extra):
        card = dict(id=f'irish-2010-fl-{key.lower()}', year=2010, level='foundation', paper=1, section=section,
                    atlasQuestionId=key, questionRef=f'2010 FL {ref}', questionText=prompt,
                    totalMarks=sum(c['maxMarks'] for c in criteria), topicId=topic, examTopicKeys=exam_topics,
                    conceptId=f'irish-foundation-{key.lower()}', paperFileid=FILE, schemeFileid=SCHEME_FILE,
                    schemePage=scheme_pages[0], schemePages=scheme_pages, taskRequirements=requirements or [],
                    criteria=criteria,
                    markingGuideNote=note or 'Use the answer and tariff published by the SEC for this part.',
                    sourceMaterial=dict(kind='source-text', label=ref, title=f'Gaeilge Bonnleibhéal 2010 · {ref}',
                                        pages=pages, attribution='© State Examinations Commission.',
                                        presentationNote='Original examination pages, including every required picture or passage.'),
                    **extra)
        cards.append(card)
        return card

    # Ceist 1: ten signs, matching key EHDGAFBJCI (paper PDF 2, scheme PDF 3).
    signs = [
        'Siopa Poitigéara\nAr oscailt 9.00 – 6.00', 'Timpeallán Romhat !\nGéill Slí',
        'Stáisiún Traenach\nDúnta\nSeirbhís Bus in úsáid', 'Bialann an Chaisleáin\n“Bia Blasta den Scoth”\nMeán Lae go Meán Oíche',
        'Ar Cíos\nTeach Saoire Cois Trá\nFón 026 645127', 'Ciúnas\nLe do thoil\nScrúdú ar siúl anseo',
        'Éist\nLe FM 102\n“Raidió na Life”', 'Stáisiún Bád Tarrthála\nCheann Heilbhic\n“Bí cúramach ar an uisce”',
        'Comharchumann Mhúscraí\nGlasraí Úra\nDíreach ón bhFeirm', 'Ospidéal na hOllscoile\nIonad Éigeandála\nCosc ar Pháirceáil anseo']
    key = 'EHDGAFBJCI'
    assert ' '.join(key) in clean(scheme[2].get_text())
    for i, (sign, answer) in enumerate(zip(signs, key), 1):
        assert all(comparable(line) in comparable(texts[1]) for line in sign.splitlines()), sign
        add(f'R-1-{i}', '2', f'Léamhthuiscint · Ceist 1({i})',
            'Meaitseáil na pictiúir leis na fógraí/comharthaí agus scríobh síos an litir cheart sa bhosca in aice leis an uimhir cheart atá sa ghreille.\n\n' + f'{i}. {sign}',
            'irish-9-1', ['match'], [2], [3], [criterion('answer', 'Litir cheart', 4, [answer], True)])

    # Each row: verbatim question, printed alternatives (or none), official answer.
    reading = {
        '2A': (3, 'letterReading', [
            ('Cén dáta ar scríobh Nóirín an litir seo?', '5 Aibreán | 3 Bealtaine | 20 Iúil', '3 Bealtaine'),
            ('Cén grád a fuair Seán sa Mhata san Ardteistiméireacht?', 'Grád A | Grád B | Grád C', 'Grád C'),
            ('Cá fhad a leanann an traenáil do phrintísigh?', '3 Bliana | 4 Bliana | 5 Bliana', '5 Bliana'),
            ('Cad atá ag BSL i mBaile Átha Cliath?', 'Club Leadóige | Ionad Spóirt | Club Sacair', 'Ionad Spóirt'),
            ('Cén post atá ag Nóirín Ní Chasaide?', 'Leictreoir | Printíseach | Oifigeach Pearsanra', 'Oifigeach Pearsanra')]),
        '2B': (4, 'brochure', [
            ('Cén t-ainm atá ar an bhFéile i gCeatharlach?', 'Fleá Cheoil | Féile TG4 | Féile na hÉigse', 'Féile Na hÉigse'),
            ('Cad a bheidh ar siúl do dhéagóirí le linn na Féile?', 'Ranganna ealaíne | Ranganna céilí | Ranganna ceoil', 'Ranganna céilí'),
            ('Cén saghas ceardlainne a bheidh ann do dhaoine fásta?', 'Ceardlann Drámaíochta | Ceardlann Scannánaíochta | Ceardlann Scríbhneoireachta', 'Ceardlann Scríbhneoireachta'),
            ('Cad as don ghrúpa “Buí Bolg”?', 'Loch Garman | Ceatharlach | An Gael-Choláiste', 'Loch Garman'),
            ('Cathain a bheidh an tóraíocht taisce ar siúl?', 'Tráthnóna Dé Sathairn | Oíche Shathairn | Tráthnóna Dé Domhnaigh', 'Tráthnóna Dé Domhnaigh')]),
        '2C': (5, 'news', [
            ('Cén mhí ar tharla an timpiste?', 'Márta | Bealtaine | Meitheamh', 'Márta'),
            ('Cárbh as do na fir óga sa charr?', 'Cill Chainnigh | Mainistir Laoise | Port Laoise', 'Cill Chainnigh'),
            ('Cé a chuir fios ar an otharcharr?', 'Na fir óga | Na Gardaí | Tiománaí bus', 'Tiománaí bus'),
            ('Cé mhéad duine a maraíodh ar láthair na timpiste?', 'Duine | Beirt | Triúr', 'Beirt'),
            ('Cad ba chúis leis an timpiste seo?', 'An aimsir | An t-ól | Luas an chairr', 'An aimsir')]),
        '3A': (6, 'news', [
            ('Cén uirlis cheoil a sheinneann Sharon Shannon?', 'Drumaí | Bosca ceoil | Giotár', 'Bosca ceoil'),
            ('Cén áit ar rugadh Sharon Shannon?', 'Co. an Chláir | Co. na Gaillimhe | Na Stáit Aontaithe', 'Co. an Chláir'),
            ('Cén saghas ceoil a sheinneann Sharon?', None, 'Ceol traidisiúnta'),
            ('Cé a rinne clár speisialta faoi Sharon i 1992?', 'Adam Clayton | Gay Byrne | Bill Clinton', 'Gay Byrne'),
            ('Cé mhéad albam atá déanta ag Sharon?', '1 | 6 | 10', '10')]),
        '3B': (7, 'extract', [
            ('Cén bhliain a rugadh Gráinne Mhaol?', '1530 | 1593 | 1603', '1530'),
            ('Cén fáth ar ghearr Gráinne an ghruaig fhada rua a bhí uirthi?', None, 'Chun dul ar bord loinge lena hathair'),
            ('Cén aois a bhí Gráinne nuair a phós sí?', 'Ceithre bliana déag | Sé bliana déag | Dhá bhliain is fiche', 'Sé bliana déag'),
            ('Cén áit a raibh Gráinne ina cónaí?', 'Co. Mhaigh Eo | Co. Shligigh | Co. na Gaillimhe', 'Co. Mhaigh Eo'),
            ('Cé a bhuail le Gráinne in Greenwich?', 'A hathair | An Bhanríon Eilís | George Bingham', 'An Bhanríon Eilís')]),
        '3C': (8, 'poem', [
            ('Cad a bhí ag Seán Ó Riain?', 'Canna | Éanadán | Rang', 'Éanadán'),
            ('Cén t-ainm a bhí ar an “ngasúr deas”?', 'Tadhg Ó Laoghaire | Seán Mac Fheorais | Seán Ó Riain', 'Tadhg Ó Laoghaire'),
            ('Cad a dhéanann gach canaerí?', 'Canann sé | Crochann sé | Ritheann sé', 'Canann sé.'),
            ('Cad a d’ith an t-éan go craosach?', None, 'Síol'),
            ('Cén dath a bhí ar an éan sa deireadh?', 'Buí | Donn | Dubh', 'Donn')])}
    # Scheme PDF 5 special notes: accepted forms 6, published reduction 6−2=4, else 0.
    special = {
        ('3A', 3): ('Ceist 3 (a) Mír 3', 'Ceist 3 (b) Mír 2',
                    'Accepted forms 6. Ceol draíochta 6−2 = 4; Bosca ceoil and Ceol 0. Enter the final mark for this part only.'),
        ('3B', 2): ('Ceist 3 (b) Mír 2', 'Ceist 3 (c) Mír 4',
                    'Accepted forms 6; an answer with excess information 6−2 = 4. Enter the final mark for this part only.'),
        ('3C', 4): ('Ceist 3 (c) Mír 4', None,
                    'Accepted forms 6; two lines of the poem 6−2 = 4; the whole stanza 6−6 = 0. Enter the final mark for this part only.')}
    notes = clean(scheme_text(scheme[4]))
    reading_cards = {}
    for slot, (page, exam_topic, rows) in reading.items():
        reading_cards[slot] = []
        for i, (prompt, options, answer) in enumerate(rows, 1):
            assert comparable(prompt) in comparable(texts[page - 1]), (slot, i, prompt)
            for option in (options or '').split(' | '):
                assert comparable(option) in comparable(texts[page - 1]), (slot, i, option)
            assert comparable(answer) in comparable(scheme[2 if slot[0] == '2' else 3].get_text()), (slot, i, answer)
            rule = special.get((slot, i))
            card = add(f'R-{slot}-{i}', '2', f'Léamhthuiscint · Ceist {slot[0]}({slot[1].lower()})({i})',
                       f'Léigh an téacs ar leathanach {page}.\n\n{i}. {prompt}' + ('\n\n' + options.replace(' | ', '\n') if options else ''),
                       'irish-9-2', [exam_topic], [page], [3] if slot[0] == '2' else [4, 5] if rule else [4],
                       [criterion('answer', 'Freagra', 5 if slot[0] == '2' else 6, [answer], True)])
            if rule:
                start, end, explanation = rule
                part = notes.split(start, 1)[1]
                if end:
                    part = part.split(end, 1)[0]
                card['criteria'][0]['permittedMarks'] = [0, 4, 6]
                card['criteria'][0]['guidance'] += [clean(part), explanation]
            reading_cards[slot].append(card)
    assert sum(c['totalMarks'] for c in cards) == 40 + 3 * 25 + 3 * 30

    def combine(key, ref, members, quote):
        criteria = []
        for member in members:
            for old in member['criteria']:
                c = copy.deepcopy(old)
                c['id'] = member['atlasQuestionId'].lower() + '-' + c['id']
                c['label'] = member['questionRef'].replace('2010 FL ', '') + ' · ' + c['label']
                criteria.append(c)
        topics = list(dict.fromkeys(t for c in members for t in [c['topicId'], *c.get('additionalTopicIds', [])]))
        return add(key, members[0]['section'], ref,
                   quote + '\n\nAn rogha don chárta seo: ' + ref + '\n\n' +
                   '\n\n'.join(c['questionRef'].replace('2010 FL ', '') + '\n' + c['questionText'] for c in members),
                   topics[0], list(dict.fromkeys(t for c in members for t in c['examTopicKeys'])),
                   sorted(set(p for c in members for p in c['sourceMaterial']['pages'])),
                   sorted(set(p for c in members for p in c['schemePages'])), criteria,
                   [r for c in members for r in c['taskRequirements']],
                   'This is one permitted printed selection. Each selected response retains its own SEC marking criteria; alternative routes are not added to this tariff.',
                   additionalTopicIds=topics[1:], memberCardIds=[c['id'] for c in members])

    for n in '23':
        for a, b in itertools.combinations('ABC', 2):
            combine(f'R-{n}-{a}{b}', f'Léamhthuiscint · Ceist {n}({a.lower()}) + ({b.lower()})',
                    reading_cards[n + a] + reading_cards[n + b],
                    f'Ceist {n} Freagair do rogha dhá cheann de (a), (b), (c) anseo thíos.')

    def guide(p):
        text = clean(scheme_text(scheme[p - 1]))
        assert text.startswith(f'Gaeilge ATBL 2010 {p} '), (p, text[:40])
        return text.removeprefix(f'Gaeilge ATBL 2010 {p} ')

    def between(text, start, end=None):
        assert start in text and (end is None or end in text.split(start, 1)[1]), (start, end)
        part = text.split(start, 1)[1]
        return clean(part.split(end, 1)[0] if end else part)

    def language(marks):
        return criterion('gaeilge', 'Cruinneas Gaeilge', marks, [
            'Dul na Gaeilge: struchtúir na Gaeilge agus cruinneas gramadaí. Foclóir: cruinneas sa stór focal. Litriú: moltar gan an iomarca béime a chur ar an ngné seo ag an leibhéal seo. Ná glac le Béarla.',
            f'Bronn marc as {marks} ar chaighdeán na Gaeilge san iarracht iomlán.',
            'Reasonable-accommodation guidance is on scheme PDF 17. No four-point language-conversion table is printed in 2010.'])

    n8, n9 = guide(8), guide(9)
    general = 'Na Treoracha: ' + between(n8, 'Na Treoracha:', 'Pictiúr 1')
    photo = ('Picture numbering: the paper prints panels 1, 2, an unnumbered photograph and 3. The scheme counts four pictures, '
             'so scheme Pictiúr 3 is the photograph and scheme Pictiúr 4 is the panel printed 3.')
    notice = add('W-4A', '3', 'Scríobh · Ceist 4(a) · Fógra',
                 'Féach ar na pictiúir thíos.\n\nScríobh amach an FÓGRA a bhaineann leis an rud atá i gceist thuas.\n\n'
                 'Cén rud a bheidh ar siúl? Cén áit a dtosóidh sé?\nCén lá? Dáta? Am? Táille iontrála?\nCé a chuirfidh tús leis an turas?\nCá rachaidh an t-airgead?',
                 'irish-9-3', ['notice'], [10], [7, 8, 9], [
                     criterion('leagan', 'Leagan Amach', 1, ['Leagan amach: ' + between(n8, 'Leagan amach:', 'Na Treoracha:')]),
                     criterion('pictiur1', 'Pictiúr 1 · rud 3 + áit 3', 6, [general, between(n8, 'Pictiúr 1', 'Pictiúr 2')]),
                     criterion('pictiur2', 'Pictiúr 2 · lá 3 + dáta 2 + am 2 + táille 2', 9, [general, between(n8, 'Pictiúr 2'), between('^' + n9, '^', 'Pictiúr 3')]),
                     criterion('pictiur3', 'Pictiúr 3 (grianghraf) · tús an turais', 3, [general, between(n9, 'Pictiúr 3', 'Pictiúr 4'), photo,
                         'Scheme PDF 9 asks “Cé a chuirfidh tús leis an rás?” where the paper asks about an turas; both original wordings are kept.']),
                     criterion('pictiur4', 'Pictiúr 4 (painéal 3) · an t-airgead', 3, [general, between(n9, 'Pictiúr 4', 'Léiriú na marcanna'), photo]),
                     language(8)],
                 ['Scríobh fógra faoin turas rothaíochta bunaithe ar gach pictiúr agus ar na treoracha.'],
                 'Whole 30-mark notice: layout 1, pictures 6+9+3+3, shared language 8. Apply the general −1 for an inappropriate tense to the affected point. '
                 'Scheme pictures 3 and 4 are the unnumbered photograph and the panel printed 3. Retain the exact 2010 activity, starting-place, day, date, time, fee and Club Óige Inis rules; later 40-mark notice tariffs do not apply.')
    r10, r11 = guide(10), guide(11)
    reply = add('W-4B', '3', 'Scríobh · Ceist 4(b) · Freagra',
                'Féach ar na pictiúir thíos.\n\n'
                'Pictiúr 2:\nA Helen,\nFuair mé dhá thicéad don cheolchoirm i bPáirc an Chrócaigh i mí Lúnasa. An dtiocfaidh tú liom? Iarr cead ó do Mham. Beidh an-chraic againn.\nPhil\n\n'
                'Is tusa an duine atá sna pictiúir seo. Scríobh FREAGRA chuig Phil agus abair:\n\n'
                '- Cén lá a fuair tú an cuireadh. — Pictiúr 1\n- Gur iarr tú cead ar do Mham dul ann. — Pictiúr 1\n'
                '- Go mbeidh tú ábalta dul ann. — Pictiúr 3\n- Conas a rachaidh sibh go Páirc an Chrócaigh. — Pictiúr 3\n'
                '- Cad a dhéanfaidh sibh ag an gceolchoirm. — Pictiúr 4\n- Cén t-am a thiocfaidh sibh abhaile. — Pictiúr 4',
                'irish-9-3', ['notice', 'pictures'], [11], [10, 11], [
                    criterion('beannu', 'Beannú', 2, [between(r10, 'Cruinneas Gaeilge = 8 marc', 'Iarracht ar fhreagra:')]),
                    criterion('freagra', 'Iarracht ar fhreagra', 1, ['Iarracht ar fhreagra: ' + between(r10, 'Iarracht ar fhreagra:', 'Síniú :')]),
                    criterion('siniu', 'Síniú', 1, ['Síniú: ' + between(r10, 'Síniú :', 'Na Treoracha Pictiúr 1')]),
                    criterion('pictiur1', 'Pictiúr 1 · lá agus cead', 6, [between(r10, 'Na Treoracha Pictiúr 1'), between('^' + r11, '^', 'Pictiúr 3')]),
                    criterion('pictiur3', 'Pictiúr 3 · dul ann agus modh taistil', 6, [between(r11, 'Pictiúr 3', 'Pictiúr 4')]),
                    criterion('pictiur4', 'Pictiúr 4 · ceolchoirm agus filleadh', 6, [between(r11, 'Pictiúr 4', 'Léiriú na Marcanna')]),
                    language(8)],
                ['Scríobh freagra chuig Phil agus freagair gach ceann de na sé threoir.'],
                'Whole 30-mark reply: greeting 2, reply attempt 1, signature 1, six required details at 3 each (pictures 1, 3, 4), shared language 8. '
                'The six details are required headings, not alternatives. The handwritten invitation in picture 2 is transcribed from the paper; the original page remains the authority. '
                'The scheme prints −1 for past tense on the picture 3 and 4 points.')
    assert all(w in texts[10] for w in ['Phil', 'Páirc an Chrócaigh', 'Cén t-am a thiocfaidh sibh abhaile'])
    l12, l13, l14 = guide(12), guide(13), guide(14)
    letter = add('W-5A', '3', 'Scríobh · Ceist 5(a) · Litir',
                 'Féach ar na pictiúir thíos.\n\nTá tusa ag obair san Ollstór Crua-Earraí seo an samhradh seo. Scríobh litir abhaile chuig do chara ag insint dó/di:\n\n'
                 '- Faoin Ollstór agus faoin áit a bhfuil an tOllstór suite — Pictiúr 1\n'
                 '- Faoin obair a dhéanann tú san Ollstór (trí phointe ag teastáil) — Pictiúr 2\n'
                 '- Faoi na custaiméirí a dhéanann siopadóireacht san Ollstór — Pictiúr 3\n'
                 '- Faoi na rudaí a dhéanann tú nuair a bhíonn am saor agat — Pictiúr 4\n\n'
                 'N.B. Bíodh an leagan amach cuí ar do litir, i.e. seoladh, dáta, tús agus críoch oiriúnach.',
                 'irish-9-3', ['letterWriting'], [12], [12, 13, 14], [
                     criterion('seoladh', 'Seoladh', 2, [between(l12, 'Seoladh: 2 mharc', 'Dáta: 1 marc')]),
                     criterion('data', 'Dáta', 1, [between(l12, 'Dáta: 1 marc', 'Tús: 1 marc')]),
                     criterion('tus', 'Tús', 1, [between(l12, 'Tús: 1 marc', 'Críoch: 2 marc')]),
                     criterion('crioch', 'Críoch', 2, [between(l12, 'Críoch: 2 marc', 'Na Treoracha: 24 marc')]),
                     criterion('pictiur1', 'Pictiúr 1 · ollstór 2 + áit 2', 4, [between(l12, 'Na Treoracha: 24 marc')]),
                     criterion('pictiur2', 'Pictiúr 2 · trí phointe × 4', 12, [between(l13, 'Pictiúr 2', 'Pictiúr 3'),
                         'Source wording note: the scheme heading says “san óstán”, but the paper, the examples and the rest of the scheme concern the hardware store. The original wording is kept; assess the printed Ollstór task.']),
                     criterion('pictiur3', 'Pictiúr 3 · custaiméirí', 4, [between(l13, 'Pictiúr 3 =', 'Pictiúr 4')]),
                     criterion('pictiur4', 'Pictiúr 4 · dhá thagairt × 2', 4, [between(l13, 'Pictiúr 4')]),
                     language(10)],
                 ['Scríobh chuig cara faoin ollstór agus an áit, trí phointe faoin obair, tagairt faoi na custaiméirí, agus dhá thagairt do na himeachtaí sa phictiúr deireanach.',
                  'Seoladh, dáta, tús agus críoch oiriúnach.'],
                 'Whole 40-mark letter: layout 6 (2+1+1+2), pictures 4+12+4+4, shared language 10. Picture 3 needs one customer reference; picture 4 needs two references to depicted activities, with −1 for an activity absent from the picture. '
                 'The activity examples are illustrative, not a closed menu. No length penalty is printed.',
                 sourceDiscrepancyNotice='Nóta foinse: deir ceannteideal amháin sa scéim “san óstán”, ach baineann an páipéar agus na samplaí leis an ollstór crua-earraí.',
                 additionalTopicIds=['irish-2-8'])
    assert 'trí phointe ag teastáil' in texts[11] and 'dó/di' in texts[11]
    form_prompt = (
        'Ba mhaith leat a bheith ag obair mar gharraíodóir i gclub gailf. Fuair tú an Fhoirm Iarratais seo le líonadh. Líon isteach an Fhoirm Iarratais atá anseo thíos.\n[ Nóta: Is tusa Áine Bhreathnach ]\n\n'
        'K-Club Chill Dara\nFoirm Iarratais do phost mar Gharraíodóir\nAinm: Áine Bhreathnach\nUimhir theileafóin:\nSeoladh:\nAois:\nDáta Breithe:\n'
        'Cén post atá agat faoi láthair?\nCén Scrúdú Teistiméireachta atá déanta agat?\nAinmnigh cúig ábhar scoile a rinne tú sa scrúdú sin:\nLuaigh trí spórt a d’imir tú ar scoil:\n'
        'An bhfuil gairdín agat sa bhaile?\nAn féidir leat tarracóir a thiomáint?\nAn mbeidh tú sásta tosú ag obair gach maidin ar a seacht a chlog?\nAr imir tú Galf riamh?\n'
        'Cuir tic (✓) leis an dáta is fearr leat le haghaidh agallaimh: 21 Iúil / 28 Iúil / 4 Lúnasa.\n\n'
        'Scríobh alt beag (timpeall 40 focal) ag insint dúinn cén fáth ar mhaith leat a bheith ag obair ar Chúrsa Gailf.\n\nSíniú: Áine Bhreathnach\nDáta:')
    for line in form_prompt.replace('(✓)', '').replace(' / ', ' ').splitlines():
        assert comparable(line) in comparable(texts[12]), line
    dates = [('21-iuil', '21 Iúil'), ('28-iuil', '28 Iúil'), ('4-lunasa', '4 Lúnasa')]
    f14 = between(l14, 'Ceist 5(b) Foirm Iarratais')
    f15 = between('^' + guide(15), '^', 'Ceist 6(a) Cuntas')
    fields = [
        'Use the printed doubled column: phone 1; address 3; age 1; birth date 2; current job 2; certificate exam 2; five subjects 10; three sports 3; garden 1; tractor 1; early start 1; previous golf 1; interview date 1; bottom date 1. Total 30, divide once by 2 and round up once: 21÷2=10½→11.',
        between('^' + f14, '^', 'An tAlt Beag'),
        'Published table conflict: the undoubled birth-date row prints ½, while the doubled row prints 2. The undoubled values sum 14½ despite the printed total 15. This rubric follows the explicit doubled 30÷2 method and its 15-mark total; both original columns remain visible.']
    forms = []
    for slug, label in dates:
        forms.append(add('W-5B-' + slug, '3', 'Scríobh · Ceist 5(b) · ' + label,
                         form_prompt + '\n\nAn rogha don chárta seo: ' + label + '.',
                         'irish-9-0', ['form'], [13], [14, 15], [
                             criterion('fields', 'Na Ceisteanna · iomlán slán', 15, fields),
                             criterion('paragraph', 'An t-Alt · marc tar éis coigeartú faid', 15, [
                                 between(f14, 'An tAlt Beag', 'Cruinneas Gaeilge'), f15,
                                 'Assess the relevant paragraph /15, off-topic /5. Reduce only its awarded mark proportionally if short: 20 of 40 words → 50% reduction (PDF 14); about 32 of 40 words → one-fifth reduction (PDF 15). No fixed reference count or later-year 8-mark ceiling is printed.']),
                             language(10)],
                         ['Líon gach réimse; cúig ábhar scoile agus trí spórt.', 'Roghnaigh ' + label + ' don agallamh.',
                          'Scríobh timpeall 40 focal faoi obair ar Chúrsa Gailf.'],
                         'Whole 40-mark form: fields 15 using the doubled column 30÷2 rounded up once, paragraph 15 after its own length adjustment, shared language 10. The three printed interview dates are expanded; school subjects and sports are open content. '
                         'The printed undoubled birth-date ½ conflicts with the doubled 2 and the total 15; compare both columns.',
                         sourceDiscrepancyNotice='Nóta foinse: tá ½ marc do dháta breithe sa chéad cholún agus 2 sa cholún dúbailte. Úsáidtear an modh foilsithe 30÷2 agus iomlán 15; féach ar an dá cholún.'))
    captions = [('faoin tuath', 'marcach óg'), ('ag tafann', 'geit'), ('chabhraigh', 'stop'), ('ar ais ar an gcapall', 'áthas')]
    assert all(w in texts[14] for pair in captions for w in pair)
    g15, g16 = guide(15), guide(16)
    stories = []
    for slot, page, scheme_pages in [('6A', 14, [15, 16]), ('6B', 15, [16])]:
        if slot == '6A':
            prompt = ('Féach ar an bpictiúr thíos.\n\nChaith tú “Lá ar an Trá leis an gClub Óige” an mhí seo caite.\nTá tú chun cuntas (timpeall 90 focal) a scríobh in Iris na Scoile faoi.\n\n'
                      'Scríobh an cuntas sin (timpeall 90 focal) sa spás atá faoin bpictiúr.\n\nLá ar an Trá leis an gClub Óige')
            details = [between(g15, 'Ceist 6(a) Cuntas'), between('^' + g16, '^', 'Ceist 6(b) Eachtra')]
        else:
            prompt = ('Féach ar na pictiúir anseo thíos.\n\nTharla an eachtra seo agus tú amuigh ag rothaíocht le do chara. Tá tú chun scríobh faoin eachtra seo in Iris na Scoile (timpeall 90 focal).\n\n'
                      'Scríobh faoin eachtra (timpeall 90 focal) sa spás atá faoi na pictiúir.\n\n'
                      + '\n'.join(f'{i}. {a} / {b}' for i, (a, b) in enumerate(captions, 1)) + '\n\nEACHTRA A THARLA')
            details = [between(g16, 'Ceist 6(b) Eachtra')]
        for line in prompt.splitlines():
            if line and not re.match(r'\d\. ', line):
                assert comparable(line) in comparable(texts[page - 1]), line
        stories.append(add('W-' + slot, '3', f'Scríobh · Ceist 6({slot[-1].lower()})', prompt, 'irish-9-4', ['pictures', 'story'],
                           [page], scheme_pages, [
                               criterion('cumarsaid', 'Cumas Cumarsáide · marc tar éis coigeartú faid', 37, details + [
                                   'Assess communication /37 against the five required references. Apply the proportional short-length reduction to this awarded communication mark only; language /13 remains separate. The 2010 scheme prints no fixed 5-mark deduction per missing reference.']),
                               language(13)],
                           ['Scríobh timpeall 90 focal in Iris na Scoile.', 'Tabhair cúig thagairt ar a laghad; i 6(b), ceann do gach pictiúr agus pointe amháin eile.'],
                           'Whole 50-mark story: communication 37 after proportional length adjustment plus language 13. Example references are illustrative and are not a closed choose-five pool. No later-year fixed penalty or worked length table is imported.'))
    # Required Q4, Q5, Q6: 2 × (one letter + three form dates) × 2 = 16 full 120-mark selections.
    for first, second, third in itertools.product([notice, reply], [letter, *forms], stories):
        combine(first['atlasQuestionId'] + '-' + second['atlasQuestionId'].removeprefix('W-') + '-' + third['atlasQuestionId'].removeprefix('W-'),
                ' + '.join(c['questionRef'].replace('2010 FL ', '') for c in [first, second, third]), [first, second, third],
                'FREAGAIR GACH CEIST (4, 5 AGUS 6). Ceist 4: Freagair (a) NÓ (b). Ceist 5: Freagair (a) NÓ (b). Ceist 6: Freagair (a) NÓ (b).')

    decisions = selection_decisions({FILE + '.pdf': paper, AURAL_FILE + '.pdf': aural})
    assert len(cards) == 70 and len({c['id'] for c in cards}) == 70
    for card in cards:
        for c in card['criteria']:
            assert all('ATBL' not in g and not re.search('[-]', g) for g in c['guidance']), (card['id'], c['id'])
    products = [c for c in cards if re.match(r'W-4[AB]-5', c['atlasQuestionId'])]
    assert len(products) == 16 and {c['totalMarks'] for c in products} == {120}
    sr = json.loads(SOURCE_REVIEW.read_text())
    assert sr['componentStatus'][AURAL_FILE + '.pdf'].startswith('source-gap')
    review = dict(year=2010, level='foundation', paperFileid=FILE + '.pdf', schemeFileid=SCHEME_FILE + '.pdf',
                  paperSha256=hashlib.sha256(paper_path.read_bytes()).hexdigest(),
                  schemeSha256=hashlib.sha256(scheme_path.read_bytes()).hexdigest(),
                  reviewedPaperPages=list(range(1, 17)), reviewedSchemePages=list(range(1, 18)),
                  reviewDate=sr['reviewDate'], status='reviewed', fullPaperAndApplicableSchemeVisualSweep=True,
                  selectionDecisions=[d for d in decisions if d['paperFileid'] == FILE + '.pdf'],
                  atomicPracticeCardIds=[c['id'] for c in cards if 'memberCardIds' not in c],
                  pairedRouteCardIds=[c['id'] for c in cards if 'memberCardIds' in c],
                  examStructure=dict(matching=40, readingQ2=50, readingQ3=60, writingQ4=30, writingQ5=40, writingQ6=50, writing=120, total=270),
                  nonPoolDecisions=sr['nonPoolDecisions'], openIssues=[], caveats=sr['sourceFindings'],
                  boundaries='10 matching + 30 reading + 8 whole writing routes; 6 reading pairs and 16 full writing products.',
                  separateListeningComponent=dict(paperFileid=AURAL_FILE + '.pdf', status=sr['componentStatus'][AURAL_FILE + '.pdf'],
                                                  decision=sr['audio']['decision']))
    return dict(review=review, cards=cards), scheme


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    result, scheme = build()
    scheme_md = '# Gaeilge Bonnleibhéal 2010 — SEC marking scheme\n\n' + '\n\n'.join(
        f'## PDF page {i + 1}\n\n' + scheme_text(p) for i, p in enumerate(scheme))
    outputs = {OUT: json.dumps(result, ensure_ascii=False, indent=2) + '\n',
               ROOT / 'examiner-reports/irish/schemes/2010-fl.md': '\n'.join(line.rstrip() for line in scheme_md.splitlines()).rstrip() + '\n'}
    for path, content in outputs.items():
        if args.check:
            assert path.exists() and path.read_text() == content, f'Stale Foundation output: {path}'
        else:
            path.write_text(content)
    print('Irish Foundation 2010: 70 written task/selection cards. The separate listening paper remains a source gap (official recording unavailable); the archive is incomplete.')


if __name__ == '__main__':
    main()
