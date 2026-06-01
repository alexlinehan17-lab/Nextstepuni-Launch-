/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState, useEffect, useCallback, useMemo } from 'react';
import { createPortal } from 'react-dom';
import { useToast } from './Toast';
import { AnimatePresence } from 'framer-motion';
import { MotionButton, MotionDiv } from './Motion';
import {
  Compass, ChevronRight, ChevronLeft, SlidersHorizontal,
  MapPin, Briefcase, Heart, Star, RotateCcw,
  BookmarkPlus, Check, ArrowUpRight, TrendingUp, X, Clock, Eye,
  type LucideIcon,
} from 'lucide-react';
import PrimaryActionButton from './ui/PrimaryActionButton';
import { COLORS } from '../design/tokens';
import { db } from '../firebase';
import { doc, getDoc, setDoc } from 'firebase/firestore';
import { type StudentSubjectProfile, LC_SUBJECTS, getPointsForGrade } from './subjectData';
import { INSTITUTIONS, REGIONS, type CAOCourse, getCoursePageUrl } from './futureFinderData';
import {
  runFutureFinderAssessment,
  ASSESSMENT_QUESTIONS,
  type FutureFinderAnswers,
  type RecommendationResult,
  type AssessmentQuestion,
} from './futureFinderAlgorithm';
import { useAuth } from '../contexts/AuthContext';
import { runSubjectExplorerMatch, type ClusterMatchResult } from './subjectExplorerData';

// ─── Types ──────────────────────────────────────────────────────────────────

interface FutureFinderProps {
  uid: string;
  profile: StudentSubjectProfile;
}

interface FutureFinderData {
  completedAt: string;
  answers: FutureFinderAnswers;
  topPicks: string[];
  savedComparisons: string[][];
  compareCodes?: string[];
}

type Phase = 'intro' | 'assessment' | 'results' | 'detail' | 'compare';

type SortMode = 'match' | 'points' | 'institution';

// ─── Default Answers ────────────────────────────────────────────────────────

function getDefaultAnswers(): FutureFinderAnswers {
  return {
    interestTags: [],
    scenarioChoices: [],
    salaryImportance: 3,
    jobSecurityImportance: 3,
    helpingOthersImportance: 3,
    workStyleTags: [],
    teamPreference: 'mix',
    studyDuration: [],
    willingToRelocate: true,
    preferredRegions: [],
    estimatedPoints: 350,
  };
}

// ─── Helpers ────────────────────────────────────────────────────────────────

/** Compute best-six CAO points from the student's current grades */
function computeCurrentPoints(profile: StudentSubjectProfile): number {
  const allPoints = profile.subjects.map(s => {
    const isMaths = LC_SUBJECTS.find(lc => lc.name === s.subjectName)?.isMaths || false;
    return getPointsForGrade(s.currentGrade, isMaths);
  }).sort((a, b) => b - a);
  return allPoints.slice(0, 6).reduce((sum, p) => sum + p, 0);
}

/** Migrate old answer format to new */
function migrateAnswers(answers: any): FutureFinderAnswers {
  const migrated = { ...getDefaultAnswers(), ...answers };

  // Migration: old preferredLevels -> new studyDuration
  if (answers.preferredLevels && !answers.studyDuration) {
    migrated.studyDuration = answers.preferredLevels.map((l: number) =>
      l === 6 ? '2' : l === 7 ? '3' : '4+'
    );
  }

  // Migration: old activityRankings -> scenarioChoices stays empty (can't auto-map)
  if (answers.activityRankings && !answers.scenarioChoices) {
    migrated.scenarioChoices = [];
  }

  // Migration: remove old fields that don't exist in new type
  delete migrated.activityRankings;
  delete migrated.dreamJobKeywords;
  delete migrated.preferredLevels;

  // Ensure new fields exist
  if (!migrated.scenarioChoices) migrated.scenarioChoices = [];
  if (!migrated.studyDuration) migrated.studyDuration = [];

  return migrated;
}

/** Get match label from percentage */
function getMatchLabel(pct: number): string {
  if (pct >= 75) return 'Strong match';
  if (pct >= 55) return 'Good fit';
  if (pct >= 40) return 'Worth exploring';
  return 'Stretch';
}

// ─── Component ──────────────────────────────────────────────────────────────

