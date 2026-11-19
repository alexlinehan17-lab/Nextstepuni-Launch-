#!/usr/bin/env python3
"""Original-PDF selectors for the independently counted 2022 Higher sitting."""
import hashlib
import json
import re
from difflib import SequenceMatcher
import fitz
from ru_paper import RuPaper
from ru_scheme import RuScheme
from ru_review_2026_hl import ROOT, squash, between, bullets, as_points, bands, mark_range, save_reviewed, attach_language_rule
from ru_review_2026_hl import base as base_2026, page_text

FILES = {
    'paper': ('examiner-reports/russian/papers/2022-hl-000-paper.pdf', '73b129f223b597be6e096ded274e54b6fbc43260ee0f0b4c356b9477e956b273'),
    'aural': ('examiner-reports/russian/papers/2022-hl-A00-paper.pdf', '86914ac9598814d8c89db30655a24271c4d5f97ddbfe1d0e976938d495f7bb6d'),
    'scheme': ('examiner-reports/russian/schemes/2022-hl.pdf', '7f539dcb7b70c18e30b1047e463426bd2715926ddfe16a6daa0a93b995907071'),
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
        card[field] = card[field].replace('2026', '2022')
    card['year'] = 2022
    card['sourceMaterial']['title'] = card['sourceMaterial']['title'].replace('2026', '2022')
    return card

def writing(docs):
    S, Q = docs['scheme'], docs['paper']
    # Read the English instructions and the complete bilingual topic pool from
    # the paper's own text order. No example essay is invented.
    paper = squash(Q[11].get_text())
    question = 'Write a short essay' + between(paper, 'Write a short essay', 'Напишите')
    question += '\n\n' + '\n'.join('• ' + part.strip() for part in paper.split('•')[1:]).split('Teideal/Title')[0].strip()
    assert 'Русский язык в Ирландии' in question and 'Праздники' in question
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
    question = '\n'.join(page_text(Q, p, (297, 35, 580, 775)) for p in (13,))
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
    heads = list(re.finditer(r'^\s*([1-4])\.\s*(?:\((i{1,3}|iv)\))?\s+(?=[A-Z])', text, re.M))
    general = bullets(text[:heads[0].start()])
    assert len(general) == 4
    keys = [(1,'i',3),(1,'ii',3),(1,'iii',1),(2,'i',2),(2,'ii',2),
            (3,'i',3),(3,'ii',1),(3,'iii',3),(4,None,2)]
    assert len(heads) == len(keys)
    for i, (head, (item, roman, count)) in enumerate(zip(heads, keys)):
        assert (int(head.group(1)), head.group(2)) == (item, roman)
        block = text[head.end():heads[i+1].start() if i+1 < len(heads) else len(text)]
        cue, body = block.split('assign two marks:', 1)
        cue = squash(re.sub(r'\(?\d+\s*x\s*2\s*marks\)?', '', cue))
        question, page, source = P.find('C1', item, roman, cue)
        assert question and source.side == 'R', (item, roman, cue)
        partials, extra = {}, []
        if 'assign no marks' in body:
            body, rejected = body.split('assign no marks', 1)
            extra.append('assign no marks' + squash(rejected))
        answers = [squash(part) for part in body.split('+')]
        assert len(answers) == [9,11,3,6,4,7,1,5,6][i], (item,roman,answers)
        c = base('C1', question, count*2, [2,3,4], [4,5], item, roman)
        c['review']['questionPages'] = [page]
        as_points(c, answers, count, partials)
        c['rubric']['taskRequirements'] = general + extra
        cards.append(c)
    assert sum(c['totalMarks'] for c in cards) == 40

    summary = '\n'.join(draw_text(S,p) for p in (7,8))
    heads = list(re.finditer(r'^\s*([1-4])\.\s+(?=[A-Z])', summary, re.M))
    rule = 'Award 2 marks for each ' + squash(between(summary[:heads[0].start()], 'Award 2 marks for each'))
    assert 'of 4 details (up to 8 marks) AND 2 discretionary marks' in rule
    assert len(heads) == 4
    for index, (head, counts) in enumerate(zip(heads, [(12,6),(10,6),(10,5),(14,8)])):
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
    cards=[]
    for unit,page,paper_pages in [('LA1',6,[2,3,4,5]),('LA2',9,[6,7,8,9])]:
        for roman in ('i','ii'):
            question=P.instruction(unit,roman)
            if unit=='LA1':
                if roman=='i':
                    text=squash(page_text(Q,5,(297,30,580,400)))
                    question='Supply'+between(text,'Supply','text.')+'text.'
                table=S[5].find_tables().tables[0 if roman=='i' else 1].extract()
                answers=[f'{squash(left)} — {squash(right)}' for left,right in table]
                assert len(answers)==5
            elif roman=='i':
                question=question[question.index('In the text'):]
                pool=between(draw_text(S,9),'In the text find five words related to ‘Higher Education’ and list them in Russian.','NÓ / OR')
                answers=[line.strip() for line in pool.splitlines() if line.strip()]
                assert len(answers)==33 and answers[-1]=='Факультет',answers
            else:
                question=question[question.index('Indicate'):]
                table=S[8].find_tables().tables[0].extract()
                answers=[f'{squash(left)} — {squash(right)}' for left,right in table]
                assert len(answers)==5
            assert question
            c=base(unit,question,10,paper_pages,[page],roman=roman)
            as_points(c,answers,5)
            if unit=='LA1' and roman=='i':
                c['rubric']['taskRequirements']=['Do not assign any marks where candidates translate the phrases into English.']
            if unit=='LA1' and roman=='ii':
                c['rubric']['taskRequirements']=['You may write your answer in Irish, English or Russian.']
            if unit=='LA2' and roman=='ii':
                c['rubric']['markingGuideNote']='The marking scheme accepts the English and Russian case names printed below.'
            cards.append(c)
    question=squash(page_text(Q,10,(297,30,580,200)))
    question=question[question.index('Read the following brief news items.'):]
    table=S[9].find_tables().tables[0].extract()
    answers=[squash(row[0]) for row in table if row[0] and re.fullmatch(r'\d+',squash(row[0]))]
    assert answers==['9','6','8','2','3','5','7','1','10','4'],table
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
                    forms.append(squash(span['text']).rstrip(','))
    assert len(forms)==14 and forms[10]=='близкими людьми',forms
    assert sum(len(form.split()) for form in forms)==15
    c=base('GR',question,30,[11],[11]);as_points(c,forms,14)
    # Source prices15 correct forms (15 x2), with two inflected words in
    # one bracketed phrase. Keep the original gap and each claimable form.
    phrase=c['rubric']['groups'][10]
    phrase['label']=forms[10];phrase['answerCount']=2
    phrase['rows']=[{'id':f'form-{i}','text':form,'marks':2} for i,form in enumerate(forms[10].split(),1)]
    c['rubric']['taskRequirements']=['TWO marks per correct form','15 x 2 marks']+bullets(between(draw_text(S,11),'In this exercise answers are either right or wrong:','Анастасия'))
    c['rubric']['markingGuideNote']='The paper has 14 bracketed gaps. The scheme prices 15 correct forms at 2 marks each; the phrase близкими людьми contains two forms within one gap.'
    cards.append(c)
    return cards


def listening(docs,P):
    S=docs['scheme']
    audio=next(row['source'] for row in json.loads((ROOT/'data/russianAudio.json').read_text()) if row['year']==2022)
    asks=P.aural_asks();assert len(asks)==23,asks
    cards=[]
    general=bullets(between(draw_text(S,17),'General:','SECTION I'))
    assert len(general)==5 and general[-1]=='Accept answers written in Russian.'
    sections=[(1,17,[2,3],[1,2,2,1,2,2]),(2,18,[4,5],[1,3,1,2,1,2]),
              (3,19,[6],[2,3,3,1,1]),(4,20,[7],[2,2,2,2,1,1])]
    expected_pools=[[1,3,6,2,6,6],[2,6,1,6,4,5],[3,4,8,3,1],[4,4,7,5,2,3]]
    for section,page,paper_pages,counts in sections:
        unit=f'L{section}';source=draw_text(S,page)
        heads=list(re.finditer(r'^\s*(\d)\.\s*(?:\((i{1,3})\))?\s*(?=[A-Z])',source,re.M))
        questions=[a for a in asks if a[0]==unit]
        assert len(heads)==len(questions)==len(counts),(unit,[(h.group(),h.start()) for h in heads],questions)
        for index,(head,ask,count) in enumerate(zip(heads,questions,counts)):
            _,item,roman,question=ask
            assert (int(head.group(1)),head.group(2))==(item,roman)
            if (unit,item,roman)==('L4',3,'ii'):
                # Legacy question collector reaches the closing cover text.
                assert '\nRúisis' in question
                question=question.split('\nRúisis',1)[0]
            block=source[head.end():heads[index+1].start() if index+1<len(heads) else len(source)]
            price=re.search(r'(\d+)\s*x\s*2\s*marks',block)
            assert price and int(price.group(1))==count,(unit,item,roman,block)
            cue=squash(block[:price.start()]);rest=block[price.end():]
            assert SequenceMatcher(None,squash(question).lower(),cue.lower()).ratio()>.94,(question,cue)
            extra=[]
            no_credit=re.search(r'(?i)award no marks:',rest)
            if no_credit:
                extra=[squash(rest[no_credit.start():])];rest=rest[:no_credit.start()]
            answers=[squash(part) for part in rest.split('+')]
            assert len(answers)==expected_pools[section-1][index],(unit,item,roman,answers)
            c=base(unit,question,count*2,paper_pages,[page],item,roman);as_points(c,answers,count)
            if section==1:
                topic='russian-0-3' if item==1 else 'russian-0-8' if item in (2,3) else 'russian-0-9'
            elif section==2:
                topic='russian-0-11' if item==1 and roman=='i' else 'russian-0-3' if item in (1,2) else 'russian-0-6' if item==3 else 'russian-0-8'
            elif section==3:
                topic='russian-0-9' if item==1 or (item==4 and roman=='ii') else 'russian-0-5' if item==2 else 'russian-0-3' if item==3 else 'russian-2-1'
            else:
                topic='russian-0-1' if item==1 and roman=='i' else 'russian-0-5' if item==1 else 'russian-0-4' if (item==2 and roman=='i') or (item==3 and roman=='i') else 'russian-0-7' if item==2 else 'russian-0-11'
            c['topicId']=topic;c['additionalTopicIds']=['russian-1-0']
            c['rubric']['taskRequirements']=general+extra
            c['sourceMaterial']['kind']='source-question'
            c['sourceMaterial']['presentationNote']='Listen to the official recording and answer the printed question. The transcript is not shown before answering.'
            c['audioMaterial']=audio;c['review']['guidancePages']=[17]
            cards.append(c)
    assert len(cards)==23 and sum(c['totalMarks'] for c in cards)==80
    return cards


def build():
    docs=opened_sources();P=RuPaper(2022,'hl')
    cards=reading(docs,P)+language_and_matching(docs,P)+writing(docs)+listening(docs,P)
    assert len(cards)==44 and sum(c['totalMarks'] for c in cards)==320
    old_ids={c['id'] for c in json.loads((ROOT/'scripts/markbank/authored/russian.json').read_text())}
    for c in cards:
        if c['id'] in old_ids:c['review']['correctsExisting']=True
        if not c.get('audioMaterial'):
            c['sourceMaterial']['presentationNote'] += ' The 2022 paper offers 170 written marks: choose Question 1 or Question 2 in Section I, plus Question 3, and complete Section II. All alternatives remain available here for practice.'
    attach_language_rule(cards,docs['scheme'])
    assert sum(c['review'].get('correctsExisting',False) for c in cards)==14
    assert sum(bool(c.get('answerLanguageRule')) for c in cards)==18
    from ru_summary_language_rules import attach_reviewed_summary_language_exceptions
    return attach_reviewed_summary_language_exceptions(cards)


if __name__=='__main__':save_reviewed(build())
