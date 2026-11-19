#!/usr/bin/env python3
"""Source selectors after the independent 58-page 2020 visual sweep."""
import hashlib
import json
import re
import sys
import fitz
from lcvp_review_2026 import ROOT, tidy, select, numbered, point, criterion, menu, partial
from lcvp_review_2024 import split_raw
from lcvp_review_2022 import page_raw, explicit_menu, char_text
from lcvp_identity import concept_id

REVIEW = ROOT / 'scripts/markbank/authoring/lcvp/2020-cl-main-review.json'
PAPER = 'paper-trail-corpus/exampapers/2020/LC462CLP000EV.pdf'
SCHEME = 'paper-trail-corpus/markingschemes/2020/LC462CLP000EV.pdf'
HASHES = {PAPER:'2834437686d332ead96ce729989f46b8018dd2b3348914b5e55c45a9beeeef37',
          SCHEME:'64a81c98ffb5ac3bd511c23e4f0215c8c5a06430c7332496123d8adcd9cf90c4'}
ADDED_IDS = {'lcvp-2020-cl-' + key for key in ['c5c','c6di','c6dii']}
VIDEO_URL = 'https://www.examinations.ie/archive/exampapers/2020/LC462CLP031EV.mp4'
SPLIT_C = {(1,'d'),(2,'a'),(3,'d'),(4,'a'),(5,'a'),(6,'d')}
HELD_KEYS = {('C',3,'a',None),('C',5,'a','i')}


def documents():
    for path, expected in HASHES.items():
        assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==expected,path
    return fitz.open(ROOT/PAPER),fitz.open(ROOT/SCHEME)


def scheme_parts(doc,raw=False):
    sections=split_raw('\n'.join(page_raw(doc,n) for n in range(4,21)),r'^\s*Section ([ABC])\s+',list('ABC'))
    out={}
    for section,value in sections.items():
        # A/B reprint Q6/Q7/Q8/Q2/Q3 before the second roman part.
        value=re.sub(r'^\s*Q\.\s*\d+\s*(?=\(ii\))','',value,flags=re.M)
        questions=split_raw(value,r'^\s*Q\.\s*(\d+)\s*',[str(n) for n in range(1,{'A':8,'B':3,'C':6}[section]+1)])
        for q,block in questions.items():
            if section=='A' and int(q) in [6,7,8]:
                for roman,part in split_raw(block,r'^\s*\((i{1,2})\)\s*',['i','ii']).items():out[(section,int(q),None,roman)]=part
            elif section=='A' or(section=='B' and q=='1'):out[(section,int(q),None,None)]=block
            elif section=='B':
                for roman,part in split_raw(block,r'^\s*\((i{1,2})\)\s*',['i','ii']).items():out[(section,int(q),None,roman)]=part
            else:
                for letter,part in split_raw(block,r'^\s*\(([abcd])\)\s*',list('abcd')).items():
                    if (int(q),letter)==(6,'d'):
                        # Both prompts precede both separate tariffs and the same coherent pool.
                        for roman in ['i','ii']:out[(section,6,letter,roman)]=part
                    elif (int(q),letter) in SPLIT_C:
                        for roman,sub in split_raw(part,r'^\s*\((i{1,2})\)\s*',['i','ii']).items():out[(section,int(q),letter,roman)]=sub
                    else:out[(section,int(q),letter,None)]=part
    assert len(out)==46,len(out)
    return out if raw else {k:tidy(v) for k,v in out.items()}


PAGES={('A',q,None,None):p for q,p in enumerate([4,4,4,5,5,6,7,8],1)}
for q in [6,7,8]:
    page=PAGES.pop(('A',q,None,None));PAGES.update({('A',q,None,r):page for r in ['i','ii']})
PAGES[('B',1,None,None)]=10
PAGES.update({('B',q,None,r):9+q for q in [2,3] for r in ['i','ii']})
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
        value=re.split(r'^\s*\(i{1,2}\)\s*',value,maxsplit=1,flags=re.M)[0]
    return tidy(re.sub(r'\(\d+\s+marks?\)','',value))


def source(pages,kind='source-question',title='Original question'):
    return dict(kind=kind,label='OFFICIAL SOURCE',title=title,pages=pages,
        attribution='SEC LCVP Link Modules 2020 Common Level — © State Examinations Commission.',
        presentationNote='Read the complete original source and question in context.')


