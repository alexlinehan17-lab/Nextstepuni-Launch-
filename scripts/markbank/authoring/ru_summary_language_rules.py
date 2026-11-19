"""Source-reviewed manual discretion exceptions for named Russian summary tasks.

Only these explicitly reviewed original sittings are covered. Existing language
flags and content adjustments remain active; no language threshold is invented.
"""
import hashlib,re
from pathlib import Path
import fitz
ROOT=Path(__file__).resolve().parents[3]
SOURCES = {2013: {'page': 6, 'sha256': 'b14c59425b38ee71743c5b59b119baad4071759692f069d143abc421b5ac4b6d'},
 2014: {'page': 6, 'sha256': 'fb5cfc36f2f64fc1a8fc068bbad392ff99eb2ff5792c37267dfcabc0d0ad1f48'},
 2015: {'page': 7, 'sha256': '210b81b664cfac3107aed4c750d839c70c82777d40b92c805f7f5db60d1c730c'},
 2016: {'page': 6, 'sha256': 'ec7771b35c2c806b9e0f2cc8a35626cd3a8e85a9c991afc8089f4319decc19e4'},
 2017: {'page': 6, 'sha256': '4436cf9e87767e3d7092bedbb38ad8818b731d232565d2d0fca1976621e95abd'},
 2022: {'page': 7, 'sha256': '7f539dcb7b70c18e30b1047e463426bd2715926ddfe16a6daa0a93b995907071'},
 2023: {'page': 7, 'sha256': '63933208c9846387f93bba3f48c13ec4d8821d7f3af1597998bcc8c531d983de'},
 2024: {'page': 8, 'sha256': '3fd5f06ee6dbc78e1ef53bcaa1e1e6f9a6d822c6ee898a69f16ec34cf0aac999'},
 2025: {'page': 7, 'sha256': '3c74de1d1d5d35a4e0e9ada2b5e7754446722444003f480a2bd876c90c27a52b'},
 2026: {'page': 7, 'sha256': 'e56810faf2cb2b34e30216c07b4ff771d1cc6f99b91fb6fcf1d47d045d8265be'}}

def attach_reviewed_summary_language_exceptions(cards):
    by_id={card['id']:card for card in cards}
    assert len(by_id)==len(cards)
    for year,source in SOURCES.items():
        identifiers=[f'ru-{year}-hl-c2-{number}' for number in range(1,5)]
        present=[identifier for identifier in identifiers if identifier in by_id]
        if not present:continue
        assert present==identifiers,('Incomplete reviewed summary batch',year,present)
        path=ROOT/f'examiner-reports/russian/schemes/{year}-hl.pdf'
        assert hashlib.sha256(path.read_bytes()).hexdigest()==source['sha256'],year
        with fitz.open(path) as document:
            page=document[source['page']-1].get_text()
        match=re.search(r'Discretionary\s+marks(?:\s*\(as\s+opposed\s+to\s+content\s+marks\))?\s+may\s+be\s+awarded[\s\S]*?answers\s*\)\s*\.',page)
        assert match,year
        clause=' '.join(match.group().split())
        for identifier in identifiers:
            card=by_id[identifier];assert card['subjectId']=='russian' and card['year']==year and card['level']=='higher' and card['section']=='C2',identifier
            assert card['rubric']['system']=='language-points',identifier
            criteria=card['rubric'].get('criteria',[])
            matches=[criterion for criterion in criteria if criterion['id']=='summary-skills']
            assert len(matches)==1 and matches[0].get('kind')!='deduction',identifier
            normal=lambda text:re.sub(r'[^\w]','',text.casefold())
            assert normal(clause) in normal(' '.join(matches[0]['guidance'])),identifier
            rule=card['answerLanguageRule'];assert rule['otherLanguageMultiplier']==0,identifier
            rule['manualCriterionExceptions']={'criterionIds':['summary-skills'],'sourceText':clause,'schemePages':[source['page']]}
    return cards


def main():
    """Regenerate only the reviewed exception metadata, preserving every other field."""
    import copy
    import json
    path = ROOT / 'scripts/markbank/authored/russian-reviewed.json'
    previous = json.loads(path.read_text())
    cards = attach_reviewed_summary_language_exceptions(copy.deepcopy(previous))
    expected = {f'ru-{year}-hl-c2-{number}' for year in SOURCES for number in range(1, 5)}
    changed = []
    for before, after in zip(previous, cards):
        if before == after:
            continue
        assert before['id'] == after['id'] and after['id'] in expected, after['id']
        original = copy.deepcopy(before)
        corrected = copy.deepcopy(after)
        original['answerLanguageRule'].pop('manualCriterionExceptions', None)
        corrected['answerLanguageRule'].pop('manualCriterionExceptions', None)
        assert original == corrected, after['id']
        changed.append(after['id'])
    assert expected <= {card['id'] for card in cards}
    path.write_text(json.dumps(cards, ensure_ascii=False, indent=2) + '\n')
    print(f'{len(expected)} reviewed summary exceptions regenerated; {len(changed)} metadata changes; all other authored fields preserved.')


if __name__ == '__main__':
    main()
