#!/usr/bin/env python3
"""
Paper Trail — PAPER-SIDE-ONLY question anchors for the Topic Vault.

~2,000 index papers have no answer-map sidecar (scheme unmappable or not yet
attempted), so the vault cannot crop their questions. This generator produces a
paper-anchors artifact for those papers: the SAME PaperAnswerMap sidecar schema
(types/paperTrail.ts) with real per-question paper anchors (pP/pY) but NO scheme
mapping claimed — every question is mode:'pagejump' with a placeholder region
[{p:1}], schemeFileid "" and a `paperOnly:1` marker. The vault only needs pP/pY
(components/PaperTrail/paperRegion.ts derives the paper crop from anchor N to
anchor N+1); mode:'crop' is required only for the answer-reveal toggle, so these
maps light up the question crop while the card keeps its honest "Open beside its
marking scheme" fallback.

HOSTING (Storage uploads are credential-blocked, task #94): outputs are staged
into public/paper-anchors/<year>/<paperFileid>.json and deploy with the app via
Firebase Hosting on push to main — no Storage objects. The vault tries the
Storage sidecar first and falls back to this hosted path (vaultResolve.ts).

HONESTY GATES — a wrong crop is worse than none:
  • detectors only accept a question token that STARTS a line at the left
    margin of an unrotated page;
  • per-question QA: after building the map, each anchor is independently
    re-verified — the expected marker text must be re-found at (pP, pY[0]);
  • numbering gate: the detected numbers must form ONE contiguous run per
    section (the run may start above 1 — e.g. biology Section-C docs print
    11..17). ANY gap in the run hard-drops the PAPER: a missing number is a
    missing marker (the 2011 OL maths P2 IV dotless-"4" class) and the
    previous question's derived crop would swallow the missed one;
  • monotonic gate: anchors must be monotonic in print order;
  • span gate: consecutive anchors more than MAX_PAGES pages apart make the
    viewer's paperRegionFor refuse the crop — drop the PAPER;
  • contiguity proof → continuation-page tolerance: when the run is gap-free
    AND every raw detector hit is positionally consistent with its anchored
    question (no out-of-place duplicate that would betray a numbering
    restart) AND the anchors plausibly tile the document (≤ MAX_LEAD_PAGES
    content pages before the first anchor; anchored span ≥ MIN_ANCHOR_SPAN of
    the content pages), then anchor-less content pages between/after anchors
    are CONTINUATION pages (answer booklets, multi-page questions) — they
    belong to the preceding question's crop and the paper ships;
  • strict fallback: when the contiguity proof fails, the original blanket
    gates apply — hole gate (a content page BETWEEN anchors with no anchor
    drops the PAPER) and tail gate (real content after the last anchor drops
    the PAPER);
  • a paper ships only when ≥ MIN_QUESTIONS anchor.
  Note the last question's crop is anchor → end of ITS OWN page (viewer
  contract): in booklets its later continuation pages are not shown, and any
  same-page trailing matter is included — verified visually per wave.

Usage:
  python3 paper_anchors.py <subjectId>
      [--grammar auto|section_token|question|lead_int|sectioned_lead_int
                 |armed_sectioned]
      [--years 2010-2025] [--qa-render N] [--dry-run]

  sectioned_lead_int is the section-restart grammar (bare 'N.' numbering that
  restarts per section, keyed by SUBJECT_SECTION_PATTERNS). It is opt-in only —
  no subject is pinned to it in production (see that table's note).

  armed_sectioned (TV-8) adds ARM/DISARM state on top of section tracking
  (keyed by SUBJECT_ARMED_PATTERNS) for the section-restart READING papers,
  whose passages / grammar sub-lists / matching tasks carry DECOY numbering in
  the same per-section space as the real questions: a bare 'N.' is a question
  only while a question-block header has ARMED detection. Opt-in only.

Outputs (deterministic, sorted, idempotent):
  public/paper-anchors/<year>/<paperFileid>.json     (committed, hosted)
  scripts/paper-trail/out/paper-anchors-<subject>-report.md
  scripts/paper-trail/out/qa-render/<subject>/*.png  (--qa-render only)

All emitted page numbers are 1-BASED; all bands are fractions of the unrotated
page box — exactly the conventions of anchor-map.py and the viewer.
"""

import argparse
import json
import os
import random
import re
import sys
import urllib.request
from collections import defaultdict

import fitz  # pymupdf

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
INDEX_TS = os.path.join(REPO, "paperTrailData.ts")
CORPUS = os.path.join(REPO, "paper-trail-corpus")          # gitignored cache
PUBLIC_OUT = os.path.join(REPO, "public", "paper-anchors")  # committed, hosted
OUT_DIR = os.path.join(HERE, "out")

BUCKET = "nextstepuni-app.firebasestorage.app"
SIDECAR_V = 1
COPYRIGHT = "© State Examinations Commission"

LEFT_MARGIN_X = 140   # a header token must start left of this (points)
LEAD_INT_X = 95       # a bare 'N.' lead number sits within this of the left edge
MIN_QUESTIONS = 3     # a paper needs ≥3 anchored questions to be worth shipping
PAGEJUMP_CONF = 0.5   # below anchor-map's 0.6 "right scheme page" tier: no scheme claim
MAX_TAIL_CHARS = 400  # a post-questions page longer than this is unexplained content
MAX_LEAD_PAGES = 3    # contiguity proof: content pages allowed before Q-first
MIN_ANCHOR_SPAN = 0.5  # contiguity proof: anchored span / content pages floor

# Pages that carry no question content (fillers, back covers).
BLANK_PAGE_TEXTS = {
    "", "blank page", "this page is intentionally blank",
    "this page has been left blank intentionally",
    "this page has been intentionally left blank",
    "there is no examination material on this page",
}

