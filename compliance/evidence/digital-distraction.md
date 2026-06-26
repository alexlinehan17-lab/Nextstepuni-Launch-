# Evidence Dossier — Creating Barriers for Digital Distractions

**Module:** `digital-distraction-protocol` (`components/DigitalDistractionModule.tsx`)
**Review date:** 2026-06-23
**Reviewer:** Pre-accreditation literature review (DCU / Brian MacCraith)
**Governing rule:** Only state/advise what peer-reviewed literature supports; every DOI
verified via CrossRef. References surface via inline `Cite` markers + the module-wide
**References** button; data in `data/references/digitalDistraction.ts`.

**Outcome:** Largely practical advice (friction, blockers, phone placement). The
"23-minute refocus" figure is real but was being stacked linearly — reframed (DD-001).
Several specific claims are well-sourced (the UT "brain drain" study; implementation
intentions).

---

## Verified references

| Key | Citation | DOI |
|-----|----------|-----|
| casey2008 | Casey, Jones & Hare (2008). The adolescent brain. *Annals of the NY Academy of Sciences*. | [10.1196/annals.1440.010](https://doi.org/10.1196/annals.1440.010) |
| mark2005 | Mark, Gonzalez & Harris (2005). No task left behind? Examining the nature of fragmented work (resumption of work). *Proc. SIGCHI (CHI)*. | [10.1145/1054972.1055017](https://doi.org/10.1145/1054972.1055017) |
| ward2017 | Ward, Duke, Gneezy & Bos (2017). Brain drain: The mere presence of one's own smartphone reduces available cognitive capacity. *J. Assoc. for Consumer Research*. | [10.1086/691462](https://doi.org/10.1086/691462) |
| gollwitzer1999 | Gollwitzer (1999). Implementation intentions: Strong effects of simple plans. *American Psychologist*. | [10.1037/0003-066x.54.7.493](https://doi.org/10.1037/0003-066x.54.7.493) |

---

## Claim-by-claim record

- **§1 Why Your Phone Wins** — Adolescent dual-systems brain: reward/socioemotional
  systems mature ahead of prefrontal self-control, biasing toward immediate rewards
  (**casey2008**). After an interruption it can take ~23 minutes to resume the task
  (**mark2005**, "No task left behind?", which examines resumption of work — corrected
  from mark2008 after the verification pass; mark2008 measures the speed/stress trade-off,
  not resumption time). Verified. The "every check = 23 min, 3 checks = zero" linear
  stacking was reframed and the calculator relabelled a simplified illustration (DD-001).
- **§2 The Phone Swap / §3 Laptop lockdown** — Adding "friction" / choice architecture to
  make distractions harder to reach. Practical strategy (consistent with behaviour-change
  principles); no specific empirical figure claimed.
- **§4 Setting Up Your Space** — The mere visible presence of one's smartphone reduces
  available cognitive capacity, even when face-down/silent. **ward2017** (the University
  of Texas study the module names). Verified.
- **§5 Building Better Habits** — "If-then" plans are implementation intentions, which
  reliably help translate goals into action (**gollwitzer1999**). Habit stacking is a
  popular framing of habit-cue pairing. Verified.
- **§6 FOMO / §7 Roadmap** — Social pre-commitment, screen-time batching, phased plan.
  Practical advice; the phased roadmap and "Attention Deficit Calculator" are interactive
  illustrations.

---

## Reframed content (also logged in `data/cutContent.ts`)

| ID | Section | Original → Reframed | Reason |
|----|---------|---------------------|--------|
| DD-001 | § 1 + calculator | "every check = 23 min; 3 checks = ~zero deep work" → accurate "~23 min to refocus after an interruption"; calculator labelled a simplified illustration | The 23-min figure (mark2005) is real but does not stack linearly; the original overstated it as a precise per-check arithmetic. |

**Source correction (verification pass, 2026-06-26):** the ~23-minute resumption figure
in §1 was re-attributed from **mark2008** → **mark2005** ("No task left behind?",
resumption of work). mark2008 (Mark, Gudith & Klocke) measures the speed/stress trade-off
and does not report a resumption time; the figure is genuinely from Mark, Gonzalez &
Harris (2005). No student-facing wording changed — the inline citation now points to the
source that supports the specific claim.
