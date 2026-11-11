#!/usr/bin/env python3
"""Original-source selectors following the independent 66-page 2021 sweep."""
import hashlib
import json
import re
import sys
import fitz
from lcvp_review_2026 import ROOT, tidy, select, numbered, point, criterion, menu, partial
from lcvp_review_2025 import paired_rows
from lcvp_review_2024 import split_raw
from lcvp_review_2022 import page_raw, lines_between, explicit_menu, line_numbered, char_text
from lcvp_identity import concept_id

REVIEW = ROOT / 'scripts/markbank/authoring/lcvp/2021-cl-main-review.json'
PAPER = 'paper-trail-corpus/exampapers/2021/LC462CLP000EV.pdf'
SCHEME = 'paper-trail-corpus/markingschemes/2021/LC462CLP000EV.pdf'
HASHES = {PAPER: '483769937547e57f5de2e552b0b850efb929cb1cfc3bf67fdc421665b6ea6445',
          SCHEME: '3ac15fb1ca2dc4c37401c3f5d9472323c51d07e04e285bd16905469efe37ca98'}
ADDED_IDS = {'lcvp-2021-cl-' + key for key in ['a6i', 'a6ii', 'c2a', 'c2b', 'c5c']}
VIDEO_URL = 'https://www.examinations.ie/archive/exampapers/2021/LC462CLP031EV.mov'


def documents():
    for path, expected in HASHES.items():
        assert hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == expected
    return fitz.open(ROOT / PAPER), fitz.open(ROOT / SCHEME)


def scheme_parts(doc, raw=False):
    sections = split_raw('\n'.join(page_raw(doc, n) for n in range(4, 23)),
                         r'^\s*Section ([ABC])\s+', list('ABC'))
    out = {}
    for section, value in sections.items():
        pattern = r'^\s*Q\.\s*(\d+)\s*'
        if section == 'C':
            pattern += r'(?=Learning about|Work experience|My Own Place|Ireland has|Entrepreneurs are|Effective leadership|A business wants)'
        questions = split_raw(value, pattern,
                              [str(n) for n in range(1, {'A': 8, 'B': 3, 'C': 7}[section] + 1)])
        for q, block in questions.items():
            if section == 'A' and q in ['6','8']:
                boundary = 'Which of these might be more important' if q == '6' else 'Do you agree with Kate’s evaluation'
                assert block.count(boundary) == 1, block
                first, second = block.split(boundary, 1)
                out[(section,int(q),None,'i')] = first
                out[(section,int(q),None,'ii')] = boundary + second
            elif section == 'A' or (section == 'B' and q == '1'):
                out[(section, int(q), None, None)] = block
            elif section == 'B':
                for roman, part in split_raw(block, r'^\s*\((i{1,2})\)\s*', ['i','ii']).items():
                    out[(section, int(q), None, roman)] = part
            else:
                # C1 repeats (d) before (ii); retain the roman boundary once.
                block = re.sub(r'^\s*\(d\)\s*(?=\(ii\))', '', block, flags=re.M)
                for letter, part in split_raw(block, r'^\s*\(([abcd])\)\s*', list('abcd')).items():
                    if (q, letter) in [('1','d'), ('5','d')]:
                        for roman, sub in split_raw(part, r'^\s*\((i{1,2})\)\s*', ['i','ii']).items():
                            out[(section,int(q),letter,roman)] = sub
                    else:
                        out[(section,int(q),letter,None)] = part
    assert len(out) == 45, len(out)
    return out if raw else {k:tidy(v) for k,v in out.items()}


PAGES = {('A', q, None, None): p for q,p in enumerate([4,4,4,5,5,6,7,8],1)}
for q in [6,8]:
    page=PAGES.pop(('A',q,None,None))
    PAGES.update({('A',q,None,r):page for r in ['i','ii']})
