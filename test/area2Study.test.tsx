/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Area 2, the study session in the agreed look (c-study.html, r5-b1.html):
 * what a student can do and what assistive technology is told. The timer,
 * saving and restoring have their own suites (studyRoomMotion, studyTimerExtras,
 * studySessionExit, studySessionPersistence); nothing here measures time.
 */
import React, { useState } from 'react';
import { act, cleanup, fireEvent, render, screen, within } from '@testing-library/react';
import { afterEach, beforeEach, describe, expect, test, vi } from 'vitest';
import StudySessionSetup from '@/components/study/StudySessionSetup';
import StudyBreak from '@/components/study/StudyBreak';
import StudySessionTimer from '@/components/study/StudySessionTimer';
import { TabBar } from '@/components/ui/Bars';
import { CheckRow } from '@/components/ui/List';
import { Sheet } from '@/components/ui/Sheet';
import StudyTimeUp from '@/components/study/StudyTimeUp';
import StrategyPickerStep from '@/components/study/StrategyPickerStep';
import { House, Timer } from 'lucide-react';
import type * as MotionModule from '@/components/Motion';

const device = vi.hoisted(() => ({ phone: false, reduced: false }));
vi.mock('@/hooks/useMobileAppDesign', () => ({ useMobileAppDesign: () => device.phone, isMobileAppDesign: () => device.phone }));
vi.mock('@/components/Motion', async original => ({ ...await original<typeof MotionModule>(), useReducedMotion: () => device.reduced }));

afterEach(cleanup);
beforeEach(() => { device.phone = false; device.reduced = false; });

type Method = 'new-learning' | 'practice' | 'revision' | '';
function Setup({ start = vi.fn(), initial = {} as { subject?: string; method?: Method; minutes?: number }, clear }: {
  start?: () => void; initial?: { subject?: string; method?: Method; minutes?: number }; clear?: () => void;
}) {
  const [subject, setSubject] = useState(initial.subject ?? '');
  const [method, setMethod] = useState<Method>(initial.method ?? '');
  const [minutes, setMinutes] = useState(initial.minutes ?? 0);
  const canStart = Boolean(subject && method && minutes >= 5);
  return (
    <>
      <StudySessionSetup
        subjects={[{ subjectName: 'Mathematics', level: 'higher' }, { subjectName: 'Irish', level: 'higher' }]}
        selectedSubject={subject} onSubject={setSubject}
        selectedType={method} onType={setMethod}
        selectedMinutes={minutes} onMinutes={setMinutes}
        onClear={clear ?? (() => { setSubject(''); setMethod(''); setMinutes(0); })}
        todayBlocks={[]} onBlock={vi.fn()} sessionCount={0} todayMinutes={0} reflectionCount={3}
        onReflections={vi.fn()} onBack={vi.fn()} onStart={start} canStart={canStart} startHint={null}
      />
      <TabBar label="Main navigation" items={[{ id: 'tree', label: 'Home', icon: House }, { id: 'study', label: 'Study', icon: Timer }]} current="study" onSelect={vi.fn()} />
    </>
  );
}

