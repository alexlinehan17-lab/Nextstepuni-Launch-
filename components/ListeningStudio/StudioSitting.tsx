/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * One sitting of a listening section: the recording on the charcoal ground,
 * one extract's questions at a time on the sheet, then every part marked
 * against its own scheme and saved to its own Mark Bank card.
 *
 * Marking is not re-implemented here. Each part mounts the Mark Bank reviewer
 * in its embedded mode (SessionScreen `embedded`), so a row, a menu, a rubric
 * or a language rule behaves exactly as it does in a review, and the result
 * handed to `onGrade` is the one a review would have recorded.
 */

import React, { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import { ArrowUpRight, Pause, Play } from 'lucide-react';
import SessionScreen, {
  listeningQuestionGroups, type EmbeddedAssessment, type SessionCardResult,
} from '../MarkBank/SessionScreen';
import FigureZoom from '../MarkBank/FigureZoom';
import SourceMaterialReader from '../MarkBank/SourceMaterialReader';
import { figureUrl } from '../../utils/figureUrl';
import { OverScreen } from '../ui/OverScreen';
import { PinnedFooter, TopBar } from '../ui/Bars';
import { Button, TextButton } from '../ui/Button';
import { Confirm } from '../ui/Sheet';
import { ToolArtwork } from '../launchpad/ToolMasthead';
import { useNativeStatusBarAppearance } from '../../hooks/useNativeStatusBarAppearance';
import {
  isNoSchemeCard, isUnpricedSectionCard, type CardSourceMaterial, type SecCard,
} from '../../types/markBank';
import { clock, useStudioAudio } from './useStudioAudio';
import { partLabel, type StudioSection } from './model';
import './listening-studio.css';

export interface StudioSittingProps {
  subjectLabel: string;
  /** "2025 Higher". */
  sittingLabel: string;
  section: StudioSection;
  /** The section that follows on the same paper, offered once this one is saved. */
  nextSectionTitle?: string;
  onNextSection?: () => void;
  /** Mark Bank's own recorder: one call per card, exactly as a review makes. */
  onGrade: (result: SessionCardResult) => string | void;
  onClose: () => void;
}

const RING = 2 * Math.PI * 76;
const noop = () => {};
const marksText = (marks: number) => `${marks} ${marks === 1 ? 'mark' : 'marks'}`;
// A diagram card has no question figure of its own; the others may.
const questionFigureOf = (card: SecCard) => ('questionFigure' in card ? card.questionFigure : undefined);
const figureOf = (card: SecCard) => ('figure' in card ? card.figure : undefined);
const printedQuestion = (card: SecCard) => {
  const figure = questionFigureOf(card);
  return figure && figure.includesPrompt !== false ? figure : null;
};
const showsMarks = (card: SecCard) =>
  card.totalMarks > 0 && !isNoSchemeCard(card) && !isUnpricedSectionCard(card);

const grow = (field: HTMLTextAreaElement | null) => {
  if (!field) return;
  field.style.height = 'auto';
  field.style.height = `${field.scrollHeight + 2}px`;
};

/** The question as the paper sets it: the SEC's own print where the card
 *  carries one (staves, grids), the typed wording otherwise. */
const PartQuestion: React.FC<{ card: SecCard }> = ({ card }) => {
  const printed = printedQuestion(card);
  const questionFigure = questionFigureOf(card);
  const figure = figureOf(card);
  // A scheme's worked solution is held back until marking, as it is in a review.
  const illustration = questionFigure && !printed ? questionFigure : figure && !figure.solution ? figure : null;
  const groups = card.subjectId === 'irish' ? listeningQuestionGroups(card.questionText) : [];
  const prompts = groups.reduce((count, group) => count + group.prompts.length, 0);
  const text = card.questionChoices ? card.questionText.split('\n')[0] : card.questionText;
  return (
    <>
      {printed ? (
        <figure className="ls-figure">
          <FigureZoom
            src={figureUrl(printed.src)} alt={printed.alt} kicker="Printed question" caption={printed.attribution}
            imgStyle={{ maxWidth: '100%', maxHeight: 620, objectFit: 'contain', display: 'block' }}
            captionStyle={{ marginTop: 6, font: "400 11px/1.4 'DM Sans', system-ui, sans-serif", color: 'var(--mb-label)' }}
          />
        </figure>
      ) : prompts > 1 ? (
        groups.map((group, groupIndex) => (
          <React.Fragment key={`${group.label ?? 'prompts'}-${groupIndex}`}>
            {group.label && <p className="ls-prompt-group">{group.label}</p>}
            {group.instruction && <p className="ls-prompt-group">{group.instruction}</p>}
            <ol className="ls-prompts">
              {group.prompts.map((prompt, promptIndex) => (
                <li key={`${prompt.label}-${promptIndex}`}><span>{prompt.label}</span><span>{prompt.text}</span></li>
              ))}
            </ol>
          </React.Fragment>
        ))
      ) : (
        <p className="ls-part-q">{text}</p>
      )}
      {card.practiceFocus && <p className="ls-part-q">Practise: {card.practiceFocus}</p>}
      {illustration && (
        <figure className="ls-figure">
          <FigureZoom
            src={figureUrl(illustration.src)} alt={illustration.alt} kicker="Figure" caption={illustration.attribution}
            imgStyle={{ maxWidth: '100%', maxHeight: 520, objectFit: 'contain', display: 'block' }}
            captionStyle={{ marginTop: 6, font: "400 11px/1.4 'DM Sans', system-ui, sans-serif", color: 'var(--mb-label)' }}
          />
        </figure>
      )}
    </>
  );
};

/** The booklet pages behind an extract, each once however many parts cite it. */
const extractSources = (cards: SecCard[]) => {
  const seen = new Map<string, { source: CardSourceMaterial; card: SecCard; fileid: string }>();
  for (const card of cards) {
    for (const source of [card.sourceMaterial, ...(card.additionalSourceMaterials ?? [])]) {
      const fileid = source?.sourceFileid ?? card.paperFileid;
      if (!source || !fileid) continue;
      const key = `${fileid}:${source.kind}:${source.pages.join(',')}`;
      if (!seen.has(key)) seen.set(key, { source, card, fileid });
    }
  }
  return [...seen.entries()];
};

const StudioSitting: React.FC<StudioSittingProps> = ({
  subjectLabel, sittingLabel, section, nextSectionTitle, onNextSection, onGrade, onClose,
}) => {
  useNativeStatusBarAppearance('dark');
  const sheetRef = useRef<HTMLElement | null>(null);
  const [mode, setMode] = useState<'sit' | 'mark' | 'saved'>('sit');
  const [index, setIndex] = useState(0);
  const [drafts, setDrafts] = useState<Record<string, string>>({});
  const [assessments, setAssessments] = useState<Record<string, EmbeddedAssessment>>({});
  const [savedCount, setSavedCount] = useState(0);
  const [confirmLeave, setConfirmLeave] = useState(false);

  const extracts = section.extracts;
  const extract = extracts[Math.min(index, extracts.length - 1)];
  const cards = section.cards;
  const audio = useStudioAudio(extract.audio);
  const singles = useMemo(() => new Map(cards.map(card => [card.id, [card]])), [cards]);
  const answered = cards.filter(card => (drafts[card.id] ?? '').trim()).length;
  const unsavedWork = mode !== 'saved' && (answered > 0 || Object.values(assessments).some(a => a.touched));

  const requestClose = useCallback(() => {
    if (unsavedWork) setConfirmLeave(true); else onClose();
  }, [unsavedWork, onClose]);

  const onAssessment = useCallback((next: EmbeddedAssessment) => {
    setAssessments(previous => {
      const before = previous[next.cardId];
      return before && before.grade === next.grade && before.marksClaimed === next.marksClaimed
        && before.marksAvailable === next.marksAvailable && before.touched === next.touched
        ? previous : { ...previous, [next.cardId]: next };
    });
  }, []);
  const embedded = useMemo(() => ({ onAssessment, locked: mode === 'saved' }), [onAssessment, mode]);

  // A new extract or a new view starts at the top of the sheet.
  useEffect(() => { sheetRef.current?.scrollTo?.({ top: 0 }); }, [index, mode]);

  const goTo = (next: number) => { setIndex(Math.max(0, Math.min(extracts.length - 1, next))); setConfirmLeave(false); };
  const startMarking = () => { audio.pause(); setMode('mark'); };

  // A part is recorded once the student has typed an answer for it or touched
  // its scheme. One they never reached stays unrecorded, not marked as missed.
  const recordable = cards.filter(card => assessments[card.id]
    && (assessments[card.id].touched || (drafts[card.id] ?? '').trim()));
  const save = () => {
    for (const card of recordable) {
      const result = assessments[card.id];
      onGrade({
        cardId: result.cardId, grade: result.grade,
        marksClaimed: result.marksClaimed, marksAvailable: result.marksAvailable,
      });
    }
    setSavedCount(recordable.length);
    setMode('saved');
  };

  const claimed = cards.reduce((sum, card) => sum + (assessments[card.id]?.marksClaimed ?? 0), 0);
  const available = cards.reduce((sum, card) => sum + (assessments[card.id]?.marksAvailable ?? 0), 0);
  const unscored = cards.filter(card => assessments[card.id] && assessments[card.id].marksAvailable === 0).length;
  const played = audio.duration > 0 ? Math.min(1, audio.time / audio.duration) : 0;
  const extractMarks = extract.cards.reduce((sum, card) => sum + (showsMarks(card) ? card.totalMarks : 0), 0);
  const stems = [...new Set(extract.cards.map(card => card.stem?.trim()).filter((stem): stem is string => Boolean(stem)))];
  const citations = [...new Set(cards.map(card => card.schemeCitation))];
  const partNumber = (card: SecCard) => partLabel(card);
  const answerLabel = (card: SecCard) =>
    partNumber(card) ? `Your answer to part ${partNumber(card)}` : `Your answer: ${card.questionText.split('\n')[0].slice(0, 80)}`;

  const player = (
    <section className="ls7-player" aria-label="Recording">
      <p className="t-meta ls7-player-what">{subjectLabel} · {sittingLabel} · {section.title}</p>

      {/* The one recording element. It stays mounted through marking, so a
          student who goes back to their answers finds it where they left it. */}
      <audio {...audio.element} hidden />

      {mode === 'sit' ? (
        audio.playable && !audio.failed ? (
          <>
            <div className="ls7-deck">
              <div className="ls7-ring">
                <svg viewBox="0 0 168 168" aria-hidden="true">
                  <circle className="rt" cx="84" cy="84" r="76" />
                  <circle className="rp" cx="84" cy="84" r="76" strokeDasharray={RING} strokeDashoffset={RING * (1 - played)} />
                </svg>
                <button type="button" className="ls7-play" onClick={audio.toggle}
                  aria-label={audio.playing ? 'Pause the recording' : 'Play the recording'}>
                  {audio.playing
                    ? <Pause aria-hidden="true" fill="currentColor" strokeWidth={0} />
                    : <Play aria-hidden="true" fill="currentColor" strokeWidth={0} />}
                </button>
              </div>
              <div className="ls7-clock">
                <span className="ls7-time" aria-label={`Position ${clock(audio.time)}`}>{clock(audio.time)}</span>
                <span className="t-meta">{audio.duration > 0 ? `of ${clock(audio.duration)}, the whole listening test` : 'the whole listening test'}</span>
              </div>
            </div>
            <div className="ls7-seek">
              <input
                type="range" min={0} max={Math.max(audio.duration, 1)} step={1} value={Math.min(audio.time, Math.max(audio.duration, 1))}
                onChange={event => audio.seek(Number(event.target.value))}
                aria-label="Position in the recording" aria-valuetext={`${clock(audio.time)} of ${clock(audio.duration)}`}
                style={{ '--ls-played': `${played * 100}%` } as React.CSSProperties}
              />
            </div>
            <p className="t-meta ls7-wide-line">{extract.audio.title}</p>
            <p className="t-meta ls7-wide-line">This is the whole listening test. Move the bar to where this question starts.</p>
          </>
        ) : (
          <div className="ls7-norec">
            <p className="ls7-norec-t">
              {audio.playable ? 'This recording could not be loaded.' : 'This recording is not in the app yet.'}
            </p>
            <p className="t-sub">Open it on the SEC site in a new tab, then answer here.</p>
            <a className="ui-part ui-btn ui-btn--sm frame-hit ls7-out" href={extract.audio.canonicalUrl} target="_blank" rel="noreferrer">
              <span>Open the SEC recording</span><ArrowUpRight className="ui-icon" width={16} height={16} strokeWidth={2} aria-hidden="true" />
            </a>
          </div>
        )
      ) : (
        <div className="ls7-total">
          <span className="ls7-num" aria-label={`${claimed} of ${available} marks`}>{claimed}<small> / {available}</small></span>
          <p className="t-sub">
            Your marks for {section.title}.
            {unscored > 0 && ` ${unscored} ${unscored === 1 ? 'part is' : 'parts are'} checked without marks and ${unscored === 1 ? 'is' : 'are'} not in this total.`}
          </p>
        </div>
      )}

      {mode === 'sit' && extracts.length > 1 && extracts.length <= 4 && (
        <div className="ls7-extracts" role="group" aria-label="Extracts in this section">
          {extracts.map((item, itemIndex) => (
            <Button size="sm" key={item.key} aria-pressed={itemIndex === index} onClick={() => goTo(itemIndex)}>{item.title}</Button>
          ))}
        </div>
      )}
      {mode === 'sit' && audio.playable && !audio.failed && (
        <div className="ls7-skip">
          <Button size="sm" onClick={() => audio.skip(-10)}>Back 10s</Button>
          <Button size="sm" onClick={() => audio.skip(10)}>Forward 10s</Button>
        </div>
      )}
    </section>
  );

  const foot = (
    <div className="ls7-sit-foot">
      <PinnedFooter className="ls7-foot">
        {mode === 'sit' && <>
          {index < extracts.length - 1
            ? <Button kind="main" size="lg" block arrow="forward" onClick={() => goTo(index + 1)}>Next: {extracts[index + 1].title}</Button>
            : <Button kind="main" size="lg" block arrow="forward" onClick={startMarking}>Mark my answers</Button>}
          {index > 0 && <TextButton tone="quiet" className="ls7-foot-back" onClick={() => goTo(index - 1)}>Back: {extracts[index - 1].title}</TextButton>}
        </>}
        {mode === 'mark' && <>
          <Button kind="main" size="lg" block onClick={save} {...(recordable.length === 0 ? { 'aria-disabled': true as const, onClickCapture: (event: React.MouseEvent) => { event.preventDefault(); event.stopPropagation(); } } : {})}>
            Save {claimed} of {available} to Mark Bank
          </Button>
          <TextButton tone="quiet" className="ls7-foot-back" onClick={() => setMode('sit')}>Back to my answers</TextButton>
        </>}
        {mode === 'saved' && <>
          <p className="ls7-saved" role="status">
            Saved to Mark Bank: {savedCount} {savedCount === 1 ? 'part' : 'parts'}.
          </p>
          {onNextSection && nextSectionTitle && (
            <Button kind="main" size="lg" block arrow="forward" onClick={onNextSection}>Next: {nextSectionTitle}</Button>
          )}
          <TextButton tone="quiet" className="ls7-foot-back" onClick={onClose}>Back to the Studio</TextButton>
        </>}
      </PinnedFooter>
    </div>
  );

  const sitting = (
    <>
      <header className="ls-sh-head">
        <h2>{extract.title}</h2>
        {extract.piece && <p className="ls-piece">{extract.piece}</p>}
        <p>
          {extracts.length > 1 && `${index + 1} of ${extracts.length} · `}
          {extract.cards.length} {extract.cards.length === 1 ? 'part' : 'parts'}
          {extractMarks > 0 && ` · ${marksText(extractMarks)}`}
          {` · ${answered} of ${cards.length} answered`}
        </p>
      </header>
      {stems.map(stem => <p className="ls-stem" key={stem}>{stem}</p>)}
      {extractSources(extract.cards).length > 0 && (
        <div className="ls-readers">
          {extractSources(extract.cards).map(([key, { source, card, fileid }]) => (
            <SourceMaterialReader key={key} source={source} subjectId={card.subjectId} year={card.year} paperFileid={fileid} inline />
          ))}
        </div>
      )}
      {extract.cards.map(card => {
        const draft = drafts[card.id] ?? '';
        const setDraft = (value: string) => setDrafts(previous => ({ ...previous, [card.id]: value }));
        return (
          <div className="ls-part" key={card.id} data-testid="listening-studio-part">
            <div className="ls-part-id">{partNumber(card)}</div>
            <div className="ls-part-body">
              <PartQuestion card={card} />
              {card.questionChoices ? (
                <div className="ls-choices" role="radiogroup" aria-label={answerLabel(card)}>
                  {card.questionChoices.map(option => (
                    <button type="button" className="ls-choice" role="radio" key={option} aria-checked={draft === option}
                      onClick={() => setDraft(draft === option ? '' : option)}>
                      <i aria-hidden="true" /><span>{option}</span>
                    </button>
                  ))}
                </div>
              ) : (
                <textarea
                  className="ls-ans" rows={1} value={draft} placeholder="Write your answer"
                  aria-label={answerLabel(card)} ref={grow}
                  onChange={event => { setDraft(event.target.value); grow(event.target); }}
                />
              )}
            </div>
            <div className="ls-part-m">{showsMarks(card) ? marksText(card.totalMarks) : ''}</div>
          </div>
        );
      })}
    </>
  );

  const marking = (
    <>
      <header className="ls-sh-head">
        <h2>Your marks, part by part</h2>
        <p>Select what you got in each scheme. Each part saves to its own Mark Bank card.</p>
      </header>
      {extracts.map(item => (
        <React.Fragment key={item.key}>
          {extracts.length > 1 && <h3 className="ls-ex-h">{item.title}</h3>}
          {item.cards.map(card => {
            const draft = (drafts[card.id] ?? '').trim();
            const result = assessments[card.id];
            return (
              <div className="ls-mpart" key={card.id} data-testid="listening-studio-marking-part">
                <div className="ls-part-id">{partNumber(card)}</div>
                <div className="ls-part-body">
                  <PartQuestion card={card} />
                  <div className="ls-yours">
                    <span>Your answer</span>
                    <span className={draft ? undefined : 'is-empty'}>{draft || 'No answer written'}</span>
                  </div>
                  <SessionScreen
                    embedded={embedded} cards={singles.get(card.id) ?? [card]} subjectLabel={subjectLabel}
                    onGrade={noop} onExit={noop} onFinish={noop}
                  />
                </div>
                <div className="ls-part-m">
                  {result && result.marksAvailable > 0 ? <><b>{result.marksClaimed}</b> / {result.marksAvailable}</> : ''}
                </div>
              </div>
            );
          })}
        </React.Fragment>
      ))}
      {mode === 'mark' && recordable.length === 0 && (
        <p className="ls-note">Select what you got in a scheme, or go back and write an answer, and that part can be saved.</p>
      )}
      {citations.map(citation => <p className="ls-credit" key={citation}>{citation}</p>)}
    </>
  );

  return (
    <OverScreen label={`Listening Studio: ${subjectLabel} ${sittingLabel}, ${section.title}`} onEscape={requestClose} className="ls7-sit">
      <div className="ls7-sit-top">
        <TopBar tool leave={{ kind: 'back', onPress: requestClose, label: 'Leave this sitting' }} over="Sit a real listening" title="Listening Studio"
          art={<ToolArtwork tool="listening-studio" />} className="ls7-bar" />
        {player}
      </div>
      <section className="ls-sheet ls7-qsheet mark-bank-theme" aria-label="Questions" ref={sheetRef}>
        <div className="ls-col">{mode === 'sit' ? sitting : marking}</div>
      </section>
      {foot}
      <Confirm open={confirmLeave} sentence="Leave this sitting?" detail="Your answers here are not kept."
        keepLabel="Stay" onKeep={() => setConfirmLeave(false)} dangerLabel="Leave" onDanger={onClose} />
    </OverScreen>
  );
};

export default StudioSitting;
