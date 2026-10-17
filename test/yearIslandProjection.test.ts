/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Year islands, server side: what a classmate can read about a student's
 * island, who never gets a projection, and when the triggers rebuild it.
 * Alex, 17 Oct 2026: "Allow students to see other students in their school
 * year island, i.e. Marino 5th year."
 */
import { describe, expect, it } from 'vitest';
import {
  MAX_PUBLIC_TILES,
  planYearIsland,
  progressProjectionKey,
  publicTiles,
  userProjectionKey,
} from '../functions/src/islandProjection';
import { syncAfterProgressWrite, syncAfterUserWrite, syncYearIsland as realSync } from '../functions/src/islandProjectionSync';
import { createPaperIsland, type PaperIsland } from '../functions/src/paperIslandModel';

const student = (extra: Record<string, unknown> = {}) => ({
  name: 'Aoife Byrne Kelly',
  avatar: 'star-crew:reader',
  school: 'marino',
  yearGroup: '5th',
  curriculumLevel: 'senior',
  ...extra,
});
const island = (): PaperIsland => ({
  ...createPaperIsland(),
  tiles: [
    ...createPaperIsland().tiles,
    { id: 'bought-tile-request-0001', q: -2, r: 0, kind: 'water', appearance: 'capybara', cost: 120, edge: { variant: 'small-bite', seed: 99 } },
    { id: 'wonder-request-00000001', q: 2, r: -1, kind: 'meadow', wonderId: 'luma', cost: 0, edge: { variant: 'long-nick', seed: 7 } },
  ],
  kept: ['ember-wyrm'],
  claimedCaches: ['far-treasure'],
  metVisitors: ['luma'],
  claimedVisitors: ['luma'],
  credits: 4,
  rewardedRank: 3,
  revision: 9,
  lastRequest: 'wonder-request-00000001',
  undo: { tileId: 'wonder-request-00000001', cost: 0, usedCredit: false },
});
const progress = (extra: Record<string, unknown> = {}) => ({
  paperIsland: island(),
  pointsData: { totalEarned: 2400, totalSpent: 120 },
  northStar: { category: 'college', statement: 'I want to study veterinary medicine' },
  studySessions: [{ subject: 'Biology', minutes: 45 }],
  subjectProfile: { yearGroup: '5th', subjects: [{ subjectName: 'Biology' }] },
  ...extra,
});

describe('the classmate-visible projection', () => {
  it('carries a first name, avatar, school, year and the drawn island, and nothing else', () => {
    const { projection } = planYearIsland(student(), progress());
    expect(projection).not.toBeNull();
    expect(Object.keys(projection!).sort()).toEqual(['avatar', 'name', 'schemaVersion', 'school', 'tileCount', 'tiles', 'yearGroup']);
    expect(projection).toMatchObject({ schemaVersion: 2, name: 'Aoife', avatar: 'star-crew:reader', school: 'marino', yearGroup: '5th', tileCount: 9 });
    for (const tile of projection!.tiles)
      expect(Object.keys(tile).every(key => ['q', 'r', 'kind', 'edge', 'appearance', 'wonderId'].includes(key))).toBe(true);
    expect(projection!.tiles).toContainEqual({ q: -2, r: 0, kind: 'water', appearance: 'capybara', edge: { variant: 'small-bite', seed: 99 } });
    expect(projection!.tiles).toContainEqual({ q: 2, r: -1, kind: 'meadow', wonderId: 'luma', edge: { variant: 'long-nick', seed: 7 } });
    const json = JSON.stringify(projection);
    for (const secret of ['Byrne', 'veterinary', 'college', 'Biology', '2400', 'cost', 'bought-tile', 'credits', 'ember-wyrm', 'far-treasure', 'curriculumLevel'])
      expect(json).not.toContain(secret);
  });

  it('orders tiles nearest home first, so the order says nothing about when they were placed', () => {
    const { projection } = planYearIsland(student(), progress());
    expect(projection!.tiles[0]).toMatchObject({ q: 0, r: 0, kind: 'home' });
    const distances = projection!.tiles.map(t => Math.max(Math.abs(t.q), Math.abs(t.r), Math.abs(t.q + t.r)));
    expect(distances).toEqual([...distances].sort((a, b) => a - b));
  });

  it('caps a huge island at the core and still reports the full tile count', () => {
    const tiles = Array.from({ length: 900 }, (_, i) => ({ q: i % 40 - 20, r: Math.floor(i / 40) - 11, kind: 'meadow' }));
    const result = publicTiles(tiles);
    expect(result.tiles).toHaveLength(MAX_PUBLIC_TILES);
    expect(result.tileCount).toBe(900);
  });

  it('drops malformed, unknown and duplicate tiles and invalid ink stamps', () => {
    const result = publicTiles([
      { q: 0, r: 0, kind: 'home', edge: { variant: 'forged', seed: 1 } },
      { q: 0, r: 0, kind: 'meadow' },
      { q: 1.5, r: 0, kind: 'meadow' },
      { q: 9999, r: 0, kind: 'meadow' },
      { q: 1, r: 0, kind: 'not-a-tile' },
      { q: 2, r: 0, kind: 'meadow', wonderId: 'stranger', appearance: 'capybara' },
      'nonsense',
    ]);
    expect(result.tiles).toEqual([{ q: 0, r: 0, kind: 'home' }, { q: 2, r: 0, kind: 'meadow' }]);
  });

  it('uses the users doc year first and falls back to the onboarding profile', () => {
    expect(planYearIsland(student({ yearGroup: '6th' }), progress()).projection?.yearGroup).toBe('6th');
    expect(planYearIsland(student({ yearGroup: undefined }), progress()).projection?.yearGroup).toBe('5th');
  });

  it.each([
    ['a guidance counsellor', student({ role: 'gc' }), progress(), 'staff'],
    ['teaching staff', student({ role: 'staff' }), progress(), 'staff'],
    ['an admin', student({ isAdmin: true }), progress(), 'staff'],
    ['a disabled account', student({ accountDisabled: true }), progress(), 'disabled'],
    ['a student who switched sharing off', student({ islandVisibility: 'hidden' }), progress(), 'hidden'],
    ['a student with no school', student({ school: undefined }), progress(), 'no-school'],
    ['a graduate', student({ yearGroup: 'graduated' }), progress(), 'graduated'],
    ['a student with no year anywhere', student({ yearGroup: undefined }), progress({ subjectProfile: {} }), 'no-year'],
    ['a student who never opened Journey', student(), progress({ paperIsland: undefined }), 'no-island'],
    ['a legacy island only', student(), progress({ paperIsland: undefined, islandState: { placements: [] } }), 'no-island'],
    ['a deleted profile', undefined, progress(), 'no-user'],
    ['deleted progress', student(), undefined, 'no-progress'],
  ])('never projects %s', (_label, user, data, reason) => {
    expect(planYearIsland(user, data)).toEqual({ projection: null, excluded: reason });
  });

  it('shares by default and only an explicit "hidden" hides', () => {
    expect(planYearIsland(student({ islandVisibility: 'year' }), progress()).projection).not.toBeNull();
    expect(planYearIsland(student({ islandVisibility: 'anything-else' }), progress()).projection).not.toBeNull();
  });
});

