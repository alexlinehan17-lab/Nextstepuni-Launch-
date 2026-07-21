# Module Content Audit — 2026-07-21

Sweeping audit of all 83 course modules (54 general + 29 subject), run for the Year Plans
curriculum build. Every module read in full (including essentials/junior variants and
PersonalStory testimonials) against a skeptic-vetted appropriateness rubric — calibration
anchor: the removed urine-colour hydration advice. Every medium/high flag was independently
verified by two adversarial reviewers; flags below are the survivors. 295 agents total.

Curriculum outputs live in `yearPlans.ts` (Year Plans page). This file is the flag ledger.

## HIGH — 34 confirmed

### reframing-catastrophic-thoughts-protocol
- **Where:** components/CatastrophicThinkingModule.tsx — module-level (sections defined lines 414-428; ThoughtRecord defaults line 26 and step 1-2 lines 37-38; DownwardArrowDrill prompt lines 336-348); applies per rubric amendment 4
- **Quote:** "placeholder={index === 0 ? "I'll fail my exam" : ...} ... 'Your worst fear' ... intensity: 90 ... placeholder="e.g., Panic""
- **Concern:** Anxiety-focused module simulates panic — a worst-fear elaboration drill, an emotion-intensity slider defaulting to 90% with 'Panic' as the modelled emotion, and harsh self-talk cards ('You're going to fail', 'You're not smart enough') — with ZERO support signposting anywhere in the file: no 'if this is bigger than exams, talk to someone' line, no mention of a trusted adult, school counsellor, Jigsaw, or Childline. The individual exercises are legitimate CBT/ACT psychoeducation (exempt per the therapeutic-exercise amendment), but the module is live to the junior path (jcStatus live, curriculum both) and essentials mode renders all three anxiety interactives identically for 12-15yo DEIS students — the cohort least likely to have other supports. Flagged once at module level per amendment 4.
- **Suggested action:** Add one warm, brief signpost callout rendered in BOTH essentials and full modes (e.g. at the end of section 1 or in the Action Plan): 'These tools are for exam nerves. If your worries feel bigger than exams, talk to someone — a parent, a teacher, jigsaw.ie, or Childline 1800 66 66 66.' Keep it non-clinical in tone to match the module register.

### learning-math-protocol
- **Where:** components/LearningMathModule.tsx lines 353 (essentials) and 356 (full), section 'The New Game'
- **Quote:** "A H6 in Maths beats a H3 in any other subject."
- **Concern:** Factually wrong CAO arithmetic (rubric item 6, decision-relevant). H6 = 46 points + 25 bonus = 71, which is LESS than a H3's 77 points. The true claim is that a H6 in HL Maths beats a H4 (66). The error appears in both the essentials and full branches, and it directly informs students' Higher-vs-Ordinary level choice — any maths teacher or guidance counsellor would challenge it, and an accreditation reviewer certainly would.
- **Suggested action:** Correct to the H4 comparison ('a H6 in Maths (71 points with the bonus) is worth more than a H3... ' is wrong; use 'more than a H4 in any other subject') in both branches, and re-verify the Highlight tooltip wording alongside it.

### mastering-english-protocol
- **Where:** components/MasteringEnglishModule.tsx lines 327 and 332 (section 4, Comparative Study — both essentials and full branches)
- **Quote:** "Important: "Theme or Issue" is NOT a mode for Higher Level. Don't waste your time preparing for it."
- **Concern:** Hard-coded 2026 exam-year claim delivered as a directive to skip preparation. The 2026 LC exam has already been sat (today is 2026-07-21), so the live audience is now the 2027 cohort, and the HL comparative modes rotate annually from the four-mode set. If Theme or Issue IS a 2027 mode, the app is actively telling students not to prepare a mode they will be examined on — direct, materially harmful exam misdirection, and exactly what a teacher or accreditation reviewer would challenge (rubric item 6).
- **Suggested action:** Make exam-year prescriptions data-driven (single dated constant or per-cohort config) and update against the DES/SEC prescribed-material circular for 2027; until verified, reframe to 'check which three modes are prescribed for YOUR exam year' and drop the 'don't waste your time' directive.

### exam-crisis-management-protocol
- **Where:** ExamCrisisManagementModule.tsx lines ~615-680 (wrapSections) and 1017-1046 (WRAP intro cards); no signpost anywhere in the module
- **Quote:** ""What are the early signs that you're heading into crisis?" — suggestions: 'Feeling hopeless', 'Withdrawing from people'; card 4: "Your 'break glass' instructions for when things get really bad.""
- **Concern:** Module-level signposting gap (rubric item 2 + amendment 4). The WRAP builder borrows a clinical mental-health recovery instrument and asks students — including 12-15yo, since WRAPBuilder renders identically in essentials mode — to self-identify crisis triggers and warning signs including 'Feeling hopeless' (a depression/risk indicator), then write a personal 'crisis plan', with zero 'if this is bigger than exams, talk to an adult / Jigsaw / Childline / 50808' signposting anywhere in the module. 'Call a trusted person' appears only as one optional suggestion pill. For a DEIS-heavy, jcStatus-live audience this is the exact gap flagged in CatastrophicThinkingModule, amplified by explicit crisis/hopelessness vocabulary.
- **Suggested action:** Add a brief, warm support signpost (trusted adult + Irish youth services) to the crisis-planning section, and consider softening 'crisis'/'break glass' register on the junior path.

### subject-english-protocol
- **Where:** subjectContentLanguages.ts lines 29, 37, 62, 68, 77, 94, 108 (Section 1 prose + 'Unseen Poetry' Highlight description, repeated in Sections 3, 4, 5, 6)
- **Quote:** "Unseen Poetry (a poem you have never seen before, followed by a comparison with a second poem — 70 marks)"
- **Concern:** Rubric item 6 (teacher-challengeable factual claim), amplified by amendment 1 (the detailed wrong breakdown lives in a Highlight description: 'guided question on it (20 marks), then get a second poem and compare both (30 marks for the comparison, 20 marks for the second poem individually)'). The actual LC HL Paper 2 poetry section is Unseen Poem (20 marks) + Prescribed Poetry essay on a studied poet (50 marks). The module invents a 70-mark two-poem unseen comparison that does not exist, and — in a module subtitled 'Your Complete English Exam Guide' — omits Prescribed Poetry (50 marks, the 8 prescribed poets) entirely. Downstream advice compounds it: the Section 4 time plan allocates '70 minutes for Unseen Poetry', and Sections 5-6 direct all poetry study to unseen practice with zero mention of studied poets. A student following this module would walk into Paper 2 unprepared for a 50-mark question. Copyright memory confirms prescribed poems are cleared for use, so the omission is not a rights constraint.
- **Suggested action:** Rewrite the poetry content to the real structure (Unseen 20 + Prescribed 50 at HL), add a Prescribed Poetry strategy passage, and correct the time plan; verify against the current SEC exam paper before shipping (per the accreditation dossier rule).

### subject-english-protocol
- **Where:** subjectContentLanguages.ts lines 28 and 63 (Section 1 paragraph 2; Section 3 paragraph 4)
- **Quote:** "Section I has two comprehension texts (Question A, worth 50 marks each — you do both)"
- **Concern:** Rubric item 6. Paper 1 Section I actually presents three texts; candidates answer Question A (50 marks, comprehension) on one text and Question B (50 marks, a functional/short writing task) on a different text. The module claims students answer two Question A's and never mentions Question B anywhere — a whole 50-mark question type (12.5% of the grade) is missing from an exam-structure guide. Section 3 repeats it: 'The comprehension section (Question A on Paper 1) delivers 100 marks across two texts.' Any English teacher would immediately challenge this, and a student could fail to prepare Question B genres at all.
- **Suggested action:** Correct Section I to the three-texts / QA-on-one, QB-on-another structure and add Question B (functional writing) coverage; check current SEC arrangements when fixing.

### subject-irish-protocol
- **Where:** subjectContentLanguages.ts line 136, Section 1 'How Irish Actually Works'
- **Quote:** "Paper 1 worth **120 marks** (20%), Paper 2 worth **160 marks** (approximately 27%), and the [[Scrúdú Cluastuisceana (Aural Exam)]] worth **80 marks** (approximately 13%)"
- **Concern:** Rubric item 6 (factual, teacher-challengeable). The SEC HL breakdown is: Oral 240 (40%), Paper 1 = 160 marks (Cluastuiscint 60 = 10% + Ceapadóireacht 100), Paper 2 = 200 marks (33%). The module's 120/160/80 split is wrong on every component except the oral, and the highlight at line 143 repeats 'worth 80 marks' for the aural. The OL claim '240 marks out of 500... 48%' (same paragraph) is also unverified and likely wrong. In a module whose entire premise is mark-weighting strategy, wrong weights actively misdirect study time and would be caught instantly by any Irish teacher or accreditation reviewer.
- **Suggested action:** Correct to the SEC figures (Paper 1: 160 incl. Cluastuiscint 60; Paper 2: 200; aural 60 = 10%) in both the paragraph and the aural Highlight; verify the OL total/percentage against the SEC before restating it.

### subject-french-protocol
- **Where:** subjectContentLanguages.ts lines 248 and 297 (Sections 1 and 4)
- **Quote:** "The written exam is a **2 hour 50 minute paper**"
- **Concern:** Rubric item 6 (factual). The LC French written paper is 2 hours 30 minutes; the 40-minute aural is a separate test. The 2h50 figure appears twice and drives concrete timing advice ('roughly 70 minutes for reading comprehension, 80 minutes for written expression, and 10 minutes for review') — which also only sums to 160 minutes, internally inconsistent with the stated 2h50. Students following this plan in the real exam would misbudget their time.
- **Suggested action:** Fix the duration to the correct SEC timetable figure and recompute the per-section time allocation so it sums to the paper length.

### subject-german-protocol
- **Where:** subjectContentLanguages.ts lines 355-365 (Section 1 paragraphs + all five Highlight descriptions), repeated at lines 388-390
- **Quote:** "[[Aural Exam]] worth **100 marks** (25%), and the [[Written Exam]] worth **200 marks** (50%)"
- **Concern:** Rubric item 6 (factual overreach a teacher would challenge), amplified by amendment 1 (claims live in Highlight descriptions too). The stated LC German HL breakdown (Oral 100/25%, Aural 100/25%, Written 200/50%, Reading ~100) does not match the actual SEC allocation: Oral 100 (25%), Aural 80 (20%), Written 220 (55%) with Reading Comprehension ~120 and Written Production ~100. The error is repeated in Sections 1 and 3 and in five tooltip descriptions, and it materially distorts the module's central 'where your marks are' advice (e.g. 'The oral and aural together determine half your grade' — actually 45%). Any German teacher or accreditation reviewer would catch this immediately.
- **Suggested action:** Verify every figure against the current SEC LC German HL specification/marking scheme and correct the breakdown in all paragraphs and Highlight descriptions consistently (also re-derive dependent claims like 'half your grade before you write a single essay').

### subject-german-protocol
- **Where:** subjectContentLanguages.ts line 358 and line 407 (Sections 1 and 4)
- **Quote:** "The written paper runs for **2 hours 50 minutes**"
- **Concern:** Rubric item 6. The LC German HL written paper is 2 hours 30 minutes (the ~40-minute aural is a separate session). The module's own time-allocation advice in Section 4 ('approximately 70 minutes for reading, 80 minutes for writing, and 10 minutes for review') sums to 160 minutes, contradicting its stated 170-minute duration either way — students following this timing plan in the real 150-minute paper would run out of time.
- **Suggested action:** Confirm the current paper duration against the SEC timetable and rewrite the Section 4 time allocation so it sums to the correct duration.

### subject-spanish-protocol
- **Where:** subjectContentLanguages.ts lines 464, 471-473 (Section 1 paragraph 1 + Aural/Written/Reading Highlight descriptions)
- **Quote:** "The [[Aural Exam]] is worth **100 marks** (25%), and the [[Written Exam]] is worth **200 marks** (50%) ... 50% of your grade is determined by your speaking and listening skills"
- **Concern:** Rubric item 6 (amendment 1: claims live in Highlight descriptions too). The mark allocations are wrong and are contradicted by the repo's own verified source, examiner-reports/spanish/2025-insights.md: HL aural is 80 marks (20%), the written paper is 220 marks (55%), and oral+aural together are 45%, not 50%. 'Reading Comprehension (approximately 100 marks)' is also off (comprehension totals ~120 across Sections A and B), and the paper is three sections with a 50-mark Linked Question, not a two-way reading/writing split. In a module whose entire value proposition is where the marks are, any Spanish teacher or accreditation reviewer would challenge this immediately, and students would misweight their preparation.
- **Suggested action:** Rewrite Section 1 paragraphs and the Aural/Written/Reading Comprehension Highlight descriptions against examiner-reports/spanish/2025-insights.md (Oral 100/25%, Aural 80/20%, Written 220/55%; Sections A/B/C structure incl. the 50-mark Linked Question), and log the correction per the dossier process.

### subject-spanish-protocol
- **Where:** subjectContentLanguages.ts lines 465 (Section 1) and 543 (Section 6 action plan)
- **Quote:** "your prepared topic (tema preparado) ... and discussion of visual or situational stimuli"
- **Concern:** Rubric item 6. The LC Spanish oral has no 'tema preparado' component — per the in-repo syllabus (examiner-reports/spanish/spanish-syllabus.md, p.25 'Oral Assessment'), it consists of (a) general conversation (with an optional literary-work discussion) and (b) a role-play situation, 15 minutes allotted. The module never mentions the role-play, and the action plan doubles down ('prepare your oral topic (tema preparado)'), directing students to rehearse a component that does not exist while leaving them unprepared for the one that does. This reads as a generic-template import (the French document option) rather than Spanish-specific fact.
- **Suggested action:** Rewrite the oral description and Section 6 action step around the actual conversation + role-play structure (and the optional literary-work discussion), citing the syllabus.

