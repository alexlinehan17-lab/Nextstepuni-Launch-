"""Restore missing 2012 Atlas maps from the independently inspected task crops.

Keep the solution and detailed credit regions separate: they occur in different
sections of these schemes. A single first-to-last-page span would expose other
questions' answers. Existing parent Q5/Q6 identities remain available alongside
the separately selectable A/B alternatives.
"""
import hashlib
import json
from pathlib import Path
import re

import fitz

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / 'scripts/markbank/authoring/maths'


def build(name, level):
    review = json.loads((ROOT / f'scripts/markbank/mathematics/reviews/2012-{level}-p2'
                        f'{"-project" if "project" in name else ""}.json').read_text())
    plan = json.loads((BASE / f'{name}-presentation.json').read_text())
    assert plan['status'] == 'visually inspected'
    docs = {}
    for kind, archive, key in [('question', 'exampapers', 'paper'), ('scheme', 'markingschemes', 'scheme')]:
        path = ROOT / f'paper-trail-corpus/{archive}/2012' / review[f'{key}Fileid']
        assert hashlib.sha256(path.read_bytes()).hexdigest() == review[f'{key}Sha256']
        docs[kind] = fitz.open(path)
    groups = {}
    for task in review['cards']:
        suffix = task['id'].split('-q', 1)[1]
        view = plan['tasks'][suffix]
        assert view['inspectedQuestionSha256'] and view['inspectedSolutionSha256']
        n = re.match(r'Q(\d+[A-Z]?)', task['printedParts'][0])[1]
        groups.setdefault(n, []).append(view)
    for n in list(groups):
        if n[-1].isalpha():
            groups.setdefault(n[:-1], []).extend(groups[n])

    def regions(views, kind):
        # Every task rectangle has already been visually inspected. Union on
        # the same page retains the whole question and its context without
        # spanning unrelated intermediate scheme pages.
        pages = {}
        for view in views:
            for box in view[f'{kind}Regions']:
                page = box['page']
                bounds = [box['x0'], box['top'], box['x1'], box['bottom']]
                if page in pages:
                    old = pages[page]
                    bounds = [min(old[0], bounds[0]), min(old[1], bounds[1]),
                              max(old[2], bounds[2]), max(old[3], bounds[3])]
                pages[page] = bounds
        result = []
        for page, box in sorted(pages.items()):
            rect = docs[kind][page - 1].rect
            # Whole-question maps use the full page width. Individual task
            # crops deliberately omit repeated prompts beside an answer box;
            # taking their x bounds for a larger vertical span would clip the
            # intervening reprinted prompt or table border.
            fractions = [0, box[1] / rect.height, 1, box[3] / rect.height]
            assert 0 <= fractions[0] < fractions[2] <= 1
            assert 0 <= fractions[1] < fractions[3] <= 1
            result.append({'p': page, 'r': [round(v, 6) for v in fractions]})
        return result

    questions = []
    for n in sorted(groups, key=lambda n: (int(re.match(r'\d+', n)[0]), n)):
        paper = regions(groups[n], 'question')
        scheme = regions(groups[n], 'scheme')
        row = dict(n=n, label=f'Q{n}', pP=paper[0]['p'], pY=[paper[0]['r'][1], 1],
                   endP=paper[-1]['p'], endY=paper[-1]['r'][3], paperRegion=paper,
                   region=scheme, mode='crop', conf=1.0)
        if n[-1].isalpha():
            row['parentN'] = n[:-1]
        questions.append(row)
    scheme_pages = [r['p'] for q in questions for r in q['region']]
    result = dict(v=1, paperFileid=review['paperFileid'], schemeFileid=review['schemeFileid'],
                  component=re.search(r'LP(\d{3})', review['paperFileid'])[1],
                  band=[min(scheme_pages), max(scheme_pages) + 1], maxCropPages=4,
                  copyright='© State Examinations Commission', q=questions)
    assert repr(f"mathematics|2012|{review['paperFileid']}") in (ROOT / 'components/PaperTrail/vaultResolve.ts').read_text()
    content = json.dumps(result, ensure_ascii=False, sort_keys=True, separators=(',', ':')) + '\n'
    for directory in ['scripts/paper-trail/answers', 'public/paper-answers']:
        (ROOT / directory / '2012' / (review['paperFileid'] + '.json')).write_text(content)
    path = ROOT / 'paperTrailData.ts'
    lines = path.read_text().splitlines(keepends=True)
    found = 0
    for i, line in enumerate(lines):
        if '"year": 2012' not in line or f'"{review["paperFileid"]}"' not in line:
            continue
        entry = json.loads(line.strip().rstrip(','))
        for item in entry['papers']:
            if item['doc']['f'] == review['paperFileid']:
                assert item['scheme']['f'] == review['schemeFileid']
                item['answers'] = 1
                found += 1
        lines[i] = '    ' + json.dumps(entry, ensure_ascii=False) + ',\n'
    assert found == 1
    path.write_text(''.join(lines))
    print(f"{review['paperFileid']}: {len(questions)} hosted anchors including the preserved alternative parent")


if __name__ == '__main__':
    build('2012-ol-p2', 'ordinary')
    build('2012-fl-p2-project', 'foundation')
