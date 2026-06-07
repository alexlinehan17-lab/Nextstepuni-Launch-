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
 * days-missed counters.
 *
 * Aesthetic: the app's chunky bordered card system (matches arm 1 + the other
 * tools) — white cardShell, cyan Catch-Up Lane identity, accent-orange CTAs,
 * cool tints, no warm gradient fields. The warmth lives in the copy + tone.
 */

import React, { useMemo, useState } from 'react';
import { AnimatePresence } from 'framer-motion';
import { MotionDiv } from '../Motion';
import { ArrowLeft, ArrowRight, Check, CheckCircle2, Circle, Heart, ChevronDown, RotateCcw, Shield, BookOpenCheck, Sparkles, Sunrise } from 'lucide-react';
import { COLORS } from '../../design/tokens';
import PrimaryActionButton from '../ui/PrimaryActionButton';
import { useProgress } from '../../contexts/ProgressContext';
import {
  LOOP_STEPS, OBSTACLES, PEER_SCRIPTS, SUPPORT_PEOPLE, EWO_NOTE, GROUNDING, WHY_OPTIONS,
  FIRST_WEEK, TEACHER_SCRIPT,
} from '../../comebackData';
import { type ComebackPlan, type FirstWeekDayProgress } from '../../types/catchUpLane';

const CYAN = '#0E9AA8';
const CYAN_TINT = '#E6F4F5';
const CYAN_DARK_TEXT = '#0A5560';
const INK = '#1a1a1a';

const cardShell =
  'w-full max-w-xl mx-auto rounded-2xl border-2 border-[#1A1A1A] dark:border-zinc-700 bg-white dark:bg-zinc-900 shadow-[4px_4px_0_0_#1A1A1A] dark:shadow-[4px_4px_0_0_#3f3f46] p-6 md:p-7';
const fade = { initial: { opacity: 0, y: 10 }, animate: { opacity: 1, y: 0 }, exit: { opacity: 0, y: -8 }, transition: { duration: 0.22 } };

type Step = 0 | 1 | 2 | 3 | 4 | 5 | 'summary';

interface ComebackProps {
  saved?: ComebackPlan;
  onSave: (plan: Omit<ComebackPlan, 'savedAt'>) => void;
  onExit: () => void;
  onGoContent: () => void;
  /** Patch one day of the First-Week-Back timeline (persisted by the hook). */
  onDayUpdate?: (day: number, patch: Partial<FirstWeekDayProgress>) => void;
}

