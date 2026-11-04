<!--
 @license
 SPDX-License-Identifier: Apache-2.0
-->

# Evidence Dossier — Mastering English (subject module)

**Module:** `subject-english-protocol` (data-driven via `components/SubjectModule.tsx`;
content in `subjectContentLanguages.ts` under key `english`)
**Group:** B (subject-specific) — grounded in official SEC sources, **not**
peer-reviewed psychology journals.
**Review date:** 2026-09-14 (first prepared 2026-07-18)
**Reviewer:** Pre-accreditation review (DCU / Brian MacCraith)
**Governing rule:** Only state/advise what a real, locatable source supports. For this
module the sources are the in-repo SEC English Higher Level 2025 marking scheme and the
in-repo 2013 English Chief Examiner's Report, the most recent Chief Examiner's Report for
LC English. Sources surface via inline `{{cite:N}}` markers (rendered as `<Cite/>`) and
the module-wide **References** button; data in `data/references/subjectEnglish.ts`. The
2024 HL scheme is the second-year stability check (`examiner-reports/english/2024-verification.md`
confirms the PCLM weightings, primacy of Purpose, the QA/QB rule and the Unseen Poem rules
for 2024 and 2025), and the 2021–2025 HL/OL schemes in `examiner-reports/english/schemes/`
back the text-list and mode-rotation checks below.

**History.** This review was first carried out on 2026-07-18 on a side branch (commit
`e6c7d99c`) against the module's pre-audit wording. Main's 2026-07-21 audit (`a396c831`)
then corrected the exam structure independently (logged as `subject-english-001`…`-003`).
On 2026-09-14 the review was redone on main's wording: main's structural corrections were
kept verbatim, the remaining strategy corrections were re-applied by hand, the whole module
was re-checked claim by claim, and two further factual errors found in that pass were
corrected (`subject-english-008`, `-009`).

**Page numbers.** Scheme references use PDF page numbers (the printed page label is one
lower, e.g. PDF p.3 = printed p.2). Report references use PDF page numbers, which match the
report's printed labels.

---

## Verified sources

| # | Source | Kind | Locator |
|---|--------|------|---------|
| 1 | SEC English Higher Level 2025 marking scheme — PCLM criteria, 30/30/30/10 weightings and primacy of Clarity of Purpose (p.3); Paper 1 Section I = QA on one text + QB on a different text, 100 marks (p.4); Composing 100 marks, single theme (p.13); Single Text 60 marks, options A–E (pp.21–31); Comparative 70 marks, 2025 modes, one-film rule (p.32), question formats (pp.33–41); Poetry 70 = Unseen Poem 20 + Prescribed Poetry 50, both required, and the unseen-poetry marking instructions (p.42); Prescribed Poetry (p.44); criteria descriptors (Appendix 1, p.50) | official | in-repo `examiner-reports/english/2025-marking-scheme.pdf` (read directly for this review; distilled in `2025-insights.md`) |
| 2 | SEC English 2013 Chief Examiner's Report — assessment structure (p.3); section averages (HL Table 4, p.7; OL Table 5, p.9); rigid, formulaic comparative answers (p.8); unseen poem omitted by some candidates (pp.8–9); "banks of knowledge" (p.11); brief compositions (pp.15–16); genre, register and short-story craft (p.16); best answers grounded in the question, loss of focus, evidence as a discriminator (p.18); comparative the lowest-scoring section, formulaic approaches hinder (pp.19–20); unfinished sections and time management (p.20); omitted questions (p.21) | official | in-repo `examiner-reports/english/2013-chief-examiner.pdf` (read directly for this review; official URL `https://www.examinations.ie/archive/examiners_reports/Chief_Examiner_Report_English_2013.pdf`, retrieved via the Internet Archive; distilled in `2013-insights.md`) |

**Uncited logistical facts.** The paper durations (Paper 1 2 h 50, Paper 2 3 h 20) and
"across two days" are exam-timetable facts printed on the papers themselves, not stated in
the marking schemes, so they carry no citation. The same durations (170 and 200 minutes)
are recorded in `data/knowledge/subjectTiming.ts`.

---

## Claim-by-claim record

