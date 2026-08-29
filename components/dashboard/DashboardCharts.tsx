import React, { useEffect, useMemo, useRef, useState } from 'react';
import type { UnifiedMockResult } from '../../types';
import {
  CONFIDENCE_LABELS,
  type ActivityBucket,
  type ActivityMetric,
  type ConfidenceObservation,
  type MasterySummary,
  type RangeBounds,
  type RankedValue,
  type RhythmDay,
} from './dashboardAnalytics';

const CHART_HEIGHT = 244;

function useChartWidth(fallback = 720) {
  const ref = useRef<HTMLDivElement>(null);
  const [width, setWidth] = useState(fallback);

  useEffect(() => {
    const element = ref.current;
    if (!element) return;
    const measure = () => {
      const next = Math.round(element.getBoundingClientRect().width);
      if (next > 0) setWidth(next);
    };
    measure();
    if (typeof ResizeObserver === 'undefined') return;
    const observer = new ResizeObserver(measure);
    observer.observe(element);
    return () => observer.disconnect();
  }, []);

  return { ref, width };
}

const ChartEmpty: React.FC<{ title: string; detail: string }> = ({ title, detail }) => (
  <div className="flex min-h-[210px] items-center justify-center px-6 text-center">
    <div className="max-w-xs">
      <p className="font-serif text-xl font-semibold text-[var(--ink-primary)]">{title}</p>
      <p className="mt-2 text-sm leading-relaxed text-[var(--ink-muted)]">{detail}</p>
    </div>
  </div>
);

function niceMax(value: number): number {
  if (value <= 4) return Math.max(1, value);
  const magnitude = 10 ** Math.floor(Math.log10(value));
  return Math.ceil(value / magnitude) * magnitude;
}

function countWithUnit(value: number, pluralUnit: string): string {
  const singularUnits: Record<string, string> = {
    sessions: 'session',
    minutes: 'minute',
    uses: 'use',
  };
  const unit = value === 1 ? (singularUnits[pluralUnit] ?? pluralUnit) : pluralUnit;
  return `${value} ${unit}`;
}

