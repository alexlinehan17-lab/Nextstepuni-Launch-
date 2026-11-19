#!/usr/bin/env python3
"""Card one Polish sitting into scripts/markbank/authored/polish.json.

    python3 scripts/markbank/authoring/pl_q3_batch.py review 2026 hl   # print what would be added
    python3 scripts/markbank/authoring/pl_q3_batch.py write 2026 hl    # add it

The languages-q3 lane's merge step (treatment D, 19 Nov 2026). A sitting's cards
come from four places, each lifted from the paper and the scheme:

  * pl_all.build()        the reading asks the existing reader pairs on their address;
  * pl_reading_specs      the reading asks it refuses, read on the rendered page;
  * pl_listen_specs       the listening asks, one card each, with the SEC recording;
  * pl_writing            the written tasks, one marking-grid card each.

Every card already in the authored file is kept BYTE FOR BYTE: the generator no
longer reproduces three live 2024/2025 Ordinary cards exactly, so regenerating
the file would change cards students have. New cards are added beside their
own sitting's. The only edits to live cards are CORRECTIONS below, each with its
evidence.
"""
import collections
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
sys.path.insert(0, HERE)

AUTHORED = os.path.join(ROOT, 'scripts', 'markbank', 'authored', 'polish.json')
LEVEL_WORD = {'hl': 'higher', 'ol': 'ordinary'}

# Live answers the scheme contradicts, found by rendering every Polish
# true/false table on its scheme page (19 Nov 2026): the reader paired each of
# these rows with the tick of the row BELOW it, which the SEC sets about six
# points higher than its own row's text. The verdict word is the table's own
# column heading ("Prawda Fałsz Marks", 2025 Ordinary scheme p6).
CORRECTIONS = {
    'pl-2025-ol-a-2-c-ii': ('Prawda', 'Fałsz',
                            'scheme p6: the tick for (ii) "Zbiórki harcerskie odbywają się raz w roku." '
                            'stands in the Fałsz column'),
    'pl-2025-ol-a-2-c-iv': ('Fałsz', 'Prawda',
                            'scheme p6: the tick for (iv) "Harcerze sami budują obóz." stands in the '
                            'Prawda column'),
    'pl-2025-ol-a-2-c-v': ('Prawda', 'Fałsz',
                           'scheme p6: the tick for (v) "Na obozie harcerze wywieszają polską flagę '
                           'każdego wieczoru." stands in the Fałsz column'),
}


def _correct(card):
    fix = CORRECTIONS.get(card['id'])
    if not fix:
        return card
    old, new, evidence = fix
    row = card['rows'][0]
    assert row['verbatim'] == old, (card['id'], row['verbatim'])
    row['verbatim'] = new
    for field in ('contextNote',):
        if row.get(field):
            row[field] = row[field].replace(f'in the {old} column', f'in the {new} column')
    if card.get('notes'):
        card['notes'] = card['notes'].replace(f'in the {old} column', f'in the {new} column')
        card['notes'] += f' Corrected 19 Nov 2026 from "{old}": {evidence}.'
    return card


def sitting_cards(year, level, generated=None):
    import pl_all
    import pl_reading_specs
    import pl_listen_specs
    import pl_writing
    with open(AUTHORED, encoding='utf-8') as fh:
        authored = json.load(fh)
    have = {c['id'] for c in authored}
    lv = LEVEL_WORD[level]
    if generated is None:
        generated = pl_all.build()[0]
    specs = pl_reading_specs.cards(year, level)
    spec_ids = {c['id'] for c in specs}
    import pl_paper
    from paper_census import key_label, PRINTED_EXAMPLES
    P = pl_paper.PlPaper(year, level)
    by_label = {key_label(a.key, 'polish'): a for a in P.all_asks()}
    worked = {k[3] for k in PRINTED_EXAMPLES if k[:3] == ('polish', year, level)}
    label = lambda c: c['questionRef'].split(' ', 2)[2]                    # noqa: E731
    # A worked example is not an ask (CARD-STANDARD 10d): pl_all still reads
    # its row, priced at 0 or a dash, and it is left out here.
    reading = [pl_reading_specs.fix_question(json.loads(json.dumps(c)), year, level,
                                             ask=by_label.get(label(c)))
               for c in generated if c['year'] == year and c['level'] == lv
               and c['id'] not in have and c['id'] not in spec_ids
               and label(c) not in worked]
    # The old examination (2021 and earlier) has no listening test and no
    # Section B grid: its essays are cards in pl_reading_specs.
    old_exam = year <= 2021
    new = (reading + specs
           + ([] if old_exam else pl_listen_specs.cards(year, level) + pl_writing.cards(year, level)))
    ids = [c['id'] for c in new]
    dup = [i for i, n in collections.Counter(ids).items() if n > 1]
    if dup:
        raise ValueError(f'{year} {level}: duplicate new ids {dup}')
    clash = [i for i in ids if i in have]
    if clash:
        raise ValueError(f'{year} {level}: new ids already live {clash}')
    return authored, new


