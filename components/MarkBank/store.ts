/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Mark Bank — persistence.
 *
 * An SRS tool is nothing but per-card state, so losing a session's reviews makes
 * it worthless. Four decisions follow from that, each one a defect this codebase
 * has already shipped somewhere else:
 *
 *  1. **localStorage is the hot path.** Grading a card is synchronous and never
 *     shows a spinner, so a review never waits on a network that, for a student
 *     on school wifi, may never answer.
 *
 *  2. **Firestore is written per card, not per deck.** A debounced whole-map
 *     mirror of ~800 cards is ~105 KB per flush; twelve grades a session would be
 *     over a megabyte every fifteen minutes, which is real money on a metered
 *     Android plan. A single dotted `updateDoc` per grade is ~150 bytes and
 *     removes the read-merge race between two devices entirely.
 *
 *  3. **Writes are never awaited.** With `persistentLocalCache`, an offline write
 *     promise neither resolves nor rejects, so awaiting one is a permanent hang.
 *     Everything goes through `saveInBackground`.
 *
 *  4. **State is seeded fresh on mount, never from the app-start snapshot.** The
 *     shared progress snapshot is taken once at boot and is not refreshed after a
 *     tool writes, which is why roughly nine Innovation Zone tools currently lose
 *     state saved in the same session when a student leaves and comes back.
 *
 * Deck state lives at `progress/{uid}/srs/{deckId}` — its own document, so ~800
 * cards of review state never inflate the app-boot read for a student who has not
 * opened the tool. Requires the matching `firestore.rules` block; Firestore rules
 * are non-hierarchical, so without it every save AND every reload is denied
 * silently.
 */

import { doc as fsDoc, getDoc, setDoc, updateDoc } from 'firebase/firestore';
import { db } from '../../firebase';
import { saveInBackground } from '../../utils/firestoreWrite';
import { NEW_CARD, type CardMemory } from './scheduler';
import { CARD_ID_ALIASES } from './cardAliases';
import { isValidCardId } from '../../types/markBank';
import { DEMO_STUDENT_UID } from '../../data/devStudent';

/** Bumped only for a shape migration. */
export const DECK_VERSION = 1;

export interface DeckState {
  v: number;
  cards: Record<string, CardMemory>;
  /** Student's exam date, ms epoch, if known. Drives the retention ramp. Stored
   *  here rather than in localStorage so the schedule cannot differ per device. */
  examTs?: number;
  updatedAt: number;
}

export type DeckId = string;

const LS_PREFIX = 'mb:deck:';
const lsKey = (uid: string | undefined, deckId: DeckId) => `${LS_PREFIX}${uid || 'anon'}:${deckId}`;

const emptyDeck = (): DeckState => ({ v: DECK_VERSION, cards: {}, updatedAt: 0 });

const deckPath = (uid: string, deckId: DeckId) => fsDoc(db, 'progress', uid, 'srs', deckId);

/* ------------------------------------------------------------------ local ---- */

export function readLocal(uid: string | undefined, deckId: DeckId): DeckState {
  try {
    const raw = localStorage.getItem(lsKey(uid, deckId));
    if (!raw) return emptyDeck();
    const parsed = JSON.parse(raw) as DeckState;
    if (!parsed || typeof parsed !== 'object' || !parsed.cards) return emptyDeck();
    return { ...emptyDeck(), ...parsed };
  } catch {
    return emptyDeck();
  }
}

/* --------------------------------------------------------- what you sit ---- */

/**
 * The subject and level this student actually sits.
 *
 * Local only, and deliberately so: it is a UI preference, not schedule state, and
 * it must be readable synchronously on mount — a student who does Chemistry
 * Ordinary should never watch the tool open on Biology Higher and correct it,
 * which is two clicks every single session forever.
 */
export interface DeckChoice { subjectId: string; level: 'higher' | 'ordinary' }

const choiceKey = (uid: string | undefined) => `mb:choice:${uid || 'anon'}`;

export function readChoice(uid: string | undefined): DeckChoice | null {
  try {
    const raw = localStorage.getItem(choiceKey(uid));
    if (!raw) return null;
    const parsed = JSON.parse(raw) as DeckChoice;
    if (!parsed?.subjectId) return null;
    return parsed.level === 'ordinary' || parsed.level === 'higher' ? parsed : null;
  } catch {
    return null;
  }
}

export function writeChoice(uid: string | undefined, choice: DeckChoice): void {
  try {
    localStorage.setItem(choiceKey(uid), JSON.stringify(choice));
  } catch {
    /* quota or private mode — the student just re-picks, which is the old behaviour */
  }
}

