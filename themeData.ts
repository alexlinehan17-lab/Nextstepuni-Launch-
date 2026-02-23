/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { type AccentThemeId, type CardStyleId } from './types';

export interface AccentTheme {
  id: AccentThemeId;
  name: string;
  hex: string;
  darkHex: string;
  rgb: string;
  darkRgb: string;
  price: number;
}

export interface CardStyleMeta {
  id: CardStyleId;
  name: string;
  description: string;
  price: number;
}

export const ACCENT_THEMES: Record<AccentThemeId, AccentTheme> = {
  terracotta: { id: 'terracotta', name: 'Terracotta', hex: '#CC785C', darkHex: '#B56A50', rgb: '204, 120, 92', darkRgb: '181, 106, 80', price: 0 },
  ocean: { id: 'ocean', name: 'Ocean Depth', hex: '#4A7C8B', darkHex: '#3D6873', rgb: '74, 124, 139', darkRgb: '61, 104, 115', price: 0 },
  sage: { id: 'sage', name: 'Sage & Stone', hex: '#6B8F71', darkHex: '#5A7A5F', rgb: '107, 143, 113', darkRgb: '90, 122, 95', price: 0 },
  midnight: { id: 'midnight', name: 'Midnight Ink', hex: '#5B6ABF', darkHex: '#4D5AA3', rgb: '91, 106, 191', darkRgb: '77, 90, 163', price: 0 },
  'dusk-rose': { id: 'dusk-rose', name: 'Dusk Rose', hex: '#B06B7D', darkHex: '#965A6A', rgb: '176, 107, 125', darkRgb: '150, 90, 106', price: 0 },
  golden: { id: 'golden', name: 'Golden Hour', hex: '#C49A3C', darkHex: '#A88332', rgb: '196, 154, 60', darkRgb: '168, 131, 50', price: 0 },
  arctic: { id: 'arctic', name: 'Arctic Slate', hex: '#6B7D8D', darkHex: '#5A6A78', rgb: '107, 125, 141', darkRgb: '90, 106, 120', price: 0 },
  obsidian: { id: 'obsidian', name: 'Obsidian', hex: '#8B7D6B', darkHex: '#766A5A', rgb: '139, 125, 107', darkRgb: '118, 106, 90', price: 0 },
};

export const ACCENT_THEME_LIST: AccentTheme[] = Object.values(ACCENT_THEMES);

export const CARD_STYLES: CardStyleMeta[] = [
  { id: 'default', name: 'Default', description: 'Clean and minimal card style', price: 0 },
  { id: 'glass', name: 'Glass', description: 'Frosted glass with blur effect', price: 0 },
  { id: 'neon', name: 'Neon', description: 'Dark with glowing accent borders', price: 0 },
  { id: 'flat', name: 'Flat', description: 'Bold borders, zero shadows', price: 0 },
  { id: 'gradient', name: 'Gradient', description: 'Subtle accent gradient background', price: 0 },
];
