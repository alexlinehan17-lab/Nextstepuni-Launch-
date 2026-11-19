#!/usr/bin/env python3
"""Write the review ledgers for English's deferred sittings from one reviewed file per sitting.

Each deferred sitting (2022-2025) is reviewed in
scripts/markbank/authored/english-deferred-review/<year>-<hl|ol>.json: what was
seen on every page, each comprehension text's reader, each task's selection
decision and marking criteria, and the sitting's printed grid. This script binds
those decisions to the papers exactly as the June ledgers are bound (paper,
scheme and question hashes, task fingerprints), so english_publish.py publishes a
deferred paper only through the same per-paper gate as June's.

Two things are read off the scheme by this script and never typed:
- a task's criteria where the deferred scheme sets out its block: discrete when
  the block prints a P/C/L/M split (the split is taken from the print),
  combined otherwise; the review file's criteria must agree;
- where the deferred scheme sets out NO block for a task (it "will only have
  been finalised for the questions attempted by the candidates", page 2), the
  task is marked on the sitting's general criteria and grid, as the review file
  records with the pages that print them.

Raw selection directives are classified by where they are printed: inside a
task's printed region and part of its wording (the task), a standalone OR or a
rubric (exam instruction), a passage, poem or introduction (source prose), or a
copyright notice (non-selection). Anything else must be classified in the
review file, or the script refuses.

    python3 scripts/markbank/authoring/english_deferred_review.py 2025-hl
    python3 scripts/markbank/authoring/english_deferred_review.py --all --check
"""
from __future__ import annotations

import argparse
import hashlib
import importlib
import json
import re
import sys

import fitz

from english_complete import ROOT, inventory

AUTHORED = ROOT / 'scripts/markbank/authored'
REVIEWS = AUTHORED / 'english-deferred-review'
DEFERRED_NOTE = ('The deferred marking scheme prints no block for this task: its PDF2 note says a deferred scheme '
                 '"will only have been finalised for the questions attempted by the candidates".')

REASONS = {
    'tasks': ('Visually located inside this task’s printed region on the viewed page. Its own selection decision '
              'carries the analysis; the binding fails if the line, its context or the task wording changes.'),
    'exam-instruction': ('Visually verified rubric: the cover or section instruction, a choice rubric, an OR separating '
                         'numbered alternatives, or a composing rubric. Every alternative is its own reviewed task.'),
    'source-prose': ('A line of a printed passage, poem or introduction, visually verified; the matched word is '
                     'narrative, argument or poetry, not an answer-choice directive.'),
    'non-selection': ('Copyright, acknowledgement or authorised-use notice; not a candidate task or answer-route '
                      'selection.'),
}


def read(name):
    return json.loads((AUTHORED / name).read_text())


def write(name, value):
    (AUTHORED / name).write_text(json.dumps(value, ensure_ascii=False, indent=2 if name in INDENT2 else 1) + '\n')


# Each ledger keeps the indentation it was committed with.
INDENT2 = set()


def detect_indent():
    for name in ('english-visual-review.json', 'english-task-review.json', 'english-selection-review.json',
                 'english-raw-selection-review.json', 'english-source-review.json', 'english-marking-grids.json',
                 'english-printed-duplicates.json'):
        text = (AUTHORED / name).read_text()
        if text.startswith('{\n  "'):
            INDENT2.add(name)


def sha(path):
    return hashlib.sha256((ROOT / path).read_bytes()).hexdigest()


def fingerprint(text):
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


def records_for(key):
    year, level = key.split('-')
    return [r for r in inventory()['papers']
            if r.get('sitting') == 'deferred' and r['year'] == int(year) and r['level'] == {'hl': 'higher', 'ol': 'ordinary'}[level]]


def extract(records):
    import english_full_cards
    importlib.reload(english_full_cards)
    out = {}
    for record in records:
        parsed, tasks = english_full_cards.extract_record(record)
        out[record['id']] = (parsed, tasks)
    return out


def scheme_split(scheme, regions):
    """The P/C/L/M split printed in a task's scheme block, or None when it prints one combined mark."""
    import english_full_cards
    text = english_full_cards.region_text(scheme, regions)
    found = {}
    for letter in ('P', 'C', 'L', 'M'):
        m = re.search(rf'(?m)^\s*{letter}\s*:?\s*(\d{{1,2}})\s*$', text)
        if m:
            found[letter] = int(m.group(1))
    return found if len(found) == 4 else None


