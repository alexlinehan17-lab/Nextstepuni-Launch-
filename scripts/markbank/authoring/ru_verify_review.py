#!/usr/bin/env python3
"""Fail if reviewed Russian claimable content does not occur on its source pages."""
import json
import re
from pathlib import Path
import fitz
from ru_source_text import open_scheme

ROOT = Path(__file__).resolve().parents[3]


def normal(text):
    return re.sub(r'[^\w]+', '', text.casefold())


def claims(card):
    if card.get('answerLanguageRule'):
        yield card['answerLanguageRule']['sourceText']
    if card['kind'] == 'question':
        rows = [row for variant in card.get('answerVariants', []) for row in variant['rows']] or card['rows']
        for row in rows:
            if row.get('group'):
                for option in row['group']['options']:
                    yield from option.split(' — ')
            else:
                yield row['verbatim']
        return
    rubric = card['rubric']
    for group in rubric.get('groups', []):
        for row in group['rows']:
            yield from row['text'].split(' — ')
    yield from rubric['taskRequirements']
    for criterion in rubric.get('criteria', []):
        yield from criterion['guidance']
        for band in criterion.get('bands', []):
            yield from band['guidance']
        for limit in criterion.get('limits', []):
            yield from limit['guidance']
            for band in limit.get('bands', []):
                yield from band['guidance']


def verify(cards=None):
    if cards is None:
        cards = json.loads((ROOT / 'scripts/markbank/authored/russian-reviewed.json').read_text())
    failures = []
    count = 0
    for card in cards:
        level = 'hl' if card['level'] == 'higher' else 'ol'
        with open_scheme(card['year'], level) as document:
            pages = sorted(set(card['review']['schemePages'] + card['review'].get('guidancePages', [])
                               + card.get('answerLanguageRule', {}).get('schemePages', [])))
            versions = ['\n'.join(document[p-1].get_text(sort=sort) for p in pages) for sort in (False,True)]
            sources = [normal(version) for version in versions]
        # Some schemes expressly accept details from their original passage
        # without repeating those details. Bind only the named answer to its
        # exact paper page, and independently require the scheme acceptance.
        paper_answers = {}
        for binding in card['review'].get('paperAnswerSources', []):
            assert any(normal(binding['schemeAcceptance']) in source for source in sources), card['id']
            component=card['review']['component']
            with fitz.open(ROOT / f"examiner-reports/russian/papers/{card['year']}-{level}-{component}-paper.pdf") as paper:
                versions=['\n'.join(paper[p-1].get_text(sort=sort) for p in binding['pages']) for sort in (False,True)]
                assert any(normal(binding['text']) in normal(version) for version in versions), (card['id'],binding['text'])
            paper_answers[normal(binding['text'])]=True
        for claim in claims(card):
            count += 1
            if not any(normal(claim) in source for source in sources) and normal(claim) not in paper_answers:
                failures.append((card['id'], claim))
    assert not failures, '\n'.join(f'{cid}: {claim}' for cid,claim in failures)
    print(f'{len(cards)} Russian cards: {count} answer/guidance slices verified against their original scheme pages and explicitly accepted paper bindings.')


if __name__ == '__main__':
    verify()
