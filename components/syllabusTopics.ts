/** @license SPDX-License-Identifier: Apache-2.0 */

/**
 * Pre-populated Leaving Cert Higher Level syllabus topics for each subject.
 * Used for tracking which syllabus areas a student has covered.
 */

export const SYLLABUS_TOPICS: Record<string, string[]> = {
  English: [
    'Paper 1 Comprehension',
    'Paper 1 Composition',
    'Paper 1 Language Analysis',
    'Single Text',
    'Comparative Study',
    'Unseen Poetry',
    'Prescribed Poetry',
  ],

  Irish: [
    'Ceapadóireacht (Essay Writing)',
    'Léamhthuiscint (Reading Comprehension)',
    'Cluastuiscint (Listening)',
    'Scrúdú Cainte (Oral)',
    'Prós Ainmnithe (Prose)',
    'Filíocht Ainmnithe (Poetry)',
    'Gramadach (Grammar)',
  ],

  Mathematics: [
    'Algebra',
    'Complex Numbers',
    'Sequences & Series',
    'Functions & Graphs',
    'Differential Calculus',
    'Integral Calculus',
    'Financial Maths',
    'Coordinate Geometry',
    'Trigonometry',
    'Probability',
    'Statistics',
    'Geometry (Theorems & Proofs)',
  ],

  Biology: [
    'Cell Biology & Biochemistry',
    'Cell Division',
    'Genetics',
    'DNA & Biotechnology',
    'Ecology',
    'Microbiology',
    'Classification',
    'Plant Biology',
    'Human Nutrition & Digestion',
    'The Circulatory System',
    'The Respiratory System',
    'Excretion & Homeostasis',
    'The Nervous System & Senses',
    'Reproduction & Growth',
    'Mandatory Experiments',
  ],

  Chemistry: [
    'Atomic Structure & Trends',
    'Chemical Bonding',
    'Stoichiometry',
    'The Mole',
    'Rates of Reaction',
    'Chemical Equilibrium',
    'Acids & Bases (pH)',
    'Organic Chemistry',
    'Volumetric Analysis',
    'Fuels & Thermochemistry',
    'Electrochemistry',
    'Water Chemistry',
    'Mandatory Experiments',
  ],

  Physics: [
    'Mechanics (Forces & Motion)',
    'Vectors & Scalars',
    'Energy & Momentum',
    'Circular Motion & Gravity',
    'Heat & Temperature',
    'Waves (Light & Sound)',
    'Reflection & Refraction',
    'Diffraction & Interference',
    'Static Electricity',
    'Current Electricity',
    'Electromagnetism',
    'The Electron',
    'Nuclear Physics & Radioactivity',
    'Semiconductors',
    'Mandatory Experiments',
  ],

  History: [
    'Research Study Skills',
    'Document Questions',
    'The Pursuit of Sovereignty (Ireland 1912–1949)',
    'Northern Ireland 1949–1993',
    'The United States & the World 1945–1989',
    'Europe & the Wider World (selected topic)',
    'Case Study Preparation',
  ],

  Geography: [
    'Plate Tectonics & Earthquakes',
    'Volcanism',
    'Rock Cycle & Landforms',
    'Weathering & Mass Movement',
    'Rivers & Flooding',
    'Coastal Processes',
    'Karst Landscapes',
    'Climate & Weather',
    'Soils & the Biome',
    'Population & Settlement',
    'Urbanisation',
    'Economic Activities',
    'Geoecology',
    'Optional Unit (Patterns & Processes)',
    'Ordnance Survey Maps',
  ],

  Business: [
    'Introduction to Enterprise',
    'Managing 1 (People & Leadership)',
    'Managing 2 (Operations & HRM)',
    'Business in Action (Marketing)',
    'Business in Action (Finance)',
    'The Domestic Business Environment',
    'The International Business Environment',
    'Business Plans & ABQ (Applied Business Question)',
  ],

  Accounting: [
    'Introduction to Accounting',
    'Final Accounts (Sole Trader)',
    'Final Accounts (Company)',
    'Incomplete Records',
    'Club Accounts',
    'Farm Accounts',
    'Published Accounts & Ratios',
    'Tabular Statements',
    'Marginal & Absorption Costing',
    'Budgeting & Cash Flow',
    'Correction of Errors & Suspense',
  ],

  Economics: [
    'Introduction to Economics (Scarcity & Choice)',
    'Demand Supply & Market Price',
    'Consumer Theory (Utility)',
    'Costs Production & Market Structures',
    'National Income',
    'Government in the Economy',
    'Money & Banking',
    'International Trade',
    'Economic Growth & Development',
    'The Irish Economy',
    'Fiscal & Monetary Policy',
  ],

  French: [
    'Reading Comprehension',
    'Listening Comprehension',
    'Written Production (Opinion Piece/Essay)',
    'Letter/Email Writing',
    'Oral Preparation',
    'Grammar & Tenses',
    'Vocabulary & Idioms',
  ],

  German: [
    'Reading Comprehension',
    'Listening Comprehension',
    'Written Production (Opinion Piece/Essay)',
    'Letter/Email Writing',
    'Oral Preparation',
    'Grammar & Tenses',
    'Vocabulary & Idioms',
  ],

  Spanish: [
    'Reading Comprehension',
    'Listening Comprehension',
    'Written Production (Opinion Piece/Essay)',
    'Letter/Email Writing',
    'Oral Preparation',
    'Grammar & Tenses',
    'Vocabulary & Idioms',
  ],

  'Applied Maths': [
    'Linear Motion (SUVAT)',
    'Projectiles',
    "Newton's Laws of Motion",
    'Connected Particles (Pulleys & Wedges)',
    'Circular Motion',
    'Simple Harmonic Motion',
    'Relative Velocity',
    'Statics (Forces in Equilibrium)',
    'Moments & Couples',
    'Hydrostatics',
    'Impact & Collisions',
  ],

  'Computer Science': [
    'Computational Thinking & Algorithms',
    'Programming Fundamentals',
    'Data Representation',
    'Computer Architecture',
    'Networking & the Internet',
    'Databases',
    'Web Development',
    'Cybersecurity',
    'Software Development',
    'Coursework Project (ALT)',
  ],

  Art: [
    'Life Drawing & Still Life',
    'Imaginative Composition',
    'Design (Craftwork)',
    'Art History — Irish Art',
    'Art History — European Art',
    'Art Appreciation',
  ],

  'Home Economics': [
    'Food Science & Nutrition',
    'Food Preparation & Cooking',
    'Diet & Health',
    'Consumer Studies',
    'Social Studies (Family & Housing)',
    'Resource Management',
    'Textiles',
    'Elective (Home Design & Management or Social Studies)',
  ],

  'Agricultural Science': [
    'Soil Science',
    'Grassland Management',
    'Animal Reproduction',
    'Animal Nutrition & Feeding',
    'Genetics & Breeding',
    'Crop Production',
    'Farm Safety',
    'Ecology',
    'Mandatory Experiments & Investigations',
  ],

  Music: [
    'Composing',
    'Listening & Responding',
    'Performing (Practical)',
    'Irish Music Tradition',
    'Art Music (Set Works)',
    'Popular Music',
    'Musical Literacy & Theory',
  ],
};

