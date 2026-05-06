/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * AnnotatedText — renders a QuestionPart[] with optional inline annotations.
 * Three render modes:
 *   - mode="raw": annotations are stripped, plain text only
 *   - mode="annotated", interactive=false: passive visual cues only
 *     (underlines, wavy lines, marks pill) — no hover/click behaviour
 *   - mode="annotated", interactive=true: passive cues + hover-to-reveal
 *     and click-to-pin tooltip showing the annotation's note
 *
 * Interactive mode is opted-in by the Debrief stage, where annotations are
 * part of the examiner reveal. Question and Predict stages stay clean.
 */

import React, { useState } from 'react';
import { type QuestionPart, type AnnotationType } from '../../types/examStrategiser';

const TEAL = '#2A7D6F';

interface AnnotatedTextProps {
  parts: QuestionPart[];
  mode: 'raw' | 'annotated';
  /** marks-to-minutes computation context. Only used by 'marks-allocation' annotations. */
  marksToMinutesContext?: { totalPaperMarks: number; totalPaperMinutes: number; questionMarks: number };
  /** When true and mode='annotated', annotated spans become interactive —
   *  hover reveals the note transiently; click pins it (click again to
   *  unpin). When false, annotations render as passive visual cues only. */
  interactive?: boolean;
}

const annotationStyle = (type: AnnotationType, interactive: boolean): React.CSSProperties => {
  const base = interactive ? { cursor: 'help' as const } : {};
  switch (type) {
    case 'command':
      return { ...base, textDecoration: `underline solid ${TEAL}`, textDecorationThickness: 2, textUnderlineOffset: 4 };
    case 'keyword':
      return { ...base, textDecoration: `underline dotted ${TEAL}`, textDecorationThickness: 2, textUnderlineOffset: 4 };
    case 'trap':
      return { ...base, textDecoration: `underline wavy ${TEAL}`, textDecorationThickness: 1.5, textDecorationSkipInk: 'auto', textUnderlineOffset: 4, opacity: 0.95 };
    case 'marks-allocation':
      // Pill is rendered separately; segment span gets neutral style.
      return base;
  }
};

const MarksPill: React.FC<{ label: string; interactive: boolean }> = ({ label, interactive }) => (
  <span
    className="inline-flex items-center gap-1 align-middle"
    style={{
      backgroundColor: '#FAF7F4',
      border: `1px solid ${TEAL}33`,
      color: TEAL,
      borderRadius: 999,
      padding: '2px 10px',
      fontSize: 11,
      fontWeight: 700,
      letterSpacing: 0.2,
      cursor: interactive ? 'help' : 'default',
    }}
  >
    {label}
  </span>
);

/** Per-segment id derived from its position in the parts tree. Used to
 *  identify which annotation is currently revealed/pinned. */
const segmentId = (partIdx: number, segIdx: number) => `ann-${partIdx}-${segIdx}`;

