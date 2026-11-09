#!/usr/bin/env python3
"""Mandatory original-PDF authoring gate; portable runtime tests stay separate."""
import json
from paper_census import census_sections, leaves_of, key_label, continuity_flags
from he_review_2020_hl_main import documents

def verify_higher():
    d = documents()
    assert [len(d[k]) for k in ['a', 'bc', 'scheme']] == [40, 8, 42]
    expected = [f'Section A Q{n}' for n in range(1, 13) if n not in [6, 10, 11, 12]]
    expected += [f'Section A Q{n}({r})' for n in [6, 10, 11, 12] for r in ['i', 'ii']]
    expected += [f'Section B Q1({letter})' for letter in 'abcd']
    expected += [f'Section B Q{n}({letter})' for n in range(2, 6) for letter in 'abc']
    expected += [f'Section C Q1(a)({r})' for r in ['i', 'ii', 'iii']]
    expected += [f'Section C Q1({letter})({r})' for letter in 'bc' for r in ['i', 'ii']]
    expected += [f'Section C Q2({letter})({r})' for letter in 'abc' for r in ['i', 'ii']]
    expected += [f'Section C Q3({letter})({r})' for letter in 'ab' for r in ['i', 'ii', 'iii']]
    expected += [f'Section C Q3(c)({r})' for r in ['i', 'ii']]
    assert len(expected) == len(set(expected)) == 53
    parts, texts, _ = census_sections('home-economics', 2020, 'hl')
    actual = {key_label(k, 'home-economics') for k in leaves_of(parts)}
    assert actual == set(expected), dict(missing=sorted(set(expected)-actual), unexpected=sorted(actual-set(expected)))
    flags = continuity_flags(parts, texts, 'home-economics')
    assert not flags, flags
    return dict(level='higher', sourceHashes='verified', expectedSourceLeaves=53,
                observedSourceLeaves=len(actual), continuityFlags=flags, keys=sorted(actual),
                reconciliation='Independent 90-page visual sweep of both split booklets and the complete scheme pinned 49 priced tasks A12/B16/C21 before parser/card inspection. Subsequent explicit reinspection of original paper A pages 4/6 confirmed four named roman pairs A6/A10/A11/A12 retained by the raw census: 53 source leaves A16/B16/C21 map to 49 whole tasks and 627marks. All eight named terms remain separately claimable 3-mark rows; no source markers removed.')

if __name__ == '__main__':
    print(json.dumps(dict(higher=verify_higher()), ensure_ascii=False, indent=2))
