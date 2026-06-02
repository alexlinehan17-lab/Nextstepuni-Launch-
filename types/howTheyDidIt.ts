/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * "How They Did It" — a card deck of real people who overcame a SPECIFIC
 * disadvantage a Leaving Cert student might share (financial hardship, a
 * learning difference, arriving with little English, being first-in-family).
 *
 * Designed (2026-06-02) to the evidence on what makes role-model content help
 * vs backfire: lead with the struggle not the trophy (Lin-Siegler 2016);
 * attainable, near-peer-leaning, not untouchable-genius (Lockwood & Kunda 1997;
 * inverted-U of success, Morgenroth 2015); attribute success to PROCESS not
 * genius (Mueller & Dweck 1998); match the SPECIFIC barrier (Gladstone &
 * Cimpian 2021); link to a concrete copyable action (Oyserman possible-selves
 * RCT 2006); name the OUTSIDE help so it's never solo-willpower / bootstraps
 * (NEPC; ESRI); reframe the background as an asset (Yosso community cultural
 * wealth, esp. bilingualism for EAL). Content is source-cited.
 */

export type Barrier = 'financial' | 'dyslexia' | 'eal' | 'first-gen';

export interface PersonCard {
  id: string;
  name: string;
  barrier: Barrier;
  /** Their domain, e.g. "Sport", "Writing", "Medicine". */
  field: string;
  /** /assets/people/{portraitKey}.png — placeholder until the real PNG is supplied. */
  portraitKey: string;
  /** Front of the card: leads with the shared OBSTACLE (the similarity hook). */
  start: string;
  /** The struggle / messy middle — an immersive micro-scene, cost kept visible. */
  hardMiddle: string;
  /** 2-3 named, copyable strategies (process, not genius). */
  moves: string[];
  /** The concrete external support that mattered (never solo willpower). */
  outsideHelp: string;
  /** Where they are now, framed as the result of the process. */
  now: string;
  /** ONE concrete thing the student can do this week (a verb, not an adjective). */
  stealThisMove: string;
  /** Optional strengths reframe (e.g. bilingualism as an asset); '' if N/A. */
  strengthsLine: string;
  /** Source citations (traceability — same discipline as examRepsData). */
  sources: string[];
}

/** Student-facing barrier filters (match on the SPECIFIC barrier they carry). */
export const BARRIERS: { id: Barrier; label: string; tagline: string }[] = [
  { id: 'financial', label: 'Money was tight', tagline: 'Grew up with little money' },
  { id: 'dyslexia', label: 'I learn differently', tagline: 'Dyslexia or a learning difference' },
  { id: 'eal', label: 'New to Ireland / English', tagline: 'English wasn’t their first language' },
  { id: 'first-gen', label: 'First in my family', tagline: 'First to finish school or reach college' },
];

/** Persisted under progress/{uid}.howTheyDidIt (additive-merge namespace). */
export interface HowTheyDidItState {
  /** Card ids opened. */
  seenIds: string[];
  /** Card ids whose "steal this move" the student saved. */
  savedIds: string[];
  updatedAt: string;
}
