/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */
import React from 'react';
import { fireEvent, render, screen } from '@testing-library/react';
import { describe, expect, test, vi } from 'vitest';
import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';

import AchievementToast from '@/components/AchievementToast';
import { ACHIEVEMENTS, getAchievementsForCurriculum } from '@/achievementData';
import { ALL_COURSES } from '@/courseData';
import { POINTS } from '@/journeyPointsConfig';
import { type AchievementDefinition, type GamificationState } from '@/gamificationConfig';

describe('Journey Points rebalance', () => {
  test('keeps passive module completion below a normal study session', () => {
    const modulePayouts = ALL_COURSES.map(course => (
      (course.sectionsCount * POINTS.SECTION_COMPLETE) + POINTS.MODULE_COMPLETE_BONUS
    ));

    expect(POINTS.SECTION_COMPLETE).toBe(2);
    expect(POINTS.MODULE_COMPLETE_BONUS).toBe(6);
    expect(POINTS.CATEGORY_COMPLETE_BONUS).toBe(20);
    expect(Math.max(...modulePayouts)).toBeLessThan(30);
  });

  test('keeps achievement currency secondary to the achievement itself', () => {
    expect(ACHIEVEMENTS.find(item => item.id === 'first-step')?.bonusPoints).toBe(2);
    expect(ACHIEVEMENTS.find(item => item.id === 'first-module')?.bonusPoints).toBe(5);
    expect(Math.max(...ACHIEVEMENTS.map(item => item.bonusPoints))).toBeLessThanOrEqual(60);
  });

  test('spaces the early section milestones beyond a single typical module', () => {
    const gettingStarted = ACHIEVEMENTS.find(item => item.id === 'getting-started');
    expect(gettingStarted?.condition({ sectionsCompleted: 9 } as GamificationState)).toBe(false);
    expect(gettingStarted?.condition({ sectionsCompleted: 10 } as GamificationState)).toBe(true);
  });
});

describe('curriculum-scoped achievements', () => {
  test('never offers both Senior and Junior Cycle copies to one student', () => {
    const seniorIds = new Set(getAchievementsForCurriculum('senior').map(item => item.id));
    const juniorIds = new Set(getAchievementsForCurriculum('junior').map(item => item.id));

    expect(seniorIds.has('first-step')).toBe(true);
    expect(seniorIds.has('jc-first-step')).toBe(false);
    expect(juniorIds.has('first-step')).toBe(false);
    expect(juniorIds.has('jc-first-step')).toBe(true);
  });

  test('applies the curriculum filter at the award boundary', () => {
    const hookSource = readFileSync(resolve(__dirname, '../hooks/useGamification.ts'), 'utf8');
    expect(hookSource).toContain('getAchievementsForCurriculum(curriculumLevel)');
  });
});

describe('achievement notification', () => {
  test('uses the quiet white ledger treatment and remains dismissible', () => {
    const onDismiss = vi.fn();
    const achievement: AchievementDefinition = {
      id: 'first-module',
      title: 'Module Master',
      description: 'Complete your first full module',
      category: 'modules',
      icon: 'BookCheck',
      condition: () => true,
      bonusPoints: 5,
      isHidden: false,
    };

    render(<AchievementToast achievement={achievement} onDismiss={onDismiss} />);

    expect(screen.getByRole('status')).toHaveTextContent('Achievement unlocked');
    expect(screen.getByText('Module Master')).toBeInTheDocument();
    expect(screen.getByText('+5 JP')).toBeInTheDocument();

    const dismiss = screen.getByRole('button', { name: 'Dismiss achievement: Module Master' });
    expect(dismiss).toHaveClass('bg-white');
    fireEvent.click(dismiss);
    expect(onDismiss).toHaveBeenCalledOnce();
  });
});
