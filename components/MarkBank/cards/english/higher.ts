/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * English Mark Bank — first complete paper batch.
 *
 * This file cards EVERY printed ask and choice on 2025 Higher Level Paper 1:
 * 9 Question A parts, 3 Question B tasks and all 7 composing choices.
 * Coverage is checked against english-census.json; a convenient subset was not
 * selected.
 *
 * English marking is not converted into exact-answer rows. Short answers use
 * the published combined grade grid; longer answers use discrete PCLM with the
 * primacy-of-Purpose cap. SEC indicative material is carried only as explicitly
 * non-exhaustive possible directions and can never be claimed as marks.
 */

import type {
  CardSourceMaterial,
  PclmCriterion,
  PclmGradeBand,
  SecRubricCard,
} from '../../../../types/markBank';

const range = (from: number, to: number) =>
  Array.from({ length: to - from + 1 }, (_, index) => from + index);

const bands = (total: 15 | 20 | 50 | 100): PclmGradeBand[] => {
  if (total === 15) return [
    { grade: 'H1', marks: [14, 15] }, { grade: 'H2', marks: [12] },
    { grade: 'H3', marks: [11] }, { grade: 'H4', marks: [9] },
    { grade: 'H5', marks: [8] }, { grade: 'H6', marks: [6] },
    { grade: 'H7', marks: [5] }, { grade: 'H8', marks: range(0, 4) },
  ];
  if (total === 20) return [
    { grade: 'H1', marks: range(18, 20) }, { grade: 'H2', marks: [16] },
    { grade: 'H3', marks: [14] }, { grade: 'H4', marks: [12] },
    { grade: 'H5', marks: [10] }, { grade: 'H6', marks: [8] },
    { grade: 'H7', marks: [6] }, { grade: 'H8', marks: range(0, 5) },
  ];
  if (total === 50) return [
    { grade: 'H1', marks: range(45, 50) }, { grade: 'H2', marks: range(40, 44) },
    { grade: 'H3', marks: range(35, 39) }, { grade: 'H4', marks: range(30, 34) },
    { grade: 'H5', marks: range(25, 29) }, { grade: 'H6', marks: range(20, 24) },
    { grade: 'H7', marks: range(15, 19) }, { grade: 'H8', marks: range(0, 14) },
  ];
  return [
    { grade: 'H1', marks: range(90, 100) }, { grade: 'H2', marks: range(80, 89) },
    { grade: 'H3', marks: range(70, 79) }, { grade: 'H4', marks: range(60, 69) },
    { grade: 'H5', marks: range(50, 59) }, { grade: 'H6', marks: range(40, 49) },
    { grade: 'H7', marks: range(30, 39) }, { grade: 'H8', marks: range(0, 29) },
  ];
};

const INDICATIVE_NOTE =
  'SEC describes these as broad examples for examiners. Valid alternatives must be judged on their merits; none is a required answer.';

const COMBINED_CRITERIA = [
  'Clear, purposeful engagement with the exact task',
  'A sustained and coherently developed response',
  'Language managed and controlled for the task',
  'Spelling and grammar appropriate to the register',
];

const TEXT_1_SOURCE: CardSourceMaterial = {
  kind: 'source-text',
  label: 'TEXT 1',
  title: 'The Underdog Effect — Changing Perspectives',
  pages: [2, 3],
  attribution: 'David Robson, BBC Essential, August 2024.',
  presentationNote: 'Official 2025 SEC examination layout; edited for assessment.',
};

const TEXT_2_SOURCE: CardSourceMaterial = {
  kind: 'source-text',
  label: 'TEXT 2',
  title: 'The Perspective of a ‘Wise Old Counsellor’',
  pages: [4, 5],
  attribution: 'Margaret Atwood, One Young World Congress, Montreal, September 2024.',
  presentationNote: 'Official 2025 SEC examination layout; edited for assessment.',
};

const TEXT_3_SOURCE: CardSourceMaterial = {
  kind: 'source-text',
  label: 'TEXT 3',
  title: 'Planet Earth from the Perspective of Space',
  pages: [6, 7],
  attribution: 'Samantha Harvey, Orbital, Jonathan Cape, 2023.',
  presentationNote: 'Official 2025 SEC examination layout; edited for assessment.',
};

