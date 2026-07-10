/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Definition Drill — drill the exact mark-earning wording of the definitions the
 * SEC scheme awards marks for. Pick a subject → work a deck: read the prompt,
 * recall the wording from memory, reveal the scheme's own allocation, self-rate.
 * "Review again" recirculates a card to the end of the deck.
 *
 * Data is the read-only projection in data/definitionDrill (derived from the
 * filed-scheme Marking Lens corpus, keeping only parts whose scheme fixes real
 * definition wording), so every reveal is the scheme's own phrasing — never a
 * model answer, never an invented definition.
 */

import React, { useMemo, useState } from 'react';
import { ArrowLeft, SpellCheck, RotateCcw, Check } from 'lucide-react';
import SubjectTilePicker from '../shared/SubjectTilePicker';
import {
  drillSubjects,
  definitionsForSubject,
  type DrillDefinition,
} from '../../data/definitionDrill';

const INK = '#1a1a1a';
const ACCENT = '#F26B1F';
const ACCENT_TINT = '#FDEEDF';
const ACCENT_DARK_TEXT = '#8C3A0E';
const SUCCESS = '#3A8D5F';
const SUCCESS_TINT = '#E8F2EC';
const SUCCESS_DARK_TEXT = '#1F5F3E';

interface Props {
  /** The student's subject NAMES (e.g. "Physics") — used to pre-scope "mine". */
  studentSubjects?: string[];
}

/** A stable-ish shuffle (Fisher–Yates). Runs in the browser at mount only. */
const shuffle = <T,>(arr: T[]): T[] => {
  const a = [...arr];
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
};

/** The drill deck for one subject. Keyed by subjectId in the parent, so all
 *  state resets when the subject changes. */
const DrillDeck: React.FC<{ definitions: DrillDefinition[]; subjectLabel: string; onBack: () => void }> = ({
  definitions,
  subjectLabel,
  onBack,
}) => {
  const total = definitions.length;
  const [main, setMain] = useState<DrillDefinition[]>(() => shuffle(definitions));
  const [again, setAgain] = useState<DrillDefinition[]>([]);
  const [revealed, setRevealed] = useState(false);
  const [knew, setKnew] = useState(0);

  const current = main[0];
  const done = !current;

  const advance = (wasKnown: boolean) => {
    const rest = main.slice(1);
    const nextAgain = wasKnown ? again : [...again, current];
    if (rest.length > 0) {
      setMain(rest);
      setAgain(nextAgain);
    } else {
      // Pass complete — recirculate the "review again" pile as the next pass.
      setMain(nextAgain);
      setAgain([]);
    }
    if (wasKnown) setKnew(k => k + 1);
    setRevealed(false);
  };

  const reset = () => {
    setMain(shuffle(definitions));
    setAgain([]);
    setKnew(0);
    setRevealed(false);
  };

  const header = (
    <>
      <button onClick={onBack} className="flex items-center gap-1.5 text-[13px] font-medium mb-4" style={{ color: '#7a7068' }}>
        <ArrowLeft size={15} /> All subjects
      </button>
      <h2 className="text-2xl font-semibold mb-1" style={{ fontFamily: "'Source Serif 4', serif", color: INK }}>{subjectLabel}</h2>
    </>
  );

  if (done) {
    return (
      <div className="w-full max-w-xl mx-auto pb-12">
        {header}
        <div className="rounded-2xl border-2 p-6 mt-4 text-center" style={{ borderColor: SUCCESS, backgroundColor: SUCCESS_TINT }}>
          <Check size={28} style={{ color: SUCCESS }} className="mx-auto mb-2" />
          <p className="text-[17px] font-semibold mb-1" style={{ fontFamily: "'Source Serif 4', serif", color: SUCCESS_DARK_TEXT }}>
            You drilled all {total} definition{total === 1 ? '' : 's'}.
          </p>
          <p className="text-[13px] mb-4" style={{ color: SUCCESS_DARK_TEXT }}>
            Every reveal was the SEC scheme’s own mark-earning wording.
          </p>
          <button
            onClick={reset}
            className="inline-flex items-center gap-2 rounded-full px-6 py-2.5 text-white font-semibold text-[14px]"
            style={{ backgroundColor: ACCENT, borderBottom: '3px solid #B54D14' }}
          >
            <RotateCcw size={15} /> Drill again
          </button>
        </div>
      </div>
    );
  }

  const pct = Math.round((knew / total) * 100);

  return (
    <div className="w-full max-w-xl mx-auto pb-12">
      {header}

      {/* Progress */}
      <div className="flex items-center gap-3 mt-3 mb-4">
        <div className="flex-1 h-2 rounded-full overflow-hidden" style={{ backgroundColor: '#e0dbd4' }}>
          <div className="h-full rounded-full transition-all" style={{ width: `${pct}%`, backgroundColor: ACCENT }} />
        </div>
        <span className="text-[12px] font-bold tabular-nums" style={{ color: '#7a7068' }}>{knew} / {total} known</span>
      </div>

      {/* Prompt card */}
      <div className="rounded-2xl border-2 p-5 sm:p-6" style={{ borderColor: INK, backgroundColor: '#fff' }}>
        <div className="flex items-start justify-between gap-2 mb-3">
          <span className="text-[11px] font-bold uppercase tracking-wide" style={{ color: '#9e9186' }}>Define / state</span>
          <span className="shrink-0 text-[12px] font-bold tabular-nums px-2.5 py-1 rounded-full" style={{ backgroundColor: ACCENT_TINT, color: ACCENT_DARK_TEXT }}>
            {current.marks} marks
          </span>
        </div>
        <p className="text-[18px] font-semibold leading-snug mb-4" style={{ fontFamily: "'Source Serif 4', serif", color: INK }}>
          {current.prompt}
        </p>

        {!revealed ? (
          <>
            <p className="text-[13px] italic mb-3" style={{ color: '#7a7068' }}>Recall the marking wording, then reveal.</p>
            <button
              onClick={() => setRevealed(true)}
              className="w-full rounded-full px-6 py-3 text-white font-semibold text-[15px]"
              style={{ backgroundColor: ACCENT, borderBottom: '3px solid #B54D14' }}
            >
              Reveal the marking wording
            </button>
          </>
        ) : (
          <>
            <div className="rounded-r-lg px-4 py-3 mb-1" style={{ backgroundColor: ACCENT_TINT, borderLeft: `3px solid ${ACCENT}` }}>
              <p className="text-[10px] font-bold uppercase tracking-wide mb-1" style={{ color: ACCENT_DARK_TEXT }}>What the scheme awards the marks for</p>
              <p className="text-[14px] leading-relaxed" style={{ color: ACCENT_DARK_TEXT }}>{current.answer}</p>
            </div>
            <p className="text-[10.5px] mb-4" style={{ color: '#9e9186' }}>{current.source}</p>

            <div className="flex gap-2.5">
              <button
                onClick={() => advance(true)}
                className="flex-1 inline-flex items-center justify-center gap-1.5 rounded-full px-4 py-2.5 font-semibold text-[14px] text-white"
                style={{ backgroundColor: SUCCESS, borderBottom: '3px solid #2C6B47' }}
              >
                <Check size={15} /> I knew it
              </button>
              <button
                onClick={() => advance(false)}
                className="flex-1 inline-flex items-center justify-center gap-1.5 rounded-full px-4 py-2.5 font-semibold text-[14px] bg-white"
                style={{ color: '#7a7068', border: '2px solid #d0cdc8' }}
              >
                <RotateCcw size={14} /> Review again
              </button>
            </div>
          </>
        )}
      </div>
    </div>
  );
};

