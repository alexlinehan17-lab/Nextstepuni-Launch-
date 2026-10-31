"""Publish visually reviewed A/B anchors without changing existing questions."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
PLAN = ROOT / 'scripts/markbank/mathematics/historical-alternative-anchors.json'


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def row(n, regions, parent=None):
    paper = regions['paper']
    result = dict(n=n, label=f'Q{n}', pP=paper[0]['p'], pY=[paper[0]['r'][1], 1],
                  endP=paper[-1]['p'], endY=paper[-1]['r'][3], paperRegion=paper,
                  region=regions['scheme'], mode='crop', conf=1.0)
    if parent:
        result['parentN'] = parent
    return result


def combine(alternatives, kind):
    pages = {}
    for alternative in alternatives:
        for region in alternative[kind]:
            p, r = region['p'], region['r']
            if p in pages:
                old = pages[p]
                r = [min(old[0], r[0]), min(old[1], r[1]), max(old[2], r[2]), max(old[3], r[3])]
            pages[p] = r
    return [{'p': p, 'r': r} for p, r in sorted(pages.items())]


def main():
    plan = json.loads(PLAN.read_text())
    assert plan['status'] == 'visually inspected'
    for review in plan['papers']:
        year, fileid = review['year'], review['paperFileid']
        for kind, archive in [('paper', 'exampapers'), ('scheme', 'markingschemes')]:
            path = ROOT / f'paper-trail-corpus/{archive}/{year}' / review[f'{kind}Fileid']
            assert hashlib.sha256(path.read_bytes()).hexdigest() == review[f'{kind}Sha256']
        source = ROOT / f'scripts/paper-trail/answers/{year}/{fileid}.json'
        answer_map = json.loads(source.read_text())
        original_numbers = set(review['originalQuestionNumbers'])
        originals = [q for q in answer_map['q'] if q['n'] in original_numbers]
        assert digest(originals) == review['originalQuestionsSha256'], f'Existing question changed: {source}'
        if len(answer_map['q']) == len(originals):
            assert hashlib.sha256(source.read_bytes()).hexdigest() == review['baseMapSha256']
        additions = []
        parents = {}
        for n, regions in review['questions'].items():
            assert n not in original_numbers
            for kind in ['paper', 'scheme']:
                assert regions[kind]
                for segment in regions[kind]:
                    x0, y0, x1, y1 = segment['r']
                    assert segment['p'] > 0 and 0 <= x0 < x1 <= 1 and 0 <= y0 < y1 <= 1
            additions.append(row(n, regions, n[:-1]))
            parents.setdefault(n[:-1], []).append(regions)
        # 2010 Ordinary Project Paper 2 previously stopped at Q8. Keep Q9 as
        # an umbrella for its two separately selectable alternatives.
        for n, alternatives in parents.items():
            if n not in original_numbers:
                additions.append(row(n, {kind: combine(alternatives, kind) for kind in ['paper', 'scheme']}))
        expected_numbers = original_numbers | {q['n'] for q in additions}
        assert all(q['n'] in expected_numbers for q in answer_map['q']), 'Unexpected anchor would be dropped'
        answer_map['q'] = originals + additions
        pages = [r['p'] for q in additions for r in q['region']]
        band = answer_map['band']
        answer_map['band'] = [min(band[0], min(pages)), max(band[1], max(pages) + 1)]
        answer_map['maxCropPages'] = max(answer_map.get('maxCropPages', 3), 4)
        assert repr(f'mathematics|{year}|{fileid}') in (ROOT / 'components/PaperTrail/vaultResolve.ts').read_text()
        content = json.dumps(answer_map, ensure_ascii=False, sort_keys=True, separators=(',', ':')) + '\n'
        for directory in ['scripts/paper-trail/answers', 'public/paper-answers']:
            path = ROOT / directory / str(year) / (fileid + '.json')
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content)
        print(f'{year}/{fileid}: {len(originals)} unchanged + {len(additions)} added anchors')


if __name__ == '__main__':
    main()