### subject-spanish-protocol
- **Where:** subjectContentLanguages.ts line 467 (Section 1 paragraph 4)
- **Quote:** "The written paper runs for **2 hours 50 minutes**"
- **Concern:** Rubric item 6. The SEC LC Spanish HL written paper is 2 hours 30 minutes (the ~40-minute aural is sat separately after it); 2h50 appears carried over from another subject's template. Not confirmable from in-repo sources (syllabus/marking schemes don't state duration), but a timing error in an exam-strategy module directly distorts students' timed-practice pacing.
- **Suggested action:** Verify against the current SEC examination timetable and correct; adjust the '40 minutes for a Higher Level composition' pacing advice in Section 5 if needed.

### subject-italian-protocol
- **Where:** subjectContentLanguages.ts lines 572-582 (Section 1) and 605-608 (Section 3)
- **Quote:** "[[Aural Exam]] worth **100 marks** (25%), and the [[Written Exam]] worth **200 marks** (50%)"
- **Concern:** Rubric item 6 (factual overreach a teacher/accreditation reviewer would challenge): the mark allocation is wrong, and the repo's own verified source contradicts it. examiner-reports/italian/2025-marking-scheme.md documents LC Italian HL as Reading 120 / Written Production 100 / Aural 80 / Oral 100 (aural = 20%, written paper = 220 = 55%); the syllabus extraction confirms Aural 20%, Reading 30%, Writing 25% at HL. The module also says Reading Comprehension is 'approximately 100 marks' (actual 120). Since the module's stated purpose is 'understand how marks are allocated' and Section 3 builds strategy on 'the aural exam at 100 marks', the error misdirects students' study weighting toward the aural and away from the written paper.
- **Suggested action:** Correct Sections 1 and 3 to the verified split (Oral 100/25%, Aural 80/20%, Written paper 220/55% comprising Reading ~120 + Written Production ~100), citing the 2025 marking scheme already in examiner-reports/italian/.

### subject-italian-protocol
- **Where:** subjectContentLanguages.ts line 572 (Section 1, paragraph 1)
- **Quote:** "The structure is identical to French, German, and Spanish — if you understand one, you understand the framework for all of them."
- **Concern:** Rubric item 6: overstated equivalence the repo's own verification file refutes. examiner-reports/italian/2025-marking-scheme.md notes Italian HL carries a prescribed-novel literature strand (Calvino, Sciascia, plus an unseen literary passage) with its own essay band appendix, absent from the French/Spanish 2025 schemes, plus a harsher reading wrong-language penalty. The module never mentions prescribed literature at all, so a student relying on it would be blindsided by an examined component.
- **Suggested action:** Soften to 'follows the same broad framework' and add coverage of the prescribed-literature strand as an examined element of the written paper.

### subject-japanese-protocol
- **Where:** subjectContentLanguages.ts lines 681-684 (Section 1 paragraphs) and line 735 (stroke-order claim)
- **Quote:** "follows the same three-component structure as the European languages ... The [[Oral Exam]] is worth **100 marks** (25%), the [[Aural Exam]] is worth **100 marks** (25%), and the [[Written Exam]] is worth **200 marks** (50%)"
- **Concern:** Rubric item 6 (factual overreach a teacher/accreditation reviewer would challenge): the claimed 25/25/50 split is asserted to be 'the same three-component structure as the European languages', but LC HL European languages are weighted 25% oral / 20% aural / 55% written — so the sentence is internally inconsistent with the figures beside it, and the Japanese-specific figures (100/100/200, 40-minute aural, 2h50 written, ~100+~100 reading/writing split, oral passage read-aloud) carry no Cite references anywhere in the entry, unlike the accreditation standard the app holds itself to. The adjacent claim that 'Kanji written with incorrect stroke order often look off to the examiner ... may not be accepted' also presents a marking consequence not obviously grounded in an SEC marking scheme. Wrong exam-format specifics are exactly the kind of claim that could embarrass the app and mislead a student's exam-day expectations.
- **Suggested action:** Verify every mark weighting, duration, and component claim against the SEC LC Japanese syllabus/papers in exam-papers/ or examiner-reports/, correct or hedge the 'same structure as European languages' sentence, soften the stroke-order marking claim to legibility, and add Cite-backed references (or reframe to non-prescriptive language) per the accreditation dossier rule.

### subject-applied-maths-protocol
- **Where:** /Users/alexlinehan/Nextstepuni-Launch-/subjectContentStem.ts lines 152-155 (Section 1 'How Applied Maths Actually Works'), propagating through Sections 3-6
- **Quote:** "There is no coursework, no practical component, and no oral or aural. It is purely an exam-based subject."
- **Concern:** Rubric item 6: the whole module teaches the pre-2023 Applied Maths syllabus. The current specification (introduced Sept 2021, first examined 2023; verified against the official spec on curriculumonline.ie) assesses via a 2.5-hour written exam worth 80% (400 marks) PLUS a mathematical modelling project worth 20% (100 marks), and its strands (mathematical modelling, networks/graph theory, difference equations, algorithms, kinematics/dynamics) replaced the old one-question-per-topic paper. Related claims are equally wrong for current students: 'The paper contains 10 questions, and you must answer 6 of them... giving a total of 300 marks', 'Each topic gets exactly one question every year', and topic lists featuring dropped old-syllabus material (SHM, conical pendulums, oblique impacts, ladders/statics). A student following the module's core strategy — 'you pick the 6 topics you are strongest in and ignore the rest' — would mis-prepare for the actual paper and skip the modelling project worth 20% of their grade. Any teacher or accreditation reviewer would challenge this immediately.
- **Suggested action:** Rewrite the entire subject entry against the current Applied Mathematics specification and the 2023-2026 SEC papers/marking schemes (Section A concepts-and-skills / Section B contexts-and-applications format, plus a dedicated modelling-project section). Salvageable general advice (free-body diagrams, sign conventions, follow-through marks, defining variables) can carry over.

### subject-chemistry-protocol
- **Where:** subjectContentStem.ts lines 399-414 (Section 1 'How Chemistry Actually Works'), propagating to lines 438, 444, 493
- **Quote:** "Section A is worth 120 marks and typically contains around 5 experiment-based questions -- you must answer 3 of them. Each is worth 40 marks... Section B is worth 280 marks and contains 8 questions -- you must answer 5 of them. Each question is worth 56 marks."
- **Concern:** Rubric item 6 (factual overreach a teacher/accreditation reviewer would challenge): this is the Leaving Cert PHYSICS paper structure, not Chemistry — the text even says 'Like Physics'. The real SEC Chemistry paper has 11 questions (Section A = Q1-3 mandatory experiments, answer at least two; Section B = Q4-11), answer 8 total at 50 marks each. The wrong figures repeat in the highlight tooltips (lines 405-406, per amendment 1: non-prose text in scope), the section bullets (411-413), the 'score 100-120 marks in Section A' high-value claim (438, 444), and the action-plan timing split '45 minutes for Section A and 2 hours 15 minutes for Section B' (493). A Chemistry teacher would spot this immediately, and a student following the '3 from ~5' rule would misplan their paper. Also violates the project's own syllabus-alignment directive.
- **Suggested action:** Rewrite Section 1 (and dependent tooltips, bullets, mark-total claims, and the action-plan timing) against the actual SEC Chemistry paper: 3-hour paper, 400 marks, 8 answers at 50 marks each, at least two from Section A's three experiment questions; recompute the per-question timing and the Section A mark ceiling (max 150 if all three answered).

### subject-ag-science-protocol
- **Where:** subjectContentStem.ts line 761 (Section 1); mirrored in courseData.ts line 747 description
- **Quote:** "the CBAs themselves do not carry a direct percentage of the final exam mark in the same way as the CS ALT"
- **Concern:** Factual overreach an Ag Science teacher or accreditation reviewer would immediately challenge (rubric item 6). Leaving Cert Agricultural Science has NO Classroom-Based Assessments — CBAs are a Junior Cycle construct. The LC practical component is the Individual Investigative Study (IIS), which is worth 25% of the grade (written paper = 75%). The module repeatedly calls this 'CBAs' and tells students it carries no direct percentage of the mark, which could lead a student to under-invest in a full quarter of their Leaving Cert grade. This is a material misstatement of the assessment structure, not a nuance.
- **Suggested action:** Replace all 'CBA'/'Classroom-Based Assessment' references throughout the entry (Section 1 paragraphs + highlight term at line 764, and the courseData description) with the Individual Investigative Study (IIS), and correct the weighting to state the IIS is worth 25% and the written paper 75%. Re-frame Section 1 accordingly.

### subject-accounting-protocol
- **Where:** subjectContentBusiness.ts lines 29-31 (Section 1 'How Accounting Actually Works'), repeated in Sections 3 and 6 (lines 75-78, 151-153)
- **Quote:** "**Section 1** contains short questions worth **120 marks** in total — you answer **four** out of six questions, each carrying 30 marks... **Section 2** has three compulsory long questions worth **60 marks each** (180 marks total). **Section 3** is one extended question worth **100 marks** — ... typically a full set of final accounts."
- **Concern:** The described exam structure is fabricated and contradicts the actual SEC paper — and the repo's own verified sources. Per examiner-reports/accounting/2024-insights.md (verified against the 2024 SEC marking scheme) and data/knowledge/subjectTiming.ts: Section 1 = Financial Accounting, 120 marks (one 120-mark Q1 OR two of Q2-Q4 at 60 each — not six 30-mark short questions); Section 2 = Financial Accounting, 200 marks (TWO of three at 100 each — not three compulsory 60-mark questions); Section 3 = MANAGEMENT Accounting, 80 marks (one of two — not a 100-mark final-accounts question; final accounts are Section 1 Q1). Rubric item 6 at its strongest: any Accounting teacher or accreditation reviewer would immediately challenge this, and every downstream strategic claim ('Section 3 = 25% of the paper', 'Section 1 + Section 3 = 220 of 400', 'quick wins zone', the Section 2 topic pattern) inherits the error. A student who trusted it would prepare for a paper that does not exist — e.g. drilling 'Section 3 final accounts questions' when Section 3 is budgeting/costing.
- **Suggested action:** Rewrite Sections 1, 3, 4 and 6 against examiner-reports/accounting/2024-insights.md (already in-repo and verified): correct section names, mark totals, and choice structure; move final accounts to Section 1 Q1 (120 marks); present Section 3 as Management Accounting (80 marks). Record the rewrite in the compliance dossier/cut log per CLAUDE.md.

### subject-accounting-protocol
- **Where:** subjectContentBusiness.ts line 98 (Section 4) and lines 139-142 (Section 5 bullets)
- **Quote:** "allocate time proportionally: roughly 25 minutes for Section 1, 75 minutes for Section 2 (25 each), and 45 minutes for Section 3"
- **Concern:** Actionable time-management advice computed from the wrong structure. On the real paper, Section 1 (120 marks) warrants ~54 minutes, Section 2 (200 marks) ~90 minutes, Section 3 (80 marks) ~36 minutes (subjectTiming.ts agrees). Following the module's 25/75/45 split would starve the highest-value section (Section 1 Q1) and over-invest elsewhere — advice that could measurably cost marks in the exam hall. The bullets '45 minutes for 100-mark questions, 25 minutes for 60-mark questions' rest on the same fabricated question sizes.
- **Suggested action:** Recompute all timing guidance from the verified 400-mark/180-minute structure (0.45 min per mark) once the structure in flag 1 is corrected.

### subject-economics-protocol
- **Where:** subjectContentBusiness.ts lines 356-359 (Section 1), pervading Sections 3, 4, 6
- **Quote:** "**Section A** contains short questions worth **100 marks (25%)**. You answer **5 out of 9** questions... **Section B**... You choose **4 from 7** questions, each worth **75 marks**"
- **Concern:** The entire module describes the pre-2019 Economics syllabus exam, retired after 2020. The repo's own SEC 2025 marking scheme (examiner-reports/economics/2025-insights.md) confirms the current exam: Section A is 75 marks of stimulus-based short questions, Section B is six themed long questions (Q11-Q16) with N@M descriptor marking, the written paper is only 80% of the grade, and the Student Research Project (20%) is never mentioned once. Every downstream number — '400 marks', '22 seconds per mark', '28-30 minutes per long question', the timing bullets — is wrong for current students. A teacher or accreditation reviewer would reject this immediately (rubric item 6).
- **Suggested action:** Rewrite all six sections against the current specification using examiner-reports/economics/2025-insights.md (descriptor bands, N@M template, calculation/diagram mark grids) and add SRP coverage; verify the diagram list (kinked demand curve, Keynesian Cross) against the 2019 specification's learning outcomes while doing so.

### subject-history-protocol
- **Where:** subjectContentHumanities.ts line 28 (Section 1 'How History Actually Works'), cascading to lines 60 and 66
- **Quote:** "There is no second paper and no coursework component — everything rides on this one sitting."
- **Concern:** Factually wrong (rubric item 6): LC History HL and OL both include the pre-submitted Research Study Report, coursework worth 20% of the total grade (100 of 500 marks). The error cascades — the paper is framed as 'worth a total of 400 marks' as if that were the whole grade, and the Document Question is called 'a full 25% of your grade' (it is 25% of the written paper but 20% of the grade). Any History teacher or accreditation reviewer would challenge this instantly, and it could lead students to deprioritise a real 20% component they must submit before the exam.
- **Suggested action:** Rewrite Section 1 to state the RSR exists (20%, submitted in advance) and that the written paper is 400 of 500 marks; correct the '25% of your grade' claim in Section 3 to 20% (or '25% of the written paper'); check against the examiner-reports/history insights per the repo's accreditation rule.

### subject-politics-and-society-protocol
- **Where:** subjectContentHumanities.ts lines 269 and 275 (Section 1 paragraph 2 + 'Section A' highlight description)
- **Quote:** "[[Section A]] consists of **short-answer questions** worth a total of **80 marks**"
- **Concern:** Factual error (rubric item 6) contradicted by the repo's own verified SEC materials: examiner-reports/politics-society/2025-insights.md and 2024-verification.md confirm Section A is 50 marks (10 questions x 5 marks, answer 10 of 15), Section B is a single 150-mark data/documents question, and Section C is 200 marks (2 x 100). An exam-structure guide getting the mark allocation wrong is exactly what a teacher or accreditation reviewer would immediately challenge, and it misleads students' effort allocation.
- **Suggested action:** Correct Section A to 50 marks (10 x 5, best 10 of 15) and add the real Section B (150 marks) and Section C (200 marks, two 100-mark essays) figures, sourced from the marking-scheme extractions already in the repo.