export const ActivityChart: React.FC<{
  buckets: ActivityBucket[];
  metric: ActivityMetric;
}> = ({ buckets, metric }) => {
  const { ref, width } = useChartWidth();
  const [activeIndex, setActiveIndex] = useState<number | null>(null);
  const values = buckets.map(bucket => bucket[metric]);
  const hasData = values.some(value => value > 0);
  const maxValue = niceMax(Math.max(...values, 0));
  const margin = { top: 18, right: 10, bottom: 38, left: width < 420 ? 34 : 42 };
  const plotWidth = Math.max(1, width - margin.left - margin.right);
  const plotHeight = CHART_HEIGHT - margin.top - margin.bottom;
  const step = plotWidth / Math.max(1, buckets.length);
  const barWidth = Math.max(3, Math.min(width < 420 ? 18 : 30, step * 0.62));
  const unit = metric === 'sessions' ? 'sessions' : 'minutes';
  const labelEvery = buckets.length > 20 ? (width < 480 ? 6 : 4) : (buckets.length > 10 && width < 480 ? 2 : 1);

  const yFor = (value: number) => margin.top + plotHeight - ((value / maxValue) * plotHeight);
  const gridValues = Array.from(new Set([0, Math.round(maxValue / 2), maxValue])).sort((a, b) => a - b);

  return (
    <div ref={ref} className="relative w-full">
      <svg
        width="100%"
        height={CHART_HEIGHT}
        viewBox={`0 0 ${width} ${CHART_HEIGHT}`}
        role="img"
        aria-label={`Study activity bar chart showing ${unit}`}
      >
        <title>Study activity</title>
        <desc>{hasData ? `${countWithUnit(values.reduce((sum, value) => sum + value, 0), unit)} in this period.` : `No ${unit} recorded in this period.`}</desc>
        {gridValues.map(value => {
          const y = margin.top + plotHeight - ((value / maxValue) * plotHeight);
          return (
            <g key={value}>
              <line x1={margin.left} y1={y} x2={width - margin.right} y2={y} stroke="var(--dashboard-grid)" strokeWidth="1" />
              <text x={margin.left - 8} y={y + 4} textAnchor="end" fontSize="11" fill="var(--ink-muted)">{value}</text>
            </g>
          );
        })}

        {buckets.map((bucket, index) => {
          const value = bucket[metric];
          const x = margin.left + (index * step) + ((step - barWidth) / 2);
          const y = yFor(value);
          const barHeight = Math.max(value > 0 ? 2 : 0, margin.top + plotHeight - y);
          const labelVisible = index % labelEvery === 0 || index === buckets.length - 1;
          const isActive = activeIndex === index;
          return (
            <g
              key={bucket.key}
              role="button"
              tabIndex={0}
              aria-label={`${bucket.accessibleLabel}: ${countWithUnit(value, unit)}`}
              onMouseEnter={() => setActiveIndex(index)}
              onMouseLeave={() => setActiveIndex(null)}
              onFocus={() => setActiveIndex(index)}
              onBlur={() => setActiveIndex(null)}
              onTouchStart={() => setActiveIndex(index)}
              className="outline-none"
            >
              <rect x={margin.left + (index * step)} y={margin.top} width={step} height={plotHeight + 24} fill="transparent" />
              <rect
                x={x}
                y={margin.top + plotHeight - barHeight}
                width={barWidth}
                height={barHeight}
                rx={Math.min(4, barWidth / 3)}
                fill={isActive ? 'var(--dashboard-series-2)' : 'var(--accent-hex)'}
                opacity={value === 0 ? 0 : isActive ? 1 : 0.88}
              />
              {labelVisible && (
                <text x={x + (barWidth / 2)} y={CHART_HEIGHT - 13} textAnchor="middle" fontSize="11" fill="var(--ink-muted)">
                  {bucket.label}
                </text>
              )}
            </g>
          );
        })}

        {!hasData && (
          <g pointerEvents="none">
            <text x={margin.left + (plotWidth / 2)} y={margin.top + (plotHeight / 2) - 4} textAnchor="middle" fontSize="14" fontWeight="600" fill="var(--ink-secondary)">
              No study sessions in this period
            </text>
            <text x={margin.left + (plotWidth / 2)} y={margin.top + (plotHeight / 2) + 16} textAnchor="middle" fontSize="11" fill="var(--ink-muted)">
              Your next completed session will update this chart.
            </text>
          </g>
        )}

        {activeIndex !== null && (() => {
          const bucket = buckets[activeIndex];
          const value = bucket[metric];
          const centre = margin.left + (activeIndex * step) + (step / 2);
          const tooltipWidth = width < 420 ? 132 : 154;
          const tooltipX = Math.max(margin.left, Math.min(width - margin.right - tooltipWidth, centre - (tooltipWidth / 2)));
          const tooltipY = Math.max(3, yFor(value) - 47);
          return (
            <g pointerEvents="none">
              <line x1={centre} y1={margin.top} x2={centre} y2={margin.top + plotHeight} stroke="var(--ink-primary)" strokeWidth="1" opacity="0.18" />
              <rect x={tooltipX} y={tooltipY} width={tooltipWidth} height="36" rx="7" fill="var(--dashboard-tooltip)" stroke="var(--outline-soft)" />
              <text x={tooltipX + 10} y={tooltipY + 14} fontSize="10" fill="var(--dashboard-tooltip-muted)">{bucket.accessibleLabel}</text>
              <text x={tooltipX + 10} y={tooltipY + 28} fontSize="12" fontWeight="600" fill="var(--dashboard-tooltip-ink)">{countWithUnit(value, unit)}</text>
            </g>
          );
        })()}
      </svg>
    </div>
  );
};

interface ConfidenceSeries {
  subject: string;
  points: ConfidenceObservation[];
  color: string;
}

