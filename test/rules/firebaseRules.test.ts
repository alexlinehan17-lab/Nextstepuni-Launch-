/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import {
  assertFails,
  assertSucceeds,
  initializeTestEnvironment,
  type RulesTestEnvironment,
} from '@firebase/rules-unit-testing';
import { collection, deleteDoc, doc, getDoc, getDocs, increment, query, setDoc, updateDoc, where } from 'firebase/firestore';
import { getBytes, ref, uploadBytes } from 'firebase/storage';
import { ADMIN_EMAIL } from '../../utils/adminIdentity';

const PROJECT_ID = 'nextstepuni-rules-test';
let environment: RulesTestEnvironment;

beforeAll(async () => {
  environment = await initializeTestEnvironment({ projectId: PROJECT_ID });
});

beforeEach(async () => {
  await environment.clearFirestore();
  await environment.clearStorage();
  await environment.withSecurityRulesDisabled(async context => {
    const db = context.firestore();
    await Promise.all([
      setDoc(doc(db, 'users/alice'), { name: 'Alice', avatar: 'A', school: 'school-a' }),
      setDoc(doc(db, 'users/bob'), { name: 'Bob', avatar: 'B', school: 'school-b' }),
      setDoc(doc(db, 'users/gc-a'), { name: 'GC', avatar: 'G', role: 'gc', school: 'school-a' }),
      setDoc(doc(db, 'users/admin'), { name: 'Admin', avatar: 'A', role: 'admin', isAdmin: true }),
      setDoc(doc(db, 'users/legacy'), { name: 'Legacy', avatar: 'L', isAdmin: false }),
      setDoc(doc(db, 'progress/alice'), { pointsData: { totalEarned: 10, totalSpent: 0 } }),
      setDoc(doc(db, 'progress/bob'), { pointsData: { totalEarned: 10, totalSpent: 0 } }),
    ]);
    await uploadBytes(ref(context.storage(), 'papers/sample.pdf'), new Uint8Array([1, 2, 3]));
  });
});

afterAll(async () => {
  await environment.cleanup();
});

