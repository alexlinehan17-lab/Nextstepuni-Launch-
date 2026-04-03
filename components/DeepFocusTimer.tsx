/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState, useEffect, useRef, useMemo, useCallback } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { MotionButton, MotionDiv } from './Motion';
import {
  Play, Pause, RotateCcw, SkipForward, Sparkles, ChevronDown, ChevronUp,
  BookOpen, Target, Clock, Volume2, VolumeX, CloudRain, Waves, Wind, Flame, Headphones,
} from 'lucide-react';
import {
  type StudentSubjectProfile, type StudyBlock, type TimetableCompletions,
  DAYS_OF_WEEK, getBlockId, toDateKey,
} from './subjectData';
import {
  computeSubjectPriorities, allocateSessions, generateWeeklyTimetable,
  computeWeeksUntilExam,
} from './timetableAlgorithm';

// ─── Types ──────────────────────────────────────────────────────────────────

type TimerPhase = 'setup' | 'work' | 'break' | 'paused' | 'done';
type AmbientSound = 'none' | 'rain' | 'ocean' | 'lofi' | 'fireplace' | 'wind';

interface DeepFocusTimerProps {
  profile?: StudentSubjectProfile;
  completions?: TimetableCompletions;
  onToggleCompletion?: (dateKey: string, blockId: string, completed: boolean) => void;
}

// ─── Subject Color Map (literal Tailwind strings for CDN constraint) ────────

const SUBJECT_COLORS: Record<string, { dot: string; bg: string; border: string; text: string }> = {
  'English': { dot: 'bg-blue-500', bg: 'bg-blue-50 dark:bg-blue-900/20', border: 'border-blue-200 dark:border-blue-800/40', text: 'text-blue-700 dark:text-blue-300' },
  'Irish': { dot: 'bg-emerald-500', bg: 'bg-emerald-50 dark:bg-emerald-900/20', border: 'border-emerald-200 dark:border-emerald-800/40', text: 'text-emerald-700 dark:text-emerald-300' },
  'Mathematics': { dot: 'bg-indigo-500', bg: 'bg-indigo-50 dark:bg-indigo-900/20', border: 'border-indigo-200 dark:border-indigo-800/40', text: 'text-indigo-700 dark:text-indigo-300' },
  'French': { dot: 'bg-sky-500', bg: 'bg-sky-50 dark:bg-sky-900/20', border: 'border-sky-200 dark:border-sky-800/40', text: 'text-sky-700 dark:text-sky-300' },
  'German': { dot: 'bg-yellow-500', bg: 'bg-yellow-50 dark:bg-yellow-900/20', border: 'border-yellow-200 dark:border-yellow-800/40', text: 'text-yellow-700 dark:text-yellow-300' },
  'Spanish': { dot: 'bg-orange-500', bg: 'bg-orange-50 dark:bg-orange-900/20', border: 'border-orange-200 dark:border-orange-800/40', text: 'text-orange-700 dark:text-orange-300' },
  'Italian': { dot: 'bg-red-500', bg: 'bg-red-50 dark:bg-red-900/20', border: 'border-red-200 dark:border-red-800/40', text: 'text-red-700 dark:text-red-300' },
  'Japanese': { dot: 'bg-pink-500', bg: 'bg-pink-50 dark:bg-pink-900/20', border: 'border-pink-200 dark:border-pink-800/40', text: 'text-pink-700 dark:text-pink-300' },
  'Physics': { dot: 'bg-cyan-500', bg: 'bg-cyan-50 dark:bg-cyan-900/20', border: 'border-cyan-200 dark:border-cyan-800/40', text: 'text-cyan-700 dark:text-cyan-300' },
  'Chemistry': { dot: 'bg-teal-500', bg: 'bg-teal-50 dark:bg-teal-900/20', border: 'border-teal-200 dark:border-teal-800/40', text: 'text-teal-700 dark:text-teal-300' },
  'Biology': { dot: 'bg-lime-500', bg: 'bg-lime-50 dark:bg-lime-900/20', border: 'border-lime-200 dark:border-lime-800/40', text: 'text-lime-700 dark:text-lime-300' },
  'Applied Maths': { dot: 'bg-violet-500', bg: 'bg-violet-50 dark:bg-violet-900/20', border: 'border-violet-200 dark:border-violet-800/40', text: 'text-violet-700 dark:text-violet-300' },
  'Computer Science': { dot: 'bg-fuchsia-500', bg: 'bg-fuchsia-50 dark:bg-fuchsia-900/20', border: 'border-fuchsia-200 dark:border-fuchsia-800/40', text: 'text-fuchsia-700 dark:text-fuchsia-300' },
  'Ag Science': { dot: 'bg-green-500', bg: 'bg-green-50 dark:bg-green-900/20', border: 'border-green-200 dark:border-green-800/40', text: 'text-green-700 dark:text-green-300' },
  'Accounting': { dot: 'bg-amber-500', bg: 'bg-amber-50 dark:bg-amber-900/20', border: 'border-amber-200 dark:border-amber-800/40', text: 'text-amber-700 dark:text-amber-300' },
  'Business': { dot: 'bg-amber-600', bg: 'bg-amber-50 dark:bg-amber-900/20', border: 'border-amber-200 dark:border-amber-800/40', text: 'text-amber-700 dark:text-amber-300' },
  'Economics': { dot: 'bg-yellow-600', bg: 'bg-yellow-50 dark:bg-yellow-900/20', border: 'border-yellow-200 dark:border-yellow-800/40', text: 'text-yellow-700 dark:text-yellow-300' },
  'History': { dot: 'bg-purple-500', bg: 'bg-purple-50 dark:bg-purple-900/20', border: 'border-purple-200 dark:border-purple-800/40', text: 'text-purple-700 dark:text-purple-300' },
  'Geography': { dot: 'bg-emerald-600', bg: 'bg-emerald-50 dark:bg-emerald-900/20', border: 'border-emerald-200 dark:border-emerald-800/40', text: 'text-emerald-700 dark:text-emerald-300' },
  'Politics & Society': { dot: 'bg-rose-500', bg: 'bg-rose-50 dark:bg-rose-900/20', border: 'border-rose-200 dark:border-rose-800/40', text: 'text-rose-700 dark:text-rose-300' },
  'Religious Education': { dot: 'bg-zinc-500', bg: 'bg-zinc-50 dark:bg-zinc-800/40', border: 'border-zinc-200 dark:border-zinc-700/40', text: 'text-zinc-700 dark:text-zinc-300' },
  'Classical Studies': { dot: 'bg-stone-500', bg: 'bg-stone-50 dark:bg-stone-800/40', border: 'border-stone-200 dark:border-stone-700/40', text: 'text-stone-700 dark:text-stone-300' },
  'Home Economics': { dot: 'bg-orange-400', bg: 'bg-orange-50 dark:bg-orange-900/20', border: 'border-orange-200 dark:border-orange-800/40', text: 'text-orange-700 dark:text-orange-300' },
  'Construction Studies': { dot: 'bg-slate-500', bg: 'bg-slate-50 dark:bg-slate-800/40', border: 'border-slate-200 dark:border-slate-700/40', text: 'text-slate-700 dark:text-slate-300' },
  'Engineering': { dot: 'bg-gray-500', bg: 'bg-gray-50 dark:bg-gray-800/40', border: 'border-gray-200 dark:border-gray-700/40', text: 'text-gray-700 dark:text-gray-300' },
  'DCG': { dot: 'bg-neutral-500', bg: 'bg-neutral-50 dark:bg-neutral-800/40', border: 'border-neutral-200 dark:border-neutral-700/40', text: 'text-neutral-700 dark:text-neutral-300' },
  'Technology': { dot: 'bg-blue-600', bg: 'bg-blue-50 dark:bg-blue-900/20', border: 'border-blue-200 dark:border-blue-800/40', text: 'text-blue-700 dark:text-blue-300' },
  'Art': { dot: 'bg-rose-400', bg: 'bg-rose-50 dark:bg-rose-900/20', border: 'border-rose-200 dark:border-rose-800/40', text: 'text-rose-700 dark:text-rose-300' },
  'Music': { dot: 'bg-pink-400', bg: 'bg-pink-50 dark:bg-pink-900/20', border: 'border-pink-200 dark:border-pink-800/40', text: 'text-pink-700 dark:text-pink-300' },
  'Design & Communication Graphics': { dot: 'bg-indigo-400', bg: 'bg-indigo-50 dark:bg-indigo-900/20', border: 'border-indigo-200 dark:border-indigo-800/40', text: 'text-indigo-700 dark:text-indigo-300' },
};

