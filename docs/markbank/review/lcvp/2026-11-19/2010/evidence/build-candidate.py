#!/usr/bin/env python3
"""Review-only 2010 candidate with both disputed split alternatives preserved."""
from pathlib import Path
from datetime import datetime, timezone
from copy import deepcopy
import hashlib
import json
import re
import sys
import fitz

HERE = Path(__file__).resolve().parent
LANE = Path('/Users/alexlinehan/Documents/Nextstepuni-LCVP-Release-20261119')
sys.path.insert(0, str(LANE / 'scripts/markbank/authoring'))
from lcvp_review_2026 import tidy, point, criterion
from lcvp_review_2018 import models, before_rate, choice_row
from lcvp_review_2017 import header_body, component_rows
from lcvp_identity import concept_id

data = json.loads((HERE / 'source-parts.json').read_text())
records = {r['ref']: r for r in data['records']}
manifest = json.loads((HERE.parent / '2026-11-19-lcvp-2010-independent/source-manifest.json').read_text())
for source in manifest['sources']:
    assert hashlib.sha256(Path(source['path']).read_bytes()).hexdigest() == source['sha256']
listing = manifest['archiveListing']
assert hashlib.sha256(Path(listing['path']).read_bytes()).hexdigest() == listing['sha256']
assert "value='LC462CLP031EV.mov'" in Path(listing['path']).read_text()
paper = fitz.open(next(s['path'] for s in manifest['sources'] if s['kind'] == 'paper'))
NOTICE = 'The scheme prints no answer for this part.'
rows, pools = {}, {}
split_proof, alternative_groups = [], {}


def body(ref):
    raw = records[ref]['sourceSchemeBlock']
    return header_body(raw)[1] if ref.startswith('A') or (ref.startswith('C') and ref.count('(') == 1) else raw


def label(ref):
    return records[ref]['sourceSchemePrompt']


def guidance(ref, extra=''):
    return extra + ' Complete printed support notes and allocation: ' + tidy(body(ref))


def ordinary(ref, count, per, expected, binary=False, parts=None):
    pool = models(before_rate(body(ref), str(count) + r'\s*@\s*' + str(per) + 'm'), expected)
    pools[ref] = pool
    if per == 1 or binary:
        rows[ref] = [choice_row('responses', label(ref), pool, count, per, guidance(ref))]
    else:
        rows[ref] = component_rows(label(ref), pool, [parts or [1] * per] * count, guidance(ref))


def complete(ref, count, steps, extra=''):
    rows[ref] = [criterion('responses', label(ref), count, steps, guidance(ref, extra))]


def missing(ref, count, steps, extra=''):
    rows[ref] = [criterion('unprinted-answer', NOTICE, count, steps, guidance(ref, extra))]


def notice(scope):
    return dict(id='unprinted-answer', kind='criterion', verbatim=NOTICE, marks=0, unprinted=True,
                contextNote=scope + ' Keep all printed material and directions. This notice adds no marks.')


complete('A1', 2, [0, 1])
a2 = ['Finance,', 'Staffing,', 'Marketing,', 'Negotiating.']
assert all(v in body('A2') for v in a2)
rows['A2'] = [choice_row('skills', label('A2'), a2, 2, 1, guidance('A2'))]
ordinary('A3', 2, 1, 2)
ordinary('A4', 2, 2, 2, binary=True)
ordinary('A5', 2, 2, 6)
ordinary('A6', 4, 1, 6)
ordinary('A7', 3, 2, 4)
pools['A8'] = models(body('A8').split('Two statements', 1)[0], 2)
rows['A8'] = component_rows(label('A8'), pools['A8'], [[2, 2], [2]],
    guidance('A8', 'Two distinct statements. The scheme gives one statement four marks (2+2), and the other two or zero. It does not assign a particular printed statement to the higher award.'))
