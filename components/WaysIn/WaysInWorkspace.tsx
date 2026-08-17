import React, { useEffect, useMemo, useRef, useState } from 'react';
import { createPortal } from 'react-dom';
import {
  ArrowLeft,
  ArrowRight,
  BookOpen,
  Check,
  Eye,
  Layers3,
  Pause,
  RotateCcw,
  Volume2,
  X,
} from 'lucide-react';
import { buildQuestionModel } from './questionModel';
import type {
  QuestionHighlightKind,
  WaysInMode,
  WaysInQuestionModel,
  WaysInQuestionSource,
} from './types';
import './waysIn.css';

interface WaysInWorkspaceProps {
  source: WaysInQuestionSource;
  originalPreview?: React.ReactNode;
  initialMode?: WaysInMode | null;
  onClose: () => void;
}

interface SavedWork {
  draft: string;
  slotNotes: string[];
}

const safeSavedWork = (key: string): SavedWork => {
  try {
    const parsed = JSON.parse(window.localStorage.getItem(key) ?? '{}') as Partial<SavedWork>;
    return {
      draft: typeof parsed.draft === 'string' ? parsed.draft : '',
      slotNotes: Array.isArray(parsed.slotNotes) ? parsed.slotNotes.filter(x => typeof x === 'string') : [],
    };
  } catch {
    return { draft: '', slotNotes: [] };
  }
};

const modeLabel: Record<WaysInMode, string> = {
  'one-step': 'One step at a time',
  'show-me': 'Show me',
};

const highlightLabel: Record<QuestionHighlightKind, string> = {
  action: 'The job',
  constraint: 'Boundary',
  data: 'Given data',
  content: 'Topic words',
};

const ExactQuestion: React.FC<{
  model: WaysInQuestionModel;
  annotated?: boolean;
}> = ({ model, annotated = false }) => {
  if (!model.exactText) {
    return (
      <p className="wi-empty-copy">
        This paper does not contain reliable searchable text. Use the original crop—the app will not guess at its wording.
      </p>
    );
  }
  if (!annotated || model.highlights.length === 0) {
    return <p className="wi-exact-question">{model.exactText}</p>;
  }
  const pieces: React.ReactNode[] = [];
  let cursor = 0;
  model.highlights.forEach((range, index) => {
    if (range.start > cursor) pieces.push(model.exactText.slice(cursor, range.start));
    pieces.push(
      <mark key={`${range.start}-${index}`} className={`wi-mark wi-mark--${range.kind}`} title={range.label}>
        {model.exactText.slice(range.start, range.end)}
      </mark>,
    );
    cursor = range.end;
  });
  if (cursor < model.exactText.length) pieces.push(model.exactText.slice(cursor));
  return <p className="wi-exact-question">{pieces}</p>;
};

const SourceSheet: React.FC<{
  source: WaysInQuestionSource;
  model: WaysInQuestionModel;
  preview?: React.ReactNode;
  compact?: boolean;
}> = ({ source, model, preview, compact = false }) => (
  <section className={`wi-source-sheet ${compact ? 'wi-source-sheet--compact' : ''}`} aria-label="Original question">
    <div className="wi-source-heading">
      <div>
        <p className="wi-eyebrow">Original · locked</p>
        <p className="wi-source-meta">
          {[source.subjectLabel, source.levelLabel, source.year, source.questionRef].filter(Boolean).join(' · ')}
        </p>
      </div>
      <span className="wi-source-lock" aria-label="The original wording is unchanged">Exact</span>
    </div>
    <div className="wi-source-body">
      {source.stem && !preview && <p className="wi-source-stem">{source.stem}</p>}
      {preview ?? <ExactQuestion model={model} />}
      {!preview && source.figure && (
        <figure className="wi-source-figure">
          <img src={source.figure.src} alt={source.figure.alt} />
          {source.figure.attribution && <figcaption>{source.figure.attribution}</figcaption>}
        </figure>
      )}
    </div>
    <div className="wi-source-foot">
      <span>{source.textConfidence === 'verified' ? 'Verified source text' : source.textConfidence === 'pdf-text' ? 'Searchable text from this PDF' : 'Image-only source'}</span>
      {source.sourceCopyright && <span>{source.sourceCopyright}</span>}
    </div>
  </section>
);

