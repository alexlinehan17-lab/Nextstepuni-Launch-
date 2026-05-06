/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Examiner Pet-Peeve Trainer (E12).
 * Card stack of the perennial 12 complaints that recur in Chief Examiner
 * Reports year after year. For each: the peeve, a worked example of what
 * triggers it, and the specific fix.
 *
 * Source: /docs/leaving-cert-knowledge-dossier.md § B1-B11 + § D.
 */

import React, { useMemo, useState } from 'react';
import { EXAMINER_PET_PEEVES } from '../../../../data/knowledge';
import { type ExaminerPetPeeve } from '../../../../types/knowledge';
import KnowledgeModuleShell from '../KnowledgeModuleShell';
import QuickCheck from '../QuickCheck';

const TEAL = '#2A7D6F';

interface Props {
  onBack: () => void;
}

const ExaminerPetPeeveTrainer: React.FC<Props> = ({ onBack }) => {
  const subjects = useMemo(() => {
    const set = new Set<string>();
    EXAMINER_PET_PEEVES.forEach(p => set.add(p.subject));
    return ['All', ...Array.from(set)];
  }, []);

  const [filter, setFilter] = useState<string>('All');
  const [revealed, setRevealed] = useState<Set<string>>(new Set());

  const filtered = useMemo(() => {
    if (filter === 'All') return EXAMINER_PET_PEEVES;
    return EXAMINER_PET_PEEVES.filter(p => p.subject === filter);
  }, [filter]);

  const toggle = (id: string) => {
    setRevealed(prev => {
      const next = new Set(prev);
      if (next.has(id)) next.delete(id); else next.add(id);
      return next;
    });
  };

  const revealAll = () => setRevealed(new Set(EXAMINER_PET_PEEVES.map(p => p.id)));
  const collapseAll = () => setRevealed(new Set());

  return (
    <KnowledgeModuleShell
      title="Examiner Pet-Peeve Trainer"
      subtitle="The same complaints every Chief Examiner Report makes, year after year. The perennial twelve, with the fix for each."
      whyThisMatters={
        <>
          <p style={{ marginBottom: 10 }}>
            Chief Examiners' Reports are a public catalogue of what bright students keep getting wrong.
            Read across 20 years and the same complaints repeat: <em>over-rehearsed essays</em>, <em>working not shown in Maths</em>,
            <em>ABQ answers without case-study quotes</em>, <em>Comparative essays treated serially</em>.
          </p>
          <p style={{ marginBottom: 10 }}>
            These aren't subject-specific. They're <strong>structural failure modes</strong> that the marking schemes are
            engineered to catch. Each one corresponds to a specific cap, deduction, or failure-band the scheme will apply.
          </p>
          <p style={{ margin: 0 }}>
            The fastest grade gain on any paper isn't more content — it's eliminating the perennial twelve from your work.
            Tap each card to see the specific failure pattern and the single behaviour that fixes it.
          </p>
        </>
      }
      summary={
        <ul style={{ paddingLeft: 18, margin: 0 }}>
          <li style={{ marginBottom: 6 }}>The perennial complaints aren't subject-specific — they're structural patterns that show up across every CER.</li>
          <li style={{ marginBottom: 6 }}>Each peeve maps to a specific marking-scheme rule that catches it (cap, deduction, or band ceiling).</li>
          <li style={{ marginBottom: 0 }}>Fixing one peeve typically lifts the corresponding question by half a grade.</li>
        </ul>
      }
      onBackToLanding={onBack}
    >
      <FilterBar subjects={subjects} active={filter} onChange={setFilter} onRevealAll={revealAll} onCollapseAll={collapseAll} />

      <div className="space-y-2">
        {filtered.map(p => (
          <PeeveCard
            key={p.id}
            peeve={p}
            revealed={revealed.has(p.id)}
            onToggle={() => toggle(p.id)}
          />
        ))}
      </div>

      <QuickCheck
        heading="Spot the peeve"
        questions={[
          {
            id: 'q1',
            prompt: 'A Maths student writes only "x = 4" with no working — the answer is wrong. Which peeve is this, and what is the cost?',
            options: [
              'Force-given-answer — caps at attempt mark',
              'Working not shown — loses 30-40% partial credit available from the formula and substitution',
              'Slip — minus 1 mark',
              'No-attempt — scores 0 only on that line',
            ],
            correctAnswer: 'Working not shown — loses 30-40% partial credit available from the formula and substitution',
            explanation:
              'Writing the formula alone earns the attempt mark — typically 30-40% of the part. The 2015 Maths CER explicitly notes "if you write nothing the examiner cannot award any marks." Showing working preserves credit even when the final figure is wrong.',
          },
          {
            id: 'q2',
            prompt: 'In a Business ABQ, a student explains demographic segmentation and applies it generally to the case study, but never quotes a specific phrase from the text. What\'s the issue?',
            options: [
              'Theory is missing',
              'Application is missing',
              'The link mark requires a direct quote — without it, the marker can\'t award it',
              'It\'s only 1 mark — not significant',
            ],
            correctAnswer: 'The link mark requires a direct quote — without it, the marker can\'t award it',
            explanation:
              '2025 Business HL marking schemes explicitly require a direct case-study quote per ABQ point. Theory + Explanation + "Quote in inverted commas" — without all three, the link mark is forfeited.',
          },
          {
            id: 'q3',
            prompt: 'A Comparative essay covers all of Text A, then all of Text B, then all of Text C. Each text gets 5+ pages. What does the English Chief Examiner say about this?',
            options: [
              '"Best answers were written in an analytical fashion" — meaning integrated comparison',
              'Long answers always score better',
              'Coverage is what matters, not integration',
              'The marking scheme rewards depth over breadth',
            ],
            correctAnswer: '"Best answers were written in an analytical fashion" — meaning integrated comparison',
            explanation:
              'Serial coverage caps the answer mid-band. The CER\'s phrase "analytical fashion" means each paragraph integrates both texts: "Both X and Y deal with Z; in Text A this manifests as..., whereas in Text B...".',
          },
        ]}
      />
    </KnowledgeModuleShell>
  );
};

