/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * A quick check after a saved study session: a few real exam questions from
 * Mark Bank on what was just studied, marked by the student against the SEC
 * scheme. Students asked for exactly this (16 Oct 2026, twice; 23 Oct 2026).
 *
 * The questions and the marking points are lifted, never written: the stem is
 * the paper's and every row is the scheme's. The student answers first (in
 * their head or on paper), reveals the scheme, and ticks what they had — the
 * same self-marking Mark Bank uses, scored with the same rules, and each grade
 * is committed to the same spaced-repetition deck so the card comes back when
 * it should.
 *
 * It runs AFTER the session is saved, so nothing here can cost a student their
 * study time (the outbox that saves a session exists because it once did).
 */

import React, { useCallback, useEffect, useRef, useState } from 'react';
import { ArrowRight, ArrowUpRight, Check } from 'lucide-react';
import KobraScope, { Button, useSoundMuted } from '../../approved-ui-runtime';
import CrewIllustration from '../../CrewIllustration';
import { figureUrl } from '../../../utils/figureUrl';
import { ensureDeck, commitReview, memoryFor, readLocal } from '../../MarkBank/store';
import { grade as gradeCard, retentionFor } from '../../MarkBank/scheduler';
import { LEVEL_LABEL } from '../../MarkBank/deck';
import { useDeckSound } from '../../immersiveDeck/useDeckSound';
import type { MarkRow, SecQuestionCard } from '../../../types/markBank';
import type { StudyTopicSelection } from '../../../types/studyTopics';
import type { StudentSubject } from '../../subjectData';
import {
  EMPTY_ANSWER,
  cardMarks,
  loadQuiz,
  marksEarned,
  quizGrade,
  rowKey,
  type LoadedQuiz,
  type QuizAnswer,
  type QuizResult,
} from './studyQuizPlan';
import './study-quiz.css';

interface Props {
  uid: string;
  /** The session's subject as the student sees it, e.g. "Mathematics". */
  subject: string;
  topicSelection?: StudyTopicSelection;
  profileSubjects?: StudentSubject[];
  examDate?: string | null;
  character?: string;
  /** The quiz ran (or there was nothing to ask): carry on to the saved screen. */
  onDone: (results: QuizResult[]) => void;
  onSkip: () => void;
  now?: () => number;
}

/** A round ink marker, empty until the mark is earned (the study room's selection). */
function Mark() {
  return <span className="sq-mark" aria-hidden="true"><Check /></span>;
}

function tariffLine(group: NonNullable<MarkRow['group']>): string {
  const all = group.claimMax === group.options.length;
  const head = all ? `All ${group.claimMax} of these` : `Any ${group.claimMax} of these`;
  const marks = group.perOptionSteps
    ? `${group.perOptionSteps.slice(0, group.claimMax).join(' then ')} marks`
    : `${group.perOption} marks each`;
  return `${head} · ${marks}`;
}