const ReadButton: React.FC<{ text: string }> = ({ text }) => {
  const supported = typeof window !== 'undefined' && 'speechSynthesis' in window;
  const [speaking, setSpeaking] = useState(false);

  useEffect(() => () => {
    if (speaking) window.speechSynthesis.cancel();
  }, [speaking]);

  if (!supported || !text.trim()) return null;
  const toggle = () => {
    if (speaking) {
      window.speechSynthesis.cancel();
      setSpeaking(false);
      return;
    }
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.rate = 0.88;
    utterance.onend = () => setSpeaking(false);
    utterance.onerror = () => setSpeaking(false);
    window.speechSynthesis.cancel();
    window.speechSynthesis.speak(utterance);
    setSpeaking(true);
  };
  return (
    <button type="button" onClick={toggle} aria-pressed={speaking} className="wi-small-action">
      {speaking ? <Pause size={16} /> : <Volume2 size={16} />}
      {speaking ? 'Stop reading' : 'Read this aloud'}
    </button>
  );
};

const EmptySlots: React.FC<{
  count: number;
  notes?: string[];
  onNote?: (index: number, value: string) => void;
  editable?: boolean;
}> = ({ count, notes = [], onNote, editable = false }) => (
  <div className="wi-slots">
    {Array.from({ length: count }, (_, index) => (
      <label className="wi-slot" key={index}>
        <span>{String(index + 1).padStart(2, '0')}</span>
        {editable ? (
          <input
            value={notes[index] ?? ''}
            onChange={event => onNote?.(index, event.target.value)}
            placeholder="Your idea—not the scheme"
            aria-label={`Plan answer idea ${index + 1}`}
          />
        ) : (
          <i aria-hidden="true" />
        )}
      </label>
    ))}
  </div>
);

