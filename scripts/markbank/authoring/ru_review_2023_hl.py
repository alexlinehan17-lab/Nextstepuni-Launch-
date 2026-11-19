#!/usr/bin/env python3
"""Original-PDF selectors for the independently counted 2023 Higher sitting."""
import hashlib
import json
import re
from difflib import SequenceMatcher
import fitz
from ru_paper import RuPaper
from ru_scheme import RuScheme
from ru_review_2026_hl import ROOT, squash, between, bullets, as_points, bands as shared_bands, mark_range, save_reviewed, attach_language_rule
from ru_review_2026_hl import base as base_2026, page_text

FILES = {
    'paper': ('examiner-reports/russian/papers/2023-hl-000-paper.pdf', '84c1b64263f16512a296609cc8e6725dccc9c1256ada024183e8f7b2cc29e5b4'),
    'aural': ('examiner-reports/russian/papers/2023-hl-A00-paper.pdf', '37f2bd651bc04a93dbd619085ba3eecb44e1976e21d224b87c677b7fdcb284b6'),
    'scheme': ('examiner-reports/russian/schemes/2023-hl.pdf', '63933208c9846387f93bba3f48c13ec4d8821d7f3af1597998bcc8c531d983de'),
}

def opened_sources():
    docs = {}
    for key, (path, digest) in FILES.items():
        path = ROOT / path
        assert hashlib.sha256(path.read_bytes()).hexdigest() == digest, path
        docs[key] = fitz.open(path)
    return docs

def draw_text(doc, page):
    # Preserve the wrapped two-column lists in the PDF's reading order.
    # Clip only the running footer; retain all printed answer continuations.
    return doc[page-1].get_text('text', clip=fitz.Rect(20,30,580,795), sort=False)

def base(*args, **kwargs):
    card = base_2026(*args, **kwargs)
    for field in ('id', 'questionRef'):
        card[field] = card[field].replace('2026', '2023')
    card['year'] = 2023
    card['sourceMaterial']['title'] = card['sourceMaterial']['title'].replace('2026', '2023')
    return card

def bands(S, page, kind):
    if kind != 'guided':
        return shared_bands(S, page, kind)
    # The 2023 table prints normal E first, then lower E. Read its headers.
    table = S[page-1].find_tables().tables[0].extract()
    assert table[0][1] == 'E' and table[0][4] == 'Lower E' and table[1][1] == 'Ex 15' and table[1][4] == 'Ex 10', table[:2]
    full, lower = [], []
    for row in table[2:]:
        normal, reduced, description = [cell for cell in row if cell]
        full.append({'label': squash(normal), 'marks': mark_range(normal), 'guidance': [squash(description)]})
        lower.append({'label': squash(reduced), 'marks': mark_range(reduced), 'guidance': [squash(description)]})
    assert [b['marks'][-1] for b in full] == [15,10,5]
    assert [b['marks'][-1] for b in lower] == [10,6,3]
    return full, lower


