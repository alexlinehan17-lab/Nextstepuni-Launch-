#!/usr/bin/env python3
"""Original-source selections after the independent 56-page 2019 visual sweep."""
import hashlib
import json
import re
import sys
import fitz
from lcvp_review_2026 import ROOT, tidy, select, numbered, point, criterion, menu, partial
from lcvp_review_2025 import paired_rows
from lcvp_review_2024 import split_raw
from lcvp_review_2022 import page_raw, explicit_menu, char_text
from lcvp_review_2021 import text_lines, single_printed_box
from lcvp_identity import concept_id

REVIEW = ROOT / 'scripts/markbank/authoring/lcvp/2019-cl-main-review.json'
PAPER = 'paper-trail-corpus/exampapers/2019/LC462CLP000EV.pdf'
SCHEME = 'paper-trail-corpus/markingschemes/2019/LC462CLP000EV.pdf'
HASHES = {PAPER:'187deb870b2768baa94a541da83c0d0447a167bc7f0d7ed94fe80659007cd752',
          SCHEME:'a342ee8e6a4394b8bb3e49e2809f165ebfb951dabe272783ee58129147037259'}
ADDED_IDS = {'lcvp-2019-cl-'+key for key in ['b3ii','c3ai','c3aii','c4a','c5ai','c5d']}
VIDEO_URL = 'https://www.examinations.ie/archive/exampapers/2019/LC462CLP031EV.mp4'
SPLIT_C = {(1,'d'),(2,'b'),(2,'d'),(3,'a'),(3,'d'),(5,'a')}
HELD_KEYS = {('C',6,'b',None)}


def documents():
    for path,expected in HASHES.items():
        assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==expected,path
    return fitz.open(ROOT/PAPER),fitz.open(ROOT/SCHEME)


def scheme_parts(doc,raw=False):
    sections=split_raw('\n'.join(page_raw(doc,n) for n in range(4,19)),r'^\s*Section ([ABC])\s+',list('ABC'))
    out={}
    for section,value in sections.items():
        pattern=r'^\s*Q\.\s*(\d+)\s*'
        if section=='C':
            # The Q.1–Q.6 labels inside the original questionnaire are examples.
            pattern+=r'(?=The world|Your Link|Teamwork|A visit|Voluntary|Information)'
        questions=split_raw(value,pattern,[str(n) for n in range(1,{'A':8,'B':3,'C':6}[section]+1)])
        for q,block in questions.items():
            if section=='A' and q=='5':
                for roman,part in split_raw(block,r'^\s*\((i{1,2})\)\s*',['i','ii']).items():out[(section,int(q),None,roman)]=part
            elif section=='A' or(section=='B' and q=='1'):out[(section,int(q),None,None)]=block
            elif section=='B':
                romans=['i','ii','iii'] if q=='2' else ['i','ii']
                for roman,part in split_raw(block,r'^\s*\((i{1,3})\)\s*',romans).items():out[(section,int(q),None,roman)]=part
            else:
                for letter,part in split_raw(block,r'^\s*\(([abcd])\)\s*',list('abcd')).items():
                    if (int(q),letter)==(3,'a'):
                        # Both prompts precede their separate name/role allocations.
                        for roman in ['i','ii']:out[(section,int(q),letter,roman)]=part
                    elif (int(q),letter) in SPLIT_C:
                        for roman,sub in split_raw(part,r'^\s*\((i{1,2})\)\s*',['i','ii']).items():out[(section,int(q),letter,roman)]=sub
                    else:out[(section,int(q),letter,None)]=part
    assert len(out)==45,len(out)
    return out if raw else {k:tidy(v) for k,v in out.items()}


PAGES={('A',q,None,None):p for q,p in enumerate([4,4,4,5,5,6,7,8],1)}
PAGES.pop(('A',5,None,None));PAGES.update({('A',5,None,r):5 for r in ['i','ii']})
PAGES[('B',1,None,None)]=10
PAGES.update({('B',q,None,r):9+q for q in [2,3] for r in (['i','ii','iii'] if q==2 else ['i','ii'])})
PAGES.update({('C',q,l,None):16+(q-1)*3+{'a':0,'b':0,'c':1,'d':2}[l] for q in range(1,7) for l in 'abcd'})
for q,l in SPLIT_C:
    page=PAGES.pop(('C',q,l,None));PAGES.update({('C',q,l,r):page for r in ['i','ii']})


