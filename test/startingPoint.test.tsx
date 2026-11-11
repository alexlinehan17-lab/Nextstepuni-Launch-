import { beforeEach, describe, expect, test, vi } from 'vitest';
import { fireEvent, render, screen, waitFor, within } from '@testing-library/react';
import { resolveCurriculumSpecification } from '../curriculumRegistry';
import type { SecCard, SecQuestionCard } from '../types/markBank';
import type * as Deck from '../components/MarkBank/deck';
import { planStartingPoint, startingPointResults, startingPointTopics } from '../components/MarkBank/startingPoint';
import StartingPointCheck from '../components/MarkBank/StartingPointCheck';
import MarkBank from '../components/MarkBank/MarkBank';
import { readLocal } from '../components/MarkBank/store';

const mocks = vi.hoisted(() => ({ loadCards: vi.fn<() => Promise<SecCard[]>>() }));
vi.mock('../components/MarkBank/deck', async importOriginal => ({
  ...(await importOriginal<typeof Deck>()), loadCards: mocks.loadCards,
}));
vi.mock('../components/PaperTrail/vaultDocs', () => ({ vaultPdf: vi.fn(() => new Promise(() => {})) }));

const spec = resolveCurriculumSpecification('chemistry', 2026)!;
const canonical = spec.groups.flatMap(group => group.topics).slice(0, 5);
const now = () => new Date('2026-11-10T12:00:00Z').getTime();
const question = (index: number, extra: Partial<SecQuestionCard> = {}): SecQuestionCard => ({
  id: `chemistry-2025-ol-check-${index}`, kind: 'question', source: 'sec', subjectId: 'chemistry', level: 'ordinary',
  year: 2025, topicId: canonical[index].id, conceptId: `concept-${index}`, paperFileid: 'LC022GLP000EV',
  section: 'A', questionRef: `2025 OL Q${index + 1}`, questionText: `Sample question ${index + 1}?`,
  totalMarks: 6, tariffModel: { kind: 'fixed' }, rows: [{ id: 'answer', kind: 'point', verbatim: 'A marking point', marks: 6 }],
  specVersion: spec.id, specificationId: spec.id, schemeCitation: 'SEC marking scheme',
  qa: { gates: ['verbatim', 'tariff'], humanReviewedBy: 'test', humanReviewedAt: '2026-11-10' }, ...extra,
});
const cards = canonical.map((_, index) => question(index));
const topics = () => startingPointTopics(spec, 'ordinary', cards);
const select = (index: number) => fireEvent.click(screen.getByRole('checkbox', { name: new RegExp(canonical[index].title.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')) }));
const begin = () => fireEvent.click(screen.getByRole('button', { name: /^Start check/ }));
const reveal = () => fireEvent.click(screen.getByRole('button', { name: 'Reveal the marking scheme' }));
const attempt = () => fireEvent.change(screen.getByRole('textbox', { name: 'Your answer' }), { target: { value: 'My attempt' } });
const renderCheck = (overrides: Partial<React.ComponentProps<typeof StartingPointCheck>> = {}) => {
  const onGrade = vi.fn(); const onPractice = vi.fn(); const onClose = vi.fn();
  const view = render(<StartingPointCheck subjectLabel="Chemistry" level="ordinary" spec={spec} cards={cards}
    memories={{}} now={now} onGrade={onGrade} onPractice={onPractice} onClose={onClose} {...overrides} />);
  return { ...view, onGrade, onPractice, onClose };
};
beforeEach(() => { localStorage.clear(); mocks.loadCards.mockResolvedValue(cards); });

describe('a bounded sample with defensible topic attribution', () => {
  test('uses the registry and correct paper level; preserves unavailable topics', () => {
    const available = startingPointTopics(spec, 'ordinary', [cards[0], question(1, { level: 'higher' }), question(2, { subjectId: 'biology' })]);
    expect(available.map(topic => topic.id)).toEqual(spec.groups.flatMap(group => group.topics.filter(topic => !topic.levels || topic.levels.includes('ordinary')).map(topic => topic.id)));
    expect(available.filter(topic => topic.cards.length).map(topic => topic.id)).toEqual([canonical[0].id]);
    expect(startingPointTopics({ ...spec, status: 'provisional' }, 'ordinary', cards)).toEqual([]);
  });

  test('does not diagnose mixed, unmapped, unreviewed or unscoreable questions', () => {
    const pool = [question(0, { additionalTopicIds: [canonical[1].id] }), question(1, { topicId: 'unknown-archive-topic' }),
      question(2, { qa: { gates: [], humanReviewedBy: '', humanReviewedAt: '' } }), question(3, { totalMarks: 0 })];
    expect(startingPointTopics(spec, 'ordinary', pool).every(topic => !topic.cards.length)).toBe(true);
  });

  test('one question per selected taught topic, no automatic expansion', () => {
    const plan = planStartingPoint(topics(), [canonical[2].id, canonical[0].id], {}, now());
    expect(plan.map(item => item.topicId)).toEqual([canonical[2].id, canonical[0].id]);
    expect(plan.map(item => item.card.id)).toEqual([cards[2].id, cards[0].id]);
    expect(planStartingPoint(topics(), [], {}, now())).toEqual([]);
  });

  test('caps at three distinct short questions and never repeats a card', () => {
    const plan = planStartingPoint(topics(), [canonical[0].id, ...canonical.map(topic => topic.id)], {}, now());
    expect(plan).toHaveLength(3);
    expect(new Set(plan.map(item => item.card.id)).size).toBe(3);
  });

  test('prefers a short task and limits an extended task to a sitting of its own', () => {
    const long = question(0, { id: 'long-question', totalMarks: 80 });
    expect(startingPointTopics(spec, 'ordinary', [long, cards[0]])[0].cards).toEqual([cards[0]]);
    const longTopics = startingPointTopics(spec, 'ordinary', [long, cards[1]]);
    expect(planStartingPoint(longTopics, [canonical[0].id, canonical[1].id], {}, now()).map(item => item.card.id)).toEqual(['long-question']);
    expect(planStartingPoint(longTopics, [canonical[1].id, canonical[0].id], {}, now()).map(item => item.card.id)).toEqual([cards[1].id]);
  });

  test('reports gaps from marks, successful samples as rechecks, and skips as unknown', () => {
    const plan = planStartingPoint(topics(), canonical.slice(0, 3).map(topic => topic.id), {}, now());
    const result = startingPointResults(plan, [
      { cardId: cards[0].id, marksAvailable: 6, marksClaimed: 3, grade: 'got' },
      { cardId: cards[1].id, marksAvailable: 6, marksClaimed: 6, grade: 'got' },
    ]);
    expect(result.map(item => item.status)).toEqual(['practice', 'recheck', 'unknown']);
  });

  test('treats a low-mark task with many marking rows as an extended task', () => {
    const manyRows = question(0, { totalMarks: 7, rows: Array.from({ length: 7 }, (_, index) => ({ id: `row-${index}`, kind: 'point', verbatim: 'A marking point', marks: 1 })) });
    const available = startingPointTopics(spec, 'ordinary', [manyRows, cards[1]]);
    expect(planStartingPoint(available, [canonical[0].id, canonical[1].id], {}, now()).map(item => item.card.id)).toEqual([manyRows.id]);
    expect(planStartingPoint(available, [canonical[1].id, canonical[0].id], {}, now()).map(item => item.card.id)).toEqual([cards[1].id]);
  });

  test.each([NaN, -1, 7])('rejects invalid awarded marks: %s', marksClaimed => {
    const plan = planStartingPoint(topics(), [canonical[0].id], {}, now());
    expect(startingPointResults(plan, [{ cardId: cards[0].id, marksAvailable: 6, marksClaimed, grade: 'got' }])[0].status).toBe('unknown');
  });

  test('rejects a wrong card or denominator rather than deriving a recommendation', () => {
    const plan = planStartingPoint(topics(), [canonical[0].id], {}, now());
    for (const result of [{ cardId: cards[1].id, marksAvailable: 6 }, { cardId: cards[0].id, marksAvailable: 10 }]) {
      expect(startingPointResults(plan, [{ ...result, marksClaimed: 1, grade: 'shaky' }])[0].status).toBe('unknown');
    }
  });
});

describe('starting-point flow in the existing question interface', () => {
  test('requires a taught-topic choice, previews questions and enforces the selection cap', () => {
    renderCheck();
    expect(screen.getByRole('button', { name: /^Start check/ })).toBeDisabled();
    select(0); select(1); select(2);
    expect(screen.getByRole('checkbox', { name: new RegExp(canonical[3].title) })).toHaveAttribute('aria-disabled', 'true');
    select(3);
    expect(screen.getByRole('button', { name: 'Start check · 3 questions' })).toBeEnabled();
    select(0);
    expect(screen.getByRole('checkbox', { name: new RegExp(canonical[3].title) })).not.toHaveAttribute('aria-disabled', 'true');
  });

  test('keeps answers hidden until an attempt; saves marks once and opens the specific recommended question', () => {
    const { onGrade, onPractice } = renderCheck();
    select(0); begin();
    expect(screen.getByRole('button', { name: 'Try the question first' })).toBeDisabled();
    expect(screen.queryByText('A marking point')).not.toBeInTheDocument();
    attempt(); reveal();
    fireEvent.click(screen.getByRole('button', { name: 'See review summary' }));
    expect(onGrade).toHaveBeenCalledExactlyOnceWith({ cardId: cards[0].id, marksClaimed: 0, marksAvailable: 6, grade: 'missed' });
    expect(screen.getByRole('heading', { name: `Start with ${canonical[0].title}.` })).toBeInTheDocument();
    fireEvent.click(screen.getByRole('button', { name: `Practise ${canonical[0].title}` }));
    expect(onPractice).toHaveBeenCalledWith(canonical[0].id, cards[0]);
    expect(onGrade).toHaveBeenCalledTimes(1);
  });

  test('accepts an offline attempt, resets the attempt gate per question, and leaves skipped work unknown', () => {
    const { onGrade } = renderCheck();
    select(0); select(1); begin();
    fireEvent.click(screen.getByRole('checkbox', { name: /I tried this on paper/ })); reveal();
    fireEvent.click(screen.getByRole('button', { name: /A marking point/ }));
    fireEvent.click(screen.getByRole('button', { name: 'Next question' }));
    expect(screen.getByRole('button', { name: 'Try the question first' })).toBeDisabled();
    fireEvent.click(screen.getByRole('button', { name: 'Skip question' }));
    expect(onGrade).toHaveBeenCalledTimes(1);
    expect(screen.getByText(/Full marks self-assessed on this question/)).toBeInTheDocument();
    expect(screen.getByText(/Not checked — skipped or unfinished/)).toBeInTheDocument();
    expect(screen.queryByRole('button', { name: /^Practise / })).not.toBeInTheDocument();
  });

  test('closing mid-check keeps marked work and never treats unfinished questions as wrong', () => {
    const { onGrade } = renderCheck();
    select(0); select(1); begin(); attempt(); reveal();
    fireEvent.click(screen.getByRole('button', { name: 'Next question' }));
    fireEvent.click(screen.getByRole('button', { name: 'Close practice' }));
    expect(onGrade).toHaveBeenCalledTimes(1);
    expect(screen.getByText(/Not checked — skipped or unfinished/)).toBeInTheDocument();
    expect(screen.getAllByRole('button', { name: /^Practise / })).toHaveLength(1);
  });

  test('skipping everything records no marks', () => {
    const { onGrade } = renderCheck(); select(0); begin();
    fireEvent.click(screen.getByRole('button', { name: 'Skip question' }));
    expect(screen.getByRole('heading', { name: 'No answers marked yet.' })).toBeInTheDocument();
    expect(onGrade).not.toHaveBeenCalled();
  });

  test('missing questions remain visible with an honest unavailable state', () => {
    renderCheck({ cards: [] });
    expect(screen.getByText(/There are no suitable questions/)).toBeInTheDocument();
    expect(screen.getAllByRole('checkbox').every(item => (item as HTMLInputElement).disabled || item.getAttribute('aria-disabled') === 'true' || item.hasAttribute('disabled'))).toBe(true);
    expect(screen.getByRole('button', { name: /^Start check/ })).toBeDisabled();
  });

  test('launches from Mark Bank and persists only marked questions through unmount and reload', async () => {
    const props = { examDate: '2026-06-03', studentSubjects: [{ subjectName: 'Chemistry', level: 'Ordinary' }], now };
    const view = render(<MarkBank {...props} />);
    await waitFor(() => expect(screen.getByRole('button', { name: 'Where should I start?' })).toBeEnabled());
    fireEvent.click(screen.getByRole('button', { name: 'Where should I start?' }));
    select(0); select(1); begin(); attempt(); reveal();
    fireEvent.click(screen.getByRole('button', { name: 'Next question' }));
    fireEvent.click(screen.getByRole('button', { name: 'Skip question' }));
    expect(Object.keys(readLocal(undefined, 'chemistry-ordinary').cards)).toEqual([cards[0].id]);
    expect(readLocal(undefined, 'chemistry-ordinary').cards[cards[0].id].reps).toBe(1);
    view.unmount();
    render(<MarkBank {...props} />);
    await waitFor(() => expect(screen.getByRole('button', { name: 'Where should I start?' })).toBeEnabled());
    expect(readLocal(undefined, 'chemistry-ordinary').cards[cards[0].id].reps).toBe(1);
    expect(within(screen.getByRole('navigation', { name: 'Subject units' })).getAllByRole('button').length).toBeGreaterThan(0);
  });
});
