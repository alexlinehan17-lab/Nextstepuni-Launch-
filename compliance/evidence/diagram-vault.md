# Evidence Dossier — Diagram Vault

**Tool:** Diagram Vault (`components/DiagramVault/DiagramVault.tsx`, registered in
`components/InnovationZone.tsx` as tool id `diagram-vault`)
**Data:** `data/diagramVault/index.ts`
**Review date:** 2026-07-10 (living document — updated with every corpus wave)

## What it is

A Topic-Vault-style browser for the real diagrams, graphs, maps and charts that
appear in SEC exams: pick a subject → see every verified exam figure for it, each
with its exam source and a plain-English decode of what the figure shows. It is
the visual counterpart to Topic Vault (questions by topic) and Marking Lens
(marks by question).

## Governing rule (same accreditation line as the rest of the app)

> Every tile shows a REAL figure, cropped from a real paper, with a verified exam
> source. No generated, redrawn or unattributed images. The decoded description
> (`alt`) states only what the figure shows — never a claim beyond it.

## Source of truth — DERIVED, not hand-authored

Diagram Vault invents no figure metadata. It is a **read-only projection** of the
figure exhibits already curated (and verified when built) in two data files:

- `catchUpLaneData.ts` → `RECOVERY_CARDS[].figure` — carries a `topicLabel`.
- `commandWordData.ts` → `COMMAND_WORD_QUESTIONS[].figure` — carries a `questionRef`.

Each figure there was cropped from the paper with `tools/extract_exam_figure.py`
(locate → render → crop → adversarially verify) and stored with a decoded `alt`
and an SEC `source` string. `data/diagramVault/index.ts` reads those two arrays,
dedupes by figure path (catch-up-lane first, so a shared figure keeps its topic),
and parses year + level from the source string. Because the vault is a projection,
it can never drift from the exhibits it mirrors — fix a figure at its source and
the vault follows.

## Machine-checked integrity (`test/diagramVault.test.ts`, every CI run)

1. Every figure the vault points at **exists** in `public/` (no 404 tiles).
2. Every entry carries a decoded `alt` and an **SEC-attributed** source.
3. Ids are unique; per-subject counts reconcile with the entry list.

`test/diagramVault.smoke.test.tsx` renders the tool: the picker lists real
subjects; drilling into one shows figure tiles pointing at real `/exam-figures/…`
files with SEC attribution and the description behind a toggle.

## Coverage (wave 1 — the existing verified corpus)

149 figures across 18 subjects, derived from the current exhibit set:

| Band | Subjects |
|------|----------|
| Richest (12+) | Applied Mathematics (21), Construction Studies (21), Art (17), Biology (14), Mathematics (13), Geography (12) |
| Mid (5–8) | Politics & Society (8), Chemistry (7), Irish JC (7), Geography JC (5), Mathematics JC (5) |
| Thin (1–4) | Business (4), History JC (4), Economics (3), Science JC (3), Business Studies JC (2), Physics (2), Agricultural Science (1) |

## Next waves (planned)

Expand the corpus via `tools/extract_exam_figure.py` — the same extract-and-verify
discipline that built the seed set — prioritising the thin subjects and the
high-diagram LC subjects (biology labelled diagrams, geography OS-map / weather
figures, business charts, physics/chemistry apparatus). Every added figure lands
first as a verified exhibit (with `alt` + SEC `source`), so the vault picks it up
automatically and the integrity gates cover it.