const FutureFinder: React.FC<FutureFinderProps> = ({ uid, profile }) => {
  // ─── Curriculum flag (Phase 2 JC support) ──────────────────────────────
  // For JC users this tool is rebranded as "Subject Explorer" — same 10-q
  // intent quiz (Q1-Q7 only; Q8-Q10 about study duration / region are CAO-
  // specific and skipped), but matches answers to clusters of LC subjects
  // they'd enjoy in senior cycle rather than to CAO courses.
  const { user } = useAuth();
  const curriculumLevel = user?.curriculumLevel ?? profile.curriculumLevel ?? 'senior';
  const isJunior = curriculumLevel === 'junior';

  // Effective question set: JC skips the CAO-flavoured Q8-Q11
  // (studyDuration, willingToRelocate, preferredRegions, estimatedPoints).
  const effectiveQuestions = useMemo(
    () => isJunior
      ? ASSESSMENT_QUESTIONS.filter(q =>
          q.id !== 'studyDuration' && q.id !== 'willingToRelocate' &&
          q.id !== 'preferredRegions' && q.id !== 'estimatedPoints'
        )
      : ASSESSMENT_QUESTIONS,
    [isJunior]
  );

  const { showToast } = useToast();
  const [isLoading, setIsLoading] = useState(true);
  const [phase, setPhase] = useState<Phase>('intro');
  const [answers, setAnswers] = useState<FutureFinderAnswers>(getDefaultAnswers());
  const [currentQ, setCurrentQ] = useState(0);
  const [results, setResults] = useState<RecommendationResult[]>([]);
  // JC cluster matches — populated in handleAssessmentComplete when isJunior.
  const [clusterResults, setClusterResults] = useState<ClusterMatchResult[]>([]);
  const [selectedCourse, setSelectedCourse] = useState<RecommendationResult | null>(null);
  const [compareCourses, setCompareCourses] = useState<RecommendationResult[]>([]);
  const [savedPicks, setSavedPicks] = useState<string[]>([]);
  const [sortMode, setSortMode] = useState<SortMode>('match');
  const [regionFilter, setRegionFilter] = useState<string>('');
  const [savedData, setSavedData] = useState<FutureFinderData | null>(null);

  // Auto-compute estimated points from profile subjects
  const autoPoints = useMemo(() => computeCurrentPoints(profile), [profile]);

  // Load existing data from Firestore
  useEffect(() => {
    if (!uid) return;
    let cancelled = false;
    const load = async () => {
      try {
        const snap = await getDoc(doc(db, 'progress', uid));
        if (cancelled) return;
        const data = snap.data();
        if (data?.futureFinder) {
          const ff = data.futureFinder as FutureFinderData;
          setSavedData(ff);
          const migrated = migrateAnswers(ff.answers);
          setAnswers(migrated);
          setSavedPicks(ff.topPicks || []);
          // Re-run the appropriate algorithm with migrated answers. JC
          // runs the cluster matcher; senior runs the CAO course matcher.
          if (isJunior) {
            setClusterResults(runSubjectExplorerMatch(migrated));
          } else {
            const res = runFutureFinderAssessment(migrated, profile, autoPoints);
            setResults(res);
            // Restore compare selections by matching codes against results
            if (ff.compareCodes && ff.compareCodes.length > 0) {
              const restored = ff.compareCodes
                .map(code => res.find(r => r.course.code === code))
                .filter((r): r is RecommendationResult => !!r);
              setCompareCourses(restored);
            }
          }
          setPhase('results');
        } else {
          // No saved data — auto-populate estimated points from profile
          setAnswers(prev => ({ ...prev, estimatedPoints: autoPoints }));
        }
      } catch (err) {
        console.error('Failed to load Future Finder data:', err);
      }
      if (!cancelled) setIsLoading(false);
    };
    load();
    return () => { cancelled = true; };
  }, [uid, profile, autoPoints, isJunior]);

  // Save data to Firestore
  const saveToFirestore = useCallback((data: FutureFinderData) => {
    setSavedData(data);
    setDoc(doc(db, 'progress', uid), { futureFinder: data }, { merge: true })
      .then(() => showToast('Results saved!', 'success'))
      .catch(err => { console.error('Failed to save:', err); showToast('Couldn\'t save \u2014 check your connection', 'error'); });
  }, [uid, showToast]);

  // Handle assessment completion. JC users run the cluster matcher
  // (Subject Explorer); senior users run the CAO course matcher (Future
  // Finder). Both paths land in the same 'results' phase, but the render
  // branches on isJunior.
  const handleAssessmentComplete = useCallback(() => {
    if (isJunior) {
      const clusters = runSubjectExplorerMatch(answers);
      setClusterResults(clusters);
      setPhase('results');
      // Persist a marker so we know the assessment was completed; we don't
      // currently persist the cluster ranking itself — it's cheap to re-run
      // from saved answers on next load.
      const data: FutureFinderData = {
        completedAt: new Date().toISOString(),
        answers,
        topPicks: [],
        savedComparisons: [],
      };
      saveToFirestore(data);
      return;
    }
    const res = runFutureFinderAssessment(answers, profile, autoPoints);
    setResults(res);
    setPhase('results');

    // Auto-save on completion
    const topPicks = res.slice(0, 10).map(r => r.course.code);
    const data: FutureFinderData = {
      completedAt: new Date().toISOString(),
      answers,
      topPicks,
      savedComparisons: [],
    };
    saveToFirestore(data);
  }, [isJunior, answers, profile, autoPoints, saveToFirestore]);

  // Toggle a saved pick
  const toggleSavedPick = useCallback((code: string) => {
    setSavedPicks(prev => {
      const next = prev.includes(code) ? prev.filter(c => c !== code) : [...prev, code];
      // Update Firestore
      if (savedData) {
        const updated = { ...savedData, topPicks: next };
        setDoc(doc(db, 'progress', uid), { futureFinder: updated }, { merge: true }).catch(() => {});
        setSavedData(updated);
      }
      return next;
    });
  }, [uid, savedData]);

  // Toggle compare
  const toggleCompare = useCallback((result: RecommendationResult) => {
    setCompareCourses(prev => {
      let next: RecommendationResult[];
      if (prev.find(c => c.course.code === result.course.code)) {
        next = prev.filter(c => c.course.code !== result.course.code);
      } else if (prev.length >= 3) {
        return prev;
      } else {
        next = [...prev, result];
      }
      // Persist compare selection so it survives navigating away
      if (savedData) {
        const codes = next.map(c => c.course.code);
        const updated = { ...savedData, compareCodes: codes };
        setDoc(doc(db, 'progress', uid), { futureFinder: updated }, { merge: true }).catch(() => {});
        setSavedData(updated);
      }
      return next;
    });
  }, [uid, savedData]);

  // Sorted and filtered results
  const displayResults = useMemo(() => {
    let filtered = results.slice(0, 30); // Top 30
    if (regionFilter) {
      filtered = filtered.filter(r => r.course.region === regionFilter);
    }
    if (sortMode === 'points') {
      filtered = [...filtered].sort((a, b) => a.course.typicalPoints - b.course.typicalPoints);
    } else if (sortMode === 'institution') {
      filtered = [...filtered].sort((a, b) => a.course.institution.localeCompare(b.course.institution));
    }
    return filtered.slice(0, 10);
  }, [results, sortMode, regionFilter]);

  // Retake
  const handleRetake = useCallback(() => {
    setAnswers(getDefaultAnswers());
    setCurrentQ(0);
    setResults([]);
    setSelectedCourse(null);
    setCompareCourses([]);
    setPhase('intro');
  }, []);

  if (isLoading) {
    return (
      <div className="flex items-center justify-center py-32">
        <div className="w-8 h-8 border-2 border-t-transparent rounded-full animate-spin" style={{ borderColor: COLORS.accent, borderTopColor: 'transparent' }} />
      </div>
    );
  }

  return (
    <div className="max-w-3xl mx-auto">
      <AnimatePresence mode="wait">
        {phase === 'intro' && (
          <IntroPhase key="intro" isJunior={isJunior} autoPoints={autoPoints} onStart={() => { setPhase('assessment'); setCurrentQ(0); }} onViewResults={(isJunior ? clusterResults.length > 0 : results.length > 0) ? () => setPhase('results') : undefined} />
        )}
        {phase === 'assessment' && (
          <AssessmentPhase
            key="assessment"
            questions={effectiveQuestions}
            currentQ={currentQ}
            answers={answers}
            autoPoints={autoPoints}
            onUpdateAnswer={(key, value) => setAnswers(prev => ({ ...prev, [key]: value }))}
            onNext={() => {
              if (currentQ < effectiveQuestions.length - 1) {
                setCurrentQ(currentQ + 1);
              } else {
                handleAssessmentComplete();
              }
            }}
            onBack={() => {
              if (currentQ > 0) setCurrentQ(currentQ - 1);
              else setPhase('intro');
            }}
          />
        )}
        {/* JC results: render cluster-based Subject Explorer instead of
            CAO course list. Detail/compare phases are senior-only — JC
            results don't need a per-course deep dive. */}
        {phase === 'results' && isJunior && (
          <SubjectExplorerResults
            key="se-results"
            clusters={clusterResults}
            onRetake={handleRetake}
          />
        )}
        {phase === 'results' && !isJunior && (
          <ResultsPhase
            key="results"
            results={displayResults}
            autoPoints={autoPoints}
            sortMode={sortMode}
            onSortChange={setSortMode}
            regionFilter={regionFilter}
            onRegionFilterChange={setRegionFilter}
            savedPicks={savedPicks}
            compareCourses={compareCourses}
            onToggleSave={toggleSavedPick}
            onToggleCompare={toggleCompare}
            onSelectCourse={(r) => { setSelectedCourse(r); setPhase('detail'); }}
            onCompare={() => setPhase('compare')}
            onRetake={handleRetake}
          />
        )}
        {phase === 'detail' && selectedCourse && (
          <DetailPhase
            key="detail"
            result={selectedCourse}
            answers={answers}
            autoPoints={autoPoints}
            isSaved={savedPicks.includes(selectedCourse.course.code)}
            isCompared={!!compareCourses.find(c => c.course.code === selectedCourse.course.code)}
            onToggleSave={() => toggleSavedPick(selectedCourse.course.code)}
            onToggleCompare={() => toggleCompare(selectedCourse)}
            onBack={() => setPhase('results')}
          />
        )}
        {phase === 'compare' && (
          <ComparePhase
            key="compare"
            courses={compareCourses}
            answers={answers}
            onBack={() => setPhase('results')}
            onRemove={(code) => {
              setCompareCourses(prev => {
                const next = prev.filter(c => c.course.code !== code);
                if (savedData) {
                  const updated = { ...savedData, compareCodes: next.map(c => c.course.code) };
                  setDoc(doc(db, 'progress', uid), { futureFinder: updated }, { merge: true }).catch(() => {});
                  setSavedData(updated);
                }
                return next;
              });
            }}
          />
        )}
      </AnimatePresence>
    </div>
  );
};

export default FutureFinder;

// ─── Phase Components ───────────────────────────────────────────────────────

/** Phase 1: Intro */
function IntroPhase({ isJunior, autoPoints, onStart, onViewResults }: { isJunior: boolean; autoPoints: number; onStart: () => void; onViewResults?: () => void }) {
  return (
    <MotionDiv initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0 }} transition={{ duration: 0.4 }}>
      <div className="text-center py-10">
        <p className="text-zinc-500 dark:text-zinc-400 max-w-md mx-auto mb-6 leading-relaxed">
          {isJunior
            ? <>Answer 7 quick questions. We'll suggest the subjects you might enjoy most in senior cycle {'\u2014'} based on what you're actually into.</>
            : <>Answer 10 quick questions. We'll match you with college courses that fit who you are {'\u2014'} not just your points.</>}
        </p>
        {!isJunior && autoPoints > 0 && (
          <p className="text-sm font-medium max-w-sm mx-auto mb-4" style={{ color: COLORS.accent }}>
            Based on your current grades, you're at {autoPoints} points
          </p>
        )}
        <p className="text-sm text-zinc-400 dark:text-zinc-500 max-w-sm mx-auto mb-8">
          {isJunior
            ? 'We look at your interests, the scenarios you find appealing, and how you like to work to suggest subject clusters that fit.'
            : 'We look at your interests, values, work style and preferred location to find courses you\'ll actually enjoy.'}
        </p>
        <div className="flex flex-col items-center gap-3">
          <PrimaryActionButton label="Let's Go" onClick={onStart} icon={Compass} />
          {onViewResults && (
            <button onClick={onViewResults} className="text-sm hover:underline" style={{ color: COLORS.accent }}>
              View previous results
            </button>
          )}
        </div>
      </div>
    </MotionDiv>
  );
}

