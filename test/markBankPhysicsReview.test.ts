/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Physics paper-by-paper review: every reviewed sitting ships exactly the
 * tasks its ledger records, at the published tariffs, with every printed ask
 * carded (no exclusions, no open asks) and every figure it points at.
 *
 * The ledger (scripts/markbank/authoring/phys_review_<year>_<level>.py) is
 * checked against the SEC PDFs by phys_review.py, which also refuses a task
 * whose rows do not add up to the mark cells the scheme prints against them.
 * This pins what reached the shipped deck, so a later regeneration cannot
 * silently drop or reshape a reviewed sitting. One PINS row per sitting,
 * added when the sitting is written.
 */
import { describe, expect, it } from 'vitest';
import { CARDS as PHYS_HIGHER } from '../components/MarkBank/cards/physics/higher';
import { CARDS as PHYS_ORDINARY } from '../components/MarkBank/cards/physics/ordinary';
import audit from '../scripts/markbank/authored/physics-review-audit.json';
import exclusions from '../scripts/markbank/authoring/exclusions/physics.json';
import physicsFigures from '../components/MarkBank/figures-physics.json';
import sharedFigures from '../components/MarkBank/figures.json';
import { tariffReconciles } from '../types/markBank';

type Task = { id: string; questionRef: string; total: number; route: string | null; status: string;
  evidence?: string; cells?: { printed: string[]; sum: number | null; waiver?: string } };
type Sitting = { tasks: Task[]; cardCount: number; baseTaskCount: number; figures: string[];
  sources: Record<string, { sha256: string; pages: number }>;
  review?: { retained: Array<{ id: string; reason: string }>;
    withdrawn?: Record<string, { replacementId: string; reason: string }> };
  checks: { censusLeaves: number; censusLeavesClaimed: number; excluded: unknown[];
    openLeaves?: unknown[]; excludedLeaves?: unknown[] } };
const sittings = (audit as unknown as { sittings: Record<string, Sitting> }).sittings;

/** sitting -> [cards, tasks, census leaves, paper sha256, scheme sha256] */
const PINS: Record<string, [number, number, number, string, string]> = {
  '2026-ol': [125, 125, 120, 'ea4a0664bb1f14de76db44a5ef8095d76f98baef5266856ce949e29d8c99579e',
    'c7f984734a202b0fa5ef413b805d208c52cdb6bd3239a8513d4e8a6a6129f302'],
  '2026-hl': [136, 136, 107, 'fd1ff3286d201f396a282c38d4bf0f40adf71a1fca80d9111e763a4141a200d5',
    '228dec63cad7a6c8653dfb8b84ac29e908ec34277869cafea69e9481ad199463'],
  '2025-ol': [133, 133, 131, 'e25bb683dbff1c207dc4092b8e2fefb1dda2b1f2c9e294785c37cd99a605fffa',
    'bf8f2367d00286ae516dae6ded5ac311ec596df035f4cb53023decbb6dfc308e'],
  '2025-hl': [137, 137, 125, 'bd8d60f621d8d952e0aaefb054a5e064ea81d6fafcee0501bad5cf10b2ddbf27',
    'f0928d59d20bb0ea168dc17dcaf180b5c68389e8c9fecbf171a17ee90e21ffa2'],
  '2024-ol': [127, 127, 125, '60ef2b1b94f5c60c5589fd019b6ee590fdb0b6253eb2e77d891562255b74314b',
    '13577ca8546caf7e616343950217bebe589aeb71245348318f65c5622146ca51'],
  '2024-hl': [134, 134, 125, '5d9da3b660536b38a60d1494dbf8d83dc6e66ae56e53366d932647cfecc153fc',
    'df74412e93844119feb44c2770ec71490a57bfb80f360364be854fdc637eee5b'],
  '2023-ol': [121, 121, 119, 'd6dff89c7bd732fffcd14557a3d16d71cf17f516ca380ae7234af028997e4511',
    '8bd4e67afb47942be5dc8087860322d606b05a71009d89d2715a0f8fc7ab4b48'],
  '2023-hl': [128, 128, 114, 'aabc53d82a590d2c96556ee256a80f130cea2c2fea7b2b0bbae3f67065dab2a1',
    '9f610bf3f7ce51bdd7ad7b438cd0d5e92ee9cbd6aa10c3f961b081528aac8020'],
  '2022-ol': [127, 127, 125, '5246af9fbc8607914806b471a78ca0805a19cb3e3b038fce7ae45c4e99c9bbd5',
    '7b0ddda535e9dc2a1be382949bced3daf0abc0c3cce10578880a8724fd46fd8d'],
  '2022-hl': [128, 128, 118, '8b9b84d905e1d09691e115178f3d563116233928d075fcea9ffdafe387f26798',
    '7fd0309754396d9091b6dd2d15523d099a469c8d09078a43f145ef2c775e64b3'],
  '2021-hl': [123, 123, 121, '877a47fe07317037cee6147a35ec8648b91052b4748b3580dbf156c60e2c2d39',
    '7184b7194b479b4ee5129ea50847ff6f3a827df37a39f962fc5ccbe85a4b380d'],
  '2021-ol': [130, 130, 130, 'd31e6b959913c35b4700d5d1ec83b554dd1c3e00a7adbe642fdd032204145c1e',
    '228f3336be97ed97331f782625f8238c94b8bd19513519721cf261141c2f7686'],
};