export const ConfidenceChart: React.FC<{
  observations: ConfidenceObservation[];
  bounds: RangeBounds;
}> = ({ observations, bounds }) => {
  const { ref, width } = useChartWidth();
  const [activePoint, setActivePoint] = useState<{ subject: string; index: number } | null>(null);
  const series = useMemo<ConfidenceSeries[]>(() => {
    const grouped = new Map<string, ConfidenceObservation[]>();
    for (const point of observations) {
      const list = grouped.get(point.subject) ?? [];
      list.push(point);
      grouped.set(point.subject, list);
    }
    return [...grouped.entries()]
      .sort((a, b) => b[1].length - a[1].length)
      .slice(0, 5)
      .map(([subject, points], index) => ({
        subject,
        points: points.sort((a, b) => a.timestamp - b.timestamp),
        color: `var(--dashboard-series-${(index % 5) + 1})`,
      }));
  }, [observations]);

  if (observations.length === 0) {
    return <ChartEmpty title="Confidence starts with a debrief" detail="Choose Lost, Shaky, Okay, Good or Confident after a study session. Your subject trend will build here." />;
  }

  const height = 270;
  const margin = { top: 18, right: 12, bottom: 36, left: width < 420 ? 58 : 72 };
  const plotWidth = Math.max(1, width - margin.left - margin.right);
  const plotHeight = height - margin.top - margin.bottom;
  const minTime = bounds.start.getTime();
  const maxTime = Math.max(minTime + DAY_MS, bounds.end.getTime() - 1);
  const xFor = (timestamp: number) => margin.left + (((timestamp - minTime) / (maxTime - minTime)) * plotWidth);
  const yFor = (score: number) => margin.top + plotHeight - (((score - 1) / 4) * plotHeight);
  const dateTicks = [minTime, minTime + ((maxTime - minTime) / 2), maxTime];

  return (
    <div ref={ref} className="w-full">
      <div className="mb-1 flex flex-wrap gap-x-4 gap-y-1 px-1" aria-label="Confidence chart legend">
        {series.map(item => (
          <span key={item.subject} className="inline-flex items-center gap-1.5 text-[11px] font-medium text-[var(--ink-secondary)]">
            <span className="h-2 w-2 rounded-full" style={{ background: item.color }} />
            {item.subject}
          </span>
        ))}
      </div>
      <svg width="100%" height={height} viewBox={`0 0 ${width} ${height}`} role="img" aria-label="Confidence over time by subject">
        <title>Confidence over time</title>
        <desc>Confidence is shown on the five-point debrief scale from Lost to Confident.</desc>
        {CONFIDENCE_LABELS.map((label, index) => {
          const score = index + 1;
          const y = yFor(score);
          return (
            <g key={label}>
              <line x1={margin.left} y1={y} x2={width - margin.right} y2={y} stroke="var(--dashboard-grid)" strokeWidth="1" />
              <text x={margin.left - 9} y={y + 4} textAnchor="end" fontSize="11" fill="var(--ink-muted)">{label}</text>
            </g>
          );
        })}
        {dateTicks.map((timestamp, index) => (
          <text
            key={timestamp}
            x={xFor(timestamp)}
            y={height - 11}
            textAnchor={index === 0 ? 'start' : index === 2 ? 'end' : 'middle'}
            fontSize="11"
            fill="var(--ink-muted)"
          >
            {new Date(timestamp).toLocaleDateString('en-IE', { day: 'numeric', month: 'short' })}
          </text>
        ))}
        {series.map(item => {
          const path = item.points.map((point, index) => `${index === 0 ? 'M' : 'L'} ${xFor(point.timestamp)} ${yFor(point.score)}`).join(' ');
          return (
            <g key={item.subject}>
              {item.points.length > 1 && <path d={path} fill="none" stroke={item.color} strokeWidth="2.25" strokeLinecap="round" strokeLinejoin="round" />}
              {item.points.map((point, index) => {
                const x = xFor(point.timestamp);
                const y = yFor(point.score);
                const isActive = activePoint?.subject === item.subject && activePoint.index === index;
                return (
                  <g
                    key={point.id}
                    role="button"
                    tabIndex={0}
                    aria-label={`${item.subject}, ${point.label}, ${new Date(point.timestamp).toLocaleDateString('en-IE')}`}
                    onMouseEnter={() => setActivePoint({ subject: item.subject, index })}
                    onMouseLeave={() => setActivePoint(null)}
                    onFocus={() => setActivePoint({ subject: item.subject, index })}
                    onBlur={() => setActivePoint(null)}
                    onPointerDown={() => setActivePoint({ subject: item.subject, index })}
                  >
                    <circle cx={x} cy={y} r="15" fill="transparent" />
                    <circle cx={x} cy={y} r={isActive ? 5 : 3.75} fill="var(--surface-paper)" stroke={item.color} strokeWidth={isActive ? 3 : 2.25} />
                  </g>
                );
              })}
            </g>
          );
        })}
        {activePoint && (() => {
          const item = series.find(candidate => candidate.subject === activePoint.subject);
          const point = item?.points[activePoint.index];
          if (!item || !point) return null;
          const x = xFor(point.timestamp);
          const y = yFor(point.score);
          const tooltipWidth = 148;
          const left = Math.max(margin.left, Math.min(width - margin.right - tooltipWidth, x - (tooltipWidth / 2)));
          const top = Math.max(2, y - 50);
          return (
            <g pointerEvents="none">
              <rect x={left} y={top} width={tooltipWidth} height="38" rx="7" fill="var(--dashboard-tooltip)" stroke="var(--outline-soft)" />
              <text x={left + 10} y={top + 15} fontSize="10" fill="var(--dashboard-tooltip-muted)">{item.subject}</text>
              <text x={left + 10} y={top + 29} fontSize="12" fontWeight="600" fill="var(--dashboard-tooltip-ink)">{CONFIDENCE_LABELS[point.score - 1]} · {new Date(point.timestamp).toLocaleDateString('en-IE', { day: 'numeric', month: 'short' })}</text>
            </g>
          );
        })()}
      </svg>
    </div>
  );
};

