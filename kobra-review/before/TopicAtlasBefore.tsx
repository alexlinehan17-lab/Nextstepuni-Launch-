/**
 * Dev-only "Now" pane for the Kobra review (27 Oct 2026): the REAL Topic Atlas,
 * components/PaperTrail/ReviseByTopic.tsx, mounted on Physics with the props
 * PaperTrail/index.tsx gives it (the Leaving Cert subjects that carry topic
 * tags, a sample student's own subjects, the Paper Trail subject labels), in
 * the same `px-6 pt-6` study surface and, as in the app, OUTSIDE the
 * pt-kobra scope. In dark mode the hex ink on the zinc-900 rows is the
 * vanishing-text bug the audit names, shown as it is.
 *
 * The paper corpus is world-readable, so the question cards load the real
 * crops and schemes. The strip at the top is the review harness, not the
 * screen: it opens the Atlas at the topic map or straight at one topic
 * (2.1, the transfer of heat energy, whose 2025 Higher question carries a marks lens).
 * "Full paper" and "Paper Trail" would leave the Atlas in the app; here they
 * only say so in the strip. Nothing is saved to an account (the review deck
 * lives in this browser's local storage under a review-only id).
 */
import { useState, type CSSProperties } from 'react';
import ReviseByTopic from '../../components/PaperTrail/ReviseByTopic';
import { paperTrailSubjectLabel } from '../../components/PaperTrail';
import { taggedSubjects } from '../../components/PaperTrail/topics';
import { PAPER_TRAIL_SUBJECTS } from '../../paperTrailData';
import { displayName } from '../../components/shared/subjectNames';

const UID = 'kobra-review-now';
const SUBJECT = 'physics';
// 2.1. The transfer of heat energy and temperature change (its 2025 Higher question carries a marks lens).
const TOPIC = 'physics-higher-new-course-21-the-transfer-of-heat-energy-and-temperature-change';
const MINE = ['physics', 'geography', 'biology', 'english', 'mathematics', 'french'];

const byId = new Map(PAPER_TRAIL_SUBJECTS.map(subject => [subject.id, subject]));
const label = (id: string) => {
  const subject = byId.get(id);
  return subject ? paperTrailSubjectLabel(subject) : displayName(id);
};
// As index.tsx builds it for a Leaving Cert student: in-cycle tagged subjects, by label.
const SUBJECTS = taggedSubjects()
  .map(id => byId.get(id))
  .filter((subject): subject is NonNullable<typeof subject> => !!subject && subject.cycle === 'lc')
  .map(subject => ({ id: subject.id, label: paperTrailSubjectLabel(subject) }))
  .sort((a, b) => a.label.localeCompare(b.label));
const MINE_IDS = SUBJECTS.filter(subject => MINE.includes(subject.id)).map(subject => subject.id);

const params = new URLSearchParams(window.location.search);
const startAtTopic = params.get('topic') === '1';
try { localStorage.setItem(`atlas.subject:${UID}`, SUBJECT); } catch { /* private mode */ }

const bar: CSSProperties = {
  display: 'flex', flexWrap: 'wrap', alignItems: 'center', gap: '8px 14px', minHeight: 48, padding: '8px 14px',
  borderBottom: '1px dashed #a1a1aa', background: '#fff', color: '#3f3f46', font: "500 12px/1.3 'DM Sans', sans-serif",
};
const control: CSSProperties = {
  minHeight: 32, padding: '4px 10px', border: '1px solid #71717a', borderRadius: 8, background: '#fff', color: '#18181b',
  font: "500 12px/1 'DM Sans', sans-serif", cursor: 'pointer',
};

export default function TopicAtlasBefore() {
  const [view, setView] = useState<'map' | 'topic'>(startAtTopic ? 'topic' : 'map');
  const [run, setRun] = useState(0);
  const [note, setNote] = useState('');
  const open = (next: 'map' | 'topic') => {
    // ReviseByTopic opens on the subject it last showed; start each run on Physics.
    try { localStorage.setItem(`atlas.subject:${UID}`, SUBJECT); } catch { /* private mode */ }
    setView(next);
    setNote('');
    setRun(value => value + 1);
  };
  return (
    <>
      <div style={bar} role="group" aria-label="Review harness">
        <span>Review harness: the real Topic Atlas, sample student</span>
        <span style={{ display: 'inline-flex', gap: 6 }}>
          {(['map', 'topic'] as const).map(value => (
            <button key={value} type="button" aria-pressed={view === value} onClick={() => open(value)}
              style={{ ...control, ...(view === value ? { background: '#18181b', color: '#fff', borderColor: '#18181b' } : null) }}>
              {value === 'map' ? 'Physics topic map' : 'One topic: 2.1, heat energy'}
            </button>
          ))}
        </span>
        {note && <span role="status">{note}</span>}
      </div>
      <div className="px-6 pt-6">
        <ReviseByTopic
          key={`${view}-${run}`}
          subjects={SUBJECTS}
          mineIds={MINE_IDS}
          uid={UID}
          subjectLabel={label}
          restore={view === 'topic' ? { subjectId: SUBJECT, subtopicId: TOPIC } : undefined}
          onOpenQuestion={question => setNote(`In the app this opens ${label(question.subjectId)} ${question.year} at question ${question.n} in the paper viewer.`)}
          onBack={() => setNote('In the app this goes back to the Paper Trail home.')}
        />
      </div>
    </>
  );
}
