/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Area 7a: the Launchpad's list of tools, the four tools leaving the app, and no black card.
 * The list keeps today's order with twelve tools; the categories menu filters as the tray did;
 * no door in the interface reaches Catch-Up Lane, War Room, Your Possible Life or the Academic
 * Journey Simulator, while each one's own address still opens it; no tool shows a black card.
 */
import React from 'react';
import { readFileSync } from 'node:fs';
import { join } from 'node:path';
import { afterEach, beforeEach, describe, expect, test, vi } from 'vitest';
import { cleanup, fireEvent, render, screen, within } from '@testing-library/react';

const navigation = vi.hoisted(() => ({
  activeTool: null as string | null,
  setActiveTool: vi.fn(),
  goBack: vi.fn(),
  navigateToInnovationZone: vi.fn(),
}));
const device = vi.hoisted(() => ({ mobile: false }));

vi.mock('@/contexts/NavigationContext', () => ({
  useNavigation: () => ({
    state: { activeTool: navigation.activeTool },
    setActiveTool: navigation.setActiveTool,
    goBack: navigation.goBack,
    navigateToInnovationZone: navigation.navigateToInnovationZone,
    navigateToModule: vi.fn(),
    navigateToStudySession: vi.fn(),
  }),
  useOptionalNavigation: () => null,
  useBackStep: () => {},
}));
vi.mock('@/hooks/useMobileAppDesign', () => ({ useMobileAppDesign: () => device.mobile }));
vi.mock('@/hooks/useTopicMastery', () => ({ useTopicMastery: () => ({ mastery: {} }) }));
vi.mock('@/components/gc/gcNotifications', () => ({ getNotifications: () => Promise.resolve([]) }));
// An open tool sits inside the shell's data provider; the bar and the shell are what is tested here.
vi.mock('@/contexts/InnovationDataContext', () => ({
  InnovationDataProvider: ({ children }: { children: React.ReactNode }) => children,
  useInnovationData: () => ({ topicMastery: { mastery: {} } }),
}));
// The tools themselves load lazily; the shell and its bar are what is tested here.
for (const path of ['WarRoom', 'CatchUpLane', 'YourPossibleLife', 'AcademicJourneyGame', 'HowTheyDidIt', 'ExaminersChair', 'PointsPassport', 'CollegeCompass', 'ComebackEngineV2']) {
  vi.doMock(`@/components/${path}`, () => ({ default: () => null }));
}

import InnovationZone from '@/components/InnovationZone';
import { ToolJumpCard } from '@/components/ModuleShared';
import { getLastVisit, recordVisit } from '@/components/lastVisited';
import { LEAVING_TOOL_IDS, isLeavingTool } from '@/components/launchpad/leavingTools';
import { createDevStudentProfile, createDevStudentSession } from '@/data/devStudent';

const LEAVING_TITLES = ['Catch-Up Lane', 'War Room', 'Your Possible Life', 'Academic Journey Simulator'];
const TODAY_ORDER = [
  'Coursework Studio', 'Planner & Study', 'Paper Trail', 'Future Finder', 'Mark Bank', 'Listening Studio',
  'Comeback Engine', 'Points Passport', 'College Compass', 'Topic Atlas', 'Command-Word Reflex', 'How They Did It',
];

function renderLaunchpad() {
  // A sixth-year senior: College Compass shows only to active senior years.
  const user = { ...createDevStudentSession(), yearGroup: '6th' as const, curriculumLevel: 'senior' as const };
  return render(
    <InnovationZone
      onBack={vi.fn()}
      user={user}
      initialSubjectProfile={createDevStudentProfile(new Date('2026-08-09T12:00:00.000Z'))}
      settings={{ language: 'en', avatar: '', darkMode: false, cardStyle: 'default', defaultWorkMinutes: 25 }}
      updateSetting={vi.fn()}
    />,
  );
}
const toolNames = () => within(screen.getByRole('list', { name: 'Tools' })).getAllByRole('heading', { level: 3 }).map(heading => heading.textContent);

beforeEach(() => { navigation.activeTool = null; device.mobile = false; vi.clearAllMocks(); localStorage.clear(); });
afterEach(() => cleanup());

