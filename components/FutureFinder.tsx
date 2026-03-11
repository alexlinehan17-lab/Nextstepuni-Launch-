/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState, useEffect, useCallback, useMemo } from 'react';
import { useToast } from './Toast';
import { motion, AnimatePresence } from 'framer-motion';
import {
  Compass, ChevronRight, ChevronLeft, Search, SlidersHorizontal,
  MapPin, GraduationCap, Briefcase, Heart, Star, RotateCcw,
  BookmarkPlus, Check, ArrowUpRight, TrendingUp, X, Building, Clock,
} from 'lucide-react';
import { db } from '../firebase';
import { doc, getDoc, setDoc } from 'firebase/firestore';
import { type StudentSubjectProfile } from './subjectData';
import { INSTITUTIONS, REGIONS, type CAOCourse } from './futureFinderData';
import {
  runFutureFinderAssessment,
  ASSESSMENT_QUESTIONS,
  type FutureFinderAnswers,
  type RecommendationResult,
  type AssessmentQuestion,
} from './futureFinderAlgorithm';

const MotionDiv = motion.div as any;
const MotionButton = motion.button as any;

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
}

type Phase = 'intro' | 'assessment' | 'results' | 'detail' | 'compare';

type SortMode = 'match' | 'points' | 'institution';

// ─── Default Answers ────────────────────────────────────────────────────────

function getDefaultAnswers(): FutureFinderAnswers {
  return {
    interestTags: [],
    activityRankings: [],
    dreamJobKeywords: '',
    workStyleTags: [],
    teamPreference: 'mix',
    salaryImportance: 3,
    jobSecurityImportance: 3,
    helpingOthersImportance: 3,
    willingToRelocate: true,
    preferredRegions: [],
    preferredLevels: [8],
    estimatedPoints: 350,
  };
}

// ─── Component ──────────────────────────────────────────────────────────────

