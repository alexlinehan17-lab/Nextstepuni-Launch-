#!/usr/bin/env python3
"""Publish the independently censused 2011 Ordinary sitting from PDF selectors.

Question/answer/guidance strings below are selected from the original PDFs.
Finite choices and required response pools remain single tasks. The census does not import this file or its output.
"""
import argparse
import hashlib
import json
import os
import re
from pathlib import Path

import fitz
from ja_text import page_rows
from ja_topics import FURIGANA_NOTE, concept_for

ROOT = Path(__file__).resolve().parents[3]
PATHS = {
    'paper': ROOT / 'examiner-reports/japanese/papers/2011-ol-000-paper.pdf',
    'aural': ROOT / 'examiner-reports/japanese/papers/2011-ol-A00-paper.pdf',
    'scheme': ROOT / 'examiner-reports/japanese/schemes/2011-ol.pdf',
}
HASHES = {
    'paper': '8f3cc484584f2f3d92d8ff527ea504244f3cdecd7bb9a317050a6c18f3788a6d',
    'aural': '309948b6752e84404c0643b54cb99d0caf72ec7b46193ef1cbc84e2a33b718d8',
    'scheme': 'bd5bd566ecfa9376f427f74b7d727ad568ac2d948bddc6845a12eda9eefef2a4',
}
for name, path in PATHS.items():
    assert hashlib.sha256(path.read_bytes()).hexdigest() == HASHES[name], path
DOCS = {name: fitz.open(path) for name, path in PATHS.items()}
ROWS = {name: [page_rows(page) for page in doc] for name, doc in DOCS.items()}
CARDS, EVIDENCE, FIGURES, BINDINGS, CORRECTIONS = [], [], {}, [], []
EXISTING_FIGURES = json.loads((ROOT / 'components/MarkBank/figures-japanese.json').read_text())
ORIGINAL_IDS = set(re.findall(r'^    id: "([^\"]+)"', (ROOT / "components/MarkBank/cards/japanese/ordinary.ts").read_text(), re.M))
UNPRINTED = re.search(r"export const UNPRINTED_ANSWER = '([^']+)'", (ROOT / 'types/markBank.ts').read_text()).group(1)


def cell(doc, page, row, group=None):
    groups = ROWS[doc][page - 1][row]
    text = ' '.join(group[2] for group in groups) if group is None else groups[group][2]
    EVIDENCE.append({'document': doc, 'page': page, 'row': row, 'group': group, 'text': text})
    return text


def p(page, row, group=None):
    return cell('paper', page, row, group)


def without_marker(text):
    return re.sub(r'^(?:\d+\.|\([a-z]+\))\s*', '', text).strip()


def english(text):
    return text.replace('\xa0', ' ').split(' / ', 1)[-1].strip()


def col(doc, page, rows, xmin=300):
    text = ' '.join(' '.join(cell(doc, page, row, i) for i, group in enumerate(ROWS[doc][page - 1][row]) if group[0] >= xmin) for row in rows).strip()
    assert text, (doc, page, rows, xmin)
    return text


def s(page, row, group=0):
    return re.sub(r'\s*\(?\s*\d+\s*marks?\)?\s*$', '', cell('scheme', page, row, group)).strip().removeprefix('- ').strip()


def sa(page, row, group=0):
    return without_marker(s(page, row, group)).removeprefix('- ').strip()


def point(text, marks=1, **extra):
    return {'kind': 'point', 'verbatim': text, 'marks': marks, **extra}


def anyn(options, count, marks=1, steps=None, **extra):
    group = {'claimMax': count, 'perOption': marks, 'options': options}
    if steps:
        group['perOptionSteps'] = steps
    return {'kind': 'anyN', 'verbatim': 'Accepted answers', 'marks': None, 'group': group, **extra}


def worth(row):
    if row['kind'] != 'anyN':
        return row['marks']
    group = row['group']
    return sum(group['perOptionSteps']) if 'perOptionSteps' in group else group['claimMax'] * group['perOption']


def source(pages, component='paper'):
    return {'kind': 'source-text', 'label': '2011 Japanese Ordinary Level', 'title': 'Original examination material',
            'pages': pages, 'attribution': '© State Examinations Commission.',
            **({'presentationNote': FURIGANA_NOTE} if component == 'paper' else {}), '_component': component}


