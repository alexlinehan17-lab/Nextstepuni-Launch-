#!/usr/bin/env python3
"""Build only visually reviewed Accounting tasks; inventory never implies completion.

python3 scripts/markbank/accounting/build.py --inventory
python3 scripts/markbank/accounting/build.py --build
python3 scripts/markbank/accounting/build.py --finalize  # after runtime/UI checks

The reviewed manifests are independent, manually checked paper/scheme boundaries.
Every prompt fragment must occur on its cited paper page and every source is
hash-pinned. The same task supplies Mark Bank and the exact Topic Atlas sidecar.
"""
import argparse
import hashlib
import json
import re
import unicodedata
from pathlib import Path
import fitz

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
SELECTION_RX = re.compile(
    r'\b(?:choos\w*|choice|select\w*|either|or|any|one\s+of|'
    r'(?:answer|explain|describe|outline|state|give|name|list|identify|discuss)\b.*\b(?:one|two|three|four|five|six|[1-6]))\b',
    re.I,
)
IRISH_SELECTION_RX = re.compile(
    r'\b(?:rogh\w*|nó|ceachtar|ar bith|aon|amháin|dhá|dá|trí|ceithre|cúig|sé|'
    r'(?:tabhair|luaigh|mínigh|liostaigh|ainmnigh|roghnaigh)\b.*\b[1-6])\b',
    re.I,
)


def selection_directives(document, lang='ev'):
    """Broad raw-source candidates, including standalone OR and choosing.

    False positives must be classified by the reviewer; overlooking a choice
    is worse than explicitly recording a conjunction or copyright sentence.
    """
    expression = IRISH_SELECTION_RX if lang == 'iv' else SELECTION_RX
    return [dict(page=page.number + 1, text=line.strip())
            for page in document for line in page.get_text().splitlines()
            if expression.search(unicodedata.normalize('NFKC', line))]


def read(path):
    return json.loads(path.read_text())


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def text_key(text):
    text = unicodedata.normalize('NFKC', text).replace('Ɵ', 'ti').replace('Ʃ', 'tt')
    return re.sub(r'[^a-z0-9€%]', '', text.lower())


def inventory():
    records = []
    for paper in sorted((ROOT / 'paper-trail-corpus/exampapers').glob('*/LC032*.pdf')):
        year, fileid = int(paper.parent.name), paper.name
        if year < 2010:  # reviewed window: the shared corpus also holds the 1995-2009 archive (#256)
            continue
        scheme = ROOT / 'paper-trail-corpus/markingschemes' / str(year) / fileid
        sidecar = ROOT / 'scripts/paper-trail/answers' / str(year) / (fileid + '.json')
        doc = fitz.open(paper)
        records.append(dict(year=year, fileid=fileid, level='higher' if fileid[5] == 'A' else 'ordinary',
                            lang=fileid[-6:-4].lower(), paperPages=len(doc), paperSha256=sha(paper),
                            schemePages=len(fitz.open(scheme)) if scheme.exists() else None,
                            schemeSha256=sha(scheme) if scheme.exists() else None,
                            sidecarQuestions=[q['n'] for q in read(sidecar)['q']] if sidecar.exists() else [],
                            reviewStatus='pending'))
    write(HERE / 'inventory.json', dict(subjectId='accounting', complete=False, papers=records))
    print(f'Inventoried {len(records)} paper editions. This is NOT a completeness audit.')


def validate_region(region, page_count):
    assert isinstance(region['p'], int) and 1 <= region['p'] <= page_count, region
    assert region.get('rotate', 0) in (0, 90, 180, 270), region
    x0, y0, x1, y1 = region['r']
    assert 0 <= x0 < x1 <= 1 and 0 <= y0 < y1 <= 1, region


def expand_tasks(tasks, scheme, paper):
    """Check every reviewer-pinned printed choice; a choice stays ONE task.

    A printed choice is one card, never one per option or combination
    (AGENTS.md, 2026-10-12): the printed question with its whole pool, the
    scheme's own tariff, and the printed "any N" instruction.
    """
    for task in tasks:
        assert 'selectionPool' not in task, f'{task["key"]}: retired route expansion; declare printedChoice'
        pool = task.get('printedChoice')
        if not pool:
            continue
        options, choose = pool['options'], pool['choose']
        assert 1 <= choose < len(options)
        assert len({o['key'] for o in options}) == len(options)
        assert any(text_key(pool['instruction']) in text_key(paper[f['page'] - 1].get_text())
                   for f in task['promptFragments']), f'{task["key"]}: unprinted choice instruction'
        for option in options:
            source_text = scheme[option['schemePage'] - 1].get_text()
            # Some SEC PDFs have damaged text encodings. A visually transcribed
            # label may pin the original glyph sequence as well as the PDF hash.
            if 'schemeSourceText' in option:
                assert option['schemeSourceText'].strip() and option['schemeSourceText'] in source_text, option
            else:
                assert text_key(option['label']) in text_key(source_text), option
    return tasks


