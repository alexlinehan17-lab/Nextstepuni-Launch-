"""Mandatory original-archive gate; ordinary tests use committed proof digests."""
import copy
import hashlib
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import fitz
import ja_glyph_derive_2010 as recovery
from ja_glyphs import repaired_rawdict
from ja_text import page_rows


class Japanese2010CffRecovery(unittest.TestCase):
    def test_all_missing_identities_are_original_image_readings_or_proven_spaces(self):
        result = recovery.derive()
        self.assertEqual(result, json.loads(recovery.OUTPUT.read_text()))
        self.assertEqual(sum(map(len, result['repairs'].values())), 314)
        self.assertEqual(result['unresolvedImageOnly'], [])
        for font, gid, character in [
            ('MS-PMincho', 16934, 'っ'), ('MS-PMincho', 16935, 'つ'),
            ('MS-PMincho', 16988, 'ァ'), ('MS-PMincho', 16989, 'ア'),
            ('MS-PMincho', 16990, 'ィ'), ('MS-PMincho', 16991, 'イ'),
            ('MS-PMincho', 17022, 'ッ'), ('MSMincho', 2046, 'ゃ'),
            ('MSMincho', 2047, 'や'), ('MSMincho', 2048, 'ゅ'),
            ('MSMincho', 2049, 'ゆ'), ('MSMincho', 2050, 'ょ'),
            ('MSMincho', 2051, 'よ'), ('MS-Gothic', 1990, 'か'),
            ('MS-Gothic', 2070, 'イ'), ('MSMincho', 6595, '末'),
        ]:
            self.assertEqual(result['repairs'][font][str(gid)]['text'], character)

    def test_every_original_scheme_page_is_readable_without_typo_normalization(self):
        with fitz.open(recovery.ROOT / recovery.SOURCE) as doc:
            for page in doc:
                text = '\n'.join(' '.join(cell[2] for cell in row) for row in page_rows(page))
                self.assertNotIn('\ufffd', text, page.number + 1)
                self.assertFalse(any(ord(char) < 32 and char not in '\n\r\t' for char in text), page.number + 1)
            text = '\n'.join(' '.join(cell[2] for cell in row) for row in page_rows(doc[8]))
            self.assertIn('デイズニーランドへ行きましたか。', text)
            self.assertNotIn('ディズニーランドへ行きました。', text)
            self.assertNotIn('ディズニーランドへ行きましたか。', text)

    def test_changed_source_origin_crop_and_missing_glyph_cannot_verify(self):
        original = json.loads(recovery.PROOF.read_text())
        changes = [
            lambda value: value.update(sha256='changed'),
            lambda value: value['glyphs'][0].update(origin=[0, 0]),
            lambda value: value['glyphs'][0].update(imageSha256='changed'),
            lambda value: value['glyphs'].pop(),
            lambda value: value['blankGlyphs'][0].update(fontSha256='changed'),
        ]
        with tempfile.TemporaryDirectory(dir=recovery.ROOT / 'tmp') as directory:
            path = Path(directory) / 'changed-proof.json'
            for change in changes:
                value = copy.deepcopy(original)
                change(value)
                path.write_text(json.dumps(value))
                with patch.object(recovery, 'PROOF', path), self.assertRaises(AssertionError):
                    recovery.derive()

    def test_unrelated_original_and_changed_source_bytes_are_not_repaired(self):
        source = recovery.ROOT / recovery.SOURCE
        self.assertEqual(hashlib.sha256(source.read_bytes()).hexdigest(), recovery.PIN)
        unrelated = recovery.ROOT / 'examiner-reports/japanese/papers/2010-hl-000-paper.pdf'
        with fitz.open(unrelated) as doc:
            raw = doc[2].get_text('rawdict')
            before = json.dumps(raw, sort_keys=True)
            self.assertIs(repaired_rawdict(doc[2], raw), raw)
            self.assertEqual(json.dumps(raw, sort_keys=True), before)
        with tempfile.TemporaryDirectory(dir=recovery.ROOT / 'tmp') as directory:
            changed = Path(directory) / 'changed-source.pdf'
            changed.write_bytes(source.read_bytes() + b'\n% changed original identity\n')
            with fitz.open(changed) as doc:
                raw = doc[8].get_text('rawdict')
                before = json.dumps(raw, sort_keys=True)
                self.assertIs(repaired_rawdict(doc[8], raw), raw)
                self.assertEqual(json.dumps(raw, sort_keys=True), before)


if __name__ == '__main__':
    unittest.main()
