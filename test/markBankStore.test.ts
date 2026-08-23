/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Mark Bank — card model and persistence guards.
 *
 * Each block below pins a defect that actually shipped in the tools Mark Bank
 * replaces, or in this app's Firestore layer. They are regression tests for
 * mistakes already made, not hypotheticals.
 */

import { describe, it, expect, beforeEach, vi } from 'vitest';
import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';

import {
  MAX_ROWS,
  isContentFreeRow,
  isDiagramCard,
  isSecCard,
  isValidCardId,
  looksLikeSectionLabel,
  rowId,
  tariffReconciles,
  type MarkRow,
  type SecCard,
  type SecDiagramCard,
  type StudentCard,
} from '../types/markBank';

/* --------------------------------------------------------------- fixtures ---- */

const row = (over: Partial<MarkRow> = {}): MarkRow => ({
  id: 'r0', kind: 'point', verbatim: 'Oesophagus', marks: 2, ...over,
});

const secCard = (over: Partial<SecCard> = {}): SecCard => ({
  source: 'sec',
  kind: 'question',
  id: 'bio-2025-hl-q6-ab',
  subjectId: 'biology',
  level: 'higher',
  topicId: 'biology-2-3',
  conceptId: 'digestive-system-parts',
  year: 2025,
  paperFileid: 'LC025ALP038EV',
  section: 'A',
  questionRef: '2025 HL Q6(a)–(b)',
  questionText: 'Name the parts labelled A and B.',
  tariffModel: { kind: 'fixed' },
  totalMarks: 4,
  rows: [row({ id: 'r0', verbatim: 'Oesophagus', marks: 2 }), row({ id: 'r1', verbatim: 'Stomach', marks: 2 })],
  schemeCitation: 'SEC marking scheme, Biology 2025 Higher Level — © State Examinations Commission',
  specVersion: 'lc-biology-2002',
  qa: { gates: ['verbatim', 'tariff'], humanReviewedBy: 'al', humanReviewedAt: '2026-07-30' },
  ...over,
} as SecCard);

/* ----------------------------------------------------------- the card type ---- */

describe('a card cannot exist without a real question', () => {
  it('rejects the exact string that shipped as a question 24 times', () => {
    expect(looksLikeSectionLabel('Section A short answer (10m).')).toBe(true);
  });

  it('rejects the other shapes of non-question', () => {
    for (const bad of ['Section B', 'Question 1', 'Question 14.', '(10m)', '10 marks', 'short answer', '  ']) {
      expect(looksLikeSectionLabel(bad)).toBe(true);
    }
  });

  it('accepts genuine SEC question wording', () => {
    for (const good of [
      'Name the parts labelled A and B.',
      'Describe the effect of increasing temperature on enzyme activity.',
      'Outline how water from the soil reaches the leaf.',
      'Give one function of the structure labelled C.',
    ]) {
      expect(looksLikeSectionLabel(good)).toBe(false);
    }
  });
});

describe('a marking row must carry an answer, not a tariff', () => {
  it('rejects the row that made Answer Architect unusable', () => {
    expect(isContentFreeRow('Three items, 2 marks each.')).toBe(true);
    expect(isContentFreeRow('The description earns 4 marks.')).toBe(true);
  });

  it('rejects content-free Section B criteria', () => {
    for (const bad of [
      'Named piece of apparatus used',
      'Control named and setup described',
      'Safety precaution described',
      'Left for a suitable time',
      'Correct position',
    ]) {
      expect(isContentFreeRow(bad)).toBe(true);
    }
  });

  it('accepts the real answer content the scheme actually printed', () => {
    for (const good of [
      'Bale wrapper',
      'Stomach tube',
      'Head gate / fostering crate',
      '(involuntary) muscular contractions (that push food)',
      'Set up a sealed Petri dish with a leaf disc, upper surface down, on the lid',
    ]) {
      expect(isContentFreeRow(good)).toBe(false);
    }
  });
});

