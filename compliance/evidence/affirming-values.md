# Evidence Dossier — Affirming Values

**Module:** `affirming-values-protocol` (`components/AffirmingValuesModule.tsx`)
**Review date:** 2026-06-23
**Reviewer:** Pre-accreditation literature review (DCU / Brian MacCraith)
**Governing rule:** Only state/advise what peer-reviewed literature supports; every DOI
verified via CrossRef. References surface via inline `Cite` markers + the module-wide
**References** button; data in `data/references/affirmingValues.ts`.

**Reviewer note (replication-sensitive).** This module is the applied form of the
values-affirmation / stereotype-threat literature, which is genuinely landmark but also
genuinely contested. The constructs and the headline studies are all real and verified:
stereotype threat (Steele & Aronson 1995), its working-memory mechanism (Schmader & Johns
2003), the values-affirmation intervention and achievement-gap result (Cohen et al. 2006),
the broaden-and-build account of positive emotion (Fredrickson 2001), and the recursive
two-year follow-up (Cohen et al. 2009). **No content cut**, but the §4 "real world data"
was handled carefully because subsequent large/preregistered studies (e.g. Hanselman et
al. 2017) find the affirmation effect is **heterogeneous** — real but variable, strongest
for the most threatened students and absent in some settings. Accordingly: (i) "their
grades jumped significantly" → "in that study, their grades rose"; (ii) an explicit
in-text caveat was *added* ("later studies find the effect is real but varies — it works
best for the students most under threat, and not in every setting"); (iii) the
essentials-mode claim was attributed to "one study" with at-risk students. The Working
Memory Grid and Values Selector widgets are illustrative/practical, not measured data.

---

## Verified references

| Key | Citation | DOI |
|-----|----------|-----|
| steeleAronson1995 | Steele & Aronson (1995). Stereotype threat and the intellectual test performance of African Americans. *J. Personality and Social Psychology*. | [10.1037/0022-3514.69.5.797](https://doi.org/10.1037/0022-3514.69.5.797) |
| schmaderJohns2003 | Schmader & Johns (2003). Converging evidence that stereotype threat reduces working memory capacity. *J. Personality and Social Psychology*. | [10.1037/0022-3514.85.3.440](https://doi.org/10.1037/0022-3514.85.3.440) |
| cohen2006 | Cohen, Garcia, Apfel & Master (2006). Reducing the racial achievement gap: A social-psychological intervention. *Science*. | [10.1126/science.1128317](https://doi.org/10.1126/science.1128317) |
| fredrickson2001 | Fredrickson (2001). The role of positive emotions in positive psychology: The broaden-and-build theory of positive emotions. *American Psychologist*. | [10.1037/0003-066x.56.3.218](https://doi.org/10.1037/0003-066x.56.3.218) |
| cohen2009 | Cohen, Garcia, Purdie-Vaughns, Apfel & Brzustoski (2009). Recursive processes in self-affirmation: Intervening to close the minority achievement gap. *Science*. | [10.1126/science.1170769](https://doi.org/10.1126/science.1170769) |

---

## Claim-by-claim record

- **§1 The Invisible Threat** — Stereotype threat impairs test performance
  (**steeleAronson1995**) by consuming working-memory capacity (**schmaderJohns2003**).
  Verified.
- **§2 The Psychological Shield** — A brief values-affirmation writing exercise buffers
  the threat (**cohen2006**). Verified.
- **§3 The Zoom-Out Effect** — Positive emotion broadens attention/cognition
  (broaden-and-build; **fredrickson2001**), the proposed mechanism for affirmation's
  effect. Verified.
- **§4 The Real World Data** — In Cohen et al.'s classroom studies, brief affirmations
  raised at-risk students' grades (**cohen2006**) with effects persisting ~2 years via a
  recursive cycle (**cohen2009**). Verified, with an added in-text caveat noting the
  effect is heterogeneous in replication.
- **§5 Your Pre-Exam Protocol** — Practical habit (pick values → write 15 min). Application;
  no new empirical claim.

---

## Reframed content
None cut. §4 strong-outcome wording tightened ("jumped significantly" → "rose"; attributed
to "that study"/"one study") and a replication caveat *added* to student-facing text;
since nothing was removed verbatim, there is no `data/cutContent.ts` entry for this module.
