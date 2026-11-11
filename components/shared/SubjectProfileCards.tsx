import React from 'react';
import SubjectAvatar from '../SubjectAvatar';
import { LC_SUBJECTS, JC_BANDS, LEVEL_LABELS, SUBJECT_GROUP_LABELS, fixedLevelNote, getGradesForLevel, getPointsForGrade, gradeRank, subjectLevels, subjectProgramme, subjectUsesExamGrades, subjectAssessmentNote, targetGradesFor, type Grade, type Level, type LCSubject, type YearGroup, type SubjectProgramme } from '../subjectData';
import { newSubjectConfig, type GradeConfig, type SubjectConfigField } from './subjectProfileModel';
export type { GradeConfig } from './subjectProfileModel';

export function SubjectCardPicker({ groups, selected, onToggle }: { groups: Record<string, LCSubject[]>; selected: Set<string>; onToggle: (name: string) => void }) {
  return <>{Object.entries(groups).map(([group, subjects]) => <section key={group} className="sc-subject-group">
    <p className="sc-eyebrow">{SUBJECT_GROUP_LABELS[group as LCSubject['group']]}</p>
    <div className="sc-subject-grid">{subjects.map(subject => <button key={subject.name} type="button" className="sc-subject" aria-label={subject.label ?? subject.name} aria-pressed={selected.has(subject.name)} onClick={() => onToggle(subject.name)}>
      <SubjectAvatar subject={subject.name} /><span>{subject.label ?? subject.name}</span><small>{selected.has(subject.name) ? 'Added' : 'Add'}</small>
    </button>)}</div>
  </section>)}</>;
}

export function SubjectGradeCards({ selected, configs, onUpdate, yearGroup, programme = subjectProgramme(yearGroup) }: { programme?: SubjectProgramme; yearGroup?: YearGroup; selected: Set<string>; configs: Record<string, GradeConfig>; onUpdate: (name: string, field: SubjectConfigField, value: string) => void }) {
  return <>{Array.from(selected).map(name => {
    const config = configs[name] || newSubjectConfig(programme, name);
    const junior = programme === 'jc';
    const lca = programme === 'lca';
    const levels = subjectLevels(programme, name);
    if (!subjectUsesExamGrades(programme, name)) return <section key={name} className="sc-grade-card"><header className="sc-grade-header"><h3>{name}</h3></header><p className="sc-small">{subjectAssessmentNote(programme, name)}</p></section>;
    const validLevel = levels.includes(config.level);
    const levelNote = junior || lca ? null : fixedLevelNote(name);
    const grades = junior ? JC_BANDS : getGradesForLevel(config.level);
    const targetGrades = junior ? JC_BANDS : targetGradesFor(config.level);
    const isMaths = LC_SUBJECTS.find(subject => subject.name === name)?.isMaths || false;
    const gain = getPointsForGrade(config.targetGrade, isMaths) - getPointsForGrade(config.currentGrade, isMaths);
    return <section key={name} className="sc-grade-card">
      <header className="sc-grade-header"><h3>{name}</h3>{levels.length > 1 ? <div className="sc-levels" role="group" aria-label={`${name} level`}>
        {levels.map((level: Level) => <button key={level} type="button" className="sc-level" aria-pressed={config.level === level} onClick={() => onUpdate(name, 'level', level)}>{LEVEL_LABELS[level]}</button>)}
      </div> : null}</header>
      {levelNote && <p className="sc-small">{levelNote}</p>}
      {!validLevel && <p className="sc-small">Choose your level. Grades can be added later.</p>}
      {validLevel && (junior ? ['currentBand','targetBand'] as const : ['currentGrade','targetGrade'] as const).map(field => <div key={field}>
        <p className={`sc-grade-label${(field === 'targetGrade' || field === 'targetBand') ? ' sc-target-label' : ''}`}>{(field === 'currentGrade' || field === 'currentBand') ? 'Where I am now' : 'My target'}</p>
        <div className="sc-grade-options" role="group" aria-label={`${name} ${(field === 'currentGrade' || field === 'currentBand') ? junior ? 'current band' : 'current grade' : junior ? 'target band' : 'target grade'}`}>
          {((field === 'targetGrade' || field === 'targetBand') ? targetGrades : grades).map(grade => <button key={grade} type="button" className={`sc-grade${(field === 'targetGrade' || field === 'targetBand') ? ' sc-grade--target' : ''}`} aria-pressed={config[field] === grade} disabled={!junior && field === 'targetGrade' && gradeRank(grade as Grade) < gradeRank(config.currentGrade)} onClick={() => onUpdate(name,field,grade)}>{grade}</button>)}
        </div>
      </div>)}
      {!lca && !junior && gradeRank(config.targetGrade) > gradeRank(config.currentGrade) && <p className="sc-grade-result"><span>{config.currentGrade} → {config.targetGrade}</span><span>+{gain} pts</span></p>}
    </section>;
  })}</>;
}
