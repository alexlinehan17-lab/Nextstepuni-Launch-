"""Original-page-pinned Construction Studies heading corrections."""
import hashlib
import json
import re
from pathlib import Path
import fitz

ROOT = Path(__file__).resolve().parents[3]
REVIEW = ROOT / 'scripts/markbank/authored/construction-studies-census-repairs.json'


def apply_construction_census_repairs(year, level, parts, texts, review=None):
    review = json.loads(REVIEW.read_text()) if review is None else review
    parts, texts = set(parts), dict(texts)
    for repair in review['repairs']:
        if (repair['year'], repair['level']) != (year, level):
            continue
        source = repair['source']
        path = ROOT / source['file']
        assert repair['reason'] and hashlib.sha256(path.read_bytes()).hexdigest() == source['sha256']
        with fitz.open(path) as pdf:
            raw = pdf[source['page'] - 1].get_text()
        assert hashlib.sha256(' '.join(raw.split()).encode()).hexdigest() == source['textSha256']
        number = repair['questionNumber']
        question = raw[re.search(rf'(?m)^{number}\.\s*$', raw).start():]
        headers = list(re.finditer(r'(?m)^\(([abc])\)\s*$', question))
        assert [m[1] for m in headers] == ['a', 'b', 'c']
        expected = []
        for i, match in enumerate(headers):
            end = headers[i + 1].start() if i + 1 < len(headers) else len(question)
            expected.append({'key': [number, match[1], None],
                             'text': ' '.join(question[match.end():end].split())})
        assert repair['parts'] == expected, 'Repair no longer matches the printed tasks'
        prior = {tuple(item['key']): item for item in repair['prior']}
        assert set(prior) == {(number, None, 'i'), (number, None, 'ii')}
        assert {key for key in parts if key[0] == number} == set(prior), 'Parser changed; review required'
        for key, item in prior.items():
            assert texts[key] == item['text']
            assert hashlib.sha256(texts[key].encode()).hexdigest() == item['sha256']
            parts.remove(key)
            texts.pop(key)
        for item in expected:
            key = tuple(item['key'])
            assert key not in parts
            parts.add(key)
            texts[key] = item['text']
    return parts, texts
