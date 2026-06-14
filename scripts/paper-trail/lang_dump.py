#!/usr/bin/env python3
"""Surface anchor candidates for authoring a language reading spec.

Dumps, for a paper+scheme pair: every left-margin numbered line and every
section header (TEXT/Léamh/Cluas/SECTION/aural/reading keywords), with the EXACT
line text (so it can be copied verbatim as a find_y anchor) and its page. The
agent reads this + the PDFs, decides which lines are READING-comprehension
questions (not aural, not composition), and pairs each to its scheme answer
block.

Usage: python3 lang_dump.py <year> <paperFileid> <schemeFileid>
"""
import sys, os, re
import fitz

HERE = os.path.dirname(os.path.abspath(__file__))
CORPUS = os.path.join(os.path.dirname(os.path.dirname(HERE)), "paper-trail-corpus")
LIG = {"Ɵ": "ti", "Ʃ": "tt", "ϐ": "fi", "ﬀ": "ff", "ﬁ": "fi", "ﬂ": "fl",
       "ﬃ": "ffi", "ﬄ": "ffl", "ﬅ": "ft", "ﬆ": "st"}
SECTION_KW = ["TEXT", "Text", "Léamh", "LÉAMH", "Cluas", "CLUAS", "SECTION", "Section",
              "Triail", "Roinn", "ROINN", "WRITTEN", "Written", "Reading", "Listening",
              "Leseverständnis", "LESEVER", "Comprehension", "Comprensión", "Compréhension",
              "Aural", "AURAL", "ESCRITA", "ORALE", "SCRITTA", "Schriftlich", "Hörverstehen",
              "Sección", "Section", "Opgave", "Partie", "Parte", "Cuid", "Léirthuiscint",
              "Léamhthuiscint", "Scríbhneoireacht", "Ceapadóireacht"]


def delig(s):
    for k, v in LIG.items():
        if k in s:
            s = s.replace(k, v)
    return s


def dump(path, label):
    d = fitz.open(path)
    print(f"\n===== {label}: {os.path.basename(path)} ({len(d)} pages) =====")
    for pi, pg in enumerate(d):
        H = pg.rect.height
        rows = []
        for b in pg.get_text("dict")["blocks"]:
            for ln in b.get("lines", []):
                txt = delig("".join(s["text"] for s in ln["spans"]).strip())
                x0, y0 = ln["bbox"][0], ln["bbox"][1]
                is_num = re.match(r"^\d{1,2}[.\)]", txt) and x0 < 150
                is_sec = any(k in txt for k in SECTION_KW) and len(txt) < 70
                if is_num or is_sec:
                    tag = "Q" if is_num else "§"
                    rows.append(f"   p{pi+1} y{y0/H:.2f} x{x0:.0f} [{tag}] {txt[:72]}")
        if rows:
            print("\n".join(rows))
    d.close()


def main():
    year, pf, sf = sys.argv[1], sys.argv[2], sys.argv[3]
    dump(os.path.join(CORPUS, "exampapers", year, pf), "PAPER")
    dump(os.path.join(CORPUS, "markingschemes", year, sf), "SCHEME")


if __name__ == "__main__":
    main()