const FutureFinder: React.FC<FutureFinderProps> = ({ uid, profile }) => {
  const { showToast } = useToast();
  const [isLoading, setIsLoading] = useState(true);
  const [phase, setPhase] = useState<Phase>('intro');
  const [answers, setAnswers] = useState<FutureFinderAnswers>(getDefaultAnswers());
  const [currentQ, setCurrentQ] = useState(0);
  const [results, setResults] = useState<RecommendationResult[]>([]);
  const [selectedCourse, setSelectedCourse] = useState<RecommendationResult | null>(null);
  const [compareCourses, setCompareCourses] = useState<RecommendationResult[]>([]);
  const [savedPicks, setSavedPicks] = useState<string[]>([]);
  const [sortMode, setSortMode] = useState<SortMode>('match');
  const [regionFilter, setRegionFilter] = useState<string>('');
  const [savedData, setSavedData] = useState<FutureFinderData | null>(null);

  // Load existing data from Firestore
  useEffect(() => {
    if (!uid) return;
    (async () => {
      try {
        const snap = await getDoc(doc(db, 'progress', uid));
        const data = snap.data();
        if (data?.futureFinder) {
          const ff = data.futureFinder as FutureFinderData;
          setSavedData(ff);
          setAnswers(ff.answers);
          setSavedPicks(ff.topPicks || []);
          // Re-run algorithm with saved answers
          const res = runFutureFinderAssessment(ff.answers, profile);
          setResults(res);
          setPhase('results');
        }
      } catch (e) {
        console.error('Failed to load Future Finder data:', e);
      }
      setIsLoading(false);
    })();
  }, [uid, profile]);

  // Save data to Firestore
  const saveToFirestore = useCallback((data: FutureFinderData) => {
    setSavedData(data);
    setDoc(doc(db, 'progress', uid), { futureFinder: data }, { merge: true })
      .then(() => showToast('Results saved!', 'success'))
      .catch(e => { console.error('Failed to save:', e); showToast('Couldn\'t save — check your connection', 'error'); });
  }, [uid, showToast]);

  // Handle assessment completion
  const handleAssessmentComplete = useCallback(() => {
    const res = runFutureFinderAssessment(answers, profile);
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
  }, [answers, profile, saveToFirestore]);

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
      if (prev.find(c => c.course.code === result.course.code)) {
        return prev.filter(c => c.course.code !== result.course.code);
      }
      if (prev.length >= 3) return prev;
      return [...prev, result];
    });
  }, []);

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
        <div className="w-8 h-8 border-2 border-indigo-500 border-t-transparent rounded-full animate-spin" />
      </div>
    );
  }

  return (
    <div className="max-w-3xl mx-auto">
      <AnimatePresence mode="wait">
        {phase === 'intro' && (
          <IntroPhase key="intro" onStart={() => { setPhase('assessment'); setCurrentQ(0); }} onViewResults={results.length > 0 ? () => setPhase('results') : undefined} />
        )}
        {phase === 'assessment' && (
          <AssessmentPhase
            key="assessment"
            currentQ={currentQ}
            answers={answers}
            onUpdateAnswer={(key, value) => setAnswers(prev => ({ ...prev, [key]: value }))}
            onNext={() => {
              if (currentQ < ASSESSMENT_QUESTIONS.length - 1) {
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
        {phase === 'results' && (
          <ResultsPhase
            key="results"
            results={displayResults}
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
            onRemove={(code) => setCompareCourses(prev => prev.filter(c => c.course.code !== code))}
          />
        )}
      </AnimatePresence>
    </div>
  );
};

export default FutureFinder;

// ─── Phase Components ───────────────────────────────────────────────────────

/** Phase 1: Intro */
function IntroPhase({ onStart, onViewResults }: { onStart: () => void; onViewResults?: () => void }) {
  return (
    <MotionDiv initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0 }} transition={{ duration: 0.4 }}>
      <div className="text-center py-12">
        <div className="w-20 h-20 mx-auto mb-6 rounded-2xl bg-indigo-100 dark:bg-indigo-900/30 flex items-center justify-center">
          <Compass size={40} className="text-indigo-600 dark:text-indigo-400" />
        </div>
        <h2 className="font-serif text-3xl font-semibold text-zinc-900 dark:text-white mb-3">Find Your Future</h2>
        <p className="text-zinc-500 dark:text-zinc-400 max-w-md mx-auto mb-8 leading-relaxed">
          Answer 12 quick questions. We'll match you with college courses that fit who you are — not just your points.
        </p>
        <p className="text-sm text-zinc-400 dark:text-zinc-500 max-w-sm mx-auto mb-8">
          We look at your interests, values, work style, preferred location and subjects to find courses you'll actually enjoy.
        </p>
        <div className="flex flex-col items-center gap-3">
          <MotionButton
            whileHover={{ scale: 1.02 }} whileTap={{ scale: 0.98 }}
            onClick={onStart}
            className="px-8 py-3.5 rounded-xl bg-indigo-600 hover:bg-indigo-700 text-white font-semibold text-base transition-colors"
          >
            Let's Go
          </MotionButton>
          {onViewResults && (
            <button onClick={onViewResults} className="text-sm text-indigo-500 dark:text-indigo-400 hover:underline">
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
  currentQ, answers, onUpdateAnswer, onNext, onBack,
}: {
  currentQ: number;
  answers: FutureFinderAnswers;
  onUpdateAnswer: (key: string, value: any) => void;
  onNext: () => void;
  onBack: () => void;
}) {
  const question = ASSESSMENT_QUESTIONS[currentQ];
  const progress = ((currentQ + 1) / ASSESSMENT_QUESTIONS.length) * 100;
  const isLast = currentQ === ASSESSMENT_QUESTIONS.length - 1;

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
          <span className="text-xs font-bold text-indigo-600 dark:text-indigo-400">Question {currentQ + 1} of {ASSESSMENT_QUESTIONS.length}</span>
          <span className="text-xs text-zinc-400 dark:text-zinc-500">{question.dimension}</span>
        </div>
        <div className="h-1.5 bg-zinc-200 dark:bg-zinc-800 rounded-full overflow-hidden">
          <div className="h-full bg-indigo-500 rounded-full transition-all duration-500" style={{ width: `${progress}%` }} />
        </div>
      </div>

      {/* Question card */}
      <div className="bg-white dark:bg-zinc-900 rounded-2xl border border-zinc-200 dark:border-zinc-800 p-6 md:p-8 mb-6">
        <h3 className="font-serif text-xl font-semibold text-zinc-900 dark:text-white mb-6">{question.question}</h3>

        {shouldSkipRegions ? (
          <p className="text-sm text-zinc-400 dark:text-zinc-500 italic">You're open to anywhere — press Next to continue.</p>
        ) : (
          <QuestionInput question={question} value={(answers as any)[question.id]} onChange={(val) => onUpdateAnswer(question.id, val)} />
        )}
      </div>

      {/* Navigation */}
      <div className="flex items-center justify-between">
        <MotionButton whileHover={{ scale: 1.02 }} whileTap={{ scale: 0.98 }} onClick={onBack}
          className="flex items-center gap-2 px-4 py-2.5 rounded-xl bg-zinc-100 dark:bg-zinc-800 text-zinc-700 dark:text-zinc-300 text-sm font-semibold hover:bg-zinc-200 dark:hover:bg-zinc-700 transition-colors">
          <ChevronLeft size={16} /> Back
        </MotionButton>
        <MotionButton whileHover={{ scale: 1.02 }} whileTap={{ scale: 0.98 }} onClick={onNext}
          disabled={!isValid && !shouldSkipRegions}
          className={`flex items-center gap-2 px-6 py-2.5 rounded-xl text-sm font-semibold transition-colors ${
            isValid || shouldSkipRegions
              ? 'bg-indigo-600 hover:bg-indigo-700 text-white'
              : 'bg-zinc-200 dark:bg-zinc-800 text-zinc-400 cursor-not-allowed'
          }`}>
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
                  ? 'bg-indigo-600 text-white border-indigo-600'
                  : 'bg-white dark:bg-zinc-800 text-zinc-700 dark:text-zinc-300 border-zinc-200 dark:border-zinc-700 hover:border-indigo-400 dark:hover:border-indigo-500'
              }`}
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
                ? 'bg-indigo-600 text-white border-indigo-600'
                : 'bg-white dark:bg-zinc-800 text-zinc-700 dark:text-zinc-300 border-zinc-200 dark:border-zinc-700 hover:border-indigo-400 dark:hover:border-indigo-500'
            }`}
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
      <div>
        <input
          type="range" min={question.min || 1} max={question.max || 5} value={val}
          onChange={e => onChange(parseInt(e.target.value))}
          className="w-full h-2 bg-zinc-200 dark:bg-zinc-700 rounded-lg appearance-none cursor-pointer accent-indigo-600"
        />
        <div className="flex justify-between mt-2">
          {labels.map((l, i) => (
            <span key={i} className={`text-xs ${val === i + 1 ? 'text-indigo-600 dark:text-indigo-400 font-bold' : 'text-zinc-400 dark:text-zinc-500'}`}>{l}</span>
          ))}
        </div>
      </div>
    );
  }

  if (question.type === 'number') {
    const val = typeof value === 'number' ? value : 350;
    return (
      <div>
        <input
          type="range" min={question.min || 100} max={question.max || 625} value={val} step={5}
          onChange={e => onChange(parseInt(e.target.value))}
          className="w-full h-2 bg-zinc-200 dark:bg-zinc-700 rounded-lg appearance-none cursor-pointer accent-indigo-600"
        />
        <div className="text-center mt-3">
          <span className="text-3xl font-bold text-indigo-600 dark:text-indigo-400">{val}</span>
          <span className="text-sm text-zinc-400 dark:text-zinc-500 ml-2">points</span>
        </div>
        <div className="flex justify-between mt-1">
          <span className="text-xs text-zinc-400 dark:text-zinc-500">{question.min || 100}</span>
          <span className="text-xs text-zinc-400 dark:text-zinc-500">{question.max || 625}</span>
        </div>
      </div>
    );
  }

  if (question.type === 'text') {
    return (
      <input
        type="text"
        value={value || ''}
        onChange={e => onChange(e.target.value)}
        placeholder="e.g. game designer, vet, software engineer, teacher..."
        className="w-full px-4 py-3 rounded-xl bg-zinc-50 dark:bg-zinc-800 border border-zinc-200 dark:border-zinc-700 text-zinc-900 dark:text-white text-sm placeholder-zinc-400 dark:placeholder-zinc-500 focus:outline-none focus:ring-2 focus:ring-indigo-500/50 focus:border-indigo-500"
      />
    );
  }

  if (question.type === 'boolean') {
    return (
      <div className="flex gap-3">
        <button
          onClick={() => onChange(true)}
          className={`flex-1 py-3 rounded-xl text-sm font-semibold transition-all border ${
            value === true ? 'bg-indigo-600 text-white border-indigo-600' : 'bg-white dark:bg-zinc-800 text-zinc-700 dark:text-zinc-300 border-zinc-200 dark:border-zinc-700 hover:border-indigo-400'
          }`}
        >
          Open to anywhere
        </button>
        <button
          onClick={() => onChange(false)}
          className={`flex-1 py-3 rounded-xl text-sm font-semibold transition-all border ${
            value === false ? 'bg-indigo-600 text-white border-indigo-600' : 'bg-white dark:bg-zinc-800 text-zinc-700 dark:text-zinc-300 border-zinc-200 dark:border-zinc-700 hover:border-indigo-400'
          }`}
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
  results, sortMode, onSortChange, regionFilter, onRegionFilterChange,
  savedPicks, compareCourses, onToggleSave, onToggleCompare, onSelectCourse, onCompare, onRetake,
}: {
  results: RecommendationResult[];
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
  return (
    <MotionDiv initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0 }} transition={{ duration: 0.4 }}>
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <div>
          <h2 className="font-serif text-2xl font-semibold text-zinc-900 dark:text-white">Your Top Matches</h2>
          <p className="text-sm text-zinc-400 dark:text-zinc-500 mt-1">Courses ranked by how well they fit you</p>
        </div>
        <button onClick={onRetake} className="flex items-center gap-1.5 text-xs font-semibold text-zinc-400 dark:text-zinc-500 hover:text-zinc-700 dark:hover:text-zinc-300 transition-colors">
          <RotateCcw size={14} /> Retake
        </button>
      </div>

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
          className="px-3 py-1.5 rounded-lg bg-zinc-100 dark:bg-zinc-800 text-xs font-semibold text-zinc-700 dark:text-zinc-300 border-none focus:outline-none focus:ring-2 focus:ring-indigo-500/50"
        >
          <option value="">All regions</option>
          {Object.entries(REGIONS).map(([key, label]) => (
            <option key={key} value={key}>{label}</option>
          ))}
        </select>
      </div>

      {/* Compare bar */}
      {compareCourses.length > 0 && (
        <div className="mb-4 p-3 rounded-xl bg-indigo-50 dark:bg-indigo-950/30 border border-indigo-200 dark:border-indigo-800/40 flex items-center justify-between">
          <span className="text-xs font-semibold text-indigo-700 dark:text-indigo-300">
            {compareCourses.length} course{compareCourses.length > 1 ? 's' : ''} selected for comparison
          </span>
          <button
            onClick={onCompare}
            disabled={compareCourses.length < 2}
            className={`px-4 py-1.5 rounded-lg text-xs font-bold transition-colors ${
              compareCourses.length >= 2 ? 'bg-indigo-600 text-white hover:bg-indigo-700' : 'bg-indigo-200 dark:bg-indigo-900 text-indigo-400 cursor-not-allowed'
            }`}
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
          <p className="text-zinc-400 dark:text-zinc-500">No courses match your filters. Try broadening your region or level preferences.</p>
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
  const c = result.course;

  return (
    <MotionDiv
      initial={{ opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: rank * 0.04, duration: 0.3 }}
      className="group bg-white dark:bg-zinc-900 rounded-2xl border border-zinc-200 dark:border-zinc-800 hover:border-indigo-400/50 dark:hover:border-indigo-500/40 transition-all hover:shadow-md cursor-pointer overflow-hidden"
      onClick={onClick}
    >
      <div className="h-[2px] bg-indigo-500 opacity-0 group-hover:opacity-100 transition-opacity" />
      <div className="p-4 md:p-5">
        <div className="flex items-start justify-between gap-3 mb-3">
          <div className="flex-1 min-w-0">
            <div className="flex items-center gap-2 mb-1">
              <span className="text-xs font-bold text-indigo-600 dark:text-indigo-400">#{rank}</span>
              <span className="text-xs font-mono text-zinc-400 dark:text-zinc-500">{c.code}</span>
              <span className="px-2 py-0.5 rounded-full bg-zinc-100 dark:bg-zinc-800 text-xs font-semibold text-zinc-500 dark:text-zinc-400">Level {c.level}</span>
            </div>
            <h4 className="font-serif font-semibold text-base text-zinc-900 dark:text-white truncate">{c.title}</h4>
            <p className="text-xs text-zinc-500 dark:text-zinc-400 mt-0.5">{c.institution} — {REGIONS[c.region] || c.region}</p>
          </div>
          <div className="flex flex-col items-center shrink-0">
            <div className={`w-12 h-12 rounded-xl flex items-center justify-center font-bold text-sm ${
              matchPct >= 70 ? 'bg-emerald-100 dark:bg-emerald-900/30 text-emerald-700 dark:text-emerald-400' :
              matchPct >= 50 ? 'bg-amber-100 dark:bg-amber-900/30 text-amber-700 dark:text-amber-400' :
              'bg-zinc-100 dark:bg-zinc-800 text-zinc-500 dark:text-zinc-400'
            }`}>
              {matchPct}%
            </div>
            <span className="text-[10px] text-zinc-400 dark:text-zinc-500 mt-1">match</span>
          </div>
        </div>

        {/* Points */}
        <div className="flex items-center gap-3 mb-3">
          <span className="text-xs font-semibold text-zinc-500 dark:text-zinc-400">
            ~{c.typicalPoints} points
          </span>
          <span className="text-xs text-zinc-400 dark:text-zinc-500">•</span>
          <span className="text-xs text-zinc-500 dark:text-zinc-400">{c.duration} years</span>
          {c.salaryBand === 'high' && (
            <>
              <span className="text-xs text-zinc-400 dark:text-zinc-500">•</span>
              <span className="text-xs font-semibold text-emerald-600 dark:text-emerald-400">High salary</span>
            </>
          )}
        </div>

        {/* Reason pills */}
        <div className="flex flex-wrap gap-1.5 mb-3">
          {result.reasons.map((reason, i) => (
            <span key={i} className="px-2.5 py-1 rounded-full bg-indigo-50 dark:bg-indigo-950/30 text-xs text-indigo-700 dark:text-indigo-300 font-medium">
              {reason}
            </span>
          ))}
        </div>

        {/* Actions */}
        <div className="flex items-center gap-2" onClick={e => e.stopPropagation()}>
          <button
            onClick={onToggleSave}
            className={`flex items-center gap-1 px-2.5 py-1.5 rounded-lg text-xs font-semibold transition-colors ${
              isSaved ? 'bg-indigo-100 dark:bg-indigo-900/30 text-indigo-700 dark:text-indigo-300' : 'bg-zinc-100 dark:bg-zinc-800 text-zinc-500 dark:text-zinc-400 hover:bg-zinc-200 dark:hover:bg-zinc-700'
            }`}
          >
            {isSaved ? <Check size={12} /> : <BookmarkPlus size={12} />}
            {isSaved ? 'Saved' : 'Save'}
          </button>
          <button
            onClick={onToggleCompare}
            className={`flex items-center gap-1 px-2.5 py-1.5 rounded-lg text-xs font-semibold transition-colors ${
              isCompared ? 'bg-violet-100 dark:bg-violet-900/30 text-violet-700 dark:text-violet-300' : 'bg-zinc-100 dark:bg-zinc-800 text-zinc-500 dark:text-zinc-400 hover:bg-zinc-200 dark:hover:bg-zinc-700'
            }`}
          >
            <SlidersHorizontal size={12} />
            {isCompared ? 'Comparing' : 'Compare'}
          </button>
        </div>
      </div>
    </MotionDiv>
  );
}

/** Phase 4: Detail View */
function DetailPhase({
  result, answers, isSaved, isCompared, onToggleSave, onToggleCompare, onBack,
}: {
  result: RecommendationResult;
  answers: FutureFinderAnswers;
  isSaved: boolean;
  isCompared: boolean;
  onToggleSave: () => void;
  onToggleCompare: () => void;
  onBack: () => void;
}) {
  const c = result.course;
  const matchPct = Math.round(result.score * 100);

  return (
    <MotionDiv initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0 }} transition={{ duration: 0.35 }}>
      <button onClick={onBack} className="flex items-center gap-1.5 text-sm font-semibold text-zinc-500 dark:text-zinc-400 hover:text-zinc-700 dark:hover:text-zinc-300 mb-4 transition-colors">
        <ChevronLeft size={16} /> Back to results
      </button>

      <div className="bg-white dark:bg-zinc-900 rounded-2xl border border-zinc-200 dark:border-zinc-800 overflow-hidden">
        {/* Header */}
        <div className="bg-gradient-to-r from-indigo-600 to-violet-600 p-6">
          <div className="flex items-center gap-2 mb-2">
            <span className="px-2.5 py-0.5 rounded-full bg-white/20 text-white text-xs font-bold">{c.code}</span>
            <span className="px-2.5 py-0.5 rounded-full bg-white/20 text-white text-xs font-bold">Level {c.level}</span>
            <span className="px-2.5 py-0.5 rounded-full bg-white/20 text-white text-xs font-bold">{matchPct}% match</span>
          </div>
          <h3 className="font-serif text-2xl font-bold text-white mb-1">{c.title}</h3>
          <p className="text-indigo-100 text-sm">{INSTITUTIONS[c.institution] || c.institution}</p>
        </div>

        <div className="p-6 space-y-6">
          {/* Description */}
          <p className="text-sm text-zinc-700 dark:text-zinc-300 leading-relaxed">{c.description}</p>

          {/* Key info grid */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
            <InfoTile icon={TrendingUp} label="Typical Points" value={`~${c.typicalPoints}`} />
            <InfoTile icon={Clock} label="Duration" value={`${c.duration} years`} />
            <InfoTile icon={MapPin} label="Region" value={REGIONS[c.region] || c.region} />
            <InfoTile icon={Briefcase} label="Salary Band" value={c.salaryBand.charAt(0).toUpperCase() + c.salaryBand.slice(1)} />
          </div>

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
                <span key={sub} className="px-3 py-1.5 rounded-lg bg-indigo-50 dark:bg-indigo-950/30 text-sm text-indigo-700 dark:text-indigo-300 font-medium">{sub}</span>
              ))}
            </div>
          </div>

          {/* Why this suits you */}
          <div className="p-4 rounded-xl bg-gradient-to-r from-indigo-50 to-violet-50 dark:from-indigo-950/20 dark:to-violet-950/20 border border-indigo-200/50 dark:border-indigo-800/30">
            <h4 className="text-sm font-bold text-indigo-800 dark:text-indigo-300 mb-3 flex items-center gap-2">
              <Heart size={16} /> Why This Suits You
            </h4>
            <ul className="space-y-2">
              {result.reasons.map((reason, i) => (
                <li key={i} className="flex items-start gap-2 text-sm text-indigo-700 dark:text-indigo-300">
                  <Star size={14} className="mt-0.5 shrink-0 text-indigo-500" />
                  {reason}
                </li>
              ))}
            </ul>
          </div>

          {/* Actions */}
          <div className="flex flex-wrap gap-2 pt-2">
            <MotionButton whileHover={{ scale: 1.02 }} whileTap={{ scale: 0.98 }} onClick={onToggleSave}
              className={`flex items-center gap-2 px-4 py-2.5 rounded-xl text-sm font-semibold transition-colors ${
                isSaved ? 'bg-indigo-600 text-white' : 'bg-zinc-100 dark:bg-zinc-800 text-zinc-700 dark:text-zinc-300 hover:bg-zinc-200 dark:hover:bg-zinc-700'
              }`}>
              {isSaved ? <Check size={16} /> : <BookmarkPlus size={16} />}
              {isSaved ? 'Saved to Picks' : 'Save to Picks'}
            </MotionButton>
            <MotionButton whileHover={{ scale: 1.02 }} whileTap={{ scale: 0.98 }} onClick={onToggleCompare}
              className={`flex items-center gap-2 px-4 py-2.5 rounded-xl text-sm font-semibold transition-colors ${
                isCompared ? 'bg-violet-600 text-white' : 'bg-zinc-100 dark:bg-zinc-800 text-zinc-700 dark:text-zinc-300 hover:bg-zinc-200 dark:hover:bg-zinc-700'
              }`}>
              <SlidersHorizontal size={16} />
              {isCompared ? 'Added to Compare' : 'Add to Compare'}
            </MotionButton>
          </div>
        </div>
      </div>
    </MotionDiv>
  );
}

