import React, { useState } from 'react';
import SignatureCard from '../ui/SignatureCard';
import ActionButton from '../ui/ActionButton';
import type { StudyTopicAllocation, StudyTopicSelection } from '../../types/studyTopics';
import { validTopicAllocations } from '../../services/studyTopicHistory';
import { CURRICULUM_SPECIFICATIONS } from '../../curriculumRegistry';
import { formatStudyTime } from '../../utils/studyTime';

interface Props { selection: StudyTopicSelection; seconds: number; allocations: StudyTopicAllocation[]; onClose: () => void; onApply: (value: StudyTopicAllocation[]) => void }
export default function TopicTimeCard({ selection, seconds, allocations, onClose, onApply }: Props) {
  const [draft, setDraft] = useState(allocations);
  const spec = CURRICULUM_SPECIFICATIONS.find(item => item.id === selection.specificationId);
  const names = new Map(spec?.groups.flatMap(group => [[group.id, group.title], ...group.topics.map(topic => [topic.id, topic.title])]) as [string, string][]);
  const total = draft.reduce((sum, item) => sum + item.seconds, 0);
  const valid = validTopicAllocations(selection, draft, seconds);
  return <SignatureCard open onClose={onClose} eyebrow="Your study record" title="Where the time went." description={`Share ${formatStudyTime(seconds)} between the topics you worked on.`}
    footer={<ActionButton disabled={!valid} onClick={() => onApply(draft)}>Keep this split</ActionButton>}>
    <div className="topic-time-rows">{draft.map(item => <div key={item.topicId}>
      <strong>{names.get(item.topicId) ?? item.topicId}</strong>
      <label>Minutes<input type="number" min="0" max={Math.floor(seconds / 60)} step="1" value={Math.floor(item.seconds / 60)} onChange={event => setDraft(previous => previous.map(row => row.topicId === item.topicId ? { ...row, seconds: Math.max(0, Math.floor(Number(event.target.value))) * 60 + row.seconds % 60 } : row))} /></label>
      <label>Seconds<input type="number" min="0" max="59" step="1" value={item.seconds % 60} onChange={event => setDraft(previous => previous.map(row => row.topicId === item.topicId ? { ...row, seconds: Math.floor(row.seconds / 60) * 60 + Math.max(0, Math.min(59, Math.floor(Number(event.target.value)))) } : row))} /></label>
    </div>)}</div>
    <p role="status">{formatStudyTime(total)} allocated of {formatStudyTime(seconds)}.{!valid && ' Adjust the split to match your recorded time.'}</p>
  </SignatureCard>;
}
