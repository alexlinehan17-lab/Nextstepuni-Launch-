#!/usr/bin/env python3
"""LCVP 2012 review candidate. Does not write authored files or a lane."""
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
from lcvp_review_2018 import models, before_rate, choice_row, response_row
from lcvp_review_2017 import paper_raw, header_body, component_rows
from lcvp_review_2024 import split_raw
from lcvp_identity import concept_id

data = json.loads((HERE / 'source-parts.json').read_text())
records = {r['ref']: r for r in data['records']}
manifest = json.loads((HERE.parent / '2026-11-19-lcvp-2012-independent/source-manifest.json').read_text())
for s in manifest['sources']:
    assert hashlib.sha256(Path(s['path']).read_bytes()).hexdigest() == s['sha256']
paper = fitz.open(next(s['path'] for s in manifest['sources'] if s['kind'] == 'paper'))
NOTICE = 'The scheme prints no answer for this part.'
rows = {}


def body(ref):
    raw = records[ref]['sourceSchemeBlock']
    if ref.startswith('A') or ref == 'B1' or (ref.startswith('C') and ref.count('(') == 1):
        return header_body(raw)[1]
    return raw


def guidance(ref, extra=''):
    return extra + ' Printed support notes and allocation: ' + tidy(records[ref]['sourceSchemeBlock'])


def label(ref):
    return records[ref]['sourceSchemePrompt']


def ordinary(ref, count, per, expected, rate, binary=False, extra=''):
    pool = models(before_rate(body(ref), rate), expected)
    row_label = label(ref)
    if per == 1 or binary:
        row = choice_row('responses', row_label, pool, count, per, guidance(ref, extra))
    else:
        row = response_row('responses', row_label, pool, count, list(range(per + 1)), guidance(ref, extra))
    rows[ref] = [row]


def complete(ref, count, steps, extra=''):
    rows[ref] = [criterion('responses', label(ref), count, steps, guidance(ref, extra))]


def whole_missing(ref, count, steps, extra=''):
    rows[ref] = [criterion('unprinted-answer', NOTICE, count, steps, guidance(ref, extra))]


def partial(ref, scope):
    rows[ref].append(dict(id='unprinted-answer', kind='criterion', verbatim=NOTICE,
                         marks=0, permittedMarks=[0], contextNote=scope))


rows['A1'] = [point('company', tidy(body('A1')), 1)]
complete('A2', 2, [0, 1], 'Two one-mark qualifications; preserve both printed sentences without creating an extra award for studying engineering.')
ordinary('A3', 3, 1, 5, r'3\s*@\s*1m')
ordinary('A4', 4, 1, 6, r'4\s*@\s*1m')
ordinary('A5', 4, 1, 5, r'4\s*@\s*1m')
ordinary('A6', 2, 2, 4, r'2\s*@\s*2m')
partial('A6', 'This notice applies only to the unprinted valid expansions in options 2 and 3. All four printed options remain; no extra mark is added.')
ordinary('A7', 3, 2, 5, r'3\s*@\s*2m')
# Keep the printed acceptance of No separate from the five affirmative examples.
a8 = before_rate(body('A8'), r'3\s*@\s*2m')
pool = models(a8.split('*Candidates', 1)[0], 5)
rows['A8'] = [response_row('responses', label('A8'), pool, 3, [0, 1, 2], guidance('A8'))]
partial('A8', 'The scheme accepts a No answer but prints no example of that answer. The five printed affirmative responses remain; either position is assessed against the same three two-mark responses.')
ordinary('B1', 3, 2, 7, r'3\s*@\s*2\s*marks', extra='One explanation ask; each response has one mark for stating and one for description.')
ordinary('B2(i)', 2, 2, 5, r'2\s*@\s*2\s*marks')
ordinary('B2(ii)', 2, 2, 3, r'2\s*@\s*2\s*marks')
complete('B2(iii)', 4, [0, 1], 'Temporary whole source record only; the separately labelled 2+2 awards are split below.')
ordinary('B3(i)', 3, 1, 6, r'3\s*@\s*1m')
complete('B3(ii)', 3, [0, 1, 2, 3], 'Require two points on set up and one on running OR two on running and one on set up. No repetition. This is one finance-section output; the full seven printed examples remain.')
ordinary('C1(a)', 4, 1, 8, r'4\s*@\s*1m')
complete('C1(b)(i)', 2, [0, 1])
complete('C1(b)(ii)', 2, [0, 1])
whole_missing('C1(c)', 9, [0, 1], 'One application letter. Sender’s address carries one printed mark; Addressee is also printed but has no separate award. Opening/closing share one printed mark. Date, reason, statement, enclosed CV, spelling, grammar and layout each carry one. No model letter is printed.')
letter_labels = ['Sender’s address', 'Date', 'Opening- Dear.. / Closing- Yours..',
                 'RE:/Reason why they are writing', 'Statement', 'Enclose CV', 'Spelling', 'Grammar', 'Layout/Neatness']
