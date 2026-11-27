/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The small pieces every part of the counsellor's dashboard draws the same way (area 8a): the
 * width it is laid out for, a status said in words with its ink mark, a figure whose unit hangs
 * past the digits, a student's character standing bare. How things are SHOWN only: nothing here
 * reads, counts or writes anything.
 */
import React, { useSyncExternalStore, type ReactNode } from 'react';
import Avatar from '../Avatar';
import { type StudentStatus } from './gcTypes';
import './gc-8a.css';

/** True from this width up (the laptop layout beside the staff sidebar starts at 768px, as today). */
export function useWide(minWidth = 768): boolean {
  const query = `(min-width: ${minWidth}px)`;
  return useSyncExternalStore(
    update => {
      if (typeof window === 'undefined' || typeof window.matchMedia !== 'function') return () => {};
      const list = window.matchMedia(query);
      list.addEventListener?.('change', update);
      return () => list.removeEventListener?.('change', update);
    },
    () => (typeof window !== 'undefined' && typeof window.matchMedia === 'function' ? window.matchMedia(query).matches : false),
    () => false,
  );
}

/** Each status in words (the status guide's own names), and the mark that repeats it in shape. */
export const STATUS_WORDS: Record<StudentStatus, string> = {
  new: 'New',
  active: 'Active',
  thriving: 'Thriving',
  drifting: 'Drifting',
  'at-risk': 'At risk',
  inactive: 'Inactive',
};
const STATUS_MARK: Record<StudentStatus, string> = {
  new: 'gc8-dot gc8-dot--new',
  active: 'gc8-dot gc8-dot--active',
  thriving: 'gc8-dot gc8-dot--good',
  drifting: 'gc8-dot gc8-dot--ring',
  'at-risk': 'gc8-dot',
  inactive: 'gc8-dot gc8-dot--quiet',
};

export function StatusDot({ status }: { status: StudentStatus }) {
  return <i className={STATUS_MARK[status]} aria-hidden="true" />;
}

/** "● At risk": the mark and the word (the word in ink inside a quieter line). */
export function StatusWords({ status, children }: { status: StudentStatus; children?: ReactNode }) {
  return <span className="gc8-why"><StatusDot status={status} /><b>{STATUS_WORDS[status]}</b>{children}</span>;
}

/** A severity of an early warning: urgent is filled, watch a ring, nudge a grey ring. */
export function SeverityDot({ severity }: { severity: 'urgent' | 'watch' | 'nudge' }) {
  const cls = severity === 'urgent' ? 'gc8-dot' : severity === 'watch' ? 'gc8-dot gc8-dot--ring' : 'gc8-dot gc8-dot--new';
  return <i className={cls} aria-hidden="true" />;
}
export const SEVERITY_WORDS = { urgent: 'Urgent', watch: 'Watch', nudge: 'Nudge' } as const;

/** A figure with its unit hanging past the digits ("25%" ends where "28" ends). */
export function Fig({ value, unit, className = '' }: { value: ReactNode; unit?: string; className?: string }) {
  return <span className={className}>{value}{unit ? <small className="gc8-unit">{unit}</small> : null}</span>;
}

/** A percent in the readout mono, right-aligned, the % smaller and hanging. */
export function Pct({ value, className = '' }: { value: number; className?: string }) {
  return <span className={`gc8-readout gc8-pct ${className}`.trim()}>{Math.round(value)}<small className="gc8-unit">%</small></span>;
}

/** A student's character, bare: no tile, no circle (Alex, 25 Nov 2026). */
export function StudentArt({ seed, size = 40 }: { seed: string; size?: 28 | 32 | 40 | 56 }) {
  return <Avatar seed={seed} alt="" className={`gc8-art crew-illustration${size !== 40 ? ` gc8-art--${size}` : ''}`} />;
}

/** "In 3 days" style counts on rows: today's numbers, the board's plain words. */
export function daysWords(days: number): string {
  if (!Number.isFinite(days)) return 'No sessions';
  if (days <= 0) return 'Today';
  return days === 1 ? '1 day' : `${days} days`;
}
