#!/usr/bin/env python3
"""Reviewed Foundation tasks. Counts are assertions, not corpus-completeness proof.

2016 paper pages 1–20 and scheme pages 1–24 visually reviewed on 2026-10-07.
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
OUT = ROOT / 'components/MarkBank/cards/irish/foundation-2016-authored.json'

def clean(text):
    return re.sub(r'\s+', ' ', text).strip()

def criterion(id, label, marks, guidance, exact=False, deduct_from=None):
    return dict(id=id, label=label, kind='deduction' if deduct_from else 'award',
                maxMarks=marks, permittedMarks=[0, marks] if exact else list(range(marks+1)),
                guidanceKind='exact-answer' if exact else 'quality', guidance=guidance,
                **({'deductFrom': deduct_from} if deduct_from else {}))

DIRECTIVE = re.compile(r'rogha|roghna|Freagair|Cuir tic|Ainmnigh|Luaigh|\bchoose\b|\beither\b|\bany\b|one of|\bnó\b|dhá phointe|dhá rud|dheartháir|dheirfiúr', re.I)
SOURCE_REVIEW = ROOT / 'scripts/markbank/authored/irish-foundation-2016-source-review.json'

def scheme_page_text(page):
    # This PDF encodes its printed bullet/arrow as private Symbol-font glyphs.
    return page.get_text().translate({0xf0b7: '•', 0xf0ae: '→', 0xf0b8: '÷'})

def selection_decisions(paper):
    decisions = json.loads(SOURCE_REVIEW.read_text())['selectionDecisions']
    expected = {(d['page'],d['raw']) for d in decisions}
    found = {(i,clean(line)) for i,page in enumerate(paper,1) for line in page.get_text().splitlines() if DIRECTIVE.search(clean(line))}
    assert found == expected, ('Unclassified/stale selection directives', found-expected, expected-found)
    return decisions

def build():
    import fitz
    paper_path = ROOT / f'paper-trail-corpus/exampapers/2016/{FILE}.pdf'
    scheme_path = ROOT / f'paper-trail-corpus/markingschemes/2016/{FILE}.pdf'
    assert hashlib.sha256(paper_path.read_bytes()).hexdigest() == '0feb093c8508dd1980c8e429e799a42030bcb26d5dcc944b12f75af8471c5959', 'Paper changed: repeat visual review'
    assert hashlib.sha256(scheme_path.read_bytes()).hexdigest() == '332068de14a914528ebe5e8677cc92ded7b538a90f8b70190b23e39c008fe060', 'Scheme changed: repeat visual review'
    paper = fitz.open(paper_path)
    scheme = fitz.open(scheme_path)
    texts = [clean(p.get_text()) for p in paper]
    cards = []
    def add(key, section, ref, prompt, topic, exam_topics, pages, scheme_pages, criteria,
            requirements=None, note=None, **extra):
        marks = sum(c['maxMarks'] for c in criteria if c['kind'] == 'award')
        card = dict(id=f'irish-2016-fl-{key.lower()}', year=2016, level='foundation',
            paper=1, section=section, atlasQuestionId=key,
            questionRef=f'2016 FL {ref}', questionText=prompt, totalMarks=marks,
            topicId=topic, examTopicKeys=exam_topics, conceptId=f'irish-foundation-{key.lower()}',
            paperFileid=FILE, schemePage=scheme_pages[0], schemePages=scheme_pages,
            taskRequirements=requirements or [], criteria=criteria,
            markingGuideNote=note or 'Use the answer and tariff published by the SEC for this part.',
            sourceMaterial=dict(kind='source-text', label=ref,
                title=f'Gaeilge Bonnleibhéal 2016 · {ref}', pages=pages,
                attribution='© State Examinations Commission.',
                presentationNote='Original examination pages, including every required picture or passage.'),
            **extra)
        cards.append(card)
        return card

    # Multiple-choice distractors are possible answers to ONE task, not alternative
    # tasks; expanding them would teach knowingly wrong responses as valid routes.
    aural = [('1a', 2, 7, 'Cén post atá ag Ciara faoi láthair?', None, 'Craoltóir Raidió = an tríú pictiúr'),
 ('1b',
  2,
  7,
  'Cad a chaitheann Ciara nuair a bhíonn sí sa stiúideo raidió?',
  'Gúna faiseanta | T-léine agus jíons | Spéaclaí gréine',
  'T-léine agus jíons'),
 ('2a', 2, 7, 'Cén obair atá ar siúl ag Diarmaid anois?', None, 'Iascaire trálaera = an ceathrú pictiúr'),
 ('2b',
  2,
  7,
  'Cad a fhaigheann Diarmaid nuair a bhíonn an aimsir go dona?',
  'Airgead maith | Trálaer nua | Sos breá',
  'Sos breá'),
 ('3', 3, 8, 'Cá bhfuil an bhean ag dul?', None, 'Siopa seodóra = an chéad phictiúr'),
 ('4',
  3,
  8,
  'Cá bhfuil stáisiún na ngardaí? (Cuir tic (✓) sa bhosca ceart.)',
  None,
  'An bosca ag an mbarr ar chlé (tic nó saighead sa bhosca)'),
 ('5a', 3, 8, 'Conas a bhí an aimsir i bPort Mearnóg Dé Sathairn?', None, 'Grianmhar, te = an dara pictiúr'),
 ('5b',
  3,
  8,
  'Cé a thit i laige de bharr an teasa?',
  'Beirt chailíní | Buachaill óg | Seanbhean',
  'Seanbhean'),
 ('6a',
  4,
  10,
  'Cén áit a mbeidh Nuala ag obair sa samhradh?',
  'I siopa leabhar | I mbialann | Ar fheirm',
  'I siopa leabhar'),
 ('6b',
  4,
  10,
  'Cén t-am a thosóidh Pól ag obair gach oíche?',
  'A trí a chlog | A sé a chlog | A deich a chlog',
  'A deich a chlog'),
 ('7a',
  4,
  10,
  'Cén lá a bheidh an glantachán mór ar siúl sa sráidbhaile?',
  'Déardaoin | Dé Sathairn | Dé Domhnaigh',
  'Dé Sathairn'),
 ('7b',
  4,
  10,
  'Cén obair a dhéanfaidh Liam?',
  'Péinteáil | Bláthanna a chur | Bruscar a bhailiú',
  'Péinteáil'),
 ('8a',
  4,
  10,
  'Cén fáth a bhfuil Barra ag dul go dtí an t-ionad sláinte?',
  'Tá sé breoite | Chun oideas a bhailiú | Chun bille a íoc',
  'Chun bille a íoc'),
 ('8b',
  4,
  10,
  'Cén áit a raibh an sparán an t-am ar fad?',
  'Sa charr | Ar an mbord | Sa seomra feithimh',
  'Ar an mbord')]
    audio_url = 'https://www.examinations.ie/archive/exampapers/2016/LC001BLP017IV.mp3'
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
                title='Gaeilge Bonnleibhéal 2016 · An Chluastuiscint',playbackUrl=audio_url,
                secFileid='LC001BLP017IV.mp3',canonicalUrl=audio_url,
                attribution='© State Examinations Commission.',
                presentationNote='Official Foundation Level recording. Answer the question shown using its printed options.'))


    signs = ['Bealach siúlóide amháin\nCosc ar Rothaíocht',
 'Ranganna Gaeilge\nDé Luain 8 – 9.30 p.m.\nGael Linn',
 'Na Cluichí Oilimpeacha\n5-21 Lúnasa\nRio de Janeiro',
 'Tiomáin go mall\nBóthar faoi leac oighir',
 'Ardaitheoir\nSpás do cheathrar\nar a mhéad',
 'Stáisiún Dóiteáin\nNá páirceáil anseo\nin am ar bith',
 '“Picnic Leictreach 2016”\nCeol den scoth\nCeannaigh do thicéad ar líne',
 'Campa Camógaíochta\ndo chailíní 13-15\nGach eolas ó 083 541778',
 'Turas Tíreolaíochta\ngo sléibhte Mhaigh Eo\nBus ón scoil ar 8.00 a.m.',
 'Fadhb Leictreachais?\nLeictreoir cáilithe ar fáil\nAindí – 092 34456']
    for i,(sign,answer) in enumerate(zip(signs,'CHEGJIABFD'),1):
        add(f'R-1-{i}','2',f'Léamhthuiscint · Ceist 1({i})',
            'Meaitseáil na pictiúir leis na fógraí/comharthaí agus scríobh síos an litir cheart sa bhosca in aice leis an uimhir cheart atá sa ghreille.\n\n'+f'{i}. {sign}',
            'irish-9-1',['match'],[5],[4],
            [criterion('answer','Litir cheart',4,[answer,
                'Glactar le córas eile (uimhir an phictiúir in ionad litir an phictiúir) má tá sé soiléir / intuigthe.'],True)])

    # Each row: verbatim question, printed alternatives (or none), official answer.
    reading = {'2A': (6,
        'letterReading',
        [('Cathain a sheol Aisling an CV isteach?', '29 Feabhra | 10 Márta | 21 Márta', '29 Feabhra'),
         ('Cén grád a fuair Aisling sa Fhraincis san Ardteistiméireacht?',
          'Grád A | Grád B | Grád C',
          'Grád B'),
         ('Cén caitheamh aimsire atá ag Aisling?', 'Ríomhairí | Peil | Teangacha', 'Peil'),
         ('Cad atá le líonadh ag Aisling anois?', 'Ríomhphost | Litir | Foirm iarratais', 'Foirm iarratais'),
         ('Cén post atá ag Gráinne Ní Ghallchóir?', 'Stiúrthóir | Cúntóir | Turasóir', 'Stiúrthóir')]),
 '2B': (7,
        'brochure',
        [('Cá bhfuil Cúil Aodha suite?', 'Ar oileán | Cois trá | I measc na gcnoc', 'I measc na gcnoc'),
         ('Cad é an baile is gaire do Chúil Aodha?',
          'Baile Bhuirne | Corcaigh | Maigh Chromtha',
          'Baile Bhuirne'),
         ('Cá bhfuil na muilte gaoithe sa cheantar seo?',
          'Sa ghleann | Ar bharr na gcnoc | Sa sráidbhaile',
          'Ar bharr na gcnoc'),
         ('Cad a bhunaigh Seán Ó Riada sa cheantar seo?',
          'Cór Chúil Aodha | Séipéal Chúil Aodha | Ionad cultúrtha',
          'Cór Chúil Aodha'),
         ('Cad atá beo láidir i gCúil Aodha?',
          'Rac-cheol | Popcheol | Amhránaíocht ar an sean-nós',
          'Amhránaíocht ar an sean-nós')]),
 '2C': (8,
        'news',
        [('Cén mhí inar tharla an stoirm mhór seo?',
          'Mí Feabhra | Mí an Mhárta | Mí na Samhna',
          'Mí an Mhárta'),
         ('Cé a thuig gur féidir le stoirm mhór a lán damáiste a dhéanamh?',
          'Na déagóirí | Na tuismitheoirí | Na páistí óga',
          'Na tuismitheoirí'),
         ('Cén áit inar bhailigh an teaghlach ar fad le chéile?',
          'Sa chistin | Thuas staighre | Sa seomra suí',
          'Sa seomra suí'),
         ('Cad a rinne siad le linn na stoirme?',
          'D’imir siad cártaí | Bhí siad ag caint | Chodail siad',
          'D’imir siad cártaí'),
         ('Cad a bhí bunoscionn sa ghairdín?',
          'An bothán adhmaid | Crann | Fuinneoga',
          'An bothán adhmaid')]),
 '3A': (9,
        'news',
        [('Cé hé “Rí na hIománaíochta” sa lá atá inniu ann?',
          'Henry Shefflin | Christy Ring | Setanta',
          'Henry Shefflin'),
         ('Cathain a bhuaigh Henry a chéad bhonn sinsearach?', '1979 | 1999 | 2000', '2000'),
         ('Cé mhéad uair a bhuaigh Henry Craobh na hÉireann?',
          'Trí huaire | Seacht n-uaire | Deich n-uaire',
          'Deich n-uaire'),
         ('Cén gortú a tharla do Henry agus é ag imirt dá chlub i mí na Nollag 2012?',
          None,
          'Bhris sé cnámh ina chos chlé'),
         ('Cá mbíonn Henry le feiceáil anois?',
          'Ar pháirc na himeartha | Ar theilifís RTÉ | San ospidéal',
          'Ar theilifís RTÉ')]),
 '3B': (10,
        'extract',
        [('Cá bhfuil cónaí ar Úna faoi láthair?', 'Baile Átha Cliath | Durlas | Northampton', 'Northampton'),
         ('Cén caitheamh aimsire a bhí ag Úna nuair a bhí sí sa bhunscoil?',
          'An giotár | Snámh | Canadh',
          'Snámh'),
         ('Cén tslí bheatha a roghnaigh Úna sa bhliain 2005?',
          'Banaltra | Ceoltóir | Múinteoir bunscoile',
          'Ceoltóir'),
         ('Cén fáth ar imigh Úna go Londain sa bhliain 2007?',
          None,
          'Chun clú agus cáil a bhaint amach mar amhránaí'),
         ('Cén sloinne atá ar Úna anois?', 'Egan | Foden | Healy', 'Foden')]),
 '3C': (11,
        'poem',
        [('Cén t-ainmhí atá ag caint sna véarsaí seo?', 'Cat | Mac tíre | Sionnach', 'Sionnach'),
         ('Cén áit a mbíonn Sionnach na Cathrach ag lorg bia?',
          'I lár na cathrach | Faoi sceach | Sa zú',
          'I lár na cathrach'),
         ('Cad a fhaigheann Sionnach na Cathrach a shásaíonn a chroí?', None, 'Bia blasta'),
         ('Cén bia nach n-itheann Sionnach na Cathrach?', 'Bia dóite | Sicín | Uachtar reoite', 'Bia dóite'),
         ('Cathain a chodlaíonn Sionnach na Cathrach?',
          'I rith na hoíche | I rith an lae | Le héirí na gréine',
          'I rith an lae')])}
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
                assert comparable(accepted) in comparable(scheme[4 if slot[0]=='2' else (6 if slot=='3C' else 5)].get_text()), (slot,i,accepted)
            card = add(f'R-{slot}-{i}','2',f'Léamhthuiscint · Ceist {slot[0]}({slot[1].lower()})({i})',
                f'Léigh an téacs ar leathanach {page}.\n\n{i}. '+prompt+
                ('\n\n'+options.replace(' | ','\n') if options else ''),
                'irish-9-2',[exam_topic],[page],[5 if slot[0]=='2' else (7 if slot=='3C' else 6)],
                [criterion('answer','Freagra',5 if slot[0]=='2' else 6,[answer],True)])
            if slot == '3A' and i == 4:
                card['criteria'][0]['permittedMarks'] = [0,2,3,4,5,6]
                card['criteria'][0]['guidance'] += [
                    '6 mharc: Bhris sé a chos chlé; Bhris sé a chos chlé, mar shampla, nuair a bhí sé ag imirt dá chlub i mí na Nollag 2012; Tharla gortú dó cúpla uair... i mí na Nollag 2012 (dhá abairt le chéile).',
                    '5 mharc: Bhris sé cnámh ina chos; Ghortaigh sé cnámh ina chos chlé.',
                    '4 mharc: Bhris sé a chos; Ghortaigh sé a chos chlé.',
                    '3 mharc: Bhris sé cnámh; Ghortaigh sé a chos.',
                    '2 mharc: An t-alt ar fad: “Bronnadh ... 2012”.']
            if slot == '3B' and i == 4:
                card['criteria'][0]['permittedMarks'] = [0,2,3,6]
                card['criteria'][0]['guidance'] += [
                    '6 mharc: Chun clú a bhaint amach mar amhránaí; Chun cáil a bhaint amach mar amhránaí; Sa bhliain 2007...mar amhránaí; Bhí sí míshásta...mar amhránaí (dhá abairt).',
                    '3 mharc: Chun clú (nó cáil) a bhaint amach.',
                    '2 mharc: Mar amhránaí. “Amhránaí” leis féin = 0.']
            if slot == '3C' and i == 3:
                card['criteria'][0]['permittedMarks'] = [0,4,6]
                card['criteria'][0]['guidance'] += [
                    '6 mharc: Faighim bia blasta a shásaíonn mo chroí; Sceallóga nó sicín nó fiú uachtar reoite; dhá chineál bia ó Véarsa2 líne3 (sceallóga nó sicín; sicín nó fiú uachtar reoite; sceallóga nó fiú uachtar reoite).',
                    '6 mharc: Véarsa2 línte1 agus2; línte1,2 agus3; línte3 agus4.',
                    '4 mharc: Véarsa3 ar fad mar fhreagra.']
            reading_cards[slot].append(card)

    def combine(key,ref,members,pool_quote):
        criteria=[]
        for member in members:
            prefix=member['atlasQuestionId'].lower()+'-'
            for old in member['criteria']:
                c=copy.deepcopy(old)
                c['id']=prefix+c['id']
                c['label']=member['questionRef'].replace('2016 FL ','')+' · '+c['label']
                if 'deductFrom' in c: c['deductFrom']=prefix+c['deductFrom']
                criteria.append(c)
        topics=list(dict.fromkeys(t for c in members for t in [c['topicId'],*c.get('additionalTopicIds',[])]))
        result=add(key,members[0]['section'],ref,
            pool_quote+'\n\nAn rogha don chárta seo: '+ref+'\n\n'+
            '\n\n'.join(c['questionRef'].replace('2016 FL ','')+'\n'+c['questionText'] for c in members),
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
            'Dul na Gaeilge: struchtúr na Gaeilge agus beachtas gramadaí. Foclóir: cruinneas agus oiriúnacht foclóra. Litriú.',
            f'Bronn marc as {marks} ar chaighdeán na Gaeilge san iarracht iomlán.',
            'The band table on PDF page17 belongs only to the modified marking scheme. Do not apply it as the standard language rubric.'])
    def scheme_guidance(start,end):
        return [clean(re.sub(r'ATBL 2016\s*Lch \d+', '', scheme_page_text(scheme[p-1]))) for p in range(start,end+1)]
    notice_p10 = scheme_guidance(10,10)[0]
    notice_p11 = scheme_guidance(11,11)[0]
    notice = add('W-4A','3','Scríobh · Ceist 4(a)',
        'Féach ar na pictiúir thíos.\n\nScríobh amach an FÓGRA a bhaineann leis an rud atá i gceist thuas.\n\n'+
        'Cén rud a bheidh ar siúl? Cén áit a mbeidh sí?\nCén lá? Dáta? Am? Cead isteach?\nCén t-aoi speisialta?\nCá rachaidh an t-airgead?',
        'irish-9-3',['notice'],[14],[9,10,11],[
            criterion('leagan','Leagan Amach',1,['Iarracht ar fhógra.']),
            criterion('pictiur1','Pictiúr 1',8,[notice_p10.split('Pictiúr 1',1)[1].split('Pictiúr 2',1)[0]]),
            criterion('pictiur2','Pictiúr 2',13,[notice_p10.split('Pictiúr 2',1)[1],notice_p11.split('Pictiúr 3',1)[0]]),
            criterion('pictiur3','Pictiúr 3',4,[notice_p11.split('Pictiúr 3',1)[1].split('Pictiúr 4',1)[0]]),
            criterion('pictiur4','Pictiúr 4',4,[notice_p11.split('Pictiúr 4',1)[1].split('Cuir tic',1)[0]]),language(10)],
        ['Scríobh fógra bunaithe ar na ceithre phictiúr agus ar na treoracha.'],
        'Award the published picture submarks and one shared ten-mark language award. Follow the exact 2016 activity/place partial credit, date, fee, Paul O’Connell and Peataí ar Strae rules within the affected picture awards. Required headings are not choices.')
    form_prompt = (
        'Ba mhaith leat a bheith ag obair an samhradh seo i gCumann Gailf na Cille, An Cabhán.\n\n'
        'Líon isteach An Fhoirm Iarratais atá anseo thíos. [Nóta: Is tusa Tadhg de Brún.]\n\n'
        'Cumann Gailf na Cille, An Cabhán\nFoirm Iarratais do Phost Samhraidh\n\n'
        'Ainm: Tadhg de Brún\nUimhir theileafóin:\nSeoladh:\nAois:\nDáta Breithe:\n'
        'Cén Scrúdú Teistiméireachta atá déanta agat?\nAinmnigh cúig ábhar scoile a rinne tú sa scrúdú sin:\n'
        'Luaigh trí chaitheamh aimsire atá agat:\nAn imríonn tú galf?\n'
        'An mbeidh tú sásta a bheith ag obair gach deireadh seachtaine?\nAn féidir leat tarracóir a thiomáint?\n'
        'Cén post ba mhaith leat? Cuir tic le ceann amháin (✓): Glantóir / Garraíodóir / Freastalaí\n\n'
        'Scríobh alt gearr (timpeall 40 focal) ag insint cén fáth ar mhaith leat post samhraidh sa chumann gailf seo.\n\n'
        'Síniú: Tadhg de Brún\nDáta:'
    )
    jobs=[('glantoir','Glantóir'),('garraiodoir','Garraíodóir'),('freastalai','Freastalaí')]
    for _,job in jobs:
        assert job in texts[14], 'Printed job changed: repeat selection review'
    fields_guide = [
        'Na Ceisteanna = 15 mharc. Úsáid an colún dúbailte: uimhir theileafóin2; seoladh4; aois2; dáta breithe2; scrúdú2; cúig ábhar10; trí chaitheamh aimsire3; galf1; obair gach deireadh seachtaine1; tarracóir1; post1; dáta ag bun1. Iomlán30 ÷ 2 = 15.',
        'Round up once after adding the doubled question awards and dividing by two: 21 ÷ 2 = 10½ → 11. Do not round each half-mark field separately.',
        scheme_guidance(12,12)[0].split('An Córas Marcála',1)[1],
        scheme_guidance(13,13)[0].split('An t-Alt',1)[0],
    ]
    forms=[]
    for key,job in jobs:
        forms.append(add(f'W-4B-{key}','3',f'Scríobh · Ceist 4(b) · {job}',
            form_prompt+f'\n\nAn rogha don chárta seo: {job}.',
            'irish-9-0',['form'],[15],[12,13],[
                criterion('fields','Na Ceisteanna · iomlán slán',15,fields_guide),
                criterion('paragraph','An t-Alt · marc tar éis coigeartú faid',15,[
                    scheme_guidance(13,13)[0].split('An t-Alt',1)[1].split('Cruinneas Gaeilge',1)[0],
                    'Mark the relevant paragraph out of15. Without reference to golf-club work/job, ceiling8; off-topic ceiling5. Then apply the published proportional short-length reduction to this paragraph award only. Example: 30 of40 words → deduct25% of the awarded paragraph mark. Enter that final paragraph score; keep the form-answer and shared-language scores separate.'
                ]), language(10)],
            ['Líon gach réimse riachtanach; cúig ábhar scoile agus trí chaitheamh aimsire.',
             f'Roghnaigh {job} mar phost.',
             'Scríobh timpeall 40 focal faoin bpost sa chumann gailf.'],
            'One whole40-mark form: questions15 (half marks combined then rounded up once), paragraph15 with its own proportional length adjustment and relevance ceilings8/5, shared language10 across questions and paragraph. Three printed job choices are expanded; school subjects, hobbies and personal answers remain open content choices.'))
    stories=[]
    for slot,page,start,end in [('5A',16,14,14),('5B',17,15,16)]:
        prompt = (
            'Féach ar an bpictiúr thíos.\n\nBhí tú ag Cóisir Lá Breithe an tseachtain seo caite.\nTá tú chun cuntas (timpeall 90 focal) a scríobh in Iris na Scoile faoin gcóisir lá breithe sin.\n\nScríobh an cuntas sin (timpeall 90 focal) sa spás atá faoin bpictiúr.\n\nCóisir Lá Breithe'
            if slot == '5A' else
            'Féach ar na pictiúir anseo thíos.\n\nTharla an eachtra seo agus tú ag dul go dtí an stáisiún traenach le do chara.\nTá tú chun scríobh faoin eachtra seo in Iris na Scoile (timpeall 90 focal).\n\nScríobh faoin eachtra (timpeall 90 focal) sa spás atá faoi na pictiúir.\n\nEACHTRA A THARLA'
        )
        # Final awarded-response adjustment must stay within this story when paired.
        stories.append(add('W-'+slot,'3','Scríobh · Ceist '+slot[0]+'('+slot[1].lower()+')',
            prompt,'irish-9-4',['pictures','story'],[page],list(range(start,end+1)),[
                criterion('freagra','Freagra iomlán · Cumarsáid 37 + Gaeilge 13',50,[
                    'Cumas Cumarsáide = 37 marc; Cruinneas Gaeilge = 13 mharc. Mark both parts, then enter the final whole-response mark after any published proportional length adjustment.',
                    *scheme_guidance(start,end),*language(13)['guidance'],
                    'If too short, subtract the appropriate percentage of the awarded mark: the SEC example is 45 words → mark the attempt, then deduct 50% of the awarded mark. Apply this only to this story. No later-year fixed length table is printed.'
                ])],
            ['Scríobh timpeall 90 focal in Iris na Scoile.','Tabhair cúig thagairt ar a laghad don ócáid sna pictiúir.'],
            'First assess communication /37 and language /13. Reduce the communication ceiling by five per missing reference; for 5(b), cover each of the four pictures plus a fifth detail. The final story score includes the scheme’s proportional short-length reduction (45 words: halve the awarded mark). Enter that final mark out of50. References are indicative, not a closed pool.'))
    # One Q4 and one Q5 required; expand all three jobs within the form.
    for first,second in itertools.product([notice,*forms],stories):
        combine(first['atlasQuestionId']+'-'+second['atlasQuestionId'].removeprefix('W-'),
            first['questionRef'].replace('2016 FL ','')+' + '+second['questionRef'].replace('2016 FL ',''),
            [first,second], 'FREAGAIR GACH CEIST (4 AGUS 5). Ceist 4: Freagair (a) NÓ (b). Ceist 5: Freagair (a) NÓ (b).')
    # Classify exact raw directive lines across all twenty paper pages. Unknown
    # additions on an already-reviewed page and stale keys both fail generation.
    decisions = selection_decisions(paper)
    assert len(cards)==74 and len({c['id'] for c in cards})==74
    assert sum(c['totalMarks'] for c in cards if c['atlasQuestionId'].startswith('A-'))==120
    review=dict(year=2016,level='foundation',paperFileid=FILE+'.pdf',
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
            'All notice headings and form fields are compulsory context. The three printed job choices are mechanically expanded; each whole form retains one shared language award.',
            'Five school subjects, three hobbies, personal details and yes/no answers are open content, not finite task-choice menus.',
            'The five story references are a communication criterion, with non-exhaustive examples, not a printed choose-five menu.',
            'The modified marking scheme changes assessment for eligible candidates, not the printed task or answer route.',
        ],
        openIssues=[],
        audio=json.loads(SOURCE_REVIEW.read_text())['audio'],
        boundaries='14 listening parts; 10 matching parts; 30 reading parts; 6 whole writing routes including three jobs; 6 paired reading routes; 8 writing products (one Q4 and one Q5).',
        caveats=json.loads(SOURCE_REVIEW.read_text())['sourceFindings'])
    return withdraw_combinations(dict(review=review,cards=cards)),scheme

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check',action='store_true')
    args=parser.parse_args()
    data,scheme=build()
    content=json.dumps(data,ensure_ascii=False,indent=2)+'\n'
    scheme_text='# Gaeilge Bonnleibhéal 2016 — SEC marking scheme\n\n'+'\n\n'.join(f'## PDF page {i+1}\n\n'+scheme_page_text(p) for i,p in enumerate(scheme))
    scheme_text = '\n'.join(line.rstrip() for line in scheme_text.splitlines()).rstrip()+'\n'
    outputs={OUT:content,ROOT/'examiner-reports/irish/schemes/2016-fl.md':scheme_text}
    for path,value in outputs.items():
        if args.check:
            assert path.exists() and path.read_text()==value, f'Stale Foundation output: {path}'
        else: path.write_text(value)
    print(f"Irish Foundation 2016: {len(data['cards'])} reviewed task/selection cards; archive remains incomplete.")

if __name__=='__main__': main()
