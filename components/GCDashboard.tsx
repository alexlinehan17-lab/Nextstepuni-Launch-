/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */
import React, { useState, useEffect, useMemo } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { MotionDiv } from './Motion';
import { CourseData } from './Library';
import { SessionUser, getAvatarUrl } from './Auth';
import { GraduationCap, LogOut, LayoutDashboard, Users, BarChart3, PanelLeft, StickyNote, Trash2, AlertTriangle, CalendarDays, Moon, Sun } from 'lucide-react';
import { db } from '../firebase';
import { collection, query, where, getDocs, doc, getDoc, deleteDoc, setDoc } from 'firebase/firestore';
import { getSchoolName } from '../schoolData';
import { UserProgress, PointsData } from '../types';
import { StudentSubjectProfile, TimetableCompletions, TimetableStreak } from './subjectData';
import { NorthStar } from '../types';
import { GameState } from './journeySimulatorData';
import {
  GCStudentFullData,
  JourneyResult,
  MockResultEntry,
} from './gc/gcTypes';
import { DebriefEntry } from './StudyDebrief';
import { GCOverview } from './gc/GCOverview';
import { GCKeyEvents } from './gc/GCKeyEvents';
import { GCStudentDetail } from './gc/GCStudentDetail';
import { generateAlerts, type DismissedAlert, type EarlyWarningAlert } from './gc/gcAlerts';
import { useGCFlags } from '../hooks/useGCFlags';

interface GCDashboardProps {
  school: string;
  onLogout: () => void;
  allCourses: CourseData[];
  gcName?: string;
  gcUid?: string;
}

// ─── Shimmer skeleton ────────────────────────────────────────────────────────

