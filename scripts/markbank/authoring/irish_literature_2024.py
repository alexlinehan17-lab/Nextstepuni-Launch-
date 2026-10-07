"""Complete the source review of Higher 2024 Paper 2 Q3A and Q4.

All eight existing response identities and prompts survive. A shared Gaeilge
award keeps each response whole; scheme conditions remain with their award.
"""
from __future__ import annotations
import hashlib
import re
import fitz
from irish_higher_routes import ROOT, HASHES, compact, section, award


SELECTIONS = {
    3: [
        ('Tá Ceist 1 - 5 ar aon mharc. Glacfar le freagraí i d’fhocail féin nó', 'Source wording or own wording are acceptable answer styles, not different tasks.'),
        ('Freagair Ceist 2A (30 marc) nó Ceist 2B (30 marc).', 'All six prose routes are present, including both film/drama alternatives.'),
        ('Freagair ceist amháin as do rogha de 2A (a) nó 2A (b).', 'Three prescribed prose routes after expanding the film/drama choice.'),
        ('nó', 'Repeated separator for the prescribed/optional families.'),
        ('Freagair ceist amháin as do rogha de 2B (a) nó 2B (b).', 'Three optional prose routes after expanding the film/drama choice.'),
        ('Freagair Ceist 3A (30 marc) nó Ceist 3B (30 marc).', 'All four prescribed/optional poetry responses are present.'),
        ('Freagair ceist amháin as do rogha de 3A (a) nó 3A (b).', 'Both prescribed poems are separate whole thirty-mark responses.'),
        ('nó', 'Repeated separator for the prescribed/optional families.'),
        ('Freagair ceist amháin as do rogha de 3B (a) nó 3B (b).', 'Both optional-poem prompts are separate whole thirty-mark responses.'),
        ('Freagair do rogha ceann amháin as Ceist 4 (A, B, C, D, E nó F).', 'Six complete forty-mark responses, one for each printed A–F option.'),
    ],
    9: [
        ('Freagair Ceist 3A (Filíocht Ainmnithe) nó Ceist 3B (Filíocht Roghnach).', 'All four responses are present; prescribed poetry has its own archive topic.'),
        ('Freagair do rogha ceann amháin de (a) nó (b).', 'Two complete prescribed responses with shared Gaeilge.'),
        ('‘Tugtar léiriú dúinn sa dán Géibheann (thíos) ar an gcodarsnacht idir dhá thréimhse éagsúla i saol', 'Both periods are required comparison content, not selectable alternatives.'),
        ('(Is leor pointe amháin eolais as an dán mar thacaíocht le do fhreagra.)', 'One open supporting point; no printed finite menu.'),
        ('FILÍOCHT AINMNITHE nó FILÍOCHT ROGHNACH 30 marc', 'Repeated section heading, already expanded above.'),
    ],
    10: [
        ('nó', 'Separator before the second prescribed poem.'),
        ('(Is leor pointe amháin eolais as an dán mar thacaíocht le do fhreagra.)', 'One open supporting point; no printed finite menu.'),
        ('(iii) Roghnaigh dhá cheann de na haidiachtaí a úsáideann an file sa dán. Déan plé ar an tábhacht', 'Retrieve two adjectives from the source and interpret their importance. These are candidate answers to one retrieval/interpretation task, not an enumerated menu of task prompts. The scheme explicitly labels its words as examples, accepts other valid content on merit, and marks the discussion together. Do not turn its illustrative list into a closed exhaustive pool or leak those answers into the prompt.'),
        ('Cliabh dhá dhroim,', 'Poem text, not a candidate selection directive.'),
    ],
    12: [
        ('Freagair do rogha ceann amháin as Ceist 4 (A, B, C, D, E nó F) thíos.', 'Six whole forty-mark responses generated mechanically from the printed A–F headings.'),
        ('á úsáid sa dán, dar leat? Is leor dhá phointe eolais. Bíodh tagairtí cruinne agat do théacs an', 'Two open supporting points about the imperative, not a finite printed menu. The better point earns five and the other four; keep the nine-mark award together.'),
    ],
}


