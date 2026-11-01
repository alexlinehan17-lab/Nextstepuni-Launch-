"""Source-layout regressions found during the independent 2016 Physics review."""
from pathlib import Path
import unittest
import fitz
from phys_review_lib import fraction_text, equation_text
from phys_review_2016_hl import GLYPHS, SOURCES

ROOT = Path(__file__).resolve().parents[3]

class PhysicsSourceMathTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.scheme = fitz.open(ROOT / SOURCES['scheme']['path'])

    @classmethod
    def tearDownClass(cls):
        cls.scheme.close()

    def test_string_equation_keeps_both_fractions_inside_correct_groups(self):
        self.assertEqual(fraction_text(self.scheme[4], (110,632,170,667), GLYPHS),
                         'f= 1/(2l) √(T/μ)')

    def test_pendulum_slanted_fraction_stays_under_the_square_root(self):
        self.assertEqual(fraction_text(self.scheme[8], (53,651,112,678), GLYPHS),
                         'T=2π√(l/g)')

    def test_beta_equation_keeps_electron_mass_above_negative_charge(self):
        self.assertEqual(equation_text(self.scheme[11], (54,532,153,560), GLYPHS),
                         '²²⁵₈₈Ra → ²²⁵₈₉Ac + ⁰₋₁e')

    def test_ordinary_gravity_unit_keeps_raised_minus_and_square(self):
        from phys_review_lib import Src
        from phys_review_2016_ol import GLYPHS as OL_GLYPHS, SOURCES as OL_SOURCES
        paper = Src(str(ROOT / OL_SOURCES['paper']['path']), 'paper', glyphs=OL_GLYPHS)
        self.assertIn('(acceleration due to gravity, g = 9.8 m s⁻²)', paper.lines[9])

    def test_doppler_correction_agrees_with_both_published_numerical_results(self):
        # The printed formulas are paired with opposite extrema. These are
        # independent calculations from the paper's 1.1 kHz, 340 and 13 m/s.
        self.assertAlmostEqual(1100 * 340 / (340 - 13), 1143.7, delta=0.05)
        self.assertAlmostEqual(1100 * 340 / (340 + 13), 1059.5, delta=0.05)

if __name__ == '__main__':
    unittest.main()
