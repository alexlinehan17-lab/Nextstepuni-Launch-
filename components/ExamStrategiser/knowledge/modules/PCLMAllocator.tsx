/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * PCLM Allocator (E2).
 * Live demonstration of the Purpose Ceiling rule in English: the marks for
 * Coherence (C) and Language (L) cannot exceed the Purpose (P) mark.
 * Sliders show the cap applying in real time.
 *
 * Source: /docs/leaving-cert-knowledge-dossier.md § A2 (page 4) — every
 * English marking scheme verbatim.
 */

import React, { useMemo, useState } from 'react';
import KnowledgeModuleShell from '../KnowledgeModuleShell';
import QuickCheck from '../QuickCheck';

const TEAL = '#2A7D6F';

interface Props {
  onBack: () => void;
}

interface Scenario {
  id: string;
  label: string;
  description: string;
  rawP: number; // out of 30
  rawC: number;
  rawL: number;
  rawM: number; // out of 10
}

const SCENARIOS: Scenario[] = [
  {
    id: 'on-question',
    label: 'On-question, well-handled',
    description: 'A student who reads the modifier carefully and writes a coherent, controlled answer to what was actually asked.',
    rawP: 25,
    rawC: 26,
    rawL: 25,
    rawM: 9,
  },
  {
    id: 'beautiful-wrong',
    label: 'Beautiful prose, wrong question',
    description: 'A student who lifts a memorised essay onto the wrong question. The writing is accomplished, but the modifier is ignored — the killer scenario from the dossier.',
    rawP: 8,
    rawC: 28,
    rawL: 28,
    rawM: 8,
  },
  {
    id: 'on-question-rough',
    label: 'On-question, rough delivery',
    description: 'A student who engages the question fully but the structure wanders and the prose has issues. Common mid-band scenario.',
    rawP: 22,
    rawC: 16,
    rawL: 17,
    rawM: 6,
  },
  {
    id: 'partial',
    label: 'Partly on-question',
    description: 'A student who answers half the question well and drifts on the other half. Common for time-pressured candidates.',
    rawP: 18,
    rawC: 24,
    rawL: 22,
    rawM: 7,
  },
];

const PCLMAllocator: React.FC<Props> = ({ onBack }) => {
  const [p, setP] = useState(20);
  const [c, setC] = useState(20);
  const [l, setL] = useState(20);
  const [m, setM] = useState(7);
  const [activeScenario, setActiveScenario] = useState<string | null>(null);

  const cappedC = Math.min(c, p);
  const cappedL = Math.min(l, p);
  const cIsCapped = c > p;
  const lIsCapped = l > p;

  const total = p + cappedC + cappedL + m;
  const totalIfNoCeiling = p + c + l + m;
  const lostToCeiling = totalIfNoCeiling - total;

  const grade = useMemo(() => gradeFor(total), [total]);

  const applyScenario = (s: Scenario) => {
    setP(s.rawP);
    setC(s.rawC);
    setL(s.rawL);
    setM(s.rawM);
    setActiveScenario(s.id);
  };

  return (
    <KnowledgeModuleShell
      title="PCLM Allocator"
      subtitle="The Purpose Ceiling rule, in motion. Watch your Coherence and Language marks cap at your Purpose mark — the rule that catches more bright English students than any other."
      whyThisMatters={
        <>
          <p style={{ marginBottom: 10 }}>
            English marks long answers — composition, comprehension Question B, Comparative essays — across four bands: <strong>P</strong> (Purpose, 30%),
            <strong> C</strong> (Coherence, 30%), <strong>L</strong> (Language, 30%), <strong>M</strong> (Mechanics, 10%).
          </p>
          <p style={{ marginBottom: 10 }}>
            Every English marking scheme contains the same line: <em>"Marks for C or L cannot exceed the marks for P."</em>
            This is the <strong>Purpose Ceiling</strong>. It is the rule that catches strong writers who answer the wrong question.
          </p>
          <p style={{ margin: 0 }}>
            A beautifully crafted essay on the wrong topic — flawless structure, vivid prose — caps at the Purpose mark.
            That can be a 32% answer with sentences that, alone, would score 90%. Move the sliders below to feel why.
          </p>
        </>
      }
      summary={
        <ul style={{ paddingLeft: 18, margin: 0 }}>
          <li style={{ marginBottom: 6 }}>P, C, L are each worth 30%; M is worth 10%. P caps both C and L.</li>
          <li style={{ marginBottom: 6 }}>An off-question essay caps at the P mark, no matter how well it's written.</li>
          <li style={{ marginBottom: 0 }}>Time spent making sure you've answered the actual modifier is the highest-leverage 60 seconds you spend on Paper 2.</li>
        </ul>
      }
      onBackToLanding={onBack}
    >
      <SliderPanel
        p={p}
        c={c}
        l={l}
        m={m}
        cappedC={cappedC}
        cappedL={cappedL}
        cIsCapped={cIsCapped}
        lIsCapped={lIsCapped}
        onP={(v) => { setP(v); setActiveScenario(null); }}
        onC={(v) => { setC(v); setActiveScenario(null); }}
        onL={(v) => { setL(v); setActiveScenario(null); }}
        onM={(v) => { setM(v); setActiveScenario(null); }}
      />

      <ResultPanel
        total={total}
        lostToCeiling={lostToCeiling}
        grade={grade}
        cIsCapped={cIsCapped}
        lIsCapped={lIsCapped}
      />

      <ScenarioPanel scenarios={SCENARIOS} activeId={activeScenario} onSelect={applyScenario} />

      <QuickCheck
        heading="Test yourself"
        questions={[
          {
            id: 'q1',
            prompt: 'A student writes a flawless personal essay. The question asked for a discursive essay. Marks: P=8, C=27, L=27, M=9. What is the final total (out of 100)?',
            options: ['71', '32', '54', '71 — but capped at 60'],
            correctAnswer: '32',
            explanation:
              'C caps at 8 and L caps at 8 (both at P). Final: 8 + 8 + 8 + 8 = 32. The genre mismatch is a Purpose failure — beautiful prose on the wrong question scores around a third.',
          },
          {
            id: 'q2',
            prompt: 'Why does the Purpose Ceiling exist in the marking scheme?',
            options: [
              'To penalise weak handwriting',
              'To stop a memorised essay scoring as if it answered the question',
              'To mark long answers more quickly',
              'To reward students who write more',
            ],
            correctAnswer: 'To stop a memorised essay scoring as if it answered the question',
            explanation:
              'The ceiling is the structural defence against rote-learned essays. The 2013 English Chief Examiner explicitly named "over-rehearsed formulaic" essays as the most-flagged failure pattern.',
          },
          {
            id: 'q3',
            prompt: 'P=24, C=15, L=15, M=8. What is the total — and what does the C+L score tell you?',
            options: [
              '62 — Purpose is ceiling-blocked',
              '62 — engagement was strong, but execution wandered',
              '62 — Mechanics dragged the answer down',
              '62 — Coherence and Language caps applied',
            ],
            correctAnswer: '62 — engagement was strong, but execution wandered',
            explanation:
              'Total = 24 + 15 + 15 + 8 = 62. Here C and L are below P, so no cap fires — the limiting factor is execution, not engagement. This profile is the opposite of the killer scenario.',
          },
        ]}
      />
    </KnowledgeModuleShell>
  );
};

