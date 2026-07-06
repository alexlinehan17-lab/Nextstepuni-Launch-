# Examiner's Chair — Accounting: Second-Year Verification (2023 vs 2024)

**Purpose.** `data/examinersChair/accounting.ts` teaches four SEC Accounting marking
rules, cited to the **SEC LC Accounting HL/OL marking scheme 2024**. This document
tests whether those rules are *stable across a second year* by re-deriving each one
from a **different** year's scheme — the **2023** HL scheme (and, for the OL session,
the 2023 OL scheme).

## Sources used

| File | What it is |
|------|-----------|
| `examiner-reports/accounting/2024-marking-scheme.pdf/.md` | SEC LC Accounting **HL 2024** — the year the module cites (baseline). |
| `examiner-reports/accounting/2024-ol-marking-scheme.pdf/.md` | SEC LC Accounting **OL 2024** — baseline for the OL session. |
| `examiner-reports/accounting/2023-marking-scheme.pdf/.md` | SEC LC Accounting **HL 2023** — the second year (this verification). Retrieved 2026-07-06 from the educateplus.ie mirror (`LC Accounting 2023 HL.pdf`), 36 pp., genuine SEC document. |
| `examiner-reports/accounting/2023-ol-marking-scheme.pdf/.md` | SEC LC Accounting **OL 2023** — second year for the OL session. Retrieved 2026-07-06 (`Accounting 2023 OL.pdf`), 24 pp. |

Extraction: PyPDF2 with `<!-- page N -->` markers; disputed items cross-checked with
`pdfminer.six` and by rendering the page to an image (PyMuPDF) and reading it directly.

**Confidence: HIGH.** A genuine second-year SEC HL scheme (2023) and OL scheme (2023)
were retrieved and read in full; no logical-only fallback was needed.

---

## Rule-by-rule result

### AC1 — "The workings are the marks" (workmark / numbered-working system)

**Claim (HL):** Accounting is marked line-by-line; each adjusted figure is justified by
a **numbered working**, and the marks live in that working, awarded step-by-step (a shown
working banks each correct step even when the final figure is wrong; a bare wrong figure
with no working scores 0). Cited to 2024 HL **p.3, p.5**.

| Element | 2024 HL (baseline) | 2023 HL (second year) | Verdict |
|---|---|---|---|
| Per-figure workmarks `[n]` on each line | p.3 (Q1A, e.g. Sales `[3]`, Purchases N1 `[7]`) | p.3 (Q1A, Sales `[3]`, Purchases W2 `[9]`, closing stock W1 `[7]`) | **Stable** |
| Figures justified by a separate numbered working | "N-notes" (N1, N2 …) | "W-notes" (W1, W2 …), with a dedicated "Question 1 B **Workings**" page (p.8) | **Stable (letter differs — see caveat)** |
| Standing legend: "Correct element (n marks)" / "Refer to notes/workings" | p.34 annotation legend | p.33 annotation legend (identical wording) | **Stable** |

**Caveat (year-specific surface label):** the 2024 scheme prefixes workings **N**
(N1, N2…); the 2023 scheme prefixes them **W** (W1, W2…). The *concept* (a numbered
working carrying the marks) is identical; only the letter differs year to year. The
module's `cite` and grid `shorthand` use the 2024 "N-note" wording. Since the module
explicitly scopes its citation to the **2024** scheme, this is accurate as written, but
the "N-note" label is not itself year-stable. Optional year-neutral reframe below.

**Verdict: RULE STABLE.**

---

### AC2 — "Balancing is its own mark" (discrete Both-totals-correct presentation mark)

**Claim (HL):** The Balance Sheet carries a **discrete mark for both totals agreeing,
"marked with a `*`"** ("Both totals correct *"), independent of the individual line
figures; a single misplaced entry that breaks the balance forfeits it. Cited to 2024 HL
**p.4, p.27**.

| Element | 2024 HL (baseline) | 2023 HL (second year) | Verdict |
|---|---|---|---|
| A discrete mark for the two balance-sheet totals **agreeing**, separate from line figures | Present. `"Both totals correct *"` printed on the company Balance Sheet on **pp.4, 8, 27** | Present in substance: on the Goodwin plc Balance Sheet (printed p.26 / PDF p.20) the two agreeing totals `1,465,550 / 1,465,550` are connected by an examiner arrow annotation worth **`[1]`** | **Concept stable** |
| The exact label **"Both totals correct *"** | Appears verbatim (pp.4, 8, 27) | **Absent.** The string "Both totals" appears on **0** pages of the 2023 HL scheme (confirmed by PyPDF2 and pdfminer). The mark is shown as an arrow-annotation `[1]`, not spelled out. | **Label year-specific** |

**Finding:** the *rule* — "a balance sheet that actually balances earns a discrete,
separately-losable mark" — holds in both years. What is **not** year-stable is the
specific asterisked wording **"Both totals correct *"**: that phrasing is a 2024
presentation choice; 2023 awards the same mark as an unlabelled arrow annotation worth
`[1]`. The module quotes the literal `"Both totals correct *"` label three times and
treats it as a standing named mark. Proposed year-neutral reframe below.

**Verdict: RULE STABLE IN PRINCIPLE; the literal "Both totals correct *" label is
year-specific.**

---

### AC3 — "One error is marked once" (own-figure / transfer marking)

