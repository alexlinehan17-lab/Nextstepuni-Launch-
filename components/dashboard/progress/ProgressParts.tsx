/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The pieces of My Progress in the agreed look (c-progress.html, r5-b2.html
 * "r5-my-progress"): sections on the white page under a hairline, a small
 * label and a heading; the figures in a line, each centred in its column; your
 * own time in orange bars on an outlined track; a subject's character at the
 * left of its row, bare. Every number here is handed in: nothing is worked out
 * again, only shown.
 */
import { type ReactNode } from 'react';
import { List, Row } from '../../ui/List';
import SubjectAvatar from '../../SubjectAvatar';
import { CONFIDENCE_LABELS, type MasterySummary, type RankedValue } from '../dashboardAnalytics';
import { formatMinutes } from './ProgressGraph';

/** A whole number of minutes as a figure with small units: 43<small>h</small> 11<small>m</small>. */
export function Duration({ minutes }: { minutes: number }) {
  const hours = Math.floor(minutes / 60);
  const rest = minutes % 60;
  if (!hours) return <>{rest}<small>m</small></>;
  return <>{hours}<small>h</small>{rest ? <>{' '}{rest}<small>m</small></> : null}</>;
}

/** A section on the page: a hairline above (unless it opens the part), a small label, a heading. */
export function Section({ label, title, big = false, ruled = true, aside, children, className = '', id }: {
  label?: ReactNode; title?: ReactNode; big?: boolean; ruled?: boolean; aside?: ReactNode;
  children?: ReactNode; className?: string; id?: string;
}) {
  return (
    <section className={`mp-sec${ruled ? ' mp-sec--ruled' : ''} ${className}`.trim()} aria-labelledby={id}>
      {label || title ? (
        <div className={aside ? 'mp-sec-headrow' : undefined}>
          <div className="mp-sec-head">
            {label ? <p className="t-label mp-label">{label}</p> : null}
            {title ? <h2 id={id} className={big ? 't-title mp-title' : 't-heading mp-heading'}>{title}</h2> : null}
          </div>
          {aside}
        </div>
      ) : null}
      {children}
    </section>
  );
}

export interface Figure { name: string; value: ReactNode; unit?: string; description?: string }

/** The supporting figures in one line, each number over nothing but its name, centred in its column. */
export function Figures({ items, className = '' }: { items: Figure[]; className?: string }) {
  return (
    <dl className={`mp-figs ${className}`.trim()} data-count={items.length}>
      {items.map(item => (
        <div key={item.name} className="mp-fig" title={item.description}>
          <dt className="t-meta mp-fig-name">{item.name}</dt>
          <dd className="mp-fig-pair">
            <span className="mp-fig-value">{item.value}</span>
            {item.unit ? <span className="mp-fig-unit">{item.unit}</span> : null}
            {item.description ? <span className="sr-only">{`. ${item.description}`}</span> : null}
          </dd>
        </div>
      ))}
    </dl>
  );
}

/** A labelled bar of your own: the name and its readout over an outlined track with an orange fill (green when done). */
export function Bar({ title, readout, share, done = false, art, note }: {
  title: ReactNode; readout: ReactNode; share: number; done?: boolean; art?: ReactNode; note?: string;
}) {
  return (
    <div className="mp-bar">
      {art ? <span className="mp-bar-art" aria-hidden="true">{art}</span> : null}
      <div className="mp-bar-body">
        <div className="mp-bar-head"><span className="mp-bar-title">{title}</span><span className="t-readout mp-bar-readout">{readout}</span></div>
        <div className="mp-track" aria-hidden="true"><i data-done={done || undefined} style={{ width: `${Math.max(0, Math.min(100, share * 100))}%` }} /></div>
        {note ? <span className="sr-only">{note}</span> : null}
      </div>
    </div>
  );
}

/** Your subjects with their characters, each with its share of your time as an orange bar. */
export function SubjectBars({ values, order }: { values: RankedValue[]; order: 'time' | 'name' }) {
  const shown = [...values].filter(item => item.value > 0)
    .sort(order === 'time' ? (a, b) => b.value - a.value : (a, b) => a.label.localeCompare(b.label));
  const most = Math.max(1, ...shown.map(item => item.value));
  return (
    <div className="mp-bars" role="img" aria-label={shown.map(item => `${item.label}: ${item.value} minutes`).join('; ')}>
      {shown.map(item => (
        <Bar key={item.id} title={item.label} readout={item.value >= 90 ? formatMinutes(item.value) : `${item.value} min`}
          share={item.value / most} art={<SubjectAvatar subject={item.label} bare className="mp-art" />} />
      ))}
    </div>
  );
}

/** Topic readiness: one strip (solid green, shaky orange, not started empty), each count under its own part. */
export function ReadinessStrip({ summary }: { summary: MasterySummary }) {
  const parts = [
    { id: 'solid', label: 'Solid', value: summary.solid },
    { id: 'shaky', label: 'Shaky', value: summary.shaky },
    { id: 'not-started', label: 'Not started', value: summary.notStarted },
  ];
  const total = parts.reduce((sum, part) => sum + part.value, 0);
  return (
    <div className="mp-ready">
      <div className="mp-ready-strip" role="img"
        aria-label={`Of ${total} topics: ${summary.solid} solid, ${summary.shaky} shaky, ${summary.notStarted} not started`}>
        {parts.map(part => <i key={part.id} data-part={part.id} style={{ flexGrow: total ? Math.max(part.value, 0.0001) : 1 }} />)}
      </div>
      <div className="mp-ready-key" aria-hidden="true">
        {parts.map(part => <span key={part.id} style={{ flexGrow: total ? Math.max(part.value, 0.0001) : 1 }}><b>{part.value}</b>{part.label}</span>)}
      </div>
    </div>
  );
}

/** The next part, at the foot of a part: "Next · 2 of 5 / Study", a row that moves forward. */
export function NextPart({ position, of, name, onPress }: { position: number; of: number; name: string; onPress: () => void }) {
  return (
    <List className="mp-next" label="Next part">
      <Row over={`Next · ${position} of ${of}`} title={name} forward onPress={onPress} />
    </List>
  );
}

/** A subject's confidence as five steps, with its score in the mono. */
export function ConfidenceScale({ score }: { score: number }) {
  return (
    <span className="mp-scale" aria-hidden="true">
      {[1, 2, 3, 4, 5].map(step => <i key={step} data-on={step <= Math.round(score) || undefined} />)}
    </span>
  );
}

export const confidenceWord = (score: number) => CONFIDENCE_LABELS[Math.max(1, Math.min(5, Math.round(score))) - 1];