b1names = ['Social', 'Sport', 'commercial', 'educational organisations']
assert all(v in body('B1(i)') for v in b1names)
rows['B1(i)'] = [choice_row('stakeholders', label('B1(i)'), b1names, 3, 1, guidance('B1(i)'))]
complete('B1(ii)', 3, [0, 1], 'One reason for each same stakeholder chosen in part(i). No repetition of reasons; any valid reason acceptable. All four complete stakeholder reason pools remain below.')
ordinary('B2(i)', 2, 3, 2, parts=[2, 1])
ordinary('B2(ii)', 3, 2, 5)
complete('B3(i)', 4, [0, 1], 'Temporary grouping; explicit description and advantages awards split below. All three original method pools and every advantage are retained.')
complete('B3(ii)', 1, [0, 2], 'One relevant trend, two or zero marks. Any category can be selected; keep the full original population table before reveal.')
pools['B3(iii)'] = models(before_rate(body('B3(iii)'), r'2\s*@\s*3m'), 8)
rows['B3(iii)'] = component_rows(label('B3(iii)'), pools['B3(iii)'], [[1, 1, 1]] * 2,
    guidance('B3(iii)', 'Two projects, with three one-mark criteria for each same project. No repetition of points.'))
for row in rows['B3(iii)']:
    for part, text in zip(row['parts'], ['statement of the project', 'how they met the challenge', 'retain what’s good about the area']):
        assert text in body('B3(iii)')
        part['verbatim'] = text
rows['B3(iii)'].append(notice('The scheme names eight possible projects but supplies no model explanation of how a chosen project meets a challenge or retains what is good about the area.'))
missing('C1(a)', 1, [0, 2], 'The scheme gives two marks for the name of the product/service; no model product or service is printed.')
rows['C1(b)'] = [criterion(name.lower(), name, 2, [0, 1], guidance('C1(b)', 'Two points under this heading. No repetition of points/examples.'))
                 for name in ['Strengths', 'Weaknesses', 'Opportunities', 'Threats']]
complete('C1(c)', 3, [0, 1, 2], 'Three relevant characteristics, each with two one-mark components. All five printed named examples are retained; no explanation is invented.')
rows['C1(c)'].append(notice('The missing content is the explanations requested for the characteristics; the five named characteristics remain in the printed guidance.'))
ordinary('C1(d)', 3, 3, 6, parts=[1, 2])
complete('C2(a)', 4, [0, 1], 'Temporary grouping; explicit activity and role awards split below.')
ordinary('C2(b)', 3, 2, 8)
ordinary('C2(c)', 3, 2, 7, binary=True)
ordinary('C2(d)', 3, 3, 7)
rows['C2(d)'].append(notice('The missing content is the developed descriptions beyond the brief method names in options2,3,7 and the evaluation questions in options5,6. Keep those exact printed names and questions, plus both fuller options1 and4.'))
complete('C3(a)', 3, [0, 2], 'Three fixed underlined terms, not a choose-three pool. One two-or-zero award for each definition. Split decision remains unresolved.')
for part, term in zip(rows['C3(a)'][0]['parts'], ['CV', 'Referees', 'Equal opportunities employer']):
    part['verbatim'] = term
pools['C3(b)'] = models(body('C3(b)').split('3 points', 1)[0], 4)
rows['C3(b)'] = component_rows(label('C3(b)'), pools['C3(b)'], [[2], [2], [1]],
    guidance('C3(b)', 'Three distinct points: two receive two or zero marks and one receives one mark. Do not assign particular printed points to the higher awards.'))
ordinary('C3(c)', 4, 2, 6)
pools['C3(d)'] = models(before_rate(body('C3(d)'), r'2\s*@\s*2m'), 9)
rows['C3(d)'] = component_rows(label('C3(d)'), pools['C3(d)'], [[1, 1], [1, 1], [1], [1]],
    guidance('C3(d)', 'Four distinct pieces of information: two receive two one-mark components each, and two receive one mark each. Preserve all nine alternatives.'))