rows['C1(c)'][0]['parts'] = [dict(id=f'criterion-{i}', verbatim=label, marks=1, permittedMarks=[0, 1])
                            for i, label in enumerate(letter_labels, 1)]
ordinary('C1(d)', 4, 2, 6, r'4\s*@\s*2\s*m')
ordinary('C2(a)', 2, 2, 7, r'2\s*@\s*2m')
c2b = before_rate(body('C2(b)'), r'3\s*@\s*2m')
pool = models(c2b.split('Relevant valid expansion required', 1)[0], 7)
rows['C2(b)'] = [response_row('responses', label('C2(b)'), pool, 3, [0, 1, 2], guidance('C2(b)'))]
partial('C2(b)', 'The notice concerns the additional valid expansion required by the scheme where a listed responsibility has no expanded explanation. All seven printed responsibilities and any printed elaborations remain. Do not invent an explanation or award a bare heading the explanation mark.')
ordinary('C2(c)', 3, 2, 5, r'3\s*@\s*2m')
ordinary('C2(d)', 3, 3, 5, r'3\s*@\s*3m')
rows['C2(d)'] = component_rows(label('C2(d)'),
    models(before_rate(body('C2(d)'), r'3\s*@\s*3m'), 5), [[1, 2]] * 3, guidance('C2(d)'))
whole_missing('C3(a)', 1, [0, 1])
ordinary('C3(b)', 3, 2, 8, r'3\s*@\s*2m')
ordinary('C3(c)', 4, 2, 7, r'4\s*@\s*2m', binary=True)
complete('C3(d)(i)', 2, [0, 1, 2, 3], 'State and explain: two responses at three marks, with printed 2+1. Keep the five paired challenge/response examples. No new semantic split is inferred within this printed part.')
complete('C3(d)(ii)', 2, [0, 2], 'Overcoming: two responses at two or zero marks. Use the challenges selected in part (i). No one-mark step or unprinted cross-part deduction.')
ordinary('C4(a)', 2, 2, 6, r'2\s*@\s*2m')
complete('C4(b)', 6, [0, 1], 'Temporary whole source record only; proposed 2+4 split is prepared below and remains subject to generic-component consistency review.')
whole_missing('C4(c)', 6, [0, 1], 'Temporary whole source record only; explicit subject/reason awards split below.')
complete('C4(d)(i)', 3, [0, 1], 'Three areas, one mark each. The paired printed (ii) receives the separate six marks.')
complete('C4(d)(ii)', 3, [0, 2], 'Three reasons, two or zero marks each. Keep the selected areas from (i). The first printed example explains that meeting the aims shows they were realistic.')
partial('C4(d)(ii)', 'Only option 1 gives a why-statement. Options 2–6 name evaluation areas without explaining why; this notice applies to those missing explanations. Keep every original area and the complete first example.')
whole_missing('C5(a)', 3, [0, 1], 'Temporary whole source record only; the explicitly labelled name and product/service awards are split below.')
complete('C5(b)', 6, [0, 1], 'Temporary whole source record only; separate agency-name and support awards split below.')
c5c = body('C5(c)')
pool = models(before_rate(c5c.split('Agenda', 1)[1], r'5\s*@\s*1m'), 7)
rows['C5(c)'] = [point('heading', 'Heading', 1), point('layout', 'Layout/numbered points', 1),
    point('election', pool[0], 1, '* Compulsory point'),
    choice_row('other-items', records['C5(c)']['questionText'], pool[1:], 4, 1,
               guidance('C5(c)', 'Election of committee is compulsory; choose four other distinct items. One seven-mark agenda.'))]
