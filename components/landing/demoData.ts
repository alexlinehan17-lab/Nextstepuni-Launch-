/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Real data slices for the landing-page demos. GENERATED from the repo's own
 * data on 2026-09-07 by a one-off script (see design-references/landing/README.md):
 *  - Mark Bank cards: components/MarkBank/cards/<subject>/higher.ts (verbatim rows)
 *  - Topic fingerprints: data/paperTrail/paperTopicTags.json + topicLabels.json
 *  - Command words: commandWordData.ts
 *  - Subject coverage: components/MarkBank/cards/sizes.json + paperTopicTags.json
 * Nothing here is typed by hand except the sample week in PLANNER_WEEK, which is
 * a UI illustration, not a statistic.
 *
 * Card order: a multi-row card leads each subject so the first reveal shows the scheme’s shape. Counts at generation time: 10495 Mark Bank cards across 15 subjects;
 * 3169 tagged papers, 32445 tagged questions, 98 subject ids.
 */

export type RowKind = 'point' | 'allOf' | 'alt' | 'anyN';

export interface DemoCard {
  id: string;
  subject: string;
  subjectLabel: string;
  level: 'Higher' | 'Ordinary';
  year: number;
  ref: string;
  marks: number;
  question: string;
  rows: { kind: RowKind; text: string; marks: number }[];
  citation: string;
}

