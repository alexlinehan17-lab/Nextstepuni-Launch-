"""Mandatory original archive checks for the 2010 Ordinary CFF scheme."""
import copy
import hashlib
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import fitz
import ja_glyph_derive_2010_ol as recovery
from ja_glyphs import repaired_rawdict
from ja_text import page_rows


class Japanese2010OrdinaryCffRecovery(unittest.TestCase):
    def test_every_missing_identity_has_new_original_image_or_blank_proof(self):
        result = recovery.derive()
        self.assertEqual(result, json.loads(recovery.OUTPUT.read_text()))
        self.assertEqual(sum(map(len, result['repairs'].values())), 156)
        self.assertEqual(result['unresolvedImageOnly'], [])
        for gid, text in [(2014, 'っ'), (2015, 'つ'), (2048, 'ゅ'),
                          (2050, 'ょ'), (2051, 'よ'), (2102, 'ッ'),
                          (2103, 'ツ'), (2136, 'ュ'), (16, '.'), (14810, '．'),
                          (3494, '午'), (5141, '年')]:
            self.assertEqual(result['repairs']['MSMincho'][str(gid)]['text'], text)

    def test_actual_scheme_is_readable_and_keeps_literal_source_spelling(self):
        with fitz.open(recovery.ROOT / recovery.SOURCE) as doc:
            decoded = []
            for page in doc:
                text = '\n'.join(' '.join(cell[2] for cell in row) for row in page_rows(page))
                self.assertNotIn('\ufffd', text, page.number + 1)
                self.assertFalse(any(ord(c) < 32 and c not in '\n\r\t' for c in text), page.number + 1)
                decoded.append(text)
            # Exact examples distinguish real Japanese recovery from a blanket
            # U+FFFD check: ordinary rawdict had substituted unrelated scripts.
            self.assertIn('きらきら・ビーチ', decoded[5])
            self.assertIn('午後  十二時から二時まで', decoded[5])
            self.assertIn('20 年間しています。/ 20 年間。', decoded[6])
            self.assertIn('Ceaser salad', decoded[5])
            self.assertNotIn('Caesar salad', decoded[5])
            self.assertIn('いっしょ', decoded[7])
            self.assertIn('スコットランド', decoded[7])
            self.assertIn('きれい', decoded[6])

    def test_changed_source_font_origin_crop_or_inventory_is_rejected(self):
        original = json.loads(recovery.PROOF.read_text())
        changes = [lambda value: value.update(sha256='changed'),
                   lambda value: value['glyphs'][0].update(origin=[0, 0]),
                   lambda value: value['glyphs'][0].update(imageSha256='changed'),
                   lambda value: value['glyphs'].pop(),
                   lambda value: value['fonts']['MSMincho'].update(sha256='changed'),
                   lambda value: value['blankGlyphs'][0].update(fontSha256='changed')]
        with tempfile.TemporaryDirectory(dir=recovery.ROOT / 'tmp') as directory:
            path = Path(directory) / 'changed-proof.json'
            for change in changes:
                value = copy.deepcopy(original); change(value)
                path.write_text(json.dumps(value))
                with patch.object(recovery, 'PROOF', path), self.assertRaises(AssertionError):
                    recovery.derive()

    def test_unrelated_pdf_and_modified_original_are_not_repaired(self):
        source = recovery.ROOT / recovery.SOURCE
        self.assertEqual(hashlib.sha256(source.read_bytes()).hexdigest(), recovery.PIN)
        unrelated = recovery.ROOT / 'examiner-reports/japanese/papers/2010-ol-000-paper.pdf'
        with fitz.open(unrelated) as doc:
            raw = doc[2].get_text('rawdict'); before = json.dumps(raw, sort_keys=True)
            self.assertIs(repaired_rawdict(doc[2], raw), raw)
            self.assertEqual(json.dumps(raw, sort_keys=True), before)
        with tempfile.TemporaryDirectory(dir=recovery.ROOT / 'tmp') as directory:
            changed = Path(directory) / 'changed-source.pdf'
            changed.write_bytes(source.read_bytes() + b'\n% changed original identity\n')
            with fitz.open(changed) as doc:
                raw = doc[7].get_text('rawdict'); before = json.dumps(raw, sort_keys=True)
                self.assertIs(repaired_rawdict(doc[7], raw), raw)
                self.assertEqual(json.dumps(raw, sort_keys=True), before)


if __name__ == '__main__':
    unittest.main()