def validate_correspondences(cards):
    """Validate separately reviewed translated editions, without duplicating tasks.

    Atlas intentionally collapses translations of a logical question. A
    correspondence may only claim the existing English task after the Irish
    paper and available scheme have been inspected; differing source wording
    and scheme pagination stay in the review record. A missing translated
    scheme may use the already reviewed English scheme only when that fallback
    is explicit and the translated paper has been compared task by task.
    """
    reviewed = []
    for path in sorted((HERE / 'correspondence').glob('*.json')):
        review = read(path)
        year, fileid = review['year'], review['fileid']
        english_path = HERE / 'reviewed' / review['englishReview']
        assert sha(english_path) == review['englishReviewSha256'], f'{path}: English review changed'
        english = read(english_path)
        assert english['year'] == year and english['level'] == review['level']
        assert fileid == english['fileid'].replace('EV.pdf', 'IV.pdf')
        paper = ROOT / 'paper-trail-corpus/exampapers' / str(year) / fileid
        scheme = ROOT / 'paper-trail-corpus/markingschemes' / str(year) / fileid
        assert sha(paper) == review['paperSha256'], f'{path}: paper changed'
        if 'schemeFallback' in review:
            fallback = review['schemeFallback']
            assert not scheme.exists(), f'{path}: translated scheme is now available; review it'
            assert fallback['fileid'] == english['fileid']
            assert fallback['reason'] and fallback['paperComparison']
            assert review['visualSchemePages'] == [], f'{path}: missing scheme cannot be visually reviewed'
            scheme = scheme.with_name(fallback['fileid'])
            assert fallback['visualSchemePages'] == english['visualSchemePages']
            assert fallback['schemeSha256'] == english['schemeSha256']
        assert sha(scheme) == review['schemeSha256'], f'{path}: scheme changed'
        pd, sd = fitz.open(paper), fitz.open(scheme)
        assert review['visualPaperPages'] == list(range(1, len(pd) + 1))
        inspected_scheme_pages = review.get('schemeFallback', review)['visualSchemePages']
        assert inspected_scheme_pages == list(range(1, len(sd) + 1))
        assert selection_directives(pd, 'iv') == [
            dict(page=d['page'], text=d['text']) for d in review['selectionReview']
        ], f'{path}: unclassified or stale Irish selection directive'
        assert all(d['classification'] in ('paper-level-choice', 'open-response', 'not-a-selection', 'closed-pool')
                   and d['reason'] for d in review['selectionReview'])
        closed_pool_keys = {t['key'] for t in english['tasks'] if t.get('printedChoice')}
        assert all(d.get('englishTaskKey') in closed_pool_keys
                   for d in review['selectionReview'] if d['classification'] == 'closed-pool'), \
            f'{path}: translated closed pool has no authored English expansion'
        assert {q['questionNumber'] for q in review['questionReview']} == set(range(1, 10))
        assert all(q['note'] for q in review['questionReview'])
        expected = {c['taskKey']: c for c in cards
                    if c['year'] == year and c['paperFileid'] == english['fileid']}
        correspondences = review['taskCorrespondence']
        assert len(correspondences) == len(expected)
        assert {t['englishTaskKey'] for t in correspondences} == set(expected)
        for task in correspondences:
            assert task['marks'] == expected[task['englishTaskKey']]['totalMarks']
            assert task['paperPages'] == sorted(set(task['paperPages']))
            assert all(1 <= p <= len(pd) for p in task['paperPages'])
            assert task['schemeRegions']
            for region in task['schemeRegions']:
                validate_region(region, len(sd))
        # A distinct task requires its own full authored review; it must never
        # disappear behind a translation-equivalence assertion.
        assert review['uniqueAdditionalTasks'] == [], f'{path}: additional tasks need authoring'
        assert review['decision']
        reviewed.append(f'accounting|{year}|{fileid}')
    return reviewed