describe('tariff arithmetic reconciles against the paper', () => {
  it('passes a fixed card whose rows sum to the printed tariff', () => {
    expect(tariffReconciles(secCard())).toBe(true);
  });

  it('fails a fixed card whose rows do not sum', () => {
    expect(tariffReconciles(secCard({ totalMarks: 10 }))).toBe(false);
  });

  it('ignores gate rows in the sum, since they carry no marks of their own', () => {
    const card = secCard({
      totalMarks: 4,
      rows: [
        row({ id: 'g0', kind: 'gate', verbatim: 'Sporangium', marks: 0, exactTermRequired: true }),
        row({ id: 'r0', verbatim: 'Oesophagus', marks: 2 }),
        row({ id: 'r1', verbatim: 'Stomach', marks: 2 }),
      ],
    });
    expect(tariffReconciles(card)).toBe(true);
  });

  it('catches the best-N-of-parts case where six rows x 4m would display 24 on a 20-mark question', () => {
    const rows = Array.from({ length: 6 }, (_, i) => row({ id: `r${i}`, verbatim: `point ${i}`, marks: 4 }));
    const wrong = secCard({ tariffModel: { kind: 'fixed' }, totalMarks: 20, rows });
    expect(tariffReconciles(wrong)).toBe(false);

    const right = secCard({
      tariffModel: { kind: 'bestNofParts', answer: 5, ofParts: 6, perPart: 4 },
      totalMarks: 20,
      rows,
    });
    expect(tariffReconciles(right)).toBe(true);
  });

  it('requires order-dependent splits to carry no per-row marks, rather than inventing them', () => {
    const rows = [
      row({ id: 'r0', verbatim: 'concentration gradient', marks: null }),
      row({ id: 'r1', verbatim: 'osmosis', marks: null }),
    ];
    const honest = secCard({ tariffModel: { kind: 'orderedSplit', notation: '2(5) + 5(2)' }, totalMarks: 20, rows });
    expect(tariffReconciles(honest)).toBe(true);

    const invented = secCard({
      tariffModel: { kind: 'orderedSplit', notation: '2(5) + 5(2)' },
      totalMarks: 20,
      rows: [row({ id: 'r0', verbatim: 'concentration gradient', marks: 5 })],
    });
    expect(tariffReconciles(invented)).toBe(false);
  });

  it('sums an anyN group by its claimable maximum', () => {
    const card = secCard({
      totalMarks: 12,
      rows: [row({
        id: 'g', kind: 'anyN', verbatim: 'Any four of the following', marks: null,
        group: { claimMax: 4, perOption: 3, options: ['a', 'b', 'c', 'd', 'e'] },
      })],
    });
    expect(tariffReconciles(card)).toBe(true);
  });
});

describe('card ids stay safe as Firestore field paths', () => {
  it('accepts the real id shape', () => {
    expect(isValidCardId('bio-2025-hl-q6-ab')).toBe(true);
  });

  it('rejects a dot, which would write to a different nested field', () => {
    expect(isValidCardId('bio.2025.hl.q6')).toBe(false);
  });

  it('rejects slashes and reserved sequences', () => {
    expect(isValidCardId('bio/2025/q6')).toBe(false);
    expect(isValidCardId('__proto__')).toBe(false);
    expect(isValidCardId('')).toBe(false);
  });
});

describe('card variants', () => {
  it('distinguishes SEC cards from a student\'s own', () => {
    const own: StudentCard = {
      source: 'student', kind: 'own', id: 'own-1', subjectId: 'biology', level: 'higher',
      topicId: 'biology-2-3', conceptId: 'own-1', front: 'What is a ribosome?',
      back: 'Site of protein synthesis', addedTs: 0,
    };
    expect(isSecCard(own)).toBe(false);
    expect(isSecCard(secCard())).toBe(true);
    expect(isDiagramCard(own)).toBe(false);
  });

  it('identifies a diagram card, which by type must carry its answer key', () => {
    const diagram: SecDiagramCard = {
      ...secCard(),
      kind: 'diagram',
      figure: {
        candId: 'cand_2025hl_p8_1', src: '/exam-figures/biology/bio-2025-hl-digestive.png',
        srcHash: 'a1b2c3', alt: 'Digestive tract with two lettered leader lines',
        lettersVisible: ['A', 'B'], attribution: 'SEC Biology 2025 HL Q6',
      },
      labelKey: [
        { letter: 'A', meaning: 'Oesophagus', askedInThisQuestion: true },
        { letter: 'B', meaning: 'Stomach', askedInThisQuestion: true },
      ],
    };
    expect(isDiagramCard(diagram)).toBe(true);
    // Every letter visible in the crop is decoded for the student.
    expect(diagram.labelKey.map(k => k.letter)).toEqual(
      expect.arrayContaining(diagram.figure.lettersVisible),
    );
  });

  it('caps rows at five so one card stays one memory and fits a phone', () => {
    expect(MAX_ROWS).toBe(5);
    expect(secCard().rows.length).toBeLessThanOrEqual(MAX_ROWS);
  });

  it('falls back to an index for a row without an id', () => {
    expect(rowId({ id: '' }, 3)).toBe('r3');
    expect(rowId({ id: 'gate-a' }, 3)).toBe('gate-a');
  });
});

