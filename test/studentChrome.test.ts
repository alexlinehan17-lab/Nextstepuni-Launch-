/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */
import { describe, expect, test } from 'vitest';

import { shouldShowStudentChrome } from '@/utils/studentChrome';

describe('student chrome visibility', () => {
  test('keeps module and onboarding views focused', () => {
    expect(shouldShowStudentChrome('module')).toBe(false);
    expect(shouldShowStudentChrome('onboarding')).toBe(false);
  });

  test('shows global student controls on normal app views', () => {
    expect(shouldShowStudentChrome('tree')).toBe(true);
    expect(shouldShowStudentChrome('study-session')).toBe(true);
  });
});
