/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Oral Exam Trainer (Launchpad tool) — the one high-weight Leaving Cert component
 * no study app prepares you for: the spoken exam. It lays out the real SEC oral
 * structure, gives verified preparation guidance and speaking prompts, and lets
 * a student practise the hardest thing to rehearse alone — speaking — by
 * recording an answer and playing it straight back. Audio never leaves the
 * device: at most the previous + latest take per part are kept in this
 * browser's IndexedDB (timestamps in localStorage) so the student can hear
 * their own progress — nothing is ever uploaded, shared, or sent to Firestore.
 * A per-component readiness tracker shows where they're prepared and where
 * they're not, and a light spaced schedule (1/3/8/21 days — see
 * oralReadiness.ts) marks parts due for a re-record.
 *
 * MVP: Leaving Cert Irish (Gaeilge). Content lives in data/oralExam/irish.ts,
 * every fact sourced to the SEC/NCCA.
 */

import React, { useCallback, useEffect, useRef, useState } from 'react';
import { ArrowLeft, Mic, Square, RotateCcw, Check } from 'lucide-react';
import { IRISH_ORAL } from '../data/oralExam/irish';
import { type OralComponent } from '../data/oralExam/types';
import {
  type TakeMeta,
  appendTake,
  daysAgoLabel,
  estimateWpm,
  isDueForRerecord,
  loadTakeBlobs,
  loadTakeMeta,
  paceNote,
  saveTakeBlobs,
  saveTakeMeta,
  wordCount,
} from './oralReadiness';

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
  const [takesMeta, setTakesMeta] = useState<Record<string, TakeMeta[]>>(() => loadTakeMeta(uid));

  // ── on-device recorder (latest + previous take per part; audio never leaves the device) ──
  const [recording, setRecording] = useState(false);
  const [audioUrl, setAudioUrl] = useState<string | null>(null);
  const [prevUrl, setPrevUrl] = useState<string | null>(null);
  const [paceWpm, setPaceWpm] = useState<number | null>(null);
  const [micError, setMicError] = useState<string | null>(null);
  const recorderRef = useRef<MediaRecorder | null>(null);
  const streamRef = useRef<MediaStream | null>(null);
  const audioUrlRef = useRef<string | null>(null);
  audioUrlRef.current = audioUrl;
  const prevUrlRef = useRef<string | null>(null);
  prevUrlRef.current = prevUrl;
  const activeIdRef = useRef<string | null>(null);
  const latestBlobRef = useRef<Blob | null>(null);
  const recStartRef = useRef(0);
  const recScriptWordsRef = useRef(0);
  const recPartIdRef = useRef<string | null>(null);

  const stopStream = () => {
    streamRef.current?.getTracks().forEach(t => t.stop());
    streamRef.current = null;
  };
  const clearAudio = useCallback(() => {
    if (audioUrlRef.current) URL.revokeObjectURL(audioUrlRef.current);
    setAudioUrl(null);
    if (prevUrlRef.current) URL.revokeObjectURL(prevUrlRef.current);
    setPrevUrl(null);
    latestBlobRef.current = null;
    setPaceWpm(null);
  }, []);

  useEffect(() => () => {
    stopStream();
    if (audioUrlRef.current) URL.revokeObjectURL(audioUrlRef.current);
    if (prevUrlRef.current) URL.revokeObjectURL(prevUrlRef.current);
  }, []);

  const startRecording = async () => {
    setMicError(null);
    recPartIdRef.current = active?.id ?? null;
    // Pace is only estimable when there's a script text (the Irish scaffold) to count words from.
    const script = active ? active.prompts[promptIdx % Math.max(1, active.prompts.length)]?.ga : undefined;
    recScriptWordsRef.current = wordCount(script ?? '');
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
        const durationMs = Date.now() - recStartRef.current;
        const partId = recPartIdRef.current;
        // The take that was "latest" becomes the previous one — hear yourself then vs now.
        const demoted = latestBlobRef.current;
        if (prevUrlRef.current) URL.revokeObjectURL(prevUrlRef.current);
        setPrevUrl(demoted ? URL.createObjectURL(demoted) : null);
        if (audioUrlRef.current) URL.revokeObjectURL(audioUrlRef.current);
        setAudioUrl(URL.createObjectURL(blob));
        latestBlobRef.current = blob;
        setPaceWpm(estimateWpm(recScriptWordsRef.current, durationMs));
        if (partId) {
          setTakesMeta(cur => {
            const next = appendTake(cur, partId, { at: Date.now(), durationMs });
            saveTakeMeta(uid, next);
            return next;
          });
          // Best-effort on-device persistence (previous + latest only, never uploaded).
          void saveTakeBlobs(uid, partId, demoted ? [demoted, blob] : [blob]);
        }
        stopStream();
      };
      recorderRef.current = mr;
      mr.start();
      recStartRef.current = Date.now();
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
    activeIdRef.current = c.id;
    setPromptIdx(0);
    clearAudio();
    setMicError(null);
    // Bring back this part's kept takes (on-device only) so old-vs-new playback works across days.
    void loadTakeBlobs(uid, c.id).then(blobs => {
      if (activeIdRef.current !== c.id || latestBlobRef.current) return; // navigated away, or already re-recorded
      if (blobs.length >= 1) {
        const latest = blobs[blobs.length - 1];
        latestBlobRef.current = latest;
        setAudioUrl(URL.createObjectURL(latest));
      }
      if (blobs.length >= 2) setPrevUrl(URL.createObjectURL(blobs[blobs.length - 2]));
    });
  };
  const backHome = () => {
    if (recording) stopRecording();
    stopStream();
    clearAudio();
    setActive(null);
    activeIdRef.current = null;
  };

  const now = Date.now();

  // ═══════════ Practice a component ═══════════
  if (active) {
    const prompt = active.prompts[promptIdx % Math.max(1, active.prompts.length)];
    const level = readiness[active.id] ?? 0;
    const meta = takesMeta[active.id] ?? [];
    const latestMeta = meta[meta.length - 1];
    const prevMeta = meta.length >= 2 ? meta[meta.length - 2] : undefined;
    const pace = paceWpm !== null ? paceNote(paceWpm) : null;
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
            onClick={() => setPromptIdx(i => i + 1)}
            className="mt-3 text-[12.5px] font-semibold"
            style={{ color: ACCENT }}
          >
            Another prompt →
          </button>
        </div>

        {/* Recorder */}
        <div className="rounded-2xl border-2 border-[#d0cdc8] dark:border-zinc-700 bg-white dark:bg-zinc-900 px-5 py-5 mb-4 text-center">
          <p className="text-[12.5px] mb-3" style={{ color: '#7a7068' }}>Say your answer out loud, then play it back. Recordings stay on this device — never uploaded. Your latest and previous take are kept so you can hear the difference.</p>
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
            <div className="mt-4 text-left">
              <p className="text-[10.5px] font-bold uppercase tracking-[0.12em] mb-1" style={{ color: '#9e9186' }}>
                Latest take{latestMeta ? ` · ${daysAgoLabel(latestMeta.at, now)}` : ''}
              </p>
              <audio controls src={audioUrl} className="w-full" />
              {paceWpm !== null && (
                <p className="text-[11.5px] mt-1.5" style={{ color: '#9e9186' }}>
                  Pace: about {paceWpm} words per minute{pace ? ` · a touch ${pace}` : ''} (rough estimate from the Irish scaffold)
                </p>
              )}
              {prevUrl && (
                <div className="mt-3 pt-3" style={{ borderTop: '1.5px solid #e0dbd4' }}>
                  <p className="text-[10.5px] font-bold uppercase tracking-[0.12em] mb-1" style={{ color: '#9e9186' }}>
                    Earlier take{prevMeta ? ` · hear yourself ${daysAgoLabel(prevMeta.at, now)}` : ''}
                  </p>
                  <audio controls src={prevUrl} className="w-full" />
                </div>
              )}
              <div className="text-center">
                <button onClick={() => { void startRecording(); }} className="inline-flex items-center gap-1.5 mt-2 text-[12.5px] font-semibold" style={{ color: ACCENT }}>
                  <RotateCcw size={13} /> Record again
                </button>
              </div>
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
          const takes = takesMeta[c.id] ?? [];
          const lastTake = takes[takes.length - 1];
          const due = isDueForRerecord(lastTake?.at, takes.length, now);
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
              <div className="flex items-center flex-wrap gap-1.5 mt-2">
                <span className="text-[11px]" style={{ color: '#9e9186' }}>Readiness:</span>
                <span className="text-[11px] font-semibold" style={{ color: readyColor(level) }}>{READINESS[level]}</span>
                {due && (
                  <span
                    className="text-[10px] font-bold uppercase tracking-[0.06em] px-2 py-0.5 rounded-full"
                    style={{ backgroundColor: '#FDEEDF', color: '#8C3A0E', border: '1px solid rgba(242,107,31,0.2)' }}
                  >
                    Due for a re-record
                  </span>
                )}
                {lastTake && (
                  <span className="text-[11px]" style={{ color: '#9e9186' }}>· last take {daysAgoLabel(lastTake.at, now)}</span>
                )}
              </div>
            </button>
          );
        })}
      </div>

      <p className="text-[11px] leading-relaxed mt-6" style={{ color: '#9e9186' }}>
        Structure and weightings per the State Examinations Commission. Recordings never leave this device — nothing is uploaded or shared. Only your latest and previous take for each part are kept, in this browser, so you can hear your own progress.
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
