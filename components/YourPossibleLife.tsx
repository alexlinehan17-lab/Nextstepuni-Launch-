/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * "Your Possible Life" — connects effort NOW to the LIFE it makes possible
 * (subjects → results → pathways → careers → lifestyle), structured as WOOP
 * (Wish → Reality → Plan), never a lifestyle-fantasy generator. Money is one
 * ingredient shown in support, never a worth-score. "Possibilities, not
 * predictions" — the student steers it.
 *
 * 2026-06-03 hybrid aesthetic: light white cards with a brightened colour HEADER
 * BAND + Lucide line-icon per career, Source Serif titles, orange chunky CTAs —
 * same family as the rest of the app. Uses the shared immersiveDeck/HybridCard
 * primitives so all three decks stay identical.
 *
 * Engine reuse: bestSixPoints (current AND target) · reachBucket via careerReach
 * · CAREERS/matchStrings ↔ CAO_COURSES · computeBargains. Net-new maths lives in
 * effortLifeModel (irishNetPay, lifestyleFromNet).
 */

import React, { useMemo, useState, useEffect, useRef } from 'react';
import {
  ArrowRight, RotateCcw, Star, Home, Car, PiggyBank, Plane,
  Heart, Compass, TrendingUp, Sparkles, GraduationCap,
} from 'lucide-react';
import { CAREERS } from '../careerPathsData';
import { type CareerCard } from '../types/careerPaths';
import {
  WORLDS, CountUp, Celebration, FIELD_WORLD, FIELD_ICON,
  HybridCard, Band, ProgressDots, OrangeBtn, NeutralBtn, Eyebrow, Segment, BackLink,
  SERIF, INK, BODY, MUTED, LABEL, HAIRLINE,
} from './immersiveDeck';
import { CAO_COURSES, type CAOCourse, hydrateCourses } from './futureFinderData';
import { useInnovationData } from '../contexts/InnovationDataContext';
import { useProgress } from '../contexts/ProgressContext';
import { useEffortLifeSim } from '../hooks/useEffortLifeSim';
import { type StudentSubjectProfile, computeBargains, type Bargain } from './subjectData';
import {
  irishNetPay, lifestyleFromNet, bestSixPoints, careerReach,
  LIFE_REGIONS, LIFE_REGION_LABELS, type LifeRegion,
} from './effortLifeModel';

const LANDING = WORLDS.denim;
const euroK = (k: number) => `€${k}k`;

/** Courses that lead to this career — same runtime join as Career Paths. */
const coursesFor = (c: CareerCard): CAOCourse[] =>
  CAO_COURSES.filter((course) => course.careerPaths.some((cp) => c.matchStrings.includes(cp)))
    .sort((a, b) => b.level - a.level || b.typicalPoints - a.typicalPoints)
    .slice(0, 6);

type Step = 'pick' | 'life' | 'reality' | 'plan' | 'steer';
const STEP_ORDER: Step[] = ['pick', 'life', 'reality', 'plan', 'steer'];
const dotsFor = (s: Step) => <ProgressDots total={STEP_ORDER.length} active={STEP_ORDER.indexOf(s)} />;

