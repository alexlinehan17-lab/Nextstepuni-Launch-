/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Oral Exam Trainer (Launchpad tool) — the one high-weight Leaving Cert component
 * no study app prepares you for: the spoken exam. It lays out the real SEC oral
 * structure, gives verified preparation guidance and speaking prompts, and lets
 * a student practise the hardest thing to rehearse alone — speaking — by
 * recording an answer and playing it straight back. Audio never leaves the
 * device (in-memory only; nothing uploaded, nothing stored). A per-component
 * readiness tracker shows where they're prepared and where they're not.
 *
 * MVP: Leaving Cert Irish (Gaeilge). Content lives in data/oralExam/irish.ts,
 * every fact sourced to the SEC/NCCA.
 */

import React, { useCallback, useEffect, useRef, useState } from 'react';
import { ArrowLeft, Mic, Square, RotateCcw, Check } from 'lucide-react';
import { IRISH_ORAL } from '../data/oralExam/irish';
import { type OralComponent } from '../data/oralExam/types';

const INK = '#1a1a1a';
const ACCENT = '#F26B1F';
const SUCCESS = '#3A8D5F';
const GREEN = '#4C8C5E';

const READINESS = ['Not yet', 'Shaky', 'Getting there', 'Ready'];
const readyColor = (n: number) => (n >= 3 ? SUCCESS : n >= 1 ? ACCENT : '#9e9186');

// ── readiness store (local, per uid) ──
const rKey = (uid?: string) => `oral:readiness:${uid || 'anon'}`;
const loadReadiness = (uid?: string): Record<string, number> => {
  try {
    const raw = localStorage.getItem(rKey(uid));
    return raw ? JSON.parse(raw) : {};
  } catch {
    return {};
  }
};
const saveReadiness = (uid: string | undefined, r: Record<string, number>) => {
  try {
    localStorage.setItem(rKey(uid), JSON.stringify(r));
  } catch {
    /* ignore */
  }
};

interface Props {
  uid?: string;
}

