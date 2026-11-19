"""Source-archive gate for the narrow 2017 reader recovery; not a CI PDF dependency."""
import hashlib
import json
import tempfile
import unittest
from pathlib import Path

import fitz
from ja_glyphs import repaired_rawdict
from ja_text import page_rows

ROOT = Path(__file__).resolve().parents[3]
SOURCE = ROOT / 'examiner-reports/japanese/papers/2017-hl-000-paper.pdf'


class JapaneseGlyphRecovery(unittest.TestCase):
    def test_original_trace_and_crop_bind_the_actual_nakai_character(self):
        proof = json.loads((Path(__file__).parent / 'reviews/japanese-2017-hl-glyph-proof.json').read_text())
        self.assertEqual(proof['text'], '居')
        self.assertEqual(proof['gid'], 5251)
        self.assertEqual(hashlib.sha256(SOURCE.read_bytes()).hexdigest(), proof['sha256'])
        with fitz.open(SOURCE) as doc:
            hits = [(span['font'], gid, [round(value, 1) for value in origin]) for span in doc[8].get_texttrace() for uni, gid, origin, _ in span['chars'] if gid == 5251]
            self.assertIn(('MS-Mincho', 5251, proof['origin']), hits)
            text = '\n'.join(' '.join(cell[2] for cell in row) for row in page_rows(doc[8]))
            self.assertIn('中居（なかい）さんは MC になります。', text)
            self.assertIn('楽', text)
            self.assertNotIn('\ufffd', text)

    def test_every_question_page_has_no_unresolved_or_control_glyph(self):
        with fitz.open(SOURCE) as doc:
            for pno in [3, 4, 7, 8, 9, 11, 12, 14, 16]:
                text = '\n'.join(' '.join(cell[2] for cell in row) for row in page_rows(doc[pno - 1]))
                self.assertNotIn('\ufffd', text, pno)
                self.assertFalse(any(ord(char) < 32 and char not in '\n\r\t' for char in text), pno)
        manifest = json.loads(Path(__file__).with_name('glyphmap-japanese-2017.json').read_text())
        self.assertEqual(len(manifest['unresolvedImageOnly']), 19)
        self.assertEqual({location['page'] for item in manifest['unresolvedImageOnly'] for location in item['locations']}, {1, 6, 10})

    def test_unrelated_pdf_and_modified_target_bytes_are_untouched(self):
        with fitz.open(ROOT / 'examiner-reports/japanese/papers/2018-hl-000-paper.pdf') as doc:
            raw = doc[2].get_text('rawdict')
            before = json.dumps(raw, sort_keys=True)
            self.assertIs(repaired_rawdict(doc[2], raw), raw)
            self.assertEqual(json.dumps(raw, sort_keys=True), before)
        with tempfile.TemporaryDirectory() as directory:
            changed = Path(directory) / SOURCE.name
            changed.write_bytes(SOURCE.read_bytes() + b'\n% unrelated byte identity\n')
            with fitz.open(changed) as doc:
                raw = doc[8].get_text('rawdict')
                before = json.dumps(raw, sort_keys=True)
                self.assertIs(repaired_rawdict(doc[8], raw), raw)
                self.assertEqual(json.dumps(raw, sort_keys=True), before)


if __name__ == '__main__':
    unittest.main()
