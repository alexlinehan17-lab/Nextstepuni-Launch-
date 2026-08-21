#!/usr/bin/env python3
"""
Mark Bank — recover marking points that the flat scheme extraction interleaves.

    python3 scripts/markbank/append-scheme-columns.py <subject> <year> <hl|ol>
    python3 scripts/markbank/append-scheme-columns.py --all          # every scheme with a PDF

SEC schemes set parallel answers side by side, and the flat extraction reads
across the page, so the two columns come out shuffled into each other:

    Increase heart rate or increase blood   Increase heart rate or strengthens
    or pressure or any valid effect         heart muscle or any valid effect

reads as "Increase heart rate or increase blood Increase heart rate or
strengthens or pressure or any valid effect heart muscle or any valid effect".
Neither column survives, so a card quoting either is dropped as untraceable even
though the SEC printed it exactly.

append-scheme-tables.py does not reach these. It works from find_tables(), and
where the two columns live inside ONE cell — which is how the SEC sets the
"either/or" answers — there is no cell boundary to read them apart at. This
works from word coordinates instead, so it does not care whether a rule was
drawn.

The columns are also joined DOWNWARD, which is the other thing the flat text
loses. Where the scheme prints

    Method     Runners          Root suckers   Leaflets
    examples:  (strawberries)   (holly bush)   (Devil's backbone)
    Organ:     Stem             Root           Leaf

a card pairing "Runners" with its own example is quoting one column, and gets it.

APPEND-ONLY, and that is the whole safety argument, the same one
append-scheme-tables.py makes: comparableScheme() joins every line, so each
substring that matches today still matches afterwards. No card that passes can
start failing. Nothing is invented either — every emitted line is words the SEC
printed, in the order its own column reads.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import pymupdf

sys.path.insert(0, str(Path(__file__).resolve().parent))
from markbank_text import unligature  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
START = '<!-- markbank:column-runs -->'
END = '<!-- /markbank:column-runs -->'

# A word space at the SEC's body size is 2–4pt. A column gutter is far wider.
# Below ~10 the emitted "columns" are just wide word spacing inside one sentence.
GUTTER = 11.0
# Two words belong to the same printed line if their tops agree this closely.
LINE_TOL = 3.0
# Two fragments belong to the same column if their left edges agree this closely.
COLUMN_TOL = 12.0
# A run ends where the vertical step between printed lines breaks.
ROW_GAP_FACTOR = 2.2
# A single-column line is only absorbed into a run if it sits inside a column
# rather than spanning the block — otherwise ordinary prose under a table would
# be swallowed and emitted as if it were part of it.
SPAN_TOL = 12.0
# The SEC prints a bare "or" between two answer boxes, centred in the gutter, so
# it belongs to neither column and lines up with neither. Ending the run there
# split every either/or answer in half — the exact answers this exists to
# recover. Short lone fragments are stepped over instead: not joined into a
# column, not treated as the end of the block.
CONNECTOR_MAX_CHARS = 24


def fragments(words, gutter=GUTTER):
    """One printed line's words split at its column gutters."""
    words = sorted(words, key=lambda w: w[0])
    out, cur = [], [words[0]]
    for w in words[1:]:
        if w[0] - cur[-1][2] > gutter:
            out.append(cur)
            cur = [w]
        else:
            cur.append(w)
    out.append(cur)
    return [(f[0][0], f[-1][2], ' '.join(w[4] for w in f)) for f in out]


def printed_lines(page):
    """The page's words grouped into the lines they were printed on."""
    words = [w for w in page.get_text('words') if w[4].strip()]
    if not words:
        return []
    words.sort(key=lambda w: (round(w[1], 1), w[0]))
    lines, cur, top = [], [words[0]], words[0][1]
    for w in words[1:]:
        if abs(w[1] - top) > LINE_TOL:
            lines.append((top, cur))
            cur, top = [w], w[1]
        else:
            cur.append(w)
    lines.append((top, cur))
    return [(top, fragments(ws)) for top, ws in lines]


def runs(lines):
    """Consecutive printed lines that share a column structure."""
    out, cur, prev_top = [], [], None
    step = median_step(lines)
    for top, frags in lines:
        multi = len(frags) > 1
        adjacent = prev_top is not None and (top - prev_top) < step * ROW_GAP_FACTOR
        if cur and adjacent and (multi or absorbable(frags, cur)):
            cur.append(frags)
        elif cur and adjacent and len(frags[0][2]) <= CONNECTOR_MAX_CHARS:
            pass                      # a connector printed between the boxes
        elif multi:
            if len(cur) > 1:
                out.append(cur)
            cur = [frags]
        else:
            if len(cur) > 1:
                out.append(cur)
            cur = []
        prev_top = top
    if len(cur) > 1:
        out.append(cur)
    return out


