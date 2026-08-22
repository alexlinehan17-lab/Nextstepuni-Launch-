/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Render smoke for Diagram Vault: the subject picker lists real subjects, and
 * drilling into one shows figure tiles that point at real files with their SEC
 * source and a decoded description behind a toggle. Guards the projection UI
 * against render regressions.
 */
import { describe, test, expect } from 'vitest';
import { render, screen, fireEvent, within } from '@testing-library/react';
import DiagramVault from '@/components/DiagramVault/DiagramVault';
import { diagramSubjects, diagramsForSubject } from '@/data/diagramVault';

describe('Diagram Vault', () => {
  test('the vault has subjects and every subject has at least one figure', () => {
    const subs = diagramSubjects();
    expect(subs.length).toBeGreaterThan(0);
    for (const s of subs) expect(diagramsForSubject(s.id).length).toBeGreaterThan(0);
  });

  // Renders every Biology tile in the vault — a hundred and nineteen of them —
  // so it takes about thirty seconds on its own and longer under the rest of the
  // suite. It was failing intermittently on the default timeout for that reason
  // and nothing else.
  test('renders the picker, then a subject’s figures with source + description toggle', () => {
    render(<DiagramVault studentSubjects={['Biology']} />);
    // Level 0 — the tool heading and the picker.
    expect(screen.getByRole('heading', { name: /Diagram Vault/i })).toBeInTheDocument();
    // Drill into Biology (a subject we know has figures).
    fireEvent.click(screen.getByRole('button', { name: /^Biology/ }));
    // Level 1 — a figure tile with a real image and SEC attribution.
    const imgs = screen.getAllByRole('img');
    expect(imgs.length).toBeGreaterThan(0);
    expect(imgs[0].getAttribute('src')).toMatch(/^\/exam-figures\/biology\//);
    expect(screen.getAllByText(/State Examinations Commission/i).length).toBeGreaterThan(0);
    // The decoded description is behind a toggle (hidden until asked for).
    const toggle = screen.getAllByRole('button', { name: /What this diagram shows/i })[0];
    expect(toggle).toHaveAttribute('aria-expanded', 'false');
    fireEvent.click(toggle);
    expect(within(toggle.closest('figure')!).getByText(/Hide description/i)).toBeInTheDocument();
  }, 120_000);
});