PAGES[('B',1,None,None)] = 11
PAGES.update({('B',q,None,r):10+q for q in [2,3] for r in ['i','ii']})
PAGES.update({('C',q,l,None):18+(q-1)*3+{'a':0,'b':0,'c':1,'d':2}[l] for q in range(1,8) for l in 'abcd'})
for q in [1,5]:
    page=PAGES.pop(('C',q,'d',None))
    PAGES.update({('C',q,'d',r):page for r in ['i','ii']})


def question(doc,key):
    section,q,letter,roman=key
    value=page_raw(doc,PAGES[key])
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


def source(pages, kind='source-question', title='Original question'):
    return dict(kind=kind,label='OFFICIAL SOURCE',title=title,pages=pages,
        attribution='SEC LCVP Link Modules 2021 Common Level — © State Examinations Commission.',
        presentationNote='Read the complete original source and question in context.')


def text_lines(page):
    return [(fitz.Rect(line['bbox']),tidy(''.join(s['text'] for s in line['spans'])))
        for block in page.get_text('dict')['blocks'] for line in block.get('lines',[])]


def skill_quality_pools(doc):
    page=doc[4]; lines=text_lines(page)
    heads=[next(box for box,text in lines if text==name) for name in ['EXAMPLES OF SKILLS','EXAMPLES OF QUALITIES']]
    end=next(box.y0 for box,text in lines if text.startswith('Which of these might'))
    split=(heads[0].x1+heads[1].x0)/2
    values=[char_text(page,fitz.Rect(left,max(h.y1 for h in heads),right,end)) for left,right in [(0,split),(split,page.rect.width)]]
    pools=[[tidy(v) for v in value.split('•')[1:]] for value in values]
    assert [len(v) for v in pools]==[8,8],pools
    return pools


def comparison_pairs(doc):
    page=doc[17]; lines=text_lines(page)
    head=next(box for box,text in lines if text=='Business manager')
    left=next(box for box,text in lines if text=='Entrepreneur')
    rows=sorted([(box,text) for box,text in lines if box.y0>left.y1 and box.x0<head.x0 and re.match(r'^\d+\. ',text)],key=lambda v:v[0].y0)
    assert [int(re.match(r'^(\d+)',text)[1]) for _,text in rows]==list(range(1,11))
    split=(max(box.x1 for box,_ in rows)+head.x0)/2
    end=rows[-1][0].y1+1
    pairs=[]
    for i,(box,_) in enumerate(rows):
        upper=box.y0-1; lower=rows[i+1][0].y0-1 if i+1<len(rows) else end
        a=char_text(page,fitz.Rect(0,upper,split,lower));b=char_text(page,fitz.Rect(split,upper,page.rect.width,lower))
        a=re.sub(r'^\d+\.\s*','',a); assert a and b
        pairs.append([a,b])
    assert 'long term' in pairs[6][0] and 'short term' in pairs[6][1]
    return pairs


def single_printed_box(boxes):
    # Original PDF paints inner/outer edges of the same visible frame.
    assert len(boxes) in [1, 2], boxes
    assert all(abs(a - b) < 1 for box in boxes for a, b in zip(box, boxes[0])), boxes
    return max(boxes, key=lambda box: box.width * box.height)


def email_source(doc):
    page=doc[12]
    boxes=[item[1] for path in page.get_drawings() for item in path['items'] if item[0]=='re' and item[1].width>100 and item[1].height>100]
    boxes=[box for box in boxes if 'Summary of marks' in char_text(page,box)]
    box=single_printed_box(boxes); summary=char_text(page,box)
    labels=[tidy(v) for v in re.findall(r'(.+?)\s+1m',select(summary,'Summary of marks','Total'))]
    assert len(labels)==6 and summary.endswith('Total 6m'),summary
    lines=text_lines(page);start=next(b.y0 for b,t in lines if t.startswith('To: principal@'))
    end=next(b.y1 for b,t in lines if t=='Mark Doyle')
    model=char_text(page,fitz.Rect(0,start-1,page.rect.width,end+1),excluded=box)
    assert model.startswith('To: principal@stsenansns.ie') and model.endswith('Mark Doyle')
    return model,labels,summary