export const RankedBarChart: React.FC<{
  values: RankedValue[];
  unit: string;
  emptyTitle: string;
  emptyDetail: string;
  limit?: number;
}> = ({ values, unit, emptyTitle, emptyDetail, limit = 6 }) => {
  if (values.length === 0) return <ChartEmpty title={emptyTitle} detail={emptyDetail} />;
  const shown = values.slice(0, limit);
  const max = Math.max(...shown.map(item => item.value), 1);
  return (
    <div className="space-y-4 py-2" role="img" aria-label={`${unit} ranked bar chart`}>
      {shown.map((item, index) => (
        <div key={item.id}>
          <div className="mb-1.5 flex items-end justify-between gap-4 text-xs">
            <span className="min-w-0 truncate font-semibold text-[var(--ink-secondary)]">{item.label}</span>
            <span className="shrink-0 font-mono text-[11px] font-semibold tabular-nums text-[var(--ink-muted)]">{countWithUnit(item.value, unit)}</span>
          </div>
          <div className="h-2 overflow-hidden rounded-full bg-[var(--dashboard-track)]">
            <div
              className="h-full rounded-full transition-[width] duration-500"
              style={{
                width: `${Math.max(item.value > 0 ? 3 : 0, (item.value / max) * 100)}%`,
                background: index === 0 ? 'var(--accent-hex)' : 'var(--dashboard-series-2)',
                opacity: index === 0 ? 1 : Math.max(0.38, 0.82 - (index * 0.08)),
              }}
            />
          </div>
        </div>
      ))}
    </div>
  );
};

