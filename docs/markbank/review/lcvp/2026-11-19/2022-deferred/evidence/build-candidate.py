#!/usr/bin/env python3
"""Review-only 2022 deferred draft; disputed splits remain provisional."""
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
from lcvp_review_2018 import models, choice_row
from lcvp_review_2017 import component_rows
from lcvp_identity import concept_id

data = json.loads((HERE / 'source-parts.json').read_text())
manifest = json.loads((HERE.parent / '2026-11-19-lcvp-2022-deferred-independent/source-manifest.json').read_text())
for s in manifest['sources']:
    assert hashlib.sha256(Path(s['path']).read_bytes()).hexdigest() == s['sha256']
scheme = fitz.open(next(s['path'] for s in manifest['sources'] if s['kind'] == 'scheme'))
records = {r['ref']: r for r in data['records']}
NOTICE = 'The scheme prints no answer for this part.'
rows = {}


def label(ref):
    return records[ref]['sourceSchemePrompt']


def guide(ref, extra=''):
    return extra + ' Complete original wording, models and allocation: ' + tidy(records[ref]['sourceSchemeBlock'])


def control(ref, count, steps, extra=''):
    rows[ref] = [criterion('responses', label(ref), count, steps, guide(ref, extra))]


def missing(ref, count, steps, extra=''):
    rows[ref] = [criterion('unprinted-answer', NOTICE, count, steps, guide(ref, extra))]


def partial(ref, note):
    rows[ref].append(dict(id='unprinted-answer', kind='criterion', verbatim=NOTICE,
                         marks=0, unprinted=True, contextNote=note + ' This notice adds no marks.'))


control('A1', 1, [0, 1])
control('A2', 2, [0, 1], 'Two areas, Tourism and Business enterprise, with their complete printed explanations. Keep as one ask.')
for part, heading in zip(rows['A2'][0]['parts'], ['Tourism', 'Business enterprise']):
    part['verbatim'] = heading
control('A3', 3, [0, 1], 'One complete CSR definition, with three one-mark components.')
control('A4', 4, [0, 1])
control('A5', 2, [0, 2], 'Choose ONE of Community, Workplace, Environment or Market place. Credit two examples from that same chosen area, two or zero marks each. Keep all four complete printed pools; do not combine areas.')
control('A6', 2, [0, 1, 2], 'Keep the agreement question open. The scheme supplies three advertising-benefit models and does not require a YES answer. No invented negative model.')
control('A7', 6, [0, 1], 'The scheme prints Three valid reasons and 6 x 1 mark. Preserve both statements: six one-mark components overall, without inventing a fixed mark allocation to the three reason groups.')
control('A8', 3, [0, 1, 2])
control('B1', 3, [0, 1, 2], 'One printed choice: explain three of the four terms. Keep all four complete models, including all Overheads examples. Do not count a term twice.')
control('B2(i)', 1, [0, 1])
control('B2(ii)', 2, [0, 1, 2])
control('B2(iii)', 2, [0, 1, 2])
control('B3(i)', 2, [0, 1, 2], 'Temporary source grouping; proposed positive/negative split needs third-reader validation.')
control('B3(ii)', 3, [0, 1, 2], 'Provisional whole ask. Generic 3 x 2 (1+1) does not name separate identification/explanation awards. A third reader decides whether it must split.')
control('C1(a)', 2, [0, 2])
control('C1(b)', 2, [0, 2], 'Two suitable interview questions, two marks each. Keep all four printed examples; no specific pair is compulsory.')
# Separate the actual letter from the neighbouring summary table by recorded
# original-page coordinates, retaining every visible letter line in order.
letter_lines = []
for block in scheme[9].get_text('dict')['blocks']:
    for line in block.get('lines', []):
        x, y, _, _ = line['bbox']
        text = tidy(''.join(s['text'] for s in line['spans']))
        if 147 < y < 380 and text and (y < 270 or x < 340):
            letter_lines.append((y, x, text, list(line['bbox'])))
letter_lines.sort()
paragraphs = []; previous = None
for y, x, text, box in letter_lines:
    if previous is None or y - previous > 20:
        paragraphs.append(text)
    else:
        paragraphs[-1] += ' ' + text
    previous = y