describe('study set-up', () => {
  test('Start session names every missing step, takes the student to the first one and starts nothing', () => {
    const start = vi.fn();
    render(<Setup start={start} initial={{ subject: 'Mathematics' }} />);
    expect(screen.getByRole('button', { name: 'Still to choose: how you’ll work and your time.' })).toBeInTheDocument();
    const button = screen.getByRole('button', { name: 'Start session' });
    expect(button).toHaveAccessibleDescription('Still to choose: how you’ll work and your time.');
    fireEvent.click(button);
    expect(start).not.toHaveBeenCalled();
    const methods = screen.getByRole('radiogroup', { name: 'How will you work?' });
    expect(methods).toContainElement(document.activeElement as HTMLElement);
    expect(methods).toHaveAttribute('data-ui-nudge');
  });

  test('with only the time missing, it says so and takes the student to the time', () => {
    render(<Setup initial={{ subject: 'Mathematics', method: 'practice' }} />);
    fireEvent.click(screen.getByRole('button', { name: 'Start session' }));
    expect(screen.getByRole('button', { name: 'Still to choose: your time.' })).toBeInTheDocument();
    expect(screen.getByRole('radiogroup', { name: 'Make some time.' })).toContainElement(document.activeElement as HTMLElement);
  });

  test('a chosen subject, way of working and length are marked chosen for assistive technology', () => {
    const start = vi.fn();
    render(<Setup start={start} />);
    fireEvent.click(screen.getByRole('radio', { name: 'Irish' }));
    fireEvent.click(screen.getByRole('radio', { name: 'Revision Recall what you know' }));
    fireEvent.click(screen.getByRole('radio', { name: '25 min' }));
    expect(screen.getByRole('radio', { name: 'Irish' })).toHaveAttribute('aria-checked', 'true');
    expect(screen.getByRole('radio', { name: 'Mathematics' })).toHaveAttribute('aria-checked', 'false');
    expect(screen.getByRole('button', { name: 'Study Irish' })).toHaveAttribute('aria-pressed', 'true');
    expect(screen.getByRole('radio', { name: 'Revision Recall what you know' })).toHaveAttribute('aria-checked', 'true');
    expect(screen.getByRole('radio', { name: '25 min' })).toHaveAttribute('aria-checked', 'true');
    expect(screen.getByRole('radio', { name: '15 min' })).toHaveAttribute('aria-checked', 'false');
    // Ready: no missing step, and it starts.
    const button = screen.getByRole('button', { name: 'Start session' });
    expect(button).not.toHaveAttribute('data-missing');
    expect(screen.getByText('Irish · Revision · 25 min')).toBeInTheDocument();
    fireEvent.click(button);
    expect(start).toHaveBeenCalledOnce();
  });

  test('arrow keys move through the subjects and the ways of working, choosing as they go', () => {
    render(<Setup />);
    const maths = screen.getByRole('radio', { name: 'Mathematics' });
    maths.focus();
    fireEvent.keyDown(maths, { key: 'ArrowRight' });
    expect(screen.getByRole('radio', { name: 'Irish' })).toHaveAttribute('aria-checked', 'true');
    expect(screen.getByRole('radio', { name: 'Irish' })).toHaveFocus();
  });

  test('Cmd or Ctrl + Enter still starts a ready session (the plan card it replaces did)', () => {
    const start = vi.fn();
    render(<Setup start={start} initial={{ subject: 'Mathematics', method: 'practice' }} />);
    fireEvent.keyDown(window, { key: 'Enter', metaKey: true });
    expect(start).not.toHaveBeenCalled();
    fireEvent.click(screen.getByRole('radio', { name: '45 min' }));
    fireEvent.keyDown(window, { key: 'Enter', ctrlKey: true });
    expect(start).toHaveBeenCalledOnce();
  });

  test('on a phone it is the Study place until something is chosen; then Start takes the tab bar\'s place, and Cancel gives it back', () => {
    device.phone = true;
    render(<Setup />);
    expect(screen.getByRole('navigation', { name: 'Main navigation' })).toBeVisible();
    expect(screen.queryByRole('button', { name: 'Start session' })).not.toBeInTheDocument();
    expect(screen.queryByRole('button', { name: 'Cancel' })).not.toBeInTheDocument();
    expect(screen.getByText('The Study Room')).toBeInTheDocument();
    act(() => { fireEvent.click(screen.getByRole('radio', { name: 'Mathematics' })); });
    expect(screen.queryByRole('navigation', { name: 'Main navigation' })).not.toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Start session' })).toHaveAttribute('data-missing');
    act(() => { fireEvent.click(screen.getByRole('button', { name: 'Cancel' })); });
    expect(screen.getByRole('radio', { name: 'Mathematics' })).toHaveAttribute('aria-checked', 'false');
    expect(screen.getByRole('navigation', { name: 'Main navigation' })).toBeVisible();
    expect(screen.queryByRole('button', { name: 'Start session' })).not.toBeInTheDocument();
  });

  test('the to-dos are dotted rings: set once chosen, never filled before the session', () => {
    const { container } = render(<Setup initial={{ subject: 'Mathematics' }} />);
    const list = screen.getByRole('list', { name: 'To-dos' });
    const dots = list.querySelectorAll('svg.study-dot');
    expect(dots).toHaveLength(3);
    expect(dots[0]).toHaveAttribute('data-set');
    expect(dots[1]).not.toHaveAttribute('data-set');
    expect(container.querySelector('svg.study-dot[data-done]')).toBeNull();
    expect(within(list).getByText('Choose how you’ll work')).toBeInTheDocument();
  });
});

