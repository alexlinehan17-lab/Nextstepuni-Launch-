"""Exact source-reviewed Japanese references with roman-then-letter nesting.

The generic grammar treats a letter after a roman as a sibling. Japanese
written and listening papers also print letters nested below romans. Only an explicitly
inventoried literal reference may bind to the canonical (letter, roman) key;
this module does not broaden the grammar or affect another subject.
"""
import json
import re
from pathlib import Path


def reviewed_japanese_refs(directory=None):
    directory = Path(directory or Path(__file__).parent / 'reviews')
    result = {}
    for path in sorted(directory.glob('japanese-*-census.json')):
        manifest = path.with_name(path.name.replace('-census.json', '.json'))
        if not manifest.exists():
            continue
        census = json.loads(path.read_text())
        review = json.loads(manifest.read_text())
        assert census['subjectId'] == review['subjectId'] == 'japanese'
        assert review['sitting'] == f"{census['year']}-{census['level']}"
        for task in census['tasks']:
            if 'paperRef' not in task:
                continue
            section, q, letter, roman = task['key']
            assert ((task['component'] == 'aural' and re.fullmatch(r'L[A-D]', section))
                    or (task['component'] == 'paper' and re.fullmatch(r'[1-3][A-D]', section)))
            assert q is None or (isinstance(q, int) and q > 0)
            assert re.fullmatch(r'[a-z]', letter) and re.fullmatch(r'(?:i|ii|iii|iv|v|vi|vii|viii|ix|x)', roman)
            question = f' Q{q}' if q is not None else ''
            literal = f"{census['year']} {census['level'].upper()} Section {section}{question}({roman})({letter})"
            assert task['paperRef'] == literal, (path, task)
            question_id = f'-{q}' if q is not None else ''
            cid = f"ja-{census['year']}-{census['level']}-{section.lower()}{question_id}-{letter}-{roman}"
            matches = [card for card in review['cards'] if card['id'] == cid]
            assert len(matches) == 1 and matches[0]['questionRef'] == literal, cid
            assert matches[0]['sourceEvidence']['paperPages'] == task['paperPages'], cid
            assert cid not in result, cid
            result[cid] = {'literal': literal, 'year': census['year'], 'level': census['level'],
                           'section': section, 'q': q, 'path': (letter, roman)}
    return result


def bind_japanese_ref(cid, literal, parsed, bindings):
    binding = bindings.get(cid)
    if binding is None:
        return parsed
    if not parsed or literal != binding['literal'] or parsed['paper'] is not None:
        return None
    if any(parsed[key] != binding[key] for key in ['year', 'level', 'section', 'q']):
        return None
    return {**parsed, 'paths': [binding['path']]}
