
/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React, { useState, useEffect, useCallback, useRef, useMemo } from 'react';
import { createPortal } from 'react-dom';
import { motion, AnimatePresence } from 'framer-motion';
import {
    ArrowLeft, ArrowRight, Zap, Clock, Shield, RotateCcw,
    TrendingUp, Users, BookOpen, BookMarked,
    Lock, Compass, Brain, HandHelping, Target, ArrowUpRight, Award, Megaphone,
    Flame, Scale, GraduationCap, Settings, CalendarDays, Calculator, Layers, GitBranch, Wrench, Gift
} from 'lucide-react';
import { doc, setDoc, getDoc } from 'firebase/firestore';
import { db } from '../firebase';
import { type StudentSubjectProfile, type TimetableCompletions, type TimetableStreak, type StudyBlock, getBlockId, toDateKey } from './subjectData';
import { computeStreak, computeSubjectPriorities, allocateSessions, generateWeeklyTimetable, computeWeeksUntilExam } from './timetableAlgorithm';
import { type StudyReflection, type PointsData, type CosmeticUnlocks, type EarnedRest, type UserSettings } from '../types';
import SubjectOnboarding from './SubjectOnboarding';
import SpacedRepetitionTimetable from './SpacedRepetitionTimetable';
import CAOPointsSimulator from './CAOPointsSimulator';

import FlashcardSystem from './FlashcardSystem';
import { type FlashcardData } from './FlashcardSystem';
import ReflectionModal from './ReflectionModal';
import StudyJournalModal from './StudyJournalModal';
import RewardShopModal from './RewardShopModal';
import {
    type GameState, type Choice, type Scene, type HistoryItem, type StatKey, type Phase,
    type Mood, type Location,
    STORY_DATA, ROUTE_RESOLVERS, INITIAL_GAME_STATE, PHASE_METADATA,
    ARCHETYPES, STAT_TO_MODULES, STAT_LABELS,
    WEAKEST_STAT_INSIGHTS,
    getStatGrade, getKeyTurningPoints, getWeakestStat,
} from './journeySimulatorData';

const MotionDiv = motion.div as any;
const MotionButton = motion.button as any;
const MotionSpan = motion.span as any;
const MotionPolygon = motion.polygon as any;

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
  settings: UserSettings;
  updateSetting: <K extends keyof UserSettings>(key: K, value: UserSettings[K]) => void;
  onCosmeticUnlocksChange?: (unlocks: CosmeticUnlocks) => void;
}

const STAT_ICONS: Record<StatKey, React.ElementType> = {
    energy: Zap,
    academicCap: TrendingUp,
    socialSupport: Users,
    systemSavvy: BookOpen,
    resilience: Shield,
};

// ─── Location Config (label only) ───────────────────────────────────────────

const LOCATION_CONFIG: Record<Location, { label: string }> = {
    school: { label: 'School' },
    home: { label: 'Home' },
    'exam-hall': { label: 'Exam Hall' },
    library: { label: 'Library' },
    social: { label: 'Social' },
    work: { label: 'Work' },
    online: { label: 'Online' },
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

// ─── Pentagon Radar Helpers ─────────────────────────────────────────────────

const pentagonPoints = (cx: number, cy: number, r: number): string => {
    return Array.from({ length: 5 }, (_, i) => {
        const angle = (Math.PI * 2 * i) / 5 - Math.PI / 2;
        return `${cx + r * Math.cos(angle)},${cy + r * Math.sin(angle)}`;
    }).join(' ');
};

const statPentagonPoints = (stats: GameState, cx: number, cy: number, maxR: number): string => {
    const keys: StatKey[] = ['energy', 'academicCap', 'socialSupport', 'systemSavvy', 'resilience'];
    return keys.map((stat, i) => {
        const angle = (Math.PI * 2 * i) / 5 - Math.PI / 2;
        const r = (stats[stat] / 100) * maxR;
        return `${cx + r * Math.cos(angle)},${cy + r * Math.sin(angle)}`;
    }).join(' ');
};

// ─── Scene transition easing ────────────────────────────────────────────────

const editorialEase = [0.22, 1, 0.36, 1];

// ─── EphemeralStatOverlay ────────────────────────────────────────────────────

const EphemeralStatOverlay: React.FC<{ effects: Partial<GameState>; gameState: GameState }> = ({ effects, gameState }) => (
    <MotionDiv
        initial={{ opacity: 0, x: 20 }}
        animate={{ opacity: 1, x: 0 }}
        exit={{ opacity: 0, x: 20 }}
        className="fixed top-32 right-4 z-[90] flex items-center gap-5
                   bg-white/90 dark:bg-zinc-900/90 backdrop-blur-sm
                   border border-zinc-200 dark:border-white/10 rounded-full px-5 py-2.5 shadow-sm"
    >
        {(Object.keys(effects) as StatKey[]).map(stat => {
            const delta = effects[stat] as number;
            const Icon = STAT_ICONS[stat];
            return (
                <div key={stat} className="flex items-center gap-2">
                    <Icon size={14} className="text-zinc-400 dark:text-zinc-500" />
                    <span className="text-xs font-bold text-zinc-500 dark:text-zinc-400">{gameState[stat]}</span>
                    <span className={`font-mono text-xs font-black ${delta >= 0 ? 'text-emerald-600 dark:text-emerald-400' : 'text-rose-600 dark:text-rose-400'}`}>
                        {delta >= 0 ? '+' : ''}{delta}
                    </span>
                </div>
            );
        })}
    </MotionDiv>
);

// ─── PhaseTransition (editorial) ────────────────────────────────────────────

const PhaseTransition: React.FC<{ phase: Phase; onComplete: () => void }> = ({ phase, onComplete }) => {
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
            className="cursor-pointer min-h-[70vh] flex flex-col items-center justify-center text-center py-16"
        >
            <MotionDiv
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.2 }}
                className="space-y-4"
            >
                <p className="font-mono text-[10px] font-bold uppercase tracking-[0.3em] text-[var(--accent-hex)]">
                    {meta?.months}
                </p>
                <div className="w-16 h-px bg-[var(--accent-hex)] mx-auto" />
                <h2 className="font-serif text-5xl sm:text-6xl font-semibold text-zinc-900 dark:text-white">
                    {phase}
                </h2>
                <p className="text-lg text-zinc-500 dark:text-zinc-400 max-w-md mx-auto">
                    {meta?.subtitle}
                </p>
            </MotionDiv>

            <MotionDiv
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: 1 }}
                className="mt-12"
            >
                <p className="font-mono text-[10px] text-zinc-400 dark:text-zinc-500 uppercase tracking-[0.2em]">Click to continue</p>
            </MotionDiv>
        </MotionDiv>
    );
};