export const DEMO_CARDS: DemoCard[] = [
  {
    id: "bio-2025-hl-q4-c", subject: "biology", subjectLabel: "Biology", level: 'Higher', year: 2025,
    ref: "2025 HL Q4(c)", marks: 6,
    question: "(i) What term describes cells without membrane-bound organelles? (ii) What term describes cells with membrane-bound organelles?",
    rows: [
      { kind: "point", text: "(i) — Prokaryotic", marks: 3 },
      { kind: "point", text: "(ii) — Eukaryotic", marks: 3 },
    ],
    citation: "Marking points quoted from the SEC marking scheme, Biology 2025 Higher Level. © State Examinations Commission.",
  },
  {
    id: "bio-2025-hl-q7-ab", subject: "biology", subjectLabel: "Biology", level: 'Higher', year: 2025,
    ref: "2025 HL Q7(a)-(b)", marks: 5,
    question: "(a) In the scientific method, a testable statement is known as a _________________. (b) How can this statement be tested?",
    rows: [
      { kind: "point", text: "(a) — Hypothesis", marks: 2 },
      { kind: "point", text: "(b) — Conducting an experiment", marks: 3 },
    ],
    citation: "Marking points quoted from the SEC marking scheme, Biology 2025 Higher Level. © State Examinations Commission.",
  },
  {
    id: "bio-2025-hl-q1-a", subject: "biology", subjectLabel: "Biology", level: 'Higher', year: 2025,
    ref: "2025 HL Q1(a)", marks: 4,
    question: "Write the general formula for carbohydrates.",
    rows: [
      { kind: "point", text: "Cx(H2O)y", marks: 4 },
    ],
    citation: "Marking points quoted from the SEC marking scheme, Biology 2025 Higher Level. © State Examinations Commission.",
  },
  {
    id: "bio-2025-hl-q1-b", subject: "biology", subjectLabel: "Biology", level: 'Higher', year: 2025,
    ref: "2025 HL Q1(b)", marks: 4,
    question: "Give the four chemical elements present in all proteins.",
    rows: [
      { kind: "allOf", text: "Carbon (or C) and hydrogen (or H) and oxygen (or O) and nitrogen (or N)", marks: 4 },
    ],
    citation: "Marking points quoted from the SEC marking scheme, Biology 2025 Higher Level. © State Examinations Commission.",
  },
  {
    id: "bio-2025-hl-q1-d", subject: "biology", subjectLabel: "Biology", level: 'Higher', year: 2025,
    ref: "2025 HL Q1(d)", marks: 4,
    question: "Name the small subunits that make protein.",
    rows: [
      { kind: "point", text: "Amino acids", marks: 4 },
    ],
    citation: "Marking points quoted from the SEC marking scheme, Biology 2025 Higher Level. © State Examinations Commission.",
  },
  {
    id: "bio-2025-hl-q3-b", subject: "biology", subjectLabel: "Biology", level: 'Higher', year: 2025,
    ref: "2025 HL Q3(b)", marks: 3,
    question: "Name the cycle of reactions that occurs in stage 2 of aerobic respiration.",
    rows: [
      { kind: "point", text: "Krebs", marks: 3 },
    ],
    citation: "Marking points quoted from the SEC marking scheme, Biology 2025 Higher Level. © State Examinations Commission.",
  },
  {
    id: "chem-2021-hl-q11-c-iii", subject: "chemistry", subjectLabel: "Chemistry", level: 'Higher', year: 2021,
    ref: "2021 HL Q11(c)(iii)", marks: 6,
    question: "What happens in a radioactive nucleus during beta decay?",
    rows: [
      { kind: "point", text: "neutron changes into a proton", marks: 3 },
      { kind: "point", text: "and an electron which is emitted", marks: 3 },
    ],
    citation: "Marking points quoted from the SEC marking scheme, Chemistry 2021 Higher Level. © State Examinations Commission.",
  },
  {
    id: "phys-2021-hl-q14d-iv", subject: "physics", subjectLabel: "Physics", level: 'Higher', year: 2021,
    ref: "2021 HL Q14(d)(iv)", marks: 4,
    question: "Explain why white light is dispersed as it passes through the ball lens.",
    rows: [
      { kind: "point", text: "different colours of light", marks: 2 },
      { kind: "alt", text: "travel at different speeds (in glass)", marks: 2 },
    ],
    citation: "Marking points quoted from the SEC marking scheme, Physics 2021 Higher Level. © State Examinations Commission.",
  },
  {
    id: "bus-2023-hl-s1-q3a", subject: "business", subjectLabel: "Business", level: 'Higher', year: 2023,
    ref: "2023 HL Section 1 Q3(a)", marks: 4,
    question: "Explain, with an example, the term invisible exports.",
    rows: [
      { kind: "point", text: "Invisible exports refer to services sold by Irish businesses to customers from foreign countries.", marks: 1 },
      { kind: "point", text: "Money enters the Irish economy.", marks: 1 },
      { kind: "point", text: "Example Required", marks: 2 },
    ],
    citation: "Marking points quoted from the SEC marking scheme, Business 2023 Higher Level. © State Examinations Commission.",
  },
  {
    id: "agsci-2021-hl-q2aiii", subject: "agricultural-science", subjectLabel: "Agricultural Science", level: 'Higher', year: 2021,
    ref: "2021 HL Q2(a)(iii)", marks: 4,
    question: "Describe two reasons for the importance of controlling these herbicide resistant wild oats in the future.",
    rows: [
      { kind: "point", text: "Decreased yield (or food production)", marks: 2 },
      { kind: "point", text: "competition between wild oats and crop", marks: 2 },
    ],
    citation: "Marking points quoted from the SEC marking scheme, Agricultural Science 2021 Higher Level. © State Examinations Commission.",
  },
  {
    id: "he-2022-hl-sa-q1", subject: "home-economics", subjectLabel: "Home Economics", level: 'Higher', year: 2022,
    ref: "2022 HL Section A Q1", marks: 6,
    question: "State two functions of calcium in the body. Identify one factor that affects calcium absorption.",
    rows: [
      { kind: "anyN", text: "Formation of strong bones and teeth; blood clotting; regulate blood pressure; normal muscle contractions; regular heartbeat; normal nerve function; etc.", marks: 4 },
      { kind: "anyN", text: "Vitamin D; oestrogen; acidic environment/Vitamin C; protein; etc. tannins; fat; phytates/phytic acid; oxalates/oxalic acid; etc.", marks: 2 },
    ],
    citation: "Marking points quoted from the SEC marking scheme, Home Economics 2022 Higher Level. © State Examinations Commission.",
  },
];


export const DEMO_CARD_SUBJECTS: { id: string; label: string }[] = [
  { id: 'biology', label: 'Biology' },
  { id: 'chemistry', label: 'Chemistry' },
  { id: 'physics', label: 'Physics' },
  { id: 'business', label: 'Business' },
  { id: 'agricultural-science', label: 'Ag. Science' },
  { id: 'home-economics', label: 'Home Ec.' },
];

