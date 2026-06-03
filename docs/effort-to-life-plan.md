# Effort → Life simulator — plan (2026-06-03)

Connect the effort a student puts in **now** to the **lifestyle** it makes possible — the missing keystone of the app's chain (subjects → results → pathways → careers → **lifestyle**). A plan; not yet built.

## The critical reframe (from the evidence)

A naive "show them their future lifestyle" tool **backfires**, per strong evidence:
- **Positive fantasy alone saps energy.** Dwelling on an idealised future predicts *lower* effort and worse outcomes — in disadvantaged students, *more* absences and *lower* grades (Kappes & Oettingen 2011/2012). The brain "consummates" the goal in imagination and relaxes.
- **A money/lifestyle frame is risky for under-18s.** Financially-contingent self-worth → anxiety, lower wellbeing (Park et al. 2017); adolescent materialism tracks *lower* self-esteem.
- **Determinism harms agency.** A fixed "this effort → this salary/life" forecast cuts against growth mindset and can induce learned helplessness in lower-attaining teens.

What the same literature shows **works** (robustly, even at age 11):
- **WOOP / mental contrasting** (Wish → Outcome → **Obstacle/reality** → **Plan**): the best-validated, kid-safe mechanism (MCII meta-analysis g≈0.34; RCT gains at age 11). Vivid future imagery only motivates when *contrasted with present reality and bound to concrete action.*
- **Possibilities, not predictions** — branching futures the user steers, framed as "what becomes possible if…", preserving malleability.
- **Balanced possible selves + strategies** (Oyserman): a hoped-for self paired with the concrete strategy to reach it; identity-based ("what someone like me does").
- **Self-transcendent purpose** (Yeager 2014): connecting effort to a "why beyond the self" beats a self-interest frame for teen persistence.
- **Repetition + human warmth**: effects fade → boosters; self-guided works but face-to-face is stronger (loop in the guidance counsellor).

→ So the tool is a **WOOP-structured "possible life" simulator**, not a lifestyle fantasy generator.

## The design

**Name:** "Your Possible Life" (locked).

**Engine (mostly existing data):**
```
current grades  ─┐                              target grades ─┐
                 ▼  (best-6 Σ getPointsForGrade)               ▼
        current points (REALITY / "coast")            target points ("push")
                 │                                              │
                 ▼  reachBucket vs CAOCourse.typicalPoints      ▼
        careers reachable now                       careers reachable if you hit targets
                 │                                              │
                 ▼  CAREERS.matchStrings ↔ course.careerPaths   ▼
        salary {startK → experiencedK}  (Career Paths, Irish €)
                 ▼  irishNetPay()  ← NEW (2026 PAYE/USC/PRSI)
        take-home (entry → established)
                 ▼  lifestyleFromNet()  ← NEW (Daft rents + essentials → affordances)
        a tangible life: where you could live, share vs alone, disposable, car, save, travel
```

**The WOOP flow wrapped around it:**
1. **Wish/Outcome** — pick/seed a path (Future Finder top match; or "I haven't done the Future Finder yet" → pick a career manually). See the *life it makes possible* at entry → established: a vivid, plural, **possibilities** view — where you could live, independence, the rhythm of the week, money as *one* ingredient (independence/freedom/saving/travel), never a worth-score.
2. **Reality** — what your **current** grades project right now (current points → reachable careers → current lifestyle). The honest gap. *This contrast is what makes the vividness motivate rather than sap.*
3. **Plan** — the concrete bridge from now to there: current vs **target** grades, and the ready-made `computeBargains` "one grade up in {subject} = +{N} points → unlocks {course/career}". An if-then plan tied to *this term's* effort. Optionally a self-transcendent "who would this help / why does it matter to you" prompt.
4. **Possibilities, steerable** — swap careers, move the target, see other lives become possible. Explicitly "what becomes possible if…", malleable, never a verdict. Optional "share with my guidance counsellor."

## Screen-by-screen (refined — draft copy)

Five screens, mapping onto WOOP. Qualitative-led throughout; € shown as a quiet supporting line, never the headline. Tone: warm, plural, agency-first. Immersive colour-world register (like Career Paths / How They Did It), not the module shell.

**Screen 0 — Pick a future to explore** *(the Wish seed)*
- If Future Finder done → hero card = top match career, with "← swap" through the alternates (the other RIASEC recommendations). Sub-line: "From your Future Finder."
- Always present: a quiet button **"I haven't done the Future Finder yet →"** → opens a manual picker over the 12 `CAREERS` (search/browse). No judgement either way.
- Copy: *"Pick a path and we'll explore the life it could open up. Not a prediction — a possibility you steer."*

**Screen 1 — The life this could open up** *(Wish / Outcome — vivid, plural)*
- Lead with the tangible life, not the salary. A toggle/slider: **Starting out → A few years in** (entry → established), so the progression is felt, not just stated.
- **Render: affordance card + a one-line vignette on top.** The card is the backbone — concrete affordances with icons (where you could live + the honest *share-vs-alone* reality, whether a car fits, room to save, room to travel) and a single quiet €/mo line at the foot. Above it, one warm second-person sentence for emotional grounding, kept plural/non-deterministic.
- Money appears once, in support: *"~€X a month take-home, starting out."* Never a worth-score.
- Caveat baked in: *"One version of the story. Salaries are typical, not promised — and rents are tight right now. It's a possibility, not a forecast."*

**Screen 2 — Where you're heading right now** *(Reality — the honest contrast)*
- Reads the student's **current** grades → current points → what that projects today.
- Names the gap plainly but without fear: *"Right now your grades project ~[X] points. [This path] usually opens around [Y]. That's a gap of [Z] — and the next screen shows exactly how it closes."*
- This contrast is the active ingredient: vivid future *minus* honest present is what makes WOOP motivate instead of sap.

