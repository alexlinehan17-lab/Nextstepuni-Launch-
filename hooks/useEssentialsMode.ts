/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { useSettings } from './useSettings';
import { useAuth } from '../contexts/AuthContext';

/**
 * Returns true if the current user has selected "Essentials" mode.
 * Essentials mode shows simplified, shorter module content with
 * all interactive elements preserved.
 */
export function useEssentialsMode(): boolean {
  const { user } = useAuth();
  const { settings } = useSettings(user?.uid);
  return settings?.essentialsMode === true;
}