/** Biology, Higher Level: which years each topic was asked, 2010 to 2026. */
export const ATLAS_YEARS: number[] = [2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026];
export const ATLAS_TOPICS: { id: string; label: string; years: number[] }[] = [
  { id: "biology-1-4", label: "Genetics, DNA & Evolution", years: [2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026] },
  { id: "biology-0-2", label: "Food & Nutrition (Food Tests)", years: [2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026] },
  { id: "biology-0-3", label: "General Principles of Ecology", years: [2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026] },
  { id: "biology-1-1", label: "Cell Metabolism & Enzymes", years: [2010, 2011, 2012, 2013, 2014, 2016, 2017, 2019, 2020, 2021, 2024, 2025, 2026] },
  { id: "biology-2-4", label: "Nervous System & Responses to Stimuli", years: [2010, 2011, 2012, 2013, 2014, 2017, 2019, 2020, 2022, 2023, 2025, 2026] },
  { id: "biology-1-6", label: "Respiration", years: [2011, 2014, 2017, 2018, 2019, 2021, 2022, 2023, 2024, 2025, 2026] },
  { id: "biology-1-5", label: "Photosynthesis", years: [2012, 2013, 2015, 2017, 2018, 2020, 2022, 2023, 2025, 2026] },
  { id: "biology-2-13", label: "Plant Reproduction", years: [2010, 2013, 2014, 2015, 2016, 2020, 2021, 2023, 2024, 2025, 2026] },
  { id: "biology-1-2", label: "Cell Continuity (Cell Division)", years: [2011, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2026] },
  { id: "biology-0-4", label: "A Study of an Ecosystem", years: [2010, 2013, 2015, 2016, 2017, 2018, 2020, 2023, 2025, 2026] },
  { id: "biology-2-0", label: "Diversity of Organisms", years: [2010, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2021, 2022, 2023, 2024, 2025, 2026] },
  { id: "biology-0-0", label: "The Scientific Method", years: [2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2023, 2024, 2025, 2026] },
];

export interface DemoCommandWord {
  id: string; subjectLabel: string; questionRef: string; marks: number;
  stem: string; commandWord: string; demand: string; trap: string; source: string;
}
export const COMMAND_WORDS: DemoCommandWord[] = [
  { id: "biz-illustrate-specific-performance", subjectLabel: "Business", questionRef: "HL · Business Law", marks: 5,
    stem: "Illustrate, using an example, what is meant by ‘specific performance’ as a remedy for breach of contract.",
    commandWord: "Illustrate",
    demand: "Explain the term AND give a concrete example. With “Illustrate”, the example is not optional decoration — it earns marks in its own right (the marking grid gives separate marks for the example).",
    trap: "Many candidates defined the term correctly but gave no example, “thereby losing marks.” The same requirement caught people out in Q3(B) and Q7(C).",
    source: "LC Business Chief Examiner 2015, p.17" },
  { id: "biz-list-discrimination-grounds", subjectLabel: "Business", questionRef: "HL · Business Law", marks: 6,
    stem: "List three grounds under which discrimination is prohibited by employment equality legislation.",
    commandWord: "List",
    demand: "Just name them — short, separate points. “List” rewards naming only; no explanation is needed or marked.",
    trap: "Some candidates “wrote paragraphs to explain the protected grounds rather than just naming the grounds, as was required.” That extra writing earns nothing and burns time.",
    source: "LC Business Chief Examiner 2015, p.17" },
  { id: "biz-define-delegation", subjectLabel: "Business", questionRef: "HL · Managing", marks: 5,
    stem: "Define the term ‘delegation’ as used in management.",
    commandWord: "Define",
    demand: "Give ONE precise sentence stating exactly what it means. “Define” wants brevity plus accuracy.",
    trap: "A vague, roundabout or example-led sentence loses the mark — a definition must be tight and technically correct, not a story about it.",
    source: "LC Business 2025 marking scheme (“Define” = a precise sentence)" },
  { id: "biz-distinguish-ltd-plc", subjectLabel: "Business", questionRef: "HL · Business Ownership", marks: 10,
    stem: "Distinguish between a private limited company and a public limited company as forms of business ownership.",
    commandWord: "Distinguish",
    demand: "Bring out the DIFFERENCE(S) — contrast the two directly (e.g. “whereas a private limited company…, a public limited company…”). The contrast is what’s marked.",
    trap: "Describing each type separately, in isolation, without making the difference explicit, misses the comparison the cue demands.",
    source: "LC Business Chief Examiner 2015, p.20 (compare/distinguish cues)" },
  { id: "biz-evaluate-management-control", subjectLabel: "Business", questionRef: "HL · Managing", marks: 7,
    stem: "Evaluate the effectiveness of one method of management control used by a business.",
    commandWord: "Evaluate",
    demand: "Make a JUDGEMENT and justify it — say how effective it is and why. Evaluation is the most heavily weighted single component (3 of 7 marks in the 2025 grid).",
    trap: "Candidates often name and explain the control, then stop. “Some evaluations continue to be very superficial and some candidates do not evaluate at all” — the highest-order, highest-mark step is the one most often skipped.",
    source: "LC Business Chief Examiner 2015, p.17; 2025 marking scheme (B(i) weights evaluation 3/7)" },
];

