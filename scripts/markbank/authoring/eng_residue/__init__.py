"""The Engineering parts the automatic author refuses, authored from the page.

eng_all.py cards a part when its readers can: the paper reader finds the ask,
eng_scheme finds its marking points and tariff, and the gates pass. Where they
cannot -- a reader fault on one page, an answer the scheme gives as a drawing,
a figure no crop was cut for -- the part used to stay open. Each sitting's
module here (y2021_hl.py, ...) says, part by part, what the page shows and how
the card is made, and every card is still built by lib.Author.card, so the
same refusals apply: question text from the paper reader, every marking point
either one the scheme reader returns (`use=`) or a rectangle lifted off the
scheme page (eng_lift.lift, `lifted=`), every row traced by the build's own
provenance gate, every tariff the one the scheme or paper prints.

A module holds:

  CROPS  {figure name: dict(doc, page, rect, ref, solution=False, letters=())}
         -- what eng_crops.py renders and publishes. Paper crops are named
         -paper-q<part>-art, the name eng_all reads for a part's own picture;
         scheme crops that ARE the answer are -scheme-q<part>-sol and solution.
  CARDS  [dict(key=(q, letter, roman), why=..., ...lib.card arguments...)]

A residue card the automatic author already builds is an error, not a merge:
the entry is stale and must go, or the two would disagree about one id --
unless the entry says `replaces=`: the automatic card was opened and is
wrong, and the reviewed card takes its place under the same id.
"""
import importlib
import os
import sys

DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(DIR))

from lib import Refused                                    # noqa: E402

# Arguments a CARDS entry may hand to lib.card, besides those built here.
PASS = ('use', 'marks', 'tariff', 'total', 'row_kind', 'notation', 'ladder',
        'lifted', 'special', 'figure', 'question_figure', 'labels', 'notes',
        'checked', 'context', 'omit', 'spread', 'suffix', 'from_run',
        'from_runs', 'question_lift', 'group', 'routes')


def module(year, level):
    name = f'eng_residue.y{year}_{level}'
    try:
        return importlib.import_module(name)
    except ModuleNotFoundError as exc:
        if exc.name == name:
            return None
        raise


def part_id(year, level, q, letter, roman):
    return (f'eng-{year}-{level}-q{q}' + (f'-{letter}' if letter else '')
            + (f'-{roman}' if roman else ''))


def build(A, year, level, built, figure_keys, topic_for_part, keeps_stem,
          concept_for, checked=lambda key: None, withdrawn=()):
    """Add this sitting's residue cards to A.cards. -> [card ids]"""
    mod = module(year, level)
    if mod is None:
        return []
    made = []
    # A card the automatic author files under the wrong syllabus heading: a
    # keyword outvoted the content ("a non-destructive test ... in a welded
    # joint" under Joining). Only the topic moves; the id, text and rows stay.
    for cid, (topic, why) in getattr(mod, 'TOPICS', {}).items():
        hit = [c for c in A.cards if c['id'] == cid]
        if not hit or not why:
            raise SystemExit(f'eng_residue {year} {level} {cid}: TOPICS entry for a '
                             f'card the author does not build, or with no reason')
        if hit[0]['topicId'] == topic:
            raise SystemExit(f'eng_residue {year} {level} {cid}: already {topic}; '
                             f'the TOPICS entry is stale')
        hit[0]['topicId'] = topic
    for entry in getattr(mod, 'CARDS', []):
        q, letter, roman = entry['key']
        cid = entry.get('id') or part_id(year, level, q, letter, roman)
        where = f'eng_residue {year} {level} {cid}'
        if not entry.get('why'):
            raise SystemExit(f'{where}: say what the page shows (why=)')
        if cid in withdrawn:
            raise SystemExit(f'{where}: a withdrawn id is never re-emitted; give the '
                             f'card an id of its own (id=)')
        if entry.get('replaces'):
            # A card the automatic author builds and a person has opened and
            # found WRONG -- a tariff for an answer, half a sentence, an axis
            # read as prose. Rebuilt under the SAME id from the page, so a
            # student's history stays with it; `replaces` says what was wrong.
            if cid not in built:
                raise SystemExit(f'{where}: replaces a card the automatic author '
                                 f'no longer builds -- the entry is stale')
            A.cards[:] = [c for c in A.cards if c['id'] != cid]
        elif cid in built:
            raise SystemExit(f'{where}: the automatic author already builds this '
                             f'card -- the entry is stale; remove it')
        for fk in (entry.get('figure'), entry.get('question_figure')):
            if fk and fk not in figure_keys:
                raise SystemExit(f'{where}: figure {fk} is not published -- run '
                                 f'eng_crops.py {year} {level} --publish')
        labels = entry.get('labels')
        if isinstance(labels, dict):
            for letter_, meaning in labels.items():
                if not hasattr(meaning, 'source'):
                    raise SystemExit(f'{where}: label {letter_} must be lifted from '
                                     f'the scheme, not typed')
            labels = {k: str(v) for k, v in labels.items()}
        try:
            ask = A.paper.text(q, letter, roman) or ''
        except Exception:                                    # noqa: BLE001
            ask = ''
        topic = entry.get('topic') or topic_for_part(A, q, letter, roman, ask)
        if not topic:
            raise SystemExit(f'{where}: files under no topic; give topic=')
        figure = entry.get('figure') or entry.get('question_figure')
        stem = entry.get('stem')
        if stem is None:
            try:
                text = A.paper.stem(q, letter) or A.paper.stem(q) or ''
            except Exception:                                # noqa: BLE001
                text = ''
            stem = keeps_stem(text, figure)
        kwargs = {k: entry[k] for k in PASS if k in entry}
        if 'labels' in kwargs:
            kwargs['labels'] = labels
        kwargs.setdefault('source', 'table')
        # The automatic author's reviewed observation about this page, where
        # it has one (eng_all.CHECKED), unless the entry gives its own.
        if 'checked' not in kwargs and checked((q, letter, roman)):
            kwargs['checked'] = checked((q, letter, roman))
        try:
            A.card(q, letter, roman, topic=topic,
                   concept=entry.get('concept') or concept_for(ask),
                   card_id=cid, stem=stem, **kwargs)
        except Refused as exc:
            raise SystemExit(f'{where}: {exc}')
        made.append(cid)
    return made