// ─── Typing Text ────────────────────────────────────────────────────────────

const TypingText: React.FC<{ text: string; sceneId: string }> = ({ text, sceneId }) => {
    const words = text.split(' ');
    const [visibleCount, setVisibleCount] = useState(0);
    const intervalRef = useRef<ReturnType<typeof setInterval> | null>(null);

    useEffect(() => {
        setVisibleCount(0);
        intervalRef.current = setInterval(() => {
            setVisibleCount(prev => {
                if (prev >= words.length) {
                    if (intervalRef.current) clearInterval(intervalRef.current);
                    return prev;
                }
                return prev + 1;
            });
        }, 40);
        return () => { if (intervalRef.current) clearInterval(intervalRef.current); };
    }, [sceneId, words.length]);

    return (
        <div className="relative max-w-2xl border-l-2 border-[rgba(var(--accent),0.2)] dark:border-[rgba(var(--accent),0.15)] pl-5">
            <p className="text-lg text-zinc-600 dark:text-zinc-300 leading-relaxed mb-8">
                {words.map((word, i) => (
                    <MotionSpan
                        key={`${sceneId}-${i}`}
                        initial={false}
                        animate={{ opacity: i < visibleCount ? 1 : 0 }}
                        transition={{ duration: 0.15 }}
                        className="inline"
                    >
                        {word}{' '}
                    </MotionSpan>
                ))}
            </p>
        </div>
    );
};

// ─── Choice Button (editorial) ──────────────────────────────────────────────

const ChoiceButton: React.FC<{ choice: Choice; gameState: GameState; visitedScenes: string[]; onChoose: (choice: Choice) => void; disabled?: boolean; chosen?: boolean }> = ({ choice, gameState, visitedScenes, onChoose, disabled, chosen }) => {
    const statRequirementsMet = !choice.requires || choice.requires.every(r => gameState[r.stat] >= r.min);
    const visitRequirementsMet = !choice.requiresVisited || choice.requiresVisited.every(id => visitedScenes.includes(id));
    const isLocked = !statRequirementsMet || !visitRequirementsMet;

    if (isLocked) {
        return (
            <div className="py-5 border-t border-zinc-200 dark:border-white/10 opacity-40">
                <div className="flex items-center gap-3">
                    <Lock size={14} className="text-zinc-400 dark:text-zinc-500 flex-shrink-0" />
                    <p className="font-serif text-lg text-zinc-400 dark:text-zinc-500">{choice.text}</p>
                </div>
                {choice.requires && (
                    <p className="font-mono text-[11px] text-zinc-400 dark:text-zinc-500 mt-1.5 ml-7 uppercase tracking-wider">
                        Requires: {choice.requires.map(r => `${STAT_LABELS[r.stat]} ${r.min}+`).join(', ')}
                    </p>
                )}
            </div>
        );
    }

    if (disabled && !chosen) {
        return (
            <div className="py-5 border-t border-zinc-200 dark:border-white/10 opacity-30">
                <p className="font-serif text-lg text-zinc-400 dark:text-zinc-500">{choice.text}</p>
            </div>
        );
    }

    if (chosen) {
        return (
            <div className="py-5 border-t-2 border-[var(--accent-hex)]">
                <p className="font-serif text-lg text-[var(--accent-hex)]">{choice.text}</p>
            </div>
        );
    }

    return (
        <MotionButton
            onClick={() => onChoose(choice)}
            whileHover={{ x: 4 }}
            whileTap={{ scale: 0.99 }}
            className="w-full text-left py-5 border-t border-zinc-200 dark:border-white/10 transition-colors group"
        >
            <p className="font-serif text-lg text-zinc-700 dark:text-zinc-200 group-hover:text-[var(--accent-hex)] dark:group-hover:text-[var(--accent-hex)] transition-colors">{choice.text}</p>
            {choice.flavor && <p className="text-xs text-zinc-400 dark:text-zinc-500 mt-1 italic">{choice.flavor}</p>}
        </MotionButton>
    );
};

// ─── ReportCard (magazine editorial) ────────────────────────────────────────