describe('Firestore ownership and staff boundaries', () => {
  it('allows repeatable 100 JP credits to the owner while preserving spending and other progress', async () => {
    await environment.withSecurityRulesDisabled(async context => {
      await setDoc(doc(context.firestore(), 'progress/alice'), {
        pointsData: { totalEarned: 250, totalSpent: 75 },
        'module-one': { unlockedSection: 3 },
      });
    });
    const db = environment.authenticatedContext('alice', { auth_time: 1 }).firestore();
    const credit = () => setDoc(doc(db, 'progress/alice'), {
      pointsData: { totalEarned: increment(100) },
    }, { merge: true });
    await assertSucceeds(Promise.all([credit(), credit()]));
    expect((await getDoc(doc(db, 'progress/alice'))).data()).toEqual({
      pointsData: { totalEarned: 450, totalSpent: 75 },
      'module-one': { unlockedSection: 3 },
    });
    await assertFails(setDoc(doc(db, 'progress/bob'), {
      pointsData: { totalEarned: increment(100) },
    }, { merge: true }));
  });

  it('allows a user to read their own private documents', async () => {
    const db = environment.authenticatedContext('alice', { auth_time: 1 }).firestore();
    await assertSucceeds(getDoc(doc(db, 'users/alice')));
    await assertSucceeds(getDoc(doc(db, 'progress/alice')));
  });

  it('denies unauthenticated and cross-user reads', async () => {
    const anonymousDb = environment.unauthenticatedContext().firestore();
    const aliceDb = environment.authenticatedContext('alice', { auth_time: 1 }).firestore();
    await assertFails(getDoc(doc(anonymousDb, 'users/alice')));
    await assertFails(getDoc(doc(aliceDb, 'users/bob')));
    await assertFails(getDoc(doc(aliceDb, 'progress/bob')));
  });

  it('prevents users from assigning themselves a role or changing school', async () => {
    const db = environment.authenticatedContext('alice', { auth_time: 1 }).firestore();
    await assertFails(updateDoc(doc(db, 'users/alice'), { role: 'gc' }));
    await assertFails(updateDoc(doc(db, 'users/alice'), { school: 'school-b' }));
  });

  it('keeps legal agreement evidence server-only on create, update and records', async () => {
    const db = environment.authenticatedContext('alice', { auth_time: 1 }).firestore();
    await assertFails(updateDoc(doc(db, 'users/alice'), { legalAcceptance: { acceptedAt: 'forged' } }));
    await assertFails(setDoc(doc(db, 'legalAgreementRecords/alice_release'), { uid: 'alice', acceptedAt: 'forged' }));
    const fresh = environment.authenticatedContext('fresh-agreement', { auth_time: 1 }).firestore();
    await assertFails(setDoc(doc(fresh, 'users/fresh-agreement'), { name: 'Student', avatar: 'A', legalAcceptance: { acceptedAt: 'forged' } }));
    await environment.withSecurityRulesDisabled(async context => {
      await setDoc(doc(context.firestore(), 'legalAgreementRecords/alice_release'), { uid: 'alice', acceptedAt: 'server-record' });
    });
    await assertFails(getDoc(doc(db, 'legalAgreementRecords/alice_release')));
  });

  it('keeps legacy isAdmin:false profiles writable without allowing escalation', async () => {
    const db = environment.authenticatedContext('legacy', { auth_time: 1 }).firestore();
    await assertSucceeds(updateDoc(doc(db, 'users/legacy'), { name: 'Updated legacy student' }));
    await assertFails(updateDoc(doc(db, 'users/legacy'), { isAdmin: true }));
  });

  it('allows staff to read only students in their own school', async () => {
    const db = environment.authenticatedContext('gc-a', { auth_time: 1 }).firestore();
    await assertSucceeds(getDoc(doc(db, 'users/alice')));
    await assertSucceeds(getDoc(doc(db, 'progress/alice')));
    await assertFails(getDoc(doc(db, 'users/bob')));
    await assertFails(getDoc(doc(db, 'progress/bob')));
  });

  it('rejects a stale staff claim when the current server-side roster has no membership', async () => {
    const db = environment.authenticatedContext('claim-only-staff', {
      auth_time: 1,
      role: 'staff',
      school: 'school-a',
    }).firestore();
    await assertFails(getDoc(doc(db, 'users/alice')));
    await assertFails(getDoc(doc(db, 'users/bob')));
  });

  it('denies sessions issued before a server-managed revocation cutoff', async () => {
    await environment.withSecurityRulesDisabled(async context => {
      await updateDoc(doc(context.firestore(), 'users/alice'), {
        sessionValidAfterSeconds: 200,
      });
    });
    const staleDb = environment.authenticatedContext('alice', { auth_time: 200 }).firestore();
    const currentDb = environment.authenticatedContext('alice', { auth_time: 201 }).firestore();
    await assertFails(getDoc(doc(staleDb, 'users/alice')));
    await assertFails(getDoc(doc(staleDb, 'progress/alice')));
    await assertSucceeds(getDoc(doc(currentDb, 'users/alice')));
    await assertSucceeds(getDoc(doc(currentDb, 'progress/alice')));
  });

  it('keeps password-reset, revocation, and authorization fields server-owned', async () => {
    const aliceDb = environment.authenticatedContext('alice', { auth_time: 1 }).firestore();
    await assertFails(updateDoc(doc(aliceDb, 'users/alice'), { needsPasswordChange: true }));
    await assertFails(updateDoc(doc(aliceDb, 'users/alice'), { sessionValidAfterSeconds: 9_999 }));

    const newUserDb = environment.authenticatedContext('new-user', { auth_time: 1 }).firestore();
    await assertFails(setDoc(doc(newUserDb, 'users/new-user'), {
      name: 'New',
      avatar: 'N',
      passwordResetAtSeconds: 123,
    }));
  });

  it('forces destructive user deletion through the audited callable', async () => {
    const gcDb = environment.authenticatedContext('gc-a', { auth_time: 1 }).firestore();
    const adminDb = environment.authenticatedContext('admin', {
      email: ADMIN_EMAIL,
      email_verified: true,
      admin: true,
      auth_time: 1,
    }).firestore();
    await assertFails(deleteDoc(doc(gcDb, 'users/alice')));
    await assertFails(deleteDoc(doc(adminDb, 'users/alice')));
    await assertFails(deleteDoc(doc(adminDb, 'progress/alice')));
  });

  it('keeps access-code secrets and peer or aggregate writes server-only', async () => {
    const aliceDb = environment.authenticatedContext('alice', { auth_time: 1 }).firestore();
    const gcDb = environment.authenticatedContext('gc-a', { auth_time: 1 }).firestore();

    await assertFails(setDoc(doc(gcDb, 'gcSettings/school-a'), {
      staffCode: 'SHOULD-NOT-BE-HERE',
      dismissedAlerts: {},
    }));
    await assertSucceeds(setDoc(doc(gcDb, 'gcSettings/school-a'), { dismissedAlerts: {} }));
    await assertFails(setDoc(doc(aliceDb, 'kudos/forged'), {
      fromUid: 'alice', toUid: 'bob', presetId: 'well-done',
    }));
    await assertFails(setDoc(doc(aliceDb, 'gifts/forged'), {
      fromUid: 'alice', toUid: 'bob', itemId: 'tree-oak',
    }));
    await assertFails(setDoc(doc(aliceDb, 'chairCohorts/class-a'), { submissions: 1 }));
    await assertFails(setDoc(doc(aliceDb, 'focusPresence/class-a/buckets/2026-08-23T10:00'), { count: 1 }));
  });

  it('bounds self-reported Journey Points and never permits a negative or overspent balance', async () => {
    const aliceDb = environment.authenticatedContext('alice', { auth_time: 1 }).firestore();
    const progress = doc(aliceDb, 'progress/alice');

    await assertFails(updateDoc(progress, {
      pointsData: { totalEarned: 9, totalSpent: 0 },
    }));
    await assertFails(updateDoc(progress, {
      pointsData: { totalEarned: 511, totalSpent: 0 },
    }));
    await assertFails(updateDoc(progress, {
      pointsData: { totalEarned: 10, totalSpent: 11 },
    }));
    await assertFails(updateDoc(progress, {
      pointsData: { totalEarned: 10.5, totalSpent: 0 },
    }));

    await assertSucceeds(updateDoc(progress, {
      pointsData: { totalEarned: 510, totalSpent: 0 },
    }));
    await assertSucceeds(updateDoc(progress, {
      pointsData: { totalEarned: 510, totalSpent: 510 },
    }));
  });

  it('protects study-session subcollections by owner and school', async () => {
    await environment.withSecurityRulesDisabled(async context => {
      await setDoc(doc(context.firestore(), 'progress/alice/sessions/session-1'), { duration: 25 });
    });
    await assertSucceeds(getDoc(doc(environment.authenticatedContext('alice', { auth_time: 1 }).firestore(), 'progress/alice/sessions/session-1')));
    await assertSucceeds(getDoc(doc(environment.authenticatedContext('gc-a', { auth_time: 1 }).firestore(), 'progress/alice/sessions/session-1')));
    await assertFails(getDoc(doc(environment.authenticatedContext('bob', { auth_time: 1 }).firestore(), 'progress/alice/sessions/session-1')));
  });
});