**Claim (HL):** Own-figure marking — an error is penalised where it happens, **once**;
correctly transferring your own (even wrong) figure earns the **full** transfer marks; a
**non-transfer** earns **half** marks; an incorrect transfer is penalised. Cited to 2024
HL **p.18, p.34**.

| Element | 2024 HL (baseline) | 2023 HL (second year) | Verdict |
|---|---|---|---|
| "-1 penalty" for Incorrect Calculation / Misplaced Figure / **Non Transfer** | Annotation legend, **p.34** | Annotation legend, **p.33**: "Minus one mark - Penalty, Incorrect Calculation, Misplaced Figure, **Non Transfer**" (identical) | **Stable** |
| "**Half marks awarded**" annotation | p.34 | p.33 (identical) | **Stable** |
| Own-figure marking applied throughout (figures carried into later statements) | Throughout (transfers of Net Profit, closing stock, etc.) | Throughout (e.g. Net profit `418,396` carried into Balance Sheet financed-by section, p.4) | **Stable** |

**Caveat (page number only):** the standing annotation legend that defines these rules is
on **p.34** in 2024 but **p.33** in 2023 — a routine per-year pagination shift, not a rule
change. The module's `cite` uses 2024 page numbers, which remain correct for the cited
2024 scheme.

**Verdict: RULE STABLE.**

---

### AC4 — "At OL, bank the theory marks first" (flat-mark written theory)

**Claim (OL):** Ordinary Level pays **big flat marks** for written definitions/benefits
(5–10 marks each), reachable independently of the computational questions; skipping them
forfeits the surest marks. Cited to 2024 OL **p.13, p.17, p.18**.

| Element | 2024 OL (baseline) | 2023 OL (second year) | Verdict |
|---|---|---|---|
| Written theory (definitions / ratio explanations) awarded as flat blocks of ~10 marks | Present (definitions/benefits at 5–10) | Present, p.14: "Shareholders' funds" definition **`[10]`**; "Intangible assets" definition **`[10]`**; "Acid test ratio" **`[10]`**; ROCE explanation **`[10]`** | **Stable** |
| Theory marks independent of computational accuracy | Yes | Yes — these are self-contained written parts (e.g. the ratio *explanation* in (ii) is prose, not tied to the account preparation); production-budget purpose theory (Q9(f)) similarly | **Stable** |

**Verdict: RULE STABLE.** (Note: the module's specific worked example — "two benefits of a
cash budget for 5 each" — is labelled *authored for this exercise* in the `questionNote`;
the 2023 OL paper doesn't happen to carry that exact item, but the underlying structure —
flat-mark written theory at 5–10 marks, independent of the figures — is confirmed for 2023.)

---

## Summary

| Session | Rule | Second-year (2023) verdict |
|---|---|---|
| AC1 | Workings carry the marks (numbered-working / workmark system) | **Stable** (surface label "N-note" → "W-note" varies by year) |
| AC2 | Balancing is its own discrete mark | **Stable in principle**; the literal "Both totals correct *" wording is 2024-specific (2023 shows it as an arrow annotation `[1]`) |
| AC3 | One error is penalised once; own-figure / transfer marking | **Stable** (legend page 34→33, pagination only) |
| AC4 | OL flat-mark written theory (5–10 marks, figure-independent) | **Stable** |

**Bottom line:** every substantive marking *rule* the module teaches is confirmed
present in a second, independent year (2023). Two items are year-specific *surface
presentation*, not rule changes: the working-note letter (N vs W) and the exact
"Both totals correct *" label. Neither makes the module inaccurate as written, because
the module explicitly attributes its citations to the **2024** scheme — but if strict
year-neutrality is desired, the reframes below remove the year-specific wording.

---

## Proposed year-stable reframes (optional — NOT applied; module unedited)

These are offered because the two labels above are 2024-specific. They are **not**
corrections of factual error; the module's 2024 citations are accurate. Apply only if the
team wants the teaching text to read as year-neutral.

**Reframe 1 — AC2 balance-sheet label (recommended if year-neutrality wanted).**

- Old (`scale.name`): `'Both totals correct *'`
- New: `'Both totals correct'`

- Old (`scale.notes[0]`):
  `'“Both totals correct *” is its own losable mark, independent of the line entries.'`
- New:
  `'The mark for both balance-sheet totals agreeing is its own losable mark, independent of the line entries.'`

- Old (`question`, the trailing sentence): `'…both totals agreeing (marked with a *).'`
- New: `'…both totals agreeing — a discrete presentation mark separate from the line figures.'`

  (Rationale: 2023 awards the same discrete balancing mark but shows it as an arrow
  annotation worth `[1]`, without the asterisked "Both totals correct *" wording.)

**Reframe 2 — AC1 working-note letter (minor; optional).**

- Old (`grid.shorthand`): `'N-note working · 7m'`
- New: `'Numbered working · 7m'`

- Old (`grid.cite` label tail): `'(workmark system, N-notes)'`
- New: `'(workmark system, numbered workings)'`

  (Rationale: the 2024 scheme labels workings N1, N2…; the 2023 scheme labels them
  W1, W2…. "Numbered working" is the year-stable term.)

No reframe is proposed for AC3 or AC4 — both are fully stable (AC3's page-number
difference is intrinsic to per-year pagination and the module correctly cites the 2024
pages).