/** Phase 2: Assessment */
function AssessmentPhase({
  questions, currentQ, answers, _autoPoints, onUpdateAnswer, onNext, onBack,
}: {
  questions: AssessmentQuestion[];
  currentQ: number;
  answers: FutureFinderAnswers;
  autoPoints: number;
  onUpdateAnswer: (key: string, value: any) => void;
  onNext: () => void;
  onBack: () => void;
}) {
  const question = questions[currentQ];
  const progress = ((currentQ + 1) / questions.length) * 100;
  const isLast = currentQ === questions.length - 1;

  // Check if current question has a valid answer
  const isValid = (() => {
    const val = (answers as any)[question.id];
    if (question.type === 'multi-select') return Array.isArray(val) && val.length > 0;
    if (question.type === 'single-select') return !!val;
    if (question.type === 'slider' || question.type === 'number') return typeof val === 'number';
    if (question.type === 'text') return true; // optional
    if (question.type === 'boolean') return typeof val === 'boolean';
    return true;
  })();

  // Skip region question if willing to relocate
  const shouldSkipRegions = question.id === 'preferredRegions' && answers.willingToRelocate;

  return (
    <MotionDiv initial={{ opacity: 0, x: 40 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: -40 }} transition={{ duration: 0.3 }}>
      {/* Progress bar */}
      <div className="mb-8">
        <div className="flex items-center justify-between mb-2">
          <span className="text-xs font-bold" style={{ color: COLORS.accent }}>Question {currentQ + 1} of {questions.length}</span>
          <span className="text-xs text-zinc-400 dark:text-zinc-500">{question.dimension}</span>
        </div>
        <div className="h-1.5 bg-zinc-200 dark:bg-zinc-800 rounded-full overflow-hidden">
          <div className="h-full rounded-full transition-all duration-500" style={{ width: `${progress}%`, backgroundColor: COLORS.accent }} />
        </div>
      </div>

      {/* Question card */}
      <div className="bg-white dark:bg-zinc-900 border border-zinc-200 dark:border-zinc-800 p-6 md:p-8 mb-6" style={{ borderRadius: '12px' }}>
        <h3 className="font-serif text-xl font-semibold text-zinc-900 dark:text-white mb-1">{question.question}</h3>
        {question.subtitle && (
          <p className="text-xs text-zinc-400 dark:text-zinc-500 mb-6">{question.subtitle}</p>
        )}
        {!question.subtitle && <div className="mb-6" />}

        {shouldSkipRegions ? (
          <p className="text-sm text-zinc-400 dark:text-zinc-500 italic">You're open to anywhere {'\u2014'} press Next to continue.</p>
        ) : (
          <QuestionInput question={question} value={(answers as any)[question.id]} onChange={(val) => onUpdateAnswer(question.id, val)} />
        )}
      </div>

      {/* Navigation */}
      <div className="flex items-center justify-between">
        <MotionButton whileHover={{ scale: 1.02 }} whileTap={{ scale: 0.98 }} onClick={onBack}
          className="flex items-center gap-2 px-4 py-2.5 rounded-xl bg-transparent border border-zinc-200 dark:border-zinc-700 text-zinc-600 dark:text-zinc-400 text-sm font-semibold hover:bg-zinc-50 dark:hover:bg-zinc-800 transition-colors">
          <ChevronLeft size={16} /> Back
        </MotionButton>
        <MotionButton whileHover={{ scale: 1.02 }} whileTap={{ scale: 0.98 }} onClick={onNext}
          disabled={!isValid && !shouldSkipRegions}
          className={`flex items-center gap-2 px-6 py-2.5 rounded-xl text-sm font-semibold transition-colors ${
            isValid || shouldSkipRegions
              ? 'text-white'
              : 'bg-zinc-200 dark:bg-zinc-800 text-zinc-400 cursor-not-allowed'
          }`}
          style={isValid || shouldSkipRegions ? { backgroundColor: COLORS.accent } : undefined}
          onMouseEnter={(e: React.MouseEvent<HTMLButtonElement>) => { if (isValid || shouldSkipRegions) e.currentTarget.style.backgroundColor = '#B54D14'; }}
          onMouseLeave={(e: React.MouseEvent<HTMLButtonElement>) => { if (isValid || shouldSkipRegions) e.currentTarget.style.backgroundColor = COLORS.accent; }}>
          {isLast ? 'See Results' : 'Next'} <ChevronRight size={16} />
        </MotionButton>
      </div>
    </MotionDiv>
  );
}

/** Question Input Renderer */
function QuestionInput({ question, value, onChange }: { question: AssessmentQuestion; value: any; onChange: (val: any) => void }) {
  if (question.type === 'multi-select' && question.options) {
    const selected: string[] = Array.isArray(value) ? value : [];
    const max = question.maxSelections || question.options.length;
    return (
      <div className="flex flex-wrap gap-2">
        {question.options.map(opt => {
          const isSelected = selected.includes(opt.value);
          return (
            <button
              key={opt.value}
              onClick={() => {
                if (isSelected) onChange(selected.filter(v => v !== opt.value));
                else if (selected.length < max) onChange([...selected, opt.value]);
              }}
              className={`px-4 py-2.5 rounded-xl text-sm font-medium transition-all border ${
                isSelected
                  ? ''
                  : 'bg-white dark:bg-zinc-800 text-zinc-700 dark:text-zinc-300 border-zinc-200 dark:border-zinc-700 hover:border-zinc-400 dark:hover:border-zinc-500'
              }`}
              style={isSelected ? { backgroundColor: COLORS.accent, color: 'white', borderColor: COLORS.accent } : undefined}
            >
              {isSelected && <Check size={14} className="inline mr-1.5 -mt-0.5" />}
              {opt.label}
            </button>
          );
        })}
      </div>
    );
  }

  if (question.type === 'single-select' && question.options) {
    return (
      <div className="space-y-2">
        {question.options.map(opt => (
          <button
            key={opt.value}
            onClick={() => onChange(opt.value)}
            className={`w-full text-left px-4 py-3 rounded-xl text-sm font-medium transition-all border ${
              value === opt.value
                ? ''
                : 'bg-white dark:bg-zinc-800 text-zinc-700 dark:text-zinc-300 border-zinc-200 dark:border-zinc-700 hover:border-zinc-400 dark:hover:border-zinc-500'
            }`}
            style={value === opt.value ? { backgroundColor: COLORS.accent, color: 'white', borderColor: COLORS.accent } : undefined}
          >
            {opt.label}
          </button>
        ))}
      </div>
    );
  }

  if (question.type === 'slider') {
    const val = typeof value === 'number' ? value : 3;
    const labels = ['Not at all', 'Slightly', 'Moderately', 'Very', 'Extremely'];
    return (
      <div className="flex gap-2">
        {labels.map((label, i) => {
          const step = i + 1;
          const isSelected = val === step;
          return (
            <MotionButton
              key={step}
              whileHover={{ scale: 1.04 }}
              whileTap={{ scale: 0.96 }}
              onClick={() => onChange(step)}
              className={`flex-1 py-3 rounded-xl text-sm font-semibold transition-all border ${
                isSelected
                  ? 'shadow-lg'
                  : 'bg-white dark:bg-zinc-800 text-zinc-600 dark:text-zinc-400 border-zinc-200 dark:border-zinc-700 hover:border-zinc-400 dark:hover:border-zinc-500'
              }`}
              style={isSelected ? { backgroundColor: COLORS.accent, color: 'white', borderColor: COLORS.accent, boxShadow: '0 10px 15px -3px rgba(242,107,31,0.25)' } : undefined}
            >
              {label}
            </MotionButton>
          );
        })}
      </div>
    );
  }

  if (question.type === 'boolean') {
    return (
      <div className="flex gap-3">
        <button
          onClick={() => onChange(true)}
          className={`flex-1 py-3 rounded-xl text-sm font-semibold transition-all border ${
            value === true ? '' : 'bg-white dark:bg-zinc-800 text-zinc-700 dark:text-zinc-300 border-zinc-200 dark:border-zinc-700 hover:border-zinc-400'
          }`}
          style={value === true ? { backgroundColor: COLORS.accent, color: 'white', borderColor: COLORS.accent } : undefined}
        >
          Open to anywhere
        </button>
        <button
          onClick={() => onChange(false)}
          className={`flex-1 py-3 rounded-xl text-sm font-semibold transition-all border ${
            value === false ? '' : 'bg-white dark:bg-zinc-800 text-zinc-700 dark:text-zinc-300 border-zinc-200 dark:border-zinc-700 hover:border-zinc-400'
          }`}
          style={value === false ? { backgroundColor: COLORS.accent, color: 'white', borderColor: COLORS.accent } : undefined}
        >
          I have a preference
        </button>
      </div>
    );
  }

  return null;
}

