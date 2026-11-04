import React, { useId, useState } from 'react';
import { ArrowRight, ChevronDown, ChevronUp } from 'lucide-react';
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
 * readable topic and one scheme action, regardless of its question count. */
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
      <span>{title} <span className="pt-question-page">· Page {page}</span></span>
      <button type="button" className="pt-question-disclosure" aria-expanded={expanded} aria-controls={id} aria-label={`${expanded ? 'Hide' : 'Show'} question details`} onClick={() => setExpanded(value => !value)}>
        <span>{available.length ? `${available.length} ${available.length === 1 ? 'question' : 'questions'}` : 'No questions'}</span>
        {expanded ? <ChevronDown size={18} aria-hidden /> : <ChevronUp size={18} aria-hidden />}
      </button>
    </div>
    <div id={id} hidden={!expanded} className="pt-question-details">
      {question ? <>
        <label className="sr-only" htmlFor={`${id}-question`}>Question on page {page}</label>
        <select id={`${id}-question`} className="pt-question-select" value={question.n} onChange={event => setSelected(event.target.value)}>
          {available.map(q => <option key={q.n} value={q.n}>{q.label ?? `Question ${q.n}`}</option>)}
        </select>
        {info && <button type="button" className="pt-question-topic" onClick={() => onTopic(question.n)} aria-label={`Explore ${info.label} across years`}>
          <span className="pt-question-topic-label">{info.label}</span>
          <span className="pt-question-topic-link">{info.totalYears > 0 ? `${info.yearsWith} of ${info.totalYears} tagged years · ` : ''}Explore topic <ArrowRight size={14} aria-hidden /></span>
        </button>}
        {showAnswers && <button type="button" className="pt-question-answer" onClick={() => onAnswer(question)} aria-label={`Open the marking scheme for ${question.label ?? `Question ${question.n}`}`}>
          <span>Marking scheme</span><ArrowRight size={18} aria-hidden />
        </button>}
      </> : <p className="pt-question-empty">No mapped questions on this page. Scroll to a question page.</p>}
    </div>
  </section>;
}