const OneStepView: React.FC<{
  source: WaysInQuestionSource;
  model: WaysInQuestionModel;
  stepIndex: number;
  onStepIndex: (value: number) => void;
  draft: string;
  onDraft: (value: string) => void;
  onReturn: () => void;
}> = ({ source, model, stepIndex, onStepIndex, draft, onDraft, onReturn }) => {
  const [lineIndex, setLineIndex] = useState(0);
  const [checks, setChecks] = useState([false, false, false]);
  const step = model.steps[stepIndex];
  const allChecked = checks.every(Boolean);

  const body = (() => {
    switch (step.id) {
      case 'meet':
        return model.lines.length ? (
          <div>
            <div className="wi-line-focus" aria-label="Question one line at a time">
              {model.lines.map((line, index) => (
                <button
                  type="button"
                  key={`${line}-${index}`}
                  className={index === lineIndex ? 'is-current' : ''}
                  onClick={() => setLineIndex(index)}
                  aria-current={index === lineIndex ? 'step' : undefined}
                >
                  <span>{String(index + 1).padStart(2, '0')}</span>
                  <strong>{line}</strong>
                </button>
              ))}
            </div>
            <div className="wi-inline-actions">
              <button type="button" className="wi-small-action" disabled={lineIndex === 0} onClick={() => setLineIndex(i => Math.max(0, i - 1))}>
                <ArrowLeft size={15} /> Previous line
              </button>
              <button type="button" className="wi-small-action" disabled={lineIndex >= model.lines.length - 1} onClick={() => setLineIndex(i => Math.min(model.lines.length - 1, i + 1))}>
                Next line <ArrowRight size={15} />
              </button>
              <ReadButton text={model.lines[lineIndex] ?? model.exactText} />
            </div>
          </div>
        ) : (
          <div className="wi-honesty-panel">
            <BookOpen size={22} />
            <div>
              <strong>Stay with the printed crop.</strong>
              <p>Read only the first instruction or line. When it feels settled, move to the next step.</p>
            </div>
          </div>
        );
      case 'job':
        return model.command ? (
          <div className="wi-command-layout">
            <div className="wi-command-word">{model.command.surface}</div>
            <div className="wi-command-copy">
              <p className="wi-eyebrow">What it asks you to do</p>
              <h3>{model.command.requiredAction}</h3>
              <div className="wi-rule" />
              <p><strong>Useful shape:</strong> {model.command.answerShape}</p>
              <p><strong>Watch for:</strong> {model.command.commonTrap}</p>
            </div>
          </div>
        ) : (
          <div className="wi-honesty-panel">
            <Eye size={22} />
            <div>
              <strong>No command word was safely detected.</strong>
              <p>Look at the exact question and underline the verb that tells you what to produce. Ways In will not invent one.</p>
            </div>
          </div>
        );
      case 'boundaries':
        return (
          <div className="wi-two-column">
            <section>
              <p className="wi-eyebrow">What the question gives you</p>
              <h3>Givens</h3>
              {model.givens.length ? (
                <ul className="wi-clean-list">{model.givens.map(item => <li key={item}>{item}</li>)}</ul>
              ) : <p className="wi-muted-copy">No separate data or lead-in was safely detected. The knowledge comes from you.</p>}
            </section>
            <section>
              <p className="wi-eyebrow">What your answer must respect</p>
              <h3>Boundaries</h3>
              {model.constraints.length ? (
                <ul className="wi-clean-list">{model.constraints.map(item => <li key={item}>{item}</li>)}</ul>
              ) : <p className="wi-muted-copy">No extra limit was safely detected. Keep the exact wording in view.</p>}
            </section>
          </div>
        );
      case 'shape':
        return (
          <div>
            <div className="wi-shape-heading">
              <div>
                <p className="wi-eyebrow">An empty frame—not an answer</p>
                <h3>{model.expectedPoints} distinct {model.expectedPoints === 1 ? 'space' : 'spaces'} to think into</h3>
              </div>
              {source.answerShape?.totalMarks && <span>{source.answerShape.totalMarks} marks</span>}
            </div>
            <EmptySlots count={model.expectedPoints} />
            {source.answerShape?.choice && (
              <p className="wi-fine-print">The paper offers {source.answerShape.choice.available}; plan only the {source.answerShape.choice.answer} you will answer.</p>
            )}
            {source.answerShape?.alternativeRoutes && (
              <p className="wi-fine-print">The official scheme allows alternative complete routes. Choose one route and keep it internally consistent.</p>
            )}
          </div>
        );
      case 'attempt':
        return (
          <div>
            <label className="wi-draft-label" htmlFor={`wi-draft-${source.id}`}>
              <span>Your attempt</span>
              <span>{draft.trim() ? draft.trim().split(/\s+/).length : 0} words · saved on this device</span>
            </label>
            <textarea
              id={`wi-draft-${source.id}`}
              aria-label="Your attempt"
              className="wi-draft"
              value={draft}
              onChange={event => onDraft(event.target.value)}
              placeholder="Start with the first idea. It does not need to be polished."
            />
            <p className="wi-fine-print">Ways In does not compare this draft with the marking scheme. Return to the question to reveal and self-mark it normally.</p>
          </div>
        );
      case 'return': {
        const labels = [
          model.command ? `My answer does the job: ${model.command.surface}.` : 'My answer does the job named in the original question.',
          model.constraints.length ? 'I respected the number, source and limits printed in the question.' : 'I checked the exact wording for any limit I may have missed.',
          `I can see ${model.expectedPoints} distinct ${model.expectedPoints === 1 ? 'idea' : 'ideas'} in my response.`,
        ];
        return (
          <div>
            <div className="wi-return-checks">
              {labels.map((label, index) => (
                <button
                  type="button"
                  key={label}
                  onClick={() => setChecks(values => values.map((value, i) => i === index ? !value : value))}
                  className={checks[index] ? 'is-checked' : ''}
                  aria-pressed={checks[index]}
                >
                  <span>{checks[index] && <Check size={16} />}</span>
                  {label}
                </button>
              ))}
            </div>
            <button type="button" className="wi-primary wi-return-button" disabled={!allChecked} onClick={onReturn}>
              Return to the original question <ArrowRight size={17} />
            </button>
          </div>
        );
      }
    }
  })();

  return (
    <section className="wi-mode-panel" aria-labelledby="wi-step-title">
      <div className="wi-step-progress" aria-label={`Step ${stepIndex + 1} of ${model.steps.length}`}>
        {model.steps.map((item, index) => (
          <button
            type="button"
            key={item.id}
            className={index === stepIndex ? 'is-current' : index < stepIndex ? 'is-done' : ''}
            onClick={() => onStepIndex(index)}
            aria-label={`Go to step ${index + 1}: ${item.title}`}
          />
        ))}
      </div>
      <p className="wi-eyebrow">{step.eyebrow} · {stepIndex + 1} of {model.steps.length}</p>
      <h2 id="wi-step-title" className="wi-mode-title" tabIndex={-1}>{step.title}</h2>
      <p className="wi-mode-intro">{step.prompt}</p>
      <div className="wi-step-body">{body}</div>
      {step.id !== 'return' && (
        <div className="wi-step-nav">
          <button type="button" className="wi-secondary" disabled={stepIndex === 0} onClick={() => onStepIndex(Math.max(0, stepIndex - 1))}>
            <ArrowLeft size={16} /> Back
          </button>
          <button type="button" className="wi-primary" onClick={() => onStepIndex(Math.min(model.steps.length - 1, stepIndex + 1))}>
            {step.id === 'attempt' ? 'Check against the question' : 'That part is clear'} <ArrowRight size={16} />
          </button>
        </div>
      )}
    </section>
  );
};

