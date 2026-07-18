/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { useSettings } from './useSettings';
import { useAuth } from '../contexts/AuthContext';

/**
 * Returns true if module content should render in "Essentials" mode:
 * simplified, shorter prose with all interactive elements preserved.
 *
 * Junior Cycle students (1st–3rd year, ages ~12–15) ALWAYS get Essentials —
 * the content complexity audit (2026-07) found the full-register prose in the
 * shared `curriculum: 'both'` modules reads harder than the senior-only
 * baseline, i.e. 1st years were being shown harder text than Leaving Cert
 * students. Auto-enabling Essentials for junior cycle keeps their reading level
 * below the senior register by construction. Senior students keep the opt-in
 * toggle.
 */
export function useEssentialsMode(): boolean {
  const { user } = useAuth();
  const { settings } = useSettings(user?.uid);
  if (user?.curriculumLevel === 'junior') return true;
  return settings?.essentialsMode === true;
}