# Per-subject grammar pins. Everything else runs 'auto' (best detector wins),
# but a pinned grammar removes one degree of freedom — prefer pinning when
# rolling a subject out. See PAPER-ANCHORS.md for the rollout recipe.
SUBJECT_GRAMMAR = {
    "design-and-communication-graphics": "section_token",
    # german runs armed_sectioned (TV-9): the HL written paper is a section-
    # restart reading paper (TEXT I / TEXT II, questions 1..4 each) whose
    # passages carry decoy line numbers and whose Satzhälften task carries a
    # decoy 1..6 list — the armed state machine excludes both, and per-question
    # crop-ends (endP/endY at the next TEXT/PRODUKTION header) stop each reading
    # section's last question bleeding into the next. Render-QA verified on
    # 2010-2021 HL; OL (3-text layout) defers cleanly. The already-live classic
    # sidecars (answers:1) are skipped, not touched.
    "german": "armed_sectioned",
    # Sciences wave: LC biology/chemistry/physics print questions as a bare
    # left-margin 'N.' in every era (pre- and post-2020 formats verified).
    "biology": "lead_int",
    "chemistry": "lead_int",
    "physics": "lead_int",
    # physics-and-chemistry prints the same bare left-margin 'N.' run
    # (Q1..12) as the other sciences in every era (2026-07 wave).
    "physics-and-chemistry": "lead_int",
    # agricultural-science is era-split (old spec ≤2020: 'N.' lead ints; new
    # spec 2021+: 'Question N') — it runs UNPINNED (auto): the per-paper
    # best-detector pick resolves the era correctly (2026-07 wave).
    # applied-mathematics is era-split like mathematics and runs UNPINNED
    # (auto): old-spec papers (≤2019 remainder) print bare 'N.' lead ints and
    # ship strict; new-spec booklets (2023+) print 'Question N'/'Ceist N' but
    # every one has a question spanning 4 pages to the next anchor, so they
    # all drop at the span gate (viewer contract) — correct refusals
    # (2026-07 STEM+languages wave).
    # mathematics is era-split too, so it runs UNPINNED (auto): compact
    # pre-Project-Maths papers (2010–2012 P100/P200/P000) print bare 'N.'
    # lead ints; every Project-Maths-format paper (P130/P230 pilots and all
    # papers 2013+) prints 'Question N' / 'Ceist N'. The PM-format papers are
    # answer booklets whose questions span multiple pages (continuation parts
    # and answer space between headers) — they ship via the contiguity proof
    # (continuation pages tolerated), while a broken run (e.g. 2011 OL P2 IV
    # prints Q4's header dotless, so Q4 goes undetected) hard-drops at the
    # numbering gate (2026-07 recovery wave — see the out/ reports).
    #
    # Business + humanities wave (2026-07). Verified against the text layers:
    # accounting prints one continuous left-margin 'N.' run (Q1..Q9, one
    # question per page) in every era; internal numbered lists exist but the
    # real headers always precede them in print order (anchor lines verified).
    "accounting": "lead_int",
    # economics 2021+ is a 'Question N' answer booklet (16 questions,
    # contiguity-proven); pre-2021 papers carry NO question-word tokens and
    # restart bare 'N.' numbering per section (Section A 1..9, Section B
    # essays restart at 1) — under this pin they anchor 0 questions and drop
    # cleanly instead of tripping over the restart.
    "economics": "question",
    # religious-education prints 'Question N' in Section A only: OL has Q1-3
    # (ships), HL has Q1-2 (< MIN_QUESTIONS, drops). Sections B-J are
    # unnumbered essay tasks with no markers of any grammar.
    "religious-education": "question",
    # technology runs UNPINNED (component-split): Section A docs (014) are
    # lead_int (HL 1..15 / OL 1..12); Section B docs (015) print 'Question N'
    # but only Q2/Q3 are numbered (Section C options are unnumbered) so they
    # drop on coverage — correct refusals. CAUTION: Section A embeds
    # '1. ____' answer-list lines inside questions (fabricated-numbers
    # class); they are harmless here ONLY because the real headers precede
    # them in print order (first-occurrence-wins) — verified textually + by
    # render for 2011/2021 (2026-07 wave). Papers where an answer list
    # follows the LAST question drop at the tail gate.
    # engineering written papers print 'Question N' (Q1..8 HL/OL) in every
    # era; pinned because lead_int also fires on numbered sub-lists (1..5)
    # inside questions and must not compete. Practical Test / Practical Paper
    # sheets (018/034/035/036, incl. BV) carry no markers and drop on
    # coverage.
    "engineering": "question",
    # construction-studies written papers print one left-margin 'N.' run
    # (Q1..10) in every era; the Practical Test / Project sheets are rotated
    # A3 drawings with no markers of any grammar and drop on coverage.
    # 2014 HL prints Q5's header without a detectable dot → numbering gap →
    # correct hard drop (dotless-header class).
    "construction-studies": "lead_int",
    # computer-science prints 'Question N' throughout (Section A&B booklets
    # number 1..15; the separate Section C doc holds only Question 16 and
    # drops on coverage — correct refusal for a one-question doc). CAUTION:
    # pinned because lead_int fabricates anchors from numbered task lists
    # inside Section C (2025 IV prints '1.'/'2.'/'3.' list lines that would
    # win the auto tie) — the fabricated-numbers trap class (2026-07 wave).
    "computer-science": "question",
    # MFL wave (2026-07): french, german, italian, japanese and russian ship
    # NOTHING — every paper class (written P1/P2, aural, BV combined)
    # restarts bare-'N.' numbering per section (and the covers print numbered
    # instruction lists), so they drop wholesale at the strict gates
    # (section-restart class; needs a section-aware detector).
    # spanish is the exception: the aural papers number ONE continuous task
    # run (old spec '1. ANUNCIO:'.. '7. UNA NOTICIA:' via lead_int; 2023+
    # 'Question 1..7' via question) and ship. CAUTION — the spanish
    # 'Section B' reading-text handouts (LC012?LP015*/LPO15*, 2pp) print
    # NUMBERED TEXT PARAGRAPHS 1..7 that pass every gate as fake questions
    # (paragraph-numbering trap, kin of the fabricated-numbers class); their
    # 24 sidecars were deleted post-run — do not ship 015/O15 docs.
    # latin + ancient-greek print a short genuine left-margin 'N.' run
    # (latin 1..5; greek HL 1..4 / OL 1..3 — verified question headers:
    # 'Translate into English…', 'Answer three of…') starting on page 2 in
    # every era (2026-07 wave).
    "latin": "lead_int",
    "ancient-greek": "lead_int",
    # arabic ships NOTHING: the text layer carries no per-question markers of
    # any grammar. CAUTION — the ONLY lead_int hits are the cover-page
    # instructions list ('1. Read these directions…', all five on p1), which
    # would PASS the contiguity proof (single-page anchor span, no other
    # markers → span ratio 1.0) and ship a garbage sidecar; the pin keeps
    # lead_int out so every paper drops on coverage (2026-07 wave).
    "arabic": "question",
    # mandarin-chinese prints 'Question N' (new-spec subject, 2022+).
    # CAUTION: cover/instruction lines ('Answer either Question 1 OR
    # Question 2') also fire the detector at the left margin; papers where
    # that garbles the run drop non-monotonic, but ALWAYS render-verify Q1's
    # crop on anchored papers — an instruction-page Q1 anchor is the
    # residual risk (2026-07 wave).
    "mandarin-chinese": "question",
    # JC wave (2026-07): the new-spec JC booklets print 'Question N'
    # continuously (maths 1..14, science 1..17, history 1..8, business
    # 1..18). Pinned because lead_int fabricates 3-12 anchors from numbered
    # lists / sub-parts in every one of them (fabricated-numbers class).
    # jc-geography's remaining docs (Map / Source Paper single sheets) carry
    # no markers of any grammar and drop on coverage.
    "jc-mathematics": "question",
    "jc-science": "question",
    "jc-history": "question",
    "jc-business-studies": "question",
    "jc-geography": "question",
    # Same 'Question N' class (jc-home-economics' lead_int fires 54 times on
    # answer-table rows — the pin is load-bearing there). jc-graphics
    # (rotated 90° sheets) and jc-music (no markers) drop wholesale under
    # any grammar; pinned for uniformity.
    # lca-engineering ships NOTHING. CAUTION — worst instance of the
    # cover-instructions trap (2026-07 wave): its only lead_int hits are the
    # exam-cover instruction list ('1. Write your examination number…'..'6.'
    # all on p1) and, because no other grammar marks any later page, the
    # contiguity proof PASSES (single-page span, ratio 1.0, 23-page
    # 'continuation' tail) and 30 garbage sidecars ship. The pin forces the
    # question detector (sole hit: the 'If Question 7 is attempted…'
    # instruction) so every paper drops on coverage. If a subject's anchors
    # all sit on page 1, treat it as this trap class.
    "lca-engineering": "question",
    # lca-sign-language ships NOTHING: the docs are 4-page interview/
    # presentation briefing sheets whose only lead_int hits are prompt/
    # marking-criteria lists on the BACK page (back-cover trap class); the
    # pin forces the hitless question grammar so all drop on coverage
    # (2026-07 wave). Other LCA subjects that ship (crafts-and-design,
    # mathematical-applications, office-admin-and-customer, active-leisure
    # 2010) do so via genuine 'Question/Ceist N' booklet headers under auto;
    # the rest drop wholesale at the span/hole/tail gates (LCA booklets give
    # each question >3 pages of answer space, or restart per section).
    "lca-sign-language": "question",
    "jc-french": "question",
    "jc-italian": "question",
    "jc-irish": "question",
    "jc-applied-technology": "question",
    "jc-classics": "question",
    "jc-home-economics": "question",
    "jc-jewish-studies": "question",
    "jc-music": "question",
    "jc-graphics": "question",
    # physical-education prints 'Question N' (1..16/18 booklets). CAUTION —
    # two trap classes (2026-07 wave): (a) 2022+ papers print an
    # instruction-line 'Question 13 …' at the left margin of the cover page;
    # first-occurrence-wins anchors it there → non-monotonic → those papers
    # drop (stray instruction-page-reference class, correct refusal);
    # (b) lead_int fabricates 3-4 anchors from '1.'/'2.' answer-list lines,
    # so the pin keeps it from ever winning the auto pick.
    "physical-education": "question",
    # irish is TYPE-SPLIT, so the DEFAULT pin is 'question' (the foundation-level
    # aural papers number continuously, Ceist 1..12, and anchor cleanly here).
    # The HL Paper-2 léamhthuiscint restarts numbering per reading text (A/B) and
    # is generated by a SECOND, explicit pass — `paper_anchors.py irish
    # --grammar armed_sectioned` — whose armed-island gate (TV-9b) anchors the
    # two texts' 12 questions with clamped crop-ends. The two passes write
    # disjoint fileids (aural vs LP200), so both sidecar sets coexist. Bare-'N.'
    # tokens elsewhere in these papers are sub-parts, never question starts.
    "irish": "question",
    # classical-studies new-spec (2024+) prints 'Question N' (exam booklets
    # and the 004BV source booklets); old-spec papers organise by 'Topic N.'
    # headers with roman-numeral parts — no supported grammar, zero detector
    # hits, correct wholesale drop pending a topic-aware detector.
    "classical-studies": "question",
    # art History-and-Appreciation papers print one continuous 'N.' run
    # (Q1..20 HL / Q1..21 OL) across all eras; the studio sheets (Craftwork,
    # Design, Life Sketching, Imaginative Composition) carry no markers and
    # drop on coverage.
    "art": "lead_int",
    # business runs UNPINNED (component/era-split): 2020+ 'Section 2 & 3'
    # long-answer booklets print 'Question N'; 2020+ 'Section 1' short-answer
    # booklets and the 2010-2019 combined papers print bare 'N.' lead ints.
    # Pre-2020 combined papers whose Sections 2/3 restart at '1.' drop at the
    # strict gates (section-restart class).
    # geography runs UNPINNED (component-split): Part 1 (042) short-answer
    # booklets are lead_int, Part 2 (043) is 'Question N'. CAUTION: the 042
    # booklets end with a back-cover marks grid of 'Question 1..12' rows; in
    # 2021 OL the question detector tied lead_int on anchor count and won the
    # tie, anchoring the GRID (all 12 anchors on the last page) — those two
    # sidecars were deleted post-run (2026-07 wave). Verify per era that
    # Part 1 ships via lead_int before trusting a new year.
    # home-economics-s-and-s runs UNPINNED (component-split): 2020-era
    # Section A booklet is lead_int (1..12), Section B&C is 'Ceist/Question N';
    # pre-2020 combined papers restart per section and drop.
    # english runs UNPINNED: HL Paper One ships its Section II composition
    # prompts (bare 'N.' 1..7 on one page, strict gates); Paper Two restarts
    # numbering per section (comparative/poetry) and drops (section-restart
    # class, needs a section-aware upgrade).
    # music runs UNPINNED (component-split): OL Listening ships via
    # 'Question N', Composing + Unprepared Tests via lead_int. CAUTION: the
    # HL Listening-Elective booklets (007) embed a numbered answer list
    # inside Q3 while real Q4 prints as '4.(a)' — lead_int fabricates Q4/Q5
    # anchors from the list lines and the strict gates cannot see it (the
    # answer-line tail is under MAX_TAIL_CHARS). The 2010-2024 Elective
    # sidecars were deleted post-run (2026-07 wave); do not ship 007 booklets
    # from lead_int without per-anchor line verification.
    # history and politics-and-society ship NOTHING (2026-07 wave): history
    # restarts topic-essay numbering per section behind the DBQ Q1-4;
    # politics-and-society prints 'Question 3(a)'-style subpart headers and
    # its Section-B header is not in the text layer. Both are correct
    # wholesale refusals pending detector upgrades.
}

