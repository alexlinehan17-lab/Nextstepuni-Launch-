import {
  JC_BANDS, defaultGradesForLevel, defaultSubjectConfig, getGradesForLevel, gradeRank,
  subjectLevels, subjectUsesExamGrades, targetGradesFor,
  type Grade, type JCBand, type Level, type StudentSubject, type SubjectProgramme,
} from '../subjectData';

export type GradeConfig = Omit<StudentSubject, 'subjectName'>;
export type SubjectConfigField = 'level' | 'currentGrade' | 'targetGrade' | 'currentBand' | 'targetBand';

export function newSubjectConfig(programme: SubjectProgramme, name: string): GradeConfig {
  if (!subjectUsesExamGrades(programme, name)) return { level: 'common' };
  if (programme === 'lc') return defaultSubjectConfig(name);
  // Common is deliberately invalid for courses requiring an explicit H/O/F choice.
  // It keeps the existing control shape while requiring the student to choose.
  const levels = subjectLevels(programme, name);
  return { level: levels.length === 1 ? levels[0] : 'common' };
}

export function updateSubjectConfig(programme: SubjectProgramme, name: string, config: GradeConfig, field: SubjectConfigField, value: string): GradeConfig {
  if (field === 'level') {
    const level = value as Level;
    if (!subjectLevels(programme, name).includes(level)) return config;
    if (programme === 'jc') return { ...config, level };
    return programme === 'lc' && subjectUsesExamGrades(programme, name)
      ? { level, ...defaultGradesForLevel(level) } : { level };
  }
  if (field === 'currentBand' || field === 'targetBand') {
    if (programme !== 'jc' || !JC_BANDS.includes(value as JCBand)) return config;
    return { ...config, [field]: value as JCBand };
  }
  const next = { ...config, [field]: value as Grade };
  if (field === 'currentGrade' && gradeRank(next.targetGrade) < gradeRank(next.currentGrade)) next.targetGrade = next.currentGrade;
  return next;
}

export function saveSubjectConfig(programme: SubjectProgramme, name: string, config: GradeConfig): StudentSubject {
  if (!subjectUsesExamGrades(programme, name)) return { subjectName: name, level: 'common' };
  if (!subjectLevels(programme, name).includes(config.level)) throw new Error(`Choose a level for ${name}.`);
  const base = { subjectName: name, level: config.level };
  if (programme === 'jc') return { ...base,
    ...(config.currentBand && JC_BANDS.includes(config.currentBand) ? { currentBand: config.currentBand } : {}),
    ...(config.targetBand && JC_BANDS.includes(config.targetBand) ? { targetBand: config.targetBand } : {}),
  };
  return { ...base,
    ...(config.currentGrade && getGradesForLevel(config.level).includes(config.currentGrade) ? { currentGrade: config.currentGrade } : {}),
    ...(config.targetGrade && targetGradesFor(config.level).includes(config.targetGrade) ? { targetGrade: config.targetGrade } : {}),
  };
}
