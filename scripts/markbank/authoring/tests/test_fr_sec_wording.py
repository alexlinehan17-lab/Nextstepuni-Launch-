"""Every SEC-attributed string on a French reading or listening card is printed.

Re-lifting each string from its own document must give back exactly that
string: the question, context and options from the paper; the answer lines
from the cited scheme pages; the rules from the paper or the scheme; the notes
from the scheme. NextStepUni's guidance may only appear in practiceNotes, and
the criterion guidance (shown under the SEC heading) is empty.
"""
from pathlib import Path
import json
import re
import sys
import unittest

AUTH = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(AUTH))
from fr_printed import lift, doc_texts, _doc, MARKER  # noqa: E402

ROOT = AUTH.parents[2]
DATA = ROOT / 'examiner-reports/french'
DECKS = ROOT / 'components/MarkBank/cards/french'


def whole(path, aliases=()):
    return doc_texts(path, list(range(1, len(_doc(str(path))) + 1)), aliases)


def lifts(groups, line, marks=''):
    """The line is the page's own text; a printed list bullet may precede it."""
    try:
        got = lift(groups, line, marks=marks)
    except AssertionError:
        return False
    return got == line or re.sub(rf'^{MARKER}\s*', '', got) == line


class FrenchSecWordingTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        review = json.loads((AUTH / 'french-reading-review.json').read_text())
        cls.aliases = {(r['year'], r['level']): tuple(a['glyph'] for a in r.get('schemeBulletAliases', []))
                       for r in review['papers']}

    def check(self, deck):
        failures = []
        seen = {}
        for card in json.loads((DECKS / f'{deck}.json').read_text()):
            year, level = card['year'], {'higher': 'hl', 'ordinary': 'ol'}[card['level']]
            paper = DATA / f'papers/{year}-{level}-{"A00" if deck == "listening" else "000"}-paper.pdf'
            scheme = DATA / f'schemes/{year}-{level}.pdf'
            aliases = self.aliases.get((year, level), ()) if deck == 'reading' else ()
            rubric = card['rubric']
            if deck == 'reading':
                cited = [int(p) for p in re.search(r'pp\.([\d, ]+);', card['schemeCitation'])[1].split(',')]
            else:
                first = card['schemeRegion']['p']
                cited = [p for p in (first, first + 1) if p <= len(_doc(str(scheme)))]
            question_pages = card['sourceMaterial']['pages']
            checks = [('question', l, paper, tuple(question_pages), '') for l in card['questionText'].split('\n') if l.strip()]
            checks += [('choice', c, paper, tuple(question_pages), '') for c in card.get('questionChoices', [])]
            if card.get('stem'):
                checks.append(('stem', card['stem'], paper, tuple(question_pages), ''))
            checks += [('guide', l, scheme, tuple(cited), None) for l in rubric['answerGuide']]
            checks += [('note', l, scheme, None, '') for l in rubric['markingGuideNote'].split('\n') if l]
            for kind, line, path, pages, marks in checks:
                key = (kind, line, str(path), pages)
                if key not in seen:
                    groups = whole(path, aliases) if pages is None else doc_texts(path, list(pages), aliases)
                    seen[key] = lifts(groups, line, marks)
                if not seen[key]:
                    failures.append((card['id'], kind, line))
            for line in rubric['taskRequirements']:
                key = ('rule', line, str(paper), str(scheme))
                if key not in seen:
                    seen[key] = lifts(whole(paper), line) or lifts(whole(scheme, aliases), line)
                if not seen[key]:
                    failures.append((card['id'], 'rule', line))
            for criterion in rubric['criteria']:
                if criterion['guidance']:
                    failures.append((card['id'], 'guidance', criterion['guidance']))
            if not rubric.get('practiceNotes'):
                failures.append((card['id'], 'practiceNotes', 'missing'))
        if failures:
            kinds = {}
            for _cid, kind, _line in failures:
                kinds[kind] = kinds.get(kind, 0) + 1
            self.fail(f'{len(failures)} unprinted strings {kinds}:\n' + '\n'.join(map(repr, failures[:40])))

    def test_refuses_the_generator_wording_it_replaced(self):
        aural = whole(DATA / 'papers/2026-hl-A00-paper.pdf')
        scheme = doc_texts(DATA / 'schemes/2026-hl.pdf', [20])
        paper = whole(DATA / 'papers/2026-ol-000-paper.pdf')
        self.assertFalse(lifts(aural, 'Answer in English or Irish; complete sentences are not required.'))
        self.assertFalse(lifts(scheme, 'Nature — 1 Marks', None))        # printed "1 Mark"
        self.assertTrue(lifts(scheme, '- Nature — 1 Mark', None))
        self.assertFalse(lifts(paper, 'Write the name of the person who talks about:'))   # no printed colon
        self.assertTrue(lifts(paper, 'Write the name of the person who talks about'))

    def test_reading_shows_only_printed_wording(self):
        self.check('reading')

    def test_listening_shows_only_printed_wording(self):
        self.check('listening')


if __name__ == '__main__':
    unittest.main()