const DEFAULT_COLOR = { dot: 'bg-zinc-500', bg: 'bg-zinc-50 dark:bg-zinc-800/40', border: 'border-zinc-200 dark:border-zinc-700/40', text: 'text-zinc-700 dark:text-zinc-300' };

function getSubjectColor(name: string) {
  return SUBJECT_COLORS[name] || DEFAULT_COLOR;
}

// ─── Subject SVG Stroke Colors (literal strings for CDN) ────────────────────

const SUBJECT_STROKE_COLORS: Record<string, string> = {
  'English': 'stroke-blue-500',
  'Irish': 'stroke-emerald-500',
  'Mathematics': 'stroke-indigo-500',
  'French': 'stroke-sky-500',
  'German': 'stroke-yellow-500',
  'Spanish': 'stroke-orange-500',
  'Italian': 'stroke-red-500',
  'Japanese': 'stroke-pink-500',
  'Physics': 'stroke-cyan-500',
  'Chemistry': 'stroke-teal-500',
  'Biology': 'stroke-lime-500',
  'Applied Maths': 'stroke-violet-500',
  'Computer Science': 'stroke-fuchsia-500',
  'Ag Science': 'stroke-green-500',
  'Accounting': 'stroke-amber-500',
  'Business': 'stroke-amber-600',
  'Economics': 'stroke-yellow-600',
  'History': 'stroke-purple-500',
  'Geography': 'stroke-emerald-600',
  'Politics & Society': 'stroke-rose-500',
  'Religious Education': 'stroke-zinc-500',
  'Classical Studies': 'stroke-stone-500',
  'Home Economics': 'stroke-orange-400',
  'Construction Studies': 'stroke-slate-500',
  'Engineering': 'stroke-gray-500',
  'DCG': 'stroke-neutral-500',
  'Technology': 'stroke-blue-600',
  'Art': 'stroke-rose-400',
  'Music': 'stroke-pink-400',
  'Design & Communication Graphics': 'stroke-indigo-400',
};

function getSubjectStroke(name: string): string {
  return SUBJECT_STROKE_COLORS[name] || 'stroke-purple-500';
}

// ─── Session Type Config ────────────────────────────────────────────────────

const SESSION_TYPE_CONFIG: Record<StudyBlock['sessionType'], { icon: React.ElementType; label: string }> = {
  'new-learning': { icon: BookOpen, label: 'Learn' },
  'practice': { icon: Target, label: 'Practice' },
  'revision': { icon: RotateCcw, label: 'Revise' },
};

// ─── Motivational Quotes ────────────────────────────────────────────────────

const MOTIVATIONAL_QUOTES = [
  'Deep focus is a superpower. You\'re building it right now.',
  'Every minute of focused study compounds over time.',
  'Distraction is the enemy. You chose differently.',
  'Your future self will thank you for this session.',
  'Flow state incoming. Stay with it.',
  'You don\'t have to be perfect. Just present.',
  'Small consistent effort beats sporadic cramming.',
  'This is the work that separates you from the crowd.',
];

// ─── Ambient Sound Engine (Web Audio API) ───────────────────────────────────

// Cleanup helper — each sound returns a dispose callback
type AmbientDispose = () => void;

