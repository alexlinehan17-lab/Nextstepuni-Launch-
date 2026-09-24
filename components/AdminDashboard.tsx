/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useEffect, useMemo, useRef, useState } from 'react';
import {
  AlertTriangle,
  BookOpenCheck,
  ChevronRight,
  GraduationCap,
  LogOut,
  RefreshCw,
  Trash2,
  UserRoundCheck,
  Users,
} from 'lucide-react';
import {
  collection,
  documentId,
  getDocs,
  limit,
  orderBy,
  query,
  startAfter,
  where,
  type DocumentData,
  type QueryDocumentSnapshot,
} from 'firebase/firestore';
import { getFunctions, httpsCallable } from 'firebase/functions';
import { MotionDiv } from './Motion';
import { type CourseData } from './Library';
import { type CategoryType } from './KnowledgeTree';
import {
  type SessionUser,
  getAvatarUrl,
  handleAvatarError,
} from '../utils/authUtils';
import app, { auth, db } from '../firebase';
import { SCHOOLS, getSchoolName } from '../schoolData';
import { type StudentSubjectProfile, type YearGroup } from './subjectData';
import { filterCoursesForStudent } from '../utils/courseVisibility';
import AdminFeedbackInbox from './AdminFeedbackInbox';
import AdminFunnelPanel from './AdminFunnelPanel';
import AdminGcAccessPanel from './AdminGcAccessPanel';
import AdminProgrammePanel from './AdminProgrammePanel';
import { reauthMethodFor, reauthenticateCurrentUser } from '../utils/reauthenticate';
import { yearGroupToCurriculumLevel } from '../utils/authUtils';

type ModuleProgress = {
  unlockedSection: number;
};

type UserProgress = {
  [moduleId: string]: ModuleProgress;
};

type AllUserProgress = {
  [uid: string]: UserProgress;
};

type StudentRecord = {
  user: SessionUser;
  progress: UserProgress;
  subjectProfile: StudentSubjectProfile | null;
};

type StudentMetrics = {
  overallProgress: number;
  startedCourses: number;
  completedCourses: number;
};

type EnrichedStudentRecord = StudentRecord & {
  metrics: StudentMetrics;
  resolvedYearGroup?: YearGroup;
  visibleCourses: CourseData[];
};

type AdminView =
  | 'overview'
  | 'programme'
  | 'students'
  | 'schools'
  | 'years'
  | 'funnel'
  | 'feedback'
  | 'gc-access';

interface AdminDashboardProps {
  allCourses: CourseData[];
  onLogout: () => void;
}

interface CohortStats {
  students: number;
  started: number;
  startRate: number;
  averageProgress: number;
  completedOne: number;
}

const CATEGORIES: { id: CategoryType; title: string }[] = [
  { id: 'architecture-mindset', title: 'The Architecture of your Mindset' },
  { id: 'science-growth', title: 'The Science of Growth' },
  { id: 'learning-cheat-codes', title: 'The Science of Learning Effectively' },
  { id: 'subject-specific-science', title: 'Decoding the Subjects' },
  { id: 'exam-zone', title: 'Exam Strategy and Points Maximisation' },
];

const NAV_ITEMS: { id: AdminView; label: string }[] = [
  { id: 'overview', label: 'Overview' },
  { id: 'programme', label: 'Programme' },
  { id: 'students', label: 'Students' },
  { id: 'schools', label: 'Schools' },
  { id: 'years', label: 'Year groups' },
  { id: 'funnel', label: 'First run' },
  { id: 'feedback', label: 'Feedback' },
  { id: 'gc-access', label: 'School access' },
];

const YEAR_GROUPS = ['1st', '2nd', '3rd', 'TY', '5th', '6th', 'LCA1', 'LCA2', 'graduated'] as const;
const NOT_SET = '__not_set__';

const YEAR_LABELS: Record<string, string> = {
  '1st': '1st Year',
  '2nd': '2nd Year',
  '3rd': '3rd Year',
  TY: 'Transition Year',
  '5th': '5th Year',
  '6th': '6th Year',
  LCA1: 'LCA Year 1',
  LCA2: 'LCA Year 2',
  graduated: 'Graduated',
  [NOT_SET]: 'Not set',
};

function calculateStudentMetrics(progress: UserProgress, allCourses: CourseData[]): StudentMetrics {
  let progressTotal = 0;
  let startedCourses = 0;
  let completedCourses = 0;

  allCourses.forEach(course => {
    const courseProgress = progress[course.id];
    if (!courseProgress || typeof courseProgress.unlockedSection !== 'number' || course.sectionsCount <= 0) return;
    const percentage = Math.min(100, Math.max(0, (courseProgress.unlockedSection / course.sectionsCount) * 100));
    progressTotal += percentage;
    if (courseProgress.unlockedSection > 0) startedCourses += 1;
    if (percentage >= 100) completedCourses += 1;
  });

  return {
    overallProgress: allCourses.length > 0 ? progressTotal / allCourses.length : 0,
    startedCourses,
    completedCourses,
  };
}

