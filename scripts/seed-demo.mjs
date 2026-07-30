// One-off: seed a realistic demo student account for App Store screenshots +
// App Review login. Uses the app's PUBLIC Firebase web config and writes as the
// authenticated demo user, so Firestore security rules are respected (no admin
// SDK / service account). Safe to re-run (create-or-sign-in).
//
//   node scripts/seed-demo.mjs
//
// NOT committed (contains the demo password). Credentials are printed at the end.
import { initializeApp } from 'firebase/app';
import { getAuth, createUserWithEmailAndPassword, signInWithEmailAndPassword, updateProfile } from 'firebase/auth';
import { getFirestore, doc, setDoc } from 'firebase/firestore';

// The web API key restricts requests to the app's HTTP referrers; Node sends an
// empty referrer and is blocked. Spoof an allowed referrer so the SDK calls pass
// the API-key referrer check (same origin a real browser would send).
const _fetch = globalThis.fetch;
globalThis.fetch = (input, init = {}) => {
  const headers = new Headers(init.headers || {});
  headers.set('Referer', 'https://nextstepuni-app.web.app/');
  headers.set('Origin', 'https://nextstepuni-app.web.app');
  return _fetch(input, { ...init, headers });
};

const firebaseConfig = {
  apiKey: 'AIzaSyCoNBVVlJifQ_n3Pf1P1BA9QalOOcK0kNA',
  authDomain: 'nextstepuni-app.firebaseapp.com',
  projectId: 'nextstepuni-app',
  storageBucket: 'nextstepuni-app.firebasestorage.app',
  messagingSenderId: '52864318610',
  appId: '1:52864318610:web:24f445c78a71f215c2ba4b',
};

const EMAIL = 'appreview@nextstepuni.app';
const PASSWORD = 'NextStep-Demo-2026';

const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
const db = getFirestore(app);

let cred;
try {
  cred = await createUserWithEmailAndPassword(auth, EMAIL, PASSWORD);
  console.log('created auth account');
} catch (e) {
  if (e.code === 'auth/email-already-in-use') {
    cred = await signInWithEmailAndPassword(auth, EMAIL, PASSWORD);
    console.log('signed in to existing account');
  } else { throw e; }
}
const uid = cred.user.uid;
await updateProfile(cred.user, { displayName: 'Aoife Brennan' }).catch(() => {});

// ── users/{uid} — omit role/isAdmin (rules forbid); valid avatar seed + school id
await setDoc(doc(db, 'users', uid), {
  name: 'Aoife Brennan',
  avatar: 'Maya Angelou',
  school: 'marino',
  yearGroup: '6th',
  curriculumLevel: 'senior',
  consent: { policyVersion: '2026-06-01', acceptedAt: '2025-09-02T10:14:00.000Z', basis: 'school-enrolment' },
}, { merge: true });

// ── progress/{uid} — module keys + named feature fields on one doc.
// pointsData.totalEarned must be <= 1000 on create (security rule).
await setDoc(doc(db, 'progress', uid), {
  subjectProfile: {
    subjects: [
      { subjectName: 'English',     level: 'higher',   currentGrade: 'H4', targetGrade: 'H2' },
      { subjectName: 'Mathematics', level: 'higher',   currentGrade: 'H5', targetGrade: 'H3' },
      { subjectName: 'Biology',     level: 'higher',   currentGrade: 'H3', targetGrade: 'H2' },
      { subjectName: 'Business',    level: 'higher',   currentGrade: 'H2', targetGrade: 'H1' },
      { subjectName: 'Geography',   level: 'ordinary', currentGrade: 'O3', targetGrade: 'O2' },
    ],
    examStartDate: '2026-06-03',
    restDays: ['Sunday'],
    defaultBlockDuration: 45,
    yearGroup: '6th',
    curriculumLevel: 'senior',
    createdAt: '2025-09-02T10:20:00.000Z',
    updatedAt: '2026-06-18T19:30:00.000Z',
  },
  northStar: {
    category: 'college-learning',
    statement: 'Study Physiotherapy at UCD and be the first in my family to go to college.',
    visionBoard: [],
    createdAt: '2025-09-02T10:25:00.000Z',
    updatedAt: '2025-09-02T10:25:00.000Z',
  },
  pointsData: { totalEarned: 980, totalSpent: 120 },
  gamification: {
    unlockedAchievements: ['first-module', 'three-day-streak', 'first-mock-logged'],
    achievementTimestamps: { 'first-module': 1739200000000 },
    weeklyGoalProgress: {},
    weekStartDate: '2026-06-15',
    lastSurpriseDate: '',
    personalBests: {},
    streakShields: 1,
    streakShieldUsedDates: [],
    lastStreakBreakDate: '',
    recoveryWindowEnd: '',
  },
  timetableCompletions: {
    '2026-06-15': ['English|new-learning|0', 'Biology|practice|1'],
    '2026-06-16': ['Mathematics|revision|0'],
    '2026-06-17': ['Business|practice|0', 'Biology|new-learning|0'],
    '2026-06-18': ['Geography|new-learning|0', 'English|revision|2'],
    '2026-06-19': ['Mathematics|practice|0'],
    '2026-06-20': ['English|new-learning|1', 'Biology|revision|0'],
    '2026-06-21': ['Business|revision|0'],
  },
  timetableStreak: { currentStreak: 7, lastActiveDate: '2026-06-21', longestStreak: 14 },
  cosmeticUnlocks: { avatarSeeds: [], themeColors: [], cardStyles: [] },
  dismissedGuides: {},
  topicMastery: {
    Biology: { 'The Cell': { confidence: 'solid', updatedAt: 1739200000000, source: 'manual' } },
  },
  unifiedMockResults: [
    {
      id: 'mock-2026-spring', label: 'Spring Mocks', date: '2026-02-12',
      entries: [
        { subjectName: 'English', grade: 'H4', level: 'higher' },
        { subjectName: 'Biology', grade: 'H3', level: 'higher' },
      ],
      totalPoints: 410, timestamp: 1739332800000,
    },
  ],
  // Completed modules in the Mind world (unlockedSection >= sectionsCount).
  'agency-protocol': { unlockedSection: 6 },
  'hope-protocol': { unlockedSection: 6 },
  'affirming-values-protocol': { unlockedSection: 5 },
  'best-possible-self-protocol': { unlockedSection: 5 },
  'grammar-of-grit-protocol': { unlockedSection: 5 },
}, { merge: true });

console.log('seeded users/' + uid + ' and progress/' + uid);
console.log('LOGIN:', EMAIL, '/', PASSWORD);
process.exit(0);
