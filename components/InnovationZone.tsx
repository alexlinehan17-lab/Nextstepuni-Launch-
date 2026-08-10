
/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React, { useState, useEffect, useCallback, useRef, lazy, Suspense } from 'react';
import { useToast } from './Toast';
import { AnimatePresence } from 'framer-motion';
import { MotionButton, MotionDiv } from './Motion';
import { FileSearch,
    ArrowLeft,
    Lock, Compass, Target,
    CalendarDays, Calculator, GitBranch, Rocket,
    Map, ScanSearch, Milestone, Highlighter, Users, Sunrise, Mic, Stamp, Images, ListChecks, SpellCheck, FolderCheck, Waypoints
} from 'lucide-react';
import { doc, setDoc, getDoc, increment, deleteField } from 'firebase/firestore';
import { saveInBackground } from '../utils/firestoreWrite';
import { db } from '../firebase';
import { type StudentSubjectProfile, type TimetableCompletions, type TimetableStreak, type YearGroup } from './subjectData';
import { type SchoolEvent } from './gc/GCKeyEvents';
import { computeStreak } from './timetableAlgorithm';
import { type StudyReflection, type PointsData, type CosmeticUnlocks, type EarnedRest, type UserSettings } from '../types';
import SubjectOnboarding from './SubjectOnboarding';
import { LoadingSpinner } from './LoadingSpinner';
// Tool components are code-split: each loads its own chunk only when the
// student opens it (rendered inside <Suspense> below). This keeps the
// InnovationZone shell light and, crucially, defers the heavy Three.js
// bundle (pulled in only by AcademicJourneyGame) until the Journey is
// actually opened, instead of at zone boot. (audit M21)
const SpacedRepetitionTimetable = lazy(() => import('./SpacedRepetitionTimetable'));
const WarRoom = lazy(() => import('./WarRoom'));
const ComebackEngine = lazy(() => import('./ComebackEngineV2'));
const FutureFinder = lazy(() => import('./FutureFinder'));
const FutureFinderRevamped = lazy(() => import('./FutureFinderRevamped'));
const CollegeCompass = lazy(() => import('./CollegeCompass'));
const SyllabusXRay = lazy(() => import('./SyllabusXRay'));
const PointsPassport = lazy(() => import('./PointsPassport'));
const CatchUpLane = lazy(() => import('./CatchUpLane'));
const CommandWordReflex = lazy(() => import('./CommandWordReflex'));
const PaperTrail = lazy(() => import('./PaperTrail'));
const MarkBank = lazy(() => import('./MarkBank/MarkBank'));
const DiagramVault = lazy(() => import('./DiagramVault/DiagramVault'));
const AnswerArchitect = lazy(() => import('./AnswerArchitect/AnswerArchitect'));
const DefinitionDrill = lazy(() => import('./DefinitionDrill/DefinitionDrill'));
const CourseworkCompanion = lazy(() => import('./CourseworkCompanion/CourseworkCompanion'));
const HowTheyDidIt = lazy(() => import('./HowTheyDidIt'));
const YourPossibleLife = lazy(() => import('./YourPossibleLife'));
const OralExamTrainer = lazy(() => import('./OralExamTrainer'));
const ExaminersChair = lazy(() => import('./ExaminersChair'));
import { InnovationDataProvider } from '../contexts/InnovationDataContext';
import { getNotifications } from './gc/gcNotifications';
// ReflectionModal import removed — "Already Studied" flow gives 2 pts, no reflection
import StudyJournalModal from './StudyJournalModal';
import { type JourneyResult } from './AcademicJourneyGame';
const AcademicJourneyGame = lazy(() => import('./AcademicJourneyGame'));
import ToolErrorBoundary from './ToolErrorBoundary';
import PointsPanel from './PointsPanel';
import { useNavigation } from '../contexts/NavigationContext';
import { ToolHeader } from './ToolHeader';
import ToolIconBlob, { type ToolIconKey } from './ToolIconBlob';
import { isActiveSeniorYear, isLcaYear } from '../utils/authUtils';

// ── Editorial chrome registry ──────────────────────────────────────────
//
// All chrome (theme colour, eyebrow, subtitle, icon, whether to show the
// auto ToolHeader) lives in one place so the launchpad grid and the
// active-tool header use identical metadata.
//
// `showHeader: false` is reserved for genuinely task-dense workspaces where
// repeated chrome costs useful working space. Narrative and strategic tools
// keep the shared header so they remain recognisably part of Launchpad.

interface ToolChrome {
  themeColor: string;
  eyebrow: string;
  subtitle: string;
  showHeader: boolean;
}

/**
 * Tools that lay out their own work surface rather than living in the shared
 * reading column. `max-w-4xl` yields 848px of usable width, which is right for a
 * page of prose and wrong for a two-pane workspace.
 */
const WIDE_TOOLS = new Set(['mark-bank', 'your-possible-life', 'war-room']);

const TOOL_CHROME: Record<string, ToolChrome> = {
  'journey':         { themeColor: '#8B82B8', eyebrow: 'Track · Simulator',           subtitle: 'Navigate the choices of your final school year, then turn the outcome into a practical next step.', showHeader: true },
  // Compatibility alias for old links. It now opens Points Passport directly
  // on Grade Planner, so students see one points product rather than two.
  'cao-simulator':   { themeColor: '#B8A079', eyebrow: 'Track · Points planning',      subtitle: 'Your points, mock history, grade plans and course reach in one place.',             showHeader: true  },
  'planner':         { themeColor: '#7DA37A', eyebrow: 'Plan · Planner',              subtitle: 'A data-driven study planner powered by your subject goals.',                       showHeader: true  },
  'war-room':        { themeColor: '#F26B1F', eyebrow: 'Plan · Strategy',             subtitle: 'Know what needs attention, understand why, and decide what to do next.', showHeader: true },
  'comeback':        { themeColor: '#E08938', eyebrow: 'Plan · Comeback',             subtitle: 'Find your quickest wins and build a comeback plan.',                                showHeader: true  },
  'future-finder':   { themeColor: '#C76489', eyebrow: 'Understand · Career discovery', subtitle: 'Discover the courses, careers, and possible lives that fit who you are.',         showHeader: true  },
  'future-finder-revamped': { themeColor: '#C76489', eyebrow: 'Understand · Interests (RIASEC)', subtitle: 'Discover the courses, careers and lives that fit who you are — your interests matched to CAO courses, points kept honest.', showHeader: true },
  'syllabus-xray':   { themeColor: '#2C4B6E', eyebrow: 'Understand · Exam intel',     subtitle: 'See where the marks are hiding in every paper, every section, every question.',   showHeader: true  },
  'points-passport': { themeColor: '#B8A079', eyebrow: 'Track · Tracker',             subtitle: 'Mock trends and grade bargains, all at a glance.',                                  showHeader: true  },
  'exam-reps':       { themeColor: '#5E9C7B', eyebrow: 'Technique · Practice',        subtitle: 'One real exam question at a time — marked the examiner’s way, so you see exactly where the marks were.', showHeader: true  },
  'college-compass': { themeColor: '#2A7D6F', eyebrow: 'Plan · Roadmap',              subtitle: 'Your year-by-year runway to college — every CAO, HEAR, DARE and scholarship deadline, in order.', showHeader: false },
  'catch-up-lane':   { themeColor: '#0E9AA8', eyebrow: 'Catch up · Recovery',         subtitle: 'Missed some classes? Pick a subject and get caught up one quick topic at a time — no catch-up is too small.', showHeader: true  },
  // No header. Mark Bank is used daily, and a tool built for daily use must not
  // re-explain itself daily: the eyebrow, title and subtitle cost ~238px at the top
  // of every screen INCLUDING every review card, which is where the exam question
  // should be. The subtitle still does its job on the tool tile, read once.
  'mark-bank':       { themeColor: '#123B2B', eyebrow: 'Practise · Spaced repetition', subtitle: 'Real exam questions, marked point by point against the real scheme, brought back to you right before you\u2019d forget them.', showHeader: false },
  'paper-trail':     { themeColor: '#33658A', eyebrow: 'Understand · Exam archive',   subtitle: 'Every past paper and marking scheme, free — your subjects, your level, three taps.', showHeader: true },
  'diagram-vault':   { themeColor: '#F26B1F', eyebrow: 'Understand · Exam diagrams',  subtitle: 'Every diagram, graph, map and chart that has come up — cropped from the paper and decoded.', showHeader: true },
  'answer-architect': { themeColor: '#F26B1F', eyebrow: 'Understand · Top-answer skeletons', subtitle: 'The mark-earning skeleton of a top answer — the beats a full-marks answer hits, in order, from the SEC scheme.', showHeader: true },
  'definition-drill': { themeColor: '#F26B1F', eyebrow: 'Understand · Key definitions', subtitle: 'Drill the exact mark-earning wording the SEC scheme awards the definition marks for.', showHeader: true },
  'coursework-companion': { themeColor: '#F26B1F', eyebrow: 'Understand · Coursework & projects', subtitle: 'The coursework, project and practical components — marked exactly as the filed SEC scheme prints it.', showHeader: true },
  'command-word-reflex': { themeColor: '#6366F1', eyebrow: 'Technique · Exam skills', subtitle: 'Half of exam technique is reading the question right. Spot the command word in real questions and learn what it’s really asking — and the trap that loses marks.', showHeader: true },
  'how-they-did-it':  { themeColor: '#0E7C6B', eyebrow: 'Mindset · Real stories', subtitle: 'Real people who started where you are — money tight, learning differently, new to the country, first in the family — and the actual moves they made.', showHeader: true },
  'your-possible-life': { themeColor: '#2E6E8E', eyebrow: 'Understand · Career discovery', subtitle: 'Explore real careers, step inside an ordinary day, and keep routes that feel worth testing.', showHeader: true },
  'oral-trainer':    { themeColor: '#4C8C5E', eyebrow: 'Technique · Speaking exam', subtitle: 'The one exam no app prepares you for — the oral. Rehearse it out loud, record yourself, and know exactly where you stand on every part.', showHeader: true },
  'examiners-chair': { themeColor: '#9E4A3E', eyebrow: 'Technique · Marking literacy', subtitle: 'Sit on the other side of the desk. Mark real-style scripts against the real SEC rules, and learn to see your own answers the way the examiner will.', showHeader: true },
};

