#!/usr/bin/env python3
"""
Mark Bank — clean extraction of SEC marking schemes.

The extractions already in the repo split words mid-token: "propagat ion",
"th at contains", "( i v )", "ammoni a", "p H". That damage lands directly in
shipped marking points, so a card either quotes the scheme wrongly or fails its
provenance check.

The cause is not the PDF being broken. SEC schemes are laid out as tables and a
single word is frequently rendered as SEVERAL text spans — kerning pairs, a
change of style, a column boundary. Naive extraction joins every span with a
space, which is right between words and wrong inside one.

This joins spans by MEASURING the horizontal gap between them and comparing it
to the width of a space in that span's own font, so a word split across spans is
put back together and genuine spacing survives.

    python3 scripts/markbank/extract-scheme.py <in.pdf> [-o out.md]
    python3 scripts/markbank/extract-scheme.py --check <file.md>
"""

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

try:
    import fitz  # PyMuPDF
except ImportError:
    fitz = None


def extract(pdf_path: Path, marks_column: bool = False,
            columns: bool = False) -> str:
    """Extract, rejoining split spans and reconstructing table rows.

    SEC schemes are tables: a marking point and the marks it earns sit in
    different cells of the SAME visual row. Emitting one cell per line separates
    an answer from its mark, so lines whose vertical centres agree are gathered
    back into one row, ordered left to right.
    """
    doc = fitz.open(pdf_path)
    out = []
    for pno, page in enumerate(doc, 1):
        out.append(f"\n## Page {pno}\n")
        marks_x = page.rect.width * MARKS_COLUMN_FRACTION if marks_column else None
        lines = []
        for block in doc[pno - 1].get_text("dict")["blocks"]:
            if block.get("type") != 0:
                continue
            for line in block["lines"]:
                text = join_spans(line["spans"])
                if not text.strip():
                    continue
                x0, y0, x1, y1 = line["bbox"]
                lines.append({"text": text, "x": x0, "x1": x1, "y": (y0 + y1) / 2, "h": y1 - y0})

        lines.sort(key=lambda l: (round(l["y"], 1), l["x"]))
        row, row_y, row_h = [], None, 10.0
        for line in lines:
            if row_y is not None and abs(line["y"] - row_y) > max(3.0, row_h * 0.6):
                out.append(render_row(row, marks_x))
                row = []
            if not row:
                row_y, row_h = line["y"], line["h"]
            row.append(line)
        if row:
            out.append(render_row(row, marks_x))
        if columns:
            out.extend(render_columns(lines))
    doc.close()
    return "\n".join(out)


# ------------------------------------------------------------- columns ----

# How far apart two pieces of text must be before they are different COLUMNS
# rather than the same line of prose. 60pt is about ten characters at this
# body size -- wider than any word space and narrower than the gutter between
# a scheme's answer column and whatever is printed beside it.
COLUMN_GAP = 60.0


def render_columns(lines):
    """The same page read DOWN its columns instead of across its rows.

    Reading across is right for keeping a marking point with its marks, and
    wrong for the prose itself whenever anything is printed beside it. The
    2021 Higher Engineering scheme answers "A single-acting cylinder is one
    where the thrust or output" at x72 and labels the diagram "Piston is
    pushed" at x495; on the same baseline, joined left to right, the label
    lands in the middle of the sentence and the sentence is not in the
    document any more. The build's provenance check compares against this
    file, so the true sentence is unfindable and the card is dropped -- 164
    Engineering asks, and the same shape costs every subject whose scheme
    prints callouts, mark cells or a second column beside its answers.

    Both readings are emitted. Neither is a correction of the other: they are
    the same text, and a claim is the SEC's own words if it is found in
    either.
    """
    if not lines:
        return []
    edges = sorted({round(l["x"]) for l in lines})
    bands, start = [], edges[0]
    for a, b in zip(edges, edges[1:]):
        if b - a > COLUMN_GAP:
            bands.append((start, a))
            start = b
    bands.append((start, edges[-1]))
    if len(bands) < 2:
        return []
    out = ["", "<!-- columns -->"]
    for left, right in bands:
        col = [l for l in lines if left - 1 <= round(l["x"]) <= right + 1]
        if not col:
            continue
        col.sort(key=lambda l: (round(l["y"], 1), l["x"]))
        out.append(" ".join(l["text"].strip() for l in col))
    return out


