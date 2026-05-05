/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useMemo, useState } from 'react';
import { type ExamQuestion, type AnnotationType, type QuestionPart } from '../../../types/examStrategiser';
import AnnotatedText, { makeAnnotationId } from '../AnnotatedText';

const TEAL = '#2A7D6F';

interface Props {
  question: ExamQuestion;
}

interface FlatAnnotation {
  id: string;
  type: AnnotationType;
  text: string;
  note: string;
}

function flattenAnnotations(parts: QuestionPart[]): FlatAnnotation[] {
  const out: FlatAnnotation[] = [];
  parts.forEach((part, partIdx) => {
    part.content.forEach((seg, segIdx) => {
      if (seg.annotation) {
        out.push({
          id: makeAnnotationId(partIdx, segIdx),
          type: seg.annotation.type,
          text: seg.text,
          note: seg.annotation.note,
        });
      }
    });
  });
  return out;
}

const ANNOTATION_LABEL: Record<AnnotationType, string> = {
  command: 'Command word',
  keyword: 'Key term',
  trap: 'Trap',
  'marks-allocation': 'Marks · time',
};

const AnnotationStage: React.FC<Props> = ({ question }) => {
  const [revealedId, setRevealedId] = useState<string | null>(null);
  const annotations = useMemo(() => flattenAnnotations(question.questionText), [question.questionText]);

  const marksToMinutesContext = (question.totalPaperMarks && question.totalPaperMinutes)
    ? { totalPaperMarks: question.totalPaperMarks, totalPaperMinutes: question.totalPaperMinutes, questionMarks: question.marks }
    : undefined;

  return (
    <div className="space-y-6">
      <header>
        <p className="font-sans" style={{ fontSize: 11, fontWeight: 700, textTransform: 'uppercase', letterSpacing: 0.6, color: '#A8A29E' }}>
          Stage 3 · Examiner notes
        </p>
        <h2 className="font-serif" style={{ fontSize: 24, fontWeight: 600, color: '#1A1A1A', marginTop: 4 }}>
          Tap an underlined phrase to see what it's really asking.
        </h2>
      </header>

      <div className="grid lg:grid-cols-[1fr_320px] gap-6">
        <article
          className="rounded-2xl"
          style={{
            backgroundColor: '#FFFFFF',
            border: '1px solid #EDEBE8',
            padding: '28px 32px',
            position: 'relative',
          }}
          onClick={() => setRevealedId(null)}
        >
          <AnnotatedText
            parts={question.questionText}
            mode="annotated"
            marksToMinutesContext={marksToMinutesContext}
            revealedAnnotationId={revealedId}
            onAnnotationClick={(id) => setRevealedId(id)}
          />
        </article>

        <aside className="space-y-2 lg:sticky lg:top-4 lg:self-start">
          <p className="font-sans" style={{ fontSize: 10, fontWeight: 700, textTransform: 'uppercase', letterSpacing: 0.6, color: '#A8A29E' }}>
            All annotations
          </p>
          {annotations.map(a => {
            const active = a.id === revealedId;
            return (
              <button
                key={a.id}
                type="button"
                onClick={() => setRevealedId(a.id)}
                className="w-full text-left rounded-xl transition-colors"
                style={{
                  backgroundColor: active ? '#FAF7F4' : '#FFFFFF',
                  border: `1px solid ${active ? `${TEAL}55` : '#EDEBE8'}`,
                  padding: '12px 14px',
                  cursor: 'pointer',
                }}
              >
                <div className="flex items-center gap-2 mb-1">
                  <AnnotationDot type={a.type} />
                  <span className="font-sans" style={{ fontSize: 10, fontWeight: 700, textTransform: 'uppercase', letterSpacing: 0.5, color: TEAL }}>
                    {ANNOTATION_LABEL[a.type]}
                  </span>
                </div>
                <p className="font-serif" style={{ fontSize: 14, fontWeight: 600, color: '#1A1A1A', marginBottom: 4 }}>
                  "{a.text}"
                </p>
                <p className="font-sans" style={{ fontSize: 12, color: '#5C5852', lineHeight: 1.5 }}>
                  {a.note}
                </p>
              </button>
            );
          })}
        </aside>
      </div>
    </div>
  );
};

const AnnotationDot: React.FC<{ type: AnnotationType }> = ({ type }) => {
  if (type === 'command') {
    return <span style={{ width: 10, height: 2, backgroundColor: TEAL, display: 'inline-block', borderRadius: 1 }} />;
  }
  if (type === 'keyword') {
    return (
      <span style={{ width: 10, height: 2, display: 'inline-flex', gap: 1.5 }}>
        <span style={{ width: 2, height: 2, backgroundColor: TEAL, borderRadius: 1 }} />
        <span style={{ width: 2, height: 2, backgroundColor: TEAL, borderRadius: 1 }} />
        <span style={{ width: 2, height: 2, backgroundColor: TEAL, borderRadius: 1 }} />
      </span>
    );
  }
  if (type === 'trap') {
    return (
      <svg width="10" height="6" viewBox="0 0 10 6" fill="none" aria-hidden>
        <path d="M0 4 Q 2 0, 4 4 T 8 4" stroke={TEAL} strokeWidth="1.4" fill="none" strokeLinecap="round" />
      </svg>
    );
  }
  // marks-allocation
  return <span style={{ width: 10, height: 5, backgroundColor: `${TEAL}33`, border: `1px solid ${TEAL}66`, borderRadius: 999 }} />;
};

export default AnnotationStage;
