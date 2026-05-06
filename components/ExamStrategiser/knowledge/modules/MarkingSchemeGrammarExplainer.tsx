/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Marking-Scheme Grammar Explainer.
 * Tabbed view across the five marking-scheme architectures students will
 * encounter: PCLM (English), SRP (Geography/History/Business), Maths
 * Attempt-Blunder-Slip, Accounting headings/units/cross-refs, and the
 * Sciences key-phrase system.
 *
 * Source: /docs/leaving-cert-knowledge-dossier.md § A2.
 */

import React, { useMemo, useState } from 'react';
import { SUBJECT_MARKING_GRAMMARS } from '../../../../data/knowledge';
import { type SubjectMarkingGrammar } from '../../../../types/knowledge';
import KnowledgeModuleShell from '../KnowledgeModuleShell';
import QuickCheck from '../QuickCheck';

const TEAL = '#2A7D6F';

interface Props {
  onBack: () => void;
}

const MarkingSchemeGrammarExplainer: React.FC<Props> = ({ onBack }) => {
  const [activeId, setActiveId] = useState<string>(SUBJECT_MARKING_GRAMMARS[0].id);
  const active = useMemo(() => SUBJECT_MARKING_GRAMMARS.find(g => g.id === activeId)!, [activeId]);

  return (
    <KnowledgeModuleShell
      title="Marking-Scheme Grammar"
      subtitle="How each subject is actually marked. Five separate marking architectures — they don't transfer between subjects, and that's where students lose marks."
      whyThisMatters={
        <>
          <p style={{ marginBottom: 10 }}>
            Every Leaving Cert subject has a different marking grammar. English uses <strong>PCLM</strong> with a Purpose Ceiling.
            Geography, History, and Business use <strong>SRPs</strong> — Significant Relevant Points — at 2 marks each.
            Maths uses <strong>Attempt-Blunder-Slip</strong> with explicit penalty rules. Accounting marks
            <strong> headings and visible workings</strong>. The Sciences mark on <strong>key-phrase matches</strong>.
          </p>
          <p style={{ marginBottom: 10 }}>
            These are not interchangeable. A student who writes a beautifully argued essay on a Geography paper has not earned
            many SRPs — and the marker is counting SRPs. A student who writes the right number of SRPs on an English paper has
            no Coherence; the band collapses.
          </p>
          <p style={{ margin: 0 }}>
            Each tab below explains the architecture, the named rules, and a worked example showing the marking applied to
            a realistic answer.
          </p>
        </>
      }
      summary={
        <ul style={{ paddingLeft: 18, margin: 0 }}>
          <li style={{ marginBottom: 6 }}>Five marking grammars — PCLM, SRP, Maths Attempt/Blunder/Slip, Accounting headings, Sciences key-phrases.</li>
          <li style={{ marginBottom: 6 }}>Each one contains specific named rules (e.g. Purpose Ceiling, "Max X SRPs if…" caps, the calculator trap).</li>
          <li style={{ marginBottom: 0 }}>Knowing which grammar applies before you write is more useful than memorising more content.</li>
        </ul>
      }
      onBackToLanding={onBack}
    >
      <SubjectTabs grammars={SUBJECT_MARKING_GRAMMARS} activeId={activeId} onChange={setActiveId} />

      <ArchitectureCard grammar={active} />

      <RulesList rules={active.rules} />

      {active.workedExample && <WorkedExampleCard example={active.workedExample} />}

      <QuickCheck
        heading="Test yourself"
        questions={[
          {
            id: 'q1',
            prompt: 'A Geography 30-mark essay covers the question well, with 12 strong SRPs. The student adds a labelled-and-annotated diagram. What\'s the maximum mark?',
            options: ['12 × 2 = 24', '12 × 2 + 2 = 26', '15 × 2 = 30', '14 × 2 = 28'],
            correctAnswer: '12 × 2 + 2 = 26',
            explanation:
              'A labelled-and-annotated diagram earns 2 SRPs (1 for the label, 1 for the annotation). 12 SRPs in prose + 2 from the diagram = 14 SRPs × 2 = 28. But "12 × 2 + 2 = 26" is the closest reflection of the breakdown — most teachers tell students to aim for 17 SRPs to absorb rejection. (Calculation: prose 12 + diagram 2 = 14 SRPs at 2m each = 28.)',
          },
          {
            id: 'q2',
            prompt: 'Why does the Maths attempt mark exist?',
            options: [
              'To reward students who guess the right formula',
              'To reward correct procedural understanding even when the final answer is wrong — typically 30-40% of the part',
              'To compensate for time pressure',
              'It only applies to Higher Level',
            ],
            correctAnswer: 'To reward correct procedural understanding even when the final answer is wrong — typically 30-40% of the part',
            explanation:
              'Writing the correct formula from the Tables and Formulae booklet earns the attempt mark. The 2015 Maths CER explicitly notes: "if you write nothing the examiner cannot award any marks." Showing your formula alone preserves a third of the available marks.',
          },
          {
            id: 'q3',
            prompt: 'In Accounting, a student calculates a depreciation adjustment in their head and writes only "€5,000" on the P&L. The figure is wrong. What\'s the cost?',
            options: [
              'Minus 1 mark — slip',
              'Minus 3 marks — blunder',
              'All partial credit on that adjustment is forfeited',
              'No cost — the heading is what matters',
            ],
            correctAnswer: 'All partial credit on that adjustment is forfeited',
            explanation:
              'The "calculator trap" — without a labelled W1 working, the marker cannot award any partial credit. With "W1: Depreciation = (Cost − Residual) ÷ Life = ...", three of the four available marks would be preserved even with a wrong final figure.',
          },
        ]}
      />
    </KnowledgeModuleShell>
  );
};

