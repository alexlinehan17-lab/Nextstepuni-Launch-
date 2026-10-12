#!/usr/bin/env python3
"""Reviewed Foundation tasks. Counts are assertions, not corpus-completeness proof.

2015 paper pages 1–20 and scheme pages 1–24 visually reviewed on 2026-10-07.
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
OUT = ROOT / 'components/MarkBank/cards/irish/foundation-2015-authored.json'

def clean(text):
    return re.sub(r'\s+', ' ', text).strip()

def criterion(id, label, marks, guidance, exact=False, deduct_from=None):
    return dict(id=id, label=label, kind='deduction' if deduct_from else 'award',
                maxMarks=marks, permittedMarks=[0, marks] if exact else list(range(marks+1)),
                guidanceKind='exact-answer' if exact else 'quality', guidance=guidance,
                **({'deductFrom': deduct_from} if deduct_from else {}))

DIRECTIVE = re.compile(r'rogha|roghna|Freagair|Cuir tic|Ainmnigh|Luaigh|\bchoose\b|\beither\b|\bany\b|one of|\bnó\b|dhá phointe|dhá rud|dheartháir|dheirfiúr|dó / d[ií]', re.I)
SOURCE_REVIEW = ROOT / 'scripts/markbank/authored/irish-foundation-2015-source-review.json'

def scheme_page_text(page):
    return page.get_text()

def selection_decisions(paper):
    decisions = json.loads(SOURCE_REVIEW.read_text())['selectionDecisions']
    expected = {(d['page'],d['raw']) for d in decisions}
    found = {(i,clean(line)) for i,page in enumerate(paper,1) for line in page.get_text().splitlines() if DIRECTIVE.search(clean(line))}
    assert found == expected, ('Unclassified/stale selection directives', found-expected, expected-found)
    return decisions

def build():
    import fitz
    paper_path = ROOT / f'paper-trail-corpus/exampapers/2015/{FILE}.pdf'
    scheme_path = ROOT / f'paper-trail-corpus/markingschemes/2015/{FILE}.pdf'
    assert hashlib.sha256(paper_path.read_bytes()).hexdigest() == '1859a73f6d6302abe096bcb38eccf61226f71e85a14f5f8f28f8b485ce3741e7', 'Paper changed: repeat visual review'
    assert hashlib.sha256(scheme_path.read_bytes()).hexdigest() == '838e7acdab6558a4103fdd928bf09c7f63ed92bdc4b0f651acb0a67c0cc62944', 'Scheme changed: repeat visual review'
    paper = fitz.open(paper_path)
    scheme = fitz.open(scheme_path)
    texts = [clean(p.get_text()) for p in paper]
    cards = []
    def add(key, section, ref, prompt, topic, exam_topics, pages, scheme_pages, criteria,
            requirements=None, note=None, **extra):
        marks = sum(c['maxMarks'] for c in criteria if c['kind'] == 'award')
        card = dict(id=f'irish-2015-fl-{key.lower()}', year=2015, level='foundation',
            paper=1, section=section, atlasQuestionId=key,
            questionRef=f'2015 FL {ref}', questionText=prompt, totalMarks=marks,
            topicId=topic, examTopicKeys=exam_topics, conceptId=f'irish-foundation-{key.lower()}',
            paperFileid=FILE, schemePage=scheme_pages[0], schemePages=scheme_pages,
            taskRequirements=requirements or [], criteria=criteria,
            markingGuideNote=note or 'Use the answer and tariff published by the SEC for this part.',
            sourceMaterial=dict(kind='source-text', label=ref,
                title=f'Gaeilge Bonnleibhéal 2015 · {ref}', pages=pages,
                attribution='© State Examinations Commission.',
                presentationNote='Original examination pages, including every required picture or passage.'),
            **extra)
        cards.append(card)
        return card

    # Multiple-choice distractors are possible answers to ONE task, not alternative
    # tasks; expanding them would teach knowingly wrong responses as valid routes.
    aural = [('1a', 2, 7, 'Cén post atá ag Áine?', None, 'Báicéir = an tríú pictiúr'),
 ('1b',
  2,
  7,
  'Cén t-am a théann Áine abhaile gach lá?',
  'Ar a haon a chlog | Ar a seacht a chlog | Ar a deich a chlog',
  'Ar a haon a chlog'),
 ('2a', 2, 7, 'Cén spórt a imríonn Cian?', None, 'Leadóg = an chéad phictiúr'),
 ('2b',
  2,
  7,
  'Cén áit a bhfuil Cian ag obair faoi láthair?',
  'Dún Dealgan | Béal Feirste | Muineachán',
  'Béal Feirste'),
 ('3', 3, 8, 'Cá bhfuil an bhean ag dul?', None, 'An Fiaclóir = an ceathrú pictiúr'),
 ('4',
  3,
  8,
  'Cá bhfuil Siopa na Ríomhairí? (Cuir tic (✓) sa bhosca ceart.)',
  None,
  'An bosca in aice leis an ospidéal (tic nó saighead sa bhosca)'),
 ('5a', 3, 8, 'Conas a bheidh an aimsir amárach?', None, 'Tirim / Gaofar = an chéad phictiúr'),
 ('5b',
  3,
  8,
  'Cá stopfaidh na rothaithe le haghaidh lóin?',
  'Ar an gCeathrú Rua | I nGaillimh | Sa Spidéal',
  'Sa Spidéal'),
 ('6a',
  4,
  10,
  'Cén fáth a raibh an príomhoide ar buile le Cáit?',
  'Bhí sí déanach inné | Bhí sí ina suí go dtí meán oíche | Ní dhearna sí an obair bhaile',
  'Bhí sí déanach inné'),
 ('6b',
  4,
  10,
  'Cén obair bhaile nach bhfuil déanta ag an mbeirt acu ar maidin?',
  'Béarla | Matamaitic | Stair',
  'Matamaitic'),
 ('7a',
  4,
  10,
  'Cad a tharla do ghluaisrothar Bhriain?',
  'Goideadh é | Dhíol sé é | Scriosadh é',
  'Dhíol sé é'),
 ('7b',
  4,
  10,
  'Cén post a bheidh ag Brian i Londain ón Luan seo chugainn?',
  'Post i siopa crua-earraí | Post ar láithreán tógála | Post in ionad spóirt',
  'Post in ionad spóirt'),
 ('8a',
  4,
  10,
  'Cá mbeidh Orlaith ag dul i mí Dheireadh Fómhair?',
  'Ar an meánscoil | Ar an Institiúid Teicneolaíochta | Ar an ollscoil',
  'Ar an ollscoil'),
 ('8b',
  4,
  10,
  'Cén fáth a bhfuil Orlaith buartha faoi Chóisir na Debs?',
  'Níl páirtí aici | Níl gúna aici | Níl ticéid aici',
  'Níl páirtí aici')]
    audio_url = 'https://www.examinations.ie/archive/exampapers/2015/LC001BLP017IV.mp3'
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
                title='Gaeilge Bonnleibhéal 2015 · An Chluastuiscint',playbackUrl=audio_url,
                secFileid='LC001BLP017IV.mp3',canonicalUrl=audio_url,
                attribution='© State Examinations Commission.',
                presentationNote='Official Foundation Level recording. Answer the question shown using its printed options.'))


    signs = ['Coimeád an trá glan\nÚsáid na boscaí bruscair',
 'Ceoláras Loch Garman\nCeoldráma Anocht\n“Romeo agus Juliet”',
 'Réamhaisnéis na hAimsire\n“An Aimsir Láithreach”\nGach lá ar TG4',
 'Géill Slí\nTimpeallán Romhat',
 'Cluiche Rugbaí - Staid Aviva\nÉire v An Astráil\nDé Sathairn, 5 Samhain',
 'Bád Farantóireachta\n€3.50 an duine\nCeannaigh Ticéad\nRoimh dhul ar bord',
 '“Spáráil Uisce”\nNá fág an sconna ar siúl',
 'Banc na Scoile\nAr oscailt: 1.00 - 1.30 p.m.\nGach Céadaoin',
 'Bialann Iodálach\nPíotsa agus Pasta den scoth\nAr oscailt 5.30 – 11.00 p.m.',
 'Fón póca caillte\nDath dubh air\nGlaoigh ar 089-135842']
    for i,(sign,answer) in enumerate(zip(signs,'GIBHADJFCE'),1):
        add(f'R-1-{i}','2',f'Léamhthuiscint · Ceist 1({i})',
            'Meaitseáil na pictiúir leis na fógraí/comharthaí agus scríobh síos an litir cheart sa bhosca in aice leis an uimhir cheart atá sa ghreille.\n\n'+f'{i}. {sign}',
            'irish-9-1',['match'],[5],[4],
            [criterion('answer','Litir cheart',4,[answer,
                'Glactar le córas eile (uimhir an phictiúir in ionad litir an phictiúir) má tá sé soiléir / intuigthe.'],True)])

    # Each row: verbatim question, printed alternatives (or none), official answer.
    reading = {'2A': (6,
        'letterReading',
        [('Cá bhfuil Óstán an Chnoic?',
          'Co. Dhún na nGall | Co. na Gaillimhe | Co. Shligigh',
          'Co. Dhún na nGall'),
         ('Cén post a theastaíonn ó Eoin?', 'Doirseoir | Freastalaí | Fáilteoir', 'Fáilteoir'),
         ('Cén grád a fuair Eoin sa Ghaeilge san Ardteistiméireacht?', 'Grád A | Grád B | Grád C', 'Grád B'),
         ('Cé mhéad bliain a chaith Eoin ag obair sa Fhrainc?', '2 | 3 | 4', '3'),
         ('Cad atá ag Eoin ó na hóstáin thar lear?',
          'Grianghraf | Teastas tiomána | Teastais oibre',
          'Teastais oibre')]),
 '2B': (7,
        'brochure',
        [('Cén áit a bhfuil “Slí an Atlantaigh Fhiáin”?',
          'I Meiriceá | In Éirinn | Ar an Mór-Roinn',
          'In Éirinn'),
         ('Gabhann “Slí an Atlantaigh Fhiáin” trí ...', '2 chontae | 5 chontae | 9 gcontae', '9 gcontae'),
         ('Cad a chuirfidh áthas ar do chroí gach oíche?',
          'Áilleacht an chósta | Áiteanna stairiúla | An ghrian ag dul faoi',
          'An ghrian ag dul faoi'),
         ('Cad a bhíonn ar siúl ar chósta Mhaigh Eo?', 'Seoltóireacht | Galf | Surfáil', 'Seoltóireacht'),
         ('Cá mbeidh an ceol traidisiúnta le cloisteáil?',
          'Sna bialanna | Sna tithe tábhairne | Ar an mbád',
          'Sna tithe tábhairne')]),
 '2C': (8,
        'news',
        [('Cá ndeachaigh Muiris agus Emer ag am lóin Dé Máirt seo caite?',
          'Ar ais ar scoil | Abhaile ón scoil | Suas dréimire',
          'Abhaile ón scoil'),
         ('Cá raibh Pól ina sheasamh?', 'Ag an doras | Sa ghairdín | Ar bharr dréimire', 'Ar bharr dréimire'),
         ('Cad a chuala Emer agus í sa chistin?',
          'Pól ag titim | Madra ag tafann | Muiris ag caint',
          'Madra ag tafann'),
         ('Cé a fuair an bindealán ón teach?', 'Emer | Pól | Muiris', 'Emer'),
         ('Cén áit a bhfuil Pól faoi láthair?', 'Sa teach | Sa scoil | San ospidéal', 'San ospidéal')]),
 '3A': (9,
        'news',
        [('Tá clú agus cáil ar Katie Taylor ...',
          'Mar réalta phopcheoil | Mar mhainicín | Mar dhornálaí',
          'Mar dhornálaí'),
         ('Cad a bhuaigh Katie sa bhliain 2012?',
          'Bonn airgid | Bonn Oilimpeach | Bonn Eorpach',
          'Bonn Oilimpeach'),
         ('Cén spórt a d’imir Katie le foireann idirnáisiúnta na hÉireann?',
          'Sacar | Camógaíocht | Peil Ghaelach',
          'Sacar'),
         ('Cad a scríobh Katie tar éis na gCluichí Oilimpeacha?',
          'Véarsaí | Leabhar | Paidreacha',
          'Leabhar'),
         ('Cad a dhéanann Katie nuair a bhíonn am saor aici?',
          None,
          'Téann sí chuig an bpictiúrlann nó chuig bialann lena cairde')]),
 '3B': (10,
        'extract',
        [('Cén áit sa chathair a bhfuil Ard-Oifig an Phoist?',
          'Faiche an Choláiste | Imeall na cathrach | Sráid Uí Chonaill',
          'Sráid Uí Chonaill'),
         ('Cad is féidir a cheannach in Ard-Oifig an Phoist?',
          'Litreacha | Stampaí poist | Cuntas',
          'Stampaí poist'),
         ('Cad a bhíodh thuas staighre do na hoibrithe?', 'Árasáin | Capaill | Stáblaí', 'Árasáin'),
         ('Cad a cuireadh in airde ar an bhfoirgneamh ar Luan Cásca 1916?', None, 'Bratach na hÉireann'),
         ('Cathain a osclófar an t-ionad staire nua in Ard-Oifig an Phoist?', '1916 | 1929 | 2016', '2016')]),
 '3C': (11,
        'poem',
        [('Cén séasúr gruama atá thart anois?',
          'An tEarrach | An Geimhreadh | Séasúr an dóchais',
          'An Geimhreadh'),
         ('Cad a bhíonn ar siúl ag na héin?', 'Ag éirí | Ag filleadh | Ag canadh', 'Ag canadh'),
         ('Cad a éiríonn níos luaithe anois?', 'An ghrian | Na ba | Na bláthanna', 'An ghrian'),
         ('Cad a dhéanann na huain? Bíonn siad ...',
          'Ag iníor | Ag rince | Ag pocléimneach',
          'Ag pocléimneach'),
         ('Cad a bhíonn ar gach ní beo?', None, 'Áthas')])}
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
            if slot == '3A' and i == 5:
                card['criteria'][0]['permittedMarks'] = [0,1,3,6]
                card['criteria'][0]['guidance'] += [
                    '6 mharc: Téann sí chuig an bpictiúrlann lena cairde; Téann sí chuig bialann lena cairde; Téann sí chuig an bpictiúrlann nó chuig bialann.',
                    '3 mharc: Téann sí chuig an bpictiúrlann; Téann sí chuig bialann.',
                    '1 mharc: Pictiúrlann; Bialann. Téann sí lena cairde = 0.']
            if slot == '3B' and i == 4:
                card['criteria'][0]['permittedMarks'] = [0,3,6]
                card['criteria'][0]['guidance'] += [
                    '6 mharc: Cuireadh Bratach na hÉireann in airde ar an bhfoirgneamh.',
                    '3 mharc: Bratach.']
            if slot == '3C' and i == 5:
                card['criteria'][0]['permittedMarks'] = [0,2,4,6]
                card['criteria'][0]['guidance'] += [
                    '6 mharc: Áthas arís ar gach ní beo; Véarsa3 líne3 agus líne4 le chéile.',
                    '4 mharc: Véarsa3 líne2 agus líne3 le chéile.',
                    '2 mharc: Dóchas; Véarsa3 líne1, líne2 agus líne3 le chéile.']
            reading_cards[slot].append(card)

    def combine(key,ref,members,pool_quote):
        criteria=[]
        for member in members:
            prefix=member['atlasQuestionId'].lower()+'-'
            for old in member['criteria']:
                c=copy.deepcopy(old)
                c['id']=prefix+c['id']
                c['label']=member['questionRef'].replace('2015 FL ','')+' · '+c['label']
                if 'deductFrom' in c: c['deductFrom']=prefix+c['deductFrom']
                criteria.append(c)
        topics=list(dict.fromkeys(t for c in members for t in [c['topicId'],*c.get('additionalTopicIds',[])]))
        result=add(key,members[0]['section'],ref,
            pool_quote+'\n\nAn rogha don chárta seo: '+ref+'\n\n'+
            '\n\n'.join(c['questionRef'].replace('2015 FL ','')+'\n'+c['questionText'] for c in members),
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

    def language(marks):
        return criterion('gaeilge','Cruinneas Gaeilge',marks,[
            'Dul na Gaeilge: struchtúr na Gaeilge agus cruinneas gramadaí. Foclóir: cruinneas foclóra. Litriú: cé go mbeadh sé seo san áireamh moltar gan iomarca béime a chur ar an ngné seo ag an leibhéal seo.',
            f'Bronn marc as {marks} ar chaighdeán na Gaeilge san iarracht iomlán.',
            'PDF page15 describes the modified marking scheme and its four-mark language score scaled to10 or13. Do not apply that conversion to the standard rubric.'])
    def scheme_guidance(start,end):
        return [clean(re.sub(r'\n\s*\d+\s*$', '', scheme_page_text(scheme[p-1]))) for p in range(start,end+1)]
    notice_p9 = scheme_guidance(9,9)[0]
    notice_p10 = scheme_guidance(10,10)[0]
    notice = add('W-4A','3','Scríobh · Ceist 4(a)',
        'Féach ar na pictiúir thíos.\n\nScríobh amach an FÓGRA a bhaineann leis an rud atá i gceist thuas.\n\n'+
        'Cén rud a bheidh ar siúl? Cén áit a mbeidh sé?\nCén lá? Dáta? Am? Cead isteach?\nCén t-aoi speisialta?\nCá rachaidh an t-airgead?',
        'irish-9-3',['notice'],[14],[8,9,10],[
            criterion('leagan','Leagan Amach',1,['Iarracht ar fhógra.']),
            criterion('pictiur1','Pictiúr 1',8,[notice_p9.split('Pictiúr 1',1)[1].split('Pictiúr 2',1)[0]]),
            criterion('pictiur2','Pictiúr 2',13,[notice_p9.split('Pictiúr 2',1)[1],notice_p10.split('Pictiúr 3',1)[0]]),
            criterion('pictiur3','Pictiúr 3',4,[notice_p10.split('Pictiúr 3',1)[1].split('Pictiúr 4',1)[0]]),
            criterion('pictiur4','Pictiúr 4',4,[notice_p10.split('Pictiúr 4',1)[1].split('Cuir tic',1)[0]]),language(10)],
        ['Scríobh fógra bunaithe ar na ceithre phictiúr agus ar na treoracha.'],
        'Award the published picture submarks and one shared ten-mark language award. Follow the exact 2015 activity/place partial credit, date, fee and guest-name and Simon charity rules within the affected picture awards. Required headings are not choices.')
    letter = add('W-4B','3','Scríobh · Ceist 4(b) · Litir',
        'Féach ar na pictiúir thíos.\n\nTá tú ag obair san aerfort an samhradh seo. Scríobh litir abhaile chuig do chara ag insint dó / di:\n\n'
        '- Faoin aerfort (pointe amháin eolais) — Pictiúr 1\n'
        '- Faoi na daoine a fheiceann tú san aerfort (dhá phointe eolais) — Pictiúr 2\n'
        '- Faoin obair a dhéanann tú san aerfort (trí phointe eolais) — Pictiúr 3\n'
        '- Faoi na rudaí a dhéanann tú nuair a bhíonn lá saor agat (dhá phointe eolais) — Pictiúr 4\n\n'
        'N.B. Bíodh an leagan amach cuí ar do litir: seoladh, dáta, tús agus críoch oiriúnach.',
        'irish-9-3',['letterWriting'],[15],[11,12],[
            criterion('seoladh','Seoladh',2,['Dhá chuid, 1+1, as Gaeilge. Glac le “Bóthar Crumlin” nó “Sráid Patrick”; ná glac le hainm an bhaile i mBéarla.']),
            criterion('data','Dáta',1,['Glac le figiúirí.']),
            criterion('beannu','Beannú',1,['Ainm ar bith, fiú a chara.']),
            criterion('crioch','Críoch / Slán',2,['Dhá chuid ag teastáil: Slán ... agus ainm.']),
            *[criterion(f'pictiur{i}',f'Pictiúr {i}',marks,[
                scheme_guidance(12,12)[0].split(f'Pictiúr {i}',1)[1].split(f'Pictiúr {i+1}' if i<4 else 'Cruinneas Gaeilge',1)[0]
            ]) for i,marks in [(1,3),(2,6),(3,9),(4,6)]],
            language(10)],
        ['Scríobh litir chuig do chara faoi do phost samhraidh san aerfort.',
         'Luaigh 1/2/3/2 pointe faoi na ceithre phictiúr; seoladh, dáta, tús agus críoch oiriúnach.'],
        'One whole40-mark letter: layout6 (2+1+1+2), picture content24 (3+6+9+6), sharedlanguage10. One friend is an open recipient; dó/dí is flexible pronoun wording, not separate prescribed task prompts. The required1/2/3/2 details have non-exhaustive examples, not finite selection menus. No length penalty is printed.',
        additionalTopicIds=['irish-2-8'])
    stories=[]
    for slot,page,end in [('5A',16,13),('5B',17,14)]:
        prompt = (
            'Féach ar an bpictiúr thíos.\n\nBhí tú ag Cluiche Mór i bPáirc an Chrócaigh an samhradh seo caite.\nTá tú chun cuntas (timpeall 90 focal) a scríobh in Iris na Scoile faoin gcluiche mór sin.\n\nScríobh an cuntas sin (timpeall 90 focal) sa spás atá faoin bpictiúr.\n\nCluiche Mór'
            if slot == '5A' else
            'Féach ar na pictiúir anseo thíos.\n\nTharla an eachtra seo agus tú ag dul go dtí an amharclann le do chara.\nTá tú chun scríobh faoin eachtra seo in Iris na Scoile (timpeall 90 focal).\n\nScríobh faoin eachtra (timpeall 90 focal) sa spás atá faoi na pictiúir.\n\nEACHTRA A THARLA'
        )
        # The scheme reduces the awarded whole-response mark proportionally for
        # insufficient length. One final score keeps that adjustment confined to
        # this story in paired routes, while preserving both 37/13 rubric parts.
        stories.append(add('W-'+slot,'3','Scríobh · Ceist '+slot[0]+'('+slot[1].lower()+')',
            prompt,'irish-9-4',['pictures','story'],[page],list(range(13 if slot=='5A' else 14,end+1)),[
                criterion('freagra','Freagra iomlán · Cumarsáid 37 + Gaeilge 13',50,[
                    'Cumas Cumarsáide = 37 marc; Cruinneas Gaeilge = 13 mharc. Mark both parts, then enter the final whole-response mark after any published proportional length adjustment.',
                    *scheme_guidance(13 if slot=='5A' else 14,end),
                    *language(13)['guidance'],
                    'If too short, subtract the appropriate percentage of the awarded mark: the SEC example is 45 words → mark the attempt, then deduct 50% of the awarded mark. Apply this only to this story. No later-year fixed length table is printed.'
                ])],
            ['Scríobh timpeall 90 focal in Iris na Scoile.','Tabhair cúig thagairt ar a laghad don ócáid sna pictiúir.'],
            'First assess communication /37 and language /13. Reduce the communication ceiling by five per missing reference; for 5(b), cover each of the four pictures plus a fifth detail. The final story score includes the scheme’s proportional short-length reduction (45 words: halve the awarded mark). Enter that final mark out of 50. References are indicative, not a closed pool.'))
    # Q4 and Q5 are both compulsory, with one of A/B in each: four products.
    for first,second in itertools.product([notice,letter],stories):
        combine(first['atlasQuestionId']+'-'+second['atlasQuestionId'].removeprefix('W-'),
            first['questionRef'].replace('2015 FL ','')+' + '+second['questionRef'].replace('2015 FL ',''),
            [first,second], 'FREAGAIR GACH CEIST (4 AGUS 5). Ceist 4: Freagair (a) NÓ (b). Ceist 5: Freagair (a) NÓ (b).')
    # Classify exact raw directive lines across all twenty paper pages. Unknown
    # additions on an already-reviewed page and stale keys both fail generation.
    decisions = selection_decisions(paper)
    assert len(cards)==68 and len({c['id'] for c in cards})==68
    assert sum(c['totalMarks'] for c in cards if c['atlasQuestionId'].startswith('A-'))==120
    review=dict(year=2015,level='foundation',paperFileid=FILE+'.pdf',
        paperSha256=hashlib.sha256(paper_path.read_bytes()).hexdigest(),
        schemeSha256=hashlib.sha256(scheme_path.read_bytes()).hexdigest(),
        reviewedPaperPages=list(range(1,21)),reviewedSchemePages=list(range(1,25)),
        reviewDate='2026-10-07',status='reviewed',selectionDecisions=decisions,
        fullPaperAndApplicableSchemeVisualSweep=True,
        atomicPracticeCardIds=[c['id'] for c in cards if 'memberCardIds' not in c],
        pairedRouteCardIds=[c['id'] for c in cards if 'memberCardIds' in c],
        examStructure=dict(listening=120,matching=40,readingQ2=50,readingQ3=60,writingQ4=40,writingQ5=50,writing=90,total=360),
        nonPoolDecisions=[
            'MCQ distractors and map boxes are answers to one task, not independently valid task routes.',
            'All notice headings and letter points are compulsory. One open friend with dó/dí is flexible pronoun wording, not a finite recipient pool; the letter retains one shared language award.',
            'The required1/2/3/2 letter details and source-retrieval answers are open content, not enumerated task prompts.',
            'The five story references are a communication criterion, with non-exhaustive examples, not a printed choose-five menu.',
            'The modified marking scheme changes assessment for eligible candidates, not the printed task or answer route.',
        ],
        openIssues=[],
        audio=json.loads(SOURCE_REVIEW.read_text())['audio'],
        boundaries='14 listening parts; 10 matching parts; 30 reading parts; 4 whole writing tasks; 6 paired reading routes; 4 writing products (one Q4 and one Q5).',
        caveats=json.loads(SOURCE_REVIEW.read_text())['sourceFindings'])
    return withdraw_combinations(dict(review=review,cards=cards)),scheme

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check',action='store_true')
    args=parser.parse_args()
    data,scheme=build()
    content=json.dumps(data,ensure_ascii=False,indent=2)+'\n'
    scheme_text='# Gaeilge Bonnleibhéal 2015 — SEC marking scheme\n\n'+'\n\n'.join(f'## PDF page {i+1}\n\n'+scheme_page_text(p) for i,p in enumerate(scheme))
    scheme_text = '\n'.join(line.rstrip() for line in scheme_text.splitlines()).rstrip()+'\n'
    outputs={OUT:content,ROOT/'examiner-reports/irish/schemes/2015-fl.md':scheme_text}
    for path,value in outputs.items():
        if args.check:
            assert path.exists() and path.read_text()==value, f'Stale Foundation output: {path}'
        else: path.write_text(value)
    print(f"Irish Foundation 2015: {len(data['cards'])} reviewed task/selection cards; archive remains incomplete.")

if __name__=='__main__': main()
