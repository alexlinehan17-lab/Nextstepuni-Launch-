/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import type React from 'react';
import { type Grade, getPointsForGrade, LC_SUBJECTS } from '../subjectData';
import { type StudentSubjectProfile } from '../subjectData';

// ── Types ──────────────────────────────────────────────────

export interface TopicEntry {
  id: string;
  name: string;
  confidence: 'solid' | 'shaky' | 'not-started';
  updatedAt: number;
}

export type TopicMap = Record<string, TopicEntry[]>;

export interface MockResult {
  id: string;
  subject: string;
  grade: string;
  date: string;
  label?: string;
  timestamp: number;
}

// ── Editorial Design Tokens ────────────────────────────────
// Shared across the War Room redesign and the Academic Journey.
// Warm cream paper + charcoal ink + restrained orange accent.

export const PAPER = '#F6F1E6';        // primary cream surface
export const PAPER_DEEP = '#EFE7D5';   // deeper cream for grouped sections
export const PAPER_SOFT = '#FBF7EC';   // softest cream for nested cards
export const INK = '#1F1B17';          // charcoal headlines
export const INK_SOFT = '#5C544A';     // body text
export const INK_MUTE = '#8E8378';     // labels, secondary text
export const INK_FAINT = '#C4BEB3';    // dividers, disabled, faint axes
export const ACCENT = '#CC785C';       // restrained orange
export const ACCENT_DARK = '#B56A50';

// Status palette — muted, not neon
export const STATUS_SOLID = '#5E8B7E';      // sage
export const STATUS_SOLID_DEEP = '#3F6A5E';
export const STATUS_SOLID_TINT = '#E8EDE6';
export const STATUS_SHAKY = '#B8843D';      // ochre
export const STATUS_SHAKY_DEEP = '#8C6022';
export const STATUS_SHAKY_TINT = '#F1E6CD';
export const STATUS_GAP = '#B86F5A';        // terracotta
export const STATUS_GAP_DEEP = '#8C4D3B';
export const STATUS_GAP_TINT = '#F0DACD';
export const STATUS_NEUTRAL = '#C4BEB3';    // faint stone for not-started

// Reusable card surface — soft cream paper with thin charcoal border + faint shadow
export const CARD_STYLE: React.CSSProperties = {
  borderRadius: 14,
  background: PAPER_SOFT,
  border: `1px solid ${INK}1A`,
  boxShadow: '0 1px 0 rgba(31,27,23,0.04), 0 8px 22px rgba(31,27,23,0.05)',
};

// Tailwind class wrapper for backwards compatibility (used in existing JSX with className+style)
export const CARD_CLASS = '';

// ── Confidence semantics ───────────────────────────────────

export const CONFIDENCE_COLORS = {
  'solid': 'bg-emerald-500',
  'shaky': 'bg-amber-400',
  'not-started': 'bg-zinc-300',
} as const;

export const CONFIDENCE_TEXT_COLORS = {
  'solid': 'text-emerald-700',
  'shaky': 'text-amber-700',
  'not-started': 'text-zinc-500',
} as const;

export const CONFIDENCE_HEX: Record<TopicEntry['confidence'], { fill: string; deep: string; tint: string }> = {
  'solid':       { fill: STATUS_SOLID, deep: STATUS_SOLID_DEEP, tint: STATUS_SOLID_TINT },
  'shaky':       { fill: STATUS_SHAKY, deep: STATUS_SHAKY_DEEP, tint: STATUS_SHAKY_TINT },
  'not-started': { fill: STATUS_NEUTRAL, deep: INK_MUTE,        tint: '#EFEAE0' },
};

export const CONFIDENCE_LABELS: Record<string, string> = {
  'solid': 'Solid',
  'shaky': 'Shaky',
  'not-started': 'Not Started',
};

export const CONFIDENCE_CYCLE: Record<string, TopicEntry['confidence']> = {
  'not-started': 'shaky',
  'shaky': 'solid',
  'solid': 'not-started',
};

// ── Helpers ────────────────────────────────────────────────

export function genId(): string {
  return Math.random().toString(36).substring(2, 10) + Date.now().toString(36);
}

export function gradeToPoints(grade: string | undefined | null): number {
  if (!grade || typeof grade !== 'string') return 0;
  if (grade.startsWith('H')) return getPointsForGrade(grade as Grade, false);
  if (grade.startsWith('O')) return getPointsForGrade(grade as Grade, false);
  return 0;
}

export function computeCurrentTotal(subjects: StudentSubjectProfile['subjects']): number {
  const all = subjects.map(s => {
    const isMaths = LC_SUBJECTS.find(lc => lc.name === s.subjectName)?.isMaths ?? false;
    return getPointsForGrade(s.currentGrade as Grade, isMaths);
  }).sort((a, b) => b - a);
  return all.slice(0, 6).reduce((sum, p) => sum + p, 0);
}

// Mute a subject hex so chart/table colours feel curated, not loud.
// Blends the source hex toward warm paper at the given strength.
export function mutedSubjectHex(hex: string, blend: number = 0.18): string {
  // blend = 0 → original colour; 1 → paper. Default lifts ~18% toward cream.
  const n = (h: string) => parseInt(h, 16);
  const m = hex.replace('#', '');
  const r = n(m.slice(0, 2));
  const g = n(m.slice(2, 4));
  const b = n(m.slice(4, 6));
  const pr = 0xF6, pg = 0xF1, pb = 0xE6;
  const mix = (a: number, p: number) => Math.round(a * (1 - blend) + p * blend);
  const toHex = (x: number) => x.toString(16).padStart(2, '0');
  return `#${toHex(mix(r, pr))}${toHex(mix(g, pg))}${toHex(mix(b, pb))}`;
}
