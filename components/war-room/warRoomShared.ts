/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React from 'react';
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

// ── Design System ──────────────────────────────────────────

export const CARD_STYLE: React.CSSProperties = {
  borderRadius: 14,
  boxShadow: '0 1px 3px rgba(28,25,23,0.04)',
};

export const CARD_CLASS = 'bg-[#FEFDFB] dark:bg-zinc-900 border border-[#EDEBE8] dark:border-zinc-800';

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
