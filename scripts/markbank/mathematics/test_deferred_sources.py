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


if __name__=='__main__': unittest.main()