export const SessionMixChart: React.FC<{ values: RankedValue[] }> = ({ values }) => {
  const total = values.reduce((sum, item) => sum + item.value, 0);
  if (total === 0) return <ChartEmpty title="No learning mix yet" detail="Session types will separate into new learning, practice and revision once you begin studying." />;
  const colors = ['var(--dashboard-series-1)', 'var(--dashboard-series-2)', 'var(--dashboard-series-3)'];
  return (
    <div className="flex min-h-[210px] flex-col justify-center" role="img" aria-label="Session type allocation">
      <div className="flex h-5 w-full overflow-hidden rounded-full bg-[var(--dashboard-track)]">
        {values.map((item, index) => (
          item.value > 0 && (
            <div
              key={item.id}
              style={{ width: `${(item.value / total) * 100}%`, background: colors[index] }}
              aria-label={`${item.label}: ${countWithUnit(item.value, 'sessions')}`}
            />
          )
        ))}
      </div>
      <div className="mt-6 grid grid-cols-3 gap-3">
        {values.map((item, index) => (
          <div key={item.id}>
            <div className="flex items-center gap-1.5">
              <span className="h-2 w-2 rounded-full" style={{ background: colors[index] }} />
              <span className="text-[11px] font-semibold text-[var(--ink-secondary)]">{item.label}</span>
            </div>
            <p className="mt-1 font-serif text-2xl font-semibold tabular-nums text-[var(--ink-primary)]">{Math.round((item.value / total) * 100)}%</p>
            <p className="text-[10px] text-[var(--ink-muted)]">{item.value} session{item.value === 1 ? '' : 's'}</p>
          </div>
        ))}
      </div>
    </div>
  );
};

export const StudyRhythmChart: React.FC<{ weeks: RhythmDay[][] }> = ({ weeks }) => {
  const hasData = weeks.some(week => week.some(day => day.sessions > 0));
  const visibleDays = weeks.flat().filter(day => !day.isFuture);
  const totalSessions = visibleDays.reduce((sum, day) => sum + day.sessions, 0);
  const activeDays = visibleDays.filter(day => day.sessions > 0).length;
  const cellColor = (day: RhythmDay) => {
    if (day.isFuture) return 'transparent';
    if (day.sessions === 0) return 'var(--dashboard-track)';
    if (day.sessions === 1) return 'var(--dashboard-heat-1)';
    if (day.sessions === 2) return 'var(--dashboard-heat-2)';
    return 'var(--accent-hex)';
  };
  return (
    <div className="flex min-h-[210px] flex-col justify-center" role="img" aria-label={`Thirteen week study rhythm: ${totalSessions} sessions across ${activeDays} active ${activeDays === 1 ? 'day' : 'days'}`}>
      <div className="flex items-stretch gap-2">
        <div className="grid grid-rows-7 gap-1 pt-px text-[9px] text-[var(--ink-muted)]" aria-hidden="true">
          {['M', '', 'W', '', 'F', '', 'S'].map((label, index) => <span key={index} className="flex h-full min-h-[12px] items-center">{label}</span>)}
        </div>
        <div aria-hidden="true" className="grid min-w-0 flex-1 gap-1" style={{ gridTemplateColumns: `repeat(${weeks.length}, minmax(0, 1fr))` }}>
          {weeks.map((week, weekIndex) => (
            <div key={weekIndex} className="grid grid-rows-7 gap-1">
              {week.map(day => (
                <span
                  key={day.key}
                  className="aspect-square min-h-[7px] rounded-[3px] border border-[var(--dashboard-cell-border)]"
                  style={{ background: cellColor(day), opacity: day.isFuture ? 0.35 : 1 }}
                  title={`${day.date.toLocaleDateString('en-IE', { day: 'numeric', month: 'short' })}: ${day.sessions} session${day.sessions === 1 ? '' : 's'}, ${day.minutes} minute${day.minutes === 1 ? '' : 's'}`}
                />
              ))}
            </div>
          ))}
        </div>
      </div>
      <div className="mt-5 flex items-center justify-between gap-3 text-[10px] text-[var(--ink-muted)]">
        <span>{hasData ? 'Each square is one day' : 'Your study days will build a rhythm here'}</span>
        <span className="flex items-center gap-1.5" aria-label="Study intensity legend">
          Less
          {[0, 1, 2, 3].map(level => (
            <span key={level} className="h-2.5 w-2.5 rounded-[2px] border border-[var(--dashboard-cell-border)]" style={{ background: level === 0 ? 'var(--dashboard-track)' : level === 1 ? 'var(--dashboard-heat-1)' : level === 2 ? 'var(--dashboard-heat-2)' : 'var(--accent-hex)' }} />
          ))}
          More
        </span>
      </div>
    </div>
  );
};

