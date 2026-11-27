import { useMemo, useRef, useState } from 'react';
import { ChevronDown } from 'lucide-react';
import KobraScope, { Dialog, DialogContent, DialogDescription, DialogTitle } from '../approved-ui-runtime';
import { TopBar } from '../ui/Bars';
import { Button, Glyph } from '../ui/Button';
import { ChoiceTile } from '../ui/Choice';
import { SearchField } from '../ui/Field';
import SessionScreen, { type SessionCardResult } from './SessionScreen';
import { LEVEL_LABEL, type Level } from './deck';
import type { SecCard } from '../../types/markBank';
import type { CanonicalCurriculumSpecification } from '../../curriculumRegistry';
import type { CardMemory } from './scheduler';
import { planStartingPoint, STARTING_POINT_TOPICS, startingPointResults, startingPointTopics, type StartingPointQuestion } from './startingPoint';
import '../study/quiz/study-quiz.css';
import './starting-point.css';

interface Props {
  subjectLabel: string;
  level: Level;
  spec?: CanonicalCurriculumSpecification;
  cards: SecCard[];
  memories: Record<string, CardMemory | undefined>;
  now: () => number;
  examTs?: number;
  onGrade: (result: SessionCardResult) => string | void;
  onPractice: (topicId: string, card: SecCard) => void;
  onClose: () => void;
}

