/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * SubjectPicker — Subject → Level → Topic chooser for Exam Reps. Shows the
 * full Leaving Cert curriculum (all 41 subjects, every strand → sub-topic);
 * subjects/topics that don't have reps yet are shown but marked "soon". The
 * chosen Subject·Level·Topic scopes the rep loop.
 */
import React, { useState, useMemo } from 'react';
import { ArrowLeft, Check } from 'lucide-react';
import { COLORS } from '../../design/tokens';
import { CURRICULUM, type CurriculumLevel } from '../../curriculum';
import { REP_CARDS } from '../../examRepsData';
import { type RepSelection } from '../../types/examReps';

const CATEGORY_ORDER: { id: string; label: string }[] = [
  { id: 'stem', label: 'STEM' },
  { id: 'business', label: 'Business' },
  { id: 'social-environmental', label: 'Social & Environmental' },
  { id: 'language', label: 'Languages' },
  { id: 'practical-applied', label: 'Practical & Applied' },
  { id: 'arts', label: 'Arts' },
  { id: 'other', label: 'Other' },
];

const LEVEL_LABEL: Record<string, string> = { higher: 'Higher', ordinary: 'Ordinary', foundation: 'Foundation', common: 'Common' };

interface SubjectPickerProps {
  selection?: RepSelection;
  onSelect: (sel: RepSelection) => void;
  /** Curriculum subject ids the student chose during onboarding. */
  studentSubjectIds?: string[];
}

