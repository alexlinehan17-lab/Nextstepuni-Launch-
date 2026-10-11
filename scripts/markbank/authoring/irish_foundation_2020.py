#!/usr/bin/env python3
"""Reviewed Foundation tasks. Counts are assertions, not corpus-completeness proof.

2020 paper pages 1–20 and scheme pages 1–20 visually reviewed on 2026-10-07.
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
OUT = ROOT / 'components/MarkBank/cards/irish/foundation-2020-authored.json'

def clean(text):
    return re.sub(r'\s+', ' ', text).strip()

def criterion(id, label, marks, guidance, exact=False, deduct_from=None):
    return dict(id=id, label=label, kind='deduction' if deduct_from else 'award',
                maxMarks=marks, permittedMarks=[0, marks] if exact else list(range(marks+1)),
                guidanceKind='exact-answer' if exact else 'quality', guidance=guidance,
                **({'deductFrom': deduct_from} if deduct_from else {}))

DIRECTIVE = re.compile(r'rogha|roghna|Freagair|Cuir tic|Ainmnigh|Luaigh|\bchoose\b|\beither\b|\bany\b|one of|\bnó\b|dhá phointe|dhá rud|dheartháir|dheirfiúr', re.I)
SOURCE_REVIEW = ROOT / 'scripts/markbank/authored/irish-foundation-2020-source-review.json'

def selection_decisions(paper):
    decisions = json.loads(SOURCE_REVIEW.read_text())['selectionDecisions']
    expected = {(d['page'],d['raw']) for d in decisions}
    found = {(i,clean(line)) for i,page in enumerate(paper,1) for line in page.get_text().splitlines() if DIRECTIVE.search(clean(line))}
    assert found == expected, ('Unclassified/stale selection directives', found-expected, expected-found)
    return decisions

def build():
    import fitz
    paper_path = ROOT / f'paper-trail-corpus/exampapers/2020/{FILE}.pdf'
    scheme_path = ROOT / f'paper-trail-corpus/markingschemes/2020/{FILE}.pdf'
    assert hashlib.sha256(paper_path.read_bytes()).hexdigest() == 'b834eb177a978fe59eb38f270104dd8cf7654346108a6da45b38245fb9a585c2', 'Paper changed: repeat visual review'
    assert hashlib.sha256(scheme_path.read_bytes()).hexdigest() == '68c56fc0aeee4e6b19c19e80049f8178e363765c413674d77ff39767507ddc9b', 'Scheme changed: repeat visual review'
    paper = fitz.open(paper_path)
    scheme = fitz.open(scheme_path)
    texts = [clean(p.get_text()) for p in paper]
    cards = []
    def add(key, section, ref, prompt, topic, exam_topics, pages, scheme_pages, criteria,
            requirements=None, note=None, **extra):
        marks = sum(c['maxMarks'] for c in criteria if c['kind'] == 'award')
        card = dict(id=f'irish-2020-fl-{key.lower()}', year=2020, level='foundation',
            paper=1, section=section, atlasQuestionId=key,
            questionRef=f'2020 FL {ref}', questionText=prompt, totalMarks=marks,
            topicId=topic, examTopicKeys=exam_topics, conceptId=f'irish-foundation-{key.lower()}',
            paperFileid=FILE, schemePage=scheme_pages[0], schemePages=scheme_pages,
            taskRequirements=requirements or [], criteria=criteria,
            markingGuideNote=note or 'Use the answer and tariff published by the SEC for this part.',
            sourceMaterial=dict(kind='source-text', label=ref,
                title=f'Gaeilge Bonnleibhéal 2020 · {ref}', pages=pages,
                attribution='© State Examinations Commission.',
                presentationNote='Original examination pages, including every required picture or passage.'),
            **extra)
        cards.append(card)
        return card

    # Multiple-choice distractors are possible answers to ONE task, not alternative
    # tasks; expanding them would teach knowingly wrong responses as valid routes.
    aural = [('1a', 2, 7, 'Cén spórt is fearr le Róisín?', None, 'Ag imirt cispheile = an tríú pictiúr'),
 ('1b',
  2,
  7,
  'Cá bhfuil an Láthair Náisiúnta Chispheile?',
  'I Loch Garman | I Luimneach | I dTamhlacht',
  'I dTamhlacht'),
 ('2a', 2, 7, 'Cá bhfuil Tomás ag obair?', None, 'In ollmhargadh = an dara pictiúr'),
 ('2b',
  2,
  7,
  'Cén obair a dhéanann Tomás i ndiaidh an lóin?',
  'Obair ag scipéad an airgid | Líonadh seilfeanna | Pacáil málaí',
  'Líonadh seilfeanna'),
 ('3', 3, 8, 'Cá bhfuil an bhean ag dul?', None, 'An linn snámha = an dara pictiúr'),
 ('4',
  3,
  8,
  'Cá bhfuil siopa an phoitigéara? (Cuir tic (✓) sa bhosca ceart.)',
  None,
  'An bosca ag an mbarr ar chlé (tic nó saighead sa bhosca)'),
 ('5a', 3, 8, 'Cén sórt tí atá le ligean ar cíos?', None, 'Teach scoite cois trá = an ceathrú pictiúr'),
 ('5b',
  3,
  8,
  'Cá bhfuil an t-ionad beárbaiciú?',
  'Ar thaobh an tí | Sa ghairdín ar chúl an tí | Trí chiliméadar ón teach',
  'Sa ghairdín ar chúl an tí'),
 ('6a',
  4,
  10,
  'Cá raibh Cáit agus a muintir don deireadh seachtaine?',
  'San Iodáil | In ionad saoire i Longfort | Sa Spáinn',
  'In ionad saoire i Longfort'),
 ('6b',
  4,
  10,
  'Cad a rinne Cáit agus a deartháir tar éis an lóin Dé Sathairn?',
  'Snámh | D’imir siad leadóg | Rothaíocht',
  'Rothaíocht'),
 ('7a',
  4,
  10,
  'Cé a labhair leis na scoláirí sa séú bliain faoi dhrugaí?',
  'Garda Síochána | Múinteoir Eacnamaíocht Bhaile | Dochtúir',
  'Garda Síochána'),
 ('7b',
  4,
  10,
  'Cad a bhí ar siúl do na scoláirí sa chúigiú bliain ar an lá aclaíochta?',
  'Comórtas peile | Siúlóid 10 gciliméadar | Ranganna ióga',
  'Siúlóid 10 gciliméadar'),
 ('8a',
  4,
  10,
  'Cén fáth nár fhreagair Liam an téacs ó Nuala?',
  'Bhí a fhón póca briste | Ní raibh creidmheas aige | Chaill sé a fhón póca',
  'Chaill sé a fhón póca'),
 ('8b',
  4,
  10,
  'Cén cineál fóin atá le díol ag deartháir Nuala?',
  'Fón nua | Fón athláimhe | Fón seanfhaiseanta',
  'Fón athláimhe')]
    audio_url = 'https://www.examinations.ie/archive/exampapers/2020/LC001BLP017IV.mp3'
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
                title='Gaeilge Bonnleibhéal 2020 · An Chluastuiscint',playbackUrl=audio_url,
                secFileid='LC001BLP017IV.mp3',canonicalUrl=audio_url,
                attribution='© State Examinations Commission.',
                presentationNote='Official Foundation Level recording. Answer the question shown using its printed options.'))


    signs = ['Rabhadh\nPéint úr\nNá húsáid an doras seo',
 'Lá na Sábháilteachta Idirlín\nDé Máirt\n11 Feabhra',
 'Tae nó caife uait?\nNá húsáid cupán plaisteach',
 'Rogha na bhFaisean\nCeannaigh d’éide scoile anseo',
 'Íoslódáil Aip TG4\nsaor in aisce ar d’fhón',
 'Cumann na Croise Deirge\nDéan Cúrsa Garchabhrach linn\nGach eolas ó (01) 467308',
 'Oibreacha bóthair romhat\nLuas 60 ciliméadar san uair',
 'Giotár leictreach ar díol\nPraghas €150\nGlaoigh ar 084 254117',
 'Taispeántas Ealaíne\nDánlann Náisiúnta na hÉireann\nCead isteach: €10',
 'An Geata Bordála\nTaispeáin do thicéad\nagus do phas']
    for i,(sign,answer) in enumerate(zip(signs,'GEIFABJDCH'),1):
        add(f'R-1-{i}','2',f'Léamhthuiscint · Ceist 1({i})',
            'Meaitseáil na pictiúir leis na fógraí/comharthaí agus scríobh síos an litir cheart sa bhosca in aice leis an uimhir cheart atá sa ghreille.\n\n'+f'{i}. {sign}',
            'irish-9-1',['match'],[5],[4],
            [criterion('answer','Litir cheart',4,[answer,
                'Glactar le córas eile (uimhir an phictiúir in ionad litir an phictiúir) má tá sé soiléir / intuigthe.'],True)])

    # Each row: verbatim question, printed alternatives (or none), official answer.
    reading = {'2A': (6,
        'letterReading',
        [('Cathain a d’fhreastail Peadar ar an agallamh?',
          '13 Lúnasa | 16 Meán Fómhair | 20 Meán Fómhair',
          '16 Meán Fómhair'),
         ('Cén grád a fuair Peadar sa Teicneolaíocht san Ardteistiméireacht?',
          'Grád O2 | Grád H3 | Grád H4',
          'Grád H4'),
         ('Cad a gheobhaidh an printíseach dhá lá sa tseachtain?',
          'Scrúdú | Ranganna | Taithí phraiticiúil',
          'Taithí phraiticiúil'),
         ('Cad a bheidh sa ríomhphost a sheolfar chuig Peadar má ghlacann sé le háit ar an gcúrsa?',
          'Liosta lóistín | Torthaí na hArdteistiméireachta | Gach eolas faoin gcúrsa',
          'Liosta lóistín'),
         ('Cén post atá ag Muireann Ní Chonaill?',
          'Leictreoir | Oifigeach Pearsanra | Stiúrthóir',
          'Oifigeach Pearsanra')]),
 '2B': (7,
        'brochure',
        [('Cá bhfuil Ionad an Bhlascaoid Mhóir suite?',
          'Ar na Blascaodaí | Sa Daingean | I nDún Chaoin',
          'I nDún Chaoin'),
         ('Cathain a tréigeadh an Blascaod Mór?',
          'Sa bhliain 1953 | Na céadta bliain ó shin | Sa bhliain 1993',
          'Sa bhliain 1953'),
         ('Cén tsiombail de thraidisiún na hiascaireachta atá ar taispeáint sa mhúsaem?',
          'Agallaimh | Naomhóg | Grianghraif',
          'Naomhóg'),
         ('Cén leabhar a scríobh Muiris Ó Súilleabháin?',
          'Machnamh Seanmhná | An tOileánach | Fiche Bliain ag Fás',
          'Fiche Bliain ag Fás'),
         ('Cén áit ar an oileán ar féidir le cuairteoirí fanacht?',
          'Teach Thomáis Uí Chriomhthain | Sa teach lóistín | Sa chaifé',
          'Sa teach lóistín')]),
 '2C': (8,
        'news',
        [('Cén seomra ina raibh Muiris nuair a chuala sé fuaim aisteach?',
          'Sa seomra suí | Sa chistin | Sa seomra leapa',
          'Sa chistin'),
         ('Cad ba chúis leis an bhfuaim aisteach?', 'Éan beag dubh | Luch | Cat', 'Éan beag dubh'),
         ('Cá raibh an súiche dubh le feiceáil?',
          'Ar an bhfuinneog | Os comhair an tinteáin | Ar an doras',
          'Os comhair an tinteáin'),
         ('Cad a chaith Muiris isteach sa seomra suí?', 'Spúnóg adhmaid | Súiche | Píosa aráin', 'Píosa aráin'),
         ('Conas a d’éalaigh an t-éan amach as an teach?',
          'Tríd an bhfuinneog oscailte | Suas an simléar | Tríd an doras',
          'Tríd an bhfuinneog oscailte')]),
 '3A': (9,
        'news',
        [('Cad as do Shibéal Ní Chasaide?', 'Gaoth Dobhair | Ráth Chairn | Meiriceá', 'Ráth Chairn'),
         ('Cad a thosaigh sí ag foghlaim nuair a bhí sí cúig bliana d’aois?',
          'An veidhlín | An chláirseach | Amhránaíocht ar an sean-nós',
          'Amhránaíocht ar an sean-nós'),
         ('Cén t-amhrán a chan Sibéal ar RTÉ sa chlár chun Éirí Amach na Cásca 1916 a chomóradh?',
          'Fuarú | Mise Éire | Ceol 2018',
          'Mise Éire'),
         ('Cá raibh Sibéal ag canadh i mí Mheán Fómhair 2019?',
          'Sa Phuball Gaeilge | I nDroichead Átha | Ag Fleadh Cheoil na hÉireann',
          'Sa Phuball Gaeilge'),
         ('Cár fhan Sibéal agus í sa chéad bhliain ar Ollscoil na hÉireann, Baile Átha Cliath?',
          None,
          'I dTeach na Gaeilge')]),
 '3B': (10,
        'extract',
        [('Cén cineál clár is mó a chuireann Hector Ó hEochagáin i láthair?',
          'Cláir thaistil | Cláir chainte | Cláir cheoil',
          'Cláir thaistil'),
         ('Cá bhfuil Hector ina chónaí faoi láthair?',
          'Sa Spáinn | I gContae na Gaillimhe | Ar Inis Meáin',
          'I gContae na Gaillimhe'),
         ('Cén áit a raibh Hector sa tsraith is déanaí?',
          'Meiriceá Láir | An Áise | Na Stáit Aontaithe',
          'Na Stáit Aontaithe'),
         ('Cé hé Carl Lewis?', 'Buachaill bó | Lúthchleasaí | Amhránaí', 'Lúthchleasaí'),
         ('Cad é an rud is spéisiúla faoi Hector ina chuid clár taistil?', None, 'Nach gcuireann aon rud eagla air')]),
 '3C': (11,
        'poem',
        [('Cén t-am atá sé agus an file ag déanamh ar an stáisiún traenach?', '5.45 | 6.15 | 6.45', '5.45'),
         ('Cad atá ag sleamhnú siar?', 'An stáisiún traenach | An ghealach | An ghrian', 'An ghealach'),
         ('Cad atá ag damhsa sa stáisiún traenach?', 'Duine | Cosa | Duilleoga', 'Duilleoga'),
         ('Cén treo a bhféachann an file?', 'Ó thuaidh | Ó dheas | Siar', 'Ó dheas'),
         ('Cad a dhéanfaidh an file nuair a stopfaidh an traein?', None, 'Brostóidh an file/mé/sé/sí ar bord')])}
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
                card['criteria'][0]['permittedMarks'] = [0,1,3,4,6]
                card['criteria'][0]['guidance'] += [
                    '6 mharc: I dTeach na Gaeilge ar an gcampas.',
                    '4 mharc: I dteach ar an gcampas; I dteach san ollscoil.',
                    '3 mharc: Ar an gcampas. 1 mharc: I dteach.']
            if slot == '3C' and i == 5:
                card['criteria'][0]['permittedMarks'] = [0,3,4,6]
                card['criteria'][0]['guidance'] += [
                    '3 mharc: Beidh an file/mé/sé/sí compordach istigh.',
                    '6 mharc: Líne 5 agus Líne 6 as Véarsa 3 le chéile.',
                    '4 mharc: An véarsa iomlán (iomarcaíocht).']
            reading_cards[slot].append(card)

    def combine(key,ref,members,pool_quote):
        criteria=[]
        for member in members:
            prefix=member['atlasQuestionId'].lower()+'-'
            for old in member['criteria']:
                c=copy.deepcopy(old)
                c['id']=prefix+c['id']
                c['label']=member['questionRef'].replace('2020 FL ','')+' · '+c['label']
                if 'deductFrom' in c: c['deductFrom']=prefix+c['deductFrom']
                criteria.append(c)
        topics=list(dict.fromkeys(t for c in members for t in [c['topicId'],*c.get('additionalTopicIds',[])]))
        result=add(key,members[0]['section'],ref,
            pool_quote+'\n\nAn rogha don chárta seo: '+ref+'\n\n'+
            '\n\n'.join(c['questionRef'].replace('2020 FL ','')+'\n'+c['questionText'] for c in members),
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
            'Dul na Gaeilge: struchtúr na Gaeilge agus beachtas gramadaí. Stór focal: cruinneas agus oiriúnacht stór focal. Litriú.',
            f'Bronn marc as {marks} ar chaighdeán na Gaeilge san iarracht iomlán.',
            'The band table on PDF page16 belongs only to the modified marking scheme. Do not apply it as the standard language rubric.'])
    def scheme_guidance(start,end):
        return [clean(re.sub(r'\n\s*\d+\s*$', '', scheme[p-1].get_text())) for p in range(start,end+1)]
    notice_p9 = scheme_guidance(9,9)[0]
    notice_p10 = scheme_guidance(10,10)[0]
    notice = add('W-4A','3','Scríobh · Ceist 4(a)',
        'Féach ar na pictiúir thíos.\n\nScríobh amach an FÓGRA a bhaineann leis an rud atá i gceist thuas.\n\n'+
        'Cén rud a bheidh ar siúl? Cén áit?\nCén lá? Cén dáta? Cén t-am? Táille?\nCén t-aoi speisialta a bheidh i láthair?\nCad a dhéanfar leis an airgead?',
        'irish-9-3',['notice'],[14],[8,9,10],[
            criterion('leagan','Leagan Amach',1,['Iarracht ar fhógra.']),
            criterion('pictiur1','Pictiúr 1',8,[notice_p9.split('Pictiúr 1',1)[1].split('Pictiúr 2',1)[0]]),
            criterion('pictiur2','Pictiúr 2',13,[notice_p9.split('Pictiúr 2',1)[1].split('Pictiúr 3',1)[0]]),
            criterion('pictiur3','Pictiúr 3',4,[notice_p9.split('Pictiúr 3',1)[1],notice_p10.split('Pictiúr 4',1)[0]]),
            criterion('pictiur4','Pictiúr 4',4,[notice_p10.split('Pictiúr 4',1)[1].split('Cuir tic',1)[0]]),language(10)],
        ['Scríobh fógra bunaithe ar na ceithre phictiúr agus ar na treoracha.'],
        'Award the published picture submarks and one shared ten-mark language award. Follow the exact 2020 activity/place partial credit, date, fee and guest-name rules within the affected picture awards. Required headings are not choices.')
    reply = add('W-4B','3','Scríobh · Ceist 4(b) · Freagra ar chuireadh',
        'Féach ar na pictiúir thíos.\n\nIs tusa Ruairí. Fuair tú an cuireadh seo ó Áine. Scríobh FREAGRA ar an gcuireadh seo.\n'
        'I do fhreagra, luaigh na pointí seo:\n\n'
        '- An lá a fuair tú an cuireadh — Pictiúr 1\n'
        '- Go raibh áthas ort nuair a fuair tú an cuireadh — Pictiúr 1\n'
        '- Gur iarr tú cead ar do Mham dul ann — Pictiúr 3\n'
        '- Go mbeidh tú ábalta dul ann — Pictiúr 3\n'
        '- Conas a rachaidh sibh ann — Pictiúr 3\n'
        '- Dhá rud faoin gcluiche — Pictiúr 4\n'
        '- An t-am a thiocfaidh sibh abhaile — Pictiúr 4\n\n'
        'N.B. Bíodh an leagan amach cuí ar do fhreagra: tús agus críoch oiriúnach.',
        'irish-9-3',['letterWriting'],[15],[11,12],[
            criterion('iarracht','Iarracht ar an bhfreagra',1,['Iarracht ar an bhfreagra = 1 mharc.']),
            criterion('beannu','Beannú',1,['Beannú = 1 mharc.']),
            criterion('slan','Slán / Síniú',1,['Slán / Síniú = 1 mharc.']),
            criterion('pictiur1','Pictiúr 1',7,[scheme_guidance(12,12)[0].split('Pictiúr 1',1)[1].split('Pictiúr 3',1)[0]]),
            criterion('pictiur3','Pictiúr 3',9,[scheme_guidance(12,12)[0].split('Pictiúr 3',1)[1].split('Pictiúr 4',1)[0]]),
            criterion('pictiur4','Pictiúr 4',11,[scheme_guidance(12,12)[0].split('Pictiúr 4',1)[1].split('Cuir tic',1)[0]]),
            language(10)],
        ['Scríobh freagra ar chuireadh Áine mar Ruairí.',
         'Luaigh gach pointe agus dhá rud faoin gcluiche; tús agus críoch oiriúnach.'],
        'The invitation reply stays whole: layout3, picture1=7(4+3), picture3=9(3+3+3), picture4=11(4+4+3), and one shared language10. Picture2 is the invitation source, not another assessed response. The two match details are open information, not a printed choice menu. No address/date or word-count penalty is specified.',
        additionalTopicIds=['irish-2-8'],taskFormatLabel='Freagra ar chuireadh')
    stories=[]
    for slot,page,end in [('5A',16,13),('5B',17,15)]:
        prompt = (
            'Féach ar an bpictiúr thíos.\n\nBhí tú ag Seó Tallainne le do chairde an mhí seo caite.\nTá tú chun cuntas (timpeall 90 focal) a scríobh in Iris na Scoile faoin Seó Tallainne sin.\n\nScríobh an cuntas sin (timpeall 90 focal) sa spás atá faoin bpictiúr.\n\nSeó Tallainne'
            if slot == '5A' else
            'Féach ar na pictiúir anseo thíos.\n\nTharla an eachtra seo agus tú ar thuras báid le do chara.\nTá tú chun scríobh faoin eachtra seo in Iris na Scoile (timpeall 90 focal).\n\nScríobh faoin eachtra (timpeall 90 focal) sa spás atá faoi na pictiúir.\n\nEACHTRA A THARLA'
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
    for first,second in itertools.product([notice,reply],stories):
        combine(first['atlasQuestionId']+'-'+second['atlasQuestionId'].removeprefix('W-'),
            first['questionRef'].replace('2020 FL ','')+' + '+second['questionRef'].replace('2020 FL ',''),
            [first,second], 'FREAGAIR GACH CEIST (4 AGUS 5). Ceist 4: Freagair (a) NÓ (b). Ceist 5: Freagair (a) NÓ (b).')
    # Classify exact raw directive lines across all twenty paper pages. Unknown
    # additions on an already-reviewed page and stale keys both fail generation.
    decisions = selection_decisions(paper)
    assert len(cards)==68 and len({c['id'] for c in cards})==68
    assert sum(c['totalMarks'] for c in cards if c['atlasQuestionId'].startswith('A-'))==120
    review=dict(year=2020,level='foundation',paperFileid=FILE+'.pdf',
        paperSha256=hashlib.sha256(paper_path.read_bytes()).hexdigest(),
        schemeSha256=hashlib.sha256(scheme_path.read_bytes()).hexdigest(),
        reviewedPaperPages=list(range(1,21)),reviewedSchemePages=list(range(1,21)),
        reviewDate='2026-10-07',status='reviewed',selectionDecisions=decisions,
        fullPaperAndApplicableSchemeVisualSweep=True,
        atomicPracticeCardIds=[c['id'] for c in cards if 'memberCardIds' not in c],
        pairedRouteCardIds=[c['id'] for c in cards if 'memberCardIds' in c],
        examStructure=dict(listening=120,matching=40,readingQ2=50,readingQ3=60,writingQ4=40,writingQ5=50,writing=90,total=360),
        nonPoolDecisions=[
            'MCQ distractors and map boxes are answers to one task, not independently valid task routes.',
            'All notice headings and invitation-reply points are compulsory context. Each whole response retains its own shared language award; Ruairí and Áine are prescribed roles, not recipient alternatives.',
            'The two match details in the reply and source-retrieval answers are content choices, not enumerated task prompts.',
            'The five story references are a communication criterion, with non-exhaustive examples, not a printed choose-five menu.',
            'The modified marking scheme changes assessment for eligible candidates, not the printed task or answer route.',
        ],
        openIssues=[],
        audio=json.loads(SOURCE_REVIEW.read_text())['audio'],
        boundaries='14 listening parts; 10 matching parts; 30 reading parts; 4 whole writing tasks; 6 paired reading routes; 4 writing products (one Q4 and one Q5).',
        caveats=json.loads(SOURCE_REVIEW.read_text())['sourceFindings'])
    return dict(review=review,cards=cards),scheme

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check',action='store_true')
    args=parser.parse_args()
    data,scheme=build()
    content=json.dumps(data,ensure_ascii=False,indent=2)+'\n'
    scheme_text='# Gaeilge Bonnleibhéal 2020 — SEC marking scheme\n\n'+'\n\n'.join(f'## PDF page {i+1}\n\n'+p.get_text() for i,p in enumerate(scheme))
    outputs={OUT:content,ROOT/'examiner-reports/irish/schemes/2020-fl.md':scheme_text}
    for path,value in outputs.items():
        if args.check:
            assert path.exists() and path.read_text()==value, f'Stale Foundation output: {path}'
        else: path.write_text(value)
    print(f"Irish Foundation 2020: {len(data['cards'])} reviewed task/selection cards; archive remains incomplete.")

if __name__=='__main__': main()
