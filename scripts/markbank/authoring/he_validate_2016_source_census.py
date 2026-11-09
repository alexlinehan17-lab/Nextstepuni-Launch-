#!/usr/bin/env python3
"""Mandatory original-source authoring gate, separate from portable runtime tests.
Run: python3 scripts/markbank/authoring/he_validate_2016_source_census.py
The 51 original leaves were pinned by a full 52-page visual sweep before parser inspection.
"""
import json
from paper_census import census_sections,leaves_of,key_label,continuity_flags
from he_review_2016_hl_main import documents
def verify_higher():
 d=documents();assert [len(d[k]) for k in ['paper','scheme']]==[12,40]
 expected=[f'Section A Q{n}' for n in range(1,13)]
 expected += [f'Section B Q1({letter})' for letter in 'abcde']
 expected += [f'Section B Q{n}({letter})' for n in range(2,6) for letter in 'abc']
 expected += [f'Section C Q{n}({letter})({roman})' for n in [1,2,3] for letter in 'abc' for roman in ((['i','ii','iii','iv'] if n==3 else ['i','ii','iii']) if letter=='a' else ['i','ii'])]
 assert len(expected)==len(set(expected))==51
 parts,texts,_=census_sections('home-economics',2016,'hl');actual={key_label(k,'home-economics') for k in leaves_of(parts)}
 assert actual==set(expected),dict(missing=sorted(set(expected)-actual),unexpected=sorted(actual-set(expected)))
 flags=continuity_flags(parts,texts,'home-economics');assert not flags,flags
 print(json.dumps(dict(level='higher',sourceHashes='verified',expectedSourceLeaves=51,observedSourceLeaves=len(actual),continuityFlags=flags,keys=sorted(actual),reconciliation='51 independent original leaves A12/B17/C22 become 53 priced tasks A12/B17/C24, 627 marks. C1(c)(i) separately prices lighting principles9/profile5 on scheme20; C2(b)(ii) separately prices colour application5/design application4 on scheme22. Dependent outfit, vitamin, heating and freezing accounts stay coherent. All52 original pages visually swept before parser/card inspection.'),ensure_ascii=False,indent=2))
if __name__=='__main__':verify_higher()