def question(doc,key):
    section,q,letter,roman=key;value=page_raw(doc,PAGES[key])
    if section in ['A','B']:
        value=re.split(r'^\s*Q\.\s*'+str(q)+r'\s+',value,maxsplit=1,flags=re.M)[1]
        value=re.split(r'^\s*Q\.\s*\d+\s+',value,maxsplit=1,flags=re.M)[0]
    else:
        value=re.split(r'^\s*\('+letter+r'\)\s*',value,maxsplit=1,flags=re.M)[1]
        value=re.split(r'^\s*\([abcd]\)\s*',value,maxsplit=1,flags=re.M)[0]
    if roman:
        value=re.split(r'^\s*\('+roman+r'\)\s*',value,maxsplit=1,flags=re.M)[1]
        value=re.split(r'^\s*\(i{1,3}\)\s*',value,maxsplit=1,flags=re.M)[0]
    return tidy(re.sub(r'\(\d+\s+marks?\)','',value))


def source(pages,kind='source-question',title='Original question'):
    return dict(kind=kind,label='OFFICIAL SOURCE',title=title,pages=pages,
        attribution='SEC LCVP Link Modules 2019 Common Level — © State Examinations Commission.',
        presentationNote='Read the complete original source and question in context.')


def column_tail(doc,page_number,left_start,right_start,last):
    page=doc[page_number-1];lines=text_lines(page)
    start_label='(d)' if page_number==14 else '(a)'
    start=next(box.y0 for box,t in lines if t.startswith(start_label))
    end=page.rect.height if page_number==14 else next(box.y0 for box,t in lines if t.startswith('(b)'))
    lines=[(box,t) for box,t in lines if start<box.y0<end]
    left=next(box for box,t in lines if re.match(r'^'+str(left_start)+r'\.\s',t))
    right=next(box for box,t in lines if re.match(r'^'+str(right_start)+r'\.\s',t))
    last_boxes=[box for box,t in lines if re.match(r'^(?:'+str(right_start-1)+'|'+str(last)+r')\.\s',t)]
    assert len(last_boxes)==2,last_boxes
    top=min(left.y0,right.y0)-1;bottom=max(box.y1 for box in last_boxes)+1;split=right.x0-5
    value=char_text(page,fitz.Rect(0,top,split,bottom))+' '+char_text(page,fitz.Rect(split,top,page.rect.width,bottom))
    matches=list(re.finditer(r'(?<!\w)(\d+)\.\s+',value));assert [int(m[1]) for m in matches]==list(range(left_start,last+1)),value
    return [tidy(value[m.end():matches[i+1].start() if i+1<len(matches) else len(value)]) for i,m in enumerate(matches)]


def work_skills(doc,block):
    first=block.split('5.',1)[0]
    return numbered(first,4)+column_tail(doc,14,5,10,13)


def ict_uses(doc):
    return column_tail(doc,17,1,9,14)


def cv_headings(doc):
    return column_tail(doc,8,1,5,7)


