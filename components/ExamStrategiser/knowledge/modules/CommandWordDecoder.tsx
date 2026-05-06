/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Command Word Decoder (E1).
 * Paste any LC question. Detects command words from COMMAND_WORDS and the
 * 4 perennial modifiers from COMMAND_MODIFIERS, then reveals what each one
 * actually demands.
 *
 * Source: /docs/leaving-cert-knowledge-dossier.md § A1 (pages 2-3).
 */

import React, { useMemo, useState } from 'react';
import { COMMAND_WORDS, COMMAND_MODIFIERS } from '../../../../data/knowledge';
import { type CommandWordEntry, type ModifierEntry } from '../../../../types/knowledge';
import KnowledgeModuleShell from '../KnowledgeModuleShell';
import QuickCheck from '../QuickCheck';

const TEAL = '#2A7D6F';

interface Props {
  onBack: () => void;
}

interface DetectedCommand {
  entry: CommandWordEntry;
  matchedTerm: string;
}

interface DetectedModifier {
  entry: ModifierEntry;
  matchedTerm: string;
}

const SAMPLE_QUESTIONS: { label: string; text: string }[] = [
  {
    label: 'English — Comparative',
    text: '"Compare the ways in which significant insights into a chosen theme are shared with the reader in two of the texts on your comparative course."',
  },
  {
    label: 'Geography — Section 2',
    text: '"Examine the formation of one feature of erosion and one feature of deposition that you have studied."',
  },
  {
    label: 'History — Documents',
    text: '"To what extent was the Treaty of Versailles a fair settlement? Discuss with reference to the documents."',
  },
  {
    label: 'Business — ABQ',
    text: '"Evaluate two factors that influenced the management style at FreshFoods Ltd, with reference to the case study."',
  },
];

const CommandWordDecoder: React.FC<Props> = ({ onBack }) => {
  const [text, setText] = useState('');

  const detectedCommands = useMemo<DetectedCommand[]>(() => {
    if (!text.trim()) return [];
    const lower = text.toLowerCase();
    const found = new Map<string, DetectedCommand>();
    for (const entry of COMMAND_WORDS) {
      const candidates = [entry.word, ...(entry.aliases ?? [])];
      for (const candidate of candidates) {
        const pattern = new RegExp(`\\b${escapeRegExp(candidate.toLowerCase())}\\b`, 'i');
        if (pattern.test(lower)) {
          if (!found.has(entry.word)) {
            found.set(entry.word, { entry, matchedTerm: candidate });
          }
          break;
        }
      }
    }
    return Array.from(found.values());
  }, [text]);

  const detectedModifiers = useMemo<DetectedModifier[]>(() => {
    if (!text.trim()) return [];
    const lower = text.toLowerCase();
    return COMMAND_MODIFIERS.filter(m => new RegExp(`\\b${escapeRegExp(m.word.toLowerCase())}\\b`, 'i').test(lower))
      .map(entry => ({ entry, matchedTerm: entry.word }));
  }, [text]);

  return (
    <KnowledgeModuleShell
      title="Command Word Decoder"
      subtitle="Paste any Leaving Cert question. We'll show you the command words, the modifiers, and the structural template the examiner expects."
      whyThisMatters={
        <>
          <p style={{ marginBottom: 10 }}>
            Every Leaving Cert question is engineered around a <strong>command word</strong> — Discuss, Evaluate, Compare, Outline.
            Each one demands a different shape of answer. Examiners write the marking scheme around the command word, not around the topic.
          </p>
          <p style={{ marginBottom: 10 }}>
            The Chief Examiner has called <em>"Explain"</em> the most-confused word in the LC: students describe when they should
            be tracing how things happen. <em>"Discuss"</em> requires multiple perspectives plus a conclusion — single-perspective
            answers cap below the band, no matter how well written.
          </p>
          <p style={{ margin: 0 }}>
            <strong>Modifiers</strong> are the words around the command — "<em>significant</em> insights", "<em>effective</em> use",
            "<em>deeply</em> embedded". In English, the Purpose marks live in these. Miss the modifier, miss the question.
          </p>
        </>
      }
      summary={
        <ul style={{ paddingLeft: 18, margin: 0 }}>
          <li style={{ marginBottom: 6 }}>The command word tells you the shape of answer — describe, explain, discuss, evaluate are not interchangeable.</li>
          <li style={{ marginBottom: 6 }}>Modifiers control how marks are awarded — "significant", "effective", "deeply" each shift the demand.</li>
          <li style={{ marginBottom: 0 }}>Underlining both before you write is a 30-second habit that prevents prepared-answer drift on every paper.</li>
        </ul>
      }
      onBackToLanding={onBack}
    >
      <PasteCard text={text} setText={setText} />

      {!text.trim() && (
        <section
          className="rounded-2xl"
          style={{ backgroundColor: '#FAF7F4', border: '1px solid #EDEBE8', padding: '20px 22px' }}
        >
          <p className="font-sans" style={{ fontSize: 11, fontWeight: 700, textTransform: 'uppercase', letterSpacing: 0.6, color: TEAL, marginBottom: 10 }}>
            Try a sample question
          </p>
          <div className="grid sm:grid-cols-2 gap-2">
            {SAMPLE_QUESTIONS.map(s => (
              <button
                key={s.label}
                type="button"
                onClick={() => setText(s.text)}
                className="text-left rounded-xl transition-colors font-sans"
                style={{
                  backgroundColor: '#FFFFFF',
                  border: '1px solid #EDEBE8',
                  padding: '12px 14px',
                  cursor: 'pointer',
                }}
              >
                <p style={{ fontSize: 10, fontWeight: 700, textTransform: 'uppercase', letterSpacing: 0.5, color: TEAL, marginBottom: 4 }}>
                  {s.label}
                </p>
                <p style={{ fontSize: 12.5, color: '#3F3B36', lineHeight: 1.45 }}>{s.text}</p>
              </button>
            ))}
          </div>
        </section>
      )}

      {text.trim() && (
        <DecodedView text={text} commands={detectedCommands} modifiers={detectedModifiers} />
      )}

      <QuickCheck
        heading="Test yourself"
        questions={[
          {
            id: 'q1',
            prompt: 'Which command word demands a judgement supported by reasons, and is most common in Business ABQ sub-parts?',
            options: ['Describe', 'Evaluate', 'Outline', 'Define'],
            correctAnswer: 'Evaluate',
            explanation:
              '"Evaluate" (alias "Assess") requires the student\'s own opinion explicitly. Treating it as "Describe" caps marks — the marking scheme rewards the judgement.',
          },
          {
            id: 'q2',
            prompt: 'A 30-mark Comparative Studies essay covers all of Text A, then all of Text B, then all of Text C. What grade band does this typically achieve?',
            options: [
              'High — thorough coverage',
              'Mid-band at best — texts must be integrated, not serial',
              'Top band if the prose is strong',
              'Untouched — markers do not read serial answers',
            ],
            correctAnswer: 'Mid-band at best — texts must be integrated, not serial',
            explanation:
              '"Compare" demands integration. The English CER explicitly notes "best answers were written in an analytical fashion" — each paragraph should bring both texts into dialogue.',
          },
          {
            id: 'q3',
            prompt: 'A question reads: "Discuss the effective use of disturbing imagery in the poem." Which modifier signals you must analyse the success of the technique, not just identify it?',
            options: ['discuss', 'effective', 'disturbing', 'imagery'],
            correctAnswer: 'effective',
            explanation:
              '"Effective" demands evaluation of how well the technique works. "Disturbing" is a tonal modifier — your evidence must support that specific tone. Both modifiers carry Purpose marks in English.',
          },
        ]}
      />
    </KnowledgeModuleShell>
  );
};

