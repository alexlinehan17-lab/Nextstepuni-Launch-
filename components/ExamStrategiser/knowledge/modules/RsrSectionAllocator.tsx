/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * RSR Section Allocator (Stage 3.2, E19).
 *
 * Three sub-tools in one module for the History Research Study Report
 * (100 marks, 20% of paper):
 *
 *   1. WORD-BUDGET METER — four bars, one per RSR section. Each bar
 *      shows words written (filled) against the mark-weighted target
 *      range (outline). HL/OL toggle drives the target ranges. When
 *      filled and outlined match, the bar pulses teal; misalignment
 *      flashes a warm-brown warn state.
 *
 *   2. SOURCE EVALUATION QUALITY — student pastes a single source-
 *      evaluation paragraph. The tool runs four criteria checks (Origin,
 *      Purpose, Value, Limitations). Each check is detected by signal-
 *      pattern matching and reports pass/fail with the specific
 *      examiner-voice prescription if missing.
 *
 *   3. REVIEW OF PROCESS SLOP DETECTOR — student pastes their Review of
 *      Process. The tool flags vague filler ("I researched on the
 *      internet", "It was challenging at times") with hover prescriptions
 *      naming what to write instead.
 *
 * Closing summary computes a section-by-section grade estimate and
 * surfaces the weakest section with a one-action prescription.
 *
 * Source: dossier § A2 (RSR mark allocation), § B5 (2017 History CER).
 *
 * Aesthetic: Stage 3 register — 2px #1a1a1a borders. The four-bar meter
 * uses two-layer overlay rendering (filled fill + outlined target) to
 * make alignment visible at a glance.
 */

import React, { useMemo, useState } from 'react';
import { motion } from 'framer-motion';
import {
  RSR_SECTIONS,
  SOURCE_EVAL_CHECKS,
  SLOP_PATTERNS,
} from '../../../../data/knowledge/rsrConfig';
import {
  type RsrSectionSpec,
  type RsrSectionId,
  type SourceEvalCheck,
  type SourceEvalCheckSpec,
  type SlopPattern,
} from '../../../../types/knowledge';

const TEAL = '#2A7D6F';
const TEAL_DARK = '#1a5a4e';
const INK = '#1a1a1a';
const CREAM = '#FDF8F0';
const WARN = '#A8746E';

type Level = 'hl' | 'ol';

interface Props {
  onBack: () => void;
}

const RsrSectionAllocator: React.FC<Props> = ({ onBack }) => {
  const [level, setLevel] = useState<Level>('hl');
  const [sectionTexts, setSectionTexts] = useState<Record<RsrSectionId, string>>({
    'outline-plan': '',
    'evaluation-sources': '',
    'extended-essay': '',
    'review-process': '',
  });

  const updateSection = (id: RsrSectionId, text: string) => {
    setSectionTexts(prev => ({ ...prev, [id]: text }));
  };

  return (
    <div className="space-y-6" style={{ color: INK }}>
      <BackBar onBack={onBack} />
      <Hero />

      <LevelToggle level={level} onChange={setLevel} />

      <WordBudgetMeter sections={RSR_SECTIONS} sectionTexts={sectionTexts} level={level} />

      <SectionEditors sections={RSR_SECTIONS} sectionTexts={sectionTexts} updateSection={updateSection} level={level} />

      <SourceEvalSubTool />

      <SlopDetectorSubTool />

      <ClosingSummary sections={RSR_SECTIONS} sectionTexts={sectionTexts} level={level} />
    </div>
  );
};

// ─── Layout chrome ─────────────────────────────────────────────────────

const BackBar: React.FC<{ onBack: () => void }> = ({ onBack }) => (
  <button
    type="button"
    onClick={onBack}
    className="font-sans flex items-center gap-1.5"
    style={{ fontSize: 12, color: '#78716C', background: 'transparent', border: 'none', padding: 0, cursor: 'pointer' }}
  >
    <svg width="12" height="12" viewBox="0 0 16 16" fill="none" aria-hidden>
      <path d="M10 3L5 8L10 13" stroke="currentColor" strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round" />
    </svg>
    Necessary Knowledge
  </button>
);

const Hero: React.FC = () => (
  <header>
    <p className="font-sans" style={{ fontSize: 11, fontWeight: 700, textTransform: 'uppercase', letterSpacing: 0.6, color: '#9e9186' }}>
      Necessary Knowledge · Stage 3 · History
    </p>
    <h1 className="font-serif" style={{ fontSize: 30, fontWeight: 600, color: INK, marginTop: 4, lineHeight: 1.15 }}>
      RSR Section Allocator.
    </h1>
    <p className="font-sans max-w-2xl" style={{ fontSize: 14.5, color: '#5a5550', marginTop: 8, lineHeight: 1.55 }}>
      The Research Study Report is 20% of your History grade — 100 marks across four sections (Outline Plan, Evaluation
      of Sources, Extended Essay, Review of Process). Each section has a mark weight; each section has a word-count
      budget. The fastest way to lose marks is to over-write the Essay and starve the others.
    </p>
  </header>
);

// ─── Level toggle ──────────────────────────────────────────────────────

const LevelToggle: React.FC<{ level: Level; onChange: (l: Level) => void }> = ({ level, onChange }) => (
  <div className="inline-flex" style={{ border: `2px solid ${INK}`, borderRadius: 999, padding: 3 }}>
    {(['hl', 'ol'] as const).map(l => {
      const active = l === level;
      return (
        <button
          key={l}
          type="button"
          onClick={() => onChange(l)}
          className="font-sans rounded-full"
          style={{
            backgroundColor: active ? INK : 'transparent',
            color: active ? '#FFFFFF' : INK,
            border: 'none',
            padding: '6px 16px',
            fontSize: 12,
            fontWeight: 600,
            cursor: 'pointer',
          }}
        >
          {l === 'hl' ? 'Higher Level' : 'Ordinary Level'}
        </button>
      );
    })}
  </div>
);

// ─── Word-budget meter ────────────────────────────────────────────────

function countWords(text: string): number {
  const trimmed = text.trim();
  if (!trimmed) return 0;
  return trimmed.split(/\s+/).length;
}

const WordBudgetMeter: React.FC<{
  sections: RsrSectionSpec[];
  sectionTexts: Record<RsrSectionId, string>;
  level: Level;
}> = ({ sections, sectionTexts, level }) => {
  const totalMin = sections.reduce((sum, s) => sum + (level === 'hl' ? s.hlMin : s.olMin), 0);
  const totalMax = sections.reduce((sum, s) => sum + (level === 'hl' ? s.hlMax : s.olMax), 0);
  const totalWords = sections.reduce((sum, s) => sum + countWords(sectionTexts[s.id]), 0);

  return (
    <section
      className="rounded-2xl"
      style={{ backgroundColor: '#FFFFFF', border: `2px solid ${INK}`, padding: '24px 26px' }}
    >
      <div className="flex items-baseline justify-between gap-3 mb-4 flex-wrap">
        <p className="font-sans" style={{ fontSize: 10, fontWeight: 700, textTransform: 'uppercase', letterSpacing: 0.6, color: TEAL }}>
          Word-budget meter
        </p>
        <span className="font-sans" style={{ fontSize: 11.5, color: '#5a5550' }}>
          Total {totalWords} / {totalMin}–{totalMax} words ({level === 'hl' ? 'HL' : 'OL'})
        </span>
      </div>

      <div className="space-y-3">
        {sections.map(s => {
          const words = countWords(sectionTexts[s.id]);
          const min = level === 'hl' ? s.hlMin : s.olMin;
          const max = level === 'hl' ? s.hlMax : s.olMax;
          return (
            <SectionBar key={s.id} section={s} words={words} min={min} max={max} />
          );
        })}
      </div>
    </section>
  );
};

const SectionBar: React.FC<{
  section: RsrSectionSpec;
  words: number;
  min: number;
  max: number;
}> = ({ section, words, min, max }) => {
  // Normalise everything against the max so the visual scale is comparable
  const VISUAL_MAX = Math.round(max * 1.3); // a little headroom
  const filledPct = Math.min(100, (words / VISUAL_MAX) * 100);
  const minPct = (min / VISUAL_MAX) * 100;
  const maxPct = (max / VISUAL_MAX) * 100;
  const inRange = words >= min && words <= max;
  const isOver = words > max;
  const isUnder = words > 0 && words < min;
  const filledColour = inRange ? TEAL : isOver ? WARN : isUnder ? '#9e9186' : '#9e9186';

  return (
    <div>
      <div className="flex items-baseline justify-between gap-3 mb-1.5 flex-wrap">
        <div>
          <span className="font-serif" style={{ fontSize: 14, fontWeight: 700, color: INK, marginRight: 8 }}>
            {section.label}
          </span>
          <span
            className="font-sans"
            style={{
              fontSize: 10,
              fontWeight: 700,
              color: TEAL,
              backgroundColor: `${TEAL}15`,
              border: `1px solid ${TEAL}66`,
              borderRadius: 999,
              padding: '1px 8px',
            }}
          >
            {section.marksOf100} marks
          </span>
        </div>
        <div className="font-serif text-right" style={{ fontSize: 13.5, fontWeight: 600 }}>
          <span style={{ color: filledColour }}>{words}</span>
          <span style={{ color: '#9e9186', fontWeight: 500, fontSize: 11.5 }}> / {min}–{max}</span>
        </div>
      </div>

      {/* Two-layer bar: target range outline + filled fill */}
      <div
        style={{
          position: 'relative',
          height: 16,
          backgroundColor: '#F5F4F1',
          borderRadius: 999,
          overflow: 'hidden',
        }}
      >
        {/* Target range outlined */}
        <div
          aria-hidden
          style={{
            position: 'absolute',
            left: `${minPct}%`,
            width: `${maxPct - minPct}%`,
            top: 0,
            bottom: 0,
            border: `2px dashed ${INK}`,
            borderLeft: `2px solid ${INK}`,
            borderRight: `2px solid ${INK}`,
            backgroundColor: 'transparent',
            pointerEvents: 'none',
            zIndex: 2,
          }}
        />
        {/* Filled */}
        <motion.div
          animate={{ width: `${filledPct}%` }}
          transition={{ duration: 0.4, ease: 'easeOut' }}
          style={{
            position: 'absolute',
            left: 0,
            top: 0,
            bottom: 0,
            backgroundColor: filledColour,
            zIndex: 1,
          }}
        />
        {inRange && words > 0 && (
          <motion.div
            animate={{ opacity: [0, 0.55, 0] }}
            transition={{ duration: 1.4, repeat: Infinity, ease: 'easeInOut' }}
            style={{
              position: 'absolute',
              inset: 0,
              backgroundColor: TEAL,
              zIndex: 3,
              pointerEvents: 'none',
            }}
          />
        )}
      </div>

      <p className="font-sans" style={{ fontSize: 11, color: '#5a5550', marginTop: 4, lineHeight: 1.4 }}>
        {isOver
          ? `${words - max} words over budget. Trim until you\'re inside ${min}–${max}.`
          : isUnder
          ? `${min - words} words below the floor. Examiners read thin sections as under-developed.`
          : words === 0
          ? section.guidance
          : 'In range.'}
      </p>
    </div>
  );
};

// ─── Section editors ──────────────────────────────────────────────────

const SectionEditors: React.FC<{
  sections: RsrSectionSpec[];
  sectionTexts: Record<RsrSectionId, string>;
  updateSection: (id: RsrSectionId, text: string) => void;
  level: Level;
}> = ({ sections, sectionTexts, updateSection, level }) => (
  <section
    className="rounded-2xl"
    style={{ backgroundColor: CREAM, border: `2px solid ${INK}`, padding: '24px 26px' }}
  >
    <p className="font-sans" style={{ fontSize: 10, fontWeight: 700, textTransform: 'uppercase', letterSpacing: 0.6, color: TEAL, marginBottom: 14 }}>
      Paste your RSR by section
    </p>
    <div className="space-y-4">
      {sections.map(s => (
        <SectionEditor
          key={s.id}
          section={s}
          text={sectionTexts[s.id]}
          onChange={(text) => updateSection(s.id, text)}
          level={level}
        />
      ))}
    </div>
  </section>
);

const SectionEditor: React.FC<{
  section: RsrSectionSpec;
  text: string;
  onChange: (t: string) => void;
  level: Level;
}> = ({ section, text, onChange, level }) => {
  const min = level === 'hl' ? section.hlMin : section.olMin;
  const max = level === 'hl' ? section.hlMax : section.olMax;
  return (
    <div>
      <label
        htmlFor={`rsr-${section.id}`}
        className="font-sans block"
        style={{ fontSize: 10, fontWeight: 700, textTransform: 'uppercase', letterSpacing: 0.5, color: '#9e9186', marginBottom: 6 }}
      >
        {section.label} <span style={{ color: TEAL }}>· {section.marksOf100} marks · {min}–{max} words</span>
      </label>
      <textarea
        id={`rsr-${section.id}`}
        value={text}
        onChange={(e) => onChange(e.target.value)}
        placeholder={section.guidance}
        className="w-full font-serif rounded-lg"
        style={{
          backgroundColor: '#FFFFFF',
          border: `1.5px solid ${INK}`,
          padding: '12px 14px',
          fontSize: 13.5,
          lineHeight: 1.55,
          color: INK,
          minHeight: 90,
          resize: 'vertical',
          outline: 'none',
        }}
      />
    </div>
  );
};

// ─── Source evaluation sub-tool ───────────────────────────────────────

const SourceEvalSubTool: React.FC = () => {
  const [text, setText] = useState('');

  const detected = useMemo(() => {
    if (!text.trim()) return null;
    return SOURCE_EVAL_CHECKS.map(check => ({
      check,
      hits: detectSignals(text, check.signalPatterns),
    }));
  }, [text]);

  const passed = detected?.filter(d => d.hits.length > 0).length ?? 0;
  const total = SOURCE_EVAL_CHECKS.length;

  return (
    <section
      className="rounded-2xl"
      style={{ backgroundColor: '#FFFFFF', border: `2px solid ${INK}`, padding: '24px 26px' }}
    >
      <div className="flex items-baseline justify-between gap-3 mb-2 flex-wrap">
        <p className="font-sans" style={{ fontSize: 10, fontWeight: 700, textTransform: 'uppercase', letterSpacing: 0.6, color: TEAL }}>
          Source-evaluation quality
        </p>
        {detected && (
          <span className="font-serif" style={{ fontSize: 14, fontWeight: 700, color: passed === total ? TEAL : passed >= 2 ? TEAL_DARK : WARN }}>
            {passed} / {total} criteria addressed
          </span>
        )}
      </div>
      <p className="font-sans" style={{ fontSize: 12.5, color: '#5a5550', marginBottom: 12, lineHeight: 1.55 }}>
        Paste a single source-evaluation paragraph. The 2017 History Chief Examiner Report flagged weak source criticism — the tool checks for the four criteria the marker is hunting.
      </p>
      <textarea
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder={'e.g. "Robert Fisk\'s The Great War for Civilisation was published in 2005 by Knopf. The author was a journalist with the Independent who covered the Middle East from the 1970s onwards. The purpose of the book was to provide..."'}
        className="w-full font-serif rounded-lg"
        style={{
          backgroundColor: CREAM,
          border: `1.5px solid ${INK}`,
          padding: '12px 14px',
          fontSize: 13.5,
          lineHeight: 1.6,
          color: INK,
          minHeight: 130,
          resize: 'vertical',
          outline: 'none',
        }}
      />

      {detected && (
        <div className="grid sm:grid-cols-2 gap-2 mt-4">
          {detected.map(d => (
            <CheckCard key={d.check.id} check={d.check} hits={d.hits} />
          ))}
        </div>
      )}
    </section>
  );
};

const CheckCard: React.FC<{ check: SourceEvalCheckSpec; hits: string[] }> = ({ check, hits }) => {
  const passed = hits.length > 0;
  const colour = passed ? TEAL : WARN;
  return (
    <article
      className="rounded-xl"
      style={{
        backgroundColor: passed ? `${TEAL}10` : `${WARN}10`,
        border: `1.5px solid ${colour}`,
        padding: '12px 14px',
      }}
    >
      <div className="flex items-baseline gap-2 mb-1.5 flex-wrap">
        <span
          className="font-sans inline-flex items-center justify-center"
          style={{
            width: 22,
            height: 22,
            borderRadius: 999,
            backgroundColor: colour,
            color: '#FFFFFF',
            fontSize: 12,
            fontWeight: 700,
          }}
          aria-hidden
        >
          {passed ? '✓' : '!'}
        </span>
        <p className="font-serif" style={{ fontSize: 14, fontWeight: 700, color: INK }}>
          {check.label}
        </p>
        <span className="font-sans" style={{ fontSize: 10.5, color: '#5a5550' }}>
          {check.promptQuestion}
        </span>
      </div>
      {passed ? (
        <p className="font-sans" style={{ fontSize: 11.5, color: '#3F3B36', lineHeight: 1.55 }}>
          Detected: {hits.slice(0, 3).map(h => `"${h}"`).join(', ')}{hits.length > 3 ? `, and ${hits.length - 3} more` : ''}.
        </p>
      ) : (
        <p className="font-sans" style={{ fontSize: 11.5, color: '#3F3B36', lineHeight: 1.55 }}>
          {check.prescription}
        </p>
      )}
    </article>
  );
};

function detectSignals(text: string, patterns: string[]): string[] {
  const hits: string[] = [];
  const lower = text.toLowerCase();
  for (const p of patterns) {
    try {
      const re = new RegExp(p, 'i');
      const m = lower.match(re);
      if (m) hits.push(m[0]);
    } catch {
      // Pattern fallback — substring match
      if (lower.includes(p.toLowerCase())) hits.push(p);
    }
  }
  return hits;
}

// ─── Slop detector sub-tool ───────────────────────────────────────────

const SlopDetectorSubTool: React.FC = () => {
  const [text, setText] = useState('');

  const flagged = useMemo(() => {
    if (!text.trim()) return [];
    return findSlopMatches(text);
  }, [text]);

  return (
    <section
      className="rounded-2xl"
      style={{ backgroundColor: '#FFFFFF', border: `2px solid ${INK}`, padding: '24px 26px' }}
    >
      <div className="flex items-baseline justify-between gap-3 mb-2 flex-wrap">
        <p className="font-sans" style={{ fontSize: 10, fontWeight: 700, textTransform: 'uppercase', letterSpacing: 0.6, color: TEAL }}>
          Review-of-process slop detector
        </p>
        {text.trim() && (
          <span className="font-serif" style={{ fontSize: 14, fontWeight: 700, color: flagged.length === 0 ? TEAL : WARN }}>
            {flagged.length} {flagged.length === 1 ? 'slop pattern' : 'slop patterns'} flagged
          </span>
        )}
      </div>
      <p className="font-sans" style={{ fontSize: 12.5, color: '#5a5550', marginBottom: 12, lineHeight: 1.55 }}>
        Paste your Review of Process. The 2017 History CER explicitly named "vague Review of Process" as a perennial weakness — the tool flags filler ("I researched on the internet", "It was challenging at times") and proposes specific replacements.
      </p>
      <textarea
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder='Paste your Review of Process here. The tool will flag generic phrases and propose specific replacements.'
        className="w-full font-serif rounded-lg"
        style={{
          backgroundColor: CREAM,
          border: `1.5px solid ${INK}`,
          padding: '12px 14px',
          fontSize: 13.5,
          lineHeight: 1.7,
          color: INK,
          minHeight: 140,
          resize: 'vertical',
          outline: 'none',
        }}
      />

      {flagged.length > 0 && (
        <div className="space-y-2 mt-4">
          <p className="font-sans" style={{ fontSize: 10, fontWeight: 700, textTransform: 'uppercase', letterSpacing: 0.5, color: '#9e9186' }}>
            Flagged passages
          </p>
          {flagged.slice(0, 6).map((f, i) => (
            <SlopFlag key={i} match={f.match} pattern={f.pattern} />
          ))}
          {flagged.length > 6 && (
            <p className="font-sans" style={{ fontSize: 11.5, color: '#5a5550' }}>
              … and {flagged.length - 6} more.
            </p>
          )}
        </div>
      )}
    </section>
  );
};

const SlopFlag: React.FC<{ match: string; pattern: SlopPattern }> = ({ match, pattern }) => (
  <div
    className="rounded-lg"
    style={{
      backgroundColor: `${WARN}10`,
      border: `1.5px solid ${WARN}`,
      padding: '12px 14px',
    }}
  >
    <p
      className="font-serif"
      style={{
        fontSize: 13,
        color: INK,
        lineHeight: 1.55,
        marginBottom: 6,
        fontStyle: 'italic',
      }}
    >
      <mark style={{ backgroundColor: `${WARN}45`, padding: '1px 4px', borderRadius: 3 }}>
        {match}
      </mark>
    </p>
    <p className="font-sans" style={{ fontSize: 11, fontWeight: 700, textTransform: 'uppercase', letterSpacing: 0.5, color: WARN, marginBottom: 3 }}>
      {pattern.flag}
    </p>
    <p className="font-sans" style={{ fontSize: 12, color: '#3F3B36', lineHeight: 1.55 }}>
      {pattern.prescription}
    </p>
  </div>
);

interface SlopMatch {
  match: string;
  pattern: SlopPattern;
}

function findSlopMatches(text: string): SlopMatch[] {
  const matches: SlopMatch[] = [];
  const lower = text.toLowerCase();
  for (const p of SLOP_PATTERNS) {
    try {
      const re = new RegExp(p.pattern, 'gi');
      let m;
      while ((m = re.exec(lower)) !== null) {
        matches.push({ match: m[0], pattern: p });
        if (m.index === re.lastIndex) re.lastIndex++;
      }
    } catch {
      // ignore bad patterns
    }
  }
  return matches;
}

// ─── Closing summary ──────────────────────────────────────────────────

const ClosingSummary: React.FC<{
  sections: RsrSectionSpec[];
  sectionTexts: Record<RsrSectionId, string>;
  level: Level;
}> = ({ sections, sectionTexts, level }) => {
  const totalWords = sections.reduce((sum, s) => sum + countWords(sectionTexts[s.id]), 0);
  if (totalWords === 0) return null;

  const sectionScores = sections.map(s => {
    const words = countWords(sectionTexts[s.id]);
    const min = level === 'hl' ? s.hlMin : s.olMin;
    const max = level === 'hl' ? s.hlMax : s.olMax;
    const inRange = words >= min && words <= max;
    const isOver = words > max;
    const isUnder = words > 0 && words < min;
    const isEmpty = words === 0;

    let estimateBand: number;
    if (isEmpty) estimateBand = 0;
    else if (inRange) estimateBand = s.marksOf100 * 0.8; // rough 80% of section marks if in range — execution still counts
    else if (isOver) estimateBand = s.marksOf100 * 0.6;
    else if (isUnder) estimateBand = (words / min) * s.marksOf100 * 0.7;
    else estimateBand = 0;

    return { section: s, words, isEmpty, isOver, isUnder, inRange, estimateBand };
  });

  const totalEstimate = Math.round(sectionScores.reduce((sum, sc) => sum + sc.estimateBand, 0));
  const weakestSection = sectionScores
    .filter(sc => !sc.isEmpty || sc.section.id === 'review-process') // Empty sections always weak
    .reduce<typeof sectionScores[number] | null>(
      (worst, cur) => {
        const curRatio = cur.estimateBand / cur.section.marksOf100;
        if (worst === null) return cur;
        const worstRatio = worst.estimateBand / worst.section.marksOf100;
        return curRatio < worstRatio ? cur : worst;
      },
      null,
    );

  return (
    <section
      className="rounded-2xl"
      style={{ backgroundColor: INK, color: '#FFFFFF', padding: '28px 30px' }}
    >
      <p className="font-sans" style={{ fontSize: 10, fontWeight: 700, textTransform: 'uppercase', letterSpacing: 0.6, color: '#FFD8A8', opacity: 0.85 }}>
        Section-by-section estimate
      </p>
      <h3 className="font-serif" style={{ fontSize: 26, fontWeight: 600, lineHeight: 1.2, marginTop: 6 }}>
        ~{totalEstimate} / 100 marks under current word allocation.
      </h3>
      <p className="font-sans" style={{ fontSize: 12, color: '#FFD8A8', opacity: 0.85, marginTop: 4 }}>
        Estimate is structural — based on word allocation against mark weight. Execution quality (sources, chronology, source criticism) lives on top of this.
      </p>

      <div className="grid sm:grid-cols-2 gap-2 mt-5">
        {sectionScores.map(sc => (
          <div
            key={sc.section.id}
            className="rounded-xl"
            style={{
              backgroundColor: '#3F3B36',
              padding: '12px 14px',
            }}
          >
            <div className="flex items-baseline justify-between mb-1">
              <span className="font-serif" style={{ fontSize: 13, fontWeight: 700, color: '#FFFFFF' }}>
                {sc.section.label}
              </span>
              <span className="font-serif" style={{ fontSize: 14, fontWeight: 700, color: sc.inRange ? TEAL : WARN }}>
                ~{Math.round(sc.estimateBand)} / {sc.section.marksOf100}
              </span>
            </div>
            <p className="font-sans" style={{ fontSize: 11, color: '#E8E4DE', opacity: 0.85, lineHeight: 1.5 }}>
              {sc.isEmpty
                ? 'Empty.'
                : sc.isOver
                ? `${sc.words - (level === 'hl' ? sc.section.hlMax : sc.section.olMax)} words over.`
                : sc.isUnder
                ? `${(level === 'hl' ? sc.section.hlMin : sc.section.olMin) - sc.words} words under.`
                : 'In range.'}
            </p>
          </div>
        ))}
      </div>

      {weakestSection && (
        <div className="mt-6" style={{ borderLeft: `3px solid ${TEAL}`, paddingLeft: 16 }}>
          <p className="font-sans" style={{ fontSize: 10, fontWeight: 700, textTransform: 'uppercase', letterSpacing: 0.6, color: '#FFD8A8', opacity: 0.9 }}>
            Weakest section · {weakestSection.section.label}
          </p>
          <p className="font-sans" style={{ fontSize: 13, color: '#E8E4DE', marginTop: 4, lineHeight: 1.55 }}>
            {weakestSection.isEmpty
              ? `This section is empty. ${weakestSection.section.marksOf100} marks are unscored. ${weakestSection.section.guidance}`
              : weakestSection.isOver
              ? `Over-written by ${weakestSection.words - (level === 'hl' ? weakestSection.section.hlMax : weakestSection.section.olMax)} words. Trim until in range — examiners cap over-budget sections.`
              : `Under-written. ${weakestSection.section.guidance}`}
          </p>
        </div>
      )}
    </section>
  );
};

export default RsrSectionAllocator;
