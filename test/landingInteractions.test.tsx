import React from 'react';
import { afterEach, describe, expect, it, vi } from 'vitest';
import { cleanup, fireEvent, render, screen, within } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import PassportGlass from '../components/landing/glass/PassportGlass';
import FutureFinderGlass from '../components/landing/glass/FutureFinderGlass';
import FutureFinderRevamped from '../components/FutureFinderRevamped';
import { DEMO_PROFILE } from '../components/landing/glass/demoProfile';
import { DEMO_STUDENT_UID } from '../data/devStudent';
import LockedButton from '../components/ui/LockedButton';
import CAOPointsSimulator from '../components/CAOPointsSimulator';

const state = vi.hoisted(() => ({ rawProgressDoc: {}, mocks: [], futureFinderPicks: [] }));
vi.mock('../contexts/ProgressContext', () => ({
  ProgressProvider: ({children}: React.PropsWithChildren) => children,
  useProgress: () => ({rawProgressDoc: state.rawProgressDoc, updateDemoProgress: vi.fn()}),
}));
vi.mock('../contexts/InnovationDataContext', () => ({
  InnovationDataProvider: ({children}: React.PropsWithChildren) => children,
  useInnovationData: () => ({mockResults:{isLoaded:true,mocks:state.mocks},futureFinderPicks:state.futureFinderPicks}),
}));
afterEach(() => { cleanup(); localStorage.clear(); });

describe('Landing interactions', () => {
  it('gives keyboard lock feedback without running the action', async () => {
    const action = vi.fn();
    const user = userEvent.setup();
    render(<LockedButton locked onClick={action}>Chemistry — available in the app</LockedButton>);
    await user.tab();
    await user.keyboard('{Enter}');
    expect(action).not.toHaveBeenCalled();
    expect(screen.getByRole('button')).toHaveClass('locked-control-shake');
    await user.keyboard(' ');
    expect(action).not.toHaveBeenCalled();
  });

  it('edits local sample grades and opens the explorer directly with Overview locked', async () => {
    render(<PassportGlass active sub="" />);
    const current = await screen.findByRole('combobox', {name:'English current grade'});
    const initialGrade = DEMO_PROFILE.subjects.find(s => s.subjectName === 'English')!.currentGrade;
    fireEvent.change(current, {target:{value:'H2'}});
    expect(current).toHaveValue('H2');
    expect(screen.getByText('444')).toBeInTheDocument();
    fireEvent.change(screen.getByRole('combobox',{name:'English target grade'}), {target:{value:'H1'}});
    expect(screen.getByText('543')).toBeInTheDocument();
    expect(DEMO_PROFILE.subjects.find(s => s.subjectName === 'English')!.currentGrade).toBe(initialGrade);
    fireEvent.click(screen.getByRole('button', {name:'Explore What If?'}));
    const tabs = await screen.findByRole('tablist', {name:'Points simulator view'});
    expect(within(tabs).getByRole('tab', {name:'What-If Explorer'})).toHaveAttribute('aria-selected','true');
    const overview = within(tabs).getByRole('tab', {name:'Overview'});
    expect(overview).toHaveAttribute('aria-disabled','true');
    fireEvent.click(overview);
    expect(overview).toHaveAttribute('aria-selected','false');
    expect(overview).toHaveClass('locked-control-shake');
    fireEvent.click(screen.getByRole('button',{name:'Edit subjects'}));
    expect(await screen.findByRole('combobox',{name:'English current grade'})).toHaveValue('H2');
  });

  it('keeps the standalone simulator Overview available', () => {
    render(<CAOPointsSimulator profile={DEMO_PROFILE} onOpenSettings={() => undefined} />);
    expect(screen.getByRole('tab',{name:'Overview'})).toHaveAttribute('aria-selected','true');
    fireEvent.click(screen.getByRole('tab',{name:'What-If Explorer'}));
    fireEvent.click(screen.getByRole('tab',{name:'Overview'}));
    expect(screen.getByRole('tab',{name:'Overview'})).toHaveAttribute('aria-selected','true');
  });

  it('shows results-only on the landing page but retains Retake in the full app', async () => {
    const view = render(<FutureFinderGlass active sub="" />);
    await screen.findByRole('heading',{name:'Your Top Matches'});
    expect(screen.queryByRole('button',{name:'Retake'})).not.toBeInTheDocument();
    expect(screen.getByRole('button',{name:'How are these results calculated?'})).toBeInTheDocument();
    view.unmount();
    render(<FutureFinderRevamped uid={DEMO_STUDENT_UID} profile={DEMO_PROFILE} />);
    expect(await screen.findByRole('button',{name:'Retake'})).toBeInTheDocument();
  });
});
