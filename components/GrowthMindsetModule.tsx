import { moduleFill,moduleText } from './learning/brandTokens';

/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import { AnimatePresence,motion } from 'framer-motion';
import {
Activity,
BrainCircuit,
Cpu,
MessageSquareQuote,
RotateCcw,Zap
} from 'lucide-react';
import React,{ useEffect,useState } from 'react';
import { GROWTH_MINDSET_REFERENCE_LIST } from '../data/references/growthMindset';
import { COLORS } from '../design/tokens';
import { useEssentialsMode } from '../hooks/useEssentialsMode';
import { useModuleResponses } from '../hooks/useModuleResponses';
import { amberTheme } from '../moduleThemes';
import { type ModuleProgress } from '../types';
import { ModuleLayout } from './ModuleLayout';
import { Cite } from './ModuleReferences';
import { Highlight,MicroCommitment,PersonalStory,ReadingSection } from './ModuleShared';
import { MotionDiv } from './Motion';

const theme = amberTheme;

// --- INTERACTIVE COMPONENTS ---

const MindsetDiagnostic = ({ savedAnswers, onSaveAnswers }: { savedAnswers?: ('fixed' | 'growth' | null)[]; onSaveAnswers?: (answers: ('fixed' | 'growth' | null)[]) => void }) => {
  const [answers, setAnswers] = useState<( 'fixed' | 'growth' | null)[]>(savedAnswers || [null, null, null]);
  const score = answers.filter(a => a === 'growth').length;

  useEffect(() => {
    if (savedAnswers) setAnswers(savedAnswers);
  }, [savedAnswers]);

  const handleAnswer = (index: number, type: 'fixed' | 'growth') => {
    const newAnswers = [...answers];
    newAnswers[index] = type;
    setAnswers(newAnswers);
    onSaveAnswers?.(newAnswers);
  };

  const isComplete = answers.every(a => a !== null);

  return <div className="wr-skin" data-wide="MindsetDiagnostic"><div className="my-10 rounded-2xl p-6 md:p-8" style={{ backgroundColor: "var(--module-surface)", borderRadius: 18 }}>
      <h4 className="font-serif text-2xl font-semibold text-[var(--module-ink)] dark:text-[var(--module-ink)] text-center">Mindset Diagnostic</h4>
      <p className="text-center text-sm text-[var(--module-muted)] dark:text-[var(--module-muted)] mb-8">Which thought sounds more like you in a tough situation?</p>
      <div className="space-y-6">
        {/* Question 1 */}
        <div>
          <p className="text-sm font-bold text-center text-[var(--module-ink)] dark:text-[var(--module-muted)] mb-3">When I fail at something...</p>
          <div className="grid grid-cols-2 gap-3">
            <button onClick={() => handleAnswer(0, 'fixed')} className="p-4 rounded-xl text-xs text-center font-medium transition-all" style={answers[0] === 'fixed' ? { backgroundColor: "var(--module-surface)", border: "2.5px solid var(--module-line)", borderRadius: 14, boxShadow: 'none', color: "var(--module-danger-text)" } : { backgroundColor: "var(--module-surface)", border: "2.5px solid var(--module-line)", borderRadius: 14, boxShadow: 'none' }} data-wide-button="true" data-selected={!!(answers[0] === 'fixed')} data-tone="coral" aria-pressed={!!(answers[0] === 'fixed')}>A) I feel like I'm a failure.</button>
            <button onClick={() => handleAnswer(0, 'growth')} className="p-4 rounded-xl text-xs text-center font-medium transition-all" style={answers[0] === 'growth' ? { backgroundColor: "var(--module-success-soft)", border: "2.5px solid var(--module-line)", borderRadius: 14, boxShadow: 'none', color: "var(--module-success-text)" } : { backgroundColor: "var(--module-surface)", border: "2.5px solid var(--module-line)", borderRadius: 14, boxShadow: 'none' }} data-wide-button="true" data-selected={!!(answers[0] === 'growth')} data-tone="mint" aria-pressed={!!(answers[0] === 'growth')}>B) I feel like I need to try a new strategy.</button>
          </div>
        </div>
        {/* Question 2 */}
         <div>
          <p className="text-sm font-bold text-center text-[var(--module-ink)] dark:text-[var(--module-muted)] mb-3">If a subject is hard for me...</p>
          <div className="grid grid-cols-2 gap-3">
            <button onClick={() => handleAnswer(1, 'fixed')} className="p-4 rounded-xl text-xs text-center font-medium transition-all" style={answers[1] === 'fixed' ? { backgroundColor: "var(--module-surface)", border: "2.5px solid var(--module-line)", borderRadius: 14, boxShadow: 'none', color: "var(--module-danger-text)" } : { backgroundColor: "var(--module-surface)", border: "2.5px solid var(--module-line)", borderRadius: 14, boxShadow: 'none' }} data-wide-button="true" data-selected={!!(answers[1] === 'fixed')} data-tone="coral" aria-pressed={!!(answers[1] === 'fixed')}>A) It means I'm probably not smart enough for it.</button>
            <button onClick={() => handleAnswer(1, 'growth')} className="p-4 rounded-xl text-xs text-center font-medium transition-all" style={answers[1] === 'growth' ? { backgroundColor: "var(--module-success-soft)", border: "2.5px solid var(--module-line)", borderRadius: 14, boxShadow: 'none', color: "var(--module-success-text)" } : { backgroundColor: "var(--module-surface)", border: "2.5px solid var(--module-line)", borderRadius: 14, boxShadow: 'none' }} data-wide-button="true" data-selected={!!(answers[1] === 'growth')} data-tone="mint" aria-pressed={!!(answers[1] === 'growth')}>B) It means I have a great opportunity to learn.</button>
          </div>
        </div>
        {/* Question 3 */}
         <div>
          <p className="text-sm font-bold text-center text-[var(--module-ink)] dark:text-[var(--module-muted)] mb-3">I believe my intelligence is something...</p>
          <div className="grid grid-cols-2 gap-3">
            <button onClick={() => handleAnswer(2, 'fixed')} className="p-4 rounded-xl text-xs text-center font-medium transition-all" style={answers[2] === 'fixed' ? { backgroundColor: "var(--module-surface)", border: "2.5px solid var(--module-line)", borderRadius: 14, boxShadow: 'none', color: "var(--module-danger-text)" } : { backgroundColor: "var(--module-surface)", border: "2.5px solid var(--module-line)", borderRadius: 14, boxShadow: 'none' }} data-wide-button="true" data-selected={!!(answers[2] === 'fixed')} data-tone="coral" aria-pressed={!!(answers[2] === 'fixed')}>A) That I can't change very much.</button>
            <button onClick={() => handleAnswer(2, 'growth')} className="p-4 rounded-xl text-xs text-center font-medium transition-all" style={answers[2] === 'growth' ? { backgroundColor: "var(--module-success-soft)", border: "2.5px solid var(--module-line)", borderRadius: 14, boxShadow: 'none', color: "var(--module-success-text)" } : { backgroundColor: "var(--module-surface)", border: "2.5px solid var(--module-line)", borderRadius: 14, boxShadow: 'none' }} data-wide-button="true" data-selected={!!(answers[2] === 'growth')} data-tone="mint" aria-pressed={!!(answers[2] === 'growth')}>B) That I can grow with effort.</button>
          </div>
        </div>
      </div>
      <AnimatePresence>
      {isComplete && (
        <motion.div initial={{opacity:0, y:10}} animate={{opacity:1, y:0}} className="mt-8 p-6 rounded-xl" style={score === 3 ? { backgroundColor: "var(--module-success-soft)", border: "2.5px solid var(--module-line)", boxShadow: 'none' } : score === 2 ? { backgroundColor: "var(--module-surface)", border: "2.5px solid var(--module-line)", boxShadow: 'none' } : { backgroundColor: "var(--module-surface)", border: "2.5px solid var(--module-line)", boxShadow: 'none' }}>
          <p className="text-center font-bold">
            {score === 3 && <span style={{ color: "var(--module-success-text)" }}>Result: You're operating with a strong Growth Mindset OS!</span>}
            {score === 2 && <span style={{ color: "var(--module-danger-text)" }}>Result: You're leaning towards Growth, with some Fixed-Mindset code still running.</span>}
            {score < 2 && <span style={{ color: "var(--module-danger-text)" }}>Result: Your system is currently running a Fixed-Mindset OS. Time for an upgrade!</span>}
          </p>
        </motion.div>
      )}
      </AnimatePresence>
    </div></div>;
};

const NeuroplasticityVisualizer = () => {
  const [connections, setConnections] = useState(0);
  const milestone = connections === 1 ? 'First connection forming.' : connections === 3 ? 'Pathway strengthening — repetition is working.' : connections === 5 ? 'Strong neural pathway established.' : null;

  return (
    <div className="my-10 rounded-2xl p-6 md:p-8" style={{ backgroundColor: "var(--module-surface)", borderRadius: 18 }}>
      <div className="text-center mb-8">
        <span className="inline-block px-3 py-1 rounded-full text-[11px] font-bold tracking-wider uppercase mb-3" style={{ backgroundColor: moduleFill(COLORS.accentTint), color: moduleText(COLORS.accentDarkText), border: '1px solid rgba(242,107,31,0.2)', letterSpacing: '0.06em' }}>Neuroscience Simulation</span>
        <h4 className="font-serif font-bold" style={{ fontSize: 24, color: "var(--module-ink)" }}>The Brain Rewiring Simulator</h4>
        <p className="text-sm mt-1" style={{ color: "var(--module-muted)" }}>Every time you practice, you strengthen the physical connections in your brain.</p>
      </div>

      {/* SVG card */}
      <div className="bg-[var(--module-surface)] dark:bg-[var(--module-surface)]" style={{ border: "2px solid var(--module-line)", borderRadius: 16, padding: 28, maxWidth: 380, margin: '0 auto' }}>
        <p className="text-center mb-3" style={{ fontSize: 10, fontWeight: 700, letterSpacing: '0.12em', color: "var(--module-muted)", textTransform: 'uppercase' as const }}>Neural Pathway</p>

        <svg width="250" height="100" viewBox="0 0 250 100" style={{ display: 'block', margin: '0 auto' }}>
          {/* Base placeholder connection */}
          <path d="M 70 50 Q 125 50 180 50" fill="none" stroke="var(--module-muted)" strokeWidth="1" opacity="0.5" />

          {/* Connection arcs */}
          <AnimatePresence>
            {connections > 0 && Array.from({length: connections}).map((_, i) => {
              const age = connections - 1 - i;
              const opacity = Math.max(0.12, 0.9 - age * 0.12);
              const sw = Math.max(1.0, 2.5 - age * 0.3);
              return (
                <motion.path
                  key={i}
                  d={`M 70 50 Q 125 ${50 + (i - (connections-1)/2) * 15} 180 50`}
                  fill="none"
                  stroke={COLORS.accent}
                  initial={{ pathLength: 0, opacity: 0, strokeWidth: sw }}
                  animate={{ pathLength: 1, opacity, strokeWidth: sw }}
                  transition={{ duration: 0.5 }}
                />
              );
            })}
          </AnimatePresence>

          {/* Neuron A */}
          <circle cx="50" cy="50" r="20" fill={COLORS.accent} stroke={COLORS.accentDark} strokeWidth="2" />
          <circle cx="50" cy="50" r="8" fill="rgba(255,255,255,0.25)" />
          {/* Neuron B */}
          <circle cx="200" cy="50" r="20" fill={COLORS.accent} stroke={COLORS.accentDark} strokeWidth="2" />
          <circle cx="200" cy="50" r="8" fill="rgba(255,255,255,0.25)" />

          {/* Node labels */}
          <text x="50" y="82" textAnchor="middle" fontSize="11" fill="var(--module-muted)" fontFamily="DM Sans, sans-serif">Neuron A</text>
          <text x="200" y="82" textAnchor="middle" fontSize="11" fill="var(--module-muted)" fontFamily="DM Sans, sans-serif">Neuron B</text>
        </svg>

        {/* Connection count */}
        <div className="text-center mt-3 pt-3" style={{ borderTop: "1px solid var(--module-line)" }}>
          <p style={{ fontSize: 12, color: "var(--module-muted)" }}>{connections} connection{connections !== 1 ? 's' : ''} formed</p>
        </div>
      </div>

      {/* Milestone callout */}
      {milestone && (
        <motion.div
          key={milestone}
          initial={{ opacity: 0, y: 6 }}
          animate={{ opacity: 1, y: 0 }}
          className="mt-4 max-w-sm mx-auto"
          style={{ borderLeft: `3px solid ${COLORS.accent}`, backgroundColor: moduleFill(COLORS.accentTint), borderRadius: '0 10px 10px 0', padding: '12px 16px' }}
        >
          <p className="text-sm italic" style={{ color: moduleText(COLORS.accentDarkText) }}>{milestone}</p>
        </motion.div>
      )}

      {/* Buttons */}
      <div className="flex items-center justify-center gap-5 mt-6">
        <motion.button
          onClick={() => setConnections(c => Math.min(c + 1, 5))}
          whileTap={{ y: 3 }}
          className="text-[var(--module-ink)] font-semibold"
          style={{ backgroundColor: moduleFill(COLORS.accent), borderRadius: 100, padding: '14px 32px', fontSize: 15, borderBottom: `3px solid ${COLORS.accentDark}`, boxShadow: 'none' }} data-wide-button="true"
        >
          Practice a Skill
        </motion.button>
        <button
          onClick={() => setConnections(0)}
          className="font-medium"
          style={{ fontSize: 13, color: "var(--module-muted)", background: 'none', border: 'none' }}
          onMouseEnter={(e: React.MouseEvent<HTMLButtonElement>) => { e.currentTarget.style.color = "var(--module-ink)"; }}
          onMouseLeave={(e: React.MouseEvent<HTMLButtonElement>) => { e.currentTarget.style.color = "var(--module-muted)"; }} data-wide-button="true"
        >
          Reset
        </button>
      </div>
    </div>
  );
}

const ReframeChallenge = ({ savedText, onSave }: { savedText?: string; onSave?: (text: string) => void }) => {
    const [reframe, setReframe] = useState(savedText || '');
    const containsYet = reframe.toLowerCase().includes('yet');

    useEffect(() => {
      if (savedText !== undefined && savedText !== reframe) setReframe(savedText);
    }, [savedText]);

    return(
        <div className="my-10 rounded-2xl p-6 md:p-8" style={{ backgroundColor: "var(--module-surface)", borderRadius: 18 }}>
            <div className="text-center mb-8">
                <span className="inline-block px-3 py-1 rounded-full text-[11px] font-bold tracking-wider uppercase mb-3" style={{ backgroundColor: moduleFill(COLORS.accentTint), color: moduleText(COLORS.accentDarkText), border: '1px solid rgba(242,107,31,0.2)', letterSpacing: '0.06em' }}>Growth Mindset Activity</span>
                <h4 className="font-serif font-bold" style={{ fontSize: 24, color: "var(--module-ink)" }}>The "Yet" Reframe Challenge</h4>
                <p className="text-sm mt-1" style={{ color: "var(--module-muted)" }}>Upgrade this fixed thought into a growth mindset statement using the power of "yet".</p>
            </div>

            {/* Fixed thought card */}
            <div className="bg-[var(--module-surface)] dark:bg-[var(--module-surface)] max-w-lg mx-auto" style={{ border: "2px solid var(--module-line)", borderRadius: 14, padding: '20px 24px' }}>
                <span className="inline-block text-[10px] font-bold uppercase tracking-wider mb-2" style={{ backgroundColor: "var(--module-surface)", color: "var(--module-danger-text)", borderRadius: 20, padding: '3px 10px' }}>Fixed Mindset Thought</span>
                <p className="font-serif italic" style={{ fontSize: 17, color: "var(--module-ink)" }}>I'm just not a maths person.</p>
            </div>

            {/* Transformation connector */}
            <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', margin: '16px 0' }}>
                <div style={{ width: 2, height: 20, background: "var(--module-surface)" }} />
                <div style={{ background: moduleFill(COLORS.accentTint), border: '1.5px solid rgba(242,107,31,0.3)', borderRadius: 20, padding: '6px 14px' }}>
                    <span style={{ fontSize: 12, fontWeight: 700, color: moduleText(COLORS.accentDarkText), letterSpacing: '0.05em' }}>ADD "YET"</span>
                </div>
                <div style={{ width: 2, height: 20, background: "var(--module-surface)" }} />
                <svg width="16" height="10" viewBox="0 0 16 10" fill="none">
                    <path d="M1 1L8 8L15 1" stroke={COLORS.accent} strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round"/>
                </svg>
            </div>

            {/* Rewrite area */}
            <div className="max-w-lg mx-auto" style={{ backgroundColor: moduleFill(COLORS.accentTint), border: `2px solid ${COLORS.accent}`, borderRadius: 14, padding: '18px 20px' }}>
                <span className="inline-block text-[10px] font-bold uppercase tracking-wider mb-3" style={{ backgroundColor: moduleFill(COLORS.accentTint), color: moduleText(COLORS.accentDarkText), borderRadius: 20, padding: '3px 10px' }}>Your Reframe</span>
                <textarea
                    value={reframe}
                    onChange={(e) => setReframe(e.target.value)}
                    onBlur={() => onSave?.(reframe)}
                    placeholder="Rewrite this using the word 'yet'..."
                    className="w-full outline-none font-serif"
                    style={{ backgroundColor: "var(--module-surface)", border: "1.5px solid var(--module-line)", borderRadius: 10, padding: '14px 16px', fontSize: 15, color: "var(--module-ink)", lineHeight: 1.6, minHeight: 100, resize: 'none' as const }}
                    onFocus={(e) => { e.currentTarget.style.borderColor = COLORS.accent; }}
                    onBlurCapture={(e) => { e.currentTarget.style.borderColor = "var(--module-muted)"; }}
                />

                <AnimatePresence>
                    {containsYet && (
                        <motion.div initial={{ opacity: 0, y: 6 }} animate={{ opacity: 1, y: 0 }} style={{ marginTop: 12, backgroundColor: moduleFill(COLORS.successTint), border: `2px solid ${COLORS.success}`, borderRadius: 14, padding: '16px 20px', textAlign: 'center' }}>
                            <p className="font-serif font-semibold" style={{ fontSize: 16, color: moduleText(COLORS.successDarkText) }}>Reframe complete.</p>
                            <p style={{ fontSize: 13, color: moduleText(COLORS.success), marginTop: 4 }}>You've opened up the possibility of future growth.</p>
                        </motion.div>
                    )}
                </AnimatePresence>
            </div>
        </div>
    );
};

const feedbackPairs = [
  {
    verdict: "This essay is poorly written.",
    data: "Your argument structure needs clearer topic sentences and supporting evidence in each paragraph.",
    shift: "Shift: vague verdict \u2192 specific, actionable data",
  },
  {
    verdict: "You're just not a maths person.",
    data: "Your current approach to maths isn't working yet. Let's identify which specific steps are causing confusion.",
    shift: "Shift: identity label \u2192 strategy problem",
  },
  {
    verdict: "This is careless work.",
    data: "There are 4 calculation errors here. A final check-through step would catch these.",
    shift: "Shift: character judgment \u2192 countable, fixable issue",
  },
  {
    verdict: "You should know this by now.",
    data: "This concept hasn't stuck yet. Try explaining it to someone else to find where your understanding breaks down.",
    shift: "Shift: time-based shame \u2192 retrieval practice suggestion",
  },
  {
    verdict: "Disappointing result.",
    data: "You scored 52%. The areas to focus on are Q3 and Q5 \u2014 those are the highest-value gaps to close.",
    shift: "Shift: emotional verdict \u2192 strategic data",
  },
  {
    verdict: "You need to try harder.",
    data: "Your effort needs to be more targeted. Spend 20 minutes on active recall instead of 40 minutes re-reading.",
    shift: "Shift: vague effort demand \u2192 specific method change",
  },
];

const writeYourOwnTranslations = [
  "That feedback is pointing to a specific skill gap I can work on \u2014 it\u2019s data, not a label.",
  "This tells me my current strategy isn\u2019t working yet. Time to try a different approach.",
  "The feedback is about my method, not my ability. I can adjust and improve.",
];

const FeedbackTranslator = () => {
  const [flipped, setFlipped] = useState<boolean[]>(Array(6).fill(false));
  const [customFeedback, setCustomFeedback] = useState('');
  const [selectedTranslation, setSelectedTranslation] = useState<number | null>(null);

  const translatedCount = flipped.filter(Boolean).length;
  const allTranslated = translatedCount === 6;

  const handleFlip = (index: number) => {
    if (flipped[index]) return;
    const next = [...flipped];
    next[index] = true;
    setFlipped(next);
  };

  return (
    <div className="my-10 rounded-2xl p-6 md:p-8" style={{ backgroundColor: "var(--module-surface)", borderRadius: 18 }}>
      <div className="text-center mb-2">
        <span className="inline-block px-3 py-1 rounded-full text-[11px] font-bold tracking-wider uppercase mb-3" style={{ backgroundColor: moduleFill(COLORS.accentTint), color: moduleText(COLORS.accentDarkText), border: '1px solid rgba(242,107,31,0.2)', letterSpacing: '0.06em' }}>Interactive Activity</span>
        <h4 className="font-serif font-bold" style={{ fontSize: 24, color: "var(--module-ink)" }}>Feedback Translator</h4>
        <p className="text-sm mt-1" style={{ color: "var(--module-muted)" }}>Tap each card to translate harsh "verdict language" into constructive "data language."</p>
      </div>

      {/* Progress chip */}
      <div className="flex justify-center mb-8 mt-3">
        <div className="inline-flex items-center gap-2" style={{ backgroundColor: moduleFill(COLORS.accentTint), border: '1px solid rgba(242,107,31,0.2)', borderRadius: 20, padding: '5px 14px' }}>
          <span style={{ fontSize: 13, fontWeight: 600, color: moduleText(COLORS.accentDarkText) }}>
            {allTranslated ? `All ${feedbackPairs.length} translated ✓` : `${translatedCount} / ${feedbackPairs.length} translated`}
          </span>
        </div>
      </div>

      <div className="space-y-3">
        {feedbackPairs.map((pair, i) => (
          <div key={i}>
            <AnimatePresence mode="wait">
              {!flipped[i] ? (
                <MotionDiv
                  key={`verdict-${i}`}
                  initial={{ opacity: 1 }}
                  exit={{ opacity: 0, rotateY: 90 }}
                  transition={{ duration: 0.25 }}
                  onClick={() => handleFlip(i)}
                  className="cursor-pointer bg-[var(--module-surface)] dark:bg-[var(--module-surface)]"
                  style={{ border: "2px solid var(--module-line)", borderRadius: 14, padding: '20px 22px' }}
                >
                  <span className="inline-block text-[10px] font-bold uppercase tracking-wider mb-2" style={{ backgroundColor: "var(--module-surface)", color: "var(--module-danger-text)", borderRadius: 20, padding: '3px 10px', letterSpacing: '0.1em' }}>Verdict Language</span>
                  <p className="font-serif italic mt-2" style={{ fontSize: 16, color: "var(--module-ink)" }}>{pair.verdict}</p>
                  <p className="flex items-center gap-1.5 mt-3" style={{ fontSize: 12, color: "var(--module-muted)" }}>
                    <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="var(--module-muted)" strokeWidth="2" strokeLinecap="round"><path d="M7 16V4m0 0L3 8m4-4l4 4M17 8v12m0 0l4-4m-4 4l-4-4"/></svg>
                    Tap to translate
                  </p>
                </MotionDiv>
              ) : (
                <MotionDiv
                  key={`data-${i}`}
                  initial={{ opacity: 0, rotateY: -90 }}
                  animate={{ opacity: 1, rotateY: 0 }}
                  transition={{ duration: 0.3 }}
                  className="relative"
                  style={{ backgroundColor: moduleFill(COLORS.successTint), border: `2px solid ${COLORS.success}`, borderRadius: 14, padding: '20px 22px' }}
                >
                  <span className="absolute top-4 right-4 font-bold" style={{ fontSize: 16, color: moduleText(COLORS.success) }}>✓</span>
                  <span className="inline-block text-[10px] font-bold uppercase tracking-wider mb-2" style={{ backgroundColor: moduleFill(COLORS.successTint), color: moduleText(COLORS.successDarkText), borderRadius: 20, padding: '3px 10px', letterSpacing: '0.1em' }}>Data Language</span>
                  <p className="font-serif mt-2" style={{ fontSize: 16, color: "var(--module-ink)" }}>{pair.data}</p>
                  <p className="italic mt-3" style={{ fontSize: 13, color: moduleText(COLORS.success) }}>{pair.shift}</p>
                </MotionDiv>
              )}
            </AnimatePresence>
          </div>
        ))}
      </div>

      {/* Completion */}
      <AnimatePresence>
        {allTranslated && (
          <MotionDiv initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} className="mt-6" style={{ backgroundColor: moduleFill(COLORS.successTint), border: `2px solid ${COLORS.success}`, borderRadius: 16, padding: '20px 24px', textAlign: 'center' }}>
            <p className="font-serif font-semibold" style={{ fontSize: 18, color: moduleText(COLORS.successDarkText) }}>Translation complete.</p>
            <p style={{ fontSize: 14, color: moduleText(COLORS.success), marginTop: 4 }}>You can now hear feedback as information, not judgment.</p>
          </MotionDiv>
        )}
      </AnimatePresence>

      {/* Write Your Own */}
      <div className="mt-10 pt-8" style={{ borderTop: "1px solid var(--module-line)" }}>
        <h5 className="font-serif font-semibold text-center mb-2" style={{ fontSize: 18, color: "var(--module-ink)" }}>Write Your Own</h5>
        <p className="text-center text-sm mb-4" style={{ color: "var(--module-muted)" }}>Type a piece of feedback you've received, then pick the translation that fits best.</p>
        <input
          type="text"
          value={customFeedback}
          onChange={(e) => { setCustomFeedback(e.target.value); setSelectedTranslation(null); }}
          placeholder="e.g. You always make silly mistakes..."
          className="w-full outline-none"
          style={{ backgroundColor: "var(--module-surface)", border: "1.5px solid var(--module-line)", borderRadius: 10, padding: '14px 16px', fontSize: 14, color: "var(--module-ink)" }}
          onFocus={(e) => { e.currentTarget.style.borderColor = COLORS.accent; }}
          onBlur={(e) => { e.currentTarget.style.borderColor = "var(--module-muted)"; }}
        />
        <AnimatePresence>
          {customFeedback.trim().length > 0 && (
            <MotionDiv initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -8 }} className="mt-4 space-y-3">
              <p style={{ fontSize: 10, fontWeight: 700, letterSpacing: '0.12em', color: "var(--module-muted)", textTransform: 'uppercase' as const }}>Pick your growth translation:</p>
              {writeYourOwnTranslations.map((t, i) => (
                <button
                  key={i}
                  onClick={() => setSelectedTranslation(i)}
                  className="w-full text-left text-sm font-medium transition-all"
                  style={selectedTranslation === i
                    ? { backgroundColor: moduleFill(COLORS.successTint), border: `2px solid ${COLORS.success}`, borderRadius: 14, padding: '16px 20px', color: moduleText(COLORS.successDarkText) }
                    : { backgroundColor: "var(--module-surface)", border: "2px solid var(--module-line)", borderRadius: 14, padding: '16px 20px', color: "var(--module-ink)", cursor: 'pointer' }
                  } data-wide-button="true" data-selected={!!(selectedTranslation === i)} data-tone="mint" aria-pressed={!!(selectedTranslation === i)}
                >
                  {t}
                </button>
              ))}
              <AnimatePresence>
                {selectedTranslation !== null && (
                  <MotionDiv initial={{ opacity: 0, y: 6 }} animate={{ opacity: 1, y: 0 }} style={{ backgroundColor: moduleFill(COLORS.successTint), border: `2px solid ${COLORS.success}`, borderRadius: 14, padding: '16px 20px', textAlign: 'center' }}>
                    <p className="font-serif font-semibold" style={{ fontSize: 16, color: moduleText(COLORS.successDarkText) }}>You just turned a verdict into data.</p>
                    <p style={{ fontSize: 13, color: moduleText(COLORS.success), marginTop: 4 }}>That's the growth mindset in action.</p>
                  </MotionDiv>
                )}
              </AnimatePresence>
            </MotionDiv>
          )}
        </AnimatePresence>
      </div>
    </div>
  );
};

