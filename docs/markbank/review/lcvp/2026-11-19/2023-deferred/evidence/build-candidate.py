#!/usr/bin/env python3
"""Review-only 2023 deferred candidate, with unresolved split proposals labelled."""
from pathlib import Path
from datetime import datetime, timezone
from copy import deepcopy
import hashlib
import json
import re
import sys

HERE = Path(__file__).resolve().parent
LANE = Path('/Users/alexlinehan/Documents/Nextstepuni-LCVP-Release-20261119')
sys.path.insert(0, str(LANE / 'scripts/markbank/authoring'))
from lcvp_review_2026 import tidy, point, criterion
from lcvp_review_2018 import models, choice_row
from lcvp_identity import concept_id

data = json.loads((HERE / 'source-parts.json').read_text())
manifest = json.loads((HERE.parent / '2026-11-19-lcvp-2023-deferred-independent/source-manifest.json').read_text())
for s in manifest['sources']:
    assert hashlib.sha256(Path(s['path']).read_bytes()).hexdigest() == s['sha256']
records = {r['ref']: r for r in data['records']}
NOTICE = 'The scheme prints no answer for this part.'
rows = {}
whole = set()


def label(ref):
    return records[ref]['sourceSchemePrompt']


def guide(ref, extra=''):
    return extra + ' Complete original wording, models and allocation: ' + tidy(records[ref]['sourceSchemeBlock'])


def control(ref, count, steps, extra=''):
    rows[ref] = [criterion('responses', label(ref), count, steps, guide(ref, extra))]


def missing(ref, count, steps, extra=''):
    rows[ref] = [criterion('unprinted-answer', NOTICE, count, steps, guide(ref, extra))]


def pool(ref, expected):
    block = records[ref]['sourceSchemeBlock']
    start = re.search(r'^\s*1\.\s+', block, re.M)
    assert start, ref
    return models(block[start.start():], expected)


def choice(ref, count, per, expected, extra=''):
    rows[ref] = [choice_row('responses', label(ref), pool(ref, expected), count, per, guide(ref, extra))]


rows['A1'] = [point('name', 'Meitheal Ltd', 1)]
choice('A2', 2, 1, 3, 'Preserve the printed Ge to do the actual job wording.')
control('A3', 3, [0, 1], 'One complete definition; three one-mark components, with its full printed model.')
choice('A4', 3, 1, 4)
choice('A5', 3, 1, 5)
choice('A6', 3, 2, 5, 'The scheme gives three responses two or zero marks each, with no separate award for reasons. Keep the full question together.')
rows['A6'].append(dict(id='unprinted-answer', kind='criterion', verbatim=NOTICE, marks=0, unprinted=True,
                      contextNote='The source lists five actions but supplies no reasons for them. This notice applies only to those missing reasons and adds no marks.'))
control('A7', 3, [0, 1, 2])
control('A8', 3, [0, 1, 2], 'The question excludes feedback; retain all seven other printed examples.')
control('B1', 3, [0, 1, 2])
choice('B2(i)', 3, 1, 9)
control('B2(ii)', 3, [0, 1, 2], 'Temporary whole source record; proposed split below requires third-reader validation.')
choice('B3(i)', 3, 1, 7)
control('B3(ii)', 2, [0, 1, 2, 3], 'Retain all six complete planning models. The paper rendering lacks the visible (ii) label; the scheme supplies it. This distinct question is counted once.')
control('B3(iii)', 3, [0, 1, 2], 'Retain all seven advantage models and five disadvantage models. No separate pool totals or required numerical mix are printed.')
missing('C1(a)', 4, [0, 1], 'Temporary source grouping; the explicitly separate naming and outline awards are split below.')
control('C1(b)', 5, [0, 1], 'Five distinct suitable questions relevant to the chosen organisation. The source gives eight examples and Etc.; none is compulsory.')
control('C1(c)', 4, [0, 1, 2])
choice('C1(d)(i)', 2, 1, 3)
control('C1(d)(ii)', 6, [0, 1], 'Temporary source grouping; explicit method/reason awards split below. Preserve all five complete method-and-reason pools.')
missing('C2(a)', 3, [0, 1], 'Temporary source grouping; the explicitly separate naming and qualities awards are split below.')
control('C2(b)', 6, [0, 1], 'Temporary source grouping; explicit source/relevance awards split below.')
missing('C2(c)', 5, [0, 1, 2], 'One career investigation. The six printed headings guide the five pieces of information, each with two one-mark components. There is no completed career-specific model.')
control('C2(d)', 3, [0, 1, 2])
missing('C3(a)', 1, [0, 2], 'Four names receive two marks in total. No per-name half-mark award or intermediate mark is printed.')
control('C3(b)', 3, [0, 2], 'Temporary source grouping; separately labelled need and solutions awards split below.')
rows['C3(c)'] = [criterion('heading-' + str(i), heading, 2, [0, 1], guide('C3(c)',
                 'Two distinct relevant statements under this heading. No marks for headings; no repetition.'))
                 for i, heading in enumerate(['Strengths:', 'Weaknesses/Challenges:', 'Opportunities:', 'Threats:'], 1)]
