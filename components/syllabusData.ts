/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

// ─── Types ───────────────────────────────────────────────────────────────────

export interface SyllabusTopic {
  name: string;
  section: string;           // Paper/section label (e.g. "Paper 1 Section B", "Section C")
  markWeight: number;        // approximate % of total marks this topic can occupy
  examFrequency: number;     // 1-10 (10 = appears every year)
  difficulty: number;        // 1-5 (5 = very hard)
  studyHours: number;        // estimated hours to study thoroughly
  tip: string;               // brief exam-specific advice
}

export interface PaperInfo {
  name: string;
  marks: number;
  duration: string;
}

export interface SubjectSyllabus {
  subject: string;
  totalMarks: number;
  papers: PaperInfo[];
  topics: SyllabusTopic[];
  keyAdvice: string;
}

// ─── Efficiency score: marks-per-hour weighted by exam frequency ─────────────

export function computeEfficiency(topic: SyllabusTopic, totalMarks: number): number {
  const potentialMarks = (topic.markWeight / 100) * totalMarks;
  const marksPerHour = potentialMarks / Math.max(1, topic.studyHours);
  const frequencyMultiplier = topic.examFrequency / 10;
  return Math.round(marksPerHour * frequencyMultiplier * 10) / 10;
}

export function getQuadrant(topic: SyllabusTopic): 'start-here' | 'high-value' | 'worth-knowing' | 'only-if-time' {
  const freqHigh = topic.examFrequency >= 7;
  const weightHigh = topic.markWeight >= 12;
  if (freqHigh && weightHigh) return 'start-here';
  if (freqHigh || weightHigh) return 'high-value';
  if (topic.examFrequency >= 4) return 'worth-knowing';
  return 'only-if-time';
}

export const QUADRANT_LABELS: Record<string, { label: string; color: string; bg: string }> = {
  'start-here': { label: 'Start Here', color: 'text-emerald-600 dark:text-emerald-400', bg: 'bg-emerald-100 dark:bg-emerald-900/30' },
  'high-value': { label: 'High Value', color: 'text-blue-600 dark:text-blue-400', bg: 'bg-blue-100 dark:bg-blue-900/30' },
  'worth-knowing': { label: 'Worth Knowing', color: 'text-amber-600 dark:text-amber-400', bg: 'bg-amber-100 dark:bg-amber-900/30' },
  'only-if-time': { label: 'Only If Time', color: 'text-zinc-500 dark:text-zinc-400', bg: 'bg-zinc-100 dark:bg-zinc-800' },
};

// ─── Subject Data ────────────────────────────────────────────────────────────