# ── Section-restart grammar (det_sectioned_lead_int) ─────────────────────────
# Papers whose bare-'N.' question numbering RESTARTS per section (language
# reading papers, léamhthuiscint A/B, etc.). Each entry is a list of compiled
# line-start patterns; a left-margin line matching any of them opens a NEW
# section, so a 'Ceist 1' under text B is a DIFFERENT question from 'Ceist 1'
# under text A. The detector emits sort_key=(section_index, N), which keeps
# per-section numbering unique (build_anchors dedups by that tuple, exactly as
# det_section_token's 'A-1' keys do for DCG) — the human 'A-1'/'B-2' style id
# lands in the sidecar `label`, while make_sidecar renumbers `n` sequentially.
#
# SAFETY — this table is INERT unless a subject is EXPLICITLY pinned to
# 'sectioned_lead_int' (SUBJECT_GRAMMAR or --grammar). In auto mode the
# detector falls back to plain det_lead_int behaviour (section_index always 0),
# so populating an entry here can never change an unpinned subject's output.
# The gate is SECTIONED_ENABLED, set once per run in main().
#
# The three entries below carry the VERIFIED section structure of the pilot
# reading papers (confirmed against 2019–2024 text layers). They are recorded
# for the next agent but DELIBERATELY LEFT UNPINNED: on every sampled paper the
# reading passages / grammar sub-lists / matching tasks print their OWN bare
# 'N.' runs (Irish/French number the passage paragraphs 1..k; German's Text-II
# 'Satzhälften' matching task and 'Angewandte Grammatik' sub-lists number 1..n;
# stray ordinals like '18. Geburtstag' fire too). Those decoys share the
# per-section numbering space with the real questions, so a bare-'N.' detector
# cannot tell a question from a paragraph — it fabricates phantom questions that
# only the span/monotonic/tail gates catch by luck, not by guarantee. These
# papers therefore DEFER to the same "armed / subsection-aware" frontier as
# English P2 and History (see PAPER-ANCHORS.md). Do NOT pin them until a
# refinement that recognises the question-block header (e.g. 'Ceisteanna',
# 'Beantworten Sie', 'Répondez') arms detection and disarms the passages.
SUBJECT_SECTION_PATTERNS = {
    # Irish Paper Two léamhthuiscint: 'Ceist N' + the 'A – 50 marc' / 'B – 50
    # marc' reading-text sub-headers restart the question run per text.
    "irish": [re.compile(p, re.I) for p in (
        r"^[AB]\s*[–—-]\s*\d+\s*marc\b",
        r"^Ceist\s+\d",
    )],
    # French written paper: Section A/B + the 'Q.1'/'Q.2' reading groups.
    "french": [re.compile(p, re.I) for p in (
        r"^Section\s+[AB]\b",
        r"^Q\.?\s*\d",
    )],
    # German written paper: 'TEXT I/II: <subsection>' + Schriftliche Produktion.
    "german": [re.compile(p, re.I) for p in (
        r"^TEXT\s+I{1,3}\s*:",
        r"^SCHRIFTLICHE\s+PRODUKTION",
    )],
}

# Set once per run in main(): the detector only consults SUBJECT_SECTION_PATTERNS
# when the active grammar is 'sectioned_lead_int' (explicit opt-in), so the new
# detector is a no-op clone of det_lead_int for every other subject/run.
ACTIVE_SUBJECT = None
ACTIVE_FILEID = None    # current paper's fileid — set per paper in main() so
                        # fileid-scoped armed configs (TV-12) can key off it
SECTIONED_ENABLED = False

# ── Armed section-aware grammar (det_armed_sectioned) — TV-8 ──────────────────
# The section-restart reading papers (irish léamhthuiscint, french/german
# reading) carry DECOY numbering that shares the per-section number space with
# the real questions: numbered passage paragraphs, numbered reading-passage
# sentences, matching-task item lists ('Satzhälften'), grammar sub-lists
# ('Angewandte Grammatik'), and stray ordinals ('18. Geburtstag'). A bare-'N.'
# detector — even the section-aware det_sectioned_lead_int — cannot tell a
# question from a paragraph, so it fabricates phantom questions (TV-7).
#
# det_armed_sectioned adds an ARM/DISARM state machine on top of the section
# tracking: bare-'N.' lines are IGNORED until a QUESTION-BLOCK header ARMS
# detection, and a passage / grammar / matching-task header DISARMS it again.
# So the numbered passage above the questions, and the numbered sub-lists inside
# a question, never emit hits. Per subject:
#   • 'open'   — a NEW section boundary (also disarms): bumps the section index
#                so each reading text's 1..N run stays a distinct key, exactly
#                as det_section_token's 'A-1'/'B-1' keys do for DCG. Matched at
#                the LEFT MARGIN and anchored at line start (re.match).
#   • 'arm'    — the question-block header that turns detection ON (re.search).
#   • 'disarm' — a passage/matching/grammar header that turns detection OFF
#                without opening a new section (re.search).
#   • 'margin' — OPTIONAL per-subject x-gate for the header lines above
#                (default LEFT_MARGIN_X). Question-marker detection is never
#                affected (still LEAD_INT_X). Added for geography, whose 2017
#                OL EV 'PART TWO' / 2013 OL IV 'CUID 1' headers print at
#                x0≈140-142, just past the default 140 gate (TV-13).
# Every pattern below was verified against the real 2019–2024 text layers.
#
# SAFETY — INERT unless the run is EXPLICITLY pinned to 'armed_sectioned'
# (SUBJECT_GRAMMAR or --grammar). When ARMED_ENABLED is False the config lookup
# returns None: detection starts ARMED, the section index stays 0, and the
# output is byte-identical to det_lead_int — so registering this detector cannot
# regress any existing subject (proven in-session, like det_sectioned_lead_int).
ARMED_ENABLED = False