const SliderPanel: React.FC<{
  p: number; c: number; l: number; m: number;
  cappedC: number; cappedL: number;
  cIsCapped: boolean; lIsCapped: boolean;
  onP: (v: number) => void; onC: (v: number) => void; onL: (v: number) => void; onM: (v: number) => void;
}> = ({ p, c, l, m, cappedC, cappedL, cIsCapped, lIsCapped, onP, onC, onL, onM }) => (
  <section
    className="rounded-2xl"
    style={{ backgroundColor: '#FFFFFF', border: '1px solid #EDEBE8', padding: '24px 26px' }}
  >
    <p className="font-sans" style={{ fontSize: 11, fontWeight: 700, textTransform: 'uppercase', letterSpacing: 0.6, color: TEAL, marginBottom: 4 }}>
      Set the marks
    </p>
    <p className="font-sans" style={{ fontSize: 12.5, color: '#78716C', marginBottom: 18, lineHeight: 1.5 }}>
      Each band is marked out of 30 (M is out of 10). Move the sliders to see the Purpose Ceiling apply.
    </p>
    <div className="space-y-5">
      <SliderRow letter="P" name="Purpose" max={30} value={p} onChange={onP} description="Engagement with the actual task asked." />
      <SliderRow
        letter="C"
        name="Coherence"
        max={30}
        value={c}
        onChange={onC}
        description="Logical structure and sustained argument."
        capped={cIsCapped ? cappedC : null}
      />
      <SliderRow
        letter="L"
        name="Language"
        max={30}
        value={l}
        onChange={onL}
        description="Genre-appropriate, controlled language."
        capped={lIsCapped ? cappedL : null}
      />
      <SliderRow letter="M" name="Mechanics" max={10} value={m} onChange={onM} description="Spelling, grammar, punctuation. Strict." />
    </div>
  </section>
);

const SliderRow: React.FC<{
  letter: string;
  name: string;
  max: number;
  value: number;
  onChange: (v: number) => void;
  description: string;
  capped?: number | null;
}> = ({ letter, name, max, value, onChange, description, capped }) => (
  <div>
    <div className="flex items-baseline justify-between gap-3 mb-1.5">
      <div>
        <span className="font-serif" style={{ fontSize: 16, fontWeight: 700, color: '#1A1A1A', marginRight: 8 }}>
          {letter}
        </span>
        <span className="font-sans" style={{ fontSize: 12.5, color: '#3F3B36', fontWeight: 600 }}>
          {name}
        </span>
        <span className="font-sans" style={{ fontSize: 11.5, color: '#A8A29E', marginLeft: 6 }}>
          / {max}
        </span>
      </div>
      <div className="font-serif flex items-baseline gap-2">
        {capped !== null && capped !== undefined ? (
          <>
            <span style={{ fontSize: 13, color: '#A8A29E', textDecoration: 'line-through' }}>{value}</span>
            <span style={{ fontSize: 18, fontWeight: 700, color: TEAL }}>{capped}</span>
            <span className="font-sans" style={{ fontSize: 10, fontWeight: 700, textTransform: 'uppercase', letterSpacing: 0.5, color: '#A8746E' }}>
              capped
            </span>
          </>
        ) : (
          <span style={{ fontSize: 18, fontWeight: 700, color: TEAL }}>{value}</span>
        )}
      </div>
    </div>
    <input
      type="range"
      min={0}
      max={max}
      value={value}
      onChange={(e) => onChange(Number(e.target.value))}
      className="w-full"
      style={{ accentColor: TEAL }}
    />
    <p className="font-sans" style={{ fontSize: 11.5, color: '#78716C', marginTop: 4 }}>
      {description}
    </p>
  </div>
);