export const SYLLABUS_DATA: SubjectSyllabus[] = [

  // ═══════════════════════════════════════════════════════════════════════════
  // ENGLISH
  // ═══════════════════════════════════════════════════════════════════════════
  {
    subject: 'English',
    totalMarks: 400,
    papers: [
      { name: 'Paper 1 — Language', marks: 200, duration: '2h 50m' },
      { name: 'Paper 2 — Literature', marks: 200, duration: '3h 20m' },
    ],
    keyAdvice: 'Paper 1 composing (personal essay) is worth 25% of your entire grade and you control it completely. Master essay structure, practise under timed conditions, and have 3-4 strong openings ready. For Paper 2, the Comparative Study is worth the most marks — know your 3 texts inside out for the active mode.',
    topics: [
      { name: 'Comprehension (Question A)', section: 'Paper 1, Section I', markWeight: 12.5, examFrequency: 10, difficulty: 2, studyHours: 6, tip: 'Practise inference and language analysis. Always quote from the text. 3 sub-questions, answer all.' },
      { name: 'Functional Writing (Question B)', section: 'Paper 1, Section I', markWeight: 12.5, examFrequency: 10, difficulty: 3, studyHours: 8, tip: 'You write for a specific audience and purpose — speech, article, letter, blog. Register and format matter as much as content.' },
      { name: 'Composing (Essay)', section: 'Paper 1, Section II', markWeight: 25, examFrequency: 10, difficulty: 3, studyHours: 15, tip: 'Worth 100 marks. Personal essay appears every year. Have a bank of prepared material: anecdotes, reflections, imagery. Examiners reward authentic voice over big vocabulary.' },
      { name: 'Single Text (Shakespeare)', section: 'Paper 2, Section I', markWeight: 15, examFrequency: 10, difficulty: 4, studyHours: 12, tip: 'Shakespeare is mandatory since 2023. Learn key quotes, know themes and character arcs. Structure: intro → 3-4 paragraphs with quotes → conclusion.' },
      { name: 'Comparative Study', section: 'Paper 2, Section II', markWeight: 17.5, examFrequency: 10, difficulty: 4, studyHours: 15, tip: 'Worth 70 marks. One mode from: General Vision & Viewpoint, Literary Genre, Theme/Issue, Cultural Context. Know your 3 texts for all modes — but predict which is rested.' },
      { name: 'Unseen Poetry', section: 'Paper 2, Section III', markWeight: 5, examFrequency: 10, difficulty: 3, studyHours: 4, tip: 'Worth 20 marks. Read the poem 3 times. Identify: tone, imagery, themes, structure. Always quote specific words/phrases.' },
      { name: 'Prescribed Poetry', section: 'Paper 2, Section III', markWeight: 12.5, examFrequency: 10, difficulty: 4, studyHours: 14, tip: 'Worth 50 marks. Study all poets on the list but focus on 4-5 deeply. Yeats and Bishop are historically high-frequency.' },
    ],
  },

  // ═══════════════════════════════════════════════════════════════════════════
  // MATHEMATICS
  // ═══════════════════════════════════════════════════════════════════════════
  {
    subject: 'Mathematics',
    totalMarks: 600,
    papers: [
      { name: 'Paper 1', marks: 300, duration: '2h 30m' },
      { name: 'Paper 2', marks: 300, duration: '2h 30m' },
    ],
    keyAdvice: 'Maths rewards consistent practice over cramming. Section A (Concepts & Skills) questions are shorter and more predictable — secure these marks first. Calculus dominates Paper 1 Section B. For Paper 2, Probability & Statistics is the most structured and predictable topic. Remember: +25 bonus for H6 or above.',
    topics: [
      { name: 'Algebra', section: 'Paper 1, Section A', markWeight: 10, examFrequency: 10, difficulty: 3, studyHours: 12, tip: 'Expressions, equations, inequalities, logs. Appears every year in Section A. Practise manipulation and solving.' },
      { name: 'Complex Numbers', section: 'Paper 1, Section A', markWeight: 8, examFrequency: 9, difficulty: 4, studyHours: 10, tip: 'Argand diagram, De Moivre\'s, roots of unity. Almost always in Section A. High marks for methodical work.' },
      { name: 'Sequences & Series', section: 'Paper 1, Section A', markWeight: 7, examFrequency: 8, difficulty: 3, studyHours: 8, tip: 'AP, GP, sigma notation, sum to infinity. Know the formulae cold. Series questions reward accuracy.' },
      { name: 'Functions', section: 'Paper 1, Section A/B', markWeight: 8, examFrequency: 8, difficulty: 3, studyHours: 10, tip: 'Graphs, transformations, injective/surjective. Can appear in Section A or B. Graphing skills are essential.' },
      { name: 'Calculus', section: 'Paper 1, Section B', markWeight: 18, examFrequency: 10, difficulty: 5, studyHours: 20, tip: 'Differentiation + integration dominate Paper 1 Section B. First principles, max/min, rates of change, area under curve. At least 1 full Section B question is calculus.' },
      { name: 'Financial Maths', section: 'Paper 1, Section A/B', markWeight: 5, examFrequency: 5, difficulty: 3, studyHours: 6, tip: 'Compound interest, present value, amortisation. Doesn\'t appear every year but when it does, it\'s straightforward. Know the formulae.' },
      { name: 'Induction', section: 'Paper 1, Section A', markWeight: 5, examFrequency: 7, difficulty: 4, studyHours: 6, tip: 'Proof by induction: base case, assume for k, prove for k+1. Practise the 4-step structure until automatic.' },
      { name: 'Coordinate Geometry', section: 'Paper 2, Section A', markWeight: 8, examFrequency: 9, difficulty: 3, studyHours: 10, tip: 'Line and circle. Equations, tangents, intersections. Very predictable question format. Know your formulae page.' },
      { name: 'Trigonometry', section: 'Paper 2, Section A/B', markWeight: 10, examFrequency: 9, difficulty: 4, studyHours: 12, tip: 'Identities, equations, graphs, sine/cosine rules, 3D problems. Identities are key — learn to prove and apply them.' },
      { name: 'Probability & Statistics', section: 'Paper 2, Section B', markWeight: 12, examFrequency: 10, difficulty: 3, studyHours: 14, tip: 'Bernoulli trials, normal distribution, hypothesis testing, confidence intervals. Always on Paper 2. Most structured and predictable topic.' },
      { name: 'Geometry (Proofs)', section: 'Paper 2, Section A', markWeight: 5, examFrequency: 6, difficulty: 5, studyHours: 8, tip: 'Theorems and proofs. Know the 3 examinable proofs. Questions tend to test constructions and theorem application.' },
      { name: 'Length, Area & Volume', section: 'Paper 1 or 2', markWeight: 4, examFrequency: 6, difficulty: 2, studyHours: 5, tip: 'Can appear on either paper. Usually combined with other topics. Formulae from the log tables.' },
    ],
  },

  // ═══════════════════════════════════════════════════════════════════════════
  // BIOLOGY
  // ═══════════════════════════════════════════════════════════════════════════
  {
    subject: 'Biology',
    totalMarks: 400,
    papers: [
      { name: 'One Paper', marks: 400, duration: '3h' },
    ],
    keyAdvice: 'Biology is definition-heavy — learn definitions first, they\'re worth 15-20% of total marks. Ecology and Genetics appear almost every year. Experiments (Section B) are free marks if you know the method, equipment, and results. Long questions follow predictable patterns — past papers are your best friend.',
    topics: [
      { name: 'Ecology', section: 'Section A & C', markWeight: 15, examFrequency: 10, difficulty: 3, studyHours: 10, tip: 'Ecosystems, food webs, nutrient cycling, pollution, conservation. Near-annual in both short and long questions. Know field study methods.' },
      { name: 'Genetics (DNA, RNA, Protein Synthesis)', section: 'Section C', markWeight: 15, examFrequency: 9, difficulty: 4, studyHours: 14, tip: 'DNA structure, replication, transcription, translation, genetic crosses, genetic engineering. Alternates between full and partial questions. Crosses didn\'t appear in 2025 — likely for 2026.' },
      { name: 'Photosynthesis', section: 'Section B & C', markWeight: 10, examFrequency: 9, difficulty: 4, studyHours: 10, tip: 'Light and dark stages, factors affecting rate, experiment (rate measurement). Can appear in consecutive years. Know the stages step by step.' },
      { name: 'Respiration', section: 'Section B & C', markWeight: 8, examFrequency: 8, difficulty: 4, studyHours: 10, tip: 'Glycolysis, Krebs cycle, electron transport chain, aerobic vs anaerobic. Often paired with photosynthesis questions.' },
      { name: 'Enzymes', section: 'Section A, B & C', markWeight: 8, examFrequency: 9, difficulty: 3, studyHours: 7, tip: 'Factors affecting enzyme activity, immobilisation, experiments. Very high frequency. Lock-and-key model, induced fit.' },
      { name: 'Cell Structure & Division', section: 'Section A & C', markWeight: 8, examFrequency: 8, difficulty: 3, studyHours: 8, tip: 'Organelles, mitosis, meiosis, cancer. Frequent in short questions. Know stages of mitosis and meiosis with diagrams.' },
      { name: 'Human Biology — Circulatory', section: 'Section C', markWeight: 7, examFrequency: 7, difficulty: 3, studyHours: 8, tip: 'Heart structure, blood vessels, blood components. Know heart dissection experiment. Diagrams earn marks.' },
      { name: 'Human Biology — Nervous System', section: 'Section C', markWeight: 7, examFrequency: 7, difficulty: 4, studyHours: 8, tip: 'Brain, reflex arc, eye structure, ear structure. Detailed labelled diagrams are essential.' },
      { name: 'Human Biology — Reproductive', section: 'Section C', markWeight: 6, examFrequency: 6, difficulty: 3, studyHours: 6, tip: 'Male/female systems, menstrual cycle, pregnancy. Rotates through Section C.' },
      { name: 'Bacteria, Fungi & Microorganisms', section: 'Section C', markWeight: 6, examFrequency: 7, difficulty: 3, studyHours: 6, tip: 'Structure, reproduction, economic importance. Only appeared as partial in 2025 — full question likely in 2026.' },
      { name: 'Plant Biology', section: 'Section A & C', markWeight: 6, examFrequency: 7, difficulty: 3, studyHours: 7, tip: 'Structure, transport (xylem/phloem), tropisms, flower reproduction. Know transport experiments.' },
      { name: 'Food & Nutrition', section: 'Section A', markWeight: 4, examFrequency: 7, difficulty: 2, studyHours: 4, tip: 'Food groups, food tests, balanced diet. Common in Section A short questions. Easy marks if you know the tests.' },
      { name: 'Mandatory Experiments', section: 'Section B', markWeight: 15, examFrequency: 10, difficulty: 2, studyHours: 10, tip: '22 experiments. Section B is guaranteed. Learn: method, equipment, results, precautions, controls. Free marks.' },
    ],
  },

  // ═══════════════════════════════════════════════════════════════════════════
  // BUSINESS
  // ═══════════════════════════════════════════════════════════════════════════
  {
    subject: 'Business',
    totalMarks: 400,
    papers: [
      { name: 'One Paper', marks: 400, duration: '3h' },
    ],
    keyAdvice: 'Business rewards students who use real-world examples. The ABQ (Section 2) is always about Units 5-7 — prepare for marketing, HRM, and ratio analysis. Learn definitions precisely — the marking scheme is strict. Short questions (Section 1) test breadth, so cover every unit.',
    topics: [
      { name: 'Management Skills & Activities', section: 'Section 1 & 3', markWeight: 12, examFrequency: 9, difficulty: 3, studyHours: 8, tip: 'Leading, motivating, communicating, planning, organising, controlling. McGregor, Maslow, Herzberg. Near-annual. Use real business examples.' },
      { name: 'Marketing', section: 'Section 2 (ABQ) & 3', markWeight: 12, examFrequency: 9, difficulty: 3, studyHours: 8, tip: 'Market research, segmentation, marketing mix (4Ps), product life cycle. Near-annual. ABQ often includes marketing analysis.' },
      { name: 'Insurance', section: 'Section 1 & 3', markWeight: 8, examFrequency: 8, difficulty: 2, studyHours: 6, tip: 'Principles of insurance, types of insurance. Very regularly appears. Learn the 7 principles and apply to scenarios.' },
      { name: 'HRM (Recruitment & Training)', section: 'Section 2 & 3', markWeight: 8, examFrequency: 8, difficulty: 3, studyHours: 7, tip: 'Recruitment process, selection, training methods, performance appraisal. Common in ABQ and long questions.' },
      { name: 'Industrial Relations & Employment Law', section: 'Section 1 & 3', markWeight: 10, examFrequency: 8, difficulty: 3, studyHours: 8, tip: 'Trade unions, WRC, Labour Court, unfair dismissal, employment legislation. Frequently in short and long questions. Know the dispute resolution process.' },
      { name: 'Consumer Protection', section: 'Section 1 & 3', markWeight: 7, examFrequency: 7, difficulty: 2, studyHours: 5, tip: 'Consumer Protection Act 2007, CCPC, Sale of Goods Act. Common long question. Know consumer rights and remedies.' },
      { name: 'Accounting & Finance', section: 'Section 2 (ABQ) & 3', markWeight: 10, examFrequency: 8, difficulty: 4, studyHours: 10, tip: 'Final accounts, ratio analysis, cash flow, budgeting. ABQ nearly always includes ratio analysis. Know profitability, liquidity, efficiency ratios.' },
      { name: 'Business Ownership & Enterprise', section: 'Section 1 & 3', markWeight: 8, examFrequency: 8, difficulty: 2, studyHours: 6, tip: 'Sole trader, partnership, company, cooperative. Characteristics of entrepreneurs. Frequent in short questions.' },
      { name: 'Taxation', section: 'Section 1 & 3', markWeight: 6, examFrequency: 7, difficulty: 3, studyHours: 5, tip: 'Income tax, corporation tax, VAT, PAYE/PRSI. Regular in both short and long questions. Know the calculations.' },
      { name: 'International Trade & EU', section: 'Section 1 & 3', markWeight: 7, examFrequency: 7, difficulty: 3, studyHours: 6, tip: 'Globalisation, MNCs, EU institutions, Single Market, exchange rates. Know advantages/disadvantages of MNCs and EU membership.' },
      { name: 'Communication & IT', section: 'Section 1 & 3', markWeight: 5, examFrequency: 6, difficulty: 2, studyHours: 4, tip: 'Types of communication, barriers, IT in business. Regular in both formats. Easy marks with good examples.' },
      { name: 'People in Business (Stakeholders)', section: 'Section 1', markWeight: 4, examFrequency: 7, difficulty: 2, studyHours: 4, tip: 'Types of stakeholders, rights, responsibilities, conflict. Common in short questions. Know all stakeholder types.' },
      { name: 'Government & Business', section: 'Section 1 & 3', markWeight: 5, examFrequency: 6, difficulty: 2, studyHours: 4, tip: 'Enterprise Ireland, IDA, LEOs, grants, supports. Know what each agency does and give examples.' },
    ],
  },

  // ═══════════════════════════════════════════════════════════════════════════
  // HISTORY (Later Modern)
  // ═══════════════════════════════════════════════════════════════════════════
  {
    subject: 'History',
    totalMarks: 500,
    papers: [
      { name: 'Research Study Report (RSR)', marks: 100, duration: 'Pre-submitted' },
      { name: 'Written Exam', marks: 400, duration: '2h 50m' },
    ],
    keyAdvice: 'The RSR is 20% of your grade and you control it — aim for full marks. For the exam, the DBQ for 2026-2027 is Ireland Topic 2 (Political & Social Reform 1870-1914). The most popular topics are Ireland Topic 3 (Sovereignty & Partition) and Europe Topic 3 (Dictatorship & Democracy). Each essay needs a clear argument, not just a list of facts.',
    topics: [
      { name: 'Research Study Report (RSR)', section: 'Pre-submitted', markWeight: 20, examFrequency: 10, difficulty: 3, studyHours: 15, tip: 'Outline plan (15), sources (25), essay (50), review (10). Start early. Choose a topic you find genuinely interesting. Marks for source evaluation and personal reflection.' },
      { name: 'DBQ — Ireland Topic 2: Political & Social Reform 1870-1914', section: 'Section 1 (Compulsory)', markWeight: 20, examFrequency: 10, difficulty: 3, studyHours: 12, tip: '2026/2027 DBQ topic. Parnell, Land War, Home Rule, GAA, Gaelic League, 1913 Lockout. Practise document analysis: comprehension, comparison, criticism of sources.' },
      { name: 'Ireland Topic 3: Sovereignty & Partition 1912-1949', section: 'Section 2', markWeight: 20, examFrequency: 10, difficulty: 4, studyHours: 14, tip: 'Most popular Ireland topic. 1916 Rising, War of Independence, Civil War, partition, de Valera, Anglo-Irish Treaty. Always has 4 essay choices.' },
      { name: 'Ireland Topic 6: Government & Society in Republic 1949-1989', section: 'Section 2', markWeight: 20, examFrequency: 10, difficulty: 3, studyHours: 12, tip: 'Second most popular Ireland topic. Lemass, economic planning, social change, troubles impact on Republic. Good alternative to Topic 3.' },
      { name: 'Europe Topic 3: Dictatorship & Democracy 1920-1945', section: 'Section 3', markWeight: 20, examFrequency: 10, difficulty: 4, studyHours: 14, tip: 'Stalin, Hitler, Mussolini. Most popular Europe topic. Know: rise to power, consolidation, policies, WWII. Each leader is a potential full essay.' },
      { name: 'Europe Topic 6: United States & the World 1945-1989', section: 'Section 3', markWeight: 20, examFrequency: 10, difficulty: 3, studyHours: 12, tip: 'JFK, Vietnam, Cold War, civil rights, Moon landing. Second most popular Europe topic. Strong narrative topics that suit essay writing.' },
      { name: 'Ireland Topic 5: Northern Ireland 1949-1993', section: 'Section 2', markWeight: 20, examFrequency: 10, difficulty: 3, studyHours: 10, tip: 'Civil rights movement, Troubles, key events (Bloody Sunday, hunger strikes). Less popular but very current and engaging.' },
      { name: 'Europe Topic 4: Division & Co-operation 1945-1992', section: 'Section 3', markWeight: 20, examFrequency: 10, difficulty: 3, studyHours: 10, tip: 'Cold War in Europe, Berlin Wall, EU formation. Good complement to US Topic 6. Know: NATO, Warsaw Pact, détente.' },
    ],
  },

  // ═══════════════════════════════════════════════════════════════════════════
  // GEOGRAPHY
  // ═══════════════════════════════════════════════════════════════════════════
  {
    subject: 'Geography',
    totalMarks: 500,
    papers: [
      { name: 'Written Exam', marks: 400, duration: '2h 50m' },
      { name: 'Geographical Investigation', marks: 100, duration: 'Pre-submitted' },
    ],
    keyAdvice: 'The Geographical Investigation is 20% — aim for full marks. For the exam, Physical Geography (plate tectonics, rivers, coasts) and Geoecology are the most examined. Short questions test breadth, so cover the whole course. Long questions need specific examples and case studies — named places, figures, and real-world evidence.',
    topics: [
      { name: 'Geographical Investigation', section: 'Pre-submitted', markWeight: 20, examFrequency: 10, difficulty: 3, studyHours: 12, tip: 'Fieldwork report. Use OS maps, photos, data analysis. Worth 100 marks. Follow the SEC marking scheme structure exactly.' },
      { name: 'Plate Tectonics & Volcanism', section: 'Section 1 — Physical', markWeight: 12, examFrequency: 10, difficulty: 3, studyHours: 10, tip: 'Plate boundaries, volcanoes, earthquakes, fold mountains. Near-guaranteed every year. Use Irish and global examples.' },
      { name: 'River Processes & Landforms', section: 'Section 1 — Physical', markWeight: 10, examFrequency: 9, difficulty: 3, studyHours: 8, tip: 'Erosion, transport, deposition. V-shaped valleys, meanders, floodplains, deltas. Very popular. Draw labelled diagrams.' },
      { name: 'Coastal Processes & Landforms', section: 'Section 1 — Physical', markWeight: 8, examFrequency: 7, difficulty: 3, studyHours: 7, tip: 'Wave action, erosion features (cliffs, stacks), deposition (beaches, spits). Good diagrams score well.' },
      { name: 'Glacial Processes & Landforms', section: 'Section 1 — Physical', markWeight: 8, examFrequency: 7, difficulty: 3, studyHours: 7, tip: 'Corries, arêtes, drumlins, moraines, erratics. Use Irish examples (Wicklow, Kerry). Know erosion vs deposition features.' },
      { name: 'Rock Cycle & Karst', section: 'Section 1 — Physical', markWeight: 5, examFrequency: 6, difficulty: 3, studyHours: 6, tip: 'Igneous, sedimentary, metamorphic rocks. Karst landscapes (the Burren). Know formation processes.' },
      { name: 'Regional Geography (Ireland)', section: 'Section 2 — Regional', markWeight: 8, examFrequency: 7, difficulty: 3, studyHours: 8, tip: 'Know 2 contrasting Irish regions in detail: population, economy, physical features, urbanisation.' },
      { name: 'Regional Geography (Europe)', section: 'Section 2 — Regional', markWeight: 6, examFrequency: 6, difficulty: 3, studyHours: 6, tip: '2 contrasting European regions. Development, population patterns, EU impact.' },
      { name: 'Geoecology', section: 'Section 4 — Option', markWeight: 10, examFrequency: 10, difficulty: 3, studyHours: 10, tip: 'Most popular option. Soils, biomes, ecosystems, human impact. Appears every year for Geoecology students. Know soil types and biome characteristics.' },
      { name: 'Population & Urbanisation', section: 'Elective 5 / Regional', markWeight: 7, examFrequency: 7, difficulty: 2, studyHours: 6, tip: 'Population change, migration, urbanisation patterns. Use census data and case studies. Know push-pull factors.' },
      { name: 'Economic Activities', section: 'Elective 4', markWeight: 6, examFrequency: 6, difficulty: 3, studyHours: 6, tip: 'Primary (farming, fishing), secondary (industry), tertiary (services). Location factors, globalisation impact.' },
      { name: 'Short Questions (Breadth)', section: 'Part 1', markWeight: 16, examFrequency: 10, difficulty: 2, studyHours: 8, tip: '10 of 12 questions, 8 marks each = 80 marks. Cover the entire course. Quick factual recall — maps, diagrams, definitions.' },
    ],
  },

  // ═══════════════════════════════════════════════════════════════════════════
  // CHEMISTRY
  // ═══════════════════════════════════════════════════════════════════════════
  {
    subject: 'Chemistry',
    totalMarks: 400,
    papers: [
      { name: 'One Paper', marks: 400, duration: '3h' },
    ],
    keyAdvice: 'Answer 8 of 11 questions (50 marks each, at least 2 from Section A). Titration (Q1) is guaranteed and should be automatic marks. Organic Chemistry appears every year. Master 9-10 topics and you\'ll always have 8 strong answers. The 2026 paper is the LAST under the current syllabus.',
    topics: [
      { name: 'Titrations (Volumetric Analysis)', section: 'Section A (Q1)', markWeight: 12.5, examFrequency: 10, difficulty: 3, studyHours: 10, tip: 'Guaranteed every year. Acid-base, redox, back titration. Practise calculations until automatic. Show all working. Free marks if prepared.' },
      { name: 'Organic Chemistry', section: 'Section A & B', markWeight: 15, examFrequency: 10, difficulty: 4, studyHours: 14, tip: 'Hydrocarbons, alcohols, aldehydes, ketones, carboxylic acids, esters, polymers. Annual appearance. Preparation experiment in Section A. Learn reaction types and functional group tests.' },
      { name: 'Acids & Bases', section: 'Section B', markWeight: 12.5, examFrequency: 9, difficulty: 3, studyHours: 10, tip: 'Arrhenius, Bronsted-Lowry definitions, pH calculations, strong vs weak, buffer solutions. Near-annual. pH calculations are essential.' },
      { name: 'Chemical Equilibrium', section: 'Section B', markWeight: 10, examFrequency: 9, difficulty: 4, studyHours: 10, tip: 'Le Chatelier\'s, Kc calculations, industrial processes (Haber, Contact). Very frequent. Kc calculation is almost guaranteed.' },
      { name: 'Rates of Reaction', section: 'Section B', markWeight: 10, examFrequency: 7, difficulty: 3, studyHours: 7, tip: 'Factors affecting rate, collision theory, catalysts. Longest gap since 2023 — very likely for 2026. Know experiments and rate graphs.' },
      { name: 'Atomic Structure & Bonding', section: 'Section B', markWeight: 10, examFrequency: 8, difficulty: 3, studyHours: 10, tip: 'Electron configuration, periodic trends, ionic/covalent bonding, VSEPR shapes, intermolecular forces. Regular. Know shapes and bonding explanations.' },
      { name: 'Stoichiometry', section: 'Across all questions', markWeight: 8, examFrequency: 9, difficulty: 3, studyHours: 8, tip: 'Mole concept, formulae, balancing, % composition, limiting reagent, % yield. Tested within other questions. Practise mole calculations.' },
      { name: 'Thermochemistry', section: 'Section A & B', markWeight: 8, examFrequency: 7, difficulty: 3, studyHours: 7, tip: 'Heats of reaction, Hess\'s Law, bond energies, calorimetry. Can appear in Section A experiments or Section B theory.' },
      { name: 'Electrochemistry', section: 'Section B', markWeight: 8, examFrequency: 6, difficulty: 4, studyHours: 8, tip: 'Oxidation states, electrochemical cells, electrolysis, standard electrode potentials. Less frequent but worth high marks when it appears.' },
      { name: 'Water Chemistry & Environmental', section: 'Section B', markWeight: 5, examFrequency: 5, difficulty: 2, studyHours: 5, tip: 'Water treatment, hardness, dissolved oxygen, atmospheric chemistry. Less frequent. Good backup topic.' },
    ],
  },

  // ═══════════════════════════════════════════════════════════════════════════
  // PHYSICS
  // ═══════════════════════════════════════════════════════════════════════════
  {
    subject: 'Physics',
    totalMarks: 400,
    papers: [
      { name: 'One Paper', marks: 400, duration: '3h' },
    ],
    keyAdvice: 'Section A (experiments) is 120 marks — these are the most predictable marks on the paper. Learn all 25 experiments: diagram, method, calculation, precautions. For Section B, Mechanics and Electricity always appear. Each topic has a characteristic question style — practise past papers to learn the patterns.',
    topics: [
      { name: 'Mandatory Experiments', section: 'Section A', markWeight: 30, examFrequency: 10, difficulty: 2, studyHours: 12, tip: '3 of 4 questions, 40 marks each = 120 marks. 25 experiments to know. Always: labelled diagram, method, calculations, graph drawing, precautions. Most predictable marks on the paper.' },
      { name: 'Mechanics', section: 'Section B', markWeight: 14, examFrequency: 10, difficulty: 4, studyHours: 14, tip: 'Newton\'s laws, momentum, energy, circular motion, SHM, gravity. At least 1 full Section B question. Know derivations and problem-solving techniques.' },
      { name: 'Electricity (Static & Current)', section: 'Section B', markWeight: 14, examFrequency: 9, difficulty: 4, studyHours: 14, tip: 'Coulomb\'s law, Ohm\'s law, circuits, Kirchhoff\'s laws, capacitance, semiconductors. Regular appearance. Circuit analysis is essential.' },
      { name: 'Electromagnetism', section: 'Section B', markWeight: 10, examFrequency: 8, difficulty: 4, studyHours: 10, tip: 'Magnetic fields, electromagnetic induction, Faraday\'s law, Lenz\'s law, transformers, AC theory. Regular. Know the right-hand rule and induced EMF calculations.' },
      { name: 'Waves & Sound', section: 'Section B', markWeight: 8, examFrequency: 7, difficulty: 3, studyHours: 8, tip: 'Wave motion, diffraction, interference, standing waves, Doppler effect, harmonics. Predicted as likely for 2026. Know frequency-wavelength relationships.' },
      { name: 'Light & Optics', section: 'Section B', markWeight: 8, examFrequency: 7, difficulty: 3, studyHours: 8, tip: 'Reflection, refraction, Snell\'s law, lenses, diffraction gratings, spectra. Know ray diagrams and calculations.' },
      { name: 'Heat', section: 'Section B', markWeight: 7, examFrequency: 6, difficulty: 3, studyHours: 7, tip: 'Specific heat capacity, latent heat, gas laws, heat transfer, U-values. Know calorimetry calculations and gas law problem-solving.' },
      { name: 'Nuclear / Modern Physics', section: 'Section B', markWeight: 8, examFrequency: 8, difficulty: 3, studyHours: 8, tip: 'Photoelectric effect, Bohr model, radioactivity, half-life, E=mc². High frequency. Know photoelectric equation and half-life calculations.' },
      { name: 'Particle Physics (Option)', section: 'Section B (Q13)', markWeight: 7, examFrequency: 10, difficulty: 4, studyHours: 8, tip: 'Quarks, leptons, hadrons, fundamental forces, accelerators. OR Applied Electricity. Near-guaranteed. Choose the option you know better.' },
    ],
  },


  // ═══════════════════════════════════════════════════════════════════════════
  // IRISH
  // ═══════════════════════════════════════════════════════════════════════════
  {
    subject: 'Irish',
    totalMarks: 600,
    papers: [
      { name: 'Oral Exam (Scrúdú Béil)', marks: 240, duration: '15m' },
      { name: 'Paper 1 — Cluastuiscint & Ceapadóireacht', marks: 160, duration: '2h 20m' },
      { name: 'Paper 2 — Léamhthuiscint & Litríocht', marks: 200, duration: '2h 50m' },
    ],
    keyAdvice: 'The oral is 40% of your grade — it\'s by far the biggest component. Focus on Sraith Pictiúr (80 marks) and Comhrá (120 marks). For Paper 1, the Ceapadóireacht (essay) is worth 100 marks — use simpler Irish you can control. Paper 2 literature is predictable since it\'s based on prescribed texts.',
    topics: [
      { name: 'Comhrá (Oral Conversation)', section: 'Oral Exam', markWeight: 20, examFrequency: 10, difficulty: 3, studyHours: 15, tip: 'Worth 120 marks. Covers personal topics, school, hobbies, current affairs. Practise speaking Irish daily — even 10 minutes helps.' },
      { name: 'Sraith Pictiúr (Picture Series)', section: 'Oral Exam', markWeight: 13, examFrequency: 10, difficulty: 3, studyHours: 12, tip: 'Worth 80 marks. 20 picture sequences to prepare. Learn key vocabulary and phrases for each. Tell the story naturally, don\'t just list events.' },
      { name: 'Ceapadóireacht (Essay)', section: 'Paper 1', markWeight: 17, examFrequency: 10, difficulty: 4, studyHours: 14, tip: 'Worth 100 marks. Personal essay, article, speech, or story. Use simpler Irish that you fully understand rather than memorised complex phrases.' },
      { name: 'Cluastuiscint (Listening)', section: 'Paper 1', markWeight: 10, examFrequency: 10, difficulty: 3, studyHours: 8, tip: 'Worth 60 marks. Fógraí, comhráite, nuacht. Listen to TG4/Raidió na Gaeltachta regularly to improve comprehension speed.' },
      { name: 'Léamhthuiscint (Reading Comprehension)', section: 'Paper 2', markWeight: 17, examFrequency: 10, difficulty: 3, studyHours: 10, tip: 'Worth 100 marks (2 passages at 50 each). Themes: Gaeltacht, culture, social issues, youth. Define key words from the question in your answer.' },
      { name: 'Prós Ainmnithe (Prescribed Prose)', section: 'Paper 2', markWeight: 5, examFrequency: 10, difficulty: 4, studyHours: 8, tip: 'Worth 30 marks. Based on prescribed stories/drama (e.g. An Triail). Know characters, themes, and key quotes.' },
      { name: 'Filíocht (Poetry)', section: 'Paper 2', markWeight: 5, examFrequency: 10, difficulty: 4, studyHours: 8, tip: 'Worth 30 marks. Study prescribed poems — themes, imagery, language techniques. Quote directly from the poems.' },
      { name: 'Litríocht Bhreise (Additional Literature)', section: 'Paper 2', markWeight: 7, examFrequency: 10, difficulty: 3, studyHours: 6, tip: 'Worth 40 marks. Choose prescribed text or unseen poem. If you know your texts well, the prescribed option is safer.' },
      { name: 'Léamh Filíochta (Poetry Reading)', section: 'Oral Exam', markWeight: 5, examFrequency: 10, difficulty: 2, studyHours: 4, tip: 'Worth 30 marks in the oral. Read with expression and correct pronunciation. Practise reading aloud regularly.' },
    ],
  },

  // ═══════════════════════════════════════════════════════════════════════════
  // FRENCH
  // ═══════════════════════════════════════════════════════════════════════════
  {
    subject: 'French',
    totalMarks: 400,
    papers: [
      { name: 'Oral Exam', marks: 100, duration: '12-15m' },
      { name: 'Written Paper', marks: 220, duration: '2h 30m' },
      { name: 'Aural (Listening)', marks: 80, duration: '40m' },
    ],
    keyAdvice: 'Reading comprehensions are worth 30% of your final grade — more than the oral. For written expression, learn flexible connector phrases (cependant, en revanche, d\'une part... d\'autre part) rather than topic-specific vocabulary alone. The oral is 25% — practise speaking consistently.',
    topics: [
      { name: 'Reading Comprehension 1 (Journalistic)', section: 'Written — Section A', markWeight: 15, examFrequency: 10, difficulty: 3, studyHours: 10, tip: 'Worth 60 marks. Topical passage on social issues, environment, culture. Read carefully — marks for inference and specific detail.' },
      { name: 'Reading Comprehension 2 (Literary)', section: 'Written — Section A', markWeight: 15, examFrequency: 10, difficulty: 4, studyHours: 10, tip: 'Worth 60 marks. Literary extract. Focus on understanding tone, character, and context. Answer precisely in French.' },
      { name: 'Written Expression (Q1 — Compulsory)', section: 'Written — Section B', markWeight: 10, examFrequency: 10, difficulty: 3, studyHours: 8, tip: 'Worth 40 marks. Linked to comprehension passages. ~90 words. Marks split equally between communication and language quality.' },
      { name: 'Written Expression (Q2-4 — Choice)', section: 'Written — Section B', markWeight: 15, examFrequency: 10, difficulty: 4, studyHours: 12, tip: 'Answer 2 of 3. Journal intime, letter, opinion piece, dialogue. ~75 words each. Have templates ready for each format.' },
      { name: 'Aural Comprehension', section: 'Aural', markWeight: 20, examFrequency: 10, difficulty: 3, studyHours: 10, tip: 'Worth 80 marks. 5 sections. Section V (news) is only heard twice — be extra alert. Practise with authentic French audio weekly.' },
      { name: 'Oral — General Conversation', section: 'Oral Exam', markWeight: 15, examFrequency: 10, difficulty: 3, studyHours: 12, tip: 'Worth ~60 marks. Personal topics, school, hobbies, future plans, current affairs. Examiners reward spontaneity over memorised blocks.' },
      { name: 'Oral — Le Document', section: 'Oral Exam', markWeight: 10, examFrequency: 10, difficulty: 3, studyHours: 6, tip: 'Worth ~40 marks. Bring a picture, article, or project. Discuss for ~2 minutes then answer follow-up questions. Choose something you can discuss confidently.' },
    ],
  },

  // ═══════════════════════════════════════════════════════════════════════════
  // GERMAN
  // ═══════════════════════════════════════════════════════════════════════════
  {
    subject: 'German',
    totalMarks: 400,
    papers: [
      { name: 'Oral Exam (Mündliche Prüfung)', marks: 100, duration: '15m' },
      { name: 'Written Paper', marks: 220, duration: '2h 30m' },
      { name: 'Listening (Hörverständnis)', marks: 80, duration: '40m' },
    ],
    keyAdvice: 'Reading comprehension carries the most written marks (120/220). For the oral, prepare all 7 conversation themes thoroughly — the Allgemeines Gespräch alone is 40% of the oral mark. Learn letter-writing conventions for Schriftliche Produktion.',
    topics: [
      { name: 'Reading Comprehension I (Literary)', section: 'Written Paper', markWeight: 15, examFrequency: 10, difficulty: 4, studyHours: 10, tip: 'Worth 60 marks. Literary text with comprehension questions. Read the passage twice before answering. Pay attention to context clues.' },
      { name: 'Reading Comprehension II (Journalistic)', section: 'Written Paper', markWeight: 15, examFrequency: 10, difficulty: 3, studyHours: 10, tip: 'Worth 60 marks. Newspaper/magazine article on current topics. Themes: family, school, environment, technology, travel.' },
      { name: 'Applied Grammar (Angewandte Grammatik)', section: 'Written Paper', markWeight: 6, examFrequency: 10, difficulty: 4, studyHours: 10, tip: 'Worth 25 marks. Tests verb conjugation, cases, prepositions, word order, conjunctions. Practise these systematically.' },
      { name: 'Opinion Piece (Äußerung zum Thema)', section: 'Written Paper', markWeight: 6, examFrequency: 10, difficulty: 3, studyHours: 6, tip: 'Worth 25 marks. Choose a or b. Express your opinion on a topic linked to the comprehensions. Clear structure: intro, argument, conclusion.' },
      { name: 'Written Production (Schriftliche Produktion)', section: 'Written Paper', markWeight: 12.5, examFrequency: 10, difficulty: 4, studyHours: 10, tip: 'Worth 50 marks. Letter response or stimulus-based writing. Learn formal and informal letter conventions (opening/closing phrases).' },
      { name: 'Listening Comprehension', section: 'Hörverständnis', markWeight: 20, examFrequency: 10, difficulty: 3, studyHours: 10, tip: 'Worth 80 marks. 4 sections: conversations, interviews, announcements, news. Practise with varied German accents weekly.' },
      { name: 'Oral — General Conversation', section: 'Oral Exam', markWeight: 10, examFrequency: 10, difficulty: 3, studyHours: 10, tip: 'Worth 40 marks. 7 themes: yourself, where you live, school, language learning, future plans, hobbies, time in a German-speaking country.' },
      { name: 'Oral — Picture Sequence & Role Play', section: 'Oral Exam', markWeight: 15, examFrequency: 10, difficulty: 3, studyHours: 8, tip: 'Worth 60 marks combined. Bildbeschreibung (30) + Rollenspiel (30). Practise narrating events and responding to prompts spontaneously.' },
    ],
  },

  // ═══════════════════════════════════════════════════════════════════════════
  // SPANISH
  // ═══════════════════════════════════════════════════════════════════════════
  {
    subject: 'Spanish',
    totalMarks: 400,
    papers: [
      { name: 'Oral Exam', marks: 100, duration: '15m' },
      { name: 'Written Paper', marks: 220, duration: '2h 30m' },
      { name: 'Listening (Comprensión Auditiva)', marks: 80, duration: '40m' },
    ],
    keyAdvice: 'The Opinion Piece (Section B) is worth 100 marks — the single highest-value written question. Have a strong intro/conclusion template and 15-20 vocabulary items per topic. The oral General Conversation is 70/100 marks — prepare for tense-based questioning (present → past → future).',
    topics: [
      { name: 'Journalistic Comprehension', section: 'Written — Section A', markWeight: 12.5, examFrequency: 10, difficulty: 3, studyHours: 10, tip: 'Worth 50 marks. Topical passage on sport, culture, environment, social issues. Read carefully and answer precisely.' },
      { name: 'Short Comprehensions', section: 'Written — Section A', markWeight: 5, examFrequency: 10, difficulty: 2, studyHours: 4, tip: 'Worth 20 marks. Information retrieval from short texts. Quick marks if you can scan efficiently.' },
      { name: 'Opinion Piece (Producción Escrita)', section: 'Written — Section B', markWeight: 25, examFrequency: 10, difficulty: 4, studyHours: 14, tip: 'Worth 100 marks — largest single question. Topics: environment, technology, sport, education, health. Have flexible intro/conclusion templates memorised.' },
      { name: 'Dialogue / Letter Writing', section: 'Written — Section C', markWeight: 7.5, examFrequency: 10, difficulty: 3, studyHours: 6, tip: 'Worth 30 marks. Choose dialogue or letter. Know formal/informal letter conventions and common dialogue structures.' },
      { name: 'Diary Entry / Note', section: 'Written — Section C', markWeight: 5, examFrequency: 10, difficulty: 2, studyHours: 4, tip: 'Worth 20 marks. Short functional writing. Learn diary entry format and common expressions for describing daily events.' },
      { name: 'Listening Comprehension', section: 'Comprensión Auditiva', markWeight: 20, examFrequency: 10, difficulty: 3, studyHours: 10, tip: 'Worth 80 marks. Weather vocabulary appears every single year — learn it. Mix of conversations, announcements, radio extracts.' },
      { name: 'Oral — General Conversation', section: 'Oral Exam', markWeight: 17.5, examFrequency: 10, difficulty: 3, studyHours: 12, tip: 'Worth 70 marks. Examiner tests tenses in order: present, past, future/conditional. Prepare thoroughly for all personal topics.' },
      { name: 'Oral — Role Play', section: 'Oral Exam', markWeight: 7.5, examFrequency: 10, difficulty: 3, studyHours: 6, tip: 'Worth 30 marks. 5 role plays prepared; examiner picks 1. Respond naturally to prompts — don\'t just recite memorised answers.' },
    ],
  },

  // ═══════════════════════════════════════════════════════════════════════════
  // ITALIAN
  // ═══════════════════════════════════════════════════════════════════════════
  {
    subject: 'Italian',
    totalMarks: 400,
    papers: [
      { name: 'Oral Exam', marks: 100, duration: '12-15m' },
      { name: 'Written Paper (incl. Aural)', marks: 300, duration: '2h 30m' },
    ],
    keyAdvice: 'Same structure as other modern languages. The journalistic comprehension alone is worth 15% of your overall grade. The long composition (50 marks) is the highest-value single writing task. Two prescribed literary texts are studied — know them thoroughly.',
    topics: [
      { name: 'Journalistic Comprehension', section: 'Written — Reading', markWeight: 15, examFrequency: 10, difficulty: 3, studyHours: 10, tip: 'Worth ~60 marks. Unseen newspaper/magazine article. 5 questions — 4 in Italian, 1 in English. Read the passage carefully twice.' },
      { name: 'Literary Comprehension', section: 'Written — Reading', markWeight: 15, examFrequency: 10, difficulty: 4, studyHours: 10, tip: 'Worth ~60 marks. Passage from a prescribed novel. Know your 2 prescribed texts thoroughly — characters, themes, key vocabulary.' },
      { name: 'Written Expression (Short Tasks)', section: 'Written — Production', markWeight: 12.5, examFrequency: 10, difficulty: 3, studyHours: 8, tip: 'Worth ~50 marks combined. Opinion piece linked to journalistic text + short letter/diary entry. Have templates ready.' },
      { name: 'Written Expression (Long Composition)', section: 'Written — Production', markWeight: 12.5, examFrequency: 10, difficulty: 4, studyHours: 10, tip: 'Worth ~50 marks. Formal letter or essay. The highest single writing mark. Plan your structure before writing.' },
      { name: 'Aural Comprehension', section: 'Aural', markWeight: 20, examFrequency: 10, difficulty: 3, studyHours: 10, tip: 'Worth 80 marks. Recorded Italian passages with comprehension questions. Practise with authentic Italian audio regularly.' },
      { name: 'Oral Exam', section: 'Oral', markWeight: 25, examFrequency: 10, difficulty: 3, studyHours: 12, tip: 'Worth 100 marks. General conversation + topic card + picture sequence. Consistent speaking practice is critical — aim for natural fluency.' },
    ],
  },

  // ═══════════════════════════════════════════════════════════════════════════
  // JAPANESE
  // ═══════════════════════════════════════════════════════════════════════════
  {
    subject: 'Japanese',
    totalMarks: 400,
    papers: [
      { name: 'Oral Exam', marks: 100, duration: '10m' },
      { name: 'Written Paper (incl. Aural)', marks: 300, duration: '2h 30m' },
    ],
    keyAdvice: 'Japanese is ab initio (pre-A1/A1 level) — the expected standard is lower than other languages but the writing systems add complexity. Master all hiragana and katakana first. Reading comprehension is the highest-weighted component at 30%. Learn all ~100 prescribed kanji.',
    topics: [
      { name: 'Reading Comprehension', section: 'Written Paper', markWeight: 30, examFrequency: 10, difficulty: 4, studyHours: 14, tip: 'Worth 120 marks — highest component. Signs, menus, timetables, letters, simplified articles. Kanji recognition tested every year. Practise varied text types.' },
      { name: 'Writing', section: 'Written Paper', markWeight: 25, examFrequency: 10, difficulty: 4, studyHours: 12, tip: 'Worth 100 marks. Letters, messages, short compositions. Respond to written/visual stimuli. Correct hiragana/katakana/kanji usage is essential.' },
      { name: 'Aural Comprehension', section: 'Written Paper', markWeight: 20, examFrequency: 10, difficulty: 3, studyHours: 10, tip: 'Worth 80 marks. Conversations, announcements, descriptions. Practise listening to spoken Japanese at natural pace.' },
      { name: 'Oral — General Conversation', section: 'Oral Exam', markWeight: 10, examFrequency: 10, difficulty: 3, studyHours: 8, tip: 'Personal topics, interests, school. Prepare set phrases for common conversation topics. Natural flow matters.' },
      { name: 'Oral — Topic Card & Picture Comparison', section: 'Oral Exam', markWeight: 15, examFrequency: 10, difficulty: 3, studyHours: 8, tip: 'Choose a topic card and discuss it, then compare two picture sets. Practise describing and comparing in Japanese.' },
    ],
  },

  // ═══════════════════════════════════════════════════════════════════════════
  // APPLIED MATHS
  // ═══════════════════════════════════════════════════════════════════════════
  {
    subject: 'Applied Maths',
    totalMarks: 500,
    papers: [
      { name: 'Written Examination', marks: 400, duration: '2h 30m' },
      { name: 'Modelling Project', marks: 100, duration: 'Coursework' },
    ],
    keyAdvice: 'Answer 8 of 10 questions (50 marks each). The Modelling Project is 20% — free marks if you follow the modelling cycle clearly. Differential Equations and the new Network/Graph questions are examined regularly. Start with your strongest topics. Integration skills are essential across multiple question types.',
    topics: [
      { name: 'Modelling Project', section: 'Coursework', markWeight: 20, examFrequency: 10, difficulty: 3, studyHours: 15, tip: 'Worth 100 marks (20%). Follow the modelling cycle: understand, assume, model, analyse, interpret. Invest serious time in this — it\'s done before the exam.' },
      { name: 'Linear Motion (SUVAT)', section: 'Written (Q1)', markWeight: 10, examFrequency: 9, difficulty: 3, studyHours: 8, tip: 'SUVAT equations, motion on inclined planes with friction. Reliable question. Draw diagrams and resolve forces carefully.' },
      { name: 'Relative Velocity', section: 'Written (Q2)', markWeight: 10, examFrequency: 9, difficulty: 4, studyHours: 10, tip: 'Relative motion, shortest distance, interception problems. Use vector triangles and velocity diagrams. Practise different problem types.' },
      { name: 'Projectiles', section: 'Written (Q3)', markWeight: 10, examFrequency: 9, difficulty: 4, studyHours: 10, tip: 'Range, max height, angle of projection, inclined plane projectiles. Inclined plane variants are challenging — practise these specifically.' },
      { name: 'Newton\'s Laws & Connected Particles', section: 'Written (Q4)', markWeight: 10, examFrequency: 10, difficulty: 3, studyHours: 10, tip: 'Force, acceleration, tension, pulleys, wedges. Draw free body diagrams for every particle. Apply F=ma systematically.' },
      { name: 'Impacts & Collisions', section: 'Written (Q5)', markWeight: 10, examFrequency: 8, difficulty: 4, studyHours: 10, tip: 'Direct and oblique collisions, coefficient of restitution, Newton\'s Experimental Law. Oblique collisions are perennially challenging.' },
      { name: 'Circular Motion', section: 'Written (Q6)', markWeight: 10, examFrequency: 8, difficulty: 4, studyHours: 10, tip: 'Horizontal/vertical circles, conical pendulum, banked tracks. Know when to use mv²/r and resolve forces towards the centre.' },
      { name: 'Statics & SHM', section: 'Written (Q7)', markWeight: 10, examFrequency: 7, difficulty: 4, studyHours: 10, tip: 'Equilibrium, moments, Hooke\'s Law, SHM. Take moments about the point with the most unknowns to simplify.' },
      { name: 'Differential Equations', section: 'Written (Q9)', markWeight: 10, examFrequency: 9, difficulty: 5, studyHours: 12, tip: '1st and 2nd order, modelling rates of change, population, cooling. Know separation of variables, integrating factors, and complementary functions.' },
      { name: 'Networks, Graphs & Optimal Paths', section: 'Written (Q10)', markWeight: 10, examFrequency: 8, difficulty: 4, studyHours: 10, tip: 'New syllabus topic. Adjacency matrices, dynamic programming, critical path analysis. Don\'t neglect this — it appears regularly now.' },
    ],
  },

  // ═══════════════════════════════════════════════════════════════════════════
  // COMPUTER SCIENCE
  // ═══════════════════════════════════════════════════════════════════════════
  {
    subject: 'Computer Science',
    totalMarks: 300,
    papers: [
      { name: 'Written/Practical Exam', marks: 210, duration: '2h 30m' },
      { name: 'Coursework Project', marks: 90, duration: 'Coursework' },
    ],
    keyAdvice: 'Section C (programming, 80 marks) is the biggest single mark earner — practise Python coding extensively. The coursework project is 30% — invest heavily in the artefact, report, and video. For Section A, be precise with definitions and show all working for binary/logic.',
    topics: [
      { name: 'Coursework Project', section: 'Coursework', markWeight: 30, examFrequency: 10, difficulty: 4, studyHours: 20, tip: 'Worth 90 marks (30%). Create a computational artefact in Python/JS responding to SEC brief. Report + video. Start early and iterate.' },
      { name: 'Programming (Python)', section: 'Section C', markWeight: 27, examFrequency: 10, difficulty: 4, studyHours: 18, tip: 'Worth 80 marks. Modify/extend provided Python code, write functions, test, debug. The more you code and debug, the stronger you get.' },
      { name: 'Short-Answer Theory', section: 'Section A', markWeight: 20, examFrequency: 10, difficulty: 3, studyHours: 10, tip: 'Worth 60 marks (12 questions). Definitions, binary conversions, logic gates, code snippet analysis. Be precise and show working.' },
      { name: 'Long-Answer Theory', section: 'Section B', markWeight: 23, examFrequency: 10, difficulty: 3, studyHours: 10, tip: 'Worth 70 marks (3 questions). Ethics, problem-solving scenarios, multi-part essay-style questions. Use real-world examples where relevant.' },
    ],
  },

  // ═══════════════════════════════════════════════════════════════════════════
  // AG SCIENCE (Agricultural Science)
  // ═══════════════════════════════════════════════════════════════════════════
  {
    subject: 'Ag Science',
    totalMarks: 400,
    papers: [
      { name: 'Written Exam', marks: 300, duration: '2h 30m' },
      { name: 'Individual Investigative Study (IIS)', marks: 100, duration: 'Coursework' },
    ],
    keyAdvice: 'The IIS is 25% — free marks for a thorough, well-structured investigation. The written exam has Section A (short, 100 marks) and Section B (long, 200 marks). Know your 22 mandatory experiments (SPAs) — they are directly examined. Diagrams and labelled drawings score well.',
    topics: [
      { name: 'Individual Investigative Study (IIS)', section: 'Coursework', markWeight: 25, examFrequency: 10, difficulty: 3, studyHours: 15, tip: 'Worth 100 marks (25%). Max 2,500 words. Follow SEC brief. Invest time in data collection, analysis, and evaluation — these are banked marks before the exam.' },
      { name: 'Soil Science', section: 'Section A & B', markWeight: 18, examFrequency: 10, difficulty: 3, studyHours: 12, tip: 'Formation, classification, physical/chemical/biological properties, management. Near-annual. Know soil experiments and the nitrogen cycle.' },
      { name: 'Animal Physiology & Enterprises', section: 'Section B', markWeight: 18, examFrequency: 9, difficulty: 3, studyHours: 14, tip: 'Dairy, beef, sheep enterprises. Reproduction, nutrition, health. Perennial favourite in long questions. Know production cycles.' },
      { name: 'Plant Physiology & Crop Production', section: 'Section B', markWeight: 15, examFrequency: 9, difficulty: 3, studyHours: 12, tip: 'Photosynthesis, transpiration, barley, potatoes, grassland management. Know growth stages and management practices.' },
      { name: 'Genetics & Breeding', section: 'Section A & B', markWeight: 10, examFrequency: 9, difficulty: 4, studyHours: 10, tip: 'Inheritance, crosses, genetic engineering, selective breeding. Extremely reliable exam topic. Practise genetic crosses.' },
      { name: 'Ecology & Environment', section: 'Section A & B', markWeight: 7, examFrequency: 7, difficulty: 3, studyHours: 6, tip: 'Ecosystems, nutrient cycling, sustainability, climate impact. Increasingly featured. Know food webs and energy flow.' },
      { name: 'Specified Practical Activities (SPAs)', section: 'Section A & B', markWeight: 7, examFrequency: 9, difficulty: 2, studyHours: 8, tip: '22 mandatory experiments directly examined. Know method, equipment, results, precautions for each. Easy marks if prepared.' },
    ],
  },

  // ═══════════════════════════════════════════════════════════════════════════
  // ACCOUNTING
  // ═══════════════════════════════════════════════════════════════════════════
  {
    subject: 'Accounting',
    totalMarks: 400,
    papers: [
      { name: 'One Paper', marks: 400, duration: '3h' },
    ],
    keyAdvice: 'Timing is critical. Q1 (Final Accounts, 120 marks) and Q5 (Ratios, 100 marks) appear every year — master these first. Always show workings beside figures — you score zero for correct figures with no working. Memorise all 20 ratio formulas (worth ~50 marks). Neat presentation matters.',
    topics: [
      { name: 'Final Accounts & Adjustments', section: 'Section 1 (Q1)', markWeight: 30, examFrequency: 10, difficulty: 4, studyHours: 16, tip: 'Worth 120 marks. Sole trader or company accounts with adjustments (depreciation, bad debts, prepayments, accruals). Annual. Don\'t attempt unless confident with ALL adjustments.' },
      { name: 'Interpretation of Accounts (Ratios)', section: 'Section 2 (Q5)', markWeight: 12.5, examFrequency: 10, difficulty: 3, studyHours: 10, tip: 'Worth ~100 marks (shared in Q5). Profitability, liquidity, efficiency ratios. 20 formulae to learn — highly structured and predictable.' },
      { name: 'Club Accounts', section: 'Section 2 (Q6/Q7)', markWeight: 12.5, examFrequency: 8, difficulty: 3, studyHours: 8, tip: 'Income & Expenditure account, Accumulated Fund. Regular rotation in Q6/Q7. Different format from business accounts — learn the structure.' },
      { name: 'Published Accounts', section: 'Section 2 (Q6/Q7)', markWeight: 12.5, examFrequency: 8, difficulty: 4, studyHours: 10, tip: 'Company published accounts, compliance with Companies Act. Know the specific format requirements and disclosure rules.' },
      { name: 'Incomplete Records', section: 'Section 1 or 2', markWeight: 7.5, examFrequency: 7, difficulty: 4, studyHours: 8, tip: 'Reconstruct accounts from partial records. Control accounts, margins, mark-ups. Logical working through missing figures is key.' },
      { name: 'Costing (Marginal & Job)', section: 'Section 3 (Q8)', markWeight: 10, examFrequency: 8, difficulty: 4, studyHours: 10, tip: 'Worth 80 marks. Product/job/marginal costing, overhead apportionment, FIFO. Know break-even analysis and contribution calculations.' },
      { name: 'Budgeting', section: 'Section 3 (Q9)', markWeight: 10, examFrequency: 8, difficulty: 3, studyHours: 8, tip: 'Worth 80 marks. Cash budgets, production budgets, flexible budgets. Follow the format precisely — layout earns marks.' },
      { name: 'Correction of Errors & Suspense', section: 'Section 1 (Q2-Q4)', markWeight: 5, examFrequency: 7, difficulty: 3, studyHours: 6, tip: 'Suspense account, journal entries. Know the 6 types of errors (compensating, commission, principle, etc.). Methodical approach needed.' },
    ],
  },

  // ═══════════════════════════════════════════════════════════════════════════
  // ECONOMICS
  // ═══════════════════════════════════════════════════════════════════════════
  {
    subject: 'Economics',
    totalMarks: 400,
    papers: [
      { name: 'One Paper', marks: 400, duration: '2h 30m' },
    ],
    keyAdvice: 'Master Market Structures first — it\'s the largest unit and appears every year (up to 22% of marks). Graphs alone can be worth 10-15% — practise drawing and labelling with pencil and ruler. Definitions are easy marks in Section B. Attempt all 10 short questions as best 8 count.',
    topics: [
      { name: 'Market Structures', section: 'Section B', markWeight: 18, examFrequency: 10, difficulty: 4, studyHours: 14, tip: 'Perfect competition, monopoly, monopolistic competition, oligopoly. Near-annual. Accurate graphs with labelled axes, curves, and equilibrium points are essential.' },
      { name: 'Demand, Supply & Market Equilibrium', section: 'Section A & B', markWeight: 10, examFrequency: 9, difficulty: 3, studyHours: 8, tip: 'Shifts in curves, price determination, consumer/producer surplus. Foundation for everything else — master this first.' },
      { name: 'Elasticity (PED, PES, Income, Cross)', section: 'Section A & B', markWeight: 8, examFrequency: 9, difficulty: 3, studyHours: 8, tip: 'Calculations and applications. PED is the most examined. Know the formula and how to interpret the coefficient.' },
      { name: 'National Income & Economic Growth', section: 'Section B', markWeight: 10, examFrequency: 9, difficulty: 3, studyHours: 10, tip: 'GDP, GNP, GNI, circular flow, factors affecting growth. Appears most years. Know the difference between real and nominal.' },
      { name: 'Fiscal & Monetary Policy', section: 'Section B', markWeight: 10, examFrequency: 8, difficulty: 3, studyHours: 10, tip: 'Government budgets, taxation, ECB monetary tools. Common long question. Apply theory to current Irish/EU economic policy.' },
      { name: 'International Trade & Protectionism', section: 'Section B', markWeight: 10, examFrequency: 8, difficulty: 3, studyHours: 8, tip: 'Comparative advantage, barriers to trade, balance of payments, WTO. Frequent long question. Use real-world examples.' },
      { name: 'Market Failure & Externalities', section: 'Section A & B', markWeight: 7, examFrequency: 7, difficulty: 3, studyHours: 6, tip: 'Public goods, merit goods, externalities (positive/negative), government intervention. Draw externality diagrams accurately.' },
      { name: 'Inflation & Unemployment', section: 'Section A & B', markWeight: 7, examFrequency: 7, difficulty: 3, studyHours: 6, tip: 'CPI, causes of inflation, types of unemployment, Phillips Curve. Know the Irish context for applied questions.' },
      { name: 'Short Questions (Breadth)', section: 'Section A', markWeight: 25, examFrequency: 10, difficulty: 2, studyHours: 8, tip: 'Answer 8 of 10, 100 marks total. Mix of micro and macro. Attempt all 10 for safety — best 8 are counted.' },
      { name: 'Banking & the Euro', section: 'Section A & B', markWeight: 5, examFrequency: 6, difficulty: 3, studyHours: 5, tip: 'Central Bank functions, credit creation, EU monetary system. Less frequent as standalone but appears within other topics.' },
    ],
  },

  // ═══════════════════════════════════════════════════════════════════════════
  // POLITICS & SOCIETY
  // ═══════════════════════════════════════════════════════════════════════════
  {
    subject: 'Politics & Society',
    totalMarks: 400,
    papers: [
      { name: 'Written Exam', marks: 320, duration: '2h 30m' },
      { name: 'Citizenship Project', marks: 80, duration: 'Coursework' },
    ],
    keyAdvice: 'Section C essays (200/320 of written marks) carry the most weight — start there after the quick Section A definitions. Stay informed on current affairs — topics like housing, education, technology appear frequently. Material overlaps between essay topics, so learn adaptable paragraphs.',
    topics: [
      { name: 'Citizenship Project', section: 'Coursework', markWeight: 20, examFrequency: 10, difficulty: 3, studyHours: 15, tip: 'Worth 80 marks (20%). Evaluate opportunities for action in communities. Follow the structure exactly — this is guaranteed marks before the exam.' },
      { name: 'Discursive Essays', section: 'Section C', markWeight: 50, examFrequency: 10, difficulty: 4, studyHours: 16, tip: 'Worth 200 marks (2 essays, 100 each). Choice from 6-7 questions. Cover all 4 strands. Current affairs examples strengthen every answer.' },
      { name: 'Document/Data-Based Questions', section: 'Section B', markWeight: 18.75, examFrequency: 10, difficulty: 3, studyHours: 10, tip: 'Worth 150 marks total in Section B. Analyse, compare, critique sources and data. Practise interpreting graphs and documents critically.' },
      { name: 'Short Answer Questions', section: 'Section A', markWeight: 12.5, examFrequency: 10, difficulty: 2, studyHours: 6, tip: 'Worth 50 marks. Definitions and key concepts across all 4 strands. Quick warm-up — spend max 20 minutes here.' },
    ],
  },

  // ═══════════════════════════════════════════════════════════════════════════
  // RELIGIOUS EDUCATION
  // ═══════════════════════════════════════════════════════════════════════════
  {
    subject: 'Religious Education',
    totalMarks: 400,
    papers: [
      { name: 'Written Exam', marks: 320, duration: '2h 30m' },
      { name: 'Coursework Journal', marks: 80, duration: 'Coursework' },
    ],
    keyAdvice: 'Each written question carries 80 marks — time management is critical (~35 mins per question). The coursework journal provides 80 guaranteed marks. Watch for "and" in questions — each typically signals a separate marking criterion. Treat it with the same seriousness as any other subject.',
    topics: [
      { name: 'Coursework Journal', section: 'Coursework', markWeight: 20, examFrequency: 10, difficulty: 3, studyHours: 12, tip: 'Worth 80 marks (20%). Part A (40) + Part B (40). Based on 2 designated sections from Unit 3. Thorough documentation is key.' },
      { name: 'Search for Meaning & Values (Unit 1)', section: 'Section A (Compulsory)', markWeight: 20, examFrequency: 10, difficulty: 3, studyHours: 12, tip: 'Worth 80 marks. Compulsory question. Religious and non-religious responses to meaning, faith and reason. Know key thinkers and perspectives.' },
      { name: 'Christianity: Origins & Expressions (Unit 2B)', section: 'Section B-D', markWeight: 20, examFrequency: 10, difficulty: 3, studyHours: 12, tip: 'Worth 80 marks if chosen. History, development, contemporary expressions of Christianity. Answer from 2 of the 3 sections studied.' },
      { name: 'World Religions (Unit 2C)', section: 'Section B-D', markWeight: 20, examFrequency: 10, difficulty: 3, studyHours: 12, tip: 'Worth 80 marks if chosen. Judaism, Islam, Hinduism, Buddhism. Compare beliefs, practices, and rituals across religions.' },
      { name: 'Moral Decision-Making (Unit 2D)', section: 'Section B-D', markWeight: 20, examFrequency: 10, difficulty: 3, studyHours: 10, tip: 'Worth 80 marks if chosen. Ethics, conscience, sources of moral authority. Apply moral frameworks to contemporary issues.' },
      { name: 'Unit 3 Topics (E-J)', section: 'Section E-J', markWeight: 20, examFrequency: 10, difficulty: 3, studyHours: 10, tip: 'Worth 80 marks. Answer 1 from your studied section (not coursework sections). Options include Gender, Justice & Peace, Worship, Bible, Irish Experience, Science.' },
    ],
  },

  // ═══════════════════════════════════════════════════════════════════════════
  // CLASSICAL STUDIES
  // ═══════════════════════════════════════════════════════════════════════════
  {
    subject: 'Classical Studies',
    totalMarks: 500,
    papers: [
      { name: 'Written Exam', marks: 400, duration: '2h 30m' },
      { name: 'Research Study Report', marks: 100, duration: 'Coursework' },
    ],
    keyAdvice: 'The Research Study is 20% — invest time as it\'s done before the exam. Section A (stimulus questions) is compulsory — answer everything. Question 11 (compulsory, 120 marks) is the biggest single question. Time pressure is significant — practise under timed conditions.',
    topics: [
      { name: 'Research Study Report', section: 'Coursework', markWeight: 20, examFrequency: 10, difficulty: 3, studyHours: 15, tip: 'Worth 100 marks (20%). Investigate a focused aspect of ancient Greek or Roman world. SEC brief issued early in 5th year.' },
      { name: 'Stimulus Questions (Section A)', section: 'Section A', markWeight: 40, examFrequency: 10, difficulty: 3, studyHours: 14, tip: 'Worth 200 marks. ALL questions compulsory. Respond to visual/written sources — images of artefacts, maps, literary excerpts. Know your texts and artefacts thoroughly.' },
      { name: 'Extended Essay (Q11 — Compulsory)', section: 'Section B', markWeight: 24, examFrequency: 10, difficulty: 4, studyHours: 14, tip: 'Worth 120 marks. Multi-part extended essay. Philosophy (Stoicism, Epicureanism, Plato) was the 2025 theme. Know prescribed texts deeply.' },
      { name: 'Extended Essay (Q12-15 — Choice)', section: 'Section B', markWeight: 16, examFrequency: 10, difficulty: 4, studyHours: 10, tip: 'Worth 80 marks. Choose 1 of 4. Covers: Heroes (Odyssey, Aeneid), Drama, Power & Identity (Alexander, Caesar), Gods & Humans.' },
    ],
  },

  // ═══════════════════════════════════════════════════════════════════════════
  // HOME ECONOMICS
  // ═══════════════════════════════════════════════════════════════════════════
  {
    subject: 'Home Economics',
    totalMarks: 400,
    papers: [
      { name: 'Written Exam', marks: 320, duration: '2h 30m' },
      { name: 'Food Studies Practical Coursework', marks: 80, duration: 'Coursework' },
    ],
    keyAdvice: 'Q1 (Food Science & Nutrition, 80 marks) is compulsory and the most important question. The coursework is 80 marks due in November — these are banked marks before the exam. A common mistake is attempting the wrong elective — read instructions carefully.',
    topics: [
      { name: 'Food Studies Practical Coursework', section: 'Coursework', markWeight: 20, examFrequency: 10, difficulty: 3, studyHours: 15, tip: 'Worth 80 marks (20%). Complete 4 of 5 assignments. Due November of LC year. Detailed, well-presented journal is essential.' },
      { name: 'Food Science & Nutrition (Q1)', section: 'Section B (Compulsory)', markWeight: 20, examFrequency: 10, difficulty: 4, studyHours: 14, tip: 'Worth 80 marks. Always appears. Food science experiments, nutritional terms, dietary guidelines. The single most important written question.' },
      { name: 'Resource Management & Consumer Studies', section: 'Section B (Q2-Q5)', markWeight: 12.5, examFrequency: 9, difficulty: 3, studyHours: 8, tip: 'Worth 50 marks (1 of 2 chosen from Q2-Q5). Consumer rights, household finance, technology. Know Consumer Protection Act and budget management.' },
      { name: 'Social Studies', section: 'Section B (Q2-Q5)', markWeight: 12.5, examFrequency: 9, difficulty: 3, studyHours: 8, tip: 'Worth 50 marks. Family, demographics, social change, childcare. Apply theory to contemporary Irish society.' },
      { name: 'Elective', section: 'Section C', markWeight: 20, examFrequency: 10, difficulty: 3, studyHours: 10, tip: 'Worth 80 marks. Choose from: Home Design & Management, Textiles/Fashion, or Social Studies extension. Know YOUR elective thoroughly.' },
      { name: 'Short Questions', section: 'Section A', markWeight: 15, examFrequency: 10, difficulty: 2, studyHours: 6, tip: 'Worth 60 marks (10 of 12, 6 marks each). Cover all core areas. Quick marks — spend max 20 minutes. Breadth of knowledge rewarded.' },
    ],
  },

  // ═══════════════════════════════════════════════════════════════════════════
  // CONSTRUCTION STUDIES
  // ═══════════════════════════════════════════════════════════════════════════
  {
    subject: 'Construction Studies',
    totalMarks: 600,
    papers: [
      { name: 'Written Exam', marks: 300, duration: '3h' },
      { name: 'Practical Woodwork Test', marks: 150, duration: '4h' },
      { name: 'Building Project & Portfolio', marks: 150, duration: 'Coursework' },
    ],
    keyAdvice: 'Label everything on drawings and always include key measurements. Sketches carry roughly half the marks on many questions. Q1 (building detail drawing) appears most years — practise large-scale drawings of walls, roofs, floors, foundations. The practical + project are worth 50% combined.',
    topics: [
      { name: 'Building Project & Portfolio', section: 'Coursework', markWeight: 25, examFrequency: 10, difficulty: 3, studyHours: 20, tip: 'Worth 150 marks (25%). High-quality craftsmanship and documentation. Plan early and aim for excellent finish.' },
      { name: 'Practical Woodwork Test', section: 'Practical Exam', markWeight: 25, examFrequency: 10, difficulty: 3, studyHours: 15, tip: 'Worth 150 marks (25%). In-school May exam (~4 hours). Practise workshop skills under timed conditions.' },
      { name: 'Building Detail Drawing (Q1)', section: 'Written (Compulsory)', markWeight: 10, examFrequency: 10, difficulty: 3, studyHours: 12, tip: 'Worth 60 marks. Most commonly: walls, roofs, floors, foundations, doors, timber frame. Label everything with measurements.' },
      { name: 'Walls, Floors & Roofs', section: 'Written', markWeight: 10, examFrequency: 9, difficulty: 3, studyHours: 10, tip: 'Core construction elements. Know cavity walls, flat/pitched roofs, ground/suspended floors. Diagrams with correct dimensions score well.' },
      { name: 'Site Safety & Redesign', section: 'Written (Q2-Q3)', markWeight: 10, examFrequency: 8, difficulty: 2, studyHours: 6, tip: 'Q2 often covers site safety culture. Q3 typically a dwelling redesign with front view and floor plan. Relatively accessible marks.' },
      { name: 'Services, Insulation & Sustainability', section: 'Written', markWeight: 10, examFrequency: 7, difficulty: 3, studyHours: 8, tip: 'Plumbing, heating, drainage, U-values, sound/light insulation, passive houses. Increasingly important. Know BER ratings.' },
      { name: 'Doors, Windows, Stairs & Finishes', section: 'Written', markWeight: 10, examFrequency: 7, difficulty: 3, studyHours: 8, tip: 'Fireplaces, windows, doors, stairs, plastering, painting. Rotate through the written paper. Detailed cross-section drawings score well.' },
    ],
  },

  // ═══════════════════════════════════════════════════════════════════════════
  // ENGINEERING
  // ═══════════════════════════════════════════════════════════════════════════
  {
    subject: 'Engineering',
    totalMarks: 600,
    papers: [
      { name: 'Written Exam', marks: 300, duration: '3h' },
      { name: 'Day Practical Exam', marks: 150, duration: '6h' },
      { name: 'Workshop Project', marks: 150, duration: 'Coursework' },
    ],
    keyAdvice: 'The Day Practical (25%) and Workshop Project (25%) are major differentiators — 50% of your grade is practical work. Q1 short questions are reliable marks — revise definitions and formulae. Past papers are essential as question formats are very consistent year to year.',
    topics: [
      { name: 'Workshop Project', section: 'Coursework', markWeight: 25, examFrequency: 10, difficulty: 3, studyHours: 20, tip: 'Worth 150 marks (25%). Plan early, aim for high-quality finish. Quality of craftsmanship is critical.' },
      { name: 'Day Practical Exam', section: 'Practical Exam', markWeight: 25, examFrequency: 10, difficulty: 4, studyHours: 15, tip: 'Worth 150 marks (25%). ~6 hours in-school. Fitting, turning, welding under timed conditions. Practise workshop skills extensively.' },
      { name: 'Short Questions (Q1)', section: 'Written (Compulsory)', markWeight: 8, examFrequency: 10, difficulty: 2, studyHours: 8, tip: 'Worth 50 marks. Section A (short-answer) + Section B (all parts). Definitions, formulae, concise engineering concepts. Reliable marks.' },
      { name: 'Workshop Processes', section: 'Written (Q2-Q8)', markWeight: 12, examFrequency: 9, difficulty: 3, studyHours: 10, tip: 'Turning, milling, welding (MIG, TIG, oxy-acetylene, arc), forging, fitting, sheet metalwork, casting. Know process steps and safety procedures.' },
      { name: 'Materials & Heat Treatment', section: 'Written (Q2-Q8)', markWeight: 10, examFrequency: 9, difficulty: 3, studyHours: 10, tip: 'Properties of metals, ferrous/non-ferrous, crystal structure. Hardening, tempering, annealing, case hardening. Know specific temperatures and processes.' },
      { name: 'Mechanisms (Cams, Gears, Linkages)', section: 'Written (Q2-Q8)', markWeight: 10, examFrequency: 8, difficulty: 4, studyHours: 10, tip: 'Cams and followers, gear trains, rack & pinion, worm/wormwheel, bevel, crank and slider. Know gear ratio calculations and cam profiles.' },
      { name: 'Engineering Drawing & Design', section: 'Written (Q2-Q8)', markWeight: 10, examFrequency: 7, difficulty: 3, studyHours: 8, tip: 'Engineering drawing conventions, design questions. Neat, accurate drawings with proper annotations score well.' },
    ],
  },

  // ═══════════════════════════════════════════════════════════════════════════
  // DCG (Design and Communication Graphics)
  // ═══════════════════════════════════════════════════════════════════════════
  {
    subject: 'DCG',
    totalMarks: 400,
    papers: [
      { name: 'Terminal Drawing Exam', marks: 240, duration: '3h' },
      { name: 'Student Assignment (incl. CAD)', marks: 160, duration: 'Coursework' },
    ],
    keyAdvice: 'The student assignment (40%) is huge — start early, demonstrate strong CAD skills, and present work professionally. Section A short questions are the most accessible marks (attempt all 4, best 3 count). Master Plane and Descriptive Geometry as the backbone of Sections A and B.',
    topics: [
      { name: 'Student Assignment (CAD)', section: 'Coursework', markWeight: 40, examFrequency: 10, difficulty: 4, studyHours: 20, tip: 'Worth 160 marks (40%). Design-based project with research, development, and CAD modelling. Start early and demonstrate strong technical skills.' },
      { name: 'Core Short Questions (Section A)', section: 'Section A', markWeight: 15, examFrequency: 10, difficulty: 3, studyHours: 10, tip: 'Worth 60 marks (best 3 of 4, 20 each). Plane Geometry, Descriptive Geometry constructions. Attempt all 4 — your best 3 count.' },
      { name: 'Core Long Questions (Section B)', section: 'Section B', markWeight: 22.5, examFrequency: 10, difficulty: 4, studyHours: 14, tip: 'Worth 90 marks (best 2 of 3, 45 each). Projections, conic sections, tangent geometry, loci. Attempt all 3 — best 2 count.' },
      { name: 'Applied Graphics (Section C)', section: 'Section C', markWeight: 22.5, examFrequency: 10, difficulty: 4, studyHours: 14, tip: 'Worth 90 marks (2 of 5, 45 each). Choose from your studied options: Dynamic Mechanisms, Structural Forms, Surface Geometry, Assemblies, Communication of Design.' },
    ],
  },

  // ═══════════════════════════════════════════════════════════════════════════
  // TECHNOLOGY
  // ═══════════════════════════════════════════════════════════════════════════
  {
    subject: 'Technology',
    totalMarks: 400,
    papers: [
      { name: 'Written Exam', marks: 400, duration: '3h' },
      { name: 'Design & Make Project', marks: 0, duration: 'Coursework (50% of overall)' },
    ],
    keyAdvice: 'The Design & Make Project is worth 50% of your overall grade — the artefact must demonstrate design skills, and the portfolio should document the full process. Section C long questions (240 marks) carry the most weight on the written paper. Cover both core and your 2 chosen options.',
    topics: [
      { name: 'Design & Make Project', section: 'Coursework', markWeight: 50, examFrequency: 10, difficulty: 4, studyHours: 25, tip: 'Worth 50% of overall grade. Artefact + design portfolio/folder. Document the full design process thoroughly. Quality of both counts.' },
      { name: 'Short Questions (Section A)', section: 'Section A', markWeight: 12.5, examFrequency: 10, difficulty: 2, studyHours: 8, tip: 'Worth 100 marks (5 of 6, 20 each). Cover all core topics. Quickest marks on the paper — revise broadly.' },
      { name: 'Practical Activities (Section B)', section: 'Section B', markWeight: 7.5, examFrequency: 10, difficulty: 3, studyHours: 6, tip: 'Worth 60 marks (2 of 3, 30 each). Practical knowledge questions. Know materials, tools, and processes.' },
      { name: 'Long Questions (Section C)', section: 'Section C', markWeight: 30, examFrequency: 10, difficulty: 4, studyHours: 14, tip: 'Worth 240 marks (4 of 6, 60 each). Structures, mechanisms, energy, electronics, materials, design. Practise structured, detailed answers.' },
    ],
  },

  // ═══════════════════════════════════════════════════════════════════════════
  // ART
  // ═══════════════════════════════════════════════════════════════════════════
  {
    subject: 'Art',
    totalMarks: 400,
    papers: [
      { name: 'Practical Coursework (Artefact A)', marks: 200, duration: '12-week project' },
      { name: 'Invigilated Practical (Artefact B)', marks: 80, duration: '5h' },
      { name: 'Written Exam (Visual Studies)', marks: 120, duration: '2h 30m' },
    ],
    keyAdvice: 'Under the new spec (2025+), coursework is 50% — plan your artefact carefully and maintain a detailed Visual Journal. Both artefacts must relate to the same SEC stimulus. The written exam (30%) covers art history, appreciation, and critical analysis. Time management in the written is critical.',
    topics: [
      { name: 'Practical Coursework (Artefact A + Visual Journal)', section: 'Coursework', markWeight: 50, examFrequency: 10, difficulty: 4, studyHours: 30, tip: 'Worth 50%. 12-week in-class project + Visual Journal documenting research, development, and artist\'s statement. Plan carefully from the start.' },
      { name: 'Invigilated Practical (Artefact B)', section: 'Practical Exam', markWeight: 20, examFrequency: 10, difficulty: 4, studyHours: 10, tip: 'Worth 20%. 5-hour exam day. Must relate to same stimulus as coursework. Practise working under timed conditions.' },
      { name: 'Visual Studies (Art History & Appreciation)', section: 'Written Exam', markWeight: 30, examFrequency: 10, difficulty: 3, studyHours: 14, tip: 'Worth 30%. Art history movements, key artists, critical analysis. Structured essay answers with specific references to artworks score highest.' },
    ],
  },

  // ═══════════════════════════════════════════════════════════════════════════
  // MUSIC
  // ═══════════════════════════════════════════════════════════════════════════
  {
    subject: 'Music',
    totalMarks: 400,
    papers: [
      { name: 'Core Performing', marks: 100, duration: 'Practical exam' },
      { name: 'Composing Paper', marks: 100, duration: '1h 30m' },
      { name: 'Listening Paper', marks: 100, duration: '1h 30m' },
      { name: 'Higher Elective', marks: 100, duration: 'Varies' },
    ],
    keyAdvice: 'Most students take the Performing Elective, making performing worth 50% total. If so, 200 marks are secured before written exams. For Composing, harmony (Q2, 60 marks) is worth more than melody (Q1, 40 marks). Know your 4 set works inside out for Listening.',
    topics: [
      { name: 'Performing (Core + Elective)', section: 'Practical Exam', markWeight: 50, examFrequency: 10, difficulty: 4, studyHours: 25, tip: 'Worth up to 200 marks (50%) if taking Performing Elective. Polished, expressive performances. Practise pieces thoroughly and aim for musicality.' },
      { name: 'Melody Composition (Q1)', section: 'Composing Paper', markWeight: 10, examFrequency: 10, difficulty: 4, studyHours: 10, tip: 'Worth 40 marks. Compose melody to given bars, in a dance metre, or set words. Practise melody writing in different metres and styles.' },
      { name: 'Harmony (Q2)', section: 'Composing Paper', markWeight: 15, examFrequency: 10, difficulty: 5, studyHours: 14, tip: 'Worth 60 marks. Compose bass notes and chords, add descant, or compose melody and bass from given chords. Invest more revision time here — it\'s worth more than melody.' },
      { name: 'Set Works (Listening Q1-Q4)', section: 'Listening Paper', markWeight: 15, examFrequency: 10, difficulty: 3, studyHours: 12, tip: 'Bulk of the Listening paper. 4 prescribed set works. Know instruments, themes, structure, historical context. Active listening with scores is essential.' },
      { name: 'Irish Traditional Music (Q5)', section: 'Listening Paper', markWeight: 5, examFrequency: 10, difficulty: 3, studyHours: 6, tip: 'Dance types (jig, reel, hornpipe, polka), sean-nós singing, fusion. 3 listening excerpts + essay. Reliable scoring section — learn the characteristics.' },
      { name: 'General Listening (Q6)', section: 'Listening Paper', markWeight: 5, examFrequency: 10, difficulty: 3, studyHours: 4, tip: 'Unseen/general question. Identify instruments, textures, forms, dynamics. Broad musical vocabulary helps here.' },
    ],
  },

];

