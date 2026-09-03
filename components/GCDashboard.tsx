/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */
import React, { useState, useEffect, useMemo } from 'react';
import { AnimatePresence } from 'framer-motion';
import { MotionDiv } from './Motion';
import { type CourseData } from './Library';
import { type SessionUser, getAvatarUrl, yearGroupToCurriculumLevel } from '../utils/authUtils';
import { LogOut, LayoutDashboard, Users, BarChart3, PanelLeft, StickyNote, AlertTriangle, CalendarDays, ListChecks, KeyRound, RefreshCw } from 'lucide-react';
import app, { auth, db } from '../firebase';
import { collection, query, where, limit, getDocs, doc, getDoc, setDoc } from 'firebase/firestore';
import { getFunctions, httpsCallable } from 'firebase/functions';
import { getSchoolName } from '../schoolData';
import { type UserProgress, type PointsData, type CollegeCompassState, type UnifiedMockResult } from '../types';
import { computeStreak } from './timetableAlgorithm';
import { lastActiveDateFrom } from '../utils/weekDates';
import { saveInBackground } from '../utils/firestoreWrite';
import { type StudentSubjectProfile, type TimetableCompletions, type TimetableStreak } from './subjectData';
import { type NorthStar } from '../types';
import { type GameState } from './journeySimulatorData';
import {
  type GCStudentFullData,
  type JourneyResult,
  type MockResultEntry,
} from './gc/gcTypes';
import { type DebriefEntry } from './StudyDebrief';
import { GCOverview } from './gc/GCOverview';
import { GCKeyEvents } from './gc/GCKeyEvents';
import { StaffAccessPanel } from './gc/StaffAccessPanel';
import { GCStudentDetail } from './gc/GCStudentDetail';
import GCHandInGrid from './gc/GCHandInGrid';
import GCAssignPanel from './gc/GCAssignPanel';
import { generateAlerts, type DismissedAlert, type EarlyWarningAlert } from './gc/gcAlerts';
import { useGCFlags } from '../hooks/useGCFlags';
import { logError } from '../utils/logError';
import { reauthenticateCurrentUser } from '../utils/reauthenticate';

interface GCDashboardProps {
  school: string;
  onLogout: () => void;
  allCourses: CourseData[];
  gcName?: string;
  gcUid?: string;
  role?: SessionUser['role'];
}

// ─── Shimmer skeleton ────────────────────────────────────────────────────────

const SkeletonPulse: React.FC<{ className?: string; style?: React.CSSProperties }> = ({ className = '', style }) => (
  <div className={`rounded-xl bg-zinc-200 dark:bg-zinc-800 animate-[shine_1.5s_ease-in-out_infinite] ${className}`} style={style} />
);

const LoadingSkeleton: React.FC = () => (
  <div className="space-y-6 p-8">
    <div className="grid grid-cols-1 sm:grid-cols-3 gap-5">
      {Array.from({ length: 3 }).map((_, i) => (
        <div key={i} className="rounded-xl bg-white dark:bg-zinc-900 border border-zinc-200 dark:border-zinc-800 p-5 space-y-3">
          <SkeletonPulse className="h-3 w-20" />
          <SkeletonPulse className="h-12 w-24" />
          <SkeletonPulse className="h-3 w-32" />
        </div>
      ))}
    </div>
    <div className="grid grid-cols-1 lg:grid-cols-3 gap-5">
      <div className="lg:col-span-2 space-y-5">
        <div className="rounded-xl bg-white dark:bg-zinc-900 border border-zinc-200 dark:border-zinc-800 p-5 space-y-4">
          <SkeletonPulse className="h-4 w-40" />
          <div className="flex items-end gap-4 h-32">
            {[60, 40, 80, 50].map((h, i) => (
              <SkeletonPulse key={i} className="flex-1 rounded-lg" style={{ height: `${h}%` }} />
            ))}
          </div>
        </div>
      </div>
      <div className="space-y-5">
        <div className="rounded-xl bg-white dark:bg-zinc-900 border border-zinc-200 dark:border-zinc-800 p-5 space-y-3">
          <SkeletonPulse className="h-4 w-28" />
          {Array.from({ length: 4 }).map((_, i) => (
            <div key={i} className="flex items-center gap-3">
              <SkeletonPulse className="w-8 h-8 rounded-full" />
              <SkeletonPulse className="h-3 flex-1" />
            </div>
          ))}
        </div>
      </div>
    </div>
  </div>
);

// ─── Progress-doc → GC record ───────────────────────────────────────────────