def questionnaire_source(doc):
    page=doc[9]
    boxes=[item[1] for path in page.get_drawings() for item in path['items'] if item[0]=='re' and item[1].width>300 and item[1].height>100]
    box=single_printed_box([r for r in boxes if 'Questionnaire' in char_text(page,r)])
    markers=sorted([(fitz.Rect(w[:4]),w[4]) for w in page.get_text('words')
                    if box.contains(fitz.Rect(w[:4])) and re.fullmatch(r'Q\.[1-6]\*?',w[4])],key=lambda v:v[0].y0)
    assert [re.sub(r'\s+','',t) for _,t in markers]==['Q.1','Q.2','Q.3','Q.4','Q.5','Q.6*'],markers
    centres=[(r.y0+r.y1)/2 for r,_ in markers]
    starts=[markers[0][0].y0-2]+[(a+b)/2 for a,b in zip(centres,centres[1:])];ends=starts[1:]+[box.y1]
    heading=char_text(page,fitz.Rect(box.x0,box.y0,box.x1,starts[0]));rows=[]
    for top,bottom in zip(starts,ends):
        clip=fitz.Rect(box.x0,top,box.x1,bottom);fragments=[]
        for block in page.get_text('rawdict')['blocks']:
            for line in block.get('lines',[]):
                chars=[c for span in line['spans'] for c in span['chars'] if clip.contains(fitz.Point((c['bbox'][0]+c['bbox'][2])/2,(c['bbox'][1]+c['bbox'][3])/2))]
                if chars:fragments.append((min(c['bbox'][0] for c in chars),''.join(c['c'] for c in chars)))
        rows.append(tidy(' '.join(v for _,v in sorted(fragments))))
    assert all(row.startswith(f'Q.{i}') for i,row in enumerate(rows,1)),rows
    return heading+' '+' | '.join(rows)