def definition_pool(raw,names):
    result=[]
    for i,name in enumerate(names):
        assert raw.count(name)==1,(name,raw)
        value=raw.split(name,1)[1]
        if i+1<len(names):value=value.split(names[i+1],1)[0]
        result.append(name+' '+tidy(value))
    return result


def qualities(doc):
    page=doc[11];lines=[(fitz.Rect(line['bbox']),tidy(''.join(s['text'] for s in line['spans']))) for block in page.get_text('dict')['blocks'] for line in block.get('lines',[])]
    # Select the two actual columns of the qualities list, bounded by its headings.
    top=next(box.y1 for box,t in lines if 'Two valid answers'==t)
    bottom=next(box.y0 for box,t in lines if t.startswith('(b)'))
    starts=[box.x0 for box,t in lines if top<box.y0<bottom and re.match(r'^[15]\. ',t)]
    assert len(starts)==2,starts
    split=max(starts)-8
    left=char_text(page,fitz.Rect(0,top,split,bottom));right=char_text(page,fitz.Rect(split,top,page.rect.width,bottom))
    result=numbered(left+' '+right,8)
    assert result[0]=='Willing to take a risk.' and result[-1]=='Decisive.'
    return result


def promotion_pairs(doc):
    page=doc[7]
    lines=[(fitz.Rect(line['bbox']),tidy(''.join(s['text'] for s in line['spans']))) for block in page.get_text('dict')['blocks'] for line in block.get('lines',[])]
    start=next(box.y0 for box,text in lines if text.startswith('1.') and 'Create a memorable' in text)
    end=next(box.y0 for box,text in lines if text.startswith('11.') and 'Etc.' in text)
    rows=sorted([(box,text) for box,text in lines if start<=box.y0<end and re.match(r'^\d+\.\s*',text)],key=lambda v:v[0].y0)
    assert [int(re.match(r'^(\d+)',text)[1]) for _,text in rows]==list(range(1,11))
    right=next(box.x0 for box,text in lines if text.startswith('this will get the business'))
    split=right-3;pairs=[]
    for i,(box,_) in enumerate(rows):
        top=box.y0-1;bottom=rows[i+1][0].y0-1 if i+1<len(rows) else end-1
        left=char_text(page,fitz.Rect(0,top,split,bottom));advantage=char_text(page,fitz.Rect(split,top,page.rect.width,bottom))
        left=re.sub(r'^\d+\.\s*','',left);assert left and advantage
        pairs.append([left,advantage])
    return pairs


