/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { motion } from 'framer-motion';
import {
AlertTriangle,
BarChart3,
Calculator,
GitBranch,Layers,
Minus,Plus,
Scale,
Target,
TrendingDown
} from 'lucide-react';
import React,{ useEffect,useId,useMemo,useState } from 'react';
import { POINTS_OPTIMIZATION_REFERENCE_LIST } from '../data/references/pointsOptimization';
import { useEssentialsMode } from '../hooks/useEssentialsMode';
import { useModuleResponses } from '../hooks/useModuleResponses';
import { redTheme } from '../moduleThemes';
import { type ModuleProgress } from '../types';
import { ModuleLayout } from './ModuleLayout';
import { Cite } from './ModuleReferences';
import { Highlight,MicroCommitment,PersonalStory,ReadingSection,ToolJumpCard } from './ModuleShared';
import { MotionDiv } from './Motion';
import { AnswerGroup,AnswerLine,AnswerTick,ExerciseSheet } from './learning/Exercise';
import { Arrow,Button,Glyph,TextButton } from './ui/Button';
import { ChoiceTile,SelectionBar } from './ui/Choice';

const theme = redTheme;

/** A native select, kept as it works today (the same value, onChange and options), drawn as the system's field:
 *  white, a 1px line, radius 9, 16px words, 48 tall, with the menu arrow. */
const FieldSelect = ({ className = '', children, ...props }: React.SelectHTMLAttributes<HTMLSelectElement>) => (
  <span className={`ui-part ui-field-wrap ${className}`.trim()}>
    <select {...props} className="ui-field-input" style={{ paddingRight: 44, borderRadius: 'var(--r-sm)', fontFamily: 'var(--font-ui)' }}>
      {children}
    </select>
    <span className="absolute right-3.5 top-1/2 -translate-y-1/2 pointer-events-none flex text-ink-muted"><Arrow meaning="menu" size={20} /></span>
  </span>
);

// ─── DATA ────────────────────────────────────────────────────────────────────

const GRADES = ['H1','H2','H3','H4','H5','H6','H7','H8'] as const;
const GRADE_POINTS: Record<string, number> = { H1:100, H2:88, H3:77, H4:66, H5:56, H6:46, H7:37, H8:0 };

const SUBJECTS_DATA = [
  { name: 'Applied Maths', h1Rate: 27, objectivity: 95, group: 'maths', synergies: ['Mathematics','Physics'] },
  { name: 'Physics', h1Rate: 11, objectivity: 90, group: 'stem', synergies: ['Mathematics','Applied Maths','Chemistry'] },
  { name: 'Chemistry', h1Rate: 12, objectivity: 88, group: 'stem', synergies: ['Physics','Biology','Ag Science'] },
  { name: 'Accounting', h1Rate: 16, objectivity: 85, group: 'business', synergies: ['Business','Economics'] },
  { name: 'Mathematics', h1Rate: 16, objectivity: 95, group: 'maths', synergies: ['Applied Maths','Physics','Economics'], isMaths: true },
  { name: 'Biology', h1Rate: 15, objectivity: 75, group: 'life-science', synergies: ['Chemistry','Ag Science','Home Economics'] },
  { name: 'Spanish', h1Rate: 14, objectivity: 60, group: 'language', synergies: ['French','German'] },
  { name: 'Economics', h1Rate: 13, objectivity: 70, group: 'business', synergies: ['Mathematics','Business','Accounting'] },
  { name: 'German', h1Rate: 12, objectivity: 60, group: 'language', synergies: ['French','Spanish'] },
  { name: 'Ag Science', h1Rate: 12, objectivity: 70, group: 'life-science', synergies: ['Biology','Chemistry','Geography'] },
  { name: 'French', h1Rate: 11, objectivity: 60, group: 'language', synergies: ['Spanish','German'] },
  { name: 'Home Economics', h1Rate: 10, objectivity: 55, group: 'practical', synergies: ['Biology'] },
  { name: 'Business', h1Rate: 10, objectivity: 65, group: 'business', synergies: ['Economics','Accounting'] },
  { name: 'Construction Studies', h1Rate: 9, objectivity: 72, group: 'practical', synergies: ['DCG','Engineering'] },
  { name: 'DCG', h1Rate: 9, objectivity: 78, group: 'practical', synergies: ['Construction Studies','Engineering'] },
  { name: 'Music', h1Rate: 8, objectivity: 50, group: 'creative', synergies: [] },
  { name: 'Irish', h1Rate: 8, objectivity: 55, group: 'language', synergies: [] },
  { name: 'Politics & Society', h1Rate: 7, objectivity: 40, group: 'humanities', synergies: ['History','Geography'] },
  { name: 'History', h1Rate: 6, objectivity: 35, group: 'humanities', synergies: ['Politics & Society','English'] },
  { name: 'English', h1Rate: 7, objectivity: 25, group: 'humanities', synergies: ['History'] },
  { name: 'Geography', h1Rate: 5, objectivity: 40, group: 'humanities', synergies: ['Ag Science','Biology'] },
  { name: 'Art', h1Rate: 4, objectivity: 20, group: 'creative', synergies: [] },
];

// ─── INTERACTIVE 1: Grade Waterfall Calculator ──────────────────────────────