SUBJECT_ARMED_PATTERNS = {
    # German written paper (LC011...P000). Two reading texts (HL) / three (OL),
    # each 'TEXT n: LESEVERSTÄNDNIS' passage (dot-less line numbers) followed by
    # 'Lesen Sie Text n. Beantworten Sie Frage ...' then questions 1..4. The
    # 'TEXT n:' headers (incl. ANGEWANDTE GRAMMATIK, ÄUSSERUNG ZUM THEMA) and
    # SCHRIFTLICHE PRODUKTION open new sections and disarm; the 'Satzhälften'
    # matching task inside a question disarms so its 1..6 item list is ignored.
    # NOTE case-sensitive open ('TEXT'≠'Text') so the arm line 'Lesen Sie Text
    # I. Beantworten…' is NOT read as a section opener.
    "german": {
        "open": [re.compile(p) for p in (
            r"^TEXT\s+[IVX]+\b",
            r"^SCHRIFTLICHE\s+PRODUKTION\b",
        )],
        "arm": [re.compile(r"Beantworten\s+Sie\s+Frage", re.I)],
        "disarm": [re.compile(r"Satzh[aä]lften", re.I)],
    },
    # Irish Paper Two léamhthuiscint (LC001[A|G]LP200IV). 'Ceist 1
    # LÉAMHTHUISCINT' holds reading texts A and B; each is 'Léigh an sliocht seo
    # a leanas …' (passage intro — opens a section, disarms) then numbered
    # passage paragraphs 1..k (ignored while disarmed) then 'Ceisteanna' (arms)
    # then questions 1..6. 'Ceist 2/3/4' (prós/filíocht/litríocht — no bare-'N.'
    # questions) open sections and disarm so nothing leaks from them.
    "irish": {
        "open": [re.compile(p) for p in (
            r"^Léigh\s+an\s+sliocht",
            r"^Ceist\s+[2-9]\b",
        )],
        "arm": [re.compile(r"^Ceisteanna\b")],
        "disarm": [],
    },
    # french: DELIBERATELY UNCONFIGURED. The reading questions follow the
    # passage with NO question-block header to arm on (the passage is headed
    # 'Q.1'/'Q.2'; the questions have no label and share the passage's 1..n
    # number space), and the 50-word sub-answers print their own '1.'/'2.'
    # answer-box numbers. There is no reliable header to arm/disarm — so french
    # stays inert (defers). See PAPER-ANCHORS.md. (Not the irish-OL case below:
    # the french questions also have no per-question SHAPE marker, so the
    # `question` row-shape key cannot separate them either.)
    #
    # Geography HL/OL written paper (LC005[A|G]LP000). 'PART ONE' (EV) / 'CUID A
    # hAON' (IV) opens the 12 short-answer questions (bare left-margin 'N.',
    # 1..12); 'PART TWO' (EV) / 'CUID A DÓ' (IV) opens the structured/essay
    # section, whose questions print as 'Question N' text (no bare 'N.') AND
    # whose examiner marking grid prints a decoy bare-'N.' run 13..24 near the
    # end — disarming at PART TWO keeps that grid, and everything after Part One,
    # out of the anchored run. Case-sensitive uppercase so the title-case
    # contents-page entries ('Part One', 'Cuid a hAon') never arm/open. This
    # anchors ONLY Part One (the tagged n 1..12); Part Two is intentionally not
    # cropped. Section 0 keeps bare 'N' labels so n matches the geography tags.
    #
    # TV-13 stragglers (verified against the text layers):
    #   • pre-2016 OL IV (2010-2015 LC005GLP000IV) print 'CUID 1 – CEISTEANNA
    #     GEARRFHREAGRA' instead of 'CUID A hAON' — hence the extra arm pattern
    #     ('1\b' cannot match 'CUID 12'; HL IV and 2016+ OL IV keep 'CUID A
    #     hAON', so the extra pattern is inert there).
    #   • 2017 OL EV's 'PART TWO …' header starts at x0=140.46 and 2013 OL IV's
    #     'CUID 1 …' at x0=141.1 — both just past the default LEFT_MARGIN_X
    #     (140) strict gate, so the open/arm never fired and the papers dropped.
    #     'margin' widens the HEADER-eligibility x-gate (arm/open/disarm lines
    #     only — question-marker detection still uses LEAD_INT_X) for this
    #     subject; every other year's headers sit at x0 ≤ 136, so the widened
    #     gate matches the same lines (regenerated 2010-2017 sidecars verified
    #     byte-identical except the two recovered stragglers).
    "geography": {
        "open": [re.compile(p) for p in (
            r"^PART TWO\b",
            r"^PART THREE\b",
            r"^CUID A DÓ\b",
            r"^CUID A TRÍ\b",
        )],
        "arm": [re.compile(r"^PART ONE\b"), re.compile(r"^CUID A hAON\b"),
                re.compile(r"^CUID 1\b")],
        "disarm": [],
        "margin": 150,
    },
}

# ── Fileid-scoped armed configs (TV-12) ───────────────────────────────────────
# One subject can print DIFFERENT armed grammars per paper class: irish HL P2
# (LC001ALP200IV) has a 'Ceisteanna' header that arms question detection, but
# irish OL P2 (LC001GLP200IV) prints its questions DIRECTLY under the passage
# with no arm header at all. Entries here are (subjectId, fileid regex, config)
# — consulted before SUBJECT_ARMED_PATTERNS, first match wins, and a paper that
# matches no row falls through to the subject-level entry unchanged. Same
# INERT-unless-pinned guard as the subject table (ARMED_ENABLED).
#
# Two OPTIONAL config keys (unused by the subject-level entries, so they change
# nothing for german/irish-HL/geography):
#   • 'always_armed' — detection starts ARMED and 'open' headers do NOT disarm
#     (there is no arm header to re-arm afterwards). Only safe together with a
#     'question' shape key: with detection always on, the shape test is the
#     ONLY thing separating questions from decoy numbering.
#   • 'question'     — row-shape regex: a bare left-margin 'N.' emits a hit
#     ONLY if the text following it in the same VISUAL ROW (all words within
#     ±3pt of the marker's top, left→right, any line group) matches. Verified
#     against every OL P2 text layer 2013-2025: question rows are 'N. (a) …'
#     (sub-part '(a)' immediately follows the number, even when the PDF splits
#     the row across line groups), passage-paragraph rows are 'N. <prose>' —
#     zero overlap in 13 sittings (130 questions / ~110 paragraph decoys).
ARMED_FILEID_CONFIGS = [
    # Irish Paper Two léamhthuiscint, ORDINARY level (LC001GLP200IV, TV-12).
    # Layout (verified 2013-2025): p4-5 text A — 'Léigh an sliocht seo a
    # leanas …' intro, numbered passage paragraphs 1..5, then questions
    # '1. (a) … (Alt 1)' .. '5. (a/b) …' directly below the passage (NO
    # 'Ceisteanna' header, unlike HL); p6-7 text B repeats the shape; then
    # Ceist 2 (prós) / Ceist 3 (filíocht) with no bare-'N.' markers. The two
    # 'Léigh an sliocht' intros open the A/B islands (so each 1..5 run keys
    # distinctly and text A's Q5 crop-end clamps at text B's intro); the
    # 'Ceist/CEIST N' headers (2013-2019 print 'CEIST 2' uppercase, 2020+
    # 'Ceist 2') open the post-reading sections so Q10's crop-end clamps
    # there when present. The instruction-page 'Ceist 2:'/'Ceist 3:' lines
    # (p3) also fire 'open' — harmlessly, before any anchor. Passage
    # paragraphs are excluded by the 'question' row shape, not by arming.
    ("irish", re.compile(r"^LC001GLP200", re.I), {
        "open": [re.compile(p) for p in (
            r"^Léigh\s+an\s+sliocht",
            r"^Ceist\s+[2-9]\b",
            r"^CEIST\s+[2-9]\b",
        )],
        "arm": [],
        "disarm": [],
        "always_armed": True,
        "question": re.compile(r"^\(a\)"),
    }),
]


def armed_cfg_for(subject, fileid):
    """Armed config for the CURRENT paper: fileid-scoped override first
    (ARMED_FILEID_CONFIGS), else the subject-level entry. None unless the run
    is pinned to armed_sectioned — exactly the old lookup for every paper that
    matches no override row."""
    if not ARMED_ENABLED:
        return None
    for subj, pat, cfg in ARMED_FILEID_CONFIGS:
        if subj == subject and fileid and pat.match(fileid):
            return cfg
    return SUBJECT_ARMED_PATTERNS.get(subject)

_LIGATURES = {
    "Ɵ": "ti", "Ʃ": "tt", "ϐ": "fi",
    "ﬀ": "ff", "ﬁ": "fi", "ﬂ": "fl",
    "ﬃ": "ffi", "ﬄ": "ffl", "ﬅ": "ft", "ﬆ": "st",
}


def deligature(s):
    if s.isascii():
        return s
    for k, v in _LIGATURES.items():
        if k in s:
            s = s.replace(k, v)
    return s


def norm_text(s):
    return re.sub(r"[^a-z0-9]+", " ", deligature(s).lower()).strip()


def log(msg):
    print(msg, flush=True)


# ─── index parsing (paperTrailData.ts is line-per-entry JSON) ─────────────────

def load_subject_index(subject_id):
    """(cycle, [(year, level, lang, label, fileid), ...]) for one subject."""
    with open(INDEX_TS, encoding="utf-8") as f:
        src = f.read()
    m = re.search(r'\{"id":\s*"%s".*?\}' % re.escape(subject_id), src)
    if not m:
        raise SystemExit(f"subject {subject_id!r} not in PAPER_TRAIL_SUBJECTS")
    cycle = json.loads(m.group(0))["cycle"]

    block_m = re.search(r'"%s":\s*\[\n(.*?)\n  \],' % re.escape(subject_id), src, re.S)
    if not block_m:
        raise SystemExit(f"subject {subject_id!r} has no PAPER_TRAIL_INDEX block")
    rows = []
    for line in block_m.group(1).splitlines():
        line = line.strip().rstrip(",")
        if not line.startswith('{"year"'):
            continue
        e = json.loads(line)
        for p in e["papers"]:
            rows.append({
                "year": e["year"], "level": e["level"], "lang": e["lang"],
                "label": p["label"], "fileid": p["doc"]["f"],
                "hasAnswers": p.get("answers") == 1,
            })
    return cycle, rows


# ─── download (public Storage REST, same layout as download.py) ──────────────

