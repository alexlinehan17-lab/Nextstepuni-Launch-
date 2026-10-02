import React, { useState } from 'react';
import { cleanup, fireEvent, render, screen, within } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { afterEach, expect, test, vi } from 'vitest';
import StudySessionSetup from '@/components/study/StudySessionSetup';
import type { PlanStep } from '../components/approved-ui-runtime';

afterEach(cleanup);
function Harness({
  onStart,
}: {
  onStart: (subject: string, method: string, minutes: number) => void;
}) {
  const [subject, setSubject] = useState('Geography');
  const [method, setMethod] = useState<'practice' | 'new-learning' | 'revision'>('practice');
  const [minutes, setMinutes] = useState(25);
  const [todos, setTodos] = useState<PlanStep[] | null>(null);
  return (
    <StudySessionSetup
      subjects={[
        { subjectName: 'Geography', level: 'higher' },
        { subjectName: 'Irish', level: 'higher' },
      ]}
      selectedSubject={subject}
      onSubject={setSubject}
      selectedType={method}
      onType={setMethod}
      selectedMinutes={minutes}
      onMinutes={setMinutes}
      todos={todos}
      onTodosChange={setTodos}
      todayBlocks={[]}
      onBlock={vi.fn()}
      sessionCount={0}
      todayMinutes={0}
      reflectionCount={0}
      onReflections={vi.fn()}
      onBack={vi.fn()}
      onStart={() => onStart(subject, method, minutes)}
      canStart={minutes >= 5}
      startHint={null}
    />
  );
}

test('the approved subject and method controls start a real session with the selected duration', async () => {
  const start = vi.fn();
  const user = userEvent.setup();
  render(<Harness onStart={start} />);
  await user.click(screen.getByRole('radio', { name: 'Irish' }));
  expect(screen.getByRole('button', { name: 'Study Irish' })).toHaveAttribute(
    'aria-pressed',
    'true',
  );
  await user.click(screen.getByRole('radio', { name: 'Revision Recall what you know' }));
  await user.click(screen.getByRole('button', { name: '45 min' }));
  await user.click(screen.getByRole('button', { name: 'Start Session' }));
  expect(start).toHaveBeenCalledWith('Irish', 'revision', 45);
});

test('to-dos can be changed, removed and added; cancel discards drafts and editing cannot start the timer', async () => {
  const start = vi.fn();
  const user = userEvent.setup();
  render(<Harness onStart={start} />);
  await user.click(screen.getByRole('button', { name: 'Edit to-dos' }));
  let dialog = screen.getByRole('dialog', { name: 'Edit your to-dos' });
  const first = within(dialog).getByRole('textbox', { name: 'To-do 1' });
  await user.clear(first);
  await user.type(first, 'Practise river processes');
  fireEvent.keyDown(window, { key: 'Enter', metaKey: true });
  expect(start).not.toHaveBeenCalled();
  await user.click(within(dialog).getByRole('button', { name: 'Cancel' }));
  expect(screen.queryByText('Practise river processes')).not.toBeInTheDocument();
  await user.click(screen.getByRole('button', { name: 'Edit to-dos' }));
  dialog = screen.getByRole('dialog', { name: 'Edit your to-dos' });
  expect(within(dialog).getByRole('textbox', { name: 'To-do 1' })).toHaveValue('Geography');
  await user.click(within(dialog).getByRole('button', { name: 'Remove to-do 3' }));
  await user.click(within(dialog).getByRole('button', { name: 'Add a to-do' }));
  await user.type(
    within(dialog).getByRole('textbox', { name: 'To-do 3' }),
    'Practise river processes',
  );
  await user.click(within(dialog).getByRole('button', { name: 'Save to-dos' }));
  expect(await screen.findByText('Practise river processes')).toBeInTheDocument();
  await user.click(screen.getByRole('button', { name: 'Start Session' }));
  expect(start).toHaveBeenCalledWith('Geography', 'practice', 25);
});

test('the timer colour control changes both ways and can be operated from its label', async () => {
  function TimerChoice() {
    const [colour, setColour] = useState(false);
    return <StudySessionSetup subjects={[]} selectedSubject="" selectedType="practice" selectedMinutes={25} onSubject={vi.fn()} onType={vi.fn()} onMinutes={vi.fn()} todayBlocks={[]} onBlock={vi.fn()} sessionCount={0} todayMinutes={0} reflectionCount={0} onReflections={vi.fn()} onBack={vi.fn()} onStart={vi.fn()} canStart={false} startHint={null} colourfulTimer={colour} onColourfulTimerChange={setColour} />;
  }
  render(<TimerChoice />);
  const user = userEvent.setup();
  const toggle = screen.getByRole('switch', { name:'I want my timer to have more colour!' });
  await user.click(screen.getByText('I want my timer to have more colour!'));
  expect(toggle).toHaveAttribute('aria-checked','true');
  expect(screen.getByText(/Paper horizon/)).toBeInTheDocument();
  toggle.focus(); await user.keyboard(' ');
  expect(toggle).toHaveAttribute('aria-checked','false');
  expect(screen.getByText(/After hours/)).toBeInTheDocument();
});
