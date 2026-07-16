# Evidence Dossier — Answer Architect

**Tool:** Answer Architect (`components/AnswerArchitect/AnswerArchitect.tsx`,
registered in `components/InnovationZone.tsx` as tool id `answer-architect`)
**Data:** `data/answerArchitect/index.ts`
**Review date:** 2026-07-10

## What it is

The mark-earning **skeleton** of a top answer, browsable by subject: pick a
subject → see real exam questions, each rebuilt as the ordered sequence of
mark-earning *beats* a full-marks answer is made of. Every card leads with the
shape of the answer (the scheme's own marking model), then each beat — what it
must deliver and what actually earns its marks — and the exact SEC source
underneath. It is the "how do I *build* the answer" counterpart to Marking Lens
(where the marks go) and Diagram Vault (the figures).

## Governing rule (same accreditation line as the rest of the app)

> Every beat is the SEC scheme's own allocation, decoded — never a model answer,
> never a mark the scheme doesn't award, never advice the scheme doesn't make.
> If a question can't be built honestly from a filed scheme, it is not shown.

## Source of truth — DERIVED, not hand-authored

Answer Architect authors **no new marking content**. It is a **read-only
projection** of the Marking Lens corpus (`data/markingLens/`), whose every entry
is authored ONLY from a filed SEC marking scheme (in `examiner-reports/`) and is
machine-checked to sum to its Available-Marks line (`test/markingLens.test.ts`).
The projection (`data/answerArchitect/index.ts`) maps each multi-part
`QuestionLens` to an `AnswerSkeleton`:

- `QuestionLens.headline` → `structure` (the shape of the answer)
- `QuestionLens.parts[]` → ordered `beats[]` (`part` → `part`, `task` →
  `requirement`, `decoded` → `earns`, `marks` → `marks`, index → 1-based `order`)
- `QuestionLens.cite` → `source` (with the `© State Examinations Commission` suffix)
- `QuestionLens.pitfall` → `pitfall` (an examiner-documented beat students skip)

Because it is a pure projection, it can never drift from the schemes it mirrors:
fix a lens entry at its source and the skeleton follows.

**Two deliberate filters keep it honest and distinct from Marking Lens:**

1. **Multi-beat only** (`parts.length >= 2`). A single-part 10-mark "short" is a
   mark-ladder, not an answer *structure*; those belong to Marking Lens alone.
   This is why Geography — whose lens entries are all one-part — is **not
   listed**, exactly as Diagram Vault only lists subjects that have figures.
2. **One skeleton per real question.** The Marking Lens EV/IV language mirror
   (the same exam marked by the same scheme, tagged twice) is collapsed to a
   single skeleton per `(subject, year, level, question)`, EV preferred, so the
   browser shows each real question once.

## Coverage (launch)

| Subject | Skeletons | Subject | Skeletons |
|---------|----------:|---------|----------:|
| Agricultural Science | 31 | Business | 24 |
| Physics | 22 | Biology | 20 |
| Construction Studies | 20 | Home Economics | 20 |
| Chemistry | 18 | Design & Communication Graphics | 16 |
| Engineering | 16 | Economics | 12 |

**199 answer skeletons across 10 subjects.** Construction Studies, Engineering
and Design & Communication Graphics joined automatically when their Marking Lens
entries were authored (wave 3) — no separate work in this tool. Geography is
present in the Marking Lens corpus but carries no multi-beat questions, so it
correctly does not appear here. Coverage grows automatically as the Marking Lens
corpus does.

## Machine-checked integrity (`test/answerArchitect.test.ts`, every CI run)

The projection inherits SEC-question grounding from the Marking Lens gate; these
gates guard the projection itself:

1. Non-empty, and **every skeleton traces back to a real Marking Lens entry**
   (its key exists in `MARKING_LENS`).
2. **Beats reconcile** — they sum to `totalMarks` (catches a dropped/duped part).
3. Beat ordering is **dense and 1-based**.
4. Every skeleton is **genuinely multi-beat** (structure, not a mark-ladder).
5. Every `source` is **SEC-attributed**; every beat carries a requirement, an
   earns line and positive marks; every `pitfall.cite` is examiner-attributed.
6. Ids unique; subject counts reconcile with the skeleton list.

`test/answerArchitect.smoke.test.tsx` renders the tool: the picker lists real
subjects; drilling into one shows skeleton cards with the SEC source and the
ordered beats behind a "Build the answer" toggle.

## Design

Follows the module visual system (CLAUDE.md). Accent orange (`#F26B1F`) marks
the brand and the *beats you must hit* — never green, because a beat is a
requirement, not a "correct" state. Beats use the ConceptCardGrid vocabulary
(accent numbered badge, Source Serif 4 term, DM Sans body) with a marks weight
badge; the structure line is an accent callout; the pitfall is an accent-tint
left-border card; the SEC source is uppercase-label text. No dynamic Tailwind
class construction — hex tokens are inline `style`.

## Next

Answer Architect deepens automatically with the Marking Lens corpus. As new
subjects/years are authored into `data/markingLens/` from filed schemes, their
multi-beat questions appear here with no further work, and the integrity gate
covers them automatically.