export type PlanKind = 'review' | 'new' | 'paper' | 'rest';
export interface PlanItem { kind: PlanKind; subject: string; label: string; count?: number; minutes: number; done?: boolean }
export interface PlanDay { day: string; date: string; today?: boolean; items: PlanItem[] }

/** A sample week in the shape the Spaced Repetition Timetable produces (45-minute blocks typed New learning / Practice / Revision, Mark Bank reviews, up to three rest days). Subjects are real; the schedule is an illustration. */
export const PLANNER_WEEK: PlanDay[] = [
  { day: 'Mon', date: '7 Sep', items: [
    { kind: 'new', subject: 'Biology', label: 'New learning', minutes: 45, done: true },
    { kind: 'review', subject: 'Mark Bank', label: '12 cards due', count: 12, minutes: 15, done: true },
  ] },
  { day: 'Tue', date: '8 Sep', today: true, items: [
    { kind: 'paper', subject: 'Mathematics', label: 'Practice', minutes: 45 },
    { kind: 'review', subject: 'Mark Bank', label: '9 cards due', count: 9, minutes: 12 },
    { kind: 'new', subject: 'Business', label: 'Revision', minutes: 45 },
  ] },
  { day: 'Wed', date: '9 Sep', items: [
    { kind: 'new', subject: 'English', label: 'New learning', minutes: 45 },
    { kind: 'review', subject: 'Mark Bank', label: '7 cards due', count: 7, minutes: 10 },
  ] },
  { day: 'Thu', date: '10 Sep', items: [
    { kind: 'paper', subject: 'Geography', label: 'Practice', minutes: 45 },
    { kind: 'new', subject: 'Biology', label: 'Revision', minutes: 45 },
  ] },
  { day: 'Fri', date: '11 Sep', items: [
    { kind: 'review', subject: 'Mark Bank', label: '11 cards due', count: 11, minutes: 14 },
    { kind: 'new', subject: 'Irish', label: 'New learning', minutes: 45 },
  ] },
  { day: 'Sat', date: '12 Sep', items: [
    { kind: 'paper', subject: 'Biology', label: '2024 Higher, Section A', minutes: 45 },
  ] },
  { day: 'Sun', date: '13 Sep', items: [ { kind: 'rest', subject: '', label: 'Rest day', minutes: 0 } ] },
];