const ReportCard: React.FC<{ endingId: string; gameState: GameState; history: HistoryItem[]; onRestart: () => void; onSelectModule?: (moduleId: string) => void }> = ({ endingId, gameState, history, onRestart, onSelectModule }) => {
    const archetype = ARCHETYPES[endingId];
    const endScene = STORY_DATA[endingId];
    const turningPoints = getKeyTurningPoints(history);
    const weakestStat = getWeakestStat(gameState);
    const recommendedModules = STAT_TO_MODULES[weakestStat];

    // Compute branching path tree data
    const pathNodes = history.map((item) => {
        return { title: item.scene.title, phase: item.scene.phase, month: item.scene.month, choiceText: item.choiceText };
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
        <MotionDiv initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="space-y-16">
            {/* A. Archetype Reveal — editorial hero */}
            <MotionDiv
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.8, ease: 'easeOut' }}
                className="min-h-[50vh] flex flex-col items-center justify-center text-center py-16"
            >
                <p className="font-mono text-[10px] font-bold uppercase tracking-[0.3em] text-[var(--accent-hex)] mb-4">Your Archetype</p>
                <h3 className="font-serif text-5xl sm:text-6xl font-semibold text-zinc-900 dark:text-white mb-6">
                    {archetype?.title || endScene?.title || 'Results Day'}
                </h3>
                <p className="text-lg text-zinc-600 dark:text-zinc-300 leading-relaxed max-w-lg mx-auto">
                    {archetype?.description || endScene?.text}
                </p>
            </MotionDiv>

            {/* B. Animated Pentagon Radar — monochrome */}
            <div className="-mt-4">
                <p className="font-mono text-[11px] font-bold uppercase tracking-[0.25em] text-zinc-400 dark:text-zinc-500 mb-2 text-center">Your Grades</p>
                <div className="flex justify-center">
                    <svg viewBox="0 0 400 330" className="w-full max-w-lg h-auto">
                        {[0.25, 0.5, 0.75, 1].map(scale => (
                            <polygon
                                key={scale}
                                points={pentagonPoints(200, 170, 110 * scale)}
                                fill="none"
                                stroke="currentColor"
                                strokeWidth="0.5"
                                className="text-zinc-200 dark:text-white/10"
                            />
                        ))}
                        <MotionPolygon
                            initial={{ opacity: 0 }}
                            animate={{ opacity: 1, points: statPentagonPoints(gameState, 200, 170, 110) }}
                            transition={{ duration: 1, ease: 'easeOut' }}
                            style={{ fill: 'rgba(var(--accent), 0.15)', stroke: 'var(--accent-hex)' }}
                            strokeWidth="2"
                        />
                        {(Object.keys(gameState) as StatKey[]).map((stat, i) => {
                            const angle = (Math.PI * 2 * i) / 5 - Math.PI / 2;
                            const lx = 200 + 140 * Math.cos(angle);
                            const ly = 170 + 140 * Math.sin(angle);
                            return (
                                <g key={stat}>
                                    <text x={lx} y={ly - 6} textAnchor="middle" dominantBaseline="middle"
                                        className="text-[15px] font-bold fill-current font-mono text-zinc-700 dark:text-zinc-200">
                                        {getStatGrade(gameState[stat]).letter}
                                    </text>
                                    <text x={lx} y={ly + 8} textAnchor="middle" dominantBaseline="middle"
                                        className="text-[9px] fill-current font-mono text-zinc-400 dark:text-zinc-500">
                                        {STAT_LABELS[stat]}
                                    </text>
                                </g>
                            );
                        })}
                    </svg>
                </div>
            </div>

            {/* B2. Weakest Stat Insight — editorial callout */}
            <div>
                <div className="w-12 h-px bg-[var(--accent-hex)] mb-6" />
                <p className="font-mono text-[11px] font-bold uppercase tracking-[0.25em] text-[var(--accent-hex)] mb-2">Your Biggest Vulnerability</p>
                <h4 className="font-serif text-2xl font-semibold text-zinc-900 dark:text-white mb-3">{STAT_LABELS[weakestStat]}</h4>
                <p className="text-zinc-600 dark:text-zinc-300 leading-relaxed max-w-2xl">
                    {WEAKEST_STAT_INSIGHTS[weakestStat]}
                </p>
            </div>

            {/* C. Key Turning Points — editorial */}
            {turningPoints.length > 0 && (
                <div>
                    <p className="font-mono text-[11px] font-bold uppercase tracking-[0.25em] text-zinc-400 dark:text-zinc-500 mb-6 text-center">Key Turning Points</p>
                    <div className="space-y-8">
                        {turningPoints.map((item, index) => (
                            <div key={index}>
                                <p className="font-mono text-[11px] font-bold uppercase tracking-[0.2em] text-[var(--accent-hex)] mb-1">{item.scene.month}</p>
                                <h5 className="font-serif text-xl font-semibold text-zinc-900 dark:text-white mb-1">{item.scene.title}</h5>
                                <p className="text-zinc-600 dark:text-zinc-400">{item.choiceText}</p>
                            </div>
                        ))}
                    </div>
                </div>
            )}

            {/* D. Paths Not Taken */}
            {pathsNotTaken.length > 0 && (
                <div>
                    <p className="font-mono text-[11px] font-bold uppercase tracking-[0.25em] text-zinc-400 dark:text-zinc-500 mb-6 text-center">Paths Not Taken</p>
                    <div className="space-y-4">
                        {pathsNotTaken.slice(0, 3).map((path, index) => (
                            <div key={index} className="border-t border-zinc-200 dark:border-white/10 pt-4">
                                <div className="flex items-center gap-2 mb-1">
                                    <Lock size={12} className="text-zinc-400 dark:text-zinc-500" />
                                    <p className="font-mono text-[11px] font-bold text-zinc-500 dark:text-zinc-400 uppercase tracking-wider">{path.sceneTitle}</p>
                                </div>
                                <p className="text-zinc-500 dark:text-zinc-400 italic">{path.choiceText}</p>
                                <p className="font-mono text-[10px] text-zinc-400 dark:text-zinc-500 mt-1 uppercase tracking-wider">Required: {path.requirement}</p>
                            </div>
                        ))}
                    </div>
                </div>
            )}

            {/* E. Recommended Modules */}
            <div>
                <p className="font-mono text-[11px] font-bold uppercase tracking-[0.25em] text-zinc-400 dark:text-zinc-500 mb-1 text-center">Recommended For You</p>
                <p className="text-xs text-zinc-400 dark:text-zinc-500 text-center mb-6">Based on your weakest area: {STAT_LABELS[weakestStat]}</p>
                <div className="space-y-0">
                    {recommendedModules.map(mod => (
                        <button
                            key={mod.moduleId}
                            onClick={() => onSelectModule?.(mod.moduleId)}
                            className="w-full text-left py-4 border-t border-zinc-200 dark:border-white/10 group transition-colors"
                        >
                            <div className="flex items-center justify-between">
                                <p className="font-serif text-lg text-zinc-700 dark:text-zinc-200 group-hover:text-[var(--accent-hex)] transition-colors">{mod.moduleTitle}</p>
                                <ArrowRight size={14} className="text-zinc-300 dark:text-zinc-600 group-hover:text-[var(--accent-hex)] transition-colors flex-shrink-0" />
                            </div>
                        </button>
                    ))}
                </div>
            </div>

            {/* F. Decision Path — monochrome vertical line */}
            <div>
                <p className="font-mono text-[11px] font-bold uppercase tracking-[0.25em] text-zinc-400 dark:text-zinc-500 mb-6 text-center">Your Path</p>
                <div className="relative pl-8">
                    <div className="absolute left-3 top-0 bottom-0 w-px bg-zinc-200 dark:bg-white/10" />

                    {groupedPath.map(({ phase, nodes }) => (
                        <div key={phase} className="mb-8">
                            <div className="flex items-center gap-2 mb-4 -ml-8">
                                <div className="w-6 h-6 rounded-full bg-[var(--accent-hex)] flex items-center justify-center ring-4 ring-white dark:ring-zinc-950">
                                    <div className="w-2 h-2 rounded-full bg-white" />
                                </div>
                                <span className="font-mono text-[10px] font-bold uppercase tracking-[0.2em] text-[var(--accent-hex)]">{phase}</span>
                            </div>

                            {nodes.map((node, ni) => (
                                <div key={ni} className="relative mb-4">
                                    <div className="absolute -left-8 top-1.5 w-6 h-6 flex items-center justify-center">
                                        <div className="w-2 h-2 rounded-full bg-zinc-300 dark:bg-zinc-600" />
                                    </div>
                                    <p className="font-mono text-[10px] text-zinc-400 dark:text-zinc-500 uppercase tracking-wider">{node.title}</p>
                                    <p className="text-sm text-[var(--accent-hex)] dark:text-[var(--accent-hex)] mt-0.5">{node.choiceText.length > 80 ? node.choiceText.slice(0, 78) + '...' : node.choiceText}</p>
                                </div>
                            ))}
                        </div>
                    ))}

                    <div className="relative -ml-8 flex items-center gap-2">
                        <div className="w-6 h-6 rounded-full bg-[var(--accent-hex)] flex items-center justify-center ring-4 ring-white dark:ring-zinc-950">
                            <div className="w-2 h-2 rounded-full bg-white" />
                        </div>
                        <span className="font-mono text-[10px] font-bold text-[var(--accent-hex)] uppercase tracking-wider">{archetype?.title || 'End'}</span>
                    </div>
                </div>
            </div>

            {/* Play Again */}
            <div className="text-center py-8">
                <button
                    onClick={onRestart}
                    className="font-mono text-[11px] font-bold uppercase tracking-[0.25em] text-[var(--accent-hex)] hover:text-[var(--accent-dark-hex)] dark:hover:text-[var(--accent-hex)] transition-colors"
                >
                    Play Again
                </button>
            </div>
        </MotionDiv>
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
    const [chosenText, setChosenText] = useState<string | null>(null);
    const [showStatOverlay, setShowStatOverlay] = useState(false);
    const [lastEffects, setLastEffects] = useState<Partial<GameState> | null>(null);
    const [lastModuleLink, setLastModuleLink] = useState<Choice['moduleLink'] | null>(null);
    const [previousResult, setPreviousResult] = useState<{ endingId: string; completedAt?: string; finalStats?: GameState } | null>(savedJourneyResult || null);
    const [showingSavedResult, setShowingSavedResult] = useState(!!savedJourneyResult);
    const hasSavedRef = useRef(false);
    const overlayTimerRef = useRef<ReturnType<typeof setTimeout> | null>(null);

    const currentScene = STORY_DATA[currentSceneId];
    const isEndScene = currentSceneId.startsWith('END_');

    // Load previous journey result from Firestore
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

    // Save journey result when game ends
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
        // Resolve route
        let targetSceneId = choice.nextSceneId;
        while (targetSceneId.startsWith('__') && ROUTE_RESOLVERS[targetSceneId]) {
            targetSceneId = ROUTE_RESOLVERS[targetSceneId](newGameState, newHistory);
        }

        setVisitedScenes(prev => [...prev, targetSceneId]);

        // Show ephemeral overlay, then advance
        setChosenText(choice.text);
        setLastEffects(choice.effects);
        setLastModuleLink(choice.moduleLink || null);
        setShowStatOverlay(true);
        setPendingSceneId(targetSceneId);

        // Clear overlay timer if one exists
        if (overlayTimerRef.current) clearTimeout(overlayTimerRef.current);

        overlayTimerRef.current = setTimeout(() => {
            setShowStatOverlay(false);
            setChosenText(null);
            setLastEffects(null);
            setLastModuleLink(null);

            const targetScene = STORY_DATA[targetSceneId];
            if (targetScene && targetScene.phase !== currentChoiceScene.phase) {
                setCurrentPhase(targetScene.phase);
                setShowPhaseTransition(true);
                // Keep pendingSceneId so handlePhaseTransitionComplete can advance
            } else {
                setCurrentSceneId(targetSceneId);
                setPendingSceneId(null);
            }
        }, 2500);
    }, [currentSceneId, gameState, history]);

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
        setChosenText(null);
        setShowStatOverlay(false);
        setLastEffects(null);
        setLastModuleLink(null);
        hasSavedRef.current = false;
        if (overlayTimerRef.current) clearTimeout(overlayTimerRef.current);
    }, []);

    // Saved result screen (editorial treatment)
    if (showingSavedResult && previousResult?.endingId && ARCHETYPES[previousResult.endingId]) {
        const savedArch = ARCHETYPES[previousResult.endingId];
        const savedStats = previousResult.finalStats || { ...INITIAL_GAME_STATE };
        const savedWeakestStat = getWeakestStat(savedStats);
        return (
            <MotionDiv initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="space-y-16">
                {/* Archetype — editorial hero */}
                <div className="min-h-[40vh] flex flex-col items-center justify-center text-center py-16">
                    <p className="font-mono text-[10px] font-bold uppercase tracking-[0.3em] text-[var(--accent-hex)] mb-4">Your Previous Result</p>
                    <h3 className="font-serif text-5xl sm:text-6xl font-semibold text-zinc-900 dark:text-white mb-6">{savedArch.title}</h3>
                    <p className="text-lg text-zinc-600 dark:text-zinc-300 leading-relaxed max-w-lg mx-auto">{savedArch.description}</p>
                </div>

                {/* Pentagon Radar — monochrome */}
                <div>
                    <p className="font-mono text-[11px] font-bold uppercase tracking-[0.25em] text-zinc-400 dark:text-zinc-500 mb-4 text-center">Your Grades</p>
                    <div className="flex justify-center">
                        <svg viewBox="0 0 400 330" className="w-full max-w-lg h-auto">
                            {[0.25, 0.5, 0.75, 1].map(scale => (
                                <polygon
                                    key={scale}
                                    points={pentagonPoints(200, 170, 110 * scale)}
                                    fill="none"
                                    stroke="currentColor"
                                    strokeWidth="0.5"
                                    className="text-zinc-200 dark:text-white/10"
                                />
                            ))}
                            <MotionPolygon
                                initial={{ opacity: 0 }}
                                animate={{ opacity: 1, points: statPentagonPoints(savedStats, 200, 170, 110) }}
                                transition={{ duration: 1, ease: 'easeOut' }}
                                style={{ fill: 'rgba(var(--accent), 0.15)', stroke: 'var(--accent-hex)' }}
                                strokeWidth="2"
                            />
                            {(Object.keys(savedStats) as StatKey[]).map((stat, i) => {
                                const angle = (Math.PI * 2 * i) / 5 - Math.PI / 2;
                                const lx = 200 + 140 * Math.cos(angle);
                                const ly = 170 + 140 * Math.sin(angle);
                                return (
                                    <g key={stat}>
                                        <text x={lx} y={ly - 6} textAnchor="middle" dominantBaseline="middle"
                                            className="text-[15px] font-bold fill-current font-mono text-zinc-700 dark:text-zinc-200">
                                            {getStatGrade(savedStats[stat]).letter}
                                        </text>
                                        <text x={lx} y={ly + 8} textAnchor="middle" dominantBaseline="middle"
                                            className="text-[9px] fill-current font-mono text-zinc-400 dark:text-zinc-500">
                                            {STAT_LABELS[stat]}
                                        </text>
                                    </g>
                                );
                            })}
                        </svg>
                    </div>
                </div>

                {/* Vulnerability — editorial callout */}
                <div>
                    <div className="w-12 h-px bg-[var(--accent-hex)] mb-6" />
                    <p className="font-mono text-[11px] font-bold uppercase tracking-[0.25em] text-[var(--accent-hex)] mb-2">Your Biggest Vulnerability</p>
                    <h4 className="font-serif text-2xl font-semibold text-zinc-900 dark:text-white mb-3">{STAT_LABELS[savedWeakestStat]}</h4>
                    <p className="text-zinc-600 dark:text-zinc-300 leading-relaxed max-w-2xl">
                        {WEAKEST_STAT_INSIGHTS[savedWeakestStat]}
                    </p>
                </div>

                {/* Recommended Modules */}
                <div>
                    <p className="font-mono text-[11px] font-bold uppercase tracking-[0.25em] text-zinc-400 dark:text-zinc-500 mb-1 text-center">Recommended For You</p>
                    <p className="text-xs text-zinc-400 dark:text-zinc-500 text-center mb-6">Based on your weakest area: {STAT_LABELS[savedWeakestStat]}</p>
                    <div className="space-y-0">
                        {STAT_TO_MODULES[savedWeakestStat].map(mod => (
                            <button
                                key={mod.moduleId}
                                onClick={() => onSelectModule?.(mod.moduleId)}
                                className="w-full text-left py-4 border-t border-zinc-200 dark:border-white/10 group transition-colors"
                            >
                                <div className="flex items-center justify-between">
                                    <p className="font-serif text-lg text-zinc-700 dark:text-zinc-200 group-hover:text-[var(--accent-hex)] transition-colors">{mod.moduleTitle}</p>
                                    <ArrowRight size={14} className="text-zinc-300 dark:text-zinc-600 group-hover:text-[var(--accent-hex)] transition-colors flex-shrink-0" />
                                </div>
                            </button>
                        ))}
                    </div>
                </div>

                {/* Play Again */}
                <div className="text-center py-8">
                    <button
                        onClick={() => { setShowingSavedResult(false); restartGame(); }}
                        className="font-mono text-[11px] font-bold uppercase tracking-[0.25em] text-[var(--accent-hex)] hover:text-[var(--accent-dark-hex)] dark:hover:text-[var(--accent-hex)] transition-colors"
                    >
                        Play Again
                    </button>
                </div>
            </MotionDiv>
        );
    }

    // End screen
    if (isEndScene) {
        return <ReportCard endingId={currentSceneId} gameState={gameState} history={history} onRestart={restartGame} onSelectModule={onSelectModule} />;
    }

    // Phase transition interstitial
    if (showPhaseTransition) {
        return (
            <AnimatePresence mode="wait">
                <PhaseTransition key={currentPhase} phase={currentPhase} onComplete={handlePhaseTransitionComplete} />
            </AnimatePresence>
        );
    }

    if (!currentScene || !currentScene.choices) {
        return null;
    }

    const locationConfig = LOCATION_CONFIG[currentScene.location];

    return (
        <>
            {/* Ephemeral Stat Overlay — portaled to body to escape Framer transform context */}
            {createPortal(
                <AnimatePresence>
                    {showStatOverlay && lastEffects && (
                        <EphemeralStatOverlay effects={lastEffects} gameState={gameState} />
                    )}
                </AnimatePresence>,
                document.body
            )}

            {/* Scene — editorial layout */}
            <div className="min-h-[60vh] flex flex-col justify-center py-8">
                <AnimatePresence mode="wait">
                    <MotionDiv
                        key={currentSceneId}
                        initial={{ opacity: 0, y: 40 }}
                        animate={{ opacity: 1, y: 0 }}
                        exit={{ opacity: 0, y: -20 }}
                        transition={{ duration: 0.5, ease: editorialEase }}
                    >
                        {/* Phase accent block */}
                        {(() => {
                            const meta = PHASE_METADATA.find(p => p.name === currentScene.phase);
                            return (
                                <div className="border-l-[3px] border-[var(--accent-hex)] pl-4 mb-6">
                                    <p className="font-mono text-[10px] font-bold uppercase tracking-[0.3em] text-[var(--accent-hex)]">{currentScene.phase}</p>
                                    <p className="font-mono text-[10px] uppercase tracking-[0.2em] text-zinc-400 dark:text-zinc-500 mt-0.5">{meta?.months}</p>
                                    <p className="text-sm text-zinc-500 dark:text-zinc-400 mt-1 leading-relaxed">{meta?.subtitle}</p>
                                </div>
                            );
                        })()}

                        {/* Month + Location */}
                        <p className="font-mono text-[11px] font-bold uppercase tracking-[0.25em] text-zinc-400 dark:text-zinc-500 mb-3">
                            {currentScene.month} — {locationConfig.label}
                        </p>

                        {/* Decorative rule */}
                        <div className="w-10 h-px bg-[rgba(var(--accent),0.4)] mb-5" />

                        {/* Title */}
                        <h2 className="font-serif text-4xl sm:text-5xl font-semibold text-zinc-900 dark:text-white leading-tight mb-6">{currentScene.title}</h2>

                        {/* Narrative */}
                        <TypingText
                            text={(() => {
                                if (currentScene.textVariants) {
                                    for (const v of currentScene.textVariants) {
                                        if ('stat' in v.condition) {
                                            const val = gameState[v.condition.stat];
                                            if (v.condition.min !== undefined && val < v.condition.min) continue;
                                            if (v.condition.max !== undefined && val > v.condition.max) continue;
                                            return v.text;
                                        }
                                        if ('visited' in v.condition && visitedScenes.includes(v.condition.visited)) {
                                            return v.text;
                                        }
                                    }
                                }
                                return currentScene.text;
                            })()}
                            sceneId={currentSceneId}
                        />

                        {/* Choices */}
                        <div>
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

                        {/* Module link footnote */}
                        {lastModuleLink && chosenText && (
                            <p className="text-xs italic text-zinc-500 dark:text-zinc-400 mt-4">
                                Related: <span className="text-[var(--accent-hex)] dark:text-[var(--accent-hex)]">{lastModuleLink.moduleTitle}</span>
                            </p>
                        )}

                        {/* Previous result badge at START */}
                        {currentSceneId === 'START' && previousResult && ARCHETYPES[previousResult.endingId] && (
                            <div className="mt-8 pt-6 border-t border-zinc-200 dark:border-white/10">
                                <p className="font-mono text-[10px] text-zinc-400 dark:text-zinc-500 uppercase tracking-wider">
                                    Previous result: <span className="text-[var(--accent-hex)] font-bold">{ARCHETYPES[previousResult.endingId].title}</span>
                                </p>
                            </div>
                        )}
                    </MotionDiv>
                </AnimatePresence>
            </div>
        </>
    );
};

