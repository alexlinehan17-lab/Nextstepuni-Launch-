"""Source-layout regressions from independent Physics paper/scheme reviews."""
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

    def test_interleaved_gravity_glyphs_keep_products_powers_and_fraction_groups(self):
        from phys_review_2014_ol import GLYPHS as G14, SOURCES as S14
        with fitz.open(ROOT / S14['scheme']['path']) as scheme:
            self.assertEqual(fraction_text(scheme[8], (65,341,290,375), G14, glyph_order=True),
                             '(g= GM/d² = ((6.67 ×10⁻¹¹)(6.4 ×10²³))/(3.4 ×10⁶)² =)3.7 (ms⁻²)')
        self.assertAlmostEqual(6.67e-11 * 6.4e23 / (3.4e6)**2, 3.7, delta=0.05)

    def test_interleaved_current_preserves_source_typo_for_visible_correction(self):
        from phys_review_2014_ol import GLYPHS as G14, SOURCES as S14
        with fitz.open(ROOT / S14['scheme']['path']) as scheme:
            self.assertEqual(fraction_text(scheme[15], (93,616,226,649), G14, glyph_order=True),
                             '(I= V/R = 6/500 =) 1.2 ×10⁻³(A)')
        # Independently recompute from the paper's 6 V and 50 + 450 ohms.
        self.assertEqual(6 / (50 + 450), 0.012)
        self.assertEqual(6 / (50 + 450) * 50, 0.6)

    def test_critical_angle_fraction_keeps_both_sine_denominators(self):
        from phys_review_2014_ol import GLYPHS as G14, SOURCES as S14
        with fitz.open(ROOT / S14['scheme']['path']) as scheme:
            self.assertEqual(fraction_text(scheme[10], (91,588,201,621), G14),
                             'n= 1/(sinC) = 1/(sin38) =1.62')

    def test_reviewed_temperature_degrees_preserve_words_and_signed_values(self):
        from phys_review_2012_hl import GLYPHS as G12, SOURCES as S12
        with fitz.open(ROOT / S12['scheme']['path']) as scheme:
            clip = (111,97,363,112)
            self.assertEqual(equation_text(scheme[14], clip, G12, degrees=True),
                             'temperature of ice increased (from ≈ –3° to 0°C as energy is added)')
            self.assertEqual(equation_text(scheme[14], clip, G12),
                             'temperature of ice increased (from ≈ –3o to 0oC as energy is added)')
            self.assertEqual(equation_text(scheme[13], (210,593,296.4,610), G12, degrees=True),
                             'answer: θ = 54.7(4)°')
            self.assertEqual(equation_text(scheme[6], (83,296,185,309), G12, degrees=True),
                             'speed of jet = 1320 (m s⁻¹)')

if __name__ == '__main__':
    unittest.main()
