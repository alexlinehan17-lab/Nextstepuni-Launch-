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
import type { SecCard, SecDiagramCard } from '@/types/markBank';

/* A stand-in illustration. NOT the SEC figure — the real corpus binds by
 * candidate id, and inventing artwork over a primary source is exactly what
 * this tool exists to stop. Labelled as a placeholder wherever it appears. */
const placeholderFungus = 'data:image/svg+xml;utf8,' + encodeURIComponent(`
  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 200" width="300" height="200">
    <rect x="0" y="150" width="300" height="50" fill="#9a9a9a"/>
    <g stroke="#c4c4c4" stroke-width="4" fill="none">
      <path d="M60 150 V95"/><path d="M110 150 V70"/><path d="M160 150 V60"/><path d="M210 150 V85"/>
      <path d="M60 150 C 95 140, 130 140, 160 150"/>
    </g>
    <circle cx="60" cy="88" r="13" fill="#9a9a9a"/><circle cx="110" cy="63" r="15" fill="#9a9a9a"/>
    <circle cx="160" cy="52" r="16" fill="#9a9a9a"/><circle cx="210" cy="78" r="13" fill="#9a9a9a"/>
    <g fill="#9a9a9a"><circle cx="238" cy="70" r="3"/><circle cx="250" cy="62" r="3"/><circle cx="246" cy="80" r="3"/><circle cx="258" cy="74" r="3"/></g>
    <g font-family="Georgia" font-size="17" font-weight="bold" fill="#111">
      <text x="150" y="26">A</text><text x="252" y="46">B</text><text x="92" y="140">C</text>
    </g>
    <g stroke="#111" stroke-width="1.6" fill="none">
      <path d="M155 30 L 160 36"/><path d="M250 50 L 246 58"/><path d="M97 136 L 104 146"/>
    </g>
  </svg>`);

const qa = { gates: ['verbatim', 'tariff'], humanReviewedBy: 'preview', humanReviewedAt: '2026-07-30' };
const base = {
  subjectId: 'biology', level: 'higher' as const, year: 2025,
  specVersion: 'lc-biology-2002', qa,
};

/** Card 1 — diagram with asterisked gate rows, an open list, and a label key. */
const rhizopus: SecDiagramCard = {
  ...base, source: 'sec', kind: 'diagram',
  id: 'bio-2025-hl-q16a', topicId: 'biology-3-2', conceptId: 'rhizopus-structure',
  paperFileid: 'LC025ALP040EV', section: 'C', questionRef: '2025 HL Q16(a)',
  stem: 'The diagram shows a fungus grown on bread.',
  questionText: 'Name the structures labelled A, B and C, and give one function of C.',
  tariffModel: { kind: 'fixed' }, totalMarks: 9,
  rows: [
    { id: 'g-a', kind: 'gate', verbatim: 'A — Sporangium', marks: 0, exactTermRequired: true },
    { id: 'g-b', kind: 'gate', verbatim: 'B — Spore', marks: 0, exactTermRequired: true },
    { id: 'g-c', kind: 'gate', verbatim: 'C — Stolon', marks: 0, exactTermRequired: true },
    { id: 'r-fn', kind: 'point', verbatim: 'One function of C — spreads the fungus (to a new food source)', marks: 3 },
    { id: 'r-nut', kind: 'alt', verbatim: 'Method of nutrition — saprophytic', accepts: ['heterotrophic'], openList: true, marks: 6 },
  ],
  figure: {
    candId: 'preview-placeholder', src: placeholderFungus, srcHash: 'preview',
    alt: 'Placeholder illustration: rounded heads on upright stalks, spores dispersing at the right, and a filament running along the surface',
    lettersVisible: ['A', 'B', 'C'],
    attribution: 'Placeholder illustration for preview — not the SEC figure',
  },
  labelKey: [
    { letter: 'A', meaning: 'Sporangium', askedInThisQuestion: true },
    { letter: 'B', meaning: 'Spore', askedInThisQuestion: true },
    { letter: 'C', meaning: 'Stolon', askedInThisQuestion: true },
  ],
  schemeCitation: 'Marking points quoted from the SEC marking scheme, Biology 2025 Higher Level — © State Examinations Commission.',
};

