/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState, useCallback, useMemo, useRef, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  Plus, Trash2, Edit3, Play, ArrowLeft, Check, X, RotateCcw,
  Layers, Flame, Star, ChevronRight, Clock, BookOpen, Sparkles,
} from 'lucide-react';

const MotionDiv = motion.div as any;
const MotionButton = motion.button as any;
const MotionSpan = motion.span as any;

// ─── Types ──────────────────────────────────────────────────────────────────

interface CardSRSState {
  easeFactor: number;
  interval: number;
  repetitions: number;
  nextReviewDate: string;
  lastReviewDate: string;
  status: 'new' | 'learning' | 'mature';
}

interface Flashcard {
  id: string;
  front: string;
  back: string;
  createdAt: number;
  srs: CardSRSState;
}

interface FlashcardDeck {
  id: string;
  name: string;
  subjectName: string | null;
  cards: Flashcard[];
  createdAt: number;
  lastStudiedAt: number | null;
}

export interface FlashcardData {
  decks: FlashcardDeck[];
  reviewStreak: { currentStreak: number; longestStreak: number; lastReviewDate: string };
  reviewHistory: { [dateKey: string]: number };
}

interface FlashcardSystemProps {
  data: FlashcardData;
  onDataChange: (data: FlashcardData) => void;
  onPointsEarn: (points: number) => void;
  subjectNames?: string[];
}

type View = 'grid' | 'detail' | 'review' | 'complete';

// ─── Constants ──────────────────────────────────────────────────────────────

const DEFAULT_SRS: CardSRSState = {
  easeFactor: 2.5,
  interval: 0,
  repetitions: 0,
  nextReviewDate: '',
  lastReviewDate: '',
  status: 'new',
};

const NEW_CARDS_PER_SESSION = 20;

const SUBJECT_BORDER_COLORS: Record<string, string> = {
  'English': 'border-l-blue-500',
  'Irish': 'border-l-emerald-500',
  'Mathematics': 'border-l-indigo-500',
  'French': 'border-l-sky-500',
  'German': 'border-l-yellow-500',
  'Spanish': 'border-l-orange-500',
  'Italian': 'border-l-red-500',
  'Japanese': 'border-l-pink-500',
  'Physics': 'border-l-cyan-500',
  'Chemistry': 'border-l-teal-500',
  'Biology': 'border-l-lime-500',
  'Applied Maths': 'border-l-violet-500',
  'Computer Science': 'border-l-fuchsia-500',
  'History': 'border-l-amber-500',
  'Geography': 'border-l-green-500',
  'Business': 'border-l-slate-500',
  'Accounting': 'border-l-zinc-500',
  'Economics': 'border-l-stone-500',
  'Art': 'border-l-rose-500',
  'Music': 'border-l-purple-500',
  'Home Economics': 'border-l-orange-500',
  'DCG': 'border-l-gray-500',
  'Construction Studies': 'border-l-yellow-600',
  'Engineering': 'border-l-blue-600',
  'Agricultural Science': 'border-l-green-600',
  'Politics & Society': 'border-l-red-600',
  'Religious Education': 'border-l-amber-600',
  'Classical Studies': 'border-l-indigo-600',
  'PE': 'border-l-emerald-600',
};

const SUBJECT_DOT_COLORS: Record<string, string> = {
  'English': 'bg-blue-500',
  'Irish': 'bg-emerald-500',
  'Mathematics': 'bg-indigo-500',
  'French': 'bg-sky-500',
  'German': 'bg-yellow-500',
  'Spanish': 'bg-orange-500',
  'Italian': 'bg-red-500',
  'Japanese': 'bg-pink-500',
  'Physics': 'bg-cyan-500',
  'Chemistry': 'bg-teal-500',
  'Biology': 'bg-lime-500',
  'Applied Maths': 'bg-violet-500',
  'Computer Science': 'bg-fuchsia-500',
  'History': 'bg-amber-500',
  'Geography': 'bg-green-500',
  'Business': 'bg-slate-500',
  'Accounting': 'bg-zinc-500',
  'Economics': 'bg-stone-500',
  'Art': 'bg-rose-500',
  'Music': 'bg-purple-500',
};

// ─── Helpers ────────────────────────────────────────────────────────────────

const genId = () => Math.random().toString(36).substring(2, 10) + Date.now().toString(36);

const toDateKey = (d: Date) => d.toISOString().split('T')[0];

const today = () => toDateKey(new Date());

const daysBetween = (a: string, b: string) => {
  const da = new Date(a + 'T00:00:00');
  const db = new Date(b + 'T00:00:00');
  return Math.round((db.getTime() - da.getTime()) / 86400000);
};

const formatInterval = (days: number): string => {
  if (days < 1) return '<1d';
  if (days < 30) return `${Math.round(days)}d`;
  if (days < 365) return `${Math.round(days / 30)}mo`;
  return `${(days / 365).toFixed(1)}y`;
};

// ─── SM-2 Algorithm ─────────────────────────────────────────────────────────

const sm2 = (srs: CardSRSState, quality: 0 | 3 | 4 | 5): CardSRSState => {
  const todayStr = today();
  let { easeFactor, interval, repetitions } = srs;

  if (quality === 0) {
    // Again — reset
    repetitions = 0;
    interval = 1;
    easeFactor = Math.max(1.3, easeFactor - 0.2);
  } else {
    // Correct answer
    if (repetitions === 0) {
      interval = 1;
    } else if (repetitions === 1) {
      interval = 6;
    } else {
      interval = Math.round(interval * easeFactor);
    }

    // Apply difficulty modifier
    if (quality === 3) {
      interval = Math.max(1, Math.round(interval * 0.8));
    } else if (quality === 5) {
      interval = Math.round(interval * 1.3);
    }

    // SM-2 ease factor update
    easeFactor = easeFactor + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02));
    easeFactor = Math.max(1.3, easeFactor);
    repetitions += 1;
  }

  const nextDate = new Date();
  nextDate.setDate(nextDate.getDate() + interval);
  const nextReviewDate = toDateKey(nextDate);

  const status: CardSRSState['status'] = interval >= 21 ? 'mature' : 'learning';

  return {
    easeFactor,
    interval,
    repetitions,
    nextReviewDate,
    lastReviewDate: todayStr,
    status,
  };
};

