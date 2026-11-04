/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * An Irish scheme's priced tariff as rows (cards/irish/tariffs.ts): a
 * literature Eolas criterion whose phrases are priced whole or in steps, the
 * samples under it, and the composite last reading question.
 */
import { describe, expect, test, vi } from 'vitest';
import { fireEvent, render, screen, within } from '@testing-library/react';
import SessionScreen from '@/components/MarkBank/SessionScreen';
import { irishCriterionMarks, irishRowScoreId } from '@/components/MarkBank/irishScoring';
import { parseIrishTariffs } from '@/components/MarkBank/cards/irish/tariffs';
import { isRubricCard, type IrishRubric, type SecCard, type SecRubricCard } from '@/types/markBank';
import { CARDS as IRISH_HIGHER } from '@/components/MarkBank/cards/irish/higher';
import { CARDS as IRISH_ORDINARY } from '@/components/MarkBank/cards/irish/ordinary';

vi.mock('@/components/PaperTrail/vaultDocs', () => ({ vaultPdf: vi.fn(() => new Promise(() => {})) }));

const byId = (id: string) => {
  const card = [...IRISH_HIGHER, ...IRISH_ORDINARY].find(candidate => candidate.id === id);
  if (!card || !isRubricCard(card) || card.rubric.system !== 'irish') throw new Error(`no Irish card ${id}`);
  return card as SecRubricCard & { rubric: IrishRubric };
};

describe('an Irish tariff cut into rows', () => {
  test('a prose option priced in two traits places each on its own steps', () => {
    const card = byId('irish-2021-hl-p2-prose-2b-a');
    const eolas = card.rubric.criteria.find(criterion => criterion.id === 'eolas')!;
    const allocation = eolas.allocation!;
    expect(allocation.parts).toHaveLength(1);
    expect(allocation.parts[0].rows.map(row => [row.text, row.marks, row.steps?.length])).toEqual([['Tréith 1', 13, 14], ['Tréith 2', 12, 13]]);
    const scores = { [irishRowScoreId('eolas', 'p1', 'r1')]: 10, [irishRowScoreId('eolas', 'p1', 'r2')]: 7 };
    expect(irishCriterionMarks(eolas, scores)).toBe(17);
    // A placed step outside the printed ones is worth nothing.
    expect(irishCriterionMarks(eolas, { [irishRowScoreId('eolas', 'p1', 'r1')]: 14 })).toBe(0);
  });

  test('a poetry option with three sub-questions keeps each tariff and its sample points', () => {
    const card = byId('irish-2024-ol-p2-poetry-3b-a');
    // One criterion per printed sub-question, and the title and poet's 2 on its own (the reviewed card).
    const priced = card.rubric.criteria.filter(criterion => criterion.allocation);
    expect(priced.map(criterion => criterion.id)).toEqual(['eolas-i', 'eolas-ii', 'eolas-iii', 'teideal']);
    const parts = priced.flatMap(criterion => criterion.allocation!.parts);
    expect(parts.map(part => part.tariff)).toEqual([9, 7, 7, 2]);
    expect(parts[0].rows[0]).toMatchObject({ text: 'Dhá phríomhsmaoineamh', marks: 9, steps: [0, 5, 9] });
    expect(parts[3].rows.map(row => [row.text, row.marks])).toEqual([['Ainm an dáin', 1], ['Ainm an fhile', 1]]);
  });

  test('rows that are the tariff\'s components can all be claimed, so full marks are reachable', () => {
    // "Tréith 1 a lua = 2 mharc", "sampla … = 4 mharc", twice: 12. An answer list would cap the claims at
    // tariff over best answer (3 here), which left 10 of 12 the most a student could place.
    const card = byId('irish-2021-hl-p2-reading-a-q6');
    const eolas = card.rubric.criteria[0];
    const part = eolas.allocation!.parts.find(candidate => candidate.tariff === 12)!;
    expect(part.rows.map(row => row.marks)).toEqual([2, 4, 2, 4]);
    const all = Object.fromEntries(part.rows.map(row => [irishRowScoreId(eolas.id, part.id, row.id), 1]));
    expect(irishCriterionMarks(eolas, all)).toBe(12);
  });

  test('the last reading question: a grammar ladder over the printed examples and a two-trait composite', () => {
    const card = byId('irish-2021-hl-p2-reading-b-q6');
    const eolas = card.rubric.criteria[0];
    const parts = eolas.allocation!.parts;
    expect(parts[0]).toMatchObject({ tariff: 3, ladder: [2, 3] });
    // The printed examples, one row per "Sampla …:" phrase, priced by the ladder.
    expect(parts[0].rows.length).toBeGreaterThanOrEqual(2);
    expect(parts[0].rows.every(row => /^Sampla/.test(row.text))).toBe(true);
    expect(parts[1].tariff).toBe(12);
    expect(parts[1].rows.reduce((sum, row) => sum + row.marks, 0)).toBe(12);
  });

  test('refuses a tariff whose parts do not reach the criterion', () => {
    const result = parseIrishTariffs({ id: 'x', totalMarks: 25, questionRef: '2021 HL Paper 2 Poetry 3A(a)', questionText: '', guidance: ['(i) Cad é? Eolas = 13 mharc Príomhthéama = 2 mharc Plé = 11 mharc'] });
    expect(result.ok).toBe(false);
  });

  test('renders stepped rows as step buttons and the samples as a list', () => {
    const card = byId('irish-2021-hl-p2-prose-2b-a');
    render(<SessionScreen cards={[card as SecCard]} subjectLabel="Irish" onGrade={vi.fn()} onFinish={vi.fn()} onExit={vi.fn()} />);
    fireEvent.click(screen.getByRole('button', { name: /Reveal the marking scheme/i }));
    const strip = screen.getByRole('group', { name: 'Marks for Tréith 1' });
    fireEvent.click(within(strip).getByRole('button', { name: 'Claim 10 marks for Tréith 1' }));
    expect(within(strip).getByRole('button', { name: 'Clear 10 marks for Tréith 1' })).toHaveAttribute('aria-pressed', 'true');
  });
});
