"""Paper-by-paper English publication: only a paper's own strict gate can ship it."""
import copy
import json
import unittest
from unittest import mock

import english_choices
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
        self.assertEqual((report['baseTasks'], len(routes)), (19, 19))
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

    def test_only_reviewed_papers_publish_and_legacy_papers_need_a_bridge(self):
        self.assertEqual(len(self.published), 36)
        self.assertEqual(sum(paper['cards'] for paper in self.published), 1329)
        self.assertEqual(sum(paper['printedDuplicates'] for paper in self.published), 6)
        reasons = {row['paperId']: row['reason'] for row in self.refused}
        bridged = {'english-2025-hl-p1', 'english-2025-hl-p2'}
        for year in range(2021, 2026):
            for level in ('hl', 'ol'):
                for paper in (1, 2):
                    paper_id = f'english-{year}-{level}-p{paper}'
                    if paper_id in bridged:
                        self.assertIn(paper_id, {row['paperId'] for row in self.published})
                    else:
                        self.assertIn('legacy', reasons[paper_id])
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
        for key in ('2016-higher', '2016-ordinary', '2018-higher', '2025-higher', '2026-higher', '2026-ordinary'):
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


class EnglishPrintedChoiceRefusalTest(unittest.TestCase):
    """Route cards that differ only in a choice label, and undeclared repeats, never publish."""

    def setUp(self):
        self.records = {record['id']: record for record in inventory()['papers']}
        self.decisions = json.loads((ROOT / 'scripts/markbank/authored/english-selection-review.json').read_text())['decisions']

    def test_label_only_route_group_is_refused(self):
        key = 'english-2026-hl-p1'
        original = publish.check_paper
        decision = dict(self.decisions[key + '-composing-5'], kind='finite')
        decision['expectedRoutes'] = decision.pop('printedChoices')

        def as_routes(record, tasks, strict=False):
            report, routes = original(record, tasks, strict=strict)
            if record['id'] == key:
                task = next(t for t in tasks if t['id'] == key + '-composing-5')
                routes = [r for r in routes if r['id'] != task['id']] + english_choices.expand(task, decision)
            return report, routes
        with mock.patch.object(publish, 'check_paper', side_effect=as_routes):
            with self.assertRaisesRegex(ValueError, 'differ only in a choice label'):
                publish.publish()

    def test_routes_that_differ_in_marking_content_are_allowed(self):
        base = {'id': 'x-route-selection-1', 'choiceParentId': 'x', 'choiceLabel': 'Selected task: A',
                'questionRef': 'Q · Selected task: A', 'questionText': 'Q\n\nFor this practice response — Selected task: A.',
                'assessment': {'mode': 'combined', 'grid': 'g'}}
        other = dict(base, id='x-route-selection-2', choiceLabel='Selected task: B', questionRef='Q · Selected task: B',
                     questionText='Q\n\nFor this practice response — Selected task: B.')
        with self.assertRaisesRegex(ValueError, 'differ only in a choice label'):
            publish.refuse_label_only_routes([base, other])
        publish.refuse_label_only_routes([base, dict(other, assessment={'mode': 'discrete', 'grid': 'g'})])

    def test_printed_duplicates_are_declared_and_identical(self):
        card = {'id': 'k-t1', 'questionText': 'Same', 'totalMarks': 10, 'atlas': {'fileid': 'f', 'n': '8'}}
        twin = dict(card, id='k-t2', atlas={'fileid': 'f', 'n': '10'})
        with self.assertRaisesRegex(ValueError, 'declare it in english-printed-duplicates.json'):
            publish.merge_printed_duplicates('k', [card, twin], {})
        kept, dropped = publish.merge_printed_duplicates(
            'k', [dict(card), dict(twin)], {'k-t2': {'canonical': 'k-t1', 'reason': 'printed twice'}})
        self.assertEqual(([c['id'] for c in kept], dropped), (['k-t1'], 1))
        self.assertEqual(kept[0]['atlasPlacements'], [{'fileid': 'f', 'n': '10'}])
        with self.assertRaisesRegex(ValueError, 'differs from'):
            publish.merge_printed_duplicates('k', [card, dict(twin, totalMarks=15)],
                                             {'k-t2': {'canonical': 'k-t1', 'reason': 'printed twice'}})


