/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The Examiner's Chair — Engineering (Higher Level) marking sessions.
 *
 * Questions and scripts are AUTHORED for this exercise (labelled in each
 * `questionNote`) — they are not real SEC questions or candidate scripts. The
 * marking grammar (the "Any N @…" best-N cap, the 3+2 point+development split,
 * and separately-credited diagram labels) is the real SEC system, cited to:
 *  - SEC LC Engineering HL marking scheme 2025 —
 *    examiner-reports/engineering/2025-marking-scheme.*
 * Claim-by-claim record: compliance/evidence/examiners-chair.md.
 */

import { type ChairSubject, type GridSession } from './types';

const MS = (p: string) => ({ label: `SEC Engineering HL marking scheme 2025, ${p}` });

// ─────────────── EN1 · The "Any N" cap ───────────────

const EN1: GridSession = {
  mode: 'grid',
  id: 'en-anyn',
  subject: 'engineering',
  level: 'common',
  title: 'Answer exactly the number asked',
  cue: 'Any three',
  question: 'A part says “Discuss any three properties”, marked 6 + 6 + 6 — and only the FIRST three you write are counted. A candidate, playing safe, discusses five: the first two are under-developed (they don’t earn), and the three strong ones come last. Mark the three counted slots.',
  questionNote:
    'Scenario authored for this exercise. In “Any N @…” parts only the first N answers count; over-answering earns nothing extra, and if your best material comes after the Nth, it falls outside the counted set. Each counted slot here is worth 6 (earned only if the property is properly discussed).',
  grid: {
    perPoint: [{ id: 'prop', label: 'Property properly discussed', marks: 6 }],
    shorthand: 'Any three @ 6 + 6 + 6 (first three count)',
    ruleNote:
      'Only the first three answers are marked. Writing five wastes time, and if your strongest points come fourth and fifth they fall outside the counted three and score nothing. Lead with your three best and develop those.',
    cite: MS('p.20 (Any three @ 6+6+6 cap)'),
  },
  scripts: [
    {
      id: 'en1-a',
      label: 'Script A',
      persona: 'Writes five, best ones last',
      attempts: [
        {
          id: 'en1-a-1',
          text: 'Counted slot 1 — Property A, named but under-developed (a bare mention, no discussion).',
          key: { prop: 0 },
          keyNote: 'The first counted slot, and it’s under-developed — no proper discussion, so it doesn’t earn the 6. The candidate led with a weak point.',
        },
        {
          id: 'en1-a-2',
          text: 'Counted slot 2 — Property B, also under-developed.',
          key: { prop: 0 },
          keyNote: 'Second counted slot, also thin. Two of the three counted slots are gone before the good material even starts.',
        },
        {
          id: 'en1-a-3',
          text: 'Counted slot 3 — Property C, properly discussed with a consequence.',
          key: { prop: 6 },
          keyNote: 'The one developed point that fell inside the first three. The candidate also wrote two excellent properties (a 4th and 5th) — but only the first three count, so those are uncounted and score nothing. 6 of 18, with the best work wasted.',
        },
      ],
      embodies: {
        behaviour: 'Over-answers an “Any N” part and leads with weak points, so the best material is uncounted.',
        cite: MS('p.20'),
      },
    },
    {
      id: 'en1-b',
      label: 'Script B',
      persona: 'Three best, developed',
      attempts: [
        {
          id: 'en1-b-1',
          text: 'Counted slot 1 — a strong property, developed with a point and its consequence.',
          key: { prop: 6 },
          keyNote: 'Led with a best point, fully developed. 6.',
        },
        {
          id: 'en1-b-2',
          text: 'Counted slot 2 — a second strong property, developed.',
          key: { prop: 6 },
          keyNote: 'Another developed point. 6.',
        },
        {
          id: 'en1-b-3',
          text: 'Counted slot 3 — a third strong property, developed.',
          key: { prop: 6 },
          keyNote: 'Exactly three, each developed. 18/18 — and less writing than Script A.',
        },
      ],
    },
  ],
  takeaway: {
    id: 'codex-en1',
    rule: 'Give your best N, in your best order.',
    detail:
      'In “Any N @…” parts only the first N answers count — extras score nothing and can push your best material outside the counted set. Choose your strongest N points and lead with them.',
    cite: MS('p.20'),
  },
};

// ─────────────── EN2 · Headline before development ───────────────

