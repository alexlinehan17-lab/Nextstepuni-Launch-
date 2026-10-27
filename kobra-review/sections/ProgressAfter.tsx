/**
 * My Progress, rebuilt on Kobra for the wave 1 / 2 review (27 Oct 2026).
 *
 * Same words, order and sample fortnight as the "Now" pane: the copy is lifted
 * from components/DashboardView.tsx and components/dashboard/progress/*, and
 * every number is the app's own analytics (dashboardAnalytics,
 * dashboardInsightAnalytics, caoGoal, the timetable algorithm, the weekly goals
 * and challenge) run over kobra-review/sections/progress-sample.ts.
 *
 * What changed against the current screen:
 *  - The section tabs are the house pill (Kobra Tabs), like the date range
 *    beside them; on a narrow screen they become a Kobra Select.
 *  - The page's own theme switch is gone: appearance lives in Your setup.
 *  - Every bar is a Kobra Progress with an outlined track and a visible fill.
 *  - Insights and the Milestones disclosures are hairline accordion panels.
 *    Accordion is purchased but not compiled into the runtime: drawn here as
 *    buttons with aria-expanded over hairline rows (needs compiling into the
 *    runtime).
 *  - The Milestones loader is a Skeleton, drawn here because Skeleton is not
 *    compiled into the runtime either (needs compiling into the runtime).
 *  - Done is mint or ink, never orange: the completed quest, a met weekly
 *    target, a reached CAO goal. Orange stays for selection and the data.
 * Charts the audit does not touch (the confidence lines, the subject bars,
 * the five mountains) are left out here; the "Now" pane shows them.
 */

import { useId, useMemo, useState, type CSSProperties, type ReactNode } from 'react';
import { ArrowRight, Check, ChevronDown, Download, Search, X } from 'lucide-react';
import { Area, AreaChart, CartesianGrid, ReferenceLine, XAxis, YAxis } from 'recharts';
import {
  Button,
  ChartContainer,
  ChartTooltip,
  ChartTooltipContent,
  Checkbox,
  Dialog,
  DialogContent,
  DialogDescription,
  DialogTitle,
  Input,
  Popover,
  PopoverContent,
  PopoverTrigger,
  Progress,
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
  Tabs,
  TabsList,
  TabsTrigger,
  toast,
} from '../../components/approved-ui-runtime';
import ThemeArtwork from '../../components/ThemeArtwork';
import CrewIllustration from '../../components/CrewIllustration';
import AchievementGallery, { AchievementBadge } from '../../components/AchievementGallery';
import { getAchievementsForCurriculum } from '../../achievementData';
import { generateWeeklyGoals, getWeekNumber } from '../../gamificationConfig';
import { STRATEGY_REGISTRY } from '../../utils/strategyRegistry';
import { CAO_MAX_POINTS, caoEvidenceLabel, caoGapLabel, caoGoalStanding } from '../../components/dashboard/progress/caoGoal';
import {
  averageConfidence, buildActivityBuckets, buildMasterySummary, buildSessionMix, collectConfidenceObservations,
  confidenceInRange, filterSessions, getRangeBounds, toLocalDateKey,
  type ActivityBucket, type ActivityMetric, type DashboardRange, type RankedValue,
} from '../../components/dashboard/dashboardAnalytics';
import {
  buildActivityInsights, buildConfidenceInsights, buildMockInsights, type DashboardInsightItem, type DashboardTrend,
} from '../../components/dashboard/dashboardInsightAnalytics';
import { selectSubjects, subjectColour } from '../../components/dashboard/progress/progressData';
import { allocateSessions, computeSubjectPriorities, computeWeeksUntilExam, generateWeeklyTimetable } from '../../components/timetableAlgorithm';
import {
  SAMPLE_LABEL, SAMPLE_POINTS, sampleGamification, sampleProfile, sampleQuest, sampleRecommendation, sampleSessions,
  sampleStrategyMastery, sampleStreak, sampleTopicMastery, sampleWeeklyChallenge,
} from './progress-sample';
import './progress.css';

type Section = 'overview' | 'study' | 'confidence' | 'practice' | 'milestones';
const SECTIONS: { id: Section; label: string }[] = [
  { id: 'overview', label: 'Overview' }, { id: 'study', label: 'Study' }, { id: 'confidence', label: 'Confidence' },
  { id: 'practice', label: 'Practice' }, { id: 'milestones', label: 'Milestones' },
];
const SECTION_ITEMS = SECTIONS.map(item => ({ value: item.id, label: item.label }));
const RANGES: { id: DashboardRange; label: string }[] = [{ id: 'week', label: 'Week' }, { id: 'month', label: 'Month' }, { id: 'year', label: 'Year' }];
const TREND_LABEL: Record<DashboardTrend, string> = {
  upward: 'Trending upward', downward: 'Trending downward', steady: 'Steady', varied: 'Varied', building: 'Building a trend',
};
const MIX: Record<string, { colour: string; note: string }> = {
  'new-learning': { colour: '#eb692a', note: 'Getting started with unfamiliar material.' },
  practice: { colour: '#397f7c', note: 'Putting what you know to work.' },
  revision: { colour: '#b27d2d', note: 'Returning to material you have studied.' },
};
const TIERS = { none: { label: 'Not started', level: 0 }, learned: { label: 'Read', level: 1 }, practiced: { label: 'Practised', level: 2 }, applied: { label: 'Applied', level: 3 }, habitual: { label: 'Habitual', level: 4 } } as const;

const serial = (n: number) => String(n).padStart(2, '0');
const formatDuration = (minutes: number) => (minutes < 60 ? `${minutes}m` : `${Math.floor(minutes / 60)}h${minutes % 60 ? ` ${minutes % 60}m` : ''}`);
const pct = (value: number, total: number) => (total ? Math.round(value / total * 100) : 0);

function Eyebrow({ children }: { children: ReactNode }) { return <p className="kr-pg-eyebrow">{children}</p>; }