/**
 * The single place a raw `progress/{uid}` document becomes a GC record.
 *
 * This is a pure function on purpose: it is the contract between what every
 * student-facing tool WRITES and what the guidance counsellor READS, and it is
 * the only consumer of those fields outside the tool that owns them. When a
 * refactor moved mock results to a top-level `mockResults` array and Future
 * Finder to a `futureFinderRevamped` namespace, nothing caught it — the GC just
 * silently read fields nobody wrote any more. test/gcLoaderContract.test.ts now
 * locks every one of these hops.
 *
 * Rule for anyone adding a field: read the field the tool actually writes, keep
 * a fallback for docs written before the last migration, and never let "absent"
 * collapse into a confident zero — hand `null` to the render layer and let it
 * show an em-dash.
 */
export function mapProgressDocToStudent(
  user: SessionUser,
  progressDoc: Record<string, any> | null,
): GCStudentFullData {
  const progress: UserProgress = {};
  if (progressDoc) {
    for (const [key, val] of Object.entries(progressDoc)) {
      if (val && typeof val === 'object' && 'unlockedSection' in val) {
        progress[key] = val as { unlockedSection: number };
      }
    }
  }

  const subjectProfile = (progressDoc?.subjectProfile as StudentSubjectProfile) ?? null;
  const northStar = (progressDoc?.northStar as NorthStar) ?? null;
  const journeyRaw = progressDoc?.['journey-simulator'] as { endingId?: string; finalStats?: GameState; completedAt?: string; decisionsCount?: number; scoringVersion?: number } | undefined;
  const journeyResult: JourneyResult | null = journeyRaw?.endingId
    ? { endingId: journeyRaw.endingId, finalStats: journeyRaw.finalStats!, completedAt: journeyRaw.completedAt, decisionsCount: journeyRaw.decisionsCount, scoringVersion: journeyRaw.scoringVersion }
    : null;
  const points = (progressDoc?.pointsData as PointsData) ?? null;
  const timetableCompletions = (progressDoc?.timetableCompletions as TimetableCompletions) ?? null;

  // Streak — DERIVED, not read.
  //
  // `timetableStreak` is a snapshot only ever written by one of the two
  // completion paths (the Innovation Zone toggle), so a student who studies
  // via "Study Now" had a live 9-day streak on their own screen and 0 here,
  // and a student who stopped a fortnight ago still showed 12. Recomputing with
  // the exact two-argument call ProgressContext makes puts the GC on the same
  // number the student sees. `longestStreak` is preserved from the snapshot so
  // the streak-broken alert's "had a 7+ run" gate still works.
  //
  // lastActiveDate comes from the completions map, NOT from computeStreak —
  // that returns TODAY whenever the streak is 0, which would mark every dormant
  // student as active today and silently disable the at-risk alerts.
  const savedStreak = (progressDoc?.timetableStreak as TimetableStreak) ?? null;
  // restDayPasses matters: a student can spend 60 points on a rest-day pass,
  // and computeStreak treats a passed day as a continuation rather than a
  // break. Omitting the 4th argument would show the GC a SHORTER streak than
  // the student's own timetable card — and could push a student who paid to
  // protect their streak into 'drifting' or 'at-risk' in the counsellor's view.
  const restDayPasses = (progressDoc?.earnedRest as { restDayPasses?: string[] })?.restDayPasses ?? [];
  const computedStreak = progressDoc
    ? computeStreak(timetableCompletions ?? {}, subjectProfile?.restDays ?? [], new Date(), restDayPasses)
    : null;
  const streak: TimetableStreak | null = computedStreak
    ? {
        currentStreak: computedStreak.currentStreak,
        longestStreak: Math.max(computedStreak.currentStreak, savedStreak?.longestStreak ?? 0),
        lastActiveDate: lastActiveDateFrom(timetableCompletions) ?? '',
      }
    : savedStreak;

  // Future Finder — two namespaces.
  //
  // The live senior tool is `future-finder-revamped`, which writes
  // `futureFinderRevamped`; the tile that writes the legacy `futureFinder`
  // namespace is tagged junior-only and titled "Future Finder Old". Reading
  // only the legacy field meant the GC showed a superseded list — or nothing —
  // for a student who had just finished the quiz. `picks` is the student's
  // explicit bookmarks (save-order); `topMatches` is the algorithm's ranking.
  const ffNew = progressDoc?.futureFinderRevamped as { picks?: string[]; topMatches?: string[]; completedAt?: string; updatedAt?: string } | undefined;
  const ffOld = progressDoc?.futureFinder as { topPicks?: string[]; completedAt?: string } | undefined;
  const newPicks = ffNew?.picks?.length ? ffNew.picks : [];
  const newRanked = ffNew?.topMatches?.length ? ffNew.topMatches : [];
  const oldPicks = ffOld?.topPicks?.length ? ffOld.topPicks : [];
  // `.length` matters: the JC Subject Explorer writes `topPicks: []`, and an
  // empty array is truthy — that alone rendered an empty "Insights" heading.
  const futureFinder: GCStudentFullData['futureFinder'] =
    newPicks.length
      ? { topPicks: newPicks, completedAt: ffNew?.completedAt ?? ffNew?.updatedAt ?? '', source: 'saved' }
      : newRanked.length
        ? { topPicks: newRanked, completedAt: ffNew?.completedAt ?? ffNew?.updatedAt ?? '', source: 'ranked' }
        : oldPicks.length
          ? { topPicks: oldPicks, completedAt: ffOld?.completedAt ?? '', source: 'legacy' }
          : null;

  // Mock results — students write a top-level `mockResults` array of
  // UnifiedMockResult (one record per sitting, subjects nested under
  // `entries`). The GC used to read `warRoom.mockResults`, which nothing has
  // written since the mock-results refactor, so the Mock Trajectory table and
  // the whole school-wide Subject Health card silently never rendered. Flatten
  // to one row per subject, exactly as WarRoom does for the student.
  const unifiedMocks = (progressDoc?.mockResults as UnifiedMockResult[] | undefined) ?? [];
  const legacyMocks = (progressDoc?.warRoom as { mockResults?: MockResultEntry[] })?.mockResults ?? null;
  const flattenedMocks: MockResultEntry[] = unifiedMocks.flatMap(m => (m.entries ?? []).map(e => ({
    id: `${m.id}-${e.subjectName}`,
    subject: e.subjectName,
    grade: String(e.grade ?? ''),
    date: m.date,
    label: m.label,
    timestamp: m.timestamp,
  })));
  // Fall back on the FLATTENED length, not on `unifiedMocks.length`. The
  // forward-migration in useMockResults maps `entries: m.grades || []`, but
  // legacy records have no `grades` key — so a migrated doc can hold a
  // non-empty mockResults array whose every record has `entries: []`. Testing
  // the raw array would make that shadow the still-intact legacy blob and hide
  // the student's real grades. Students dormant since the refactor hold only
  // the legacy blob; both cases land here.
  const mockResults: MockResultEntry[] | null = flattenedMocks.length ? flattenedMocks : legacyMocks;

  const debriefArr = progressDoc?.studyDebriefs as DebriefEntry[] | undefined;
  const recentDebriefs = debriefArr ? debriefArr.slice(-20) : null;

  // College Compass — read the SAME field the student writes (no copy, no drift).
  const collegeCompass = (progressDoc?.collegeCompass as CollegeCompassState) ?? null;

  // Derive year-group / curriculum-level (Phase 1 JC plumbing).
  // Prefer the user doc (set during onboarding + by AuthContext
  // migration), fall back to subjectProfile (legacy location).
  const yearGroup = user.yearGroup ?? subjectProfile?.yearGroup;
  const curriculumLevel = user.curriculumLevel
    ?? (yearGroup ? yearGroupToCurriculumLevel(yearGroup) : undefined);

  return {
    user,
    progress,
    subjectProfile,
    northStar,
    journeyResult,
    streak,
    points,
    timetableCompletions,
    futureFinder,
    mockResults,
    recentDebriefs,
    collegeCompass,
    yearGroup,
    curriculumLevel,
  };
}

