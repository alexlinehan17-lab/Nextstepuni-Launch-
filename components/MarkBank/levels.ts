import { examinationYearFromDate, resolveCurriculumSpecification } from '../../curriculumRegistry';
import type { MarkBankLevel } from '../../types/markBank';

export function levelsForSubject(subjectId: string, examYear = examinationYearFromDate()): MarkBankLevel[] {
  return (resolveCurriculumSpecification(subjectId, examYear)?.levels ?? [])
    .filter((level): level is MarkBankLevel => level === 'higher' || level === 'ordinary' || level === 'foundation');
}
