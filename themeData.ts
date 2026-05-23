/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { type CardStyleId } from './types';

// Accent theme picker removed as part of the teal→orange brand pivot —
// `--accent` CSS variables now come solely from index.html and never
// change at runtime. CARD_STYLES below is unrelated and still in use.

export interface CardStyleMeta {
  id: CardStyleId;
  name: string;
  description: string;
  price: number;
}

export const CARD_STYLES: CardStyleMeta[] = [
  { id: 'default', name: 'Default', description: 'Clean and minimal card style', price: 0 },
  { id: 'glass', name: 'Glass', description: 'Frosted glass with blur effect', price: 0 },
  { id: 'neon', name: 'Neon', description: 'Dark with glowing accent borders', price: 0 },
  { id: 'flat', name: 'Flat', description: 'Bold borders, zero shadows', price: 0 },
  { id: 'gradient', name: 'Gradient', description: 'Subtle accent gradient background', price: 0 },
];
