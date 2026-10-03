import React from 'react';
import { afterEach, beforeEach, expect, test, vi } from 'vitest';
import { cleanup, fireEvent, render, screen } from '@testing-library/react';
import MarkBank from '../components/MarkBank/MarkBank';

vi.mock('../hooks/useMobileAppDesign', () => ({ useMobileAppDesign: () => true }));
beforeEach(() => { localStorage.clear(); Element.prototype.scrollIntoView = vi.fn(); });
afterEach(() => { cleanup(); localStorage.clear(); });

test('the subject index keeps topic practice available without a dismissible overview', async () => {
  render(<MarkBank studentSubjects={[{ subjectName: 'Geography', level: 'higher' }]} />);
  const start = await screen.findByRole('button', { name: /^Start 6 questions$/ }, {timeout: 10000});
  expect(start).toBeEnabled();
  expect(screen.getByRole('navigation', { name: 'Subject units' })).toBeInTheDocument();
  expect(screen.queryByRole('button', { name: 'Dismiss practice overview' })).not.toBeInTheDocument();
  fireEvent.change(screen.getByRole('textbox', { name: 'Search topics' }), { target: { value: 'Rock Cycle' } });
  fireEvent.click(screen.getByRole('button', { name: /The Rock Cycle.*questions/ }));
  fireEvent.click(screen.getByRole('button', { name: /^Start 6 questions$/ }));
  expect(await screen.findByRole('button', { name: 'Expand to full screen' })).toBeInTheDocument();
  expect(screen.getByRole('textbox', { name: 'Your answer' })).toBeInTheDocument();
});
