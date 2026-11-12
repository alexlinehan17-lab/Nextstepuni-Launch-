"""Portable Python half of the exact Russian joint-question topic contract."""
import copy
import json
import unittest
from pathlib import Path
from ru_joint_tasks import validate_joint_task

ROOT = Path(__file__).resolve().parents[3]


class JointQuestionTopicContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        read = lambda path: json.loads((ROOT / path).read_text())
        cls.registry = read('scripts/markbank/authoring/russian-joint-tasks.json')
        cls.source = next(s for s in read('scripts/markbank/authoring/russian-reviewed-sources.json') if s['id'] == 'ru-2011-hl-c2')
        cls.card = next(c for c in read('components/MarkBank/cards/russian/reviewed.json') if c['id'] == cls.source['id'])

    def fixture(self):
        source, card, registry = copy.deepcopy((self.source, self.card, self.registry))
        registry['tasks'] = [next(t for t in registry['tasks'] if t['id'] == card['id'])]
        for i, q in enumerate(registry['tasks'][0]['questions']):
            q['topicId'] = 'russian-1-0' if i % 2 else 'russian-0-3'
            q['additionalTopicIds'] = []
        self.sync(source, registry)
        card['topicId'] = 'russian-1-0'
        card['additionalTopicIds'] = ['russian-0-3']
        return source, card, registry

    @staticmethod
    def sync(source, registry):
        source['atlasQuestions'] = [{k: copy.deepcopy(v) for k, v in q.items() if k != 'leafKey'} for q in registry['tasks'][0]['questions']]

    def test_legacy_mapping_and_inputs_are_unchanged(self):
        before = copy.deepcopy((self.source, self.card, self.registry))
        expected = validate_joint_task(self.source, self.card, self.registry)
        self.assertEqual([q['n'] for q in expected['questions']], ['c2-1', 'c2-2', 'c2-3', 'c2-4'])
        self.assertEqual((self.source, self.card, self.registry), before)

    def test_complete_explicit_topics_are_accepted(self):
        self.assertIsNotNone(validate_joint_task(*self.fixture()))

    def test_missing_duplicate_extra_or_whitespace_topic_annotations_are_rejected(self):
        for mutate in [
            lambda q: q.pop('topicId'),
            lambda q: q.pop('additionalTopicIds'),
            lambda q: q.update(topicId=''),
            lambda q: q.update(topicId=' russian-0-3'),
            lambda q: q.update(additionalTopicIds=[q['topicId']]),
            lambda q: q.update(additionalTopicIds=['russian-1-0', 'russian-0-9']),
        ]:
            source, card, registry = self.fixture()
            mutate(registry['tasks'][0]['questions'][0]); self.sync(source, registry)
            with self.assertRaises(AssertionError): validate_joint_task(source, card, registry)

    def test_whole_card_topic_union_cannot_lose_or_add_topics(self):
        for topics in [[], ['russian-0-3', 'russian-0-3'], ['russian-0-3', 'russian-0-9']]:
            source, card, registry = self.fixture(); card['additionalTopicIds'] = topics
            with self.assertRaises(AssertionError): validate_joint_task(source, card, registry)

    def test_source_topics_cannot_disagree_with_the_reviewed_manifest(self):
        source, card, registry = self.fixture()
        source['atlasQuestions'][0]['topicId'] = 'russian-0-9'
        with self.assertRaises(AssertionError): validate_joint_task(source, card, registry)

    def test_missing_or_out_of_scope_pages_and_duplicate_identities_are_rejected(self):
        for mutate in [
            lambda q: q[0].update(n=''),
            lambda q: q[1].update(n=q[0]['n']),
            lambda q: q[1].update(questionRef=q[0]['questionRef']),
            lambda q: q[0].update(questionPages=[]),
            lambda q: q[0].update(questionPages=[99]),
            lambda q: q[0].update(schemePages=[8, 8]),
            lambda q: q[0].update(schemePages=['8']),
        ]:
            source, card, registry = self.fixture()
            mutate(registry['tasks'][0]['questions']); self.sync(source, registry)
            source['coveredQuestionRefs'] = [q['questionRef'] for q in source['atlasQuestions']]
            with self.assertRaises(AssertionError): validate_joint_task(source, card, registry)


if __name__ == '__main__': unittest.main()