ORDINARY_KINDS = ((r'^p1-t\d-a-(?:i|ii)$', 'qa15'), (r'^p1-t\d-a-iii-', 'qa10'), (r'^p1-t\d-b', 'qb'),
                  (r'^p1-composing', 'composing'), (r'^p2-single-[a-i]-q1-', 'single-q1'),
                  (r'^p2-single-[a-i]-q[2-4]$', 'single-q'), (r'^p2-comparative-[a-c]-q[12]-a-', 'comparative-a'),
                  (r'^p2-comparative-[a-c]-q[12]-b$', 'comparative-b'), (r'^p2-unseen', 'unseen'),
                  (r'^p2-prescribed-[a-f]-q1-', 'prescribed-q1'), (r'^p2-prescribed-[a-f]-q2-', 'prescribed-q2'))


def task_kind(task):
    tid = task['id'].split('-deferred-')[1]
    if task['level'] == 'ordinary':
        for pattern, kind in ORDINARY_KINDS:
            if re.match(pattern, tid):
                return kind
        raise ValueError('Unclassified deferred Ordinary task: ' + task['id'])
    for pattern, kind in ((r'^p1-t\d-a-', 'qa'), (r'^p1-t\d-b', 'qb'), (r'^p1-composing', 'composing'),
                          (r'^p2-single', 'single'), (r'^p2-comparative-[a-c]-q1', 'comparative-q1'),
                          (r'^p2-comparative-[a-c]-q2', 'comparative-q2'), (r'^p2-unseen', 'unseen'),
                          (r'^p2-prescribed', 'prescribed')):
        if re.match(pattern, tid):
            return kind
    raise ValueError('Unclassified deferred task: ' + task['id'])


