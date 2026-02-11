
/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React, { useState, useEffect, useCallback, useRef, useMemo } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
    ArrowLeft, ArrowRight, Lightbulb, Zap, Clock, Shield, Wrench, RotateCcw,
    TrendingUp, Users, BookOpen, GitBranch, ChevronDown, ChevronUp, BookMarked,
    Lock, MapPin, Sparkles, AlertTriangle, MessageCircle, BookOpenCheck,
    ClipboardCheck, Home, School, Library, Coffee, Wifi, ArrowUp, ArrowDown,
    Trophy, Compass, Brain, HandHelping, Target, ArrowUpRight, Award, Megaphone,
    Flame, Scale, GraduationCap, Settings, CalendarDays, Calculator
} from 'lucide-react';
import { doc, setDoc, getDoc } from 'firebase/firestore';
import { db } from '../firebase';
import { type StudentSubjectProfile, type TimetableCompletions, type TimetableStreak, type StudyBlock, getBlockId, toDateKey } from './subjectData';
import { computeStreak, computeSubjectPriorities, allocateSessions, generateWeeklyTimetable, computeWeeksUntilExam } from './timetableAlgorithm';
import { type StudyReflection, type PointsData, type CosmeticUnlocks, type EarnedRest } from '../types';
import SubjectOnboarding from './SubjectOnboarding';
import SpacedRepetitionTimetable from './SpacedRepetitionTimetable';
import CAOPointsSimulator from './CAOPointsSimulator';
import DeepFocusTimer from './DeepFocusTimer';
import ReflectionModal from './ReflectionModal';
import StudyJournalModal from './StudyJournalModal';
import RewardShopModal from './RewardShopModal';
import {
    type GameState, type Choice, type Scene, type HistoryItem, type StatKey, type Phase,
    type Mood, type Location,
    STORY_DATA, ROUTE_RESOLVERS, INITIAL_GAME_STATE, PHASE_METADATA,
    ARCHETYPES, STAT_TO_MODULES, STAT_LABELS, STAT_COLORS, STAT_BG_COLORS,
    WEAKEST_STAT_INSIGHTS,
    getStatGrade, getKeyTurningPoints, getWeakestStat,
} from './journeySimulatorData';

const MotionDiv = motion.div as any;
const MotionButton = motion.button as any;
const MotionSpan = motion.span as any;
const MotionCircle = motion.circle as any;

interface JourneyResult {
  endingId: string;
  finalStats?: GameState;
}

interface InnovationZoneProps {
  onBack: () => void;
  onSelectModule?: (moduleId: string) => void;
  user?: { uid: string } | null;
  autoOpenJourney?: boolean;
  savedJourneyResult?: JourneyResult | null;
  onJourneyComplete?: (result: JourneyResult) => void;
}

const STAT_ICONS: Record<StatKey, React.ElementType> = {
    energy: Zap,
    academicCap: TrendingUp,
    socialSupport: Users,
    systemSavvy: BookOpen,
    resilience: Shield,
};

// ─── Mood & Location Maps (literal Tailwind strings for CDN) ─────────────────

const MOOD_CONFIG: Record<Mood, { icon: React.ElementType; bg: string; border: string; text: string }> = {
    opportunity: { icon: Sparkles, bg: 'bg-amber-100 dark:bg-amber-900/30', border: 'border-amber-200 dark:border-amber-700/30', text: 'text-amber-600 dark:text-amber-400' },
    crisis: { icon: AlertTriangle, bg: 'bg-rose-100 dark:bg-rose-900/30', border: 'border-rose-200 dark:border-rose-700/30', text: 'text-rose-600 dark:text-rose-400' },
    social: { icon: MessageCircle, bg: 'bg-emerald-100 dark:bg-emerald-900/30', border: 'border-emerald-200 dark:border-emerald-700/30', text: 'text-emerald-600 dark:text-emerald-400' },
    study: { icon: BookOpenCheck, bg: 'bg-blue-100 dark:bg-blue-900/30', border: 'border-blue-200 dark:border-blue-700/30', text: 'text-blue-600 dark:text-blue-400' },
    exam: { icon: ClipboardCheck, bg: 'bg-purple-100 dark:bg-purple-900/30', border: 'border-purple-200 dark:border-purple-700/30', text: 'text-purple-600 dark:text-purple-400' },
    reflection: { icon: Coffee, bg: 'bg-zinc-100 dark:bg-zinc-800/50', border: 'border-zinc-200 dark:border-zinc-700/30', text: 'text-zinc-600 dark:text-zinc-400' },
    triumph: { icon: Trophy, bg: 'bg-yellow-100 dark:bg-yellow-900/30', border: 'border-yellow-200 dark:border-yellow-700/30', text: 'text-yellow-600 dark:text-yellow-400' },
};

const LOCATION_CONFIG: Record<Location, { icon: React.ElementType; label: string }> = {
    school: { icon: School, label: 'School' },
    home: { icon: Home, label: 'Home' },
    'exam-hall': { icon: ClipboardCheck, label: 'Exam Hall' },
    library: { icon: Library, label: 'Library' },
    social: { icon: Users, label: 'Social' },
    work: { icon: Coffee, label: 'Work' },
    online: { icon: Wifi, label: 'Online' },
};

// ─── Archetype Icon Map ─────────────────────────────────────────────────────

const ARCHETYPE_ICONS: Record<string, React.ElementType> = {
    'compass': Compass,
    'brain': Brain,
    'hand-helping': HandHelping,
    'target': Target,
    'arrow-up-right': ArrowUpRight,
    'rotate-ccw': RotateCcw,
    'award': Award,
    'megaphone': Megaphone,
    'flame': Flame,
    'scale': Scale,
};

// ─── Phase Timeline Months ───────────────────────────────────────────────────

const PHASE_MONTHS: Record<Phase, string[]> = {
    'Foundation': ['Sep', 'Oct', 'Nov', 'Dec'],
    'Pressure Cooker': ['Jan', 'Feb', 'Mar'],
    'Final Stretch': ['Apr', 'May', 'Jun'],
};

const MONTH_TO_INDEX: Record<string, number> = {
    'September': 0, 'October': 1, 'November': 2, 'December': 3,
    'January': 4, 'February': 5, 'March': 6,
    'April': 7, 'May': 8, 'June': 9, 'July': 10, 'August': 11,
};

// ─── Phase Colors (literal strings for Tailwind CDN) ─────────────────────────

const PHASE_COLORS: Record<Phase, { dot: string; line: string; label: string; labelBg: string; fill: string }> = {
    'Foundation': { dot: 'bg-blue-500', line: 'bg-blue-200 dark:bg-blue-800', label: 'text-blue-700 dark:text-blue-300', labelBg: 'bg-blue-100 dark:bg-blue-900/30', fill: 'bg-blue-500' },
    'Pressure Cooker': { dot: 'bg-amber-500', line: 'bg-amber-200 dark:bg-amber-800', label: 'text-amber-700 dark:text-amber-300', labelBg: 'bg-amber-100 dark:bg-amber-900/30', fill: 'bg-amber-500' },
    'Final Stretch': { dot: 'bg-rose-500', line: 'bg-rose-200 dark:bg-rose-800', label: 'text-rose-700 dark:text-rose-300', labelBg: 'bg-rose-100 dark:bg-rose-900/30', fill: 'bg-rose-500' },
};

// ─── Stat HUD Mini Arc ───────────────────────────────────────────────────────

const STAT_ARC_COLORS: Record<StatKey, string> = {
    energy: 'stroke-amber-500',
    academicCap: 'stroke-blue-500',
    socialSupport: 'stroke-emerald-500',
    systemSavvy: 'stroke-purple-500',
    resilience: 'stroke-rose-500',
};

const StatHudItem = ({ stat, value, prevValue }: { stat: StatKey; value: number; prevValue: number }) => {
    const Icon = STAT_ICONS[stat];
    const radius = 14;
    const circumference = 2 * Math.PI * radius;
    const progress = (value / 100) * circumference;
    const changed = value !== prevValue;
    const increased = value > prevValue;

    return (
        <div className="flex flex-col items-center gap-0.5 relative">
            <div className="relative w-9 h-9">
                <svg viewBox="0 0 36 36" className="w-9 h-9 -rotate-90">
                    <circle cx="18" cy="18" r={radius} fill="none" strokeWidth="2.5"
                        className="stroke-zinc-200 dark:stroke-white/10" />
                    <MotionCircle
                        cx="18" cy="18" r={radius} fill="none" strokeWidth="2.5"
                        strokeLinecap="round"
                        className={STAT_ARC_COLORS[stat]}
                        initial={{ strokeDashoffset: circumference }}
                        animate={{ strokeDashoffset: circumference - progress }}
                        transition={{ duration: 0.6, ease: 'easeOut' }}
                        style={{ strokeDasharray: circumference }}
                    />
                </svg>
                <div className="absolute inset-0 flex items-center justify-center">
                    <Icon size={13} className={STAT_COLORS[stat]} />
                </div>
            </div>
            <MotionSpan
                key={value}
                initial={changed ? { scale: 1.4, color: increased ? '#10b981' : '#f43f5e' } : false}
                animate={{ scale: 1, color: 'inherit' }}
                transition={{ duration: 0.4 }}
                className="text-[10px] font-bold font-mono text-zinc-500 dark:text-zinc-400"
            >
                {value}
            </MotionSpan>
        </div>
    );
};