const AnnotatedText: React.FC<AnnotatedTextProps> = ({ parts, mode, marksToMinutesContext, interactive = false }) => {
  // Two-state interaction model:
  //   hoverId  — transient, set on mouseenter, cleared on mouseleave
  //   pinnedId — sticky, set on click, cleared on click of same span
  // Tooltip shows when either matches the current segment.
  const [hoverId, setHoverId] = useState<string | null>(null);
  const [pinnedId, setPinnedId] = useState<string | null>(null);

  const revealId = pinnedId ?? hoverId;

  const renderSegment = (seg: QuestionPart['content'][number], partIdx: number, segIdx: number) => {
    const text = seg.text;
    if (mode === 'raw' || !seg.annotation) {
      return <span key={segIdx}>{text}</span>;
    }
    const id = segmentId(partIdx, segIdx);
    const ann = seg.annotation;
    const isOpen = interactive && revealId === id;

    const interactiveHandlers = interactive
      ? {
          onMouseEnter: () => setHoverId(id),
          onMouseLeave: () => setHoverId(null),
          onClick: (e: React.MouseEvent) => {
            e.stopPropagation();
            setPinnedId(prev => (prev === id ? null : id));
          },
        }
      : {};

    if (ann.type === 'marks-allocation') {
      // Question-level marker like "(20)" → computed pill from question-wide
      // marks/minutes. Otherwise (e.g. subpart label "(a)") → use the note.
      const isQuestionLevelMarker = /^\s*\(\d+\)\s*$/.test(text);
      let pillLabel: string;
      if (isQuestionLevelMarker && marksToMinutesContext) {
        const { totalPaperMarks, totalPaperMinutes, questionMarks } = marksToMinutesContext;
        const mins = totalPaperMarks > 0 ? Math.round((questionMarks / totalPaperMarks) * totalPaperMinutes) : 0;
        pillLabel = mins > 0 ? `${questionMarks} marks · ${mins} mins` : ann.note;
      } else {
        pillLabel = ann.note;
      }
      // Show tooltip for marks-allocation only when the pill label differs
      // from the note (i.e. the pill text doesn't already convey the note).
      const showTooltip = isOpen && pillLabel !== ann.note;
      return (
        <span
          key={segIdx}
          id={id}
          data-annotation-id={id}
          {...interactiveHandlers}
          style={{ position: 'relative', display: 'inline-block' }}
        >
          <MarksPill label={pillLabel} interactive={interactive} />
          {showTooltip && <AnnotationTooltip note={ann.note} />}
        </span>
      );
    }

    return (
      <span
        key={segIdx}
        id={id}
        data-annotation-id={id}
        {...interactiveHandlers}
        style={{ ...annotationStyle(ann.type, interactive), position: 'relative' }}
      >
        {text}
        {isOpen && <AnnotationTooltip note={ann.note} />}
      </span>
    );
  };

  // Click anywhere outside an annotated span clears the pin. Wrapping the
  // whole article in this handler lets users dismiss tooltips by clicking
  // off the annotation.
  const onArticleClick = () => setPinnedId(null);

  return (
    <div
      className="font-serif text-zinc-900 dark:text-zinc-100"
      style={{ fontSize: 18, lineHeight: 1.65 }}
      onClick={interactive ? onArticleClick : undefined}
    >
      {parts.map((part, partIdx) => {
        if (part.type === 'spacer') return <div key={partIdx} style={{ height: 12 }} />;
        if (part.type === 'subpart-label') {
          return (
            <div key={partIdx} className="font-sans" style={{ fontWeight: 700, fontSize: 13, color: '#78716C', letterSpacing: 0.4, marginTop: 14, marginBottom: 4 }}>
              {part.content.map((s, i) => renderSegment(s, partIdx, i))}
            </div>
          );
        }
        if (part.type === 'formula') {
          return (
            <div key={partIdx} className="font-mono" style={{ fontSize: 16, padding: '10px 14px', backgroundColor: '#FAF7F4', border: '1px solid #EDEBE8', borderRadius: 8, margin: '8px 0', display: 'inline-block' }}>
              {part.content.map((s, i) => renderSegment(s, partIdx, i))}
            </div>
          );
        }
        if (part.type === 'list-item') {
          return (
            <li key={partIdx} style={{ marginLeft: 20, marginBottom: 6, listStyle: 'disc' }}>
              {part.content.map((s, i) => renderSegment(s, partIdx, i))}
            </li>
          );
        }
        return (
          <p key={partIdx} style={{ marginBottom: 10 }}>
            {part.content.map((s, i) => renderSegment(s, partIdx, i))}
          </p>
        );
      })}
    </div>
  );
};

const AnnotationTooltip: React.FC<{ note: string }> = ({ note }) => (
  <span
    role="tooltip"
    onClick={(e) => e.stopPropagation()}
    style={{
      position: 'absolute',
      top: 'calc(100% + 8px)',
      left: 0,
      zIndex: 20,
      width: 'min(320px, 80vw)',
      backgroundColor: '#FFFFFF',
      border: '1px solid #EDEBE8',
      boxShadow: '0 8px 24px rgba(0,0,0,0.08)',
      borderRadius: 10,
      padding: '10px 12px',
      fontFamily: 'DM Sans, system-ui, sans-serif',
      fontSize: 12.5,
      lineHeight: 1.5,
      color: '#3F3B36',
      textDecoration: 'none',
      fontWeight: 400,
    }}
  >
    {note}
  </span>
);

export default AnnotatedText;
