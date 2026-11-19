#!/usr/bin/env python3
"""Review-only 2011 candidate; all source/lane release checks remain separate."""
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
manifest = json.loads((HERE.parent / '2026-11-19-lcvp-2011-independent/source-manifest.json').read_text())
for source in manifest['sources']:
    assert hashlib.sha256(Path(source['path']).read_bytes()).hexdigest() == source['sha256']
paper = fitz.open(next(s['path'] for s in manifest['sources'] if s['kind'] == 'paper'))
NOTICE = 'The scheme prints no answer for this part.'
rows = {}
split_proof = []


def body(ref):
    raw = records[ref]['sourceSchemeBlock']
    if ref.startswith('A') or ref == 'B1' or (ref.startswith('C') and ref.count('(') == 1):
        return header_body(raw)[1]
    return raw


def label(ref):
    return records[ref]['sourceSchemePrompt']


def guidance(ref, extra=''):
    return extra + ' Complete printed support notes and allocation: ' + tidy(body(ref))


def ordinary(ref, count, per, expected, binary=False, components=None):
    pool = models(before_rate(body(ref), str(count) + r'\s*@\s*' + str(per) + 'm'), expected)
    if per == 1 or binary:
        rows[ref] = [choice_row('responses', label(ref), pool, count, per, guidance(ref))]
    elif components:
        assert sum(components) == per
        rows[ref] = component_rows(label(ref), pool, [components] * count, guidance(ref))
    else:
        rows[ref] = [criterion('responses', label(ref), count, list(range(per + 1)), guidance(ref))]


def complete(ref, count, steps, extra=''):
    rows[ref] = [criterion('responses', label(ref), count, steps, guidance(ref, extra))]


def missing(ref, count, steps, extra=''):
    rows[ref] = [criterion('unprinted-answer', NOTICE, count, steps, guidance(ref, extra))]


def ordered(ref, awards, extra=''):
    rows[ref] = [criterion(f'response-{i}', label(ref), 1, list(range(mark + 1)),
                          guidance(ref, extra + f' Response {i} of {len(awards)} receives up to {mark} marks.'))
                 for i, mark in enumerate(awards, 1)]


