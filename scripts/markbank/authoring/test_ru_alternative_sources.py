"""Authoring-only checks for source-bound alternatives; no archived PDF needed."""
import unittest
import fitz
from ru_verify_review import verify_alternative_sources


class AlternativeSourcesTest(unittest.TestCase):
    def setUp(self):
        self.document = fitz.open()
        self.document.new_page().insert_text((50, 50), 'General answer / up to two specific details')
        self.document.new_page().insert_text((50, 50), 'Unrelated guidance')

    def tearDown(self):
        self.document.close()

    def card(self, text='General answer / up to two specific details', pages=None):
        return {'id': 'synthetic-source-check', 'rubric': {'alternativeSets': [{
            'id': 'response', 'sourceText': text, 'schemePages': [1] if pages is None else pages,
        }]}}

    def test_exact_bound_source_is_accepted(self):
        verify_alternative_sources(self.document, self.card())

    def test_rule_on_another_page_is_rejected(self):
        with self.assertRaises(AssertionError):
            verify_alternative_sources(self.document, self.card(pages=[2]))

    def test_invented_rule_is_rejected(self):
        with self.assertRaises(AssertionError):
            verify_alternative_sources(self.document, self.card(text='All answers may be added together'))

    def test_missing_or_invalid_binding_is_rejected(self):
        for pages in ([], [0], [3], [1.5], [True]):
            with self.subTest(pages=pages), self.assertRaises(AssertionError):
                verify_alternative_sources(self.document, self.card(pages=pages))

    def test_empty_rule_is_rejected(self):
        with self.assertRaises(AssertionError):
            verify_alternative_sources(self.document, self.card(text=''))


if __name__ == '__main__':
    unittest.main()
