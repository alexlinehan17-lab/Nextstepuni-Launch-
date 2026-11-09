#!/usr/bin/env python3
"""2023 Ordinary Russian: original-PDF review, 29 written + 18 listening tasks.

This sitting has 220 written and 100 listening marks. Published alternatives
which share a grid remain one task; the two discourse routes use the existing
answerVariants contract so a student cannot mix the two dialogues.
"""
import hashlib
import json
import re
from pathlib import Path

import fitz
from ru_paper import RuPaper, bag, score
from ru_review_2026_hl import ROOT, squash, page_text as original_page_text, between, bullets, base as higher_base, as_points, mark_range, save_reviewed

FILES = {
    'paper': ('papers/2023-ol-000-paper.pdf', '28b5a7cf5e15f3c2da6f6938f3b2f13abd888eab5dabd16f28b6966fb1e0e4ce'),
    'aural': ('papers/2023-ol-A00-paper.pdf', 'a5ecc7cb74169bcd00d5bc69fe2ce083c96019f449d31515ada7041d2a298b32'),
    'scheme': ('schemes/2023-ol.pdf', 'da5064b6da1f3906e010bf0ae0610add8100a8b00964149bb6d2ca97593e1b5b'),
}


def page_text(doc, page, box=None):
    # Preserve the entire answer area while excluding the running footer.
    return original_page_text(doc, page, box or (20, 30, 580, 740)).replace('\uf0b7','•')


def opened_sources():
    docs = {}
    for key, (relative, digest) in FILES.items():
        path = ROOT / 'examiner-reports/russian' / relative
        assert hashlib.sha256(path.read_bytes()).hexdigest() == digest, path
        docs[key] = fitz.open(path)
    return docs


def base(unit, text, total, pages, scheme_pages, item=None, roman=None):
    card = higher_base(unit, text, total, pages, scheme_pages, item, roman)
    card['id'] = card['id'].replace('2026', '2023').replace('-hl-', '-ol-')
    card['year'] = 2023
    card['level'] = 'ordinary'
    card['questionRef'] = f'2023 OL Section {unit}' + (f' Q{item}' if item is not None else '')
    if roman:
        card['questionRef'] += f'({roman})'
    card['sourceMaterial']['title'] = f'2023 Ordinary Russian — {unit}'
    return card


def question_blocks(text):
    """Read reviewed numbered/roman headings, including continuation romans."""
    pattern = r'^\s*(?:(\d)\s*\.\s*)?\((iv|v|i{1,3})\)\.?\s+|^\s*(\d)\s*\.\s+(?=[A-Z])'
    heads = list(re.finditer(pattern, text, re.M))
    output, item = [], None
    for index, head in enumerate(heads):
        item = int(head.group(1) or head.group(3)) if head.group(1) or head.group(3) else item
        roman = head.group(2)
        block = text[head.end():heads[index + 1].start() if index + 1 < len(heads) else len(text)]
        output.append((item, roman, block))
    return output


def unprice(text):
    return re.sub(r'\b\d+\s*(?:x\s*\d+\s*)?marks?\b', '', text)

def criterion(cid, label, maximum, allowed, guidance, bands=None):
    return {'id': cid, 'label': label, 'maxMarks': maximum, 'permittedMarks': allowed,
            'guidance': guidance, **({'bands': bands} if bands else {})}