def questionnaire_source(doc):
    page = doc[14]
    boxes = [item[1] for path in page.get_drawings() for item in path['items']
             if item[0] == 're' and item[1].width > 300 and item[1].height > 100]
    box = single_printed_box([r for r in boxes if 'Questionnaire' in char_text(page, r)])
    markers = sorted([(r, text) for r, text in text_lines(page)
                      if box.contains(r) and re.fullmatch(r'Q\.\s*[1-8]', text)], key=lambda v: v[0].y0)
    assert [re.sub(r'\s+', '', text) for _, text in markers] == [f'Q.{n}' for n in range(1, 9)]
    centres = [(r.y0 + r.y1) / 2 for r, _ in markers]
    starts = [markers[0][0].y0 - 2] + [(a + b) / 2 for a, b in zip(centres, centres[1:])]
    ends = starts[1:] + [box.y1]
    heading = char_text(page, fitz.Rect(box.x0, box.y0, box.x1, starts[0]))
    rows = []
    for top, bottom in zip(starts, ends):
        clip = fitz.Rect(box.x0, top, box.x1, bottom)
        # Glyph baselines differ slightly across the same printed row. Read
        # its original line fragments left-to-right, retaining every box/word.
        fragments = []
        for block in page.get_text('rawdict')['blocks']:
            for line in block.get('lines', []):
                chars = [char for span in line['spans'] for char in span['chars']
                         if clip.contains(fitz.Point((char['bbox'][0] + char['bbox'][2]) / 2,
                                                     (char['bbox'][1] + char['bbox'][3]) / 2))]
                if chars:
                    fragments.append((min(char['bbox'][0] for char in chars), ''.join(char['c'] for char in chars)))
        rows.append(tidy(' '.join(value for _, value in sorted(fragments))))
    assert all(row.startswith(f'Q.{i}') for i, row in enumerate(rows, 1)), rows
    return heading + ' ' + ' | '.join(rows)


