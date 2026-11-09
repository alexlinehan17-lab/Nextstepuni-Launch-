"""Every grouped criterion descriptor must occur in its original source pages."""
import copy
import io
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

import fitz
from ru_verify_review import verify


class GroupedCriteriaSourceTest(unittest.TestCase):
    def setUp(self):
        with fitz.open() as doc:
            doc.new_page().insert_text((50, 50), '\n'.join([
                'Original criterion guidance', 'Original band guidance',
                'Original limit guidance', 'Original limited band guidance',
            ]))
            self.pdf = doc.tobytes()
        self.criterion = {
            'guidance': ['Original criterion guidance'],
            'bands': [{'guidance': ['Original band guidance']}],
            'limits': [{'guidance': ['Original limit guidance'],
                        'bands': [{'guidance': ['Original limited band guidance']}]}],
        }
        self.card = {
            'id': 'synthetic-grouped-source-check', 'kind': 'rubric',
            'year': 2016, 'level': 'higher', 'review': {'schemePages': [1]},
            'rubric': {'system': 'language-points', 'taskRequirements': [],
                       'groups': [{'id': 'detail', 'rows': [], 'criteria': [self.criterion]}]},
        }

    def check(self, card):
        with patch('ru_verify_review.open_scheme', side_effect=lambda *_: fitz.open(stream=self.pdf, filetype='pdf')):
            with redirect_stdout(io.StringIO()):
                verify([card])

    def test_all_grouped_descriptor_layers_are_source_bound(self):
        self.check(self.card)

    def test_invented_grouped_descriptors_are_rejected_at_every_layer(self):
        for location in ('criterion', 'band', 'limit', 'limited-band'):
            with self.subTest(location=location):
                card = copy.deepcopy(self.card)
                criterion = card['rubric']['groups'][0]['criteria'][0]
                target = {
                    'criterion': criterion,
                    'band': criterion['bands'][0],
                    'limit': criterion['limits'][0],
                    'limited-band': criterion['limits'][0]['bands'][0],
                }[location]
                target['guidance'] = ['An invented award not present in the source']
                with self.assertRaises(AssertionError):
                    self.check(card)

    def test_existing_whole_task_criteria_remain_source_bound(self):
        card = copy.deepcopy(self.card)
        card['rubric']['criteria'] = card['rubric']['groups'][0].pop('criteria')
        self.check(card)
        card['rubric']['criteria'][0]['guidance'] = ['An invented whole-task award']
        with self.assertRaises(AssertionError):
            self.check(card)


if __name__ == '__main__':
    unittest.main()