def writing(docs):
    S, Q, cards = docs['scheme'], docs['paper'], []
    raw = Q[14].get_text().replace('\u00a0', ' ')
    instructions = squash('Write 3' + between(raw, 'Write 3', '1.'))
    table = Q[14].find_tables().tables[0].extract()
    assert len(table) == 5
    question = instructions + '\n\n' + '\n'.join(squash(row[1]) + ' / ' + squash(row[2]) for row in table)
    source = page_text(S, 12)
    content = squash(between(source, 'Content of each answer', 'Textual coherence'))
    coherence = between(source, 'Textual coherence')
    bands = [{'label': n, 'marks': [int(n)], 'guidance': [squash(text)]}
             for n, text in re.findall(r'(\d) marks\s+(.+?)(?=\d marks|\Z)', coherence, re.S)]
    assert len(bands) == 4
    card = base('SA', question, 30, [15], [12])
    card.pop('rows'); card.pop('tariffModel'); card['kind'] = 'rubric'
    card['rubric'] = {'system': 'language-writing', 'taskRequirements': [
        'Write 3-5 sentences on ONE of the following topics in Russian or English. Each answer should contain three factual details. Marks are awarded for relevant content and textual coherence.',
        'The quality of the English/Russian will only be an assessment factor insofar as it impedes communication.'],
        'criteria': [criterion('content', 'Content', 24, list(range(0, 25, 4)), [content]),
                     criterion('coherence', 'Textual coherence', 6, [0, 2, 4, 6], [], bands)],
        'markingGuideNote': ''}
    cards.append(card)

    raw = Q[15].get_text().replace('\u00a0', ' ')
    instructions = squash('Write 6' + between(raw, 'Write 6', '1.'))
    table = Q[15].find_tables().tables[0].extract()
    assert len(table) == 3
    choices = []
    for row in table:
        for cell in row[1:]:
            choices.append('\n• '.join(squash(part) for part in re.split(r'[\uf0b7•]', cell)))
    question = instructions + '\n\n' + '\n\n'.join(choices)
    source = page_text(S, 14)
    instruction_source = squash(between(page_text(S, 13), 'Write 6-10 sentences', '1. Saoire'))
    instruction_source = 'Write 6-10 sentences ' + instruction_source
    content = squash(between(source, '2 points for content', 'Accuracy and fluency'))
    content = '2 points for content ' + content
    lower_rule = squash('If the answer' + between(source, 'If the answer', 'Put square box'))
    table = next(t.extract() for t in S[13].find_tables().tables if 'Lower E' in str(t.extract()))
    full, lower = [], []
    for row in table[1:]:
        normal, low, description = map(squash, row)
        full.append({'label': normal, 'marks': mark_range(normal), 'guidance': [description]})
        lower.append({'label': low, 'marks': mark_range(low), 'guidance': [description]})
    coherence = between(source, 'Allocate 6 marks for textual coherence:')
    coherent = [{'label': n, 'marks': mark_range(n), 'guidance': [squash(text)]}
                for n, text in re.findall(r'^\s*(\d(?:-\d)?)\s+(.+?)(?=^\s*\d(?:-\d)?\s|\Z)', coherence, re.S | re.M)]
    assert len(coherent) == 5, coherent
    expression = criterion('expression', 'Language + expression', 12, list(range(13)), [], full)
    expression['limits'] = [{'id': 'lower-expression', 'maxMarks': 9,
        'when': {'any': [{'criterionIds': ['content'], 'atMost': 6},
                         {'flag': 'fewer-six-sentences', 'prompt': lower_rule}]},
        'guidance': [lower_rule], 'bands': lower}]
    card = base('EW', question, 30, [16], [13, 14])
    card.pop('rows'); card.pop('tariffModel'); card['kind'] = 'rubric'
    card['rubric'] = {'system': 'language-writing', 'taskRequirements': [squash(instruction_source),
        'No marks are awarded for additional information/content.'],
        'criteria': [criterion('content', 'Communication + content', 12, list(range(0, 13, 2)), [content]),
                     expression, criterion('coherence', 'Textual coherence', 6, list(range(7)), [], coherent)],
        'markingGuideNote': ''}
    cards.append(card)
    return cards

def reading(docs,P):
    S=docs['scheme'];cards=[]
    assert 'Do not penalise answers supplied in Russian.' in squash(page_text(S,2))
    specs=[('IR1',[4,5],[2,3,4],[2,2,2,2,2,1,1],'Language Awareness'),
           ('IR2',[5,6],[6,7],[2,2,1,1,2,2,2],'LANGUAGE AWARENESS'),
           ('CD',[10,11],[12,13,14],[3,2,1,2,1,3,3,2,3],None)]
    for unit,scheme_pages,paper_pages,counts,end in specs:
        source='\n'.join(S[p-1].get_text(clip=fitz.Rect(20,30,580,740)).replace('\uf0b7','•') for p in scheme_pages)
        if unit=='IR2':source=source.split('Q.2')[1]
        if end:source=source.split(end)[0]
        blocks=question_blocks(source);assert len(blocks)==len(counts),(unit,blocks)
        general=re.split(r'\n\s*1\.',source[source.index('Allocate 2 marks for each'):],maxsplit=1)[0].strip()
        if unit=='IR1':general=general.split('24 marks')[0].strip()
        for (item,roman,block),count in zip(blocks,counts):
            candidates=[b for b in P.blocks if b.unit==unit and b.item==item and b.roman==roman and b.side=='R']
            assert len(candidates)==1,(unit,item,roman)
            question=candidates[0].text
            cue,_=block.split('•',1);cue=squash(unprice(cue))
            reworded = (unit,item,roman)==('CD',1,'ii') and question=='What subject did Pavel like at school? Give two details.' and cue=='What subjects did he like at school? Give two details.'
            reworded |= (unit,item,roman)==('CD',3,'ii') and question=='Name three challenges Pavel faced in college.' and cue=='Name three challenges he faced in his first year in college.'
            assert score(bag(question),bag(cue))>=.8 or question.startswith(cue) or reworded,(question,cue)
            extra=[]
            if 'Accept details about the camp' in block:
                block,rule=block.split('Accept details about the camp',1)
                extra.append('Accept details about the camp '+squash(rule))
            answers=bullets(unprice(block))
            if extra:
                example=between(extra[0],'e.g. ‘','’')
                answers.append(example)
            c=as_points(base(unit,question,count*2,paper_pages,scheme_pages,item,roman),answers,count,steps=[0,1,2])
            c['rubric']['taskRequirements']=[squash(general)]+extra
            c['review']['questionPages']=[candidates[0].page+1]
            c['rubric']['markingGuideNote']='Answer in English or Irish. Marking scheme page 2: Do not penalise answers supplied in Russian.'
            if unit=='IR1' and item==3:
                assert answers==['Summer: Olympic / Olympic Village / Sun','All-year: Star / Ambitious / Storm'],answers
                c['rubric']['groups'][0]['label']='One summer camp'
                c['rubric']['groups'][1]['label']='One all-year-round camp'
            cards.append(c)
    assert len(cards)==23 and sum(c['totalMarks'] for c in cards)==88
    return cards