const DefinitionDrill: React.FC<Props> = ({ studentSubjects = [] }) => {
  const subjects = useMemo(() => drillSubjects(), []);
  const mineIds = useMemo(() => {
    const names = new Set(studentSubjects.map(s => s.trim().toLowerCase()));
    return subjects.filter(s => names.has(s.label.trim().toLowerCase())).map(s => s.id);
  }, [studentSubjects, subjects]);
  const [scope, setScope] = useState<'mine' | 'all'>('all');
  const [subjectId, setSubjectId] = useState<string | null>(null);

  const subjectLabel = (id: string) => subjects.find(s => s.id === id)?.label ?? id;

  // ── Level 1: the drill deck (keyed so state resets per subject) ──
  if (subjectId) {
    return (
      <DrillDeck
        key={subjectId}
        definitions={definitionsForSubject(subjectId)}
        subjectLabel={subjectLabel(subjectId)}
        onBack={() => setSubjectId(null)}
      />
    );
  }

  // ── Level 0: subject picker ──
  return (
    <div className="w-full max-w-xl mx-auto pb-12">
      <h2 className="text-2xl font-semibold mb-1 flex items-center gap-2" style={{ fontFamily: "'Source Serif 4', serif", color: INK }}>
        <SpellCheck size={20} style={{ color: ACCENT }} /> Definition Drill
      </h2>
      <p className="text-[13.5px] leading-relaxed mb-5" style={{ color: '#5a5550' }}>
        Drill the exact wording the marking scheme awards the definition marks for. Read the prompt, recall the wording, then reveal the scheme’s own allocation — and rate yourself.
      </p>
      {subjects.length === 0 ? (
        <p className="text-[13.5px] rounded-2xl px-4 py-4" style={{ backgroundColor: '#E8EFF5', color: '#27506E' }}>
          Definitions are being added subject by subject — check back soon.
        </p>
      ) : (
        <SubjectTilePicker
          headingLabel="Pick a subject"
          subjects={subjects.map(s => ({ id: s.id, label: s.label, sublabel: `${s.count} definition${s.count === 1 ? '' : 's'}` }))}
          mineIds={mineIds}
          scope={scope}
          onScopeChange={setScope}
          onPick={setSubjectId}
        />
      )}
    </div>
  );
};

export default DefinitionDrill;
