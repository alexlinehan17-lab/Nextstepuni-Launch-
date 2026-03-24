/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

/**
 * Client-side profanity filter for SOS Flare text content.
 * Checks against a keyword list with basic leetspeak normalization.
 */

const PROFANITY_LIST: string[] = [
  // Common English profanity
  'fuck', 'shit', 'ass', 'asshole', 'bitch', 'bastard', 'damn', 'dick',
  'cock', 'cunt', 'piss', 'whore', 'slut', 'wanker', 'twat', 'bollocks',
  'crap', 'prick', 'arsehole', 'arse', 'tosser', 'bellend',
  // Slurs and hate speech
  'nigger', 'nigga', 'faggot', 'fag', 'retard', 'retarded', 'spastic',
  'tranny', 'dyke',
  // Irish slang profanity
  'gobshite', 'shitehawk', 'fecker', 'bollix', 'eejit',
  // Sexual terms
  'porn', 'dildo', 'blowjob',
  // Drug references
  'cocaine', 'heroin',
  // Violence
  'kill yourself', 'kys',
];

/** Multi-word phrases that need exact substring matching */
const PHRASE_LIST: string[] = [
  'kill yourself',
  'kys',
];

/** Leetspeak character substitutions */
const LEET_MAP: Record<string, string> = {
  '0': 'o',
  '1': 'i',
  '3': 'e',
  '4': 'a',
  '5': 's',
  '7': 't',
  '@': 'a',
  '$': 's',
  '!': 'i',
};

/** Normalize text: lowercase + leetspeak substitution + collapse repeated chars */
function normalize(text: string): string {
  let result = text.toLowerCase();

  // Leetspeak substitution
  result = result.replace(/[013457@$!]/g, ch => LEET_MAP[ch] || ch);

  // Strip non-alphanumeric except spaces (removes asterisks, dots used to bypass)
  result = result.replace(/[^a-z\s]/g, '');

  return result;
}

/** Single-word list (excluding multi-word phrases) */
const SINGLE_WORDS = PROFANITY_LIST.filter(w => !w.includes(' '));

/** Build word-boundary regex for single words */
const WORD_REGEX = new RegExp(
  '\\b(' + SINGLE_WORDS.map(w => w.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')).join('|') + ')\\b',
  'i',
);

/**
 * Returns true if the text contains profanity.
 */
export function containsProfanity(text: string): boolean {
  const normalized = normalize(text);

  // Check multi-word phrases first (substring match)
  for (const phrase of PHRASE_LIST) {
    if (normalized.includes(phrase)) return true;
  }

  // Check single words with word boundaries (avoids "class", "assess", etc.)
  return WORD_REGEX.test(normalized);
}