complete('C4(a)', 5, [0, 1], 'Temporary grouping; explicit activity-name and success awards split below.')
ordinary('C4(b)', 3, 2, 8)
ordinary('C4(c)', 3, 2, 4)
complete('C4(d)(i)', 2, [0, 1], 'One definition with two one-mark components; retain the complete printed model.')
ordinary('C4(d)(ii)', 3, 2, 5)
agenda = models(before_rate(body('C5(a)'), r'5\s*@\s*1m'), 8)
rows['C5(a)'] = [point('officers', agenda[0], 1, guidance('C5(a)', 'This is a compulsory point.')),
                 point('permission', agenda[4], 1, 'This is a compulsory point.'),
                 choice_row('other-agenda-items', 'AGENDA', [v for i, v in enumerate(agenda) if i not in [0, 4]], 3, 1,
                            'Three other distinct agenda points, one mark each; five total including the two compulsory points. No marks for an unprinted heading or layout requirement.')]
ordinary('C5(b)', 3, 2, 6)
pools['C5(c)'] = models(before_rate(body('C5(c)'), r'1\s*@\s*3m'), 4)
rows['C5(c)'] = component_rows(label('C5(c)'), pools['C5(c)'], [[2, 1], [2]],
    guidance('C5(c)', 'Two distinct responses: one receives three marks (2+1), the other two or zero. Do not fix a particular printed model to the higher award.'))
ordinary('C5(d)', 3, 3, 4)
ordinary('C6(a)', 2, 2, 9)
ordinary('C6(b)', 2, 3, 6, parts=[1, 2])
for row in rows['C6(b)']:
    row['contextNote'] += ' The source prints (1 + 2), then Explanation and example, without assigning either word to a particular number. Preserve the numeric components without reversing or semantically labelling them.'
rows['C6(b)'].append(notice('The scheme requires Explanation and example. In particular, option5 Take steps to avoid bullying supplies no example. The notice covers that missing example and does not replace any of the six printed options or assign the1+2 components to particular words.'))
complete('C6(c)', 7, [0, 1], 'Temporary grouping; explicit planning and evaluation awards split below.')
ordinary('C6(d)', 4, 2, 6)
assert set(rows) == set(records)


def source(pages, kind='source-question', title='Original question'):
    return dict(kind=kind, label='OFFICIAL SOURCE', title=title, pages=pages,
                attribution='SEC LCVP Link Modules 2010 Common Level — © State Examinations Commission.',
                presentationNote='Read the complete original source and question in context.')


native = paper[7].get_text(sort=False)
case = native[native.index('KILLMALOE COMMUNITY DEVELOPMENT'):]
prose, tail = case.split('Table showing the Population of Killmaloe between the years 1999 and 2009', 1)
table, conclusion = tail.split('Communities, like Killmaloe,', 1)
table_text = tidy(table)
headers = ['0 – 14 yrs', '15 – 24 yrs', '25 – 44 yrs', '45 – 64 yrs', '65+ yrs', 'Total']
assert table_text.startswith('Age Groups ' + ' '.join(headers))
first = re.search(r'1999\s+((?:\d+\s+){6})2009', table_text)
second = re.search(r'2009\s+((?:\d+\s*){6})$', table_text)
assert first and second
old, new = [int(x) for x in first[1].split()], [int(x) for x in second[1].split()]
assert old == [673, 469, 667, 554, 412, 2775] and new == [528, 348, 580, 670, 458, 2584]
table_title = 'Table showing the Population of Killmaloe between the years 1999 and 2009'
readable = table_title + '\n' + '\n'.join(f'{name} — 1999: {a}; 2009: {b}' for name, a, b in zip(headers, old, new))
case_text = tidy(prose) + '\n\n' + readable + '\n\n' + tidy('Communities, like Killmaloe,' + conclusion)
(HERE / 'case-table-transcription-proof.json').write_text(json.dumps(dict(sourcePaperSha256=data['sourceSha256']['paper'],
    physicalPage=8, originalTable=table, headers=headers, values={'1999': old, '2009': new}, transcription=readable,
    sourceImage='2010-independent/original-pages/paper-08.png',
    scope='Every original column and all12 values, full five preceding paragraphs and final paragraph retained. Original layout remains available before reveal.'), ensure_ascii=False, indent=2) + '\n')