function summariseCohort(records: EnrichedStudentRecord[]): CohortStats {
  const students = records.length;
  const started = records.filter(record => record.metrics.startedCourses > 0).length;
  const averageProgress = students > 0
    ? records.reduce((sum, record) => sum + record.metrics.overallProgress, 0) / students
    : 0;
  return {
    students,
    started,
    startRate: students > 0 ? Math.round((started / students) * 100) : 0,
    averageProgress,
    completedOne: records.filter(record => record.metrics.completedCourses > 0).length,
  };
}

function displaySchool(school?: string): string {
  if (!school || school === NOT_SET) return 'School not set';
  return getSchoolName(school);
}

function displayYear(yearGroup?: string): string {
  return YEAR_LABELS[yearGroup || NOT_SET] || yearGroup || YEAR_LABELS[NOT_SET];
}

function formatDate(): string {
  return new Intl.DateTimeFormat('en-IE', {
    weekday: 'long',
    day: 'numeric',
    month: 'long',
  }).format(new Date());
}

const FilterControls: React.FC<{
  schoolFilter: string;
  yearFilter: string;
  schoolOptions: string[];
  yearOptions: string[];
  onSchoolChange: (value: string) => void;
  onYearChange: (value: string) => void;
}> = ({ schoolFilter, yearFilter, schoolOptions, yearOptions, onSchoolChange, onYearChange }) => (
  <div className="flex flex-wrap items-end gap-3" aria-label="Dashboard filters">
    <label className="min-w-[180px] flex-1 sm:flex-none">
      <span className="mb-1.5 block text-xs font-bold uppercase tracking-[0.12em] text-[#7A7068]">School</span>
      <select
        value={schoolFilter}
        onChange={event => onSchoolChange(event.target.value)}
        className="w-full rounded-lg border-2 border-[#1A1A1A] bg-white px-3 py-2.5 text-sm font-semibold text-[#1A1A1A] outline-none focus:border-[#F26B1F] sm:w-[220px]"
      >
        <option value="all">All schools</option>
        {schoolOptions.map(school => <option key={school} value={school}>{displaySchool(school)}</option>)}
      </select>
    </label>
    <label className="min-w-[165px] flex-1 sm:flex-none">
      <span className="mb-1.5 block text-xs font-bold uppercase tracking-[0.12em] text-[#7A7068]">Year group</span>
      <select
        value={yearFilter}
        onChange={event => onYearChange(event.target.value)}
        className="w-full rounded-lg border-2 border-[#1A1A1A] bg-white px-3 py-2.5 text-sm font-semibold text-[#1A1A1A] outline-none focus:border-[#F26B1F] sm:w-[190px]"
      >
        <option value="all">All year groups</option>
        {yearOptions.map(year => <option key={year} value={year}>{displayYear(year)}</option>)}
      </select>
    </label>
  </div>
);

const StudentProgressCard: React.FC<{
  record: EnrichedStudentRecord;
  onDelete: (user: SessionUser) => void;
}> = ({ record, onDelete }) => {
  const { user, progress, metrics, resolvedYearGroup, visibleCourses } = record;

  const calculateCategoryProgress = (category: CategoryType) => {
    const categoryCourses = visibleCourses.filter(course => course.category === category);
    if (categoryCourses.length === 0) return 0;
    const totalProgress = categoryCourses.reduce((sum, course) => {
      const courseProgress = progress[course.id];
      if (!courseProgress || typeof courseProgress.unlockedSection !== 'number' || course.sectionsCount <= 0) return sum;
      return sum + Math.min(100, (courseProgress.unlockedSection / course.sectionsCount) * 100);
    }, 0);
    return totalProgress / categoryCourses.length;
  };

  return (
    <article className="rounded-xl border-2 border-[#1A1A1A] bg-white p-5">
      <div className="mb-5 flex items-center gap-3 border-b border-[#DDD8D2] pb-4">
        <img
          src={getAvatarUrl(user.avatar)}
          onError={event => handleAvatarError(event, user.avatar || user.name)}
          alt=""
          className="h-11 w-11 rounded-full bg-[#E8E8E8]"
        />
        <div className="min-w-0 flex-1">
          <h3 className="truncate text-base font-bold text-[#1A1A1A]">{user.name}</h3>
          <p className="mt-0.5 truncate text-xs text-[#7A7068]">
            {displaySchool(user.school)} · {displayYear(resolvedYearGroup)}
          </p>
        </div>
        <button
          type="button"
          onClick={() => onDelete(user)}
          className="flex h-9 w-9 shrink-0 items-center justify-center rounded-full border-2 border-transparent text-[#7A7068] hover:border-[#B42318] hover:text-[#B42318] focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[#B42318]"
          aria-label={`Delete ${user.name}`}
        >
          <Trash2 size={16} />
        </button>
      </div>

      <div className="mb-5 grid grid-cols-3 divide-x divide-[#DDD8D2] border-y border-[#DDD8D2] py-3 text-center">
        <div>
          <strong className="block font-serif text-2xl text-[#1A1A1A]">{metrics.overallProgress.toFixed(0)}%</strong>
          <span className="text-xs text-[#7A7068]">Overall</span>
        </div>
        <div>
          <strong className="block font-serif text-2xl text-[#1A1A1A]">{metrics.startedCourses}</strong>
          <span className="text-xs text-[#7A7068]">Started</span>
        </div>
        <div>
          <strong className="block font-serif text-2xl text-[#1A1A1A]">{metrics.completedCourses}</strong>
          <span className="text-xs text-[#7A7068]">Complete</span>
        </div>
      </div>

      <div className="space-y-3">
        {CATEGORIES.map(category => {
          const categoryProgress = calculateCategoryProgress(category.id);
          return (
            <div key={category.id}>
              <div className="flex items-center justify-between gap-4">
                <p className="truncate text-xs font-semibold text-[#3A3530]">{category.title}</p>
                <p className="text-xs font-bold tabular-nums text-[#7A7068]">{categoryProgress.toFixed(0)}%</p>
              </div>
              <div className="mt-1.5 h-2 w-full overflow-hidden rounded-full bg-[#E0DBD4]">
                <MotionDiv
                  className={`h-full rounded-full ${categoryProgress >= 100 ? 'bg-[#3A8D5F]' : 'bg-[#F26B1F]'}`}
                  initial={{ width: 0 }}
                  animate={{ width: `${categoryProgress}%` }}
                  transition={{ duration: 0.45, ease: 'easeOut' }}
                />
              </div>
            </div>
          );
        })}
      </div>
    </article>
  );
};

