import React, { useState } from 'react';
import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import { describe, expect, test, vi } from 'vitest';
import Subjects from '@/components/landing/sections/Subjects';
import catalogue from '@/components/landing/subjectShowcase.json';
import StudySessionFinish from '@/components/study/StudySessionFinish';
import StudyBreak from '@/components/study/StudyBreak';
import { curateAchievements } from '@/components/AchievementGallery';
import { getAchievementsForCurriculum } from '@/achievementData';

describe('subject carousel', () => {
  test('shows five cards and two previews, updates real stats, and wraps in both directions', () => {
    const { container } = render(<Subjects />);
    expect(container.querySelectorAll('.lsc-card:not(.lsc-peek)')).toHaveLength(5);
    expect(container.querySelectorAll('.lsc-peek')).toHaveLength(2);
    const subject = screen.getByRole('combobox', { name: 'Jump to a subject' });
    fireEvent.change(subject, { target: { value: 'biology' } });
    expect(screen.getByLabelText('Biology resources')).toHaveTextContent('1,359');
    const lc = catalogue.filter(item => item.cycle === 'lc');
    fireEvent.change(subject, { target: { value: lc[0].id } });
    fireEvent.click(screen.getByRole('button', { name: 'Previous subject' }));
    expect(subject).toHaveValue(lc.at(-1)!.id);
    fireEvent.click(screen.getByRole('button', { name: 'Next subject' }));
    expect(subject).toHaveValue(lc[0].id);
    fireEvent.keyDown(screen.getByRole('region', { name: 'Explore subjects' }), { key: 'ArrowRight' });
    expect(subject).toHaveValue(lc[1].id);
  });
  test('keeps programme catalogues separate and distinguishes unavailable resources', () => {
    render(<Subjects />);
    fireEvent.change(screen.getByRole('combobox', { name: 'Exam programme' }), { target: { value: 'jc' } });
    const jc = catalogue.filter(item => item.cycle === 'jc');
    expect(screen.getByRole('combobox', { name: 'Jump to a subject' })).toHaveValue(jc[0].id);
    expect(screen.getAllByText('Not yet available for this subject').length).toBeGreaterThan(0);
    expect(screen.getByRole('combobox', { name: 'Jump to a subject' }).children).toHaveLength(jc.length);
  });
  test('flicks horizontally without hijacking vertical scrolling or selecting a released card', () => {
    render(<Subjects />);
    const region = screen.getByRole('region', { name: 'Explore subjects' });
    const subject = screen.getByRole('combobox', { name: 'Jump to a subject' });
    fireEvent.pointerDown(region, { clientX: 200, clientY: 100 });
    fireEvent.pointerUp(region, { clientX: 190, clientY: 200 });
    expect(subject).toHaveValue('music');
    fireEvent.pointerDown(region, { clientX: 200, clientY: 100 });
    fireEvent.pointerUp(region, { clientX: 100, clientY: 105 });
    expect(subject).toHaveValue('ancient-greek');
    fireEvent.click(screen.getByRole('button', { name: 'Explore Music' }));
    expect(subject).toHaveValue('ancient-greek');
    fireEvent.wheel(region, { deltaX: 0, deltaY: 60 });
    expect(subject).toHaveValue('ancient-greek');
    fireEvent.wheel(region, { deltaX: 60, deltaY: 0 });
    expect(subject).toHaveValue('art');
  });
});

const finishProps = {
  subject: 'Irish', elapsedSeconds: 1505, plannedSeconds: 1800, practice: 'Revision',
  character: 'star-crew:stargazer', strategies: ['Active Recall'], basePoints: 25, isSaving: false,
};

