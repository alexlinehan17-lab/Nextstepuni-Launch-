import { cleanup, render, screen } from '@testing-library/react';
import { afterEach, describe, expect, it, vi } from 'vitest';
import LanguageRubricPanel from '../components/MarkBank/LanguageRubricPanel';
import { REVIEWED_CARDS } from '../components/MarkBank/cards/russian/reviewed';
import { languageMarks, languageScoreId, languageGroupId, languageRowId } from '../components/MarkBank/languageScoring';
import { isRubricCard, tariffReconciles, UNPRINTED_ANSWER } from '../types/markBank';

const written = REVIEWED_CARDS.filter(c => c.year === 2017 && c.level === 'ordinary' && !c.audioMaterial);
const get = (suffix: string) => {
  const card = written.find(c => c.id === `ru-2017-ol-${suffix}`);
  if (!card || !isRubricCard(card)) throw new Error(suffix);
  return card;
};
const points = (suffix: string) => {
  const card = get(suffix);
  if (card.rubric.system !== 'language-points') throw new Error(suffix);
  return { ...card, rubric: card.rubric };
};
const selected = (group: string, row = 'full', value = 2) => ({
  [languageGroupId(group)]: 1, [languageRowId(group, row)]: value,
});
afterEach(cleanup);

describe('Russian 2017 Ordinary written asks', () => {
  it('covers all 33 written asks and the original 220 marks', () => {
    expect(written).toHaveLength(33);
    expect(written.reduce((sum, c) => sum + c.totalMarks, 0)).toBe(220);
    expect(written.filter(c => !tariffReconciles(c)).map(c => c.id)).toEqual([]);
    expect(written.every(c => c.sourceMaterial?.pages.length)).toBe(true);
  });

  it('accepts the full hot-and-cold answer as an alternative to two details', () => {
    const c = points('ir1-ii');
    const one = selected('two-details', 'detail-1');
    expect(languageMarks(c, one)).toBe(2);
    expect(languageMarks(c, { ...one, ...selected('two-details', 'detail-2') })).toBe(4);
    expect(languageMarks(c, selected('complete-answer', 'hot-and-cold', 1))).toBe(4);
    // Conflicting saved routes are rejected; the UI requires one route.
    expect(languageMarks(c, { ...one, ...selected('complete-answer', 'hot-and-cold', 1) })).toBe(0);
  });

  it('prevents a full weather feature and its named partial earning twice', () => {
    const c = points('ir1-vii');
    for (const g of c.rubric.groups.filter(g => g.rows.some(r => r.id === 'named-partial'))) {
      expect(languageMarks(c, selected(g.id, 'named-partial', 1))).toBe(1);
      expect(languageMarks(c, { ...selected(g.id), ...selected(g.id, 'named-partial', 1) })).toBe(2);
    }
    expect(languageMarks(c, { ...selected('answer-1'), ...selected('answer-2'), ...selected('answer-3') })).toBe(4);
  });

  it('keeps the complete date pair under one two-mark assessment', () => {
    const c = points('ir2-vi');
    expect(c.rubric.groups).toHaveLength(1);
    expect(languageMarks(c, selected('answer-1', 'full', 1))).toBe(1);
    expect(languageMarks(c, selected('answer-1'))).toBe(2);
  });

  it('requires two different competition categories and caps all submission details', () => {
    const categories = points('ir2-iii');
    expect(categories.rubric.groups).toHaveLength(5);
    expect(languageMarks(categories, selected('answer-1'))).toBe(2);
    expect(languageMarks(categories, { ...selected('answer-1'), ...selected('answer-2') })).toBe(4);
    const formats = points('ir2-v');
    expect(formats.rubric.groups).toHaveLength(8);
    expect(languageMarks(formats, Object.assign({}, ...formats.rubric.groups.map(g => selected(g.id))))).toBe(4);
  });

  it('retains the one-mark propaganda answer without adding it to a specific answer', () => {
    const c = points('ir2-iv');
    const partial = selected('partial-propaganda', 'propaganda', 1);
    const specific = selected('specific-propaganda', 'specific-1');
    expect(languageMarks(c, partial)).toBe(1);
    expect(languageMarks(c, { ...partial, ...specific })).toBe(0);
    expect(languageMarks(c, { ...partial, ...selected('answer-1') })).toBe(3);
    expect(languageMarks(c, { ...specific, ...selected('specific-propaganda', 'specific-2'), ...selected('answer-1') })).toBe(4);
  });

  it('keeps the dog-detail quota and the electronics partial', () => {
    const dog = points('cd-2');
    expect(dog.rubric.groups).toHaveLength(11);
    expect(languageMarks(dog, Object.assign({}, ...dog.rubric.groups.map(g => selected(g.id))))).toBe(10);
    const c = points('cd-3-i');
    const partial = c.rubric.groups.find(g => g.rows[0].text === 'electronics');
    expect(partial).toBeDefined();
    expect(languageMarks(c, selected(partial!.id, 'full', 1))).toBe(1);
    expect(languageMarks(c, { ...selected(partial!.id, 'full', 1), ...selected('answer-1') })).toBe(2);
  });

  it.each([['la2', 6], ['mm-1', 40], ['sd', 20]] as const)('scores every original %s answer', (suffix, total) => {
    const c = points(suffix);
    expect(languageMarks(c, Object.assign({}, ...c.rubric.groups.map(g => selected(g.id, 'full', 1))))).toBe(total);
  });

  it('uses the global rounded cursive mark and preserves both writing choices', () => {
    expect(languageMarks(get('la1'), { [languageScoreId('cursive')]: 5 })).toBe(5);
    const sa = get('sa');
    expect(languageMarks(sa, { [languageScoreId('first-content')]: 12, [languageScoreId('first-coherence')]: 3 })).toBe(15);
    expect(languageMarks(sa, { [languageScoreId('first-content')]: 12, [languageScoreId('first-coherence')]: 3,
      [languageScoreId('second-content')]: 12, [languageScoreId('second-coherence')]: 3 })).toBe(30);
    expect(languageMarks(get('ew'), { [languageScoreId('content')]: 12, [languageScoreId('expression')]: 12,
      [languageScoreId('coherence')]: 6 })).toBe(30);
  });

  it.each(['la1', 'sa', 'ew'])('shows the fixed no-answer line and scoring for %s', suffix => {
    const card = get(suffix);
    expect(card.rubric.system).toBe('language-writing');
    render(<LanguageRubricPanel card={card} scores={{}} onScore={vi.fn()} />);
    expect(screen.getAllByText(new RegExp(UNPRINTED_ANSWER.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'))).length).toBeGreaterThan(0);
  });
});