const MetricCard: React.FC<{
  label: string;
  value: string | number;
  detail: string;
  icon: React.ReactNode;
  positive?: boolean;
}> = ({ label, value, detail, icon, positive = false }) => (
  <article className="min-w-0 rounded-xl border-2 border-[#1A1A1A] bg-white p-4 sm:p-5">
    <div className="flex items-start justify-between gap-3">
      <span className="text-xs font-bold uppercase tracking-[0.12em] text-[#7A7068]">{label}</span>
      <span className={positive ? 'text-[#3A8D5F]' : 'text-[#F26B1F]'}>{icon}</span>
    </div>
    <strong className="mt-3 block font-serif text-3xl font-bold tabular-nums text-[#1A1A1A] sm:text-4xl">{value}</strong>
    <span className="mt-1 block text-xs leading-relaxed text-[#7A7068]">{detail}</span>
  </article>
);

const ProgressDistribution: React.FC<{ records: EnrichedStudentRecord[] }> = ({ records }) => {
  const groups = [
    { label: 'Not started', count: records.filter(record => record.metrics.startedCourses === 0).length, colour: '#A8A29E' },
    { label: 'Getting started', count: records.filter(record => record.metrics.startedCourses > 0 && record.metrics.overallProgress < 25).length, colour: '#F26B1F' },
    { label: 'Building progress', count: records.filter(record => record.metrics.overallProgress >= 25 && record.metrics.overallProgress < 75).length, colour: '#F26B1F' },
    { label: 'Advanced', count: records.filter(record => record.metrics.overallProgress >= 75).length, colour: '#3A8D5F' },
  ];

  return (
    <section className="rounded-xl border-2 border-[#1A1A1A] bg-white p-5 sm:p-6" aria-labelledby="progress-distribution-title">
      <p className="text-xs font-bold uppercase tracking-[0.14em] text-[#9E9186]">Learning progress</p>
      <h2 id="progress-distribution-title" className="mt-1 font-serif text-2xl font-semibold text-[#1A1A1A]">Where students currently sit</h2>
      <div className="mt-6 space-y-5">
        {groups.map(group => {
          const percentage = records.length > 0 ? Math.round((group.count / records.length) * 100) : 0;
          return (
            <div key={group.label}>
              <div className="mb-2 flex items-baseline justify-between gap-4">
                <span className="text-sm font-semibold text-[#3A3530]">{group.label}</span>
                <span className="text-sm font-bold tabular-nums text-[#1A1A1A]">{group.count} <span className="font-normal text-[#7A7068]">({percentage}%)</span></span>
              </div>
              <div className="h-2.5 overflow-hidden rounded-full bg-[#E0DBD4]">
                <div className="h-full rounded-full" style={{ width: `${percentage}%`, backgroundColor: group.colour }} />
              </div>
            </div>
          );
        })}
      </div>
    </section>
  );
};