const getDueCards = (deck: FlashcardDeck): Flashcard[] => {
  const todayStr = today();
  const newCards: Flashcard[] = [];
  const reviewCards: Flashcard[] = [];

  for (const card of deck.cards) {
    if (card.srs.status === 'new' && !card.srs.nextReviewDate) {
      newCards.push(card);
    } else if (card.srs.nextReviewDate && card.srs.nextReviewDate <= todayStr) {
      reviewCards.push(card);
    }
  }

  // Cap new cards at 20 per session
  const cappedNew = newCards.slice(0, NEW_CARDS_PER_SESSION);
  return [...reviewCards, ...cappedNew];
};

// ─── Mastery Ring ───────────────────────────────────────────────────────────

const MasteryRing: React.FC<{ percentage: number; size?: number; strokeWidth?: number; className?: string }> = ({
  percentage, size = 48, strokeWidth = 4, className = '',
}) => {
  const radius = (size - strokeWidth) / 2;
  const circumference = 2 * Math.PI * radius;
  const offset = circumference - (percentage / 100) * circumference;

  return (
    <svg width={size} height={size} className={className}>
      <circle cx={size / 2} cy={size / 2} r={radius} fill="none"
        className="stroke-zinc-200 dark:stroke-zinc-700" strokeWidth={strokeWidth} />
      <motion.circle
        cx={size / 2} cy={size / 2} r={radius} fill="none"
        className="stroke-emerald-500" strokeWidth={strokeWidth}
        strokeLinecap="round" strokeDasharray={circumference}
        initial={{ strokeDashoffset: circumference }}
        animate={{ strokeDashoffset: offset }}
        transition={{ duration: 1, ease: 'easeOut' }}
        transform={`rotate(-90 ${size / 2} ${size / 2})`}
      />
      <text x={size / 2} y={size / 2} textAnchor="middle" dominantBaseline="central"
        className="fill-zinc-700 dark:fill-zinc-300 text-[10px] font-bold">
        {Math.round(percentage)}%
      </text>
    </svg>
  );
};

// ─── Heat Map (7×12 grid) ───────────────────────────────────────────────────

const HeatMap: React.FC<{ history: Record<string, number> }> = ({ history }) => {
  const cells = useMemo(() => {
    const result: { dateKey: string; count: number }[] = [];
    const d = new Date();
    // Go back 84 days (12 weeks)
    d.setDate(d.getDate() - 83);
    for (let i = 0; i < 84; i++) {
      const key = toDateKey(d);
      result.push({ dateKey: key, count: history[key] || 0 });
      d.setDate(d.getDate() + 1);
    }
    return result;
  }, [history]);

  const maxCount = Math.max(1, ...cells.map(c => c.count));

  const getIntensity = (count: number): string => {
    if (count === 0) return 'bg-zinc-100 dark:bg-zinc-800';
    const ratio = count / maxCount;
    if (ratio < 0.25) return 'bg-emerald-200 dark:bg-emerald-900/60';
    if (ratio < 0.5) return 'bg-emerald-300 dark:bg-emerald-700/70';
    if (ratio < 0.75) return 'bg-emerald-400 dark:bg-emerald-600/80';
    return 'bg-emerald-500 dark:bg-emerald-500';
  };

  // Display as 12 columns × 7 rows (week columns, day rows)
  return (
    <div className="flex gap-[3px]">
      {Array.from({ length: 12 }, (_, col) => (
        <div key={col} className="flex flex-col gap-[3px]">
          {Array.from({ length: 7 }, (_, row) => {
            const idx = col * 7 + row;
            const cell = cells[idx];
            return (
              <div
                key={row}
                className={`w-3 h-3 rounded-[2px] ${cell ? getIntensity(cell.count) : 'bg-zinc-100 dark:bg-zinc-800'} transition-colors`}
                title={cell ? `${cell.dateKey}: ${cell.count} cards` : ''}
              />
            );
          })}
        </div>
      ))}
    </div>
  );
};

// ─── Status Pill ────────────────────────────────────────────────────────────

const StatusPill: React.FC<{ label: string; count: number; variant: 'new' | 'learning' | 'mature' }> = ({ label, count, variant }) => {
  const styles = {
    new: 'bg-blue-100 text-blue-700 dark:bg-blue-900/40 dark:text-blue-300',
    learning: 'bg-amber-100 text-amber-700 dark:bg-amber-900/40 dark:text-amber-300',
    mature: 'bg-emerald-100 text-emerald-700 dark:bg-emerald-900/40 dark:text-emerald-300',
  };
  return (
    <span className={`inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[10px] font-bold ${styles[variant]}`}>
      {count} {label}
    </span>
  );
};

// ─── Deck Card ──────────────────────────────────────────────────────────────

const DeckCard: React.FC<{
  deck: FlashcardDeck;
  onClick: () => void;
}> = ({ deck, onClick }) => {
  const newCount = deck.cards.filter(c => c.srs.status === 'new').length;
  const learningCount = deck.cards.filter(c => c.srs.status === 'learning').length;
  const matureCount = deck.cards.filter(c => c.srs.status === 'mature').length;
  const mastery = deck.cards.length > 0 ? (matureCount / deck.cards.length) * 100 : 0;
  const dueCount = getDueCards(deck).length;
  const borderColor = deck.subjectName ? (SUBJECT_BORDER_COLORS[deck.subjectName] || 'border-l-zinc-400') : 'border-l-violet-500';

  return (
    <MotionButton
      whileHover={{ scale: 1.02, y: -2 }}
      whileTap={{ scale: 0.98 }}
      onClick={onClick}
      className={`w-full text-left p-5 rounded-2xl bg-white/80 dark:bg-zinc-900/60 backdrop-blur-xl border border-zinc-200/60 dark:border-zinc-700/40 border-l-4 ${borderColor} shadow-sm hover:shadow-lg transition-shadow`}
    >
      <div className="flex items-start justify-between gap-3">
        <div className="flex-1 min-w-0">
          <h3 className="font-serif font-semibold text-lg text-zinc-900 dark:text-white truncate">{deck.name}</h3>
          {deck.subjectName && (
            <p className="text-xs text-zinc-500 dark:text-zinc-400 mt-0.5">{deck.subjectName}</p>
          )}
          <div className="flex gap-2 mt-3 flex-wrap">
            {newCount > 0 && <StatusPill label="new" count={newCount} variant="new" />}
            {learningCount > 0 && <StatusPill label="learning" count={learningCount} variant="learning" />}
            {matureCount > 0 && <StatusPill label="mature" count={matureCount} variant="mature" />}
          </div>
        </div>
        <div className="flex flex-col items-center gap-1 flex-shrink-0">
          <MasteryRing percentage={mastery} size={48} />
          {dueCount > 0 && (
            <span className="text-[10px] font-bold text-violet-600 dark:text-violet-400">{dueCount} due</span>
          )}
        </div>
      </div>
      <div className="flex items-center justify-between mt-3 pt-3 border-t border-zinc-100 dark:border-zinc-800">
        <span className="text-xs text-zinc-400 dark:text-zinc-500">{deck.cards.length} cards</span>
        <ChevronRight size={14} className="text-zinc-400" />
      </div>
    </MotionButton>
  );
};

