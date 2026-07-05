/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Paper Trail — focus session (feature E7). Pick a length, start a calm timer,
 * and watch a procedural plant grow with your focus. Finish it and the plant
 * joins your grove — effort made visible, no points chase. Quitting early simply
 * doesn't plant it. A completed session also counts toward the practice streak.
 */

import React, { useEffect, useRef, useState } from 'react';
import { ArrowLeft, X } from 'lucide-react';
import { drawPlant } from './focusArt';
import { addSession, focusStats, loadGrove, type FocusRecord } from './focusStore';
import { recordActivity } from './streakStore';

const INK = '#1a1a1a';
const ACCENT = '#F26B1F';
const DURATIONS = [15, 25, 45];

const PlantThumb: React.FC<{ seed: number; minutes: number }> = ({ seed, minutes }) => {
  const ref = useRef<HTMLCanvasElement | null>(null);
  useEffect(() => {
    const c = ref.current;
    const ctx = c?.getContext('2d');
    if (c && ctx) {
      c.width = c.offsetWidth;
      c.height = c.offsetHeight;
      drawPlant(ctx, c.width, c.height, 1, seed);
    }
  }, [seed]);
  return (
    <div className="rounded-xl border-2 border-[#d0cdc8] dark:border-zinc-700 bg-white dark:bg-zinc-900 p-1.5 text-center">
      <canvas ref={ref} className="w-full h-[72px]" aria-hidden />
      <span className="block text-[10.5px] font-semibold tabular-nums" style={{ color: '#7a7068' }}>{minutes}m</span>
    </div>
  );
};

interface Props {
  uid?: string;
  onBack: () => void;
}

