"""Pin independent visual tallies; these tests do not replace scheme review."""
import copy
import json
import unittest
from itertools import combinations, permutations
from unittest import mock

import english_full_cards as full_cards
from english_choices import fingerprint, review
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
        routes, missing = review(tasks, decisions)
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
            resolved, pending = review(tasks, {t['id']: decisions[t['id']] for t in tasks})
            self.assertEqual((len(tasks), len(resolved), pending), (base, routes, []))

    def test_2014_comprehension_routes_and_shared_visual_context(self):
        decisions = json.loads((ROOT / 'scripts/markbank/authored/english-selection-review.json').read_text())['decisions']
        for level, base, count in [('hl', 19, 20), ('ol', 22, 26)]:
            key = f'english-2014-{level}-p1'
            tasks = self.tasks[key]
            routes, pending = review(tasks, {t['id']: decisions[t['id']] for t in tasks})
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
            routes, pending = review(tasks, {t['id']: decisions[t['id']] for t in tasks})
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
            routes, pending = review(tasks, {t['id']: decisions[t['id']] for t in tasks})
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
        posters = review([self.by_id[hl + 't1-b']], {hl + 't1-b': decisions[hl + 't1-b']})[0]
        self.assertEqual({(r['choiceRoute']['selections']['first'][0], r['choiceRoute']['selections']['second'][0])
                          for r in posters}, set(permutations('1234', 2)))
        self.assertTrue(all(r['sourceMaterial']['pages'] == [2] for r in posters))
        virtues = review([self.by_id[ol + 'composing-4']], {ol + 'composing-4': decisions[ol + 'composing-4']})[0]
        self.assertEqual({tuple(r['choiceRoute']['selections']['virtues']) for r in virtues},
                         set(combinations('12345', 2)))
        self.assertEqual([o['text'] for o in decisions[ol + 'composing-4']['pools'][0]['options']],
                         ['Kindness', 'Patience', 'Generosity', 'Tolerance', 'Forgiveness'])
        china = review([self.by_id[ol + 't1-a-ii']], {ol + 't1-a-ii': decisions[ol + 't1-a-ii']})[0]
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
        routes, pending = review(tasks, {t['id']: decisions[t['id']] for t in tasks})
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
            resolved, pending = review(tasks, {t['id']: decisions[t['id']] for t in tasks})
            self.assertEqual((len(tasks), len(resolved), pending), (base, routes, []))
        self.assertEqual(decisions['english-2018-hl-p1-composing-7']['kind'], 'open')
        source = self.by_id['english-2018-hl-p1-t3-a-i']['sourceMaterial']
        self.assertEqual(source['pages'], [6])
        self.assertIn('Dead Man’s Dump', source['title'])

    def test_2014_higher_poem_reader_and_flexible_character_minimum(self):
        key = 'english-2014-hl-p2'
        decisions = json.loads((ROOT / 'scripts/markbank/authored/english-selection-review.json').read_text())['decisions']
        tasks = self.tasks[key]
        routes, pending = review(tasks, {t['id']: decisions[t['id']] for t in tasks})
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
            resolved, pending = review(tasks, {t['id']: decisions[t['id']] for t in tasks})
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
            resolved, pending = review(tasks, {t['id']: decisions[t['id']] for t in tasks})
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
            resolved, pending = review(tasks, {t['id']: decisions[t['id']] for t in tasks})
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
        exclusions = {key: value for key, value in attachments.items() if value['kind'] == full_cards.SOURCE_NOT_REQUIRED}
        self.assertEqual(exclusions.keys(), {'english-2016-ol-p1-t1-a-iii-b', 'english-2016-ol-p1-t3-a-iii-a'})
        record = next(r for r in inventory()['papers'] if r['id'] == 'english-2016-ol-p1')
        for entry in exclusions.values():
            self.assertEqual(entry['paperSha256'], record['questionPaper']['sha256'])
            self.assertIn('Self-contained', entry['reason'])
        self.assertEqual(exclusions['english-2016-ol-p1-t1-a-iii-b']['excludedSource'],
                         {'label': 'TEXT 1', 'title': 'A TRAVEL BLOG', 'pages': [2, 3]})


if __name__ == '__main__':
    unittest.main()
