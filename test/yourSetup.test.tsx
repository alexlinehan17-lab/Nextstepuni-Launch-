/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * "Your setup" reads back what a student entered in onboarding and routes each
 * section to the editor that already owns it.
 */
import React from 'react';
import { beforeEach, describe, expect, test, vi } from 'vitest';
import { fireEvent, render, screen } from '@testing-library/react';
import { summariseSetup } from '@/components/setup/yourSetupModel';
import YourSetupView from '@/components/setup/YourSetupView';
import NextStepUniSidebar from '@/components/navigation/NextStepUniSidebar';
import { MobileProfileSheet } from '@/components/UserProfileMenu';
import { NavigationProvider, useNavigation } from '@/contexts/NavigationContext';
import { createDemoStudentNorthStar, createDemoStudentProfile } from '@/data/devStudent';
import type { StudentSubjectProfile } from '@/components/subjectData';

vi.mock('@/components/GetPointsButton', () => ({ default: () => null }));
vi.mock('@/components/NotificationBell', () => ({ default: () => null }));

const TODAY = new Date('2026-10-14T12:00:00');

describe('summariseSetup', () => {
  test('reads a Leaving Cert profile back, with best-six points and the maths bonus', () => {
    const profile = createDemoStudentProfile(TODAY);
    const setup = summariseSetup(profile, createDemoStudentNorthStar(TODAY), '6th', TODAY);

    expect(setup.year).toEqual({ label: '6th Year', cycle: 'Leaving Cert' });
    expect(setup.exam).toMatchObject({ iso: '2027-06-09', label: '9 June 2027', daysAway: 238 });
    expect(setup.subjects.find(s => s.name === 'Mathematics')).toMatchObject({ level: 'Higher', current: 'H4', target: 'H2' });
    expect(setup.points).toEqual({ current: 465, target: 577, counted: 7 });
    expect(setup.week.find(d => d.day === 'Sunday')?.study).toBe(false);
    expect(setup.studyDays).toBe(6);
    expect(setup.blockMinutes).toBe(45);
    expect(setup.northStar?.title).toBe('Keep My Options Open');
    expect(setup.northStar?.vision.map(v => v.label)).toEqual(['Having Real Choices', 'Seeing the World', 'Freedom to Say No']);
  });

  test('shows LCA and Junior Cycle answers without inventing CAO points', () => {
    const lca: StudentSubjectProfile = { subjects: [{ subjectName: 'Mathematical Applications', level: 'common' }], examStartDate: null, restDays: [], yearGroup: 'LCA1', createdAt: '', updatedAt: '' };
    expect(summariseSetup(lca, null, 'LCA1', TODAY)).toMatchObject({ year: { label: 'LCA Year 1', cycle: 'Leaving Cert Applied' }, points: null, exam: null, studyDays: 7 });

    const jc: StudentSubjectProfile = { subjects: [{ subjectName: 'English', level: 'higher', currentBand: 'Merit', targetBand: 'Distinction' }], examStartDate: '2027-06-02', restDays: ['Saturday', 'Sunday'], yearGroup: '3rd', createdAt: '', updatedAt: '' };
    const junior = summariseSetup(jc, null, '3rd', TODAY);
    expect(junior.year?.cycle).toBe('Junior Cycle');
    expect(junior.subjects[0]).toMatchObject({ current: 'Merit', target: 'Distinction' });
    expect(junior.points).toBeNull();
    expect(junior.studyDays).toBe(5);
  });

  test('a student who skipped onboarding gets an empty summary, not an error', () => {
    expect(summariseSetup(null, null, undefined, TODAY)).toMatchObject({ year: null, exam: null, subjects: [], points: null, northStar: null, studyDays: 7 });
  });
});

