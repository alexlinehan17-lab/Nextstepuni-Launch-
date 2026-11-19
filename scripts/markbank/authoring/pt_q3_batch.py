#!/usr/bin/env python3
"""Add one Portuguese sitting's cards to the bank (languages-q3 lane).

    python3 scripts/markbank/authoring/pt_q3_batch.py review 2026 hl
    python3 scripts/markbank/authoring/pt_q3_batch.py write 2026 hl
    python3 scripts/markbank/authoring/pt_q3_batch.py add 2023 ol   # a held ask, since unblocked

On the Polish pattern (pl_q3_batch.py). The live 2021-2025 cards were written
by the shared generator (eu_all.py), which no longer reproduces all of them
byte for byte, so the authored file is NEVER regenerated: a sitting's new
cards are merged in beside the live ones, and a live card is never touched.

A sitting's new cards are
* the reading asks eu_all cards correctly and that are not live yet, as it
  writes them;
* the reading asks a spec in pt_specs.py takes over (refused by eu_all, or
  shaped wrongly by it): those ids are dropped from eu_all's output;
* every listening ask (pt_specs.LISTENING), with the year's recording from
  data/portugueseAudio.json (CARD-STANDARD 10g);
* the written tasks (pt_writing.py) — HELD for 2025 and 2026, whose schemes
  print a word-count lower scale that waits on the shared lower-scale change
  (coordinator ruling 19 Nov 2026): those asks stay open until it lands.
"""
import collections
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
sys.path.insert(0, HERE)

AUTHORED = os.path.join(ROOT, 'scripts', 'markbank', 'authored', 'portuguese.json')
TAGS = os.path.join(ROOT, 'scripts', 'paper-trail', 'topic-tags', 'tags', 'portuguese.json')
FILINGS = '/Users/alexlinehan/Documents/NextStepUni-MarkBank-Lanes-20261104/languages-q3/filings-pending.json'
LEVEL_WORD = {'hl': 'higher', 'ol': 'ordinary'}
# Sittings with no live card before this lane: a rewrite replaces them whole.
ALL_NEW = {2026}
# Written tasks held: 2025/2026 for the shared lower-scale change (see the
# docstring); 2022/2023 because their grids print every mark, band range and
# rung price only in the marks cells, which provenance strips (schemeText
# MARKS_CELL) -- asked of the coordinator 19 Nov 2026.
WRITING_HELD = {2022, 2023, 2025, 2026}

_GENERATED = None


def generated():
    global _GENERATED
    if _GENERATED is None:
        import eu_all
        _GENERATED = eu_all.build('portuguese')[0]
    return _GENERATED


def sitting_cards(year, level, present='raise'):
    """The sitting's cards not yet in the bank. present='raise' refuses a
    card whose id is already there; present='skip' (the add command) leaves
    it out, but only if it regenerates byte for byte as it stands."""
    import pt_specs
    with open(AUTHORED, encoding='utf-8') as fh:
        authored = json.load(fh)
    have = {c['id'] for c in authored}
    lv = LEVEL_WORD[level]
    specs = pt_specs.reading_cards(year, level)
    spec_ids = {c['id'] for c in specs}
    reading = [json.loads(json.dumps(c)) for c in generated()
               if c['year'] == year and c['level'] == lv
               and c['id'] not in have and c['id'] not in spec_ids]
    new = reading + specs
    if year >= 2022:
        new += pt_specs.listening_cards(year, level)
        if year not in WRITING_HELD:
            import pt_writing
            new += pt_writing.cards(year, level)
    ids = [c['id'] for c in new]
    dup = [i for i, n in collections.Counter(ids).items() if n > 1]
    if dup:
        raise ValueError(f'{year} {level}: duplicate new ids {dup}')
    clash = [i for i in ids if i in have]
    if clash and present == 'skip':
        by_id = {c['id']: c for c in authored}
        drift = [c['id'] for c in new if c['id'] in have
                 and json.dumps(c, sort_keys=True) != json.dumps(by_id[c['id']], sort_keys=True)]
        if drift:
            raise ValueError(f'{year} {level}: cards in the bank no longer regenerate as they stand {drift}')
        new = [c for c in new if c['id'] not in have]
    elif clash:
        raise ValueError(f'{year} {level}: new ids already live {clash}')
    order = {k: i for i, k in enumerate(['A', 'B', 'LA', 'LB', 'LC', 'LD', 'LE'])}

    def place(c):
        key = pt_specs.parse_key(_spec_key(c))
        return (order.get(key[0], 99), key[1], key[2] or '', key[3] or '')
    new.sort(key=place)
    return authored, new