type VisualView = 'map' | 'shape' | 'colours';

const ShowMeView: React.FC<{
  source: WaysInQuestionSource;
  model: WaysInQuestionModel;
  slotNotes: string[];
  onSlotNote: (index: number, value: string) => void;
  onUseSteps: (step?: number) => void;
}> = ({ source, model, slotNotes, onSlotNote, onUseSteps }) => {
  const [view, setView] = useState<VisualView>('map');
  const [selectedNode, setSelectedNode] = useState(0);
  const nodes = [
    {
      label: 'Start with',
      title: model.givens.length ? 'What is given' : 'Your subject knowledge',
      detail: model.givens[0] ?? 'The question supplies no separate data that could be safely extracted.',
    },
    {
      label: 'Your job',
      title: model.command?.surface ?? 'Find the command',
      detail: model.command?.requiredAction ?? 'Use the exact paper to identify the action word. It was not safely detectable in searchable text.',
    },
    {
      label: 'Build',
      title: `${model.expectedPoints} ${model.expectedPoints === 1 ? 'answer idea' : 'answer ideas'}`,
      detail: source.answerShape?.choice
        ? `Choose ${source.answerShape.choice.answer} from ${source.answerShape.choice.available} available parts.`
        : 'Keep each answer idea distinct so one point does not hide another.',
    },
    {
      label: 'Finish by',
      title: 'Returning to the wording',
      detail: model.constraints[0] ?? 'Check the original question for a number, source, comparison or limit.',
    },
  ];

  return (
    <section className="wi-mode-panel" aria-labelledby="wi-show-title">
      <p className="wi-eyebrow">A visual route through the task</p>
      <h2 id="wi-show-title" className="wi-mode-title" tabIndex={-1}>See the shape before you answer.</h2>
      <p className="wi-mode-intro">These views map the task—not the answer. The official marking points stay closed.</p>
      <div className="wi-view-tabs" role="tablist" aria-label="Visual views">
        {([
          ['map', 'Task map', Layers3],
          ['shape', 'Answer shape', Eye],
          ['colours', 'Question colours', BookOpen],
        ] as const).map(([id, label, Icon]) => (
          <button type="button" role="tab" aria-selected={view === id} key={id} className={view === id ? 'is-active' : ''} onClick={() => setView(id)}>
            <Icon size={16} /> {label}
          </button>
        ))}
      </div>

      {view === 'map' && (
        <div className="wi-visual-stage">
          <div className="wi-task-map" role="list" aria-label="Question task map">
            {nodes.map((node, index) => (
              <React.Fragment key={node.label}>
                <div role="listitem">
                  <button
                    type="button"
                    className={selectedNode === index ? 'is-selected' : ''}
                    onClick={() => setSelectedNode(index)}
                    aria-pressed={selectedNode === index}
                  >
                    <span>{String(index + 1).padStart(2, '0')} · {node.label}</span>
                    <strong>{node.title}</strong>
                  </button>
                </div>
                {index < nodes.length - 1 && <ArrowRight className="wi-map-arrow" size={18} aria-hidden="true" />}
              </React.Fragment>
            ))}
          </div>
          <div className="wi-node-detail" aria-live="polite">
            <p className="wi-eyebrow">{nodes[selectedNode].label}</p>
            <h3>{nodes[selectedNode].title}</h3>
            <p>{nodes[selectedNode].detail}</p>
          </div>
          {model.keywords.length > 0 && (
            <div className="wi-keyword-orbit" aria-label="Topic words found in the question">
              <span>Topic</span>
              {model.keywords.map(word => <i key={word}>{word}</i>)}
            </div>
          )}
        </div>
      )}

      {view === 'shape' && (
        <div className="wi-visual-stage">
          <div className="wi-shape-heading">
            <div>
              <p className="wi-eyebrow">Plan without revealing</p>
              <h3>Give every answer idea somewhere to go.</h3>
            </div>
            {source.answerShape?.totalMarks && <span>{source.answerShape.totalMarks} marks</span>}
          </div>
          <EmptySlots count={model.expectedPoints} notes={slotNotes} onNote={onSlotNote} editable />
          <p className="wi-fine-print">The number of spaces comes from the tariff shape. Their contents come from you.</p>
          <button type="button" className="wi-primary wi-inline-primary" onClick={() => onUseSteps(4)}>
            Write the attempt one step at a time <ArrowRight size={16} />
          </button>
        </div>
      )}

      {view === 'colours' && (
        <div className="wi-visual-stage">
          <div className="wi-legend" aria-label="Question colour key">
            {(['action', 'constraint', 'data'] as QuestionHighlightKind[]).map(kind => (
              <span key={kind}><i className={`wi-legend-dot wi-legend-dot--${kind}`} />{highlightLabel[kind]}</span>
            ))}
          </div>
          <div className="wi-colour-question">
            <ExactQuestion model={model} annotated />
          </div>
          {model.highlights.length === 0 && (
            <p className="wi-muted-copy">No wording was highlighted because the source did not contain enough reliable searchable text. Use the original crop beside you.</p>
          )}
          <div className="wi-colour-explanations">
            <div><span className="wi-legend-dot wi-legend-dot--action" /><strong>The job</strong><p>What kind of thinking or output the question demands.</p></div>
            <div><span className="wi-legend-dot wi-legend-dot--constraint" /><strong>Boundary</strong><p>A number, source or condition your answer must obey.</p></div>
            <div><span className="wi-legend-dot wi-legend-dot--data" /><strong>Given data</strong><p>Information already supplied; do not spend memory trying to recreate it.</p></div>
          </div>
        </div>
      )}
    </section>
  );
};