const permitted = (max: 5 | 10 | 15 | 30) => {
  if (max === 5) return range(0, 5);
  if (max === 10) return range(0, 10);
  if (max === 15) return [...range(0, 6), 8, 9, 11, 12, 14, 15];
  return [...range(0, 9), 12, 15, 18, 21, 24, 27, 28, 29, 30];
};

const discreteCriteria = (
  total: 50 | 100,
  purpose: string[],
  coherence: string[] = ['Sustained focus and control of register', 'Management and sequencing of ideas'],
): PclmCriterion[] => {
  const main = total === 50 ? 15 : 30;
  const mechanics = total === 50 ? 5 : 10;
  return [
    { id: 'purpose', label: 'Clarity of Purpose', maxMarks: main, guidance: purpose, permittedMarks: permitted(main) },
    { id: 'coherence', label: 'Coherence of Delivery', maxMarks: main, guidance: coherence, permittedMarks: permitted(main) },
    {
      id: 'language', label: 'Efficiency of Language Use', maxMarks: main,
      guidance: ['Language managed and controlled to communicate clearly', 'Quality of expression, style and fluency'],
      permittedMarks: permitted(main),
    },
    {
      id: 'mechanics', label: 'Accuracy of Mechanics', maxMarks: mechanics,
      guidance: ['Accuracy of spelling and grammar appropriate to the chosen register'],
      permittedMarks: permitted(mechanics),
    },
  ];
};

interface CardArgs {
  id: string;
  conceptId: string;
  topicId: 'english-9-1' | 'english-10-0' | 'english-10-1';
  ref: string;
  text: string;
  marks: 15 | 20 | 50 | 100;
  page: number;
  source?: CardSourceMaterial;
  requirements: string[];
  indicative?: string[];
  purpose?: string[];
  coherence?: string[];
}

const makeCard = (args: CardArgs): SecRubricCard => ({
  id: args.id,
  subjectId: 'english',
  level: 'higher',
  topicId: args.topicId,
  conceptId: args.conceptId,
  source: 'sec',
  kind: 'rubric',
  year: 2025,
  // Resolved from Paper Trail's 2025 English Higher entry. The source reader
  // uses this same question-paper document; it never points at the scheme.
  paperFileid: 'LC002ALP100EV',
  section: '1',
  questionRef: args.ref,
  sourceMaterial: args.source,
  questionText: args.text,
  totalMarks: args.marks,
  schemeCitation: `SEC English Higher Level marking scheme 2025, p.${args.page} — © State Examinations Commission.`,
  specVersion: 'english:outgoing',
  qa: {
    gates: ['verbatim', 'pclm-grid', 'indicative-not-checklist', 'paper-census'],
    humanReviewedBy: 'agent-verified',
    humanReviewedAt: '2026-08-30',
  },
  rubric: {
    system: 'pclm',
    taskRequirements: args.requirements,
    assessment: args.marks === 15 || args.marks === 20
      ? { mode: 'combined', bands: bands(args.marks), criteria: COMBINED_CRITERIA }
      : {
          mode: 'discrete',
          bands: bands(args.marks),
          criteria: discreteCriteria(args.marks, args.purpose ?? args.requirements, args.coherence),
          primacyOfPurpose: true,
        },
    indicativeMaterial: args.indicative,
    indicativeMaterialNote: INDICATIVE_NOTE,
  },
});

