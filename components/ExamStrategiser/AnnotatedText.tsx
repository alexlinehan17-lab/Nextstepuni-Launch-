/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * AnnotatedText — renders a QuestionPart[] with optional inline annotations.
 * Two render modes:
 *   - mode="raw": annotations are stripped, plain question text only
 *   - mode="annotated": annotations are visualised, hover/tap reveals notes
 */

import React from 'react';
import { type QuestionPart, type AnnotationType } from '../../types/examStrategiser';

const TEAL = '#2A7D6F';

interface AnnotatedTextProps {
  parts: QuestionPart[];
  mode: 'raw' | 'annotated';
  /** marks-to-minutes computation context. Only used by 'marks-allocation' annotations. */
  marksToMinutesContext?: { totalPaperMarks: number; totalPaperMinutes: number; questionMarks: number };
  /** Currently revealed annotation id (click-to-reveal on mobile). null = none open. */
  revealedAnnotationId?: string | null;
  /** Tells the parent which annotation a tap opened, so the side-panel can scroll to it. */
  onAnnotationClick?: (annotationId: string) => void;
}

/** Each annotated segment gets a stable id derived from its position in the
 *  parts tree. Used so the side-panel and inline tooltip stay in sync. */
function makeAnnotationId(partIdx: number, segIdx: number) {
  return `ann-${partIdx}-${segIdx}`;
}

const annotationStyle = (type: AnnotationType): React.CSSProperties => {
  switch (type) {
    case 'command':
      return { textDecoration: `underline solid ${TEAL}`, textDecorationThickness: 2, textUnderlineOffset: 4, cursor: 'help' };
    case 'keyword':
      return { textDecoration: `underline dotted ${TEAL}`, textDecorationThickness: 2, textUnderlineOffset: 4, cursor: 'help' };
    case 'trap':
      return { textDecoration: `underline wavy ${TEAL}`, textDecorationThickness: 1.5, textDecorationSkipInk: 'auto', textUnderlineOffset: 4, cursor: 'help', opacity: 0.95 };
    case 'marks-allocation':
      // Pill is rendered separately, segment span just gets neutral style.
      return { cursor: 'help' };
  }
};

const TrapIcon: React.FC = () => (
  <svg width="11" height="11" viewBox="0 0 12 12" aria-hidden style={{ display: 'inline-block', marginLeft: 3, verticalAlign: 'middle', color: TEAL, opacity: 0.65 }}>
    <path d="M6 2L11 10H1L6 2Z" stroke="currentColor" strokeWidth="1.4" fill="none" strokeLinejoin="round" />
    <line x1="6" y1="5" x2="6" y2="7.5" stroke="currentColor" strokeWidth="1.4" strokeLinecap="round" />
    <circle cx="6" cy="9" r="0.6" fill="currentColor" />
  </svg>
);

const MarksPill: React.FC<{ label: string }> = ({ label }) => (
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
    }}
  >
    {label}
  </span>
);

const AnnotatedText: React.FC<AnnotatedTextProps> = ({
  parts,
  mode,
  marksToMinutesContext,
  revealedAnnotationId,
  onAnnotationClick,
}) => {
  const renderSegment = (
    seg: QuestionPart['content'][number],
    partIdx: number,
    segIdx: number,
  ) => {
    const text = seg.text;
    if (mode === 'raw' || !seg.annotation) {
      return <span key={segIdx}>{text}</span>;
    }
    const id = makeAnnotationId(partIdx, segIdx);
    const isOpen = revealedAnnotationId === id;
    const ann = seg.annotation;

    if (ann.type === 'marks-allocation') {
      // Heuristic: a "question-level marker" is a segment whose text is a
      // parenthesised marks number like "(20)" or "(50)". Those keep the
      // existing computed pill ("20 marks · 17 mins"). Anything else (e.g.
      // a subpart label like "(a)" with per-subpart marks in the note) uses
      // the annotation note as the pill text directly.
      const isQuestionLevelMarker = /^\s*\(\d+\)\s*$/.test(text);
      let pillLabel: string;
      if (isQuestionLevelMarker && marksToMinutesContext) {
        const { totalPaperMarks, totalPaperMinutes, questionMarks } = marksToMinutesContext;
        const mins = totalPaperMarks > 0 ? Math.round((questionMarks / totalPaperMarks) * totalPaperMinutes) : 0;
        pillLabel = mins > 0 ? `${questionMarks} marks · ${mins} mins` : ann.note;
      } else {
        pillLabel = ann.note;
      }
      return (
        <span
          key={segIdx}
          id={id}
          data-annotation-id={id}
          onMouseEnter={() => onAnnotationClick?.(id)}
          onClick={() => onAnnotationClick?.(id)}
          style={{ position: 'relative', cursor: 'help' }}
        >
          <MarksPill label={pillLabel} />
          {pillLabel !== ann.note && <AnnotationTooltip note={ann.note} open={isOpen} />}
        </span>
      );
    }

    return (
      <span
        key={segIdx}
        id={id}
        data-annotation-id={id}
        onMouseEnter={() => onAnnotationClick?.(id)}
        onMouseLeave={() => { /* hover close handled by parent if needed */ }}
        onClick={(e) => { e.stopPropagation(); onAnnotationClick?.(id); }}
        style={{ ...annotationStyle(ann.type), position: 'relative' }}
      >
        {text}
        {ann.type === 'trap' && <TrapIcon />}
        <AnnotationTooltip note={ann.note} open={isOpen} />
      </span>
    );
  };

  return (
    <div className="font-serif text-zinc-900 dark:text-zinc-100" style={{ fontSize: 18, lineHeight: 1.65 }}>
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

const AnnotationTooltip: React.FC<{ note: string; open: boolean }> = ({ note, open }) => {
  if (!open) return null;
  return (
    <span
      role="tooltip"
      style={{
        position: 'absolute',
        top: 'calc(100% + 8px)',
        left: 0,
        zIndex: 20,
        width: 'min(320px, 80vw)',
        backgroundColor: '#FFFFFF',
        border: '1px solid #EDEBE8',
        boxShadow: '0 8px 24px rgba(0,0,0,0.06)',
        borderRadius: 10,
        padding: '10px 12px',
        fontFamily: 'DM Sans, system-ui, sans-serif',
        fontSize: 12.5,
        lineHeight: 1.5,
        color: '#3F3B36',
        textDecoration: 'none',
        fontWeight: 400,
        opacity: 1,
      }}
    >
      {note}
    </span>
  );
};

export default AnnotatedText;
export { makeAnnotationId };
