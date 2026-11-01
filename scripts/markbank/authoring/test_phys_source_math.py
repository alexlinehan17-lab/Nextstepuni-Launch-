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


    def test_legacy_lambda_is_not_duplicated_by_a_synthetic_space(self):
        from phys_review_2011_hl import GLYPHS as G11, SOURCES as S11
        with fitz.open(ROOT / S11['scheme']['path']) as scheme:
            self.assertEqual(equation_text(scheme[4], (220,428,286,446), G11['scheme'],
                                           degrees=True, dedupe=True), 'nλ =dsinθ')

    def test_legacy_equal_size_powers_and_beta_indices_use_geometry(self):
        from phys_review_2011_hl import GLYPHS as G11, SOURCES as S11
        with fitz.open(ROOT / S11['scheme']['path']) as scheme:
            self.assertEqual(equation_text(scheme[6], (154,213,342,234), G11['scheme'],
                                           degrees=True, dedupe=True, baseline=True),
                             'v²=u² + 2as/0=20² + 2(a )(50)/a=4ms⁻²')
            self.assertEqual(equation_text(scheme[11], (114,219,190,238), G11['scheme'],
                                           degrees=True, dedupe=True, baseline=230.3),
                             '²²⁸₈₈X → ²²⁸₈₉Y + ⁰₋₁e')

    def test_compound_paths_preserve_complete_charge_products_and_ratios(self):
        from phys_review_2011_hl import GLYPHS as G11, SOURCES as S11
        with fitz.open(ROOT / S11['scheme']['path']) as scheme:
            options=dict(baseline=True, dedupe=True, glyph_order=True, segments=True)
            self.assertEqual(fraction_text(scheme[10], (170,253,232,285), G11['scheme'], **options),
                             'F= Q(3Q)/(4πεd²)')
            self.assertEqual(fraction_text(scheme[10], (290,332,351,365), G11['scheme'], **options),
                             "// F'/F = 4Q²/(3Q²)")
        self.assertEqual((2*2)/(1*3), 4/3)

    def test_legacy_fraction_reader_keeps_digits_contiguous_and_angles_unraised(self):
        from phys_review_2011_hl import GLYPHS as G11, SOURCES as S11
        with fitz.open(ROOT / S11['scheme']['path']) as scheme:
            options=dict(baseline=True, dedupe=True, glyph_order=True, segments=True)
            self.assertEqual(fraction_text(scheme[13], (134,214,418,238), G11['scheme'], **options),
                             'EFL(= 8/60 )=0.133//F.L:( (8×100)/60 )/13.33%(efficient)')
            self.assertEqual(fraction_text(scheme[14], (180,644,264,672), G11['scheme'], **options),
                             'n= 1/(sinic) (=1.33)')
            self.assertEqual(fraction_text(scheme[15], (190,333,354,381), G11['scheme'], **options),
                             'r²= ((1.7×10⁻⁸)(1))/(π(6.75×10⁻³)) //8.017×10⁻⁷')

    def test_strontium_atom_count_uses_the_half_life_given_in_the_question(self):
        import math
        for days in (365,365.25):
            decay_constant=math.log(2)/(28.78*days*24*3600)
            self.assertAlmostEqual(decay_constant,7.63e-10,delta=0.01e-10)
            self.assertAlmostEqual(4250/decay_constant,5.57e12,delta=0.01e12)
            self.assertGreater(abs(decay_constant-7.77e-10),0.1e-10)

    def test_overlapping_paper_strips_recover_whole_questions_and_velocity_units(self):
        from phys_review_lib import Src
        from phys_review_2011_ol import GLYPHS, SOURCES
        src = Src(str(ROOT / SOURCES['paper']['path']), 'paper', glyphs=GLYPHS['paper'])
        self.assertIn('A car of mass 1400 kg was travelling with a constant speed of 15 m s⁻¹', src.lines[5])
        self.assertIn('(j) Give a disadvantage of a named renewable source of energy.', src.lines[4])
        self.assertIn('How is this risk of injury minimised?', src.lines[5])
        self.assertIn('(11)', src.cells[5].values())
        question = 'Draw a diagram of the forces acting on the car before'
        self.assertTrue(src.find_box(5, question, (83,73,545,256)))
        self.assertFalse(src.find_box(5, question, (83,73,545,230)))
        self.assertIn('(iv) Name the scientist who designed the experiment.', src.lines[10])

    def test_ordinary_2011_fractions_keep_separate_denominators_and_signed_acceleration(self):
        from phys_review_2011_ol import GLYPHS, SOURCES
        with fitz.open(ROOT / SOURCES['scheme']['path']) as scheme:
            options=dict(baseline=True, dedupe=True, glyph_order=True, segments=True)
            self.assertEqual(fraction_text(scheme[2], (89,525,220,556), GLYPHS['scheme'], **options),
                             '(velocity=) distance/(time) / s/t')
            self.assertEqual(fraction_text(scheme[7], (77,357,277,390), GLYPHS['scheme'], **options),
                             '(a= (v−u)/t = (0−15)/0.4 =−)37.5(ms⁻²)')
        self.assertEqual((0-15)/.4, -37.5)
        self.assertAlmostEqual((.0675*4180+.0734*390)*9, 2796.984)
        self.assertAlmostEqual(.00103*4180*(100-19), 348.7374)

if __name__ == '__main__':
    unittest.main()