const GradeWaterfall = () => {
  const defaultGrades = ['H1','H1','H1','H1','H1','H1','H1'];
  const defaultSubjects = ['Mathematics','English','Irish','Physics','Chemistry','Biology','French'];
  const [grades, setGrades] = useState<string[]>(defaultGrades);
  const rowId = useId();

  const subjectPoints = grades.map((grade, i) => {
    let pts = GRADE_POINTS[grade] || 0;
    if (i === 0 && ['H1','H2','H3','H4','H5','H6'].includes(grade)) pts += 25; // Maths bonus
    return pts;
  });

  const sorted = [...subjectPoints].sort((a, b) => b - a);
  const bestSix = sorted.slice(0, 6);
  const total = bestSix.reduce((sum, p) => sum + p, 0);
  const maxTotal = 625;

  const setGrade = (idx: number, grade: string) => {
    const next = [...grades];
    next[idx] = grade;
    setGrades(next);
  };

  return (
    <ExerciseSheet title="Grade Waterfall Calculator" sub="Change the grades below and watch your points total respond. Notice how steep the H1→H2 cliff is." name="GradeWaterfall">
      {/* Each subject ruled like a row: its name and points, then its grade and the student's own bar (ink on a hairline track) */}
      <div className="ex-list">
        {defaultSubjects.map((subj, idx) => {
          const pts = subjectPoints[idx];
          const isMaths = idx === 0;

          return (
            <div key={subj}>
              <div className="flex items-baseline justify-between gap-3">
                <span id={`${rowId}-${idx}`} className="t-sub text-ink-primary">{subj}{isMaths ? ' *' : ''}</span>
                <span className="ui-readout text-ink-primary text-right">
                  {pts} pts{isMaths && grades[idx] !== 'H7' && grades[idx] !== 'H8' ? ' (incl. +25)' : ''}
                </span>
              </div>
              <div className="flex items-center gap-3">
                <FieldSelect
                  className="w-24 shrink-0"
                  aria-labelledby={`${rowId}-${idx}`}
                  value={grades[idx]}
                  onChange={(e) => setGrade(idx, e.target.value)}
                >
                  {GRADES.map(g => <option key={g} value={g}>{g}</option>)}
                </FieldSelect>
                <div className="flex-grow h-2 rounded-full overflow-hidden" style={{ background: 'var(--hairline)' }}>
                  <motion.div
                    className="h-full rounded-full"
                    style={{ background: 'var(--ink-primary)' }}
                    animate={{ width: `${(pts / 125) * 100}%` }}
                    transition={{ duration: 0.4, ease: [0.16, 1, 0.3, 1] }}
                  />
                </div>
              </div>
            </div>
          );
        })}
      </div>

      {/* The totals: labels and numbers in ink under a hairline (no tinted panel, no colour for lost points) */}
      <div className="ex-result">
        <div className="flex items-end justify-between gap-4">
          <div>
            <p className="ex-label">Best 6 Total</p>
            <p className="t-number text-ink-primary">{total}<span className="t-sub">/{maxTotal}</span></p>
          </div>
          <div className="text-right">
            <p className="ex-label">Points Lost</p>
            <p className="t-number text-ink-primary">
              {total < maxTotal ? `-${maxTotal - total}` : '0'}
            </p>
          </div>
        </div>
      </div>
      <p className="t-meta">* Mathematics includes the 25-point Higher Level bonus for grades H1–H6.</p>
    </ExerciseSheet>
  );
};

// ─── INTERACTIVE 2: Maths Bonus Amplifier ───────────────────────────────────

const MathsBonusVisualizer = () => {
  const [mathsGrade, setMathsGrade] = useState('H6');
  const [otherGrade, setOtherGrade] = useState('H3');

  const mathsPts = (GRADE_POINTS[mathsGrade] || 0) + (['H1','H2','H3','H4','H5','H6'].includes(mathsGrade) ? 25 : 0);
  const otherPts = GRADE_POINTS[otherGrade] || 0;
  const mathsId = useId();
  const otherId = useId();

  return (
    <ExerciseSheet title="The Maths Bonus Amplifier" sub="Compare HL Maths (with bonus) to any other subject. See how much difference the 25-point bonus actually makes." name="MathsBonusVisualizer">
      <div className="grid grid-cols-2 gap-6">
        <div className="flex flex-col gap-3">
          <p id={mathsId} className="ex-label">HL Mathematics</p>
          <FieldSelect aria-labelledby={mathsId} value={mathsGrade} onChange={e => setMathsGrade(e.target.value)}>
            {GRADES.map(g => <option key={g} value={g}>{g}</option>)}
          </FieldSelect>
          {/* The points, as a number in ink with its label (no filled square) */}
          <motion.div
            className="flex flex-col"
            animate={{ scale: [1, 1.05, 1] }}
            transition={{ duration: 0.3 }}
            key={mathsGrade}
            style={{ transformOrigin: 'left center' }}
          >
            <span className="t-number text-ink-primary">{mathsPts}</span>
            <span className="ex-label">POINTS</span>
          </motion.div>
          <p className="t-meta">{GRADE_POINTS[mathsGrade]}{['H1','H2','H3','H4','H5','H6'].includes(mathsGrade) ? ' + 25 bonus' : ''}</p>
        </div>

        <div className="flex flex-col gap-3">
          <p id={otherId} className="ex-label">Any Other Subject</p>
          <FieldSelect aria-labelledby={otherId} value={otherGrade} onChange={e => setOtherGrade(e.target.value)}>
            {GRADES.map(g => <option key={g} value={g}>{g}</option>)}
          </FieldSelect>
          <motion.div
            className="flex flex-col"
            key={otherGrade}
          >
            <span className="t-number text-ink-primary">{otherPts}</span>
            <span className="ex-label">POINTS</span>
          </motion.div>
          <p className="t-meta">{GRADE_POINTS[otherGrade]} points (no bonus)</p>
        </div>
      </div>

      {/* The comparison: a line in ink (the tick when Maths comes out ahead or level) */}
      <AnswerLine tone={mathsPts >= otherPts ? 'ok' : 'note'}>
        {mathsPts >= otherPts
          ? `A ${mathsGrade} in Maths (${mathsPts} pts) is worth ${mathsPts - otherPts > 0 ? `${mathsPts - otherPts} points MORE than` : 'the same as'} a ${otherGrade} in any other subject (${otherPts} pts).`
          : `A ${otherGrade} in another subject (${otherPts} pts) beats a ${mathsGrade} in Maths (${mathsPts} pts) by ${otherPts - mathsPts} points.`
        }
      </AnswerLine>
    </ExerciseSheet>
  );
};

// ─── INTERACTIVE 3: Subject H1 Rate Dashboard ──────────────────────────────

/** The dashboard's title, also the name of its sort bar for screen readers. */
const H1_DASHBOARD_TITLE = 'Subject H1 Rate Dashboard';

