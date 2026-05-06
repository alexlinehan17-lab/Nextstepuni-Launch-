/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Time-Allocation Calculator (E3).
 * Per-mark timing for every paper. Includes a sunk-cost simulator showing
 * why a part-answer to all required questions beats a perfect answer to
 * fewer.
 *
 * Source: /docs/leaving-cert-knowledge-dossier.md § A3 (page 6) and the
 * arithmetic on the per-mark rate per subject.
 */

import React, { useMemo, useState } from 'react';
import { SUBJECT_TIMING } from '../../../../data/knowledge';
import { type SubjectTiming } from '../../../../types/knowledge';
import KnowledgeModuleShell from '../KnowledgeModuleShell';
import QuickCheck from '../QuickCheck';

const TEAL = '#2A7D6F';

interface Props {
  onBack: () => void;
}

const TimeAllocationCalculator: React.FC<Props> = ({ onBack }) => {
  const [subjectId, setSubjectId] = useState<string>(SUBJECT_TIMING[0].id);
  const subject = useMemo(() => SUBJECT_TIMING.find(s => s.id === subjectId)!, [subjectId]);

  const minPerMark = subject.totalMinutes / subject.totalMarks;
  const secPerMark = Math.round(minPerMark * 60);

  return (
    <KnowledgeModuleShell
      title="Time-Allocation Calculator"
      subtitle="Per-mark timing for every paper. Plus a sunk-cost simulator showing why a part-answer to every required question beats a perfect answer to fewer."
      whyThisMatters={
        <>
          <p style={{ marginBottom: 10 }}>
            Every Leaving Cert paper has a different per-mark time budget. Geography gives you 25.5 seconds per mark.
            Accounting gives you 27 seconds — the fastest-paced LC paper. Maths gives you 30. Knowing your rate is
            the single most important time-management number you'll learn this year.
          </p>
          <p style={{ marginBottom: 10 }}>
            But the harder lesson is the <strong>sunk-cost trap</strong>: a perfect 50-mark answer scores at most 50.
            Two attempted 30-mark questions, even at half quality, score 30. <em>Diminishing returns vs. zero returns</em>
            — past around 80% on a single question, every extra minute gives you less than what the unanswered question would have given you.
          </p>
          <p style={{ margin: 0 }}>
            The 2012 Geography Chief Examiner specifically flagged time over-runs on short questions as the most common
            grade-killer. Use a watch. Set hard cuts. The sim below shows you why.
          </p>
        </>
      }
      summary={
        <ul style={{ paddingLeft: 18, margin: 0 }}>
          <li style={{ marginBottom: 6 }}>Each LC paper has a published per-mark rate — Accounting is 27 seconds, Maths is 30, English Paper 1 is 51 seconds.</li>
          <li style={{ marginBottom: 6 }}>The sunk-cost trap kills more grades than poor content: a perfect answer to 4 questions scores below an OK answer to 5.</li>
          <li style={{ marginBottom: 0 }}>Plan time per question before you start, not when the bell rings.</li>
        </ul>
      }
      onBackToLanding={onBack}
    >
      <SubjectPickerCard
        subjectId={subjectId}
        onChange={setSubjectId}
      />

      <PerMarkRateCard subject={subject} minPerMark={minPerMark} secPerMark={secPerMark} />

      <BreakdownTable subject={subject} minPerMark={minPerMark} />

      <SunkCostSimulator />

      <QuickCheck
        heading="Test yourself"
        questions={[
          {
            id: 'q1',
            prompt: 'Accounting Higher gives you 0.45 minutes per mark — 27 seconds. A 60-mark adjustment question should take how long, including planning?',
            options: ['~15 minutes', '~27 minutes', '~45 minutes', '~60 minutes'],
            correctAnswer: '~27 minutes',
            explanation:
              '60 marks × 27 seconds = 1,620 seconds = 27 minutes. Going over by 5 minutes here means a Section 3 management-accounting question loses 5 minutes — the highest-rate trade in the paper.',
          },
          {
            id: 'q2',
            prompt: 'You have one Geography long question left and 25 minutes remaining. Should you (A) write a perfect 25-minute answer to one 80-mark question, or (B) split — 15 mins on the leftover question, 10 mins racing through it and your unanswered Section 5 option?',
            options: [
              'A — perfect one is always worth more',
              'B — partial answers to both score more',
              'A — leave Section 5 blank, focus quality',
              'B but only at Higher Level',
            ],
            correctAnswer: 'B — partial answers to both score more',
            explanation:
              'A perfect 80-mark answer scores 80. A 60% answer to one + 30% to the other scores ~48 + ~24 = 72 — but if you don\'t attempt the second, that\'s 80 vs. 50. Below ~70%, partial > perfect.',
          },
          {
            id: 'q3',
            prompt: 'Why is the per-mark rate a more useful planning number than the per-question time?',
            options: [
              'It is easier to remember',
              'Different sections often weight question types differently — a 60-mark question and a 20-mark question both deserve their own budget',
              'Markers prefer it',
              'It is what the marking scheme uses',
            ],
            correctAnswer: 'Different sections often weight question types differently — a 60-mark question and a 20-mark question both deserve their own budget',
            explanation:
              'A flat "10 minutes per question" gives a 10-mark short question the same time as a 60-mark long. Per-mark rate scales naturally to whatever the question is worth.',
          },
        ]}
      />
    </KnowledgeModuleShell>
  );
};