export function writeLocal(uid: string | undefined, deckId: DeckId, deck: DeckState): void {
  try {
    localStorage.setItem(lsKey(uid, deckId), JSON.stringify(deck));
  } catch {
    /* quota or private mode — the Firestore mirror is still authoritative */
  }
}

/* -------------------------------------------------------------- remote io ---- */

/**
 * Read the deck fresh from Firestore. Call on mount — never seed from the shared
 * progress snapshot.
 *
 * Concurrent reads of the same deck are de-duped, mirroring `useFreshProgress`,
 * so several mounts in one tick share a single `getDoc`.
 */
const inflight = new Map<string, Promise<DeckState | null>>();

export function fetchDeck(uid: string | undefined, deckId: DeckId): Promise<DeckState | null> {
  if (!uid || uid === DEMO_STUDENT_UID) return Promise.resolve(null);
  const key = `${uid}:${deckId}`;
  const existing = inflight.get(key);
  if (existing) return existing;
  const p = getDoc(deckPath(uid, deckId))
    .then(snap => (snap.exists() ? ({ ...emptyDeck(), ...(snap.data() as DeckState) }) : null))
    .catch(() => null)
    .finally(() => { inflight.delete(key); });
  inflight.set(key, p);
  return p;
}

/**
 * Merge a remote deck over local state.
 *
 * Per-card last-write-wins on `last`, so two devices reviewing the same deck
 * converge on the more recent review of each card rather than one clobbering the
 * other wholesale. Cards present on only one side survive.
 */
export function mergeDecks(local: DeckState, remote: DeckState | null): DeckState {
  if (!remote) return local;
  const cards: Record<string, CardMemory> = { ...remote.cards };
  for (const [id, mine] of Object.entries(local.cards)) {
    const theirs = cards[id];
    if (!theirs || (mine.last || 0) >= (theirs.last || 0)) cards[id] = mine;
  }
  return {
    v: DECK_VERSION,
    cards,
    examTs: remote.examTs ?? local.examTs,
    updatedAt: Math.max(local.updatedAt, remote.updatedAt || 0),
  };
}

/**
 * Make sure the deck document exists before any per-card update.
 *
 * `updateDoc` fails on a missing document, so a student's very first grade would
 * be lost without this. The payload deliberately carries NO dotted keys —
 * `setDoc` treats a dotted string as one literal field name, which is how points
 * data was silently lost elsewhere in this app.
 */
export function ensureDeck(uid: string | undefined, deckId: DeckId, now: number): void {
  if (!uid || uid === DEMO_STUDENT_UID) return;
  saveInBackground(
    setDoc(deckPath(uid, deckId), { v: DECK_VERSION, updatedAt: now }, { merge: true }),
    'MarkBank.ensureDeck',
    undefined,
    { silent: true },
  );
}

/**
 * Persist one card's memory. ~150 bytes on the wire.
 *
 * Dotted paths are `updateDoc`-only syntax and are correct here; the project's
 * payload guard bans them inside `setDoc` payloads, not this.
 */
export function saveCard(
  uid: string | undefined,
  deckId: DeckId,
  cardId: string,
  memory: CardMemory,
  now: number,
): void {
  if (!uid || uid === DEMO_STUDENT_UID) return;
  if (!isValidCardId(cardId)) {
    // A dot here would write to a nested field that isn't this card.
    throw new Error(`Mark Bank: unsafe card id for a Firestore field path: "${cardId}"`);
  }
  saveInBackground(
    updateDoc(deckPath(uid, deckId), { [`cards.${cardId}`]: stripUndefined(memory), updatedAt: now }),
    'MarkBank.saveCard',
    undefined,
    { silent: true },
  );
}

export function saveExamDate(uid: string | undefined, deckId: DeckId, examTs: number, now: number): void {
  if (!uid || uid === DEMO_STUDENT_UID) return;
  saveInBackground(
    setDoc(deckPath(uid, deckId), { examTs, updatedAt: now }, { merge: true }),
    'MarkBank.saveExamDate',
  );
}

/**
 * Drop undefined values. The SDK throws on `undefined` unless
 * `ignoreUndefinedProperties` is set, which this project deliberately does not
 * set — and a throw surfaces to a student as "check your connection".
 * `CardMemory.stepDue` is genuinely optional, so this is a real path, not paranoia.
 */
export function stripUndefined<T extends object>(obj: T): T {
  const out = {} as Record<string, unknown>;
  for (const [k, v] of Object.entries(obj)) if (v !== undefined) out[k] = v;
  return out as T;
}

