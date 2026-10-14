"""
Mark Bank — repair mangled glyphs by GLYPH ID, not by the character the PDF reports.

Word embeds subset fonts whose ToUnicode map assigns arbitrary code points to
ligatures and symbols. The same code point means different things in different
PDFs: U+01A9 is the "tt" ligature in a Business scheme ("leƩers") but stood for
"t" in a Maths scheme, and U+01AB is "tti" in Business ("seƫng" = setting) where
the shared character map says "tt" -- so a character-keyed repair silently turns
"putting" into "puttng". What identifies a glyph is the font and its glyph id,
which PyMuPDF exposes through get_texttrace().

Two kinds of key, because two kinds of font reach the text layer:

* CID TrueType text fonts (Calibri and its styles) keep the original font's glyph
  ids in every subset, so ``Calibri|427`` is the same glyph in every PDF. These
  entries are DERIVED by scripts/markbank/authoring/derive_glyph_ids.py from the
  sightings where the same id carries a sane ToUnicode, or settled by cropping
  the glyph out of the page and looking at it when no sane sighting exists.
* Symbol fonts (Wingdings, Wingdings 2, Symbol) are simple fonts: their private
  use code point is 0xF000 + the font's own character code, which names the
  glyph, while their subset glyph ids are renumbered per PDF. These are keyed by
  family and code point, each settled by cropping the glyph and looking at it.

Anything the table cannot resolve is left in place so the gates refuse it.
"""
import json
import re
from pathlib import Path

TABLE_PATH = Path(__file__).resolve().parent / "authoring" / "glyph_ids.json"

# Code points a broken subset font leaves in the text layer: Latin Extended,
# IPA, combining marks, Greek and Cyrillic through Ethiopic and the other blocks
# a subset borrows, private use, alphabetic presentation forms (the ligatures)
# and the replacement character. Greek is included: a Business scheme prints no
# Greek, and its text layer spells "Certificate" with U+03D0 and a dash as
# U+0374. A genuine Greek letter elsewhere has no entry in the table, so
# repair_char leaves it alone; only a gate has to know which subject is which.
MANGLED = re.compile(r"[\u0100-\u1FFF\uE000-\uF8FF\uFB00-\uFB4F\uFFFD]")


def family(font: str) -> str:
    """The font whose glyph order an id indexes.

    'ABCDEF+Calibri,Bold' and 'Calibri-Bold2' -> 'Calibri': Word's Calibri
    styles and the numbered duplicates MuPDF gives repeated subsets share one
    glyph order (gid 415 reads "ti" and 302 "fi" in regular, bold and italic
    alike). Calibri Light is a different font and keeps its own name, as does
    Wingdings 2. 'Wingdings-Regular' -> 'Wingdings'.
    """
    name = re.sub(r"^[A-Z]{6}\+", "", font or "")
    if name.startswith("Calibri"):
        name = re.sub(r"\d+$", "", name)
    base, _, style = name.replace(",", "-").partition("-")
    return base + "-Light" if style.startswith("Light") else base


def load_table(path: Path = TABLE_PATH) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    by_gid = {f'{e["font"]}|{e["gid"]}': e["text"] for e in data["byGlyphId"]}
    by_code = {f'{e["font"]}|{e["code"]}': e["text"] for e in data["byCodePoint"]}
    return {"gid": by_gid, "code": by_code}


def page_glyphs(page) -> dict:
    """Drawing origin -> (family, glyph id) for every glyph drawn on the page."""
    origin = {}
    for sp in page.get_texttrace():
        fam = family(sp.get("font", ""))
        for ch in sp["chars"]:
            if ch[1] >= 0:
                origin[(round(ch[2][0], 2), round(ch[2][1], 2))] = (fam, ch[1])
    return origin


def repair_char(ch: dict, origin: dict, table: dict) -> str:
    """The text a rawdict character really stands for, or the character itself."""
    c = ch["c"]
    if not MANGLED.match(c):
        return c
    hit = origin.get((round(ch["origin"][0], 2), round(ch["origin"][1], 2)))
    if hit:
        fam, gid = hit
        text = table["gid"].get(f"{fam}|{gid}")
        if text is not None:
            return text
        text = table["code"].get(f"{fam}|{ord(c):04X}")
        if text is not None:
            return text
    return c


def document_map(doc, table: dict) -> tuple:
    """Per-document character -> repair, read off the glyph ids.

    Within one PDF a mangled code point is one glyph, so the map is a function;
    a code point that resolves two ways here is refused rather than guessed.
    Returns (map, unresolved code points, ambiguous code points).
    """
    seen, unresolved = {}, set()
    for page in doc:
        origin = page_glyphs(page)
        for blk in page.get_text("rawdict")["blocks"]:
            for line in blk.get("lines", []):
                for sp in line.get("spans", []):
                    for ch in sp["chars"]:
                        if not MANGLED.match(ch["c"]):
                            continue
                        text = repair_char(ch, origin, table)
                        if text == ch["c"]:
                            unresolved.add(ch["c"])
                        else:
                            seen.setdefault(ch["c"], set()).add(text)
    ambiguous = {c for c, v in seen.items() if len(v) > 1}
    return {c: next(iter(v)) for c, v in seen.items() if len(v) == 1}, unresolved, ambiguous