def crop(key, page, region, alt, component='paper'):
    doc = DOCS[component]
    sheet = doc[page - 1]
    rect = fitz.Rect(region[0] * sheet.rect.width, region[1] * sheet.rect.height, region[2] * sheet.rect.width, region[3] * sheet.rect.height)
    rel = f'/exam-figures/japanese/{key}.png'
    path = ROOT / 'public' / rel.lstrip('/')
    path.parent.mkdir(parents=True, exist_ok=True)
    metadata = {'src': rel, 'alt': alt, 'attribution': '© State Examinations Commission.',
                'source': {'document': component, 'page': page, 'region': region}}
    previous_path = ROOT / 'components/MarkBank/figures-japanese.json'
    previous = json.loads(previous_path.read_text()).get(key, {})
    current = path.exists() and all(previous.get(field) == value for field, value in metadata.items()) and previous.get('md5') == hashlib.md5(path.read_bytes()).hexdigest()
    proof_path = ROOT / 'tmp/japanese-review/2011-ol-crop-rendered.json'
    proofs = json.loads(proof_path.read_text()) if proof_path.exists() else {}
    if os.environ.get('JA_RENDER_ONLY') == key:
        sheet.get_pixmap(matrix=fitz.Matrix(2, 2), clip=rect).save(path)
        proofs[key] = {**metadata, 'md5': hashlib.md5(path.read_bytes()).hexdigest()}
        proof_path.write_text(json.dumps(proofs, ensure_ascii=False, indent=2) + '\n')
    elif path.exists() and not current:
        proof = proofs.get(key, {})
        valid = all(proof.get(field) == value for field, value in metadata.items()) and proof.get('md5') == hashlib.md5(path.read_bytes()).hexdigest()
        if not valid:
            assert os.environ.get('JA_RENDER_ONLY'), f'Crop metadata changed; rerender explicitly: {key}'
            FIGURES[key] = {**metadata, 'md5': None}
            return key
    FIGURES[key] = {**metadata, 'md5': hashlib.md5(path.read_bytes()).hexdigest() if path.exists() else None}
    return key



def add(section, q, question, rows, topic, pp, sp, suffix='', rubric=None, total=None, reading=None, figure=None, stem=None):
    cid = f'ja-2011-ol-{section.lower()}' + (f'-{q}' if q is not None else '') + (f'-{suffix}' if suffix else '')
    ref = f'2011 OL Section {section}' + (f' Q{q}' if q is not None else ' Q' if suffix else '') + ''.join(f'({part})' for part in suffix.split('-') if part)
    listening = section.startswith('L')
    card = {'id': cid, 'source': 'sec', 'subjectId': 'japanese', 'specVersion': 'lc-japanese-syllabus',
            'kind': 'rubric' if rubric else 'question', 'level': 'ordinary', 'year': 2011,
            'section': section[1:] if listening else section[0] if section[0] in '1234' else 'Q5',
            'topicId': topic, 'conceptId': concept_for(question, cid), 'questionRef': ref,
            'questionText': question, 'totalMarks': total if total is not None else sum(map(worth, rows)),
            'qa': {'gates': ['verbatim', 'tariff', 'figure'], 'humanReviewedBy': 'agent-verified', 'humanReviewedAt': '2026-11-12'},
            'sourceEvidence': {'component': 'aural' if listening else 'paper', 'paperPages': pp, 'schemePages': sp},
            'schemeCitation': 'Marking points quoted from the SEC marking scheme, Japanese 2011 Ordinary Level — © State Examinations Commission.'}
    if cid in ORIGINAL_IDS:
        card['qa']['gates'].append('reviewed-card-correction')
    if section[0] in '123' and cid != 'ja-2011-ol-1-2-ii':
        card['sourceEvidence']['generalSchemePages'] = [6]
        card['answerLanguageRule'] = {'otherLanguageMultiplier': 0.5, 'sourceText': cell('scheme', 6, 2), 'schemePages': [6]}
    if rubric:
        card['rubric'] = rubric
    else:
        card['tariffModel'] = {'kind': 'fixed'}
        card['rows'] = [dict(row, id=f'r-{i + 1}') for i, row in enumerate(rows)]
    if reading:
        card['sourceMaterial'] = source(reading, 'aural' if listening else 'paper')
    if figure:
        card['questionFigureKey'] = figure
    if stem:
        card['stem'] = stem
    CARDS.append(card)
    return card