def apply(key, review, check):
    import english_choices
    from english_raw_selection import scan, suggested_tasks
    from english_task_review import task_fingerprint
    records = records_for(key)
    by_paper = {r['id']: r for r in records}
    changed = {}

    # 1. Grid for the sitting's own scheme.
    grids = read('english-marking-grids.json')
    sitting = f"{records[0]['year']}-{records[0]['level']}-deferred"
    scheme_path = records[0]['markingScheme']['path']
    grid = dict(review['grid'])
    grids['sittings'][sitting] = {'family': grid['family'], 'scheme': scheme_path, 'schemeSha256': sha(scheme_path),
                                  'gridPages': grid['gridPages'], 'capRule': grid['capRule'],
                                  'capRulePage': grid['capRulePage'], 'capRuleEvidence': grid['capRuleEvidence']}
    changed['english-marking-grids.json'] = grids

    # 2. Readers (source attachments) and printed duplicates, before tasks are extracted.
    extracted = extract(records)
    attachments = read('english-source-review.json')
    previous = dict(attachments['attachments'])
    for tid in [t for t in attachments['attachments'] if t.startswith(key_prefix(key))]:
        del attachments['attachments'][tid]
    for tid, decision in review.get('sources', {}).items():
        paper_id = tid.split('-p')[0] + '-p' + tid.split('-deferred-p')[1][0]
        parsed, tasks = extracted[paper_id]
        task = next(t for t in tasks if t['id'] == tid)
        entry = dict(decision)
        if decision['kind'] == 'not-required':
            card = next(c for c in parsed if c['id'] == tid or tid.startswith(c['id'] + '-'))
            # The reader the exclusion removes: the card's default, or (once excluded, the leaf shares the
            # card's dict) the reader the previous run recorded, which extraction re-checks against the default.
            default = card.get('sourceMaterial') or previous[tid]['excludedSource']
            entry = {'kind': 'not-required',
                     'excludedSource': {k: default[k] for k in ('label', 'title', 'pages')},
                     'paperSha256': by_paper[paper_id]['questionPaper']['sha256'],
                     'questionSha256': fingerprint(task['questionText']), 'reason': decision['reason']}
        else:
            entry['questionSha256'] = fingerprint(task['questionText'])
        attachments['attachments'][tid] = entry
    changed['english-source-review.json'] = attachments
    duplicates = read('english-printed-duplicates.json')
    for tid in [t for t in duplicates['duplicates'] if t.startswith(key_prefix(key))]:
        del duplicates['duplicates'][tid]
    duplicates['duplicates'].update(review.get('duplicates', {}))
    changed['english-printed-duplicates.json'] = duplicates
    if not check:
        for name, value in changed.items():
            write(name, value)
        extracted = extract(records)

    # 3. Task reviews, selections, raw directives and the visual ledger, bound to the fresh tasks.
    task_reviews = read('english-task-review.json')
    selections = read('english-selection-review.json')
    raw = read('english-raw-selection-review.json')
    visual = read('english-visual-review.json')
    for ledger, field in ((task_reviews, 'tasks'), (selections, 'decisions'), (raw, 'decisions')):
        for tid in [t for t in ledger[field] if t.startswith(key_prefix(key))]:
            del ledger[field][tid]
    visual['papers'] = [p for p in visual['papers'] if not p['paperId'].startswith(key_prefix(key))]
    for paper_id in by_paper:
        raw.setdefault('sources', {}).pop(paper_id, None)

    defaults = review['criteria']['defaults']
    for paper_id, record in sorted(by_paper.items()):
        parsed, tasks = extracted[paper_id]
        side = json.loads((ROOT / 'scripts/paper-trail/answers' / str(record['year']) / (record['paperFileid'] + '.json')).read_text())
        parents = {q['n']: q for q in side['q']}
        scheme = fitz.open(ROOT / record['markingScheme']['path'])
        for task in tasks:
            kind = task_kind(task)
            default = defaults[kind]
            override = review['criteria'].get('tasks', {}).get(task['id'], {})
            mode = override.get('mode', default['mode'])
            allocation = override.get('allocation', default.get('allocation'))
            parent = parents[task['atlasParent']]
            if task.get('schemeAbsent'):
                pages = review['criteria']['absentPages'][kind]
                reason = review['criteria'].get('absentPreamble', DEFERRED_NOTE) + ' ' + \
                    review['criteria']['absentReason'][kind].format(marks=task['totalMarks'])
            else:
                # The page the task's own wording is traced to inside its scheme block.
                pages = override.get('schemePages') or [task['schemePage']]
                printed = scheme_split(scheme, parent.get('schemeRegion') or parent['region']) \
                    if mode == 'discrete' or kind not in ('comparative-q1', 'qa', 'unseen') else None
                if mode == 'discrete' and len(tasks_in_block(tasks, task)) == 1 and printed and printed != allocation:
                    raise ValueError(f"{task['id']}: the scheme prints {printed}, the review says {allocation}")
                if mode != 'discrete' and printed and len(tasks_in_block(tasks, task)) == 1:
                    raise ValueError(f"{task['id']}: the scheme prints a split {printed} for a combined task")
                reason = review['criteria']['presentReason'][kind].format(marks=task['totalMarks'], page=pages[0])
                if task['level'] == 'ordinary':
                    ordinary_criteria_printed(scheme, task, mode, allocation)
            criteria = {'mode': mode}
            if mode == 'discrete' or (mode == 'combined' and allocation):
                criteria['allocation'] = allocation
            notes = override.get('notes') or (default['absentNotes'] if task.get('schemeAbsent') else default['notes'])
            criteria['notes'] = notes.format(marks=task['totalMarks'])
            task_reviews['tasks'][task['id']] = {
                'taskSha256': task_fingerprint(task),
                'paperSha256': record['questionPaper']['sha256'], 'schemeSha256': record['markingScheme']['sha256'],
                'totalMarks': task['totalMarks'], 'schemePages': pages,
                'generalCriteriaPages': review['criteria']['generalCriteriaPages'][paper_id[-2:]],
                'criteria': criteria, 'reason': reason}
            decision = review.get('selection', {}).get(task['id'])
            if decision:
                # "{page}" in a reason is the scheme page the task's wording traces to.
                decision = {**decision, 'reason': decision['reason'].format(page=task.get('schemePage'))}
                entry = {'questionSha256': fingerprint(task['questionText']), **decision}
                english_choices.expand(task, entry)
                selections['decisions'][task['id']] = entry
            elif english_choices.DIRECTIVE.search(task['rawQuestionText']):
                raise ValueError(f"{task['id']}: selection wording with no reviewed decision")

        # Raw directives.
        hits = scan([record])
        raw['sources'][paper_id] = record['questionPaper']['sha256']
        overrides = review.get('raw', {})
        source_pages = set(review['sourcePages'].get(paper_id[-2:], []))
        last_page = record['questionPaper']['pages']
        for hit in hits:
            local = hit['id'][len(key_prefix(key)):]
            decision = overrides.get(local) or classify(hit, tasks, suggested_tasks, source_pages, last_page)
            if not decision:
                raise ValueError(f'{hit["id"]}: unclassified raw directive {hit["text"]!r}')
            entry = {'textSha256': hit['textSha256'], 'contextSha256': hit['contextSha256'], 'kind': decision['kind']}
            if decision['kind'] == 'tasks':
                entry['taskIds'] = decision['taskIds']
                entry['taskSha256'] = {tid: fingerprint(next(t for t in tasks if t['id'] == tid)['questionText'])
                                       for tid in decision['taskIds']}
            entry['reason'] = decision.get('reason') or REASONS[decision['kind']]
            raw['decisions'][hit['id']] = entry

        # Visual ledger.
        routes, _ = english_choices.review(tasks, {t: d for t, d in selections['decisions'].items()
                                                   if t.startswith(paper_id + '-')})
        paper = review['papers'][paper_id[-2:]]
        visual['papers'].append({
            'paperId': paper_id,
            'paperSha256': record['questionPaper']['sha256'], 'schemeSha256': record['markingScheme']['sha256'],
            'paperPagesInspected': list(range(1, record['questionPaper']['pages'] + 1)),
            'visualSweepComplete': True, 'notes': paper['notes'],
            'allTaskBoundariesSchemeChecked': True, 'allFiniteRoutesReconciled': True,
            'schemePagesTextChecked': paper['schemePagesChecked'], 'schemePagesVisuallyChecked': paper['schemePagesViewed'],
            'independentPaperTally': {'baseTasks': paper['tally']['baseTasks'], 'finiteRoutes': paper['tally']['finiteRoutes'],
                                      'basis': paper['tally']['basis']}})
        if paper['tally']['baseTasks'] != len(tasks) or paper['tally']['finiteRoutes'] != len(routes):
            raise ValueError(f'{paper_id}: the independent tally ({paper["tally"]["baseTasks"]}/'
                             f'{paper["tally"]["finiteRoutes"]}) differs from the extracted {len(tasks)}/{len(routes)}')
    changed.update({'english-task-review.json': task_reviews, 'english-selection-review.json': selections,
                    'english-raw-selection-review.json': raw, 'english-visual-review.json': visual})
    # One order whatever order the sittings are written in: June's entries as committed, then every
    # deferred entry by id.
    def ordered(mapping):
        june = [(k, v) for k, v in mapping.items() if '-deferred' not in k]
        return dict(june + sorted((k, v) for k, v in mapping.items() if '-deferred' in k))
    grids['sittings'] = ordered(grids['sittings'])
    attachments['attachments'] = ordered(attachments['attachments'])
    duplicates['duplicates'] = ordered(duplicates['duplicates'])
    task_reviews['tasks'] = ordered(task_reviews['tasks'])
    selections['decisions'] = ordered(selections['decisions'])
    raw['decisions'] = ordered(raw['decisions'])
    raw['sources'] = ordered(raw['sources'])
    visual['papers'] = [p for p in visual['papers'] if '-deferred-' not in p['paperId']] + \
        sorted((p for p in visual['papers'] if '-deferred-' in p['paperId']), key=lambda p: p['paperId'])
    stale = []
    for name, value in changed.items():
        text = json.dumps(value, ensure_ascii=False, indent=2 if name in INDENT2 else 1) + '\n'
        if check:
            if (AUTHORED / name).read_text() != text:
                stale.append(name)
        else:
            (AUTHORED / name).write_text(text)
    return stale


