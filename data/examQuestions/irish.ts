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
    taskType: 'irish-literature-essay',
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
        debrief: {
          strategicPrinciple: 'Pléigh = Discuss. Like English "Discuss", the command demands balanced analysis with reference to specific moments in the text — not a plot summary. A position taken and defended, with multiple textual moments to support it.',
          commonWrongAnswer: {
            answer: 'Summarise',
            reason: 'Treating Pléigh as "retell the story" produces a plot summary rather than discussion of the chosen theme. Plot retelling without analysis caps in the lower marking bands regardless of how thorough the recount.',
          },
        },
      },
      {
        id: 'time-allocation',
        prompt: 'How many minutes should you spend on this question?',
        type: 'number',
        correctAnswer: 45,
        hint: '50 marks out of 200 on a 180-minute paper.',
        debrief: {
          strategicPrinciple: 'Paper 2 Litríocht runs at 0.9 minutes per mark (180 min / 200 marks). A 50-mark essay gets 45 minutes — roughly 7-8 minutes per paragraph across 5-6 paragraphs plus a tight opening and closing.',
          commonWrongAnswer: {
            answer: '30',
            reason: 'Under-budgets a quarter-of-the-paper question. The per-mark rate gives 45 minutes for a 50-mark essay; going under leaves the essay thin (not enough textual reference); going over starves the next question on the paper.',
          },
        },
      },
      {
        id: 'reference-count',
        prompt: 'Roughly how many specific textual references should a top answer include?',
        type: 'short-text',
        hint: 'Per paragraph — across 5-6 paragraphs.',
        debrief: {
          strategicPrinciple: 'Two specific textual references per paragraph across 5-6 paragraphs = 10-12 quoted or paraphrased moments. Vague "sa scéal seo" or "an príomhcharachtar" without naming costs you in the content and language bands.',
          commonWrongAnswer: {
            answer: 'One per paragraph',
            reason: 'Halves your evidence density. The marking convention for Irish literature essays rewards specific reference — two per paragraph keeps every claim anchored. Single references per paragraph read as general assertion supported by one moment, rather than theme analysis grounded in the text.',
          },
        },
      },
    ],
    biggestMistake: {
      title: 'Vague references and plot summary instead of theme analysis',
      body: 'Pléigh asks for discussion of ONE main theme with specific evidence from the gearrscéal. Two patterns consistently cap students: (a) covering three or four themes shallowly instead of one in depth, and (b) using vague references like "sa scéal seo" or "an príomhcharachtar" without naming characters or quoting moments. Pick one theme, write 5-6 paragraphs, two specific references in each — names, quoted phrases, exchanges, decisions.',
    },
  },
];