def writing(docs):
    S, Q = docs['scheme'], docs['paper']
    # Read the English instructions and the complete bilingual topic pool from
    # the paper's own text order. No example essay is invented.
    paper = squash(Q[11].get_text())
    question = 'Write a short essay' + between(paper, 'Write a short essay')
    question += '\n\n' + '\n'.join('• ' + part.strip() for part in paper.split('•')[1:]).split('Teideal/Title')[0].strip()
    assert 'Столица Российской Федерации' in question and 'Транспорт в Российской Федерации' in question
    content_page = page_text(S, 12)
    content = bullets(between(content_page, 'Communication/content (C)'))
    expression = bullets(between(page_text(S, 13, (20,30,580,255)), 'Expression (E)'))
    assert len(content) == 6 and len(expression) == 7, (content, expression)
    full, lower = bands(S, 13, 'essay')
    c = base('SE', question, 30, [12], [12, 13])
    c.pop('rows'); c.pop('tariffModel'); c['kind'] = 'rubric'
    c['rubric'] = {'system': 'language-writing', 'taskRequirements': [], 'markingGuideNote': '', 'criteria': [
        {'id': 'content', 'label': 'Communication/content (C)', 'maxMarks': 10,
         'permittedMarks': [0, 2, 4, 6, 8, 10], 'guidance': content},
        {'id': 'title-penalty', 'label': 'Essay title penalty', 'kind': 'deduction', 'deductFrom': 'content',
         'maxMarks': 1, 'permittedMarks': [0, 1], 'guidance': [content[-1]]},
        {'id': 'expression', 'label': 'Language + expression (E)', 'maxMarks': 20,
         'permittedMarks': list(range(21)), 'guidance': expression, 'bands': full,
         'limits': [{'id': 'lower-e', 'maxMarks': 14, 'when': {'any': [
                         {'criterionIds': ['content'], 'atMost': 5, 'ignoreDeductions': True},
                         {'length': 'words', 'below': 25}]}, 'bands': lower, 'guidance': [expression[2]]},
                    {'id': 'no-content', 'maxMarks': 0, 'when': {'any': [
                         {'criterionIds': ['content'], 'atMost': 0, 'ignoreDeductions': True}]}, 'guidance': [content[2]]}]},
        {'id': 'soft-sign-penalty', 'label': 'Soft signs penalty', 'kind': 'deduction', 'deductFrom': 'expression',
         'maxMarks': 2, 'permittedMarks': [0, 1, 2], 'guidance': [expression[-1]]},
    ]}
    # All six choices share the40-mark grid. One complete choice pool avoids
    # six copies of the same practice task; all six prompts fit on page13.
    question = '\n'.join(page_text(Q, p, (309, 35, 580, 775)) for p in (13,))
    question = 'Write a piece' + between(question, 'Write a piece')
    assert all(term in question for term in ('1. LETTER', '2. NARRATIVE', '3. DISCUSSION', 'DISCUSSION'))
    g = base('GW', question, 40, [13], [14, 15, 16])
    g.pop('rows'); g.pop('tariffModel'); g['kind'] = 'rubric'
    scheme = page_text(S, 15)
    content = bullets(between(scheme, 'Communication/content (C)', '2.'))
    expression = bullets(between(page_text(S, 15, (20,30,580,445)), 'Expression (E):'))
    full, lower = bands(S, 15, 'guided')
    coherence, _ = bands(S, 16, 'coherence')
    g['rubric'] = {'system': 'language-writing', 'taskRequirements': [squash(page_text(S, 14))],
                   'markingGuideNote': '', 'criteria': [
        {'id': 'content', 'label': 'Communication + content (C)', 'maxMarks': 15,
         'permittedMarks': list(range(16)), 'guidance': content},
        {'id': 'expression', 'label': 'Language + expression (E)', 'maxMarks': 15,
         'permittedMarks': list(range(16)), 'guidance': expression, 'bands': full,
         'limits': [{'id': 'lower-e', 'maxMarks': 10, 'when': {'any': [
                         {'criterionIds': ['content'], 'atMost': 7}, {'length': 'words', 'below': 60}]},
                     'bands': lower, 'guidance': [expression[1]]}]},
        {'id': 'coherence', 'label': 'Textual coherence (TC)', 'maxMarks': 10,
         'permittedMarks': list(range(11)), 'guidance': [], 'bands': coherence},
        {'id': 'soft-sign-penalty', 'label': 'Soft sign penalty', 'kind': 'deduction', 'deductFrom': 'expression',
         'maxMarks': 2, 'permittedMarks': [0, 2], 'guidance': [expression[-1]]},
    ]}
    return [c, g]