def ordinary_criteria_printed(scheme, task, mode, allocation):
    """An Ordinary scheme prints each part's award on one line: "Combined Criteria ex 10 P + C = 6 L + M = 4" or
    "Discrete Criteria ex 30 P = 9 C = 9 L = 9 M = 3". The task's own line must be on its traced page or the next."""
    page = task['schemePage']
    text = ' '.join(' '.join(scheme[p - 1].get_text().split()) for p in (page, page + 1) if p <= len(scheme))
    text = text.replace('P+C', 'P + C').replace('L+M', 'L + M')
    marks = task['totalMarks']
    if mode == 'discrete':
        want = (f"Discrete Criteria ex {marks} P = {allocation['P']} C = {allocation['C']} L = {allocation['L']} "
                f"M = {allocation['M']}")
    else:
        want = f"Combined Criteria ex {marks} P + C = {allocation['P+C']} L + M = {allocation['L+M']}"
    if mode == 'discrete' and marks == 100 and allocation == {'P': 30, 'C': 30, 'L': 30, 'M': 10}:
        # A composition prints its discrete grid in full: 100% / 30% / 10% rows (2022 leaves the 100% row's
        # label cell empty, so the row is matched by its first two bands).
        flat = re.sub(r'\s*-\s*', ' - ', text)
        if '100 - 90 89 - 80' in flat and '30% 30 - 27' in flat and '10% 10 - 9' in flat:
            return
    if re.sub(r'\s+', ' ', want) not in re.sub(r'\s*=\s*', ' = ', text):
        raise ValueError(f"{task['id']}: the scheme does not print “{want}” on PDF{page}-{page + 1}")