interface StudyNowBlock {
  subject: string;
  sessionType: 'new-learning' | 'practice' | 'revision';
  durationMinutes: number;
  dateKey: string;
  blockId: string;
}

interface InnovationZoneProps {
  onBack: () => void;
  onSelectModule?: (moduleId: string) => void;
  user?: { uid: string; school?: string; yearGroup?: YearGroup; curriculumLevel?: 'junior' | 'senior' } | null;
  /** Profile already loaded by ProgressContext. It unlocks tools immediately
   *  and is the fallback when the local-only dev session cannot read Firestore. */
  initialSubjectProfile?: StudentSubjectProfile | null;
  savedJourneyResult?: JourneyResult | null;
  onJourneyComplete?: (result: JourneyResult) => void;
  settings: UserSettings;
  updateSetting: <K extends keyof UserSettings>(key: K, value: UserSettings[K]) => void;
  onCosmeticUnlocksChange?: (unlocks: CosmeticUnlocks) => void;
  onStudyNow?: (block: StudyNowBlock) => void;
  dismissedGuides?: Record<string, string>;
  onDismissGuide?: (id: string) => void;
}

// ─── Data Validation Helpers ─────────────────────────────────────────────────

/** Ensures a value is a finite number, falling back to a default. */
function safeNum(val: unknown, fallback: number = 0): number {
    if (typeof val === 'number' && Number.isFinite(val)) return val;
    return fallback;
}

/** Validates PointsData from Firestore, ensuring no NaN or undefined values. */
function validatePointsData(raw: unknown): PointsData {
    if (!raw || typeof raw !== 'object') return { totalEarned: 0, totalSpent: 0 };
    const obj = raw as Record<string, unknown>;
    return {
        totalEarned: safeNum(obj.totalEarned),
        totalSpent: safeNum(obj.totalSpent),
    };
}

/** Suspense fallback shown while a tool's code-split chunk loads. */
const ToolLoadingFallback: React.FC = () => <LoadingSpinner />;

// ─── InnovationZone ──────────────────────────────────────────────────────────

