/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Topic Atlas playground demo. Pick a topic and the years it was asked light
 * up along a seventeen-cell strip — the app's year-fingerprint idiom. Flip to
 * "By year" and the same strip becomes the selector and the list turns into
 * the topics that sat that year. Echoes Leonardo's tab-swap feel: the data is
 * the artwork, the motion is the state change, nothing else moves.
 */

import React, { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import { MotionDiv, MotionSpan, useReducedMotion } from '../../Motion';
import { COPY } from '../copy';
import { ATLAS_TOPICS, ATLAS_YEARS } from '../demoData';
import type { DemoProps } from '../sections/Playground';
import { FONT, L } from '../theme';

export const ATLAS_SUBTABS: { id: string; label: string }[] = [
  { id: 'topic', label: 'By topic' },
  { id: 'year', label: 'By year' },
];

/** Orange at 55% on paper — apricot. The one warm element on this view. */
const APRICOT = 'rgba(242, 107, 31, 0.55)';
const EASE: [number, number, number, number] = [0.2, 0.8, 0.2, 1];
const AUTOPLAY_MS = 2000;
const STAGGER_S = 0.02;
const T = COPY.playground.atlas;
const TOTAL_YEARS = ATLAS_YEARS.length;
/** Open on a topic WITH gaps so the fingerprint shows what it is for; fall back to the first row. */
const START_LABEL = 'Photosynthesis';
const START_IDX = Math.max(0, ATLAS_TOPICS.findIndex(t => t.label === START_LABEL));

const promptStyle: React.CSSProperties = {
  fontFamily: FONT.mono, fontSize: 11, letterSpacing: '0.14em', textTransform: 'uppercase',
  color: L.faint, margin: 0, lineHeight: 1.3,
};
const bigStyle: React.CSSProperties = {
  fontFamily: FONT.serif, fontWeight: 600, color: L.ink, fontSize: 'clamp(40px, 5vw, 60px)',
  lineHeight: 1, letterSpacing: '-0.02em', fontVariantNumeric: 'tabular-nums',
};
const unitStyle: React.CSSProperties = {
  fontFamily: FONT.mono, fontSize: 11, letterSpacing: '0.14em', textTransform: 'uppercase', color: L.faint,
};
const yearLabelStyle: React.CSSProperties = {
  fontFamily: FONT.mono, fontSize: 10, letterSpacing: '0.02em', color: L.faint,
  fontVariantNumeric: 'tabular-nums', lineHeight: 1, marginTop: 4, textAlign: 'center',
};
const countStyle: React.CSSProperties = {
  fontFamily: FONT.mono, fontSize: 11, color: L.faint, fontVariantNumeric: 'tabular-nums', letterSpacing: '0.02em',
};
/** Every year cell, asked or not, is the same square with a hairline edge: an unasked year is a hollow cell, so the strip is always full width and the gaps are the picture. */
const cellStyle: React.CSSProperties = { aspectRatio: '1 / 1', border: `1px solid ${L.hairline}` };
/** A topic row in "By year": same rhythm as the topic-mode rows, ink because it is not a control. */
const yearRowClass = 'flex items-center gap-2.5 text-[14px] lg:text-[15px] py-2 lg:py-2.5';
const yearRowStyle: React.CSSProperties = {
  fontFamily: FONT.sans, fontWeight: 500, color: L.ink, lineHeight: 1.25, borderBottom: `1px solid ${L.hairline}`,
};

/** Seventeen cells, wrapping to 9 + 8 under 640px. */
const STRIP_GRID = 'grid grid-cols-9 sm:grid-cols-[repeat(17,minmax(0,1fr))] gap-1 sm:gap-1.5';

/** The serif number with its mono unit. Re-keyed so a change rises in. */
const Count: React.FC<{ n: number; unit: string; reduce: boolean }> = ({ n, unit, reduce }) => (
  <p className="m-0 flex flex-wrap items-baseline gap-x-2">
    {reduce
      ? <span style={bigStyle}>{n}</span>
      : (
        <MotionSpan
          key={n}
          style={{ ...bigStyle, display: 'inline-block' }}
          initial={{ opacity: 0, y: 6 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.22, ease: EASE }}
        >
          {n}
        </MotionSpan>
      )}
    <span style={unitStyle}>{unit}</span>
  </p>
);

/** The fingerprint: asked years fill apricot with a 20ms stagger; unasked stay hollow (hairline edge, paper fill). */
const Fingerprint: React.FC<{ years: number[]; reduce: boolean; label: string }> = ({ years, reduce, label }) => {
  const asked = useMemo(() => new Set(years), [years]);
  return (
    <div role="img" aria-label={label} className={STRIP_GRID}>
      {ATLAS_YEARS.map((y, i) => {
        const on = asked.has(y);
        return (
          <div key={y}>
            {reduce
              ? <div style={{ ...cellStyle, background: on ? APRICOT : L.paper }} />
              : (
                <MotionDiv
                  initial={false}
                  animate={{ backgroundColor: on ? APRICOT : L.paper }}
                  transition={{ duration: 0.3, delay: i * STAGGER_S, ease: EASE }}
                  style={cellStyle}
                />
              )}
            <div style={yearLabelStyle}>{y}</div>
          </div>
        );
      })}
    </div>
  );
};

/** The same strip as a selector: one button per year, the chosen one ink-filled. */
const YearSelector: React.FC<{ year: number; onChange: (y: number) => void }> = ({ year, onChange }) => (
  <div role="group" aria-label={T.yearList} className={STRIP_GRID}>
    {ATLAS_YEARS.map(y => {
      const on = y === year;
      return (
        <button
          key={y}
          type="button"
          aria-pressed={on}
          onClick={() => onChange(y)}
          className="block w-full"
          style={{ background: 'none', border: 0, padding: 0, margin: 0, cursor: 'pointer' }}
        >
          <div
            className={on ? undefined : 'landing-hover-card'}
            style={{
              ...cellStyle,
              borderColor: on ? L.ink : L.hairline,
              background: on ? L.ink : L.paper,
              transition: 'background-color 180ms ease, border-color 180ms ease',
            }}
          />
          <div style={{ ...yearLabelStyle, color: on ? L.ink : L.faint, fontWeight: on ? 700 : 400 }}>{y}</div>
        </button>
      );
    })}
  </div>
);

const TopicRow: React.FC<{ label: string; count: number; on: boolean; onSelect: () => void }> = ({ label, count, on, onSelect }) => (
  <button
    type="button"
    aria-pressed={on}
    onClick={onSelect}
    className="landing-tab flex w-full items-center gap-2.5 text-left text-[14px] lg:text-[15px] py-2 lg:py-2.5"
    style={{
      background: 'none', border: 0, borderBottom: `1px solid ${L.hairline}`, borderRadius: 0,
      paddingLeft: 0, paddingRight: 0, cursor: 'pointer',
      fontFamily: FONT.sans, fontWeight: on ? 700 : 500, color: on ? L.ink : L.muted,
      lineHeight: 1.25, transition: 'color 140ms ease',
    }}
  >
    {/* Selection mark in ink, matching the chosen year in "By year"; orange belongs to the CTA and the apricot strip only. */}
    <span aria-hidden="true" style={{ width: 7, height: 7, borderRadius: 999, flexShrink: 0, background: on ? L.ink : 'transparent' }} />
    <span className="min-w-0 flex-1">{label}</span>
    <span className="hidden sm:block" style={countStyle}>{count}</span>
  </button>
);

const AtlasDemo: React.FC<DemoProps> = ({ sub, active }) => {
  const reduce = useReducedMotion() === true;
  const mode: 'topic' | 'year' = sub === 'year' ? 'year' : 'topic';
  const [topicIdx, setTopicIdx] = useState(START_IDX);
  const [year, setYear] = useState(ATLAS_YEARS[TOTAL_YEARS - 1]);
  const [interacted, setInteracted] = useState(false);
  const listRef = useRef<HTMLDivElement>(null);

  const topic = ATLAS_TOPICS[topicIdx];
  const topicsThatYear = useMemo(() => ATLAS_TOPICS.filter(t => t.years.includes(year)), [year]);

  // Autoplay: only while this tab is showing, only in topic mode, only until the first real touch.
  const autoplay = active && mode === 'topic' && !interacted && !reduce;
  useEffect(() => {
    if (!autoplay) return;
    const id = window.setInterval(() => setTopicIdx(i => (i + 1) % ATLAS_TOPICS.length), AUTOPLAY_MS);
    return () => window.clearInterval(id);
  }, [autoplay]);

  // Keep the autoplayed row in view inside the list without touching page scroll.
  // The list is position:relative, so a row's offsetTop is measured from the list itself.
  useEffect(() => {
    if (!autoplay) return;
    const list = listRef.current;
    const row = list?.children[topicIdx];
    if (!list || !(row instanceof HTMLElement)) return;
    const top = row.offsetTop;
    const bottom = top + row.offsetHeight;
    if (top < list.scrollTop) list.scrollTo({ top, behavior: 'smooth' });
    else if (bottom > list.scrollTop + list.clientHeight) list.scrollTo({ top: bottom - list.clientHeight, behavior: 'smooth' });
  }, [autoplay, topicIdx]);

  const stop = useCallback(() => setInteracted(true), []);

  const askedCount = topic.years.length;
  const stripLabel = `${topic.label}: ${askedCount} ${T.of} ${TOTAL_YEARS} ${T.yearsAsked} (${topic.years.join(', ')})`;

  return (
    <div
      className="flex h-full w-full flex-col p-4 sm:p-6 lg:p-7"
      style={{ overflowY: 'auto', background: L.paper }}
      onPointerDownCapture={stop}
      onKeyDownCapture={stop}
    >
      <p className="shrink-0" style={promptStyle}>{mode === 'topic' ? T.prompt : T.promptYear}</p>

      {mode === 'topic' ? (
        <div className="mt-3 flex min-h-0 flex-1 flex-col lg:grid lg:grid-cols-12 lg:grid-rows-[minmax(0,1fr)] lg:gap-8">
          <div
            ref={listRef}
            role="group"
            aria-label={T.topicList}
            className="relative grid min-h-0 flex-1 grid-cols-2 content-start gap-x-4 overflow-y-auto lg:col-span-5 lg:grid-cols-1"
          >
            {ATLAS_TOPICS.map((t, i) => (
              <TopicRow key={t.id} label={t.label} count={t.years.length} on={i === topicIdx} onSelect={() => setTopicIdx(i)} />
            ))}
          </div>

          <div className="mt-4 shrink-0 lg:col-span-7 lg:mt-0 lg:self-start">
            <Count n={askedCount} unit={`${T.of} ${TOTAL_YEARS} ${T.yearsAsked}`} reduce={reduce} />
            <p
              aria-hidden={askedCount !== TOTAL_YEARS}
              className="m-0 mt-1"
              style={{
                fontFamily: FONT.serif, fontStyle: 'italic', fontSize: 15, lineHeight: 1.3, color: L.muted,
                visibility: askedCount === TOTAL_YEARS ? 'visible' : 'hidden',
              }}
            >
              {T.everyYear}
            </p>
            <div className="mt-3">
              <Fingerprint years={topic.years} reduce={reduce} label={stripLabel} />
            </div>
          </div>
        </div>
      ) : (
        <div className="mt-3 flex min-h-0 flex-1 flex-col">
          <div className="shrink-0">
            <YearSelector year={year} onChange={setYear} />
          </div>
          <div className="mt-4 flex min-h-0 flex-1 flex-col lg:grid lg:grid-cols-12 lg:grid-rows-[minmax(0,1fr)] lg:gap-8">
            <div className="shrink-0 lg:col-span-5">
              <Count n={topicsThatYear.length} unit={T.topics} reduce={reduce} />
            </div>
            <div
              role="list"
              className="mt-3 grid min-h-0 flex-1 grid-cols-2 content-start gap-x-4 overflow-y-auto lg:col-span-7 lg:mt-0 lg:grid-cols-1"
            >
              {topicsThatYear.map((t, i) => {
                const inner = (
                  <>
                    <span className="min-w-0 flex-1">{t.label}</span>
                    <span className="hidden sm:block" style={countStyle}>{t.years.length}</span>
                  </>
                );
                // The listitem is the outermost element so the list keeps its semantics.
                return reduce ? (
                  <div key={t.id} role="listitem" className={yearRowClass} style={yearRowStyle}>{inner}</div>
                ) : (
                  <MotionDiv
                    key={`${year}-${t.id}`}
                    role="listitem"
                    className={yearRowClass}
                    style={yearRowStyle}
                    initial={{ opacity: 0, y: 4 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.24, delay: i * STAGGER_S, ease: EASE }}
                  >
                    {inner}
                  </MotionDiv>
                );
              })}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default AtlasDemo;
