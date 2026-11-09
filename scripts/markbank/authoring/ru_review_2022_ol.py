#!/usr/bin/env python3
"""2022 Ordinary Russian: original-PDF review, 24 written + 18 listening tasks.

This sitting has 175 chosen written and 100 listening marks. Published alternatives
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
    'paper': ('papers/2022-ol-000-paper.pdf', 'a706a1a3b4a1898ebe170609a5b699388178b8dd45461a60a546e4381b8882cd'),
    'aural': ('papers/2022-ol-A00-paper.pdf', 'ed8dc696911237310a16ce4e7ed7bc2c16381aecf33ecc78fc976469119796fd'),
    'scheme': ('schemes/2022-ol.pdf', '184ff292e15bf7702b94bdb4e7626d7bfb538bfb948bed4c85ae4efe01df7399'),
}


def page_text(doc, page, box=None):
    # Preserve the entire answer area while excluding the running footer.
    return original_page_text(doc, page, box or (20, 30, 580, 790)).replace('\uf0b7','•')


def opened_sources():
    docs = {}
    for key, (relative, digest) in FILES.items():
        path = ROOT / 'examiner-reports/russian' / relative
        assert hashlib.sha256(path.read_bytes()).hexdigest() == digest, path
        docs[key] = fitz.open(path)
    return docs


def base(unit, text, total, pages, scheme_pages, item=None, roman=None):
    card = higher_base(unit, text, total, pages, scheme_pages, item, roman)
    card['id'] = card['id'].replace('2026', '2022').replace('-hl-', '-ol-')
    card['year'] = 2022
    card['level'] = 'ordinary'
    card['questionRef'] = f'2022 OL Section {unit}' + (f' Q{item}' if item is not None else '')
    if roman:
        card['questionRef'] += f'({roman})'
    card['sourceMaterial']['title'] = f'2022 Ordinary Russian — {unit}'
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
    raw = Q[13].get_text().replace('\u00a0', ' ')
    instructions = squash('Write 3' + between(raw, 'Write 3', '1.'))
    table = Q[13].find_tables().tables[0].extract()
    assert len(table) == 5
    question = instructions + '\n\n' + '\n'.join(squash(row[1]) + ' / ' + squash(row[2]) for row in table)
    source = page_text(S, 12)
    content = squash(between(source, 'Content of each answer', 'Textual coherence'))
    coherence = between(source, 'Textual coherence')
    bands = [{'label': n, 'marks': [int(n)], 'guidance': [squash(text)]}
             for n, text in re.findall(r'(\d) marks?\s+(.+?)(?=\d marks?|\Z)', coherence, re.S)]
    assert len(bands) == 4
    card = base('SA', question, 15, [14], [12])
    card.pop('rows'); card.pop('tariffModel'); card['kind'] = 'rubric'
    card['rubric'] = {'system': 'language-writing', 'taskRequirements': [
        'Write 3-5 sentences on ONE of the following topics in Russian or English. Each answer should contain three factual details. Marks are awarded for relevant content and textual coherence.',
        'The quality of the English/Russian will only be an assessment factor insofar as it impedes communication.'],
        'criteria': [criterion('content', 'Content', 12, list(range(0, 13, 2)), [content]),
                     criterion('coherence', 'Textual coherence', 3, [0, 1, 2, 3], [], bands)],
        'markingGuideNote': ''}
    cards.append(card)

    raw = Q[14].get_text().replace('\u00a0', ' ')
    instructions = squash('Write 6' + between(raw, 'Write 6', '1.'))
    table = Q[14].find_tables().tables[0].extract()
    assert len(table) == 3
    choices = []
    for row in table:
        for cell in row[1:]:
            choices.append('\n• '.join(squash(part) for part in re.split(r'[\uf0b7•]', cell)))
    question = instructions + '\n\n' + '\n\n'.join(choices)
    source = page_text(S, 14)
    instruction_source = squash(between(page_text(S, 13), 'Write 6-10 sentences', '1. Кемпинг'))
    instruction_source = 'Write 6-10 sentences ' + instruction_source
    content = squash(between(page_text(S,13), '2 points for content'))
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
    card = base('EW', question, 30, [15], [13, 14])
    card.pop('rows'); card.pop('tariffModel'); card['kind'] = 'rubric'
    card['rubric'] = {'system': 'language-writing', 'taskRequirements': [squash(instruction_source),
        'No marks are awarded for additional information/content.'],
        'criteria': [criterion('content', 'Communication + content', 12, list(range(0, 13, 2)), [content]),
                     expression, criterion('coherence', 'Textual coherence', 6, list(range(7)), [], coherent)],
        'markingGuideNote': ''}
    cards.append(card)
    return cards

def draw_text(doc,page):
    return doc[page-1].get_text(clip=fitz.Rect(20,30,580,790),sort=False)


def reading(docs,P):
    S,Q=docs['scheme'],docs['paper'];cards=[]
    assert 'Do not penalise answers supplied in Russian.' in squash(page_text(S,3))
    specs=[('IR1',[4],[2,3,4],[1,2,3,2,2,2]),('IR2',[5],[5,6],[3,3,3,3]),
           ('CD',[10,11],[11,12,13],[2,2,3,3,2,2,3,3])]
    for unit,scheme_pages,paper_pages,counts in specs:
        source='\n'.join(draw_text(S,p) for p in scheme_pages)
        if unit=='IR2':source=between(source,'TEXT 2')
        if unit in ('IR1','IR2'):
            heads=list(re.finditer(r'^\s*\((vi|iv|v|i{1,3})\)\s+',source,re.M))
            blocks=[]
            for i,h in enumerate(heads):
                block=source[h.end():heads[i+1].start() if i+1<len(heads) else len(source)]
                blocks.append((i+1 if unit=='IR1' else 1,None if unit=='IR1' else h.group(1),block))
        else:
            blocks=question_blocks(source)
        assert len(blocks)==len(counts),(unit,blocks)
        general='Allocate 2 marks for each'+squash(between(source,'Allocate 2 marks for each','(i)' if unit!='CD' else '1.'))
        if unit=='IR1':general=general.split('Answer in English')[0].strip()
        # Preserve a space after the source delimiter when joining PDF lines.
        general=general.replace('eachcorrect','each correct')
        for index,((item,roman,block),count) in enumerate(zip(blocks,counts)):
            candidates=[b for b in P.blocks if b.unit==unit and b.item==item and b.roman==roman and b.side=='R']
            assert len(candidates)==1,(unit,item,roman)
            question=candidates[0].text
            if (unit,item,roman)==('CD',4,'i'):
                # The old collector stops at the line break before Sochi.
                raw=page_text(Q,12,(297,30,580,775))
                question=squash(re.search(r'Give two details about the Winter Olympics in\s+Sochi\.',raw).group())
            if unit=='IR2':
                cue,rest=block.split('•',1);answers=bullets('•'+rest)
            else:
                price=re.search(r'(\d+)\s*x\s*2\s*marks',block);assert price and int(price.group(1))==count
                cue=block[:price.start()];rest=block[price.end():]
                answers=[squash(line) for line in rest.splitlines() if squash(line)]
            cue=squash(unprice(cue))
            reviewed_rewording=(unit,item,roman)==('IR1',4,None) and cue=='Name two additional subjects available.' and question=='Name two additional activities available to these students.'
            assert score(bag(question),bag(cue))>=.7 or question.startswith(cue) or reviewed_rewording,(question,cue)
            extras=[]
            if unit=='CD' and item==6:
                assert answers.pop()=='Max 2 marks for mentioning the name of a festival'
                extras=['Max 2 marks for mentioning the name of a festival']
            expected={'IR1':[4,4,10,4,5,3],'IR2':[6,6,5,5],'CD':[6,5,7,5,5,6,7,4]}[unit][index]
            assert len(answers)==expected,(unit,item,roman,answers)
            c=as_points(base(unit,question,count*2,paper_pages,scheme_pages,item,roman),answers,count,steps=[0,1,2])
            if extras:
                c['rubric']['groups'].append({'id':'festival-name','label':'Named festival (maximum 2 marks)',
                  'answerCount':1,'rows':[{'id':'full','text':'mentioning the name of a festival','marks':2}]})
            c['rubric']['taskRequirements']=[squash(general)]+extras
            c['review']['questionPages']=[candidates[0].page+1]
            c['rubric']['markingGuideNote']='Answer in English or Irish. Marking scheme page 3: Do not penalise answers supplied in Russian.'
            cards.append(c)
    assert len(cards)==18 and sum(c['totalMarks'] for c in cards)==88
    return cards


def language_and_matching(docs):
    S,Q,cards=docs['scheme'],docs['paper'],[]
    raw=page_text(Q,4)
    english=page_text(Q,4,(300,30,580,775))
    instruction=squash(re.search(r'Write out three.*?script\.',english,re.S).group())
    phrases=re.findall(r'^\s*\d\.\s*([А-Яа-яЁё][А-Яа-яЁё ]+?)\s*$',raw,re.M)
    assert len(phrases)==6,phrases
    instruction+='\n\n'+'\n'.join(phrases)
    c=base('LA1',instruction,6,[4],[5]);c.pop('rows');c.pop('tariffModel');c['kind']='rubric'
    c['rubric']={'system':'language-writing','taskRequirements':['Three phrases in handwritten/cursive script.','2 marks per phrase.','Do not penalise for repeated errors.'],
        'criteria':[criterion(f'phrase-{n}',f'Chosen phrase {n}',2,[0,2],['2 marks per phrase.']) for n in (1,2,3)],'markingGuideNote':''}
    cards.append(c)
    instruction=squash(page_text(Q,7,(300,30,580,200)))
    instruction=instruction[instruction.index('Put three'):]
    instruction=instruction[:instruction.index('nominative case.')+len('nominative case.')]
    table=next(t.extract() for t in S[5].find_tables().tables if 'средней школы' in str(t.extract()))
    pairs=[(squash(row[0]),squash(row[1])) for row in table if len(row)==2 and row[0] and row[1]]
    assert len(pairs)==6,pairs
    c=as_points(base('LA2',instruction,6,[7],[6]),[left+' — '+right for left,right in pairs],3,steps=[0,1,2])
    c['rubric']['taskRequirements']=['Do not penalise if the singular is supplied instead of the plural','1 mark if nominative correctly identified but spelled incorrectly']
    cards.append(c)
    table=next(t.extract() for t in S[6].find_tables().tables if len(t.extract())==11)[1:]
    assert [row[0] for row in table]==['7','2','9','10','1','3','6','8','5','4'],table
    answers=[squash(row[1])+' — '+squash(row[0]) for row in table]
    raw=Q[7].get_text().replace('\u00a0',' ')
    question='Match the headings'+between(raw,'Match the headings')
    c=as_points(base('MM',question,40,[8],[7]),answers,10)
    for group in c['rubric']['groups']:group['rows'][0]['marks']=4
    cards.append(c)
    raw=Q[8].get_text().replace('\u00a0',' ')
    question=squash('Read through'+between(raw,'Read through','Focail'))
    question+='\n\n'+page_text(Q,9,(20,180,580,775))+'\n\n'+page_text(Q,10,(20,30,580,775))
    c=base('SD',question,20,[9,10],[8,9]);c['kind']='question';variants=[]
    for page,group in [(8,'A'),(9,'B')]:
        spans=[span for block in S[page-1].get_text('dict')['blocks'] if 'lines' in block for line in block['lines'] for span in line['spans'] if span['flags']&16 and span['bbox'][1]>150 and re.search('[А-Яа-яЁё]',span['text'])]
        answers=[squash(span['text']) for span in spans if squash(span['text'])]
        assert len(answers)==5,(page,answers)
        variants.append({'id':f'group-{group.lower()}','label':f'Group {group}','rows':[{'id':f'gap-{i}','kind':'point','verbatim':answer,'marks':4} for i,answer in enumerate(answers,1)]})
    c['rows']=variants[0]['rows'];c['answerVariants']=variants;cards.append(c)
    return cards


def listening(docs,P):
    S=docs['scheme'];cards=[]
    general=bullets(between(draw_text(S,15),'LISTENING COMPREHENSION - 100 MARKS','SECTION I'))
    assert len(general)==5 and 'Russian – do not penalise' in general[-1]
    asks=P.aural_asks();assert len(asks)==18
    audio=next(row['source'] for row in json.loads((ROOT/'data/russianAudio.json').read_text()) if row['year']==2022)
    prices=[[5,10,3,2,5],[5,5,5,5,5],[5,5,5,10],[10,5,5,5]]
    pools=[[6,5,1,1,6],[6,1,3,1,5],[3,7,7,5],[4,2,3,3]]
    for section,page in enumerate(range(15,19),1):
        source=draw_text(S,page)
        if section==1:
            # The final item is unnumbered in the scheme; exact original
            # wording identifies it after the preceding price/answer pair.
            source=source.replace('Give one detail about the item the customer has chosen','5. Give one detail about the item the customer has chosen')
        blocks=question_blocks(source);tasks=[a for a in asks if a[0]==f'L{section}']
        assert len(blocks)==len(tasks)==len(prices[section-1]),(section,blocks)
        for index,((scheme_item,scheme_roman,block),(_,item,roman,question),total) in enumerate(zip(blocks,tasks,prices[section-1])):
            unit=f'L{section}'
            if (unit,item,roman)==('L4',3,None):
                assert '\nRúisis' in question;question=question.split('\nRúisis',1)[0]
            price=re.search(r'\((?:(\d+)\s*x\s*)?(\d+)\s*marks\)',block);assert price,(unit,block)
            count=int(price.group(1) or 1);rate=int(price.group(2));assert count*rate==total
            cue=squash(block[:price.start()]);rest=block[price.end():]
            if (unit,item,roman)==('L4',1,None):cue=cue.replace('2 details','two details')
            assert score(bag(question),bag(cue))>=.7 or squash(question).startswith(cue),(question,cue)
            answers=[squash(line) for line in rest.splitlines() if squash(line)]
            assert len(answers)==pools[section-1][index],(unit,item,roman,answers)
            c=as_points(base(unit,question,total,[section+1],[page],item,roman),answers,count)
            for group in c['rubric']['groups']:group['rows'][0]['marks']=rate
            if (unit,item,roman)==('L2',2,None):
                assert answers==['Started going to Russian school (3 marks) on Saturdays (2 marks)']
                c['rubric']['groups']=[{'id':'school-and-day','label':'Russian school and day','answerCount':2,
                  'rows':[{'id':'school','text':'Started going to Russian school','marks':3},{'id':'day','text':'on Saturdays','marks':2}]}]
            notes=[]
            if (item,roman)!=(scheme_item,scheme_roman):
                printed={('L1',3,'i'):'3',('L1',3,'ii'):'4',('L1',4,None):'unnumbered',('L4',1,None):'1(i)',('L4',2,'i'):'2(ii)'}
                assert (unit,item,roman) in printed,(unit,item,roman,scheme_item,scheme_roman)
                notes.append(f'The question booklet labels this {item}'+(f'({roman})' if roman else '')+f'; the marking scheme labels it {printed[(unit,item,roman)]}. This card follows the original question booklet.')
            if section==1:topic='russian-0-3' if item==1 else 'russian-0-8' if item in (2,3) else 'russian-0-9'
            elif section==2:topic='russian-0-1' if item==1 else 'russian-0-3' if item in (2,3) else 'russian-0-8'
            elif section==3:topic='russian-0-9' if item==1 else 'russian-0-8' if item==2 else 'russian-0-3' if item==3 else 'russian-2-1'
            else:topic='russian-0-1' if item==1 else 'russian-0-7' if item==2 else 'russian-0-11'
            c['topicId']=topic;c['additionalTopicIds']=['russian-1-0'];c['rubric']['taskRequirements']=general
            c['rubric']['markingGuideNote']=' '.join(notes)
            c['sourceMaterial']['kind']='source-question';c['sourceMaterial']['presentationNote']='Listen to the official recording and answer the printed question. The transcript is not shown before answering.'
            c['audioMaterial']=audio;c['review']['guidancePages']=[15];cards.append(c)
    assert len(cards)==18 and sum(c['totalMarks'] for c in cards)==100
    return cards


def build():
    docs=opened_sources();P=RuPaper(2022,'ol')
    cards=reading(docs,P)+language_and_matching(docs)+writing(docs)+listening(docs,P)
    assert len(cards)==42 and sum(c['totalMarks'] for c in cards)==305
    old_ids={c['id'] for c in json.loads((ROOT/'scripts/markbank/authored/russian.json').read_text())}
    for c in cards:
        if c['id'] in old_ids:c['review']['correctsExisting']=True
        if not c.get('audioMaterial'):
            c['sourceMaterial']['presentationNote']+=' The 2022 paper offers 175 written marks. Choose one information-retrieval text and its language task; all alternatives remain available here for practice.'
    assert sum(c['review'].get('correctsExisting',False) for c in cards)==19
    return cards

if __name__=='__main__':save_reviewed(build())