const H1RateDashboard = () => {
  const [sortBy, setSortBy] = useState<'h1Rate' | 'objectivity' | 'name'>('h1Rate');
  const [showAll, setShowAll] = useState(false);

  const sorted = useMemo(() => {
    const copy = [...SUBJECTS_DATA];
    if (sortBy === 'h1Rate') return copy.sort((a, b) => b.h1Rate - a.h1Rate);
    if (sortBy === 'objectivity') return copy.sort((a, b) => b.objectivity - a.objectivity);
    return copy.sort((a, b) => a.name.localeCompare(b.name));
  }, [sortBy]);

  const displayed = showAll ? sorted : sorted.slice(0, 10);
  const maxRate = Math.max(...SUBJECTS_DATA.map(s => s.h1Rate));

  // The yield is said in words beside each bar (no tinted tag, no colour per bar).
  const getRiskLabel = (rate: number) => {
    if (rate >= 15) return { text: 'High Yield' };
    if (rate >= 10) return { text: 'Moderate' };
    return { text: 'Low Yield' };
  };

  return (
    <ExerciseSheet title={H1_DASHBOARD_TITLE} sub="Indicative H1 rates (illustrative, not official SEC figures). Sort to compare which subjects tend to have higher H1 rates." name="H1RateDashboard">
      {/* The sort: the system's selection bar (one of three short words), named by the sheet's own title */}
      <SelectionBar<string>
        label={H1_DASHBOARD_TITLE}
        value={sortBy}
        onChange={(key) => setSortBy(key as any)}
        options={[
          { key: 'h1Rate', label: 'H1 Rate' },
          { key: 'objectivity', label: 'Objectivity' },
          { key: 'name', label: 'A–Z' },
        ].map(opt => ({ value: opt.key, label: opt.label }))}
      />

      {/* Each subject ruled like a row: its name and yield, then its bar (ink on a hairline track) and rate */}
      <div className="ex-list">
        {displayed.map((subj, idx) => {
          const risk = getRiskLabel(subj.h1Rate);
          return (
            <MotionDiv
              key={subj.name}
              initial={{ opacity: 0, x: -10 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: idx * 0.02 }}
            >
              <div className="flex items-baseline justify-between gap-3">
                <span className="t-sub text-ink-primary">{subj.name}</span>
                <span className="t-meta shrink-0">{risk.text}</span>
              </div>
              <div className="flex items-center gap-3">
                <div className="flex-grow h-2 rounded-full overflow-hidden" style={{ background: 'var(--hairline)' }}>
                  <motion.div
                    className="h-full rounded-full"
                    style={{ background: 'var(--ink-primary)' }}
                    initial={{ width: 0 }}
                    animate={{ width: `${(subj.h1Rate / maxRate) * 100}%` }}
                    transition={{ duration: 0.5, delay: idx * 0.02 }}
                  />
                </div>
                <span className="w-10 shrink-0 text-right ui-readout text-ink-primary">{subj.h1Rate}%</span>
              </div>
            </MotionDiv>
          );
        })}
      </div>

      {!showAll && (
        <div className="ex-actions">
          <TextButton tone="quiet" arrow="menu" onClick={() => setShowAll(true)}>
            Show all {SUBJECTS_DATA.length} subjects
          </TextButton>
        </div>
      )}
      <p className="t-meta">Illustrative relative estimates of recent SEC Leaving Certificate (Higher Level) H1 rates — for ranking subjects, not official published figures. Rates vary a lot year to year (and rose sharply post-2020); check the current SEC examination statistics for exact numbers.</p>
    </ExerciseSheet>
  );
};

// ─── INTERACTIVE 4: Objectivity Spectrum ────────────────────────────────────

const ObjectivitySpectrum = () => {
  const [revealed, setRevealed] = useState(false);
  const sorted = [...SUBJECTS_DATA].sort((a, b) => b.objectivity - a.objectivity);

  return (
    <ExerciseSheet title="The Objectivity Spectrum" sub={'Where does each subject fall between "right/wrong" and "examiner\'s discretion"?'} name="ObjectivitySpectrum">
      {!revealed ? (
        <div className="ex-stack">
          <p className="t-sub">Before you see the data — think about your own subjects. Which do you think have the most objective marking?</p>
          <div className="ex-actions">
            <Button onClick={() => setRevealed(true)}>
              Reveal the Spectrum
            </Button>
          </div>
        </div>
      ) : (
        <div className="ex-stack">
          <div className="flex justify-between gap-4">
            <span className="ex-label">Pure Objective (Right/Wrong)</span>
            <span className="ex-label text-right">Pure Subjective (Discretion)</span>
          </div>
          {/* Each subject on one line: its name, its bar (ink on a hairline track) and its share */}
          <div className="ex-list">
            {sorted.map((subj, idx) => (
              <MotionDiv
                key={subj.name}
                initial={{ opacity: 0, scale: 0.95 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ delay: idx * 0.03 }}
              >
                <div className="flex items-center gap-3">
                  <span className="w-36 shrink-0 t-sub text-ink-primary">{subj.name}</span>
                  <div className="flex-grow h-2 rounded-full overflow-hidden" style={{ background: 'var(--hairline)' }}>
                    <motion.div
                      className="h-full rounded-full"
                      style={{ background: 'var(--ink-primary)' }}
                      initial={{ width: 0 }}
                      animate={{ width: `${subj.objectivity}%` }}
                      transition={{ duration: 0.6, delay: idx * 0.03 }}
                    />
                  </div>
                  <span className="w-10 shrink-0 text-right ui-readout text-ink-muted">{subj.objectivity}%</span>
                </div>
              </MotionDiv>
            ))}
          </div>
          {/* The pattern: words you read, under a hairline (no box) */}
          <div className="ex-block">
            <p className="ex-block-text">
              <strong className="text-ink-primary">The pattern is clear:</strong> STEM subjects and Maths sit at the objective end — a right answer gets full marks, no question. Humanities and Arts sit at the subjective end, where different examiners might give different marks. If you want to reduce surprise on exam day, having more objective subjects in your mix helps.
            </p>
          </div>
        </div>
      )}
    </ExerciseSheet>
  );
};

// ─── INTERACTIVE 5: Subject Synergy Map ─────────────────────────────────────