/** Phase 3: Results */
function ResultsPhase({
  results, autoPoints, sortMode, onSortChange, regionFilter, onRegionFilterChange,
  savedPicks, compareCourses, onToggleSave, onToggleCompare, onSelectCourse, onCompare, onRetake,
}: {
  results: RecommendationResult[];
  autoPoints: number;
  sortMode: SortMode;
  onSortChange: (m: SortMode) => void;
  regionFilter: string;
  onRegionFilterChange: (r: string) => void;
  savedPicks: string[];
  compareCourses: RecommendationResult[];
  onToggleSave: (code: string) => void;
  onToggleCompare: (r: RecommendationResult) => void;
  onSelectCourse: (r: RecommendationResult) => void;
  onCompare: () => void;
  onRetake: () => void;
}) {
  const [explainerOpen, setExplainerOpen] = useState(false);
  return (
    <MotionDiv initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0 }} transition={{ duration: 0.4 }}>
      {/* Header */}
      <div className="flex items-start justify-between mb-6 gap-3">
        <div className="min-w-0">
          <h2 className="font-serif text-2xl font-semibold text-zinc-900 dark:text-white">Your Top Matches</h2>
          <p className="text-sm text-zinc-400 dark:text-zinc-500 mt-1">Courses ranked by how well they fit you</p>
          {autoPoints > 0 && (
            <p className="text-xs font-medium mt-1" style={{ color: COLORS.accent }}>
              Based on your current grades, you're at {autoPoints} points
            </p>
          )}
        </div>
        <div className="flex items-center gap-3 shrink-0 pt-1">
          <button
            onClick={() => setExplainerOpen(true)}
            className="flex items-center gap-1.5 text-xs font-semibold text-zinc-400 dark:text-zinc-500 hover:text-zinc-700 dark:hover:text-zinc-300 transition-colors"
            aria-label="How are these results calculated?"
          >
            <Eye size={14} /> How this works
          </button>
          <button onClick={onRetake} className="flex items-center gap-1.5 text-xs font-semibold text-zinc-400 dark:text-zinc-500 hover:text-zinc-700 dark:hover:text-zinc-300 transition-colors">
            <RotateCcw size={14} /> Retake
          </button>
        </div>
      </div>

      <AnimatePresence>
        {explainerOpen && <ScoringExplainerModal onClose={() => setExplainerOpen(false)} />}
      </AnimatePresence>

      {/* Sort & Filter controls */}
      <div className="flex flex-wrap gap-2 mb-4">
        <div className="flex items-center gap-1 bg-zinc-100 dark:bg-zinc-800 rounded-lg p-0.5">
          {([['match', 'Match %'], ['points', 'Points'], ['institution', 'College']] as const).map(([key, label]) => (
            <button
              key={key}
              onClick={() => onSortChange(key)}
              className={`px-3 py-1.5 rounded-md text-xs font-semibold transition-colors ${
                sortMode === key ? 'bg-white dark:bg-zinc-700 text-zinc-900 dark:text-white shadow-sm' : 'text-zinc-500 dark:text-zinc-400 hover:text-zinc-700 dark:hover:text-zinc-300'
              }`}
            >
              {label}
            </button>
          ))}
        </div>
        <select
          value={regionFilter}
          onChange={e => onRegionFilterChange(e.target.value)}
          className="px-3 py-1.5 rounded-lg bg-zinc-100 dark:bg-zinc-800 text-xs font-semibold text-zinc-700 dark:text-zinc-300 border-none focus:outline-none focus:ring-2 focus:ring-zinc-400/50"
        >
          <option value="">All regions</option>
          {Object.entries(REGIONS).map(([key, label]) => (
            <option key={key} value={key}>{label}</option>
          ))}
        </select>
      </div>

      {/* Compare bar */}
      {compareCourses.length > 0 && (
        <div className="mb-4 p-3 rounded-xl border flex items-center justify-between bg-[#FAF7F4] dark:bg-zinc-900" style={{ borderColor: 'rgba(242,107,31,0.2)' }}>
          <span className="text-xs font-semibold" style={{ color: COLORS.accent }}>
            {compareCourses.length} course{compareCourses.length > 1 ? 's' : ''} selected for comparison
          </span>
          <button
            onClick={onCompare}
            disabled={compareCourses.length < 2}
            className={`px-4 py-1.5 rounded-lg text-xs font-bold transition-colors ${
              compareCourses.length >= 2 ? 'text-white' : 'bg-zinc-200 dark:bg-zinc-800 text-zinc-400 cursor-not-allowed'
            }`}
            style={compareCourses.length >= 2 ? { backgroundColor: COLORS.accent } : undefined}
          >
            Compare
          </button>
        </div>
      )}

      {/* Result cards */}
      <div className="space-y-3">
        {results.map((r, i) => (
          <ResultCard
            key={r.course.code}
            result={r}
            rank={i + 1}
            isSaved={savedPicks.includes(r.course.code)}
            isCompared={!!compareCourses.find(c => c.course.code === r.course.code)}
            onToggleSave={() => onToggleSave(r.course.code)}
            onToggleCompare={() => onToggleCompare(r)}
            onClick={() => onSelectCourse(r)}
          />
        ))}
      </div>

      {results.length === 0 && (
        <div className="text-center py-16">
          <p className="text-zinc-400 dark:text-zinc-500">No courses match your filters. Try broadening your region or study duration preferences.</p>
        </div>
      )}
    </MotionDiv>
  );
}

/** Result Card */
function ResultCard({
  result, rank, isSaved, isCompared, onToggleSave, onToggleCompare, onClick,
}: {
  result: RecommendationResult;
  rank: number;
  isSaved: boolean;
  isCompared: boolean;
  onToggleSave: () => void;
  onToggleCompare: () => void;
  onClick: () => void;
}) {
  const matchPct = Math.round(result.score * 100);
  const matchLabel = getMatchLabel(matchPct);
  const c = result.course;

  return (
    <MotionDiv
      initial={{ opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: rank * 0.04, duration: 0.3 }}
      className="group rounded-xl border hover:shadow-md cursor-pointer overflow-hidden transition-all bg-[#FAF7F4] dark:bg-zinc-900"
      style={{ borderColor: 'rgba(0,0,0,0.07)' }}
      onClick={onClick}
    >
      <div className="h-[2px] opacity-0 group-hover:opacity-100 transition-opacity" style={{ backgroundColor: COLORS.accent }} />
      <div className="p-4 md:p-5">
        <div className="flex items-start justify-between gap-3 mb-3">
          <div className="flex-1 min-w-0">
            <div className="flex items-center gap-2 mb-1 flex-wrap">
              <span className="text-xs font-bold" style={{ color: COLORS.accent }}>#{rank}</span>
              <span className="text-xs font-mono text-zinc-400 dark:text-zinc-500">{c.code}</span>
              <span className="px-2 py-0.5 rounded-full bg-zinc-100 dark:bg-zinc-800 text-xs font-semibold text-zinc-500 dark:text-zinc-400">Level {c.level}</span>
              {c.pathwayType === 'plc' && (
                <span className="px-2 py-0.5 rounded-full text-[10px] font-bold" style={{ backgroundColor: '#EDF2EE', color: '#4A6B4F' }}>PLC</span>
              )}
              {c.pathwayType === 'apprenticeship' && (
                <span className="px-2 py-0.5 rounded-full text-[10px] font-bold" style={{ backgroundColor: '#FDF3E7', color: '#8B5E2A' }}>Apprenticeship</span>
              )}
              {result.subjectAlignment === 'strong' && (
                <span className="px-2 py-0.5 rounded-full text-xs font-semibold" style={{ backgroundColor: '#E8F0E8', color: '#4A6B4F' }}>Subjects align</span>
              )}
              {result.subjectAlignment === 'none' && c.subjectBonus.length > 0 && (
                <span className="px-2 py-0.5 rounded-full text-xs font-semibold" style={{ backgroundColor: '#FEF3C7', color: '#92400E' }}>Check requirements</span>
              )}
            </div>
            <h4 className="font-serif font-semibold text-base text-zinc-900 dark:text-white truncate">{c.title}</h4>
            <p className="text-xs text-zinc-500 dark:text-zinc-400 mt-0.5">{INSTITUTIONS[c.institution] || c.institution} {'\u2014'} {REGIONS[c.region] || c.region}</p>
          </div>
          <div className="flex flex-col items-center shrink-0">
            <div className={`w-12 h-12 rounded-xl flex items-center justify-center font-bold text-sm ${
              matchPct < 50 ? 'bg-zinc-100 text-zinc-500' : ''
            }`}
              style={matchPct >= 70 ? { backgroundColor: '#EDF2EE', color: '#4A6B4F' } : matchPct >= 50 ? { backgroundColor: '#FDF3E7', color: '#8B5E2A' } : undefined}
            >
              {matchPct}%
            </div>
            <span className="text-[10px] text-zinc-400 dark:text-zinc-500 mt-1">{matchLabel}</span>
          </div>
        </div>

        {/* Points */}
        <div className="flex items-center gap-3 mb-3">
          <span className="text-xs font-semibold text-zinc-500 dark:text-zinc-400">
            {c.typicalPoints === 0 ? (c.pathwayType === 'apprenticeship' ? 'Employer-based' : 'Open entry') : `~${c.typicalPoints} points`}
          </span>
          <span className="text-xs text-zinc-400 dark:text-zinc-500">{'\u2022'}</span>
          <span className="text-xs text-zinc-500 dark:text-zinc-400">{c.duration} years</span>
          {c.salaryBand === 'high' && (
            <>
              <span className="text-xs text-zinc-400 dark:text-zinc-500">{'\u2022'}</span>
              <span className="text-xs font-semibold text-emerald-600 dark:text-emerald-400">High salary</span>
            </>
          )}
        </div>

        {/* Reason pills — show up to 5 */}
        <div className="flex flex-wrap gap-1.5 mb-3">
          {result.reasons.slice(0, 5).map((reason, i) => (
            <span key={i} className="px-2.5 py-1 rounded-full text-xs font-medium" style={{ backgroundColor: '#EDF2EE', color: '#4A6B4F' }}>
              {reason}
            </span>
          ))}
        </div>

        {/* Actions */}
        <div className="flex items-center gap-2" onClick={e => e.stopPropagation()}>
          <button
            onClick={onToggleSave}
            className={`flex items-center gap-1 px-2.5 py-1.5 rounded-lg text-xs font-semibold transition-colors border ${
              isSaved ? 'bg-transparent border-zinc-300 dark:border-zinc-600' : 'bg-transparent border-zinc-200 dark:border-zinc-700 text-zinc-500 dark:text-zinc-400 hover:bg-zinc-50 dark:hover:bg-zinc-800'
            }`}
            style={isSaved ? { color: COLORS.accent } : undefined}
          >
            {isSaved ? <Check size={12} /> : <BookmarkPlus size={12} />}
            {isSaved ? 'Saved' : 'Save'}
          </button>
          <button
            onClick={onToggleCompare}
            className={`flex items-center gap-1 px-2.5 py-1.5 rounded-lg text-xs font-semibold transition-colors border ${
              isCompared ? 'bg-transparent border-zinc-300 dark:border-zinc-600' : 'bg-transparent border-zinc-200 dark:border-zinc-700 text-zinc-500 dark:text-zinc-400 hover:bg-zinc-50 dark:hover:bg-zinc-800'
            }`}
            style={isCompared ? { color: COLORS.accent } : undefined}
          >
            <SlidersHorizontal size={12} />
            {isCompared ? 'Comparing' : 'Compare'}
          </button>
          <a
            href={getCoursePageUrl(c)}
            target="_blank"
            rel="noopener noreferrer"
            className="flex items-center gap-1 px-2.5 py-1.5 rounded-lg text-xs font-semibold bg-transparent border border-zinc-200 dark:border-zinc-700 text-zinc-500 dark:text-zinc-400 hover:bg-zinc-50 dark:hover:bg-zinc-800 transition-colors"
          >
            <ArrowUpRight size={12} />
            College page
          </a>
        </div>
      </div>
    </MotionDiv>
  );
}