/* ------------------------------------------------------------------ store ---- */

vi.mock('../firebase', () => ({ db: {} }));
const writes: { kind: string; payload: Record<string, unknown> }[] = [];
vi.mock('firebase/firestore', () => ({
  doc: (..._a: unknown[]) => ({ path: _a.slice(1).join('/') }),
  getDoc: () => Promise.resolve({ exists: () => false, data: () => undefined }),
  setDoc: (_ref: unknown, payload: Record<string, unknown>) => {
    writes.push({ kind: 'setDoc', payload });
    return Promise.resolve();
  },
  updateDoc: (_ref: unknown, payload: Record<string, unknown>) => {
    writes.push({ kind: 'updateDoc', payload });
    return Promise.resolve();
  },
}));

const store = await import('../components/MarkBank/store');
const { NEW_CARD } = await import('../components/MarkBank/scheduler');

const NOW = Date.UTC(2026, 6, 30, 12, 0, 0);
const UID = 'student-1';
const DECK = 'biology-higher';

beforeEach(() => {
  writes.length = 0;
  localStorage.clear();
});

describe('the review survives, which is the whole point', () => {
  it('writes locally and reads back the same memory', () => {
    const memory = { s: 4.2, d: 5.1, last: NOW, reps: 1, lapses: 0, state: 2 as const };
    store.commitReview(UID, DECK, 'bio-2025-hl-q6-ab', memory, NOW);
    expect(store.memoryFor(store.readLocal(UID, DECK), 'bio-2025-hl-q6-ab')).toEqual(memory);
  });

  it('treats an unknown card as new rather than throwing', () => {
    expect(store.memoryFor(store.readLocal(UID, DECK), 'never-seen')).toEqual(NEW_CARD);
  });

  it('survives corrupt localStorage instead of taking the tool down', () => {
    localStorage.setItem(`mb:deck:${UID}:${DECK}`, '{not json');
    expect(store.readLocal(UID, DECK).cards).toEqual({});
  });
});