def language_and_matching(docs):
    S,Q,cards=docs['scheme'],docs['paper'],[]
    instruction=squash(page_text(Q,5,(300,30,580,200)))
    instruction=instruction[instruction.index('The following adjective'):]
    table=next(t.extract() for t in S[4].find_tables().tables if 'сценические площадки' in str(t.extract()))
    pairs=[(squash(row[0]),squash(row[1])) for row in table if len(row)==2 and row[0] and row[1]]
    assert len(pairs)==6,pairs
    c=as_points(base('LA1',instruction,6,[5],[5]),[left+' — '+right for left,right in pairs],3)
    cards.append(c)
    text=page_text(Q,8,(300,30,580,775))
    instruction=squash(re.search(r'Write out three.*?script\s*:',text,re.S).group())
    phrases=re.findall(r'^\s*([А-Яа-яЁё][А-Яа-яЁё ]+?)\s+_{5,}',page_text(Q,8),re.M)
    assert len(phrases)==6,phrases
    instruction+='\n\n'+'\n'.join(phrases)
    source=between(page_text(S,6),'2 marks per phrase.')
    guidance=[squash(line) for line in source.splitlines() if squash(line)]
    c=base('LA2',instruction,6,[8],[6]);c.pop('rows');c.pop('tariffModel');c['kind']='rubric'
    c['rubric']={'system':'language-writing','taskRequirements':['Three phrases in handwritten/cursive script.','2 marks per phrase.'],
        'criteria':[{'id':f'phrase-{n}','label':f'Chosen phrase {n}','maxMarks':2,'permittedMarks':[0,1,2],'guidance':guidance} for n in (1,2,3)],'markingGuideNote':''}
    cards.append(c)
    table=next(t.extract() for t in S[6].find_tables().tables if len(t.extract())==10);assert [row[0] for row in table]==['8','1','4','10','6','7','2','9','5','3']
    answers=[squash(row[1])+' — '+squash(row[0]) for row in table]
    question=Q[8].get_text().replace('\u00a0',' ');question=question[question.index('Match the following'):].strip()
    c=as_points(base('MM',question,40,[9],[7]),answers,10)
    for group in c['rubric']['groups']:group['rows'][0]['marks']=4
    cards.append(c)
    raw=Q[9].get_text().replace('\u00a0',' ')
    question=squash('Read through'+between(raw,'Read through','Focail'))
    question+='\n\n'+page_text(Q,10,(20,180,580,775))+'\n\n'+page_text(Q,11)
    c=base('SD',question,20,[10,11],[8,9]);c['kind']='question';variants=[]
    for page,group in [(8,'A'),(9,'B')]:
        spans=[span for block in S[page-1].get_text('dict')['blocks'] if 'lines' in block for line in block['lines'] for span in line['spans'] if span['flags']&16 and span['bbox'][1]>180 and re.search('[А-Яа-яЁё]',span['text'])]
        answers=[squash(span['text']) for span in spans if squash(span['text'])];assert len(answers)==5,(page,answers)
        variants.append({'id':f'group-{group.lower()}','label':f'Group {group}','rows':[{'id':f'gap-{i}','kind':'point','verbatim':answer,'marks':4} for i,answer in enumerate(answers,1)]})
    c['rows']=variants[0]['rows'];c['answerVariants']=variants;cards.append(c)
    return cards


