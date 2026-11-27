import React from 'react';
import { afterEach, beforeEach, expect, test, vi } from 'vitest';
import { cleanup, fireEvent, render, screen, within } from '@testing-library/react';
import MarkBank from '../components/MarkBank/MarkBank';

vi.mock('../hooks/useMobileAppDesign', () => ({ useMobileAppDesign: () => true }));
beforeEach(() => { localStorage.clear(); Element.prototype.scrollIntoView = vi.fn(); });
afterEach(() => { cleanup(); localStorage.clear(); });

test('the mobile library uses the student cohort and one heading list', async () => {
  render(<MarkBank examDate="2027-06-02" studentSubjects={[{ subjectName: 'Latin', level: 'higher' }]} />);
  expect(screen.getByText(/Your syllabus:.*Latin/)).toBeInTheDocument();
  // The subject home lists the strands as rows (Structure A, 24 Nov 2026).
  const index = await screen.findByRole('list', { name: 'All topics' }, { timeout: 10000 });
  expect(await within(index).findByRole('button', { name: /Latin Language/ }, { timeout: 10000 })).toBeInTheDocument();
  // Latin is in the single model: older papers' questions are filed under the one heading list, so the index has no
  // separate 'Original paper topics' units (Alex, 18 Nov: no second old-course list).
  expect(within(index).queryAllByText('Original paper topics')).toHaveLength(0);
});

test('the subject index keeps topic practice available without a dismissible overview', async () => {
  render(<MarkBank studentSubjects={[{ subjectName: 'Geography', level: 'higher' }]} />);
  // Structure A (24 Nov 2026): the subject home, then a topic's own page with Practise; search opens from the bar (or Cmd K).
  const start = await screen.findByRole('button', { name: /^Practise \d+ questions/ }, {timeout: 10000});
  expect(start).toBeEnabled();
  expect(screen.getByRole('list', { name: 'All topics' })).toBeInTheDocument();
  expect(screen.queryByRole('button', { name: 'Dismiss practice overview' })).not.toBeInTheDocument();
  // Geography is in the single model: the index lists the Atlas heading the rock cycle is filed under.
  fireEvent.keyDown(window, { key: 'k', metaKey: true });
  fireEvent.change(await screen.findByRole('searchbox', { name: 'Search topics' }), { target: { value: 'Rocks' } });
  fireEvent.click(await screen.findByRole('button', { name: /Rocks, Weathering & Mass Movement.*questions/ }));
  fireEvent.click(screen.getByRole('button', { name: /^Practise 6 questions$/ }));
  expect(await screen.findByRole('button', { name: 'Expand to full screen' })).toBeInTheDocument();
  expect(screen.getByRole('textbox', { name: 'Your answer' })).toBeInTheDocument();
});
