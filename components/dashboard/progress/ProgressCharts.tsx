import { useId, useMemo, useState, type CSSProperties, type ReactNode } from 'react';
import { motion, useReducedMotion } from 'motion/react';
import { Area, AreaChart, CartesianGrid, Line, LineChart, ReferenceLine, XAxis, YAxis } from 'recharts';
import { ChevronDown } from 'lucide-react';
import { ChartContainer, ChartTooltip, ChartTooltipContent } from '../../approved-ui-runtime';
import { Button } from '../../approved-ui-runtime';
import { Checkbox } from '../../approved-ui-runtime';
import { Popover, PopoverTrigger, PopoverContent } from '../../approved-ui-runtime';
import CrewIllustration from '../../CrewIllustration';
import type { UnifiedMockResult } from '../../../types';
import { CONFIDENCE_LABELS, type ActivityBucket, type ActivityMetric, type ConfidenceObservation, type RangeBounds, type RankedValue } from '../dashboardAnalytics';
import { Surface, Eyebrow, Empty, ProgressTabs } from './shared';
import { confidenceChartData, subjectColour } from './progressData';

const orange = '#eb692a';
const dayLabel = (value: number) => new Date(value).toLocaleDateString('en-IE', { day: 'numeric', month: 'short' });
const activityConfig = { sessions: { label: 'Sessions', color: orange }, minutes: { label: 'Minutes', color: orange } };
function Insights({ children, label }: { children: ReactNode; label: string }) {
  return <Popover><PopoverTrigger render={<Button variant="outline" className="nsu-ink-outline" aria-label={`Show ${label} insights`} />}>Insights<ChevronDown /></PopoverTrigger><PopoverContent className="pr-insights" align="end">{children}</PopoverContent></Popover>;
}

export function ProgressActivity({ buckets, metric, onMetricChange, period, subjectLabel, insights, className = '', onStartStudy }: {
  buckets: ActivityBucket[]; metric: ActivityMetric; onMetricChange: (metric: ActivityMetric) => void; period: string;
  subjectLabel: string; insights: ReactNode; className?: string; onStartStudy?: () => void;
}) {
  const [record, setRecord] = useState(false);
  const [average, setAverage] = useState(false);
  const id = useId().replace(/:/g, '');
  const total = buckets.reduce((sum, bucket) => sum + bucket[metric], 0);
  const periodUnit = buckets.length === 12 && buckets[0]?.label === 'Jan' ? 'year' : buckets.length > 7 ? 'month' : 'week';
  const activeDays = buckets.filter(bucket => bucket.sessions > 0).length;
  const elapsedBuckets = buckets.filter(bucket => bucket.start <= Date.now());
  const mean = elapsedBuckets.length ? elapsedBuckets.reduce((sum, bucket) => sum + bucket[metric], 0) / elapsedBuckets.length : 0;
  return <Surface className={`pr-activity pr-study ${className}`}><header className="pr-chart-header"><div><Eyebrow>Study activity / {period}</Eyebrow><h2>{metric === 'sessions' ? `Your ${periodUnit} in focus.` : 'The time you made.'}</h2><p>{subjectLabel}</p></div><div className="pr-chart-controls"><ProgressTabs label="Study activity measure" value={metric} onChange={value => onMetricChange(value as ActivityMetric)} options={[{ value: 'sessions', label: 'Sessions' }, { value: 'minutes', label: 'Minutes' }]} /><Insights label="study activity"><label><Checkbox checked={average} onCheckedChange={setAverage} />Show period average</label><p>The average covers elapsed days or months in this period. It isn’t a study target.</p>{insights}</Insights></div></header>
    <div className="pr-chart-reading"><strong>{total}<small>{metric === 'sessions' ? 'sessions' : 'minutes'}</small></strong><span>across {activeDays} active {buckets.length === 12 && buckets[0]?.label === 'Jan' ? 'months' : 'days'}</span><Button variant="ghost" onClick={() => setRecord(!record)}>{record ? 'Show graph' : 'Read the numbers'}</Button></div>
    {record ? <table className="pr-data-table"><caption>{period} · {subjectLabel}</caption><thead><tr><th scope="col">Date</th><th scope="col">Sessions</th><th scope="col">Minutes</th></tr></thead><tbody>{buckets.map(day => <tr key={day.key}><th scope="row">{day.accessibleLabel}</th><td>{day.sessions}</td><td>{day.minutes}</td></tr>)}</tbody></table> : total === 0 ? <Empty title="No study sessions in this period" onStartStudy={onStartStudy}>Your next completed session will update this chart.</Empty> : <div role="img" aria-label={`Study activity chart showing ${metric}`}><ChartContainer config={activityConfig} className="pr-activity-chart"><AreaChart data={buckets} margin={{ left: 4, right: 24, top: 24, bottom: 8 }} accessibilityLayer><defs><linearGradient id={`focus-${id}`} x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stopColor={orange} stopOpacity={.2} /><stop offset="100%" stopColor={orange} stopOpacity={.015} /></linearGradient></defs><CartesianGrid vertical={false} stroke="var(--border)" /><XAxis dataKey="label" tickLine={false} axisLine={false} tickMargin={14} minTickGap={24} /><YAxis width={38} tickLine={false} axisLine={false} allowDecimals={false} domain={[0, 'auto']} tickMargin={9} /><ChartTooltip content={<ChartTooltipContent />} />{average && <ReferenceLine y={mean} stroke="var(--muted-foreground)" strokeDasharray="4 5" label={{ value: `Average ${mean.toFixed(1)}`, position: 'insideTopRight', fill: 'var(--muted-foreground)', fontSize: 12 }} />}<Area key={metric} type="monotone" dataKey={metric} stroke={orange} strokeWidth={2.5} fill={`url(#focus-${id})`} dot={{ r: 4, fill: orange, stroke: 'var(--nsu-surface)', strokeWidth: 2 }} activeDot={{ r: 6, strokeWidth: 3, stroke: 'var(--nsu-surface)' }} isAnimationActive={false} animationDuration={850} /></AreaChart></ChartContainer></div>}
    <footer className="pr-chart-footer"><span><i />Completed study</span><span>Actual recorded study time.</span></footer>
  </Surface>;
}