function createAmbientSound(ctx: AudioContext, type: AmbientSound): AmbientDispose | null {
  if (type === 'none') return null;

  // Collector for all nodes to disconnect on dispose
  const nodes: { stop?: () => void; disconnect: () => void }[] = [];
  const dispose = () => { for (const n of nodes) { try { n.stop?.(); } catch {} try { n.disconnect(); } catch {} } };

  // Helper: create a brown noise ScriptProcessor
  const makeBrownNoise = () => {
    const proc = ctx.createScriptProcessor(4096, 1, 1);
    let last = 0;
    proc.onaudioprocess = (e) => {
      const out = e.outputBuffer.getChannelData(0);
      for (let i = 0; i < 4096; i++) {
        last = (last + 0.02 * (Math.random() * 2 - 1)) / 1.02;
        out[i] = last * 3.5;
      }
    };
    nodes.push(proc);
    return proc;
  };

  // Helper: create + start an oscillator
  const makeOsc = (freq: number, oscType: OscillatorType = 'sine') => {
    const osc = ctx.createOscillator();
    osc.type = oscType;
    osc.frequency.value = freq;
    osc.start();
    nodes.push(osc);
    return osc;
  };

  // Helper: create a gain node
  const makeGain = (value: number) => {
    const g = ctx.createGain();
    g.gain.value = value;
    nodes.push(g);
    return g;
  };

  // Helper: create a filter
  const makeFilter = (filterType: BiquadFilterType, freq: number, q?: number) => {
    const f = ctx.createBiquadFilter();
    f.type = filterType;
    f.frequency.value = freq;
    if (q !== undefined) f.Q.value = q;
    nodes.push(f);
    return f;
  };

  if (type === 'rain') {
    // Brown noise → lowpass 800Hz — the one that works
    const noise = makeBrownNoise();
    const lp = makeFilter('lowpass', 800);
    const gain = makeGain(0.3);
    noise.connect(lp);
    lp.connect(gain);
    gain.connect(ctx.destination);
    return dispose;
  }

  if (type === 'ocean') {
    // Brown noise with dramatic wave swells via dual LFOs
    const noise = makeBrownNoise();
    const lp = makeFilter('lowpass', 400);
    const volumeNode = makeGain(0.5);

    // Slow swell LFO on volume (0.06Hz ≈ 17s wave cycle)
    const swellLfo = makeOsc(0.06);
    const swellDepth = makeGain(0.45);
    swellLfo.connect(swellDepth);
    swellDepth.connect(volumeNode.gain); // modulates 0.5 ± 0.45 → range 0.05–0.95

    // Filter sweep LFO — waves get brighter as they crest
    const filterLfo = makeOsc(0.06);
    const filterDepth = makeGain(300);
    filterLfo.connect(filterDepth);
    filterDepth.connect(lp.frequency); // sweeps 400 ± 300 → range 100–700Hz

    const master = makeGain(0.35);
    noise.connect(lp);
    lp.connect(volumeNode);
    volumeNode.connect(master);
    master.connect(ctx.destination);
    return dispose;
  }

  if (type === 'lofi') {
    // Warm ambient pad: layered oscillators forming a chord, slow evolution, subtle noise texture
    // Cmaj7 chord voiced low: C3, E3, G3, B3 — gentle, jazzy, warm
    const chordFreqs = [130.81, 164.81, 196.00, 246.94];
    const master = makeGain(0.10);

    for (let i = 0; i < chordFreqs.length; i++) {
      const osc = makeOsc(chordFreqs[i], 'sine');
      const oscGain = makeGain(0.12);
      const oscFilter = makeFilter('lowpass', 600 - i * 80);

      // Each oscillator gets a slow detune wobble for movement (different rate per voice)
      const wobble = makeOsc(0.05 + i * 0.03);
      const wobbleDepth = makeGain(1.5 + i * 0.5); // ±1.5 to ±3 cents of frequency wobble
      wobble.connect(wobbleDepth);
      wobbleDepth.connect(osc.frequency);

      osc.connect(oscFilter);
      oscFilter.connect(oscGain);
      oscGain.connect(master);
    }

    // Subtle brown noise bed through heavy lowpass for tape-like warmth
    const noise = makeBrownNoise();
    const noiseLp = makeFilter('lowpass', 200, 1);
    const noiseGain = makeGain(0.03);
    noise.connect(noiseLp);
    noiseLp.connect(noiseGain);
    noiseGain.connect(master);

    // Vinyl crackle — sparse pops for character
    const crackle = ctx.createScriptProcessor(4096, 1, 1);
    nodes.push(crackle);
    crackle.onaudioprocess = (e) => {
      const out = e.outputBuffer.getChannelData(0);
      for (let i = 0; i < 4096; i++) {
        out[i] = Math.random() < 0.001 ? (Math.random() * 0.3) : 0;
      }
    };
    const crackleHp = makeFilter('highpass', 4000);
    const crackleGain = makeGain(0.08);
    crackle.connect(crackleHp);
    crackleHp.connect(crackleGain);
    crackleGain.connect(master);

    master.connect(ctx.destination);
    return dispose;
  }

  if (type === 'fireplace') {
    // Warm low drone oscillator + heavy crackle layer
    const master = makeGain(0.25);

    // Warm base: low triangle oscillator for hearth rumble (not noise-based)
    const baseOsc = makeOsc(55, 'triangle'); // A1
    const baseOsc2 = makeOsc(82.4, 'triangle'); // E2 (fifth)
    const baseGain = makeGain(0.08);
    const baseLp = makeFilter('lowpass', 120);
    // Slow amplitude modulation on base for organic feel
    const baseLfo = makeOsc(0.1);
    const baseLfoDepth = makeGain(0.03);
    baseLfo.connect(baseLfoDepth);
    baseLfoDepth.connect(baseGain.gain);
    baseOsc.connect(baseLp);
    baseOsc2.connect(baseLp);
    baseLp.connect(baseGain);
    baseGain.connect(master);

    // Crackle layer — use ScriptProcessor with dense, varied burst envelopes
    const crackle = ctx.createScriptProcessor(2048, 1, 1);
    nodes.push(crackle);
    let env1 = 0, env2 = 0, env3 = 0;
    crackle.onaudioprocess = (e) => {
      const out = e.outputBuffer.getChannelData(0);
      for (let i = 0; i < 2048; i++) {
        // Three independent envelope generators at different rates/decays
        if (Math.random() < 0.008) env1 = 0.5 + Math.random() * 0.5; // frequent small crackles
        if (Math.random() < 0.002) env2 = 0.7 + Math.random() * 0.3; // medium crackles
        if (Math.random() < 0.0004) env3 = 1.0; // rare loud pops
        env1 *= 0.995;
        env2 *= 0.992;
        env3 *= 0.998;
        const noise = Math.random() * 2 - 1;
        out[i] = noise * (env1 * 0.3 + env2 * 0.5 + env3 * 0.8);
      }
    };
    // Filter crackle to sound more natural — boost the mid-highs
    const crackleHp = makeFilter('highpass', 1500);
    const cracklePeak = makeFilter('peaking', 3500);
    cracklePeak.gain.value = 8;
    const crackleGain = makeGain(0.5);
    crackle.connect(crackleHp);
    crackleHp.connect(cracklePeak);
    cracklePeak.connect(crackleGain);
    crackleGain.connect(master);

    master.connect(ctx.destination);
    return dispose;
  }

  if (type === 'wind') {
    // Brown noise with a VERY slow bandpass sweep — howling/whooshing wind
    const noise = makeBrownNoise();
    const bp = makeFilter('bandpass', 500, 0.6);
    const gain = makeGain(0.3);

    // Very slow LFO sweeps the bandpass center frequency between 150–2500Hz
    const sweepLfo = makeOsc(0.04); // 25s cycle
    const sweepDepth = makeGain(1100);
    sweepLfo.connect(sweepDepth);
    sweepDepth.connect(bp.frequency); // 500 ± 1100 → clamped naturally by filter

    // Second noise layer at higher register for whistling
    const noise2 = makeBrownNoise();
    const hp = makeFilter('highpass', 2000);
    const whistleGain = makeGain(0.06);
    const whistleLfo = makeOsc(0.07); // different speed for variation
    const whistleDepth = makeGain(800);
    whistleLfo.connect(whistleDepth);
    whistleDepth.connect(hp.frequency);
    noise2.connect(hp);
    hp.connect(whistleGain);

    const master = makeGain(0.35);
    noise.connect(bp);
    bp.connect(gain);
    gain.connect(master);
    whistleGain.connect(master);
    master.connect(ctx.destination);
    return dispose;
  }

  return null;
}

