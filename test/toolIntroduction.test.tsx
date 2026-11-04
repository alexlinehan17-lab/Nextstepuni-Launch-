import React, { StrictMode } from 'react';
import { fireEvent, render, screen, cleanup } from '@testing-library/react';
import { beforeEach, afterEach, describe, expect, test, vi } from 'vitest';
import ToolMasthead, { ToolIntroduction, ToolIntroductionContext } from '../components/launchpad/ToolMasthead';

const props = { tool: 'mark-bank' as const, title: 'The Mark Bank', eyebrow: 'Work the real questions', subtitle: 'Build your answer.', uid: 'student-a' };
beforeEach(() => localStorage.clear());
afterEach(() => { cleanup(); vi.restoreAllMocks(); });

describe('first-visit tool introductions', () => {
  test('can dismiss on first visit and stays dismissed on returning', () => {
    const { unmount } = render(<StrictMode><ToolIntroduction {...props} /></StrictMode>);
    expect(screen.getByRole('region', { name: 'The Mark Bank introduction' })).toBeInTheDocument();
    fireEvent.click(screen.getByRole('button', { name: 'Dismiss The Mark Bank introduction' }));
    expect(screen.queryByRole('region')).not.toBeInTheDocument();
    unmount();
    render(<ToolIntroduction {...props} />);
    expect(screen.queryByRole('region')).not.toBeInTheDocument();
  });
  test('a visit is remembered without dismissal, separately per tool and account', () => {
    const first = render(<ToolIntroduction {...props} />);
    first.unmount();
    const returned = render(<ToolIntroduction {...props} />);
    expect(screen.queryByRole('region')).not.toBeInTheDocument();
    returned.unmount();
    const otherTool = render(<ToolIntroduction {...props} tool="planner" title="Your Planner" />);
    expect(screen.getByRole('region', { name: 'Your Planner introduction' })).toBeInTheDocument();
    otherTool.unmount();
    render(<ToolIntroduction {...props} uid="student-b" />);
    expect(screen.getByRole('region', { name: 'The Mark Bank introduction' })).toBeInTheDocument();
  });
  test('blocked device storage does not prevent using or dismissing a tool', () => {
    vi.spyOn(Storage.prototype, 'getItem').mockImplementation(() => { throw new Error('blocked'); });
    vi.spyOn(Storage.prototype, 'setItem').mockImplementation(() => { throw new Error('blocked'); });
    render(<ToolIntroduction {...props} />);
    fireEvent.click(screen.getByRole('button', { name: 'Dismiss The Mark Bank introduction' }));
    expect(screen.queryByRole('region')).not.toBeInTheDocument();
  });
  test('the shell suppresses repeated mastheads without hiding functional children', () => {
    render(<ToolIntroductionContext.Provider value><ToolMasthead {...props}><button>Continue</button></ToolMasthead></ToolIntroductionContext.Provider>);
    expect(screen.queryByRole('heading')).not.toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Continue' })).toBeInTheDocument();
  });
});