const EN2: GridSession = {
  mode: 'grid',
  id: 'en-headline',
  subject: 'engineering',
  level: 'common',
  title: 'State the point, then develop it',
  cue: 'Explain',
  question: 'An “explain” point is marked 3 + 2: 3 for stating the point clearly, 2 for developing it. A candidate writes a flowing paragraph that circles the idea and eventually implies it, but never states it plainly.',
  questionNote:
    'Scenario authored for this exercise. The dominant Engineering “explain” pattern is 3 (state the point) + 2 (develop it); the clear headline banks the larger mark.',
  grid: {
    perPoint: [
      { id: 'point', label: 'State the point clearly', marks: 3 },
      { id: 'develop', label: 'Develop it', marks: 2 },
    ],
    shorthand: '3 + 2 (point + development)',
    ruleNote:
      'The headline is the bigger mark, and it has to be stated, not implied. A paragraph that circles the idea without naming it risks the 3, even if the development is good. Say the point in a plain sentence first, then develop it.',
    cite: MS('p.7–9 (3+2 point + development split)'),
  },
  scripts: [
    {
      id: 'en2-a',
      label: 'Script A',
      persona: 'Circles the point',
      attempts: [
        {
          id: 'en2-a-1',
          text: 'A flowing paragraph that hints at the idea and implies it by the end — but never states it in a plain sentence.',
          key: { point: 0, develop: 2 },
          keyNote: 'The development marks are there, but the 3-mark headline needs the point stated plainly — an implied point is a risked point. A single clear opening sentence naming the property or principle would have banked the 3. State it, then develop it.',
        },
      ],
      embodies: {
        behaviour: 'Implies the point instead of stating it, risking the larger headline mark.',
        cite: MS('p.7'),
      },
    },
    {
      id: 'en2-b',
      label: 'Script B',
      persona: 'Headline then development',
      attempts: [
        {
          id: 'en2-b-1',
          text: 'States the point in a plain opening sentence, then develops it with a reason and an example.',
          key: { point: 3, develop: 2 },
          keyNote: 'Clear headline (3) plus development (2). Full 5 — and the plain first sentence is what secured the bigger mark.',
        },
      ],
    },
  ],
  takeaway: {
    id: 'codex-en2',
    rule: 'State the point before you develop it.',
    detail:
      'Engineering “explain” marks split 3 (state the point) + 2 (develop) — and the headline is the bigger, must-be-stated mark. Open with a plain sentence naming the point, then develop it; don’t leave it implied.',
    cite: MS('p.7'),
  },
};

// ─────────────── EN3 · Labels are their own marks ───────────────

const EN3: GridSession = {
  mode: 'grid',
  id: 'en-labels',
  subject: 'engineering',
  level: 'common',
  title: 'The labels score too',
  cue: 'Draw a diagram',
  question: 'A diagram part is marked 8 + 1 + 1: 8 for the diagram, and two required labels credited separately at 1 mark each. A candidate draws an excellent diagram but leaves both labels off.',
  questionNote:
    'Scenario authored for this exercise. Engineering diagrams credit required labels separately from the drawing (e.g. 8 + 1 + 1).',
  grid: {
    perPoint: [
      { id: 'diagram', label: 'Diagram', marks: 8 },
      { id: 'label1', label: 'Label 1', marks: 1 },
      { id: 'label2', label: 'Label 2', marks: 1 },
    ],
    shorthand: '8 + 1 + 1 (diagram + 2 labels)',
    ruleNote:
      'The labels are their own marks, separate from the drawing. A flawless but unlabelled diagram forfeits them — small marks, but free ones, and routinely dropped.',
    cite: MS('p.16–17 (diagram + separate label marks)'),
  },
  scripts: [
    {
      id: 'en3-a',
      label: 'The diagram',
      persona: 'Great diagram, no labels',
      attempts: [
        {
          id: 'en3-a-1',
          text: 'A clear, correct diagram — but the two required parts are not labelled.',
          key: { diagram: 8, label1: 0, label2: 0 },
          keyNote: 'The diagram earns its 8, but the two label marks are separate and unearned. Two words would have added them. Whenever a diagram names parts, label them — the marks are itemised.',
        },
      ],
      embodies: {
        behaviour: 'Draws well but omits the separately-credited labels.',
        cite: MS('p.16'),
      },
    },
  ],
  takeaway: {
    id: 'codex-en3',
    rule: 'Label the diagram — those are separate marks.',
    detail:
      'Engineering diagrams credit required labels separately from the drawing (8 + 1 + 1). A perfect unlabelled diagram forfeits them. Add every required label — they’re small, free, and easy to drop.',
    cite: MS('p.16'),
  },
};

export const ENGINEERING_CHAIR: ChairSubject = {
  id: 'engineering',
  label: 'Engineering',
  tagline: 'Answer the number asked, state the point, label the diagram.',
  offeredLevels: ['higher', 'ordinary'],
  sessions: [EN1, EN2, EN3],
  sources: [
    { label: 'SEC LC Engineering HL marking scheme 2025 (examiner-reports/engineering/2025-marking-scheme)' },
  ],
  coverageNote:
    'These sessions teach the general conventions — the “Any N” cap, the point+development split and separately-credited labels — which apply at both Higher and Ordinary level. Verified against the 2025 Higher Level scheme; level-specific worked questions are being added.',
};