describe('Anonymous feedback boundary', () => {
  beforeEach(async () => {
    await environment.withSecurityRulesDisabled(async context => {
      await setDoc(doc(context.firestore(), 'anonymousFeedback/feedback-1'), {
        category: 'broken',
        message: 'The module button did not open.',
        context: { surface: 'home' },
        platform: 'web',
        appVersion: '0.0.0',
        status: 'new',
        createdAt: new Date(),
        expiresAt: new Date(Date.now() + 86_400_000),
      });
      await setDoc(doc(context.firestore(), 'feedbackRateLimits/bucket-1'), {
        count: 1,
        day: '2026-08-13',
      });
    });
  });

  it('denies feedback reads and writes to students', async () => {
    const studentDb = environment.authenticatedContext('alice', { auth_time: 1 }).firestore();
    await assertFails(getDocs(collection(studentDb, 'anonymousFeedback')));
    await assertFails(setDoc(doc(studentDb, 'anonymousFeedback/student-write'), {
      category: 'idea',
      message: 'Please add this feature.',
    }));
    await assertFails(getDoc(doc(studentDb, 'feedbackRateLimits/bucket-1')));
  });

  it('gives the retired admin@nextstep.app address no admin rights', async () => {
    // Moved to a real mailbox on 2026-08-17 so the password can be reset. The
    // old Auth account still exists, so prove it is now just another signed-in
    // user as far as the database is concerned.
    const retiredDb = environment.authenticatedContext('retired-admin', {
      email: 'admin@nextstep.app',
      auth_time: 1,
    }).firestore();
    await assertFails(getDocs(collection(retiredDb, 'anonymousFeedback')));
    await assertFails(getDoc(doc(retiredDb, 'users/student-1')));
  });

  it('lets the platform admin read feedback and change only workflow fields', async () => {
    const adminDb = environment.authenticatedContext('admin', {
      email: ADMIN_EMAIL,
      email_verified: true,
      admin: true,
      auth_time: 1,
    }).firestore();
    await assertSucceeds(getDocs(collection(adminDb, 'anonymousFeedback')));
    await assertSucceeds(updateDoc(doc(adminDb, 'anonymousFeedback/feedback-1'), {
      status: 'reviewing',
      reviewedAt: new Date(),
    }));
    await assertFails(updateDoc(doc(adminDb, 'anonymousFeedback/feedback-1'), {
      message: 'Changed by admin',
      status: 'reviewing',
      reviewedAt: new Date(),
    }));
    await assertFails(getDoc(doc(adminDb, 'feedbackRateLimits/bucket-1')));
  });

  it('does not grant admin access from an email alone', async () => {
    const emailOnlyDb = environment.authenticatedContext('email-only-admin', {
      email: ADMIN_EMAIL,
      email_verified: true,
      auth_time: 1,
    }).firestore();
    const unverifiedClaimDb = environment.authenticatedContext('unverified-admin', {
      email: ADMIN_EMAIL,
      email_verified: false,
      admin: true,
      auth_time: 1,
    }).firestore();
    await assertFails(getDocs(collection(emailOnlyDb, 'anonymousFeedback')));
    await assertFails(getDocs(collection(unverifiedClaimDb, 'anonymousFeedback')));
  });
});

