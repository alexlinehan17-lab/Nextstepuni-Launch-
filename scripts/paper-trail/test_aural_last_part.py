#!/usr/bin/env python3
"""
Fixtures for aural_papers.py's LAST_PART_TO_KEY_END: a keyed booklet's last
part runs to the end of the scheme's listening key, which is the page before
the first later page heading an appendix (APPENDIX / AGUISÍN) in its top third
or carrying a transcript. Run: python3 test_aural_last_part.py (exits non-zero
on failure). Needs the local paper-trail-corpus for the keyed booklets.
"""

import os
import sys

import fitz

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import aural_papers as A  # noqa: E402


def test_no_end_marker_raises():
    """A scheme with no appendix and no transcript after the last part is
    refused: the generator never runs a part on to the scheme's last page."""
    doc = fitz.open()
    for text in ("Part A answers", "Part E answers", "more Part E answers", "Notes"):
        page = doc.new_page()
        page.insert_text((72, 72), text)
    try:
        A._key_end(doc, 2, 0.05)
    except ValueError as e:
        assert "cannot be read" in str(e), e
    else:
        raise AssertionError("a scheme with no end marker was not refused")


def test_appendix_opening_a_page_ends_the_page_before():
    doc = fitz.open()
    for text in ("Part E answers", "more Part E answers", "APPENDIX 1"):
        page = doc.new_page()
        page.insert_text((72, 72), text)
    assert A._key_end(doc, 1, 0.05) == (2, 1.0)


def test_appendix_under_the_last_answers_ends_at_its_heading():
    """Polish 2026 Higher p16: the appendix heading follows the last answer
    on the same page, so the key ends at the heading's own height."""
    doc = fitz.open()
    doc.new_page().insert_text((72, 72), "Part E answers")
    page = doc.new_page()
    page.insert_text((72, 72), "more Part E answers")
    page.insert_text((72, 400), "APPENDIX 1")
    pg, y = A._key_end(doc, 1, 0.05)
    assert pg == 2 and 0.3 < y < 0.6, (pg, y)


def test_keyed_booklets_end_where_the_key_ends():
    """Each keyed booklet's last part runs past its first page and stops at
    the appendix: mid-page at the heading, or at the foot of the page before
    a page the appendix (or a transcript) opens."""
    for key in sorted(A.LAST_PART_TO_KEY_END):
        year, fid = key.split("/")
        pp = os.path.join(A.CORPUS, "exampapers", year, fid)
        lang = fid[-6:-4]
        sp = os.path.join(A.CORPUS, "markingschemes", year,
                          f"{fid[:6]}LP000{'EV' if lang == 'BV' else lang}.pdf")
        sc, err = A.build_sidecar(pp, sp)
        assert err is None, (key, err)
        last = sc["q"][-1]["region"]
        assert len(last) >= 2, (key, "last part not extended past its first page", last)
        end, bottom = last[-1]["p"], last[-1]["r"][3]
        scheme = fitz.open(sp)
        if bottom < 1.0:
            heads = [y for t, _x, y in A.lines_with_pos(scheme[end - 1]) if A.KEY_END.match(t)]
            assert any(abs(y - bottom) < 0.002 for y in heads), (key, end, bottom, heads)
        else:
            nxt = scheme[end]
            opens = [t for t, _x, _y in A.lines_with_pos(nxt)][:3]
            assert any(A.KEY_END.match(t) for t in opens) or A.TRANSCRIPT.search(nxt.get_text()), (key, end, opens)


if __name__ == "__main__":
    fails = 0
    for name, fn in list(globals().items()):
        if name.startswith("test_") and callable(fn):
            try:
                fn()
                print(f"ok   {name}")
            except AssertionError as e:
                fails += 1
                print(f"FAIL {name}: {e}")
    sys.exit(1 if fails else 0)
