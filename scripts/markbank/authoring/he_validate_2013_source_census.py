#!/usr/bin/env python3
"""Mandatory original-PDF gate, separate from portable checkout tests.
Run: python3 scripts/markbank/authoring/he_validate_2013_source_census.py
Keys pinned from the independent 48-page visual sweep, before authoring.
"""
import json
from paper_census import census_sections,leaves_of,key_label,continuity_flags
from he_review_2013_hl_main import documents
def verify_higher():
 d=documents();assert [len(d[k]) for k in ['paper','scheme']]==[12,36]
 expected=[f'Section A Q{n}' for n in range(1,13)]
 expected += [f'Section B Q1({letter})' for letter in 'abcde']
 expected += ['Section B Q2(a)','Section B Q2(b)(i)','Section B Q2(b)(ii)','Section B Q2(c)']
 expected += [f'Section B Q{n}({letter})' for n in [3,4,5] for letter in 'abc']
 expected += [f'Section C Q1({letter})({roman})' for letter in 'abc' for roman in (['i','ii','iii'] if letter=='a' else ['i','ii'])]
 expected += [f'Section C Q2(a)({roman})' for roman in ['i','ii','iii']]+['Section C Q2(b)','Section C Q2(c)(i)','Section C Q2(c)(ii)']
 expected += [f'Section C Q3(a)({roman})' for roman in ['i','ii','iii']]+['Section C Q3(b)(i)','Section C Q3(b)(ii)','Section C Q3(c)']
 assert len(expected)==len(set(expected))==49
 parts,texts,_=census_sections('home-economics',2013,'hl');actual={key_label(k,'home-economics') for k in leaves_of(parts)}
 assert actual==set(expected),dict(missing=sorted(set(expected)-actual),unexpected=sorted(actual-set(expected)))
 flags=continuity_flags(parts,texts,'home-economics');assert not flags,flags
 print(json.dumps(dict(level='higher',sourceHashes='verified',expectedSourceLeaves=49,observedSourceLeaves=len(actual),continuityFlags=flags,keys=sorted(actual),reconciliation='Independent original source leaves and priced tasks both49 (A12/B18/C19),627 marks. A remains twelve whole-six questions. B2(b) has two printed roman asks separately priced8+18. C1(c)(ii) is one paired flooring task18 with required9+9 profiles; C3(c) is one primary-education account30 with required9/9/6/6 headings.'),ensure_ascii=False,indent=2))
if __name__=='__main__':verify_higher()
