"""Every SEC-attributed string on an audited Art card is printed.

For each audited year, the question, stem and task-check lines must occur in
that year's paper, and every scheme string (the question's own scheme row,
each descriptor bullet and lead-in, each Section B/C criterion label, each
marking note) must occur on the scheme page the card cites. NextStepUni's
guidance appears only in practiceNotes, which the scheme must NOT print.
An independent census read from the paper (art_paper_census.py, sharing no
code with art_cards.py) must find exactly the deck's printed tasks.

    python3 -m unittest discover -s scripts/markbank/authoring/tests -p 'test_art_*.py'
"""
from pathlib import Path
import json
import re
import sys
import unittest

AUTH = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(AUTH))
import art_printed as P  # noqa: E402
import art_paper_census  # noqa: E402
import art_cards  # noqa: E402

ROOT = AUTH.parents[2]
AUTHORED = json.loads((ROOT / 'components/MarkBank/cards/art/authored.json').read_text())
AUDITED = tuple(AUTHORED['auditedYears'])
REF_LEVEL = {'higher': 'HL', 'ordinary': 'OL'}


def page_has(path: str, page: int, text: str) -> bool:
    return P.normal(text) in P.normal(P.visible_lines(P._open(path)[page - 1]))


def on_cited_page(path: str, pages, text: str) -> bool:
    pages = pages if isinstance(pages, list) else [pages]
    return any(page_has(path, page, text) for page in pages)


