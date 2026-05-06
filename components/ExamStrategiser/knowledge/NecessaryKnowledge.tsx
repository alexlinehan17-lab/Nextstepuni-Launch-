/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Necessary Knowledge — tab landing.
 *
 * Hero, five entry tiles for Stage 1 modules, and a closing Chief Examiner
 * Report quote that frames the whole tab's thesis.
 *
 * Source of truth for content: /docs/leaving-cert-knowledge-dossier.md.
 * Every claim here traces to that file.
 */

import React from 'react';

const TEAL = '#2A7D6F';

export type KnowledgeModuleId =
  | 'command-words'
  | 'pclm'
  | 'time-allocation'
  | 'pet-peeves'
  | 'marking-grammar';

interface ModuleTile {
  id: KnowledgeModuleId;
  title: string;
  valueProp: string;
  estimatedMinutes: number;
}

const TILES: ModuleTile[] = [
  {
    id: 'command-words',
    title: 'Command Word Decoder',
    valueProp: 'Paste any LC question. See the command words, modifiers, the structural template the examiner expects, and the specific error each one catches.',
    estimatedMinutes: 8,
  },
  {
    id: 'pclm',
    title: 'PCLM Allocator',
    valueProp: 'The Purpose Ceiling rule in English caps your Coherence and Language marks at your Purpose mark. See it in action with sliders.',
    estimatedMinutes: 6,
  },
  {
    id: 'time-allocation',
    title: 'Time-Allocation Calculator',
    valueProp: 'Per-mark timing for every paper. Plus a sunk-cost simulator showing why a part-answer to all required questions beats a perfect answer to fewer.',
    estimatedMinutes: 7,
  },
  {
    id: 'pet-peeves',
    title: 'Examiner Pet-Peeve Trainer',
    valueProp: 'The same complaints every Chief Examiner Report makes, year after year. Card-stack of the perennial 12, with the fix for each.',
    estimatedMinutes: 10,
  },
  {
    id: 'marking-grammar',
    title: 'Marking-Scheme Grammar',
    valueProp: 'How each subject is actually marked: PCLM in English, SRPs in Geography, Attempt-mark/Blunder/Slip in Maths, headings in Accounting, key-phrases in Sciences.',
    estimatedMinutes: 9,
  },
];

interface Props {
  onOpenModule: (id: KnowledgeModuleId) => void;
}

const NecessaryKnowledge: React.FC<Props> = ({ onOpenModule }) => {
  return (
    <div className="space-y-6">
      <header>
        <p className="font-sans" style={{ fontSize: 11, fontWeight: 700, textTransform: 'uppercase', letterSpacing: 0.6, color: '#A8A29E' }}>
          Necessary Knowledge
        </p>
        <h1 className="font-serif" style={{ fontSize: 28, fontWeight: 600, color: '#1A1A1A', marginTop: 4, lineHeight: 1.2 }}>
          The hidden curriculum of the Leaving Cert.
        </h1>
        <p className="font-sans max-w-xl" style={{ fontSize: 14, color: '#78716C', marginTop: 8, lineHeight: 1.55 }}>
          Marking schemes, command words, examiner pet peeves — the stuff that separates a H4 from a H2 that nobody actually teaches you.
        </p>
      </header>

      <div className="grid sm:grid-cols-2 gap-3">
        {TILES.map(tile => (
          <Tile key={tile.id} tile={tile} onOpen={() => onOpenModule(tile.id)} />
        ))}
      </div>

      <ChiefExaminerCallout />
    </div>
  );
};

const Tile: React.FC<{ tile: ModuleTile; onOpen: () => void }> = ({ tile, onOpen }) => (
  <button
    type="button"
    onClick={onOpen}
    className="rounded-2xl text-left transition-colors w-full"
    style={{
      backgroundColor: '#FFFFFF',
      border: '1px solid #EDEBE8',
      padding: '20px 22px',
      cursor: 'pointer',
    }}
    onMouseEnter={(e) => { e.currentTarget.style.borderColor = `${TEAL}55`; e.currentTarget.style.backgroundColor = '#FAF7F4'; }}
    onMouseLeave={(e) => { e.currentTarget.style.borderColor = '#EDEBE8'; e.currentTarget.style.backgroundColor = '#FFFFFF'; }}
  >
    <div className="flex items-start justify-between gap-3 mb-2">
      <h3 className="font-serif" style={{ fontSize: 16, fontWeight: 600, color: '#1A1A1A', lineHeight: 1.3 }}>
        {tile.title}
      </h3>
      <span
        className="font-sans shrink-0"
        style={{
          fontSize: 10,
          fontWeight: 700,
          color: TEAL,
          backgroundColor: '#FAF7F4',
          border: `1px solid ${TEAL}33`,
          borderRadius: 999,
          padding: '2px 8px',
          whiteSpace: 'nowrap',
        }}
      >
        {tile.estimatedMinutes} min
      </span>
    </div>
    <p className="font-sans" style={{ fontSize: 13, color: '#5C5852', lineHeight: 1.55, marginBottom: 14 }}>
      {tile.valueProp}
    </p>
    <span
      className="font-sans inline-flex items-center gap-1"
      style={{ fontSize: 12, fontWeight: 600, color: TEAL }}
    >
      Start
      <svg width="11" height="11" viewBox="0 0 12 12" fill="none" aria-hidden>
        <path d="M4 3L7 6L4 9" stroke="currentColor" strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round" />
      </svg>
    </span>
  </button>
);

/** Closing CER quote to frame the tab's thesis. Drawn from dossier § B1
 *  (English CER 2013) — the line the entire "exam technique > content"
 *  argument rests on. */
const ChiefExaminerCallout: React.FC = () => (
  <section
    className="rounded-2xl"
    style={{
      backgroundColor: '#FAF7F4',
      border: `1px solid ${TEAL}33`,
      padding: '22px 26px',
    }}
  >
    <p className="font-sans" style={{ fontSize: 10, fontWeight: 700, textTransform: 'uppercase', letterSpacing: 0.6, color: TEAL, marginBottom: 8 }}>
      What the examiners keep saying
    </p>
    <blockquote
      className="font-serif"
      style={{
        fontSize: 17,
        fontStyle: 'italic',
        color: '#1A1A1A',
        lineHeight: 1.45,
        marginBottom: 10,
      }}
    >
      "Weaker responses tended to be characterised by an over-rehearsed formulaic approach."
    </blockquote>
    <p className="font-sans" style={{ fontSize: 12, color: '#78716C' }}>
      — Chief Examiner's Report, English 2013. The complaint recurs across English (2001, 2005, 2008), Modern Languages (2016), Home Economics (2017) and every other subject the SEC has reported on. Exam technique is the trainable variable that separates grades.
    </p>
  </section>
);

export default NecessaryKnowledge;