describe('Firestore writes are shaped so they cannot fail silently', () => {
  it('mirrors one card per grade, not the whole deck', () => {
    for (let i = 0; i < 3; i++) {
      store.commitReview(UID, DECK, `bio-c${i}`, { s: 3, d: 5, last: NOW, reps: 1, lapses: 0, state: 2 }, NOW);
    }
    const updates = writes.filter(w => w.kind === 'updateDoc');
    expect(updates).toHaveLength(3);
    for (const u of updates) {
      // Exactly one card key plus the timestamp — never a whole-map mirror.
      const cardKeys = Object.keys(u.payload).filter(k => k.startsWith('cards.'));
      expect(cardKeys).toHaveLength(1);
    }
  });

  it('uses a dotted path for the card, which is updateDoc-only syntax', () => {
    store.commitReview(UID, DECK, 'bio-2025-hl-q6-ab', { s: 3, d: 5, last: NOW, reps: 1, lapses: 0, state: 2 }, NOW);
    const update = writes.find(w => w.kind === 'updateDoc');
    expect(Object.keys(update!.payload)).toContain('cards.bio-2025-hl-q6-ab');
  });

  it('never puts a dotted key in a setDoc payload, which would create a literal field name', () => {
    store.ensureDeck(UID, DECK, NOW);
    store.saveExamDate(UID, DECK, Date.UTC(2027, 5, 9), NOW);
    for (const w of writes.filter(w => w.kind === 'setDoc')) {
      for (const key of Object.keys(w.payload)) expect(key).not.toContain('.');
    }
  });

  it('never sends undefined, which the SDK throws on', () => {
    // stepDue is genuinely absent on a review-state card.
    store.commitReview(UID, DECK, 'bio-c1', { s: 3, d: 5, last: NOW, reps: 1, lapses: 0, state: 2 }, NOW);
    const update = writes.find(w => w.kind === 'updateDoc');
    const payload = update!.payload['cards.bio-c1'] as Record<string, unknown>;
    expect(Object.values(payload)).not.toContain(undefined);
    expect('stepDue' in payload).toBe(false);
  });

  it('keeps stepDue when a card really is inside a learning step', () => {
    store.commitReview(UID, DECK, 'bio-c2', { s: 1, d: 6, last: NOW, reps: 0, lapses: 1, state: 3, stepDue: NOW + 600_000 }, NOW);
    const payload = writes.find(w => w.kind === 'updateDoc')!.payload['cards.bio-c2'] as Record<string, unknown>;
    expect(payload.stepDue).toBe(NOW + 600_000);
  });

  it('refuses a card id that would corrupt the field path', () => {
    expect(() => store.saveCard(UID, DECK, 'bio.q6', NEW_CARD, NOW)).toThrow(/field path/i);
  });

  it('does nothing at all for a signed-out student', () => {
    store.saveCard(undefined, DECK, 'bio-c1', NEW_CARD, NOW);
    store.ensureDeck(undefined, DECK, NOW);
    expect(writes).toHaveLength(0);
  });

  it('keeps Demo Account reviews local and never contacts Firestore', async () => {
    const demoUid = 'demo-student';
    const memory = { s: 3, d: 5, last: NOW, reps: 1, lapses: 0, state: 2 as const };

    store.ensureDeck(demoUid, DECK, NOW);
    store.commitReview(demoUid, DECK, 'bio-c1', memory, NOW);
    store.saveExamDate(demoUid, DECK, Date.UTC(2027, 5, 9), NOW);

    expect(store.memoryFor(store.readLocal(demoUid, DECK), 'bio-c1')).toEqual(memory);
    await expect(store.fetchDeck(demoUid, DECK)).resolves.toBeNull();
    expect(writes).toHaveLength(0);
  });
});

describe('two devices converge instead of one clobbering the other', () => {
  it('keeps the more recent review of each card and loses nothing', () => {
    const local = {
      v: 1, updatedAt: NOW,
      cards: {
        shared: { s: 9, d: 5, last: NOW, reps: 3, lapses: 0, state: 2 as const },
        localOnly: { s: 2, d: 5, last: NOW - 1000, reps: 1, lapses: 0, state: 2 as const },
      },
    };
    const remote = {
      v: 1, updatedAt: NOW - 5000,
      cards: {
        shared: { s: 4, d: 5, last: NOW - 5000, reps: 2, lapses: 0, state: 2 as const },
        remoteOnly: { s: 7, d: 5, last: NOW - 4000, reps: 2, lapses: 0, state: 2 as const },
      },
    };
    const merged = store.mergeDecks(local, remote);
    expect(merged.cards.shared.s).toBe(9);
    expect(merged.cards.localOnly).toBeDefined();
    expect(merged.cards.remoteOnly).toBeDefined();
  });

  it('prefers the remote review when it is the newer one', () => {
    const local = { v: 1, updatedAt: 0, cards: { c: { s: 2, d: 5, last: NOW - 9000, reps: 1, lapses: 0, state: 2 as const } } };
    const remote = { v: 1, updatedAt: NOW, cards: { c: { s: 8, d: 5, last: NOW, reps: 4, lapses: 0, state: 2 as const } } };
    expect(store.mergeDecks(local, remote).cards.c.s).toBe(8);
  });

  it('returns local untouched when there is no remote deck yet', () => {
    const local = { v: 1, updatedAt: NOW, cards: { c: NEW_CARD } };
    expect(store.mergeDecks(local, null)).toBe(local);
  });

  it('carries the exam date from the remote deck, so the schedule cannot differ per device', () => {
    const exam = Date.UTC(2027, 5, 9);
    const merged = store.mergeDecks({ v: 1, updatedAt: 0, cards: {} }, { v: 1, updatedAt: NOW, cards: {}, examTs: exam });
    expect(merged.examTs).toBe(exam);
  });
});

