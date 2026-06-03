/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * "Your Possible Life" — the keystone that connects the effort a student puts
 * in NOW to the LIFE it makes possible (subjects → results → pathways →
 * careers → lifestyle). Structured as WOOP (Wish → Reality → Plan), NOT a
 * lifestyle-fantasy generator: the evidence is clear that dwelling on an
 * idealised future alone saps effort, especially for teens, so every bright
 * future is contrasted with the honest present and bound to a concrete plan.
 * Money is one ingredient of a life, shown in support — never a worth-score.
 * "Possibilities, not predictions": the student steers it.
 *
 * Engine reuse: bestSixPoints (current AND target grades) · reachBucket via
 * careerReach · CAREERS/matchStrings ↔ CAO_COURSES · computeBargains · the
 * Career Paths colour worlds. Net-new maths lives in effortLifeModel
 * (irishNetPay, lifestyleFromNet), authored + verified like careerPathsData.
 */

import React, { useMemo, useState, useEffect, useRef } from 'react';
import { MotionDiv } from './Motion';
import {
  ArrowLeft, ArrowRight, RotateCcw, Star, Home, Car, PiggyBank, Plane,
  Heart, Compass, TrendingUp, Sparkles, GraduationCap, type LucideIcon,
} from 'lucide-react';
import { CAREERS } from '../careerPathsData';
import { type CareerCard, type CareerField } from '../types/careerPaths';
import { WORLDS, type ColorWorld, CountUp, Celebration } from './immersiveDeck';
import { CAO_COURSES, type CAOCourse } from './futureFinderData';
import { useInnovationData } from '../contexts/InnovationDataContext';
import { useProgress } from '../contexts/ProgressContext';
import { useEffortLifeSim } from '../hooks/useEffortLifeSim';
import { hydrateCourses } from './futureFinderData';
import {
  type StudentSubjectProfile, computeBargains, type Bargain,
} from './subjectData';
import {
  irishNetPay, lifestyleFromNet, bestSixPoints, careerReach,
  LIFE_REGIONS, LIFE_REGION_LABELS, type LifeRegion,
} from './effortLifeModel';

/** Each career field owns a colour world (same mapping as Career Paths). */
const FIELD_WORLD: Record<CareerField, ColorWorld> = {
  health: WORLDS.teal,
  animals: WORLDS.forest,
  tech: WORLDS.ocean,
  engineering: WORLDS.slate,
  law: WORLDS.indigo,
  psychology: WORLDS.rose,
  business: WORLDS.denim,
  education: WORLDS.terracotta,
  design: WORLDS.rust,
  science: WORLDS.pine,
  trades: WORLDS.cocoa,
  creative: WORLDS.claret,
};
const LANDING = WORLDS.denim;

const SERIF = "'Source Serif 4', serif";
const euroK = (k: number) => `€${k}k`;

/** Courses that lead to this career — same runtime join as Career Paths. */
const coursesFor = (c: CareerCard): CAOCourse[] =>
  CAO_COURSES.filter((course) => course.careerPaths.some((cp) => c.matchStrings.includes(cp)))
    .sort((a, b) => b.level - a.level || b.typicalPoints - a.typicalPoints)
    .slice(0, 6);

type Step = 'pick' | 'life' | 'reality' | 'plan' | 'steer';
const STEP_ORDER: Step[] = ['pick', 'life', 'reality', 'plan', 'steer'];

// ─── Small shared faces ──────────────────────────────────────────────────────

const Surface: React.FC<{ wd: ColorWorld; children: React.ReactNode }> = ({ wd, children }) => (
  <div className="relative rounded-[28px] border-2 border-[#1A1A1A] overflow-hidden" style={{ backgroundColor: wd.bg, boxShadow: '6px 8px 0 0 #1A1A1A', color: wd.onBg }}>
    <div className="absolute -top-12 -right-10 w-48 h-48 rounded-full pointer-events-none" style={{ backgroundColor: wd.glow, opacity: 0.4, filter: 'blur(10px)' }} />
    <div className="relative p-6 md:p-7">{children}</div>
  </div>
);

