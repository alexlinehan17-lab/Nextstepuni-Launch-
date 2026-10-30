import hashlib
import unittest
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


if __name__=='__main__': unittest.main()