ordinary('C5(d)(i)', 5, 1, 8, r'5\s*@\s*1m')
ordinary('C5(d)(ii)', 2, 2, 6, r'2\s*@\s*2m', binary=True)
partial('C5(d)(ii)', 'This notice applies only to the unprinted valid expansion in option 6, Good management/leadership. All six printed options remain; each response receives two or zero marks.')
complete('C6(a)', 3, [0, 1], 'One definition. The scheme gives one mark for Mix of people and one each for two examples; keep all examples in its full sentence.')
rows['C6(a)'][0]['parts'] = [dict(id='mix-of-people', verbatim='Mix of people', marks=1, permittedMarks=[0, 1]),
                            dict(id='example-1', verbatim='Example 1', marks=1, permittedMarks=[0, 1]),
                            dict(id='example-2', verbatim='Example 2', marks=1, permittedMarks=[0, 1])]
ordinary('C6(b)', 2, 3, 5, r'2\s*@\s*3m')
rows['C6(b)'] = component_rows(label('C6(b)'),
    models(before_rate(body('C6(b)'), r'2\s*@\s*3m'), 5), [[2, 1]] * 2, guidance('C6(b)'))
ordinary('C6(c)', 4, 2, 5, r'4\s*@\s*2m', binary=True)
ordinary('C6(d)', 4, 2, 7, r'4\s*@\s*2m')
assert set(rows) == set(records)


def source(pages, kind='source-question', title='Original question'):
    return dict(kind=kind, label='OFFICIAL SOURCE', title=title, pages=pages,
                attribution='SEC LCVP Link Modules 2012 Common Level — © State Examinations Commission.',
                presentationNote='Read the complete original source and question in context.')


native_case = paper[7].get_text(sort=False)
case = native_case[native_case.index('GLENCAR COMMUNITY RESOURCE CENTRE'):]
case = re.sub(r'Page 8 of 32\s*', '', case)
# Keep the six complete prose paragraphs; chart geometry carries the original
# values before reveal. The following transcription is checked against page8.
prose, chart = case.split('\n0\n5\n10\n15\n20\n25\n30\n35\n', 1)
assert tidy(chart) == 'Creche Youth Club/Café Retirement Group Meeting & Training Facilities Recreational Classes Uses for Resource Centre'
case_before, case_after = prose.split('The committee is currently', 1)
case_after = 'The committee is currently' + case_after
case_text = tidy(case_before) + '\n\nUses for Resource Centre: Creche 30; Youth Club/Café 20; Retirement Group 15; Meeting & Training Facilities 20; Recreational Classes 15.\n\n' + tidy(case_after)
stems = {}
for q, number in [(1, 14), (2, 17), (3, 20), (4, 23), (5, 26), (6, 29)]:
    text = re.split(r'^\s*Q\.\s*' + str(q) + r'\s+', paper_raw(paper, number), maxsplit=1, flags=re.M)[1]
    stems[q] = tidy(text.split('(a)', 1)[0])
heading_topics = {
    'audio-visual': '1-1', '1-career-investigation': '0-2', '1-job-seeking-skills': '0-1',
    '1-introduction-to-working-life': '0-0', '2-enterprise-skills': '1-0',
    '2-local-voluntarycommunity-enterprises': '1-2', '2-an-enterprise-activity': '1-3',
    '2-local-business-enterprises': '1-1'}
