#!/usr/bin/env python3
"""Reviewed Foundation tasks. Counts are assertions, not corpus-completeness proof.

2022 paper pages 1–20 and scheme pages 1–24 visually reviewed on 2026-10-07.
Source hashes, selection decisions and task identities travel with the output.
The older Foundation papers remain pending in irish-archive-inventory.json.
"""
from __future__ import annotations
import argparse
import copy
import hashlib
import itertools
import json
import re
from pathlib import Path
from irish_choice import withdraw_combinations

ROOT = Path(__file__).resolve().parents[3]
FILE = 'LC001BLP000IV'
OUT = ROOT / 'components/MarkBank/cards/irish/foundation-2022-authored.json'

def clean(text):
    return re.sub(r'\s+', ' ', text).strip()

def criterion(id, label, marks, guidance, exact=False, deduct_from=None):
    return dict(id=id, label=label, kind='deduction' if deduct_from else 'award',
                maxMarks=marks, permittedMarks=[0, marks] if exact else list(range(marks+1)),
                guidanceKind='exact-answer' if exact else 'quality', guidance=guidance,
                **({'deductFrom': deduct_from} if deduct_from else {}))

DIRECTIVE = re.compile(r'rogha|roghna|Freagair|Cuir tic|Ainmnigh|Luaigh|\bchoose\b|\beither\b|\bany\b|one of|\bnó\b|dhá phointe|aintín|uncail', re.I)
SOURCE_REVIEW = ROOT / 'scripts/markbank/authored/irish-foundation-2022-source-review.json'

def selection_decisions(paper):
    decisions = json.loads(SOURCE_REVIEW.read_text())['selectionDecisions']
    expected = {(d['page'],d['raw']) for d in decisions}
    found = {(i,clean(line)) for i,page in enumerate(paper,1) for line in page.get_text().splitlines() if DIRECTIVE.search(clean(line))}
    assert found == expected, ('Unclassified/stale selection directives', found-expected, expected-found)
    return decisions