rows['A1'] = [point('definition', tidy(before_rate(body('A1'), r'1\s+mark')), 1)]
complete('A2', 2, [0, 1])
ordinary('A3', 3, 1, 3)
ordinary('A4', 2, 2, 2, binary=True)
ordinary('A5', 4, 1, 7)
ordinary('A6', 2, 2, 2)
complete('A7', 6, [0, 1], 'Temporary source grouping; explicit one-mark decision and five-mark learning split below.')
ordered('A8', [2, 2, 1, 1], 'Use four distinct responses: the scheme gives two developed responses two marks each and the other two one mark each. Preserve all four complete printed examples.')
complete('B1', 6, [0, 1], 'Temporary source grouping; explicit stating and description awards split below. No repetition.')
ordinary('B2(i)', 4, 1, 4)
complete('B2(ii)', 4, [0, 1, 2], 'No marks for headings. No repetition of points. Preserve all six full ICT pools and their examples.')
ordinary('B3(i)', 4, 1, 5)
complete('B3(ii)', 3, [0, 1, 2], 'No marks for headings. Preserve all seven full start-up issue pools, including each question and example.')
missing('B3(iii)', 1, [0, 2], 'Any relevant comment to the case study: two marks. No model answer or intermediate mark is printed.')
missing('C1(a)', 1, [0, 1])
complete('C1(b)', 6, [0, 1], 'Temporary source grouping; explicitly labelled state and explain awards split below.')
ordinary('C1(c)', 3, 3, 6, components=[1, 2])
ordinary('C1(d)', 3, 3, 8, components=[1, 2])
missing('C2(a)', 1, [0, 2])
ordinary('C2(b)', 2, 2, 5, binary=True)
ordinary('C2(c)', 3, 3, 6, components=[1, 2])
complete('C2(d)(i)', 2, [0, 2], 'One definition, with the printed two plus two marks. No one-mark steps are printed.')
complete('C2(d)(ii)', 6, [0, 1], 'Temporary source grouping; proposed methods/reasons split below awaits generic-component consistency adjudication.')
c3a = body('C3(a)')
pool = models(c3a.split('Any valid reason', 1)[0], 4)
rows['C3(a)'] = [choice_row('reason', label('C3(a)'), pool, 1, 1, guidance('C3(a)'))]
complete('C3(b)', 6, [0, 1], 'Temporary source grouping; explicit types and advantages awards split below.')
complete('C3(c)', 8, [0, 1], 'Temporary source grouping; explicit challenge and remedy awards split below.')
ordered('C3(d)', [3, 3, 2, 2], 'Four distinct points. The scheme gives two responses three marks (1+2) and two responses two marks (1+1). Preserve all nine printed alternatives; do not fix particular alternatives to the higher award.')
ordinary('C4(a)', 2, 1, 5)
ordinary('C4(b)', 3, 2, 6, binary=True)
c4b_options = models(before_rate(body('C4(b)'), r'3\s*@\s*2m').split('Explanation is needed', 1)[0], 6)
rows['C4(b)'] = [choice_row('responses', label('C4(b)'), c4b_options, 3, 2,
                            guidance('C4(b)', 'Explanation is needed applies to every response; it is not part of option6.')),
                 dict(id='unprinted-answer', kind='criterion', verbatim=NOTICE, marks=0, unprinted=True,
                      contextNote='The notice applies to the unprinted explanations required beyond the brief statements in options1–4. Keep the complete printed wording of all six options, including the explanatory clauses in options5 and6. Each complete response receives two or zero marks; this notice adds no marks.')]
complete('C4(c)', 8, [0, 1], 'Temporary source grouping; definition and reasons split below.')
ordinary('C4(d)', 3, 3, 6, components=[1, 2])
ordinary('C5(a)', 2, 2, 6, binary=True)
ordinary('C5(b)', 2, 2, 5, binary=True)
# One questionnaire, retaining all six example questions. Its repeated Q1–Q6
# labels are printed model content, never extra asks in the paper census.
questionnaire = body('C5(c)')
presentation = ['Layout', 'Heading', 'Neatness', 'Instructions', 'Variety of question styles']
assert all(word in questionnaire for word in presentation)
rows['C5(c)'] = [point(f'presentation-{i}', word, 1, guidance('C5(c)') if i == 1 else '')
                 for i, word in enumerate(presentation, 1)]
rows['C5(c)'] += [criterion('compulsory-question', 'How much would you be willing to pay for 1 bracelet?', 1, [0, 1],
                           'The source marks this question with an asterisk and says Compulsory Question.'),
                  criterion('other-questions', '5 Questions', 4, [0, 1],
                            'Four other distinct questions, one mark each. Together with the compulsory willingness-to-pay question these make the five marked questions. Preserve all six example questions and printed answer choices in the full model above.')]
marketing = body('C5(d)')
research = marketing.split('Market Research:', 1)[1].split('1 mark', 1)[0]
rows['C5(d)'] = [point('research', 'Market Research: ' + tidy(research), 1, guidance('C5(d)'))]
rows['C5(d)'] += [criterion(f'mix-{i}', 'Marketing section:', 1, list(range(mark + 1)),
                            f'Use each of the four marketing-mix elements once. The two more developed elements receive two marks each and the other two one each; no particular element is assigned the higher award. Response {i} of four.')
                   for i, mark in enumerate([2, 2, 1, 1], 1)]
missing('C6(a)', 4, [0, 1], 'One email. Choose any four of the eight printed criteria, one mark each. A complete model email is not printed.')
ordinary('C6(b)', 3, 2, 6, binary=True)
ordinary('C6(c)', 3, 2, 5)
complete('C6(d)', 9, [0, 1], 'Temporary source grouping; explicitly labelled naming and explanation awards split below.')
assert set(rows) == set(records)