// ─── Compact Stat HUD ────────────────────────────────────────────────────────

const StatHud = ({ gameState, prevState }: { gameState: GameState; prevState: GameState }) => (
    <div className="flex items-center justify-center gap-4">
        {(Object.keys(gameState) as StatKey[]).map(stat => (
            <StatHudItem key={stat} stat={stat} value={gameState[stat]} prevValue={prevState[stat]} />
        ))}
    </div>
);

// ─── Phase Progress Timeline ─────────────────────────────────────────────────

const PhaseTimeline = ({ currentMonth, currentPhase }: { currentMonth: string; currentPhase: Phase }) => {
    const currentMonthIndex = MONTH_TO_INDEX[currentMonth] ?? 0;
    const phases: Phase[] = ['Foundation', 'Pressure Cooker', 'Final Stretch'];

    return (
        <div className="flex items-center gap-1 w-full">
            {phases.map((phase, pi) => {
                const months = PHASE_MONTHS[phase];
                const colors = PHASE_COLORS[phase];
                const phaseStartIndex = pi === 0 ? 0 : pi === 1 ? 4 : 7;
                const isCurrentPhase = phase === currentPhase;

                return (
                    <React.Fragment key={phase}>
                        {pi > 0 && <div className="w-2 h-px bg-zinc-300 dark:bg-zinc-600 flex-shrink-0" />}
                        <div className="flex-1 min-w-0">
                            <div className="flex gap-0.5 mb-1">
                                {months.map((m, mi) => {
                                    const monthAbsIndex = phaseStartIndex + mi;
                                    const isCurrent = monthAbsIndex === currentMonthIndex && isCurrentPhase;
                                    const isPast = monthAbsIndex < currentMonthIndex;
                                    return (
                                        <div key={m} className={`flex-1 h-1.5 rounded-full transition-all duration-300 ${
                                            isCurrent ? colors.fill : isPast ? colors.fill + ' opacity-40' : 'bg-zinc-200 dark:bg-white/10'
                                        }`} />
                                    );
                                })}
                            </div>
                            <p className={`text-[9px] font-bold text-center truncate ${isCurrentPhase ? colors.label : 'text-zinc-400 dark:text-zinc-600'}`}>
                                {phase}
                            </p>
                        </div>
                    </React.Fragment>
                );
            })}
        </div>
    );
};

// ─── Achievement Toast ───────────────────────────────────────────────────────

type Toast = { id: number; message: string };

const AchievementToast = ({ toast, onDone }: { toast: Toast; onDone: () => void }) => {
    useEffect(() => {
        const timer = setTimeout(onDone, 3000);
        return () => clearTimeout(timer);
    }, [onDone]);

    return (
        <MotionDiv
            initial={{ opacity: 0, y: -20, x: 20 }}
            animate={{ opacity: 1, y: 0, x: 0 }}
            exit={{ opacity: 0, y: -20, x: 20 }}
            className="bg-white dark:bg-zinc-800 border border-zinc-200 dark:border-white/10 rounded-lg px-4 py-2.5 shadow-lg flex items-center gap-2"
        >
            <Sparkles size={14} className="text-amber-500 flex-shrink-0" />
            <p className="text-xs font-medium text-zinc-700 dark:text-zinc-300">{toast.message}</p>
        </MotionDiv>
    );
};

// ─── ChoiceFeedback (inline, not modal) ──────────────────────────────────────

type FeedbackState = {
    effects: Partial<GameState>;
    moduleLink?: Choice['moduleLink'];
};

const InlineChoiceFeedback: React.FC<{ feedback: FeedbackState; onComplete: () => void }> = ({ feedback, onComplete }) => {
    const [showInsight, setShowInsight] = useState(false);

    useEffect(() => {
        const timer = setTimeout(onComplete, 3000);
        return () => clearTimeout(timer);
    }, [onComplete]);

    return (
        <MotionDiv
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            className="overflow-hidden"
        >
            <div className="bg-white dark:bg-zinc-900 rounded-xl p-4 border border-zinc-200 dark:border-white/10 mt-3 cursor-pointer" onClick={onComplete}>
                <div className="flex flex-wrap items-center gap-3 mb-2">
                    {Object.entries(feedback.effects).map(([stat, value], index) => {
                        const Icon = STAT_ICONS[stat as StatKey];
                        const isPositive = (value as number) >= 0;
                        return (
                            <MotionDiv
                                key={stat}
                                initial={{ opacity: 0, y: 8 }}
                                animate={{ opacity: 1, y: 0 }}
                                transition={{ delay: index * 0.08 }}
                                className="flex items-center gap-1"
                            >
                                <Icon size={14} className={isPositive ? 'text-emerald-500' : 'text-rose-500'} />
                                {isPositive
                                    ? <ArrowUp size={10} className="text-emerald-500" />
                                    : <ArrowDown size={10} className="text-rose-500" />
                                }
                                <span className={`font-mono text-xs font-bold ${isPositive ? 'text-emerald-600 dark:text-emerald-400' : 'text-rose-600 dark:text-rose-400'}`}>
                                    {Math.abs(value as number)}
                                </span>
                            </MotionDiv>
                        );
                    })}
                </div>

                {feedback.moduleLink && (
                    <button
                        onClick={(e) => { e.stopPropagation(); setShowInsight(!showInsight); }}
                        className="text-[11px] font-semibold text-purple-600 dark:text-purple-400 hover:underline flex items-center gap-1"
                    >
                        <BookMarked size={11} />
                        {showInsight ? 'Hide insight' : 'Learn more'}
                    </button>
                )}

                <AnimatePresence>
                    {showInsight && feedback.moduleLink && (
                        <MotionDiv
                            initial={{ opacity: 0, height: 0 }}
                            animate={{ opacity: 1, height: 'auto' }}
                            exit={{ opacity: 0, height: 0 }}
                            className="overflow-hidden"
                        >
                            <div className="mt-2 bg-purple-50 dark:bg-purple-900/20 border border-purple-200 dark:border-purple-700/30 rounded-lg p-3">
                                <p className="text-[10px] font-bold text-purple-600 dark:text-purple-400 mb-1">{feedback.moduleLink.moduleTitle}</p>
                                <p className="text-[11px] text-purple-700 dark:text-purple-300 leading-relaxed">{feedback.moduleLink.insight}</p>
                            </div>
                        </MotionDiv>
                    )}
                </AnimatePresence>

                <p className="text-[10px] text-zinc-400 dark:text-zinc-500 mt-2">Tap to continue</p>
            </div>
        </MotionDiv>
    );
};

// ─── PhaseTransition ─────────────────────────────────────────────────────────

const PhaseTransition: React.FC<{ phase: Phase; gameState: GameState; onComplete: () => void }> = ({ phase, gameState, onComplete }) => {
    useEffect(() => {
        const timer = setTimeout(onComplete, 4000);
        return () => clearTimeout(timer);
    }, [onComplete]);

    const meta = PHASE_METADATA.find(p => p.name === phase);

    return (
        <MotionDiv
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            transition={{ duration: 0.5 }}
            onClick={onComplete}
            className="cursor-pointer"
        >
            <div className="bg-white/50 dark:bg-white/5 backdrop-blur-2xl border border-zinc-200/50 dark:border-white/10 rounded-xl p-10 text-center">
                <MotionDiv
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.2 }}
                >
                    <p className="text-xs font-bold uppercase tracking-[0.3em] text-purple-600 dark:text-purple-400 mb-2">
                        {meta?.months}
                    </p>
                    <h2 className="font-serif text-4xl font-semibold text-zinc-900 dark:text-white mb-3">
                        {phase}
                    </h2>
                    <p className="text-zinc-500 dark:text-zinc-400 max-w-md mx-auto mb-8">
                        {meta?.subtitle}
                    </p>
                </MotionDiv>

                <MotionDiv
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.5 }}
                    className="grid grid-cols-5 gap-3 max-w-lg mx-auto"
                >
                    {(Object.keys(gameState) as StatKey[]).map(stat => {
                        const Icon = STAT_ICONS[stat];
                        return (
                            <div key={stat} className="text-center">
                                <Icon size={16} className={`${STAT_COLORS[stat]} mx-auto mb-1`} />
                                <div className="w-full bg-zinc-200 dark:bg-white/10 rounded-full h-1.5">
                                    <div className={`h-1.5 rounded-full ${STAT_BG_COLORS[stat]}`} style={{ width: `${gameState[stat]}%` }} />
                                </div>
                                <p className="text-[10px] font-bold text-zinc-400 dark:text-zinc-500 mt-1">{gameState[stat]}</p>
                            </div>
                        );
                    })}
                </MotionDiv>

                <MotionDiv
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    transition={{ delay: 1 }}
                    className="mt-6"
                >
                    <p className="text-[10px] text-zinc-400 dark:text-zinc-500">Click to continue</p>
                </MotionDiv>
            </div>
        </MotionDiv>
    );
};

// ─── ReportCard ──────────────────────────────────────────────────────────────