const CohortTable: React.FC<{
  title: string;
  eyebrow: string;
  rows: { key: string; label: string; stats: CohortStats }[];
  emptyLabel: string;
  onOpen: (key: string) => void;
}> = ({ title, eyebrow, rows, emptyLabel, onOpen }) => (
  <section className="overflow-hidden rounded-xl border-2 border-[#1A1A1A] bg-white">
    <div className="flex flex-wrap items-end justify-between gap-3 border-b-2 border-[#1A1A1A] px-5 py-4 sm:px-6">
      <div>
        <p className="text-xs font-bold uppercase tracking-[0.14em] text-[#9E9186]">{eyebrow}</p>
        <h2 className="mt-1 font-serif text-2xl font-semibold text-[#1A1A1A]">{title}</h2>
      </div>
      <span className="text-xs text-[#7A7068]">Existing student records</span>
    </div>
    <div className="overflow-x-auto">
      <table className="w-full min-w-[700px] border-collapse text-left">
        <thead className="bg-[#F0F0F0] text-xs uppercase tracking-[0.1em] text-[#7A7068]">
          <tr>
            <th className="px-5 py-3 font-bold">Cohort</th>
            <th className="px-4 py-3 font-bold">Students</th>
            <th className="px-4 py-3 font-bold">Started</th>
            <th className="px-4 py-3 font-bold">Average progress</th>
            <th className="px-4 py-3 font-bold">Completed a course</th>
            <th className="px-5 py-3"><span className="sr-only">Open students</span></th>
          </tr>
        </thead>
        <tbody className="divide-y divide-[#DDD8D2]">
          {rows.length > 0 ? rows.map(row => (
            <tr key={row.key} className="text-sm text-[#3A3530]">
              <td className="px-5 py-4 font-bold text-[#1A1A1A]">{row.label}</td>
              <td className="px-4 py-4 tabular-nums">{row.stats.students}</td>
              <td className="px-4 py-4 tabular-nums">{row.stats.started} <span className="text-[#7A7068]">({row.stats.startRate}%)</span></td>
              <td className="px-4 py-4 font-semibold tabular-nums">{row.stats.averageProgress.toFixed(0)}%</td>
              <td className="px-4 py-4 tabular-nums">{row.stats.completedOne}</td>
              <td className="px-5 py-4 text-right">
                <button
                  type="button"
                  onClick={() => onOpen(row.key)}
                  aria-label={`Open students in ${row.label}`}
                  className="inline-flex items-center gap-1 rounded-full border-2 border-[#1A1A1A] bg-white px-3 py-1.5 text-xs font-bold text-[#1A1A1A] hover:border-[#F26B1F] hover:text-[#B54D14]"
                >
                  Students <ChevronRight size={13} />
                </button>
              </td>
            </tr>
          )) : (
            <tr><td colSpan={6} className="px-5 py-10 text-center text-sm text-[#7A7068]">{emptyLabel}</td></tr>
          )}
        </tbody>
      </table>
    </div>
  </section>
);