def source(pages, kind='source-question', title='Original question'):
    return dict(kind=kind, label='OFFICIAL SOURCE', title=title, pages=pages,
                attribution='SEC LCVP Link Modules 2011 Common Level — © State Examinations Commission.',
                presentationNote='Read the complete original source and question in context.')


native = paper[7].get_text(sort=False)
case = native[native.index('SWEET DREAMS BY SARA'):]
prose, table = case.split('\nTable\n', 1) if '\nTable\n' in case else case.split('\nTable \n', 1)
assert 'Source: Fáilte Ireland 2009' in table
headers = ['National Parks', 'Water Sports', 'Houses Castles', 'Hiking Walking', 'Visits to Spas',
           'Gardens', 'Heritage Interpretive Centres', 'Museums Art Galleries', 'Golf']
table_text = tidy(table)
title = 'Activities Engaged in by Domestic Holidaymakers (%)'
assert table_text.startswith(title + ' ' + ' '.join(headers))
first = re.search(r'2008\s+((?:\d+\s+){9})2009', table_text)
second = re.search(r'2009\s+((?:\d+\s+){9})Source:', table_text)
assert first and second
year_2008, year_2009 = [int(x) for x in first[1].split()], [int(x) for x in second[1].split()]
assert year_2008 == [26, 26, 25, 25, 20, 19, 15, 14, 11]
assert year_2009 == [23, 27, 24, 21, 24, 20, 21, 14, 10]
readable_table = title + '\n' + '\n'.join(f'{name} — 2008: {a}; 2009: {b}'
    for name, a, b in zip(headers, year_2008, year_2009)) + '\nSource: Fáilte Ireland 2009'
case_text = tidy(prose) + '\n\n' + readable_table
(HERE / 'case-table-transcription-proof.json').write_text(json.dumps(dict(
    sourcePaperSha256=data['sourceSha256']['paper'], physicalPage=8, originalText=table,
    headers=headers, values={'2008': year_2008, '2009': year_2009}, transcription=readable_table,
    originalImageRead='2011-independent/original-pages/paper-08.png',
    scope='Both original row sequences and every column header preserved. Original table layout remains available before reveal through source page8.'),
    ensure_ascii=False, indent=2) + '\n')
stems = {int(q): text for q, text in data['sectionCStems'].items()}
heading_topics = {'1-career-investigation': '0-2', '1-job-seeking-skills': '0-1',
                  '1-introduction-to-working-life': '0-0', '1-work-placement': '0-3',
                  '2-enterprise-skills': '1-0', '2-local-voluntarycommunity-enterprises': '1-2',
                  '2-an-enterprise-activity': '1-3', '2-local-business-enterprises': '1-1'}
cards = []
for ref, record in records.items():
    section, number = ref[0], int(ref[1])
    topics = ['lcvp-link-modules-' + heading_topics[h.removeprefix('link-modules-common-')]
              for h in record['firstReaderHeadings']]
    card = dict(id=record['id'], subjectId='lcvp', topicId=topics[0],
                conceptId=concept_id(record['id'], record['id'].removeprefix('lcvp-2011-cl-') + '-2011-source'),
                level='common', year=2011, section=section,
                questionRef='2011 CL Section ' + section + ' Q' + ref[1:],
                questionText=record['questionText'], stem=case_text if section == 'B' else stems[number] if section == 'C' else '',
                figureKey='', labelKey=[], totalMarks=sum(record['proposedCardMarks']), rows=rows[ref],
                tariffModel=dict(kind='fixed', notation='Original 2011 marking scheme allocation.'),
                sourceMaterial=source(record['paperPages']))
    if len(topics) == 2:
        card['additionalTopicIds'] = [topics[1]]
    if section == 'A':
        url = 'https://www.examinations.ie/archive/exampapers/2011/LC462CLP031EV.mp4'
        card['videoMaterial'] = dict(kind='source-video', label='OFFICIAL VIDEO', title='2011 LCVP audiovisual examination',
                                    playbackUrl=url, canonicalUrl=url, secFileid='LC462CLP031EV.mp4',
                                    attribution='State Examinations Commission — original 2011 Common Level English audiovisual recording.',
                                    presentationNote='Watch the original sequence with sound before answering. Follow the printed viewing instructions.')
        card['additionalSourceMaterials'] = [source([2], title='Original audiovisual instructions')]
    elif section == 'B':
        card['sourceMaterial'] = source([8], 'source-text', 'Sweet Dreams by Sara — complete case and table')
        card['additionalSourceMaterials'] = [source(record['paperPages'])]
    elif number in [1, 2] and ref not in ['C1(a)', 'C2(a)']:
        card['stem'] += ' ' + records[f'C{number}(a)']['questionText']
    cards.append(card)