def pool(count, labels, answers, marks, instruction, guide):
    return {'system': 'language-points', 'count': count, 'taskRequirements': [instruction],
            'groups': [{'id': f'item-{i + 1}', 'label': label, 'rows': [{'id': 'answer', 'text': answer, 'marks': marks}]} for i, (label, answer) in enumerate(zip(labels, answers))],
            'markingGuideNote': guide}


def options(page, rows, group=0, separator=','):
    text = ' '.join(s(page, row, group) for row in rows)
    text = re.sub(r'\s*\(any .*?\)', '', text, flags=re.I)
    return [part.strip() for part in text.split(separator)]


def joined_selector(doc, page, rows):
    text = ' '.join(cell(doc, page, row, group) for row, group in rows)
    EVIDENCE.append({'document': doc, 'page': page, 'parts': [{'row': row, 'group': group} for row, group in rows], 'text': text})
    return text

def clean_label(text):
    return re.sub(r'_+', '', text).strip()


def find_row(doc, page, phrase):
    found = [i for i, row in enumerate(ROWS[doc][page - 1]) if phrase in ' '.join(group[2] for group in row)]
    assert len(found) == 1, (doc, page, phrase, found)
    return found[0]



def group_rows(card, groups):
    card['taskGroups'] = [{'sourceCardId': card['id'] + '-' + name, 'label': label,
        'marks': sum(worth(row) for row in card['rows'][start:end]), 'rowIds': [row['id'] for row in card['rows'][start:end]]}
        for name, label, start, end in groups]


def criterion(text, maximum, allowed, note):
    return {'kind': 'criterion', 'verbatim': text, 'marks': maximum, 'permittedMarks': allowed, 'contextNote': note}


def reading_q1():
    labels = [english(p(3, r, 1 if r == 2 else 0)) for r in range(2, 10)]
    c = add('1', 1, p(3, 1) + '\n' + '\n'.join(labels),
        [point(s(6, r, 1), 2, contextNote=label) for r, label in zip(range(5, 13), labels)],
        'japanese-5-0', [3], [6], reading=[2], figure=crop('ja-2011-ol-1-1', 3, [.065, .025, .97, .32], p(3, 1)))
    group_rows(c, [(str(i + 1), label, i, i + 1) for i, label in enumerate(labels)])
    add('1', 2, clean_label(p(3, 11)), [point(s(6, 14).split('?')[1].strip(), 2, contextNote=cell('scheme', 6, 13))], 'japanese-5-0', [3], [6], 'i', reading=[2])
    exception = joined_selector('scheme', 6, [(15, 1), (16, 0)])
    guide = joined_selector('scheme', 6, [(2, None), (13, None), (15, 1), (16, 0)])
    guide += ' — Award 1 for correct Naeba in the appropriate language; 0 for Hiragana or incorrect content. Award 0.5 only for otherwise correct content in another inappropriate language, excluding Hiragana. These are whole-response marks; apply no second language reduction.'
    c = add('1', 2, clean_label(p(3, 13)), [criterion(exception, 1, [0, 0.5, 1], guide)], 'japanese-5-0', [3], [6], 'ii', reading=[2])
    c['sourceEvidence']['generalSchemePages'] = [6]
    date = s(6, 17).split('?')[1]
    parts = [part.strip() for part in re.split(r'\(1 mark\)', date) if part.strip()]
    assert parts == ['July', '30th']
    add('1', 2, english(p(3, 14)), [point(part, contextNote=cell('scheme', 6, 13)) for part in parts], 'japanese-5-0', [3], [6], 'iii', reading=[2])
    dates = s(6, 19).split('?')[1]
    parts = [part.strip() for part in dates.split('(1 mark)') if part.strip()]
    assert parts == ['13 / 14', 'August']
    add('1', 3, clean_label(p(3, 17)), [point(part, contextNote='The scheme prices 13 / 14 as one day component and August as one month component; no additional day tariff is printed.') for part in parts], 'japanese-5-0', [3], [6], 'i', reading=[2])
    cities = [part.strip() for part in s(6, 22).split('(1 mark)') if part.strip()]
    add('1', 3, p(3, 19), [point(city) for city in cities], 'japanese-5-0', [3], [6], 'ii', reading=[2])
    add('1', 3, p(3, 23) + '\n' + p(3, 24) + '\n' + p(3, 25), [point(s(6, 25, i)) for i in [0, 1]], 'japanese-5-0', [3], [6], 'iii', reading=[2],
        figure=crop('ja-2011-ol-1-3-iii', 3, [.10, .585, .97, .715], p(3, 23)))
    instruction = english(p(3, 26, 1))
    for roman, qr, sr in [('i', range(27,31),28),('ii',range(31,33),30),('iii',range(33,36),32)]:
        question = instruction + '\n' + '\n'.join(english(p(3, r)) for r in qr)
        note = 'Printed source discrepancy: the final two options are both labelled c (Fred and Naruto). The original choice labels are retained.' if roman == 'iii' else None
        add('1', 4, question, [point(s(6,sr),2,**({'contextNote':note} if note else {}))], 'japanese-5-0',[3],[6],roman,reading=[2])


