import { useMemo, useState } from 'react';
import { CartesianGrid, Line, LineChart, XAxis, YAxis } from 'recharts';
import { ChartContainer, ChartTooltip, ChartTooltipContent } from '../../approved-ui-runtime';
import { TextButton } from '../../ui/Button';
import { ChoiceTile, SelectionBar } from '../../ui/Choice';
import SubjectAvatar from '../../SubjectAvatar';
import { List, Row } from '../../ui/List';
import type { UnifiedMockResult } from '../../../types';
import { CONFIDENCE_LABELS, type ConfidenceObservation, type RangeBounds } from '../dashboardAnalytics';
import { confidenceChartData, subjectColour } from './progressData';
import { Section } from './ProgressParts';
import { COLORS } from '../../../design/tokens';

const orange = COLORS.accent;
const dayLabel = (value: number) => new Date(value).toLocaleDateString('en-IE', { day: 'numeric', month: 'short' });

/** Confidence over time: today's line chart by subject, on the page, below the subjects' scales.
 *  Each subject keeps its own line colour (the subject palette tells them apart). */
export function ProgressConfidence({ observations, bounds, subjects, universe, onInsights, className = '' }: {
  observations: ConfidenceObservation[]; bounds: RangeBounds; subjects: string[]; universe: string[]; onInsights?: () => void; className?: string;
}) {
  const [selection, setSelection] = useState<string[] | null>(null);
  const [view, setView] = useState<'Together' | 'By subject'>('Together');
  const selected = selection === null ? subjects : subjects.filter(subject => selection.includes(subject));
  const chartConfig = Object.fromEntries(subjects.map((subject, index) => [`s${index}`, { label: subject, color: subjectColour(subject, universe) }]));
  const data = useMemo(() => confidenceChartData(observations, subjects), [observations, subjects]);
  const start = bounds.start.getTime();
  const end = bounds.end.getTime() - 1;
  const ticks = [start, start + (end - start) / 3, start + (end - start) * 2 / 3, end];
  const entriesFor = (subject: string) => observations.filter(point => point.subject === subject).sort((a, b) => a.timestamp - b.timestamp);
  const plot = (chosen: string[], mini = false) => <div role="img" aria-label={mini ? `${chosen[0]} confidence over time` : 'Confidence over time by subject'}><ChartContainer config={chartConfig} className={mini ? 'pr-confidence-mini' : 'pr-confidence-chart'}><LineChart data={data} margin={{ top: 20, right: 24, left: mini ? 0 : 8, bottom: 8 }} accessibilityLayer><CartesianGrid vertical={false} stroke="var(--hairline)" /><XAxis dataKey="timestamp" type="number" domain={[start, end]} ticks={ticks} tickFormatter={dayLabel} tickLine={false} axisLine={false} tickMargin={12} minTickGap={25} /><YAxis domain={[1, 5]} ticks={[1, 2, 3, 4, 5]} width={mini ? 28 : 85} tickLine={false} axisLine={false} tickFormatter={value => mini ? String(value) : CONFIDENCE_LABELS[value - 1]} /><ChartTooltip content={<ChartTooltipContent labelFormatter={label => dayLabel(Number(label))} formatter={(value, name) => <div className="pr-confidence-tooltip"><strong>{chartConfig[String(name)]?.label ?? name}</strong><span>{value}/5 · {CONFIDENCE_LABELS[Math.round(Number(value)) - 1]}</span></div>} />} />{chosen.map(subject => {
    const index = subjects.indexOf(subject);
    const colour = subjectColour(subject, universe);
    return <Line key={subject} dataKey={`s${index}`} connectNulls type="linear" stroke={colour} fill={colour} strokeWidth={2.5} strokeLinecap="round" strokeLinejoin="round" dot={{ r: 3, fill: colour, strokeWidth: 0 }} activeDot={{ r: 5, fill: colour, strokeWidth: 0 }} isAnimationActive={false} animationDuration={650} />;
  })}</LineChart></ChartContainer></div>;
  return <section className={`mp-sec mp-sec--ruled pr-confidence ${className}`.trim()} aria-label="Confidence over time">
    <div className="mp-sec-headrow">
      <div className="mp-sec-head"><p className="t-label mp-label">{`Your check-ins · ${bounds.label}`}</p><h2 className="t-heading mp-heading">Over time</h2></div>
      {onInsights && <TextButton tone="quiet" aria-label="Show confidence chart insights" onClick={onInsights}>Insights</TextButton>}
    </div>
    <SelectionBar<'Together' | 'By subject'> label="Confidence view" value={view} onChange={setView} options={[{ value: 'Together', label: 'Together' }, { value: 'By subject', label: 'By subject' }]} />
    {!selected.length ? <div className="mp-empty"><p className="t-body">Choose a subject to follow its story.</p><p className="t-meta">Your check-ins will appear here.</p></div>
      : view === 'Together' ? <div className="mp-confidence-plot">{selected.some(subject => entriesFor(subject).length) ? plot(selected) : <div className="mp-empty"><p className="t-body">Confidence starts with a debrief.</p><p className="t-meta">Choose Lost, Shaky, Okay, Good or Confident after a study session.</p></div>}</div>
      : <div className="pr-confidence-grid">{selected.map(subject => { const entries = entriesFor(subject); const latest = entries[entries.length - 1]; return <article key={subject} className="mp-confidence-one"><header><SubjectAvatar subject={subject} bare className="mp-art" /><div><h3 className="t-row">{subject}</h3><p className="t-meta">{entries.length} check-ins · {latest ? `latest ${CONFIDENCE_LABELS[latest.score - 1]}` : 'not recorded'}</p></div></header>{entries.length ? plot([subject], true) : <p className="t-meta">No check-ins yet. Your next debrief will start this subject’s line.</p>}</article>; })}</div>}
    <div className="mp-compare" role="group" aria-label="Subjects to compare">{subjects.map(subject => <ChoiceTile key={subject} kind="several" chosen={selected.includes(subject)}
      label={<><i className="mp-key" style={{ background: subjectColour(subject, universe) }} aria-hidden="true" />{subject}</>}
      onClick={() => setSelection(selected.includes(subject) ? selected.filter(item => item !== subject) : [...selected, subject])} />)}</div>
    <div className="mp-graph-actions"><TextButton tone="quiet" onClick={() => setSelection(null)}>All subjects</TextButton>{subjects.length > 3 && <TextButton tone="quiet" onClick={() => setSelection(subjects.slice(0, 3))}>Focus on three</TextButton>}</div>
    <p className="t-meta">Dots are recorded check-ins; lines join those moments. Dates between them contain no reading. Confidence is your experience of study, not a prediction of your grade.</p>
  </section>;
}