def build():
    paper,scheme=documents();blocks,raw=scheme_parts(scheme),scheme_parts(scheme,raw=True)
    rows,totals,topics={},{},{}
    def put(key,mark,topic,value):rows[key],totals[key],topics[key]=value,mark,topic
    def a(q,r=None):return ('A',q,None,r)
    def b(q,r=None):return ('B',q,None,r)
    def c(q,l,r=None):return ('C',q,l,r)
    job_ads=select(blocks[a(1)],'Agencies', include=True).split('/')
    assert len(job_ads)==4
    put(a(1),1,'0-1',explicit_menu('one way a job may be advertised',job_ads,1))
    for n,count,expected in [(2,2,7),(3,3,7),(4,2,5)]:put(a(n),count,'0-1',menu(blocks[a(n)],count,1,expected))
    put(a(5),4,'0-1',menu(blocks[a(5)],2,2,5))
    pools=skill_quality_pools(scheme)
    put(a(6,'i'),4,'0-1',[criterion('skill','one skill',1,[0,1,2],
        'ONE skill, name1 + explanation1; keep the explanation tied to Mark’s interview. Complete original skill pool: '+' | '.join(pools[0])),
        criterion('quality','one quality',1,[0,1,2],
        'ONE quality, name1 + explanation1; both skill and quality are required. Complete original quality pool: '+' | '.join(pools[1]))])
    put(a(6,'ii'),2,'0-1',[criterion('linked-reason','One valid reason linked to the skill or quality discussed in part (i)',1,[0,1,2],
        'ONE linked reason,1+1. It must concern the SAME skill or quality selected in part(i); the source supplies no completed personal explanation and none is invented.')])
    put(a(7),6,'0-0',partial(blocks[a(7)],3,2,7))
    put(a(8,'i'),2,'0-1',menu(blocks[a(8,'i')],2,1,7))
    put(a(8,'ii'),4,'0-1',partial(blocks[a(8,'ii')],2,2,7,
        'Retain the printed evaluation/opinion question. No separate agreement mark or invented dissent model is added.'))
    definitions=split_raw(raw[b(1)],r'^\s*\((i|ii|iii|iv)\)\s*',['i','ii','iii','iv'])
    put(b(1),6,'1-1',[criterion('definitions','Explain three of the following terms',3,[0,1,2],
        'Choose THREE of the FOUR printed definitions,1+1 each. Full original models: '+' | '.join(tidy(v) for v in definitions.values()))])
    put(b(2,'i'),3,'1-1',menu(blocks[b(2,'i')],3,1,9))
    put(b(2,'ii'),6,'1-1',partial(blocks[b(2,'ii')],3,2,7,
        'THREE distinct marketing headings, each heading1 + matching case-applied content1. All SEVEN original section pools across both pages are retained.'))
    put(b(3,'i'),4,'1-1',paired_rows(2,['challenges','ways to overcome'],[1,1],
        'TWO challenge/solution pairs: challenge1 + matching way to overcome1. Complete original14 challenge models: '+' | '.join(numbered(blocks[b(3,'i')],14))+
        ' The source prints no separate model solutions; none is invented.'))
    put(b(3,'ii'),6,'1-1',partial(blocks[b(3,'ii')],3,2,10))
    ways=lines_between(raw[c(1,'a')],'Class discussion',expected=7)
    put(c(1,'a'),2,'1-1',[criterion('decision','One valid answer',1,[0,1,2],
        'ONE explained decision method,1+1. Complete original examples: '+' | '.join(ways))])
    specs=[(1,'b',3,2,8,'1-1'),(1,'c',4,2,7,'1-1'),(2,'c',3,2,10,'0-0'),(2,'d',3,3,11,'0-3'),
           (3,'d',3,3,7,'1-4'),(4,'c',4,2,8,'0-0'),(4,'d',3,3,12,'0-0'),
           (6,'b',2,2,13,'1-0'),(6,'c',4,2,16,'1-0'),(6,'d',3,3,9,'1-0'),
           (7,'b',3,2,8,'1-1'),(7,'c',3,2,7,'1-1'),(7,'d',3,3,16,'1-1')]
    for q,l,count,per,expected,topic in specs:put(c(q,l),count*per,topic,partial(blocks[c(q,l)],count,per,expected))
    headings=lines_between(raw[c(1,'d','i')],'Title',expected=7)
    put(c(1,'d','i'),3,'0-4',explicit_menu('Three headings',headings,3))
    put(c(1,'d','ii'),6,'0-4',partial(blocks[c(1,'d','ii')],3,2,9))
    put(c(2,'a'),4,'0-3',[point('placement','Name of employer/placement',2,
        'Name ONE employer/placement,2marks as printed; no internal1mark step. Both following reasons refer to this SAME placement.'),
        criterion('reasons','Two valid reasons',2,[0,1],'TWO reasons for choosing the SAME named employer/placement,1each. No personal model answer is printed or invented.')])
    model,labels,_=email_source(scheme)
    put(c(2,'b'),6,'0-3',[point(f'email-{i}',label,1,
        'SIX required email components,1each. No extra marks for availability or dates. Complete original model: '+model if i==1 else '') for i,label in enumerate(labels,1)])
    rows[c(2,'c')][0]['contextNote']+=' These are the original historical examination examples; their printed figures are retained exactly.'
    put(c(3,'a'),4,'1-4',menu(blocks[c(3,'a')],4,1,15))
    benefits=numbered(select(blocks[c(3,'b')],'Two Advantages','Two Disadvantages'),6)
    drawbacks=numbered(select(blocks[c(3,'b')],'Two Disadvantages'),9)
    mr=[]
    for name,values in [('Advantages',benefits),('Disadvantages',drawbacks)]:
        row=explicit_menu(name,values,2,'TWO from this category,1each. The other category is separately required.')[0];row['id']=name.lower();mr.append(row)
    put(c(3,'b'),4,'1-4',mr)
    questionnaire=questionnaire_source(scheme)
    put(c(3,'c'),8,'1-4',[point('heading','heading',1),point('styles','variety of question styles',1),point('instructions','instructions',1),
        criterion('questions','5 questions required',5,[0,1],
        'FIVE distinct relevant questions,1each, alongside the three separately priced layout components. Complete original eight-question model with all printed choices: '+questionnaire)])
    definition=select(blocks[c(4,'a')],'There is',include=True)
    put(c(4,'a'),4,'0-0',[point('mix','mix of people',2,
        'The source underlines the required phrase mix of people and allocates2marks to it; no1partial is printed. Complete original explanation: '+definition),
        criterion('examples','2 examples',2,[0,1],'TWO examples,1each, from the complete original definition above; do not count the required opening phrase again.')])
    put(c(4,'b'),4,'0-0',[criterion('definition',select(blocks[c(4,'b')],'Equal opportunity',include=True),2,[0,2],
        'TWO valid points,2each; no1mark step or compulsory internal semantic split is printed.')])
    put(c(5,'a'),4,'1-0',menu(blocks[c(5,'a')],4,1,8))
    pairs=comparison_pairs(scheme)
    put(c(5,'b'),6,'1-0',paired_rows(3,['Entrepreneur','Business manager'],[1,1],
        'THREE paired comparisons,1+1; contrast may be implicit or explicit. Preserve the original column/line placement, including Has at the end of the ninth manager line. Complete TEN pairs: '+' | '.join(' → '.join(v) for v in pairs)))
    skills=select(blocks[c(5,'c')],'Communication skills -',include=True)
    put(c(5,'c'),6,'1-0',[criterion('skills','Explain why three of these skills are important for entrepreneurs.',3,[0,1,2],
        'Choose THREE distinct named skills from the FOUR printed choices, each1+1. Keep each explanation with its named skill; no combinations or repeated skill. Complete original cross-page pools: '+skills)])
    put(c(5,'d','i'),3,'1-0',menu(blocks[c(5,'d','i')],3,1,5))
    put(c(5,'d','ii'),6,'1-0',partial(blocks[c(5,'d','ii')],3,2,9))
    put(c(6,'a'),4,'1-0',[criterion('reasons',select(blocks[c(6,'a')],'(0/2)'),2,[0,2],
        'TWO reasons,2or0each as explicitly printed. No1mark step is permitted; keep the complete original explanation.')])
    put(c(7,'a'),4,'1-1',menu(blocks[c(7,'a')],2,2,10))
    assert set(rows)==set(blocks)==set(PAGES)
    case=select(tidy(page_raw(paper,10)),'Section B Case Study 25 marks')
    stems={n:tidy(re.sub(r'^Q\.\s*\d+\s+25\s+marks\s*','',page_raw(paper,18+(n-1)*3).split('(a)',1)[0])) for n in range(1,8)}
    cards=[]
    for key in blocks:
        section,q,letter,roman=key;suffix=section.lower()+str(q)+(letter or '')+(roman or '')
        ref=f'2021 CL Section {section} Q{q}'+(f'({letter})' if letter else '')+(f'({roman})' if roman else '')
        card=dict(id='lcvp-2021-cl-'+suffix,subjectId='lcvp',topicId='lcvp-link-modules-'+topics[key],conceptId=concept_id('lcvp-2021-cl-'+suffix,suffix),
            level='common',year=2021,section=section,questionRef=ref,questionText=question(paper,key),stem=stems[q] if section=='C' else case if section=='B' else '',
            figureKey='',labelKey=[],totalMarks=totals[key],rows=rows[key],tariffModel=dict(kind='fixed',notation='Original 2021 allocation; complete source guidance retained'),sourceMaterial=source([PAGES[key]]))
        if section=='A':
            card['videoMaterial']=dict(kind='source-video',label='OFFICIAL VIDEO',title='2021 LCVP audiovisual examination',playbackUrl=VIDEO_URL,canonicalUrl=VIDEO_URL,secFileid='LC462CLP031EV.mov',
                attribution='State Examinations Commission — original 2021 Common Level English audiovisual recording.',presentationNote='Watch the original interviewing-for-a-job sequence with its sound before answering. Follow the printed viewing instructions. Use the original source link if embedded playback is unavailable.')
            card['additionalSourceMaterials']=[source([3],title='Original audiovisual instructions')]
            if q==6:
                card['stem']='People are born with qualities but can learn skills.'
                if roman=='ii':card['stem']+=' '+question(paper,a(6,'i'))
        elif section=='B':
            card['sourceMaterial']=source([10],'source-text','Grosvenor Hotel — complete case study');card['additionalSourceMaterials']=[source([PAGES[key]])]
        cards.append(card)
    assert len(cards)==45 and sum(c['totalMarks'] for c in cards)==230
    return cards,scheme


