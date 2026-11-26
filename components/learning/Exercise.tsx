/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The pieces an exercise in a module is made of (area 5b of the design build; the boards
 * c-read-flow, c-read-choices and c-read-write, agreed 26 Nov 2026). Built from the shared
 * parts: ChoiceTile (an answer you choose), AreaField / Field (an answer you write),
 * PressBox (a card you press to turn it over), PaperSheet's look (the one lifted sheet).
 *
 *   <ExerciseSheet title="Control Panel" sub="Scenario: You fail a test. …">
 *     <AnswerGroup kind="several" count>
 *       <ChoiceTile kind="several" chosen={on} label="I didn't use the right study method."
 *         note={on ? '(CONTROLLABLE)' : undefined} onClick={toggle} />
 *     </AnswerGroup>
 *   </ExerciseSheet>
 *   <AnswerLine><b>Reframe complete.</b> You've opened up the possibility of future growth.</AnswerLine>
 *   <RevealCard revealed={on} onPress={flip} before="…" after="…" hint="Tap to reframe" done="Reframed" />
 *
 * The words are always the module's own: a piece adds no words of its own, except the
 * count of chosen answers ("2 of 4 chosen"), and only where a screen asks for it.
 * Every answer line is ink with a green tick beside it; green is never used for a
 * sentence (Alex, 26 Nov 2026). No mint, coral, peach or orange fill on an answer: what
 * is chosen has an ink outline and a tick that draws. On a phone the sheet is lifted, with
 * two tilted sheets behind it; on a laptop the step is already on a sheet, so the
 * exercise lies flat on it under a hairline (no sheet on a sheet).
 */
import { createContext, useContext, useId, useLayoutEffect, useRef, useState, type KeyboardEvent, type ReactNode } from 'react';
import { RotateCcw } from 'lucide-react';
import { AnswerTick } from '../ui/Choice';
import { PressBox } from '../ui/List';
import '../ui/parts.css';
import './exercise.css';

export { AnswerTick };

/** The id of the exercise's title, so a group of answers inside it is named by it. */
const ExerciseTitle = createContext<string | undefined>(undefined);

type HeadingLevel = 3 | 4 | 5;

interface HeadProps {
  /** A small capitals label over the title: the module's own label, if it has one. */
  label?: ReactNode;
  title?: ReactNode;
  /** The line under the title that says what to do. */
  sub?: ReactNode;
  titleId: string;
  level: HeadingLevel;
}

function ExerciseHead({ label, title, sub, titleId, level }: HeadProps) {
  if (!label && !title && !sub) return null;
  const Title = `h${level}` as 'h3' | 'h4' | 'h5';
  return (
    <div className="ex-head">
      {label ? <p className="ex-label">{label}</p> : null}
      {title ? <Title id={titleId} className="ex-title">{title}</Title> : null}
      {sub ? <p className="ex-sub">{sub}</p> : null}
    </div>
  );
}

export interface ExerciseSheetProps {
  label?: ReactNode;
  title?: ReactNode;
  sub?: ReactNode;
  children?: ReactNode;
  /** The title's heading level. Default 4, as the modules' exercises have always used. */
  level?: HeadingLevel;
  className?: string;
  /** Hooks a module's own styling or a test kept on the old wrapper (`data-wide`). */
  name?: string;
}

/** The one lifted sheet an exercise sits on: its label, its title, the line that says
 *  what to do, then the exercise. */
export function ExerciseSheet({ label, title, sub, children, level = 4, className = '', name }: ExerciseSheetProps) {
  const titleId = useId();
  return (
    <section className={`ui-part ex-sheet ${className}`.trim()} aria-labelledby={title ? titleId : undefined} data-exercise={name}>
      <div className="ex-sheet-face">
        <ExerciseHead label={label} title={title} sub={sub} titleId={titleId} level={level} />
        <ExerciseTitle.Provider value={title ? titleId : undefined}>{children}</ExerciseTitle.Provider>
      </div>
    </section>
  );
}

/** A second exercise on the same sheet (a step with two exercises shares one sheet),
 *  under a hairline, with its own title. */
export function ExercisePart({ label, title, sub, children, level = 4, className = '' }: Omit<ExerciseSheetProps, 'name'>) {
  const titleId = useId();
  return (
    <div className={`ex-part ${className}`.trim()}>
      <ExerciseHead label={label} title={title} sub={sub} titleId={titleId} level={level} />
      <ExerciseTitle.Provider value={title ? titleId : undefined}>{children}</ExerciseTitle.Provider>
    </div>
  );
}

/** A small capitals label for a module's own label inside an exercise (where today it
 *  is a tinted pill). */
export function ExerciseLabel({ children, className = '' }: { children: ReactNode; className?: string }) {
  return <p className={`ex-label ${className}`.trim()}>{children}</p>;
}

export interface AnswerGroupProps {
  /** one: a radio group (a round mark); several: a group of checkboxes (a square mark). */
  kind?: 'one' | 'several';
  /** The question, above the answers, in the module's own words. */
  legend?: ReactNode;
  /** The group's accessible name when it has no legend and sits outside a titled sheet. */
  label?: string;
  /** "2 of 4 chosen" at the right of the legend: counted from the answers marked chosen. */
  count?: boolean;
  /** Two columns of tiles (a module's pair of answers side by side). */
  columns?: 1 | 2;
  /** Arrow keys move between the answers. In a one-of group they also choose, as radios
   *  do; leave this off where choosing an answer locks it in (a quiz that marks you). */
  chooseOnArrow?: boolean;
  children: ReactNode;
  className?: string;
}

