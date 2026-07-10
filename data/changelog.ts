/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * "What's new" entries — newest first. The sidebar dot lights up when the
 * top entry's id differs from the account's last-seen id. Keep each entry
 * to two or three plain lines a student actually cares about; this is a
 * heads-up, not release notes.
 */

export interface ChangelogEntry {
  /** Stable id — bump by adding a new entry, never editing an old id. */
  id: string;
  /** Human date, e.g. "July 2026". */
  date: string;
  title: string;
  lines: string[];
}

export const CHANGELOG: ChangelogEntry[] = [
  {
    id: '2026-07-marking-lens',
    date: 'July 2026',
    title: 'Marking Lens — how the marks are given',
    lines: [
      'Under questions in the Topic Vault you’ll now find "How the marks are given": the official scheme’s own marks grid, decoded part by part.',
      'See exactly what each mark is for — state, develop, link, example — before you look at the scheme itself.',
      'Starting with Business; more subjects are being added from the filed SEC schemes.',
    ],
  },
  {
    id: '2026-07-topic-vault',
    date: 'July 2026',
    title: 'Questions by topic, as printed',
    lines: [
      'Pick a subject and topic in Paper Trail → Revise: every past question on it, newest first, shown exactly as printed on the paper.',
      'Tap "Show the marking scheme" under any question to reveal the official scheme — and hide it again.',
      'Now covers 41 subjects including English (by poet and text), Irish, French, German, Spanish and Arabic.',
    ],
  },
  {
    id: '2026-07-qol',
    date: 'July 2026',
    title: 'Faster ways around',
    lines: [
      'Press ⌘K (or Ctrl+K) to jump straight to any module, tool or page.',
      'The home page now offers to pick up exactly where you left off.',
      'Papers you use most can be pinned in Paper Trail.',
    ],
  },
  {
    id: '2026-07-site-guide',
    date: 'July 2026',
    title: 'The Site Guide',
    lines: [
      'Press the ? in the sidebar for a guided tour of every core page.',
      'New accounts get a three-step welcome tour on first visit.',
    ],
  },
  {
    id: '2026-07-full-loop',
    date: 'July 2026',
    title: 'Paper Trail: The Full Loop',
    lines: [
      'Work a whole paper question by question, self-mark against the real scheme, and see your gaps at the end.',
      'Low self-marks now link to similar questions from other years.',
    ],
  },
];

/** The id the "seen" marker compares against. */
export const LATEST_CHANGELOG_ID = CHANGELOG[0]?.id ?? '';
