/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The single model's two automatic checks (plan section 5, M5), plus the model's own record:
 *   1. every Mark Bank card reaches a Topic Atlas question under the same topic;
 *   2. every Topic Atlas question in scope has a card;
 *   3. data/atlasModel/<subject>.json is what scripts/atlas-model/askTopics.ts derives today (never hand-edited).
 * Both checks run across every subject. They gate the subjects switched on in the model (MODEL_SUBJECTS): their
 * cards that reach no Atlas question (the Atlas does not list the printed question yet) and their Atlas questions
 * without a card are listed in test/fixtures/atlasModelKnownMisses.json, which may shrink and never grow (a new miss
 * fails, and so does a listed miss that has been fixed and not taken off the list). Subjects not yet switched on are measured and reported, not
 * gated, so another lane adding cards to them is never blocked here; each joins the gate when it is switched on.
 * To rewrite the list after a fix or a switch-on, run this file with ATLAS_MISSES_WRITE=1: it refuses to grow the
 * list of a subject already on it, and adds a newly switched-on subject.
 */
import { describe, expect, it } from 'vitest';
import fs from 'node:fs';
import path from 'node:path';
import { runAtlasModelChecks, type CheckResult } from '../scripts/atlas-model/checks';
import { deriveAskTopics, MODEL_SUBJECTS } from '../scripts/atlas-model/askTopics';
import headings from '../data/atlasModel/headings.json';

const FIXTURE = path.join(__dirname, 'fixtures', 'atlasModelKnownMisses.json');
// One-off misses the coordinator ruled on (id, reason, owner each): the only ids the list may take beyond a newly
// switched-on subject's own, and each must still miss, so the file only shrinks.
interface Ruled { entries: Array<{ subject: string; kind: 'card' | 'question'; id: string; reason: string; owner: string; ruling: string }> }
const RULED: Ruled = JSON.parse(fs.readFileSync(path.join(__dirname, 'fixtures', 'atlasModelRuledMisses.json'), 'utf8'));
const ruledKey = new Set(RULED.entries.map(e => `${e.subject}: ${e.id}`));
interface Known { note: string; cards: Record<string, string[]>; questions: CheckResult['questions'] }
const known: Known | null = fs.existsSync(FIXTURE) ? JSON.parse(fs.readFileSync(FIXTURE, 'utf8')) : null;

/** The Atlas subjects whose questions the model gates (History's Later and Early Modern lists both). */
const MODEL_ATLAS_IDS = new Set((headings as { subjects: Array<{ subjectId: string; atlasIds: string[] }> }).subjects
  .filter(s => MODEL_SUBJECTS.includes(s.subjectId)).flatMap(s => s.atlasIds));
const gated = (questions: CheckResult['questions']): CheckResult['questions'] =>
  Object.fromEntries([...MODEL_ATLAS_IDS].sort().map(atlasId => [atlasId, questions[atlasId] ?? []]));

const gatedCards = (cards: CheckResult['cards']): Record<string, string[]> =>
  Object.fromEntries([...MODEL_SUBJECTS].sort().map(s => [s, (Object.values(cards[s] ?? {}).flat() as string[]).sort()]));

function compare(actual: Record<string, string[]>, listed: Record<string, string[]>) {
  const grew: string[] = []; const fixed: string[] = [];
  for (const [s, keys] of Object.entries(actual)) for (const k of keys) if (!listed[s]?.includes(k)) grew.push(`${s}: ${k}`);
  for (const [s, keys] of Object.entries(listed)) for (const k of keys) if (!actual[s]?.includes(k)) fixed.push(`${s}: ${k}`);
  return { grew, fixed };
}