const PasteCard: React.FC<{ text: string; setText: (v: string) => void }> = ({ text, setText }) => (
  <section
    className="rounded-2xl"
    style={{ backgroundColor: '#FFFFFF', border: '1px solid #EDEBE8', padding: '22px 24px' }}
  >
    <label htmlFor="cw-input" className="font-sans block" style={{ fontSize: 11, fontWeight: 700, textTransform: 'uppercase', letterSpacing: 0.6, color: TEAL, marginBottom: 8 }}>
      Paste a Leaving Cert question
    </label>
    <textarea
      id="cw-input"
      value={text}
      onChange={(e) => setText(e.target.value)}
      placeholder="e.g. Discuss, with reference to two of the texts you have studied, how a significant insight into a chosen theme was shared with the reader."
      className="w-full font-serif rounded-xl"
      style={{
        backgroundColor: '#FAF7F4',
        border: '1px solid #EDEBE8',
        padding: '14px 16px',
        fontSize: 14.5,
        lineHeight: 1.55,
        color: '#1A1A1A',
        minHeight: 110,
        resize: 'vertical',
        outline: 'none',
      }}
    />
    {text.trim() && (
      <button
        type="button"
        onClick={() => setText('')}
        className="font-sans"
        style={{ marginTop: 10, fontSize: 12, color: '#78716C', background: 'transparent', border: 'none', padding: 0, cursor: 'pointer' }}
      >
        Clear
      </button>
    )}
  </section>
);