describe('what makes the triggers rebuild', () => {
  it('ignores progress writes that cannot change the island, and notices ones that can', () => {
    const base = progress();
    expect(progressProjectionKey({ ...base, pointsData: { totalEarned: 9999, totalSpent: 0 }, studySessions: [] })).toBe(progressProjectionKey(base));
    expect(progressProjectionKey({ ...base, paperIsland: { ...island(), credits: 0, revision: 99, lastRequest: 'x' } })).toBe(progressProjectionKey(base));
    expect(progressProjectionKey({ ...base, paperIsland: { ...island(), tiles: island().tiles.slice(1) } })).not.toBe(progressProjectionKey(base));
    expect(progressProjectionKey({ ...base, subjectProfile: { yearGroup: '6th' } })).not.toBe(progressProjectionKey(base));
  });

  it('ignores profile writes that cannot change the island, and notices ones that can', () => {
    const base = student();
    expect(userProjectionKey({ ...base, curriculumLevel: 'junior', legalAcceptance: { at: 1 } })).toBe(userProjectionKey(base));
    for (const change of [{ islandVisibility: 'hidden' }, { yearGroup: '6th' }, { name: 'Ciara' }, { avatar: 'x' }, { role: 'gc' }, { accountDisabled: true }])
      expect(userProjectionKey({ ...base, ...change })).not.toBe(userProjectionKey(base));
  });
});

type Doc = Record<string, unknown> | undefined;
function fakeDb(docs: { users?: Doc; progress?: Doc; islandPublic?: Doc }) {
  const store = { ...docs };
  const writes: string[] = [];
  const masks: string[][] = [];
  const ref = (collection: keyof typeof store) => ({ collection });
  const getAll = async (...args: unknown[]) => {
    const options = args.at(-1) as { fieldMask: string[] };
    masks.push(options.fieldMask);
    return (args.slice(0, -1) as { collection: keyof typeof store }[]).map(r => ({
      exists: store[r.collection] !== undefined,
      data: () => store[r.collection],
    }));
  };
  const db = {
    collection: (name: keyof typeof store) => ({ doc: () => ref(name) }),
    getAll,
    runTransaction: async (work: (tx: unknown) => Promise<unknown>) => work({
      getAll,
      set: (r: { collection: keyof typeof store }, data: Doc) => { writes.push(`set ${r.collection}`); store[r.collection] = data; },
      delete: (r: { collection: keyof typeof store }) => { writes.push(`delete ${r.collection}`); store[r.collection] = undefined; },
    }),
  };
  return { db: db as unknown as Parameters<typeof realSync>[0], store, writes, masks };
}