stems = {int(k): v for k, v in data['sectionCStems'].items()}
heading_topics = {'1-career-investigation': '0-2', '1-job-seeking-skills': '0-1', '1-introduction-to-working-life': '0-0',
                  '1-work-placement': '0-3', '2-enterprise-skills': '1-0', '2-local-voluntarycommunity-enterprises': '1-2',
                  '2-an-enterprise-activity': '1-3', '2-local-business-enterprises': '1-1'}


def set_topics(card, headings):
    topics = ['lcvp-link-modules-' + heading_topics[h.removeprefix('link-modules-common-')] for h in headings]
    card['topicId'] = topics[0]
    card.pop('additionalTopicIds', None)
    if len(topics) > 1:
        card['additionalTopicIds'] = topics[1:]


cards = []
for ref, record in records.items():
    section, number = ref[0], int(ref[1])
    card = dict(id=record['id'], subjectId='lcvp', conceptId=concept_id(record['id'], record['id'].removeprefix('lcvp-2010-cl-') + '-2010-source'),
                level='common', year=2010, section=section, questionRef='2010 CL Section ' + section + ' Q' + ref[1:],
                questionText=record['questionText'], stem=case_text if section == 'B' else stems[number] if section == 'C' else '',
                figureKey='', labelKey=[], totalMarks=sum(record['proposedCardMarks']), rows=rows[ref],
                tariffModel=dict(kind='fixed', notation='Original 2010 marking scheme allocation.'),
                sourceMaterial=source(record['paperPages']))
    set_topics(card, record['proposedHeadingIds'])
    if section == 'A':
        url = 'https://www.examinations.ie/archive/exampapers/2010/LC462CLP031EV.mov'
        card['videoMaterial'] = dict(kind='source-video', label='OFFICIAL VIDEO', title='2010 LCVP audiovisual examination',
                                    playbackUrl=url, canonicalUrl=url, secFileid='LC462CLP031EV.mov',
                                    attribution='State Examinations Commission — original 2010 Common Level English audiovisual recording.',
                                    presentationNote='Watch the original sequence with sound before answering. Follow the printed viewing instructions.')
        card['additionalSourceMaterials'] = [source([2], title='Original audiovisual instructions')]
    elif section == 'B':
        card['sourceMaterial'] = source([8], 'source-text', 'Killmaloe Community Development — complete case and table')
        card['additionalSourceMaterials'] = [source(record['paperPages'])]
        if ref == 'B1(ii)':
            card['stem'] += ' ' + records['B1(i)']['questionText']
    else:
        if number in [1, 2, 4] and ref != f'C{number}(a)':
            card['stem'] += ' ' + records[f'C{number}(a)']['questionText']
        if number == 3 and record['paperPages'] != [20]:
            card['additionalSourceMaterials'] = [source([20], 'source-text', 'Complete Gourmet Café advertisement')]
    cards.append(card)