describe('the Launchpad list', () => {
  test.each([false, true])('lists exactly twelve tools in today\'s order (phone design: %s)', mobile => {
    device.mobile = mobile;
    renderLaunchpad();
    expect(toolNames()).toEqual(TODAY_ORDER);
  });

  test('the categories menu filters as the tray did, and applies at once', async () => {
    renderLaunchpad();
    const menu = screen.getByRole('button', { name: /Launchpad categories/ });
    expect(menu).toHaveTextContent('All tools');
    fireEvent.click(menu);
    fireEvent.click(await screen.findByRole('menuitemradio', { name: 'Plan' }));
    expect(toolNames()).toEqual(['Planner & Study', 'Comeback Engine', 'College Compass']);
    fireEvent.click(screen.getByRole('button', { name: /Launchpad categories/ }));
    fireEvent.click(await screen.findByRole('menuitemradio', { name: 'Track' }));
    expect(toolNames()).toEqual(['Points Passport']);
    fireEvent.click(screen.getByRole('button', { name: /Launchpad categories/ }));
    fireEvent.click(await screen.findByRole('menuitemradio', { name: 'Practice' }));
    expect(toolNames()).toEqual(['Mark Bank', 'Listening Studio']);
  });

  test('on a phone, Practice also gathers the practice tools, as the tray did', async () => {
    device.mobile = true;
    renderLaunchpad();
    fireEvent.click(screen.getByRole('button', { name: /Launchpad categories/ }));
    fireEvent.click(await screen.findByRole('menuitemradio', { name: 'Practice' }));
    expect(toolNames()).toEqual(expect.arrayContaining(['Mark Bank', 'Listening Studio', 'Paper Trail']));
    expect(toolNames().some(name => LEAVING_TITLES.includes(name ?? ''))).toBe(false);
  });

  test('"How points work" says so in words and opens the points panel', () => {
    renderLaunchpad();
    const points = screen.getByRole('button', { name: 'How points work' });
    expect(points).toHaveAttribute('aria-expanded', 'false');
    fireEvent.click(points);
    expect(points).toHaveAttribute('aria-expanded', 'true');
    expect(screen.getByRole('region', { name: 'How points work' })).toBeInTheDocument();
  });

  test('on a laptop there is no "A place to start" and the card dealer stands beside the opening words', () => {
    renderLaunchpad();
    expect(screen.queryByText('A place to start')).not.toBeInTheDocument();
    expect(screen.queryByText('Your plan for today')).not.toBeInTheDocument();
    expect(document.querySelector('.lp7-intro .lp7-dealer')).toHaveAttribute('src', expect.stringContaining('card-dealer'));
  });
});