export function ProgressConfidence({ observations, bounds, subjects, universe, insights, className = '' }: {
  observations: ConfidenceObservation[]; bounds: RangeBounds; subjects: string[]; universe: string[]; insights: ReactNode; className?: string;
}) {
  const [selection, setSelection] = useState<string[] | null>(null);
  const [view, setView] = useState('Together');
  const selected = selection === null ? subjects : subjects.filter(subject => selection.includes(subject));
  const chartConfig = Object.fromEntries(subjects.map((subject, index) => [`s${index}`, { label: subject, color: subjectColour(subject, universe) }]));
  const data = useMemo(() => confidenceChartData(observations, subjects), [observations, subjects]);
  const start = bounds.start.getTime();
  const end = bounds.end.getTime() - 1;
  const ticks = [start, start + (end - start) / 3, start + (end - start) * 2 / 3, end];
  const entriesFor = (subject: string) => observations.filter(point => point.subject === subject).sort((a, b) => a.timestamp - b.timestamp);
  const plot = (chosen: string[], mini = false) => <div role="img" aria-label={mini ? `${chosen[0]} confidence over time` : 'Confidence over time by subject'}><ChartContainer config={chartConfig} className={mini ? 'pr-confidence-mini' : 'pr-confidence-chart'}><LineChart data={data} margin={{ top: 20, right: 24, left: mini ? 0 : 8, bottom: 8 }} accessibilityLayer><CartesianGrid vertical={false} stroke="var(--border)" /><XAxis dataKey="timestamp" type="number" domain={[start, end]} ticks={ticks} tickFormatter={dayLabel} tickLine={false} axisLine={false} tickMargin={12} minTickGap={25} /><YAxis domain={[1, 5]} ticks={[1, 2, 3, 4, 5]} width={mini ? 28 : 85} tickLine={false} axisLine={false} tickFormatter={value => mini ? String(value) : CONFIDENCE_LABELS[value - 1]} /><ChartTooltip content={<ChartTooltipContent labelFormatter={label => dayLabel(Number(label))} formatter={(value, name) => <div className="pr-confidence-tooltip"><strong>{chartConfig[String(name)]?.label ?? name}</strong><span>{value}/5 · {CONFIDENCE_LABELS[Math.round(Number(value)) - 1]}</span></div>} />} />{chosen.map(subject => {
    const index = subjects.indexOf(subject);
    const colour = subjectColour(subject, universe);
    return <Line key={subject} dataKey={`s${index}`} connectNulls type="linear" stroke={colour} fill={colour} strokeWidth={2.5} strokeLinecap="round" strokeLinejoin="round" dot={{ r: 3, fill: colour, strokeWidth: 0 }} activeDot={{ r: 5, fill: colour, strokeWidth: 0 }} isAnimationActive={false} animationDuration={650} />;
  })}</LineChart></ChartContainer></div>;
  return <section className={`pr-study pr-confidence ${className}`} aria-label="Confidence over time"><header className="pr-card-heading"><div><Eyebrow>Your check-ins / {bounds.label}</Eyebrow><h2>A different story in every subject.</h2><p>How you felt after study, on a scale of 1–5.</p></div><Insights label="confidence chart">{insights}</Insights></header>
    <div className="pr-confidence-pickers" role="group" aria-label="Subjects to compare">{subjects.map(subject => <label key={subject} data-selected={selected.includes(subject)}><Checkbox checked={selected.includes(subject)} onCheckedChange={checked => setSelection(checked ? [...selected, subject] : selected.filter(item => item !== subject))} /><CrewIllustration className="pr-subject-art" subject={subject} /><span>{subject}</span><i style={{ background: subjectColour(subject, universe) }} /></label>)}</div>
    <div className="pr-confidence-toolbar"><div><Button variant="ghost" size="sm" onClick={() => setSelection(null)}>All subjects</Button>{subjects.length > 3 && <Button variant="ghost" size="sm" onClick={() => setSelection(subjects.slice(0, 3))}>Focus on three</Button>}</div><ProgressTabs label="Confidence view" value={view} onChange={setView} options={[{ value: 'Together', label: 'Together' }, { value: 'By subject', label: 'By subject' }]} /></div>
    {!selected.length ? <Surface><Empty title="Choose a subject to follow its story.">Your check-ins will appear here.</Empty></Surface> : view === 'Together' ? <Surface>{selected.some(subject => entriesFor(subject).length) ? plot(selected) : <Empty title="Confidence starts with a debrief">Choose Lost, Shaky, Okay, Good or Confident after a study session.</Empty>}<div className="pr-confidence-key">{selected.map(subject => { const entries = entriesFor(subject); const latest = entries[entries.length - 1]; return <div key={subject}><CrewIllustration className="pr-subject-art" subject={subject} /><div><strong>{subject}</strong><span>{entries.length} check-ins · {latest ? `latest ${latest.score}/5` : 'none in this period'}</span></div><svg width="32" height="10" aria-hidden="true"><path d="M0 5H32" stroke={subjectColour(subject, universe)} strokeWidth="2.5" /></svg></div>; })}</div></Surface> : <div className="pr-confidence-grid">{selected.map(subject => { const entries = entriesFor(subject); const latest = entries[entries.length - 1]; return <Surface key={subject}><header><CrewIllustration className="pr-subject-art" subject={subject} /><div><h3>{subject}</h3><p>{entries.length} check-ins · {latest ? `latest ${CONFIDENCE_LABELS[latest.score - 1]}` : 'not recorded'}</p></div></header>{entries.length ? plot([subject], true) : <Empty title="No check-ins yet">Your next debrief will start this subject’s line.</Empty>}</Surface>; })}</div>}
    <p className="pr-evidence-note">Dots are recorded check-ins; lines join those moments. Dates between them contain no reading. Confidence is your experience of study, not a prediction of your grade.</p>
  </section>;
}