/** A small tinted, coloured-ink career chip with its field icon. */
const CareerChip: React.FC<{ c: CareerCard; onClick: () => void }> = ({ c, onClick }) => {
  const cw = FIELD_WORLD[c.field];
  const CI = FIELD_ICON[c.field];
  return (
    <button onClick={onClick} className="inline-flex items-center gap-1.5 text-[12.5px] font-semibold px-3 py-1.5 rounded-full transition-transform active:translate-y-0.5" style={{ backgroundColor: cw.tint, color: cw.deep }}>
      <CI size={13} /> {c.title}
    </button>
  );
};

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

  const currentPoints = useMemo(() => bestSixPoints(profile, 'current'), [profile]);
  const targetPoints = useMemo(() => Math.max(bestSixPoints(profile, 'target'), currentPoints), [profile, currentPoints]);
  const hasGrades = currentPoints > 0 || targetPoints > 0;
  const bargains = useMemo<Bargain[]>(() => computeBargains(profile), [profile]);

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

  useEffect(() => {
    if (!simLoaded || !seedRef.current || !careerId) return;
    save({ careerId, region, horizon });
  }, [careerId, region, horizon, simLoaded, save]);

  const career = careerId ? CAREERS.find((c) => c.id === careerId) ?? null : null;
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
          <HybridCard>
            <Band
              wd={wd}
              icon={FIELD_ICON[topMatch.field]}
              eyebrow={<span className="inline-flex items-center gap-1"><Star size={10} /> Your Future Finder match</span>}
              title={topMatch.title}
              subtitle={topMatch.tagline}
              right={dotsFor('pick')}
            />
            <div className="p-6">
              <p className="text-[15.5px] leading-snug mb-6" style={{ color: BODY }}>
                Let's explore the life this could open up — and the bridge from your grades today to get there. A possibility you steer, not a prediction.
              </p>
              {matchedCareers.length > 1 && (
                <>
                  <Eyebrow>Or swap to another of your matches</Eyebrow>
                  <div className="flex flex-wrap gap-1.5 mb-6">
                    {matchedCareers.slice(0, 6).map((c) => <CareerChip key={c.id} c={c} onClick={() => chooseCareer(c.id)} />)}
                  </div>
                </>
              )}
              <div className="flex flex-col sm:flex-row gap-2.5">
                <OrangeBtn label="Explore this life" icon={ArrowRight} onClick={() => chooseCareer(topMatch.id)} />
                <NeutralBtn label="Pick a different career" onClick={() => setShowManual(true)} />
              </div>
            </div>
          </HybridCard>
        ) : (
          <HybridCard>
            <Band wd={LANDING} icon={Compass} eyebrow="Pick a future to explore" title="Your Possible Life" right={dotsFor('pick')} />
            <div className="p-6">
              <h3 className="text-[20px] leading-tight font-semibold mb-2" style={{ fontFamily: SERIF, color: INK }}>Pick a path, and we'll explore the life it could open up.</h3>
              <p className="text-[14.5px] leading-snug mb-5" style={{ color: BODY }}>
                {hasMatches ? 'Choose any career below.' : "Haven't done the Future Finder yet? No problem — choose any career and we'll work out the nitty-gritty."} A possibility you steer, not a prediction.
              </p>
              <div className="grid grid-cols-2 gap-2.5">
                {CAREERS.map((c) => {
                  const cw = FIELD_WORLD[c.field];
                  const CI = FIELD_ICON[c.field];
                  const matched = matchedCareers.some((m) => m.id === c.id);
                  return (
                    <button key={c.id} onClick={() => chooseCareer(c.id)} className="flex items-center gap-2.5 rounded-2xl p-3 text-left transition-transform active:translate-y-0.5" style={{ backgroundColor: '#fff', border: `1.5px solid ${HAIRLINE}`, color: INK }}>
                      <span className="w-9 h-9 rounded-full flex items-center justify-center shrink-0" style={{ backgroundColor: cw.bg }}><CI size={17} color="#fff" /></span>
                      <span className="min-w-0">
                        <span className="block text-[13.5px] font-semibold leading-tight truncate">{c.title}</span>
                        <span className="block text-[11px]" style={{ color: MUTED }}>{euroK(c.salary.startK)} → {euroK(c.salary.experiencedK)}{matched ? ' · ★ match' : ''}</span>
                      </span>
                    </button>
                  );
                })}
              </div>
              {hasMatches && (
                <button onClick={() => setShowManual(false)} className="mt-5 text-[13px] font-medium" style={{ color: MUTED }}>← Back to your match</button>
              )}
            </div>
          </HybridCard>
        )}
      </div>
    );
  }

  if (!career) return null;
  const wd = FIELD_WORLD[career.field];
  const CareerIcon = FIELD_ICON[career.field];
  const grossK = horizon === 'experienced' ? career.salary.experiencedK : career.salary.startK;
  const pay = irishNetPay(grossK * 1000);
  const life = lifestyleFromNet(pay.netMonthly, region);
  const courses = coursesFor(career);
  const reach = careerReach(courses, currentPoints, targetPoints);

  // ── LIFE (Wish / Outcome) ───────────────────────────────────────────────
  if (step === 'life') {
    return (
      <div className="w-full max-w-xl mx-auto pb-12">
        <BackLink onClick={startOver} label="Pick another path" />
        <HybridCard>
          <Band wd={wd} icon={CareerIcon} eyebrow="The life this could open up" title={career.title} right={dotsFor('life')} />
          <div className="p-6">
            <p className="text-[20px] leading-snug font-semibold mb-4" style={{ fontFamily: SERIF, color: INK }}>{life.vignette}</p>

            <div className="flex items-center gap-2 mb-2.5">
              <Segment wd={wd} value={horizon} onChange={(v) => setHorizon(v as 'start' | 'experienced')} options={[{ value: 'start', label: 'Starting out' }, { value: 'experienced', label: 'A few years in' }]} />
            </div>
            <div className="flex items-center gap-2 mb-5 flex-wrap">
              <Segment wd={wd} value={region} onChange={(v) => setRegion(v as LifeRegion)} options={LIFE_REGIONS.map((r) => ({ value: r, label: r === 'dublin' ? 'Dublin' : r === 'city' ? 'City' : 'Town' }))} />
              <span className="text-[11.5px]" style={{ color: MUTED }}>{LIFE_REGION_LABELS[region]}</span>
            </div>

            <div className="rounded-2xl p-4 mb-3" style={{ backgroundColor: wd.tint }}>
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
                      <span className="w-8 h-8 rounded-full flex items-center justify-center shrink-0" style={{ backgroundColor: wd.bg }}><Icon size={15} color="#fff" /></span>
                      <span className="min-w-0">
                        <span className="block text-[14px] font-semibold leading-snug" style={{ color: INK }}>{row.label}</span>
                        {row.sub && <span className="block text-[12px] leading-snug" style={{ color: MUTED }}>{row.sub}</span>}
                      </span>
                    </div>
                  );
                })}
              </div>
              <div className="mt-3.5 pt-3 flex items-center justify-between" style={{ borderTop: `1px solid ${wd.glow}66` }}>
                <span className="text-[11px] uppercase tracking-[0.12em] font-bold" style={{ color: wd.deep }}>{life.tier}</span>
                <span className="text-[13px]" style={{ color: BODY }}>
                  ~<CountUp to={Math.round(pay.netMonthly)} durationMs={700} format={(n) => `€${n.toLocaleString()}`} className="font-semibold" style={{ color: INK }} />/mo take-home
                </span>
              </div>
            </div>

            <p className="text-[12px] leading-snug mb-6" style={{ color: MUTED }}>{life.caveat}</p>
            <div className="flex justify-end"><OrangeBtn label="Where am I heading now?" icon={ArrowRight} onClick={goReality} /></div>
          </div>
        </HybridCard>
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
        <BackLink onClick={() => setStep('life')} label="The life" />
        <HybridCard>
          <Band wd={wd} icon={Compass} eyebrow="Where you're heading now" right={dotsFor('reality')} />
          <div className="p-6">
            {hasGrades && (
              <div className="flex items-stretch gap-3 mb-5">
                <div className="flex-1 rounded-2xl p-3.5 text-center" style={{ backgroundColor: wd.tint }}>
                  <p className="text-[10px] uppercase tracking-[0.12em] font-bold mb-1" style={{ color: wd.deep }}>Your grades now</p>
                  <p className="text-[30px] font-bold leading-none" style={{ fontFamily: SERIF, color: wd.deep }}>{currentPoints}</p>
                  <p className="text-[11px] mt-1" style={{ color: MUTED }}>projected points</p>
                </div>
                <div className="flex items-center"><ArrowRight size={18} style={{ color: MUTED }} /></div>
                <div className="flex-1 rounded-2xl p-3.5 text-center" style={{ backgroundColor: '#fff', border: `1.5px solid ${HAIRLINE}` }}>
                  <p className="text-[10px] uppercase tracking-[0.12em] font-bold mb-1" style={{ color: LABEL }}>Route in</p>
                  <p className="text-[30px] font-bold leading-none" style={{ fontFamily: SERIF, color: INK }}>{reach.entryPoints ?? '—'}</p>
                  <p className="text-[11px] mt-1" style={{ color: MUTED }}>{reach.entryPoints == null ? 'no points race' : 'typical points'}</p>
                </div>
              </div>
            )}
            <p className="text-[20px] leading-snug font-semibold mb-2" style={{ fontFamily: SERIF, color: INK }}>{headline}</p>
            <p className="text-[15px] leading-snug mb-7" style={{ color: BODY }}>{body}</p>
            <div className="flex justify-between items-center">
              <NeutralBtn label="Back" onClick={() => setStep('life')} />
              <OrangeBtn label="Show me the bridge" icon={ArrowRight} onClick={goPlan} />
            </div>
          </div>
        </HybridCard>
      </div>
    );
  }

  // ── PLAN (concrete, if-then) ────────────────────────────────────────────
  if (step === 'plan') {
    let covered = 0; let used = 0;
    for (const b of bargains) { if (covered >= reach.gapFromCurrent) break; covered += b.pointsGain; used++; }
    const closesGap = reach.gapFromCurrent > 0 && covered >= reach.gapFromCurrent;
    return (
      <div className="w-full max-w-xl mx-auto pb-12">
        <BackLink onClick={() => setStep('reality')} label="Where you're heading" />
        <HybridCard>
          <Band wd={wd} icon={TrendingUp} eyebrow="Your bridge from here to there" right={dotsFor('plan')} />
          <div className="p-6">
            {bargains.length > 0 ? (
              <>
                <Eyebrow>What one grade of effort is worth</Eyebrow>
                <div className="space-y-2 mb-3">
                  {bargains.slice(0, 4).map((b, i) => (
                    <div key={`${b.subjectName}-${i}`} className="flex items-center gap-3 rounded-xl p-3" style={{ backgroundColor: '#fff', border: `1.5px solid ${HAIRLINE}` }}>
                      <span className="w-9 h-9 rounded-full flex items-center justify-center shrink-0 text-[13px] font-bold" style={{ backgroundColor: wd.bg, color: '#fff' }}>+{b.pointsGain}</span>
                      <span className="min-w-0 flex-1">
                        <span className="block text-[13.5px] font-semibold leading-tight" style={{ color: INK }}>{b.subjectName}: {b.fromGrade} → {b.toGrade}</span>
                        <span className="block text-[11.5px]" style={{ color: MUTED }}>{b.effortHint}{b.isMathsBonus ? ' · unlocks the HL Maths bonus' : ''}</span>
                      </span>
                    </div>
                  ))}
                </div>
                {reach.gapFromCurrent > 0 ? (
                  <p className="text-[13.5px] leading-snug mb-6" style={{ color: BODY }}>
                    {closesGap
                      ? <>Just the top {used} of these — about +{covered} points — clears the ~{reach.gapFromCurrent}-point gap into {career.title}. One term's focus, not a miracle.</>
                      : <>Stack these and you close the gap into {career.title} fast. Every grade up is real points in the bank.</>}
                  </p>
                ) : (
                  <p className="text-[13.5px] leading-snug mb-6" style={{ color: BODY }}>You're already in reach — these are how you make it safe and keep your options open.</p>
                )}
              </>
            ) : (
              <p className="text-[15px] leading-snug mb-6" style={{ color: BODY }}>Set your current and target grades in your subject profile and this fills with the exact moves — what each grade up is worth, in points.</p>
            )}

            <Eyebrow>One thing to hold onto</Eyebrow>
            <div className="rounded-2xl p-4 mb-6" style={{ backgroundColor: wd.tint }}>
              <div className="flex items-center gap-2 mb-2"><Heart size={14} style={{ color: wd.deep }} /><p className="text-[13.5px] font-semibold" style={{ color: wd.deep }}>Who, beyond you, would this matter to?</p></div>
              <textarea
                value={why}
                onChange={(e) => setWhy(e.target.value)}
                onBlur={() => { if (careerId) save({ why }); }}
                placeholder="Who could this help? Why does it matter to you?"
                rows={2}
                className="w-full rounded-xl p-3 text-[13.5px] resize-none outline-none"
                style={{ backgroundColor: '#fff', color: INK, border: `1.5px solid ${HAIRLINE}` }}
              />
            </div>

            <div className="flex justify-between items-center">
              <NeutralBtn label="Back" onClick={() => setStep('reality')} />
              <OrangeBtn label="See your possibilities" icon={Sparkles} onClick={goSteer} />
            </div>
          </div>
        </HybridCard>
      </div>
    );
  }

  // ── STEER (possibilities, malleable) ────────────────────────────────────
  return (
    <div className="w-full max-w-xl mx-auto pb-12">
      <BackLink onClick={() => setStep('plan')} label="The plan" />
      <HybridCard>
        {burst && <Celebration colors={[wd.bg, wd.glow]} />}
        <Band wd={wd} icon={Sparkles} eyebrow="Steer it" right={dotsFor('steer')} />
        <div className="p-6">
          <p className="text-[20px] leading-snug font-semibold mb-2" style={{ fontFamily: SERIF, color: INK }}>These are possibilities, not predictions.</p>
          <p className="text-[15px] leading-snug mb-5" style={{ color: BODY }}>
            Move the dials and watch other lives come into view. As {career.title}, {region === 'dublin' ? 'in Dublin' : region === 'city' ? 'in a city' : 'in a town'}, {horizon === 'start' ? 'starting out' : 'a few years in'} — that's <span className="font-semibold" style={{ color: wd.deep }}>{life.tier.toLowerCase()}</span>.
          </p>

          <Eyebrow>What becomes possible if…</Eyebrow>
          <div className="space-y-3 mb-6">
            <div className="rounded-2xl p-3.5" style={{ backgroundColor: wd.tint }}>
              <p className="text-[11px] uppercase tracking-[0.1em] font-bold mb-2" style={{ color: wd.deep }}>A few years in</p>
              <Segment wd={wd} value={horizon} onChange={(v) => setHorizon(v as 'start' | 'experienced')} options={[{ value: 'start', label: 'Starting out' }, { value: 'experienced', label: 'A few years in' }]} />
            </div>
            <div className="rounded-2xl p-3.5" style={{ backgroundColor: wd.tint }}>
              <p className="text-[11px] uppercase tracking-[0.1em] font-bold mb-2" style={{ color: wd.deep }}>Where you live</p>
              <Segment wd={wd} value={region} onChange={(v) => setRegion(v as LifeRegion)} options={LIFE_REGIONS.map((r) => ({ value: r, label: r === 'dublin' ? 'Dublin' : r === 'city' ? 'City' : 'Town' }))} />
            </div>
          </div>

          {matchedCareers.length > 1 && (
            <>
              <Eyebrow>A different path</Eyebrow>
              <div className="flex flex-wrap gap-1.5 mb-6">
                {matchedCareers.filter((c) => c.id !== career.id).slice(0, 5).map((c) => <CareerChip key={c.id} c={c} onClick={() => { setCareerId(c.id); setStep('life'); }} />)}
              </div>
            </>
          )}

          <div className="rounded-2xl p-3.5 mb-6 flex items-start gap-2.5" style={{ backgroundColor: wd.tint }}>
            <GraduationCap size={16} className="mt-0.5 shrink-0" style={{ color: wd.deep }} />
            <p className="text-[12.5px] leading-snug" style={{ color: BODY }}>A snapshot you author, not a destiny. Bring it to your guidance counsellor — they can help you turn it into next steps.</p>
          </div>

          <div className="flex flex-col sm:flex-row gap-2.5">
            <OrangeBtn label="Revisit the life" icon={ArrowRight} onClick={() => setStep('life')} />
            <NeutralBtn label="Start over" icon={RotateCcw} onClick={() => { reset(); startOver(); }} />
          </div>
        </div>
      </HybridCard>
    </div>
  );
};

export default YourPossibleLife;