class ArtSecWordingTest(unittest.TestCase):
    def test_audits_at_least_one_year(self):
        self.assertTrue(AUDITED)
        # Descriptors exist from 2023; the 2021-2022 schemes allocate marks
        # to components without descriptor bands.
        self.assertEqual(sorted(AUTHORED['descriptors']),
                         sorted(f'{year}-{level}' for year in AUDITED if year >= 2023
                                for level in ('higher', 'ordinary')))

    def test_every_card_string_is_printed(self):
        failures = []
        for card in AUTHORED['cards']:
            if card['year'] not in AUDITED:
                continue
            year, level = card['year'], card['level']
            paper, scheme = P.paper_path(year, level), P.scheme_path(year, level)
            lines = [re.sub(r'^•\s*', '', line) for line in card['questionText'].split('\n') if line.strip()]
            checks = [('question', line) for line in lines]
            checks += [('requirement', line) for line in card['taskRequirements']]
            if card.get('stem'):
                checks.append(('stem', card['stem']))
            for kind, text in checks:
                if not P.printed(paper, text):
                    failures.append((card['id'], kind, text))
            if re.search('[\ue000-\uf8ff]', json.dumps(card, ensure_ascii=False)):
                failures.append((card['id'], 'private-use glyph', ''))
            if not page_has(paper, card['paperPage'], lines[0]):
                failures.append((card['id'], 'paperPage', card['paperPage']))
            for criterion in card.get('criteria', []):
                for text in criterion['guidance'] + [n for n in criterion.get('rowNotes', []) if n]:
                    if not on_cited_page(scheme, card['schemePage'], text):
                        failures.append((card['id'], 'scheme row', text))
                if 'rowMarks' in criterion and sum(criterion['rowMarks']) != criterion['maxMarks']:
                    failures.append((card['id'], 'row marks', criterion['rowMarks']))
                if any(text.startswith('SEC note') for text in criterion['guidance']):
                    failures.append((card['id'], 'written prefix', criterion['guidance']))
        self.assertEqual(failures, [])

    def test_every_descriptor_and_note_is_printed_on_its_page(self):
        failures = []
        for key, lifted in AUTHORED['descriptors'].items():
            year, level = key.split('-')
            scheme = P.scheme_path(int(year), level)
            short = lifted['short']
            for text in [short['lead'], *(b for band in short['bands'].values() for b in band)]:
                if not page_has(scheme, short['page'], text):
                    failures.append((key, 'short', text))
            for criterion in lifted['long']:
                texts = [criterion['label'], criterion['lead']]
                texts += [g for band in criterion['bands'].values() for g in band['guidance']]
                for text in texts:
                    if not page_has(scheme, criterion['page'], text):
                        failures.append((key, criterion['id'], text))
            for kind, note in lifted['notes'].items():
                for text in note['text']:
                    if not page_has(scheme, note['page'], text):
                        failures.append((key, kind, text))
        self.assertEqual(failures, [])

    def test_cards_cite_the_pages_they_quote(self):
        for card in AUTHORED['cards']:
            if card['year'] not in AUDITED:
                continue
            if card['assessment'] == 'legacy-components':
                # One scheme table per question, on its one page.
                self.assertIsInstance(card['schemePage'], int, card['id'])
                continue
            lifted = AUTHORED['descriptors'][f"{card['year']}-{card['level']}"]
            if card['assessment'] == 'current-long-descriptors':
                expected = [lifted['notes']['current-long-descriptors']['page'],
                            *(criterion['page'] for criterion in lifted['long'])]
                self.assertEqual(card['schemePage'], expected, card['id'])
            else:
                self.assertEqual(card['schemePage'][:2], [
                    lifted['notes']['current-short-descriptors']['page'], lifted['short']['page']], card['id'])

    def test_refuses_wording_the_scheme_does_not_print(self):
        for year in AUDITED:
            for level in ('higher', 'ordinary'):
                scheme = P.scheme_path(year, level)
                # The condensed descriptors the cards showed before the audit,
                # and NextStepUni's practice notes, are not the SEC's.
                for text in (
                    'Limited coherence, focus, visual-art terminology and/or relevant sketches.',
                    'Understand the demands of the chosen question and build the response around it.',
                    'Judge the complete response once against each of the four published descriptors.',
                    'Score each independently awarded component once.',
                ):
                    self.assertFalse(P.printed(scheme, text), (year, level, text))

    # Every answer-box label the generator drops, pinned here as well as in
    # art_cards.ANSWER_BOX_LABELS, so no question wording can be dropped by
    # the same rule without this list changing.
    PINNED_LABELS = {
        (2023, 'higher', 2): ('Imagery:', 'Mood:'),
        (2023, 'higher', 3): ('Artwork:', 'Artist:'),
        (2023, 'higher', 6): ('Style:', 'Composition and use of surface:'),
        (2023, 'ordinary', 1): ('Colour, composition:',),
        (2023, 'ordinary', 3): ('Imagery:', 'Composition:', 'Colour:'),
        (2023, 'ordinary', 5): ('Lettering:', 'Imagery:', 'Colour:'),
        (2023, 'ordinary', 6): ('Hat A – form, materials:', 'Hat B – form, materials:', 'Hat A – function:', 'Hat B – function:'),
        (2023, 'ordinary', 7): ('Scale:', 'Treatment of the human figure:', 'Use of materials:'),
        (2024, 'higher', 3): ('Name of sculptor:',),
        (2024, 'ordinary', 2): ('Name of organisation:', 'Explain:'),
        (2024, 'ordinary', 6): ('Name of film, TV show or theatrical performance:', 'Name of character:',
                                'Description of costume:'),
        (2025, 'ordinary', 3): ('Name of gallery, arts centre or museum:', 'Name of artwork:'),
        (2025, 'ordinary', 4): ('Heading 1:', 'Heading 2:'),
    }

    def test_only_pinned_answer_box_labels_are_dropped(self):
        self.assertEqual(art_cards.ANSWER_BOX_LABELS, self.PINNED_LABELS)
        for (year, level, number), labels in self.PINNED_LABELS.items():
            paper = P.paper_path(year, level)
            cards = [c for c in AUTHORED['cards'] if c['year'] == year and c['level'] == level
                     and re.match(rf"{year} {REF_LEVEL[level]} Q{number}\b(?!\d)", c['questionRef'])]
            self.assertTrue(cards, (year, level, number))
            pages = sorted({c['paperPage'] for c in cards} | {c['paperPage'] + 1 for c in cards})
            for label in labels:
                # A label: one short phrase ending in a colon, no sentence.
                self.assertRegex(label, r'^[^.?!]{1,60}:$')
                self.assertTrue(any(P.in_answer_box(paper, page, label) for page in pages
                                    if page <= len(P._open(paper))), (year, level, number, label))
                for card in cards:
                    text = ' '.join([card.get('stem') or '', card['questionText'], *card['taskRequirements']])
                    self.assertNotIn(label, text, card['id'])

    def test_audited_topics_are_ones_the_atlas_gives_the_question(self):
        runtime = json.loads((ROOT / 'data/examTopics/art-runtime.json').read_text())
        topics = runtime['topics']
        atlas = {}
        for level, lang, year, component, number, topic_indexes in runtime['questionMappings']:
            if lang == 'e' and str(number).isdigit():
                atlas[(2000 + year, level, component, int(number))] = {
                    t for index in topic_indexes for t in topics[index][5]}
        failures = []
        for card in AUTHORED['cards']:
            if card['year'] not in AUDITED:
                continue
            number = int(re.search(r'Q(\d+)', card['questionRef']).group(1))
            # No exceptions: reviewed anomalies, per-option headings and the
            # specific headings of generic-only questions are in the Atlas.
            component = re.search(r'LP(\w{3})', card['paperFileid']).group(1)
            allowed = set(atlas.get((card['year'], card['level'][0], component, number)) or ())
            if not allowed or card['topicId'] not in allowed:
                failures.append((card['id'], card['topicId'], sorted(allowed or [])))
        self.assertEqual(failures, [])

    def test_independent_paper_census_matches_the_deck(self):
        for year in AUDITED:
            for level in ('higher', 'ordinary'):
                census = art_paper_census.census(year, level)
                printed_refs = set()
                directive_questions = set()
                for number, question in census['questions'].items():
                    for task in question['tasks']:
                        suffix = '' if task == 'response' else task.replace('task ', ' · task ')
                        printed_refs.add(f'{year} {REF_LEVEL[level]} Q{number}{suffix}')
                    if question['directives']:
                        directive_questions.add(int(number))
                deck_refs = {card['questionRef'].split(' · ')[0] if ' · task' not in card['questionRef']
                             else card['questionRef']
                             for card in AUTHORED['cards'] if card['year'] == year and card['level'] == level}
                self.assertEqual(deck_refs, printed_refs, (year, level))
                reviewed = {key[2] for key in (*art_cards.PRINTED_CHOICES, *art_cards.REVIEWED_OPEN_SELECTIONS,
                                               *art_cards.REVIEWED_NON_ENUMERABLE_POOLS,
                                               *art_cards.TASK_COMBINATION_CHOICES)
                            if key[:2] == (year, level)}
                self.assertEqual(directive_questions, reviewed, (year, level))


if __name__ == '__main__':
    unittest.main()
