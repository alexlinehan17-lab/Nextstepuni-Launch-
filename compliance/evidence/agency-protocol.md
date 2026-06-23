# Evidence Dossier — The Driver's Manual (Agency)

**Module:** `agency-protocol` (`components/AgencyProtocolModule.tsx`)
**Review date:** 2026-06-23
**Reviewer:** Pre-accreditation literature review (DCU / Brian MacCraith)
**Governing rule:** Only state/advise what peer-reviewed literature supports; every DOI
verified via CrossRef. References surface via inline `Cite` markers + the module-wide
**References** button; data in `data/references/agencyProtocol.ts`.

**Reviewer note.** A student-agency module that dresses six established motivation
constructs in a driving metaphor (sat-nav, driver/passenger, engine). Each named construct
maps cleanly to a peer-reviewed source: possible selves (Markus & Nurius 1986), future
time perspective / linking study to goals (Husman & Lens 1999), autonomy as the "origin"
vs "pawn" experience (Ryan & Deci 2000, the SDT formalisation of deCharms' origin/pawn),
agentic engagement (Reeve 2013), the difficulty-as-impossibility identity trap (Oyserman &
Destin 2010), and funds of knowledge (Moll et al. 1992). **No content cut.** Two minor
tightenings: "far more likely to do the work" → "more likely", and "do far better in
school" → "tend to do better in school" (the autonomy/achievement link is correlational).
The metaphor widgets (FlipCards, MindsetSorter, Reorder checklist, input forms) are
interactive exercises, not data claims.

---

## Verified references

| Key | Citation | DOI |
|-----|----------|-----|
| markus1986 | Markus & Nurius (1986). Possible selves. *American Psychologist*. | [10.1037/0003-066x.41.9.954](https://doi.org/10.1037/0003-066x.41.9.954) |
| husman1999 | Husman & Lens (1999). The role of the future in student motivation. *Educational Psychologist*. | [10.1207/s15326985ep3402_4](https://doi.org/10.1207/s15326985ep3402_4) |
| ryandeci2000 | Ryan & Deci (2000). Self-determination theory and the facilitation of intrinsic motivation, social development, and well-being. *American Psychologist*. | [10.1037/0003-066x.55.1.68](https://doi.org/10.1037/0003-066x.55.1.68) |
| reeve2013 | Reeve (2013). How students create motivationally supportive learning environments for themselves: The concept of agentic engagement. *Journal of Educational Psychology*. | [10.1037/a0032690](https://doi.org/10.1037/a0032690) |
| oyserman2010 | Oyserman & Destin (2010). Identity-based motivation: Implications for intervention. *The Counseling Psychologist*. | [10.1177/0011000010374775](https://doi.org/10.1177/0011000010374775) |
| moll1992 | Moll, Amanti, Neff & Gonzalez (1992). Funds of knowledge for teaching. *Theory Into Practice*. | [10.1080/00405849209543534](https://doi.org/10.1080/00405849209543534) |

---

## Claim-by-claim record

- **§1 Setting the Sat-Nav** — "Possible self" as a motivating image of the future
  (**markus1986**); linking daily study to a future goal raises follow-through
  (**husman1999**). Verified; "far more likely" softened to "more likely."
- **§2 Driver or Passenger** — The origin/pawn experience and academic ownership map to
  autonomy, a core driver of motivation and (correlationally) achievement
  (**ryandeci2000**). Verified; "far better" softened to "tend to do better."
- **§3 The Driver's Controls** — Agentic engagement: students actively shaping their own
  learning environment (**reeve2013**). Verified.
- **§4 Roadblocks & Potholes** — The difficulty-as-impossibility identity trap
  (**oyserman2010**). Verified.
- **§5 Your Unique Engine** — Funds of knowledge: home/community knowledge as a genuine
  asset (**moll1992**). Verified.
- **§6 Your Route Plan** — Application/planning exercise; no new empirical claim.

---

## Reframed content
None cut. Two correlational claims tightened ("far more likely" → "more likely";
"do far better in school" → "tend to do better"); no verbatim removals, so no
`data/cutContent.ts` entries for this module.
