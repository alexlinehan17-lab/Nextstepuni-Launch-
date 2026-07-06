# Examiner's Chair — Spanish HL: second-year (cross-year) rule verification

**Session file verified:** `data/examinersChair/spanish.ts`
**Rules cited in that file to:** SEC LC Spanish HL **2025** marking scheme (`examiner-reports/spanish/2025-marking-scheme.*`).
**Second/third source used for this check:**
- SEC LC Spanish HL **2024** marking scheme — `examiner-reports/spanish/2024-marking-scheme.pdf` / `.md` (primary cross-check).
- SEC LC Spanish HL **2023** marking scheme — `examiner-reports/spanish/2023-marking-scheme.pdf` / `.md` (corroborating third year).
- Both retrieved 2026-07-06 from the educateplus.ie SEC mirror; extracted with PyPDF2, `<!-- page N -->` markers = PDF pages, which coincide with the printed page numbers used in the citations.

**Method:** For each load-bearing rule in `spanish.ts`, locate the exact governing text in the 2024 scheme (and 2023 as a third data point), confirm the page number still matches the citation, and classify STABLE / DIFFERS / UNCONFIRMED. The 2025 scheme's own standing-rules note (p.2, "Future Marking Schemes": "the underlying assessment principles remain the same … aspects of structure, detail and application … are subject to change") frames what counts as a year-stable *principle* vs. a year-specific *detail*.

---

## Rule-by-rule result

| # | Rule (as taught in spanish.ts) | Cited in spanish.ts | 2024 source (page) | 2023 source (page) | Verdict | Note |
|---|---|---|---|---|---|---|
| Sp1 | On the written question (Q5), **no marks for phrases taken directly from the text** | p.9 | p.9: "No marks will be awarded for phrases taken directly from the text." (verbatim) | p.9: same verbatim | **STABLE** | Core assessment principle; identical wording 3 years running. The related prescribed-lit Q5 rule "No marks awarded for answers supported by reference to the extract" is also present in all three years (p.5). |
| Sp2 | **Content gates Language** — where no marks for Content, no marks for Language | p.9 | p.9: "Where no marks are awarded for Content 1, (i.e. effort totally irrelevant), no marks will be awarded for Language 2." (verbatim) | p.9: same verbatim | **STABLE** | Identical wording 3 years running; part of the Q5 marking guidelines block. |
| Sp3 | **Verbs must be correct** to reach the top band on Section C production units | p.10–11 | p.10: "Verbs must be correct for full marks." — stated in the Section C general guidelines and again in the Q1(a) DIALOGUE / (b) LETTER top-band (6 marks) criteria. Q2 (DIARY/NOTE) band scale on p.11. | p.10 (+p.11): same verbatim | **STABLE** | The verb-gate wording is unchanged across all three years. Band-scale structure (6-mark dialogue/letter units, 5-mark diary/note units) is also unchanged 2023→2025. |
| Sp4 | **Aural**: in the aural vocabulary-list items, **a wrong extra answer cancels a correct one** — so hedging with a second guess voids the mark | p.5 ("aural: wrong extra cancels a correct answer") | **Not found.** The 2024 aural section (Listening Comprehension, pp.12–14) contains no "wrong extra cancels a correct answer" rule. p.5 is Section A (written); its only "extra" rule is "No marks awarded if extra words are added. Exact transcription required" — which governs the *exact-transcription written* items, not the aural, and voids the whole item for extra words rather than cancelling one right answer against one wrong. | Same as 2024: no aural cancel rule; p.5 rule is the exact-transcription written rule only | **DIFFERS / UNCONFIRMED** | The cited mechanism is not in the scheme in *any* of the three years, and the p.5 reference points at a Section A written rule, not the aural. This is a citation/attribution problem, not cross-year drift — it is "stable" only in that all three years equally lack the cited rule. See reframe proposal below. |

---

## Standing-convention vs. year-specific classification

