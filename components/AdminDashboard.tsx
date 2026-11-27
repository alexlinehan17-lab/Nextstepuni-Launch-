/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import './admin/admin-dashboard.css';
import React, { useEffect, useMemo, useRef, useState } from 'react';
import {
  ChartNoAxesColumn,
  ChevronLeft,
  ChevronRight,
  House,
  Inbox,
  Landmark,
  Lock,
  LogOut,
  RefreshCw,
  Trash2,
  User,
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
import { type CourseData } from './Library';
import { type CategoryType } from './KnowledgeTree';
import { type SessionUser } from '../utils/authUtils';
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
import { TopBar, TabBar, type TabBarItem } from './ui/Bars';
import { Button, IconButton, TextButton } from './ui/Button';
import { Confirm } from './ui/Sheet';
import { Field, SearchField } from './ui/Field';
import { Row } from './ui/List';
import { Menu, MenuAction, MenuPanel, MenuRule } from './ui/Menu';
import { SelectionBar } from './ui/Choice';
import { ErrorState, LoadingShape } from './ui/States';
import { MessageHost, showMessage } from './ui/Message';
import { Fig, Pct, StudentArt, useWide } from './gc/gcView';

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

/** The five places along the bottom of a phone (the agreed board: eight tabs became five; Year groups
 *  lives in Schools, First run opens from Overview, School access from the account menu). */
type Place = 'overview' | 'students' | 'schools' | 'programme' | 'feedback';
const PLACES: TabBarItem<Place>[] = [
  { id: 'overview', label: 'Overview', icon: House },
  { id: 'students', label: 'Students', icon: Users },
  { id: 'schools', label: 'Schools', icon: Landmark },
  { id: 'programme', label: 'Programme', icon: ChartNoAxesColumn },
  { id: 'feedback', label: 'Feedback', icon: Inbox },
];
/** On a laptop the staff sidebar lists the same five and School access (the agreed laptop board). */
const SIDEBAR: { id: AdminView; label: string; icon: typeof House }[] = [
  ...PLACES.map(place => ({ id: place.id as AdminView, label: place.label, icon: place.icon })),
  { id: 'gc-access', label: 'School access', icon: Lock },
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

/** "Tue 24 Nov": the day in the bar, as the agreed boards write it (never a machine date). */
function formatShortDate(): string {
  const today = new Date();
  const part = (options: Intl.DateTimeFormatOptions) => new Intl.DateTimeFormat('en-IE', options).format(today);
  return `${part({ weekday: 'short' })} ${part({ day: 'numeric' })} ${part({ month: 'short' })}`;
}

/** One course area's share for one student (today's sum, unchanged). */
function categoryProgressFor(record: EnrichedStudentRecord, category: CategoryType): number {
  const categoryCourses = record.visibleCourses.filter(course => course.category === category);
  if (categoryCourses.length === 0) return 0;
  const totalProgress = categoryCourses.reduce((sum, course) => {
    const courseProgress = record.progress[course.id];
    if (!courseProgress || typeof courseProgress.unlockedSection !== 'number' || course.sectionsCount <= 0) return sum;
    return sum + Math.min(100, (courseProgress.unlockedSection / course.sectionsCount) * 100);
  }, 0);
  return totalProgress / categoryCourses.length;
}

// ─── Dark by default ────────────────────────────────────────────────────────

const SETTINGS_KEY = 'nextstep-settings';

/**
 * The Light / Dark choice saved for this account, if there is one. The app keeps each account's
 * settings in this browser under `nextstep-settings:<uid>` (hooks/useSettings.ts): a `darkMode`
 * there is a choice that account has saved. Undefined: no choice saved.
 */
export function adminSavedTheme(uid?: string | null): boolean | undefined {
  if (!uid || typeof localStorage === 'undefined') return undefined;
  try {
    const raw = localStorage.getItem(`${SETTINGS_KEY}:${uid}`);
    if (!raw) return undefined;
    const saved = JSON.parse(raw) as { darkMode?: unknown };
    return typeof saved.darkMode === 'boolean' ? saved.darkMode : undefined;
  } catch {
    return undefined;
  }
}

/**
 * The Admin dashboard opens in dark (Alex, 24 Nov 2026: "have it auto set to dark mode though"), on the
 * app's own four dark surfaces: its separate palette is gone. How the default is decided: with no
 * choice saved for the signed-in account, the dashboard holds the app's `dark` setting on while it is
 * open and gives the page back as it found it when it closes, so the sign-in page and a student who
 * signs in next keep their own theme. A saved choice (light or dark) is kept: the app's setting
 * applies, as on every other screen. Nothing is written.
 */
export function useAdminOpensDark(uid?: string | null) {
  useEffect(() => {
    if (adminSavedTheme(uid) !== undefined || typeof document === 'undefined') return undefined;
    const root = document.documentElement;
    const had = root.classList.contains('dark');
    root.classList.add('dark');
    // The app's own settings effect may set the class from its default after this runs: keep it on.
    const keep = typeof MutationObserver === 'undefined' ? null : new MutationObserver(() => {
      if (!root.classList.contains('dark')) root.classList.add('dark');
    });
    keep?.observe(root, { attributes: true, attributeFilter: ['class'] });
    return () => {
      keep?.disconnect();
      if (!had) root.classList.remove('dark');
    };
  }, [uid]);
}

// ─── Pieces ─────────────────────────────────────────────────────────────────

/** A percent whose digits end on the column's edge, the % hanging past it. */
const PctCell: React.FC<{ value: number }> = ({ value }) => (
  <span className="adm-pct">{Math.round(value)}<small className="gc8-unit">%</small></span>
);

/** The four figures of the bigger picture: two by two, ruled, each over its small label. */
const Figures: React.FC<{ items: { label: string; value: React.ReactNode; detail: string }[] }> = ({ items }) => (
  <div className="adm-stats">
    {items.map(item => (
      <div key={item.label}>
        <span className="gc8-label">{item.label}</span>
        <span className="gc8-num adm-statnum">{item.value}</span>
        <span className="gc8-meta">{item.detail}</span>
      </div>
    ))}
  </div>
);

const ProgressDistribution: React.FC<{ records: EnrichedStudentRecord[] }> = ({ records }) => {
  const groups = [
    { label: 'Not started', count: records.filter(record => record.metrics.startedCourses === 0).length },
    { label: 'Getting started', count: records.filter(record => record.metrics.startedCourses > 0 && record.metrics.overallProgress < 25).length },
    { label: 'Building progress', count: records.filter(record => record.metrics.overallProgress >= 25 && record.metrics.overallProgress < 75).length },
    { label: 'Advanced', count: records.filter(record => record.metrics.overallProgress >= 75).length },
  ];

  return (
    <section className="gc8-sec adm-where" aria-labelledby="progress-distribution-title">
      <div className="gc8-sechead">
        <div className="gc8-sechead-col">
          <p className="gc8-label">Learning progress</p>
          <h2 id="progress-distribution-title" className="gc8-h">Where students are</h2>
        </div>
      </div>
      <div className="adm-stack" aria-hidden="true">
        {groups.map((group, index) => <i key={group.label} className={`adm-s${index}`} style={{ flex: group.count }} />)}
      </div>
      <div className="adm-dist">
        {groups.map((group, index) => {
          const percentage = records.length > 0 ? Math.round((group.count / records.length) * 100) : 0;
          return (
            <div key={group.label}>
              <div className="adm-dhead">
                <span>{group.label}</span>
                <span className="adm-dn"><span>{group.count}</span><span className="adm-dp">{percentage}<small className="gc8-unit">%</small></span></span>
              </div>
              <span className={`gc8-bar gc8-bar--thin adm-dbar adm-s${index}`} aria-hidden="true"><i style={{ width: `${percentage}%` }} /></span>
            </div>
          );
        })}
      </div>
    </section>
  );
};

type CohortRow = { key: string; label: string; stats: CohortStats };

/** A cohort (a school or a year group) as a row: two facts and one number; the row opens its students. */
const CohortRows: React.FC<{ rows: CohortRow[]; emptyLabel: string; onOpen: (key: string) => void }> = ({ rows, emptyLabel, onOpen }) => (
  rows.length > 0 ? (
    <ul className="ui-list gc8-list adm-rows">
      {rows.map(row => (
        <Row
          key={row.key}
          title={<span className="adm-one" title={row.label}>{row.label}</span>}
          label={`Open students in ${row.label}`}
          meta={`${row.stats.students} student${row.stats.students === 1 ? '' : 's'} · ${row.stats.startRate}% started`}
          trailing={<><Pct value={row.stats.averageProgress} className="ui-row-value" /><ChevronRight className="ui-icon ui-row-chev" width={20} height={20} strokeWidth={1.75} aria-hidden="true" /></>}
          onPress={() => onOpen(row.key)}
        />
      ))}
    </ul>
  ) : <p className="gc8-empty">{emptyLabel}</p>
);

/** The full comparison on a laptop: every column, the figures on their right edge, the % hanging. */
const CohortTable: React.FC<{ rows: CohortRow[]; emptyLabel: string; onOpen: (key: string) => void }> = ({ rows, emptyLabel, onOpen }) => (
  <div className="adm-tbl" role="table">
    <div className="adm-tr adm-tr--head" role="row">
      <span className="gc8-label" role="columnheader">Cohort</span>
      <span className="gc8-label adm-n" role="columnheader">Students</span>
      <span className="gc8-label adm-n" role="columnheader">Started</span>
      <span className="gc8-label" role="columnheader">Average progress</span>
      <span className="gc8-label adm-n" role="columnheader">Completed a course</span>
      <span role="columnheader"><span className="sr-only">Open students</span></span>
    </div>
    {rows.length > 0 ? rows.map(row => (
      <div key={row.key} className="adm-tr" role="row">
        <b role="cell" title={row.label}>{row.label}</b>
        <span role="cell" className="adm-n">{row.stats.students}</span>
        <span role="cell" className="adm-split"><span>{row.stats.started}</span><PctCell value={row.stats.startRate} /></span>
        <span role="cell" className="adm-prog"><PctCell value={row.stats.averageProgress} /><span className="gc8-bar gc8-bar--thin" aria-hidden="true"><i style={{ width: `${row.stats.averageProgress}%` }} /></span></span>
        <span role="cell" className="adm-n">{row.stats.completedOne}</span>
        <span role="cell" className="adm-open">
          <Button size="sm" arrow="opens" className="adm-openbtn" onClick={() => onOpen(row.key)} aria-label={`Open students in ${row.label}`}>Students</Button>
        </span>
      </div>
    )) : <p className="gc8-empty">{emptyLabel}</p>}
  </div>
);

/** Three figures in a line, each centred over its small label (My Progress's agreed figures). */
const StudentFigures: React.FC<{ metrics: StudentMetrics }> = ({ metrics }) => (
  <div className="adm-fa">
    <div><span className="gc8-meta">Overall</span><span className="gc8-num"><Fig value={metrics.overallProgress.toFixed(0)} unit="%" /></span></div>
    <div><span className="gc8-meta">Started</span><span className="gc8-num">{metrics.startedCourses}</span></div>
    <div><span className="gc8-meta">Complete</span><span className="gc8-num">{metrics.completedCourses}</span></div>
  </div>
);

/** The five course areas, each with its figure and an ink bar (green once complete, as today). */
const CourseAreas: React.FC<{ record: EnrichedStudentRecord; small?: boolean }> = ({ record, small = false }) => (
  <div className={`adm-areas${small ? ' adm-areas--sm' : ''}`}>
    {CATEGORIES.map(category => {
      const share = categoryProgressFor(record, category.id);
      return (
        <div key={category.id} className="adm-area">
          <div className="adm-ahead"><span title={category.title}>{category.title}</span><PctCell value={share} /></div>
          <span className={`gc8-bar adm-abar${share >= 100 ? ' adm-abar--done' : ''}`} aria-hidden="true"><i style={{ width: `${share}%` }} /></span>
        </div>
      );
    })}
  </div>
);

/** One student on a laptop: today's card laid on the page (three across), the bin at the top right. */
const StudentProgressCard: React.FC<{
  record: EnrichedStudentRecord;
  onDelete: (user: SessionUser) => void;
}> = ({ record, onDelete }) => {
  const { user, resolvedYearGroup, metrics } = record;
  return (
    <article className="adm-stu">
      <div className="adm-shead">
        <StudentArt seed={user.avatar || user.name} />
        <span className="adm-shead-copy">
          <h3 className="gc8-person adm-one" title={user.name}>{user.name}</h3>
          <span className="gc8-meta adm-one">{displaySchool(user.school)} · {displayYear(resolvedYearGroup)}</span>
        </span>
        <IconButton className="adm-bin" label={`Delete ${user.name}`} onClick={() => onDelete(user)}
          icon={<Trash2 className="ui-icon" width={20} height={20} strokeWidth={1.75} aria-hidden="true" />} />
      </div>
      <StudentFigures metrics={metrics} />
      <CourseAreas record={record} small />
    </article>
  );
};

/** "Best on a laptop": the board's plain line. Its "Email me a link" button is not built (there is no
 *  such feature: it would send something), so the line stands alone (FOR-ALEX, area 8b). */
const BestOnLaptop: React.FC<{ children: React.ReactNode }> = ({ children }) => (
  <div className="gc8-best adm-best">
    <p className="gc8-label">Best on a laptop</p>
    <p className="gc8-sub">{children}</p>
  </div>
);

// ─── The dashboard ──────────────────────────────────────────────────────────

export const AdminDashboard: React.FC<AdminDashboardProps> = ({ allCourses, onLogout }) => {
  const [studentData, setStudentData] = useState<StudentRecord[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [loadError, setLoadError] = useState('');
  const [reloadToken, setReloadToken] = useState(0);
  const [lastLoadedAt, setLastLoadedAt] = useState<Date | null>(null);
  const [deleteTarget, setDeleteTarget] = useState<SessionUser | null>(null);
  const [isDeleting, setIsDeleting] = useState(false);
  const [deleteVerificationPassword, setDeleteVerificationPassword] = useState('');
  const [activeView, setActiveView] = useState<AdminView>('overview');
  // School access is a page you go back from (the account menu opens it on a phone).
  const [returnView, setReturnView] = useState<AdminView>('overview');
  // One student, opened from Students on a phone.
  const [openStudentUid, setOpenStudentUid] = useState<string | null>(null);
  const [studentSearch, setStudentSearch] = useState('');
  const [schoolFilter, setSchoolFilter] = useState('all');
  const [yearFilter, setYearFilter] = useState('all');
  const [accountOpen, setAccountOpen] = useState(false);
  const deleteFieldRef = useRef<HTMLInputElement>(null);
  const wide = useWide();
  const tables = useWide(1200);
  // The feature table's five columns and four figures across need about a laptop's width.
  const roomy = useWide(1000);
  useAdminOpensDark(auth.currentUser?.uid);

  // The phone's bar gains its hairline once the page has scrolled under it (tokens.md, "Bars").
  const [scrolled, setScrolled] = useState(false);
  useEffect(() => {
    if (wide) return undefined;
    const update = () => setScrolled(window.scrollY > 4);
    update();
    window.addEventListener('scroll', update, { passive: true });
    return () => window.removeEventListener('scroll', update);
  }, [wide]);

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
      if (openStudentUid === user.uid) setOpenStudentUid(null);
    } catch (error) {
      console.error('Error deleting student:', error);
      // Today's words, in the app's message (it was a browser alert).
      showMessage('Failed to delete student. You may not have permission.');
    } finally {
      setIsDeleting(false);
      setDeleteVerificationPassword('');
      closeDeleteDialog();
    }
  };

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
        setLastLoadedAt(new Date());
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

  // The search box on Students narrows the list already loaded, by name: it makes no new read.
  const searchedData = useMemo(() => {
    const needle = studentSearch.trim().toLocaleLowerCase('en-IE');
    if (!needle) return filteredData;
    return filteredData.filter(record => (record.user.name || '').toLocaleLowerCase('en-IE').includes(needle));
  }, [filteredData, studentSearch]);

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

  const go = (view: AdminView) => {
    setAccountOpen(false);
    setOpenStudentUid(null);
    setActiveView(view);
    if (typeof window !== 'undefined' && typeof window.scrollTo === 'function') window.scrollTo(0, 0);
  };

  const openSchoolAccess = () => {
    setReturnView(activeView === 'gc-access' ? returnView : activeView);
    go('gc-access');
  };

  const openSchoolStudents = (school: string) => {
    setSchoolFilter(school);
    go('students');
  };

  const openYearStudents = (year: string) => {
    setYearFilter(year);
    go('students');
  };

  const refreshStudents = () => setReloadToken(value => value + 1);
  const notStarted = selectedStats.students - selectedStats.started;
  const dataAsOf = lastLoadedAt ? lastLoadedAt.toLocaleTimeString('en-IE', { hour: '2-digit', minute: '2-digit' }) : null;
  const filterWords = `${schoolFilter === 'all' ? 'All schools' : displaySchool(schoolFilter)} · ${yearFilter === 'all' ? 'All year groups' : displayYear(yearFilter)}`;
  const shortDate = formatShortDate();
  const placeLabel = `The programme desk · ${shortDate}`;
  const openStudent = !wide && openStudentUid ? enrichedData.find(record => record.user.uid === openStudentUid) ?? null : null;

  const currentPlace: Place = activeView === 'years' ? 'schools'
    : activeView === 'funnel' ? 'overview'
      : activeView === 'gc-access' ? (returnView === 'years' ? 'schools' : returnView === 'funnel' || returnView === 'gc-access' ? 'overview' : returnView as Place)
        : activeView as Place;
  const sideCurrent: AdminView = activeView === 'years' ? 'schools' : activeView === 'funnel' ? 'overview' : activeView;

  const filterMenus = (
    <>
      <Menu
        label="School"
        value={schoolFilter}
        onChange={setSchoolFilter}
        options={[{ value: 'all', label: 'All schools' }, ...schoolOptions.map(school => ({ value: school, label: displaySchool(school) }))]}
      />
      <Menu
        label="Year group"
        value={yearFilter}
        onChange={setYearFilter}
        options={[{ value: 'all', label: 'All year groups' }, ...yearOptions.map(year => ({ value: year, label: displayYear(year) }))]}
      />
    </>
  );
  const filters = <div className="adm-filters" aria-label="Dashboard filters">{filterMenus}</div>;

  const studentsUnavailable = loadError ? <ErrorState sentence={loadError} onRetry={refreshStudents} /> : null;

  // ── Overview ──
  const attention = (
    <ul className={`ui-list gc8-list adm-attn${wide ? ' adm-attn--wide' : ''}`} aria-label="What needs attention">
      <Row
        title={isLoading || loadError ? 'Students' : notStarted > 0 ? `${notStarted} student${notStarted === 1 ? ' is' : 's are'} yet to get started` : 'Every student in this view has started learning'}
        meta={isLoading || loadError ? undefined : `Students · across ${schoolRows.length} school${schoolRows.length === 1 ? '' : 's'}`}
        onPress={() => go('students')}
      />
      <Row title="Are students getting in?" meta="First run" onPress={() => go('funnel')} />
      <Row title="Feedback inbox" meta="Anonymous student voice" onPress={() => go('feedback')} />
    </ul>
  );

  const figures = (
    <Figures items={[
      { label: 'Student accounts', value: isLoading || loadError ? '—' : selectedStats.students, detail: loadError ? 'Student data unavailable' : 'In the selected cohort' },
      {
        label: 'Started learning',
        value: isLoading || loadError ? '—' : <Fig value={selectedStats.startRate} unit="%" />,
        detail: loadError ? 'Student data unavailable' : isLoading ? 'Loading existing records' : wide ? `${selectedStats.started} students opened at least one course` : `${selectedStats.started} of ${selectedStats.students} students`,
      },
      { label: 'Average progress', value: isLoading || loadError ? '—' : <Fig value={selectedStats.averageProgress.toFixed(0)} unit="%" />, detail: loadError ? 'Student data unavailable' : wide ? 'Across courses available to each student' : 'Across available courses' },
      { label: 'Completed a course', value: isLoading || loadError ? '—' : selectedStats.completedOne, detail: loadError ? 'Student data unavailable' : wide ? 'Students with at least one completion' : 'At least one completion' },
    ]} />
  );

  const cohorts = (rows: CohortRow[], emptyLabel: string, onOpen: (key: string) => void) => (
    tables ? <CohortTable rows={rows} emptyLabel={emptyLabel} onOpen={onOpen} /> : <CohortRows rows={rows} emptyLabel={emptyLabel} onOpen={onOpen} />
  );

  const overview = (
    <>
      {wide ? (
        <div className="gc8-hero adm-hero">
          <div className="gc8-head">
            <h1 className="gc8-title">What needs attention today</h1>
            <p className="gc8-sub">Participation, progress and the next conversation to have.</p>
          </div>
          {filters}
        </div>
      ) : (
        <header className="gc8-head adm-head">
          <h1 className="gc8-title">What needs attention today</h1>
          <p className="gc8-sub">Participation, progress and the next conversation to have.</p>
          {filters}
        </header>
      )}
      {attention}
      <div className="gc8-two adm-two">
        <section className="gc8-sec" aria-label="Cohort summary">
          <div className="gc8-sechead">
            <h2 className="gc8-h">The bigger picture</h2>
            <span className="gc8-meta">{!wide && dataAsOf ? `Data as of ${dataAsOf}` : filterWords}</span>
          </div>
          {figures}
        </section>
        {isLoading ? <LoadingShape rows={4} label="Loading existing records" /> : loadError ? null : <ProgressDistribution records={filteredData} />}
      </div>
      {isLoading ? <LoadingShape rows={5} label="Loading existing records" /> : loadError ? studentsUnavailable : (
        <>
          <section className="gc8-sec" aria-labelledby="adm-schools-glance">
            <div className="gc8-sechead">
              <div className="gc8-sechead-col"><p className="gc8-label">Your schools</p><h2 id="adm-schools-glance" className="gc8-h">Schools at a glance</h2></div>
              <span className="gc8-meta">Existing student records</span>
            </div>
            {cohorts(schoolRows, 'No schools match the current filters.', openSchoolStudents)}
          </section>
          <section className="gc8-sec" aria-labelledby="adm-years-glance">
            <div className="gc8-sechead">
              <div className="gc8-sechead-col"><p className="gc8-label">Cohorts</p><h2 id="adm-years-glance" className="gc8-h">Year groups at a glance</h2></div>
              <span className="gc8-meta">Existing student records</span>
            </div>
            {cohorts(yearRows, 'No year groups match the current filters.', openYearStudents)}
          </section>
        </>
      )}
    </>
  );

  // ── Schools, with Year groups behind the switch ──
  const yearSide = activeView === 'years';
  const cohortRows = yearSide ? yearRows : schoolRows;
  const schools = (
    <>
      <header className="gc8-head adm-head">
        <h1 className={wide ? 'gc8-title' : 'gc8-name'}>Schools</h1>
        <SelectionBar
          label="Compare"
          size="md"
          className="adm-switch"
          options={[{ value: 'schools', label: 'Schools' }, { value: 'years', label: 'Year groups' }]}
          value={yearSide ? 'years' : 'schools'}
          onChange={value => setActiveView(value)}
        />
        {filters}
      </header>
      {isLoading ? <LoadingShape rows={5} label="Loading existing records" /> : loadError ? studentsUnavailable : (
        <section className="gc8-sec" aria-label={yearSide ? 'Year groups' : 'Schools'}>
          {tables ? (
            <div className="gc8-sechead">
              <div className="gc8-sechead-col">
                <p className="gc8-label">{yearSide ? 'Year-group portfolio' : 'School portfolio'}</p>
                <h2 className="gc8-h">{yearSide ? 'All year groups' : 'All participating schools'}</h2>
              </div>
              <span className="gc8-meta">Existing student records</span>
            </div>
          ) : (
            <div className="adm-colhead">
              <span className="gc8-label">{cohortRows.length} {yearSide ? `year group${cohortRows.length === 1 ? '' : 's'}` : `school${cohortRows.length === 1 ? '' : 's'}`}</span>
              <span className="gc8-label">Avg progress</span>
            </div>
          )}
          {cohorts(cohortRows, yearSide ? 'No year groups match the current filters.' : 'No schools match the current filters.', yearSide ? openYearStudents : openSchoolStudents)}
          {!wide && <BestOnLaptop>Comparing every column side by side, and the feature table in Programme.</BestOnLaptop>}
        </section>
      )}
    </>
  );

  // ── Students ──
  const studentsHead = (
    <>
      <div className="gc8-head">
        <h1 className={wide ? 'gc8-title' : 'gc8-name'}>Students</h1>
        <p className="gc8-sub">{filteredData.length} student record{filteredData.length === 1 ? '' : 's'} in the current view.</p>
      </div>
      <SearchField
        label="Search students"
        placeholder="Search students"
        className="adm-find"
        value={studentSearch}
        onChange={event => setStudentSearch(event.target.value)}
        autoComplete="off"
      />
    </>
  );
  const noStudents = (
    <div className="gc8-empty adm-none">
      <b>No matching students</b>
      Change the school or year-group filter to widen this view.
    </div>
  );
  const students = (
    <>
      {wide ? (
        <div className="gc8-hero adm-hero">
          <div className="gc8-head">
            <h1 className="gc8-title">Students</h1>
            <p className="gc8-sub">{filteredData.length} student record{filteredData.length === 1 ? '' : 's'} in the current view.</p>
          </div>
          <div className="adm-filters" aria-label="Dashboard filters">
            <SearchField
              label="Search students"
              placeholder="Search students"
              className="adm-find"
              value={studentSearch}
              onChange={event => setStudentSearch(event.target.value)}
              autoComplete="off"
            />
            {filterMenus}
          </div>
        </div>
      ) : (
        <header className="gc8-head adm-head">
          {studentsHead}
          {filters}
        </header>
      )}
      {isLoading ? <LoadingShape rows={6} label="Loading student records" /> : loadError ? studentsUnavailable : searchedData.length === 0 ? noStudents : wide ? (
        <div className="adm-sgrid">
          {searchedData.map(record => (
            <StudentProgressCard key={record.user.uid} record={record} onDelete={setDeleteTarget} />
          ))}
        </div>
      ) : (
        <section className="gc8-sec" aria-label="Students">
          <div className="adm-colhead">
            <span className="gc8-label">{searchedData.length} student{searchedData.length === 1 ? '' : 's'}</span>
            <span className="gc8-label">Overall</span>
          </div>
          <ul className="ui-list gc8-list adm-rows">
            {searchedData.map(record => (
              <Row
                key={record.user.uid}
                art={<StudentArt seed={record.user.avatar || record.user.name} />}
                title={<span className="adm-one" title={record.user.name}>{record.user.name}</span>}
                label={`View ${record.user.name}`}
                meta={`${displayYear(record.resolvedYearGroup)} · ${displaySchool(record.user.school)}`}
                trailing={<><Pct value={record.metrics.overallProgress} className="ui-row-value" /><ChevronRight className="ui-icon ui-row-chev" width={20} height={20} strokeWidth={1.75} aria-hidden="true" /></>}
                onPress={() => { setOpenStudentUid(record.user.uid); window.scrollTo?.(0, 0); }}
              />
            ))}
          </ul>
        </section>
      )}
    </>
  );

  // ── One student, on a phone: today's card on its own page ──
  const studentPage = openStudent ? (
    <>
      <div className="adm-who">
        <StudentArt seed={openStudent.user.avatar || openStudent.user.name} size={56} />
        <div className="adm-who-copy">
          <p className="gc8-label">{displayYear(openStudent.resolvedYearGroup)} · {displaySchool(openStudent.user.school)}</p>
          <h1 className="gc8-name">{openStudent.user.name}</h1>
        </div>
      </div>
      <StudentFigures metrics={openStudent.metrics} />
      <CourseAreas record={openStudent} />
      <BestOnLaptop>Deleting this student&apos;s account, with your password to confirm it.</BestOnLaptop>
    </>
  ) : null;

  // ── What fills the page ──
  const leaveTo: { view: AdminView; label: string } | null = openStudent ? { view: 'students', label: 'Students' }
    : activeView === 'funnel' ? { view: 'overview', label: 'Overview' }
      : activeView === 'gc-access' && !wide ? { view: returnView, label: 'Back' }
        : null;
  const leave = () => {
    if (openStudent) { setOpenStudentUid(null); return; }
    if (leaveTo) go(leaveTo.view);
  };

  const page = openStudent ? studentPage
    : activeView === 'overview' ? overview
      : activeView === 'students' ? students
        : activeView === 'schools' || activeView === 'years' ? schools
          : activeView === 'programme' ? (
            <>
              {wide ? (
                <div className="gc8-hero adm-hero">
                  <div className="gc8-head">
                    <h1 className="gc8-title">Programme evidence</h1>
                    <p className="gc8-sub">Reach, participation, retention and feature evidence, with every percentage tied to its denominator.</p>
                  </div>
                  {filters}
                </div>
              ) : (
                <header className="gc8-head adm-head">
                  <h1 className="gc8-name">Programme evidence</h1>
                  <p className="gc8-sub">Reach, participation, retention and feature evidence, with every percentage tied to its denominator.</p>
                  {filters}
                </header>
              )}
              <AdminProgrammePanel schoolFilter={schoolFilter} yearFilter={yearFilter} allCourses={allCourses} wide={roomy} />
            </>
          )
            : activeView === 'funnel' ? <AdminFunnelPanel />
              : activeView === 'feedback' ? <AdminFeedbackInbox />
                : <AdminGcAccessPanel />;

  const accountFace = <User className="ui-icon" width={20} height={20} strokeWidth={1.75} aria-hidden="true" />;

  return (
    <div className="gc8 adm">
      {/* ─── Laptop: the staff sidebar (Log out in the menu under your name) ─── */}
      {wide && <aside className="gc8-side frame-page frame-foot" aria-label="Admin dashboard">
        <div className="gc8-brand">
          <p className="gc8-wordmark">nextstepuni<i aria-hidden="true">.</i></p>
        </div>
        <nav className="gc8-nav" aria-label="Admin dashboard">
          {SIDEBAR.map(item => (
            <button
              key={item.id}
              type="button"
              className="gc8-nav-item"
              aria-current={sideCurrent === item.id ? 'page' : undefined}
              onClick={() => go(item.id)}
            >
              <item.icon className="ui-icon" width={20} height={20} strokeWidth={1.75} aria-hidden="true" />
              {item.label}
            </button>
          ))}
        </nav>
        <MenuPanel
          label="Your account"
          buttonLabel="Your account: Admin"
          buttonClassName="gc8-user"
          className="gc8-usermenu"
          align="start"
          side="top"
          face={<>
            <span className="gc8-user-box">{accountFace}</span>
            <span className="gc8-user-copy"><span>Admin</span><span className="gc8-meta">The programme desk</span></span>
          </>}
        >
          <MenuAction title="Log out" plain tone="danger" onPress={onLogout} />
        </MenuPanel>
      </aside>}

      <div className="gc8-col">
        {/* ─── Laptop: the bar along the top ─── */}
        {wide && <div className="gc8-dbar">
          <p className="gc8-label">{placeLabel}</p>
          <div className="gc8-dbar-end">
            {dataAsOf && <span className="gc8-meta">Data as of {dataAsOf}</span>}
            <TextButton tone="quiet" className="gc8-ib" onClick={refreshStudents}>
              <RefreshCw className="ui-icon" width={16} height={16} strokeWidth={2} aria-hidden="true" />Refresh
            </TextButton>
          </div>
        </div>}

        {/* ─── Phone: a place's bar with your account, or a page's bar with Back ─── */}
        {!wide && (leaveTo ? (
          activeView === 'funnel' && !openStudent ? null : (
            <TopBar className="gc8-placebar adm-pagebar" ruled={scrolled} leave={{ kind: 'back', onPress: leave, label: openStudent ? 'Back to Students' : 'Back' }} />
          )
        ) : (
          <TopBar
            className="gc8-placebar"
            ruled={scrolled}
            placeLabel={placeLabel}
            action={
              <MenuPanel
                label="Your account"
                buttonLabel="Your account"
                buttonClassName="adm-me"
                className="adm-accountmenu"
                chevron={false}
                open={accountOpen}
                onOpenChange={setAccountOpen}
                face={<span className="adm-me-box">{accountFace}</span>}
                head={<span className="adm-menuhead"><span>Admin</span><span className="gc8-meta">The programme desk</span></span>}
              >
                <MenuAction title="School access" onPress={openSchoolAccess} />
                <MenuAction plain title={<span className="adm-mrow"><span>Refresh data</span>{dataAsOf ? <span className="gc8-meta">As of {dataAsOf}</span> : null}</span>} onPress={refreshStudents} />
                <MenuRule />
                <MenuAction plain title={<span className="adm-mrow"><span>Log out</span><LogOut className="ui-icon" width={20} height={20} strokeWidth={1.75} aria-hidden="true" /></span>} onPress={onLogout} />
              </MenuPanel>
            }
          />
        ))}

        {/* First run on a phone draws its own bar: Back, and its Refresh at the right. */}
        {!wide && activeView === 'funnel' && !openStudent ? (
          <AdminFunnelPanel onBack={() => go('overview')} />
        ) : (
          <main className="gc8-main adm-main">
            {wide && activeView === 'funnel' && (
              <div className="adm-backrow">
                <TextButton tone="quiet" className="adm-back" aria-label="Back to Overview" onClick={() => go('overview')}>
                  <ChevronLeft className="ui-icon" width={20} height={20} strokeWidth={1.75} aria-hidden="true" />Overview
                </TextButton>
              </div>
            )}
            {page}
          </main>
        )}

        {!wide && <TabBar className="gc8-tabbar" label="Admin dashboard" items={PLACES} current={currentPlace} onSelect={id => go(id)} />}
      </div>

      {/* Delete: the shared confirm, today's words and its typed check (the administrator's password). */}
      <Confirm
        open={!!deleteTarget}
        sentence="Delete student account"
        detail={<>Delete <b>{deleteTarget?.name}</b> and all associated progress and profile data? This action cannot be undone.</>}
        keepLabel="Cancel"
        onKeep={() => { if (!isDeleting) closeDeleteDialog(); }}
        dangerLabel={isDeleting ? 'Deleting...' : 'Delete account'}
        dangerBlocked={isDeleting || (reauthMethodFor(auth.currentUser) === 'password' && !deleteVerificationPassword)}
        onDanger={() => {
          if (isDeleting || !deleteTarget) return;
          if (reauthMethodFor(auth.currentUser) === 'password' && !deleteVerificationPassword) { deleteFieldRef.current?.focus(); return; }
          void handleDeleteStudent(deleteTarget);
        }}
      >
        {reauthMethodFor(auth.currentUser) === 'password' ? (
          <Field
            ref={deleteFieldRef}
            id="admin-delete-password"
            type="password"
            label="Re-enter your password"
            value={deleteVerificationPassword}
            onChange={event => setDeleteVerificationPassword(event.target.value)}
            autoComplete="current-password"
          />
        ) : null}
      </Confirm>

      {/* A failed delete says so here (it was a browser alert). */}
      <MessageHost />
    </div>
  );
};
