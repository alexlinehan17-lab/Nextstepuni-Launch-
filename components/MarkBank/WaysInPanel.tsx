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
import './waysInPanel.css';

type Stage = 'read' | 'understand' | 'plan';

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
  read: 'Read',
  understand: 'Understand',
  plan: 'Plan',
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
  const readingLines = useMemo(() => [
    ...splitQuestionLines(source.stem ?? '').map(text => ({ text, kind: 'Paper instruction' })),
    ...(model.lines.length ? model.lines : [model.exactText].filter(Boolean))
      .map(text => ({ text, kind: 'Question' })),
  ], [model.exactText, model.lines, source.stem]);
  const [stage, setStage] = useState<Stage>('read');
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
  const commandGroups = useMemo(() => {
    const grouped: Array<(typeof model.commands)[number] & { count: number }> = [];
    for (const command of model.commands) {
      const existing = grouped.find(item => (
        item.surface.toLowerCase() === command.surface.toLowerCase()
        && item.requiredAction === command.requiredAction
      ));
      if (existing) existing.count += 1;
      else grouped.push({ ...command, count: 1 });
    }
    return grouped;
  }, [model.commands]);

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
      if (current.planNotes.length >= model.planPrompts.length) return current;
      return {
        ...current,
        planNotes: [
          ...current.planNotes,
          ...Array.from({ length: model.planPrompts.length - current.planNotes.length }, () => ''),
        ],
      };
    });
  }, [model.planPrompts.length, setWork]);

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

  const minimumPlanLines = model.planPrompts.length;
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
    stage === 'read'
      ? 'Work with one exact line at a time.'
      : stage === 'understand'
        ? 'The task map is now available.'
        : 'The planning frame is now available.'
  }`;
  const planEvidence = model.planShape.evidence?.replace(/(\d)\.(?=,|$)/g, '$1');
  const planHeading = model.planKind === 'calculation'
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

        {stage === 'understand' && (
          <section id="mb-wi-understand-panel" aria-labelledby="mb-wi-understand-title">
            <p className="mb-wi-eyebrow">Map the task</p>
            <h3 id="mb-wi-understand-title">What the wording is doing</h3>
            <p className="mb-wi-stage-intro">Separate the action from the information and limits around it.</p>

            <dl className="mb-wi-task-map">
              {commandGroups.length > 0 && <div>
                <dt>Instruction</dt>
                <dd className="mb-wi-instructions">
                    {commandGroups.map((command, index) => (
                      <div key={`${command.surface}-${index}`}>
                        <strong>
                          {commandGroups.length > 1 && <b>{String(index + 1).padStart(2, '0')}</b>}
                          “{command.surface}”
                        </strong>
                        {command.count > 1 && <small>Used in {command.count} printed parts</small>}
                        <span>{command.requiredAction}</span>
                      </div>
                    ))}
                </dd>
              </div>}
              {model.constraints.length > 0 && <div>
                <dt>Printed limits</dt>
                <dd>
                  <ul>{model.constraints.map(item => <li key={item}>{item}</li>)}</ul>
                </dd>
              </div>}
              {model.givens.length > 0 && <div>
                <dt>Information supplied</dt>
                <dd>
                  <ul>{model.givens.map(item => <li key={item}>{item}</li>)}</ul>
                </dd>
              </div>}
            </dl>
            <p className="mb-wi-method-note">This is a wording map, not a marking rule or a model answer.</p>
          </section>
        )}

        {stage === 'plan' && (
          <section id="mb-wi-plan-panel" aria-labelledby="mb-wi-plan-title">
            <p className="mb-wi-eyebrow">Externalise the next step</p>
            <h3 id="mb-wi-plan-title">{planHeading}</h3>
            {model.planShape.basis === 'printed' ? (
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
                <div className="mb-wi-plan-row" key={model.planPrompts[index]?.id ?? `extra-${index}`}>
                  <span aria-hidden="true">{String(index + 1).padStart(2, '0')}</span>
                  <label>
                    <strong>{model.planPrompts[index]?.label ?? 'Extra idea'}</strong>
                    {model.planPrompts[index]?.sourceText && (
                      <small>{model.planPrompts[index].sourceText}</small>
                    )}
                    <input
                      value={note}
                      onChange={event => updatePlanNote(index, event.target.value)}
                      placeholder={model.planPrompts[index]?.placeholder ?? 'Add another point if you need one'}
                      aria-label={`Plan idea ${index + 1}: ${model.planPrompts[index]?.label ?? 'Extra idea'}`}
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
  if (!hasWaysInWork(work)) return null;
  const notes = work.planNotes.flatMap((note, index) => note.trim() ? [{ note, index }] : []);
  return (
    <section className="mb-wi-attempt-review" aria-labelledby="mb-wi-attempt-review-title">
      <p className="mb-wi-eyebrow">Your work before reveal</p>
      <h3 id="mb-wi-attempt-review-title">Compare your attempt.</h3>
      {notes.length > 0 && (
        <ol>{notes.map(({ note, index }) => (
          <li key={`${index}-${note}`}>
            <strong>{model.planPrompts[index]?.label ?? `Extra idea ${index + 1}`}</strong>
            {model.planPrompts[index]?.sourceText && <small>{model.planPrompts[index].sourceText}</small>}
            <span>{note}</span>
          </li>
        ))}</ol>
      )}
      {work.draft.trim() && <p className="mb-wi-draft-review">{work.draft}</p>}
    </section>
  );
};

export default WaysInPanel;