def fetch_paper(cycle, subject_id, year, fileid):
    dst = os.path.join(CORPUS, "exampapers", str(year), fileid)
    if os.path.exists(dst) and os.path.getsize(dst) > 0:
        return dst
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    path = f"papers/{cycle}/{subject_id}/{year}/paper/{fileid}"
    url = (f"https://firebasestorage.googleapis.com/v0/b/{BUCKET}/o/"
           + urllib.parse.quote(path, safe="") + "?alt=media")
    try:
        with urllib.request.urlopen(url, timeout=120) as r, open(dst + ".part", "wb") as fh:
            while True:
                chunk = r.read(1 << 16)
                if not chunk:
                    break
                fh.write(chunk)
        os.replace(dst + ".part", dst)
        return dst
    except Exception as e:  # noqa: BLE001 — report + drop, never guess
        if os.path.exists(dst + ".part"):
            os.remove(dst + ".part")
        log(f"    download FAILED {fileid}: {e}")
        return None


# ─── PDF primitives ───────────────────────────────────────────────────────────

def line_groups(page):
    """get_text('words') grouped into lines, each sorted left→right."""
    lines = defaultdict(list)
    for w in page.get_text("words"):
        lines[(w[5], w[6])].append(w)
    for lw in lines.values():
        lw.sort(key=lambda w: w[0])
    return list(lines.values())


def is_blank(page):
    if re.sub(r"\d+", "", norm_text(page.get_text("text"))).strip() in BLANK_PAGE_TEXTS:
        return True
    if page.get_text("text").strip():
        return False
    if page.get_images():
        return False
    try:
        return len(page.get_drawings()) <= 3
    except Exception:  # noqa: BLE001
        return True


# ─── detectors: hits are (sort_key, printed_label, page0, x0, yFrac) ─────────
# sort_key orders questions across the doc: (section_index, number).

SECTION_TOKEN_RE = re.compile(r"([A-C])-(\d{1,2})\.?")


def det_section_token(doc):
    """'A-1.' / 'B-2' / 'C-3.' as the FIRST word of a left-margin line (DCG,
    Engineering-style sectioned papers)."""
    hits = []
    for pi, page in enumerate(doc):
        if page.rotation:
            continue
        H = page.rect.height
        for lw in line_groups(page):
            w = lw[0]
            m = SECTION_TOKEN_RE.fullmatch(deligature(w[4]))
            if m and w[0] < LEFT_MARGIN_X:
                sec, num = m.group(1), int(m.group(2))
                hits.append(((ord(sec) - ord("A"), num), f"{sec}-{num}", pi, w[0], w[1] / H))
    return hits


def det_question_word(doc):
    hits = []
    for pi, page in enumerate(doc):
        if page.rotation:
            continue
        H = page.rect.height
        for lw in line_groups(page):
            for i, w in enumerate(lw):
                word = deligature(w[4])
                if word not in ("Question", "QUESTION", "Ceist", "CEIST") or i + 1 >= len(lw):
                    continue
                m = re.fullmatch(r"(\d+)[.:]?", lw[i + 1][4])
                if m and w[0] < LEFT_MARGIN_X:
                    n = int(m.group(1))
                    hits.append(((0, n), str(n), pi, w[0], w[1] / H))
    return hits


def det_lead_int(doc):
    hits = []
    for pi, page in enumerate(doc):
        if page.rotation:
            continue
        H = page.rect.height
        for lw in line_groups(page):
            w = lw[0]
            m = re.fullmatch(r"(\d{1,2})\.", w[4])
            if m and w[0] < LEAD_INT_X:
                n = int(m.group(1))
                hits.append(((0, n), str(n), pi, w[0], w[1] / H))
    return hits


def det_sectioned_lead_int(doc):
    """Section-aware det_lead_int: a bare left-margin 'N.' whose question number
    RESTARTS per section (language reading papers). Scans pages in print order
    maintaining a current section index; a left-margin line matching one of the
    active subject's SUBJECT_SECTION_PATTERNS opens the next section, and each
    bare 'N.' emits sort_key=(section_index, N) — so 'Ceist 1' under text B is a
    distinct question from 'Ceist 1' under text A (build_anchors keeps both;
    each section's run is validated contiguous 1..N by the unchanged gates).

    INERT unless the run is explicitly pinned to this grammar: when
    SECTIONED_ENABLED is False (auto mode, or any other pin) there are no section
    patterns, section_index stays 0, and the output is byte-identical to
    det_lead_int — so registering this detector cannot regress any subject."""
    pats = SUBJECT_SECTION_PATTERNS.get(ACTIVE_SUBJECT) if SECTIONED_ENABLED else None
    hits = []
    sec = 0
    for pi, page in enumerate(doc):
        if page.rotation:
            continue
        H = page.rect.height
        for lw in line_groups(page):
            w = lw[0]
            if pats and w[0] < LEFT_MARGIN_X:
                line = deligature(" ".join(x[4] for x in lw))
                if any(p.match(line) for p in pats):
                    sec += 1
                    continue
            m = re.fullmatch(r"(\d{1,2})\.", w[4])
            if m and w[0] < LEAD_INT_X:
                n = int(m.group(1))
                # section 0 (no header seen yet / detector inert) keeps the bare
                # 'N' label so the output is byte-identical to det_lead_int;
                # later sections carry an 'A-1'/'B-2' style id in the label.
                if sec == 0:
                    lab = str(n)
                else:
                    lab = f"{chr(ord('A') + sec)}-{n}" if sec < 26 else f"S{sec}-{n}"
                hits.append(((sec, n), lab, pi, w[0], w[1] / H))
    return hits


def det_armed_sectioned(doc):
    """Armed section-aware det_lead_int (TV-8). A bare left-margin 'N.' is a
    question ONLY while detection is ARMED — armed by a question-block header
    and disarmed by a passage / grammar / matching-task header (per subject in
    SUBJECT_ARMED_PATTERNS). So the numbered passage paragraphs ABOVE the
    questions, and the numbered sub-lists INSIDE a question, never emit hits —
    the decoy numbering that defeated det_sectioned_lead_int (TV-7). A section
    boundary bumps the section index, so each reading text's 1..N run is a
    distinct key (build_anchors keeps 'A-1' and 'B-1' apart, exactly as
    det_section_token does for DCG); make_sidecar still renumbers `n`
    sequentially.

    INERT unless the run is explicitly pinned to this grammar: when
    ARMED_ENABLED is False the config is None, detection starts ARMED, the
    section index stays 0 and every label is the bare 'N' — byte-identical to
    det_lead_int, so registering this detector cannot regress any subject.

    TV-12 extensions (both keyed by OPTIONAL config keys, so configs without
    them — german, irish HL, geography — behave exactly as before):
      • 'always_armed' — papers with no arm header (irish OL P2 prints its
        questions directly under the passage): detection starts ARMED and
        'open' headers only bump the section index instead of disarming.
      • 'question' — row-shape regex: the bare 'N.' emits a hit only if the
        text following it in the same VISUAL ROW matches (irish OL P2:
        '^\\(a\\)' — questions are 'N. (a) …', passage paragraphs 'N. <prose>').
        The row is assembled from the page's word list because the PDFs often
        split 'N.' and '(a) …' into separate line groups."""
    cfg = armed_cfg_for(ACTIVE_SUBJECT, ACTIVE_FILEID)
    # Header-eligibility x-gate: per-subject override for papers whose PART/CUID
    # headers print just past LEFT_MARGIN_X (geography 2017 OL EV / 2013 OL IV).
    # Applies ONLY to arm/open/disarm header lines — never to question markers.
    hdr_x = cfg.get("margin", LEFT_MARGIN_X) if cfg else LEFT_MARGIN_X
    qshape = cfg.get("question") if cfg else None
    always = bool(cfg.get("always_armed")) if cfg else False
    hits = []
    sec = 0
    # inert → always armed (== det_lead_int); pinned → wait for an arm header,
    # unless the config declares there is none (always_armed).
    armed = cfg is None or always
    for pi, page in enumerate(doc):
        if page.rotation:
            continue
        H = page.rect.height
        # The arm/disarm state machine needs TRUE reading order (a header must
        # arm/disarm the lines that visually follow it), but line_groups yields
        # word-stream order. When PINNED, walk each page top→bottom, left→right
        # so 'Ceisteanna' arms only the questions BELOW it, not a passage
        # paragraph that happens to precede it in the word stream. When INERT
        # (cfg None) keep the raw line_groups order so the emitted hit list is
        # byte-identical to det_lead_int (proven zero-regression).
        lines = line_groups(page)
        if cfg is not None:
            lines = sorted(lines, key=lambda lw: (round(lw[0][1], 1), lw[0][0]))
        words = page.get_text("words") if qshape is not None else None
        for lw in lines:
            w = lw[0]
            if cfg and w[0] < hdr_x:
                line = deligature(" ".join(x[4] for x in lw))
                if any(p.match(line) for p in cfg["open"]):
                    sec += 1
                    armed = always
                    continue
                if any(p.search(line) for p in cfg["disarm"]):
                    armed = False
                    continue
                if any(p.search(line) for p in cfg["arm"]):
                    armed = True
                    continue
            if not armed:
                continue
            m = re.fullmatch(r"(\d{1,2})\.", w[4])
            if m and w[0] < LEAD_INT_X:
                if qshape is not None and not qshape.match(_row_rest(words, w)):
                    continue
                n = int(m.group(1))
                # section 0 (inert / before any section) keeps the bare 'N'
                # label so the output is byte-identical to det_lead_int.
                if sec == 0:
                    lab = str(n)
                else:
                    lab = f"{chr(ord('A') + sec)}-{n}" if sec < 26 else f"S{sec}-{n}"
                hits.append(((sec, n), lab, pi, w[0], w[1] / H))
    return hits


