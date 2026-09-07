/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Chapters — the Editions "chapters of a book" anatomy. A sticky contents
 * rail on the left (a horizontal strip on phones) tracks which of the six
 * chapters is on screen; on the right each chapter opens with one giant
 * serif word that folds away as the chapter scrolls out (Leonardo's move),
 * then a drop-cap line, the body copy, a link into the playground where a demo
 * exists, and a screenshot frame. Starguy stands on the baseline at the end of
 * the word on chapters I and IV.
 */

import React, { useEffect, useMemo, useRef, useState } from 'react';
import { MotionDiv, useReducedMotion } from '../../Motion';
import { COPY, type Chapter, type ChapterId, type PlaygroundTabId } from '../copy';
import { CAPTURES } from '../demoData';
import { CollapseWord, LetterBuild, Reveal } from '../motion';
import { Body, Button, Container, Display, DropLine, Eyebrow, Frame, Rule, Starguy } from '../primitives';
import { FONT, L, SPACE } from '../theme';
import { openDemo } from './Playground';
import { LiveGlimpse, hasGlimpse } from '../glass/Glimpse';

const CHAPTERS = COPY.chapters.items;
/** Chapters whose giant word Starguy stands at the end of. */
const HANGS: ReadonlySet<ChapterId> = new Set<ChapterId>(['markbank', 'planner']);
/** Chapters with a matching playground demo (papertrail and lab have none). Ids map 1:1. */
const DEMO_OF: Partial<Record<ChapterId, PlaygroundTabId>> = { markbank: 'markbank', papertrail: 'papertrail', atlas: 'atlas', planner: 'planner', launchpad: 'reflex' };

const anchor = (id: ChapterId): string => `#chapter-${id}`;

/** The contents-page heading: eyebrow over a serif intro line. */
const RailHeading: React.FC<{ className?: string }> = ({ className = '' }) => (
  <div className={className}>
    <Eyebrow>{COPY.chapters.eyebrow}</Eyebrow>
    <h2 className="mt-3" style={{ fontFamily: FONT.serif, fontWeight: 600, fontSize: 20, lineHeight: 1.3, letterSpacing: '-0.01em', color: L.ink, margin: 0, maxWidth: '22ch' }}>
      {COPY.chapters.intro}
    </h2>
  </div>
);

/** Starguy walks the rail: he stands beside whichever chapter is on screen and hops to the next as it arrives. */
const StarguyWalker: React.FC<{ active: ChapterId; listRef: React.RefObject<HTMLOListElement | null> }> = ({ active, listRef }) => {
  const reduce = useReducedMotion();
  const [top, setTop] = useState(0);
  useEffect(() => {
    const list = listRef.current;
    if (!list) return;
    const row = list.querySelector<HTMLElement>('[aria-current="true"]');
    if (!row) return;
    const lr = list.getBoundingClientRect(); const rr = row.getBoundingClientRect();
    setTop(rr.top - lr.top + rr.height / 2 - 20);
  }, [active, listRef]);
  return (
    <MotionDiv
      aria-hidden="true"
      className="hidden lg:block"
      initial={false}
      animate={reduce ? { top } : { top, y: [0, -10, 0] }}
      transition={{ top: { type: 'spring', stiffness: 260, damping: 26 }, y: { duration: 0.45, ease: 'easeOut' } }}
      style={{ position: 'absolute', left: -46, width: 34, pointerEvents: 'none' }}
    >
      <Starguy size={0} style={{ width: 34, height: 'auto' }} />
    </MotionDiv>
  );
};

/** Desktop rail: a vertical table of contents. */
const Rail: React.FC<{ active: ChapterId }> = ({ active }) => {
  const listRef = useRef<HTMLOListElement>(null);
  return (
  <nav aria-label={COPY.chapters.eyebrow} style={{ position: 'relative' }}>
    <StarguyWalker active={active} listRef={listRef} />
    <ol ref={listRef} className="flex flex-col" style={{ listStyle: 'none', margin: 0, padding: 0, borderTop: `1px solid ${L.hairline}` }}>
      {CHAPTERS.map(ch => {
        const on = ch.id === active;
        return (
          <li key={ch.id} style={{ borderBottom: `1px solid ${L.hairline}` }}>
            <a
              href={anchor(ch.id)}
              aria-current={on ? 'true' : undefined}
              className="landing-tab flex items-baseline gap-3"
              style={{ padding: '10px 2px', textDecoration: 'none', color: on ? L.ink : L.muted, transition: 'color 120ms ease' }}
            >
              <span aria-hidden="true" style={{ fontFamily: FONT.serif, fontWeight: 600, fontSize: 13, width: 22, flexShrink: 0, color: on ? L.orangeText : L.faint, transition: 'color 120ms ease' }}>{ch.numeral}</span>
              <span style={{ fontFamily: FONT.sans, fontSize: 14, fontWeight: on ? 700 : 500, color: 'inherit', lineHeight: 1.3 }}>{ch.railLabel}</span>
            </a>
          </li>
        );
      })}
    </ol>
  </nav>
  );
};

/** Phone rail: a sticky, horizontally scrolling strip under the nav. */
const Strip: React.FC<{ active: ChapterId }> = ({ active }) => {
  const reduce = useReducedMotion();
  const stripRef = useRef<HTMLDivElement>(null);

  // Keep the active item in view as the reader scrolls down the chapters.
  useEffect(() => {
    const strip = stripRef.current;
    // The strip is display:none on lg, so there is nothing to centre there.
    if (!strip || strip.clientWidth === 0) return;
    const item = strip.querySelector<HTMLElement>('[aria-current="true"]');
    if (!item) return;
    const left = item.offsetLeft - (strip.clientWidth - item.offsetWidth) / 2;
    strip.scrollTo({ left: Math.max(0, left), behavior: reduce ? 'auto' : 'smooth' });
  }, [active, reduce]);

  return (
    <nav
      aria-label={COPY.chapters.eyebrow}
      className="lg:hidden sticky -mx-5 sm:-mx-8"
      style={{ top: 68, zIndex: 40, background: L.paper, borderBottom: `1px solid ${L.hairline}` }}
    >
      <div ref={stripRef} className="landing-strip flex gap-1 overflow-x-auto px-5 sm:px-8" style={{ position: 'relative' }}>
        {CHAPTERS.map(ch => {
          const on = ch.id === active;
          return (
            <a
              key={ch.id}
              href={anchor(ch.id)}
              aria-current={on ? 'true' : undefined}
              className="landing-tab shrink-0 flex items-baseline gap-2 whitespace-nowrap"
              style={{
                // No -1px margin: the scroll div clips at its padding box, which would cut the underline to 1px and add 1px of vertical scroll.
                padding: '13px 10px', textDecoration: 'none',
                color: on ? L.ink : L.muted,
                borderBottom: `2px solid ${on ? L.ink : 'transparent'}`,
                transition: 'color 120ms ease, border-color 120ms ease',
              }}
            >
              <span aria-hidden="true" style={{ fontFamily: FONT.serif, fontWeight: 600, fontSize: 13, color: on ? L.orangeText : L.faint, transition: 'color 120ms ease' }}>{ch.numeral}</span>
              <span style={{ fontFamily: FONT.sans, fontSize: 14, fontWeight: on ? 700 : 500, color: 'inherit', lineHeight: 1 }}>{ch.railLabel}</span>
            </a>
          );
        })}
      </div>
    </nav>
  );
};

/** A supplied screenshot, else a live glimpse of the real surface, else a labelled placeholder. */
const Capture: React.FC<{ chapter: Chapter }> = ({ chapter }) => {
  const src = CAPTURES[chapter.id];
  return (
    <Frame title={chapter.frameLabel} meta={chapter.numeral}>
      {src
        ? <img src={src} alt={chapter.frameLabel} loading="lazy" style={{ display: 'block', width: '100%', height: 'auto' }} />
        : hasGlimpse(chapter.id) ? <LiveGlimpse id={chapter.id} /> : (
          <div
            role="img"
            aria-label={COPY.chapters.placeholder}
            style={{
              aspectRatio: '16 / 10', display: 'flex', alignItems: 'center', justifyContent: 'center',
              fontFamily: FONT.mono, fontSize: 11, letterSpacing: '0.14em', textTransform: 'uppercase', color: L.faint,
              backgroundImage: `linear-gradient(${L.hairline} 1px, transparent 1px), linear-gradient(90deg, ${L.hairline} 1px, transparent 1px)`,
              backgroundSize: '24px 24px',
            }}
          >
            {COPY.chapters.placeholder}
          </div>
        )}
    </Frame>
  );
};

/** One chapter: eyebrow, the folding word, then the alternating text / frame row. */
const ChapterBlock: React.FC<{ chapter: Chapter; index: number; articleRef: React.RefObject<HTMLElement | null> }> = ({ chapter, index, articleRef }) => {
  const flip = index % 2 === 1;
  const titleId = `chapter-${chapter.id}-title`;
  const demo = DEMO_OF[chapter.id];
  return (
    <article
      ref={articleRef}
      id={`chapter-${chapter.id}`}
      aria-labelledby={titleId}
      className="scroll-mt-[124px] lg:scroll-mt-[96px]"
    >
      <Eyebrow numeral={chapter.numeral}>{chapter.railLabel}</Eyebrow>
      <CollapseWord className="mt-4">
        {/* The word row clips sideways so Starguy, hung past the word's end, never widens the page. */}
        <Display size="chapter" as="h3" id={titleId} style={{ overflowWrap: 'anywhere', overflowX: 'clip' }}>
          <span style={{ position: 'relative', display: 'inline-block', maxWidth: '100%' }}>
            <LetterBuild text={chapter.word} />
            {HANGS.has(chapter.id) && (
              <span
                aria-hidden="true"
                className="landing-starguy-lg"
                style={{ position: 'absolute', left: 'calc(100% + 0.06em)', bottom: '0.04em', width: '0.55em', lineHeight: 0 }}
              >
                <Starguy size={0} style={{ width: '100%', height: 'auto' }} />
              </span>
            )}
          </span>
        </Display>
      </CollapseWord>
      <div className="mt-8 md:mt-10 grid grid-cols-1 lg:grid-cols-12 gap-8 lg:gap-12 items-start">
        <div className={flip ? 'lg:col-span-5 lg:order-2' : 'lg:col-span-5'}>
          <DropLine>{chapter.line}</DropLine>
          <div className="mt-6 flex flex-col gap-4">
            {chapter.body.map(p => <Body key={p} style={{ fontSize: 16 }}>{p}</Body>)}
          </div>
          {demo && (
            <div className="mt-6">
              <Button variant="ghost" onClick={() => openDemo(demo)}>{COPY.chapters.tryIt}</Button>
            </div>
          )}
        </div>
        <Reveal className={flip ? 'lg:col-span-7 lg:order-1' : 'lg:col-span-7'}>
          <Capture chapter={chapter} />
        </Reveal>
      </div>
    </article>
  );
};

const Chapters: React.FC = () => {
  const [active, setActive] = useState<ChapterId>(CHAPTERS[0].id);
  // One ref per article, made once: the observer and each CollapseWord share it.
  const refs = useMemo(() => CHAPTERS.map(() => React.createRef<HTMLElement>()), []);

  // One observer over the six articles. The band is the middle 10% of the
  // viewport, so a chapter becomes current as its word crosses the fold.
  useEffect(() => {
    if (typeof IntersectionObserver === 'undefined') return;
    const visible = new Set<ChapterId>();
    const io = new IntersectionObserver(entries => {
      for (const entry of entries) {
        const id = entry.target.id.replace('chapter-', '') as ChapterId;
        if (entry.isIntersecting) visible.add(id); else visible.delete(id);
      }
      const first = CHAPTERS.find(ch => visible.has(ch.id));
      if (first) setActive(first.id);
    }, { rootMargin: '-40% 0px -50% 0px' });
    refs.forEach(r => { if (r.current) io.observe(r.current); });
    return () => io.disconnect();
  }, [refs]);

  return (
    <section id="chapters" className={SPACE.section} style={{ scrollMarginTop: 70 }}>
      <Container>
        {/* Phone: heading, then the sticky strip. Both stay in the Container's flow so the strip sticks through every chapter. */}
        <RailHeading className="lg:hidden mb-6" />
        <Strip active={active} />

        <div className="lg:grid lg:grid-cols-12 lg:gap-x-8">
          <div className="hidden lg:block lg:col-span-3">
            <div className="sticky" style={{ top: 92 }}>
              <Rail active={active} />
              <RailHeading className="mt-10" />
            </div>
          </div>

          <div className="mt-12 lg:mt-0 lg:col-span-9">
            {CHAPTERS.map((ch, i) => (
              <React.Fragment key={ch.id}>
                {i > 0 && <Rule strong className="mt-24 md:mt-32 mb-16 md:mb-20" />}
                <ChapterBlock chapter={ch} index={i} articleRef={refs[i]} />
              </React.Fragment>
            ))}
          </div>
        </div>
      </Container>
    </section>
  );
};

export default Chapters;