/** A Kobra Progress with the house track: outlined, and a fill you can see. */
function Bar({ value, label, tone = 'ink', colour, size = 'thin' }: {
  value: number; label: string; tone?: 'ink' | 'mint' | 'orange' | 'item'; colour?: string; size?: 'thin' | 'fat';
}) {
  return (
    <Progress value={Math.max(0, Math.min(100, value))} aria-label={label} className="kr-pg-bar" data-tone={tone} data-size={size}
      style={colour ? ({ '--kr-pg-item': colour } as CSSProperties) : undefined} />
  );
}

/** Accordion, drawn by hand: Kobra's Accordion is purchased but not compiled into the runtime. */
function AccordionItem({ id, open, onToggle, title, aside, children }: {
  id: string; open: boolean; onToggle: () => void; title: ReactNode; aside?: ReactNode; children: ReactNode;
}) {
  return (
    <div className="kr-pg-acc-item" data-open={open || undefined}>
      <h4 className="kr-pg-acc-heading">
        <button type="button" className="kr-pg-acc-trigger" aria-expanded={open} aria-controls={`${id}-panel`} id={`${id}-trigger`} onClick={onToggle}>
          <span className="kr-pg-acc-title">{title}</span>
          {aside && <span className="kr-pg-acc-aside">{aside}</span>}
          <ChevronDown aria-hidden="true" className="kr-pg-acc-chevron" />
        </button>
      </h4>
      <div className="kr-pg-acc-panel" id={`${id}-panel`} role="region" aria-labelledby={`${id}-trigger`} hidden={!open}>{children}</div>
    </div>
  );
}

function Trend({ trend }: { trend: DashboardTrend }) {
  return <span className="kr-pg-trend" data-trend={trend}><i aria-hidden="true" />{TREND_LABEL[trend]}</span>;
}

/** "What the pattern suggests": the insight index as a hairline accordion, first item open. */
function InsightIndex({ id, items, context, note }: { id: string; items: DashboardInsightItem[]; context: string; note?: string }) {
  const [selected, setSelected] = useState<string | null | undefined>(undefined);
  const openId = selected === null ? null : items.some(item => item.id === selected) ? selected : items[0]?.id;
  return (
    <section className="kr-pg-insight-index" aria-label="Chart insights">
      <header><p className="kr-pg-eyebrow">{context}</p><h3>What the pattern suggests</h3></header>
      <div className="kr-pg-acc">
        {items.map(item => (
          <AccordionItem key={item.id} id={`${id}-${item.id}`} open={openId === item.id} onToggle={() => setSelected(openId === item.id ? null : item.id)}
            title={<><strong>{item.title}</strong><Trend trend={item.trend} /></>}>
            <p>{item.evidence}</p>
            <div className="kr-pg-try"><strong>Try next</strong><p>{item.guidance}</p></div>
          </AccordionItem>
        ))}
      </div>
      {note && <footer>{note}</footer>}
    </section>
  );
}

/** The Insights control: an outline Button that opens a hairline panel inside the card, not a floating popover. */
function Insights({ label, open, onToggle, controls }: { label: string; open: boolean; onToggle: () => void; controls: string }) {
  return (
    <Button variant="outline" className="nsu-ink-outline kr-pg-insights-toggle" aria-label={`${open ? 'Hide' : 'Show'} ${label} insights`}
      aria-expanded={open} aria-controls={controls} onClick={onToggle}>
      Insights<ChevronDown aria-hidden="true" />
    </Button>
  );
}

function Panel({ eyebrow, title, detail, action, className = '', children, label }: {
  eyebrow: string; title: ReactNode; detail?: ReactNode; action?: ReactNode; className?: string; children?: ReactNode; label?: string;
}) {
  return (
    <article className={`kr-pg-panel ${className}`} aria-label={label}>
      <header className="kr-pg-panel-head">
        <div className="kr-pg-panel-copy"><Eyebrow>{eyebrow}</Eyebrow><h2>{title}</h2>{detail && <p>{detail}</p>}</div>
        {action && <div className="kr-pg-panel-action">{action}</div>}
      </header>
      {children}
    </article>
  );
}

function Breakdown({ kind, values = [], summary, period }: {
  kind: 'mix' | 'readiness'; values?: RankedValue[]; summary?: { notStarted: number; shaky: number; solid: number }; period?: string;
}) {
  const [selected, setSelected] = useState<string | null>(null);
  const data = kind === 'mix' ? values.map(item => ({ ...item, ...MIX[item.id] })) : [
    { id: 'not-started', label: 'Not started', value: summary?.notStarted ?? 0, colour: '#999da4', note: 'Topics with no recorded readiness yet.' },
    { id: 'shaky', label: 'Shaky', value: summary?.shaky ?? 0, colour: '#b27d2d', note: 'Topics that would benefit from another look.' },
    { id: 'solid', label: 'Solid', value: summary?.solid ?? 0, colour: '#397f7c', note: 'Topics you currently feel secure with.' },
  ];
  const total = data.reduce((sum, item) => sum + item.value, 0);
  const unit = kind === 'mix' ? 'sessions' : 'topics';
  return (
    <Panel eyebrow={kind === 'mix' ? 'Session design' : 'Current picture'}
      title={<span className="kr-pg-breakdown-title">{kind === 'mix' ? 'Learning mix' : 'Topic readiness'}<span><strong>{total}</strong> {unit}</span></span>}
      detail={kind === 'mix' ? 'How you spent your study sessions.' : 'How your topics feel right now.'}>
      <div className="kr-pg-panel-body">
        <div className="kr-pg-breakdown" role="group" aria-label={kind === 'mix' ? 'Session types' : 'Readiness levels'}>
          {data.map(item => (
            <button type="button" key={item.id} aria-pressed={selected === item.id} onClick={() => setSelected(item.id)}
              style={{ '--kr-pg-item': item.colour } as CSSProperties}>
              <span className="kr-pg-breakdown-label"><i aria-hidden="true" />{item.label}</span>
              <strong>{pct(item.value, total)}<small>%</small></strong>
              <span className="kr-pg-breakdown-count">{item.value} {unit}</span>
              <span className="kr-pg-breakdown-bar" aria-hidden="true"><Bar value={pct(item.value, total)} label={item.label} tone="item" colour={item.colour} /></span>
            </button>
          ))}
        </div>
        <p className="kr-pg-reading" role="status">{!total ? `No ${unit} recorded yet.` : data.find(item => item.id === selected)?.note ?? 'Select a category to read more.'}</p>
      </div>
      <footer className="kr-pg-panel-foot">{kind === 'mix' ? `Recorded sessions${period ? ` · ${period}` : ' in the selected period'}.` : 'Current snapshot · subject filter applies; date range does not.'}</footer>
    </Panel>
  );
}

