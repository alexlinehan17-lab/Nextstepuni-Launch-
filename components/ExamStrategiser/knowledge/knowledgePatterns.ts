/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Knowledge tab — cross-module pattern persistence.
 *
 * A small localStorage helper that lets each module write a pattern
 * signal at the end of a session. The Necessary Knowledge landing
 * surfaces these signals on a "Your patterns" panel — the payoff for
 * personalising closing screens across modules.
 *
 * Storage key: `nk:patterns:v1`. Latest-write-wins per module — we keep
 * the most recent observation, not a history. The shape is versioned so
 * future migrations can ignore stale data cleanly.
 */

const KEY = 'nk:patterns:v1';

export interface SanityCheckPattern {
  /** The check the student missed most often. */
  weakestCheck: 'order-of-magnitude' | 'units' | 'sign' | 'substitute-back';
  /** Per-check accuracy 0..1 — useful for weighted summaries. */
  accuracyByCheck: Record<string, number>;
  sampleSize: number;
  updatedAt: number;
}

export interface SpotTrapPattern {
  /** The trap category the student missed most often. */
  weakestCategory: string;
  accuracyByCategory: Record<string, number>;
  sampleSize: number;
  updatedAt: number;
}

export interface ComparativePattern {
  /** Average integration ratio across selected points (0..100). */
  avgIntegrationRatio: number;
  sampleSize: number;
  updatedAt: number;
}

export interface CeilingPattern {
  /** Number of cap-rule scenarios the student has viewed. */
  scenariosViewed: number;
  updatedAt: number;
}

export interface PatternSignals {
  sanityCheck?: SanityCheckPattern;
  spotTrap?: SpotTrapPattern;
  comparative?: ComparativePattern;
  ceiling?: CeilingPattern;
}

/** Read all stored pattern signals. Returns an empty object if storage
 *  is unavailable, empty, or corrupt. */
export function readPatterns(): PatternSignals {
  if (typeof window === 'undefined') return {};
  try {
    const raw = window.localStorage.getItem(KEY);
    if (!raw) return {};
    const parsed = JSON.parse(raw);
    if (typeof parsed !== 'object' || parsed === null) return {};
    return parsed as PatternSignals;
  } catch {
    return {};
  }
}

/** Write a single pattern signal. Reads + merges + writes. Silent on
 *  storage failure. */
export function writePattern<K extends keyof PatternSignals>(
  key: K,
  value: NonNullable<PatternSignals[K]>,
): void {
  if (typeof window === 'undefined') return;
  try {
    const current = readPatterns();
    const next: PatternSignals = { ...current, [key]: value };
    window.localStorage.setItem(KEY, JSON.stringify(next));
  } catch {
    // Storage may be full or disabled — silently fail.
  }
}

/** Clear all stored patterns. Used by the "reset patterns" affordance
 *  on the landing panel. */
export function clearPatterns(): void {
  if (typeof window === 'undefined') return;
  try {
    window.localStorage.removeItem(KEY);
  } catch {
    // ignore
  }
}
