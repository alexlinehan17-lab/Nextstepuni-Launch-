"""Paper-by-paper English publication: only a paper's own strict gate can ship it."""
import copy
import json
import unittest
from unittest import mock

import english_full_cards as parser
import english_publish as publish
from english_complete import ROOT, inventory
from english_review_gate import check_paper


class EnglishPaperGateTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.records = {record['id']: record for record in inventory()['papers']}

    def gate(self, paper_id, strict):
        record = self.records[paper_id]
        return check_paper(record, parser.extract_record(record)[1], strict=strict)

    def test_reviewed_paper_passes_its_own_gate_while_the_corpus_gate_refuses(self):
        report, routes = self.gate('english-2026-hl-p1', strict=True)
        self.assertEqual((report['baseTasks'], len(routes)), (19, 20))
        self.assertFalse(any(report['pending'].values()))

    def test_unreviewed_paper_is_refused_with_its_pending_work(self):
        with self.assertRaisesRegex(ValueError, 'refused by its own gate'):
            self.gate('english-2017-hl-p1', strict=True)
        report, _ = self.gate('english-2017-hl-p1', strict=False)
        self.assertTrue(report['pending']['schemeTasks'])
        self.assertTrue(report['pending']['paperReviews'])

    def test_gate_rejects_tasks_from_another_paper(self):
        record = self.records['english-2026-hl-p1']
        foreign = parser.extract_record(self.records['english-2026-hl-p2'])[1]
        with self.assertRaisesRegex(ValueError, 'another paper'):
            check_paper(record, foreign)


class EnglishPublisherTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.outputs, cls.published, cls.refused = publish.publish()

    def test_generated_files_are_current(self):
        for path, value in self.outputs.items():
            self.assertEqual(path.read_text(), publish.dump(value), str(path.relative_to(ROOT)))

    def test_only_reviewed_non_legacy_papers_publish(self):
        self.assertEqual(len(self.published), 34)
        self.assertEqual(sum(paper['cards'] for paper in self.published), 1916)
        reasons = {row['paperId']: row['reason'] for row in self.refused}
        for year in range(2021, 2026):
            for level in ('hl', 'ol'):
                for paper in (1, 2):
                    self.assertIn('legacy', reasons[f'english-{year}-{level}-p{paper}'])
        for paper_id in ('english-2016-hl-p2', 'english-2017-ol-p1', 'english-2019-hl-p2'):
            self.assertNotIn(paper_id, {paper['paperId'] for paper in self.published})
            self.assertIn(paper_id, reasons)

    def test_each_card_names_its_years_grid_and_reviewed_scheme_pages(self):
        reviews = json.loads((ROOT / 'scripts/markbank/authored/english-task-review.json').read_text())['tasks']
        for level in ('higher', 'ordinary'):
            manifest = self.outputs[publish.CARDS_DIR / f'published-{level}.json']
            for card in manifest['cards']:
                task_id = card.get('choiceParentId', card['id'])
                self.assertEqual(card['schemePages'], reviews[task_id]['schemePages'], card['id'])
                self.assertEqual(card['assessment']['grid'], f"{card['year']}-{card['level']}")
                self.assertEqual(card['assessment']['grid'] in manifest['grids']['sittings'], True)

    def test_grid_transcription_is_bound_to_the_printed_cells(self):
        grids = json.loads(publish.GRIDS.read_text())
        broken = copy.deepcopy(grids)
        broken['families']['ol-a-to-ng']['combined']['10']['total'][-1] = '0-1'
        with self.assertRaisesRegex(ValueError, 'not printed'):
            publish.verify_grids(broken, inventory()['papers'])
        swapped = copy.deepcopy(grids)
        swapped['sittings']['2015-ordinary']['schemeSha256'] = '0' * 64
        with self.assertRaisesRegex(ValueError, 'different scheme'):
            publish.verify_grids(swapped, inventory()['papers'])

    def test_cap_rules_follow_each_years_criteria_page(self):
        sittings = json.loads(publish.GRIDS.read_text())['sittings']
        kinds = {key: value['capRule']['kind'] for key, value in sittings.items()}
        for year in range(2010, 2016):
            self.assertEqual(kinds[f'{year}-higher'], 'none')
            self.assertEqual(kinds[f'{year}-ordinary'], 'language-at-d-band')
        for key in ('2016-higher', '2016-ordinary', '2018-higher', '2026-higher', '2026-ordinary'):
            self.assertEqual(kinds[key], 'purpose-primacy')
        self.assertEqual(kinds['2018-ordinary'], 'none')

    def test_legacy_parents_receive_reviewed_companion_readers(self):
        attachments = json.loads((ROOT / 'scripts/markbank/authored/english-source-review.json').read_text())
        fake = copy.deepcopy(attachments)
        fake['attachments']['english-2024-ol-p2-single-a-q1-b'] = {
            'kind': 'source-text', 'additionalSources': [{
                'kind': 'source-text', 'label': 'PRESCRIBED POEM', 'title': 'Inversnaid', 'pages': [20],
                'attribution': 'Inversnaid — Gerard Manley Hopkins.', 'sourcePaperId': 'english-2021-ol-p2',
                'sourceSha256': next(r for r in inventory()['papers'] if r['id'] == 'english-2021-ol-p2')['questionPaper']['sha256'],
            }]}
        original = publish.read

        def patched(path):
            return fake if path.name == 'english-source-review.json' else original(path)
        with mock.patch.object(publish, 'read', side_effect=patched):
            aggregated = publish.legacy_additional_sources()
        self.assertEqual(list(aggregated), ['english-2024-ol-p2-single-a-q1'])
        self.assertEqual(aggregated['english-2024-ol-p2-single-a-q1'][0]['sourceYear'], 2021)
        self.assertEqual(publish.legacy_additional_sources(), {})


if __name__ == '__main__':
    unittest.main()
