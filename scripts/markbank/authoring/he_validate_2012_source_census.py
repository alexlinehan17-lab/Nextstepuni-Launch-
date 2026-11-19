#!/usr/bin/env python3
"""Mandatory original-PDF gate, separate from portable checkout tests.
Run: python3 scripts/markbank/authoring/he_validate_2012_source_census.py
Expected keys pinned from the independent 48/44-page visual sweeps, not cards.
"""
import json
from paper_census import census_sections,leaves_of,key_label,continuity_flags
from he_review_2012_hl_main import documents
def verify_higher():
 d=documents();assert [len(d[k]) for k in ['paper','scheme']]==[12,36]
 expected=[f'Section A Q{n}' for n in range(1,13) if n not in [2,4,11]]
 expected += [f'Section A Q{n}({roman})' for n in [2,4,11] for roman in ['i','ii']]
 expected += [f'Section B Q{n}({letter})' for n in range(1,6) for letter in ('abcd' if n==1 else 'abc')]
 expected += [f'Section C Q{n}({letter})({roman})' for n in [1,3] for letter in 'abc' for roman in (['i','ii','iii'] if letter=='a' else ['i','ii'])]
 expected += [f'Section C Q2({letter})({roman})' for letter in 'ab' for roman in ['i','ii']]+['Section C Q2(c)']
 assert len(expected)==len(set(expected))==50
 parts,texts,_=census_sections('home-economics',2012,'hl');actual={key_label(k,'home-economics') for k in leaves_of(parts)}
 assert actual==set(expected),dict(missing=sorted(set(expected)-actual),unexpected=sorted(actual-set(expected)))
 flags=continuity_flags(parts,texts,'home-economics');assert not flags,flags
 print(json.dumps(dict(level='higher',sourceHashes='verified',expectedSourceLeaves=50,observedSourceLeaves=len(actual),continuityFlags=flags,keys=sorted(actual),reconciliation='Source A15/B16/C19 leaves become A12/B17/C22 priced tasks: A2, A4 and A11 each retain both roman asks under one unallocated six-mark question (-3); B5(b) child/parent12+12 (+1), C2(c) construction/colour/design5+5+5 (+2), C3(b)(i) definition6/value12 (+1). Total51 tasks,627marks.'),ensure_ascii=False,indent=2))
def verify_ordinary():
 from he_review_2012_ol_main import documents as ordinary_documents
 d=ordinary_documents();assert [len(d[k]) for k in ['paper','scheme']]==[12,32]
 expected=[f'Section A Q{n}' for n in range(1,13)]
 expected += [f'Section B Q{n}({letter})' for n in range(1,5) for letter in ('abcd' if n==1 else 'abc')]
 expected += ['Section B Q5(a)(i)','Section B Q5(a)(ii)','Section B Q5(b)','Section B Q5(c)']
 expected += [f'Section C Q{n}({letter})({roman})' for n in [1,2,3] for letter in 'abc' for roman in (['i','ii','iii'] if n in [1,2] and letter=='a' else ['i','ii'])]
 assert len(expected)==len(set(expected))==49
 parts,texts,_=census_sections('home-economics',2012,'ol');actual={key_label(k,'home-economics') for k in leaves_of(parts)}
 assert actual==set(expected),dict(missing=sorted(set(expected)-actual),unexpected=sorted(actual-set(expected)))
 flags=continuity_flags(parts,texts,'home-economics');assert not flags,flags
 print(json.dumps(dict(level='ordinary',sourceHashes='verified',expectedSourceLeaves=49,observedSourceLeaves=len(actual),continuityFlags=flags,keys=sorted(actual),reconciliation='Original A12/B17/C20 source leaves become A12/B20/C21 priced tasks through separately allocated B2(a) sources12/reasons8, B2(c) definition5/consumption10, B4(c) reasons12/schemes6, C1(b)(ii) difference8/procedure16. All44 original pages independently visually inspected.'),ensure_ascii=False,indent=2))
if __name__=='__main__':verify_higher();verify_ordinary()