/** Info Tile (for detail view) */
function InfoTile({ icon: Icon, label, value }: { icon: React.ElementType; label: string; value: string }) {
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
  courses, answers, onBack, onRemove,
}: {
  courses: RecommendationResult[];
  answers: FutureFinderAnswers;
  onBack: () => void;
  onRemove: (code: string) => void;
}) {
  const fields: { label: string; render: (c: CAOCourse, r: RecommendationResult) => string }[] = [
    { label: 'Institution', render: c => INSTITUTIONS[c.institution] || c.institution },
    { label: 'Level', render: c => `Level ${c.level}` },
    { label: 'Typical Points', render: c => `~${c.typicalPoints}` },
    { label: 'Duration', render: c => `${c.duration} years` },
    { label: 'Region', render: c => REGIONS[c.region] || c.region },
    { label: 'Salary Band', render: c => c.salaryBand.charAt(0).toUpperCase() + c.salaryBand.slice(1) },
    { label: 'Employability', render: c => `${'★'.repeat(c.employability)}${'☆'.repeat(5 - c.employability)}` },
    { label: 'Career Paths', render: c => c.careerPaths.join(', ') },
    { label: 'Match', render: (_c, r) => `${Math.round(r.score * 100)}%` },
  ];

  return (
    <MotionDiv initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0 }} transition={{ duration: 0.35 }}>
      <button onClick={onBack} className="flex items-center gap-1.5 text-sm font-semibold text-zinc-500 dark:text-zinc-400 hover:text-zinc-700 dark:hover:text-zinc-300 mb-4 transition-colors">
        <ChevronLeft size={16} /> Back to results
      </button>

      <h2 className="font-serif text-2xl font-semibold text-zinc-900 dark:text-white mb-6">Compare Courses</h2>

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
                    {r.reasons.map((reason, i) => (
                      <li key={i} className="flex items-start gap-1 text-xs text-indigo-700 dark:text-indigo-300">
                        <Star size={10} className="mt-0.5 shrink-0 text-indigo-500" /> {reason}
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