const ANSWERS = '[role="radio"], [role="checkbox"]';

/** A question's answers: a white box with a line for each, chosen = an ink outline and
 *  the drawn tick. Arrow keys move within the group; Home and End jump to its ends. */
export function AnswerGroup({ kind = 'one', legend, label, count = false, columns = 1, chooseOnArrow = kind === 'one', children, className = '' }: AnswerGroupProps) {
  const listRef = useRef<HTMLDivElement>(null);
  const legendId = useId();
  const titleId = useContext(ExerciseTitle);
  const answers = () => [...(listRef.current?.querySelectorAll<HTMLButtonElement>(ANSWERS) ?? [])]
    .filter(el => el.closest('[data-answer-group]') === listRef.current && !el.disabled);
  const onKeyDown = (event: KeyboardEvent<HTMLDivElement>) => {
    const items = answers();
    const at = items.indexOf((event.target as HTMLElement).closest<HTMLButtonElement>(ANSWERS) as HTMLButtonElement);
    if (at < 0) return;
    const step = event.key === 'ArrowDown' || event.key === 'ArrowRight' ? 1 : event.key === 'ArrowUp' || event.key === 'ArrowLeft' ? -1 : 0;
    let next = step ? (at + step + items.length) % items.length : at;
    if (event.key === 'Home') next = 0;
    if (event.key === 'End') next = items.length - 1;
    if (next === at) return;
    event.preventDefault();
    items[next].focus();
    if (chooseOnArrow && items[next].getAttribute('aria-checked') !== 'true') items[next].click();
  };
  // The count is read from the answers themselves after each render, so it never needs
  // the module's own state.
  const [chosen, setChosen] = useState<[number, number]>([0, 0]);
  useLayoutEffect(() => {
    if (!count) return;
    const items = [...(listRef.current?.querySelectorAll<HTMLButtonElement>(ANSWERS) ?? [])].filter(el => el.closest('[data-answer-group]') === listRef.current);
    const next: [number, number] = [items.filter(el => el.getAttribute('aria-checked') === 'true').length, items.length];
    setChosen(prev => (prev[0] === next[0] && prev[1] === next[1] ? prev : next));
  });
  const named = legend ? legendId : undefined;
  return (
    <div className={`ex-group ${className}`.trim()}>
      {legend || count ? (
        <div className="ui-choices-head ex-group-head">
          {legend ? <p id={legendId} className="ui-choices-legend">{legend}</p> : <span />}
          {count ? <span className="ui-choices-count ui-readout" aria-live="polite">{`${chosen[0]} of ${chosen[1]} chosen`}</span> : null}
        </div>
      ) : null}
      <div
        ref={listRef}
        data-answer-group=""
        role={kind === 'one' ? 'radiogroup' : 'group'}
        aria-labelledby={named ?? (label ? undefined : titleId)}
        aria-label={named ? undefined : label}
        className={columns === 2 ? 'ui-choices ui-choices--tiles' : 'ui-choices'}
        onKeyDown={onKeyDown}
      >
        {children}
      </div>
    </div>
  );
}

export interface AnswerLineProps {
  children: ReactNode;
  /** ok: the green tick beside the words (right, complete, done); note: the words alone. */
  tone?: 'ok' | 'note';
  className?: string;
  /** Announce the line when it appears. */
  live?: boolean;
}

/** A line that answers what the student did: ink words; the tick beside them is the only
 *  green. Never a tinted panel. */
export function AnswerLine({ children, tone = 'ok', className = '', live = false }: AnswerLineProps) {
  return (
    <p className={`ex-line${tone === 'ok' ? ' ex-line--ok' : ''} ${className}`.trim()} aria-live={live ? 'polite' : undefined}>
      {tone === 'ok' ? <AnswerTick className="ex-line-tick" /> : null}
      <span className="ex-line-words">{children}</span>
    </p>
  );
}

export interface RevealCardProps {
  revealed: boolean;
  onPress: () => void;
  /** What the card shows first (the module's own words). */
  before: ReactNode;
  /** What it turns into. */
  after: ReactNode;
  /** Keep the first words, struck through and small, above the new ones once turned (the
   *  agreed drill). Off: the first words give way to the new ones, as some modules do. */
  keepBefore?: boolean;
  /** The line that says it can be pressed ("Tap to reframe"), in the module's words. */
  hint?: ReactNode;
  /** The line once it is turned ("Reframed"), with the green tick. */
  done?: ReactNode;
  /** The card turns back when pressed again (the turn-over mark is shown). Off for a card
   *  that turns once. */
  toggles?: boolean;
  className?: string;
}

/** A card you press to turn it over: a white box with a line; turned, its words are ink,
 *  with no orange or green panel. */
export function RevealCard({ revealed, onPress, before, after, keepBefore = true, hint, done, toggles = true, className = '' }: RevealCardProps) {
  return (
    <PressBox pressed={revealed} onPress={onPress} className={`ex-reveal${revealed ? ' ex-reveal--on' : ''} ${className}`.trim()}>
      <span className="ex-reveal-body">
        {!revealed || keepBefore ? <span className="ex-reveal-before">{before}</span> : null}
        {revealed ? <span className="ex-reveal-after">{after}</span> : null}
        {revealed && done ? <span className="ex-reveal-state ex-reveal-state--done"><AnswerTick /><span>{done}</span></span>
          : !revealed && hint ? <span className="ex-reveal-state">{hint}</span> : null}
      </span>
      {toggles ? <RotateCcw className="ex-reveal-turn" width={20} height={20} strokeWidth={1.75} aria-hidden="true" focusable="false" /> : null}
    </PressBox>
  );
}
