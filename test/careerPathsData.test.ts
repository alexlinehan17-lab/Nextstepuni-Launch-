/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Data-integrity guards for the Career Paths deck — the regression net for the
 * 2026 expansion (12 → 27 careers). Catches a future card that links to no
 * course, a typo'd iconKey, a duplicate id, an inverted salary band, or a
 * half-filled card before it reaches students.
 */
import { describe, test, expect } from 'vitest';
import { CAREERS } from '@/careerPathsData';
import { CAO_COURSES } from '@/components/futureFinderData';
import { FIELD_WORLD, FIELD_ICON, CAREER_ICONS, careerIcon } from '@/components/immersiveDeck/deckGlyphs';

describe('Career Paths data integrity', () => {
  test('every career links to at least one CAO course (matchStrings ∩ careerPaths)', () => {
    const orphans = CAREERS.filter(
      (c) => !CAO_COURSES.some((co) => co.careerPaths.some((cp) => c.matchStrings.includes(cp))),
    );
    expect(orphans.map((c) => c.id)).toEqual([]);
  });

  test('career ids are unique', () => {
    const ids = CAREERS.map((c) => c.id);
    expect(new Set(ids).size).toBe(ids.length);
  });

  test('every field has a colour world + field icon, and every iconKey resolves', () => {
    for (const c of CAREERS) {
      expect(FIELD_WORLD[c.field], `colour world for ${c.id}`).toBeTruthy();
      expect(FIELD_ICON[c.field], `field icon for ${c.id}`).toBeTruthy();
      if (c.iconKey) expect(CAREER_ICONS[c.iconKey], `iconKey "${c.iconKey}" for ${c.id}`).toBeTruthy();
      expect(careerIcon(c.field, c.iconKey), `resolved icon for ${c.id}`).toBeTruthy();
    }
  });

  test('salary bands are sane (0 < start ≤ experienced)', () => {
    for (const c of CAREERS) {
      expect(c.salary.startK, `${c.id} startK`).toBeGreaterThan(0);
      expect(c.salary.experiencedK, `${c.id} experiencedK`).toBeGreaterThanOrEqual(c.salary.startK);
      expect(c.salary.note.length, `${c.id} salary note`).toBeGreaterThan(0);
    }
  });

  test('each card is fully populated', () => {
    for (const c of CAREERS) {
      expect(c.title.length, `${c.id} title`).toBeGreaterThan(0);
      expect(c.tagline.length, `${c.id} tagline`).toBeGreaterThan(0);
      expect(c.whatYouDo.length, `${c.id} whatYouDo`).toBeGreaterThanOrEqual(2);
      expect(c.routes.length, `${c.id} routes`).toBeGreaterThanOrEqual(1);
      expect(c.skills.length, `${c.id} skills`).toBeGreaterThanOrEqual(3);
      expect(c.pros.length, `${c.id} pros`).toBe(3);
      expect(c.cons.length, `${c.id} cons`).toBe(3);
      expect(c.matchStrings.length, `${c.id} matchStrings`).toBeGreaterThanOrEqual(1);
      expect(c.sources.length, `${c.id} sources`).toBeGreaterThanOrEqual(1);
    }
  });

  test('no HTML entities leaked into copy', () => {
    const blob = JSON.stringify(CAREERS);
    for (const ent of ['&amp;', '&gt;', '&lt;', '&#']) {
      expect(blob.includes(ent), `found ${ent} in career copy`).toBe(false);
    }
  });
});