def build():
    paper,scheme=documents();blocks,raw=scheme_parts(scheme),scheme_parts(scheme,raw=True)
    rows,totals,topics={},{},{}
    def put(key,mark,topic,value):rows[key],totals[key],topics[key]=value,mark,topic
    def a(q,r=None):return ('A',q,None,r)
    def b(q,r=None):return ('B',q,None,r)
    def c(q,l,r=None):return ('C',q,l,r)
    put(a(1),1,'0-2',[point('teacher',select(blocks[a(1)],'His LCVP teacher','1 mark',include=True),1)])
    for q,count,expected in [(2,2,6),(3,3,4),(4,4,5),(8,6,8)]:put(a(q),count,'0-2',menu(blocks[a(q)],count,1,expected))
    for q,count,expected in [(6,4,13),(7,6,10)]:put(a(q),count,'0-2',partial(blocks[a(q)],count,1,expected,
        'The complete original model pool is retained below; each distinct answer receives 1 or 0 marks.'))
    put(a(5,'i'),2,'0-2',[point('duration',select(blocks[a(5,'i')],'2 / 3 / 4 years','2 marks',include=True),2,'ONE accepted duration answer, 2 marks; preserve all original alternatives and no unprinted 1 mark step.')])
    put(a(5,'ii'),2,'0-2',[point('qualification',select(blocks[a(5,'ii')],'Level 8 NFQ','2 marks',include=True),2,'ONE accepted qualification answer, 2 marks; no unprinted internal split.')])
    put(b(1),6,'1-2',partial(blocks[b(1)],3,2,8))
    for r,count,expected in [('i',6,9),('ii',3,11),('iii',3,8)]:put(b(2,r),count,'1-2',menu(blocks[b(2,r)],count,1,expected))
    rows[b(2,'iii')][0]['contextNote']+=' MUST link to the SAME assistance selected in part(ii), as explicitly required by the original scheme.'
    put(b(3,'i'),3,'1-3',[point('enterprise','Name',1,'MUST be a SCHOOL BASED ACTIVITY/ENTERPRISE. Complete original pool: '+' | '.join(numbered(blocks[b(3,'i')],7))),
        criterion('reason','1 valid reason',1,[0,1,2],'ONE reason for the SAME named school-based enterprise, 1+1. Original name 1 and reason 2 are separately printed; preserve the whole response.')])
    headings=[tidy(s) for s in raw[b(3,'ii')].split('➢')[1:]];assert len(headings)==4,headings
    put(b(3,'ii'),9,'1-3',[criterion('plan','Set it out under three headings.',3,[0,1,2,3],
        'THREE distinct relevant headings, each 3 marks (1+1+1). Keep the plan applied to the SAME school enterprise and site. Retain ALL FOUR printed heading models; the paper requires three headings but does not restrict them to a named list. The general scheme accepts other valid responses. Original complete heading pool: '+' | '.join(headings))])
    cv=select(blocks[c(1,'a')],'A CV is used','1 mark',include=True)
    put(c(1,'a'),4,'0-4',[point('use',cv,1),*explicit_menu('Valid headings which should appear on a CV',cv_headings(scheme),3,
        'THREE distinct headings,1 each, from ALL SEVEN original choices in the two printed columns. The purpose of the CV receives its separate1 mark.')])
    for q,l,r,count,per,expected,topic in [(1,'b',None,3,2,7,'0-1'),(1,'c',None,3,2,9,'0-0'),(2,'d','ii',3,2,8,'1-3'),
        (3,'c',None,3,2,10,'1-0'),(3,'d','ii',3,2,7,'1-0'),(4,'c',None,4,2,10,'1-1'),(5,'b',None,3,2,11,'1-2'),
        (5,'c',None,3,3,9,'1-2'),(6,'c',None,4,2,15,'0-0'),(6,'d',None,3,3,12,'0-0')]:put(c(q,l,r),count*per,topic,partial(blocks[c(q,l,r)],count,per,expected))
    rows[c(1,'c')][0]['contextNote']+=' These are the original historical examination examples; the printed figures are retained exactly.'
    put(c(1,'d','i'),3,'0-0',[criterion('definition','Three valid explanations',3,[0,1],
        'Original 3 marks (1+1+1); three valid pieces from the complete original explanation, with no invented compulsory semantic split. Full source model: '+' | '.join(numbered(blocks[c(1,'d','i')],2)))])
    put(c(1,'d','ii'),6,'0-0',menu(blocks[c(1,'d','ii')],6,1,10))
    put(c(2,'a'),3,'1-3',menu(blocks[c(2,'a')],3,1,9))
    put(c(2,'b','i'),2,'1-3',[criterion('definition',select(blocks[c(2,'b','i')],'Market research involves',include=True),2,[0,1],
        'Original definition 2 marks (1+1); two valid pieces from the complete source definition, with no invented compulsory word split.')])
    put(c(2,'b','ii'),3,'1-3',menu(blocks[c(2,'b','ii')],3,1,6))
    model=questionnaire_source(scheme)
    put(c(2,'c'),8,'1-3',[point('heading','heading',1,'Original layout 3x1: heading, variety of question styles, instructions. If activity is non-hoodie based, mark on LAYOUT ONLY; all five question-content marks must remain 0. Complete original six-question model, all choices and compulsory finance marker: '+model),
        point('styles','variety of question styles',1),point('instructions','instructions',1),
        point('finance','Compulsory question relating to finance',1,'ONE of the FIVE questions must relate to finance; this counts within the five, not an extra mark. Only a relevant hoodie question scores.'),
        criterion('questions','questions',4,[0,1],'FOUR other distinct relevant hoodie questions, 1 each, alongside the separately required finance question 1. Original allocation: 5 questions, 5 x 1 mark total. Non-hoodie activity receives LAYOUT ONLY; no question-content marks. At least five questions are required; preserve all six source examples as alternatives.')])
    put(c(2,'d','i'),3,'1-3',menu(blocks[c(2,'d','i')],3,1,6))
    rows[c(2,'d','ii')][0]['contextNote']+=' Original NOTE: Repetition will not score.'
    put(c(3,'a','i'),1,'1-0',[point('activity','Name of activity',1,'Name ONE LCVP team activity actually participated in. The source gives no personal example; none is invented.')])
    put(c(3,'a','ii'),3,'1-0',[point('role','State role',1),point('explanation','explain role in activity',2,'Explain the role in the SAME activity named in(i); original 3 marks (1+2), no internal 1 mark explanation step printed. No invented personal model.')])
    agenda_pool=numbered(select(blocks[c(3,'b')],'Heading - Agenda 1 mark','5 x 1 mark'),8)
    put(c(3,'b'),6,'1-0',[point('heading','Heading - Agenda',1),*explicit_menu('Agenda items',agenda_pool,5,'FIVE relevant agenda items, 1 each, for the first meeting of the SAME activity. Heading 1 is separately required; all 8 original item alternatives retained.')])
    put(c(3,'d','i'),3,'1-0',menu(blocks[c(3,'d','i')],3,1,8))
    rows[c(3,'d','ii')][0]['contextNote']+=' Each explanation must overcome the SAME challenge named in part(i); no fixed model pairing is inferred.'
    put(c(4,'a'),3,'1-1',[point('business','Name of the business',1),criterion('reasons','Two reasons',2,[0,1],
        'TWO reasons for choosing the SAME named local business, 1 each; business name 1 separately. No personal model answer printed or invented.')])
    put(c(4,'b'),8,'1-1',menu(blocks[c(4,'b')],4,2,8))
    skills=work_skills(scheme,blocks[c(4,'d')]);assert len(skills)==13
    put(c(4,'d'),6,'0-0',[criterion('reasons','Three valid reasons YES or NO',3,[0,1,2],
        'THREE explained reasons, 1+1 each; YES or NO accepted, no separate opinion mark. Complete original 12-model pool and Etc, including both original columns: '+' | '.join(skills))])
    put(c(5,'a','i'),2,'1-2',[point('purpose',select(blocks[c(5,'a','i')],'The purpose',include=True),2,'ONE whole purpose response, 2 marks; no internal 1 mark split printed.')])
    put(c(5,'a','ii'),2,'1-2',menu(blocks[c(5,'a','ii')],2,1,5))
    challenges=numbered(select(blocks[c(5,'d')],'Three valid challenges','Describe how these challenges can be overcome'),10)
    put(c(5,'d'),6,'1-2',paired_rows(3,['challenge','description relevant to the challenge'],[1,1],
        'THREE distinct challenges 1 each plus THREE matching descriptions of how they can be overcome 1 each. Keep each solution linked to its challenge. Full original 10-model challenge pool: '+' | '.join(challenges)+'. The scheme prints no completed solution examples; none is invented.'))
    uses=ict_uses(scheme);assert len(uses)==14
    put(c(6,'a'),4,'0-0',explicit_menu('Any relevant answer',uses[:-1],4,'FOUR distinct ICT uses during LCVP, 1 each. Full original 13-model two-column pool retained; the source also prints Etc.'))
    put(c(6,'b'),4,'0-0',[point(f'model-{i}',v,note=(
        'Numeric scoring held. Original conflicting instructions: Two relevant answers; 4 x 1 mark. Employees need to: follows in the source. Paper total 4. All original models retained; confidence review only pending authoritative clarification. No two-answer 2+2 repair, four-answer quota, partial award or tariff precedence inferred.' if i==1 else '')) for i,v in enumerate(numbered(blocks[c(6,'b')],8),1)])
    assert set(rows)==set(blocks)==set(PAGES)
    case=select(tidy(page_raw(paper,9)),'Section B Case Study 30 marks')
    stems={n:tidy(re.sub(r'^Q\.\s*\d+\s*|\(25\s+marks\)','',page_raw(paper,16+(n-1)*3).split('(a)',1)[0])) for n in range(1,7)}
    cards=[]
    for key in blocks:
        section,q,letter,roman=key;suffix=section.lower()+str(q)+(letter or '')+(roman or '')
        ref=f'2019 CL Section {section} Q{q}'+(f'({letter})' if letter else '')+(f'({roman})' if roman else '')
        card=dict(id='lcvp-2019-cl-'+suffix,subjectId='lcvp',topicId='lcvp-link-modules-'+topics[key],conceptId=concept_id('lcvp-2019-cl-'+suffix,suffix),
            level='common',year=2019,section=section,questionRef=ref,questionText=question(paper,key),stem=stems[q] if section=='C' else case if section=='B' else '',
            figureKey='',labelKey=[],totalMarks=totals[key],rows=rows[key],tariffModel=dict(kind='questionTotal' if key in HELD_KEYS else 'fixed',notation='Original 2019 allocation; C6(b) conflicting count held'),sourceMaterial=source([PAGES[key]]))
        if section=='A':
            card['videoMaterial']=dict(kind='source-video',label='OFFICIAL VIDEO',title='2019 LCVP audiovisual examination',playbackUrl=VIDEO_URL,canonicalUrl=VIDEO_URL,secFileid='LC462CLP031EV.mp4',
                attribution='State Examinations Commission — original 2019 Common Level English audiovisual recording.',presentationNote='Watch the original Apprenticeship sequence with its sound before answering. Follow the printed viewing instructions. Use the original source link if embedded playback is unavailable.')
            card['additionalSourceMaterials']=[source([3],title='Original audiovisual instructions')]
        elif section=='B':
            card['sourceMaterial']=source([9],'source-text','Ballytiernan Community Co-operative — complete case study');card['additionalSourceMaterials']=[source([PAGES[key]])]
            if q==3:card['stem']+=' '+select(tidy(page_raw(paper,12)),'Q.3','(i)')
        if section=='C' and (q,letter) in [(1,'d'),(3,'d')]:card['stem']+=' '+select(tidy(page_raw(paper,PAGES[key])),'(d)','(i)')
        previous={b(2,'iii'):b(2,'ii'),b(3,'ii'):b(3,'i'),c(3,'a','ii'):c(3,'a','i'),c(3,'b'):c(3,'a','i'),c(3,'d','ii'):c(3,'d','i')}.get(key)
        if previous:card['stem']+=' '+question(paper,previous)
        cards.append(card)
    assert len(cards)==45 and sum(c['totalMarks'] for c in cards)==210
    return cards,scheme