const ReportCard: React.FC<{ endingId: string; gameState: GameState; history: HistoryItem[]; onRestart: () => void; onSelectModule?: (moduleId: string) => void }> = ({ endingId, gameState, history, onRestart, onSelectModule }) => {
    const [showLog, setShowLog] = useState(false);
    const archetype = ARCHETYPES[endingId];
    const endScene = STORY_DATA[endingId];
    const turningPoints = getKeyTurningPoints(history);
    const weakestStat = getWeakestStat(gameState);
    const recommendedModules = STAT_TO_MODULES[weakestStat];

    // Compute branching path tree data — show ALL unchosen options
    const pathNodes = history.map((item) => {
        const choices = item.scene.choices || [];
        const branches: { label: string; locked: boolean }[] = [];
        for (const alt of choices) {
            if (alt.text !== item.choiceText) {
                const isLocked = !!alt.requires;
                // Truncate to keep compact
                const label = alt.text.length > 40 ? alt.text.slice(0, 38) + '...' : alt.text;
                branches.push({ label, locked: isLocked });
            }
        }
        return { title: item.scene.title, phase: item.scene.phase, choiceText: item.choiceText, branches };
    });

    // Paths not taken — locked choices the player missed
    const pathsNotTaken: { sceneTitle: string; choiceText: string; requirement: string }[] = [];
    for (const item of history) {
        const choices = item.scene.choices || [];
        for (const alt of choices) {
            if (alt.text !== item.choiceText && alt.requires) {
                const reqText = alt.requires.map(r => `${STAT_LABELS[r.stat]} ${r.min}+`).join(', ');
                const meetsReqs = alt.requires.every(r => gameState[r.stat] >= r.min);
                if (!meetsReqs) {
                    pathsNotTaken.push({ sceneTitle: item.scene.title, choiceText: alt.text, requirement: reqText });
                }
            }
        }
    }

    const phases: Phase[] = ['Foundation', 'Pressure Cooker', 'Final Stretch'];
    const groupedPath = phases
        .map(phase => ({ phase, nodes: pathNodes.filter(n => n.phase === phase) }))
        .filter(g => g.nodes.length > 0);

    return (
        <MotionDiv initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="space-y-6">
            {/* A. Archetype Badge */}
            <div className={`${archetype?.accentBg || 'bg-zinc-100 dark:bg-white/5'} rounded-2xl p-8 text-center border border-zinc-200/50 dark:border-white/10`}>
                <div className="mx-auto mb-4 w-16 h-16 rounded-2xl bg-white/60 dark:bg-white/10 flex items-center justify-center">
                    {(() => { const IconComp = archetype?.icon ? ARCHETYPE_ICONS[archetype.icon] : GraduationCap; return IconComp ? <IconComp size={32} className={archetype?.accentColor || 'text-zinc-600 dark:text-zinc-300'} /> : <GraduationCap size={32} className="text-zinc-600 dark:text-zinc-300" />; })()}
                </div>
                <h3 className={`font-serif text-3xl font-semibold mb-3 ${archetype?.accentColor || 'text-zinc-900 dark:text-white'}`}>
                    {archetype?.title || endScene?.title || 'Results Day'}
                </h3>
                <p className="text-zinc-600 dark:text-zinc-300 leading-relaxed max-w-lg mx-auto">
                    {archetype?.description || endScene?.text}
                </p>
            </div>

            {/* B. Stat Letter Grades */}
            <div>
                <h4 className="font-bold text-sm uppercase tracking-widest text-zinc-500 dark:text-zinc-400 mb-3 text-center">Your Grades</h4>
                <div className="grid grid-cols-5 gap-3">
                    {(Object.keys(gameState) as StatKey[]).map(stat => {
                        const grade = getStatGrade(gameState[stat]);
                        const Icon = STAT_ICONS[stat];
                        return (
                            <div key={stat} className="bg-white/50 dark:bg-white/5 border border-zinc-200 dark:border-white/10 rounded-xl p-3 text-center">
                                <Icon size={16} className={`${STAT_COLORS[stat]} mx-auto mb-1`} />
                                <p className={`font-serif text-2xl font-bold ${grade.color}`}>{grade.letter}</p>
                                <p className="text-[10px] font-bold text-zinc-400 dark:text-zinc-500 mt-0.5">{STAT_LABELS[stat]}</p>
                            </div>
                        );
                    })}
                </div>
            </div>

            {/* B2. Weakest Stat Insight */}
            <div className="bg-amber-50 dark:bg-amber-900/15 border border-amber-200 dark:border-amber-700/30 rounded-2xl p-6">
                <div className="flex items-center gap-2 mb-3">
                    <AlertTriangle size={16} className="text-amber-600 dark:text-amber-400" />
                    <h4 className="font-bold text-sm uppercase tracking-widest text-amber-600 dark:text-amber-400">Your Biggest Vulnerability: {STAT_LABELS[weakestStat]}</h4>
                </div>
                <p className="text-sm text-zinc-700 dark:text-zinc-300 leading-relaxed">
                    {WEAKEST_STAT_INSIGHTS[weakestStat]}
                </p>
            </div>

            {/* C. Key Turning Points */}
            {turningPoints.length > 0 && (
                <div>
                    <h4 className="font-bold text-sm uppercase tracking-widest text-zinc-500 dark:text-zinc-400 mb-3 text-center">Key Turning Points</h4>
                    <div className="space-y-2">
                        {turningPoints.map((item, index) => (
                            <div key={index} className="bg-white/50 dark:bg-white/5 border border-zinc-200 dark:border-white/10 rounded-xl p-4">
                                <div className="flex items-center gap-2 mb-1">
                                    <p className="text-xs font-bold text-purple-600 dark:text-purple-400">{item.scene.month}</p>
                                    <span className="text-zinc-300 dark:text-zinc-600">|</span>
                                    <p className="text-xs font-bold text-zinc-700 dark:text-zinc-300">{item.scene.title}</p>
                                </div>
                                <p className="text-sm text-zinc-600 dark:text-zinc-400">{item.choiceText}</p>
                                <div className="flex items-center gap-3 mt-2">
                                    {Object.entries(item.effects).map(([stat, value]) => {
                                        const Icon = STAT_ICONS[stat as StatKey];
                                        const isPositive = (value as number) >= 0;
                                        return (
                                            <div key={stat} className="flex items-center gap-1">
                                                <Icon size={12} className={isPositive ? 'text-emerald-500' : 'text-rose-500'} />
                                                <span className={`font-mono text-xs font-bold ${isPositive ? 'text-emerald-500' : 'text-rose-500'}`}>
                                                    {isPositive ? '+' : ''}{value}
                                                </span>
                                            </div>
                                        );
                                    })}
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            )}

            {/* D. Paths Not Taken */}
            {pathsNotTaken.length > 0 && (
                <div>
                    <h4 className="font-bold text-sm uppercase tracking-widest text-zinc-500 dark:text-zinc-400 mb-3 text-center">Paths Not Taken</h4>
                    <div className="space-y-2">
                        {pathsNotTaken.slice(0, 3).map((path, index) => (
                            <div key={index} className="bg-zinc-50 dark:bg-white/5 border border-zinc-200 dark:border-white/10 rounded-xl p-3">
                                <div className="flex items-center gap-2 mb-1">
                                    <Lock size={12} className="text-zinc-400 dark:text-zinc-500" />
                                    <p className="text-xs font-bold text-zinc-500 dark:text-zinc-400">{path.sceneTitle}</p>
                                </div>
                                <p className="text-sm text-zinc-500 dark:text-zinc-400 italic">{path.choiceText}</p>
                                <p className="text-[10px] text-zinc-400 dark:text-zinc-500 mt-1">Required: {path.requirement}</p>
                            </div>
                        ))}
                    </div>
                </div>
            )}

            {/* E. Recommended Modules */}
            <div>
                <h4 className="font-bold text-sm uppercase tracking-widest text-zinc-500 dark:text-zinc-400 mb-1 text-center">Recommended For You</h4>
                <p className="text-xs text-zinc-400 dark:text-zinc-500 text-center mb-3">Based on your weakest area: {STAT_LABELS[weakestStat]}</p>
                <div className="space-y-2">
                    {recommendedModules.map(mod => (
                        <button
                            key={mod.moduleId}
                            onClick={() => onSelectModule?.(mod.moduleId)}
                            className="w-full flex items-center gap-3 bg-purple-50 dark:bg-purple-900/20 border border-purple-200 dark:border-purple-700/30 rounded-xl p-3 text-left hover:bg-purple-100 dark:hover:bg-purple-900/40 transition-colors group"
                        >
                            <BookMarked size={16} className="text-purple-600 dark:text-purple-400 flex-shrink-0" />
                            <p className="text-sm font-semibold text-purple-700 dark:text-purple-300 flex-1">{mod.moduleTitle}</p>
                            <ArrowRight size={14} className="text-purple-400 dark:text-purple-500 opacity-0 group-hover:opacity-100 transition-opacity flex-shrink-0" />
                        </button>
                    ))}
                </div>
            </div>

            {/* F. Detroit-Style Branching Path Tree */}
            {(() => {
                // Layout constants
                const COL_W = 140;
                const BRANCH_H = 26;
                const NODE_H = 26;
                const NODE_W = 120;
                const PAD_L = 20;
                const PAD_T = 48;
                const GAP_LINE = 20;

                // Phase stroke colors
                const PHASE_STROKE: Record<Phase, string> = {
                    'Foundation': '#3b82f6',
                    'Pressure Cooker': '#f59e0b',
                    'Final Stretch': '#f43f5e',
                };

                // Build flat column list with branch counts for height calc
                const allNodes = pathNodes;
                const totalCols = allNodes.length + 1; // +1 for end node
                const maxBranches = Math.max(...allNodes.map(n => n.branches.length), 0);
                const svgW = totalCols * COL_W + PAD_L * 2;
                const svgH = PAD_T + NODE_H + (maxBranches > 0 ? maxBranches * BRANCH_H + 12 : 0) + 20;

                // Phase divider positions
                const phaseDividers: { phase: Phase; startCol: number; endCol: number }[] = [];
                let runCol = 0;
                for (const group of groupedPath) {
                    const start = runCol;
                    runCol += group.nodes.length;
                    phaseDividers.push({ phase: group.phase, startCol: start, endCol: runCol - 1 });
                }

                // Node center helpers
                const nodeCx = (col: number) => PAD_L + col * COL_W + NODE_W / 2;
                const nodeCy = PAD_T + NODE_H / 2;
                const branchCy = (bi: number) => PAD_T + NODE_H + 10 + bi * BRANCH_H + BRANCH_H / 2;

                return (
                    <div>
                        <h4 className="font-bold text-sm uppercase tracking-widest text-zinc-500 dark:text-zinc-400 mb-3 text-center">Your Path</h4>
                        <div className="bg-zinc-50 dark:bg-zinc-900 border border-zinc-200 dark:border-white/10 rounded-xl overflow-x-auto">
                            <div style={{ width: svgW, height: svgH }} className="relative">

                                {/* Phase labels — positioned above their column span */}
                                {phaseDividers.map(({ phase, startCol, endCol }) => {
                                    const phaseColors = PHASE_COLORS[phase];
                                    const midX = PAD_L + ((startCol + endCol) / 2) * COL_W + NODE_W / 2;
                                    return (
                                        <div key={phase} className="absolute" style={{ left: midX, top: 12, transform: 'translateX(-50%)' }}>
                                            <span className={`px-2.5 py-0.5 rounded-full text-[9px] font-bold uppercase tracking-wider whitespace-nowrap ${phaseColors.label} ${phaseColors.labelBg}`}>
                                                {phase}
                                            </span>
                                        </div>
                                    );
                                })}

                                {/* SVG connecting lines */}
                                <svg width={svgW} height={svgH} className="absolute inset-0 pointer-events-none">
                                    {/* Horizontal taken-path lines between nodes */}
                                    {allNodes.map((node, i) => {
                                        if (i === allNodes.length - 1) return null;
                                        const x1 = nodeCx(i) + NODE_W / 2;
                                        const x2 = nodeCx(i + 1) - NODE_W / 2;
                                        const stroke = PHASE_STROKE[node.phase];
                                        return <line key={`h-${i}`} x1={x1} y1={nodeCy} x2={x2} y2={nodeCy} stroke={stroke} strokeWidth="2" opacity="0.6" />;
                                    })}
                                    {/* Line from last node to end */}
                                    {allNodes.length > 0 && (
                                        <line
                                            x1={nodeCx(allNodes.length - 1) + NODE_W / 2}
                                            y1={nodeCy}
                                            x2={nodeCx(allNodes.length) - NODE_W / 2}
                                            y2={nodeCy}
                                            stroke={PHASE_STROKE[allNodes[allNodes.length - 1].phase]}
                                            strokeWidth="2" opacity="0.6"
                                        />
                                    )}
                                    {/* Vertical dashed lines to branches */}
                                    {allNodes.map((node, colIdx) => (
                                        node.branches.map((_, bi) => (
                                            <line
                                                key={`v-${colIdx}-${bi}`}
                                                x1={nodeCx(colIdx)}
                                                y1={nodeCy + NODE_H / 2}
                                                x2={nodeCx(colIdx)}
                                                y2={branchCy(bi) - BRANCH_H / 2}
                                                stroke="#a1a1aa"
                                                strokeWidth="1"
                                                strokeDasharray="3 2"
                                                opacity="0.4"
                                            />
                                        ))
                                    ))}
                                </svg>

                                {/* Taken-path node boxes */}
                                {allNodes.map((node, colIdx) => {
                                    const phaseColors = PHASE_COLORS[node.phase];
                                    return (
                                        <div key={`n-${colIdx}`} className="absolute" style={{ left: PAD_L + colIdx * COL_W, top: PAD_T, width: NODE_W, height: NODE_H }}>
                                            <div className={`w-full h-full rounded-md flex items-center justify-center px-2 ${phaseColors.dot}`} title={node.title}>
                                                <p className="text-[9px] font-bold text-white leading-none truncate">{node.title}</p>
                                            </div>
                                        </div>
                                    );
                                })}

                                {/* Branch (not-taken) boxes */}
                                {allNodes.map((node, colIdx) => (
                                    node.branches.map((branch, bi) => (
                                        <div
                                            key={`b-${colIdx}-${bi}`}
                                            className="absolute"
                                            style={{ left: PAD_L + colIdx * COL_W + 6, top: PAD_T + NODE_H + 10 + bi * BRANCH_H, width: NODE_W - 12, height: BRANCH_H - 4 }}
                                        >
                                            <div className="w-full h-full rounded border border-zinc-200 dark:border-zinc-700 bg-white dark:bg-zinc-800 flex items-center justify-center px-1.5 gap-1" title={branch.label}>
                                                {branch.locked && <Lock size={7} className="text-zinc-400 dark:text-zinc-500 flex-shrink-0" />}
                                                <p className="text-[8px] text-zinc-400 dark:text-zinc-500 leading-none truncate">{branch.label}</p>
                                            </div>
                                        </div>
                                    ))
                                ))}

                                {/* End node */}
                                <div className="absolute" style={{ left: PAD_L + allNodes.length * COL_W, top: PAD_T, width: NODE_W, height: NODE_H }}>
                                    <div className={`w-full h-full rounded-md flex items-center justify-center gap-1.5 px-2 ${archetype?.accentBg || 'bg-zinc-100 dark:bg-white/5'} border border-zinc-200/50 dark:border-white/10`}>
                                        {(() => { const IC = archetype?.icon ? ARCHETYPE_ICONS[archetype.icon] : GraduationCap; return IC ? <IC size={10} className={archetype?.accentColor || 'text-zinc-600 dark:text-zinc-300'} /> : null; })()}
                                        <p className={`text-[8px] font-bold leading-none truncate ${archetype?.accentColor || 'text-zinc-700 dark:text-zinc-300'}`}>
                                            {archetype?.title || 'End'}
                                        </p>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                );
            })()}

            {/* G. Collapsible Journey Log */}
            <div>
                <button
                    onClick={() => setShowLog(!showLog)}
                    className="w-full flex items-center justify-center gap-2 text-sm font-bold text-zinc-500 dark:text-zinc-400 hover:text-zinc-700 dark:hover:text-zinc-200 transition-colors py-2"
                >
                    {showLog ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
                    {showLog ? 'Hide' : 'Show'} Full Journey Log ({history.length} decisions)
                </button>
                {showLog && (
                    <MotionDiv
                        initial={{ opacity: 0, height: 0 }}
                        animate={{ opacity: 1, height: 'auto' }}
                        className="overflow-hidden"
                    >
                        <div className="text-left space-y-4 max-h-96 overflow-y-auto p-4 bg-zinc-100 dark:bg-white/5 rounded-xl border border-zinc-200 dark:border-white/10 mt-2">
                            {history.map((item, index) => (
                                <div key={index} className="relative pl-8">
                                    <div className="absolute top-1 left-0 flex flex-col items-center">
                                        <div className="w-6 h-6 rounded-full bg-purple-200 dark:bg-purple-800 flex items-center justify-center ring-4 ring-zinc-100 dark:ring-white/5">
                                            <GitBranch size={14} className="text-purple-600 dark:text-purple-300"/>
                                        </div>
                                        {index < history.length - 1 && <div className="w-px h-full bg-zinc-300 dark:bg-zinc-700 mt-1" style={{height: 'calc(100% + 1rem)'}} />}
                                    </div>
                                    <p className="font-bold text-sm text-zinc-800 dark:text-zinc-200">{item.scene.month}: {item.scene.title}</p>
                                    <p className="text-xs text-zinc-500 dark:text-zinc-400 mt-1">{item.choiceText}</p>
                                    <div className="flex items-center gap-2 mt-1">
                                        {Object.entries(item.effects).map(([stat, value]) => {
                                            const Icon = STAT_ICONS[stat as StatKey];
                                            const isPositive = (value as number) >= 0;
                                            return (
                                                <div key={stat} className="flex items-center gap-0.5">
                                                    <Icon size={10} className={isPositive ? 'text-emerald-500' : 'text-rose-500'} />
                                                    <span className={`font-mono text-[10px] font-bold ${isPositive ? 'text-emerald-500' : 'text-rose-500'}`}>
                                                        {isPositive ? '+' : ''}{value}
                                                    </span>
                                                </div>
                                            );
                                        })}
                                    </div>
                                </div>
                            ))}
                        </div>
                    </MotionDiv>
                )}
            </div>

            {/* Play Again */}
            <div className="text-center">
                <MotionButton
                    onClick={onRestart}
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                    className="inline-flex items-center gap-2 px-6 py-3 bg-zinc-800 dark:bg-white text-white dark:text-zinc-900 font-bold text-sm rounded-full shadow-lg hover:bg-purple-600 dark:hover:bg-purple-400 transition-colors"
                >
                    Play Again <RotateCcw size={16} />
                </MotionButton>
            </div>
        </MotionDiv>
    );
};

// ─── Choice Button (with locked state) ───────────────────────────────────────

const ChoiceButton: React.FC<{ choice: Choice; gameState: GameState; visitedScenes: string[]; onChoose: (choice: Choice) => void; disabled?: boolean; chosen?: boolean }> = ({ choice, gameState, visitedScenes, onChoose, disabled, chosen }) => {
    const statRequirementsMet = !choice.requires || choice.requires.every(r => gameState[r.stat] >= r.min);
    const visitRequirementsMet = !choice.requiresVisited || choice.requiresVisited.every(id => visitedScenes.includes(id));
    const isLocked = !statRequirementsMet || !visitRequirementsMet;

    if (isLocked) {
        return (
            <div className="w-full text-left p-4 rounded-xl bg-zinc-100/50 dark:bg-white/[0.02] border border-zinc-200/50 dark:border-white/5 opacity-60">
                <div className="flex items-center gap-2">
                    <Lock size={14} className="text-zinc-400 dark:text-zinc-500 flex-shrink-0" />
                    <p className="font-semibold text-zinc-400 dark:text-zinc-500 text-sm">{choice.text}</p>
                </div>
                {choice.requires && (
                    <div className="flex flex-wrap items-center gap-2 mt-2 ml-6">
                        {choice.requires.map((r, i) => {
                            const Icon = STAT_ICONS[r.stat];
                            const met = gameState[r.stat] >= r.min;
                            return (
                                <span key={i} className={`inline-flex items-center gap-1 text-[10px] font-bold px-2 py-0.5 rounded-full ${
                                    met ? 'bg-emerald-100 dark:bg-emerald-900/30 text-emerald-600 dark:text-emerald-400' : 'bg-zinc-200 dark:bg-white/10 text-zinc-500 dark:text-zinc-400'
                                }`}>
                                    <Icon size={10} />
                                    {STAT_LABELS[r.stat]} {r.min}+
                                </span>
                            );
                        })}
                    </div>
                )}
                {choice.flavor && <p className="text-[10px] text-zinc-400 dark:text-zinc-500 mt-1.5 ml-6 italic">{choice.flavor}</p>}
            </div>
        );
    }

    if (disabled && !chosen) {
        return (
            <div className="w-full text-left p-4 rounded-xl bg-zinc-100/50 dark:bg-white/[0.02] border border-zinc-200/50 dark:border-white/5 opacity-40 transition-opacity">
                <p className="font-semibold text-zinc-400 dark:text-zinc-500 text-sm">{choice.text}</p>
            </div>
        );
    }

    if (chosen) {
        return (
            <div className="w-full text-left p-4 rounded-xl bg-purple-50 dark:bg-purple-900/20 border-2 border-purple-300 dark:border-purple-600/50">
                <p className="font-semibold text-purple-700 dark:text-purple-300 text-sm">{choice.text}</p>
            </div>
        );
    }

    return (
        <MotionButton
            onClick={() => onChoose(choice)}
            whileHover={{ scale: 1.01 }}
            whileTap={{ scale: 0.99 }}
            className="w-full text-left p-4 rounded-xl bg-zinc-100 dark:bg-white/5 border border-zinc-200 dark:border-white/10 hover:bg-zinc-200 dark:hover:bg-white/10 transition-colors"
        >
            <p className="font-semibold text-zinc-700 dark:text-zinc-200 text-sm">{choice.text}</p>
            {choice.flavor && <p className="text-[10px] text-zinc-400 dark:text-zinc-500 mt-1 italic">{choice.flavor}</p>}
        </MotionButton>
    );
};

// ─── AcademicJourneyGame ─────────────────────────────────────────────────────

const AcademicJourneyGame: React.FC<{ onSelectModule?: (moduleId: string) => void; user?: { uid: string } | null; savedJourneyResult?: JourneyResult | null; onJourneyComplete?: (result: JourneyResult) => void }> = ({ onSelectModule, user, savedJourneyResult, onJourneyComplete }) => {
    const [gameState, setGameState] = useState<GameState>({ ...INITIAL_GAME_STATE });
    const [prevState, setPrevState] = useState<GameState>({ ...INITIAL_GAME_STATE });
    const [currentSceneId, setCurrentSceneId] = useState('START');
    const [history, setHistory] = useState<HistoryItem[]>([]);
    const [visitedScenes, setVisitedScenes] = useState<string[]>(['START']);
    const [currentPhase, setCurrentPhase] = useState<Phase>('Foundation');
    const [showPhaseTransition, setShowPhaseTransition] = useState(false);
    const [pendingSceneId, setPendingSceneId] = useState<string | null>(null);
    const [feedbackState, setFeedbackState] = useState<FeedbackState | null>(null);
    const [chosenText, setChosenText] = useState<string | null>(null);
    const [toasts, setToasts] = useState<Toast[]>([]);
    const [previousResult, setPreviousResult] = useState<{ endingId: string; completedAt?: string; finalStats?: GameState } | null>(savedJourneyResult || null);
    const [showingSavedResult, setShowingSavedResult] = useState(!!savedJourneyResult);
    const toastIdRef = useRef(0);
    const hasSavedRef = useRef(false);

    const currentScene = STORY_DATA[currentSceneId];
    const isEndScene = currentSceneId.startsWith('END_');

    // Load previous journey result from Firestore — auto-show if exists
    useEffect(() => {
        if (!user?.uid) return;
        const loadPrevious = async () => {
            try {
                const progressDoc = await getDoc(doc(db, 'progress', user.uid));
                if (progressDoc.exists()) {
                    const data = progressDoc.data();
                    if (data['journey-simulator']?.endingId) {
                        setPreviousResult(data['journey-simulator']);
                        setShowingSavedResult(true);
                    }
                }
            } catch (e) {
                console.error('Failed to load journey result:', e);
            }
        };
        loadPrevious();
    }, [user?.uid]);

    // Save journey result when game ends — lift to App.tsx + persist to Firestore
    useEffect(() => {
        if (!isEndScene || hasSavedRef.current) return;
        hasSavedRef.current = true;
        const result = { endingId: currentSceneId, finalStats: gameState };
        setPreviousResult(result);
        onJourneyComplete?.(result);
        if (user?.uid) {
            const saveResult = async () => {
                try {
                    const progressDocRef = doc(db, 'progress', user.uid);
                    await setDoc(progressDocRef, {
                        'journey-simulator': {
                            completedAt: new Date().toISOString(),
                            endingId: currentSceneId,
                            finalStats: gameState,
                            decisionsCount: history.length,
                        }
                    }, { merge: true });
                } catch (e) {
                    console.error('Failed to save journey result:', e);
                }
            };
            saveResult();
        }
    }, [isEndScene, user?.uid, currentSceneId, gameState, history.length]);

    // Check for stat threshold crossings and show toasts
    const checkThresholds = useCallback((prev: GameState, next: GameState) => {
        const thresholds = [40, 60, 80];
        const messages: Record<StatKey, string[]> = {
            energy: ['Energy stabilizing...', 'Energy is strong! Stay sharp.', 'Peak energy! You\'re in the zone.'],
            academicCap: ['Academic skills building...', 'Academic mastery growing! New options may appear...', 'Elite academic level reached!'],
            socialSupport: ['Social network forming...', 'Strong social support! New paths may open...', 'Social powerhouse! Collaborative options unlocked.'],
            systemSavvy: ['System awareness rising...', 'System savvy growing! New strategies may appear...', 'System master! You see angles others miss.'],
            resilience: ['Resilience building...', 'Resilience is growing! New options may appear...', 'Iron resilience! Nothing can break you.'],
        };

        for (const stat of Object.keys(next) as StatKey[]) {
            for (let i = 0; i < thresholds.length; i++) {
                if (prev[stat] < thresholds[i] && next[stat] >= thresholds[i]) {
                    const id = ++toastIdRef.current;
                    setToasts(prev => [...prev, { id, message: messages[stat][i] }]);
                }
            }
        }
    }, []);

    const handleChoice = useCallback((choice: Choice) => {
        const currentChoiceScene = STORY_DATA[currentSceneId];
        const newGameState = { ...gameState };

        for (const [key, value] of Object.entries(choice.effects)) {
            newGameState[key as StatKey] = Math.max(0, Math.min(100, newGameState[key as StatKey] + value));
        }

        const newHistoryItem: HistoryItem = {
            scene: currentChoiceScene,
            choiceText: choice.text,
            effects: choice.effects,
            moduleLink: choice.moduleLink,
        };
        const newHistory = [...history, newHistoryItem];
        setHistory(newHistory);
        setPrevState(gameState);
        setGameState(newGameState);
        checkThresholds(gameState, newGameState);

        // Resolve route if it's an invisible logic gate
        let targetSceneId = choice.nextSceneId;
        if (targetSceneId.startsWith('__') && ROUTE_RESOLVERS[targetSceneId]) {
            targetSceneId = ROUTE_RESOLVERS[targetSceneId](newGameState, newHistory);
        }

        // Track visited scenes
        setVisitedScenes(prev => [...prev, targetSceneId]);

        // Show feedback inline, then advance
        setChosenText(choice.text);
        setFeedbackState({ effects: choice.effects, moduleLink: choice.moduleLink });
        setPendingSceneId(targetSceneId);
    }, [currentSceneId, gameState, history, checkThresholds]);

    const handleFeedbackComplete = useCallback(() => {
        setFeedbackState(null);
        setChosenText(null);
        if (pendingSceneId) {
            const targetScene = STORY_DATA[pendingSceneId];
            if (targetScene && targetScene.phase !== currentPhase) {
                setShowPhaseTransition(true);
                setCurrentPhase(targetScene.phase);
            } else {
                setCurrentSceneId(pendingSceneId);
                setPendingSceneId(null);
            }
        }
    }, [pendingSceneId, currentPhase]);

    const handlePhaseTransitionComplete = useCallback(() => {
        setShowPhaseTransition(false);
        if (pendingSceneId) {
            setCurrentSceneId(pendingSceneId);
            setPendingSceneId(null);
        }
    }, [pendingSceneId]);

    const restartGame = useCallback(() => {
        setGameState({ ...INITIAL_GAME_STATE });
        setPrevState({ ...INITIAL_GAME_STATE });
        setCurrentSceneId('START');
        setHistory([]);
        setVisitedScenes(['START']);
        setCurrentPhase('Foundation');
        setShowPhaseTransition(false);
        setPendingSceneId(null);
        setFeedbackState(null);
        setToasts([]);
        hasSavedRef.current = false;
    }, []);

    const removeToast = useCallback((id: number) => {
        setToasts(prev => prev.filter(t => t.id !== id));
    }, []);

    // Saved result screen (returning to journey after completion)
    if (showingSavedResult && previousResult?.endingId && ARCHETYPES[previousResult.endingId]) {
        const savedArch = ARCHETYPES[previousResult.endingId];
        const savedStats = previousResult.finalStats || { ...INITIAL_GAME_STATE };
        return (
            <div className="bg-white/50 dark:bg-white/5 backdrop-blur-2xl border border-zinc-200/50 dark:border-white/10 rounded-xl p-8">
                <MotionDiv initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="space-y-6">
                    {/* Archetype Badge */}
                    <div className={`${savedArch.accentBg} rounded-2xl p-8 text-center border border-zinc-200/50 dark:border-white/10`}>
                        <div className="mx-auto mb-4 w-16 h-16 rounded-2xl bg-white/60 dark:bg-white/10 flex items-center justify-center">
                            {(() => { const IC = ARCHETYPE_ICONS[savedArch.icon]; return IC ? <IC size={32} className={savedArch.accentColor} /> : <GraduationCap size={32} className="text-zinc-600 dark:text-zinc-300" />; })()}
                        </div>
                        <p className="text-[10px] font-bold uppercase tracking-widest text-zinc-400 dark:text-zinc-500 mb-2">Your Previous Result</p>
                        <h3 className={`font-serif text-3xl font-semibold mb-3 ${savedArch.accentColor}`}>{savedArch.title}</h3>
                        <p className="text-zinc-600 dark:text-zinc-300 leading-relaxed max-w-lg mx-auto">{savedArch.description}</p>
                    </div>

                    {/* Saved Stat Grades */}
                    <div>
                        <h4 className="font-bold text-sm uppercase tracking-widest text-zinc-500 dark:text-zinc-400 mb-3 text-center">Your Grades</h4>
                        <div className="grid grid-cols-5 gap-3">
                            {(Object.keys(savedStats) as StatKey[]).map(stat => {
                                const grade = getStatGrade(savedStats[stat]);
                                const Icon = STAT_ICONS[stat];
                                return (
                                    <div key={stat} className="bg-white/50 dark:bg-white/5 border border-zinc-200 dark:border-white/10 rounded-xl p-3 text-center">
                                        <Icon size={16} className={`${STAT_COLORS[stat]} mx-auto mb-1`} />
                                        <p className={`font-serif text-2xl font-bold ${grade.color}`}>{grade.letter}</p>
                                        <p className="text-[10px] font-bold text-zinc-400 dark:text-zinc-500 mt-0.5">{STAT_LABELS[stat]}</p>
                                    </div>
                                );
                            })}
                        </div>
                    </div>

                    {/* Weakest Stat Insight */}
                    <div className="bg-amber-50 dark:bg-amber-900/15 border border-amber-200 dark:border-amber-700/30 rounded-2xl p-6">
                        <div className="flex items-center gap-2 mb-3">
                            <AlertTriangle size={16} className="text-amber-600 dark:text-amber-400" />
                            <h4 className="font-bold text-sm uppercase tracking-widest text-amber-600 dark:text-amber-400">Your Biggest Vulnerability: {STAT_LABELS[getWeakestStat(savedStats)]}</h4>
                        </div>
                        <p className="text-sm text-zinc-700 dark:text-zinc-300 leading-relaxed">
                            {WEAKEST_STAT_INSIGHTS[getWeakestStat(savedStats)]}
                        </p>
                    </div>

                    {/* Recommended Modules */}
                    <div>
                        <h4 className="font-bold text-sm uppercase tracking-widest text-zinc-500 dark:text-zinc-400 mb-1 text-center">Recommended For You</h4>
                        <p className="text-xs text-zinc-400 dark:text-zinc-500 text-center mb-3">Based on your weakest area: {STAT_LABELS[getWeakestStat(savedStats)]}</p>
                        <div className="space-y-2">
                            {STAT_TO_MODULES[getWeakestStat(savedStats)].map(mod => (
                                <button
                                    key={mod.moduleId}
                                    onClick={() => onSelectModule?.(mod.moduleId)}
                                    className="w-full flex items-center gap-3 bg-purple-50 dark:bg-purple-900/20 border border-purple-200 dark:border-purple-700/30 rounded-xl p-3 text-left hover:bg-purple-100 dark:hover:bg-purple-900/40 transition-colors group"
                                >
                                    <BookMarked size={16} className="text-purple-600 dark:text-purple-400 flex-shrink-0" />
                                    <p className="text-sm font-semibold text-purple-700 dark:text-purple-300 flex-1">{mod.moduleTitle}</p>
                                    <ArrowRight size={14} className="text-purple-400 dark:text-purple-500 opacity-0 group-hover:opacity-100 transition-opacity flex-shrink-0" />
                                </button>
                            ))}
                        </div>
                    </div>

                    {/* Play Again */}
                    <div className="text-center">
                        <MotionButton
                            onClick={() => { setShowingSavedResult(false); restartGame(); }}
                            whileHover={{ scale: 1.05 }}
                            whileTap={{ scale: 0.95 }}
                            className="inline-flex items-center gap-2 px-6 py-3 bg-zinc-800 dark:bg-white text-white dark:text-zinc-900 font-bold text-sm rounded-full shadow-lg hover:bg-purple-600 dark:hover:bg-purple-400 transition-colors"
                        >
                            Play Again <RotateCcw size={16} />
                        </MotionButton>
                    </div>
                </MotionDiv>
            </div>
        );
    }

    // End screen
    if (isEndScene) {
        return (
            <div className="bg-white/50 dark:bg-white/5 backdrop-blur-2xl border border-zinc-200/50 dark:border-white/10 rounded-xl p-8">
                <ReportCard endingId={currentSceneId} gameState={gameState} history={history} onRestart={restartGame} onSelectModule={onSelectModule} />
            </div>
        );
    }

    // Phase transition interstitial
    if (showPhaseTransition) {
        return (
            <AnimatePresence mode="wait">
                <PhaseTransition key={currentPhase} phase={currentPhase} gameState={gameState} onComplete={handlePhaseTransitionComplete} />
            </AnimatePresence>
        );
    }

    if (!currentScene || !currentScene.choices) {
        return null;
    }

    const moodConfig = MOOD_CONFIG[currentScene.mood];
    const locationConfig = LOCATION_CONFIG[currentScene.location];
    const MoodIcon = moodConfig.icon;
    const LocationIcon = locationConfig.icon;

    return (
        <>
            {/* Achievement Toasts */}
            <div className="fixed top-24 right-4 z-[90] space-y-2">
                <AnimatePresence>
                    {toasts.map(toast => (
                        <AchievementToast key={toast.id} toast={toast} onDone={() => removeToast(toast.id)} />
                    ))}
                </AnimatePresence>
            </div>

            <div className="space-y-4">
                {/* Previous Result Badge */}
                {currentSceneId === 'START' && previousResult && ARCHETYPES[previousResult.endingId] && (
                    <div className="flex items-center justify-center gap-2 px-4 py-2.5 bg-white/50 dark:bg-white/5 border border-zinc-200/50 dark:border-white/10 rounded-xl">
                        {(() => { const prevArch = ARCHETYPES[previousResult.endingId]; const PrevIcon = prevArch?.icon ? ARCHETYPE_ICONS[prevArch.icon] : GraduationCap; return PrevIcon ? <PrevIcon size={14} className={prevArch.accentColor} /> : null; })()}
                        <p className="text-xs text-zinc-500 dark:text-zinc-400">
                            Previous result: <span className={`font-bold ${ARCHETYPES[previousResult.endingId].accentColor}`}>{ARCHETYPES[previousResult.endingId].title}</span>
                        </p>
                    </div>
                )}

                {/* Phase Timeline + Stat HUD */}
                <div className="bg-white/50 dark:bg-white/5 backdrop-blur-2xl border border-zinc-200/50 dark:border-white/10 rounded-xl px-5 py-3 space-y-3">
                    <PhaseTimeline currentMonth={currentScene.month} currentPhase={currentScene.phase} />
                    <StatHud gameState={gameState} prevState={prevState} />
                </div>

                {/* Scene Card */}
                <div className="bg-white/50 dark:bg-white/5 backdrop-blur-2xl border border-zinc-200/50 dark:border-white/10 rounded-xl p-6">
                    <AnimatePresence mode="wait">
                        <MotionDiv
                            key={currentSceneId}
                            initial={{ opacity: 0, x: 20 }}
                            animate={{ opacity: 1, x: 0 }}
                            exit={{ opacity: 0, x: -20 }}
                            transition={{ duration: 0.4, ease: 'easeInOut' }}
                        >
                            {/* Scene Header */}
                            <div className="flex items-start gap-4 mb-5">
                                {/* Mood Icon */}
                                <div className={`w-12 h-12 rounded-xl flex items-center justify-center flex-shrink-0 ${moodConfig.bg} border ${moodConfig.border}`}>
                                    <MoodIcon size={24} className={moodConfig.text} />
                                </div>
                                <div className="flex-1 min-w-0">
                                    {/* Location pill + Month */}
                                    <div className="flex items-center gap-2 mb-1">
                                        <span className="inline-flex items-center gap-1 text-[10px] font-bold px-2 py-0.5 rounded-full bg-zinc-100 dark:bg-white/10 text-zinc-500 dark:text-zinc-400">
                                            <LocationIcon size={10} />
                                            {locationConfig.label}
                                        </span>
                                        <span className="text-[10px] font-bold text-zinc-400 dark:text-zinc-500">{currentScene.month}</span>
                                    </div>
                                    <h3 className="font-serif text-xl font-semibold text-zinc-900 dark:text-white leading-tight">{currentScene.title}</h3>
                                </div>
                            </div>

                            {/* Scene Text */}
                            <p className="text-sm text-zinc-600 dark:text-zinc-300 leading-relaxed mb-6">{currentScene.text}</p>

                            {/* Choices */}
                            <div className="space-y-2.5">
                                {currentScene.choices.map((choice, index) => (
                                    <ChoiceButton
                                        key={index}
                                        choice={choice}
                                        gameState={gameState}
                                        visitedScenes={visitedScenes}
                                        onChoose={handleChoice}
                                        disabled={!!chosenText}
                                        chosen={chosenText === choice.text}
                                    />
                                ))}
                            </div>

                            {/* Inline Feedback */}
                            <AnimatePresence>
                                {feedbackState && (
                                    <InlineChoiceFeedback feedback={feedbackState} onComplete={handleFeedbackComplete} />
                                )}
                            </AnimatePresence>
                        </MotionDiv>
                    </AnimatePresence>
                </div>
            </div>
        </>
    );
};

// ─── ToolCard ────────────────────────────────────────────────────────────────

const ToolCard: React.FC<{title: string, description: string, icon: React.ElementType, onClick: () => void, disabled?: boolean, accentColor?: string}> =
({ title, description, icon: Icon, onClick, disabled = false, accentColor = 'text-purple-500' }) => (
    <MotionButton
        onClick={onClick}
        disabled={disabled}
        whileHover={{ scale: disabled ? 1 : 1.03 }}
        className={`w-full text-left p-6 rounded-2xl border-2 transition-all ${disabled ? 'bg-zinc-50 dark:bg-white/5 border-zinc-200 dark:border-white/10 opacity-50 cursor-not-allowed' : 'bg-white/50 dark:bg-white/10 border-zinc-200/80 dark:border-white/15 hover:border-purple-300 dark:hover:border-purple-500/50 cursor-pointer'}`}
    >
        <div className="flex items-center gap-4">
            <div className={`w-12 h-12 rounded-lg flex items-center justify-center ${disabled ? 'bg-zinc-200 dark:bg-white/10' : 'bg-purple-100 dark:bg-purple-900/50'}`}>
                <Icon size={24} className={disabled ? 'text-zinc-400 dark:text-zinc-600' : accentColor} />
            </div>
            <div>
                <h3 className="font-bold text-zinc-800 dark:text-white">{title}</h3>
                <p className="text-xs text-zinc-500 dark:text-zinc-400">{disabled ? "Coming Soon..." : description}</p>
            </div>
        </div>
    </MotionButton>
);

// ─── InnovationZone ──────────────────────────────────────────────────────────

const InnovationZone: React.FC<InnovationZoneProps> = ({ onBack, onSelectModule, user, autoOpenJourney, savedJourneyResult, onJourneyComplete }) => {
    const [activeTool, setActiveTool] = useState<string | null>(autoOpenJourney ? 'journey' : null);
    const [subjectProfile, setSubjectProfile] = useState<StudentSubjectProfile | null>(null);
    const [showOnboarding, setShowOnboarding] = useState(false);
    const [profileLoaded, setProfileLoaded] = useState(false);
    const [pendingToolId, setPendingToolId] = useState<string | null>(null);
    const [timetableCompletions, setTimetableCompletions] = useState<TimetableCompletions>({});
    const [timetableStreak, setTimetableStreak] = useState<TimetableStreak>({ currentStreak: 0, lastActiveDate: '', longestStreak: 0 });
    const [reflections, setReflections] = useState<StudyReflection[]>([]);
    const [pointsData, setPointsData] = useState<PointsData>({ totalEarned: 0, totalSpent: 0 });
    const [cosmeticUnlocks, setCosmeticUnlocks] = useState<CosmeticUnlocks>({ avatarSeeds: [], themeColors: [] });
    const [earnedRest, setEarnedRest] = useState<EarnedRest>({ skippedSessions: [], restDayPasses: [] });
    const [pendingCompletion, setPendingCompletion] = useState<{ dateKey: string; blockId: string; subjectName: string; sessionType: 'new-learning' | 'practice' | 'revision' } | null>(null);
    const [showRewardShop, setShowRewardShop] = useState(false);
    const [showJournal, setShowJournal] = useState(false);

    // Load subject profile from Firebase
    useEffect(() => {
        if (!user?.uid) { setProfileLoaded(true); return; }
        const loadProfile = async () => {
            try {
                const progressDoc = await getDoc(doc(db, 'progress', user.uid));
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
                    if (data.pointsData) {
                        setPointsData(data.pointsData as PointsData);
                    }
                    if (data.cosmeticUnlocks) {
                        setCosmeticUnlocks(data.cosmeticUnlocks as CosmeticUnlocks);
                    }
                    if (data.earnedRest) {
                        setEarnedRest(data.earnedRest as EarnedRest);
                    }
                }
            } catch (e) {
                console.error('Failed to load subject profile:', e);
            }
            setProfileLoaded(true);
        };
        loadProfile();
    }, [user?.uid]);

    // Handle onboarding completion — save to Firebase and auto-open pending tool
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
            } catch (e) {
                console.error('Failed to save subject profile:', e);
            }
        }
    }, [user?.uid, pendingToolId]);

    // Compute streak multiplier from current streak
    const getStreakMultiplier = useCallback((streak: number): number => {
        if (streak >= 14) return 2.5;
        if (streak >= 7) return 2.0;
        if (streak >= 3) return 1.5;
        return 1.0;
    }, []);

    // Core toggle logic (used directly for unchecking, or after reflection for completing)
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
                }, { merge: true }).catch(e => console.error('Failed to save completions:', e));
            }

            return updated;
        });
    }, [subjectProfile?.restDays, timetableStreak.longestStreak, user?.uid, earnedRest.restDayPasses]);

    // Handle timetable session toggle — gates completions through reflection modal
    const handleToggleCompletion = useCallback(async (dateKey: string, blockId: string, completed: boolean) => {
        if (completed) {
            // Parse blockId format: "SubjectName|sessionType|blockIndex"
            const parts = blockId.split('|');
            const subjectName = parts[0];
            const sessionType = (parts[1] || 'new-learning') as 'new-learning' | 'practice' | 'revision';
            setPendingCompletion({ dateKey, blockId, subjectName, sessionType });
        } else {
            // Unchecking — proceed directly
            executeToggle(dateKey, blockId, false);
        }
    }, [executeToggle]);

    // Handle reflection submission — calculates points and completes the block
    const handleReflectionSubmit = useCallback((reflectionText: string) => {
        if (!pendingCompletion) return;
        const { dateKey, blockId, subjectName, sessionType } = pendingCompletion;

        const basePoints = 10;
        const multiplier = getStreakMultiplier(timetableStreak.currentStreak);
        const earned = Math.round(basePoints * multiplier);

        const newReflection: StudyReflection = {
            dateKey,
            blockId,
            subjectName,
            sessionType,
            reflection: reflectionText,
            pointsEarned: earned,
            timestamp: Date.now(),
        };

        const updatedReflections = [...reflections, newReflection];
        const updatedPointsData: PointsData = {
            totalEarned: pointsData.totalEarned + earned,
            totalSpent: pointsData.totalSpent,
        };

        setReflections(updatedReflections);
        setPointsData(updatedPointsData);
        setPendingCompletion(null);

        // Check for perfect day bonus after this completion
        // We need to check after the toggle completes, so we pass extra data
        executeToggle(dateKey, blockId, true, {
            reflections: updatedReflections,
            pointsData: updatedPointsData,
        });
    }, [pendingCompletion, timetableStreak.currentStreak, reflections, pointsData, getStreakMultiplier, executeToggle]);

    // Handle spending points in the reward shop
    const handleSpendPoints = useCallback((type: 'skip-session' | 'rest-day-pass' | 'unlock-avatar' | 'unlock-theme', detail?: string) => {
        const costs: Record<string, number> = {
            'skip-session': 20,
            'rest-day-pass': 60,
            'unlock-avatar': 50,
            'unlock-theme': 40,
        };
        const cost = costs[type];
        const balance = pointsData.totalEarned - pointsData.totalSpent;
        if (balance < cost) return;

        const updatedPointsData: PointsData = {
            totalEarned: pointsData.totalEarned,
            totalSpent: pointsData.totalSpent + cost,
        };
        setPointsData(updatedPointsData);

        const todayKey = toDateKey(new Date());
        let updatedEarnedRest = earnedRest;
        let updatedCosmeticUnlocks = cosmeticUnlocks;

        if (type === 'skip-session' && detail) {
            updatedEarnedRest = {
                ...earnedRest,
                skippedSessions: [...earnedRest.skippedSessions, detail],
            };
            setEarnedRest(updatedEarnedRest);
        } else if (type === 'rest-day-pass') {
            updatedEarnedRest = {
                ...earnedRest,
                restDayPasses: [...earnedRest.restDayPasses, todayKey],
            };
            setEarnedRest(updatedEarnedRest);
        } else if (type === 'unlock-avatar' && detail) {
            updatedCosmeticUnlocks = {
                ...cosmeticUnlocks,
                avatarSeeds: [...cosmeticUnlocks.avatarSeeds, detail],
            };
            setCosmeticUnlocks(updatedCosmeticUnlocks);
        } else if (type === 'unlock-theme' && detail) {
            updatedCosmeticUnlocks = {
                ...cosmeticUnlocks,
                themeColors: [...cosmeticUnlocks.themeColors, detail],
            };
            setCosmeticUnlocks(updatedCosmeticUnlocks);
        }

        if (user?.uid) {
            setDoc(doc(db, 'progress', user.uid), {
                pointsData: updatedPointsData,
                earnedRest: updatedEarnedRest,
                cosmeticUnlocks: updatedCosmeticUnlocks,
            }, { merge: true }).catch(e => console.error('Failed to save purchase:', e));
        }
    }, [pointsData, earnedRest, cosmeticUnlocks, user?.uid]);

    // Tool click gate: if tool needs subjects and no profile exists, show onboarding
    const handleToolClick = useCallback((toolId: string, needsProfile: boolean) => {
        if (needsProfile && !profileLoaded) return; // still loading from Firebase
        if (needsProfile && !subjectProfile) {
            setPendingToolId(toolId);
            setShowOnboarding(true);
            return;
        }
        setActiveTool(toolId);
    }, [subjectProfile, profileLoaded]);

    // Compute today's skippable blocks for the reward shop
    const skippableBlocks = useMemo(() => {
        if (!subjectProfile) return [];
        const today = new Date();
        const todayKey = toDateKey(today);
        const jsDay = today.getDay();
        const todayDayIndex = jsDay === 0 ? 6 : jsDay - 1;

        const priorities = computeSubjectPriorities(subjectProfile.subjects);
        const weeksUntilExam = computeWeeksUntilExam(subjectProfile.examStartDate);
        const allocations = allocateSessions(priorities, weeksUntilExam);
        const restDaysArray = subjectProfile.restDays || [];
        const timetable = generateWeeklyTimetable(allocations, weeksUntilExam, 0, restDaysArray);
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
        { id: 'journey', title: 'Academic Journey Simulator', description: 'Navigate the choices of your final school year.', icon: GitBranch, needsProfile: false, component: <AcademicJourneyGame onSelectModule={onSelectModule} user={user} savedJourneyResult={savedJourneyResult} onJourneyComplete={onJourneyComplete} /> },
        { id: 'cao-simulator', title: 'CAO Points Simulator', description: 'Explore how grade changes affect your CAO points.', icon: Calculator, needsProfile: true, component: subjectProfile ? <CAOPointsSimulator profile={subjectProfile} onOpenSettings={() => setShowOnboarding(true)} /> : null },
        { id: 'focus', title: 'Deep Focus Timer', description: 'Pomodoro timer tied to your study timetable.', icon: Clock, needsProfile: false, component: <DeepFocusTimer profile={subjectProfile ?? undefined} completions={timetableCompletions} onToggleCompletion={handleToggleCompletion} /> },
        { id: 'planner', title: 'Spaced Repetition Timetable', description: 'A data-driven study planner powered by your subject goals.', icon: CalendarDays, needsProfile: true, component: subjectProfile ? <SpacedRepetitionTimetable profile={subjectProfile} onOpenSettings={() => setShowOnboarding(true)} completions={timetableCompletions} streak={timetableStreak} onToggleCompletion={handleToggleCompletion} points={pointsData.totalEarned - pointsData.totalSpent} onOpenShop={() => setShowRewardShop(true)} onOpenJournal={() => setShowJournal(true)} skippedSessions={earnedRest.skippedSessions} onRestDaysChange={async (days) => { const updated = { ...subjectProfile, restDays: days }; setSubjectProfile(updated); if (user?.uid) { try { await setDoc(doc(db, 'progress', user.uid), { subjectProfile: updated }, { merge: true }); } catch (e) { console.error('Failed to save rest days:', e); } } }} /> : null },
    ];

    const currentTool = tools.find(t => t.id === activeTool);

  return (
    <div className="min-h-screen bg-zinc-50 dark:bg-zinc-950 transition-colors duration-500 overflow-x-hidden relative flex flex-col items-center pt-32 pb-24">

      <header className="fixed top-0 left-0 right-0 z-[60] bg-zinc-50 dark:bg-zinc-950 border-b border-zinc-200 dark:border-zinc-800 px-10 py-6">
        <div className="container mx-auto flex items-center justify-between">
          <div className="flex items-center gap-8">
            <MotionButton whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }} onClick={onBack} className="p-2.5 rounded-lg bg-white dark:bg-zinc-900 border border-zinc-200 dark:border-zinc-800 transition-colors hover:bg-zinc-100 dark:hover:bg-zinc-800">
              <ArrowLeft size={18} className="text-zinc-900 dark:text-white" />
            </MotionButton>
            <div className="h-10 w-px bg-zinc-200 dark:bg-zinc-800" />
            <div>
              <p className="font-mono text-[9px] font-bold text-zinc-400 dark:text-zinc-500 uppercase tracking-[0.25em] mb-1">Explore</p>
              <h1 className="font-serif font-semibold text-2xl tracking-tight text-zinc-900 dark:text-white">The Innovation Zone</h1>
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
            <div className="w-12 h-12 bg-purple-500 dark:bg-purple-400 rounded-xl flex items-center justify-center text-white">
              <Lightbulb size={24} strokeWidth={1.5} />
            </div>
          </div>
        </div>
      </header>

      <main className="flex-grow w-full max-w-4xl px-6 pt-16 relative z-10">
         <AnimatePresence mode="wait">
            {!activeTool ? (
                <MotionDiv
                    key="tool-grid"
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    exit={{ opacity: 0 }}
                >
                    <div className="text-center mb-12">
                        <h2 className="font-serif text-5xl font-semibold text-zinc-900 dark:text-white">Experimental Tools</h2>
                        <p className="max-w-xl mx-auto mt-4 text-zinc-500 dark:text-zinc-400">A collection of interactive simulations and utilities designed to help you master the key concepts from the Learning Lab.</p>
                    </div>
                    <div className="space-y-4">
                        {tools.map(tool => (
                            <ToolCard
                                key={tool.id}
                                title={tool.title}
                                description={tool.description}
                                icon={tool.icon}
                                onClick={() => !tool.disabled && !(tool.needsProfile && !profileLoaded) && handleToolClick(tool.id, tool.needsProfile)}
                                disabled={tool.disabled || (tool.needsProfile && !profileLoaded)}
                            />
                        ))}
                    </div>
                </MotionDiv>
            ) : (
                <MotionDiv
                    key="active-tool"
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    exit={{ opacity: 0 }}
                >
                    <MotionButton onClick={() => setActiveTool(null)} className="flex items-center gap-2 text-sm font-bold text-zinc-500 dark:text-zinc-400 hover:text-zinc-900 dark:hover:text-white mb-8">
                        <ArrowLeft size={16} /> Back to Tools
                    </MotionButton>
                    {currentTool?.component}
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

      {/* Reflection Modal */}
      <ReflectionModal
        isOpen={!!pendingCompletion}
        subjectName={pendingCompletion?.subjectName ?? ''}
        sessionType={pendingCompletion?.sessionType ?? 'new-learning'}
        basePoints={10}
        streakMultiplier={getStreakMultiplier(timetableStreak.currentStreak)}
        onSubmit={handleReflectionSubmit}
        onCancel={() => setPendingCompletion(null)}
      />

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
      />
    </div>
  );
};
export default InnovationZone;