const OralExamTrainer: React.FC<Props> = ({ uid }) => {
  const exam = IRISH_ORAL;
  const [active, setActive] = useState<OralComponent | null>(null);
  const [promptIdx, setPromptIdx] = useState(0);
  const [readiness, setReadiness] = useState<Record<string, number>>(() => loadReadiness(uid));

  // ── on-device recorder ──
  const [recording, setRecording] = useState(false);
  const [audioUrl, setAudioUrl] = useState<string | null>(null);
  const [micError, setMicError] = useState<string | null>(null);
  const recorderRef = useRef<MediaRecorder | null>(null);
  const streamRef = useRef<MediaStream | null>(null);
  const audioUrlRef = useRef<string | null>(null);
  audioUrlRef.current = audioUrl;

  const stopStream = () => {
    streamRef.current?.getTracks().forEach(t => t.stop());
    streamRef.current = null;
  };
  const clearAudio = useCallback(() => {
    if (audioUrlRef.current) URL.revokeObjectURL(audioUrlRef.current);
    setAudioUrl(null);
  }, []);

  useEffect(() => () => { stopStream(); if (audioUrlRef.current) URL.revokeObjectURL(audioUrlRef.current); }, []);

  const startRecording = async () => {
    setMicError(null);
    clearAudio();
    const md = typeof navigator !== 'undefined' ? navigator.mediaDevices : undefined;
    if (!md?.getUserMedia || typeof MediaRecorder === 'undefined') {
      setMicError('Recording isn’t supported on this device — you can still practise out loud and set your readiness below.');
      return;
    }
    try {
      const stream = await md.getUserMedia({ audio: true });
      streamRef.current = stream;
      const chunks: BlobPart[] = [];
      const mr = new MediaRecorder(stream);
      mr.ondataavailable = e => { if (e.data.size) chunks.push(e.data); };
      mr.onstop = () => {
        const blob = new Blob(chunks, { type: mr.mimeType || 'audio/webm' });
        setAudioUrl(URL.createObjectURL(blob));
        stopStream();
      };
      recorderRef.current = mr;
      mr.start();
      setRecording(true);
    } catch {
      setMicError('Couldn’t reach the microphone. Check permissions, or practise out loud and set your readiness below.');
      stopStream();
    }
  };
  const stopRecording = () => {
    recorderRef.current?.stop();
    setRecording(false);
  };

  const setReady = (componentId: string, level: number) => {
    const next = { ...readiness, [componentId]: level };
    setReadiness(next);
    saveReadiness(uid, next);
  };

  const openComponent = (c: OralComponent) => {
    setActive(c);
    setPromptIdx(0);
    clearAudio();
    setMicError(null);
  };
  const backHome = () => {
    if (recording) stopRecording();
    stopStream();
    clearAudio();
    setActive(null);
  };

  // ═══════════ Practice a component ═══════════
  if (active) {
    const prompt = active.prompts[promptIdx % Math.max(1, active.prompts.length)];
    const level = readiness[active.id] ?? 0;
    return (
      <div className="w-full max-w-xl mx-auto pb-12">
        <button onClick={backHome} className="flex items-center gap-1.5 text-[13px] font-medium mb-4" style={{ color: '#7a7068' }}>
          <ArrowLeft size={15} /> Oral components
        </button>
        <p className="text-[10.5px] font-bold uppercase tracking-[0.12em] mb-1" style={{ color: '#9e9186' }}>{active.nameGa} · {active.nameEn}</p>
        <h2 className="text-2xl font-semibold mb-4" style={{ fontFamily: "'Source Serif 4', serif", color: INK }}>Practise speaking</h2>

        {/* Prompt card */}
        <div className="rounded-2xl border-2 border-[#1a1a1a] dark:border-zinc-700 bg-white dark:bg-zinc-900 shadow-[4px_4px_0_0_#1a1a1a] dark:shadow-[4px_4px_0_0_#3f3f46] px-5 py-5 mb-4">
          <p className="text-[10.5px] font-bold uppercase tracking-[0.12em] mb-2" style={{ color: '#9e9186' }}>Prompt</p>
          <p className="text-[16px] leading-relaxed" style={{ color: INK }}>{prompt.en}</p>
          {prompt.ga && <p className="text-[14px] italic mt-2" style={{ color: '#5a5550' }}>{prompt.ga}</p>}
          <button
            onClick={() => { setPromptIdx(i => i + 1); clearAudio(); }}
            className="mt-3 text-[12.5px] font-semibold"
            style={{ color: ACCENT }}
          >
            Another prompt →
          </button>
        </div>

        {/* Recorder */}
        <div className="rounded-2xl border-2 border-[#d0cdc8] dark:border-zinc-700 bg-white dark:bg-zinc-900 px-5 py-5 mb-4 text-center">
          <p className="text-[12.5px] mb-3" style={{ color: '#7a7068' }}>Say your answer out loud, then play it back. Your recording stays on this device — it’s never uploaded.</p>
          {!recording ? (
            <button onClick={startRecording} className="inline-flex items-center gap-2 rounded-full px-6 py-3 text-[15px] font-semibold text-white transition-transform active:translate-y-0.5" style={{ backgroundColor: GREEN, boxShadow: '0 4px 0 #366B44' }}>
              <Mic size={18} /> Record
            </button>
          ) : (
            <button onClick={stopRecording} className="inline-flex items-center gap-2 rounded-full px-6 py-3 text-[15px] font-semibold text-white transition-transform active:translate-y-0.5" style={{ backgroundColor: '#C0392B', boxShadow: '0 4px 0 #8E2A20' }}>
              <Square size={16} /> Stop
            </button>
          )}
          {micError && <p className="text-[12.5px] mt-3" style={{ color: '#8C3A0E' }}>{micError}</p>}
          {audioUrl && (
            <div className="mt-4">
              <audio controls src={audioUrl} className="w-full" />
              <button onClick={() => { clearAudio(); startRecording(); }} className="inline-flex items-center gap-1.5 mt-2 text-[12.5px] font-semibold" style={{ color: ACCENT }}>
                <RotateCcw size={13} /> Record again
              </button>
            </div>
          )}
        </div>

        {/* Readiness */}
        <p className="text-[11px] font-bold uppercase tracking-[0.12em] mb-2" style={{ color: '#9e9186' }}>How ready do you feel on this?</p>
        <div className="grid grid-cols-4 gap-2">
          {READINESS.map((label, i) => (
            <button
              key={i}
              onClick={() => setReady(active.id, i)}
              className="flex flex-col items-center gap-0.5 rounded-xl border-2 py-2.5 text-[12px] font-semibold transition-transform active:translate-y-0.5"
              style={level === i ? { backgroundColor: i >= 3 ? '#E8F2EC' : '#FDEEDF', borderColor: readyColor(i), color: readyColor(i) } : { backgroundColor: '#fff', borderColor: '#d0cdc8', color: '#7a7068' }}
            >
              {i >= 3 && level === i ? <Check size={14} /> : null}
              {label}
            </button>
          ))}
        </div>
      </div>
    );
  }

  // ═══════════ Home ═══════════
  const readyCount = exam.components.filter(c => (readiness[c.id] ?? 0) >= 3).length;
  return (
    <div className="w-full max-w-xl mx-auto pb-12">
      <p className="text-[14px] leading-relaxed mb-4" style={{ color: '#5a5550' }}>{exam.intro}</p>
      <div className="rounded-xl px-4 py-3 mb-5" style={{ backgroundColor: '#EAF3EC', border: `1.5px solid ${GREEN}` }}>
        <p className="text-[13px] font-semibold" style={{ color: '#1F5F3E' }}>{exam.totalWeight}</p>
        {exam.levelNote && <p className="text-[12px] mt-0.5" style={{ color: '#3a5a45' }}>{exam.levelNote}</p>}
      </div>

      <div className="flex items-center justify-between mb-2.5">
        <h3 className="text-[11px] font-bold uppercase tracking-[0.12em]" style={{ color: '#9e9186' }}>The four parts</h3>
        <span className="text-[11px] font-semibold" style={{ color: readyCount === exam.components.length ? '#1F5F3E' : '#7a7068' }}>{readyCount}/{exam.components.length} feel ready</span>
      </div>

      <div className="space-y-2.5">
        {exam.components.map(c => {
          const level = readiness[c.id] ?? 0;
          return (
            <button
              key={c.id}
              onClick={() => openComponent(c)}
              className="w-full text-left rounded-2xl border-2 border-[#1a1a1a] dark:border-zinc-700 bg-white dark:bg-zinc-900 shadow-[3px_3px_0_0_#1a1a1a] dark:shadow-[3px_3px_0_0_#3f3f46] px-4 py-3.5 transition-transform active:translate-y-0.5 hover:-translate-y-0.5"
            >
              <div className="flex items-start justify-between gap-3">
                <span className="min-w-0">
                  <span className="block text-[15px] font-semibold" style={{ fontFamily: "'Source Serif 4', serif", color: INK }}>{c.nameGa} <span className="text-[13px] font-normal" style={{ color: '#7a7068' }}>· {c.nameEn}</span></span>
                  <span className="block text-[12px] mt-0.5" style={{ color: '#7a7068' }}>{c.whatItIs}</span>
                </span>
                <span className="shrink-0 text-[10.5px] font-bold px-2 py-0.5 rounded-full whitespace-nowrap" style={{ backgroundColor: '#EAF3EC', color: '#1F5F3E' }}>{c.weight}</span>
              </div>
              <div className="flex items-center gap-1.5 mt-2">
                <span className="text-[11px]" style={{ color: '#9e9186' }}>Readiness:</span>
                <span className="text-[11px] font-semibold" style={{ color: readyColor(level) }}>{READINESS[level]}</span>
              </div>
            </button>
          );
        })}
      </div>

      <p className="text-[11px] leading-relaxed mt-6" style={{ color: '#9e9186' }}>
        Structure and weightings per the State Examinations Commission. Recordings are processed on your device only and are never uploaded or saved.
        {exam.sources.length > 0 && (
          <> Source{exam.sources.length === 1 ? '' : 's'}: {exam.sources.map((s, i) => (
            <React.Fragment key={s.url}>{i > 0 ? ', ' : ' '}<a href={s.url} target="_blank" rel="noreferrer" className="underline" style={{ color: '#7a7068' }}>{s.label}</a></React.Fragment>
          ))}.</>
        )}
      </p>
    </div>
  );
};

export default OralExamTrainer;