const ModeChooser: React.FC<{ source: WaysInQuestionSource; onChoose: (mode: WaysInMode) => void }> = ({ source, onChoose }) => (
  <section className="wi-mode-chooser">
    <p className="wi-eyebrow">Choose the kind of help—not a label</p>
    <h1>Find a way into this question.</h1>
    <p>The original stays beside you. Neither route reveals the marking scheme or changes what the question asks.</p>
    <div className="wi-choice-grid">
      <button type="button" onClick={() => onChoose('one-step')}>
        <span className="wi-choice-number">01</span>
        <div className="wi-choice-art wi-choice-art--steps" aria-hidden="true"><i /><i /><i /><i /></div>
        <p className="wi-eyebrow">Reduce what is on screen</p>
        <h2>One step at a time</h2>
        <p>Read, decode, plan, attempt and return to the original—one deliberate action at a time.</p>
        <strong>Start step by step <ArrowRight size={16} /></strong>
      </button>
      <button type="button" onClick={() => onChoose('show-me')}>
        <span className="wi-choice-number">02</span>
        <div className="wi-choice-art wi-choice-art--map" aria-hidden="true"><i /><i /><i /></div>
        <p className="wi-eyebrow">Make the structure visible</p>
        <h2>Show me</h2>
        <p>See the job, constraints and answer shape as a task map—without being shown the answer.</p>
        <strong>Open the visual map <ArrowRight size={16} /></strong>
      </button>
    </div>
    <p className="wi-source-promise">Working from {source.sourceLabel}. Exact wording remains available throughout.</p>
  </section>
);