def split(ref, texts, marks, new_rows, scopes, provisional=False):
    index = next(i for i, c in enumerate(cards) if c['id'] == records[ref]['id'])
    original = deepcopy(cards[index])
    parts = []
    for n in range(len(marks)):
        card = deepcopy(original)
        card.update(questionText=texts[n], totalMarks=marks[n], rows=new_rows[n])
        card['questionRef'] += ' — ' + scopes[n]
        card['stem'] += ' ' + original['questionText']
        if n:
            card['id'] += '-' + str(n + 1)
            card['conceptId'] += '-ask-' + str(n + 1)
        if records[ref]['perAskHeadingIds']:
            set_topics(card, records[ref]['perAskHeadingIds'][n])
        parts.append(card)
    cards[index:index + 1] = parts
    split_proof.append(dict(ref=ref, originalPrompt=original['questionText'], selectedPrompts=texts, marks=marks,
                            scopes=scopes, fullOriginalRetainedBeforeReveal=True, provisional=provisional))
    if ref in ['B2(i)', 'C3(a)']:
        alternative_groups[ref] = dict(status='Unresolved alternatives; neither is approved or applied.', combined=[original], split=deepcopy(parts))


def sentences(ref, boundary):
    value = records[ref]['questionText']; pos = value.index(boundary)
    return [value[:pos].strip(), value[pos:].strip()]


# A fixed entity/term from the original question is selected without inventing
# a singular rewording. The complete joint prompt is retained in shared context.
b2texts = ['County Enterprise Board', 'County Council']
assert all(text in records['B2(i)']['questionText'] for text in b2texts)
split('B2(i)', b2texts, [3, 3],
      [component_rows(label('B2(i)'), [pool], [[2, 1]], guidance('B2(i)', 'Answer only for this named organisation. The source gives one of the two three-mark awards to each printed model; split form remains provisional.'))
       for pool in pools['B2(i)']], b2texts, True)
split('B2(ii)', sentences('B2(ii)', 'Explain each'), [3, 3],
      [[choice_row('ways', label('B2(ii)'), pools['B2(ii)'], 3, 1, guidance('B2(ii)', 'Provisional split of the three printed1+1 allocations; generic-component consistency decision remains pending.'))],
       [criterion('explanations', label('B2(ii)'), 3, [0, 1], guidance('B2(ii)', 'Explain each same chosen way. Keep all five printed option lines; do not invent explanations. The proposed naming/explanation split remains provisional.')),
        notice('The notice covers explanations not supplied beyond the printed option fragments, particularly Grants and Serviced facilities/enterprise units/infrastructure.')]],
      ['ways', 'explanations'], True)
split('B3(i)', sentences('B3(i)', 'Give two advantages'), [2, 2],
      [[criterion('description', 'Description', 2, [0, 1], guidance('B3(i)', 'Describe one chosen method.'))],
       [criterion('advantages', 'Advantages', 2, [0, 1], guidance('B3(i)', 'Give two advantages of the same chosen method.'))]], ['description', 'advantages'])
split('C2(a)', sentences('C2(a)', 'Indicate clearly'), [1, 3],
      [[criterion('unprinted-answer', NOTICE, 1, [0, 1], guidance('C2(a)', 'One mark for the name of the activity.'))],
       [criterion('unprinted-answer', NOTICE, 1, [0, 1, 2, 3], guidance('C2(a)', 'State role + explain, using the printed1+2 components and the same chosen activity.'))]], ['activity', 'role'])
cards[next(i for i,c in enumerate(cards) if c['id'] == 'lcvp-2010-cl-c2a-2')]['rows'][0]['parts'] = [
    dict(id='state-role', verbatim='State role', marks=1, permittedMarks=[0,1]),
    dict(id='explain', verbatim='explain', marks=2, permittedMarks=[0,2])]
c3body = body('C3(a)')
terms = ['CV', 'Referees', 'Equal opportunities employer']
selected = [tidy(v) for v in re.split(r'CV:|Referees:|Equal opportunities employer:', before_rate(c3body, r'3\s*@\s*2m'))[1:]]
assert len(selected) == 3
split('C3(a)', ['CV', 'referees', 'equal opportunities employer'], [2, 2, 2],
      [[criterion('definition', term + ': ' + model, 1, [0,2], guidance('C3(a)', 'Define only this fixed underlined term. Split form remains provisional.'))]
       for term, model in zip(terms, selected)], terms, True)
