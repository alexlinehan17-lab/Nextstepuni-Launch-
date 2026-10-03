import React from 'react';
import { act, cleanup, fireEvent, render, screen, within } from '@testing-library/react';
import { afterEach, beforeEach, expect, test, vi } from 'vitest';
import FutureFinderPaper from '../components/FutureFinderPaper';
import { computeAnalysis } from '../components/futureFinderAnalysis';
import type { FutureFinderRevampedState } from '../hooks/useFutureFinderRevamped';
import type { StudentSubjectProfile } from '../components/subjectData';
const state = vi.hoisted(() => ({ saved: null as FutureFinderRevampedState | null, persist: vi.fn(), reset: vi.fn() }));
vi.mock('../hooks/useFutureFinderRevamped', () => ({useFutureFinderRevamped:()=>({...state,isLoaded:true})}));
const profile: StudentSubjectProfile = {subjects:[{subjectName:'Mathematics',level:'higher',targetGrade:'H1'}],examStartDate:'2027-06-09',restDays:[],createdAt:'',updatedAt:''};
beforeEach(()=>{state.saved=null;state.persist.mockClear();Element.prototype.scrollIntoView=vi.fn();});
afterEach(()=>{cleanup();vi.useRealTimers();});

test('the focus flow saves the final answer, values, and actual ranked results', () => {
  render(<FutureFinderPaper uid="student-test" profile={profile}/>);
  fireEvent.click(screen.getByRole('radio',{name:/Quick discovery/}));
  fireEvent.click(screen.getByRole('button',{name:'Let’s explore'}));
  vi.useFakeTimers();
  for(let i=0;i<42;i++) {
    const scale = document.querySelector('.ff-answer-scale')!;
    fireEvent.click(within(scale as HTMLElement).getAllByRole('button')[3]);
    expect(screen.queryByText('Keep this answer')).not.toBeInTheDocument();
    act(()=>vi.advanceTimersByTime(300));
  }
  expect(state.persist).toHaveBeenCalledOnce();
  const saved = state.persist.mock.calls[0][0] as FutureFinderRevampedState;
  expect(Object.keys(saved.responses)).toHaveLength(30);
  expect(Object.keys(saved.valueResponses)).toHaveLength(12);
  expect(Object.values(saved.valueResponses)).toEqual(Array(12).fill(4));
  expect(saved.topMatches).toEqual(computeAnalysis(saved.responses,saved.valueResponses,125,['Mathematics']).shown.slice(0,10).map(item=>item.course.code));
  expect(saved.picks).toEqual([]);
});

test('saved results restore, expose all course facts, and preserve answers when bookmarking', () => {
  state.saved={length:'quick',responses:{R1:4,I1:5},valueResponses:{},completedAt:'2026-09-28',updatedAt:'2026-09-28',picks:[],rankingVersion:2};
  render(<FutureFinderPaper profile={profile} uid="student-test"/>);
  const course = document.querySelector('.ff-course')! as HTMLElement;
  fireEvent.click(within(course).getByRole('button',{name:'Save'}));
  expect(state.persist.mock.lastCall?.[0]).toMatchObject({responses:state.saved.responses,valueResponses:{},picks:[expect.any(String)]});
  fireEvent.click(within(course).getByRole('button',{name:'Explore'}));
  const dialog = screen.getByRole('dialog');
  for(const label of ['Region','Salary band','Duration','Typical entry','Why it appears here','Possible paths']) expect(within(dialog).getByText(label)).toBeInTheDocument();
  expect(within(dialog).getByRole('link',{name:/Visit .* page/})).toHaveAttribute('href');
});
