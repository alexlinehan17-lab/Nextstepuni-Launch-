/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { ArrowLeft, BookOpen, Target, RotateCcw, Play, Pause, Clock, Sparkles, Zap, X, ChevronRight, Brain, Repeat, Shuffle, HelpCircle, Compass, Sprout, Shield, Radar, ClipboardCheck, Trophy } from 'lucide-react';
import { type SessionUser } from '../Auth';
import { type StudentSubjectProfile } from '../subjectData';
import { type UserProgress, type StrategyMasteryMap, type MasteryTier } from '../../types';
import { type CourseData } from '../Library';
import { STRATEGY_REGISTRY } from '../../studySessionData';
import { type StreakData } from '../../hooks/useStreak';
import { useStudySession } from '../../hooks/useStudySession';
import { getSubjectColor, getSubjectStroke, DURATION_PRESETS } from '../../studySessionData';
import StrategyPickerStep from './StrategyPickerStep';
import ReflectionModal from '../ReflectionModal';
import { scoreReflection, REFLECTION_TIER_POINTS } from '../ReflectionModal';
import { type WeeklyChallengeState } from '../../hooks/useWeeklyChallenge';

const MotionDiv = motion.div as any;

const TIER_COLORS: Record<MasteryTier, { text: string; bar: string }> = {
  none: { text: 'text-zinc-400 dark:text-zinc-500', bar: 'bg-zinc-200 dark:bg-zinc-700' },
  learned: { text: 'text-blue-500', bar: 'bg-blue-500' },
  practiced: { text: 'text-teal-500', bar: 'bg-teal-500' },
  applied: { text: 'text-amber-500', bar: 'bg-amber-500' },
  habitual: { text: 'text-purple-500', bar: 'bg-purple-500' },
};

const TIER_LABELS: Record<MasteryTier, string> = {
  none: 'Not Started', learned: 'Learned', practiced: 'Practiced', applied: 'Applied', habitual: 'Habitual',
};

const TIER_ORDER: MasteryTier[] = ['learned', 'practiced', 'applied', 'habitual'];

const STRATEGY_ICONS: Record<string, React.ElementType> = {
  'mastering-active-recall-protocol': Brain,
  'mastering-spaced-repetition-protocol': Repeat,
  'mastering-interleaving-protocol': Shuffle,
  'elaborative-interrogation-protocol': HelpCircle,
  'agency-protocol': Compass,
  'growth-mindset-protocol': Sprout,
  'digital-distraction-protocol': Shield,
  'learning-radar-protocol': Radar,
  'exam-hall-strategies-protocol': ClipboardCheck,
};

const SESSION_TYPE_CONFIG: Record<string, { icon: React.ElementType; label: string }> = {
  'new-learning': { icon: BookOpen, label: 'New Learning' },
  'practice': { icon: Target, label: 'Practice' },
  'revision': { icon: RotateCcw, label: 'Revision' },
};

interface StudySessionViewProps {
  user: SessionUser;
  studentProfile: StudentSubjectProfile | null;
  userProgress: UserProgress;
  allCourses: CourseData[];
  pointsReload: () => void;
  streak: StreakData;
  onBack: () => void;
  onStrategyMasteryRecompute?: () => Promise<void>;
  strategyMastery?: StrategyMasteryMap;
  onGoToTrainingHub?: () => void;
  dismissedGuides?: Record<string, string>;
  onDismissGuide?: (id: string) => void;
  weeklyChallenge?: WeeklyChallengeState;
}

