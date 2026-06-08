/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Catch-Up Lane content — absence-recovery micro-units.
 *
 * FIRST SLICE: Leaving Cert Biology (8 topics), tagged to real curriculum.ts
 * subtopic IDs. Authored from the LC Biology syllabus, source-grounded, the
 * same discipline as examRepsData.ts. Content scales subject-by-subject (the
 * way Exam Reps rolled out); these prove the format end to end.
 *
 * Content rule (per CLAUDE.md): no verbatim exam material; plain-language
 * paraphrase of syllabus content with the source named. Re-verify against the
 * current syllabus on the same cadence as examRepsData.ts.
 */

import { type RecoveryCard } from './types/catchUpLane';

export const RECOVERY_CARDS: RecoveryCard[] = [
  {
    id: 'bio-cell-structure',
    subjectId: 'biology', topicId: 'biology-1-0',
    subjectLabel: 'Biology', topicLabel: 'Cell Structure', level: 'common',
    gist: 'The cell is the basic unit of life. Animal and plant cells both have a cell membrane, cytoplasm, a nucleus, mitochondria and ribosomes. Plant cells have three extra structures: a cell wall (made of cellulose), a large permanent vacuole and chloroplasts.',
    oneMove: {
      label: 'Know what each organelle DOES, not just its name',
      text: 'Nucleus = controls the cell and holds the DNA · mitochondrion = releases energy (respiration) · chloroplast = photosynthesis · ribosome = makes protein · cell wall = support. The exam asks for the function, not just a label.',
    },
    check: {
      prompt: 'Name two structures found in a plant cell but not an animal cell, and give the function of one.',
      modelAnswer: 'Cell wall (made of cellulose) — gives the cell support and shape; and chloroplast — the site of photosynthesis. (A large permanent vacuole is also acceptable as the second structure.)',
      needed: ['Cell wall (cellulose)', 'Chloroplast (or large vacuole)', 'A correct function for one'],
    },
    source: 'LC Biology syllabus — Unit 2: The Cell',
    marksWeight: 9,
  },
  {
    id: 'bio-enzymes',
    subjectId: 'biology', topicId: 'biology-1-1',
    subjectLabel: 'Biology', topicLabel: 'Cell Metabolism', level: 'common',
    gist: 'Enzymes are biological catalysts — proteins that speed up reactions without being used up. Each enzyme is specific to its substrate (the lock-and-key idea). Activity rises with temperature up to an optimum, then falls sharply as the enzyme denatures. pH affects them in the same way.',
    oneMove: {
      label: "Say 'denatures', never 'dies'",
      text: "Above its optimum temperature the enzyme's shape changes permanently (it denatures), so the substrate no longer fits the active site and the reaction slows or stops. Enzymes aren't alive, so 'the enzyme dies' loses the mark.",
    },
    check: {
      prompt: "Explain what happens to an enzyme's activity above its optimum temperature, and why.",
      modelAnswer: "Activity falls sharply. The high temperature denatures the enzyme (changes its shape), so the active site no longer fits the substrate and the reaction slows or stops.",
      needed: ['Activity decreases / stops', 'Enzyme denatures (shape changes)', 'Active site no longer fits substrate'],
    },
    source: 'LC Biology syllabus — Unit 2: Cell Metabolism',
    marksWeight: 9,
  },
  {
    id: 'bio-cell-continuity',
    subjectId: 'biology', topicId: 'biology-1-2',
    subjectLabel: 'Biology', topicLabel: 'Cell Continuity', level: 'common',
    gist: 'Cell continuity is about how cells divide. Mitosis makes two daughter cells genetically identical to the parent — used for growth and repair. Meiosis makes four cells that are not identical and have half the chromosome number — used to make gametes (sex cells).',
    oneMove: {
      label: 'Match the division to its job',
      text: 'Mitosis → 2 identical cells → growth and repair. Meiosis → 4 different cells, half the chromosomes → gametes and variation. State the number of cells and the purpose and the marks are yours.',
    },
    check: {
      prompt: 'State one way the daughter cells of meiosis differ from those of mitosis.',
      modelAnswer: 'Meiosis produces cells with half the chromosome number (haploid) that are genetically different from one another; mitosis produces genetically identical cells with the full (diploid) chromosome number.',
      needed: ['Half the chromosome number (meiosis)', 'Genetically different / not identical', '(vs identical in mitosis)'],
    },
    source: 'LC Biology syllabus — Unit 2: Cell Continuity',
    marksWeight: 8,
  },
  {
    id: 'bio-genetics',
    subjectId: 'biology', topicId: 'biology-1-4',
    subjectLabel: 'Biology', topicLabel: 'Genetics', level: 'common',
    gist: 'A gene is a section of DNA that codes for a characteristic. You inherit two versions (alleles), one from each parent. A dominant allele shows its effect even with one copy; a recessive allele shows only when both copies are recessive. Genotype = the alleles (e.g. Tt); phenotype = the physical trait (e.g. tall).',
    oneMove: {
      label: 'Set up a Punnett square cleanly',
      text: 'Define your symbols first. Put one parent’s alleles along the top, the other’s down the side, fill the four boxes. Two heterozygous parents (Tt × Tt) give a 3:1 ratio of dominant:recessive.',
    },
    check: {
      prompt: 'Two parents are both Tt (T = tall, dominant). What ratio of tall to short offspring is expected?',
      modelAnswer: '3 tall : 1 short. The cross Tt × Tt gives TT, Tt, Tt, tt — three with at least one T (tall) and one tt (short).',
      needed: ['3 : 1 ratio', 'Tall : short', 'Shown via TT, Tt, Tt, tt'],
    },
    source: 'LC Biology syllabus — Unit 2: Genetics',
    marksWeight: 10,
  },
  {
    id: 'bio-nutrition-food-tests',
    subjectId: 'biology', topicId: 'biology-0-2',
    subjectLabel: 'Biology', topicLabel: 'Nutrition', level: 'common',
    gist: 'Food is made of biomolecules: carbohydrates (energy), lipids/fats (energy store and membranes) and proteins (growth and repair), plus vitamins, minerals and water. You should know a simple chemical test for the main food types.',
    oneMove: {
      label: 'Learn each test as reagent → colour change',
      text: 'Starch + iodine → blue-black. Reducing sugar + Benedict’s solution, heated → brick-red. Protein + biuret → purple/violet. Name the reagent AND the colour change — half an answer gets half the marks.',
    },
    check: {
      prompt: 'Describe a test for starch, including the result.',
      modelAnswer: 'Add iodine solution to the food sample. If starch is present, the iodine changes from orange/brown to blue-black.',
      needed: ['Iodine solution', 'Blue-black result', 'Colour change stated'],
    },
    source: 'LC Biology syllabus — Unit 1: Nutrition',
    marksWeight: 7,
  },
  {
    id: 'bio-ecology-principles',
    subjectId: 'biology', topicId: 'biology-0-3',
    subjectLabel: 'Biology', topicLabel: 'General Principles of Ecology', level: 'common',
    gist: 'An ecosystem is the living organisms in an area plus their non-living environment. Energy enters through producers (plants, by photosynthesis) and passes along a food chain to consumers. About 90% of the energy is lost at each step (as heat, movement and waste), so only ~10% passes on.',
    oneMove: {
      label: 'Use the 10% rule to explain short food chains',
      text: 'Because ~90% of energy is lost between trophic levels, there isn’t enough left to support many links — so food chains are usually only 4–5 organisms long. Food-chain arrows point the way the energy flows (eaten → eater).',
    },
    check: {
      prompt: 'Why are food chains rarely longer than four or five links?',
      modelAnswer: 'Because roughly 90% of the energy is lost at each trophic level (as heat, movement and waste), so after a few links there is too little energy left to support another organism.',
      needed: ['~90% energy lost per level', 'Too little energy left', '(hence short chains)'],
    },
    source: 'LC Biology syllabus — Unit 1: General Principles of Ecology',
    marksWeight: 8,
  },
  {
    id: 'bio-ecosystem-study',
    subjectId: 'biology', topicId: 'biology-0-4',
    subjectLabel: 'Biology', topicLabel: 'A Study of an Ecosystem', level: 'common',
    gist: 'This is the mandatory ecosystem study. Examiners expect a NAMED ecosystem you actually studied, named organisms in it, how you identified and counted them, and an adaptation. The marks are in the specifics, not general statements.',
    oneMove: {
      label: 'Bank a method + a named organism',
      text: 'Know two methods (e.g. a quadrat or line transect for plants; a pitfall trap or beating tray for animals) and exactly how you used one — plus one named organism and an adaptation it has to that habitat.',
    },
    check: {
      prompt: 'Name a method you could use to estimate the number of a plant species in an ecosystem, and outline how you used it.',
      modelAnswer: 'A quadrat. Place it at random points in the area, count the species inside each quadrat, repeat several times, find the average per quadrat, then scale up to the whole area.',
      needed: ['A named method (quadrat / transect)', 'Random / repeated sampling', 'Count then average / scale up'],
    },
    source: 'LC Biology syllabus — Unit 1: A Study of an Ecosystem (mandatory practical)',
    marksWeight: 8,
  },
  {
    id: 'bio-characteristics-of-life',
    subjectId: 'biology', topicId: 'biology-0-1',
    subjectLabel: 'Biology', topicLabel: 'The Characteristics of Life', level: 'common',
    gist: 'All living organisms carry out the same basic life processes: nutrition, excretion, response to stimuli, movement, growth, reproduction and respiration. These are what separate living things from non-living things.',
    oneMove: {
      label: 'Have the list ready as quick definitions',
      text: 'You can be asked to name characteristics OR define one: nutrition = obtaining food/energy; excretion = removing the waste products of metabolism; response = reacting to a stimulus. Short, precise definitions score.',
    },
    check: {
      prompt: 'List three characteristics of all living organisms.',
      modelAnswer: 'Any three of: nutrition, excretion, response, movement, growth, reproduction, respiration.',
      needed: ['Three valid characteristics', 'From the syllabus list', 'Correctly named'],
    },
    source: 'LC Biology syllabus — Unit 1: The Characteristics of Life',
    marksWeight: 6,
  },
  // ── English ──
  {
    id: 'eng-single-text-indepth',
    subjectId: 'english', topicId: 'english-6-0',
    subjectLabel: 'English', topicLabel: 'Single Text — in-depth study', level: 'common',
    gist: 'On Paper 2, Section I (60 marks) you answer ONE question on the single text you studied in depth (a novel or play). At Higher Level the question quotes a statement about the text — a character, a relationship, a theme or how it is written — and asks you to discuss it with close reference. (At Ordinary Level the same text is examined through shorter guided sub-tasks instead of one long essay.) Either way the answer is graded on Purpose, Coherence, Language and Mechanics (PCLM), not on a checklist of facts: you build a focused response and prove every point with apt reference or short quotation.',
    oneMove: {
      label: 'Answer BOTH halves of the quoted statement',
      text: 'The scheme tags the question\'s keywords with codes — e.g. on the 2024 Doerr question one code marked \'the tensions that emerge\' and a separate one marked the \'moral and ethical issues\' — and checks you addressed each. Retelling the plot or writing a pre-learned \'character essay\' covers only one half. Because the scheme states marks for Coherence or Language cannot exceed the marks for Purpose, a half-answered question drags the whole grade down.',
    },
    check: {
      prompt: 'A question quotes a statement and says \'Discuss this statement.\' What two things must your answer actually do to be in focus?',
      modelAnswer: 'Engage directly with the specific terms of the statement (every part of it, not just one), and develop each point with apt reference or short quotation from the text — building a discussion rather than retelling the story.',
      needed: ['Address the actual terms/both halves of the statement', 'Support points with apt textual reference/quotation', 'Discuss/argue rather than narrate the plot'],
    },
    source: 'LC English Paper 2 Section I, The Single Text (60 marks); Marking scheme 2024 HL (PCLM criteria; keyword codes T/M on the Doerr question; \'marks for C or L cannot exceed P\')',
    marksWeight: 60,
  },
  {
    id: 'eng-shakespeare-drama',
    subjectId: 'english', topicId: 'english-6-1',
    subjectLabel: 'English', topicLabel: 'Shakespearean drama', level: 'common',
    gist: 'Every candidate must engage with Shakespearean drama somewhere on Paper 2 — either as the Single Text (e.g. Hamlet or King Lear) in Section I, or with a Shakespeare play in the Comparative Study in Section II. You discuss character, relationships, themes and Shakespeare\'s dramatic techniques (soliloquy, imagery, structure, stagecraft), grounded in specific moments from the play rather than a whole-plot summary.',
    oneMove: {
      label: 'Lock in WHERE your Shakespeare answer lives before the exam',
      text: 'If a candidate makes no attempt at Shakespeare anywhere on Paper 2, the scheme imposes a penalty on the comparative answer (it disallows part of those marks). So if you skip Shakespeare in the Single Text you MUST cover it in the Comparative — and you can\'t reuse the same text across Sections I and II. Decide your route in advance, then anchor points in specific moments (a soliloquy, a confrontation) with brief quotation.',
    },
    check: {
      prompt: 'You decide to answer your Single Text question on a non-Shakespeare novel. What does the Paper 2 rubric then require of you?',
      modelAnswer: 'You must then engage with Shakespearean drama in the Comparative Study (Section II) instead — and you may not reuse the same text across both sections. If Shakespeare appears in neither, the scheme penalises the comparative answer.',
      needed: ['Shakespeare must be covered in Section I OR Section II', 'Cannot use the same text in both sections', 'No-attempt-at-Shakespeare triggers a penalty — plan which section carries it'],
    },
    source: 'LC English Paper 2; Marking scheme 2025 HL Appendix 4 (\'THERE IS NO ATTEMPT AT SHAKESPEARE\' penalty) + Section II rubric (\'may not answer on the text included in Section 1\')',
    marksWeight: 60,
  },
  {
    id: 'eng-comparative-theme-issue',
    subjectId: 'english', topicId: 'english-7-0',
    subjectLabel: 'English', topicLabel: 'Comparative — Theme or Issue', level: 'common',
    gist: 'The Comparative Study (Section II, 70 marks) reads 2-3 prescribed texts side by side through a chosen \'mode\' or lens. In Theme or Issue you trace one theme (e.g. conflict, loss, the search for freedom) across the texts. The question is usually a 30-mark part on ONE text plus a 40-mark part comparing two OTHER texts — or a single 70-mark comparison. You build the answer around key moments, not full plot summaries.',
    oneMove: {
      label: 'Compare across texts in the comparing parts — don\'t write them serially',
      text: 'In the 40-mark and single-70-mark parts the scheme separately credits \'evidence of effective comparison within the mode\' under Purpose. A \'serial\' answer — a block on Text A, then a separate block on Text B with no linking — forfeits those comparison marks even when each text is described well. Use connective signposting (\'similarly\', \'in contrast\', \'unlike\') so the marker can SEE the texts held against each other on the same theme.',
    },
    check: {
      prompt: 'Why does writing everything about Text A and then everything about Text B lose marks in the comparing part of a Theme or Issue question?',
      modelAnswer: 'Because in the comparing parts the scheme awards a distinct credit for effective comparison within the mode. A serial answer (block A, then block B) describes each text but never compares them, so it forfeits that comparison credit. You need to link the texts on the same theme — similarities and differences — throughout.',
      needed: ['Effective comparison within the mode is separately credited', 'Serial/block answers forfeit those comparison marks', 'Use linking language to compare on the same theme'],
    },
    source: 'LC English Paper 2 Section II, Comparative Study (Theme or Issue, 70 marks); Marking scheme 2024 HL (\'evidence of effective comparison within the mode\' under P, in the 40- and 70-mark parts)',
    marksWeight: 70,
  },
  {
    id: 'eng-comparative-cultural-context',
    subjectId: 'english', topicId: 'english-7-3',
    subjectLabel: 'English', topicLabel: 'Comparative — Cultural Context', level: 'common',
    gist: 'Cultural Context is a Comparative mode that examines the \'world\' of each text — the social structures, power, gender roles, class, money, religion and rules that shape how characters can live. You compare how that world enables or limits a character (e.g. how social position determines someone\'s freedom) across your prescribed texts, using key moments as evidence.',
    oneMove: {
      label: 'Show how the WORLD shapes the character — not just what happens to them',
      text: 'Cultural Context answers slide into plain story-telling or theme-spotting. The scheme lists \'evidence of understanding of the mode Cultural Context\' under Purpose, so you must keep the lens on the society and its rules (values, freedoms, power, conformity) and how they act on characters. \'In this world, a woman of her class could not...\' earns the mode marks; \'she was sad because...\' does not.',
    },
    check: {
      prompt: 'What is the difference between a strong Cultural Context point and one that just describes a sad event in the text?',
      modelAnswer: 'A strong point links the event to the world/society of the text — the social rules, class, gender expectations or power structures that caused or constrained it — showing understanding of the Cultural Context mode, rather than just narrating what happened to the character.',
      needed: ['Focus on the society/world\'s rules and structures', 'Show how the world shapes/limits the character', 'Understanding of the mode is part of the Purpose marks'],
    },
    source: 'LC English Paper 2 Section II, Comparative Study (Cultural Context, 70 marks); Marking scheme 2024 HL (\'evidence of understanding of the mode Cultural Context\' under P)',
    marksWeight: 70,
  },
  {
    id: 'eng-comparative-gvv',
    subjectId: 'english', topicId: 'english-7-4',
    subjectLabel: 'English', topicLabel: 'Comparative — General Vision & Viewpoint', level: 'common',
    gist: 'General Vision and Viewpoint (GVV) is the Comparative mode about the overall outlook a text leaves you with — broadly optimistic, bleak, or a mix — and what shapes that impression. You weigh things like the level of compassion and kindness shown, how characters respond to crises, and key moments such as the climax, opening and ending, then compare how bright or dark the vision feels across your texts.',
    oneMove: {
      label: 'GVV is YOUR reasoned reading — defend a position with key moments',
      text: 'Real questions have asked, for example, whether the climax of a text is \'over-influential\' in shaping a reader\'s perception of the general vision (2025), and how far the level of compassion and kindness shapes it (2023). Weak answers just label a text \'happy\' or \'sad\'; strong ones take a clear stance and prove it from specific key moments, and the scheme rewards \'evidence of critical literacy\' under Purpose. Commit to a viewpoint and earn it with evidence.',
    },
    check: {
      prompt: 'A question asks how far the climax of a text shapes its general vision and viewpoint. What does a top answer do beyond calling the text optimistic or bleak?',
      modelAnswer: 'It takes a clear, reasoned position on the vision and proves it from specific key moments — climax, opening and ending — weighing the evidence rather than just applying a one-word label, and comparing how the texts differ in the comparing parts.',
      needed: ['Take a clear reasoned stance on the vision', 'Support it with specific key moments (e.g. climax/opening/ending)', 'Argue/substantiate (critical literacy) rather than just label'],
    },
    source: 'LC English Paper 2 Section II, Comparative Study (General Vision and Viewpoint, 70 marks); Marking schemes 2023 HL (compassion and kindness) & 2025 HL (climax \'over-influential\')',
    marksWeight: 70,
  },
  {
    id: 'eng-prescribed-poetry-hl',
    subjectId: 'english', topicId: 'english-8-0',
    subjectLabel: 'English', topicLabel: 'Prescribed Poetry (Higher)', level: 'higher',
    gist: 'At Higher Level you study eight prescribed poets and answer ONE 50-mark essay on a single poet from memory (no poems are printed). The question quotes a statement about that poet — often about their imagery, themes, style or insights — and asks you to discuss it with reference to the poems you\'ve studied. You\'re expected to engage with the poetry itself (its imagery, language, suggestiveness), not deliver a biography.',
    oneMove: {
      label: 'Answer the actual statement with quotation — don\'t recite a pre-learned poet essay',
      text: 'The scheme codes the question\'s key terms — e.g. on the 2024 Yeats question one code marked \'powerful imagery\' and another marked the \'fascinating contradictions\' it explores — and checks you addressed each. A memorised general essay that ignores the specific statement loses Purpose marks. Weave accurate, brief quotation through your discussion: the scheme rewards \'effective use of accurate quotation and reference\' under Coherence.',
    },
    check: {
      prompt: 'A Higher Level poetry question quotes a statement about a poet\'s \'powerful imagery\' and the \'contradictions\' it explores. What must your essay do to stay in focus?',
      modelAnswer: 'It must engage with both terms of the statement — the imagery AND the contradictions it explores — discussing the poems themselves with accurate, apt quotation, rather than reciting a general pre-learned essay about the poet.',
      needed: ['Engage with each key term of the statement', 'Discuss the poems with accurate quotation/reference', 'Avoid a generic biography or pre-learned essay that ignores the wording'],
    },
    source: 'LC English Paper 2 Section III, Prescribed Poetry (Higher, eight poets, 50 marks); Marking scheme 2024 HL (keyword codes I/C on the Yeats question; \'effective use of accurate quotation and reference\' under C)',
    marksWeight: 50,
  },
  {
    id: 'eng-prescribed-poetry-ol',
    subjectId: 'english', topicId: 'english-8-1',
    subjectLabel: 'English', topicLabel: 'Prescribed Poetry (Ordinary)', level: 'ordinary',
    gist: 'At Ordinary Level the prescribed poem is PRINTED in front of you, and you answer a set of shorter, guided sub-questions on it (e.g. which word best describes its tone/mood, what the poet is saying in a given line, or why you\'d nominate or recommend it). The whole section is worth 50 marks and rewards a personal response backed by the poem on the page — you don\'t memorise poems or write one long essay as at Higher Level.',
    oneMove: {
      label: 'Quote a line for every point — the poem is right there',
      text: 'Because the poem is printed, the easiest marks come from pointing to specific words and lines, yet many answers give an opinion with no evidence. Each sub-question asks you to \'support your answer with reference to the poem\' — so every point needs a short quoted phrase plus a sentence on its effect. A general feeling about the poem with nothing quoted leaves marks on the table.',
    },
    check: {
      prompt: 'An Ordinary Level question asks which word best describes the poem\'s mood and to explain your choice. What does a full answer include?',
      modelAnswer: 'It names the mood, then quotes a specific word or line from the printed poem that creates that mood, and briefly explains how those words produce the feeling — opinion plus textual evidence plus effect.',
      needed: ['State the mood/tone clearly', 'Quote a specific word/line from the printed poem', 'Explain the effect of those words'],
    },
    source: 'LC English Paper 2 Section III, Prescribed Poetry (Ordinary, printed poem + guided sub-questions, 50 marks); Marking scheme 2024 OL (tone/mood, interpret-the-line and nominate-the-poem tasks; Combined Criteria)',
    marksWeight: 50,
  },
  {
    id: 'eng-composition',
    subjectId: 'english', topicId: 'english-9-1',
    subjectLabel: 'English', topicLabel: 'Composition (Paper 1)', level: 'common',
    gist: 'The Composition on Paper 1 (Section II) is worth 100 marks — the single biggest mark block in English. You choose ONE title and write in the genre it specifies: a short story, personal essay, discursive essay, speech, article, etc. It\'s graded on Purpose, Coherence, Language and Mechanics (PCLM), and \'Purpose\' explicitly includes understanding and sustaining the right genre.',
    oneMove: {
      label: 'Match the GENRE the title names, not just the topic',
      text: 'The scheme lists \'understanding of genre\' under Purpose — and it states marks for Coherence or Language cannot exceed the marks for Purpose. So a brilliant short story written when the title asked for a speech \'for or against the motion\' is capped: the genre conventions (argument, rhetoric, audience and one side of the motion for a speech; narrative shape and atmosphere for a story; a personal reflective voice for a personal essay) must match the title. Pick the title whose genre you can deliver, then hold that register the whole way through.',
    },
    check: {
      prompt: 'You write a vivid descriptive story, but the title asked for a speech for or against a motion. Why does this cost marks even if the writing is good?',
      modelAnswer: 'Because understanding of genre is part of the Purpose (P) criterion, and marks for Coherence and Language cannot exceed the marks for Purpose. A story doesn\'t use the speech conventions (argument, persuasion, rhetorical devices, audience awareness, one side of the motion), so Purpose is low and that ceiling pulls the whole answer down — regardless of how well it\'s written.',
      needed: ['Understanding of genre is part of Purpose', 'Marks for C and L cannot exceed the Purpose mark', 'Must use the conventions of the genre the title names (e.g. argument/audience for a speech)'],
    },
    source: 'LC English Paper 1 Section II, Composing (100 marks); Marking scheme 2024 HL (\'Understanding of genre\' under P; \'marks for C or L cannot exceed P\'; speech-for/against-the-motion title)',
    marksWeight: 100,
  },
  // ── Mathematics ──
  {
    id: 'maths-calculus-differentiation',
    subjectId: 'mathematics', topicId: 'mathematics-4-1',
    subjectLabel: 'Mathematics', topicLabel: 'Calculus', level: 'common',
    gist: 'Differentiation finds the slope of a curve at any point. The derivative f\'(x) tells you the rate of change. Set f\'(x) = 0 to find turning points (local max/min), and use the second derivative f\'\'(x) = 0 to find the point of inflection. On Paper 1 this shows up as: differentiate a function, find the tangent to a curve at a point, or find a max/min. The tangent at x = a uses slope m = f\'(a) and the point (a, f(a)) in y - y1 = m(x - x1).',
    oneMove: {
      label: 'Sub the x-value into f\'(x), not f(x), for slope',
      text: 'The recurring mark-loss on tangent and rate-of-change questions is using the original function for the slope. The slope at x = a is f\'(a) (the derivative); you find the point on the curve with f(a) (the original). Students differentiate correctly, then plug the x-value back into f(x) for the slope. The 2024 scheme credits Step 3 (finding f\'(a)) separately and requires it before giving the tangent-equation mark, so always show f\'(x) explicitly before substituting.',
    },
    check: {
      prompt: 'For f(x) = x^2 - 7x - 10, find the slope of the tangent at x = 3 and the y-coordinate of that point.',
      modelAnswer: 'f\'(x) = 2x - 7, so slope = f\'(3) = 2(3) - 7 = -1. The point is f(3) = 9 - 21 - 10 = -22, so (3, -22). Tangent: y + 22 = -1(x - 3).',
      needed: ['differentiate to get f\'(x) = 2x - 7', 'slope = f\'(3) = -1 (use the derivative)', 'point from f(3) = -22 (use original function)'],
    },
    source: 'LC Mathematics syllabus — Strand 5: Functions & Calculus; informed by Marking scheme 2024 (HL Paper 1, Q2/Q3 — tangent and point of inflection)',
    marksWeight: 30,
  },
  {
    id: 'maths-solving-equations-quadratic',
    subjectId: 'mathematics', topicId: 'mathematics-3-1',
    subjectLabel: 'Mathematics', topicLabel: 'Solving Equations', level: 'common',
    gist: 'Quadratics (ax^2 + bx + c = 0) solve by factorising or the quadratic formula x = (-b +/- root(b^2 - 4ac)) / 2a. Simultaneous equations (one linear and one quadratic, or three linear) solve by substituting one variable in terms of another. These dominate Paper 1\'s algebra question. When the answer is irrational, the formula is needed; when it factorises neatly, factors are faster.',
    oneMove: {
      label: 'Mind the sign on b in the formula, and substitute back',
      text: 'Two specific errors cost the most marks. First, in the quadratic formula students drop the minus on -b, especially when b is negative (-b becomes +5 when b = -5). Second, on simultaneous equations the chief mistake is compounded algebraic slips that go unnoticed. The fix examiners reward: substitute your final values back into the ORIGINAL equation to verify - it catches a wrong sign instantly and protects the solution marks.',
    },
    check: {
      prompt: 'Solve 3x^2 - 5x + 1 = 0, giving answers to 2 decimal places.',
      modelAnswer: 'a = 3, b = -5, c = 1. x = (5 +/- root(25 - 12)) / 6 = (5 +/- root(13)) / 6. So x = 1.43 or x = 0.23.',
      needed: ['correct a = 3, b = -5, c = 1 with -b = +5', 'fully substituted formula: root(b^2 - 4ac) = root(13)', 'both answers correctly evaluated and rounded: 1.43 and 0.23'],
    },
    source: 'LC Mathematics syllabus — Strand 4: Algebra; informed by Marking scheme 2024 (OL Paper 1, Q3(b))',
    marksWeight: 30,
  },
  {
    id: 'maths-complex-numbers-demoivre',
    subjectId: 'mathematics', topicId: 'mathematics-3-3',
    subjectLabel: 'Mathematics', topicLabel: 'Complex Numbers', level: 'higher',
    gist: 'A complex number a + bi can be written in polar form r(cos T + i sin T), where r = root(a^2 + b^2) is the modulus and T is the argument. De Moivre\'s theorem says [r(cos T + i sin T)]^n = r^n(cos nT + i sin nT) - the fast way to raise a complex number to a power. On Paper 1 (Higher) you convert to polar, apply de Moivre, then convert back to a + bi form.',
    oneMove: {
      label: 'Put the angle in the correct quadrant before using de Moivre',
      text: 'The biggest mark-loss is taking the argument straight from tan^-1(b/a) without checking the quadrant. For 1 - root(3)i (fourth quadrant) the calculator gives -60 degrees, which is correct, but for points in the second or third quadrant the calculator\'s value is wrong by 180 degrees and every later step inherits the error. The 2024 HL scheme states that candidates must engage with polar form or de Moivre to be awarded ANY credit, so always plot the point and fix the angle to its true quadrant first.',
    },
    check: {
      prompt: 'Evaluate (1 - root(3)i)^9 using de Moivre\'s theorem, and give the answer as a + bi.',
      modelAnswer: 'r = root(1 + 3) = 2; argument = -60 degrees (fourth quadrant). So [2(cos(-60) + i sin(-60))]^9 = 2^9(cos(-540) + i sin(-540)) = 512(-1 + 0i) = -512.',
      needed: ['r = 2', 'argument = -60 degrees (correct quadrant)', '2^9 = 512 and final answer -512 (i.e. -512 + 0i)'],
    },
    source: 'LC Mathematics syllabus — Strand 3: Number (Complex Numbers); informed by Marking scheme 2024 (HL Paper 1, Q2(b))',
    marksWeight: 15,
  },
  {
    id: 'maths-arithmetic-depreciation',
    subjectId: 'mathematics', topicId: 'mathematics-2-2',
    subjectLabel: 'Mathematics', topicLabel: 'Arithmetic', level: 'common',
    gist: 'Financial maths uses percentage change repeatedly. Depreciation (decreasing value) multiplies by (1 - rate) each year; appreciation/compound interest multiplies by (1 + rate). To reverse a percentage increase (find the original price before VAT or growth), you DIVIDE by the multiplier, not subtract the percentage. Arithmetic and geometric sequences also live here: arithmetic adds a common difference d, geometric multiplies by a common ratio r.',
    oneMove: {
      label: 'To undo an increase, divide - don\'t subtract the percent',
      text: 'The classic error: a value rose 12.5% to 52,875, so students subtract 12.5% of 52,875. That is wrong, because the 12.5% was of the smaller original. The original = 52,875 / 1.125. The same trap hits VAT-inclusive prices. For depreciation, multiply by 0.8 for a 20% drop (not subtract 20% of the new value each time). Always ask: is the percentage of the old value or the new one?',
    },
    check: {
      prompt: 'A machine worth 30,000 depreciates 20% per year. Find its value after 2 years. Separately, land rose 12.5% to 52,875 - find its original value.',
      modelAnswer: 'Machine: 30,000 x 0.8 = 24,000 after year 1; 24,000 x 0.8 = 19,200 after year 2. Land original: 52,875 / 1.125 = 47,000.',
      needed: ['multiply by 0.8 each year (not subtract from new value)', 'machine value = 19,200 after 2 years', 'reverse increase by dividing: 52,875 / 1.125 = 47,000'],
    },
    source: 'LC Mathematics syllabus — Strand 3: Number (Arithmetic & Sequences); informed by Marking scheme 2024 (OL Paper 1, Q1 — 30,000 machine depreciating 20%)',
    marksWeight: 20,
  },
  {
    id: 'maths-coord-geometry-circle',
    subjectId: 'mathematics', topicId: 'mathematics-1-1',
    subjectLabel: 'Mathematics', topicLabel: 'Co-ordinate Geometry', level: 'common',
    gist: 'A circle x^2 + y^2 + 2gx + 2fy + c = 0 has centre (-g, -f) and radius root(g^2 + f^2 - c). The form (x - h)^2 + (y - k)^2 = r^2 reads off the centre (h, k) and radius r directly. To find a circle through given points, use the fact that the centre is equidistant from all of them, or that the perpendicular bisector of a chord passes through the centre. The circle appears on Paper 2 nearly every year.',
    oneMove: {
      label: 'Centre is (-g, -f) - flip BOTH signs',
      text: 'The single most common mark-loss is the sign of the centre. From x^2 + y^2 + 4x - 6y + 5 = 0 students read the centre as (4, -6) or (-4, 6) instead of the correct (-2, 3): 2g = 4 so g = 2 and centre x = -g = -2; 2f = -6 so f = -3 and centre y = -f = 3. Halve the coefficient AND flip its sign for each. The radius also needs g^2 + f^2 - c (minus c), not plus.',
    },
    check: {
      prompt: 'State the centre and radius of the circle x^2 + y^2 + 4x - 6y + 5 = 0.',
      modelAnswer: '2g = 4 so g = 2; 2f = -6 so f = -3. Centre = (-g, -f) = (-2, 3). Radius = root(g^2 + f^2 - c) = root(4 + 9 - 5) = root(8) = 2root(2).',
      needed: ['g = 2, f = -3', 'centre = (-2, 3) (signs flipped)', 'radius = root(4 + 9 - 5) = 2root(2)'],
    },
    source: 'LC Mathematics syllabus — Strand 2: Geometry & Trigonometry (Co-ordinate Geometry); informed by Marking scheme 2024 (HL Paper 2, Q5)',
    marksWeight: 20,
  },
  {
    id: 'maths-trigonometry-sine-cosine-rule',
    subjectId: 'mathematics', topicId: 'mathematics-1-2',
    subjectLabel: 'Mathematics', topicLabel: 'Trigonometry', level: 'common',
    gist: 'In any triangle: the Sine Rule a/sin A = b/sin B relates sides to opposite angles; the Cosine Rule a^2 = b^2 + c^2 - 2bc cos A handles two sides and the included angle (or all three sides). The area of a triangle is (1/2)ab sin C. Use the Cosine Rule when no angle-opposite-side pair is known; otherwise the Sine Rule. These appear on Paper 2 nearly every year.',
    oneMove: {
      label: 'Sine Rule for an angle? Check the second (obtuse) solution',
      text: 'When you use the Sine Rule to find an ANGLE, sin gives two answers between 0 and 180 degrees: the acute value T and its supplement 180 - T. Students give only the calculator\'s acute angle and lose the mark when both are valid (the ambiguous case, e.g. theta = 47 or 133 degrees). The 2024 HL scheme explicitly awards High Partial Credit for only ONE correct angle. Also confirm your calculator is in degree mode first - schemes flag \'incorrect calculator mode\' as a recurring error that can cost the answer marks.',
    },
    check: {
      prompt: 'In triangle KLM, sin(theta)/45 = sin(25)/15root(3). Find the two possible values of theta in degrees (0 < theta < 180).',
      modelAnswer: 'sin(theta) = 45 x sin(25) / (15root(3)) = 0.732. theta = 47 degrees (acute) or 180 - 47 = 133 degrees. Both are valid for 0 < theta < 180.',
      needed: ['sin(theta) = 0.732', 'first value theta = 47 degrees', 'supplement theta = 133 degrees'],
    },
    source: 'LC Mathematics syllabus — Strand 2: Geometry & Trigonometry; informed by Marking scheme 2024 (HL Paper 2, Q3)',
    marksWeight: 20,
  },
  {
    id: 'maths-probability-expected-value',
    subjectId: 'mathematics', topicId: 'mathematics-0-1',
    subjectLabel: 'Mathematics', topicLabel: 'Concepts of Probability', level: 'common',
    gist: 'Expected value is the long-run average outcome: multiply each possible value by its probability and add them, E(X) = sum of (value x probability). A game is fair when the expected return equals the cost to play (equivalently, expected net gain = 0). Other staples: mutually exclusive events have P(A and B) = 0 so P(A or B) = P(A) + P(B); independent events have P(A and B) = P(A) x P(B). Probability appears on Paper 2 nearly every year.',
    oneMove: {
      label: 'Compare the expected return to the cost before calling a game \'fair\'',
      text: 'On fair-game questions the recurring error is ignoring the entry cost. A game is fair when the expected value of the amount received equals the cost to play (so expected NET gain is 0) - not simply when an expected value equals 0. The 2023 OL scheme requires both a conclusion AND a justification comparing the expected outcome to the amount paid; either one missing drops you to Full Credit -1. Also watch \'mutually exclusive\' (P together = 0) versus \'independent\' (multiply) - questions deliberately test the confusion.',
    },
    check: {
      prompt: 'A game costs 10 to play. The amount you receive is 0 (prob 0.30), 2 (0.40), x-10 (0.28), or x (0.02). The game is fair. Find x.',
      modelAnswer: 'E(received) = 0(0.30) + 2(0.40) + (x-10)(0.28) + x(0.02) = 0.8 + 0.28x - 2.8 + 0.02x = 0.3x - 2. Fair means E(received) = cost = 10, so 0.3x - 2 = 10, giving 0.3x = 12, x = 40.',
      needed: ['E(received) = 0.3x - 2', 'fair means E(received) = cost to play (10)', 'x = 40'],
    },
    source: 'LC Mathematics syllabus — Strand 1: Statistics & Probability; informed by Marking scheme 2023 (OL Paper 2 — fair-game conclusion-and-justification rule)',
    marksWeight: 20,
  },
  {
    id: 'maths-volume-sphere-cone',
    subjectId: 'mathematics', topicId: 'mathematics-2-3',
    subjectLabel: 'Mathematics', topicLabel: 'Length, Area & Volume', level: 'common',
    gist: 'Volume questions on Paper 2 combine standard solids: sphere (4/3)pi r^3, cone (1/3)pi r^2 h, cylinder pi r^2 h. Composite-solid problems set the total volume equal to the sum (or difference) of parts - for example, melting a sphere and recasting it as cones means equal volumes. All the formulas are in the Formulae and Tables booklet, so the marks are for choosing the right one and substituting correctly. This topic appears on Paper 2 most years.',
    oneMove: {
      label: 'Use the radius, not the diameter, in the formula',
      text: 'The most common volume mark-loss is substituting the diameter where the formula needs the radius (every formula uses r, but questions love to give the diameter). Halve it first. The second trap is mixing units mid-problem (cm with m), which corrupts the number. Note: marking schemes generally state \'Accept correct answer without units\' on volume/area parts, so missing cm^3 usually won\'t cost a mark - but incorrect ROUNDING will (Full Credit -1). Halve to the radius, keep units consistent, and round correctly.',
    },
    check: {
      prompt: 'A solid metal sphere of radius 6 cm is melted and recast into cones of radius 2 cm and height 9 cm. How many full cones are made?',
      modelAnswer: 'Sphere volume = (4/3)pi(6)^3 = 288pi cm^3. Cone volume = (1/3)pi(2)^2(9) = 12pi cm^3. Number = 288pi / 12pi = 24 cones.',
      needed: ['sphere = (4/3)pi(6)^3 = 288pi', 'cone = (1/3)pi(2)^2(9) = 12pi', '288/12 = 24 full cones'],
    },
    source: 'LC Mathematics syllabus — Strand 2: Geometry & Trigonometry (Length, Area & Volume); informed by Marking scheme 2024 (OL Paper 2 — units/rounding rule)',
    marksWeight: 15,
  },
  // ── Geography ──
  {
    id: 'geo-tectonic-cycle',
    subjectId: 'geography', topicId: 'geography-0-0',
    subjectLabel: 'Geography', topicLabel: 'The Tectonic Cycle', level: 'common',
    gist: 'The Earth\'s crust is broken into plates that move on the semi-molten layer of the upper mantle below, dragged by convection currents. Where plates pull apart (constructive), push together (destructive) or slide past each other (transform), you get earthquakes, volcanoes and fold mountains. Because these events cluster along plate boundaries, plate-tectonic theory explains why they are NOT scattered randomly around the globe.',
    oneMove: {
      label: 'Link the hazard to the boundary, don\'t just describe it',
      text: 'The exam wants you to USE plate tectonics to explain the global DISTRIBUTION (e.g. why volcanoes ring the Pacific). The 2023 scheme caps you at a maximum of 2 SRPs if there is no reference to how plate tectonics explains the distribution of volcanoes, earthquakes or fold mountains. So after every fact, add \'because at this plate boundary...\' and tie it to the pattern.',
    },
    check: {
      prompt: 'Explain why most of the world\'s volcanoes and earthquakes occur along the edges of the Pacific Ocean (the Ring of Fire).',
      modelAnswer: 'The Pacific Plate meets several other plates at destructive (subduction) boundaries around its rim. As the dense oceanic plate sinks and melts, magma rises to form volcanoes, and the locked plates build up and release stress, causing earthquakes. Because these processes only happen along these boundaries, the volcanoes and quakes form a ring rather than being spread evenly. A labelled diagram of a subduction zone earns a further mark.',
      needed: ['Named plate boundary type (destructive / subduction)', 'Mechanism: oceanic plate sinks/melts so magma rises / stress builds and releases', 'Explicit link to the distribution pattern (clustered at boundaries, not random)', 'Worth a mark: a relevant LABELLED diagram (unlabelled = 0)'],
    },
    source: 'LC Geography — Core Unit 1: Patterns and Processes in the Physical Environment (Plate Tectonics); marking criteria from 2023 HL Q3B \'The Tectonic Cycle\' (30m: 2+2 example, then 13 SRPs; max 2 SRPs with no link to global distribution).',
    marksWeight: 30,
  },
  {
    id: 'geo-rock-cycle-human-interaction',
    subjectId: 'geography', topicId: 'geography-0-1',
    subjectLabel: 'Geography', topicLabel: 'The Rock Cycle', level: 'common',
    gist: 'Rocks are continuously recycled: igneous rock forms when magma/lava cools, weathering and erosion break rock into sediment that compacts into sedimentary rock, and heat plus pressure change rock into metamorphic rock, which can melt back to magma. Humans interact with this cycle through mining, extraction of building materials, oil/gas exploitation, and geothermal energy production — a high-value exam theme.',
    oneMove: {
      label: 'Name the interaction AND a place, then examine the impact',
      text: 'The \'human interaction with the rock cycle\' question wants a named interaction (e.g. a quarry, oil field or geothermal plant), a named example, and examination of how the activity uses or alters the cycle. You get 1 SRP for the example and 1 SRP for the interaction identified; every further interaction must be examined, not just listed. Note the question is NOT tied to Ireland — any valid location works. Process: name the interaction, name where, then explain the impact.',
    },
    check: {
      prompt: 'Examine ONE way humans interact with the rock cycle (mining, building materials, oil/gas, or geothermal), using a named example.',
      modelAnswer: 'Humans extract building materials by quarrying limestone (e.g. at a large limestone quarry such as those near the Burren/Co. Clare). This removes sedimentary rock that formed over millions of years far faster than the cycle replaces it, scarring the landscape, producing dust and noise, but supplying cement and aggregate for construction. The interaction is identified and the example given (2 SRPs), then each further point examines the impact.',
      needed: ['A named human interaction (mining / building materials / oil-gas / geothermal) identified', 'A named example or location (need NOT be in Ireland)', 'Examination of the impact or how the activity uses/alters the rock cycle (further points must be examined, not listed)'],
    },
    source: 'LC Geography — Core Unit 1: Patterns and Processes in the Physical Environment (Human Interaction with the Rock Cycle); marking criteria from 2023 HL Q3C \'Human Interaction with the Rock Cycle\' (30m: 15 SRPs; 1 SRP example + 1 SRP interaction, all further interactions require examination; question not tied to Ireland).',
    marksWeight: 30,
  },
  {
    id: 'geo-surface-processes-formation',
    subjectId: 'geography', topicId: 'geography-0-4',
    subjectLabel: 'Geography', topicLabel: 'Landform Development: Surface Processes', level: 'common',
    gist: 'The land surface is shaped by weathering (breaking rock in place), mass movement (rock and soil moving downslope under gravity, from slow soil creep to fast landslides) and erosion by rivers, the sea and ice. These processes build recognisable landforms — a river V-shaped valley and waterfall, a coastal sea stack, a glacial corrie. The exam asks you to explain the ROLE of erosion in FORMING a chosen landform.',
    oneMove: {
      label: 'Explain FORMATION, never just describe the landform',
      text: 'If the question asks about the role of erosion in forming a landform, trace the process stage by stage. The scheme awards only a maximum of 2 SRPs if the answer is just a description of the landform with no reference to its formation, and explaining DEPOSITION when EROSION was asked scores zero. Name the erosion process (e.g. hydraulic action, abrasion), say what it does at each stage, and add a labelled diagram.',
    },
    check: {
      prompt: 'Explain the role of the processes of erosion in forming ONE river OR coastal OR glacial landform you have studied.',
      modelAnswer: 'A waterfall forms where a river crosses a band of hard rock lying over softer rock. Hydraulic action and abrasion erode the soft rock faster, undercutting the hard rock. The unsupported hard rock collapses, a plunge pool deepens at the base, and the waterfall slowly retreats upstream leaving a gorge. (A coastal sea stack formed by hydraulic action and abrasion of a headland, or a glacial corrie, is equally valid.) A labelled diagram earns a further mark.',
      needed: ['Landform named (2 marks) + a process of erosion identified, e.g. hydraulic action / abrasion (2 marks)', 'Step-by-step formation, not just a description (mere description capped at 2 SRPs)', 'A named example/location, and ideally a labelled diagram (deposition explained instead of erosion = 0)'],
    },
    source: 'LC Geography — Core Unit 1: Patterns and Processes in the Physical Environment (Surface Processes / Landform Development); marking criteria from 2024 HL Q2B(i), \'role of the processes of erosion on the formation of one fluvial/coastal/glacial landform\' (30m; max 2 SRPs for mere description with no formation; deposition = 0; question not tied to Ireland).',
    marksWeight: 30,
  },
  {
    id: 'geo-concept-of-a-region',
    subjectId: 'geography', topicId: 'geography-1-0',
    subjectLabel: 'Geography', topicLabel: 'The Concept of a Region', level: 'common',
    gist: 'A region is an area of the Earth\'s surface that is broadly uniform in some defining feature, marked off from its surroundings. Regions are defined in different ways: physical/geomorphological (the Burren\'s limestone), climatic (a hot desert), administrative (a county), socio-economic (core vs peripheral), cultural, urban, or by how they function. The same place can belong to several region types at once.',
    oneMove: {
      label: 'Tie every point to the named criterion AND a real example',
      text: 'When asked how climate or geomorphology defines regions, you score an example for 2 marks, then 1 SRP for a specific reference to climate or geomorphology, with all further examples requiring examination. So link each fact explicitly to that criterion in a named example (e.g. \'the Burren is a karst region because...\'); a vague list of region types with no example and no link to the criterion earns almost nothing.',
    },
    check: {
      prompt: 'Examine how geomorphology (landscape/rock type) can be used to define a region, with reference to a named example.',
      modelAnswer: 'A geomorphological region is defined by a distinctive landscape, rock type or relief. The Burren in Co. Clare is a karst region: it is made of carboniferous limestone weathered by carbonation into bare grey pavement, with features like clints, grikes and underground caves. This uniform limestone landscape marks it off clearly from the surrounding land, so geomorphology defines its boundary. A labelled sketch map earns a further mark.',
      needed: ['A named example, e.g. the Burren (worth 2 marks)', 'A specific reference to the defining criterion — geomorphology: rock type / relief / landscape (1 SRP)', 'Examination of how that criterion makes the area uniform and marks its boundary (further examples must be examined)'],
    },
    source: 'LC Geography — Core Unit 2: Regional Geography (The Concept of a Region); marking criteria from 2025 HL Q5C \'Concept of a Region\' (climate OR geomorphology; 30m: 2 marks example + 14 SRPs; 1 SRP for specific reference to climate/geomorphology). The 2024 HL Q4B variant asks the same with culture/climate.',
    marksWeight: 30,
  },
  {
    id: 'geo-region-dynamics-core-periphery',
    subjectId: 'geography', topicId: 'geography-1-1',
    subjectLabel: 'Geography', topicLabel: 'The Dynamics of Regions', level: 'common',
    gist: 'Regions are not static — they change over time and differ in wealth. Core regions (e.g. the Greater Dublin Area, the Paris Basin) have high population density, strong infrastructure, services and jobs across all sectors. Peripheral regions (e.g. the West of Ireland, the Italian Mezzogiorno) are further from the centre, more rural, more dependent on primary activity, and often lose people through out-migration.',
    oneMove: {
      label: 'Name BOTH a core and a peripheral region, then contrast',
      text: 'The \'core vs peripheral\' question gives 1 SRP for naming a core region, 1 SRP for naming a peripheral region, and 2 SRPs for examples of economic activity. The scheme caps you at a maximum of 2 SRPs for mere description of economic activity in either type that doesn\'t actually contrast them. Use: in the core X happens, whereas in the periphery Y happens, because...',
    },
    check: {
      prompt: 'How does economic activity in a core region differ from a peripheral region? Use one named example of each.',
      modelAnswer: 'In a core region like the Greater Dublin Area, activity is dominated by high-value tertiary and quaternary jobs — finance and tech (the IFSC, multinational HQs) — supported by dense infrastructure, which draws in workers. In a peripheral region like the West of Ireland (e.g. Co. Mayo / Connacht), activity leans on primary work such as sheep farming and on tourism, jobs are fewer and lower paid, and young people out-migrate to the core. The contrast and reason for it are stated explicitly.',
      needed: ['A named core region with its dominant activity (tertiary/quaternary) — 1 SRP for the named region', 'A named peripheral region with its dominant activity (primary) — 1 SRP for the named region', 'Examples of economic activity and a clear contrast/reason (mere description of either, with no contrast, capped at 2 SRPs)'],
    },
    source: 'LC Geography — Core Unit 2: Regional Geography (Dynamics of Regions / Socio-economic regions); marking criteria from 2024 HL Q6C \'Socio-Economic Regions\' (30m: 15 SRPs; 1 SRP each for a named core and peripheral region, 2 SRPs for examples of activity; max 2 SRPs for mere description).',
    marksWeight: 30,
  },
  {
    id: 'geo-gi-posing-the-problem',
    subjectId: 'geography', topicId: 'geography-2-1',
    subjectLabel: 'Geography', topicLabel: 'Investigation: Posing the Problem', level: 'common',
    gist: 'The Geographical Investigation (GI) is a fieldwork report worth 100 marks (20% of the LC Geography grade), completed before the written exam. It starts by posing a clear problem: the Introduction states the aims (what exactly you set out to find out, 5 marks) and the Planning sets out what information you needed, your methods and your preparation (5 marks). It must be a genuine, location-specific question you can actually answer with fieldwork.',
    oneMove: {
      label: 'Make aims specific and qualified, never vague',
      text: 'The scheme requires that aims be specific and qualified — a woolly aim like \'to study the river\' wins few marks. Name the place, the feature and what you\'ll measure (e.g. \'to investigate how the width and velocity of a named river change from source toward mouth\'). In Planning, every statement must be qualified (how/where/why) or it earns nothing, and work done solely by the teacher scores 0.',
    },
    check: {
      prompt: 'Write a strong aim for a geographical investigation, and explain why it scores better than a vague one.',
      modelAnswer: 'Strong aim: \'To investigate how the width and velocity of a named local river increase downstream between two named sample sites.\' It scores well because it is specific (a named river, named sites) and qualified (states exactly what is measured and the expected relationship), so it can be tested by fieldwork. A vague aim like \'to study rivers\' gives the examiner nothing measurable to credit.',
      needed: ['A specific aim naming a place/feature', 'A measurable variable (what you\'ll record)', 'The aim is specific AND qualified (testable), beating a vague aim with nothing creditable'],
    },
    source: 'LC Geography — Geographical Investigation & Skills (Posing the Problem: Introduction/Aims + Planning); GI marking criteria appended to the marking schemes: Introduction 5 marks (aims must be specific and qualified), Planning 5 marks (all statements must be qualified how/where/why; teacher-only work = 0).',
    marksWeight: 10,
  },
  {
    id: 'geo-gi-collection-of-data',
    subjectId: 'geography', topicId: 'geography-2-3',
    subjectLabel: 'Geography', topicLabel: 'Investigation: Collection of Data', level: 'common',
    gist: 'Gathering of Data is the single biggest part of the Geographical Investigation, worth 40 marks — two methods or tasks at 18 marks each, plus coherence. You report HOW you actually collected your information — e.g. measuring river width with a tape, timing a float for velocity, or doing a land-use survey. It must read as an activity-based account of what you carried out, tied to your aims.',
    oneMove: {
      label: 'Qualify every step with how/where — not \'I observed\'',
      text: 'The scheme states that simple statements such as \'I observed the features\' or \'I recorded the results\' are NOT sufficient on their own. Each point must be activity-based and qualified — what equipment you used, and exactly how and where you used it. \'I measured the river\'s width by stretching a tape between both banks at site 1\' scores; \'I measured the river\' does not. No marks for results in this section.',
    },
    check: {
      prompt: 'Describe how you would collect data on river width in the field, in a way that would actually earn marks.',
      modelAnswer: 'At each chosen site I stretched a measuring tape across the river from the waterline on one bank to the waterline on the opposite bank, held it taut and level just above the surface, and read the width in metres. I recorded the figure in a prepared results table and repeated this at three sites downstream so the readings were comparable. The equipment, the exact method, and the location make it a creditable activity tied to the aim.',
      needed: ['A named method/equipment (e.g. measuring tape stretched across the channel)', 'Qualified detail — exactly how and where it was done (a bare statement like \'I measured the river\' earns nothing)', 'Activity tied to the stated aim (results themselves are credited in a later section, not here)'],
    },
    source: 'LC Geography — Geographical Investigation & Skills (Gathering/Collection of Data); GI marking criteria appended to the marking schemes: Gathering of Data 40 marks (two methods/tasks @ 18 marks; must be activity-based and qualified; \'I observed/recorded\' alone not sufficient; no marks for results in this section).',
    marksWeight: 40,
  },
  {
    id: 'geo-economic-development-gnp-hdi',
    subjectId: 'geography', topicId: 'geography-3-0',
    subjectLabel: 'Geography', topicLabel: 'Economic Development', level: 'common',
    gist: 'Economic development means improving the wealth and quality of life in a country, and it is measured in different ways. GNP (Gross National Product) is a mainly economic measure — the total value of goods and services produced by a country\'s people, usually per capita — but it ignores how wealth is shared or how people actually live. The HDI (Human Development Index) is broader, combining income with life expectancy and education into a single index, giving a fuller picture of human wellbeing.',
    oneMove: {
      label: 'Discuss BOTH GNP and HDI — one alone is half-capped',
      text: 'The \'measuring development\' question gives 2 marks for reference to GNP as a measure, 2 marks for HDI as a measure, and 2 marks for a named example. The scheme caps you at a maximum of 6 SRPs (out of 13 — roughly half) if you discuss only GNP, and the same if you discuss only HDI. Balance both, and explain WHY HDI is fuller (it adds health and education) rather than just defining each.',
    },
    check: {
      prompt: 'Discuss how GNP and the HDI are each used to measure economic development, and how they differ. Refer to an example.',
      modelAnswer: 'GNP measures the total value of goods and services produced by a country\'s people, usually given per capita, so a high GNP suggests a wealthy economy (e.g. a high-income country). The HDI combines income with life expectancy and average years of schooling into a single index from 0 to 1. HDI is considered a fuller measure because two countries with a similar GNP (e.g. an oil-exporting state versus a strong-welfare state) can have very different health and education, which only HDI captures.',
      needed: ['Reference to GNP as a measure — value of output, usually per person (2 marks)', 'Reference to HDI as a measure — combines income + life expectancy + education (2 marks)', 'A named example (2 marks) and a stated difference (HDI is broader / captures quality of life)'],
    },
    source: 'LC Geography — Elective (Economic Development / Measuring Development); marking criteria from 2024 HL Q7B \'Economic Development\' (30m: 2+2 GNP/HDI, 2 example, 12 SRPs; max 6 SRPs if only GNP discussed, max 6 if only HDI).',
    marksWeight: 30,
  },
  {
    id: 'geo-population-change-fertility-mortality',
    subjectId: 'geography', topicId: 'geography-4-0',
    subjectLabel: 'Geography', topicLabel: 'Population: Change Over Time and Space', level: 'common',
    gist: 'Population changes through births (fertility), deaths (mortality) and migration. Natural change = births minus deaths. The Demographic Transition Model shows how, as a country develops, death rates fall first (better food and medicine) and birth rates fall later, so population grows fast in between then levels off. Changing fertility and mortality reshape the population pyramid — fewer young, more elderly.',
    oneMove: {
      label: 'Show the rates CHANGING and link to structure',
      text: 'This question rewards the impact of CHANGING fertility and mortality rates on population STRUCTURE. The scheme caps you at a maximum of 2 SRPs if your answer does not deal with \'changing\' rates, and again at a maximum of 2 SRPs if you examine the rates but never link them to population structure. Always say: as fertility fell, the base of the pyramid narrowed; as mortality fell, the top widened (ageing).',
    },
    check: {
      prompt: 'Examine how CHANGING fertility and mortality rates impact on a country\'s population structure, with reference to an example.',
      modelAnswer: 'As fertility falls, fewer babies are born each year, so the base of the population pyramid (the 0-14 age group) narrows. As mortality falls, people live longer, so the top of the pyramid widens and the proportion of elderly grows — the population ages. Together this shifts a country from a wide-based \'pyramid\' toward a more column-like structure, as seen in developed countries like Italy or Japan, raising the dependency ratio.',
      needed: ['Impact of CHANGING fertility identified — narrower base / fewer young (2 marks)', 'Impact of CHANGING mortality identified — wider top / ageing population (2 marks)', 'Explicit link to population structure/pyramid plus a named example (failing to address \'changing\' rates, or omitting the structure link, caps the answer at 2 SRPs)'],
    },
    source: 'LC Geography — Elective (Population Dynamics / Change over Time and Space); marking criteria from 2024 HL Q10C \'Dynamics of Population\' (30m: 2+2 changing fertility/mortality, 2 example, 12 SRPs; max 2 SRPs if not \'changing\', max 2 SRPs if no link to structure).',
    marksWeight: 30,
  },
  {
    id: 'geo-settlement-site-situation-function',
    subjectId: 'geography', topicId: 'geography-4-3',
    subjectLabel: 'Geography', topicLabel: 'Settlement: Site, Situation and Function', level: 'common',
    gist: 'Site is the actual land a settlement is built on (e.g. flat, dry, defensible land beside fresh water). Situation is the settlement\'s position relative to its surroundings (routeways, other towns, a coast). Function is what the settlement does (port, market, route centre, tourism). Towns like Bantry grew where a good site met a good situation, and the exam asks you to explain, using map or photo evidence, why a town developed where it did.',
    oneMove: {
      label: 'Back each reason with OS-map/photo evidence',
      text: 'When asked why a town developed at its location, the scheme marks each reason as: reason stated (2), OS-map or aerial-photo evidence (2), then explanation. If there is no map/photo reference (or it is incorrect) you lose the 2 evidence marks — you can still get the reason and explanation, but not the evidence. So quote a grid reference, a river, a bridging point or a road junction; don\'t just assert \'good location\'. Use map OR photo, not both.',
    },
    check: {
      prompt: 'Give two reasons, with the kind of evidence the exam wants, why a town developed at its present location.',
      modelAnswer: '1. A bridging-point/route reason: it grew where a road crosses the river on the OS map at a named grid reference, because the lowest bridge forced routes to converge there, encouraging trade. 2. A site reason: it sits on flat, dry land beside the river shown on the map, giving fresh water and easy building land. Each reason is stated (2 marks), evidenced from the map (2 marks), then explained.',
      needed: ['A valid reason — e.g. bridging point, route focus, water supply, flat/dry land (2 marks)', 'Specific OS-map or aerial-photo evidence: grid ref / named feature (2 marks; missing or wrong reference loses these 2 marks)', 'An explanation of why that factor encouraged the town to develop there'],
    },
    source: 'LC Geography — Elective (Settlement: Site, Situation, Function); marking criteria from 2024 HL Q10B \'Urban Settlement\' (Bantry: three reasons @ 10 marks each — reason stated 2 + map/photo evidence 2 + explanation; no/incorrect map reference loses the evidence marks). Related OS-map settlement question: 2025 HL Q12B \'Settlement Distribution\'.',
    marksWeight: 30,
  },
  {
    id: 'bio-photosynthesis-absorption',
    subjectId: 'biology', topicId: 'biology-1-1',
    subjectLabel: 'Biology', topicLabel: 'Cell Metabolism', level: 'higher',
    gist: 'Photosynthesis happens in the chloroplast, where the pigment chlorophyll absorbs light energy — but not all colours equally. Chlorophyll a and b absorb mainly in the blue/violet and red parts of the spectrum and absorb green light least, so green is reflected (which is why leaves look green). The absorbed energy excites electrons that drive the light stage.',
    oneMove: {
      label: 'Read the peaks — and remember green is REFLECTED, not absorbed',
      text: 'On an absorption-spectrum graph the colour absorbed “most” is wherever the curve PEAKS (blue/violet and red). The dip across the green/yellow band means that light is reflected, not used — the classic exam point that explains why plants are green.',
    },
    check: {
      prompt: 'Using the graph above, which colour of light does chlorophyll b absorb most strongly, and what happens to green light?',
      modelAnswer: 'Chlorophyll b absorbs most strongly in the blue (its tallest peak), with a second peak in the red. Green light is barely absorbed — it is reflected/transmitted, which is why leaves appear green.',
      needed: ['Blue (chlorophyll b’s main peak)', 'Green light is reflected / not absorbed', 'Why leaves appear green'],
    },
    source: 'LC Biology syllabus — Unit 2: Cell Metabolism (Photosynthesis)',
    marksWeight: 9,
    figure: {
      src: '/exam-figures/biology/bio-2023-hl-photosynthesis-absorption.png',
      alt: 'Graph of light absorption against colour of light (violet to red) for chlorophyll a (dotted) and chlorophyll b (solid): peaks in blue/violet and red, a dip across green and yellow.',
      source: 'SEC Leaving Certificate Biology 2023 Higher Level, Q7 — © State Examinations Commission',
    },
  },
  {
    id: 'eng-comprehending-gravel-heart',
    subjectId: 'english', topicId: 'english-10-0',
    subjectLabel: 'English', topicLabel: 'Reading & comprehension', level: 'higher',
    gist: 'Question A on Paper 1 (50 marks) is close reading, not opinion. You are asked for insights (into a character or idea), your own developed response to a view, and the writer’s style/language features. Marks live in PRECISE points that are anchored to the text — make the point, quote or reference the line that proves it, then explain its effect.',
    oneMove: {
      label: 'Anchor every point to the text — quote, then explain the effect',
      text: 'The single biggest comprehension mark-loss is asserting without evidence. For each point: name it, give a short quotation or reference from the passage, then say what it shows or does. A point with no textual anchor is barely rewarded; three anchored points beat six floating assertions.',
    },
    check: {
      prompt: 'Read the passage. Give two insights into Salim’s character, each supported by a reference to the text.',
      modelAnswer: 'e.g. (1) He is bookish / drawn to literature — he had "worked my way through most of my father’s books" and thought of himself as "a future student of literature". (2) He is passive / lacks the courage to assert himself — he "did not have the courage" to tell Uncle Amir he would have preferred to study literature. (Also creditable: observant — he notices "the amplitude of space and the expensive furnishings".)',
      needed: ['One insight into Salim (e.g. bookish / loves literature)', 'A second, different insight (e.g. passive / lacks courage)', 'A short quotation or reference from the passage for each'],
    },
    source: 'LC English Paper 1 — Section I Comprehending, Question A (close-reading technique)',
    marksWeight: 15,
    passage: {
      text: 'TEXT 1 – BETWEEN TWO WORLDS: VILLAGE AND CITY This text is based on an edited extract from Gravel Heart, a novel by Abdulrazak Gurnah, 2021 Nobel Prize winner for literature. In this extract Salim, from a small island village in Zanzibar, comes to stay with his uncle in London to further his education. He doesn’t know how to belong in this strange city and feels cut off from the world he has left behind.\n\nWhen I went to live with Uncle Amir in London, it was his wish that I should study for a career in business. “In your circumstances, it is the perfect option and it will allow you to work anywhere in the world. Make money! Think of the outcomes: accountancy, management, consultancy, and at the end of it all plenty of money in the bank.”\n\nIt would have sounded cowardly to tell him that I should have preferred to study literature. By the time I left for London, I had worked my way through most of my father’s books, had made good progress through the school library shelves, had borrowed and exchanged books with friends, and I thought of myself as someone with proven credentials as a future student of literature. When I came to London I realised how unimpressive my credentials were, how much there was to read, how much there was to work through. Uncle Amir had different plans for me and I did not have the courage to say anything about how I might have preferred to proceed with my life.\n\nhad bought new just before I left, looked cheap and flimsy and tiny on that rug, like a cardboard box. I sat on the bed when I was left alone, looking around the room, gazing out of the darkened window then at the clean bare desk with its angled lamp, and I smiled. That is the desk where I will sit and write to Mama about the wonders I encounter and I won’t allow the thought of my ignorance to discourage me. I allowed this resolution to overcome the slight feeling of panic I sensed at the edge of my mind. What was I doing here?\n\nI was moved by the pleasure they took in my arrival. They both beamed smiles at me and Auntie Asha spoke to me as if I was a diffident younger brother who needed to be brought out of himself. I was too flustered to take in everything immediately, but I noticed the amplitude of space and the expensive furnishings. Auntie Asha took me upstairs to show me my room which was luxurious: a large bed, a dark wardrobe the depth of a coffin, a wide desk, a chest of drawers, a bookshelf, a comfortable reading chair, and still enough space in the middle for a rug. A whole family lived in a room of this size where I had come from. My suitcase, which I\n\nDear Mama, I hope you are well. It is now October and I started college last week. London is full of people from everywhere in the world. I just had not expected to see that, Indians, Arabs, Africans, Chinese, and I don’t know where all the European people come from but they are not all English. When a double-decker bus goes by and you see the faces through the window, it is like a glimpse of a page in an illustrated children’s encyclopaedia under the title People of the World.',
      source: 'SEC Leaving Certificate English 2023 Higher Level, Paper 1, Text 1 — adapted from “Gravel Heart” by Abdulrazak Gurnah — © State Examinations Commission',
    },
  },
  // ── Biology (visual backfill) ──
  {
    id: 'biology-2022-hl-kidney-nephron',
    subjectId: 'biology', topicId: 'biology-2-3',
    subjectLabel: 'Biology', topicLabel: 'Breathing System and Excretion', level: 'higher',
    gist: 'The kidney has three regions you read from the outside in. The cortex is the outer band where filtration happens (it holds the glomeruli). The medulla is the middle, made of cone-shaped pyramids where water is reabsorbed and urine concentrated. The pelvis is the inner funnel-shaped space that collects urine before it leaves down the ureter. Inside, the working unit is the nephron: blood is forced into the glomerulus under pressure, small molecules are filtered out, then the proximal convoluted tubule (PCT), loop of Henle and distal convoluted tubule (DCT) reabsorb water and useful substances back into the surrounding capillaries.',
    oneMove: {
      label: 'Read the kidney outside-in',
      text: 'On any cross-section, the three regions always go outer to inner: cortex (filtration) then medulla/pyramids (reabsorption) then pelvis (collection). Lock that order and you can label A, B, C even on an unfamiliar drawing, then trace the urine path outward to the ureter.',
    },
    check: {
      prompt: 'In the kidney diagram above, name the three regions labelled A (outermost), B (the pyramids) and C (the inner funnel), and name the structure that urine then travels through to reach the bladder.',
      modelAnswer: 'A = cortex (the outer region, where filtration occurs in the glomeruli). B = medulla, made of the pyramids (where water is reabsorbed). C = pelvis (the central funnel-shaped space that collects urine). Urine then leaves the kidney through the ureter on its way to the bladder.',
      needed: ['A = cortex (outer region)', 'B = medulla / pyramid (middle region)', 'C = pelvis (inner collecting space)', 'Urine travels to the bladder via the ureter'],
    },
    source: 'SEC Leaving Certificate Biology 2022 Higher Level marking scheme, Q15(b) — kidney regions A: cortex, B: medulla (pyramid), C: pelvis; ureter to bladder',
    marksWeight: 9,
    figure: { src: '/exam-figures/biology/biology-2022-hl-kidney-nephron.png', alt: 'Two linked diagrams. Left: a cross-section of a human kidney with three regions marked by leader lines — A points to the thin outer band (cortex), B to the cone-shaped striped tissue beneath it (medulla/pyramids), and C to the central funnel-shaped cavity (pelvis) feeding the ureter. A small square on the kidney is magnified into the right-hand diagram: a single nephron showing the cup-shaped Glomerulus at top, the proximal convoluted tubule (PCT) and distal convoluted tubule (DCT) coiled tubules, the long hairpin Loop of Henle, and the surrounding Capillary network.', source: 'SEC Leaving Certificate Biology 2022 Higher Level, Q15 — © State Examinations Commission' },
  },
  {
    id: 'biology-2025-hl-neurons-motor-sensory',
    subjectId: 'biology', topicId: 'biology-2-4',
    subjectLabel: 'Biology', topicLabel: 'Responses to Stimuli', level: 'higher',
    gist: 'You can tell a motor neuron from a sensory neuron by what it connects to and where its cell body sits. A motor neuron carries impulses OUT to an effector, so its ending sits on a muscle (or gland) and its cell body lies at one end, in the central nervous system. A sensory neuron carries impulses IN from a receptor, so its ending sits in a sense organ such as the skin, and its cell body bulges off to the side on a branch part-way along the fibre. The myelin segments wrapped along the fibres of both are made by Schwann cells, which produce the myelin sheath that speeds the impulse.',
    oneMove: {
      label: 'Follow the wire to its destination',
      text: 'Don\'t guess from the cell body shape alone — trace each neuron to its end. If it terminates on muscle, it\'s the motor neuron (impulse going out). If it terminates in a receptor like skin, it\'s the sensory neuron (impulse coming in), and its cell body will be branched off to the side rather than in line.',
    },
    check: {
      prompt: 'In the diagram above, state whether Neuron X or Neuron Y is the motor neuron and justify your answer from the diagram. Then name what the Schwann cells produce.',
      modelAnswer: 'Neuron X is the motor neuron — it is connected to the muscle cells (and its cell body lies at one end), so it carries impulses out to an effector. (Neuron Y is therefore the sensory neuron — it ends in the skin and its cell body branches off to the side.) The Schwann cells produce myelin, forming the myelin sheath around the fibre.',
      needed: ['Neuron X is the motor neuron', 'Justification: it connects to / ends on the muscle cells (effector); cell body at one end', 'Schwann cells produce myelin (the myelin sheath)'],
    },
    source: 'SEC Leaving Certificate Biology 2025 Higher Level marking scheme, Q14(c) — motor neuron = X (connected to muscle cell); sensory neuron = Y (connected to skin); Schwann cell produces myelin sheath',
    marksWeight: 9,
    figure: { src: '/exam-figures/biology/biology-2025-hl-neurons.png', alt: 'Two neuron diagrams side by side. Neuron X (left) is a multipolar neuron with a large central cell body and many dendrites; its single long fibre runs down through Schwann-cell segments and branches onto a bundle of striated Muscle cells at the bottom. Neuron Y (right) has a tuft of dendrites at the top (bracketed and labelled Z), an oval cell body bulging off to the side on a short branch, and a fibre running down through Schwann-cell segments to fine endings inside a magnified circle of Skin. A central label \'Schwann cells\' with arrows points to the myelinated segments on both fibres.', source: 'SEC Leaving Certificate Biology 2025 Higher Level, Q14 — © State Examinations Commission' },
  },
  // ── Geography (visual backfill) ──
  {
    id: 'geography-2022-hl-forest-cover-barchart',
    subjectId: 'geography', topicId: 'geography-2-0',
    subjectLabel: 'Geography', topicLabel: 'Geographical Skills', level: 'higher',
    gist: 'Part One short-answer questions on a graph are pure data-reading: every mark is sitting in the figure if you read the axes and the question wording exactly. A bar chart gives you a category axis (the countries) and a value axis (here, % of land under forest, 0-70). Three moves cover almost every variant: COMPARE (count how many bars clear a reference line, e.g. the EU average), RELATE (find a bar that is double / half / equal to another), and CALCULATE (work out an average or a difference). The trap is the reference category: an EU Average bar is shown for comparison but is NOT one of the countries, so it is excluded when you are asked to average \'the countries shown\'. Read the value off the top of each bar, not the gridline nearest it.',
    oneMove: {
      label: 'The exam move',
      text: 'Before averaging, re-read the wording: \'the countries shown\' excludes any EU Average / reference bar. Sum only the country bars and divide by the number of countries, not by the total number of bars.',
    },
    check: {
      prompt: 'Using the bar chart above: (a) how many of the countries shown had a higher percentage of land covered by forest than the EU average? (b) name one country that had roughly twice the forest cover of Germany, and (c) calculate the average forest cover for the countries shown (i.e. excluding the EU Average bar).',
      modelAnswer: '(a) 4 countries — Austria (46%), Finland (66%), Slovakia (39%) and Sweden (64%) all sit above the EU average of 38%; Germany (32%), Ireland (11%) and Spain (37%) are below it. (b) Sweden (64%), which is about twice Germany\'s 32%. (c) Average = (46+66+32+11+39+37+64) ÷ 7 = 295 ÷ 7 = 42.1%. The EU Average bar (38%) is a reference value, not a country, so it is left out of the calculation.',
      needed: ['Count of 4 countries above the EU average (38%) — Austria, Finland, Slovakia, Sweden', 'Sweden named as roughly twice Germany\'s 32%', 'Average of the seven country values = 42.1%, with the EU Average bar correctly excluded'],
    },
    source: 'SEC Leaving Certificate Geography 2022 Higher Level, Part One Q11 (marking scheme: 4 / Sweden / 42.1)',
    marksWeight: 8,
    figure: { src: '/exam-figures/geography/geography-2022-hl-forest-cover-barchart.png', alt: 'A bar chart titled \'Percentage of Total Land Covered by Forest in Selected Countries in 2019\'. The vertical axis is labelled % and runs from 0 to 70. Eight green vertical bars show: Austria 46, Finland 66, Germany 32, Ireland 11, Slovakia 39, Spain 37, Sweden 64, and EU Average 38. Each bar is labelled with its value above it. Attribution: \'Amended from Eurostat\'.', source: 'SEC Leaving Certificate Geography 2022 Higher Level, Q11 — © State Examinations Commission' },
  },
  {
    id: 'geography-2022-hl-irelands-progress-infographic',
    subjectId: 'geography', topicId: 'geography-2-0',
    subjectLabel: 'Geography', topicLabel: 'Geographical Skills', level: 'higher',
    gist: 'A graphical-interpretation question hands you an infographic and tests whether you can extract a specific figure and do simple comparison and arithmetic on it. This CSO \'Measuring Ireland\'s Progress\' infographic ranks Ireland among the 27 EU states on three metrics, each shown as a row: a ranked strip from EU27 Lowest (rank 27) to EU27 Highest (rank 1), with the named lowest country, Ireland\'s own value, and the named highest country. Read each row separately. The marks come from: LIFT a single value straight off the row (Ireland\'s health spend); SPOT a country that appears at the same rank in more than one row; and SUBTRACT the highest from the lowest in a row. Watch the unit type printed on each row — persons vs % of GDP vs per 1,000 population — so you don\'t mix figures from different rows.',
    oneMove: {
      label: 'The exam move',
      text: 'Treat each metric as its own row and read the unit type first. For a \'difference between highest and lowest\' calculation, take the two named endpoint values from the SAME row and subtract — don\'t pull a number from a different metric.',
    },
    check: {
      prompt: 'Using the infographic above: (a) what percentage of its GDP did Ireland spend on health care in 2019? (b) which single country was ranked 27th (EU27 Lowest) in two of the three metrics? and (c) calculate the difference in number of persons between the lowest- and highest-ranked countries for population.',
      modelAnswer: '(a) 6.9% of GDP — read straight off Ireland\'s marker on the \'Public Expenditure on Health Care\' row (unit: % of GDP). (b) Luxembourg — it is the EU27 Lowest country for both Public Expenditure on Health Care (5.3%) and STEM Graduates (4.0). (Malta is lowest only for population.) (c) Population row, unit = number of persons: Germany (EU27 Highest) 83,166,711 minus Malta (EU27 Lowest) 514,564 = 82,652,147 persons.',
      needed: ['Ireland\'s health-care spend read correctly as 6.9% of GDP', 'Luxembourg identified as the lowest-ranked (27th) country in two metrics', 'Population difference = 83,166,711 − 514,564 = 82,652,147, using the two endpoint values from the population row'],
    },
    source: 'SEC Leaving Certificate Geography 2022 Higher Level, Part One Q12 (marking scheme: 6.9 / Luxembourg / 82,652,147)',
    marksWeight: 8,
    figure: { src: '/exam-figures/geography/geography-2022-hl-irelands-progress-infographic.png', alt: 'A CSO infographic titled \'Measuring Ireland\'s Progress 2019\' with three horizontal rows, one per metric. Each row runs from \'EU27 Lowest\' (rank 27) on the left to \'EU27 Highest\' (rank 1) on the right, with Ireland\'s position marked in between. Row 1 Population (Unit: No. of Persons): lowest Malta 514,564, highest Germany 83,166,711. Row 2 Public Expenditure on Health Care (Unit: % of GDP): lowest Luxembourg 5.3, Ireland 6.9, highest Germany 11.5. Row 3 STEM Graduates (Unit: Per 1,000 of population aged 20-29): lowest Luxembourg 4.0, highest Ireland 35.2. Each row notes \'No Change from 2018\'. Attribution: \'Amended from CSO\'.', source: 'SEC Leaving Certificate Geography 2022 Higher Level, Q12 — © State Examinations Commission' },
  },
  // ── Mathematics (visual backfill) ──
  {
    id: 'mathematics-2023-ol-scatterplot-correlation',
    subjectId: 'mathematics', topicId: 'mathematics-0-6',
    subjectLabel: 'Mathematics', topicLabel: 'Analysing & Interpreting Data', level: 'ordinary',
    gist: 'The correlation coefficient r is a single number from -1 to +1 that captures two things about a scatterplot at once: DIRECTION and STRENGTH. The SIGN gives direction - positive means the cloud of points slopes up (as x rises, y rises), negative means it slopes down. The SIZE (how close |r| is to 1) gives strength - the tighter the points hug a straight line, the closer r is to 1 or -1; a loose, scattered cloud sits nearer 0. So r = 0.95 is a strong upward line, r = -0.95 is an equally strong downward line, and r = 0.6 is a weaker (looser) upward trend. You read the picture before you reach for a number: first ask \'up or down?\' to fix the sign, then ask \'tight or loose?\' to fix the size.',
    oneMove: {
      label: 'Sign first, then strength',
      text: 'Decide the SIGN from the slope direction (up = +, down = -), THEN rank the positives by how tightly they cling to a line. The downward plot is the only negative one; of the two upward plots, the tighter one is 0.95 and the looser one is 0.6.',
    },
    check: {
      prompt: 'In the diagram above, each scatterplot (A, B, C) matches one of the correlation coefficients 0.95, 0.6, and -0.95. Match each coefficient to the correct plot, and explain why scatterplot B matches its value.',
      modelAnswer: '0.95 -> B, 0.6 -> C, -0.95 -> A. Plot A is the only one that slopes downward (as x increases y decreases), so it takes the negative value -0.95. B and C both slope upward, so both are positive. B\'s points lie very close to a straight upward line, so it is the strong positive value 0.95; C\'s points are more scattered about the upward trend, so it is the weaker 0.6. B matches 0.95 because it shows a strong positive linear correlation - the points all lie close to a positive straight line, so as x goes up y goes up.',
      needed: ['A slopes down so it is the negative coefficient -0.95', 'B and C both slope up so both are positive (0.95 and 0.6)', 'B\'s points cluster tightly on a straight line = strong, so 0.95; C is looser = weaker, so 0.6', 'B justification: strong positive linear correlation, points lie close to a positive straight line, as x increases y increases'],
    },
    source: 'SEC Leaving Certificate Mathematics 2023 Ordinary Level, Paper 2, Q3(b); marking scheme 2023 (0.95->B, 0.6->C, -0.95->A; B = strong positive linear correlation)',
    marksWeight: 10,
    figure: { src: '/exam-figures/maths/mathematics-2023-ol-scatterplot-correlation.png', alt: 'Three scatterplots side by side, labelled A, B and C, each plotted on identical axes and scales. Plot A shows about nine points forming a clear downward band from top-left to bottom-right (negative trend). Plot B shows about nine points rising tightly from bottom-left to top-right, hugging a straight upward line (strong positive trend). Plot C shows about nine points that rise overall from left to right but are more loosely scattered about the upward trend (weaker positive).', source: 'SEC Leaving Certificate Mathematics 2023 Ordinary Level, Paper 2, Q3 — © State Examinations Commission' },
  },
  {
    id: 'mathematics-2023-ol-cosine-rule-triangle',
    subjectId: 'mathematics', topicId: 'mathematics-1-2',
    subjectLabel: 'Mathematics', topicLabel: 'Trigonometry', level: 'ordinary',
    gist: 'When a triangle is NOT right-angled and you know all three sides but want an angle, the Cosine Rule is the tool: cos A = (b^2 + c^2 - a^2) / (2bc), where the angle you want sits opposite the side you label \'a\', and \'b\' and \'c\' are the two sides that meet AT that angle. The single most common slip is mislabelling: students plug the three numbers in without checking which side is actually opposite the wanted angle. The diagram is what tells you that. Find the angle\'s vertex, see which two sides touch it (those are b and c, on the bottom of the fraction), and the remaining side - the one across the triangle from the angle - is \'a\', the one that gets subtracted on top. Once cos A is a number, finish with the inverse cosine, cos^-1, on your calculator (in degrees mode) to recover the angle.',
    oneMove: {
      label: 'Opposite side gets subtracted',
      text: 'Identify the two sides touching the angle\'s vertex (these are b and c) and the side opposite it (this is a). Then a^2 is the one subtracted in the numerator: cos A = (b^2 + c^2 - a^2)/(2bc). Read the diagram to assign the sides BEFORE substituting.',
    },
    check: {
      prompt: 'Using the triangle in the diagram above (XY = 800 m, XZ = 700 m, ZY = 550 m, not to scale), find the size of the angle at X, correct to 1 decimal place.',
      modelAnswer: 'The two sides meeting at vertex X are XZ = 700 and XY = 800, and the side opposite X is ZY = 550. By the Cosine Rule, 550^2 = 700^2 + 800^2 - 2(700)(800)cos X, so cos X = (700^2 + 800^2 - 550^2) / (2 x 700 x 800) = (490000 + 640000 - 302500) / 1120000 = 827500/1120000 = 0.738839... Then X = cos^-1(0.738839) = 42.4° (correct to 1 decimal place).',
      needed: ['Read the diagram: the two sides at X are 700 and 800; the side opposite X is 550', 'Set up Cosine Rule with the OPPOSITE side (550) subtracted: cos X = (700^2 + 800^2 - 550^2)/(2x700x800)', 'Evaluate cos X = 827500/1120000 = 0.7388 (approx)', 'Take inverse cosine in degrees: X = cos^-1(0.7388) = 42.4°'],
    },
    source: 'SEC Leaving Certificate Mathematics 2023 Ordinary Level, Paper 2, Q7(c); marking scheme 2023 (cos X = (700^2+800^2-550^2)/(2x700x800); angle X = 42.4°)',
    marksWeight: 5,
    figure: { src: '/exam-figures/maths/mathematics-2023-ol-cosine-rule-triangle.png', alt: 'A triangle XYZ, not to scale, drawn flat and wide. X is the bottom-left vertex, Y the bottom-right vertex, and Z the apex slightly right of centre at the top. The side from X to Z (left) is labelled 700 m, the side from Z to Y (right) is labelled 550 m, and the base from X to Y is labelled 800 m. No angle values are marked.', source: 'SEC Leaving Certificate Mathematics 2023 Ordinary Level, Paper 2, Q7 — © State Examinations Commission' },
  },
  // ── English (visual backfill) ──
  {
    id: 'eng-comprehending-waxwing-birds-hl',
    subjectId: 'english', topicId: 'english-10-0',
    subjectLabel: 'English', topicLabel: 'Reading & comprehension', level: 'higher',
    gist: 'Paper 1 Question A is a close-reading test, not a comprehension-of-the-gist test. The examiner is checking whether you can do three separate things on the SAME text: (i) understand what the writer says, (ii) respond to an idea it raises, and (iii) analyse HOW the writing works (style). The trap is treating it like a summary. A summary scores the floor. What lifts you is that every single point you make is anchored to a specific moment in the text — a named image, a phrase you can point to, a sentence you can quote. Marks here are awarded for \'engagement with the text\', so a point with no textual reference is a half-point, however true it is.  Work the 2024 HL Text 1 example: Fintan O\'Toole\'s article \'We have taken flight from our deep link with birds\'. It links three generations of his family — himself, his father, his son — through birds: a waxwing tattoo on his son\'s arm, and a pallid swift his father found dead and had stuffed for the Natural History Museum (the \'Dead Zoo\'). Notice that he never states \'family relationships are about shared memory\' as an abstract claim — he SHOWS it through the swift in the freezer, the bus to Ballsbridge, the boy who would rather look at sharks. Your job in Question A is to read those concrete moments back to the examiner as evidence.',
    oneMove: {
      label: 'Anchor every point to a quotable moment in the text',
      text: 'For each point you make, you must be able to put your finger on the exact word, image or sentence in the passage that proves it, and ideally quote a short phrase of it. Make the point, then immediately attach the textual reference — point, then proof, in the same breath. A point without a reference is an opinion; a point with a reference is an answer. Do this three times for a three-point question and you have a full-marks structure before you have written anything clever.',
    },
    check: {
      prompt: 'Based on the passage shown (2024 HL Paper 1, Text 1), what does the writer reveal about the nature of family relationships? Make TWO points, and support each one with a short reference to the text.',
      modelAnswer: 'Point 1 — Family relationships are carried across generations through shared, inherited interest. The writer shows that his son\'s bird tattoo \'connects him to his father and his grandfather\', and he calls it \'a genetic memory with wings\' — the love of birds is passed down like an inheritance, binding three generations together. Point 2 — Family love is expressed through small, ordinary acts of shared time rather than grand statements. The writer recalls his father taking him on the bus \'out to Ballsbridge\' to see the waxwings, and says he was interested \'less in the birds than in my dad\'s excitement\', because the sharing of that pleasure \'was a gift of time and love\'. (A strong answer names the specific moment for each point and quotes a short phrase; a weak answer says \'the family is close\' with nothing from the text attached.)',
      needed: ['Point 1: relationships passed down the generations — anchored to the tattoo that \'connects him to his father and his grandfather\' / \'a genetic memory with wings\'', 'Point 2: love shown through small shared acts, not statements — anchored to the bus trip to Ballsbridge and the \'gift of time and love\'', 'Each point carries its own short textual reference (point, then proof)', 'The two points are distinct insights, not the same idea reworded'],
    },
    source: 'SEC Leaving Certificate English 2024 Higher Level, Paper 1, Text 1 — edited article from The Irish Times, \'We have taken flight from our deep link with birds\' by Fintan O\'Toole (published January 2023) — © State Examinations Commission',
    marksWeight: 15,
    passage: {
      text: 'TEXT 1 – FAMILY CONNECTIONS AND THE NATURAL WORLD\nThis text is an edited article from The Irish Times, by Fintan O\'Toole entitled, \'We have taken flight from our deep link with birds.\' It was published in January 2023.\n\nParents – at least those of my age – don\'t like the idea of their children getting tattoos. Perhaps it\'s an ego thing: the flesh of our flesh should remain spotless.\n\nMy youngest son swerved elegantly around these foolish objections by getting a large image of a handsome bird inked onto his forearm.\n\nIt\'s a waxwing, a gorgeous winter visitor to Ireland that looks like a dressed-up finch, with a backwards quiff for a crest and two vivid red blobs on its wings like sealing wax applied to an ancient missive from on high. My son knew that this image would disarm my prejudices because the bird connects him to his father and his grandfather. It is a genetic memory with wings.\n\nThe first conscious piece of writing I ever did was a school essay on the topic of birds. I called it \'Waxwings\'.\n\nI wrote about how my father took me and my brother on the bus out to Ballsbridge where the rowan trees near the American embassy were alive with dozens of waxwings. I was interested, of course, less in the birds than in my dad\'s excitement at seeing them, and the way the sharing of this pleasure with us was a gift of time and love.\n\nAfter my father died, something of his spirit migrated into that tattoo. It found a new fleshy perch. It also has an older abode. One of the reasons I was so glad to see the Dead Zoo reopened, that strange treasure house of taxidermy that is the Natural History Museum in Dublin, is that there\'s another bird in it that connects me to my father.\n\nIn the corner of a top shelf of a case of stuffed birds, there is one you would miss if you were not looking for it. It is a pallid swift, a Mediterranean bird first recorded in Ireland in 1953. The person who spotted it, on Howth Head, was my father. In those days before mobile phones, he ran down to the village to find a phone box to call his fellow bird watchers. As he was making his way back up the Head he found it dead on the path, apparently hit by a hawk.\n\nHe did what any normal obsessive would do, which was to lift its body gently and place it tenderly in his bag. He took it home and, over my mother\'s appalled objections, put it beside the garden peas in the freezer until the Dead Zoo opened after the weekend. The curators there did not tell him to get stuffed, but had the bird stuffed and mounted, albeit in an obscure cranny. His name is on the label.\n\nI hadn\'t seen it for a long time, while the museum was closed for an extensive refurbishment. But, last week, I called in to see if it was still there. I went with my waxwing-stamped son and his own four-year-old son. The boy was not impressed - the sharks and giant elks are far more interesting. But that was not the point. Maybe, if we do this every year, he will lay down a little seam of memory: a trace of his great-grandfather in a hidden corner of a slightly fantastical hall of animal curiosities in Dublin.\n\nBetween the waxwing tattoo on the arm and the pallid swift on the shelf, I couldn\'t help thinking about birds as our living clocks and calendars. They mark time, calling the sun up and lulling it down, announcing the seasons with their comings and goings. But they also deepen our sense of time itself. Because they are unbounded, they connect everything to everything else. They animate the physical world – the trees, the skies, the seashore, the hedges – but also the intangible worlds of memory and belonging.\n\nBut we are breaking this connection, cruelly and carelessly. Much as I loved being back in the Dead Zoo last week, I could not avoid the melancholy realisation that birds that were common in Ireland can now be seen only through the glass of display cases. In the museum of natural history, nature is consigned to history.\n\nI grew up on a housing estate three miles from the centre of Dublin. The sound that punctuated our football games in the local park was the loud kerrx-kerrx of the corncrake calling for a mate. There are fewer than 200 calling males left in Ireland now. Almost no one in any built-up area ever hears that fabulously comic song of urgency and yearning.\n\nWe are systematically de-animating the landscape, sucking the life out of it, making it flat and dull and bleakly lifeless. The texture of sound that every previous generation experienced is being frayed into dead air.\n\nWe are not creatures that can live by bread alone. We live on memory and wonder, on the sense of connection to each other and to the natural world. If we allow those things to depart, we are taking flight from ourselves.',
      source: 'SEC Leaving Certificate English 2024 Higher Level, Paper 1, Text 1 — edited article from The Irish Times, \'We have taken flight from our deep link with birds\' by Fintan O\'Toole (published January 2023) — © State Examinations Commission',
    },
  },
  {
    id: 'eng-comprehending-ai-robots-friends-or-foes-ol',
    subjectId: 'english', topicId: 'english-10-0',
    subjectLabel: 'English', topicLabel: 'Reading & comprehension', level: 'ordinary',
    gist: 'At Ordinary Level, Paper 1 Question A is worth 40 marks and almost always asks you to (i) say what you LEARNED from the text, (ii) give a personal response to an idea it raises, and (iii) do a short personal task. The single biggest mark-loser is answering from your own opinion when the question says \'support your answer with reference to the text\'. The examiner cannot give you the marks for \'I think robots are scary\' — they CAN give you the marks for \'the text says HAL murders the humans it was designed to assist, which is frightening\'. Same idea; only the second one is paid.  Work the 2022 OL Text 1 example: an information text titled \'Humans and AI robots: friends or foes?\'. It walks through how our relationship with artificially intelligent (AI) robots is changing — people thanking their vacuum cleaners, robotic pets, the lifelike robot Sophia being given citizenship by Saudi Arabia, and two films (HAL in 2001: A Space Odyssey, and Robot and Frank) that show a frightening future and a hopeful one. When the question asks what you LEARNED, you go back and lift the specific facts — Sophia, the bar-codes idea, the two films — rather than writing your general feelings about technology.',
    oneMove: {
      label: 'For every point, point back to a fact the text actually states',
      text: 'Make your point in your own words, then add \'the text says…\' or \'for example, in the text…\' and quote or name the exact detail. Do this for each point the question asks for (usually three). If you cannot point to where the text says it, it is your opinion, not something you learned — and the personal-response part is the only place opinions get marked. Keep the two separate: facts-from-the-text for \'what you learned\', your own view only where the question invites it.',
    },
    check: {
      prompt: 'Based on the passage shown (2022 OL Paper 1, Text 1), explain TWO things you learned about the changing relationship between humans and AI robots. Support each point with a reference to the text.',
      modelAnswer: 'Point 1 — I learned that people are starting to form emotional bonds with their machines, not just use them. The text says that some owners of AI vacuum cleaners \'display gratitude toward their devices\' and believe that because the machine \'works hard it should take breaks, just as a human would\'. Point 2 — I learned that AI robots are becoming so lifelike that society is treating them more like people. The text says that in 2017 a lifelike robot called Sophia, developed by Hanson Robotics, \'was offered citizenship by Saudi Arabia\', and that some experts now suggest robots should have \'visible bar-codes\' so humans know they are not human. (A strong answer names the specific detail — the grateful vacuum-cleaner owners, Sophia\'s citizenship — for each point; a weak answer just says \'robots are getting better\' with nothing from the text.)',
      needed: ['Point 1: people now form emotional/human-like bonds with machines — anchored to owners who \'display gratitude toward their devices\' and think the machine \'should take breaks, just as a human would\'', 'Point 2: robots are increasingly lifelike and treated more like people — anchored to Sophia being \'offered citizenship by Saudi Arabia\' and the \'visible bar-codes\' suggestion', 'Each point is supported with a specific reference to the text, not general opinion', 'The two points are different ideas, not the same point twice'],
    },
    source: 'SEC Leaving Certificate English 2022 Ordinary Level, Paper 1, Text 1 — \'Humans and AI robots: friends or foes?\' (based on information from a variety of sources) — © State Examinations Commission',
    marksWeight: 10,
    passage: {
      text: 'TEXT 1 – HUMANS AND AI ROBOTS: FRIENDS OR FOES?\nThis text is based on information from a variety of sources and raises the question, will human beings and artificially intelligent (AI) robots be friends or foes in the future? The text also features two images of AI robots.\n\n1. Whether we like it or not, it seems inevitable that humans will co-exist with artificially intelligent (AI) robots in the future. This raises an important question: can humans and such robots ever be friends or will the relationship be a destructive one?\n\n2. Studies suggest that as we engage more and more with robotic machines, such as lawn mowers or AI vacuum cleaners, people develop emotional bonds with these devices. Some owners of AI vacuum cleaners display gratitude toward their devices. They believe that because their machine works hard it should take breaks, just as a human would. Our relationship with AI robots will continue to evolve as our engagement with these devices extends beyond merely useful machines. A variety of robotic pets already on the market can provide companionship without the need for feeding, cleaning or exercise that a more traditional pet would require. These practical alternatives to real animals will enable people who might not be able to keep a regular pet to enjoy an equivalent experience with a robotic one in the future.\n\n3. By now we have become quite familiar with AI assistants that have human names, such as Alexa or Siri. While many people regard these as useful devices, few would think of them as having human qualities and even fewer would regard them as friends. This long-established divide between humans and robots underwent a seismic change in 2017 when Sophia, an incredibly lifelike AI robot developed by Hanson Robotics, was offered citizenship by Saudi Arabia. Described as a "humanoid", Sophia has become one of the best-known AI robots in the world and has revolutionised the way in which we think about AI robots and their relationship with us.\n\n4. In the light of these developments, it is perhaps not surprising some experts have suggested that AI robots should have visible bar-codes, or other clear signage, to alert any humans interacting with them of their robotic, non-human status. As intelligent robots grow increasingly sophisticated, concerns also grow that they may pose a growing risk to human employment. While many people are happy to see dangerous or unpleasant jobs done by non-humans, a less friendly view may be taken if AI robots pose a significant threat to human jobs in sectors such as retail, hospitality and health care.\n\n5. The film industry may offer us some insight into what our future life with AI robots could be like. The AI computer, HAL, in Stanley Kubrick\'s classic film, 2001: A Space Odyssey, provides a rather frightening view of the relationship between humans and AI robots. HAL begins to think on its own and show signs of emotion, which it has not been programmed to do. Ultimately HAL, in order to protect itself, murders the humans it was designed to assist. Does this film provide a warning for the future which we would be wise to heed?\n\n6. The 2012 movie, Robot and Frank, offers us a more hopeful prospect. The movie\'s main character, Frank, is suffering from early symptoms of dementia. Frank\'s son buys his father a home robot that can talk, cook and clean. It reminds Frank to take his medicine. Although initially unhappy with the arrangement, Frank slowly starts to see the robot both as a functional tool and a companion. By the end of the film, a close bond has developed between a man and a machine. With the number of older people in our society increasing, it is possible that in the future AI robots could provide some of the care and companionship they will require. There is little doubt that in the future artificially intelligent robots will play an increasing role in our lives. We must work to ensure that our future relationship with them is a happy one for us all.\n\nIMAGE 1   An AI robotic vacuum cleaner\nIMAGE 2   AI robot, Sophia',
      source: 'SEC Leaving Certificate English 2022 Ordinary Level, Paper 1, Text 1 — \'Humans and AI robots: friends or foes?\' (based on information from a variety of sources) — © State Examinations Commission',
    },
  },
];

/** Subject ids that currently have recovery content (drives the picker). */
export function subjectsWithContent(): { subjectId: string; subjectLabel: string; count: number }[] {
  const map = new Map<string, { subjectId: string; subjectLabel: string; count: number }>();
  for (const c of RECOVERY_CARDS) {
    const e = map.get(c.subjectId) ?? { subjectId: c.subjectId, subjectLabel: c.subjectLabel, count: 0 };
    e.count++;
    map.set(c.subjectId, e);
  }
  return [...map.values()];
}

/** All recovery cards for a subject, in curriculum (syllabus) order. */
export function cardsForSubject(subjectId: string): RecoveryCard[] {
  return RECOVERY_CARDS.filter(c => c.subjectId === subjectId);
}