export default function StudySessionQuiz({
  uid, subject, topicSelection, profileSubjects, examDate, character, onDone, onSkip, now = () => Date.now(),
}: Props) {
  const [quiz, setQuiz] = useState<LoadedQuiz | null | undefined>(undefined);
  const [index, setIndex] = useState(0);
  const [revealed, setRevealed] = useState(false);
  const [answer, setAnswer] = useState<QuizAnswer>(EMPTY_ANSWER);
  const [results, setResults] = useState<QuizResult[]>([]);
  const [finished, setFinished] = useState(false);
  const deckReady = useRef(false);
  const headingRef = useRef<HTMLHeadingElement>(null);
  // The deck's "complete" cue (four rising notes) marks the reveal — the one
  // moment the page changes state on the student's action. Alex's pick, 24 Oct
  // 2026, over the room's bloom. It honours the app's mute.
  const { play: playCue, setEnabled: setCueEnabled } = useDeckSound();
  const muted = useSoundMuted();
  useEffect(() => { setCueEnabled(!muted); }, [muted, setCueEnabled]);

  useEffect(() => {
    let live = true;
    setQuiz(undefined);
    loadQuiz({ subjectName: subject, topicSelection, profileSubjects, examDate, uid, now: now() })
      .then(loaded => { if (live) setQuiz(loaded); })
      .catch(() => { if (live) setQuiz(null); });
    return () => { live = false; };
    // The session is fixed once saved, so only its identity reloads the quiz;
    // re-running on every render would restart it mid-question.
  }, [uid, subject, topicSelection?.specificationId]);

  // Nothing to ask (no deck, no cards on this topic, or too few short ones):
  // step aside without a word rather than show an empty page.
  useEffect(() => { if (quiz === null) onDone([]); }, [quiz, onDone]);

  const card = quiz?.cards[index];
  const available = card ? cardMarks(card) : 0;
  const earned = card ? marksEarned(card, answer) : 0;

  useEffect(() => { headingRef.current?.focus(); }, [index, finished]);

  const commit = useCallback((graded: SecQuestionCard, result: QuizResult) => {
    if (!quiz) return;
    const t = now();
    const deckId = quiz.deck.deckId;
    if (!deckReady.current) { ensureDeck(uid, deckId, t); deckReady.current = true; }
    const local = readLocal(uid, deckId);
    const after = gradeCard(memoryFor(local, graded.id), result.grade, t, retentionFor(t, local.examTs));
    commitReview(uid, deckId, graded.id, after, t);
  }, [quiz, uid, now]);

  const next = useCallback(() => {
    if (!quiz || !card) return;
    const result: QuizResult = {
      cardId: card.id,
      questionRef: card.questionRef,
      marksClaimed: earned,
      marksAvailable: available,
      grade: quizGrade(card, answer),
    };
    commit(card, result);
    const all = [...results, result];
    setResults(all);
    setAnswer(EMPTY_ANSWER);
    setRevealed(false);
    if (index + 1 < quiz.cards.length) setIndex(index + 1);
    else setFinished(true);
  }, [quiz, card, earned, available, answer, commit, results, index]);

  const primary = useCallback(() => {
    if (finished) { onDone(results); return; }
    if (!revealed) { playCue('complete'); setRevealed(true); return; }
    next();
  }, [finished, onDone, results, revealed, next, playCue]);

  // ⌘↵ / Ctrl↵ moves on, as on the Kobra question card.
  useEffect(() => {
    const onKey = (event: KeyboardEvent) => {
      if (event.key === 'Enter' && (event.metaKey || event.ctrlKey)) { event.preventDefault(); primary(); }
    };
    window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
  }, [primary]);

  const toggleClaim = (key: string) => setAnswer(current => ({
    ...current,
    claims: { ...current.claims, [key]: current.claims[key] === 'yes' ? 'no' : 'yes' },
  }));
  const setStep = (key: string, marks: number) => setAnswer(current => ({
    ...current,
    claims: { ...current.claims, [key]: current.claims[key] === marks ? 'no' : marks },
  }));
  const togglePick = (key: string, option: number, max: number) => setAnswer(current => {
    const chosen = current.picks[key] ?? [];
    const on = chosen.includes(option);
    if (!on && chosen.length >= max) return current;
    return { ...current, picks: { ...current.picks, [key]: on ? chosen.filter(item => item !== option) : [...chosen, option] } };
  });

  const total = quiz?.cards.length ?? 0;
  const scoreClaimed = results.reduce((sum, item) => sum + item.marksClaimed, 0);
  const scoreAvailable = results.reduce((sum, item) => sum + item.marksAvailable, 0);
  const topicLabel = quiz?.topicLabel ?? subject;

  return (
    <KobraScope className="nsu-study-quiz">
      <div className="product-shell min-h-screen bg-[var(--surface-canvas)] text-[var(--ink-primary)]">
        <div className="sq-topbar" style={{ paddingTop: 'calc(16px + var(--sat, 0px))' }}>
          <div className="sq-width sq-topbar-row">
            <div className="sq-progress" aria-live="polite">
              <span className="sq-progress-count">
                {finished ? total : Math.min(index + 1, Math.max(total, 1))} of {Math.max(total, 1)}<small>questions</small>
              </span>
              <span className="sq-track" aria-hidden="true">
                <span style={{ width: `${total ? ((finished ? total : index) / total) * 100 : 0}%` }} />
              </span>
            </div>
            {!finished && quiz && (
              <button type="button" className="sq-quiet" onClick={onSkip}>Skip the quiz</button>
            )}
          </div>
        </div>

        <main className="sq-width sq-main">
          <div className="sq-hero">
            <div>
              <p className="sq-kicker">Quick check</p>
              <h1 ref={headingRef} tabIndex={-1} className="sq-title">
                {finished ? 'Here’s what stuck.' : `What stuck from ${subject}?`}
              </h1>
              <p className="sq-lede">
                {finished
                  ? 'Marked by you against the examiner’s scheme. Each of these comes back in Mark Bank when it’s due.'
                  : `Real exam questions on ${topicLabel}. Answer each one in your head or on paper, then reveal the scheme and tick what the examiner would have given you.`}
              </p>
            </div>
            <CrewIllustration character={character} />
          </div>

          {quiz === undefined && (
            <section className="sq-card nsu-paper-card" aria-busy="true" aria-label="Finding questions">
              <div className="sq-loading"><span /><span /><span /></div>
            </section>
          )}

          {quiz && !finished && card && (
            <section className="sq-card nsu-paper-card" aria-labelledby="sq-question-title">
              <header className="sq-card-head">
                <p className="sq-eyebrow">
                  <span>{String(index + 1).padStart(2, '0')}</span>
                  {card.year} {LEVEL_LABEL[quiz.deck.level]} · {card.questionRef}
                </p>
                <span className="sq-marks">{card.totalMarks} {card.totalMarks === 1 ? 'mark' : 'marks'}</span>
              </header>
              {card.stem && <p className="sq-stem">{card.stem}</p>}
              <h2 id="sq-question-title" className="sq-question">{card.questionText}</h2>
              {card.questionFigure && (
                <figure className="sq-figure">
                  <img src={figureUrl(card.questionFigure.src)} alt={card.questionFigure.alt} loading="lazy" />
                  <figcaption>{card.questionFigure.attribution}</figcaption>
                </figure>
              )}
              {card.figure && (!card.figure.solution || revealed) && (
                <figure className="sq-figure">
                  <img src={figureUrl(card.figure.src)} alt={card.figure.alt} loading="lazy" />
                  <figcaption>{card.figure.attribution}</figcaption>
                </figure>
              )}

              {!revealed ? (
                <div className="sq-answer-step">
                  <p className="sq-step-label">Step one · answer it</p>
                  <p className="sq-step-copy">Say it or jot it down. When you’re done, reveal the marking scheme and mark yourself.</p>
                  <div className="sq-actions">
                    <div>
                      <Button className="sq-primary" onClick={primary}>
                        Reveal the marking scheme <ArrowRight aria-hidden="true" />
                        <span className="sq-kbd" aria-hidden="true"><kbd>⌘</kbd><kbd>↵</kbd></span>
                      </Button>
                    </div>
                  </div>
                </div>
              ) : (
                <div className="sq-answer-step">
                  <p className="sq-step-label">Step two · mark yourself</p>
                  <p className="sq-step-copy">Tick each point the examiner would have given you.</p>
                  <ul className="sq-rows" aria-label="Marking scheme">
                    {card.rows.map((row, i) => {
                      const key = rowKey(row, i);
                      if (row.kind === 'anyN' && row.group) {
                        const group = row.group;
                        const chosen = answer.picks[key] ?? [];
                        return (
                          <li key={key} className="sq-group" role="group" aria-label={tariffLine(group)}>
                            <p className="sq-group-head"><span>{tariffLine(group)}</span><span>{Math.min(chosen.length, group.claimMax)} of {group.claimMax}</span></p>
                            {row.contextNote && <p className="sq-step-copy">{row.contextNote}</p>}
                            <ul className="sq-rows">
                              {group.options.map((option, oi) => {
                                const on = chosen.includes(oi);
                                const atCap = !on && chosen.length >= group.claimMax;
                                return (
                                  <li key={oi}>
                                    <button type="button" className="sq-row" aria-pressed={on} disabled={atCap} onClick={() => togglePick(key, oi, group.claimMax)}>
                                      <Mark />
                                      <span className="sq-row-text">{option}</span>
                                      <span className="sq-row-marks">{group.perOptionSteps ? '' : `${group.perOption} ${group.perOption === 1 ? 'mark' : 'marks'}`}</span>
                                    </button>
                                  </li>
                                );
                              })}
                            </ul>
                          </li>
                        );
                      }
                      if (row.permittedMarks) {
                        const selected = answer.claims[key];
                        return (
                          <li key={key} className="sq-group" role="group" aria-label={`Marks for ${row.verbatim}`}>
                            <p className="sq-group-head"><span>{row.verbatim}</span><span>up to {row.marks ?? Math.max(...row.permittedMarks)}</span></p>
                            {row.contextNote && <p className="sq-step-copy">{row.contextNote}</p>}
                            <div className="sq-steps">
                              {row.permittedMarks.map(marks => (
                                <button key={marks} type="button" aria-pressed={selected === marks} aria-label={`Award ${marks} marks`} onClick={() => setStep(key, marks)}>{marks}</button>
                              ))}
                            </div>
                          </li>
                        );
                      }
                      const needs = row.dependsOn && answer.claims[row.dependsOn] !== 'yes';
                      const on = answer.claims[key] === 'yes';
                      const marks = row.marks ?? 0;
                      return (
                        <li key={key}>
                          <button type="button" className="sq-row" aria-pressed={on} disabled={Boolean(needs)} onClick={() => toggleClaim(key)}
                            title={needs ? 'Needs the point above first' : undefined}>
                            <Mark />
                            <span className="sq-row-text">
                              {row.verbatim}
                              {row.accepts?.length ? <small>Also accepted: {row.accepts.join(' · ')}</small> : null}
                              {row.contextNote ? <small>{row.contextNote}</small> : null}
                              {row.exactTermRequired || row.kind === 'gate' ? <small>Exact term required.</small> : null}
                              {row.openList ? <small>The scheme’s list is open: a correct answer not printed still counts.</small> : null}
                            </span>
                            <span className="sq-row-marks">{marks} {marks === 1 ? 'mark' : 'marks'}</span>
                          </button>
                        </li>
                      );
                    })}
                  </ul>
                  <p className="sq-tally" aria-live="polite">
                    <strong><em>{earned}</em> of {available}</strong>
                    <span>marks you’d have been given</span>
                  </p>
                  <p className="sq-citation">{card.schemeCitation}</p>
                  <div className="sq-actions">
                    <div>
                      <Button className="sq-primary" onClick={primary}>
                        {index + 1 < total ? 'Next question' : 'See my score'} <ArrowRight aria-hidden="true" />
                        <span className="sq-kbd" aria-hidden="true"><kbd>⌘</kbd><kbd>↵</kbd></span>
                      </Button>
                    </div>
                  </div>
                </div>
              )}
            </section>
          )}

          {quiz && finished && (
            <section className="sq-card nsu-paper-card sq-score" aria-labelledby="sq-score-title">
              <header className="sq-card-head">
                <p className="sq-eyebrow"><span>{String(total).padStart(2, '0')}</span>{topicLabel}</p>
              </header>
              <h2 id="sq-score-title" className="sq-kicker">Your score</h2>
              <p className="sq-score-value"><em>{scoreClaimed}</em> of {scoreAvailable}<small>marks</small></p>
              <p className="sq-score-copy">
                {scoreAvailable > 0 && scoreClaimed >= scoreAvailable
                  ? 'Every mark. Whatever you did in that session, keep doing it.'
                  : scoreClaimed === 0
                    ? 'Nothing stuck yet — that’s useful to know now rather than in June. These come back in Mark Bank soon.'
                    : 'A fair read on what stuck. The ones you missed come back in Mark Bank sooner; the ones you had, later.'}
              </p>
              <ul className="sq-results" aria-label="Question by question">
                {results.map(result => (
                  <li key={result.cardId} data-grade={result.grade}>
                    <Mark />
                    <span>{result.questionRef}<small>{result.grade === 'got' ? 'Got it' : result.grade === 'shaky' ? 'Partly' : 'Missed'}</small></span>
                    <strong>{result.marksClaimed} / {result.marksAvailable}</strong>
                  </li>
                ))}
              </ul>
              <p className="sq-next">{quiz.poolTotal} questions on this in Mark Bank{quiz.poolTotal > total ? ' when you want more.' : '.'}</p>
              <div className="sq-actions">
                <div>
                  <Button className="sq-primary" onClick={primary}>
                    Collect your points <ArrowUpRight aria-hidden="true" />
                    <span className="sq-kbd" aria-hidden="true"><kbd>⌘</kbd><kbd>↵</kbd></span>
                  </Button>
                </div>
              </div>
            </section>
          )}
        </main>
      </div>
    </KobraScope>
  );
}