- **§1 How English Actually Works**
  - Two papers × 200 = 400 marks — the 2025 section allocations sum to 400 (100 + 100;
    60 + 70 + 70) (**scheme2025**); the 2013 report states it outright: "two written
    papers, each with an allocation of 200 marks, giving an overall total of 400 marks"
    (p.3).
  - Paper 1: Comprehending 100 marks with three texts on a shared theme; QA (50) on one
    text and QB (50) on a different text, never both on the same text (**scheme2025**
    p.4; three texts on a theme also in the 2013 report, p.3); Composition 100 marks, one
    of a list, prompts tied to the paper's single theme (**scheme2025** p.13). Main's
    wording, corrected under ENG-001. "Functional writing task" is the module's label
    for Question B; the scheme does not use the term, but its tasks are short pieces in
    a set form (2025: a team talk, an online response to a review, a podcast reflection).
  - Paper 2: Single Text 60 marks, a play or a novel (**scheme2025** pp.21–31, corrected
    — ENG-008); Comparative 70 marks, three texts, one mode, the 2025 modes named
    (**scheme2025** p.32, corrected — ENG-008; the 2013 report asks candidates to "be
    prepared to refer to three texts", p.8); Poetry 70 = Unseen Poem 20 + Prescribed
    Poetry 50, an essay on a studied poet (**scheme2025** pp.42, 44 — main's wording,
    corrected under ENG-002).
  - 50/50 paper balance (**scheme2025**, section totals).
  - Highlights: Single Text is a play or a novel; Hamlet (2024 HL and OL) and
    Philadelphia, Here I Come! (2021, 2023 and 2024 OL) are real past Single Text options
    in the in-repo schemes (ENG-008). Comparative: one question drawing on at least two
    texts, some questions requiring three (**scheme2025** pp.33–41, ENG-008); weakest
    section (**chiefExaminer2013** p.19, ENG-004). Poetry highlight is main's (ENG-002).
- **§2 What the Examiner Rewards**
  - PCLM criteria, 30/30/30/10 and primacy of Purpose — main's wording (ENG-003),
    **scheme2025** p.3.
  - Purpose: engaging the set task, matching the genre, sustaining focus — the
    scheme's Clarity of Purpose descriptor ("engagement with the set task … understanding
    of genre", Appendix 1, p.50) and the p.3 requirement "to display a clear and purposeful
    engagement with the set task" (**scheme2025**). The "most common reason students lose
    marks" ranking was removed (ENG-007).
  - Coherence: "ability to sustain the response over the entire answer … continuity of
    argument, sequencing, management of ideas, choice of reference" (**scheme2025**
    Appendix 1, p.50).
  - Language: "lively interesting phrasing, energy, style" (**scheme2025** Appendix 1,
    p.50). Mechanics = spelling and grammar, 10% (**scheme2025** p.3; punctuation sits
    under Language in Appendix 1 — corrected, ENG-009).
- **§3 Where Your Marks Are**
  - Composition 100 = 25% and the largest single allocation (**scheme2025**).
  - Comparative + Poetry = 140/400 = 35% (**scheme2025**). The "highly formulaic, learn
    the structure" advice is reversed to the report's findings: lowest-scoring section
    (HL 60%, p.7; OL 58%, p.9; "scored less well here than in other sections", p.19),
    formulaic approaches "can hinder candidates by inhibiting their engagement with the
    terms of the questions" (pp.19–20), evidence quality "a significant discriminator
    used by examiners" (p.18) (**chiefExaminer2013**, ENG-004).
  - Poetry split and Prescribed Poetry essay — main's wording (ENG-002), **scheme2025**
    pp.42, 44. The "playing field is level" framing of the unseen poem is advice.
  - Comprehending: QA/QB on different texts — main's wording (ENG-001), **scheme2025**
    p.4. The Question B forms listed (speech, letter, article, diary entry, proposal) all
    occur in the 2023–2025 HL Question B tasks in the in-repo schemes. Matching genre and
    register in Question B: **chiefExaminer2013** p.16 ("Writing in the correct genre
    using an appropriate register … when responding to tasks on Paper 1, Section I,
    Question B").
- **§4 What Costs You Marks**
  - Task focus: "The best answers managed to remain grounded, both in the question asked
    and in the text"; comparative under-achievement "could often be attributed to a loss
    of focus in terms of the requirements of the task" (**chiefExaminer2013** p.18). The
    "number one" / "every year" wording was removed (ENG-007).
  - Timing: "Omitting questions or parts of questions inevitably has a deleterious effect
    on outcomes" (p.21); "inefficient time management may have been a factor" (p.20)
    (**chiefExaminer2013**). The 55/70/70-minute split is main's example plan (practical
    advice, uncited). "Second biggest" was softened (ENG-007).
  - Composition development: "extremely brief and lacked development" (HL, p.15); "it is
    difficult to sustain a response or develop a range of ideas necessary to acquire
    maximum marks if the answer is brief in the extreme" (OL, pp.15–16); genre
    conventions and short-story craft (p.16) (**chiefExaminer2013**). Replaces the
    invented 5 / 7–9-paragraph and 1,000+-word figures (ENG-005).
  - Voice: re-anchored to the Language descriptor (**scheme2025** Appendix 1, p.50,
    ENG-009).
