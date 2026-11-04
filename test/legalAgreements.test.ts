import { beforeEach, describe, expect, test, vi } from 'vitest';
import { PRIVACY_POLICY_VERSION, TERMS_VERSION } from '../functions/src/legalAgreementPolicy';

const mocks = vi.hoisted(() => ({ get: vi.fn(), set: vi.fn(), update: vi.fn(), verify: vi.fn(), timestamp: { serverTimestamp: true } }));
import { saveLegalAgreement } from '../functions/src/legalAgreements';
const invoke = (request: Record<string, unknown>) => saveLegalAgreement(request as never, {
  getDb: (() => ({ collection: (collection: string) => ({ doc: (id: string) => ({ path: `${collection}/${id}` }) }),
    runTransaction: (run: (transaction: unknown) => Promise<unknown>) => run({ get: mocks.get, set: mocks.set, update: mocks.update }),
  })) as never,
  verify: mocks.verify,
  timestamp: (() => mocks.timestamp) as never,
});
const payload = () => ({ privacyVersion: PRIVACY_POLICY_VERSION, termsVersion: TERMS_VERSION, agreeTerms: true, acknowledgePrivacy: true, studentAgeConfirmed: true });
const request = (data = payload()) => ({ auth: { uid: 'student-a', token: {} }, data });

beforeEach(() => {
  vi.clearAllMocks();
  mocks.verify.mockResolvedValue(undefined);
  mocks.get.mockImplementation((ref: { path: string }) => Promise.resolve(ref.path.startsWith('users/')
    ? { exists: true, data: () => ({ role: 'student' }) } : { exists: false, data: () => undefined }));
});

describe('server agreement evidence', () => {
  test('rejects anonymous calls and unrevoked-session failures without writing', async () => {
    await expect(invoke({ data: payload() })).rejects.toMatchObject({ code: 'unauthenticated' });
    mocks.verify.mockRejectedValue(new Error('revoked'));
    await expect(invoke(request())).rejects.toThrow('revoked');
    expect(mocks.set).not.toHaveBeenCalled();
  });
  test.each([
    { privacyVersion: '2026-09-24' }, { termsVersion: '2026-09-24' },
    { agreeTerms: false }, { acknowledgePrivacy: false }, { studentAgeConfirmed: false }, { uid: 'another-person' },
  ])('rejects stale documents, missing actions and identity substitution: %j', async patch => {
    await expect(invoke(request({ ...payload(), ...patch }))).rejects.toMatchObject({ code: 'invalid-argument' });
    expect(mocks.set).not.toHaveBeenCalled();
    expect(mocks.update).not.toHaveBeenCalled();
  });
  test('records the authenticated identity, separate versions and server time', async () => {
    await expect(invoke(request())).resolves.toMatchObject({ success: true });
    expect(mocks.set).toHaveBeenCalledWith({ path: `legalAgreementRecords/student-a_${PRIVACY_POLICY_VERSION}_${TERMS_VERSION}` }, {
      uid: 'student-a', privacyVersion: PRIVACY_POLICY_VERSION, termsVersion: TERMS_VERSION,
      acceptedAt: mocks.timestamp, method: 'explicit-checkbox', studentAgeConfirmed: true,
    });
    expect(mocks.update).toHaveBeenCalledWith({ path: 'users/student-a' }, { legalAcceptance: expect.objectContaining({ acceptedAt: mocks.timestamp }) });
  });
  test('retries preserve the first accepted time for that release', async () => {
    mocks.get.mockImplementation((ref: { path: string }) => Promise.resolve({ exists: true, data: () => ref.path.startsWith('users/')
      ? { role: 'student' } : { acceptedAt: 'original-server-time', studentAgeConfirmed: true } }));
    await invoke(request());
    expect(mocks.set.mock.calls[0][1].acceptedAt).toBe('original-server-time');
  });
  test('school staff still agree explicitly but need no student-age attestation', async () => {
    mocks.get.mockImplementation((ref: { path: string }) => Promise.resolve(ref.path.startsWith('users/')
      ? { exists: true, data: () => ({ role: 'staff' }) } : { exists: false, data: () => undefined }));
    await invoke(request({ ...payload(), studentAgeConfirmed: false }));
    expect(mocks.set.mock.calls[0][1].studentAgeConfirmed).toBe(false);
  });
});