# ------------------------------------------------------------ misread words ----
#
# A ligature glyph can be misread two ways, and only one of them leaves a
# mangled character behind. Calibri's "tt" (gid 425) reaches some text layers as
# U+01A9 and others as a plain "t": the 2023 OL Latin scheme's text says "batle"
# where the page prints "battle". A plain "t" is not a mangled character, so a
# character gate cannot see it; only the glyph id can. These read each glyph that
# the table knows to be a ligature, compare what the text layer reported for it
# with what the glyph is, and turn every disagreement into a whole-word repair
# for that one document.

WORD_EDGE = re.compile(r"^[\W_]*(.*?)[\W_]*$", re.S)


def ligature_ids(table: dict) -> dict:
    """Glyph-id entries that stand for more than one letter: "tt", "tti", "fi"..."""
    return {k: v for k, v in table["gid"].items() if len(v) > 1 and v.replace("í", "i").isalpha()}


def _glyph_lengths(page) -> dict:
    """Drawing origin -> (family, glyph id, characters its ToUnicode reports).

    MuPDF reports a glyph whose ToUnicode is several characters as the glyph
    followed by id -1 continuations at the same origin in the trace, but as
    separate characters at advancing origins in rawdict ("ti" arrives as a "t"
    and an "i"), so the trace says how many rawdict characters each glyph owns.
    """
    out = {}
    for sp in page.get_texttrace():
        fam = family(sp.get("font", ""))
        chars = sp["chars"]
        i = 0
        while i < len(chars):
            gid, org = chars[i][1], chars[i][2]
            j = i + 1
            while (j < len(chars) and chars[j][1] == -1 and abs(chars[j][2][0] - org[0]) < 0.01
                   and abs(chars[j][2][1] - org[1]) < 0.01):
                j += 1
            if gid >= 0:
                out[(round(org[0], 2), round(org[1], 2))] = (fam, gid, j - i)
            i = j
    return out


def _glyph_groups(page, lengths):
    """Per text line: [(reported text, (family, gid) or None), ...] in reading order."""
    for blk in page.get_text("rawdict")["blocks"]:
        for line in blk.get("lines", []):
            chars = [ch for sp in line.get("spans", []) for ch in sp["chars"]]
            groups, i = [], 0
            while i < len(chars):
                ch = chars[i]
                hit = lengths.get((round(ch["origin"][0], 2), round(ch["origin"][1], 2)))
                n = hit[2] if hit else 1
                groups.append(("".join(c["c"] for c in chars[i:i + n]), hit[:2] if hit else None))
                i += n
            yield groups


def document_words(doc, table: dict, variants: tuple = ()) -> tuple:
    """Per document: {misread word: printed word}, the misread forms refused,
    and the words the document's text layer reads correctly.

    `variants` are character maps an older pipeline already applied to the
    mangled characters (the shared glyphmap turned U+01A9 into "t"), so text
    that went through one of them is recognised too. A misread form that the
    same document also prints as a correctly read word is refused, never
    guessed: replacing it there would change a word that is right.
    """
    lig = ligature_ids(table)
    words, clean = {}, set()
    for page in doc:
        lengths = _glyph_lengths(page)
        for groups in _glyph_groups(page, lengths):
            rep, cor = [], []
            for text, hit in groups:
                # Only ligature glyphs are re-read here. A Greek or maths symbol
                # that a broken map also reports oddly is real text in a science
                # paper, and is not this function's business.
                fixed = text
                if hit:
                    true = lig.get(f"{hit[0]}|{hit[1]}")
                    if true is not None and text != true:
                        fixed = true
                rep.append(text)
                cor.append(fixed)
            r_tokens, c_tokens = "".join(rep).split(), "".join(cor).split()
            if len(r_tokens) != len(c_tokens):
                continue
            for r, c in zip(r_tokens, c_tokens):
                rw, cw = WORD_EDGE.match(r).group(1), WORD_EDGE.match(c).group(1)
                if r == c:
                    clean.add(rw)
                    continue
                # A word the repair cannot make whole (a control-character
                # encoding, an unresolved glyph) is left for the gates.
                if not cw.isprintable() or MANGLED.search(cw) or not rw.isprintable():
                    continue
                forms = {rw}
                for v in variants:
                    forms.add("".join(v.get(ch, ch) for ch in rw))
                for form in forms:
                    if form != cw:
                        words.setdefault(form, set()).add(cw)
    refused = {w for w, rights in words.items() if len(rights) > 1 or w in clean}
    return {w: next(iter(r)) for w, r in words.items() if w not in refused}, refused, clean


def apply_words(text: str, words: dict) -> tuple:
    """Whole-word replacement; returns (text, {misread: count})."""
    counts = {}
    for wrong in sorted(words, key=len, reverse=True):
        pattern = re.compile(r"(?<![\w])" + re.escape(wrong) + r"(?![\w])")
        text, n = pattern.subn(words[wrong], text)
        if n:
            counts[wrong] = n
    return text, counts
