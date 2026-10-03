import React from 'react';
import { fireEvent, render, screen, within } from '@testing-library/react';
import { beforeEach, describe, expect, it, vi } from 'vitest';
import TopicTimeCard from '../components/study/TopicTimeCard';
import TopicDetailCard from '../components/topics/TopicDetailCard';
import StudySessionFinish from '../components/study/StudySessionFinish';
import { resolveCurriculumSpecification } from '../curriculumRegistry';
import { equalTopicAllocations, studyTopicSelection } from '../services/studyTopicHistory';
import { emptyTopicMasteryV2, upsertCanonicalMastery } from '../services/topicMasteryMigration';
import StudyTopicPicker from '../components/study/StudyTopicPicker';
import userEvent from '@testing-library/user-event';

beforeEach(() => localStorage.clear());
describe('topic cards', () => {
  it('searches and selects several syllabus topics through the Kobra picker', async () => {
    const user = userEvent.setup();
    const spec = resolveCurriculumSpecification('Politics & Society', 2027)!;
    const first = spec.groups[0].topics[0], second = spec.groups[1].topics[0];
    function Picker() {
      const [selected, setSelected] = React.useState<string[]>([]);
      return <StudyTopicPicker subject="Politics & Society" examDate="2027-06-02" level="higher" selected={selected} onChange={setSelected} />;
    }
    render(<Picker />);
    const input = screen.getByRole('combobox');
    await user.click(input);
    await user.type(input, first.title);
    await user.click(await screen.findByRole('option', { name: new RegExp(first.title) }));
    expect(screen.getByRole('button', { name: `Remove ${first.title}` })).toBeInTheDocument();
    await user.clear(input);
    await user.type(input, second.title);
    await user.click(await screen.findByRole('option', { name: new RegExp(second.title) }));
    const chips = screen.getByRole('list', { name: 'Selected study topics' });
    expect(within(chips).getAllByRole('button')).toHaveLength(2);
    await user.click(screen.getByRole('button', { name: `Remove ${first.title}` }));
    expect(within(chips).getAllByRole('button')).toHaveLength(1);
    expect(screen.getByRole('button', { name: `Remove ${second.title}` })).toBeInTheDocument();
  });
  it('edits a split in a Signature popup and blocks a mismatched total', () => {
    const spec = resolveCurriculumSpecification('Mathematics', 2027)!;
    const ids = spec.groups.slice(0, 3).map(item => item.id);
    const selection = studyTopicSelection('Mathematics', ids, '2027-06-02')!;
    const onApply = vi.fn();
    render(<TopicTimeCard selection={selection} seconds={1800} allocations={equalTopicAllocations(ids, 1800)} onClose={vi.fn()} onApply={onApply} />);
    const dialog = screen.getByRole('dialog', { name: 'Where the time went.' });
    expect(dialog).toHaveClass('signature-card');
    const inputs = within(dialog).getAllByRole('spinbutton', { name: 'Minutes' });
    fireEvent.change(inputs[0], { target: { value: '15' } });
    expect(within(dialog).getByRole('button', { name: 'Keep this split' })).toBeDisabled();
    fireEvent.change(inputs[1], { target: { value: '5' } });
    fireEvent.click(within(dialog).getByRole('button', { name: 'Keep this split' }));
    expect(onApply).toHaveBeenCalledWith(ids.map((topicId, index) => ({ topicId, seconds: [900, 300, 600][index] })));
  });
  it('keeps reflection writing in place while the time card opens separately', () => {
    const spec = resolveCurriculumSpecification('Mathematics', 2027)!;
    const selection = studyTopicSelection('Mathematics', [spec.groups[0].id], '2027-06-02')!;
    render(<StudySessionFinish subject="Mathematics" elapsedSeconds={1800} plannedSeconds={1800} practice="Revision" strategies={[]} basePoints={15} isSaving={false} mode="full" onModeChange={vi.fn()} onSave={vi.fn()} onSkip={vi.fn()} topicSelection={selection} />);
    const reflection = screen.getByRole('textbox', { name: /^What worked, and what will you try next time\?/ });
    fireEvent.change(reflection, { target: { value: 'Active recall helped me identify a gap.' } });
    fireEvent.click(screen.getByRole('button', { name: 'Review topic time' }));
    expect(screen.getByRole('dialog', { name: 'Where the time went.' })).toBeInTheDocument();
    fireEvent.click(screen.getByRole('button', { name: 'Keep this split' }));
    expect(reflection).toHaveValue('Active recall helped me identify a gap.');
  });
  it('opens an individual topic from a coverage area and launches its stable identity', () => {
    const spec = resolveCurriculumSpecification('Politics & Society', 2027)!;
    const group = spec.groups[0], topic = group.topics[0];
    const mastery = upsertCanonicalMastery(emptyTopicMasteryV2(), 'Politics & Society', topic.title, { confidence: 'solid', updatedAt: 1, source: 'manual' }, '2027-06-02', topic.id);
    const onStudyTopic = vi.fn(), onConfidence = vi.fn();
    render(<TopicDetailCard uid="test" subject="Politics & Society" nodeId={group.id} examDate="2027-06-02" level="Higher" sessions={[]} mastery={mastery} onClose={vi.fn()} onStudyTopic={onStudyTopic} onConfidence={onConfidence} />);
    fireEvent.change(screen.getByRole('combobox', { name: 'Look at' }), { target: { value: topic.id } });
    expect(screen.getByRole('dialog')).toHaveClass('signature-card');
    expect(screen.getByRole('button', { name: 'Solid' })).toHaveAttribute('aria-pressed', 'true');
    fireEvent.click(screen.getByRole('button', { name: 'Shaky' }));
    expect(onConfidence).toHaveBeenCalledWith('Politics & Society', topic.title, 'shaky', topic.id);
    fireEvent.click(screen.getByRole('button', { name: 'Start studying' }));
    expect(onStudyTopic).toHaveBeenCalledWith({ subjectId: spec.subjectId, specificationId: spec.id, topicIds: [topic.id] });
  });
});
