/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Smoke tests for the Paper Trail study-loop surfaces built on the topic tags:
 * the mock-set builder (subject → configure → build → checklist) and the
 * progress dashboard (honest empty state → populated after self-marks). Both
 * take plain props and read the real localStorage stores (no Firebase), so they
 * render standalone in jsdom against the committed tag data.
 */
import { describe, test, expect, beforeEach, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import MockExamBuilder from '@/components/PaperTrail/MockExamBuilder';
import ProgressDashboard from '@/components/PaperTrail/ProgressDashboard';
import { setMark } from '@/components/PaperTrail/attemptStore';
import { loadDeck } from '@/components/PaperTrail/reviewStore';
import { taggedSubjects } from '@/components/PaperTrail/topics';

const NOW = 1_700_000_000_000;
const noop = vi.fn();
const label = (id: string) => id.charAt(0).toUpperCase() + id.slice(1);
const aTaggedSubject = () => taggedSubjects()[0];

describe('Paper Trail — mock-set builder', () => {
  beforeEach(() => localStorage.clear());

  test('builds a set from a subject and shows the run checklist', () => {
    const sid = aTaggedSubject();
    render(
      <MockExamBuilder
        uid="u1"
        now={NOW}
        subjects={[{ id: sid, label: label(sid) }]}
        mineIds={[]}
        subjectLabel={label}
        onOpenQuestion={noop}
        onBack={noop}
      />,
    );
    // Pick the subject tile → configure screen.
    fireEvent.click(screen.getByRole('button', { name: new RegExp(`^${label(sid)}`) }));
    expect(screen.getByText(/Coverage/i)).toBeInTheDocument();
    // Build with the default (mixed) coverage.
    fireEvent.click(screen.getByRole('button', { name: /^Build set$/ }));
    // Run checklist: an export affordance and at least one numbered question.
    expect(screen.getByRole('button', { name: /Export set/i })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /New set/i })).toBeInTheDocument();

    // Bridge to spaced review: "Add all to review" seeds the deck.
    expect(loadDeck('u1')).toHaveLength(0);
    fireEvent.click(screen.getByRole('button', { name: /Add all to review/i }));
    expect(loadDeck('u1').length).toBeGreaterThan(0);
    expect(screen.getByRole('button', { name: /Added to review/i })).toBeInTheDocument();
  });
});

describe('Paper Trail — progress dashboard', () => {
  beforeEach(() => localStorage.clear());

  test('reads empty honestly, then populates after a self-mark', () => {
    const { rerender } = render(
      <ProgressDashboard uid="u1" now={NOW} subjectLabel={label} onDrill={noop} onBack={noop} />,
    );
    expect(screen.getByText(/Nothing to show yet/i)).toBeInTheDocument();

    setMark('u1|business|2022|higher|ev|f1', '1', { score: 8, max: 20, gap: 'careless', ts: NOW });
    rerender(<ProgressDashboard uid="u1" now={NOW + 1} subjectLabel={label} onDrill={noop} onBack={noop} />);

    expect(screen.queryByText(/Nothing to show yet/i)).not.toBeInTheDocument();
    expect(screen.getByText(/Accuracy by subject/i)).toBeInTheDocument();
    // The careless gap shows under the error autopsy (bar label + nudge).
    expect(screen.getByText(/why your marks die/i)).toBeInTheDocument();
    expect(screen.getAllByText(/Careless slips/i).length).toBeGreaterThan(0);
  });
});