/* ------------------------------------------------------------ operations ---- */

/**
 * Apply a graded review: update local state synchronously, then mirror one card.
 *
 * Returns the new deck so the caller can render immediately. Local first, always
 * — the student's next card must not wait on a write.
 */
export function commitReview(
  uid: string | undefined,
  deckId: DeckId,
  cardId: string,
  memory: CardMemory,
  now: number,
): DeckState {
  const local = readLocal(uid, deckId);
  const next: DeckState = {
    ...local,
    v: DECK_VERSION,
    cards: { ...local.cards, [cardId]: memory },
    updatedAt: now,
  };
  writeLocal(uid, deckId, next);
  saveCard(uid, deckId, cardId, memory, now);
  return next;
}

export function memoryFor(deck: DeckState, cardId: string): CardMemory {
  const candidates = [deck.cards[cardId]];
  for (const [legacyId, canonicalId] of Object.entries(CARD_ID_ALIASES)) {
    if (canonicalId === cardId) candidates.push(deck.cards[legacyId]);
  }
  return candidates
    .filter((memory): memory is CardMemory => Boolean(memory))
    .reduce<CardMemory | undefined>((latest, memory) => (
      !latest || (memory.last || 0) > (latest.last || 0) ? memory : latest
    ), undefined) ?? NEW_CARD;
}

/**
 * Seed an Ordinary Level card from the Higher Level sibling on the same concept,
 * writing only cards that are genuinely new to the OL deck. Called once when a
 * student switches level.
 */
export function seedLevelSwitch(
  uid: string | undefined,
  targetDeckId: DeckId,
  seeds: Record<string, CardMemory>,
  now: number,
): DeckState {
  const local = readLocal(uid, targetDeckId);
  const cards = { ...local.cards };
  let added = 0;
  for (const [id, memory] of Object.entries(seeds)) {
    if (cards[id]) continue;
    cards[id] = memory;
    added++;
    saveCard(uid, targetDeckId, id, memory, now);
  }
  if (!added) return local;
  const next: DeckState = { ...local, v: DECK_VERSION, cards, updatedAt: now };
  writeLocal(uid, targetDeckId, next);
  return next;
}

/* -------------------------------------------------------------- migration ---- */

/** Paper Trail's student-authored flashcards, as persisted today. */
interface LegacyFlashcard {
  id: string;
  front: string;
  back: string;
  subjectId?: string;
  stability?: number;
  difficulty?: number;
  intervalDays: number;
  reps: number;
  lapses: number;
  addedTs: number;
  lastTs: number;
}

export const LEGACY_PREFIX = 'pt:cards:';
export const MIGRATION_FLAG = 'mb:migrated:ptcards:';

/**
 * Read Paper Trail's flashcard deck so it can be folded into Mark Bank.
 *
 * Those cards are the student's own writing, scheduled with the same engine but
 * persisted only to localStorage — so clearing browser data or changing phone
 * destroys them silently. Folding them in is the fix; nothing is deleted here.
 *
 * A card that was scheduled but never given a stability value gets one derived
 * from its last interval, which is the honest reading of "we knew roughly this
 * much about your memory" — not an invented number.
 */
export function readLegacyFlashcards(uid: string | undefined): { cards: LegacyFlashcard[]; memories: Record<string, CardMemory> } {
  let cards: LegacyFlashcard[] = [];
  try {
    const raw = localStorage.getItem(LEGACY_PREFIX + (uid || 'anon'));
    if (raw) cards = Object.values(JSON.parse(raw) as Record<string, LegacyFlashcard>);
  } catch {
    return { cards: [], memories: {} };
  }
  const memories: Record<string, CardMemory> = {};
  for (const c of cards) {
    if (!isValidCardId(c.id)) continue;
    if (!c.lastTs) { memories[c.id] = { ...NEW_CARD }; continue; }
    memories[c.id] = {
      s: c.stability ?? Math.max(0.5, c.intervalDays || 1),
      d: c.difficulty ?? 5,
      last: c.lastTs,
      reps: c.reps,
      lapses: c.lapses,
      state: 2,
    };
  }
  return { cards, memories };
}

export function hasMigratedLegacy(uid: string | undefined): boolean {
  try {
    return localStorage.getItem(MIGRATION_FLAG + (uid || 'anon')) === '1';
  } catch {
    return false;
  }
}

export function markLegacyMigrated(uid: string | undefined): void {
  try {
    localStorage.setItem(MIGRATION_FLAG + (uid || 'anon'), '1');
  } catch {
    /* private mode — worst case the migration is attempted again, which is idempotent */
  }
}
