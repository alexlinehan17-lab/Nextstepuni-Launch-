/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Applied Maths published steps as crops of the scheme page (reviewed.json
 * allocation.region, cut by scripts/markbank/authoring/am_steps.py): what a
 * cut card carries and how the panel shows each step's own lines.
 */
import { render, screen } from '@testing-library/react';
import { describe, expect, it, vi } from 'vitest';
import { REVIEWED_CARDS } from '../components/MarkBank/cards/applied-maths/reviewed';
import AppliedMathematicsRubricPanel from '../components/MarkBank/AppliedMathematicsRubricPanel';
import type { AppliedMathematicsRubric, SecRubricCard } from '../types/markBank';

vi.mock('../components/PaperTrail/vaultDocs', () => ({ vaultPdf: vi.fn(() => new Promise(() => {})) }));

type Card = SecRubricCard & { rubric: AppliedMathematicsRubric };
const byId = (id: string) => {
  const card = REVIEWED_CARDS.find(candidate => candidate.id === id) as Card | undefined;
  if (!card) throw new Error(`no card ${id}`);
  return card;
};

describe('Applied Maths steps', () => {
  it('cuts each published step to the band ending at its margin mark, in order, inside the solution', () => {
    const card = byId('am-2010-hl-1-a-ii');
    const regions = card.rubric.allocations.map(item => item.region!);
    expect(regions.map(region => region.p)).toEqual([4, 4, 4]);
    expect(regions.map(region => region.r)).toEqual([[0.07, 0.375, 0.95, 0.441], [0.07, 0.439, 0.95, 0.512], [0.07, 0.51, 0.95, 0.6269]]);
    const whole = card.rubric.solution.regions![0];
    for (const { r } of regions) expect(r[1] >= whole[1] && r[3] <= whole[3] + 1e-9).toBe(true);
    expect(regions[1].r[1]).toBeGreaterThan(regions[0].r[1]);
  });

  it('shows a crop for each cut step and keeps the credit buttons', () => {
    const card = byId('am-2010-hl-1-a-ii');
    render(<AppliedMathematicsRubricPanel card={card} scores={{}} onScore={() => {}} />);
    for (const item of card.rubric.allocations) {
      expect(screen.getByLabelText(`${item.label}: the lines it prices`)).toBeInTheDocument();
      expect(screen.getByRole('button', { name: `Set ${item.label} to 5 marks` })).toBeInTheDocument();
    }
  });

  it('leaves a card in the residue, and a scale card, with the whole solution only', () => {
    const scale = REVIEWED_CARDS.find(candidate => (candidate as Card).rubric.allocations.every(item => !item.label.startsWith('Published step'))) as Card;
    expect(scale.rubric.allocations.some(item => item.region)).toBe(false);
    render(<AppliedMathematicsRubricPanel card={scale} scores={{}} onScore={() => {}} />);
    expect(screen.queryByLabelText(/the lines it prices/)).not.toBeInTheDocument();
  });
});
