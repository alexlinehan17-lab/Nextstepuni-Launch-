#!/usr/bin/env python3
"""Reviewed Foundation tasks. Counts are assertions, not corpus-completeness proof.

2014 paper pages 1–20 and scheme pages 1–24 visually reviewed on 2026-10-07.
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

ROOT = Path(__file__).resolve().parents[3]
FILE = 'LC001BLP000IV'
OUT = ROOT / 'components/MarkBank/cards/irish/foundation-2014-authored.json'

def clean(text):
    return re.sub(r'\s+', ' ', text).strip()

def criterion(id, label, marks, guidance, exact=False, deduct_from=None):
    return dict(id=id, label=label, kind='deduction' if deduct_from else 'award',
                maxMarks=marks, permittedMarks=[0, marks] if exact else list(range(marks+1)),
                guidanceKind='exact-answer' if exact else 'quality', guidance=guidance,
                **({'deductFrom': deduct_from} if deduct_from else {}))

DIRECTIVE = re.compile(r'rogha|roghna|Freagair|Cuir tic|Ainmnigh|Luaigh|\bchoose\b|\beither\b|\bany\b|one of|\bnó\b|dhá phointe|dhá rud|dheartháir|dheirfiúr', re.I)
SOURCE_REVIEW = ROOT / 'scripts/markbank/authored/irish-foundation-2014-source-review.json'

def scheme_page_text(page):
    # Reviewed missing-ToUnicode mappings: only the named fonts are decoded.
    # The original PDF remains untouched. Unknown glyphs require a new review.
    maps = {
        'Cambria': {3:' ',4:'A',23:'T',5:'B',15:'L',133:'c',138:'h',
                    0x372:'0',0x373:'1',0x374:'2',0x375:'3',0x376:'4',0x377:'5',
                    0x378:'6',0x379:'7',0x37a:'8',0x37b:'9'},
        'Calibri': {3:' '}, 'Calibri-Bold': {3:' '},
        'SymbolMT': {32:' ',111:'→',120:'•',121:'÷'},
        'Wingdings-Regular': {131:'▪'},
    }
    lines=[]
    for block in page.get_text('dict')['blocks']:
        for line in block.get('lines',[]):
            parts=[]
            for span in line['spans']:
                text=span['text']
                if span['font'] in maps:
                    mapping=maps[span['font']]
                    assert all(ord(c) in mapping for c in text), ('Unreviewed scheme glyph',page.number+1,span['font'],repr(text))
                    text=''.join(mapping[ord(c)] for c in text)
                parts.append(text)
            lines.append(''.join(parts))
    text='\n'.join(lines)
    assert not any(ord(c)<32 and c not in '\n\r\t' for c in text), 'Undecoded scheme control character'
    return text

def selection_decisions(paper):
    decisions = json.loads(SOURCE_REVIEW.read_text())['selectionDecisions']
    expected = {(d['page'],d['raw']) for d in decisions}
    found = {(i,clean(line)) for i,page in enumerate(paper,1) for line in page.get_text().splitlines() if DIRECTIVE.search(clean(line))}
    assert found == expected, ('Unclassified/stale selection directives', found-expected, expected-found)
    return decisions

def build():
    import fitz
    paper_path = ROOT / f'paper-trail-corpus/exampapers/2014/{FILE}.pdf'
    scheme_path = ROOT / f'paper-trail-corpus/markingschemes/2014/{FILE}.pdf'
    assert hashlib.sha256(paper_path.read_bytes()).hexdigest() == '309599ea483361084f229f718f6277d66b15e9a6abf6a3fdc6e6aa4df174331c', 'Paper changed: repeat visual review'
    assert hashlib.sha256(scheme_path.read_bytes()).hexdigest() == '71e9686562b416eafe9f5930bfa767911d8dfcafa408d354526dca727c203c55', 'Scheme changed: repeat visual review'
    paper = fitz.open(paper_path)
    scheme = fitz.open(scheme_path)
    texts = [clean(p.get_text()) for p in paper]
    cards = []
    def add(key, section, ref, prompt, topic, exam_topics, pages, scheme_pages, criteria,
            requirements=None, note=None, **extra):
        marks = sum(c['maxMarks'] for c in criteria if c['kind'] == 'award')
        card = dict(id=f'irish-2014-fl-{key.lower()}', year=2014, level='foundation',
            paper=1, section=section, atlasQuestionId=key,
            questionRef=f'2014 FL {ref}', questionText=prompt, totalMarks=marks,
            topicId=topic, examTopicKeys=exam_topics, conceptId=f'irish-foundation-{key.lower()}',
            paperFileid=FILE, schemePage=scheme_pages[0], schemePages=scheme_pages,
            taskRequirements=requirements or [], criteria=criteria,
            markingGuideNote=note or 'Use the answer and tariff published by the SEC for this part.',
            sourceMaterial=dict(kind='source-text', label=ref,
                title=f'Gaeilge Bonnleibhéal 2014 · {ref}', pages=pages,
                attribution='© State Examinations Commission.',
                presentationNote='Original examination pages, including every required picture or passage.'),
            **extra)
        cards.append(card)
        return card

    # Multiple-choice distractors are possible answers to ONE task, not alternative
    # tasks; expanding them would teach knowingly wrong responses as valid routes.
    aural = [('1a', 2, 7, 'Cén post atá ag Deirdre?', None, 'Garda Síochána = an dara pictiúr'),
 ('1b',
  2,
  7,
  'Cá bhfuil Deirdre ag obair faoi láthair?',
  'An Teampall Mór | Ceatharlach | Cill Chainnigh',
  'Cill Chainnigh'),
 ('2a', 2, 7, 'Cén spórt is fearr le Liam?', None, 'Lúthchleasaíocht = an ceathrú pictiúr'),
 ('2b',
  2,
  7,
  'Cad a fuair Liam ó Choláiste na hOllscoile, Baile Átha Cliath?',
  'Airgead | Scoláireacht | Turas thar lear',
  'Scoláireacht'),
 ('3', 3, 8, 'Cá bhfuil an fear ag dul?', None, 'An bhunscoil = an tríú pictiúr'),
 ('4',
  3,
  8,
  'Cá bhfuil Óstán na Páirce? (Cuir tic (✓) sa bhosca ceart.)',
  None,
  'An bosca ag an mbarr ar dheis (tic nó saighead)'),
 ('5a', 3, 8, 'Conas a bheidh an aimsir amárach?', None, 'Fliuch = an chéad phictiúr'),
 ('5b',
  3,
  8,
  'Cathain a bheidh an cluiche mór peile ar siúl?',
  'Maidin amárach | Tráthnóna amárach | Oíche amárach',
  'Tráthnóna amárach'),
 ('6a',
  4,
  10,
  'Cathain a bheidh agallamh ag Barra?',
  'Maidin Dé hAoine | Maidin inniu | Oíche Dé hAoine',
  'Maidin Dé hAoine'),
 ('6b',
  4,
  10,
  'Conas a rachaidh Barra go dtí an t-agallamh?',
  'Ar an mbus | Ar an traein | Sa charr',
  'Sa charr'),
 ('7a',
  4,
  10,
  'Cathain a líon Aoife foirm an CAO?',
  'Inniu | Seachtain ó shin | Trí lá ó shin',
  'Seachtain ó shin'),
 ('7b',
  4,
  10,
  'Cén rogha atá déanta ag Seosamh?',
  'Cúrsa eolaíochta | Cúrsa gnó | Printíseacht mar mheicneoir',
  'Printíseacht mar mheicneoir'),
 ('8a',
  4,
  10,
  'Conas a chaith Cathal an deireadh seachtaine seo caite?',
  'Ag éisteacht le ceol | Ag féachaint ar an teilifís | Ag staidéar',
  'Ag staidéar'),
 ('8b',
  4,
  10,
  'Cá mbeidh Cathal Dé Sathairn seo chugainn?',
  'Ag dioscó | Ag comórtas snámha | Ag ceolchoirm',
  'Ag comórtas snámha')]
    audio_url = 'https://www.examinations.ie/archive/exampapers/2014/LC001BLP017IV.mp3'
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
                title='Gaeilge Bonnleibhéal 2014 · An Chluastuiscint',playbackUrl=audio_url,
                secFileid='LC001BLP017IV.mp3',canonicalUrl=audio_url,
                attribution='© State Examinations Commission.',
                presentationNote='Official Foundation Level recording. Answer the question shown using its printed options.'))


    signs = ['Comórtas Cispheile\nColáiste Eoin v Scoil Mhuire\nInniu 4.30 p.m.',
 'Aire !\nTarracóirí Feirme\nar an mbóthar seo',
 'Oifig Thaistil\nSaoire sa Spáinn\nPraghas Réasúnta',
 'Oíche Cheoil\nAn Ceoláras Náisiúnta\n12 Meitheamh 8.00 p.m.',
 'Seachtain na Gaeilge\nCéilí Mór\nHalla na Scoile',
 'Club Ríomhaireachta\nna Scoile\nGach Déardaoin\nFáilte roimh chách',
 'Stáisiún Heuston\nIonad Tacsaithe',
 'Saotharlann Cheimice\nCaith Spéaclaí Cosanta\nsa seomra seo i gcónaí',
 'Leapacha ar Leathphraghas\nSladmhargadh\nSiopa Troscáin de Búrca',
 'Leabharlann an Chontae\nAr oscailt Luan – Satharn\n10.00 -17.30']
    for i,(sign,answer) in enumerate(zip(signs,'DCIHAGEJFB'),1):
        add(f'R-1-{i}','2',f'Léamhthuiscint · Ceist 1({i})',
            'Meaitseáil na pictiúir leis na fógraí/comharthaí agus scríobh síos an litir cheart sa bhosca in aice leis an uimhir cheart atá sa ghreille.\n\n'+f'{i}. {sign}',
            'irish-9-1',['match'],[5],[4],
            [criterion('answer','Litir cheart',4,[answer,
                'Glactar le córas eile (uimhir an phictiúir in ionad litir an phictiúir) má tá sé soiléir / intuigthe.'],True)])

    # Each row: verbatim question, printed alternatives (or none), official answer.
    reading = {'2A': (6,
        'letterReading',
        [('Cá bhfuil Máirtín ina chónaí?',
          'Co. an Chabháin | Co. Bhaile Átha Cliath | Co. na Mí',
          'Co. An Chabháin'),
         ('Cén grád a fuair Máirtín sa Ghaeilge san Ardteistiméireacht?',
          'Grád A | Grád B | Grád C',
          'Grád C'),
         ('Cén sórt oibre atá ar fáil in Woodies faoi láthair?',
          'Obair lánaimseartha | Obair pháirtaimseartha | Obair shealadach',
          'Obair pháirtaimseartha'),
         ('Cé mhéad a gheobhaidh Máirtín in aghaidh na huaire?', '€5 | €9 | €13', '€9'),
         ('Cén post atá ag Bríd Ní Laoire?', 'Bainisteoir | Feirmeoir | Rúnaí', 'Bainisteoir')]),
 '2B': (7,
        'brochure',
        [('Cén áit a bhfuil Aerfort Dhún na nGall?',
          'Baile Átha Cliath | An Charraig Fhinn | Glaschú',
          'An Charraig Fhinn'),
         ('Cad is féidir a fháil ar cíos ag Aerfort Dhún na nGall?', 'Carr | Eitleán | Bia blasta', 'Carr'),
         ('Cén saghas trá atá díreach in aice leis an aerfort?',
          'Trá charraigeach | Trá bheag | Trá ghainmheach',
          'Trá ghainmheach'),
         ('Cad atá i measc na ngleannta glasa?', 'Machairí gailf | Óstáin | Oileáin', 'Machairí gailf'),
         ('Cad atá cois cósta atá oiriúnach do gach aoisghrúpa?',
          'Surfáil | Siúlóidí breátha | Seoltóireacht',
          'Siúlóidí breátha')]),
 '2C': (8,
        'news',
        [('Cén gaol atá ag Liam agus Pól le chéile?',
          'Cairde | Deartháireacha | Tuismitheoirí',
          'Deartháireacha'),
         ('Cad as ar tháinig an héileacaptar?', 'Trá Lí | Cill Airne | Corcaigh', 'Corcaigh'),
         ('Cén áit a ndeachaigh Liam agus Pól inné?',
          'Go barr an tsléibhe | Ar scoil | Ag snámh',
          'Go barr an tsléibhe'),
         ('Cad a bhris Liam nuair a thit sé?', 'A chos | An fón póca | A lámh', 'A chos'),
         ('Cad a chuala na deartháireacha i lár na hoíche?',
          'An héileacaptar | An fón | An fhoireann tarrthála',
          'An fhoireann tarrthála')]),
 '3A': (9,
        'news',
        [('Cé a fhéachann ar an gclár “Bog Stop” ar TG4?',
          'Páistí bunscoile | Déagóirí | Gach aoisghrúpa',
          'Páistí bunscoile'),
         ('Cár rugadh Máire Treasa?', 'I gContae Shligigh | I Luimneach | Sa Ghaeltacht', 'Sa Ghaeltacht'),
         ('Cén áit a bhfuair Máire Treasa taithí ar an drámaíocht?',
          'Sa bhunscoil | Sa mheánscoil | Sa choláiste',
          'Sa mheánscoil'),
         ('Cén saghas éadaí a chaitheann Máire Treasa?', None, 'Éadaí faiseanta'),
         ('Ar an gclár “Rugbaí Beo” déanann Máire Treasa anailís ...',
          'Ar chúrsaí faisin | Ar stíl imeartha rugbaí | Ar stíleanna gruaige',
          'Ar stíl imeartha rugbaí')]),
 '3B': (10,
        'extract',
        [('Cén áit a bhfuil Cruach Phádraig?',
          'Sa tSeapáin | San Éigipt | I gContae Mhaigh Eo',
          'I gContae Mhaigh Eo'),
         ('Cén fáth a mbailíodh daoine ar Chruach Phádraig fadó, fadó?',
          None,
          '(chun) ( tús) an fhómhair a cheiliúradh'),
         ('Chaith Pádraig daichead lá ag barr an tsléibhe. Bhí sé ...',
          'Ag guí | Ag glaoch amach | Ag sú na gréine',
          'Bhí sé ag guí'),
         ('Cad atá ag barr an tsléibhe anois?',
          'Bróga agus stocaí | Séipéal beag | Ionad cuairteoirí',
          'Séipéal beag'),
         ('Cad atá ag déanamh damáiste do Chruach Phádraig?',
          'Líon na gcuairteoirí | Na cosáin | Sneachta',
          'Líon na gcuairteoirí')]),
 '3C': (11,
        'poem',
        [('Cén aois atá ag Mamó?', '17 | 70 | 77', '70'),
         ('Cad a deir Mamó linn go minic?', None, 'Nach mbeidh sí óg arís'),
         ('Cad a thuigeann Mamó?', 'Facebook | An ríomhaire | An croí istigh', 'An croí istigh'),
         ('Cad a dhéanann Mamó go tuisceanach?', 'Cáineann sí | Léann sí | Éisteann sí', 'Éisteann sí'),
         ('Cad a spreagann Mamó ionainn?', 'Faic | Grá | Raic', 'Grá')])}
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
                card['criteria'][0]['guidance'] += ['6 mharc: faiseanta; Caitheann Máire (Treasa) éadaí faiseanta; Caitheann sí éadaí faiseanta.']
            if slot == '3B' and i == 2:
                card['criteria'][0]['permittedMarks'] = [0,3,6]
                card['criteria'][0]['guidance'] += ['6 mharc: thug na daoine sin ómós don ghrian ó bharr an tsléibhe.', '3 mharc: ceiliúradh (leis féin).']
            if slot == '3C' and i == 2:
                card['criteria'][0]['permittedMarks'] = [0,2,4,6]
                card['criteria'][0]['guidance'] += [
                    '6 mharc: Is deir sí linn go minic / Nach mbeidh sí óg arís (an dá líne).',
                    'Líne bhreise amháin: pionós −2; an véarsa ar fad: pionós −4. Enter the resulting mark for this answer only.']
            reading_cards[slot].append(card)

    def combine(key,ref,members,pool_quote):
        criteria=[]
        for member in members:
            prefix=member['atlasQuestionId'].lower()+'-'
            for old in member['criteria']:
                c=copy.deepcopy(old)
                c['id']=prefix+c['id']
                c['label']=member['questionRef'].replace('2014 FL ','')+' · '+c['label']
                if 'deductFrom' in c: c['deductFrom']=prefix+c['deductFrom']
                criteria.append(c)
        topics=list(dict.fromkeys(t for c in members for t in [c['topicId'],*c.get('additionalTopicIds',[])]))
        result=add(key,members[0]['section'],ref,
            pool_quote+'\n\nAn rogha don chárta seo: '+ref+'\n\n'+
            '\n\n'.join(c['questionRef'].replace('2014 FL ','')+'\n'+c['questionText'] for c in members),
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
            'PDF page17 describes the modified marking scheme and its four-mark language score scaled to10 or13. Do not apply that conversion to the standard rubric.'])
    def scheme_guidance(start,end):
        return [clean(re.sub(r'ATBL(?: 2014)?\s*Lch \d+', '', scheme_page_text(scheme[p-1]))) for p in range(start,end+1)]
    notice_p10 = scheme_guidance(10,10)[0]
    notice_p11 = scheme_guidance(11,11)[0]
    notice = add('W-4A','3','Scríobh · Ceist 4(a)',
        'Féach ar na pictiúir thíos.\n\nScríobh amach an FÓGRA a bhaineann leis an rud atá i gceist thuas.\n\n'+
        'Cén rud a bheidh ar siúl? Cén áit a mbeidh sé?\nCén lá? Dáta? Am? Cead isteach?\nCén t-aoi speisialta?\nCá rachaidh an t-airgead?',
        'irish-9-3',['notice'],[14],[9,10,11,12],[
            criterion('leagan','Leagan Amach',1,['Iarracht ar fhógra.']),
            criterion('pictiur1','Pictiúr 1',8,[notice_p10.split('Pictiúr 1',1)[1].split('Pictiúr 2',1)[0]]),
            criterion('pictiur2','Pictiúr 2',13,[notice_p10.split('Pictiúr 2',1)[1],notice_p11.split('Pictiúr 3',1)[0]]),
            criterion('pictiur3','Pictiúr 3',4,[notice_p11.split('Pictiúr 3',1)[1].split('Pictiúr 4',1)[0]]),
            criterion('pictiur4','Pictiúr 4',4,[notice_p11.split('Pictiúr 4',1)[1].split('Cuir tic',1)[0]]),language(10)],
        ['Scríobh fógra bunaithe ar na ceithre phictiúr agus ar na treoracha.'],
        'Award the published picture submarks and one shared ten-mark language award. Follow the exact 2014 activity/place partial credit, date, fee, Sharon Shannon and school sports-hall rules within the affected picture awards. Required headings are not choices.')
    form_prompt = (
        'Ba mhaith leat a bheith ag obair don samhradh in Óstán na Trá, Loch Garman.\n\n'
        'Líon isteach An Fhoirm Iarratais atá anseo thíos. [Nóta: Is tusa Séamas Ó Néill.]\n\n'
        'Óstán na Trá, Loch Garman\nFoirm Iarratais do Phost Samhraidh\n\n'
        'Ainm: Séamas Ó Néill\nUimhir theileafóin:\nSeoladh:\nAois:\nDáta Breithe:\n'
        'Cén Scrúdú Teistiméireachta atá déanta agat?\nAinmnigh cúig ábhar scoile a rinne tú sa scrúdú sin:\n'
        'Luaigh trí chaitheamh aimsire atá agat:\nAn réitíonn tú go maith le daoine?\n'
        'An mbeidh tú sásta a bheith ag obair go luath gach maidin?\nCén modh taistil atá agat?\n'
        'Cén post ba mhaith leat? Cuir tic le ceann amháin (✓): Cócaire / Doirseoir / Freastalaí\n\n'
        'Scríobh alt gearr (timpeall 40 focal) ag insint cén fáth ar mhaith leat post samhraidh san óstán seo.\n\n'
        'Síniú: Séamas Ó Néill\nDáta:'
    )
    jobs=[('cocaire','Cócaire'),('doirseoir','Doirseoir'),('freastalai','Freastalaí')]
    for _,job in jobs:
        assert job in texts[14], 'Printed job changed: repeat selection review'
    fields_guide = [
        'Na Ceisteanna = 15 mharc. Úsáid an colún dúbailte: uimhir theileafóin2; seoladh4; aois2; dáta breithe2; scrúdú2; cúig ábhar10; trí chaitheamh aimsire3; réiteach le daoine1; obair go luath gach maidin1; modh taistil1; post1; dáta ag bun1. Iomlán30 ÷ 2 = 15.',
        'Round up once after adding the doubled question awards and dividing by two: 21 ÷ 2 = 10½ → 11. Do not round each half-mark field separately.',
        scheme_guidance(13,13)[0].split('An Córas Marcála',1)[1],
        scheme_guidance(14,14)[0].split('An t-Alt',1)[0],
    ]
    forms=[]
    for key,job in jobs:
        forms.append(add(f'W-4B-{key}','3',f'Scríobh · Ceist 4(b) · {job}',
            form_prompt+f'\n\nAn rogha don chárta seo: {job}.',
            'irish-9-0',['form'],[15],[13,14],[
                criterion('fields','Na Ceisteanna · iomlán slán',15,fields_guide),
                criterion('paragraph','An t-Alt · marc tar éis coigeartú faid',15,[
                    scheme_guidance(14,14)[0].split('An t-Alt',1)[1].split('Cruinneas Gaeilge',1)[0],
                    'Mark the relevant paragraph out of15. Off-topic ceiling5. Then apply the published proportional short-length reduction to this paragraph award only. Example: 30 of40 words → deduct25% of the awarded paragraph mark. Enter that final paragraph score; keep the form-answer and shared-language scores separate.'
                ]), language(10)],
            ['Líon gach réimse riachtanach; cúig ábhar scoile agus trí chaitheamh aimsire.',
             f'Roghnaigh {job} mar phost.',
             'Scríobh timpeall 40 focal faoin bpost san óstán.'],
            'One whole40-mark form: questions15 (half marks combined then rounded up once), paragraph15 with its own proportional length adjustment and off-topic ceiling5, shared language10 across questions and paragraph. Three printed job choices are expanded; school subjects, hobbies and personal answers remain open content choices.'))
    stories=[]
    for slot,page,start,end in [('5A',16,15,15),('5B',17,16,16)]:
        prompt = (
            'Féach ar an bpictiúr thíos.\n\nBhí tú ag Féile Cheoil an samhradh seo caite.\nTá tú chun cuntas (timpeall 90 focal) a scríobh in Iris na Scoile faoin bhFéile Cheoil sin.\n\nScríobh an cuntas sin (timpeall 90 focal) sa spás atá faoin bpictiúr.\n\nFéile Cheoil'
            if slot == '5A' else
            'Féach ar na pictiúir anseo thíos.\n\nTharla an eachtra seo agus tú amuigh ag siúl le do chara.\nTá tú chun scríobh faoin eachtra seo in Iris na Scoile (timpeall 90 focal).\n\nScríobh faoin eachtra (timpeall 90 focal) sa spás atá faoi na pictiúir.\n\nEACHTRA A THARLA'
        )
        # Final awarded-response adjustment must stay within this story when paired.
        stories.append(add('W-'+slot,'3','Scríobh · Ceist '+slot[0]+'('+slot[1].lower()+')',
            prompt,'irish-9-4',['pictures','story'],[page],list(range(start,end+1)),[
                criterion('freagra','Freagra iomlán · Cumarsáid 37 + Gaeilge 13',50,[
                    'Cumas Cumarsáide = 37 marc; Cruinneas Gaeilge = 13 mharc. Mark both parts, then enter the final whole-response mark after any published proportional length adjustment.',
                    *scheme_guidance(start,end),*language(13)['guidance'],
                    'If too short, subtract the appropriate percentage of the awarded mark: the SEC example is 45 words → mark the attempt, then deduct approximately 50% of the awarded mark. Apply this only to this story. No later-year fixed length table is printed.'
                ])],
            ['Scríobh timpeall 90 focal in Iris na Scoile.','Tabhair cúig thagairt ar a laghad don ócáid sna pictiúir.'],
            'First assess communication /37 and language /13. Reduce the communication ceiling by five per missing reference; for 5(b), cover each of the four pictures plus a fifth detail. The final story score includes the scheme’s proportional short-length reduction (45 words: deduct approximately 50% of the awarded mark). Enter that final mark out of 50. References are indicative, not a closed pool.'))
    # One Q4 and one Q5 required; expand all three jobs within the form.
    for first,second in itertools.product([notice,*forms],stories):
        combine(first['atlasQuestionId']+'-'+second['atlasQuestionId'].removeprefix('W-'),
            first['questionRef'].replace('2014 FL ','')+' + '+second['questionRef'].replace('2014 FL ',''),
            [first,second], 'FREAGAIR GACH CEIST (4 AGUS 5). Ceist 4: Freagair (a) NÓ (b). Ceist 5: Freagair (a) NÓ (b).')
    # Classify exact raw directive lines across all twenty paper pages. Unknown
    # additions on an already-reviewed page and stale keys both fail generation.
    decisions = selection_decisions(paper)
    assert len(cards)==74 and len({c['id'] for c in cards})==74
    assert sum(c['totalMarks'] for c in cards if c['atlasQuestionId'].startswith('A-'))==120
    review=dict(year=2014,level='foundation',paperFileid=FILE+'.pdf',
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
    return dict(review=review,cards=cards),scheme

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check',action='store_true')
    args=parser.parse_args()
    data,scheme=build()
    content=json.dumps(data,ensure_ascii=False,indent=2)+'\n'
    scheme_text='# Gaeilge Bonnleibhéal 2014 — SEC marking scheme\n\n'+'\n\n'.join(f'## PDF page {i+1}\n\n'+scheme_page_text(p) for i,p in enumerate(scheme))
    scheme_text = '\n'.join(line.rstrip() for line in scheme_text.splitlines()).rstrip()+'\n'
    outputs={OUT:content,ROOT/'examiner-reports/irish/schemes/2014-fl.md':scheme_text}
    for path,value in outputs.items():
        if args.check:
            assert path.exists() and path.read_text()==value, f'Stale Foundation output: {path}'
        else: path.write_text(value)
    print(f"Irish Foundation 2014: {len(data['cards'])} reviewed task/selection cards; archive remains incomplete.")

if __name__=='__main__': main()