const FocusSession: React.FC<Props> = ({ uid, onBack }) => {
  const [mode, setMode] = useState<'setup' | 'running' | 'done'>('setup');
  const [minutes, setMinutes] = useState(25);
  const [startTs, setStartTs] = useState(0);
  const [elapsed, setElapsed] = useState(0);
  const [seed, setSeed] = useState(1);
  const [grove, setGrove] = useState<FocusRecord[]>(() => loadGrove(uid));
  const canvasRef = useRef<HTMLCanvasElement | null>(null);

  const durationMs = minutes * 60_000;
  const progress = mode === 'running' ? Math.min(1, elapsed / durationMs) : 0;

  // Tick while running.
  useEffect(() => {
    if (mode !== 'running') return;
    const id = setInterval(() => setElapsed(Date.now() - startTs), 250);
    return () => clearInterval(id);
  }, [mode, startTs]);

  // Complete when the time is up.
  useEffect(() => {
    if (mode === 'running' && elapsed >= durationMs) {
      addSession(uid, minutes, seed, Date.now());
      recordActivity(uid, Date.now(), 1);
      setGrove(loadGrove(uid));
      setMode('done');
    }
  }, [mode, elapsed, durationMs, minutes, seed, uid]);

  // Redraw the growing plant.
  useEffect(() => {
    if (mode !== 'running' && mode !== 'done') return;
    const c = canvasRef.current;
    const ctx = c?.getContext('2d');
    if (c && ctx) {
      c.width = c.offsetWidth;
      c.height = c.offsetHeight;
      drawPlant(ctx, c.width, c.height, mode === 'done' ? 1 : progress, seed);
    }
  }, [mode, progress, seed]);

  const start = () => {
    setSeed(Math.floor(Math.random() * 1e9) + 1);
    setStartTs(Date.now());
    setElapsed(0);
    setMode('running');
  };
  const giveUp = () => { setMode('setup'); setElapsed(0); };

  const stats = focusStats(uid, Date.now());
  const remainingMs = Math.max(0, durationMs - elapsed);
  const mm = Math.floor(remainingMs / 60_000);
  const ss = Math.floor((remainingMs % 60_000) / 1000);

  // ── Running / done ──
  if (mode === 'running' || mode === 'done') {
    return (
      <div className="w-full max-w-md mx-auto pb-12 text-center">
        {mode === 'running' ? (
          <button onClick={giveUp} className="flex items-center gap-1.5 text-[13px] font-medium mb-6 mx-auto" style={{ color: '#9e9186' }}>
            <X size={15} /> Give up
          </button>
        ) : (
          <div className="h-6 mb-6" />
        )}
        <canvas ref={canvasRef} className="w-full h-[300px]" aria-hidden />
        {mode === 'running' ? (
          <>
            <p className="text-[44px] font-bold tabular-nums leading-none mt-4" style={{ fontFamily: "'Source Serif 4', serif", color: INK }}>
              {mm}:{String(ss).padStart(2, '0')}
            </p>
            <p className="text-[13px] mt-2" style={{ color: '#7a7068' }}>Stay with it — the plant grows while you focus.</p>
          </>
        ) : (
          <>
            <h2 className="text-2xl font-semibold mt-4 mb-1" style={{ fontFamily: "'Source Serif 4', serif", color: '#1F5F3E' }}>Planted</h2>
            <p className="text-[14px] mb-6" style={{ color: '#5a5550' }}>{minutes} focused minutes added to your grove.</p>
            <button onClick={() => setMode('setup')} className="rounded-full px-6 py-2.5 text-[14px] font-semibold text-white transition-transform active:translate-y-0.5" style={{ backgroundColor: ACCENT, boxShadow: '0 3px 0 #B54D14' }}>
              Done
            </button>
          </>
        )}
      </div>
    );
  }

  // ── Setup ──
  return (
    <div className="w-full max-w-xl mx-auto pb-12">
      <button onClick={onBack} className="flex items-center gap-1.5 text-[13px] font-medium mb-4" style={{ color: '#7a7068' }}>
        <ArrowLeft size={15} /> Paper Trail
      </button>
      <h2 className="text-2xl font-semibold mb-1" style={{ fontFamily: "'Source Serif 4', serif", color: INK }}>Focus session</h2>
      <p className="text-[13.5px] leading-relaxed mb-5" style={{ color: '#5a5550' }}>
        Put the phone down and focus. A plant grows while you work and joins your grove when you finish — {stats.sessions > 0 ? `${stats.todayMinutes}m today, ${stats.totalMinutes}m in all.` : 'no streak pressure, just quiet progress.'}
      </p>

      <h3 className="text-[11px] font-bold uppercase tracking-[0.12em] mb-2" style={{ color: '#9e9186' }}>How long?</h3>
      <div className="flex gap-2 mb-5">
        {DURATIONS.map(d => (
          <button
            key={d}
            aria-pressed={minutes === d}
            onClick={() => setMinutes(d)}
            className="flex-1 py-3 rounded-xl border-2 text-[15px] font-bold transition-colors"
            style={minutes === d ? { backgroundColor: ACCENT, borderColor: ACCENT, color: '#fff' } : { backgroundColor: '#fff', borderColor: '#d0cdc8', color: '#7a7068' }}
          >
            {d}<span className="text-[11px] font-medium ml-0.5">min</span>
          </button>
        ))}
      </div>

      <button onClick={start} className="w-full py-3.5 rounded-full text-[15px] font-semibold text-white transition-transform active:translate-y-0.5 mb-7" style={{ backgroundColor: ACCENT, boxShadow: '0 4px 0 #B54D14' }}>
        Start focusing
      </button>

      {grove.length > 0 && (
        <>
          <h3 className="text-[11px] font-bold uppercase tracking-[0.12em] mb-2.5" style={{ color: '#9e9186' }}>Your grove · {grove.length} session{grove.length === 1 ? '' : 's'}</h3>
          <div className="grid grid-cols-4 sm:grid-cols-6 gap-2">
            {grove.slice(0, 18).map(r => <PlantThumb key={r.ts} seed={r.seed} minutes={r.minutes} />)}
          </div>
        </>
      )}
    </div>
  );
};

export default FocusSession;
