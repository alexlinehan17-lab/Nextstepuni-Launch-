/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The end-of-session quiz asks only short, real Mark Bank questions on what
 * was studied, and scores a tick exactly as Mark Bank does.
 */

import { describe, expect, test } from 'vitest';
import { QUIZ_SIZE, isQuizCard, planQuiz, quizPool, quizTopicLabel, resolveQuizDeck, loadQuiz, preferShortQuestions } from '@/components/study/quiz/studyQuizPlan';
import { loadCards } from '@/components/MarkBank/deck';
import { cardsForCurriculumNode } from '@/components/MarkBank/curriculumMenu';
import { CURRICULUM_SPECIFICATIONS, type CanonicalCurriculumSpecification } from '@/curriculumRegistry';
import type { SecCard, SecQuestionCard } from '@/types/markBank';

const base = {
  source: 'sec' as const,
  subjectId: 'chemistry',
  level: 'ordinary' as const,
  year: 2021,
  paperFileid: 'LC022GLP000EV',
  section: 'B' as const,
  schemeCitation: 'Marking points quoted from the SEC marking scheme, Chemistry 2021 Ordinary Level — © State Examinations Commission.',
  specVersion: 'chemistry:2022',
  qa: { gates: [], humanReviewedBy: 'test', humanReviewedAt: '2026-10-23' },
  conceptId: 'c',
};

const point = (id: string, topicId: string, extra: Partial<SecQuestionCard> = {}): SecQuestionCard => ({
  ...base, kind: 'question', id, topicId, questionRef: `2021 OL ${id}`,
  questionText: `Question ${id}`, tariffModel: { kind: 'fixed' }, totalMarks: 6,
  rows: [{ id: `${id}-r1`, kind: 'point', verbatim: 'planar', marks: 6 }],
  ...extra,
});

const simple = point('q1', 'chem-2-2');
const grouped = point('q2', 'chem-2-2', {
  totalMarks: 8,
  rows: [
    { id: 'q2-r1', kind: 'anyN', verbatim: 'Any two of', marks: 6, group: { claimMax: 2, perOption: 3, options: ['one', 'two', 'three', 'four'] } },
    { id: 'q2-r2', kind: 'point', verbatim: 'units', marks: 2 },
  ],
});
const stepped = point('q3', 'chem-3-1', {
  rows: [{ id: 'q3-r1', kind: 'criterion', verbatim: 'Diagram', marks: 6, permittedMarks: [0, 3, 6] }],
});
const descending = point('q4', 'chem-3-1', {
  totalMarks: 10,
  rows: [{ id: 'q4-r1', kind: 'anyN', verbatim: 'Two consequences', marks: 10, group: { claimMax: 2, perOption: 6, perOptionSteps: [6, 4], options: ['a', 'b', 'c'] } }],
});
const dependent = point('q5', 'chem-3-1', {
  rows: [
    { id: 'q5-r1', kind: 'point', verbatim: 'name', marks: 3 },
    { id: 'q5-r2', kind: 'point', verbatim: 'justify', marks: 3, dependsOn: 'q5-r1' },
  ],
});
const crossListed = point('q6', 'chem-1-1', { additionalTopicIds: ['chem-2-2'] });

const tooLong = point('x1', 'chem-2-2', { totalMarks: 15 });
const split = point('x2', 'chem-2-2', { tariffModel: { kind: 'orderedSplit', notation: '3, 3' } });
const withSource = point('x3', 'chem-2-2', {
  sourceMaterial: { kind: 'source-text', label: 'Q', title: 'Passage', pages: [2], attribution: 'SEC', presentationNote: '' },
});
const routed = point('x4', 'chem-2-2', {
  rows: [
    { id: 'x4-r1', kind: 'point', verbatim: 'via moles', marks: 6, route: 'A' },
    { id: 'x4-r2', kind: 'point', verbatim: 'via mass', marks: 6, route: 'B' },
  ],
});
const unpriced = point('x5', 'chem-2-2', { rows: [{ id: 'x5-r1', kind: 'point', verbatim: 'scale', marks: null }] });
const rubric = {
  ...base, kind: 'rubric', id: 'x6', topicId: 'chem-2-2', questionRef: 'x6', questionText: 'Essay', totalMarks: 8,
  rubric: { system: 'geography', taskRequirements: [], guidanceKind: 'exact', schemeGuidance: [] },
} as unknown as SecCard;