letter = '\n\n'.join(paragraphs)
assert len(paragraphs) == 7 and letter.endswith('John Smith')
assert 'Summary of marks' not in letter and 'my referees.' in letter
criteria = ['Own address', 'Business address', 'Date', 'Subject line', 'Opening', 'Introduction/reason', 'Closing', 'CV/references']
assert all(t in tidy(records['C1(c)']['sourceSchemeBlock']) for t in criteria)
rows['C1(c)'] = [point('criterion-' + str(i), text, 1,
                      'Original model letter:\n\n' + letter + '\n\nSummary of marks: ' + '; '.join(t + ' 1m' for t in criteria) + '; Total 8m.' if i == 1 else '')
                 for i, text in enumerate(criteria, 1)]
partial('C1(c)', 'The scheme gives one mark each for Own address, Business address and Date, but its model letter begins at Re: and prints none of those three fields. The complete model and all eight printed criteria are retained; no address or date is invented.')
(HERE / 'letter-model-extraction-proof.json').write_text(json.dumps(dict(
    schemeSha256=data['sourceSha256']['scheme'], page=10, selectedLines=letter_lines,
    letter=letter, criteria=criteria, originalImageViewed='2022-deferred-independent/original-pages/scheme-10.png',
    scope='All seven visible model paragraphs and eight printed one-mark criteria; no invented sender/address/date inserted.'), ensure_ascii=False, indent=2) + '\n')
control('C1(d)', 3, [0, 1, 2, 3])
missing('C2(a)', 1, [0, 2])
control('C2(b)', 3, [0, 1, 2], 'Eight complete examples plus Etc.; retain the same chosen community association.')
control('C2(c)(i)', 2, [0, 1], 'Six actual preparation examples plus Etc. The printed numbering skips 5; do not create a missing example.')
control('C2(c)(ii)', 3, [0, 2], 'Three personal qualities at two marks each. The source prints no one-mark step; examples plus Etc. remain open.')
control('C2(d)', 3, [0, 1, 2, 3], 'Keep every continuation in all seven evaluation-method models. No separate naming/reason awards are printed.')
control('C3(a)', 4, [0, 1], 'One agenda with four one-mark items chosen from the seven printed examples. No compulsory item or extra layout/heading award is printed.')
control('C3(b)', 2, [0, 1, 2])
rows['C3(c)'] = component_rows(label('C3(c)'), [tidy(records['C3(c)']['sourceSchemeBlock'])], [[2, 2], [2, 2]],
    'Provisional whole ask. Two responses, each with two indivisible two-mark components. No semantic allocation is invented; a third reader decides the split.')
partial('C3(c)', 'The scheme names eleven skills plus Etc. but prints no descriptions. Retain all names and the printed 2 x 4 (2+2) allocation.')
headings = ['Aims/Objectives', 'Research Methods', 'Analysis of Research', 'Action Steps', 'Schedule of Time', 'Schedule of Costs', 'Evaluation Methods']
assert all(h in records['C3(d)']['sourceSchemeBlock'] for h in headings)
rows['C3(d)'] = [choice_row('headings', label('C3(d)'), headings, 4, 1, guide('C3(d)', 'One event plan with four appropriate headings.')),
                 criterion('unprinted-answer', NOTICE, 5, [0, 1], guide('C3(d)', 'The five one-mark action steps have no printed example answers. The seven printed headings remain above.'))]