function playNotificationDing(ctx: AudioContext) {
  const osc = ctx.createOscillator();
  const gain = ctx.createGain();
  osc.type = 'sine';
  osc.frequency.value = 830;
  gain.gain.setValueAtTime(0.3, ctx.currentTime);
  gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.5);
  osc.connect(gain);
  gain.connect(ctx.destination);
  osc.start(ctx.currentTime);
  osc.stop(ctx.currentTime + 0.5);
}

// ─── Helpers ────────────────────────────────────────────────────────────────

function formatTime(seconds: number): string {
  const m = Math.floor(seconds / 60);
  const s = seconds % 60;
  return `${String(m).padStart(2, '0')}:${String(s).padStart(2, '0')}`;
}

function getTodayDayIndex(): number {
  const jsDay = new Date().getDay(); // 0=Sun
  return jsDay === 0 ? 6 : jsDay - 1; // 0=Mon
}

// ─── Main Component ─────────────────────────────────────────────────────────

const DeepFocusTimer: React.FC<DeepFocusTimerProps> = ({ profile, completions = {}, onToggleCompletion }) => {
  // Timer state
  const [phase, setPhase] = useState<TimerPhase>('setup');
  const [pausedFrom, setPausedFrom] = useState<'work' | 'break' | null>(null);
  const [secondsRemaining, setSecondsRemaining] = useState(0);
  const [totalSeconds, setTotalSeconds] = useState(0);
  const [currentPomodoro, setCurrentPomodoro] = useState(1);
  const [totalPomodoros, setTotalPomodoros] = useState(4);
  const [totalWorkSecondsLogged, setTotalWorkSecondsLogged] = useState(0);

  // Session config
  const [workMinutes, setWorkMinutes] = useState(25);
  const [breakMinutes, setBreakMinutes] = useState(5);
  const [activeSubject, setActiveSubject] = useState<string>('General');
  const [activeSessionType, setActiveSessionType] = useState<StudyBlock['sessionType']>('new-learning');
  const [timetableBlockId, setTimetableBlockId] = useState<string | null>(null);
  const [timetableDateKey, setTimetableDateKey] = useState<string | null>(null);

  // Ambient sound
  const [ambientSound, setAmbientSound] = useState<AmbientSound>('none');
  const [showAmbient, setShowAmbient] = useState(false);

  // Refs
  const intervalRef = useRef<number | null>(null);
  const expectedEndRef = useRef<number>(0);
  const startTimeRef = useRef<number>(0);
  const audioCtxRef = useRef<AudioContext | null>(null);
  const ambientDisposeRef = useRef<AmbientDispose | null>(null);
  const timetableMarkedRef = useRef(false);

  // ─── Timetable integration ──────────────────────────────────────────────

  const todayBlocks = useMemo(() => {
    if (!profile) return [];
    const weeksUntilExam = computeWeeksUntilExam(profile.examStartDate);
    const priorities = computeSubjectPriorities(profile.subjects);
    const allocs = allocateSessions(priorities, weeksUntilExam);
    const timetable = generateWeeklyTimetable(allocs, weeksUntilExam, 0, profile.restDays || []);
    const todayIdx = getTodayDayIndex();
    const day = timetable[todayIdx];
    if (!day) return [];
    return day.blocks;
  }, [profile]);

  const todayDateKey = useMemo(() => toDateKey(new Date()), []);

  const uncompletedBlocks = useMemo(() => {
    const completedIds = completions[todayDateKey] ?? [];
    return todayBlocks
      .map((block, idx) => ({ block, idx, blockId: getBlockId(block, idx) }))
      .filter(item => !completedIds.includes(item.blockId));
  }, [todayBlocks, completions, todayDateKey]);

  // ─── Audio context management ───────────────────────────────────────────

  const getAudioCtx = useCallback((): AudioContext | null => {
    if (!audioCtxRef.current) {
      try {
        audioCtxRef.current = new AudioContext();
      } catch {
        return null;
      }
    }
    if (audioCtxRef.current.state === 'suspended') {
      audioCtxRef.current.resume().catch(() => {});
    }
    return audioCtxRef.current;
  }, []);

  const stopAmbient = useCallback(() => {
    if (ambientDisposeRef.current) {
      ambientDisposeRef.current();
      ambientDisposeRef.current = null;
    }
  }, []);

  const startAmbient = useCallback((sound: AmbientSound) => {
    stopAmbient();
    if (sound === 'none') return;
    const ctx = getAudioCtx();
    if (!ctx) return;
    const dispose = createAmbientSound(ctx, sound);
    ambientDisposeRef.current = dispose;
  }, [getAudioCtx, stopAmbient]);

  // Toggle ambient and start/stop based on timer phase
  const handleAmbientChange = useCallback((sound: AmbientSound) => {
    setAmbientSound(sound);
    if (phase === 'work' || phase === 'break') {
      startAmbient(sound);
    }
  }, [phase, startAmbient]);

  // ─── Timer mechanics ────────────────────────────────────────────────────

  const clearTimer = useCallback(() => {
    if (intervalRef.current !== null) {
      clearInterval(intervalRef.current);
      intervalRef.current = null;
    }
  }, []);

  const startCountdown = useCallback((seconds: number) => {
    clearTimer();
    const now = Date.now();
    startTimeRef.current = now;
    expectedEndRef.current = now + seconds * 1000;
    setTotalSeconds(seconds);
    setSecondsRemaining(seconds);

    intervalRef.current = window.setInterval(() => {
      const remaining = Math.max(0, Math.round((expectedEndRef.current - Date.now()) / 1000));
      setSecondsRemaining(remaining);
      if (remaining <= 0) {
        clearInterval(intervalRef.current!);
        intervalRef.current = null;
      }
    }, 1000);
  }, [clearTimer]);

  // Handle visibility change for tab throttling correction
  useEffect(() => {
    const handleVisibility = () => {
      if (document.visibilityState === 'visible' && (phase === 'work' || phase === 'break')) {
        const remaining = Math.max(0, Math.round((expectedEndRef.current - Date.now()) / 1000));
        setSecondsRemaining(remaining);
      }
    };
    document.addEventListener('visibilitychange', handleVisibility);
    return () => document.removeEventListener('visibilitychange', handleVisibility);
  }, [phase]);

  // Handle timer reaching 0
  useEffect(() => {
    if (secondsRemaining > 0) return;
    if (phase !== 'work' && phase !== 'break') return;

    clearTimer();

    // Play notification
    const ctx = getAudioCtx();
    if (ctx) playNotificationDing(ctx);

    if (phase === 'work') {
      // Log work time
      setTotalWorkSecondsLogged(prev => prev + totalSeconds);

      // Auto-mark timetable block on first work pomodoro completion
      if (timetableBlockId && timetableDateKey && onToggleCompletion && !timetableMarkedRef.current) {
        timetableMarkedRef.current = true;
        onToggleCompletion(timetableDateKey, timetableBlockId, true);
      }

      if (currentPomodoro >= totalPomodoros) {
        // All pomodoros done
        stopAmbient();
        setPhase('done');
      } else {
        // Start break
        const isLongBreak = currentPomodoro % 4 === 0;
        const breakDuration = isLongBreak ? 15 : breakMinutes;
        setPhase('break');
        startCountdown(breakDuration * 60);
      }
    } else if (phase === 'break') {
      // Start next work session
      setCurrentPomodoro(prev => prev + 1);
      setPhase('work');
      startCountdown(workMinutes * 60);
    }
  }, [secondsRemaining, phase, currentPomodoro, totalPomodoros, workMinutes, breakMinutes,
      totalSeconds, timetableBlockId, timetableDateKey, onToggleCompletion, clearTimer,
      getAudioCtx, startCountdown, stopAmbient]);

  // Start/stop ambient when phase changes
  useEffect(() => {
    if (phase === 'work' || phase === 'break') {
      startAmbient(ambientSound);
    } else {
      stopAmbient();
    }
  }, [phase, ambientSound, startAmbient, stopAmbient]);

  // Cleanup on unmount
  useEffect(() => {
    return () => {
      clearTimer();
      stopAmbient();
      if (audioCtxRef.current) {
        audioCtxRef.current.close().catch(() => {});
        audioCtxRef.current = null;
      }
    };
  }, [clearTimer, stopAmbient]);

  // ─── Actions ────────────────────────────────────────────────────────────

  const handleStartSession = useCallback((subject: string, sessionType: StudyBlock['sessionType'], blockId?: string, dateKey?: string, pomodoroCount?: number) => {
    setActiveSubject(subject);
    setActiveSessionType(sessionType);
    setTimetableBlockId(blockId || null);
    setTimetableDateKey(dateKey || null);
    setCurrentPomodoro(1);
    setTotalPomodoros(pomodoroCount || totalPomodoros);
    setTotalWorkSecondsLogged(0);
    timetableMarkedRef.current = false;
    setPhase('work');
    startCountdown(workMinutes * 60);
  }, [workMinutes, totalPomodoros, startCountdown]);

  const handleQuickStart = useCallback((block: StudyBlock, blockIdx: number) => {
    const blockId = getBlockId(block, blockIdx);
    const pomCount = Math.max(1, Math.round(block.durationMinutes / workMinutes));
    handleStartSession(block.subjectName, block.sessionType, blockId, todayDateKey, pomCount);
  }, [workMinutes, todayDateKey, handleStartSession]);

  const handlePause = useCallback(() => {
    if (phase === 'work' || phase === 'break') {
      clearTimer();
      setPausedFrom(phase);
      setPhase('paused');
      stopAmbient();
    }
  }, [phase, clearTimer, stopAmbient]);

  const handleResume = useCallback(() => {
    if (phase === 'paused' && pausedFrom) {
      setPhase(pausedFrom);
      setPausedFrom(null);
      // Restart with remaining time
      const now = Date.now();
      expectedEndRef.current = now + secondsRemaining * 1000;
      startTimeRef.current = now;

      intervalRef.current = window.setInterval(() => {
        const remaining = Math.max(0, Math.round((expectedEndRef.current - Date.now()) / 1000));
        setSecondsRemaining(remaining);
        if (remaining <= 0) {
          clearInterval(intervalRef.current!);
          intervalRef.current = null;
        }
      }, 1000);
    }
  }, [phase, pausedFrom, secondsRemaining]);

  const handleReset = useCallback(() => {
    clearTimer();
    stopAmbient();
    setPhase('setup');
    setPausedFrom(null);
    setSecondsRemaining(0);
    setTotalSeconds(0);
    setCurrentPomodoro(1);
    setTotalWorkSecondsLogged(0);
    setTimetableBlockId(null);
    setTimetableDateKey(null);
    timetableMarkedRef.current = false;
  }, [clearTimer, stopAmbient]);

  const handleSkipBreak = useCallback(() => {
    if (phase === 'break') {
      clearTimer();
      setCurrentPomodoro(prev => prev + 1);
      setPhase('work');
      startCountdown(workMinutes * 60);
    }
  }, [phase, workMinutes, clearTimer, startCountdown]);

  // ─── Progress ring values ───────────────────────────────────────────────

  const ringRadius = 80;
  const ringCircumference = 2 * Math.PI * ringRadius;
  const ringProgress = totalSeconds > 0 ? secondsRemaining / totalSeconds : 0;
  const ringStroke = phase === 'break' ? 'stroke-emerald-500' : getSubjectStroke(activeSubject);

  // Motivational quote
  const motivationalQuote = MOTIVATIONAL_QUOTES[(currentPomodoro - 1) % MOTIVATIONAL_QUOTES.length];

  // Subject list for custom mode
  const subjectOptions = useMemo(() => {
    const subjects = profile?.subjects?.map(s => s.subjectName) ?? [];
    return ['General', ...subjects];
  }, [profile]);

  // ─── Render ─────────────────────────────────────────────────────────────

  // Ambient sound controls (shared across phases)
  const ambientControls = (
    <div className="mt-4">
      <button
        onClick={() => setShowAmbient(!showAmbient)}
        className="flex items-center gap-2 text-xs font-bold text-zinc-400 dark:text-zinc-500 hover:text-zinc-600 dark:hover:text-zinc-300 transition-colors mx-auto"
      >
        {ambientSound === 'none' ? <VolumeX size={14} /> : <Volume2 size={14} />}
        Ambient Sounds
        {showAmbient ? <ChevronUp size={12} /> : <ChevronDown size={12} />}
      </button>
      <AnimatePresence>
        {showAmbient && (
          <MotionDiv
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            className="overflow-hidden"
          >
            <div className="flex flex-wrap items-center justify-center gap-2 mt-3">
              {([
                { key: 'none' as AmbientSound, icon: VolumeX, label: 'Silent' },
                { key: 'rain' as AmbientSound, icon: CloudRain, label: 'Rain' },
                { key: 'ocean' as AmbientSound, icon: Waves, label: 'Ocean' },
                { key: 'lofi' as AmbientSound, icon: Headphones, label: 'Lo-fi' },
                { key: 'fireplace' as AmbientSound, icon: Flame, label: 'Fire' },
                { key: 'wind' as AmbientSound, icon: Wind, label: 'Wind' },
              ]).map(({ key, icon: Icon, label }) => (
                <button
                  key={key}
                  onClick={() => handleAmbientChange(key)}
                  className={`flex flex-col items-center gap-1 px-3 py-2 rounded-lg border transition-all text-xs font-bold ${
                    ambientSound === key
                      ? 'bg-purple-100 dark:bg-purple-900/30 border-purple-300 dark:border-purple-600 text-purple-600 dark:text-purple-400'
                      : 'bg-white dark:bg-zinc-800 border-zinc-200 dark:border-zinc-700 text-zinc-500 dark:text-zinc-400 hover:border-purple-300 dark:hover:border-purple-600'
                  }`}
                >
                  <Icon size={16} />
                  {label}
                </button>
              ))}
            </div>
          </MotionDiv>
        )}
      </AnimatePresence>
    </div>
  );

  // ─── Setup Phase ────────────────────────────────────────────────────────

  if (phase === 'setup') {
    return (
      <div className="space-y-6">
        <div className="text-center">
          <h2 className="font-serif text-2xl font-semibold text-zinc-900 dark:text-white">Deep Focus Timer</h2>
          <p className="text-sm text-zinc-500 dark:text-zinc-400 mt-1">Pomodoro-style focus sessions tied to your study plan.</p>
        </div>

        {/* Quick Start from timetable */}
        {profile && uncompletedBlocks.length > 0 && (
          <div className="bg-white/50 dark:bg-white/5 backdrop-blur-2xl border border-zinc-200/50 dark:border-white/10 rounded-xl p-5">
            <p className="text-[10px] font-bold uppercase tracking-widest text-zinc-400 dark:text-zinc-500 mb-3">Quick Start — Today's Plan</p>
            <div className="space-y-2">
              {uncompletedBlocks.map(({ block, idx }) => {
                const color = getSubjectColor(block.subjectName);
                const typeConfig = SESSION_TYPE_CONFIG[block.sessionType];
                const TypeIcon = typeConfig.icon;
                return (
                  <MotionButton
                    key={idx}
                    whileHover={{ scale: 1.01 }}
                    whileTap={{ scale: 0.98 }}
                    onClick={() => handleQuickStart(block, idx)}
                    className={`w-full flex items-center gap-3 p-3 rounded-lg border transition-all text-left ${color.bg} ${color.border} hover:shadow-sm`}
                  >
                    <div className={`w-3 h-3 rounded-full ${color.dot} flex-shrink-0`} />
                    <div className="flex-1 min-w-0">
                      <p className={`text-sm font-bold truncate ${color.text}`}>{block.subjectName}</p>
                    </div>
                    <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full bg-white/60 dark:bg-white/10 text-[10px] font-bold text-zinc-600 dark:text-zinc-300">
                      <TypeIcon size={10} />
                      {typeConfig.label}
                    </span>
                    <span className="text-[10px] font-mono text-zinc-400 dark:text-zinc-500">{block.durationMinutes}m</span>
                    <Play size={14} className="text-zinc-400 dark:text-zinc-500 flex-shrink-0" />
                  </MotionButton>
                );
              })}
            </div>
          </div>
        )}

        {/* Custom Session */}
        <div className="bg-white/50 dark:bg-white/5 backdrop-blur-2xl border border-zinc-200/50 dark:border-white/10 rounded-xl p-5 space-y-5">
          <p className="text-[10px] font-bold uppercase tracking-widest text-zinc-400 dark:text-zinc-500">Custom Session</p>

          {/* Subject selector */}
          <div>
            <p className="text-xs font-bold text-zinc-500 dark:text-zinc-400 mb-2">Subject</p>
            <div className="flex flex-wrap gap-1.5">
              {subjectOptions.map(subject => {
                const color = subject === 'General' ? DEFAULT_COLOR : getSubjectColor(subject);
                const isSelected = activeSubject === subject;
                return (
                  <button
                    key={subject}
                    onClick={() => setActiveSubject(subject)}
                    className={`px-3 py-1.5 rounded-full text-xs font-bold transition-all border ${
                      isSelected
                        ? `${color.bg} ${color.border} ${color.text}`
                        : 'bg-white dark:bg-zinc-800 border-zinc-200 dark:border-zinc-700 text-zinc-500 dark:text-zinc-400 hover:border-zinc-300 dark:hover:border-zinc-600'
                    }`}
                  >
                    {subject}
                  </button>
                );
              })}
            </div>
          </div>

          {/* Duration presets */}
          <div>
            <p className="text-xs font-bold text-zinc-500 dark:text-zinc-400 mb-2">Duration</p>
            <div className="flex gap-2">
              {([
                { work: 25, brk: 5, label: '25 / 5' },
                { work: 50, brk: 10, label: '50 / 10' },
              ]).map(preset => {
                const isSelected = workMinutes === preset.work && breakMinutes === preset.brk;
                return (
                  <button
                    key={preset.label}
                    onClick={() => { setWorkMinutes(preset.work); setBreakMinutes(preset.brk); }}
                    className={`flex-1 py-2 rounded-lg text-sm font-bold transition-all border ${
                      isSelected
                        ? 'bg-purple-100 dark:bg-purple-900/30 border-purple-300 dark:border-purple-600 text-purple-600 dark:text-purple-400'
                        : 'bg-white dark:bg-zinc-800 border-zinc-200 dark:border-zinc-700 text-zinc-500 dark:text-zinc-400 hover:border-purple-300 dark:hover:border-purple-600'
                    }`}
                  >
                    {preset.label}
                  </button>
                );
              })}
            </div>
          </div>

          {/* Pomodoro count */}
          <div>
            <p className="text-xs font-bold text-zinc-500 dark:text-zinc-400 mb-2">Pomodoros</p>
            <div className="flex items-center justify-center gap-4">
              <button
                onClick={() => setTotalPomodoros(p => Math.max(1, p - 1))}
                className="w-10 h-10 rounded-lg bg-white dark:bg-zinc-800 border border-zinc-200 dark:border-zinc-700 text-zinc-600 dark:text-zinc-300 font-bold text-lg hover:bg-zinc-100 dark:hover:bg-zinc-700 transition-colors"
              >
                -
              </button>
              <span className="text-2xl font-bold font-mono text-zinc-800 dark:text-zinc-200 w-8 text-center">
                {totalPomodoros}
              </span>
              <button
                onClick={() => setTotalPomodoros(p => Math.min(8, p + 1))}
                className="w-10 h-10 rounded-lg bg-white dark:bg-zinc-800 border border-zinc-200 dark:border-zinc-700 text-zinc-600 dark:text-zinc-300 font-bold text-lg hover:bg-zinc-100 dark:hover:bg-zinc-700 transition-colors"
              >
                +
              </button>
            </div>
            <p className="text-[10px] text-zinc-400 dark:text-zinc-500 text-center mt-1">
              {totalPomodoros * workMinutes}min total focus time
            </p>
          </div>

          {/* Start button */}
          <MotionButton
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            onClick={() => handleStartSession(activeSubject, activeSessionType)}
            className="w-full py-3 rounded-xl bg-zinc-800 dark:bg-white text-white dark:text-zinc-900 font-bold text-sm hover:bg-zinc-700 dark:hover:bg-zinc-100 transition-colors flex items-center justify-center gap-2"
          >
            <Play size={16} />
            Start Focusing
          </MotionButton>
        </div>

        {/* Ambient sounds */}
        {ambientControls}
      </div>
    );
  }

  // ─── Active Timer Phase (work / break / paused) ─────────────────────────

  if (phase === 'work' || phase === 'break' || phase === 'paused') {
    const isWork = phase === 'work' || (phase === 'paused' && pausedFrom === 'work');
    const isLongBreak = !isWork && currentPomodoro % 4 === 0;
    const phaseLabel = isWork ? 'FOCUS' : isLongBreak ? 'LONG BREAK' : 'BREAK';
    const subjectColor = getSubjectColor(activeSubject);
    const TypeIcon = SESSION_TYPE_CONFIG[activeSessionType].icon;

    return (
      <div className="space-y-6">
        {/* Top bar */}
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className={`w-3 h-3 rounded-full ${subjectColor.dot}`} />
            <span className="text-sm font-bold text-zinc-800 dark:text-zinc-200">{activeSubject}</span>
            <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full bg-white/60 dark:bg-white/10 text-[10px] font-bold text-zinc-500 dark:text-zinc-400">
              <TypeIcon size={10} />
              {SESSION_TYPE_CONFIG[activeSessionType].label}
            </span>
          </div>
          <span className="text-xs font-bold font-mono text-zinc-400 dark:text-zinc-500">
            {currentPomodoro} of {totalPomodoros}
          </span>
        </div>

        {/* Phase label */}
        <div className="text-center">
          <span className={`text-[10px] font-bold uppercase tracking-[0.3em] ${
            isWork ? 'text-purple-600 dark:text-purple-400' : 'text-emerald-600 dark:text-emerald-400'
          }`}>
            {phaseLabel}
          </span>
        </div>

        {/* Countdown ring */}
        <div className="flex justify-center">
          <div className="relative w-48 h-48">
            <svg viewBox="0 0 200 200" className="w-48 h-48 -rotate-90">
              <circle cx="100" cy="100" r={ringRadius} fill="none" strokeWidth="6"
                className="stroke-zinc-200 dark:stroke-white/10" />
              <motion.circle
                cx="100" cy="100" r={ringRadius} fill="none" strokeWidth="6"
                strokeLinecap="round"
                className={phase === 'break' ? 'stroke-emerald-500' : (phase === 'paused' && pausedFrom === 'break') ? 'stroke-emerald-500' : ringStroke}
                animate={{ strokeDashoffset: ringCircumference * (1 - ringProgress) }}
                transition={{ duration: 0.3, ease: 'linear' }}
                style={{ strokeDasharray: ringCircumference }}
              />
            </svg>
            <div className="absolute inset-0 flex items-center justify-center">
              {phase === 'paused' ? (
                <MotionDiv
                  animate={{ opacity: [1, 0.3, 1] }}
                  transition={{ duration: 2, repeat: Infinity, ease: 'easeInOut' }}
                >
                  <span className="text-4xl font-bold font-mono text-zinc-800 dark:text-zinc-200">
                    {formatTime(secondsRemaining)}
                  </span>
                </MotionDiv>
              ) : (
                <span className="text-4xl font-bold font-mono text-zinc-800 dark:text-zinc-200">
                  {formatTime(secondsRemaining)}
                </span>
              )}
            </div>
          </div>
        </div>

        {/* Controls */}
        <div className="flex items-center justify-center gap-4">
          {phase === 'paused' ? (
            <MotionButton
              whileHover={{ scale: 1.1 }}
              whileTap={{ scale: 0.9 }}
              onClick={handleResume}
              className="w-14 h-14 rounded-full bg-zinc-800 dark:bg-white text-white dark:text-zinc-900 flex items-center justify-center shadow-lg"
            >
              <Play size={24} />
            </MotionButton>
          ) : (
            <MotionButton
              whileHover={{ scale: 1.1 }}
              whileTap={{ scale: 0.9 }}
              onClick={handlePause}
              className="w-14 h-14 rounded-full bg-zinc-800 dark:bg-white text-white dark:text-zinc-900 flex items-center justify-center shadow-lg"
            >
              <Pause size={24} />
            </MotionButton>
          )}
          <MotionButton
            whileHover={{ scale: 1.1 }}
            whileTap={{ scale: 0.9 }}
            onClick={handleReset}
            className="w-10 h-10 rounded-full bg-zinc-200 dark:bg-zinc-700 text-zinc-600 dark:text-zinc-300 flex items-center justify-center"
          >
            <RotateCcw size={16} />
          </MotionButton>
          {phase === 'break' && (
            <MotionButton
              whileHover={{ scale: 1.1 }}
              whileTap={{ scale: 0.9 }}
              onClick={handleSkipBreak}
              className="w-10 h-10 rounded-full bg-emerald-100 dark:bg-emerald-900/30 text-emerald-600 dark:text-emerald-400 flex items-center justify-center"
              title="Skip break"
            >
              <SkipForward size={16} />
            </MotionButton>
          )}
        </div>

        {/* Motivational quote (work phase only) */}
        {isWork && (
          <p className="text-xs text-zinc-400 dark:text-zinc-500 text-center italic max-w-sm mx-auto">
            {motivationalQuote}
          </p>
        )}

        {/* Ambient sounds */}
        {ambientControls}
      </div>
    );
  }

  // ─── Done Phase ─────────────────────────────────────────────────────────

  if (phase === 'done') {
    const totalMinutes = Math.round(totalWorkSecondsLogged / 60);
    const subjectColor = getSubjectColor(activeSubject);

    return (
      <MotionDiv
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        className="space-y-6"
      >
        {/* Celebration */}
        <div className="bg-white/50 dark:bg-white/5 backdrop-blur-2xl border border-zinc-200/50 dark:border-white/10 rounded-xl p-8 text-center">
          <MotionDiv
            initial={{ scale: 0 }}
            animate={{ scale: 1 }}
            transition={{ type: 'spring', stiffness: 300, damping: 20, delay: 0.1 }}
            className="w-16 h-16 rounded-2xl bg-amber-100 dark:bg-amber-900/30 flex items-center justify-center mx-auto mb-4"
          >
            <Sparkles size={32} className="text-amber-500" />
          </MotionDiv>
          <h3 className="font-serif text-2xl font-semibold text-zinc-900 dark:text-white mb-2">Session Complete!</h3>
          <p className="text-sm text-zinc-500 dark:text-zinc-400">Great work staying focused.</p>
        </div>

        {/* Stats */}
        <div className="grid grid-cols-2 gap-3">
          <div className="bg-white/50 dark:bg-white/5 border border-zinc-200/50 dark:border-white/10 rounded-xl p-4 text-center">
            <Clock size={16} className="text-purple-500 mx-auto mb-1" />
            <p className="text-2xl font-bold font-mono text-zinc-800 dark:text-zinc-200">{totalMinutes}</p>
            <p className="text-[10px] font-bold text-zinc-400 dark:text-zinc-500 uppercase tracking-wider">Minutes Focused</p>
          </div>
          <div className="bg-white/50 dark:bg-white/5 border border-zinc-200/50 dark:border-white/10 rounded-xl p-4 text-center">
            <Target size={16} className="text-emerald-500 mx-auto mb-1" />
            <p className="text-2xl font-bold font-mono text-zinc-800 dark:text-zinc-200">{currentPomodoro}</p>
            <p className="text-[10px] font-bold text-zinc-400 dark:text-zinc-500 uppercase tracking-wider">Pomodoros</p>
          </div>
          <div className="bg-white/50 dark:bg-white/5 border border-zinc-200/50 dark:border-white/10 rounded-xl p-4 text-center">
            <div className={`w-3 h-3 rounded-full ${subjectColor.dot} mx-auto mb-1`} />
            <p className="text-sm font-bold text-zinc-800 dark:text-zinc-200 truncate">{activeSubject}</p>
            <p className="text-[10px] font-bold text-zinc-400 dark:text-zinc-500 uppercase tracking-wider">Subject</p>
          </div>
          <div className="bg-white/50 dark:bg-white/5 border border-zinc-200/50 dark:border-white/10 rounded-xl p-4 text-center">
            {(() => { const TypeIcon = SESSION_TYPE_CONFIG[activeSessionType].icon; return <TypeIcon size={16} className="text-blue-500 mx-auto mb-1" />; })()}
            <p className="text-sm font-bold text-zinc-800 dark:text-zinc-200">{SESSION_TYPE_CONFIG[activeSessionType].label}</p>
            <p className="text-[10px] font-bold text-zinc-400 dark:text-zinc-500 uppercase tracking-wider">Session Type</p>
          </div>
        </div>

        {/* Timetable badge */}
        {timetableMarkedRef.current && (
          <div className="flex items-center justify-center gap-2 px-4 py-2.5 rounded-xl bg-emerald-50 dark:bg-emerald-900/20 border border-emerald-200 dark:border-emerald-800/40">
            <Sparkles size={14} className="text-emerald-500 flex-shrink-0" />
            <p className="text-xs font-bold text-emerald-600 dark:text-emerald-400">Marked complete on your timetable</p>
          </div>
        )}

        {/* Start Another */}
        <div className="text-center">
          <MotionButton
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={handleReset}
            className="inline-flex items-center gap-2 px-6 py-3 bg-zinc-800 dark:bg-white text-white dark:text-zinc-900 font-bold text-sm rounded-full shadow-lg hover:bg-zinc-700 dark:hover:bg-zinc-100 transition-colors"
          >
            Start Another <RotateCcw size={16} />
          </MotionButton>
        </div>
      </MotionDiv>
    );
  }

  return null;
};

export default DeepFocusTimer;