### subject-religious-education-protocol
- **Where:** subjectContentHumanities.ts lines 388-397 (Section 1, 'How Religious Education Actually Works') and dependent Sections 3-6
- **Quote:** "[[Section A]] is the short-answer section, worth **80 marks** ... [[Section B]] is worth **120 marks** and consists of **response-to-stimulus** material ... [[Section C]] is the extended essay section, worth **200 marks** — a full **half of the exam paper**"
- **Concern:** Rubric item 6, at the it-would-embarrass level: the entire exam anatomy is invented. Per the SEC marking schemes archived in this repo (examiner-reports/religious-education/2025-insights.md, cross-verified against 2024), the written paper is 320 marks (not 400) built from Unit One (Section A, one structured 80-mark question — not short-answer recall), Unit Two (160 marks, two of Sections B/C/D, which are content areas: Christianity, World Religions, Moral Decision-Making — not a stimulus format), and Unit Three (80 marks). There is no 200-mark essay section; 'Section C' is actually World Religions worth 80. Every downstream strategy claim ('Section C ... half the entire paper', the 60-70 min / 80 min timing split in Section 4, 'practise 5 past Section B stimulus questions' in Sections 5-6) inherits the error, so a student following this module would misallocate study time and be confused by any real past paper. An RE teacher or the DCU accreditation reviewer would spot this immediately.
- **Suggested action:** Rewrite the module's structural spine from the repo's own verified sources (examiner-reports/religious-education/2025-insights.md and the 2024/2025 marking schemes): 320-mark paper, Unit One/Two/Three architecture, section choice mechanics (two of B/C/D; one of F-J), and rebuild the high-value-zone, timing, and action-plan advice on the real choice/banding economics. Record the correction in the compliance dossier per CLAUDE.md.

### subject-religious-education-protocol
- **Where:** subjectContentHumanities.ts line 407 (Section 2 paragraph) and line 413 (Highlight description for 'cumulative marking')
- **Quote:** "The examiner uses [[cumulative marking]] — each relevant, well-explained point adds to your total"
- **Concern:** Rubric item 6, aggravated by amendment 1 (the claim also lives in a Highlight tooltip: 'Each relevant, well-explained point adds to your mark total ... there is no cap on quality'). This is the direct opposite of how LC RE is marked. The repo's own verified insights state: 'Unlike Geography (SRP tariff) or History (cumulative marking by paragraph), RE is marked holistically band-by-band ... There is no adding-up of points; there is one band per question', with six grade bands and a descriptive-answer cap at the Fair ceiling — a mechanism stable across the 2024 and 2025 schemes. Teaching students to accumulate points encourages exactly the descriptive list-writing the real scheme caps at 21/40.
- **Suggested action:** Replace 'cumulative marking' (paragraph AND Highlight description) with the real holistic band model: four descriptor dimensions (Marking Criteria evidence, relevance, skill, factual accuracy), six bands, and the descriptive-answer cap when a higher-order command word (e.g. Compare, Evaluate) is answered descriptively. This is actually a more useful strategy lesson than the false one.

### subject-religious-education-protocol
- **Where:** subjectContentHumanities.ts lines 388/394 (Section 1 + Highlight), 422/428 (Section 3), 440 (Section 4), 456 (Section 5), 470/480 (Section 6)
- **Quote:** "Coursework Journal ... A reflective journal completed during the course, covering your engagement with religious education topics"
- **Concern:** Rubric item 6: mischaracterises the real assessment component. SEC LC RE coursework (20%) is a Coursework Booklet on ONE prescribed title chosen from Section E or H, marked on research/analysis/evaluation descriptor grids (marking scheme pp.33-36) — not a reflective journal with 'entries after each topic'. The repeated advice to 'write reflective entries as you go through the course' would have a student preparing the wrong artefact for a component worth a fifth of their grade. (Likely conflated with the old Junior Certificate RE journal work.)
- **Suggested action:** Rename to 'Coursework (prescribed title)' throughout and rewrite the guidance around choosing a title, the research/summary-of-findings/skills/personal-insights structure the Part A + Part B grids reward, and starting it early.

### subject-home-economics-protocol
- **Where:** subjectContentPractical.ts lines 37, 43, 71, 73, 91, 113 (Section 1 paragraph 3, its highlight tooltip, and Sections 3-6)
- **Quote:** "The [[Food Practical Exam]] is the timed cooking test, typically held in April or early May in your school's home ec room. It is worth roughly **35% of your total mark**."
- **Concern:** Rubric item 6, factual overreach: there is no timed food practical exam in Leaving Cert Home Economics. LC Home Ec is assessed by written paper (320/400, 80%) + Food Studies Coursework Journal (80/400, 20%). The described timed cooking exam is a Junior Cycle component. The error is load-bearing: Sections 3-6 build the module's core strategy on it ('you walk into the June written paper with potentially 50% of your marks already banked', practising dishes 3-4 times, planning-sheet marks '15-20+'). Per amendment 1, the fiction also lives in the Highlight tooltip ('A timed cooking examination, usually 2.5-3 hours'). Any Home Ec teacher or accreditation reviewer would reject this outright, and it contradicts the file header's claim that all structures are 'based on the current SEC specifications'.
- **Suggested action:** Rewrite Sections 1 and 3-6 around the real LC assessment model (written paper 80%, journal 20%); move all timed-practical content to the future JC variant where it belongs, verified against the current JC specification.

### subject-home-economics-protocol
- **Where:** subjectContentPractical.ts lines 36, 41-42 (Section 1 paragraph 2 + Elective highlights)
- **Quote:** "You choose one of two electives: [[Elective 1 — Food Studies]] or [[Elective 2 — Social Studies]]. Most students take Elective 1."
- **Concern:** Rubric item 6: the elective structure is wrong. Food Studies is CORE in LC Home Economics, not an elective; the actual electives are Home Design & Management, Textiles Fashion & Design, and Social Studies, examined in Section C (not 'Section B... from your chosen elective' as stated). Both Highlight tooltips (amendment 1) repeat and elaborate the false framing ('The most popular elective, covering food science...'). A student following this could misunderstand their own paper's structure — the kind of error that embarrasses the app in front of teachers.
- **Suggested action:** Correct to the real core + three-elective structure and Section A/B/C paper layout, verified against a recent SEC paper before republishing.

### subject-construction-studies-protocol
- **Where:** subjectContentPractical.ts lines 159-161 (Section 1 paragraphs + 'written paper' highlight description, line 165)
- **Quote:** "roughly 50% for the written exam and 50% for the practical project ... a 3-hour exam worth 400 marks"
- **Concern:** Rubric item 6 (factual overreach a teacher/accreditation reviewer would challenge). The current SEC LC Construction Studies HL assessment is written paper 300 marks (50%), practical skills examination 150 marks (25%), and project 150 marks (25%). The module states the written paper is worth 400 marks, presents the project alone as ~50% of the grade, and omits the practical skills examination entirely — a whole assessment component worth a quarter of the grade is never mentioned anywhere in the six sections. A Construction Studies teacher would challenge this immediately, and it could misdirect students' effort allocation (e.g. Section 3's claim 'you walk into June with half your marks already determined' overstates the pre-June banked marks). The file header's claim that 'All mark allocations and exam structures are based on the current SEC specifications' compounds the embarrassment risk.
- **Suggested action:** Correct the component split to written 50% / practical skills exam 25% / project 25% (300/150/150 of 600), add coverage of the practical skills examination (it is a distinct timed workshop test), verify against the SEC specification, and re-check the derived strategic claims in Sections 1, 3, and 6 that build on the 50/50 framing.

### subject-art-protocol
- **Where:** /Users/alexlinehan/Nextstepuni-Launch-/subjectContentCreative.ts lines 27-31 (Section 1), and pervasively through all 6 sections and highlight tooltips
- **Quote:** "Together the practical exam accounts for roughly **62.5%** of your total mark — that is **250 out of 400 marks**."
- **Concern:** Rubric item 6, whole-module scale: the entire module describes the discontinued pre-2021 LC Art syllabus — 400 marks total, a 'Life Drawing' session from a live model, an 'Art History and Appreciation' paper (150 marks/37.5%), an unseen-image 'Appreciation question', and everything decided on exam day. The current specification (examined since 2021, and correctly documented in this app's own syllabusMeta.ts lines 534-547) is 500 marks: Practical Coursework/Artefact A 250 marks (50%), Invigilated Practical Exam/Artefact B 100 marks (20%), and the 'Visual Studies' written paper 150 marks (30%). Life Drawing was abolished. Worse than embarrassment, the advice is actively harmful: the module names the 5-hour exam piece as 'the single biggest mark zone' and never once mentions the coursework workbook/Artefact A — the actual largest component at 50% — so a student following this plan would neglect half their grade. Any Art teacher would challenge it on sight.
- **Suggested action:** Full content rewrite against the revised specification using the app's own syllabusMeta.ts art entry and data/examinersChair/art.ts as the source of truth (Artefact A coursework + workbook 50%, Artefact B invigilated 20%, Visual Studies Sections A/B/C 30%, Visual Studies Framework, primary-source workbook guidance). Do not ship the module to any cohort in its current form.

### subject-art-protocol
- **Where:** /Users/alexlinehan/Nextstepuni-Launch-/subjectContentCreative.ts (whole art entry) vs /Users/alexlinehan/Nextstepuni-Launch-/syllabusMeta.ts lines 534-547 and /Users/alexlinehan/Nextstepuni-Launch-/data/examinersChair/art.ts
- **Quote:** "It covers Irish art, European art from the Renaissance to the present, and appreciation of art and design."
- **Concern:** Cross-surface contradiction inside the same app: an Art student who opens both this module and the app's Examiner's Chair / syllabus tools will see two irreconcilable descriptions of their exam (Art History & Appreciation at 37.5% of 400 vs Visual Studies at 30% of 500 with named Sections A/B/C). This independently damages credibility with teachers and accreditation reviewers even before the factual question of which is right, and violates the project's own syllabus-alignment directive that subject content must match curriculum.ts/syllabusMeta.ts.
- **Suggested action:** Treat syllabusMeta.ts and examinersChair/art.ts as canonical when rewriting; add a consistency check so subject-strategy modules cite the same component names, mark totals, and percentages as the syllabus metadata.

### subject-music-protocol
- **Where:** /Users/alexlinehan/Nextstepuni-Launch-/subjectContentCreative.ts ~line 200 (Section 1 'How Music Actually Works', Composing paragraph) plus the Composing highlight (~line 215) and Sections 3, 4, 6 built on it
- **Quote:** "You submit a portfolio of compositions as coursework... as well as an original composition. The portfolio is prepared throughout the year and submitted before a set deadline."
- **Concern:** Rubric item 6 (factual overreach a teacher would challenge): in actual LC Music, Composing is a 1.5-hour written June exam of melody and harmony questions — not submitted coursework. An original-composition portfolio exists only for the rarely-chosen Composing elective. Sections 3 ('your composition portfolio is coursework — you can draft, revise, get feedback'), 4 ('leaving it too late... deadline'), and 6 ('Finalise and polish your composition portfolio') all extend strategy advice from this wrong premise, so a student could genuinely misprepare (waiting for a portfolio deadline instead of practising timed melody/harmony writing).
- **Suggested action:** Rewrite the Composing strand across Sections 1, 3, 4, and 6 (paragraphs and Highlight descriptions) to describe the timed written Composing paper (melody + harmony), with the elective portfolio mentioned only as the minority pathway.

### subject-music-protocol
- **Where:** /Users/alexlinehan/Nextstepuni-Launch-/subjectContentCreative.ts lines 198 and 206 (Section 1 Listening paragraph + 'Listening Paper' highlight; repeated in Section 3 ~line 257)
- **Quote:** "The [[Listening Paper]] ... is worth **200 marks — 50% of your total**. It runs for approximately **two and a half hours**"
- **Concern:** Rubric item 6: the marks, weighting, and duration are wrong, and the module's whole 'where your marks are' strategy inverts reality. LC Music core activities are 25% each plus a 25% HL elective; the Listening core paper is 100 marks (~1.5 hours). Because the large majority of HL students take the Performing elective, Performing is typically 50% and Listening 25% — the opposite of what the module tells students. The HL elective system, the single most important strategic fact in LC Music, is never mentioned.
- **Suggested action:** Correct the marks/percentages/durations for all three components using SEC figures, and add the elective system so the 'High-Value Zones' section reflects the typical Performing-elective weighting.

## MEDIUM — 67 confirmed

### agency-protocol
- **Where:** courseData.ts:44-52 (no jcStatus field) + App.tsx:389-395 + AppRouter.tsx:526
- **Quote:** "curriculum: 'senior' as const"
- **Concern:** Metadata/gating gap: this senior-only module has no jcStatus, which defaults to 'available' (hence 'live'), and the category-showcase path (AppRouter.tsx:526) filters ALL_COURSES by category only — never by curriculum — while the JC click-interceptor in App.tsx only fires on jcStatus === 'coming-soon'. Net effect: a 12-15yo Junior Cycle user browsing architecture-mindset sees and can open this LC module. Auto-essentials mode then shows them the shared unbranched inputs with senior-only framing — 'My Destination (LC Goal)' with placeholder 'e.g., 500 points for Engineering at UCD' (AgencyProtocolModule.tsx:526-527) and 'e.g., Computer Science at Trinity' (line 286) — exactly the mocks/CAO-points/college framing the app's own JC readability audit (ModuleShared.tsx:303-306) says juniors must not be shown.
- **Suggested action:** Add jcStatus: 'coming-soon' to the agency-protocol courseData entry (routes JC clicks to the placeholder), or apply the passesCurriculum filter to categoryCourses in AppRouter's category view so senior-only tiles never render for JC users.

### affirming-values-protocol
- **Where:** components/AffirmingValuesModule.tsx line 376-377 (essentials branch, section 0 — junior-visible by construction since JC users are forced into essentials)
- **Quote:** "in exams, your brain fights two battles. You fight the questions. You also fight a background voice saying "people like me don't get these results.""
- **Concern:** Hedge-stripping in simplification (amendment 3) combined with a clinical-sounding claim about the reader's own mind (rubric item 2). The full variant scopes the claim conditionally ('For students from disadvantaged backgrounds, there's an extra, invisible threat... the fear that a bad result will confirm...'); the junior/essentials variant asserts unconditionally, as fact, that every 12-15-year-old reader personally fights this deficit voice ('It hijacks your working memory. You lose brainpower to anxiety... This costs you real marks.'). For juniors who don't have this experience, stating it as universal risks suggesting the threat rather than naming it — and stereotype-threat salience effects are exactly the mechanism the module teaches.
- **Suggested action:** Restore the conditional in the essentials branch, e.g. 'many students also fight a second battle: a background voice saying...' — one word of scoping preserves the pedagogy without asserting the deficit onto every reader.