def write(cards,scheme):
    path=ROOT/'scripts/markbank/authored/lcvp.json';old=json.loads(path.read_text())
    prior=[c for c in old if c['year']==2021];preserved=[c for c in old if c['year']!=2021]
    assert len(preserved)==336 and len(prior) in [40,45]
    assert {c['id'] for c in prior}<={c['id'] for c in cards}
    assert {c['id'] for c in cards}-{c['id'] for c in prior} in [set(),ADDED_IDS]
    concepts={c['id']:c['conceptId'] for c in prior}
    assert all(c['conceptId']==concepts.get(c['id'],c['conceptId']) for c in cards)
    result=[];inserted=False
    for card in old:
        if card['year']==2021:
            if not inserted:result.extend(cards);inserted=True
        else:result.append(card)
    assert [c for c in result if c['year']!=2021]==preserved
    path.write_text(json.dumps(result,ensure_ascii=False,indent=1)+'\n')
    pages=[]
    for i,page in enumerate(scheme,1):
        value=f'## Physical page {i}\n\n'+page.get_text(sort=True)
        if i==5:value+='\n\n### Original separate skill/quality columns\n\n'+'\n'.join(' | '.join(v) for v in skill_quality_pools(scheme))
        if i==13:
            model,_,summary=email_source(scheme);value+='\n\n### Original email outside its mark box\n\n'+model+'\n\n'+summary
        if i==15:value+='\n\n### Original questionnaire\n\n'+questionnaire_source(scheme)
        if i==18:value+='\n\n### Original comparison columns\n\n'+'\n'.join(' | '.join(v) for v in comparison_pairs(scheme))
        pages.append(value)
    text='# SEC LCVP 2021 Common Level written marking scheme\n\n'+'\n\n'.join(pages)
    (ROOT/'examiner-reports/lcvp/schemes/2021-cl.md').write_text('\n'.join(line.rstrip() for line in text.splitlines()).rstrip()+'\n')
    review=json.loads(REVIEW.read_text());review['status']='source-authored; independent-sweep-complete; validation-pending'
    review['tasks']=[dict(id=c['id'],questionRef=c['questionRef'],marks=c['totalMarks'],topicId=c['topicId']) for c in cards]
    review['legacyCorrections']=dict(retainedStableIds=40,retainedOriginalConceptIds=40,addedIds=sorted(ADDED_IDS),previousPrintedMarks=206,correctedPrintedMarks=230,
        correctedExistingTariff='B3(i) previously lost the TWO matching ways-to-overcome marks:2→4. Source explicitly gives two challenges1each and two matching ways1each.',canonicalTopics='Reviewed against canonical registry; original IDs/concepts and Atlas identities retained.')
    review['heldNumericScoring']=[];REVIEW.write_text(json.dumps(review,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':
    cards,scheme=build()
    if '--write' in sys.argv:write(cards,scheme)
    else:print(json.dumps(cards,ensure_ascii=False,indent=2))