describe('the single model: Mark Bank and Topic Atlas, both ways', () => {
  let result: CheckResult;
  it('runs both checks across every subject', async () => {
    result = await runAtlasModelChecks();
    const ungatedCards = Object.entries(result.cards).filter(([s]) => !MODEL_SUBJECTS.includes(s))
      .reduce((n, [, reasons]) => n + Object.values(reasons).flat().length, 0);
    const ungatedQuestions = Object.entries(result.questions).filter(([s]) => !MODEL_ATLAS_IDS.has(s))
      .reduce((n, [, keys]) => n + keys.length, 0);
    console.info(`[atlas model] not yet switched on: ${ungatedCards} cards miss the Atlas, ${ungatedQuestions} Atlas questions have no card`);
    if (process.env.ATLAS_MISSES_WRITE) {
      const next = { cards: gatedCards(result.cards), questions: gated(result.questions) };
      const grows = known && [
        ...compare(next.cards, known.cards ?? {}).grew.filter(k => k.split(': ')[0] in (known.cards ?? {}) && !ruledKey.has(k)),
        ...compare(next.questions, known.questions).grew.filter(k => k.split(': ')[0] in known.questions && !ruledKey.has(k)),
      ];
      if (grows && grows.length) throw new Error(`refusing to grow the known-miss list: ${grows.slice(0, 5).join('; ')}`);
      fs.writeFileSync(FIXTURE, `${JSON.stringify({
        note: 'Shrink-only (test/atlasModelChecks.test.ts), for the subjects switched on in the single model. cards: Mark Bank subject -> cards that reach no Topic Atlas question (the Atlas does not list their printed question). questions: Atlas subject -> in-scope Atlas questions (year|level|booklet|n) with no card.',
        ...next,
      }, null, 1)}\n`);
    }
    expect(result.totals.cards).toBeGreaterThan(50000);
  }, 900_000);

  it('every card of a switched-on subject reaches a Topic Atlas question under the same topic (known misses may only shrink)', () => {
    expect(known, 'test/fixtures/atlasModelKnownMisses.json is missing').not.toBeNull();
    for (const subject of MODEL_SUBJECTS) expect(subject in (known!.cards ?? {}), `${subject}: run with ATLAS_MISSES_WRITE=1`).toBe(true);
    // A switched-on subject's card can miss only because the Atlas does not list its paper or question yet.
    for (const subject of MODEL_SUBJECTS) {
      expect(Object.keys(result.cards[subject] ?? {}).filter(reason => reason !== 'no-atlas-question' && reason !== 'no-atlas-paper'), subject).toEqual([]);
    }
    const { grew, fixed } = compare(gatedCards(result.cards), known!.cards);
    expect(grew, 'cards that newly fail to reach the Atlas').toEqual([]);
    expect(fixed, 'fixed: take these cards off the known-miss list (ATLAS_MISSES_WRITE=1)').toEqual([]);
  });

  it('every Topic Atlas question of a switched-on subject has a card (known misses may only shrink)', () => {
    expect(known, 'test/fixtures/atlasModelKnownMisses.json is missing').not.toBeNull();
    for (const atlasId of MODEL_ATLAS_IDS) expect(atlasId in known!.questions, `${atlasId}: run with ATLAS_MISSES_WRITE=1`).toBe(true);
    const { grew, fixed } = compare(gated(result.questions), known!.questions);
    expect(grew, 'Atlas questions that newly have no card').toEqual([]);
    expect(fixed, 'fixed: take these questions off the known-miss list (ATLAS_MISSES_WRITE=1)').toEqual([]);
  });

  it('every ruled one-off miss still misses and is on the known-miss list (the ruled list only shrinks)', () => {
    const missing = new Set([
      ...Object.entries(gatedCards(result.cards)).flatMap(([s, ids]) => ids.map(id => `${s}: ${id}`)),
      ...Object.entries(gated(result.questions)).flatMap(([s, keys]) => keys.map(k => `${s}: ${k}`)),
    ]);
    const listed = new Set([
      ...Object.entries(known!.cards ?? {}).flatMap(([s, ids]) => ids.map(id => `${s}: ${id}`)),
      ...Object.entries(known!.questions).flatMap(([s, keys]) => keys.map(k => `${s}: ${k}`)),
    ]);
    for (const e of RULED.entries) {
      expect(e.reason && e.owner && e.ruling, `${e.subject}: ${e.id} needs a reason, an owner and a ruling`).toBeTruthy();
    }
    expect([...ruledKey].filter(k => !missing.has(k)), 'cleared: take these off atlasModelRuledMisses.json and the known-miss list').toEqual([]);
    expect([...ruledKey].filter(k => !listed.has(k)), 'ruled but not on the known-miss list (ATLAS_MISSES_WRITE=1)').toEqual([]);
  });

  it('the committed topic record of every switched-on subject is the one the model derives today', async () => {
    for (const subject of MODEL_SUBJECTS) {
      const { file, problems } = await deriveAskTopics(subject);
      expect(problems, subject).toEqual([]);
      const committed = JSON.parse(fs.readFileSync(path.join(__dirname, '..', 'data', 'atlasModel', `${subject}.json`), 'utf8'));
      expect(committed, `${subject}: run node scripts/atlas-model/build-ask-topics.mjs ${subject}`).toEqual(JSON.parse(JSON.stringify(file)));
    }
  }, 300_000);
});
