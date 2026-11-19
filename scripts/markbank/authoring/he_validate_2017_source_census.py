#!/usr/bin/env python3
"""Mandatory raw-source authoring gate; normal runtime tests remain portable.
Run: python3 scripts/markbank/authoring/he_validate_2017_source_census.py
Higher 48 and Ordinary 52 original leaves were pinned before parser inspection
by independent 52-page and 44-page visual sweeps respectively.
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
 return dict(level='higher',sourceHashes='verified',expectedSourceLeaves=48,observedSourceLeaves=len(actual),continuityFlags=flags,keys=sorted(actual),reconciliation='48 independently reviewed original leaves A12/B17/C19 map to 48 priced tasks, 627 marks. Whole-six A questions keep all companion asks without invented allocations. C1(a)(i) evaluation/modification share four5 points; C1(c)(ii) required natural/artificial profiles share18; C2(b) is one blended-fabric profile15. All52 original pages swept and manual ledger saved before parser/author inspection.')

def verify_ordinary():
 from he_review_2017_ol_main import documents as ordinary_documents
 d=ordinary_documents();assert [len(d[k]) for k in ['paper','scheme']]==[12,32]
 expected=[f'Section A Q{n}' for n in range(1,13)]
 expected += [f'Section B Q1(a)({r})' for r in ['i','ii']]+[f'Section B Q1({l})' for l in 'bcd']
 expected += [f'Section B Q2(a)({r})' for r in ['i','ii']]+['Section B Q2(b)','Section B Q2(c)']
 expected += [f'Section B Q3({l})({r})' for l in 'ab' for r in ['i','ii']]+['Section B Q3(c)']
 expected += [f'Section B Q{n}({l})' for n in [4,5] for l in 'abc']
 expected += [f'Section C Q{n}({l})({r})' for n in [1,3] for l in 'abc' for r in (['i','ii','iii'] if l=='a' else ['i','ii'])]
 expected += [f'Section C Q2({l})({r})' for l in 'abc' for r in ['i','ii']]
 assert len(expected)==len(set(expected))==52
 parts,texts,_=census_sections('home-economics',2017,'ol');actual={key_label(k,'home-economics') for k in leaves_of(parts)}
 assert actual==set(expected),dict(missing=sorted(set(expected)-actual),unexpected=sorted(actual-set(expected)))
 flags=continuity_flags(parts,texts,'home-economics');assert not flags,flags
 return dict(level='ordinary',sourceHashes='verified',expectedSourceLeaves=52,observedSourceLeaves=len(actual),continuityFlags=flags,keys=sorted(actual),reconciliation='52 original leaves A12/B20/C20 reconcile to 52 priced tasks A12/B19/C21, 627 marks. Equal totals are coincidental: B3(a)(i)/(ii) share one four-point 20-mark tariff without a 10/10 split; C3(a)(i) has separately printed poverty-definition 6 and relative/absolute-poverty 12 asks. B2(a) roman tasks explicitly 8/12; B3(b) roman tasks explicitly 8/8. All 44 original pages independently swept and manual ledger saved before parser/card inspection.')
if __name__=='__main__':print(json.dumps(dict(higher=verify_higher(),ordinary=verify_ordinary()),ensure_ascii=False,indent=2))