# ------------------------------------------------------------ marks column ----

# Where the marks column ends, as a fraction of page width — measured on the cell's
# RIGHT edge, not its left.
#
# The marks column is right-aligned against the table border; the prose beside it
# is ragged-right. So left edges overlap and right edges do not. Across the SEC
# Business schemes, marks cells END at 490-542 of a 595pt page while the widest
# prose ends by 460. A left-edge rule set between them cut the column in half: on
# the 2025 Higher paper it lifted "17" at x0=511 and fused "3+3" at 469 and
# "2@(3+2)" at 457 into the middle of the sentences they were printed against.
MARKS_COLUMN_FRACTION = 0.79

# What a marks cell can say: "8", "(4+4)", "15m", "2@5m(3+2)", "3, 2, 2, 2, 1".
# Digits, the operators the SEC combines them with, and nothing else.
MARK_CELL = re.compile(r"^[\s\d@+×x*.,;:()\[\]/m-]*\d[\s\d@+×x*.,;:()\[\]/m-]*$", re.I)

# A thousands separator: groups of exactly three digits after a comma.
#
# An accounts table's TOTAL column is right-aligned to the same edge as the marks
# column, so "Total Receipts (A) 115,000 110,000 120,000 345,000" would have its
# answer lifted out as though it were a tariff. Marks never carry a thousands
# separator — the SEC's own comma notation is "3,2,2,2,1", groups of one digit —
# so the shape of the number settles it without needing to know the column.
MONEY = re.compile(r"\d,\d{3}(\D|$)")


def is_mark(text: str) -> bool:
    """Whether a cell states marks rather than an answer that happens to be numeric."""
    return bool(MARK_CELL.fullmatch(text)) and not MONEY.search(text)


def render_row(row, marks_x=None) -> str:
    """One table row: cells left to right, separated so a mark stays with its
    marking point but is still distinguishable from it.

    With `marks_x` set, a trailing cell from the marks column is emitted inside
    ⟨angle brackets⟩ rather than run into the prose. This matters more than it
    looks. A marking point that wraps onto two lines has the marks cell of the
    FIRST line dropped into the middle of its own sentence:

        A takeover involves one company buying out at least 8
        51% of another company's shares. It can be friendly (4+4)

    An author reading that cannot quote the sentence — the build's provenance
    check compares against this file, so the true sentence is not findable and
    the card is dropped. Ten Business papers' worth of agents worked around it by
    inventing dashes mid-sentence or truncating the point, which is exactly the
    damage the check exists to prevent. Bracketing the cell keeps the prose
    continuous AND keeps the mark on the line it was printed against, so which
    answer earns which mark stays readable.
    """
    cells = [c for c in sorted(row, key=lambda c: c["x"]) if c["text"].strip()]
    if marks_x is None:
        return " ".join(c["text"].strip() for c in cells)
    marks, body = [], []
    for i, c in enumerate(cells):
        text = c["text"].strip()
        trailing = i == len(cells) - 1 or all(
            d["x1"] >= marks_x and is_mark(d["text"].strip()) for d in cells[i + 1:]
        )
        if c["x1"] >= marks_x and trailing and is_mark(text):
            marks.append(text)
        else:
            body.append(text)
    line = " ".join(body)
    if marks:
        line = (line + " " if line else "") + " ".join(f"⟨{m}⟩" for m in marks)
    return line



# ------------------------------------------------------------- ligatures ----