/** Mock trajectory: each full sitting as a row with its points (the latest first), opening its subjects; the line on request. */
export function ProgressMocks({ mocks, period, subjectLabel, onInsights, className = '' }: { mocks: UnifiedMockResult[]; period: string; subjectLabel: string; onInsights?: () => void; className?: string }) {
  const [chart, setChart] = useState(false);
  const [open, setOpen] = useState<string | null>(null);
  const data = [...mocks].sort((a, b) => a.date.localeCompare(b.date)).map(mock => ({ ...mock, timestamp: new Date(`${mock.date}T12:00:00`).getTime(), points: mock.totalPoints }));
  const latestFirst = data.slice().reverse();
  return <Section label={`Exam evidence · ${period}`} title="Mock trajectory" className={`pr-mocks mp-mocks ${className}`.trim()}
    aside={onInsights ? <TextButton tone="quiet" aria-label="Show mock trajectory insights" onClick={onInsights}>Insights</TextButton> : undefined}>
    <p className="t-sub">{subjectLabel === 'All subjects' ? 'Total points from full mock sittings in Points Passport.' : `Full mock totals stay all-subject · insights focus on ${subjectLabel}.`}</p>
    {!data.length ? <div className="mp-empty"><p className="t-body">No full mocks in this period.</p><p className="t-meta">Add a full mock sitting in Points Passport to build your trajectory. Single-subject results remain in Insights.</p></div> : <>
      <div className="mp-mock-list" role="group" aria-label="Mock sittings">{latestFirst.map((mock, index) => <div key={mock.id} className="dashboard-mock-record">
        <List><Row title={mock.label} meta={index === 0 ? `${dayLabel(mock.timestamp)} · ${data.length === 1 ? 'one sitting recorded so far' : `${data.length} sittings recorded`}` : dayLabel(mock.timestamp)}
          value={`${mock.points} points`} expanded={open === mock.id} onPress={() => setOpen(open === mock.id ? null : mock.id)} /></List>
        {open === mock.id && <div className="mp-mock-detail"><p className="t-meta">Full sitting, all subjects. Recorded result, not a forecast.</p><ul>{mock.entries.map(entry => <li key={entry.subjectName}><SubjectAvatar subject={entry.subjectName} bare className="mp-art mp-art--sm" /><span className="t-body">{entry.subjectName}</span><strong className="t-readout">{entry.grade}</strong></li>)}</ul></div>}
      </div>)}</div>
      <div className="mp-graph-actions"><TextButton tone="quiet" aria-expanded={chart} onClick={() => setChart(value => !value)}>{chart ? 'Hide the chart' : 'Show the chart'}</TextButton></div>
      {chart && <div role="img" aria-label="Mock exam total points trajectory"><ChartContainer config={{ points: { label: 'Points', color: orange } }} className="pr-activity-chart"><LineChart data={data} accessibilityLayer margin={{ top: 20, right: 24, bottom: 8, left: 4 }}><CartesianGrid vertical={false} stroke="var(--hairline)" /><XAxis dataKey="timestamp" type="number" domain={['dataMin', 'dataMax']} ticks={data.map(item => item.timestamp)} tickFormatter={dayLabel} tickLine={false} axisLine={false} minTickGap={24} /><YAxis domain={[0, 625]} width={38} tickLine={false} axisLine={false} /><ChartTooltip content={<ChartTooltipContent labelFormatter={label => dayLabel(Number(label))} />} /><Line dataKey="points" stroke="var(--ink-primary)" strokeWidth={2} dot={{ r: 3.5, fill: 'var(--ink-primary)', strokeWidth: 0 }} activeDot={{ r: 5, fill: orange, strokeWidth: 0 }} isAnimationActive={false} /></LineChart></ChartContainer></div>}
    </>}
  </Section>;
}