def _spec_key(card):
    """'por-2026-hl-la-4-ii' -> 'LA4ii'; 'por-2026-hl-a-1-b' -> 'A1b'."""
    parts = card['id'].split('-')[3:]
    sec = parts[0].upper()
    rest = parts[1:]
    q = rest[0]
    tail = rest[1:]
    if sec.startswith('L'):
        return f'{sec}{q}{tail[0]}-{tail[1]}' if len(tail) == 2 else f'{sec}{q}{"".join(tail)}'
    letter = tail[0] if tail else ''
    roman = f'-{tail[1]}' if len(tail) > 1 else ''
    return f'{sec}{q}{letter}{roman}'


def write(year, level):
    lv = LEVEL_WORD[level]
    if year in ALL_NEW:
        with open(AUTHORED, encoding='utf-8') as fh:
            kept = [c for c in json.load(fh) if not (c['year'] == year and c['level'] == lv)]
        with open(AUTHORED, 'w', encoding='utf-8') as fh:
            json.dump(kept, fh, ensure_ascii=False, indent=1)
            fh.write('\n')
    authored, new = sitting_cards(year, level)
    # After its own sitting's last card, or else after the newest earlier
    # sitting of the same level (2026, which had none, went after 2025).
    at = max((i for i, c in enumerate(authored) if c['level'] == lv and c['year'] == year),
             default=None)
    if at is None:
        at = max((i for i, c in enumerate(authored) if c['level'] == lv and c['year'] < year),
                 default=len(authored) - 1)
    out = authored[:at + 1] + new + authored[at + 1:]
    with open(AUTHORED, 'w', encoding='utf-8') as fh:
        json.dump(out, fh, ensure_ascii=False, indent=1)
        fh.write('\n')
    return new


def add(year, level):
    """Add the cards a sitting already in the bank still lacks (an ask held
    and since unblocked). Each goes straight after the last card of its
    sitting that comes before it in paper order, so the lane's cards stay in
    paper order after the live ones; no card already there moves or changes."""
    authored, new = sitting_cards(year, level, present='skip')
    lv = LEVEL_WORD[level]
    order = {k: i for i, k in enumerate(['A', 'B', 'LA', 'LB', 'LC', 'LD', 'LE'])}
    import pt_specs

    def place(c):
        key = pt_specs.parse_key(_spec_key(c))
        return (order.get(key[0], 99), key[1], key[2] or '', key[3] or '')
    out = list(authored)
    for c in new:
        mine = [i for i, x in enumerate(out) if x['year'] == year and x['level'] == lv]
        before = [i for i in mine if place(out[i]) < place(c)]
        at = max(before) if before else (min(mine) - 1 if mine else len(out) - 1)
        out.insert(at + 1, c)
    with open(AUTHORED, 'w', encoding='utf-8') as fh:
        json.dump(out, fh, ensure_ascii=False, indent=1)
        fh.write('\n')
    return new


def atlas_rows(year, level):
    """The sitting's English booklets as Topic Atlas wave rows, numbered as the
    paper prints them: the written booklet by its question numbers (Question
    1-5; no answer map exists for most of these booklets), the Listening
    Comprehension booklet by its five Partes (A-E as 1-5, as its answer map
    numbers them)."""
    from eu_paper import EuPaper
    from eu_topics import topic_for
    P = EuPaper(year, level, 'portuguese')
    letter = {'hl': 'A', 'ol': 'G'}[level]
    written = sorted({(a.section, a.q) for a in P.all_asks() if a.section in ('A', 'B')},
                     key=lambda t: t[1])
    rows = [{'subjectId': 'portuguese', 'level': LEVEL_WORD[level], 'lang': 'ev', 'year': year,
             'fileid': f'LC018{letter}LP000EV.pdf', 'paperKey': 'single',
             'q': [{'n': str(q), 'primary': topic_for('portuguese', P.era, sec)} for sec, q in written]}]
    if year >= 2022:
        parts = sorted({a.section[1] for a in P.aural_asks()})
        _check_aural_map(year, letter, parts)
        rows.append({'subjectId': 'portuguese', 'level': LEVEL_WORD[level], 'lang': 'ev', 'year': year,
                     'fileid': f'LC018{letter}LPA00EV.pdf', 'paperKey': 'aural',
                     'q': [{'n': str(i + 1), 'primary': topic_for('portuguese', P.era, 'L' + p)}
                           for i, p in enumerate(parts)]})
    return rows


