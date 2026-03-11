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
    totalMarks: 300,
    papers: [
      { name: 'One Paper', marks: 300, duration: '3h' },
    ],
    keyAdvice: 'Answer any 6 of 11 questions (50 marks each). Titration (Q1) is guaranteed and should be automatic marks. Organic Chemistry appears every year. Since you choose your 6, play to your strengths — master 7-8 topics and you\'ll always have 6 strong answers. The 2026 paper is the LAST under the current syllabus.',
    topics: [
      { name: 'Titrations (Volumetric Analysis)', section: 'Section A (Q1)', markWeight: 17, examFrequency: 10, difficulty: 3, studyHours: 10, tip: 'Guaranteed every year. Acid-base, redox, back titration. Practise calculations until automatic. Show all working. Free marks if prepared.' },
      { name: 'Organic Chemistry', section: 'Section A & B', markWeight: 17, examFrequency: 10, difficulty: 4, studyHours: 14, tip: 'Hydrocarbons, alcohols, aldehydes, ketones, carboxylic acids, esters, polymers. Annual appearance. Preparation experiment in Section A. Learn reaction types and functional group tests.' },
      { name: 'Acids & Bases', section: 'Section B', markWeight: 12, examFrequency: 9, difficulty: 3, studyHours: 10, tip: 'Arrhenius, Bronsted-Lowry definitions, pH calculations, strong vs weak, buffer solutions. Near-annual. pH calculations are essential.' },
      { name: 'Chemical Equilibrium', section: 'Section B', markWeight: 10, examFrequency: 9, difficulty: 4, studyHours: 10, tip: 'Le Chatelier\'s, Kc calculations, industrial processes (Haber, Contact). Very frequent. Kc calculation is almost guaranteed.' },
      { name: 'Rates of Reaction', section: 'Section B', markWeight: 8, examFrequency: 7, difficulty: 3, studyHours: 7, tip: 'Factors affecting rate, collision theory, catalysts. Longest gap since 2023 — very likely for 2026. Know experiments and rate graphs.' },
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
      { name: 'Mandatory Experiments', section: 'Section A', markWeight: 30, examFrequency: 10, difficulty: 2, studyHours: 12, tip: '3 of 5 questions, 40 marks each = 120 marks. 25 experiments to know. Always: labelled diagram, method, calculations, graph drawing, precautions. Most predictable marks on the paper.' },
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

];

// ─── Helpers ─────────────────────────────────────────────────────────────────

export const AVAILABLE_SUBJECTS = SYLLABUS_DATA.map(s => s.subject);

export function getSyllabusForSubject(subject: string): SubjectSyllabus | undefined {
  return SYLLABUS_DATA.find(s => s.subject === subject);
}