const SubjectPickerCard: React.FC<{
  subjectId: string;
  onChange: (id: string) => void;
}> = ({ subjectId, onChange }) => (
  <section
    className="rounded-2xl"
    style={{ backgroundColor: '#FFFFFF', border: '1px solid #EDEBE8', padding: '20px 24px' }}
  >
    <label htmlFor="ta-subject" className="font-sans block" style={{ fontSize: 11, fontWeight: 700, textTransform: 'uppercase', letterSpacing: 0.6, color: TEAL, marginBottom: 8 }}>
      Subject
    </label>
    <select
      id="ta-subject"
      value={subjectId}
      onChange={(e) => onChange(e.target.value)}
      className="w-full font-sans rounded-xl"
      style={{
        backgroundColor: '#FAF7F4',
        border: '1px solid #EDEBE8',
        padding: '12px 14px',
        fontSize: 14,
        color: '#1A1A1A',
        outline: 'none',
        appearance: 'none',
        cursor: 'pointer',
      }}
    >
      {SUBJECT_TIMING.map(s => (
        <option key={s.id} value={s.id}>
          {s.subjectLabel}
        </option>
      ))}
    </select>
  </section>
);

const PerMarkRateCard: React.FC<{
  subject: SubjectTiming;
  minPerMark: number;
  secPerMark: number;
}> = ({ subject, minPerMark, secPerMark }) => (
  <section
    className="rounded-2xl"
    style={{ backgroundColor: '#FAF7F4', border: `1px solid ${TEAL}33`, padding: '22px 26px' }}
  >
    <p className="font-sans" style={{ fontSize: 11, fontWeight: 700, textTransform: 'uppercase', letterSpacing: 0.6, color: TEAL, marginBottom: 6 }}>
      Your per-mark rate
    </p>
    <div className="flex items-baseline gap-3 flex-wrap">
      <div>
        <span className="font-serif" style={{ fontSize: 38, fontWeight: 700, color: '#1A1A1A' }}>
          {secPerMark}s
        </span>
        <span className="font-sans" style={{ fontSize: 14, color: '#78716C', marginLeft: 8 }}>
          ({minPerMark.toFixed(2)} min/mark)
        </span>
      </div>
    </div>
    <div className="grid sm:grid-cols-3 gap-3 mt-4">
      <Stat label="Total marks" value={subject.totalMarks.toString()} />
      <Stat label="Total minutes" value={`${subject.totalMinutes} min`} />
      <Stat label="Hours" value={`${(subject.totalMinutes / 60).toFixed(1)} hrs`} />
    </div>
    {subject.source.cite && (
      <p className="font-sans" style={{ fontSize: 11.5, color: '#78716C', marginTop: 12, fontStyle: 'italic' }}>
        {subject.source.cite}
      </p>
    )}
  </section>
);

const Stat: React.FC<{ label: string; value: string }> = ({ label, value }) => (
  <div
    className="rounded-xl"
    style={{ backgroundColor: '#FFFFFF', border: '1px solid #EDEBE8', padding: '12px 14px' }}
  >
    <p className="font-sans" style={{ fontSize: 10, fontWeight: 700, textTransform: 'uppercase', letterSpacing: 0.5, color: '#A8A29E', marginBottom: 4 }}>
      {label}
    </p>
    <p className="font-serif" style={{ fontSize: 18, fontWeight: 600, color: '#1A1A1A' }}>
      {value}
    </p>
  </div>
);

