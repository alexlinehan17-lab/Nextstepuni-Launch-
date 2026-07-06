<!--
  Second-year verification for the Examiner's Chair Religious Education session.
  Cross-checks the load-bearing rules in data/examinersChair/religiouseducation.ts
  (cited to the SEC RE marking scheme 2025, HL + OL) against a DIFFERENT year's
  schemes: SEC RE marking scheme 2024 (HL + OL).
-->

# Religious Education — Examiner's Chair second-year verification (2024)

## Purpose

`data/examinersChair/religiouseducation.ts` teaches three marking rules cited to the
**SEC LC Religious Education marking scheme 2025** (HL for RE1/RE2, OL for RE3). This
document verifies those load-bearing rules are stable across a second year by
cross-checking them against the **SEC LC Religious Education marking scheme 2024**
(Higher Level and Ordinary Level).

## Sources obtained

| File | What it is | Retrieval |
|------|------------|-----------|
| `2024-marking-scheme.pdf` / `.md` | SEC LC Religious Education **HL** marking scheme 2024 (32 pp) | educateplus.ie mirror (`.../storage/Religious%20Education%20HL.pdf`); cover page confirms "Leaving Certificate 2024 … Higher Level … Religious Education" |
| `2024-ol-marking-scheme.pdf` / `.md` | SEC LC Religious Education **OL** marking scheme 2024 (36 pp) | educateplus.ie mirror (`.../storage/Religious%20Education%20OL.pdf`); cover page confirms "Leaving Certificate 2024 … Ordinary Level … Religious Education" |

Both retrieved successfully — this is a **full documentary cross-year check**, not a
logical fallback. `.md` extractions done via PyPDF2 with `<!-- page N -->` markers.
(Note: the educateplus filenames for the current year omit the year token; cover-page
extraction was used to confirm each PDF is the 2024 edition.)

## Standing caveat in the schemes themselves

Both 2024 schemes carry the SEC "Future Marking Schemes" note (p.2): *"Assumptions about
future marking schemes on the basis of past schemes should be avoided. While the
underlying assessment principles remain the same, the details of the marking of a
particular type of question may change …"* The verification below therefore separates
**underlying mechanism** (stable) from **question-specific figures** (may move year to
year).

---

## Rule-by-rule result

### RULE 1 (RE1) — Descriptive answer to a higher-order command is capped at the top of the Fair band (Max 21 on a 40-mark question)

Session cite: `SEC RE HL marking scheme 2025, p.18 (descriptive-answer cap; band ranges p.6)`.

| Element | 2025 (cited) | 2024 (verified) | Verdict |
|---------|--------------|-----------------|---------|
| 40-mark band ranges | Excellent 34–40, VG 28–33, Good 22–27, **Fair top 21**, Weak 10–15, 0–9 | Every 40-mark grid: `40-34 / 33-28 / 27-22 / 21-16 / 15-10 / 9-0` — **Fair top = 21** | **Identical** |
| Descriptive-cap mechanism | p.18, Q D(c) "**Compare** …": *"Note: Allow descriptive answers. If a candidate gives an accurate account … with only implicit reference to a similarity/difference … mark on its merits — **Max 21 marks**."* | Same "cap at the Fair ceiling" mechanism present, e.g. p.13 Q C(c): *"Note: Allow descriptive answers. If a candidate gives an accurate account … with only implicit reference to how this is communicated through individual people, mark on its merits — **Max 10 marks x 2**."* On a 20-mark question the Fair top is 10, so Max 10 = top of Fair — the identical rule scaled to the question's marks. | **Stable (mechanism)** |
| A 40-mark "Max 21" instance in 2024 | present (Q D(c)) | The 2024 paper had no 40-mark *Compare*-style question, so the literal "Max 21 on a 40-mark question" note does not recur. The comparative 40-mark questions in 2024 were framed with the lower-order command *"Outline a similarity and a difference"* (skill = "setting out information"), which carries no cap. | **Not year-critical** — the figure "21" is just the Fair ceiling for a 40-mark question (confirmed identical); the cap is applied wherever a descriptive answer meets a higher-order command. |

**Verdict: STABLE.** The band structure and the descriptive-cap mechanism ("mark on its
merits — Max [Fair ceiling]" when an answer describes where a higher-order command asked
for more) are both present in 2024. In 2024 the mechanism surfaces as "Max 10" on a
20-mark question; in 2025 it surfaces as "Max 21" on a 40-mark *Compare* question. Same
rule, both years. No change needed.

### RULE 2 (RE2) — Holistic banding on four dimensions (marking criteria, relevance, skill, factual accuracy)

Session cite: `SEC RE HL marking scheme 2025, p.2, p.4 (four-dimension holistic banding)`.

| Element | 2024 (verified) | Verdict |
|---------|-----------------|---------|
| Six-band scale | p.3 General Introduction: mark awarded "within a range from excellent to very good, good, fair, weak, very weak or no grade" | **Identical** |
| Four-dimension grid on every question | Every marking grid in 2024 uses the four rows **Evidence of MC / Relevance / Use of skill(s) / Factual accuracy** judged across Excellent–Weak columns at once | **Identical** |
| Accuracy is a band-setting dimension, not a line-item deduction | Confirmed — "Factual accuracy" is one of the four grid rows that jointly place the answer in a band; there is no separate subtraction | **Identical** |
| /20 band ranges (used in RE2 scale) | `20-17 / 16-14 / 13-11 / 10-8 / 7-5 / 4-0` → Good 11–13, VG 14–16, Excellent 17–20 (matches RE2) | **Identical** |

