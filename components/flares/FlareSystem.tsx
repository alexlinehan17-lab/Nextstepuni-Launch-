/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState, useEffect, useCallback, useRef } from 'react';
import { AnimatePresence } from 'framer-motion';
import { MotionButton, MotionDiv } from '../Motion';
import { createPortal } from 'react-dom';
import { X, Send, RefreshCw, ThumbsUp, CheckCircle, AlertCircle, MessageCircle, Flame, Radio } from 'lucide-react';
import { containsProfanity } from './profanityFilter';
import { useFlares, type FlareResponse } from '../../hooks/useFlares';

// ─── Types ──────────────────────────────────────────────────────────────────

interface FlareSystemProps {
  isOpen: boolean;
  onClose: () => void;
  initialView: 'launcher' | 'feed';
  uid: string;
  school: string;
  subjects: string[];
}

type FlareTab = 'launcher' | 'feed' | 'my-flares' | 'stats';

// ─── Constants ──────────────────────────────────────────────────────────────

const SUBJECT_COLORS: Record<string, { bg: string; text: string; border: string; ring: string }> = {
  English: { bg: 'bg-blue-500/10', text: 'text-blue-400', border: 'border-blue-500/20', ring: 'ring-blue-500' },
  Irish: { bg: 'bg-emerald-500/10', text: 'text-emerald-400', border: 'border-emerald-500/20', ring: 'ring-emerald-500' },
  Mathematics: { bg: 'bg-purple-500/10', text: 'text-purple-400', border: 'border-purple-500/20', ring: 'ring-purple-500' },
  Biology: { bg: 'bg-green-500/10', text: 'text-green-400', border: 'border-green-500/20', ring: 'ring-green-500' },
  Chemistry: { bg: 'bg-cyan-500/10', text: 'text-cyan-400', border: 'border-cyan-500/20', ring: 'ring-cyan-500' },
  Physics: { bg: 'bg-orange-500/10', text: 'text-orange-400', border: 'border-orange-500/20', ring: 'ring-orange-500' },
  History: { bg: 'bg-amber-500/10', text: 'text-amber-400', border: 'border-amber-500/20', ring: 'ring-amber-500' },
  Geography: { bg: 'bg-teal-500/10', text: 'text-teal-400', border: 'border-teal-500/20', ring: 'ring-teal-500' },
  Business: { bg: 'bg-indigo-500/10', text: 'text-indigo-400', border: 'border-indigo-500/20', ring: 'ring-indigo-500' },
  French: { bg: 'bg-rose-500/10', text: 'text-rose-400', border: 'border-rose-500/20', ring: 'ring-rose-500' },
  German: { bg: 'bg-yellow-500/10', text: 'text-yellow-400', border: 'border-yellow-500/20', ring: 'ring-yellow-500' },
  Spanish: { bg: 'bg-red-500/10', text: 'text-red-400', border: 'border-red-500/20', ring: 'ring-red-500' },
  Accounting: { bg: 'bg-lime-500/10', text: 'text-lime-400', border: 'border-lime-500/20', ring: 'ring-lime-500' },
  Economics: { bg: 'bg-sky-500/10', text: 'text-sky-400', border: 'border-sky-500/20', ring: 'ring-sky-500' },
  Art: { bg: 'bg-pink-500/10', text: 'text-pink-400', border: 'border-pink-500/20', ring: 'ring-pink-500' },
  Music: { bg: 'bg-violet-500/10', text: 'text-violet-400', border: 'border-violet-500/20', ring: 'ring-violet-500' },
  DCG: { bg: 'bg-slate-500/10', text: 'text-slate-400', border: 'border-slate-500/20', ring: 'ring-slate-500' },
  Engineering: { bg: 'bg-zinc-500/10', text: 'text-zinc-400', border: 'border-zinc-500/20', ring: 'ring-zinc-400' },
};

const DEFAULT_COLOR = { bg: 'bg-zinc-500/10', text: 'text-zinc-400', border: 'border-zinc-500/20', ring: 'ring-zinc-400' };

const TAB_ITEMS: { key: FlareTab; label: string; icon: React.ReactNode }[] = [
  { key: 'launcher', label: 'Launch', icon: <Flame size={13} /> },
  { key: 'feed', label: 'Feed', icon: <Radio size={13} /> },
  { key: 'my-flares', label: 'My Flares', icon: <MessageCircle size={13} /> },
  { key: 'stats', label: 'Stats', icon: <ThumbsUp size={13} /> },
];

const LIGHTHOUSE_LEVELS = [
  { threshold: 0, label: 'No Light', next: 5 },
  { threshold: 5, label: 'Lantern', next: 15 },
  { threshold: 15, label: 'Lighthouse', next: 30 },
  { threshold: 30, label: 'Beacon Tower', next: null },
];

// ─── Helpers ────────────────────────────────────────────────────────────────

function timeAgo(date: Date): string {
  const mins = Math.floor((Date.now() - date.getTime()) / 60000);
  if (mins < 1) return 'just now';
  if (mins < 60) return `${mins}m ago`;
  const hrs = Math.floor(mins / 60);
  if (hrs < 24) return `${hrs}h ago`;
  return `${Math.floor(hrs / 24)}d ago`;
}

function getSubjectColors(subject: string) {
  return SUBJECT_COLORS[subject] ?? DEFAULT_COLOR;
}