missing('C4(a)', 4, [0, 1])
control('C4(b)', 2, [0, 1, 2])
control('C4(c)', 8, [0, 1], 'Temporary source grouping; explicit sources and developed-point awards split below.')
control('C4(d)', 9, [0, 1], 'Temporary source grouping; the scheme explicitly separates challenges and solutions below.')
control('C5(a)', 1, [0, 2], 'Retain all twelve printed agency names, including their historical wording. No one-mark step is printed.')
control('C5(b)', 3, [0, 1, 2])
control('C5(c)', 4, [0, 1, 2])
control('C5(d)', 3, [0, 1, 2, 3])
partial('C5(d)', 'The eight printed characteristics are names only; the scheme prints no developed descriptions. Keep the original 3 x 3 (1+1+1) award.')
missing('C6(a)(i)', 1, [0, 1])
missing('C6(a)(ii)', 1, [0, 1])
control('C6(b)', 3, [0, 2], 'The source allows any other relevant skill/quality with valid explanations. Preserve all six complete models and the chosen-career context.')
control('C6(c)', 4, [0, 1, 2], 'Provisional whole ask: a third reader decides whether generic 1+1 supplies separate source/relevance awards. Retain all six source models.')
partial('C6(c)', 'The relevance of source options 2 and 6 is not printed. Retain the four developed source examples and those two names.')
control('C6(d)', 3, [0, 1, 2, 3], 'YES or NO is explicitly allowed. Keep all printed positive examples and original duplicated numbering; do not require agreement.')
partial('C6(d)', 'The scheme permits NO but gives no model answer for that route. Do not invent negative examples.')
control('C7(a)', 2, [0, 2], 'One whole market-research definition. The scheme prints 2+2, without assigning those awards to particular phrases; do not create a semantic split.')
control('C7(b)', 2, [0, 1, 2])
control('C7(c)', 4, [0, 1, 2], 'Provisional whole ask: a third reader decides whether generic 1+1 permits separate naming/explanation cards.')
partial('C7(c)', 'The nine printed forms of promotion have no explanations. Preserve all nine source examples, without inventing reasons.')
control('C7(d)', 3, [0, 1, 2, 3])
assert set(rows) == set(records)


def source(pages, kind='source-question', title='Original deferred question'):
    return dict(kind=kind, label='OFFICIAL SOURCE', title=title, pages=pages,
                attribution='SEC LCVP Link Modules 2022 Common Level, deferred examination — © State Examinations Commission.',
                presentationNote='Read the complete original source and question in context.')


heading_topics = {'1-career-investigation': '0-2', '1-job-seeking-skills': '0-1',
                  '1-introduction-to-working-life': '0-0', '1-work-placement': '0-3',
                  '2-enterprise-skills': '1-0', '2-local-voluntarycommunity-enterprises': '1-2',
                  '2-an-enterprise-activity': '1-3', '2-local-business-enterprises': '1-1'}
cards = []
for ref, r in records.items():
    section, number = ref[0], int(ref[1])
    topics = ['lcvp-link-modules-' + heading_topics[h.removeprefix('link-modules-common-')] for h in r['firstReaderHeadings']]
    card = dict(id=r['id'], subjectId='lcvp', topicId=topics[0],
                conceptId=concept_id(r['id'], r['id'].removeprefix('lcvp-2022-cl-') + '-source'),
                level='common', year=2022, section=section,
                questionRef='2022 CL Section ' + section + ' Q' + ref[1:] + ' — Deferred sitting',
                questionText=r['questionText'], stem=data['caseStudy'] if section == 'B' else data['sectionCStems'][str(number)] if section == 'C' else '',
                figureKey='', labelKey=[], totalMarks=sum(r['proposedCardMarks']), rows=rows[ref],
                tariffModel=dict(kind='fixed', notation='Original 2022 deferred marking scheme allocation.'),
                sourceMaterial=source(r['paperPages']))
    if len(topics) > 1:
        card['additionalTopicIds'] = topics[1:]
    if section == 'A':
        # Review-only: no official recording has yet been verified. Do not
        # fabricate a URL, substitute June, or claim it was unpublished.
        card['additionalSourceMaterials'] = [source([3], title='Original deferred audiovisual instructions')]
    elif section == 'B':
        card['sourceMaterial'] = source([10], 'source-text', 'Alex and Rami — complete case study')
        card['additionalSourceMaterials'] = [source(r['paperPages'])]
    elif number == 2:
        if ref != 'C2(a)':
            card['stem'] += ' ' + records['C2(a)']['questionText']
        if ref.startswith('C2(c)') or ref == 'C2(d)':
            parent = records[ref]['sourceSchemeBlock']
            # Parent introduction comes from the paper, selected separately below.
            paper = fitz.open(next(s['path'] for s in manifest['sources'] if s['kind'] == 'paper'))
            text = paper[21].get_text(sort=True)
            intro = tidy(text.split('(c)', 1)[1].split('(i)', 1)[0])
            card['stem'] += ' ' + intro
    elif number == 6 and ref != 'C6(a)(i)':
        card['stem'] += ' ' + records['C6(a)(i)']['questionText']
    cards.append(card)


