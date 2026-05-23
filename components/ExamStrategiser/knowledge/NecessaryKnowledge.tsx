/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Necessary Knowledge — tab landing.
 *
 * Hero, three module groups (Foundations / Tools / Subject Deep Dives),
 * a "Your patterns" panel that surfaces cross-module insights from
 * localStorage signals, and a closing Chief Examiner Report quote that
 * frames the whole tab's thesis.
 *
 * Stage 1 (Foundations) modules use the quieter Strategiser register.
 * Stage 2 (Tools) and Stage 3 (Subject Deep Dives) modules use the
 * bolder Brilliant.org / Mercury hybrid register — denser and more
 * instrument-panel-like.
 *
 * Source of truth for content: /docs/leaving-cert-knowledge-dossier.md.
 * Every claim here traces to that file.
 */

import React from 'react';
import YourPatternsContainer, { type KnowledgeModuleId } from './YourPatternsContainer';
import { ACCENT, ACCENT_TINT } from '../colors';

const INK = '#1a1a1a';

export type { KnowledgeModuleId };

type Stage = 1 | 2 | 3;

interface ModuleTile {
  id: KnowledgeModuleId;
  stage: Stage;
  title: string;
  valueProp: string;
  estimatedMinutes: number;
  /** Subject label shown as a kicker on Stage 3 rows. */
  subject?: string;
}

const TILES: ModuleTile[] = [
  // ─── Stage 1 ────────────────────────────────────────────────────────
  {
    id: 'command-words',
    stage: 1,
    title: 'Command Word Decoder',
    valueProp: 'Read any LC question the way an examiner does.',
    estimatedMinutes: 8,
  },
  {
    id: 'pclm',
    stage: 1,
    title: 'PCLM Allocator',
    valueProp: 'Why brilliant English answers still get capped at Purpose.',
    estimatedMinutes: 6,
  },
  {
    id: 'time-allocation',
    stage: 1,
    title: 'Time-Allocation Calculator',
    valueProp: 'Per-mark timing plus a sunk-cost simulator.',
    estimatedMinutes: 7,
  },
  {
    id: 'pet-peeves',
    stage: 1,
    title: 'Examiner Pet-Peeve Trainer',
    valueProp: 'The same twelve complaints every CER makes — and the fix.',
    estimatedMinutes: 10,
  },
  {
    id: 'marking-grammar',
    stage: 1,
    title: 'Marking-Scheme Grammar',
    valueProp: 'How each subject is actually marked.',
    estimatedMinutes: 9,
  },
  // ─── Stage 2 ────────────────────────────────────────────────────────
  {
    id: 'srp-identifier',
    stage: 2,
    title: 'SRP Identifier',
    valueProp: 'Read a paragraph like an examiner. Watch the marks land.',
    estimatedMinutes: 12,
  },
  {
    id: 'working-shown',
    stage: 2,
    title: 'Working-Shown Allocator',
    valueProp: 'Mark ribbons land beside every step you write.',
    estimatedMinutes: 14,
  },
  {
    id: 'sanity-check',
    stage: 2,
    title: 'Sanity-Check Trainer',
    valueProp: 'Catch the absurd answer before you write it down.',
    estimatedMinutes: 12,
  },
  {
    id: 'spot-the-trap',
    stage: 2,
    title: 'Spot the Trap',
    valueProp: 'Thirty seconds to spot it. Pattern map at the end.',
    estimatedMinutes: 16,
  },
  {
    id: 'ceiling-visualiser',
    stage: 2,
    title: 'Sub-task Ceiling Visualiser',
    valueProp: 'Watch a top answer hit the ceiling and drop.',
    estimatedMinutes: 10,
  },
  // ─── Stage 3 — subject-deep ────────────────────────────────────────
  {
    id: 'comparative-linker',
    stage: 3,
    subject: 'English',
    title: 'Comparative Texts Linker',
    valueProp: 'Build comparative answers that actually integrate.',
    estimatedMinutes: 18,
  },
  {
    id: 'rsr-allocator',
    stage: 3,
    subject: 'History',
    title: 'RSR Section Allocator',
    valueProp: 'Word-budget every section of the Research Study Report.',
    estimatedMinutes: 16,
  },
  {
    id: 'phrase-match',
    stage: 3,
    subject: 'Sciences',
    title: 'Phrase Match Petri-Dish',
    valueProp: 'Hit the marking scheme’s exact key phrases.',
    estimatedMinutes: 14,
  },
  {
    id: 'oral-coach',
    stage: 3,
    subject: 'Languages',
    title: 'Oral Authenticity Coach',
    valueProp: 'Detect rote, monotony, and missing personalisation.',
    estimatedMinutes: 18,
  },
];

