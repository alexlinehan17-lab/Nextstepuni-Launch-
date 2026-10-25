"""Paper Trail chip labels for English Paper 2 keep the paper's printed title.

title_case() turns a heading the SEC prints in capitals into a chip label.
str.title() alone printed "The Handmaid’S Tale" and "Yeats’S", and a split at
the first spaced dash cut 2019 Ordinary's "THE FISH (EXTRACT: LINES 45 – 76)"
to "The Fish (Extract: Lines 45". Run: python3 scripts/paper-trail/test_english_p2_labels.py
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from english_p2_complete import title_case  # noqa: E402


class TitleCaseTest(unittest.TestCase):
    def test_possessive_after_an_apostrophe_stays_lower_case(self):
        self.assertEqual(title_case("THE HANDMAID’S TALE – Margaret Atwood"), "The Handmaid’s Tale")
        self.assertEqual(title_case("A DOLL’S HOUSE – Henrik Ibsen"), "A Doll’s House")
        self.assertEqual(title_case("“Yeats’s poetry is both intellectually stimulating"),
                         "“Yeats’s Poetry Is Both Intellectually Stimulating")
        self.assertEqual(title_case("“Yeats's poetry is driven by a tension"), "“Yeats's Poetry Is Driven By A Tension")
        self.assertEqual(title_case("IT’S NOT"), "It’s Not")

    def test_a_name_after_an_apostrophe_keeps_its_capital(self):
        self.assertEqual(title_case("O’CASEY’S DUBLIN"), "O’Casey’s Dublin")
        self.assertEqual(title_case("“Hopkins’ innovative style"), "“Hopkins’ Innovative Style")

    def test_a_dash_inside_brackets_is_part_of_the_title(self):
        self.assertEqual(title_case("THE FISH (EXTRACT: LINES 45 – 76)"),
                         "The Fish (Extract: Lines 45 – 76)")
        self.assertEqual(title_case("DANIEL’S DUCK  (EXTRACT: LINES 7 – 27)"),
                         "Daniel’s Duck (Extract: Lines 7 – 27)")

    def test_the_author_after_a_dash_outside_brackets_is_dropped(self):
        self.assertEqual(title_case("WUTHERING HEIGHTS – Emily Brontë"), "Wuthering Heights")
        self.assertEqual(title_case("HERO, HEROINE, VILLAIN"), "Hero, Heroine, Villain")

    def test_a_roman_numeral_is_printed_in_capitals(self):
        self.assertEqual(title_case("BABY-MOVEMENTS II, “TRAILING CLOUDS”"),
                         "Baby-Movements II, “Trailing Clouds”")


if __name__ == "__main__":
    unittest.main()
