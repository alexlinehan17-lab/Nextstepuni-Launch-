/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * CollapsibleQuestionCard — pinned question reference at the top of post-
 * Question stages (Predict, Debrief). Default expanded; chevron toggles.
 * Lets students re-read the question without leaving the stage they're on.
 *
 * Renders the question text via AnnotatedText (passive visual annotations)
 * plus a metadata strip (year/paper/section/level/marks-pill/command-words).
 */

import React, { useState } from 'react';
import { type ExamQuestion } from '../../types/examStrategiser';
import AnnotatedText from './AnnotatedText';

const TEAL = '#2A7D6F';

interface Props {
  question: ExamQuestion;
  /** Default open. Pass `false` if the parent prefers collapsed-by-default. */
  defaultOpen?: boolean;
  /** Whether to render passive visual annotations on the question text
   *  (underlines, wavy lines, inline marks-pills). Default `false` so the
   *  card stays clean on Predict; the Debrief stage opts in to show
   *  annotations as part of the reveal. */
  showAnnotations?: boolean;
}

const CollapsibleQuestionCard: React.FC<Props> = ({ question, defaultOpen = true, showAnnotations = false }) => {
  const [open, setOpen] = useState(defaultOpen);

  const marksToMinutesContext =
    question.totalPaperMarks && question.totalPaperMinutes
      ? {
          totalPaperMarks: question.totalPaperMarks,
          totalPaperMinutes: question.totalPaperMinutes,
          questionMarks: question.marks,
        }
      : undefined;

  const minutesPill = marksToMinutesContext
    ? `${question.marks} marks · ${Math.round(
        (question.marks / marksToMinutesContext.totalPaperMarks) *
          marksToMinutesContext.totalPaperMinutes,
      )} mins`
    : `${question.marks} marks`;

  return (
    <section
      className="rounded-2xl"
      style={{
        backgroundColor: '#FFFFFF',
        border: '1px solid #EDEBE8',
        marginBottom: 24,
      }}
    >
      <header
        className="flex items-center justify-between gap-3"
        style={{ padding: '14px 18px', cursor: 'pointer' }}
        onClick={() => setOpen(o => !o)}
        role="button"
        aria-expanded={open}
      >
        <div className="flex items-baseline gap-2 min-w-0 flex-1">
          <p className="font-sans" style={{ fontSize: 10, fontWeight: 700, textTransform: 'uppercase', letterSpacing: 0.6, color: '#A8A29E' }}>
            Question
          </p>
          <span style={{ color: '#E5E3DF' }}>·</span>
          <span className="font-sans truncate" style={{ fontSize: 12, color: '#78716C' }}>
            {question.year}
            {question.paper ? ` · ${question.paper}` : ''}
            {question.questionNumber ? ` · Q${question.questionNumber}` : ''}
          </span>
        </div>
        <div className="flex items-center gap-2 shrink-0">
          <span
            className="font-sans"
            style={{
              fontSize: 11,
              fontWeight: 700,
              color: TEAL,
              backgroundColor: '#FAF7F4',
              border: `1px solid ${TEAL}33`,
              borderRadius: 999,
              padding: '2px 9px',
              whiteSpace: 'nowrap',
            }}
          >
            {minutesPill}
          </span>
          <Chevron open={open} />
        </div>
      </header>

      {open && (
        <div style={{ padding: '4px 22px 22px 22px' }}>
          {question.section && (
            <p className="font-sans" style={{ fontSize: 11, color: '#A8A29E', marginBottom: 10 }}>
              {question.section}
              {question.level ? ` · ${question.level}` : ''}
            </p>
          )}
          <AnnotatedText
            parts={question.questionText}
            mode={showAnnotations ? 'annotated' : 'raw'}
            marksToMinutesContext={marksToMinutesContext}
            interactive={showAnnotations}
          />
          {question.commandWords.length > 0 && (
            <div className="mt-4 flex items-baseline gap-2 flex-wrap">
              <p className="font-sans" style={{ fontSize: 10, fontWeight: 700, textTransform: 'uppercase', letterSpacing: 0.6, color: '#A8A29E' }}>
                Command words
              </p>
              <p className="font-sans" style={{ fontSize: 12, color: '#78716C' }}>
                {question.commandWords.join(', ')}
              </p>
            </div>
          )}
        </div>
      )}
    </section>
  );
};

const Chevron: React.FC<{ open: boolean }> = ({ open }) => (
  <svg
    width="12"
    height="12"
    viewBox="0 0 12 12"
    fill="none"
    aria-hidden
    style={{ color: '#78716C', transform: open ? 'rotate(0deg)' : 'rotate(-90deg)', transition: 'transform 200ms ease' }}
  >
    <path d="M3 4.5L6 7.5L9 4.5" stroke="currentColor" strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round" />
  </svg>
);

export default CollapsibleQuestionCard;
