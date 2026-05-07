/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Necessary Knowledge — tab landing.
 *
 * Hero, two stages of entry tiles, and a closing Chief Examiner Report
 * quote that frames the whole tab's thesis.
 *
 * Stage 1 modules use the quieter Strategiser register.
 * Stage 2 modules use the bolder Brilliant.org / Mercury hybrid register
 * — denser and more instrument-panel-like — and are flagged as such on
 * their tiles.
 *
 * Source of truth for content: /docs/leaving-cert-knowledge-dossier.md.
 * Every claim here traces to that file.
 */

import React from 'react';

const TEAL = '#2A7D6F';
const INK = '#1a1a1a';

export type KnowledgeModuleId =
  // Stage 1
  | 'command-words'
  | 'pclm'
  | 'time-allocation'
  | 'pet-peeves'
  | 'marking-grammar'
  // Stage 2
  | 'srp-identifier'
  | 'working-shown'
  | 'sanity-check'
  | 'spot-the-trap'
  | 'ceiling-visualiser'
  // Stage 3
  | 'comparative-linker';

type Stage = 1 | 2 | 3;

interface ModuleTile {
  id: KnowledgeModuleId;
  stage: Stage;
  title: string;
  valueProp: string;
  estimatedMinutes: number;
}

const TILES: ModuleTile[] = [
  // ─── Stage 1 ────────────────────────────────────────────────────────
  {
    id: 'command-words',
    stage: 1,
    title: 'Command Word Decoder',
    valueProp: 'Paste any LC question. See the command words, modifiers, the structural template the examiner expects, and the specific error each one catches.',
    estimatedMinutes: 8,
  },
  {
    id: 'pclm',
    stage: 1,
    title: 'PCLM Allocator',
    valueProp: 'The Purpose Ceiling rule in English caps your Coherence and Language marks at your Purpose mark. See it in action with sliders.',
    estimatedMinutes: 6,
  },
  {
    id: 'time-allocation',
    stage: 1,
    title: 'Time-Allocation Calculator',
    valueProp: 'Per-mark timing for every paper. Plus a sunk-cost simulator showing why a part-answer to all required questions beats a perfect answer to fewer.',
    estimatedMinutes: 7,
  },
  {
    id: 'pet-peeves',
    stage: 1,
    title: 'Examiner Pet-Peeve Trainer',
    valueProp: 'The same complaints every Chief Examiner Report makes, year after year. Card-stack of the perennial 12, with the fix for each.',
    estimatedMinutes: 10,
  },
  {
    id: 'marking-grammar',
    stage: 1,
    title: 'Marking-Scheme Grammar',
    valueProp: 'How each subject is actually marked: PCLM in English, SRPs in Geography, Attempt-mark/Blunder/Slip in Maths, headings in Accounting, key-phrases in Sciences.',
    estimatedMinutes: 9,
  },
  // ─── Stage 2 ────────────────────────────────────────────────────────
  {
    id: 'srp-identifier',
    stage: 2,
    title: 'SRP Identifier',
    valueProp: 'Read a real long-question paragraph like an examiner. Three phases: highlight what you think counts, see the actual classification, then watch every credited SRP draw down to a live mark counter.',
    estimatedMinutes: 12,
  },
  {
    id: 'working-shown',
    stage: 2,
    title: 'Working-Shown Allocator',
    valueProp: 'Build a Maths/Science answer step by step. Marks land as ribbons next to each step. Slips and blunders are deducted in real time. Five answer paths show what each level of "showing your work" actually scores.',
    estimatedMinutes: 14,
  },
  {
    id: 'sanity-check',
    stage: 2,
    title: 'Sanity-Check Trainer',
    valueProp: 'Four candidate answers, three absurd. Tap each wrong one and identify which check (Order of Magnitude, Units, Sign, Substitute-Back) catches it. The radar pulses around the answer in the colour of the catching check. Reaction time logged.',
    estimatedMinutes: 12,
  },
  {
    id: 'spot-the-trap',
    stage: 2,
    title: 'Spot the Trap',
    valueProp: 'Past-paper-style traps across six subjects. 30-second timer to spot the trap before the reveal. Pattern card every 5 cards shows where your blind spots cluster. Closing trap-map names your worst category.',
    estimatedMinutes: 16,
  },
  {
    id: 'ceiling-visualiser',
    stage: 2,
    title: 'Sub-task Ceiling Visualiser',
    valueProp: 'Watch a beautiful answer hit the ceiling and drop. Rewind to the exact sentence where the cap fired. See what 2 minutes on the missed sub-task would have done. Four cap-rule scenarios; closing pattern names the single habit that defeats all four.',
    estimatedMinutes: 10,
  },
  // ─── Stage 3 — subject-deep ────────────────────────────────────────
  {
    id: 'comparative-linker',
    stage: 3,
    title: 'Comparative Texts Linker',
    valueProp: 'English Comparative answers fail when paragraphs are about one text at a time. Build your answer point by point; watch each point either thread across all three texts or sit isolated. Six sample questions across all four modes.',
    estimatedMinutes: 18,
  },
];

