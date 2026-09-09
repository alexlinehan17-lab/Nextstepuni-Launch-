/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Chapters — the Editions "chapters of a book" anatomy. A sticky contents
 * rail on the left (a horizontal strip on phones) tracks which of the seven
 * chapters is on screen; on the right each chapter opens with one giant
 * serif word that folds away as the chapter scrolls out (Leonardo's move),
 * then a drop-cap line, the body copy, a link into the playground where a demo
 * exists, and a screenshot frame. Starguy stands on the baseline at the end of
 * the word on chapters I, IV and VII.
 *
 * Effects (components/landing/fx): the flow-field ornament that was hatched
 * behind each heading is gone (Alex, 2026-09-09); the frames of I–III blot
 * into the page as they arrive;
 * Chapter I's frame is the real question with its marking scheme under a
 * lens; the rail numerals carry an orange gauge that fills as each chapter
 * is read, with 'you are here' lettered under the list; and the one circled
 * figure on the page is 2010 in Chapter II.
 *
 * Chapter VII (components/landing/fx-f) carries Points Passport's course
 * search in its frame. Choose a course and the whole chapter rewrites itself
 * around it in place — word, line, body and frame — with a page turn; a
 * button turns it back. Every figure on the rewritten page is the course's
 * own field in components/futureFinderData.ts.
 */

import React, { useEffect, useMemo, useRef, useState } from 'react';
import { MotionDiv, useReducedMotion } from '../../Motion';
import { COPY, type Chapter, type ChapterId, type PlaygroundTabId } from '../copy';
import { CAPTURES } from '../demoData';
import { Reveal, WordRise } from '../motion';
import { StarguySlot, useTravellerLive, type SlotId } from '../starguy/Traveller';
import { Body, Button, Container, DISPLAY, Display, DropLine, Eyebrow, Frame, Rule, Starguy } from '../primitives';
import { FONT, L, SPACE } from '../theme';
import { openDemo } from './Playground';
import { LiveGlimpse, hasGlimpse } from '../glass/Glimpse';
import { Note } from '../fx/Note';
import { Spotlight } from '../fx/Spotlight';
import { Mark, markPhrase } from '../fx/marks';
import { isStatic } from '../fx/env';
import { CourseFrame } from '../fx-f/CourseFrame';
import { announceTurn, courseBody, courseLine, type CAOCourse } from '../fx-f/courses';
import { useFitTitle, usePageTurn } from '../fx-f/pageTurn';
import '../fx-f/fx-f.css';

const CHAPTERS = COPY.chapters.items;
/** Chapters whose giant word Starguy stands at the end of. */
const HANGS: ReadonlySet<ChapterId> = new Set<ChapterId>(['markbank', 'planner', 'futurefinder']);
/** Chapters with a matching playground demo (papertrail and lab have none). Ids map 1:1. */
const DEMO_OF: Partial<Record<ChapterId, PlaygroundTabId>> = { markbank: 'markbank', papertrail: 'papertrail', atlas: 'atlas', planner: 'planner', launchpad: 'reflex', futurefinder: 'futurefinder' };
/** The frames that blot into the page (the rest simply rise). One blot each; the hero star uses the third. */
const BLOTS: Partial<Record<ChapterId, 1 | 2 | 3>> = { markbank: 1, papertrail: 2, atlas: 3 };
/** The page's one orange circle: a figure in a chapter's body copy. */
const CIRCLED: { chapter: ChapterId; paragraph: number; phrase: string } = { chapter: 'papertrail', paragraph: 0, phrase: '2010' };
/** demoData's frame table predates chapter VII; read it as the partial map it is. */
const FRAMES: Partial<Record<ChapterId, string | null>> = CAPTURES;

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
  // While the traveller is live this box is only his target: it moves at once and he springs to it.
  const live = useTravellerLive();
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
      animate={reduce || live ? { top } : { top, y: [0, -10, 0] }}
      transition={live ? { top: { duration: 0 } } : { top: { type: 'spring', stiffness: 260, damping: 26 }, y: { duration: 0.45, ease: 'easeOut' } }}
      style={{ position: 'absolute', left: -46, width: 34, pointerEvents: 'none' }}
    >
      <StarguySlot id="rail"><Starguy size={0} style={{ width: 34, height: 'auto' }} /></StarguySlot>
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
      {CHAPTERS.map((ch, i) => {
        const on = ch.id === active;
        return (
          <li key={ch.id} style={{ borderBottom: `1px solid ${L.hairline}` }}>
            <a
              href={anchor(ch.id)}
              aria-current={on ? 'true' : undefined}
              className="landing-tab flex items-baseline gap-3"
              style={{ padding: '10px 2px', textDecoration: 'none', color: on ? L.ink : L.muted, transition: 'color 120ms ease' }}
            >
              <span aria-hidden="true" style={{ position: 'relative', fontFamily: FONT.serif, fontWeight: 600, fontSize: 13, width: 22, flexShrink: 0, color: on ? L.orangeText : L.faint, transition: 'color 120ms ease' }}>
                {ch.numeral}
                {/* The gauge: fills on this chapter's own view timeline (fx.css, .fx-tick; fx-f.css adds the seventh). */}
                <span className={`fx-tick fx-tick-${i + 1}`} />
              </span>
              <span style={{ fontFamily: FONT.sans, fontSize: 14, fontWeight: on ? 700 : 500, color: 'inherit', lineHeight: 1.3 }}>{ch.railLabel}</span>
            </a>
          </li>
        );
      })}
    </ol>
    {/* Written once the rail is on screen: the rail is sticky, so a scroll timeline would never move here. */}
    <Note id="here" mode="timed" className="mt-4" style={{ width: 172 }} />
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

/** Chapter I: the real question with the marking scheme under the lens. Otherwise a supplied screenshot, else a live glimpse of the real surface, else a labelled placeholder. */
const Capture: React.FC<{ chapter: Chapter }> = ({ chapter }) => {
  const src = FRAMES[chapter.id];
  return (
    <Frame title={chapter.frameLabel} meta={chapter.numeral}>
      {chapter.id === 'markbank' ? <Spotlight /> : src
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
  const frameRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);
  const reduce = useReducedMotion();
  const flip = index % 2 === 1;
  const titleId = `chapter-${chapter.id}-title`;
  const blot = BLOTS[chapter.id];
  const frameCol = flip ? 'lg:col-span-7 lg:order-1' : 'lg:col-span-7';
  const turns = chapter.id === 'futurefinder';

  // Chapter VII: the course the chapter is written around, if any (fx-f). The
  // turn copies the page BEFORE the state changes, then wipes the copy away
  // once the rewrite has rendered. Instant under reduced motion or ?static=1.
  const [course, setCourse] = useState<CAOCourse | null>(null);
  const [said, setSaid] = useState('');
  const turn = usePageTurn(articleRef, course?.code ?? '', reduce || isStatic());
  useFitTitle(articleRef, titleId, course?.title ?? chapter.word, course !== null, String(DISPLAY.chapter.fontSize));
  const choose = (c: CAOCourse) => {
    if (c.code === course?.code) return;
    turn.snapshot(false);
    setCourse(c);
    setSaid(announceTurn(c));
  };
  const back = () => {
    turn.snapshot(true);
    setCourse(null);
    setSaid(COPY.futurefinder.restored);
    inputRef.current?.focus({ preventScroll: true });
  };

  const word = course ? course.title : chapter.word;
  const line = course ? courseLine(course) : chapter.line;
  const body = course ? courseBody(course) : chapter.body;
  const frameLabel = course ? `${course.code} · ${course.institution}` : chapter.frameLabel;
  const demo: PlaygroundTabId | undefined = course ? 'passport' : DEMO_OF[chapter.id];
  const tryIt = course ? COPY.futurefinder.tryPassport : COPY.chapters.tryIt;

  const capture = turns
    ? <Frame title={frameLabel} meta={chapter.numeral}><CourseFrame course={course} onChoose={choose} inputRef={inputRef} /></Frame>
    : <Capture chapter={chapter} />;

  return (
    <article
      ref={articleRef}
      id={`chapter-${chapter.id}`}
      aria-labelledby={titleId}
      className={`scroll-mt-[124px] lg:scroll-mt-[96px] fx-chapter-${index + 1}${turns ? ' fxf-leaf' : ''}`}
    >
      <div className="fx-head">
        <div className="fx-head-text">
          <Eyebrow numeral={chapter.numeral}>{chapter.railLabel}</Eyebrow>
          <WordRise className="mt-4">
            {/* The word row clips sideways so Starguy, hung past the word's end, never widens the page. */}
            <Display size="chapter" as="h3" id={titleId} style={{ overflowWrap: 'anywhere', overflowX: 'clip' }}>
              <span style={{ position: 'relative', display: 'inline-block', maxWidth: '100%' }}>
                {word}
                {HANGS.has(chapter.id) && (
                  /* Inline, so a word that wraps ("Planner & Study") still ends with him on its LAST line. A fitted course title keeps him at least 56px. */
                  <span
                    aria-hidden="true"
                    className="landing-starguy-lg"
                    style={{ display: 'inline-block', verticalAlign: 'baseline', marginLeft: '0.06em', marginBottom: '0.04em', width: course ? 'max(0.55em, 56px)' : '0.55em', lineHeight: 0 }}
                  >
                    <StarguySlot id={`word-${chapter.id}` as SlotId}><Starguy size={0} style={{ width: '100%', height: 'auto' }} /></StarguySlot>
                  </span>
                )}
              </span>
            </Display>
          </WordRise>
        </div>
      </div>
      <div className="mt-8 md:mt-10 grid grid-cols-1 lg:grid-cols-12 gap-8 lg:gap-12 items-start">
        <div className={flip ? 'lg:col-span-5 lg:order-2' : 'lg:col-span-5'}>
          <DropLine>{line}</DropLine>
          <div className="mt-6 flex flex-col gap-4">
            {body.map((p, pi) => (
              <Body key={p} style={{ fontSize: 16 }}>
                {chapter.id === CIRCLED.chapter && pi === CIRCLED.paragraph
                  ? markPhrase(p, CIRCLED.phrase, node => <Mark type="circle" color={L.orange} padding={[2, 5]} strokeWidth={1.5} delay={250}>{node}</Mark>)
                  : p}
              </Body>
            ))}
          </div>
          {(demo || course) && (
            <div className="mt-6 fxf-actions">
              {course && <Button variant="secondary" onClick={back}>{COPY.futurefinder.back}</Button>}
              {demo && <Button variant="ghost" onClick={() => openDemo(demo, undefined, frameRef.current)}>{tryIt}</Button>}
            </div>
          )}
          {turns && <p className="fxf-sr" role="status" aria-live="polite">{said}</p>}
        </div>
        {/* I–III soak into the page (the blot is this chapter's one motion); the rest rise. */}
        {blot ? (
          <div className={frameCol}>
            <div ref={frameRef} className={`fx-blot fx-blot--scroll fx-blot-${blot}`}>{capture}</div>
          </div>
        ) : (
          <Reveal className={frameCol}>
            <div ref={frameRef}>{capture}</div>
          </Reveal>
        )}
      </div>
    </article>
  );
};

const Chapters: React.FC = () => {
  const [active, setActive] = useState<ChapterId>(CHAPTERS[0].id);
  // One ref per article, made once: the observer and each chapter share it.
  const refs = useMemo(() => CHAPTERS.map(() => React.createRef<HTMLElement>()), []);

  // One observer over the seven articles. The band is the middle 10% of the
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

        {/* fx-scope: the seven chapters' view timelines are scoped here so the sticky rail can read them. */}
        <div className="lg:grid lg:grid-cols-12 lg:gap-x-8 fx-scope">
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
