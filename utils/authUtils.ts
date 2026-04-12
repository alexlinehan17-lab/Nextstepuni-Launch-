/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import type React from 'react';

// ─── Session User Type ──────────────────────────────────────

export type SessionUser = {
  uid: string;
  name: string;
  avatar: string;
  isAdmin?: boolean;
  role?: 'student' | 'gc' | 'admin';
  school?: string;
  yearGroup?: '5th' | '6th';
  needsPasswordChange?: boolean;
};

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