**Screen 3 — Your bridge from here to there** *(Plan — concrete, if-then)*
- current vs **target** grades side by side; `computeBargains` powers the line: *"One grade up in [subject] = +[N] points → puts [course/career] in reach."*
- An if-then plan tied to *this term's* effort, not a vague someday.
- The self-transcendent prompt (optional, one line): *"Who, beyond you, would this matter to? Who could it help?"* — a save-able reflection.

**Screen 4 — Steer it** *(Possibilities, malleable)*
- Swap careers, nudge the target up, watch other lives become possible. Framed as *"what becomes possible if…"*, never a verdict.
- Saved to `effortLifeSim` so it persists; "share with guidance counsellor" deferred to a later pass.

**Tool name candidates:** "Your Possible Life" · "Future You" · "Life in Focus" · "The Long Game".

## The model (researched, cited)

**Irish take-home (`irishNetPay(gross, year=2026)`):**
- Income tax: 20% to €44,000, 40% above; minus €4,000 credits (personal €2,000 + PAYE €2,000), floored at €0.
- USC: €0 if income ≤ €13,000 (cliff), else banded 0.5% (≤€12,012) / 2% (→€28,700) / 3% (→€70,044) / 8% (above). [2025: 2% ceiling €27,382.]
- PRSI: 4.2% on all earnings if weekly > €352 (tapered credit €352.01–€424).
- Worked: €50k gross → ~€39,667 net (~€3,306/mo). Sources: revenue.ie, gov.ie, citizensinformation.ie.

**Lifestyle (`lifestyleFromNet(netMonthly, region)`):** Daft Q4-2025 rents (Dublin 2-bed €2,517 / room ~€876; national room €775; Cork/Galway/Limerick rooms ~€450-700; Waterford/regional lower) + essentials ~€600-900/mo (utilities, groceries, transport, phone) + car ~€700-1,000/mo for a young driver. `disposable = net − rent − essentials`. The 30% rule (rent ≤ ~35% net comfortable / 35-45% stretched / >45% rent-burdened). **The real divider is share-vs-alone, not city.** Tiers: Getting-by · Independent-lite · Comfortable · Thriving. Sources: Daft.ie Q4 2025, CSO, OUTsurance, gradireland.
- **Honesty caveats baked into copy:** rents are a floor (up 13 of 14 years; acute supply shortage), 1-bed euro figures are *modelled* (~0.8× 2-bed), salaries are typical not guaranteed, "possibilities not predictions."

## Reuse vs new
- **Reuse:** `getPointsForGrade` + best-6 reducer (run on current AND target grades); `computeBargains` (the plan panel — points gain per grade); `reachBucket` + `CAOCourse.typicalPoints`; `CAREERS`/`matchStrings` ↔ courses (the `coursesFor` join); `SalaryBand`; `useProgress()` live `studentProfile`; the GC dashboard (optional share). JC users fall out cleanly (points = 0).
- **New:** `irishNetPay()` + `lifestyleFromNet()` (small, pure, source-grounded, unit-tested like the RIASEC engine); `useEffortLifeSim` hook (`progress/{uid}.effortLifeSim` namespace — saved path, persists across sessions); the component + WOOP flow. New tool in the Innovation Zone (no change to existing tools).

## Ethical guardrails (non-negotiable, from the evidence)
- **No fear/scarcity** copy ("don't end up broke", countdown-to-ruin). Aspirational + agency only.
- **No worth-as-income.** Money is one ingredient of a life; never a single number that ranks the student.
- **Possibilities, not predictions** — malleable, steerable, "what becomes possible if…"; never a fixed forecast.
- **Pair dream with reality + plan** (WOOP) — never let the user just bask in the bright future.
- **Off-ramp / positive default** for students who find future-imagining anxious; "a snapshot you author, not a destiny."
- **Minors / decision support** — frame alongside the guidance counsellor; ties to the outstanding consent work.

## Decisions locked (2026-06-03)
1. **Money vs life: lead qualitative, money in support.** Headline is the tangible life; € figures are present but secondary. (Safest per the teen-wellbeing evidence.)
2. **Include the self-transcendent "why" prompt now** (Yeager 2014) — one optional reflective step in the Plan stage.
3. **Defer the "share with guidance counsellor" hook** — ship student-facing first; wire the GC surface in a follow-up.
4. **Refine the plan first** (this pass), then build.

## Resolved this refinement pass (2026-06-03)
- **Tool name: "Your Possible Life"** — plural, malleable, on-message with "possibilities not predictions".
- **Screen-1 rendering: affordance card + a one-line vignette on top.** The card (live/car/save/travel + a quiet €/mo line) is the scannable, honest, steerable backbone; one warm second-person sentence above it for emotional grounding (kept plural and non-deterministic).

## Sources
**Take-home:** revenue.ie tax/USC; gov.ie PRSI; citizensinformation.ie. **Cost of living:** Daft.ie Q4 2025 Rent Report (RTÉ/Examiner/TheJournal), CSO, OUTsurance car-cost 2025, gradireland/Indeed grad salaries, Numbeo. **Science:** Ersner-Hershfield 2009 (future-self continuity & assets); Hershfield 2011 (age-progressed avatars, d≈.5–.77); van Gelder 2013; Grekin 2025 review; Oettingen/Kappes (positive-fantasy backfire; MCII g=.336); Oyserman possible-selves / School-to-Jobs (2-yr effects); Yeager 2014 (self-transcendent purpose); Park 2017 (financially-contingent self-worth); Yeager 2019 (growth mindset context-dependence).
