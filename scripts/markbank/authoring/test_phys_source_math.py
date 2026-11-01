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

    def test_2010_shared_spans_preserve_radius_powers_and_negative_unit_exponents(self):
        from phys_review_2010_hl import GLYPHS, SOURCES
        with fitz.open(ROOT / SOURCES['scheme']['path']) as scheme:
            options=dict(baseline=True, dedupe=True, glyph_order=True, segments=True, glyph_baselines=True)
            self.assertEqual(fraction_text(scheme[8], (122,496,190,526), GLYPHS['scheme'], **options),
                             'GMEm/R₁² = GMₘm/R₂²')
            self.assertEqual(fraction_text(scheme[8], (122,525,181,553), GLYPHS['scheme'], **options),
                             'ME/Mₘ (=81)= R₁²/R₂²')
            self.assertEqual(equation_text(scheme[8], (247,679,377,698), GLYPHS['scheme'],
                                          baseline=True, dedupe=True, degrees=True, glyph_baselines=True),
                             'v=1022.9ms⁻¹(≈1.02×10³ms⁻¹)')

    def test_2010_bracket_only_groups_and_padding_keep_doppler_and_energy_equations(self):
        from phys_review_2010_hl import GLYPHS, SOURCES
        with fitz.open(ROOT / SOURCES['scheme']['path']) as scheme:
            options=dict(baseline=True, dedupe=True, glyph_order=True, segments=True, glyph_baselines=True)
            self.assertEqual(fraction_text(scheme[9], (215,546,280,584), GLYPHS['scheme'], **options),
                             'λ′=λ( (c+u)/c )')
            self.assertEqual(equation_text(scheme[12], (212,395,452,421), GLYPHS['scheme'],
                                          baseline=True, dedupe=True, degrees=True, glyph_baselines=True),
                             'E=hf/E=(6.6×10⁻³⁴)[3.6×10²⁰]/2.376×10⁻¹³(J )')
            self.assertEqual(fraction_text(scheme[16], (232,606,337,639), GLYPHS['scheme'], **options),
                             '1/(4πε) [ (2×10⁻⁶)/(0.1)² + (5×10⁻⁶)/(0.15)² ]')

    def test_2010_calculations_independently_follow_the_supplied_data(self):
        import math
        self.assertAlmostEqual(9.8/9, 1.09, delta=.005)
        self.assertAlmostEqual(2*math.pi*3.84e8/(27.3*24*3600),1022.9,delta=.1)
        self.assertAlmostEqual(3e8*(590/587-1),1.5333e6,delta=100)
        self.assertAlmostEqual((6.6e-34*3.6e20-2*9.1e-31*(3e8)**2)/2,3.69e-14,delta=1e-18)
        latent=((.0618*4180+.0346*390)*11.8-.0012*4180*80)/.0012
        self.assertAlmostEqual(latent,2.34e6,delta=5000)
        self.assertAlmostEqual(2000/230,8.7,delta=.01)
        self.assertAlmostEqual(230**2/2000,26.4,delta=.1)
        self.assertAlmostEqual(202.5e6*1.6e-19/(3e8)**2,3.6e-28,delta=1e-31)
        self.assertAlmostEqual((2e-6/.1**2+5e-6/.15**2)/(4*math.pi*8.9e-12),3.77e6,delta=6000)
        self.assertEqual(150*6+300*8+150*5,4050)
        self.assertAlmostEqual(4050/(19*60),3.55,delta=.01)

    def test_2010_ordinary_experimental_data_and_unit_conversions(self):
        import math
        focal_lengths=[u*v/(u+v) for u,v in [(20,65),(30,32),(50,23)]]
        self.assertAlmostEqual(sum(focal_lengths)/3,15.5,delta=.02)
        diameter=(.21+.20+.18)/3*1e-3
        area=math.pi*(diameter/2)**2
        self.assertGreaterEqual(area,3.03e-8)
        self.assertLessEqual(area,3.14e-8)
        resistivity=20.2*area/.488
        self.assertGreaterEqual(resistivity,1.25e-6)
        self.assertLessEqual(resistivity,1.29e-6)
        for force,acceleration in [(0.20,.4),(.25,.5),(.30,.6),(.35,.7),(.40,.8),(.45,.9),(.50,1)]:
            self.assertEqual(acceleration,2*force)

    def test_2010_ordinary_collision_circuit_and_two_stage_journey(self):
        speed=(50*6+70*0)/(50+70)
        self.assertEqual(speed,2.5)
        self.assertEqual(.5*50*6**2,900)
        self.assertEqual(.5*(50+70)*speed**2,375)
        parallel=1/(1/15+1/30)
        self.assertEqual(parallel,10)
        self.assertEqual(12/(10+parallel+4),.5)
        acceleration=60/120
        end_speed=acceleration*15
        self.assertEqual(.5*acceleration*15**2,56.25)
        self.assertAlmostEqual(80/((end_speed+0)/2),21.33,delta=.005)

if __name__ == '__main__':
    unittest.main()