# Literal full-paper line audit: narrative and task directives are distinguished.
# Changes require a fresh source review, including previously empty pages.
SELECTIONS.update({4: [('le droichead nó le cabhsa, agus nach bhfuil faoi',
      'Passage narrative: bridges/causeways, remaining/moving, and available choices describe islands; no candidate '
      'task choice.'),
     ('chun fanacht ar na hoileáin nó chun bogadh',
      'Passage narrative: bridges/causeways, remaining/moving, and available choices describe islands; no candidate '
      'task choice.'),
     ('go mbeadh teacht acu ar rogha leathan',
      'Passage narrative: bridges/causeways, remaining/moving, and available choices describe islands; no candidate '
      'task choice.')],
 5: [('1. (a) Scríobh síos dhá shaintréith ar leith atá ag baint le gach ceann de na trí oileán is fiche amach',
      'Reading task A1a: source retrieval or open supporting points, classified with its exact whole prompt and '
      'published allocation in irish-reading-review.json.'),
     ('(b) (i) Luaigh beart amháin atá sa pholasaí maidir le cúrsaí fostaíochta ar na hoileáin. (Alt 2)',
      'Reading task A2bi: source retrieval or open supporting points, classified with its exact whole prompt and '
      'published allocation in irish-reading-review.json.'),
     ('3. (a) Scríobh síos dhá dhúshlán a bhaineann le soláthar cuí tithíochta ar na hoileáin a luadh le linn',
      'Reading task A3a: source retrieval or open supporting points, classified with its exact whole prompt and '
      'published allocation in irish-reading-review.json.'),
     ('(b) (i) Luaigh moladh amháin atá sa pholasaí nua chun cúrsaí tithíochta a fheabhsú ar na hoileáin.',
      'Reading task A3bi: source retrieval or open supporting points, classified with its exact whole prompt and '
      'published allocation in irish-reading-review.json.'),
     ('(ii) Scríobh síos beart amháin atá sa pholasaí a chinnteoidh go mbeidh áiseanna cuí oideachais',
      'Reading task A3bii: source retrieval or open supporting points, classified with its exact whole prompt and '
      'published allocation in irish-reading-review.json.'),
     ('4. (a) Tabhair dhá chúis a mealltar a lán turasóirí go dtí na hoileáin. (Alt 4)',
      'Reading task A4a: source retrieval or open supporting points, classified with its exact whole prompt and '
      'published allocation in irish-reading-review.json.'),
     ('(b) (i) Scríobh síos aidhm amháin a bheidh leis an bhfeachtas margaíochta a fhorbróidh Fáilte',
      'Reading task A4bi: source retrieval or open supporting points, classified with its exact whole prompt and '
      'published allocation in irish-reading-review.json.'),
     ('5. (a) Scríobh síos dhá ghealltanas atá tugtha sa pholasaí nua maidir le seirbhísí iompair farraige',
      'Reading task A5a: source retrieval or open supporting points, classified with its exact whole prompt and '
      'published allocation in irish-reading-review.json.'),
     ('(b) (i) Luaigh cuspóir amháin atá ag an rialtas sa pholasaí seo chun seirbhísí sláinte a fheabhsú',
      'Reading task A5bi: source retrieval or open supporting points, classified with its exact whole prompt and '
      'published allocation in irish-reading-review.json.'),
     ('Tabhair dhá phointe eolais, i d’fhocail féin, as an sliocht, mar thacaíocht le do fhreagra.',
      'Reading task A6b: source retrieval or open supporting points, classified with its exact whole prompt and '
      'published allocation in irish-reading-review.json.')],
 6: [('na linne seo. Roghnaigh an foilsitheoir foclóirí',
      'Passage narrative about dictionary selection, technology uses, time and behaviour; no candidate task choice.'),
     ('a gcuntais meán sóisialta nó nuair a labhraíonn',
      'Passage narrative about dictionary selection, technology uses, time and behaviour; no candidate task choice.'),
     ('siad tuarthéacs nó nuair a bhíonn siad ag',
      'Passage narrative about dictionary selection, technology uses, time and behaviour; no candidate task choice.'),
     ('taobh istigh de dhá mhí agus is é an feidhmchlár',
      'Passage narrative about dictionary selection, technology uses, time and behaviour; no candidate task choice.'),
     ('ar iompraíocht an duine nó nach mbeadh.',
      'Passage narrative about dictionary selection, technology uses, time and behaviour; no candidate task choice.')],
 7: [('nó nach bhfuil cuid den eolas iontu cruinn', 'Passage narrative: reliability of generated information.'),
     ('1. (a) Tabhair dhá chúis ar roghnaigh an foilsitheoir foclóirí Collins an téarma ‘intleacht shaorga’',
      'Reading task B1a: classified with its exact whole prompt and published allocation in '
      'irish-reading-review.json.'),
     ('(b) (i) Luaigh dhá shampla den úsáid a bhaineann daoine as an intleacht shaorga gach lá. (Alt 1)',
      'Reading task B1bi: classified with its exact whole prompt and published allocation in '
      'irish-reading-review.json.'),
     ('3. (a) Scríobh síos dhá dheis a bhaineann leis an intleacht shaorga i dtionscal an ghnó agus',
      'Reading task B3a: classified with its exact whole prompt and published allocation in '
      'irish-reading-review.json.'),
     ('(b) (i) Tabhair dhá dhúshlán atá ag baint leis an intleacht shaorga don duine aonair. (Alt 4)',
      'Reading task B4bi: classified with its exact whole prompt and published allocation in '
      'irish-reading-review.json.'),
     ('(ii) Scríobh síos dhá chúis a bhfuil amhras léirithe maidir leis na buntéacsanna a mbaineann',
      'Reading task B4bii: classified with its exact whole prompt and published allocation in '
      'irish-reading-review.json.'),
     ('(ii) Scríobh síos dhá cheist a ardaítear i ndíospóireachtaí faoi thodhchaí na hintleachta saorga.',
      'Reading task B5bii: classified with its exact whole prompt and published allocation in '
      'irish-reading-review.json.'),
     ('(b) Bunaithe ar an eolas sa sliocht thuas, mínigh dhá léargas a fhaigheann tú ar an intleacht shaorga.',
      'Reading task B6b: classified with its exact whole prompt and published allocation in '
      'irish-reading-review.json.'),
     ('Bíodh sampla amháin as an sliocht agat, i d’fhocail féin, ag tacú le gach ceann den dá léargas',
      'Reading task B6b: classified with its exact whole prompt and published allocation in '
      'irish-reading-review.json.')],
 8: [('Freagair Ceist 2A (Prós Ainmnithe) nó Ceist 2B (Prós Roghnach).',
      'Prose family choice: all six routes retained.'),
     ('Freagair do rogha ceann amháin de (a) nó (b) thíos.',
      'Prescribed prose outer choice: three routes after internal film/drama expansion.'),
     ('Freagair an cheist thíos ar an scannán Cáca Milis nó ar an dráma An Lasair Choille.',
      'Closed film/drama choice: Cáca Milis and An Lasair Choille both present.'),
     ('nó', 'Separator for classified alternatives.'),
     ('nó', 'Separator for classified alternatives.'),
     ('Freagair do rogha ceann amháin de (a) nó (b) thíos.',
      'Optional prose outer choice: three routes after internal film/drama expansion.'),
     ('Freagair an cheist thíos ar an scannán roghnach nó ar an dráma roghnach.',
      'Closed genre choice: optional film and optional drama both present.'),
     ('nó', 'Separator for classified alternatives.'),
     ('nó', 'Separator for classified alternatives.'),
     ('Maidir le gearrscéal roghnach a ndearna tú staidéar air le linn do chúrsa, roghnaigh duine',
      'Character comes from a student-chosen story; open choice, not a finite printed pool.'),
     ('PRÓS AINMNITHE nó PRÓS ROGHNACH 30 marc', 'Repeated prescribed/optional section heading.')],
 11: [('Freagair do rogha ceann amháin de (a) nó (b) thíos.', 'Two whole optional poetry prompts, both retained.'),
      ('(Is leor pointe amháin eolais as an dán mar thacaíocht le do fhreagra.)', 'One open supporting point.'),
      ('nó', 'Separator between the two whole responses.'),
      ('(Is leor pointe amháin eolais as an dán mar thacaíocht le do fhreagra.)', 'One open supporting point.'),
      ('Tabhair dhá phointe eolais as an dán faoin teicníc sin.',
       'Two open supporting points about a stated technique, not a finite printed menu.')],
 16: [('D’fhéadfadh sé go bhfuil téacsanna nó íomhánna sa scrúdpháipéar seo nach é Coimisiún na Scrúduithe',
       'Copyright notice, not a candidate instruction.'),
      ('Chóipcheart agus Cearta Gaolmhara, 2000. Ní údaraítear aon úsáid dá éis chun aon chríche ach amháin',
       'Copyright notice, not a candidate instruction.')]})