const DecodedView: React.FC<{
  text: string;
  commands: DetectedCommand[];
  modifiers: DetectedModifier[];
}> = ({ text, commands, modifiers }) => {
  const detectedTerms = [
    ...commands.map(c => c.matchedTerm),
    ...modifiers.map(m => m.matchedTerm),
  ];

  return (
    <div className="space-y-4">
      <section
        className="rounded-2xl"
        style={{ backgroundColor: '#FAF7F4', border: `1px solid ${TEAL}33`, padding: '20px 24px' }}
      >
        <p className="font-sans" style={{ fontSize: 11, fontWeight: 700, textTransform: 'uppercase', letterSpacing: 0.6, color: TEAL, marginBottom: 10 }}>
          Highlighted question
        </p>
        <p className="font-serif" style={{ fontSize: 16, lineHeight: 1.6, color: '#1A1A1A' }}>
          <HighlightedText text={text} terms={detectedTerms} />
        </p>
      </section>

      {commands.length === 0 && modifiers.length === 0 && (
        <section
          className="rounded-2xl"
          style={{ backgroundColor: '#FFFFFF', border: '1px solid #EDEBE8', padding: '20px 24px' }}
        >
          <p className="font-sans" style={{ fontSize: 13, color: '#78716C', lineHeight: 1.55 }}>
            No command words or modifiers detected. Try a fuller question — the command word is usually the first verb (Discuss, Compare, Outline, Evaluate, Examine).
          </p>
        </section>
      )}

      {commands.length > 0 && (
        <section className="space-y-3">
          <h3 className="font-serif" style={{ fontSize: 16, fontWeight: 600, color: '#1A1A1A' }}>
            Command words detected
          </h3>
          {commands.map(c => <CommandCard key={c.entry.word} detected={c} />)}
        </section>
      )}

      {modifiers.length > 0 && (
        <section className="space-y-2">
          <h3 className="font-serif" style={{ fontSize: 16, fontWeight: 600, color: '#1A1A1A' }}>
            Modifiers detected
          </h3>
          <p className="font-sans" style={{ fontSize: 12.5, color: '#78716C', marginBottom: 6 }}>
            Each modifier shifts the demand around the command word. In English, the Purpose marks live here.
          </p>
          <div className="grid sm:grid-cols-2 gap-2">
            {modifiers.map(m => <ModifierCard key={m.entry.word} detected={m} />)}
          </div>
        </section>
      )}
    </div>
  );
};

const CommandCard: React.FC<{ detected: DetectedCommand }> = ({ detected }) => (
  <article
    className="rounded-2xl"
    style={{ backgroundColor: '#FFFFFF', border: '1px solid #EDEBE8', padding: '18px 22px' }}
  >
    <div className="flex items-baseline justify-between gap-3 mb-2">
      <h4 className="font-serif" style={{ fontSize: 18, fontWeight: 600, color: '#1A1A1A' }}>
        {detected.entry.word}
        {detected.matchedTerm.toLowerCase() !== detected.entry.word.toLowerCase() && (
          <span className="font-sans" style={{ fontSize: 12, fontWeight: 500, color: '#78716C', marginLeft: 8 }}>
            (you wrote &ldquo;{detected.matchedTerm}&rdquo;)
          </span>
        )}
      </h4>
      <span
        className="font-sans shrink-0"
        style={{
          fontSize: 10,
          fontWeight: 700,
          color: TEAL,
          backgroundColor: '#FAF7F4',
          border: `1px solid ${TEAL}33`,
          borderRadius: 999,
          padding: '2px 9px',
          whiteSpace: 'nowrap',
        }}
      >
        {detected.entry.typicalMarkRange.split('.')[0]}
      </span>
    </div>
    <DetailRow label="Required action" body={detected.entry.requiredAction} />
    <DetailRow label="Structural template" body={detected.entry.structuralTemplate} />
    <DetailRow label="Common error" body={detected.entry.commonError} highlight />
  </article>
);

const ModifierCard: React.FC<{ detected: DetectedModifier }> = ({ detected }) => (
  <article
    className="rounded-xl"
    style={{ backgroundColor: '#FFFFFF', border: '1px solid #EDEBE8', padding: '14px 16px' }}
  >
    <p className="font-serif" style={{ fontSize: 14, fontWeight: 600, color: '#1A1A1A', marginBottom: 4, fontStyle: 'italic' }}>
      {detected.entry.word}
    </p>
    <p className="font-sans" style={{ fontSize: 12.5, color: '#3F3B36', lineHeight: 1.5 }}>
      {detected.entry.signal}
    </p>
  </article>
);

const DetailRow: React.FC<{ label: string; body: string; highlight?: boolean }> = ({ label, body, highlight }) => (
  <div style={{ marginTop: 10, paddingTop: 10, borderTop: '1px solid #F5F4F1' }}>
    <p className="font-sans" style={{ fontSize: 10, fontWeight: 700, textTransform: 'uppercase', letterSpacing: 0.5, color: highlight ? '#A8746E' : '#A8A29E', marginBottom: 4 }}>
      {label}
    </p>
    <p className="font-sans" style={{ fontSize: 13, color: '#3F3B36', lineHeight: 1.55 }}>
      {body}
    </p>
  </div>
);

const HighlightedText: React.FC<{ text: string; terms: string[] }> = ({ text, terms }) => {
  if (terms.length === 0) return <>{text}</>;
  const pattern = new RegExp(`(${terms.map(escapeRegExp).join('|')})`, 'gi');
  const parts = text.split(pattern);
  return (
    <>
      {parts.map((part, i) => {
        const isMatch = terms.some(t => t.toLowerCase() === part.toLowerCase());
        return isMatch ? (
          <mark
            key={i}
            style={{
              backgroundColor: `${TEAL}26`,
              color: '#1A1A1A',
              padding: '1px 4px',
              borderRadius: 4,
              fontWeight: 600,
            }}
          >
            {part}
          </mark>
        ) : (
          <React.Fragment key={i}>{part}</React.Fragment>
        );
      })}
    </>
  );
};

function escapeRegExp(s: string): string {
  return s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

export default CommandWordDecoder;
