/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Sit the paper — the last thing on the page, and the one a student can
 * click into: a Frame with the six real first pages the Subjects stack
 * shows, each with the length of its sitting as the cover prints it
 * (fx-j/covers.ts, lifted off the PDFs by scripts/landing/hall-cover.mjs),
 * and one press-in button. Pressing it turns the page into the exam hall
 * (fx-j/ExamHall.tsx). Nothing here moves on its own, so the box works the
 * same under reduced motion and ?static=1; the hall handles its own.
 */

import React, { useCallback, useEffect, useId, useRef, useState } from 'react';
import { Body, Button, Container, Display, Eyebrow, Frame, SectionRule } from '../primitives';
import { FONT, L, SPACE } from '../theme';
import { STACK_PAGE, STACK_PAPERS, type StackPaper } from '../fx-c/papers';
import { HALL_COVERS } from '../fx-j/covers';
import ExamHall, { attribution } from '../fx-j/ExamHall';
import { durationShort, durationWords } from '../fx-j/time';
import '../fx-j/fx-j.css';

const TEXT = {
  eyebrow: 'The exam hall',
  title: 'Sit a real paper, against its real clock.',
  body: 'The page goes quiet, the paper lands on the desk, and the clock counts down the time printed on its cover. Leave whenever you like.',
  frame: 'Sit the paper',
  line: 'Six first pages from the Paper Trail. Each cover prints its own sitting; the clock runs for exactly that long.',
  picker: 'Choose a paper',
  cta: 'Sit this paper',
} as const;

/** The stack's papers that have a lifted cover. */
const PAPERS = STACK_PAPERS.filter(p => HALL_COVERS[p.id]);

/** "English · Higher Level · Paper 1 · 2025". */
const label = (p: StackPaper): string => [p.subject, p.level, p.part, String(p.year)].filter(Boolean).join(' · ');

const fine: React.CSSProperties = { fontFamily: FONT.mono, fontSize: 11, lineHeight: 1.6, color: L.faint, margin: 0 };

const SitThePaper: React.FC = () => {
  const name = useId();
  const [selected, setSelected] = useState(PAPERS[0]?.id ?? '');
  const [open, setOpen] = useState(false);
  const openerRef = useRef<HTMLSpanElement>(null);
  const paper = PAPERS.find(p => p.id === selected) ?? PAPERS[0];
  const cover = paper ? HALL_COVERS[paper.id] : undefined;

  const onClosed = useCallback(() => setOpen(false), []);
  // Focus returns to the button that opened the hall — after the commit that
  // removed the layer, since until then the page is inert and cannot take it.
  const wasOpen = useRef(false);
  useEffect(() => {
    if (wasOpen.current && !open) openerRef.current?.querySelector('button')?.focus();
    wasOpen.current = open;
  }, [open]);

  if (!paper || !cover) return null;

  return (
    <section id="sit" className={SPACE.sectionTight} style={{ position: 'relative', scrollMarginTop: 70 }}>
      <SectionRule />
      <Container>
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 lg:gap-12 items-start">
          <div className="lg:col-span-4 lg:pt-2">
            <Eyebrow>{TEXT.eyebrow}</Eyebrow>
            <Display size="sub" as="h2" className="mt-4" style={{ maxWidth: '18ch' }}>{TEXT.title}</Display>
            <Body className="mt-5" style={{ maxWidth: '40ch' }}>{TEXT.body}</Body>
          </div>

          <div className="lg:col-span-8 min-w-0">
            <Frame title={TEXT.frame} meta={durationWords(cover.minutes)} padded>
              <div className="hallpick__grid">
                <div className="min-w-0">
                  <Body style={{ margin: 0, maxWidth: '48ch' }}>{TEXT.line}</Body>
                  <fieldset className="hallpick mt-5">
                    <legend className="sr-only">{TEXT.picker}</legend>
                    {PAPERS.map(p => {
                      const on = p.id === paper.id;
                      return (
                        <label key={p.id} className="hallpick__row" data-on={on || undefined}>
                          <input type="radio" name={name} value={p.id} checked={on} onChange={() => setSelected(p.id)} className="sr-only" />
                          <span className="hallpick__sq" aria-hidden="true" />
                          <span className="hallpick__label">{label(p)}</span>
                          <span className="hallpick__time">{durationShort(HALL_COVERS[p.id].minutes)}</span>
                        </label>
                      );
                    })}
                  </fieldset>
                  <div className="mt-6 flex flex-wrap items-center gap-4">
                    <span ref={openerRef}>
                      <Button variant="ink" onClick={() => setOpen(true)}>{TEXT.cta}</Button>
                    </span>
                    <span style={fine}>{cover.sitting}</span>
                  </div>
                </div>
                <figure className="hallpick__preview">
                  <img
                    key={paper.id}
                    src={paper.src}
                    alt={`${label(paper)}: the first page of the paper`}
                    width={STACK_PAGE.width}
                    height={STACK_PAGE.height}
                    decoding="async"
                    draggable={false}
                  />
                  <figcaption>{attribution(paper)}</figcaption>
                </figure>
              </div>
            </Frame>
          </div>
        </div>
      </Container>
      {open && <ExamHall paper={paper} cover={cover} onClosed={onClosed} />}
    </section>
  );
};

export default SitThePaper;