def split(ref, texts, marks, new_rows, scopes):
    i = next(i for i, c in enumerate(cards) if c['id'] == records[ref]['id'])
    original = cards[i]
    original_prompt = original['questionText']
    parts = []
    for n in range(2):
        card = deepcopy(original)
        card.update(questionText=texts[n], totalMarks=marks[n], rows=new_rows[n])
        card['questionRef'] += ' — ' + scopes[n]
        card['stem'] += ' ' + original_prompt
        if n:
            card['id'] += '-2'
            card['conceptId'] += '-second-ask'
        parts.append(card)
    cards[i:i + 1] = parts
    split_proof.append({'ref': ref, 'originalPrompt': original_prompt, 'selectedPrompts': texts, 'marks': marks,
                        'fullOriginalRetainedBeforeReveal': True})


def sentences(ref, boundary):
    value = records[ref]['questionText']; pos = value.index(boundary)
    return [value[:pos].strip(), value[pos:].strip()]


a7body = body('A7')
decision = tidy(a7body.split('1m', 1)[0])
learned = models(before_rate(a7body.split('Orla has learned;', 1)[1], r'5\s*@\s*1m'), 5)
split('A7', sentences('A7', 'What has Orla learned'), [1, 5],
      [[point('decision', decision, 1)], [choice_row('learning', 'Orla has learned;', learned, 5, 1)]], ['decision', 'learning'])
for ref, names in [('B1', ['Innovative/Creative', 'Motivated', 'Realistic', 'Risktaker', 'Decisive', 'Flexible', 'Hardworking']),
                   ('C1(b)', ['Teamwork skills', 'Communication skills', 'Confidence'])]:
    original = records[ref]['questionText']
    assert original.startswith('State and explain ')
    # Select the two original verbs with their shared object. No new words;
    # the complete joint paper sentence remains in both cards' shared context.
    selected = ['State ' + original[len('State and explain '):], original[len('State and '):]]
    assert all(n in tidy(body(ref)) for n in names)
    explain = criterion('unprinted-answer' if ref == 'C1(b)' else 'descriptions',
                        NOTICE if ref == 'C1(b)' else label(ref), 3, [0, 1],
                        guidance(ref, 'Explain the same three chosen characteristics. No repetition.'))
    stating = (criterion('characteristics', 'State', 3, [0, 1],
                         guidance(ref, 'Three distinct skills, one mark each. The three printed examples end with Etc.; they are examples rather than three compulsory answers.'))
               if ref == 'C1(b)' else choice_row('characteristics', 'State', names, 3, 1, guidance(ref)))
    split(ref, selected, [3, 3], [[stating], [explain]],
          ['characteristics', 'explanations'])