describe('syncYearIsland', () => {
  it('writes a missing projection, then leaves an identical one alone', async () => {
    const fake = fakeDb({ users: student(), progress: progress() });
    expect(await realSync(fake.db, 'uid-1')).toEqual({ action: 'written' });
    expect(fake.store.islandPublic).toMatchObject({ schemaVersion: 2, yearGroup: '5th' });
    expect(await realSync(fake.db, 'uid-1')).toEqual({ action: 'unchanged' });
    expect(fake.writes).toEqual(['set islandPublic']);
  });

  it('deletes the projection the moment its owner hides it', async () => {
    const fake = fakeDb({ users: student({ islandVisibility: 'hidden' }), progress: progress(), islandPublic: { schemaVersion: 2 } });
    expect(await realSync(fake.db, 'uid-1')).toEqual({ action: 'deleted', excluded: 'hidden' });
    expect(fake.store.islandPublic).toBeUndefined();
  });

  it('replaces a schema 1, whole-school projection outright', async () => {
    const legacy = { name: 'Aoife', avatar: 'A', school: 'marino', category: 'college', placements: [], score: 3, schemaVersion: 1 };
    const fake = fakeDb({ users: student(), progress: progress(), islandPublic: legacy });
    expect(await realSync(fake.db, 'uid-1')).toEqual({ action: 'written' });
    expect(fake.store.islandPublic).not.toHaveProperty('category');
    expect(fake.store.islandPublic).not.toHaveProperty('score');
  });

  it('deletes a schema 1 projection whose owner has no current island', async () => {
    const fake = fakeDb({ users: student(), progress: progress({ paperIsland: undefined }), islandPublic: { schemaVersion: 1 } });
    expect(await realSync(fake.db, 'uid-1')).toEqual({ action: 'deleted', excluded: 'no-island' });
  });

  it('reads only the fields it needs, so study data never leaves Firestore', async () => {
    const fake = fakeDb({ users: student(), progress: progress() });
    await realSync(fake.db, 'uid-1');
    const mask = fake.masks[0];
    expect(mask).toEqual(expect.arrayContaining(['paperIsland.tiles', 'paperIsland.version', 'subjectProfile.yearGroup', 'islandVisibility']));
    for (const field of ['pointsData', 'northStar', 'studySessions', 'paperIsland', 'subjectProfile']) expect(mask).not.toContain(field);
    expect(new Set(mask).size).toBe(mask.length);
  });

  it('reports without writing in a dry run', async () => {
    const fake = fakeDb({ users: student(), progress: progress() });
    expect(await realSync(fake.db, 'uid-1', { dryRun: true })).toEqual({ action: 'written' });
    expect(fake.writes).toEqual([]);
    expect(fake.store.islandPublic).toBeUndefined();
  });
});

describe('the trigger decisions (onProgressWritten / onUserWritten)', () => {
  it('does no reads for a progress write that only moves points or study data', async () => {
    const fake = fakeDb({ users: student(), progress: progress() });
    expect(await syncAfterProgressWrite(fake.db, 'uid-1', progress(), progress({ pointsData: { totalEarned: 2500, totalSpent: 120 } }))).toBeNull();
    expect(fake.masks).toHaveLength(0);
  });

  it('syncs when the island changes, when progress is created, and when it is deleted', async () => {
    const changed = fakeDb({ users: student(), progress: progress() });
    expect(await syncAfterProgressWrite(changed.db, 'uid-1', progress(), progress({ paperIsland: { ...island(), tiles: island().tiles.slice(0, 7) } }))).toEqual({ action: 'written' });
    const created = fakeDb({ users: student(), progress: progress() });
    expect(await syncAfterProgressWrite(created.db, 'uid-1', undefined, progress())).toEqual({ action: 'written' });
    const deleted = fakeDb({ users: student(), islandPublic: { schemaVersion: 2 } });
    expect(await syncAfterProgressWrite(deleted.db, 'uid-1', progress(), undefined)).toEqual({ action: 'deleted', excluded: 'no-progress' });
  });

  it('syncs on the sharing switch, a year change or a deleted profile, not on unrelated profile writes', async () => {
    const fake = fakeDb({ users: student({ islandVisibility: 'hidden' }), progress: progress(), islandPublic: { schemaVersion: 2 } });
    expect(await syncAfterUserWrite(fake.db, 'uid-1', student(), student({ curriculumLevel: 'junior' }))).toBeNull();
    expect(fake.masks).toHaveLength(0);
    expect(await syncAfterUserWrite(fake.db, 'uid-1', student(), student({ islandVisibility: 'hidden' }))).toEqual({ action: 'deleted', excluded: 'hidden' });
    const moved = fakeDb({ users: student({ yearGroup: '6th' }), progress: progress() });
    expect(await syncAfterUserWrite(moved.db, 'uid-1', student(), student({ yearGroup: '6th' }))).toEqual({ action: 'written' });
    expect(moved.store.islandPublic).toMatchObject({ yearGroup: '6th' });
    const gone = fakeDb({ progress: progress(), islandPublic: { schemaVersion: 2 } });
    expect(await syncAfterUserWrite(gone.db, 'uid-1', student(), undefined)).toEqual({ action: 'deleted', excluded: 'no-user' });
  });
});