**Verdict: STABLE.** No change needed.

### RULE 3 (RE3, OL) — No descriptive cap at OL; a full, accurate, relevant description can reach the top band

Session cite: `SEC RE OL marking scheme 2025, p.5, p.20 (no descriptive cap at OL)`.

| Sub-claim (as written in the session file) | 2024 OL (verified) | Verdict |
|--------------------------------------------|--------------------|---------|
| Core: no HL-style descriptive-to-Fair cap; a full accurate description reaches Excellent | **Holds.** The 2024 OL paper includes a higher-order question — Q J(b)(ii) *"Discuss the extent to which …"* (skill: "examining perspectives and drawing conclusions") — and it carries **no** note capping a descriptive answer at Fair. A full, accurate, relevant answer can reach 34–40. Band grids identical to HL. | **STABLE (core)** |
| "OL commands are lower-order: Outline, Describe, Give an account." | **Overstated for 2024.** OL 2024 uses lower-order commands heavily (Outline ×10, Describe ×10, Explain ×9) **but also** higher-order/analytic stems: *"Discuss the extent to which…"* (Q J(b)(ii)), *"Profile how…"* (Q 2(a)), *"Explore how…"* (Q 3(a)). So OL is not exclusively lower-order. | **Year-specific / overstated** |
| "the OL scheme uses 'Max' zero times." | **FALSE for 2024 OL.** The 2024 OL scheme uses "max" **twice**: Q 2(a) — *"…without reference to the person … mark on its merits to a **max of 33 marks**"* (33 = top of Very Good on a 40-mark question); Q 3(a) — *"…implicit rather than explicit reference … mark on its merits to a **max of 16 marks**"* (16 = top of Very Good on a 20-mark question). These are **partial-answer caps** (an answer that omits a required element is capped at the top of VG) — NOT descriptive-style penalties — so the *core* rule survives, but the literal "zero times" statement does not. (For context: the **2025** OL scheme genuinely uses "max" zero times — grep returns nothing — so the session's claim was true for its cited year but is a brittle year-specific fact.) | **FALSE in 2024 — year-specific** |

**Verdict: CORE STABLE, two sub-claims year-specific.** The load-bearing teaching point
(OL does not ceiling a description at Fair for failing to evaluate; a strong description
is a top-band answer) is confirmed in 2024. But the supporting note *"the OL scheme uses
'Max' zero times"* is false for 2024, and *"OL commands are lower-order: Outline,
Describe, Give an account"* is overstated. Proposed year-stable replacements below.

---

## Summary

| Rule | Cited year (2025) | Second year (2024) | Verdict |
|------|-------------------|--------------------|---------|
| RE1 — descriptive answer to higher-order command capped at top of Fair | ✓ p.18, Max 21 (40M Compare) | ✓ mechanism present (Max 10 on 20M; Fair ceilings identical) | **STABLE** |
| RE2 — four-dimension holistic banding | ✓ p.2/p.4 | ✓ identical grids, six bands, /20 ranges match | **STABLE** |
| RE3 core — no descriptive cap at OL; description reaches top band | ✓ | ✓ (OL "Discuss" carries no Fair cap) | **STABLE (core)** |
| RE3 sub-claim — "OL scheme uses 'Max' zero times" | true for 2025 | **false for 2024** (used twice) | **YEAR-SPECIFIC** |
| RE3 sub-claim — "OL commands are lower-order (Outline/Describe/Give an account)" | broadly true | **overstated for 2024** (Discuss/Profile/Explore also appear) | **YEAR-SPECIFIC** |

## Proposed year-stable reframes (RE3 only — session file NOT edited)

In `data/examinersChair/religiouseducation.ts`, RE3 `scale.notes`:

Current:
```
notes: [
  'OL commands are lower-order: Outline, Describe, Give an account.',
  'There is no HL-style "you didn’t evaluate" cap — the OL scheme uses "Max" zero times.',
  'A full, accurate, relevant description can reach the Excellent band.',
],
```

Proposed (year-stable):
```
notes: [
  'OL centres on lower-order skills (Outline, Describe, Give an account); even where an OL question uses a higher-order stem, the scheme does not cap a description at Fair.',
  'There is no HL-style descriptive cap at OL: a description is not ceilinged at Fair for "not evaluating." Where an OL note applies a "Max", it caps a partial answer that omits a required element — not a description.',
  'A full, accurate, relevant description can reach the Excellent band.',
],
```

Rationale: the reframed note 1 no longer asserts OL commands are *exclusively* lower-order
(false in 2024); note 2 drops the brittle "uses 'Max' zero times" count (true 2025, false
2024) and instead states the stable principle — the cap that does exist at OL is a
partial-answer cap, not a descriptive-style penalty — which holds in both years. The RE3
`questionNote`, `keyNote`, `takeaway`, and the `coverageNote` do not repeat the "zero
times" count and are already year-stable, so no change is proposed there. RE1 and RE2 need
no change.