type Card = (typeof PHYS_HIGHER)[number] & {
  rows: Array<{ verbatim?: string; contextNote?: string; marks?: number | null }>;
  figureKey?: string; questionFigureKey?: string;
};
const deck = [...PHYS_HIGHER, ...PHYS_ORDINARY] as unknown as Card[];
const figureKeys = new Set([...Object.keys(physicsFigures), ...Object.keys(sharedFigures)]);
const UNPRINTED = 'The scheme prints no answer for this part.';

describe('Physics — reviewed sittings', () => {
  it('pins every reviewed sitting, and reviews no sitting it does not pin', () => {
    expect(Object.keys(sittings).sort()).toEqual(Object.keys(PINS).sort());
  });

  it.each(Object.entries(PINS))('%s ships every reviewed task, and nothing else', (key, pin) => {
    const [cards, tasks, leaves, paperSha, schemeSha] = pin;
    const s = sittings[key];
    const [year, level] = key.split('-');
    const prefix = `phys-${year}-${level}-`;
    const shipped = deck.filter(card => card.id.startsWith(prefix));
    // A retained id the review withdrew onto its replacement does not ship.
    const withdrawn = new Set(Object.keys(s.review?.withdrawn ?? {}));
    const retained = new Set((s.review?.retained ?? []).map(r => r.id).filter(id => !withdrawn.has(id)));
    expect(s.cardCount).toBe(cards);
    expect(s.baseTaskCount).toBe(tasks);
    expect(s.sources.paper.sha256).toBe(paperSha);
    expect(s.sources.scheme.sha256).toBe(schemeSha);
    expect(new Set(shipped.map(card => card.id)))
      .toEqual(new Set([...s.tasks.map(task => task.id), ...retained]));
    // Every printed ask is carded: none open, none excluded.
    expect(s.checks.censusLeaves).toBe(leaves);
    expect(s.checks.censusLeavesClaimed).toBe(leaves);
    expect(s.checks.excluded).toEqual([]);
    expect(s.checks.openLeaves ?? []).toEqual([]);
    expect(s.checks.excludedLeaves ?? []).toEqual([]);
    expect(s.tasks.filter(task => task.status === 'excluded')).toEqual([]);
  });

  it.each(Object.keys(PINS))('%s carries each task at its published tariff', (key) => {
    const byId = new Map(deck.map(card => [card.id, card]));
    for (const task of sittings[key].tasks) {
      const card = byId.get(task.id)!;
      expect(card, task.id).toBeDefined();
      expect(card.totalMarks, task.id).toBe(task.total);
      expect(tariffReconciles(card as never), task.id).toBe(true);
      // The mark cells the scheme prints against the rows make the total, or
      // the ledger says why not.
      if (task.cells && task.cells.printed.length && !task.cells.waiver) {
        expect(task.cells.sum, task.id).toBe(task.total);
      }
    }
  });

  it.each(Object.keys(PINS))('%s shows an unprinted answer only as the one row, with its evidence', (key) => {
    const byId = new Map(deck.map(card => [card.id, card]));
    for (const task of sittings[key].tasks) {
      const card = byId.get(task.id)!;
      const unprinted = card.rows.filter(row => row.verbatim === UNPRINTED);
      if (!unprinted.length) continue;
      expect(card.rows, task.id).toHaveLength(1);
      expect(unprinted[0].contextNote, task.id).toBeTruthy();
      expect(task.evidence, task.id).toBeTruthy();
    }
  });

  it.each(Object.keys(PINS))('%s binds every figure it crops, from the manifest', (key) => {
    const [year, level] = key.split('-');
    const prefix = `phys-${year}-${level}-`;
    for (const card of deck.filter(c => c.id.startsWith(prefix))) {
      for (const k of [card.figureKey, card.questionFigureKey]) {
        if (k) expect(figureKeys.has(k), `${card.id}: ${k}`).toBe(true);
      }
    }
    for (const k of sittings[key].figures) expect(figureKeys.has(k), k).toBe(true);
  });

  it('keeps no exclusion for a reviewed sitting', () => {
    const reviewed = Object.keys(PINS).map(key => {
      const [year, level] = key.split('-');
      return `${year} ${level.toUpperCase()} `;
    });
    const stale = (exclusions as Array<{ ref: string }>).filter(e => reviewed.some(r => e.ref.startsWith(r)));
    expect(stale).toEqual([]);
  });
});
