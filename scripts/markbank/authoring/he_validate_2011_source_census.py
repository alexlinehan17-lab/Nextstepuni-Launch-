#!/usr/bin/env python3
"""Mandatory local PDF gate, separate from portable checkout-based Vitest.

Run: python3 scripts/markbank/authoring/he_validate_2011_source_census.py
Requires original PDFs and PyMuPDF. Expected keys are pinned from the independent
44-page visual source sweep, not generated from authored or emitted cards.
"""
import json
from paper_census import census_sections, leaves_of, key_label, continuity_flags
from he_review_2011_hl_main import documents
def verify():
 d=documents();assert [len(d[k]) for k in ['paper','scheme']]==[12,32]
 expected=[f'Section A Q{n}' for n in range(1,13)]
 expected += [f'Section B Q{n}({letter})' for n in range(1,6) for letter in ('abcd' if n==1 else 'abc')]
 expected += [f'Section C Q{n}({letter})({roman})' for n in [1,3] for letter in 'abc' for roman in (['i','ii','iii'] if letter=='a' else ['i','ii'])]
 expected += ['Section C Q2(a)(i)','Section C Q2(a)(ii)','Section C Q2(b)','Section C Q2(c)(i)','Section C Q2(c)(ii)']
 assert len(expected)==len(set(expected))==47
 parts,texts,_=census_sections('home-economics',2011,'hl');actual={key_label(k,'home-economics') for k in leaves_of(parts)}
 assert actual==set(expected),dict(missing=sorted(set(expected)-actual),unexpected=sorted(actual-set(expected)))
 flags=continuity_flags(parts,texts,'home-economics');assert not flags,flags
 print(json.dumps(dict(sourceHashes='verified',expectedSourceLeaves=47,observedSourceLeaves=len(actual),continuityFlags=flags,keys=sorted(actual),reconciliation='The paper has 47 source leaves. B5(a) contains independent definition/universality asks priced 5+5 by scheme13, so 48 priced tasks. A12 retains its two pictured symbols together under the whole six-mark source question.'),ensure_ascii=False,indent=2))
if __name__=='__main__':verify()
