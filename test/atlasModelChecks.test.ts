/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The single model's two automatic checks across every subject (plan section 5, M5), plus the model's own record:
 *   1. every Mark Bank card reaches a Topic Atlas question under the same topic;
 *   2. every Topic Atlas question in scope has a card;
 *   3. data/atlasModel/<subject>.json is what scripts/atlas-model/askTopics.ts derives today (never hand-edited).
 * Today's misses are listed in test/fixtures/atlasModelKnownMisses.json. The list may shrink and never grow: a new
 * miss fails, and so does a listed miss that has been fixed and not taken off the list. To shrink the file after a
 * fix, run this file with ATLAS_MISSES_WRITE=1; it refuses to write a list that grows.
 */
import { describe, expect, it } from 'vitest';
import fs from 'node:fs';
import path from 'node:path';
import { runAtlasModelChecks, type CheckResult } from '../scripts/atlas-model/checks';
import { deriveAskTopics, MODEL_SUBJECTS } from '../scripts/atlas-model/askTopics';

const FIXTURE = path.join(__dirname, 'fixtures', 'atlasModelKnownMisses.json');
interface Known { note: string; cards: CheckResult['cards']; questions: CheckResult['questions'] }
const known: Known | null = fs.existsSync(FIXTURE) ? JSON.parse(fs.readFileSync(FIXTURE, 'utf8')) : null;

const cardIds = (m: CheckResult['cards']) => new Map(Object.entries(m).map(([s, reasons]) => [s, new Set(Object.values(reasons).flat() as string[])]));
const questionKeys = (m: CheckResult['questions']) => new Map(Object.entries(m).map(([s, keys]) => [s, new Set(keys)]));
function compare(actual: Map<string, Set<string>>, listed: Map<string, Set<string>>) {
  const grew: string[] = []; const fixed: string[] = [];
  for (const [s, ids] of actual) for (const id of ids) if (!listed.get(s)?.has(id)) grew.push(`${s}: ${id}`);
  for (const [s, ids] of listed) for (const id of ids) if (!actual.get(s)?.has(id)) fixed.push(`${s}: ${id}`);
  return { grew, fixed };
}

describe('the single model: Mark Bank and Topic Atlas, both ways', () => {
  let result: CheckResult;
  it('runs both checks across every subject', async () => {
    result = await runAtlasModelChecks();
    if (process.env.ATLAS_MISSES_WRITE) {
      const grows = known && (compare(cardIds(result.cards), cardIds(known.cards)).grew.length
        || compare(questionKeys(result.questions), questionKeys(known.questions)).grew.length);
      if (grows) throw new Error('refusing to write a known-miss list that grows');
      fs.writeFileSync(FIXTURE, `${JSON.stringify({
        note: 'Shrink-only (test/atlasModelChecks.test.ts). cards: Mark Bank subject -> reason -> cards that do not reach a Topic Atlas question under the same topic. questions: Atlas subject -> in-scope Atlas questions (year|level|booklet|n) with no card.',
        cards: result.cards, questions: result.questions,
      }, null, 1)}\n`);
    }
    expect(result.totals.cards).toBeGreaterThan(50000);
  }, 900_000);

  it('every card reaches a Topic Atlas question under the same topic (known misses may only shrink)', () => {
    expect(known, 'test/fixtures/atlasModelKnownMisses.json is missing').not.toBeNull();
    const { grew, fixed } = compare(cardIds(result.cards), cardIds(known!.cards));
    expect(grew, 'cards that newly fail to reach the Atlas under their topic').toEqual([]);
    expect(fixed, 'fixed: take these cards off the known-miss list (ATLAS_MISSES_WRITE=1)').toEqual([]);
  });

  it('every Topic Atlas question in scope has a card (known misses may only shrink)', () => {
    const { grew, fixed } = compare(questionKeys(result.questions), questionKeys(known!.questions));
    expect(grew, 'Atlas questions that newly have no card').toEqual([]);
    expect(fixed, 'fixed: take these questions off the known-miss list (ATLAS_MISSES_WRITE=1)').toEqual([]);
  });

  it('every subject in the model has no miss at all on its own cards', () => {
    for (const subject of MODEL_SUBJECTS) expect(result.cards[subject] ?? {}, subject).toEqual({});
  });

  it('the committed topic record is the one the model derives today', async () => {
    for (const subject of MODEL_SUBJECTS) {
      const { file, problems } = await deriveAskTopics(subject);
      expect(problems, subject).toEqual([]);
      const committed = JSON.parse(fs.readFileSync(path.join(__dirname, '..', 'data', 'atlasModel', `${subject}.json`), 'utf8'));
      expect(committed, `${subject}: run node scripts/atlas-model/build-ask-topics.mjs`).toEqual(JSON.parse(JSON.stringify(file)));
    }
  }, 300_000);
});
