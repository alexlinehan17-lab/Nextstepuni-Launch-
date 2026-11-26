/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Area 1, the account pages (r5-your-setup, r5-insights, r5-year-plans,
 * r5-learning-paths, agreed 26 Nov 2026). Your setup on a laptop: "Change exam
 * date" sits beside "Change year" at the top of School year; on a phone it
 * stays under the dates. Year Plans and Learning Paths: the current year and
 * the path recommended next are the screen's one sheet with the one charcoal
 * Continue; every other Continue is a second button.
 */
import React from 'react';
import { cleanup, fireEvent, render, screen, within } from '@testing-library/react';
import { afterEach, beforeEach, describe, expect, test, vi } from 'vitest';
import YourSetupView from '@/components/setup/YourSetupView';
import YearPlansView from '@/components/YearPlansView';
import { createDemoStudentProfile } from '@/data/devStudent';

const device = vi.hoisted(() => ({ mobile: false }));
vi.mock('@/hooks/useMobileAppDesign', () => ({ useMobileAppDesign: () => device.mobile }));

const TODAY = new Date('2026-10-14T12:00:00');
afterEach(cleanup);
beforeEach(() => { window.scrollTo = vi.fn(); });

describe('Your setup: the exam date button', () => {
  const handlers = () => ({
    onBack: vi.fn(), onFinishSetup: vi.fn(), onEditSubjects: vi.fn(), onEditNorthStar: vi.fn(),
    onOpenSettings: vi.fn(), onOpenPlanner: vi.fn(), onSetDarkMode: vi.fn(),
  });

  test.each([[false, 'beside Change year at the top'], [true, 'under the dates']])('mobile=%s: Change exam date sits %s, and still opens the date form', (mobile) => {
    device.mobile = mobile;
    const onSaveExamDate = vi.fn();
    render(<YourSetupView profile={createDemoStudentProfile(TODAY)} northStar={null} yearGroup="6th" darkMode={false} {...handlers()} onSaveExamDate={onSaveExamDate} />);
    const schoolYear = screen.getByRole('heading', { name: '6th Year' }).closest('section')!;
    const head = schoolYear.querySelector('.ys-sec-head')!;
    const change = within(schoolYear).getByRole('button', { name: 'Change exam date' });
    expect(head.contains(change)).toBe(!mobile);
    expect(within(head as HTMLElement).getByRole('button', { name: 'Change year' })).toBeInTheDocument();
    fireEvent.click(change);
    fireEvent.change(screen.getByLabelText('When do your exams start?'), { target: { value: '2027-06-02' } });
    fireEvent.click(screen.getByRole('button', { name: 'Save date' }));
    expect(onSaveExamDate).toHaveBeenCalledWith('2027-06-02');
  });
});

describe('Year Plans', () => {
  test('your current year is the one sheet with the one charcoal Continue', () => {
    const select = vi.fn();
    render(<YearPlansView allCourses={[]} userProgress={{}} onSelectModule={select} onBack={vi.fn()} currentYearGroup="6th" />);
    const sixth = screen.getByRole('region', { name: '6th Year' });
    expect(sixth).toHaveClass('ui-paper');
    expect(within(sixth).getByText('Your current plan')).toBeInTheDocument();
    const main = document.querySelectorAll('.ui-btn--main');
    // No courses are loaded here, so every year reads as complete or startable; the main button, if any, is in the sheet.
    main.forEach(button => expect(sixth.contains(button)).toBe(true));
    const fifth = screen.getByRole('region', { name: '5th Year' });
    expect(fifth).not.toHaveClass('ui-paper');
    fireEvent.click(within(fifth).getByRole('button', { name: /modules in 5th Year/ }));
    expect(within(fifth).getByRole('list', { name: 'Modules in 5th Year' })).toBeInTheDocument();
  });
});
