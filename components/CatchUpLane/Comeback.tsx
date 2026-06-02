/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Catch-Up Lane — Arm 2: "Your Comeback".
 *
 * A guided, interactive flow where the student BUILDS a personal re-entry plan:
 * warm open → see the avoidance loop → your why → name what's hard → build your
 * comeback (tiny step + if-then + script) → your people + safe space → saved plan.
 *
 * Evidence-grounded (NEPS/EBSA, self-compassion, implementation intentions/MCII,
 * Irish supports). Shame is designed out: never asks why they were absent, no
 * days-missed counters. Aesthetics: Headspace-immersive — a warm dawn colour
 * field with white cards inset, gentle motion, the plan building up as they go.
 */

import React, { useMemo, useState } from 'react';
import { AnimatePresence } from 'framer-motion';
import { MotionDiv } from '../Motion';
import { ArrowLeft, ArrowRight, Check, Heart, ChevronDown, RotateCcw, Sun, Shield, BookOpenCheck } from 'lucide-react';
import { COLORS } from '../../design/tokens';
import PrimaryActionButton from '../ui/PrimaryActionButton';
import { useProgress } from '../../contexts/ProgressContext';
import {
  LOOP_STEPS, OBSTACLES, PEER_SCRIPTS, TEACHER_SCRIPT, SUPPORT_PEOPLE, EWO_NOTE, GROUNDING, WHY_OPTIONS,
} from '../../comebackData';
import { type ComebackPlan } from '../../types/catchUpLane';

const INK = '#1a1a1a';
const WARM_FIELD = 'linear-gradient(165deg, #FFEAD6 0%, #FFD9D2 52%, #F7D9E6 100%)';
const WARM_LABEL = '#8C3A0E';   // accent-dark-text — readable warm label on the field

const card = 'rounded-2xl bg-white dark:bg-zinc-900 border border-white/60 dark:border-zinc-700 shadow-[0_8px_30px_rgba(180,90,40,0.12)] p-5 md:p-6';
const fade = { initial: { opacity: 0, y: 12 }, animate: { opacity: 1, y: 0 }, exit: { opacity: 0, y: -8 }, transition: { duration: 0.24 } };

type Step = 0 | 1 | 2 | 3 | 4 | 5 | 'summary';

interface ComebackProps {
  saved?: ComebackPlan;
  onSave: (plan: Omit<ComebackPlan, 'savedAt'>) => void;
  onExit: () => void;
  onGoContent: () => void;
}

