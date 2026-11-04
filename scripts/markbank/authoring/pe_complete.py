#!/usr/bin/env python3
"""Build PE cards from independently reviewed paper/scheme task inventories.

Run without --write to audit. Every sitting has an independent visual task
inventory, source-bound selection review and published allocation checks.
--write emits the deck, level modules, Atlas index and paper-review manifest.
The separate raw-paper reconciliation remains an additional coverage check.
"""
import argparse
import collections
import hashlib
import json
import re
import subprocess
from pathlib import Path
import fitz

import pe_review_2020 as review2020
import pe_review_2021_hl as review2021hl
import pe_review_2021_ol as review2021ol
import pe_review_2022_hl as review2022hl
import pe_review_2022_ol as review2022ol
import pe_review_2023_hl as review2023hl
import pe_review_2023_ol as review2023ol
import pe_review_2024_hl as review2024hl
import pe_review_2024_ol as review2024ol
import pe_review_2025_hl as review2025hl
import pe_review_2025_ol as review2025ol
import pe_review_2026_hl as review2026hl
import pe_review_2026_ol as review2026ol

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / 'components/MarkBank/cards/physical-education/reviewed.json'
AUDIT = ROOT / 'scripts/markbank/authored/physical-education-reviewed-audit.json'
ATLAS = ROOT / 'data/paperTrail/physicalEducationTasks.json'
REVIEWS = [(2020, 'hl', review2020), (2021, 'hl', review2021hl), (2021, 'ol', review2021ol), (2022, 'hl', review2022hl), (2022, 'ol', review2022ol), (2023, 'hl', review2023hl), (2023, 'ol', review2023ol), (2024, 'hl', review2024hl), (2024, 'ol', review2024ol), (2025, 'hl', review2025hl), (2025, 'ol', review2025ol), (2026, 'hl', review2026hl), (2026, 'ol', review2026ol)]


def ref(part):
    m = re.fullmatch(r'(\d+)([a-z])?(i{1,3}|iv|v|vi{0,3}|ix|x)?', part)
    assert m, part
    return 'Q' + m[1] + ''.join(f'({x})' for x in m.groups()[1:] if x)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def tokens(text):
    return re.findall(r'[a-z0-9]+', text.casefold().replace('’', "'"))


def unprinted_segments(text, pages):
    """Segments of a lifted question whose words are not printed, in order, on its pages.

    A segment is a line, a list item or a clause before a colon. Layout (bullets,
    columns, case) may differ from the paper; a word may not.
    """
    hay = ' ' + ' '.join(tokens(' '.join(pages))) + ' '
    segments = [segment for segment in re.split(r'\n|;|:\s', text) if tokens(segment)]
    return [segment for segment in segments if ' ' + ' '.join(tokens(segment)) + ' ' not in hay]