function SubjectPicker({ subjects, value, onChange }: { subjects: string[]; value: string[]; onChange: (next: string[]) => void }) {
  const [query, setQuery] = useState('');
  const visible = subjects.filter(subject => subject.toLowerCase().includes(query.toLowerCase().trim()));
  return (
    <div className="kr-pg-subjects">
      <Popover>
        <PopoverTrigger render={<Button variant="outline" className="nsu-ink-outline kr-pg-picker" aria-label="Filter by subject" />}>
          <span>{value.length ? value.length === 1 ? value[0] : `${value.length} subjects selected` : 'All subjects'}</span><ChevronDown aria-hidden="true" />
        </PopoverTrigger>
        <PopoverContent className="kr-pg-subject-menu" align="start">
          <div className="kr-pg-subject-search"><Search aria-hidden="true" /><Input value={query} onChange={event => setQuery(event.target.value)} placeholder="Find a subject…" aria-label="Find a subject" /></div>
          <div className="kr-pg-subject-options" role="group" aria-label="Filter by subject">
            {visible.map(subject => (
              <label className="kr-pg-subject-option" key={subject} data-selected={value.includes(subject) || undefined}>
                <Checkbox checked={value.includes(subject)} onCheckedChange={checked => onChange(checked ? [...value, subject] : value.filter(item => item !== subject))} />
                <span>{subject}</span>
              </label>
            ))}
            {!visible.length && <p className="kr-pg-muted">No matching subjects.</p>}
          </div>
          <div className="kr-pg-subject-foot"><span>{value.length || 'All'} subjects</span><Button variant="outline" size="sm" className="nsu-ink-outline" disabled={!value.length} onClick={() => onChange([])}>Clear selection</Button></div>
        </PopoverContent>
      </Popover>
      {!!value.length && (
        <div className="kr-pg-chosen">
          {value.map(subject => <Button key={subject} variant="outline" size="sm" className="nsu-ink-outline" aria-label={`Remove ${subject}`} onClick={() => onChange(value.filter(item => item !== subject))}>{subject}<X aria-hidden="true" /></Button>)}
        </div>
      )}
    </div>
  );
}

function Skeleton({ className = '' }: { className?: string }) {
  // Skeleton is purchased but not compiled into the runtime (needs compiling into the runtime).
  return <span className={`kr-pg-skeleton ${className}`} aria-hidden="true" />;
}

