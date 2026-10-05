import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';

// Resolve the same Admin SDK copy as the deployed functions, which install
// their dependencies separately from the web app. Only external I/O is mocked;
// the callable, authorization policy and island transaction reducer are real.
const sdk = await vi.hoisted(async () => {
  const { createRequire } = await import('node:module');
  const { dirname, resolve } = await import('node:path');
  const require = createRequire(resolve(process.cwd(), 'functions/package.json'));
  const adminRoot = resolve(dirname(require.resolve('firebase-admin')), '..');
  const admin = require(resolve(adminRoot, 'package.json'));
  return {
    authPath: resolve(adminRoot, admin.exports['./auth'].import),
    firestorePath: resolve(adminRoot, admin.exports['./firestore'].import),
    getUser: vi.fn(),
    getProfile: vi.fn(),
    getProgress: vi.fn(),
    update: vi.fn(),
    transaction: vi.fn(),
  };
});
vi.mock(sdk.authPath, () => ({ getAuth: () => ({ getUser: sdk.getUser }) }));
vi.mock(sdk.firestorePath, () => ({
  getFirestore: () => ({
    collection: () => ({ doc: () => ({ get: sdk.getProfile }) }),
    doc: (path: string) => ({ path }),
    runTransaction: sdk.transaction,
  }),
  FieldValue: { delete: () => 'delete-old-island' },
}));

import { updatePaperIsland } from '../functions/src/paperIsland';
import type { PaperProgress } from '../functions/src/paperIslandModel';

const now = Date.parse('2026-09-13T18:00:00Z');
const signedInYesterday = Math.floor(now / 1000) - 86_400;
type Request = Parameters<typeof updatePaperIsland.run>[0];
const request = (data: unknown): Request => ({
  auth: { uid: 'journey-auth-test', token: { auth_time: signedInYesterday } },
  data,
} as Request);

describe('Journey callable session authorization', () => {
  let progress: PaperProgress;
  beforeEach(() => {
    vi.useFakeTimers();
    vi.setSystemTime(now);
    vi.clearAllMocks();
    progress = { pointsData: { totalEarned: 300, totalSpent: 0 } };
    sdk.getUser.mockResolvedValue({
      disabled: false,
      tokensValidAfterTime: new Date(now - 7 * 86_400_000).toUTCString(),
    });
    sdk.getProfile.mockResolvedValue({ exists: true, data: () => ({}) });
    sdk.getProgress.mockImplementation(async () => ({ exists: true, data: () => progress }));
    sdk.update.mockImplementation((_ref, update) => {
      progress = {
        ...progress,
        paperIsland: update.paperIsland,
        pointsData: { ...progress.pointsData, totalSpent: update['pointsData.totalSpent'] },
      };
    });
    sdk.transaction.mockImplementation(async work => work({ get: sdk.getProgress, update: sdk.update }));
  });
  afterEach(() => vi.useRealTimers());

  it('opens, places and undoes with a valid session signed in yesterday', async () => {
    const opened = await updatePaperIsland.run(request({ action: 'open' }));
    expect(opened.state.tiles).toHaveLength(7);
    const placed = await updatePaperIsland.run(request({
      action: 'place', kind: 'water', q: -2, r: 0,
      revision: opened.state.revision, requestId: 'session-place-001',
    }));
    expect(placed.totalSpent).toBe(90);
    const undone = await updatePaperIsland.run(request({
      action: 'undo', revision: placed.state.revision, requestId: 'session-undo-0001',
    }));
    expect(undone.totalSpent).toBe(0);
    expect(undone.state.tiles).toEqual(opened.state.tiles);
    expect(sdk.getUser).toHaveBeenCalledWith('journey-auth-test');
  });

  it('validates and saves a visitor gift and Wonder placement through the authenticated transaction', async () => {
    await updatePaperIsland.run(request({ action:'open' }));
    const met=await updatePaperIsland.run(request({ action:'meetVisitor',id:'wisp',uid:'another-student' }));
    expect(met.state.metVisitors).toEqual(['wisp']);
    const writes=sdk.update.mock.calls.length;
    await expect(updatePaperIsland.run(request({ action:'claimVisitor',id:'wisp' }))).rejects.toMatchObject({code:'failed-precondition'});
    expect(sdk.update).toHaveBeenCalledTimes(writes);
    const paired=await updatePaperIsland.run(request({ action:'place',kind:'water',q:-1,r:-1,revision:met.state.revision,requestId:'visitor-wish-place-001' }));
    expect(paired.totalSpent).toBe(90);
    const gift=await updatePaperIsland.run(request({ action:'claimVisitor',id:'wisp' }));
    const retry=await updatePaperIsland.run(request({ action:'claimVisitor',id:'wisp' }));
    expect(retry.state.claimedVisitors).toEqual(['wisp']);expect(retry.totalSpent).toBe(90);
    const placed=await updatePaperIsland.run(request({ action:'placeWonder',id:'wisp',q:-2,r:-1,revision:gift.state.revision,requestId:'visitor-wonder-place-001' }));
    expect(placed.state.tiles.filter(tile=>tile.wonderId==='wisp')).toHaveLength(1);
    expect(placed.totalSpent).toBe(90);
    expect(sdk.update.mock.calls.every(([ref])=>ref.path==='progress/journey-auth-test')).toBe(true);
  });

  it.each(['meetVisitor','claimVisitor','placeWonder'])('requires authentication for %s',async action=>{
    await expect(updatePaperIsland.run({data:{action,id:'wisp',q:-2,r:-1,revision:0,requestId:'visitor-unauth-001'}} as Request)).rejects.toMatchObject({code:'unauthenticated'});
    expect(sdk.transaction).not.toHaveBeenCalled();
  });

  it('rejects signed-out requests without touching the island', async () => {
    await expect(updatePaperIsland.run({ data: { action: 'open' } } as Request))
      .rejects.toMatchObject({ code: 'unauthenticated' });
    expect(sdk.transaction).not.toHaveBeenCalled();
  });

  it('still rejects revoked sessions before reading or writing progress', async () => {
    sdk.getUser.mockResolvedValue({ disabled: false, tokensValidAfterTime: new Date(now).toUTCString() });
    await expect(updatePaperIsland.run(request({ action: 'open' })))
      .rejects.toMatchObject({ code: 'unauthenticated' });
    expect(sdk.transaction).not.toHaveBeenCalled();
  });

  it.each([
    ['disabled Auth account', { disabled: true }, { exists: true, data: () => ({}) }],
    ['disabled profile', { disabled: false }, { exists: true, data: () => ({ accountDisabled: true }) }],
    ['missing profile', { disabled: false }, { exists: false, data: () => ({}) }],
  ])('still rejects a %s', async (_name, auth, profile) => {
    sdk.getUser.mockResolvedValue(auth);
    sdk.getProfile.mockResolvedValue(profile);
    await expect(updatePaperIsland.run(request({ action: 'open' })))
      .rejects.toMatchObject({ code: 'permission-denied' });
    expect(sdk.transaction).not.toHaveBeenCalled();
  });

  it('still rejects sessions ended by the account profile', async () => {
    sdk.getProfile.mockResolvedValue({ exists: true, data: () => ({ sessionValidAfterSeconds: signedInYesterday }) });
    await expect(updatePaperIsland.run(request({ action: 'open' })))
      .rejects.toMatchObject({ code: 'unauthenticated' });
    expect(sdk.transaction).not.toHaveBeenCalled();
  });
});