def key_prefix(key):
    year, level = key.split('-')
    return f'english-{year}-{level}-deferred-'


def tasks_in_block(tasks, task):
    return [t for t in tasks if t['atlasParent'] == task['atlasParent']]


def norm(text):
    return re.sub(r'[^\w]+', ' ', text.lower()).strip()


def classify(hit, tasks, suggested_tasks, source_pages, last_page):
    text = hit['text'].strip()
    if re.fullmatch(r'(?i)or', text):
        # A standalone OR between printed alternatives, each its own task.
        return {'kind': 'exam-instruction'}
    suggested = suggested_tasks(hit, tasks)
    if suggested:
        return {'kind': 'tasks', 'taskIds': suggested}
    bare = text
    while True:
        stripped = re.sub(r'^\s*(?:[1-9]\.|\((?:[a-c]|i{1,3}|iv)\))\s*', '', bare)
        if stripped == bare:
            break
        bare = stripped
    bare = norm(bare)
    inside = [t for t in tasks if any(region['p'] == hit['page'] and region['r'][1] - .01 <= hit['y'] < region['r'][3]
                                      for region in t.get('paperRegion', []))]
    holders = [t['id'] for t in inside if len(bare.split()) >= 2 and f' {bare} ' in f" {norm(t['rawQuestionText'])} "]
    if holders:
        return {'kind': 'tasks', 'taskIds': holders}
    if hit['page'] == last_page and re.search(r'(?i)copyright|examination paper|third.party|authoris|section 53|'
                                               r'commission does not|\(2000\)', hit['context']):
        return {'kind': 'non-selection'}
    if hit['page'] == 1 or re.match(r'(?i)^(?:candidates\s+(?:must|should|may)|answer|write\s+a\s+composition\s+on\s+any|'
                                    r'read\s+the\s+following\s|you\s+must\s+answer|[A-C]\s+[A-Z ,]+$|'
                                    # the choice rubric's last line ("or C – Cultural Context.") and the
                                    # Comparative Study's "Please note" definitions ("• When used, the words …")
                                    r'or\s+[A-C]\s*[–—-]|[•\uf0b7]\s*when\s+used|'
                                    # a comparative mode's heading printed apart from its letter
                                    r'(?:THEME OR ISSUE|CULTURAL CONTEXT|GENERAL VISION AND VIEWPOINT|LITERARY GENRE|'
                                    r'HERO, HEROINE,? VILLAIN|SOCIAL SETTING|RELATIONSHIPS)$)', text):
        return {'kind': 'exam-instruction'}
    if hit['page'] in source_pages:
        # A line of the printed passage or poem: on a page that prints one, and in no task's own wording.
        return {'kind': 'source-prose'}
    return None


def remove(key):
    """Take one sitting's entries out of every ledger (to commit sittings one at a time)."""
    prefix = key_prefix(key)
    for name, field in (('english-task-review.json', 'tasks'), ('english-selection-review.json', 'decisions'),
                        ('english-raw-selection-review.json', 'decisions'), ('english-source-review.json', 'attachments'),
                        ('english-printed-duplicates.json', 'duplicates')):
        ledger = read(name)
        ledger[field] = {k: v for k, v in ledger[field].items() if not k.startswith(prefix)}
        if name == 'english-raw-selection-review.json':
            ledger['sources'] = {k: v for k, v in ledger['sources'].items() if not k.startswith(prefix)}
        write(name, ledger)
    visual = read('english-visual-review.json')
    visual['papers'] = [p for p in visual['papers'] if not p['paperId'].startswith(prefix)]
    write('english-visual-review.json', visual)
    grids = read('english-marking-grids.json')
    year, level = key.split('-')
    grids['sittings'].pop(f"{year}-{'higher' if level == 'hl' else 'ordinary'}-deferred", None)
    write('english-marking-grids.json', grids)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--remove', help='take this sitting\'s entries out of the ledgers')
    parser.add_argument('sittings', nargs='*')
    parser.add_argument('--all', action='store_true')
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    detect_indent()
    if args.remove:
        remove(args.remove)
        print(f'{args.remove}: removed')
        return 0
    keys = sorted(p.stem for p in REVIEWS.glob('*.json')) if args.all else args.sittings
    stale = []
    for key in keys:
        review = json.loads((REVIEWS / f'{key}.json').read_text())
        stale += [f'{key}: {name}' for name in apply(key, review, args.check)]
        print(f'{key}: {"checked" if args.check else "written"}')
    if stale:
        print('Stale English deferred ledgers: ' + ', '.join(stale), file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