export const MasteryBar: React.FC<{ summary: MasterySummary }> = ({ summary }) => {
  if (summary.total === 0) return <ChartEmpty title="No topics rated yet" detail="Topic confidence from War Room and study debriefs will appear here as your readiness picture develops." />;
  const segments = [
    { label: 'Not started', value: summary.notStarted, color: 'var(--dashboard-track-strong)' },
    { label: 'Shaky', value: summary.shaky, color: 'var(--dashboard-series-3)' },
    { label: 'Solid', value: summary.solid, color: 'var(--dashboard-series-2)' },
  ];
  return (
    <div className="flex min-h-[210px] flex-col justify-center" role="img" aria-label="Topic readiness breakdown">
      <div className="flex h-5 overflow-hidden rounded-full bg-[var(--dashboard-track)]">
        {segments.map(segment => segment.value > 0 && (
          <div key={segment.label} style={{ width: `${(segment.value / summary.total) * 100}%`, background: segment.color }} />
        ))}
      </div>
      <div className="mt-6 grid grid-cols-3 gap-4">
        {segments.map(segment => (
          <div key={segment.label}>
            <div className="flex items-center gap-1.5 text-[11px] font-semibold text-[var(--ink-secondary)]">
              <span className="h-2 w-2 rounded-full" style={{ background: segment.color }} />
              {segment.label}
            </div>
            <p className="mt-1 font-serif text-2xl font-semibold tabular-nums text-[var(--ink-primary)]">{segment.value}</p>
            <p className="text-[10px] text-[var(--ink-muted)]">{Math.round((segment.value / summary.total) * 100)}% of topics</p>
          </div>
        ))}
      </div>
    </div>
  );
};

const DAY_MS = 86_400_000;

interface MockMonthTick {
  key: string;
  label: string;
  firstTimestamp: number;
  lastTimestamp: number;
}

function buildMockMonthTicks(timestamps: number[]): MockMonthTick[] {
  const ticks = new Map<string, MockMonthTick>();

  for (const timestamp of timestamps) {
    const date = new Date(timestamp);
    const key = `${date.getFullYear()}-${date.getMonth()}`;
    const existing = ticks.get(key);

    if (existing) {
      existing.lastTimestamp = timestamp;
      continue;
    }

    ticks.set(key, {
      key,
      label: date.toLocaleDateString('en-IE', { month: 'short', year: '2-digit' }),
      firstTimestamp: timestamp,
      lastTimestamp: timestamp,
    });
  }

  return [...ticks.values()];
}