### grammar-of-grit-protocol
- **Where:** components/TheGrammarOfGritModule.tsx lines 32-49 and 102-116 (ThoughtReframer input + getReframedThought template)
- **Quote:** "Type a negative thought, then flip the 3 Ps to rewrite the script."
- **Concern:** Unbounded emotional free-text input (amendment 5). The instruction invites ANY negative thought (only the placeholder is study-themed), and the reframe template mechanically embeds arbitrary input: a genuine disclosure (bereavement, home situation, self-harm) would be echoed back as 'My approach to [disclosure] isn't working yet — but it's one specific area I can improve with the right strategy', an unsafe closing claim for arbitrary input. Renders identically to 12-year-olds in essentials mode, and the module has no support signposting anywhere.
- **Suggested action:** Scope the prompt to school/study ('Type a negative thought about school or study'), and add a light module-level signpost near the input ('if this is bigger than school, talk to someone you trust').

### procrastination-protocol
- **Where:** ProcrastinationModule.tsx lines 469–477 and 546–556 (CircuitBreaker, junior-visible in essentials mode)
- **Quote:** "Circuit broken. ... You rewrote a harmful thought into something that actually helps you move forward."
- **Concern:** Amendment 5 (unbounded emotional free-text) + item 2: quality detection is naive substring matching, so negations pass — 'can' matches "can't", 'okay' matches "not okay", 'forgive' matches "I can't forgive myself". A student can type a MORE self-critical thought (e.g. "I can't forgive myself, I will never be okay") and the widget lights all three success chips and asserts they wrote something 'that actually helps'. The closing claim is not safe for arbitrary input in a self-criticism-rewrite exercise.
- **Suggested action:** Add negation guards (or match on word boundaries with a small deny-list like "can't", "won't", "never", "not okay"), and soften the completion copy to non-evaluative phrasing (e.g. "Your rewrite includes all three ingredients") so it never certifies arbitrary text as helpful.