split('C4(a)', sentences('C4(a)', 'Was the activity'), [1, 4],
      [[criterion('unprinted-answer', NOTICE, 1, [0, 1], guidance('C4(a)', 'Name the same LCVP activity where you had a leadership role.'))],
       [criterion('unprinted-answer', NOTICE, 2, [0, 2], guidance('C4(a)', 'The scheme prints Successful? Yes or No and two awards of two or zero, but no model. Do not assign one award to yes/no and the other to an explanation without source support.'))]], ['activity', 'success'])
c6plan = models(before_rate(body('C6(c)').split('Planned for and organised', 1)[1], r'3\s*@\s*1m'), 7)
split('C6(c)', sentences('C6(c)', 'Write a brief evaluation'), [3, 4],
      [[choice_row('planning', 'Planned for and organised', c6plan, 3, 1, guidance('C6(c)'))],
       [criterion('unprinted-answer', NOTICE, 4, [0, 1], guidance('C6(c)', 'Evaluate the same placement. Four printed one-mark criteria: career choice/future studies, Home, School, Community. No model evaluation is printed.'))]], ['planning', 'evaluation'])

evaluation = next(c for c in cards if c['id'] == 'lcvp-2010-cl-c6c-2')['rows'][0]
for part, text in zip(evaluation['parts'], ['Comment on career choice/future studies and this type of job.', 'Home', 'School', 'Community']):
    assert text in body('C6(c)')
    part['verbatim'] = text

for card in cards:
    for row in card['rows']:
        if row['verbatim'] == NOTICE:
            row['unprinted'] = True
assert len(cards) == len({c['id'] for c in cards}) == 48
assert sum(c['totalMarks'] for c in cards) == 210
assert all(sum(row['marks'] for row in c['rows']) == c['totalMarks'] for c in cards)
assert all(not re.search(r'Office Use|Page \d+ of|^\.', c['stem']) for c in cards)
alternative = deepcopy(cards)
for ref, group in alternative_groups.items():
    ids = {c['id'] for c in group['split']}
    index = next(i for i,c in enumerate(alternative) if c['id'] in ids)
    alternative = [c for c in alternative if c['id'] not in ids]
    alternative[index:index] = deepcopy(group['combined'])
assert len(alternative) == 45 and sum(c['totalMarks'] for c in alternative) == 210
output = HERE / 'proposed-48-authored-cards.json'
output.write_text(json.dumps(cards, ensure_ascii=False, indent=2) + '\n')
(HERE / 'alternative-45-authored-cards.json').write_text(json.dumps(alternative, ensure_ascii=False, indent=2) + '\n')
(HERE / 'unresolved-split-alternatives.json').write_text(json.dumps(alternative_groups, ensure_ascii=False, indent=2) + '\n')
(HERE / 'split-source-selections.json').write_text(json.dumps(split_proof, ensure_ascii=False, indent=2) + '\n')
proof = dict(recordedAt=datetime.now(timezone.utc).isoformat(), status='Review-only provisional shape; no production writes or adjudication.',
             cards=48, alternativeCards=45, offeredMarks=210, sourceParts=40, candidateMaximum=160,
             payloadSha256=hashlib.sha256(output.read_bytes()).hexdigest(),
             wholeNotices=[c['id'] for c in cards if all(r.get('unprinted') for r in c['rows'])],
             partialNotices=[c['id'] for c in cards if any(r.get('unprinted') for r in c['rows']) and not all(r.get('unprinted') for r in c['rows'])],
             outstanding=['B2(i) and C3(a) split adjudication; B2(ii) generic-component consistency', 'Five display-heading differences and final filing',
                          'Independent candidate review and source-provenance checks', 'Source/Atlas bindings, application and browser checks',
                          'Fresh archive recheck and original video hosting/playback'])
(HERE / 'candidate-proof.json').write_text(json.dumps(proof, indent=2) + '\n')
print(json.dumps(proof, indent=2))
