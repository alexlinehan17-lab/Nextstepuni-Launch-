"""Pin independent visual tallies; these tests do not replace scheme review."""
import copy
import json
import unittest
from itertools import combinations, permutations
from unittest import mock

import english_full_cards as full_cards
from english_choices import enumerate_choices, fingerprint, review
from english_complete import ROOT, inventory
from english_full_cards import extract_record
from english_task_review import reconcile as reconcile_schemes, task_fingerprint


class VisuallyReviewedEnglishPapersTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        records = inventory()['papers']
        cls.tasks = {year: extract_record(next(r for r in records if r['id'] == f'english-{year}-ol-p2'))[1]
                     for year in (2010, 2011, 2012, 2013, 2014, 2015, 2018)}
        cls.decisions = json.loads((ROOT / 'scripts/markbank/authored/english-selection-review.json').read_text())['decisions']

    def routes(self, year):
        tasks = self.tasks[year]
        decisions = {task['id']: self.decisions[task['id']] for task in tasks if task['id'] in self.decisions}
        routes, missing = enumerate_choices(tasks, decisions)
        self.assertEqual(missing, [])
        return routes

    def test_2013_independent_tally_and_inherited_aspect_choices(self):
        self.assertEqual(len(self.tasks[2013]), 90)
        routes = self.routes(2013)
        self.assertEqual(len(routes), 107)
        aspects = [r for r in routes if '-comparative-b-' in r['id']]
        self.assertEqual(len(aspects), 15)
        self.assertEqual(sorted(r['totalMarks'] for r in aspects), [20] * 6 + [30] * 6 + [40] * 3)
        for route in aspects:
            self.assertIn('parentQuestionText', route)
            self.assertIn(route['choiceRoute']['selections']['selection'][0], ('1', '2', '3'))
        part = next(t for t in self.tasks[2013] if t['id'].endswith('-comparative-a-q1-b'))
        self.assertEqual(part['schemePage'], 32)
        self.assertEqual(part['totalMarks'], 40)

    def test_2018_named_character_routes_and_flexible_phrase_count(self):
        self.assertEqual(len(self.tasks[2018]), 92)
        routes = self.routes(2018)
        self.assertEqual(len(routes), 104)
        characters = [r for r in routes if '-single-' in r['id'] and '-q3-iii-route-' in r['id']]
        self.assertEqual(len(characters), 18)
        self.assertTrue(all(r['totalMarks'] == 30 for r in characters))
        flexible = [r for r in routes if '-single-' in r['id'] and r['id'].endswith('-q3-ii')]
        self.assertEqual(len(flexible), 9)
        self.assertTrue(all('choiceRoute' not in r for r in flexible))

    def test_2010_closed_groups_and_inherited_stanza_exclusion(self):
        self.assertEqual(len(self.tasks[2010]), 89)
        routes = self.routes(2010)
        self.assertEqual(len(routes), 115)
        for suffix in ('single-b-q1-b', 'prescribed-d-q1-b', 'prescribed-d-q1-c'):
            variants = [r for r in routes if r.get('choiceParentId') == 'english-2010-ol-p2-' + suffix]
            self.assertEqual(len(variants), 5)
            self.assertEqual({r['totalMarks'] for r in variants}, {10})
        exclusions = [r for r in routes if r.get('choiceParentId') == 'english-2010-ol-p2-prescribed-d-q1-c']
        for route in exclusions:
            self.assertIn('exclude its images here', route['questionText'])
            self.assertIn('1(b)', route['parentQuestionText'])
            self.assertEqual(route['sourceMaterial']['pages'], [16])
        for task in self.tasks[2010]:
            self.assertNotIn('(continued)', task['questionText'])
            if '-comparative-' in task['id']:
                self.assertIn('name the texts', task['contextNotes'][0])

    def test_sources_exclude_question_only_and_next_poem_pages(self):
        expected = {2011: {'a': 11, 'b': 13, 'c': 15, 'd': 16},
                    2012: {'a': 12, 'b': 14, 'c': 16, 'd': 18},
                    2013: {'a': 11, 'b': 13, 'c': 15, 'd': 17},
                    2014: {'a': 12, 'b': 14, 'c': 16, 'd': 18},
                    2015: {'a': 12, 'b': 14, 'c': 16, 'd': 18},
                    2018: {'a': 14, 'b': 15, 'c': 16, 'd': 17}}
        for year, poems in expected.items():
            for letter, page in poems.items():
                tasks = [t for t in self.tasks[year] if f'-prescribed-{letter}-' in t['id']]
                self.assertEqual(len(tasks), 6)
                self.assertTrue(all(t['sourceMaterial']['pages'] == [page] for t in tasks))
        unseen = next(t for t in self.tasks[2013] if '-unseen-' in t['id'])
        self.assertEqual(unseen['sourceMaterial']['title'], 'Earbud')
        self.assertEqual(unseen['sourceMaterial']['pages'], [10])

    def test_2010_named_studied_poems_have_attributed_readers(self):
        task = next(t for t in self.tasks[2010] if t['id'].endswith('-prescribed-d-q2-iii'))
        source = task['sourceMaterial']
        self.assertEqual(source['kind'], 'supplementary-text')
        self.assertEqual(source['pages'], [])
        self.assertEqual([t['title'] for t in source['texts']], [
            'The Lake Isle of Innisfree', 'An Irish Airman Foresees his Death'])
        self.assertEqual([[len(s) for s in t['stanzas']] for t in source['texts']], [[4, 4, 4], [16]])
        self.assertIn('not printed in the 2010 examination paper', source['presentationNote'])
        self.assertFalse(any('official source material' in x for x in task['taskRequirements']))

    def test_2011_closed_groups_and_required_second_poem(self):
        self.assertEqual(len(self.tasks[2011]), 91)
        routes = self.routes(2011)
        self.assertEqual(len(routes), 111)
        for suffix, count, marks in [('single-g-q3-i', 5, 30), ('prescribed-d-q2-ii', 3, 20)]:
            variants = [r for r in routes if r.get('choiceParentId') == 'english-2011-ol-p2-' + suffix]
            self.assertEqual(len(variants), count)
            self.assertEqual(len({r['id'] for r in variants}), count)
            self.assertEqual({r['totalMarks'] for r in variants}, {marks})
        task = next(t for t in self.tasks[2011] if t['id'].endswith('-prescribed-d-q2-iii'))
        self.assertEqual((task['sourceMaterial']['title'], task['sourceMaterial']['pages']), ('Spring', [16]))
        companion, = task['additionalSourceMaterials']
        self.assertEqual((companion['title'], companion['sourceYear'], companion['pages']), ('Inversnaid', 2021, [20]))
        self.assertEqual(companion['sourceFileid'], 'LC002GLP200EV.pdf')
        self.assertIn('not printed there', companion['presentationNote'])

    def test_2012_routes_keep_exact_openings_and_complete_poems(self):
        tasks = self.tasks[2012]
        routes = self.routes(2012)
        self.assertEqual((len(tasks), len(routes)), (90, 113))
        self.assertEqual(len({r['id'] for r in routes}), 113)
        prefix = 'english-2012-ol-p2-'
        openings = {
            'single-a-q3-ii': ['I would like to live in Emma’s world because ...',
                               'I would not like to live in Emma’s world because ...'],
            'single-e-q3-ii': ['I would like to live in Nora’s world because ...',
                               'I would not like to live in Nora’s world because ...'],
            'single-g-q3-ii': ['I think this play would make a good film because…',
                               'I do not think this play would make a good film because…'],
            'single-h-q3-iii': ['I would find it exciting to live in Elsinore in Hamlet’s time because...',
                                'I would find it frightening to live in Elsinore in Hamlet’s time because...'],
            'single-i-q3-ii': ['I think this novel would make a good film because…',
                               'I do not think this novel would make a good film because…'],
        }
        for suffix, wording in openings.items():
            variants = [r for r in routes if r.get('choiceParentId') == prefix + suffix]
            self.assertEqual(len(variants), 2)
            for index, (route, text) in enumerate(zip(variants, wording), 1):
                self.assertEqual(route['id'], prefix + suffix + f'-route-selection-{index}')
                self.assertEqual(route['totalMarks'], 30)
                self.assertIn(text, route['choiceRoute']['label'])
                self.assertIn(text, route['questionText'])
        for suffix in ('single-b-q3-ii', 'single-c-q3-ii', 'single-f-q3-iii', 'single-i-q3-iii'):
            variants = [r for r in routes if r.get('choiceParentId') == prefix + suffix]
            self.assertEqual((len(variants), {r['totalMarks'] for r in variants}), (3, {30}))
        for suffix in ('prescribed-a-q2-ii', 'prescribed-b-q2-iii', 'prescribed-c-q2-ii', 'prescribed-d-q2-ii'):
            variants = [r for r in routes if r.get('choiceParentId') == prefix + suffix]
            self.assertEqual((len(variants), {r['totalMarks'] for r in variants}), (3, {20}))
        attitudes = [r for r in routes if r.get('choiceParentId') == prefix + 'prescribed-d-q1-c']
        self.assertEqual((len(attitudes), {r['totalMarks'] for r in attitudes}), (2, {10}))
        unseen = [t for t in tasks if '-unseen-' in t['id']]
        self.assertEqual(len(unseen), 2)
        for task in unseen:
            self.assertEqual((task['sourceMaterial']['title'], task['sourceMaterial']['pages']), ('Shoulders', [11]))
            self.assertEqual(task['totalMarks'], 10)
        sun = next(t for t in tasks if t['id'] == prefix + 'prescribed-b-q1-c')
        self.assertTrue(sun['questionText'].startswith('or have you too gone crazy for power, for things?'))
        self.assertEqual(self.decisions[prefix + 'comparative-a-q2-b']['kind'], 'open')
        self.assertIn('equally', self.decisions[prefix + 'comparative-a-q2-b']['reason'])

    def test_2014_preferences_preserve_every_route_and_named_reading(self):
        tasks = self.tasks[2014]
        routes = self.routes(2014)
        self.assertEqual((len(tasks), len(routes)), (90, 117))
        self.assertEqual(len({r['id'] for r in routes}), 117)
        prefix = 'english-2014-ol-p2-'
        for letter in 'abcdefghi':
            variants = [r for r in routes if r.get('choiceParentId') == prefix + f'single-{letter}-q1-b']
            self.assertEqual((len(variants), {r['totalMarks'] for r in variants}), (3, {10}))
        for suffix, count, marks in [('single-e-q3-i', 3, 30), ('comparative-b-q1-a', 2, 30),
                                     ('prescribed-a-q2-iii', 3, 20), ('prescribed-b-q2-ii', 3, 20),
                                     ('prescribed-c-q2-iii', 3, 20)]:
            variants = [r for r in routes if r.get('choiceParentId') == prefix + suffix]
            self.assertEqual((len(variants), {r['totalMarks'] for r in variants}), (count, {marks}))
            for index, route in enumerate(variants, 1):
                self.assertEqual(route['id'], prefix + suffix + f'-route-selection-{index}')
        heaney = [r for r in routes if r.get('choiceParentId') == prefix + 'prescribed-a-q2-iii']
        for route in heaney:
            self.assertEqual(route['sourceMaterial']['title'], 'The Underground')
            self.assertEqual([(s['title'], s['sourceYear'], s['pages']) for s in route['additionalSourceMaterials']],
                             [('A Constable Calls', 2012, [12]), ('A Call', 2024, [16])])
        plath = [r for r in routes if r.get('choiceParentId') == prefix + 'prescribed-c-q2-iii']
        for route in plath:
            self.assertEqual(route['sourceMaterial']['title'], 'Child')
            reading, = route['additionalSourceMaterials']
            self.assertEqual(reading['kind'], 'linked-reading')
            self.assertEqual(reading['pages'], [])
            self.assertEqual([r['title'] for r in reading['readings']], ['Poppies in July', 'The Arrival of the Bee Box'])
            self.assertTrue(reading['readings'][0]['sourceUrl'].endswith('#page=54'))
            self.assertTrue(reading['readings'][1]['sourceUrl'].endswith('#page=12'))
        for suffix in ('prescribed-b-q2-i', 'prescribed-c-q2-ii', 'prescribed-d-q2-iii'):
            self.assertEqual(self.decisions[prefix + suffix]['kind'], 'flexible')
        for letter in 'ehi':
            diary = next(r for r in routes if r['id'] == prefix + f'single-{letter}-q3-iii')
            self.assertEqual(diary['totalMarks'], 30)
            self.assertIn('two diary entries', diary['questionText'])

    def test_2015_closed_statements_and_open_comparison_focus(self):
        tasks = self.tasks[2015]
        routes = self.routes(2015)
        self.assertEqual((len(tasks), len(routes), len({r['id'] for r in routes})), (92, 128, 128))
        prefix = 'english-2015-ol-p2-'
        for letter, roman in zip('abcdefghi', ['ii', 'i', 'i', 'ii', 'i', 'ii', 'i', 'iii', 'i']):
            variants = [r for r in routes if r.get('choiceParentId') == prefix + f'single-{letter}-q3-{roman}']
            self.assertEqual((len(variants), {r['totalMarks'] for r in variants}), (3, {30}))
            for index, route in enumerate(variants, 1):
                self.assertEqual(route['id'], prefix + f'single-{letter}-q3-{roman}-route-selection-{index}')
                self.assertIn('It is a ', route['choiceRoute']['label'])
        for letter, q, count in [('a', 2, 2), ('b', 1, 2), ('b', 2, 3)]:
            for roman in ['i', 'ii']:
                variants = [r for r in routes if r.get('choiceParentId') == prefix + f'comparative-{letter}-q{q}-a-{roman}']
                self.assertEqual((len(variants), {r['totalMarks'] for r in variants}), (count, {15}))
            comparison, = [r for r in routes if r['id'] == prefix + f'comparative-{letter}-q{q}-b']
            self.assertEqual(comparison['totalMarks'], 40)
            self.assertIn('parentQuestionText', comparison)
            self.assertNotIn('choiceRoute', comparison)
        for suffix in ['prescribed-a-q1-c', 'prescribed-a-q2-ii', 'prescribed-b-q2-i',
                       'prescribed-b-q2-ii', 'prescribed-c-q2-iii', 'prescribed-d-q2-ii']:
            self.assertEqual(self.decisions[prefix + suffix]['kind'], 'flexible')
        memory = [r for r in routes if r.get('choiceParentId') == prefix + 'prescribed-d-q2-iii']
        self.assertEqual(len(memory), 3)
        self.assertIn('memory', memory[0]['choiceRoute']['label'])
        self.assertNotIn('memories', memory[0]['questionText'])
        for task in tasks:
            self.assertNotIn('Question continues', task['questionText'])
            if '-unseen-' in task['id']:
                self.assertEqual((task['sourceMaterial']['title'], task['sourceMaterial']['pages']), ('Today', [11]))

    def test_reviewed_scheme_evidence_remains_current(self):
        ledger = json.loads((ROOT / 'scripts/markbank/authored/english-task-review.json').read_text())
        for year in (2010, 2011, 2012, 2013, 2014, 2015, 2018):
            subset = {'tasks': {key: value for key, value in ledger['tasks'].items()
                                if key.startswith(f'english-{year}-ol-p2-')}}
            self.assertEqual(reconcile_schemes(self.tasks[year], inventory()['papers'], subset), [])


class EnglishVerifiedRepairsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        keys = ('english-2013-hl-p1', 'english-2013-ol-p1', 'english-2013-hl-p2',
                'english-2010-hl-p1', 'english-2010-ol-p1', 'english-2010-hl-p2',
                'english-2011-hl-p1', 'english-2011-ol-p1', 'english-2011-hl-p2',
                'english-2012-hl-p1', 'english-2012-ol-p1', 'english-2012-hl-p2',
                'english-2014-hl-p1', 'english-2014-ol-p1', 'english-2014-hl-p2',
                'english-2015-hl-p1', 'english-2015-ol-p1', 'english-2015-hl-p2',
                'english-2018-hl-p1', 'english-2018-ol-p1', 'english-2018-hl-p2',
                'english-2016-hl-p1', 'english-2016-ol-p1',
                'english-2016-ol-p2', 'english-2017-ol-p2', 'english-2021-ol-p2',
                'english-2022-hl-p2')
        cls.tasks = {record['id']: extract_record(record)[1] for record in inventory()['papers']
                     if record['id'] in keys}
        cls.by_id = {task['id']: task for tasks in cls.tasks.values() for task in tasks}

    def test_independent_2013_counts(self):
        decisions = json.loads((ROOT / 'scripts/markbank/authored/english-selection-review.json').read_text())['decisions']
        for key, base, routes in [('english-2013-hl-p1', 19, 21), ('english-2013-ol-p1', 22, 32),
                                  ('english-2013-hl-p2', 23, 23)]:
            tasks = self.tasks[key]
            resolved, pending = enumerate_choices(tasks, {t['id']: decisions[t['id']] for t in tasks})
            self.assertEqual((len(tasks), len(resolved), pending), (base, routes, []))

    def test_2014_comprehension_routes_and_shared_visual_context(self):
        decisions = json.loads((ROOT / 'scripts/markbank/authored/english-selection-review.json').read_text())['decisions']
        for level, base, count in [('hl', 19, 20), ('ol', 22, 26)]:
            key = f'english-2014-{level}-p1'
            tasks = self.tasks[key]
            routes, pending = enumerate_choices(tasks, {t['id']: decisions[t['id']] for t in tasks})
            self.assertEqual((len(tasks), len(routes), pending), (base, count, []))
            self.assertEqual(len({r['id'] for r in routes}), count)
            if level == 'hl':
                outline = [r for r in routes if r.get('choiceParentId') == key + '-t2-a-i']
                self.assertEqual((len(outline), {r['totalMarks'] for r in outline}), (2, {15}))
                self.assertEqual(decisions[key + '-t2-a-iii']['kind'], 'open')
                self.assertIn('equally effective', decisions[key + '-t2-a-iii']['reason'])
                self.assertEqual(self.by_id[key + '-t3-b']['sourceMaterial']['pages'], [6, 7])
            else:
                covers = [r for r in routes if r.get('choiceParentId') == key + '-t3-a-iii-b']
                self.assertEqual((len(covers), {r['totalMarks'] for r in covers}), (2, {10}))
                for route in covers:
                    self.assertEqual(route['sourceMaterial']['pages'], [6, 7])
                    self.assertIn('both covers', route['questionText'])
                topics = [r for r in routes if r.get('choiceParentId') == key + '-composing-5']
                self.assertEqual((len(topics), {r['totalMarks'] for r in topics}), (3, {100}))
                self.assertEqual({r['choiceRoute']['label'] for r in topics}, {
                    'Selected task: Ambition', 'Selected task: My home place', 'Selected task: Simple pleasures'})
                self.assertEqual(decisions[key + '-t3-a-ii']['kind'], 'flexible')
                self.assertEqual(decisions[key + '-composing-4']['kind'], 'flexible')
                self.assertEqual(self.by_id[key + '-t1-a-iii-b']['sourceMaterial']['pages'], [2, 3])
                self.assertEqual(self.by_id[key + '-t2-b']['sourceMaterial']['pages'], [4, 5])

    def test_2015_paper_one_routes_keep_required_context(self):
        decisions = json.loads((ROOT / 'scripts/markbank/authored/english-selection-review.json').read_text())['decisions']
        ledger = json.loads((ROOT / 'scripts/markbank/authored/english-task-review.json').read_text())
        for level, base in [('hl', 19), ('ol', 22)]:
            key = f'english-2015-{level}-p1'
            tasks = self.tasks[key]
            routes, pending = enumerate_choices(tasks, {t['id']: decisions[t['id']] for t in tasks})
            self.assertEqual((len(tasks), len(routes), pending), (base, 25, []))
            self.assertEqual(len({r['id'] for r in routes}), 25)
            subset = {'tasks': {t['id']: ledger['tasks'][t['id']] for t in tasks}}
            self.assertEqual(reconcile_schemes(tasks, inventory()['papers'], subset), [])
            pools = [('t2-b', 6, 50), ('composing-5', 2, 100)] if level == 'hl' else [
                ('t2-a-iii-b', 2, 10), ('t2-b', 2, 50), ('t3-a-iii-a', 2, 10)]
            for suffix, count, marks in pools:
                variants = [r for r in routes if r.get('choiceParentId') == key + '-' + suffix]
                self.assertEqual((len(variants), {r['totalMarks'] for r in variants}), (count, {marks}))
                for index, route in enumerate(variants, 1):
                    self.assertEqual(route['id'], key + '-' + suffix + f'-route-selection-{index}')
            if level == 'hl':
                both = self.by_id[key + '-t2-a-iii']
                self.assertEqual(both['sourceMaterial']['pages'], [4, 5])
                self.assertIn('both of the book covers and to the written text', both['questionText'])
            else:
                for suffix, pages in [('t2-a-i', [4, 5]), ('t2-a-iii-b', [4]),
                                      ('t3-a-iii-a', [7]), ('t3-a-iii-b', [6, 7])]:
                    self.assertEqual(self.by_id[key + '-' + suffix]['sourceMaterial']['pages'], pages)
                self.assertIn('two diary entries', self.by_id[key + '-t3-b']['questionText'])
                self.assertEqual(self.by_id[key + '-t3-b']['totalMarks'], 50)
                for text in range(1, 4):
                    self.assertEqual(decisions[key + f'-t{text}-a-ii']['kind'], 'flexible')

    def test_2016_paper_one_routes_tariffs_and_readers(self):
        decisions = json.loads((ROOT / 'scripts/markbank/authored/english-selection-review.json').read_text())['decisions']
        ledger = json.loads((ROOT / 'scripts/markbank/authored/english-task-review.json').read_text())
        for level, base, total in [('hl', 19, 34), ('ol', 22, 39)]:
            key = f'english-2016-{level}-p1'
            tasks = self.tasks[key]
            routes, pending = enumerate_choices(tasks, {t['id']: decisions[t['id']] for t in tasks})
            self.assertEqual((len(tasks), len(routes), len({r['id'] for r in routes}), pending), (base, total, total, []))
            subset = {'tasks': {t['id']: ledger['tasks'][t['id']] for t in tasks}}
            self.assertEqual(reconcile_schemes(tasks, inventory()['papers'], subset), [])
            pools = [('t1-a-ii', 4, 15), ('t1-b', 12, 50), ('composing-5', 2, 100)] if level == 'hl' else [
                ('t1-a-ii', 2, 15), ('t1-a-iii-a', 2, 10), ('t2-a-iii-a', 4, 10), ('t2-b', 2, 50),
                ('t3-a-iii-b', 2, 10), ('t3-b', 2, 50), ('composing-4', 10, 100)]
            for suffix, count, marks in pools:
                variants = [r for r in routes if r.get('choiceParentId') == key + '-' + suffix]
                # Every alternative keeps the route tariff; marks are never added together.
                self.assertEqual((len(variants), {r['totalMarks'] for r in variants}), (count, {marks}))
                parent = self.by_id[key + '-' + suffix]
                for route in variants:
                    self.assertTrue(route['questionText'].startswith(parent['questionText']))
                    self.assertEqual(route.get('sourceMaterial'), parent.get('sourceMaterial'))
            self.assertEqual(len([r for r in routes if 'choiceParentId' not in r]), base - len(pools))
            for task in tasks:
                criteria = ledger['tasks'][task['id']]['criteria']
                if task['totalMarks'] in (50, 100):
                    self.assertEqual(criteria['mode'], 'discrete')
                    self.assertIn('cannot exceed Purpose', criteria['notes'])
                    self.assertIn('PDF40' if level == 'hl' else 'PDF52', criteria['notes'])
                elif level == 'hl':
                    self.assertEqual(criteria['mode'], 'holistic')
                    self.assertNotIn('allocation', criteria)
                else:
                    self.assertEqual(criteria['allocation'], {'P+C': task['totalMarks'] * 6 // 10,
                                                              'L+M': task['totalMarks'] * 4 // 10})
        hl, ol = 'english-2016-hl-p1-', 'english-2016-ol-p1-'
        posters = enumerate_choices([self.by_id[hl + 't1-b']], {hl + 't1-b': decisions[hl + 't1-b']})[0]
        self.assertEqual({(r['choiceRoute']['selections']['first'][0], r['choiceRoute']['selections']['second'][0])
                          for r in posters}, set(permutations('1234', 2)))
        self.assertTrue(all(r['sourceMaterial']['pages'] == [2] for r in posters))
        virtues = enumerate_choices([self.by_id[ol + 'composing-4']], {ol + 'composing-4': decisions[ol + 'composing-4']})[0]
        self.assertEqual({tuple(r['choiceRoute']['selections']['virtues']) for r in virtues},
                         set(combinations('12345', 2)))
        self.assertEqual([o['text'] for o in decisions[ol + 'composing-4']['pools'][0]['options']],
                         ['Kindness', 'Patience', 'Generosity', 'Tolerance', 'Forgiveness'])
        china = enumerate_choices([self.by_id[ol + 't1-a-ii']], {ol + 't1-a-ii': decisions[ol + 't1-a-ii']})[0]
        self.assertEqual([r['id'] for r in china], [ol + 't1-a-ii-route-selection-1', ol + 't1-a-ii-route-selection-2'])
        self.assertIn('A mainly positive view of China', china[0]['questionText'])
        self.assertIn('A mainly negative view of China', china[1]['questionText'])
        self.assertIn('PDF5', decisions[ol + 't1-a-ii']['reason'])
        self.assertEqual(decisions[ol + 't3-a-ii']['kind'], 'open')
        self.assertIn('not a fixed enumerated pool', decisions[ol + 't3-a-ii']['reason'])
        self.assertEqual(decisions[ol + 't1-a-iii-b']['kind'], 'open')
        self.assertIn('either in Ireland or abroad', decisions[ol + 't1-a-iii-b']['reason'])
        self.assertIn('you identity the elements', self.by_id[hl + 't2-b']['questionText'])
        self.assertNotIn('identify', self.by_id[hl + 't2-b']['questionText'])
        expected = {hl + f't{n}-{part}': pages for n, pages in ((1, [2, 3]), (2, [4, 5]), (3, [6, 7]))
                    for part in ('a-i', 'a-ii', 'a-iii', 'b')}
        expected[hl + 't1-b'] = [2]
        expected.update({ol + 't1-a-i': [2, 3], ol + 't1-a-ii': [2, 3], ol + 't1-a-iii-a': [2, 3],
                         ol + 't2-a-i': [4], ol + 't2-a-ii': [4, 5], ol + 't2-a-iii-a': [4, 5],
                         ol + 't2-a-iii-b': [4, 5], ol + 't2-b': [4, 5], ol + 't3-a-i': [6, 7],
                         ol + 't3-a-ii': [6, 7], ol + 't3-a-iii-b': [6, 7]})
        for key in ('english-2016-hl-p1', 'english-2016-ol-p1'):
            for task in self.tasks[key]:
                source = task.get('sourceMaterial')
                self.assertEqual(source and source['pages'], expected.get(task['id']), task['id'])
        for suffix in ('t1-a-iii-b', 't3-a-iii-a', 't1-b', 't3-b'):
            self.assertNotIn('sourceMaterial', self.by_id[ol + suffix])
        self.assertEqual(self.by_id[ol + 't2-a-i']['sourceMaterial']['title'], 'Two Diaries from 1916')

    def test_2015_exactly_two_characters_creates_three_full_tariff_routes(self):
        key = 'english-2015-hl-p2'
        tasks = self.tasks[key]
        decisions = json.loads((ROOT / 'scripts/markbank/authored/english-selection-review.json').read_text())['decisions']
        routes, pending = enumerate_choices(tasks, {t['id']: decisions[t['id']] for t in tasks})
        self.assertEqual((len(tasks), len(routes), pending), (23, 25, []))
        pairs = [r for r in routes if r.get('choiceParentId') == key + '-single-c-ii']
        self.assertEqual({tuple(r['choiceRoute']['selections']['selection']) for r in pairs},
                         {('1', '2'), ('1', '3'), ('2', '3')})
        for pair in pairs:
            self.assertEqual(pair['totalMarks'], 60)
            self.assertIn('steady and relentless erosion', pair['questionText'])
            self.assertEqual(pair['id'], key + '-single-c-ii-route-selection-' +
                             '-'.join(pair['choiceRoute']['selections']['selection']))
        for task in tasks:
            if '-unseen-' in task['id']:
                self.assertEqual((task['sourceMaterial']['title'], task['sourceMaterial']['pages']),
                                 ('Peter Street', [6]))
            if '-prescribed-' in task['id']:
                self.assertTrue(task['questionText'].startswith('“'))

    def test_independent_2018_counts_and_open_speech(self):
        decisions = json.loads((ROOT / 'scripts/markbank/authored/english-selection-review.json').read_text())['decisions']
        for key, base, routes in [('english-2018-hl-p1', 19, 20), ('english-2018-ol-p1', 22, 24),
                                  ('english-2018-hl-p2', 23, 23)]:
            tasks = self.tasks[key]
            resolved, pending = enumerate_choices(tasks, {t['id']: decisions[t['id']] for t in tasks})
            self.assertEqual((len(tasks), len(resolved), pending), (base, routes, []))
        self.assertEqual(decisions['english-2018-hl-p1-composing-7']['kind'], 'open')
        source = self.by_id['english-2018-hl-p1-t3-a-i']['sourceMaterial']
        self.assertEqual(source['pages'], [6])
        self.assertIn('Dead Man’s Dump', source['title'])

    def test_2014_higher_poem_reader_and_flexible_character_minimum(self):
        key = 'english-2014-hl-p2'
        decisions = json.loads((ROOT / 'scripts/markbank/authored/english-selection-review.json').read_text())['decisions']
        tasks = self.tasks[key]
        routes, pending = enumerate_choices(tasks, {t['id']: decisions[t['id']] for t in tasks})
        self.assertEqual((len(tasks), len(routes), pending), (23, 23, []))
        self.assertEqual(decisions[key + '-single-d-i']['kind'], 'flexible')
        self.assertIn('AT LEAST', decisions[key + '-single-d-i']['reason'])
        for suffix in ('q1-a', 'q1-b', 'q2'):
            source = self.by_id[key + '-unseen-' + suffix]['sourceMaterial']
            self.assertEqual((source['title'], source['pages']), ('The Peninsula', [6]))
        self.assertTrue(self.by_id[key + '-prescribed-1']['questionText'].startswith('“Yeats'))
        ledger = json.loads((ROOT / 'scripts/markbank/authored/english-task-review.json').read_text())
        subset = {'tasks': {tid: value for tid, value in ledger['tasks'].items() if tid.startswith(key + '-')}}
        self.assertEqual(reconcile_schemes(tasks, inventory()['papers'], subset), [])

    def test_2010_visual_routes_and_scheme_erratum(self):
        decisions = json.loads((ROOT / 'scripts/markbank/authored/english-selection-review.json').read_text())['decisions']
        for key, base, routes in [('english-2010-hl-p1', 19, 20), ('english-2010-ol-p1', 19, 29),
                                  ('english-2010-hl-p2', 23, 23)]:
            tasks = self.tasks[key]
            resolved, pending = enumerate_choices(tasks, {t['id']: decisions[t['id']] for t in tasks})
            self.assertEqual((len(tasks), len(resolved), pending), (base, routes, []))
        self.assertTrue(self.by_id['english-2010-ol-p1-t1-b']['questionText'].startswith('People need'))
        self.assertEqual(self.by_id['english-2010-hl-p1-t3-a-ii']['sourceMaterial']['pages'], [7])
        self.assertEqual(self.by_id['english-2010-ol-p1-t3-a-ii']['sourceMaterial']['pages'], [6])
        self.assertEqual(self.by_id['english-2010-ol-p1-t3-a-ii']['totalMarks'], 15)
        for suffix in ('q1-a', 'q1-b', 'q2'):
            source = self.by_id['english-2010-hl-p2-unseen-' + suffix]['sourceMaterial']
            self.assertEqual((source['title'], source['pages']), ('Seed', [6]))
            self.assertIn('accepts responses based on either version', source['presentationNote'])
        self.assertTrue(self.by_id['english-2010-hl-p2-prescribed-1']['questionText'].startswith('“Yeats'))

    def test_2011_independent_paper_tallies_and_combined_awards(self):
        decisions = json.loads((ROOT / 'scripts/markbank/authored/english-selection-review.json').read_text())['decisions']
        for key, base, routes in [('english-2011-hl-p1', 19, 20), ('english-2011-ol-p1', 19, 21),
                                  ('english-2011-hl-p2', 23, 23)]:
            tasks = self.tasks[key]
            resolved, pending = enumerate_choices(tasks, {t['id']: decisions[t['id']] for t in tasks})
            self.assertEqual((len(tasks), len(resolved), pending), (base, routes, []))
        for number in (1, 2, 3):
            task = self.by_id[f'english-2011-ol-p1-t{number}-a-iii']
            self.assertEqual(task['totalMarks'], 20)
            self.assertIn('(a)', task['questionText'])
            self.assertIn('(b)', task['questionText'])

    def test_shared_stem_does_not_hide_first_roman_part(self):
        for key in ('english-2016-ol-p2-comparative-b-q1', 'english-2017-ol-p2-comparative-b-q2'):
            first = self.by_id[key + '-a-i']
            self.assertEqual(first['totalMarks'], 15)
            self.assertTrue(first['questionRef'].endswith('(a)(i)'))
            self.assertNotIn('(i)', first['questionText'])
            self.assertIn(first['questionText'].split('.')[0], first['parentQuestionText'])
            self.assertEqual(self.by_id[key + '-a-ii']['totalMarks'], 15)
            self.assertEqual(self.by_id[key + '-b']['totalMarks'], 40)

    def test_2012_image_pools_and_independent_tallies(self):
        decisions = json.loads((ROOT / 'scripts/markbank/authored/english-selection-review.json').read_text())['decisions']
        all_routes = []
        for key, base, routes in [('english-2012-hl-p1', 19, 24), ('english-2012-ol-p1', 22, 35),
                                  ('english-2012-hl-p2', 23, 23)]:
            tasks = self.tasks[key]
            resolved, pending = enumerate_choices(tasks, {t['id']: decisions[t['id']] for t in tasks})
            self.assertEqual((len(tasks), len(resolved), pending), (base, routes, []))
            all_routes.extend(resolved)
        for parent, size, take, marks, pages in [
            ('english-2012-hl-p1-t2-a-iii', 3, 2, 20, [4, 5]),
            ('english-2012-ol-p1-t3-a-i', 5, 3, 15, [6, 7]),
        ]:
            variants = [r for r in all_routes if r.get('choiceParentId') == parent]
            expected = set(combinations([str(i) for i in range(1, size + 1)], take))
            self.assertEqual({tuple(r['choiceRoute']['selections']['selection']) for r in variants}, expected)
            self.assertEqual(len({r['id'] for r in variants}), len(expected))
            for route in variants:
                self.assertEqual(route['totalMarks'], marks)
                self.assertEqual(route['sourceMaterial']['pages'], pages)
                self.assertIn(self.by_id[parent]['questionText'], route['questionText'])
        diary = [r for r in all_routes if r.get('choiceParentId') == 'english-2012-ol-p1-t1-b']
        self.assertEqual(len(diary), 5)
        self.assertTrue(all(r['totalMarks'] == 50 and 'three diary entries' in r['questionText'] for r in diary))
        self.assertEqual(self.by_id['english-2012-ol-p1-t3-a-iii-b']['sourceMaterial']['pages'], [6])
        self.assertEqual(self.by_id['english-2012-ol-p1-t2-b']['sourceMaterial']['pages'], [4, 5])
        self.assertIn('Google', self.by_id['english-2012-ol-p1-t3-a-i']['sourceMaterial']['title'])
        self.assertEqual(self.by_id['english-2012-hl-p2-unseen-q2']['sourceMaterial']['title'], 'The Beautiful Lie')

    def test_repaired_name_and_footer(self):
        self.assertTrue(self.by_id['english-2022-hl-p2-prescribed-4']['questionText'].startswith('“Emily Dickinson’s'))
        self.assertNotIn('Ordinary Level', self.by_id['english-2021-ol-p2-prescribed-e-q2-iii']['questionText'])

    def test_split_unseen_parts_receive_verified_reader(self):
        for suffix in ('q1-a', 'q1-b', 'q2'):
            source = self.by_id['english-2013-hl-p2-unseen-' + suffix]['sourceMaterial']
            self.assertEqual(source['title'], 'The Fist')
            self.assertEqual(source['pages'], [6])


class EnglishSourceExclusionTest(unittest.TestCase):
    """A default reader is removed only on current, source-bound, reasoned evidence."""

    QUESTION = 'Imagine that you have found an old diary that you kept when you were in First Year.'

    def setUp(self):
        self.record = {'questionPaper': {'sha256': 'paper'}}
        self.default = {'kind': 'source-text', 'label': 'TEXT 3', 'title': 'KEEPING A DIARY', 'pages': [6, 7],
                        'attribution': 'As printed.'}
        self.task = {'id': 'english-2016-ol-p1-t3-a-iii-a', 'paper': 1, 'questionText': self.QUESTION,
                     'questionRef': '2016 OL Paper 1 Text 3 QA(iii)(a)', 'totalMarks': 10,
                     'sourceMaterial': dict(self.default), 'taskRequirements': []}
        self.entry = {'kind': full_cards.SOURCE_NOT_REQUIRED, 'paperSha256': 'paper',
                      'questionSha256': fingerprint(self.QUESTION), 'reason': 'Self-contained diary entry.',
                      'excludedSource': {'label': 'TEXT 3', 'title': 'KEEPING A DIARY', 'pages': [6, 7]}}

    def apply(self, entry, task=None):
        task = copy.deepcopy(task or self.task)
        with mock.patch.dict(full_cards.SOURCE_ATTACHMENTS, {task['id']: entry}):
            full_cards.apply_source_exclusion(task, self.record)
        return task

    def test_reviewed_exclusion_removes_only_the_named_default_reader(self):
        task = self.apply(self.entry)
        self.assertNotIn('sourceMaterial', task)
        self.assertFalse(any('source material' in r for r in task['taskRequirements']))
        # The scheme review binds the missing reader: restoring it makes that review stale.
        self.assertNotEqual(task_fingerprint(task), task_fingerprint(self.task))

    def test_stale_or_unexplained_exclusions_fail_closed(self):
        broken = {
            'does not match': {**self.entry, 'excludedSource': {**self.entry['excludedSource'], 'pages': [7]}},
            'stale': {**self.entry, 'paperSha256': 'changed paper'},
            'written reason': {**self.entry, 'reason': ' '},
            'only a written reason': {**self.entry, 'pages': [6, 7]},
        }
        for message, entry in broken.items():
            with self.subTest(message=message), self.assertRaisesRegex(ValueError, message):
                self.apply(entry)
        with self.assertRaisesRegex(ValueError, 'stale'):
            self.apply(self.entry, {**self.task, 'questionText': self.QUESTION + ' Changed.'})
        with self.assertRaisesRegex(ValueError, 'does not match'):
            self.apply(self.entry, {key: value for key, value in self.task.items() if key != 'sourceMaterial'})

    def test_recorded_2016_exclusions_are_bound_to_the_verified_defaults(self):
        attachments = json.loads((ROOT / 'scripts/markbank/authored/english-source-review.json').read_text())['attachments']
        exclusions = {key: value for key, value in attachments.items()
                      if value['kind'] == full_cards.SOURCE_NOT_REQUIRED and key.startswith('english-2016-')}
        self.assertEqual(exclusions.keys(), {'english-2016-ol-p1-t1-a-iii-b', 'english-2016-ol-p1-t3-a-iii-a'})
        record = next(r for r in inventory()['papers'] if r['id'] == 'english-2016-ol-p1')
        for entry in exclusions.values():
            self.assertEqual(entry['paperSha256'], record['questionPaper']['sha256'])
            self.assertIn('Self-contained', entry['reason'])
        self.assertEqual(exclusions['english-2016-ol-p1-t1-a-iii-b']['excludedSource'],
                         {'label': 'TEXT 1', 'title': 'A TRAVEL BLOG', 'pages': [2, 3]})


class English2026ReviewedPapersTest(unittest.TestCase):
    """Pin the independent 2026 reviews: tallies, routes, readers, tariffs and raw scan."""

    KEYS = ('english-2026-ol-p2', 'english-2026-hl-p1', 'english-2026-hl-p2', 'english-2026-ol-p1')

    @classmethod
    def setUpClass(cls):
        cls.records = {r['id']: r for r in inventory()['papers'] if r['id'] in cls.KEYS}
        cls.tasks = {key: extract_record(record)[1] for key, record in cls.records.items()}
        cls.by_id = {task['id']: task for tasks in cls.tasks.values() for task in tasks}
        authored = ROOT / 'scripts/markbank/authored'
        cls.decisions = json.loads((authored / 'english-selection-review.json').read_text())['decisions']
        cls.ledger = json.loads((authored / 'english-task-review.json').read_text())
        cls.raw = json.loads((authored / 'english-raw-selection-review.json').read_text())

    def routes(self, key):
        tasks = self.tasks[key]
        routes, pending = enumerate_choices(tasks, {t['id']: self.decisions[t['id']] for t in tasks})
        self.assertEqual(pending, [])
        return routes

    def test_2026_ordinary_paper_two_tally_routes_and_tariffs(self):
        key = 'english-2026-ol-p2'
        tasks, routes = self.tasks[key], self.routes(key)
        self.assertEqual((len(tasks), len(routes), len({r['id'] for r in routes})), (104, 105, 105))
        sections = {}
        for task in tasks:
            sections.setdefault(task['section'], []).append(task['totalMarks'])
        self.assertEqual({s: sorted(m) for s, m in sections.items()}, {
            'Single Text': [10] * 27 + [30] * 27, 'Comparative Study': [15] * 12 + [40] * 6,
            'Unseen Poetry': [10, 10], 'Prescribed Poetry': [15] * 12 + [20] * 18})
        # Only the unseen sad/hopeful choice is finite; each route keeps the 10-mark tariff and the poem.
        variants = [r for r in routes if 'choiceParentId' in r]
        self.assertEqual([r['id'] for r in variants], [key + '-unseen-q2-route-selection-1', key + '-unseen-q2-route-selection-2'])
        self.assertIn('Best description: Sad', variants[0]['questionText'])
        self.assertIn('Best description: Hopeful', variants[1]['questionText'])
        self.assertTrue(all(r['totalMarks'] == 10 and r['sourceMaterial']['pages'] == [14] for r in variants))
        # “Positive or negative or both” is an and/or judgement, kept whole like 2015 happy/sad/both.
        for letter in 'abcdef':
            decision = self.decisions[f'{key}-prescribed-{letter}-q1-b']
            self.assertEqual(decision['kind'], 'flexible')
            self.assertIn('2015 OL happy/sad/both', decision['reason'])
        subset = {'tasks': {t['id']: self.ledger['tasks'][t['id']] for t in tasks}}
        self.assertEqual(reconcile_schemes(tasks, inventory()['papers'], subset), [])
        for task in tasks:
            criteria = self.ledger['tasks'][task['id']]['criteria']
            marks = task['totalMarks']
            if marks in (30, 40):
                self.assertEqual(criteria['allocation'], {'P': marks * 3 // 10, 'C': marks * 3 // 10,
                                                          'L': marks * 3 // 10, 'M': marks // 10})
                self.assertIn('cannot exceed Purpose', criteria['notes'])
            else:
                self.assertEqual(criteria['allocation'], {'P+C': marks * 6 // 10, 'L+M': marks * 4 // 10})
        # Scheme PDF68 prints “ex 20” boxes under poem F Q1; the printed tariff (15) stands.
        for part in ('q1-a', 'q1-b'):
            entry = self.ledger['tasks'][f'{key}-prescribed-f-{part}']
            self.assertEqual((entry['totalMarks'], entry['criteria']['allocation']), (15, {'P+C': 9, 'L+M': 6}))
            self.assertIn('ex 20', entry['reason'])

    def test_2026_ordinary_paper_two_readers_and_shared_wording(self):
        key = 'english-2026-ol-p2'
        pages = dict(zip('abcdef', range(15, 21)))
        for task in self.tasks[key]:
            source = task.get('sourceMaterial')
            suffix = task['id'][len(key) + 1:]
            if suffix.startswith('prescribed-'):
                self.assertEqual(source['pages'], [pages[suffix.split('-')[1]]], suffix)
            elif suffix.startswith('unseen-'):
                self.assertEqual((source['title'], source['pages']), ('Long Distance', [14]))
                self.assertIn('Moya Roddy', source['attribution'])
            else:
                self.assertIsNone(source, suffix)
        self.assertEqual(self.by_id[key + '-prescribed-c-q1-b']['sourceMaterial']['title'], 'It’s Not')
        # Each mode prints identical Q1(b)/Q2(b) wording; both stay separate tasks with their own scheme pages.
        for mode, pages_b in (('a', ([51, 52], [52, 53])), ('b', ([53, 54], [54, 55])), ('c', ([55, 56], [56]))):
            q1, q2 = (self.by_id[f'{key}-comparative-{mode}-q{n}-b'] for n in (1, 2))
            self.assertEqual(q1['questionText'], q2['questionText'])
            self.assertEqual([self.ledger['tasks'][t['id']]['schemePages'] for t in (q1, q2)], list(pages_b))

    def test_2026_ordinary_paper_two_raw_scan_is_fully_classified(self):
        key = 'english-2026-ol-p2'
        record = self.records[key]
        from english_raw_selection import scan
        hits = scan([record])
        self.assertEqual(len(hits), 167)
        self.assertEqual(self.raw['sources'][key], record['questionPaper']['sha256'])
        kinds = {}
        for hit in hits:
            decision = self.raw['decisions'][hit['id']]
            self.assertEqual(decision['textSha256'], hit['textSha256'])
            kinds[decision['kind']] = kinds.get(decision['kind'], 0) + 1
            for task_id in decision.get('taskIds', []):
                self.assertEqual(len(decision['taskIds']), 1)
                self.assertIn(task_id, self.by_id)
        # Tasks: Single 9×6 + Comparative 26 + Unseen 2 + Prescribed 6×6 = 118. Rubric: cover 2, “any two”
        # 9, comparative 5, unseen 2, prescribed 1 + 6×3 = 37. Poem lines 7; final-page copyright notice 5.
        self.assertEqual(kinds, {'tasks': 118, 'exam-instruction': 37, 'source-prose': 7, 'non-selection': 5})

    def test_2026_higher_paper_one_routes_readers_and_criteria(self):
        key = 'english-2026-hl-p1'
        tasks, routes = self.tasks[key], self.routes(key)
        self.assertEqual((len(tasks), len(routes), len({r['id'] for r in routes})), (19, 20, 20))
        motion = [r for r in routes if 'choiceParentId' in r]
        self.assertEqual([r['id'] for r in motion], [key + '-composing-5-route-selection-1', key + '-composing-5-route-selection-2'])
        self.assertTrue(all(r['totalMarks'] == 100 for r in motion))
        self.assertIn('For the motion', motion[0]['questionText'])
        self.assertIn('Against the motion', motion[1]['questionText'])
        for suffix in ('t1-b', 't3-a-i', 't3-a-iii'):
            self.assertEqual(self.decisions[f'{key}-{suffix}']['kind'], 'flexible')
        titles = {1: ('An Influential Place - My Unquenchable City', [2, 3]), 2: ('Influential Life Moment', [4, 5]),
                  3: ('Influence of the Arts', [6, 7])}
        for task in tasks:
            suffix = task['id'][len(key) + 1:]
            source = task.get('sourceMaterial')
            if '-a-' in suffix:
                self.assertEqual((source['title'], source['pages']), titles[int(suffix[1])])
            elif suffix == 'composing-6':
                self.assertEqual((source['label'], source['title'], source['pages']), ('TEXT 2', 'Influential Life Moment', [4, 5]))
            else:
                self.assertIsNone(source, suffix)
            criteria = self.ledger['tasks'][task['id']]['criteria']
            if task['totalMarks'] in (15, 20):
                self.assertEqual(criteria['mode'], 'holistic')
                self.assertNotIn('allocation', criteria)
            else:
                marks = task['totalMarks']
                self.assertEqual(criteria['allocation'], {'P': marks * 3 // 10, 'C': marks * 3 // 10,
                                                          'L': marks * 3 // 10, 'M': marks // 10})
        # Printed wording is kept even where the question misspells the writer.
        self.assertIn('Enuma Okora asserts', self.by_id[key + '-t3-a-ii']['questionText'])
        subset = {'tasks': {t['id']: self.ledger['tasks'][t['id']] for t in tasks}}
        self.assertEqual(reconcile_schemes(tasks, inventory()['papers'], subset), [])
        from english_raw_selection import scan
        kinds = {}
        for hit in scan([self.records[key]]):
            kind = self.raw['decisions'][hit['id']]['kind']
            kinds[kind] = kinds.get(kind, 0) + 1
        self.assertEqual(kinds, {'tasks': 9, 'exam-instruction': 2, 'source-prose': 27, 'non-selection': 4})

    def test_2026_higher_paper_two_routes_headings_and_criteria(self):
        key = 'english-2026-hl-p2'
        tasks, routes = self.tasks[key], self.routes(key)
        self.assertEqual((len(tasks), len(routes), len({r['id'] for r in routes})), (27, 28, 28))
        # Only the single-text General Vision judgement requires a final side (scheme PDF37).
        variants = [r for r in routes if 'choiceParentId' in r]
        self.assertEqual([r['id'] for r in variants], [key + '-comparative-b-q1-a-route-selection-1',
                                                       key + '-comparative-b-q1-a-route-selection-2'])
        self.assertTrue(all(r['totalMarks'] == 30 for r in variants))
        self.assertIn('predominantly by my emotional response', variants[0]['questionText'])
        self.assertIn('predominantly by my rational response', variants[1]['questionText'])
        self.assertEqual(self.decisions[key + '-comparative-b-q1-b']['kind'], 'flexible')
        self.assertEqual(self.decisions[key + '-unseen-q2']['kind'], 'open')
        # Poet headings are stems, not prompt text.
        for number, poet in enumerate(('Elizabeth Bishop', 'Eiléan Ní Chuilleanáin', 'W.B. Yeats', 'Paula Meehan', 'John Donne'), 1):
            task = self.by_id[f'{key}-prescribed-{number}']
            self.assertTrue(task['questionText'].startswith('“'), task['questionText'][:40])
            self.assertEqual(task['stem'], poet)
            self.assertNotIn('sourceMaterial', task)
        for task in tasks:
            suffix = task['id'][len(key) + 1:]
            if suffix.startswith('unseen-'):
                self.assertEqual((task['sourceMaterial']['title'], task['sourceMaterial']['pages']), ('Library', [6]))
            else:
                self.assertNotIn('sourceMaterial', task)
            criteria = self.ledger['tasks'][task['id']]['criteria']
            marks = task['totalMarks']
            if marks in (10, 20, 30, 40):
                self.assertEqual(criteria['mode'], 'holistic')
            else:
                self.assertEqual(criteria['allocation'], {'P': marks * 3 // 10, 'C': marks * 3 // 10,
                                                          'L': marks * 3 // 10, 'M': marks // 10})
        subset = {'tasks': {t['id']: self.ledger['tasks'][t['id']] for t in tasks}}
        self.assertEqual(reconcile_schemes(tasks, inventory()['papers'], subset), [])
        from english_raw_selection import scan
        kinds = {}
        for hit in scan([self.records[key]]):
            kind = self.raw['decisions'][hit['id']]['kind']
            kinds[kind] = kinds.get(kind, 0) + 1
        self.assertEqual(kinds, {'tasks': 16, 'exam-instruction': 16, 'source-prose': 1, 'non-selection': 4})

    def test_2026_ordinary_paper_one_routes_readers_and_exclusions(self):
        key = 'english-2026-ol-p1'
        tasks, routes = self.tasks[key], self.routes(key)
        self.assertEqual((len(tasks), len(routes), len({r['id'] for r in routes})), (22, 390, 390))
        advice = [r for r in routes if r.get('choiceParentId') == key + '-t3-a-i']
        self.assertEqual(len(advice), 360)
        pairs = {(tuple(r['choiceRoute']['selections']['most']), r['choiceRoute']['selections']['least'][0]) for r in advice}
        self.assertEqual(pairs, {(pair, least) for pair in combinations([str(i) for i in range(1, 11)], 2)
                                 for least in map(str, range(1, 11)) if least not in pair})
        self.assertTrue(all(r['totalMarks'] == 15 and r['sourceMaterial']['pages'] == [6] for r in advice))
        self.assertIn('Most valuable: Spare the rod and spoil the child.; Children should be seen and not heard.',
                      advice[0]['questionText'])
        images = [r for r in routes if r.get('choiceParentId') == key + '-t3-a-ii']
        self.assertEqual({tuple(r['choiceRoute']['selections']['selection']) for r in images},
                         set(combinations('1234', 2)))
        self.assertTrue(all(r['sourceMaterial']['pages'] == [6, 7] for r in images))
        for number in (1, 2, 3):
            either = [r for r in routes if r.get('choiceParentId') == f'{key}-t{number}-a-iii-a']
            self.assertEqual((len(either), {r['totalMarks'] for r in either}), (2, {10}))
            self.assertTrue(all('sourceMaterial' not in r for r in either))
        self.assertEqual([r['totalMarks'] for r in routes if r.get('choiceParentId') == key + '-composing-3'], [100, 100])
        titles = {1: ('School Days', [2, 3]), 2: ('Play Centre', [4, 5]), 3: ('Advice and Images about Raising Children', [6, 7])}
        for task in tasks:
            suffix = task['id'][len(key) + 1:]
            source = task.get('sourceMaterial')
            if '-a-' in suffix and not suffix.endswith('iii-a'):
                title, pages = titles[int(suffix[1])]
                self.assertEqual((source['title'], source['pages']), (title, [6] if suffix == 't3-a-i' else pages))
            else:
                self.assertIsNone(source, suffix)
        subset = {'tasks': {t['id']: self.ledger['tasks'][t['id']] for t in tasks}}
        self.assertEqual(reconcile_schemes(tasks, inventory()['papers'], subset), [])


class EnglishPrintedChoiceCollapseTest(unittest.TestCase):
    """Coordinator rule 2026-10-12: a printed choice the scheme marks identically is ONE card."""

    @classmethod
    def setUpClass(cls):
        authored = ROOT / 'scripts/markbank/authored'
        cls.decisions = json.loads((authored / 'english-selection-review.json').read_text())['decisions']
        cls.visual = {e['paperId']: e for e in json.loads((authored / 'english-visual-review.json').read_text())['papers']}
        cls.records = {r['id']: r for r in inventory()['papers']}

    def test_no_finite_decision_remains(self):
        kinds = {decision['kind'] for decision in self.decisions.values()}
        self.assertNotIn('finite', kinds)
        printed = [d for d in self.decisions.values() if d['kind'] == 'printed-choice']
        self.assertEqual(len(printed), 221)
        self.assertTrue(all(d['printedChoices'] >= 2 and 'expectedRoutes' not in d for d in printed))
        self.assertTrue(all(d['reason'].startswith('One card (coordinator rule, 2026-10-12)') for d in printed))

    def test_advice_choice_is_one_card_with_the_printed_instruction(self):
        key = 'english-2026-ol-p1'
        tasks = extract_record(self.records[key])[1]
        cards, pending = review(tasks, {t['id']: self.decisions[t['id']] for t in tasks})
        self.assertEqual((len(tasks), len(cards), pending), (22, 22, []))
        self.assertFalse(any('-route-' in card['id'] for card in cards))
        advice = next(card for card in cards if card['id'] == key + '-t3-a-i')
        self.assertEqual(advice['printedChoice']['choices'], 360)
        self.assertEqual(advice['printedChoice']['requirement'],
                         'Make the choice the paper prints (Most valuable: 2 of 10; Least valuable: 1 of 10, '
                         'each a different one). Every choice is marked on the same grid.')
        enumerated, _ = enumerate_choices(tasks, {t['id']: self.decisions[t['id']] for t in tasks})
        self.assertEqual(len(enumerated), 390)

    def test_tallies_count_one_card_per_printed_choice(self):
        for key, entry in self.visual.items():
            tally = entry.get('independentPaperTally')
            if not tally or not entry['visualSweepComplete']:
                continue
            tasks = extract_record(self.records[key])[1]
            cards, pending = review(tasks, {t['id']: self.decisions[t['id']] for t in tasks if t['id'] in self.decisions})
            self.assertEqual((tally['baseTasks'], tally['finiteRoutes']), (len(tasks), len(cards)), key)
            self.assertEqual(len(tasks), len(cards), key)


class EnglishPrintedLabelsTest(unittest.TestCase):
    """Headings, titles and prompts carry the printed wording and case (2026-10-11)."""

    @classmethod
    def setUpClass(cls):
        keys = ('english-2026-hl-p2', 'english-2013-ol-p2', 'english-2026-ol-p2', 'english-2015-ol-p2',
                'english-2013-hl-p2', 'english-2018-hl-p2', 'english-2012-hl-p2')
        cls.by_id = {t['id']: t for r in inventory()['papers'] if r['id'] in keys for t in extract_record(r)[1]}
        cls.decisions = json.loads((ROOT / 'scripts/markbank/authored/english-selection-review.json').read_text())['decisions']

    def test_comparative_mode_headings_use_printed_case(self):
        self.assertEqual(self.by_id['english-2026-hl-p2-comparative-b-q1-a']['stem'],
                         'Comparative B · General Vision and Viewpoint · Q1')
        self.assertEqual(self.by_id['english-2012-hl-p2-comparative-a-q1']['stem'],
                         'Comparative A · The General Vision and Viewpoint · Q1')
        self.assertEqual(self.by_id['english-2013-ol-p2-comparative-b-q1-a']['stem'],
                         'Comparative B · Aspects of Story: Tension or Climax or Resolution')
        with self.assertRaisesRegex(ValueError, 'no printed-case label'):
            full_cards.printed_mode_label('Theme And Something', 'THEME AND SOMETHING')

    def test_poem_titles_are_pinned_to_the_page(self):
        self.assertEqual(self.by_id['english-2026-ol-p2-prescribed-b-q1-a']['sourceMaterial']['title'],
                         'Driving to the Hospital')
        self.assertEqual(self.by_id['english-2026-ol-p2-prescribed-d-q1-a']['sourceMaterial']['title'],
                         'This Is Just To Say')
        self.assertEqual(self.by_id['english-2015-ol-p2-prescribed-d-q1-a']['sourceMaterial']['title'],
                         'The Bend in the Road')
        self.assertEqual(self.by_id['english-2015-ol-p2-prescribed-d-q1-a']['stem'],
                         'The Bend in the Road — Eiléan Ní Chuilleanáin')

    def test_hl_poet_headings_are_stems_not_prompt_text(self):
        for key in ('english-2013-hl-p2', 'english-2018-hl-p2'):
            for number in range(1, 5):
                task = self.by_id[f'{key}-prescribed-{number}']
                # The heading line is gone; 2018 Q4's own sentence then opens “Philip Larkin wanted …”.
                self.assertFalse(task['questionText'].startswith(task['stem'] + ' ' + task['stem']), task['id'])
                self.assertFalse(task['rawQuestionText'].splitlines()[0].strip() == task['stem'], task['id'])
        self.assertTrue(self.by_id['english-2018-hl-p2-prescribed-1']['questionText'].startswith(
            'From your study of the poetry of Robert Frost'))

    def test_2024_combined_tone_is_one_open_response(self):
        for letter in 'abcdef':
            decision = self.decisions[f'english-2024-ol-p2-prescribed-{letter}-q1-a']
            self.assertEqual(decision['kind'], 'flexible')
            self.assertIn('or a combination of both', decision['reason'])

    def test_repaired_ordinary_paper_two_scheme_crops(self):
        def scheme(year, n):
            sidecar = json.loads((ROOT / f'scripts/paper-trail/answers/{year}/LC002GLP200EV.pdf.json').read_text())
            question = next(q for q in sidecar['q'] if q['n'] == n)
            return (question.get('schemeRegion') or question['region'])[0]
        self.assertEqual(scheme(2018, '11'), {'p': 40, 'r': [0.0, 0.4038, 1.0, 1.0]})
        self.assertEqual(scheme(2014, '4'), {'p': 18, 'r': [0.0, 0.086, 1.0, 1.0]})
        self.assertEqual(scheme(2014, '10'), {'p': 30, 'r': [0.0, 0.7079, 1.0, 1.0]})
        self.assertEqual(scheme(2013, '11'), {'p': 33, 'r': [0.0, 0.5867, 1.0, 1.0]})
        self.assertEqual(scheme(2012, '10'), {'p': 30, 'r': [0.0, 0.5922, 1.0, 1.0]})
        self.assertEqual(scheme(2012, '11'), {'p': 32, 'r': [0.0, 0.418, 1.0, 1.0]})
        self.assertEqual(scheme(2016, '10'), {'p': 37, 'r': [0.0, 0.332, 1.0, 1.0]})


if __name__ == '__main__':
    unittest.main()