cards = []
for ref, record in records.items():
    section, number = ref[0], int(ref[1])
    heading = record['firstReaderHeading'].removeprefix('link-modules-common-')
    card = dict(id=record['id'], subjectId='lcvp', topicId='lcvp-link-modules-' + heading_topics[heading],
                conceptId=concept_id(record['id'], record['id'].removeprefix('lcvp-2012-cl-') + '-2012-source'),
                level='common', year=2012, section=section,
                questionRef='2012 CL Section ' + section + ' Q' + ref[1:],
                questionText=record['questionText'], stem=case_text if section == 'B' else stems[number] if section == 'C' else '',
                figureKey='', labelKey=[], totalMarks=sum(record['proposedCardMarks']), rows=rows[ref],
                tariffModel=dict(kind='fixed', notation='Original 2012 marking scheme allocation.'),
                sourceMaterial=source(record['paperPages']))
    if section == 'A':
        url = 'https://www.examinations.ie/archive/exampapers/2012/LC462CLP031EV.mov'
        card['videoMaterial'] = dict(kind='source-video', label='OFFICIAL VIDEO', title='2012 LCVP audiovisual examination',
                                    playbackUrl=url, canonicalUrl=url, secFileid='LC462CLP031EV.mov',
                                    attribution='State Examinations Commission — original 2012 Common Level English audiovisual recording.',
                                    presentationNote='Watch the original sequence with its sound before answering. Follow the printed viewing instructions.')
        card['additionalSourceMaterials'] = [source([2], title='Original audiovisual instructions')]
    elif section == 'B':
        card['sourceMaterial'] = source([8], 'source-text', 'Glencar Community Resource Centre — complete case study and chart')
        card['additionalSourceMaterials'] = [source(record['paperPages'])]
    elif number == 1:
        card['additionalSourceMaterials'] = [source([14], 'source-text', 'Original Newsradio job advertisement')]
    if section == 'C' and number == 3 and ref != 'C3(a)':
        card['stem'] += ' ' + records['C3(a)']['questionText']
    if ref == 'C3(d)(ii)':
        card['stem'] += ' ' + records['C3(d)(i)']['questionText']
    if ref == 'C4(d)(ii)':
        card['stem'] += ' ' + records['C4(d)(i)']['questionText']
    cards.append(card)


def split(ref, boundary, marks, new_rows):
    i = next(i for i, c in enumerate(cards) if c['id'] == records[ref]['id'])
    original = cards[i]
    pos = original['questionText'].index(boundary)
    texts = [original['questionText'][:pos].strip(), original['questionText'][pos:].strip()]
    assert ' '.join(texts) == original['questionText']
    parts = []
    for n in range(2):
        card = deepcopy(original)
        card.update(questionText=texts[n], totalMarks=marks[n], rows=new_rows[n])
        if n:
            card['id'] += '-2'
            card['conceptId'] += '-second-ask'
            card['stem'] += ' ' + texts[0]
        parts.append(card)
    cards[i:i + 1] = parts


need_names = ['Creche', 'Youth Club/Cafe', 'Retirement Group', 'Meeting/training facilities:', 'Recreational:']
assert all(n in body('B2(iii)') for n in need_names)
split('B2(iii)', 'What are the implications', [2, 2], [
    [choice_row('need', 'Select a need.', need_names, 1, 2, guidance('B2(iii)'))],
    [criterion('implications', 'Implications for the committee of this choice.', 2, [0, 1], guidance('B2(iii)', 'Use the same selected need. Valid implication to the need is required.'))]])
method_names = [tidy(line) for line in [
    'Telephone call, face to face meetings, talking with school Principal and teachers and anyone else involved.',
    'Survey/Questionaire/Sugggestion Box', 'Internet', 'Brainstorming/Class Discussion/Group discussion', 'Publications']]
assert all(name in tidy(body('C4(b)')) for name in method_names)
split('C4(b)', 'Analyse the usefulness', [2, 4], [
    [choice_row('methods', 'State two research methods', method_names, 2, 1, guidance('C4(b)', 'Proposed name allocation from the printed 2@3m(1+2), awaiting consistency adjudication.'))],
    [criterion('usefulness', 'Analyse' + label('C4(b)').split('Analyse', 1)[1], 2, [0, 1, 2], guidance('C4(b)', 'Use the same two research methods. Keep all positive details and the acceptance of valid criticism with expansion. Proposed 2+4 split awaits adjudication.'))]])