def reading(docs, P):
    S = docs['scheme']
    cards = []
    text = '\n'.join(draw_text(S, p) for p in (4, 5))
    heads = list(re.finditer(r'^\s*([1-4])\.\s*\((i{1,3}|iv)\)\s+(?=[A-Z])', text, re.M))
    general = bullets(text[:heads[0].start()])
    assert len(general) == 4
    keys = [(1,'i',2),(1,'ii',2),(1,'iii',3),(2,'i',3),(2,'ii',3),
            (3,'i',2),(3,'ii',2),(4,'i',1),(4,'ii',2)]
    assert len(heads) == len(keys)
    for i, (head, (item, roman, count)) in enumerate(zip(heads, keys)):
        assert (int(head.group(1)), head.group(2)) == (item, roman)
        block = text[head.end():heads[i+1].start() if i+1 < len(heads) else len(text)]
        cue, body = block.split('assign two marks:', 1)
        cue = squash(re.sub(r'\d+\s*x\s*2\s*marks', '', cue))
        question, page, source = P.find('C1', item, roman, cue)
        assert question and source.side == 'R', (item, roman, cue)
        partials, extra = {}, []
        if 'assign no marks' in body:
            body, rejected = body.split('assign no marks', 1)
            extra.append('assign no marks' + squash(rejected))
        if 'assign one mark:' in body:
            body, partial = body.split('assign one mark:', 1)
            assert (item, roman) == (4,'ii') and squash(partial) == 'arrived by bike'
            partials = {1:[squash(partial)]}
        answers = bullets(body)
        assert len(answers) == [4,3,8,11,9,6,3,2,6][i], (item,roman,answers)
        c = base('C1', question, count*2, [2,3,4], [4,5], item, roman)
        c['review']['questionPages'] = [page]
        as_points(c, answers, count, partials)
        c['rubric']['taskRequirements'] = general + extra
        cards.append(c)
    assert sum(c['totalMarks'] for c in cards) == 40

    rule = 'Award 2 marks for each ' + squash(between(draw_text(S,7), 'Award 2 marks for each'))
    assert 'of 4 details (up to 8 marks) AND 2 discretionary marks' in rule
    summary = draw_text(S,8)
    heads = list(re.finditer(r'^\s*([1-4])\.\s+(?=[A-Z])', summary, re.M))
    assert len(heads) == 4
    for index, (head, counts) in enumerate(zip(heads, [(14,2),(12,9),(6,9),(9,7)])):
        item = index+1
        block = summary[head.end():heads[index+1].start() if index+1 < len(heads) else len(summary)]
        cue, rest = block.split('Main points:',1)
        cue = squash(re.sub(r'10\s*marks', '', cue))
        question, page, source = P.find('C2', item, None, cue)
        assert question and source.side == 'R', (item, cue)
        main, secondary = rest.split('Secondary details:',1)
        main_answers = [squash(part) for part in main.split('+')]
        secondary = [squash(part) for part in secondary.split('+')]
        assert (len(main_answers),len(secondary)) == counts, (item,main_answers,secondary)
        c = base('C2', question, 10, [6,7,8], [7,8], item)
        c['review']['questionPages'] = [page]
        as_points(c, main_answers+secondary, 4, steps=[0,1,2],
                  labels=['Main point']*len(main_answers)+['Secondary detail']*len(secondary))
        c['rubric']['taskRequirements'] = [rule]
        c['rubric']['criteria'] = [{'id':'summary-skills','label':'Discretionary marks',
            'maxMarks':2,'permittedMarks':[0,1,2],'guidance':[rule],
            'limits':[{'id':'incomplete-response','maxMarks':1,
                'when':{'any':[{'flag':'incomplete-response','prompt':squash(rule[rule.index('If a candidate fails'):])}]},
                'guidance':[rule]}]}]
        cards.append(c)
    return cards