def reading_q2():
    instruction = english(p(5,0))
    names = [p(5,2,i) for i in range(4)]
    fields = [joined_selector('paper',5,[(r,0) for r in rr]) for rr in [[5,6],[9,10,11],[14,15]]]
    rows,groups = [],[]
    for i,name in enumerate(names):
        start=len(rows)
        if i!=2:
            rows.extend([point(s(7,5,i+1),contextNote=name+' — '+fields[0]),point(s(7,8,i+1),contextNote=name+' — '+fields[1])])
        if i!=0: rows.append(point(s(7,12,i),contextNote=name+' — '+fields[2]))
        groups.append((str(i+1),name,start,len(rows)))
    c=add('2A',None,instruction+'\n'+'\n'.join(fields),rows,'japanese-5-1',[5],[7],reading=[4],figure=crop('ja-2011-ol-2a',5,[.065,.025,.97,.295],instruction))
    group_rows(c,groups)
    c['rows'][0]['contextNote']+=' — Paris Café, French and Wednesday are already given and earn no marks. '+cell('scheme',7,2)
    labels=[english(p(5,r,1 if r in [23,25] else None)) for r in [23,25,28,31,34,37,40,43]]
    rows=[]
    for i,(label,sr) in enumerate(zip(labels,[16,17,18,19,21,22,23,24])):
        rows.extend([point(re.sub(r'^\d+\.\s*','',s(7,sr)),contextNote=label+' — True or False'),point(s(7,sr,2),contextNote=label+' — Supporting phrase')])
    instruction=p(5,18)+' '+p(5,19)
    c=add('2B',None,instruction+'\n'+'\n'.join(labels),rows,'japanese-5-1',[5],[7],reading=[4],figure=crop('ja-2011-ol-2b',5,[.065,.30,.97,.95],instruction))
    group_rows(c,[(str(i+1),label,i*2,i*2+2) for i,label in enumerate(labels)])
    instruction=p(6,2)+' '+p(6,3)
    rows=[]
    # The source-local correction follows the same printed option b; both literals remain visible.
    for i,(sr,rg,mg) in enumerate([(3,1,3),(4,1,3),(5,0,2),(6,1,3),(8,1,3),(9,0,2),(10,1,3),(11,1,3)]):
        answer=s(8,sr,rg)
        answer=re.search(r'[a-d]\.\s*.+$',answer).group(0)
        note=p(6,7+i).split('a.',1)[0].strip()
        if i==0:
            printed=answer
            answer=p(6,7,2)
            note+=' — Source discrepancy: scheme prints '+printed+', while the paper prints '+p(6,7,1)+' and '+answer+'. The same printed option letter b identifies the paper’s にほん. This explicitly source-bound reading correction retains both original strings and the unchanged reading 1 / meaning 1 allocation.'
        rows.extend([point(answer,contextNote=note+' — Reading'),point(s(8,sr,mg),contextNote=note+' — Meaning')])
    c=add('2C',None,instruction+'\n'+'\n'.join(p(6,r) for r in range(7,15)),rows,'japanese-5-4',[6],[8],reading=[4],figure=crop('ja-2011-ol-2c',6,[.065,.025,.97,.475],instruction))
    group_rows(c,[(str(i+1),p(6,7+i).split('a.',1)[0].strip(),i*2,i*2+2) for i in range(8)])
    BINDINGS.append({'cardId':c['id'],'answer':p(6,7,2),'rowIds':['r-1'],
        'paperSelector':{'document':'paper','page':6,'row':7,'group':2,'text':p(6,7,2)},
        'schemeSelectors':[{'document':'scheme','page':8,'row':3,'group':1,'text':cell('scheme',8,3,1)}]})
    guide=cell('scheme',8,14,0)
    rubric={'system':'language-writing','taskRequirements':[p(6,17)+' '+p(6,18)],'criteria':[
        {'id':f'difference-{i}','label':f'Difference {i}','maxMarks':2,'permittedMarks':[0,2],'guidance':[guide]} for i in [1,2]]+
        [{'id':'discretionary','label':'Discretionary','maxMarks':1,'permittedMarks':[0,1],'guidance':[cell('scheme',8,15)]}],
        'markingGuideNote':guide+'; '+cell('scheme',8,15)+' — Assess two distinct differences. The scheme gives no model answer or further discretionary descriptor.'}
    add('2D',None,p(6,17)+' '+p(6,18)+'\n'+p(6,20),[],'japanese-5-6',[6],[8],total=5,rubric=rubric)