def median_step(lines):
    steps = sorted(b[0] - a[0] for a, b in zip(lines, lines[1:]) if b[0] > a[0])
    return steps[len(steps) // 2] if steps else 12.0


def absorbable(frags, run):
    """A continuation line of one column, not a fresh full-width line.

    A wrapped column often has nothing beside it, so the line reads as a single
    fragment and would otherwise end the run — which is exactly how the second
    half of "Difficulty breathing or tightening of / muscles around airways" was
    being lost.
    """
    if len(frags) != 1:
        return False
    x0, x1, _ = frags[0]
    for prev in run:
        for px0, px1, _ in prev:
            if abs(x0 - px0) <= COLUMN_TOL and x1 <= px1 + SPAN_TOL:
                return True
    return False


def columns(run):
    """A run's fragments gathered into the columns they were printed in."""
    anchors = []
    for frags in run:
        for x0, _, _ in frags:
            if not any(abs(x0 - a) <= COLUMN_TOL for a in anchors):
                anchors.append(x0)
    anchors.sort()
    if len(anchors) < 2:
        return []
    cols = {a: [] for a in anchors}
    for frags in run:
        for x0, _, text in frags:
            nearest = min(anchors, key=lambda a: abs(a - x0))
            if abs(nearest - x0) <= COLUMN_TOL:
                cols[nearest].append(text)
    return [' '.join(cols[a]) for a in anchors if len(cols[a]) > 1]


def column_runs(pdf: Path) -> list[str]:
    doc = pymupdf.open(pdf)
    out, seen = [], set()
    for page in doc:
        for run in runs(printed_lines(page)):
            for text in columns(run):
                # The PDF font encodes ligatures as glyphs, so "letters"
                # extracts as "leƩers". Anything appended has to be folded the
                # same way extract-scheme.py folds it, or the mangled form is
                # what a shipped marking point ends up quoting.
                text = unligature(re.sub(r'\s+', ' ', text).strip())
                # A column of pure marks or lone labels carries no marking
                # point, and comparableScheme drops those lines anyway.
                if len(text) < 12 or text in seen:
                    continue
                seen.add(text)
                out.append(text)
    doc.close()
    return out


def pdf_for(subject: str, year: int, level: str) -> Path | None:
    """The marking-scheme PDF for exactly this subject, year and level.

    The explicitly-levelled name is preferred over the bare one, and a Deferred
    Examinations cover is refused outright. Both matter: examiner-reports holds
    biology/2023-marking-scheme.pdf, which is the DEFERRED Higher Level paper —
    a different exam with different answers — alongside the real 2023-hl one.
    Preferring the bare name appended the deferred paper's marking points to the
    main paper's scheme text, where they would let a card trace to wording the
    paper it cites never printed. That is the one thing the provenance gate
    exists to stop.
    """
    d = ROOT / 'examiner-reports' / subject
    names = ([f'{year}-{level}-marking-scheme.pdf'] if level == 'ol'
             else [f'{year}-hl-marking-scheme.pdf', f'{year}-marking-scheme.pdf'])
    for name in names:
        path = d / name
        if not path.exists():
            continue
        with pymupdf.open(path) as doc:
            cover = ' '.join(doc[0].get_text().split())
        if 'Deferred' in cover:
            continue
        want = 'Ordinary Level' if level == 'ol' else 'Higher Level'
        if want not in cover:
            continue
        return path
    return None


def apply(subject: str, year: int, level: str) -> None:
    md = ROOT / 'examiner-reports' / subject / 'schemes' / f'{year}-{level}.md'
    if not md.exists():
        raise SystemExit(f'no scheme markdown at {md}')
    pdf = pdf_for(subject, year, level)
    if pdf is None:
        raise SystemExit(f'no marking-scheme PDF for {subject} {year} {level}')
    lines = column_runs(pdf)
    body = f'{START}\n' + '\n'.join(lines) + f'\n{END}\n'
    text = md.read_text(encoding='utf-8')
    # Re-running replaces the block rather than stacking another, so this is
    # idempotent and the diff of a re-run shows only what actually changed.
    if START in text:
        text = re.sub(re.escape(START) + r'.*?' + re.escape(END) + r'\n?', '', text, flags=re.S)
    md.write_text(text.rstrip('\n') + '\n\n' + body, encoding='utf-8')
    print(f'{subject} {year} {level}: appended {len(lines)} column runs to {md.name}')


def main() -> None:
    if sys.argv[1:2] == ['--all']:
        for md in sorted((ROOT / 'examiner-reports').glob('*/schemes/*.md')):
            subject = md.parents[1].name
            year, level = md.stem.split('-')
            if pdf_for(subject, int(year), level) is None:
                print(f'{subject} {year} {level}: no PDF, skipped')
                continue
            apply(subject, int(year), level)
        return
    if len(sys.argv) < 4:
        raise SystemExit(__doc__.strip().splitlines()[2].strip())
    apply(sys.argv[1], int(sys.argv[2]), sys.argv[3])


if __name__ == '__main__':
    main()
