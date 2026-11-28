/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * What the reading frame tells the pieces inside a module (area 5 of the design build), and what
 * the app tells the finishing screen. No heavy imports: the app shell provides ModuleFinish.
 */
import { createContext } from 'react';
import type { CourseData } from '../Library';

/** The step being read: "Step 4 of 5" over a step's headline (ReadingSection). */
export const ReaderStepContext = createContext<{ index: number; total: number; name?: string } | null>(null);

/** The module's world as the finishing screen shows it: the next module, one tap away. */
export interface ModuleFinish {
  /** The module's world (a CategoryType id). */
  category: string;
  /** Modules finished in the world, counted from progress, and how many it has. */
  done: number;
  total: number;
  /** The next module in the world still to read, with its number in the world. */
  next: { course: CourseData; number: number } | null;
  openModule: (id: string) => void;
}
export const ModuleFinishContext = createContext<ModuleFinish | null>(null);