const Label: React.FC<{ children: React.ReactNode }> = ({ children }) => (
  <p className="text-[10px] font-bold uppercase tracking-[0.16em] mb-3" style={{ color: 'rgba(255,255,255,0.7)' }}>{children}</p>
);

const WorldButton: React.FC<{ label: string; icon?: LucideIcon; onClick: () => void; wd: ColorWorld }> = ({ label, icon: Icon, onClick, wd }) => (
  <button onClick={onClick} className="inline-flex items-center gap-2 px-5 py-3 rounded-full text-[14px] font-semibold transition-transform active:translate-y-0.5" style={{ backgroundColor: '#fff', color: wd.deep, boxShadow: '0 4px 0 0 rgba(0,0,0,0.18)' }}>
    {label} {Icon && <Icon size={16} />}
  </button>
);

const GhostBack: React.FC<{ onClick: () => void; label?: string }> = ({ onClick, label = 'Back' }) => (
  <button onClick={onClick} className="text-[13px] font-medium" style={{ color: 'rgba(255,255,255,0.7)' }}>{label}</button>
);

const StepDots: React.FC<{ step: Step }> = ({ step }) => {
  const idx = STEP_ORDER.indexOf(step);
  return (
    <div className="flex items-center gap-1.5">
      {STEP_ORDER.map((_, s) => (
        <span key={s} className="h-1.5 rounded-full transition-all" style={{ width: s === idx ? 18 : 6, backgroundColor: s <= idx ? '#fff' : 'rgba(255,255,255,0.35)' }} />
      ))}
    </div>
  );
};

/** A toggle pill pair (used for horizon + region segments). */
const Segment: React.FC<{ options: { value: string; label: string }[]; value: string; onChange: (v: string) => void; wd: ColorWorld }> = ({ options, value, onChange, wd }) => (
  <div className="inline-flex rounded-full p-1" style={{ backgroundColor: 'rgba(0,0,0,0.18)' }}>
    {options.map((o) => {
      const active = o.value === value;
      return (
        <button key={o.value} onClick={() => onChange(o.value)} className="px-3.5 py-1.5 rounded-full text-[12.5px] font-semibold transition-colors" style={active ? { backgroundColor: '#fff', color: wd.deep } : { color: 'rgba(255,255,255,0.85)' }}>
          {o.label}
        </button>
      );
    })}
  </div>
);

// ─── Component ────────────────────────────────────────────────────────────────