# Sittings with no live card before this lane: every card in them is the
# lane's own, so a rewrite replaces them whole.
ALL_NEW = {2026}


def write(year, level, generated=None):
    if year in ALL_NEW:
        with open(AUTHORED, encoding='utf-8') as fh:
            kept = [c for c in json.load(fh)
                    if not (c['year'] == year and c['level'] == LEVEL_WORD[level])]
        with open(AUTHORED, 'w', encoding='utf-8') as fh:
            json.dump(kept, fh, ensure_ascii=False, indent=1)
            fh.write('\n')
    authored, new = sitting_cards(year, level, generated)
    lv = LEVEL_WORD[level]
    out = [_correct(c) if (c['year'], c['level']) == (year, lv) else c for c in authored]
    # Beside its own sitting's cards, or after the newest earlier sitting of
    # the same level.
    at = max((i for i, c in enumerate(out) if c['level'] == lv and c['year'] <= year),
             default=len(out) - 1) + 1
    out = out[:at] + new + out[at:]
    with open(AUTHORED, 'w', encoding='utf-8') as fh:
        json.dump(out, fh, ensure_ascii=False, indent=1)
        fh.write('\n')
    return new


TAGS = os.path.join(ROOT, 'scripts', 'paper-trail', 'topic-tags', 'tags', 'polish.json')
FILINGS = '/Users/alexlinehan/Documents/NextStepUni-MarkBank-Lanes-20261104/languages-q3/filings-pending.json'


def atlas_rows(year, level):
    """The sitting's two English booklets as Topic Atlas wave rows, numbered as
    the paper prints them: the written booklet by its question numbers
    (Pytanie/Zadanie 1-5), the Listening Comprehension booklet by its five
    parts (Część A-E as 1-5, which is how its answer map numbers them, as
    German's aural booklet numbers its parts 1-4)."""
    import pl_paper
    from pl_topics import topic_for
    P = pl_paper.PlPaper(year, level)
    letter = {'hl': 'A', 'ol': 'G'}[level]
    if year <= 2021:
        return [old_exam_row(year, level, letter, P, topic_for)]
    written = sorted({(a.section, a.q) for a in P.all_asks() if a.section in ('A', 'B')},
                     key=lambda t: t[1])
    parts = sorted({a.section[1] for a in P.aural_asks()})
    return [
        {'subjectId': 'polish', 'level': LEVEL_WORD[level], 'lang': 'ev', 'year': year,
         'fileid': f'LC548{letter}LP000EV.pdf', 'paperKey': 'single',
         'q': [{'n': str(q), 'primary': topic_for(year, sec)} for sec, q in written]},
        {'subjectId': 'polish', 'level': LEVEL_WORD[level], 'lang': 'ev', 'year': year,
         'fileid': f'LC548{letter}LPA00EV.pdf', 'paperKey': 'aural',
         'q': [{'n': str(i + 1), 'primary': topic_for(year, 'L' + p)} for i, p in enumerate(parts)]},
    ]


ANSWERS = os.path.join(ROOT, 'scripts', 'paper-trail', 'answers')
ROMAN = ['I', 'II', 'III', 'IV', 'V']


def old_exam_row(year, level, letter, P, topic_for):
    """The old examination's one booklet, numbered as its answer map numbers
    it (the keys Paper Trail anchors on): 2021 numbers Część I's questions 1-6
    and its essay 7; 2020 and earlier number the Części themselves, 1 to 3 or 4.
    Each number is checked against the census's sections."""
    fileid = f'LC548{letter}LP000EV.pdf'
    with open(os.path.join(ANSWERS, str(year), f'{fileid}.json'), encoding='utf-8') as fh:
        ns = [q['n'] for q in json.load(fh)['q']]
    sections = {}
    for a in P.all_asks():
        sections.setdefault(a.section, set()).add(a.q)
    if year == 2021:
        first = sorted(sections['I'])
        if ns != [str(q) for q in first] + [str(len(first) + 1)] or set(sections) != {'I', 'II'}:
            raise ValueError(f'{year}: answer map {ns} does not match Część I {first} + the essay')
        q = ([{'n': str(n), 'primary': topic_for(year, 'I')} for n in first]
             + [{'n': ns[-1], 'primary': topic_for(year, 'II')}])
    else:
        if set(sections) != set(ROMAN[:len(ns)]) or ns != [str(i) for i in range(1, len(ns) + 1)]:
            raise ValueError(f'{year}: answer map {ns} does not match the Części {sorted(sections)}')
        q = [{'n': n, 'primary': topic_for(year, ROMAN[int(n) - 1])} for n in ns]
    return {'subjectId': 'polish', 'level': LEVEL_WORD[level], 'lang': 'ev', 'year': year,
            'fileid': fileid, 'paperKey': 'single', 'q': q}