const Comeback: React.FC<ComebackProps> = ({ saved, onSave, onExit, onGoContent }) => {
  const { northStar } = useProgress();
  const [step, setStep] = useState<Step>(saved ? 'summary' : 0);

  // plan being built
  const [why, setWhy] = useState(saved?.why ?? '');
  const [obstacleIds, setObstacleIds] = useState<string[]>(saved?.obstacleIds ?? []);
  const [actionText, setActionText] = useState(saved?.ifThen.action ?? '');
  const [script, setScript] = useState(saved?.script ?? '');
  const [person, setPerson] = useState(saved?.person ?? '');
  const [safeSpace, setSafeSpace] = useState(saved?.safeSpace ?? '');
  const [showGrounding, setShowGrounding] = useState(false);

  const primary = useMemo(() => OBSTACLES.find(o => o.id === obstacleIds[0]) ?? null, [obstacleIds]);
  const northStarWhy = (northStar as { headline?: string; goal?: string; label?: string } | null)?.headline
    ?? (northStar as { goal?: string } | null)?.goal ?? null;

  const toggleObstacle = (id: string) =>
    setObstacleIds(prev => prev.includes(id) ? prev.filter(x => x !== id) : [...prev, id]);

  const finish = () => {
    if (!primary) return;
    onSave({
      why,
      obstacleIds,
      firstStep: primary.firstStep,
      ifThen: { trigger: primary.ifThen.trigger, action: actionText || primary.ifThen.action },
      script,
      person,
      safeSpace,
    });
    setStep('summary');
  };

  // shared chrome -------------------------------------------------
  const Dots = ({ active }: { active: number }) => (
    <div className="flex items-center gap-1.5 justify-center mb-5">
      {[0, 1, 2, 3, 4, 5].map(s => (
        <span key={s} className="h-1.5 rounded-full transition-all" style={{ width: s === active ? 20 : 6, backgroundColor: s <= active ? '#E07A4E' : 'rgba(140,58,14,0.22)' }} />
      ))}
    </div>
  );

  const Field: React.FC<{ children: React.ReactNode }> = ({ children }) => (
    <div className="w-full max-w-xl mx-auto relative overflow-hidden rounded-3xl p-4 md:p-6" style={{ background: WARM_FIELD }}>
      {/* soft depth blobs */}
      <div className="absolute -top-10 -right-8 w-40 h-40 rounded-full" style={{ background: 'rgba(255,255,255,0.35)', filter: 'blur(8px)' }} aria-hidden />
      <div className="absolute -bottom-12 -left-10 w-44 h-44 rounded-full" style={{ background: 'rgba(224,122,78,0.18)', filter: 'blur(10px)' }} aria-hidden />
      <div className="relative">{children}</div>
    </div>
  );

  const backRow = (onBack: () => void, label = 'Back') => (
    <button onClick={onBack} className="flex items-center gap-1.5 text-[13px] font-medium mb-3" style={{ color: WARM_LABEL }}>
      <ArrowLeft size={15} /> {label}
    </button>
  );

  // ── SUMMARY (saved plan) ───────────────────────────────────────
  if (step === 'summary') {
    const ob = OBSTACLES.find(o => o.id === (saved?.obstacleIds[0] ?? obstacleIds[0]));
    const plan = saved ?? null;
    return (
      <Field>
        <button onClick={onExit} className="flex items-center gap-1.5 text-[13px] font-medium mb-4" style={{ color: WARM_LABEL }}>
          <ArrowLeft size={15} /> Catch-Up Lane
        </button>
        <div className="flex items-center gap-2 mb-3">
          <div className="w-9 h-9 rounded-full flex items-center justify-center" style={{ backgroundColor: '#fff' }}><Heart size={18} style={{ color: '#E07A4E' }} /></div>
          <h2 className="text-2xl font-semibold" style={{ fontFamily: "'Source Serif 4', serif", color: INK }}>Your comeback plan</h2>
        </div>
        <p className="text-[14px] mb-4" style={{ color: WARM_LABEL }}>Someone’s glad you’re back. Here’s your plan — it’s here whenever you need it.</p>

        <div className={card}>
          {[
            ['Your why', why || plan?.why],
            ['Your tiny first step', plan?.firstStep ?? primary?.firstStep],
            ['Your if-then', `${plan?.ifThen.trigger ?? primary?.ifThen.trigger} — ${plan?.ifThen.action ?? actionText}`],
            ['If someone asks where you were', script || plan?.script],
            ['Your person', person || plan?.person],
            ['Your safe space', safeSpace || plan?.safeSpace],
          ].filter(([, v]) => v).map(([k, v]) => (
            <div key={k as string} className="py-2.5 border-b border-zinc-100 dark:border-zinc-800 last:border-0">
              <p className="text-[10px] font-bold uppercase tracking-[0.12em] mb-0.5" style={{ color: '#E07A4E' }}>{k}</p>
              <p className="text-[14px] leading-snug" style={{ color: '#2a2622' }}>{v}</p>
            </div>
          ))}
        </div>

        <button onClick={() => setShowGrounding(v => !v)} className="w-full mt-3 flex items-center justify-between rounded-2xl bg-white/70 px-4 py-3">
          <span className="text-[13px] font-semibold" style={{ color: INK }}>{GROUNDING.title}</span>
          <ChevronDown size={16} style={{ color: WARM_LABEL, transform: showGrounding ? 'rotate(180deg)' : 'none', transition: 'transform .2s' }} />
        </button>
        {showGrounding && (
          <div className="mt-2 rounded-2xl bg-white/80 px-4 py-3 space-y-1.5">
            {GROUNDING.steps.map((s, i) => <p key={i} className="text-[13px] leading-relaxed" style={{ color: '#3a3530' }}>• {s}</p>)}
          </div>
        )}

        <div className="flex gap-2 mt-4">
          <button onClick={() => { setStep(0); }} className="flex-1 py-3 rounded-full text-[14px] font-semibold inline-flex items-center justify-center gap-2 bg-white/80" style={{ color: WARM_LABEL }}>
            <RotateCcw size={15} /> Redo my plan
          </button>
          <PrimaryActionButton label="Done" icon={Check} onClick={onExit} className="flex-1" />
        </div>
      </Field>
    );
  }

  // ── WIZARD ─────────────────────────────────────────────────────
  return (
    <Field>
      <button onClick={onExit} className="flex items-center gap-1.5 text-[13px] font-medium mb-2" style={{ color: WARM_LABEL }}>
        <ArrowLeft size={15} /> Catch-Up Lane
      </button>
      <Dots active={step as number} />
      <AnimatePresence mode="wait">
        {/* 0 — warm open */}
        {step === 0 && (
          <MotionDiv key="s0" {...fade} className={card}>
            <div className="w-12 h-12 rounded-full flex items-center justify-center mb-4" style={{ background: 'linear-gradient(135deg,#FFD9A8,#FFB38A)' }}><Sun size={24} className="text-white" /></div>
            <h2 className="text-2xl font-semibold mb-2" style={{ fontFamily: "'Source Serif 4', serif", color: INK }}>Coming back is the hard part — and you’re already doing it</h2>
            <p className="text-[15px] leading-relaxed mb-6" style={{ color: '#5a5550' }}>Let’s make the first morning feel smaller, together. We’ll build a short plan that’s yours — no big questions about where you’ve been, just a few steps to make walking back in easier.</p>
            <PrimaryActionButton label="Let’s build it" icon={ArrowRight} onClick={() => setStep(1)} />
          </MotionDiv>
        )}

        {/* 1 — see the loop */}
        {step === 1 && (
          <MotionDiv key="s1" {...fade} className={card}>
            {backRow(() => setStep(0))}
            <h3 className="text-xl font-semibold mb-1" style={{ fontFamily: "'Source Serif 4', serif", color: INK }}>Why it gets harder the longer you wait</h3>
            <p className="text-[13px] mb-4" style={{ color: '#7a7068' }}>This is a loop, not a you-problem.</p>
            <div className="space-y-2 mb-5">
              {LOOP_STEPS.map((l, i) => (
                <MotionDiv key={i} initial={{ opacity: 0, x: -8 }} animate={{ opacity: 1, x: 0 }} transition={{ delay: 0.12 * i }} className="rounded-xl px-3.5 py-2.5" style={{ backgroundColor: '#FFF4EC' }}>
                  <p className="text-[14px] font-semibold" style={{ color: INK }}>{l.label}</p>
                  <p className="text-[12.5px] leading-snug" style={{ color: '#6a625b' }}>{l.note}</p>
                </MotionDiv>
              ))}
            </div>
            <div className="rounded-xl px-4 py-3 mb-5" style={{ backgroundColor: '#fff' }}>
              <p className="text-[14px] leading-relaxed" style={{ color: '#2a2622' }}><span className="font-semibold">You break the loop with one small thing</span> — not by feeling ready first. That’s what this plan is for.</p>
            </div>
            <div className="flex justify-end"><PrimaryActionButton label="Makes sense" icon={ArrowRight} onClick={() => setStep(2)} /></div>
          </MotionDiv>
        )}

        {/* 2 — your why */}
        {step === 2 && (
          <MotionDiv key="s2" {...fade} className={card}>
            {backRow(() => setStep(1))}
            <h3 className="text-xl font-semibold mb-1" style={{ fontFamily: "'Source Serif 4', serif", color: INK }}>First — your why</h3>
            <p className="text-[13px] mb-4" style={{ color: '#7a7068' }}>Pick the reason it’s worth it. (A plan tied to your own why is far more likely to actually happen.)</p>
            <div className="space-y-2 mb-5">
              {(northStarWhy ? [northStarWhy, ...WHY_OPTIONS] : WHY_OPTIONS).map((w, i) => (
                <button key={i} onClick={() => setWhy(w)} className="w-full text-left rounded-xl px-4 py-3 transition-colors flex items-center gap-2.5" style={{ backgroundColor: why === w ? '#FFE0CC' : '#fff', border: why === w ? '2px solid #E07A4E' : '2px solid transparent' }}>
                  <span className="w-5 h-5 rounded-full flex items-center justify-center shrink-0" style={why === w ? { backgroundColor: '#E07A4E' } : { border: '2px solid #e0cdbf' }}>{why === w && <Check size={12} strokeWidth={3} className="text-white" />}</span>
                  <span className="text-[14px]" style={{ color: '#2a2622' }}>{w}{i === 0 && northStarWhy ? ' ✦' : ''}</span>
                </button>
              ))}
            </div>
            <div className="flex justify-end"><PrimaryActionButton label="Next" icon={ArrowRight} onClick={() => setStep(3)} disabled={!why} /></div>
          </MotionDiv>
        )}

        {/* 3 — name what's hard */}
        {step === 3 && (
          <MotionDiv key="s3" {...fade} className={card}>
            {backRow(() => setStep(2))}
            <h3 className="text-xl font-semibold mb-1" style={{ fontFamily: "'Source Serif 4', serif", color: INK }}>What makes coming back hard right now?</h3>
            <p className="text-[13px] mb-4" style={{ color: '#7a7068' }}>Tap whatever’s true. We’ll start with the first one you pick.</p>
            <div className="space-y-2 mb-5">
              {OBSTACLES.map(o => {
                const on = obstacleIds.includes(o.id);
                return (
                  <button key={o.id} onClick={() => toggleObstacle(o.id)} className="w-full text-left rounded-xl px-4 py-3 transition-colors flex items-center gap-2.5" style={{ backgroundColor: on ? '#FFE0CC' : '#fff', border: on ? '2px solid #E07A4E' : '2px solid transparent' }}>
                    <span className="w-5 h-5 rounded-md flex items-center justify-center shrink-0" style={on ? { backgroundColor: '#E07A4E' } : { border: '2px solid #e0cdbf' }}>{on && <Check size={12} strokeWidth={3} className="text-white" />}</span>
                    <span className="text-[14px]" style={{ color: '#2a2622' }}>{o.label}</span>
                  </button>
                );
              })}
            </div>
            <div className="flex justify-end"><PrimaryActionButton label="Next" icon={ArrowRight} onClick={() => { setActionText(primary?.ifThen.action ?? ''); setStep(4); }} disabled={obstacleIds.length === 0} /></div>
          </MotionDiv>
        )}

        {/* 4 — build your comeback */}
        {step === 4 && primary && (
          <MotionDiv key="s4" {...fade} className={card}>
            {backRow(() => setStep(3))}
            {/* reframe (self-compassion) */}
            <div className="rounded-xl px-4 py-3 mb-4" style={{ backgroundColor: '#FFF4EC' }}>
              <p className="text-[14px] leading-relaxed italic" style={{ color: '#5a4a3e' }}>{primary.reframe}</p>
            </div>

            <p className="text-[10px] font-bold uppercase tracking-[0.12em] mb-1" style={{ color: '#E07A4E' }}>Your tiny first step</p>
            <p className="text-[15px] mb-4" style={{ color: INK, fontFamily: "'Source Serif 4', serif" }}>{primary.firstStep}</p>

            {primary.id === 'so-behind' && (
              <button onClick={onGoContent} className="w-full mb-4 rounded-xl px-4 py-2.5 text-[13px] font-semibold inline-flex items-center justify-center gap-2 bg-white" style={{ color: '#0B6E7A' }}>
                <BookOpenCheck size={15} /> Catch up on what you missed →
              </button>
            )}

            <p className="text-[10px] font-bold uppercase tracking-[0.12em] mb-1.5" style={{ color: '#E07A4E' }}>Your if-then plan</p>
            <div className="rounded-xl px-4 py-3 mb-2" style={{ backgroundColor: '#fff' }}>
              <p className="text-[13.5px] font-medium mb-2" style={{ color: '#2a2622' }}>{primary.ifThen.trigger}…</p>
              <textarea value={actionText} onChange={e => setActionText(e.target.value)} rows={2} className="w-full text-[13.5px] rounded-lg p-2 outline-none resize-none" style={{ backgroundColor: '#FFF4EC', color: '#2a2622' }} placeholder="…then I’ll…" />
            </div>
            <p className="text-[11px] mb-4" style={{ color: WARM_LABEL }}>Read it back to yourself once — that’s what makes it stick.</p>

            <p className="text-[10px] font-bold uppercase tracking-[0.12em] mb-1.5" style={{ color: '#E07A4E' }}>If someone asks “where were you?”</p>
            <div className="space-y-1.5 mb-5">
              {PEER_SCRIPTS.map((s, i) => (
                <button key={i} onClick={() => setScript(s)} className="w-full text-left rounded-lg px-3 py-2 text-[13.5px] transition-colors" style={{ backgroundColor: script === s ? '#FFE0CC' : '#fff', border: script === s ? '2px solid #E07A4E' : '2px solid transparent', color: '#2a2622' }}>“{s}”</button>
              ))}
            </div>
            <div className="flex justify-end"><PrimaryActionButton label="Next" icon={ArrowRight} onClick={() => setStep(5)} disabled={!script} /></div>
          </MotionDiv>
        )}

        {/* 5 — your people + safe space */}
        {step === 5 && (
          <MotionDiv key="s5" {...fade} className={card}>
            {backRow(() => setStep(4))}
            <div className="flex items-center gap-2 mb-1">
              <Shield size={18} style={{ color: '#E07A4E' }} />
              <h3 className="text-xl font-semibold" style={{ fontFamily: "'Source Serif 4', serif", color: INK }}>Who’s got your back?</h3>
            </div>
            <p className="text-[13px] mb-3" style={{ color: '#7a7068' }}>Pick one person to tell you’re back. Having one trusted adult is one of the biggest things that helps.</p>

            <div className="flex flex-wrap gap-1.5 mb-2">
              {SUPPORT_PEOPLE.map(p => (
                <button key={p.id} onClick={() => setPerson(p.role)} className="rounded-full px-3 py-1.5 text-[12.5px] font-medium transition-colors" style={{ backgroundColor: person === p.role ? '#E07A4E' : '#fff', color: person === p.role ? '#fff' : '#2a2622' }}>{p.role}{p.deis ? ' · DEIS' : ''}</button>
              ))}
            </div>
            <input value={person} onChange={e => setPerson(e.target.value)} className="w-full rounded-lg px-3 py-2.5 text-[14px] outline-none mb-4 bg-white" style={{ color: '#2a2622' }} placeholder="…or type their name" />

            <p className="text-[10px] font-bold uppercase tracking-[0.12em] mb-1.5" style={{ color: '#E07A4E' }}>Your safe space if it gets too much</p>
            <input value={safeSpace} onChange={e => setSafeSpace(e.target.value)} className="w-full rounded-lg px-3 py-2.5 text-[14px] outline-none mb-4 bg-white" style={{ color: '#2a2622' }} placeholder="e.g. the library, the guidance office, the year head’s room" />

            {/* who-can-help reference */}
            <div className="rounded-xl px-4 py-3 mb-3 bg-white/70">
              <p className="text-[11px] font-bold uppercase tracking-[0.1em] mb-2" style={{ color: WARM_LABEL }}>Who can help, and what to say</p>
              <div className="space-y-2.5">
                {SUPPORT_PEOPLE.map(p => (
                  <div key={p.id}>
                    <p className="text-[13px] font-semibold" style={{ color: INK }}>{p.role}{p.deis && <span className="ml-1.5 text-[9px] font-bold uppercase tracking-wide px-1.5 py-0.5 rounded-full align-middle" style={{ backgroundColor: '#FFE0CC', color: WARM_LABEL }}>DEIS</span>}</p>
                    <p className="text-[12px] leading-snug" style={{ color: '#6a625b' }}>{p.whatTheyDo}</p>
                    <p className="text-[12px] leading-snug mt-0.5" style={{ color: '#8a7e74' }}>{p.script}</p>
                  </div>
                ))}
                <p className="text-[11.5px] leading-snug pt-1" style={{ color: '#8a7e74' }}>{EWO_NOTE}</p>
              </div>
            </div>

            <div className="flex justify-end"><PrimaryActionButton label="Save my plan" icon={Check} onClick={finish} disabled={!person} /></div>
          </MotionDiv>
        )}
      </AnimatePresence>
    </Field>
  );
};

export default Comeback;