def _row_rest(words, w):
    """Text that VISUALLY follows word `w` on its row: every page word whose
    top is within 3pt of w's and that starts right of w, joined left→right.
    Row assembly must come from the raw word list, not w's line group — the
    reading papers often split a question row ('5.' + '(a) Cén …') into
    separate line groups (TV-12, `question` row-shape key)."""
    same = sorted((x for x in words if abs(x[1] - w[1]) < 3.0 and x[0] > w[0]),
                  key=lambda x: x[0])
    return deligature(" ".join(x[4] for x in same))


def armed_section_boundaries(doc):
    """Positions (page0, yFrac) of the active armed subject's 'open' headers —
    each is the START of a new reading section / passage, hence the END of the
    PREVIOUS section's questions (the "island" boundary). These feed the
    per-question crop-END (endP/endY) so a reading section's last question stops
    at the following passage instead of bleeding across it (TV-9).

    Empty unless the run is pinned to armed_sectioned AND the subject has an
    armed config — so it changes nothing for any other run. Mirrors the 'open'
    branch of det_armed_sectioned exactly (same top→bottom line order, same
    left-margin gate, same patterns, same fileid-scoped config)."""
    cfg = armed_cfg_for(ACTIVE_SUBJECT, ACTIVE_FILEID)
    if not cfg:
        return []
    hdr_x = cfg.get("margin", LEFT_MARGIN_X)  # same header x-gate as the detector
    bounds = []
    for pi, page in enumerate(doc):
        if page.rotation:
            continue
        H = page.rect.height
        lines = sorted(line_groups(page), key=lambda lw: (round(lw[0][1], 1), lw[0][0]))
        for lw in lines:
            w = lw[0]
            if w[0] < hdr_x:
                line = deligature(" ".join(x[4] for x in lw))
                if any(p.match(line) for p in cfg["open"]):
                    bounds.append((pi, w[1] / H))
    return bounds


def clamp_ends(anchors, boundaries):
    """{anchor_index: (page0, yFrac)} — the section boundary that ENDS each
    last-in-island (or final) question's content. For anchor i, the first
    boundary strictly after it; kept only when that boundary falls before the
    NEXT anchor (i.e. i really is the last question of its island) or i is the
    last anchor (a trailing writing/production section). Empty without
    boundaries — so non-island papers are untouched."""
    ends = {}
    if not boundaries:
        return ends
    bounds = sorted(boundaries)
    apos = [(a[2], a[4]) for a in anchors]
    for i, pos in enumerate(apos):
        nxt = apos[i + 1] if i + 1 < len(apos) else None
        b = next((bp for bp in bounds if bp > pos), None)
        if b is None:
            continue
        if nxt is None or b < nxt:
            ends[i] = b
    return ends


DETECTORS = {
    "section_token": det_section_token,
    "question": det_question_word,
    "lead_int": det_lead_int,
    "sectioned_lead_int": det_sectioned_lead_int,
    "armed_sectioned": det_armed_sectioned,
}


# ─── anchor building + gates ──────────────────────────────────────────────────

def build_anchors(doc, hits):
    """hits → (anchors, expected, reasons, gaps). anchors = [(sort_key, label,
    page0, x0, yFrac)] deduped/ordered; expected counts the contiguous
    first..last run per section (the run may start above 1 — biology
    Section-C docs legitimately print 11..17). gaps=True flags any missing
    number inside a run: that is a missing MARKER (dotless-header class), so
    the paper-level numbering gate hard-drops it."""
    reasons = []
    first = {}
    for h in sorted(hits, key=lambda h: (h[2], h[4])):  # print order
        first.setdefault(h[0], h)                        # first occurrence wins

    by_sec = defaultdict(list)
    for key in sorted(first):
        by_sec[key[0]].append(key[1])

    anchors, expected, gaps = [], 0, False
    for sec in sorted(by_sec):
        nums = by_sec[sec]
        lo, top = min(nums), max(nums)
        expected += top - lo + 1
        missing = sorted(set(range(lo, top + 1)) - set(nums))
        if missing:
            gaps = True
            reasons.append(f"section {sec}: missing question number(s) {missing} "
                           f"in the {lo}..{top} run")
        for n in range(lo, top + 1):
            if n in nums:
                anchors.append(first[(sec, n)])

    anchors.sort(key=lambda a: a[0])
    # print order must match question order — else the layout defeats the
    # anchor→next-anchor crop derivation and every question is in doubt.
    pos = [(a[2], a[4]) for a in anchors]
    if any(pos[i] >= pos[i + 1] for i in range(len(pos) - 1)):
        return [], expected, reasons + ["anchors not monotonic in print order"], gaps
    return anchors, expected, reasons, gaps


def stray_marker_check(anchors, hits):
    """Every raw detector hit must sit inside its own question's print span — an
    out-of-place duplicate (e.g. a restarted 'Section B, Q1' after Q10) would
    mean the run we anchored is NOT the whole paper. Returns None when clean,
    else a reason. Used by both the document-tiling proof and the armed-island
    path (TV-9b) — it is the one integrity check both share."""
    apos = [(a[2], a[4]) for a in anchors]
    akey = {a[0]: i for i, a in enumerate(anchors)}
    for key, label, pi, _x, y in hits:
        i = akey.get(key)
        if i is None:
            return f"stray marker {label!r} on page {pi + 1} outside the anchored run"
        hi = apos[i + 1] if i + 1 < len(apos) else None
        if (pi, y) < apos[i] or (hi is not None and (pi, y) >= hi):
            return (f"duplicate marker {label!r} on page {pi + 1} out of position "
                    f"(numbering restart?)")
    return None


def contiguity_proof(doc, anchors, hits, content_pages):
    """Prove the anchored numbering is the paper's ONE question sequence, so
    anchor-less pages between/after anchors are continuation pages (answer
    booklets, multi-page questions) rather than evidence of a missed marker.
    Preconditions already held by the caller: no gaps in the per-section runs
    and monotonic print order. Returns None when the proof holds, else why it
    fails (→ the caller falls back to the strict blanket gates)."""
    stray = stray_marker_check(anchors, hits)
    if stray:
        return stray

    apos = [(a[2], a[4]) for a in anchors]
    # The anchors must plausibly tile the document: a small contiguous run of
    # look-alike tokens (a numbered list inside one question) must not pass
    # itself off as the paper's question sequence.
    first_p, last_p = apos[0][0], apos[-1][0]
    lead = sum(1 for pi in range(first_p) if not is_blank(doc[pi]))
    if lead > MAX_LEAD_PAGES:
        return f"{lead} content pages before the first anchor (> {MAX_LEAD_PAGES})"

    # Trailing answer-space tolerance. Booklet docs bind a large answer section
    # AFTER the last question (biology Section-A&B docs carry ~28 pages of
    # Section-C answerbook after Q10). Such pages are answer space, not hidden
    # questions — provably so when NO detector (any grammar) finds a
    # question-start marker on them. So the tiling floor measures the anchored
    # span against content pages only up to the last page that bears a marker
    # (of any grammar); a marker-free tail is excluded and cannot penalise
    # coverage. If the tail DOES carry a cross-grammar marker (a possible
    # missed question in another numbering), that page stays in the denominator
    # and the floor still bites — the safe direction. This can only RAISE the
    # ratio vs. the whole-doc denominator, so no previously-passing paper
    # regresses.
    marked = set()
    for det in DETECTORS.values():
        for h in det(doc):
            marked.add(h[2])
    last_marked = max(marked) if marked else last_p
    tiling_end = max(last_p, last_marked)
    tiling_pages = sum(1 for pi in range(tiling_end + 1) if not is_blank(doc[pi]))
    if tiling_pages and (last_p - first_p + 1) / tiling_pages < MIN_ANCHOR_SPAN:
        return (f"anchored span {last_p - first_p + 1}p covers < "
                f"{MIN_ANCHOR_SPAN:.0%} of {tiling_pages} content pages up to the "
                f"last question marker")
    return None