export function ProgressSubjects({ values, period, className = '' }: { values: RankedValue[]; period: string; className?: string }) {
  const [sort, setSort] = useState('Time');
  const reduced = useReducedMotion();
  const data = [...values].sort(sort === 'Time' ? (a, b) => b.value - a.value : (a, b) => a.label.localeCompare(b.label));
  const max = Math.max(1, ...data.map(item => item.value));
  const total = data.reduce((sum, item) => sum + item.value, 0);
  return <Surface className={`pr-study pr-subject-bars ${className}`}><header className="pr-chart-header"><div><Eyebrow>Your subjects / {period}</Eyebrow><h2>Everyone has a place.</h2><p>{total} focused minutes, shared across your subjects.</p></div><ProgressTabs label="Subject order" value={sort} onChange={setSort} options={[{ value: 'Time', label: 'Time' }, { value: 'A–Z', label: 'A–Z' }]} /></header>{!data.length ? <Empty title="No subject split yet">Log a study session and its subject will appear here.</Empty> : <div className="pr-subject-chart-scroll"><div className="pr-crew-plot" style={{ '--subject-count': data.length } as CSSProperties} role="img" aria-label={data.map(item => `${item.label}: ${item.value} minutes`).join('; ')}>{data.map(subject => <div className="pr-bar-column" key={subject.id}><div className="pr-bar-space"><motion.div className="pr-crew-bar" initial={false} animate={{ height: Math.round(subject.value / max * 200) }} transition={{ duration: reduced ? 0 : .65, ease: [.22, 1, .36, 1] }}><CrewIllustration className="pr-subject-art" subject={subject.label} /></motion.div></div><strong>{subject.value}<small>min</small></strong><span>{subject.label}</span></div>)}</div></div>}<footer className="pr-chart-footer"><span><i />Focused minutes</span><span>Actual recorded study time.</span></footer></Surface>;
}

