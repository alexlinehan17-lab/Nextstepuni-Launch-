/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

// ── Subject-specific guidance based on SEC examiner report patterns ──────────
// Grade-band-aware advice grounded in the Irish Leaving Cert exam context.
// Sources: SEC Chief Examiner Reports, marking scheme commentary, and common
// pitfalls observed across exam cycles.

export interface SubjectGuidance {
  commonStruggles: string[];   // why students at this level typically get stuck
  actions: string[];           // concrete, exam-context-specific actions
  examTrap: string;            // the one thing to stop doing
  mindsetShift: string;        // reframe that unlocks progress
}

export type GradeBand = 'low' | 'mid' | 'high';

// low:  H5–H8 / O3–O8 — fundamentals and exam literacy
// mid:  H3–H4 / O1–O2 — bridging to excellence
// high: H1–H2         — refinement, consistency, top-mark technique

export const SUBJECT_GUIDANCE: Record<string, Record<GradeBand, SubjectGuidance>> = {

  // ═══════════════════════════════════════════════════════════════════════════
  // ENGLISH
  // ═══════════════════════════════════════════════════════════════════════════
  'English': {
    low: {
      commonStruggles: [
        'Examiners consistently note that weaker candidates reproduce pre-learned essays rather than engaging with the task set. Your answer must respond to the specific question on the paper.',
        'Paper 1 comprehension answers are too vague — students lift chunks of the passage without explaining them in their own words.',
        'Poor time management: spending too long on Paper 1 Q.A and running out of steam for the composition.',
      ],
      actions: [
        'For every past paper composition, underline the key instruction words (discuss, argue, describe, narrate) before writing a single word.',
        'Practice the "PEEL" paragraph: Point, Evidence, Explanation, Link. Examiners award marks for developed points, not quantity.',
        'Do 3 timed Paper 1 comprehensions (Q.A only) per week — 40 minutes each. Check the marking scheme after to see exactly what scored.',
      ],
      examTrap: 'Memorising full essays and hoping one will fit. The examiner can tell — the Chief Examiner Report flags "pre-prepared material that does not address the task" every year.',
      mindsetShift: 'The exam doesn\'t test what you know about texts — it tests whether you can think on the page. Your own voice, responding to what\'s asked, is worth more than any memorised quote.',
    },
    mid: {
      commonStruggles: [
        'Answers show understanding but lack the "personal engagement" examiners look for at the higher grades — your response reads as competent but not distinctive.',
        'Comparative study answers tend to describe each text separately rather than weaving genuine comparison throughout.',
        'Paper 1 compositions have a solid start but lose momentum — the conclusion often feels rushed or tacked on.',
      ],
      actions: [
        'For your single text, develop 3 strong personal responses with specific quotes — "I found this disturbing because..." is worth more than a paragraph of plot summary.',
        'In comparative, use link phrases that force real comparison: "While Text A approaches this through..., Text B subverts this by..." in every paragraph.',
        'Plan your composition in 5 minutes: opening hook, 3–4 body movements, and a closing image or idea. Know your ending before you start.',
      ],
      examTrap: 'Writing everything you know about a text instead of answering the specific question. An examiner remarked: "Candidates who select and shape material to the question consistently outperform those who reproduce learned content."',
      mindsetShift: 'The gap between H4 and H2 isn\'t knowledge — it\'s craft. You already know enough. Now focus on how you use it: sharper arguments, more precise quotes, a real personal voice.',
    },
    high: {
      commonStruggles: [
        'At this level the Chief Examiner notes that the difference is "originality of thought and expression" — your analytical points are sound but may lack the distinctive insight that separates H1 from H2.',
        'Comparative answers may be well-structured but rely on obvious connections rather than nuanced, surprising links between texts.',
        'Paper 1 compositions are polished but sometimes play it safe — examiners reward candidates who take controlled creative risks.',
      ],
      actions: [
        'For each text, find one interpretation that goes against the obvious reading. Examiners specifically note they reward "sophisticated and original engagement."',
        'Read 2–3 quality opinion pieces per week (Irish Times, The Atlantic) to absorb how strong writers structure arguments — this directly improves your Paper 1 register.',
        'In your final comparative revision, identify one thematic tension (not just a theme) that connects all three texts — e.g. "the failure of language to capture experience."',
      ],
      examTrap: 'Over-quoting. At H1 level, a well-integrated short quote embedded in your own sentence is worth more than a block quote followed by explanation.',
      mindsetShift: 'You\'re not answering an English exam — you\'re writing something worth reading. The examiner has 400 scripts. Make yours the one they remember.',
    },
  },

  // ═══════════════════════════════════════════════════════════════════════════
  // IRISH
  // ═══════════════════════════════════════════════════════════════════════════
  'Irish': {
    low: {
      commonStruggles: [
        'The examiner report consistently flags "anglicised Irish" — sentences that follow English grammar patterns rather than natural Irish syntax.',
        'Aural comprehension scores are low because students don\'t practise listening to spoken Irish regularly outside the classroom.',
        'Reading comprehension answers often lift phrases from the passage without demonstrating understanding — examiners look for answers "i d\'fhocail féin" (in your own words).',
      ],
      actions: [
        'Learn 10 key "nathanna cainte" (set phrases) per topic area — these score heavily and signal fluency: "is léir dom," "dar liom féin," "tá sé soiléir go."',
        'Listen to TG4 news or Raidió na Gaeltachta for 10 minutes daily — even passive listening trains your ear for the aural exam.',
        'For Ceapadóireacht, master the structure of one essay type (litir/aiste/scéal) with clear opening, 3 developed paragraphs, and a conclusion. Examiners reward structure.',
      ],
      examTrap: 'Translating English thoughts word-by-word into Irish. This produces unnatural sentences that examiners can identify immediately. Think in short, correct Irish sentences rather than complex English ones translated badly.',
      mindsetShift: 'You don\'t need to write beautifully — you need to write correctly and clearly. Five simple, correct Irish sentences score higher than two complex, error-filled ones.',
    },
    mid: {
      commonStruggles: [
        'Prose and poetry answers show comprehension but lack the depth of analysis — examiners note that mid-range candidates "describe content rather than analyse technique."',
        'Ceapadóireacht essays plateau because students use the same limited vocabulary — the range and accuracy of "stór focal" is what separates grades.',
        'The Oral exam is often under-prepared — it\'s worth 40% and many students don\'t practise speaking beyond class.',
      ],
      actions: [
        'For Filíocht, learn 3 technical terms per poem (meafar, íomhánna, fuaim-focail) and practise using them: "Úsáideann an file meafar chun..." This is exactly what the marking scheme rewards.',
        'Build topic vocabulary lists: 10 advanced phrases each for sport, environment, technology, school life. Use them in compositions to show range.',
        'Record yourself answering Oral exam questions (Sraith Pictiúr, conversation topics) weekly. Listen back — fluency improves dramatically with self-monitoring.',
      ],
      examTrap: 'Spending equal time on all Oral sequences. Focus on your 5 weakest Sraith Pictiúr — examiners report that candidates who can handle unexpected sequences score significantly higher.',
      mindsetShift: 'The Oral is 40% of your total grade. Improving from a B to an A in the Oral is worth the same as jumping a full grade in a written paper. Prioritise it.',
    },
    high: {
      commonStruggles: [
        'The Chief Examiner notes that top candidates are distinguished by "saibhreas teanga" (richness of language) — your Irish is accurate but may lack the idiomatic flair that marks an H1.',
        'Prose/poetry analysis at the highest level requires genuine personal response — not just identifying techniques but explaining their effect on you as a reader.',
        'Ceapadóireacht at H1 requires a distinctive voice — examiners note that many competent essays feel "formulaic."',
      ],
      actions: [
        'Incorporate seanfhocail naturally into compositions and poetry answers — "Mar a deir an seanfhocal, \'Ní neart go cur le chéile.\'" Examiners specifically note this as a marker of excellence.',
        'For prose, develop one critical interpretation per text that shows original thinking: "Cé go gceapann formhór na ndaltaí go bhfuil..., measaim féin go..."',
        'Write one timed essay (Ceapadóireacht) per week under exam conditions. Get it checked for "botúin choitianta" that even strong students make.',
      ],
      examTrap: 'Being too safe in the Oral. At H1 level, examiners reward candidates who can discuss topics with "tuairimí pearsanta" and genuine spontaneity, not rehearsed scripts.',
      mindsetShift: 'At your level, Irish isn\'t about avoiding mistakes — it\'s about expressing complex ideas naturally. Think of yourself as someone who speaks Irish, not someone studying it.',
    },
  },

  // ═══════════════════════════════════════════════════════════════════════════
  // MATHEMATICS
  // ═══════════════════════════════════════════════════════════════════════════
  'Mathematics': {
    low: {
      commonStruggles: [
        'Examiners report that weaker candidates "apply procedures without understanding" — you can follow steps but struggle when questions are worded differently from what you practised.',
        'Not showing sufficient work: the marking scheme awards "attempt marks" and "method marks" even when the final answer is wrong. Blank spaces score zero.',
        'Basic algebra and manipulation errors cascade through multi-step questions, costing marks across the paper.',
      ],
      actions: [
        'Do one past paper question per topic, then immediately check the marking scheme — study HOW marks are awarded, not just the answer.',
        'For every question, write down the formula or method first before substituting numbers. Examiners award marks for stating the correct approach.',
        'Drill the fundamentals: simultaneous equations, factorising, indices rules. These aren\'t just standalone topics — they appear inside nearly every other question.',
      ],
      examTrap: 'Trying to memorise solutions to specific past paper questions. The SEC explicitly designs novel question contexts each year. Understanding the method is the only reliable strategy.',
      mindsetShift: 'Maths marks aren\'t about getting the right answer — they\'re about showing the right thinking. A question worth 25 marks might award 15 for method alone.',
    },
    mid: {
      commonStruggles: [
        'The examiner report notes mid-range candidates handle routine parts well but struggle with the "parts (c)" of questions — the parts requiring deeper application or proof.',
        'Geometry proofs and constructions are often underprepared — many students avoid them, but they\'re guaranteed marks.',
        'Statistics questions are frequently underperformed because students skip the interpretation parts ("What does this mean in context?").',
      ],
      actions: [
        'Target the constructions and theorems — there are only 22 constructions and a fixed set of proofs. These are the most predictable marks on the paper.',
        'For "in context" questions (especially statistics), always reference the original scenario in your answer. "The correlation coefficient of 0.87 suggests a strong positive relationship between study hours and exam results" — context scores.',
        'Time yourself on Paper 2 Section A — these should be fast, accurate marks. If you\'re spending more than 8 minutes per question here, you need more drill.',
      ],
      examTrap: 'Leaving out geometry/trigonometry proofs because they feel hard. The examiner report notes these questions have excellent "attempt marks" — even partial proofs score well.',
      mindsetShift: 'The H3 to H2 jump isn\'t about learning new maths — it\'s about becoming reliable on the parts (c) you currently skip or rush. Those 10-mark parts (c) are where grades are won.',
    },
    high: {
      commonStruggles: [
        'At H1 level, the Chief Examiner notes the difference is "precision and completeness" — top candidates lose marks on minor omissions like not stating conditions or not fully justifying steps.',
        'Problem-solving questions (Paper 2 Section B) require connecting multiple topics — strong candidates sometimes tunnel-vision on one approach rather than stepping back.',
        'Careless arithmetic errors under time pressure. At this level, every lost mark hurts disproportionately.',
      ],
      actions: [
        'On every proof or "show that" question, explicitly state each logical step. The marking scheme deducts for assumed steps, even when the answer is correct.',
        'For the final 10 minutes of each paper, go back and verify arithmetic on your highest-value answers. One caught error can be worth a grade.',
        'Do 3 full past papers under strict timed conditions before the exam. Your time management needs to be automatic — this is the only way to build it.',
      ],
      examTrap: 'Spending too long perfecting one question. At H1 level, time discipline is crucial — move on after your allocated time and come back if you can.',
      mindsetShift: 'At your level, you can do the maths. The exam is a performance — accuracy under pressure, clear communication of method, and disciplined time management.',
    },
  },

  // ═══════════════════════════════════════════════════════════════════════════
  // BIOLOGY
  // ═══════════════════════════════════════════════════════════════════════════
  'Biology': {
    low: {
      commonStruggles: [
        'Examiners report that weaker candidates give "definitions without understanding" — memorised lines that can\'t be applied to unfamiliar scenarios.',
        'Mandatory experiment answers are vague: students describe the experiment in general terms rather than giving precise procedure, results, and conclusions.',
        'Diagram labelling is imprecise — lines don\'t clearly point to the correct structure, or labels are incomplete.',
      ],
      actions: [
        'For each mandatory experiment, write out: aim, method (step-by-step), expected result, and conclusion. The marking scheme awards marks for each of these separately.',
        'Use the "define, explain, example" approach: learn the definition, then explain it in your own words, then give a biological example. Examiners test all three.',
        'Practise drawing and labelling the key diagrams (heart, plant cell, DNA replication) until you can do them from memory with all labels correct.',
      ],
      examTrap: 'Learning off long paragraphs of notes and hoping to write them out. The examiner specifically notes that "rote-learned material that does not address the question" scores poorly.',
      mindsetShift: 'Biology isn\'t about memorising facts — it\'s about understanding processes. If you can explain WHY something happens (not just WHAT happens), you\'ll answer any question.',
    },
    mid: {
      commonStruggles: [
        'The examiner report notes mid-range candidates answer well on familiar topics but struggle to apply knowledge to "novel contexts" — experiments described differently, or organisms they haven\'t studied.',
        'Ecology questions are often underperformed: students know definitions but can\'t explain ecological relationships in context.',
        'Genetics problems lose marks through poor presentation — Punnett squares not clearly laid out, or phenotype ratios not stated.',
      ],
      actions: [
        'For ecology, learn 2 specific named examples for each concept (named organism, named ecosystem). "The peppered moth" is better than "an organism that adapted."',
        'Practise 5 genetics problems per week — cross them off as you go. The marking scheme gives marks for correctly setting up the cross, not just the final ratio.',
        'When a question says "explain," always include the mechanism: "Osmosis occurs because water moves from a region of high water concentration to low water concentration across a semi-permeable membrane." Each underlined part scores.',
      ],
      examTrap: 'Skipping the longer Section C questions because they look harder. They\'re worth 60 marks each — and the marking scheme is often more generous than Section B because more valid answers are accepted.',
      mindsetShift: 'The jump to H2 comes from connecting topics. Respiration links to ecology links to enzymes links to food science. The examiner loves questions that cross topic boundaries — prepare for them.',
    },
    high: {
      commonStruggles: [
        'At H1 level, the examiner distinguishes candidates by "depth and precision of scientific language" — vague terms like "stuff" or "things" cost marks even when the understanding is there.',
        'Experimental design questions require students to identify variables, controls, and replicates — even strong candidates sometimes omit the control.',
        'Long-answer questions sometimes lack structure — a wall of text without clear paragraphing or logical flow.',
      ],
      actions: [
        'Replace every vague term with the correct scientific term: "glucose" not "sugar," "semi-permeable membrane" not "the thing that lets stuff through." Precision is the H1 marker.',
        'For any experiment question, always state: independent variable, dependent variable, controlled variables, and control experiment. This is the SEC\'s framework.',
        'Structure long answers with clear topic sentences: "The first stage of respiration is glycolysis, which occurs in the cytoplasm..." Each new stage or concept gets its own paragraph.',
      ],
      examTrap: 'Over-writing. At H1 level, examiners note that concise, precise answers often outscore lengthy ones. Say it once, say it correctly, move on.',
      mindsetShift: 'You know the biology. Now write like a scientist — precise, structured, evidence-based. Every sentence should earn a mark.',
    },
  },

  // ═══════════════════════════════════════════════════════════════════════════
  // CHEMISTRY
  // ═══════════════════════════════════════════════════════════════════════════
  'Chemistry': {
    low: {
      commonStruggles: [
        'The examiner report highlights that weaker candidates confuse similar concepts: oxidation/reduction, endothermic/exothermic, empirical/molecular formula.',
        'Calculation questions lose marks at multiple stages because students don\'t show the mole calculation steps — the marking scheme awards intermediate marks.',
        'Mandatory experiment write-ups are too vague — "we added the chemicals and heated them" doesn\'t score.',
      ],
      actions: [
        'Make flashcards for the 15 most commonly confused pairs (acid/base, oxidising/reducing agent, rate/equilibrium). Test yourself until they\'re automatic.',
        'For every calculation, write: formula → substitution → intermediate answer → final answer with units. The marking scheme typically awards 4 separate marks across these steps.',
        'Rewrite each mandatory experiment as a numbered procedure (1. Rinse the burette with... 2. Fill with... 3. Record initial reading...). Examiners award marks for procedural precision.',
      ],
      examTrap: 'Skipping definitions questions because they seem like "easy marks you\'ll get anyway." The examiner notes that definitions are frequently poorly answered — learn the exact textbook wording.',
      mindsetShift: 'Chemistry has a precise language. Learning to use it correctly (moles, concentration, yield) is half the battle — once you speak the language, the concepts follow.',
    },
    mid: {
      commonStruggles: [
        'Organic chemistry reaction sequences are where mid-range candidates lose marks — you know individual reactions but can\'t chain them together.',
        'Titration calculations are well-practised but the associated theory questions (why we use indicators, sources of error) are often weak.',
        'Equilibrium and rates questions require explanation, not just description — "explain why the rate increases" needs a molecular-level answer.',
      ],
      actions: [
        'Map out the organic chemistry pathways: ethanol → ethanal → ethanoic acid → ethyl ethanoate. Learn the reagent, catalyst, and conditions for each step. Examiners test the chain, not just individual reactions.',
        'For every mandatory experiment, prepare 2 genuine sources of error and how they\'d affect results. "Human error" is not accepted — "parallax error when reading the meniscus" is.',
        'When explaining rate changes, always reference collision theory: "Increasing temperature increases the kinetic energy of molecules, leading to more frequent collisions with energy ≥ Ea."',
      ],
      examTrap: 'Ignoring the option topics (atmospheric chemistry, materials, etc.) because they seem minor. They\'re worth a full question — and are often the least competitive marks on the paper.',
      mindsetShift: 'Chemistry at H3/H2 level is about depth, not breadth. You know the topics — now go deeper into the "why" behind each reaction.',
    },
    high: {
      commonStruggles: [
        'The examiner notes that even top candidates lose marks on "discuss" and "explain" questions by not providing enough distinct points — each mark requires a separate, valid point.',
        'pH and equilibrium calculations sometimes have subtle traps (dilution effects, weak acid assumptions) that catch candidates who work on autopilot.',
        'Industrial chemistry and societal applications of chemistry are sometimes underprepared relative to the core theory.',
      ],
      actions: [
        'For "discuss" questions, count the marks available and ensure you make at least that many distinct points. 6 marks = 6 separate facts or explanations.',
        'Practise pH calculations for weak acids (Ka expressions) and buffer solutions until they\'re automatic. These questions differentiate at the top.',
        'Know one real-world application for each major topic area — the examiner notes that top candidates "demonstrate awareness of chemistry in context."',
      ],
      examTrap: 'Rushing through the early, "easier" questions. At H1 level, dropping marks on Section A definitions or straightforward calculations is what costs the grade.',
      mindsetShift: 'The H1 paper rewards completeness. Answer every part of every question — even partial attempts on hard parts score. Leave nothing blank.',
    },
  },

  // ═══════════════════════════════════════════════════════════════════════════
  // PHYSICS
  // ═══════════════════════════════════════════════════════════════════════════
  'Physics': {
    low: {
      commonStruggles: [
        'Examiners report that weaker candidates "state formulae but cannot apply them to problems" — particularly when the question uses unfamiliar wording.',
        'Units are consistently omitted or wrong. The marking scheme often has a dedicated mark for correct units.',
        'Mandatory experiment descriptions lack the precise detail that scores — "set up the apparatus" gets zero marks.',
      ],
      actions: [
        'For each formula, practise 3 rearranged versions (e.g. v = fλ → f = v/λ → λ = v/f). Many questions require you to rearrange before substituting.',
        'After every calculation, check your units match what was asked. Force = Newtons, Energy = Joules, Wavelength = metres. Write them explicitly.',
        'For each mandatory experiment, know: what you measure, what you vary, what you keep constant, and how you use the results. The marking scheme checks each of these.',
      ],
      examTrap: 'Skipping the "describe an experiment" questions because you think you need to remember every detail. The examiner awards marks for the key steps — a clear, logical procedure with measurements scores well even if it\'s not word-perfect.',
      mindsetShift: 'Physics problems are puzzles, not memory tests. If you understand what each formula means (not just what it looks like), you can solve questions you\'ve never seen before.',
    },
    mid: {
      commonStruggles: [
        'Explanation questions require linking cause and effect — "explain why the image is inverted" needs a ray diagram AND a verbal explanation, not just one.',
        'Students handle calculation-heavy topics well but underperform on conceptual topics like particle physics, nuclear physics, and wave phenomena.',
        'Graph interpretation questions lose marks when students describe the graph shape but don\'t extract specific values or explain physical significance.',
      ],
      actions: [
        'For every "explain" question, use the format: "Because [cause], [effect] occurs. This means [consequence]." This three-part structure matches how marks are awarded.',
        'Draw ray diagrams and circuit diagrams neatly with a ruler. Examiners explicitly state that "poorly drawn diagrams cannot be awarded full marks."',
        'When reading graphs, always: (1) state what the axes represent, (2) identify the relationship (linear, inverse, etc.), (3) calculate the slope if relevant.',
      ],
      examTrap: 'Avoiding the option question you didn\'t study. Read both options on exam day — sometimes the "other" option has more straightforward parts than you expect.',
      mindsetShift: 'The jump from H4 to H2 in Physics comes from explaining, not just calculating. For every formula you know, ask yourself: "What does this physically mean?"',
    },
    high: {
      commonStruggles: [
        'At the highest level, the examiner notes that marks are lost on "precision of language" — saying "light bends" instead of "light refracts" costs marks.',
        'Derivation and proof questions require every step to be shown and justified — skipping "obvious" steps loses marks.',
        'Time pressure on the longer calculation questions — strong candidates sometimes don\'t finish the paper.',
      ],
      actions: [
        'Use the precise physical term in every answer: refraction not bending, diffraction not spreading, electromagnetic induction not "making electricity."',
        'For derivations, write out every algebraic step and state the physical principle at each stage: "By conservation of energy..." or "Applying Newton\'s second law..."',
        'Do 2 full papers under timed conditions. Identify which question types take you longest and drill those specifically.',
      ],
      examTrap: 'Over-explaining simple parts and under-explaining complex parts. Allocate your time by marks, not by perceived difficulty.',
      mindsetShift: 'At H1 level, you\'re a physicist explaining your reasoning, not a student answering questions. Precision, clarity, and completeness on every line.',
    },
  },

  // ═══════════════════════════════════════════════════════════════════════════
  // HISTORY
  // ═══════════════════════════════════════════════════════════════════════════
  'History': {
    low: {
      commonStruggles: [
        'The examiner report flags that weaker candidates write "narrative accounts" rather than answering the question — telling the story without analysis.',
        'Document-based question (DBQ) answers often fail to engage with the source — students write about the topic generally instead of analysing what the document shows.',
        'Key concepts (sovereignty, nationalism, propaganda) are used without being defined or explained.',
      ],
      actions: [
        'For every essay question, identify what type of answer is needed: causes, consequences, significance, or comparison. Then structure your answer around that — not chronological narrative.',
        'For DBQs, use the formula: "This source shows [content]. This is significant because [context]. However, we should consider [bias/limitation]." This mirrors the marking scheme.',
        'Learn 5 key dates and 5 key quotes per topic. A specific date or a short primary source quote signals to the examiner that you know your material.',
      ],
      examTrap: 'Writing everything you know about a topic in chronological order. The examiner specifically awards marks for "relevance and focus" — a short, focused answer outscores a long, unfocused one.',
      mindsetShift: 'History isn\'t about what happened — it\'s about why it happened and why it mattered. The examiner is looking for your analysis, not your memory.',
    },
    mid: {
      commonStruggles: [
        'Essays have a clear structure but lack the "sustained argument" examiners look for — each paragraph makes a point but they don\'t build towards a conclusion.',
        'Research Study answers are often descriptive rather than evaluative — "I found out that..." instead of "This reveals that..."',
        'Case study detail is thin — broad statements without specific evidence from the case study.',
      ],
      actions: [
        'Open every essay with a thesis statement that directly answers the question. Then use each paragraph to support that thesis with evidence. The conclusion should refer back to it.',
        'For the Research Study, structure your answer around the specific question asked. Examiners note that candidates who tailor their RSP to the exam question score significantly higher.',
        'For each case study, know 3 specific facts (names, dates, statistics) that you can deploy as evidence. "The Marshall Plan provided $13 billion" is worth more than "America gave money."',
      ],
      examTrap: 'Spending too long on Section A (documents) and not leaving enough time for the essays. The essays carry more marks — allocate your time accordingly.',
      mindsetShift: 'The H3 to H2 jump is about argument, not information. You need to make a case, use evidence to support it, and reach a justified conclusion.',
    },
    high: {
      commonStruggles: [
        'The Chief Examiner notes that top candidates are distinguished by "historiographical awareness" — understanding that history involves interpretation, not just facts.',
        'Source evaluation at the highest level requires commenting on provenance, purpose, and reliability — not just content.',
        'The best essays show awareness of historical debate: "While traditional accounts emphasise..., revisionist historians argue..."',
      ],
      actions: [
        'For at least one essay topic, learn two contrasting historical interpretations. This demonstrates the "critical analysis" the examiner identifies as the H1 marker.',
        'When evaluating sources, always comment on: who created it, when, for what purpose, and how this affects its reliability. Each of these is a separate mark.',
        'Your conclusion should do more than summarise — it should evaluate the relative importance of the factors you\'ve discussed.',
      ],
      examTrap: 'Writing an answer that\'s impressive but doesn\'t quite match the question. At H1 level, the examiner penalises "learned answers deployed without sufficient adaptation to the question set."',
      mindsetShift: 'At H1, you\'re not a student recounting history — you\'re a historian making an argument. Engage with the complexity and ambiguity.',
    },
  },

  // ═══════════════════════════════════════════════════════════════════════════
  // GEOGRAPHY
  // ═══════════════════════════════════════════════════════════════════════════
  'Geography': {
    low: {
      commonStruggles: [
        'Examiners note that short-answer questions are poorly answered because students give one-word answers when 2-3 developed points are needed.',
        'Sketches and diagrams are frequently missing or too vague to score — the examiner can\'t award marks for unlabelled drawings.',
        'Case study knowledge is shallow — students name a case study but can\'t provide specific details from it.',
      ],
      actions: [
        'For each topic, prepare one Irish and one global case study with 4 specific facts each (name, location, statistics, outcomes). "The Burren" alone scores 1 mark; specific karst features and processes score 4.',
        'Practise drawing the key diagrams: water cycle, rock cycle, plate boundaries, population pyramids. Label every part. The marking scheme awards marks per correct label.',
        'For short questions, always give more than the minimum. If a question is worth 3 marks, give 3 distinct points.',
      ],
      examTrap: 'Answering physical geography questions without diagrams. The examiner report states that "candidates who support their answers with clearly labelled diagrams consistently score higher."',
      mindsetShift: 'Geography rewards specifics. Replace "a river in Ireland" with "the River Shannon at Limerick." Replace "it rains a lot" with "annual precipitation of 1200mm on the west coast."',
    },
    mid: {
      commonStruggles: [
        'Long questions have the knowledge but lack the structure that examiners look for — answers read as a list of facts rather than a developed explanation.',
        'Human geography answers often lack the "geographical terminology" that scores at higher grades — urbanisation, counter-urbanisation, gentrification.',
        'OS map questions lose marks on grid references, scale calculations, and cross-section drawing.',
      ],
      actions: [
        'Structure long answers using the SES framework: State the process → Explain how it works → Support with a case study. Repeat for each part of the question.',
        'Build a glossary of 20 key geographical terms per unit. Use them explicitly: "This is an example of a corrie lake formed by glacial erosion" — the technical term scores.',
        'Practise 4-figure and 6-figure grid references until they\'re automatic. These are easy marks that shouldn\'t be dropped.',
      ],
      examTrap: 'Writing about processes without naming specific examples. The marking scheme consistently awards separate marks for "named example" and "relevant detail."',
      mindsetShift: 'Geography at H2 level is about demonstrating you understand processes AND can illustrate them with real places. Process + place = full marks.',
    },
    high: {
      commonStruggles: [
        'The examiner notes that H1 candidates demonstrate "integration of physical and human geography" — understanding how physical processes shape human activity.',
        'Geoecology and optional unit answers sometimes lack the depth of the core units.',
        'Essay-style answers at the highest level need a concluding evaluation, not just a summary.',
      ],
      actions: [
        'For at least 2 topics, prepare an answer that links physical and human geography: "Karst topography in the Burren limits agricultural productivity, leading to..."',
        'In your optional unit, ensure your case study detail matches the depth of your core units — the examiner marks them to the same standard.',
        'End every long answer with an evaluative conclusion: "The most significant factor in... is... because..." This shows the analytical thinking that distinguishes H1.',
      ],
      examTrap: 'Treating the exam as 4 separate sections. The strongest answers draw connections across the syllabus.',
      mindsetShift: 'Geography at H1 is about seeing the world as a system where everything connects. Demonstrate those connections and you\'ll stand out.',
    },
  },

  // ═══════════════════════════════════════════════════════════════════════════
  // BUSINESS
  // ═══════════════════════════════════════════════════════════════════════════
  'Business': {
    low: {
      commonStruggles: [
        'The examiner report notes that weaker candidates "define terms but cannot apply them" — especially in the Applied Business Question (ABQ).',
        'Short questions are answered too briefly — a 10-mark question needs developed points, not one-liners.',
        'ABQ answers are generic rather than being linked to the specific business scenario described.',
      ],
      actions: [
        'For every business concept, prepare: definition + real Irish business example. "Economies of scale — Ryanair achieves lower per-unit costs by operating a fleet of 500+ Boeing 737s."',
        'In the ABQ, reference the company in the stimulus material by name in every paragraph. The marking scheme specifically checks for "application to the case."',
        'For 10-mark short questions, aim for 5 developed points — each point stated AND briefly explained.',
      ],
      examTrap: 'Listing points without developing them. Writing "good communication, leadership, motivation" as a list scores far less than explaining each with a sentence.',
      mindsetShift: 'Business isn\'t a subject you memorise — it\'s a subject you understand through examples. Every concept connects to a real business doing real things.',
    },
    mid: {
      commonStruggles: [
        'Long questions show knowledge but lack the "evaluation" that examiners associate with higher grades — you describe but don\'t assess effectiveness.',
        'The people/HR unit is often weaker than management or enterprise because students find it harder to give concrete examples.',
        'Exam timing: spending too long on Q1 (ABQ) and rushing the long questions.',
      ],
      actions: [
        'Add evaluative phrases to your answers: "This is effective because...", "However, the limitation of this approach is...", "The most important factor is... because..."',
        'For HR/people topics, prepare 2 real Irish business examples (e.g. Aldi\'s training programme, Google Dublin\'s employee wellbeing initiatives).',
        'Time discipline: ABQ = 40 mins, each long question = 25 mins. Practise this timing on past papers.',
      ],
      examTrap: 'Ignoring the "illustrate your answer" instruction. When the question says illustrate, the marking scheme requires a relevant example — without it, you cap your marks.',
      mindsetShift: 'The difference between H4 and H2 in Business is depth, not breadth. Go deeper on fewer points rather than listing more surface-level ones.',
    },
    high: {
      commonStruggles: [
        'At H1 level, the examiner distinguishes candidates by their ability to "critically evaluate" — not just describe advantages and disadvantages but weigh them against each other.',
        'Enterprise and management theory answers sometimes lack contemporary examples.',
        'The ABQ at the highest level needs genuine analysis of the business situation, not just application of theory.',
      ],
      actions: [
        'Use current Irish business examples (within the last 2 years). The examiner notes that contemporary examples demonstrate genuine business awareness.',
        'In the ABQ, go beyond what\'s asked — if you\'re discussing marketing, briefly acknowledge how it connects to finance or HR. This shows integrated thinking.',
        'Every long answer should have a concluding paragraph that makes a judgement: "Overall, the most critical factor for this business is..."',
      ],
      examTrap: 'Playing it safe with textbook-only answers. H1 candidates bring in real-world knowledge that shows they understand business beyond the syllabus.',
      mindsetShift: 'At H1, you\'re not a Business student — you\'re a business analyst. Read the scenario, diagnose the issues, recommend solutions, and justify your thinking.',
    },
  },

  // ═══════════════════════════════════════════════════════════════════════════
  // ACCOUNTING
  // ═══════════════════════════════════════════════════════════════════════════
  'Accounting': {
    low: {
      commonStruggles: [
        'Errors in early entries cascade through entire accounts, losing marks at multiple stages. The examiner notes "fundamental errors in double entry" as the primary issue.',
        'Layout and presentation of accounts is poor — headings missing, columns misaligned, dates omitted.',
        'Theory questions are neglected in favour of accounts preparation, but they carry significant marks.',
      ],
      actions: [
        'Master the 5 core adjustments (depreciation, bad debts, prepayments, accruals, closing stock) until they\'re automatic. These appear in nearly every question.',
        'Use the correct layout for every account you prepare — the examiner awards marks for correct headings, format, and presentation separately from the figures.',
        'Allocate time for theory: 30% of marks are theory-based. Learn the definitions and purposes of each financial statement.',
      ],
      examTrap: 'Starting a question without reading it fully. The examiner notes that candidates often miss adjustments listed at the bottom of the question, costing easy marks.',
      mindsetShift: 'Accounting is logical, not random. Every debit has a credit. If your trial balance doesn\'t balance, one specific entry is wrong — find it systematically rather than guessing.',
    },
    mid: {
      commonStruggles: [
        'Ratio analysis and interpretation questions are often weak — students calculate ratios correctly but can\'t explain what they mean for the business.',
        'Club accounts and farm accounts have specific formats that differ from standard accounts — these catch students who haven\'t practised them.',
        'Published accounts adjustments (corporation tax, dividends, reserves) are where mid-range candidates lose marks.',
      ],
      actions: [
        'For every ratio, prepare a one-sentence interpretation: "A current ratio of 1.8:1 means the business has €1.80 in current assets for every €1 of current liabilities — this is healthy."',
        'Practise at least 2 full club account questions and 2 farm accounts. The format differences are learnable — don\'t leave them to chance.',
        'For published accounts, learn the specific adjustments: interim vs final dividends, transfers to reserves, corporation tax provision. These are tested every year.',
      ],
      examTrap: 'Not checking your trial balance before moving on. If it doesn\'t balance, you have an error that will cost marks throughout the question. Stop and find it.',
      mindsetShift: 'Accounting at H2 level requires you to think like an accountant, not a calculator. Understand WHY each adjustment is made and what it means for the financial statements.',
    },
    high: {
      commonStruggles: [
        'The examiner notes that top candidates lose marks on "analysis and interpretation" — the figures are perfect but the commentary lacks insight.',
        'Tabular statements and cash flow statements require meticulous accuracy — one wrong sign or classification costs multiple marks.',
        'Time pressure in the final question — strong candidates sometimes don\'t finish.',
      ],
      actions: [
        'When interpreting accounts, always make recommendations: "The declining gross profit margin suggests the business should review its cost of sales or pricing strategy." This is what separates H1 from H2.',
        'Double-check the sign conventions in cash flow statements: increases in debtors are cash outflows, increases in creditors are cash inflows. Errors here cascade.',
        'Practise full papers under time pressure — 20 minutes per question maximum. Build speed through repetition, not by rushing.',
      ],
      examTrap: 'Presenting perfect accounts without showing your workings. The examiner awards method marks — if your workings are visible, you score even if the final figure is wrong.',
      mindsetShift: 'At H1, accuracy is expected. What distinguishes you is the ability to read the story the numbers tell and communicate it clearly.',
    },
  },

  // ═══════════════════════════════════════════════════════════════════════════
  // ECONOMICS
  // ═══════════════════════════════════════════════════════════════════════════
  'Economics': {
    low: {
      commonStruggles: [
        'Examiners note that weaker candidates "describe economic concepts without using diagrams" — in Economics, the diagram IS the answer.',
        'Definitions are vague or inaccurate. The examiner awards specific marks for precise definitions.',
        'Short-answer questions get one-line responses when developed answers are needed.',
      ],
      actions: [
        'For every major concept (demand, supply, elasticity, market failure), draw the diagram AND write a 2-sentence explanation. The marking scheme awards marks for both.',
        'Learn the exact textbook definition for the 20 most common terms. "Demand is the quantity of a good consumers are willing and able to buy at a given price" — every word matters.',
        'For short questions worth 10+ marks, provide at least 4 developed points with brief explanations.',
      ],
      examTrap: 'Drawing supply/demand diagrams without labels. An unlabelled diagram scores zero. Always label: axes (Price/Quantity), curves (S/D), equilibrium point (P*, Q*).',
      mindsetShift: 'Economics is about how the world works. Connect every concept to a real example — "minimum wage" isn\'t abstract, it\'s the price floor on the labour market you\'ll work in.',
    },
    mid: {
      commonStruggles: [
        'Long-answer questions cover the topic broadly but don\'t address the specific question asked — particularly "evaluate" and "discuss" questions.',
        'Macroeconomic policy questions (fiscal/monetary) lack the cause-and-effect chain that examiners look for.',
        'Current economic affairs examples are outdated or generic.',
      ],
      actions: [
        'For policy questions, use the transmission mechanism: "The Central Bank reduces interest rates → cost of borrowing falls → investment increases → aggregate demand rises → economic growth." Each link is a mark.',
        'Follow Irish economic news weekly (CSO releases, Budget commentary). Use current data: "Ireland\'s corporation tax rate of 15% attracts FDI" scores better than generic statements.',
        'When "evaluating," always give both sides AND a conclusion: "While fiscal expansion increases demand, it may also increase government debt. In the current context, the trade-off is justified because..."',
      ],
      examTrap: 'Answering a microeconomics question with macroeconomics content (or vice versa). Read the question carefully — the examiner notes this is a common mid-range error.',
      mindsetShift: 'Economics at H2 level is about chains of reasoning, not isolated facts. Every policy has a mechanism, every mechanism has a consequence, every consequence has a trade-off.',
    },
    high: {
      commonStruggles: [
        'The Chief Examiner notes that H1 candidates show "critical awareness of economic models and their limitations" — acknowledging assumptions and real-world complications.',
        'Diagrams are correct but sometimes lack the detailed shifts needed to show the full economic story.',
        'International economics and development questions sometimes lack the depth of microeconomics answers.',
      ],
      actions: [
        'When using economic models, acknowledge their limitations: "The Phillips Curve suggests an inverse relationship between inflation and unemployment, however, this broke down during the stagflation of the 1970s."',
        'On diagrams, show the full story: original equilibrium, the shift, the new equilibrium, AND label the deadweight loss or welfare effects if relevant.',
        'Prepare one detailed Irish and one international example for each major policy area. The examiner rewards "informed awareness of economic issues."',
      ],
      examTrap: 'Presenting textbook answers without engagement. At H1 level, the examiner wants to see you think like an economist — weigh evidence, consider alternatives, reach a balanced judgement.',
      mindsetShift: 'At H1, you understand that economics is about trade-offs under uncertainty. Every answer should reflect that nuance.',
    },
  },

  // ═══════════════════════════════════════════════════════════════════════════
  // FRENCH (applies similarly to German/Spanish with language adjustments)
  // ═══════════════════════════════════════════════════════════════════════════
  'French': {
    low: {
      commonStruggles: [
        'The examiner notes that weaker candidates rely on "memorised phrases without adaptation" — producing answers that don\'t quite fit the question.',
        'Aural comprehension scores are low because students aren\'t exposed to spoken French at natural speed outside class.',
        'Written production uses present tense almost exclusively — the marking scheme specifically rewards use of multiple tenses.',
      ],
      actions: [
        'Learn 5 opinion phrases, 5 past tense structures, and 5 future tense structures. Use them in every written answer. The marking scheme awards marks for "range of language."',
        'Listen to French audio daily (podcasts like "Journal en français facile" or TV5Monde). Even 10 minutes builds the processing speed needed for the aural.',
        'For comprehension, answer in full sentences that rephrase the question: Q: "Où habite Marie?" A: "Marie habite à Paris, dans le cinquième arrondissement."',
      ],
      examTrap: 'Writing very short answers in the written production to avoid making errors. The marking scheme rewards "communication" — a longer answer with some errors outscores a short, perfect one.',
      mindsetShift: 'French isn\'t about being perfect — it\'s about communicating. The examiner rewards students who try to express ideas, even with grammar mistakes.',
    },
    mid: {
      commonStruggles: [
        'Written production plateaus because vocabulary range is limited — the same adjectives and verbs appear repeatedly.',
        'Reading comprehension answers show understanding but lack precision — vague paraphrasing rather than targeted answers.',
        'The Oral exam conversational element is where marks are lost — students give one-sentence answers instead of developing their responses.',
      ],
      actions: [
        'Build "upgrade" vocabulary: replace "bon" with "formidable/extraordinaire," "faire" with "réaliser/accomplir." Range of vocabulary is a specific marking criterion.',
        'In the Oral, develop every answer with: opinion + reason + example. "J\'aime le sport parce que c\'est bon pour la santé. Par exemple, je joue au football chaque samedi."',
        'For reading comprehension, underline the key words in the question FIRST, then find the corresponding section in the text. Answer precisely — don\'t add unrelated information.',
      ],
      examTrap: 'Spending too long on the comprehension sections and rushing the written production. The written section carries heavy marks and rewards preparation.',
      mindsetShift: 'At H2 level, it\'s your range that matters — different tenses, varied vocabulary, complex sentence structures. Show the examiner you can do more than survive in French.',
    },
    high: {
      commonStruggles: [
        'The examiner notes that H1 candidates demonstrate "authentic use of language" — idiomatic expressions, subjunctive mood, and varied syntax.',
        'Written production may be technically excellent but lack the "personal voice" that distinguishes the highest grades.',
        'Aural comprehension at the highest level requires catching nuance, inference, and implied meaning.',
      ],
      actions: [
        'Incorporate 3-4 idiomatic expressions naturally into your written production: "à mon avis," "il va sans dire que," "en ce qui concerne." These signal advanced fluency.',
        'Use the subjunctive where appropriate (après "il faut que," "bien que," "pour que"). This is the grammatical feature that marks H1 candidates.',
        'For aural, practise with authentic French media at full speed — not slowed-down classroom recordings. The exam aural is closer to natural speech.',
      ],
      examTrap: 'Over-preparing for the Oral with scripted answers. At H1 level, examiners test spontaneity — they will ask follow-up questions to push you beyond your prepared material.',
      mindsetShift: 'At H1, you\'re not translating from English — you\'re thinking in French. Let your personality come through in the language.',
    },
  },

  // ═══════════════════════════════════════════════════════════════════════════
  // APPLIED MATHS
  // ═══════════════════════════════════════════════════════════════════════════
  'Applied Maths': {
    low: {
      commonStruggles: [
        'Students struggle to translate word problems into mathematical equations — the gap between "a car accelerates" and "v = u + at" is too large.',
        'Sign convention errors (positive/negative direction) cascade through entire solutions.',
        'Diagrams are omitted — in Applied Maths, the free-body diagram IS the first step.',
      ],
      actions: [
        'For every problem: (1) draw a diagram, (2) label all forces/velocities, (3) choose a positive direction, (4) THEN write equations. Follow this order religiously.',
        'Master the 5 linear motion equations (suvat) until you can select the right one instantly based on what\'s given and what\'s asked.',
        'Practise past paper Q1 and Q2 (linear motion and projectiles) until they\'re automatic — these are the most accessible marks.',
      ],
      examTrap: 'Trying to solve problems in your head. Applied Maths requires systematic written working — the examiner awards marks at each stage.',
      mindsetShift: 'Applied Maths is physics with better maths. Every question is a real-world scenario — draw it, label it, and the equations follow.',
    },
    mid: {
      commonStruggles: [
        'Relative velocity and collisions questions are conceptually challenging — students apply formulas without understanding the physics.',
        'Connected particles (pulleys, wedges) require careful force resolution that mid-range candidates sometimes oversimplify.',
        'The statics question is often underprepared despite being highly predictable.',
      ],
      actions: [
        'For collisions, always check: is momentum conserved? Is energy conserved? These two questions determine which equations to use.',
        'For connected particles, draw a separate free-body diagram for EACH object. Resolve forces parallel and perpendicular to the motion. Don\'t combine objects until you have separate equations.',
        'Statics (moments) is the most predictable question on the paper. Practise 10 past paper statics questions — the same patterns repeat.',
      ],
      examTrap: 'Only preparing 6 topics and hoping the right ones come up. The paper has evolved — prepare at least 8 topics to guarantee choice.',
      mindsetShift: 'Applied Maths rewards problem-solving strategy, not memorised solutions. Learn to identify which physical principles apply, then build the solution from first principles.',
    },
    high: {
      commonStruggles: [
        'Differential equation and SHM questions require confident calculus — hesitation here loses time.',
        'The most challenging parts of questions require combining concepts from different topic areas.',
        'Precision in stating assumptions and initial conditions.',
      ],
      actions: [
        'SHM: memorise the standard results (x = A sin(ωt), v² = ω²(A² - x²)) and practise deriving them. Questions often start from first principles.',
        'For every solution, state your assumptions explicitly: "assuming no air resistance," "taking g = 9.8 m/s²." The marking scheme awards this.',
        'Practise the hardest past paper parts (c) from recent years. These are where H1 marks are won.',
      ],
      examTrap: 'Not checking dimensions. If your answer for velocity comes out in metres, something is wrong. Dimensional analysis catches errors.',
      mindsetShift: 'At H1, elegance matters. A clean, well-structured solution that flows logically impresses more than a correct answer reached through messy working.',
    },
  },

  // ═══════════════════════════════════════════════════════════════════════════
  // COMPUTER SCIENCE
  // ═══════════════════════════════════════════════════════════════════════════
  'Computer Science': {
    low: {
      commonStruggles: [
        'Coding questions are left blank or incomplete — students freeze when asked to write code under exam conditions.',
        'Theory concepts (abstraction, decomposition, algorithms) are described vaguely without concrete examples.',
        'The ALT (Applied Learning Task) portfolio is underdeveloped — it carries 20% and many students underinvest.',
      ],
      actions: [
        'Practise writing short Python functions on paper — no IDE, no autocomplete. The exam requires handwritten code. Do 3 per week.',
        'For each theory concept, prepare one concrete example: "Abstraction: a map abstracts a city by showing roads but hiding buildings."',
        'Start your ALT early and iterate. The marking rubric rewards "reflection on learning" — document what you tried, what failed, and what you learned.',
      ],
      examTrap: 'Relying on your IDE to find errors. In the exam, you need to trace code mentally. Practise desk-checking (tracing through code line by line with test values).',
      mindsetShift: 'Computer Science isn\'t about memorising code — it\'s about problem-solving. If you can break a problem into steps, you can code it.',
    },
    mid: {
      commonStruggles: [
        'Algorithm design questions (sorting, searching) are known in theory but students struggle to implement variations.',
        'Data representation (binary, hexadecimal, ASCII) questions lose marks through conversion errors.',
        'Longer programming questions lack structure — no comments, no clear variable naming, no logical flow.',
      ],
      actions: [
        'Implement bubble sort, linear search, and binary search from memory. Then practise modifying them — "sort in descending order" or "search for the closest value." Exam questions often twist the standard algorithm.',
        'Drill binary-decimal-hexadecimal conversions until they\'re instant. These are guaranteed marks.',
        'When writing code in the exam, use meaningful variable names and add brief comments. The marking scheme awards marks for "readability and structure."',
      ],
      examTrap: 'Ignoring the theory sections (ethics, hardware, networking) because you\'re strong at coding. These sections carry significant marks and are often easier than the programming questions.',
      mindsetShift: 'Computer Science at H2 level requires you to think about code, not just write it. Can you explain WHY bubble sort is O(n²)? Can you choose between algorithms and justify your choice?',
    },
    high: {
      commonStruggles: [
        'Complex programming questions require combining data structures (lists, dictionaries) with algorithms — handling nested structures confidently.',
        'Ethical and societal impact questions need depth — not just "privacy is important" but analysis of specific trade-offs.',
        'The ALT at the highest level needs genuine computational thinking, not just a working program.',
      ],
      actions: [
        'Practise problems that combine file I/O, data parsing, and algorithmic processing — these mirror the style of challenging exam questions.',
        'For ethics questions, use a framework: describe the technology, identify stakeholders, analyse benefits and risks, and make a justified recommendation.',
        'In your ALT reflection, demonstrate iterative development: "My first approach was X, but I realised Y was more efficient because Z."',
      ],
      examTrap: 'Writing working but inelegant code. At H1 level, examiners note efficiency matters — avoid unnecessary loops, use appropriate data structures, handle edge cases.',
      mindsetShift: 'At H1, you\'re a computational thinker, not just a coder. Elegance, efficiency, and clear communication of your approach are what separate the top grades.',
    },
  },
};

