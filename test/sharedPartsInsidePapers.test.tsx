/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Shared parts extended for what a student meets inside the papers (area 6c,
 * 27 Nov 2026): a sheet whose head carries controls at its right (the marking
 * scheme's previous and next question), and short choices in a row (self-mark's
 * Blank to Full, and why marks were lost), chosen with the ink outline and the
 * drawn tick like every other choice.
 */
import React, { useState } from 'react';
import { describe, expect, it, vi } from 'vitest';
import { fireEvent, render, screen, within } from '@testing-library/react';
import { Sheet } from '../components/ui/Sheet';
import { ChoiceTile } from '../components/ui/Choice';
import { List, Row } from '../components/ui/List';

describe('Sheet with controls at the right of its head', () => {
  it('keeps Close at the top left and puts the controls at the right, each still working', () => {
    const onClose = vi.fn();
    const onNext = vi.fn();
    render(<Sheet open onClose={onClose} title="Question 1 · marking scheme" titleAlign="start"
      actions={<button type="button" onClick={onNext}>Next question’s marking scheme</button>}>
      <p>The scheme</p>
    </Sheet>);
    const sheet = screen.getByRole('dialog', { name: 'Question 1 · marking scheme' });
    const head = sheet.querySelector('.ui-sheet-head') as HTMLElement;
    const parts = Array.from(head.children);
    expect(parts[0]).toHaveAccessibleName('Close');
    expect(parts[parts.length - 1]).toHaveClass('ui-sheet-actions');
    fireEvent.click(within(head).getByRole('button', { name: 'Next question’s marking scheme' }));
    expect(onNext).toHaveBeenCalledTimes(1);
    fireEvent.click(within(head).getByRole('button', { name: 'Close' }));
    expect(onClose).toHaveBeenCalledTimes(1);
  });

  it('shows a status word when it has no controls, as before', () => {
    render(<Sheet open onClose={() => {}} title="Notes" titleAlign="start" status="Saved"><p>Notes</p></Sheet>);
    expect(screen.getByText('Saved')).toHaveClass('ui-sheet-status');
  });
});

describe('ChoiceTile compact: short choices in a row', () => {
  function Bands() {
    const [score, setScore] = useState<number | null>(null);
    return <div role="group" aria-label="How did you do against the scheme?">
      {[{ v: 0, label: 'Blank' }, { v: 50, label: 'Half' }, { v: 100, label: 'Full' }].map(b =>
        <ChoiceTile key={b.v} compact kind="toggle" chosen={score === b.v} label={b.label} onClick={() => setScore(b.v)} />)}
    </div>;
  }

  it('is a button that stays pressed, named by its words, with the drawn tick only when chosen', () => {
    render(<Bands />);
    const half = screen.getByRole('button', { name: 'Half' });
    expect(half).toHaveClass('ui-choice', 'ui-choice--compact');
    expect(half).toHaveAttribute('aria-pressed', 'false');
    expect(half.querySelector('.ui-mark')).toHaveAttribute('data-mark', 'off');
    fireEvent.click(half);
    expect(half).toHaveAttribute('aria-pressed', 'true');
    expect(half.querySelector('.ui-mark')).toHaveAttribute('data-mark', 'on');
    fireEvent.click(screen.getByRole('button', { name: 'Full' }));
    expect(half).toHaveAttribute('aria-pressed', 'false');
    expect(screen.getByRole('button', { name: 'Full' })).toHaveAttribute('aria-pressed', 'true');
  });
});

describe('Row with a control beside it', () => {
  it('opens from the row and toggles from the control, which is never inside the row', () => {
    const onOpen = vi.fn();
    const onSave = vi.fn();
    render(<List label="Saved papers"><Row title="Accounting · Exam Paper" meta="2025 · Higher level · English" onPress={onOpen}
      end={<button type="button" aria-pressed="true" onClick={onSave}>Remove saved Accounting 2025 Exam Paper</button>} /></List>);
    const row = screen.getByRole('button', { name: /Accounting · Exam Paper/ });
    const mark = screen.getByRole('button', { name: 'Remove saved Accounting 2025 Exam Paper' });
    expect(row.contains(mark)).toBe(false);
    expect(row.closest('li')).toHaveClass('ui-row-item--end');
    fireEvent.click(mark);
    expect(onSave).toHaveBeenCalledTimes(1);
    expect(onOpen).not.toHaveBeenCalled();
    fireEvent.click(row);
    expect(onOpen).toHaveBeenCalledTimes(1);
  });
});
