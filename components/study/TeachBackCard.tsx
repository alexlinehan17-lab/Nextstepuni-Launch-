/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { BookOpen, Send, ThumbsUp, X } from 'lucide-react';

const MotionDiv = motion.div as any;

// ── Read Card ──────────────────────────────────────────────

interface TeachBackReadProps {
  subject: string;
  explanation: string;
  onHelpful: () => void;
  onSkip: () => void;
}

export const TeachBackReadCard: React.FC<TeachBackReadProps> = ({
  subject, explanation, onHelpful, onSkip,
}) => (
  <MotionDiv
    initial={{ opacity: 0, y: 20 }}
    animate={{ opacity: 1, y: 0 }}
    exit={{ opacity: 0, y: -10 }}
    transition={{ duration: 0.4, ease: [0.16, 1, 0.3, 1] }}
    className="absolute bottom-12 left-4 right-4 max-w-md mx-auto"
  >
    <div className="bg-zinc-900 border border-indigo-500/30 rounded-xl p-4 shadow-2xl">
      <div className="flex items-center gap-2 mb-2">
        <BookOpen size={14} className="text-indigo-400" />
        <span className="text-xs font-bold uppercase tracking-widest text-indigo-400">
          A classmate shared
        </span>
      </div>
      <p className="text-[11px] text-zinc-500 mb-2">{subject}</p>
      <p className="text-sm text-zinc-200 leading-relaxed italic">
        &ldquo;{explanation}&rdquo;
      </p>
      <div className="flex items-center gap-3 mt-3">
        <button
          onClick={onHelpful}
          className="inline-flex items-center gap-1.5 text-xs font-semibold text-indigo-400 hover:text-indigo-300 transition-colors"
        >
          <ThumbsUp size={12} />
          Helpful
        </button>
        <button
          onClick={onSkip}
          className="text-xs text-zinc-500 hover:text-zinc-400 transition-colors"
        >
          Skip
        </button>
      </div>
    </div>
  </MotionDiv>
);

// ── Write Card ─────────────────────────────────────────────

interface TeachBackWriteProps {
  subject: string;
  onSubmit: (text: string) => void;
  onSkip: () => void;
  isSubmitting: boolean;
}

export const TeachBackWriteCard: React.FC<TeachBackWriteProps> = ({
  subject, onSubmit, onSkip, isSubmitting,
}) => {
  const [text, setText] = useState('');

  const handleSubmit = () => {
    if (text.trim().length < 10) return;
    onSubmit(text);
  };

  return (
    <MotionDiv
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -10 }}
      transition={{ duration: 0.4, ease: [0.16, 1, 0.3, 1] }}
      className="absolute bottom-12 left-4 right-4 max-w-md mx-auto"
    >
      <div className="bg-zinc-900 border border-emerald-500/30 rounded-xl p-4 shadow-2xl">
        <div className="flex items-center justify-between mb-2">
          <div className="flex items-center gap-2">
            <Send size={14} className="text-emerald-400" />
            <span className="text-xs font-bold uppercase tracking-widest text-emerald-400">
              Teach a classmate
            </span>
          </div>
          <button
            onClick={onSkip}
            className="p-1 rounded-lg hover:bg-zinc-800 transition-colors"
          >
            <X size={14} className="text-zinc-500" />
          </button>
        </div>
        <p className="text-xs text-zinc-400 leading-relaxed mb-3">
          Explain a key concept from your {subject} session. Your anonymous explanation will help a peer study.
        </p>
        <textarea
          value={text}
          onChange={e => setText(e.target.value)}
          placeholder="E.g. The trick to understanding osmosis is..."
          rows={3}
          maxLength={500}
          className="w-full bg-zinc-800 border border-zinc-700 rounded-lg px-3 py-2 text-sm text-zinc-200 placeholder-zinc-600 resize-none focus:outline-none focus:border-emerald-500/50"
        />
        <div className="flex items-center justify-between mt-2">
          <span className="text-[10px] text-zinc-600">{text.length}/500</span>
          <button
            onClick={handleSubmit}
            disabled={text.trim().length < 10 || isSubmitting}
            className={`inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold transition-colors ${
              text.trim().length >= 10 && !isSubmitting
                ? 'bg-emerald-500 text-white hover:bg-emerald-600'
                : 'bg-zinc-800 text-zinc-600 cursor-not-allowed'
            }`}
          >
            <Send size={10} />
            {isSubmitting ? 'Sending...' : 'Send'}
          </button>
        </div>
      </div>
    </MotionDiv>
  );
};