def reading_q3():
    instruction=p(9,2)+' '+p(9,3)
    rows=[point(s(9,r),contextNote='The completed Ireland example is unpriced. '+cell('scheme',9,2)) for r in range(4,12)]
    c=add('3A',1,instruction+'\n'+'\n'.join(p(9,r) for r in range(4,21)),rows,'japanese-5-0',[9],[9],reading=[8],figure=crop('ja-2011-ol-3a-1',9,[.065,.025,.97,.44],instruction))
    group_rows(c,[(str(i+1),row['verbatim'].split('=')[0].strip(),i,i+1) for i,row in enumerate(rows)])
    for roman,pr,sr in [('i',22,13),('ii',24,15)]:
        answer=cell('scheme',9,sr).split('?')[1]
        parts=[part.strip(' -') for part in answer.split('(1 mark)') if part.strip(' -')]
        add('3A',2,clean_label(p(9,pr)),[point(part, contextNote=joined_selector('scheme',9,[(sr,None),(sr+1,None)])) for part in parts],'japanese-5-0',[9],[9],roman,reading=[8])
    add('3A',3,clean_label(p(9,26)),[point(s(9,18).split('?')[1].strip(),2)],'japanese-5-0',[9],[9],'i',reading=[8])
    add('3A',3,clean_label(p(9,28)),[anyn([v.strip() for v in s(9,20).split('/')],2,1,contextNote=cell('scheme',9,19))],'japanese-5-0',[9],[9],'ii',reading=[8])
    add('3A',3,clean_label(p(9,30)),[point(s(9,21).split('activity.')[1].strip(),2)],'japanese-5-0',[9],[9],'iii',reading=[8])
    add('3A',3,p(9,33)+'\n'+p(9,34)+'\n'+p(9,35),[point(s(9,23),2)],'japanese-5-0',[9],[9],'iv',reading=[8])
    opts=[v.strip() for v in s(9,26).split('/')]
    add('3A',4,p(9,37),[anyn(opts,2,1,contextNote=cell('scheme',9,27))],'japanese-5-0',[9],[9],reading=[8])
    instruction=p(10,2)
    rows=[]
    for i,sr in enumerate(range(3,8)):
        answer=s(10,sr,0 if sr==6 else 1)
        answer=re.sub(r'^\([ivx]+\)\s*','',answer)
        note=p(10,4+i)
        if i==4:note+=' — Source discrepancy: scheme labels で as d, but the paper labels it b and has no d option. Preserve the answer text で and both literal labels.'
        rows.append(point(answer,2,contextNote=note))
    c=add('3B',1,instruction+'\n'+'\n'.join(p(10,r) for r in range(3,9)),rows,'japanese-5-5',[10],[10],reading=[8],figure=crop('ja-2011-ol-3b-1',10,[.065,.025,.97,.325],instruction))
    group_rows(c,[(str(i+1),p(10,4+i),i,i+1) for i in range(5)])
    instruction=p(10,10)
    rows=[point(re.sub(r'^\([ivx]+\)\.?\s*','',s(10,9+i)),m,contextNote=p(10,12+i,0)) for i,m in enumerate([2,2,2,2,1])]
    c=add('3B',2,instruction+'\n'+'\n'.join(p(10,r) for r in range(11,17)),rows,'japanese-5-5',[10],[10],reading=[8],figure=crop('ja-2011-ol-3b-2',10,[.065,.385,.97,.68],instruction))
    group_rows(c,[(str(i+1),p(10,12+i,0),i,i+1) for i in range(5)])


