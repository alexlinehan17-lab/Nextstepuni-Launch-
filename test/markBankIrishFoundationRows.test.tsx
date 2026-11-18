/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Foundation official answers are claimable rows (cards/irish/foundationAnswers.ts): the row model and chip of the
 * Higher and Ordinary listening and reading cards, each row the scheme's printed answer at its printed mark.
 */
import { fireEvent, render, screen } from '@testing-library/react';
import { describe, expect, it, vi } from 'vitest';
import { CARDS } from '../components/MarkBank/cards/irish/foundation';
import { FOUNDATION_UNCUT } from '../components/MarkBank/cards/irish/foundationAnswers';
import SessionScreen, { irishMarks } from '../components/MarkBank/SessionScreen';
import { irishRowScoreId } from '../components/MarkBank/irishScoring';
import type { IrishCriterion, SecRubricCard } from '../types/markBank';

const criteriaOf = (card: SecRubricCard): IrishCriterion[] => (card.rubric.system === 'irish' ? card.rubric.criteria : []);
const card = (id: string) => CARDS.find(candidate => candidate.id === id)!;
const rowsOf = (id: string) => criteriaOf(card(id))[0].allocation!.parts[0].rows.map(row => [row.text, row.marks]);
const normalise = (value: string) => value.toLowerCase().replace(/[^a-z0-9áéíóú’'-]+/g, '');

describe('Foundation official answers', () => {
  const answers = CARDS.flatMap(c => criteriaOf(c).filter(x => x.guidanceKind !== 'quality').map(criterion => ({ card: c, criterion })));

  it('every answer criterion is the official-answer row model; none is left as directions', () => {
    expect(FOUNDATION_UNCUT).toEqual([]);
    expect(answers).toHaveLength(934);
    for (const { card: c, criterion } of answers) {
      expect(criterion.guidanceKind, c.id).toBe('exact');
      expect(criterion.allocation, c.id).toBeDefined();
    }
    expect(CARDS.flatMap(criteriaOf).filter(x => x.guidanceKind === 'quality')).toHaveLength(304);
  });

  it('each row is the scheme’s printed answer at its printed mark, one of which earns the part', () => {
    for (const { card: c, criterion } of answers) {
      const corpus = normalise(criterion.guidance.join(' ') + ' ' + c.questionText);
      const { parts, directions } = criterion.allocation!;
      expect(parts, c.id).toHaveLength(1);
      const [part] = parts;
      expect(part.tariff, c.id).toBe(criterion.maxMarks);
      expect(part.rows.length, c.id).toBeGreaterThan(0);
      for (const row of part.rows) {
        expect(corpus.includes(normalise(row.text)), `${c.id}: "${row.text}"`).toBe(true);
        expect(row.marks, c.id).toBeGreaterThan(0);
        expect(row.marks, c.id).toBeLessThanOrEqual(part.tariff);
      }
      expect(part.rows.some(row => row.marks === part.tariff), c.id).toBe(true);
      // An answer list: its rows are alternatives, so they never add up to the part (which would make them components).
      if (part.rows.length > 1) expect(part.rows.reduce((sum, row) => sum + row.marks, 0), c.id).not.toBe(part.tariff);
      for (const direction of directions) expect(corpus.includes(normalise(direction)), `${c.id}: "${direction}"`).toBe(true);
    }
  });

  it('pins the answers read against the scheme pages', () => {
    expect(rowsOf('irish-2018-fl-r-2a-1')).toEqual([['15 Aibreán', 5]]);
    expect(rowsOf('irish-2010-fl-a-1a')).toEqual([['Fáilteoir = an tríú pictiúr', 7]]);
    expect(rowsOf('irish-2022-fl-a-1b')).toEqual([['Páirt i scannáin mhóra', 7], ['Páirt i Ros na Rún', 5]]);
    expect(rowsOf('irish-2010-fl-r-3a-3')).toContainEqual(['Ceol draíochta', 4]);
    expect(criteriaOf(card('irish-2010-fl-r-3a-3'))[0].allocation!.directions).toEqual(['Bosca ceoil = 0', 'Ceol = 0']);
    expect(rowsOf('irish-2015-fl-r-3a-5').slice(-2)).toEqual([['Pictiúrlann', 1], ['Bialann', 1]]);
    expect(criteriaOf(card('irish-2015-fl-r-3a-5'))[0].allocation!.directions).toEqual(['Téann sí lena cairde = 0']);
    expect(rowsOf('irish-2021-fl-r-3c-5')).toEqual([['An aois', 6],
      ['Líne 2 agus Líne 3 as an véarsa deireanach', 4], ['Líne 3 agus Líne 4 as an véarsa deireanach', 4]]);
    expect(rowsOf('irish-2014-fl-r-1-1')).toEqual([['D', 4]]);
    expect(criteriaOf(card('irish-2014-fl-r-1-1'))[0].allocation!.directions[0]).toMatch(/^Glactar le córas eile/);
  });

  it('scores the best claimed answer, never the sum of alternatives', () => {
    const c = card('irish-2022-fl-a-1b');
    const claim = (...rows: string[]) => Object.fromEntries(rows.map(row => [irishRowScoreId('answer', 'p1', row), 1]));
    expect(irishMarks(c, claim('r2'))).toBe(5);
    expect(irishMarks(c, claim('r1', 'r2'))).toBe(7);
  });

  it('shows the official answer as a claimable row under the official-answer chip', () => {
    render(<SessionScreen cards={[card('irish-2018-fl-r-2a-1')]} subjectLabel="Irish" onGrade={vi.fn()} onFinish={vi.fn()} onExit={vi.fn()} />);
    fireEvent.click(screen.getByRole('button', { name: /Reveal the marking scheme/i }));
    expect(screen.getByText('Official answers and tariff')).toBeInTheDocument();
    expect(screen.queryByText('Possible directions — not a checklist')).not.toBeInTheDocument();
    expect(screen.getByRole('button', { name: '15 Aibreán · 5m' })).toBeInTheDocument();
  });
});