rows['C3(d)'] = [criterion('response-' + str(i), label('C3(d)'), 1, list(range(mark + 1)),
                  guide('C3(d)', f'Response {i} of four. One response receives up to three marks and the other three up to two each. No named model is assigned the larger award.'))
                  for i, mark in enumerate([3, 2, 2, 2], 1)]
promotions = 'Media/advertisements/brochures/posters/presentations/special events/displays & exhibits/promotional material/visit in from a representative'
assert promotions in tidy(records['C4(a)']['sourceSchemeBlock'])
rows['C4(a)'] = [point('complete-pool', promotions, None, guide('C4(a)',
                   'Four ways receive two marks in total; no internal award is printed. Assess the complete response against the two-mark total.'))]
whole.add('C4(a)')
missing('C4(b)', 3, [0, 2], 'One account under Services Provided, Finance and Staffing. Two or zero marks for each section, no heading marks. Keep all printed guiding questions; no organisation-specific example is printed.')
for part, heading in zip(rows['C4(b)'][0]['parts'], ['Services Provided', 'Finance', 'Staffing']):
    part['verbatim'] = heading
control('C4(c)', 4, [0, 1, 2], 'Keep all eight complete obligations across both scheme pages.')
control('C4(d)', 3, [0, 1, 2, 3])
control('C5(a)', 3, [0, 1], 'One complete definition with three one-mark components and its full model.')
rows['C5(b)'] = [point('model-' + str(i), text, None, guide('C5(b)',
                 'Three ways receive eight marks in total, with no per-response split. Assess the whole response against eight; do not infer 3+3+2.') if i == 1 else '')
                 for i, text in enumerate(pool('C5(b)', 7), 1)]
whole.add('C5(b)')
control('C5(c)', 3, [0, 1, 2])
control('C5(d)', 4, [0, 1, 2], 'No repetition of answers; preserve all nine complete models.')
control('C6(a)', 4, [0, 1], 'One complete definition, four one-mark components; retain the full model.')
control('C6(b)', 4, [0, 1], 'Temporary source grouping; proposed skills/qualities split requires third-reader validation.')
control('C6(c)', 4, [0, 1, 2])
control('C6(d)', 3, [0, 1, 2, 3])
rows['C7(a)'] = [point('definition', 'A Recruitment Agency is a business that will find employees/staff for an employer.', 2,
                       guide('C7(a)', 'Two or zero marks; no one-mark step is printed.'))]
choice('C7(b)', 3, 2, 6)
control('C7(c)', 3, [0, 1, 2, 3])
control('C7(d)', 4, [0, 1, 2])
assert set(rows) == set(records)


def source(pages, kind='source-question', title='Original deferred question'):
    return dict(kind=kind, label='OFFICIAL SOURCE', title=title, pages=pages,
                attribution='SEC LCVP Link Modules 2023 Common Level, deferred examination — © State Examinations Commission.',
                presentationNote='Read the complete original source and question in context.')


heading_topics = {'1-career-investigation': '0-2', '1-job-seeking-skills': '0-1',
                  '1-introduction-to-working-life': '0-0', '1-work-placement': '0-3',
                  '2-enterprise-skills': '1-0', '2-local-voluntarycommunity-enterprises': '1-2',
                  '2-an-enterprise-activity': '1-3', '2-local-business-enterprises': '1-1'}