### reframing-catastrophic-thoughts-protocol
- **Where:** components/CatastrophicThinkingModule.tsx — DownwardArrowDrill, lines 336-348 (prompt label + placeholder) and 380-392 (unconditional 'Catastrophe Dissolved' reflection); junior-visible in essentials section 3
- **Quote:** "'Your worst fear' ... "Most catastrophic chains end somewhere manageable. The fear lives in the ambiguity — not the reality.""
- **Concern:** Unbounded emotional free-text input (rubric amendment 5): the card label asks for 'Your worst fear' — only the placeholder ('I'll fail my exam') hints at exam scope, and placeholders vanish on typing. The drill then forces up to 5 levels of 'And then what?' elaboration and, regardless of what was typed, always renders 'Catastrophe Dissolved' plus the flat claim that most chains 'end somewhere manageable'. A genuine disclosure (bereavement, home situation, self-harm ideation) would be met with mechanical generic reassurance and an implicit message that the fear is a thinking error. The full-mode prose hedges this ('you usually realise the worst case is actually survivable') but the widget's computed conclusion does not condition on input.
- **Suggested action:** Scope the label to the exam context ('Your worst exam fear' / 'The exam thought that scares you most') and soften/condition the closing copy, e.g. 'If your chain ended somewhere that still doesn't feel manageable, that's not a thinking error — it's a sign to talk to someone.' Pair with the module-level signpost from the high flag.

### emotional-intelligence-protocol
- **Where:** components/EmotionalIntelligenceModule.tsx — module-level (whole module; e.g. PFCShutdownSimulator L195/L302, section 1 L671-677, section 7)
- **Quote:** "See what happens when your Amygdala hijacks your brain under exam stress."
- **Concern:** This is the app's stress/panic module and it renders to Junior Cycle students (curriculum 'both', jcStatus live). It repeatedly evokes panic states — 'amygdala hijacks', 'survival mode', 'you go blank', a chart ending in 'Panic'/'Meltdown', and an interactive 'Trigger Stress Response' simulation — but contains no signpost anywhere to a trusted adult, guidance counsellor, or support if a student's stress is bigger than exam nerves. Per amendment 4, flag once at module level: an anxiety/stress-focused module aimed partly at 12-15yos should carry a single 'if this is bigger than exams, talk to someone' line.
- **Suggested action:** Add one module-level signpost (e.g. a closing callout in section 7 or under the module intro) pointing students to a trusted adult / guidance counsellor / a helpline if stress persists beyond exams. Low effort, closes a real safeguarding gap for the JC audience.

### praise-protocol
- **Where:** components/ThePraiseProtocolModule.tsx line 314 (ErrorSignalVisualizer 'What am I looking at?' explainer)
- **Quote:** "growth-minded students improve after mistakes while fixed-minded students keep making the same ones"
- **Concern:** Rubric item 6 + amendments 1 and 3: this interactive explainer (identical in essentials mode, so junior-visible) states deterministically what the cited §3 prose carefully hedges ('tend to produce a smaller signal', 'linked to learning more'). 'Keep making the same ones' is not a finding of Moser 2011 (a correlational ERP study showing post-error accuracy adjustments), and it self-labels any reader who identifies as fixed-mindset. The dossier's claim-by-claim record covers the §3 prose but not this explainer string — a reviewer comparing the two would spot the mismatch. Same register issue in the adjacent 'tiny Pe / huge Pe' dramatisation vs the paper's 'larger'.
- **Suggested action:** Reword to the hedged form used in §3 prose (e.g. 'students with a growth mindset tended to pay more attention to the error and improve on the next try'), and add the explainer text to compliance/evidence/praise-protocol.md so the dossier covers non-prose strings.

### effective-struggle-protocol
- **Where:** components/EffectiveStruggleAndGrowthModule.tsx line 684 (essentials branch, Step 6 'Recalibrate Your Dashboard')
- **Quote:** "If studying feels hard and frustrating, that means it is working. Your brain is rewiring. Do not stop. Easy study is wasted study."
- **Concern:** Amendment 3 (hedge-stripping in simplification): the full variant distinguishes productive ZPD struggle from Frustration Zone overload, and Step 3 in both variants explicitly teaches that frustration-zone difficulty means step back and get help. The essentials closer strips that distinction to an unconditional 'frustrating = working, do not stop', plus the absolute 'Easy study is wasted study' (the module's own data shows re-readers still recalled 40%). This is the designated junior-visible text once jcStatus ships (essentials is force-on for JC users), and it could keep a struggling or overloaded 12-15yo grinding against the module's own advice; senior opt-in essentials users see it today.
- **Suggested action:** Rewrite the essentials closer to carry the ZPD caveat, e.g. 'If it feels hard but you are making some progress, keep going — that is learning. If you are completely lost, step back and get a worked example or ask for help (see Step 3).' Drop or soften 'Easy study is wasted study'.

### controllable-variables-protocol
- **Where:** components/ControllableVariablesModule.tsx — getZone/getMilestone (lines 239, 243-245), finished summary (lines 452-453), essentials sleep prose (line 556); all inside CognitiveImpairmentClock, which renders IDENTICALLY in essentials mode
- **Quote:** "Studying after {impairedTime} is like studying drunk."
- **Concern:** Repeated adult-register alcohol/drink-driving comparisons ('Equivalent to mild alcohol impairment', 'as impaired as someone who has been drinking', 'over the drink-drive limit') are shown to 12-15yo Junior Cycle students because the Cognitive Impairment Clock and the essentials sleep prose render unchanged in essentials mode. The underlying Dawson & Reid (1997) finding is cited and valid, but rubric item 3 flags alcohol/driving as adult-register examples for the junior path; drink-driving especially assumes an adult frame of reference.
- **Suggested action:** For essentials/junior render, replace the alcohol and drink-drive milestone strings and the 'like studying drunk' summary with a teen-appropriate impairment analogy (e.g. reaction-time / 'trying to study with a bad head cold'); keep the alcohol comparison only in the non-essentials (LC) branch.

### reframing-progress-protocol
- **Where:** components/ReframingProgressModule.tsx lines 154 (essentials) and 159 (full), Section 2 'The 80/20 Protocol'
- **Quote:** "In Biology, for example, Ecology and Genetics are guaranteed long questions."
- **Concern:** Rubric item 6 factual overreach in both branches: the SEC guarantees no topic, and the claim will age badly under the redeveloped LC Biology specification (first examined 2027). The essentials branch compounds the certainty register ('Find the topics that always come up') and drops the full branch's explicit hedge ('This isn't about ignoring everything else') down to a weaker 'before tackling the rest' — a mild instance of hedge-stripping in simplification (amendment 3). Certainty language could drive risky selective study, and an accreditation reviewer or Biology teacher would challenge 'guaranteed'. The 80/20 prioritisation strategy itself is fine and not flagged.
- **Suggested action:** Soften to frequency language in both branches (e.g. 'have appeared as long questions in almost every recent paper — check the last five years yourself'), restore the 'not about ignoring everything else' caveat verbatim in the essentials branch, and note the claim for re-verification against the new Biology specification.

### linking-study-future-goals-protocol
- **Where:** LinkingStudyFutureGoalsModule.tsx lines 307 (essentials prose + HEAR Highlight tooltip) and 310 (full prose), section 'Hacking the System'
- **Quote:** "It can knock 30-50 points off the score you need -- that's huge."
- **Concern:** Rubric item 6 with item 5 crossover (and amendment 1 — the claim lives in a Highlight tooltip and essentials text as well as prose). The '30-50 points' range is not an official published figure: HEAR reduced-points offers vary by course, college, and year, are set by each HEI, and are quota-limited — qualifying for HEAR does not guarantee any reduction, and minimum entry requirements still apply. The essentials variant states it most flatly ('reduced CAO points... (30-50 points off)'), a mild hedge-stripping per amendment 3. A guidance counsellor or accreditation reviewer would challenge this, and for DEIS students it risks setting a concrete expectation (e.g. targeting 30-50 points below a course requirement) that may not materialise.
- **Suggested action:** Reframe to 'a reduced-points offer — the size varies by course and college, places are limited, and you still need the minimum entry requirements', in all three surfaces (full prose, essentials prose, Highlight tooltip); cite accesscollege.ie rather than a numeric range, and log the change per the compliance cut-log convention.

### mastering-spaced-repetition-protocol
- **Where:** components/MasteringSpacedRepetitionModule.tsx lines 730 and 733 (Highlight description, rendered in BOTH essentials and full branches) plus line 738 (MicroCommitment)
- **Quote:** "Free apps like Anki that automatically figure out when you're about to forget something... Download Anki on your phone or computer."
- **Concern:** Rubric 5 + 6 overlap (amendment 8 pattern, same as the 'Freedom is free' tooltip): Anki is free on desktop and Android, but the official iPhone app (AnkiMobile) is a paid app (~EUR 30). The module tells students — including junior/DEIS students likely on phones — that a product is free and instructs them to download it 'on your phone'. A DEIS student hitting a EUR 30 paywall after being told 'free' is exactly the assumed-money framing the rubric targets, and the claim lives in a tooltip an auditor reading prose only would miss.
- **Suggested action:** Reword tooltip and MicroCommitment: 'free on computer and Android; on iPhone the official app is paid — use ankiweb.net free in the browser instead', or point iPhone users to a genuinely free alternative.

### mastering-interleaving-protocol
- **Where:** components/MasteringInterleavingModule.tsx lines 53-104 (ProblemTypeSpotter), plus junior-visible Highlight descriptions at lines 178 and 209
- **Quote:** "Differentiate: y = sin(x²) ... like knowing whether you need the chain rule or the product rule"
- **Concern:** Junior-path age-fit (rubric item 3 via amendment 2): the module is curriculum 'both'/jcStatus live, and essentials mode only simplifies prose — the ProblemTypeSpotter renders identically for 12-14yo, but it is entirely LC Higher Maths calculus. The essentials-branch Highlight tooltips also reference 'chain rule or the product rule'. A 1st-3rd Year cannot attempt the module's only hands-on within-subject exercise (score 0/6 territory), which risks the item-5 belonging failure of making the tool feel like it's for older/higher students. Not harmful content, but a real accessibility gap on the live JC path.
- **Suggested action:** Gate a junior variant of ProblemTypeSpotter behind the essentials flag using JC-level discrimination pairs (e.g. area vs perimeter, mean vs mode, French verb tenses), and swap the two calculus-referencing Highlight descriptions in the essentials branches for JC-level examples.

### cognitive-endurance-protocol
- **Where:** components/CognitiveEnduranceModule.tsx line 554 (essentials branch, Sleep & Fuel) vs line 570 (full Fueling the Engine)
- **Quote:** "Try the Sports Drink Mouth Rinse in the last hour of a long exam."
- **Concern:** Hedge-stripping in simplification (amendment 3): the full LC variant carries the dossier-mandated CE-001 caveat ('it may give a similar lift... though the evidence for mental tasks is less settled'), but the essentials/junior variant presents the mouth rinse as a flat instruction to 12-15-year-olds with no epistemic qualifier — stating as directed practice what the full variant qualifies as unsettled evidence.
- **Suggested action:** Add a short hedge to the essentials sentence (e.g. 'Some athletes find the Sports Drink Mouth Rinse helps — you could try it...') so the junior path retains the CE-001 reframe.

### learning-math-protocol
- **Where:** components/LearningMathModule.tsx lines 22-45, PartialCreditCalculator (marks logic lines 26-29, result line 42)
- **Quote:** "else if(steps.formula && steps.sub) marks = 10; ... You get {marks}/10 marks."
- **Concern:** Dynamically generated numeric claim (amendment 7 + rubric item 6) that contradicts both SEC Scale D marking and the module's own prose. Section 4 correctly teaches that formula + one substituted value earns the low partial credit of 3/10, but the calculator awards 10/10 (full marks) for exactly those two actions with no correct answer, and 5/10 for the formula alone. Students playing with the widget get a materially inflated picture of partial credit; a teacher demoing it would spot the contradiction immediately.
- **Suggested action:** Rework the mapping to mirror Scale D (0,3,5,8,10): formula alone = 3 (low partial), formula + substitution = 5 (mid partial), full correct work = 10, slip = 8 (high partial), blunder capping progress appropriately — and make the copy state that full marks require the finished answer.

### learning-math-protocol
- **Where:** components/LearningMathModule.tsx line 359, PersonalStory (Orlaith)
- **Quote:** "I started using the bonus points as motivation -- even a H7 would be worth it."
- **Concern:** Factual error inside a testimonial used for level-choice motivation (rubric item 6). Bonus points apply only at H6 and above — a H7 earns no bonus and only 37 CAO points, less than a top Ordinary Level grade (O1 = 56). The story's premise ('even a H7 would be worth it' because of bonus points) is false and could encourage a struggling student to stay at Higher Level on incorrect grounds. The surrounding message (she got a H5 and it paid off) is fine; the H7 line is the problem.
- **Suggested action:** Change to 'even a H6 would be worth it' (which is true: 71 points) or reframe the motivation without the H7 claim.

### mastering-foreign-languages-protocol
- **Where:** components/LanguageMasteryModule.tsx line 239-241 (PersonalStory, section 3)
- **Quote:** "I ended up getting a H1 in the Leaving Cert. — Saoirse, 6th Year, Galway"
- **Concern:** Rubric amendment 9 (testimonial authenticity): a named student with school year and county, telling a specific H4-to-H1 outcome story, implies a real student. There is no provenance record and no clearly-illustrative framing; an accreditation reviewer would ask whether this is real-with-consent or invented, and an invented named testimonial presented as real is exactly the item-6 embarrassment risk.
- **Suggested action:** Either document consent/provenance for the testimonial, or reframe with clearly-illustrative language (e.g. a 'stories like Saoirse's' composite disclaimer) consistent with how PersonalStory is handled elsewhere in the app.

### mastering-foreign-languages-protocol
- **Where:** courseData.ts lines 376-385 + entire module (both essentials and full branches)
- **Quote:** "curriculum: 'both' as const, jcStatus: 'coming-soon' as const"
- **Concern:** Curriculum-placement mismatch (rubric amendment 2 lens): the module is tagged 'both' but 100% of its content — including the essentials/junior-facing branch — is Leaving Cert material (H1-H7 grades, the 25% Oral, Subjunctive, LC paper weightings, 'the single best opportunity in the entire Leaving Cert'). Essentials mode only compresses the LC prose; it is not a Junior Cycle adaptation, and there is no junior PersonalStory variant. If any surface renders this to a 12-14yo (search, recommendations, or a jcStatus regression), they get LC grade-pressure framing with zero JC relevance.
- **Suggested action:** Keep the JC path hard-gated on jcStatus until a genuine JC variant is authored, or change curriculum to 'senior' until then; verify no discovery surface (search, related-modules, counsellor dashboard) exposes it to junior accounts in the meantime.

### applied-sciences-protocol
- **Where:** components/AppliedSciencesModule.tsx lines 224-226 and 232-234 (PersonalStory, rendered in BOTH essentials and full branches)
- **Quote:** "I thought the project would speak for itself. I got a B2."
- **Concern:** Factual anachronism plus testimonial-authenticity problem (rubric item 6 + amendment 9). 'B2' is the pre-2017 LC grading scale, abolished when a current 6th year (2026) was about 8 years old — a real 'Oisin, 6th Year, Waterford' would say H2/H3. The story also implies the Engineering project was graded in 5th year and re-done for a better grade in 6th year, but the LC Engineering project is a single 6th-year submission with no standalone per-component letter grade. Any Engineering teacher or accreditation reviewer would spot this instantly, and the anachronism strongly signals the testimonial is invented while its name/year/county format implies a real student.
- **Suggested action:** Rewrite in current grading language and align with reality (e.g. frame as a 5th-year practice project vs the real 6th-year one, or drop the grade claim); establish provenance for all PersonalStory testimonials or add clearly-illustrative framing app-wide.

### applied-sciences-protocol
- **Where:** components/AppliedSciencesModule.tsx lines 208, 243, 247 (subtitle 'Your 2026 Project & Exam Guide'; 'The 2026 Special Topic'; 'This year's Special Topic') and sections 3-4
- **Quote:** "This year's Special Topic is <strong>Semiconductor Technology</strong>."
- **Concern:** Time-decay / accuracy risk (item 6). Every year-specific claim was verified correct for the 2026 sitting (Engineering prescribed topic, DCG HL refillable soap dispensers / OL fidget toys, LCCS 'Forests, Climate Change, and Biodiversity' at 30%), but as of July 2026 those exams have been sat: incoming 6th years get new briefs in September 2026, and a new Engineering specification begins for 5th years in September 2026. 'This year's' phrasing will shortly be actively wrong for the students reading it — a teacher would challenge it as last year's brief.
- **Suggested action:** Add an annual-refresh process for this module (and date the briefs explicitly, e.g. 'for the June 2026 exam') so the hardcoded themes cannot silently go stale; update for 2027 briefs when SEC releases them.

### mastering-english-protocol
- **Where:** components/MasteringEnglishModule.tsx lines 239 (section eyebrow '04 // Macbeth 2026'), 312 and 317 (section 3, both branches)
- **Quote:** "For 2026, the Shakespeare play is Macbeth."
- **Concern:** Same staleness problem: the single-text prescription is hard-coded to the now-past 2026 exam. Lower severity than the modes flag because the single text is set per school from the prescribed list and students will hear it from their teacher, but the module still presents outdated year-specific fact as current (rubric item 6 / embarrassment risk for accreditation review).
- **Suggested action:** Tie the year and text to the same per-cohort config as the comparative modes, or reframe the section as 'your prescribed Shakespeare play' with Macbeth as the worked example.

### mastering-english-protocol
- **Where:** components/MasteringEnglishModule.tsx lines 270-272 (section 0, full branch only)
- **Quote:** "PersonalStory name="Aisling" role="6th Year, Kilkenny" ... I got a H4 in my mock. ... I got a H2."
- **Concern:** Testimonial with a first name, school year, and county implying a real identifiable student, attached to a quantified grade-jump claim (H4 to H2) attributed to a single technique. Provenance is unverifiable from the code; an accreditation reviewer would ask whether this is a real student with consent or invented (amendment 9 — PersonalStory authenticity check).
- **Suggested action:** Either verify and document consent/provenance in the compliance dossier, or add clearly-illustrative framing (e.g. a 'stories are illustrative composites' disclosure at the PersonalStory component level) and soften the specific grade claim.

### mastering-business-protocol
- **Where:** components/MasteringBusinessModule.tsx lines 344-345, 354-355, 364-365, 376-377 (all essentials branches) + courseData.ts lines 423-424
- **Quote:** "Know how the exam works. For 2026, the compulsory ABQ covers Units 3, 4, and 5"
- **Concern:** Curriculum metadata says 'both', but the essentials-mode branches are condensed LC HL content (2026 ABQ, H1, SEEE, 80-mark ABQ), not a junior variant — and the interactive ABQAnswerScaffold/ABQLinkDrill render identically in essentials mode. There is also no junior PersonalStory variant. If the essentials branch is ever treated as the JC rendering path (or jcStatus is flipped without new content), 12-15yo Junior Cycle Business Studies students would be shown a Leaving Cert exam guide that does not match their course (JC has CBAs and a Common Level paper, no ABQ).
- **Suggested action:** Keep jcStatus 'coming-soon' gating firmly in place; when building the JC variant, author genuinely Junior Cycle content (CBA + Common Level structure) rather than reusing the essentials branch, and add a junior PersonalStory variant. Alternatively re-tag curriculum 'senior' until the JC version exists.

### mastering-the-creatives-protocol
- **Where:** components/MasteringTheCreativesModule.tsx lines 220, 235, 451, 455, 526, 528 (section 0 both branches, DeliberatePracticeWheel copy, section 5 both branches)
- **Quote:** "Talent is a myth. Spin the wheel and practice a real technique for 2 minutes."
- **Concern:** Rubric item 6 (factual overreach): the flat assertion that talent is 'a myth' / 'nonsense' is stated as fact repeatedly, including in junior-visible essentials prose ('skills, not talents') and in the wheel widget which renders identically in essentials mode (amendments 1 & 2). Deliberate-practice research is contested (Macnamara et al. meta-analyses found practice explains a minority of performance variance), and the module has NO Cite system, no data/references/ file, and no compliance/evidence/ dossier — an accreditation reviewer working to the CLAUDE.md evidence rule would challenge this as uncited pop-psychology overreach.
- **Suggested action:** Soften to defensible framing ('you don't need to be naturally gifted — the marking scheme rewards process') or add verified references via the Cite/References system plus an evidence dossier, per the pilot module pattern.

### mastering-the-creatives-protocol
- **Where:** components/MasteringTheCreativesModule.tsx lines 457-459 (PersonalStory, non-essentials branch of section 0)
- **Quote:** "PersonalStory name="Clodagh" role="6th Year, Ballyfermot" ... I got a H2 and I still can't draw a straight line."
- **Concern:** Amendment 9 (testimonial authenticity): a first name + school year + specific Dublin locality with a claimed H2 grade implies a real, identifiable student. No provenance or 'illustrative example' framing exists in the component or its data. An accreditation reviewer would ask whether this is real-with-consent or invented. Note also there is no junior PersonalStory variant, but that is acceptable since the story sits only in the non-essentials branch (LC-only per amendment 2).
- **Suggested action:** Verify provenance/consent, or add clearly-illustrative framing (e.g. a shared 'stories are composites' disclosure in ModuleShared's PersonalStory).

### leaving-cert-strategy-protocol
- **Where:** components/LeavingCertStrategyModule.tsx lines 451-453 (PersonalStory, section 3)
- **Quote:** "I ended up getting a H3 -- way higher than I expected. (Ciara, Leaving Cert 2024, Dublin)"
- **Concern:** Amendment 9 (testimonial authenticity): a named student with a specific sitting year, county, and a concrete grade outcome (H3) implies a real, consenting person. No provenance or clearly-illustrative framing exists anywhere in the module. An accreditation reviewer would ask whether this is real-with-consent; if invented, a fabricated grade outcome is presented as evidence the strategy works.
- **Suggested action:** Verify the testimonial's provenance and consent, or reframe with explicit illustrative framing (e.g. 'a composite student story') and drop the specific grade claim.

### reverse-engineering-protocol
- **Where:** ReverseEngineeringModule.tsx lines 310-314 (PersonalStory, section 3)
- **Quote:** "name="Caoimhe" role="Senior cycle, Limerick" junior={{ name: 'Caoimhe', role: '3rd Year, Limerick' ... }}"
- **Concern:** PersonalStory authenticity (amended rubric item 9): the identical testimonial is attributed to 'Caoimhe, Senior cycle, Limerick' in the full path and 'Caoimhe, 3rd Year, Limerick' in the junior path (with only 'January'/'mid-February' edited out). The same named, county-located student cannot be in two year groups — this reveals the quote as invented while presenting it as a real student's account, with no illustrative framing. An accreditation reviewer would ask for provenance.
- **Suggested action:** Either verify a real consented source, or add clearly-illustrative framing (e.g. 'a student like Caoimhe' / composite-story disclosure) app-wide for PersonalStory; at minimum stop re-attributing one quote to two different year groups.

### reverse-engineering-protocol
- **Where:** ReverseEngineeringModule.tsx lines 304 and 309 (80/20 Highlight description + prose, both essentials and full branches)
- **Quote:** "Look at past papers and you will notice that roughly 20% of topics come up for about 80% of the marks. Focus your energy there first."
- **Concern:** Rubric item 6 (factual overreach): a specific quantitative claim about SEC paper composition presented as an observable fact ('you will notice'), with no citation — the module's own dossier (compliance/evidence/reverse-engineering.md) classifies it as an uncited heuristic, but the student-facing text states it as fact. A teacher would challenge the numbers, and it nudges topic-spotting/question-prediction, which SEC Chief Examiner reports repeatedly warn against. The junior essentials branch states it just as flatly ('About 20% of topics earn 80% of the marks. Hit those first.') to 12-15yo readers.
- **Suggested action:** Reframe to qualitative, hedged language ('some topics come up far more often — weight them first, but still cover the syllabus') and add an explicit anti-question-spotting caveat; keep numbers out unless a source supports them.

### exam-hall-strategies-protocol
- **Where:** components/ExamHallStrategiesModule.tsx line 615 (DumpSheetBuilder results callout)
- **Quote:** "your dump sheet prevents interference — facts written down can't be displaced by exam stress"
- **Concern:** Rubric item 6 + amendments 1 and 3: an absolute, uncited cognitive-mechanism claim ('prevents', 'can't be displaced') stated as fact inside interactive non-prose text. The surrounding prose is properly hedged and cited (stress 'can block access', Cite 1; worry-writing 'tend to score higher', Cite 2), but this widget string strips the hedges — and it violates the repo's own accreditation governance rule that uncited claims must be reframed non-prescriptively. Renders identically in essentials/junior mode.
- **Suggested action:** Soften to hedged phrasing, e.g. 'facts already on the page are safe even if stress makes recall harder', or attach a verifiable citation; log any reframe per the dossier/cut-log process.

### exam-crisis-management-protocol
- **Where:** ExamCrisisManagementModule.tsx line 998 (essentials, junior-visible), lines 1002, 1053, 1057
- **Quote:** "Cut caffeine the week before so a normal cup on exam morning actually works."
- **Concern:** Rubric items 1 + 3 (substance mention, junior path). The ESSENTIALS branch — the simplified junior-visible text — coaches a caffeine-dosing strategy ('caffeine tapering' so exam-morning caffeine 'hits properly'), normalising coffee/energy-drink use for 12-15yo; Irish health guidance discourages caffeine for under-16s. The full-variant tooltip repeats it, and the 7-day countdown ('Cut back on caffeine, 7 days out') appears in both branches. The claim also carries no Cite, unlike the surrounding sleep/food content.
- **Suggested action:** Gate the caffeine-tapering strategy to the non-essentials (senior) branch; junior variant should say only 'skip energy drinks/caffeine'. Add a citation or soften if retained for seniors.

### exam-crisis-management-protocol
- **Where:** ExamCrisisManagementModule.tsx lines 947-951 (PersonalStory)
- **Quote:** "name="Roisin" role="6th Year, Limerick" junior={{ name: 'Roisin', role: '3rd Year, Limerick' ... }}"
- **Concern:** Amendment 9 (testimonial authenticity). The named, county-placed testimonial implies a real student, but the same 'Roisin' switches between 6th Year (mocks/real exam) and 3rd Year (class test/Junior Cert) depending on viewing mode — in-app proof the story is synthetic and rewritten per audience. An accreditation reviewer would challenge unlabelled invented testimonials presented as real students.
- **Suggested action:** Verify provenance with consent, or add clearly-illustrative framing (e.g. 'a story like many we hear' / composite disclaimer) via the PersonalStory component.

### game-day-protocol
- **Where:** components/GameDayModule.tsx line 118 (FOODS array, PreExamMealBuilder — renders identically in essentials/junior mode)
- **Quote:** "{ id: 13, name: 'Black coffee (moderate)', category: 'Caffeine', score: 1 }"
- **Concern:** The meal builder awards a positive score (+1) for black coffee, actively rewarding a caffeine choice, and the interactive is fully visible on the junior path (essentials mode only simplifies prose, per amendment 2). Positively scoring a caffeinated drink for 12-15-year-olds sits under item 1's substance language and item 3's junior lens; the module correctly penalises energy drinks (-3) but then endorses caffeine one row later, and no age caveat exists anywhere.
- **Suggested action:** Score coffee 0/neutral or hide the item in essentials mode; if kept for seniors, add a note that caffeine isn't recommended for younger students.

### game-day-protocol
- **Where:** components/GameDayModule.tsx lines 504-508 (PersonalStory, section 1)
- **Quote:** "PersonalStory name="Aisling" role="6th Year, Limerick" junior={{ name: 'Aisling', role: '3rd Year, Limerick', ... }}"
- **Concern:** Amendment 9 (testimonial authenticity): the name + school year + county format implies a real student, yet the same 'Aisling, Limerick' is presented as a 6th Year to seniors and a 3rd Year to juniors with a re-worded story ('mocks'→'big test', '2am'→'midnight') — internally inconsistent if real, so it is evidently invented while formatted as genuine. An accreditation reviewer would challenge unlabelled invented testimonials, and no provenance or 'illustrative' framing exists.
- **Suggested action:** Either verify a real consented source or add clearly-illustrative framing (e.g. 'a story like many we hear') across all PersonalStory usages; fix the year inconsistency.

### mastering-the-humanities-protocol
- **Where:** components/MasteringTheHumanitiesModule.tsx lines 265-267 (PersonalStory, full-variant only)
- **Quote:** "Sinéad" role="6th Year, Wexford" ... I jumped to a H1 in the mocks without learning a single new fact."
- **Concern:** Testimonial carries a real-sounding name, school year and county, implying a real student, and promises a two-grade jump (H3 to H1) from technique alone. Provenance is unverifiable from the code and there is no illustrative-example framing; an accreditation reviewer would ask whether this is a real student with consent or invented (amendment 9).
- **Suggested action:** Verify the testimonial's provenance and consent, or add clearly-illustrative framing (e.g. 'based on real student experiences') and soften the guaranteed-jump implication.

### digital-distraction-protocol
- **Where:** components/DigitalDistractionModule.tsx lines 26-28 and 93-98 (AttentionDeficitCalculator state-dependent callouts)
- **Quote:** "Two checks and you've lost 46 minutes. Only 14 minutes of real studying. … At 3 checks, you're losing over an hour of focus time."
- **Concern:** Rubric item 6 via amendment 7 (dynamically generated numeric claims). The widget linearly applies the contested Gloria Mark ~23-minute office-interruption recovery figure per phone check and asserts the computed results as fact ('you've lost 46 minutes', 'virtually none of your study time is productive'), including the internally impossible 'over an hour of focus time' inside a 60-minute hour (code caps timeLost at 60 but the string doesn't). The 'simplified illustration' hedge in the intro (line 41) is contradicted by the declarative callouts below it. The full-variant Highlight (line 392) also states 'Research shows it takes about 23 minutes' flatly, while the essentials prose (line 386) correctly hedges 'can take around'. This calculator renders identically in essentials mode, so 12-15yo see these claims too. A teacher or accreditation reviewer would challenge the per-check linear extrapolation as overreach of the cited source.
- **Suggested action:** Rewrite the callout strings in conditional register ('could cost you up to...', 'on this model...'); remove or fix the 'over an hour' impossibility at 3 checks; align the Highlight tooltip's '23 minutes' phrasing with the hedged 'can take around' used in the essentials prose.

### digital-distraction-protocol
- **Where:** components/DigitalDistractionModule.tsx line 428 (Highlight description tooltip, non-essentials branch of section 3)
- **Quote:** "Free apps like Cold Turkey or Freedom that block distracting websites and apps"
- **Concern:** Rubric items 5+6 via amendments 1 and 8 (factual claim in a tooltip, DEIS crossover). Freedom is a paid subscription product, and Cold Turkey's lockable tiers are paid; calling both 'free' is factually wrong and specifically harmful to DEIS students who may act on the claim and hit a paywall. The same apps are also recommended without the 'free' claim in the essentials branch (line 423) and the Phase 1 roadmap item (line 114), so only the tooltip needs fixing.
- **Suggested action:** Correct the tooltip to distinguish genuinely free options (e.g. Cold Turkey's free tier, built-in Screen Time / Digital Wellbeing / Focus Mode) from paid products, or drop the word 'Free'.

### digital-distraction-protocol
- **Where:** components/DigitalDistractionModule.tsx lines 393-397 (PersonalStory)
- **Quote:** "name="Ciara" role="5th Year, Cork" junior={{ name: 'Ciara', role: '2nd Year, Cork', ... }}"
- **Concern:** Amendment 9 (PersonalStory authenticity). The testimonial carries a real-student presentation (name, school year, county) with no illustrative framing, and the junior variant re-badges the same person and near-identical quote as '2nd Year, Cork' instead of '5th Year, Cork' — internal evidence the persona is invented while being presented as a real student. An accreditation reviewer would ask for provenance/consent, and the year-swapping makes the fabrication demonstrable from the source.
- **Suggested action:** Either verify a real consented source, or add clearly-illustrative framing (e.g. a 'composite student story' label in the PersonalStory component) app-wide.

### learning-radar-protocol
- **Where:** components/TheLearningRadarModule.tsx line 904 (Section 6 'The Prediction Game', Highlight tooltip), rendered identically to junior/essentials users if they open the full-variant tooltip path — full branch only, but the concern is accreditation not age
- **Quote:** "By the end, their predictions were about 50% more accurate."
- **Concern:** The module's own compliance dossier (compliance/evidence/learning-radar.md, cut-log LR-003) records this exact '50% more accurate over a year' figure as CUT/reframed to qualitative language because it is unverifiable against Cite 4 (Dunlosky et al. 2013, a techniques review, not a year-long prediction-tracking study). The body prose was duly reframed ('noticeably more accurate') but the Highlight tooltip still states the removed figure plus an invented-sounding study design ('tracked students... throughout a whole school year'). This is the amendment-1/amendment-7 failure mode (numeric claim living in a tooltip) inverted through amendment 3: the prose hedges while the tooltip asserts. An accreditation reviewer cross-checking the dossier would catch the contradiction directly.
- **Suggested action:** Edit the line-904 Highlight description to the qualitative LR-003 wording (e.g. 'students who predicted their scores before each test got noticeably better at predicting over time') and remove the 'whole school year' / '50%' study framing; confirm the dossier claim table then matches the shipped text.

### learning-radar-protocol
- **Where:** components/TheLearningRadarModule.tsx lines 888-892 (PersonalStory, Section 5 — junior variant included)
- **Quote:** "name="Ciara" role="5th Year, Cork" junior={{ name: 'Ciara', role: '2nd Year, Cork'"
- **Concern:** Amendment 9 (testimonial authenticity): the testimonial carries a real-sounding name, school year and county, implying a real student — yet the code presents the SAME person as both a 5th Year (Biology) and a 2nd Year (Science) depending on essentials mode, which demonstrates in-code that it is invented. There is no 'illustrative example' framing anywhere. An accreditation or press reviewer reading the source would reasonably challenge fabricated attributed quotes from named minors' peers.
- **Suggested action:** Either verify provenance (real student, consent on file) or add clearly-illustrative framing app-wide in the PersonalStory component (e.g. 'Stories are composites based on real student experiences') — a one-line fix in ModuleShared covers every module.

### note-taking-paradox-protocol
- **Where:** components/TheNoteTakingParadoxModule.tsx line 371 (PersonalStory, section 0 full-prose branch)
- **Quote:** "name="Maeve" role="6th Year, Sligo" junior={{ name: 'Maeve', role: '3rd Year, Sligo', ... }} ... My History grade went up a full grade in the mocks."
- **Concern:** Testimonial authenticity (amendment 9): a named student with year and county plus a concrete grade-improvement outcome implies a real person, but the identical story is re-attributed to '3rd Year' for junior users — demonstrating it is invented/adjustable copy with no provenance or clearly-illustrative framing. An accreditation reviewer would ask whether Maeve is real-with-consent. Secondary consistency issue: the junior variant is unreachable dead code, because junior users always get essentials mode (useEssentialsMode returns true for curriculumLevel 'junior') and the PersonalStory sits only in the non-essentials branch.
- **Suggested action:** Either source real consented testimonials or add clearly-illustrative framing (e.g. a shared 'stories are composites' convention/label in PersonalStory). Separately, decide whether PersonalStory should appear in the essentials branch; if not, delete the dead junior variant.

### cognitive-load-protocol
- **Where:** components/TheCognitiveLoadModule.tsx lines 422-426 (PersonalStory, section 1)
- **Quote:** "name="Niamh" role="6th Year, Galway" junior={{ name: 'Niamh', role: '3rd Year, Galway', ..."
- **Concern:** PersonalStory authenticity (amendment 9 / item 6): the testimonial is presented as a named real student with year and county, but the identical person appears as both '6th Year, Galway' (Biology, mock) and '3rd Year, Galway' (Science, test) depending on audience — internally confirming it is an invented/templated story formatted as a genuine testimonial. An accreditation reviewer would ask for provenance.
- **Suggested action:** Either verify a real consented source or add clearly-illustrative framing (e.g. a shared 'stories are composites/illustrative' disclosure at the PersonalStory component level, which would fix this app-wide).

### implementation-protocol
- **Where:** components/TheImplementationProtocolModule.tsx lines 388 (essentials branch, junior-visible) and 393 (Highlight description tooltip)
- **Quote:** "The other 72%? That comes down to strategy, not willpower."
- **Concern:** Rubric item 6 overreach: Sheeran (2002) shows intentions explain ~28% of behaviour variance; the module asserts as flat fact that the remaining unexplained 72% 'comes down to strategy'. Unexplained variance also includes measurement error, circumstance, ability, etc. The dossier verifies the 28% figure but this 72%-is-strategy inference is an uncited gloss a statistics teacher or the accreditation reviewer would challenge — and it appears without hedging in both the junior-visible essentials paragraph and a Highlight tooltip (amendment 1 surface).
- **Suggested action:** Reframe to a supportable claim (e.g. 'much of the rest comes down to things you can control — like having a specific plan') in both the essentials paragraph and the Highlight description; record the reframe in the dossier and cutContent log.

### context-effect-protocol
- **Where:** TheContextEffectModule.tsx lines 35-41 and 66-75 (ContextMemoryComparison, shown in essentials/junior mode too)
- **Quote:** "const diffRetrieval = [0.35, 0.42, 0.40, 0.38, 0.35, 0.30]; ... { label: 'Inaccessible', x1: 0.66, x2: 1, color: '#ef4444' }"
- **Concern:** Invented retrieval curves presented as a data chart with no 'simplified illustration' disclaimer. The 'Different Context' line crashes toward the floor with phase labels 'Cues missing' and 'Inaccessible', dramatising the context effect as near-total memory loss — which contradicts the module's own section 4 ('the effect is modest', Smith & Vela 2001 meta-analysis) and overstates Godden & Baddeley's extreme underwater manipulation. An accreditation reviewer would ask what data this plots (rubric item 6 via amendments 1 and 7).
- **Suggested action:** Add an 'illustrative — not measured data' caption, soften the diff-context curve so it shows a modest gap rather than collapse, and relabel 'Inaccessible' (e.g. 'Harder to reach').

### context-effect-protocol
- **Where:** TheContextEffectModule.tsx lines 779-783 (PersonalStory, section 1)
- **Quote:** "name="Aoife" role="5th Year, Cork" junior={{ name: 'Aoife', role: '2nd Year, Cork', ..."
- **Concern:** Testimonial carries a name, school year, and county implying a real student, and the identical story is re-badged from '5th Year, Cork' to '2nd Year, Cork' for the junior path — confirming it is invented while still presenting as authentic. No provenance or clearly-illustrative framing (amendment 9); an accreditation reviewer would challenge this.
- **Suggested action:** Either verify real-student-with-consent provenance or add clearly-illustrative framing (e.g. a 'composite/illustrative example' label) at the PersonalStory component level.

### points-optimization-protocol
- **Where:** components/PointsOptimizationModule.tsx lines 29-52 (SUBJECTS_DATA), line 222 vs line 270 (H1RateDashboard)
- **Quote:** "Real H1 percentages from recent Leaving Cert results"
- **Concern:** Item 6 + amendment 1 (claims in component chrome, not prose). The dashboard header asserts these are 'Real H1 percentages' while its own small-print footnote contradicts it: 'Illustrative relative estimates... not official published figures.' The hardcoded h1Rate values are presented with data-like precision and drive High Yield/Low Yield labels and study-time advice. A teacher or accreditation reviewer checking against SEC statistics would challenge the header claim, and the internal contradiction itself embarrasses.
- **Suggested action:** Change the header to 'Indicative H1 rates' matching the footnote, or replace the array with actual published SEC figures for a named year and cite it via the Cite/references system (rights are cleared for SEC material).

### points-optimization-protocol
- **Where:** components/PointsOptimizationModule.tsx lines 29-52 (objectivity values), ObjectivitySpectrum lines 277-328, PortfolioOptimizer 'Objectivity' stat line 602-603
- **Quote:** "Where does each subject fall between "right/wrong" and "examiner's discretion"?"
- **Concern:** Item 6 pseudo-quantification. The 'objectivity' scores (English 25%, Art 20%, History 35%...) are invented numbers with no source and no Cite marker, yet they are displayed as percentage data, averaged into a personal 'Objectivity' score, and used to flag students' subjects as risks ('your grade could depend on which examiner reads your paper' — a claim the SEC, which uses marking conferences and appeals precisely to standardise, would dispute as stated). The qualitative point is defensible; the precise percentages are not.
- **Suggested action:** Reframe as an unnumbered qualitative spectrum (objective ⟷ discretion bands), drop the invented percentages and the averaged Objectivity stat, and soften 'depends on which examiner' to 'has more marker judgement involved'.

### points-optimization-protocol
- **Where:** components/PointsOptimizationModule.tsx lines 700-702 (Maths Multiplier, full variant) and line 697 (essentials)
- **Quote:** "every hour you put into HL Maths is worth more points than the same hour in any other subject"
- **Concern:** Item 6 overreach with real guidance stakes. The section presents only the upside of staying in HL Maths ('Even if Maths is your weakest subject, the bonus points give you a cushion that makes the extra effort worth it') and never mentions the downside the bonus structure creates: H7 gets no bonus (37 pts) and H8 gets 0 points, versus 56 for an O1 — for a genuinely weak-at-maths student, dropping to Ordinary is often the points-maximising and safer call. A guidance counsellor would challenge this as one-sided advice that could keep struggling students in HL.
- **Suggested action:** Add one balancing sentence + visualizer state: below H6 the bonus vanishes (H7 = 37, H8 = 0, vs O1 = 56), so the HL-vs-OL call depends on realistically clearing H6 — talk to your maths teacher.

### points-optimization-protocol
- **Where:** components/PointsOptimizationModule.tsx lines 790-792 and 799-801 (PersonalStory)
- **Quote:** "Ciara" role="6th Year, Galway"
- **Concern:** Amendment 9 (testimonial authenticity). The Ciara testimonial carries a name, school year, county, and a quantified outcome ('my mock results jumped by nearly 40 points'), presented identically to the verifiably real founder story beside it — implying a real student without any provenance or illustrative framing. An accreditation reviewer would ask whether this is real-with-consent or invented. Secondary concern inside the same quote: it models diverting effort away from English ('hours on English essays that might get me 2 extra points'), a compulsory matriculation subject.
- **Suggested action:** Verify provenance/consent, or clearly frame as illustrative (e.g. 'a story like many we hear' / composite label), and soften the English line so it reads as rebalancing rather than abandoning a compulsory subject.

### marking-scheme-decoder-protocol
- **Where:** components/MarkingSchemeDecoderModule.tsx line 223-227 (SchemeDecoder extract 4 annotation — non-prose surface per amendment 1)
- **Quote:** "PCLM ... Partial Credit Level Marks = you get marks for each correct element."
- **Concern:** Rubric item 6 factual error: in SEC usage PCLM is the English assessment criteria (Purpose, Coherence, Language, Mechanics), not 'Partial Credit Level Marks', and it is not notation used on a Biology-style 'Define osmosis' question. The app's own Mastering English entry (courseData.ts:604) uses PCLM in the correct English sense, so this module contradicts the app itself. A teacher or accreditation reviewer would catch this immediately.
- **Suggested action:** Replace the invented expansion: either move the PCLM annotation to an English-context extract with the correct Purpose/Coherence/Language/Mechanics meaning, or swap the term for genuine partial-credit notation actually used in science/maths schemes (e.g. 'low/high partial credit').

### marking-scheme-decoder-protocol
- **Where:** components/MarkingSchemeDecoderModule.tsx lines 515-517 and 586-588 (PersonalStory blocks)
- **Quote:** "Darragh, Leaving Cert 2023, Limerick ... I'd picked up 11 marks across those two questions ... My final grade was a H3 instead of a H4. That was worth 10 CAO points."
- **Concern:** Amendment 9 authenticity check: both testimonials carry a first name, exam year, and county plus precise verifiable-sounding outcomes ('went up a full grade in two subjects', '11 marks', 'H3 instead of H4'), implying real students. No provenance or 'illustrative example' framing exists in the component. An accreditation reviewer would ask whether these are real accounts with consent or invented.
- **Suggested action:** Verify provenance/consent for both stories, or add clearly-illustrative framing (e.g. a shared PersonalStory disclosure that stories are composites) at the component or module level.

### answer-engineering-protocol
- **Where:** components/AnswerEngineeringModule.tsx line 799, §5 The 60% Answer
- **Quote:** "a structured 60% answer scores higher than an unstructured 80% answer"
- **Concern:** Rubric item 6 overreach. Stated as fact ('The key insight') with Cite n=1 (generic SEC marking schemes), but the evidence dossier (compliance/evidence/answer-engineering.md §5) only verifies the weaker claim that structure lets the examiner find and award every point — not that structure beats a 20-point knowledge gap. An SEC-literate teacher or accreditation reviewer would challenge the quantified comparison; it is exactly the class of false-precision claim this module already cut in AE-001/AE-002 ('400+ scripts', '4-5 of 25 marks').
- **Suggested action:** Reframe to the supported qualitative claim (e.g. 'a well-structured partial answer collects every mark it earns — and can outscore a stronger but buried answer') and log the reframe in data/cutContent.ts per the module accreditation rule.

### answer-engineering-protocol
- **Where:** components/AnswerEngineeringModule.tsx lines 800-802, PersonalStory in §5
- **Quote:** "I got 18 out of 25. My friend who knew more but wrote it as a paragraph got 14."
- **Concern:** Amendment 9 (testimonial authenticity) plus rubric item 4 crossover. 'Niamh, Leaving Cert 2023, Waterford' and 'Sean, Leaving Cert 2024, Cork' carry name/year/county implying real students, with no provenance or illustrative framing; the Niamh story additionally claims exact knowledge of a named friend's lower mark, hard-coding the unverified 60%>80% claim as anecdote and modelling peer mark-comparison. An accreditation reviewer would ask whether these are real-with-consent or invented.
- **Suggested action:** Verify provenance/consent or add clearly-illustrative framing app-wide for PersonalStory; drop or soften the friend's-mark comparison ('my more structured answer scored better than I expected').

### subject-english-protocol
- **Where:** subjectContentLanguages.ts lines 45 and 51 (Section 2 prose + 'PCLM' Highlight description)
- **Quote:** "Each criterion carries roughly equal weight"
- **Concern:** Rubric item 6, and again duplicated into a Highlight tooltip ('Each element is weighted roughly equally'). The published PCLM weighting is Purpose 30%, Coherence 30%, Language 30%, Mechanics 10% — Mechanics is explicitly NOT equal. This misdirects effort (the same section warns 'Consistent errors in mechanics will pull your grade down even if your ideas are strong', overstating a 10% criterion) and is exactly the kind of claim an examiner-report-literate teacher or accreditation reviewer would catch.
- **Suggested action:** State the real 30/30/30/10 split in both the paragraph and the Highlight; it is strategically useful information in its own right.

### subject-irish-protocol
- **Where:** subjectContentLanguages.ts line 171, Section 3 'Where Your Marks Are'
- **Quote:** "The essay is typically worth 50 marks or more"
- **Concern:** Rubric item 6. The HL Ceapadóireacht essay is worth 100 marks — this understates it by half and contradicts the module's own (already wrong) 'Paper 1 worth 120 marks' claim, muddling exactly the prioritisation the section exists to teach.
- **Suggested action:** State the real figure: 100 marks at Higher Level (and the OL equivalent once verified).

### subject-irish-protocol
- **Where:** subjectContentLanguages.ts line 138, Section 1
- **Quote:** "It runs for **2 hours 50 minutes**. ... It runs for **3 hours 20 minutes**."
- **Concern:** Rubric item 6. These are the LC English Paper 1/Paper 2 durations (identical to the English entry at lines 28-29), apparently copy-carried into the Irish entry. Irish HL Paper 2 is 3 hours 5 minutes, and Paper 1's timing includes the Cluastuiscint session. Wrong durations in an exam-technique module undermine the timing advice the app gives elsewhere.
- **Suggested action:** Verify both paper durations against the SEC timetable and correct; audit the other language entries in this file for the same copy-forward pattern.

### subject-french-protocol
- **Where:** subjectContentLanguages.ts lines 245, 248, 251-255 (Section 1 'How French Actually Works' + Highlight tooltips)
- **Quote:** "the [[Aural Exam (Listening)]] worth **100 marks** (25%), and the [[Written Exam]] worth **200 marks** (50%)"
- **Concern:** Rubric item 6 (factual overreach a teacher would challenge). The module states the Higher Level breakdown as Oral 100/Aural 100/Written 200 (25/25/50) and 'reading and writing sections are each worth approximately 100 marks'. The actual LC French HL split is Oral 100 (25%), Aural 80 (20%), Written 220 (55%, with reading ~120 and written production ~100); the 25/25/50 split is the Ordinary Level allocation. Presenting the OL breakdown as HL misdirects study-time allocation (the module's own core argument) and would be caught instantly by any French teacher or accreditation reviewer. The error is repeated in the Highlight tooltips (in-scope per amendment 1) and in Section 3's 'worth the same as the oral — 100 marks' claim about the aural.
- **Suggested action:** Correct to the real HL weightings (100/80/220) throughout Section 1, its highlights, and Section 3, or explicitly present both HL and OL splits. Verify against the SEC/curriculum spec per the accreditation dossier rule in CLAUDE.md.

### subject-german-protocol
- **Where:** subjectContentLanguages.ts line 388 (Section 3, first paragraph)
- **Quote:** "often score 15 to 20 marks higher than their written paper performance would predict"
- **Concern:** Rubric item 6 plus the project's accreditation rule (never state a specific figure without a verifiable source). This precise quantitative claim about oral-vs-written score differentials is presented as fact with no Cite reference and no plausible SEC or peer-reviewed source; it reads as an invented statistic and would be challenged by an accreditation reviewer.
- **Suggested action:** Either source it from a Chief Examiner report (examiner-reports/ library) or reframe qualitatively, e.g. 'the oral rewards direct preparation more reliably than any other component', per the project's cut-log process.

### subject-mathematics-protocol
- **Where:** subjectContentStem.ts line 28 (Section 1, para 1) and line 34 highlight; sourced to the 2015 Chief Examiner report per data/references/subjectMathematics.ts
- **Quote:** "you must answer **all** questions. There is no choice -- every question counts."
- **Concern:** Item 6 (factual overreach a teacher would challenge): the no-choice / Section A 6x25 + Section B 3-question format describes the canonical pre-2022 structure, but the 2022-2025 papers ran under SEC adjusted arrangements that introduced question choice; the claim is cited to a 2015 report. A maths teacher whose students sat recent papers, or an accreditation reviewer checking the citation date, could reasonably challenge this as stale or at least unhedged.
- **Suggested action:** Verify against the current-year SEC arrangements circular; either update the structure description or add a one-line hedge ('check the current year's arrangements on examinations.ie') and refresh the citation.

### subject-applied-maths-protocol
- **Where:** /Users/alexlinehan/Nextstepuni-Launch-/subjectContentStem.ts lines 146-259 (whole applied-maths entry; contrast mathematics entry lines 14-131)
- **Quote:** "you can solve nearly every collision problem that has appeared in the last 15 years"
- **Concern:** Rubric item 6 + project accreditation rule: the entry contains zero citations and no references list, unlike the sibling mathematics entry which uses {{cite:N}} markers and SUBJECT_MATHEMATICS_REFERENCE_LIST. Specific factual/overreach claims ('Most students can master both topics with 4-5 hours of focused practice', 'worth 10-15 marks before you even start solving', the 15-years claim) are unverifiable as written and, given the syllabus mismatch above, demonstrably unsafe. The repo's accreditation rule requires claims to be source-backed or reframed non-prescriptively.
- **Suggested action:** When rewriting, ground mark-allocation and structure claims in the current SEC marking schemes / Chief Examiner material via the Cite + references system, and add the compliance/evidence dossier entry per the pilot (active-recall) pattern.

### subject-computer-science-protocol
- **Where:** subjectContentStem.ts lines 639-641 (Section 1) and throughout
- **Quote:** "The [[written exam]] is a **2-hour paper** worth **70%** of your grade."
- **Concern:** Rubric item 6 (factual overreach a teacher would challenge): the LCCS end-of-course exam is the SEC's computer-based exam — candidates sit it at computers, and Section C involves working with actual program code in the exam environment. The module repeatedly frames it as a conventional 'written paper' and never mentions the computer-based format, which is one of the subject's defining features and materially affects exam preparation (typing answers, on-screen code work vs handwritten pseudocode).
- **Suggested action:** Rewrite Section 1 and related highlights to describe the computer-based delivery and the paper's actual section structure (including the on-computer programming section), and adjust the 'sketch pseudocode on paper' advice to fit the real exam environment.

### subject-economics-protocol
- **Where:** subjectContentBusiness.ts line 405 (Section 3, final paragraph)
- **Quote:** "if you score 90 in Section A and average 60 out of 75 on your four long questions, that gives you 330 out of 400 — a comfortable H1"
- **Concern:** Arithmetic/grading error independent of the stale structure: 330/400 = 82.5%, which is a H2 (H1 requires 90%+). Students planning to this benchmark would fall a full grade short of the promise.
- **Suggested action:** Correct the worked example to the real H1 threshold (or reframe as a H2 illustration) when rebuilding the section on the current 80/20 paper+SRP structure.

### subject-economics-protocol
- **Where:** subjectContentBusiness.ts line 478 (Section 6, Action Plan)
- **Quote:** "downloading the last 10 years of Economics HL papers and marking schemes. Create a [[topic frequency table]]"
- **Concern:** Only 2021-2025 papers exist under the current specification (repo holds exactly economics-2021 through 2025). A 10-year frequency table would be built mostly from old-syllabus papers with a different structure and partly different content, actively misleading topic prioritisation.
- **Suggested action:** Scope the instruction to papers from 2021 onward and note the syllabus change explicitly.

### subject-history-protocol
- **Where:** subjectContentHumanities.ts line 61 (Section 3 'Where Your Marks Are')
- **Quote:** "the **contextualisation** sub-question (typically worth 20 marks)"
- **Concern:** Rubric item 6: at Higher Level the contextualisation question is the largest DBQ sub-question — 40 marks in SEC marking schemes, not 20. The understatement contradicts the same paragraph's own advice that contextualisation is the one part requiring memorised preparation, and misweights where students should invest effort.
- **Suggested action:** Verify the current mark allocation against a recent SEC HL marking scheme in /examiner-reports/ and correct the figure.

### subject-history-protocol
- **Where:** subjectContentHumanities.ts lines 46 and 51 (Section 2 'What the Examiner Rewards', paragraph + 'SIP' Highlight description)
- **Quote:** "the key scoring unit is the [[SIP]] — a Significant Individual Point... Examiners allocate marks per SIP, so more developed points means more marks."
- **Concern:** Rubric item 6: 'SIP' is not SEC terminology, and HL History essays are not marked by tallying marks per point — SEC schemes use a cumulative mark for paragraphs plus a separate overall-evaluation mark. Presenting an invented scoring unit as the official examiner mechanism is exactly the overreach a teacher or accreditation reviewer would challenge, and it appears in both prose and a Highlight tooltip (amendment 1 surface).
- **Suggested action:** Reframe as informal study advice ('aim for 5-7 well-developed points per essay') or replace with the real marking structure (cumulative paragraph marks + overall evaluation), sourced from the marking schemes in /examiner-reports/history/.

### subject-geography-protocol
- **Where:** subjectContentHumanities.ts lines 149 and 155 (Section 1 paragraph 3 + 'Physical Geography' highlight tooltip)
- **Quote:** "[[Physical Geography]] (including your elective — Geoecology or the Atmosphere)"
- **Concern:** Rubric item 6 (factual overreach a teacher would challenge, surfaced partly in a Highlight tooltip per amendment 1): this conflates the LC Geography electives with the HL Options. The electives are 'Patterns and processes in economic activities' vs 'Patterns and processes in the human environment'; Geoecology and The Atmosphere–Ocean Environment are two of the four Higher-Level-only Options, and they are not part of Physical Geography core. The tooltip repeats it: 'Core physical processes plus your chosen elective (Geoecology or the Atmosphere)'. This could misdirect a student's study plan and would embarrass the app in front of a Geography teacher or accreditation reviewer.
- **Suggested action:** Rewrite Section 1 paragraph 3 and the 'Physical Geography' highlight to use the correct syllabus architecture: core (Physical + Regional + Geographical Skills), one elective (Economic Activities or Human Environment), and one HL-only Option (Global Interdependence, Geoecology, Culture and Identity, or Atmosphere–Ocean Environment).

### subject-home-economics-protocol
- **Where:** subjectContentPractical.ts lines 36, 38 (Section 1 paragraphs 2 and 4)
- **Quote:** "worth approximately **250 marks** (around 50% of the total)... worth approximately **80 marks (around 15%)**"
- **Concern:** Rubric item 6: mark allocations are wrong even where the component is real. The written paper is 320 marks (80% of 400), not ~250 (50%); the journal's 80 marks are 20%, not 15%. The percentages only sum because they accommodate the invented 35% practical. Bold formatting presents these as authoritative figures.
- **Suggested action:** Replace with the correct 320/80 split (80%/20%) as part of the Section 1 rewrite; cross-check every bolded figure against the SEC specification.

### subject-engineering-protocol
- **Where:** subjectContentPractical.ts lines 281, 283-284, 288, 315 (sections 1 and 3)
- **Quote:** "The assessment is split roughly **50/50 between the written exam and the practical project**"
- **Concern:** Rubric item 6 (factual claim a teacher would challenge). LC Engineering HL has THREE assessment components: the 300-mark written paper, the project, and a separate SEC Day Practical Examination — confirmed by the repo's own examiner-reports/engineering/2025-insights.md, which documents the 'Day 2 Practical Examination' marked out of 100 as a distinct component. The project alone is roughly 25%, not 'half your final grade' / 'roughly 50% of the total mark' (repeated in the Highlight tooltip at line 288 and again at line 315). The module never mentions the day practical exam at all, and it builds strategic advice ('safety net', 'the single biggest mark opportunity', 'half your grade — it deserves your best effort') on the inflated figure, so an Engineering teacher or accreditation reviewer would challenge both the number and the derived strategy. Note the error also lives in a Highlight description prop (amendment 1), not just prose.
- **Suggested action:** Rewrite sections 1 and 3 (and the 'practical project' Highlight tooltip) around the real three-component structure — written paper ~50%, project ~25%, day practical exam ~25% at HL — add the day practical exam as its own preparation target, and recalibrate the 'project is half your grade' strategy framing. Log the reframe in data/cutContent.ts per the accreditation workflow.

## LOW — 3 confirmed

### effective-struggle-protocol
- **Where:** components/EffectiveStruggleAndGrowthModule.tsx lines 410-565 (ConfidenceRetentionParadox), data arrays at 419-425
- **Quote:** "passiveRetention  = [0.85, 0.55, 0.38, 0.28, 0.22, 0.18]"
- **Concern:** Item 6 + amendment 7 (non-prose numeric claims): the Confidence Trap chart plots invented Day 0-30 confidence/retention curves with no citation and no 'illustrative' labelling, immediately after a chart that carries a 'Research Evidence' chip and verified R&K 2006 figures — giving fabricated time-series the same visual authority as cited data. The active-recall retention line also rises monotonically over 30 days (0.50→0.61), which is empirically wrong unless ongoing practice is assumed and stated. Under the repo's own accreditation rule (verifiable source or reframe), a DCU reviewer would ask which study produced the Day-14 values.
- **Suggested action:** Add an 'Illustrative model' chip and one-line caption (e.g. 'Schematic curves based on Bjork & Bjork's retrieval-vs-storage-strength model, not measured data'), and either flatten the active retention line or caption it as assuming continued weekly self-testing.

### mastering-the-creatives-protocol
- **Where:** components/MasteringTheCreativesModule.tsx lines 449-451, 467-470, 483-486, 498-501, 513-514 (all essentials branches) + line 462 (wheel outside conditional)
- **Quote:** "Your Visual Journal is worth 50% of your mark... The 16-bar melody is a puzzle with clear rules... In the Comparative Study, connect visual choices to themes."
- **Concern:** Rubric item 3 + amendment 2 (junior-path scoping): the essentials 'simplified variant' only shortens the LC prose — every essentials section still teaches Leaving-Cert-only assessment content (Visual Journal weighting, 16-bar melody question, Comparative Study/Film Noir), and the DeliberatePracticeWheel renders identically. Junior Cycle Visual Art and Music are assessed via CBAs with entirely different structures. Harmless today because jcStatus is 'coming-soon', but flipping that flag without authoring genuine JC content would put factually wrong curriculum guidance in front of 12-15-year-olds.
- **Suggested action:** Keep jcStatus 'coming-soon' until a real JC variant exists; when building it, replace section content with JC Visual Art / JC Music CBA structures rather than reusing essentials prose.

### exam-hall-strategies-protocol
- **Where:** courseData.ts line 463 (description) and components/ExamHallStrategiesModule.tsx line 859 (moduleDescription)
- **Quote:** "the practical tips that help top students turn what they know into the marks they deserve"
- **Concern:** Rubric item 5: exclusionary 'top student' framing. Positions the strategies as belonging to top students rather than the reader — directly against the DEIS-audience directive (frame around autonomy and incremental progress, not elite achievement).
- **Suggested action:** Reword to second person, e.g. 'the practical tips that help you turn what you know into the marks you deserve', in both courseData.ts and the module's moduleDescription.

## Not included: 185 low-severity observations (unverified by design) and 1 refuted flags.

## Completeness critic — structural gaps beyond per-module content

COMPLETENESS CRITIC REPORT — what the 83-module audit could not see

VERIFIED COVERAGE FACTS
- moduleRegistry.ts ids == courseData.ts ids, 83 = 83, zero orphans either direction; every `components/*Module.tsx` file is registered (no unreachable module components).
- `SUBJECT_MODULE_CONTENT` (subjectModuleData.ts merging the six subjectContent*.ts files) covers all 29 `subject-*` course entries 1:1 — no dangling or extra subject content blobs.
- CLAUDE.md's `data/examStrategy/` and `data/examQuestions/` do NOT exist in the repo (stale docs) — nothing there to audit.

GAP 1 — Cut Content page re-displays removed content VERBATIM to every student (highest priority)
- `data/cutContent.ts` (59 entries) stores the verbatim `original` of everything removed/reframed; `components/CutContentPage.tsx:114` renders `entry.original` on screen; the route is ungated (`components/AppRouter.tsx:442-448`) and the sidebar item is shown unconditionally to all students (`components/KnowledgeTree.tsx:119`, "Cut Content").
- The file's own header comment (data/cutContent.ts ~line 17-20) claims it is "admin/owner reference — not student-facing guidance", but no role gate exists. CLAUDE.md makes logging every removal here MANDATORY, so any removal the audit makes will, per repo process, resurface verbatim on a student-visible page — defeating the removal.
- Corollary inconsistency: the calibration removal (urine-colour hydration advice) is NOT logged in cutContent.ts (grep "urine" — zero hits in that file, and git history shows it never touched the module files). So either the audit workflow is skipping the repo's mandatory cut-log, or removals are logged and re-exposed. Both branches need a decision: gate/curate CutContentPage, or exempt appropriateness-removals from the verbatim log.

GAP 2 — Junior Cycle parallel copy renders text the audit likely never assessed
- `components/ModuleShared.tsx:299-315` (`PersonalStory` `junior` prop): when `user.curriculumLevel === 'junior'`, name/role/body are swapped for alternate JC copy. 11 module files carry `junior={{...}}` variants. Auditors reading a module "as rendered" for a senior student would produce placement metadata that doesn't cover the JC render path.
- Same pattern in quest/reward copy: `questData.ts` has parallel JC quest strings (`onboard-jc-1..7`, `p-jc-*`, lines 28-80) in a deliberately looser peer voice ("Crack open your first module", "Don't break the streak"). Content is benign on inspection, but it's a second student-visible voice keyed off curriculum level that the module-file audit would not have surfaced.

GAP 3 — moduleSections.ts is an unsynced duplicate of section titles, shown pre-entry
- `moduleSections.ts` hand-duplicates section titles/eyebrows for the 54 non-subject modules; `components/ModuleShowcase.tsx:73` renders it on the module picker (subject modules fall back to live SUBJECT_MODULE_CONTENT). Spot checks (game-day, procrastination, note-taking-paradox, exam-crisis) currently match the components, but any audit fix that renames/removes a section will NOT propagate — a removed section title would keep appearing on the showcase. Note exam-crisis titles surfaced there include "Sleep: Your Secret Weapon" and "Food and Focus" — health-framed headings visible before entering the (flagged) module. Any content edits from this audit must be mirrored here.

GAP 4 — Module-flow copy outside module files (reviewed; mostly benign, but audit didn't see it)
- `studySessionData.ts:207-333` — ~108 STRATEGY_PROMPTS attributed by `moduleId` to 9 audited modules, shown as in-session overlays (StudySessionView). Content reviewed: standard study advice, nothing rubric-violating; a few rhetorical quantifications ("30 minutes of real focus beats 2 hours of half-attention", line 304) sit outside the citation-governance that applies to the modules they claim to speak for.
- `components/ReflectionModal.tsx:74-82` — 7 rotating debrief prompts; benign.
- `components/ModuleCompleteScreen.tsx` — completion celebration; copy benign ("Module Complete", stats, user's own North Star quote). (Design-only note: off-token emerald #6EE7B7/#059669 at lines 48/60 — known green-migration debt.)
- `components/ModuleLayout.tsx` / `ModuleShared.tsx` chrome labels ("Quick Challenge", "Key Insight", "Key Lever", Reading Comfort) — benign; the `northStarNudge` line in MicroCommitment (ModuleShared.tsx:205-209) echoes strings authored inside the module files, so audit saw those.
- `data/references/*.ts` — student-visible via ReferencesModal; citation lists only, benign.

GAP 5 — Six subject modules absent from the flagged list: confirm they were actually read
`subject-biology`, `subject-business`, `subject-physics`, `subject-classical-studies`, `subject-dcg`, `subject-technology` are in courseData/SUBJECT_MODULE_CONTENT but not in the 58 flagged ids. If the flag list is also the audit's coverage record, verify these six subjectContent entries were opened (subjectContentStem.ts, subjectContentBusiness.ts, subjectContentHumanities.ts, subjectContentPractical.ts). My keyword sweep of those files found only curricular content (diet/food-science hits are Home Ec / Ag Science syllabus material, not advice).

OUT OF SCOPE BUT ADJACENT (no action needed): `data/knowledge/*`, `catchUpLaneData.ts`, `commandWordData.ts`, examRepsData feed Innovation-Zone tools, not the 83 modules; the kidney/urine hits there (catchUpLaneData.ts:660-668) are legitimate LC Biology syllabus content, not the removed hydration advice.

VERDICT: Component/courseData coverage itself was structurally complete (no unreachable module files), but the audit could not see four real student-visible surfaces: the ungated Cut Content page re-exposing removals verbatim (Gap 1, actionable now), the Junior Cycle copy variants (Gap 2), the duplicated showcase section titles (Gap 3), and the module-attributed study-session prompts (Gap 4 — reviewed here, benign).