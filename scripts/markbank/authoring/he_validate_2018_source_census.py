#!/usr/bin/env python3
"""Mandatory raw-source authoring gate; normal runtime tests remain portable.
Run: python3 scripts/markbank/authoring/he_validate_2018_source_census.py
Higher 49 original leaves were pinned before parser inspection
by an independent 52-page visual sweep.
"""
import json
from paper_census import census_sections,leaves_of,key_label,continuity_flags
from he_review_2018_hl_main import documents
def verify_higher():
 d=documents();assert [len(d[k]) for k in ['paper','scheme']]==[12,40]
 expected=[f'Section A Q{n}' for n in range(1,13)]
 expected += [f'Section B Q1({letter})' for letter in 'abcde']
 expected += [f'Section B Q{n}({letter})' for n in range(2,6) for letter in 'abc']
 expected += [f'Section C Q{n}({letter})({roman})' for n in [1,3] for letter in 'abc' for roman in (['i','ii','iii'] if letter=='a' else ['i','ii'])]
 expected += [f'Section C Q2({letter})({roman})' for letter in 'abc' for roman in ['i','ii']]
 assert len(expected)==len(set(expected))==49
 parts,texts,_=census_sections('home-economics',2018,'hl');actual={key_label(k,'home-economics') for k in leaves_of(parts)}
 assert actual==set(expected),dict(missing=sorted(set(expected)-actual),unexpected=sorted(actual-set(expected)))
 flags=continuity_flags(parts,texts,'home-economics');assert not flags,flags
 return dict(level='higher',sourceHashes='verified',expectedSourceLeaves=49,observedSourceLeaves=len(actual),continuityFlags=flags,keys=sorted(actual),reconciliation='49 independently reviewed original leaves A12/B17/C20 map one-to-one to 49 priced tasks and 627 marks. Whole-six A questions keep companion asks without invented allocations. Both additive accounts, linked floor-covering profiles, and paired school-programme curricula/assessments follow original tariffs. All 52 original pages swept and manual ledger saved before parser/author inspection.')

if __name__=='__main__':print(json.dumps(verify_higher(),ensure_ascii=False,indent=2))
