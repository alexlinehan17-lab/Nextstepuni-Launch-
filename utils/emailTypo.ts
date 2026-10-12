/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Likely-typo detection for the email domain at signup.
 *
 * A mistyped domain can never receive the verification or password-reset
 * email, so the student is locked out the first time they forget their
 * password. Real signups include `marinocollge.ie` (no mail server at all),
 * `gmail.comdeedw` and `marino.ie` (another organisation's domain). This only
 * ever SUGGESTS a correction; the address the student typed is always allowed.
 */
import { SCHOOL_IDENTITY } from '../data/schoolIdentity';

const CONSUMER_DOMAINS = [
  'gmail.com',
  'googlemail.com',
  'hotmail.com',
  'hotmail.ie',
  'hotmail.co.uk',
  'outlook.com',
  'outlook.ie',
  'live.com',
  'live.ie',
  'icloud.com',
  'me.com',
  'yahoo.com',
  'yahoo.ie',
  'yahoo.co.uk',
  'eircom.net',
];

// Real providers that sit one keystroke from a consumer domain above. They
// are never "corrected", and never suggested either.
const OTHER_REAL_DOMAINS = ['mail.com', 'ymail.com', 'gmx.com', 'msn.com', 'aol.com', 'proton.me', 'protonmail.com'];

// Partner schools' student addresses use the school's website domain
// (marinocollege.ie, oconnellschool.ie, stjosephsfairview.ie and pwc.ie all
// appear on real accounts).
const SCHOOL_DOMAINS = Object.values(SCHOOL_IDENTITY)
  .map(({ website }) => new URL(website).hostname.replace(/^www\./, ''));

// Real domains that belong to someone else but that a partner school's
// students type as shorthand for their own. `marino.ie` is another
// organisation's mail domain; Marino College students used it on real
// signups, so their emails went elsewhere.
const SCHOOL_SHORTHANDS: Record<string, string> = {
  'marino.ie': 'marinocollege.ie',
};

const SUGGESTED_DOMAINS = [...CONSUMER_DOMAINS, ...SCHOOL_DOMAINS];
const VALID_DOMAINS = new Set([...SUGGESTED_DOMAINS, ...OTHER_REAL_DOMAINS]);

/** Optimal string alignment distance: insertions, deletions, substitutions and adjacent swaps. */
function editDistance(a: string, b: string): number {
  const rows = a.length + 1, cols = b.length + 1;
  const d: number[][] = Array.from({ length: rows }, (_, i) => Array.from({ length: cols }, (_, j) => (i === 0 ? j : j === 0 ? i : 0)));
  for (let i = 1; i < rows; i++) {
    for (let j = 1; j < cols; j++) {
      const cost = a[i - 1] === b[j - 1] ? 0 : 1;
      d[i][j] = Math.min(d[i - 1][j] + 1, d[i][j - 1] + 1, d[i - 1][j - 1] + cost);
      if (i > 1 && j > 1 && a[i - 1] === b[j - 2] && a[i - 2] === b[j - 1]) {
        d[i][j] = Math.min(d[i][j], d[i - 2][j - 2] + 1);
      }
    }
  }
  return d[a.length][b.length];
}

/**
 * The address with its domain corrected, or null when the domain looks
 * intentional. The local part is kept exactly as typed.
 */
export function suggestEmailCorrection(input: string): string | null {
  const email = input.trim();
  const at = email.lastIndexOf('@');
  if (at < 1) return null;
  const local = email.slice(0, at);
  const domain = email.slice(at + 1).toLowerCase();
  if (SCHOOL_SHORTHANDS[domain]) return `${local}@${SCHOOL_SHORTHANDS[domain]}`;
  if (domain.length < 4 || VALID_DOMAINS.has(domain)) return null;

  // Letters after a complete domain: "gmail.comdeedw", "gmail.com.".
  const extended = SUGGESTED_DOMAINS
    .filter(known => domain.startsWith(known))
    .sort((a, b) => b.length - a.length)[0];
  if (extended) return `${local}@${extended}`;

  let best: string | null = null;
  let bestDistance = Infinity;
  for (const known of SUGGESTED_DOMAINS) {
    const distance = editDistance(domain, known);
    const allowed = known.length >= 12 ? 2 : 1;
    if (distance <= allowed && distance < bestDistance) {
      best = known;
      bestDistance = distance;
    }
  }
  return best ? `${local}@${best}` : null;
}
