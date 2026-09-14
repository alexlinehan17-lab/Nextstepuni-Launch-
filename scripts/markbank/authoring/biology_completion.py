#!/usr/bin/env python3
"""Complete Biology at the marking boundary the paper actually prices.

The recovered 2016--2020 schemes predate the first hand-authored Biology
wave, so every ask in those ten papers was open.  Later schemes leave a small
number of content-free leaf answers (``any valid example``) between otherwise
complete cards.  Biology prices those leaves together: Section A prices a
whole short question, and Sections B/C normally print one tariff for an outer
letter and all of its roman children.  This generator therefore publishes one
card at that printed boundary.  It never invents a leaf tariff and it never
uses a scheme criterion as a stand-alone answer.

Question wording comes only from the paper reader.  Answer rows are contiguous
text lifted from the matching scheme boundary and must pass the same
verify-claims provenance gate as the deck build.  The target census is pinned
in biology-completion-targets.json so a zero-open rebuild cannot erase the
completion layer that produced it.
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import unicodedata
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mathtext  # noqa: E402
from paper import Paper, unligature  # noqa: E402
from paper_census import (  # noqa: E402
    ROMANS, census_merged, census_subject, key_label, leaves_of,
    marks_by_question,
)
from reconcile import reconcile_subject  # noqa: E402


DIR = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(DIR)))
TARGETS_PATH = os.path.join(
    ROOT, 'scripts', 'markbank', 'authored',
    'biology-completion-targets.json')
VERIFY = os.path.join(DIR, 'verify-claims.mjs')

TOKEN = re.compile(r"[^\W_]+(?:['’][^\W_]+)?", re.UNICODE)
MARK_TOKEN = re.compile(
    r'⟨\s*\(?\s*([^⟩]*?\d[^⟩]*?)\s*\)?\s*⟩'
    r'|\[\s*([^\]]*?\d[^\]]*?)\s*\]')
PAPER_MARK = re.compile(r'\((\d{1,2})\s*(?:marks?)?\)', re.I)
PAGE = re.compile(
    r'^(?:##\s*Page|Page\s+\d+|Leaving Certificate|Biology\s*[–-]|'
    r'Ordinary Level Biology|Higher Level Biology|Marking Scheme|Section\s+[ABC]|'
    r'Blank Page|Copyright notice|Acknowledgements)', re.I)
MARK_ONLY = re.compile(
    r'^[\[\]⟨⟩()\d\s+x×:;,./+–—-]*(?:marks?)?'
    r'[\[\]⟨⟩()\d\s+x×:;,./+–—-]*$', re.I)
TARIFF_LINE = re.compile(
    r'^(?:(?:best|any)\s+\w+\s+answers?\s+from\s+\([a-z]\)\s*[–-]\s*\([a-z]\)\s*)?'
    r'[\d\s()+x×,–—.+]+(?:i\.e\..*)?$', re.I)
CONTENT_FREE = re.compile(
    r'^(?:any valid (?:answer|example|reason)|correct(?:ly)?\s+(?:named|drawn|'
    r'labelled|shown|stated|described|identified|matched)(?:\s+\w+){0,5}|'
    r'diagram|drawing|labels?|answer|example|reason|description|name|role|'
    r'function|location|treatment|cause|effect|application)[\s,;:/&-]*$', re.I)
QUESTIONISH = re.compile(
    r'^(?:what|why|how|when|where|which|who|name|state|give|list|define|'
    r'explain|describe|identify|suggest|outline|calculate|draw|sketch|compare|'
    r'distinguish|account|match|complete|write|find|show|determine|use)\b', re.I)
FURNITURE_CUT = re.compile(
    r'\b(?:\[OVER\]|Page\s+\d+\s+of\s+\d+|Leaving Certificate(?: Examination)?'
    r'[–,—\s]|Blank Page|Copyright notice|This question continues)\b', re.I)
PART_PREFIX = re.compile(
    r'^(?P<prefix>(?:\((?:[a-h]|xii|viii|vii|vi|iv|iii|ii|i|ix|xi|x|v)\s*\)\s*)+)')
NUMBERED = re.compile(r'^\d+[.)]\s+')
Q_SPELLED = re.compile(
    r'^(?:Question\s+|Q\s*)(\d{1,2})\s*:?[.]?\s*(.*)$', re.I)
Q_NUMBER = re.compile(r'^(\d{1,2})[.]?\s+(.*)$')
Q_BARE = re.compile(r'^(\d{1,2})[.]?$')
LETTER = re.compile(r'^\(([a-h])\s*\)\s*(.*)$')


def fold(text: str) -> str:
    return unicodedata.normalize('NFKD', text).encode(
        'ascii', 'ignore').decode().casefold()


def natural(key):
    q, letter, roman = key
    return (q, letter or '', ROMANS.index(roman) if roman in ROMANS else 99)


def clean_paper_text(text):
    text = unligature(text or '')
    text = FURNITURE_CUT.split(text, maxsplit=1)[0]
    text = re.sub(r'_{3,}', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip(' \t\n;')


def display_text(text):
    text = ''.join(mathtext.GLYPH.get(char, char) for char in text)
    if mathtext.unreadable(text):
        return None
    return text


def strip_marks(text):
    text = MARK_TOKEN.sub(' ', text)
    text = re.sub(r'\s+\(?\d{1,2}\s*(?:marks?)?\)?\s*$', ' ', text,
                  flags=re.I)
    return ' '.join(text.split()).strip(' •;,')


def boundary_for(year, key):
    q, letter, _ = key
    # Section A short questions share one printed best-of/ordered tariff.
    if q <= (7 if year >= 2021 else 6):
        return (q, None, None)
    # Later sections price the outer route, including every roman below it.
    return (q, letter, None) if letter else (q, None, None)


def key_suffix(key):
    q, letter, _ = key
    return f'q{q}' + (letter or '')


def refresh_targets():
    census = census_subject('biology')
    audit = reconcile_subject('biology', census)
    payload = {
        'paperLeafCount': audit['leaves'],
        'targetCount': audit['open'],
        'censusCounts': {
            f"{p['year']}-{p['level']}": p['leafCount']
            for p in census['papers']
        },
        'targets': [
            {'year': p['year'], 'level': p['level'], 'label': label}
            for p in audit['papers'] for label in p['open']
        ],
    }
    with open(TARGETS_PATH, 'w', encoding='utf-8') as fh:
        json.dump(payload, fh, ensure_ascii=False, indent=1)
        fh.write('\n')
    print(f'wrote {TARGETS_PATH}', file=sys.stderr)


def load_targets():
    payload = json.load(open(TARGETS_PATH, encoding='utf-8'))
    out = defaultdict(set)
    for row in payload['targets']:
        out[(row['year'], row['level'])].add(row['label'])
    if sum(map(len, out.values())) != payload['targetCount']:
        raise AssertionError('Biology completion target count is stale')
    return payload, out


def scheme_lines(year, level):
    path = os.path.join(
        ROOT, 'examiner-reports', 'biology', 'schemes',
        f'{year}-{level}.md')
    raw = open(path, encoding='utf-8', errors='ignore').read()
    raw = raw.split('<!-- markbank:', 1)[0].split(
        '<!-- pdf-block-order', 1)[0]
    lines = [' '.join(line.split()) for line in raw.splitlines()]
    # The preamble itself numbers examples 1, 2 and 3.  The real answer table
    # starts only at the explicit Section A assessment heading.
    starts = [i for i, line in enumerate(lines)
              if re.match(r'^Section A(?:\s*$|.*\b(?:Best|Answer)\b)',
                          line, re.I)]
    if not starts:
        raise RuntimeError(f'{year} {level}: no Section A scheme boundary')
    return lines[starts[-1] + 1:], path


def parsed_scheme_groups(year, level):
    """{(q, outer-letter, None): source lines}, in printed order."""
    lines, path = scheme_lines(year, level)
    groups = defaultdict(list)
    q = None
    letter = None
    for line in lines:
        if not line or PAGE.match(line):
            continue
        spelled = Q_SPELLED.match(line)
        numbered = Q_NUMBER.match(line) if not spelled else None
        bare = Q_BARE.match(line) if not spelled and not numbered else None
        accepted = None
        rest = ''
        if spelled:
            candidate, rest = int(spelled.group(1)), spelled.group(2)
            if q is None and candidate == 1 or q is not None and (
                    candidate == q + 1 or candidate == q):
                accepted = candidate
        elif numbered:
            candidate, rest = int(numbered.group(1)), numbered.group(2)
            # A numbered marking subpoint (``1. Safety hazard``) cannot move
            # the paper's question counter backwards or jump over a question.
            if q is None and candidate == 1 or q is not None and (
                    candidate == q + 1 or
                    (candidate == q and rest.startswith('('))):
                accepted = candidate
        elif bare:
            candidate, rest = int(bare.group(1)), ''
            if q is None and candidate == 1 or q is not None and candidate == q + 1:
                accepted = candidate
        if accepted is not None:
            q = accepted
            lead = LETTER.match(rest)
            letter = lead.group(1) if lead else None
            groups[boundary_for(year, (q, letter, None))].append(rest)
            continue

        lead = LETTER.match(line)
        if q is not None and lead:
            found = lead.group(1)
            # Outer letters run forward; a lower-case enumeration inside one
            # answer is content and stays with the current boundary.
            if letter is None or found >= letter:
                letter = found
                groups[boundary_for(year, (q, letter, None))].append(line)
                continue
        if q is not None:
            groups[boundary_for(year, (q, letter, None))].append(line)
    return groups, path


def answer_rows(lines):
    """One scheme-verbatim row per printed leaf-sized answer block."""
    rows = []
    buffer = []

    def flush():
        nonlocal buffer
        text = strip_marks(' '.join(buffer))
        buffer = []
        text = re.sub(r'^(?:OR\s+)+', '', text, flags=re.I).strip()
        if (not text or MARK_ONLY.fullmatch(text) or TARIFF_LINE.fullmatch(text)
                or CONTENT_FREE.fullmatch(text)
                or sum(ch.isalnum() for ch in text) < 2):
            return
        if len(text) > 1500:
            # The scheme has packed several independently marked statements
            # onto one extraction line.  Its solidus is the official boundary
            # between acceptable points; split there rather than truncate.
            pieces = [p.strip() for p in re.split(r'\s*/\s*', text) if p.strip()]
            if len(pieces) > 1:
                for piece in pieces:
                    if len(piece) <= 1500 and piece not in rows:
                        rows.append(piece)
                return
        if text not in rows:
            rows.append(text)

    for raw in lines:
        line = ' '.join(raw.split()).strip()
        if not line or PAGE.match(line):
            continue
        if re.match(r'^\[(?:Award|Accept|Allow|Note|Maximum|If|No marks)', line, re.I):
            continue
        starts = bool(PART_PREFIX.match(line) or NUMBERED.match(line))
        if starts and buffer:
            flush()
        line = PART_PREFIX.sub('', line).strip()
        if not line or MARK_ONLY.fullmatch(line) or TARIFF_LINE.fullmatch(line):
            continue
        # A pure examiner instruction is not an answer row.
        if re.match(r'^(?:Any\s+\w+|Best\s+\w+|Award\s+|Maximum\s+)', line, re.I):
            if buffer:
                buffer.append(line)
            continue
        buffer.append(line)
    flush()
    return rows


def traceable(scheme_path, claims):
    if not claims:
        return set()
    proc = subprocess.run(
        ['node', VERIFY], cwd=ROOT, text=True, capture_output=True,
        input=json.dumps({
            'scheme': os.path.relpath(scheme_path, ROOT),
            'claims': claims,
        }))
    if proc.returncode:
        raise RuntimeError(proc.stderr.strip() or 'verify-claims failed')
    return set(json.loads(proc.stdout)['ok'])


def grouped_question(paper, boundary, members):
    q, outer, _ = boundary
    pieces = []
    if outer:
        parent = paper.text(q, outer, None) or paper.stem(q, outer)
        if parent:
            pieces.append(clean_paper_text(parent))
    else:
        parent = paper.stem(q)
        if parent:
            pieces.append(clean_paper_text(parent))
    seen_parents = set()
    for key in sorted(members, key=natural):
        _, letter, roman = key
        if not outer and letter and roman and letter not in seen_parents:
            parent = paper.text(q, letter, None) or paper.stem(q, letter)
            if parent:
                pieces.append(f'({letter}) {clean_paper_text(parent)}')
            seen_parents.add(letter)
        text = clean_paper_text(paper.text(*key) or '')
        if not text:
            continue
        label = ''.join(f'({part})' for part in (letter, roman) if part)
        pieces.append(f'{label} {text}'.strip())
    return clean_paper_text(' '.join(p for p in pieces if p))


def printed_total(question):
    values = [int(v) for v in PAPER_MARK.findall(question or '')
              if 0 < int(v) <= 80]
    return values[-1] if values else None


def boundary_total(year, boundary):
    """The fixed Biology paper structure, at its printed group boundary."""
    q, letter, _ = boundary
    if year <= 2020:
        if q <= 6:
            return 20
        if q <= 9:
            return {'a': 6, 'b': 24}.get(letter)
        if q <= 13:
            return {'a': 9, 'b': 27, 'c': 24}.get(letter)
        return 30
    if q <= 7:
        return 20
    if q <= 10:
        return {'a': 6, 'b': 24}.get(letter)
    if q <= 15:
        return {'a': 9, 'b': 27, 'c': 24}.get(letter)
    return 30


def section_map(paper):
    marks = marks_by_question(paper.files, 'biology')
    out = {}
    for (section, q), total in marks.items():
        if q not in out or section:
            out[q] = (str(section) if section else None, total)
    return out


def topic_for(text):
    s = fold(text)
    rules = [
        (r'ecolog|ecosystem|food chain|food web|population|habitat|niche|'
         r'pollution|nitrogen cycle|carbon cycle|conservation', 'bio-3-1'),
        (r'microorgan|bacter|fung|rhizopus|virus|yeast|bioprocess|antibiotic', 'bio-3-2'),
        (r'experiment|apparatus|microscope|investigation|control|hypothesis|'
         r'prepare and examine|food test', 'bio-3-3'),
        (r'cell membrane|cell wall|nucleus|mitosis|meiosis|osmosis|diffusion|'
         r'active transport|organelle|tissue culture', 'bio-1-3'),
        (r'dna|rna|gene|chromosome|hered|genetic|allele|mutation|variation|'
         r'evolution|sex.link', 'bio-1-4'),
        (r'enzyme|protein|carbohydrate|lipid|vitamin|mineral|biomolecule|food', 'bio-1-2'),
        (r'photosynth|respiration|atp|nad|metabolism', 'bio-2-2'),
        (r'plant|leaf|root|stem|xylem|phloem|transpiration|tropism|seed|'
         r'germination|flower|pollination', 'bio-2-6'),
        (r'heart|blood|circul|breath|lung|kidney|excret|homeostasis|digest|'
         r'neuron|brain|eye|ear|skeleton|bone|muscle', 'bio-2-4'),
        (r'reproduc|fertili|menstrual|embryo|placenta|gamete', 'bio-2-5'),
        (r'immune|antibody|vaccine|lymphocyte|disease', 'bio-2-3'),
        (r'cell|organism|classification|kingdom', 'bio-1-1'),
    ]
    for pattern, topic in rules:
        if re.search(pattern, s):
            return topic
    return 'bio-u1'


def slug(question):
    stop = {'a', 'an', 'and', 'the', 'of', 'to', 'in', 'for', 'on', 'with',
            'each', 'following', 'one', 'two', 'three', 'what', 'how', 'why',
            'give', 'state', 'explain', 'describe', 'calculate', 'draw', 'show'}
    words = [fold(m.group()) for m in TOKEN.finditer(question)]
    words = [word for word in words if word and word not in stop][:10]
    return '-'.join(words) or 'paper-task'


def make_card(year, level, boundary, question, total, rows, section):
    q, letter, _ = boundary
    ref = f'{year} {level.upper()} Q{q}' + (f'({letter})' if letter else '')
    return {
        'id': f'bio-{year}-{level}-completion-{key_suffix(boundary)}',
        'topicId': topic_for(question),
        'conceptId': slug(question),
        'level': 'higher' if level == 'hl' else 'ordinary',
        'year': year,
        'subjectId': 'biology',
        'section': section,
        'questionRef': ref,
        'questionText': question,
        'tariffModel': {'kind': 'questionTotal'},
        'totalMarks': total,
        'rows': [
            {'id': f'r-{i}', 'kind': 'point', 'verbatim': row, 'marks': None}
            for i, row in enumerate(rows, 1)
        ],
        'notes': ('Question wording is lifted from the SEC paper and answer '
                  'content from its marking scheme. Biology prices this '
                  'printed group as a whole, so no row-level tariff is '
                  'inferred.'),
    }


def build():
    payload, target_sets = load_targets()
    census = census_subject('biology')
    paper_records = {(p['year'], p['level']): p for p in census['papers']}
    cards = []
    held = []
    observed = 0

    for year in range(2016, 2026):
        for level in ('hl', 'ol'):
            record = paper_records[(year, level)]
            parts, _texts, _ = census_merged('biology', year, level)
            leaves = leaves_of(parts)
            expected = payload['censusCounts'][f'{year}-{level}']
            if len(leaves) != expected or record['leafCount'] != expected:
                raise AssertionError(
                    f'{year} {level}: census drifted {expected} -> {len(leaves)}')
            lookup = {key_label(key): key for key in leaves}
            wanted_labels = target_sets.get((year, level), set())
            missing = wanted_labels - set(lookup)
            if missing:
                raise AssertionError(
                    f'{year} {level}: target(s) absent {sorted(missing)[:5]}')
            targets = {lookup[label] for label in wanted_labels}
            observed += len(targets)

            by_boundary = defaultdict(list)
            for leaf in leaves:
                by_boundary[boundary_for(year, leaf)].append(leaf)
            selected = {boundary for boundary, members in by_boundary.items()
                        if set(members) & targets}
            scheme, scheme_path = parsed_scheme_groups(year, level)
            paper = Paper('biology', year, level)
            sections = section_map(paper)

            proposals = {}
            for boundary in selected:
                raw_rows = answer_rows(scheme.get(boundary, []))
                proposals[boundary] = raw_rows
            claims = list(dict.fromkeys(
                row for rows in proposals.values() for row in rows))
            good = traceable(scheme_path, claims)

            made = 0
            for boundary in sorted(selected, key=natural):
                members = by_boundary[boundary]
                question = display_text(grouped_question(
                    paper, boundary, members))
                rows = [display_text(row) for row in proposals[boundary]
                        if row in good]
                rows = [row for row in rows if row is not None]
                # One row per printed leaf normally stays below 30; retain the
                # complete group where the scheme has a few explicit subrows.
                rows = rows[:40]
                q = boundary[0]
                section, question_total = sections.get(q, (None, None))
                total = boundary_total(year, boundary)
                # Keep the independently read paper value as a cross-check
                # where the group prints it explicitly. Some leaf text omits
                # the shared tariff, which is why boundary_total is primary.
                seen_total = printed_total(question)
                if seen_total and total and seen_total != total:
                    held.append((year, level, boundary,
                                 f'paper total {seen_total} disagrees with group total {total}'))
                    continue
                if not section:
                    # Stable Biology section families, used only when the
                    # independent page-heading pass cannot see a header.
                    split_a = 7 if year >= 2021 else 6
                    split_b = 10 if year >= 2021 else 9
                    section = 'A' if q <= split_a else 'B' if q <= split_b else 'C'
                if not question:
                    held.append((year, level, boundary, 'no safe paper wording'))
                elif not total:
                    held.append((year, level, boundary, 'no printed group total'))
                elif not rows:
                    held.append((year, level, boundary,
                                 'no traceable content-bearing answer row'))
                else:
                    cards.append(make_card(
                        year, level, boundary, question, total, rows, section))
                    made += 1
            print(f'{year} {level}: {made}/{len(selected)} cards', file=sys.stderr)

    if observed != payload['targetCount']:
        raise AssertionError(
            f'target total drifted {payload["targetCount"]} -> {observed}')
    for year, level, boundary, why in held:
        print(f'HELD {year} {level} {key_label(boundary)} — {why}',
              file=sys.stderr)
    return cards


if __name__ == '__main__':
    if '--refresh-targets' in sys.argv:
        refresh_targets()
    else:
        print(json.dumps(build(), ensure_ascii=False, indent=1))