cards = []
for ref, r in records.items():
    section, number = ref[0], int(ref[1])
    headings = r['firstReaderHeadings']
    # These are provisional first-reader topics; canonical independent filings
    # and the six third-reader decisions must precede any production integration.
    topics = ['lcvp-link-modules-' + heading_topics[h.removeprefix('link-modules-common-')]
              if not h.endswith('-audio-visual') else 'lcvp-link-modules-0-3' for h in headings]
    card = dict(id=r['id'], subjectId='lcvp', topicId=topics[0],
                conceptId=concept_id(r['id'], r['id'].removeprefix('lcvp-2023-cl-') + '-source'),
                level='common', year=2023, section=section,
                questionRef='2023 CL Section ' + section + ' Q' + ref[1:] + ' — Deferred sitting',
                questionText=r['questionText'], stem=data['caseStudy'] if section == 'B' else data['sectionCStems'][str(number)] if section == 'C' else '',
                figureKey='', labelKey=[], totalMarks=sum(r['proposedCardMarks']), rows=rows[ref],
                tariffModel=dict(kind='questionTotal' if ref in whole else 'fixed', notation='Original 2023 deferred marking scheme allocation.'),
                sourceMaterial=source(r['paperPages']))
    if len(topics) > 1:
        card['additionalTopicIds'] = topics[1:]
    if section == 'A':
        url = 'https://www.examinations.ie/archive/deferredexams/2023/LC462CLP031EV.mov'
        card['videoMaterial'] = dict(kind='source-video', label='OFFICIAL VIDEO', title='2023 deferred LCVP audiovisual examination',
                                    playbackUrl=url, canonicalUrl=url, secFileid='LC462CLP031EV.mov',
                                    attribution='State Examinations Commission — original 2023 Common Level English deferred audiovisual recording.',
                                    presentationNote='Watch the original deferred sequence with sound before answering. Follow the printed viewing instructions.')
        card['additionalSourceMaterials'] = [source([3], title='Original deferred audiovisual instructions')]
    elif section == 'B':
        card['sourceMaterial'] = source([9], 'source-text', 'Ballyfert — complete case study')
        card['additionalSourceMaterials'] = [source(r['paperPages'])]
    elif number in [1, 2] and ref != f'C{number}(a)':
        card['stem'] += ' ' + records[f'C{number}(a)']['questionText']
    cards.append(card)


split_proof = []
def split(ref, boundary, allocations, new_rows, scopes):
    index = next(i for i, c in enumerate(cards) if c['id'] == records[ref]['id'])
    original = cards[index]
    text = original['questionText']; position = text.index(boundary)
    selected = [text[:position].strip(), text[position:].strip()]
    parts = []
    for n in range(2):
        card = deepcopy(original)
        card.update(questionText=selected[n], totalMarks=allocations[n], rows=new_rows[n])
        card['stem'] += ' ' + text
        card['questionRef'] = card['questionRef'].removesuffix(' — Deferred sitting') + ' — ' + scopes[n] + ' — Deferred sitting'
        if n:
            card['id'] += '-2'; card['conceptId'] += '-second-ask'
        parts.append(card)
    cards[index:index + 1] = parts
    split_proof.append(dict(ref=ref, originalPrompt=text, selectedPrompts=selected, marks=allocations,
                            fullOriginalRetainedBeforeReveal=True,
                            thirdReaderRequired=ref in ['B2(ii)', 'C6(b)']))


def component(ref, key, text, count, steps, extra=''):
    return [criterion(key, text, count, steps, guide(ref, extra))]


split('B2(ii)', 'Give reasons', [3, 3],
      [component('B2(ii)', 'ways', label('B2(ii)'), 3, [0, 1], 'Proposed three one-mark ways; third-reader validation required.'),
       component('B2(ii)', 'reasons', label('B2(ii)'), 3, [0, 1], 'One reason for each same chosen way. Proposed split; third-reader validation required.')], ['ways', 'reasons'])
split('C1(a)', 'and give', [1, 3],
      [component('C1(a)', 'unprinted-answer', NOTICE, 1, [0, 1]),
       component('C1(a)', 'unprinted-answer', NOTICE, 1, [0, 3], 'The outline has a printed three-mark award with no internal split or intermediate award; retain the printed three-mark criterion.')], ['name', 'services'])