const Comeback: React.FC<ComebackProps> = ({ saved, onSave, onExit, onGoContent, onDayUpdate }) => {
  const { northStar } = useProgress();
  const [step, setStep] = useState<Step>(saved ? 'summary' : 0);

  const [why, setWhy] = useState(saved?.why ?? '');
  const [obstacleIds, setObstacleIds] = useState<string[]>(saved?.obstacleIds ?? []);
  const [actionText, setActionText] = useState(saved?.ifThen.action ?? '');
  const [script, setScript] = useState(saved?.script ?? '');
  const [person, setPerson] = useState(saved?.person ?? '');
  const [safeSpace, setSafeSpace] = useState(saved?.safeSpace ?? '');
  const [showGrounding, setShowGrounding] = useState(false);
  const [showPlan, setShowPlan] = useState(false);
  // Per-day reflection drafts (local until the student marks the day done).
  const [reflectDrafts, setReflectDrafts] = useState<Record<number, string>>({});

  const primary = useMemo(() => OBSTACLES.find(o => o.id === obstacleIds[0]) ?? null, [obstacleIds]);
  const northStarWhy = (northStar as { headline?: string; goal?: string } | null)?.headline
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

  // shared bits ---------------------------------------------------
  const inputCls = 'w-full rounded-xl px-3 py-2.5 text-[14px] outline-none bg-white dark:bg-zinc-800 border-2 border-zinc-200 dark:border-zinc-700 focus:border-[#0E9AA8] text-zinc-800 dark:text-zinc-100';

  const Back = ({ onClick, label = 'Catch-Up Lane' }: { onClick: () => void; label?: string }) => (
    <button onClick={onClick} className="flex items-center gap-1.5 text-[13px] font-medium text-zinc-500 hover:text-zinc-800 dark:hover:text-zinc-200 mb-4 max-w-xl mx-auto w-full">
      <ArrowLeft size={15} /> {label}
    </button>
  );

  const Dots = ({ active }: { active: number }) => (
    <div className="flex items-center gap-1.5 justify-center mb-4 max-w-xl mx-auto">
      {[0, 1, 2, 3, 4, 5].map(s => (
        <span key={s} className="h-1.5 rounded-full transition-all" style={{ width: s === active ? 20 : 6, backgroundColor: s <= active ? CYAN : '#E2E0DC' }} />
      ))}
    </div>
  );

  const label = (t: string) => <p className="text-[10px] font-bold uppercase tracking-[0.12em] mb-1.5" style={{ color: CYAN_DARK_TEXT }}>{t}</p>;

  // ── FIRST WEEK BACK (the living timeline) ──────────────────────
  // Reached once a plan is saved. The static record becomes a graded 5-day
  // walk: one cue-bound if-then a day, the right adult on the right day, a
  // quiet reflection that closes the loop, and a non-punitive "not today".
  if (step === 'summary') {
    const eff = {
      why: saved?.why ?? why,
      ifThen: saved?.ifThen ?? { trigger: primary?.ifThen.trigger ?? '', action: actionText || primary?.ifThen.action || '' },
      script: saved?.script ?? script,
      person: saved?.person ?? person,
      safeSpace: saved?.safeSpace ?? safeSpace,
    };
    const fw = saved?.firstWeek;
    const dayDone = (d: number) => Boolean(fw?.days[d]?.doneAt);
    const currentDay = FIRST_WEEK.find(d => !dayDone(d.day))?.day ?? null;
    const allDone = currentDay === null;

    const planRows: [string, string | undefined][] = [
      ['Your why', eff.why],
      ['If someone asks where you were', eff.script],
      ['Your person', eff.person],
      ['Your safe space', eff.safeSpace],
    ];

    return (
      <div className="w-full">
        <Back onClick={onExit} />
        <div className={cardShell}>
          <div className="flex items-center gap-2.5 mb-1">
            <div className="w-9 h-9 rounded-xl flex items-center justify-center" style={{ backgroundColor: CYAN_TINT }}><Sunrise size={18} style={{ color: CYAN }} /></div>
            <h2 className="text-xl font-semibold" style={{ fontFamily: "'Source Serif 4', serif", color: INK }}>Your first week back</h2>
          </div>
          <p className="text-[14px] mb-4" style={{ color: '#5a5550' }}>
            {allDone
              ? 'You walked the whole week back in — one small step at a time. That’s the loop broken.'
              : 'One small, do-able thing a day. We’ll take the week together — you don’t have to feel ready first.'}
          </p>

          {/* day stepper (done = green, today = cyan, ahead = muted — never rainbow) */}
          <div className="flex items-center gap-1.5 justify-center mb-5">
            {FIRST_WEEK.map(d => {
              const done = dayDone(d.day);
              const isCur = d.day === currentDay;
              return <span key={d.day} className="h-2 rounded-full transition-all" style={{ width: isCur ? 24 : 9, backgroundColor: done ? COLORS.success : isCur ? CYAN : '#d0cdc8' }} />;
            })}
          </div>

          <div className="space-y-2.5">
            {FIRST_WEEK.map(d => {
              const done = dayDone(d.day);
              const isCur = d.day === currentDay;

              if (done) {
                const refl = fw?.days[d.day]?.reflection;
                return (
                  <div key={d.day} className="flex gap-2.5 px-1">
                    <CheckCircle2 size={18} style={{ color: COLORS.success }} className="shrink-0 mt-0.5" />
                    <div className="flex-1 min-w-0">
                      <p className="text-[13.5px] font-semibold" style={{ color: '#5a6a64' }}>Day {d.day} · {d.title}</p>
                      {refl && <p className="text-[12.5px] italic leading-snug mt-0.5" style={{ color: '#7a7068' }}>“{refl}”</p>}
                    </div>
                  </div>
                );
              }

              if (isCur) {
                const it = d.ifThen ?? eff.ifThen; // day 1's ifThen is null → use the student's own
                const softened = Boolean(fw?.days[d.day]?.softened);
                const draft = reflectDrafts[d.day] ?? '';
                return (
                  <div key={d.day} className="rounded-xl border-2 p-4" style={{ borderColor: CYAN }}>
                    <p className="text-[10px] font-bold uppercase tracking-[0.14em] mb-1" style={{ color: CYAN_DARK_TEXT }}>Today · Day {d.day} of 5</p>
                    <h3 className="text-lg font-semibold mb-1.5" style={{ fontFamily: "'Source Serif 4', serif", color: INK }}>{d.title}</h3>

                    {softened && primary && (
                      <div className="rounded-xl px-3.5 py-2.5 mb-3" style={{ backgroundColor: CYAN_TINT }}>
                        <p className="text-[13px] leading-relaxed italic mb-1" style={{ color: '#2a4a4a' }}>{primary.reframe}</p>
                        <p className="text-[12.5px]" style={{ color: CYAN_DARK_TEXT }}>No rush — this step waits for you. Come back to it when you’re ready.</p>
                      </div>
                    )}

                    <p className="text-[14px] leading-relaxed mb-3" style={{ color: '#3a3530' }}>{d.goal}</p>

                    {(it.trigger || it.action) && (
                      <div className="rounded-xl px-3.5 py-3 mb-3" style={{ backgroundColor: CYAN_TINT }}>
                        <div className="flex items-center gap-1.5 mb-1"><Sparkles size={14} style={{ color: CYAN }} /><span className="text-[10px] font-bold uppercase tracking-[0.12em]" style={{ color: CYAN_DARK_TEXT }}>Today’s if-then</span></div>
                        <p className="text-[13.5px] leading-snug" style={{ color: '#2a2622' }}>{it.trigger}, {it.action}</p>
                      </div>
                    )}

                    {d.useTeacherScript && (
                      <div className="rounded-xl px-3.5 py-3 mb-3 border-2 border-zinc-200 dark:border-zinc-700">
                        <p className="text-[10px] font-bold uppercase tracking-[0.12em] mb-1" style={{ color: CYAN_DARK_TEXT }}>Your person today</p>
                        <p className="text-[13.5px] font-semibold mb-1" style={{ color: INK }}>{eff.person || 'Your year head or tutor'}</p>
                        <p className="text-[12.5px] leading-snug italic" style={{ color: '#5a6a6a' }}>“{TEACHER_SCRIPT}”</p>
                      </div>
                    )}

                    {d.linkCatchUp && (
                      <button onClick={onGoContent} className="w-full mb-3 rounded-xl px-4 py-2.5 text-[13px] font-semibold inline-flex items-center justify-center gap-2 border-2" style={{ borderColor: CYAN, color: CYAN_DARK_TEXT }}>
                        <BookOpenCheck size={15} /> Clear one Catch-Up topic →
                      </button>
                    )}

                    <p className="text-[12px] mb-1.5" style={{ color: '#7a7068' }}>{d.reflectPrompt}</p>
                    <textarea
                      value={draft}
                      onChange={e => setReflectDrafts(p => ({ ...p, [d.day]: e.target.value }))}
                      rows={2}
                      className="w-full text-[13.5px] rounded-lg p-2.5 outline-none resize-none border-2 border-zinc-200 focus:border-[#0E9AA8] mb-3"
                      style={{ backgroundColor: '#F6F6F4', color: '#2a2622' }}
                      placeholder="One line, just for you (optional)"
                    />

                    <div className="flex flex-col sm:flex-row gap-2.5">
                      <PrimaryActionButton label="I did this today" icon={Check} onClick={() => onDayUpdate?.(d.day, { doneAt: new Date().toISOString(), reflection: draft.trim() || undefined })} />
                      <button onClick={() => onDayUpdate?.(d.day, { softened: true })} className="px-5 py-3 rounded-full text-[14px] font-semibold border-2 border-zinc-200 dark:border-zinc-700 text-zinc-600 dark:text-zinc-300 inline-flex items-center justify-center gap-2">
                        Not today
                      </button>
                    </div>
                  </div>
                );
              }

              // ahead of the student — shown muted so they can see the shape of the week
              return (
                <div key={d.day} className="flex gap-2.5 px-1 opacity-60">
                  <Circle size={18} className="shrink-0 mt-0.5 text-zinc-300 dark:text-zinc-600" />
                  <p className="text-[13.5px] font-medium" style={{ color: '#9e9186' }}>Day {d.day} · {d.title}</p>
                </div>
              );
            })}
          </div>

          {allDone && (
            <div className="rounded-xl px-4 py-3 mt-4" style={{ backgroundColor: COLORS.successTint }}>
              <p className="text-[13.5px] leading-relaxed" style={{ color: COLORS.successDarkText }}>That’s your first week back, done. The dread said it was impossible — and you did it one small step at a time. Keep your person close.</p>
            </div>
          )}

          {/* the full plan, tucked away */}
          <button onClick={() => setShowPlan(v => !v)} className="w-full mt-4 flex items-center justify-between rounded-xl px-4 py-3 border-2 border-zinc-200 dark:border-zinc-700">
            <span className="text-[13px] font-semibold" style={{ color: INK }}>Your plan</span>
            <ChevronDown size={16} className="text-zinc-400" style={{ transform: showPlan ? 'rotate(180deg)' : 'none', transition: 'transform .2s' }} />
          </button>
          {showPlan && (
            <div className="mt-2 rounded-xl overflow-hidden" style={{ backgroundColor: CYAN_TINT }}>
              {planRows.filter(([, v]) => v).map(([k, v], i) => (
                <div key={k} className={`px-4 py-2.5 ${i > 0 ? 'border-t border-white/70' : ''}`}>
                  <p className="text-[10px] font-bold uppercase tracking-[0.1em] mb-0.5" style={{ color: CYAN_DARK_TEXT }}>{k}</p>
                  <p className="text-[14px] leading-snug" style={{ color: '#2a2622' }}>{v}</p>
                </div>
              ))}
            </div>
          )}

          <button onClick={() => setShowGrounding(v => !v)} className="w-full mt-2.5 flex items-center justify-between rounded-xl px-4 py-3 border-2 border-zinc-200 dark:border-zinc-700">
            <span className="text-[13px] font-semibold" style={{ color: INK }}>{GROUNDING.title}</span>
            <ChevronDown size={16} className="text-zinc-400" style={{ transform: showGrounding ? 'rotate(180deg)' : 'none', transition: 'transform .2s' }} />
          </button>
          {showGrounding && (
            <div className="mt-2 rounded-xl px-4 py-3 space-y-1.5" style={{ backgroundColor: CYAN_TINT }}>
              {GROUNDING.steps.map((s, i) => <p key={i} className="text-[13px] leading-relaxed" style={{ color: '#3a3530' }}>• {s}</p>)}
            </div>
          )}

          <div className="flex flex-col sm:flex-row gap-2.5 mt-5">
            <PrimaryActionButton label="Done for now" icon={Check} onClick={onExit} />
            <button onClick={() => setStep(0)} className="px-5 py-3 rounded-full text-[14px] font-semibold border-2 border-zinc-200 dark:border-zinc-700 text-zinc-600 dark:text-zinc-300 inline-flex items-center justify-center gap-2">
              <RotateCcw size={15} /> Redo my plan
            </button>
          </div>
        </div>
      </div>
    );
  }

  // ── WIZARD ─────────────────────────────────────────────────────
  return (
    <div className="w-full">
      <Back onClick={onExit} />
      <Dots active={step as number} />
      <AnimatePresence mode="wait">
        {/* 0 — open */}
        {step === 0 && (
          <MotionDiv key="s0" {...fade} className={cardShell}>
            <div className="w-12 h-12 rounded-xl flex items-center justify-center mb-4" style={{ backgroundColor: CYAN_TINT }}><Heart size={24} style={{ color: CYAN }} /></div>
            <h2 className="text-2xl font-semibold mb-2" style={{ fontFamily: "'Source Serif 4', serif", color: INK }}>Coming back is the hard part — and you’re already doing it</h2>
            <p className="text-[15px] leading-relaxed mb-6" style={{ color: '#5a5550' }}>Let’s make the first morning feel smaller, together. We’ll build a short plan that’s yours — no big questions about where you’ve been, just a few steps to make walking back in easier.</p>
            <PrimaryActionButton label="Let’s build it" icon={ArrowRight} onClick={() => setStep(1)} />
          </MotionDiv>
        )}

        {/* 1 — loop */}
        {step === 1 && (
          <MotionDiv key="s1" {...fade} className={cardShell}>
            <h3 className="text-xl font-semibold mb-1" style={{ fontFamily: "'Source Serif 4', serif", color: INK }}>Why it gets harder the longer you wait</h3>
            <p className="text-[13px] mb-4" style={{ color: '#7a7068' }}>This is a loop, not a you-problem.</p>
            <div className="space-y-2 mb-5">
              {LOOP_STEPS.map((l, i) => (
                <MotionDiv key={i} initial={{ opacity: 0, x: -8 }} animate={{ opacity: 1, x: 0 }} transition={{ delay: 0.12 * i }} className="rounded-xl px-3.5 py-2.5" style={{ backgroundColor: '#F6F6F4' }}>
                  <p className="text-[14px] font-semibold" style={{ color: INK }}>{l.label}</p>
                  <p className="text-[12.5px] leading-snug" style={{ color: '#6a625b' }}>{l.note}</p>
                </MotionDiv>
              ))}
            </div>
            <div className="rounded-xl px-4 py-3 mb-5" style={{ backgroundColor: CYAN_TINT }}>
              <p className="text-[14px] leading-relaxed" style={{ color: '#2a2622' }}><span className="font-semibold">You break the loop with one small thing</span> — not by feeling ready first. That’s what this plan is for.</p>
            </div>
            <div className="flex justify-between items-center">
              <button onClick={() => setStep(0)} className="text-[13px] font-medium text-zinc-400 hover:text-zinc-700">Back</button>
              <PrimaryActionButton label="Makes sense" icon={ArrowRight} onClick={() => setStep(2)} />
            </div>
          </MotionDiv>
        )}

        {/* 2 — why */}
        {step === 2 && (
          <MotionDiv key="s2" {...fade} className={cardShell}>
            <h3 className="text-xl font-semibold mb-1" style={{ fontFamily: "'Source Serif 4', serif", color: INK }}>First — your why</h3>
            <p className="text-[13px] mb-4" style={{ color: '#7a7068' }}>Pick the reason it’s worth it. A plan tied to your own why is far more likely to actually happen.</p>
            <div className="space-y-2 mb-5">
              {(northStarWhy ? [northStarWhy, ...WHY_OPTIONS] : WHY_OPTIONS).map((w, i) => {
                const on = why === w;
                return (
                  <button key={i} onClick={() => setWhy(w)} className="w-full text-left rounded-xl px-4 py-3 transition-colors flex items-center gap-2.5" style={{ backgroundColor: on ? CYAN_TINT : '#F6F6F4', border: on ? `2px solid ${CYAN}` : '2px solid transparent' }}>
                    <span className="w-5 h-5 rounded-full flex items-center justify-center shrink-0" style={on ? { backgroundColor: CYAN } : { border: '2px solid #d0cdc8' }}>{on && <Check size={12} strokeWidth={3} className="text-white" />}</span>
                    <span className="text-[14px]" style={{ color: '#2a2622' }}>{w}{i === 0 && northStarWhy ? ' ✦' : ''}</span>
                  </button>
                );
              })}
            </div>
            <div className="flex justify-between items-center">
              <button onClick={() => setStep(1)} className="text-[13px] font-medium text-zinc-400 hover:text-zinc-700">Back</button>
              <PrimaryActionButton label="Next" icon={ArrowRight} onClick={() => setStep(3)} disabled={!why} />
            </div>
          </MotionDiv>
        )}

        {/* 3 — obstacle */}
        {step === 3 && (
          <MotionDiv key="s3" {...fade} className={cardShell}>
            <h3 className="text-xl font-semibold mb-1" style={{ fontFamily: "'Source Serif 4', serif", color: INK }}>What makes coming back hard right now?</h3>
            <p className="text-[13px] mb-4" style={{ color: '#7a7068' }}>Tap whatever’s true. We’ll start with the first one you pick.</p>
            <div className="space-y-2 mb-5">
              {OBSTACLES.map(o => {
                const on = obstacleIds.includes(o.id);
                return (
                  <button key={o.id} onClick={() => toggleObstacle(o.id)} className="w-full text-left rounded-xl px-4 py-3 transition-colors flex items-center gap-2.5" style={{ backgroundColor: on ? CYAN_TINT : '#F6F6F4', border: on ? `2px solid ${CYAN}` : '2px solid transparent' }}>
                    <span className="w-5 h-5 rounded-md flex items-center justify-center shrink-0" style={on ? { backgroundColor: CYAN } : { border: '2px solid #d0cdc8' }}>{on && <Check size={12} strokeWidth={3} className="text-white" />}</span>
                    <span className="text-[14px]" style={{ color: '#2a2622' }}>{o.label}</span>
                  </button>
                );
              })}
            </div>
            <div className="flex justify-between items-center">
              <button onClick={() => setStep(2)} className="text-[13px] font-medium text-zinc-400 hover:text-zinc-700">Back</button>
              <PrimaryActionButton label="Next" icon={ArrowRight} onClick={() => { setActionText(primary?.ifThen.action ?? ''); setStep(4); }} disabled={obstacleIds.length === 0} />
            </div>
          </MotionDiv>
        )}

        {/* 4 — build */}
        {step === 4 && primary && (
          <MotionDiv key="s4" {...fade} className={cardShell}>
            <div className="rounded-xl px-4 py-3 mb-4" style={{ backgroundColor: CYAN_TINT }}>
              <p className="text-[14px] leading-relaxed italic" style={{ color: '#2a4a4a' }}>{primary.reframe}</p>
            </div>

            {label('Your tiny first step')}
            <p className="text-[15px] mb-4" style={{ color: INK, fontFamily: "'Source Serif 4', serif" }}>{primary.firstStep}</p>

            {primary.id === 'so-behind' && (
              <button onClick={onGoContent} className="w-full mb-4 rounded-xl px-4 py-2.5 text-[13px] font-semibold inline-flex items-center justify-center gap-2 border-2" style={{ borderColor: CYAN, color: CYAN_DARK_TEXT }}>
                <BookOpenCheck size={15} /> Catch up on what you missed →
              </button>
            )}

            {label('Your if-then plan')}
            <div className="rounded-xl px-4 py-3 mb-2 border-2 border-zinc-200 dark:border-zinc-700">
              <p className="text-[13.5px] font-medium mb-2" style={{ color: '#2a2622' }}>{primary.ifThen.trigger}…</p>
              <textarea value={actionText} onChange={e => setActionText(e.target.value)} rows={2} className="w-full text-[13.5px] rounded-lg p-2 outline-none resize-none border border-zinc-200 focus:border-[#0E9AA8]" style={{ backgroundColor: '#F6F6F4', color: '#2a2622' }} placeholder="…then I’ll…" />
            </div>
            <p className="text-[11px] mb-4" style={{ color: CYAN_DARK_TEXT }}>Read it back to yourself once — that’s what makes it stick.</p>

            {label('If someone asks “where were you?”')}
            <div className="space-y-1.5 mb-5">
              {PEER_SCRIPTS.map((s, i) => {
                const on = script === s;
                return (
                  <button key={i} onClick={() => setScript(s)} className="w-full text-left rounded-lg px-3 py-2 text-[13.5px] transition-colors" style={{ backgroundColor: on ? CYAN_TINT : '#F6F6F4', border: on ? `2px solid ${CYAN}` : '2px solid transparent', color: '#2a2622' }}>“{s}”</button>
                );
              })}
            </div>
            <div className="flex justify-between items-center">
              <button onClick={() => setStep(3)} className="text-[13px] font-medium text-zinc-400 hover:text-zinc-700">Back</button>
              <PrimaryActionButton label="Next" icon={ArrowRight} onClick={() => setStep(5)} disabled={!script} />
            </div>
          </MotionDiv>
        )}

        {/* 5 — people + safe space */}
        {step === 5 && (
          <MotionDiv key="s5" {...fade} className={cardShell}>
            <div className="flex items-center gap-2 mb-1">
              <Shield size={18} style={{ color: CYAN }} />
              <h3 className="text-xl font-semibold" style={{ fontFamily: "'Source Serif 4', serif", color: INK }}>Who’s got your back?</h3>
            </div>
            <p className="text-[13px] mb-3" style={{ color: '#7a7068' }}>Pick one person to tell you’re back. Having one trusted adult is one of the biggest things that helps.</p>

            <div className="flex flex-wrap gap-1.5 mb-2">
              {SUPPORT_PEOPLE.map(p => (
                <button key={p.id} onClick={() => setPerson(p.role)} className="rounded-full px-3 py-1.5 text-[12.5px] font-medium transition-colors" style={{ backgroundColor: person === p.role ? CYAN : '#F6F6F4', color: person === p.role ? '#fff' : '#2a2622' }}>{p.role}{p.deis ? ' · DEIS' : ''}</button>
              ))}
            </div>
            <input value={person} onChange={e => setPerson(e.target.value)} className={`${inputCls} mb-4`} placeholder="…or type their name" />

            {label('Your safe space if it gets too much')}
            <input value={safeSpace} onChange={e => setSafeSpace(e.target.value)} className={`${inputCls} mb-4`} placeholder="e.g. the library, the guidance office, the year head’s room" />

            <div className="rounded-xl px-4 py-3 mb-4" style={{ backgroundColor: CYAN_TINT }}>
              <p className="text-[11px] font-bold uppercase tracking-[0.1em] mb-2" style={{ color: CYAN_DARK_TEXT }}>Who can help, and what to say</p>
              <div className="space-y-2.5">
                {SUPPORT_PEOPLE.map(p => (
                  <div key={p.id}>
                    <p className="text-[13px] font-semibold" style={{ color: INK }}>{p.role}{p.deis && <span className="ml-1.5 text-[9px] font-bold uppercase tracking-wide px-1.5 py-0.5 rounded-full align-middle" style={{ backgroundColor: '#fff', color: CYAN_DARK_TEXT }}>DEIS</span>}</p>
                    <p className="text-[12px] leading-snug" style={{ color: '#5a6a6a' }}>{p.whatTheyDo}</p>
                    <p className="text-[12px] leading-snug mt-0.5 italic" style={{ color: '#6a7a7a' }}>{p.script}</p>
                  </div>
                ))}
                <p className="text-[11.5px] leading-snug pt-1" style={{ color: '#5a6a6a' }}>{EWO_NOTE}</p>
              </div>
            </div>

            <div className="flex justify-between items-center">
              <button onClick={() => setStep(4)} className="text-[13px] font-medium text-zinc-400 hover:text-zinc-700">Back</button>
              <PrimaryActionButton label="Save my plan" icon={Check} onClick={finish} disabled={!person} />
            </div>
          </MotionDiv>
        )}
      </AnimatePresence>
    </div>
  );
};

export default Comeback;