export const AdminDashboard: React.FC<AdminDashboardProps> = ({ allCourses, onLogout }) => {
  const [studentData, setStudentData] = useState<StudentRecord[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [loadError, setLoadError] = useState('');
  const [reloadToken, setReloadToken] = useState(0);
  const [deleteTarget, setDeleteTarget] = useState<SessionUser | null>(null);
  const [isDeleting, setIsDeleting] = useState(false);
  const [deleteVerificationPassword, setDeleteVerificationPassword] = useState('');
  const [activeView, setActiveView] = useState<AdminView>('overview');
  const [schoolFilter, setSchoolFilter] = useState('all');
  const [yearFilter, setYearFilter] = useState('all');
  const deleteDialogRef = useRef<HTMLDivElement>(null);
  const cancelDeleteButtonRef = useRef<HTMLButtonElement>(null);
  const isDeletingRef = useRef(false);

  useEffect(() => {
    isDeletingRef.current = isDeleting;
    if (isDeleting) deleteDialogRef.current?.focus();
  }, [isDeleting]);

  const closeDeleteDialog = () => {
    setDeleteVerificationPassword('');
    setDeleteTarget(null);
  };

  const handleDeleteStudent = async (user: SessionUser) => {
    setIsDeleting(true);
    try {
      if (!auth.currentUser) throw new Error('No administrator is signed in.');
      await reauthenticateCurrentUser(auth.currentUser, deleteVerificationPassword);
      const functions = getFunctions(app);
      const deleteFn = httpsCallable<{ uid: string }, { success: boolean }>(functions, 'requestAccountDeletion');
      await deleteFn({ uid: user.uid });
      setStudentData(previous => previous.filter(record => record.user.uid !== user.uid));
    } catch (error) {
      console.error('Error deleting student:', error);
      alert('Failed to delete student. You may not have permission.');
    } finally {
      setIsDeleting(false);
      setDeleteVerificationPassword('');
      closeDeleteDialog();
    }
  };

  useEffect(() => {
    if (!deleteTarget) return;
    const previousFocus = document.activeElement instanceof HTMLElement ? document.activeElement : null;
    const focusFrame = window.requestAnimationFrame(() => cancelDeleteButtonRef.current?.focus());
    const handleDialogKeyDown = (event: KeyboardEvent) => {
      if (event.key === 'Escape' && !isDeletingRef.current) {
        event.preventDefault();
        setDeleteVerificationPassword('');
        setDeleteTarget(null);
        return;
      }
      if (event.key !== 'Tab' || !deleteDialogRef.current) return;
      const focusable = [...deleteDialogRef.current.querySelectorAll<HTMLElement>(
        'button:not([disabled]), input:not([disabled]), select:not([disabled]), textarea:not([disabled]), [tabindex]:not([tabindex="-1"])',
      )];
      if (focusable.length === 0) {
        event.preventDefault();
        deleteDialogRef.current.focus();
        return;
      }
      const first = focusable[0];
      const last = focusable[focusable.length - 1];
      if (!deleteDialogRef.current.contains(document.activeElement) || document.activeElement === deleteDialogRef.current) {
        event.preventDefault();
        (event.shiftKey ? last : first).focus();
      } else if (event.shiftKey && document.activeElement === first) {
        event.preventDefault();
        last.focus();
      } else if (!event.shiftKey && document.activeElement === last) {
        event.preventDefault();
        first.focus();
      }
    };
    document.addEventListener('keydown', handleDialogKeyDown);
    return () => {
      window.cancelAnimationFrame(focusFrame);
      document.removeEventListener('keydown', handleDialogKeyDown);
      previousFocus?.focus();
    };
  }, [deleteTarget]);

  useEffect(() => {
    let cancelled = false;
    const fetchData = async () => {
      setIsLoading(true);
      setLoadError('');
      try {
        const users: SessionUser[] = [];
        let userCursor: QueryDocumentSnapshot<DocumentData> | null = null;
        const userPageSize = 500;
        let pageLength = 0;
        do {
          const usersQuery = userCursor
            ? query(collection(db, 'users'), orderBy(documentId()), startAfter(userCursor), limit(userPageSize))
            : query(collection(db, 'users'), orderBy(documentId()), limit(userPageSize));
          const usersSnapshot = await getDocs(usersQuery);
          users.push(...usersSnapshot.docs.map(userDoc => ({ uid: userDoc.id, ...userDoc.data() })) as SessionUser[]);
          userCursor = usersSnapshot.docs.at(-1) || null;
          pageLength = usersSnapshot.docs.length;
        } while (pageLength === userPageSize && userCursor);
        const students = users.filter(user => !user.isAdmin && user.role !== 'gc' && user.role !== 'staff' && user.role !== 'admin');
        const allProgress: AllUserProgress = {};
        const ids = students.map(student => student.uid);

        for (let index = 0; index < ids.length; index += 30) {
          const chunk = ids.slice(index, index + 30);
          const snapshot = await getDocs(query(collection(db, 'progress'), where(documentId(), 'in', chunk)));
          snapshot.docs.forEach(progressDoc => { allProgress[progressDoc.id] = progressDoc.data(); });
        }

        if (cancelled) return;
        setStudentData(students.map(user => {
          const progress = allProgress[user.uid] || {};
          const subjectProfile = (progress as unknown as { subjectProfile?: StudentSubjectProfile }).subjectProfile ?? null;
          return { user, progress, subjectProfile };
        }));
      } catch (error) {
        console.error('Error fetching admin data:', error);
        if (!cancelled) setLoadError('Student records could not be loaded. Try refreshing this view.');
      } finally {
        if (!cancelled) setIsLoading(false);
      }
    };

    void fetchData();
    return () => { cancelled = true; };
  }, [reloadToken]);

  const enrichedData = useMemo<EnrichedStudentRecord[]>(() => studentData.map(record => {
    const resolvedYearGroup = record.user.yearGroup ?? record.subjectProfile?.yearGroup;
    const curriculumLevel = record.user.curriculumLevel
      ?? record.subjectProfile?.curriculumLevel
      ?? (resolvedYearGroup ? yearGroupToCurriculumLevel(resolvedYearGroup) : undefined);
    const visibleCourses = filterCoursesForStudent(allCourses, curriculumLevel, record.subjectProfile);
    return {
      ...record,
      resolvedYearGroup,
      visibleCourses,
      metrics: calculateStudentMetrics(record.progress, visibleCourses),
    };
  }), [allCourses, studentData]);

  const schoolOptions = useMemo(() => {
    const values = new Set<string>(SCHOOLS.map(school => school.id));
    enrichedData.forEach(record => values.add(record.user.school || NOT_SET));
    return [...values].sort((a, b) => displaySchool(a).localeCompare(displaySchool(b)));
  }, [enrichedData]);

  const yearOptions = useMemo(() => {
    const values = new Set<string>(YEAR_GROUPS);
    enrichedData.forEach(record => values.add(record.resolvedYearGroup || NOT_SET));
    return [...values].sort((a, b) => {
      const order = [...YEAR_GROUPS, NOT_SET] as string[];
      return order.indexOf(a) - order.indexOf(b);
    });
  }, [enrichedData]);

  const filteredData = useMemo(() => enrichedData.filter(record => {
    const schoolMatches = schoolFilter === 'all' || (record.user.school || NOT_SET) === schoolFilter;
    const recordYear = record.resolvedYearGroup || NOT_SET;
    const yearMatches = yearFilter === 'all' || recordYear === yearFilter;
    return schoolMatches && yearMatches;
  }), [enrichedData, schoolFilter, yearFilter]);

  const selectedStats = useMemo(() => summariseCohort(filteredData), [filteredData]);

  const schoolRows = useMemo(() => {
    const recordsInYear = enrichedData.filter(record => yearFilter === 'all' || (record.resolvedYearGroup || NOT_SET) === yearFilter);
    return schoolOptions
      .filter(school => schoolFilter === 'all' || school === schoolFilter)
      .map(school => ({
        key: school,
        label: displaySchool(school),
        stats: summariseCohort(recordsInYear.filter(record => (record.user.school || NOT_SET) === school)),
      }))
      .filter(row => row.stats.students > 0);
  }, [enrichedData, schoolFilter, schoolOptions, yearFilter]);

  const yearRows = useMemo(() => {
    const recordsInSchool = enrichedData.filter(record => schoolFilter === 'all' || (record.user.school || NOT_SET) === schoolFilter);
    return yearOptions
      .filter(year => yearFilter === 'all' || year === yearFilter)
      .map(year => ({
        key: year,
        label: displayYear(year),
        stats: summariseCohort(recordsInSchool.filter(record => (record.resolvedYearGroup || NOT_SET) === year)),
      }))
      .filter(row => row.stats.students > 0);
  }, [enrichedData, schoolFilter, yearFilter, yearOptions]);

  const openSchoolStudents = (school: string) => {
    setSchoolFilter(school);
    setActiveView('students');
  };

  const openYearStudents = (year: string) => {
    setYearFilter(year);
    setActiveView('students');
  };

  const showFilters = activeView === 'overview' || activeView === 'programme' || activeView === 'students' || activeView === 'schools' || activeView === 'years';
  const notStarted = selectedStats.students - selectedStats.started;

  const renderStudentContent = () => {
    if (isLoading) {
      return (
        <div className="grid grid-cols-1 gap-5 md:grid-cols-2 xl:grid-cols-3" aria-label="Loading student records">
          {[0, 1, 2].map(item => <div key={item} className="h-[360px] animate-pulse rounded-xl border-2 border-[#1A1A1A] bg-white" />)}
        </div>
      );
    }
    if (loadError) {
      return (
        <div role="alert" className="rounded-r-[10px] border-l-[3px] border-[#F26B1F] bg-[#FDEEDF] px-5 py-4 text-sm italic text-[#8C3A0E]">
          <p className="font-bold not-italic">Student records are unavailable</p>
          <p className="mt-1">{loadError}</p>
          <button type="button" onClick={() => setReloadToken(value => value + 1)} className="mt-3 rounded-full border-2 border-[#1A1A1A] bg-white px-4 py-2 text-xs font-bold not-italic text-[#1A1A1A]">Try again</button>
        </div>
      );
    }
    if (filteredData.length === 0) {
      return (
        <div className="rounded-xl border-2 border-[#1A1A1A] bg-white px-5 py-12 text-center">
          <h2 className="font-serif text-2xl font-semibold text-[#1A1A1A]">No matching students</h2>
          <p className="mt-2 text-sm text-[#7A7068]">Change the school or year-group filter to widen this view.</p>
        </div>
      );
    }
    return (
      <div className="grid grid-cols-1 gap-5 md:grid-cols-2 xl:grid-cols-3">
        {filteredData.map(record => (
          <StudentProgressCard key={record.user.uid} record={record} onDelete={setDeleteTarget} />
        ))}
      </div>
    );
  };

  return (
    <div className="theme-compat min-h-screen w-full bg-[#f0f0f0] font-sans text-[#3A3530]">
      <header className="sticky top-0 z-40 border-b-2 border-[#1A1A1A] bg-white">
        <div className="mx-auto flex max-w-[1440px] flex-wrap items-center gap-x-8 px-4 sm:px-6 lg:px-8">
          <div className="flex h-16 items-center justify-between gap-5 max-lg:w-full">
            <div className="flex items-baseline gap-3">
              <span className="font-serif text-xl font-bold text-[#1A1A1A]">NextStepUni</span>
              <span className="text-xs font-bold uppercase tracking-[0.14em] text-[#9E9186]">Command desk</span>
            </div>
            <button type="button" onClick={onLogout} className="flex items-center gap-2 rounded-full border-2 border-[#1A1A1A] bg-white px-3 py-2 text-xs font-bold text-[#1A1A1A] hover:border-[#F26B1F] hover:text-[#B54D14] lg:hidden">
              <LogOut size={14} /> Log out
            </button>
          </div>

          <nav className="-mx-4 flex min-w-0 flex-1 overflow-x-auto px-4 lg:mx-0 lg:px-0" aria-label="Admin dashboard">
            <div className="flex min-w-max items-stretch">
              {NAV_ITEMS.map(item => (
                <button
                  key={item.id}
                  type="button"
                  onClick={() => setActiveView(item.id)}
                  aria-current={activeView === item.id ? 'page' : undefined}
                  className={`relative flex h-14 items-center px-3 text-sm font-bold transition-colors lg:h-16 ${activeView === item.id ? 'text-[#1A1A1A]' : 'text-[#7A7068] hover:text-[#1A1A1A]'}`}
                >
                  {item.label}
                  {activeView === item.id && <span className="absolute inset-x-3 bottom-0 h-[3px] bg-[#F26B1F]" />}
                </button>
              ))}
            </div>
          </nav>

          <button type="button" onClick={onLogout} className="hidden items-center gap-2 rounded-full border-2 border-[#1A1A1A] bg-white px-4 py-2 text-xs font-bold text-[#1A1A1A] hover:border-[#F26B1F] hover:text-[#B54D14] lg:flex">
            <LogOut size={14} /> Log out
          </button>
        </div>
      </header>

      <main className="mx-auto max-w-[1440px] px-4 py-6 sm:px-6 sm:py-8 lg:px-8">
        {(activeView === 'overview' || activeView === 'programme' || activeView === 'students' || activeView === 'schools' || activeView === 'years') && (
          <div className="mb-6 flex flex-col justify-between gap-5 border-b-2 border-[#1A1A1A] pb-6 lg:flex-row lg:items-end">
            <div>
              <p className="text-xs font-bold uppercase tracking-[0.14em] text-[#F26B1F]">{formatDate()}</p>
              <h1 className="mt-2 font-serif text-3xl font-semibold leading-tight text-[#1A1A1A] sm:text-4xl">
                {activeView === 'overview' ? 'What needs attention today' : activeView === 'programme' ? 'Programme evidence' : NAV_ITEMS.find(item => item.id === activeView)?.label}
              </h1>
              <p className="mt-2 max-w-2xl text-sm leading-relaxed text-[#7A7068]">
                {activeView === 'overview' && 'A live operational view built from the student and progress records already available.'}
                {activeView === 'programme' && 'Reach, participation, retention and feature evidence — with every percentage tied to its denominator.'}
                {activeView === 'students' && `${filteredData.length} student record${filteredData.length === 1 ? '' : 's'} in the current view.`}
                {activeView === 'schools' && 'Compare participation and learning progress across participating schools.'}
                {activeView === 'years' && 'Compare participation and learning progress across year groups.'}
              </p>
            </div>
            {showFilters && (
              <FilterControls
                schoolFilter={schoolFilter}
                yearFilter={yearFilter}
                schoolOptions={schoolOptions}
                yearOptions={yearOptions}
                onSchoolChange={setSchoolFilter}
                onYearChange={setYearFilter}
              />
            )}
          </div>
        )}

        {activeView === 'overview' && (
          <div className="space-y-6">
            <div className="grid grid-cols-2 gap-3 lg:grid-cols-4 lg:gap-5">
              <MetricCard label="Student accounts" value={isLoading || loadError ? '—' : selectedStats.students} detail={loadError ? 'Student data unavailable' : 'In the selected cohort'} icon={<Users size={19} />} />
              <MetricCard label="Started learning" value={isLoading || loadError ? '—' : `${selectedStats.startRate}%`} detail={loadError ? 'Student data unavailable' : isLoading ? 'Loading existing records' : `${selectedStats.started} students opened at least one course`} icon={<UserRoundCheck size={19} />} positive={selectedStats.startRate === 100 && selectedStats.students > 0} />
              <MetricCard label="Average progress" value={isLoading || loadError ? '—' : `${selectedStats.averageProgress.toFixed(0)}%`} detail={loadError ? 'Student data unavailable' : 'Across courses available to each student'} icon={<GraduationCap size={19} />} />
              <MetricCard label="Completed a course" value={isLoading || loadError ? '—' : selectedStats.completedOne} detail={loadError ? 'Student data unavailable' : 'Students with at least one completion'} icon={<BookOpenCheck size={19} />} positive={selectedStats.completedOne > 0} />
            </div>

            {!isLoading && !loadError && selectedStats.students > 0 && (
              <section className="flex flex-col justify-between gap-4 rounded-xl border-2 border-[#1A1A1A] bg-white px-5 py-4 sm:flex-row sm:items-center">
                <div className="flex items-start gap-3">
                  <span className={`mt-0.5 flex h-8 w-8 shrink-0 items-center justify-center rounded-full ${notStarted > 0 ? 'bg-[#FDEEDF] text-[#B54D14]' : 'bg-[#E8F2EC] text-[#1F5F3E]'}`}>
                    {notStarted > 0 ? <AlertTriangle size={17} /> : <UserRoundCheck size={17} />}
                  </span>
                  <div>
                    <h2 className="font-bold text-[#1A1A1A]">{notStarted > 0 ? `${notStarted} student${notStarted === 1 ? '' : 's'} have not started a learning module.` : 'Every student in this view has started learning.'}</h2>
                    <p className="mt-1 text-sm text-[#7A7068]">Open the student view to see the individual records behind this number.</p>
                  </div>
                </div>
                <button type="button" onClick={() => setActiveView('students')} className="inline-flex shrink-0 items-center justify-center gap-1 rounded-full border-2 border-[#1A1A1A] bg-white px-4 py-2 text-xs font-bold text-[#1A1A1A] hover:border-[#F26B1F] hover:text-[#B54D14]">
                  View students <ChevronRight size={14} />
                </button>
              </section>
            )}

            {isLoading ? (
              <div className="grid grid-cols-1 gap-5 lg:grid-cols-2">
                <div className="h-[340px] animate-pulse rounded-xl border-2 border-[#1A1A1A] bg-white" />
                <div className="h-[340px] animate-pulse rounded-xl border-2 border-[#1A1A1A] bg-white" />
              </div>
            ) : loadError ? (
              <div role="alert" className="rounded-r-[10px] border-l-[3px] border-[#F26B1F] bg-[#FDEEDF] px-5 py-4 text-sm italic text-[#8C3A0E]">{loadError}</div>
            ) : (
              <div className="grid grid-cols-1 gap-6 lg:grid-cols-[0.8fr_1.2fr]">
                <ProgressDistribution records={filteredData} />
                <CohortTable eyebrow="Portfolio" title="Schools at a glance" rows={schoolRows} emptyLabel="No schools match the current filters." onOpen={openSchoolStudents} />
              </div>
            )}

            {!isLoading && !loadError && (
              <CohortTable eyebrow="Cohorts" title="Year groups at a glance" rows={yearRows} emptyLabel="No year groups match the current filters." onOpen={openYearStudents} />
            )}
          </div>
        )}

        {activeView === 'programme' && (
          <AdminProgrammePanel
            schoolFilter={schoolFilter}
            yearFilter={yearFilter}
            allCourses={allCourses}
          />
        )}

        {activeView === 'students' && renderStudentContent()}

        {activeView === 'schools' && (
          isLoading ? <div className="h-[360px] animate-pulse rounded-xl border-2 border-[#1A1A1A] bg-white" /> : loadError ?
            <div role="alert" className="rounded-r-[10px] border-l-[3px] border-[#F26B1F] bg-[#FDEEDF] px-5 py-4 text-sm italic text-[#8C3A0E]">{loadError}</div> :
            <CohortTable eyebrow="School portfolio" title="All participating schools" rows={schoolRows} emptyLabel="No schools match the current filters." onOpen={openSchoolStudents} />
        )}

        {activeView === 'years' && (
          isLoading ? <div className="h-[360px] animate-pulse rounded-xl border-2 border-[#1A1A1A] bg-white" /> : loadError ?
            <div role="alert" className="rounded-r-[10px] border-l-[3px] border-[#F26B1F] bg-[#FDEEDF] px-5 py-4 text-sm italic text-[#8C3A0E]">{loadError}</div> :
            <CohortTable eyebrow="Year-group portfolio" title="All year groups" rows={yearRows} emptyLabel="No year groups match the current filters." onOpen={openYearStudents} />
        )}

        {activeView === 'funnel' && <section className="rounded-xl border-2 border-[#1A1A1A] bg-white p-5 sm:p-7"><AdminFunnelPanel /></section>}
        {activeView === 'feedback' && <section className="rounded-xl border-2 border-[#1A1A1A] bg-white p-5 sm:p-7"><AdminFeedbackInbox /></section>}
        {activeView === 'gc-access' && <section className="rounded-xl border-2 border-[#1A1A1A] bg-white p-5 sm:p-7"><AdminGcAccessPanel /></section>}

        {(activeView === 'overview' || activeView === 'students') && (
          <div className="mt-5 flex justify-end">
            <button type="button" onClick={() => setReloadToken(value => value + 1)} disabled={isLoading} className="inline-flex items-center gap-2 rounded-full border-2 border-[#1A1A1A] bg-white px-4 py-2 text-xs font-bold text-[#1A1A1A] disabled:opacity-50">
              <RefreshCw size={14} className={isLoading ? 'animate-spin' : undefined} /> Refresh student data
            </button>
          </div>
        )}
      </main>

      {deleteTarget && (
        <div className="fixed inset-0 z-[200] flex items-center justify-center bg-black/50 p-4" onClick={() => !isDeleting && closeDeleteDialog()}>
          <div
            ref={deleteDialogRef}
            role="dialog"
            aria-modal="true"
            aria-labelledby="delete-student-title"
            aria-describedby="delete-student-description"
            tabIndex={-1}
            className="w-full max-w-sm rounded-xl border-2 border-[#1A1A1A] bg-white p-6"
            onClick={event => event.stopPropagation()}
          >
            <div className="mb-4 flex items-center gap-3">
              <div className="flex h-10 w-10 items-center justify-center rounded-full bg-[#FDE8E7] text-[#B42318]"><AlertTriangle size={20} /></div>
              <h2 id="delete-student-title" className="font-serif text-xl font-semibold text-[#1A1A1A]">Delete student account</h2>
            </div>
            <p id="delete-student-description" className="text-sm leading-relaxed text-[#3A3530]">Delete <strong>{deleteTarget.name}</strong> and all associated progress and profile data?</p>
            <p className="mt-2 text-xs leading-relaxed text-[#7A7068]">This action cannot be undone.</p>
            {reauthMethodFor(auth.currentUser) === 'password' && (
              <label className="mt-5 block" htmlFor="admin-delete-password">
                <span className="mb-2 block text-xs font-bold uppercase tracking-[0.12em] text-[#7A7068]">Re-enter your password</span>
                <input id="admin-delete-password" type="password" value={deleteVerificationPassword} onChange={event => setDeleteVerificationPassword(event.target.value)} autoComplete="current-password" className="w-full rounded-lg border-2 border-[#1A1A1A] bg-white px-4 py-3 text-sm text-[#1A1A1A] outline-none focus:border-[#B42318]" />
              </label>
            )}
            <div className="mt-6 flex gap-3">
              <button ref={cancelDeleteButtonRef} type="button" onClick={closeDeleteDialog} disabled={isDeleting} className="flex-1 rounded-full border-2 border-[#1A1A1A] bg-white px-4 py-2.5 text-sm font-bold text-[#1A1A1A] disabled:opacity-50">Cancel</button>
              <button type="button" onClick={() => void handleDeleteStudent(deleteTarget)} disabled={isDeleting || (reauthMethodFor(auth.currentUser) === 'password' && !deleteVerificationPassword)} className="flex-1 rounded-full border-2 border-[#8F1D14] bg-[#B42318] px-4 py-2.5 text-sm font-bold text-white disabled:opacity-50">
                {isDeleting ? 'Deleting...' : 'Delete account'}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
