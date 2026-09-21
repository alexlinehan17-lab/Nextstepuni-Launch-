import React from 'react';
import { afterEach, beforeEach, expect, test, vi } from 'vitest';
import { cleanup, fireEvent, render, screen } from '@testing-library/react';
import MarkBank from '../components/MarkBank/MarkBank';

vi.mock('../hooks/useMobileAppDesign', () => ({ useMobileAppDesign: () => true }));
beforeEach(() => localStorage.clear());
afterEach(() => { cleanup(); localStorage.clear(); });

test('dismissing the overview keeps practice available and remembers the choice on return', async () => {
  const props = { studentSubjects: [{ subjectName: 'Geography', level: 'higher' as const }] };
  const first = render(<MarkBank {...props} />);
  fireEvent.click(await screen.findByRole('button', { name: 'Dismiss practice overview' }));
  expect(screen.queryByRole('heading', { name: 'Make a start today.' })).not.toBeInTheDocument();
  expect(screen.getByRole('button', { name: 'Start a practice session' })).toBeEnabled();
  first.unmount();
  render(<MarkBank {...props} />);
  expect(await screen.findByRole('button', { name: 'Show overview' })).toBeInTheDocument();
  expect(screen.getByRole('button', { name: 'Start a practice session' })).toBeEnabled();
  fireEvent.click(screen.getByRole('button', { name: 'Show overview' }));
  expect(screen.getByRole('button', { name: 'Dismiss practice overview' })).toBeInTheDocument();
});
