"""Mandatory original-archive gate; ordinary unit tests use committed digests."""
import copy
import hashlib
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import fitz
import ja_glyph_derive_2014 as recovery
from ja_glyphs import repaired_rawdict
from ja_text import page_rows


class Japanese2014CffRecovery(unittest.TestCase):
    def test_every_marking_page_is_readable_and_transcript_only_survivors_are_explicit(self):
        result = recovery.derive()
        self.assertEqual(sum(map(len, result['repairs'].values())), 115)
        self.assertEqual(len(result['unresolvedImageOnly']), 186)
        self.assertTrue(all(place['page'] >= 11 for item in result['unresolvedImageOnly'] for place in item['locations']))
        self.assertEqual(result['repairs']['MSMincho']['2120']['text'], 'ご')
        self.assertEqual(result['repairs']['MSMincho']['2145']['text'], 'ね')
        self.assertEqual(result['repairs']['MSMincho']['2169']['text'], 'ゅ')
        self.assertEqual(result['repairs']['MSMincho']['2249']['text'], 'プ')
        self.assertEqual(result['repairs']['MSMincho']['15917']['text'], '／')
        with fitz.open(recovery.ROOT / recovery.SOURCE) as doc:
            for page in [doc[i] for i in range(10)]:
                text = '\n'.join(' '.join(cell[2] for cell in row) for row in page_rows(page))
                self.assertNotIn('\ufffd', text, page.number + 1)
                self.assertFalse(any(ord(char) < 32 and char not in '\n\r\t' for char in text), page.number + 1)
            text = '\n'.join(' '.join(cell[2] for cell in row) for row in page_rows(doc[4]))
            self.assertIn('パズル', text)
            self.assertIn('ネクタイ', text)
            text = '\n'.join(' '.join(cell[2] for cell in row) for row in page_rows(doc[6]))
            self.assertIn('朝ごはん', text)
            self.assertIn('じゃありません／ではありません／ではないです／', text)

    def test_proof_rejects_changed_crop_origin_source_and_missing_required_glyph(self):
        proof = json.loads(recovery.PROOF.read_text())
        mutations = [
            lambda value: value.update(sha256='0' * 64),
            lambda value: value['glyphs'][0].update(origin=[0, 0]),
            lambda value: value['glyphs'][0].update(imageSha256='0' * 64),
            lambda value: value['glyphs'].pop(0),
        ]
        with tempfile.TemporaryDirectory(dir=recovery.ROOT / 'tmp') as directory:
            path = Path(directory) / 'changed-proof.json'
            for mutate in mutations:
                changed = copy.deepcopy(proof)
                mutate(changed)
                path.write_text(json.dumps(changed))
                with patch.object(recovery, 'PROOF', path), self.assertRaises(AssertionError):
                    recovery.derive()

    def test_modified_source_identity_is_never_silently_repaired(self):
        original = recovery.ROOT / recovery.SOURCE
        self.assertEqual(hashlib.sha256(original.read_bytes()).hexdigest(), recovery.PIN)
        with tempfile.TemporaryDirectory() as directory:
            changed = Path(directory) / 'changed.pdf'
            changed.write_bytes(original.read_bytes() + b'\n% changed byte identity\n')
            with fitz.open(changed) as doc:
                raw = doc[4].get_text('rawdict')
                before = json.dumps(raw, sort_keys=True)
                self.assertIs(repaired_rawdict(doc[4], raw), raw)
                self.assertEqual(json.dumps(raw, sort_keys=True), before)


if __name__ == '__main__':
    unittest.main()
