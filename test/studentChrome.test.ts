/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */
import { describe, expect, test } from 'vitest';

import { shouldShowStudentChrome, shouldShowStudentSidebar } from '@/utils/studentChrome';

describe('student chrome visibility', () => {
  test('keeps module and onboarding views focused', () => {
    expect(shouldShowStudentChrome('module')).toBe(false);
    expect(shouldShowStudentChrome('onboarding')).toBe(false);
  });

  test('shows global student controls on normal app views', () => {
    expect(shouldShowStudentChrome('tree')).toBe(true);
    expect(shouldShowStudentChrome('study-session')).toBe(true);
  });

  test('sidebar B stays beside a module on a laptop (area 5), and still steps aside for onboarding', () => {
    expect(shouldShowStudentSidebar('module')).toBe(true);
    expect(shouldShowStudentSidebar('tree')).toBe(true);
    expect(shouldShowStudentSidebar('onboarding')).toBe(false);
  });
});