def writing():
    instruction=joined_selector('paper',11,[(1,0),(3,0)])
    question=instruction+'\n(a) '+p(11,5)+'\n'+'\n'.join(p(11,r) for r in range(6,25))+'\n'+p(11,25)+'\n(b) '+p(12,2)+'\n'+'\n'.join(p(12,r) for r in range(3,22))
    allocation=cell('scheme',11,5)
    criteria=[{'id':f'question-{i}','label':f'Selected question {i}','maxMarks':7,'permittedMarks':list(range(8)),'guidance':[allocation]} for i in range(1,6)]
    criteria.append({'id':'discretionary','label':'Discretionary content','maxMarks':5,'permittedMarks':list(range(6)),'guidance':[cell('scheme',11,6)]})
    desc=[col('scheme',12,range(a,b),190) for a,b in [(17,24),(24,31),(31,38)]]
    bands=lambda spans:[{'label':f'{lo}–{hi}','marks':list(range(lo,hi+1)),'guidance':[text]} for (lo,hi),text in zip(spans,desc)]
    criteria.append({'id':'expression','label':'Expression','maxMarks':40,'permittedMarks':list(range(41)),
        'guidance':[joined_selector('scheme',12,[(r,None) for r in range(1,9)]),joined_selector('scheme',12,[(38,None),(39,None)])],
        'bands':bands([(0,9),(10,27),(28,40)]),
        'limits':[{'id':'lower-e','maxMarks':26,'when':{'any':[{'criterionIds':[c['id'] for c in criteria],'atMost':20},{'length':'characters','below':150}]},
        'guidance':[joined_selector('scheme',12,[(r,None) for r in range(9,14)])],'bands':bands([(0,6),(7,16),(17,26)])}]})
    add('4',None,question,[],'japanese-5-7',[11,12],[11,12],total=80,reading=[11,12],rubric={'system':'language-writing','taskRequirements':[instruction],
        'criteria':criteria,'markingGuideNote':'Choose one complete option: music OR studying Japanese. Both sets of eight original questions are retained. Record five distinct selected questions, each up to 7 marks, and up to 5 discretionary marks under content. Do not mix options or score the same question twice. Multi-ask questions retain their whole 7-mark maximum; no internal split is published. The music paper says at least five, the Japanese option any five, and the scheme prices any five. Lower E26 applies when total content, including discretionary marks, is 20 or less OR fewer than 150 characters.'})