// ─── Create Deck Modal ──────────────────────────────────────────────────────

const COMMON_SUBJECTS = [
  'English', 'Irish', 'Mathematics', 'French', 'German', 'Spanish',
  'Physics', 'Chemistry', 'Biology', 'History', 'Geography', 'Business',
  'Accounting', 'Economics', 'Art', 'Music', 'Computer Science',
  'Applied Maths', 'Home Economics', 'Engineering',
];

const CreateDeckModal: React.FC<{
  isOpen: boolean;
  onClose: () => void;
  onCreate: (name: string, subject: string | null) => void;
  subjectNames?: string[];
}> = ({ isOpen, onClose, onCreate, subjectNames }) => {
  const [name, setName] = useState('');
  const [subject, setSubject] = useState<string | null>(null);
  const [showSubjects, setShowSubjects] = useState(false);
  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    if (isOpen) {
      setName('');
      setSubject(null);
      setShowSubjects(false);
      setTimeout(() => inputRef.current?.focus(), 100);
    }
  }, [isOpen]);

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-[100] flex items-center justify-center p-4">
      <MotionDiv
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        exit={{ opacity: 0 }}
        className="absolute inset-0 bg-black/50 backdrop-blur-sm"
        onClick={onClose}
      />
      <MotionDiv
        initial={{ opacity: 0, scale: 0.95, y: 20 }}
        animate={{ opacity: 1, scale: 1, y: 0 }}
        exit={{ opacity: 0, scale: 0.95, y: 20 }}
        className="relative w-full max-w-md bg-white dark:bg-zinc-900 rounded-3xl shadow-2xl border border-zinc-200 dark:border-zinc-700 p-8"
      >
        <h2 className="font-serif text-2xl font-semibold text-zinc-900 dark:text-white mb-6">Create New Deck</h2>

        <div className="space-y-4">
          <div>
            <label className="block text-xs font-bold text-zinc-500 dark:text-zinc-400 uppercase tracking-wider mb-2">Deck Name</label>
            <input
              ref={inputRef}
              type="text"
              value={name}
              onChange={e => setName(e.target.value)}
              placeholder="e.g. Biology Chapter 3"
              className="w-full px-4 py-3 bg-zinc-50 dark:bg-zinc-800 border border-zinc-200 dark:border-zinc-700 rounded-xl text-zinc-900 dark:text-white placeholder:text-zinc-400 focus:outline-none focus:ring-2 focus:ring-violet-500/40 transition-shadow"
              maxLength={60}
            />
          </div>

          <div>
            <button
              onClick={() => setShowSubjects(!showSubjects)}
              className="text-xs font-bold text-violet-600 dark:text-violet-400 hover:underline"
            >
              {subject ? `Subject: ${subject}` : '+ Assign to a subject'}
            </button>
            {showSubjects && (
              <div className="mt-2 space-y-2">
                {subjectNames && subjectNames.length > 0 && (
                  <>
                    <p className="text-[10px] font-bold text-zinc-400 dark:text-zinc-500 uppercase tracking-wider">Your Subjects</p>
                    <div className="flex flex-wrap gap-1.5">
                      {subjectNames.map(s => (
                        <button
                          key={s}
                          onClick={() => { setSubject(subject === s ? null : s); setShowSubjects(false); }}
                          className={`px-2.5 py-1 rounded-lg text-xs font-medium transition-colors ${subject === s
                            ? 'bg-violet-100 text-violet-700 dark:bg-violet-900/50 dark:text-violet-300'
                            : 'bg-violet-50 text-violet-600 dark:bg-violet-900/30 dark:text-violet-300 hover:bg-violet-100 dark:hover:bg-violet-900/50'
                          }`}
                        >
                          {s}
                        </button>
                      ))}
                    </div>
                    <p className="text-[10px] font-bold text-zinc-400 dark:text-zinc-500 uppercase tracking-wider pt-1">Other</p>
                  </>
                )}
                <div className="flex flex-wrap gap-1.5">
                  {COMMON_SUBJECTS.filter(s => !subjectNames?.includes(s)).map(s => (
                    <button
                      key={s}
                      onClick={() => { setSubject(subject === s ? null : s); setShowSubjects(false); }}
                      className={`px-2.5 py-1 rounded-lg text-xs font-medium transition-colors ${subject === s
                        ? 'bg-violet-100 text-violet-700 dark:bg-violet-900/50 dark:text-violet-300'
                        : 'bg-zinc-100 text-zinc-600 dark:bg-zinc-800 dark:text-zinc-400 hover:bg-zinc-200 dark:hover:bg-zinc-700'
                      }`}
                    >
                      {s}
                    </button>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>

        <div className="flex gap-3 mt-8">
          <button
            onClick={onClose}
            className="flex-1 py-3 rounded-xl border border-zinc-200 dark:border-zinc-700 text-zinc-600 dark:text-zinc-400 font-semibold text-sm hover:bg-zinc-50 dark:hover:bg-zinc-800 transition-colors"
          >
            Cancel
          </button>
          <button
            onClick={() => { if (name.trim()) { onCreate(name.trim(), subject); onClose(); } }}
            disabled={!name.trim()}
            className="flex-1 py-3 rounded-xl bg-violet-600 text-white font-semibold text-sm hover:bg-violet-700 disabled:opacity-40 disabled:cursor-not-allowed transition-colors"
          >
            Create Deck
          </button>
        </div>
      </MotionDiv>
    </div>
  );
};

// ─── Main FlashcardSystem ───────────────────────────────────────────────────

const FlashcardSystem: React.FC<FlashcardSystemProps> = ({ data, onDataChange, onPointsEarn, subjectNames }) => {
  const [view, setView] = useState<View>('grid');
  const [selectedDeckId, setSelectedDeckId] = useState<string | null>(null);
  const [showCreateModal, setShowCreateModal] = useState(false);

  // Deck detail state
  const [editingCardId, setEditingCardId] = useState<string | null>(null);
  const [editFront, setEditFront] = useState('');
  const [editBack, setEditBack] = useState('');
  const [addFront, setAddFront] = useState('');
  const [addBack, setAddBack] = useState('');

  // Review state
  const [reviewQueue, setReviewQueue] = useState<Flashcard[]>([]);
  const [reviewIndex, setReviewIndex] = useState(0);
  const [isFlipped, setIsFlipped] = useState(false);
  const [hasRated, setHasRated] = useState(false);
  const [reviewedCount, setReviewedCount] = useState(0);
  const [sessionPoints, setSessionPoints] = useState(0);

  const selectedDeck = useMemo(() => data.decks.find(d => d.id === selectedDeckId) ?? null, [data.decks, selectedDeckId]);

  // ─── Data Mutations ─────────────────────────────────────────────────────

  const updateDecks = useCallback((updater: (decks: FlashcardDeck[]) => FlashcardDeck[]) => {
    const newDecks = updater([...data.decks]);
    onDataChange({ ...data, decks: newDecks });
  }, [data, onDataChange]);

  const handleCreateDeck = useCallback((name: string, subject: string | null) => {
    const newDeck: FlashcardDeck = {
      id: genId(),
      name,
      subjectName: subject,
      cards: [],
      createdAt: Date.now(),
      lastStudiedAt: null,
    };
    onDataChange({ ...data, decks: [...data.decks, newDeck] });
    setSelectedDeckId(newDeck.id);
    setView('detail');
  }, [data, onDataChange]);

  const handleDeleteDeck = useCallback((deckId: string) => {
    updateDecks(decks => decks.filter(d => d.id !== deckId));
    setSelectedDeckId(null);
    setView('grid');
  }, [updateDecks]);

  const handleAddCard = useCallback(() => {
    if (!selectedDeckId || !addFront.trim() || !addBack.trim()) return;
    const newCard: Flashcard = {
      id: genId(),
      front: addFront.trim(),
      back: addBack.trim(),
      createdAt: Date.now(),
      srs: { ...DEFAULT_SRS },
    };
    updateDecks(decks => decks.map(d => d.id === selectedDeckId ? { ...d, cards: [...d.cards, newCard] } : d));
    setAddFront('');
    setAddBack('');
  }, [selectedDeckId, addFront, addBack, updateDecks]);

  const handleDeleteCard = useCallback((cardId: string) => {
    if (!selectedDeckId) return;
    updateDecks(decks => decks.map(d => d.id === selectedDeckId ? { ...d, cards: d.cards.filter(c => c.id !== cardId) } : d));
  }, [selectedDeckId, updateDecks]);

  const handleSaveEdit = useCallback(() => {
    if (!selectedDeckId || !editingCardId || !editFront.trim() || !editBack.trim()) return;
    updateDecks(decks => decks.map(d => d.id === selectedDeckId
      ? { ...d, cards: d.cards.map(c => c.id === editingCardId ? { ...c, front: editFront.trim(), back: editBack.trim() } : c) }
      : d
    ));
    setEditingCardId(null);
  }, [selectedDeckId, editingCardId, editFront, editBack, updateDecks]);

  // ─── Review Session ─────────────────────────────────────────────────────

  const startReview = useCallback(() => {
    if (!selectedDeck) return;
    const due = getDueCards(selectedDeck);
    if (due.length === 0) return;
    setReviewQueue(due);
    setReviewIndex(0);
    setIsFlipped(false);
    setHasRated(false);
    setReviewedCount(0);
    setSessionPoints(0);
    setView('review');
  }, [selectedDeck]);

  const handleRate = useCallback((quality: 0 | 3 | 4 | 5) => {
    const currentCard = reviewQueue[reviewIndex];
    if (!currentCard || !selectedDeckId) return;

    const updatedSrs = sm2(currentCard.srs, quality);

    // Update card in deck
    updateDecks(decks => decks.map(d => {
      if (d.id !== selectedDeckId) return d;
      return {
        ...d,
        lastStudiedAt: Date.now(),
        cards: d.cards.map(c => c.id === currentCard.id ? { ...c, srs: updatedSrs } : c),
      };
    }));

    setHasRated(true);
    const newReviewedCount = reviewedCount + 1;
    setReviewedCount(newReviewedCount);

    // Auto-advance after brief delay
    setTimeout(() => {
      if (reviewIndex + 1 < reviewQueue.length) {
        setReviewIndex(reviewIndex + 1);
        setIsFlipped(false);
        setHasRated(false);
      } else {
        // Session complete — calculate points
        const streakMultiplier = getStreakMultiplier(data.reviewStreak.currentStreak);
        const basePoints = Math.min(newReviewedCount * 2, 20);
        const earned = Math.round(basePoints * streakMultiplier);
        setSessionPoints(earned);

        // Update streak
        const todayStr = today();
        const { lastReviewDate, currentStreak, longestStreak } = data.reviewStreak;
        let newStreak = 1;
        if (lastReviewDate) {
          const diff = daysBetween(lastReviewDate, todayStr);
          if (diff === 1) newStreak = currentStreak + 1;
          else if (diff === 0) newStreak = currentStreak;
        }

        const newHistory = { ...data.reviewHistory };
        newHistory[todayStr] = (newHistory[todayStr] || 0) + newReviewedCount;

        onDataChange({
          ...data,
          decks: data.decks.map(d => {
            if (d.id !== selectedDeckId) return d;
            return {
              ...d,
              lastStudiedAt: Date.now(),
              cards: d.cards.map(c => {
                const queueCard = reviewQueue.find(q => q.id === c.id);
                return queueCard ? { ...c, srs: sm2(queueCard.srs, quality).status === c.srs.status ? c.srs : c.srs } : c;
              }),
            };
          }),
          reviewStreak: {
            currentStreak: newStreak,
            longestStreak: Math.max(longestStreak, newStreak),
            lastReviewDate: todayStr,
          },
          reviewHistory: newHistory,
        });

        onPointsEarn(earned);
        setView('complete');
      }
    }, 500);
  }, [reviewQueue, reviewIndex, selectedDeckId, updateDecks, reviewedCount, data, onDataChange, onPointsEarn]);

  const getStreakMultiplier = (streak: number): number => {
    if (streak >= 14) return 2.5;
    if (streak >= 7) return 2.0;
    if (streak >= 3) return 1.5;
    return 1.0;
  };

  // ─── Computed Stats ─────────────────────────────────────────────────────

  const globalStats = useMemo(() => {
    const allCards = data.decks.flatMap(d => d.cards);
    const totalCards = allCards.length;
    const dueToday = data.decks.reduce((sum, d) => sum + getDueCards(d).length, 0);
    const matureCards = allCards.filter(c => c.srs.status === 'mature').length;
    const mastery = totalCards > 0 ? Math.round((matureCards / totalCards) * 100) : 0;
    return { totalCards, dueToday, mastery };
  }, [data.decks]);

  // ─── Render: Deck Grid ──────────────────────────────────────────────────

  const renderGrid = () => (
    <MotionDiv initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}>
      {/* Global Stats */}
      <div className="grid grid-cols-3 gap-3 mb-8">
        {[
          { label: 'Total Cards', value: globalStats.totalCards, icon: Layers },
          { label: 'Due Today', value: globalStats.dueToday, icon: Clock },
          { label: 'Mastery', value: `${globalStats.mastery}%`, icon: Star },
        ].map(stat => (
          <div key={stat.label} className="flex items-center gap-3 p-4 rounded-2xl bg-white/70 dark:bg-zinc-900/50 backdrop-blur-xl border border-zinc-200/50 dark:border-zinc-700/30">
            <div className="p-2 rounded-xl bg-violet-100 dark:bg-violet-900/40">
              <stat.icon size={16} className="text-violet-600 dark:text-violet-400" />
            </div>
            <div>
              <p className="text-lg font-bold text-zinc-900 dark:text-white">{stat.value}</p>
              <p className="text-[10px] font-medium text-zinc-500 dark:text-zinc-400 uppercase tracking-wider">{stat.label}</p>
            </div>
          </div>
        ))}
      </div>

      {/* Streak + Heat Map */}
      {Object.keys(data.reviewHistory).length > 0 && (
        <div className="mb-8 p-5 rounded-2xl bg-white/70 dark:bg-zinc-900/50 backdrop-blur-xl border border-zinc-200/50 dark:border-zinc-700/30">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center gap-2">
              <Flame size={16} className="text-orange-500" />
              <span className="font-bold text-sm text-zinc-900 dark:text-white">
                {data.reviewStreak.currentStreak} day streak
              </span>
            </div>
            <span className="text-[10px] text-zinc-500 dark:text-zinc-400 font-medium">
              Best: {data.reviewStreak.longestStreak}d
            </span>
          </div>
          <HeatMap history={data.reviewHistory} />
        </div>
      )}

      {/* Decks */}
      <div className="flex items-center justify-between mb-4">
        <h3 className="font-serif text-xl font-semibold text-zinc-900 dark:text-white">Your Decks</h3>
        <MotionButton
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          onClick={() => setShowCreateModal(true)}
          className="flex items-center gap-1.5 px-4 py-2 rounded-xl bg-violet-600 text-white text-sm font-semibold hover:bg-violet-700 transition-colors"
        >
          <Plus size={14} /> New Deck
        </MotionButton>
      </div>

      {data.decks.length === 0 ? (
        <div className="text-center py-16">
          <div className="mx-auto w-16 h-16 rounded-2xl bg-violet-100 dark:bg-violet-900/40 flex items-center justify-center mb-4">
            <Layers size={28} className="text-violet-500" />
          </div>
          <p className="font-serif text-lg text-zinc-700 dark:text-zinc-300 mb-2">No decks yet</p>
          <p className="text-sm text-zinc-500 dark:text-zinc-400">Create your first flashcard deck to start studying.</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {data.decks.map(deck => (
            <DeckCard key={deck.id} deck={deck} onClick={() => { setSelectedDeckId(deck.id); setView('detail'); }} />
          ))}
        </div>
      )}
    </MotionDiv>
  );

  // ─── Render: Deck Detail ────────────────────────────────────────────────

  const renderDetail = () => {
    if (!selectedDeck) return null;

    const newCount = selectedDeck.cards.filter(c => c.srs.status === 'new').length;
    const learningCount = selectedDeck.cards.filter(c => c.srs.status === 'learning').length;
    const matureCount = selectedDeck.cards.filter(c => c.srs.status === 'mature').length;
    const mastery = selectedDeck.cards.length > 0 ? (matureCount / selectedDeck.cards.length) * 100 : 0;
    const dueCount = getDueCards(selectedDeck).length;

    return (
      <MotionDiv initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: -20 }}>
        {/* Back */}
        <button
          onClick={() => { setView('grid'); setSelectedDeckId(null); }}
          className="flex items-center gap-1.5 text-sm font-bold text-zinc-500 dark:text-zinc-400 hover:text-zinc-900 dark:hover:text-white mb-6 transition-colors"
        >
          <ArrowLeft size={14} /> All Decks
        </button>

        {/* Header */}
        <div className="flex items-start justify-between mb-8">
          <div>
            <h2 className="font-serif text-3xl font-semibold text-zinc-900 dark:text-white">{selectedDeck.name}</h2>
            {selectedDeck.subjectName && (
              <p className="text-sm text-zinc-500 dark:text-zinc-400 mt-1">{selectedDeck.subjectName}</p>
            )}
            <div className="flex gap-2 mt-3">
              <StatusPill label="new" count={newCount} variant="new" />
              <StatusPill label="learning" count={learningCount} variant="learning" />
              <StatusPill label="mature" count={matureCount} variant="mature" />
            </div>
          </div>
          <div className="flex flex-col items-center gap-2">
            <MasteryRing percentage={mastery} size={72} strokeWidth={5} />
          </div>
        </div>

        {/* Start Review */}
        {dueCount > 0 && (
          <MotionButton
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            onClick={startReview}
            className="w-full flex items-center justify-center gap-3 py-4 rounded-2xl bg-gradient-to-r from-violet-600 to-purple-600 text-white font-semibold text-lg shadow-lg shadow-violet-500/20 hover:shadow-violet-500/40 transition-shadow mb-8"
          >
            <Play size={20} fill="white" />
            Start Review
            <span className="ml-1 px-2.5 py-0.5 rounded-full bg-white/20 text-sm font-bold">{dueCount}</span>
          </MotionButton>
        )}

        {/* Quick Add */}
        <div className="p-4 rounded-2xl bg-white/70 dark:bg-zinc-900/50 backdrop-blur-xl border border-zinc-200/50 dark:border-zinc-700/30 mb-6">
          <p className="text-xs font-bold text-zinc-500 dark:text-zinc-400 uppercase tracking-wider mb-3">Add Card</p>
          <div className="flex flex-col sm:flex-row gap-2">
            <input
              type="text"
              value={addFront}
              onChange={e => setAddFront(e.target.value)}
              placeholder="Front (question)"
              className="flex-1 px-3 py-2.5 bg-zinc-50 dark:bg-zinc-800 border border-zinc-200 dark:border-zinc-700 rounded-xl text-sm text-zinc-900 dark:text-white placeholder:text-zinc-400 focus:outline-none focus:ring-2 focus:ring-violet-500/40"
              onKeyDown={e => { if (e.key === 'Enter' && addFront.trim() && addBack.trim()) handleAddCard(); }}
            />
            <input
              type="text"
              value={addBack}
              onChange={e => setAddBack(e.target.value)}
              placeholder="Back (answer)"
              className="flex-1 px-3 py-2.5 bg-zinc-50 dark:bg-zinc-800 border border-zinc-200 dark:border-zinc-700 rounded-xl text-sm text-zinc-900 dark:text-white placeholder:text-zinc-400 focus:outline-none focus:ring-2 focus:ring-violet-500/40"
              onKeyDown={e => { if (e.key === 'Enter' && addFront.trim() && addBack.trim()) handleAddCard(); }}
            />
            <MotionButton
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={handleAddCard}
              disabled={!addFront.trim() || !addBack.trim()}
              className="px-5 py-2.5 rounded-xl bg-violet-600 text-white text-sm font-semibold disabled:opacity-40 disabled:cursor-not-allowed hover:bg-violet-700 transition-colors"
            >
              <Plus size={16} />
            </MotionButton>
          </div>
        </div>

        {/* Card List */}
        <div className="space-y-2">
          {selectedDeck.cards.length === 0 ? (
            <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 py-8">No cards yet. Add your first card above.</p>
          ) : (
            selectedDeck.cards.map(card => {
              const statusDot = card.srs.status === 'new'
                ? 'bg-blue-500'
                : card.srs.status === 'learning' ? 'bg-amber-500' : 'bg-emerald-500';

              if (editingCardId === card.id) {
                return (
                  <div key={card.id} className="p-3 rounded-xl bg-white dark:bg-zinc-800 border border-violet-200 dark:border-violet-700">
                    <div className="flex flex-col sm:flex-row gap-2 mb-2">
                      <input
                        type="text"
                        value={editFront}
                        onChange={e => setEditFront(e.target.value)}
                        className="flex-1 px-3 py-2 bg-zinc-50 dark:bg-zinc-900 border border-zinc-200 dark:border-zinc-700 rounded-lg text-sm text-zinc-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-violet-500/40"
                      />
                      <input
                        type="text"
                        value={editBack}
                        onChange={e => setEditBack(e.target.value)}
                        className="flex-1 px-3 py-2 bg-zinc-50 dark:bg-zinc-900 border border-zinc-200 dark:border-zinc-700 rounded-lg text-sm text-zinc-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-violet-500/40"
                      />
                    </div>
                    <div className="flex gap-2 justify-end">
                      <button onClick={() => setEditingCardId(null)} className="px-3 py-1.5 text-xs font-medium text-zinc-500 hover:text-zinc-700 dark:hover:text-zinc-300">Cancel</button>
                      <button onClick={handleSaveEdit} className="px-3 py-1.5 text-xs font-bold text-violet-600 dark:text-violet-400 hover:underline">Save</button>
                    </div>
                  </div>
                );
              }

              return (
                <div key={card.id} className="group flex items-center gap-3 p-3 rounded-xl bg-white/60 dark:bg-zinc-900/40 border border-zinc-100 dark:border-zinc-800 hover:border-zinc-300 dark:hover:border-zinc-600 transition-colors">
                  <div className={`w-2 h-2 rounded-full flex-shrink-0 ${statusDot}`} />
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-medium text-zinc-800 dark:text-zinc-200 truncate">{card.front}</p>
                  </div>
                  {card.srs.nextReviewDate && (
                    <span className="text-[10px] text-zinc-400 dark:text-zinc-500 font-medium flex-shrink-0">
                      {card.srs.nextReviewDate <= today() ? 'Due' : card.srs.nextReviewDate}
                    </span>
                  )}
                  <div className="flex gap-1 opacity-0 group-hover:opacity-100 transition-opacity flex-shrink-0">
                    <button
                      onClick={() => { setEditingCardId(card.id); setEditFront(card.front); setEditBack(card.back); }}
                      className="p-1.5 rounded-lg hover:bg-zinc-100 dark:hover:bg-zinc-800 text-zinc-400 hover:text-zinc-600 dark:hover:text-zinc-300 transition-colors"
                    >
                      <Edit3 size={12} />
                    </button>
                    <button
                      onClick={() => handleDeleteCard(card.id)}
                      className="p-1.5 rounded-lg hover:bg-rose-50 dark:hover:bg-rose-900/30 text-zinc-400 hover:text-rose-500 transition-colors"
                    >
                      <Trash2 size={12} />
                    </button>
                  </div>
                </div>
              );
            })
          )}
        </div>

        {/* Delete Deck */}
        <div className="mt-8 pt-6 border-t border-zinc-200 dark:border-zinc-800">
          <button
            onClick={() => { if (window.confirm('Delete this deck and all its cards?')) handleDeleteDeck(selectedDeck.id); }}
            className="text-xs font-medium text-rose-500 hover:text-rose-600 dark:hover:text-rose-400 hover:underline transition-colors"
          >
            Delete Deck
          </button>
        </div>
      </MotionDiv>
    );
  };

  // ─── Render: Review Session ─────────────────────────────────────────────

  const renderReview = () => {
    const currentCard = reviewQueue[reviewIndex];
    if (!currentCard) return null;

    const progress = ((reviewIndex + 1) / reviewQueue.length) * 100;
    const currentSrs = currentCard.srs;

    // Compute preview intervals for each rating
    const previewIntervals = {
      again: formatInterval(1),
      hard: formatInterval(Math.max(1, currentSrs.repetitions === 0 ? 1 : Math.round((currentSrs.repetitions === 1 ? 6 : currentSrs.interval * currentSrs.easeFactor) * 0.8))),
      good: formatInterval(currentSrs.repetitions === 0 ? 1 : currentSrs.repetitions === 1 ? 6 : Math.round(currentSrs.interval * currentSrs.easeFactor)),
      easy: formatInterval(Math.round((currentSrs.repetitions === 0 ? 1 : currentSrs.repetitions === 1 ? 6 : currentSrs.interval * currentSrs.easeFactor) * 1.3)),
    };

    return (
      <MotionDiv initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} className="max-w-lg mx-auto">
        {/* Progress bar */}
        <div className="mb-8">
          <div className="flex items-center justify-between mb-2">
            <button
              onClick={() => { setView('detail'); }}
              className="text-sm font-bold text-zinc-500 dark:text-zinc-400 hover:text-zinc-900 dark:hover:text-white transition-colors"
            >
              <X size={18} />
            </button>
            <span className="text-sm font-bold text-zinc-500 dark:text-zinc-400">
              {reviewIndex + 1} / {reviewQueue.length}
            </span>
          </div>
          <div className="w-full h-2 bg-zinc-200 dark:bg-zinc-800 rounded-full overflow-hidden">
            <motion.div
              className="h-full bg-gradient-to-r from-violet-500 to-purple-500 rounded-full"
              initial={{ width: 0 }}
              animate={{ width: `${progress}%` }}
              transition={{ duration: 0.4, ease: 'easeOut' }}
            />
          </div>
        </div>

        {/* 3D Flipping Card */}
        <div
          className="relative w-full cursor-pointer mb-8"
          style={{ perspective: '1200px' }}
          onClick={() => { if (!isFlipped) setIsFlipped(true); }}
        >
          <AnimatePresence mode="wait">
            <motion.div
              key={`${currentCard.id}-${reviewIndex}`}
              initial={{ x: 80, opacity: 0 }}
              animate={{ x: 0, opacity: 1 }}
              exit={{ x: -80, opacity: 0 }}
              transition={{ duration: 0.3 }}
            >
              <motion.div
                className="relative w-full"
                style={{ transformStyle: 'preserve-3d' }}
                animate={{ rotateY: isFlipped ? 180 : 0 }}
                transition={{ duration: 0.6, ease: [0.23, 1, 0.32, 1] }}
              >
                {/* Front */}
                <div
                  className="w-full min-h-[320px] p-8 rounded-3xl bg-white/90 dark:bg-zinc-900/80 backdrop-blur-2xl border border-zinc-200/60 dark:border-zinc-700/40 shadow-xl shadow-violet-500/5 flex flex-col items-center justify-center text-center"
                  style={{ backfaceVisibility: 'hidden' }}
                >
                  <span className="text-[10px] font-bold text-violet-500 dark:text-violet-400 uppercase tracking-[0.2em] mb-6">Question</span>
                  <p className="font-serif text-2xl md:text-3xl leading-relaxed text-zinc-900 dark:text-white font-medium">{currentCard.front}</p>
                  {!isFlipped && (
                    <p className="mt-8 text-xs text-zinc-400 dark:text-zinc-500 font-medium">Tap to reveal</p>
                  )}
                </div>

                {/* Back */}
                <div
                  className="absolute inset-0 w-full min-h-[320px] p-8 rounded-3xl bg-white/90 dark:bg-zinc-900/80 backdrop-blur-2xl border border-purple-200/60 dark:border-purple-700/40 shadow-xl shadow-purple-500/10 flex flex-col items-center justify-center text-center"
                  style={{ backfaceVisibility: 'hidden', transform: 'rotateY(180deg)' }}
                >
                  <span className="text-[10px] font-bold text-purple-500 dark:text-purple-400 uppercase tracking-[0.2em] mb-6">Answer</span>
                  <p className="font-serif text-2xl md:text-3xl leading-relaxed text-zinc-900 dark:text-white font-medium">{currentCard.back}</p>
                </div>
              </motion.div>
            </motion.div>
          </AnimatePresence>
        </div>

        {/* Rating Buttons */}
        <AnimatePresence>
          {isFlipped && !hasRated && (
            <MotionDiv
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: 10 }}
              className="grid grid-cols-4 gap-2"
            >
              {[
                { quality: 0 as const, label: 'Again', interval: previewIntervals.again, bg: 'bg-rose-100 dark:bg-rose-900/40 hover:bg-rose-200 dark:hover:bg-rose-900/60', text: 'text-rose-700 dark:text-rose-300', border: 'border-rose-200 dark:border-rose-800/40' },
                { quality: 3 as const, label: 'Hard', interval: previewIntervals.hard, bg: 'bg-amber-100 dark:bg-amber-900/40 hover:bg-amber-200 dark:hover:bg-amber-900/60', text: 'text-amber-700 dark:text-amber-300', border: 'border-amber-200 dark:border-amber-800/40' },
                { quality: 4 as const, label: 'Good', interval: previewIntervals.good, bg: 'bg-emerald-100 dark:bg-emerald-900/40 hover:bg-emerald-200 dark:hover:bg-emerald-900/60', text: 'text-emerald-700 dark:text-emerald-300', border: 'border-emerald-200 dark:border-emerald-800/40' },
                { quality: 5 as const, label: 'Easy', interval: previewIntervals.easy, bg: 'bg-blue-100 dark:bg-blue-900/40 hover:bg-blue-200 dark:hover:bg-blue-900/60', text: 'text-blue-700 dark:text-blue-300', border: 'border-blue-200 dark:border-blue-800/40' },
              ].map((btn, idx) => (
                <MotionButton
                  key={btn.quality}
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: idx * 0.05 }}
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  onClick={() => handleRate(btn.quality)}
                  className={`flex flex-col items-center gap-1 py-3 px-2 rounded-xl border ${btn.bg} ${btn.border} ${btn.text} transition-colors`}
                >
                  <span className="text-sm font-bold">{btn.label}</span>
                  <span className="text-[10px] opacity-70">{btn.interval}</span>
                </MotionButton>
              ))}
            </MotionDiv>
          )}
        </AnimatePresence>
      </MotionDiv>
    );
  };

  // ─── Render: Review Complete ────────────────────────────────────────────

  const renderComplete = () => {
    const deck = selectedDeck;
    if (!deck) return null;

    const newCount = deck.cards.filter(c => c.srs.status === 'new').length;
    const learningCount = deck.cards.filter(c => c.srs.status === 'learning').length;
    const matureCount = deck.cards.filter(c => c.srs.status === 'mature').length;
    const total = deck.cards.length || 1;

    return (
      <MotionDiv
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        className="max-w-md mx-auto text-center py-8"
      >
        {/* Animated checkmark */}
        <div className="mx-auto mb-6 relative">
          <svg width="96" height="96" viewBox="0 0 96 96" className="mx-auto">
            <motion.circle
              cx="48" cy="48" r="42" fill="none"
              className="stroke-emerald-500"
              strokeWidth="4" strokeLinecap="round"
              initial={{ pathLength: 0 }}
              animate={{ pathLength: 1 }}
              transition={{ duration: 0.8, ease: 'easeOut' }}
            />
            <motion.path
              d="M30 50 L42 62 L66 38"
              fill="none"
              className="stroke-emerald-500"
              strokeWidth="4" strokeLinecap="round" strokeLinejoin="round"
              initial={{ pathLength: 0 }}
              animate={{ pathLength: 1 }}
              transition={{ duration: 0.5, delay: 0.5, ease: 'easeOut' }}
            />
          </svg>
        </div>

        <h2 className="font-serif text-3xl font-semibold text-zinc-900 dark:text-white mb-2">Session Complete!</h2>
        <p className="text-zinc-500 dark:text-zinc-400 mb-6">You reviewed {reviewedCount} cards</p>

        {/* Points Banner */}
        {sessionPoints > 0 && (
          <MotionDiv
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.8 }}
            className="inline-flex items-center gap-2 px-6 py-3 rounded-2xl bg-amber-100/80 dark:bg-amber-900/30 border border-amber-200 dark:border-amber-700/40 mb-8"
          >
            <Sparkles size={18} className="text-amber-600 dark:text-amber-400" />
            <span className="font-bold text-amber-700 dark:text-amber-300">+{sessionPoints} points earned</span>
            {data.reviewStreak.currentStreak >= 3 && (
              <span className="text-xs text-amber-600/70 dark:text-amber-400/60">({getStreakMultiplier(data.reviewStreak.currentStreak)}x streak)</span>
            )}
          </MotionDiv>
        )}

        {/* Mastery Distribution */}
        <div className="p-5 rounded-2xl bg-white/70 dark:bg-zinc-900/50 backdrop-blur-xl border border-zinc-200/50 dark:border-zinc-700/30 mb-8 text-left">
          <p className="text-xs font-bold text-zinc-500 dark:text-zinc-400 uppercase tracking-wider mb-4">Card Distribution</p>
          {[
            { label: 'New', count: newCount, color: 'bg-blue-500', bgTrack: 'bg-blue-100 dark:bg-blue-900/30' },
            { label: 'Learning', count: learningCount, color: 'bg-amber-500', bgTrack: 'bg-amber-100 dark:bg-amber-900/30' },
            { label: 'Mature', count: matureCount, color: 'bg-emerald-500', bgTrack: 'bg-emerald-100 dark:bg-emerald-900/30' },
          ].map(bar => (
            <div key={bar.label} className="mb-3 last:mb-0">
              <div className="flex justify-between text-xs mb-1">
                <span className="font-medium text-zinc-600 dark:text-zinc-400">{bar.label}</span>
                <span className="font-bold text-zinc-700 dark:text-zinc-300">{bar.count}</span>
              </div>
              <div className={`w-full h-2 rounded-full ${bar.bgTrack} overflow-hidden`}>
                <motion.div
                  className={`h-full rounded-full ${bar.color}`}
                  initial={{ width: 0 }}
                  animate={{ width: `${(bar.count / total) * 100}%` }}
                  transition={{ duration: 0.8, delay: 0.3, ease: 'easeOut' }}
                />
              </div>
            </div>
          ))}
        </div>

        {/* Actions */}
        <div className="flex gap-3">
          <MotionButton
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            onClick={() => { setView('detail'); }}
            className="flex-1 py-3 rounded-xl border border-zinc-200 dark:border-zinc-700 text-zinc-600 dark:text-zinc-400 font-semibold text-sm hover:bg-zinc-50 dark:hover:bg-zinc-800 transition-colors"
          >
            Back to Deck
          </MotionButton>
          <MotionButton
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            onClick={() => { setView('grid'); setSelectedDeckId(null); }}
            className="flex-1 py-3 rounded-xl bg-violet-600 text-white font-semibold text-sm hover:bg-violet-700 transition-colors"
          >
            All Decks
          </MotionButton>
        </div>
      </MotionDiv>
    );
  };

  // ─── Main Render ────────────────────────────────────────────────────────

  return (
    <div>
      <AnimatePresence mode="wait">
        {view === 'grid' && <div key="grid">{renderGrid()}</div>}
        {view === 'detail' && <div key="detail">{renderDetail()}</div>}
        {view === 'review' && <div key="review">{renderReview()}</div>}
        {view === 'complete' && <div key="complete">{renderComplete()}</div>}
      </AnimatePresence>

      <CreateDeckModal
        isOpen={showCreateModal}
        onClose={() => setShowCreateModal(false)}
        onCreate={handleCreateDeck}
        subjectNames={subjectNames}
      />
    </div>
  );
};

export default FlashcardSystem;
