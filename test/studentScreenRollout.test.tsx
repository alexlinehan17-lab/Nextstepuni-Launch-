import React from 'react';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { act, fireEvent, render, renderHook, screen, cleanup } from '@testing-library/react';
import StudentHomeContent from '@/components/StudentHomeContent';
import ModuleCompleteScreen from '@/components/ModuleCompleteScreen';
import { useStudyTimerAppearance } from '@/hooks/useStudyTimerAppearance';
import { recordVisit } from '@/components/lastVisited';
import { ALL_COURSES as courseData } from '@/courseData';

beforeEach(() => localStorage.clear());
afterEach(() => { cleanup(); vi.useRealTimers(); });

describe('student Home navigation', () => {
  it('resumes the last available unfinished module and keeps the destination actions', () => {
    const courses = courseData.slice(0, 2);
    recordVisit('student-a', { kind: 'module', id: courses[1].id, label: courses[1].title });
    const select = vi.fn(); const direction = vi.fn(); const browse = vi.fn();
    render(<StudentHomeContent uid="student-a" allCourses={courses} categoryTitles={{}} userProgress={{ [courses[1].id]: { unlockedSection: 1 } }} onSelectModule={select} onGoToModules={browse} onGoToDashboard={vi.fn()} onGoToLearningPaths={vi.fn()} onGoToDirection={direction} onGoToJourney={vi.fn()} onGoToInnovationZone={vi.fn()} />);
    fireEvent.click(screen.getByRole('button', { name: 'Continue learning' }));
    expect(select).toHaveBeenCalledWith(courses[1].id);
    fireEvent.click(screen.getByRole('button', { name: /My Direction/ }));
    expect(direction).toHaveBeenCalledOnce();
    fireEvent.click(screen.getByRole('button', { name: 'Browse all five module worlds' }));
    expect(browse).toHaveBeenCalledOnce();
  });

  it('does not reopen a completed or unavailable saved module', () => {
    const course = courseData[0];
    recordVisit('student-a', { kind: 'module', id: 'unavailable', label: 'Hidden module' });
    render(<StudentHomeContent uid="student-a" allCourses={[course]} categoryTitles={{}} userProgress={{ [course.id]: { unlockedSection: course.sectionsCount } }} onSelectModule={vi.fn()} onGoToModules={vi.fn()} onGoToDashboard={vi.fn()} onGoToLearningPaths={vi.fn()} onGoToJourney={vi.fn()} onGoToInnovationZone={vi.fn()} />);
    expect(screen.getByRole('heading', { name: 'Look how far you’ve come.' })).toBeInTheDocument();
    expect(screen.queryByRole('button', { name: 'Continue learning' })).not.toBeInTheDocument();
  });
});

describe('timer appearance preference', () => {
  it('defaults to After hours, persists a change and isolates student accounts', () => {
    const { result, rerender, unmount } = renderHook(({ uid }) => useStudyTimerAppearance(uid), { initialProps: { uid: 'a' } });
    expect(result.current[0]).toBe('ink');
    act(() => result.current[1]('layers'));
    expect(result.current[0]).toBe('layers');
    rerender({ uid: 'b' });
    expect(result.current[0]).toBe('ink');
    unmount();
    const restored = renderHook(() => useStudyTimerAppearance('a'));
    expect(restored.result.current[0]).toBe('layers');
  });
});

it('keeps completion navigation separate from practice and review', () => {
  const practice = vi.fn(); const back = vi.fn(); const review = vi.fn();
  render(<ModuleCompleteScreen isOpen moduleTitle="The Driver’s Manual" categoryColor="#ff7915" sectionsCount={6} onContinue={back} onPractice={practice} onReview={review} />);
  expect(screen.getByText('6 sections complete')).toBeInTheDocument();
  fireEvent.click(screen.getByRole('button', { name: 'Put it into practice' }));
  expect(practice).toHaveBeenCalledOnce(); expect(back).not.toHaveBeenCalled();
  fireEvent.click(screen.getByRole('button', { name: 'Back to the programme' }));
  expect(back).toHaveBeenCalledOnce();
  fireEvent.click(screen.getByRole('button', { name: 'Review module' }));
  expect(review).toHaveBeenCalledOnce();
});
