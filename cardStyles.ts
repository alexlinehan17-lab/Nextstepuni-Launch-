/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { type CardStyleId } from './types';

const CARD_CLASS_MAP: Record<CardStyleId, string> = {
  default: 'bg-white dark:bg-zinc-900 border border-zinc-200 dark:border-zinc-800 rounded-2xl shadow-sm',
  glass: 'bg-white/60 dark:bg-zinc-900/60 backdrop-blur-xl border border-white/20 dark:border-white/10 rounded-2xl shadow-lg',
  neon: 'bg-zinc-950 dark:bg-zinc-950 border border-[rgba(var(--accent),0.4)] rounded-2xl shadow-[0_0_15px_rgba(var(--accent),0.15)]',
  flat: 'bg-white dark:bg-zinc-900 border-2 border-zinc-200 dark:border-zinc-700 rounded-xl shadow-none',
  gradient: 'bg-gradient-to-br from-white to-[rgba(var(--accent),0.05)] dark:from-zinc-900 dark:to-[rgba(var(--accent),0.08)] border border-zinc-200 dark:border-zinc-800 rounded-2xl shadow-sm',
};

export function getCardClasses(style: CardStyleId): string {
  return CARD_CLASS_MAP[style] || CARD_CLASS_MAP.default;
}
