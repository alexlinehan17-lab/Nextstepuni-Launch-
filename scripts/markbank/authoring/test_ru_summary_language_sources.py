"""Mandatory original-page gate for the source-specific manual summary exception."""
import copy,hashlib,importlib,json,unittest
from pathlib import Path
from ru_source_text import open_scheme
from ru_verify_review import verify_manual_criterion_exception_sources
ROOT=Path(__file__).resolve().parents[3]
SOURCES={2013: {'page': 6, 'sha256': 'b14c59425b38ee71743c5b59b119baad4071759692f069d143abc421b5ac4b6d'}, 2014: {'page': 6, 'sha256': 'fb5cfc36f2f64fc1a8fc068bbad392ff99eb2ff5792c37267dfcabc0d0ad1f48'}, 2015: {'page': 7, 'sha256': '210b81b664cfac3107aed4c750d839c70c82777d40b92c805f7f5db60d1c730c'}, 2016: {'page': 6, 'sha256': 'ec7771b35c2c806b9e0f2cc8a35626cd3a8e85a9c991afc8089f4319decc19e4'}, 2017: {'page': 6, 'sha256': '4436cf9e87767e3d7092bedbb38ad8818b731d232565d2d0fca1976621e95abd'}, 2022: {'page': 7, 'sha256': '7f539dcb7b70c18e30b1047e463426bd2715926ddfe16a6daa0a93b995907071'}, 2023: {'page': 7, 'sha256': '63933208c9846387f93bba3f48c13ec4d8821d7f3af1597998bcc8c531d983de'}, 2024: {'page': 8, 'sha256': '3fd5f06ee6dbc78e1ef53bcaa1e1e6f9a6d822c6ee898a69f16ec34cf0aac999'}, 2025: {'page': 7, 'sha256': '3c74de1d1d5d35a4e0e9ada2b5e7754446722444003f480a2bd876c90c27a52b'}, 2026: {'page': 7, 'sha256': 'e56810faf2cb2b34e30216c07b4ff771d1cc6f99b91fb6fcf1d47d045d8265be'}}

class RussianSummaryLanguageOriginals(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cards={c['id']:c for c in json.loads((ROOT/'scripts/markbank/authored/russian-reviewed.json').read_text())}
    def test_all_40_exceptions_are_bound_to_exact_original_pages_and_manual_criteria(self):
        for year,source in SOURCES.items():
            path=ROOT/f'examiner-reports/russian/schemes/{year}-hl.pdf'
            self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(),source['sha256'])
            with open_scheme(year,'hl') as document:
                for number in range(1,5):
                    card=self.cards[f'ru-{year}-hl-c2-{number}']
                    rule=card['answerLanguageRule']['manualCriterionExceptions']
                    self.assertEqual(rule['criterionIds'],['summary-skills'])
                    self.assertEqual(rule['schemePages'],[source['page']])
                    verify_manual_criterion_exception_sources(document,card)
    def test_invented_empty_and_wrong_page_claims_fail_for_every_sitting(self):
        for year in SOURCES:
            original=self.cards[f'ru-{year}-hl-c2-1']
            with open_scheme(year,'hl') as document:
                for change in [lambda rule:rule.update(schemePages=[1]),lambda rule:rule.update(sourceText='Always award both discretionary marks for Russian answers.'),lambda rule:rule.update(sourceText='   ')]:
                    card=copy.deepcopy(original);change(card['answerLanguageRule']['manualCriterionExceptions'])
                    with self.assertRaises(AssertionError):verify_manual_criterion_exception_sources(document,card)
    def test_unknown_grouped_duplicate_and_deduction_targets_fail(self):
        original=self.cards['ru-2014-hl-c2-1']
        with open_scheme(2014,'hl') as document:
            for identifiers in [['invented'],['detail-1'],['summary-skills','summary-skills'],[]]:
                card=copy.deepcopy(original);card['answerLanguageRule']['manualCriterionExceptions']['criterionIds']=identifiers
                with self.assertRaises(AssertionError):verify_manual_criterion_exception_sources(document,card)
            card=copy.deepcopy(original);card['rubric']['criteria'][0]['kind']='deduction'
            with self.assertRaises(AssertionError):verify_manual_criterion_exception_sources(document,card)
    def test_specific_2016_zero_discretion_condition_remains_bound_to_original(self):
        card=self.cards['ru-2016-hl-c2-4'];criterion=card['rubric']['criteria'][0]
        limit=next(limit for limit in criterion['limits'] if limit['id']=='missed-return-delay')
        self.assertEqual(limit['maxMarks'],0)
        self.assertEqual(limit['when']['any'][0]['flag'],'missed-return-delay')
        self.assertIn('a week later than originally promised',limit['guidance'][0])
    def test_each_sitting_builder_reproduces_the_published_corrected_summaries(self):
        for year in SOURCES:
            built=importlib.import_module(f'ru_review_{year}_hl').build()
            summaries={card['id']:card for card in built if card['section']=='C2'}
            self.assertEqual(set(summaries),{f'ru-{year}-hl-c2-{number}' for number in range(1,5)})
            for identifier,card in summaries.items():
                self.assertEqual(card,self.cards[identifier])
    def test_new_2011_joint_card_remains_manual_without_legacy_language_state(self):
        self.assertNotIn('answerLanguageRule',self.cards['ru-2011-hl-c2'])

if __name__=='__main__':unittest.main()
