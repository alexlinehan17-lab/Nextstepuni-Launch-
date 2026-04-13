
/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React, { useState, useEffect, useCallback, useRef, useMemo } from 'react';
import { useToast } from './Toast';
import { AnimatePresence } from 'framer-motion';
import { MotionButton, MotionDiv } from './Motion';
import {
    ArrowLeft, Zap, Clock,
    BookMarked,
    Lock, Compass, Target,
    Flame, Settings, CalendarDays, Calculator, GitBranch, Rocket,
    Map, ScanSearch
} from 'lucide-react';
import { doc, setDoc, getDoc, increment } from 'firebase/firestore';
import { db } from '../firebase';
import { type StudentSubjectProfile, type TimetableCompletions, type TimetableStreak, getBlockId, toDateKey } from './subjectData';
import { type SchoolEvent } from './gc/GCKeyEvents';
import { computeStreak, computeSubjectPriorities, allocateSessions, generateWeeklyTimetable, computeWeeksUntilExam } from './timetableAlgorithm';
import { type StudyReflection, type PointsData, type CosmeticUnlocks, type EarnedRest, type UserSettings } from '../types';
import SubjectOnboarding from './SubjectOnboarding';
import SpacedRepetitionTimetable from './SpacedRepetitionTimetable';
import WarRoom from './WarRoom';
import ComebackEngine from './ComebackEngine';
import CAOPointsSimulator from './CAOPointsSimulator';

import FutureFinder from './FutureFinder';
import SyllabusXRay from './SyllabusXRay';
import PointsPassport from './PointsPassport';
import { InnovationDataProvider } from '../contexts/InnovationDataContext';
import { useTopicMastery } from '../hooks/useTopicMastery';
import { getNotifications } from './gc/gcNotifications';
// ReflectionModal import removed — "Already Studied" flow gives 2 pts, no reflection
import StudyJournalModal from './StudyJournalModal';
import RewardShopModal from './RewardShopModal';
import AcademicJourneyGame, { type JourneyResult } from './AcademicJourneyGame';
import ToolErrorBoundary from './ToolErrorBoundary';
import { useNavigation } from '../contexts/NavigationContext';

