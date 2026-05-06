/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Subject strategy preamble for English (Higher Level, Paper 1).
 * Read once before opening any individual question — covers the marking
 * shape, the killer P-caps-C-L rule, the genre vocabulary, and timing.
 */

import { type SubjectStrategy } from '../../types/examStrategiser';

export const englishStrategy: SubjectStrategy = {
  subject: 'english',
  headline: 'How English Higher Level is marked',
  intro:
    'Every long composition (50-mark Question B and 100-mark Section II) is graded on four criteria: Purpose, Coherence, Language, Mechanics. Knowing how these interact is worth more than any individual writing tip.',
  rules: [
    {
      id: 'pclm',
      title: 'P / C / L / M = 30 / 30 / 30 / 10',
      body: 'Long compositions split four ways: Purpose 30%, Coherence 30%, Language 30%, Mechanics 10%. Each criterion has its own ladder. Mechanics is small but examined strictly — apostrophes, comma splices, run-ons all count.',
    },
    {
      id: 'p-caps-cl',
      title: 'P caps C and L — the killer rule',
      body: 'Your Coherence and Language marks CANNOT exceed your Purpose mark. Brilliant prose in the wrong genre, or that misses one of the question\'s sub-tasks, is capped at the level of Purpose. Translation: get the genre and the task right BEFORE you flourish. Most 100-mark answers that score below H1 are capped here.',
      pinned: true,
    },
    {
      id: 'qa-shapes',
      title: 'Question A — three task shapes',
      body: 'A(i) "What does the writer reveal" — comprehension; three points anchored in the text. A(ii) "Why do you think... develop three points" — your personal views drawn from text and/or experience; "develop" means paragraph not sentence. A(iii) "Identify four elements of style" — writer\'s craft; four elements each linked to a named effect (informative, engaging, intriguing, appealing).',
    },
    {
      id: 'genre-vocab',
      title: 'Genre vocabulary',
      body: 'Recognise the genre BEFORE writing. Discursive essay = weigh multiple views (NOT argumentative). Argumentative/persuasive = pick one side and defend. Personal essay = first-person reflective, voice-driven. Speech = spoken register, rhetorical features, audience awareness. Short story = plot, character, conflict, resolution. Question B genre task (50m) = prescribed audience + 2-3 explicit sub-tasks.',
    },
    {
      id: 'three-points',
      title: 'When the question says "three points"',
      body: 'Three is enforced. Two falls short of the band. Five dilutes — markers reward QUALITY, not volume. Three discrete points, each genuinely different (not three rephrasings of the same thought).',
    },
  ],
  marksToMinutes: {
    summary: 'Paper 1: 200 marks across 170 minutes — roughly 0.85 minutes per mark.',
    examples: [
      '15-mark A(i)/A(ii) → ~13 mins each',
      '20-mark A(iii) → ~17 mins',
      '50-mark Question B → ~43 mins',
      '100-mark Section II composition → ~85 mins',
    ],
  },
};