def build(finalize=False):
    cards, mapping_rows, reviewed_papers = [], [], []
    for path in sorted((HERE / 'reviewed').glob('*.json')):
        review = read(path)
        year, level, fileid = review['year'], review['level'], review['fileid']
        paper = ROOT / 'paper-trail-corpus/exampapers' / str(year) / fileid
        scheme = ROOT / 'paper-trail-corpus/markingschemes' / str(year) / fileid
        assert sha(paper) == review['paperSha256'], f'{path}: paper changed'
        assert sha(scheme) == review['schemeSha256'], f'{path}: scheme changed'
        pd, sd = fitz.open(paper), fitz.open(scheme)
        assert review['visualPaperPages'] == list(range(1, len(pd) + 1)), f'{path}: paper sweep incomplete'
        assert review['visualSchemePages'] == list(range(1, len(sd) + 1)), f'{path}: scheme sweep incomplete'
        # Classify selections against RAW source wording, not generated cards.
        directives = selection_directives(pd)
        assert directives == [dict(page=d['page'], text=d['text']) for d in review['selectionReview']], f'{path}: unclassified or stale selection directive'
        assert all(d['classification'] and d['reason'] for d in review['selectionReview'])
        pooled_keys = {t['key'] for t in review['tasks'] if t.get('printedChoice')}
        classified_keys = {d['taskKey'] for d in review['selectionReview']
                           if d['classification'] == 'finite-pool-one-card'}
        assert pooled_keys == classified_keys, f'{path}: unclassified or orphaned finite pool'
        sidecar_path = ROOT / 'scripts/paper-trail/answers' / str(year) / (fileid + '.json')
        sidecar = read(sidecar_path)
        # Preserve original identities and anchors. Corrections are additive.
        for q in sidecar['q']:
            correction = review.get('legacyCorrections', {}).get(q['n'])
            if correction:
                q.update(correction)
        legacy = {q['n'] for q in sidecar['q']}
        tasks = expand_tasks(review['tasks'], sd, pd)
        assert len(tasks) == review['expectedTaskCount']
        assert sum(t['marks'] for t in tasks) == review['allRouteMarks']
        assert {t['questionNumber'] for t in tasks} == set(range(1, 10))
        for task in tasks:
            for fragment in task['promptFragments']:
                assert text_key(fragment['text']) in text_key(pd[fragment['page'] - 1].get_text()), f'{path} {task["key"]}: prompt not in paper: {fragment}'
            for region in task['schemeRegions']:
                validate_region(region, len(sd))
            solution_regions = task['schemeRegions'] + [
                dict(p=p, r=[0, 0, 1, 1]) for p in review.get('markingGuidePages', [])
            ]
            for region in solution_regions:
                validate_region(region, len(sd))
            pages = task['paperPages']
            assert pages == sorted(set(pages)) and all(1 <= p <= len(pd) for p in pages)
            assert task['boundaryReason'] and task['allocationEvidence']
            ident = f'acc-{year}-{"hl" if level == "higher" else "ol"}-q{task["key"]}'
            prompt = '\n'.join(fragment['text'] for fragment in task['promptFragments'])
            card = dict(id=ident, year=year, level=level, paperFileid=fileid,
                        questionNumber=task['questionNumber'], taskKey=task['key'],
                        title=task['title'], questionText=prompt, totalMarks=task['marks'],
                        topicId=task['topicId'], examTopicIds=task['examTopicIds'],
                        paperPages=pages, schemeRegions=solution_regions,
                        taskFocus=task.get('focus'), allocationNote=task['allocationEvidence'],
                        reviewedAt=review['reviewedAt'])
            cards.append(card)
            mapping_rows.append(dict(level=level, year=year, fileid=fileid,
                                     n=task['key'], topicIds=task['examTopicIds']))
            if task['key'] not in legacy:
                sidecar['q'].append(dict(n=task['key'], label=f'Question {task["key"]} · {task["title"]}',
                    pP=pages[0], pY=[0, 1], paperRegion=[dict(p=p, r=[0, 0, 1, 1]) for p in pages],
                    region=solution_regions, mode='crop', conf=1,
                    practiceTask=dict(prompt=prompt, focus=task.get('focus'), marks=task['marks'])))
            else:
                # An unsplit task (e.g. a complete tabular statement) retains n.
                q = next(q for q in sidecar['q'] if q['n'] == task['key'])
                q['paperRegion'] = [dict(p=p, r=[0, 0, 1, 1]) for p in pages]
                q['schemeRegion'] = solution_regions
                q['practiceTask'] = dict(prompt=prompt, focus=task.get('focus'), marks=task['marks'])
        sidecar['maxCropPages'] = max(
            [len(t['paperPages']) for t in tasks]
            + [len(q.get('paperRegion', [])) for q in sidecar['q']]
        )
        write(ROOT / 'public/paper-answers' / str(year) / (fileid + '.json'), sidecar)
        reviewed_papers.append(f'accounting|{year}|{fileid}')
        # Local provenance text for the existing whole-deck guards.
        scheme_md = ROOT / 'examiner-reports/accounting/schemes' / f'{year}-{"hl" if level == "higher" else "ol"}.md'
        scheme_md.parent.mkdir(parents=True, exist_ok=True)
        scheme_md.write_text('\n'.join(f'\n## PDF page {p.number+1}\n'+p.get_text() for p in sd))
    assert len({c['id'] for c in cards}) == len(cards)
    write(ROOT / 'components/MarkBank/cards/accounting/authored.json', dict(complete=False, cards=cards))
    write(ROOT / 'data/examTopics/accounting-task-runtime.json', dict(reviewedPapers=reviewed_papers, tasks=mapping_rows))
    correspondence_papers = validate_correspondences(cards)
    source_inventory = read(HERE / 'inventory.json')
    reviewed_keys = set(reviewed_papers)
    correspondence_keys = set(correspondence_papers)
    progress = []
    for item in source_inventory['papers']:
        reviewed = f'accounting|{item["year"]}|{item["fileid"]}' in reviewed_keys
        progress.append(dict(year=item['year'], level=item['level'], fileid=item['fileid'],
                             status='tasks-reviewed' if reviewed else
                             'correspondence-reviewed' if f'accounting|{item["year"]}|{item["fileid"]}' in correspondence_keys
                             else 'pending',
                             tasks=sum(c['year'] == item['year'] and c['paperFileid'] == item['fileid'] for c in cards)))
    write(HERE / 'progress.json', dict(
        complete=False,
        note='Progress only. Counts do not establish full-corpus completeness. Remaining edition correspondence and final zero-open/zero-orphan reconciliation must pass.',
        sourceEditions=len(progress), reviewedEditions=len(reviewed_papers),
        correspondenceReviewedEditions=len(correspondence_papers),
        reviewedTasks=len(cards), editions=progress,
    ))
    sizes = read(ROOT / 'components/MarkBank/cards/sizes.json')
    sizes['accounting'] = {level: sum(c['level'] == level for c in cards) for level in ['higher', 'ordinary']}
    (ROOT / 'components/MarkBank/cards/sizes.json').write_text(json.dumps(sizes, indent=1) + '\n')
    if finalize:
        # Explicit finalization follows the runtime, preservation and browser
        # checks recorded in verification.json. Ordinary builds stay cautious.
        from reconcile import reconcile
        reconciliation = reconcile()
        verification = read(HERE / 'verification.json')
        assert verification['accountingChecksPassed'], 'Runtime/UI verification is not complete'
        assert verification['cardIdsSha256'] == hashlib.sha256(
            '\n'.join(sorted(c['id'] for c in cards)).encode()).hexdigest()
        assert verification['cardDataSha256'] == hashlib.sha256(
            json.dumps(cards, ensure_ascii=False, sort_keys=True).encode()).hexdigest()
        assert verification['verifiedFiles'] and all(
            sha(ROOT / name) == digest for name, digest in verification['verifiedFiles'].items()
        ), 'Verified implementation or audit inputs changed; repeat the affected checks'
        assert not reconciliation['openIssues']
        assert len(reviewed_keys | correspondence_keys) == len(source_inventory['papers'])
        write(ROOT / 'components/MarkBank/cards/accounting/authored.json', dict(complete=True, cards=cards))
        progress_report = read(HERE / 'progress.json')
        progress_report.update(complete=True, note='All local paper editions visually reviewed; source reconciliation, runtime Atlas parity, preservation and Accounting UI checks passed. See reconciliation.json and verification.json, including the two explicit 2020 Irish scheme fallbacks.')
        write(HERE / 'progress.json', progress_report)
        print(f'Finalized {len(cards)} Accounting tasks with zero open source/runtime issues.')
    else:
        print(f'Built {len(cards)} reviewed tasks from {len(reviewed_papers)} papers. Final verification is recorded separately.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--inventory', action='store_true')
    parser.add_argument('--build', action='store_true')
    parser.add_argument('--finalize', action='store_true')
    args = parser.parse_args()
    if args.inventory:
        inventory()
    if args.build or args.finalize:
        build(finalize=args.finalize)
