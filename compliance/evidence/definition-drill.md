# Evidence Dossier — Definition Drill

**Tool:** Definition Drill (`components/DefinitionDrill/DefinitionDrill.tsx`,
registered in `components/InnovationZone.tsx` as tool id `definition-drill`)
**Data:** `data/definitionDrill/index.ts`
**Review date:** 2026-07-10

## What it is

A drill for the exact **mark-earning wording** of the definitions the SEC scheme
awards marks for. Pick a subject → work a deck: read the prompt ("Explain what is
meant by centripetal force"), recall the wording from memory, reveal the scheme's
own allocation, and self-rate ("I knew it" / "Review again"). "Review again"
recirculates the card. It is the retrieval-practice counterpart to Marking Lens,
Answer Architect and Diagram Vault.

## Governing rule (same accreditation line as the rest of the app)

> Every reveal is the SEC scheme's own mark-earning wording, decoded — never a
> model answer, never an invented definition. A term whose scheme fixes only a
> mark split (not the words) has no wording to reveal, so it is not drillable and
> is dropped. If it can't be shown from a filed scheme, it isn't shown.

## Source of truth — DERIVED, not hand-authored

Definition Drill authors **no definitions**. It is a **read-only projection** of
the Marking Lens corpus (`data/markingLens/`), whose every entry is authored ONLY
from a filed SEC marking scheme (`examiner-reports/`) and machine-checked. The
projection (`data/definitionDrill/index.ts`) keeps a lens part only when **both**:

1. its `task` is a definition prompt (`Explain what is meant by…`, `Define…`,
   `State … law/principle`, `Distinguish between…`), **and**
2. its `decoded` field carries the scheme's **actual mark-earning wording** — not
   just a description of how the marks divide.

Filter (2) is the accreditation-critical gate. Open-ended "explain the term X"
parts (Business, Economics, Biology, Agricultural Science) carry only a mark
split in `decoded` — e.g. *"State (2m) + develop (3m)"*, *"The explanation earns
2 marks"*, *"Two 3-mark elements of the explanation"* — with **no wording to
reveal**. Drilling those would leave the reveal empty or force invention, so they
are excluded (a documented set of mark-split patterns, verified against the full
projected set). What survives is the **fixed-wording** definitions: laws,
principles, SI-unit and physical-quantity definitions whose scheme fixes the
exact phrase.

## Coverage (launch — honestly narrow)

| Subject | Definitions | Source |
|---------|------------:|--------|
| Physics | 18 | projected from Marking Lens |
| Chemistry | 5 | 4 projected + 1 authored (acid, Brønsted–Lowry) |
| Biology | 2 | authored (enzyme, osmosis) |

**25 definitions across 3 subjects.** (Engineering's only definition prompt —
"define material toughness" — is one the filed scheme awards a bare "4 marks"
with no wording, encoded in the lens as "a single 4-mark granule", so it carries
nothing to reveal and is correctly filtered out; `granule` is in the mark-split
exclusion set alongside "State (2m) + develop (3m)" and the rest.) Most are a projection of the Marking Lens
corpus — Physics and Chemistry schemes fix the phrase ("Force towards centre of
circle; that keeps an object moving in a circle"; "−log₁₀; [H⁺]"), whereas most
subjects' schemes fix only a mark structure for open-ended terms, so those are
correctly absent. Definition Drill deepens automatically as the Marking Lens
corpus adds more fixed-wording definitions.

**Authored-but-strictly-cited extension (`data/definitionDrill/authored.ts`).**
A few high-value definitions live in filed schemes not yet in the Marking Lens
corpus (notably Biology, whose lens entries are marks-only for these terms). Each
was verified verbatim against its named filed scheme — a re-citation pass over
`data/knowledge/phraseMatch.ts` (whose original source was the internal § B4
dossier, not a scheme) confirmed exactly which entries a filed SEC scheme
literally prints the wording for: **enzyme** ("Protein catalyst", 2023 HL
Q15(c)(i)), **osmosis** ("Movement of water; from higher to lower water
concentration across a selectively permeable membrane", 2025 HL Q9(a)) and the
**Brønsted–Lowry acid** ("proton donor", 2025 HL Q7(a)(i)). The other 15
phraseMatch entries did NOT verify against a filed scheme (no matching question,
mark-split only, or materially different wording) and were left out — never
invented to fill breadth. Authored cards carry an `authored|…` id and are held
to the same SEC-attribution and real-wording gates as the projected cards.

## Machine-checked integrity (`test/definitionDrill.test.ts`, every CI run)

1. Non-empty; **every definition traces to a real Marking Lens part, or is an
   `authored|…` entry SEC-attributed to a named filed scheme**.
2. **THE ACCREDITATION GATE** — no `answer` is a mark-split description: every
   reveal carries real wording (asserted against the mark-split pattern set, plus
   a minimum-substance check after stripping mark tags). A card whose reveal is
   "the explanation earns 2 marks" can never ship.
3. Prompt/term non-empty; `marks > 0`.
4. Every `source` is SEC-attributed.
5. Ids unique; subject counts reconcile.

`test/definitionDrill.smoke.test.tsx` renders the tool: the picker lists real
subjects; drilling into one shows a prompt, a Reveal button, the mark-earning
wording, the SEC source, and the "I knew it" / "Review again" self-rate buttons.

## Design

Follows the module visual system (CLAUDE.md). Accent orange (`#F26B1F`) for the
prompt, the marks badge, the Reveal button and the reveal callout (the wording is
a *target to hit*). Success green (`#3A8D5F`) is used — correctly, per the
accent-vs-success rule — for the **"I knew it"** self-rating and the end-of-deck
completion card, because that is a self-assessed "you got it" signal. Neutral for
"Review again". No dynamic Tailwind class construction — hex tokens are inline
`style`. The drill runs client-side only; no new persistence.