export const MockTrajectoryChart: React.FC<{ mocks: UnifiedMockResult[] }> = ({ mocks }) => {
  const { ref, width } = useChartWidth();
  const [activeIndex, setActiveIndex] = useState<number | null>(null);
  if (mocks.length === 0) return <ChartEmpty title="No full mock results yet" detail="Add a full mock in Points Passport and the total-points trajectory will appear here automatically." />;

  const height = 238;
  const margin = { top: 20, right: 14, bottom: 38, left: width < 420 ? 40 : 48 };
  const plotWidth = Math.max(1, width - margin.left - margin.right);
  const plotHeight = height - margin.top - margin.bottom;
  const timestamps = mocks.map(mock => new Date(`${mock.date}T12:00:00`).getTime());
  const minTime = Math.min(...timestamps);
  const maxTime = Math.max(...timestamps);
  const yMax = Math.max(100, Math.ceil(Math.max(...mocks.map(mock => mock.totalPoints), 0) / 100) * 100);
  const xFor = (timestamp: number) => maxTime === minTime
    ? margin.left + (plotWidth / 2)
    : margin.left + (((timestamp - minTime) / (maxTime - minTime)) * plotWidth);
  const yFor = (points: number) => margin.top + plotHeight - ((points / yMax) * plotHeight);
  const path = mocks.map((mock, index) => `${index === 0 ? 'M' : 'L'} ${xFor(timestamps[index])} ${yFor(mock.totalPoints)}`).join(' ');
  const monthTicks = buildMockMonthTicks(timestamps);
  const visibleMonthTicks = width >= 480 || monthTicks.length <= 2
    ? monthTicks
    : monthTicks.filter((_, index) => index === 0 || index === monthTicks.length - 1);

  return (
    <div ref={ref} className="w-full">
      <svg width="100%" height={height} viewBox={`0 0 ${width} ${height}`} role="img" aria-label="Mock exam total points trajectory">
        <title>Mock trajectory</title>
        {[0, 0.5, 1].map(tick => {
          const y = margin.top + plotHeight - (tick * plotHeight);
          return (
            <g key={tick}>
              <line x1={margin.left} y1={y} x2={width - margin.right} y2={y} stroke="var(--dashboard-grid)" />
              <text x={margin.left - 8} y={y + 4} textAnchor="end" fontSize="11" fill="var(--ink-muted)">{Math.round(yMax * tick)}</text>
            </g>
          );
        })}
        {mocks.length > 1 && <path d={path} fill="none" stroke="var(--accent-hex)" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" />}
        {mocks.map((mock, index) => {
          const x = xFor(timestamps[index]);
          const y = yFor(mock.totalPoints);
          const active = activeIndex === index;
          return (
            <g
              key={mock.id}
              role="button"
              tabIndex={0}
              aria-label={`${mock.label}: ${mock.totalPoints} points`}
              onMouseEnter={() => setActiveIndex(index)}
              onMouseLeave={() => setActiveIndex(null)}
              onFocus={() => setActiveIndex(index)}
              onBlur={() => setActiveIndex(null)}
              onPointerDown={() => setActiveIndex(index)}
            >
              <circle cx={x} cy={y} r="16" fill="transparent" />
              <circle cx={x} cy={y} r={active ? 5.5 : 4} fill="var(--surface-paper)" stroke="var(--accent-hex)" strokeWidth={active ? 3 : 2.5} />
            </g>
          );
        })}
        {visibleMonthTicks.map((tick, index) => {
          const x = xFor((tick.firstTimestamp + tick.lastTimestamp) / 2);
          const textAnchor = monthTicks.length === 1
            ? 'middle'
            : index === 0
              ? 'start'
              : index === visibleMonthTicks.length - 1
                ? 'end'
                : 'middle';
          return (
            <text key={tick.key} x={x} y={height - 12} textAnchor={textAnchor} fontSize="11" fill="var(--ink-muted)">
              {tick.label}
            </text>
          );
        })}
        {activeIndex !== null && (() => {
          const mock = mocks[activeIndex];
          const x = xFor(timestamps[activeIndex]);
          const y = yFor(mock.totalPoints);
          const tooltipWidth = 152;
          const left = Math.max(margin.left, Math.min(width - margin.right - tooltipWidth, x - (tooltipWidth / 2)));
          const top = Math.max(2, y - 51);
          return (
            <g pointerEvents="none">
              <rect x={left} y={top} width={tooltipWidth} height="38" rx="7" fill="var(--dashboard-tooltip)" stroke="var(--outline-soft)" />
              <text x={left + 10} y={top + 15} fontSize="10" fill="var(--dashboard-tooltip-muted)">{mock.label}</text>
              <text x={left + 10} y={top + 29} fontSize="12" fontWeight="600" fill="var(--dashboard-tooltip-ink)">{mock.totalPoints} total points</text>
            </g>
          );
        })()}
      </svg>
    </div>
  );
};