const SubjectPicker: React.FC<SubjectPickerProps> = ({ selection, onSelect, studentSubjectIds }) => {
  const mySet = useMemo(() => new Set(studentSubjectIds ?? []), [studentSubjectIds]);
  // Default to the student's own subjects; if they have none, show everything.
  const [showAll, setShowAll] = useState((studentSubjectIds?.length ?? 0) === 0);
  // which subject ids / topic ids have at least one rep
  const avail = useMemo(() => {
    const subj = new Set<string>();
    const topicLevel = new Set<string>(); // `${topicId}|${level}`
    const subjLevel = new Set<string>();
    for (const c of REP_CARDS) {
      if (c.subjectId) subj.add(c.subjectId);
      if (c.subjectId) subjLevel.add(`${c.subjectId}|${c.level}`);
      if (c.topicId) topicLevel.add(`${c.topicId}|${c.level}`);
    }
    return { subj, topicLevel, subjLevel };
  }, []);

  const [step, setStep] = useState<'subject' | 'detail'>('subject');
  const [subjectId, setSubjectId] = useState<string | null>(null);
  const [level, setLevel] = useState<string | null>(null);

  const subject = subjectId ? CURRICULUM.find(s => s.id === subjectId) ?? null : null;

  const openSubject = (id: string) => {
    const subj = CURRICULUM.find(s => s.id === id);
    if (!subj) return;
    // default to the first level that has reps, else the first level
    const lvl = (subj.levels as string[]).find(l => avail.subjLevel.has(`${id}|${l}`)) ?? subj.levels[0];
    setSubjectId(id); setLevel(lvl); setStep('detail');
  };

  // ── Subject step ────────────────────────────────────────────────────────
  if (step === 'subject') {
    return (
      <div className="w-full max-w-2xl mx-auto pb-12">
        <header className="mb-6 flex items-start justify-between gap-3">
          <div>
            <p className="font-mono text-[10px] font-bold uppercase tracking-[0.2em] text-zinc-400 mb-1">Exam Reps</p>
            <h1 className="font-serif text-2xl md:text-3xl font-bold text-[#1A1A1A] dark:text-white">Pick your subject</h1>
            <p className="text-sm text-[#7a7068] dark:text-zinc-400 mt-1">{showAll ? 'All Leaving Cert subjects. ' : 'Your subjects. '}Ones without reps yet are marked “soon”.</p>
          </div>
          {(studentSubjectIds?.length ?? 0) > 0 && (
            <button
              type="button"
              onClick={() => setShowAll(v => !v)}
              className="shrink-0 rounded-full border-2 px-3 py-1.5 text-xs font-semibold transition-colors"
              style={{ borderColor: COLORS.border, backgroundColor: showAll ? COLORS.accentTint : '#FFFFFF', color: '#1A1A1A' }}
            >
              {showAll ? 'My subjects' : 'All subjects'}
            </button>
          )}
        </header>

        {CATEGORY_ORDER.map(cat => {
          const subs = CURRICULUM.filter(s => s.category === cat.id && (showAll || mySet.has(s.id)));
          if (subs.length === 0) return null;
          return (
            <section key={cat.id} className="mb-5">
              <p className="text-[10px] font-bold uppercase tracking-[0.15em] text-zinc-400 mb-2">{cat.label}</p>
              <div className="flex flex-wrap gap-2">
                {subs.map(s => {
                  const has = avail.subj.has(s.id);
                  return (
                    <button
                      key={s.id}
                      type="button"
                      onClick={() => openSubject(s.id)}
                      className="rounded-xl border-2 px-3 py-2 text-sm font-semibold transition-colors text-left"
                      style={{
                        borderColor: has ? COLORS.border : '#e0ddd8',
                        backgroundColor: has ? '#FFFFFF' : '#F9F9F7',
                        color: has ? '#1A1A1A' : '#9e9186',
                        boxShadow: has ? `2px 2px 0 0 ${COLORS.border}` : 'none',
                      }}
                    >
                      {s.name}
                      {!has && <span className="ml-1.5 text-[9px] font-bold uppercase tracking-wide px-1.5 py-0.5 rounded-full" style={{ backgroundColor: '#EDEBE8', color: '#9e9186' }}>soon</span>}
                    </button>
                  );
                })}
              </div>
            </section>
          );
        })}
      </div>
    );
  }

  // ── Detail step (level + topics) ────────────────────────────────────────
  if (!subject || !level) return null;
  const subjectHasAny = avail.subj.has(subject.id);

  return (
    <div className="w-full max-w-2xl mx-auto pb-12">
      <button type="button" onClick={() => setStep('subject')} className="inline-flex items-center gap-1.5 text-xs font-semibold text-[#7a7068] hover:text-[#1A1A1A] transition-colors mb-3">
        <ArrowLeft size={14} /> Subjects
      </button>
      <h1 className="font-serif text-2xl font-bold text-[#1A1A1A] dark:text-white mb-3">{subject.name}</h1>

      {/* level toggle */}
      <div className="flex gap-2 mb-5">
        {subject.levels.map((lvl: CurriculumLevel) => {
          const on = level === lvl;
          const hasLvl = avail.subjLevel.has(`${subject.id}|${lvl}`);
          return (
            <button
              key={lvl}
              type="button"
              onClick={() => setLevel(lvl)}
              className="rounded-xl border-2 px-4 py-2 text-sm font-semibold transition-colors"
              style={{ borderColor: on ? COLORS.accent : COLORS.border, backgroundColor: on ? COLORS.accentTint : '#FFFFFF', color: '#1A1A1A' }}
            >
              {LEVEL_LABEL[lvl] ?? lvl}{hasLvl && <span className="ml-1.5 inline-block w-1.5 h-1.5 rounded-full align-middle" style={{ backgroundColor: COLORS.success }} />}
            </button>
          );
        })}
      </div>

      {!subjectHasAny && (
        <div className="rounded-xl p-4 mb-4 text-center" style={{ backgroundColor: '#F9F9F7' }}>
          <p className="text-sm text-[#7a7068]">No reps for {subject.name} yet — we’re forging them. Browse the topics below.</p>
        </div>
      )}

      {subject.strands.map(strand => (
        <section key={strand.id} className="mb-4">
          <p className="text-[11px] font-bold text-[#1A1A1A] dark:text-zinc-200 mb-2">{strand.name}</p>
          <div className="flex flex-wrap gap-1.5">
            {strand.subtopics.map(st => {
              const has = avail.topicLevel.has(`${st.id}|${level}`);
              const isCurrent = selection && selection.subjectId === subject.id && selection.level === level && selection.topicId === st.id;
              return (
                <button
                  key={st.id}
                  type="button"
                  disabled={!has}
                  onClick={() => has && onSelect({ subjectId: subject.id, level, topicId: st.id })}
                  className="rounded-full border-2 px-3 py-1.5 text-xs font-semibold transition-colors text-left"
                  style={{
                    borderColor: isCurrent ? COLORS.accent : has ? COLORS.border : '#e8e5e0',
                    backgroundColor: isCurrent ? COLORS.accentTint : has ? '#FFFFFF' : '#FAFAF8',
                    color: has ? '#1A1A1A' : '#b5ada3',
                    cursor: has ? 'pointer' : 'default',
                  }}
                >
                  {isCurrent && <Check size={11} className="inline -mt-0.5 mr-1" style={{ color: COLORS.accent }} />}
                  {st.name}
                  {!has && <span className="ml-1.5 text-[9px] font-semibold uppercase">soon</span>}
                </button>
              );
            })}
          </div>
        </section>
      ))}
    </div>
  );
};

export default SubjectPicker;
