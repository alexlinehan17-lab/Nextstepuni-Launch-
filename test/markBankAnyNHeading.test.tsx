/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The any-N menu heading on screen says "1 mark each", not "1 marks each".
 */

import { describe, expect, test, vi } from 'vitest';
import { fireEvent, render, screen } from '@testing-library/react';

import SessionScreen from '@/components/MarkBank/SessionScreen';
import type { MarkRow, SecQuestionCard } from '@/types/markBank';

vi.mock('@/components/PaperTrail/vaultDocs', () => ({ vaultPdf: vi.fn(() => new Promise(() => {})) }));

const row = (o: Partial<MarkRow> = {}): MarkRow => ({ id: 'r0', kind: 'point', verbatim: 'Oesophagus', marks: 2, ...o });
const card = (o: Partial<SecQuestionCard> = {}): SecQuestionCard => ({
  source: 'sec', kind: 'question',
  id: 'chem-2021-hl-q5-b-ii', subjectId: 'chemistry', level: 'higher',
  topicId: 'chemistry-1', conceptId: 'radius',
  year: 2021, paperFileid: 'LC022ALP000EV', section: 'A',
  questionRef: '2021 HL Q5(b)(ii)',
  questionText: 'How is atomic (covalent) radius defined?',
  tariffModel: { kind: 'fixed' }, totalMarks: 6,
  rows: [
    row({ id: 'a1', verbatim: 'half the internuclear distance of two atoms of same element', marks: 3, route: 'a' }),
    row({ id: 'a2', verbatim: 'joined by a single covalent bond', marks: 3, route: 'a' }),
    row({ id: 'b1', verbatim: 'half the internuclear distance between two atoms', marks: 3, route: 'b' }),
    row({ id: 'b2', verbatim: 'joined by a single homonuclear bond', marks: 3, route: 'b' }),
  ],
  schemeCitation: 'SEC marking scheme, Chemistry 2021 Higher Level',
  specVersion: 'lc-chemistry',
  qa: { gates: [], humanReviewedBy: 'al', humanReviewedAt: '2026-11-04' },
  ...o,
} as SecQuestionCard);

const renderSession = (c: SecQuestionCard) => render(
  <SessionScreen cards={[c]} subjectLabel="Chemistry" onGrade={vi.fn()} onFinish={vi.fn()} onExit={vi.fn()} />,
);
const reveal = () => fireEvent.click(screen.getByRole('button', { name: /Reveal the marking scheme/i }));

describe('the any-N heading on screen', () => {
  test('a one-mark menu says "1 mark each"', () => {
    renderSession(card({
      totalMarks: 2,
      rows: [row({ id: 'g', kind: 'anyN', verbatim: 'Any two', marks: null, group: { claimMax: 2, perOption: 1, options: ['Price', 'Quantity', 'QE'] } })],
    }));
    reveal();
    expect(screen.getByText('Any 2 of these — 1 mark each')).toBeInTheDocument();
    expect(screen.queryByText(/1 marks/)).not.toBeInTheDocument();
  });
});