// ── Fallback for subjects without specific guidance ──────────────────────────

const GENERIC_GUIDANCE: Record<GradeBand, SubjectGuidance> = {
  low: {
    commonStruggles: [
      'Answers lack the specific detail examiners look for — general statements instead of precise, developed points.',
      'Past paper practice is insufficient — familiarity with how questions are worded and what the marking scheme rewards is essential.',
      'Time management during the exam leads to incomplete answers on later questions.',
    ],
    actions: [
      'Do one past paper question per topic and immediately check the marking scheme. Study how marks are awarded — this is more valuable than re-reading notes.',
      'For every answer, aim to develop each point: state it, explain it, and give a specific example.',
      'Practise under timed conditions at least twice before the exam. Know exactly how long you can spend on each question.',
    ],
    examTrap: 'Re-reading notes passively instead of actively testing yourself. The examiner tests recall and application — practise both.',
    mindsetShift: 'The exam doesn\'t test everything — it tests specific skills. Identify what the marking scheme rewards and focus your preparation there.',
  },
  mid: {
    commonStruggles: [
      'Answers demonstrate knowledge but lack the depth and evaluation that distinguish higher grades.',
      'Questions requiring application to new contexts or scenarios are weaker than straightforward recall questions.',
      'Some topic areas are stronger than others, creating gaps that limit overall performance.',
    ],
    actions: [
      'For each topic, go beyond "what" to "why" and "so what" — explanation and evaluation are where higher marks are awarded.',
      'Identify your 2-3 weakest topics and allocate focused revision time to them. Closing gaps is more valuable than perfecting strengths.',
      'Read the Chief Examiner Report for your subject — it explicitly states what distinguishes higher-performing candidates.',
    ],
    examTrap: 'Spending too long on questions you\'re comfortable with and rushing the ones you\'re not. Allocate time strictly by marks available.',
    mindsetShift: 'The jump from the mid-range to the top is rarely about knowing more — it\'s about using what you know more effectively.',
  },
  high: {
    commonStruggles: [
      'At this level, the examiner distinguishes candidates by precision of language, depth of analysis, and originality of thought.',
      'Minor errors and omissions accumulate — each lost mark matters disproportionately at the top.',
      'Time pressure can lead to rushed final answers that don\'t reflect your true ability.',
    ],
    actions: [
      'Review your answers for precision — replace vague terms with specific technical vocabulary.',
      'Do at least 2 full papers under strict exam conditions. Identify which questions take longest and refine your approach.',
      'For every "explain" or "discuss" question, aim for one insight that goes beyond the obvious. This is what examiners identify as H1-level thinking.',
    ],
    examTrap: 'Assuming you\'ll perform well because you know the material. Exam performance is a skill separate from knowledge — it requires practice.',
    mindsetShift: 'At H1, you\'re demonstrating mastery. Every answer should show not just that you know the material, but that you understand it deeply enough to apply it confidently.',
  },
};