const SynergyMap = ({ savedSubjects, onSave }: { savedSubjects?: string[]; onSave?: (subjects: string[]) => void }) => {
  const [selected, setSelected] = useState<string[]>(savedSubjects || []);

  useEffect(() => {
    if (savedSubjects) setSelected(savedSubjects);
  }, [savedSubjects]);

  const toggleSubject = (name: string) => {
    let next: string[];
    if (selected.includes(name)) {
      next = selected.filter(s => s !== name);
    } else if (selected.length < 7) {
      next = [...selected, name];
    } else {
      return;
    }
    setSelected(next);
    onSave?.(next);
  };

  const activeSynergies = useMemo(() => {
    const links: { from: string; to: string }[] = [];
    selected.forEach(subj => {
      const data = SUBJECTS_DATA.find(s => s.name === subj);
      if (data) {
        data.synergies.forEach(syn => {
          if (selected.includes(syn) && !links.find(l => (l.from === syn && l.to === subj))) {
            links.push({ from: subj, to: syn });
          }
        });
      }
    });
    return links;
  }, [selected]);

  return (
    <ExerciseSheet title="Subject Overlap Map" sub="Select up to 7 subjects and see which share overlapping content — study one, benefit in another." name="SynergyMap">
      <p className="ex-count ui-readout" aria-live="polite">{selected.length}/7 selected</p>

      {/* Each subject is an answer you choose (up to seven): an ink outline and a tick, no colour per group */}
      <AnswerGroup kind="several" columns={2}>
        {SUBJECTS_DATA.map(subj => {
          const isSelected = selected.includes(subj.name);
          return (
            <ChoiceTile
              key={subj.name}
              kind="several"
              chosen={isSelected}
              onClick={() => toggleSubject(subj.name)}
              label={<>{subj.name}{subj.isMaths ? ' *' : ''}</>}
            />
          );
        })}
      </AnswerGroup>

      {/* What overlaps: under a hairline and its label; each pair ruled like a row with the green tick (no box) */}
      {selected.length > 0 && (
        <div className="ex-block">
          <div className="flex items-center justify-between gap-3">
            <p className="ex-label">Overlapping Subjects</p>
            <p className="ui-readout text-ink-primary">{activeSynergies.length} found</p>
          </div>
          {activeSynergies.length > 0 ? (
            <div className="ex-list">
              {activeSynergies.map((link, i) => (
                <MotionDiv key={i} initial={{ opacity: 0, x: -10 }} animate={{ opacity: 1, x: 0 }} transition={{ delay: i * 0.05 }}>
                  <div className="flex items-center gap-2 t-sub text-ink-primary">
                    <span>{link.from}</span>
                    <span className="text-ink-muted"></span>
                    <span>{link.to}</span>
                    <AnswerTick className="ml-auto" />
                  </div>
                </MotionDiv>
              ))}
            </div>
          ) : (
            <p className="t-sub">No overlap between your selected subjects yet. Try adding STEM or language pairs.</p>
          )}
        </div>
      )}
    </ExerciseSheet>
  );
};

// ─── INTERACTIVE 6: SRP Surplus Calculator ──────────────────────────────────

