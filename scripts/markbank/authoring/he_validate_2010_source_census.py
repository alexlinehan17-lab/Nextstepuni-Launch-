#!/usr/bin/env python3
"""Mandatory local source gate for both independently swept 2010 HE sittings.

Run before a 2010 content checkpoint:
    python3 scripts/markbank/authoring/he_validate_2010_source_census.py

This gate requires the original local PDF corpus and PyMuPDF. The ordinary
checkout-based Vitest suite deliberately has no dependency on that archive.
Expected source keys below were pinned from the visual paper census, separately
from the authored card manifest. Do not derive them from emitted cards.
"""
import json
from paper_census import census_sections, leaves_of, key_label, continuity_flags
from he_review_2010_hl_main import documents as higher_documents
from he_review_2010_ol_main import documents as ordinary_documents

def verify():
 higher_documents();ordinary_documents()  # original source SHA256 guards
 common_b=[f'Section B Q{n}({l})' for n in [2,3,4,5] for l in 'abc']
 common_c1=[f'Section C Q1({l})({r})' for l in 'abc' for r in (['i','ii','iii'] if l=='a' else ['i','ii'])]
 higher=[f'Section A Q{n}' for n in range(1,13) if n!=5]+['Section A Q5(i)','Section A Q5(ii)']
 higher+=['Section B Q1(a)(i)','Section B Q1(a)(ii)']+[f'Section B Q1({l})' for l in 'bcd']+common_b+common_c1
 higher += [f'Section C Q2(a)({r})' for r in ['i','ii','iii']]+['Section C Q2(b)','Section C Q2(c)(i)','Section C Q2(c)(ii)']
 higher += [f'Section C Q3({l})({r})' for l in 'abc' for r in (['i','ii','iii'] if l=='a' else ['i','ii'])]
 ordinary=[f'Section A Q{n}' for n in range(1,13)]+[f'Section B Q1({l})' for l in 'abcd']+common_b+common_c1
 ordinary += [f'Section C Q2({l})({r})' for l in 'ab' for r in ['i','ii']]+['Section C Q2(c)']
 ordinary += [f'Section C Q3(a)({r})' for r in ['i','ii','iii']]+['Section C Q3(b)(i)','Section C Q3(b)(ii)','Section C Q3(c)']
 result={}
 for level,expected,count in [('hl',higher,50),('ol',ordinary,46)]:
  assert len(expected)==len(set(expected))==count
  parts,texts,_=census_sections('home-economics',2010,level)
  actual={key_label(k,'home-economics') for k in leaves_of(parts)}
  assert actual==set(expected),dict(level=level,missing=sorted(set(expected)-actual),unexpected=sorted(actual-set(expected)))
  flags=continuity_flags(parts,texts,'home-economics');assert not flags,(level,flags)
  result[level]=dict(sourceHashes='verified',expectedSourceLeaves=count,observedSourceLeaves=len(actual),continuityFlags=flags,keys=sorted(actual))
 print(json.dumps(result,ensure_ascii=False,indent=2))
if __name__=='__main__':verify()