describe('YourSetupView', () => {
  const handlers = () => ({
    onBack: vi.fn(), onFinishSetup: vi.fn(), onEditSubjects: vi.fn(), onEditNorthStar: vi.fn(),
    onOpenSettings: vi.fn(), onOpenPlanner: vi.fn(), onSetDarkMode: vi.fn(),
  });

  test('every section opens the editor that already owns it', () => {
    const h = handlers();
    render(<YourSetupView profile={createDemoStudentProfile(TODAY)} northStar={createDemoStudentNorthStar(TODAY)} yearGroup="6th" darkMode={false} {...h} />);

    fireEvent.click(screen.getByRole('button', { name: /Change year/ }));
    fireEvent.click(screen.getByRole('button', { name: /Edit North Star/ }));
    fireEvent.click(screen.getByRole('button', { name: /Change subjects/ }));
    fireEvent.click(screen.getByRole('button', { name: /Open Planner/ }));
    fireEvent.click(screen.getByRole('tab', { name: 'Dark' }));

    expect(h.onOpenSettings).toHaveBeenCalledOnce();
    expect(h.onEditNorthStar).toHaveBeenCalledOnce();
    expect(h.onEditSubjects).toHaveBeenCalledOnce();
    expect(h.onOpenPlanner).toHaveBeenCalledOnce();
    expect(h.onSetDarkMode).toHaveBeenCalledWith(true);
    expect(screen.getByText('465')).toBeInTheDocument();
    expect(screen.getByText('577')).toBeInTheDocument();
  });

  test('a student who skipped onboarding is offered a way to finish it', () => {
    const h = handlers();
    render(<YourSetupView profile={null} northStar={null} darkMode={false} {...h} />);

    fireEvent.click(screen.getByRole('button', { name: /Finish setting up/ }));
    expect(h.onFinishSetup).toHaveBeenCalledOnce();
    expect(screen.queryByRole('button', { name: /Change subjects/ })).not.toBeInTheDocument();
    fireEvent.click(screen.getByRole('button', { name: /Set North Star/ }));
    expect(h.onEditNorthStar).toHaveBeenCalledOnce();
  });
});

describe('getting to Your setup', () => {
  beforeEach(() => {
    localStorage.clear();
    window.scrollTo = vi.fn();
    window.history.replaceState(null, '', '/');
  });

  const Location = () => <output aria-label="Current app view">{useNavigation().state.viewState}</output>;
  const noop = vi.fn();

  test('the sidebar button opens it and shows it as the current page', () => {
    render(<NavigationProvider><Location /><NextStepUniSidebar
      user={{ uid: 'setup-nav-test', name: 'Demo Student', avatar: '' }}
      settings={{ darkMode: false } as never} updateSetting={noop} onLogout={noop}
      onOpenSettings={noop} onOpenPassport={noop} onOpenSiteGuide={noop}
      onOpenFeedback={noop} onUnreadCountChange={noop} completedCount={0}
      totalCount={0} unreadCount={0}
    ><div /></NextStepUniSidebar></NavigationProvider>);

    const button = screen.getByRole('button', { name: 'Your setup' });
    expect(button).not.toHaveAttribute('aria-current');
    fireEvent.click(button);

    expect(screen.getByLabelText('Current app view')).toHaveTextContent('your-setup');
    expect(window.location.search).toContain('view=your-setup');
    expect(screen.getByRole('button', { name: 'Your setup' })).toHaveAttribute('aria-current', 'page');
  });

  test('a deep link restores it', () => {
    window.history.replaceState(null, '', '/?view=your-setup');
    render(<NavigationProvider><Location /></NavigationProvider>);
    expect(screen.getByLabelText('Current app view')).toHaveTextContent('your-setup');
  });

  test('the phone and iPad profile sheet links to it', () => {
    const goToYourSetup = vi.fn();
    const close = vi.fn();
    render(<MobileProfileSheet isOpen onClose={close} user={{ uid: 'u', name: 'Demo Student', avatar: '' } as never}
      onLogout={noop} settings={{ darkMode: false } as never} updateSetting={noop} onOpenSettings={noop} avatarOverride=""
      streak={{ currentStreak: 0, longestStreak: 0, lastActiveDate: '' }} recommendation={null} onSelectModule={noop}
      onOpenPassport={noop} onGoToDashboard={noop} onGoToInsights={noop} onGoToReferences={noop} onGoToYearPlans={noop}
      onGoToYourSetup={goToYourSetup} onOpenSiteGuide={noop} onOpenFeedback={noop} completedCount={0} totalCount={0}
      onOpenNorthStar={noop} hasNorthStar unlockedThemes={[]} />);

    fireEvent.click(screen.getByRole('button', { name: 'Your setup' }));
    expect(close).toHaveBeenCalled();
    expect(goToYourSetup).toHaveBeenCalledOnce();
  });
});