const YourPossibleLife: React.FC<{ uid?: string; profile: StudentSubjectProfile }> = ({ uid, profile }) => {
  const { futureFinderPicks } = useInnovationData();
  const { rawProgressDoc } = useProgress();
  const { saved, isLoaded: simLoaded, save, reset } = useEffortLifeSim(uid);

  const [step, setStep] = useState<Step>('pick');
  const [careerId, setCareerId] = useState<string | null>(null);
  const [region, setRegion] = useState<LifeRegion>('city');
  const [horizon, setHorizon] = useState<'start' | 'experienced'>('start');
  const [why, setWhy] = useState('');
  const [showManual, setShowManual] = useState(false);
  const [burst, setBurst] = useState(false);

  // Best-6 points on current ("coast") vs target ("push") grades.
  const currentPoints = useMemo(() => bestSixPoints(profile, 'current'), [profile]);
  const targetPoints = useMemo(() => Math.max(bestSixPoints(profile, 'target'), currentPoints), [profile, currentPoints]);
  const hasGrades = currentPoints > 0 || targetPoints > 0;
  const bargains = useMemo<Bargain[]>(() => computeBargains(profile), [profile]);

  // Careers the student's Future Finder (either tool) points toward, in FF order.
  const ffCourses = useMemo(() => {
    const revamped = hydrateCourses((rawProgressDoc?.futureFinderRevamped?.picks as string[] | undefined) ?? []);
    return [...futureFinderPicks, ...revamped];
  }, [futureFinderPicks, rawProgressDoc]);

  const matchedCareers = useMemo<CareerCard[]>(() => {
    const seen = new Set<string>();
    const ordered: CareerCard[] = [];
    for (const course of ffCourses) {
      for (const career of CAREERS) {
        if (seen.has(career.id)) continue;
        if (career.matchStrings.some((m) => course.careerPaths.includes(m))) {
          seen.add(career.id);
          ordered.push(career);
        }
      }
    }
    return ordered;
  }, [ffCourses]);
  const hasMatches = matchedCareers.length > 0;
  const topMatch = matchedCareers[0] ?? null;

  // Seed from saved state once loaded — restore the student's last exploration.
  const seedRef = useRef(false);
  useEffect(() => {
    if (!simLoaded || seedRef.current) return;
    seedRef.current = true;
    if (saved?.careerId && CAREERS.some((c) => c.id === saved.careerId)) {
      setCareerId(saved.careerId);
      if (saved.region) setRegion(saved.region);
      if (saved.horizon) setHorizon(saved.horizon);
      if (saved.why) setWhy(saved.why);
      setStep('life');
    }
  }, [simLoaded, saved]);

  // Persist selections (not keystrokes of `why` — that saves on blur).
  useEffect(() => {
    if (!simLoaded || !seedRef.current || !careerId) return;
    save({ careerId, region, horizon });
  }, [careerId, region, horizon, simLoaded, save]);

  const career = careerId ? CAREERS.find((c) => c.id === careerId) ?? null : null;

  // Guard: never sit on a career screen without a career.
  useEffect(() => { if (step !== 'pick' && !career) setStep('pick'); }, [step, career]);

  const chooseCareer = (id: string) => { setCareerId(id); setShowManual(false); setStep('life'); };
  const goReality = () => setStep('reality');
  const goPlan = () => setStep('plan');
  const goSteer = () => { setStep('steer'); setBurst(true); window.setTimeout(() => setBurst(false), 950); };
  const startOver = () => { setCareerId(null); setShowManual(false); setStep('pick'); };

  // ── PICK (the Wish seed) ────────────────────────────────────────────────
  if (step === 'pick') {
    const wd = topMatch ? FIELD_WORLD[topMatch.field] : LANDING;
    return (
      <div className="w-full max-w-xl mx-auto pb-12">
        {hasMatches && !showManual && topMatch ? (
          <Surface wd={wd}>
            <div className="flex items-center justify-between mb-5">
              <span className="inline-flex items-center gap-1.5 text-[10px] font-bold uppercase tracking-[0.12em] px-2.5 py-1 rounded-full" style={{ backgroundColor: '#fff', color: wd.deep }}><Star size={11} /> Your Future Finder match</span>
              <StepDots step="pick" />
            </div>
            <div className="flex items-center gap-3.5 mb-4">
              <div className="w-16 h-16 rounded-full flex items-center justify-center shrink-0" style={{ backgroundColor: wd.chip }}><span style={{ fontSize: 33, lineHeight: 1 }}>{topMatch.emoji}</span></div>
              <div>
                <h2 className="text-[24px] font-semibold leading-tight" style={{ fontFamily: SERIF }}>{topMatch.title}</h2>
                <p className="text-[13.5px]" style={{ color: wd.onSoft }}>{topMatch.tagline}</p>
              </div>
            </div>
            <p className="text-[16px] leading-snug mb-6" style={{ color: wd.onSoft }}>
              Let's explore the life this could open up — and the bridge from your grades today to get there. A possibility you steer, not a prediction.
            </p>

            {matchedCareers.length > 1 && (
              <>
                <Label>Or swap to another of your matches</Label>
                <div className="flex flex-wrap gap-1.5 mb-6">
                  {matchedCareers.slice(0, 6).map((c) => (
                    <button key={c.id} onClick={() => chooseCareer(c.id)} className="inline-flex items-center gap-1.5 text-[12.5px] font-medium px-3 py-1.5 rounded-full transition-transform active:translate-y-0.5" style={{ backgroundColor: wd.chip, color: '#fff' }}>
                      <span>{c.emoji}</span> {c.title}
                    </button>
                  ))}
                </div>
              </>
            )}

            <div className="flex flex-col sm:flex-row gap-2.5">
              <WorldButton label="Explore this life" icon={ArrowRight} onClick={() => chooseCareer(topMatch.id)} wd={wd} />
              <button onClick={() => setShowManual(true)} className="px-5 py-3 rounded-full text-[13.5px] font-semibold" style={{ border: '2px solid rgba(255,255,255,0.5)', color: '#fff' }}>
                Pick a different career
              </button>
            </div>
          </Surface>
        ) : (
          <Surface wd={LANDING}>
            <div className="flex items-center justify-between mb-5">
              <span className="inline-flex items-center gap-1.5 text-[10px] font-bold uppercase tracking-[0.12em] px-2.5 py-1 rounded-full" style={{ backgroundColor: LANDING.chip, color: '#fff' }}><Compass size={11} /> Pick a future to explore</span>
              <StepDots step="pick" />
            </div>
            <p className="text-[22px] leading-tight font-semibold mb-2" style={{ fontFamily: SERIF }}>Pick a path, and we'll explore the life it could open up.</p>
            <p className="text-[15px] leading-snug mb-6" style={{ color: LANDING.onSoft }}>
              {hasMatches ? 'Choose any career below.' : "Haven't done the Future Finder yet? No problem — choose any career and we'll work out the nitty-gritty."} A possibility you steer, not a prediction.
            </p>
            <div className="grid grid-cols-2 gap-2.5">
              {CAREERS.map((c) => {
                const matched = matchedCareers.some((m) => m.id === c.id);
                return (
                  <button key={c.id} onClick={() => chooseCareer(c.id)} className="flex items-center gap-2.5 rounded-2xl p-3 text-left transition-transform active:translate-y-0.5" style={{ backgroundColor: '#fff', color: '#1a1a1a' }}>
                    <span className="w-9 h-9 rounded-full flex items-center justify-center shrink-0" style={{ backgroundColor: FIELD_WORLD[c.field].bg }}><span style={{ fontSize: 18 }}>{c.emoji}</span></span>
                    <span className="min-w-0">
                      <span className="block text-[13.5px] font-semibold leading-tight truncate">{c.title}</span>
                      <span className="block text-[11px] text-zinc-500">{euroK(c.salary.startK)} → {euroK(c.salary.experiencedK)}{matched ? ' · ★ match' : ''}</span>
                    </span>
                  </button>
                );
              })}
            </div>
            {hasMatches && (
              <button onClick={() => setShowManual(false)} className="mt-5 text-[13px] font-medium" style={{ color: 'rgba(255,255,255,0.8)' }}>← Back to your match</button>
            )}
          </Surface>
        )}
      </div>
    );
  }

  if (!career) return null;
  const wd = FIELD_WORLD[career.field];
  const grossK = horizon === 'experienced' ? career.salary.experiencedK : career.salary.startK;
  const pay = irishNetPay(grossK * 1000);
  const life = lifestyleFromNet(pay.netMonthly, region);
  const courses = coursesFor(career);
  const reach = careerReach(courses, currentPoints, targetPoints);

  // ── LIFE (Wish / Outcome — vivid, plural) ───────────────────────────────
  if (step === 'life') {
    return (
      <div className="w-full max-w-xl mx-auto pb-12">
        <button onClick={startOver} className="flex items-center gap-1.5 text-[13px] font-medium text-zinc-500 hover:text-zinc-800 dark:hover:text-zinc-200 mb-4"><ArrowLeft size={15} /> Pick another path</button>
        <Surface wd={wd}>
          <div className="flex items-center justify-between mb-5">
            <span className="inline-flex items-center gap-2 text-[15px] font-semibold"><span style={{ fontSize: 22 }}>{career.emoji}</span> {career.title}</span>
            <StepDots step="life" />
          </div>

          <Label>The life this could open up</Label>
          <p className="text-[20px] leading-snug font-semibold mb-4" style={{ fontFamily: SERIF }}>{life.vignette}</p>

          {/* Horizon — entry → established progression, felt not stated. */}
          <div className="flex items-center gap-2 mb-2">
            <Segment wd={wd} value={horizon} onChange={(v) => setHorizon(v as 'start' | 'experienced')} options={[{ value: 'start', label: 'Starting out' }, { value: 'experienced', label: 'A few years in' }]} />
          </div>
          <div className="flex items-center gap-2 mb-5">
            <Segment wd={wd} value={region} onChange={(v) => setRegion(v as LifeRegion)} options={LIFE_REGIONS.map((r) => ({ value: r, label: r === 'dublin' ? 'Dublin' : r === 'city' ? 'City' : 'Town' }))} />
            <span className="text-[11.5px]" style={{ color: wd.onSoft }}>{LIFE_REGION_LABELS[region]}</span>
          </div>

          {/* Affordance card — the scannable, honest backbone. */}
          <div className="rounded-2xl p-4 mb-3" style={{ backgroundColor: '#fff', color: '#1a1a1a' }}>
            <div className="space-y-3">
              {[
                { icon: Home, label: life.housing, sub: life.housingDetail },
                { icon: Car, label: life.transport },
                { icon: PiggyBank, label: life.saving },
                { icon: Plane, label: life.travel },
              ].map((row, i) => {
                const Icon = row.icon;
                return (
                  <div key={i} className="flex items-start gap-3">
                    <span className="w-8 h-8 rounded-full flex items-center justify-center shrink-0" style={{ backgroundColor: wd.bg }}><Icon size={15} style={{ color: '#fff' }} /></span>
                    <span className="min-w-0">
                      <span className="block text-[14px] font-semibold leading-snug">{row.label}</span>
                      {row.sub && <span className="block text-[12px] text-zinc-500 leading-snug">{row.sub}</span>}
                    </span>
                  </div>
                );
              })}
            </div>
            <div className="mt-3.5 pt-3 border-t border-zinc-100 flex items-center justify-between">
              <span className="text-[11.5px] uppercase tracking-[0.12em] font-bold text-zinc-400">{life.tier}</span>
              <span className="text-[13px] text-zinc-600">
                ~<CountUp to={Math.round(pay.netMonthly)} durationMs={700} format={(n) => `€${n.toLocaleString()}`} className="font-semibold text-zinc-800" />/mo take-home
              </span>
            </div>
          </div>

          <p className="text-[12px] leading-snug mb-6" style={{ color: wd.onSoft }}>{life.caveat}</p>

          <div className="flex justify-end">
            <WorldButton label="Where am I heading now?" icon={ArrowRight} onClick={goReality} wd={wd} />
          </div>
        </Surface>
      </div>
    );
  }

  // ── REALITY (the honest contrast) ───────────────────────────────────────
  if (step === 'reality') {
    const reachable = reach.reachNow === 'safety' || reach.reachNow === 'match' || reach.reachNow === 'open';
    let headline: string;
    let body: string;
    if (!hasGrades) {
      headline = 'Add your grades to see the gap';
      body = 'Pop your current and target grades into your subject profile and this becomes real — the honest distance between today and there.';
    } else if (reach.entryPoints == null) {
      // No CAO points threshold — an apprenticeship/PLC route, or no mapped
      // course. Either way there's no points race to render, so never touch
      // reach.entryPoints below.
      headline = "There's a route in that doesn't ride on points";
      body = reach.hasOpenRoute
        ? `${career.title} has an apprenticeship or PLC route — you can start without a CAO points race at all. Effort still counts, just differently.`
        : `${career.title} has routes that don't hinge on a CAO points race. Effort still counts here, just differently.`;
    } else if (reachable) {
      headline = 'Good news — your grades are already pointing here';
      body = `Where your current grades land (~${currentPoints} pts) already reaches the most accessible route in (~${reach.entryPoints} pts). The plan is about making it safe and keeping your options open.`;
    } else {
      headline = `A gap of about ${reach.gapFromCurrent} points — and it closes faster than you'd think`;
      body = `Right now your grades project ~${currentPoints} pts. The most accessible route into ${career.title} is ~${reach.entryPoints} pts. ${reach.gapFromTarget === 0 ? "Your own targets already close it — the next screen shows the moves." : "The next screen shows exactly which grades close it."}`;
    }
    return (
      <div className="w-full max-w-xl mx-auto pb-12">
        <button onClick={() => setStep('life')} className="flex items-center gap-1.5 text-[13px] font-medium text-zinc-500 hover:text-zinc-800 dark:hover:text-zinc-200 mb-4"><ArrowLeft size={15} /> The life</button>
        <Surface wd={wd}>
          <div className="flex items-center justify-between mb-5">
            <span className="inline-flex items-center gap-1.5 text-[10px] font-bold uppercase tracking-[0.12em] px-2.5 py-1 rounded-full" style={{ backgroundColor: wd.chip, color: '#fff' }}><Compass size={11} /> Where you're heading now</span>
            <StepDots step="reality" />
          </div>

          {hasGrades && (
            <div className="flex items-stretch gap-3 mb-5">
              <div className="flex-1 rounded-2xl p-3.5 text-center" style={{ backgroundColor: wd.chip }}>
                <p className="text-[10px] uppercase tracking-[0.12em] font-bold mb-1" style={{ color: wd.onSoft }}>Your grades now</p>
                <p className="text-[30px] font-bold leading-none" style={{ fontFamily: SERIF }}>{currentPoints}</p>
                <p className="text-[11px] mt-1" style={{ color: wd.onSoft }}>projected points</p>
              </div>
              <div className="flex items-center"><ArrowRight size={18} style={{ color: wd.onSoft }} /></div>
              <div className="flex-1 rounded-2xl p-3.5 text-center" style={{ backgroundColor: '#fff', color: '#1a1a1a' }}>
                <p className="text-[10px] uppercase tracking-[0.12em] font-bold mb-1 text-zinc-400">Route in</p>
                <p className="text-[30px] font-bold leading-none" style={{ fontFamily: SERIF }}>{reach.entryPoints ?? '—'}</p>
                <p className="text-[11px] mt-1 text-zinc-500">{reach.entryPoints == null ? 'no points race' : 'typical points'}</p>
              </div>
            </div>
          )}

          <p className="text-[20px] leading-snug font-semibold mb-2" style={{ fontFamily: SERIF }}>{headline}</p>
          <p className="text-[15px] leading-snug mb-7" style={{ color: wd.onSoft }}>{body}</p>

          <div className="flex justify-between items-center">
            <GhostBack onClick={() => setStep('life')} label="Back to the life" />
            <WorldButton label="Show me the bridge" icon={ArrowRight} onClick={goPlan} wd={wd} />
          </div>
        </Surface>
      </div>
    );
  }

  // ── PLAN (concrete, if-then) ────────────────────────────────────────────
  if (step === 'plan') {
    // Greedy: how many top bargains it takes to clear the current gap.
    let covered = 0; let used = 0;
    for (const b of bargains) { if (covered >= reach.gapFromCurrent) break; covered += b.pointsGain; used++; }
    const closesGap = reach.gapFromCurrent > 0 && covered >= reach.gapFromCurrent;
    return (
      <div className="w-full max-w-xl mx-auto pb-12">
        <button onClick={() => setStep('reality')} className="flex items-center gap-1.5 text-[13px] font-medium text-zinc-500 hover:text-zinc-800 dark:hover:text-zinc-200 mb-4"><ArrowLeft size={15} /> Where you're heading</button>
        <Surface wd={wd}>
          <div className="flex items-center justify-between mb-5">
            <span className="inline-flex items-center gap-1.5 text-[10px] font-bold uppercase tracking-[0.12em] px-2.5 py-1 rounded-full" style={{ backgroundColor: wd.chip, color: '#fff' }}><TrendingUp size={11} /> Your bridge from here to there</span>
            <StepDots step="plan" />
          </div>

          {bargains.length > 0 ? (
            <>
              <Label>What one grade of effort is worth</Label>
              <div className="space-y-2 mb-3">
                {bargains.slice(0, 4).map((b, i) => (
                  <MotionDiv key={`${b.subjectName}-${i}`} className="flex items-center gap-3 rounded-xl p-3" style={{ backgroundColor: '#fff', color: '#1a1a1a' }} initial={{ opacity: 0, x: -10 }} animate={{ opacity: 1, x: 0 }} transition={{ delay: 0.06 + i * 0.08 }}>
                    <span className="w-9 h-9 rounded-full flex items-center justify-center shrink-0 text-[13px] font-bold" style={{ backgroundColor: wd.bg, color: '#fff' }}>+{b.pointsGain}</span>
                    <span className="min-w-0 flex-1">
                      <span className="block text-[13.5px] font-semibold leading-tight">{b.subjectName}: {b.fromGrade} → {b.toGrade}</span>
                      <span className="block text-[11.5px] text-zinc-500">{b.effortHint}{b.isMathsBonus ? ' · unlocks the HL Maths bonus' : ''}</span>
                    </span>
                  </MotionDiv>
                ))}
              </div>
              {reach.gapFromCurrent > 0 ? (
                <p className="text-[13.5px] leading-snug mb-6" style={{ color: wd.onSoft }}>
                  {closesGap
                    ? <>Just the top {used} of these — about +{covered} points — clears the ~{reach.gapFromCurrent}-point gap into {career.title}. One term's focus, not a miracle.</>
                    : <>Stack these and you close the gap into {career.title} fast. Every grade up is real points in the bank.</>}
                </p>
              ) : (
                <p className="text-[13.5px] leading-snug mb-6" style={{ color: wd.onSoft }}>
                  You're already in reach — these are how you make it safe and keep your options open.
                </p>
              )}
            </>
          ) : (
            <p className="text-[15px] leading-snug mb-6" style={{ color: wd.onSoft }}>
              Set your current and target grades in your subject profile and this fills with the exact moves — what each grade up is worth, in points.
            </p>
          )}

          {/* Self-transcendent "why" — purpose beyond the self (Yeager 2014). */}
          <Label>One thing to hold onto</Label>
          <div className="rounded-2xl p-4 mb-6" style={{ backgroundColor: wd.chip }}>
            <div className="flex items-center gap-2 mb-2"><Heart size={14} style={{ color: '#fff' }} /><p className="text-[13.5px] font-semibold">Who, beyond you, would this matter to?</p></div>
            <textarea
              value={why}
              onChange={(e) => setWhy(e.target.value)}
              onBlur={() => { if (careerId) save({ why }); }}
              placeholder="Who could this help? Why does it matter to you?"
              rows={2}
              className="w-full rounded-xl p-3 text-[13.5px] resize-none outline-none"
              style={{ backgroundColor: '#fff', color: '#1a1a1a' }}
            />
          </div>

          <div className="flex justify-between items-center">
            <GhostBack onClick={() => setStep('reality')} label="Back" />
            <WorldButton label="See your possibilities" icon={Sparkles} onClick={goSteer} wd={wd} />
          </div>
        </Surface>
      </div>
    );
  }

  // ── STEER (possibilities, malleable) ────────────────────────────────────
  return (
    <div className="w-full max-w-xl mx-auto pb-12">
      <button onClick={() => setStep('plan')} className="flex items-center gap-1.5 text-[13px] font-medium text-zinc-500 hover:text-zinc-800 dark:hover:text-zinc-200 mb-4"><ArrowLeft size={15} /> The plan</button>
      <Surface wd={wd}>
        {burst && <Celebration colors={['#ffffff', wd.glow]} />}
        <div className="flex items-center justify-between mb-5">
          <span className="inline-flex items-center gap-1.5 text-[10px] font-bold uppercase tracking-[0.12em] px-2.5 py-1 rounded-full" style={{ backgroundColor: wd.chip, color: '#fff' }}><Sparkles size={11} /> Steer it</span>
          <StepDots step="steer" />
        </div>

        <p className="text-[20px] leading-snug font-semibold mb-2" style={{ fontFamily: SERIF }}>These are possibilities, not predictions.</p>
        <p className="text-[15px] leading-snug mb-5" style={{ color: wd.onSoft }}>
          Move the dials and watch other lives come into view. As {career.title}, {region === 'dublin' ? 'in Dublin' : region === 'city' ? 'in a city' : 'in a town'}, {horizon === 'start' ? 'starting out' : 'a few years in'} — that's <span className="font-semibold" style={{ color: '#fff' }}>{life.tier.toLowerCase()}</span>.
        </p>

        <Label>What becomes possible if…</Label>
        <div className="space-y-3 mb-6">
          <div className="rounded-2xl p-3.5" style={{ backgroundColor: wd.chip }}>
            <p className="text-[11px] uppercase tracking-[0.1em] font-bold mb-2" style={{ color: wd.onSoft }}>A few years in</p>
            <Segment wd={wd} value={horizon} onChange={(v) => setHorizon(v as 'start' | 'experienced')} options={[{ value: 'start', label: 'Starting out' }, { value: 'experienced', label: 'A few years in' }]} />
          </div>
          <div className="rounded-2xl p-3.5" style={{ backgroundColor: wd.chip }}>
            <p className="text-[11px] uppercase tracking-[0.1em] font-bold mb-2" style={{ color: wd.onSoft }}>Where you live</p>
            <Segment wd={wd} value={region} onChange={(v) => setRegion(v as LifeRegion)} options={LIFE_REGIONS.map((r) => ({ value: r, label: r === 'dublin' ? 'Dublin' : r === 'city' ? 'City' : 'Town' }))} />
          </div>
        </div>

        {matchedCareers.length > 1 && (
          <>
            <Label>A different path</Label>
            <div className="flex flex-wrap gap-1.5 mb-6">
              {matchedCareers.filter((c) => c.id !== career.id).slice(0, 5).map((c) => (
                <button key={c.id} onClick={() => { setCareerId(c.id); setStep('life'); }} className="inline-flex items-center gap-1.5 text-[12.5px] font-medium px-3 py-1.5 rounded-full" style={{ backgroundColor: wd.chip, color: '#fff' }}>
                  <span>{c.emoji}</span> {c.title}
                </button>
              ))}
            </div>
          </>
        )}

        <div className="rounded-2xl p-3.5 mb-6 flex items-start gap-2.5" style={{ backgroundColor: 'rgba(255,255,255,0.12)' }}>
          <GraduationCap size={16} className="mt-0.5 shrink-0" style={{ color: '#fff' }} />
          <p className="text-[12.5px] leading-snug" style={{ color: wd.onSoft }}>A snapshot you author, not a destiny. Bring it to your guidance counsellor — they can help you turn it into next steps.</p>
        </div>

        <div className="flex flex-col sm:flex-row gap-2.5">
          <WorldButton label="Revisit the life" icon={ArrowRight} onClick={() => setStep('life')} wd={wd} />
          <button onClick={() => { reset(); startOver(); }} className="inline-flex items-center gap-1.5 px-5 py-3 rounded-full text-[13.5px] font-semibold" style={{ border: '2px solid rgba(255,255,255,0.5)', color: '#fff' }}>
            <RotateCcw size={15} /> Start over
          </button>
        </div>
      </Surface>
    </div>
  );
};

export default YourPossibleLife;
