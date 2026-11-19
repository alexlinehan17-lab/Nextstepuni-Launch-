#!/usr/bin/env python3
# Copyright 2026 Nextstepuni
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
Paper Trail — language AURAL papers (Listening Comprehension Tests).

Ten Leaving Cert languages sit a separate listening booklet (fileid *LPA00*)
whose answers are printed in the MAIN marking scheme's listening section, and
none of the ~380 such papers had a single answer chip. Both sides are plain
numbered runs (paper: "Question 1"… or "1."…; scheme: "1."… under a LISTENING
COMPREHENSION / CLUASTUISCINT header), so one generator covers every language.

The one real hazard is section choice, and it is the same hazard Irish Paper
One hit in the first campaign: schemes print the TAPESCRIPT — which numbers
its texts exactly like the answer key numbers its answers — and some print
reading-section answers under the same 1..N numbering earlier in the document.
Anchoring on the first thing that looks right chips the transcript. So this
generator enumerates EVERY candidate section start (each page matching a
listening header, in any of the corpus's languages) and keeps the LAST
candidate whose following numbered run exactly reconciles with the paper's own
question count, monotonic, no gaps. No candidate reconciles -> the paper is
DROPPED, never guessed.

Aural components come in three language editions: BV (bilingual booklet,
paired with the EV scheme), and EV/IV twins (the IV scheme is the Irish
translation, headed CLUASTUISCINT with C.n / Ceist markers).

Usage:
  python3 aural_papers.py                      # every language, every year
  python3 aural_papers.py --subject spanish
  python3 aural_papers.py --dry-run
"""
import argparse
import json
import os
import re
import sys

import fitz  # pymupdf

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
CORPUS = os.path.join(REPO, "paper-trail-corpus")
ANSWERS_DIR = os.path.join(HERE, "answers")

YEARS = range(2010, 2027)
COPYRIGHT = "© State Examinations Commission"

SUBJECT_CODES = {
    "spanish": "LC012", "french": "LC010", "german": "LC011",
    "italian": "LC013", "japanese": "LC058", "russian": "LC099",
    "polish": "LC548", "portuguese": "LC018", "lithuanian": "LC550",
    "mandarin-chinese": "LC566",
    # Irish (LC001) is deliberately ABSENT: its 2010-2011 aural schemes print
    # only a mark-allocation grid and the tapescript — no stated answers exist
    # to chip, so a reconciling map would send a student to a tariff table.
    # Verified against the HL, OL and FL schemes; the modern Irish aural lives
    # inside Paper One and is chipped by irish_p1.py.
}

# Listening-section headers across the corpus's scheme languages. EV schemes
# head the section in English; IV schemes in Irish; a few older ones use the
# target language's own word for it.
LISTEN = re.compile(
    r"LISTENING\s+COMPREHENSION|AURAL\s+EXAM|CLUASTUISCINT|"
    r"COMPR[ÉE]HENSION\s+ORALE|H[ÖO]RVERST[ÄA]NDNIS|"
    r"COMPRENSI[ÓO]N\s+AUDITIVA|ASCOLTO", re.I)
# A tapescript page is a hard boundary: answers never follow the transcript.
TRANSCRIPT = re.compile(r"TRANSCRIPT|TAPESCRIPT|SCRIPT\s+OF|TÉACS(?:ANNA)?\s+CLUAS", re.I)

# Question heads. Worded forms win over bare numbers wherever both appear.
Q_WORD = re.compile(r"^(?:Question|QUESTION|Ceist|CEIST|C\.)\s*(\d{1,2})\b")
Q_BARE = re.compile(r"^(\d{1,2})\.(?:\s|$)")
# Part headings, for booklets that number PARTS rather than questions
# (Portuguese "Parte A", Russian BV "ROINN II", old Russian EV "Segment 1" /
# "Mír 1"). The part WORD differs between a paper and its scheme — the 2016
# Russian paper says Segment where its scheme says Section — so parts are
# matched by ORDINAL (A=1, II=2, 3=3), never by the word.
PART_RX = re.compile(
    r"^(?:Parte|PARTE|Parts?|PARTS?|Roinn|ROINN|Section|SECTION|Cuid|CUID|Segment|SEGMENT|"
    r"M[íi]r|MÍR|P[áa]irt|Cz[ęe][śs][ćc]|CZ[ĘE][ŚS][ĆC]|Часть)\s*([A-Z]\b|[IVXivx]+\b|\d{1,2}\b)")
# "First Part: Interview" — the 2012-era German scheme and paper both head
# their listening parts with ordinal WORDS.
PART_WORD_RX = re.compile(
    r"^(First|Second|Third|Fourth|Fifth|Sixth|Erster|Zweiter|"
    r"Dritter|Vierter|F[üu]nfter)\s+(?:Part|Teil)\b"
    r"|^(?:Cuid|Chuid|Roinn|Teil)\s+(?:a\s+)?"
    r"(hAon|D[óo]|Tr[íi]|Ceathair|C[úu]ig|S[ée]|Eins|Zwei|Drei|Vier|F[üu]nf)\b"
    r"|^An\s+(Ch[ée]ad|Dara|Tr[íi][úu]|Ceathr[úu]|C[úu]igi[úu]|S[ée][úu])\s+Ch?uid\b",
    re.I)
WORD_ORD = {"first": 1, "second": 2, "third": 3, "fourth": 4, "fifth": 5,
            "sixth": 6, "erster": 1, "zweiter": 2, "dritter": 3, "vierter": 4,
            "fünfter": 5, "funfter": 5,
            "haon": 1, "dó": 2, "do": 2, "trí": 3, "tri": 3, "ceathair": 4,
            "cúig": 5, "cuig": 5, "sé": 6, "se": 6,
            "eins": 1, "zwei": 2, "drei": 3, "vier": 4, "fünf": 5, "funf": 5,
            "chéad": 1, "chead": 1, "dara": 2, "tríú": 3, "triu": 3,
            "ceathrú": 4, "ceathru": 4, "cúigiú": 5, "cuigiu": 5,
            "séú": 6, "seu": 6}
ROMAN = {"i": 1, "ii": 2, "iii": 3, "iv": 4, "v": 5, "vi": 6, "vii": 7,
         "viii": 8, "ix": 9, "x": 10}


def _part_word(txt):
    """The heading's own word, normalised — ROINN and Section count as distinct
    runs on one side, but the ordinal is what pairs them ACROSS sides."""
    if PART_WORD_RX.match(txt):
        return "ordword"
    return txt.split()[0].rstrip(":.").lower()


def _part_match(txt):
    """(ordinal, matched) for either part-heading form, else (None, False)."""
    m = PART_RX.match(txt)
    if m:
        return _ordinal(m.group(1)), True
    m = PART_WORD_RX.match(txt)
    if m:
        tok = (m.group(1) or m.group(2) or m.group(3)).lower().replace("ü", "u")
        return WORD_ORD.get(tok), True
    return None, False


def _ordinal(tok):
    t = tok.strip().lower()
    if t.isdigit():
        return int(t)
    if t in ROMAN:
        return ROMAN[t]
    if len(t) == 1 and t.isalpha():
        return ord(t) - ord("a") + 1
    return None


def lines_with_pos(page):
    W, H = page.rect.width, page.rect.height
    rows = {}
    for w in page.get_text("words"):
        rows.setdefault((w[5], w[6]), []).append(w)
    out = []
    for key in rows:
        ws = sorted(rows[key], key=lambda w: w[0])
        out.append((" ".join(w[4] for w in ws).strip(),
                    ws[0][0] / W, min(w[1] for w in ws) / H))
    out.sort(key=lambda t: (t[2], t[1]))
    return out


# Booklets whose PARTS are the answer map's units though the question run
# looks longer, keyed by year/fileid. The Portuguese listening booklets of
# 2022 Ordinary, 2023 and 2024 restart their question numbers in every Parte,
# and a later Parte prints more questions than the first, so the run "1..N"
# splices one Parte's numbers onto another's and wins over the five Partes:
# 2024 (and 2022 OL IV, 2023 HL IV) then read their answers off the scheme's
# READING pages; 2022 OL EV and 2023 EV/IV OL mapped "questions" 6-8 onto
# later Partes. Every other Portuguese map (2022 HL, 2025, 2026) already
# numbers the Partes. A general restart test would move maps of other
# languages too (Japanese, Polish, Russian), so the override names the
# papers. EV and IV twins alike. The Polish 2026 Ordinary booklet does the
# same with its five Części (A 1-5, C 1-6, E 1-7): the run "1..7" read A1-5,
# C6 and E7; the EV map's scheme run then started on the READING pages (p7),
# and the IV map's entry "6" ran from Część C Q6 to Część E Q6.
FORCE_PARTS = {"2026/LC548GLPA00EV.pdf", "2026/LC548GLPA00IV.pdf",
               "2022/LC018GLPA00EV.pdf", "2022/LC018GLPA00IV.pdf",
               "2023/LC018ALPA00EV.pdf", "2023/LC018ALPA00IV.pdf",
               "2023/LC018GLPA00EV.pdf", "2023/LC018GLPA00IV.pdf",
               "2024/LC018ALPA00EV.pdf", "2024/LC018ALPA00IV.pdf",
               "2024/LC018GLPA00EV.pdf", "2024/LC018GLPA00IV.pdf"}


def paper_questions(doc, force_parts=False):
    """{n: (page1, y)} — the longest ascending 1..N run of question heads.

    The booklet's cover counts its own questions ("There are seven questions in
    this paper"), so heads only count from page 2 on, at the left half of the
    page, ascending with no gaps. Worded heads are collected separately from
    bare "N." heads and the longer run wins — mixing them lets an instruction
    list ("1. Answer all questions.") splice into a worded run.
    """
    runs = {"word": {}, "bare": {}}
    want = {"word": 1, "bare": 1}
    # Part runs are kept PER PART-WORD: a Russian booklet heads its sections
    # ROINN I..IV and each section's audio pieces Mír 1..3 — one shared counter
    # spliced them into "ROINN I, Mír 2, Mír 3, ROINN IV". The longest
    # word-consistent run wins.
    parts, pwant = {}, {}
    for pi in range(1, len(doc)):
        for txt, x, y in lines_with_pos(doc[pi]):
            # Part headings float free of the margin — German 2012 right-aligns
            # "First Part" at x=0.70 — so they get a wide gate; question heads
            # keep the tight one.
            if x > 0.85:
                continue
            if x <= 0.55:
                for kind, rx in (("word", Q_WORD), ("bare", Q_BARE)):
                    m = rx.match(txt)
                    if m and int(m.group(1)) == want[kind]:
                        runs[kind][want[kind]] = (pi + 1, y)
                        want[kind] += 1
            ordn, hit = _part_match(txt)
            if hit and ordn is not None:
                word = _part_word(txt)
                pwant.setdefault(word, 1)
                if ordn == pwant[word]:
                    parts.setdefault(word, {})[pwant[word]] = (pi + 1, y, txt[:24].strip())
                    pwant[word] += 1
    best = max(runs.values(), key=len)
    prun = max(parts.values(), key=len) if parts else {}
    # A part run speaks when the booklet numbers no questions — OR when its
    # question numbering RESTARTS: German 2012 heads four parts and numbers
    # each part's questions from 1, so the 4-long question run is really the
    # first part's internals. A fresh "1." on or after part 2's first page is
    # the restart signature.
    if len(prun) >= 2:
        p2pg, p2y, _ = prun[2]
        # The question run is part 1's INTERNALS — not the booklet's global
        # numbering — exactly when every head it found sits before part 2
        # begins. Polish numbers its questions straight through the parts, so
        # its runs extend past part 2 and keep question mode.
        confined = best and all(
            pg < p2pg or (pg == p2pg and y < p2y) for pg, y in best.values())
        if len(prun) > len(best) or confined or force_parts:
            return {n: (pg, y) for n, (pg, y, _) in prun.items()}, \
                {n: lab for n, (_, _, lab) in prun.items()}
    return best, None


STOP_WORDS = {"the", "and", "that", "with", "this", "from", "have", "what",
              "give", "details", "full", "marks", "question", "level",
              "agus", "chun", "seo", "sin", "leis", "bhfuil",
              # Exam furniture appears on every page of both documents, so it
              # can carry a WRONG section past a right one whose answers are
              # terse (the Italian 2016 key lost to the reading section 15-13
              # on words like these).
              "questions", "answer", "answers", "answered", "section",
              "english", "write", "written", "candidates", "candidate",
              "spaces", "provided", "booklet", "examination", "certificate",
              "leaving", "ordinary", "higher", "each", "will", "hear",
              "there", "three", "times", "then", "right", "through",
              "played", "pause", "pauses", "segment", "segments",
              "freagair", "freagra", "freagraí", "scríobh", "ceisteanna",
              "cluastuisceana", "hardteistiméireachta", "scrúdú"}


def _harvest_words(doc, pages=None):
    out = set()
    rng = pages if pages is not None else range(1, len(doc))
    for pi in rng:
        if pi >= len(doc):
            continue
        for w in doc[pi].get_text("words"):
            t = re.sub(r"\W+", "", w[4]).lower()
            if len(t) >= 4 and t not in STOP_WORDS:
                out.add(t)
    return out


def scheme_blocks(doc, want_n, paper_words, parts_mode=False):
    """{n: (page1, y0)} for the listening answer key, or None.

    A candidate section start is any page matching a listening header — OR any
    page where a fresh "1." run begins, because the 2016-2019 Spanish schemes
    open their aural answers with no header at all, straight into "1. Anuncio".
    Each candidate must yield an ascending 1..want_n run before a transcript
    page. Among reconciling candidates the winner is the one whose block text
    shares the most words with the AURAL PAPER itself: the booklet prints the
    same titles the key answers ("FÚTBOL GAÉLICO EN MADRID"), while a reading
    section that happens to count to the same N shares almost nothing. This is
    also the answers-not-tapescript discriminator, made positive rather than
    positional.
    """
    cands = set(pi for pi in range(len(doc)) if LISTEN.search(doc[pi].get_text()))
    for pi in range(len(doc)):
        for txt, x, y in lines_with_pos(doc[pi]):
            if x > 0.4:
                continue
            if parts_mode:
                # Part headings are often centred (x≈0.45), unlike question
                # numbers which hug the margin.
                if x > 0.6:
                    continue
                ordn, hit = _part_match(txt)
                if hit and ordn == 1:
                    cands.add(pi)
                    break
            elif (Q_WORD.match(txt) or Q_BARE.match(txt)) \
                    and int((Q_WORD.match(txt) or Q_BARE.match(txt)).group(1)) == 1:
                cands.add(pi)
                break
    best, best_score = None, (-1, -1)
    for start in sorted(cands):
        stop = len(doc)
        for pi in range(start + 1, len(doc)):
            if TRANSCRIPT.search(doc[pi].get_text()):
                stop = pi
                break
        if parts_mode:
            # Word-consistent runs, one per part-word seen from this start.
            per = {}
            wantw = {}
            for pi in range(start, stop):
                for txt, x, y in lines_with_pos(doc[pi]):
                    if x > 0.6:
                        continue
                    ordn, hit = _part_match(txt)
                    if not hit or ordn is None:
                        continue
                    word = _part_word(txt)
                    wantw.setdefault(word, 1)
                    if ordn == wantw[word]:
                        per.setdefault(word, {})[wantw[word]] = (pi + 1, y)
                        wantw[word] += 1
                if any(len(r) == want_n for r in per.values()):
                    break
            full = [r for r in per.values() if len(r) == want_n]
            if not full:
                continue
            found = full[0]
        else:
            found, want = {}, 1
            for pi in range(start, stop):
                for txt, x, y in lines_with_pos(doc[pi]):
                    if x > 0.4:
                        continue
                    m = Q_WORD.match(txt) or Q_BARE.match(txt)
                    if m and int(m.group(1)) == want:
                        found[want] = (pi + 1, y)
                        want += 1
                if len(found) == want_n:
                    break
            if len(found) != want_n:
                continue
        pages = sorted({pg - 1 for pg, _ in found.values()})
        # A run whose pages carry a listening header outranks any that does
        # not, whatever the word overlap says: overlap is a tie-breaker among
        # structurally plausible candidates, not a licence to pick the
        # reading section because it shares more exam furniture.
        heard = any(LISTEN.search(doc[pi].get_text()) for pi in pages) \
            or LISTEN.search(doc[start].get_text()) is not None
        score = (1 if heard else 0, len(_harvest_words(doc, pages) & paper_words))
        if score >= best_score:
            best, best_score = found, score
    return best


# Booklets whose LAST part's answers run on past the page they start on. The
# last entry of a map otherwise ends at the foot of its first scheme page
# (right for a last QUESTION), which cut off the rest of the Polish 2026
# Ordinary Część E (EV p13 -> p14, IV p14 -> p15). Keyed for the same reason
# as FORCE_PARTS: a general rule moves the maps of eleven languages.
# The Portuguese 2022 booklets' Parte E runs on too (Higher p23 -> p24,
# Ordinary p21 -> p22), and so does the Polish Część E of 2025 Ordinary
# (p14 -> p15) and 2026 Higher (p15 -> p16, up to "APPENDIX 1" / "AGUISÍN 1"
# mid-page); EV and IV alike.
LAST_PART_TO_KEY_END = {"2026/LC548GLPA00EV.pdf", "2026/LC548GLPA00IV.pdf",
                        "2022/LC018ALPA00EV.pdf", "2022/LC018ALPA00IV.pdf",
                        "2022/LC018GLPA00EV.pdf", "2022/LC018GLPA00IV.pdf",
                        "2025/LC548GLPA00EV.pdf", "2025/LC548GLPA00IV.pdf",
                        "2026/LC548ALPA00EV.pdf", "2026/LC548ALPA00IV.pdf"}

# A heading that ends a scheme's listening key: its appendices (the modified
# marking scheme, the audio scripts), a line opening "APPENDIX" / "AGUISÍN".
KEY_END = re.compile(r"^(?:APPENDIX|AGUIS[ÍI]N)\b")


def _key_end(doc, start, start_y):
    """Where the listening key ends, for a last part that begins on scheme page
    `start` (1-based) at height `start_y`, as (page, y): at the first later
    appendix heading -- at its own height when answers are printed above it
    on its page (Polish 2026 Higher p16 sets "APPENDIX 1" under Część E's last
    answer), else at the foot of the page before -- or at the foot of the page
    before the first later transcript page. A scheme with neither is refused,
    never run on to its last page."""
    for pi in range(start - 1, len(doc)):
        lines = [ln for ln in lines_with_pos(doc[pi]) if pi > start - 1 or ln[2] > start_y]
        for txt, _x, y in lines:
            if KEY_END.match(txt):
                above = any(ln[2] < y for ln in lines)
                return (pi + 1, y) if above else (pi, 1.0)
        if pi > start - 1 and TRANSCRIPT.search(doc[pi].get_text()):
            return pi, 1.0
    raise ValueError(f"no appendix or transcript after scheme page {start}: "
                     "the key's end cannot be read, so the last part is not extended")


def build_sidecar(paper_path, scheme_path):
    paper, scheme = fitz.open(paper_path), fitz.open(scheme_path)
    key = f"{os.path.basename(os.path.dirname(paper_path))}/{os.path.basename(paper_path)}"
    pq, part_labels = paper_questions(paper, force_parts=key in FORCE_PARTS)
    if not (2 <= len(pq) <= 12):
        return None, f"paper run is {len(pq)} heads — outside any aural format"
    sb = scheme_blocks(scheme, len(pq), _harvest_words(paper),
                       parts_mode=part_labels is not None)
    if sb is None:
        return None, "no listening section reconciles with the paper's question count"

    order = [sb[n] for n in sorted(sb)]
    if order != sorted(order):
        return None, "scheme run is not monotonic"

    q = []
    ordered = sorted(pq)
    for i, n in enumerate(ordered):
        pg, y = pq[n]
        y_end = 1.0
        if i + 1 < len(ordered) and pq[ordered[i + 1]][0] == pg:
            y_end = pq[ordered[i + 1]][1]
        spg, sy = sb[n]
        if i + 1 < len(ordered):
            npg, ny = sb[ordered[i + 1]]
        elif key in LAST_PART_TO_KEY_END:
            npg, ny = _key_end(scheme, spg, sy)
        else:
            npg, ny = spg, 1.0
        region = []
        if npg == spg:
            region.append({"p": spg, "r": [0.0, round(max(0.0, sy - 0.012), 4),
                                           1.0, round(ny if ny > sy else 1.0, 4)]})
        else:
            region.append({"p": spg, "r": [0.0, round(max(0.0, sy - 0.012), 4), 1.0, 1.0]})
            for mid in range(spg + 1, npg):
                region.append({"p": mid, "r": [0.0, 0.0, 1.0, 1.0]})
            if ny > 0.04:
                region.append({"p": npg, "r": [0.0, 0.0, 1.0, round(ny, 4)]})
        chip = {"n": str(n), "conf": 1.0, "mode": "crop",
                "pP": pg, "pY": [round(y, 4), round(y_end, 4)],
                "region": region}
        if part_labels:
            chip["label"] = part_labels[n]
        q.append(chip)
    return {
        "v": 1,
        "paperFileid": os.path.basename(paper_path),
        "schemeFileid": os.path.basename(scheme_path),
        "component": "",
        "band": [1, len(scheme) + 1],  # bounds SCHEME pages, upper exclusive
        "copyright": COPYRIGHT,
        "q": q,
    }, None


def qa_echo(paper_path, scheme_path, sidecar, limit=2):
    paper, scheme = fitz.open(paper_path), fitz.open(scheme_path)
    for chip in sidecar["q"][:limit]:
        pg = paper[chip["pP"] - 1]
        W, H = pg.rect.width, pg.rect.height
        ask = pg.get_text(clip=fitz.Rect(0, chip["pY"][0] * H, W,
                                         min(chip["pY"][0] + 0.08, 1.0) * H))
        seg = chip["region"][0]
        sg = scheme[seg["p"] - 1]
        SW, SH = sg.rect.width, sg.rect.height
        x0, y0, x1, y1 = seg["r"]
        crop = sg.get_text(clip=fitz.Rect(x0 * SW, y0 * SH, x1 * SW,
                                          min(y0 + 0.10, y1) * SH))
        print(f"      Q{chip['n']:<3} ask : {' '.join(ask.split())[:60]!r}")
        print(f"      {'':<4} crop: {' '.join(crop.split())[:60]!r}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--subject", choices=sorted(SUBJECT_CODES))
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args()

    wrote = dropped = 0
    for subject, code in sorted(SUBJECT_CODES.items()):
        if args.subject and subject != args.subject:
            continue
        for year in YEARS:
            for level in ("A", "G", "B"):
                for lang in ("BV", "EV", "IV"):
                    pf = f"{code}{level}LPA00{lang}.pdf"
                    ppath = os.path.join(CORPUS, "exampapers", str(year), pf)
                    if not os.path.exists(ppath):
                        continue
                    # A BV booklet answers to the EV scheme; EV/IV pair 1:1.
                    slang = "EV" if lang == "BV" else lang
                    spath = os.path.join(CORPUS, "markingschemes", str(year),
                                         f"{code}{level}LP000{slang}.pdf")
                    if not os.path.exists(spath):
                        continue
                    out = os.path.join(ANSWERS_DIR, str(year), f"{pf}.json")
                    if os.path.exists(out):
                        continue
                    sidecar, why = build_sidecar(ppath, spath)
                    tag = f"{subject} {year} {level}{lang}"
                    if sidecar is None:
                        print(f"DROP {tag}: {why}")
                        dropped += 1
                        continue
                    print(f"MAP  {tag}: {len(sidecar['q'])} questions")
                    if not args.quiet:
                        qa_echo(ppath, spath, sidecar)
                    if args.dry_run:
                        continue
                    os.makedirs(os.path.dirname(out), exist_ok=True)
                    with open(out, "w", encoding="utf-8") as fh:
                        json.dump(sidecar, fh, ensure_ascii=False, sort_keys=True,
                                  separators=(",", ":"))
                    wrote += 1
    print(f"done: {wrote} sidecars written, {dropped} dropped")
    return 0


if __name__ == "__main__":
    sys.exit(main())