describe('the study room and the breathing guide', () => {
  const timer = (extra: Partial<React.ComponentProps<typeof StudySessionTimer>> = {}) => (
    <StudySessionTimer subject="Mathematics" subjectColor="#2d3436" type="Practice" totalSeconds={1500} elapsedSeconds={477}
      paused={false} onLeave={vi.fn()} onTogglePause={vi.fn()} prompt={null} onCompletePrompt={vi.fn()} onSkipPrompt={vi.fn()} {...extra} />
  );

  test('Close at the left puts the room away while the timer runs; ending is on the pause screen', () => {
    const minimise = vi.fn(), leave = vi.fn();
    render(timer({ onMinimise: minimise, onLeave: leave }));
    fireEvent.click(screen.getByRole('button', { name: 'Close the room. Your session keeps running.' }));
    expect(minimise).toHaveBeenCalledOnce();
    expect(leave).not.toHaveBeenCalled();
    expect(screen.queryByRole('button', { name: 'Leave study session' })).not.toBeInTheDocument();
    // The Rule replaces the orange strip and bar: one orange tick, the time to come inked.
    const progress = screen.getByRole('progressbar', { name: 'Session progress' });
    expect(progress).toHaveAttribute('aria-valuenow', '32');
    expect(progress.querySelectorAll('.study-rule > i')).toHaveLength(51);
    expect(progress.querySelectorAll('.study-rule > b')).toHaveLength(1);
    expect(document.querySelector('.ss-ink-edge')).toBeNull();
    expect(screen.getByRole('timer')).toHaveTextContent('17:03');
  });

  test('where the room cannot be put away, the same corner leaves (as today)', () => {
    const leave = vi.fn();
    render(timer({ onLeave: leave }));
    fireEvent.click(screen.getByRole('button', { name: 'Leave study session' }));
    expect(leave).toHaveBeenCalledOnce();
  });

  test.each([false, true])('the breathing guide keeps today\'s ten-second breath, and stops for reduced motion: %s', async reduced => {
    device.reduced = reduced;
    const effects: KeyframeAnimationOptions[] = [];
    Object.defineProperty(Element.prototype, 'animate', { configurable: true, value: (_frames: Keyframe[], options: KeyframeAnimationOptions) => {
      effects.push(options);
      return { finished: Promise.resolve(), cancel: vi.fn() } as unknown as Animation;
    } });
    try {
      render(<StudyBreak subject="Mathematics" elapsedSeconds={1070} onResume={vi.fn()} onLeave={vi.fn()} />);
      expect(screen.queryByText('Your place is right here.')).not.toBeInTheDocument();
      fireEvent.click(screen.getByRole('button', { name: 'Take a few slow breaths' }));
      await act(async () => { await new Promise(resolve => setTimeout(resolve, 0)); });
      const guide = screen.getByRole('dialog', { name: 'Take a moment.' });
      expect(within(guide).queryByText('Your place is right here.')).not.toBeInTheDocument();
      const breaths = effects.filter(options => options.iterations === Infinity);
      if (reduced) expect(breaths).toHaveLength(0);
      else {
        expect(breaths).toHaveLength(2);
        expect(breaths.every(options => options.duration === 10000)).toBe(true);
      }
    } finally {
      delete (Element.prototype as { animate?: unknown }).animate;
    }
  });
});

describe('after the session, and the parts it added', () => {
  test('Time\'s up brings the to-dos back: the set ones fill, the student\'s own fills when tapped, nothing is saved', () => {
    device.reduced = true;
    const todos = [{ label: 'Mathematics', done: true }, { label: 'Work through questions', done: true }, { label: '2024 Paper 1, Question 6', done: false }];
    render(<StudyTimeUp subject="Mathematics" elapsedSeconds={1500} extendedMinutes={0} extensionBonus={0} sessionPoints={20} onKeepGoing={vi.fn()} onFinish={vi.fn()} todos={todos} />);
    const own = screen.getByRole('checkbox', { name: '2024 Paper 1, Question 6' });
    expect(screen.getByRole('checkbox', { name: 'Mathematics' })).toHaveAttribute('aria-checked', 'true');
    expect(own).toHaveAttribute('aria-checked', 'false');
    expect(screen.getByText('2 / 3')).toBeInTheDocument();
    fireEvent.click(own);
    expect(own).toHaveAttribute('aria-checked', 'true');
    expect(screen.getByText('3 / 3')).toBeInTheDocument();
    expect(screen.getByLabelText('Session details')).toHaveTextContent('25 minutes');
  });

  test('what helped you focus: square ticks marked for assistive technology, and Continue says what it needs', () => {
    const go = vi.fn();
    render(<StrategyPickerStep learnedStrategyIds={[]} autoTrackedIds={[]} onContinue={go} subject="Mathematics" durationSeconds={1500} pointsEarned={20} />);
    const recall = screen.getByRole('checkbox', { name: 'Active Recall' });
    expect(recall).toHaveAttribute('aria-checked', 'false');
    fireEvent.click(screen.getByRole('button', { name: 'Continue' }));
    expect(go).not.toHaveBeenCalled();
    expect(screen.getByRole('button', { name: 'Select strategies to continue.' })).toBeInTheDocument();
    fireEvent.click(recall);
    expect(recall).toHaveAttribute('aria-checked', 'true');
    fireEvent.click(screen.getByRole('button', { name: 'Continue with 1 strategy' }));
    expect(go).toHaveBeenCalledWith(['mastering-active-recall-protocol']);
  });

  test('CheckRow is a checkbox row; a plain Sheet has its title and no Close', () => {
    const change = vi.fn();
    render(<><CheckRow checked={false} onChange={change} mark={<i />}>Tick me</CheckRow>
      <Sheet open plain title="Finish for now?" onClose={vi.fn()}><p>Body</p></Sheet></>);
    fireEvent.click(screen.getByRole('checkbox', { name: 'Tick me' }));
    expect(change).toHaveBeenCalledWith(true);
    const sheet = screen.getByRole('dialog', { name: 'Finish for now?' });
    expect(within(sheet).queryByRole('button', { name: 'Close' })).not.toBeInTheDocument();
  });
});