const SurplusCalculator = () => {
  const [questionMarks, setQuestionMarks] = useState(30);
  const [marksPerPoint, setMarksPerPoint] = useState(3);
  const [pointsWritten, setPointsWritten] = useState(10);

  const requiredPoints = Math.ceil(questionMarks / marksPerPoint);
  const surplusPoints = pointsWritten - requiredPoints;
  const safetyMargin = surplusPoints > 0 ? Math.round((surplusPoints / requiredPoints) * 100) : 0;

  return (
    <ExerciseSheet title="The Surplus Rule Calculator" sub="Marking schemes often accept more valid answers than the question needs. Calculate your safety margin." name="SurplusCalculator">
      {/* Three steppers: each its label, a white button with a line either side of the number in ink, and its unit */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="flex flex-col gap-2">
          <p className="ex-label">Question Worth</p>
          <div className="flex items-center gap-2">
            <Button size="sm" aria-label="Decrease" onClick={() => setQuestionMarks(Math.max(5, questionMarks - 5))}><Glyph icon={Minus} size={16} /></Button>
            <span className="t-heading text-ink-primary w-12 text-center tabular-nums">{questionMarks}</span>
            <Button size="sm" aria-label="Increase" onClick={() => setQuestionMarks(Math.min(100, questionMarks + 5))}><Glyph icon={Plus} size={16} /></Button>
            <span className="t-meta">marks</span>
          </div>
        </div>
        <div className="flex flex-col gap-2">
          <p className="ex-label">Marks per Point</p>
          <div className="flex items-center gap-2">
            <Button size="sm" aria-label="Decrease" onClick={() => setMarksPerPoint(Math.max(1, marksPerPoint - 1))}><Glyph icon={Minus} size={16} /></Button>
            <span className="t-heading text-ink-primary w-12 text-center tabular-nums">{marksPerPoint}</span>
            <Button size="sm" aria-label="Increase" onClick={() => setMarksPerPoint(Math.min(10, marksPerPoint + 1))}><Glyph icon={Plus} size={16} /></Button>
            <span className="t-meta">each</span>
          </div>
        </div>
        <div className="flex flex-col gap-2">
          <p className="ex-label">Points You Write</p>
          <div className="flex items-center gap-2">
            <Button size="sm" aria-label="Decrease" onClick={() => setPointsWritten(Math.max(1, pointsWritten - 1))}><Glyph icon={Minus} size={16} /></Button>
            <span className="t-heading text-ink-primary w-12 text-center tabular-nums">{pointsWritten}</span>
            <Button size="sm" aria-label="Increase" onClick={() => setPointsWritten(Math.min(20, pointsWritten + 1))}><Glyph icon={Plus} size={16} /></Button>
            <span className="t-meta">SRPs</span>
          </div>
        </div>
      </div>

      {/* The three results: labels and numbers in ink under a hairline (no tinted boxes) */}
      <div className="ex-result">
        <div className="grid grid-cols-3 gap-4">
          <div>
            <p className="ex-label">Required</p>
            <p className="t-heading text-ink-primary">{requiredPoints} SRPs</p>
          </div>
          <div>
            <p className="ex-label">Surplus</p>
            <p className="t-heading text-ink-primary">
              {surplusPoints > 0 ? `+${surplusPoints}` : surplusPoints}
            </p>
          </div>
          <div>
            <p className="ex-label">Safety</p>
            <p className="t-heading text-ink-primary">{safetyMargin}%</p>
          </div>
        </div>
      </div>

      {/* What the margin means: a line in ink (the tick for a strong surplus) */}
      {surplusPoints >= 2 && (
        <AnswerLine>
          Strong surplus. Even if {surplusPoints} of your points are rejected, you still get full marks.
        </AnswerLine>
      )}
      {surplusPoints >= 0 && surplusPoints < 2 && (
        <AnswerLine tone="note">
          Thin margin. Add {2 - surplusPoints} more points to build a safe buffer.
        </AnswerLine>
      )}
      {surplusPoints < 0 && (
        <AnswerLine tone="note">
          You're writing fewer points than required. You will lose marks. Write at least {requiredPoints + 2} SRPs.
        </AnswerLine>
      )}
    </ExerciseSheet>
  );
};

// ─── INTERACTIVE 7: Portfolio Optimizer ──────────────────────────────────────

const DEFAULT_PORTFOLIO = [
  { subject: 'Mathematics', confidence: 'H2' },
  { subject: 'English', confidence: 'H2' },
  { subject: 'Irish', confidence: 'H3' },
  { subject: '', confidence: 'H2' },
  { subject: '', confidence: 'H2' },
  { subject: '', confidence: 'H2' },
  { subject: '', confidence: 'H3' },
];

const PortfolioOptimizer = ({ savedPortfolio, onSave }: { savedPortfolio?: { subject: string; confidence: string }[]; onSave?: (portfolio: { subject: string; confidence: string }[]) => void }) => {
  const [portfolio, setPortfolio] = useState<{ subject: string; confidence: string }[]>(savedPortfolio || DEFAULT_PORTFOLIO);

  useEffect(() => {
    if (savedPortfolio) setPortfolio(savedPortfolio);
  }, [savedPortfolio]);

  const updateSubject = (idx: number, subject: string) => {
    const next = [...portfolio];
    next[idx] = { ...next[idx], subject };
    setPortfolio(next);
    onSave?.(next);
  };

  const updateConfidence = (idx: number, confidence: string) => {
    const next = [...portfolio];
    next[idx] = { ...next[idx], confidence };
    setPortfolio(next);
    onSave?.(next);
  };

  const analysis = useMemo(() => {
    const filled = portfolio.filter(p => p.subject);
    const points = filled.map(p => {
      let pts = GRADE_POINTS[p.confidence] || 0;
      const data = SUBJECTS_DATA.find(s => s.name === p.subject);
      if (data?.isMaths && ['H1','H2','H3','H4','H5','H6'].includes(p.confidence)) pts += 25;
      return { ...p, pts, data };
    });

    const sorted = [...points].sort((a, b) => b.pts - a.pts);
    const bestSix = sorted.slice(0, 6);
    const totalPts = bestSix.reduce((s, p) => s + p.pts, 0);

    const avgObjectivity = filled.length > 0
      ? Math.round(filled.reduce((s, p) => s + (SUBJECTS_DATA.find(d => d.name === p.subject)?.objectivity || 50), 0) / filled.length)
      : 0;

    const h1Count = filled.filter(p => p.confidence === 'H1').length;
    const riskSubjects = filled.filter(p => {
      const d = SUBJECTS_DATA.find(subj => subj.name === p.subject);
      return d && d.objectivity < 50;
    });

    return { totalPts, avgObjectivity, h1Count, riskSubjects, filledCount: filled.length };
  }, [portfolio]);

  const availableSubjects = SUBJECTS_DATA.map(s => s.name);

  return (
    <ExerciseSheet title="Your Portfolio Optimizer" sub="Enter your 7 subjects and your current realistic grade expectation. Get a personalized risk report." name="PortfolioOptimizer">
      {/* Seven rows: the number, the subject field and the grade field (the native selects, kept as they work today) */}
      <div className="ex-stack">
        {portfolio.map((item, idx) => (
          <div key={idx} className="flex items-center gap-3">
            <span className="ui-readout text-ink-muted w-4 shrink-0">{idx + 1}</span>
            <FieldSelect className="flex-grow min-w-0" value={item.subject} onChange={e => updateSubject(idx, e.target.value)}>
              <option value="">Select subject...</option>
              {availableSubjects.map(s => <option key={s} value={s}>{s}{s === 'Mathematics' ? ' (+ bonus)' : ''}</option>)}
            </FieldSelect>
            <FieldSelect className="w-24 shrink-0" value={item.confidence} onChange={e => updateConfidence(idx, e.target.value)}>
              {GRADES.map(g => <option key={g} value={g}>{g}</option>)}
            </FieldSelect>
          </div>
        ))}
      </div>

      {/* The risk report: labels and numbers in ink under a hairline (no tinted panel, no colour for the gap) */}
      {analysis.filledCount >= 4 && (
        <MotionDiv initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} className="ex-result">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div>
              <p className="ex-label">Projected Points</p>
              <p className="t-heading text-ink-primary">{analysis.totalPts}<span className="t-sub">/625</span></p>
            </div>
            <div>
              <p className="ex-label">Objectivity</p>
              <p className="t-heading text-ink-primary">{analysis.avgObjectivity}%</p>
            </div>
            <div>
              <p className="ex-label">H1 Confident</p>
              <p className="t-heading text-ink-primary">{analysis.h1Count}/{analysis.filledCount}</p>
            </div>
            <div>
              <p className="ex-label">Gap to 625</p>
              <p className="t-heading text-ink-primary">
                {analysis.totalPts >= 625 ? '0' : `-${625 - analysis.totalPts}`}
              </p>
            </div>
          </div>

          {/* The warning: the bare glyph in ink-3 beside the words (no box) */}
          {analysis.riskSubjects.length > 0 && (
            <div className="flex items-start gap-2 mt-3">
              <AlertTriangle size={16} className="shrink-0 mt-0.5 text-ink-muted" />
              <p className="t-sub text-ink-primary">
                <strong>Watch out for these:</strong> {analysis.riskSubjects.map(s => s.subject).join(', ')}. These have subjective marking — your grade could depend on which examiner reads your paper. Put extra time into learning exactly what the marking scheme rewards for these subjects.
              </p>
            </div>
          )}
        </MotionDiv>
      )}
    </ExerciseSheet>
  );
};

// ─── MODULE COMPONENT ───────────────────────────────────────────────────────