const StudySessionView: React.FC<StudySessionViewProps> = ({
  user,
  studentProfile,
  userProgress,
  allCourses,
  pointsReload,
  streak,
  onBack,
  onStrategyMasteryRecompute,
  strategyMastery,
  onGoToTrainingHub,
  dismissedGuides,
  onDismissGuide,
  weeklyChallenge,
}) => {
  const session = useStudySession(user.uid, userProgress, allCourses);

  // Setup selections
  const [selectedSubject, setSelectedSubject] = useState('');
  const [selectedType, setSelectedType] = useState<'new-learning' | 'practice' | 'revision' | ''>('');
  const [selectedMinutes, setSelectedMinutes] = useState<number>(0);

  // Strategy picker
  const [pickerDone, setPickerDone] = useState(false);
  const [selectedStrategies, setSelectedStrategies] = useState<string[]>([]);

  // Reflection modal
  const [reflectionOpen, setReflectionOpen] = useState(false);
  const [isSaving, setIsSaving] = useState(false);

  const subjects = studentProfile?.subjects ?? [];

  const learnedStrategyIds = STRATEGY_REGISTRY
    .filter(s => {
      const course = allCourses.find(c => c.id === s.moduleId);
      const progress = userProgress[s.moduleId];
      return course && progress && progress.unlockedSection >= course.sectionsCount;
    })
    .map(s => s.moduleId);

  const canStart = selectedSubject && selectedType && selectedMinutes > 0;

  const handleStart = () => {
    if (!canStart || !selectedType) return;
    session.startSession(selectedSubject, selectedType, selectedMinutes);
  };

  const handleSaveWithReflection = async (reflectionText: string) => {
    const quality = scoreReflection(reflectionText);
    const bonus = REFLECTION_TIER_POINTS[quality.tier];
    setIsSaving(true);
    await session.saveSession(bonus, selectedStrategies);
    pointsReload();
    onStrategyMasteryRecompute?.();
    weeklyChallenge?.reload();
    setReflectionOpen(false);
    setIsSaving(false);
    setPickerDone(false);
    setSelectedStrategies([]);
    session.resetSession();
  };

  const handleSkipReflection = async () => {
    setIsSaving(true);
    await session.saveSession(0, selectedStrategies);
    pointsReload();
    onStrategyMasteryRecompute?.();
    weeklyChallenge?.reload();
    setIsSaving(false);
    setPickerDone(false);
    setSelectedStrategies([]);
    session.resetSession();
  };

  // ── Format time ──
  const formatTime = (seconds: number) => {
    const m = Math.floor(seconds / 60);
    const s = seconds % 60;
    return `${m.toString().padStart(2, '0')}:${s.toString().padStart(2, '0')}`;
  };

  // ── SVG ring calculations ──
  const ringRadius = 120;
  const ringCircumference = 2 * Math.PI * ringRadius;
  const progress = session.totalDuration > 0 ? session.elapsedSeconds / session.totalDuration : 0;
  const ringOffset = ringCircumference * (1 - progress);
  const timeRemaining = Math.max(0, session.totalDuration - session.elapsedSeconds);

  // ── SETUP PHASE ──
  if (session.phase === 'idle') {
    return (
      <div className="min-h-screen bg-zinc-50 dark:bg-zinc-950 flex flex-col">
        {/* Header — minimal */}
        <div className="shrink-0 px-6 pt-6 pb-2">
          <button onClick={onBack} className="p-2 -ml-2 rounded-xl hover:bg-zinc-100 dark:hover:bg-zinc-800/60 transition-colors">
            <ArrowLeft size={20} className="text-zinc-400" />
          </button>
        </div>

        {/* Centered content */}
        <div className="flex-1 flex items-center justify-center px-6 pb-28">
          <div className="w-full max-w-md space-y-10">
            {/* First-visit intro card */}
            <AnimatePresence>
              {!dismissedGuides?.['study-session-intro'] && (
                <MotionDiv
                  key="study-session-intro"
                  initial={{ opacity: 0, y: -8 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: -8, transition: { duration: 0.2 } }}
                  className="bg-[rgba(var(--accent),0.04)] border border-[rgba(var(--accent),0.15)] rounded-2xl p-5 mb-6"
                >
                  <div className="flex items-start gap-3">
                    <Sparkles size={18} className="text-[rgba(var(--accent),1)] shrink-0 mt-0.5" />
                    <div className="space-y-2">
                      <p className="font-semibold text-sm text-zinc-800 dark:text-white">Welcome to Study Sessions</p>
                      <p className="text-sm text-zinc-600 dark:text-zinc-400 leading-relaxed">
                        During sessions you'll see strategy prompts from modules you've completed. Tap "Done" to track your engagement — this feeds your mastery progress visible below.
                      </p>
                      <button
                        onClick={() => onDismissGuide?.('study-session-intro')}
                        className="mt-1 text-sm font-medium text-[rgba(var(--accent),1)] hover:underline"
                      >
                        Got it
                      </button>
                    </div>
                  </div>
                </MotionDiv>
              )}
            </AnimatePresence>
            {/* Title + today summary */}
            <div className="text-center space-y-3">
              <h1 className="text-3xl font-bold text-zinc-800 dark:text-white tracking-tight">Study Session</h1>
              {session.todaySessions.length > 0 ? (
                <p className="text-sm text-zinc-400 dark:text-zinc-500">
                  {session.todaySessions.length} session{session.todaySessions.length !== 1 ? 's' : ''} today &middot; {session.todayTotalMinutes} min total
                </p>
              ) : (
                <p className="text-sm text-zinc-400 dark:text-zinc-500">Choose a subject and start studying</p>
              )}
            </div>

            {/* Subject picker */}
            <div className="space-y-3">
              <p className="text-[11px] font-semibold uppercase tracking-[0.15em] text-zinc-400 dark:text-zinc-500">Subject</p>
              <div className="flex flex-wrap gap-2">
                {subjects.map(s => {
                  const colors = getSubjectColor(s.subjectName);
                  const isActive = selectedSubject === s.subjectName;
                  return (
                    <button
                      key={s.subjectName}
                      onClick={() => setSelectedSubject(s.subjectName)}
                      className={`inline-flex items-center gap-2 px-4 py-2.5 rounded-full text-[13px] font-medium transition-all ${
                        isActive
                          ? `${colors.bg} ${colors.text} shadow-sm ring-1 ring-inset`
                          : 'bg-white dark:bg-zinc-900 text-zinc-500 dark:text-zinc-400 hover:bg-zinc-100 dark:hover:bg-zinc-800/60'
                      }`}
                      style={isActive ? { ['--tw-ring-color' as any]: 'rgba(var(--accent), 0.25)' } : undefined}
                    >
                      <span className={`w-2 h-2 rounded-full shrink-0 ${colors.dot}`} />
                      {s.subjectName}
                    </button>
                  );
                })}
                {subjects.length === 0 && (
                  <p className="text-sm text-zinc-400 dark:text-zinc-500">No subjects set up yet. Complete onboarding first.</p>
                )}
              </div>
            </div>

            {/* Session type + Duration — side by side */}
            <div className="grid grid-cols-2 gap-8">
              {/* Session type */}
              <div className="space-y-3">
                <p className="text-[11px] font-semibold uppercase tracking-[0.15em] text-zinc-400 dark:text-zinc-500">Type</p>
                <div className="space-y-2">
                  {(['new-learning', 'practice', 'revision'] as const).map(type => {
                    const config = SESSION_TYPE_CONFIG[type];
                    const Icon = config.icon;
                    const isActive = selectedType === type;
                    return (
                      <button
                        key={type}
                        onClick={() => setSelectedType(type)}
                        className={`w-full flex items-center gap-3 px-4 py-3 rounded-xl text-[13px] font-medium transition-all ${
                          isActive
                            ? 'bg-[rgba(var(--accent),0.08)] text-[var(--accent-hex)] shadow-sm ring-1 ring-inset ring-[rgba(var(--accent),0.2)]'
                            : 'bg-white dark:bg-zinc-900 text-zinc-500 dark:text-zinc-400 hover:bg-zinc-100 dark:hover:bg-zinc-800/60'
                        }`}
                      >
                        <Icon size={16} strokeWidth={isActive ? 2 : 1.5} />
                        <span>{config.label}</span>
                      </button>
                    );
                  })}
                </div>
              </div>

              {/* Duration */}
              <div className="space-y-3">
                <p className="text-[11px] font-semibold uppercase tracking-[0.15em] text-zinc-400 dark:text-zinc-500">Duration</p>
                <div className="space-y-2">
                  {DURATION_PRESETS.map(preset => {
                    const isActive = selectedMinutes === preset.minutes;
                    return (
                      <button
                        key={preset.minutes}
                        onClick={() => setSelectedMinutes(preset.minutes)}
                        className={`w-full flex items-center justify-center px-4 py-3 rounded-xl text-[13px] font-semibold transition-all ${
                          isActive
                            ? 'bg-[rgba(var(--accent),0.08)] text-[var(--accent-hex)] shadow-sm ring-1 ring-inset ring-[rgba(var(--accent),0.2)]'
                            : 'bg-white dark:bg-zinc-900 text-zinc-500 dark:text-zinc-400 hover:bg-zinc-100 dark:hover:bg-zinc-800/60'
                        }`}
                      >
                        {preset.minutes} min
                      </button>
                    );
                  })}
                </div>
              </div>
            </div>

            {/* Start button */}
            <button
              onClick={handleStart}
              disabled={!canStart}
              className={`w-full py-4 rounded-2xl text-[15px] font-bold tracking-wide transition-all ${
                canStart
                  ? 'bg-[var(--accent-hex)] text-white shadow-lg shadow-[rgba(var(--accent),0.2)] hover:shadow-[rgba(var(--accent),0.35)] active:scale-[0.98]'
                  : 'bg-zinc-100 dark:bg-zinc-900 text-zinc-300 dark:text-zinc-700 cursor-not-allowed'
              }`}
            >
              Start Session
            </button>

            {/* Strategy Mastery Summary */}
            {strategyMastery && Object.keys(strategyMastery).length > 0 && (
              <div className="space-y-3">
                <p className="text-[11px] font-semibold uppercase tracking-[0.15em] text-zinc-400 dark:text-zinc-500">Strategy Mastery</p>
                <div className="space-y-2">
                  {STRATEGY_REGISTRY.map(strategy => {
                    const record = strategyMastery[strategy.moduleId];
                    const tier = record?.tier ?? 'none';
                    const tierIndex = TIER_ORDER.indexOf(tier);
                    const colors = TIER_COLORS[tier];
                    const Icon = STRATEGY_ICONS[strategy.moduleId] || Brain;

                    return (
                      <div key={strategy.moduleId} className="flex items-center gap-3">
                        <Icon size={14} className={colors.text} />
                        <span className="text-xs font-medium text-zinc-600 dark:text-zinc-400 w-24 truncate">{strategy.strategyName}</span>
                        <div className="flex-1 grid grid-cols-4 gap-0.5">
                          {TIER_ORDER.map((t, i) => (
                            <div
                              key={t}
                              className={`h-1.5 rounded-full ${i <= tierIndex ? (
                                t === 'learned' ? 'bg-blue-500'
                                : t === 'practiced' ? 'bg-teal-500'
                                : t === 'applied' ? 'bg-amber-500'
                                : 'bg-purple-500'
                              ) : 'bg-zinc-200 dark:bg-zinc-700'}`}
                            />
                          ))}
                        </div>
                        <span className={`text-[10px] font-semibold w-16 text-right ${colors.text}`}>{TIER_LABELS[tier]}</span>
                      </div>
                    );
                  })}
                </div>
                {onGoToTrainingHub && (
                  <button
                    onClick={onGoToTrainingHub}
                    className="w-full flex items-center justify-center gap-1.5 py-2.5 rounded-xl text-xs font-medium text-zinc-500 dark:text-zinc-400 hover:bg-zinc-100 dark:hover:bg-zinc-800/50 transition-colors"
                  >
                    View all in Training Hub
                    <ChevronRight size={12} />
                  </button>
                )}
              </div>
            )}
          </div>
        </div>
      </div>
    );
  }

  // ── ACTIVE / PAUSED PHASE ──
  if (session.phase === 'active' || session.phase === 'paused') {
    const subjectColors = getSubjectColor(session.subject);
    const strokeColor = getSubjectStroke(session.subject);
    const typeConfig = SESSION_TYPE_CONFIG[session.sessionType];

    const handleQuit = () => {
      if (window.confirm('End this session and go back? Any time studied will be lost.')) {
        session.endSession();
        session.resetSession();
      }
    };

    return (
      <div className="fixed inset-0 z-[100] bg-zinc-950 flex flex-col items-center justify-center">
        {/* Subject + type pill */}
        <div className="absolute top-8 left-0 right-0 flex justify-center">
          <div className={`inline-flex items-center gap-2 px-4 py-2 rounded-full ${subjectColors.bg} ${subjectColors.border} border`}>
            <span className={`w-2 h-2 rounded-full ${subjectColors.dot}`} />
            <span className={`text-sm font-semibold ${subjectColors.text}`}>{session.subject}</span>
            <span className="text-zinc-400 dark:text-zinc-500 mx-1">·</span>
            <span className="text-sm text-zinc-400 dark:text-zinc-400">{typeConfig.label}</span>
          </div>
        </div>

        {/* Circular countdown ring */}
        <div className="relative w-72 h-72 flex items-center justify-center">
          <svg className="w-full h-full -rotate-90" viewBox="0 0 280 280">
            {/* Background ring */}
            <circle
              cx="140" cy="140" r={ringRadius}
              fill="none"
              strokeWidth="6"
              className="stroke-zinc-800"
            />
            {/* Progress ring */}
            <motion.circle
              cx="140" cy="140" r={ringRadius}
              fill="none"
              strokeWidth="6"
              strokeLinecap="round"
              className={strokeColor}
              strokeDasharray={ringCircumference}
              strokeDashoffset={ringOffset}
              style={{ transition: 'stroke-dashoffset 0.5s ease' }}
            />
          </svg>
          {/* Time display */}
          <div className="absolute inset-0 flex flex-col items-center justify-center">
            <span className="text-5xl font-bold text-white tabular-nums tracking-tight">
              {formatTime(timeRemaining)}
            </span>
            <span className="text-sm text-zinc-500 mt-1">remaining</span>
          </div>
        </div>

        {/* Controls */}
        <div className="flex flex-col items-center gap-4 mt-8">
          <button
            onClick={session.phase === 'active' ? session.pauseSession : session.resumeSession}
            className="w-16 h-16 rounded-full bg-white/10 hover:bg-white/15 flex items-center justify-center transition-colors"
          >
            {session.phase === 'active' ? (
              <Pause size={28} className="text-white" />
            ) : (
              <Play size={28} className="text-white ml-1" />
            )}
          </button>
          <button
            onClick={session.endSession}
            className="px-6 py-2.5 rounded-full bg-white/10 hover:bg-white/15 text-sm font-semibold text-zinc-300 hover:text-white transition-colors"
          >
            End Early
          </button>
        </div>

        {/* Strategy prompt card */}
        <AnimatePresence mode="wait">
          {session.currentPrompt && (
            <MotionDiv
              key={session.currentPrompt.phase}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -10 }}
              transition={{ duration: 0.4, ease: [0.16, 1, 0.3, 1] }}
              className="absolute bottom-12 left-4 right-4 max-w-md mx-auto"
            >
              <div className="bg-zinc-900 border border-zinc-800 rounded-xl p-4 shadow-2xl">
                <div className="flex items-center gap-2 mb-2">
                  <Sparkles size={14} className="text-amber-400" />
                  <span className="text-xs font-bold uppercase tracking-widest text-amber-400">
                    {session.currentPrompt.strategyName}
                  </span>
                </div>
                <p className="text-sm text-zinc-300 leading-relaxed">
                  {session.currentPrompt.prompt}
                </p>
                <div className="flex items-center gap-3 mt-3">
                  <button
                    onClick={session.completePrompt}
                    className="text-xs font-semibold text-teal-400 hover:text-teal-300 transition-colors"
                  >
                    Done
                  </button>
                  <button
                    onClick={() => session.setCurrentPrompt(null)}
                    className="text-xs text-zinc-500 hover:text-zinc-400 transition-colors"
                  >
                    Skip
                  </button>
                </div>
              </div>
            </MotionDiv>
          )}
        </AnimatePresence>

        {/* Paused overlay */}
        {session.phase === 'paused' && (
          <div className="absolute inset-0 bg-zinc-950/60 flex items-center justify-center pointer-events-none">
            <span className="text-2xl font-bold text-white/50">Paused</span>
          </div>
        )}
      </div>
    );
  }

  // ── COMPLETE PHASE ──
  if (session.phase === 'complete') {
    // Show strategy picker before stats if student has learned strategies
    if (!pickerDone && learnedStrategyIds.length > 0) {
      return (
        <StrategyPickerStep
          learnedStrategyIds={learnedStrategyIds}
          autoTrackedIds={session.getTrackedStrategies()}
          onContinue={(ids) => {
            setSelectedStrategies(ids);
            setPickerDone(true);
          }}
        />
      );
    }

    const subjectColors = getSubjectColor(session.subject);
    const typeConfig = SESSION_TYPE_CONFIG[session.sessionType];
    const actualMinutes = Math.round(session.elapsedSeconds / 60);

    return (
      <div className="min-h-screen bg-zinc-50 dark:bg-zinc-950 flex flex-col items-center justify-center px-4">
        <MotionDiv
          initial={{ scale: 0.9, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          transition={{ duration: 0.5, ease: [0.16, 1, 0.3, 1] }}
          className="w-full max-w-sm space-y-6"
        >
          {/* Header */}
          <div className="text-center">
            <div className="inline-flex items-center justify-center w-16 h-16 rounded-2xl bg-amber-50 dark:bg-amber-500/10 mb-4">
              <Sparkles size={32} className="text-amber-500" />
            </div>
            <h2 className="text-2xl font-bold text-zinc-800 dark:text-white">Session Complete!</h2>
          </div>

          {/* Stats card */}
          <div className="bg-white dark:bg-zinc-900 border border-zinc-200/60 dark:border-white/[0.06] rounded-xl p-5 space-y-3">
            <div className="flex items-center justify-between">
              <span className="text-sm text-zinc-500">Duration</span>
              <span className="text-sm font-bold text-zinc-800 dark:text-white">{actualMinutes} min</span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-sm text-zinc-500">Subject</span>
              <div className="flex items-center gap-2">
                <span className={`w-2 h-2 rounded-full ${subjectColors.dot}`} />
                <span className="text-sm font-medium text-zinc-800 dark:text-white">{session.subject}</span>
              </div>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-sm text-zinc-500">Type</span>
              <span className="text-sm font-medium text-zinc-800 dark:text-white">{typeConfig.label}</span>
            </div>
            <div className="border-t border-zinc-100 dark:border-zinc-800 pt-3 flex items-center justify-between">
              <span className="text-sm text-zinc-500">Points Earned</span>
              <span className="text-base font-bold text-[var(--accent-hex)]">+{session.basePointsEarned}</span>
            </div>
          </div>

          {/* Weekly Challenge nudge */}
          {weeklyChallenge?.isLoaded && !weeklyChallenge?.isClaimed && (
            <div className="flex items-center gap-3 p-3 rounded-xl bg-amber-50 dark:bg-amber-900/20 border border-amber-200/60 dark:border-amber-800/30">
              <Trophy size={16} className="text-amber-500 shrink-0" />
              <div className="flex-1 min-w-0">
                <p className="text-xs font-semibold text-zinc-700 dark:text-zinc-300 truncate">
                  Weekly Challenge: {weeklyChallenge.challenge.title}
                </p>
                <div className="flex items-center gap-2 mt-1">
                  <div className="flex-1 h-1.5 bg-amber-200 dark:bg-amber-800/40 rounded-full overflow-hidden">
                    <div
                      className="h-full bg-amber-500 rounded-full transition-all duration-500"
                      style={{ width: `${Math.min(100, Math.round((weeklyChallenge.current / weeklyChallenge.challenge.target) * 100))}%` }}
                    />
                  </div>
                  <span className="text-[10px] font-bold text-amber-600 dark:text-amber-400 tabular-nums">
                    {weeklyChallenge.current}/{weeklyChallenge.challenge.target}
                  </span>
                </div>
              </div>
            </div>
          )}

          {/* Actions */}
          <div className="space-y-3">
            <button
              onClick={() => setReflectionOpen(true)}
              disabled={isSaving}
              className="w-full py-3.5 rounded-xl text-sm font-bold bg-[var(--accent-hex)] text-white shadow-lg shadow-[rgba(var(--accent),0.25)] hover:shadow-[rgba(var(--accent),0.4)] active:scale-[0.98] transition-all disabled:opacity-50"
            >
              Write a Reflection (+10-20 pts)
            </button>
            <button
              onClick={handleSkipReflection}
              disabled={isSaving}
              className="w-full py-3 rounded-xl text-sm font-medium text-zinc-500 hover:text-zinc-700 dark:hover:text-zinc-300 hover:bg-zinc-100 dark:hover:bg-zinc-800/50 transition-all disabled:opacity-50"
            >
              {isSaving ? 'Saving...' : 'Skip'}
            </button>
          </div>
        </MotionDiv>

        {/* Reflection Modal */}
        <ReflectionModal
          isOpen={reflectionOpen}
          subjectName={session.subject}
          sessionType={session.sessionType}
          basePoints={session.basePointsEarned + REFLECTION_TIER_POINTS.basic}
          streakMultiplier={1}
          onSubmit={(text) => handleSaveWithReflection(text)}
          onCancel={() => setReflectionOpen(false)}
        />
      </div>
    );
  }

  return null;
};

export default StudySessionView;
