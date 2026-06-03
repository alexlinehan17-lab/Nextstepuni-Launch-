/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * "How They Did It" — a card deck of real people who overcame a SPECIFIC
 * disadvantage a Leaving Cert student might share (financial hardship, a
 * learning difference, arriving with little English, being first-in-family).
 *
 * Built to the evidence on what makes role-model content help vs backfire:
 * lead with the struggle not the trophy (Lin-Siegler 2016); attainable,
 * near-peer-leaning, not untouchable-genius (Lockwood & Kunda 1997; Morgenroth
 * 2015); attribute success to PROCESS not genius (Mueller & Dweck 1998); match
 * the SPECIFIC barrier (Gladstone & Cimpian 2021); link to a concrete copyable
 * action (Oyserman 2006); name the OUTSIDE help so it's never solo-willpower
 * (NEPC; ESRI); reframe the background as an asset (Yosso). Content is source-cited.
 *
 * Presentation (redesigned 2026-06-03): an immersive "colour world" swipe deck —
 * one bold idea per screen, tightened copy, tap-to-flip moves. Each barrier owns
 * a colour (see BARRIER_WORLD in the component). Copy is deliberately short.
 */

export type Barrier = 'financial' | 'dyslexia' | 'eal' | 'first-gen';

/** One concrete strategy: a short verb-led title + a one-line detail (the flip). */
export interface PersonMove {
  /** 2-5 word headline, e.g. "Showed up anyway". */
  title: string;
  /** One short sentence of detail revealed on flip. */
  detail: string;
}

export interface PersonCard {
  id: string;
  name: string;
  barrier: Barrier;
  /** Their domain, kept short, e.g. "Boxing", "Writing", "Medicine". */
  field: string;
  /** Emoji glyph shown on the colour-world face (until a real PNG is supplied). */
  emoji: string;
  /** /assets/people/{portraitKey}.png — reserved for future real portraits. */
  portraitKey: string;
  /** Card face: the shared OBSTACLE in one short line (the similarity hook). */
  hook: string;
  /** Their own words — a short pull-quote. '' if no first-person line fits. */
  quote: string;
  /** The struggle, as 2-3 short beats (one idea each) — not a paragraph. */
  struggle: string[];
  /** 2-3 named, copyable strategies (process, not genius). */
  moves: PersonMove[];
  /** The concrete external support that mattered (never solo willpower). */
  helpedBy: string;
  /** Where they are now, framed as the result of the process — one line. */
  now: string;
  /** ONE concrete thing the student can do this week (a verb, not an adjective). */
  stealThisMove: string;
  /** Optional strengths reframe (e.g. bilingualism as an asset); '' if N/A. */
  strengthsLine: string;
  /** Source citations (traceability — same discipline as the rest of the app). */
  sources: string[];
}

/** Student-facing barrier filters (match on the SPECIFIC barrier they carry). */
export const BARRIERS: { id: Barrier; label: string; tagline: string; emoji: string }[] = [
  { id: 'financial', label: 'Money was tight', tagline: 'Grew up with little money', emoji: '💶' },
  { id: 'dyslexia', label: 'I learn differently', tagline: 'Dyslexia or a learning difference', emoji: '🧩' },
  { id: 'eal', label: 'New to Ireland / English', tagline: 'English wasn’t their first language', emoji: '🌍' },
  { id: 'first-gen', label: 'First in my family', tagline: 'First to finish school or reach college', emoji: '🎓' },
];

/** Persisted under progress/{uid}.howTheyDidIt (additive-merge namespace). */
export interface HowTheyDidItState {
  /** Card ids opened. */
  seenIds: string[];
  /** Card ids whose "steal this move" the student saved. */
  savedIds: string[];
  updatedAt: string;
}