def listening():
    def listen(section,q,roman,qr,rows):
        page={'A':2,'B':3,'C':4}[section]
        question=re.sub(r'^\([ivx]+\)\s*','',col('aural',page,qr)).strip()
        c=add('L'+section,q,question,rows,'japanese-6-2' if section=='C' else 'japanese-6-0',[page],[page],roman,reading=[page])
        c['sourceMaterial']['_component']='aural'
        c['stem']=col('aural',page,range(1,7 if section=='A' else 6 if section=='B' else 5))
        if section=='A':c['stem']+='\n'+col('aural',page,[{1:7,2:17,3:26,4:35}[q]])
        if section=='B':c['stem']+='\n'+col('aural',page,[{1:6,2:27,3:42}[q]])
        if section=='C':c['stem']+='\n'+col('aural',page,{1:[5],2:[25,26],3:[33]}[q])
        return c
    for q,roman,qr,sr in [(1,'i',range(8,14),4),(1,'ii',[14,15],5),(2,'i',range(18,24),7),(2,'ii',[24],8),(3,'i',range(27,33),10),(3,'ii',[33],11),(4,'i',range(36,42),13),(4,'ii',[42,43],14)]:
        listen('A',q,roman,qr,[point(s(2,sr,1),3)])
    for roman,qr,sr in [('i',[7,9,10,11,12],3),('ii',[13,*range(15,21)],4),('iii',range(22,27),5)]:
        answer=s(3,sr,0 if sr==5 else 1)
        if sr==5:answer=answer.removeprefix('(iii)').strip()
        listen('B',1,roman,qr,[point(answer,3)])
    listen('B',2,'i',[28,29],[point(s(3,7,1),3)])
    c=listen('B',2,'ii',range(31,37),[point(s(3,8,1),3,contextNote=col('aural',3,[31])),point(s(3,9),3,contextNote=col('aural',3,[36]))])
    group_rows(c,[('donut',col('aural',3,[31]),0,1),('drink',col('aural',3,[36]),1,2)])
    listen('B',2,'iii',range(38,42),[point(s(3,10,1),3)])
    listen('B',3,'i',[43],[anyn([v.strip() for v in s(3,12,1).split('/')],1,3)])
    listen('B',3,'ii',[45],[point(s(3,13,1),3)])
    for roman,qr,sr in [('i',range(7,14),3),('ii',range(14,20),4),('iii',range(20,25),5)]:listen('C',1,roman,qr,[point(s(4,sr,1),3)])
    listen('C',2,'i',[27,28],[anyn([v.strip() for v in s(4,7,1).split('/')],1,4)])
    number=s(4,8,1).removeprefix('(a)').strip()
    halves=[v.strip() for v in number.split('(2 marks)') if v.strip()]
    assert halves==['2 (4) 44','-17(0)1']
    c=listen('C',2,'ii',[30,31],[point(v.lstrip('-'),2,contextNote='One complete number block earns 2. Parenthesised 4 and 0 are already given; no per-digit partial allocation is printed.') for v in halves])
    c['questionFigureKey']=crop('ja-2011-ol-lc-2-ii',4,[.065,.615,.97,.715],c['questionText'],'aural')
    for roman,qr,sr in [('i',range(34,40),10),('ii',range(40,45),11)]:listen('C',3,roman,qr,[point(s(4,sr,1),4)])
    labels=[cell('aural',5,r) for r in range(14,37,2)]
    groups=[{'id':f'item-{i+1}','label':label,'rows':[{'id':'answer','text':s(5,i+2,1),'marks':3}]} for i,label in enumerate(labels)]
    paper_selector={'document':'aural','page':5,'row':32,'group':None,'text':cell('aural',5,32)}
    negative_selector={'document':'scheme','page':5,'row':11,'group':0,'text':cell('scheme',5,11,0)}
    false_selector={'document':'scheme','page':5,'row':11,'group':1,'text':cell('scheme',5,11,1)}
    higher_review=json.loads((Path(__file__).parent/'reviews/japanese-2011-hl.json').read_text())
    higher_selector=next(v for v in higher_review['selectors'] if v['document']=='scheme' and v.get('page')==6 and v.get('row')==12 and v.get('group')==0)
    recording=next(v for v in json.loads((ROOT/'data/japaneseAudio.json').read_text()) if v['year']==2011)
    CORRECTIONS.append({'cardId':'ja-2011-ol-ld','groupId':'item-10','resolvedAnswer':'True',
        'paperSelector':paper_selector,'schemeSelectors':[negative_selector,false_selector],
        'corroboratingReview':'scripts/markbank/authoring/reviews/japanese-2011-hl.json','corroboratingCardId':'ja-2011-hl-ld-2-ii',
        'corroboratingSource':{'path':'examiner-reports/japanese/schemes/2011-hl.pdf','sha256':'b074b5846c2f41ce7a4476795922fd4570334c44536924c8484a4aed02238f81','selector':higher_selector},
        'audio':{'paperFileids':recording['paperFileids'],'canonicalUrl':recording['source']['canonicalUrl'],'secFileid':recording['source']['secFileid'],'sha256':recording['verification']['sha256']}})
    groups[9]['rows'][0]['text']='True'
    guide=cell('scheme',5,1)+' — The paper prints 12 statements and does not say choose eight. Keep every statement; the scheme caps credit at 8 correct responses. Source discrepancy in item(x): paper “'+paper_selector['text']+'”; Ordinary scheme “'+negative_selector['text']+'” → '+false_selector['text']+'. The resolved answer True for the positive paper statement is explicitly corroborated by the same-year Higher scheme, physical page 6, Kenichi’s reasons for liking his job: “'+higher_selector['text']+'”. Both levels use the same verified official recording LC058ZLP017EV.mp3. This is a cross-source editorial correction, not direct audio listening verification or a generic reversal of False.'
    c=add('LD',None,col('aural',5,[5])+'\n'+'\n'.join(labels),[],'japanese-6-0',[5],[5],total=24,reading=[5],rubric={'system':'language-points','count':8,'taskRequirements':[col('aural',5,[5])],'groups':groups,'markingGuideNote':guide},
        figure=crop('ja-2011-ol-ld',5,[.055,.025,.97,.78],col('aural',5,[5]),'aural'))
    c['stem']=col('aural',5,range(1,5));c['sourceMaterial']['_component']='aural'


