import copy
import json
import unittest

import construction_2022_higher as m
import construction_paper as cp


class SourceGuard(unittest.TestCase):
    def test_source_and_images(self):
        d = json.loads((cp.R / f'scripts/markbank/authored/construction-studies-{m.YEAR}-{m.LEVEL}-reviewed.json').read_text())
        self.assertEqual(m.validate(d)['tasks'], 45)

    def test_rejects_lost_marks_wording_routes_topics_or_corrections(self):
        original = json.loads((cp.R / f'scripts/markbank/authored/construction-studies-{m.YEAR}-{m.LEVEL}-reviewed.json').read_text())
        cases = cp.mutation_cases(m, original)
        self.assertGreaterEqual(len(cases), 30)
        for label, change in cases.items():
            with self.subTest(label=label):
                d = copy.deepcopy(original)
                change(d)
                with self.assertRaises(AssertionError):
                    m.validate(d, images=False)


if __name__ == '__main__':
    unittest.main()
