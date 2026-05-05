/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Placeholder Irish questions — used to verify Exam Strategiser rendering.
 * Real Leaving Cert questions to be authored in subsequent prompts.
 */

import { type ExamQuestion } from '../../types/examStrategiser';

export const irishQuestions: ExamQuestion[] = [
  {
    id: 'irish-placeholder-2024-p2-q1',
    subject: 'irish',
    year: 2024,
    paper: 'Paper 2',
    section: 'Litríocht',
    questionNumber: '1',
    level: 'higher',
    marks: 50,
    totalPaperMarks: 200,
    totalPaperMinutes: 180,
    commandWords: ['Pléigh'],
    questionText: [
      {
        type: 'paragraph',
        content: [
          {
            text: 'Pléigh',
            annotation: {
              type: 'command',
              note: '"Pléigh" = Discuss. Like the English equivalent, this asks for balanced analysis with reference to specific moments in the text — not a summary of the plot.',
            },
          },
          { text: ' an ' },
          {
            text: 'phríomhthéama',
            annotation: {
              type: 'keyword',
              note: 'Príomhthéama = main theme. Pick ONE main theme and stick with it across the whole answer. Markers penalise scatter-gun coverage of three or four themes.',
            },
          },
          { text: ' atá sa ghearrscéal a rinne tú don chúrsa. ' },
          {
            text: 'Déan tagairt do shamplaí ón téacs',
            annotation: {
              type: 'trap',
              note: 'Vague references lose marks. "An scéal" or "an príomhcharachtar" without naming them costs you. Quote at least two specific moments and name characters explicitly.',
            },
          },
          { text: '.' },
        ],
      },
      {
        type: 'spacer',
        content: [{ text: '' }],
      },
      {
        type: 'paragraph',
        content: [
          {
            text: '(50 marc)',
            annotation: {
              type: 'marks-allocation',
              note: '50 marks out of 200 on a 180-minute Paper 2 = ~45 minutes. Aim for 5-6 paragraphs with two textual references in each.',
            },
          },
        ],
      },
    ],
    predictPrompts: [
      {
        id: 'command-word',
        prompt: 'What does the command word "Pléigh" ask you to do?',
        type: 'multiple-choice',
        options: ['Summarise', 'Discuss', 'Translate', 'Compare two texts'],
        correctAnswer: 'Discuss',
        hint: 'It is the Irish equivalent of a familiar English command word.',
      },
      {
        id: 'time-allocation',
        prompt: 'How many minutes should you spend on this question?',
        type: 'number',
        correctAnswer: 45,
        hint: '50 marks out of 200 on a 180-minute paper.',
      },
      {
        id: 'reference-count',
        prompt: 'Roughly how many specific textual references should a top answer include?',
        type: 'short-text',
        hint: 'Per paragraph — across 5-6 paragraphs.',
      },
    ],
    topAnswerIncludes: [
      'A single main theme identified clearly in the opening line',
      'Specific characters named, not "an príomhcharachtar"',
      'At least two quoted or paraphrased moments per paragraph',
      'A short closing paragraph linking the theme back to the title of the gearrscéal',
    ],
    commonTraps: [
      'Picking three or four themes and covering each shallowly',
      'Vague references like "sa scéal seo" without quoting specific moments',
    ],
  },
];
