/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Leaving Cert English exam questions for the Exam Strategiser.
 * 2025 Paper 1 (Higher Level), theme: Perspectives.
 */

import { type ExamQuestion } from '../../types/examStrategiser';

export const englishQuestions: ExamQuestion[] = [
  {
    id: 'english-2025-p1-text1-qa-iii',
    subject: 'english',
    year: 2025,
    paper: 'Paper 1',
    section: 'Section I — Comprehending — Text 1 (The Underdog Effect) Question A',
    questionNumber: '(iii)',
    level: 'higher',
    marks: 20,
    totalPaperMarks: 200,
    totalPaperMinutes: 170,
    commandWords: ['to what extent do you agree', 'support'],
    questionText: [
      {
        type: 'paragraph',
        content: [
          { text: '"In TEXT 1, David Robson uses elements of language that are effective in making this article both ' },
          { text: 'informative and thought-provoking', annotation: { note: 'Both qualities must be addressed across your answer — not necessarily equally, but ignoring one is penalised.', type: 'keyword' } },
          { text: '." ' },
          { text: 'To what extent do you agree', annotation: { note: 'Not yes/no. Take a position on the DEGREE (fully / largely / partly / disagree) and justify it. Bald agreement scores poorly.', type: 'command' } },
          { text: ' with this statement? Support your answer with reference to ' },
          { text: 'four elements of Robson\'s style', annotation: { note: 'Four is the explicit minimum. Style = HOW the writer writes (tone, statistics, anecdote, rhetorical questions, sentence structure, allusion) — NOT what they say.', type: 'keyword' } },
          { text: ' from the text. ' },
          { text: '(20)', annotation: { note: '20 marks → roughly 17 minutes. About 4 minutes per element plus 1 minute planning.', type: 'marks-allocation' } },
        ],
      },
    ],
    predictPrompts: [
      {
        id: 'p1',
        type: 'multiple-choice',
        prompt: "What's the command instruction in this question?",
        options: ['Describe', 'To what extent do you agree', 'Compare', 'Discuss'],
        correctAnswer: 'To what extent do you agree',
      },
      {
        id: 'p2',
        type: 'number',
        prompt: 'How many style elements must you discuss (minimum)?',
        correctAnswer: 4,
      },
      {
        id: 'p3',
        type: 'multiple-choice',
        prompt: 'Which counts as a "style element" rather than a "content point"?',
        options: ['The writer mentions Donald Trump', 'The writer uses statistics from a study', 'The underdog effect is real', 'Trump won in 2016'],
        correctAnswer: 'The writer uses statistics from a study',
      },
      {
        id: 'p4',
        type: 'short-text',
        prompt: 'The article must be shown to be both ___ and ___ (the two qualities in the statement).',
        hint: 'Informative and thought-provoking.',
      },
    ],
    topAnswerIncludes: [
      'A clear stance on the degree of agreement — not just "I agree"',
      'Four distinct style elements (e.g. statistics, anecdote, tone, rhetorical questions, allusion, sentence structure)',
      'For each element: identification + brief quote/reference + explanation of effect',
      'Both "informative" AND "thought-provoking" engaged with across the response',
      'Awareness of how form creates meaning — not just labelling techniques',
    ],
    commonTraps: [
      'Listing four content POINTS the writer makes instead of four STYLE elements',
      'Engaging with only one of the two qualities (informative OR thought-provoking, not both)',
      'Vague claims ("uses great language") with no quote or analysis',
      'Discussing fewer than four elements',
      'Pure agreement/disagreement with no engagement with degree',
    ],
    markScheme: 'P/C/L/M weighted 30/30/30/10. Examiner indicative material: factual information / statistics / real-life examples (informative); experimental research / studies / quotations (informative + thought-provoking); cultural illustrations / allusions; instructive / knowledgeable / personal tone; inclusive language / questions / emotive language (thought-provoking). Counter: too many examples can blur the argument.',
  },

  {
    id: 'english-2025-p1-text2-qb',
    subject: 'english',
    year: 2025,
    paper: 'Paper 1',
    section: 'Section I — Comprehending — Text 2 (Margaret Atwood) Question B',
    questionNumber: 'B',
    level: 'higher',
    marks: 50,
    totalPaperMarks: 200,
    totalPaperMinutes: 170,
    commandWords: ['outline', 'challenge', 'encourage'],
    questionText: [
      {
        type: 'paragraph',
        content: [
          { text: 'You are a hotel manager', annotation: { note: 'Adopt this register throughout — professional, confident, polished. Slipping into student voice loses Purpose marks.', type: 'keyword' } },
          { text: '. A recent, disgruntled guest has left a highly critical review of your hotel and its facilities on a travel-review website. You decide to challenge this person\'s views with an ' },
          { text: 'online response', annotation: { note: 'Genre = public-facing review reply (Tripadvisor / Google reviews vibe). Not a private letter. Other readers will see it.', type: 'keyword' } },
          { text: ' on the same website. In your response you should: ' },
        ],
      },
      {
        type: 'list-item',
        content: [
          { text: 'outline the proud tradition and history', annotation: { note: 'Task component 1 of 3. You MUST address this. Invent specific history details — founding year, family ownership, awards.', type: 'command' } },
          { text: ' of your establishment, ' },
        ],
      },
      {
        type: 'list-item',
        content: [
          { text: 'challenge the specific criticisms', annotation: { note: 'Task component 2 of 3. "Specific" is doing work — you need to invent plausible criticisms (cleanliness, service, food) and rebut each.', type: 'command' } },
          { text: ' of the guest reviewer, and ' },
        ],
      },
      {
        type: 'list-item',
        content: [
          { text: 'encourage the reviewer to return', annotation: { note: 'Task component 3 of 3. Forward-looking. Tone shifts from defence to invitation.', type: 'command' } },
          { text: ' by highlighting some of the ' },
          { text: 'exciting upcoming events', annotation: { note: 'Specific concrete events required — food festival, jazz weekend, local heritage week. Vague "we have lots of events" loses freshness marks.', type: 'keyword' } },
          { text: ' in your hotel and its locality. ' },
          { text: '(50)', annotation: { note: '50 marks → ~42 mins. P 15 / C 15 / L 15 / M 5. Plan structure before writing.', type: 'marks-allocation' } },
        ],
      },
    ],
    predictPrompts: [
      {
        id: 'p1',
        type: 'multiple-choice',
        prompt: 'What genre is required?',
        options: ['Personal letter', 'Online review response', 'Newspaper article', 'Speech'],
        correctAnswer: 'Online review response',
      },
      {
        id: 'p2',
        type: 'number',
        prompt: 'How many distinct task components must your answer address?',
        correctAnswer: 3,
      },
      {
        id: 'p3',
        type: 'multiple-choice',
        prompt: 'Which voice/register should dominate?',
        options: ['Casual student voice', 'Aggressive defensive', 'Professional hotel manager', 'Detached journalist'],
        correctAnswer: 'Professional hotel manager',
      },
      {
        id: 'p4',
        type: 'number',
        prompt: 'Roughly how many minutes should you spend on this?',
        correctAnswer: 42,
      },
    ],
    topAnswerIncludes: [
      'Sustained hotel-manager register — confident, professional, never grovelling or aggressive',
      'All three task components clearly addressed, in a logical order',
      'Specific invented detail — the hotel\'s history, the criticisms being challenged, the named events',
      'Public-facing awareness — written for OTHER potential guests reading the reply, not just the reviewer',
      'A clear structure: opening acknowledgement → pride/history → point-by-point rebuttal → invitation back',
    ],
    commonTraps: [
      'Slipping out of manager voice into the student\'s own register',
      'Addressing only one or two of the three task components',
      'Vague "you said bad things" instead of inventing specific criticisms to rebut',
      'Becoming aggressive or defensive — undermines register and Purpose marks',
      'Generic "events" with no concrete detail or local flavour',
      'Treating it as a private letter — losing the public, online dimension',
    ],
    markScheme: 'P 15 / C 15 / L 15 / M 5. P: register of hotel manager, all three task components addressed, relevance, originality. C: sustained focus, control of register, sequencing. L: quality of expression, fluency. M: spelling, grammar. Serious or humorous approaches both acceptable.',
  },

  {
    id: 'english-2025-p1-composing-2',
    subject: 'english',
    year: 2025,
    paper: 'Paper 1',
    section: 'Section II — Composing',
    questionNumber: '2',
    level: 'higher',
    marks: 100,
    totalPaperMarks: 200,
    totalPaperMinutes: 170,
    commandWords: ['write a speech', 'for or against'],
    questionText: [
      {
        type: 'paragraph',
        content: [
          { text: "The theme of this examination, 'Perspectives', explores how we see things in different ways." },
        ],
      },
      {
        type: 'paragraph',
        content: [
          { text: 'Write a speech', annotation: { note: 'Genre is FIXED. Must read like a SPOKEN speech — direct address, rhetorical devices, oral rhythm. Not an essay with quotes around it.', type: 'command' } },
          { text: ' ' },
          { text: 'for or against', annotation: { note: 'Pick ONE side. Hedging or arguing both sides equally is penalised under Purpose. Commit and defend.', type: 'keyword' } },
          { text: ' the motion that: "' },
          { text: 'Truth has become a valueless currency', annotation: { note: 'Engage with the metaphor — truth as something traded, devalued, debased. Don\'t just argue "is truth important?" — argue the specific currency framing.', type: 'keyword' } },
          { text: ' ' },
          { text: 'in today\'s world', annotation: { note: 'Contemporary references expected — fake news, AI deepfakes, social media, post-truth politics, recent named scandals or figures.', type: 'keyword' } },
          { text: '."  ' },
          { text: '(100)', annotation: { note: '100 marks → ~85 mins. The biggest single piece on Paper 1. P 30 / C 30 / L 30 / M 10.', type: 'marks-allocation' } },
        ],
      },
    ],
    predictPrompts: [
      {
        id: 'p1',
        type: 'multiple-choice',
        prompt: 'What is the required genre?',
        options: ['Personal essay', 'Speech', 'Discursive essay', 'Short story'],
        correctAnswer: 'Speech',
      },
      {
        id: 'p2',
        type: 'multiple-choice',
        prompt: 'Which approach scores highest?',
        options: ['Argue both sides equally', 'Argue ONE side only and commit', 'Stay neutral', 'Mostly one side, slightly the other'],
        correctAnswer: 'Argue ONE side only and commit',
      },
      {
        id: 'p3',
        type: 'short-text',
        prompt: 'Name two rhetorical devices a speech should use.',
        hint: 'Common ones: rhetorical question, anaphora (repetition), direct address, tricolon, anecdote, pathos, contrast.',
      },
      {
        id: 'p4',
        type: 'number',
        prompt: 'Roughly how many minutes should you spend on this?',
        correctAnswer: 85,
      },
    ],
    topAnswerIncludes: [
      'A clear committed stance — for OR against, not both',
      'Speech-genre features: opening hook, direct address, rhetorical questions, repetition, building rhythm, memorable close',
      'Contemporary, specific evidence (named figures, scandals, platforms, recent events)',
      'Audience awareness — written to be SPOKEN, not silently read',
      'Engagement with the metaphor of truth as "currency"',
      'A through-line — one developed central argument, not scattered points',
    ],
    commonTraps: [
      'Writing an essay rather than a speech — no audience, no oral rhythm',
      'Sitting on the fence — half for, half against',
      'Vague generalisations ("the modern world is bad") with no concrete examples',
      'Overloading with rhetorical devices to the point of melodrama',
      'Long sub-claused sentences that wouldn\'t survive a podium delivery',
      'Ignoring the "currency" framing and arguing a different question',
    ],
    markScheme: 'P 30 / C 30 / L 30 / M 10. P: focus on a speech for or against the motion, effective use of speech-writing elements (rhetorical devices, anecdotes, imagery, emotive/inclusive language, audience awareness), relevance, originality. C: shaped, developed, sustained. L: quality and control. M: accuracy.',
  },

  {
    id: 'english-2025-p1-composing-3',
    subject: 'english',
    year: 2025,
    paper: 'Paper 1',
    section: 'Section II — Composing',
    questionNumber: '3',
    level: 'higher',
    marks: 100,
    totalPaperMarks: 200,
    totalPaperMinutes: 170,
    commandWords: ['write a short story'],
    questionText: [
      {
        type: 'paragraph',
        content: [
          { text: "TEXT 1 analyses how the 'Underdog Effect' influences people's attitudes and behaviour." },
        ],
      },
      {
        type: 'paragraph',
        content: [
          { text: 'Write a short story', annotation: { note: 'Genre is FIXED. Narrative — plot, character, setting, conflict, resolution. Not an essay reflecting on underdogs.', type: 'command' } },
          { text: ' in which a "' },
          { text: 'plucky chancer', annotation: { note: 'Your protagonist must be unmistakably this — scrappy underdog with nerve. SHOW it through action and dialogue, don\'t TELL it ("she was very plucky").', type: 'keyword' } },
          { text: '" ' },
          { text: 'challenges', annotation: { note: 'Conflict is REQUIRED. Needs an actual confrontation, contest, or pursuit — not just internal musing.', type: 'keyword' } },
          { text: ' a more ' },
          { text: 'privileged or established opponent', annotation: { note: 'Antagonist with structural advantages. Their power must be visible — name, position, social capital. Avoid mustache-twirling caricature.', type: 'keyword' } },
          { text: '. ' },
          { text: '(100)', annotation: { note: '100 marks → ~85 mins. P 30 / C 30 / L 30 / M 10. Plan structure (5 mins) before writing.', type: 'marks-allocation' } },
        ],
      },
    ],
    predictPrompts: [
      {
        id: 'p1',
        type: 'multiple-choice',
        prompt: 'What genre is required?',
        options: ['Personal essay', 'Short story', 'Speech', 'Feature article'],
        correctAnswer: 'Short story',
      },
      {
        id: 'p2',
        type: 'multiple-choice',
        prompt: 'Which structural element is required?',
        options: ['Bibliography', 'Conflict between protagonist and opponent', 'Statistics', 'Counter-argument'],
        correctAnswer: 'Conflict between protagonist and opponent',
      },
      {
        id: 'p3',
        type: 'short-text',
        prompt: 'Name two short-story craft elements you would use.',
        hint: 'Setting, dialogue, tension, characterisation, atmosphere, narrative voice, resolution, sensory detail.',
      },
      {
        id: 'p4',
        type: 'multiple-choice',
        prompt: 'The opponent should be...',
        options: ['Equally matched', 'Younger and weaker', 'Privileged or established', 'Off-page entirely'],
        correctAnswer: 'Privileged or established',
      },
    ],
    topAnswerIncludes: [
      'A clearly drawn protagonist with underdog qualities — flaws AND determination, shown through action',
      'A clearly drawn opponent with visible structural power (name, position, social capital)',
      'A specific grounded setting (sport, courtroom, talent show, school, workplace)',
      'A genuine narrative arc — setup, escalation, crisis/contest, resolution',
      'Short-story craft: dialogue, sensory detail, tension, atmosphere',
      'Originality — the chancer doesn\'t have to win. Surprise the reader.',
    ],
    commonTraps: [
      'Writing a discursive essay ABOUT underdogs instead of a story FEATURING one',
      'Telling rather than showing ("she was plucky and determined")',
      'No real conflict — protagonist just musing or wandering',
      'Predictable Cinderella ending with no twist or specificity',
      'Overlong setup, rushed climax',
      'Caricature opponents — the privileged opponent should feel real, not cartoon villain',
    ],
    markScheme: 'P 30 / C 30 / L 30 / M 10. P: short story with plucky chancer challenging privileged opponent, effective use of narrative shape, setting, plot, characterisation, dialogue, tension, narrative voice, resolution. C: shaped, developed, sustained. L: quality and control. M: accuracy.',
  },
];