split('C2(d)(ii)', sentences('C2(d)(ii)', 'Give reasons'), [3, 3],
      [[criterion('methods', label('C2(d)(ii)'), 3, [0, 1], guidance('C2(d)(ii)', 'Three methods; proposed split awaiting consistency adjudication.'))],
       [criterion('reasons', label('C2(d)(ii)'), 3, [0, 1], guidance('C2(d)(ii)', 'One reason for each same method; proposed split awaiting consistency adjudication.'))]], ['methods', 'reasons'])
types = ['Retail', 'Manufacturing', 'Financial', 'Transport', 'Service industry', 'Job creation', 'State run organisations', 'Tourism/Heritage',
         'Community organisation', 'Charitable organisation', 'Sporting organisations']
assert all(t in body('C3(b)') for t in types)
split('C3(b)', sentences('C3(b)', 'Explain one advantage'), [2, 4],
      [[choice_row('types', 'Types of enterprises', types, 2, 1, guidance('C3(b)', 'Keep both original columns: commercial and voluntary organisations. No mandatory mix is printed.'))],
       [criterion('advantages', 'Advantages', 2, [0, 2], guidance('C3(b)', 'One advantage for each same selected type. Two or zero marks each.'))]], ['types', 'advantages'])
split('C3(c)', sentences('C3(c)', 'Explain two ways'), [4, 4],
      [[criterion('challenges', label('C3(c)'), 2, [0, 2], guidance('C3(c)', 'Two challenges, two or zero marks each.'))],
       [criterion('first-remedies', label('C3(c)'), 2, [0, 1], guidance('C3(c)', 'Two one-mark remedies for the first chosen challenge.')),
        criterion('second-remedies', label('C3(c)'), 2, [0, 1], guidance('C3(c)', 'Two one-mark remedies for the second chosen challenge.'))]], ['challenges', 'ways to overcome'])
split('C4(c)', sentences('C4(c)', 'Explain three reasons'), [2, 6],
      [[criterion('definition', 'What is a Trade Union?', 2, [0, 1], guidance('C4(c)'))],
       [criterion('reasons', 'Reasons why workers join unions.', 3, [0, 1, 2], guidance('C4(c)'))]], ['definition', 'reasons'])
split('C6(d)', sentences('C6(d)', 'Explain why'), [3, 6],
      [[criterion('characteristics', 'Naming characteristics:', 3, [0, 1], guidance('C6(d)'))],
       [criterion('explanations', 'explain' + label('C6(d)').split('and explain', 1)[1], 3, [0, 1, 2], guidance('C6(d)', 'Explain why each same characteristic matters to the employer; two one-mark details per characteristic. No repetition.'))]], ['characteristics', 'explanations'])

for card in cards:
    for row in card['rows']:
        if row['verbatim'] == NOTICE:
            row['unprinted'] = True
assert len(cards) == len({c['id'] for c in cards}) == 47
assert sum(c['totalMarks'] for c in cards) == 210
assert all(sum(row['marks'] for row in c['rows']) == c['totalMarks'] for c in cards)
assert all(not re.search(r'\b1 2\b|Office Use', c['stem']) for c in cards)
output = HERE / 'proposed-47-authored-cards.json'
output.write_text(json.dumps(cards, ensure_ascii=False, indent=2) + '\n')
(HERE / 'split-source-selections.json').write_text(json.dumps(split_proof, ensure_ascii=False, indent=2) + '\n')
proof = dict(recordedAt=datetime.now(timezone.utc).isoformat(), status='Review-only; not applied or independently reviewed',
             cards=47, offeredMarks=210, sourceParts=39, payloadSha256=hashlib.sha256(output.read_bytes()).hexdigest(),
             outstanding=['Original-PDF claim trace and layout review', 'Independent candidate review', 'Third-reader headings and generic split consistency',
                          'Full case-table layout, questionnaire checkbox glyphs and ordered-mark controls', 'Fresh R4 archive recheck',
                          'Video hosting, source/Atlas bindings and application verification'])
(HERE / 'candidate-proof.json').write_text(json.dumps(proof, indent=2) + '\n')
print(json.dumps(proof, indent=2))