/** Phase 4: Detail View */
function DetailPhase({
  result, _answers, autoPoints, isSaved, isCompared, onToggleSave, onToggleCompare, onBack,
}: {
  result: RecommendationResult;
  answers: FutureFinderAnswers;
  autoPoints: number;
  isSaved: boolean;
  isCompared: boolean;
  onToggleSave: () => void;
  onToggleCompare: () => void;
  onBack: () => void;
}) {
  const c = result.course;
  const matchPct = Math.round(result.score * 100);
  const matchLabel = getMatchLabel(matchPct);
  const pointsGap = c.typicalPoints - autoPoints;

  return (
    <MotionDiv initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0 }} transition={{ duration: 0.35 }}>
      <button onClick={onBack} className="flex items-center gap-1.5 text-sm font-semibold text-zinc-500 dark:text-zinc-400 hover:text-zinc-700 dark:hover:text-zinc-300 mb-4 transition-colors">
        <ChevronLeft size={16} /> Back to results
      </button>

      <div className="bg-[#FAF7F4] dark:bg-zinc-900 overflow-hidden" style={{ border: '0.5px solid rgba(0,0,0,0.07)', borderRadius: '12px' }}>
        {/* Header */}
        <div className="p-6" style={{ backgroundColor: COLORS.accent }}>
          <div className="flex items-center gap-2 mb-2 flex-wrap">
            <span className="px-2.5 py-0.5 rounded-full bg-white/20 text-white text-xs font-bold">{c.code}</span>
            <span className="px-2.5 py-0.5 rounded-full bg-white/20 text-white text-xs font-bold">Level {c.level}</span>
            <span className="px-2.5 py-0.5 rounded-full bg-white/20 text-white text-xs font-bold">{matchPct}% {matchLabel}</span>
            {c.pathwayType === 'plc' && (
              <span className="px-2.5 py-0.5 rounded-full text-xs font-bold" style={{ backgroundColor: 'rgba(255,255,255,0.25)', color: 'white' }}>PLC</span>
            )}
            {c.pathwayType === 'apprenticeship' && (
              <span className="px-2.5 py-0.5 rounded-full text-xs font-bold" style={{ backgroundColor: 'rgba(255,255,255,0.25)', color: 'white' }}>Apprenticeship</span>
            )}
            {result.subjectAlignment === 'strong' && (
              <span className="px-2.5 py-0.5 rounded-full text-xs font-bold" style={{ backgroundColor: 'rgba(255,255,255,0.25)', color: 'white' }}>Subjects align</span>
            )}
            {result.subjectAlignment === 'none' && c.subjectBonus.length > 0 && (
              <span className="px-2.5 py-0.5 rounded-full text-xs font-bold" style={{ backgroundColor: 'rgba(254,243,199,0.3)', color: '#FEF3C7' }}>Check requirements</span>
            )}
          </div>
          <h3 className="font-serif text-2xl font-bold text-white mb-1">{c.title}</h3>
          <p className="text-white/80 text-sm">{INSTITUTIONS[c.institution] || c.institution}</p>
        </div>

        <div className="p-6 space-y-6">
          {/* Description */}
          <p className="text-sm text-zinc-700 dark:text-zinc-300 leading-relaxed">{c.description}</p>

          {/* Key info grid */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
            <InfoTile icon={TrendingUp} label="Typical Points" value={c.typicalPoints === 0 ? (c.pathwayType === 'apprenticeship' ? 'Employer-based' : 'Open entry') : `~${c.typicalPoints}`} />
            <InfoTile icon={Clock} label="Duration" value={`${c.duration} years`} />
            <InfoTile icon={MapPin} label="Region" value={REGIONS[c.region] || c.region} />
            <InfoTile icon={Briefcase} label="Salary Band" value={c.salaryBand.charAt(0).toUpperCase() + c.salaryBand.slice(1)} />
          </div>

          {/* Your Points section */}
          {c.typicalPoints === 0 ? (
            <div className="p-4 rounded-xl border bg-[#FAF7F4] dark:bg-zinc-900" style={{ borderColor: 'rgba(242,107,31,0.15)' }}>
              <h4 className="text-xs font-bold text-zinc-500 dark:text-zinc-400 uppercase tracking-wider mb-3">Entry Requirements</h4>
              <p className="text-sm text-zinc-700 dark:text-zinc-300">
                {c.pathwayType === 'apprenticeship'
                  ? 'Apply directly to an employer. No CAO points required. You will earn a wage from day one while training on the job.'
                  : 'No CAO points required. This is an open-entry QQI Level 5 course. Apply directly through the college.'}
              </p>
            </div>
          ) : autoPoints > 0 ? (
            <div className="p-4 rounded-xl border bg-[#FAF7F4] dark:bg-zinc-900" style={{ borderColor: 'rgba(242,107,31,0.15)' }}>
              <h4 className="text-xs font-bold text-zinc-500 dark:text-zinc-400 uppercase tracking-wider mb-3">Your Points</h4>
              <div className="grid grid-cols-3 gap-3 text-center">
                <div>
                  <p className="text-2xl font-bold" style={{ color: COLORS.accent }}>{autoPoints}</p>
                  <p className="text-xs text-zinc-400 dark:text-zinc-500 mt-0.5">Your current points</p>
                </div>
                <div>
                  <p className="text-2xl font-bold text-zinc-600 dark:text-zinc-400">{c.typicalPoints}</p>
                  <p className="text-xs text-zinc-400 dark:text-zinc-500 mt-0.5">Typical entry</p>
                </div>
                <div>
                  {pointsGap > 0 ? (
                    <>
                      <p className="text-2xl font-bold" style={{ color: '#D97706' }}>{pointsGap}</p>
                      <p className="text-xs text-zinc-400 dark:text-zinc-500 mt-0.5">Points gap</p>
                    </>
                  ) : (
                    <>
                      <p className="text-2xl font-bold text-emerald-600 dark:text-emerald-400">{Math.abs(pointsGap)}</p>
                      <p className="text-xs text-zinc-400 dark:text-zinc-500 mt-0.5">Points ahead</p>
                    </>
                  )}
                </div>
              </div>
            </div>
          ) : null}

          {/* Employability */}
          <div>
            <h4 className="text-xs font-bold text-zinc-500 dark:text-zinc-400 uppercase tracking-wider mb-2">Employability</h4>
            <div className="flex gap-1">
              {[1, 2, 3, 4, 5].map(n => (
                <div key={n} className={`h-2 flex-1 rounded-full ${n <= c.employability ? 'bg-emerald-500' : 'bg-zinc-200 dark:bg-zinc-700'}`} />
              ))}
            </div>
          </div>

          {/* Career paths */}
          <div>
            <h4 className="text-xs font-bold text-zinc-500 dark:text-zinc-400 uppercase tracking-wider mb-2">Career Paths</h4>
            <div className="flex flex-wrap gap-2">
              {c.careerPaths.map(cp => (
                <span key={cp} className="px-3 py-1.5 rounded-lg bg-zinc-100 dark:bg-zinc-800 text-sm text-zinc-700 dark:text-zinc-300 font-medium">{cp}</span>
              ))}
            </div>
          </div>

          {/* Subject bonus */}
          <div>
            <h4 className="text-xs font-bold text-zinc-500 dark:text-zinc-400 uppercase tracking-wider mb-2">Subjects That Help</h4>
            <div className="flex flex-wrap gap-2">
              {c.subjectBonus.map(sub => (
                <span key={sub} className="px-3 py-1.5 rounded-lg text-sm font-medium bg-[#FAF7F4] dark:bg-zinc-900" style={{ color: COLORS.accent }}>{sub}</span>
              ))}
            </div>
          </div>

          {/* Why this suits you — show up to 5 reasons */}
          <div className="p-4 rounded-xl border bg-[#FAF7F4] dark:bg-zinc-900" style={{ borderColor: 'rgba(242,107,31,0.15)' }}>
            <h4 className="text-sm font-bold mb-3 flex items-center gap-2" style={{ color: COLORS.accent }}>
              <Heart size={16} style={{ color: COLORS.accent }} /> Why This Suits You
            </h4>
            <ul className="space-y-2">
              {result.reasons.slice(0, 5).map((reason, i) => (
                <li key={i} className="flex items-start gap-2 text-sm text-zinc-700 dark:text-zinc-300">
                  <Star size={14} className="mt-0.5 shrink-0" style={{ color: COLORS.accent }} />
                  {reason}
                </li>
              ))}
            </ul>
          </div>

          {/* How we scored this */}
          <div className="p-4 rounded-xl border border-zinc-200 dark:border-zinc-800">
            <h4 className="text-xs font-bold text-zinc-500 dark:text-zinc-400 uppercase tracking-wider mb-4">How We Scored This</h4>
            <div className="space-y-3">
              <ScoreBar label="Interest match" score={result.scoreBreakdown.interestScore} />
              <ScoreBar label="Values alignment" score={result.scoreBreakdown.valuesScore} />
              <ScoreBar label="Practical fit" score={result.scoreBreakdown.feasibilityScore} />
            </div>
          </div>

          {/* Actions */}
          <div className="flex flex-wrap gap-2 pt-2">
            <MotionButton whileHover={{ scale: 1.02 }} whileTap={{ scale: 0.98 }} onClick={onToggleSave}
              className={`flex items-center gap-2 px-4 py-2.5 rounded-xl text-sm font-semibold transition-colors border ${
                isSaved ? 'text-white' : 'bg-transparent border-zinc-200 dark:border-zinc-700 text-zinc-700 dark:text-zinc-300 hover:bg-zinc-50 dark:hover:bg-zinc-800'
              }`}
              style={isSaved ? { backgroundColor: COLORS.accent, borderColor: COLORS.accent } : undefined}>
              {isSaved ? <Check size={16} /> : <BookmarkPlus size={16} />}
              {isSaved ? 'Saved to Picks' : 'Save to Picks'}
            </MotionButton>
            <MotionButton whileHover={{ scale: 1.02 }} whileTap={{ scale: 0.98 }} onClick={onToggleCompare}
              className={`flex items-center gap-2 px-4 py-2.5 rounded-xl text-sm font-semibold transition-colors border ${
                isCompared ? 'text-white' : 'bg-transparent border-zinc-200 dark:border-zinc-700 text-zinc-700 dark:text-zinc-300 hover:bg-zinc-50 dark:hover:bg-zinc-800'
              }`}
              style={isCompared ? { backgroundColor: COLORS.accent, borderColor: COLORS.accent } : undefined}>
              <SlidersHorizontal size={16} />
              {isCompared ? 'Added to Compare' : 'Add to Compare'}
            </MotionButton>
            <a
              href={getCoursePageUrl(c)}
              target="_blank"
              rel="noopener noreferrer"
              className="flex items-center gap-2 px-4 py-2.5 rounded-xl text-sm font-semibold bg-transparent border border-zinc-200 dark:border-zinc-700 text-zinc-700 dark:text-zinc-300 hover:bg-zinc-50 dark:hover:bg-zinc-800 transition-colors"
            >
              <ArrowUpRight size={16} />
              Visit {c.institution} course page
            </a>
          </div>
        </div>
      </div>
    </MotionDiv>
  );
}

