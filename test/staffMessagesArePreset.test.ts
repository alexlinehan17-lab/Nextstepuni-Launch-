/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Safeguarding guard: a member of staff cannot send free text to a student.
 *
 * "Send Encouragement" and the note on "Recommend a Tool" were free-text
 * textareas — an unmoderated private channel from an adult to a minor, with no
 * review and no record of what was sent. Owner decision 2026-08-17: preset
 * messages only.
 *
 * Two halves, and the second is the one that matters. Removing the textarea
 * stops the dashboard sending prose. Rendering staff notifications from the
 * preset table by id — never from the stored `body` — is what makes it true
 * even for a document written directly through the SDK.
 */
import { describe, expect, it } from 'vitest';
import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';

import {
  STAFF_ENCOURAGEMENT,
  STAFF_RECOMMENDATION_NOTES,
  isKnownStaffMessage,
  staffMessageText,
} from '@/data/staffEncouragement';

const root = resolve(__dirname, '..');
const read = (p: string) => readFileSync(resolve(root, p), 'utf8');

describe('staff messages are preset', () => {
  it('resolves a known preset to its exact text', () => {
    const first = STAFF_ENCOURAGEMENT[0];
    expect(staffMessageText(first.id)).toBe(first.text);
  });

  it('refuses anything not in the table', () => {
    // The attack this defends against: a body written straight to Firestore.
    expect(staffMessageText('meet me after school')).toBe('A message from your school.');
    expect(staffMessageText(undefined)).toBe('A message from your school.');
    expect(isKnownStaffMessage('anything-else')).toBe(false);
    expect(isKnownStaffMessage(undefined)).toBe(false);
  });

  it('has unique, non-empty presets', () => {
    const all = [...STAFF_ENCOURAGEMENT, ...STAFF_RECOMMENDATION_NOTES];
    expect(all.length).toBeGreaterThan(0);
    expect(new Set(all.map(m => m.id)).size).toBe(all.length);
    for (const message of all) expect(message.text.trim().length).toBeGreaterThan(0);
  });

  it('the staff dashboard has no free-text field for messaging a student', () => {
    const source = read('components/gc/GCStudentDetail.tsx');
    expect(source, 'a textarea here is a private channel to a minor').not.toMatch(/<textarea/);
  });

  it('the student client renders staff notifications from the preset id, not the body', () => {
    const bell = read('components/NotificationBell.tsx');
    // Staff-originated types must go through the resolver.
    expect(bell).toMatch(/STAFF_ORIGINATED/);
    expect(bell).toMatch(/staffMessageText/);
    // and the raw body must not be rendered directly any more.
    expect(bell).not.toMatch(/line-clamp-2">\{item\.body\}/);

    const launchpad = read('components/InnovationZone.tsx');
    expect(launchpad).toMatch(/staffMessageText\(n\.messageId/);
    expect(launchpad, 'the tool card must not surface a stored body').not.toMatch(/message: n\.body/);
  });
});
