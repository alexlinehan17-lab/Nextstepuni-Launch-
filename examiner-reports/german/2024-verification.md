# German — Examiner's Chair second-year verification (2024 vs 2025)

**Purpose.** Second-year stability check for the marking rules taught in
`data/examinersChair/german.ts`. Those sessions cite the **SEC LC German HL
marking scheme 2025** (`examiner-reports/german/2025-marking-scheme.*`). This
document verifies each load-bearing rule against a **different year** — the
**SEC LC German HL marking scheme 2024** — to confirm the rules are standing
conventions, not one-year artefacts.

## Second source

- File: `examiner-reports/german/2024-marking-scheme.pdf` (+ `.md` extraction)
- Source: State Examinations Commission, Leaving Certificate 2024 Marking
  Scheme, German, Higher Level.
- Retrieved: 2026-07-06 from the educateplus.ie mirror
  (`https://www.educateplus.ie/sites/default/files/storage/German%20HL_1.pdf`),
  1.53 MB, 32 pages. Cover page confirms "Leaving Certificate 2024 … Marking
  Scheme … Higher Level … German".
- Extraction: PyPDF2 with `<!-- page N -->` markers. Page numbers below are PDF
  page numbers (the printed page number equals the PDF page number in the 2024
  file; in the 2025 file the PDF page runs ~2 ahead of the printed page — hence
  the two schemes cite the same rule at slightly different page numbers, which
  is expected and not a discrepancy).

## Standing-rule front matter (both years, verbatim)

Two pieces of front matter make several of these rules **year-stable by
construction** — they are general scheme conventions, not question details:

- **General instructions**, 2025 p.[3] / 2024 p.3:
  *"Where answers are in the language other than specified: award half marks."*
- **Annotations table**, 2025 p.[4] / 2024 p.4 (identical wording):
  *"Half mark penalty for answers in language not specified / extraneous
  material / quotation without manipulation where manipulation required"* and a
  separate *"Lower Expression"* annotation.

Counter-caveat, also in both years (2025 p.[2] / 2024 p.2, "Future Marking
Schemes"): *"the details of the marking of a particular type of question may
change … aspects of the structure, detail and application of the marking scheme
… are subject to change from one year to the next without notice."* This is why
an empirical two-year check matters. The check below finds every cited rule
**identical** across 2024 and 2025.

## Rule-by-rule verification

| # | Rule (as taught in german.ts) | Cited in german.ts (2025) | Found in 2024 source (page) | Verdict | Note |
|---|-------------------------------|---------------------------|------------------------------|---------|------|
| GE1 | **Lower-E length gate** on written production: if content ≤ 12 **or** answer < 100 words, Expression is marked out of 18 not 25. | p.[20] (Schriftliche Produktion, "Marking Written Expression") | **p.19**, verbatim: *"If the content mark is 12 or less, or the answer is too short (less than 100 words), mark expression out of 18 … (Lower E)."* Same 4-band scale (0–4/0–6 … 14–18/20–25). | **STABLE** | Thresholds (12 / 100 words / out of 18) identical to the word. Sits in the standing "Marking Written Expression in Schriftliche Produktion" section. NB there is a *parallel* Lower-E gate for the shorter Äußerung task (content ≤ 8 or < 60 words → out of 7) — also identical in both years (2025 p.[15] / 2024 p.15); german.ts teaches the 100-word/Schriftliche Produktion one, which is the correct pairing. |
| GE2 | **Unmanipulated quotation = half marks** in comprehension (and extraneous material = half marks). | p.[10] (half marks for unmanipulated quotation) | **p.5** and **p.10** comprehension headers, verbatim: *"quotation without manipulation where manipulation required / containing extraneous material: half marks. Full marks for manipulated parts."* Plus the standing annotation on **p.4**. | **STABLE** | Appears (a) as a standing annotation (p.4) and (b) repeated at the head of every Leseverständnis text. Year-stable by construction. |
| GE3 | **Tense-critical comprehension**: for a past-events question, a present-tense answer scores 0 ("Present Tense = 0"). | p.[5] (tense-critical marking, Present Tense = 0) | **p.5**, Frage 1(b) and 1(c): explicit *"(Present Tense = 0)"* annotations on past-frame questions (Arno Geiger's flat/why he lived there). 2025 used the same *"(NB: Present Tense = 0)"* on its Frage 1(a). | **STABLE (convention)** | This is a **per-question annotation**, applied to whichever items are past-framed that year — it recurs every year but attaches to different questions. german.ts already frames it correctly and non-prescriptively: *"Some comprehension answers are tense-critical … where the scheme flags a question as tense-critical."* It does **not** claim tense is always decisive, so it remains accurate. No reframe needed. |
| GE4 | **Aural answer language flips per section**; a section answered in the wrong language is halved. | p.[23] (aural: language flips per section; half-marks penalty) | **p.20** First Part / Interview: *"Where answers are in German, award half marks"* (→ answer in English). **p.22** Second Part / Telephone: *"Where answers are in English/Irish, award half marks"* + *"Write down in German…"* (→ answer in German). | **STABLE** | Same per-section language pattern as 2025 (interview → English; phone note → German). Underpinned by the standing general instruction (p.3). german.ts's worked example (interview in English, phone-message note in German) matches both years exactly. |

## Conclusion

All four load-bearing rules cited by `data/examinersChair/german.ts` are
**STABLE** across two independent years (2024 and 2025):

- GE1 (Lower-E 100-word gate), GE2 (unmanipulated-lift half marks) and GE4
  (aural language-per-section half marks) are **standing scheme conventions** —
  they live in the general instructions / annotations front matter and/or the
  fixed "Marking Written Expression" sections, and are **verbatim identical**
  between 2024 and 2025.
- GE3 (Present Tense = 0) is a **recurring per-question annotation** rather than
  a blanket rule; german.ts already teaches it with the correct conditional
  framing ("where the scheme flags a question as tense-critical"), so it is
  accurate and year-safe as written.

Only the **page numbers** differ between the two schemes (expected — question
lengths shift the pagination). The rules themselves do not differ. **No changes
to `data/examinersChair/german.ts` are required.**