const BreakdownTable: React.FC<{
  subject: SubjectTiming;
  minPerMark: number;
}> = ({ subject, minPerMark }) => (
  <section
    className="rounded-2xl"
    style={{ backgroundColor: '#FFFFFF', border: '1px solid #EDEBE8', padding: '22px 24px' }}
  >
    <p className="font-sans" style={{ fontSize: 11, fontWeight: 700, textTransform: 'uppercase', letterSpacing: 0.6, color: TEAL, marginBottom: 12 }}>
      Section-by-section budget
    </p>
    <div className="space-y-2">
      <div className="flex items-baseline gap-3" style={{ paddingBottom: 6, borderBottom: '1px solid #EDEBE8' }}>
        <span className="font-sans flex-1" style={{ fontSize: 10, fontWeight: 700, textTransform: 'uppercase', letterSpacing: 0.5, color: '#A8A29E' }}>Section</span>
        <span className="font-sans" style={{ fontSize: 10, fontWeight: 700, textTransform: 'uppercase', letterSpacing: 0.5, color: '#A8A29E', width: 60, textAlign: 'right' }}>Marks</span>
        <span className="font-sans" style={{ fontSize: 10, fontWeight: 700, textTransform: 'uppercase', letterSpacing: 0.5, color: '#A8A29E', width: 70, textAlign: 'right' }}>Time</span>
      </div>
      {subject.breakdown.map((row, i) => (
        <div key={i} className="flex items-baseline gap-3" style={{ paddingTop: 6, paddingBottom: 6, borderBottom: i < subject.breakdown.length - 1 ? '1px solid #F5F4F1' : 'none' }}>
          <span className="font-sans flex-1" style={{ fontSize: 13, color: '#3F3B36', lineHeight: 1.45 }}>
            {row.section}
          </span>
          <span className="font-sans" style={{ fontSize: 13, color: '#1A1A1A', fontWeight: 600, width: 60, textAlign: 'right' }}>
            {row.marks}
          </span>
          <span className="font-sans" style={{ fontSize: 13, color: TEAL, fontWeight: 600, width: 70, textAlign: 'right' }}>
            {row.minutes} min
          </span>
        </div>
      ))}
    </div>
    <p className="font-sans" style={{ fontSize: 11.5, color: '#78716C', marginTop: 14, lineHeight: 1.5 }}>
      Built from the {subject.totalMinutes}-minute total at the rate of {minPerMark.toFixed(2)} min/mark. Add a 5-minute reading-and-planning buffer at the start; subtract from the section you're strongest at.
    </p>
  </section>
);

// ─── Sunk-cost simulator ────────────────────────────────────────────────

interface SimQuestion {
  id: string;
  marks: number;
  minutesAllocated: number;
  minutesSpent: number;
}

const DEFAULT_QUESTIONS: SimQuestion[] = [
  { id: 'q1', marks: 80, minutesAllocated: 35, minutesSpent: 0 },
  { id: 'q2', marks: 80, minutesAllocated: 35, minutesSpent: 0 },
  { id: 'q3', marks: 80, minutesAllocated: 35, minutesSpent: 0 },
];

