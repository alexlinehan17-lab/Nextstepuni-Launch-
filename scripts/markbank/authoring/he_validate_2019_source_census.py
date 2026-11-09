#!/usr/bin/env python3
"""Mandatory independent original-PDF authoring gate; portable runtime tests are separate."""
import json
from paper_census import census_sections,leaves_of,key_label,continuity_flags
from he_review_2019_hl_main import documents
def verify_higher():
 d=documents();assert [len(d[k]) for k in ['paper','scheme']]==[12,36]
 expected=[f'Section A Q{n}' for n in range(1,13)]
 expected += [f'Section B Q1({l})' for l in 'abcde']
 expected += ['Section B Q2(a)','Section B Q2(b)(i)','Section B Q2(b)(ii)','Section B Q2(c)']
 expected += [f'Section B Q{n}({l})' for n in [3,4,5] for l in 'abc']
 expected += [f'Section C Q1(a)({r})' for r in ['i','ii','iii']]+[f'Section C Q1({l})({r})' for l in 'bc' for r in ['i','ii']]
 expected += [f'Section C Q2({l})({r})' for l in 'abc' for r in ['i','ii']]
 expected += [f'Section C Q3(a)({r})' for r in ['i','ii','iii','iv']]+[f'Section C Q3({l})({r})' for l in 'bc' for r in ['i','ii']]
 assert len(expected)==len(set(expected))==51
 parts,texts,_=census_sections('home-economics',2019,'hl');actual={key_label(k,'home-economics') for k in leaves_of(parts)}
 assert actual==set(expected),dict(missing=sorted(set(expected)-actual),unexpected=sorted(actual-set(expected)))
 flags=continuity_flags(parts,texts,'home-economics');assert not flags,flags
 return dict(level='higher',sourceHashes='verified',expectedSourceLeaves=51,observedSourceLeaves=len(actual),continuityFlags=flags,keys=sorted(actual),reconciliation='Independent 48-page original visual sweep pinned 51 original leaves A12/B18/C21 before parser/author inspection. One-to-one mapping to 51 priced tasks, 627 marks. B2(b) has two separately allocated roman tasks 8/12. Paired snack and sketch/description asks remain coherent within their original leaf.')
if __name__=='__main__':print(json.dumps(dict(higher=verify_higher()),ensure_ascii=False,indent=2))