describe('Storage corpus boundary', () => {
  it('allows public reads of published papers', async () => {
    const storage = environment.unauthenticatedContext().storage();
    await assertSucceeds(getBytes(ref(storage, 'papers/sample.pdf')));
  });

  it('denies client writes and access outside the paper corpus', async () => {
    const storage = environment.authenticatedContext('alice', { auth_time: 1 }).storage();
    await assertFails(uploadBytes(ref(storage, 'papers/client-upload.pdf'), new Uint8Array([1])));
    await assertFails(uploadBytes(ref(storage, 'private/file.txt'), new Uint8Array([1])));
    await assertFails(getBytes(ref(storage, 'private/file.txt')));
  });
});


describe('paper island transaction ownership', () => {
  it('prevents clients from forging island state or refund receipts', async () => {
    const db = environment.authenticatedContext('alice', { auth_time: 1 }).firestore();
    await assertFails(updateDoc(doc(db, 'progress/alice'), { paperIsland: {version: 1, credits: 999} }));
    await environment.withSecurityRulesDisabled(async context => {
      await updateDoc(doc(context.firestore(), 'progress/alice'), {paperIsland: {version: 1, credits: 3}});
    });
    await assertFails(updateDoc(doc(db, 'progress/alice'), {'paperIsland.credits': 99}));
    await assertSucceeds(updateDoc(doc(db, 'progress/alice'), {'pointsData.totalEarned': 20}));
  });
  it('does not permit a forged island on initial profile creation', async () => {
    const db = environment.authenticatedContext('legacy', { auth_time: 1 }).firestore();
    await assertFails(setDoc(doc(db, 'progress/legacy'), {paperIsland: {version: 1}, pointsData: {totalEarned: 0, totalSpent: 0}}));
    await assertSucceeds(setDoc(doc(db, 'progress/legacy'), {subjectProfile: {}, pointsData: {totalEarned: 0, totalSpent: 0}}));
  });
});