interface InnovationZoneProps {
  onBack: () => void;
  onSelectModule?: (moduleId: string) => void;
  user?: { uid: string; school?: string; yearGroup?: '5th' | '6th' } | null;
  savedJourneyResult?: JourneyResult | null;
  onJourneyComplete?: (result: JourneyResult) => void;
  settings: UserSettings;
  updateSetting: <K extends keyof UserSettings>(key: K, value: UserSettings[K]) => void;
  onCosmeticUnlocksChange?: (unlocks: CosmeticUnlocks) => void;
  onStudyNow?: (block: { subject: string; sessionType: 'new-learning' | 'practice' | 'revision'; durationMinutes: number; dateKey: string; blockId: string }) => void;
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

// ─── InnovationZone ──────────────────────────────────────────────────────────

const InnovationZone: React.FC<InnovationZoneProps> = ({ onBack, onSelectModule, user, savedJourneyResult, onJourneyComplete, settings, updateSetting, onCosmeticUnlocksChange, onStudyNow }) => {
    const { showToast } = useToast();
    const nav = useNavigation();
    const activeTool = nav.state.activeTool;
    const setActiveTool = nav.setActiveTool;
    const [subjectProfile, setSubjectProfile] = useState<StudentSubjectProfile | null>(null);
    const [showOnboarding, setShowOnboarding] = useState(false);
    const [profileLoaded, setProfileLoaded] = useState(false);
    const [pendingToolId, setPendingToolId] = useState<string | null>(null);
    const [timetableCompletions, setTimetableCompletions] = useState<TimetableCompletions>({});
    const [timetableStreak, setTimetableStreak] = useState<TimetableStreak>({ currentStreak: 0, lastActiveDate: '', longestStreak: 0 });
    const [reflections, setReflections] = useState<StudyReflection[]>([]);

    // Topic mastery for skippableBlocks computation (shared context loads separately for tools)
    const { mastery: topicMasteryForPriorities } = useTopicMastery(user?.uid);
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
    const pointsDataRef = useRef(pointsData);
    pointsDataRef.current = pointsData;
    const cosmeticUnlocksRef = useRef(cosmeticUnlocks);
    cosmeticUnlocksRef.current = cosmeticUnlocks;
    const earnedRestRef = useRef(earnedRest);
    earnedRestRef.current = earnedRest;
    const onCosmeticUnlocksChangeRef = useRef(onCosmeticUnlocksChange);
    onCosmeticUnlocksChangeRef.current = onCosmeticUnlocksChange;
    const [showRewardShop, setShowRewardShop] = useState(false);
    const [showJournal, setShowJournal] = useState(false);
    const [showPointsExplainer, setShowPointsExplainer] = useState(() => {
        try { return !localStorage.getItem('nextstep-points-explainer-v2'); } catch (err) { console.error('Failed to read points explainer state:', err); return true; }
    });

    const dismissPointsExplainer = useCallback(() => {
        setShowPointsExplainer(false);
        try { localStorage.setItem('nextstep-points-explainer-v2', '1'); } catch (err) { console.error('Failed to save points explainer state:', err); }
    }, []);

    // Load subject profile from Firebase
    useEffect(() => {
        if (!user?.uid) { setProfileLoaded(true); return; }
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
        setSubjectProfile(profile);
        setShowOnboarding(false);
        if (pendingToolId) {
            setActiveTool(pendingToolId);
            setPendingToolId(null);
        }
        if (user?.uid) {
            try {
                await setDoc(doc(db, 'progress', user.uid), { subjectProfile: profile }, { merge: true });
            } catch (err) {
                console.error('Failed to save subject profile:', err);
                showToast('Couldn\'t save — check your connection', 'error');
            }
        }
    }, [user?.uid, pendingToolId, setActiveTool]);

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
            if (dayArr.length === 0) {
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
                setDoc(doc(db, 'progress', user.uid), {
                    timetableCompletions: updated,
                    timetableStreak: newStreak,
                    ...extraFirestoreData,
                }, { merge: true }).catch(err => { console.error('Failed to save completions:', err); showToast('Couldn\'t save — check your connection', 'error'); });
            }

            return updated;
        });
    }, [subjectProfile?.restDays, timetableStreak.longestStreak, user?.uid, earnedRest.restDayPasses]);

    const handleToggleCompletion = useCallback(async (dateKey: string, blockId: string, completed: boolean) => {
        if (completed) {
            // "Already Studied" flow: 2 pts flat, no reflection
            const ALREADY_STUDIED_POINTS = 2;
            setPointsData(prev => ({
                ...prev,
                totalEarned: prev.totalEarned + ALREADY_STUDIED_POINTS,
            }));
            executeToggle(dateKey, blockId, true, {
                'pointsData.totalEarned': increment(ALREADY_STUDIED_POINTS),
            });
        } else {
            executeToggle(dateKey, blockId, false);
        }
    }, [executeToggle, pointsData]);

    const handleSpendPoints = useCallback((type: 'skip-session' | 'rest-day-pass' | 'unlock-avatar' | 'unlock-theme' | 'unlock-card-style', detail?: string) => {
        const costs: Record<string, number> = {
            'skip-session': 20,
            'rest-day-pass': 60,
            'unlock-avatar': 50,
            'unlock-theme': 40,
            'unlock-card-style': 40,
        };
        const cost = costs[type];

        // Read latest state from refs to avoid stale closures
        const currentPoints = pointsDataRef.current;
        const currentCosmeticUnlocks = cosmeticUnlocksRef.current;
        const currentEarnedRest = earnedRestRef.current;

        const balance = currentPoints.totalEarned - currentPoints.totalSpent;
        if (balance < cost) return;

        const updatedPointsData: PointsData = {
            totalEarned: currentPoints.totalEarned,
            totalSpent: currentPoints.totalSpent + cost,
        };
        setPointsData(updatedPointsData);

        const todayKey = toDateKey(new Date());
        let updatedEarnedRest = currentEarnedRest;
        let updatedCosmeticUnlocks = currentCosmeticUnlocks;

        if (type === 'skip-session' && detail) {
            updatedEarnedRest = {
                ...currentEarnedRest,
                skippedSessions: [...currentEarnedRest.skippedSessions, detail],
            };
            setEarnedRest(updatedEarnedRest);
        } else if (type === 'rest-day-pass') {
            updatedEarnedRest = {
                ...currentEarnedRest,
                restDayPasses: [...currentEarnedRest.restDayPasses, todayKey],
            };
            setEarnedRest(updatedEarnedRest);
        } else if (type === 'unlock-avatar' && detail) {
            updatedCosmeticUnlocks = {
                ...currentCosmeticUnlocks,
                avatarSeeds: [...(currentCosmeticUnlocks.avatarSeeds || []), detail],
            };
            setCosmeticUnlocks(updatedCosmeticUnlocks);
        } else if (type === 'unlock-theme' && detail) {
            updatedCosmeticUnlocks = {
                ...currentCosmeticUnlocks,
                themeColors: [...(currentCosmeticUnlocks.themeColors || []), detail],
            };
            setCosmeticUnlocks(updatedCosmeticUnlocks);
        } else if (type === 'unlock-card-style' && detail) {
            updatedCosmeticUnlocks = {
                ...currentCosmeticUnlocks,
                cardStyles: [...(currentCosmeticUnlocks.cardStyles || []), detail],
            };
            setCosmeticUnlocks(updatedCosmeticUnlocks);
        }

        // Notify parent of cosmetic unlock changes so App.tsx state stays in sync
        if (updatedCosmeticUnlocks !== currentCosmeticUnlocks) {
            onCosmeticUnlocksChangeRef.current?.(updatedCosmeticUnlocks);
        }

        if (user?.uid) {
            setDoc(doc(db, 'progress', user.uid), {
                'pointsData.totalSpent': increment(cost),
                earnedRest: updatedEarnedRest,
                cosmeticUnlocks: updatedCosmeticUnlocks,
            }, { merge: true }).catch(err => {
                console.error('Failed to save purchase:', err);
                showToast('Purchase couldn\'t be saved — check your connection', 'error');
                // Roll back to latest ref values (may have changed since write started)
                setPointsData(currentPoints);
                setEarnedRest(currentEarnedRest);
                setCosmeticUnlocks(currentCosmeticUnlocks);
                onCosmeticUnlocksChangeRef.current?.(currentCosmeticUnlocks);
            });
        }
    }, [user?.uid]);

    const handleToolClick = useCallback((toolId: string, needsProfile: boolean) => {
        if (needsProfile && !profileLoaded) return;
        if (needsProfile && !subjectProfile) {
            setPendingToolId(toolId);
            setShowOnboarding(true);
            return;
        }
        setActiveTool(toolId);
    }, [subjectProfile, profileLoaded, setActiveTool]);

    const skippableBlocks = useMemo(() => {
        if (!subjectProfile) return [];
        const today = new Date();
        const todayKey = toDateKey(today);
        const jsDay = today.getDay();
        const todayDayIndex = jsDay === 0 ? 6 : jsDay - 1;

        const priorities = computeSubjectPriorities(subjectProfile.subjects, topicMasteryForPriorities);
        const weeksUntilExam = computeWeeksUntilExam(subjectProfile.examStartDate);
        const allocations = allocateSessions(priorities, weeksUntilExam);
        const restDaysArray = subjectProfile.restDays || [];
        const timetable = generateWeeklyTimetable(allocations, weeksUntilExam, 0, restDaysArray, subjectProfile.defaultBlockDuration ?? 45);
        const todayBlocks = timetable[todayDayIndex]?.blocks ?? [];

        const completedIds = timetableCompletions[todayKey] ?? [];
        const skippedSet = new Set(earnedRest.skippedSessions);

        return todayBlocks
            .map((block, bi) => {
                const blockId = getBlockId(block, bi);
                const fullId = `${todayKey}|${blockId}`;
                const isCompleted = completedIds.includes(blockId);
                const isSkipped = skippedSet.has(fullId);
                if (isCompleted || isSkipped) return null;
                return { blockId, fullId, subjectName: block.subjectName, sessionType: block.sessionType };
            })
            .filter((b): b is { blockId: string; fullId: string; subjectName: string; sessionType: string } => b !== null);
    }, [subjectProfile, timetableCompletions, earnedRest.skippedSessions]);

    const tools = [
        {
            id: 'journey', title: 'Academic Journey Simulator', description: 'Navigate the choices of your final school year.', icon: GitBranch, needsProfile: false,
            tag: 'Simulator', accentHex: '#f59e0b', gridClass: 'md:col-span-3',
            iconBg: 'bg-amber-100 dark:bg-amber-900/30', iconColor: 'text-amber-600 dark:text-amber-400',
            accentBarColor: 'bg-amber-500', tagBg: 'bg-amber-100 dark:bg-amber-900/30', tagText: 'text-amber-700 dark:text-amber-400',
            hoverBorder: 'hover:border-amber-400/50 dark:hover:border-amber-500/40',
            component: <AcademicJourneyGame onSelectModule={onSelectModule} user={user} savedJourneyResult={savedJourneyResult} onJourneyComplete={onJourneyComplete} />,
        },
        {
            id: 'cao-simulator', title: 'CAO Points Simulator', description: 'Explore how grade changes affect your CAO points.', icon: Calculator, needsProfile: true,
            tag: 'Simulator', accentHex: '#64748b', gridClass: 'md:col-span-3',
            iconBg: 'bg-slate-100 dark:bg-slate-800/40', iconColor: 'text-slate-600 dark:text-slate-300',
            accentBarColor: 'bg-slate-500', tagBg: 'bg-slate-100 dark:bg-slate-800/40', tagText: 'text-slate-600 dark:text-slate-300',
            hoverBorder: 'hover:border-slate-400/50 dark:hover:border-slate-500/40',
            component: subjectProfile ? <CAOPointsSimulator profile={subjectProfile} uid={user?.uid} onOpenSettings={() => setShowOnboarding(true)} /> : null,
        },
        {
            id: 'planner', title: 'Spaced Repetition Timetable', description: 'A data-driven study planner powered by your subject goals.', icon: CalendarDays, needsProfile: true,
            tag: 'Planner', accentHex: '#6366f1', gridClass: 'md:col-span-2',
            iconBg: 'bg-indigo-100 dark:bg-indigo-900/30', iconColor: 'text-indigo-600 dark:text-indigo-400',
            accentBarColor: 'bg-indigo-500', tagBg: 'bg-indigo-100 dark:bg-indigo-900/30', tagText: 'text-indigo-700 dark:text-indigo-400',
            hoverBorder: 'hover:border-indigo-400/50 dark:hover:border-indigo-500/40',
            component: subjectProfile ? <SpacedRepetitionTimetable profile={subjectProfile} uid={user?.uid} onOpenSettings={() => setShowOnboarding(true)} completions={timetableCompletions} streak={timetableStreak} onToggleCompletion={handleToggleCompletion} points={pointsData.totalEarned - pointsData.totalSpent} onOpenShop={() => setShowRewardShop(true)} onOpenJournal={() => setShowJournal(true)} skippedSessions={earnedRest.skippedSessions} onStudyNow={onStudyNow} schoolEvents={schoolEvents} onBlockDurationChange={async (_s, _t, newDuration) => { const updated = { ...subjectProfile, defaultBlockDuration: newDuration }; setSubjectProfile(updated); if (user?.uid) { try { await setDoc(doc(db, 'progress', user.uid), { subjectProfile: updated }, { merge: true }); } catch (err) { console.error('Failed to save block duration:', err); showToast('Couldn\'t save — check your connection', 'error'); } } }} onRestDaysChange={async (days) => { const updated = { ...subjectProfile, restDays: days }; setSubjectProfile(updated); if (user?.uid) { try { await setDoc(doc(db, 'progress', user.uid), { subjectProfile: updated }, { merge: true }); } catch (err) { console.error('Failed to save rest days:', err); showToast('Couldn\'t save — check your connection', 'error'); } } }} /> : null,
        },
        {
            id: 'war-room', title: 'War Room', description: 'Your strategic study command centre.', icon: Target, needsProfile: true,
            tag: 'Strategy', accentHex: '#dc2626', gridClass: 'md:col-span-2',
            iconBg: 'bg-red-100 dark:bg-red-900/30', iconColor: 'text-red-600 dark:text-red-400',
            accentBarColor: 'bg-red-500', tagBg: 'bg-red-100 dark:bg-red-900/30', tagText: 'text-red-700 dark:text-red-400',
            hoverBorder: 'hover:border-red-400/50 dark:hover:border-red-500/40',
            component: subjectProfile ? <WarRoom uid={user!.uid} profile={subjectProfile} timetableCompletions={timetableCompletions} /> : null,
        },
        {
            id: 'comeback', title: 'Comeback Engine', description: 'Find your quickest wins and build a comeback plan.', icon: Rocket, needsProfile: true,
            tag: 'Comeback', accentHex: '#f97316', gridClass: 'md:col-span-2',
            iconBg: 'bg-orange-100 dark:bg-orange-900/30', iconColor: 'text-orange-600 dark:text-orange-400',
            accentBarColor: 'bg-orange-500', tagBg: 'bg-orange-100 dark:bg-orange-900/30', tagText: 'text-orange-700 dark:text-orange-400',
            hoverBorder: 'hover:border-orange-400/50 dark:hover:border-orange-500/40',
            component: subjectProfile ? <ComebackEngine uid={user!.uid} profile={subjectProfile} /> : null,
        },
        {
            id: 'future-finder', title: 'Future Finder', description: 'Discover college courses that fit who you are.', icon: Compass, needsProfile: true,
            tag: 'Career Discovery', accentHex: '#6366f1', gridClass: 'md:col-span-2',
            iconBg: 'bg-indigo-100 dark:bg-indigo-900/30', iconColor: 'text-indigo-600 dark:text-indigo-400',
            accentBarColor: 'bg-indigo-500', tagBg: 'bg-indigo-100 dark:bg-indigo-900/30', tagText: 'text-indigo-700 dark:text-indigo-400',
            hoverBorder: 'hover:border-indigo-400/50 dark:hover:border-indigo-500/40',
            component: subjectProfile ? <FutureFinder uid={user!.uid} profile={subjectProfile} /> : null,
        },
        {
            id: 'syllabus-xray', title: 'Syllabus X-Ray', description: 'See where the marks are hiding in your exams.', icon: ScanSearch, needsProfile: false,
            tag: 'Exam Intel', accentHex: '#e11d48', gridClass: 'md:col-span-2',
            iconBg: 'bg-rose-100 dark:bg-rose-900/30', iconColor: 'text-rose-600 dark:text-rose-400',
            accentBarColor: 'bg-rose-500', tagBg: 'bg-rose-100 dark:bg-rose-900/30', tagText: 'text-rose-700 dark:text-rose-400',
            hoverBorder: 'hover:border-rose-400/50 dark:hover:border-rose-500/40',
            component: <SyllabusXRay studentSubjects={subjectProfile?.subjects.map(s => s.subjectName)} uid={user?.uid} />,
        },
        {
            id: 'points-passport', title: 'Points Passport', description: 'Mock trends & grade bargains at a glance.', icon: Map, needsProfile: true,
            tag: 'Tracker', accentHex: '#0ea5e9', gridClass: 'md:col-span-2',
            iconBg: 'bg-sky-100 dark:bg-sky-900/30', iconColor: 'text-sky-600 dark:text-sky-400',
            accentBarColor: 'bg-sky-500', tagBg: 'bg-sky-100 dark:bg-sky-900/30', tagText: 'text-sky-700 dark:text-sky-400',
            hoverBorder: 'hover:border-sky-400/50 dark:hover:border-sky-500/40',
            component: subjectProfile && user ? <PointsPassport uid={user.uid} profile={subjectProfile} /> : null,
        },
    ];

    const [activeFilter, setActiveFilter] = useState<'all' | 'understand' | 'plan' | 'track'>('all');

    const TOOL_CATEGORIES: Record<string, 'understand' | 'plan' | 'track'> = {
        'syllabus-xray': 'understand',
        'cao-simulator': 'understand',
        'future-finder': 'understand',
        'planner': 'plan',
        'war-room': 'plan',
        'comeback': 'plan',
        'points-passport': 'track',
        'journey': 'track',
    };

    const filteredTools = activeFilter === 'all'
        ? tools
        : tools.filter(t => TOOL_CATEGORIES[t.id] === activeFilter);

    const currentTool = tools.find(t => t.id === activeTool);

  return (
    <div className={`min-h-screen bg-zinc-50 dark:bg-zinc-950 transition-colors duration-500 overflow-x-hidden relative flex flex-col items-center pb-36 md:pb-24 ${activeTool === 'journey' || activeTool === 'war-room' ? 'pt-14 md:pt-16' : 'pt-24 md:pt-32'}`}>

      <header className={`fixed top-0 left-0 right-0 z-[60] bg-zinc-50 dark:bg-zinc-950 px-4 py-4 md:px-10 md:py-6 ${activeTool === 'journey' || activeTool === 'war-room' ? '' : 'border-b border-zinc-200 dark:border-zinc-800'}`} style={{ paddingTop: 'var(--sat, 0px)' }}>
        <div className="container mx-auto flex items-center justify-between">
          <div className="flex items-center gap-4 md:gap-8">
            <MotionButton whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }} onClick={activeTool ? () => nav.goBack() : onBack} className="p-2.5 rounded-xl bg-white dark:bg-zinc-900 border border-zinc-200 dark:border-zinc-800 transition-colors hover:bg-zinc-100 dark:hover:bg-zinc-800 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[rgba(var(--accent),0.5)]">
              <ArrowLeft size={18} className="text-zinc-900 dark:text-white" />
            </MotionButton>
            <div className="hidden md:block h-10 w-px bg-zinc-200 dark:bg-zinc-800" />
            <div>
              <p className="font-mono text-[9px] font-bold text-zinc-400 dark:text-zinc-500 uppercase tracking-[0.25em] mb-1">Explore</p>
              <h1 className="font-serif font-semibold text-lg md:text-2xl tracking-tight text-zinc-900 dark:text-white truncate">The Innovation Zone</h1>
            </div>
          </div>
          <div className="flex items-center gap-3">
            {subjectProfile && (
              <button
                onClick={() => setShowOnboarding(true)}
                className="p-2.5 rounded-lg bg-white dark:bg-zinc-900 border border-zinc-200 dark:border-zinc-800 transition-colors hover:bg-zinc-100 dark:hover:bg-zinc-800"
                title="Edit subjects"
              >
                <Settings size={16} className="text-zinc-500 dark:text-zinc-400" />
              </button>
            )}
          </div>
        </div>
      </header>

      <main className={`flex-grow w-full max-w-4xl relative z-10 ${activeTool === 'journey' || activeTool === 'war-room' ? 'px-6 pt-0' : 'px-6 pt-16'}`}>
         <AnimatePresence mode="wait">
            {!activeTool ? (
                <MotionDiv
                    key="tool-grid"
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    exit={{ opacity: 0 }}
                >
                    {/* Filter pills */}
                    <div className="mb-8">
                        <div className="flex items-center gap-1 p-1 rounded-xl bg-zinc-100 dark:bg-zinc-800/50 w-fit">
                            {(['all', 'understand', 'plan', 'track'] as const).map(filter => (
                                <button
                                    key={filter}
                                    onClick={() => setActiveFilter(filter)}
                                    className={`px-4 py-2 rounded-lg text-sm transition-all ${
                                        activeFilter === filter
                                            ? 'bg-white dark:bg-zinc-800 text-zinc-900 dark:text-white font-medium shadow-sm'
                                            : 'text-zinc-500 dark:text-zinc-400 hover:text-zinc-700 dark:hover:text-zinc-300'
                                    }`}
                                >
                                    {filter === 'all' ? 'All' : filter.charAt(0).toUpperCase() + filter.slice(1)}
                                </button>
                            ))}
                        </div>
                    </div>

                    {/* Bento card grid */}
                    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))', gap: '16px' }}>
                        {filteredTools.map((tool, i) => {
                            const Icon = tool.icon;
                            const disabled = (tool.needsProfile && !profileLoaded) || (tool.needsProfile && !subjectProfile);
                            const gcRecommended = gcRecommendations[tool.id];

                            return (
                                <MotionDiv
                                    key={tool.id}
                                    initial={{ opacity: 0, y: 16 }}
                                    animate={{ opacity: 1, y: 0 }}
                                    transition={{ duration: 0.3, delay: i * 0.04 }}
                                    onClick={disabled ? undefined : () => handleToolClick(tool.id, tool.needsProfile)}
                                    className={`flex flex-col rounded-xl border overflow-hidden transition-all ${
                                        disabled
                                            ? 'border-zinc-200/60 dark:border-zinc-800/40 cursor-not-allowed'
                                            : 'border-zinc-200/60 dark:border-zinc-800/40 hover:border-zinc-300 dark:hover:border-zinc-700 hover:shadow-md cursor-pointer'
                                    } bg-white dark:bg-zinc-900`}
                                >
                                    <div className="p-6 flex-1 flex flex-col">
                                        {/* Icon in colored circle */}
                                        <div className={`w-10 h-10 rounded-full flex items-center justify-center mb-4 ${
                                            disabled ? 'bg-zinc-100 dark:bg-zinc-800' : tool.iconBg
                                        }`}>
                                            {disabled
                                                ? <Lock size={18} className="text-zinc-400 dark:text-zinc-600" />
                                                : <Icon size={18} className={tool.iconColor} />
                                            }
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
                    <InnovationDataProvider uid={user?.uid} subjectProfile={subjectProfile}>
                        <ToolErrorBoundary
                            key={currentTool?.id}
                            toolName={currentTool?.title ?? 'this tool'}
                            onBack={() => nav.goBack()}
                        >
                            {currentTool?.component}
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

      {/* Reward Shop Modal */}
      <RewardShopModal
        isOpen={showRewardShop}
        onClose={() => setShowRewardShop(false)}
        pointsBalance={pointsData.totalEarned - pointsData.totalSpent}
        cosmeticUnlocks={cosmeticUnlocks}
        earnedRest={earnedRest}
        onSpend={handleSpendPoints}
        skippableBlocks={skippableBlocks}
        settings={settings}
        updateSetting={updateSetting}
      />

      {/* Points Explainer (first visit) */}
      <AnimatePresence>
        {showPointsExplainer && (
          <MotionDiv
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-[100] p-4"
            onClick={dismissPointsExplainer}
          >
            <MotionDiv
              initial={{ scale: 0.92, opacity: 0, y: 20 }}
              animate={{ scale: 1, opacity: 1, y: 0 }}
              exit={{ scale: 0.92, opacity: 0, y: 20 }}
              transition={{ duration: 0.35, ease: [0.16, 1, 0.3, 1] }}
              className="bg-white dark:bg-zinc-900 rounded-2xl max-w-sm w-full shadow-2xl border border-zinc-200 dark:border-zinc-800 overflow-hidden"
              onClick={(e: React.MouseEvent) => e.stopPropagation()}
            >
              <div className="h-1.5 bg-gradient-to-r from-amber-400 via-[var(--accent-hex)] to-purple-500" />

              <div className="p-6">
                <div className="flex items-center gap-3 mb-5">
                  <div className="w-10 h-10 rounded-xl bg-amber-100 dark:bg-amber-900/30 flex items-center justify-center">
                    <Zap size={20} className="text-amber-500" />
                  </div>
                  <div>
                    <h3 className="font-serif font-semibold text-lg text-zinc-900 dark:text-white">How Points Work</h3>
                    <p className="text-xs text-zinc-400 dark:text-zinc-500">Earn & spend in the Innovation Zone</p>
                  </div>
                </div>

                <div className="space-y-2.5 mb-4">
                  <div className="flex items-start gap-3 p-3 rounded-xl bg-zinc-50 dark:bg-white/[0.04]">
                    <div className="w-8 h-8 rounded-lg bg-teal-100 dark:bg-teal-900/30 flex items-center justify-center shrink-0 mt-0.5">
                      <Clock size={14} className="text-teal-600 dark:text-teal-400" />
                    </div>
                    <div>
                      <p className="text-sm font-medium text-zinc-800 dark:text-zinc-200">Study Sessions</p>
                      <p className="text-xs text-zinc-500 dark:text-zinc-400">10 pts per completed timetable session</p>
                    </div>
                  </div>
                  <div className="flex items-start gap-3 p-3 rounded-xl bg-zinc-50 dark:bg-white/[0.04]">
                    <div className="w-8 h-8 rounded-lg bg-purple-100 dark:bg-purple-900/30 flex items-center justify-center shrink-0 mt-0.5">
                      <BookMarked size={14} className="text-purple-600 dark:text-purple-400" />
                    </div>
                    <div>
                      <p className="text-sm font-medium text-zinc-800 dark:text-zinc-200">Reflections</p>
                      <p className="text-xs text-zinc-500 dark:text-zinc-400">Bonus points for thoughtful study reflections</p>
                    </div>
                  </div>
                </div>

                {/* Streak Explainer */}
                <div className="mb-4 p-3 rounded-xl bg-gradient-to-r from-amber-50 to-orange-50 dark:from-amber-950/20 dark:to-orange-950/20 border border-amber-200/50 dark:border-amber-800/30">
                  <div className="flex items-center gap-2 mb-2">
                    <Flame size={14} className="text-amber-500" />
                    <p className="text-sm font-semibold text-zinc-800 dark:text-zinc-200">Streak Multiplier</p>
                  </div>
                  <p className="text-xs text-zinc-500 dark:text-zinc-400 mb-2">Complete your timetable sessions on consecutive days to build a streak and multiply your points.</p>
                  <div className="grid grid-cols-3 gap-1.5">
                    <div className="text-center p-1.5 rounded-lg bg-white/60 dark:bg-white/[0.04]">
                      <p className="text-[10px] font-bold text-amber-600 dark:text-amber-400">3+ days</p>
                      <p className="text-[10px] text-zinc-500 dark:text-zinc-400">1.5x pts</p>
                    </div>
                    <div className="text-center p-1.5 rounded-lg bg-white/60 dark:bg-white/[0.04]">
                      <p className="text-[10px] font-bold text-orange-600 dark:text-orange-400">7+ days</p>
                      <p className="text-[10px] text-zinc-500 dark:text-zinc-400">2x pts</p>
                    </div>
                    <div className="text-center p-1.5 rounded-lg bg-white/60 dark:bg-white/[0.04]">
                      <p className="text-[10px] font-bold text-red-600 dark:text-red-400">14+ days</p>
                      <p className="text-[10px] text-zinc-500 dark:text-zinc-400">2.5x pts</p>
                    </div>
                  </div>
                </div>

                <p className="text-xs text-zinc-400 dark:text-zinc-500 text-center mb-4">
                  Spend points in the <span className="font-semibold text-zinc-600 dark:text-zinc-300">Reward Shop</span> on avatars, themes & card styles.
                </p>

                <button
                  onClick={dismissPointsExplainer}
                  className="w-full py-2.5 rounded-xl bg-[var(--accent-hex)] hover:bg-[var(--accent-dark-hex)] text-white font-semibold text-sm transition-colors"
                >
                  Got it!
                </button>
              </div>
            </MotionDiv>
          </MotionDiv>
        )}
      </AnimatePresence>
    </div>
  );
};
export default InnovationZone;
