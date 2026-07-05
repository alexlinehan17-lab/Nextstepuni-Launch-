/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * AI mark-scheme feedback panel (feature E11) — SHIP-GATED, INERT.
 *
 * Renders nothing until AI_MARKING_LIVE is on (governance sign-off + a governed
 * server endpoint). The typed UI seam exists so the flow can be reviewed without
 * any model ever executing — `requestAnswerMarking` throws by design, and the
 * catch surfaces a graceful, honest message. Self-marking against the real
 * scheme remains the shipped, non-AI path.
 */

import React, { useState } from 'react';
import { Sparkles, Check, X } from 'lucide-react';
import {
  AI_MARKING_LIVE,
  requestAnswerMarking,
  tallyMarking,
  type MarkingResult,
} from '../../data/aiMarking';

const INK = '#1a1a1a';
const ACCENT = '#F26B1F';

const AiMarkingPanel: React.FC<{ questionRef: string }> = ({ questionRef }) => {
  const [answer, setAnswer] = useState('');
  const [result, setResult] = useState<MarkingResult | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);

  if (!AI_MARKING_LIVE) return null;

  const mark = async () => {
    if (!answer.trim()) return;
    setBusy(true);
    setError(null);
    try {
      setResult(await requestAnswerMarking({ questionRef, studentAnswer: answer }));
    } catch {
      setError('Instant marking isn’t available yet — self-mark against the scheme for now.');
    } finally {
      setBusy(false);
    }
  };

  const tally = result ? tallyMarking(result.points) : null;

  return (
    <div className="rounded-2xl border-2 border-[#1a1a1a] dark:border-zinc-700 bg-white dark:bg-zinc-900 px-4 py-4">
      <p className="text-[13.5px] font-semibold mb-2 flex items-center gap-1.5" style={{ fontFamily: "'Source Serif 4', serif", color: INK }}>
        <Sparkles size={15} style={{ color: ACCENT }} /> Mark my answer against the scheme
      </p>
      <textarea
        value={answer}
        onChange={e => setAnswer(e.target.value)}
        rows={4}
        placeholder="Type your answer…"
        className="w-full mb-2 px-3 py-2 rounded-xl border-2 border-zinc-200 dark:border-zinc-700 bg-white dark:bg-zinc-900 text-[14px] outline-none focus:border-[#1a1a1a]"
      />
      <button
        onClick={mark}
        disabled={!answer.trim() || busy}
        className="rounded-full px-5 py-2 text-[13px] font-semibold text-white disabled:opacity-40 transition-transform active:translate-y-0.5"
        style={{ backgroundColor: ACCENT, boxShadow: '0 3px 0 #B54D14' }}
      >
        {busy ? 'Marking…' : 'Mark my answer'}
      </button>

      {error && <p className="text-[12.5px] mt-3" style={{ color: '#8C3A0E' }}>{error}</p>}

      {result && tally && (
        <div className="mt-4">
          <p className="text-[14px] font-bold mb-2" style={{ color: INK }}>{tally.awarded} / {tally.max} marks</p>
          <div className="space-y-1.5">
            {result.points.map((pt, i) => (
              <div key={i} className="flex items-start gap-2 text-[13px]">
                {pt.awarded
                  ? <Check size={15} className="shrink-0 mt-0.5" style={{ color: '#3A8D5F' }} />
                  : <X size={15} className="shrink-0 mt-0.5" style={{ color: '#C0392B' }} />}
                <span style={{ color: '#3a3530' }}>{pt.text}{pt.note ? ` — ${pt.note}` : ''}</span>
              </div>
            ))}
          </div>
          <p className="text-[13px] mt-3 leading-relaxed" style={{ color: '#5a5550' }}>{result.summary}</p>
        </div>
      )}
    </div>
  );
};

export default AiMarkingPanel;
