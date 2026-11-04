/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Ways In inside Mark Bank.
 *
 * This is a question workspace, not a second product and not an answer helper.
 * It receives the same SEC card as the session, but its source adapter strips
 * every marking-scheme field before the question is interpreted. The only
 * durable state lives in SessionScreen for the lifetime of the current card;
 * no draft is written to localStorage or sent with the card grade.
 */

import React, { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import { ChevronLeft, ChevronRight, Minus, Plus, Square, Volume2, X } from 'lucide-react';
import type { SecCard } from '../../types/markBank';
import { buildQuestionModel, splitQuestionLines } from '../WaysIn/questionModel';
import { waysInSourceFromMarkBank } from '../WaysIn/sources';
import {
  buildKeyParts, planRowsFor,
  type KeyPartsBreakdown, type KPFlag, type KPUnit,
} from '../WaysIn/keyParts';
import './waysInPanel.css';

type Stage = 'breakdown' | 'read' | 'plan';

export interface WaysInWork {
  planNotes: string[];
  draft: string;
}

export const emptyWaysInWork = (): WaysInWork => ({ planNotes: [], draft: '' });

export const hasWaysInWork = (work: WaysInWork): boolean =>
  work.draft.trim().length > 0 || work.planNotes.some(note => note.trim().length > 0);

interface WaysInPanelProps {
  card: SecCard;
  subjectLabel: string;
  work: WaysInWork;
  setWork: React.Dispatch<React.SetStateAction<WaysInWork>>;
  focusMode: boolean;
  onFocusModeChange: (focused: boolean) => void;
  onClose: () => void;
}

interface SpokenRange {
  start: number;
  end: number;
}

const wordEnd = (text: string, start: number, reportedLength: number): number => {
  if (reportedLength > 0) return Math.min(text.length, start + reportedLength);
  const rest = text.slice(start);
  const match = /^\S+/.exec(rest);
  return Math.min(text.length, start + (match?.[0].length ?? 1));
};

const SpokenLine: React.FC<{
  text: string;
  activeText: string | null;
  spokenRange: SpokenRange | null;
}> = ({ text, activeText, spokenRange }) => {
  if (text !== activeText || !spokenRange) return <>{text}</>;
  return (
    <>
      {text.slice(0, spokenRange.start)}
      <mark className="mb-wi-spoken-word">{text.slice(spokenRange.start, spokenRange.end)}</mark>
      {text.slice(spokenRange.end)}
    </>
  );
};

const stageLabels: Record<Stage, string> = {
  breakdown: 'Break it down',
  read: 'Read',
  plan: 'Plan',
};

const FLAG_COPY: Record<KPFlag, string> = {
  'needs-figure': 'Uses a figure printed on the paper.',
  'values-on-paper': 'The values it needs are on the paper — in an earlier part or a table.',
  'depends-on-earlier-part': 'Builds on your answer to an earlier part.',
  'excludes-example': 'Not the example the paper already gives.',
  'as-printed': 'Shown exactly as printed.',
};

const fallbackCopy = (kp: KeyPartsBreakdown): string => {
  if (kp.mode === 'blocked') return 'This question did not come through cleanly here. Read it on the printed page.';
  if (kp.reasons.includes('non-english')) return 'This question is in the exam language, so it stays exactly as printed.';
  if (kp.reasons.includes('no-text')) return 'This question is printed as an image. Read it from the page.';
  return 'This part gives information rather than an instruction. Read it as printed; the instruction is on the paper beside it.';
};

/** One unit of the question: the job, how many, what it is about, the limits. */
const KeyPartUnit: React.FC<{ unit: KPUnit; partner?: KPUnit }> = ({ unit, partner }) => {
  const verb = [partner?.action?.display, unit.action?.display].filter(Boolean).join(' and ');
  const givens = unit.use.filter(u => u.kind === 'given');
  const material = unit.use.filter(u => u.kind !== 'given');
  const printed = unit.flags.includes('as-printed');
  const flags = unit.flags.filter(f => f !== 'as-printed');
  return (
    <li className="mb-wi-kp-unit">
      {(unit.ref || unit.altGroup || unit.marks != null) && (
        <div className="mb-wi-kp-head">
          {unit.ref && <span className="mb-wi-kp-ref">{unit.ref}</span>}
          {unit.altGroup && <span className="mb-wi-kp-alt">{unit.altGroup === 'A' ? 'Option A' : 'Option B'}</span>}
          {unit.marks != null && <span className="mb-wi-kp-marks">{unit.marks} marks</span>}
        </div>
      )}
      {printed ? (
        // A part the breakdown cannot read honestly is shown whole, never dropped.
        <dl className="mb-wi-kp-slots">
          <div>
            <dt>Do</dt>
            <dd><strong>Read it as printed</strong><span>{unit.means || 'This part could not be broken down here, so every word of it is shown.'}</span></dd>
          </div>
          {unit.focus && <div><dt>Printed</dt><dd className="mb-wi-kp-printed">{unit.focus.display}</dd></div>}
        </dl>
      ) : (
      <dl className="mb-wi-kp-slots">
        <div>
          <dt>Do</dt>
          <dd><strong className={verb.length > 56 ? 'mb-wi-kp-long' : undefined}>{verb.charAt(0).toUpperCase() + verb.slice(1)}</strong>{unit.means && <span>{unit.means}</span>}</dd>
        </div>
        {unit.item && <div><dt>Item</dt><dd className="mb-wi-kp-item">{unit.item.display}</dd></div>}
        {unit.count && <div><dt>How many</dt><dd>{unit.count.display}</dd></div>}
        {unit.sides && (
          <div><dt>Compare</dt><dd>{unit.sides[0].display} <em>vs</em> {unit.sides[1].display}</dd></div>
        )}
        {/* Two jobs done together on different objects: "Name any two methods
            … and, for each named method, give one example of a plant …". */}
        {partner?.focus && unit.focus && partner.focus.display !== unit.focus.display && (
          <div><dt>About</dt><dd>{partner.focus.display}</dd></div>
        )}
        {/* A comparison keeps its About when the sides do not cover it:
            "the indenters used in both the Brinell and the Vickers tests". */}
        {unit.focus && (!unit.sides || (unit.sides[0].from === unit.focus.from && unit.sides[0].start > unit.focus.start + 2)) && (
          <div>
            <dt>{partner?.focus && partner.focus.display !== unit.focus.display ? 'Then' : 'About'}</dt>
            <dd>
              {unit.focus.display}
              {unit.focusMore?.map(more => (
                <React.Fragment key={`${more.start}-${more.from}`}>
                  <span className="mb-wi-kp-gap" aria-hidden="true"> … </span>{more.display}
                </React.Fragment>
              ))}
            </dd>
          </div>
        )}
        {unit.conditions.length > 0 && (
          <div><dt>Only counts if</dt><dd><ul>{unit.conditions.map(c => <li key={`${c.start}-${c.from}`}>{c.display}</li>)}</ul></dd></div>
        )}
        {givens.length > 0 && (
          <div><dt>Given</dt><dd><ul>{givens.map(g => <li key={`${g.start}-${g.from}`}>{g.display}</li>)}</ul></dd></div>
        )}
        {material.length > 0 && (
          <div><dt>Use</dt><dd className="mb-wi-kp-chips">{material.map(m => <span key={`${m.start}-${m.from}`}>{m.display}</span>)}</dd></div>
        )}
      </dl>
      )}
      {flags.length > 0 && (
        <ul className="mb-wi-kp-flags">{flags.map(f => <li key={f}>{FLAG_COPY[f]}</li>)}</ul>
      )}
    </li>
  );
};

const KeyPartsView: React.FC<{ kp: KeyPartsBreakdown; onRead: () => void }> = ({ kp, onRead }) => {
  if (kp.mode === 'verbatim' || kp.mode === 'blocked') {
    return (
      <div className="mb-wi-kp-fallback">
        <p>{fallbackCopy(kp)}</p>
        {kp.mode !== 'blocked' && <button type="button" onClick={onRead}>Read it line by line</button>}
      </div>
    );
  }
  const shown = kp.units.filter(u => !u.jointWith);
  return (
    <div className="mb-wi-kp">
      {kp.mode === 'glossed' && (
        <p className="mb-wi-kp-note">This question is in the exam language. Its instruction words are explained here; the rest stays as printed.</p>
      )}
      {kp.banner && <p className="mb-wi-kp-note">The paper prints two options, marked OR. Answer one of them.</p>}
      {kp.setting && kp.setting.length > 0 && (
        <div className="mb-wi-kp-setting"><span>The question tells you</span>{kp.setting.map(s => <p key={`${s.start}-${s.from}`}>{s.display}</p>)}</div>
      )}
      {kp.cardRules.length > 0 && (
        <p className="mb-wi-kp-rules"><span>For the whole answer</span>{kp.cardRules.map(r => <em key={`${r.start}-${r.from}`}>{r.display}</em>)}</p>
      )}
      <ol className="mb-wi-kp-list" aria-label="Key parts of the question">
        {shown.map(unit => (
          <KeyPartUnit key={unit.id} unit={unit} partner={kp.units.find(p => p.jointWith === unit.id)} />
        ))}
      </ol>
    </div>
  );
};

const WaysInPanel: React.FC<WaysInPanelProps> = ({
  card,
  subjectLabel,
  work,
  setWork,
  focusMode,
  onFocusModeChange,
  onClose,
}) => {
  const source = useMemo(() => waysInSourceFromMarkBank(card, subjectLabel), [card, subjectLabel]);
  const model = useMemo(() => buildQuestionModel(source), [source]);
  const keyParts = useMemo(() => buildKeyParts(source), [source]);
  const kpRows = useMemo(
    () => planRowsFor(keyParts, { basis: model.planShape.basis, prompts: model.planPrompts }),
    [keyParts, model.planShape.basis, model.planPrompts],
  );
  const usesKeyPlan = kpRows.length > 0;
  const planRowCount = usesKeyPlan ? kpRows.length : model.planPrompts.length;
  const readingLines = useMemo(() => [
    ...splitQuestionLines(source.stem ?? '').map(text => ({ text, kind: 'Paper instruction' })),
    ...(model.lines.length ? model.lines : [model.exactText].filter(Boolean))
      .map(text => ({ text, kind: 'Question' })),
  ], [model.exactText, model.lines, source.stem]);
  const [stage, setStage] = useState<Stage>('breakdown');
  const [lineIndex, setLineIndex] = useState(0);
  const [rate, setRate] = useState(0.9);
  const [speaking, setSpeaking] = useState(false);
  const [activeText, setActiveText] = useState<string | null>(null);
  const [spokenRange, setSpokenRange] = useState<SpokenRange | null>(null);
  const panelRef = useRef<HTMLElement | null>(null);
  const titleRef = useRef<HTMLHeadingElement | null>(null);
  const speechRunRef = useRef(0);
  const speechSupported = typeof window !== 'undefined'
    && 'speechSynthesis' in window
    && typeof SpeechSynthesisUtterance !== 'undefined';

  const stopReading = useCallback(() => {
    // Invalidate callbacks before cancelling. Some engines dispatch a delayed
    // onend/onerror for the cancelled utterance; it must not stop the next one.
    speechRunRef.current += 1;
    if (typeof window !== 'undefined' && 'speechSynthesis' in window) {
      window.speechSynthesis.cancel();
    }
    setSpeaking(false);
    setActiveText(null);
    setSpokenRange(null);
  }, []);

  useEffect(() => {
    const focus = requestAnimationFrame(() => titleRef.current?.focus());
    const onKeyDown = (event: KeyboardEvent) => {
      if (event.key !== 'Escape') return;
      stopReading();
      onClose();
    };
    window.addEventListener('keydown', onKeyDown);
    return () => {
      cancelAnimationFrame(focus);
      window.removeEventListener('keydown', onKeyDown);
      speechRunRef.current += 1;
      if (typeof window !== 'undefined' && 'speechSynthesis' in window) {
        window.speechSynthesis.cancel();
      }
    };
  }, [onClose, stopReading]);

  useEffect(() => {
    if (!focusMode) return;
    let settleFrame = 0;
    const layoutFrame = requestAnimationFrame(() => {
      settleFrame = requestAnimationFrame(() => {
        if (typeof panelRef.current?.scrollIntoView === 'function') {
          panelRef.current.scrollIntoView({ block: 'start' });
        }
      });
    });
    return () => {
      cancelAnimationFrame(layoutFrame);
      cancelAnimationFrame(settleFrame);
    };
  }, [focusMode]);

  useEffect(() => {
    setWork(current => {
      if (current.planNotes.length >= planRowCount) return current;
      return {
        ...current,
        planNotes: [
          ...current.planNotes,
          ...Array.from({ length: planRowCount - current.planNotes.length }, () => ''),
        ],
      };
    });
  }, [planRowCount, setWork]);

  const readAloud = useCallback((text: string) => {
    if (!speechSupported || !text.trim()) return;
    stopReading();
    const speechRun = speechRunRef.current + 1;
    speechRunRef.current = speechRun;
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = 'en-IE';
    utterance.rate = rate;
    utterance.onboundary = event => {
      if (speechRunRef.current !== speechRun) return;
      if (event.name && event.name !== 'word') return;
      setSpokenRange({
        start: event.charIndex,
        end: wordEnd(text, event.charIndex, event.charLength),
      });
    };
    const finish = () => {
      if (speechRunRef.current !== speechRun) return;
      speechRunRef.current += 1;
      setSpeaking(false);
      setActiveText(null);
      setSpokenRange(null);
    };
    utterance.onend = finish;
    utterance.onerror = finish;
    setActiveText(text);
    setSpeaking(true);
    window.speechSynthesis.speak(utterance);
  }, [rate, speechSupported, stopReading]);

  const focusedLine = readingLines[Math.min(lineIndex, Math.max(0, readingLines.length - 1))]
    ?? { text: model.exactText, kind: 'Question' };
  const changeLine = (next: number) => {
    stopReading();
    setLineIndex(Math.max(0, Math.min(readingLines.length - 1, next)));
  };

  const changeStage = (next: Stage) => {
    stopReading();
    if (next !== 'read') onFocusModeChange(false);
    setStage(next);
  };

  const close = () => {
    stopReading();
    onFocusModeChange(false);
    onClose();
  };

  const minimumPlanLines = planRowCount;
  const visiblePlanNotes = work.planNotes.length ? work.planNotes : [''];
  const updatePlanNote = (index: number, value: string) => {
    setWork(current => {
      const planNotes = [...current.planNotes];
      planNotes[index] = value;
      return { ...current, planNotes };
    });
  };
  const addPlanLine = () => {
    setWork(current => current.planNotes.length >= 8
      ? current
      : { ...current, planNotes: [...current.planNotes, ''] });
  };
  const removePlanLine = () => {
    setWork(current => current.planNotes.length <= minimumPlanLines
      ? current
      : { ...current, planNotes: current.planNotes.slice(0, -1) });
  };
  const wordCount = work.draft.trim() ? work.draft.trim().split(/\s+/).length : 0;
  const stageStatus = `${stageLabels[stage]} stage. ${
    stage === 'breakdown'
      ? 'The key parts of the question are shown.'
      : stage === 'read'
        ? 'Work with one exact line at a time.'
        : 'The planning frame is now available.'
  }`;
  const planEvidence = model.planShape.evidence?.replace(/(\d)\.(?=,|$)/g, '$1');
  const planHeading = usesKeyPlan
    ? 'One space for each part'
    : model.planKind === 'calculation'
    ? 'Set up the working'
    : model.planKind === 'procedure'
      ? 'Set out the sequence'
      : model.planKind === 'explanation'
        ? 'Build the explanation'
        : model.planKind === 'comparison'
          ? 'Make the comparison explicit'
          : model.planKind === 'printed-parts'
            ? 'Plan each printed part'
            : 'Shape your response';
  const flexiblePlanIntro = model.planKind === 'calculation'
    ? 'Use this frame to hold the values, target and numerical route in separate places. These are working spaces, not marking points.'
    : model.planKind === 'procedure'
      ? 'Keep the actions in order so one stage does not disappear while you write the next.'
      : model.planKind === 'explanation'
        ? 'Separate your main point, the relevant information and the link back to the question.'
        : model.planKind === 'comparison'
          ? 'Hold both sides of the comparison before making the difference or connection explicit.'
          : 'Keep the exact task beside one clear response space. Add another line only if you need it.';
  const toggleFocusMode = () => {
    onFocusModeChange(!focusMode);
  };

  return (
    <section ref={panelRef} className="mb-wi-panel" aria-labelledby="mb-wi-title">
      <header className="mb-wi-header">
        <div>
          <p className="mb-wi-eyebrow">Ways In · question support</p>
          <h2 id="mb-wi-title" ref={titleRef} tabIndex={-1}>Work with the wording.</h2>
        </div>
        <button type="button" className="mb-wi-icon-button" onClick={close} aria-label="Close Ways In">
          <X size={18} aria-hidden="true" />
        </button>
      </header>

      <p className="mb-wi-promise">
        The question stays exact. These tools use its printed wording only; the marking scheme remains closed.
      </p>

      <div className="mb-wi-stage-switch" role="group" aria-label="Ways In stage">
        {(Object.keys(stageLabels) as Stage[]).map((item, index) => (
          <button
            type="button"
            key={item}
            aria-pressed={stage === item}
            aria-controls={`mb-wi-${item}-panel`}
            onClick={() => changeStage(item)}
          >
            <span>{String(index + 1).padStart(2, '0')}</span>
            {stageLabels[item]}
          </button>
        ))}
      </div>

      <p className="mb-wi-sr-only" role="status" aria-live="polite" aria-atomic="true">
        {stageStatus}
      </p>

      <div className="mb-wi-stage">
        {stage === 'breakdown' && (
          <section id="mb-wi-breakdown-panel" aria-labelledby="mb-wi-breakdown-title">
            <p className="mb-wi-eyebrow">Break it down</p>
            <h3 id="mb-wi-breakdown-title">What the question is asking</h3>
            <p className="mb-wi-stage-intro">Every piece is taken from the printed question. The marking scheme stays closed.</p>
            <KeyPartsView kp={keyParts} onRead={() => changeStage('read')} />
          </section>
        )}

        {stage === 'read' && (
          <section id="mb-wi-read-panel" aria-labelledby="mb-wi-read-title">
            <p className="mb-wi-eyebrow">Reduce what is on screen</p>
            <h3 id="mb-wi-read-title">One line at a time</h3>
            <p className="mb-wi-stage-intro">Move through the exact question without losing your place.</p>

            <button
              type="button"
              className="mb-wi-focus-toggle"
              aria-pressed={focusMode}
              onClick={toggleFocusMode}
            >
              {focusMode ? 'Show the full question' : 'Focus on this line'}
            </button>

            <div className="mb-wi-line-focus">
              <span className="mb-wi-line-kind">{focusedLine.kind}</span>
              <p>
                <SpokenLine text={focusedLine.text} activeText={activeText} spokenRange={spokenRange} />
              </p>
              <span className="mb-wi-sr-only" aria-live="polite" aria-atomic="true">
                Line {lineIndex + 1} of {readingLines.length}: {focusedLine.text}
              </span>
              <div className="mb-wi-line-nav">
                <button
                  type="button"
                  onClick={() => changeLine(lineIndex - 1)}
                  disabled={lineIndex === 0}
                  aria-label="Previous question line"
                >
                  <ChevronLeft size={17} aria-hidden="true" />
                </button>
                <span aria-live="polite">{lineIndex + 1} of {readingLines.length}</span>
                <button
                  type="button"
                  onClick={() => changeLine(lineIndex + 1)}
                  disabled={lineIndex >= readingLines.length - 1}
                  aria-label="Next question line"
                >
                  <ChevronRight size={17} aria-hidden="true" />
                </button>
              </div>
            </div>

            {focusMode && source.figure && (
              <figure className="mb-wi-focus-figure">
                <img src={source.figure.src} alt={source.figure.alt} />
                {source.figure.attribution && <figcaption>{source.figure.attribution}</figcaption>}
              </figure>
            )}

            {speechSupported && (
              <div className="mb-wi-reading-controls">
                <button
                  type="button"
                  className="mb-wi-read-button"
                  aria-pressed={speaking}
                  onClick={() => speaking ? stopReading() : readAloud(focusedLine.text)}
                >
                  {speaking
                    ? <Square size={15} fill="currentColor" aria-hidden="true" />
                    : <Volume2 size={17} aria-hidden="true" />}
                  {speaking ? 'Stop reading' : 'Read this line'}
                </button>
                <div className="mb-wi-rate" role="group" aria-label="Reading speed">
                  {[0.75, 0.9, 1].map(option => (
                    <button
                      type="button"
                      key={option}
                      aria-pressed={rate === option}
                      onClick={() => { stopReading(); setRate(option); }}
                    >
                      {option}×
                    </button>
                  ))}
                </div>
              </div>
            )}
          </section>
        )}

        {stage === 'plan' && (
          <section id="mb-wi-plan-panel" aria-labelledby="mb-wi-plan-title">
            <p className="mb-wi-eyebrow">Externalise the next step</p>
            <h3 id="mb-wi-plan-title">{planHeading}</h3>
            {usesKeyPlan ? (
              <p className="mb-wi-stage-intro">
                Each space matches one part of the question{kpRows.some(r => /\d$/.test(r.label)) ? ', and a counted part gets one space per item' : ''}. Your ideas go in; nothing here is marked.
              </p>
            ) : model.planShape.basis === 'printed' ? (
              <p className="mb-wi-stage-intro">
                {model.planShape.structure === 'parts'
                  ? `The paper separates this task into ${model.planShape.count} visible parts: ${planEvidence}.`
                  : model.planShape.structure === 'choice'
                    ? `The paper asks you to plan ${model.planShape.count}: “${model.planShape.evidence}”. The other printed options are choices, not extra tasks.`
                  : model.planShape.structure === 'blanks'
                    ? `The paper prints ${model.planShape.count} ${model.planShape.count === 1 ? 'answer space' : 'answer spaces'}.`
                    : model.planShape.structure === 'labels'
                      ? `The paper names ${model.planShape.count} figure labels: “${model.planShape.evidence}”.`
                      : model.planShape.structure === 'instructions'
                        ? `The paper gives ${model.planShape.count} separate instructions: ${model.planShape.evidence}. Start a line for each, then add more if you need them.`
                      : `The question clearly prints the planning cue: “${model.planShape.evidence}”.`}
              </p>
            ) : (
              <p className="mb-wi-stage-intro">
                {flexiblePlanIntro}
              </p>
            )}

            <div className="mb-wi-plan-lines">
              {visiblePlanNotes.map((note, index) => (
                <div className="mb-wi-plan-row" key={(usesKeyPlan ? kpRows[index]?.id : model.planPrompts[index]?.id) ?? `extra-${index}`}>
                  <span aria-hidden="true">{String(index + 1).padStart(2, '0')}</span>
                  <label>
                    <strong>{(usesKeyPlan ? kpRows[index]?.label : model.planPrompts[index]?.label) ?? 'Extra idea'}</strong>
                    {usesKeyPlan
                      ? kpRows[index]?.summary && <small>{kpRows[index].summary}</small>
                      : model.planPrompts[index]?.sourceText && <small>{model.planPrompts[index].sourceText}</small>}
                    <input
                      value={note}
                      onChange={event => updatePlanNote(index, event.target.value)}
                      placeholder={(usesKeyPlan ? kpRows[index]?.placeholder : model.planPrompts[index]?.placeholder) ?? 'Add another point if you need one'}
                      aria-label={`Plan idea ${index + 1}: ${(usesKeyPlan ? kpRows[index]?.label : model.planPrompts[index]?.label) ?? 'Extra idea'}`}
                    />
                  </label>
                </div>
              ))}
            </div>

            <div className="mb-wi-plan-actions">
              <button type="button" onClick={addPlanLine} disabled={visiblePlanNotes.length >= 8}>
                <Plus size={16} aria-hidden="true" /> Add a line
              </button>
              {visiblePlanNotes.length > minimumPlanLines && (
                <button type="button" onClick={removePlanLine}>
                  <Minus size={16} aria-hidden="true" /> Remove last
                </button>
              )}
            </div>

            <label className="mb-wi-draft-label" htmlFor={`mb-wi-draft-${card.id}`}>
              <span>Full draft <em>optional</em></span>
              <small>{wordCount} {wordCount === 1 ? 'word' : 'words'}</small>
            </label>
            <textarea
              id={`mb-wi-draft-${card.id}`}
              value={work.draft}
              onChange={event => setWork(current => ({ ...current, draft: event.target.value }))}
              placeholder="Use this space if you want to assemble the plan into a complete answer."
              aria-label="Your attempt (optional full draft)"
            />
            <p className="mb-wi-method-note">
              Kept only in this review session. It is not assessed, saved to your profile or sent with your grade.
            </p>
          </section>
        )}
      </div>
    </section>
  );
};

export const WaysInAttemptReview: React.FC<{
  work: WaysInWork;
  card: SecCard;
  subjectLabel: string;
}> = ({ work, card, subjectLabel }) => {
  const source = useMemo(() => waysInSourceFromMarkBank(card, subjectLabel), [card, subjectLabel]);
  const model = useMemo(() => buildQuestionModel(source), [source]);
  const kpRows = useMemo(
    () => planRowsFor(buildKeyParts(source), { basis: model.planShape.basis, prompts: model.planPrompts }),
    [source, model.planShape.basis, model.planPrompts],
  );
  if (!hasWaysInWork(work)) return null;
  const labelFor = (index: number) => (kpRows.length ? kpRows[index]?.label : model.planPrompts[index]?.label) ?? `Extra idea ${index + 1}`;
  const summaryFor = (index: number) => kpRows.length ? kpRows[index]?.summary : model.planPrompts[index]?.sourceText;
  const notes = work.planNotes.flatMap((note, index) => note.trim() ? [{ note, index }] : []);
  return (
    <section className="mb-wi-attempt-review" aria-labelledby="mb-wi-attempt-review-title">
      <p className="mb-wi-eyebrow">Your work before reveal</p>
      <h3 id="mb-wi-attempt-review-title">Compare your attempt.</h3>
      {notes.length > 0 && (
        <ol>{notes.map(({ note, index }) => (
          <li key={`${index}-${note}`}>
            <strong>{labelFor(index)}</strong>
            {summaryFor(index) && <small>{summaryFor(index)}</small>}
            <span>{note}</span>
          </li>
        ))}</ol>
      )}
      {work.draft.trim() && <p className="mb-wi-draft-review">{work.draft}</p>}
    </section>
  );
};

export default WaysInPanel;
