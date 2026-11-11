import { useMemo, useRef, useState } from 'react';
import { X } from 'lucide-react';
import KobraScope, { Button, Checkbox, Dialog, DialogContent, DialogDescription, DialogTitle, Input } from '../approved-ui-runtime';
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
      banner: <div className="sq-session-banner">Starting-point check · {subjectLabel} · {LEVEL_LABEL[level]}</div>,
      topicTitle: card => questions.find(question => question.card.id === card.id)?.title ?? subjectLabel,
      requireAttempt: true, onCue: () => {}, onResponse: () => {},
    }} />;

  const outcomes = startingPointResults(questions, results);
  const practice = outcomes.filter(item => item.status === 'practice');
  const unknown = topics.filter(topic => !outcomes.some(item => item.topicId === topic.id && item.result));
  const visible = topics.filter(topic => `${topic.title} ${topic.group}`.toLowerCase().includes(query.trim().toLowerCase()));
  return <KobraScope><Dialog open onOpenChange={open => { if (!open) onClose(); }}>
    <DialogContent className="mb-live-session-dialog sq-dialog mb-starting-point" showCloseButton={false}>
      <header className="mb-paper-session-heading">
        <div><p className="mb-kicker">{subjectLabel} / {LEVEL_LABEL[level]}</p>
          <DialogTitle>{phase === 'choose' ? 'Where should I start?' : 'Your next step.'}</DialogTitle>
          <DialogDescription>{phase === 'choose' ? 'A small check on topics you have already covered.' : 'Based only on the questions you attempted and marked.'}</DialogDescription>
        </div>
        <Button variant="outline" size="icon" aria-label="Close starting-point check" onClick={onClose}><X size={18} /></Button>
      </header>
      <div className="sq-summary-body">
        {phase === 'choose' ? <>
          <p>Choose up to {STARTING_POINT_TOPICS} topics you have covered in class or studied yourself. Try each question without notes, then compare your answer with the official marking scheme. You can skip any question.</p>
          <Input aria-label="Find a topic for your starting-point check" placeholder="Find a topic…" value={query} onChange={event => setQuery(event.target.value)} />
          {!topics.length && <p>No verified topic map is available for this syllabus and level yet. You can still use the normal question bank.</p>}
          {topics.length > 0 && !topics.some(topic => topic.cards.length) && <p>There are no suitable questions for this check yet. The normal question bank is still available.</p>}
          <fieldset className="mb-starting-topics"><legend>Topics you have covered</legend>
            {visible.map(topic => <label key={topic.id} className="mb-starting-topic" data-selected={selected.includes(topic.id)}>
              <Checkbox checked={selected.includes(topic.id)} disabled={!topic.cards.length || (selected.length >= STARTING_POINT_TOPICS && !selected.includes(topic.id))}
                onCheckedChange={checked => setSelected(previous => checked
                  ? previous.includes(topic.id) || previous.length >= STARTING_POINT_TOPICS ? previous : [...previous, topic.id]
                  : previous.filter(id => id !== topic.id))} />
              <span>{topic.title}<small>{topic.cards.length ? topic.group : 'No suitable question for this check yet'}</small></span>
            </label>)}
          </fieldset>
          {topics.length > 0 && !visible.length && <p>No matching topics. Try another search.</p>}
          {preview.length > 0 && <div aria-live="polite"><h2>This check</h2>
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
            {item.status === 'practice' && <Button variant="outline" onClick={() => onPractice(item.topicId, item.card)}>Practise {item.title}</Button>}
          </li>)}</ul>
          <details><summary>Not checked ({unknown.length} topics)</summary>
            <p>There is no result for these topics from this check. They may be untaught, unselected, skipped or have no suitable question yet.</p>
            <ul>{unknown.map(topic => <li key={topic.id}>{topic.title}</li>)}</ul>
          </details>
          <p>These are self-assessed results from a small sample, not a subject score. Marked questions are saved in your normal Mark Bank review history.</p>
        </>}
      </div>
      <footer className="sq-summary-footer"><span>{phase === 'choose' ? `${selected.length} / ${STARTING_POINT_TOPICS} topics selected` : `${results.length} ${results.length === 1 ? 'question' : 'questions'} marked`}</span><div>
        <Button variant="outline" onClick={onClose}>Back to Mark Bank</Button>
        {phase === 'choose' && <Button className="sq-primary" disabled={!preview.length} onClick={() => { setQuestions(preview); setPhase('questions'); }}>Start check · {preview.length} {preview.length === 1 ? 'question' : 'questions'}</Button>}
      </div></footer>
    </DialogContent>
  </Dialog></KobraScope>;
}