- **§5 How to Study English**
  - Timed composition practice, one-page summaries, quote counts — practical study advice
    (uncited; see Outstanding).
  - Comparison grid kept, with the anti-formula caution (**chiefExaminer2013** pp.19–20,
    ENG-004).
  - Prescribed Poetry preparation — practical advice on main's wording.
  - Unseen Poem: the TPCASLT mnemonic is replaced with a routine built from the scheme's
    unseen-poetry instructions, quoted: reward "the patterned nature of the language of
    poetry, its imagery, its sensuous qualities, and its suggestiveness"; "guard against
    the temptation to assume a ‘correct’ reading of the poem" (**scheme2025** p.42,
    ENG-006).
- **§6 Your English Action Plan** — Practical plan; no factual claims beyond those
  verified above.

---

## Corrections & reframed content (also logged in `data/cutContent.ts`)

| ID | Section | Original → Corrected | Reason |
|----|---------|----------------------|--------|
| ENG-001 (`subject-english-001`, 2026-07-21) | §1, §3 | "two comprehension texts (Question A, worth 50 marks each — you do both)" → QA (50) on one text + QB (50, functional writing) on a different text; never both on the same text | Main's audit fix. Scheme p.4 (`2025-marking-scheme.md` lines 143–144). |
| ENG-002 (`subject-english-002`, 2026-07-21) | §1, with the poetry advice in §3–§6 | "Unseen Poetry … comparison with a second poem — 70 marks" → Poetry 70 = Unseen Poem 20 + Prescribed Poetry 50 | Main's audit fix. Scheme p.42 (2024 scheme lines 1801–1857). |
| ENG-003 (`subject-english-003`, 2026-07-21) | §2 | "Each criterion carries roughly equal weight" → 30/30/30/10 + primacy of Purpose | Main's audit fix. Scheme p.3 (`2025-marking-scheme.md` lines 66–69, 85–86); stable in 2024. |
| ENG-004 (`subject-english-004`) | §1 & §3 highlights, §3, §5 | "the Comparative is highly formulaic … you can consistently score well" / "often the highest-scoring section" → lowest-scoring section; formulaic approaches hinder; evidence quality discriminates | 2013 report pp.7–9, 18–20 contradict the original advice. |
| ENG-005 (`subject-english-005`) | §4 | "A five-paragraph essay will not score in the top bracket" / "seven to nine substantial paragraphs" / "1,000+ words" → the report's brevity principle + genre control | Figures not in any SEC source; report supports the principle only (pp.15–16). |
| ENG-006 (`subject-english-006`) | §5 | "TPCASLT method" + "within six weeks" → reading routine grounded in the scheme's unseen-poetry instructions | Mnemonic in no in-repo SEC source; scheme p.42 quoted instead. |
| ENG-007 (`subject-english-007`) | §2, §4 | "the most common reason students lose marks" / "number one mark-killer" / "Every year, the Chief Examiner's Report says…" / "second biggest killer" → unranked, attributed to the report's actual words | No SEC ranking exists; only one CE report exists for LC English. |
| ENG-008 (`subject-english-008`) | §1 | Single Text "plays, novels, or films" → "plays or novels"; comparative "typically … all three texts" → at least two, some questions all three; mode list → the 2025 set | No Single Text option in the in-repo 2021–2025 schemes is a film (the one-film rule is a Comparative rule, p.32); 2025 Q2s ask for "at least two texts" (pp.33–41). |
| ENG-009 (`subject-english-009`) | §2, §4 | Mechanics "spelling, grammar, and punctuation" → "spelling and grammar"; "authentic voice" / "explicitly reward authentic language" → the Language descriptor | Scheme p.3 and Appendix 1 (p.50) put punctuation under Language and name no "authentic" criterion. |

## Outstanding for accreditation

- The 2013 Chief Examiner's Report is the most recent for LC English; its statistics
  predate the 2017 grading-scale change. The module uses its averages only for relative
  ordering (weakest section), which is the reading the report itself gives (p.19).
- The comparative modes are stated as the 2025 set; they rotate (2023: General Vision and
  Viewpoint, Literary Genre, Theme or Issue; 2024: Literary Genre, Cultural Context, Theme
  or Issue; 2025: Theme or Issue, Cultural Context, General Vision and Viewpoint), so this
  line needs a yearly refresh.
- Study-advice claims outside the SEC sources, left as written and uncited: the
  "one-page summary" highlight ("active recall at its best — far more effective than
  re-reading your notes") is a learning-science claim that belongs with the Group A
  active-recall evidence, and summarising is not the same technique as retrieval
  practice; "strong readers tend to be stronger writers" (§1 highlight) and "Top-scoring
  students plan before they write" (§2) are consistent with the report's
  read-widely and process-writing recommendations (p.20) but are not findings in it;
  "Many students treat this as warm-up" (§3) and "many students write in a generic,
  impersonal voice" (§4) are unquantified.
- The timed-practice figure of about 65 minutes for a composition (§5, §6) is advice, not
  an SEC figure, and differs from the 85-minute composition allocation in
  `data/knowledge/subjectTiming.ts`. Worth reconciling.
- "The SEC website has decades of them for free" (§5) is an uncited logistical pointer.