def _check_aural_map(year, letter, parts):
    path = os.path.join(ROOT, 'scripts', 'paper-trail', 'answers', str(year), f'LC018{letter}LPA00EV.pdf.json')
    if not os.path.exists(path):
        return
    with open(path, encoding='utf-8') as fh:
        mapped = json.load(fh)['q']
    ns = [q['n'] for q in mapped]
    if not any(q.get('label') for q in mapped) and ns != [str(i + 1) for i in range(len(parts))]:
        # An unlabelled map that does not number the Partes: the 2024 maps
        # number Parte A's questions and anchor them on the scheme's reading
        # pages (a Paper Trail defect, reported). The rows number the Partes
        # 1-5, the convention of every labelled Portuguese map, so a mended
        # map lines up with them.
        print(f'  NOTE {year} {letter}: aural answer map numbers {ns} without labels; Partes numbered 1-{len(parts)}')
        return
    if ns != [str(i + 1) for i in range(len(parts))]:
        raise ValueError(f'{year} {letter}: aural answer map numbers {ns} against Partes {parts}')
    for q, p in zip(mapped, parts):
        label = (q.get('label') or '').strip()
        if label and not label.startswith(f'Parte {p}'):
            raise ValueError(f'{year} {letter}: aural answer map {q["n"]} is {label!r}, not Parte {p}')


def write_tags(year, level):
    with open(TAGS, encoding='utf-8') as fh:
        rows = json.load(fh)
    new = atlas_rows(year, level)
    key = lambda r: (r['year'], r['level'], r['lang'], r['fileid'])        # noqa: E731
    fresh = {key(r): r for r in new}
    rows = [fresh.pop(key(r), r) for r in rows] + list(fresh.values())
    with open(TAGS, 'w', encoding='utf-8') as fh:
        json.dump(rows, fh, ensure_ascii=False, indent=1)
        fh.write('\n')
    return new


def write_filings(cards):
    """card id -> the heading it would file under and why (CARD-STANDARD 9).
    Portuguese has no exam-topic headings in the Atlas: its heading list is the
    curriculum outline its Atlas tags use, so the heading is the card's own
    topic, which is also the tag of the printed question it answers."""
    why = {'portuguese-2-3': 'a reading ask of the post-2022 paper: Section A Reading Comprehension, '
                             'filed under Reading Comprehension — two texts (portuguese-2-3)',
           'portuguese-2-4': 'a written task: Section B Written Production, filed under Written '
                             'Production (portuguese-2-4)',
           'portuguese-2-5': 'a listening ask: the Atlas files the Listening Comprehension booklet '
                             'Parte under Listening Comprehension Test (portuguese-2-5)'}
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
    kinds = collections.Counter('listening' if c['section'].startswith('L') else
                                'writing' if c['section'] == 'B' else 'reading' for c in new)
    print(f'{year} {level}: {len(new)} new cards {dict(kinds)}')
    for c in new:
        print(f"  {c['id']:24} {c['totalMarks']:2} {c['tariffModel']['kind'][:5]} | {c['questionText'][:90]}")


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
    elif cmd == 'add':
        new = add(year, level)
        print(f'{year} {level}: {len(new)} cards added to {AUTHORED}: {[c["id"] for c in new]}')
        write_filings(new)
    elif cmd == 'tags':
        for r in write_tags(year, level):
            print(f"  atlas {r['fileid']} {r['paperKey']}: {[q['n'] + ' ' + q['primary'] for q in r['q']]}")
    return 0


if __name__ == '__main__':
    sys.exit(main())
