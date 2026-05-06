/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Subject strategy preamble for Irish (Higher Level).
 */

import { type SubjectStrategy } from '../../types/examStrategiser';

export const irishStrategy: SubjectStrategy = {
  subject: 'irish',
  headline: 'How Irish Higher Level Litríocht is marked',
  intro:
    'Litríocht (literature) questions on Paper 2 reward specific textual reference — quoted moments and named characters — far more than thematic generalities. Vague engagement with the text caps you well below the top bands.',
  rules: [
    {
      id: 'pleigh',
      title: 'Pléigh / Déan cur síos — the recurring command words',
      body: 'Pléigh = Discuss. Balanced analysis with reference to specific moments in the text — not a one-sided argument, not a plot summary. Déan cur síos = Describe. More expository, but still requires textual specificity. Both reward analysis over narration.',
    },
    {
      id: 'specific-over-thematic',
      title: 'Specific quotes beat thematic gestures',
      body: '"Sa scéal seo" or "an príomhcharachtar" without naming them costs marks. Quote at least two specific moments and name characters explicitly. Markers reward concrete textual engagement: paraphrased moments, named characters, and direct quotes earn SRPs that vague gestures do not.',
      pinned: true,
    },
    {
      id: 'one-theme',
      title: 'One main theme, not three',
      body: 'Most "main theme" questions reward picking ONE theme and developing it across 5-6 paragraphs with two textual references each. Scatter-gun coverage of three or four themes is penalised — depth on one theme beats shallow coverage of many.',
    },
  ],
  marksToMinutes: {
    summary: 'Paper 2: 200 marks across 180 minutes — roughly 0.9 minutes per mark.',
    examples: [
      '50-mark literature essay → ~45 mins',
      'Aim for 5-6 paragraphs with two textual references each',
    ],
  },
};