function stageMeta(tiles: ModuleTile[]): string {
  return `${tiles.length} tool${tiles.length === 1 ? '' : 's'}`;
}

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

      <YourPatternsContainer onOpenModule={onOpenModule} />

      <StageSection
        kicker="Foundations"
        title="Learn the marking grammar."
        subtitle="The fundamentals every LC student should learn first. Command words, marking-scheme architecture, time per mark, perennial examiner peeves."
        meta={stageMeta(stage1)}
        tiles={stage1}
        onOpenModule={onOpenModule}
      />

      <StageSection
        kicker="Tools"
        title="See the marks happen."
        subtitle="Mistake-first interactives — see the wrong answer, feel why it loses marks, surface the fix."
        meta={stageMeta(stage2)}
        tiles={stage2}
        onOpenModule={onOpenModule}
      />

      {stage3.length > 0 && (
        <StageSection
          kicker="Subject deep dives"
          title="Where a top answer separates from a middle one."
          subtitle="Per-subject simulators that go where teachers can rarely reach."
          meta={stageMeta(stage3)}
          tiles={stage3}
          onOpenModule={onOpenModule}
        />
      )}

      <ChiefExaminerCallout />
    </div>
  );
};

/** Stage block — uppercase teal kicker (kicker · count), serif title,
 *  muted subtitle, then the tool rows. No numbered chrome — vertical
 *  whitespace and kicker text do the section punctuation. */
const StageSection: React.FC<{
  kicker: string;
  title: string;
  subtitle: string;
  meta: string;
  tiles: ModuleTile[];
  onOpenModule: (id: KnowledgeModuleId) => void;
}> = ({ kicker, title, subtitle, meta, tiles, onOpenModule }) => (
  <section className="space-y-3">
    <div className="pt-2">
      <p className="font-sans" style={{ fontSize: 10, fontWeight: 700, textTransform: 'uppercase', letterSpacing: 0.6, color: ACCENT }}>
        {kicker}
        <span style={{ color: '#D6D2CC', margin: '0 6px' }}>·</span>
        <span style={{ color: '#A8A29E' }}>{meta}</span>
      </p>
      <p className="font-serif" style={{ fontSize: 18, fontWeight: 600, color: INK, marginTop: 4, lineHeight: 1.3 }}>
        {title}
      </p>
      <p className="font-sans max-w-2xl" style={{ fontSize: 12.5, color: '#5a5550', marginTop: 4, lineHeight: 1.55 }}>
        {subtitle}
      </p>
    </div>
    <div className="space-y-2">
      {tiles.map(tile => (
        <ModuleRow key={tile.id} tile={tile} onOpen={() => onOpenModule(tile.id)} />
      ))}
    </div>
  </section>
);

/** Tool row — light Strategiser register, matches QuestionList rows.
 *  Cream hover, animated chevron. Stage 3 rows carry a subject kicker;
 *  Stage 1/2 rows lead with the title. */
const ModuleRow: React.FC<{ tile: ModuleTile; onOpen: () => void }> = ({ tile, onOpen }) => (
  <button
    type="button"
    onClick={onOpen}
    className="w-full text-left rounded-xl transition-colors group"
    style={{
      backgroundColor: '#FFFFFF',
      border: '1px solid #EDEBE8',
      padding: '14px 18px',
      cursor: 'pointer',
    }}
    onMouseEnter={(e) => { e.currentTarget.style.backgroundColor = ACCENT_TINT; }}
    onMouseLeave={(e) => { e.currentTarget.style.backgroundColor = '#FFFFFF'; }}
  >
    <div className="flex items-center gap-3">
      <div className="flex-1 min-w-0">
        {tile.subject && (
          <p className="font-sans" style={{ fontSize: 10, fontWeight: 700, textTransform: 'uppercase', letterSpacing: 0.6, color: ACCENT, marginBottom: 3 }}>
            {tile.subject}
          </p>
        )}
        <p className="font-serif" style={{ fontSize: 15.5, fontWeight: 600, color: INK, lineHeight: 1.3 }}>
          {tile.title}
        </p>
        <p className="font-sans" style={{ fontSize: 12.5, color: '#78716C', marginTop: 3, lineHeight: 1.5 }}>
          {tile.valueProp}
        </p>
      </div>
      <svg
        width="16"
        height="16"
        viewBox="0 0 16 16"
        fill="none"
        aria-hidden
        className="transition-transform group-hover:translate-x-0.5 shrink-0"
        style={{ color: '#A8A29E' }}
      >
        <path d="M6 4L10 8L6 12" stroke="currentColor" strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round" />
      </svg>
    </div>
  </button>
);

/** Closing CER quote to frame the tab's thesis. Drawn from dossier § B1
 *  (English CER 2013) — the line the entire "exam technique > content"
 *  argument rests on. */
const ChiefExaminerCallout: React.FC = () => (
  <section
    className="rounded-2xl"
    style={{
      backgroundColor: ACCENT_TINT,
      border: `1px solid ${ACCENT}33`,
      padding: '22px 26px',
    }}
  >
    <p className="font-sans" style={{ fontSize: 10, fontWeight: 700, textTransform: 'uppercase', letterSpacing: 0.6, color: ACCENT, marginBottom: 8 }}>
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