// ---------------------------------------------------------------------------
// Alias map: maps common short-hand / variant names to the canonical key
// used in SYLLABUS_TOPICS. All keys are stored in lower-case for matching.
// ---------------------------------------------------------------------------
const SUBJECT_ALIASES: Record<string, string> = {
  // Mathematics
  maths: 'Mathematics',
  math: 'Mathematics',
  'higher maths': 'Mathematics',
  'hl maths': 'Mathematics',

  // Biology
  bio: 'Biology',

  // Chemistry
  chem: 'Chemistry',

  // Physics
  phys: 'Physics',

  // Irish
  gaeilge: 'Irish',
  gaelige: 'Irish',

  // English
  eng: 'English',

  // Geography
  geo: 'Geography',
  geog: 'Geography',

  // History
  hist: 'History',

  // Business
  'business studies': 'Business',

  // Economics
  econ: 'Economics',

  // Applied Maths
  'applied mathematics': 'Applied Maths',
  'applied math': 'Applied Maths',

  // Computer Science
  cs: 'Computer Science',
  'comp sci': 'Computer Science',
  computing: 'Computer Science',
  'computer studies': 'Computer Science',
  lccs: 'Computer Science',

  // Home Economics
  'home ec': 'Home Economics',
  'home econ': 'Home Economics',

  // Agricultural Science
  'ag science': 'Agricultural Science',
  'ag sci': 'Agricultural Science',
  'agri science': 'Agricultural Science',

  // Art
  'art history': 'Art',
  'visual art': 'Art',

  // Accounting
  accounts: 'Accounting',

  // Music
  mus: 'Music',
};

/**
 * Look up syllabus topics for a given subject name.
 *
 * Performs a case-insensitive match against the canonical subject names first,
 * then falls back to a set of common aliases (e.g. "Maths" → "Mathematics",
 * "Bio" → "Biology"). Returns an empty array when no match is found.
 */
export function getSyllabusTopics(subjectName: string): string[] {
  if (!subjectName) return [];

  const trimmed = subjectName.trim();

  // 1. Try exact (case-insensitive) match against canonical keys
  const canonical = Object.keys(SYLLABUS_TOPICS).find(
    (key) => key.toLowerCase() === trimmed.toLowerCase(),
  );
  if (canonical) return SYLLABUS_TOPICS[canonical];

  // 2. Try alias lookup
  const aliasTarget = SUBJECT_ALIASES[trimmed.toLowerCase()];
  if (aliasTarget && SYLLABUS_TOPICS[aliasTarget]) {
    return SYLLABUS_TOPICS[aliasTarget];
  }

  // 3. No match
  return [];
}