export interface SubjectRow { id: string; label: string; markBankCards: number; paperTrail: boolean; /** Years with papers in the Paper Trail, e.g. '2010–2026'. */ paperYears: string }
export interface SubjectGroup { id: string; label: string; subjects: SubjectRow[] }
export const SUBJECT_GROUPS: SubjectGroup[] = [
  { id: "sciences", label: "Sciences", subjects: [
    { id: "biology", label: "Biology", markBankCards: 1359, paperTrail: true, paperYears: '2010–2026' },
    { id: "chemistry", label: "Chemistry", markBankCards: 876, paperTrail: true, paperYears: '2010–2026' },
    { id: "physics", label: "Physics", markBankCards: 1133, paperTrail: true, paperYears: '2010–2026' },
    { id: "agricultural-science", label: "Agricultural Science", markBankCards: 869, paperTrail: true, paperYears: '2010–2025' }
  ] },
  { id: "business", label: "Business & Economics", subjects: [
    { id: "business", label: "Business", markBankCards: 606, paperTrail: true, paperYears: '2010–2026' },
    { id: "economics", label: "Economics", markBankCards: 697, paperTrail: true, paperYears: '2010–2026' },
    { id: "accounting", label: "Accounting", markBankCards: 0, paperTrail: true, paperYears: '2010–2020' }
  ] },
  { id: "maths", label: "Maths & Computing", subjects: [
    { id: "maths", label: "Mathematics", markBankCards: 833, paperTrail: true, paperYears: '2010–2025' },
    { id: "applied-mathematics", label: "Applied Maths", markBankCards: 0, paperTrail: true, paperYears: '2010–2022' },
    { id: "computer-science", label: "Computer Science", markBankCards: 336, paperTrail: true, paperYears: '2020–2026' }
  ] },
  { id: "languages", label: "Languages", subjects: [
    { id: "english", label: "English", markBankCards: 650, paperTrail: true, paperYears: '2010–2025' },
    { id: "irish", label: "Irish", markBankCards: 400, paperTrail: true, paperYears: '2010–2026' },
    { id: "french", label: "French", markBankCards: 0, paperTrail: true, paperYears: '2010–2026' },
    { id: "german", label: "German", markBankCards: 0, paperTrail: true, paperYears: '2010–2026' },
    { id: "spanish", label: "Spanish", markBankCards: 0, paperTrail: true, paperYears: '2010–2026' },
    { id: "italian", label: "Italian", markBankCards: 0, paperTrail: true, paperYears: '2010–2026' }
  ] },
  { id: "humanities", label: "Humanities", subjects: [
    { id: "geography", label: "Geography", markBankCards: 754, paperTrail: true, paperYears: '2010–2025' },
    { id: "history", label: "History", markBankCards: 0, paperTrail: true, paperYears: '2010–2026' },
    { id: "politics-and-society", label: "Politics & Society", markBankCards: 0, paperTrail: true, paperYears: '2018–2025' },
    { id: "religious-education", label: "Religious Education", markBankCards: 0, paperTrail: true, paperYears: '2010–2026' },
    { id: "classical-studies", label: "Classical Studies", markBankCards: 0, paperTrail: true, paperYears: '2023–2025' }
  ] },
  { id: "practical", label: "Practical & Creative", subjects: [
    { id: "art", label: "Art", markBankCards: 462, paperTrail: true, paperYears: '2010–2026' },
    { id: "construction-studies", label: "Construction Studies", markBankCards: 505, paperTrail: true, paperYears: '2010–2026' },
    { id: "engineering", label: "Engineering", markBankCards: 466, paperTrail: true, paperYears: '2010–2026' },
    { id: "home-economics", label: "Home Economics", markBankCards: 549, paperTrail: true, paperYears: '2011–2025' },
    { id: "design-and-communication-graphics", label: "DCG", markBankCards: 0, paperTrail: true, paperYears: '2010–2026' },
    { id: "technology", label: "Technology", markBankCards: 0, paperTrail: true, paperYears: '2010–2026' },
    { id: "music", label: "Music", markBankCards: 0, paperTrail: true, paperYears: '2010–2026' },
    { id: "physical-education", label: "Physical Education", markBankCards: 0, paperTrail: true, paperYears: '2020–2025' }
  ] },
];

/**
 * Screenshot frames for the chapters. null = a labelled placeholder frame
 * (Alex supplies real captures later). The app already ships captures under
 * /assets/guide/*.jpg, so flipping one of these to that path swaps a real
 * screen in without touching the layout.
 */
export const CAPTURES: Record<'markbank' | 'papertrail' | 'atlas' | 'planner' | 'launchpad' | 'lab', string | null> = {
  markbank: null,
  papertrail: null,
  atlas: null,
  planner: null,
  launchpad: null,
  lab: null,
};