interface Props {
  onOpenModule: (id: KnowledgeModuleId) => void;
}

const NecessaryKnowledge: React.FC<Props> = ({ onOpenModule }) => {
  const stage1 = TILES.filter(t => t.stage === 1);
  const stage2 = TILES.filter(t => t.stage === 2);
  const stage3 = TILES.filter(t => t.stage === 3);

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

      <StageHeader number={1} title="Foundations" subtitle="Five fundamentals every LC student should learn first." />
      <div className="grid sm:grid-cols-2 gap-3">
        {stage1.map(tile => (
          <Tile key={tile.id} tile={tile} onOpen={() => onOpenModule(tile.id)} />
        ))}
      </div>

      <StageHeader number={2} title="See marks happen" subtitle="Denser, more visual interactives. Mistake-first pedagogy — see the wrong answer, feel why it loses marks, then surface the fix." />
      <div className="grid sm:grid-cols-2 gap-3">
        {stage2.map(tile => (
          <Stage2Tile key={tile.id} tile={tile} onOpen={() => onOpenModule(tile.id)} />
        ))}
      </div>

      {stage3.length > 0 && (
        <>
          <StageHeader number={3} title="Subject deep dives" subtitle="Per-subject simulators that go where teachers can rarely reach — into the precise mechanics of how a top answer differs from a middle one." />
          <div className="grid sm:grid-cols-2 gap-3">
            {stage3.map(tile => (
              <Stage2Tile key={tile.id} tile={tile} onOpen={() => onOpenModule(tile.id)} />
            ))}
          </div>
        </>
      )}

      <ChiefExaminerCallout />
    </div>
  );
};

const StageHeader: React.FC<{ number: number; title: string; subtitle: string }> = ({ number, title, subtitle }) => (
  <div className="flex items-baseline gap-3 pt-1">
    <span
      className="font-serif shrink-0"
      style={{
        backgroundColor: TEAL,
        color: '#FFFFFF',
        borderRadius: 999,
        width: 26,
        height: 26,
        fontSize: 12,
        fontWeight: 700,
        display: 'inline-flex',
        alignItems: 'center',
        justifyContent: 'center',
      }}
    >
      {number}
    </span>
    <div>
      <p className="font-serif" style={{ fontSize: 17, fontWeight: 600, color: INK }}>
        {title}
      </p>
      <p className="font-sans" style={{ fontSize: 12.5, color: '#78716C', marginTop: 1 }}>
        {subtitle}
      </p>
    </div>
  </div>
);

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

/** Stage 2 tile — denser, bolder. Inverts on hover. */
const Stage2Tile: React.FC<{ tile: ModuleTile; onOpen: () => void }> = ({ tile, onOpen }) => (
  <button
    type="button"
    onClick={onOpen}
    className="rounded-2xl text-left transition-colors w-full"
    style={{
      backgroundColor: '#FFFFFF',
      border: `2px solid ${INK}`,
      padding: '20px 22px',
      cursor: 'pointer',
    }}
    onMouseEnter={(e) => { e.currentTarget.style.backgroundColor = INK; e.currentTarget.querySelectorAll('[data-flip]').forEach(el => { (el as HTMLElement).style.color = '#FFFFFF'; }); }}
    onMouseLeave={(e) => { e.currentTarget.style.backgroundColor = '#FFFFFF'; e.currentTarget.querySelectorAll('[data-flip]').forEach(el => { (el as HTMLElement).style.color = INK; }); }}
  >
    <div className="flex items-start justify-between gap-3 mb-2">
      <div>
        <p
          className="font-sans"
          style={{ fontSize: 9.5, fontWeight: 700, textTransform: 'uppercase', letterSpacing: 0.7, color: TEAL, marginBottom: 4 }}
        >
          Stage 2 · Interactive
        </p>
        <h3 data-flip className="font-serif" style={{ fontSize: 17, fontWeight: 600, color: INK, lineHeight: 1.25, transition: 'color 0.2s' }}>
          {tile.title}
        </h3>
      </div>
      <span
        className="font-sans shrink-0"
        style={{
          fontSize: 10,
          fontWeight: 700,
          color: '#FFFFFF',
          backgroundColor: TEAL,
          borderRadius: 999,
          padding: '3px 9px',
          whiteSpace: 'nowrap',
        }}
      >
        {tile.estimatedMinutes} min
      </span>
    </div>
    <p data-flip className="font-sans" style={{ fontSize: 12.5, color: '#3F3B36', lineHeight: 1.55, marginBottom: 14, transition: 'color 0.2s' }}>
      {tile.valueProp}
    </p>
    <span
      className="font-sans inline-flex items-center gap-1"
      style={{ fontSize: 12, fontWeight: 700, color: TEAL }}
    >
      Open the instrument panel
      <svg width="11" height="11" viewBox="0 0 12 12" fill="none" aria-hidden>
        <path d="M4 3L7 6L4 9" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round" />
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