def build():
    paper,scheme=documents();blocks,raw=scheme_parts(scheme),scheme_parts(scheme,raw=True)
    rows,totals,topics={},{},{}
    def put(key,mark,topic,value):rows[key],totals[key],topics[key]=value,mark,topic
    def a(q,r=None):return ('A',q,None,r)
    def b(q,r=None):return ('B',q,None,r)
    def c(q,l,r=None):return ('C',q,l,r)
    evidence=tidy(re.sub(r'\b1 mark\b','',select(blocks[a(1)],'She knows',include=True)))
    assert evidence.count('She is')==1
    first,second=evidence.split('She is',1)
    put(a(1),1,'1-2',explicit_menu('What evidence is there that Denise is environmentally aware?',[tidy(first),'She is'+second],1,
        'ONE valid piece of evidence,1mark; both original alternatives are retained.'))
    for q,count,expected in [(2,2,4),(3,3,4),(4,3,5),(5,4,4)]:put(a(q),count,'1-0',menu(blocks[a(q)],count,1,expected))
    put(a(6,'i'),4,'1-0',menu(blocks[a(6,'i')],4,1,4))
    put(a(6,'ii'),1,'1-0',menu(blocks[a(6,'ii')],1,1,5))
    put(a(7,'i'),4,'1-0',partial(blocks[a(7,'i')],2,2,6))
    put(a(7,'ii'),2,'1-0',menu(blocks[a(7,'ii')],2,1,7))
    rows[a(7,'ii')][0]['contextNote']+=' Preserve the opinion/reasons wording and all positive/negative source examples; no separate opinion mark is printed.'
    put(a(8,'i'),4,'1-0',partial(blocks[a(8,'i')],2,2,11,
        'TWO comparisons,1+1each. The source lists only well-run meeting features; retain the badly-run comparison requirement without inventing a second model column.'))
    put(a(8,'ii'),2,'1-0',menu(blocks[a(8,'ii')],2,1,7))
    definitions=definition_pool(raw[b(1)],['Mentor:','Bookkeeping:','Sole trader:','Upskill:'])
    put(b(1),6,'1-1',[criterion('definitions','Explain three of the following terms',3,[0,1,2],
        'Choose THREE of FOUR original terms,1+1each; all four labels/models remain available. Complete original models: '+' | '.join(definitions))])
    put(b(2,'i'),6,'1-1',partial(blocks[b(2,'i')],3,2,4))
    pairs=promotion_pairs(scheme)
    put(b(2,'ii'),6,'1-1',[criterion('promotion','Three valid answers',3,[0,1,2],
        'THREE distinct methods with the advantage of EACH chosen method;1+1each. Full original paired models: '+' | '.join(' → '.join(p) for p in pairs)+' | Etc.')])
    topics_pool=definition_pool(raw[b(3,'i')],['Sole trader or PLC:','Professional indemnity:','Employers insurance:','Health and safety legislation:','Location:','Staff requirements:'])
    put(b(3,'i'),6,'1-1',[criterion('topics','Three valid answers',3,[0,1,2],
        'THREE mentor-discussed topics OTHER THAN promotion,1+1each. Keep the complete cross-page pools and application to Jim: '+' | '.join(topics_pool))])
    put(b(3,'ii'),6,'1-1',partial(blocks[b(3,'ii')],3,2,6))
    terms=definition_pool(raw[c(1,'a')],['Problem Solving:','Flexible Working Hours:','Referees:','Equal Opportunities Employer:'])
    put(c(1,'a'),4,'0-1',[criterion('terms','Two terms explained',2,[0,1,2],
        'Choose TWO of the FOUR underlined advert terms,1+1each. The complete original advert and all four definitions are retained: '+' | '.join(terms))])
    put(c(1,'b'),4,'0-0',menu(blocks[c(1,'b')],4,1,12))
    put(c(1,'c'),8,'0-0',partial(blocks[c(1,'c')],4,2,8))
    put(c(1,'d','i'),6,'0-1',partial(blocks[c(1,'d','i')],3,2,5))
    put(c(1,'d','ii'),3,'0-1',menu(blocks[c(1,'d','ii')],3,1,7))
    put(c(2,'a','i'),2,'1-0',[criterion('definition',select(blocks[c(2,'a','i')],'This is',include=True),2,[0,1],
        'Original allocation2x1mark. Explain the term using two valid pieces from the whole source definition; no invented compulsory semantic split.')])
    put(c(2,'a','ii'),2,'1-0',explicit_menu('Two valid answers',qualities(scheme),2))
    put(c(2,'b'),4,'1-0',menu(blocks[c(2,'b')],2,2,5))
    put(c(2,'c'),8,'1-0',partial(blocks[c(2,'c')],4,2,10,
        'The paper requires advantages AND disadvantages. Four responses total,1+1each, with both categories represented; the source gives no fixed category quota such as two-and-two.'))
    put(c(2,'d'),9,'1-0',partial(blocks[c(2,'d')],3,3,10))
    for key,mark,topic,expected,literal in [(c(3,'a'),4,'0-3',8,'Four valid points; 2 x 2 mark (1+1)'),(c(5,'a','i'),2,'1-0',7,'Three points; 2 x 1 mark')]:
        put(key,mark,topic,[point(f'model-{i}',value,note=(
            f'Numeric scoring held. Original conflicting instructions: {literal}. The total is {mark}, but the response count and allocation disagree. '
            'Compare the complete response with all original models; confidence review only pending authoritative clarification. No quota, partial ladder or numeric claim is inferred.' if i==1 else ''))
            for i,value in enumerate(numbered(blocks[key],expected),1)])
    for q,l,r,count,per,expected,topic in [(3,'b',None,3,2,7,'0-3'),(3,'c',None,3,2,9,'0-3'),(3,'d','i',3,2,6,'0-3'),
        (4,'b',None,3,2,12,'0-2'),(4,'c',None,3,2,7,'0-0'),(5,'b',None,3,2,7,'1-0'),(5,'d',None,4,2,7,'1-0'),
        (6,'b',None,3,2,7,'1-3'),(6,'c',None,3,2,8,'1-3')]:put(c(q,l,r),count*per,topic,partial(blocks[c(q,l,r)],count,per,expected))
    rows[c(5,'d')][0]['contextNote']+=' Every method must include its OWN reason. Preserve all seven complete method/reason pools, including the continuation page.'
    put(c(3,'d','ii'),3,'0-3',menu(blocks[c(3,'d','ii')],3,1,6))
    rows[c(3,'d','ii')][0]['contextNote']+=' Each solution must address the SAME challenge selected in part(i); retain all six source examples without assigning an unprinted fixed pairing.'
    benefits=numbered(blocks[c(4,'a','i')],4)
    put(c(4,'a','i'),2,'0-2',[point('career','One valid career',1,'Name the career investigated; the source prints no named career example and none is invented.'),
        point('benefit','One valid benefit',1,'ONE benefit of investigating that SAME career. Full source pool: '+' | '.join(benefits))])
    put(c(4,'a','ii'),2,'0-2',menu(blocks[c(4,'a','ii')],2,1,7))
    benefits=numbered(blocks[c(4,'d')],5);profiles=[]
    for i in range(1,4):
        row=criterion(f'benefit-{i}','Three valid benefits',1,[0,1,2,3],
            'THREE distinct benefits. Literal allocation3x3marks(1m+(0/2)): each benefit1 plus explanation2or0; no1mark explanation step. Complete original pool: '+' | '.join(benefits) if i==1 else 'Use a different benefit and its matching explanation, following1+(0/2).')
        row['parts']=[dict(id='benefit',verbatim='Benefit',marks=1,permittedMarks=[0,1]),dict(id='explanation',verbatim='Explanation',marks=2,permittedMarks=[0,2])];profiles.append(row)
    put(c(4,'d'),9,'0-0',profiles)
    put(c(5,'a','ii'),1,'1-0',[point('subject-use',select(blocks[c(5,'a','ii')],'Subject clearly','1 mark',include=True),1,
        'ONE whole criterion: name an LC subject OTHER THAN Link Modules and explain how its skills/knowledge were useful. No internal split or personal model is printed or invented.')])
    email=select(blocks[c(5,'c')],'Email contents')
    labels=re.findall(r'(.+?)\s+1m',select(email,'8 marks'))
    assert len(labels)==6,labels
    labels=[tidy(label) for label in labels]
    assert labels[4].endswith('3 x'),labels
    labels[4]=labels[4].removesuffix('3 x').strip()
    email_rows=[point('email-'+str(i),label,1) if i!=5 else criterion('information',label,3,[0,1],
        'THREE distinct relevant pieces of information about the visit,1each. The scheme prints criteria but no completed email model; none is invented.') for i,label in enumerate(labels,1)]
    email_rows[0]['contextNote']='Eight required marks: address1,subject1,salutation1,purpose1,three information points3,closing1. Complete original allocation: '+email
    put(c(5,'c'),8,'1-0',email_rows)
    put(c(6,'a'),4,'1-3',menu(blocks[c(6,'a')],4,1,6))
    profiles=numbered(blocks[c(6,'d','i')],5)
    put(c(6,'d','i'),6,'1-3',[criterion('items','Three valid items',3,[0,1,2],
        'THREE key business-plan items stated and explained,1+1each. Importance has a separate3-mark task and is not counted again here. All FIVE original coherent item/importance profiles: '+' | '.join(profiles))])
    put(c(6,'d','ii'),3,'1-3',[criterion('importance','Importance of each item',3,[0,1],
        'ONE importance for EACH of the SAME THREE items chosen in part(i),1each. All FIVE original coherent item/importance profiles: '+' | '.join(profiles))])
    assert set(rows)==set(blocks)==set(PAGES)
    case=select(tidy(page_raw(paper,9)),'Section B Case Study 30 marks')
    stems={n:tidy(re.sub(r'^Q\.\s*\d+\s+\(?25\s+marks\)?\s*','',page_raw(paper,16+(n-1)*3).split('(a)',1)[0])) for n in range(1,7)}
    cards=[]
    for key in blocks:
        section,q,letter,roman=key;suffix=section.lower()+str(q)+(letter or '')+(roman or '')
        ref=f'2020 CL Section {section} Q{q}'+(f'({letter})' if letter else '')+(f'({roman})' if roman else '')
        card=dict(id='lcvp-2020-cl-'+suffix,subjectId='lcvp',topicId='lcvp-link-modules-'+topics[key],conceptId=concept_id('lcvp-2020-cl-'+suffix,suffix),
            level='common',year=2020,section=section,questionRef=ref,questionText=question(paper,key),stem=stems[q] if section=='C' else case if section=='B' else '',
            figureKey='',labelKey=[],totalMarks=totals[key],rows=rows[key],tariffModel=dict(kind='questionTotal' if key in HELD_KEYS else 'fixed',notation='Original 2020 allocation; conflicting quotas explicitly held'),sourceMaterial=source([PAGES[key]]))
        if section=='A':
            card['videoMaterial']=dict(kind='source-video',label='OFFICIAL VIDEO',title='2020 LCVP audiovisual examination',playbackUrl=VIDEO_URL,canonicalUrl=VIDEO_URL,secFileid='LC462CLP031EV.mp4',
                attribution='State Examinations Commission — original 2020 Common Level English audiovisual recording.',presentationNote='Watch the original Committee Meetings sequence with its sound before answering. Follow the printed viewing instructions. Use the original source link if embedded playback is unavailable.')
            card['additionalSourceMaterials']=[source([3],title='Original audiovisual instructions')]
        elif section=='B':
            card['sourceMaterial']=source([9],'source-text','Climate Entrepreneur — complete case study');card['additionalSourceMaterials']=[source([PAGES[key]])]
        if section=='C' and q==1:
            card['sourceMaterial']=source([16],'source-question','Complete Manray Technologies job advert')
            if PAGES[key]!=16:card['additionalSourceMaterials']=[source([PAGES[key]])]
            if letter=='d':
                shared=select(tidy(page_raw(paper,18)),'(d)','(i)')
                card['stem']+=' '+shared
        if key in [a(6,'ii'),c(3,'d','ii'),c(6,'d','ii')]:
            previous=(section,q,letter,'i');card['stem']+=' '+question(paper,previous)
        cards.append(card)
    assert len(cards)==46 and sum(c['totalMarks'] for c in cards)==210
    return cards,scheme


