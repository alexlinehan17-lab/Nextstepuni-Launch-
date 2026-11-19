#!/usr/bin/env python3
"""2018 Ordinary Russian: original-PDF review, 26 written + 17 listening tasks.

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
    'paper': ('papers/2018-ol-000-paper.pdf', 'ecdc14883748d1b8784886a5a8daa9215273c90f666d88a4750cf31958b4e018'),
    'aural': ('papers/2018-ol-A00-paper.pdf', 'd5f944ddcacabec032c48ee1bfc130b4cdf60e96905e27376570afe5297d5c9c'),
    'scheme': ('schemes/2018-ol.pdf', 'fcb24b1b07dc2d5369a4c27506485b2e0670f79dfdfb68b556efc289fac62bc3'),
}


def page_text(doc, page, box=None):
    # Preserve the entire answer area while excluding the running footer.
    return original_page_text(doc, page, box or (20, 30, 580, 770)).replace('\uf0b7','•')


def opened_sources():
    docs = {}
    for key, (relative, digest) in FILES.items():
        path = ROOT / 'examiner-reports/russian' / relative
        assert hashlib.sha256(path.read_bytes()).hexdigest() == digest, path
        docs[key] = fitz.open(path)
    return docs


def base(unit, text, total, pages, scheme_pages, item=None, roman=None):
    card = higher_base(unit, text, total, pages, scheme_pages, item, roman)
    card['id'] = card['id'].replace('2026', '2018').replace('-hl-', '-ol-')
    card['year'] = 2018
    card['level'] = 'ordinary'
    card['questionRef'] = f'2018 OL Section {unit}' + (f' Q{item}' if item is not None else '')
    if roman:
        card['questionRef'] += (' Q' if item is None else '') + f'({roman})'
    card['sourceMaterial']['title'] = f'2018 Ordinary Russian — {unit}'
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
    content=content.removeprefix('12 ').strip()
    coherence=between(source,'Textual coherence')
    pairs=re.findall(r'^\s*([0-3])\s+(.+?)(?=^\s*[0-3]\s|\Z)',coherence,re.M|re.S)
    bands=[{'label':n,'marks':[int(n)],'guidance':[squash(text)]} for n,text in pairs if not squash(text).startswith('Allocate')]
    assert len(bands) == 4
    card = base('SA', question, 30, [14], [9])
    card.pop('rows'); card.pop('tariffModel'); card['kind'] = 'rubric'
    card['rubric'] = {'system': 'language-writing', 'taskRequirements': [
        'Write 3-5 sentences on TWO of the following topics in Russian or English. Each answer should contain three factual details. Marks are awarded for relevant content and textual coherence.',
        'The quality of the English/Russian will only be an assessment factor insofar as it impedes communication.'],
        'criteria': [criterion(f'{choice}-content', f'{label}: content', 12, list(range(0,13,2)), [content]) if part=='content' else criterion(f'{choice}-coherence', f'{label}: textual coherence', 3, [0,1,2,3], [], bands) for choice,label in [('first','First chosen topic'),('second','Second chosen topic')] for part in ['content','coherence']],
        'markingGuideNote': ''}
    cards.append(card)

    raw = Q[15].get_text().replace('\u00a0', ' ')
    english = page_text(Q,16,(295,30,580,160))
    instructions = squash('Write 6' + between(english, 'Write 6', 'IN RUSSIAN.')) + ' IN RUSSIAN.'
    table = Q[15].find_tables().tables[0].extract()
    assert len(table) == 3
    choices = []
    for row in table:
        for cell in row[1:]:
            choices.append('\n• '.join(squash(part) for part in re.split(r'[\uf0b7•]', cell)))
    question = instructions + '\n\n' + '\n\n'.join(choices)
    source = page_text(S, 11)
    instruction_source = squash(between(page_text(S, 10), 'Write 6-10 sentences', '1.'))
    instruction_source = 'Write 6-10 sentences ' + instruction_source
    content = squash(between(page_text(S,10), '2 points for content'))
    content = '2 points for content ' + content
    table = S[10].find_tables().tables[0].extract()
    full = [{'label': squash(row[0]), 'marks': mark_range(squash(row[0])), 'guidance': [squash(row[1])]} for row in table[1:]]
    coherence = between(source, 'Allocate 6 marks for textual coherence:')
    coherent = [{'label': n, 'marks': mark_range(n), 'guidance': [squash(text)]}
                for n, text in re.findall(r'^\s*(\d(?:-\d)?)\s+(.+?)(?=^\s*\d(?:-\d)?\s|\Z)', coherence, re.S | re.M)]
    assert len(coherent) == 5, coherent
    expression = criterion('expression', 'Language + expression', 12, list(range(13)), [], full)
    card = base('EW', question, 30, [16], [10, 11])
    card.pop('rows'); card.pop('tariffModel'); card['kind'] = 'rubric'
    card['rubric'] = {'system': 'language-writing', 'taskRequirements': [squash(instruction_source),
        'No marks are awarded for additional information/content.'],
        'criteria': [criterion('content', 'Communication + content', 12, list(range(0, 13, 2)), [content]),
                     expression, criterion('coherence', 'Textual coherence', 6, list(range(7)), [], coherent)],
        'markingGuideNote': ''}
    cards.append(card)
    return cards


def draw_text(doc,page):
    return doc[page-1].get_text(clip=fitz.Rect(20,30,580,770),sort=False).replace('\uf0b7','•')


def numbered_blocks(text):
    heads=list(re.finditer(r'^\s*(\d)\.\s*(?:(iv|vi|i{1,3})\.\s*)?(?=[A-Z])',text,re.M))
    return [(int(h.group(1)),h.group(2),text[h.end():heads[n+1].start() if n+1<len(heads) else len(text)]) for n,h in enumerate(heads)]


def clean_question(text):
    return squash(text.split('_')[0].split('Segment')[0])


def reading(docs,P):
    S,Q,cards=docs['scheme'],docs['paper'],[]
    specs=[('IR1',4,[2,3],[2,1,1,1,5,1,1],[6,1,1,1,7,2,1]),
           ('IR2',5,[5,6],[3,3,3,3],[8,13,10,8]),
           ('CD',8,[11,12,13],[1,3,1,1,2,3,5,2,2],[3,6,2,1,4,4,17,5,3])]
    for unit,page,pages,counts,pools in specs:
        source=draw_text(S,page)
        if unit!='CD':source=source.split('Language awareness')[0]
        if unit=='IR1':
            heads=list(re.finditer(r'^\s*(vii|vi|iv|v|i{1,3})\.\s+',source,re.M))
            blocks=[(None,h.group(1),source[h.end():heads[n+1].start() if n+1<len(heads) else len(source)]) for n,h in enumerate(heads)]
            paper=page_text(Q,3,(300,30,580,770))
            asks={roman:clean_question(block) for _,roman,block in [(None,h.group(1),paper[h.end():hs[n+1].start() if n+1<len(hs) else len(paper)]) for hs in [list(re.finditer(r'^\s*(vii|vi|iv|v|i{1,3})\.\s+',paper,re.M))] for n,h in enumerate(hs)]}
        elif unit=='IR2':
            heads=list(re.finditer(r'^\s*((?:Give|A Russian school).+?\(Section \d\))\s*\n',source,re.M|re.S))
            assert len(heads)==4
            blocks=[(n+1,None,source[h.start():heads[n+1].start() if n+1<len(heads) else len(source)]) for n,h in enumerate(heads)]
            asks=[]
            for p in (5,6):
                text=page_text(Q,p,(300,30,580,770))
                asks.extend((p,squash(m.group())) for m in re.finditer(r'(?:Give three details|A Russian school).+?(?=\n\s*\n)',text,re.S))
            assert len(asks)==4,asks
        else:blocks=numbered_blocks(source)
        assert len(blocks)==len(counts),(unit,blocks)
        if unit in ('IR1','IR2'):
            end='i.' if unit=='IR1' else 'Give three details'
            general='Allocate 2 marks '+squash(between(source,'Allocate 2 marks',end))
        else:general=squash(between(source,'D.','1.i.'))
        for n,((item,roman,block),count) in enumerate(zip(blocks,counts)):
            if unit=='IR1':
                lines=block.strip().splitlines();cue=lines[0];rest='\n'.join(lines[1:]);question=asks[roman];question_page=3
            elif unit=='IR2':
                cue,rest=re.split(r'\(Section \d\)',block,maxsplit=1);question_page,question=asks[n]
            else:
                m=re.search(r'\(\d+ marks\)',block);assert m,block
                cue=block[:m.start()];rest=block[m.end():]
                if (item,roman)==(1,'vi'):roman='iv'
                candidate=next(b for b in P.blocks if b.unit=='CD' and b.item==item and b.side=='R' and (b.text.startswith(roman+'.') if roman else not re.match(r'i+[v]?\.',b.text)))
                question=re.sub(r'^i+[v]?\.\s*','',candidate.text);question_page=candidate.page+1
            cue=squash(cue)
            assert score(bag(question),bag(cue))>=.7,(question,cue)
            answers=[squash(a) for a in rest.split('+') if squash(a)]
            assert len(answers)==pools[n],(unit,item,roman,answers)
            # The same unqualified work-experience phrase is printed twice.
            # One accepted answer retains it without awarding identical detail twice.
            if unit=='IR2' and item==2:
                assert answers.count('work experience with children')==2
                answers=list(dict.fromkeys(answers))
            c=as_points(base(unit,question,count*2,pages,[page],item,roman),answers,count,steps=[0,1,2])
            c['review']['questionPages']=[question_page]
            c['rubric']['taskRequirements']=[general]
            c['rubric']['markingGuideNote']='Answer in English or Irish.'
            if unit=='CD' and (item,roman)==(1,'iv'):c['rubric']['markingGuideNote']+=' The booklet labels this question1.iv; scheme physical page8 prints1.vi. This card follows the booklet.'
            cards.append(c)
    assert len(cards)==20 and sum(c['totalMarks'] for c in cards)==88
    return cards


def language_and_matching(docs):
    S,Q,cards=docs['scheme'],docs['paper'],[]
    phrases=['Наши цены очень низкие.','Дополнительные услуги']
    raw=page_text(Q,4)
    assert all(p in squash(raw) for p in phrases)
    question=squash(re.search(r'Write out.*?script\.',page_text(Q,4,(300,30,580,770)),re.S).group())+'\n\n'+'\n'.join(phrases)
    c=base('LA1',question,6,[4],[4]);c['kind']='question';c['tariffModel']={'kind':'questionTotal'}
    c['rows']=[{'id':f'phrase-{n}','kind':'point','verbatim':p,'marks':None} for n,p in enumerate(phrases,1)]
    c['rows'][0]['contextNote']='The scheme gives 6 marks for both phrases without per-phrase allocations or a handwritten exemplar. Review the complete printed task; numeric self-scoring is unavailable for this exercise.'
    cards.append(c)
    instruction=squash(page_text(Q,7,(300,30,580,250)))
    instruction='The following'+between(instruction,'The following','plural:')+'plural:'
    table=S[4].find_tables().tables[0].extract();assert len(table)==6
    c=as_points(base('LA2',instruction,6,[7],[5]),[squash(a)+' — '+squash(b) for a,b in table],6)
    for g in c['rubric']['groups']:g['rows'][0]['marks']=1
    cards.append(c)
    table=S[5].find_tables().tables[0].extract();assert [r[0] for r in table]==['3','7','9','2','1','8','5','6','10','4']
    raw=Q[7].get_text().replace('\u00a0',' ');question='Match the following'+between(raw,'Match the following')
    c=as_points(base('MM',question,40,[8],[6]),[squash(b)+' — '+squash(a) for a,b in table],10)
    for g in c['rubric']['groups']:g['rows'][0]['marks']=4
    cards.append(c)
    raw=Q[8].get_text().replace('\u00a0',' ');question=squash('Read through'+between(raw,'Read through','Focail'))
    question+='\n\n'+'Focail'+between(page_text(Q,9,(20,180,580,770)),'Focail')+'\n\n'+page_text(Q,10)
    c=base('SD',question,20,[9,10],[7]);c['kind']='question';c['tariffModel']={'kind':'questionTotal'}
    # Underlined source words; retain source Latin C/H glyphs rather than silently
    # replacing them with visually similar Cyrillic characters.
    answers=['cлушаю','забронировать','интересуют','скажите','приедете','Добрый','Kонечно','Приятно','Hе за что','большое']
    c['rows']=[{'id':f'gap-{n}','kind':'point','verbatim':answer,'marks':None} for n,answer in enumerate(answers,1)]
    c['rows'][0]['contextNote']='Complete both Group A and Group B. The scheme publishes 20 marks for the whole exercise without per-gap allocations. Review all ten answers here; numeric self-scoring is unavailable for this exercise.'
    cards.append(c)
    return cards


def listening(docs):
    S,A,cards=docs['scheme'],docs['aural'],[]
    general=bullets(between(draw_text(S,12),'General:','Award five marks'))
    general.append('Award five marks for each correct/relevant point.')
    assert len(general)==6
    audio=next(r['source'] for r in json.loads((ROOT/'data/russianAudio.json').read_text()) if r['year']==2018)
    source=draw_text(S,12)+'\n'+draw_text(S,13)+'\n'+draw_text(S,14)
    source=re.sub(r'(Section (?:III|IV|II)) *\n',r'\1\n',source)
    sections=[between(source,'Section 1','Section II\n'),between(source,'Section II\n','Section III\n'),between(source,'Section III\n','Section IV\n'),between(source,'Section IV\n')]
    counts=[[1,1,1,1,1],[1,1,2,1],[1,2,1,1],[2,1,1,1]]
    pools=[[1,5,3,5,7],[8,3,13,5],[1,7,9,5],[6,9,12,2]]
    for section,text in enumerate(sections,1):
        unit=f'L{section}';blocks=numbered_blocks(text)
        asks=numbered_blocks(page_text(A,section+1,(300,30,580,770)))
        assert len(blocks)==len(asks)==len(counts[section-1]),(unit,blocks,asks)
        for index,((scheme_item,scheme_roman,block),(item,roman,q),count) in enumerate(zip(blocks,asks,counts[section-1])):
            question=clean_question(q);lines=[line for line in block.strip().splitlines() if line.strip()]
            # Locate the final question punctuation, retaining any Give... clause.
            match=re.search(r'^(.*?(?:Give (?:one|two) detail(?:s)?\.|\?|\.(?=\s*\n)))(?:\s*\n)(.*)$',block.strip(),re.S)
            assert match,(unit,block)
            cue,rest=match.groups();cue=squash(cue)
            assert score(bag(question),bag(cue))>=.7,(question,cue)
            no_credit='';partial=None
            if 'no marks:' in rest:rest,no_credit=rest.split('no marks:',1);no_credit='no marks: '+squash(no_credit)
            if 'Award two marks:' in rest:rest,partial=rest.split('Award two marks:',1);partial=squash(partial)
            answers=[squash(a) for a in rest.split('+') if squash(a)]
            assert len(answers)==pools[section-1][index],(unit,item,roman,answers)
            c=as_points(base(unit,question,count*5,[section+1],[12] if section==1 else [13] if section==2 else [13,14] if section==3 else [14],item,roman),answers,count)
            for g in c['rubric']['groups']:g['rows'][0]['marks']=5
            if partial:c['rubric']['groups'].append({'id':'dublin-partial','label':'Published partial answer','answerCount':1,'rows':[{'id':'partial','text':partial,'marks':2}]})
            c['rubric']['taskRequirements']=general+([no_credit] if no_credit else [])
            if (item,roman)!=(scheme_item,scheme_roman):
                assert (unit,item,roman,scheme_item,scheme_roman)==('L4',1,None,1,'i')
                c['rubric']['markingGuideNote']='The booklet labels this question1; scheme physical page14 prints1.i. This card follows the booklet.'
            # Match the published curriculum labels to the actual question.
            topics=[['russian-0-9','russian-0-14','russian-0-9','russian-0-8','russian-0-3'],
                    ['russian-0-7','russian-0-3','russian-0-3','russian-0-1'],
                    ['russian-0-5','russian-0-8','russian-0-5','russian-0-5'],
                    ['russian-0-7','russian-0-4','russian-2-5','russian-0-4']]
            c['topicId']=topics[section-1][index]
            c['additionalTopicIds']=['russian-1-0']
            c['sourceMaterial']['kind']='source-question';c['sourceMaterial']['presentationNote']='Listen to the official recording and answer the printed question. The transcript is not shown before answering.'
            c['audioMaterial']=audio;c['review']['guidancePages']=[12];cards.append(c)
    assert len(cards)==17 and sum(c['totalMarks'] for c in cards)==100
    return cards


def build():
    docs=opened_sources();P=RuPaper(2018,'ol')
    cards=reading(docs,P)+language_and_matching(docs)+writing(docs)+listening(docs)
    assert len(cards)==43 and sum(c['totalMarks'] for c in cards)==320
    old={c['id'] for c in json.loads((ROOT/'scripts/markbank/authored/russian.json').read_text())}
    assert not any(c['id'] in old for c in cards)
    return cards


if __name__=='__main__':save_reviewed(build())