describe('session receipt and debrief', () => {
  test('uses actual time and validates the quick debrief before saving once', async () => {
    let release: () => void = () => {};
    const onSave = vi.fn(() => new Promise<void>(resolve => { release = resolve; }));
    render(<StudySessionFinish {...finishProps} mode="quick" onModeChange={vi.fn()} onSave={onSave} onSkip={vi.fn()} />);
    expect(screen.getByLabelText('Your study receipt')).toHaveTextContent('25 min 5 sec');
    expect(screen.getByText('Session ended early')).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Keep this session' })).toBeDisabled();
    fireEvent.click(screen.getByRole('button', { name: 'Good' }));
    fireEvent.click(screen.getByRole('button', { name: 'Keep this session' }));
    expect(screen.getByRole('button', { name: 'Save without a debrief' })).toBeDisabled();
    expect(onSave).toHaveBeenCalledExactlyOnceWith('good');
    release();
    await waitFor(() => expect(screen.getByRole('button', { name: 'Keep this session' })).toBeEnabled());
  });
  test('keeps a failed full reflection for retry and preserves its structured confidence', async () => {
    const onSave = vi.fn().mockRejectedValueOnce(new Error('offline')).mockResolvedValueOnce(undefined);
    render(<StudySessionFinish {...finishProps} mode="full" onModeChange={vi.fn()} onSave={onSave} onSkip={vi.fn()} />);
    fireEvent.click(screen.getByRole('button', { name: 'Okay' }));
    const note = screen.getByRole('textbox');
    fireEvent.change(note, { target: { value: 'Short' } });
    expect(screen.getByRole('button', { name: 'Keep this session' })).toBeDisabled();
    fireEvent.change(note, { target: { value: 'Next time I will revisit the verbs.' } });
    fireEvent.click(screen.getByRole('button', { name: 'Keep this session' }));
    await screen.findByRole('alert');
    expect(note).toHaveValue('Next time I will revisit the verbs.');
    fireEvent.click(screen.getByRole('button', { name: 'Keep this session' }));
    await waitFor(() => expect(onSave).toHaveBeenCalledTimes(2));
    expect(onSave).toHaveBeenLastCalledWith('okay|Next time I will revisit the verbs.');
  });
  test('saving without a debrief does not submit reflection or bonus data', async () => {
    const skip = vi.fn().mockResolvedValue(undefined), save = vi.fn();
    function Finish() { const [mode, setMode] = useState<'quick' | 'full'>('quick'); return <StudySessionFinish {...finishProps} mode={mode} onModeChange={setMode} onSave={save} onSkip={skip} />; }
    render(<Finish />);
    fireEvent.click(screen.getByRole('button', { name: 'Save without a debrief' }));
    await waitFor(() => expect(skip).toHaveBeenCalledOnce());
    expect(save).not.toHaveBeenCalled();
  });
});

test('break starts only when shown, keeps actual studied time, and resumes explicitly', () => {
  const resume = vi.fn(), leave = vi.fn();
  render(<StudyBreak subject="Irish" elapsedSeconds={301} onResume={resume} onLeave={leave} />);
  expect(screen.getByText('5 min 1 sec studied · Timer paused')).toBeInTheDocument();
  expect(resume).not.toHaveBeenCalled();
  fireEvent.click(screen.getByRole('button', { name: 'Take a few slow breaths' }));
  expect(screen.getByText('Breathe in, gently…')).toBeInTheDocument();
  fireEvent.click(screen.getByRole('button', { name: 'Back to study' }));
  expect(resume).toHaveBeenCalledOnce();
  fireEvent.click(screen.getByRole('button', { name: 'Finish for now' }));
  expect(leave).toHaveBeenCalledOnce();
});

test('curated achievements keep all earned stamps and limit upcoming milestones', () => {
  const all = getAchievementsForCurriculum('senior');
  const earned = new Set(all.filter((_, i) => i % 4 === 0).map(item => item.id));
  const curated = curateAchievements(all, earned, false);
  for (const id of earned) expect(curated.some(item => item.id === id)).toBe(true);
  for (const category of new Set(all.map(item => item.category))) {
    expect(curated.filter(item => item.category === category && !earned.has(item.id)).length).toBeLessThanOrEqual(2);
  }
  expect(curateAchievements(all, earned, true)).toHaveLength(all.filter(item => !item.isHidden || earned.has(item.id)).length);
});