describe('year islands: classmates in the same school and year only', () => {
  const island = (school: string, yearGroup?: string) => ({
    schemaVersion: 2,
    name: 'Classmate',
    avatar: 'C',
    school,
    ...(yearGroup ? { yearGroup } : {}),
    tiles: [{ q: 0, r: 0, kind: 'home' }],
    tileCount: 1,
  });
  const as = (uid: string) => environment.authenticatedContext(uid, { auth_time: 1 }).firestore();
  const yearQuery = (uid: string, school: string, yearGroup: string) =>
    getDocs(query(collection(as(uid), 'islandPublic'), where('school', '==', school), where('yearGroup', '==', yearGroup)));

  beforeEach(async () => {
    await environment.withSecurityRulesDisabled(async context => {
      const db = context.firestore();
      await Promise.all([
        setDoc(doc(db, 'users/a5-viewer'), { name: 'Viewer Student', avatar: 'V', school: 'school-a', yearGroup: '5th' }),
        setDoc(doc(db, 'users/a5-hidden-viewer'), { name: 'Quiet', avatar: 'Q', school: 'school-a', yearGroup: '5th', islandVisibility: 'hidden' }),
        setDoc(doc(db, 'users/a-no-year'), { name: 'New', avatar: 'N', school: 'school-a' }),
        setDoc(doc(db, 'users/a-graduate'), { name: 'Grad', avatar: 'G', school: 'school-a', yearGroup: 'graduated' }),
        setDoc(doc(db, 'users/gc-a5'), { name: 'GC', avatar: 'G', role: 'gc', school: 'school-a', yearGroup: '5th' }),
        setDoc(doc(db, 'islandPublic/a5-classmate'), island('school-a', '5th')),
        setDoc(doc(db, 'islandPublic/a6-older'), island('school-a', '6th')),
        setDoc(doc(db, 'islandPublic/b5-other-school'), island('school-b', '5th')),
        setDoc(doc(db, 'islandPublic/a-legacy'), island('school-a')),
      ]);
    });
  });

  it('lets a student list and open their own year group at their own school', async () => {
    const snapshot = await assertSucceeds(yearQuery('a5-viewer', 'school-a', '5th'));
    expect(snapshot.docs.map(d => d.id)).toEqual(['a5-classmate']);
    await assertSucceeds(getDoc(doc(as('a5-viewer'), 'islandPublic/a5-classmate')));
  });

  it('lets a student who hides their own island still browse their year', async () => {
    await assertSucceeds(yearQuery('a5-hidden-viewer', 'school-a', '5th'));
  });

  it('denies another year, another school, a school-wide query and a schema 1 projection', async () => {
    await assertFails(yearQuery('a5-viewer', 'school-a', '6th'));
    await assertFails(yearQuery('a5-viewer', 'school-b', '5th'));
    await assertFails(getDocs(query(collection(as('a5-viewer'), 'islandPublic'), where('school', '==', 'school-a'))));
    await assertFails(getDoc(doc(as('a5-viewer'), 'islandPublic/a6-older')));
    await assertFails(getDoc(doc(as('a5-viewer'), 'islandPublic/b5-other-school')));
    await assertFails(getDoc(doc(as('a5-viewer'), 'islandPublic/a-legacy')));
  });

  it('denies students with no year, graduates, staff and signed-out visitors', async () => {
    await assertFails(getDoc(doc(as('a-no-year'), 'islandPublic/a5-classmate')));
    await assertFails(yearQuery('a-graduate', 'school-a', 'graduated'));
    await assertFails(getDoc(doc(as('a-graduate'), 'islandPublic/a5-classmate')));
    await assertFails(yearQuery('gc-a5', 'school-a', '5th'));
    await assertFails(getDoc(doc(environment.unauthenticatedContext().firestore(), 'islandPublic/a5-classmate')));
  });

  it('denies a session issued before a revocation cutoff', async () => {
    await environment.withSecurityRulesDisabled(async context => {
      await updateDoc(doc(context.firestore(), 'users/a5-viewer'), { sessionValidAfterSeconds: 5 });
    });
    await assertFails(yearQuery('a5-viewer', 'school-a', '5th'));
  });

  it('never lets a client write a projection, even their own', async () => {
    await assertFails(setDoc(doc(as('a5-viewer'), 'islandPublic/a5-viewer'), island('school-a', '5th')));
    await assertFails(updateDoc(doc(as('a5-viewer'), 'islandPublic/a5-classmate'), { name: 'Changed' }));
    await assertFails(deleteDoc(doc(as('a5-viewer'), 'islandPublic/a5-classmate')));
  });

  it('accepts only the two island visibility choices', async () => {
    const profile = doc(as('a5-viewer'), 'users/a5-viewer');
    await assertSucceeds(updateDoc(profile, { islandVisibility: 'hidden' }));
    await assertSucceeds(updateDoc(profile, { islandVisibility: 'year' }));
    await assertFails(updateDoc(profile, { islandVisibility: 'school' }));
    await assertFails(updateDoc(profile, { islandVisibility: true }));
    const fresh = environment.authenticatedContext('fresh-visibility', { auth_time: 1 }).firestore();
    await assertFails(setDoc(doc(fresh, 'users/fresh-visibility'), { name: 'New', avatar: 'N', islandVisibility: 'everyone' }));
  });
});
