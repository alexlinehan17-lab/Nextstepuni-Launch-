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
        if repair.get('kind') == 'unnumbered-question':
            parts, texts = _repair_unnumbered(repair, raw, parts, texts)
            continue
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


def _lettered(segment, number):
    """The lettered tasks (a), (b), (c)... printed in one question's segment of the page."""
    headers = list(re.finditer(r'(?m)^\(([a-e])\)\s*$', segment))
    out = []
    for i, match in enumerate(headers):
        end = headers[i + 1].start() if i + 1 < len(headers) else len(segment)
        out.append({'key': [number, match[1], None], 'text': ' '.join(segment[match.end():end].split())})
    return out


def _repair_unnumbered(repair, raw, parts, texts):
    """A question number printed without its full stop ("5" above "(a)") is read as more parts of the
    previous question: its tasks collide with that question's keys. Re-key both questions from the page."""
    number, previous = repair['questionNumber'], repair['questionNumber'] - 1
    start_prev = re.search(rf'(?m)^{previous}\.\s*$', raw)
    start = re.search(rf'(?m)^{number}\s*$', raw)
    assert start_prev and start and start_prev.start() < start.start(), 'Question numbers no longer printed as reviewed'
    expected = _lettered(raw[start_prev.end():start.start()], previous) + _lettered(raw[start.end():], number)
    assert repair['parts'] == expected, 'Repair no longer matches the printed tasks'
    prior = {tuple(item['key']): item for item in repair['prior']}
    assert {key for key in parts if key[0] in (previous, number)} == set(prior), 'Parser changed; review required'
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