def build():
    entries = json.loads(subprocess.check_output([
        'node', '--input-type=module', '-e',
        'import {paperIndex} from "./scripts/markbank/paperIndex.mjs"; console.log(JSON.stringify(paperIndex["physical-education"]))',
    ], cwd=ROOT))
    # Reviewed window only: June sittings (the deferred sitting reuses year and level).
    entries = [e for e in entries if not e.get('sitting') and e['year'] >= 2010]
    cards, papers, atlas = [], [], []
    crosswalk = json.loads((ROOT / 'data/examTopics/physical-education-curriculum-crosswalk.json').read_text())
    legacy = json.loads((ROOT / 'scripts/markbank/authored/physical-education.json').read_text())
    previous = {card['id']:card for card in legacy}
    for year, short, review in REVIEWS:
        level = 'higher' if short == 'hl' else 'ordinary'
        entry, = [e for e in entries if e['year'] == year and e['level'] == level and e['lang'] == 'ev']
        item, = entry['papers']
        fileid, schemeid = item['doc']['f'], item['scheme']['f']
        paper_path = ROOT / f'examiner-reports/physical-education/papers/{year}-{short}-paper.pdf'
        scheme_path = ROOT / f'examiner-reports/physical-education/schemes/{year}-{short}.pdf'
        anchor_map = json.loads((ROOT / f'scripts/paper-trail/answers/{year}/{fileid}.json').read_text())
        parent_anchors = {q['n'] for q in anchor_map['q']}
        totals = collections.Counter()
        paper_cards = []
        # Scan the raw PDF, not the task list. A newly appearing directive must
        # be classified; a stale manual classification must also fail.
        selection_scan = []
        pool_scan = []
        pattern = r'\b(?:choose|select|either|or|one of|any (?:one|two|three|four|five|\d+)|at least two of|different group|and/or|named physical activity)\b'
        pool_pattern = r'\b(?:(?:one|two|three|four|five|six|\d+) of|from the list|(?:from|of) (?:the )?following|any ten)\b'
        with fitz.open(paper_path) as doc:
            assert len(doc) == review.PAPER_PAGE_COUNT
            raw_pages = {}
            for page_index, page in enumerate(doc):
                raw = ' '.join(page.get_text().split())
                raw_pages[page_index+1] = raw.casefold()
                for match in re.finditer(pattern,raw,re.I):
                    selection_scan.append([page_index+1,match[0].lower()])
                for match in re.finditer(pool_pattern,raw,re.I):
                    pool_scan.append([page_index+1,match[0].lower()])
        with fitz.open(scheme_path) as doc:
            assert len(doc) == review.SCHEME_PAGE_COUNT
        assert selection_scan == review.EXPECTED_SELECTION_SCAN, ('unclassified/stale selection',selection_scan)
        assert pool_scan == review.EXPECTED_POOL_SCAN, ('unclassified/stale pool wording',year,short,pool_scan)
        # A printed choice is ONE card (AGENTS.md): never one per option or pair.
        assert set(review.CHOICES) == set(review.SOURCE_POOLS)
        assert set(review.CHOICES) <= {task[0] for task in review.TASKS}
        for part, anchors in review.SOURCE_POOLS.items():
            for page, anchor in anchors:
                assert anchor.casefold() in raw_pages[page], ('stale printed pool',year,short,part,page,anchor)
        for part, topic, paper_pages, scheme_pages, prompt, allocations in review.TASKS:
            number = int(re.match(r'\d+', part)[0])
            assert str(number) in parent_anchors, ('missing full-paper anchor',year,short,part)
            part_ref = getattr(review,'PART_REF_OVERRIDES',{}).get(part) or ref(part)
            total = sum(allocation[1] for allocation in allocations)
            totals[number] += total
            criteria = []
            for i, allocation in enumerate(allocations):
                label, maximum, guidance, *scores = allocation
                criteria.append(dict(id=f'c{i+1}', label=label, maxMarks=maximum,
                                     guidance=[guidance], permittedMarks=scores[0] if scores else list(range(maximum+1))))
            choice = review.CHOICES.get(part)
            requirements = []
            if choice:
                printed = [raw_pages[page] for page in paper_pages]
                assert 1 <= choice['choose'] < len(choice['pool']), (year,short,part)
                if choice.get('poolPrinted', True):
                    for label in choice['pool']:
                        assert ' '.join(tokens(label)) in ' '.join(tokens(' '.join(printed))), ('unprinted pool item',year,short,part,label)
                assert not unprinted_segments(prompt, printed), ('question not as printed',year,short,part,unprinted_segments(prompt, printed))
                if choice.get('stemPrinted'):
                    # A leading "Question 15(c)(i):" names the printed predecessor; the rest is lifted.
                    lead_in = re.sub(r'^Question [0-9a-z()]+: ', '', review.CONTEXT[part])
                    assert not unprinted_segments(lead_in, printed), ('lead-in not as printed',year,short,part,unprinted_segments(lead_in, printed))
                if choice['choose'] > 1:
                    assert not unprinted_segments(choice['instruction'], printed), ('instruction not as printed',year,short,part)
                    requirements = [choice['instruction']]
                    if choice.get('slots'):
                        # One criterion per chosen item, at the scheme's per-item tariff.
                        assert len(choice['slots']) == choice['choose'] == len(criteria), (year,short,part)
                        assert len({criterion['maxMarks'] for criterion in criteria}) == 1, (year,short,part)
                        for criterion, label in zip(criteria, choice['slots']):
                            criterion['label'] = label
                    else:
                        # The scheme's own structure: a holistic grid, or fixed role slots.
                        assert choice.get('holistic') or len(criteria) > choice['choose'], (year,short,part)
            ident = getattr(review,'CARD_ID_OVERRIDES',{}).get(part,f'pe-{year}-{short}-q{part}')
            question_ref = f'{year} {short.upper()} {part_ref}'
            question_text = prompt
            source = dict(kind='exam-material', label=f'{part_ref} · original paper',
                          title=f'{year} Physical Education · {short.upper()} · {part_ref}',
                          pages=paper_pages, attribution=f'© State Examinations Commission. Third-party sources are acknowledged on paper page {review.ACKNOWLEDGEMENT_PAGE}.',
                          presentationNote='The original examination pages, including all printed text, figures and tables.')
            scheme = dict(kind='marking-scheme', label=f'{part_ref} · published marking guide',
                          title=f'{question_ref} · marking scheme', pages=scheme_pages, sourceFileid=schemeid,
                          attribution='© State Examinations Commission.',
                          presentationNote='The original SEC marking scheme. Read the allocation for this part; examples are not exhaustive.')
            rotations = {p:r for p,r in review.PAGE_ROTATIONS.items() if p in paper_pages}
            if rotations:
                source['pageRotations'] = rotations
            card = dict(id=ident, source='sec', kind='rubric', subjectId='physical-education',
                        level=level, year=year, topicId='physical-education-'+topic,
                        conceptId=previous.get(ident,{}).get('conceptId') or f'pe-{topic}-'+hashlib.sha256((question_text+' '+review.CONTEXT.get(part,'')).encode()).hexdigest()[:12],
                        paperFileid=fileid.removesuffix('.pdf'),
                        section='A' if number<review.CASE_STUDY_QUESTION else 'B' if number==review.CASE_STUDY_QUESTION else 'C',
                        questionRef=question_ref, questionText=question_text, totalMarks=total,
                        sourceMaterial=source, stem=review.CONTEXT.get(part,''),
                        schemeCitation=f'SEC Physical Education {year} {short.upper()}, {part_ref}, PDF pages '+', '.join(map(str,scheme_pages))+' — © State Examinations Commission.',
                        specVersion='physical-education:outgoing',
                        qa=dict(gates=['visual-paper-sweep','visual-scheme-allocation','printed-choice-review','source-pages','canonical-topic'],humanReviewedBy='agent-visual-review',humanReviewedAt='2026-10-07'),
                        rubric=dict(system='physical-education',taskRequirements=requirements,criteria=criteria,
                                    schemeMaterial=scheme,
                                    markingGuideNote='Apply the allocation to the complete response. The SEC’s suggestions and examples are not exhaustive; other valid answers may earn credit.'))
            cards.append(card)
            atlas_topics = [topic_id for topic_id, canonical in crosswalk.items()
                            if topic_id.startswith(f'physical-education-{level}-')
                            and '-new-course-' not in topic_id and card['topicId'] in canonical]
            override = getattr(review,'ATLAS_TOPIC_OVERRIDES',{}).get(part)
            if override:
                assert override in crosswalk, override
                atlas_topics = [override]
            elif len(atlas_topics) > 1:
                # The existing crosswalk overlaps fitness assessment with
                # fitness planning. These tasks assess demands, not plans.
                assert topic in ('0-5','0-6','0-7','0-8','0-9'), (part,atlas_topics)
                atlas_topics = [f'physical-education-{level}-2-physical-demands-of-performance']
            assert len(atlas_topics)==1, (year,short,part,atlas_topics)
            # A task that genuinely examines a second specification topic
            # (decided from the paper, scheme and NCCA wording) is also
            # filed there. The primary topic stays first.
            for extra in getattr(review,'ATLAS_TOPIC_ADDITIONS',{}).get(part,()):
                assert extra in crosswalk and extra.startswith(f'physical-education-{level}-') \
                    and extra not in atlas_topics, (year,short,part,extra)
                atlas_topics.append(extra)
            task_n = part_ref[1:]
            atlas.append(dict(cardId=ident,subjectId='physical-education',level=level,lang='ev',year=year,
                              fileid=fileid,paperKey='single',n=task_n,parentQuestion=str(number),
                              canonicalTopicId=card['topicId'],specificationId=card['specVersion'],
                              examTopicIds=atlas_topics,paperPages=paper_pages,schemePages=scheme_pages,
                              pageRotations=rotations,questionRef=question_ref,totalMarks=total))
            paper_cards.append(dict(cardId=ident, part=part, topicId=card['topicId'], totalMarks=total,
                                    paperPages=paper_pages,schemePages=scheme_pages,
                                    choice=dict(choose=choice['choose'],pool=choice['pool'],instruction=choice.get('instruction')) if choice else None))
        assert dict(totals) == review.EXPECTED_QUESTION_TOTALS, (totals,review.EXPECTED_QUESTION_TOTALS)
        previous_ids = {c['id'] for c in legacy if c['year']==year and c['level']==level}
        generated_ids = {c['cardId'] for c in paper_cards}
        assert previous_ids <= generated_ids, previous_ids-generated_ids
        papers.append(dict(year=year,level=level,lang='ev',paperFileid=fileid,schemeFileid=schemeid,
                           paperSha256=digest(paper_path),schemeSha256=digest(scheme_path),
                           reviewedPaperPages=list(range(1,review.PAPER_PAGE_COUNT+1)),reviewedSchemePages=list(range(1,review.SCHEME_PAGE_COUNT+1)),
                           taskCount=len(review.TASKS),cardCount=len(paper_cards),questionTotals=dict(totals),
                           retainedLegacyIds=sorted(previous_ids),idCorrections=getattr(review,'ID_CORRECTIONS',[]),selectionScan=selection_scan,poolScan=pool_scan,selectionReview=review.SELECTION_REVIEW,cards=paper_cards))
    corpus = {(e['year'], e['level']) for e in entries if e['lang'] == 'ev'}
    assert {(p['year'], p['level']) for p in papers} == corpus, 'unreviewed corpus sitting'
    assert set(previous) <= {c['id'] for c in cards}, 'lost legacy identity'
    assert len(cards) == len({c['id'] for c in cards})
    for c in cards:
        assert c['sourceMaterial']['pages']==sorted(set(c['sourceMaterial']['pages']))
        for criterion in c['rubric']['criteria']:
            assert min(criterion['permittedMarks'])==0 and max(criterion['permittedMarks'])==criterion['maxMarks']
    return dict(schemaVersion=1,cards=cards), dict(schemaVersion=1,status='complete',
                  reviewedTaskCount=sum(p['taskCount'] for p in papers),cardCount=len(cards),
                  retainedLegacyCardCount=len(previous),
                  corpusPaperCount=len([e for e in entries if e['lang']=='ev']),reviewedPapers=papers), atlas


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write',action='store_true')
    args=parser.parse_args()
    data,audit,atlas=build()
    if args.write:
        OUT.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
        AUDIT.write_text(json.dumps(audit,ensure_ascii=False,indent=2)+'\n')
        ATLAS.write_text(json.dumps(atlas,ensure_ascii=False,separators=(',',':'))+'\n')
        sizes_path=ROOT/'components/MarkBank/cards/sizes.json'
        sizes=json.loads(sizes_path.read_text())
        for level in ('higher','ordinary'):
            (OUT.parent/f'{level}.ts').write_text(
                '/** @license SPDX-License-Identifier: Apache-2.0 */\n'
                '// Generated by scripts/markbank/authoring/pe_complete.py.\n'
                "import { REVIEWED_CARDS } from './factory';\n"
                f"export const CARDS = REVIEWED_CARDS.filter(card => card.level === '{level}');\n")
        sizes['physical-education']={level:sum(c['level']==level for c in data['cards']) for level in ('higher','ordinary')}
        sizes_path.write_text(json.dumps(sizes,indent=1)+'\n')
    print(f"Reviewed {len(audit['reviewedPapers'])}/{audit['corpusPaperCount']} papers; {len(data['cards'])} cards. All corpus sittings and legacy IDs are accounted for; run reconcile.py for the independent raw-paper check.")