- **Sp1, Sp2, Sp3** are **standing conventions.** Each appears verbatim in the 2023, 2024 and 2025 schemes, in the same section, on the same printed page, and each is one of the "underlying assessment principles" the SEC note (p.2) says remain constant. Cross-year stability: **high confidence.** No reframe needed; the 2025 citation is safe to continue using, and is now corroborated by two further years.
- **Sp4** is **neither** a standing convention **nor** a correctly-cited year-specific detail — the "aural: a wrong extra answer cancels a correct one" rule cited to p.5 is absent from the Spanish HL scheme in 2023, 2024 and 2025. The only real p.5 rule is the exact-transcription rule for the written Section A finding-phrases questions.

---

## Proposed reframe (Sp4 only) — NOT applied to the session file

`data/examinersChair/spanish.ts` was **not edited** (per instructions). The following is proposed for a future maintainer to action in a change that also updates `compliance/evidence/examiners-chair.md`.

The issue: Sp4 attributes to the **aural** a "wrong extra cancels a correct one" rule and cites **p.5**, but no such rule exists in the aural section (pp.12–14) in any of 2023/2024/2025, and p.5 is Section A written. The defensible, year-stable rule that p.5 *does* support is the **exact-transcription** rule for the written finding-a-phrase questions: *"No marks awarded if extra words are added. Exact transcription required"* (p.5, Section A; the same rule also appears for the Section B transcription questions, e.g. p.7–8: "No marks awarded if words are added or omitted. Exact transcription required").

Two options for the maintainer:

**Option A — retarget Sp4 to the real, verifiable rule (recommended).** Recast the session from an "aural hedging" lesson to a "don't add extra words to a transcription answer" lesson, which is genuinely in the scheme.

- `cue`: `'Aural'` → `'Written comprehension (transcription)'`
- `question` (verbatim old): "A listening item asks for one detail. The candidate, unsure, writes two — one right, one wrong — hoping the extra covers them. In the aural vocabulary-list items, a wrong extra answer cancels a correct one. What does it score?"
  proposed new: "A transcription question asks the candidate to copy the exact phrase from the text that means X. The candidate writes the correct phrase but pads it with extra words to be safe. The rule is: exact transcription required, and no marks are awarded if extra words are added. What does it score?"
- `questionNote` (old): "…In the Spanish aural, hedging with an extra wrong answer in a list item cancels a correct one — the same trap as over-answering elsewhere."
  new: "…On the exact-transcription questions the scheme requires the exact phrase and awards no marks if extra words are added — padding a correct answer voids it."
- `scale.notes` (old): "In the aural list items, a wrong extra answer cancels a correct one." → "The transcription questions require the exact phrase; no marks are awarded if extra words are added."
- `scale.cite`: `MS('p.5 (aural: wrong extra cancels a correct answer)')` → `MS('p.5 (exact transcription: no marks if extra words added)')`
- `embodies.cite` / `takeaway.cite`: keep `p.5` (now correctly describing the Section A transcription rule).
- `takeaway.detail` (old): "Spanish aural list items cancel a correct answer with a wrong extra…" → "On Spanish exact-transcription questions the scheme requires the exact phrase and gives no marks if extra words are added — copy the phrase exactly, don't pad it."

**Option B — cut Sp4** if an aural-specific lesson is required and cannot be grounded, per the accreditation rule ("If a claim can't be backed by a verifiable source, reframe it … or cut it"). This would also require removing `SP4` from the `sessions` array and updating the `codex-es4` takeaway references.

Either way the file's header comment and `compliance/evidence/examiners-chair.md` claim record must be updated in the same change, and the removal/reframe appended to `data/cutContent.ts`.

---

## Files created by this verification

- `examiner-reports/spanish/2024-marking-scheme.pdf`
- `examiner-reports/spanish/2024-marking-scheme.md`
- `examiner-reports/spanish/2023-marking-scheme.pdf`
- `examiner-reports/spanish/2023-marking-scheme.md`
- `examiner-reports/spanish/2024-verification.md` (this file)

No shared files were edited (`data/examinersChair/spanish.ts`, `examiner-reports/README.md` left untouched).
