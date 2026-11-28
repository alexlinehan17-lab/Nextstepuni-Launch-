import React, { useId, useState } from 'react';
import { ChevronDown, ChevronUp } from 'lucide-react';
import { Button, TextButton } from '../ui/Button';
import { List, Row } from '../ui/List';
import type { PaperAnswerQuestion } from '../../types/paperTrail';
import './questionTools.css';

export interface QuestionTopicInfo {
  subtopicId: string;
  label: string;
  yearsWith: number;
  totalYears: number;
}

interface Props {
  page: number;
  initialQuestion?: string;
  questions: PaperAnswerQuestion[];
  topicInfo?: ReadonlyMap<string, QuestionTopicInfo> | null;
  showAnswers: boolean;
  onAnswer: (question: PaperAnswerQuestion) => void;
  onTopic: (n: string) => void;
}

/** Phone controls live outside the PDF canvas. A dense page still has one
 * readable topic and one scheme action, regardless of its question count.
 * Drawn as a sheet resting under the paper (area 6a): the system's surface,
 * type, row and main button; it follows the page being read, so it stays open
 * while the paper scrolls rather than covering it. */
export default function MobileQuestionTools({ page, initialQuestion, questions, topicInfo, showAnswers, onAnswer, onTopic }: Props) {
  const [expanded, setExpanded] = useState(true);
  const [selected, setSelected] = useState(initialQuestion ?? '');
  const id = useId();
  const available = questions.filter(q => showAnswers || topicInfo?.has(q.n));
  const question = available.find(q => q.n === selected) ?? available[0];
  const info = question ? topicInfo?.get(question.n) : undefined;
  const title = topicInfo ? showAnswers ? 'Topics & answers' : 'Topics' : 'Answers';

  return <section className="pt-question-tools" aria-label={`${title} on page ${page}`}>
    <div className="pt-question-tools-heading">
      <span className="pt-question-title">{title} <span className="pt-question-page">· Page {page}</span></span>
      <TextButton tone="quiet" className="pt-question-disclosure" aria-expanded={expanded} aria-controls={id} aria-label={`${expanded ? 'Hide' : 'Show'} question details`} onClick={() => setExpanded(value => !value)}>
        {available.length ? `${available.length} ${available.length === 1 ? 'question' : 'questions'}` : 'No questions'}
        {expanded ? <ChevronDown className="ui-icon" width={20} height={20} strokeWidth={1.75} aria-hidden="true" /> : <ChevronUp className="ui-icon" width={20} height={20} strokeWidth={1.75} aria-hidden="true" />}
      </TextButton>
    </div>
    <div id={id} hidden={!expanded} className="pt-question-details">
      {question ? <>
        <label className="sr-only" htmlFor={`${id}-question`}>Question on page {page}</label>
        <select id={`${id}-question`} className="pt-question-select" value={question.n} onChange={event => setSelected(event.target.value)}>
          {available.map(q => <option key={q.n} value={q.n}>{q.label ?? `Question ${q.n}`}</option>)}
        </select>
        {info && <List className="pt-question-topic"><Row title={info.label} label={`Explore ${info.label} across years`}
          meta={`${info.totalYears > 0 ? `${info.yearsWith} of ${info.totalYears} tagged years · ` : ''}Explore topic`} onPress={() => onTopic(question.n)} /></List>}
        {showAnswers && <Button kind="main" block arrow="forward" className="pt-question-answer" onClick={() => onAnswer(question)} aria-label={`Open the marking scheme for ${question.label ?? `Question ${question.n}`}`}>
          Marking scheme
        </Button>}
      </> : <p className="pt-question-empty">No mapped questions on this page. Scroll to a question page.</p>}
    </div>
  </section>;
}
