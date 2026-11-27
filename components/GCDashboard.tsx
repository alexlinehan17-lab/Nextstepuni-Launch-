/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */
import React, { useState, useEffect, useMemo, useRef } from 'react';
import { type CourseData } from './Library';
import { type SessionUser, yearGroupToCurriculumLevel } from '../utils/authUtils';
import { LogOut, House, Users, ChartNoAxesColumn, LayoutGrid, CalendarDays, Lock, RefreshCw, User } from 'lucide-react';
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
import { TopBar, TabBar, type TabBarItem } from './ui/Bars';
import { Button, IconButton, TextButton } from './ui/Button';
import { Sheet } from './ui/Sheet';
import { Field } from './ui/Field';
import { List, Row } from './ui/List';
import { MenuAction, MenuPanel } from './ui/Menu';
import { LoadingShape } from './ui/States';
import { OverScreen } from './ui/OverScreen';
import { FramePortal } from './ui/Frame';
import { useWide } from './gc/gcView';

interface GCDashboardProps {
  school: string;
  onLogout: () => void;
  allCourses: CourseData[];
  gcName?: string;
  gcUid?: string;
  role?: SessionUser['role'];
}

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
  // The dashboard is a one-shot snapshot (the /progress read rule authorises
  // get()-shaped reads only, so onSnapshot is not available here). Make the
  // staleness visible instead of silent, and give the GC a way to re-pull.
  const [lastLoadedAt, setLastLoadedAt] = useState<Date | null>(null);
  const [reloadVersion, setReloadVersion] = useState(0);
  const [truncated, setTruncated] = useState(false);

  // The dashboard no longer forces dark: it sits on the white page, and goes dark only where this
  // browser's own theme setting says so (Alex, 24 Nov 2026: every part "restyled in the new system").

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

  // The places. On a laptop the staff sidebar lists them as today (Notes, which went nowhere, is left out
  // as the agreed board shows); on a phone the four along the bottom (Practice and Key dates were out of
  // reach on a phone before). School access stays a counsellor's page only, as today.
  const wide = useWide();
  const sidebarItems = [
    { id: 'gc-overview', label: 'Overview', icon: House },
    { id: 'gc-handin', label: 'Practice', icon: LayoutGrid },
    { id: 'gc-events', label: 'Key dates', icon: CalendarDays },
    { id: 'gc-analytics', label: 'Analytics', icon: ChartNoAxesColumn },
    { id: 'gc-students', label: 'Students', icon: Users },
    ...(role === 'gc' ? [{ id: 'gc-staff-access', label: 'School access', icon: Lock }] : []),
  ];
  const tabItems: TabBarItem<string>[] = [
    { id: 'gc-overview', label: 'Overview', icon: House },
    { id: 'gc-students', label: 'Students', icon: Users },
    { id: 'gc-handin', label: 'Practice', icon: LayoutGrid },
    { id: 'gc-events', label: 'Key dates', icon: CalendarDays },
  ];
  const [accountOpen, setAccountOpen] = useState(false);
  const resetFieldRef = useRef<HTMLInputElement>(null);
  const deleteFieldRef = useRef<HTMLInputElement>(null);
  const roleWords = role === 'gc' ? 'Guidance counsellor' : 'Staff';
  const youName = gcName || getSchoolName(school);

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

  // A place on a phone, or a part of the page on a laptop (Overview, Analytics and Students are the one
  // Overview, scrolled to; Practice, Key dates and School access are pages, as today).
  const handleNavClick = (sectionId: string) => {
    setActiveNav(sectionId);
    if (!wide) {
      window.scrollTo(0, 0);
      return;
    }
    // After the page under it has drawn (from Practice, Analytics lands on the Overview first).
    window.setTimeout(() => {
      const el = document.getElementById(sectionId);
      if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' });
      else window.scrollTo(0, 0);
    }, 0);
  };

  const dataAsOf = lastLoadedAt ? lastLoadedAt.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) : null;
  const truncatedLine = truncated ? 'Showing the first 1000 accounts — some students may be missing.' : null;
  const currentTab = activeNav === 'gc-analytics' || activeNav === 'gc-staff-access' ? 'gc-overview' : activeNav;
  const studentsPlace = !wide && activeNav === 'gc-students';

  const page = isLoading ? (
    <LoadingShape rows={6} label="Opening your school dashboard" />
  ) : activeNav === 'gc-events' ? (
    <GCKeyEvents school={school} layout="page" />
  ) : activeNav === 'gc-staff-access' && role === 'gc' ? (
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
      place={studentsPlace ? 'students' : 'overview'}
      onOpenStudents={() => handleNavClick('gc-students')}
      dataAsOf={dataAsOf}
      notice={truncatedLine}
    />
  );

  const closeStudent = () => setSelectedStudentUid(null);

  return (
    <div className="gc8">
      {/* ─── Laptop: the staff sidebar ───────────────────────────────── */}
      {wide && <aside className="gc8-side frame-page frame-foot" aria-label="Staff dashboard">
        <div className="gc8-brand">
          <p className="gc8-wordmark">nextstepuni<i aria-hidden="true">.</i></p>
          <p className="gc8-label">{getSchoolName(school)}</p>
        </div>
        <nav className="gc8-nav" aria-label="Staff dashboard">
          {sidebarItems.map(item => (
            <button
              key={item.id}
              type="button"
              className="gc8-nav-item"
              aria-current={activeNav === item.id ? 'page' : undefined}
              onClick={() => handleNavClick(item.id)}
            >
              <item.icon className="ui-icon" width={20} height={20} strokeWidth={1.75} aria-hidden="true" />
              {item.label}
            </button>
          ))}
        </nav>
        <MenuPanel
          label="Your account"
          buttonLabel={`Your account: ${youName}`}
          buttonClassName="gc8-user"
          className="gc8-usermenu"
          align="start"
          side="top"
          face={<>
            <span className="gc8-user-box"><User className="ui-icon" width={20} height={20} strokeWidth={1.75} aria-hidden="true" /></span>
            <span className="gc8-user-copy"><span>{youName}</span><span className="gc8-meta">{roleWords}</span></span>
          </>}
        >
          <MenuAction title="Log out" plain tone="danger" onPress={onLogout} />
        </MenuPanel>
      </aside>}

      <div className="gc8-col">
        {/* ─── Laptop: the bar along the top (the snapshot says when it was taken) ─── */}
        {wide && <div className="gc8-dbar">
          <p className="gc8-label">Staff dashboard</p>
          {!isLoading && (
            <div className="gc8-dbar-end">
              {truncatedLine && <span className="gc8-meta gc8-strong">{truncatedLine}</span>}
              {dataAsOf && <span className="gc8-meta">Data as of {dataAsOf}</span>}
              <TextButton tone="quiet" className="gc8-ib" onClick={() => setReloadVersion(v => v + 1)}>
                <RefreshCw className="ui-icon" width={16} height={16} strokeWidth={2} aria-hidden="true" />Refresh
              </TextButton>
            </div>
          )}
        </div>}

        {/* ─── Phone: the place's bar, your account at the top right ─── */}
        {!wide && (
          <TopBar
            className="gc8-placebar"
            placeLabel={getSchoolName(school)}
            action={
              <IconButton className="gc8-me" label="Your account" onClick={() => setAccountOpen(true)}
                icon={<span><User className="ui-icon" width={20} height={20} strokeWidth={1.75} aria-hidden="true" /></span>} />
            }
          />
        )}

        <main className="gc8-main">{page}</main>

        {!wide && <TabBar className="gc8-tabbar" label="Staff dashboard" items={tabItems} current={currentTab} onSelect={handleNavClick} />}
      </div>

      {/* ─── Phone: your account (Refresh and Log out, which sat in the status band) ─── */}
      <Sheet
        open={accountOpen && !wide}
        onClose={() => setAccountOpen(false)}
        title={youName}
        meta={roleWords}
        art={<span className="gc8-user-box"><User className="ui-icon" width={20} height={20} strokeWidth={1.75} aria-hidden="true" /></span>}
      >
        <List>
          <Row
            icon={<RefreshCw />}
            title="Refresh"
            trailing={<span aria-hidden="true" />}
            meta={[dataAsOf ? `Data as of ${dataAsOf}` : null, truncatedLine].filter(Boolean).join(' · ') || undefined}
            onPress={() => { setReloadVersion(v => v + 1); setAccountOpen(false); }}
          />
          <Row icon={<LogOut />} title="Log out" tone="danger" trailing={<span aria-hidden="true" />} onPress={onLogout} />
        </List>
      </Sheet>

      {/* ─── One student: a page with Back on a phone, the side tray on a laptop ─── */}
      {selectedStudent && (
        <>
          {wide && <FramePortal><div className="frame-takeover gc8-scrim" aria-hidden="true" onClick={closeStudent} /></FramePortal>}
          <OverScreen
            label={`Student profile: ${selectedStudent.user.name}`}
            // Escape belongs to a menu open on the student first (sheets take it themselves).
            onEscape={() => { if (!document.querySelector('.ui-menu')) closeStudent(); }}
            className={wide ? 'gc8-over gc8-tray' : 'gc8-over'}
          >
            {/* Keyed by uid so switching students remounts the tray. Without
                it React reuses the instance and the previous student's local
                state (unsent kudos/recommend drafts, the status-change badge)
                bleeds into the next student's profile. */}
            <GCStudentDetail
              key={selectedStudent.user.uid}
              student={selectedStudent}
              allCourses={allCourses}
              onBack={closeStudent}
              school={school}
              isTrayMode
              alerts={getStudentAlerts(selectedStudent.user.uid)}
              gcFlags={gcFlags}
              onDismissAlert={handleDismissAlert}
              onResetPassword={role === 'gc' ? setResetTargetUid : undefined}
              onDeleteStudent={role === 'gc' ? setDeleteTarget : undefined}
              wide={wide}
            />
          </OverScreen>
        </>
      )}

      {/* Delete confirmation: the safe choice is the main button, the destructive one red text. */}
      <Sheet
        open={!!deleteTarget}
        plain
        title="Delete student"
        onClose={() => { if (!isDeleting) closeDeleteDialog(); }}
        footer={
          <div className="gc8-sheet-foot">
            <Button kind="main" size="lg" block onClick={closeDeleteDialog}>Cancel</Button>
            <TextButton
              tone="danger"
              aria-disabled={isDeleting || !deleteVerificationPassword || undefined}
              onClick={() => {
                if (isDeleting) return;
                if (!deleteVerificationPassword) { deleteFieldRef.current?.focus(); return; }
                if (deleteTarget) void handleDeleteStudent(deleteTarget);
              }}
            >
              {isDeleting ? 'Deleting...' : 'Delete'}
            </TextButton>
          </div>
        }
      >
        <div className="gc8-sheet-body">
          <div className="gc8-reading">
            <p>Are you sure you want to delete <b>{deleteTarget?.name}</b>?</p>
            <p className="gc8-meta">This will permanently remove all their progress and profile. This action cannot be undone.</p>
          </div>
          <Field
            ref={deleteFieldRef}
            id="delete-verification-password"
            type="password"
            label="Re-enter your password to continue"
            value={deleteVerificationPassword}
            onChange={event => setDeleteVerificationPassword(event.target.value)}
            autoComplete="current-password"
          />
        </div>
      </Sheet>

      {/* Password reset: verify, then the temporary password */}
      <Sheet
        open={!!resetTargetUid}
        title="Reset student password?"
        onClose={() => { if (!isResettingPassword) closeResetDialog(); }}
        footer={
          <Button
            kind="main"
            size="lg"
            block
            missing={!resetVerificationPassword ? { sentence: 'Re-enter your password to continue.', goTo: resetFieldRef } : undefined}
            onClick={() => { if (!isResettingPassword && resetTargetUid) void handleResetPassword(resetTargetUid); }}
          >
            {isResettingPassword ? 'Resetting…' : 'Reset password'}
          </Button>
        }
      >
        <div className="gc8-sheet-body">
          <p className="gc8-sub">This ends the student's other sessions and creates a temporary password that expires after 24 hours.</p>
          <Field
            ref={resetFieldRef}
            id="reset-verification-password"
            type="password"
            label="Re-enter your password"
            value={resetVerificationPassword}
            onChange={event => setResetVerificationPassword(event.target.value)}
            autoComplete="current-password"
          />
        </div>
      </Sheet>

      <Sheet
        open={!!resetResult}
        plain
        title="Password reset"
        onClose={() => setResetResult(null)}
        footer={<Button kind="main" size="lg" block onClick={() => setResetResult(null)}>Done</Button>}
      >
        <div className="gc8-sheet-body">
          <p className="gc8-sub">Temporary password for <span className="gc8-strong">{resetResult?.name}</span>:</p>
          <div className="gc8-secret"><code className="gc8-code-value">{resetResult?.password}</code></div>
          <p className="gc8-meta">Share this with the student. They should change it after logging in.</p>
        </div>
      </Sheet>
    </div>
  );
};