const InnovationZone: React.FC<InnovationZoneProps> = ({ onBack, onSelectModule, user, initialSubjectProfile, savedJourneyResult, onJourneyComplete, settings: _settings, updateSetting: _updateSetting, onCosmeticUnlocksChange, onStudyNow, dismissedGuides: _dismissedGuides, onDismissGuide: _onDismissGuide }) => {
    const { showToast } = useToast();
    const nav = useNavigation();
    const activeTool = nav.state.activeTool;
    const setActiveTool = nav.setActiveTool;

    // Retired tool aliases keep old bookmarks and persisted navigation useful.
    useEffect(() => {
        if (activeTool === 'career-paths') setActiveTool('your-possible-life');
    }, [activeTool, setActiveTool]);
    const [subjectProfile, setSubjectProfile] = useState<StudentSubjectProfile | null>(() => (
        initialSubjectProfile ? { restDays: [], ...initialSubjectProfile } : null
    ));
    const [showOnboarding, setShowOnboarding] = useState(false);
    const [profileLoaded, setProfileLoaded] = useState(Boolean(initialSubjectProfile));
    const [pendingToolId, setPendingToolId] = useState<string | null>(null);
    const [timetableCompletions, setTimetableCompletions] = useState<TimetableCompletions>({});
    const [timetableStreak, setTimetableStreak] = useState<TimetableStreak>({ currentStreak: 0, lastActiveDate: '', longestStreak: 0 });
    const [reflections, setReflections] = useState<StudyReflection[]>([]);
    const [pointsData, setPointsData] = useState<PointsData>({ totalEarned: 0, totalSpent: 0 });
    const [cosmeticUnlocks, setCosmeticUnlocks] = useState<CosmeticUnlocks>({ avatarSeeds: [], themeColors: [], cardStyles: [] });
    const [earnedRest, setEarnedRest] = useState<EarnedRest>({ skippedSessions: [], restDayPasses: [] });
    const [schoolEvents, setSchoolEvents] = useState<SchoolEvent[]>([]);
    const [gcRecommendations, setGcRecommendations] = useState<Record<string, { fromName: string; message?: string }>>({});

    // Load school events for student's school + year group
    useEffect(() => {
        if (!user?.school) return;
        let cancelled = false;
        const loadEvents = async () => {
            try {
                const eventsDoc = await getDoc(doc(db, 'gcEvents', user.school!));
                if (cancelled) return;
                if (eventsDoc.exists()) {
                    const data = eventsDoc.data();
                    const allEvents: SchoolEvent[] = data.events || [];
                    const yg = user.yearGroup || '6th';
                    setSchoolEvents(allEvents.filter(e => e.yearGroup === 'both' || e.yearGroup === yg));
                }
            } catch (err) {
                if (!cancelled) console.error('Failed to load school events:', err);
            }
        };
        loadEvents();
        return () => { cancelled = true; };
    }, [user?.school, user?.yearGroup]);

    // Refs to always access latest state in callbacks (avoids stale closures)
    const cosmeticUnlocksRef = useRef(cosmeticUnlocks);
    cosmeticUnlocksRef.current = cosmeticUnlocks;
    const onCosmeticUnlocksChangeRef = useRef(onCosmeticUnlocksChange);
    onCosmeticUnlocksChangeRef.current = onCosmeticUnlocksChange;
    const [showJournal, setShowJournal] = useState(false);
    // Points panel is hidden by default; revealed by the `?` tooltip
    // button in the header. Pure local state — the old persisted-guide
    // flow was retired since the panel no longer interrupts on landing.
    const [showPointsPanel, setShowPointsPanel] = useState(false);
    const hidePointsPanel = useCallback(() => setShowPointsPanel(false), []);
    const togglePointsPanel = useCallback(() => setShowPointsPanel(v => !v), []);

    // ProgressContext is the immediate source of truth. This also makes the
    // local dev account fully usable: its reserved uid has no Firebase token,
    // so the refresh below is expected to be rejected by security rules.
    useEffect(() => {
        if (!initialSubjectProfile) return;
        setSubjectProfile({ restDays: [], ...initialSubjectProfile });
        setProfileLoaded(true);
    }, [initialSubjectProfile]);

    // Refresh the subject profile and supporting Launchpad data from Firebase.
    useEffect(() => {
        if (!user?.uid) {
            setProfileLoaded(true);
            return;
        }
        let cancelled = false;
        const loadProfile = async () => {
            try {
                const progressDoc = await getDoc(doc(db, 'progress', user.uid));
                if (cancelled) return;
                if (progressDoc.exists()) {
                    const data = progressDoc.data();
                    if (data.subjectProfile) {
                        setSubjectProfile({ restDays: [], ...data.subjectProfile } as StudentSubjectProfile);
                    }
                    if (data.timetableCompletions) {
                        setTimetableCompletions(data.timetableCompletions as TimetableCompletions);
                    }
                    if (data.timetableStreak) {
                        setTimetableStreak(data.timetableStreak as TimetableStreak);
                    }
                    if (data.reflections) {
                        setReflections(data.reflections as StudyReflection[]);
                    }
                    setPointsData(validatePointsData(data.pointsData));
                    if (data.cosmeticUnlocks) {
                        setCosmeticUnlocks({
                            avatarSeeds: [],
                            themeColors: [],
                            cardStyles: [],
                            ...data.cosmeticUnlocks,
                        });
                    }
                    if (data.earnedRest) {
                        setEarnedRest(data.earnedRest as EarnedRest);
                    }
                }
            } catch (err) {
                if (!cancelled) console.error('Failed to load subject profile:', err);
            }
            if (!cancelled) setProfileLoaded(true);
        };
        loadProfile();
        return () => { cancelled = true; };
    }, [user?.uid]);

    // Load GC recommendations from notifications
    useEffect(() => {
        if (!user?.uid) return;
        let cancelled = false;
        const loadRecommendations = async () => {
            try {
                const notifications = await getNotifications(user.uid);
                const recMap: Record<string, { fromName: string; message?: string }> = {};
                for (const n of notifications) {
                    if (n.type === 'gc-recommendation' && !n.read && n.actionToolId && !recMap[n.actionToolId]) {
                        recMap[n.actionToolId] = { fromName: n.fromGCName || 'your counsellor', message: n.body };
                    }
                }
                if (!cancelled) setGcRecommendations(recMap);
            } catch (err) { console.error('Failed to load GC recommendations:', err); }
        };
        loadRecommendations();
        return () => { cancelled = true; };
    }, [user?.uid]);

    const handleOnboardingComplete = useCallback(async (profile: StudentSubjectProfile) => {
        setShowOnboarding(false);
        if (pendingToolId) {
            setActiveTool(pendingToolId);
            setPendingToolId(null);
        }
        // Commit OPTIMISTICALLY, then roll back if the write is actually
        // rejected.
        //
        // Do NOT gate this on the awaited setDoc: firebase.ts enables
        // persistentLocalCache, and with offline persistence a setDoc promise
        // settles only on SERVER acknowledgement. Offline it never resolves
        // AND never rejects — so awaiting first would leave a student on flaky
        // school wifi staring at an empty tool body with every profile-gated
        // tool locked until they fully reloaded the app, with no error and no
        // spinner. The write itself is safe: Firestore applies it to the local
        // cache immediately and flushes it when the connection returns.
        const previousProfile = subjectProfile;
        setSubjectProfile(profile);
        if (user?.uid) {
            setDoc(doc(db, 'progress', user.uid), { subjectProfile: profile }, { merge: true })
                .catch(err => {
                    console.error('Failed to save subject profile:', err);
                    showToast('Couldn\'t save your subjects — please try again', 'error');
                    setSubjectProfile(previousProfile);
                });
        }
    }, [user?.uid, pendingToolId, setActiveTool, subjectProfile]);

    const _getStreakMultiplier = useCallback((streak: number): number => {
        if (streak >= 14) return 2.5;
        if (streak >= 7) return 2.0;
        if (streak >= 3) return 1.5;
        return 1.0;
    }, []);

    const executeToggle = useCallback((dateKey: string, blockId: string, completed: boolean, extraFirestoreData?: Record<string, any>) => {
        setTimetableCompletions(prev => {
            const updated = { ...prev };
            const dayArr = [...(updated[dateKey] ?? [])];
            if (completed) {
                if (!dayArr.includes(blockId)) dayArr.push(blockId);
            } else {
                const idx = dayArr.indexOf(blockId);
                if (idx >= 0) dayArr.splice(idx, 1);
            }
            const dayEmptied = dayArr.length === 0;
            if (dayEmptied) {
                delete updated[dateKey];
            } else {
                updated[dateKey] = dayArr;
            }

            const restDays = subjectProfile?.restDays ?? [];
            const { currentStreak, lastActiveDate } = computeStreak(updated, restDays, new Date(), earnedRest.restDayPasses);
            const newLongest = Math.max(timetableStreak.longestStreak, currentStreak);
            const newStreak: TimetableStreak = { currentStreak, lastActiveDate, longestStreak: newLongest };
            setTimetableStreak(newStreak);

            if (user?.uid) {
                // `delete updated[dateKey]` only removes the day locally — a
                // merge:true setDoc builds its field mask from the keys that ARE
                // present, so an omitted key is left untouched on the server.
                // Un-ticking the last block of a day therefore looked like it
                // worked and silently came back on reload, leaving the GC's
                // "active days" permanently ahead of the student's own count.
                // deleteField() is legal inside a merge setDoc; a dotted path
                // string is not (that's updateDoc-only syntax).
                const completionsPayload: Record<string, any> = { ...updated };
                if (dayEmptied) completionsPayload[dateKey] = deleteField();

                setDoc(doc(db, 'progress', user.uid), {
                    timetableCompletions: completionsPayload,
                    timetableStreak: newStreak,
                    ...extraFirestoreData,
                }, { merge: true }).catch(err => { console.error('Failed to save completions:', err); showToast('Couldn\'t save — check your connection', 'error'); });
            }

            return updated;
        });
    }, [subjectProfile?.restDays, timetableStreak.longestStreak, user?.uid, earnedRest.restDayPasses]);

    const handleToggleCompletion = useCallback(async (dateKey: string, blockId: string, completed: boolean) => {
        if (completed) {
            // "Already Studied" flow: 5 pts flat, no reflection.
            //
            // Award ONCE PER BLOCK. Un-ticking deducts nothing, so without this
            // guard a student could tick/un-tick the same block repeatedly and
            // farm points indefinitely. That was previously harmless because
            // the award went to a dead root field and local state reset on
            // reload — fixing the write path makes it permanent and spendable
            // (rest-day passes feed computeStreak), so it has to be idempotent
            // now. executeToggle is already idempotent about the completion.
            const alreadyCredited = (timetableCompletions[dateKey] ?? []).includes(blockId);
            if (alreadyCredited) {
                executeToggle(dateKey, blockId, true);
                return;
            }
            const ALREADY_STUDIED_POINTS = 5;
            setPointsData(prev => ({
                ...prev,
                totalEarned: prev.totalEarned + ALREADY_STUDIED_POINTS,
            }));
            // A dotted key inside setDoc is NOT a field path — setDoc treats it
            // as one literal segment, so this used to create a root field
            // called "pointsData.totalEarned" and the real total never moved.
            // Every timetable tick's points were lost. (Dotted paths only work
            // in updateDoc, which can't be used here: the progress doc may not
            // exist yet.) merge:true deep-merges maps, so the sibling
            // pointsData.totalSpent written elsewhere is preserved.
            executeToggle(dateKey, blockId, true, {
                pointsData: { totalEarned: increment(ALREADY_STUDIED_POINTS) },
            });
        } else {
            executeToggle(dateKey, blockId, false);
        }
    }, [executeToggle, pointsData, timetableCompletions]);

    const handleToolClick = useCallback((toolId: string, needsProfile: boolean) => {
        if (needsProfile && !profileLoaded) return;
        if (needsProfile && !subjectProfile) {
            setPendingToolId(toolId);
            setShowOnboarding(true);
            return;
        }
        setActiveTool(toolId);
    }, [subjectProfile, profileLoaded, setActiveTool]);

    // Curriculum level — used by the tools array below for curriculum-aware
    // titles (e.g. Future Finder → "Subject Explorer" for JC users) and by
    // the filter further down. Declared here so the tools array can read it.
    const curriculumLevel = user?.curriculumLevel ?? 'senior';

    const tools = [
        {
            id: 'journey', title: 'Academic Journey Simulator', description: 'Navigate the choices of your final school year.', icon: GitBranch, needsProfile: false,
            curriculum: 'senior' as const,
            tag: 'Simulator', accentHex: '#f59e0b', gridClass: 'md:col-span-3',
            iconBg: 'bg-amber-100 dark:bg-amber-900/30', iconColor: 'text-amber-600 dark:text-amber-400',
            accentBarColor: 'bg-amber-500', tagBg: 'bg-amber-100 dark:bg-amber-900/30', tagText: 'text-amber-700 dark:text-amber-400',
            hoverBorder: 'hover:border-amber-400/50 dark:hover:border-amber-500/40',
            component: <AcademicJourneyGame onSelectModule={onSelectModule} user={user} savedJourneyResult={savedJourneyResult} onJourneyComplete={onJourneyComplete} />,
        },
        {
            id: 'cao-simulator', title: 'Points Passport', description: 'Your points, mock history and grade planner in one place.', icon: Calculator, needsProfile: true,
            curriculum: 'senior' as const,
            tag: 'Simulator', accentHex: '#64748b', gridClass: 'md:col-span-3',
            iconBg: 'bg-slate-100 dark:bg-slate-800/40', iconColor: 'text-slate-600 dark:text-slate-300',
            accentBarColor: 'bg-slate-500', tagBg: 'bg-slate-100 dark:bg-slate-800/40', tagText: 'text-slate-600 dark:text-slate-300',
            hoverBorder: 'hover:border-slate-400/50 dark:hover:border-slate-500/40',
            component: subjectProfile && user ? <PointsPassport uid={user.uid} profile={subjectProfile} initialTab="planner" onOpenSettings={() => setShowOnboarding(true)} /> : null,
        },
        {
            id: 'planner', title: 'Spaced Repetition Timetable', description: 'A data-driven study planner powered by your subject goals.', icon: CalendarDays, needsProfile: true,
            curriculum: 'both' as const,
            tag: 'Planner', accentHex: '#6366f1', gridClass: 'md:col-span-2',
            iconBg: 'bg-indigo-100 dark:bg-indigo-900/30', iconColor: 'text-indigo-600 dark:text-indigo-400',
            accentBarColor: 'bg-indigo-500', tagBg: 'bg-indigo-100 dark:bg-indigo-900/30', tagText: 'text-indigo-700 dark:text-indigo-400',
            hoverBorder: 'hover:border-indigo-400/50 dark:hover:border-indigo-500/40',
            component: subjectProfile ? <SpacedRepetitionTimetable profile={subjectProfile} uid={user?.uid} onOpenSettings={() => setShowOnboarding(true)} completions={timetableCompletions} streak={timetableStreak} onToggleCompletion={handleToggleCompletion} onOpenJournal={() => setShowJournal(true)} skippedSessions={earnedRest.skippedSessions} onStudyNow={onStudyNow} schoolEvents={schoolEvents} onBlockDurationChange={(_s, _t, newDuration) => { const previous = subjectProfile; const updated = { ...subjectProfile, defaultBlockDuration: newDuration }; setSubjectProfile(updated); if (user?.uid) { saveInBackground(setDoc(doc(db, 'progress', user.uid), { subjectProfile: updated }, { merge: true }), 'InnovationZone.saveBlockDuration', () => setSubjectProfile(previous)); } }} onRestDaysChange={(days) => { const previous = subjectProfile; const updated = { ...subjectProfile, restDays: days }; setSubjectProfile(updated); if (user?.uid) { saveInBackground(setDoc(doc(db, 'progress', user.uid), { subjectProfile: updated }, { merge: true }), 'InnovationZone.saveRestDays', () => setSubjectProfile(previous)); } }} /> : null,
        },
        {
            id: 'war-room', title: 'War Room', description: 'Your strategic study command centre.', icon: Target, needsProfile: true,
            curriculum: 'senior' as const,
            tag: 'Strategy', accentHex: '#dc2626', gridClass: 'md:col-span-2',
            iconBg: 'bg-red-100 dark:bg-red-900/30', iconColor: 'text-red-600 dark:text-red-400',
            accentBarColor: 'bg-red-500', tagBg: 'bg-red-100 dark:bg-red-900/30', tagText: 'text-red-700 dark:text-red-400',
            hoverBorder: 'hover:border-red-400/50 dark:hover:border-red-500/40',
            component: subjectProfile ? <WarRoom uid={user!.uid} profile={subjectProfile} timetableCompletions={timetableCompletions} skippedSessions={earnedRest.skippedSessions} onStudyNow={onStudyNow} /> : null,
        },
        {
            id: 'comeback', title: 'Comeback Engine', description: 'A realistic seven-day recovery plan built from your actual study pattern.', icon: Rocket, needsProfile: true,
            curriculum: 'both' as const,
            tag: 'Comeback', accentHex: '#f97316', gridClass: 'md:col-span-2',
            iconBg: 'bg-orange-100 dark:bg-orange-900/30', iconColor: 'text-orange-600 dark:text-orange-400',
            accentBarColor: 'bg-orange-500', tagBg: 'bg-orange-100 dark:bg-orange-900/30', tagText: 'text-orange-700 dark:text-orange-400',
            hoverBorder: 'hover:border-orange-400/50 dark:hover:border-orange-500/40',
            component: subjectProfile ? <ComebackEngine uid={user!.uid} profile={subjectProfile} timetableCompletions={timetableCompletions} onOpenTool={setActiveTool} /> : null,
        },
        {
            // Option B (per Phase 2 spec): same tile, but the title and
            // description swap for JC users. Inside FutureFinder.tsx the
            // entire post-quiz output diverges — JC runs the cluster
            // matcher and renders the Subject Explorer results view.
            id: 'future-finder',
            title: curriculumLevel === 'junior' ? 'Subject Explorer' : 'Future Finder Old',
            description: curriculumLevel === 'junior'
              ? 'Find out which subjects you\'d enjoy in senior cycle.'
              : 'Discover college courses that fit who you are.',
            icon: Compass, needsProfile: true,
            // TEMP (pre-demo): hidden from Senior Cycle so the old Future Finder
            // doesn't show alongside the revamped 'future-finder-revamped' tile.
            // Restricted to 'junior' keeps this tile alive as the JC Subject Explorer.
            // To fully restore for senior, change back to 'both'.
            curriculum: 'junior' as const,
            tag: 'Career Discovery', accentHex: '#6366f1', gridClass: 'md:col-span-2',
            iconBg: 'bg-indigo-100 dark:bg-indigo-900/30', iconColor: 'text-indigo-600 dark:text-indigo-400',
            accentBarColor: 'bg-indigo-500', tagBg: 'bg-indigo-100 dark:bg-indigo-900/30', tagText: 'text-indigo-700 dark:text-indigo-400',
            hoverBorder: 'hover:border-indigo-400/50 dark:hover:border-indigo-500/40',
            component: subjectProfile ? <FutureFinder uid={user!.uid} profile={subjectProfile} onOpenCareerPaths={() => setActiveTool('your-possible-life')} /> : null,
        },
        {
            id: 'future-finder-revamped', title: 'Future Finder', description: 'Interest-based (RIASEC) course matching — ranked CAO courses that fit who you are.', icon: Compass, needsProfile: true,
            curriculum: 'senior' as const,
            tag: 'Career Discovery', accentHex: '#C76489', gridClass: 'md:col-span-2',
            iconBg: 'bg-pink-100 dark:bg-pink-900/30', iconColor: 'text-pink-700 dark:text-pink-300',
            accentBarColor: 'bg-pink-500', tagBg: 'bg-pink-100 dark:bg-pink-900/30', tagText: 'text-pink-700 dark:text-pink-400',
            hoverBorder: 'hover:border-pink-400/50 dark:hover:border-pink-500/40',
            component: subjectProfile ? <FutureFinderRevamped uid={user!.uid} profile={subjectProfile} onOpenCareerPaths={() => setActiveTool('your-possible-life')} /> : null,
        },
        {
            id: 'syllabus-xray', title: 'Syllabus X-Ray', description: 'See where the marks are hiding in your exams.', icon: ScanSearch, needsProfile: false,
            curriculum: 'senior' as const,
            tag: 'Exam Intel', accentHex: '#e11d48', gridClass: 'md:col-span-2',
            iconBg: 'bg-rose-100 dark:bg-rose-900/30', iconColor: 'text-rose-600 dark:text-rose-400',
            accentBarColor: 'bg-rose-500', tagBg: 'bg-rose-100 dark:bg-rose-900/30', tagText: 'text-rose-700 dark:text-rose-400',
            hoverBorder: 'hover:border-rose-400/50 dark:hover:border-rose-500/40',
            component: <SyllabusXRay studentSubjects={subjectProfile?.subjects.map(s => s.subjectName)} uid={user?.uid} examDate={subjectProfile?.examStartDate} />,
        },
        {
            id: 'points-passport', title: 'Points Passport', description: 'Mock trends & grade bargains at a glance.', icon: Map, needsProfile: true,
            curriculum: 'senior' as const,
            tag: 'Tracker', accentHex: '#0ea5e9', gridClass: 'md:col-span-2',
            iconBg: 'bg-sky-100 dark:bg-sky-900/30', iconColor: 'text-sky-600 dark:text-sky-400',
            accentBarColor: 'bg-sky-500', tagBg: 'bg-sky-100 dark:bg-sky-900/30', tagText: 'text-sky-700 dark:text-sky-400',
            hoverBorder: 'hover:border-sky-400/50 dark:hover:border-sky-500/40',
            component: subjectProfile && user ? <PointsPassport uid={user.uid} profile={subjectProfile} onOpenSettings={() => setShowOnboarding(true)} /> : null,
        },
        {
            // Senior-cycle only (TY/5th/6th). `seniorYearsOnly` additionally
            // hides it from graduated users, who still map to the 'senior'
            // curriculum level (see isActiveSeniorYear). needsProfile:false —
            // it reads only the student's year, never their subject profile.
            id: 'college-compass', title: 'College Compass', description: 'Your runway to college — CAO, HEAR, DARE & scholarships, in order.', icon: Milestone, needsProfile: false,
            curriculum: 'senior' as const, seniorYearsOnly: true,
            tag: 'Roadmap', accentHex: '#2A7D6F', gridClass: 'md:col-span-3',
            iconBg: 'bg-teal-100 dark:bg-teal-900/30', iconColor: 'text-teal-700 dark:text-teal-300',
            accentBarColor: 'bg-teal-600', tagBg: 'bg-teal-100 dark:bg-teal-900/30', tagText: 'text-teal-700 dark:text-teal-400',
            hoverBorder: 'hover:border-teal-400/50 dark:hover:border-teal-500/40',
            component: <CollegeCompass uid={user?.uid} yearGroup={user?.yearGroup} />,
        },
        {
            id: 'catch-up-lane', title: 'Catch-Up Lane', description: 'Missed class? Get caught up, one quick topic at a time.', icon: Waypoints, needsProfile: false,
            // The content library covers both Junior Cycle and Leaving Cert.
            curriculum: 'both' as const,
            tag: 'Catch up', accentHex: '#0E9AA8', gridClass: 'md:col-span-2',
            iconBg: 'bg-cyan-100 dark:bg-cyan-900/30', iconColor: 'text-cyan-700 dark:text-cyan-300',
            accentBarColor: 'bg-cyan-500', tagBg: 'bg-cyan-100 dark:bg-cyan-900/30', tagText: 'text-cyan-700 dark:text-cyan-400',
            hoverBorder: 'hover:border-cyan-400/50 dark:hover:border-cyan-500/40',
            component: <CatchUpLane uid={user?.uid} studentSubjects={subjectProfile?.subjects.map(s => s.subjectName)} studentCycle={curriculumLevel === 'junior' ? 'junior-cycle' : 'leaving-cert'} />,
        },
        {
            id: 'mark-bank', title: 'Mark Bank', description: 'Real exam questions, marked point by point \u2014 brought back before you forget.', icon: ListChecks, needsProfile: false,
            curriculum: 'senior' as const,
            tag: 'Spaced repetition', accentHex: '#123B2B', gridClass: 'md:col-span-2',
            iconBg: 'bg-emerald-100 dark:bg-emerald-900/30', iconColor: 'text-emerald-900 dark:text-emerald-300',
            accentBarColor: 'bg-emerald-800', tagBg: 'bg-emerald-100 dark:bg-emerald-900/30', tagText: 'text-emerald-900 dark:text-emerald-400',
            hoverBorder: 'hover:border-emerald-400/50 dark:hover:border-emerald-500/40',
            component: <MarkBank uid={user?.uid} />,
        },
        {
            id: 'paper-trail', title: 'Paper Trail', description: 'Every SEC past paper and marking scheme — three taps away.', icon: FileSearch, needsProfile: false,
            // 'both': serves Junior Cycle (new-spec) AND Leaving Cert / LCA papers (cycle-filtered picker).
            curriculum: 'both' as const,
            tag: 'Exam archive', accentHex: '#33658A', gridClass: 'md:col-span-2',
            iconBg: 'bg-sky-100 dark:bg-sky-900/30', iconColor: 'text-sky-800 dark:text-sky-300',
            accentBarColor: 'bg-sky-700', tagBg: 'bg-sky-100 dark:bg-sky-900/30', tagText: 'text-sky-800 dark:text-sky-400',
            hoverBorder: 'hover:border-sky-400/50 dark:hover:border-sky-500/40',
            component: <PaperTrail uid={user?.uid} studentSubjects={subjectProfile?.subjects.map(s => s.subjectName)} studentLevels={subjectProfile?.subjects.map(s => ({ name: s.subjectName, level: s.level }))} studentCycle={curriculumLevel === 'junior' ? 'junior-cycle' : 'leaving-cert'} isLca={isLcaYear(user?.yearGroup)} onboardingExamDate={subjectProfile?.examStartDate} onOpenTool={setActiveTool} />,
        },
        {
            id: 'diagram-vault', title: 'Diagram Vault', description: 'Every diagram, graph, map and chart that has come up in the exams — decoded.', icon: Images, needsProfile: false,
            // 'both': the figure corpus spans Junior Cycle and Leaving Cert subjects.
            curriculum: 'both' as const,
            tag: 'Exam diagrams', accentHex: '#F26B1F', gridClass: 'md:col-span-2',
            iconBg: 'bg-orange-100 dark:bg-orange-900/30', iconColor: 'text-orange-700 dark:text-orange-300',
            accentBarColor: 'bg-orange-500', tagBg: 'bg-orange-100 dark:bg-orange-900/30', tagText: 'text-orange-700 dark:text-orange-400',
            hoverBorder: 'hover:border-orange-400/50 dark:hover:border-orange-500/40',
            component: <DiagramVault studentSubjects={subjectProfile?.subjects.map(s => s.subjectName)} />,
        },
        {
            id: 'answer-architect', title: 'Answer Architect', description: 'The mark-earning skeleton of a top answer — the beats a full-marks answer is built from, in order.', icon: ListChecks, needsProfile: false,
            curriculum: 'senior' as const,
            tag: 'Top-answer skeletons', accentHex: '#F26B1F', gridClass: 'md:col-span-2',
            iconBg: 'bg-orange-100 dark:bg-orange-900/30', iconColor: 'text-orange-700 dark:text-orange-300',
            accentBarColor: 'bg-orange-500', tagBg: 'bg-orange-100 dark:bg-orange-900/30', tagText: 'text-orange-700 dark:text-orange-400',
            hoverBorder: 'hover:border-orange-400/50 dark:hover:border-orange-500/40',
            component: <AnswerArchitect studentSubjects={subjectProfile?.subjects.map(s => s.subjectName)} />,
        },
        {
            id: 'definition-drill', title: 'Definition Drill', description: 'Drill the exact mark-earning wording the SEC scheme awards the definition marks for.', icon: SpellCheck, needsProfile: false,
            curriculum: 'senior' as const,
            tag: 'Key definitions', accentHex: '#F26B1F', gridClass: 'md:col-span-2',
            iconBg: 'bg-orange-100 dark:bg-orange-900/30', iconColor: 'text-orange-700 dark:text-orange-300',
            accentBarColor: 'bg-orange-500', tagBg: 'bg-orange-100 dark:bg-orange-900/30', tagText: 'text-orange-700 dark:text-orange-400',
            hoverBorder: 'hover:border-orange-400/50 dark:hover:border-orange-500/40',
            component: <DefinitionDrill studentSubjects={subjectProfile?.subjects.map(s => s.subjectName)} />,
        },
        {
            id: 'coursework-companion', title: 'Coursework Companion', description: 'The coursework, project and practical components — and exactly how the SEC scheme marks them.', icon: FolderCheck, needsProfile: false,
            curriculum: 'senior' as const,
            tag: 'Coursework & projects', accentHex: '#F26B1F', gridClass: 'md:col-span-2',
            iconBg: 'bg-orange-100 dark:bg-orange-900/30', iconColor: 'text-orange-700 dark:text-orange-300',
            accentBarColor: 'bg-orange-500', tagBg: 'bg-orange-100 dark:bg-orange-900/30', tagText: 'text-orange-700 dark:text-orange-400',
            hoverBorder: 'hover:border-orange-400/50 dark:hover:border-orange-500/40',
            component: <CourseworkCompanion studentSubjects={subjectProfile?.subjects.map(s => s.subjectName)} />,
        },
        {
            id: 'oral-trainer', title: 'Irish Oral Trainer', description: 'Rehearse the Irish oral out loud, record yourself, and track your readiness on every part.', icon: Mic, needsProfile: false,
            curriculum: 'senior' as const,
            tag: 'Speaking exam', accentHex: '#4C8C5E', gridClass: 'md:col-span-2',
            iconBg: 'bg-emerald-100 dark:bg-emerald-900/30', iconColor: 'text-emerald-700 dark:text-emerald-300',
            accentBarColor: 'bg-emerald-500', tagBg: 'bg-emerald-100 dark:bg-emerald-900/30', tagText: 'text-emerald-700 dark:text-emerald-400',
            hoverBorder: 'hover:border-emerald-400/50 dark:hover:border-emerald-500/40',
            component: <OralExamTrainer uid={user?.uid} />,
        },
        {
            id: 'examiners-chair', title: 'The Examiner’s Chair', description: 'Mark scripts against the real SEC rules — and learn exactly where marks are won and lost.', icon: Stamp, needsProfile: false,
            curriculum: 'senior' as const,
            tag: 'Marking literacy', accentHex: '#9E4A3E', gridClass: 'md:col-span-2',
            iconBg: 'bg-rose-100 dark:bg-rose-900/30', iconColor: 'text-rose-800 dark:text-rose-300',
            accentBarColor: 'bg-rose-700', tagBg: 'bg-rose-100 dark:bg-rose-900/30', tagText: 'text-rose-800 dark:text-rose-400',
            hoverBorder: 'hover:border-rose-400/50 dark:hover:border-rose-500/40',
            component: <ExaminersChair uid={user?.uid} />,
        },
        {
            id: 'command-word-reflex', title: 'Command-Word Reflex', description: 'Spot the command word in real questions — and dodge the trap.', icon: Highlighter, needsProfile: false,
            // 'both': has Junior Cycle AND Leaving Cert content (cycle-grouped picker), so visible to JC and senior users.
            curriculum: 'both' as const,
            tag: 'Exam skills', accentHex: '#6366F1', gridClass: 'md:col-span-2',
            iconBg: 'bg-indigo-100 dark:bg-indigo-900/30', iconColor: 'text-indigo-700 dark:text-indigo-300',
            accentBarColor: 'bg-indigo-500', tagBg: 'bg-indigo-100 dark:bg-indigo-900/30', tagText: 'text-indigo-700 dark:text-indigo-400',
            hoverBorder: 'hover:border-indigo-400/50 dark:hover:border-indigo-500/40',
            component: <CommandWordReflex uid={user?.uid} studentSubjects={subjectProfile?.subjects.map(s => s.subjectName)} studentCycle={curriculumLevel === 'junior' ? 'junior-cycle' : 'leaving-cert'} />,
        },
        {
            id: 'how-they-did-it', title: 'How They Did It', description: 'Real people who started where you are — and the moves they made.', icon: Users, needsProfile: false,
            curriculum: 'both' as const,
            tag: 'Real stories', accentHex: '#C8862B', gridClass: 'md:col-span-3',
            iconBg: 'bg-amber-100 dark:bg-amber-900/30', iconColor: 'text-amber-700 dark:text-amber-300',
            accentBarColor: 'bg-amber-500', tagBg: 'bg-amber-100 dark:bg-amber-900/30', tagText: 'text-amber-700 dark:text-amber-400',
            hoverBorder: 'hover:border-amber-400/50 dark:hover:border-amber-500/40',
            component: <HowTheyDidIt uid={user?.uid} studentSubjects={subjectProfile?.subjects.map(s => s.subjectName)} />,
        },
        {
            id: 'your-possible-life', title: 'Your Possible Life', description: 'Explore real careers, ordinary working days, pay and routes — then save possibilities worth testing.', icon: Sunrise, needsProfile: true,
            curriculum: 'senior' as const,
            tag: 'Career Discovery', accentHex: '#2E6E8E', gridClass: 'md:col-span-3',
            iconBg: 'bg-sky-100 dark:bg-sky-900/30', iconColor: 'text-sky-700 dark:text-sky-300',
            accentBarColor: 'bg-sky-500', tagBg: 'bg-sky-100 dark:bg-sky-900/30', tagText: 'text-sky-700 dark:text-sky-400',
            hoverBorder: 'hover:border-sky-400/50 dark:hover:border-sky-500/40',
            component: subjectProfile ? <YourPossibleLife uid={user!.uid} profile={subjectProfile} /> : null,
        },
    ];

    const [activeFilter, setActiveFilter] = useState<'all' | 'understand' | 'practise' | 'plan' | 'track'>('all');

    const TOOL_CATEGORIES: Record<string, 'understand' | 'practise' | 'plan' | 'track'> = {
        'mark-bank': 'practise',
        'syllabus-xray': 'understand',
        'cao-simulator': 'understand',
        'future-finder': 'understand',
        'planner': 'plan',
        'war-room': 'plan',
        'comeback': 'plan',
        'points-passport': 'track',
        'journey': 'track',
        'exam-reps': 'plan',
        'college-compass': 'plan',
        'catch-up-lane': 'plan',
        'paper-trail': 'understand',
        'diagram-vault': 'understand',
        'answer-architect': 'understand',
        'definition-drill': 'understand',
        'coursework-companion': 'understand',
        'command-word-reflex': 'understand',
        'oral-trainer': 'understand',
        'examiners-chair': 'understand',
        'how-they-did-it': 'understand',
        'future-finder-revamped': 'understand',
        'your-possible-life': 'understand',
    };

    // Curriculum gating (Phase 4): JC users only see tools tagged 'both'
    // or 'junior'. Senior users see everything (incl. tools without a tag).
    // (curriculumLevel itself is now declared above the tools array.)
    // Workshop (WIP) tools — parked out of the main grid but still openable via
    // the sidebar Workshop page's deep-links (currentTool lookup is unfiltered).
    const WIP_TOOL_IDS = new Set(['diagram-vault', 'answer-architect', 'definition-drill', 'oral-trainer', 'examiners-chair', 'coursework-companion']);
    const curriculumVisibleTools = tools.filter(t => {
      // Old CAO Simulator URLs and module links remain valid, but the duplicate
      // tile is removed now that all of its capability lives in Points Passport.
      if (t.id === 'cao-simulator') return false;
      if (WIP_TOOL_IDS.has(t.id)) return false;
      const tag = t.curriculum ?? 'senior';
      const okCurriculum = tag === 'both' || tag === curriculumLevel;
      // Tools flagged `seniorYearsOnly` must ALSO be an active senior year
      // (TY/5th/6th) — this is what excludes graduated users, who still
      // resolve to the 'senior' curriculum level. JC users are already
      // excluded by okCurriculum above.
      const okYear = !(t as { seniorYearsOnly?: boolean }).seniorYearsOnly || isActiveSeniorYear(user?.yearGroup);
      return okCurriculum && okYear;
    });

    const filteredTools = activeFilter === 'all'
        ? curriculumVisibleTools
        : curriculumVisibleTools.filter(t => TOOL_CATEGORIES[t.id] === activeFilter);

    const currentTool = tools.find(t => t.id === activeTool);

  return (
    <div
      className="product-shell launchpad-shell min-h-screen bg-[var(--surface-canvas)] transition-colors duration-500 overflow-x-hidden relative flex flex-col items-center pb-36 md:pb-24"
      // Fixed header at top is ~80px tall (back button + eyebrow + title) + safe-area-inset-top.
      // The journey/war-room tools historically had a smaller header offset (pt-14)
      // which left content peeking out behind the bar. Use the same generous offset
      // for every tool so nothing slides under the fixed banner.
      style={{
        paddingTop: `calc(96px + var(--sat, 0px))`,
      }}
    >

      <header
        className="fixed top-0 left-0 right-0 z-[60] bg-[var(--surface-paper)] md:px-10 border-b border-[var(--outline-soft)]"
        style={{
          paddingTop: 'calc(16px + var(--sat, 0px))',
          paddingBottom: '16px',
          paddingLeft: 'calc(16px + var(--sal, 0px))',
          paddingRight: 'calc(16px + var(--sar, 0px))',
        }}
      >
        <div className="container mx-auto flex min-w-0 items-center justify-between gap-3">
          <div className="flex min-w-0 items-center gap-3 md:gap-8">
            <MotionButton whileHover={{ y: -1 }} whileTap={{ x: 1, y: 1 }} onClick={activeTool ? () => nav.goBack() : onBack} className="p-2.5 rounded-xl bg-[var(--surface-paper)] border-[1.5px] border-[var(--outline-strong)] shadow-[2px_2px_0_0_var(--outline-strong)] active:shadow-none transition-all focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[rgba(var(--accent),0.5)]">
              <ArrowLeft size={18} className="text-zinc-900 dark:text-white" />
            </MotionButton>
            <div className="hidden md:block h-10 w-px bg-[var(--outline-soft)]" />
            <div className="min-w-0">
              <p className="font-mono text-[9px] font-bold text-zinc-400 dark:text-zinc-500 uppercase tracking-[0.25em] mb-1">Explore</p>
              <h1 className="font-serif font-semibold text-lg md:text-2xl tracking-tight text-zinc-900 dark:text-white truncate">The Launchpad</h1>
            </div>
          </div>
          {/* Global rank, notifications and profile controls own the top-right.
              A second settings action here sat underneath that fixed cluster and
              appeared as a stray button. Subject editing remains available from
              the profile/settings flow. */}
          <div aria-hidden="true" />
        </div>
      </header>

      {/* Tools that lay out their own work surface. `max-w-4xl` gives 848px of
          usable width, which is a reading column, not a desk: Mark Bank puts a
          question and its marking scheme side by side and needs 1092px. Tools
          listed here also own their top spacing, so `pt-16` comes off. */}
      <main className={`flex-grow w-full relative z-10 ${WIDE_TOOLS.has(activeTool ?? '') ? 'max-w-[1140px]' : 'max-w-4xl'} ${activeTool === 'journey' || activeTool === 'war-room' || activeTool === 'college-compass' || WIDE_TOOLS.has(activeTool ?? '') ? 'px-6 pt-0' : 'px-6 pt-16'}`}>
         <AnimatePresence mode="wait">
            {!activeTool ? (
                <MotionDiv
                    key="tool-grid"
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    exit={{ opacity: 0 }}
                >
                    {/* Inline points panel — replaces the old PointsExplainer modal */}
                    <PointsPanel open={showPointsPanel} onHide={hidePointsPanel} />

                    {/* Filter pills + Points trigger — same row, opposite ends */}
                    <div className="mb-8 flex items-center justify-between gap-3 flex-wrap">
                        <div className="flex items-center gap-1 p-1 rounded-xl border border-[var(--outline-soft)] bg-[var(--surface-soft)] w-fit">
                            {(['all', 'understand', 'practise', 'plan', 'track'] as const).map(filter => (
                                <button
                                    key={filter}
                                    onClick={() => setActiveFilter(filter)}
                                    className={`px-4 py-2 rounded-lg text-sm transition-all ${
                                        activeFilter === filter
                                            ? 'bg-[var(--surface-paper)] text-[var(--ink-primary)] font-medium border border-[var(--outline-strong)]'
                                            : 'text-zinc-500 dark:text-zinc-400 hover:text-zinc-700 dark:hover:text-zinc-300'
                                    }`}
                                >
                                    {filter === 'all' ? 'All' : filter.charAt(0).toUpperCase() + filter.slice(1)}
                                </button>
                            ))}
                        </div>
                        <div className="flex items-center gap-1 p-1 rounded-xl border border-[var(--outline-soft)] bg-[var(--surface-soft)] w-fit">
                            <button
                                onClick={togglePointsPanel}
                                aria-label="How points work"
                                aria-expanded={showPointsPanel}
                                title="How points work"
                                className={`inline-flex items-center gap-2 px-4 py-2 rounded-lg text-sm transition-all ${
                                    showPointsPanel
                                        ? 'bg-[var(--surface-paper)] text-[var(--ink-primary)] font-medium border border-[var(--outline-strong)]'
                                        : 'text-zinc-500 dark:text-zinc-400 hover:text-zinc-700 dark:hover:text-zinc-300'
                                }`}
                            >
                                <span
                                    className="inline-flex items-center justify-center w-4 h-4 rounded-full shrink-0 text-[11px] font-semibold"
                                    style={{
                                        background: showPointsPanel ? 'rgba(0,0,0,0.06)' : 'rgba(0,0,0,0.05)',
                                        fontFamily: "'Source Serif 4', serif",
                                        lineHeight: 1,
                                    }}
                                    aria-hidden="true"
                                >
                                    ?
                                </span>
                                Points
                            </button>
                        </div>
                    </div>

                    {/* Empty state for JC users when no tools are curriculum-visible.
                        JC-visible tools now include the Spaced Repetition Timetable,
                        Comeback Engine, Subject Explorer,
                        Command-Word Reflex, How They Did It and Exploring Options.
                        This branch is now only reachable when the user filters by a
                        category that contains zero JC-visible tools — so the message
                        reflects a filter mismatch, not a roadmap gap. */}
                    {filteredTools.length === 0 && curriculumLevel === 'junior' && (
                      <div className="rounded-2xl p-10 text-center" style={{ backgroundColor: '#FDF8F0', border: '2px solid #1A1A1A' }}>
                        <p className="font-serif text-xl font-bold mb-2 text-[#1A1A1A]">No tools in this category for Junior Cycle yet.</p>
                        <p className="text-sm text-[#78716C] max-w-md mx-auto">
                          Try a different category, or hit "All" to see the tools we have ready for you — including Command-Word Reflex, the Spaced Repetition Timetable and the Comeback Engine.
                        </p>
                      </div>
                    )}

                    {/* Bento card grid */}
                    <div style={{ display: filteredTools.length === 0 ? 'none' : 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))', gap: '16px' }}>
                        {filteredTools.map((tool, i) => {
                            const disabled = (tool.needsProfile && !profileLoaded) || (tool.needsProfile && !subjectProfile);
                            const gcRecommended = gcRecommendations[tool.id];

                            return (
                                <MotionDiv
                                    key={tool.id}
                                    initial={{ opacity: 0, y: 16 }}
                                    animate={{ opacity: 1, y: 0 }}
                                    transition={{ duration: 0.3, delay: i * 0.04 }}
                                    onClick={disabled ? undefined : () => handleToolClick(tool.id, tool.needsProfile)}
                                    className={`flex flex-col rounded-2xl border-[1.5px] overflow-hidden transition-all ${
                                        disabled
                                            ? 'border-[var(--outline-soft)] cursor-not-allowed'
                                            : 'border-[var(--outline-strong)] hover:-translate-y-0.5 hover:shadow-[3px_3px_0_0_var(--outline-strong)] cursor-pointer'
                                    } bg-[var(--surface-paper)]`}
                                >
                                    <div className="p-6 flex-1 flex flex-col">
                                        {/* Painted blob + hand-drawn ink illustration. Disabled state
                                            falls back to the muted lock tile so locked tools still
                                            communicate gating without showing the bright illustration. */}
                                        <div className="mb-4">
                                            {disabled ? (
                                                <div
                                                    className="flex items-center justify-center"
                                                    style={{
                                                        width: 72,
                                                        height: 72,
                                                        borderRadius: 18,
                                                        background: '#E7E5E2',
                                                        opacity: 0.7,
                                                    }}
                                                >
                                                    <Lock size={20} className="text-zinc-500" />
                                                </div>
                                            ) : (
                                                <ToolIconBlob toolId={tool.id as ToolIconKey} size={72} />
                                            )}
                                        </div>

                                        {/* Category label */}
                                        <p className={`text-[10px] font-bold uppercase tracking-widest mb-1.5 ${
                                            disabled ? 'text-zinc-300 dark:text-zinc-600' : 'text-zinc-400 dark:text-zinc-500'
                                        }`}>
                                            {disabled ? 'Needs Profile' : tool.tag}
                                        </p>

                                        {/* Title */}
                                        <h3 className={`text-base font-semibold mb-1.5 ${
                                            disabled ? 'text-zinc-300 dark:text-zinc-600' : 'text-zinc-900 dark:text-white'
                                        }`}>
                                            {tool.title}
                                        </h3>

                                        {/* Description */}
                                        <p className={`text-xs leading-relaxed flex-1 ${
                                            disabled ? 'text-zinc-300 dark:text-zinc-600' : 'text-zinc-500 dark:text-zinc-400'
                                        }`}>
                                            {disabled ? 'Complete your Subject Profile to unlock.' : tool.description}
                                        </p>

                                        {/* GC recommendation badge if present */}
                                        {gcRecommended && !disabled && (
                                            <div className="mt-3 px-3 py-2 rounded-lg bg-indigo-50 dark:bg-indigo-900/20 border border-indigo-200/60 dark:border-indigo-800/40">
                                                <p className="text-[11px] font-semibold text-indigo-600 dark:text-indigo-400">
                                                    Recommended by {gcRecommended.fromName || 'your counsellor'}
                                                </p>
                                            </div>
                                        )}
                                    </div>

                                    {/* Bottom section with divider */}
                                    {!disabled && (
                                        <div className="px-6 py-3 border-t border-zinc-100 dark:border-zinc-800/60">
                                            <span className="text-xs font-medium text-zinc-400 dark:text-zinc-500">
                                                Launch tool
                                            </span>
                                        </div>
                                    )}
                                </MotionDiv>
                            );
                        })}
                    </div>
                </MotionDiv>
            ) : (
                <MotionDiv
                    key="active-tool"
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    exit={{ opacity: 0 }}
                >
                    {currentTool && TOOL_CHROME[currentTool.id]?.showHeader && (
                        <div className="mb-6">
                            <ToolHeader
                                themeColor={TOOL_CHROME[currentTool.id].themeColor}
                                eyebrow={TOOL_CHROME[currentTool.id].eyebrow}
                                title={currentTool.title}
                                subtitle={TOOL_CHROME[currentTool.id].subtitle}
                                iconBlob={<ToolIconBlob toolId={(currentTool.id === 'cao-simulator' ? 'points-passport' : currentTool.id) as ToolIconKey} size={108} />}
                            />
                        </div>
                    )}
                    <InnovationDataProvider uid={user?.uid} subjectProfile={subjectProfile}>
                        <ToolErrorBoundary
                            key={currentTool?.id}
                            toolName={currentTool?.title ?? 'this tool'}
                            onBack={() => nav.goBack()}
                        >
                            <Suspense fallback={<ToolLoadingFallback />}>
                                {currentTool?.component}
                            </Suspense>
                        </ToolErrorBoundary>
                    </InnovationDataProvider>
                </MotionDiv>
            )}
        </AnimatePresence>
      </main>

      {/* Subject Onboarding Modal */}
      <AnimatePresence>
        {showOnboarding && user && (
          <SubjectOnboarding
            user={user}
            existingProfile={subjectProfile || undefined}
            onComplete={handleOnboardingComplete}
            onClose={() => { setShowOnboarding(false); setPendingToolId(null); }}
          />
        )}
      </AnimatePresence>

      {/* Reflection Modal — kept for backwards compat but no longer triggered */}

      {/* Study Journal Modal */}
      <StudyJournalModal
        isOpen={showJournal}
        onClose={() => setShowJournal(false)}
        reflections={reflections}
      />


    </div>
  );
};
export default InnovationZone;
