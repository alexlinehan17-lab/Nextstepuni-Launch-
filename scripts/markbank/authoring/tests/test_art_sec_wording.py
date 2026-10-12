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
        self.assertEqual(sorted(AUTHORED['descriptors']),
                         sorted(f'{year}-{level}' for year in AUDITED for level in ('higher', 'ordinary')))

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
            if not page_has(paper, card['paperPage'], lines[0]):
                failures.append((card['id'], 'paperPage', card['paperPage']))
            for criterion in card.get('criteria', []):
                for text in criterion['guidance']:
                    if not on_cited_page(scheme, card['schemePage'], text):
                        failures.append((card['id'], 'scheme row', text))
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