def language_and_matching(docs, P):
    S,Q = docs['scheme'],docs['paper']
    scheme = RuScheme(2023,'hl')
    cards=[]
    for unit, page, paper_pages in [('LA1',6,[2,3,4,5]),('LA2',9,[6,7,8,9])]:
        tasks=scheme.tasks(unit)
        assert len(tasks)==2
        for roman,task in zip(('i','ii'),tasks):
            question=P.instruction(unit,roman)
            assert question
            if unit=='LA2' and roman=='ii':
                pool=between(draw_text(S,9), 'In Section 1 of the text find five words related to ‘Music’ and list them in Russian.')
                answers=[line.strip() for line in pool.splitlines() if line.strip()]
                assert len(answers)==18 and answers[-1]=='разогрев',answers
            else:
                answers=[f'{left} — {right}' for left,right in task.pairs]
                assert len(answers)==5,(unit,roman,answers)
            c=base(unit,question,10,paper_pages,[page],roman=roman)
            as_points(c,answers,5)
            if unit=='LA1' and roman=='i':
                c['rubric']['taskRequirements']=['Do not assign any marks where candidates translate the phrases into English.']
            cards.append(c)
    question=squash(page_text(Q,10,(297,30,580,180)))
    question=question[question.index('Match the following professions'):]
    table=S[9].find_tables().tables[0].extract()
    answers=[squash(row[0]) for row in table if row[0] and re.fullmatch(r'\d+',squash(row[0]))]
    assert answers==['7','5','8','6','1','2','10','3','9','4'],table
    c=base('SD',question,20,[10],[10]);as_points(c,[f'{i} — {a}' for i,a in enumerate(answers,1)],10)
    c['rubric']['markingGuideNote']='Rows are numbered from top to bottom in the original table. Award 2 marks for each correct answer.'
    cards.append(c)
    question=squash(page_text(Q,11,(297,30,580,340)))
    question=question[question.index('Read through the following text.'):]
    end='No marks are awarded for incorrectly spelled words or substitute words.'
    question=question[:question.index(end)+len(end)]
    forms=[]
    for block in S[10].get_text('dict')['blocks']:
        for line in block.get('lines',[]):
            for span in line['spans']:
                if span['bbox'][1]>260 and 'Bold' in span['font'] and re.search('[А-Яа-яЁё]',span['text']):
                    forms.append(squash(span['text']))
    assert len(forms)==14 and forms[5]=='Олимпийском музеe',forms
    assert sum(len(form.split()) for form in forms)==15
    c=base('GR',question,30,[11],[11]);as_points(c,forms,14)
    # The printed tariff is per correct form (15 x2). One bracketed phrase
    # contains two separately inflected words; keep it one visible gap.
    phrase=c['rubric']['groups'][5]
    phrase['label']=forms[5]
    phrase['answerCount']=2
    phrase['rows']=[{'id':f'form-{i}','text':form,'marks':2} for i,form in enumerate(forms[5].split(),1)]
    c['rubric']['taskRequirements']=['TWO marks per correct form', '15 x 2 marks']+bullets(between(draw_text(S,11),'In this exercise answers are either right or wrong:', 'Прошлым летом'))
    c['rubric']['markingGuideNote']='The paper has 14 bracketed gaps. The scheme prices 15 correct forms at 2 marks each; the phrase Олимпийском музеe contains two forms within one gap.'
    cards.append(c)
    return cards


