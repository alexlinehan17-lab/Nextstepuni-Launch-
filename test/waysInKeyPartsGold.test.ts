/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Ways In — the key parts against 220 hand-written breakdowns.
 *
 * Each gold card was broken down by hand, the way a teacher would: the job,
 * how many, what it is about, the limits and the material. The parser does
 * not have to match word for word — a teacher's "two advantages" and the
 * parser's "two" are both right — so a slot counts as found when one reading
 * contains the other or they share most of their words. The floors sit a
 * little under today's scores: a change that drops one is a change that
 * makes the breakdown worse for students, and should be looked at, not
 * waved through.
 */
/// <reference types="vite/client" />
import { describe, expect, test } from 'vitest';
import { buildKeyParts, type KeyPartsBreakdown } from '@/components/WaysIn/keyParts';
import { waysInSourceFromMarkBank } from '@/components/WaysIn/sources';
import gold from './fixtures/waysInKeyPartsGold.json';

interface GoldUnit { action?: string; count?: string; focus?: string; conditions?: string[]; use?: string[] }
interface GoldCard { id: string; notDecomposable?: string; units?: GoldUnit[] }

const decks = import.meta.glob('/components/MarkBank/cards/*/*.ts', { eager: true }) as Record<string, { CARDS?: readonly any[] }>;
const cards = new Map<string, { card: any; subject: string }>();
for (const [path, mod] of Object.entries(decks)) {
  for (const card of mod.CARDS ?? []) cards.set(card.id, { card, subject: path.split('/').at(-2) ?? '' });
}

const SLOTS = ['action', 'count', 'focus', 'conditions', 'use'] as const;
type Slot = typeof SLOTS[number];
const norm = (s: string) => s.replace(/\s+/g, ' ').replace(/[.,;:?!]+$/, '').trim().toLowerCase();
const words = (s: string) => new Set(s.split(/[^\p{L}\p{N}]+/u).filter(w => w.length > 2));
const close = (a: string, b: string) => {
  if (a === b || a.includes(b) || b.includes(a)) return true;
  const A = words(a);
  const B = words(b);
  if (!A.size || !B.size) return false;
  let shared = 0;
  for (const w of A) if (B.has(w)) shared += 1;
  return shared / (A.size + B.size - shared) >= 0.6;
};

function mine(kp: KeyPartsBreakdown, slot: Slot): Set<string> {
  const out = new Set<string>();
  for (const u of kp.units) {
    const value = slot === 'action' ? u.action : slot === 'count' ? u.count : slot === 'focus' ? u.focus : null;
    if (value) out.add(norm(value.display));
    if (slot === 'conditions') [...u.conditions, ...kp.cardRules].forEach(c => out.add(norm(c.display)));
    if (slot === 'use') u.use.forEach(x => out.add(norm(x.display)));
  }
  return out;
}

function theirs(units: GoldUnit[], slot: Slot): Set<string> {
  const out = new Set<string>();
  for (const u of units) {
    const value = u[slot];
    if (Array.isArray(value)) value.forEach(v => out.add(norm(v)));
    else if (value) out.add(norm(value));
  }
  return out;
}

const scored = (gold as GoldCard[]).filter(g => cards.has(g.id));
const found = { tp: {} as Record<Slot, number>, fp: {} as Record<Slot, number>, fn: {} as Record<Slot, number> };
for (const slot of SLOTS) { found.tp[slot] = 0; found.fp[slot] = 0; found.fn[slot] = 0; }
let modeAgree = 0;
for (const g of scored) {
  const { card, subject } = cards.get(g.id)!;
  const kp = buildKeyParts(waysInSourceFromMarkBank(card, subject));
  if (Boolean(g.notDecomposable) === (kp.mode !== 'decomposed')) modeAgree += 1;
  if (g.notDecomposable || !g.units) continue;
  for (const slot of SLOTS) {
    const ours = mine(kp, slot);
    const gold = theirs(g.units, slot);
    for (const x of ours) found[[...gold].some(y => close(y, x)) ? 'tp' : 'fp'][slot] += 1;
    for (const y of gold) if (![...ours].some(x => close(y, x))) found.fn[slot] += 1;
  }
}
const precision = (slot: Slot) => found.tp[slot] / Math.max(1, found.tp[slot] + found.fp[slot]);
const recall = (slot: Slot) => found.tp[slot] / Math.max(1, found.tp[slot] + found.fn[slot]);

describe('key parts against the hand-written gold set', () => {
  test('reads the gold cards from the live bank', () => {
    expect(scored.length).toBeGreaterThanOrEqual(210);
  });

  test('agrees on which questions can be broken down at all', () => {
    expect(modeAgree / scored.length).toBeGreaterThanOrEqual(0.93);
  });

  // [precision floor, recall floor] per slot.
  const FLOORS: Record<Slot, [number, number]> = {
    action: [0.94, 0.9],
    count: [0.86, 0.6],
    focus: [0.82, 0.74],
    conditions: [0.78, 0.4],
    use: [0.6, 0.5],
  };
  test.each(SLOTS)('finds the %s a teacher would', slot => {
    expect(precision(slot)).toBeGreaterThanOrEqual(FLOORS[slot][0]);
    expect(recall(slot)).toBeGreaterThanOrEqual(FLOORS[slot][1]);
  });
});
