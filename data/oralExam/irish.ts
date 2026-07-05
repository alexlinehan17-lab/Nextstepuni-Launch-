/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Leaving Cert Irish (Gaeilge) oral — content for the Oral Exam Trainer.
 *
 * All structural facts (components, marks, the 10-of-20 sraith pictiúr rule, the
 * five prescribed poems) are confirmed against primary SEC / Department of
 * Education documents for 2026 — see the `sources` list and
 * compliance/evidence/oral-trainer.md. The oral is a COMMON exam: identical at
 * Higher and Ordinary level. Conversation topics are the set students typically
 * prepare (a teaching convention), not an SEC-prescribed list, and are labelled
 * as such. Prescribed material is year-cycled — this is the 2026 set.
 */

import { type OralExam } from './types';

export const IRISH_ORAL: OralExam = {
  language: 'Irish',
  totalWeight: '240 marks — 40% of Leaving Cert Irish',
  intro:
    'The Irish oral (an scrúdú béil) is 40% of your Leaving Cert Irish — and it’s the part you can’t cram the night before. It takes rehearsal, out loud, over time. Work through each part below, practise speaking, and track where you feel ready. (Structure and prescribed material shown are for 2026.)',
  levelNote: 'It’s a common exam — the same components and marks at Higher and Ordinary level.',
  components: [
    {
      id: 'comhra',
      nameGa: 'An Comhrá',
      nameEn: 'General conversation',
      weight: '120 marks',
      whatItIs: 'A free general conversation with the examiner about you and your life — the biggest part of the oral.',
      prepTips: [
        'It’s the largest component — 120 of the 240 marks — so it’s worth the most preparation.',
        'Prepare a few reliable topics you can always talk about: yourself, your family, your home area, school, pastimes, and your plans after the Leaving Cert. (These are the topics students usually prepare — the conversation is free-ranging, not an official SEC checklist.)',
        'For each topic, have several sentences and a follow-up ready.',
        'Practise developing answers — say why, give an example. A developed answer scores far better than a one-liner.',
      ],
      prompts: [
        { en: 'Talk for a minute about yourself and your family.' },
        { en: 'Talk about your home area — what you like about it, and what you’d change.' },
        { en: 'Talk about your pastimes, and why you enjoy them.' },
        { en: 'Talk about what you hope to do after the Leaving Cert.' },
      ],
    },
    {
      id: 'sraith-pictiur',
      nameGa: 'An tSraith Pictiúr',
      nameEn: 'Picture sequence',
      weight: '80 marks',
      whatItIs: 'You describe a prepared picture sequence, telling the story from the first picture to the last.',
      prepTips: [
        'For 2026 you prepare 10 of the 20 official picture sequences; in the exam the examiner picks one of your prepared sequences to describe.',
        'Get the official 2026 sequences from your teacher or examinations.ie — then practise describing each one aloud.',
        'Narrate in order, usually in the past tense, using sequencing words (e.g. ar dtús, ansin, ina dhiaidh sin, ar deireadh).',
        'Time yourself — aim to tell a full sequence smoothly, without long pauses.',
      ],
      prompts: [
        { en: 'Describe one of your prepared picture sequences, from the first picture to the last.' },
        { en: 'Tell the story again, adding one extra detail to each picture this time.' },
      ],
    },
    {
      id: 'leamh-filiochta',
      nameGa: 'Léamh na Filíochta',
      nameEn: 'Reading the poetry',
      weight: '35 marks',
      whatItIs: 'You read one of the five prescribed poems aloud — you read it (the text is in front of you); it isn’t recited from memory.',
      prepTips: [
        'The five prescribed poems for 2026 are: An Spailpín Fánach (verses 1–3), Géibheann (Caitlín Maude), An tEarrach Thiar (Máirtín Ó Direáin), Mo Ghrá-sa (idir lúibíní) (Nuala Ní Dhomhnaill), and Colscaradh (Pádraig Mac Suibhne).',
        'You read the poem aloud — it is not recited from memory — so focus on clear, confident pronunciation and rhythm.',
        'Record yourself reading each one and listen back for the words you stumble on.',
      ],
      prompts: [
        { en: 'Read one of the five prescribed poems aloud, slowly and clearly.' },
        { en: 'Read it again, focusing on the words you stumbled on last time.' },
      ],
    },
    {
      id: 'failtiu',
      nameGa: 'An Fáiltiú',
      nameEn: 'The greeting',
      weight: '5 marks',
      whatItIs: 'The examiner greets you, confirms your exam number and eases you in.',
      prepTips: [
        'It’s worth 5 marks — small, but a calm, clear start sets the tone for the whole exam.',
        'Rehearse greeting the examiner and giving your details steadily and confidently.',
      ],
      prompts: [
        { en: 'Greet the examiner and give your name and exam number — calmly and clearly.' },
      ],
    },
  ],
  sources: [
    { label: 'SEC Assessment Arrangements 2026', url: 'https://assets.gov.ie/static/documents/2c504db1/Assessment_Doc_EN_2026.pdf' },
    { label: 'Prescribed Material circular 0026/2024', url: 'https://assets.gov.ie/288543/d803ad6c-6573-4026-91a6-9dc1d05197dd.pdf' },
  ],
};