export function ProgressMocks({ mocks, period, subjectLabel, insights, className = '' }: { mocks: UnifiedMockResult[]; period: string; subjectLabel: string; insights: ReactNode; className?: string }) {
  const [view, setView] = useState('Chart');
  const data = [...mocks].sort((a, b) => a.date.localeCompare(b.date)).map(mock => ({ ...mock, timestamp: new Date(`${mock.date}T12:00:00`).getTime(), points: mock.totalPoints }));
  return <Surface className={`pr-study pr-mocks ${className}`}><header className="pr-chart-header"><div><Eyebrow>Exam evidence / {period}</Eyebrow><h2>Mock trajectory</h2><p>{subjectLabel === 'All subjects' ? 'Total points from full mock sittings in Points Passport.' : `Full mock totals stay all-subject · insights focus on ${subjectLabel}.`}</p></div><Insights label="mock trajectory">{insights}</Insights></header><div className="pr-mock-controls"><ProgressTabs label="Mock trajectory view" value={view} onChange={setView} options={[{ value: 'Chart', label: 'Chart' }, { value: 'The record', label: 'The record' }]} /></div>
    {!data.length ? <Empty title="No full mocks in this period">Add a full mock sitting in Points Passport to build your trajectory. Single-subject results remain in Insights.</Empty> : view === 'Chart' ? <div role="img" aria-label="Mock exam total points trajectory"><ChartContainer config={{ points: { label: 'Points', color: orange } }} className="pr-activity-chart"><LineChart data={data} accessibilityLayer margin={{ top: 20, right: 24, bottom: 8, left: 4 }}><CartesianGrid vertical={false} stroke="var(--border)" /><XAxis dataKey="timestamp" type="number" domain={['dataMin', 'dataMax']} ticks={data.map(item => item.timestamp)} tickFormatter={dayLabel} tickLine={false} axisLine={false} minTickGap={24} /><YAxis domain={[0, 625]} width={38} tickLine={false} axisLine={false} /><ChartTooltip content={<ChartTooltipContent labelFormatter={label => dayLabel(Number(label))} />} /><Line dataKey="points" stroke={orange} strokeWidth={2.5} dot={{ r: 4, fill: orange, strokeWidth: 0 }} activeDot={{ r: 6, fill: orange, strokeWidth: 0 }} isAnimationActive={false} /></LineChart></ChartContainer></div> : <div className="pr-mock-records">{data.slice().reverse().map(mock => <details className="dashboard-mock-record" key={mock.id}><summary><span>{mock.label}<time dateTime={mock.date}>{dayLabel(mock.timestamp)}</time></span><strong>{mock.points} points</strong></summary><p>Full sitting, all subjects. Recorded result, not a forecast.</p><ul>{mock.entries.map(entry => <li key={entry.subjectName}><CrewIllustration className="pr-subject-art" subject={entry.subjectName} /><span>{entry.subjectName}</span><strong>{entry.grade}</strong></li>)}</ul></details>)}</div>}
    {data.length > 0 && <footer className="pr-chart-footer"><span>Latest practice mock</span><strong>{data[data.length - 1].points} points</strong></footer>}
  </Surface>;
}