// --- MODULE COMPONENT ---
const GrowthMindsetModule: React.FC<{ onBack: () => void; progress: ModuleProgress; onProgressUpdate: (progress: ModuleProgress) => void }> = ({ onBack, progress, onProgressUpdate }) => {
  const essentials = useEssentialsMode();
  const { responses, saveResponse, isLoaded: _isLoaded } = useModuleResponses('growth-mindset-protocol');

  const sections = [
    { id: 'two-brains', title: 'The Two Brains: Fixed vs. Growth', eyebrow: '01 // The Operating System', icon: Cpu },
    { id: 'brain-muscle', title: 'Your Brain is Plastic', eyebrow: '02 // The Hardware Upgrade', icon: BrainCircuit },
    { id: 'power-of-yet', title: 'The Most Powerful Word', eyebrow: '03 // The Software Patch', icon: RotateCcw },
    { id: 'effort-is-key', title: 'Effort is the Real Talent', eyebrow: '04 // The Engine', icon: Zap },
    { id: 'feedback-fuel', title: 'Feedback is Fuel, Not a Verdict', eyebrow: '05 // The Navigation Data', icon: MessageSquareQuote },
    { id: 'install-os', title: 'Installing Your Growth OS', eyebrow: '06 // System Integration', icon: Activity },
  ];

  return (
    <ModuleLayout
      moduleNumber="14"
      moduleTitle="The Growth Playbook"
      moduleSubtitle="The Mind's Operating System"
      moduleDescription={`Your brain can actually change and get better at things — that's not just a nice idea, it's how your brain works. This module shows you how to stop thinking "I'm just not smart enough" and start seeing every challenge as a chance to grow.`}
      theme={theme}
      sections={sections}
      references={GROWTH_MINDSET_REFERENCE_LIST}
      onBack={onBack}
      progress={progress}
      onProgressUpdate={onProgressUpdate}
      finishButtonText="Unlock Growth Mode"
    >
      {(activeSection) => (
        <>
          {activeSection === 0 && (
            <ReadingSection title="The Two Brains: Fixed vs. Growth." eyebrow="Step 1" icon={Cpu} theme={theme}>
              {essentials ? (
                <>
                  <p>Fixed mindset: you believe you are either smart or not. Effort feels pointless. Failing feels permanent. Growth mindset: you believe you can get better with effort. Challenges become opportunities.<Cite n={1} /></p>
                  <p>Which one are you running? Take the diagnostic below to find out.</p>
                </>
              ) : (
                <>
                  <p>Think of your brain like a phone. Some people believe it shipped with whatever apps it's going to have, and that's it. You're born with a certain amount of intelligence, and you're stuck with it. This is the <Highlight description="Basically thinking you're either smart or you're not, and there's nothing you can do about it. If you have this, you'll dodge hard stuff because failing feels like proof you're just not good enough." theme={theme}>Fixed Mindset</Highlight>. When you're running this, effort feels pointless and failing feels like a permanent label on who you are.</p>
                  <p>But your brain is actually more like a phone you can keep upgrading. Every time you learn something new, you're adding new capabilities. This is the <Highlight description="Thinking that you can actually get smarter and better at things by putting in effort and trying new approaches. When you believe this, you stop being scared of hard stuff and start seeing it as a way to level up." theme={theme}>Growth Mindset</Highlight>.<Cite n={1} /> With this one, challenges are chances to get better and failing is just useful information about what to try next. So which one are you running right now?</p>
                  <PersonalStory name="Alex" role="Founder, NextStepUni" junior={{ children: (
                    <p>Growing up in Togher in Cork, I never saw school as something that mattered. I spent my time playing soccer and messing around — I genuinely believed the classroom wasn't for people like me. I fell in with the wrong crowds and was heading nowhere. I failed my Junior Cert, but honestly, I was on that path long before the results came out. The fixed mindset wasn't some concept in a textbook — it was my entire operating system, and I didn't even know it was running.</p>
                  ) }}>
                    <p>Growing up in Togher in Cork, I never saw school as something that mattered. I spent my time playing soccer and messing around — I genuinely believed the classroom wasn't for people like me. I fell in with the wrong crowds, started drinking, and was heading nowhere. I failed my Junior Cert, but honestly, I was on that path long before the results came out. The fixed mindset wasn't some concept in a textbook — it was my entire operating system, and I didn't even know it was running.</p>
                  </PersonalStory>
                </>
              )}
              <MindsetDiagnostic savedAnswers={responses['mindset-diagnostic']} onSaveAnswers={(a) => saveResponse('mindset-diagnostic', a)} />
              <MicroCommitment theme={theme}>
                <p>Listen to how you talk about school today. Catch one "fixed" thought (e.g., "I'm bad at Irish") and just notice it. You don't have to change it yet, just acknowledge you're running that piece of code.</p>
              </MicroCommitment>
            </ReadingSection>
          )}
           {activeSection === 1 && (
            <ReadingSection title="Your Brain is Plastic." eyebrow="Step 2" icon={BrainCircuit} theme={theme}>
              {essentials ? (
                <p>Your brain physically changes when you practise.<Cite n={2} /> Every time you study, you build stronger connections between brain cells. It is like wearing a path through a forest. More practice means a clearer, faster path. Try the simulator below.</p>
              ) : (
                <>
                  <p>Here's the thing most people don't realise: your brain is not set in stone. It physically changes based on what you do with it. This is called <Highlight description="Your brain's ability to physically rewire itself whenever you learn something new. Every time you practise, your brain builds stronger connections — it's literally how learning works under the hood." theme={theme}>Neuroplasticity</Highlight>. Think of learning a new maths formula like walking through a forest. The first time, it's hard going because there's no clear path.</p>
                  <p>But if you walk that same route every day (i.e., you practise the formula), you wear down a clear trail. In your brain, this is literally what happens: the connections between your brain cells get stronger, faster, and more efficient.<Cite n={2} /> You're actually building roads in your head every time you study. Every bit of effort you put in is real construction work happening inside your brain.</p>
                </>
              )}
              <NeuroplasticityVisualizer />
               <MicroCommitment theme={theme}>
                <p>Pick the one school subject you find hardest. Spend just five minutes tonight reviewing a topic from it. You just sent a work crew to start clearing a new path in your brain's forest.</p>
              </MicroCommitment>
            </ReadingSection>
          )}
           {activeSection === 2 && (
            <ReadingSection title="The Most Powerful Word." eyebrow="Step 3" icon={RotateCcw} theme={theme}>
                {essentials ? (
                  <p>Add the word "yet" to any fixed statement. "I cannot do this" becomes "I cannot do this yet." It keeps the door open. It tells your brain the story is not over. Try the reframe challenge below.</p>
                ) : (
                  <>
                    <p>A fixed mindset talks in absolutes: "I can't do this." "I'm not good at this." These are dead ends. They shut down effort and kill motivation. But there's a ridiculously simple fix: the word "yet."</p>
                    <p>Adding "yet" to the end of a fixed statement instantly changes it from a full stop into a work in progress. "I can't do this" becomes "I can't do this... yet." "I'm not good at this" becomes "I'm not good at this... yet." It sounds small, but it tells your brain the story isn't over. It keeps the door open for new approaches and more effort, and that's what keeps you going.</p>
                    <PersonalStory name="Alex" role="Founder, NextStepUni" junior={{ children: (
                      <p>After I lost one of my best friends during my Junior Cert years, my whole world shattered. But at some point, something shifted. I started reading about how people actually learn, and I realised the voice that had been telling me "you can't do this" was just a habit, not a fact. I built my own study system, and "I can't" slowly became "I can't yet." It felt fake at first — but bit by bit, it started to prove itself true.</p>
                    ) }}>
                      <p>After I lost one of my best friends during Junior Cert, my whole world shattered. In 4th year, something shifted. I started reading about how people actually learn, and I realised the voice that had been telling me "you can't do this" was just a habit, not a fact. I built my own study system, and "I can't" slowly became "I can't yet." It felt fake at first. But I went from failing my Junior Cert to nearly 600 points in the Leaving Cert and a UCC Scholarship. The "yet" was real — I just had to give it time to prove itself.</p>
                    </PersonalStory>
                  </>
                )}
                <ReframeChallenge savedText={responses['reframe-text']} onSave={(t) => saveResponse('reframe-text', t)} />
                <MicroCommitment theme={theme}>
                    <p>The next time you hear a friend (or yourself) say a "fixed" statement like "I don't get this," add a gentle "...yet?" at the end. You're installing the software patch for them.</p>
                </MicroCommitment>
            </ReadingSection>
          )}
           {activeSection === 3 && (
            <ReadingSection title="Effort is the Real Talent." eyebrow="Step 4" icon={Zap} theme={theme}>
                {essentials ? (
                  <p>Talent gives you a head start. Effort is what actually makes you better. Focused practice on the hard bits builds real brain connections.<Cite n={3} /> If something feels hard, that is not a sign you are not smart enough. That is the process of getting smarter.</p>
                ) : (
                  <>
                    <p>Everyone loves the idea of "natural talent." We see someone who's brilliant at something and assume they were just born that way. This is one of the most unhelpful ideas out there. It teaches us that if something doesn't come easily, we must not be cut out for it.</p>
                    <p>But that's just not true. Talent might give you a head start, but effort is what actually makes you better. It's <Highlight description="Practising with focus on the bits you actually find hard, not just repeating the easy stuff. It's the kind of effort that stretches you just enough to make your brain build new connections and get better." theme={theme}>Deliberate Practice</Highlight><Cite n={3} /> — the focused, targeted kind — that builds those strong brain connections we talked about earlier. A growth mindset gets this: effort isn't a sign you're not smart enough. It's literally the process of getting smarter.</p>
                  </>
                )}
                <MicroCommitment theme={theme}>
                    <p>Identify one area where you rely on "talent". Now, identify one tiny, effortful action you can take to actually improve it. (e.g., If you're 'naturally good' at English, spend 10 minutes learning one new sophisticated word).</p>
                </MicroCommitment>
            </ReadingSection>
          )}
           {activeSection === 4 && (
            <ReadingSection title="Feedback is Fuel, Not a Verdict." eyebrow="Step 5" icon={MessageSquareQuote} theme={theme}>
              {essentials ? (
                <p>Fixed mindset hears feedback as "you are stupid." Growth mindset hears "here is what to do differently." A bad grade is a signpost, not a label.<Cite n={4} /> Separate how you did from who you are. Try the translator below.</p>
              ) : (
                <>
                  <p>A fixed mindset hears criticism and thinks: "They're telling me I'm stupid." It treats feedback like a final judgement on who you are. This is why people with a fixed mindset get defensive or just give up when they get a bad grade or a harsh correction from a teacher.</p>
                  <p>A growth mindset hears the exact same criticism and thinks: "OK, so what can I do differently next time?" It treats feedback as useful information, not a personal attack. It's not about you as a person — it's about what you did this time. A bad grade isn't a label. It's a signpost showing you where to focus.<Cite n={4} /> Learning to separate how you did from who you are is one of the most useful things you can do.</p>
                </>
              )}
              <FeedbackTranslator />
              <MicroCommitment theme={theme}>
                <p>Go back to a piece of work where you got a lower grade than you wanted. Find one comment from the teacher and write down what strategy it's telling you to try next time.</p>
              </MicroCommitment>
            </ReadingSection>
          )}
           {activeSection === 5 && (
            <ReadingSection title="Installing Your Growth OS." eyebrow="Step 6" icon={Activity} theme={theme}>
              {essentials ? (
                <p>Growth mindset is a daily practice, not a one-time switch. Change how you talk to yourself. React to mistakes with curiosity, not shame. You become "the person working on getting better" instead of "the person who is bad at it."</p>
              ) : (
                <>
                  <p>A growth mindset isn't a magic switch you flip once. It's something you choose to practise every day through small, consistent habits: the way you talk to yourself, the way you react to mistakes, and the way you approach something difficult.</p>
                  <p>Once you start thinking this way, something cool happens. You stop being "the person who's bad at Maths" and become "the person who's working on getting better at Maths." That might sound like a small change, but it's massive. It's the difference between giving up and keeping going. And that's what this whole module has been building towards.</p>
                </>
              )}
               <MicroCommitment theme={theme}>
                <p>Write down your favourite "Growth Mindset Mantra" from this module. Stick it on your bedroom wall, your mirror, or the inside of your school journal. Make it visible.</p>
              </MicroCommitment>
            </ReadingSection>
          )}
        </>
      )}
    </ModuleLayout>
  );
};
export default GrowthMindsetModule;