def write_tags(year, level):
    with open(TAGS, encoding='utf-8') as fh:
        rows = json.load(fh)
    new = atlas_rows(year, level)
    key = lambda r: (r['year'], r['level'], r['lang'], r['fileid'])
    fresh = {key(r): r for r in new}
    # In place where the booklet is already tagged, appended where it is not;
    # every other row and the file's own layout are left as they are.
    rows = [fresh.pop(key(r), r) for r in rows] + list(fresh.values())
    with open(TAGS, 'w', encoding='utf-8') as fh:
        json.dump(rows, fh, ensure_ascii=False, indent=1)
        fh.write('\n')
    return new


def write_filings(cards):
    """card id -> the heading it would file under and why, ready for the
    model lane's filing tool (CARD-STANDARD 9). Polish has no exam-topic
    headings in the Atlas: its heading list is the curriculum outline the
    Atlas tags already use, so the heading is the card's own topic, which is
    also the tag of the printed question it answers."""
    why = {'polish-2-1': 'a listening ask: the Atlas files the Listening Comprehension booklet '
                         'part under Aural (polish-2-1)',
           'polish-3-1': 'a reading ask of the post-2022 paper: Section A Czytanie, filed under '
                         'Reading — Matching, Multiple-Choice & True/False (polish-3-1)',
           'polish-3-3': 'a written task: Section B Pisanie, filed under Written Production '
                         '(polish-3-3)'}
    data = {}
    if os.path.exists(FILINGS):
        with open(FILINGS, encoding='utf-8') as fh:
            data = json.load(fh)
    for c in cards:
        data[c['id']] = {'heading': c['topicId'], 'questionRef': c['questionRef'],
                         'reason': why.get(c['topicId'], 'the card\'s own topic')}
    with open(FILINGS, 'w', encoding='utf-8') as fh:
        json.dump(dict(sorted(data.items())), fh, ensure_ascii=False, indent=1)
        fh.write('\n')


def review(year, level):
    _authored, new = sitting_cards(year, level)
    kinds = collections.Counter(
        'listening' if c['section'].startswith('L') else
        'writing' if c.get('kind') == 'rubric' or c['section'] in ('II', 'III') else 'reading'
        for c in new)
    print(f'{year} {level}: {len(new)} new cards {dict(kinds)}')
    for c in new:
        if c['section'].startswith('L') or c.get('kind') == 'rubric' or c['section'] in ('II', 'III'):
            continue
        print(f"{c['id']:22} {c['totalMarks']:2} | {c['questionText'][:110]}")
        for r in c['rows']:
            g = r.get('group')
            if g:
                print(f"       any {g['claimMax']}x{g['perOption']} {g['options'][:6]} {g.get('optionMarks', '')}")
            else:
                print(f"       {r['kind']} {r['marks']} {r['verbatim'][:100]!r}")


def main():
    cmd, year, level = sys.argv[1], int(sys.argv[2]), sys.argv[3]
    if cmd == 'review':
        review(year, level)
    elif cmd == 'write':
        new = write(year, level)
        print(f'{year} {level}: {len(new)} cards added to {AUTHORED}')
        write_filings(new)
        for r in write_tags(year, level):
            print(f"  atlas {r['fileid']} {r['paperKey']}: {[q['n'] + ' ' + q['primary'] for q in r['q']]}")
    elif cmd == 'tags':
        for r in write_tags(year, level):
            print(f"  atlas {r['fileid']} {r['paperKey']}: {[q['n'] + ' ' + q['primary'] for q in r['q']]}")
    elif cmd == 'filings':
        with open(AUTHORED, encoding='utf-8') as fh:
            cards = [c for c in json.load(fh) if c['year'] == year and c['level'] == LEVEL_WORD[level]
                     and (c['section'].startswith('L') or c['section'] == 'B' or c['id'] in set(sys.argv[4:]))]
        write_filings(cards)
    return 0


if __name__ == '__main__':
    sys.exit(main())