// ─── Component ──────────────────────────────────────────────────────────────

export const GCDashboard: React.FC<GCDashboardProps> = ({ school, onLogout, allCourses, gcName, gcUid, role }) => {
  const [studentData, setStudentData] = useState<GCStudentFullData[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [selectedStudentUid, setSelectedStudentUid] = useState<string | null>(null);
  const [activeNav, setActiveNav] = useState<string>('gc-overview');
  const [sidebarOpen, setSidebarOpen] = useState(false);
  // The dashboard is a one-shot snapshot (the /progress read rule authorises
  // get()-shaped reads only, so onSnapshot is not available here). Make the
  // staleness visible instead of silent, and give the GC a way to re-pull.
  const [lastLoadedAt, setLastLoadedAt] = useState<Date | null>(null);
  const [reloadVersion, setReloadVersion] = useState(0);
  const [truncated, setTruncated] = useState(false);

  // GC dashboard is always dark mode
  useEffect(() => {
    document.documentElement.classList.add('dark');
    return () => { document.documentElement.classList.remove('dark'); };
  }, []);

  const gcFlags = useGCFlags(gcUid);

  const [deleteTarget, setDeleteTarget] = useState<SessionUser | null>(null);
  const [isDeleting, setIsDeleting] = useState(false);
  const [deleteVerificationPassword, setDeleteVerificationPassword] = useState('');
  const closeDeleteDialog = () => {
    setDeleteVerificationPassword('');
    setDeleteTarget(null);
  };
  const [dismissedAlerts, setDismissedAlerts] = useState<Record<string, DismissedAlert>>({});

  // Full cascade delete via the requestAccountDeletion Cloud Function (Admin
  // SDK): removes the Auth account + every Firestore collection holding the
  // student's data, not just users + progress. Audit 2026-06-01 (item 15).
  const handleDeleteStudent = async (user: SessionUser) => {
    setIsDeleting(true);
    try {
      if (!auth.currentUser) throw new Error('No signed-in user');
      await reauthenticateCurrentUser(auth.currentUser, deleteVerificationPassword);
      const functions = getFunctions(app);
      const deleteFn = httpsCallable<{ uid: string }, { success: boolean }>(functions, 'requestAccountDeletion');
      await deleteFn({ uid: user.uid });
      setStudentData(prev => prev.filter(s => s.user.uid !== user.uid));
      if (selectedStudentUid === user.uid) setSelectedStudentUid(null);
    } catch (err) {
      console.error('Error deleting student:', err);
      alert('Failed to delete student. You may not have permission.');
    }
    setIsDeleting(false);
    setDeleteVerificationPassword('');
    closeDeleteDialog();
  };

  // ── Password reset handler ──
  const [resetResult, setResetResult] = useState<{ name: string; password: string } | null>(null);
  const [resetTargetUid, setResetTargetUid] = useState<string | null>(null);
  const [resetVerificationPassword, setResetVerificationPassword] = useState('');
  const [isResettingPassword, setIsResettingPassword] = useState(false);
  const closeResetDialog = () => {
    setResetVerificationPassword('');
    setResetTargetUid(null);
  };
  const handleResetPassword = async (studentUid: string) => {
    setIsResettingPassword(true);
    try {
      if (!auth.currentUser) throw new Error('No signed-in user');
      await reauthenticateCurrentUser(auth.currentUser, resetVerificationPassword);
      const functions = getFunctions(app);
      const resetFn = httpsCallable<{ studentUid: string }, { tempPassword: string; studentName: string }>(functions, 'resetStudentPassword');
      const result = await resetFn({ studentUid });
      setResetResult({ name: result.data.studentName, password: result.data.tempPassword });
    } catch (err) {
      console.error('Failed to reset password:', err);
      alert('Failed to reset password. Please try again.');
    }
    setIsResettingPassword(false);
    setResetVerificationPassword('');
    closeResetDialog();
  };

  // ── Alert dismiss handler ──
  const handleDismissAlert = async (alert: EarlyWarningAlert) => {
    const entry: DismissedAlert = { dismissedAt: Date.now(), metricAtDismissal: alert.metric };
    const updated = { ...dismissedAlerts, [alert.id]: entry };
    setDismissedAlerts(updated);
    saveInBackground(
      setDoc(doc(db, 'gcSettings', school), { dismissedAlerts: updated }, { merge: true }),
      'GCDashboard.dismissAlert',
      () => setDismissedAlerts(dismissedAlerts),
      { silent: true },
    );
  };

  // ── Compute alerts ──
  const alerts = useMemo(
    () => generateAlerts(studentData, dismissedAlerts),
    [studentData, dismissedAlerts],
  );

  // ── Alerts for a specific student (used in detail tray) ──
  const getStudentAlerts = (uid: string) => alerts.filter(a => a.studentUid === uid);

  // Stable random avatar seed per school
  const avatarSeed = useMemo(() => `gc-${school}-${school.length}`, [school]);

  const sidebarItems = [
    { id: 'gc-overview', label: 'Overview', icon: LayoutDashboard, active: activeNav === 'gc-overview' },
    { id: 'gc-handin', label: 'Practice', icon: ListChecks, active: activeNav === 'gc-handin' },
    { id: 'gc-events', label: 'Key Dates', icon: CalendarDays, active: activeNav === 'gc-events' },
    { id: 'gc-analytics', label: 'Analytics', icon: BarChart3, active: activeNav === 'gc-analytics' },
    { id: 'gc-students', label: 'Students', icon: Users, active: activeNav === 'gc-students' },
    { id: 'gc-notes', label: 'Notes', icon: StickyNote, active: activeNav === 'gc-notes' },
    ...(role === 'gc'
      ? [{ id: 'gc-staff-access', label: 'School access', icon: KeyRound, active: activeNav === 'gc-staff-access' }]
      : []),
  ];

  // Body scroll lock when tray is open
  useEffect(() => {
    if (selectedStudentUid) {
      document.body.style.overflow = 'hidden';
    } else {
      document.body.style.overflow = '';
    }
    return () => { document.body.style.overflow = ''; };
  }, [selectedStudentUid]);

  // On opening a student's tray, re-pull their progress doc so the GC sees the
  // most recent committed state.
  //
  // This used to keep ONLY collegeCompass off the fresh snapshot and throw the
  // rest away, so every other tray metric — points, streak, today's blocks,
  // mocks — stayed frozen at whatever it was when the dashboard first loaded.
  // Same getDoc, same cost; now the whole record is rehydrated.
  useEffect(() => {
    if (!selectedStudentUid) return;
    let cancelled = false;
    getDoc(doc(db, 'progress', selectedStudentUid)).then(snap => {
      if (cancelled || !snap.exists()) return;
      setStudentData(prev => prev.map(s =>
        s.user.uid === selectedStudentUid ? mapProgressDocToStudent(s.user, snap.data()) : s,
      ));
    }).catch((e) => logError('GCDashboard.reloadStudentProgress', e));
    return () => { cancelled = true; };
  }, [selectedStudentUid]);

  useEffect(() => {
    let cancelled = false;
    const fetchData = async () => {
      setIsLoading(true);
      try {
        const usersCol = collection(db, 'users');
        // Truncation used to be silent: a school over the cap simply lost
        // students with no error anywhere. Surface it instead.
        const USER_CAP = 1000;
        const schoolQuery = query(usersCol, where('school', '==', school), limit(USER_CAP));
        const userSnapshot = await getDocs(schoolQuery);
        const users = userSnapshot.docs.map(d => ({ uid: d.id, ...d.data() })) as SessionUser[];
        setTruncated(users.length >= USER_CAP);

        // Exclude all staff roles (gc/staff/admin) — the dashboard lists students only.
        const students = users.filter(u => u.role !== 'gc' && u.role !== 'staff' && u.role !== 'admin');

        // Read each student's progress with an individual getDoc, in parallel.
        //
        // IMPORTANT — do NOT "optimise" this into a batched
        //   getDocs(query(collection('progress'), where(documentId(),'in',chunk)))
        // The /progress read rule authorises GC access via a per-document
        // get(users/$(userId)).school == callerSchool() check. Firestore permits
        // get()-based rules for `get` operations but REJECTS them for `list`
        // (query) operations — so the batched query fails for EVERY chunk, the
        // error is swallowed, and the whole dashboard reads back empty
        // (subjectProfile null → CAO shows '—' for all students). Regression
        // introduced in e1450e3; reverted 2026-07-23. Per-student get() is the
        // only read the rules allow here.
        const progressByUid = new Map<string, Record<string, any>>();
        const progressSnaps = await Promise.all(
          students.map(s =>
            getDoc(doc(db, 'progress', s.uid)).catch(err => {
              console.error('Failed to fetch progress for student:', s.uid, err);
              return null;
            }),
          ),
        );
        progressSnaps.forEach((snap, i) => {
          if (snap && snap.exists()) progressByUid.set(students[i].uid, snap.data());
        });

        const fullData: GCStudentFullData[] = students.map(user =>
          mapProgressDocToStudent(user, progressByUid.get(user.uid) ?? null),
        );

        if (cancelled) return;
        setStudentData(fullData);
        setLastLoadedAt(new Date());

        // Load dismissed alerts
        try {
          const settingsSnap = await getDoc(doc(db, 'gcSettings', school));
          if (cancelled) return;
          if (settingsSnap.exists()) {
            setDismissedAlerts(settingsSnap.data().dismissedAlerts ?? {});
          }
        } catch (err) { console.error('Failed to load GC settings:', err); }
      } catch (err) {
        console.error('Error fetching GC data:', err);
      }
      if (!cancelled) setIsLoading(false);
    };

    fetchData();
    return () => { cancelled = true; };
  }, [school, reloadVersion]);

  const selectedStudent = selectedStudentUid
    ? studentData.find(s => s.user.uid === selectedStudentUid) ?? null
    : null;

  const handleNavClick = (sectionId: string) => {
    setActiveNav(sectionId);
    const el = document.getElementById(sectionId);
    if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' });
  };

  return (
    <div className="min-h-screen bg-white dark:bg-zinc-950 relative overflow-x-hidden">
      {/* ─── Sidebar (exact student dashboard replica) ───────────────────── */}
      <aside
        className={`hidden md:flex flex-col fixed top-0 left-0 h-full z-40 bg-white/80 dark:bg-zinc-900/80 backdrop-blur-sm border-r border-zinc-200 dark:border-zinc-800 overflow-hidden transition-all duration-300 ease-[cubic-bezier(0.16,1,0.3,1)] ${sidebarOpen ? 'w-56' : 'w-[60px]'}`}
      >
        {/* Avatar row — click to toggle */}
        <button
          onClick={() => setSidebarOpen(!sidebarOpen)}
          className="flex items-center gap-3 px-3 py-4 w-full hover:bg-zinc-100 dark:hover:bg-zinc-800 transition-colors"
        >
          <div className="w-9 h-9 rounded-lg overflow-hidden shrink-0 bg-zinc-200 dark:bg-zinc-700 flex items-center justify-center">
            <img src={getAvatarUrl(avatarSeed)} alt="Avatar" className="w-full h-full object-cover" />
          </div>
          <span className={`text-sm font-medium text-zinc-700 dark:text-zinc-300 whitespace-nowrap overflow-hidden transition-opacity duration-300 ${sidebarOpen ? 'opacity-100' : 'opacity-0'}`}>
            {getSchoolName(school)}
          </span>
        </button>

        {/* Nav items */}
        <nav className="flex-1 flex flex-col gap-1 px-2 mt-2">
          {sidebarItems.map((item) => (
            <button
              key={item.id}
              onClick={() => handleNavClick(item.id)}
              className={`flex items-center gap-3 px-2.5 py-2 rounded-lg transition-colors ${item.active ? 'bg-zinc-100 dark:bg-zinc-800' : 'hover:bg-zinc-100 dark:hover:bg-zinc-800'}`}
            >
              <div className="shrink-0 flex items-center justify-center w-[18px]">
                <item.icon size={18} strokeWidth={1.5} className="text-zinc-600 dark:text-zinc-400" />
              </div>
              <span className={`text-sm font-medium text-zinc-700 dark:text-zinc-300 whitespace-nowrap overflow-hidden transition-opacity duration-300 ${sidebarOpen ? 'opacity-100' : 'opacity-0'}`}>
                {item.label}
              </span>
            </button>
          ))}
        </nav>

        {/* Bottom section */}
        <div className="border-t border-zinc-200 dark:border-zinc-800 mx-2 pt-2 flex flex-col gap-1">
          {/* Log Out */}
          <button
            onClick={onLogout}
            className="flex items-center gap-3 px-2.5 py-2 rounded-lg hover:bg-zinc-100 dark:hover:bg-zinc-800 transition-colors"
          >
            <div className="shrink-0 flex items-center justify-center w-[18px]">
              <LogOut size={18} strokeWidth={1.5} className="text-rose-500" />
            </div>
            <span className={`text-sm font-medium text-rose-500 whitespace-nowrap overflow-hidden transition-opacity duration-300 ${sidebarOpen ? 'opacity-100' : 'opacity-0'}`}>
              Log Out
            </span>
          </button>
        </div>

        {/* Collapse toggle */}
        <button
          onClick={() => setSidebarOpen(!sidebarOpen)}
          className="flex items-center gap-3 px-2.5 py-3 mx-2 mb-3 rounded-lg hover:bg-zinc-100 dark:hover:bg-zinc-800 transition-colors"
        >
          <div className={`shrink-0 flex items-center justify-center w-[18px] transition-transform duration-300 ${sidebarOpen ? '' : 'rotate-180'}`}>
            <PanelLeft size={18} strokeWidth={1.5} className="text-zinc-400 dark:text-zinc-500" />
          </div>
          <span className={`text-sm font-medium text-zinc-400 dark:text-zinc-500 whitespace-nowrap overflow-hidden transition-opacity duration-300 ${sidebarOpen ? 'opacity-100' : 'opacity-0'}`}>
            Collapse
          </span>
        </button>
      </aside>

      {/* ─── Mobile Header ───────────────────────────────────────────── */}
      <div className="md:hidden flex items-center justify-between px-4 py-3 border-b border-zinc-200 dark:border-zinc-800 bg-white dark:bg-zinc-900">
        <div className="flex items-center gap-2">
          <div className="w-7 h-7 rounded-lg overflow-hidden bg-zinc-200 dark:bg-zinc-700">
            <img src={getAvatarUrl(avatarSeed)} alt="Avatar" className="w-full h-full object-cover" />
          </div>
          <span className="text-sm font-medium text-zinc-700 dark:text-zinc-300">{getSchoolName(school)}</span>
        </div>
        <button onClick={onLogout} className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium text-rose-500 hover:bg-rose-50 dark:hover:bg-rose-900/20 transition-colors">
          <LogOut size={14} />
          Log Out
        </button>
      </div>

      {/* ─── Main Content ─────────────────────────────────────────────── */}
      <main className={`flex-1 flex flex-col transition-all duration-300 ease-[cubic-bezier(0.16,1,0.3,1)] ${sidebarOpen ? 'md:ml-56' : 'md:ml-[60px]'}`}>
        {/* Freshness strip — this dashboard is a snapshot, not a live feed.
            Saying so beats a GC quietly reading yesterday's numbers. */}
        {!isLoading && (
          <div className="flex items-center justify-end gap-3 px-6 pt-4 pb-1">
            {truncated && (
              <span className="text-[11px] font-medium text-amber-600 dark:text-amber-500">
                Showing the first 1000 accounts — some students may be missing.
              </span>
            )}
            {lastLoadedAt && (
              <span className="text-[11px] text-zinc-400 dark:text-zinc-500">
                Data as of {lastLoadedAt.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
              </span>
            )}
            <button
              onClick={() => setReloadVersion(v => v + 1)}
              className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-lg text-[11px] font-medium text-zinc-500 dark:text-zinc-400 hover:bg-zinc-100 dark:hover:bg-zinc-800 transition-colors"
            >
              <RefreshCw size={12} />
              Refresh
            </button>
          </div>
        )}
        {isLoading ? (
          <LoadingSkeleton />
        ) : activeNav === 'gc-events' ? (
          <div className="p-6 max-w-4xl mx-auto w-full">
            <GCKeyEvents school={school} />
          </div>
        ) : activeNav === 'gc-staff-access' ? (
          <StaffAccessPanel school={school} />
        ) : activeNav === 'gc-handin' ? (
          <>
            <GCAssignPanel school={school} gcName={gcName} />
            <GCHandInGrid
              students={studentData}
              allCourses={allCourses}
              school={school}
              onSelectStudent={(uid) => setSelectedStudentUid(uid)}
            />
          </>
        ) : (
          <GCOverview
            studentData={studentData}
            allCourses={allCourses}
            school={school}
            onSelectStudent={(uid) => setSelectedStudentUid(prev => prev === uid ? null : uid)}
            onDeleteStudent={role === 'gc' ? setDeleteTarget : undefined}
            onResetPassword={role === 'gc' ? setResetTargetUid : undefined}
            alerts={alerts}
            onDismissAlert={handleDismissAlert}
            gcFlags={gcFlags}
          />
        )}
      </main>

      {/* ─── Side Tray Overlay ────────────────────────────────────────── */}
      <AnimatePresence>
        {selectedStudent && (
          <>
            {/* Backdrop */}
            <MotionDiv
              key="backdrop"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              transition={{ duration: 0.2 }}
              className="fixed inset-0 z-40 bg-black/30"
              onClick={() => setSelectedStudentUid(null)}
            />

            {/* Panel */}
            <MotionDiv
              key="tray"
              initial={{ x: '100%' }}
              animate={{ x: 0 }}
              exit={{ x: '100%' }}
              transition={{ duration: 0.4, ease: [0.16, 1, 0.3, 1] }}
              className="fixed top-0 right-0 z-50 h-screen w-full max-w-2xl bg-white dark:bg-zinc-900 shadow-2xl overflow-y-auto border-l border-zinc-200 dark:border-zinc-800"
            >
              {/* Keyed by uid so switching students remounts the tray. Without
                  it React reuses the instance and the previous student's local
                  state (unsent kudos/recommend drafts, the status-change badge)
                  bleeds into the next student's profile. */}
              <GCStudentDetail
                key={selectedStudent.user.uid}
                student={selectedStudent}
                allCourses={allCourses}
                onBack={() => setSelectedStudentUid(null)}
                school={school}
                isTrayMode
                alerts={getStudentAlerts(selectedStudent.user.uid)}
                gcFlags={gcFlags}
              />
            </MotionDiv>
          </>
        )}
      </AnimatePresence>

      {/* Delete confirmation modal */}
      {deleteTarget && (
        <div className="fixed inset-0 z-[200] flex items-center justify-center bg-black/50 backdrop-blur-sm p-4" onClick={() => !isDeleting && closeDeleteDialog()}>
          <div className="bg-white dark:bg-zinc-900 rounded-2xl border border-zinc-200 dark:border-zinc-800 p-6 max-w-sm w-full shadow-2xl" onClick={e => e.stopPropagation()}>
            <div className="flex items-center gap-3 mb-4">
              <div className="w-10 h-10 rounded-xl bg-red-100 dark:bg-red-500/10 flex items-center justify-center text-red-500">
                <AlertTriangle size={20} />
              </div>
              <h3 className="font-semibold text-zinc-900 dark:text-white">Delete Student</h3>
            </div>
            <p className="text-sm text-zinc-600 dark:text-zinc-400 mb-1">
              Are you sure you want to delete <span className="font-semibold text-zinc-900 dark:text-white">{deleteTarget.name}</span>?
            </p>
            <p className="text-xs text-zinc-400 dark:text-zinc-500 mb-6">
              This will permanently remove all their progress and profile. This action cannot be undone.
            </p>
            <label className="block text-xs font-medium text-zinc-500 dark:text-zinc-400 mb-2" htmlFor="delete-verification-password">
              Re-enter your password to continue
            </label>
            <input
              id="delete-verification-password"
              type="password"
              value={deleteVerificationPassword}
              onChange={event => setDeleteVerificationPassword(event.target.value)}
              autoComplete="current-password"
              className="w-full rounded-xl border border-zinc-200 dark:border-zinc-700 bg-white dark:bg-zinc-800 px-4 py-3 text-sm text-zinc-900 dark:text-white mb-5 outline-none focus:border-red-400"
            />
            <div className="flex gap-3">
              <button
                onClick={closeDeleteDialog}
                disabled={isDeleting}
                className="flex-1 px-4 py-2.5 text-sm font-medium rounded-xl border border-zinc-200 dark:border-zinc-700 text-zinc-700 dark:text-zinc-300 hover:bg-zinc-50 dark:hover:bg-zinc-800 transition-colors disabled:opacity-50"
              >
                Cancel
              </button>
              <button
                onClick={() => handleDeleteStudent(deleteTarget)}
                disabled={isDeleting || !deleteVerificationPassword}
                className="flex-1 px-4 py-2.5 text-sm font-medium rounded-xl bg-red-500 text-white hover:bg-red-600 transition-colors disabled:opacity-50"
              >
                {isDeleting ? 'Deleting...' : 'Delete'}
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Password reset verification modal */}
      {resetTargetUid && (
        <div className="fixed inset-0 z-[200] flex items-center justify-center bg-black/50 backdrop-blur-sm p-4" onClick={() => !isResettingPassword && closeResetDialog()}>
          <div role="dialog" aria-modal="true" aria-labelledby="reset-student-title" className="bg-white dark:bg-zinc-900 rounded-2xl border border-zinc-200 dark:border-zinc-800 p-6 max-w-sm w-full shadow-2xl" onClick={event => event.stopPropagation()}>
            <h3 id="reset-student-title" className="font-semibold text-zinc-900 dark:text-white">Reset student password?</h3>
            <p className="text-sm text-zinc-600 dark:text-zinc-400 mt-2 mb-4">This ends the student's other sessions and creates a temporary password that expires after 24 hours.</p>
            <label className="block text-xs font-medium text-zinc-500 dark:text-zinc-400 mb-2" htmlFor="reset-verification-password">Re-enter your password</label>
            <input
              id="reset-verification-password"
              type="password"
              value={resetVerificationPassword}
              onChange={event => setResetVerificationPassword(event.target.value)}
              autoFocus
              autoComplete="current-password"
              className="w-full rounded-xl border border-zinc-200 dark:border-zinc-700 bg-white dark:bg-zinc-800 px-4 py-3 text-sm text-zinc-900 dark:text-white outline-none focus:border-orange-500"
            />
            <div className="flex gap-3 mt-5">
              <button type="button" disabled={isResettingPassword} onClick={closeResetDialog} className="flex-1 px-4 py-2.5 text-sm rounded-xl border border-zinc-200 dark:border-zinc-700 text-zinc-700 dark:text-zinc-300">Cancel</button>
              <button type="button" disabled={isResettingPassword || !resetVerificationPassword} onClick={() => void handleResetPassword(resetTargetUid)} className="flex-1 px-4 py-2.5 text-sm font-semibold rounded-xl bg-orange-600 text-white disabled:opacity-50">
                {isResettingPassword ? 'Resetting…' : 'Reset password'}
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Password reset result modal */}
      {resetResult && (
        <div className="fixed inset-0 z-[200] flex items-center justify-center bg-black/50 backdrop-blur-sm p-4" onClick={() => setResetResult(null)}>
          <div className="bg-white dark:bg-zinc-900 rounded-2xl border border-zinc-200 dark:border-zinc-800 p-6 max-w-sm w-full shadow-2xl" onClick={e => e.stopPropagation()}>
            <h3 className="font-semibold text-zinc-900 dark:text-white mb-2">Password Reset</h3>
            <p className="text-sm text-zinc-600 dark:text-zinc-400 mb-4">
              Temporary password for <span className="font-semibold text-zinc-900 dark:text-white">{resetResult.name}</span>:
            </p>
            <div className="bg-zinc-50 dark:bg-zinc-800 rounded-xl p-4 mb-4 text-center">
              <code className="text-lg font-mono font-bold tracking-widest text-zinc-900 dark:text-white select-all">{resetResult.password}</code>
            </div>
            <p className="text-xs text-zinc-400 dark:text-zinc-500 mb-6">
              Share this with the student. They should change it after logging in.
            </p>
            <button
              onClick={() => setResetResult(null)}
              className="w-full px-4 py-2.5 text-sm font-medium rounded-xl text-white transition-colors"
              style={{ backgroundColor: '#F26B1F' }}
            >
              Done
            </button>
          </div>
        </div>
      )}
    </div>
  );
};