split('C4(c)', 'Give a reason', [2, 4], [
    [criterion('unprinted-answer', NOTICE, 2, [0, 1], guidance('C4(c)', 'Naming subject, one mark for each of two subjects.'))],
    [criterion('unprinted-answer', NOTICE, 2, [0, 1, 2], guidance('C4(c)', 'Valid reason for each same subject, two marks each.'))]])
split('C5(a)', 'and identify', [1, 2], [
    [criterion('unprinted-answer', NOTICE, 1, [0, 1], guidance('C5(a)', 'Name: one mark.'))],
    [criterion('unprinted-answer', NOTICE, 1, [0, 2], guidance('C5(a)', 'Product/service: two marks; the same named business. No intermediate award is printed.'))]])
agency_names = ['County Enterprise Boards', 'Enterprise Ireland', 'Local Area Partnerships', 'Leader Plus', 'FAS/Solas', 'Udaras na Gaeltachta', 'IDA Ireland', 'Teagasc', 'Failte Ireland']
assert all(n in body('C5(b)') for n in agency_names)
split('C5(b)', 'Outline the type', [2, 4], [
    [choice_row('agencies', 'Name agency', agency_names, 2, 1, guidance('C5(b)'))],
    [criterion('agency-1-support', 'Type of support', 2, [0, 1], guidance('C5(b)', 'First selected agency: two one-mark support details. Keep each support attached to its agency; do not transfer a printed example between agencies.')),
     criterion('agency-2-support', 'Type of support', 2, [0, 1], guidance('C5(b)', 'Second selected agency: two one-mark support details. Use a different agency from the first response.')),
     dict(id='unprinted-answer', kind='criterion', verbatim=NOTICE, marks=0, permittedMarks=[0],
          contextNote='No support examples are printed for Local Area Partnerships, Udaras na Gaeltachta, IDA Ireland, Teagasc or Failte Ireland. All nine names and the full four printed support pools remain.')]])

assert len(cards) == 47 and len({c['id'] for c in cards}) == 47
for card in cards:
    for row in card['rows']:
        if row['verbatim'] == NOTICE:
            row['unprinted'] = True
            if row['marks'] == 0:
                # Notices have no mark ladder. A one-value permittedMarks array
                # is rejected by the existing shared shape validator.
                row.pop('permittedMarks', None)
assert sum(c['totalMarks'] for c in cards) == 210
assert all(sum(r['marks'] for r in c['rows']) == c['totalMarks'] for c in cards)
assert all('Office Use' not in c['questionText'] for c in cards)
(HERE / 'proposed-47-authored-cards.json').write_text(json.dumps(cards, ensure_ascii=False, indent=2) + '\n')
proof = dict(recordedAt=datetime.now(timezone.utc).isoformat(), status='REVIEW ONLY — not applied or production verified',
             proposedAsks=47, originalParts=42, offeredMarks=210,
             sourcePartFileSha256=hashlib.sha256((HERE / 'source-parts.json').read_bytes()).hexdigest(),
             payloadSha256=hashlib.sha256((HERE / 'proposed-47-authored-cards.json').read_bytes()).hexdigest(),
             wholeNoAnswerIds=[c['id'] for c in cards if len(c['rows']) == 1 and c['rows'][0]['verbatim'] == NOTICE],
             partialNoAnswerIds=[c['id'] for c in cards if len(c['rows']) > 1 and c['rows'][-1]['verbatim'] == NOTICE],
             outstanding=['Source-selection audit against original pages', 'Independent candidate review', 'Five topic decisions and generic split consistency adjudication',
                          'Fresh SEC R4 archive recheck', 'Native video hosting/playback', 'Lane integration, source bindings, canonical filings and automatic checks'])
(HERE / 'candidate-proof.json').write_text(json.dumps(proof, indent=2) + '\n')
print(json.dumps(proof, indent=2))