def build():
    import fitz
    paper_path = ROOT / f'paper-trail-corpus/exampapers/2022/{FILE}.pdf'
    scheme_path = ROOT / f'paper-trail-corpus/markingschemes/2022/{FILE}.pdf'
    assert hashlib.sha256(paper_path.read_bytes()).hexdigest() == '9b931da007adf04cf65c1dda4bca322eb53860c0f974f6a92370030218fc6a52', 'Paper changed: repeat visual review'
    assert hashlib.sha256(scheme_path.read_bytes()).hexdigest() == '1187a66bd529189eda5fbcd4d6ea21a5e3f4656c198c4ce01ffef78ac9a609de', 'Scheme changed: repeat visual review'
    paper = fitz.open(paper_path)
    scheme = fitz.open(scheme_path)
    texts = [clean(p.get_text()) for p in paper]
    cards = []
    def add(key, section, ref, prompt, topic, exam_topics, pages, scheme_pages, criteria,
            requirements=None, note=None, **extra):
        marks = sum(c['maxMarks'] for c in criteria if c['kind'] == 'award')
        card = dict(id=f'irish-2022-fl-{key.lower()}', year=2022, level='foundation',
            paper=1, section=section, atlasQuestionId=key,
            questionRef=f'2022 FL {ref}', questionText=prompt, totalMarks=marks,
            topicId=topic, examTopicKeys=exam_topics, conceptId=f'irish-foundation-{key.lower()}',
            paperFileid=FILE, schemePage=scheme_pages[0], schemePages=scheme_pages,
            taskRequirements=requirements or [], criteria=criteria,
            markingGuideNote=note or 'Use the answer and tariff published by the SEC for this part.',
            sourceMaterial=dict(kind='source-text', label=ref,
                title=f'Gaeilge Bonnleibhéal 2022 · {ref}', pages=pages,
                attribution='© State Examinations Commission.',
                presentationNote='Original examination pages, including every required picture or passage.'),
            **extra)
        cards.append(card)
        return card

    # Multiple-choice distractors are possible answers to ONE task, not alternative
    # tasks; expanding them would teach knowingly wrong responses as valid routes.
    aural = [('1a', 2, 7, 'Cén post atá ag máthair Ailbhe?', None, 'Múinteoir ceoil = an dara pictiúr'),
 ('1b',
  2,
  7,
  'Cén pháirt ba mhaith le hAilbhe i gceann cúpla bliain?',
  'Páirt i Ros na Rún | Páirt i ndrámaí scoile | Páirt i scannáin mhóra',
  'Páirt i scannáin mhóra: 7 marc. Páirt i Ros na Rún: 5 mharc.'),
 ('2a', 2, 7, 'Cá háit a bhfuil Seán ina chónaí faoi láthair?', None, 'Páras = an tríú pictiúr'),
 ('2b',
  2,
  7,
  'Cén fáth a mbíonn na mílte cuairteoir i bPáras gach bliain?',
  'Chun freastal ar mheánscoil | Chun na radhairc a fheiceáil | Chun dul ag obair',
  'Chun na radhairc a fheiceáil'),
 ('3', 3, 8, 'Cá bhfuil an bhean ag dul?', None, 'Ionad Sláinte = an tríú pictiúr'),
 ('4',
  3,
  8,
  'Cá bhfuil an siopa éadaí? (Cuir tic (✓) sa bhosca ceart.)',
  None,
  'An bosca ag an mbarr ar dheis (tic nó saighead sa bhosca)'),
 ('5a', 3, 8, 'Conas mar a bheidh an aimsir don cheolchoirm mhór i bPáirc an Chrócaigh?', None, 'Báisteach = an tríú pictiúr'),
 ('5b',
  3,
  8,
  'Cén teocht is airde a bheidh ann amárach?',
  '20° Celsius | 22° Celsius | 28° Celsius',
  '28 céim Celsius: 8 marc. 22 céim Celsius: 6 mharc.'),
 ('6a',
  4,
  10,
  'Cén fáth nach bhfuil a Daid sásta le hAisling?',
  'Fuair sí tatú. | Fuair sí peata madra. | Cheannaigh sí éadaí nua.',
  'Fuair sí tatú'),
 ('6b', 4, 10, 'Cé mhéad a chosain an rothar?', '€75 | €90 | €220', '€220'),
 ('7a',
  4,
  10,
  'Cad a bheidh ar siúl ag Síle ar an Aoine?',
  'Beidh sí ag cóisir. | Beidh sí ag staidéar. | Beidh sí ag imirt cluiche.',
  'Beidh sí ag staidéar'),
 ('7b',
  4,
  10,
  'Cén saghas scannáin nua a bheidh ar siúl sa phictiúrlann?',
  'Scannán rómánsúil | Scannán eachtraíochta | Scannán ficsean eolaíochta',
  'Scannán rómánsúil'),
 ('8a', 4, 10, 'Cé a bhí ag siopadóireacht le Rian in Chicago gach lá?', 'Caoimhe | A uncail | A chol ceathracha', 'A chol ceathracha'),
 ('8b', 4, 10, 'Cad a cheannaigh Rian dá mháthair?', 'Bróga reatha | Uaireadóir galánta | Cúpla húdaí gleoite', 'Uaireadóir galánta')]
    audio_url = 'https://www.examinations.ie/archive/exampapers/2022/LC001BLP017IV.mp3'
    for n,page,marks,prompt,options,answer in aural:
        comparable = lambda s: re.sub(r'[^\w]+','',s.lower())
        assert re.search('.*?'.join(re.escape(comparable(w)) for w in prompt.split()), comparable(texts[page-1])), (n,prompt)
        for option in (options or '').split(' | '):
            assert comparable(option) in comparable(texts[page-1]), (n,option)
        ref = 'Cluastuiscint · Ceist ' + re.sub(r'([ab])$',r'(\1)',n)
        card = add('A-'+n,'1',ref,re.sub(r'^(\d+)([ab]?)$', lambda m: m[1]+'. '+('('+m[2]+') ' if m[2] else ''), n)+prompt+
            ('\n\n'+options.replace(' | ','\n') if options else ''),
            'irish-1-3',['aural'],[page],[3],
            [criterion('answer','Freagra',marks,[answer],True)],
            ['Éist leis an taifeadadh. Úsáid na pictiúir ar an leathanach nuair is gá.'],
            audioMaterial=dict(kind='source-audio',label=ref,
                title='Gaeilge Bonnleibhéal 2022 · An Chluastuiscint',playbackUrl=audio_url,
                secFileid='LC001BLP017IV.mp3',canonicalUrl=audio_url,
                attribution='© State Examinations Commission.',
                presentationNote='Official Foundation Level recording. Answer the question shown using its printed options.'))

    # The scheme explicitly allows partial credit for these two MCQs.
        if n in ['1b','5b']:
            card['criteria'][0]['permittedMarks'] = [0,5,7] if n == '1b' else [0,6,8]

    signs = ['Scoil Cheoil\nRanganna ceoil gach Aoine\nSaor in aisce',
 'Bialann Shíneach\nDíreach go dtí do dhoras\nOrdaigh ar líne',
 'Ceachtanna Tiomána\nAr fáil\nGlaoigh ar 096-764390',
 'Ionad Athchúrsála\nBruscar tí amháin',
 'Aire!\nUrlár fliuch\nBí cúramach',
 'An Siopa Leabhar\nFoclóir Nua Béarla-Gaeilge ar díol',
 'Club Leadóige\nFáilte roimh dhéagóirí\nCláraigh anois',
 'Bád Farantóireachta\nTuras go hOileáin Árann\n€20.00 an duine',
 'Seomra Ríomhairí\nCosc ar bhia agus ar dheoch',
 'Madra ar strae\nDath dubh agus bán\nGlaoigh ar: 01 548 9321']
    for i,(sign,answer) in enumerate(zip(signs,'CEDGJBIFAH'),1):
        add(f'R-1-{i}','2',f'Léamhthuiscint · Ceist 1({i})',
            'Meaitseáil na pictiúir leis na fógraí/comharthaí agus scríobh síos an litir cheart sa bhosca in aice leis an uimhir cheart atá sa ghreille.\n\n'+f'{i}. {sign}',
            'irish-9-1',['match'],[5],[4],
            [criterion('answer','Litir cheart',4,[answer,
                'Glactar le córas eile (uimhir an phictiúir in ionad litir an phictiúir) má tá sé soiléir / intuigthe.'],True)])

    # Each row: verbatim question, printed alternatives (or none), official answer.
    reading = {'2A': (6,
        'letterReading',
        [('Cén dáta ar sheol Máire an fhoirm iarratais isteach?', '7 Meitheamh | 10 Meitheamh | 16 Meitheamh', '7 Meitheamh'),
         ('Cad atá á thiomáint ag Máire ina post faoi láthair?', 'Carr | Leoraí | Mionbhus', 'Mionbhus'),
         ('Conas a iarrtar ar Mháire glacadh leis an agallamh?',
          'Glaoch fóin a chur | Ríomhphost a sheoladh | Litir a scríobh',
          'Glaoch fóin a chur'),
         ('Cá fhad a leanann an cúrsa traenála de ghnáth?', 'Ar feadh seachtaine | Ar feadh coicíse | Ar feadh míosa', 'Ar feadh coicíse'),
         ('Cén post atá ag Liam Ó Laoire?', 'Rúnaí oifige | Traenálaí sinsearach | Tiománaí bus', 'Traenálaí sinsearach')]),
 '2B': (7,
        'brochure',
        [('Cén saghas saoire atá ar fáil ar an tSionainn?',
          'Saoire thar lear | Saoire cois trá | Saoire ag bádóireacht',
          'Saoire ag bádóireacht'),
         ('Cén contae ina bhfuil Cora Droma Rúisc?', 'Contae na Gaillimhe | Contae Liatroma | Contae an Chabháin', 'Contae Liatroma'),
         ('Cén rud is fearr le gach duine ar bord an bháid?',
          'Ceangal idirlín agus Wi-Fi | Cistin bheag | Seomra leapa compordach',
          'Ceangal idirlín agus Wifi'),
         ('Cad atá ar fáil don duine spórtúil cois abhann?',
          'Bialanna agus béilí blasta | Siopaí agus caiféanna | Machairí gailf den scoth',
          'Machairí gailf den scoth'),
         ('Cad is féidir a dhéanamh má bhíonn an aimsir go dona?',
          'Luí siar ar an mbád | Fanacht te teolaí sa bhád | An spotsolas a lasadh',
          'Fanacht te teolaí sa bhád')]),
 '2C': (8,
        'news',
        [('Cad a theastaigh ó Bhríd?', 'Dul ar scoil | Dul go dtí teach na cúirte | Dul ag siopadóireacht', 'Dul ag siopadóireacht'),
         ('Cén t-am ar bhuail Bríd agus Dónall lena chéile?', 'Luath ar maidin | Ag meán lae | Déanach sa tráthnóna', 'Ag meán lae'),
         ('Cad a rinne na déagóirí nuair a chonaic siad na robálaithe?',
          'Chuir siad fios ar na Gardaí. | Rith siad síos an tsráid. | Ghabh siad na robálaithe.',
          'Chuir siad fios ar na gardaí'),
         ('Cad a rinne na robálaithe nuair a tháinig na Gardaí?',
          'Thiomáin siad an carr. | Rith siad isteach sa siopa. | Scaoil siad urchar leo.',
          'Scaoil siad urchair leo'),
         ('Cé a fuair dearbháin ó úinéir an tsiopa?', 'Na Gardaí | Na déagóirí | Na robálaithe', 'Na déagóirí')]),
 '3A': (9,
        'news',
        [('Cén bhliain a rugadh Dermot Kennedy?', '2015 | 1991 | 2014', '1991'),
         ('Cén aois a bhí ag Dermot Kennedy nuair a thosaigh sé ag scríobh amhrán?',
          '10 mbliana d’aois | 13 bliana d’aois | 14 bliana d’aois',
          '14 bliana d’aois'),
         ('Cén áit ar fhreastail Dermot ar an ollscoil?',
          'I gCo. Chill Dara | I gCo. Bhaile Átha Cliath | Sna Stáit Aontaithe',
          'Co. Chill Dara'),
         ('Cad a bhíodh á dhéanamh ag Dermot Kennedy go minic i mBaile Átha Cliath?',
          'Ag freastal ar ollscoil | Ag buscáil ar na sráideanna | Ag tosú grúpa ceoil nua',
          'Ag buscail ar na sráideanna'),
         ('Cad a fuair an singil Giants agus an t-amhrán Better Days ar na meáin shóisialta?', None, 'Moladh mór / a lán poiblíochta')]),
 '3B': (10,
        'extract',
        [('Cé dóibh is mó a scríobhann Áine leabhair?', 'Do dhaoine fásta | Do léachtóirí | Do dhéagóirí', 'Do dhéagóirí'),
         ('Cá háit ar rugadh Áine Ní Ghlinn?', 'I mBaile Átha Cliath | I gCo. Thiobraid Árann | I Londain', 'I gCo Thiobraid Árann'),
         ('Cén post a fuair Áine nuair a d’fhág sí an ollscoil?',
          'Iriseoir le RTÉ | Múinteoir meánscoile | Obair le Ros na Rún',
          'Múinteoir meánscoile'),
         ('Cathain a ceapadh Áine Ní Ghlinn mar Laureate na nÓg?', '2017 | 2019 | 2020', '2020'),
         ('Cad a bhuaigh an scéal Boscadán?', None, 'Duais')]),
 '3C': (11,
        'poem',
        [('Cén t-ainm atá ar athair Sheáin?', 'Cat | Seán | Tadhg', 'Tadhg'),
         ('Cad a bhíonn ar siúl go sámh ag Seán agus an cat?',
          'Bíonn siad ag rith. | Bíonn siad ag súgradh. | Bíonn siad ar fán.',
          'Súgradh'),
         ('Cén dath atá ar an gcat?', 'Bán | Breá | Dubh', 'Bán'),
         ('Cá háit a rachaidh Seán?', 'Abhaile | Ar scoil | Ar saoire', 'Ar scoil'),
         ('Cá rachaidh an cat nuair a bheidh Seán ar scoil?', None, 'ar fán / i measc cat na gcomharsan')])}
    reading_cards = {}
    for slot,(page,exam_topic,rows) in reading.items():
        reading_cards[slot] = []
        for i,(prompt,options,answer) in enumerate(rows,1):
            # Fail on stale question text; normalize only punctuation differences
            # between PDF fonts and the accessible prompt.
            comparable = lambda s: re.sub(r'[^\w]+','',s.lower())
            assert re.search('.*?'.join(re.escape(comparable(w)) for w in prompt.split()), comparable(texts[page-1])), (slot,i,prompt)
            for option in (options or '').split(' | '):
                assert comparable(option) in comparable(texts[page-1]), (slot,i,option)
            for accepted in answer.split(' / '):
                assert comparable(accepted) in comparable(scheme[4 if slot[0]=='2' else 5].get_text()), (slot,i,accepted)
            card = add(f'R-{slot}-{i}','2',f'Léamhthuiscint · Ceist {slot[0]}({slot[1].lower()})({i})',
                f'Léigh an téacs ar leathanach {page}.\n\n{i}. '+prompt+
                ('\n\n'+options.replace(' | ','\n') if options else ''),
                'irish-9-2',[exam_topic],[page],[5 if slot[0]=='2' else 6],
                [criterion('answer','Freagra',5 if slot[0]=='2' else 6,[answer],True)])
            reading_cards[slot].append(card)

    def combine(key,ref,members,pool_quote):
        criteria=[]
        for member in members:
            prefix=member['atlasQuestionId'].lower()+'-'
            for old in member['criteria']:
                c=copy.deepcopy(old)
                c['id']=prefix+c['id']
                c['label']=member['questionRef'].replace('2022 FL ','')+' · '+c['label']
                if 'deductFrom' in c: c['deductFrom']=prefix+c['deductFrom']
                criteria.append(c)
        topics=list(dict.fromkeys(t for c in members for t in [c['topicId'],*c.get('additionalTopicIds',[])]))
        result=add(key,members[0]['section'],ref,
            pool_quote+'\n\nAn rogha don chárta seo: '+ref+'\n\n'+
            '\n\n'.join(c['questionRef'].replace('2022 FL ','')+'\n'+c['questionText'] for c in members),
            topics[0],list(dict.fromkeys(t for c in members for t in c['examTopicKeys'])),
            sorted(set(p for c in members for p in c['sourceMaterial']['pages'])),
            sorted(set(p for c in members for p in c['schemePages'])),criteria,
            [r for c in members for r in c['taskRequirements']],
            'This is one permitted printed selection. Each selected response retains its own SEC marking criteria; alternative routes are not added to this tariff.',
            additionalTopicIds=topics[1:], memberCardIds=[c['id'] for c in members])
        return result

    for n in '23':
        for a,b in itertools.combinations('ABC',2):
            combine(f'R-{n}-{a}{b}',f'Léamhthuiscint · Ceist {n}({a.lower()}) + ({b.lower()})',
                reading_cards[n+a]+reading_cards[n+b],
                f'Ceist {n} Freagair do rogha dhá cheann de (a), (b), (c) anseo thíos.')

    language=criterion('gaeilge','Cruinneas Gaeilge',11,[
        'Sármhaith 9–11; An-mhaith 7–8; Maith 5–6; Lag 2–4; An-lag 1; Easnamhach 0.',
        'Dul na Gaeilge: struchtúr na Gaeilge agus beachtas gramadaí. Foclóir: cruinneas agus oiriúnacht foclóra. Litriú.',
        'Bronn marc as 11 ar chaighdeán na Gaeilge san iarracht iomlán.'])
    def scheme_guidance(start,end):
        return [clean(re.sub(r'\n\s*\d+\s*$', '', scheme[p-1].get_text())) for p in range(start,end+1)]
    notice_p9 = scheme_guidance(9,9)[0]
    notice_p10 = scheme_guidance(10,10)[0]
    notice = add('W-4A','3','Scríobh · Ceist 4(a)',
        'Féach ar na pictiúir thíos.\n\nScríobh amach an FÓGRA a bhaineann leis an rud atá i gceist thuas.\n\n'+
        'Cén rud a bheidh ar siúl? Cén áit?\nCén lá? Cén dáta? Cén t-am? Cead isteach?\nCén t-aoi speisialta a bheidh i láthair?\nCá rachaidh an t-airgead?',
        'irish-9-3',['notice'],[14],[8,9,10],[
            criterion('leagan','Leagan Amach',1,['Iarracht ar fhógra.']),
            criterion('pictiur1','Pictiúr 1',10,[notice_p9.split('Pictiúr 1',1)[1].split('Pictiúr 2',1)[0]]),
            criterion('pictiur2','Pictiúr 2',13,[notice_p9.split('Pictiúr 2',1)[1].split('Pictiúr 3',1)[0]]),
            criterion('pictiur3','Pictiúr 3',5,[notice_p9.split('Pictiúr 3',1)[1]]),
            criterion('pictiur4','Pictiúr 4',5,[notice_p10.split('Pictiúr 4',1)[1].split('Cuir tic',1)[0]]),copy.deepcopy(language)],
        ['Scríobh fógra bunaithe ar na ceithre phictiúr agus ar na treoracha.'],
        'Award the published picture submarks and one shared language mark. Follow the exact 2022 partial-credit and date/currency/name-only rules within the affected picture awards. Required headings are not choices.')
    letter = add('W-4B','3','Scríobh · Ceist 4(b)',
        'Féach ar na pictiúir thíos.\n\nBhí tú ag ceolchoirm mhór i bPáirc Mharlaí.\nScríobh litir chuig d’aintín / d’uncail i Meiriceá ag insint dó / di:\n\n'
        '- Faoin bpóstaer a chonaic tú (dhá phointe eolais) — Pictiúr 1\n'
        '- Faoin turas go dtí an cheolchoirm (dhá phointe eolais) — Pictiúr 2\n'
        '- Faoin gceolchoirm (dhá phointe eolais) — Pictiúr 3\n'
        '- Faoi na rudaí a rinne tú nuair a bhí an cheolchoirm thart (dhá phointe eolais) — Pictiúr 4\n\n'
        'N.B. Bíodh an leagan amach cuí ar do litir: seoladh, dáta, tús agus críoch oiriúnach.',
        'irish-9-3',['letterWriting'],[15],[11,12],[
            criterion('seoladh','Seoladh',2,['Dhá chuid (1 + 1), as Gaeilge. Glac lena leithéid de “Bóthar Crumlin” nó “Sráid Patrick”. Ná glac le hainm an bhaile i mBéarla.']),
            criterion('data','Dáta',1,['Glac le figiúirí.']),
            criterion('beannu','Beannú',1,['Ainm ar bith, fiú a chara.']),
            criterion('crioch','Críoch / Slán',2,['Dhá chuid ag teastáil: Slán … agus ainm.']),
            *[criterion(f'pictiur{i}',f'Pictiúr {i} · dhá phointe eolais',7,
                [scheme_guidance(12,12)[0].split(f'Pictiúr {i}',1)[1].split(f'Pictiúr {i+1}',1)[0].split('Cuir tic',1)[0]]) for i in range(1,5)],
            copy.deepcopy(language)],
        ['Scríobh litir chuig d’aintín nó d’uncail i Meiriceá faoin gceolchoirm.',
         'Dhá phointe eolais faoi gach ceann de na ceithre phictiúr; leagan amach cuí.'],
        'The letter stays whole: six layout marks, four seven-mark picture awards (4 + 3 for two points), and one shared eleven-mark language award. Two open information points per picture are not a closed printed menu. There is no word-count penalty in the published letter scheme.', additionalTopicIds=['irish-2-8'])
    # Mechanically expand the two printed recipients; all letter criteria stay whole.
    cards.remove(letter)
    for recipient in ['aintin','uncail']:
        route=copy.deepcopy(letter)
        route['id'] += '-'+recipient
        route['atlasQuestionId'] += '-'+recipient
        route['conceptId'] += '-'+recipient
        label='d’aintín' if recipient == 'aintin' else 'd’uncail'
        route['questionRef'] += ' · '+label
        route['questionText'] += '\n\nAn rogha don chárta seo: litir chuig '+label+'.'
        cards.append(route)

    stories=[]
    for slot,page,end,title in [('5A',16,13,'Cuntas'),('5B',17,15,'Eachtra')]:
        prompt = (
            'Féach ar an bpictiúr thíos.\n\nBhí tú ar Saoire Cois Farraige an mhí seo caite.\nTá tú chun cuntas (timpeall 90 focal) a scríobh in Iris na Scoile faoin tsaoire sin.\n\nScríobh an cuntas sin (timpeall 90 focal) sa spás atá faoin bpictiúr.\n\nSaoire Cois Farraige'
            if slot == '5A' else
            'Féach ar na pictiúir anseo thíos.\n\nTharla an eachtra seo agus tú ar do bhealach abhaile ón scoil le do chara.\nTá tú chun scríobh faoin eachtra seo in Iris na Scoile (timpeall 90 focal).\n\nScríobh faoin eachtra (timpeall 90 focal) sa spás atá faoi na pictiúir.\n\nEachtra a Tharla'
        )
        stories.append(add('W-'+slot,'3','Scríobh · Ceist '+slot[0]+'('+slot[1].lower()+')',
            prompt,'irish-9-4',['pictures','story'],[page],list(range(13 if slot=='5A' else 14,end+1)),[
                criterion('cumarsaid','Cumas Cumarsáide',34,scheme_guidance(13 if slot=='5A' else 14,end)),
                copy.deepcopy(language),
                criterion('length','Fad',4,['80–90 focal: 0; 60–79: −2; 30–59: −3; <30: −4.'],deduct_from='cumarsaid')],
            ['Scríobh timpeall 90 focal in Iris na Scoile.','Tabhair cúig thagairt ar a laghad don ócáid sna pictiúir.'],
            'References in the scheme are indicative, not a closed selection pool. One shared communication award and one language award cover the whole response. For 5(b), the published text conflicts: a −4 bullet and 34/30/26/22/18 caps appear alongside a later −5 line and Tagairt /−12 header. The complete wording is retained; no extra automatic reference deduction is applied.'))
    # The 2022 paper selects ONE writing response: no paired writing routes.
    # Classify exact raw directive lines across all twenty paper pages. Unknown
    # additions on an already-reviewed page and stale keys both fail generation.
    decisions = selection_decisions(paper)
    assert len(cards)==65 and len({c['id'] for c in cards})==65
    assert sum(c['totalMarks'] for c in cards if c['atlasQuestionId'].startswith('A-'))==120
    review=dict(year=2022,level='foundation',paperFileid=FILE+'.pdf',
        paperSha256=hashlib.sha256(paper_path.read_bytes()).hexdigest(),
        schemeSha256=hashlib.sha256(scheme_path.read_bytes()).hexdigest(),
        reviewedPaperPages=list(range(1,21)),reviewedSchemePages=list(range(1,25)),
        reviewDate='2026-10-07',status='reviewed',selectionDecisions=decisions,
        fullPaperAndApplicableSchemeVisualSweep=True,
        atomicPracticeCardIds=[c['id'] for c in cards if 'memberCardIds' not in c],
        pairedRouteCardIds=[c['id'] for c in cards if 'memberCardIds' in c],
        examStructure=dict(listening=120,matching=40,readingQ2=50,readingQ3=60,writing=45,total=315),
        nonPoolDecisions=[
            'MCQ distractors and map boxes are answers to one task, not independently valid task routes.',
            'All notice headings and letter picture instructions are compulsory context. One language award covers each whole response; the two printed letter recipients are separately expanded.',
            'The two information points in each letter picture and source-retrieval answers are content choices, not enumerated task prompts.',
            'The five story references are a communication criterion, with non-exhaustive examples, not a printed choose-five menu.',
            'The modified marking scheme changes assessment for eligible candidates, not the printed task or answer route.',
        ],
        openIssues=[],
        audio=json.loads(SOURCE_REVIEW.read_text())['audio'],
        boundaries='14 listening parts; 10 matching parts; 30 reading parts; 5 whole writing routes including two letter recipients; 6 paired reading routes; no paired writing routes.',
        caveats=json.loads(SOURCE_REVIEW.read_text())['sourceFindings'])
    return withdraw_combinations(dict(review=review,cards=cards)),scheme

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check',action='store_true')
    args=parser.parse_args()
    data,scheme=build()
    content=json.dumps(data,ensure_ascii=False,indent=2)+'\n'
    scheme_text='# Gaeilge Bonnleibhéal 2022 — SEC marking scheme\n\n'+'\n\n'.join(f'## PDF page {i+1}\n\n'+p.get_text() for i,p in enumerate(scheme))
    outputs={OUT:content,ROOT/'examiner-reports/irish/schemes/2022-fl.md':scheme_text}
    for path,value in outputs.items():
        if args.check:
            assert path.exists() and path.read_text()==value, f'Stale Foundation output: {path}'
        else: path.write_text(value)
    print(f"Irish Foundation 2022: {len(data['cards'])} reviewed task/selection cards; archive remains incomplete.")

if __name__=='__main__': main()