const all: SecCard[] = [simple, grouped, stepped, descending, dependent, crossListed, tooLong, split, withSource, routed, unpriced, rubric];

const spec = {
  id: 'chemistry:2022', subjectId: 'chemistry', subjectName: 'Chemistry',
  groups: [
    { id: 'chemistry:cs2', title: 'Strand 2', topics: [{ id: 'chem-2-2', title: 'Bonding' }] },
    { id: 'chemistry:cs3', title: 'Strand 3', topics: [{ id: 'chem-3-1', title: 'Thermochemistry' }] },
  ],
} as unknown as CanonicalCurriculumSpecification;

describe('which questions qualify', () => {
  test('native point and rubric cards qualify, including long tasks, sources and answer routes', () => {
    expect(all.filter(isQuizCard).map(card => card.id)).toEqual(['q1', 'q2', 'q3', 'q4', 'q5', 'q6', 'x1', 'x3', 'x4', 'x6']);
  });

  test('topics narrow the pool, a whole area expands to its topics, and cross-listed cards count once', () => {
    expect(quizPool(all, ['chem-2-2'], spec).map(card => card.id)).toEqual(['q1', 'q2', 'q6', 'x1', 'x3', 'x4', 'x6']);
    expect(quizPool(all, ['chemistry:cs3'], spec).map(card => card.id)).toEqual(['q3', 'q4', 'q5']);
    expect(quizPool(all, ['chem-2-2', 'chemistry:cs2'], spec).map(card => card.id)).toEqual(['q1', 'q2', 'q6', 'x1', 'x3', 'x4', 'x6']);
    expect(quizPool(all, []).length).toBe(10);
  });

  test('one or two matches are enough; queues remain bounded and stable', () => {
    const pool = quizPool(all, [], undefined);
    expect(planQuiz([], {}, 1_000)).toEqual([]);
    expect(planQuiz(pool.slice(0, 1), {}, 1_000)).toHaveLength(1);
    expect(planQuiz(pool.slice(0, 2), {}, 1_000)).toHaveLength(2);
    const first = planQuiz(pool, {}, 1_000);
    expect(first.length).toBe(QUIZ_SIZE);
    expect(planQuiz(pool, {}, 1_000).map(card => card.id)).toEqual(first.map(card => card.id));
  });
});

describe('which deck', () => {
  test('maps the session subject to Mark Bank’s deck at the student’s level', () => {
    expect(resolveQuizDeck('Mathematics', undefined, [{ subjectName: 'Mathematics', level: 'ordinary' }])).toMatchObject({ subjectId: 'maths', level: 'ordinary', deckId: 'maths-ordinary' });
    expect(resolveQuizDeck('Mathematics', 'mathematics', [{ subjectName: 'Mathematics', level: 'foundation' }])?.level).toBe('ordinary');
    expect(resolveQuizDeck('Chemistry', undefined, [])?.level).toBe('higher');
    expect(resolveQuizDeck('LCVP Link Modules', undefined, [{ subjectName: 'LCVP Link Modules', level: 'common' }])).toMatchObject({ subjectId: 'lcvp', level: 'common' });
    expect(resolveQuizDeck('Ag Science', undefined, [])?.subjectId).toBe('agricultural-science');
  });

  test('a subject with no deck gets no quiz', () => {
    expect(resolveQuizDeck('Hebrew Studies', undefined, [])).toBeNull();
    expect(resolveQuizDeck('Not a subject', undefined, [])).toBeNull();
  });
});