class EnglishLegacyBridgeTest(unittest.TestCase):
    """A bridged legacy paper keeps every legacy id: on the published card or as an alias."""

    @classmethod
    def setUpClass(cls):
        cls.outputs, cls.published, _ = publish.publish()
        cls.bridge = json.loads(publish.LEGACY_BRIDGE.read_text())
        cls.legacy = json.loads((publish.CARDS_DIR / 'authored.json').read_text())
        cls.records = {record['id']: record for record in inventory()['papers']}

    def emitted(self, paper_id):
        manifest = self.outputs[publish.CARDS_DIR / 'published-higher.json']
        return [copy.deepcopy(card) for card in manifest['cards'] if card['id'].startswith(paper_id + '-')]

    def apply(self, paper_id, bridge=None):
        bridge = bridge or self.bridge['papers'][paper_id]
        publish.apply_bridge(paper_id, bridge, self.records[paper_id], self.emitted(paper_id), self.legacy)

    def test_every_legacy_id_survives(self):
        manifest = self.outputs[publish.CARDS_DIR / 'published-higher.json']
        published = {card['id'] for card in manifest['cards']}
        aliases = publish.card_aliases()
        self.assertEqual(manifest['bridgedPapers'], ['english-2025-hl-p1', 'english-2025-hl-p2'])
        legacy_ids = sorted(card['id'] for card in self.legacy['cards'] if card['id'].startswith('english-2025-hl-'))
        self.assertEqual(manifest['bridgedLegacyIds'], legacy_ids)
        self.assertEqual(len(legacy_ids), 42)
        kept = [cid for cid in legacy_ids if cid in published]
        aliased = {cid: aliases[cid] for cid in legacy_ids if cid not in published}
        self.assertEqual((len(kept), len(aliased)), (38, 4))
        self.assertEqual(aliased, manifest['bridgeAliases'])
        self.assertTrue(all(target in published for target in aliased.values()))

    def test_lifted_indicative_material_reaches_only_its_cards(self):
        manifest = self.outputs[publish.CARDS_DIR / 'published-higher.json']
        carrying = sorted(card['id'] for card in manifest['cards'] if card.get('indicativeMaterial'))
        self.assertEqual(carrying, sorted(f'english-2025-hl-p1-t{n}-a-{part}' for n in (1, 2, 3) for part in ('i', 'iii')))

    def test_bridge_refuses_a_missing_legacy_card(self):
        bridge = copy.deepcopy(self.bridge['papers']['english-2025-hl-p2'])
        del bridge['legacyCards']['english-2025-hl-p2-unseen-q2']
        with self.assertRaisesRegex(ValueError, 'exactly its legacy cards'):
            self.apply('english-2025-hl-p2', bridge)

    def test_bridge_refuses_an_unregistered_alias(self):
        with mock.patch.object(publish, 'card_aliases', return_value={}):
            with self.assertRaisesRegex(ValueError, 'register the progress alias'):
                self.apply('english-2025-hl-p2')

    def test_bridge_refuses_a_same_id_without_its_card(self):
        bridge = copy.deepcopy(self.bridge['papers']['english-2025-hl-p2'])
        bridge['legacyCards']['english-2025-hl-p2-unseen-q1'] = {'kind': 'same-id', 'reason': 'test'}
        with self.assertRaisesRegex(ValueError, 'publishes no such card'):
            self.apply('english-2025-hl-p2', bridge)

    def test_bridge_refuses_a_different_printed_task(self):
        bridge = copy.deepcopy(self.bridge['papers']['english-2025-hl-p2'])
        bridge['legacyCards']['english-2025-hl-p2-unseen-q1']['to'] = 'english-2025-hl-p2-prescribed-1'
        with mock.patch.object(publish, 'card_aliases', return_value={
                **publish.card_aliases(), 'english-2025-hl-p2-unseen-q1': 'english-2025-hl-p2-prescribed-1'}):
            with self.assertRaisesRegex(ValueError, 'not the same printed task'):
                self.apply('english-2025-hl-p2', bridge)

    def test_bridge_refuses_written_indicative_material(self):
        bridge = copy.deepcopy(self.bridge['papers']['english-2025-hl-p1'])
        bridge['legacyCards']['english-2025-hl-p1-t1-a-i']['indicativeMaterial']['items'][0] = (
            'It can heighten empathy or create an emotional bias towards the underdog.')
        with self.assertRaisesRegex(ValueError, 'not printed on scheme'):
            self.apply('english-2025-hl-p1', bridge)


if __name__ == '__main__':
    unittest.main()
