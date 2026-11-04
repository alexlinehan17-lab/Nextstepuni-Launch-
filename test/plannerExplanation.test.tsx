import React from 'react';
import { describe, expect, it, vi } from 'vitest';
import { render, screen, fireEvent, within } from '@testing-library/react';
import PlannerExplanation from '../components/launchpad/PlannerExplanation';
import { computeSubjectPriorities, allocateSessions } from '../components/timetableAlgorithm';
import { DEMO_PROFILE } from '../components/landing/glass/demoProfile';

const priorities = computeSubjectPriorities(DEMO_PROFILE.subjects);
const allocations = allocateSessions(priorities, 30, undefined, 45);
const props = {open:true,onClose:vi.fn(),priorities,allocations,totalSessions:8,totalMinutes:360,workloadExplanation:'Build a steady routine.'};

describe('Planner explanation', () => {
  it('shows the sample profile’s real best-six projection and selected allocation', () => {
    render(<PlannerExplanation {...props} />);
    expect(within(screen.getByRole('region', {name:'Projected CAO points'})).getByText('520')).toBeInTheDocument();
    fireEvent.click(screen.getByRole('button', {name:'Inspect Mathematics allocation'}));
    const detail = screen.getByRole('region', {name:'Mathematics allocation details'});
    expect(within(detail).getByText('+21')).toBeInTheDocument();
    expect(within(detail).getByText('×0.71')).toBeInTheDocument();
    expect(within(detail).getByText('×1.00')).toBeInTheDocument();
    expect(detail).toHaveTextContent('H5');
    expect(detail).toHaveTextContent('H3');
    expect(within(detail).getByText('1')).toBeInTheDocument();
  });
  it('does not mistake zero best-six gain for an already-met target', () => {
    render(<PlannerExplanation {...props} />);
    fireEvent.change(screen.getByLabelText('Look at a subject'), {target:{value:'Irish'}});
    const detail = screen.getByRole('region', {name:'Irish allocation details'});
    expect(detail).toHaveTextContent('O2');
    expect(detail).toHaveTextContent('O1');
    expect(within(detail).getByText(/would not change your current best-six total/)).toBeInTheDocument();
    expect(within(detail).queryByText(/already met|at or above your target/)).not.toBeInTheDocument();
  });
});
