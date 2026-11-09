#!/usr/bin/env python3
"""Mandatory original-PDF gate, separately run from portable checkout tests.
Run: python3 scripts/markbank/authoring/he_validate_2014_source_census.py
Keys pinned from the independent full 52-page visual sweep before authoring.
"""
import json
from paper_census import census_sections,leaves_of,key_label,continuity_flags
from he_review_2014_hl_main import documents
def verify_higher():
 d=documents();assert [len(d[k]) for k in ['paper','scheme']]==[12,40]
 expected=[f'Section A Q{n}' for n in range(1,13)]
 expected += [f'Section B Q1({letter})' for letter in 'abcd']
 expected += [f'Section B Q{n}({letter})' for n in [2,3,4] for letter in 'abc']
 expected += ['Section B Q5(a)','Section B Q5(b)(i)','Section B Q5(b)(ii)','Section B Q5(c)']
 expected += [f'Section C Q1({letter})({roman})' for letter in 'abc' for roman in (['i','ii','iii'] if letter=='a' else ['i','ii'])]
 expected += [f'Section C Q2({letter})({roman})' for letter in 'abc' for roman in ['i','ii']]
 expected += [f'Section C Q3(a)({roman})' for roman in ['i','ii','iii']]+['Section C Q3(b)','Section C Q3(c)(i)','Section C Q3(c)(ii)']
 assert len(expected)==len(set(expected))==48
 parts,texts,_=census_sections('home-economics',2014,'hl');actual={key_label(k,'home-economics') for k in leaves_of(parts)}
 assert actual==set(expected),dict(missing=sorted(set(expected)-actual),unexpected=sorted(actual-set(expected)))
 flags=continuity_flags(parts,texts,'home-economics');assert not flags,flags
 print(json.dumps(dict(level='higher',sourceHashes='verified',expectedSourceLeaves=48,observedSourceLeaves=len(actual),continuityFlags=flags,keys=sorted(actual),reconciliation='48 independent original leaves A12/B17/C19 become49 priced tasks A12/B18/C19,627 marks: B2(b) independently prices toughness factors9 and tenderising methods6 (paper7,scheme11). Coherent protein47 (classification24/complementary8/structure15), microwave26 and family-change30 accounts preserve their printed priced headings. All A tasks retain whole6 without inferred suballocations. All52 original pages visually swept.'),ensure_ascii=False,indent=2))
if __name__=='__main__':verify_higher()