export const CARDS: SecRubricCard[] = [
  // ── Text 1 · The Underdog Effect ──────────────────────────────────────────
  makeCard({
    id: 'english-2025-hl-p1-t1-a-i', conceptId: 'english-comprehending-insights',
    topicId: 'english-10-0', ref: '2025 HL Paper 1 Text 1 QA(i)', marks: 15, page: 4,
    source: TEXT_1_SOURCE,
    text: 'Based on your reading of TEXT 1, what insights do you gain about how the ‘underdog effect’ can influence our perspectives? Make three points, supporting your response with reference to the text.',
    requirements: ['Explain three insights about how the ‘underdog effect’ can influence perspectives', 'Support the response with reference to TEXT 1'],
    indicative: [
      'It can heighten empathy or create an emotional bias towards the underdog.',
      'It can shape opinions about people and issues by making weak-over-strong outcomes attractive.',
      'It can be framed strategically to gain advantage, including influencing voting intentions.',
      'It can determine support in sport.',
      'It can fuel a sense of injustice or inspire belief in hard work and possibility.',
      'It can make people defy the apparently rational choice of the stronger side.',
    ],
  }),
  makeCard({
    id: 'english-2025-hl-p1-t1-a-ii', conceptId: 'english-comprehending-viewpoint',
    topicId: 'english-10-0', ref: '2025 HL Paper 1 Text 1 QA(ii)', marks: 15, page: 5,
    source: TEXT_1_SOURCE,
    text: 'To what extent do you agree with the writer’s claim, in TEXT 1, that humankind has a “fixation on status and prestige”? Develop at least two points in your response.',
    requirements: ['Take a clear position on the extent of agreement or disagreement', 'Develop at least two points', 'Address the claim about humankind’s “fixation on status and prestige”'],
  }),
  makeCard({
    id: 'english-2025-hl-p1-t1-a-iii', conceptId: 'english-comprehending-style',
    topicId: 'english-10-0', ref: '2025 HL Paper 1 Text 1 QA(iii)', marks: 20, page: 5,
    source: TEXT_1_SOURCE,
    text: '“In TEXT 1, David Robson uses elements of language that are effective in making this article both informative and thought-provoking.” To what extent do you agree with this statement? Support your answer with reference to four elements of Robson’s style from the text.',
    requirements: ['Judge the extent to which the statement is convincing', 'Engage with both “informative” and “thought-provoking”', 'Discuss four elements of Robson’s style', 'Support the response with reference to TEXT 1'],
    indicative: [
      'Factual information, statistics and real-life examples.',
      'Research, studies, reports and quotations.',
      'Cultural illustrations and media allusions.',
      'An instructive, knowledgeable or personal tone.',
      'Inclusive language, questions, summative sentences or emotive language.',
      'A critical view that too many examples, quotations or studies may blur the argument.',
    ],
  }),
  makeCard({
    id: 'english-2025-hl-p1-t1-b', conceptId: 'english-functional-team-talk',
    topicId: 'english-10-1', ref: '2025 HL Paper 1 Text 1 QB', marks: 50, page: 6,
    text: 'You are the captain of a school’s sports team, about to compete, as the underdogs, in the final of a national competition and you are required to give the pre-match team-talk. Write the text of the talk that you would deliver. In your talk you should: outline to your team mates aspects of the game plan you have decided to employ on the field, remind them of the strengths and weaknesses of your opponents, and motivate them to overcome the odds and to achieve victory.',
    requirements: ['Write a pre-match team-talk in the voice and register of the school team captain', 'Outline aspects of the game plan', 'Address the opponents’ strengths and weaknesses', 'Motivate the team to overcome the odds and achieve victory'],
    purpose: ['Understanding of the team-talk genre and captain-to-team register', 'Focus on every required aspect of the task', 'Relevance, freshness and originality'],
  }),

  // ── Text 2 · Margaret Atwood ──────────────────────────────────────────────
  makeCard({
    id: 'english-2025-hl-p1-t2-a-i', conceptId: 'english-comprehending-insights',
    topicId: 'english-10-0', ref: '2025 HL Paper 1 Text 2 QA(i)', marks: 15, page: 7,
    source: TEXT_2_SOURCE,
    text: 'Based on your reading of TEXT 2 what insights do you gain about Margaret Atwood’s perspective on current world problems? Make three points, supporting your response with reference to the text.',
    requirements: ['Explain three insights into Atwood’s perspective on current world problems', 'Support the response with reference to TEXT 2'],
    indicative: [
      'Past knowledge gives her perspective and supports a hopeful view that things have been worse.',
      'Hard work and involvement are necessary; people cannot sit back.',
      'She sees grounds for optimism in innovation and new approaches.',
      'Beneficial action must be local, grounded and part of real lives.',
      'Local action and international cooperation must work together.',
      'No single person or group can solve world problems alone.',
    ],
  }),
  makeCard({
    id: 'english-2025-hl-p1-t2-a-ii', conceptId: 'english-comprehending-viewpoint',
    topicId: 'english-10-0', ref: '2025 HL Paper 1 Text 2 QA(ii)', marks: 15, page: 7,
    source: TEXT_2_SOURCE,
    text: 'To what extent do you agree with the observation, in TEXT 2, that in order to address world problems, “all beneficial actions must be local and grounded”? Develop at least two points in your response.',
    requirements: ['Take a clear position on the extent of agreement or disagreement', 'Develop at least two points', 'Address whether beneficial action must be “local and grounded”'],
  }),
  makeCard({
    id: 'english-2025-hl-p1-t2-a-iii', conceptId: 'english-comprehending-style',
    topicId: 'english-10-0', ref: '2025 HL Paper 1 Text 2 QA(iii)', marks: 20, page: 8,
    source: TEXT_2_SOURCE,
    text: '“In TEXT 2, Margaret Atwood uses elements of language that are effective in making this speech both engaging and inspiring.” To what extent do you agree with this statement? Support your answer with reference to four elements of Atwood’s style from the text.',
    requirements: ['Judge the extent to which the statement is convincing', 'Engage with both “engaging” and “inspiring”', 'Discuss four elements of Atwood’s style', 'Support the response with reference to TEXT 2'],
    indicative: [
      'Humour, self-reference and asides.',
      'A personal or self-deprecating tone, voice and colloquialisms.',
      'Factual information, lists and historical references.',
      'Imagery, emotive examples, illustrations and allusions.',
      'Direct address, questions, repetition, rhythm or cadence.',
      'A critical view that flippancy may undercut the seriousness of the content.',
    ],
  }),
  makeCard({
    id: 'english-2025-hl-p1-t2-b', conceptId: 'english-functional-online-response',
    topicId: 'english-10-1', ref: '2025 HL Paper 1 Text 2 QB', marks: 50, page: 9,
    text: 'You are a hotel manager. A recent, disgruntled guest has left a highly critical review of your hotel and its facilities on a travel-review website. You decide to challenge this person’s views with an online response on the same website. In your response you should: outline the proud tradition and history of your establishment, challenge the specific criticisms of the guest reviewer, and encourage the reviewer to return by highlighting some of the exciting upcoming events in your hotel and its locality.',
    requirements: ['Write an online response in the voice and register of the hotel manager', 'Outline the establishment’s proud tradition and history', 'Challenge the reviewer’s specific criticisms', 'Encourage a return by highlighting upcoming events in the hotel and locality'],
    purpose: ['Understanding of an online response and the hotel-manager register', 'Focus on every required aspect of the task', 'Relevance, freshness and originality'],
  }),

  // ── Text 3 · Orbital ──────────────────────────────────────────────────────
  makeCard({
    id: 'english-2025-hl-p1-t3-a-i', conceptId: 'english-comprehending-insights',
    topicId: 'english-10-0', ref: '2025 HL Paper 1 Text 3 QA(i)', marks: 15, page: 10,
    source: TEXT_3_SOURCE,
    text: 'Based on your reading of TEXT 3 what insights do you gain about planet Earth by viewing it from the perspective of space? Make three points, supporting your response with reference to the text.',
    requirements: ['Explain three insights about Earth viewed from space', 'Support the response with reference to TEXT 3'],
    indicative: [
      'Earth’s beauty appears majestic or regal.',
      'It seems protective like a mother while also needing protection.',
      'Distance makes it appear harmonious and peaceful as divisions disappear.',
      'Its variety of landscapes and colours becomes striking.',
      'It is placed within a larger universe and phase of exploration.',
      'The view puts the role and importance of human beings into perspective.',
    ],
  }),
  makeCard({
    id: 'english-2025-hl-p1-t3-a-ii', conceptId: 'english-comprehending-viewpoint',
    topicId: 'english-10-0', ref: '2025 HL Paper 1 Text 3 QA(ii)', marks: 15, page: 10,
    source: TEXT_3_SOURCE,
    text: 'To what extent do you agree with the view, in TEXT 3, that, “striking out, further and deeper” into space is worthwhile? Develop at least two points in your response.',
    requirements: ['Take a clear position on the extent of agreement or disagreement', 'Develop at least two points', 'Address whether deeper space exploration is worthwhile'],
  }),
  makeCard({
    id: 'english-2025-hl-p1-t3-a-iii', conceptId: 'english-comprehending-style',
    topicId: 'english-10-0', ref: '2025 HL Paper 1 Text 3 QA(iii)', marks: 20, page: 11,
    source: TEXT_3_SOURCE,
    text: '“In TEXT 3, Samantha Harvey uses elements of language that are effective in making the writing in this passage both elegant and thought-provoking.” To what extent do you agree with this statement? Support your answer with reference to four elements of Harvey’s style from the text.',
    requirements: ['Judge the extent to which the statement is convincing', 'Engage with both “elegant” and “thought-provoking”', 'Discuss four elements of Harvey’s style', 'Support the response with reference to TEXT 3'],
    indicative: [
      'Figurative language such as imagery, simile, metaphor and personification.',
      'Descriptive language, colour, adjectives and listing.',
      'Places, contrasts and questions that create a philosophical or meditative tone.',
      'Alliteration and repetition that give the passage a lyrical quality.',
      'Characterisation of Nell, Roman or human beings as a thought-provoking device.',
      'A critical view that excessive figurative or descriptive writing may weaken the impact.',
    ],
  }),
  makeCard({
    id: 'english-2025-hl-p1-t3-b', conceptId: 'english-functional-podcast-reflection',
    topicId: 'english-10-1', ref: '2025 HL Paper 1 Text 3 QB', marks: 50, page: 12,
    text: 'You are a contributor to a podcast entitled, ‘Eyes Wide Open’, where you reflect on how your perspective on a significant issue changed as a result of an experience or an encounter. Write your reflection for the podcast in which you: identify the issue and explain your previous attitude towards it, describe the experience or encounter that changed your perspective, and consider some of the life lessons that you and others can learn from this reflection.',
    requirements: ['Write a reflective podcast contribution in an appropriate register', 'Identify a significant issue and explain the previous attitude towards it', 'Describe the experience or encounter that changed the perspective', 'Consider life lessons for the writer and others'],
    purpose: ['Understanding of a reflective podcast piece and its register', 'Focus on every required aspect of the task', 'Relevance, freshness and originality'],
  }),

  // ── Section II · every composing choice ──────────────────────────────────
  makeCard({
    id: 'english-2025-hl-p1-composing-1', conceptId: 'english-composing-discursive',
    topicId: 'english-9-1', ref: '2025 HL Paper 1 Composing 1', marks: 100, page: 14,
    text: 'In TEXT 3, Nell and her husband exchange photographs as a means of staying close while they are far apart. Write a discursive essay in which you consider the power and value of both printed and digital photographic images today.',
    requirements: ['Write a discursive essay', 'Consider both the power and the value of photographic images', 'Address both printed and digital images', 'Keep the discussion grounded in the present day'],
    purpose: ['Focus on the power and value of both printed and digital photographic images today', 'Controlled use of discursive writing, such as multiple perspectives, argument and counter-argument, evidence, examples or personal experience', 'Relevance, originality and freshness'],
    coherence: ['Successfully shape, develop and sustain the discussion', 'Sequence and manage ideas effectively'],
  }),
  makeCard({
    id: 'english-2025-hl-p1-composing-2', conceptId: 'english-composing-speech',
    topicId: 'english-9-1', ref: '2025 HL Paper 1 Composing 2', marks: 100, page: 15,
    text: 'The theme of this examination, ‘Perspectives’, explores how we see things in different ways. Write a speech for or against the motion that: “Truth has become a valueless currency in today’s world.”',
    requirements: ['Write a speech', 'Argue either for or against the motion, not both sides as the adopted position', 'Address the value of truth in today’s world', 'Use argument and persuasion for an audience'],
    purpose: ['Focus on a speech for or against the stated motion', 'Controlled speech-writing features such as audience awareness, references, rhetoric, anecdotes, imagery or inclusive and emotive language', 'Relevance, originality and freshness'],
    coherence: ['Successfully shape, develop and sustain the speech', 'Sequence and manage ideas effectively'],
  }),
  makeCard({
    id: 'english-2025-hl-p1-composing-3', conceptId: 'english-composing-short-story',
    topicId: 'english-9-1', ref: '2025 HL Paper 1 Composing 3', marks: 100, page: 16,
    text: 'TEXT 1 analyses how the ‘Underdog Effect’ influences people’s attitudes and behaviour. Write a short story in which a “plucky chancer” challenges a more privileged or established opponent.',
    requirements: ['Write a short story', 'Feature a “plucky chancer”', 'Have that character challenge a more privileged or established opponent'],
    purpose: ['Focus on the required challenge between the “plucky chancer” and opponent', 'Controlled short-story features such as narrative shape, setting, plot, characterisation, atmosphere, dialogue, tension, voice or resolution', 'Relevance, originality and freshness'],
    coherence: ['Successfully shape, develop and sustain the narrative', 'Sequence and manage ideas effectively'],
  }),
  makeCard({
    id: 'english-2025-hl-p1-composing-4', conceptId: 'english-composing-personal-essay',
    topicId: 'english-9-1', ref: '2025 HL Paper 1 Composing 4', marks: 100, page: 17,
    text: 'In TEXT 1 the writer asks why we would, “willingly put ourselves through disappointment”. Write a personal essay in which you reflect on some of the disappointments you have experienced and the impact they have had on you.',
    requirements: ['Write a personal essay', 'Reflect on more than one disappointment', 'Explore the impact those disappointments had on you'],
    purpose: ['Focus on personal reflection about disappointments and their impact', 'Controlled personal-writing features such as first-person voice, reflection, insight, authentic observation or anecdote', 'Relevance, originality and freshness'],
    coherence: ['Successfully shape, develop and sustain the personal approach', 'Sequence and manage ideas effectively'],
  }),
  makeCard({
    id: 'english-2025-hl-p1-composing-5', conceptId: 'english-composing-feature-article',
    topicId: 'english-9-1', ref: '2025 HL Paper 1 Composing 5', marks: 100, page: 18,
    text: 'In TEXT 2 Margaret Atwood tells young people, “you’ve got the energy and optimism to take on the challenge.” Write a feature article entitled, ‘A love letter to Ireland’ in which you explore some of the reasons why we should view contemporary Irish society through an optimistic lens.',
    requirements: ['Write a feature article entitled “A love letter to Ireland”', 'Explore more than one reason for optimism', 'Focus on contemporary Irish society', 'Adopt an optimistic lens'],
    purpose: ['Focus on reasons to view contemporary Irish society through an optimistic lens', 'Controlled article-writing features such as engaging style, personal observations, facts, references, anecdotes, imagery or humour', 'Relevance, originality and freshness'],
    coherence: ['Successfully shape, develop and sustain the article', 'Sequence and manage ideas effectively'],
  }),
  makeCard({
    id: 'english-2025-hl-p1-composing-6', conceptId: 'english-composing-personal-essay',
    topicId: 'english-9-1', ref: '2025 HL Paper 1 Composing 6', marks: 100, page: 19,
    text: 'In TEXT 2 Margaret Atwood refers to cherishing, “democratic elections”. Write a personal essay in which you reflect on some of the factors that would influence your voting intentions in future elections.',
    requirements: ['Write a personal essay', 'Reflect on more than one factor', 'Explain how those factors would influence future voting intentions'],
    purpose: ['Focus on personal reflection about factors influencing future voting intentions', 'Controlled personal-writing features such as first-person voice, reflection, insight, authentic observation or anecdote', 'Relevance, originality and freshness'],
    coherence: ['Successfully shape, develop and sustain the personal approach', 'Sequence and manage ideas effectively'],
  }),
  makeCard({
    id: 'english-2025-hl-p1-composing-7', conceptId: 'english-composing-short-story',
    topicId: 'english-9-1', ref: '2025 HL Paper 1 Composing 7', marks: 100, page: 20,
    text: 'In TEXT 3, the character Roman thinks that – “A human being was not made to stand still.” Write a short story featuring an ambitious character whose reckless actions lead to disaster.',
    requirements: ['Write a short story', 'Feature an ambitious character', 'Make the character’s actions reckless', 'Have those actions lead to disaster'],
    purpose: ['Focus on an ambitious character whose reckless actions lead to disaster', 'Controlled short-story features such as narrative shape, setting, plot, characterisation, atmosphere, dialogue, tension, voice or resolution', 'Relevance, originality and freshness'],
    coherence: ['Successfully shape, develop and sustain the narrative', 'Sequence and manage ideas effectively'],
  }),
];