def paper_gates(doc, anchors, expected, reasons, gaps, hits, boundaries=None):
    """Paper-level honesty gates. Returns (drop_reason, notes): drop_reason is
    None when the paper passes; notes carry report-worthy judgment calls
    (continuation pages tolerated, offset numbering, …)."""
    notes = []
    if len(anchors) < MIN_QUESTIONS:
        return (f"only {len(anchors)} anchored questions (<{MIN_QUESTIONS}): "
                + "; ".join(reasons), notes)

    # Numbering gate: a gap inside a run is a missing MARKER — the previous
    # question's derived crop would silently swallow the missed question
    # (2011 OL maths P2 IV prints Q4's header without the dot). Hard drop.
    if gaps:
        return ("numbering not contiguous — " + "; ".join(reasons)
                + f" ({len(anchors)}/{expected} anchored)", notes)

    # Span gate: the viewer's paperRegionFor refuses a crop spanning more
    # than MAX_PAGES pages — such a sidecar would fail CI. For section-restart
    # island papers, a last-in-island question's crop ENDS at the next section
    # boundary (its clamp), not at the far next anchor across the passage, so it
    # is measured to that clamp instead (TV-9 island-aware gating).
    ends = clamp_ends(anchors, boundaries)
    for i, (a, b) in enumerate(zip(anchors, anchors[1:])):
        end_page = ends[i][0] if i in ends else b[2]
        if end_page - a[2] > MAX_PAGES:
            return (f"Q{a[1]} runs {end_page - a[2]} pages to its crop end "
                    f"(> {MAX_PAGES}) — the viewer would refuse the crop", notes)

    first = anchors[0][0]
    if first[1] != 1:
        notes.append(f"numbering starts at {anchors[0][1]}")

    # Armed-island gating (TV-9b). A section-restart reading paper's questions
    # occupy small "islands" (each text's Ceisteanna / Fragen) inside a much
    # larger document of passages, answer space and non-anchored essay sections.
    # contiguity_proof's document-tiling heuristics (lead-page cap, anchored-span
    # floor) assume questions tile the whole paper and would wrongly drop these.
    # Those heuristics exist to stop a CONTEXT-FREE detector mistaking a decoy
    # list for the question sequence — which the armed detector already precludes
    # (arm/disarm headers + the qa_verify marker re-check). The ONLY thing that
    # could make a WRONG crop here is a last-in-island question with no crop-end
    # clamp bleeding into the next island; so we still run the shared stray-marker
    # integrity check AND require every island boundary to be clamped. Given both,
    # tolerating the non-anchor pages is safe: a tolerated page can only cost a
    # MISSING question, never a wrong crop (the clamp stops every crop short of it).
    if ARMED_ENABLED and boundaries:
        stray = stray_marker_check(anchors, hits)
        if stray:
            return (stray, notes)
        for i in range(len(anchors) - 1):
            crosses_island = anchors[i][0][0] != anchors[i + 1][0][0]
            if crosses_island and i not in ends:
                return (f"island boundary after {anchors[i][1]} has no crop-end "
                        f"clamp — its crop could bleed into {anchors[i + 1][1]}", notes)
        pages_with = {a[2] for a in anchors}
        n_sections = len({a[0][0] for a in anchors})
        tol = sum(1 for pi in range(len(doc))
                  if pi not in pages_with and not is_blank(doc[pi]))
        notes.append(f"armed-island paper: {len(anchors)} question(s) across "
                     f"{n_sections} reading section(s); {tol} passage/answer/"
                     f"other-section page(s) tolerated (every island crop-end "
                     f"clamped — no bleed)")
        return (None, notes)

    pages_with = {a[2] for a in anchors}
    first_p, last_p = min(pages_with), max(pages_with)
    content_pages = sum(1 for pg in doc if not is_blank(pg))

    proof_fail = contiguity_proof(doc, anchors, hits, content_pages)
    if proof_fail is None:
        # Contiguity proven: anchor-less content pages between/after anchors
        # are continuation pages — count them for the report, don't gate.
        holes = sum(1 for pi in range(first_p, last_p + 1)
                    if pi not in pages_with and not is_blank(doc[pi]))
        tail = sum(1 for pi in range(last_p + 1, len(doc)) if not is_blank(doc[pi]))
        if holes or tail:
            notes.append(f"contiguity-verified booklet: {holes} continuation "
                         f"page(s) between anchors, {tail} after the last")
        return (None, notes)

    # Strict fallback (numbering not PROVABLY one run): the original blanket
    # hole/tail gates.
    notes.append(f"contiguity unproven: {proof_fail}")
    for pi in range(first_p, last_p + 1):
        if pi in pages_with:
            continue
        if not is_blank(doc[pi]) and not doc[pi].rotation:
            return (f"content page {pi + 1} between anchors carries no anchor "
                    f"(missed question?) [{proof_fail}]", notes)
        if doc[pi].rotation:
            return (f"rotated page {pi + 1} between anchors (unrepresentable "
                    f"question?) [{proof_fail}]", notes)
    for pi in range(last_p + 1, len(doc)):
        page = doc[pi]
        if is_blank(page):
            continue
        t = norm_text(page.get_text("text"))
        if len(t) > MAX_TAIL_CHARS or SECTION_TOKEN_RE.search(page.get_text("text")):
            return (f"page {pi + 1} after the last anchor still carries content "
                    f"[{proof_fail}]", notes)
    return (None, notes)


def qa_verify(pdf_path, sidecar, grammar):
    """Independent per-question re-verification: re-open the PDF and require the
    printed marker text to be re-found at each anchor position. Any mismatch
    fails the WHOLE paper (the generator and verifier disagreeing = doubt)."""
    doc = fitz.open(pdf_path)
    det = DETECTORS[grammar]
    hits = det(doc)
    by_pos = {}
    for _, label, pi, _x, y in hits:
        by_pos.setdefault((pi, round(y, 3)), set()).add(label)
    for q in sidecar["q"]:
        want = q.get("label") or f"{q['n']}"
        found = by_pos.get((q["pP"] - 1, round(q["pY"][0], 3)), set())
        # tolerate rounding: scan nearby y keys on the same page
        if want not in found:
            near = {lab for (pi, y), labs in by_pos.items()
                    if pi == q["pP"] - 1 and abs(y - q["pY"][0]) < 0.004 for lab in labs}
            if want not in near:
                return f"Q{q['n']} ({want}): marker not re-found at page {q['pP']} y={q['pY'][0]}"
    return None


# ─── sidecar emit ─────────────────────────────────────────────────────────────

def component_of(fileid):
    m = re.match(r"^(LC|JC|LB)(\d{3})([A-Z])L?P([A-Z0-9]{3})(EV|IV|BV)\.pdf$", fileid, re.I)
    return m.group(4).upper() if m else ""


def make_sidecar(fileid, anchors, doc, boundaries=None):
    by_page = defaultdict(list)
    for a in anchors:
        by_page[a[2]].append(a[4])
    for pi in by_page:
        by_page[pi].sort()

    ends = clamp_ends(anchors, boundaries)  # {0-based anchor idx: (page0, yFrac)}

    qout = []
    for i, (_key, label, pi, _x, y) in enumerate(anchors, start=1):
        nxt = next((yf for yf in by_page[pi] if yf > y + 1e-6), 1.0)
        q = {
            "n": str(i),
            "pP": pi + 1,
            "pY": [round(y, 4), round(nxt, 4)],
            "region": [{"p": 1}],
            "mode": "pagejump",
            "conf": PAGEJUMP_CONF,
        }
        if label != str(i):
            q["label"] = label
        # Section-restart "island" papers: pin the crop-END at the next section
        # boundary so this question stops at the following passage/section
        # instead of running to the next island's first question (TV-9).
        end = ends.get(i - 1)
        if end is not None:
            q["endP"] = end[0] + 1
            q["endY"] = round(end[1], 4)
        qout.append(q)
    return {
        "v": SIDECAR_V,
        "paperFileid": fileid,
        "schemeFileid": "",     # paper-only: NO scheme mapping claimed
        "component": component_of(fileid),
        "band": [1, 1],         # empty band — nothing indexes into a scheme
        "copyright": COPYRIGHT,
        "paperOnly": 1,
        "q": qout,
    }


# ─── QA render (ports components/PaperTrail/paperRegion.ts) ──────────────────

TOP_PAD = 0.008
MAX_PAGES = 3
MIN_TAIL = 0.03