def listening(docs,P):
    S=docs['scheme']
    audio=next(row['source'] for row in json.loads((ROOT/'data/russianAudio.json').read_text()) if row['year']==2023)
    asks=P.aural_asks();assert len(asks)==20,asks
    cards=[]
    general=bullets(between(draw_text(S,17),'General:','SECTION I'))
    assert len(general)==4 and 'no penalty for excess material' in ' '.join(general)
    assert 'contradictory' not in ' '.join(general)
    sections=[(1,17,[2],[2,2,3,2,1]),(2,18,[3,4],[1,2,2,2,1,2]),
              (3,19,[5],[2,3,3,2]),(4,20,[6],[3,1,2,3,1])]
    for section,page,paper_pages,counts in sections:
        unit=f'L{section}';source=draw_text(S,page)
        assert 'Award 2 marks per each detail.' in squash(source)
        heads=list(re.finditer(r'^\s*(\d)\.\s*(?:\((i{1,3})\))?\s*(?=[A-Z])',source,re.M))
        questions=[a for a in asks if a[0]==unit]
        assert len(heads)==len(questions)==len(counts),(unit,[(h.group(),h.start()) for h in heads],questions)
        for index,(head,ask,count) in enumerate(zip(heads,questions,counts)):
            _,item,roman,question=ask
            assert (int(head.group(1)),head.group(2))==(item,roman)
            block=source[head.end():heads[index+1].start() if index+1<len(heads) else len(source)]
            block=re.sub(r'Segment\s+\d+:?','',block)
            cue,rest=block.split('•',1);cue=squash(cue)
            assert SequenceMatcher(None,squash(question).lower(),cue.lower()).ratio()>.9,(question,cue)
            extra=[];special=''
            for delimiter in ('Accept mention of','Award 2 marks for mention','Candidates must mention'):
                if delimiter in rest:
                    rest,special=rest.split(delimiter,1);special=delimiter+' '+squash(special)
                    extra.append(special)
                    break
            answers=bullets('•'+rest)
            c=base(unit,question,count*2,paper_pages,[page],item,roman);as_points(c,answers,count)
            if (unit,item,roman)==('L2',2,'ii'):
                example=between(special,"e.g. '").rstrip("'")
                c['rubric']['groups'].append({'id':'vegetarian-context','label':'Vegetarian answer with correct context',
                    'answerCount':1,'rows':[{'id':'full','text':example,'marks':2}]})
            if (unit,item,roman)==('L3',1,'ii'):
                countries=between(special,'(',')').split('/')
                assert countries==['Turkey','Egypt','Bulgaria','Greece']
                c['rubric']['groups'].append({'id':'countries','label':'One country detail',
                    'answerCount':1,'rows':[{'id':f'country-{i}','text':name,'marks':2} for i,name in enumerate(countries,1)]})
            if (unit,item,roman)==('L4',3,None):
                assert len(answers)==9
                c['rubric']['allocationCap']={'maxMarks':6,'answerCount':3,'sourceText':special,'schemePages':[20]}
                extra.remove(special)  # The cap panel renders this source rule once.
                hockey=[2,4,5,6,7,8]
                c['rubric']['groups']=[g for i,g in enumerate(c['rubric']['groups']) if i not in hockey]
                c['rubric']['groups'].append({'id':'hockey','label':'Hockey details (maximum 4 marks)',
                    'answerCount':2,'rows':[{'id':f'detail-{i+1}','text':answers[i],'marks':2} for i in hockey]})
            if section==1:
                topic=('russian-0-9' if roman=='i' else 'russian-2-2') if item==1 else 'russian-0-8' if item==2 else 'russian-0-9'
            elif section==2:
                topic='russian-2-0' if item==2 and roman=='ii' else 'russian-0-2' if item==2 else 'russian-0-6' if item==3 and roman=='ii' else 'russian-0-8' if item==1 and roman=='ii' else 'russian-0-3'
            elif section==3:topic='russian-0-8'
            else:topic='russian-0-1' if item==2 and roman=='i' else 'russian-0-5' if item==3 else 'russian-0-7'
            c['topicId']=topic;c['additionalTopicIds']=['russian-1-0']
            c['rubric']['taskRequirements']=general+extra
            c['sourceMaterial']['kind']='source-question'
            c['sourceMaterial']['presentationNote']='Listen to the official recording and answer the printed question. The transcript is not shown before answering.'
            c['audioMaterial']=audio;c['review']['guidancePages']=[17]
            cards.append(c)
    assert len(cards)==20 and sum(c['totalMarks'] for c in cards)==80
    return cards


def build():
    docs=opened_sources();P=RuPaper(2023,'hl')
    cards=reading(docs,P)+language_and_matching(docs,P)+writing(docs)+listening(docs,P)
    assert len(cards)==41 and sum(c['totalMarks'] for c in cards)==320
    old_ids={c['id'] for c in json.loads((ROOT/'scripts/markbank/authored/russian.json').read_text())}
    for c in cards:
        if c['id'] in old_ids:c['review']['correctsExisting']=True
    attach_language_rule(cards,docs['scheme'])
    assert sum(c['review'].get('correctsExisting',False) for c in cards)==16
    assert sum(bool(c.get('answerLanguageRule')) for c in cards)==18
    from ru_summary_language_rules import attach_reviewed_summary_language_exceptions
    return attach_reviewed_summary_language_exceptions(cards)


if __name__=='__main__':save_reviewed(build())