def listening(docs,P):
    S=docs['scheme']
    source='\n'.join(S[p-1].get_text(clip=fitz.Rect(20,30,580,740)).replace('\uf0b7','•') for p in range(15,19))
    sections=re.split(r'SECTION\s+(?:IV|III|II|I)\b',source);assert len(sections)==5
    general=bullets(sections[0]);assert len(general)==4
    asks=P.aural_asks();assert len(asks)==18
    audio=next(row['source'] for row in json.loads((ROOT/'data/russianAudio.json').read_text()) if row['year']==2023)
    cards=[];pages={'L1':[2],'L2':[3],'L3':[4],'L4':[5]}
    prices={'L1':[6,6,9,2,2],'L2':[6,6,6,3,4],'L3':[6,9,6,4],'L4':[6,3,8,8]}
    for index in range(1,5):
        unit=f'L{index}';tasks=[ask for ask in asks if ask[0]==unit];blocks=question_blocks(sections[index])
        assert len(tasks)==len(blocks)==len(prices[unit]),(unit,blocks)
        parsed=[]
        for (_,item,roman,question),(scheme_item,scheme_roman,block),total in zip(tasks,blocks,prices[unit]):
            assert (item,roman)==(scheme_item,scheme_roman)
            block=re.sub(r'^\s*Segment\s+\d+\s*$','',block,flags=re.M)
            cue,_=block.split('•',1)
            tariff=re.search(r'(\d+)\s*x\s*(\d+)\s*marks|(\d+)\s*marks',cue);assert tariff,(unit,item,roman,cue)
            count=int(tariff.group(1)) if tariff.group(1) else 1;price=int(tariff.group(2) or tariff.group(3));assert count*price==total
            cue=squash(unprice(cue));assert score(bag(question),bag(cue))>.8 or squash(question).startswith(cue),(question,cue)
            extra=[];partial=None
            if 'Accept relevant details from' in block:
                block,rule=block.split('Accept relevant details from',1);extra.append('Accept relevant details from '+squash(rule))
            if 'Award 1 mark:' in block:
                block,partial=block.split('Award 1 mark:',1);partial=squash(partial)
            answers=[squash(unprice(answer)) for answer in bullets(block)]
            c=as_points(base(unit,question,total,pages[unit],[14+index],item,roman),answers,count)
            for group in c['rubric']['groups']:group['rows'][0]['marks']=price
            if partial:
                assert (unit,item,roman)==('L4',2,None) and partial=='their name is Bumaga'
                c['rubric']['groups'].append({'id':'surname','label':'Published partial answer','answerCount':1,'rows':[{'id':'partial','text':partial,'marks':1}]})
            if (unit,item,roman)==('L2',1,'i'):
                assert extra==['Accept relevant details from other sections e.g. vegetarian']
                c['rubric']['groups'].append({'id':'vegetarian','label':'Other explicitly accepted detail','answerCount':1,'rows':[{'id':'full','text':'vegetarian','marks':price}]})
            if unit=='L1':topic='russian-0-11' if item==1 else 'russian-0-8' if item==2 else 'russian-0-9'
            elif unit=='L2':topic='russian-0-6' if item==3 and roman=='ii' else 'russian-0-2' if item==2 else 'russian-0-3'
            elif unit=='L3':topic='russian-0-8'
            else:topic='russian-0-1' if item==2 else 'russian-0-5' if item==3 else 'russian-0-7'
            c['topicId']=topic;c['additionalTopicIds']=['russian-1-0'];c['rubric']['taskRequirements']=general+extra
            c['sourceMaterial']['kind']='source-question';c['sourceMaterial']['presentationNote']='Listen to the official recording and answer the printed question. The transcript is not shown before answering.'
            c['audioMaterial']=audio;c['review']['guidancePages']=[15]
            cards.append(c);parsed.append((c,answers,price))
        if unit=='L4':
            # The scheme expressly cross-accepts relevant details in these two
            # answer pools. Preserve their source wording and each task's rate.
            for dest,other in [(0,3),(3,0)]:
                c,_,price=parsed[dest];_,other_answers,_=parsed[other]
                for n,answer in enumerate(other_answers,1):
                    c['rubric']['groups'].append({'id':f'other-segment-{n}','label':f'Accepted from Segment {4 if dest==0 else 1}',
                        'answerCount':1,'rows':[{'id':'full','text':answer,'marks':price}]})
    assert len(cards)==18 and sum(c['totalMarks'] for c in cards)==100
    return cards


def build():
    docs=opened_sources();P=RuPaper(2023,'ol')
    cards=reading(docs,P)+language_and_matching(docs)+writing(docs)+listening(docs,P)
    assert len(cards)==47 and sum(c['totalMarks'] for c in cards)==320
    old_ids={c['id'] for c in json.loads((ROOT/'scripts/markbank/authored/russian.json').read_text())}
    for c in cards:
        if c['id'] in old_ids:c['review']['correctsExisting']=True
    assert sum(c['review'].get('correctsExisting',False) for c in cards)==23
    return cards

if __name__=='__main__':save_reviewed(build())
