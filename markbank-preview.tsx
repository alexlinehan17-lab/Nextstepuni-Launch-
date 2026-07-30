/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Mark Bank — dev-only preview harness.
 *
 * Mark Bank is not yet wired into the Innovation Zone, so there is nothing to
 * navigate to in the app. This mounts the real SessionScreen against the real
 * FSRS scheduler so the whole loop can be clicked through: reveal, claim marks,
 * grade, and see the actual interval the scheduler returns.
 *
 * Served only by the dev server (vite build takes index.html alone), so this
 * never reaches production. Delete once the tool is registered properly.
 */

import React, { useState } from 'react';
import { createRoot } from 'react-dom/client';
import SessionScreen, { type SessionCardResult } from '@/components/MarkBank/SessionScreen';
import {
  NEW_CARD, RETENTION_BASE, grade as gradeCard, intervalWords,
  type CardMemory,
} from '@/components/MarkBank/scheduler';
import { CARDS as SAMPLE_CARDS } from '@/components/MarkBank/cards/higher';
import type { SecCard } from '@/types/markBank';

const CARDS: SecCard[] = SAMPLE_CARDS.slice(0, 12);

const seenAWeekAgo = (): CardMemory => ({
  s: 6, d: 5, last: Date.now() - 6 * 86_400_000, reps: 3, lapses: 0, state: 2,
});

const WIDTHS = [360, 390, 430, 0];

const Harness: React.FC = () => {
  const [width, setWidth] = useState(390);
  const [run, setRun] = useState(0);
  const [memories, setMemories] = useState<Record<string, CardMemory>>(
    () => Object.fromEntries(CARDS.map(c => [c.id, seenAWeekAgo()])),
  );
  const [log, setLog] = useState<string[]>([]);

  const handleGrade = (r: SessionCardResult): string => {
    const now = Date.now();
    const before = memories[r.cardId] ?? NEW_CARD;
    const after = gradeCard(before, r.grade, now, RETENTION_BASE);
    setMemories(m => ({ ...m, [r.cardId]: after }));
    const words = intervalWords(r.cardId, after, now, RETENTION_BASE);
    setLog(l => [...l, `${r.cardId} · ${r.grade} · ${r.marksClaimed}/${r.marksAvailable} marks · back ${words} (stability ${after.s.toFixed(2)}d)`]);
    return words;
  };

  return (
    <div style={{ minHeight: '100vh', background: '#0d0d0d', fontFamily: "'DM Sans', system-ui, sans-serif" }}>
      <div style={{
        display: 'flex', gap: 8, alignItems: 'center', flexWrap: 'wrap',
        padding: '10px 14px', background: '#161616', color: '#e8e8e8', fontSize: 12,
      }}>
        <strong style={{ fontSize: 12, letterSpacing: '.08em', textTransform: 'uppercase' }}>Mark Bank preview</strong>
        {WIDTHS.map(w => (
          <button
            key={w} onClick={() => setWidth(w)}
            style={{
              padding: '5px 11px', borderRadius: 8, cursor: 'pointer', fontSize: 12,
              border: '1px solid ' + (width === w ? '#4CC5B4' : '#3a3a3a'),
              background: width === w ? '#123B2B' : 'transparent',
              color: width === w ? '#fff' : '#b8b8b8',
            }}
          >
            {w === 0 ? 'Full width' : `${w}px`}
          </button>
        ))}
        <button
          onClick={() => { setRun(r => r + 1); setLog([]); }}
          style={{ padding: '5px 11px', borderRadius: 8, cursor: 'pointer', fontSize: 12, border: '1px solid #3a3a3a', background: 'transparent', color: '#b8b8b8' }}
        >
          Restart session
        </button>
        <span style={{ color: '#8a8a8a' }}>
          {CARDS.length} cards from the Higher Level deck
        </span>
      </div>

      <div style={{
        width: width || '100%', margin: '0 auto', position: 'relative',
        boxShadow: width ? '0 0 0 1px #2a2a2a' : 'none',
      }}>
        <SessionScreen
          key={run}
          cards={CARDS}
          subjectLabel="Biology"
          onGrade={handleGrade}
          onExit={() => { setRun(r => r + 1); setLog([]); }}
          onFinish={() => setLog(l => [...l, '— session finished —'])}
        />
      </div>

      {log.length > 0 && (
        <pre style={{
          maxWidth: 760, margin: '18px auto', padding: '12px 14px', borderRadius: 10,
          background: '#161616', color: '#9fd8c8', fontSize: 11.5, lineHeight: 1.7,
          whiteSpace: 'pre-wrap', fontFamily: "'Roboto Mono', ui-monospace, monospace",
        }}>
          {log.join('\n')}
        </pre>
      )}
    </div>
  );
};

createRoot(document.getElementById('root')!).render(<Harness />);
