import hashlib
import json
import re
import sys
import unittest
from pathlib import Path
from sources import source_path


class DeferredSources(unittest.TestCase):
    def test_same_sec_filename_resolves_to_different_sittings(self):
        main=source_path(2025,'LC003GLP100EV.pdf','paper')
        deferred=source_path(2025,'LC003GLP100EV-deferred.pdf','paper','deferred')
        self.assertEqual(main.name,deferred.name)
        self.assertNotEqual(main,deferred)
        self.assertNotEqual(hashlib.sha256(main.read_bytes()).digest(),hashlib.sha256(deferred.read_bytes()).digest())

    def test_scheme_and_question_are_separate_sources(self):
        self.assertIn('deferredmarkingschemes',source_path(2025,'LC003GLP000EV-deferred.pdf','scheme','deferred').parts)
        self.assertIn('deferredexams',source_path(2025,'LC003GLP100EV-deferred.pdf','paper','deferred').parts)

    def test_wrong_sitting_is_rejected_instead_of_falling_back_to_june(self):
        for fileid,sitting in [('LC003GLP100EV.pdf','deferred'),('LC003GLP100EV-deferred.pdf','main')]:
            with self.assertRaises(ValueError):source_path(2025,fileid,'paper',sitting)

    def test_atlas_regions_include_every_reviewed_task_and_solution_crop(self):
        plans=Path(__file__).resolve().parents[1]/'authoring'/'maths'
        for path in plans.glob('*-deferred-presentation.json'):
            plan=json.loads(path.read_text())
            self.assertTrue(plan['atlasInspectionNote'])
            for cid,task in plan['tasks'].items():
                n=re.search(r'-q(\d+)',cid)[1]
                for kind,key in [('question','paper'),('solution','scheme')]:
                    first,top,last,bottom=plan['atlasQuestions'][n][key]
                    for page,x0,y0,x1,y1 in task[kind]:
                        with self.subTest(card=cid,kind=kind,page=page):
                            self.assertTrue(first<=page<=last)
                            self.assertTrue(page!=first or y0>=top)
                            self.assertTrue(page!=last or y1<=bottom)

    def test_authored_probability_tree_is_complete_and_consistent_with_the_paper(self):
        sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'authoring'/'maths'))
        from worked_supplements import probability_tree_values
        branches,outcomes=probability_tree_values()
        self.assertEqual(list(map(str,branches)),['0.65','0.35','0.75','0.25','0.98','0.02'])
        self.assertEqual(list(map(str,outcomes)),['0.4875','0.1625','0.3430','0.0070'])
        self.assertEqual(sum(outcomes),1)

    def test_skydiver_graph_reproduces_the_printed_formula_and_complete_table(self):
        sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'authoring'/'maths'))
        from worked_supplements import skydiver_speed
        speeds=[skydiver_speed(t) for t in range(0,33,4)]
        self.assertEqual([round(v,1) for v in speeds],[0,29.7,43.1,49.1,51.8,53.0,53.6,53.8,53.9])
        self.assertEqual(speeds,sorted(speeds))
        self.assertTrue(all(0<=v<54 for v in speeds))

    def test_2024_shed_example_uses_the_positive_given_value_and_full_domain(self):
        sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'authoring'/'maths'))
        from worked_supplements import shed_profit
        self.assertEqual([shed_profit(x) for x in range(0,26,5)],[-900,925,2200,2625,1900,-275])

    def test_2024_faster_drying_example_keeps_the_same_start_and_limit(self):
        sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'authoring'/'maths'))
        from worked_supplements import drying_water
        self.assertEqual(drying_water(0),25)
        self.assertEqual(drying_water(0,-.15),25)
        for t in [1,5,10,30,60]:
            self.assertTrue(5<drying_water(t,-.15)<drying_water(t)<25)
        self.assertAlmostEqual(drying_water(1000,-.15),5)

    def test_2024_wheel_graph_uses_seconds_and_completes_two_revolutions(self):
        sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'authoring'/'maths'))
        from worked_supplements import wheel_height
        self.assertEqual([round(wheel_height(i/10)) for i in range(9)],[0,30,60,30,0,30,60,30,0])
        for t in [.03,.15,.27,.4]:
            self.assertAlmostEqual(wheel_height(t),wheel_height(t+.4))
        self.assertAlmostEqual(wheel_height(.2),60)
        self.assertAlmostEqual(wheel_height(.4),0)

    def test_2024_firework_curve_continues_to_the_correct_positive_zero(self):
        sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'authoring'/'maths'))
        from worked_supplements import firework_height, firework_sea_time
        self.assertEqual([round(firework_height(t)) for t in range(9)],[20,57,84,102,110,108,97,76,46])
        t=firework_sea_time()
        self.assertTrue(9.1<t<9.2)
        self.assertAlmostEqual(firework_height(t),0)
        self.assertTrue(firework_height(8)>0)

    def test_2024_data_graph_reads_the_calendar_year_and_doubling_time(self):
        sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'authoring'/'maths'))
        from worked_supplements import world_data, world_data_time
        self.assertEqual(world_data(0),64)
        self.assertEqual(round(world_data(5),1),152.7)
        self.assertTrue(world_data(6)<200<world_data(7))
        self.assertTrue(2027<2021+world_data_time(200)<2028)
        self.assertEqual(round(world_data_time(150)-world_data_time(75)),4)
        self.assertAlmostEqual(world_data(world_data_time(200)),200)


    def test_2024_parallelogram_completes_the_printed_vertices(self):
        sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'authoring'/'maths'))
        from worked_supplements import parallelogram_2024_vertices
        o,p,q,r=parallelogram_2024_vertices()
        self.assertEqual((o,p,q),((0,0),(2,0),(0,4)))
        self.assertEqual(r,(-2,4))
        # Diagonals share a midpoint, and Q/P satisfy the given line.
        self.assertEqual(tuple(a+b for a,b in zip(o,q)),tuple(a+b for a,b in zip(p,r)))
        self.assertTrue(all(2*x+y-4==0 for x,y in [p,q]))

    def test_2024_vanilla_interval_distinguishes_rounding_and_rejects_the_null(self):
        sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'authoring'/'maths'))
        from worked_supplements import vanilla_2024_interval
        low,high=vanilla_2024_interval()
        self.assertAlmostEqual(low,.174)
        self.assertAlmostEqual(high,.286)
        low_full,high_full=vanilla_2024_interval(False)
        self.assertEqual([round(low_full,3),round(high_full,3)],[.175,.287])
        self.assertTrue(0<low<high<.30)
        self.assertTrue(0<low_full<high_full<.30)


if __name__=='__main__': unittest.main()
