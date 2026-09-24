/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */
import React, { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import { Activity, CalendarCheck2, RefreshCw, ShieldCheck, Target, UsersRound } from 'lucide-react';
import { getFunctions, httpsCallable } from 'firebase/functions';
import app from '../firebase';
import { type CourseData } from './Library';

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

const EvidenceCard: React.FC<{
  label: string;
  value: React.ReactNode;
  detail: string;
  icon: React.ReactNode;
  positive?: boolean;
}> = ({ label, value, detail, icon, positive = false }) => (
  <article className="rounded-lg border border-[var(--admin-rule)] bg-[var(--admin-surface)] p-5">
    <div className="flex items-start justify-between gap-3">
      <p className="text-xs font-bold uppercase tracking-[0.13em] text-[var(--admin-muted)]">{label}</p>
      <span className={positive ? 'text-[var(--admin-success)]' : 'text-[var(--admin-accent)]'}>{icon}</span>
    </div>
    <strong className="mt-3 block font-sans text-3xl font-bold tabular-nums text-[var(--admin-ink)]">{value}</strong>
    <p className="mt-1 text-xs leading-relaxed text-[var(--admin-muted)]">{detail}</p>
  </article>
);

const AdminProgrammePanel: React.FC<Props> = ({ schoolFilter, yearFilter, allCourses }) => {
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
    return <div className="grid grid-cols-2 gap-3 lg:grid-cols-4" aria-label="Loading programme evidence">
      {[0, 1, 2, 3].map(item => <div key={item} className="h-36 animate-pulse rounded-lg border border-[var(--admin-rule)] bg-[var(--admin-surface)]" />)}
    </div>;
  }

  if (error && !summary) {
    return (
      <div role="alert" className="rounded-lg border border-[var(--admin-accent)] bg-[var(--admin-warning-bg)] px-5 py-4 text-sm text-[var(--admin-accent)]">
        <p className="font-bold not-italic">Programme evidence is unavailable</p>
        <p className="mt-1">{error}</p>
        <button type="button" onClick={() => setReloadToken(value => value + 1)} className="mt-3 rounded-full border border-[var(--admin-rule)] bg-[var(--admin-surface)] px-4 py-2 text-xs font-bold not-italic text-[var(--admin-ink)]">Try again</button>
      </div>
    );
  }

  if (!summary) return null;

  if (summary.enabled === false) {
    return (
      <section className="rounded-lg border border-[var(--admin-rule)] bg-[var(--admin-surface)] p-6 sm:p-8">
        <p className="text-xs font-bold uppercase tracking-[0.14em] text-[var(--admin-accent)]">Governed rollout</p>
        <h2 className="mt-2 font-sans text-2xl font-semibold text-[var(--admin-ink)]">Programme measurement is staged, not collecting</h2>
        <p className="mt-3 max-w-3xl text-sm leading-relaxed text-[var(--admin-muted)]">
          The event contract, privacy controls and reporting surface are ready for review. Collection remains disabled until controller approval, the updated student-notice decision, and the Year-2 aggregate pipeline are complete.
        </p>
      </section>
    );
  }

  if (summary.suppressed) {
    return (
      <section className="rounded-lg border border-[var(--admin-rule)] bg-[var(--admin-surface)] p-6">
        <p className="text-xs font-bold uppercase tracking-[0.14em] text-[var(--admin-muted)]">Privacy threshold</p>
        <h2 className="mt-2 font-sans text-2xl font-semibold text-[var(--admin-ink)]">This cohort is too small to report separately</h2>
        <p className="mt-2 max-w-2xl text-sm leading-relaxed text-[var(--admin-muted)]">
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

  return (
    <div className="space-y-6">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <div className="flex flex-wrap gap-2" aria-label="Programme reporting period">
          {RANGE_OPTIONS.map(option => (
            <button
              key={option.days}
              type="button"
              onClick={() => setRangeDays(option.days)}
              aria-pressed={rangeDays === option.days}
              className={`rounded-full border px-4 py-2 text-xs font-bold ${rangeDays === option.days ? 'border-[var(--admin-accent)] bg-[var(--admin-accent)] text-[var(--admin-action-ink)]' : 'border-[var(--admin-rule)] bg-[var(--admin-surface)] text-[var(--admin-ink)]'}`}
            >
              {option.label}
            </button>
          ))}
        </div>
        <button type="button" onClick={() => setReloadToken(value => value + 1)} disabled={isLoading} className="inline-flex items-center gap-2 rounded-full border border-[var(--admin-rule)] bg-[var(--admin-surface)] px-4 py-2 text-xs font-bold text-[var(--admin-ink)] disabled:opacity-50">
          <RefreshCw size={14} className={isLoading ? 'animate-spin' : undefined} /> Refresh evidence
        </button>
      </div>

      <div className="grid grid-cols-2 gap-3 lg:grid-cols-4 lg:gap-5">
        <EvidenceCard label="Registered" value={summary.registeredStudents} detail="Current students in this cohort; eligible count still required for reach." icon={<UsersRound size={19} />} />
        <EvidenceCard
          label="Activated in 7 days"
          value={activation.percentage === null ? 'Building' : `${activation.percentage}%`}
          detail={ratioDetail(activation, `${activation.numerator} of ${activation.denominator} measurable new accounts`, 'Starts with accounts created after measurement began')}
          icon={<Target size={19} />}
          positive={activation.percentage !== null && activation.percentage >= 70}
        />
        <EvidenceCard
          label="Weekly participation"
          value={participation.percentage === null ? 'Building' : `${participation.percentage}%`}
          detail={ratioDetail(participation, `${participation.numerator} of ${participation.denominator} activated students`, 'Requires activated students and a return visit')}
          icon={<Activity size={19} />}
          positive={participation.percentage !== null && participation.percentage >= 50}
        />
        <EvidenceCard
          label="Four-week retention"
          value={retention.percentage === null ? 'Building' : `${retention.percentage}%`}
          detail={ratioDetail(retention, `${retention.numerator} of ${retention.denominator} eligible activations`, 'Appears after a cohort reaches week four')}
          icon={<CalendarCheck2 size={19} />}
          positive={retention.percentage !== null && retention.percentage >= 40}
        />
      </div>

      <div className="grid grid-cols-1 gap-6 lg:grid-cols-[1.15fr_0.85fr]">
        <section className="rounded-lg border border-[var(--admin-rule)] bg-[var(--admin-surface)] p-5 sm:p-6" aria-labelledby="weekly-participation-title">
          <p className="text-xs font-bold uppercase tracking-[0.14em] text-[var(--admin-muted)]">Participation</p>
          <h2 id="weekly-participation-title" className="mt-1 font-sans text-2xl font-semibold text-[var(--admin-ink)]">Active students by week</h2>
          <div className="mt-6 flex h-44 items-end gap-2" aria-label="Twelve-week active-student trend">
            {(summary.weeklyTrend || []).map(item => (
              <div key={item.weekStart} className="flex min-w-0 flex-1 flex-col items-center justify-end gap-2">
                <span className="text-xs font-bold tabular-nums text-[var(--admin-body)]">{item.activeStudents ?? '—'}</span>
                <div className="w-full rounded-t-sm bg-[var(--admin-accent)]" style={{ height: `${item.activeStudents === null ? 3 : Math.max(3, (item.activeStudents / trendMax) * 112)}px` }} />
                <span className="hidden text-[11px] text-[var(--admin-muted)] sm:block">{readableDate(item.weekStart)}</span>
              </div>
            ))}
          </div>
        </section>

        <section className="rounded-lg border border-[var(--admin-rule)] bg-[var(--admin-surface)] p-5 sm:p-6" aria-labelledby="programme-actions-title">
          <p className="text-xs font-bold uppercase tracking-[0.14em] text-[var(--admin-muted)]">Intentional activity</p>
          <h2 id="programme-actions-title" className="mt-1 font-sans text-2xl font-semibold text-[var(--admin-ink)]">Actions completed</h2>
          <dl className="mt-6 divide-y divide-[var(--admin-rule)]">
            <div className="flex items-end justify-between gap-4 py-4 first:pt-0">
              <dt className="text-sm font-semibold text-[var(--admin-body)]">Planned study activities</dt>
              <dd className="font-sans text-3xl font-bold tabular-nums text-[var(--admin-ink)]">{displayCount(summary.planActivitiesCompleted)}</dd>
            </div>
            <div className="flex items-end justify-between gap-4 py-4">
              <dt className="text-sm font-semibold text-[var(--admin-body)]">Study sessions completed</dt>
              <dd className="font-sans text-3xl font-bold tabular-nums text-[var(--admin-ink)]">{displayCount(summary.studySessionsCompleted)}</dd>
            </div>
            <div className="flex items-end justify-between gap-4 py-4">
              <dt>
                <span className="block text-sm font-semibold text-[var(--admin-body)]">Practice attempts</span>
                <span className="mt-1 block text-xs text-[var(--admin-muted)]">{summary.strongPracticePercentage === null || summary.strongPracticePercentage === undefined ? 'Accuracy builds with new attempts' : `${summary.strongPracticePercentage}% strong or full self-marks`}</span>
              </dt>
              <dd className="font-sans text-3xl font-bold tabular-nums text-[var(--admin-ink)]">{displayCount(summary.practiceAttemptsCompleted)}</dd>
            </div>
            <div className="flex items-end justify-between gap-4 py-4 last:pb-0">
              <dt>
                <span className="block text-sm font-semibold text-[var(--admin-body)]">Confidence after study</span>
                <span className="mt-1 block text-xs text-[var(--admin-muted)]">{summary.confidenceResponses === null ? 'Hidden for a small response group' : `${summary.confidenceResponses ?? 0} responses`}</span>
              </dt>
              <dd className="font-sans text-3xl font-bold tabular-nums text-[var(--admin-ink)]">{summary.averageConfidence === null || summary.averageConfidence === undefined ? '—' : `${summary.averageConfidence}/5`}</dd>
            </div>
          </dl>
        </section>
      </div>

      <section className="overflow-hidden rounded-lg border border-[var(--admin-rule)] bg-[var(--admin-surface)]" aria-labelledby="feature-success-title">
        <div className="border-b border-[var(--admin-rule)] px-5 py-5 sm:px-6">
          <p className="text-xs font-bold uppercase tracking-[0.14em] text-[var(--admin-muted)]">Product decisions</p>
          <h2 id="feature-success-title" className="mt-1 font-sans text-2xl font-semibold text-[var(--admin-ink)]">Feature starts and successful finishes</h2>
          <p className="mt-2 text-sm text-[var(--admin-muted)]">Rows appear after at least {summary.suppressionMinimum} students have started or completed the flow.</p>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full min-w-[680px] border-collapse text-left">
            <thead className="bg-[var(--admin-raised)] text-xs font-bold uppercase tracking-[0.1em] text-[var(--admin-muted)]">
              <tr><th className="px-5 py-3">Feature</th><th className="px-4 py-3 text-right">Exposed</th><th className="px-4 py-3 text-right">Started</th><th className="px-4 py-3 text-right">Completed</th><th className="px-5 py-3 text-right">Success</th></tr>
            </thead>
            <tbody className="divide-y divide-[var(--admin-rule)]">
              {(summary.featureRows || []).length > 0 ? summary.featureRows!.map(row => (
                <tr key={row.id}>
                  <th scope="row" className="px-5 py-4 text-sm font-bold text-[var(--admin-ink)]">{featureLabel(row.id)}</th>
                  <td className="px-4 py-4 text-right text-sm tabular-nums text-[var(--admin-body)]">{row.exposed ?? '—'}</td>
                  <td className="px-4 py-4 text-right text-sm tabular-nums text-[var(--admin-body)]">{row.started}</td>
                  <td className="px-4 py-4 text-right text-sm tabular-nums text-[var(--admin-body)]">{row.completed ?? '—'}</td>
                  <td className="px-5 py-4 text-right text-sm font-bold tabular-nums text-[var(--admin-ink)]">{row.successRate === null ? '—' : `${row.successRate}%`}</td>
                </tr>
              )) : (
                <tr><td colSpan={5} className="px-5 py-10 text-center text-sm text-[var(--admin-muted)]">Feature evidence will appear as students use this version of the app.</td></tr>
              )}
            </tbody>
          </table>
        </div>
      </section>

      <section className="grid grid-cols-1 gap-6 rounded-lg border border-[var(--admin-rule)] bg-[var(--admin-surface)] p-5 sm:p-6 lg:grid-cols-2">
        <div>
          <div className="flex items-center gap-2 text-[var(--admin-success)]"><ShieldCheck size={18} /><span className="text-xs font-bold uppercase tracking-[0.13em]">Measurement coverage</span></div>
          <p className="mt-3 text-sm leading-relaxed text-[var(--admin-body)]">
            {summary.coverage?.eventCount === null
              ? `Activity volume is hidden until ${summary.suppressionMinimum} students contribute. `
              : `${summary.coverage?.eventCount ?? 0} structured events in this period. `}
            {summary.coverage?.studentsWithAnalyticsId === null
              ? 'Measurement coverage is hidden for the current small contributor group.'
              : `${summary.coverage?.studentsWithAnalyticsId ?? 0} of ${summary.registeredStudents} students now have a separate analytics identifier.`}
          </p>
          <p className="mt-2 text-xs leading-relaxed text-[var(--admin-muted)]">
            {summary.measurementStartedOn
              ? `History begins ${readableDate(summary.measurementStartedOn)}. Earlier product use is not reconstructed or presented as event data.`
              : 'No programme events have been recorded yet; earlier product use will not be reconstructed.'}
          </p>
        </div>
        <div>
          <p className="text-xs font-bold uppercase tracking-[0.13em] text-[var(--admin-muted)]">Awaiting programme input</p>
          <ul className="mt-3 space-y-2 text-sm text-[var(--admin-body)]">
            {(summary.awaitingProgrammeInput || []).map(item => <li key={item} className="flex gap-2"><span aria-hidden="true" className="mt-2 h-1.5 w-1.5 shrink-0 rounded-full bg-[var(--admin-accent)]" />{item}</li>)}
          </ul>
        </div>
      </section>
    </div>
  );
};

export default AdminProgrammePanel;
