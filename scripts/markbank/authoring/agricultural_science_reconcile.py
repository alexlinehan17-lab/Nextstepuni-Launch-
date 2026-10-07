#!/usr/bin/env python3
"""Exact reconciliation of the independently reviewed Agricultural Science scope.

Default exit status remains nonzero until EVERY indexed edition is audited.
--check-reviewed validates only the explicitly reviewed batch. It is not a
corpus completion gate. The generic parser is retained for unaudited leads.
"""
import argparse
import collections
import json
import re
from pathlib import Path

from agricultural_science_census import ROOT, build
from reconcile import shipped_cards

OUTPUT = ROOT / 'scripts/markbank/authored/agricultural-science-reconciliation.json'


def reconcile():
    census = build()
    shipped = shipped_cards('agricultural-science')
    refs = collections.defaultdict(list)
    for cid,ref in shipped:
        refs[ref].append(cid)
    marks = {}
    for level in ['higher','ordinary']:
        source = (ROOT / f'components/MarkBank/cards/agricultural-science/{level}.ts').read_text()
        for chunk in re.split(r'^\s*\.\.\.base,',source,flags=re.M)[1:]:
            cid = re.search(r'\bid: "([^"]+)"',chunk)
            tariff = re.search(r'\btotalMarks: (\d+)',chunk)
            assert cid and tariff, 'Deck emitter changed: re-review the reader'
            assert cid[1] not in marks, f'Duplicate shipped card: {cid[1]}'
            marks[cid[1]] = int(tariff[1])
    assert set(marks)=={cid for cid,_ in shipped}
    atlas = json.loads((ROOT / 'data/examTopics/agricultural-science-question-runtime.json').read_text())
    issues, papers = [], []
    checked = 0
    for paper in census['papers']:
        tag = 'HL' if paper['level']=='higher' else 'OL'
        prefix = f'{paper["year"]} {tag} '
        expected = {ref:task['marksPerResponse'] for task in paper['baseTasks'] for ref in task['routes']}
        actual = {ref for _,ref in shipped if ref.startswith(prefix)}
        for ref in sorted(actual-expected.keys()):
            issues.append(f'Unmatched reviewed-sitting card: {ref}')
        for ref,tariff in expected.items():
            ids = refs[ref]
            if len(ids)!=1:
                issues.append(f'Expected exactly one card for {ref}: {ids}')
                continue
            cid = ids[0]
            if marks[cid]!=tariff:
                issues.append(f'Marks differ for {ref}: shipped {marks[cid]}, source {tariff}')
            editions = [('ev','markBankCards')]
            if paper['year']==2010 or (paper['year']==2011 and paper['level']=='higher'):
                editions.append(('iv','translatedMarkBankCards'))
            for lang,field in editions:
                joins = [j for j in atlas[field] if j['cardId']==cid]
                if len(joins)!=1:
                    issues.append(f'Expected one {lang} Atlas binding for {ref}: {len(joins)}')
                    continue
                join = joins[0]
                fileid = paper['paperFileid'].replace('EV.pdf',f'{lang.upper()}.pdf')
                if join['year']!=paper['year'] or join['fileid']!=fileid:
                    issues.append(f'Wrong source edition: {ref} {lang}')
                # Independently observed Irish printed exceptions, not values
                # copied from the authoring or review ledgers.
                expected_marks = 20 if lang=='iv' and ref in ['2010 OL Q9(f)','2010 OL Q12(d)(ii)'] else tariff
                if lang=='iv' and join['marksPerRoute']!=expected_marks:
                    issues.append(f'Wrong translated tariff: {ref}')
                path = ROOT / f'public/paper-answers/{join["year"]}/{join["fileid"]}.json'
                answer_map = json.loads(path.read_text())
                anchors = [q for q in answer_map['q'] if q['n']==join['n']]
                if len(anchors)!=1 or not anchors[0].get('paperRegion') or not anchors[0].get('region'):
                    issues.append(f'Missing source crops: {ref} {lang}')
            checked += 1
        papers.append({'year':paper['year'],'level':paper['level'],'expectedRoutes':len(expected),
                       'shippedRoutes':len(actual),'missing':sorted(expected.keys()-actual),
                       'unmatched':sorted(actual-expected.keys())})
    pending = [p for p in census['editionStatus'] if p['independentCensus']=='open']
    return {'status':'in-progress' if issues or pending else 'complete',
            'shippedCardCount':len(shipped),'reviewedRoutesChecked':checked,
            'reviewedBatchIssues':issues,'papers':papers,
            'independentCensusEditionsOpen':pending,
            'limitation':'2010 Higher/Ordinary and 2011 Higher English boundaries and all 217 corresponding Atlas bindings reconciled exactly, plus 217 translated bindings. Remaining sitting boundaries and independent Irish censuses remain open. This partial result cannot establish corpus completeness.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write',action='store_true')
    parser.add_argument('--check-reviewed',action='store_true')
    args = parser.parse_args()
    result = reconcile()
    if args.write:
        OUTPUT.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(f'{result["reviewedRoutesChecked"]} reviewed routes; {len(result["reviewedBatchIssues"])} reviewed-batch issues; '
          f'{len(result["independentCensusEditionsOpen"])} editions still need an independent census.')
    if result['reviewedBatchIssues']:
        print('\n'.join(result['reviewedBatchIssues']))
    return bool(result['reviewedBatchIssues']) or (not args.check_reviewed and result['status']!='complete')


if __name__=='__main__':
    raise SystemExit(main())
