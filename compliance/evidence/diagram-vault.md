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

## Native corpus — the paper-extraction pipeline

Beyond the derived projection above, the vault now carries a **native** corpus:
figures cropped straight from SEC question papers by a dedicated pipeline and
confirmed one crop at a time by a verify agent. These land in
`data/diagramVault/figures/<subject>.ts` (one file per subject), are aggregated
by `data/diagramVault/native.ts`, and win on any `src` collision with a derived
figure (native is the primary paper crop). The same integrity gate
(`test/diagramVault.test.ts`) covers them.

Pipeline (`tools/`):

1. **`dv_prepare.py <subjectId> <cycle> [--years …]`** — downloads each tagged
   paper from the world-readable SEC corpus on Firebase Storage, runs
   `detect_exam_figures.py`, and crops every candidate region to a PNG with a
   `candidates.json` manifest. The cache key and `cand_id` include year + level
   so SEC's reuse of one `fileid` across years can't scramble the attribution.
2. **`detect_exam_figures.py`** — proposes candidate regions: raster images
   (header/banner/cover/sliver-filtered) **plus** vector-drawing clusters
   (union-find over all small paths — essential for line-art subjects whose
   circuits/apparatus/CAD drawings are drawn, not rastered).
3. **Agent verify** — one agent per (subject, year, level) VIEWS every crop and
   accepts only a genuine technical figure, writing a claim-free `alt`, an SEC
   `source` (paper + question label where confidently known, else `questionRef`
   null — never a guessed number), and copying the crop path verbatim. This is
   the accreditation gate: covers, decorative photos, blank answer grids and
   generic number tables are rejected. "When unsure, REJECT."
4. **`dv_apply.py <subjectId> <verified…>`** — copies accepted crops into
   `public/exam-figures/<subject>/` and (re)writes the subject figure file.

### Native coverage (2022–2024 waves shipped)

| Subject | Figures | Subject | Figures |
|---------|--------:|---------|--------:|
| Chemistry | 68 | Geography | 60 |
| Biology | 55 | Design & Communication Graphics | 49 |
| Mathematics | 42 | Physics | 36 |
| Agricultural Science | 40 | Construction Studies | 33 |
| Computer Science | 28 | Economics | 25 |
| Engineering | 25 | Technology | 17 |
| Home Economics | 7 | Business | 4 |
| Applied Mathematics | 1 | | |

Art was run and yielded **no** diagrams (its papers are reproductions of
artworks/photographs, not technical figures) — correctly empty, not skipped
silently.

### Junior Cycle + Physics & Chemistry wave (2022–2024, shipped)

| Subject | Figures | Subject | Figures |
|---------|--------:|---------|--------:|
| Physics & Chemistry (LC) | 52 | JC Applied Technology | 42 |
| JC Science | 40 | JC Geography | 40 |
| JC Wood Technology | 40 | JC Mathematics | 38 |
| JC Engineering | 20 | JC Home Economics | 7 |
| JC Business Studies | 6 | | |

JC papers are common-level, so their entries carry `level: null` and an SEC
"Junior Certificate/Junior Cycle" source string. JC Science, Geography, Physics &
Chemistry and the JC technical subjects (Applied Technology, Wood Technology,
Engineering) are the richest veins — labelled apparatus, circuits, OS maps,
synoptic charts, CAD/orthographic drawings, joints and mechanisms.

### 2025 wave (most recent exam year, shipped)

The 2025 papers were extracted for every diagram subject that lacked them
(biology, chemistry, physics and geography already carried 2025). Each subject
file was regenerated from the full set of its verified year-slices (2022–2025),
never overwritten with 2025 alone. Highlights: Physics & Chemistry, Mathematics
(incl. Foundation level), DCG, JC Applied Technology, JC Wood Technology and JC
Science all gained a fresh year of figures. The native corpus now stands at
**~1,500 figures across 24 subject files** (after 2016–2021 backfill for
Biology, Chemistry, Physics, Geography, DCG, Construction, Engineering,
Agricultural Science and Physics & Chemistry, plus filling Biology's 2022–2023
gap). The richest subjects (Biology 135, Geography 100, Physics & Chemistry 96,
DCG 88) now span **2016–2025**. 2020 was a COVID-disrupted year — several papers
were figure-light and correctly yielded few or no diagrams. Older physics and
agricultural-science HL papers are text/photo-heavy and correctly yield little;
MISSING is acceptable, a wrong crop is not.

## Next waves (planned)

Continue the native pipeline until every paper with extractable diagrams is
covered: LCA technical strands (engineering, graphics-and-construction,
technology), any remaining JC diagram subjects (jc-music listening figures where
present), and older-year backfill (2010–2021) for the subjects already covered —
the tagged corpus reaches back to 2010. Every added figure is agent-verified with
an SEC `source`, so the integrity gate covers it automatically.
