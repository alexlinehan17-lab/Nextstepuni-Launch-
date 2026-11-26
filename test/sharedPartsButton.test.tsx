/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The shared button (components/ui/Button.tsx): a main button never goes dead.
 * While a step is missing, the sentence directly above it names the step, and
 * pressing the sentence or the button moves focus to that step
 * (components.md, "States"; audit 03 B.8.1: today Start Session fades to half
 * strength, ignores taps and names only the first gap at the foot of the page).
 */
import { useRef, useState } from 'react';
import { cleanup, fireEvent, render, screen } from '@testing-library/react';
import { afterEach, expect, test, vi } from 'vitest';
import { Button, IconButton, TextButton } from '@/components/ui/Button';

afterEach(cleanup);

function SetUp({ onStart }: { onStart: () => void }) {
  const subjectRef = useRef<HTMLDivElement>(null);
  const [subject, setSubject] = useState<string | null>(null);
  return (
    <>
      <div ref={subjectRef} role="radiogroup" aria-label="Subject">
        {[['bio', 'Biology'], ['maths', 'Mathematics']].map(([value, label]) => (
          <label key={value}><input type="radio" name="subject" checked={subject === value} onChange={() => setSubject(value)} />{label}</label>
        ))}
      </div>
      <Button kind="main" size="lg" block arrow="forward" onClick={onStart}
        missing={subject ? undefined : { sentence: 'Choose a subject to continue.', goTo: subjectRef }}>
        {subject ? 'Start session' : 'Choose your subject'}
      </Button>
    </>
  );
}

test('the sentence above a main button that cannot go yet moves focus to the missing step', () => {
  const onStart = vi.fn();
  render(<SetUp onStart={onStart} />);
  const sentence = screen.getByRole('button', { name: 'Choose a subject to continue.' });
  expect(document.activeElement).toBe(document.body);
  fireEvent.click(sentence);
  // Focus lands on the first choice of the missing group (nothing is chosen yet).
  expect(document.activeElement).toBe(screen.getByRole('radio', { name: 'Biology' }));
  expect(onStart).not.toHaveBeenCalled();
});

test('the button itself stays pressable: pressing it early also takes the student to the missing step', () => {
  const onStart = vi.fn();
  render(<SetUp onStart={onStart} />);
  const main = screen.getByRole('button', { name: 'Choose your subject' });
  expect(main).not.toBeDisabled();
  expect(main).not.toHaveAttribute('aria-disabled');
  // It is described by the sentence, for a screen reader.
  expect(main).toHaveAccessibleDescription('Choose a subject to continue.');
  fireEvent.click(main);
  expect(document.activeElement).toBe(screen.getByRole('radio', { name: 'Biology' }));
  expect(onStart).not.toHaveBeenCalled();
});

test('once nothing is missing, the sentence goes and the button does its job', () => {
  const onStart = vi.fn();
  render(<SetUp onStart={onStart} />);
  fireEvent.click(screen.getByRole('radio', { name: 'Mathematics' }));
  expect(screen.queryByRole('button', { name: 'Choose a subject to continue.' })).not.toBeInTheDocument();
  fireEvent.click(screen.getByRole('button', { name: 'Start session' }));
  expect(onStart).toHaveBeenCalledTimes(1);
});

test('a missing step given as a function is opened by it (a carousel, a sheet)', () => {
  const open = vi.fn();
  render(<Button kind="main" missing={{ sentence: 'Choose how long to study.', goTo: open }}>Choose how long</Button>);
  fireEvent.click(screen.getByRole('button', { name: 'Choose how long to study.' }));
  fireEvent.click(screen.getByRole('button', { name: 'Choose how long' }));
  expect(open).toHaveBeenCalledTimes(2);
});

test('something truly unavailable says why, stays focusable, and does nothing when pressed', () => {
  const onClick = vi.fn();
  render(<Button block unavailable="Opens when you finish Your interests." onClick={onClick}>Start What matters</Button>);
  const button = screen.getByRole('button', { name: 'Start What matters' });
  expect(button).toHaveAttribute('aria-disabled', 'true');
  expect(button).toHaveAccessibleDescription('Opens when you finish Your interests.');
  fireEvent.click(button);
  expect(onClick).not.toHaveBeenCalled();
});

test('rank is shown by kind, not size: kinds and heights are separate classes; there is no orange kind', () => {
  render(<>
    <Button kind="main">Practise</Button>
    <Button>Browse topics</Button>
    <Button size="sm">Filter</Button>
    <TextButton tone="danger">Delete account</TextButton>
    <IconButton label="Back" icon={<svg />} />
  </>);
  expect(screen.getByRole('button', { name: 'Practise' }).className).toMatch(/\bui-btn--main\b/);
  expect(screen.getByRole('button', { name: 'Practise' }).className).not.toMatch(/--lg|--sm/);
  expect(screen.getByRole('button', { name: 'Browse topics' }).className).not.toMatch(/--main/);
  // The 36px size keeps a 44px press area (frame-hit), and so does a short text button.
  expect(screen.getByRole('button', { name: 'Filter' })).toHaveClass('ui-btn--sm', 'frame-hit');
  expect(screen.getByRole('button', { name: 'Delete account' })).toHaveClass('ui-link--danger', 'frame-hit');
  expect(screen.getByRole('button', { name: 'Back' })).toHaveClass('ui-icon-btn');
});