/** Score progress bar for the "How we scored this" section */
function ScoreBar({ label, score }: { label: string; score: number }) {
  const pct = Math.round(score * 100);
  return (
    <div className="flex items-center gap-3">
      <span className="text-xs font-medium text-zinc-600 dark:text-zinc-400 w-32 shrink-0">{label}</span>
      <div className="flex-1 h-2 bg-zinc-200 dark:bg-zinc-700 rounded-full overflow-hidden">
        <div
          className="h-full rounded-full transition-all duration-500"
          style={{ width: `${pct}%`, backgroundColor: COLORS.accent }}
        />
      </div>
      <span className="text-xs font-bold text-zinc-600 dark:text-zinc-400 w-10 text-right">{pct}%</span>
    </div>
  );
}

/** Info Tile (for detail view) */
function InfoTile({ icon: Icon, label, value }: { icon: LucideIcon; label: string; value: string }) {
  return (
    <div className="p-3 rounded-xl bg-zinc-50 dark:bg-zinc-800/50 text-center">
      <Icon size={16} className="mx-auto text-zinc-400 dark:text-zinc-500 mb-1" />
      <p className="text-xs text-zinc-400 dark:text-zinc-500 mb-0.5">{label}</p>
      <p className="text-sm font-bold text-zinc-900 dark:text-white">{value}</p>
    </div>
  );
}

