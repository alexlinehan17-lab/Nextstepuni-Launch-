/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { createContext, useContext } from 'react';
import { type UserSettings } from '../types';

interface SettingsContextValue {
  settings: UserSettings;
  updateSetting: <K extends keyof UserSettings>(key: K, value: UserSettings[K]) => void;
  unlockedThemes: string[];
  unlockedCardStyles: string[];
}

export const SettingsContext = createContext<SettingsContextValue | null>(null);

export const useSettingsContext = () => useContext(SettingsContext);
