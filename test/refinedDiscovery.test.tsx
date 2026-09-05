import React from 'react';
import { beforeEach, describe, expect, it, vi } from 'vitest';
import { fireEvent, render, screen } from '@testing-library/react';
import { getLastVisit, recordVisit } from '../components/lastVisited';
import { matchesToolSearch, PRACTICE_TOOL_IDS } from '../components/launchpadSearch';
import HomeNextStep from '../components/HomeNextStep';
import { type StudyBlock } from '../components/subjectData';
import ResumeCard from '../components/ResumeCard';

vi.mock('../hooks/useMobileAppDesign', () => ({ isMobileAppDesign: () => true }));

beforeEach(() => localStorage.clear());
describe('Launchpad discovery', () => {
  it('finds task language as well as product names', () => {
    expect(matchesToolSearch({ id: 'paper-trail', title: 'Paper Trail', description: 'Exam archive', tag: 'Understand' }, 'past papers')).toBe(true);
    expect(matchesToolSearch({ id: 'planner', title: 'Spaced Repetition Timetable', description: '', tag: 'Plan' }, 'weekly calendar')).toBe(true);
    expect(matchesToolSearch({ id: 'planner', title: 'Spaced Repetition Timetable', description: '', tag: 'Plan' }, 'unrelated')).toBe(false);
    expect(PRACTICE_TOOL_IDS.has('paper-trail')).toBe(true);
    expect(PRACTICE_TOOL_IDS.has('command-word-reflex')).toBe(true);
  });
  it('keeps the resume destination without collecting a recent-tools list', () => {
    expect(getLastVisit('a')).toBeNull();
    for (const id of ['planner', 'paper-trail', 'mark-bank', 'planner']) recordVisit('a', { id, kind: 'tool', label: id });
    recordVisit('a', { id: 'module-1', kind: 'module', label: 'A module' });
    expect(getLastVisit('a')).toMatchObject({ id: 'module-1', kind: 'module' });
    expect(localStorage.getItem('nsu-recent-tools:a')).toBeNull();
    expect(getLastVisit('b')).toBeNull();
    expect(getLastVisit(undefined)).toBeNull();
  });
});
describe('Home handoffs', () => {
  it('distinguishes a failed plan load from a rest day and offers working exits', () => {
    const plan = vi.fn();
    const study = vi.fn();
    render(<HomeNextStep blocks={[]} completions={[]} hasProfile error onPlan={plan} onStudy={study} onProgress={vi.fn()} />);
    expect(screen.getByRole('status')).toHaveTextContent('Your plan couldn’t load.');
    expect(screen.queryByText('Room to breathe today.')).toBeNull();
    fireEvent.click(screen.getByRole('button', { name: 'Open your plan' }));
    fireEvent.click(screen.getByRole('button', { name: 'Start a session' }));
    expect(plan).toHaveBeenCalledOnce();
    expect(study).toHaveBeenCalledOnce();
  });
  it('passes the tapped real timetable block to the unchanged study setup', () => {
    const planned = vi.fn();
    const blocks: StudyBlock[] = [{ subjectName: 'Biology', sessionType: 'revision', durationMinutes: 45 }, { subjectName: 'English', sessionType: 'practice', durationMinutes: 20 }];
    render(<HomeNextStep blocks={blocks} completions={[]} hasProfile onPlannedStudy={planned} onProgress={vi.fn()} />);
    fireEvent.click(screen.getByRole('button', { name: 'Study English: Practice, 20 minutes' }));
    expect(planned).toHaveBeenCalledWith(blocks[1], 1);
  });
  it('does not briefly claim a rest day before the timetable loads', () => {
    render(<HomeNextStep blocks={[]} completions={[]} hasProfile ready={false} onProgress={vi.fn()} />);
    expect(screen.getByRole('status')).toHaveTextContent('Getting your plan ready');
    expect(screen.queryByText('Room to breathe today.')).not.toBeInTheDocument();
  });
  it('keeps module browsing available even when there is nothing left to resume', () => {
    const browse = vi.fn();
    render(<ResumeCard allCourses={[]} userProgress={{}} onSelectModule={vi.fn()} onBrowseModules={browse} />);
    fireEvent.click(screen.getByRole('button', { name: 'Browse all modules' }));
    expect(browse).toHaveBeenCalledOnce();
  });
});