const FilterBar: React.FC<{
  subjects: string[];
  active: string;
  onChange: (s: string) => void;
  onRevealAll: () => void;
  onCollapseAll: () => void;
}> = ({ subjects, active, onChange, onRevealAll, onCollapseAll }) => (
  <section className="space-y-3">
    <div className="flex flex-wrap items-center gap-2">
      {subjects.map(s => {
        const isActive = s === active;
        return (
          <button
            key={s}
            type="button"
            onClick={() => onChange(s)}
            className="rounded-full transition-colors font-sans"
            style={{
              padding: '6px 14px',
              fontSize: 12,
              fontWeight: 600,
              backgroundColor: isActive ? TEAL : '#FFFFFF',
              color: isActive ? '#FFFFFF' : '#3F3B36',
              border: `1px solid ${isActive ? TEAL : '#EDEBE8'}`,
              cursor: 'pointer',
            }}
          >
            {s}
          </button>
        );
      })}
      <div className="ml-auto flex items-center gap-3">
        <button
          type="button"
          onClick={onRevealAll}
          className="font-sans"
          style={{ fontSize: 12, color: TEAL, background: 'transparent', border: 'none', padding: 0, cursor: 'pointer', fontWeight: 600 }}
        >
          Reveal all
        </button>
        <button
          type="button"
          onClick={onCollapseAll}
          className="font-sans"
          style={{ fontSize: 12, color: '#78716C', background: 'transparent', border: 'none', padding: 0, cursor: 'pointer' }}
        >
          Collapse all
        </button>
      </div>
    </div>
  </section>
);

const PeeveCard: React.FC<{
  peeve: ExaminerPetPeeve;
  revealed: boolean;
  onToggle: () => void;
}> = ({ peeve, revealed, onToggle }) => (
  <article
    className="rounded-2xl"
    style={{
      backgroundColor: revealed ? '#FAF7F4' : '#FFFFFF',
      border: `1px solid ${revealed ? `${TEAL}55` : '#EDEBE8'}`,
      transition: 'background-color 200ms ease, border-color 200ms ease',
    }}
  >
    <button
      type="button"
      onClick={onToggle}
      className="w-full text-left"
      style={{ background: 'transparent', border: 'none', padding: '18px 22px', cursor: 'pointer' }}
      aria-expanded={revealed}
    >
      <div className="flex items-start justify-between gap-3">
        <div className="flex-1">
          <div className="flex items-baseline gap-2 mb-1.5 flex-wrap">
            <span
              className="font-sans"
              style={{
                fontSize: 10,
                fontWeight: 700,
                textTransform: 'uppercase',
                letterSpacing: 0.5,
                color: TEAL,
                backgroundColor: '#FFFFFF',
                border: `1px solid ${TEAL}33`,
                borderRadius: 999,
                padding: '2px 8px',
              }}
            >
              {peeve.subject}
            </span>
            <span className="font-sans" style={{ fontSize: 11, color: '#A8A29E' }}>
              CER {peeve.reportYear}
            </span>
          </div>
          <p className="font-serif" style={{ fontSize: 15, fontWeight: 600, color: '#1A1A1A', lineHeight: 1.4 }}>
            {peeve.peeve}
          </p>
        </div>
        <svg
          width="14"
          height="14"
          viewBox="0 0 12 12"
          fill="none"
          aria-hidden
          style={{
            color: '#78716C',
            transform: revealed ? 'rotate(180deg)' : 'rotate(0deg)',
            transition: 'transform 200ms ease',
            marginTop: 4,
          }}
        >
          <path d="M3 4.5L6 7.5L9 4.5" stroke="currentColor" strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round" />
        </svg>
      </div>
    </button>

    {revealed && (
      <div style={{ padding: '0 22px 20px 22px' }}>
        <div style={{ borderTop: '1px solid #EDEBE8', paddingTop: 14 }}>
          <DetailBlock label="What triggers it" body={peeve.example} />
          <DetailBlock label="The fix" body={peeve.fix} highlight />
          {peeve.source.cite && (
            <p className="font-sans" style={{ fontSize: 11.5, color: '#78716C', marginTop: 10, fontStyle: 'italic' }}>
              {peeve.source.cite}
            </p>
          )}
        </div>
      </div>
    )}
  </article>
);

const DetailBlock: React.FC<{ label: string; body: string; highlight?: boolean }> = ({ label, body, highlight }) => (
  <div style={{ marginTop: 4, marginBottom: 10 }}>
    <p className="font-sans" style={{ fontSize: 10, fontWeight: 700, textTransform: 'uppercase', letterSpacing: 0.5, color: highlight ? TEAL : '#A8A29E', marginBottom: 4 }}>
      {label}
    </p>
    <p className="font-sans" style={{ fontSize: 13, color: highlight ? '#1A1A1A' : '#3F3B36', lineHeight: 1.55 }}>
      {body}
    </p>
  </div>
);

export default ExaminerPetPeeveTrainer;
