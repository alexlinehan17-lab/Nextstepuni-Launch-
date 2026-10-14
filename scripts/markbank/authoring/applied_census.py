"""Applied Mathematics denominator from the independent visual review ledgers.

The generic printed-part parser cannot distinguish a shared tariff from two
separately priced diagrams. These ledgers record the paper-and-scheme review;
the generated runtime manifest is deliberately not an input to this census.
Irish editions share practice identities but retain independently checked PDFs.
"""
import hashlib
import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]


def read(path):
    return json.loads(path.read_text())


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def census_applied_maths(verify_sources=True):
    entries = json.loads(subprocess.check_output([
        'node', '--input-type=module', '-e',
        "import {paperIndex} from './scripts/markbank/paperIndex.mjs';"
        "console.log(JSON.stringify(paperIndex['applied-mathematics']));",
    ], cwd=ROOT, text=True))
    indexed = {(e['year'], e['level'], e['lang']): e for e in entries}
    assert len(indexed) == len(entries), 'Duplicate indexed Applied Mathematics edition'
    review_root = ROOT / 'scripts/markbank/authoring'
    canonical = {}
    papers = []
    editions = []
    seen_ids = set()

    def source(path, sha):
        if verify_sources:
            assert digest(path) == sha, f'Source changed since visual review: {path}'

    for path in sorted((review_root / 'reviewed/applied-maths').glob('*.json')):
        review = read(path)
        assert review.get('reviewMethod'), f'Missing visual review method: {path}'
        for p in review['papers']:
            year, level = review['year'], p['level']
            short = {'higher': 'hl', 'ordinary': 'ol'}[level]
            key = (year, level, 'ev')
            assert key in indexed and key not in canonical, f'Unindexed/duplicate review: {key}'
            assert len(indexed[key]['papers']) == 1, f'Unreviewed component: {key}'
            source(ROOT / f'examiner-reports/applied-maths/papers/{year}-{short}-paper.pdf', p['paperSha256'])
            source(ROOT / f'examiner-reports/applied-maths/schemes/{year}-{short}.pdf', p['schemeSha256'])
            tasks = p['tasks']
            assert len(tasks) == p['practiceTaskCount'], f'Stale task count: {key}'
            leaves = []
            marks = {}
            for task in tasks:
                cid = f'am-{year}-{short}-{task["idSuffix"]}'
                assert cid not in seen_ids, f'Duplicate reviewed task: {cid}'
                seen_ids.add(cid)
                tariff = sum(max(a['credit']) for a in task['allocations'])
                number = re.match(r'^Q(\d+)', task['ref'])[1]
                marks[number] = marks.get(number, 0) + tariff
                leaves.append({'key': [cid], 'label': f'{year} {short.upper()} {task["ref"]}',
                               'text': task['questionText'], 'marks': tariff})
            assert marks == p['questionMarks'], f'Published question tariffs changed: {key}'
            assert sum(marks.values()) == p['availableMarks'], f'Paper tariff mismatch: {key}'
            canonical[key] = (path, p, leaves)
            papers.append({'year': year, 'level': short, 'paper': None,
                           'leafCount': len(leaves), 'leaves': leaves, 'flags': [],
                           'marksSum': p['availableMarks'], 'marksQuestions': len(marks)})
            editions.append({'year': year, 'level': level, 'lang': 'ev',
                             'paperSha256': p['paperSha256'], 'schemeSha256': p['schemeSha256'],
                             'schemeLang': 'ev', 'tasks': len(tasks)})

    translated_keys = set()
    crop_reviews = {(p['year'], p['level']): p for p in
                    read(review_root / 'translated/applied-maths-crop-review.json')['papers']}
    for path in sorted((review_root / 'translated/applied-maths').glob('*.json')):
        review = read(path)
        for p in review['papers']:
            year, level = review['year'], p['level']
            short = {'higher': 'hl', 'ordinary': 'ol'}[level]
            key = (year, level, 'iv')
            assert key in indexed and key not in translated_keys, f'Unindexed/duplicate translation: {key}'
            translated_keys.add(key)
            canonical_path, original, leaves = canonical[(year, level, 'ev')]
            assert digest(canonical_path) == p['canonicalReviewSha256'], f'Stale translation review: {key}'
            assert crop_reviews[(year, level)]['ledgerSha256'] == digest(path), f'Stale crop review: {key}'
            assert not p['distinctAdditionalTasks'], f'Unauthored distinct Irish tasks: {key}'
            expected = {leaf['key'][0]: leaf['marks'] for leaf in leaves}
            links = [(cid, tariff) for q in p['questions']
                     for cid, tariff in zip(q['canonicalTaskIds'], q['taskTariffs'])]
            assert all(len(q['canonicalTaskIds']) == len(q['taskTariffs']) for q in p['questions'])
            assert len(links) == len(expected) and dict(links) == expected, f'Missing/duplicate Irish task links: {key}'
            assert p['practiceTaskCount'] == len(expected), f'Stale Irish task count: {key}'
            assert len(indexed[key]['papers']) == 1, f'Unreviewed Irish component: {key}'
            item = indexed[key]['papers'][0]
            assert item['doc']['f'] == p['paperFileid'] and item['scheme']['f'] == p['schemeFileid'], f'Wrong native source: {key}'
            paper_path = ROOT / f'examiner-reports/applied-maths/irish/{year}-{short}-paper.pdf'
            scheme_path = ROOT / (f'examiner-reports/applied-maths/irish/{year}-{short}-scheme.pdf'
                                  if p['schemeLang'] == 'iv' else
                                  f'examiner-reports/applied-maths/schemes/{year}-{short}.pdf')
            source(paper_path, p['paperSha256'])
            source(scheme_path, p['schemeSha256'])
            if verify_sources:
                import fitz
                for kind, pdf_path in [('paper', paper_path), ('scheme', scheme_path)]:
                    with fitz.open(pdf_path) as doc:
                        assert p[f'{kind}PagesReviewed'] == list(range(1, len(doc) + 1)), f'Unreviewed native pages: {key}'
            editions.append({'year': year, 'level': level, 'lang': 'iv',
                             'paperSha256': p['paperSha256'], 'schemeSha256': p['schemeSha256'],
                             'schemeLang': p['schemeLang'], 'tasks': len(expected)})
    assert set(indexed) == set(canonical) | translated_keys, 'Indexed paper edition has no independent review'
    assert set(crop_reviews) == {(k[0], k[1]) for k in translated_keys}, 'Missing/orphan native crop review'
    return {'subject': 'applied-maths', 'mode': 'reviewed-boundaries',
            'papers': papers, 'sourceEditions': editions}