describe('a level switch carries memory across', () => {
  it('seeds only cards the target deck does not already have', () => {
    store.commitReview(UID, 'biology-ordinary', 'existing', { s: 6, d: 5, last: NOW, reps: 2, lapses: 0, state: 2 }, NOW);
    writes.length = 0;
    const next = store.seedLevelSwitch(UID, 'biology-ordinary', {
      existing: { s: 1, d: 5, last: NOW, reps: 0, lapses: 0, state: 2 },
      fresh: { s: 18, d: 5, last: NOW, reps: 0, lapses: 0, state: 2 },
    }, NOW);
    expect(next.cards.existing.s).toBe(6);
    expect(next.cards.fresh.s).toBe(18);
    expect(writes.filter(w => w.kind === 'updateDoc')).toHaveLength(1);
  });
});

describe('Paper Trail flashcards fold in without being destroyed', () => {
  it('reads the legacy deck and converts each card to memory state', () => {
    localStorage.setItem('pt:cards:' + UID, JSON.stringify({
      a: { id: 'a', front: 'Q', back: 'A', intervalDays: 6, reps: 2, lapses: 0, addedTs: 1, lastTs: NOW - 6 * 86_400_000, stability: 6.4, difficulty: 5.2 },
      b: { id: 'b', front: 'Q2', back: 'A2', intervalDays: 0, reps: 0, lapses: 0, addedTs: 2, lastTs: 0 },
    }));
    const { cards, memories } = store.readLegacyFlashcards(UID);
    expect(cards).toHaveLength(2);
    expect(memories.a.s).toBeCloseTo(6.4);
    // Never reviewed, so it stays new rather than being given invented memory.
    expect(memories.b.state).toBe(0);
  });

  it('derives a stability for a scheduled card that never stored one', () => {
    localStorage.setItem('pt:cards:' + UID, JSON.stringify({
      c: { id: 'c', front: 'Q', back: 'A', intervalDays: 9, reps: 3, lapses: 1, addedTs: 1, lastTs: NOW - 9 * 86_400_000 },
    }));
    expect(store.readLegacyFlashcards(UID).memories.c.s).toBe(9);
  });

  it('skips a legacy id that is unsafe as a field path rather than corrupting the deck', () => {
    localStorage.setItem('pt:cards:' + UID, JSON.stringify({
      'bad.id': { id: 'bad.id', front: 'Q', back: 'A', intervalDays: 1, reps: 1, lapses: 0, addedTs: 1, lastTs: NOW },
    }));
    expect(Object.keys(store.readLegacyFlashcards(UID).memories)).toHaveLength(0);
  });

  it('is idempotent, so a repeated migration cannot double-apply', () => {
    expect(store.hasMigratedLegacy(UID)).toBe(false);
    store.markLegacyMigrated(UID);
    expect(store.hasMigratedLegacy(UID)).toBe(true);
  });

  it('leaves the legacy data in place — nothing is deleted on migration', () => {
    const raw = JSON.stringify({ a: { id: 'a', front: 'Q', back: 'A', intervalDays: 1, reps: 1, lapses: 0, addedTs: 1, lastTs: NOW } });
    localStorage.setItem('pt:cards:' + UID, raw);
    store.readLegacyFlashcards(UID);
    store.markLegacyMigrated(UID);
    expect(localStorage.getItem('pt:cards:' + UID)).toBe(raw);
  });
});

/* ------------------------------------------------------------------ rules ---- */

describe('the Firestore rules block exists', () => {
  it('declares /srs/{deckId} explicitly, because rules are non-hierarchical', () => {
    // Without this block every save AND reload is denied silently — the same
    // failure mode as audit blocker B3 on /sessions.
    const rules = readFileSync(resolve(__dirname, '..', 'firestore.rules'), 'utf8');
    expect(rules).toMatch(/match \/srs\/\{deckId\}/);
    const block = rules.slice(rules.indexOf('match /srs/{deckId}'));
    expect(block).toMatch(/allow read, write: if request\.auth != null && request\.auth\.uid == userId/);
  });
});
