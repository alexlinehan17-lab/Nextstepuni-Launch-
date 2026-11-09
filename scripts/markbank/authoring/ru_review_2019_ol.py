#!/usr/bin/env python3
"""2019 Ordinary Russian: original-PDF review, 27 written + 17 listening tasks.

This sitting has 220 written and 100 listening marks. Both discourse dialogues
are mandatory. Unpriced multi-part allocations retain their printed total; no
per-gap or per-detail prices are inferred.
"""
import hashlib
import json
import re
from pathlib import Path

import fitz
from ru_paper import RuPaper, bag, score
from ru_review_2026_hl import ROOT, squash, page_text as original_page_text, between, bullets, base as higher_base, as_points, mark_range, save_reviewed

FILES = {
    'paper': ('papers/2019-ol-000-paper.pdf', '41d32895142e7d84b407db7aba924b55c6f436cf04f8e5d42752008d52766857'),
    'aural': ('papers/2019-ol-A00-paper.pdf', 'f0a5627680ab08fd5249384d34e2d95dd67eba058144feb7c6458ea1683f2dbb'),
    'scheme': ('schemes/2019-ol.pdf', '8622b34ca8c3a357141ced0ff917e9ebeea56e3f3783e86f3f1403d5e32a3237'),
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
    card['id'] = card['id'].replace('2026', '2019').replace('-hl-', '-ol-')
    card['year'] = 2019
    card['level'] = 'ordinary'
    card['questionRef'] = f'2019 OL Section {unit}' + (f' Q{item}' if item is not None else '')
    if roman:
        card['questionRef'] += (' Q' if item is None else '') + f'({roman})'
    card['sourceMaterial']['title'] = f'2019 Ordinary Russian — {unit}'
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
    source = page_text(S, 9)
    content = squash(between(source, 'Content of each answer', 'Textual coherence'))
    coherence = between(source, 'Textual coherence\n', 'B.')
    bands = [{'label': n, 'marks': [int(n)], 'guidance': [squash(text)]}
             for n, text in re.findall(r'(\d) marks?\s+(.+?)(?=\d marks?|\Z)', coherence, re.S)]
    assert len(bands) == 4
    card = base('SA', question, 30, [14], [9])
    card.pop('rows'); card.pop('tariffModel'); card['kind'] = 'rubric'
    card['rubric'] = {'system': 'language-writing', 'taskRequirements': [
        'Write 3-5 sentences on TWO of the following topics in Russian or English. Each answer should contain three factual details. Marks are awarded for relevant content and textual coherence.',
        'The quality of the English/Russian will only be an assessment factor insofar as it impedes communication.'],
        'criteria': [criterion(f'{choice}-content', f'{label}: content', 12, list(range(0,13,2)), [content]) if part=='content' else criterion(f'{choice}-coherence', f'{label}: textual coherence', 3, [0,1,2,3], [], bands) for choice,label in [('first','First chosen topic'),('second','Second chosen topic')] for part in ['content','coherence']],
        'markingGuideNote': ''}
    cards.append(card)

    raw = Q[14].get_text().replace('\u00a0', ' ')
    english = page_text(Q,15,(295,30,580,160))
    instructions = squash('Write 6' + between(english, 'Write 6', 'IN RUSSIAN.')) + ' IN RUSSIAN.'
    table = Q[14].find_tables().tables[0].extract()
    assert len(table) == 3
    choices = []
    for row in table:
        for cell in row[1:]:
            choices.append('\n• '.join(squash(part) for part in re.split(r'[\uf0b7•]', cell)))
    question = instructions + '\n\n' + '\n\n'.join(choices)
    source = page_text(S, 10)
    instruction_source = squash(between(page_text(S, 9), 'Write 6-10 sentences', '1.'))
    instruction_source = 'Write 6-10 sentences ' + instruction_source
    content = squash(between(page_text(S,10), '2 points for content', 'Accuracy and fluency'))
    content = '2 points for content ' + content
    lower_rule = squash('If the content mark' + between(source, 'If the content mark', 'Put square box'))
    table = S[9].find_tables().tables[0].extract()
    full = [{'label': squash(row[0]), 'marks': mark_range(squash(row[0])), 'guidance': [squash(row[1])]} for row in table[1:]]
    coherence = between(source, 'Allocate 6 marks for textual coherence:')
    coherent = [{'label': n, 'marks': mark_range(n), 'guidance': [squash(text)]}
                for n, text in re.findall(r'^\s*(\d(?:-\d)?)\s+(.+?)(?=^\s*\d(?:-\d)?\s|\Z)', coherence, re.S | re.M)]
    assert len(coherent) == 5, coherent
    expression = criterion('expression', 'Language + expression', 12, list(range(13)), [], full)
    expression['limits'] = [{'id': 'lower-expression', 'maxMarks': 9,
        'when': {'any': [{'criterionIds': ['content'], 'atMost': 6}]}, 'guidance': [lower_rule]}]
    card = base('EW', question, 30, [15], [9, 10])
    card.pop('rows'); card.pop('tariffModel'); card['kind'] = 'rubric'
    card['rubric'] = {'system': 'language-writing', 'taskRequirements': [squash(instruction_source),
        'No marks are awarded for additional information/content.'],
        'criteria': [criterion('content', 'Communication + content', 12, list(range(0, 13, 2)), [content]),
                     expression, criterion('coherence', 'Textual coherence', 6, list(range(7)), [], coherent)],
        'markingGuideNote': ''}
    cards.append(card)
    return cards


def draw_text(doc,page):
    return doc[page-1].get_text(clip=fitz.Rect(20,30,580,790),sort=False).replace('\uf0b7','•')


def printed_ask(Q,pages,item):
    # The legacy 2019 collector misses the information-retrieval headings.
    # Recover the question verbatim from the original English column.
    found=[]
    for page in pages:
        raw=page_text(Q,page,(300,30,580,775))
        for match in re.finditer(r'^\s*'+str(item)+r'\.\s+((?:What|How|Give|There)\b.+?)(?=\n\s*\n)',raw,re.M|re.S):
            found.append((page,squash(match.group(1))))
    assert len(found)==1,(pages,item,found)
    return found[0]


def reading(docs,P):
    S,Q,cards=docs['scheme'],docs['paper'],[]
    specs=[('IR1',4,[2,3,4],[1,1,3,1,2,2,2],[2,1,6,1,3,3,3]),
           ('IR2',5,[5,6,7],[3,2,3,1,3],[5,8,11,2,12]),
           ('CD',8,[11,12,13],[2,1,2,2,4,1,3,2,3],[4,3,7,3,8,1,5,4,6])]
    for unit,page,pages,counts,pools in specs:
        source=draw_text(S,page)
        if unit=='IR1':source=between(source,'Answer in English unless otherwise indicated.')
        if unit=='IR2':source=between(source,'Text 2')
        blocks=question_blocks(source)
        assert len(blocks)==len(counts),(unit,blocks)
        for index,((item,roman,block),count) in enumerate(zip(blocks,counts)):
            price=re.search(r'\b\d+(?:\s*x\s*\d+)?\s*marks?\b',block)
            assert price,(unit,block)
            cue=squash(block[:price.start()]);rest=block[price.end():].strip()
            if unit=='CD':
                candidate=next(b for b in P.blocks if (b.unit,b.item,b.roman,b.side)==(unit,item,roman,'R'))
                page_q,question=candidate.page+1,candidate.text
            else:page_q,question=printed_ask(Q,pages,item)
            assert score(bag(question),bag(cue))>=.7,(question,cue)
            note='Answer in English or Irish. Marking scheme page 3: Do not penalise answers supplied in Russian.'
            partials={}
            if unit=='IR1' and item==3:
                rest=rest.split('Assign 1 mark theatre')[0]
                partials={4:['theatre']}
            if unit=='IR1' and item==7:
                rest,extra=rest.split('(Accept an answer written')
                note+=' '+squash('(Accept an answer written'+extra)
            if unit=='CD' and (item,roman)==(3,'ii'):
                english,russian=rest.split('Accept Russian versions of these six adjectives:')
                en=[squash(t) for t in re.split(r'\bor\b',english)]
                ru=[squash(t).rstrip(')') for t in russian.split(',')]
                assert len(en)==len(ru)==6
                answers=[e+' — '+r for e,r in zip(en,ru)]
            else:answers=bullets(rest) if '•' in rest else [squash(line) for line in rest.splitlines() if squash(line)]
            assert len(answers)==pools[index],(unit,item,roman,answers)
            c=as_points(base(unit,question,count*2,pages,[page],item,roman),answers,count,partials=partials,steps=[0,1,2])
            c['review']['questionPages']=[page_q]
            c['rubric']['taskRequirements']=['Allocate 2 marks for each correct idea/concept'+(' unless otherwise stated' if unit!='CD' else '')+' and 1 mark for a partially correct idea/concept.']
            c['rubric']['markingGuideNote']=note
            if unit=='IR1' and item==7:
                # The scheme expressly accepts earlier price options. Retain the
                # exact earlier scheme wording, plus the child's price only
                # printed in the original passage. All remain under two answers.
                earlier=['1200 roubles','Discount for families from 200 to 600 roubles','Two adults and one child costs 3000 roubles instead of 3200 roubles']
                passage=squash(page_text(Q,2))
                child=re.search(r'детский билет \(7.13 лет\) стоит 800 руб',passage).group()
                earlier.append(child)
                for n,answer in enumerate(earlier,1):
                    c['rubric']['groups'].append({'id':f'earlier-price-{n}','label':f'Earlier price option {n}','answerCount':1,'rows':[{'id':'full','text':answer,'marks':2,'steps':[0,1,2]}]})
                c['review']['paperAnswerSources']=[{'text':child,'pages':[2],
                    'schemeAcceptance':'Accept answers referring to price options from earlier in the text if marks have not already been awarded.'}]
            cards.append(c)
    assert len(cards)==21 and sum(c['totalMarks'] for c in cards)==88
    return cards


def language_and_matching(docs):
    S,Q,cards=docs['scheme'],docs['paper'],[]
    raw=page_text(Q,4)
    english=page_text(Q,4,(300,30,580,775))
    instruction=squash(re.search(r'Write out.*?script\.',english,re.S).group())
    phrases=['Посмотрите на Москву.','На двухэтажном автобусе']
    assert all(squash(t).rstrip('.') in squash(raw) for t in phrases)
    c=base('LA1',instruction+'\n\n'+'\n'.join(phrases),6,[4],[5])
    c.pop('rows');c.pop('tariffModel');c['kind']='rubric'
    source=draw_text(S,5)
    guidance=squash('Assign three marks'+between(source,'Assign three marks','Text 2'))
    c['rubric']={'system':'language-writing','taskRequirements':[guidance],
        'criteria':[criterion(f'phrase-{n}',phrase,3,[0,3],[]) for n,phrase in enumerate(phrases,1)],'markingGuideNote':''}
    cards.append(c)
    instruction=squash(page_text(Q,7,(300,30,580,420)))
    instruction='The following'+between(instruction,'The following','plural:')+'plural:'
    table=next(t.extract() for t in S[5].find_tables().tables if len(t.extract())==6)
    pairs=[squash(row[0])+' — '+squash(row[1]) for row in table]
    c=as_points(base('LA2',instruction,6,[7],[6]),pairs,6)
    for group in c['rubric']['groups']:group['rows'][0]['marks']=1
    cards.append(c)
    table=next(t.extract() for t in S[5].find_tables().tables if len(t.extract())==10)
    assert [row[0].split('.')[0] for row in table]==['2','4','5','6','7','8','1','9','10','3']
    answers=[squash(row[0])+' — '+squash(row[1]) for row in table]
    raw=Q[7].get_text().replace('\u00a0',' ')
    question='Match the following'+between(raw,'Match the following')
    c=as_points(base('MM',question,40,[8],[6]),answers,10)
    for group in c['rubric']['groups']:group['rows'][0]['marks']=4
    cards.append(c)
    raw=Q[8].get_text().replace('\u00a0',' ')
    question=squash('Read through'+between(raw,'Read through','Focail'))
    question+='\n\n'+('Focail'+between(page_text(Q,9,(20,180,580,775)),'Focail'))+'\n\n'+page_text(Q,10,(20,30,580,775))
    c=base('SD',question,20,[9,10],[7]);c['kind']='question';c['tariffModel']={'kind':'questionTotal'}
    # The source highlights ten answers in red but publishes no per-gap prices.
    spans=[span for block in S[6].get_text('dict')['blocks'] if 'lines' in block for line in block['lines'] for span in line['spans'] if span['color']!=0 and re.search('[А-Яа-яЁё]',span['text'])]
    answers=[squash(span['text']) for span in spans if squash(span['text'])]
    assert answers==['Где','кто','кем / где','каком','кем / где','Чем','Какие','Сколько','Когда','какой'],answers
    c['rows']=[{'id':f'gap-{n}','kind':'point','verbatim':answer,'marks':None} for n,answer in enumerate(answers,1)]
    c['rows'][0]['contextNote']='Complete both Group A and Group B. The scheme publishes 20 marks for the whole exercise without per-gap allocations. Review all ten answers here; numeric self-scoring is unavailable for this exercise.'
    cards.append(c)
    return cards


def listening(docs,P):
    S=docs['scheme'];cards=[]
    general=bullets(between(draw_text(S,11),'LISTENING COMPREHENSION - 100 marks','SECTION I'))
    assert len(general)==5 and 'Russian – do not penalise' in general[-1]
    asks=P.aural_asks();assert len(asks)==17
    audio=next(row['source'] for row in json.loads((ROOT/'data/russianAudio.json').read_text()) if row['year']==2019)
    prices=[[5,5,5,5,5],[5,10,5,5],[10,5,5,5],[10,5,5,5]]
    pools=[[6,5,3,5,7],[1,7,5,1],[13,9,1,1],[7,8,1,3]]
    sources=[between(draw_text(S,11),'SECTION I'),between(draw_text(S,12),'SECTION II','Section III'),between(draw_text(S,12),'Section III'),between(draw_text(S,13),'SECTION IV')]
    for section,(source,page) in enumerate(zip(sources,[11,12,12,13]),1):
        # The original L3Q2(i) drops the2 before its roman marker.
        if section==3:source=source.replace('.(i)','2.(i)')
        blocks=question_blocks(source);tasks=[a for a in asks if a[0]==f'L{section}']
        assert len(blocks)==len(tasks)==len(prices[section-1]),(section,blocks)
        for index,((scheme_item,scheme_roman,block),(_,item,roman,question),total) in enumerate(zip(blocks,tasks,prices[section-1])):
            unit=f'L{section}';question=squash(question.split('Rúisis')[0])
            price=re.search(r'\b(\d+)\s*marks?\b',block);assert price,(unit,block)
            assert int(price.group(1))==total
            cue=squash(block[:price.start()]);rest=block[price.end():]
            assert score(bag(question),bag(cue))>=.7,(question,cue)
            partial=None
            if (unit,item)==('L2',3):rest,partial=rest.split('Award two marks: museum');partial='museum'
            answers=bullets(rest) if '•' in rest else [squash(line) for line in rest.splitlines() if squash(line)]
            assert len(answers)==pools[section-1][index],(unit,item,roman,answers)
            paper_pages={'L1':[2,3],'L2':[3],'L3':[4],'L4':[5]}[unit]
            c=base(unit,question,total,paper_pages,[page],item,roman)
            if total==10:
                c['kind']='question';c['tariffModel']={'kind':'questionTotal'}
                c['rows']=[{'id':f'answer-{n}','kind':'point','verbatim':answer,'marks':None} for n,answer in enumerate(answers,1)]
                c['rows'][0]['contextNote']=' '.join(general)+' Choose two distinct details. The scheme publishes 10 marks for this question without a per-detail allocation. Review the accepted answers here; numeric self-scoring is unavailable for this question.'
            else:
                c=as_points(c,answers,1)
                for group in c['rubric']['groups']:group['rows'][0]['marks']=5
                if partial:c['rubric']['groups'][0]['rows'].append({'id':'museum-partial','text':partial,'marks':2})
                c['rubric']['taskRequirements']=general
                if (unit,item,roman)==('L3',2,'i'):c['rubric']['markingGuideNote']='The booklet labels this question2(i); scheme page12 prints only.(i). This card follows the booklet.'
            c['topicId']=('russian-0-8' if item in (1,5) else 'russian-0-4' if item==2 else 'russian-0-5' if item==3 else 'russian-0-3') if section==1 else ('russian-0-1' if section==4 else 'russian-0-3')
            c['additionalTopicIds']=['russian-1-0']
            c['sourceMaterial']['kind']='source-question';c['sourceMaterial']['presentationNote']='Listen to the official recording and answer the printed question. The transcript is not shown before answering.'
            c['audioMaterial']=audio;c['review']['guidancePages']=[11];cards.append(c)
    assert len(cards)==17 and sum(c['totalMarks'] for c in cards)==100
    return cards


def build():
    docs=opened_sources();P=RuPaper(2019,'ol')
    cards=reading(docs,P)+language_and_matching(docs)+writing(docs)+listening(docs,P)
    assert len(cards)==44 and sum(c['totalMarks'] for c in cards)==320
    old_ids={c['id'] for c in json.loads((ROOT/'scripts/markbank/authored/russian.json').read_text())}
    for c in cards:
        if c['id'] in old_ids:c['review']['correctsExisting']=True
    assert not any(c['review'].get('correctsExisting') for c in cards)
    return cards


if __name__=='__main__':save_reviewed(build())