def classify(paper):
    decisions=[]
    for page in range(1,len(paper)+1):
        expected=SELECTIONS.get(page,[])
        actual=[compact(line) for line in paper[page-1].get_text().splitlines()
                if re.search(r'\b(rogha|roghnaigh|nó|dhá|amháin)\b',line,re.I)]
        assert actual==[quote for quote,_ in expected], ('Unknown or stale selection',page,actual)
        decisions += [dict(page=page,quote=q,reason=r) for q,r in expected]
    return decisions


def apply_literature_review(cards):
    docs=[]
    for kind,file,expected in [('exampapers','LC001ALP200IV.pdf',HASHES[2024][0]),
                               ('markingschemes','LC001ALP000IV.pdf',HASHES[2024][1])]:
        path=ROOT/f'paper-trail-corpus/{kind}/2024/{file}'
        assert hashlib.sha256(path.read_bytes()).hexdigest()==expected,'Repeat literature source review'
        docs.append(fitz.open(path))
    paper,scheme=docs
    decisions=classify(paper)
    s={n:compact(re.sub(r'(?m)^\s*\d+\s*$', '',page.get_text())) for n,page in enumerate(scheme,1)}
    by_id={c['id']:c for c in cards}
    reviewed=[]
    language=award('gaeilge','Gaeilge',5,
        '5 sárchumas; 4 cumas an-mhaith; 3 cumas maith; 2 cumas measartha; 1 cumas lag/an-lag; 0 gan fiúntas. Gramadach, comhréir, struchtúr agus deilbhíocht.')

    def update(key,atlas,title,pages,scheme_pages,criteria):
        card=by_id['irish-2024-hl-p2-'+key]
        card.update(questionRef='2024 HL Paper 2 '+title,atlasQuestionId=atlas,
                    reviewedAt='2026-10-07',reviewedPaperPages=pages,
                    paperPage=pages[0],paperTraceScore=1,schemeTraceScore=1,
                    schemePage=scheme_pages[0],schemePages=scheme_pages,
                    criteria=criteria+[dict(language)],
                    taskRequirements=['Freagair gach cuid den cheist atá priontáilte.',
                                      'Úsáid tagairtí cruinne agus ábhartha don téacs.'],
                    markingGuideNote='One complete SEC response with one shared five-mark Gaeilge award. The Eolas criteria retain the printed caps and conditions. Supporting examples are indicative rather than exhaustive.')
        assert sum(c['maxMarks'] for c in card['criteria'])==card['totalMarks']
        reviewed.append(card['id'])

    for option,title,pages,scheme_pages,guide in [
        ('a','Géibheann',[9],[33,34,35],section(s[33],r'\(a\) Géibheann')+' '+s[34]),
        ('b','An tEarrach Thiar',[10],[35,36,37],section(s[35],r'\(b\) An tEarrach Thiar')+' '+s[36]+' '+s[37].split('Gaeilge',1)[0]),
    ]:
        parts=[section(guide,r'\('+part+r'\)',r'\('+nxt+r'\)' if nxt else None)
               for part,nxt in [('i','ii'),('ii','iii'),('iii',None)]]
        if option=='a':
            assert 'as 10 marc' in parts[0] and 'bronn 0 ar an mír ar fad' in parts[2]
        else:
            assert 'gan dul thar 3 mharc' in parts[2] and 'Níos mó ná dhá aidiacht' in parts[2]
        update('poetry-3a-'+option,'F-3A-'+option,'Filíocht 3A('+option+') · '+title,pages,scheme_pages,
               [award('eolas-'+part,'Eolas ('+part+')',marks,text)
                for part,marks,text in zip(['i','ii','iii'],[13,5,7],parts)])

    # A–F is a finite printed choose-one pool. Iterate the actual headings and
    # pin all six existing identities rather than creating a second generic card.
    headings=re.findall(r'\b4([A-F])\.\s+([^\n]+)',paper[11].get_text())
    assert [letter for letter,_ in headings]==list('ABCDEF'),headings
    scheme_all=' '.join(s[n] for n in range(42,51))
    scheme_pages={'A':[41,42,43],'B':[41,43,44],'C':[41,44,45],
                  'D':[41,45,46],'E':[41,46,47],'F':[47,48,49,50]}
    general=s[41].rsplit('Gaeilge',1)[0]
    for index,(letter,title) in enumerate(headings):
        key='literature-4-'+letter.lower()
        if letter=='F':
            criteria=by_id['irish-2024-hl-p2-'+key]['criteria'][:-1]
            assert [c['maxMarks'] for c in criteria]==[19,7,9]
            # Previously source-reviewed Q4F allocations and complete prompts.
        else:
            guide=section(scheme_all,r'4'+letter+r'\.',r'4'+chr(ord(letter)+1)+r'\.')
            assert 'as 25 marc' in guide,(letter,'Missing incomplete-response cap')
            criteria=[award('eolas','Eolas',35,general+' '+guide)]
        update(key,'X-4'+letter,'Litríocht 4'+letter+' · '+compact(title),
               [12,13] if letter=='F' else [12],scheme_pages[letter],criteria)
    assert len(reviewed)==8
    return cards,dict(year=2024,level='higher',paperFileid='LC001ALP200IV.pdf',
        paperSha256=HASHES[2024][0],schemeSha256=HASHES[2024][1],reviewDate='2026-10-07',
        scope='Q3A and Q4 source review; combine with reading and Higher route reviews for full paper reconciliation.',
        reviewedPaperPages=[3,9,10,12,13],reviewedSchemePages=list(range(33,38))+list(range(41,51)),
        cardIds=reviewed,selectionDecisions=decisions,
        boundaries=['Two complete prescribed poems: 13/5/7 Eolas plus one shared 5 Gaeilge.',
                    'Five whole additional-literature essays: 35 Eolas plus one shared 5 Gaeilge; incomplete required coverage caps Eolas at 25.',
                    'Q4F stays whole: 19/7/9 Eolas and one shared 5 Gaeilge; best imperative point earns 5, other 4.'],
        preservation='All eight existing IDs and full question prompts unchanged; published rubric conditions and complete scheme regions restored.')