// ─── ToolCard ────────────────────────────────────────────────────────────────

interface ToolCardProps {
    title: string;
    description: string;
    icon: React.ElementType;
    onClick: () => void;
    disabled?: boolean;
    tag: string;
    accentHex: string;
    gridClass: string;
    iconBg: string;
    iconColor: string;
    accentBarColor: string;
    tagBg: string;
    tagText: string;
    hoverBorder: string;
    index: number;
}

const ToolCard: React.FC<ToolCardProps> = ({
    title, description, icon: Icon, onClick, disabled = false,
    tag, accentHex, gridClass, iconBg, iconColor, accentBarColor,
    tagBg, tagText, hoverBorder, index,
}) => (
    <MotionDiv
        onClick={disabled ? undefined : onClick}
        initial={{ opacity: 0, y: 24 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.45, delay: index * 0.08, ease: [0.25, 0.46, 0.45, 0.94] }}
        className={`group relative flex flex-col rounded-2xl border-2 overflow-hidden transition-all duration-300 ${gridClass} ${
            disabled
                ? 'bg-zinc-50 dark:bg-white/5 border-zinc-200 dark:border-white/10 cursor-not-allowed'
                : `bg-white/60 dark:bg-white/[0.06] border-zinc-200/80 dark:border-white/10 ${hoverBorder} cursor-pointer hover:shadow-lg dark:hover:shadow-2xl`
        }`}
    >
        {/* Accent top bar */}
        <div className={`h-[3px] w-full transition-opacity duration-300 ${disabled ? 'opacity-0' : 'opacity-0 group-hover:opacity-100'} ${accentBarColor}`} />

        {/* Radial hover glow */}
        {!disabled && (
            <div
                className="pointer-events-none absolute inset-0 opacity-0 group-hover:opacity-100 transition-opacity duration-500"
                style={{ background: `radial-gradient(ellipse at 50% 0%, ${accentHex}15 0%, transparent 70%)` }}
            />
        )}

        <div className="relative flex flex-col flex-grow p-5 md:p-6">
            {/* Icon + Tag row */}
            <div className="flex items-start justify-between mb-4">
                <div className={`w-14 h-14 rounded-xl flex items-center justify-center transition-transform duration-300 group-hover:scale-110 ${
                    disabled ? 'bg-zinc-200 dark:bg-white/10' : iconBg
                }`}>
                    {disabled
                        ? <Lock size={24} className="text-zinc-400 dark:text-zinc-600" />
                        : <Icon size={26} className={iconColor} />
                    }
                </div>
                <span className={`text-[10px] font-mono font-bold uppercase tracking-wider px-2.5 py-1 rounded-full ${
                    disabled ? 'bg-zinc-200 dark:bg-white/10 text-zinc-400 dark:text-zinc-600' : `${tagBg} ${tagText}`
                }`}>
                    {disabled ? 'Needs Profile' : tag}
                </span>
            </div>

            {/* Title + Description */}
            <h3 className={`font-serif font-semibold text-base md:text-lg tracking-tight mb-1.5 ${
                disabled ? 'text-zinc-400 dark:text-zinc-600' : 'text-zinc-800 dark:text-white'
            }`}>{title}</h3>
            <p className={`text-xs leading-relaxed flex-grow ${
                disabled ? 'text-zinc-400 dark:text-zinc-600' : 'text-zinc-500 dark:text-zinc-400'
            }`}>{disabled ? 'Complete your Subject Profile to unlock this tool.' : description}</p>

            {/* Footer */}
            <div className={`mt-4 pt-3 border-t flex items-center justify-between ${
                disabled ? 'border-zinc-200 dark:border-white/5' : 'border-zinc-200/60 dark:border-white/10'
            }`}>
                <span className={`font-mono text-[10px] uppercase tracking-wider ${
                    disabled ? 'text-zinc-300 dark:text-zinc-700' : 'text-zinc-400 dark:text-zinc-500'
                }`}>
                    {disabled ? 'Locked' : 'Launch Tool'}
                </span>
                {!disabled && (
                    <ArrowRight size={14} className="text-zinc-300 dark:text-zinc-600 opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
                )}
            </div>
        </div>
    </MotionDiv>
);

