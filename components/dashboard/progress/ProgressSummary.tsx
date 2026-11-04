import { useEffect, useRef, useState } from 'react';
import { ChevronLeft, ChevronRight } from 'lucide-react';
import { BrandBook } from '../../learning/BrandBook';
import { Tooltip, TooltipTrigger, TooltipContent } from '../../approved-ui-runtime';
import type { ActivityBucket } from '../dashboardAnalytics';
import { Surface, Artwork, Eyebrow } from './shared';

const formatDuration = (minutes: number) => minutes < 60 ? `${minutes}m` : `${Math.floor(minutes / 60)}h${minutes % 60 ? ` ${minutes % 60}m` : ''}`;

export function ProgressSummary({ period, minutes, sessions, activeDays, confidence, streak, pointsEarned, pointsAvailable, buckets }: {
  period: string; minutes: number; sessions: number; activeDays: number; confidence: number | null; streak: number;
  pointsEarned: number; pointsAvailable?: number; buckets: ActivityBucket[];
}) {
  const [selectedKey, setSelectedKey] = useState<string | null>(null);
  const columnsRef = useRef<HTMLDivElement>(null);
  const [scrollable, setScrollable] = useState({ before: false, after: false });
  const annual = buckets.length === 12 && buckets[0]?.label === 'Jan';
  const updateScrollControls = () => {
    const columns = columnsRef.current;
    if (columns) setScrollable({ before: columns.scrollLeft > 1, after: columns.scrollLeft + columns.clientWidth < columns.scrollWidth - 1 });
  };
  const selected = buckets.find(bucket => bucket.key === selectedKey)
    ?? buckets.reduce<ActivityBucket | undefined>((highest, bucket) => !highest || bucket.minutes > highest.minutes ? bucket : highest, undefined);
  useEffect(() => {
    const columns = columnsRef.current;
    if (!columns) return;
    const syncColumns = () => {
      const active = columns.querySelector<HTMLButtonElement>('[aria-pressed=true]');
      if (active && columns.scrollWidth > columns.clientWidth) {
        const containerBounds = columns.getBoundingClientRect();
        const activeBounds = active.getBoundingClientRect();
        if (activeBounds.left < containerBounds.left || activeBounds.right > containerBounds.right) {
          const gap = parseFloat(getComputedStyle(columns).columnGap) || 0;
          const step = activeBounds.width + gap;
          const target = columns.scrollLeft + activeBounds.left - containerBounds.left - (columns.clientWidth - activeBounds.width) / 2;
          columns.scrollLeft = step ? Math.max(0, Math.round(target / step) * step) : 0;
        }
      }
      updateScrollControls();
    };
    syncColumns();
    const observer = typeof ResizeObserver !== 'undefined' ? new ResizeObserver(syncColumns) : null;
    observer?.observe(columns);
    return () => observer?.disconnect();
  }, [selected?.key, buckets.length]);
  const moveColumns = (direction: number) => {
    const columns = columnsRef.current;
    if (!columns) return;
    const first = columns.querySelector('button');
    const gap = parseFloat(getComputedStyle(columns).columnGap) || 0;
    const step = (first?.getBoundingClientRect().width ?? 0) + gap;
    if (step) {
      const pageSize = Math.max(1, Math.round(columns.clientWidth / step));
      const currentIndex = buckets.findIndex(bucket => bucket.key === selected?.key);
      const nextIndex = Math.min(buckets.length - 1, Math.max(0, currentIndex + direction * pageSize));
      setSelectedKey(buckets[nextIndex]?.key ?? null);
    }
  };
  const duration = formatDuration(minutes);
  const stats = [
    { label: 'Sessions', value: String(sessions), detail: `Across ${activeDays} active day${activeDays === 1 ? '' : 's'}`, hint: 'Completed sessions in the selected period and subjects.' },
    { label: 'Confidence', value: confidence === null ? '—' : confidence.toFixed(1), detail: confidence === null ? 'Awaiting your first check-in' : 'Your check-in, out of 5', hint: 'Your average recorded confidence in this selection. This is not a grade prediction.' },
    { label: 'Study streak', value: String(streak), detail: 'Consecutive days · all subjects', hint: 'Your current overall study streak. It is independent of the selected subjects and period.' },
  ];
  const highest = Math.max(1, ...buckets.map(day => day.minutes));
  return <Surface className="pr-notebook pr-study" label="Learning record summary">
    <div className="pr-notebook-feature">
      <Eyebrow>{period} / Focus time</Eyebrow>
      <div className="pr-focus-heading">
        <h2>Time you made<br /><em>for yourself.</em></h2>
        <Artwork src="/assets/star-crew/companions/thinker.png" size={100} />
      </div>
      <strong className="pr-focus-total">{duration}</strong>
      <div ref={columnsRef} className="pr-focus-columns" data-dense={buckets.length > 7} data-annual={annual} onScroll={updateScrollControls} role="group" aria-label="Focus time in the selected period">
        {buckets.map(bucket => <button
          key={bucket.key}
          type="button"
          aria-label={`${bucket.accessibleLabel}: ${bucket.minutes} minutes`}
          aria-pressed={selected?.key === bucket.key}
          onClick={() => setSelectedKey(bucket.key)}
          onFocus={() => setSelectedKey(bucket.key)}
          onMouseEnter={() => setSelectedKey(bucket.key)}
        >
          <span className="pr-focus-track" aria-hidden="true"><i style={{ height: `${bucket.minutes / highest * 100}%` }} /></span>
          <span className="pr-focus-day">{bucket.label}</span>
          <strong>{formatDuration(bucket.minutes)}</strong>
        </button>)}
      </div>
      <div className="pr-focus-caption">
        <p className="pr-focus-reading" role="status">
          {selected ? `${selected.accessibleLabel} · ${selected.minutes ? `${selected.minutes} minute${selected.minutes === 1 ? '' : 's'} of focused study` : 'No study recorded'}` : 'No study recorded in this period'}
        </p>
        {(scrollable.before || scrollable.after) && <div className="pr-focus-navigation" aria-label="Focus time navigation">
          <button type="button" disabled={!scrollable.before} aria-label={`Previous ${annual ? 'months' : 'days'}`} onClick={() => moveColumns(-1)}><ChevronLeft size={16} /></button>
          <button type="button" disabled={!scrollable.after} aria-label={`Next ${annual ? 'months' : 'days'}`} onClick={() => moveColumns(1)}><ChevronRight size={16} /></button>
        </div>}
      </div>
    </div>
    <div className="pr-notebook-notes">
      <BrandBook size={36} />
      <Eyebrow>In the margins</Eyebrow>
      {stats.map(stat => <Tooltip key={stat.label}>
        <TooltipTrigger render={<div tabIndex={0} className="pr-notebook-note" />}>
          <div><h3>{stat.label}</h3><p>{stat.detail}</p></div><strong>{stat.value}</strong>
        </TooltipTrigger>
        <TooltipContent>{stat.hint}</TooltipContent>
      </Tooltip>)}
      <div className="pr-points pr-points-compact">
        <Artwork src="/assets/star-crew/companions/islander.png" size={70} />
        <div><Eyebrow>Journey points</Eyebrow><p><strong>{pointsEarned.toLocaleString()}</strong> <span>earned to date</span></p>
          {pointsAvailable !== undefined && <p>{pointsAvailable.toLocaleString()} available to spend</p>}
        </div>
      </div>
    </div>
  </Surface>;
}
