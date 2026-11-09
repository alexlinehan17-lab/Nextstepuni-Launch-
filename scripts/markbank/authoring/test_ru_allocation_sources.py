"""Fixed and conditional caps must be bound to their own original pages."""
import copy
import unittest
import fitz
from ru_verify_review import verify_allocation_sources


class AllocationSourcesTest(unittest.TestCase):
    def setUp(self):
        self.document = fitz.open()
        self.document.new_page().insert_text((50, 50), 'Two details at two marks each')
        self.document.new_page().insert_text((50, 50), 'Without the required reference award a maximum of three marks')
        self.card = {'id': 'synthetic-allocation', 'rubric': {'allocationCap': {
            'sourceText': 'Two details at two marks each', 'schemePages': [1],
            'limits': [{'id': 'reference', 'sourceText': 'Without the required reference award a maximum of three marks', 'schemePages': [2]}],
        }}}

    def tearDown(self):
        self.document.close()

    def test_each_rule_is_accepted_on_its_own_page(self):
        verify_allocation_sources(self.document, self.card)

    def test_wrong_pages_invented_or_empty_rules_fail_for_both_layers(self):
        for layer in ('fixed', 'conditional'):
            for change in ({'schemePages': [2 if layer == 'fixed' else 1]}, {'schemePages': []},
                           {'schemePages': [0]}, {'schemePages': [3]}, {'schemePages': [1.5]},
                           {'schemePages': [True]}, {'sourceText': 'Invented four mark bonus'}, {'sourceText': ' \n'}):
                with self.subTest(layer=layer, change=change):
                    card = copy.deepcopy(self.card)
                    rule = card['rubric']['allocationCap']
                    if layer == 'conditional':
                        rule = rule['limits'][0]
                    rule.update(change)
                    with self.assertRaises(AssertionError):
                        verify_allocation_sources(self.document, card)

    def test_ordinary_cards_need_no_allocation_binding(self):
        verify_allocation_sources(self.document, {'id': 'ordinary'})


if __name__ == '__main__':
    unittest.main()
