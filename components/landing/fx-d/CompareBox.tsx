/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The question-vs-scheme compare box — one framed document. Drag the
 * hairline divider and the real SEC exam question (left) gives way to the
 * marking scheme's row for the same part (right), with the marks column that
 * scores it. Both crops are the SEC's own pages — Economics 2024, Higher
 * Level, Question 1, from the paper and its published scheme — exported at
 * the same pixel size so the infographic, the (a) prompt and the workings box
 * sit on top of each other. A 1px ink handle with a 10px orange grip is the
 * only chrome; the handle is a keyboard slider (arrow keys) with a 44px hit
 * area. Moved unchanged from sections/Compare.tsx into the "Answer like an
 * examiner" section, where it is the first of four boxes.
 */

import React from 'react';
import { ReactCompareSlider } from 'react-compare-slider';
import { Frame } from '../primitives';
import { FONT, L } from '../theme';
import '../fx-c/fx-c.css';

/** The pair. Same crop box on both pages (540 × 485 pt at 2.2×), so they overlay. */
const PAIR = {
  paper: '/assets/landing/compare/economics-2024-hl-q1-paper.webp',
  scheme: '/assets/landing/compare/economics-2024-hl-q1-scheme.webp',
  width: 1188,
  height: 1067,
  title: 'Economics · Higher Level · 2024 · Question 1',
  paperAlt: 'Economics 2024, Higher Level, Question 1: the CSO balance of payments infographic, part (a) asking for the current account balance, and the empty workings and answer boxes.',
  schemeAlt: 'The marking scheme for the same question: the possible responses column with the workings (€76bn + €91bn = €167bn, €38bn + €83bn = €121bn, €46bn surplus) and the marks column awarding 6 marks for part (a) and 6 for part (b).',
} as const;

/** Copy for this box. The line is the client's; the rest states what the two crops are. */
export const COMPARE_TEXT = {
  eyebrow: 'Question and marking scheme',
  line: 'It’s never been easier to mark like an examiner.',
  body: 'The 2024 Higher Level Economics paper, Question 1, and the marking scheme the SEC published for it: the possible responses beside the question, and the marks column that scores each part.',
  caption: 'Drag — the scheme is on the right',
  left: 'The question',
  right: 'The marking scheme',
} as const;

const InkHandle: React.FC = () => (
  <div className="fxc-handle">
    <span className="fxc-handle__grip" aria-hidden="true" />
  </div>
);

const Side: React.FC<{ src: string; alt: string; tag: string; edge: 'left' | 'right' }> = ({ src, alt, tag, edge }) => (
  <div style={{ position: 'relative' }}>
    <img src={src} alt={alt} width={PAIR.width} height={PAIR.height} loading="lazy" decoding="async" draggable={false} />
    <span className="fxc-compare__tag" style={edge === 'left' ? { left: 10 } : { right: 10 }} aria-hidden="true">{tag}</span>
  </div>
);

/** The framed compare document, exactly as it stood in the Compare section. */
export const CompareBox: React.FC = () => (
  <Frame title={PAIR.title} meta="Paper Trail">
    <div className="fxc-compare">
      <ReactCompareSlider
        itemOne={<Side src={PAIR.paper} alt={PAIR.paperAlt} tag={COMPARE_TEXT.left} edge="left" />}
        itemTwo={<Side src={PAIR.scheme} alt={PAIR.schemeAlt} tag={COMPARE_TEXT.right} edge="right" />}
        handle={<InkHandle />}
        defaultPosition={55}
        keyboardIncrement="5%"
        onlyHandleDraggable
        style={{ width: '100%', aspectRatio: `${PAIR.width} / ${PAIR.height}` }}
      />
    </div>
    <div
      className="flex items-center justify-between gap-4"
      style={{ padding: '10px 14px', borderTop: `1px solid ${L.hairline}`, fontFamily: FONT.mono, fontSize: 11, letterSpacing: '0.14em', textTransform: 'uppercase', color: L.faint }}
    >
      <span>{COMPARE_TEXT.caption}</span>
      <span aria-hidden="true" style={{ display: 'inline-block', width: 10, height: 10, background: L.orange, flexShrink: 0 }} />
    </div>
  </Frame>
);

export default CompareBox;