// ─── Helpers ─────────────────────────────────────────────────────────────────

export const AVAILABLE_SUBJECTS = SYLLABUS_DATA.map(s => s.subject);

export function getSyllabusForSubject(subject: string): SubjectSyllabus | undefined {
  return SYLLABUS_DATA.find(s => s.subject === subject);
}

// ─── Fuzzy Topic Matcher ────────────────────────────────────────────────────

function normalizeStr(s: string): string {
  return s.toLowerCase().replace(/[^a-z0-9\s]/g, '').trim();
}

function tokenize(s: string): string[] {
  return normalizeStr(s).split(/\s+/).filter(t => t.length > 0);
}

export function fuzzyMatchTopic(subject: string, input: string): SyllabusTopic | null {
  if (!input || input.trim().length < 3) return null;
  const syllabus = getSyllabusForSubject(subject);
  if (!syllabus) return null;

  const normInput = normalizeStr(input);
  const inputTokens = tokenize(input);

  // 1. Exact match (normalized)
  for (const topic of syllabus.topics) {
    if (normalizeStr(topic.name) === normInput) return topic;
  }

  // 2. Substring match (either direction)
  for (const topic of syllabus.topics) {
    const normTopic = normalizeStr(topic.name);
    if (normTopic.includes(normInput) || normInput.includes(normTopic)) return topic;
  }

  // 3. Token overlap (2+ shared tokens)
  let bestMatch: SyllabusTopic | null = null;
  let bestOverlap = 0;
  for (const topic of syllabus.topics) {
    const topicTokens = tokenize(topic.name);
    const overlap = inputTokens.filter(t => topicTokens.some(tt => tt.includes(t) || t.includes(tt))).length;
    if (overlap >= 2 && overlap > bestOverlap) {
      bestOverlap = overlap;
      bestMatch = topic;
    }
  }

  return bestMatch;
}
