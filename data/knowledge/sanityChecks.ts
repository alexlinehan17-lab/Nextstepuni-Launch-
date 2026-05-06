/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Sanity-Check Trainer questions (Stage 2, E6).
 *
 * 12 questions across Maths/Chemistry/Physics/Biology. Each presents
 * four candidate answers — three absurd, one correct. Each absurd answer
 * is tagged with the *primary check* that catches it:
 *
 *   - order-of-magnitude — answer is implausibly large or small
 *   - units               — answer has wrong/missing units
 *   - sign                — answer has the wrong sign or direction
 *   - substitute-back     — answer fails when plugged back into the question
 *
 * Source: dossier § C1 (sanity-check habit), § B2 / B4 (subject-specific
 * common errors), 2015 Maths CER ("if you find a person's height is
 * 800m, something is wrong").
 */

import { type SanityCheckQuestion } from '../../types/knowledge';

export const SANITY_CHECK_QUESTIONS: SanityCheckQuestion[] = [
  // ─── Maths ────────────────────────────────────────────────────────
  {
    id: 'sc-prob',
    subject: 'maths',
    topicLabel: 'Probability',
    questionPrompt: 'A bag holds 3 red and 7 blue balls. What is the probability of drawing a red ball?',
    candidates: [
      {
        id: 'a',
        text: '3 / 10',
        correct: true,
      },
      {
        id: 'b',
        text: '1.4',
        correct: false,
        catchingCheck: 'order-of-magnitude',
        absurdityExplanation: 'A probability is between 0 and 1. 1.4 means a 140% chance — impossible. Order of Magnitude catches this in two seconds.',
      },
      {
        id: 'c',
        text: '−3 / 10',
        correct: false,
        catchingCheck: 'sign',
        absurdityExplanation: 'A probability cannot be negative. The sign check catches this immediately.',
      },
      {
        id: 'd',
        text: '7 / 10',
        correct: false,
        catchingCheck: 'substitute-back',
        absurdityExplanation: '7/10 is the probability of blue, not red. Substitute back: "is 7 the count of red balls?" — no, 3 is.',
      },
    ],
    source: { section: 'C1', page: 15, cite: 'Dossier § C1 — probabilities lie between 0 and 1' },
  },
  {
    id: 'sc-area',
    subject: 'maths',
    topicLabel: 'Rectangular area',
    questionPrompt: 'Find the area of a rectangle 5 m wide and 3 m long.',
    candidates: [
      {
        id: 'a',
        text: '15 m²',
        correct: true,
      },
      {
        id: 'b',
        text: '15 m³',
        correct: false,
        catchingCheck: 'units',
        absurdityExplanation: 'Area uses m² (metres squared), not m³ (cubic metres — that\'s volume). The units check catches the wrong dimensionality.',
      },
      {
        id: 'c',
        text: '1500 m²',
        correct: false,
        catchingCheck: 'order-of-magnitude',
        absurdityExplanation: '5 × 3 = 15, not 1500. The order-of-magnitude check catches the missing decimal — 1500 m² is the size of a small park.',
      },
      {
        id: 'd',
        text: '8 m²',
        correct: false,
        catchingCheck: 'substitute-back',
        absurdityExplanation: '8 = 5 + 3, not 5 × 3. The student computed perimeter-divided-by-two instead of area.',
      },
    ],
    source: { section: 'C1', page: 15 },
  },
  {
    id: 'sc-linear',
    subject: 'maths',
    topicLabel: 'Linear equation',
    questionPrompt: 'Solve for x: 2x + 4 = 10.',
    candidates: [
      {
        id: 'a',
        text: 'x = 3',
        correct: true,
      },
      {
        id: 'b',
        text: 'x = 7',
        correct: false,
        catchingCheck: 'substitute-back',
        absurdityExplanation: '2(7) + 4 = 18, not 10. Substitute back catches the arithmetic slip in 30 seconds.',
      },
      {
        id: 'c',
        text: 'x = −3',
        correct: false,
        catchingCheck: 'sign',
        absurdityExplanation: 'The student divided correctly but got the sign wrong. Substitute back: 2(−3) + 4 = −2, not 10.',
      },
      {
        id: 'd',
        text: 'x = 0.3',
        correct: false,
        catchingCheck: 'order-of-magnitude',
        absurdityExplanation: 'A factor-of-ten error. 2(0.3) + 4 = 4.6, miles from 10. The OoM check catches the missing decimal place.',
      },
    ],
    source: { section: 'C1', page: 15 },
  },

  // ─── Chemistry ────────────────────────────────────────────────────
  {
    id: 'sc-ph',
    subject: 'chemistry',
    topicLabel: 'pH of pure water',
    questionPrompt: 'What is the pH of pure water at 25°C?',
    candidates: [
      {
        id: 'a',
        text: '7',
        correct: true,
      },
      {
        id: 'b',
        text: '17',
        correct: false,
        catchingCheck: 'order-of-magnitude',
        absurdityExplanation: 'pH runs from 0 to 14. 17 is off the scale. Order-of-magnitude catches this — pH outside [0, 14] is non-physical.',
      },
      {
        id: 'c',
        text: '−7',
        correct: false,
        catchingCheck: 'sign',
        absurdityExplanation: 'pH for normal aqueous solutions is non-negative. Negative pH only appears in extremely concentrated strong acids — never for water.',
      },
      {
        id: 'd',
        text: '14',
        correct: false,
        catchingCheck: 'substitute-back',
        absurdityExplanation: 'pH = 14 is the pH of a strong base like 1M NaOH. Pure water is neutral — substitute back: does pH 14 mean neutral? No.',
      },
    ],
    source: { section: 'C1', page: 15 },
  },
  {
    id: 'sc-moles',
    subject: 'chemistry',
    topicLabel: 'Moles from mass',
    questionPrompt: 'How many moles are in 18 g of water? (M = 18 g/mol)',
    candidates: [
      {
        id: 'a',
        text: '1 mol',
        correct: true,
      },
      {
        id: 'b',
        text: '18 mol',
        correct: false,
        catchingCheck: 'substitute-back',
        absurdityExplanation: '18 mol of water would weigh 324 g — not the 18 g we started with. Substitute back: mass = moles × M = 18 × 18 = 324, not 18.',
      },
      {
        id: 'c',
        text: '0.001 mol',
        correct: false,
        catchingCheck: 'order-of-magnitude',
        absurdityExplanation: 'A factor-of-1000 error. The OoM check: a teaspoon of water is roughly 1 mol, not a thousandth.',
      },
      {
        id: 'd',
        text: '−1 mol',
        correct: false,
        catchingCheck: 'sign',
        absurdityExplanation: 'Moles count particles. They are non-negative. The sign check catches this immediately.',
      },
    ],
    source: { section: 'B4', page: 10 },
  },
  {
    id: 'sc-mass',
    subject: 'chemistry',
    topicLabel: 'Mass from moles',
    questionPrompt: 'Mass of 0.5 mol NaCl? (M = 58.5 g/mol)',
    candidates: [
      {
        id: 'a',
        text: '29.25 g',
        correct: true,
      },
      {
        id: 'b',
        text: '29.25 mol',
        correct: false,
        catchingCheck: 'units',
        absurdityExplanation: 'Mass should be in grams (g), not moles. The units check catches this — the question asks for mass, not amount.',
      },
      {
        id: 'c',
        text: '117 g',
        correct: false,
        catchingCheck: 'substitute-back',
        absurdityExplanation: '117 g = 2 mol × 58.5 g/mol, not 0.5 mol. Sub back: 117 / 58.5 = 2, not 0.5.',
      },
      {
        id: 'd',
        text: '0.0855 g',
        correct: false,
        catchingCheck: 'order-of-magnitude',
        absurdityExplanation: 'A factor-of-1000 error suggests the student converted to kg without realising. OoM: 0.5 mol of table salt is a teaspoon, not a milligram.',
      },
    ],
    source: { section: 'B4', page: 10 },
  },

  // ─── Physics ──────────────────────────────────────────────────────
  {
    id: 'sc-force',
    subject: 'physics',
    topicLabel: 'Newton\'s second law',
    questionPrompt: 'Force needed to accelerate a 10 kg trolley at 5 m/s²?',
    candidates: [
      {
        id: 'a',
        text: '50 N',
        correct: true,
      },
      {
        id: 'b',
        text: '50',
        correct: false,
        catchingCheck: 'units',
        absurdityExplanation: 'No units. Per dossier § B4: missing units in physics commonly costs the final mark — the answer is physically meaningless without them.',
      },
      {
        id: 'c',
        text: '2 N',
        correct: false,
        catchingCheck: 'substitute-back',
        absurdityExplanation: 'F = ma, not F = m/a. The student divided. Substitute back: ma = 10 × 5 = 50, not 2.',
      },
      {
        id: 'd',
        text: '5000 N',
        correct: false,
        catchingCheck: 'order-of-magnitude',
        absurdityExplanation: '5000 N ≈ the weight of half a tonne. A 10 kg trolley accelerating gently shouldn\'t need that. OoM check catches it.',
      },
    ],
    source: { section: 'B4', page: 11 },
  },
  {
    id: 'sc-light',
    subject: 'physics',
    topicLabel: 'Speed of light',
    questionPrompt: 'Speed of light in vacuum?',
    candidates: [
      {
        id: 'a',
        text: '3 × 10⁸ m/s',
        correct: true,
      },
      {
        id: 'b',
        text: '3 × 10⁸ m',
        correct: false,
        catchingCheck: 'units',
        absurdityExplanation: 'Speed has units of m/s, not m. The units check catches this — m alone is a distance, not a speed.',
      },
      {
        id: 'c',
        text: '3 × 10¹⁰ m/s',
        correct: false,
        catchingCheck: 'order-of-magnitude',
        absurdityExplanation: '100× too fast — and faster than the universal speed limit, which is the speed of light itself. OoM catches the impossible.',
      },
      {
        id: 'd',
        text: '−3 × 10⁸ m/s',
        correct: false,
        catchingCheck: 'sign',
        absurdityExplanation: 'Speed is a magnitude — non-negative. Velocity can be negative; speed cannot. The sign check catches the conflation.',
      },
    ],
    source: { section: 'B4', page: 11 },
  },
  {
    id: 'sc-ke',
    subject: 'physics',
    topicLabel: 'Kinetic energy',
    questionPrompt: 'Kinetic energy of a 2 kg ball at 10 m/s?',
    candidates: [
      {
        id: 'a',
        text: '100 J',
        correct: true,
      },
      {
        id: 'b',
        text: '20 J',
        correct: false,
        catchingCheck: 'substitute-back',
        absurdityExplanation: '20 = mv = 2 × 10. That\'s momentum (p = mv), not kinetic energy (KE = ½mv²). Sub back: ½(2)(10²) = 100, not 20.',
      },
      {
        id: 'c',
        text: '100 J/s',
        correct: false,
        catchingCheck: 'units',
        absurdityExplanation: 'Energy is measured in J (joules), not J/s (joules per second — that\'s power, in watts). The units check catches the dimensional confusion.',
      },
      {
        id: 'd',
        text: '1000 J',
        correct: false,
        catchingCheck: 'order-of-magnitude',
        absurdityExplanation: 'Off by 10×. The student probably forgot the ½ in KE = ½mv². OoM: a 2 kg object at 10 m/s carries about as much energy as a small dropped book.',
      },
    ],
    source: { section: 'B4', page: 11 },
  },

  // ─── Biology ──────────────────────────────────────────────────────
  {
    id: 'sc-gestation',
    subject: 'biology',
    topicLabel: 'Human gestation',
    questionPrompt: 'Approximate human gestation period?',
    candidates: [
      {
        id: 'a',
        text: '9 months (~40 weeks)',
        correct: true,
      },
      {
        id: 'b',
        text: '9 weeks',
        correct: false,
        catchingCheck: 'order-of-magnitude',
        absurdityExplanation: '9 weeks is the end of the first trimester. The OoM check: babies are born at ~40 weeks, not 9.',
      },
      {
        id: 'c',
        text: '9 years',
        correct: false,
        catchingCheck: 'order-of-magnitude',
        absurdityExplanation: 'No mammal has a 9-year gestation. Elephants — the longest of any land mammal — are about 22 months. OoM catches this immediately.',
      },
      {
        id: 'd',
        text: '9 days',
        correct: false,
        catchingCheck: 'order-of-magnitude',
        absurdityExplanation: 'OoM: 9 days is the gestation of a small invertebrate. For a human, it\'s impossibly short.',
      },
    ],
    source: { section: 'C1', page: 15 },
  },
  {
    id: 'sc-heart',
    subject: 'biology',
    topicLabel: 'Resting heart rate',
    questionPrompt: 'Resting heart rate of a healthy adult?',
    candidates: [
      {
        id: 'a',
        text: '60–100 beats / min',
        correct: true,
      },
      {
        id: 'b',
        text: '7.5 beats / min',
        correct: false,
        catchingCheck: 'order-of-magnitude',
        absurdityExplanation: '7.5 bpm is a heart rate seen in deep medical emergencies. OoM: healthy adults are 60–100 bpm.',
      },
      {
        id: 'c',
        text: '7500 beats / min',
        correct: false,
        catchingCheck: 'order-of-magnitude',
        absurdityExplanation: '7500 bpm = 125 beats per second. Physiologically impossible. OoM catches the absurd.',
      },
      {
        id: 'd',
        text: '75 beats / hour',
        correct: false,
        catchingCheck: 'units',
        absurdityExplanation: '75 beats per hour ≈ 1 beat per minute. The units error makes the answer 60× too small. The unit check catches this when comparing /min vs /hour.',
      },
    ],
    source: { section: 'C1', page: 15 },
  },
  {
    id: 'sc-popgrowth',
    subject: 'biology',
    topicLabel: 'Bacterial population growth',
    questionPrompt: 'Starting from 1 cell of E. coli, doubling every 20 minutes — how many cells after 3 hours?',
    candidates: [
      {
        id: 'a',
        text: '2⁹ = 512',
        correct: true,
      },
      {
        id: 'b',
        text: '2³ = 8',
        correct: false,
        catchingCheck: 'substitute-back',
        absurdityExplanation: 'The student counted hours, not 20-minute intervals. 3 hours ÷ 20 min = 9 doublings, not 3. Sub back: in 3 hours there are 9 × 20 min, not 3.',
      },
      {
        id: 'c',
        text: '9 cells',
        correct: false,
        catchingCheck: 'substitute-back',
        absurdityExplanation: 'The student wrote down the number of doublings as the answer instead of 2⁹. Sub back: 9 doublings ≠ 9 cells; that\'s linear growth, not exponential.',
      },
      {
        id: 'd',
        text: '1.5 × 10⁹ cells',
        correct: false,
        catchingCheck: 'order-of-magnitude',
        absurdityExplanation: '1.5 × 10⁹ would take ~30 doublings — that\'s 10 hours, not 3. OoM catches the time-scale confusion.',
      },
    ],
    source: { section: 'C1', page: 15 },
  },
];