def build():
    reading_q1();reading_q2();reading_q3();writing();listening()
    census=json.loads((Path(__file__).parent/'reviews/japanese-2011-ol-census.json').read_text())
    expected={'ja-2011-ol-'+'-'.join(str(v).lower() for v in task['key'] if v is not None):task for task in census['tasks']}
    assert set(expected)=={c['id'] for c in CARDS}
    for c in CARDS:
        t=expected[c['id']]
        assert c['questionText'].strip()
        assert c['totalMarks']==t['marks'],(c['id'],c['totalMarks'],t['marks'])
        assert c['sourceEvidence']['paperPages']==t['paperPages']
        assert c['sourceEvidence']['schemePages']==t['schemePages']
        assert not any(ord(ch)<32 and ch not in '\n\r\t' or ch=='\ufffd' for ch in json.dumps(c,ensure_ascii=False))
    assert len(CARDS)==49 and sum(c['totalMarks'] for c in CARDS)==300
    assert sum('answerLanguageRule' in c for c in CARDS)==23
    assert not any(c['id'] in ORIGINAL_IDS for c in CARDS)
    return {'subjectId':'japanese','sitting':'2011-ol','reviewedAt':'2026-11-12','sources':[{'document':name,'path':str(path.relative_to(ROOT)),'sha256':HASHES[name],'pagesReviewed':list(range(1,len(DOCS[name])+1))} for name,path in PATHS.items()],
        'cards':CARDS,'selectors':EVIDENCE,'status':'source-reviewed-browser-qa-pending','choiceAnalysis':census['choiceBoundaries'],'consolidations':[],'sourceAnswerBindings':BINDINGS,'sourceCorrections':CORRECTIONS}

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--write',action='store_true');args=parser.parse_args()
    result=build()
    (ROOT/'tmp/japanese-review/2011-ol-source-draft.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    plan=ROOT/'tmp/japanese-review/2011-ol-crop-plan.json';plan.write_text(json.dumps(FIGURES,ensure_ascii=False,indent=2)+'\n')
    if args.write:
        assert all(v['md5'] for v in FIGURES.values()),'Render each planned crop before publication'
        text='# Original PDF text and furigana folded at its printed character\n'
        for i,page in enumerate(DOCS['scheme']):text+=f'\n## Physical page {i+1}\n\n'+page.get_text()+'\n### Printed rows\n\n'+'\n'.join(' '.join(g[2] for g in row) for row in page_rows(page))+'\n'
        PATHS['scheme'].with_suffix('.md').write_text(text.rstrip()+'\n')
        (ROOT/'scripts/markbank/authoring/reviews/japanese-2011-ol.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
        manifest=ROOT/'components/MarkBank/figures-japanese.json';previous=json.loads(manifest.read_text());previous.update(FIGURES);manifest.write_text(json.dumps(previous,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'cards':len(CARDS),'marks':sum(c['totalMarks'] for c in CARDS),'figures':len(FIGURES)},indent=2))