const SunkCostSimulator: React.FC = () => {
  const [questions, setQuestions] = useState<SimQuestion[]>(DEFAULT_QUESTIONS);

  const totalAllocated = questions.reduce((sum, q) => sum + q.minutesAllocated, 0);
  const totalSpent = questions.reduce((sum, q) => sum + q.minutesSpent, 0);
  const totalMarks = questions.reduce((sum, q) => sum + q.marks, 0);

  /** Diminishing-returns scoring model.
   *  At allocated time → ~80% of marks. Each extra minute adds less. After
   *  ~150% of allocated, returns are negligible. Below allocated, scoring
   *  is roughly linear from 0. */
  const score = (q: SimQuestion): number => {
    const ratio = q.minutesSpent / q.minutesAllocated;
    if (ratio === 0) return 0;
    if (ratio <= 1) return q.marks * 0.8 * ratio;
    // Diminishing returns past 100%: gain ~20% over the next 50% of time, then plateau.
    const overshoot = Math.min(ratio - 1, 1);
    const diminishingGain = q.marks * 0.2 * (1 - Math.exp(-2.5 * overshoot));
    return q.marks * 0.8 + diminishingGain;
  };

  const totalScore = questions.reduce((sum, q) => sum + score(q), 0);
  const overBudget = totalSpent > totalAllocated;

  const reset = () => setQuestions(DEFAULT_QUESTIONS);

  const updateMinutesSpent = (id: string, value: number) => {
    setQuestions(prev => prev.map(q => q.id === id ? { ...q, minutesSpent: value } : q));
  };

  return (
    <section
      className="rounded-2xl"
      style={{ backgroundColor: '#FFFFFF', border: '1px solid #EDEBE8', padding: '24px 26px' }}
    >
      <div className="flex items-baseline justify-between gap-3 mb-2">
        <p className="font-sans" style={{ fontSize: 11, fontWeight: 700, textTransform: 'uppercase', letterSpacing: 0.6, color: TEAL }}>
          Sunk-cost simulator
        </p>
        <button
          type="button"
          onClick={reset}
          className="font-sans"
          style={{ fontSize: 12, color: '#78716C', background: 'transparent', border: 'none', padding: 0, cursor: 'pointer' }}
        >
          Reset
        </button>
      </div>
      <p className="font-sans" style={{ fontSize: 13, color: '#3F3B36', lineHeight: 1.55, marginBottom: 16 }}>
        Three 80-mark questions, 35 minutes each. 105 minutes total. Move each slider to set how long you actually spent. Watch what happens when one over-runs.
      </p>

      <div className="space-y-4">
        {questions.map((q, i) => (
          <SimRow
            key={q.id}
            label={`Q${i + 1}`}
            question={q}
            estimatedScore={score(q)}
            onChange={(v) => updateMinutesSpent(q.id, v)}
          />
        ))}
      </div>

      <div
        className="rounded-xl mt-5"
        style={{ backgroundColor: '#FAF7F4', border: `1px solid ${TEAL}33`, padding: '16px 18px' }}
      >
        <div className="grid sm:grid-cols-3 gap-3">
          <SimStat label="Time used" value={`${totalSpent} / ${totalAllocated} min`} highlight={overBudget ? 'warn' : null} />
          <SimStat label="Estimated marks" value={`${Math.round(totalScore)} / ${totalMarks}`} />
          <SimStat label="Estimated %" value={`${Math.round((totalScore / totalMarks) * 100)}%`} />
        </div>
        <p className="font-sans" style={{ fontSize: 12.5, color: '#3F3B36', lineHeight: 1.55, marginTop: 12 }}>
          {overBudget
            ? `You've over-run by ${totalSpent - totalAllocated} minutes. Notice how spending another 10 minutes on the question you're already 90% done with adds maybe 3 marks — and the unanswered question loses 30+. The fastest mark-grab on a paper is always the question you haven't started.`
            : 'Try over-running on Q1 by 10-15 minutes. Then drop Q3 down to compensate. The math is brutal: a perfect Q1 buys nothing once Q3 falls below half.'}
        </p>
      </div>
    </section>
  );
};

const SimRow: React.FC<{
  label: string;
  question: SimQuestion;
  estimatedScore: number;
  onChange: (v: number) => void;
}> = ({ label, question, estimatedScore, onChange }) => {
  const overBudget = question.minutesSpent > question.minutesAllocated;
  return (
    <div>
      <div className="flex items-baseline justify-between gap-3 mb-1">
        <div>
          <span className="font-serif" style={{ fontSize: 14, fontWeight: 700, color: '#1A1A1A', marginRight: 8 }}>
            {label}
          </span>
          <span className="font-sans" style={{ fontSize: 12, color: '#78716C' }}>
            {question.marks} marks · {question.minutesAllocated} min budget
          </span>
        </div>
        <div className="font-serif" style={{ fontSize: 14, fontWeight: 600, color: TEAL }}>
          ~{Math.round(estimatedScore)} / {question.marks}
        </div>
      </div>
      <input
        type="range"
        min={0}
        max={Math.round(question.minutesAllocated * 1.6)}
        value={question.minutesSpent}
        onChange={(e) => onChange(Number(e.target.value))}
        className="w-full"
        style={{ accentColor: overBudget ? '#A8746E' : TEAL }}
      />
      <p className="font-sans" style={{ fontSize: 11.5, color: overBudget ? '#A8746E' : '#78716C', marginTop: 2 }}>
        {question.minutesSpent} min spent {overBudget ? `· ${question.minutesSpent - question.minutesAllocated} over budget` : ''}
      </p>
    </div>
  );
};

const SimStat: React.FC<{ label: string; value: string; highlight?: 'warn' | null }> = ({ label, value, highlight }) => (
  <div>
    <p className="font-sans" style={{ fontSize: 10, fontWeight: 700, textTransform: 'uppercase', letterSpacing: 0.5, color: '#A8A29E', marginBottom: 2 }}>
      {label}
    </p>
    <p className="font-serif" style={{ fontSize: 18, fontWeight: 700, color: highlight === 'warn' ? '#A8746E' : '#1A1A1A' }}>
      {value}
    </p>
  </div>
);

export default TimeAllocationCalculator;