export default function StartingPointCheck({ subjectLabel, level, spec, cards, memories, now, examTs, onGrade, onPractice, onClose }: Props) {
  const topics = useMemo(() => startingPointTopics(spec, level, cards), [spec, level, cards]);
  const [selected, setSelected] = useState<string[]>([]);
  const [query, setQuery] = useState('');
  const [phase, setPhase] = useState<'choose' | 'questions' | 'summary'>('choose');
  const [questions, setQuestions] = useState<StartingPointQuestion[]>([]);
  const [results, setResults] = useState<SessionCardResult[]>([]);
  const committed = useRef(new Set<string>());
  // Re-rendering while typing must not replace the sample shown in the preview.
  const [sampleTime] = useState(now);
  const preview = useMemo(() => planStartingPoint(topics, selected, memories, sampleTime, examTs), [topics, selected, memories, sampleTime, examTs]);
  const complete = () => setPhase('summary');

  if (phase === 'questions') return <SessionScreen paperLayout
    cards={questions.map(question => question.card)} subjectLabel={subjectLabel}
    onGrade={result => {
      if (committed.current.has(result.cardId) || !startingPointResults(questions, [result]).some(item => item.result)) return;
      committed.current.add(result.cardId);
      onGrade(result);
      setResults(previous => [...previous, result]);
    }}
    onFinish={complete} onExit={complete}
    studyReview={{
      banner: <div className="sq-session-banner mb-starting-banner">Starting-point check · {subjectLabel} · {LEVEL_LABEL[level]}</div>,
      topicTitle: card => questions.find(question => question.card.id === card.id)?.title ?? subjectLabel,
      requireAttempt: true, onCue: () => {}, onResponse: () => {},
    }} />;

  const outcomes = startingPointResults(questions, results);
  const practice = outcomes.filter(item => item.status === 'practice');
  const unknown = topics.filter(topic => !outcomes.some(item => item.topicId === topic.id && item.result));
  const visible = topics.filter(topic => `${topic.title} ${topic.group}`.toLowerCase().includes(query.trim().toLowerCase()));
  const toggleTopic = (topicId: string) => setSelected(previous => previous.includes(topicId)
    ? previous.filter(id => id !== topicId)
    : previous.length >= STARTING_POINT_TOPICS ? previous : [...previous, topicId]);
  // The frame is today's (a dialog over Mark Bank), drawn with the shared parts
  // (starting-point.css). One leave control, top left: the footer's "Back to Mark
  // Bank" did exactly what this Close does, so it has gone (navigation.md).
  return <KobraScope><Dialog open onOpenChange={open => { if (!open) onClose(); }}>
    <DialogContent className="mb-live-session-dialog sq-dialog mb-starting-point" showCloseButton={false}>
      <TopBar className="mb-starting-bar" leave={{ kind: 'close', onPress: onClose, label: 'Close starting-point check' }} />
      <div className="sq-summary-body">
        <div className="mb-starting-head">
          <p className="t-label mb-starting-kicker">{subjectLabel} / {LEVEL_LABEL[level]}</p>
          <DialogTitle className="mb-starting-title">{phase === 'choose' ? 'Where should I start?' : 'Your next step.'}</DialogTitle>
          <DialogDescription className="mb-starting-lede">{phase === 'choose' ? 'A small check on topics you have already covered.' : 'Based only on the questions you attempted and marked.'}</DialogDescription>
        </div>
        {phase === 'choose' ? <>
          <p>Choose up to {STARTING_POINT_TOPICS} topics you have covered in class or studied yourself. Try each question without notes, then compare your answer with the official marking scheme. You can skip any question.</p>
          <SearchField className="mb-starting-search" label="Find a topic for your starting-point check" placeholder="Find a topic…" autoComplete="off" value={query} onChange={event => setQuery(event.target.value)} />
          {!topics.length && <p>No verified topic map is available for this syllabus and level yet. You can still use the normal question bank.</p>}
          {topics.length > 0 && !topics.some(topic => topic.cards.length) && <p>There are no suitable questions for this check yet. The normal question bank is still available.</p>}
          <fieldset className="mb-starting-topics"><legend className="t-label">Topics you have covered</legend>
            <div className="ui-choices">
              {visible.map(topic => {
                const chosen = selected.includes(topic.id);
                const unavailable = !topic.cards.length || (selected.length >= STARTING_POINT_TOPICS && !chosen);
                return <ChoiceTile key={topic.id} kind="several" chosen={chosen} aria-disabled={unavailable || undefined}
                  label={topic.title} meta={topic.cards.length ? topic.group : 'No suitable question for this check yet'}
                  onClick={() => { if (!unavailable) toggleTopic(topic.id); }} />;
              })}
            </div>
          </fieldset>
          {topics.length > 0 && !visible.length && <p>No matching topics. Try another search.</p>}
          {preview.length > 0 && <div className="mb-starting-sec" aria-live="polite"><h2>This check</h2>
            <ul className="sq-results">{preview.map(item => <li key={item.card.id}><div><strong>{item.title}</strong><small>{item.card.questionRef} · {item.card.totalMarks} marks</small></div></li>)}</ul>
            <p>One question per sampled topic. A check contains up to three short questions or one extended task. {selected.length > preview.length && 'The other selected topics will remain unchecked this time.'}</p>
          </div>}
          <p>This sample helps you choose some practice. It cannot measure your whole subject or predict an exam grade.</p>
        </> : <>
          <h2>{practice.length ? `Start with ${practice[0].title}.` : results.length ? 'Return to these questions another day.' : 'No answers marked yet.'}</h2>
          <p>{practice.length ? 'Your answer left some marking points to work on. Read those points, correct your answer, then try the question again without the scheme.' : results.length ? 'You awarded yourself all the available marks on the questions you marked. A later attempt without notes is a useful next check; this does not establish mastery of the topic.' : 'Skipped and unfinished questions do not count as wrong answers. Choose a topic you have covered and try a question when you are ready.'}</p>
          <ul className="sq-results" aria-label="Starting-point results">{outcomes.map(item => <li key={item.card.id}>
            <div><strong>{item.title}</strong><small>{item.card.questionRef} · {item.status === 'unknown' ? 'Not checked — skipped or unfinished' : item.status === 'practice' ? 'Practise this question next' : 'Full marks self-assessed on this question — check again later'}</small>
              {item.result && <small>{item.result.marksClaimed} / {item.result.marksAvailable} self-assessed marks</small>}
            </div>
            {item.status === 'practice' && <Button onClick={() => onPractice(item.topicId, item.card)}>Practise {item.title}</Button>}
          </li>)}</ul>
          <details className="mb-starting-more"><summary><span>Not checked ({unknown.length} topics)</span><Glyph icon={ChevronDown} size={20} /></summary>
            <p>There is no result for these topics from this check. They may be untaught, unselected, skipped or have no suitable question yet.</p>
            <ul>{unknown.map(topic => <li key={topic.id}>{topic.title}</li>)}</ul>
          </details>
          <p>These are self-assessed results from a small sample, not a subject score. Marked questions are saved in your normal Mark Bank review history.</p>
        </>}
      </div>
      <footer className="sq-summary-footer mb-starting-foot"><span>{phase === 'choose' ? `${selected.length} / ${STARTING_POINT_TOPICS} topics selected` : `${results.length} ${results.length === 1 ? 'question' : 'questions'} marked`}</span>
        {/* The shared Button has no disabled state; until a topic is chosen the
            fieldset holds it disabled, as today, and the count beside it says why. */}
        {phase === 'choose' && <fieldset className="mb-starting-go" disabled={!preview.length}>
          <Button kind="main" size="lg" block arrow="forward" onClick={() => { setQuestions(preview); setPhase('questions'); }}>Start check · {preview.length} {preview.length === 1 ? 'question' : 'questions'}</Button>
        </fieldset>}
      </footer>
    </DialogContent>
  </Dialog></KobraScope>;
}