/** Phase 5: Compare View */
function ComparePhase({
  courses, _answers, onBack, onRemove,
}: {
  courses: RecommendationResult[];
  answers: FutureFinderAnswers;
  onBack: () => void;
  onRemove: (code: string) => void;
}) {
  const fields: { label: string; render: (c: CAOCourse, r: RecommendationResult) => string }[] = [
    { label: 'Institution', render: c => INSTITUTIONS[c.institution] || c.institution },
    { label: 'Level', render: c => `Level ${c.level}` },
    { label: 'Typical Points', render: c => c.typicalPoints === 0 ? (c.pathwayType === 'apprenticeship' ? 'Employer-based' : 'Open entry') : `~${c.typicalPoints}` },
    { label: 'Duration', render: c => `${c.duration} years` },
    { label: 'Region', render: c => REGIONS[c.region] || c.region },
    { label: 'Salary Band', render: c => c.salaryBand.charAt(0).toUpperCase() + c.salaryBand.slice(1) },
    { label: 'Employability', render: c => `${'\u2605'.repeat(c.employability)}${'\u2606'.repeat(5 - c.employability)}` },
    { label: 'Career Paths', render: c => c.careerPaths.join(', ') },
    { label: 'Match', render: (_c, r) => `${Math.round(r.score * 100)}%` },
  ];

  return (
    <MotionDiv initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0 }} transition={{ duration: 0.35 }}>
      <button onClick={onBack} className="flex items-center gap-1.5 text-sm font-semibold text-zinc-500 dark:text-zinc-400 hover:text-zinc-700 dark:hover:text-zinc-300 mb-4 transition-colors">
        <ChevronLeft size={16} /> Back to results
      </button>

      <div className="flex items-start justify-between gap-4 mb-6">
        <h2 className="font-serif text-2xl font-semibold text-zinc-900 dark:text-white">Compare Courses</h2>
        <img
          src="/assets/future-finder-compare.png"
          alt=""
          aria-hidden
          className="shrink-0"
          style={{ width: 'clamp(56px, 7vw, 88px)', height: 'auto', objectFit: 'contain' }}
        />
      </div>

      <div className="overflow-x-auto">
        <table className="w-full text-sm">
          <thead>
            <tr>
              <th className="text-left p-3 text-xs font-bold text-zinc-400 dark:text-zinc-500 uppercase tracking-wider" />
              {courses.map(r => (
                <th key={r.course.code} className="p-3 text-left min-w-[180px]">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="font-serif font-semibold text-zinc-900 dark:text-white text-sm">{r.course.title}</p>
                      <p className="text-xs text-zinc-400 dark:text-zinc-500 font-normal">{r.course.code}</p>
                    </div>
                    <button onClick={() => onRemove(r.course.code)} className="p-1 rounded-md hover:bg-zinc-100 dark:hover:bg-zinc-800 transition-colors">
                      <X size={14} className="text-zinc-400" />
                    </button>
                  </div>
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {fields.map(field => (
              <tr key={field.label} className="border-t border-zinc-100 dark:border-zinc-800">
                <td className="p-3 text-xs font-bold text-zinc-400 dark:text-zinc-500 uppercase tracking-wider whitespace-nowrap">{field.label}</td>
                {courses.map(r => (
                  <td key={r.course.code} className="p-3 text-zinc-700 dark:text-zinc-300">
                    {field.render(r.course, r)}
                  </td>
                ))}
              </tr>
            ))}
            <tr className="border-t border-zinc-100 dark:border-zinc-800">
              <td className="p-3 text-xs font-bold text-zinc-400 dark:text-zinc-500 uppercase tracking-wider">Why It Fits</td>
              {courses.map(r => (
                <td key={r.course.code} className="p-3">
                  <ul className="space-y-1">
                    {r.reasons.slice(0, 5).map((reason, i) => (
                      <li key={i} className="flex items-start gap-1 text-xs text-zinc-700 dark:text-zinc-300">
                        <Star size={10} className="mt-0.5 shrink-0" style={{ color: COLORS.accent }} /> {reason}
                      </li>
                    ))}
                  </ul>
                </td>
              ))}
            </tr>
          </tbody>
        </table>
      </div>

      {courses.length < 2 && (
        <p className="text-center text-sm text-zinc-400 dark:text-zinc-500 mt-8">
          Add at least 2 courses to compare. Go back and use the Compare button on result cards.
        </p>
      )}
    </MotionDiv>
  );
}

// ─── JC Subject Explorer Results ────────────────────────────────────────────
//
// JC variant of the results phase. Instead of CAO course matches we show
// 1 top cluster + 2 alternates + a "things to try" section + a soft career
// callout. No saving/comparing — clusters aren't selectable artefacts, just
// a sense of direction.
function SubjectExplorerResults({
  clusters, onRetake,
}: {
  clusters: ClusterMatchResult[];
  onRetake: () => void;
}) {
  if (clusters.length === 0) {
    return (
      <MotionDiv initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} className="py-10 text-center space-y-4">
        <p className="text-zinc-500 dark:text-zinc-400">We couldn't find a strong pattern from your answers. Try the quiz again and pick whichever options actually appeal to you, not what you think you should pick.</p>
        <PrimaryActionButton onClick={onRetake}>Retake the quiz</PrimaryActionButton>
      </MotionDiv>
    );
  }

  const top = clusters[0];
  const alternates = clusters.slice(1, 3);

  return (
    <MotionDiv initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0 }} transition={{ duration: 0.4 }} className="space-y-8">
      {/* Top cluster — primary suggestion */}
      <div>
        <p className="text-[10px] font-bold uppercase tracking-widest text-zinc-400 dark:text-zinc-500 mb-2">Best fit</p>
        <div className="rounded-2xl p-6 bg-[#FDEEDF] dark:bg-zinc-900" style={{ border: `2px solid ${COLORS.accent}` }}>
          <div className="flex items-start gap-3 mb-3">
            <div className="w-10 h-10 rounded-xl flex items-center justify-center shrink-0" style={{ backgroundColor: COLORS.accent }}>
              <Compass className="w-5 h-5 text-white" />
            </div>
            <div className="flex-1 min-w-0">
              <h3 className="font-serif text-xl font-bold text-zinc-900 dark:text-white">{top.cluster.label}</h3>
              <p className="text-sm text-zinc-700 dark:text-zinc-300 mt-1 leading-relaxed">{top.cluster.blurb}</p>
            </div>
          </div>

          <p className="text-[10px] font-bold uppercase tracking-widest mt-4 mb-2" style={{ color: COLORS.accent }}>Subjects to consider</p>
          <div className="flex flex-wrap gap-2 mb-4">
            {top.cluster.subjects.map(s => (
              <span key={s} className="text-xs font-semibold px-3 py-1.5 rounded-full bg-white dark:bg-zinc-800 text-zinc-800 dark:text-zinc-200" style={{ border: `1px solid rgba(242,107,31,0.2)` }}>
                {s}
              </span>
            ))}
          </div>

          {top.matchedSignals.length > 0 && (
            <p className="text-xs text-zinc-500 dark:text-zinc-400 italic mt-3">
              Why this fits: {top.matchedSignals.slice(0, 3).join(' · ')}.
            </p>
          )}
        </div>
      </div>

      {/* Alternate clusters */}
      {alternates.length > 0 && (
        <div>
          <p className="text-[10px] font-bold uppercase tracking-widest text-zinc-400 dark:text-zinc-500 mb-2">Also worth a look</p>
          <div className="space-y-3">
            {alternates.map(alt => (
              <div key={alt.cluster.id} className="rounded-xl p-4 bg-[#FAF7F4] dark:bg-zinc-900" style={{ border: '0.5px solid rgba(0,0,0,0.07)' }}>
                <h4 className="font-serif text-base font-bold text-zinc-900 dark:text-white mb-1">{alt.cluster.label}</h4>
                <p className="text-xs text-zinc-600 dark:text-zinc-400 leading-relaxed mb-2">{alt.cluster.blurb}</p>
                <div className="flex flex-wrap gap-1.5">
                  {alt.cluster.subjects.slice(0, 5).map(s => (
                    <span key={s} className="text-[10px] font-semibold px-2 py-1 rounded-full bg-white dark:bg-zinc-800 text-zinc-600 dark:text-zinc-400" style={{ border: '0.5px solid rgba(0,0,0,0.08)' }}>
                      {s}
                    </span>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Things to try — concrete, low-stakes exploration from the top cluster */}
      <div>
        <p className="text-[10px] font-bold uppercase tracking-widest text-zinc-400 dark:text-zinc-500 mb-2">Things to try in TY or before senior cycle</p>
        <ul className="space-y-2">
          {top.cluster.thingsToTry.map((thing, i) => (
            <li key={i} className="flex items-start gap-2 text-sm text-zinc-700 dark:text-zinc-300">
              <Star size={14} className="mt-0.5 shrink-0" style={{ color: COLORS.accent }} />
              <span>{thing}</span>
            </li>
          ))}
        </ul>
      </div>

      {/* Soft career callout — low-prescription. NOT "your future career". */}
      <div className="rounded-xl p-4 bg-[#FAF7F4] dark:bg-zinc-900" style={{ border: '0.5px solid rgba(0,0,0,0.07)' }}>
        <p className="text-[10px] font-bold uppercase tracking-widest text-zinc-400 dark:text-zinc-500 mb-2">Where this can lead</p>
        <p className="text-sm text-zinc-700 dark:text-zinc-300 leading-relaxed">{top.cluster.careerHint}</p>
        <p className="text-xs text-zinc-500 dark:text-zinc-400 mt-2 italic">
          You don't have to decide anything now — this is just a sense of where these subjects open doors to.
        </p>
      </div>

      {/* Retake */}
      <div className="text-center pt-2">
        <button
          onClick={onRetake}
          className="inline-flex items-center gap-2 text-xs font-semibold text-zinc-500 hover:text-zinc-700 dark:text-zinc-400 dark:hover:text-zinc-200"
        >
          <RotateCcw size={12} /> Retake the quiz
        </button>
      </div>
    </MotionDiv>
  );
}

// ── Scoring explainer modal ────────────────────────────────────────────────
// Surfaces what's actually happening behind the match %, how the salary band
// is derived, and how the employability number is sourced. The intent is to
// be honest with the student about what's a real algorithm vs. what's a
// hand-curated reference value — so they can use the result as a guide
// without treating it as a prediction.
function ScoringExplainerModal({ onClose }: { onClose: () => void }) {
  // Portalled to document.body so the modal escapes ResultsPhase's Framer
  // `<MotionDiv>` transform context. Without the portal, `position: fixed`
  // is positioned relative to the transformed ancestor instead of the
  // viewport, and the modal spills off the top of the screen.
  return createPortal(
    <MotionDiv
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      className="fixed inset-0 z-[200] flex items-center justify-center bg-black/55 backdrop-blur-sm p-4"
      onClick={onClose}
    >
      <MotionDiv
        initial={{ opacity: 0, scale: 0.96, y: 12 }}
        animate={{ opacity: 1, scale: 1, y: 0 }}
        exit={{ opacity: 0, scale: 0.96, y: 12 }}
        transition={{ duration: 0.25, ease: [0.16, 1, 0.3, 1] as number[] }}
        className="bg-[#FAFBF6] dark:bg-zinc-900 rounded-2xl border-2 border-[#1A1A1A] dark:border-zinc-700 shadow-[6px_6px_0_0_#1A1A1A] dark:shadow-[6px_6px_0_0_#3f3f46] max-w-xl w-full max-h-[90vh] flex flex-col overflow-hidden"
        onClick={(e: React.MouseEvent) => e.stopPropagation()}
      >
        {/* Header (fixed) */}
        <div className="flex items-start justify-between p-6 pb-4 shrink-0">
          <div className="flex items-start gap-3 min-w-0">
            <div className="w-11 h-11 rounded-xl flex items-center justify-center bg-[rgba(242,107,31,0.12)] shrink-0">
              <Eye size={20} className="text-[#F26B1F]" />
            </div>
            <div className="min-w-0">
              <h2 className="font-serif text-xl font-bold text-[#1A1A1A] dark:text-white">How your results are calculated</h2>
              <p className="text-xs text-zinc-500 dark:text-zinc-400 mt-0.5">A quick look behind the match percentage</p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="w-8 h-8 rounded-lg flex items-center justify-center hover:bg-black/5 dark:hover:bg-white/10 transition-colors shrink-0"
            aria-label="Close"
          >
            <X size={18} className="text-zinc-500" />
          </button>
        </div>

        {/* Body (scrolls when content exceeds the viewport-capped modal) */}
        <div className="px-6 pb-6 space-y-5 overflow-y-auto flex-1 min-h-0">
          {/* Matching */}
          <section>
            <p className="text-[10px] font-bold uppercase tracking-widest text-zinc-400 dark:text-zinc-500 mb-2">The match score</p>
            <p className="text-sm text-zinc-700 dark:text-zinc-300 leading-relaxed mb-3">
              Every course gets a 0–100% score made of three parts:
            </p>
            <div className="space-y-2.5">
              <div className="rounded-xl bg-white dark:bg-zinc-800 border border-zinc-200 dark:border-zinc-700 p-3">
                <div className="flex items-baseline justify-between mb-1">
                  <p className="text-sm font-bold text-[#1A1A1A] dark:text-white">Interest fit</p>
                  <span className="text-xs font-bold" style={{ color: COLORS.accent }}>45%</span>
                </div>
                <p className="text-xs text-zinc-500 dark:text-zinc-400 leading-relaxed">
                  How well your interest tags and the scenarios you picked overlap with the course's own tags. Full credit at 3+ matching interests, with a bonus for matching scenarios.
                </p>
              </div>
              <div className="rounded-xl bg-white dark:bg-zinc-800 border border-zinc-200 dark:border-zinc-700 p-3">
                <div className="flex items-baseline justify-between mb-1">
                  <p className="text-sm font-bold text-[#1A1A1A] dark:text-white">Values alignment</p>
                  <span className="text-xs font-bold" style={{ color: COLORS.accent }}>30%</span>
                </div>
                <p className="text-xs text-zinc-500 dark:text-zinc-400 leading-relaxed">
                  Your salary, job-security, and helping-others sliders weighted against the course's salary band and employability rating. Plus your work-style picks (analytical / hands-on / etc.) and team preference.
                </p>
              </div>
              <div className="rounded-xl bg-white dark:bg-zinc-800 border border-zinc-200 dark:border-zinc-700 p-3">
                <div className="flex items-baseline justify-between mb-1">
                  <p className="text-sm font-bold text-[#1A1A1A] dark:text-white">Feasibility</p>
                  <span className="text-xs font-bold" style={{ color: COLORS.accent }}>25%</span>
                </div>
                <p className="text-xs text-zinc-500 dark:text-zinc-400 leading-relaxed">
                  Does your preferred study length match the course's NFQ level, and are your current points realistic for the course's typical entry threshold. Geographic preferences nudge the final score up or down.
                </p>
              </div>
            </div>
          </section>

          {/* Salary */}
          <section>
            <p className="text-[10px] font-bold uppercase tracking-widest text-zinc-400 dark:text-zinc-500 mb-2">Salary band</p>
            <div className="rounded-xl bg-white dark:bg-zinc-800 border border-zinc-200 dark:border-zinc-700 p-3">
              <p className="text-xs text-zinc-700 dark:text-zinc-300 leading-relaxed mb-2">
                Every course carries a <span className="font-bold">Low / Mid / High</span> salary band. These are <span className="font-bold">informed reference values</span>, not predictions for you personally — they reflect roughly where typical mid-career graduate earnings sit in Ireland for that pathway, based on the general patterns visible across publicly-available labour-market and graduate-outcome reporting.
              </p>
              <p className="text-xs text-zinc-500 dark:text-zinc-400 leading-relaxed italic">
                Two students in the same course will end up in very different bands depending on specialisation, region, and employer. The band is a useful first signal — not a number to bank on.
              </p>
            </div>
          </section>

          {/* Employability */}
          <section>
            <p className="text-[10px] font-bold uppercase tracking-widest text-zinc-400 dark:text-zinc-500 mb-2">Employability rating</p>
            <div className="rounded-xl bg-white dark:bg-zinc-800 border border-zinc-200 dark:border-zinc-700 p-3">
              <p className="text-xs text-zinc-700 dark:text-zinc-300 leading-relaxed mb-2">
                A <span className="font-bold">1 to 5 rating</span> per course, also informed-but-curated. Higher means the path from this course to substantive employment or further study tends to be more predictable in the Irish market.
              </p>
              <ul className="text-xs text-zinc-600 dark:text-zinc-400 space-y-1 leading-relaxed">
                <li><span className="font-bold text-[#1A1A1A] dark:text-white">5</span> — Very strong outcomes (medicine, nursing, education, accounting)</li>
                <li><span className="font-bold text-[#1A1A1A] dark:text-white">4</span> — Strong (engineering, computer science, most business)</li>
                <li><span className="font-bold text-[#1A1A1A] dark:text-white">3</span> — Solid (general degrees, sciences, social sciences)</li>
                <li><span className="font-bold text-[#1A1A1A] dark:text-white">1–2</span> — Niche or competitive fields where placement is less predictable</li>
              </ul>
            </div>
          </section>

          {/* Disclaimer */}
          <section className="rounded-xl p-3" style={{ backgroundColor: 'rgba(242,107,31,0.10)' }}>
            <p className="text-xs text-[#8C3A0E] dark:text-[#FDEEDF] leading-relaxed">
              <span className="font-bold">Treat the result as a guide, not a verdict.</span> The algorithm reflects fit between you and a course, not how your career will go. Use it to surface options you hadn't thought about — then go talk to people doing the job.
            </p>
          </section>
        </div>

        {/* Footer CTA (fixed below the scrolling body) */}
        <div className="px-6 pb-6 pt-2 shrink-0 border-t border-black/[0.04] dark:border-white/[0.06]">
          <button
            onClick={onClose}
            className="w-full flex items-center justify-center gap-2 px-5 py-3 rounded-2xl border-2 border-[#1A1A1A] bg-[#F26B1F] text-[#FDF8F0] font-sans font-bold text-sm shadow-[4px_4px_0_0_#1A1A1A] hover:shadow-[6px_6px_0_0_#1A1A1A] hover:-translate-y-0.5 active:translate-x-1 active:translate-y-1 active:shadow-[0px_0px_0_0_#1A1A1A] transition-all duration-150"
          >
            Got it
          </button>
        </div>
      </MotionDiv>
    </MotionDiv>,
    document.body
  );
}
