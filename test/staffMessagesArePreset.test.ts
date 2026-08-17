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
  STAFF_BROADCASTS,
  STAFF_ENCOURAGEMENT,
  STAFF_RECOMMENDATION_NOTES,
  isKnownStaffMessage,
  staffMessageText,
} from '@/data/staffEncouragement';
import {
  BROADCAST_IDS,
  ENCOURAGEMENT_IDS,
  RECOMMENDATION_NOTE_IDS,
  checkStaffMessage,
} from '@/functions/src/staffMessagePolicy';

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
    const all = [...STAFF_ENCOURAGEMENT, ...STAFF_RECOMMENDATION_NOTES, ...STAFF_BROADCASTS];
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

describe('the control is enforced on the server, not the renderer', () => {
  const read = (p: string) => readFileSync(resolve(root, p), 'utf8');

  it('rejects any message id staff may not send', () => {
    // The 2026-08-17 review: the old control lived in the student's own bundle
    // and keyed on `type`, a field the sender wrote. This is the server gate.
    expect(checkStaffMessage('encouragement', 'se1').ok).toBe(true);
    expect(checkStaffMessage('encouragement', 'meet me after school').ok).toBe(false);
    expect(checkStaffMessage('encouragement', 'sr1').ok).toBe(false); // wrong kind's id
    expect(checkStaffMessage('study-insight', 'se1').ok).toBe(false); // type laundering
    expect(checkStaffMessage('broadcast', 'sb1').ok).toBe(true);
    expect(checkStaffMessage(undefined, undefined).ok).toBe(false);
  });

  it('never lets caller text become the title or body', () => {
    const check = checkStaffMessage('encouragement', 'se2');
    expect(check.ok).toBe(true);
    if (check.ok) {
      // Title is generated from the kind; nothing the caller sent appears.
      expect(check.title).toBe('Words of encouragement');
      expect(check.type).toBe('gc-kudos');
    }
    const fn = read('functions/src/staffMessage.ts');
    expect(fn, 'body must be written empty, never from the caller').toContain('body: ""');
  });

  it('server ids and client display copy cover each other', () => {
    expect(ENCOURAGEMENT_IDS.sort()).toEqual(STAFF_ENCOURAGEMENT.map(m => m.id).sort());
    expect(RECOMMENDATION_NOTE_IDS.sort()).toEqual(STAFF_RECOMMENDATION_NOTES.map(m => m.id).sort());
    expect(BROADCAST_IDS.sort()).toEqual(STAFF_BROADCASTS.map(m => m.id).sort());
  });

  it('firestore.rules denies staff writes to a student notification doc', () => {
    // Rules cannot validate the `items` array, so the write path is closed and
    // routed through the callable instead.
    const rules = read('firestore.rules');
    const block = rules.slice(rules.indexOf('match /notifications/'), rules.indexOf('match /kudos/'));
    expect(block).toContain('allow read: if request.auth != null');
    expect(block, 'staff must not be able to create or update a student notification')
      .not.toMatch(/allow read, create, update: if request\.auth != null\s*\n\s*&& isSchoolStaff\(\)/);
  });

  it('no staff surface types free text to a student any more', () => {
    for (const file of ['components/gc/GCStudentDetail.tsx', 'components/gc/GCOverview.tsx']) {
      expect(read(file), `${file} still has a free-text field aimed at students`)
        .not.toMatch(/<textarea/);
    }
  });

  it('renders the title from a fixed table for staff-originated types', () => {
    const bell = read('components/NotificationBell.tsx');
    expect(bell).toContain('STAFF_TITLES');
    expect(bell).toContain('{displayTitle(item)}');
    expect(bell, 'the stored title must not be rendered raw').not.toMatch(/>\s*\{item\.title\}/);
  });
});