/** Card 2 — a fixed tariff with a dependent row: the description is unreachable
 *  until the process is named. */
const peristalsis: SecCard = {
  ...base, source: 'sec', kind: 'question',
  id: 'bio-2025-hl-q6-bc', topicId: 'biology-2-6', conceptId: 'peristalsis',
  paperFileid: 'LC025ALP038EV', section: 'A', questionRef: '2025 HL Q6(b)–(c)',
  questionText: 'Name and describe briefly the method by which food travels through structure A.',
  tariffModel: { kind: 'fixed' }, totalMarks: 8,
  rows: [
    { id: 'r-name', kind: 'point', verbatim: 'Name — Peristalsis', marks: 3 },
    { id: 'r-desc', kind: 'point', verbatim: '(involuntary) muscular contractions that push food along', marks: 3, dependsOn: 'r-name' },
    { id: 'r-ph', kind: 'point', verbatim: 'The pH lowers as food travels from A to B', marks: 2 },
  ],
  schemeCitation: 'Marking points quoted from the SEC marking scheme, Biology 2025 Higher Level — © State Examinations Commission.',
};

/** Card 3 — an order-dependent split, where per-row mark values do not exist and
 *  so none are shown. */
const waterUptake: SecCard = {
  ...base, source: 'sec', kind: 'question', year: 2023,
  id: 'bio-2023-hl-q3', topicId: 'biology-2-6', conceptId: 'water-transport',
  paperFileid: 'LC025ALP038EV', section: 'A', questionRef: '2023 HL Q3',
  questionText: 'Outline how water from the soil reaches the leaf of a plant.',
  tariffModel: { kind: 'orderedSplit', notation: '2(5) + 5(2)' }, totalMarks: 20,
  rows: [
    { id: 'w1', kind: 'point', verbatim: 'Root hair', marks: null },
    { id: 'w2', kind: 'point', verbatim: 'Osmosis', marks: null, contextNote: 'The word alone scores nothing — it must be stated as the mechanism of uptake.' },
    { id: 'w3', kind: 'point', verbatim: 'Xylem', marks: null, contextNote: 'Named as the vessel the water travels up.' },
    { id: 'w4', kind: 'point', verbatim: 'Transpiration (pull)', marks: null },
    { id: 'w5', kind: 'point', verbatim: 'Cohesion / adhesion of water molecules', marks: null, openList: true },
  ],
  schemeCitation: 'Marking points quoted from the SEC marking scheme, Biology 2023 Higher Level — © State Examinations Commission.',
};

const CARDS: SecCard[] = [rhizopus, peristalsis, waterUptake];

const seenAWeekAgo = (): CardMemory => ({
  s: 6, d: 5, last: Date.now() - 6 * 86_400_000, reps: 3, lapses: 0, state: 2,
});

const WIDTHS = [360, 390, 430, 0];

const Harness: React.FC = () => {
  const [width, setWidth] = useState(390);
  const [run, setRun] = useState(0);
  const [memories, setMemories] = useState<Record<string, CardMemory>>(() => ({
    'bio-2025-hl-q16a': seenAWeekAgo(),
    'bio-2025-hl-q6-bc': seenAWeekAgo(),
    'bio-2023-hl-q3': NEW_CARD,
  }));
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
          3 cards: diagram with exact-term gates · dependent rows · order-dependent split
        </span>
      </div>

      <div style={{
        width: width || '100%', margin: '0 auto', position: 'relative',
        boxShadow: width ? '0 0 0 1px #2a2a2a' : 'none',
      }}>
        <SessionScreen
          key={run}
          cards={CARDS}
          memories={memories}
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
