/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The paper stack: real first pages of SEC papers pinned as the reader
 * scrolls, each new one sliding over the last while the ones beneath settle
 * back (scale .96, up 10px, an ink hairline edge and nothing softer). The
 * motion is a CSS scroll-driven animation in fx-c.css — zero JavaScript
 * where the browser has view timelines. Where it does not (Firefox, older
 * Safari) each page settles with a spring the moment the next page has
 * climbed past the middle of the viewport. Reduced motion and ?static=1:
 * the pages simply overlap. Every figure carries a real caption.
 */

import React, { useEffect, useRef, useState } from 'react';
import { useInView } from 'framer-motion';
import { MotionDiv, useReducedMotion } from '../../Motion';
import { STACK_PAGE, STACK_PAPERS, stackCaption, type StackPaper } from './papers';
import './fx-c.css';

const supportsScrollTimeline = (): boolean =>
  typeof CSS !== 'undefined' && typeof CSS.supports === 'function' && CSS.supports('animation-timeline: view()');

const Paper: React.FC<{ paper: StackPaper; index: number; nextRef: React.RefObject<HTMLLIElement | null> | null; settleByScript: boolean; liRef: React.RefObject<HTMLLIElement | null> }> = ({ paper, index, nextRef, settleByScript, liRef }) => {
  // The page after this one is "over" it once its top has climbed above 55% of the viewport.
  const nextArrived = useInView(nextRef ?? liRef, { margin: '0px 0px -45% 0px' as never });
  const settled = settleByScript && nextRef !== null && nextArrived;
  return (
    <li ref={liRef} style={{ '--i': index } as React.CSSProperties}>
      <MotionDiv
        className="fxc-stack__paper"
        initial={false}
        animate={settleByScript ? { y: settled ? -10 : 0, scale: settled ? 0.96 : 1 } : undefined}
        transition={{ type: 'spring', bounce: 0, duration: 0.6 }}
      >
        <figure style={{ margin: 0 }}>
          <img
            src={paper.src}
            alt={`${stackCaption(paper)}: the first page of the paper`}
            width={STACK_PAGE.width}
            height={STACK_PAGE.height}
            loading={index < 2 ? 'eager' : 'lazy'}
            decoding="async"
            draggable={false}
          />
          <figcaption className="fxc-stack__caption">
            <span>{paper.subject} · {paper.level}{paper.part ? ` · ${paper.part}` : ''}</span>
            <b>{paper.year}</b>
          </figcaption>
        </figure>
      </MotionDiv>
    </li>
  );
};

const PaperStack: React.FC = () => {
  const reduce = useReducedMotion();
  const [settleByScript, setSettleByScript] = useState(false);
  useEffect(() => {
    const isStatic = document.documentElement.classList.contains('landing-static');
    setSettleByScript(!reduce && !isStatic && !supportsScrollTimeline());
  }, [reduce]);
  // One ref per page, made once, so each page can watch the one after it.
  const refs = useRef(STACK_PAPERS.map(() => React.createRef<HTMLLIElement>())).current;
  return (
    <ol className="fxc-stack" aria-label="First pages of Leaving Certificate papers in the Paper Trail">
      {STACK_PAPERS.map((p, i) => (
        <Paper
          key={p.id}
          paper={p}
          index={i}
          liRef={refs[i]}
          nextRef={i + 1 < STACK_PAPERS.length ? refs[i + 1] : null}
          settleByScript={settleByScript}
        />
      ))}
    </ol>
  );
};

export default PaperStack;
