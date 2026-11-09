#!/usr/bin/env python3
"""2021 Ordinary Russian: original-PDF review, 29 written + 18 listening tasks.

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
    'paper': ('papers/2021-ol-000-paper.pdf', '9f52fa220c7d5e407d32de63d657e8e43b822d782872c57b4e8f84b9b3c4f796'),
    'aural': ('papers/2021-ol-A00-paper.pdf', 'bab6aad288773bf503848dc4e868b6c0c5dbac13ae118e4bc19e03f9ac0521c4'),
    'scheme': ('schemes/2021-ol.pdf', '2a4833b1c9cda239dac9671a3a9a7a6bbdf2d93d5ab58954e928dc0c49f9bc14'),
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
    card['id'] = card['id'].replace('2026', '2021').replace('-hl-', '-ol-')
    card['year'] = 2021
    card['level'] = 'ordinary'
    card['questionRef'] = f'2021 OL Section {unit}' + (f' Q{item}' if item is not None else '')
    if roman:
        card['questionRef'] += (' Q' if item is None else '') + f'({roman})'
    card['sourceMaterial']['title'] = f'2021 Ordinary Russian — {unit}'
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
    english = page_text(Q,15,(300,30,580,250))
    instructions = squash('Write 6' + between(english, 'Write 6', 'suggestions only.')) + ' suggestions only.'
    table = Q[14].find_tables().tables[0].extract()
    assert len(table) == 3
    choices = []
    for row in table:
        for cell in row[1:]:
            choices.append('\n• '.join(squash(part) for part in re.split(r'[\uf0b7•]', cell)))
    question = instructions + '\n\n' + '\n\n'.join(choices)
    source = page_text(S, 14)
    instruction_source = squash(between(page_text(S, 13), 'Write 6-10 sentences', '1.'))
    instruction_source = 'Write 6-10 sentences ' + instruction_source
    content = squash(between(page_text(S,13), '2 points for content'))
    content = '2 points for content ' + content
    lower_rule = squash('If the content mark' + between(source, 'If the content mark', 'Put square box'))
    table = S[13].find_tables().tables[0].extract()
    full = [{'label': squash(row[0]), 'marks': mark_range(squash(row[0])), 'guidance': [squash(row[1])]} for row in table[1:]]
    coherence = between(source, 'Allocate 6 marks for textual coherence:')
    coherent = [{'label': n, 'marks': mark_range(n), 'guidance': [squash(text)]}
                for n, text in re.findall(r'^\s*(\d(?:-\d)?)\s+(.+?)(?=^\s*\d(?:-\d)?\s|\Z)', coherence, re.S | re.M)]
    assert len(coherent) == 5, coherent
    expression = criterion('expression', 'Language + expression', 12, list(range(13)), [], full)
    expression['limits'] = [{'id': 'lower-expression', 'maxMarks': 9,
        'when': {'any': [{'criterionIds': ['content'], 'atMost': 6}]}, 'guidance': [lower_rule]}]
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
    S=docs['scheme'];cards=[]
    assert 'Do not penalise answers supplied in Russian.' in squash(page_text(S,3))
    specs=[('IR1',[4],[2,3,4],[1,3,1,1,2,2,1,1]),('IR2',[5,6],[5,6],[3,3,3,3]),
           ('CD',[10,11],[11,12,13],[2,3,2,2,1,2,1,1,2,2,2])]
    for unit,scheme_pages,paper_pages,counts in specs:
        source='\n'.join(draw_text(S,p) for p in scheme_pages)
        if unit=='IR2':source=between(source,'Text 2','Language awareness')
        if unit in ('IR1','IR2'):
            heads=list(re.finditer(r'^\s*\((viii|vii|vi|iv|v|i{1,3})\)\s+',source,re.M))
            blocks=[]
            for i,h in enumerate(heads):
                block=source[h.end():heads[i+1].start() if i+1<len(heads) else len(source)]
                # The last IR1 scheme heading repeats(vii); booklet prints(viii).
                roman='viii' if unit=='IR1' and i==7 else h.group(1)
                blocks.append((None,roman,block))
        else:blocks=question_blocks(source)
        assert len(blocks)==len(counts),(unit,blocks)
        general='Allocate 2 marks for each '+squash(between(source,'Allocate 2 marks for each','(i)' if unit!='CD' else '1.'))
        if unit=='IR1':general=general.split('Answer in English')[0].strip()
        for index,((item,roman,block),count) in enumerate(zip(blocks,counts)):
            candidates=[b for b in P.blocks if b.unit==unit and b.item==item and b.roman==roman and b.side=='R']
            assert len(candidates)==1,(unit,item,roman)
            question=candidates[0].text
            if unit=='IR2':
                cue,rest=block.split('•',1);answers=bullets('•'+rest)
            else:
                chunks=re.split(r'\n\s*\n',unprice(block).strip(),maxsplit=1)
                assert len(chunks)==2,(unit,block)
                cue,rest=chunks
                answers=[squash(line) for line in rest.splitlines() if squash(line)]
            cue=squash(unprice(cue))
            assert score(bag(question),bag(cue))>=.7 or question.startswith(cue),(question,cue)
            expected={'IR1':[1,8,1,1,3,4,4,2],'IR2':[9,6,9,7],'CD':[4,8,5,3,2,3,1,1,3,4,6]}[unit][index]
            assert len(answers)==expected,(unit,item,roman,answers)
            c=as_points(base(unit,question,count*2,paper_pages,scheme_pages,item,roman),answers,count,steps=[0,1,2])
            c['rubric']['taskRequirements']=[squash(general)]
            c['review']['questionPages']=[candidates[0].page+1]
            note='Answer in English or Irish. Marking scheme page 3: Do not penalise answers supplied in Russian.'
            if unit=='IR1' and roman=='viii':note+=' The booklet labels the ticket-price question(viii); scheme page4 repeats(vii). This card follows the booklet.'
            c['rubric']['markingGuideNote']=note
            cards.append(c)
    assert len(cards)==23 and sum(c['totalMarks'] for c in cards)==88
    return cards


def language_and_matching(docs):
    S,Q,cards=docs['scheme'],docs['paper'],[]
    raw=page_text(Q,4)
    english=page_text(Q,4,(300,30,580,775))
    instruction=squash(re.search(r'Write out two.*?script\.',english,re.S).group())
    phrases=re.findall(r'^\s*\d\.\s*([А-Яа-яЁё][А-Яа-яЁё ]+?)\s*$',raw,re.M)
    assert len(phrases)==4,phrases
    instruction+='\n\n'+'\n'.join(phrases)
    c=base('LA1',instruction,6,[4],[5]);c.pop('rows');c.pop('tariffModel');c['kind']='rubric'
    c['rubric']={'system':'language-writing','taskRequirements':['Two of the following phrases in handwritten, cursive script.'],
        'criteria':[criterion(f'phrase-{n}',f'Chosen phrase {n}',3,[0,3],['2 x 3 marks']) for n in (1,2)],'markingGuideNote':''}
    cards.append(c)
    instruction=squash(page_text(Q,7,(300,30,580,200)))
    instruction=instruction[instruction.index('Put three'):]
    instruction=instruction[:instruction.index('nominative case.')+len('nominative case.')]
    table=next(t.extract() for t in S[5].find_tables().tables if 'первом этаже' in str(t.extract()))
    pairs=[(squash(row[0]),squash(row[1])) for row in table if len(row)==2 and row[0] and row[1]]
    assert len(pairs)==6,pairs
    c=as_points(base('LA2',instruction,6,[7],[6]),[left+' — '+right for left,right in pairs],3)
    c['rubric']['taskRequirements']=['Put three of the following expression into the nominative case.']
    cards.append(c)
    table=next(t.extract() for t in S[6].find_tables().tables if len(t.extract())==10)
    assert [row[0] for row in table]==['7','1','9','5','6','10','4','2','3','8'],table
    answers=[squash(row[1])+' — '+squash(row[0]) for row in table]
    raw=Q[7].get_text().replace('\u00a0',' ')
    question='Match the words'+between(raw,'Match the words')
    c=as_points(base('MM',question,40,[8],[7]),answers,10)
    for group in c['rubric']['groups']:group['rows'][0]['marks']=4
    cards.append(c)
    raw=Q[8].get_text().replace('\u00a0',' ')
    question=squash('Read through'+between(raw,'Read through','Focail'))
    question+='\n\n'+('Focail'+between(page_text(Q,9,(20,180,580,775)),'Focail'))+'\n\n'+page_text(Q,10,(20,30,580,775))
    c=base('SD',question,20,[9,10],[8,9]);c['kind']='question';variants=[]
    for page,group in [(8,'A'),(9,'B')]:
        spans=[span for block in S[page-1].get_text('dict')['blocks'] if 'lines' in block for line in block['lines'] for span in line['spans'] if span['flags']&16 and span['size']>15 and re.search('[А-Яа-яЁё]',span['text'])]
        answers=[squash(span['text']) for span in spans if squash(span['text'])]
        assert len(answers)==5,(page,answers)
        variants.append({'id':f'group-{group.lower()}','label':f'Group {group}','rows':[{'id':f'gap-{i}','kind':'point','verbatim':answer,'marks':4} for i,answer in enumerate(answers,1)]})
    c['rows']=variants[0]['rows'];c['answerVariants']=variants;cards.append(c)
    return cards


def listening(docs,P):
    S=docs['scheme'];cards=[]
    general=bullets(between(draw_text(S,15),'LISTENING COMPREHENSION - 100 marks','SECTION I'))
    assert len(general)==5 and 'Russian – do not penalise' in general[-1]
    asks=P.aural_asks();assert len(asks)==18
    audio=next(row['source'] for row in json.loads((ROOT/'data/russianAudio.json').read_text()) if row['year']==2021)
    prices=[[10,5,5,5],[5,5,5,5,5],[5,5,5,5,5],[5,5,10,5]]
    pools=[[4,5,6,1],[3,5,9,5,5],[9,4,5,5,5],[5,3,7,3]]
    for section,page in enumerate(range(15,19),1):
        source=draw_text(S,page)
        blocks=question_blocks(source);tasks=[a for a in asks if a[0]==f'L{section}']
        assert len(blocks)==len(tasks)==len(prices[section-1]),(section,blocks)
        for index,((scheme_item,scheme_roman,block),(_,item,roman,question),total) in enumerate(zip(blocks,tasks,prices[section-1])):
            unit=f'L{section}'
            if (unit,item,roman)==('L3',2,'i'):
                # Legacy collector drops the line ending steamboat.
                raw=page_text(docs['aural'],4,(300,30,580,775))
                question=squash(re.search(r'Give one detail about the cabins on the\s+steamboat\.',raw).group())
            price=re.search(r'\((?:\d+\s*x\s*\d+\s*marks|2 marks \+ 3 marks)\)',block);assert price,(unit,block)
            split=price.group()=='(2 marks + 3 marks)'
            count=2 if split else int(re.search(r'(\d+)\s*x',price.group()).group(1))
            rate=None if split else int(re.search(r'x\s*(\d+)',price.group()).group(1))
            assert (5 if split else count*rate)==total
            cue=squash(block[:price.start()]);rest=block[price.end():]
            assert score(bag(question),bag(cue))>=.7 or squash(question).startswith(cue),(question,cue)
            partial=None
            if (unit,item)==('L1',2):
                rest,partial=rest.split('Plays guitar = 2 marks');partial='Plays guitar'
            answers=bullets(rest) if '•' in rest else [squash(line) for line in rest.splitlines() if squash(line)]
            assert len(answers)==pools[section-1][index],(unit,item,roman,answers)
            c=base(unit,question,total,[section+1],[page],item,roman)
            if split:
                c['kind']='question';c['rows']=[{'id':'answers','kind':'anyN','verbatim':'The answers the scheme accepts','marks':None,
                    'group':{'claimMax':2,'perOption':2,'perOptionSteps':[2,3],'options':answers},
                    'contextNote':' '.join(general)+' Published tariff: 2 marks + 3 marks. Choose two distinct accepted details; the ordered awards are 2 and then 3.'}]
            else:
                c=as_points(c,answers,count)
                for group in c['rubric']['groups']:group['rows'][0]['marks']=rate
                if partial:c['rubric']['groups'].append({'id':'guitar-partial','label':'Published partial answer','answerCount':1,'rows':[{'id':'partial','text':partial,'marks':2}]})
                c['rubric']['taskRequirements']=general
                if (item,roman)!=(scheme_item,scheme_roman):
                    assert (unit,item,roman,scheme_item,scheme_roman)==('L2',2,None,2,'i')
                    c['rubric']['markingGuideNote']='The booklet labels this question2; scheme page16 labels it2(i). This card follows the booklet.'
            if section==1:topic='russian-0-8' if item in (1,4) else 'russian-0-3' if item==2 else 'russian-0-5'
            elif section==2:topic='russian-0-1' if item==1 and roman=='i' else 'russian-0-3'
            elif section==3:topic='russian-2-1' if item==4 else 'russian-0-8'
            else:topic='russian-0-1' if item in (1,3) else 'russian-0-11'
            c['topicId']=topic;c['additionalTopicIds']=['russian-1-0']
            if (unit,item,roman)==('L3',4,None):c['sourceMaterial']['pages']=[5];c['review']['paperPages']=[5]
            if section==4:c['sourceMaterial']['pages']=[6];c['review']['paperPages']=[6]
            c['sourceMaterial']['kind']='source-question';c['sourceMaterial']['presentationNote']='Listen to the official recording and answer the printed question. The transcript is not shown before answering.'
            c['audioMaterial']=audio;c['review']['guidancePages']=[15];cards.append(c)
    assert len(cards)==18 and sum(c['totalMarks'] for c in cards)==100
    return cards


def build():
    docs=opened_sources();P=RuPaper(2021,'ol')
    cards=reading(docs,P)+language_and_matching(docs)+writing(docs)+listening(docs,P)
    assert len(cards)==47 and sum(c['totalMarks'] for c in cards)==305
    old_ids={c['id'] for c in json.loads((ROOT/'scripts/markbank/authored/russian.json').read_text())}
    for c in cards:
        if c['id'] in old_ids:c['review']['correctsExisting']=True
        if not c.get('audioMaterial'):
            c['sourceMaterial']['presentationNote']+=' The 2021 paper offers 175 written marks. Choose one information-retrieval text and its language task; all alternatives remain available here for practice.'
    assert sum(c['review'].get('correctsExisting',False) for c in cards)==24
    return cards

if __name__=='__main__':save_reviewed(build())
