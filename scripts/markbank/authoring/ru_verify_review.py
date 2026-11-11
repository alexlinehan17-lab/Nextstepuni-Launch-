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


def verify_alternative_sources(document, card):
    """An alternative rule must occur on its own declared source pages.

    Do not accept a matching phrase elsewhere in the task's wider guidance.
    This gate reads original PDF text; runtime tests do not require local PDFs.
    """
    for alternative in card.get('rubric', {}).get('alternativeSets', []):
        pages = alternative['schemePages']
        assert pages and all(type(page) is int and 1 <= page <= len(document) for page in pages), (card['id'], alternative['id'])
        claim = normal(alternative['sourceText'])
        sources = [normal('\n'.join(document[page-1].get_text(sort=sort) for page in pages)) for sort in (False, True)]
        assert claim and any(claim in source for source in sources), (card['id'], alternative['id'], alternative['sourceText'])


def verify_allocation_sources(document, card):
    """Each fixed/conditional cap must quote its own original scheme pages."""
    cap = card.get('rubric', {}).get('allocationCap')
    if not cap:
        return
    for rule in [cap, *cap.get('limits', [])]:
        pages = rule['schemePages']
        assert pages and all(type(page) is int and 1 <= page <= len(document) for page in pages), card['id']
        claim = normal(rule['sourceText'])
        sources = [normal('\n'.join(document[page-1].get_text(sort=sort) for page in pages)) for sort in (False, True)]
        assert claim and any(claim in source for source in sources), (card['id'], rule.get('id', 'allocation-cap'), rule['sourceText'])



def verify_manual_criterion_exception_sources(document, card):
    """A manual language exception must name existing top-level awards and quote its own pages."""
    exception = card.get('answerLanguageRule', {}).get('manualCriterionExceptions')
    if not exception:
        return
    rubric = card.get('rubric', {})
    assert rubric.get('system') == 'language-points', card['id']
    criteria = {criterion['id']: criterion for criterion in rubric.get('criteria', [])}
    identifiers = exception['criterionIds']
    assert identifiers and all(isinstance(identifier, str) and identifier.strip() for identifier in identifiers), card['id']
    assert len(identifiers) == len(set(identifiers)), card['id']
    assert all(identifier in criteria and criteria[identifier].get('kind') != 'deduction' for identifier in identifiers), card['id']
    pages = exception['schemePages']
    assert pages and all(type(page) is int and 1 <= page <= len(document) for page in pages), card['id']
    claim = normal(exception['sourceText'])
    sources = [normal('\n'.join(document[page-1].get_text(sort=sort) for page in pages)) for sort in (False, True)]
    assert claim and any(claim in source for source in sources), (card['id'], 'manual-criterion-language-exception', exception['sourceText'])

def verify_automatic_award_sources(document, card):
    """Fixed awards must quote their own original pages, not wider guidance."""
    rubric = card.get('rubric', {})
    for criterion in [*rubric.get('criteria', []),
                      *[c for group in rubric.get('groups', []) for c in group.get('criteria', [])]]:
        award = criterion.get('automaticAward')
        if award is None:
            continue
        assert rubric.get('system') == 'language-writing' and not card.get('answerLanguageRule'), card['id']
        assert type(award['marks']) is int and award['marks'] > 0, card['id']
        assert award['marks'] == criterion['maxMarks'] and criterion['permittedMarks'] == [award['marks']], card['id']
        assert criterion.get('kind') != 'deduction' and 'deductFrom' not in criterion, card['id']
        assert 'limits' not in criterion and 'bands' not in criterion, card['id']
        assert not any(other.get('deductFrom') == criterion['id'] for other in rubric['criteria']), card['id']
        pages = award['schemePages']
        assert pages and all(type(page) is int and 1 <= page <= len(document) for page in pages), card['id']
        claim = normal(award['sourceText'])
        sources = [normal('\n'.join(document[page-1].get_text(sort=sort) for page in pages)) for sort in (False, True)]
        assert claim and any(claim in source for source in sources), (card['id'], criterion['id'], award['sourceText'])


def criterion_claims(criteria):
    for criterion in criteria:
        yield from criterion['guidance']
        if criterion.get('automaticAward'):
            yield criterion['automaticAward']['sourceText']
        for band in criterion.get('bands', []):
            yield from band['guidance']
        for limit in criterion.get('limits', []):
            yield from limit['guidance']
            for band in limit.get('bands', []):
                yield from band['guidance']


def claims(card):
    if card.get('answerLanguageRule'):
        yield card['answerLanguageRule']['sourceText']
        if card['answerLanguageRule'].get('manualCriterionExceptions'):
            yield card['answerLanguageRule']['manualCriterionExceptions']['sourceText']
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
    if rubric.get('allocationCap'):
        yield rubric['allocationCap']['sourceText']
        for limit in rubric['allocationCap'].get('limits', []):
            yield limit['sourceText']
    for group in rubric.get('groups', []):
        for row in group['rows']:
            yield from row['text'].split(' — ')
        yield from criterion_claims(group.get('criteria', []))
    yield from rubric['taskRequirements']
    yield from criterion_claims(rubric.get('criteria', []))


def verify(cards=None):
    if cards is None:
        cards = json.loads((ROOT / 'scripts/markbank/authored/russian-reviewed.json').read_text())
    failures = []
    count = 0
    for card in cards:
        level = 'hl' if card['level'] == 'higher' else 'ol'
        with open_scheme(card['year'], level) as document:
            verify_alternative_sources(document, card)
            verify_allocation_sources(document, card)
            verify_manual_criterion_exception_sources(document, card)
            verify_automatic_award_sources(document, card)
            pages = sorted(set(card['review']['schemePages'] + card['review'].get('guidancePages', [])
                               + card.get('answerLanguageRule', {}).get('schemePages', [])
                               + card.get('answerLanguageRule', {}).get('manualCriterionExceptions', {}).get('schemePages', [])
                               + card.get('rubric', {}).get('allocationCap', {}).get('schemePages', [])
                               + [page for criterion in card.get('rubric', {}).get('criteria', [])
                                  for page in criterion.get('automaticAward', {}).get('schemePages', [])]
                               + [page for limit in card.get('rubric', {}).get('allocationCap', {}).get('limits', [])
                                  for page in limit['schemePages']]))
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
            if not claim.strip() or (not any(normal(claim) in source for source in sources) and normal(claim) not in paper_answers):
                failures.append((card['id'], claim))
    assert not failures, '\n'.join(f'{cid}: {claim}' for cid,claim in failures)
    print(f'{len(cards)} Russian cards: {count} answer/guidance slices verified against their original scheme pages and explicitly accepted paper bindings.')


if __name__ == '__main__':
    verify()
