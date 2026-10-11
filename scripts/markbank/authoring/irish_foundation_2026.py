#!/usr/bin/env python3
"""Reviewed 2026 Foundation tasks. Counts are assertions, not corpus-completeness proof.

2026 paper pages 1–20 and scheme pages 1–20 visually reviewed on 2026-10-11.
Source hashes, classified raw selection directives and task identities travel with
the output. 2026 publishes unequal per-part listening and reading tariffs; every
card keeps its own printed tariff.
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
SCHEME_FILE = 'LC001BLP100IV'
OUT = ROOT / 'components/MarkBank/cards/irish/foundation-2026-authored.json'
SOURCE_REVIEW = ROOT / 'scripts/markbank/authored/irish-foundation-2026-source-review.json'
DIRECTIVE = re.compile(r'rogha|roghna|Freagair|Cuir tic|Ainmnigh|Luaigh|\bchoose\b|\beither\b|\bany\b|one of|\bnó\b|dhá phointe|trí phointe|dhá rud|dheartháir|dheirfiúr|dó / d[ií]|dó/di|Cuir ciorcal|dhá thagairt', re.I)


def clean(text):
    return re.sub(r'\s+', ' ', text).strip()


def comparable(text):
    return re.sub(r'[^\w]+', '', text.lower())


def in_order(prompt, text):
    # Words in printed order; PDF extraction interleaves wrapped prompts with options.
    return re.search('.*?'.join(re.escape(comparable(w)) for w in prompt.split() if comparable(w)), comparable(text))


def criterion(id, label, marks, guidance, exact=False, deduct_from=None):
    return dict(id=id, label=label, kind='deduction' if deduct_from else 'award',
                maxMarks=marks, permittedMarks=[0, marks] if exact else list(range(marks + 1)),
                guidanceKind='exact-answer' if exact else 'quality', guidance=guidance,
                **({'deductFrom': deduct_from} if deduct_from else {}))


def selection_decisions(paper):
    decisions = json.loads(SOURCE_REVIEW.read_text())['selectionDecisions']
    expected = {(d['page'], d['raw']) for d in decisions}
    found = {(i, clean(line)) for i, page in enumerate(paper, 1)
             for line in page.get_text().splitlines() if DIRECTIVE.search(clean(line))}
    assert found == expected, ('Unclassified/stale selection directives', found - expected, expected - found)
    return decisions


def build():
    import fitz
    paper_path = ROOT / f'paper-trail-corpus/exampapers/2026/{FILE}.pdf'
    scheme_path = ROOT / f'paper-trail-corpus/markingschemes/2026/{SCHEME_FILE}.pdf'
    assert hashlib.sha256(paper_path.read_bytes()).hexdigest() == 'f2a1105cfe9c5db4a43bd095177aa862ba941bc667aaf5dffe35281da7c472b4', 'Paper changed: repeat visual review'
    assert hashlib.sha256(scheme_path.read_bytes()).hexdigest() == '4e00fb7f805905d2b08af1a88d79514c73e44696748341a49d3293ff45315368', 'Scheme changed: repeat visual review'
    paper = fitz.open(paper_path)
    scheme = fitz.open(scheme_path)
    texts = [clean(p.get_text()) for p in paper]
    cards = []

    def add(key, section, ref, prompt, topic, exam_topics, pages, scheme_pages, criteria,
            requirements=None, note=None, **extra):
        card = dict(id=f'irish-2026-fl-{key.lower()}', year=2026, level='foundation', paper=1, section=section,
                    atlasQuestionId=key, questionRef=f'2026 FL {ref}', questionText=prompt,
                    totalMarks=sum(c['maxMarks'] for c in criteria if c['kind'] == 'award'),
                    topicId=topic, examTopicKeys=exam_topics, conceptId=f'irish-foundation-{key.lower()}',
                    paperFileid=FILE, schemeFileid=SCHEME_FILE, schemePage=scheme_pages[0], schemePages=scheme_pages,
                    taskRequirements=requirements or [], criteria=criteria,
                    markingGuideNote=note or 'Use the answer and tariff published by the SEC for this part.',
                    sourceMaterial=dict(kind='source-text', label=ref, title=f'Gaeilge Bonnleibhéal 2026 · {ref}', pages=pages,
                                        attribution='© State Examinations Commission.',
                                        presentationNote='Original examination pages, including every required picture or passage.'),
                    **extra)
        cards.append(card)
        return card

    # Multiple-choice distractors are possible answers to ONE task, not alternative
    # tasks; expanding them would teach knowingly wrong responses as valid routes.
    # 2026 prints unequal per-part listening tariffs (scheme PDF 2).
    aural = [
        ('1a', 3, 10, 'Cén spórt is fearr le Síle?', None, 'Rugbaí = an chéad phictiúr'),
        ('1b', 3, 4, 'Cá ndeachaigh Síle i mí Lúnasa seo caite?', 'Go hÉirinn | Go dtí an tSeapáin | Go Sasana', 'Sasana'),
        ('2a', 3, 10, 'Cén sórt seó a luaitear anseo?', None, 'Seó damhsa = an ceathrú pictiúr'),
        ('2b', 3, 4, 'Cén mhí a thaistil na damhsóirí go Meiriceá?', 'I mí Eanáir | I mí an Mhárta | I mí na Nollag', 'I mí Eanáir'),
        ('3', 4, 8, 'Cá bhfuil an bhean ag dul?', None, 'Oifig turasóireachta = an tríú pictiúr'),
        ('4', 4, 8, 'Cá bhfuil an leabharlann? (Cuir tic (✓) sa bhosca ceart.)', None, 'An ceathrú bosca ag an mbarr (tic nó saighead sa bhosca)'),
        ('5a', 4, 8, 'Conas atá an aimsir maidin inniu?', None, 'Go hálainn = an chéad phictiúr'),
        ('5b', 4, 8, 'Cén teocht a bheidh ann anocht?', '6 chéim Celsius | 10 gcéim Celsius | 19 gcéim Celsius', '6 chéim Celsius'),
        ('6a', 5, 15, 'Cén t-am a dhúisigh Róisín?', 'Ar a sé a chlog | Ar a seacht a chlog | Ar a hocht a chlog', 'Ar a seacht a chlog'),
        ('6b', 5, 5, 'Cé mhéad a chosain ticéad amháin?', '€90 | €245 | €490', '€490'),
        ('7a', 5, 10, 'Cén lá a bhí an cluiche ag an scoil?', 'Dé Luain | Déardaoin | Dé hAoine', 'Dé hAoine'),
        ('7b', 5, 10, 'Cé mhéad bréag san iomlán a d’inis Seán?', 'Dhá bhréag | Trí bhréag | Ceithre bhréag', 'Trí bhréag'),
        ('8a', 5, 10, 'Cad a bheidh ar siúl Dé Sathairn?', 'Seó faisin | Damhsa an Séú Bliain | Cluiche peile', 'Damhsa an Séú Bliain'),
        ('8b', 5, 10, 'Cá mbeidh siad ag teacht le chéile ar a cúig a chlog?', 'I dteach Órla | San óstán | I gcarrchlós na scoile', 'I gcarrchlós na Scoile'),
    ]
    audio_url = 'https://www.examinations.ie/archive/exampapers/2026/LC001BLP017IV.mp3'
    s2 = clean(scheme[1].get_text())
    for n, page, marks, prompt, options, answer in aural:
        assert in_order(prompt, texts[page - 1]), (n, prompt)
        for option in (options or '').split(' | '):
            assert comparable(option) in comparable(texts[page - 1]), (n, option)
        assert comparable(answer) in comparable(s2) and f'/{marks}' in s2.split(answer, 1)[1][:12], (n, answer, marks)
        ref = 'Cluastuiscint · Ceist ' + re.sub(r'([ab])$', r'(\1)', n)
        add('A-' + n, '1', ref, re.sub(r'^(\d+)([ab]?)$', lambda m: m[1] + '. ' + ('(' + m[2] + ') ' if m[2] else ''), n) + prompt +
            ('\n\n' + options.replace(' | ', '\n') if options else ''),
            'irish-1-3', ['aural'], [page], [2], [criterion('answer', 'Freagra', marks, [answer], True)],
            ['Éist leis an taifeadadh. Úsáid na pictiúir ar an leathanach nuair is gá.'],
            audioMaterial=dict(kind='source-audio', label=ref, title='Gaeilge Bonnleibhéal 2026 · An Chluastuiscint',
                               playbackUrl=audio_url, secFileid='LC001BLP017IV.mp3', canonicalUrl=audio_url,
                               attribution='© State Examinations Commission.',
                               presentationNote='Official Foundation Level recording. Answer the question shown using its printed options.'))
    assert sum(c['totalMarks'] for c in cards) == 120

    signs = [
        'Fainic!\nMadra dainséarach ar dualgas!', 'Imreoirí á Lorg\nSéasúr nua iománaíochta',
        'Pictiúrlann an Bhaile\nCosc ar cheamaraí', 'Carrchlós Dúnta\nCarr trí thine',
        'Ciúnas\nScoláirí ag staidéar', 'Siúlóid Urraithe\nAr mhaithe le Trócaire',
        'Dráma na Nollag\nAr stáitse ag 8.00 p.m.', 'Siopa Bláthanna\nLascaine 10% do Lá Fhéile Vailintín',
        'Bialann an Bhaile\nMilseog saor in aisce le béile an lae', 'Péintéir ar Fáil\nAon áit, aon am!']
    key = 'HGFBIJECDA'
    s3 = clean(scheme[2].get_text())
    assert ' '.join(f'{i} {k}' for i, k in enumerate(key, 1)) in s3
    other = 'Beifear ag súil le litir ach glacfar le córas eile (uimhir an phictiúir in ionad litir an phictiúir) má tá sé soiléir / intuigthe.'
    assert other in s3
    for i, (sign, answer) in enumerate(zip(signs, key), 1):
        assert all(in_order(line, texts[5]) for line in sign.splitlines()), sign
        add(f'R-1-{i}', '2', f'Léamhthuiscint · Ceist 1({i})',
            'Meaitseáil na pictiúir leis na fógraí/comharthaí agus scríobh síos an litir cheart sa bhosca in aice leis an uimhir cheart atá sa ghreille.\n\n' + f'{i}. {sign}',
            'irish-9-1', ['match'], [6], [3], [criterion('answer', 'Litir cheart', 4, [answer, other], True)])

    # Each row: verbatim question, printed alternatives (or none), SEC key, printed tariff.
    reading = {
        '2A': (7, 'letterReading', [
            ('Cathain a thosóidh an taithí oibre?', 'Ar an 10 Eanáir | I mí Feabhra | Roimh dheireadh na míosa', 'I mí Feabhra', 1),
            ('Cén bhaint atá ag Seán le nuachtán na scoile?', 'Is teicneolaí é. | Is eagarthóir é. | Is iriseoir é.', 'Is eagarthóir é', 6),
            ('Cad a sheol Seán chucu lena litir?', 'Ailt a scríobh sé féin | Nuachtán | Litir ón scoil', 'Ailt a scríobh sé féin', 6),
            ('Cad a sheas amach i gcás Sheáin?', 'A spéis i gcúrsaí polaitíochta | A spéis sa spórt | A spéis i gcúrsaí bia', 'A spéis i gcúrsaí polaitíochta', 6),
            ('Cé eile a sheol isteach iarratais?', 'Eagarthóir an nuachtáin | Scoláirí eile | Príomhoidí', 'Scoláirí eile', 6)]),
        '2B': (8, 'brochure', [
            ('Cé mhéad acra de choill ar a bhfuil ionad Center Parcs suite?', 'Cúig acra | Dhá acra is fiche | Ceithre chéad acra', 'Ceithre chéad acra', 6),
            ('Cén fáth a bhfuil an t-ionad an-áisiúil do gach duine ó thaobh taistil de?', 'Tá sé suite i lár na tíre. | Is baile beag é. | Tá coill álainn ann.', 'Tá sé suite i lár na tíre', 6),
            ('Cén rud faoin ionad a chabhraíonn le cúrsaí sábháilteachta?', 'An fiadhúlra | Tá sé saor ó charranna. | An t-ollmhargadh', 'Tá sé saor ó charranna', 6),
            ('Cad air a mbíonn tóir ollmhór?', 'Ar an gcadhcáil | Ar an ziplíneáil | Ar an bpáirc uisce', 'Ar an bpáirc uisce', 6),
            ('An féidir fanacht ann ar feadh oíche amháin?', 'Is féidir | Ní féidir | Is féidir le pas lae.', 'Ní féidir', 1)]),
        '2C': (9, 'extract', [
            ('Cathain a bhog teaghlach Shinéad thar lear?', 'Go ceann bliana | Lá amháin | Mí ó shin', 'Mí ó shin', 6),
            ('Cá háit ar chaith Seán níos mó ama?', 'Ar scoil | Ina sheomra codlata | Thar lear', 'Ina sheomra codlata', 1),
            ('Cad as a dtagann go leor amhrán?', 'Briseadh croí | Giotár | Ionadh', 'Briseadh croí', 6),
            ('Cad a bhí le bheith ar siúl an tseachtain dár gcionn?', 'Comórtas amhránaíochta | Scoil | Cleachtadh', 'Comórtas amhránaíochta', 6),
            ('Cad a bhí ar aghaidh Sheáin ag deireadh an chomórtais?', 'Uaigneas | Neirbhís | Meangadh mór gáire', 'Meangadh mór gáire', 6)]),
        '3A': (10, 'news', [
            ('Cad a d’fhógair Taylor Swift agus Travis Kelce ar an 26 Lúnasa 2025?', 'Gur bhuaigh siad Grammy | Go raibh siad geallta | Gur phós siad', 'Go raibh siad geallta', 7),
            ('Cén tslí bheatha atá ag Taylor Swift?', 'Is réalta cheoil í. | Is imreoir peile í. | Is tuismitheoir í.', 'Is realta cheoil í.', 7),
            ('Cén aois a bhí Taylor nuair a bhog a teaghlach go Nashville?', None, 'Ceithre bliana déag d’aois/14', 7),
            ('Cad eile a dhéanann Travis Kelce chomh maith leis an spórt?', 'Imríonn sé peil. | Podchraoladh rathúil | Bíonn sé ag canadh.', 'Podchraoladh ráthúil', 2),
            ('Cá huair atá Taylor agus Travis le pósadh?', 'Ar an 13 Nollaig 1989 | Ar an 26 Lúnasa 2025 | Ar an 13 Meitheamh 2026', 'Ar an 13 Meitheamh 2026', 7)]),
        '3B': (11, 'extract', [
            ('Cár tháinig na saighdiúirí trasna ar an mbuachaill óg?', 'Sa Pholainn | San Iaráin | San Iodáil', 'San Iaráin', 6),
            ('Cén fáth ar thóg na saighdiúirí an béar óg leo?', None, 'Bhí an-trua acu dó / chun aire a thabhairt dó', 6),
            ('Cá gcodlaíodh Wojtek?', 'I bpuball | I mbosca | Ar an gclár Blue Peter', 'I bpuball', 6),
            ('Cén bhliain a tógadh Wojtek go dtí an zú?', 'Sa bhliain 1942 | Sa bhliain 1944 | Sa bhliain 1947', 'Sa bhliain 1947', 6),
            ('Cén sórt saoil a bhí ag Wojtek sa zú?', 'Compordach | Uaigneach | Bocht', 'Compórdach', 6)]),
        '3C': (12, 'poem', [
            ('Cén rud nach mbactar riamh leis?', '“Taibhse mór” | “Taibhsín bídeach” | “Teach dhá stór”', 'Taibhsín bídeach', 7),
            ('Cé a theithfeadh go beo ón “taibhse millteach”?', None, 'Múinteoirí', 7),
            ('Cén rud nach n-osclódh Mal Magú?', 'Falla | Áit | Doras', 'Doras', 7),
            ('Cad a thógfadh Mal Magú ón Zú?', 'Eilifint | Púca | Feannóg', 'Eilifint', 7),
            ('Cad a dhéanfadh Mal Magú sa spéir istoíche?', 'Ríl | Míle murdar | Codladh', 'Ríl', 2)]),
    }
    spelling = {('3A', 2): 'réalta', ('3A', 4): 'rathúil', ('3B', 5): 'Compordach'}
    reading_cards = {}
    for slot, (page, exam_topic, rows) in reading.items():
        reading_cards[slot] = []
        scheme_page = clean(scheme[3 if slot[0] == '2' else 4].get_text())
        assert sum(r[3] for r in rows) == (25 if slot[0] == '2' else 30), slot
        for i, (prompt, options, answer, marks) in enumerate(rows, 1):
            assert in_order(prompt, texts[page - 1]), (slot, i, prompt)
            for option in (options or '').split(' | '):
                assert comparable(option) in comparable(texts[page - 1]), (slot, i, option)
            for accepted in answer.split(' / '):
                assert comparable(accepted) in comparable(scheme_page), (slot, i, accepted)
            label = f'{slot[0]}{slot[1].lower()}({i})'
            assert re.search(re.escape(label) + r'\s*/' + str(marks) + r'\b', scheme_page), (slot, i, marks)
            guidance = [answer]
            if (slot, i) in spelling:
                guidance.append(f'The scheme prints this key with a spelling variant of the paper option ({spelling[(slot, i)]} on the paper); it is the same answer.')
            card = add(f'R-{slot}-{i}', '2', f'Léamhthuiscint · Ceist {slot[0]}({slot[1].lower()})({i})',
                       f'Léigh an téacs ar leathanach {page}.\n\n{i}. ' + prompt + ('\n\n' + options.replace(' | ', '\n') if options else ''),
                       'irish-9-2', [exam_topic], [page], [4 if slot[0] == '2' else 5],
                       [criterion('answer', 'Freagra', marks, guidance, True)],
                       note=f'Use the answer and the {marks}-mark tariff the SEC printed for {label}. The 2026 scheme weights the five parts of this passage unequally.')
            reading_cards[slot].append(card)

    def combine(key, ref, members, pool_quote, note):
        criteria = []
        for member in members:
            prefix = member['atlasQuestionId'].lower() + '-'
            for old in member['criteria']:
                c = copy.deepcopy(old)
                c['id'] = prefix + c['id']
                c['label'] = member['questionRef'].replace('2026 FL ', '') + ' · ' + c['label']
                if 'deductFrom' in c:
                    c['deductFrom'] = prefix + c['deductFrom']
                criteria.append(c)
        topics = list(dict.fromkeys(t for c in members for t in [c['topicId'], *c.get('additionalTopicIds', [])]))
        return add(key, members[0]['section'], ref,
                   pool_quote + '\n\nAn rogha don chárta seo: ' + ref + '\n\n' +
                   '\n\n'.join(c['questionRef'].replace('2026 FL ', '') + '\n' + c['questionText'] for c in members),
                   topics[0], list(dict.fromkeys(t for c in members for t in c['examTopicKeys'])),
                   sorted(set(p for c in members for p in c['sourceMaterial']['pages'])),
                   sorted(set(p for c in members for p in c['schemePages'])), criteria,
                   [r for c in members for r in c['taskRequirements']], note,
                   # Member notices reach every route through memberCardIds in the Atlas builder.
                   additionalTopicIds=topics[1:], memberCardIds=[c['id'] for c in members])

    route_note = 'This is one permitted printed selection. Each selected response retains its own SEC marking criteria; alternative routes are not added to this tariff.'
    for n in '23':
        for a, b in itertools.combinations('ABC', 2):
            combine(f'R-{n}-{a}{b}', f'Léamhthuiscint · Ceist {n}({a.lower()}) + ({b.lower()})',
                    reading_cards[n + a] + reading_cards[n + b],
                    f'Ceist {n} Freagair do rogha dhá cheann de (a), (b), (c) anseo thíos.', route_note)

    def guide(p):
        text = clean(scheme[p - 1].get_text())
        assert text.startswith(f'{p} '), (p, text[:20])
        return text[len(str(p)) + 1:]

    def between(text, start, end=None):
        assert start in text and (end is None or end in text.split(start, 1)[1]), (start, end)
        part = text.split(start, 1)[1]
        return clean(part.split(end, 1)[0] if end else part)

    def language():
        return criterion('gaeilge', 'Cruinneas Gaeilge', 11, [
            'Sár-mhaith 9–11; An-mhaith 6–8; Maith / Maith go leor 3–5; Lag / An-lag 0–2 (Cruinnúsáid de gnéithe ainmnithe den ghramadach).',
            'Dul na Gaeilge: struchtúir na Gaeilge agus beachtas gramadaí. Foclóir: cruinneas agus oiriúnacht foclóra. Litriú. Ná glac le Béarla.',
            'Bronn marc as 11 ar chaighdeán na Gaeilge san iarracht iomlán.',
            'Scéim Mharcála Mhodhnaithe (scheme PDF 15): for eligible candidates spelling and the listed grammar features are not counted. It changes assessment, not the task.'])

    p7, p8, p9 = guide(7), guide(8), guide(9)
    for phrase in ['Sár-mhaith', '9-11', '6-8', '3-5', '0-2']:
        assert phrase in p7
    past = 'N.B. Beidh pionós -1 i gceist gach uair a luaitear an Aimsir Chaite.'
    assert past in p9
    notice = add('W-4A', '3', 'Scríobh · Ceist 4(a) · Fógra',
                 'Féach ar na pictiúir thíos.\n\nScríobh amach an FÓGRA a bhaineann leis an rud atá i gceist thuas.\n\n'
                 'Cén rud a bheidh ar siúl? Cén áit?\nCén lá? Cén dáta? Cén t-am? Cén táille?\nCén t-aoi speisialta a bheidh i láthair?\nCad a dhéanfar leis an airgead?',
                 'irish-9-3', ['notice'], [14], [7, 8, 9], [
                     criterion('leagan', 'Leagan Amach', 1, ['Iarracht ar fhógra 1 mharc ' + between(p8, 'Iarracht ar fhógra 1 mharc', 'Pictiúr 1')]),
                     criterion('pictiur1', 'Pictiúr 1 · rud 5 + áit 5', 10, ['Pictiúr 1 Cén rud ' + between(p8, 'Pictiúr 1 Cén rud', 'Pictiúr 2 Cén lá?'), past]),
                     criterion('pictiur2', 'Pictiúr 2 · lá 4 + dáta 3 + am 3 + táille 3', 13, ['Pictiúr 2 Cén lá? ' + between(p8, 'Pictiúr 2 Cén lá?', 'Pictiúr 3'), past]),
                     criterion('pictiur3', 'Pictiúr 3 · aoi speisialta', 5, ['Pictiúr 3 ' + between(p8, 'Pictiúr 3'), between('^' + p9, '^', 'Pictiúr 4'), past]),
                     criterion('pictiur4', 'Pictiúr 4 · an t-airgead', 5, ['Pictiúr 4 ' + between(p9, 'Pictiúr 4', 'N.B.').replace(' ` ', ' '), past]),
                     language()],
                 ['Scríobh fógra bunaithe ar na ceithre phictiúr agus ar na treoracha.'],
                 'Whole 45-mark notice: layout 1, pictures 10+13+5+5, shared language 11. Apply each −1 past-tense penalty within the affected picture award. Required headings are not choices.')
    p10, p11 = guide(10), guide(11)
    assert 'Turas go Londain' in texts[14] and 'Costas €200' in texts[14]
    letter = add('W-4B', '3', 'Scríobh · Ceist 4(b) · Litir',
                 'Féach ar na pictiúir thíos.\n\nPictiúr 1:\nTuras go Londain\nDé hAoine 9 Meitheamh – Dé Domhnaigh 11 Meitheamh\nCostas €200\n\n'
                 'Chuaigh tú ar thuras go Londain le déanaí. Scríobh litir chuig do chara ag insint dó/di:\n\n'
                 '- Faoin bpóstaer a chonaic tú (dhá phointe eolais) — Pictiúr 1\n'
                 '- Faoin taisteal ar an Aoine (dhá phointe eolais) — Pictiúr 2\n'
                 '- Faoi na rudaí a rinne tú ar an Satharn (dhá phointe eolais) — Pictiúr 3\n'
                 '- Faoi mar a chaith tú an lá deireanach (dhá phointe eolais) — Pictiúr 4\n\n'
                 'N.B. Bíodh an leagan amach cuí ar do litir: seoladh, dáta, tús agus críoch oiriúnach.',
                 'irish-9-3', ['letterWriting'], [15], [10, 11], [
                     criterion('seoladh', 'Seoladh', 2, ['Seoladh: Caithfidh ' + between(p10, 'Seoladh: Caithfidh', 'Dáta: Glac')]),
                     criterion('data', 'Dáta', 1, ['Dáta: Glac ' + between(p10, 'Dáta: Glac', 'Beannú: Ainm')]),
                     criterion('beannu', 'Beannú', 1, ['Beannú: Ainm ' + between(p10, 'Beannú: Ainm', 'Críoch: Dhá')]),
                     criterion('crioch', 'Críoch / Slán', 2, ['Críoch: Dhá ' + between(p10, 'Críoch: Dhá', '(ii)')]),
                     *[criterion(f'pictiur{i}', f'Pictiúr {i} · dhá phointe eolais (4 + 3)', 7,
                                 [f'Pictiúr {i} ' + between(p11, f'Pictiúr {i} ', f'Pictiúr {i + 1} ' if i < 4 else None)]) for i in range(1, 5)],
                     language()],
                 ['Scríobh litir chuig do chara faoin turas go Londain.', 'Dhá phointe eolais faoi gach ceann de na ceithre phictiúr; leagan amach cuí.'],
                 'Whole 45-mark letter: layout 6 (2+1+1+2), four seven-mark picture awards (4 + 3 for two points), shared language 11. Two open information points per picture are not a closed printed menu. No word-count penalty is printed for the letter.',
                 sourceDiscrepancyNotice='Nóta foinse: tá “Ceist 4(b) Foirm Iarratais” sa scéim mhodhnaithe (PDF 15), ach is litir í Ceist 4(b) in 2026.',
                 additionalTopicIds=['irish-2-8'])
    p12, p13, p14 = guide(12), guide(13), guide(14)
    length = criterion('length', 'Fad', 4, ['Líon focal: 80–90: 0; 60–79: −2; 30–59: −3; <30: −4. Apply only when marking communication out of 34; with only T1–T4 (marking out of 30, 26, 22, 18 or 14) Fad = −0.'], deduct_from='cumarsaid')
    caps = 'Five references (T1–T5) are needed to mark communication out of 34. Deduct 4 for each missing reference and mark the remainder out of 30, 26, 22, 18 or 14. Length is penalised at most once.'
    stories = []
    captions = [('Ina suí ar bhinse', 'Ag comhrá'), ('Ar strae', 'Trína chéile'), ('Ag lorg', 'Faighte'), ('Sábháilte', 'Áthas')]
    assert all(w in texts[16] for pair in captions for w in pair)
    for slot, page, scheme_pages in [('5A', 16, [12]), ('5B', 17, [13, 14])]:
        if slot == '5A':
            prompt = ('Féach ar an bpictiúr thíos.\n\nBhí tú ag Cóisir Lae Breithe an samhradh seo caite.\nTá tú chun cuntas (timpeall 90 focal) a scríobh in Iris na Scoile faoin gcóisir sin.\n\n'
                      'Scríobh an cuntas sin (timpeall 90 focal) sa spás atá faoin bpictiúr.\n\nCóisir Lae Breithe')
            guidance = [between('^' + p12, '^', 'Cruinneas Gaeilge o Bronn'),
                        'Source note: the scheme task line names “Féile cheoil”, but the paper and the scheme reference examples concern the Cóisir Lae Breithe; assess the printed 2026 task.']
            extra = dict(sourceDiscrepancyNotice='Nóta foinse: tá “Féile cheoil” i líne an taisc sa scéim, ach baineann an páipéar agus samplaí na scéime leis an gCóisir Lae Breithe.')
        else:
            prompt = ('Féach ar na pictiúir anseo thíos.\n\nTharla an eachtra seo agus tú sa pháirc le do chara.\nTá tú chun scríobh faoin eachtra seo in Iris na Scoile (timpeall 90 focal).\n\n'
                      'Scríobh faoin eachtra (timpeall 90 focal) sa spás atá faoi na pictiúir.\n\n'
                      + '\n'.join(f'{i}. {a} / {b}' for i, (a, b) in enumerate(captions, 1)) + '\n\nEachtra a Tharla agus Mé sa Pháirc')
            guidance = [between('^' + p13, '^', 'Cruinneas Gaeilge o Bronn'), p14]
            extra = {}
        for line in prompt.splitlines():
            if line and not re.match(r'\d\. ', line):
                assert in_order(line, texts[page - 1]), line
        stories.append(add('W-' + slot, '3', f'Scríobh · Ceist 5({slot[-1].lower()})' + (' · Cuntas' if slot == '5A' else ' · Eachtra'),
                           prompt, 'irish-9-4', ['pictures', 'story'], [page], scheme_pages, [
                               criterion('cumarsaid', 'Cumas Cumarsáide', 34, guidance + [caps]), language(), copy.deepcopy(length)],
                           ['Scríobh timpeall 90 focal in Iris na Scoile.', 'Tabhair cúig thagairt ar a laghad don ócáid sna pictiúir.'],
                           'Whole 45-mark story: communication 34 (−4 per missing reference: 30, 26, 22, 18 or 14), shared language 11, length deduction up to 4 only when marking out of 34. '
                           'References in the scheme are indicative, not a closed selection pool.' + (' 5(b) needs one reference to each of the four pictures plus one more.' if slot == '5B' else ''),
                           **extra))
    writing = {'4A': notice, '4B': letter, '5A': stories[0], '5B': stories[1]}
    for a, b in itertools.combinations(writing, 2):
        left, right = writing[a], writing[b]
        combine('W-' + a + '-' + b, left['questionRef'].removeprefix('2026 FL ') + ' + ' + right['questionRef'].removeprefix('2026 FL '),
                [left, right], 'Freagair dhá cheist ar bith as na ceithre cinn seo a leanas: 4 (a), 4 (b), 5 (a) nó 5 (b).',
                route_note + ' Scheme PDF 6: every attempted writing answer is marked and the best two count.')

    decisions = selection_decisions(paper)
    assert len(cards) == 70 and len({c['id'] for c in cards}) == 70
    for card in cards:
        for c in card['criteria']:
            assert all(not re.search('[-]', g) for g in c['guidance']), (card['id'], c['id'])
    sr = json.loads(SOURCE_REVIEW.read_text())
    review = dict(year=2026, level='foundation', paperFileid=FILE + '.pdf', schemeFileid=SCHEME_FILE + '.pdf',
                  paperSha256=hashlib.sha256(paper_path.read_bytes()).hexdigest(),
                  schemeSha256=hashlib.sha256(scheme_path.read_bytes()).hexdigest(),
                  reviewedPaperPages=list(range(1, 21)), reviewedSchemePages=list(range(1, 21)),
                  reviewDate=sr['reviewDate'], status='reviewed', selectionDecisions=decisions,
                  fullPaperAndApplicableSchemeVisualSweep=True,
                  atomicPracticeCardIds=[c['id'] for c in cards if 'memberCardIds' not in c],
                  pairedRouteCardIds=[c['id'] for c in cards if 'memberCardIds' in c],
                  examStructure=dict(listening=120, matching=40, readingQ2=50, readingQ3=60, writing=90, total=360),
                  nonPoolDecisions=sr['nonPoolDecisions'], openIssues=[], audio=sr['audio'],
                  boundaries='14 listening parts; 10 matching parts; 30 reading parts at their printed unequal tariffs; 4 whole writing responses; 6 paired reading routes; 6 paired writing routes.',
                  caveats=sr['sourceFindings'])
    return dict(review=review, cards=cards), scheme


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    data, scheme = build()
    scheme_md = '# Gaeilge Bonnleibhéal 2026 — SEC marking scheme\n\n' + '\n\n'.join(f'## PDF page {i + 1}\n\n' + p.get_text() for i, p in enumerate(scheme))
    outputs = {OUT: json.dumps(data, ensure_ascii=False, indent=2) + '\n',
               ROOT / 'examiner-reports/irish/schemes/2026-fl.md': '\n'.join(line.rstrip() for line in scheme_md.splitlines()).rstrip() + '\n'}
    for path, value in outputs.items():
        if args.check:
            assert path.exists() and path.read_text() == value, f'Stale Foundation output: {path}'
        else:
            path.write_text(value)
    print(f"Irish Foundation 2026: {len(data['cards'])} reviewed task/selection cards; the archive remains incomplete.")


if __name__ == '__main__':
    main()