split('C1(d)(ii)', 'Give a reason', [3, 3],
      [component('C1(d)(ii)', 'methods', label('C1(d)(ii)'), 3, [0, 1]),
       component('C1(d)(ii)', 'reasons', label('C1(d)(ii)'), 3, [0, 1], 'One reason for each same selected method.')], ['methods', 'reasons'])
split('C2(a)', 'and outline', [1, 2],
      [component('C2(a)', 'unprinted-answer', NOTICE, 1, [0, 1]),
       component('C2(a)', 'unprinted-answer', NOTICE, 2, [0, 1], 'The qualities must be explained, not just named; the same selected career is retained.')], ['career', 'qualities'])
split('C2(b)', 'How was', [3, 3],
      [component('C2(b)', 'sources', label('C2(b)'), 3, [0, 1]),
       component('C2(b)', 'relevance', label('C2(b)'), 3, [0, 1], 'One relevance point for each same source.')], ['sources', 'relevance'])
split('C3(b)', 'and suggest', [2, 4],
      [component('C3(b)', 'unprinted-answer', NOTICE, 1, [0, 2]),
       component('C3(b)', 'solutions', label('C3(b)'), 2, [0, 2], 'Two solutions for the same identified need. Keep all seven printed examples and Etc.; equivalent valid solutions remain possible.')], ['need', 'solutions'])
# Shared verb and object are selected from the original sentence; the complete
# sentence remains before reveal. The allocation is an explicit review proposal.
ref = 'C6(b)'; index = next(i for i, c in enumerate(cards) if c['id'] == records[ref]['id'])
original = cards[index]; text = original['questionText']
assert text == 'Outline two skills and two qualities of an entrepreneur that you are familiar with.'
tail = ' of an entrepreneur that you are familiar with.'
parts = []
for n, (selection, scope) in enumerate([('Outline two skills' + tail, 'skills'), ('Outline two qualities' + tail, 'qualities')]):
    c = deepcopy(original); c.update(questionText=selection, totalMarks=2,
        rows=component(ref, scope, label(ref), 2, [0, 1], 'Proposed two marks for this category; third-reader validation required. Preserve Skills and Qualities lists and List is not exhaustive.'))
    c['stem'] += ' ' + text; c['questionRef'] = c['questionRef'].removesuffix(' — Deferred sitting') + ' — ' + scope + ' — Deferred sitting'
    if n:
        c['id'] += '-2'; c['conceptId'] += '-second-ask'
    parts.append(c)
cards[index:index + 1] = parts
split_proof.append(dict(ref=ref, originalPrompt=text, selectedPrompts=[c['questionText'] for c in parts], marks=[2, 2],
                        fullOriginalRetainedBeforeReveal=True, thirdReaderRequired=True, sharedVerbAndObject=True))
for c in cards:
    for row in c['rows']:
        if row['verbatim'] == NOTICE:
            row['unprinted'] = True
    if c['tariffModel']['kind'] != 'questionTotal':
        assert sum(r['marks'] for r in c['rows']) == c['totalMarks'], c['id']
assert len(cards) == len({c['id'] for c in cards}) == 50
assert sum(c['totalMarks'] for c in cards) == 235
assert len([c for c in cards if len(c['rows']) == 1 and c['rows'][0].get('unprinted')]) == 8
output = HERE / 'proposed-50-authored-cards.json'
output.write_text(json.dumps(cards, ensure_ascii=False, indent=2) + '\n')
(HERE / 'split-source-selections.json').write_text(json.dumps(split_proof, ensure_ascii=False, indent=2) + '\n')
proof = dict(recordedAt=datetime.now(timezone.utc).isoformat(), status='Review-only; not applied or independently reviewed',
             cards=50, sourceParts=43, offeredMarks=235, examMaximum=160,
             wholeNoAnswerNotices=8, partialNoAnswerNotices=1, wholeQuestionAwards=['C4(a)', 'C5(b)'],
             payloadSha256=hashlib.sha256(output.read_bytes()).hexdigest(),
             outstanding=['Second-reader candidate/source inspection', 'Two proposed splits and six headings need third reading',
                          'Question/answer source tracing', 'Deferred media binding and hosted video verification',
                          'Fresh R4 archive checks', 'Canonical filings, Atlas/source bindings and application checks'])
(HERE / 'candidate-proof.json').write_text(json.dumps(proof, indent=2) + '\n')
print(json.dumps(proof, indent=2))
