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

def verify_ordinary():
    from he_review_2020_ol_main import documents as ordinary_documents
    d = ordinary_documents()
    assert [len(d[k]) for k in ['a', 'bc', 'scheme']] == [32, 8, 38]
    expected = [f'Section A Q{n}' for n in range(1, 13) if n != 2]
    expected += [f'Section A Q2({r})' for r in ['i', 'ii']]
    expected += [f'Section B Q1(a)({r})' for r in ['i', 'ii']]
    expected += [f'Section B Q1({letter})' for letter in 'bcd']
    expected += [f'Section B Q{n}(a)({r})' for n in [2, 3, 5] for r in ['i', 'ii']]
    expected += [f'Section B Q{n}({letter})' for n in [2, 3, 5] for letter in 'bc']
    expected += [f'Section B Q4({letter})' for letter in 'abc']
    expected += [f'Section C Q{n}(a)({r})' for n in [1, 3] for r in ['i', 'ii', 'iii', 'iv']]
    expected += [f'Section C Q{n}({letter})({r})' for n in [1, 3] for letter in 'bc' for r in ['i', 'ii']]
    expected += [f'Section C Q2({letter})({r})' for letter in 'abc' for r in ['i', 'ii']]
    assert len(expected) == len(set(expected)) == 55
    parts, texts, _ = census_sections('home-economics', 2020, 'ol')
    actual = {key_label(k, 'home-economics') for k in leaves_of(parts)}
    assert actual == set(expected), dict(missing=sorted(set(expected)-actual), unexpected=sorted(actual-set(expected)))
    flags = continuity_flags(parts, texts, 'home-economics')
    assert not flags, flags
    return dict(level='ordinary', sourceHashes='verified', expectedSourceLeaves=55,
                observedSourceLeaves=len(actual), continuityFlags=flags, keys=sorted(actual),
                reconciliation='Independent 78-page visual sweep and saved manual ledger before parser/card inspection: 55 original leaves A13/B20/C22 map to 56 priced tasks A15/B19/C22, 627 marks. A2 named roman terms remain required 3-mark rows in one task. Three A companion asks are separately printed/priced; B3(a) two named roman leaves share a flexible five-point allocation and stay one whole task. Narrow original B3(a) marker restoration; no source marker removed.')

if __name__ == '__main__':
    print(json.dumps(dict(higher=verify_higher(), ordinary=verify_ordinary()), ensure_ascii=False, indent=2))