export default function ProgressAfter() {
  const ids = useId();
  const sessions = useMemo(() => sampleSessions(), []);
  const profile = useMemo(sampleProfile, []);
  const streak = useMemo(() => sampleStreak(), []);
  const topics = useMemo(sampleTopicMastery, []);
  const recommendation = useMemo(sampleRecommendation, []);
  const questSample = useMemo(sampleQuest, []);
  const gamification = useMemo(sampleGamification, []);
  const challenge = useMemo(sampleWeeklyChallenge, []);
  const mastery = useMemo(sampleStrategyMastery, []);

  const [preview, setPreview] = useState<'loaded' | 'loading'>('loaded');
  const [tab, setTab] = useState<Section>('overview');
  const [range, setRange] = useState<DashboardRange>('week');
  const [metric, setMetric] = useState<ActivityMetric>('sessions');
  const [selectedSubjects, setSelectedSubjects] = useState<string[]>([]);
  const [focusKey, setFocusKey] = useState<string | null>(null);
  const [record, setRecord] = useState(false);
  const [average, setAverage] = useState(false);
  const [insights, setInsights] = useState<Record<string, boolean>>({});
  const [questClaimed, setQuestClaimed] = useState(false);
  const [openMilestone, setOpenMilestone] = useState<string | null>(null);
  const [gallery, setGallery] = useState(false);
  const [badgeId, setBadgeId] = useState<string | null>(null);

  // The same derivations DashboardView makes.
  const subjects = useMemo(() => [...new Set([...profile.subjects.map(item => item.subjectName), ...sessions.map(item => item.subject)])].sort((a, b) => a.localeCompare(b)), [profile, sessions]);
  const visibleSubjects = selectedSubjects.length ? subjects.filter(item => selectedSubjects.includes(item)) : subjects;
  const scoped = useMemo(() => selectSubjects(sessions, selectedSubjects), [sessions, selectedSubjects]);
  const bounds = useMemo(() => getRangeBounds(range), [range]);
  const inRange = useMemo(() => filterSessions(scoped, range), [scoped, range]);
  const buckets = useMemo(() => buildActivityBuckets(scoped, range), [scoped, range]);
  const confidence = useMemo(() => confidenceInRange(selectSubjects(collectConfidenceObservations(sessions, [], []), selectedSubjects), range), [sessions, selectedSubjects, range]);
  const mix = useMemo(() => buildSessionMix(inRange), [inRange]);
  const readiness = useMemo(() => buildMasterySummary(topics), [topics]);
  const goal = useMemo(() => caoGoalStanding(profile, [], 'senior'), [profile]);
  const todayKey = toLocalDateKey(new Date());
  const subjectLabel = selectedSubjects.length ? selectedSubjects.join(' · ') : 'All subjects';
  const activityInsights = useMemo(() => buildActivityInsights(buckets, metric, subjectLabel), [buckets, metric, subjectLabel]);
  const confidenceItems = useMemo(() => buildConfidenceInsights(confidence, visibleSubjects), [confidence, visibleSubjects]);
  const mockInsights = useMemo(() => buildMockInsights([], 'all', todayKey), [todayKey]);
  const totalMinutes = Math.round(inRange.reduce((sum, item) => sum + Math.max(0, item.actualSeconds), 0) / 60);
  const activeDays = new Set(inRange.map(item => item.date)).size;
  const avgConfidence = averageConfidence(confidence);
  const todayLabel = useMemo(() => new Date().toLocaleDateString('en-IE', { weekday: 'long', day: 'numeric', month: 'long' }), []);
  const nextBlock = useMemo(() => {
    try {
      const priorities = computeSubjectPriorities(profile.subjects, undefined, profile.examStartDate);
      const weeks = computeWeeksUntilExam(profile.examStartDate);
      const timetable = generateWeeklyTimetable(allocateSessions(priorities, weeks), weeks, 0, profile.restDays ?? [], profile.defaultBlockDuration ?? 45);
      const dayIndex = new Date().getDay() === 0 ? 6 : new Date().getDay() - 1;
      return timetable[dayIndex]?.blocks?.[0];
    } catch { return undefined; }
  }, [profile]);

  const toggleInsights = (key: string) => setInsights(current => ({ ...current, [key]: !current[key] }));
  const chooseTab = (next: Section) => { setTab(next); if (next !== 'milestones') setPreview('loaded'); };
  const loading = preview === 'loading';

  /* ---------------------------------------------------------- panels ---- */
  const periodUnit = buckets.length === 12 && buckets[0]?.label === 'Jan' ? 'year' : buckets.length > 7 ? 'month' : 'week';
  const annual = periodUnit === 'year';
  const activityTotal = buckets.reduce((sum, bucket) => sum + bucket[metric], 0);
  const activeBuckets = buckets.filter(bucket => bucket.sessions > 0).length;
  const elapsed = buckets.filter(bucket => bucket.start <= Date.now());
  const mean = elapsed.length ? elapsed.reduce((sum, bucket) => sum + bucket[metric], 0) / elapsed.length : 0;
  const activityId = `${ids}-activity-insights`;
  const activity = (
    <Panel eyebrow={`Study activity / ${bounds.label}`} title={metric === 'sessions' ? `Your ${periodUnit} in focus.` : 'The time you made.'} detail={subjectLabel}
      action={<div className="kr-pg-controls">
        <Tabs value={metric} onValueChange={value => setMetric(value as ActivityMetric)}>
          <TabsList aria-label="Study activity measure"><TabsTrigger value="sessions">Sessions</TabsTrigger><TabsTrigger value="minutes">Minutes</TabsTrigger></TabsList>
        </Tabs>
        <Insights label="study activity" open={Boolean(insights.activity)} onToggle={() => toggleInsights('activity')} controls={activityId} />
      </div>}>
      {insights.activity && (
        <div className="kr-pg-insights" id={activityId}>
          <label className="kr-pg-check"><Checkbox checked={average} onCheckedChange={checked => setAverage(Boolean(checked))} />Show period average</label>
          <p className="kr-pg-muted">The average covers elapsed days or months in this period. It isn’t a study target.</p>
          <InsightIndex id={`${ids}-activity`} items={activityInsights} context={`${bounds.label} · ${subjectLabel}`} />
        </div>
      )}
      <div className="kr-pg-reading-row">
        <strong>{activityTotal}<small>{metric === 'sessions' ? 'sessions' : 'minutes'}</small></strong>
        <span>across {activeBuckets} active {annual ? 'months' : 'days'}</span>
        <Button variant="outline" size="sm" className="nsu-ink-outline" onClick={() => setRecord(value => !value)}>{record ? 'Show graph' : 'Read the numbers'}</Button>
      </div>
      {record ? (
        <table className="kr-pg-table">
          <caption>{bounds.label} · {subjectLabel}</caption>
          <thead><tr><th scope="col">Date</th><th scope="col">Sessions</th><th scope="col">Minutes</th></tr></thead>
          <tbody>{buckets.map(day => <tr key={day.key}><th scope="row">{day.accessibleLabel}</th><td>{day.sessions}</td><td>{day.minutes}</td></tr>)}</tbody>
        </table>
      ) : (
        <div role="img" aria-label={`Study activity chart showing ${metric}`}>
          <ChartContainer config={{ sessions: { label: 'Sessions', color: 'var(--nsu-orange)' }, minutes: { label: 'Minutes', color: 'var(--nsu-orange)' } }} className="kr-pg-chart">
            <AreaChart data={buckets} margin={{ left: 4, right: 24, top: 24, bottom: 8 }} accessibilityLayer>
              <CartesianGrid vertical={false} stroke="var(--border)" />
              <XAxis dataKey="label" tickLine={false} axisLine={false} tickMargin={14} minTickGap={24} />
              <YAxis width={38} tickLine={false} axisLine={false} allowDecimals={false} domain={[0, 'auto']} tickMargin={9} />
              <ChartTooltip content={<ChartTooltipContent />} />
              {average && <ReferenceLine y={mean} stroke="var(--muted-foreground)" strokeDasharray="4 5" label={{ value: `Average ${mean.toFixed(1)}`, position: 'insideTopRight', fill: 'var(--muted-foreground)', fontSize: 12 }} />}
              <Area key={metric} type="monotone" dataKey={metric} stroke="var(--nsu-orange)" strokeWidth={2.5} fill="none"
                dot={{ r: 4, fill: 'var(--nsu-orange)', stroke: 'var(--background)', strokeWidth: 2 }} activeDot={{ r: 6, strokeWidth: 3, stroke: 'var(--background)' }} isAnimationActive={false} />
            </AreaChart>
          </ChartContainer>
        </div>
      )}
      <footer className="kr-pg-panel-foot kr-pg-legend"><span><i aria-hidden="true" />Completed study</span><span>Actual recorded study time.</span></footer>
    </Panel>
  );

  const quest = { ...questSample, isClaimed: questClaimed };
  const questProgress = Math.min(100, quest.current / quest.quest.target * 100);
  const today = (
    <Panel className="kr-pg-today" eyebrow="Today" title={nextBlock ? nextBlock.subjectName : 'Choose your next move'}
      detail={nextBlock ? `${nextBlock.durationMinutes} min · ${nextBlock.sessionType.replace('-', ' ')}` : 'Keep the momentum small and specific.'}>
      <div className="kr-pg-panel-body kr-pg-today-body">
        <p className="kr-pg-today-message">{recommendation?.reason === 'in-progress' ? 'Continue what you started.' : nextBlock ? 'One focused block is enough.' : 'Build evidence, one session at a time.'}</p>
        <div className="kr-pg-quest">
          <div className="kr-pg-quest-head">
            <span>{quest.isOnboarding ? `Day ${quest.dayNumber} quest` : 'Daily quest'}</span>
            {quest.isCompleted
              ? <span className="kr-pg-done"><Check aria-hidden="true" />Completed</span>
              : <span>{Math.min(quest.current, quest.quest.target)}/{quest.quest.target}</span>}
          </div>
          <p className="kr-pg-quest-title">{quest.quest.title}</p>
          <Bar value={questProgress} label={quest.quest.title} tone={quest.isCompleted ? 'mint' : 'ink'} size="fat" />
        </div>
        {recommendation && recommendation.reason !== 'all-complete' && (
          <p className="kr-pg-muted kr-pg-why">{recommendation.reason === 'in-progress' ? 'Suggested because it’s already underway — finishing beats starting fresh.' : 'Suggested because it’s the next module you haven’t opened.'}</p>
        )}
        <div className="kr-pg-today-actions">
          <Button variant="outline" className="nsu-ink-outline" onClick={() => toast({ message: 'Start studying' })}>Start studying<ArrowRight aria-hidden="true" /></Button>
          {recommendation && <Button variant="outline" className="nsu-ink-outline" onClick={() => toast({ message: `Continue ${recommendation.title}` })}>{recommendation.reason === 'in-progress' ? 'Continue' : 'Open'} {recommendation.title}</Button>}
          {quest.isCompleted && !quest.isClaimed && <Button variant="outline" className="nsu-ink-outline" onClick={() => setQuestClaimed(true)}>Claim {quest.quest.rewardPoints} JP</Button>}
        </div>
      </div>
    </Panel>
  );

  const confidenceId = `${ids}-confidence-insights`;
  const confidencePanel = (
    <Panel eyebrow={`Your check-ins / ${bounds.label}`} title="A different story in every subject." detail="How you felt after study, on a scale of 1–5."
      action={<Insights label="confidence chart" open={Boolean(insights.confidence)} onToggle={() => toggleInsights('confidence')} controls={confidenceId} />}>
      {insights.confidence && (
        <div className="kr-pg-insights" id={confidenceId}>
          <InsightIndex id={`${ids}-confidence`} items={confidenceItems.length ? confidenceItems : [{
            id: 'confidence-empty', title: 'Confidence trend', trend: 'building', evidence: 'No confidence debriefs fall inside the selected period yet.',
            guidance: 'Choose a confidence rating after your next completed session and the subject trend will begin here.',
          }]} context={`${bounds.label} · ${subjectLabel}`} note="Confidence is self-reported, not a grade prediction. Every subject in the current filter is included." />
        </div>
      )}
      <div className="kr-pg-key">
        {visibleSubjects.map(subject => {
          const entries = confidence.filter(point => point.subject === subject);
          const latest = entries[entries.length - 1];
          return (
            <div key={subject}>
              <CrewIllustration className="kr-pg-key-art" subject={subject} />
              <div><strong>{subject}</strong><span>{entries.length} check-ins · {latest ? `latest ${latest.score}/5` : 'none in this period'}</span></div>
              <svg width="32" height="10" aria-hidden="true"><path d="M0 5H32" stroke={subjectColour(subject, subjects)} strokeWidth="2.5" /></svg>
            </div>
          );
        })}
      </div>
      <p className="kr-pg-muted kr-pg-panel-foot">Dots are recorded check-ins; lines join those moments. Dates between them contain no reading. Confidence is your experience of study, not a prediction of your grade.</p>
    </Panel>
  );

  const mockId = `${ids}-mock-insights`;
  const mockPanel = (
    <Panel eyebrow={`Exam evidence / ${bounds.label}`} title="Mock trajectory" detail="Total points from full mock sittings in Points Passport."
      action={<Insights label="mock trajectory" open={Boolean(insights.mocks)} onToggle={() => toggleInsights('mocks')} controls={mockId} />}>
      {insights.mocks && (
        <div className="kr-pg-insights" id={mockId}>
          <InsightIndex id={`${ids}-mocks`} items={mockInsights} context={`${bounds.label} · ${subjectLabel}`}
            note="Total-point trends use comparable full mock sittings only. Subject insights also include single-subject results. These are recorded results, not predictions of final grades." />
        </div>
      )}
      <div className="kr-pg-empty"><h3>No full mocks in this period</h3><p>Add a full mock sitting in Points Passport to build your trajectory. Single-subject results remain in Insights.</p></div>
    </Panel>
  );

  /* ------------------------------------------------------- milestones ---- */
  const available = useMemo(() => getAchievementsForCurriculum('senior'), []);
  const earned = available.filter(item => gamification.unlockedAchievements.includes(item.id));
  const visibleAchievements = available.filter(item => !item.isHidden || gamification.unlockedAchievements.includes(item.id));
  const recent = [...earned].sort((a, b) => (gamification.achievementTimestamps[b.id] ?? 0) - (gamification.achievementTimestamps[a.id] ?? 0)).slice(0, 3);
  const goals = generateWeeklyGoals(gamification.currentRank.id, getWeekNumber());
  const resetDays = new Date().getDay() === 0 ? 1 : 8 - new Date().getDay();
  const allMinutes = Math.round(sessions.reduce((sum, item) => sum + Math.max(0, item.actualSeconds || 0), 0) / 60);
  const methods = STRATEGY_REGISTRY.map(item => ({ ...item, record: mastery[item.moduleId] }))
    .filter(item => item.record && item.record.tier !== 'none')
    .sort((a, b) => TIERS[b.record.tier].level - TIERS[a.record.tier].level);
  const dateLabel = (id: string) => gamification.achievementTimestamps[id] ? new Date(gamification.achievementTimestamps[id]).toLocaleDateString('en-IE', { day: 'numeric', month: 'short' }) : 'Part of your story';
  const bySubject = new Map<string, number>();
  for (const item of sessions) bySubject.set(item.subject, (bySubject.get(item.subject) ?? 0) + item.actualSeconds);
  const topSubject = [...bySubject.entries()].sort((a, b) => b[1] - a[1])[0]?.[0] ?? '—';
  const termHours = allMinutes / 60 >= 10 ? String(Math.round(allMinutes / 60)) : String(Math.round(allMinutes / 6) / 10);
  const badge = available.find(item => item.id === badgeId);
  const toggleMilestone = (key: string) => setOpenMilestone(current => (current === key ? null : key));

  const milestones = loading ? (
    <Panel eyebrow="Milestones" title="Progress is loading" detail="Your goals and achievements will appear here.">
      <div className="kr-pg-panel-body kr-pg-loading" aria-busy="true">
        <Skeleton className="kr-pg-skeleton-line" /><Skeleton className="kr-pg-skeleton-short" />
        <div className="kr-pg-skeleton-row"><Skeleton className="kr-pg-skeleton-figure" /><Skeleton className="kr-pg-skeleton-figure" /><Skeleton className="kr-pg-skeleton-figure" /></div>
      </div>
    </Panel>
  ) : (
    <div className="kr-pg-milestones">
      <article className="kr-pg-panel kr-pg-hero" aria-label="Study Passport — all-time record">
        <div className="kr-pg-hero-intro"><Eyebrow>Your learning record / Milestones</Eyebrow><h2>The work <em>adds up.</em></h2><p>A record of the time, habits and small steps you have made your own.</p></div>
        <div className="kr-pg-rank">
          <ThemeArtwork src="/assets/star-crew/personal/07-maker.png" transparentBackground alt="" width={80} height={80} className="kr-pg-art" />
          <div>
            <Eyebrow>Your rank</Eyebrow>
            <h3>{gamification.currentRank.title}</h3>
            <p>{gamification.nextRank ? <><strong>{Math.max(0, gamification.nextRank.minPoints - gamification.totalPointsEarned).toLocaleString()}</strong> points to {gamification.nextRank.title}</> : 'Highest rank reached.'}</p>
          </div>
          <div className="kr-pg-rank-line">
            <span>{gamification.currentRank.title}</span><strong>{gamification.rankProgress}%</strong><span>{gamification.nextRank?.title ?? 'Complete'}</span>
            <Bar value={gamification.rankProgress} label="Rank progress" tone="ink" />
          </div>
          <p className="kr-pg-rank-totals"><span><strong>{gamification.totalPointsEarned.toLocaleString()}</strong> XP earned</span><span>{SAMPLE_POINTS.available.toLocaleString()} JP available to spend</span></p>
        </div>
        <dl className="kr-pg-all-time">
          {([[streak.currentStreak, 'Day streak'], [streak.longestStreak, 'Longest streak'], [sessions.length, 'Sessions'], [formatDuration(allMinutes), 'Focused time'], [`${earned.length} / ${visibleAchievements.length}`, 'Achievements']] as const).map(([value, label]) => (
            <div key={label}><dt>{label}</dt><dd>{typeof value === 'number' ? value.toLocaleString() : value}</dd></div>
          ))}
        </dl>
      </article>

      <div className="kr-pg-pair">
        <Panel eyebrow={`This week / Resets ${resetDays === 1 ? 'tomorrow' : `in ${resetDays} days`}`} title="Three useful targets.">
          <div className="kr-pg-targets">
            {goals.map((item, index) => {
              const current = Math.max(0, gamification.weeklyGoalProgress[item.metric] ?? 0);
              const done = current >= item.target;
              return (
                <div className="kr-pg-target" key={item.id} data-done={done || undefined}>
                  <span className="kr-pg-target-mark">{done ? <Check aria-label="Complete" /> : serial(index + 1)}</span>
                  <div><h3>{item.label}</h3><Bar value={Math.min(100, current / item.target * 100)} label={item.label} tone={done ? 'mint' : 'ink'} /></div>
                  <strong>{Math.min(current, item.target)}<span> / {item.target}</span></strong>
                </div>
              );
            })}
          </div>
          {challenge.isLoaded && challenge.challenge && (
            <div className="kr-pg-acc kr-pg-challenge">
              <AccordionItem id={`${ids}-challenge`} open={openMilestone === 'challenge'} onToggle={() => toggleMilestone('challenge')}
                title={<><small>Weekly challenge</small><strong>{challenge.challenge.title}</strong></>}
                aside={challenge.isClaimed ? 'Claimed' : `${Math.min(challenge.current, challenge.challenge.target)} / ${challenge.challenge.target}`}>
                <p>{challenge.challenge.description}</p>
                <p>{challenge.challenge.rewardPoints} JP when complete.</p>
              </AccordionItem>
            </div>
          )}
        </Panel>

        <Panel eyebrow="Recognition" title="Marks of progress." action={<span className="kr-pg-count">{earned.length} earned</span>}>
          {recent.length ? (
            <div className="kr-pg-badges">
              {recent.map(item => (
                <button type="button" key={item.id} onClick={() => setBadgeId(item.id)}>
                  <AchievementBadge achievementId={item.id} size={72} /><strong>{item.title}</strong><small>{dateLabel(item.id)}</small>
                </button>
              ))}
            </div>
          ) : <p className="kr-pg-muted kr-pg-panel-body">Every collection starts with a first step. Your earned milestones will appear here.</p>}
          <div className="kr-pg-panel-body kr-pg-gallery-row">
            <Button variant="outline" className="nsu-ink-outline kr-pg-gallery" aria-expanded={gallery} onClick={() => setGallery(value => !value)}>{gallery ? 'Close gallery' : 'Open achievement gallery'}<ArrowRight aria-hidden="true" /></Button>
          </div>
        </Panel>
      </div>

      {gallery && (
        <Panel eyebrow="Achievement gallery" title="The collection so far." label="Achievement gallery">
          <div className="kr-pg-panel-body"><AchievementGallery unlockedAchievements={gamification.unlockedAchievements} achievementTimestamps={gamification.achievementTimestamps} curriculumLevel="senior" showHeader={false} /></div>
        </Panel>
      )}

      <Panel eyebrow="Learning methods" title="From knowing to doing." detail="Techniques you have brought into your learning."
        action={<span className="kr-pg-count">{methods.length} method{methods.length === 1 ? '' : 's'}</span>}>
        {methods.length ? (
          <div className="kr-pg-panel-body">
            <div className="kr-pg-method-head" aria-hidden="true"><span>Technique</span><span>Use in study</span><span>Stage</span></div>
            <div className="kr-pg-acc">
              {methods.map(item => (
                <AccordionItem key={item.moduleId} id={`${ids}-${item.moduleId}`} open={openMilestone === item.moduleId} onToggle={() => toggleMilestone(item.moduleId)}
                  title={<span className="kr-pg-method"><strong>{item.strategyName}</strong><span>{item.record.sessionCount} session{item.record.sessionCount === 1 ? '' : 's'}</span>
                    <span className="kr-pg-stage">{[1, 2, 3, 4].map(level => <i key={level} data-filled={level <= TIERS[item.record.tier].level || undefined} aria-hidden="true" />)}<small>{TIERS[item.record.tier].label}</small></span></span>}>
                  <p>{item.description}.{item.record.subjectsSeen.length > 0 && <> Used in {item.record.subjectsSeen.join(', ')}.</>}</p>
                </AccordionItem>
              ))}
            </div>
          </div>
        ) : <p className="kr-pg-muted kr-pg-panel-body">Complete a strategy module, then use that technique during a study session to begin tracking it here.</p>}
      </Panel>

      <Panel eyebrow="Personal records" title="Best efforts." detail="A few days and weeks to remember. Every session has its place.">
        <div className="kr-pg-records">
          {([['In a day', [['bestDayPoints', 'Points earned'], ['bestDaySections', 'Sections completed']]], ['In a week', [['bestWeekPoints', 'Points earned'], ['bestWeekSessions', 'Study sessions']]]] as const).map(([title, records]) => (
            <section key={title}><h3>{title}</h3><dl>{records.map(([key, label]) => <div key={key}><dt>{label}</dt><dd>{gamification.personalBests[key] > 0 ? gamification.personalBests[key].toLocaleString() : <span className="kr-pg-muted">Yet to record</span>}</dd></div>)}</dl></section>
          ))}
        </div>
      </Panel>

      <article className="kr-pg-panel kr-pg-term">
        <div><Eyebrow>Since 1 September</Eyebrow><h2>A term taking shape.</h2><p><strong>{termHours}h</strong> focused · <strong>{sessions.length}</strong> sessions · Most studied: <strong>{topSubject}</strong></p></div>
        <Button variant="outline" className="nsu-ink-outline" onClick={() => toast({ message: 'Save term review' })}>Save term review<Download aria-hidden="true" /></Button>
      </article>

      {/* The badge was a native <dialog> with a blurred backdrop; now the runtime Dialog. */}
      <Dialog open={Boolean(badge)} onOpenChange={open => { if (!open) setBadgeId(null); }}>
        <DialogContent size="sm" className="kr-pg-dialog" showCloseButton={false}>
          {badge && (
            <div className="kr-pg kr-pg-badge-dialog">
              <Button variant="outline" size="icon" className="nsu-ink-outline kr-pg-dialog-close" aria-label="Close achievement" onClick={() => setBadgeId(null)}><X aria-hidden="true" /></Button>
              <AchievementBadge achievementId={badge.id} size={110} />
              <Eyebrow>Achievement earned</Eyebrow>
              <DialogTitle className="kr-pg-dialog-title">{badge.title}</DialogTitle>
              <DialogDescription>{badge.description}</DialogDescription>
              <small>{dateLabel(badge.id)}</small>
            </div>
          )}
        </DialogContent>
      </Dialog>
    </div>
  );

  /* ---------------------------------------------------------- summary ---- */
  const highest = Math.max(1, ...buckets.map(bucket => bucket.minutes));
  const focus = buckets.find(bucket => bucket.key === focusKey)
    ?? buckets.reduce<ActivityBucket | undefined>((best, bucket) => (!best || bucket.minutes > best.minutes ? bucket : best), undefined);
  const stats = [
    { label: 'Sessions', value: String(inRange.length), detail: `Across ${activeDays} active day${activeDays === 1 ? '' : 's'}` },
    { label: 'Confidence', value: avgConfidence === null ? '—' : avgConfidence.toFixed(1), detail: avgConfidence === null ? 'Awaiting your first check-in' : 'Your check-in, out of 5' },
    { label: 'Study streak', value: String(streak.currentStreak), detail: 'Consecutive days · all subjects' },
  ];
  const reached = goal.status === 'ready' && goal.gap <= 0;
  const position = (points: number) => Math.min(100, Math.max(0, points / CAO_MAX_POINTS * 100));

  return (
    <section className="kr-section kr-pg" aria-label="My Progress on Kobra">
      <div className="kr-pg-preview">
        <span className="kr-pg-eyebrow" id={`${ids}-state`}>Preview state</span>
        <Tabs value={preview} onValueChange={value => { setPreview(value as 'loaded' | 'loading'); if (value === 'loading') setTab('milestones'); }}>
          <TabsList aria-labelledby={`${ids}-state`}><TabsTrigger value="loaded">Loaded</TabsTrigger><TabsTrigger value="loading">Milestones loading</TabsTrigger></TabsList>
        </Tabs>
        <span className="kr-pg-sample">{SAMPLE_LABEL}</span>
      </div>

      <div className="kr-pg-heading">
        <div className="kr-pg-heading-copy">
          <div className="kr-pg-dateline"><p className="kr-pg-kicker">Your learning record</p><span aria-hidden="true" /><p>{todayLabel}</p></div>
          <h2 className="kr-pg-title">Your learning, in motion.</h2>
          <p className="kr-pg-lede">Study rhythm, confidence and practice evidence—connected in one clear view.</p>
        </div>
        {tab !== 'milestones' && (
          <div className="kr-pg-filters">
            <SubjectPicker subjects={subjects} value={selectedSubjects} onChange={setSelectedSubjects} />
            <Tabs value={range} onValueChange={value => setRange(value as DashboardRange)}>
              <TabsList aria-label="Dashboard time range">{RANGES.map(item => <TabsTrigger key={item.id} value={item.id}>{item.label}</TabsTrigger>)}</TabsList>
            </Tabs>
          </div>
        )}
      </div>

      {tab === 'overview' && goal.status === 'ready' && (
        <article className="kr-pg-panel kr-pg-goal" aria-label="CAO points against your goal">
          <div className="kr-pg-goal-figures">
            <Eyebrow>CAO points</Eyebrow>
            <dl><div><dt>Now</dt><dd>{goal.current}</dd></div><div><dt>Goal</dt><dd>{goal.goal}</dd></div></dl>
          </div>
          <div className="kr-pg-goal-chart">
            <p className="kr-pg-goal-gap" data-reached={reached || undefined}>{reached && <Check aria-hidden="true" />}{caoGapLabel(goal.gap)}</p>
            <div className="kr-pg-goal-bar" role="img" aria-label={`${goal.current} points now, goal ${goal.goal} points, out of ${CAO_MAX_POINTS}. ${caoGapLabel(goal.gap)}.`}>
              <Bar value={position(goal.current)} label="CAO points now" tone={reached ? 'mint' : 'orange'} size="fat" />
              <span className="kr-pg-goal-marker" data-edge={goal.goal / CAO_MAX_POINTS > 0.85 || undefined} style={{ left: `${position(goal.goal)}%` }} aria-hidden="true"><b>Goal</b></span>
            </div>
            <div className="kr-pg-goal-scale" aria-hidden="true"><span>0</span><span>{CAO_MAX_POINTS}</span></div>
            <p className="kr-pg-muted kr-pg-goal-source">{caoEvidenceLabel(goal.evidence)} Best six subjects, with the Higher Maths bonus.</p>
          </div>
          <div className="kr-pg-goal-actions">
            <Button variant="outline" className="nsu-ink-outline" onClick={() => toast({ message: 'Add a mock result' })}>Add a mock result</Button>
            <Button variant="outline" className="nsu-ink-outline" onClick={() => toast({ message: 'Update your grades' })}>Update your grades</Button>
          </div>
        </article>
      )}

      {tab !== 'milestones' && (tab === 'overview' || tab === 'study') && (
        <article className="kr-pg-panel kr-pg-notebook" aria-label="Learning record summary">
          <div className="kr-pg-notebook-feature">
            <Eyebrow>{bounds.label} / Focus time</Eyebrow>
            <div className="kr-pg-focus-heading">
              <h2>Time you made<br /><em>for yourself.</em></h2>
              <ThemeArtwork src="/assets/star-crew/companions/thinker.png" transparentBackground alt="" width={84} height={84} className="kr-pg-art" />
            </div>
            <strong className="kr-pg-focus-total">{formatDuration(totalMinutes)}</strong>
            <div className="kr-pg-columns" data-dense={buckets.length > 7 || undefined} role="group" aria-label="Focus time in the selected period">
              {buckets.map(bucket => (
                <button type="button" key={bucket.key} aria-label={`${bucket.accessibleLabel}: ${bucket.minutes} minutes`} aria-pressed={focus?.key === bucket.key}
                  onClick={() => setFocusKey(bucket.key)} onMouseEnter={() => setFocusKey(bucket.key)}>
                  <span className="kr-pg-column-track" aria-hidden="true"><i style={{ height: `${bucket.minutes / highest * 100}%` }} /></span>
                  <span className="kr-pg-column-day">{bucket.label}</span>
                  <strong>{formatDuration(bucket.minutes)}</strong>
                </button>
              ))}
            </div>
            <p className="kr-pg-muted kr-pg-focus-reading" role="status">
              {focus ? `${focus.accessibleLabel} · ${focus.minutes ? `${focus.minutes} minute${focus.minutes === 1 ? '' : 's'} of focused study` : 'No study recorded'}` : 'No study recorded in this period'}
            </p>
          </div>
          <div className="kr-pg-notebook-notes">
            <Eyebrow>In the margins</Eyebrow>
            {stats.map(stat => <div className="kr-pg-note" key={stat.label}><div><h3>{stat.label}</h3><p>{stat.detail}</p></div><strong>{stat.value}</strong></div>)}
            <div className="kr-pg-points"><Eyebrow>Journey points</Eyebrow><p><strong>{SAMPLE_POINTS.earned.toLocaleString()}</strong> earned to date</p><p>{SAMPLE_POINTS.available.toLocaleString()} available to spend</p></div>
          </div>
        </article>
      )}

      <nav className="kr-pg-sections" aria-label="Progress sections">
        <Tabs value={tab} onValueChange={value => chooseTab(value as Section)} className="kr-pg-sections-tabs">
          <TabsList aria-label="Dashboard sections">
            {SECTIONS.map((item, index) => <TabsTrigger key={item.id} value={item.id}><span aria-hidden="true">{serial(index + 1)}</span>{item.label}</TabsTrigger>)}
          </TabsList>
        </Tabs>
        <div className="kr-pg-sections-select">
          <span className="kr-pg-eyebrow">Explore your record</span>
          <Select value={tab} items={SECTION_ITEMS} onValueChange={value => { if (typeof value === 'string') chooseTab(value as Section); }}>
            <SelectTrigger aria-label="Progress section"><SelectValue /><small>{SECTIONS.findIndex(item => item.id === tab) + 1} / {SECTIONS.length}</small></SelectTrigger>
            <SelectContent align="start" alignItemWithTrigger={false}>
              {SECTIONS.map((item, index) => <SelectItem key={item.id} value={item.id}><small className="kr-pg-select-n">{serial(index + 1)}</small>{item.label}</SelectItem>)}
            </SelectContent>
          </Select>
        </div>
      </nav>

      <div className="kr-pg-grid">
        {tab === 'overview' && <>{activity}{today}{confidencePanel}{mockPanel}</>}
        {tab === 'study' && <>{activity}<Breakdown kind="mix" values={mix} period={bounds.label} /></>}
        {tab === 'confidence' && <>{confidencePanel}<Breakdown kind="readiness" summary={readiness} /></>}
        {tab === 'practice' && <>{mockPanel}<div className="kr-pg-pair"><Breakdown kind="mix" values={mix} period={bounds.label} /><Breakdown kind="readiness" summary={readiness} /></div></>}
        {tab === 'milestones' && milestones}
      </div>
    </section>
  );
}
