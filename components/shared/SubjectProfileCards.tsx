import React from 'react';
import SubjectAvatar from '../SubjectAvatar';
import { LC_SUBJECTS, SUBJECT_GROUP_LABELS, getGradeIndex, getGradesForLevel, getPointsForGrade, type Grade, type Level, type LCSubject } from '../subjectData';

export interface GradeConfig { level: Level; currentGrade: Grade; targetGrade: Grade }
export function SubjectCardPicker({ groups, selected, onToggle }: { groups: Record<string, LCSubject[]>; selected: Set<string>; onToggle: (name: string) => void }) {
  return <>{Object.entries(groups).map(([group, subjects]) => <section key={group} className="sc-subject-group">
    <p className="sc-eyebrow">{SUBJECT_GROUP_LABELS[group as LCSubject['group']]}</p>
    <div className="sc-subject-grid">{subjects.map(subject => <button key={subject.name} type="button" className="sc-subject" aria-label={subject.name} aria-pressed={selected.has(subject.name)} onClick={() => onToggle(subject.name)}>
      <SubjectAvatar subject={subject.name} /><span>{subject.name}</span><small>{selected.has(subject.name) ? 'Added' : 'Add'}</small>
    </button>)}</div>
  </section>)}</>;
}

export function SubjectGradeCards({ selected, configs, onUpdate }: { selected: Set<string>; configs: Record<string, GradeConfig>; onUpdate: (name: string, field: 'level' | 'currentGrade' | 'targetGrade', value: string) => void }) {
  return <>{Array.from(selected).map(name => {
    const config = configs[name] || { level: 'higher' as Level, currentGrade: 'H4' as Grade, targetGrade: 'H2' as Grade };
    const grades = getGradesForLevel(config.level);
    const currentIndex = getGradeIndex(config.currentGrade);
    const isMaths = LC_SUBJECTS.find(subject => subject.name === name)?.isMaths || false;
    const gain = getPointsForGrade(config.targetGrade, isMaths) - getPointsForGrade(config.currentGrade, isMaths);
    return <section key={name} className="sc-grade-card">
      <header className="sc-grade-header"><h3>{name}</h3><div className="sc-levels" role="group" aria-label={`${name} level`}>
        {(['higher','ordinary'] as const).map(level => <button key={level} type="button" className="sc-level" aria-pressed={config.level === level} onClick={() => onUpdate(name, 'level', level)}>{level === 'higher' ? 'Higher' : 'Ordinary'}</button>)}
      </div></header>
      {(['currentGrade','targetGrade'] as const).map(field => <div key={field}>
        <p className={`sc-grade-label${field === 'targetGrade' ? ' sc-target-label' : ''}`}>{field === 'currentGrade' ? 'Where I am now' : 'My target'}</p>
        <div className="sc-grade-options" role="group" aria-label={`${name} ${field === 'currentGrade' ? 'current grade' : 'target grade'}`}>
          {grades.map((grade,index) => <button key={grade} type="button" className={`sc-grade${field === 'targetGrade' ? ' sc-grade--target' : ''}`} aria-pressed={config[field] === grade} disabled={field === 'targetGrade' && index > currentIndex} onClick={() => onUpdate(name,field,grade)}>{grade}</button>)}
        </div>
      </div>)}
      {getGradeIndex(config.targetGrade) < currentIndex && <p className="sc-grade-result"><span>{config.currentGrade} → {config.targetGrade}</span><span>+{gain} pts</span></p>}
    </section>;
  })}</>;
}
