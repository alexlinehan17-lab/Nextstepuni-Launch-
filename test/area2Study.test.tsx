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
import { TabBar } from '@/components/ui/Bars';
import { House, Timer } from 'lucide-react';

const device = vi.hoisted(() => ({ phone: false }));
vi.mock('@/hooks/useMobileAppDesign', () => ({ useMobileAppDesign: () => device.phone, isMobileAppDesign: () => device.phone }));

afterEach(cleanup);
beforeEach(() => { device.phone = false; });

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
