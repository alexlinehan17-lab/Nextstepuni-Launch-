/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React from 'react';
import { type ExamQuestion } from '../../../types/examStrategiser';

interface Props {
  question: ExamQuestion;
}

/** Tiny, dependency-free markdown-ish renderer for mark schemes:
 *   blank lines split paragraphs; lines starting with "- " become list items;
 *   "**bold**" becomes <strong>. Anything more elaborate should land in a real
 *   markdown renderer later. */
function renderMini(md: string): React.ReactNode {
  const blocks = md.split(/\n\s*\n/);
  return blocks.map((block, i) => {
    const lines = block.split('\n');
    const isList = lines.every(l => l.trim().startsWith('- '));
    if (isList) {
      return (
        <ul key={i} style={{ paddingLeft: 18, marginBottom: 12 }}>
          {lines.map((l, j) => (
            <li key={j} style={{ marginBottom: 4, listStyle: 'disc' }}>{boldify(l.replace(/^-\s*/, ''))}</li>
          ))}
        </ul>
      );
    }
    return <p key={i} style={{ marginBottom: 12 }}>{boldify(block)}</p>;
  });
}

function boldify(text: string): React.ReactNode {
  const parts = text.split(/(\*\*[^*]+\*\*)/g);
  return parts.map((p, i) => {
    if (p.startsWith('**') && p.endsWith('**')) {
      return <strong key={i}>{p.slice(2, -2)}</strong>;
    }
    return <span key={i}>{p}</span>;
  });
}

const MarkSchemeStage: React.FC<Props> = ({ question }) => (
  <div className="space-y-6">
    <header>
      <p className="font-sans" style={{ fontSize: 11, fontWeight: 700, textTransform: 'uppercase', letterSpacing: 0.6, color: '#A8A29E' }}>
        Stage 5 · Mark scheme
      </p>
      <h2 className="font-serif" style={{ fontSize: 24, fontWeight: 600, color: '#1A1A1A', marginTop: 4 }}>
        How the marks are actually awarded.
      </h2>
    </header>
    <article
      className="rounded-2xl"
      style={{
        backgroundColor: '#FFFFFF',
        border: '1px solid #EDEBE8',
        padding: '28px 32px',
        fontFamily: 'DM Sans, system-ui, sans-serif',
        fontSize: 14,
        lineHeight: 1.6,
        color: '#3F3B36',
      }}
    >
      {question.markScheme ? renderMini(question.markScheme) : (
        <p style={{ color: '#A8A29E' }}>No marking scheme available for this question.</p>
      )}
    </article>
  </div>
);

export default MarkSchemeStage;
