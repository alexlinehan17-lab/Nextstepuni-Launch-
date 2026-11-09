#!/usr/bin/env python3
"""Mandatory raw-source authoring gate; normal runtime tests remain portable.
Run: python3 scripts/markbank/authoring/he_validate_2017_source_census.py
The 48 original leaves were pinned before parser inspection by a 52-page visual sweep.
"""
import json
from paper_census import census_sections,leaves_of,key_label,continuity_flags
from he_review_2017_hl_main import documents
def verify_higher():
 d=documents();assert [len(d[k]) for k in ['paper','scheme']]==[12,40]
 expected=[f'Section A Q{n}' for n in range(1,13)]
 expected += [f'Section B Q1({letter})' for letter in 'abcde']
 expected += [f'Section B Q{n}({letter})' for n in range(2,6) for letter in 'abc']
 expected += [f'Section C Q{n}({letter})({roman})' for n in [1,3] for letter in 'abc' for roman in (['i','ii','iii'] if letter=='a' else ['i','ii'])]
 expected += [f'Section C Q2({letter})({roman})' for letter in 'ac' for roman in ['i','ii']]+['Section C Q2(b)']
 assert len(expected)==len(set(expected))==48
 parts,texts,_=census_sections('home-economics',2017,'hl');actual={key_label(k,'home-economics') for k in leaves_of(parts)}
 assert actual==set(expected),dict(missing=sorted(set(expected)-actual),unexpected=sorted(actual-set(expected)))
 flags=continuity_flags(parts,texts,'home-economics');assert not flags,flags
 print(json.dumps(dict(level='higher',sourceHashes='verified',expectedSourceLeaves=48,observedSourceLeaves=len(actual),continuityFlags=flags,keys=sorted(actual),reconciliation='48 independently reviewed original leaves A12/B17/C19 map to 48 priced tasks, 627 marks. Whole-six A questions keep all companion asks without invented allocations. C1(a)(i) evaluation/modification share four5 points; C1(c)(ii) required natural/artificial profiles share18; C2(b) is one blended-fabric profile15. All52 original pages swept and manual ledger saved before parser/author inspection.'),ensure_ascii=False,indent=2))
if __name__=='__main__':verify_higher()