def write(cards,scheme):
    path=ROOT/'scripts/markbank/authored/lcvp.json';old=json.loads(path.read_text())
    prior=[c for c in old if c['year']==2020];preserved=[c for c in old if c['year']!=2020]
    assert len(preserved)==338 and len(prior) in [43,46]
    assert {c['id'] for c in prior}<={c['id'] for c in cards}
    assert {c['id'] for c in cards}-{c['id'] for c in prior} in [set(),ADDED_IDS]
    concepts={c['id']:c['conceptId'] for c in prior};assert all(c['conceptId']==concepts.get(c['id'],c['conceptId']) for c in cards)
    result=[];inserted=False
    for card in old:
        if card['year']==2020:
            if not inserted:result.extend(cards);inserted=True
        else:result.append(card)
    assert [c for c in result if c['year']!=2020]==preserved
    path.write_text(json.dumps(result,ensure_ascii=False,indent=1)+'\n')
    pages=[]
    for i,page in enumerate(scheme,1):
        value=f'## Physical page {i}\n\n'+page.get_text(sort=True)
        if i==8:value+='\n\n### Original promotion and matching advantage columns\n\n'+'\n'.join(' | '.join(p) for p in promotion_pairs(scheme))
        if i==12:value+='\n\n### Original separate qualities columns\n\n'+'\n'.join(qualities(scheme))
        pages.append(value)
    text='# SEC LCVP 2020 Common Level written marking scheme\n\n'+'\n\n'.join(pages)
    (ROOT/'examiner-reports/lcvp/schemes/2020-cl.md').write_text('\n'.join(line.rstrip() for line in text.splitlines()).rstrip()+'\n')
    review=json.loads(REVIEW.read_text());review['status']='source-authored; independent-sweep-complete; validation-pending'
    review['tasks']=[dict(id=c['id'],questionRef=c['questionRef'],marks=c['totalMarks'],topicId=c['topicId']) for c in cards]
    review['legacyCorrections']=dict(retainedStableIds=43,retainedOriginalConceptIds=43,addedIds=sorted(ADDED_IDS),previousPrintedMarks=192,correctedPrintedMarks=210,
        correctedExistingTariff='C4(a)(i) restores its separately printed career1+benefit1: previous1→2.',canonicalTopics='Reviewed against canonical registry; original IDs/concepts and Atlas identities retained.')
    review['heldNumericScoring']=[dict(id='lcvp-2020-cl-'+suffix,marks=mark,reason=reason) for suffix,mark,reason in [('c3a',4,'Four valid points vs2x2(1+1)'),('c5ai',2,'Three points vs2x1')]]
    REVIEW.write_text(json.dumps(review,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':
    cards,scheme=build()
    if '--write' in sys.argv:write(cards,scheme)
    else:print(json.dumps(cards,ensure_ascii=False,indent=2))