describe('the topic label', () => {
  test('names the studied topics from the registry, or says nothing when it cannot', () => {
    const real = CURRICULUM_SPECIFICATIONS.find(item => item.groups.length > 0 && item.groups[0].topics.length > 1)!;
    const [first, second] = real.groups[0].topics;
    expect(quizTopicLabel({ subjectId: real.subjectId, specificationId: real.id, topicIds: [first.id] })).toBe(first.title);
    expect(quizTopicLabel({ subjectId: real.subjectId, specificationId: real.id, topicIds: [first.id, second.id] })).toBe(`${first.title} and ${second.title}`);
    expect(quizTopicLabel({ subjectId: real.subjectId, specificationId: real.id, topicIds: [real.groups[0].id] })).toBe(real.groups[0].title);
    expect(quizTopicLabel({ subjectId: real.subjectId, specificationId: 'no-such-spec', topicIds: [first.id] })).toBeNull();
    expect(quizTopicLabel(undefined)).toBeNull();
  });
});


describe('saved session topics', () => {
  const politics = CURRICULUM_SPECIFICATIONS.find(spec => spec.id === 'politics-and-society:current')!;
  const selection = { subjectId: politics.subjectId, specificationId: politics.id, topicIds: ['politics-and-society-0-0'] };
  test('the real school topic returns native rubric cards only from that topic', async () => {
    const loaded = await loadQuiz({ uid: 'demo-student', subjectName: 'Politics and Society', topicSelection: selection, now: 1_000 });
    expect(loaded?.cards.length).toBeGreaterThan(0);
    const deck = await loadCards('politics-and-society', 'higher');
    const matching = new Set(cardsForCurriculumNode(selection.topicIds[0], deck, politics).map(card => card.id));
    expect(loaded?.cards.every(card => matching.has(card.id))).toBe(true);
    expect(loaded?.cards.some(card => card.kind === 'rubric')).toBe(true);
    expect(isQuizCard(deck.find(card => card.id === 'politics-2019-hl-q1-d')!)).toBe(true);
    expect(isQuizCard(deck.find(card => card.id === 'politics-2025-hl-q1-a')!)).toBe(true);
  });
  test('unmatched, missing and mismatched selections never widen to the whole subject', async () => {
    const input = { uid: 'demo-student', subjectName: 'Politics and Society', now: 1_000 };
    expect(await loadQuiz(input)).toBeNull();
    expect(await loadQuiz({ ...input, topicSelection: { ...selection, topicIds: ['unknown-topic'] } })).toBeNull();
    expect(await loadQuiz({ ...input, subjectName: 'Chemistry', topicSelection: selection })).toBeNull();
  });
  test('each selected topic gets a question before a busy topic fills the queue', () => {
    const busy = Array.from({ length: 8 }, (_, i) => point(`busy${i}`, 'chem-2-2'));
    const rare = [point('rare', 'chem-3-1')];
    const picked = planQuiz([...busy, ...rare], {}, 1_000, undefined, 4, [busy, rare]);
    expect(picked).toHaveLength(4);
    expect(picked.slice(0, 2).map(card => card.topicId)).toEqual(['chem-2-2', 'chem-3-1']);
    expect(new Set(picked.map(card => card.id)).size).toBe(4);
    expect(planQuiz([simple], {}, 1_000, undefined, 4, [[simple], [simple]])).toEqual([simple]);
  });
});


test('a full response remains available when the topic has no short question', async () => {
  expect(preferShortQuestions([tooLong])).toEqual([tooLong]);
  expect(preferShortQuestions([tooLong, simple])).toEqual([simple]);
  const english = CURRICULUM_SPECIFICATIONS.find(spec => spec.subjectId === 'english' && spec.status === 'verified')!;
  const deck = await loadCards('english', 'higher');
  const longTopic = english.groups.flatMap(group => group.topics).find(topic => {
    const pool = quizPool(deck, [topic.id], english);
    return pool.length > 0 && pool.every(card => card.totalMarks > 10);
  })!;
  expect(longTopic).toBeDefined();
  const loaded = await loadQuiz({ uid: 'demo-student', subjectName: 'English', now: 1_000,
    topicSelection: { subjectId: english.subjectId, specificationId: english.id, topicIds: [longTopic.id] } });
  expect(loaded?.cards).toHaveLength(1);
  expect(loaded?.cards[0].totalMarks).toBeGreaterThan(10);
  expect(cardsForCurriculumNode(longTopic.id, loaded!.cards, english)).toHaveLength(1);
});
