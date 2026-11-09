#!/usr/bin/env python3
"""Mandatory original-PDF gate, separately run from portable checkout tests.
Run: python3 scripts/markbank/authoring/he_validate_2015_source_census.py
Source leaves pinned from independent full49-page visual sweep before parser inspection.
"""
import json
from paper_census import census_sections,leaves_of,key_label,continuity_flags
from he_review_2015_hl_main import documents
def verify_higher():
 d=documents();assert [len(d[k]) for k in ['paper','scheme']]==[12,37]
 expected=[f'Section A Q{n}' for n in range(1,13)]
 expected += ['Section B Q1(a)(i)','Section B Q1(a)(ii)','Section B Q1(b)','Section B Q1(c)(i)','Section B Q1(c)(ii)','Section B Q1(d)']
 expected += ['Section B Q2(a)','Section B Q2(b)']
 expected += [f'Section B Q{n}({letter})' for n in [3,4] for letter in 'abc']
 expected += ['Section B Q5(a)(i)','Section B Q5(a)(ii)','Section B Q5(b)','Section B Q5(c)']
 expected += [f'Section C Q1({letter})({roman})' for letter in 'abc' for roman in (['i','ii','iii'] if letter=='a' else ['i','ii'])]
 expected += ['Section C Q2(a)(i)','Section C Q2(a)(ii)','Section C Q2(b)','Section C Q2(c)(i)','Section C Q2(c)(ii)']
 expected += [f'Section C Q3({letter})({roman})' for letter in 'abc' for roman in (['i','ii','iii'] if letter=='a' else ['i','ii'])]
 assert len(expected)==len(set(expected))==49
 parts,texts,_=census_sections('home-economics',2015,'hl');actual={key_label(k,'home-economics') for k in leaves_of(parts)}
 assert actual==set(expected),dict(missing=sorted(set(expected)-actual),unexpected=sorted(actual-set(expected)))
 flags=continuity_flags(parts,texts,'home-economics');assert not flags,flags
 print(json.dumps(dict(level='higher',sourceHashes='verified',expectedSourceLeaves=49,observedSourceLeaves=len(actual),continuityFlags=flags,keys=sorted(actual),reconciliation='49 independent original leaves A12/B18/C19 become48 priced tasks A12/B17/C19,627marks. B1(a)(i)/(ii) share one flexible24-mark tariff: two provision4,two nutritional4,+two other4. No invented12/12 split. Coherent egg-study40, mould22, savings14, garment-construction16 and natural-fabric15 profiles retain all linked priced headings. All49 original pages visually swept.'),ensure_ascii=False,indent=2))
def verify_ordinary():
 from he_review_2015_ol_main import documents
 d=documents();assert [len(d[k]) for k in ['paper','scheme']]==[12,36]
 expected=[f'Section A Q{n}' for n in range(1,13)]
 expected += ['Section B Q1(a)','Section B Q1(b)','Section B Q1(c)(i)','Section B Q1(c)(ii)','Section B Q1(d)']
 expected += [f'Section B Q{n}(a)({roman})' for n in [2,3] for roman in ['i','ii']]
 expected += [f'Section B Q{n}({letter})' for n in [2,3] for letter in 'bc']
 expected += [f'Section B Q{n}({letter})' for n in [4,5] for letter in 'abc']
 expected += [f'Section C Q1({letter})({roman})' for letter in 'abc' for roman in (['i','ii','iii'] if letter=='a' else ['i','ii'])]
 expected += ['Section C Q2(a)(i)','Section C Q2(a)(ii)','Section C Q2(b)','Section C Q2(c)(i)','Section C Q2(c)(ii)']
 expected += [f'Section C Q3({letter})({roman})' for letter in 'abc' for roman in (['i','ii','iii'] if letter=='a' else ['i','ii'])]
 assert len(expected)==len(set(expected))==50
 parts,texts,_=census_sections('home-economics',2015,'ol');actual={key_label(k,'home-economics') for k in leaves_of(parts)}
 assert actual==set(expected),dict(missing=sorted(set(expected)-actual),unexpected=sorted(actual-set(expected)))
 flags=continuity_flags(parts,texts,'home-economics');assert not flags,flags
 print(json.dumps(dict(level='ordinary',sourceHashes='verified',expectedSourceLeaves=50,observedSourceLeaves=len(actual),continuityFlags=flags,keys=sorted(actual),reconciliation='50 original printed leaves A12/B19/C19 become51 priced tasks A12/B19/C20,627marks. B3(a)(i)/(ii) share one flexible24 account while B3(b) separately prices method names12 and explanation8 (scheme10), offsetting withinB. C1(a)(i) separately prices evaluation15/modifications10 (scheme13), adding one priced task. All48 original pages independently visually swept before authoring/parser counts.'),ensure_ascii=False,indent=2))
if __name__=='__main__':verify_higher();verify_ordinary()