function getLighthouseInfo(rescueCount: number) {
  let current = LIGHTHOUSE_LEVELS[0];
  for (const level of LIGHTHOUSE_LEVELS) {
    if (rescueCount >= level.threshold) current = level;
  }
  const idx = LIGHTHOUSE_LEVELS.indexOf(current);
  const nextLevel = idx < LIGHTHOUSE_LEVELS.length - 1 ? LIGHTHOUSE_LEVELS[idx + 1] : null;
  const remaining = nextLevel ? nextLevel.threshold - rescueCount : 0;
  const nextLabel = nextLevel?.label ?? null;
  return { level: idx, label: current.label, remaining, nextLabel };
}

// ─── Sub-components ─────────────────────────────────────────────────────────

/** Subject pill badge */
const SubjectPill: React.FC<{ subject: string; className?: string }> = ({ subject, className = '' }) => {
  const colors = getSubjectColors(subject);
  return (
    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-[10px] font-semibold uppercase tracking-wider border ${colors.bg} ${colors.text} ${colors.border} ${className}`}>
      {subject}
    </span>
  );
};

/** Lighthouse SVG visualization */
const LighthouseVis: React.FC<{ level: number }> = ({ level }) => {
  if (level === 0) {
    return (
      <div className="w-24 h-32 mx-auto flex items-center justify-center">
        <svg viewBox="0 0 60 80" className="w-full h-full opacity-20">
          <rect x="20" y="20" width="20" height="50" rx="2" fill="none" stroke="#71717a" strokeWidth="2" strokeDasharray="4 2" />
          <polygon points="15,20 45,20 40,8 20,8" fill="none" stroke="#71717a" strokeWidth="2" strokeDasharray="4 2" />
          <circle cx="30" cy="14" r="4" fill="none" stroke="#71717a" strokeWidth="1.5" strokeDasharray="3 2" />
          <rect x="16" y="70" width="28" height="4" rx="2" fill="none" stroke="#71717a" strokeWidth="2" strokeDasharray="4 2" />
        </svg>
      </div>
    );
  }

  if (level === 1) {
    return (
      <div className="w-24 h-32 mx-auto flex items-center justify-center">
        <svg viewBox="0 0 60 80" className="w-full h-full">
          <rect x="22" y="30" width="16" height="40" rx="2" fill="#78716c" />
          <polygon points="18,30 42,30 38,18 22,18" fill="#a8a29e" />
          <circle cx="30" cy="24" r="5" fill="#fbbf24">
            <animate attributeName="opacity" values="0.7;1;0.7" dur="2s" repeatCount="indefinite" />
          </circle>
          <rect x="18" y="70" width="24" height="4" rx="2" fill="#57534e" />
        </svg>
      </div>
    );
  }

  if (level === 2) {
    return (
      <div className="w-24 h-32 mx-auto flex items-center justify-center">
        <svg viewBox="0 0 60 80" className="w-full h-full">
          <rect x="20" y="25" width="20" height="45" rx="2" fill="#78716c" />
          <rect x="24" y="40" width="5" height="6" rx="1" fill="#fbbf24" opacity="0.4" />
          <rect x="31" y="40" width="5" height="6" rx="1" fill="#fbbf24" opacity="0.4" />
          <rect x="24" y="52" width="5" height="6" rx="1" fill="#fbbf24" opacity="0.3" />
          <rect x="31" y="52" width="5" height="6" rx="1" fill="#fbbf24" opacity="0.3" />
          <polygon points="16,25 44,25 40,10 20,10" fill="#a8a29e" />
          <circle cx="30" cy="17" r="6" fill="#f59e0b">
            <animate attributeName="opacity" values="0.8;1;0.8" dur="1.5s" repeatCount="indefinite" />
          </circle>
          <circle cx="30" cy="17" r="10" fill="#fbbf24" opacity="0.15">
            <animate attributeName="r" values="10;14;10" dur="2s" repeatCount="indefinite" />
            <animate attributeName="opacity" values="0.15;0.05;0.15" dur="2s" repeatCount="indefinite" />
          </circle>
          <rect x="16" y="70" width="28" height="4" rx="2" fill="#57534e" />
        </svg>
      </div>
    );
  }

  // Level 3: Beacon Tower
  return (
    <div className="w-28 h-36 mx-auto flex items-center justify-center">
      <svg viewBox="0 0 70 90" className="w-full h-full">
        <rect x="22" y="28" width="26" height="50" rx="3" fill="#78716c" />
        <rect x="26" y="42" width="6" height="7" rx="1" fill="#fbbf24" opacity="0.5" />
        <rect x="34" y="42" width="6" height="7" rx="1" fill="#fbbf24" opacity="0.5" />
        <rect x="26" y="55" width="6" height="7" rx="1" fill="#fbbf24" opacity="0.4" />
        <rect x="34" y="55" width="6" height="7" rx="1" fill="#fbbf24" opacity="0.4" />
        <rect x="26" y="67" width="6" height="5" rx="1" fill="#fbbf24" opacity="0.3" />
        <rect x="34" y="67" width="6" height="5" rx="1" fill="#fbbf24" opacity="0.3" />
        <polygon points="17,28 53,28 48,12 22,12" fill="#a8a29e" />
        <circle cx="35" cy="20" r="7" fill="#f59e0b">
          <animate attributeName="opacity" values="0.9;1;0.9" dur="1s" repeatCount="indefinite" />
        </circle>
        <circle cx="35" cy="20" r="14" fill="#fbbf24" opacity="0.12">
          <animate attributeName="r" values="14;22;14" dur="2.5s" repeatCount="indefinite" />
          <animate attributeName="opacity" values="0.12;0.03;0.12" dur="2.5s" repeatCount="indefinite" />
        </circle>
        <circle cx="35" cy="20" r="20" fill="#fbbf24" opacity="0.06">
          <animate attributeName="r" values="20;30;20" dur="3s" repeatCount="indefinite" />
          <animate attributeName="opacity" values="0.06;0.01;0.06" dur="3s" repeatCount="indefinite" />
        </circle>
        <line x1="35" y1="20" x2="0" y2="10" stroke="#fbbf24" strokeWidth="2" opacity="0.15">
          <animateTransform attributeName="transform" type="rotate" from="0 35 20" to="360 35 20" dur="6s" repeatCount="indefinite" />
        </line>
        <rect x="18" y="78" width="34" height="5" rx="2" fill="#57534e" />
      </svg>
    </div>
  );
};

// ─── Main Component ─────────────────────────────────────────────────────────

const FlareSystem: React.FC<FlareSystemProps> = ({
  isOpen,
  onClose,
  initialView,
  uid,
  school,
  subjects,
}) => {
  const [activeTab, setActiveTab] = useState<FlareTab>(initialView);
  const [selectedSubject, setSelectedSubject] = useState<string | null>(null);
  const [questionText, setQuestionText] = useState('');
  const [profanityError, setProfanityError] = useState(false);
  const [sendSuccess, setSendSuccess] = useState(false);
  const [expandedFlareId, setExpandedFlareId] = useState<string | null>(null);
  const [responseText, setResponseText] = useState('');
  const [responseProfanityError, setResponseProfanityError] = useState(false);
  const [loadedResponses, setLoadedResponses] = useState<Record<string, FlareResponse[]>>({});
  const [loadingResponses, setLoadingResponses] = useState<Record<string, boolean>>({});
  const [isSending, setIsSending] = useState(false);
  const [isResponding, setIsResponding] = useState(false);
  const [sendError, setSendError] = useState<string | null>(null);
  const [respondError, setRespondError] = useState<string | null>(null);

  const textareaRef = useRef<HTMLTextAreaElement>(null);
  const responseTextareaRef = useRef<HTMLTextAreaElement>(null);

  const {
    activeFlares,
    myFlares,
    rescueCount,
    _lighthouseLevel,
    flareCounts,
    isLoading,
    sendFlare,
    respondToFlare,
    getResponses,
    markHelpful,
    resolveFlare,
    reload,
  } = useFlares(uid, school, subjects);

  // Reset tab to initialView when modal opens
  useEffect(() => {
    if (isOpen) {
      setActiveTab(initialView);
    }
  }, [isOpen, initialView]);

  // ─── Handlers ───────────────────────────────────────────────────────────

  const handleQuestionBlur = useCallback(() => {
    if (questionText.trim() && containsProfanity(questionText)) {
      setProfanityError(true);
    } else {
      setProfanityError(false);
    }
  }, [questionText]);

  const handleSendFlare = useCallback(async () => {
    if (!selectedSubject || !questionText.trim() || isSending) return;
    if (containsProfanity(questionText)) {
      setProfanityError(true);
      return;
    }
    setIsSending(true);
    setSendError(null);
    try {
      const result = await sendFlare(selectedSubject, questionText.trim());
      if (result.ok) {
        setSendSuccess(true);
        setQuestionText('');
        setSelectedSubject(null);
        setProfanityError(false);
        setTimeout(() => setSendSuccess(false), 2000);
      } else {
        setSendError(result.error || 'Failed to send flare.');
      }
    } catch {
      setSendError('Something went wrong. Try again.');
    } finally {
      setIsSending(false);
    }
  }, [selectedSubject, questionText, isSending, sendFlare]);

  const handleRespondToFlare = useCallback(async (flareId: string) => {
    if (!responseText.trim() || isResponding) return;
    if (containsProfanity(responseText)) {
      setResponseProfanityError(true);
      return;
    }
    setIsResponding(true);
    setRespondError(null);
    try {
      const result = await respondToFlare(flareId, responseText.trim());
      if (result.ok) {
        setResponseText('');
        setExpandedFlareId(null);
        setResponseProfanityError(false);
        const responses = await getResponses(flareId);
        setLoadedResponses(prev => ({ ...prev, [flareId]: responses }));
      } else {
        setRespondError(result.error || 'Failed to send response.');
      }
    } catch {
      setRespondError('Something went wrong. Try again.');
    } finally {
      setIsResponding(false);
    }
  }, [responseText, isResponding, respondToFlare, getResponses]);

  const handleLoadResponses = useCallback(async (flareId: string) => {
    if (loadingResponses[flareId]) return;
    setLoadingResponses(prev => ({ ...prev, [flareId]: true }));
    try {
      const responses = await getResponses(flareId);
      setLoadedResponses(prev => ({ ...prev, [flareId]: responses }));
    } finally {
      setLoadingResponses(prev => ({ ...prev, [flareId]: false }));
    }
  }, [loadingResponses, getResponses]);

  const handleMarkHelpful = useCallback(async (flareId: string, responseId: string) => {
    await markHelpful(flareId, responseId);
    const responses = await getResponses(flareId);
    setLoadedResponses(prev => ({ ...prev, [flareId]: responses }));
  }, [markHelpful, getResponses]);

  const handleResolveFlare = useCallback(async (flareId: string) => {
    await resolveFlare(flareId);
  }, [resolveFlare]);

  const canSendFlare = selectedSubject && questionText.trim().length > 0 && !profanityError && !isSending;

  const lighthouseInfo = getLighthouseInfo(rescueCount);

  const myActiveFlares = myFlares.filter(f => f.status === 'active');

  // ─── Render ─────────────────────────────────────────────────────────────

  return createPortal(
    <AnimatePresence>
      {isOpen && (
        <MotionDiv
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          className="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center z-[200] p-4"
          onClick={onClose}
        >
          <MotionDiv
            initial={{ scale: 0.96, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            exit={{ scale: 0.96, opacity: 0 }}
            transition={{ duration: 0.2, ease: [0.16, 1, 0.3, 1] }}
            className="relative bg-white dark:bg-zinc-900 border border-zinc-200/50 dark:border-white/[0.08] rounded-2xl w-full max-w-md shadow-[0_24px_64px_rgba(0,0,0,0.12)] dark:shadow-[0_24px_64px_rgba(0,0,0,0.5)] overflow-hidden max-h-[90vh] flex flex-col"
            onClick={(e: React.MouseEvent) => e.stopPropagation()}
          >
            {/* Ambient glow */}
            <div className="absolute top-0 left-1/2 -translate-x-1/2 w-64 h-32 bg-amber-500/[0.07] rounded-full blur-3xl pointer-events-none" />

            {/* Header */}
            <div className="relative flex items-center justify-between p-6 pb-4">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-amber-500/20 to-orange-500/20 border border-amber-500/20 flex items-center justify-center">
                  <svg width="18" height="18" viewBox="0 0 24 24" fill="none">
                    <path d="M12 2L14.5 8.5L21 9.5L16.5 14.5L17.5 21L12 18L6.5 21L7.5 14.5L3 9.5L9.5 8.5L12 2Z" fill="#f59e0b" opacity="0.9" />
                    <path d="M12 2L14.5 8.5L21 9.5L16.5 14.5L17.5 21L12 18L6.5 21L7.5 14.5L3 9.5L9.5 8.5L12 2Z" stroke="#f59e0b" strokeWidth="1.5" fill="none" />
                  </svg>
                </div>
                <div>
                  <h2 className="font-sans text-xl font-semibold text-zinc-900 dark:text-white tracking-tight">
                    SOS Flare
                  </h2>
                  <p className="text-[10px] font-mono font-bold uppercase tracking-[0.3em] text-zinc-400 dark:text-white/30 mt-0.5">
                    Peer Help
                  </p>
                </div>
              </div>
              <button
                onClick={onClose}
                className="text-zinc-400 dark:text-white/25 hover:text-zinc-600 dark:hover:text-white/50 transition-colors"
              >
                <X size={18} />
              </button>
            </div>

            {/* Tab Bar */}
            <div className="relative px-6 pb-4">
              <div className="flex rounded-xl bg-zinc-100 dark:bg-white/[0.04] border border-zinc-200/50 dark:border-white/[0.06] p-1 gap-1">
                {TAB_ITEMS.map(tab => (
                  <button
                    key={tab.key}
                    onClick={() => setActiveTab(tab.key)}
                    className={`relative flex-1 flex items-center justify-center gap-1.5 px-2 py-2 rounded-lg text-[11px] font-medium transition-all ${
                      activeTab === tab.key
                        ? 'bg-white dark:bg-white/[0.08] text-amber-600 dark:text-amber-400 shadow-sm border border-zinc-200/50 dark:border-white/[0.08]'
                        : 'text-zinc-400 dark:text-zinc-500 hover:text-zinc-600 dark:hover:text-zinc-300'
                    }`}
                  >
                    {tab.icon}
                    {tab.label}
                  </button>
                ))}
              </div>
            </div>

            {/* Content */}
            <div className="px-6 pb-6 overflow-y-auto flex-1" style={{ scrollbarWidth: 'none' }}>
              {isLoading ? (
                <div className="flex flex-col items-center justify-center py-16 gap-3">
                  <div className="w-8 h-8 border-2 border-zinc-200 dark:border-zinc-700 border-t-amber-500 rounded-full animate-spin" />
                  <p className="text-xs text-zinc-400 dark:text-zinc-500">Loading flares...</p>
                </div>
              ) : (
                <>
                  {/* ─── Tab: Launcher ─── */}
                  {activeTab === 'launcher' && (
                    <div className="space-y-5">
                      {/* Success animation */}
                      <AnimatePresence>
                        {sendSuccess && (
                          <MotionDiv
                            initial={{ opacity: 0, y: -10, scale: 0.95 }}
                            animate={{ opacity: 1, y: 0, scale: 1 }}
                            exit={{ opacity: 0, y: -10, scale: 0.95 }}
                            className="flex items-center gap-3 p-4 rounded-xl bg-emerald-50 dark:bg-emerald-500/10 border border-emerald-200 dark:border-emerald-500/20"
                          >
                            <div className="w-8 h-8 rounded-lg bg-emerald-500/20 flex items-center justify-center">
                              <CheckCircle size={16} className="text-emerald-600 dark:text-emerald-400" />
                            </div>
                            <div>
                              <p className="text-sm font-semibold text-emerald-700 dark:text-emerald-400">Flare launched!</p>
                              <p className="text-[10px] text-emerald-600/70 dark:text-emerald-400/50">Your classmates will see it soon</p>
                            </div>
                          </MotionDiv>
                        )}
                      </AnimatePresence>

                      {/* Remaining counts — styled as a subtle info bar */}
                      <div className="flex items-center justify-center gap-4">
                        <div className="flex items-center gap-1.5">
                          <div className="flex gap-0.5">
                            {Array.from({ length: flareCounts.dailyLimit }).map((_, i) => (
                              <div
                                key={i}
                                className={`w-1.5 h-4 rounded-full transition-colors ${
                                  i < flareCounts.dailyRemaining
                                    ? 'bg-amber-500'
                                    : 'bg-zinc-200 dark:bg-white/[0.06]'
                                }`}
                              />
                            ))}
                          </div>
                          <span className="text-[10px] font-medium text-zinc-400 dark:text-zinc-500">today</span>
                        </div>
                        <div className="w-px h-3 bg-zinc-200 dark:bg-white/[0.08]" />
                        <div className="flex items-center gap-1.5">
                          <div className="flex gap-0.5">
                            {Array.from({ length: flareCounts.weeklyLimit }).map((_, i) => (
                              <div
                                key={i}
                                className={`w-1 h-3 rounded-full transition-colors ${
                                  i < flareCounts.weeklyRemaining
                                    ? 'bg-amber-500/60'
                                    : 'bg-zinc-200 dark:bg-white/[0.06]'
                                }`}
                              />
                            ))}
                          </div>
                          <span className="text-[10px] font-medium text-zinc-400 dark:text-zinc-500">this week</span>
                        </div>
                      </div>

                      {/* Subject picker */}
                      <section>
                        <h3 className="text-xs font-semibold uppercase tracking-widest text-zinc-400 dark:text-zinc-500 mb-3">
                          Subject
                        </h3>
                        <div className="flex flex-wrap gap-2">
                          {subjects.map(subject => {
                            const colors = getSubjectColors(subject);
                            const isSelected = selectedSubject === subject;
                            return (
                              <button
                                key={subject}
                                onClick={() => setSelectedSubject(subject)}
                                className={`px-3 py-1.5 rounded-xl text-xs font-medium transition-all ${
                                  isSelected
                                    ? `ring-2 ${colors.ring} ${colors.bg} ${colors.text}`
                                    : 'bg-zinc-50 dark:bg-white/[0.04] text-zinc-500 dark:text-zinc-400 ring-1 ring-zinc-200 dark:ring-white/[0.06] hover:ring-zinc-300 dark:hover:ring-white/[0.15]'
                                }`}
                              >
                                {subject}
                              </button>
                            );
                          })}
                        </div>
                      </section>

                      {/* Question textarea */}
                      <section>
                        <h3 className="text-xs font-semibold uppercase tracking-widest text-zinc-400 dark:text-zinc-500 mb-3">
                          Your Question
                        </h3>
                        <div className="rounded-xl bg-zinc-50 dark:bg-white/[0.03] border border-zinc-200/50 dark:border-white/[0.06] overflow-hidden focus-within:border-amber-500/30 dark:focus-within:border-amber-500/30 transition-colors">
                          <textarea
                            ref={textareaRef}
                            value={questionText}
                            onChange={e => {
                              if (e.target.value.length <= 300) {
                                setQuestionText(e.target.value);
                                if (profanityError) setProfanityError(false);
                                if (sendError) setSendError(null);
                              }
                            }}
                            onBlur={handleQuestionBlur}
                            placeholder="What do you need help with?"
                            rows={3}
                            className="w-full bg-transparent px-4 py-3 text-sm text-zinc-900 dark:text-white placeholder-zinc-400 dark:placeholder-zinc-600 resize-none focus:outline-none"
                          />
                          <div className="flex items-center justify-between px-4 py-2 border-t border-zinc-200/50 dark:border-white/[0.04]">
                            {profanityError ? (
                              <span className="text-[10px] text-red-500 dark:text-red-400 flex items-center gap-1 font-medium">
                                <AlertCircle size={10} />
                                Please rephrase
                              </span>
                            ) : (
                              <span />
                            )}
                            <span className={`text-[10px] font-mono tabular-nums ${questionText.length >= 280 ? 'text-amber-500' : 'text-zinc-300 dark:text-zinc-600'}`}>
                              {questionText.length}/300
                            </span>
                          </div>
                        </div>
                      </section>

                      {/* Send error */}
                      <AnimatePresence>
                        {sendError && (
                          <MotionDiv
                            initial={{ opacity: 0, height: 0 }}
                            animate={{ opacity: 1, height: 'auto' }}
                            exit={{ opacity: 0, height: 0 }}
                            className="flex items-center gap-2 p-3 rounded-xl bg-red-50 dark:bg-red-500/10 border border-red-200 dark:border-red-500/20"
                          >
                            <AlertCircle size={14} className="text-red-500 dark:text-red-400 shrink-0" />
                            <span className="text-xs text-red-600 dark:text-red-400">{sendError}</span>
                          </MotionDiv>
                        )}
                      </AnimatePresence>

                      {/* Launch button */}
                      <MotionButton
                        whileHover={canSendFlare ? { scale: 1.02 } : {}}
                        whileTap={canSendFlare ? { scale: 0.98 } : {}}
                        disabled={!canSendFlare}
                        onClick={handleSendFlare}
                        className={`w-full py-3.5 rounded-xl text-sm font-semibold flex items-center justify-center gap-2.5 transition-all ${
                          canSendFlare
                            ? 'bg-gradient-to-r from-amber-500 to-orange-500 text-white shadow-lg shadow-amber-500/25 hover:shadow-amber-500/40'
                            : 'bg-zinc-100 dark:bg-white/[0.04] text-zinc-300 dark:text-zinc-600 cursor-not-allowed'
                        }`}
                      >
                        {isSending ? (
                          <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                        ) : (
                          <>
                            <Send size={14} />
                            Launch Flare
                          </>
                        )}
                      </MotionButton>

                      {/* Own active flares */}
                      {myActiveFlares.length > 0 && (
                        <section>
                          <h3 className="text-xs font-semibold uppercase tracking-widest text-zinc-400 dark:text-zinc-500 mb-3">
                            Your Active Flares
                          </h3>
                          <div className="space-y-2">
                            {myActiveFlares.map(flare => (
                              <div
                                key={flare.id}
                                className="flex items-center gap-3 p-3 rounded-xl bg-zinc-50 dark:bg-white/[0.03] border border-zinc-200/50 dark:border-white/[0.06]"
                              >
                                <SubjectPill subject={flare.subject} />
                                <p className="text-xs text-zinc-600 dark:text-zinc-300 flex-1 min-w-0 truncate">
                                  {flare.question}
                                </p>
                                <span className="shrink-0 text-[10px] font-medium text-zinc-400 dark:text-zinc-500 bg-zinc-100 dark:bg-white/[0.06] px-2 py-0.5 rounded-full tabular-nums">
                                  {flare.responseCount ?? 0} replies
                                </span>
                              </div>
                            ))}
                          </div>
                        </section>
                      )}
                    </div>
                  )}

                  {/* ─── Tab: Feed ─── */}
                  {activeTab === 'feed' && (
                    <div className="space-y-3">
                      {/* Refresh button */}
                      <div className="flex justify-end">
                        <button
                          onClick={reload}
                          className="flex items-center gap-1.5 text-[10px] font-medium text-zinc-400 dark:text-zinc-500 hover:text-zinc-600 dark:hover:text-zinc-300 transition-colors px-2.5 py-1.5 rounded-lg hover:bg-zinc-100 dark:hover:bg-white/[0.04]"
                        >
                          <RefreshCw size={11} />
                          Refresh
                        </button>
                      </div>

                      {activeFlares.length === 0 ? (
                        <div className="text-center py-16">
                          <div className="w-12 h-12 rounded-2xl bg-zinc-100 dark:bg-white/[0.04] border border-zinc-200/50 dark:border-white/[0.06] flex items-center justify-center mx-auto mb-4">
                            <Radio size={20} className="text-zinc-300 dark:text-zinc-600" />
                          </div>
                          <p className="text-sm font-medium text-zinc-400 dark:text-zinc-500">All quiet</p>
                          <p className="text-xs text-zinc-300 dark:text-zinc-600 mt-1">No active flares from classmates right now</p>
                        </div>
                      ) : (
                        activeFlares.map(flare => (
                          <div
                            key={flare.id}
                            className="p-4 rounded-xl bg-zinc-50 dark:bg-white/[0.03] border border-zinc-200/50 dark:border-white/[0.06] space-y-3"
                          >
                            <div className="flex items-start justify-between gap-3">
                              <div className="flex-1 min-w-0">
                                <div className="flex items-center gap-2 mb-2">
                                  <SubjectPill subject={flare.subject} />
                                  <span className="text-[10px] font-mono text-zinc-300 dark:text-zinc-600">
                                    {timeAgo(flare.createdAt instanceof Date ? flare.createdAt : new Date(flare.createdAt))}
                                  </span>
                                </div>
                                <p className="text-sm text-zinc-700 dark:text-zinc-200 leading-relaxed">{flare.question}</p>
                              </div>
                            </div>

                            {expandedFlareId === flare.id ? (
                              <div className="space-y-2.5 pt-2 border-t border-zinc-200/50 dark:border-white/[0.06]">
                                <div className="rounded-xl bg-white dark:bg-white/[0.03] border border-zinc-200/50 dark:border-white/[0.06] overflow-hidden focus-within:border-amber-500/30 dark:focus-within:border-amber-500/30 transition-colors">
                                  <textarea
                                    ref={responseTextareaRef}
                                    value={responseText}
                                    onChange={e => {
                                      if (e.target.value.length <= 500) {
                                        setResponseText(e.target.value);
                                        if (responseProfanityError) setResponseProfanityError(false);
                                        if (respondError) setRespondError(null);
                                      }
                                    }}
                                    placeholder="Share your knowledge..."
                                    rows={3}
                                    className="w-full bg-transparent px-3 py-2.5 text-sm text-zinc-900 dark:text-white placeholder-zinc-400 dark:placeholder-zinc-600 resize-none focus:outline-none"
                                  />
                                </div>
                                <div className="flex items-center justify-between">
                                  {responseProfanityError ? (
                                    <span className="text-[10px] text-red-500 dark:text-red-400 flex items-center gap-1 font-medium">
                                      <AlertCircle size={10} />
                                      Please rephrase
                                    </span>
                                  ) : respondError ? (
                                    <span className="text-[10px] text-red-500 dark:text-red-400 flex items-center gap-1 font-medium">
                                      <AlertCircle size={10} />
                                      {respondError}
                                    </span>
                                  ) : (
                                    <span className={`text-[10px] font-mono tabular-nums ${responseText.length >= 480 ? 'text-amber-500' : 'text-zinc-300 dark:text-zinc-600'}`}>
                                      {responseText.length}/500
                                    </span>
                                  )}
                                  <div className="flex gap-2">
                                    <button
                                      onClick={() => {
                                        setExpandedFlareId(null);
                                        setResponseText('');
                                        setResponseProfanityError(false);
                                      }}
                                      className="px-3 py-1.5 rounded-lg text-[11px] font-medium text-zinc-400 dark:text-zinc-500 hover:text-zinc-600 dark:hover:text-zinc-300 hover:bg-zinc-100 dark:hover:bg-white/[0.04] transition-colors"
                                    >
                                      Cancel
                                    </button>
                                    <MotionButton
                                      whileTap={{ scale: 0.95 }}
                                      disabled={!responseText.trim() || isResponding}
                                      onClick={() => handleRespondToFlare(flare.id)}
                                      className={`px-4 py-1.5 rounded-lg text-[11px] font-semibold flex items-center gap-1.5 transition-all ${
                                        responseText.trim() && !isResponding
                                          ? 'bg-amber-500 text-white shadow-sm hover:bg-amber-600'
                                          : 'bg-zinc-100 dark:bg-white/[0.04] text-zinc-300 dark:text-zinc-600 cursor-not-allowed'
                                      }`}
                                    >
                                      {isResponding ? (
                                        <div className="w-3 h-3 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                                      ) : (
                                        <>
                                          <Send size={10} />
                                          Send
                                        </>
                                      )}
                                    </MotionButton>
                                  </div>
                                </div>
                              </div>
                            ) : (
                              <button
                                onClick={() => {
                                  setExpandedFlareId(flare.id);
                                  setResponseText('');
                                  setResponseProfanityError(false);
                                }}
                                className="flex items-center gap-1.5 text-[11px] font-semibold text-amber-600 dark:text-amber-400 hover:text-amber-500 dark:hover:text-amber-300 transition-colors"
                              >
                                <MessageCircle size={12} />
                                Respond
                              </button>
                            )}
                          </div>
                        ))
                      )}
                    </div>
                  )}

                  {/* ─── Tab: My Flares ─── */}
                  {activeTab === 'my-flares' && (
                    <div className="space-y-3">
                      {myFlares.length === 0 ? (
                        <div className="text-center py-16">
                          <div className="w-12 h-12 rounded-2xl bg-zinc-100 dark:bg-white/[0.04] border border-zinc-200/50 dark:border-white/[0.06] flex items-center justify-center mx-auto mb-4">
                            <Flame size={20} className="text-zinc-300 dark:text-zinc-600" />
                          </div>
                          <p className="text-sm font-medium text-zinc-400 dark:text-zinc-500">No flares yet</p>
                          <p className="text-xs text-zinc-300 dark:text-zinc-600 mt-1">Launch your first flare to get help</p>
                        </div>
                      ) : (
                        myFlares.map(flare => {
                          const isActive = flare.status === 'active';
                          const responses = loadedResponses[flare.id];
                          const isLoadingResp = loadingResponses[flare.id];

                          return (
                            <div
                              key={flare.id}
                              className="p-4 rounded-xl bg-zinc-50 dark:bg-white/[0.03] border border-zinc-200/50 dark:border-white/[0.06] space-y-3"
                            >
                              <div className="flex items-start justify-between gap-3">
                                <div className="flex-1 min-w-0">
                                  <div className="flex items-center gap-2 mb-2">
                                    <SubjectPill subject={flare.subject} />
                                    <span className={`text-[10px] px-2 py-0.5 rounded-full font-semibold uppercase tracking-wider ${
                                      isActive
                                        ? 'bg-amber-100 dark:bg-amber-500/15 text-amber-600 dark:text-amber-400'
                                        : 'bg-emerald-100 dark:bg-emerald-500/15 text-emerald-600 dark:text-emerald-400'
                                    }`}>
                                      {isActive ? 'Active' : 'Resolved'}
                                    </span>
                                  </div>
                                  <p className="text-sm text-zinc-700 dark:text-zinc-200 leading-relaxed">{flare.question}</p>
                                </div>
                              </div>

                              {/* Load / show responses */}
                              {!responses && !isLoadingResp && (
                                <button
                                  onClick={() => handleLoadResponses(flare.id)}
                                  className="flex items-center gap-1.5 text-[11px] font-medium text-zinc-400 dark:text-zinc-500 hover:text-zinc-600 dark:hover:text-zinc-300 transition-colors"
                                >
                                  <MessageCircle size={11} />
                                  View responses ({flare.responseCount ?? 0})
                                </button>
                              )}

                              {isLoadingResp && (
                                <div className="flex items-center gap-2 py-2">
                                  <div className="w-3 h-3 border-2 border-zinc-200 dark:border-zinc-700 border-t-zinc-400 dark:border-t-zinc-400 rounded-full animate-spin" />
                                  <span className="text-[10px] text-zinc-400 dark:text-zinc-500">Loading...</span>
                                </div>
                              )}

                              {responses && responses.length > 0 && (
                                <div className="space-y-2 ml-3 pl-3 border-l-2 border-zinc-200 dark:border-white/[0.06]">
                                  {responses.map(resp => (
                                    <div key={resp.id} className="p-3 rounded-lg bg-white dark:bg-white/[0.02] border border-zinc-100 dark:border-white/[0.04]">
                                      <p className="text-xs text-zinc-600 dark:text-zinc-300 leading-relaxed mb-2">{resp.text}</p>
                                      <div className="flex items-center justify-between">
                                        <span className="text-[10px] font-mono text-zinc-300 dark:text-zinc-600">
                                          {timeAgo(resp.createdAt instanceof Date ? resp.createdAt : new Date(resp.createdAt))}
                                        </span>
                                        <button
                                          onClick={() => handleMarkHelpful(flare.id, resp.id)}
                                          disabled={resp.helpful}
                                          className={`flex items-center gap-1 text-[10px] px-2 py-1 rounded-lg font-medium transition-all ${
                                            resp.helpful
                                              ? 'text-amber-600 dark:text-amber-400 bg-amber-50 dark:bg-amber-500/10 border border-amber-200/50 dark:border-amber-500/20'
                                              : 'text-zinc-400 dark:text-zinc-500 hover:text-amber-600 dark:hover:text-amber-400 hover:bg-amber-50 dark:hover:bg-amber-500/10'
                                          }`}
                                        >
                                          <ThumbsUp size={10} className={resp.helpful ? 'fill-amber-500 dark:fill-amber-400' : ''} />
                                          {resp.helpful ? 'Helpful' : 'Mark helpful'}
                                        </button>
                                      </div>
                                    </div>
                                  ))}
                                </div>
                              )}

                              {responses && responses.length === 0 && (
                                <p className="text-[11px] text-zinc-300 dark:text-zinc-600 italic pl-3">No responses yet</p>
                              )}

                              {/* Mark Resolved button */}
                              {isActive && (
                                <button
                                  onClick={() => handleResolveFlare(flare.id)}
                                  className="flex items-center gap-1.5 text-[11px] font-semibold text-emerald-600 dark:text-emerald-400 hover:text-emerald-500 dark:hover:text-emerald-300 transition-colors"
                                >
                                  <CheckCircle size={12} />
                                  Mark Resolved
                                </button>
                              )}
                            </div>
                          );
                        })
                      )}
                    </div>
                  )}

                  {/* ─── Tab: Stats ─── */}
                  {activeTab === 'stats' && (
                    <div className="space-y-6 py-2">
                      {/* Hero stat */}
                      <div className="text-center">
                        <div className="inline-flex items-center justify-center w-20 h-20 rounded-2xl bg-gradient-to-br from-amber-500/10 to-orange-500/10 border border-amber-500/10 mb-3">
                          <p className="text-4xl font-bold text-zinc-900 dark:text-white tabular-nums">{rescueCount}</p>
                        </div>
                        <p className="text-xs font-semibold uppercase tracking-widest text-zinc-400 dark:text-zinc-500">classmates helped</p>
                      </div>

                      {/* Lighthouse visualization */}
                      <div className="p-5 rounded-xl bg-zinc-50 dark:bg-white/[0.03] border border-zinc-200/50 dark:border-white/[0.06]">
                        <div className="text-center">
                          <LighthouseVis level={lighthouseInfo.level} />
                          <p className="text-sm font-semibold text-amber-600 dark:text-amber-400 mt-2">{lighthouseInfo.label}</p>
                        </div>

                        {/* Progress to next level */}
                        {lighthouseInfo.nextLabel && (
                          <div className="space-y-2 mt-5">
                            <div className="flex justify-between text-[10px] font-medium text-zinc-400 dark:text-zinc-500 uppercase tracking-wider">
                              <span>{lighthouseInfo.label}</span>
                              <span>{lighthouseInfo.nextLabel}</span>
                            </div>
                            <div className="h-1.5 bg-zinc-200 dark:bg-white/[0.06] rounded-full overflow-hidden">
                              <MotionDiv
                                initial={{ width: 0 }}
                                animate={{
                                  width: `${Math.min(100, ((rescueCount - LIGHTHOUSE_LEVELS[lighthouseInfo.level].threshold) / (LIGHTHOUSE_LEVELS[lighthouseInfo.level + 1].threshold - LIGHTHOUSE_LEVELS[lighthouseInfo.level].threshold)) * 100)}%`,
                                }}
                                transition={{ duration: 0.8, ease: 'easeOut' }}
                                className="h-full bg-gradient-to-r from-amber-500 to-orange-500 rounded-full"
                              />
                            </div>
                            <p className="text-[10px] text-zinc-400 dark:text-zinc-500 text-center font-medium">
                              {lighthouseInfo.remaining} more rescue{lighthouseInfo.remaining !== 1 ? 's' : ''} to reach <span className="text-amber-600 dark:text-amber-400">{lighthouseInfo.nextLabel}</span>
                            </p>
                          </div>
                        )}

                        {lighthouseInfo.level >= 3 && (
                          <p className="text-xs text-amber-600 dark:text-amber-400 text-center font-semibold mt-4">
                            Maximum level reached!
                          </p>
                        )}
                      </div>

                      {/* Motivational text */}
                      <div className="text-center">
                        <p className="text-[11px] text-zinc-400 dark:text-zinc-500 italic leading-relaxed">
                          Every response strengthens your own understanding
                        </p>
                      </div>
                    </div>
                  )}
                </>
              )}
            </div>
          </MotionDiv>
        </MotionDiv>
      )}
    </AnimatePresence>,
    document.body,
  );
};

export default FlareSystem;
