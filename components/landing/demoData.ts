/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Real data for the landing page. GENERATED from the repo's own data on
 * 2026-09-07 by a one-off script (see design-references/landing/README.md):
 *  - Subject coverage: components/MarkBank/cards/sizes.json + paperTopicTags.json
 * The playground itself mounts the real app surfaces (components/landing/glass),
 * so nothing here is a mock of app content.
 *
 * Card order: a multi-row card leads each subject so the first reveal shows the scheme’s shape. Counts at generation time: 10495 Mark Bank cards across 15 subjects;
 * 3169 tagged papers, 32445 tagged questions, 98 subject ids.
 */

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