const ResultPanel: React.FC<{
  total: number;
  lostToCeiling: number;
  grade: string;
  cIsCapped: boolean;
  lIsCapped: boolean;
}> = ({ total, lostToCeiling, grade, cIsCapped, lIsCapped }) => {
  const ceilingFired = cIsCapped || lIsCapped;
  return (
    <section
      className="rounded-2xl"
      style={{ backgroundColor: '#FAF7F4', border: `1px solid ${TEAL}33`, padding: '22px 26px' }}
    >
      <div className="flex items-baseline justify-between gap-4 flex-wrap">
        <div>
          <p className="font-sans" style={{ fontSize: 11, fontWeight: 700, textTransform: 'uppercase', letterSpacing: 0.6, color: TEAL, marginBottom: 4 }}>
            Final mark
          </p>
          <div className="flex items-baseline gap-3">
            <span className="font-serif" style={{ fontSize: 38, fontWeight: 700, color: '#1A1A1A' }}>
              {total}
              <span style={{ fontSize: 18, color: '#78716C', fontWeight: 500 }}> / 100</span>
            </span>
            <span className="font-sans" style={{ fontSize: 13, fontWeight: 700, color: TEAL, backgroundColor: '#FFFFFF', border: `1px solid ${TEAL}55`, padding: '4px 10px', borderRadius: 999 }}>
              {grade}
            </span>
          </div>
        </div>
        {ceilingFired && (
          <div style={{ textAlign: 'right' }}>
            <p className="font-sans" style={{ fontSize: 10, fontWeight: 700, textTransform: 'uppercase', letterSpacing: 0.5, color: '#A8746E', marginBottom: 2 }}>
              Lost to the ceiling
            </p>
            <p className="font-serif" style={{ fontSize: 22, fontWeight: 700, color: '#1A1A1A' }}>
              − {lostToCeiling}
            </p>
          </div>
        )}
      </div>
      {ceilingFired && (
        <p className="font-sans" style={{ fontSize: 13, color: '#3F3B36', marginTop: 14, lineHeight: 1.55 }}>
          The Purpose Ceiling has fired. The C and / or L marks have been capped at the Purpose mark — losing <strong>{lostToCeiling}</strong> marks of brilliantly executed but off-question work.
        </p>
      )}
    </section>
  );
};

const ScenarioPanel: React.FC<{
  scenarios: Scenario[];
  activeId: string | null;
  onSelect: (s: Scenario) => void;
}> = ({ scenarios, activeId, onSelect }) => (
  <section className="space-y-3">
    <div>
      <h3 className="font-serif" style={{ fontSize: 16, fontWeight: 600, color: '#1A1A1A', marginBottom: 4 }}>
        Try a real scenario
      </h3>
      <p className="font-sans" style={{ fontSize: 12.5, color: '#78716C' }}>
        Each scenario applies a real grade pattern from English Chief Examiner Reports.
      </p>
    </div>
    <div className="grid sm:grid-cols-2 gap-2">
      {scenarios.map(s => {
        const active = activeId === s.id;
        return (
          <button
            key={s.id}
            type="button"
            onClick={() => onSelect(s)}
            className="text-left rounded-xl transition-colors"
            style={{
              backgroundColor: active ? '#FAF7F4' : '#FFFFFF',
              border: `1px solid ${active ? `${TEAL}66` : '#EDEBE8'}`,
              padding: '14px 16px',
              cursor: 'pointer',
            }}
          >
            <p className="font-serif" style={{ fontSize: 14, fontWeight: 600, color: '#1A1A1A', marginBottom: 4 }}>
              {s.label}
            </p>
            <p className="font-sans" style={{ fontSize: 12, color: '#78716C', lineHeight: 1.5 }}>
              {s.description}
            </p>
          </button>
        );
      })}
    </div>
  </section>
);

function gradeFor(percent: number): string {
  if (percent >= 90) return 'H1';
  if (percent >= 80) return 'H2';
  if (percent >= 70) return 'H3';
  if (percent >= 60) return 'H4';
  if (percent >= 50) return 'H5';
  if (percent >= 40) return 'H6';
  if (percent >= 30) return 'H7';
  return 'H8';
}

export default PCLMAllocator;