// ── Language subjects that can reuse French guidance with slight adaptation ──

const LANGUAGE_SUBJECTS = ['German', 'Spanish', 'Italian', 'Japanese'];
for (const lang of LANGUAGE_SUBJECTS) {
  SUBJECT_GUIDANCE[lang] = {
    low: {
      ...SUBJECT_GUIDANCE['French'].low,
      commonStruggles: SUBJECT_GUIDANCE['French'].low.commonStruggles.map(s => s.replace(/French/g, lang)),
      actions: SUBJECT_GUIDANCE['French'].low.actions.map(s =>
        s.replace(/French/g, lang).replace(/français facile.*TV5Monde/, `${lang.toLowerCase()} language podcasts or radio`)
      ),
    },
    mid: {
      ...SUBJECT_GUIDANCE['French'].mid,
      commonStruggles: SUBJECT_GUIDANCE['French'].mid.commonStruggles.map(s => s.replace(/French/g, lang)),
    },
    high: {
      ...SUBJECT_GUIDANCE['French'].high,
      commonStruggles: SUBJECT_GUIDANCE['French'].high.commonStruggles.map(s => s.replace(/French/g, lang)),
      actions: SUBJECT_GUIDANCE['French'].high.actions.map(s => s.replace(/French/g, lang).replace(/français/g, lang.toLowerCase())),
    },
  };
}

// ── Lookup function ─────────────────────────────────────────────────────────

export function getGradeBand(grade: string): GradeBand {
  if (!grade) return 'low';
  if (grade.startsWith('H')) {
    const num = parseInt(grade.substring(1));
    if (num <= 2) return 'high';
    if (num <= 4) return 'mid';
    return 'low';
  }
  if (grade.startsWith('O')) {
    const num = parseInt(grade.substring(1));
    if (num <= 2) return 'mid';
    return 'low';
  }
  return 'low';
}

export function getSubjectGuidance(subjectName: string, grade: string): SubjectGuidance {
  const band = getGradeBand(grade);
  const subjectEntry = SUBJECT_GUIDANCE[subjectName];
  if (subjectEntry) return subjectEntry[band];
  return GENERIC_GUIDANCE[band];
}