def paper_region_for(qs, n):
    """Mirror of paperRegionFor in components/PaperTrail/paperRegion.ts."""
    ordered = sorted(qs, key=lambda q: (q["pP"], q["pY"][0]))
    idx = next((i for i, q in enumerate(ordered) if q["n"] == n), -1)
    if idx == -1:
        return None
    q = ordered[idx]
    y0 = max(0.0, min(1.0, q["pY"][0]) - TOP_PAD)

    # Explicit crop-END (section-restart island papers) — mirror of the TS
    # paperRegionFor branch: stop at (endP, endY) independent of the next anchor.
    endP, endY = q.get("endP"), q.get("endY")
    if isinstance(endP, int) and isinstance(endY, (int, float)):
        ey = min(1.0, max(0.0, endY))
        if endP < q["pP"] or (endP == q["pP"] and ey <= q["pY"][0] + 0.005):
            return None
        if endP - q["pP"] > MAX_PAGES:
            return None
        if endP == q["pP"]:
            return [{"p": q["pP"], "r": [0, y0, 1, ey]}]
        segs = [{"p": q["pP"], "r": [0, y0, 1, 1]}]
        for p in range(q["pP"] + 1, endP):
            segs.append({"p": p, "r": [0, 0, 1, 1]})
        if ey > MIN_TAIL:
            segs.append({"p": endP, "r": [0, 0, 1, ey]})
        return segs

    nxt = ordered[idx + 1] if idx + 1 < len(ordered) else None
    if nxt is None:
        y1 = q["pY"][1] if q["pY"][1] > y0 + 0.01 else 1.0
        return [{"p": q["pP"], "r": [0, y0, 1, min(1.0, y1)]}]
    if nxt["pP"] < q["pP"] or (nxt["pP"] == q["pP"] and nxt["pY"][0] <= q["pY"][0] + 0.005):
        return None
    span = nxt["pP"] - q["pP"]
    if span > MAX_PAGES:
        return None
    if span == 0:
        return [{"p": q["pP"], "r": [0, y0, 1, min(1.0, nxt["pY"][0])]}]
    segs = [{"p": q["pP"], "r": [0, y0, 1, 1]}]
    for p in range(q["pP"] + 1, nxt["pP"]):
        segs.append({"p": p, "r": [0, 0, 1, 1]})
    tail = min(1.0, nxt["pY"][0])
    if tail > MIN_TAIL:
        segs.append({"p": nxt["pP"], "r": [0, 0, 1, tail]})
    return segs


def qa_render(pdf_path, sidecar, out_dir, n_samples, rng, year):
    """Render N derived question crops to PNG for visual QA. The FIRST and
    LAST questions are always in the sample (the crop-start and the
    last-question/tail derivations are the two highest-risk classes); the
    rest is a random draw."""
    doc = fitz.open(pdf_path)
    qs = sidecar["q"]
    os.makedirs(out_dir, exist_ok=True)
    sample = [qs[0]]
    if len(qs) > 1:
        sample.append(qs[-1])
    middle = qs[1:-1]
    if len(sample) < n_samples and middle:
        sample.extend(rng.sample(middle, min(n_samples - len(sample), len(middle))))
    sample = sample[:max(n_samples, 1)]
    rendered = []
    for q in sample:
        region = paper_region_for(qs, q["n"])
        if not region:
            continue
        pixmaps = []
        for seg in region:
            page = doc[seg["p"] - 1]
            r = seg["r"]
            clip = fitz.Rect(r[0] * page.rect.width, r[1] * page.rect.height,
                             r[2] * page.rect.width, r[3] * page.rect.height)
            pixmaps.append(page.get_pixmap(clip=clip, dpi=100))
        w = max(p.width for p in pixmaps)
        h = sum(p.height for p in pixmaps)
        combo = fitz.Pixmap(fitz.csRGB, fitz.IRect(0, 0, w, h))
        combo.clear_with(255)
        y = 0
        for p in pixmaps:
            # A clipped Pixmap keeps its clip origin (p.x/p.y = the clip's
            # top-left in page pixels); Pixmap.copy works in the SHARED
            # coordinate space of both pixmaps, so without re-origining the
            # copy rect misses the source data entirely (blank/misstacked
            # renders). Re-origin each segment to its slot in the stack.
            p.set_origin(0, y)
            combo.copy(p, fitz.IRect(0, y, p.width, y + p.height))
            y += p.height
        label = q.get("label", q["n"]).replace("/", "_")
        fn = os.path.join(out_dir, f"{year}-{sidecar['paperFileid']}-Q{q['n']}-{label}.png")
        combo.save(fn)
        rendered.append(fn)
    return rendered


# ─── main ─────────────────────────────────────────────────────────────────────

def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    ap.add_argument("subject")
    ap.add_argument("--grammar", default=None,
                    help="pin a detector (default: SUBJECT_GRAMMAR pin, else auto)")
    ap.add_argument("--years", default="2010-2025")
    ap.add_argument("--qa-render", type=int, default=0, metavar="N",
                    help="render N random derived crops per anchored paper")
    ap.add_argument("--seed", type=int, default=562)
    ap.add_argument("--dry-run", action="store_true", help="no files written")
    args = ap.parse_args()

    y0, y1 = (int(x) for x in args.years.split("-"))
    years = set(range(y0, y1 + 1))
    cycle, rows = load_subject_index(args.subject)
    rows = [r for r in rows if r["year"] in years]
    grammar_pin = args.grammar or SUBJECT_GRAMMAR.get(args.subject)
    rng = random.Random(args.seed)

    # det_sectioned_lead_int / det_armed_sectioned only consult their pattern
    # tables when this run is explicitly pinned to them — otherwise each is a
    # no-op clone of lead_int.
    global ACTIVE_SUBJECT, ACTIVE_FILEID, SECTIONED_ENABLED, ARMED_ENABLED
    ACTIVE_SUBJECT = args.subject
    SECTIONED_ENABLED = grammar_pin == "sectioned_lead_int"
    ARMED_ENABLED = grammar_pin == "armed_sectioned"

    log(f"paper-anchors: {args.subject} ({cycle}) — {len(rows)} papers, "
        f"grammar {grammar_pin or 'auto'}")

    report, shipped, dropped, skipped = [], 0, 0, 0
    for r in sorted(rows, key=lambda r: (-r["year"], r["level"], r["lang"], r["fileid"])):
        tag = f"{r['year']} {r['level']}/{r['lang']} {r['label']} {r['fileid']}"
        if r["hasAnswers"]:
            skipped += 1
            report.append((tag, "SKIP", "already has a verified Storage sidecar"))
            continue
        pdf_path = fetch_paper(cycle, args.subject, r["year"], r["fileid"])
        if not pdf_path:
            dropped += 1
            report.append((tag, "DROP", "download failed"))
            continue

        # Fileid-scoped armed configs (TV-12) key off the CURRENT paper; the
        # global stays set through qa_verify/qa_render for this iteration.
        ACTIVE_FILEID = r["fileid"]
        doc = fitz.open(pdf_path)
        cands = [grammar_pin] if grammar_pin else list(DETECTORS)
        best = None  # (grammar, anchors, expected, reasons, gaps, hits)
        for g in cands:
            hits = DETECTORS[g](doc)
            anchors, expected, reasons, gaps = build_anchors(doc, hits)
            if best is None or len(anchors) > len(best[1]):
                best = (g, anchors, expected, reasons, gaps, hits)
        g, anchors, expected, reasons, gaps, hits = best
        # Section boundaries feed island-aware gating + per-question crop-ends;
        # empty for every non-armed grammar, so this is inert elsewhere (TV-9).
        boundaries = armed_section_boundaries(doc) if g == "armed_sectioned" else None
        drop, notes = paper_gates(doc, anchors, expected, reasons, gaps, hits, boundaries)
        if drop:
            dropped += 1
            report.append((tag, "DROP", drop))
            continue

        sidecar = make_sidecar(r["fileid"], anchors, doc, boundaries)
        qa_fail = qa_verify(pdf_path, sidecar, g)
        if qa_fail:
            dropped += 1
            report.append((tag, "DROP", f"QA re-verify failed: {qa_fail}"))
            continue

        if not args.dry_run:
            ydir = os.path.join(PUBLIC_OUT, str(r["year"]))
            os.makedirs(ydir, exist_ok=True)
            with open(os.path.join(ydir, f"{r['fileid']}.json"), "w", encoding="utf-8") as fh:
                json.dump(sidecar, fh, ensure_ascii=False, sort_keys=True,
                          separators=(",", ":"))
        rendered = []
        if args.qa_render:
            rdir = os.path.join(OUT_DIR, "qa-render", args.subject)
            rendered = qa_render(pdf_path, sidecar, rdir, args.qa_render, rng, r["year"])
        labels = ",".join(q.get("label", q["n"]) for q in sidecar["q"])
        detail = f"{len(sidecar['q'])}q [{labels}] via {g}"
        for note in notes:
            detail += f" · {note}"
        if rendered:
            detail += f" · {len(rendered)} QA crops"
        shipped += 1
        report.append((tag, "ANCHORED", detail))

    os.makedirs(OUT_DIR, exist_ok=True)
    rep_path = os.path.join(OUT_DIR, f"paper-anchors-{args.subject}-report.md")
    with open(rep_path, "w", encoding="utf-8") as f:
        f.write(f"# Paper anchors — {args.subject}\n\n")
        f.write(f"**{shipped} anchored · {dropped} dropped · {skipped} skipped "
                f"(already sidecar'd)** of {len(rows)} papers\n\n")
        f.write("| paper | status | detail |\n|---|---|---|\n")
        for tag, status, detail in report:
            f.write(f"| {tag} | {status} | {detail} |\n")
    log(f"  {shipped} anchored · {dropped} dropped · {skipped} skipped")
    log(f"  → {os.path.relpath(rep_path, REPO)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