describe('the four tools that are leaving have no door', () => {
  test('not on the list, in any category or search', () => {
    renderLaunchpad();
    for (const title of LEAVING_TITLES) expect(screen.queryByRole('button', { name: `Open ${title}` })).not.toBeInTheDocument();
    for (const word of ['War Room', 'Catch-Up', 'Possible Life', 'Journey Simulator', 'syllabus']) {
      fireEvent.change(screen.getByRole('searchbox', { name: 'Find a tool or task' }), { target: { value: word } });
      for (const title of LEAVING_TITLES) expect(screen.queryByRole('button', { name: `Open ${title}` })).not.toBeInTheDocument();
    }
  });

  test('not in Meet the tools or Help me choose', () => {
    renderLaunchpad();
    fireEvent.click(screen.getByRole('button', { name: 'Meet the tools' }));
    const guide = within(screen.getByRole('list', { name: 'Tools in this guide' }));
    for (const title of LEAVING_TITLES) expect(guide.queryByText(title)).not.toBeInTheDocument();
    fireEvent.click(screen.getByRole('button', { name: 'Close Launchpad guide' }));
    fireEvent.click(screen.getByRole('button', { name: 'Help me choose' }));
    // Every goal, every answer: the recommendation is never a leaving tool.
    const goals = screen.getAllByRole('button').filter(button => button.closest('.ui-sheet-body') && button.classList.contains('ui-row'));
    expect(goals.length).toBeGreaterThan(0);
    for (let g = 0; g < goals.length; g += 1) {
      const goal = screen.getAllByRole('button').filter(button => button.closest('.ui-sheet-body') && button.classList.contains('ui-row'))[g];
      fireEvent.click(goal);
      const answers = screen.getAllByRole('button').filter(button => button.closest('.ui-sheet-body') && button.classList.contains('ui-row'));
      for (let a = 0; a < answers.length; a += 1) {
        const answer = screen.getAllByRole('button').filter(button => button.closest('.ui-sheet-body') && button.classList.contains('ui-row'))[a];
        fireEvent.click(answer);
        for (const title of LEAVING_TITLES) expect(screen.queryByRole('button', { name: `Open ${title}` })).not.toBeInTheDocument();
        fireEvent.click(screen.getByRole('button', { name: /Start again/ }));
        fireEvent.click(screen.getAllByRole('button').filter(button => button.closest('.ui-sheet-body') && button.classList.contains('ui-row'))[g]);
      }
      fireEvent.click(screen.getByRole('button', { name: /Back/ }));
    }
  });

  test('not on Home\'s "Pick up where you left off" (a visit saved before they left is skipped)', () => {
    for (const id of ['war-room', 'catch-up-lane', 'your-possible-life', 'journey']) {
      recordVisit('student-a', { kind: 'tool', id, label: id });
      expect(getLastVisit('student-a')).toBeNull();
    }
    recordVisit('student-a', { kind: 'tool', id: 'paper-trail', label: 'Paper Trail' });
    expect(getLastVisit('student-a')?.id).toBe('paper-trail');
  });

  test('not in a module: the shared tool card shows nothing for a leaving tool', () => {
    const { container } = render(<ToolJumpCard toolId="war-room" title="Map your syllabus in the War Room" description="…" ctaLabel="Open the War Room" />);
    expect(container).toBeEmptyDOMElement();
    render(<ToolJumpCard toolId="planner" title="Plan your week" description="…" />);
    expect(screen.getByText('Plan your week')).toBeInTheDocument();
  });

  test('not in the command palette, nor in Future Finder\'s "Explore career paths"', () => {
    const palette = readFileSync(join(process.cwd(), 'components/CommandPalette.tsx'), 'utf8');
    expect(palette).toMatch(/Object\.entries\(TOOL_TITLES\)\.filter\(\(\[id\]\) => !isLeavingTool\(id\)\)/);
    const shell = readFileSync(join(process.cwd(), 'components/InnovationZone.tsx'), 'utf8');
    expect(shell).not.toMatch(/onOpenCareerPaths=/);
    expect([...LEAVING_TOOL_IDS].sort()).toEqual(['career-paths', 'catch-up-lane', 'journey', 'syllabus-xray', 'war-room', 'your-possible-life']);
    expect(isLeavingTool('planner')).toBe(false);
  });

  test.each([
    ['war-room', 'War Room'],
    ['syllabus-xray', 'War Room · Subject Coverage'],
    ['catch-up-lane', 'Catch-Up Lane'],
    ['your-possible-life', 'Your Possible Life'],
    ['journey', 'Academic Journey Simulator'],
  ])('its own address still opens it: %s', (id, title) => {
    navigation.activeTool = id;
    renderLaunchpad();
    expect(document.querySelector(`main[data-tool="${id}"]`)).not.toBeNull();
    expect(screen.getByRole('heading', { level: 1, name: title })).toBeInTheDocument();
  });

  test('the old career-paths address still leads to Your Possible Life', () => {
    navigation.activeTool = 'career-paths';
    renderLaunchpad();
    expect(navigation.setActiveTool).toHaveBeenCalledWith('your-possible-life');
  });
});

describe('no black card when a tool opens', () => {
  test.each([false, true])('the shell draws no masthead and no first-visit card (phone design: %s)', mobile => {
    device.mobile = mobile;
    for (const id of ['how-they-did-it', 'examiners-chair', 'points-passport', 'college-compass', 'comeback']) {
      navigation.activeTool = id;
      const { unmount } = renderLaunchpad();
      expect(document.querySelector('.lp-masthead, .lp-first-introduction')).toBeNull();
      unmount();
    }
  });
});
