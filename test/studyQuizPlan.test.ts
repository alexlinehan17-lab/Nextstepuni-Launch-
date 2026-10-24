/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The end-of-session quiz asks only short, real Mark Bank questions on what
 * was studied, and scores a tick exactly as Mark Bank does.
 */

import { describe, expect, test } from 'vitest';
import {
  EMPTY_ANSWER,
  QUIZ_MIN,
  QUIZ_SIZE,
  cardMarks,
  isQuizCard,
  marksEarned,
  planQuiz,
  quizGrade,
  quizPool,
  quizTopicLabel,
  resolveQuizDeck,
  rowKey,
  type QuizAnswer,
} from '@/components/study/quiz/studyQuizPlan';
import { claimableTotal, marksClaimed, suggestGrade } from '@/components/MarkBank/SessionScreen';
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
  test('short fixed-tariff point cards qualify; booklets, splits, routes, long and unpriced ones do not', () => {
    expect(all.filter(isQuizCard).map(card => card.id)).toEqual(['q1', 'q2', 'q3', 'q4', 'q5', 'q6']);
  });

  test('topics narrow the pool, a whole area expands to its topics, and cross-listed cards count once', () => {
    expect(quizPool(all, ['chem-2-2'], spec).map(card => card.id)).toEqual(['q1', 'q2', 'q6']);
    expect(quizPool(all, ['chemistry:cs3'], spec).map(card => card.id)).toEqual(['q3', 'q4', 'q5']);
    expect(quizPool(all, ['chem-2-2', 'chemistry:cs2'], spec).map(card => card.id)).toEqual(['q1', 'q2', 'q6']);
    expect(quizPool(all, []).length).toBe(6);
  });

  test('fewer than the minimum means no quiz; otherwise at most a quiz’s worth, in a stable order', () => {
    const pool = quizPool(all, [], undefined);
    expect(planQuiz(pool.slice(0, QUIZ_MIN - 1), {}, 1_000)).toEqual([]);
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

describe('scoring matches Mark Bank', () => {
  const answers: Array<[SecQuestionCard, QuizAnswer]> = [
    [simple, EMPTY_ANSWER],
    [simple, { claims: { 'q1-r1': 'yes' }, picks: {} }],
    [grouped, { claims: { 'q2-r2': 'yes' }, picks: { 'q2-r1': [0] } }],
    [grouped, { claims: {}, picks: { 'q2-r1': [0, 1, 2] } }],
    [stepped, { claims: { 'q3-r1': 3 }, picks: {} }],
    [stepped, { claims: { 'q3-r1': 4 }, picks: {} }],
    [descending, { claims: {}, picks: { 'q4-r1': [2] } }],
    [descending, { claims: {}, picks: { 'q4-r1': [1, 2] } }],
    [dependent, { claims: { 'q5-r1': 'yes', 'q5-r2': 'yes' }, picks: {} }],
  ];

  test.each(answers)('%#: marks and grade agree with SessionScreen', (card, answer) => {
    expect(cardMarks(card)).toBe(claimableTotal(card));
    expect(marksEarned(card, answer)).toBe(marksClaimed(card, answer.claims, answer.picks));
    expect(quizGrade(card, answer)).toBe(suggestGrade(card, answer.claims, answer.picks));
  });

  test('a bounded group caps at its claimMax and pays a descending tariff as printed', () => {
    expect(marksEarned(grouped, { claims: {}, picks: { 'q2-r1': [0, 1, 2, 3] } })).toBe(6);
    expect(marksEarned(descending, { claims: {}, picks: { 'q4-r1': [0] } })).toBe(6);
    expect(marksEarned(descending, { claims: {}, picks: { 'q4-r1': [0, 1] } })).toBe(10);
  });

  test('rows are keyed the way Mark Bank keys them', () => {
    expect(rowKey(simple.rows[0], 0)).toBe('q1-r1');
    expect(rowKey({ id: '' }, 2)).toBe('r2');
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