// ─── InnovationZone ──────────────────────────────────────────────────────────

const InnovationZone: React.FC<InnovationZoneProps> = ({ onBack, onSelectModule, user, autoOpenJourney, savedJourneyResult, onJourneyComplete, settings, updateSetting, onCosmeticUnlocksChange }) => {
    const [activeTool, setActiveTool] = useState<string | null>(autoOpenJourney ? 'journey' : null);
    const [subjectProfile, setSubjectProfile] = useState<StudentSubjectProfile | null>(null);
    const [showOnboarding, setShowOnboarding] = useState(false);
    const [profileLoaded, setProfileLoaded] = useState(false);
    const [pendingToolId, setPendingToolId] = useState<string | null>(null);
    const [timetableCompletions, setTimetableCompletions] = useState<TimetableCompletions>({});
    const [timetableStreak, setTimetableStreak] = useState<TimetableStreak>({ currentStreak: 0, lastActiveDate: '', longestStreak: 0 });
    const [reflections, setReflections] = useState<StudyReflection[]>([]);
    const [pointsData, setPointsData] = useState<PointsData>({ totalEarned: 0, totalSpent: 0 });
    const [cosmeticUnlocks, setCosmeticUnlocks] = useState<CosmeticUnlocks>({ avatarSeeds: [], themeColors: [], cardStyles: [] });
    const [earnedRest, setEarnedRest] = useState<EarnedRest>({ skippedSessions: [], restDayPasses: [] });

    // Refs to always access latest state in callbacks (avoids stale closures)
    const pointsDataRef = useRef(pointsData);
    pointsDataRef.current = pointsData;
    const cosmeticUnlocksRef = useRef(cosmeticUnlocks);
    cosmeticUnlocksRef.current = cosmeticUnlocks;
    const earnedRestRef = useRef(earnedRest);
    earnedRestRef.current = earnedRest;
    const onCosmeticUnlocksChangeRef = useRef(onCosmeticUnlocksChange);
    onCosmeticUnlocksChangeRef.current = onCosmeticUnlocksChange;
    const [pendingCompletion, setPendingCompletion] = useState<{ dateKey: string; blockId: string; subjectName: string; sessionType: 'new-learning' | 'practice' | 'revision' } | null>(null);
    const [showRewardShop, setShowRewardShop] = useState(false);
    const [showJournal, setShowJournal] = useState(false);
    const [flashcardData, setFlashcardData] = useState<FlashcardData>({ decks: [], reviewStreak: { currentStreak: 0, longestStreak: 0, lastReviewDate: '' }, reviewHistory: {} });
    const [showPointsExplainer, setShowPointsExplainer] = useState(() => {
        try { return !localStorage.getItem('nextstep-points-explainer-v2'); } catch { return true; }
    });

    const dismissPointsExplainer = useCallback(() => {
        setShowPointsExplainer(false);
        try { localStorage.setItem('nextstep-points-explainer-v2', '1'); } catch {}
    }, []);

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
                    if (data.flashcardDecks) {
                        setFlashcardData(data.flashcardDecks as FlashcardData);
                    }
                }
            } catch (e) {
                console.error('Failed to load subject profile:', e);
            }
            setProfileLoaded(true);
        };
        loadProfile();
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
            } catch (e) {
                console.error('Failed to save subject profile:', e);
            }
        }
    }, [user?.uid, pendingToolId]);

    const getStreakMultiplier = useCallback((streak: number): number => {
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
                }, { merge: true }).catch(e => console.error('Failed to save completions:', e));
            }

            return updated;
        });
    }, [subjectProfile?.restDays, timetableStreak.longestStreak, user?.uid, earnedRest.restDayPasses]);

    const handleToggleCompletion = useCallback(async (dateKey: string, blockId: string, completed: boolean) => {
        if (completed) {
            const parts = blockId.split('|');
            const subjectName = parts[0];
            const sessionType = (parts[1] || 'new-learning') as 'new-learning' | 'practice' | 'revision';
            setPendingCompletion({ dateKey, blockId, subjectName, sessionType });
        } else {
            executeToggle(dateKey, blockId, false);
        }
    }, [executeToggle]);

    const handleReflectionSubmit = useCallback((reflectionText: string, quality?: { tier: 'basic' | 'thoughtful' | 'deep' }) => {
        if (!pendingCompletion) return;
        const { dateKey, blockId, subjectName, sessionType } = pendingCompletion;

        // Tiered points based on reflection quality
        const tierPoints: Record<string, number> = { basic: 10, thoughtful: 15, deep: 20 };
        const basePoints = tierPoints[quality?.tier ?? 'basic'] ?? 10;
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

        executeToggle(dateKey, blockId, true, {
            reflections: updatedReflections,
            pointsData: updatedPointsData,
        });
    }, [pendingCompletion, timetableStreak.currentStreak, reflections, pointsData, getStreakMultiplier, executeToggle]);

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
                pointsData: updatedPointsData,
                earnedRest: updatedEarnedRest,
                cosmeticUnlocks: updatedCosmeticUnlocks,
            }, { merge: true }).catch(e => {
                console.error('Failed to save purchase:', e);
                // Roll back to latest ref values (may have changed since write started)
                setPointsData(currentPoints);
                setEarnedRest(currentEarnedRest);
                setCosmeticUnlocks(currentCosmeticUnlocks);
                onCosmeticUnlocksChangeRef.current?.(currentCosmeticUnlocks);
            });
        }
    }, [user?.uid]);

    const handleFlashcardDataChange = useCallback((newData: FlashcardData) => {
        setFlashcardData(newData);
        if (user?.uid) {
            setDoc(doc(db, 'progress', user.uid), { flashcardDecks: newData }, { merge: true })
                .catch(e => console.error('Failed to save flashcard data:', e));
        }
    }, [user?.uid]);

    const handleFlashcardPointsEarn = useCallback((earned: number) => {
        const updatedPointsData: PointsData = {
            totalEarned: pointsData.totalEarned + earned,
            totalSpent: pointsData.totalSpent,
        };
        setPointsData(updatedPointsData);
        if (user?.uid) {
            setDoc(doc(db, 'progress', user.uid), { pointsData: updatedPointsData }, { merge: true })
                .catch(e => console.error('Failed to save flashcard points:', e));
        }
    }, [pointsData, user?.uid]);

    const handleToolClick = useCallback((toolId: string, needsProfile: boolean) => {
        if (needsProfile && !profileLoaded) return;
        if (needsProfile && !subjectProfile) {
            setPendingToolId(toolId);
            setShowOnboarding(true);
            return;
        }
        setActiveTool(toolId);
    }, [subjectProfile, profileLoaded]);

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
            component: subjectProfile ? <CAOPointsSimulator profile={subjectProfile} onOpenSettings={() => setShowOnboarding(true)} /> : null,
        },
        {
            id: 'flashcards', title: 'Flashcard Studio', description: 'Create and review flashcards with spaced repetition scheduling.', icon: Layers, needsProfile: false,
            tag: 'Studio', accentHex: 'var(--accent-hex)', gridClass: 'md:col-span-2',
            iconBg: 'bg-[rgba(var(--accent),0.1)] dark:bg-[rgba(var(--accent),0.2)]', iconColor: 'text-[var(--accent-hex)]',
            accentBarColor: 'bg-[var(--accent-hex)]', tagBg: 'bg-[rgba(var(--accent),0.1)] dark:bg-[rgba(var(--accent),0.2)]', tagText: 'text-[var(--accent-hex)]',
            hoverBorder: 'hover:border-[rgba(var(--accent),0.4)] dark:hover:border-[rgba(var(--accent),0.5)]',
            component: <FlashcardSystem data={flashcardData} onDataChange={handleFlashcardDataChange} onPointsEarn={handleFlashcardPointsEarn} subjectNames={subjectProfile?.subjects.map(s => s.subjectName)} />,
        },
        {
            id: 'planner', title: 'Spaced Repetition Timetable', description: 'A data-driven study planner powered by your subject goals.', icon: CalendarDays, needsProfile: true,
            tag: 'Planner', accentHex: '#6366f1', gridClass: 'md:col-span-2',
            iconBg: 'bg-indigo-100 dark:bg-indigo-900/30', iconColor: 'text-indigo-600 dark:text-indigo-400',
            accentBarColor: 'bg-indigo-500', tagBg: 'bg-indigo-100 dark:bg-indigo-900/30', tagText: 'text-indigo-700 dark:text-indigo-400',
            hoverBorder: 'hover:border-indigo-400/50 dark:hover:border-indigo-500/40',
            component: subjectProfile ? <SpacedRepetitionTimetable profile={subjectProfile} onOpenSettings={() => setShowOnboarding(true)} completions={timetableCompletions} streak={timetableStreak} onToggleCompletion={handleToggleCompletion} points={pointsData.totalEarned - pointsData.totalSpent} onOpenShop={() => setShowRewardShop(true)} onOpenJournal={() => setShowJournal(true)} skippedSessions={earnedRest.skippedSessions} onRestDaysChange={async (days) => { const updated = { ...subjectProfile, restDays: days }; setSubjectProfile(updated); if (user?.uid) { try { await setDoc(doc(db, 'progress', user.uid), { subjectProfile: updated }, { merge: true }); } catch (e) { console.error('Failed to save rest days:', e); } } }} /> : null,
        },
    ];

    const currentTool = tools.find(t => t.id === activeTool);

  return (
    <div className="min-h-screen bg-zinc-50 dark:bg-zinc-950 transition-colors duration-500 overflow-x-hidden relative flex flex-col items-center pt-24 md:pt-32 pb-36 md:pb-24">

      <header className="fixed top-0 left-0 right-0 z-[60] bg-zinc-50 dark:bg-zinc-950 border-b border-zinc-200 dark:border-zinc-800 px-4 py-4 md:px-10 md:py-6">
        <div className="container mx-auto flex items-center justify-between">
          <div className="flex items-center gap-4 md:gap-8">
            <MotionButton whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }} onClick={onBack} className="p-2.5 rounded-xl bg-white dark:bg-zinc-900 border border-zinc-200 dark:border-zinc-800 transition-colors hover:bg-zinc-100 dark:hover:bg-zinc-800 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[rgba(var(--accent),0.5)]">
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
                    <div className="grid grid-cols-1 md:grid-cols-8 gap-4 md:gap-6">
                        {tools.slice(0, 2).map((tool, i) => (
                            <ToolCard
                                key={tool.id}
                                title={tool.title}
                                description={tool.description}
                                icon={tool.icon}
                                onClick={() => !(tool as any).disabled && !(tool.needsProfile && !profileLoaded) && handleToolClick(tool.id, tool.needsProfile)}
                                disabled={(tool as any).disabled || (tool.needsProfile && !profileLoaded)}
                                tag={tool.tag}
                                accentHex={tool.accentHex}
                                gridClass={tool.gridClass}
                                iconBg={tool.iconBg}
                                iconColor={tool.iconColor}
                                accentBarColor={tool.accentBarColor}
                                tagBg={tool.tagBg}
                                tagText={tool.tagText}
                                hoverBorder={tool.hoverBorder}
                                index={i}
                            />
                        ))}

                        {/* Shop Bento Card */}
                        <MotionDiv
                            initial={{ opacity: 0, y: 24 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ duration: 0.45, delay: 2 * 0.08, ease: [0.25, 0.46, 0.45, 0.94] }}
                            onClick={() => setShowRewardShop(true)}
                            className="md:col-span-2 md:row-span-2 group relative cursor-pointer flex flex-col rounded-2xl border-2 border-zinc-200/80 dark:border-white/10 hover:border-purple-400/50 dark:hover:border-purple-500/40 overflow-hidden bg-gradient-to-b from-purple-50/80 via-white to-white dark:from-purple-950/30 dark:via-zinc-900/80 dark:to-zinc-900 transition-all hover:shadow-lg dark:hover:shadow-2xl"
                        >
                            <div className="h-[3px] w-full bg-gradient-to-r from-purple-500 via-fuchsia-500 to-pink-500 opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
                            <div
                                className="pointer-events-none absolute inset-0 opacity-0 group-hover:opacity-100 transition-opacity duration-500"
                                style={{ background: 'radial-gradient(ellipse at 50% 0%, rgba(147,51,234,0.08) 0%, transparent 70%)' }}
                            />
                            <div className="relative flex flex-col flex-grow items-center justify-center p-5 md:p-6 text-center">
                                <div className="mb-3 md:mb-4 px-3 py-1.5 rounded-full bg-amber-100 dark:bg-amber-900/30 flex items-center gap-1.5">
                                    <Zap size={12} className="text-amber-500" />
                                    <span className="text-xs font-bold text-amber-700 dark:text-amber-400">{pointsData.totalEarned - pointsData.totalSpent} pts</span>
                                </div>
                                <div className="w-14 h-14 rounded-xl bg-purple-100 dark:bg-purple-900/30 flex items-center justify-center mb-3 transition-transform duration-300 group-hover:scale-110">
                                    <Gift size={26} className="text-purple-600 dark:text-purple-400" />
                                </div>
                                <h3 className="font-serif font-semibold text-base md:text-lg tracking-tight text-zinc-800 dark:text-white mb-1">Reward Shop</h3>
                                <p className="text-xs text-zinc-500 dark:text-zinc-400 leading-relaxed">Spend points on avatars, themes & card styles</p>
                                <div className="mt-3 md:mt-4 pt-3 border-t border-zinc-100 dark:border-white/[0.06] w-full flex items-center justify-center gap-1.5 text-xs font-bold text-purple-600 dark:text-purple-400 group-hover:gap-2.5 transition-all">
                                    Browse <ArrowRight size={12} />
                                </div>
                            </div>
                        </MotionDiv>

                        {tools.slice(2).map((tool, i) => (
                            <ToolCard
                                key={tool.id}
                                title={tool.title}
                                description={tool.description}
                                icon={tool.icon}
                                onClick={() => !(tool as any).disabled && !(tool.needsProfile && !profileLoaded) && handleToolClick(tool.id, tool.needsProfile)}
                                disabled={(tool as any).disabled || (tool.needsProfile && !profileLoaded)}
                                tag={tool.tag}
                                accentHex={tool.accentHex}
                                gridClass={tool.gridClass}
                                iconBg={tool.iconBg}
                                iconColor={tool.iconColor}
                                accentBarColor={tool.accentBarColor}
                                tagBg={tool.tagBg}
                                tagText={tool.tagText}
                                hoverBorder={tool.hoverBorder}
                                index={i + 3}
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
                    <MotionButton onClick={() => setActiveTool(null)} className="flex items-center gap-2 text-sm font-bold text-zinc-500 dark:text-zinc-400 hover:text-zinc-900 dark:hover:text-white mb-2">
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