split_proof = []
def apply_split(ref, selected, allocations, new_rows, scopes, requires_third=False):
    index = next(i for i, c in enumerate(cards) if c['id'] == records[ref]['id'])
    original = cards[index]; text = original['questionText']; parts = []
    for n in range(2):
        c = deepcopy(original); c.update(questionText=selected[n], totalMarks=allocations[n], rows=new_rows[n])
        c['stem'] += ' ' + text
        c['questionRef'] = c['questionRef'].removesuffix(' — Deferred sitting') + ' — ' + scopes[n] + ' — Deferred sitting'
        if n:
            c['id'] += '-2'; c['conceptId'] += '-second-ask'
        parts.append(c)
    cards[index:index + 1] = parts
    split_proof.append(dict(ref=ref, originalPrompt=text, selectedPrompts=selected, marks=allocations,
                            fullOriginalRetainedBeforeReveal=True, thirdReaderRequired=requires_third))


def at(ref, boundary):
    text = records[ref]['questionText']; pos = text.index(boundary)
    return [text[:pos].strip(), text[pos:].strip()]


ref = 'B3(i)'; text = records[ref]['questionText']
assert text == 'Describe one positive and one negative effect for an enterprise moving to selling online.'
tail = ' effect for an enterprise moving to selling online.'
apply_split(ref, ['Describe one positive' + tail, 'Describe one negative' + tail], [2, 2],
    [[criterion('positive', label(ref), 1, [0, 1, 2], guide(ref, 'Proposed positive-effect card, with all seven positive models. The six negative models are shown for source context only. Third-reader validation required.'))],
     [criterion('negative', label(ref), 1, [0, 1, 2], guide(ref, 'Proposed negative-effect card, with all six negative models. The seven positive models are shown for source context only. Third-reader validation required.'))]],
    ['positive effect', 'negative effect'], True)
apply_split('C4(c)', at('C4(c)', 'Explain in detail'), [3, 5],
    [[criterion('sources', label('C4(c)'), 3, [0, 1], guide('C4(c)', 'Three different named sources, one mark each; keep all nine printed names.'))],
     component_rows(NOTICE, [tidy(records['C4(c)']['sourceSchemeBlock'])], [[2, 2, 1]], 'One developed point about one of the same stated sources; the scheme prints no developed example.')],
    ['sources', 'developed support'])
apply_split('C4(d)', at('C4(d)', 'Outline how'), [6, 3],
    [[criterion('challenges', label('C4(d)'), 3, [0, 1, 2], guide('C4(d)', 'The scheme labels this (i), three challenges at two marks each.'))],
     [criterion('solutions', 'Outline how these challenges might be overcome.', 3, [0, 1], guide('C4(d)', 'The scheme labels this (ii), one solution for each of the same three challenges.'))]],
    ['challenges', 'solutions'])
for c in cards:
    for row in c['rows']:
        if row['verbatim'] == NOTICE:
            row['unprinted'] = True
    assert sum(r['marks'] for r in c['rows']) == c['totalMarks'], c['id']
assert len(cards) == len({c['id'] for c in cards}) == 47
assert sum(c['totalMarks'] for c in cards) == 230
assert len([c for c in cards if len(c['rows']) == 1 and c['rows'][0].get('unprinted')]) == 5
output = HERE / 'proposed-47-authored-cards.json'
output.write_text(json.dumps(cards, ensure_ascii=False, indent=2) + '\n')
(HERE / 'split-source-selections.json').write_text(json.dumps(split_proof, ensure_ascii=False, indent=2) + '\n')
proof = dict(recordedAt=datetime.now(timezone.utc).isoformat(), status='Review-only; not applied or independently reviewed',
             cards=47, sourceParts=44, offeredMarks=230, examMaximum=130, wholeNoAnswerNotices=5,
             partialNoAnswerNotices=7, payloadSha256=hashlib.sha256(output.read_bytes()).hexdigest(),
             outstanding=['Second-reader candidate/source inspection', 'Four split differences, one informed split and twelve headings need third reading',
                          'Question/answer source tracing', 'Official deferred recording search: no URL or unpublished assertion invented',
                          'Fresh R4 archive checks', 'Canonical filings, Atlas/source bindings and application checks'])
(HERE / 'candidate-proof.json').write_text(json.dumps(proof, indent=2) + '\n')
print(json.dumps(proof, indent=2))
