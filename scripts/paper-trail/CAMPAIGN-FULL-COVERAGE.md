# Answers campaign — "scheme published ⇒ chips" (started 2026-08-31)

Founder directive: every paper that has a marking scheme gets answer chips,
except the minor languages (keep French, German, Spanish, Irish; skip Russian,
Polish, Japanese, Italian, etc. for now). Quality bar unchanged: a chip must
open the right part of the scheme — precise maps only, render-verified per
profile, no proportional fallback (see README §Annual refresh item 6).

**Gap at kickoff (rebuilt index, minor languages excluded): 2,122 papers with a
scheme and no chips**, of 4,135 scheme-carrying papers (1,608 flagged).

## The classes, and what closes each

### A. The IV sweep (~700–800 papers) — biggest, most mechanical
Nearly every wave record says "Drops: IV (out of EV scope)" — the Irish-medium
universe was excluded by an early scope decision, not by infeasibility. The
2026 refresh proved IV maps verify cleanly (Physics OL IV, Physics & Chemistry
OL IV, Geography HL IV, Computer Science IV, Latin IV, Music listening IV all
render-verified and live). The Irish schemes mirror the EV layouts.
Work: run the generic engine + each bespoke script with `--langs IV` over
2010–2025 for every code whose EV layout is proven; render-QA per profile
batch; light the `(sid, level, 'iv')` profiles.
Prerequisites now in place: the clearing loop is lang/level-aware (an IV run
can no longer delete committed EV sidecars), and the corpus comes from OUR
Storage bucket (no SEC traffic).
Targets: Maths IV 99 · Art IV ~115 · Music IV 81 · Classical IV 52 ·
Technology IV 45 · Geography IV 38 · sciences IV ~60 · Business IV 28 ·
Ag Sci IV 28 · Accounting IV 26 · Home Ec IV 21 · RE IV 26 · Construction IV
32 · History HIV 13 · CS IV 10 · P&S IV 16 · Link Modules IV 21 · …

### B. Mainstream language completion (~250)
`lang_reading.py` covers FR/DE/ES reading sections for 2016–18 EV only.
Extend the per-paper specs to 2010–2026, both levels, EV+IV. Aural and
composition stay skipped (honest partial coverage, as shipped). English:
extend `english_p2.py` to OL (same grade-band + indicative-material shape)
and re-probe P1 comprehension (Section A may anchor; composition drops).

### C. Irish (83 papers) — new bespoke
All-IV by nature; the old "no EV" ⛔ was a category error. Páipéar 2
léamhthuiscint maps like the language reading tier; prós/filíocht indicative
blocks like Arabic's literature blocks; Páipéar 1 ceapadóireacht → the shared
essay-criteria block (wave-10 labelled-chip pattern). All-Irish marker tokens
(Ceist/C{n}/Freagra).

### D. Per-year drop-fills of lit subjects (~250)
Documented per-year drops to revisit with the modern engine + targeted guards:
Music "off-by-one/partial" (2018/2022 006 maps verified correct this session —
the engine CAN do composing years; find why others dropped) · Art H&A missing
years (hev:40!) · Technology/RE/Construction/CS/Accounting-OL/Ag-Sci year
gaps · Swedish non-monotonic year · Geography pre-2020 single-booklet years
(cover-anchor guard exists since CV wave — re-run) · History OL (the repeated
instruction list defeats first-marker banding — pin the band past it, like
hem_history.py did for Early Modern).

### E. New-spec 2026 restructures — content-matching bespoke (new tool)
Biology, Economics, Applied Maths, Construction, Chemistry HL, Accounting HL,
Business 032, PE 2023+: the scheme restates each question's TEXT but numbers
questions on its own plan (Biology paper Q6 = scheme "Question 12"). A
number-blind matcher — pair paper question text to the scheme block that
restates it (similarity over restated stems) — with the standing gates
(monotonic print order NOT required here; instead: every pairing must pass a
text-echo check, else drop the paper).

### F. Cannot have chips (documented, honest remainder)
- DCG (132): the paper side is a draw-on answer booklet — nothing to anchor a
  chip to (confirmed 2026-07-07). The scheme HAS per-question text; if a
  future wave adds question-paper components, revisit.
- JC visual/practical subjects (Graphics, Metalwork, TG, Art, Engineering…).
- Hebrew Studies (scheme carries no question-specific answers).
- LCA portfolio Tasks (no exam), aural papers (audio feature is a separate
  probe), LCA Graphics & Construction (project criteria, not per-Q).
- Same-day exceptions inside mappable subjects (e.g. Geography Part One
  1-page key) keep their documented drops.

## Order of work
1. **A** — corpus pull → IV runs in subject batches → per-profile render QA →
   light profiles → rebuild → upload → commit. (Batches sized so each lands
   verified; nothing ships unverified.)
2. **D** alongside A where the same corpus batch covers it.
3. **B**, then **C** (Irish is B's grammar + C's tokens).
4. **E** as its own tool with its own kill-skeptic QA.
5. Report F as the permanent, documented remainder.

Every batch: `verify_all.py` + `npx vitest run test/paperTrailAnswers.test.ts`
+ render spot-check (first/middle/last of ≥3 papers per profile) before its
profile lights. The autumn canary rules apply to every profile added here.