const SkeletonPulse: React.FC<{ className?: string }> = ({ className = '' }) => (
  <div className={`rounded-xl bg-zinc-200 dark:bg-zinc-800 animate-[shine_1.5s_ease-in-out_infinite] ${className}`} />
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

// ─── Component ──────────────────────────────────────────────────────────────

export const GCDashboard: React.FC<GCDashboardProps> = ({ school, onLogout, allCourses, gcName, gcUid }) => {
  const [studentData, setStudentData] = useState<GCStudentFullData[]>([]);
  const [studentNotes, setStudentNotes] = useState<Record<string, { notes: string; updatedAt: string }>>({});
  const [isLoading, setIsLoading] = useState(true);
  const [selectedStudentUid, setSelectedStudentUid] = useState<string | null>(null);
  const [activeNav, setActiveNav] = useState<string>('gc-overview');
  const [sidebarOpen, setSidebarOpen] = useState(false);

  // Restore dark mode preference for GC dashboard
  useEffect(() => {
    const saved = localStorage.getItem('nextstep-gc-dark');
    if (saved === '1') {
      document.documentElement.classList.add('dark');
    }
  }, []);

  const gcFlags = useGCFlags(gcUid);

  const [deleteTarget, setDeleteTarget] = useState<SessionUser | null>(null);
  const [isDeleting, setIsDeleting] = useState(false);
  const [dismissedAlerts, setDismissedAlerts] = useState<Record<string, DismissedAlert>>({});

  const handleDeleteStudent = async (user: SessionUser) => {
    setIsDeleting(true);
    try {
      // Delete progress FIRST (their rules reference the users doc)
      await deleteDoc(doc(db, 'progress', user.uid)).catch(() => {});
      // Then delete the users doc last
      await deleteDoc(doc(db, 'users', user.uid));
      setStudentData(prev => prev.filter(s => s.user.uid !== user.uid));
      if (selectedStudentUid === user.uid) setSelectedStudentUid(null);
    } catch (error) {
      console.error('Error deleting student:', error);
      alert('Failed to delete student. You may not have permission.');
    }
    setIsDeleting(false);
    setDeleteTarget(null);
  };

  // ── Alert dismiss handler ──
  const handleDismissAlert = async (alert: EarlyWarningAlert) => {
    const entry: DismissedAlert = { dismissedAt: Date.now(), metricAtDismissal: alert.metric };
    const updated = { ...dismissedAlerts, [alert.id]: entry };
    setDismissedAlerts(updated);
    try {
      await setDoc(doc(db, 'gcSettings', school), { dismissedAlerts: updated }, { merge: true });
    } catch (err) {
      console.error('[GCAlerts] Failed to save dismissal:', err);
    }
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
    { id: 'gc-events', label: 'Key Dates', icon: CalendarDays, active: activeNav === 'gc-events' },
    { id: 'gc-analytics', label: 'Analytics', icon: BarChart3, active: activeNav === 'gc-analytics' },
    { id: 'gc-students', label: 'Students', icon: Users, active: activeNav === 'gc-students' },
    { id: 'gc-notes', label: 'Notes', icon: StickyNote, active: activeNav === 'gc-notes' },
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

  useEffect(() => {
    let cancelled = false;
    const fetchData = async () => {
      setIsLoading(true);
      try {
        const usersCol = collection(db, 'users');
        const schoolQuery = query(usersCol, where('school', '==', school));
        const userSnapshot = await getDocs(schoolQuery);
        const users = userSnapshot.docs.map(d => ({ uid: d.id, ...d.data() })) as SessionUser[];

        const students = users.filter(u => u.role !== 'gc' && u.role !== 'admin');

        const fullData: GCStudentFullData[] = await Promise.all(
          students.map(async (user) => {
            let progressDoc: Record<string, any> | null = null;

            try {
              const progressSnap = await getDoc(doc(db, 'progress', user.uid));
              progressDoc = progressSnap.exists() ? progressSnap.data() : null;
            } catch { /* Permission error */ }

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
            const journeyRaw = progressDoc?.['journey-simulator'] as { endingId?: string; finalStats?: GameState; completedAt?: string; decisionsCount?: number } | undefined;
            const journeyResult: JourneyResult | null = journeyRaw?.endingId
              ? { endingId: journeyRaw.endingId, finalStats: journeyRaw.finalStats!, completedAt: journeyRaw.completedAt, decisionsCount: journeyRaw.decisionsCount }
              : null;
            const streak = (progressDoc?.timetableStreak as TimetableStreak) ?? null;
            const points = (progressDoc?.pointsData as PointsData) ?? null;
            const timetableCompletions = (progressDoc?.timetableCompletions as TimetableCompletions) ?? null;

            // Cross-tool integration fields
            const ffRaw = progressDoc?.futureFinder as { topPicks?: string[]; completedAt?: string } | undefined;
            const futureFinder = ffRaw?.topPicks ? { topPicks: ffRaw.topPicks, completedAt: ffRaw.completedAt ?? '' } : null;

            const wrMocks = (progressDoc?.warRoom as { mockResults?: MockResultEntry[] })?.mockResults ?? null;

            const debriefArr = progressDoc?.studyDebriefs as DebriefEntry[] | undefined;
            const recentDebriefs = debriefArr ? debriefArr.slice(-20) : null;

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
              mockResults: wrMocks,
              recentDebriefs,
            };
          })
        );

        if (cancelled) return;
        setStudentData(fullData);

        // Fetch all GC notes for this school
        try {
          const notesCol = collection(db, 'gcNotes', school, 'students');
          const notesSnapshot = await getDocs(notesCol);
          if (cancelled) return;
          const notes: Record<string, { notes: string; updatedAt: string }> = {};
          notesSnapshot.docs.forEach(d => {
            const data = d.data();
            if (data.notes) {
              notes[d.id] = { notes: data.notes, updatedAt: data.updatedAt ?? '' };
            }
          });
          setStudentNotes(notes);
        } catch { /* Permission error or no notes yet */ }

        // Load dismissed alerts
        try {
          const settingsSnap = await getDoc(doc(db, 'gcSettings', school));
          if (cancelled) return;
          if (settingsSnap.exists()) {
            setDismissedAlerts(settingsSnap.data().dismissedAlerts ?? {});
          }
        } catch { /* No settings yet */ }
      } catch (error) {
        console.error('Error fetching GC data:', error);
      }
      if (!cancelled) setIsLoading(false);
    };

    fetchData();
    return () => { cancelled = true; };
  }, [school]);

  const selectedStudent = selectedStudentUid
    ? studentData.find(s => s.user.uid === selectedStudentUid) ?? null
    : null;

  const handleNavClick = (sectionId: string) => {
    setActiveNav(sectionId);
    const el = document.getElementById(sectionId);
    if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' });
  };

  return (
    <div className="min-h-screen bg-[#FAF9F6] dark:bg-zinc-950 relative">
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
          {/* Dark Mode Toggle */}
          <button
            onClick={() => {
              const isDark = document.documentElement.classList.toggle('dark');
              localStorage.setItem('nextstep-gc-dark', isDark ? '1' : '0');
            }}
            className="flex items-center gap-3 px-2.5 py-2 rounded-lg hover:bg-zinc-100 dark:hover:bg-zinc-800 transition-colors"
          >
            <div className="shrink-0 flex items-center justify-center w-[18px]">
              <Moon size={18} strokeWidth={1.5} className="text-zinc-400 dark:text-zinc-500 dark:hidden" />
              <Sun size={18} strokeWidth={1.5} className="text-amber-400 hidden dark:block" />
            </div>
            <span className={`text-sm font-medium text-zinc-500 dark:text-zinc-400 whitespace-nowrap overflow-hidden transition-opacity duration-300 ${sidebarOpen ? 'opacity-100' : 'opacity-0'}`}>
              <span className="dark:hidden">Dark Mode</span>
              <span className="hidden dark:inline">Light Mode</span>
            </span>
          </button>

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
        {isLoading ? (
          <LoadingSkeleton />
        ) : activeNav === 'gc-events' ? (
          <div className="p-6 max-w-4xl mx-auto w-full">
            <GCKeyEvents school={school} />
          </div>
        ) : (
          <GCOverview
            studentData={studentData}
            allCourses={allCourses}
            school={school}
            studentNotes={studentNotes}
            onSelectStudent={(uid) => setSelectedStudentUid(prev => prev === uid ? null : uid)}
            onDeleteStudent={setDeleteTarget}
            alerts={alerts}
            onDismissAlert={handleDismissAlert}
            gcName={gcName}
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
              <GCStudentDetail
                student={selectedStudent}
                allCourses={allCourses}
                onBack={() => setSelectedStudentUid(null)}
                school={school}
                isTrayMode
                onNoteSaved={(uid, notes, updatedAt) => {
                  setStudentNotes(prev => ({ ...prev, [uid]: { notes, updatedAt } }));
                }}
                alerts={getStudentAlerts(selectedStudent.user.uid)}
                gcName={gcName}
                gcFlags={gcFlags}
              />
            </MotionDiv>
          </>
        )}
      </AnimatePresence>

      {/* Delete confirmation modal */}
      {deleteTarget && (
        <div className="fixed inset-0 z-[200] flex items-center justify-center bg-black/50 backdrop-blur-sm p-4" onClick={() => !isDeleting && setDeleteTarget(null)}>
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
            <div className="flex gap-3">
              <button
                onClick={() => setDeleteTarget(null)}
                disabled={isDeleting}
                className="flex-1 px-4 py-2.5 text-sm font-medium rounded-xl border border-zinc-200 dark:border-zinc-700 text-zinc-700 dark:text-zinc-300 hover:bg-zinc-50 dark:hover:bg-zinc-800 transition-colors disabled:opacity-50"
              >
                Cancel
              </button>
              <button
                onClick={() => handleDeleteStudent(deleteTarget)}
                disabled={isDeleting}
                className="flex-1 px-4 py-2.5 text-sm font-medium rounded-xl bg-red-500 text-white hover:bg-red-600 transition-colors disabled:opacity-50"
              >
                {isDeleting ? 'Deleting...' : 'Delete'}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