const PointsOptimizationModule: React.FC<{
  onBack: () => void;
  progress: ModuleProgress;
  onProgressUpdate: (progress: ModuleProgress) => void;
}> = ({ onBack, progress, onProgressUpdate }) => {
  const essentials = useEssentialsMode();
  const { responses, saveResponse, isLoaded: _isLoaded } = useModuleResponses('the-625-blueprint');

  const sections = [
    { id: 'the-cliff', title: 'The 12-Point Cliff', eyebrow: '01 // How Points Really Work', icon: TrendingDown },
    { id: 'maths-multiplier', title: 'The Maths Multiplier', eyebrow: '02 // The 25-Point Bonus', icon: Calculator },
    { id: 'h1-probability', title: 'H1 Probability Map', eyebrow: '03 // The Data', icon: BarChart3 },
    { id: 'objectivity-advantage', title: 'The Objectivity Advantage', eyebrow: '04 // Reducing Exam-Day Risk', icon: Scale },
    { id: 'synergy-blocks', title: 'Subject Overlap', eyebrow: '05 // Study Smarter', icon: GitBranch },
    { id: 'surplus-rule', title: 'The Surplus Rule', eyebrow: '06 // Banking Extra Marks', icon: Layers },
    { id: 'your-blueprint', title: 'Your 625 Blueprint', eyebrow: '07 // Your Personal Plan', icon: Target },
  ];

  return (
    <ModuleLayout
      moduleNumber="09"
      moduleTitle="The 625 Blueprint"
      moduleSubtitle="How to Maximise Your Points"
      moduleDescription="The Leaving Cert is a points game — and there are smart ways to play it. Use real data on H1 rates, how points really work, and marking scheme tricks to get the most points you can."
      theme={theme}
      sections={sections}
      onBack={onBack}
      progress={progress}
      onProgressUpdate={onProgressUpdate}
      references={POINTS_OPTIMIZATION_REFERENCE_LIST}
      finishButtonText="Maximise Your Points"
    >
      {(activeSection) => (
        <>
          {activeSection === 0 && (
            <ReadingSection title="The 12-Point Cliff." eyebrow="Step 1" icon={TrendingDown} theme={theme}>
              {essentials ? (
                <>
                  <p>The most important number: <Highlight description="H1 to H2 costs you 12 points — the steepest drop in the system." theme={theme}>12</Highlight>. That is how many points you lose dropping from H1 to H2. The difference between 89% and 90% is 12 CAO points.<Cite n={1} /> No other boundary hits this hard. If you are chasing 625, you cannot afford a single H2 in your best six. Aim for 93-95% in practice as a buffer.</p>
                  <PersonalStory name="Alex" role="Founder, NextStepUni">
                    <p>I went from failing my Junior Cert to nearly 600 points in the Leaving Cert. If someone had shown me this data — how the points really work, the maths bonus, the H1 rates — when I was in 4th year, I would have saved months of wasted effort. The system has rules, and once you understand them, you stop feeling like the game is rigged against you and start playing it smart. That's what this module is for.</p>
                  </PersonalStory>
                </>
              ) : (
                <>
                  <p>Here is the single most important number in the Leaving Cert: <Highlight description="Going from an H1 (100 points) to an H2 (88 points) costs you 12 points — that's the biggest single drop between any two passing grades." theme={theme}>12</Highlight>. That's how many points you lose the moment you drop from an H1 to an H2. It's the steepest cliff in the entire grading system.</p>
                  <p>Think about what that means. The difference between 89% and 90% in a single exam is not 1 point — it's <strong>12 points</strong> on the CAO scale. No other grade boundary hits this hard. The drop from H2 to H3 is 11 points. From H3 to H4, it's also 11. But H1 to H2? That 12-point cliff means that if you're chasing 625, there's almost no room for error.<Cite n={1} /> You can't afford a single H2 in your best six subjects.</p>
                  <p>This isn't about being a perfectionist — it's about understanding how the system actually works. The grading system was redesigned in 2017, but at the very top, it accidentally created the most punishing boundary on the entire scale. A student scoring 89% and a student scoring 90% are separated by a single percentage point — but <strong>12 CAO points</strong>.</p>
                  <PersonalStory name="Alex" role="Founder, NextStepUni">
                    <p>I went from failing my Junior Cert to nearly 600 points in the Leaving Cert. If someone had shown me this data — how the points really work, the maths bonus, the H1 rates — when I was in 4th year, I would have saved months of wasted effort. The system has rules, and once you understand them, you stop feeling like the game is rigged against you and start playing it smart. That's what this module is for.</p>
                  </PersonalStory>
                  <p>So what do you do about it? You don't just aim for 90%. You aim for 93-95% in practice — building a buffer that protects you from a bad day, unexpected questions, or tough marking. Use the calculator below to see exactly how each grade drop affects your total.</p>
                </>
              )}
              <GradeWaterfall />
              <MicroCommitment theme={theme}>
                <p>Enter your current realistic grades into the calculator above. What's your projected total? Now change just ONE subject from H2 to H1 — notice the 12-point jump. That's the subject to prioritise this week.</p>
              </MicroCommitment>
            </ReadingSection>
          )}

          {activeSection === 1 && (
            <ReadingSection title="The Maths Multiplier." eyebrow="Step 2" icon={Calculator} theme={theme}>
              {essentials ? (
                <p>HL Maths has a <Highlight description="25 extra CAO points for HL Maths, H6 or above." theme={theme}>25-point bonus</Highlight>. An H1 gives you 125 points. Even an H6 (barely a pass) gives you 71 points — nearly the same as an H3 in any other subject.<Cite n={1} /> Every hour in HL Maths is worth more points than any other subject. If you are chasing 625, HL Maths is the foundation.</p>
              ) : (
                <>
                  <p>Higher Level Maths has a secret weapon that no other subject has: the <Highlight description="You get an extra 25 CAO points just for doing Higher Level Maths, as long as you get at least an H6. No other subject gives you this." theme={theme}>25-point bonus</Highlight>. This single rule makes HL Maths the most valuable subject on the Leaving Cert — by a long way.</p>
                  <p>Let's do the maths on the Maths. An H1 in Higher Level Maths gives you <strong>125 points</strong> (100 + 25 bonus). That's 25% more than the max in any other subject. But the bonus isn't just for top students. An H6 in HL Maths (that's 40-49%, barely a pass) gives you 46 + 25 = <strong>71 points</strong>. That's nearly the same as an H3 (77 points) in any other subject — where you'd need 70-79% to earn a similar reward.<Cite n={1} /></p>
                  <p>The bottom line: <strong>every hour you put into HL Maths is worth more points than the same hour in any other subject</strong>. Even if Maths is your weakest subject, the bonus points give you a cushion that makes the extra effort worth it. If you're chasing 625, HL Maths isn't optional — it's the foundation of the whole plan.</p>
                </>
              )}
              <MathsBonusVisualizer />
              <MicroCommitment theme={theme}>
                <p>Use the tool above. Set Maths to H6 (a bare pass) and compare it to an H3 in another subject. The fact that similar points come from very different percentages should change how you spend your study time this week.</p>
              </MicroCommitment>
            </ReadingSection>
          )}

          {activeSection === 2 && (
            <ReadingSection title="H1 Probability Map." eyebrow="Step 3" icon={BarChart3} theme={theme}>
              {essentials ? (
                <p>Your <Highlight description="H1 rates vary hugely by subject." theme={theme}>chances of getting an H1</Highlight> depend on the subject. Applied Maths and the sciences have some of the highest H1 rates; subjects like English, Geography and Art are among the lowest.<Cite n={2} /> Use this to decide where you spend your study time. Protect subjects with high H1 rates. Put extra effort into exam technique for subjects where H1s are rare.</p>
              ) : (
                <>
                  <p>Not all H1s are created equal. The SEC's own published data shows huge differences in the percentage of students who get H1s across different subjects.<Cite n={2} /> The figures here are approximate, indicative of recent years' distributions. This isn't necessarily because some subjects are "easier" — it's because your <Highlight description="Your chances of getting an H1 depend on the subject itself — how it's marked, how big the course is, and who else takes it. Some subjects just have way higher H1 rates than others." theme={theme}>chances of getting an H1</Highlight> depend on the subject, how it's marked, and who else takes it.</p>
                  <p>Applied Maths has one of the highest H1 rates of any subject (recently well above 25%, though notably lower before the pandemic). The course is focused, the exam is pure problem-solving, and the marking is black and white — you either got it right or you didn't. The students who pick it tend to be strong at maths already, which pushes the rates up — but for anyone decent at maths, it's one of the easiest H1s to get.</p>
                  <p>Physics and Chemistry also sit relatively high among the sciences — they reward precision: exact definitions, correct formulae, and mathematical accuracy, marked against strict schemes. Meanwhile, English — which everyone has to do — has one of the lowest H1 rates of the major subjects (only a few percent in most years), and Geography is similarly low. When marking is more subjective, your grade depends partly on which examiner reads your paper.</p>
                  <p>This data should shape both your subject choices and, just as importantly, <strong>where you spend your study time</strong>. If you're already taking a subject with a high H1 rate, protect that advantage. If you're in a subject where H1s are rare, you'll need to put extra time into nailing the exam technique to make up for the tougher marking.</p>
                </>
              )}
              <H1RateDashboard />
              <MicroCommitment theme={theme}>
                <p>Sort the dashboard by H1 Rate. Find your own subjects in the list. Are you spending the most study time on the subjects where H1s are easiest or hardest to get? The answer might surprise you.</p>
              </MicroCommitment>
            </ReadingSection>
          )}

          {activeSection === 3 && (
            <ReadingSection title="The Objectivity Advantage." eyebrow="Step 4" icon={Scale} theme={theme}>
              {essentials ? (
                <p><Highlight description="How much marking is right/wrong vs. examiner's judgement." theme={theme}>Objectivity</Highlight> affects your control over your grade. In Maths, a right answer gets full marks. In English, your essay grade partly depends on your examiner. More objective subjects in your mix means less exam-day risk. For subjective subjects, learn exactly what the marking scheme rewards.</p>
              ) : (
                <>
                  <p>There's a hidden factor that affects how much control you actually have over your grade: the <Highlight description="How much the marking is black-and-white (right or wrong answers) versus up to the examiner's judgement. In Maths, if you get the answer right, you get the marks. In English, two examiners might give the same essay different marks." theme={theme}>objectivity</Highlight> of the marking scheme. In Maths, a correct answer is a correct answer — the examiner can't withhold marks. In English, a brilliant essay might not click with a particular examiner.</p>
                  <p>This isn't a dig at subjective subjects — they test different and equally valuable skills. But when it comes to getting the most points possible, the difference matters a lot. In objective subjects (Maths, Physics, Chemistry, Applied Maths, Accounting), there's a simple rule: <strong>if you know it, you get the marks</strong>. In subjective subjects (English, History, Art, Geography), there's always some element of luck on the day.</p>
                  <p>If you're trying to maximise your points, it helps to have more objective subjects in your mix. That doesn't mean avoiding subjective subjects — English and Irish are compulsory, and plenty of students do brilliantly in the humanities. But it means knowing that for every subjective subject you take, there's more exam-day risk, and you need to put extra work into nailing the marking criteria.</p>
                </>
              )}
              <ObjectivitySpectrum />
              <MicroCommitment theme={theme}>
                <p>Count how many of your subjects sit above 70% objectivity and how many sit below 50%. If most of yours are on the subjective side, your priority this term should be learning exactly what the examiner is looking for — check the marking scheme and practise giving them exactly that.</p>
              </MicroCommitment>
            </ReadingSection>
          )}

          {activeSection === 4 && (
            <ReadingSection title="Subject Overlap." eyebrow="Step 5" icon={GitBranch} theme={theme}>
              {essentials ? (
                <p>Your subjects share <Highlight description="Studying one subject helps you in another when content overlaps." theme={theme}>hidden connections</Highlight>. The Maths-Applied Maths-Physics block gives you a 3-for-1 deal on mechanics. Biology-Chemistry-Ag Science overlap on organic chemistry. Languages share grammar structures. Select your subjects below to see your overlaps.</p>
              ) : (
                <>
                  <p>The smartest students don't just study seven separate subjects — they take advantage of the <Highlight description="When two subjects cover similar material, studying for one helps you in the other. It's like a 2-for-1 deal on study time." theme={theme}>hidden connections</Highlight> between them. The Leaving Cert curriculum is full of overlapping content, and picking the right combination of subjects can seriously cut down on how much you need to learn overall.</p>
                  <p>Take the "Maths Block": Higher Maths, Applied Maths, and Physics. The mechanics section of Physics overlaps massively with Applied Maths. Calculus in Maths helps with both. If you're doing all three, you're basically getting a 3-for-1 deal on certain topics. The "Life Science Block" (Biology, Chemistry, Ag Science) works the same way — organic chemistry shows up in both Chemistry and Biology, and Ag Science leans on chemical concepts too.</p>
                  <p>Even languages help each other — grammar structures and essay techniques from French carry over to Spanish and German. The key question isn't just "what subjects do I like?" but "which of my subjects help each other when I study them together?"</p>
                </>
              )}
              <SynergyMap savedSubjects={responses['synergy-subjects']} onSave={(s) => saveResponse('synergy-subjects', s)} />
              <MicroCommitment theme={theme}>
                <p>Select your actual subjects in the tool above. How many connections light up? If you're getting zero, think about whether you could rearrange your study timetable to study overlapping subjects back-to-back in the same session.</p>
              </MicroCommitment>
            </ReadingSection>
          )}

          {activeSection === 5 && (
            <ReadingSection title="The Surplus Rule." eyebrow="Step 6" icon={Layers} theme={theme}>
              {essentials ? (
                <p>Marking schemes often list <Highlight description="Write more valid points than needed as a safety net." theme={theme}>more valid answers than required</Highlight>. Write a few extra points as insurance. If two get rejected, you still hit full marks. This works in Biology, Geography, History, and Business.<Cite n={3} /> Write the minimum plus three extra. Use the calculator below.</p>
              ) : (
                <>
                  <p>Here's something most students don't know: in many subjects, the marking scheme has <Highlight description="The marking scheme often lists way more valid points than the question actually needs. So you can write extra points as a safety net — if a couple get rejected, the examiner keeps reading until you hit full marks." theme={theme}>more valid answers than the question requires</Highlight>. This is the Surplus Rule, and it's the closest thing to a guaranteed-marks trick in the Leaving Cert.</p>
                  <p>Here's how it works. A 30-mark question in Biology might need 10 Significant Relevant Points (SRPs) at 3 marks each. But the marking scheme might list 20 valid points. If you write exactly 10 and the examiner rejects 2 as incomplete or off-topic, you score 24/30. But if you write 13 points, you've built in a safety net. The examiner reads until they've given you 30 marks, then stops. There's no penalty for writing extra correct information.</p>
                  <p>This works in Biology, Geography, History, Business, and loads of other subjects that use SRP-based marking.<Cite n={3} /> Students who get H1s don't just write the minimum — they write the minimum plus a few extra points as insurance. The exact number depends on the question.</p>
                </>
              )}
              <SurplusCalculator />
              <MicroCommitment theme={theme}>
                <p>Pick your most SRP-heavy subject. Find a past paper question and its marking scheme. Count the required SRPs. Now practice answering with a surplus of +3. Time yourself — the surplus should cost you less than 2 extra minutes per question.</p>
              </MicroCommitment>
            </ReadingSection>
          )}

          {activeSection === 6 && (
            <ReadingSection title="Your 625 Blueprint." eyebrow="Step 7" icon={Target} theme={theme}>
              {essentials ? (
                <>
                  <p>Pull everything together into a <Highlight description="Your subjects, projected points, risk areas, and what to focus on." theme={theme}>personal plan</Highlight>. Enter your seven subjects and honest grade expectations below. The gap between your total and 625 is your action plan. Each H2-to-H1 jump is worth 12 points. Focus on subjects with the highest H1 rates first.</p>
                  <PersonalStory name="Ciara" role="6th Year, Galway">
                    <p>I was doing seven subjects and putting equal time into all of them. When I actually sat down and looked at the H1 rates and how objective each subject was, I realised I was spending hours on English essays that might get me 2 extra points, while ignoring Applied Maths where the same effort could have got me 12. Once I shifted my study time around, my mock results jumped by nearly 40 points.</p>
                  </PersonalStory>
                </>
              ) : (
                <>
                  <p>You now have the data. You understand how the points really work, the maths bonus, where H1s are easiest and hardest to get, the objectivity advantage, how subjects overlap, and the surplus rule. The final step is to pull it all together into a <Highlight description="A personalised look at your specific subjects, your projected points total, where you're at risk, and what to focus on to improve." theme={theme}>personal plan</Highlight>.</p>
                  <p>Use the Portfolio Optimizer below to enter your actual seven subjects and your honest, current grade expectations. Not your target grades — your realistic prediction based on how you're actually doing right now. The tool will calculate your projected total, objectivity score, and flag your highest-risk subjects.</p>
                  <p>The result isn't a judgement — it's a starting point. If your projected total is 560, you're not "failing." You're 65 points away, which means you need to bump roughly 5-6 subjects from H2 to H1. That's your plan for the year. Each H2-to-H1 jump is worth 12 points. Focus on the subjects where the jump is most realistic — usually your subjects with the highest H1 rates and most objective marking.</p>
                  <PersonalStory name="Ciara" role="6th Year, Galway">
                    <p>I was doing seven subjects and putting equal time into all of them. When I actually sat down and looked at the H1 rates and how objective each subject was, I realised I was spending hours on English essays that might get me 2 extra points, while ignoring Applied Maths where the same effort could have got me 12. Once I shifted my study time around, my mock results jumped by nearly 40 points.</p>
                  </PersonalStory>
                  <p>One more thing: recent H1 rates have been unusually high by historical standards,<Cite n={2} /> and the temporary post-pandemic grade adjustments are being wound down — so today's rates may not hold. It is sensible to prepare for tougher marking — aiming for 93-95% in practice to safely clear the 90% H1 threshold on exam day. The buffer is your safety net.</p>
                </>
              )}
              <PortfolioOptimizer savedPortfolio={responses['portfolio']} onSave={(p) => saveResponse('portfolio', p)} />
              <MicroCommitment theme={theme}>
                <p>Complete the Portfolio Optimizer with your real subjects and honest grade expectations. Screenshot the result. This is your 625 Blueprint — the gap between your projected total and 625 is exactly what you need to close between now and June.</p>
              </MicroCommitment>
              <ToolJumpCard
                toolId="cao-simulator"
                title="Run your portfolio through Points Passport"
                description="Use the Grade Planner to see exactly how each subject changes your best-six total. Test different combinations without doing the maths yourself."
                ctaLabel="Open the Grade Planner"
              />
            </ReadingSection>
          )}
        </>
      )}
    </ModuleLayout>
  );
};

export default PointsOptimizationModule;
