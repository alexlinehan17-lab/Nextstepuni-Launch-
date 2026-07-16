/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import type React from 'react';
import type { YearGroup } from '../components/subjectData';

// ─── Curriculum level ───────────────────────────────────────
//
// Computed from the user's `yearGroup` (see `yearGroupToCurriculumLevel`
// below) but also stored explicitly on the user doc for fast O(1) gating
// without re-deriving it at every call site.
//
// Mapping rule (Phase 1):
//   1st / 2nd / 3rd  → junior
//   TY / 5th / 6th   → senior  (TY rides senior content for now;
//                                revisit post-launch per the audit).
//   graduated        → senior  (Phase 8 — graduates came from senior;
//                                this is just a label-flip post-LC and
//                                doesn't drive any active UI gating.)

export type CurriculumLevel = 'junior' | 'senior';

export function yearGroupToCurriculumLevel(yg: YearGroup): CurriculumLevel {
  return yg === '1st' || yg === '2nd' || yg === '3rd' ? 'junior' : 'senior';
}

/** Phase 8: convenience predicate. Used in places that want to gate
 *  forward-progression UI (e.g. the "I'm now in X" button) or recognise
 *  post-LC users for label tweaks without re-deriving from yearGroup. */
export function isGraduated(yg: YearGroup | undefined): boolean {
  return yg === 'graduated';
}

// ─── Active senior cycle ────────────────────────────────────
//
// The TRUE "4th/5th/6th year" set — active senior cycle EXCLUDING
// graduated. There is no '4th' token: Transition Year is 'TY'.
//
// NB: `yearGroupToCurriculumLevel('graduated')` is 'senior', so a plain
// `curriculum: 'senior'` gate LEAKS senior-only tools to graduated users.
// Tools that should disappear once a student has left school (e.g. the
// CAO/HEAR/DARE roadmap) must gate on this predicate instead. Undefined
// (legacy / partially-onboarded / GC / admin accounts) returns false.

export const ACTIVE_SENIOR_YEARS = ['TY', '5th', '6th'] as const;

export function isActiveSeniorYear(yg: YearGroup | undefined): boolean {
  return yg === 'TY' || yg === '5th' || yg === '6th';
}

// ─── Year progression ──────────────────────────────────────
//
// Phase 8: forward-only year progression. Used by Settings → School Year
// to render the "I'm now in X" button label and decide what transition
// flow to run.
//   - JC→JC (1st→2nd, 2nd→3rd) and senior→senior (TY→5th, 5th→6th) are
//     quiet bumps: write the new yearGroup, brief celebratory toast.
//   - 3rd→TY|5th crosses the curriculum boundary: triggers JC→senior
//     re-onboarding (TransitionToSenior wrapper).
//   - 6th→graduated is the terminal soft-state transition.

export type NextYearAction =
  | { kind: 'bump'; next: YearGroup; label: string }                // quiet bump
  | { kind: 'pick-senior'; label: string }                          // 3rd → TY or 5th picker
  | { kind: 'graduate'; label: string }                             // 6th → graduated
  | { kind: 'terminal'; label: string };                            // graduated — no further button

/** Resolve what the "I'm now in X" button should do for a given year. */
export function nextYearAction(yg: YearGroup | undefined): NextYearAction {
  switch (yg) {
    case '1st': return { kind: 'bump', next: '2nd', label: "I'm now in 2nd Year" };
    case '2nd': return { kind: 'bump', next: '3rd', label: "I'm now in 3rd Year" };
    case '3rd': return { kind: 'pick-senior', label: "I'm starting Senior Cycle" };
    case 'TY':  return { kind: 'bump', next: '5th', label: "I'm now in 5th Year" };
    case '5th': return { kind: 'bump', next: '6th', label: "I'm now in 6th Year" };
    case '6th': return { kind: 'graduate', label: 'Mark as graduated' };
    case 'graduated': return { kind: 'terminal', label: "Best of luck with what's next" };
    default: return { kind: 'terminal', label: '' }; // undefined — shouldn't reach UI
  }
}

/** Human-readable label for the current year (used in Settings header
 *  copy and the GC dashboard year cell). */
export function yearGroupLabel(yg: YearGroup | undefined): string {
  switch (yg) {
    case '1st': return '1st Year';
    case '2nd': return '2nd Year';
    case '3rd': return '3rd Year';
    case 'TY':  return 'Transition Year';
    case '5th': return '5th Year';
    case '6th': return '6th Year';
    case 'graduated': return 'Graduated';
    default: return '';
  }
}

// ─── Session User Type ──────────────────────────────────────

export type UserRole = 'student' | 'gc' | 'staff' | 'admin';

export type SessionUser = {
  uid: string;
  name: string;
  avatar: string;
  isAdmin?: boolean;
  role?: UserRole;
  school?: string;
  yearGroup?: YearGroup;
  curriculumLevel?: CurriculumLevel;
  needsPasswordChange?: boolean;
};

/**
 * School staff = guidance counsellors (`gc`) AND teaching staff (`staff`).
 * They have full parity on the Staff Dashboard (owner decision 2026-07-16;
 * see compliance/STAFF_DASHBOARD_PLAN.md), so every place that used to branch
 * on `role === 'gc'` for dashboard access should use this instead. `staff`
 * accounts are provisioned only via the `claimStaffAccess` Cloud Function
 * (server-side, per-school code), never self-assigned.
 */
export function isSchoolStaff(role?: string | null): boolean {
  return role === 'gc' || role === 'staff';
}

// ─── Avatar Seeds ───────────────────────────────────────────

export const AVATAR_SEEDS = [
  'Mary Baker', 'Harriet Tubman', 'Ma Rainey', 'Maud Nathan',
  'Annie Jump', 'Felisa Rincon', 'Maya Angelou', 'Elizabeth Peratrovich',
];

// ─── Avatar Helpers ─────────────────────────────────────────

/** Build avatar URL — DiceBear Notionists Neutral with improved background colors. */
export function getAvatarUrl(seed: string): string {
  return `https://api.dicebear.com/9.x/notionists-neutral/svg?seed=${encodeURIComponent(seed)}&backgroundColor=d1e8d5,c4d5f2,f2d5c4,d5c4f2,f2e6c4,c4e8f2,f2c4d1,e8e4d1`;
}

/** Fallback avatar as a data URI — initials on a coloured circle. Used when DiceBear fails (e.g. offline). */
export function getAvatarFallback(seed: string): string {
  const initial = (seed.charAt(0) || '?').toUpperCase();
  const colors = ['#2A7D6F', '#E84393', '#0984E3', '#E67E22', '#6C5CE7', '#00B894', '#D63031', '#FDCB6E'];
  let hash = 0;
  for (let i = 0; i < seed.length; i++) hash = seed.charCodeAt(i) + ((hash << 5) - hash);
  const bg = colors[Math.abs(hash) % colors.length];
  const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="64" height="64" viewBox="0 0 64 64"><circle cx="32" cy="32" r="32" fill="${bg}"/><text x="32" y="32" dy=".35em" text-anchor="middle" fill="#fff" font-family="DM Sans,sans-serif" font-size="28" font-weight="700">${initial}</text></svg>`;
  return `data:image/svg+xml,${encodeURIComponent(svg)}`;
}

/** onError handler for avatar <img> tags — swaps to initials fallback */
export function handleAvatarError(e: React.SyntheticEvent<HTMLImageElement>, seed: string) {
  const img = e.currentTarget;
  const fallback = getAvatarFallback(seed);
  if (img.src !== fallback) {
    img.src = fallback;
  }
}
