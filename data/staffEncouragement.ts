/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Preset messages for staff → student encouragement and tool recommendations.
 *
 * ─── WHY PRESETS, NOT FREE TEXT (2026-08-17, owner decision) ───────────────
 *
 * "Send Encouragement" and the note on "Recommend a Tool" were free-text
 * fields, which made the product an unmoderated private messaging channel from
 * an adult to a minor, with no logging, no review and no way for a parent or
 * DLP to see what had been sent. That is not a feature this product can carry.
 *
 * The safeguarding property is achieved the same way peer kudos already does
 * it (see kudosData.ts / hooks/useKudos.ts): the sender writes an ID, and the
 * student's client renders text from this table. Arbitrary text therefore
 * cannot reach a student even if a document were written directly through the
 * SDK, bypassing the UI — an unknown id renders the neutral fallback, not the
 * stored string. A client-side restriction alone would only be theatre.
 *
 * Tone note: these are deliberately warmer and more specific than the peer
 * kudos list, and say nothing about a student's ability, mood or wellbeing —
 * an adult's message carries more weight, and anything read as a judgement of
 * the student rather than of the work is out of scope for a preset nobody
 * reviews before it sends.
 */

export interface StaffMessage {
  id: string;
  text: string;
}

/** "Send Encouragement" — the whole message a student receives. */
export const STAFF_ENCOURAGEMENT: StaffMessage[] = [
  { id: 'se1', text: 'Great to see the work you have been putting in — keep going.' },
  { id: 'se2', text: 'Really strong effort lately. Well done.' },
  { id: 'se3', text: 'You are making steady progress. Stick with it.' },
  { id: 'se4', text: 'Nice consistency this week — that is the hard part.' },
  { id: 'se5', text: 'Good to see you back at it. One step at a time.' },
  { id: 'se6', text: 'That is a solid bit of work. Keep it up.' },
  { id: 'se7', text: 'You are on the right track. Keep the routine going.' },
  { id: 'se8', text: 'Well done for sticking with a tough topic.' },
];

/** Optional note attached to a tool recommendation. */
export const STAFF_RECOMMENDATION_NOTES: StaffMessage[] = [
  { id: 'sr1', text: 'This one might help with what you are working on.' },
  { id: 'sr2', text: 'Worth ten minutes when you get a chance.' },
  { id: 'sr3', text: 'Have a look at this before your next study session.' },
  { id: 'sr4', text: 'This should make the next step a bit clearer.' },
  { id: 'sr5', text: 'Give this a try and see how you get on.' },
];

const BY_ID: Record<string, string> = Object.fromEntries(
  [...STAFF_ENCOURAGEMENT, ...STAFF_RECOMMENDATION_NOTES].map(m => [m.id, m.text]),
);

/**
 * Resolve a preset id to its text.
 *
 * Returns the fallback for anything not in the table — including any legacy
 * free-text notification written before presets existed, which is the point:
 * text that did not come from this file is never rendered to a student.
 */
export function staffMessageText(messageId: string | undefined, fallback = 'A message from your school.'): string {
  if (!messageId) return fallback;
  return BY_ID[messageId] ?? fallback;
}

/** True when the id is one this app is willing to render. */
export function isKnownStaffMessage(messageId: string | undefined): boolean {
  return !!messageId && messageId in BY_ID;
}