# Some SEC PDFs embed a subsetted font whose LIGATURE glyphs carry no sensible
# Unicode mapping, so the extractor faithfully reports the wrong codepoint. The
# 2024 Chemistry Ordinary scheme came out with 213 instances of "Ɵ" standing for
# "ti" — "unsaturaƟon", "addiƟon reacƟon", "separaƟon" — plus 73 f-ligatures.
#
# This costs far more than legibility. The authoring agents READ these files, and
# a diligent one silently corrects "reacƟon" to "reaction" in its head; the card
# is then right and the provenance check, which compares against the corrupted
# source, throws it away. That one file was losing 43% of its cards while every
# other paper lost under 17%.
from markbank_text import LIGATURES, unligature  # noqa: E402  (shared with describe-tables.py)
_ = LIGATURES


def join_spans(spans) -> str:
    """Join spans, inserting a space only where the geometry shows one."""
    parts = []
    prev = None
    for span in spans:
        text = span["text"]
        if not text:
            continue
        if prev is not None:
            gap = span["bbox"][0] - prev["bbox"][2]
            # A space in this font is roughly 0.25em. Anything at or below about
            # a third of that is kerning inside a word, not a word break.
            space_w = max(1.0, span["size"] * 0.25)
            joined_touching = gap < space_w * 0.38
            ends_open = prev["text"].endswith(" ")
            starts_open = text.startswith(" ")
            if joined_touching and not ends_open and not starts_open:
                parts.append(text)
                prev = span
                continue
        parts.append((" " if parts and not parts[-1].endswith(" ") and not text.startswith(" ") else "") + text)
        prev = span
    return unligature(re.sub(r"[ \t]+", " ", "".join(parts)).rstrip())


# ---------------------------------------------------------------- quality ----

# Words that legitimately contain a space-looking split or are domain terms the
# checker would otherwise flag. Kept deliberately short.
ALLOW = {
    "sec", "hl", "ol", "dna", "rna", "atp", "adp", "nad", "nadp", "ph",
    "srp", "aac", "lc", "mrna", "trna", "co", "o", "h", "n", "c",
}

SPLIT_RE = re.compile(r"\b([a-z]{2,})\s+([a-z]{1,4})\b")


def load_dictionary() -> set:
    for path in ("/usr/share/dict/words", "/usr/dict/words"):
        p = Path(path)
        if p.exists():
            return {w.strip().lower() for w in p.read_text(errors="ignore").splitlines() if w.strip()}
    return set()


def check(text: str, words: set) -> list:
    """Find likely intra-word splits: 'propagat ion' where 'propagation' is a word
    but 'propagat' is not."""
    if not words:
        return []
    hits = []
    for m in SPLIT_RE.finditer(text.lower()):
        a, b = m.group(1), m.group(2)
        if a in ALLOW or b in ALLOW:
            continue
        if a in words:
            continue  # first part is a real word, so this is normal spacing
        if (a + b) in words:
            hits.append(f"{a} {b}  ->  {a}{b}")
    return hits


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("path", type=Path)
    ap.add_argument("-o", "--out", type=Path)
    ap.add_argument("--check", action="store_true", help="report likely splits in an existing .md")
    ap.add_argument("--marks-column", action="store_true",
                    help="lift the right-hand marks cells out of the prose into ⟨brackets⟩")
    ap.add_argument("--columns", action="store_true",
                    help="also read each page DOWN its columns, for prose that "
                         "has something printed beside it")
    args = ap.parse_args()

    words = load_dictionary()

    if args.check:
        text = args.path.read_text()
        hits = check(text, words)
        print(f"{args.path.name}: {len(hits)} suspected intra-word splits")
        for h in sorted(set(hits))[:40]:
            print("   ", h)
        return 0

    if fitz is None:
        print("PyMuPDF is required to extract", file=sys.stderr)
        return 1

    text = extract(args.path, marks_column=args.marks_column,
                   columns=args.columns)
    hits = check(text, words)
    out = args.out or args.path.with_suffix(".md")
    out.write_text(text)
    print(f"{args.path.name} -> {out}  ({len(text):,} chars, {len(set(hits))} suspected splits)")
    for h in sorted(set(hits))[:12]:
        print("   ", h)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
