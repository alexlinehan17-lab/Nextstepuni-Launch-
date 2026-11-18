import React from 'react';
import { cleanup, fireEvent, render, screen } from '@testing-library/react';
import { afterEach, beforeEach, expect, test, vi } from 'vitest';
const mock = vi.hoisted(() => ({
  status: { available: true, authorized: true, enabled: false, active: false, selectionCount: 0, busy: false, error: null as string | null },
  configure: vi.fn(), enabled: vi.fn(),
}));
vi.mock('@/hooks/useStudyFocus', () => ({ useStudyFocus: () => mock.status }));
vi.mock('@/services/studyFocus', () => ({ configureStudyFocus: mock.configure, setStudyFocusEnabled: mock.enabled }));
import StudyFocusChoice, { StudyFocusStatus } from '@/components/study/StudyFocusChoice';

beforeEach(() => {
  mock.status = { available: true, authorized: true, enabled: false, active: false, selectionCount: 0, busy: false, error: null };
  mock.configure.mockReset(); mock.enabled.mockReset();
});
afterEach(cleanup);

test('unsupported devices add no option or active-session notice', () => {
  mock.status.available = false;
  const { container } = render(<><StudyFocusChoice /><StudyFocusStatus /></>);
  expect(container).toBeEmptyDOMElement();
});
test('the explicit picker button and switch use separate actions', () => {
  render(<StudyFocusChoice />);
  fireEvent.click(screen.getByRole('button', { name: 'Choose apps' }));
  expect(mock.configure).toHaveBeenCalledOnce();
  fireEvent.click(screen.getByRole('switch', { name: 'Block distracting apps' }));
  expect(mock.enabled).toHaveBeenCalledWith(true);
});
test('saved selections and on state are clear without exposing app names', () => {
  mock.status.selectionCount = 3; mock.status.enabled = true;
  render(<StudyFocusChoice />);
  expect(screen.getByRole('switch')).toHaveAttribute('aria-checked', 'true');
  expect(screen.getByText('3 selections · saved only on this device')).toBeVisible();
  expect(screen.getByRole('button', { name: 'Change apps' })).toBeVisible();
});
test('pending permission prevents duplicate prompts', () => {
  mock.status.busy = true;
  render(<StudyFocusChoice />);
  expect(screen.getByRole('button')).toBeDisabled();
  expect(screen.getByRole('switch')).toBeDisabled();
});
test('the active timer provides an explicit release control', () => {
  mock.status.enabled = true; mock.status.active = true;
  render(<StudyFocusStatus />);
  expect(screen.getByText('Your selected apps are blocked while you study.')).toBeVisible();
  fireEvent.click(screen.getByRole('button', { name: 'Turn off app blocking' }));
  expect(mock.enabled).toHaveBeenCalledWith(false);
});
test('failed blocking is visible rather than described as active', () => {
  mock.status.enabled = true; mock.status.error = 'Could not confirm app blocking.';
  render(<><StudyFocusChoice /><StudyFocusStatus /></>);
  expect(screen.getByRole('alert')).toHaveTextContent('Could not confirm app blocking.');
  expect(screen.getByRole('status')).toHaveTextContent('Could not confirm app blocking.');
  expect(screen.queryByText('Your selected apps are blocked while you study.')).not.toBeInTheDocument();
});
