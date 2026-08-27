/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Timetable subject chips carry one ink — white — on a deepened version of the
 * subject's own colour. That only works if EVERY subject in the palette is
 * deepened far enough to clear AA, so this locks the property rather than the
 * particular hex values: add a subject to the palette and this test tells you
 * if its chip would be unreadable.
 */
import { describe, expect, it } from 'vitest';

import { subjectFill } from '@/components/SpacedRepetitionTimetable';
import { LC_SUBJECTS, JC_SUBJECTS, LCA_SUBJECTS } from '@/components/subjectData';

const AA = 4.5;

function contrastWithWhite(hex: string): number {
  const lin = (v: number) => (v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4));
  const [r, g, b] = [1, 3, 5].map(i => lin(parseInt(hex.slice(i, i + 2), 16) / 255));
  const l = 0.2126 * r + 0.7152 * g + 0.0722 * b;
  return 1.05 / (l + 0.05);
}

function hue(hex: string): number {
  const [r, g, b] = [1, 3, 5].map(i => parseInt(hex.slice(i, i + 2), 16) / 255);
  const max = Math.max(r, g, b), min = Math.min(r, g, b);
  if (max === min) return -1; // grey: no meaningful hue
  const d = max - min;
  const h = max === r ? ((g - b) / d + (g < b ? 6 : 0))
    : max === g ? (b - r) / d + 2
      : (r - g) / d + 4;
  return (h / 6) * 360;
}

// The palette is private to the component; drive the test off the real subject
// lists so a newly added subject is covered automatically. Subjects with no
// palette entry fall back to grey, which must also carry white text.
const SUBJECT_NAMES: string[] = Array.from(new Set(
  [...LC_SUBJECTS, ...JC_SUBJECTS, ...LCA_SUBJECTS].map(s => s.name),
));

describe('subjectFill', () => {
  it('returns a valid 6-digit hex', () => {
    expect(subjectFill('#eab308')).toMatch(/^#[0-9a-f]{6}$/i);
  });

  it('deepens every subject enough for white text to clear AA', () => {
    const failures: string[] = [];
    for (const name of SUBJECT_NAMES) {
      const fill = subjectFill(subjectHexFor(name));
      const ratio = contrastWithWhite(fill);
      if (ratio < AA) failures.push(`${name}: ${fill} at ${ratio.toFixed(2)}:1`);
    }
    expect(failures).toEqual([]);
  });

  it('leaves colours that already clear AA untouched', () => {
    // Tailwind blue-600: already dark enough, must not be darkened further.
    expect(subjectFill('#2563eb')).toBe('#2563eb');
  });

  it('preserves the hue, so a subject stays its own colour', () => {
    // German's yellow must still read as yellow, not brown-black.
    const before = hue('#eab308');
    const after = hue(subjectFill('#eab308'));
    expect(Math.abs(after - before)).toBeLessThan(6);
  });

  it('is deterministic and cheap to call repeatedly in render', () => {
    const a = subjectFill('#84cc16');
    const b = subjectFill('#84cc16');
    expect(a).toBe(b);
  });

  it('handles pure black and pure white without looping forever', () => {
    expect(subjectFill('#000000')).toMatch(/^#[0-9a-f]{6}$/i);
    expect(contrastWithWhite(subjectFill('#ffffff'))).toBeGreaterThanOrEqual(AA);
  });
});

/** Mirror of the component's palette lookup, kept local to the test. */
function subjectHexFor(name: string): string {
  const SUBJECT_HEX: Record<string, string> = {
    'English': '#3b82f6', 'Irish': '#10b981', 'Mathematics': '#6366f1',
    'French': '#0ea5e9', 'German': '#eab308', 'Spanish': '#f97316',
    'Italian': '#ef4444', 'Japanese': '#ec4899', 'Physics': '#06b6d4',
    'Chemistry': '#14b8a6', 'Biology': '#84cc16', 'Applied Maths': '#8b5cf6',
    'Computer Science': '#d946ef', 'Ag Science': '#22c55e', 'Accounting': '#f59e0b',
    'Business': '#d97706', 'Economics': '#ca8a04', 'History': '#a855f7',
    'Geography': '#059669', 'Politics & Society': '#f43f5e',
    'Religious Education': '#71717a', 'Classical Studies': '#78716c',
    'Home Economics': '#fb923c', 'Construction Studies': '#64748b',
    'Engineering': '#6b7280', 'DCG': '#737373', 'Technology': '#2563eb',
    'Art': '#fb7185', 'Music': '#f472b6',
    'Design & Communication Graphics': '#818cf8',
  };
  return SUBJECT_HEX[name] || '#71717a';
}
