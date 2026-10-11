import copy
import json
import unittest

import paper_census as census
import construction_census_repairs as repair


class ConstructionHeadingRepair(unittest.TestCase):
    def setUp(self):
        paper = census.PP.Paper('construction-studies', 2015, 'hl')
        paper._adopt_unlettered()
        self.texts = {key: (paper.text(*key) or '') for key in paper.parts}
        self.parts = census.complete_leading_romans(paper.parts, self.texts, stem=paper.stem)
        self.review = json.loads(repair.REVIEW.read_text())

    def test_original_lettered_tasks_replace_introductory_options_only(self):
        parts, texts = repair.apply_construction_census_repairs(2015, 'hl', self.parts, self.texts)
        self.assertEqual({key for key in parts if key[0] == 3},
                         {(3, 'a', None), (3, 'b', None), (3, 'c', None)})
        self.assertEqual({key for key in parts if key[0] != 3},
                         {key for key in self.parts if key[0] != 3})
        for key in self.parts:
            if key[0] != 3:
                self.assertEqual(texts[key], self.texts[key])
        self.assertIn('each option listed at (i) and (ii)', texts[(3, 'a', None)])
        self.assertIn('Select one of the above options', texts[(3, 'b', None)])
        self.assertIn('Discuss two advantages', texts[(3, 'c', None)])
        actual, _, _ = census.census_merged('construction-studies', 2015, 'hl')
        self.assertEqual(actual, parts)

    def test_other_sittings_are_unchanged(self):
        for year, level in [(2015, 'ol'), (2016, 'hl'), (2026, 'hl')]:
            self.assertEqual(repair.apply_construction_census_repairs(
                year, level, self.parts, self.texts), (set(self.parts), dict(self.texts)))

    def test_source_and_parser_drift_fail_closed(self):
        mutations = [
            lambda r: r['repairs'][0]['source'].update(sha256='changed'),
            lambda r: r['repairs'][0]['source'].update(textSha256='changed'),
            lambda r: r['repairs'][0]['parts'].pop(),
            lambda r: r['repairs'][0]['parts'][0].update(text='Invented question'),
            lambda r: r['repairs'][0]['prior'][0].update(sha256='changed'),
            lambda r: r['repairs'][0]['prior'][0].update(key=[3, 'a', None]),
        ]
        for change in mutations:
            with self.subTest(change=change):
                review = copy.deepcopy(self.review)
                change(review)
                with self.assertRaises(AssertionError):
                    repair.apply_construction_census_repairs(
                        2015, 'hl', self.parts, self.texts, review)
        with self.assertRaises(AssertionError):
            repair.apply_construction_census_repairs(
                2015, 'hl', set(self.parts) | {(3, 'a', None)}, self.texts)


if __name__ == '__main__':
    unittest.main()