export const WaysInWorkspace: React.FC<WaysInWorkspaceProps> = ({
  source,
  originalPreview,
  initialMode = null,
  onClose,
}) => {
  const model = useMemo(() => buildQuestionModel(source), [source]);
  const storageKey = `nextstepuni:ways-in:${source.id}`;
  const initialSaved = useMemo(() => safeSavedWork(storageKey), [storageKey]);
  const [mode, setMode] = useState<WaysInMode | null>(initialMode);
  const [stepIndex, setStepIndex] = useState(0);
  const [draft, setDraft] = useState(initialSaved.draft);
  const [slotNotes, setSlotNotes] = useState(initialSaved.slotNotes);
  const [mobileOriginal, setMobileOriginal] = useState(false);
  const closeRef = useRef<HTMLButtonElement | null>(null);
  const shellRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    const before = document.body.style.overflow;
    const previouslyFocused = document.activeElement instanceof HTMLElement ? document.activeElement : null;
    document.body.style.overflow = 'hidden';
    closeRef.current?.focus();
    const onKey = (event: KeyboardEvent) => {
      if (event.key === 'Escape') onClose();
      if (event.key !== 'Tab' || !shellRef.current) return;
      const focusable = Array.from(shellRef.current.querySelectorAll<HTMLElement>(
        'button:not([disabled]), [href], input:not([disabled]), textarea:not([disabled]), select:not([disabled]), [tabindex]:not([tabindex="-1"])',
      )).filter(element => element.offsetParent !== null);
      if (!focusable.length) return;
      const first = focusable[0];
      const last = focusable[focusable.length - 1];
      if (event.shiftKey && document.activeElement === first) {
        event.preventDefault();
        last.focus();
      } else if (!event.shiftKey && document.activeElement === last) {
        event.preventDefault();
        first.focus();
      }
    };
    window.addEventListener('keydown', onKey);
    return () => {
      document.body.style.overflow = before;
      window.removeEventListener('keydown', onKey);
      previouslyFocused?.focus();
    };
  }, [onClose]);

  useEffect(() => {
    try {
      window.localStorage.setItem(storageKey, JSON.stringify({ draft, slotNotes } satisfies SavedWork));
    } catch {
      // Storage can be unavailable in private browsing; the active draft still works.
    }
  }, [storageKey, draft, slotNotes]);

  const selectMode = (next: WaysInMode) => {
    setMode(next);
    setMobileOriginal(false);
    requestAnimationFrame(() => document.querySelector<HTMLElement>('.wi-mode-title')?.focus?.());
  };

  const clearWork = () => {
    setDraft('');
    setSlotNotes([]);
    try { window.localStorage.removeItem(storageKey); } catch { /* no-op */ }
  };

  const shell = (
    <div ref={shellRef} className="ways-in-shell" role="dialog" aria-modal="true" aria-label={`Ways In for ${source.questionRef}`}>
      <header className="wi-topbar">
        <div className="wi-topbar-inner">
          <button ref={closeRef} type="button" onClick={onClose} className="wi-close">
            <X size={18} /> <span>Close</span>
          </button>
          <div className="wi-brand">
            <span>Ways In</span>
            <small>{source.subjectLabel} · {source.questionRef}</small>
          </div>
          <div className="wi-top-actions">
            <button type="button" className="wi-mobile-original" onClick={() => setMobileOriginal(value => !value)} aria-expanded={mobileOriginal}>
              <BookOpen size={16} /> Original
            </button>
            {(draft || slotNotes.some(Boolean)) && (
              <button type="button" onClick={clearWork} className="wi-reset" title="Clear the saved draft and plan">
                <RotateCcw size={15} /> <span>Clear work</span>
              </button>
            )}
          </div>
        </div>
      </header>

      {mobileOriginal && (
        <div className="wi-mobile-source">
          <SourceSheet source={source} model={model} preview={originalPreview} compact />
        </div>
      )}

      <main className="wi-workspace">
        <aside className="wi-source-column">
          <SourceSheet source={source} model={model} preview={originalPreview} />
        </aside>
        <div className="wi-support-column">
          {mode && (
            <div className="wi-mode-switch" role="group" aria-label="Ways In mode">
              {(Object.keys(modeLabel) as WaysInMode[]).map(item => (
                <button type="button" key={item} className={mode === item ? 'is-active' : ''} onClick={() => selectMode(item)}>
                  {modeLabel[item]}
                </button>
              ))}
            </div>
          )}
          {!mode ? (
            <ModeChooser source={source} onChoose={selectMode} />
          ) : mode === 'one-step' ? (
            <OneStepView
              source={source}
              model={model}
              stepIndex={stepIndex}
              onStepIndex={setStepIndex}
              draft={draft}
              onDraft={setDraft}
              onReturn={onClose}
            />
          ) : (
            <ShowMeView
              source={source}
              model={model}
              slotNotes={slotNotes}
              onSlotNote={(index, value) => setSlotNotes(current => {
                const next = [...current];
                next[index] = value;
                return next;
              })}
              onUseSteps={(step = 0) => { setStepIndex(step); selectMode('one-step'); }}
            />
          )}
        </div>
      </main>
    </div>
  );

  return typeof document === 'undefined' ? null : createPortal(shell, document.body);
};

export default WaysInWorkspace;