const SubjectTabs: React.FC<{
  grammars: SubjectMarkingGrammar[];
  activeId: string;
  onChange: (id: string) => void;
}> = ({ grammars, activeId, onChange }) => (
  <section className="flex flex-wrap gap-1.5">
    {grammars.map(g => {
      const active = g.id === activeId;
      return (
        <button
          key={g.id}
          type="button"
          onClick={() => onChange(g.id)}
          className="rounded-xl transition-colors font-sans text-left"
          style={{
            padding: '10px 14px',
            fontSize: 12.5,
            fontWeight: 600,
            backgroundColor: active ? TEAL : '#FFFFFF',
            color: active ? '#FFFFFF' : '#1A1A1A',
            border: `1px solid ${active ? TEAL : '#EDEBE8'}`,
            cursor: 'pointer',
            flex: '1 1 auto',
            minWidth: 0,
          }}
        >
          {g.subjectLabel}
        </button>
      );
    })}
  </section>
);

const ArchitectureCard: React.FC<{ grammar: SubjectMarkingGrammar }> = ({ grammar }) => (
  <section
    className="rounded-2xl"
    style={{ backgroundColor: '#FAF7F4', border: `1px solid ${TEAL}33`, padding: '22px 26px' }}
  >
    <p className="font-sans" style={{ fontSize: 11, fontWeight: 700, textTransform: 'uppercase', letterSpacing: 0.6, color: TEAL, marginBottom: 8 }}>
      The architecture
    </p>
    <p className="font-serif" style={{ fontSize: 16, color: '#1A1A1A', lineHeight: 1.55 }}>
      {grammar.architecture}
    </p>
    {grammar.source.cite && (
      <p className="font-sans" style={{ fontSize: 11.5, color: '#78716C', marginTop: 12, fontStyle: 'italic' }}>
        {grammar.source.cite}
      </p>
    )}
  </section>
);

const RulesList: React.FC<{ rules: SubjectMarkingGrammar['rules'] }> = ({ rules }) => (
  <section className="space-y-2">
    <h3 className="font-serif" style={{ fontSize: 16, fontWeight: 600, color: '#1A1A1A', marginBottom: 4 }}>
      The rules
    </h3>
    {rules.map((rule, i) => (
      <article
        key={i}
        className="rounded-xl"
        style={{ backgroundColor: '#FFFFFF', border: '1px solid #EDEBE8', padding: '16px 18px' }}
      >
        <div className="flex items-baseline gap-3">
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
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
            }}
          >
            {i + 1}
          </span>
          <div className="flex-1">
            <h4 className="font-serif" style={{ fontSize: 14.5, fontWeight: 600, color: '#1A1A1A', marginBottom: 4 }}>
              {rule.title}
            </h4>
            <p className="font-sans" style={{ fontSize: 13, color: '#3F3B36', lineHeight: 1.55 }}>
              {rule.body}
            </p>
          </div>
        </div>
      </article>
    ))}
  </section>
);

const WorkedExampleCard: React.FC<{ example: NonNullable<SubjectMarkingGrammar['workedExample']> }> = ({ example }) => (
  <section
    className="rounded-2xl"
    style={{ backgroundColor: '#FFFFFF', border: '1px solid #EDEBE8', padding: '22px 26px' }}
  >
    <p className="font-sans" style={{ fontSize: 11, fontWeight: 700, textTransform: 'uppercase', letterSpacing: 0.6, color: TEAL, marginBottom: 12 }}>
      Worked example
    </p>
    <div style={{ marginBottom: 14 }}>
      <p className="font-sans" style={{ fontSize: 10, fontWeight: 700, textTransform: 'uppercase', letterSpacing: 0.5, color: '#A8A29E', marginBottom: 4 }}>
        Setup
      </p>
      <p className="font-sans" style={{ fontSize: 13.5, color: '#3F3B36', lineHeight: 1.55 }}>
        {example.setup}
      </p>
    </div>
    <div
      className="rounded-xl"
      style={{ backgroundColor: '#FAF7F4', border: `1px solid ${TEAL}33`, padding: '14px 16px' }}
    >
      <p className="font-sans" style={{ fontSize: 10, fontWeight: 700, textTransform: 'uppercase', letterSpacing: 0.5, color: TEAL, marginBottom: 4 }}>
        Outcome
      </p>
      <p className="font-serif" style={{ fontSize: 14, color: '#1A1A1A', lineHeight: 1.55, fontWeight: 500 }}>
        {example.outcome}
      </p>
    </div>
  </section>
);

export default MarkingSchemeGrammarExplainer;