def write(cards,scheme):
    path=ROOT/'scripts/markbank/authored/lcvp.json';old=json.loads(path.read_text())
    prior=[c for c in old if c['year']==2019];preserved=[c for c in old if c['year']!=2019]
    assert len(preserved)==345 and len(prior) in [39,45]
    assert {c['id'] for c in prior}<={c['id'] for c in cards}
    assert {c['id'] for c in cards}-{c['id'] for c in prior} in [set(),ADDED_IDS]
    concepts={c['id']:c['conceptId'] for c in prior};assert all(c['conceptId']==concepts.get(c['id'],c['conceptId']) for c in cards)
    result=[];inserted=False
    for card in old:
        if card['year']==2019:
            if not inserted:result.extend(cards);inserted=True
        else:result.append(card)
    assert [c for c in result if c['year']!=2019]==preserved
    path.write_text(json.dumps(result,ensure_ascii=False,indent=1)+'\n')
    pages=[]
    for i,page in enumerate(scheme,1):
        value=f'## Physical page {i}\n\n'+page.get_text(sort=True)
        if i==8:value+='\n\n### Original CV-heading column order\n\n'+'\n'.join(cv_headings(scheme))
        if i==14:value+='\n\n### Original work-skills column order\n\n'+'\n'.join(column_tail(scheme,14,5,10,13))
        if i==17:value+='\n\n### Original ICT-use column order\n\n'+'\n'.join(ict_uses(scheme))
        pages.append(value)
    text='# SEC LCVP 2019 Common Level written marking scheme\n\n'+'\n\n'.join(pages)
    (ROOT/'examiner-reports/lcvp/schemes/2019-cl.md').write_text('\n'.join(line.rstrip() for line in text.splitlines()).rstrip()+'\n')
    review=json.loads(REVIEW.read_text());review['status']='source-authored; independent-sweep-complete; validation-pending'
    review['tasks']=[dict(id=c['id'],questionRef=c['questionRef'],marks=c['totalMarks'],topicId=c['topicId']) for c in cards]
    review['legacyCorrections']=dict(retainedStableIds=39,retainedOriginalConceptIds=39,addedIds=sorted(ADDED_IDS),previousPrintedMarks=185,correctedPrintedMarks=210,
        correctedExistingTariff='B3(i) restores separately printed name1+reason2: previous2→3.',canonicalTopics='Reviewed against canonical registry; originalIDs/concepts and Atlas identities retained.')
    review['heldNumericScoring']=[dict(id='lcvp-2019-cl-c6b',marks=4,reason='Two relevant answers vs4x1mark; independently confirmed by root')]
    REVIEW.write_text(json.dumps(review,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':
    cards,scheme=build()
    if '--write' in sys.argv:write(cards,scheme)
    else:print(json.dumps(cards,ensure_ascii=False,indent=2))
