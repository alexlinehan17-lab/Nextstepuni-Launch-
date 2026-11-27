/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */
import React, { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import { RefreshCw } from 'lucide-react';
import { getFunctions, httpsCallable } from 'firebase/functions';
import app from '../firebase';
import { type CourseData } from './Library';
import { TextButton } from './ui/Button';
import { SelectionBar } from './ui/Choice';
import { ErrorState, LoadingShape } from './ui/States';
import { Fig } from './gc/gcView';

type Ratio = {
  numerator: number | null;
  denominator: number | null;
  percentage: number | null;
  suppressed?: boolean;
};

type ProgrammeSummary = {
  enabled?: boolean;
  rangeDays: 7 | 28 | 84;
  rangeStart?: string;
  rangeEnd?: string;
  generatedAt: string;
  suppressed: boolean;
  suppressionMinimum: number;
  registeredStudents: number | null;
  measurementStartedOn?: string | null;
  eligibleStudents?: number | null;
  activation?: Ratio;
  weeklyParticipation?: Ratio;
  fourWeekRetention?: Ratio;
  planActivitiesCompleted?: number | null;
  studySessionsCompleted?: number | null;
  practiceAttemptsCompleted?: number | null;
  strongPracticeAttempts?: number | null;
  strongPracticePercentage?: number | null;
  averageConfidence?: number | null;
  confidenceResponses?: number | null;
  featureRows?: Array<{
    id: string;
    exposed: number | null;
    started: number;
    completed: number | null;
    successRate: number | null;
  }>;
  weeklyTrend?: Array<{ weekStart: string; activeStudents: number | null }>;
  coverage?: {
    eventCount: number | null;
    studentsWithAnalyticsId: number | null;
    studentsWithRegistrationDate: number | null;
  };
  awaitingProgrammeInput?: string[];
};

interface Props {
  schoolFilter: string;
  yearFilter: string;
  allCourses: CourseData[];
  /** Laid out for a laptop (beside the staff sidebar): every column of the feature table. */
  wide?: boolean;
}

const RANGE_OPTIONS = [
  { days: 7 as const, label: '7 days' },
  { days: 28 as const, label: '28 days' },
  { days: 84 as const, label: '12 weeks' },
];

function readableDate(day?: string): string {
  if (!day) return '';
  return new Intl.DateTimeFormat('en-IE', { day: 'numeric', month: 'short' }).format(new Date(`${day}T12:00:00Z`));
}

function sentenceCaseId(value: string): string {
  return value
    .replace(/^module:/, '')
    .split('-')
    .map(word => word.charAt(0).toUpperCase() + word.slice(1))
    .join(' ');
}

/** A count with its thousands comma ("3,690"). */
function countWords(value: number | string | null | undefined): string {
  return typeof value === 'number' ? value.toLocaleString('en-IE') : String(value ?? '');
}

/** A figure whose comma or decimal point keeps its own narrow width; only the digits are tabular. */
function figureWords(text: string): React.ReactNode {
  return text.split(/([.,])/).map((part, index) => (part === '.' || part === ',' ? <span key={index} className="adm-pu">{part}</span> : part));
}

/** The time the summary was worked out, for "Data as of 10:42" (never a machine date). */
function asOfTime(generatedAt?: string): string | null {
  if (!generatedAt) return null;
  const at = new Date(generatedAt);
  return Number.isNaN(at.getTime()) ? null : at.toLocaleTimeString('en-IE', { hour: '2-digit', minute: '2-digit' });
}

const AdminProgrammePanel: React.FC<Props> = ({ schoolFilter, yearFilter, allCourses, wide = false }) => {
  const [rangeDays, setRangeDays] = useState<7 | 28 | 84>(28);
  const [summary, setSummary] = useState<ProgrammeSummary | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState('');
  const [reloadToken, setReloadToken] = useState(0);
  const requestVersionRef = useRef(0);

  const load = useCallback(async () => {
    const requestVersion = ++requestVersionRef.current;
    setIsLoading(true);
    setError('');
    setSummary(null);
    try {
      const getSummary = httpsCallable<
        { rangeDays: 7 | 28 | 84; schoolId: string; yearGroup: string },
        ProgrammeSummary
      >(getFunctions(app), 'getProgrammeAnalyticsSummary');
      const response = await getSummary({
        rangeDays,
        schoolId: schoolFilter === '__not_set__' ? 'not-set' : schoolFilter,
        yearGroup: yearFilter === '__not_set__' ? 'not-set' : yearFilter,
      });
      if (requestVersion === requestVersionRef.current) setSummary(response.data);
    } catch (loadError) {
      if (requestVersion !== requestVersionRef.current) return;
      console.error('Programme analytics summary could not be loaded:', loadError);
      setError('Programme evidence could not be loaded. The measurement functions may still need to be deployed.');
    } finally {
      if (requestVersion === requestVersionRef.current) setIsLoading(false);
    }
  }, [rangeDays, reloadToken, schoolFilter, yearFilter]);

  useEffect(() => {
    void load();
    return () => { requestVersionRef.current += 1; };
  }, [load]);

  const courseTitleById = useMemo(() => new Map(allCourses.map(course => [course.id, course.title])), [allCourses]);
  const featureLabel = (id: string) => {
    if (id.startsWith('module:')) return courseTitleById.get(id.slice(7)) || sentenceCaseId(id);
    if (id === 'study-session') return 'Study sessions';
    if (id === 'study-planner') return 'Study planner';
    return sentenceCaseId(id);
  };

  if (isLoading && !summary) {
    return <LoadingShape rows={4} label="Loading programme evidence" />;
  }

  if (error && !summary) {
    return (
      <ErrorState
        sentence={<><span className="adm-ink">Programme evidence is unavailable</span><br />{error}</>}
        onRetry={() => setReloadToken(value => value + 1)}
      />
    );
  }

  if (!summary) return null;

  if (summary.enabled === false) {
    return (
      <section className="gc8-sec adm-state">
        <p className="gc8-label">Governed rollout</p>
        <h2 className="gc8-h">Programme measurement is staged, not collecting</h2>
        <p className="gc8-sub">
          The event contract, privacy controls and reporting surface are ready for review. Collection remains disabled until controller approval, the updated student-notice decision, and the Year-2 aggregate pipeline are complete.
        </p>
      </section>
    );
  }

  if (summary.suppressed) {
    return (
      <section className="gc8-sec adm-state">
        <p className="gc8-label">Privacy threshold</p>
        <h2 className="gc8-h">This cohort is too small to report separately</h2>
        <p className="gc8-sub">
          This selection, or one of the subgroups that could be inferred from it, is below the {summary.suppressionMinimum}-student privacy threshold. Choose a broader view or wait for the cohort to grow.
        </p>
      </section>
    );
  }

  const activation = summary.activation || { numerator: 0, denominator: 0, percentage: null };
  const participation = summary.weeklyParticipation || { numerator: 0, denominator: 0, percentage: null };
  const retention = summary.fourWeekRetention || { numerator: 0, denominator: 0, percentage: null };
  const trendMax = Math.max(1, ...(summary.weeklyTrend || []).map(item => item.activeStudents ?? 0));
  const ratioDetail = (ratio: Ratio, available: string, building: string) => {
    if (ratio.suppressed) return `Hidden until at least ${summary.suppressionMinimum} students are represented`;
    if (ratio.denominator && ratio.numerator !== null) return available;
    return building;
  };
  const displayCount = (value?: number | null) => value === null ? 'Hidden' : (value ?? 0);
  const percentFigure = (value: number | null) => value === null ? 'Building' : <Fig value={value} unit="%" />;
  const asOf = asOfTime(summary.generatedAt);
  const figures = [
    { label: 'Registered', value: summary.registeredStudents, detail: 'Current students in this cohort; eligible count still required for reach.' },
    { label: 'Activated in 7 days', value: percentFigure(activation.percentage), detail: ratioDetail(activation, `${activation.numerator} of ${activation.denominator} measurable new accounts`, 'Starts with accounts created after measurement began') },
    { label: 'Weekly participation', value: percentFigure(participation.percentage), detail: ratioDetail(participation, `${participation.numerator} of ${participation.denominator} activated students`, 'Requires activated students and a return visit') },
    { label: 'Four-week retention', value: percentFigure(retention.percentage), detail: ratioDetail(retention, `${retention.numerator} of ${retention.denominator} eligible activations`, 'Appears after a cohort reaches week four') },
  ];
  const featureRows = summary.featureRows || [];

  return (
    <div className="adm-progpanel">
      <div className="adm-progtools">
        <SelectionBar
          label="Programme reporting period"
          size="md"
          className="adm-range"
          options={RANGE_OPTIONS.map(option => ({ value: String(option.days) as '7' | '28' | '84', label: option.label }))}
          value={String(rangeDays) as '7' | '28' | '84'}
          onChange={value => setRangeDays(Number(value) as 7 | 28 | 84)}
        />
        <div className="adm-asof">
          <span className="gc8-meta">{asOf ? `Data as of ${asOf}` : null}</span>
          <TextButton tone="quiet" className="gc8-ib" aria-disabled={isLoading || undefined} onClick={() => { if (!isLoading) setReloadToken(value => value + 1); }}>
            <RefreshCw className={`ui-icon${isLoading ? ' adm-spin' : ''}`} width={16} height={16} strokeWidth={2} aria-hidden="true" />Refresh evidence
          </TextButton>
        </div>
      </div>

      <div className={`adm-stats${wide ? ' adm-stats--four' : ''}`}>
        {figures.map(item => (
          <div key={item.label}>
            <span className="gc8-label">{item.label}</span>
            <span className="gc8-num adm-statnum">{item.value}</span>
            <span className="gc8-meta">{item.detail}</span>
          </div>
        ))}
      </div>

      <div className="adm-progtwo">
        <section className="gc8-sec" aria-labelledby="weekly-participation-title">
          <div className="gc8-sechead">
            <div className="gc8-sechead-col">
              <p className="gc8-label">Participation</p>
              <h2 id="weekly-participation-title" className="gc8-h">Active students by week</h2>
            </div>
          </div>
          <div className="adm-weeks" aria-label="Twelve-week active-student trend">
            {(summary.weeklyTrend || []).map(item => (
              <div key={item.weekStart}>
                <span className="gc8-readout">{item.activeStudents ?? '—'}</span>
                <i style={{ height: `${item.activeStudents === null ? 3 : Math.max(3, (item.activeStudents / trendMax) * 112)}px` }} />
                {wide ? <span className="adm-weekday">{readableDate(item.weekStart)}</span> : null}
              </div>
            ))}
          </div>
        </section>

        <section className="gc8-sec" aria-labelledby="programme-actions-title">
          <div className="gc8-sechead">
            <div className="gc8-sechead-col">
              <p className="gc8-label">Intentional activity</p>
              <h2 id="programme-actions-title" className="gc8-h">Actions completed</h2>
            </div>
          </div>
          <dl className="gc8-figrows adm-figrows">
            <div>
              <dt className="gc8-sub">Planned study activities</dt>
              <dd className="gc8-num">{figureWords(countWords(displayCount(summary.planActivitiesCompleted)))}</dd>
            </div>
            <div>
              <dt className="gc8-sub">Study sessions completed</dt>
              <dd className="gc8-num">{figureWords(countWords(displayCount(summary.studySessionsCompleted)))}</dd>
            </div>
            <div>
              <dt className="gc8-figrows-col">
                <span className="gc8-sub">Practice attempts</span>
                <span className="gc8-meta">{summary.strongPracticePercentage === null || summary.strongPracticePercentage === undefined ? 'Accuracy builds with new attempts' : `${summary.strongPracticePercentage}% strong or full self-marks`}</span>
              </dt>
              <dd className="gc8-num">{figureWords(countWords(displayCount(summary.practiceAttemptsCompleted)))}</dd>
            </div>
            <div>
              <dt className="gc8-figrows-col">
                <span className="gc8-sub">Confidence after study</span>
                <span className="gc8-meta">{summary.confidenceResponses === null ? 'Hidden for a small response group' : `${countWords(summary.confidenceResponses ?? 0)} responses`}</span>
              </dt>
              <dd className="gc8-num">{summary.averageConfidence === null || summary.averageConfidence === undefined ? '—' : <>{figureWords(String(summary.averageConfidence))} <span className="adm-of">/ 5</span></>}</dd>
            </div>
          </dl>
        </section>
      </div>

      <section className="gc8-sec" aria-labelledby="feature-success-title">
        <div className="gc8-sechead">
          <div className="gc8-sechead-col">
            <p className="gc8-label">Product decisions</p>
            <h2 id="feature-success-title" className="gc8-h">Feature starts and successful finishes</h2>
          </div>
        </div>
        <p className="gc8-meta">Rows appear after at least {summary.suppressionMinimum} students have started or completed the flow.</p>
        <table className={`adm-ftable${wide ? '' : ' adm-ftable--two'}`}>
          <thead>
            <tr>
              <th scope="col" className="gc8-label">Feature</th>
              <th scope="col" className="gc8-label adm-n">Exposed</th>
              {wide ? <><th scope="col" className="gc8-label adm-n">Started</th><th scope="col" className="gc8-label adm-n">Completed</th><th scope="col" className="gc8-label adm-n">Success</th></> : null}
            </tr>
          </thead>
          <tbody>
            {featureRows.length > 0 ? featureRows.map(row => (
              <tr key={row.id}>
                <th scope="row">{featureLabel(row.id)}</th>
                <td className="adm-n">{row.exposed ?? '—'}</td>
                {wide ? <>
                  <td className="adm-n">{row.started}</td>
                  <td className="adm-n">{row.completed ?? '—'}</td>
                  <td className="adm-n">{row.successRate === null ? '—' : <span className="adm-pct">{row.successRate}<small className="gc8-unit">%</small></span>}</td>
                </> : null}
              </tr>
            )) : (
              <tr><td colSpan={wide ? 5 : 2} className="gc8-empty">Feature evidence will appear as students use this version of the app.</td></tr>
            )}
          </tbody>
        </table>
        {wide ? null : (
          <div className="gc8-best adm-best">
            <p className="gc8-label">Best on a laptop</p>
            <p className="gc8-sub">Started, completed and success for each feature, side by side.</p>
          </div>
        )}
      </section>

      <section className="adm-cover">
        <div className="adm-cover-part">
          <p className="gc8-label">Measurement coverage</p>
          <p className="adm-cover-text">
            {summary.coverage?.eventCount === null
              ? `Activity volume is hidden until ${summary.suppressionMinimum} students contribute. `
              : `${countWords(summary.coverage?.eventCount ?? 0)} structured events in this period. `}
            {summary.coverage?.studentsWithAnalyticsId === null
              ? 'Measurement coverage is hidden for the current small contributor group.'
              : `${summary.coverage?.studentsWithAnalyticsId ?? 0} of ${summary.registeredStudents} students now have a separate analytics identifier.`}
          </p>
          <p className="gc8-meta">
            {summary.measurementStartedOn
              ? `History begins ${readableDate(summary.measurementStartedOn)}. Earlier product use is not reconstructed or presented as event data.`
              : 'No programme events have been recorded yet; earlier product use will not be reconstructed.'}
          </p>
        </div>
        <div className="adm-cover-part">
          <p className="gc8-label">Awaiting programme input</p>
          <ul className="adm-ruled">
            {(summary.awaitingProgrammeInput || []).map(item => <li key={item}>{item}</li>)}
          </ul>
        </div>
      </section>
    </div>
  );
};

export default AdminProgrammePanel;
