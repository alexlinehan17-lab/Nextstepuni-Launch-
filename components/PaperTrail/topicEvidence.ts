import { allMarks } from './attemptStore';
import { browseTopicIdsForQuestion, logicalQuestionIdentity, questionsForTopics, topicsForPaper, topicsForSubject } from './topics';
import { loadDeck } from './reviewStore';
import { examTopicTaxonomyFor } from '../../data/examTopics/registry';
import { canonicalNodeIds } from '../../services/studyTopicHistory';
import type { CanonicalCurriculumSpecification } from '../../curriculumRegistry';
import { PAPER_TRAIL_SUBJECTS } from '../../paperTrailData';
import type { PaperLevel, PaperLang } from '../../types/paperTrail';

/** Question evidence is counted by question, even when several topic links match. */
export function evidenceForCurriculumNode(uid: string | undefined, spec: CanonicalCurriculumSpecification, nodeId?: string, level?: string) {
  const practiceSubjectId = PAPER_TRAIL_SUBJECTS.find(subject => subject.cycle === 'lc' && subject.curriculumId === spec.subjectId)?.id ?? spec.subjectId;
  const nodes = nodeId ? new Set(canonicalNodeIds(spec, nodeId)) : undefined;
  const taxonomy = examTopicTaxonomyFor(practiceSubjectId);
  const matches = taxonomy?.topics.filter(topic => (!level || topic.level === level.toLowerCase()) && (!nodes || topic.curriculumNodeIds.some(id => nodes.has(id)))) ?? [];
  const browseIds = new Set(taxonomy ? matches.map(topic => topic.id) : nodes);
  const visible = topicsForSubject(practiceSubjectId).filter(topic => taxonomy || nodeId ? browseIds.has(topic.subtopicId) : true)
    .map(topic => level ? { ...topic, count: questionsForTopics(practiceSubjectId, [topic.subtopicId]).filter(question => question.level === level.toLowerCase()).length } : topic);
  const byQuestion = new Map<string, ReturnType<typeof allMarks>[number]>();
  // With no uid, do not aggregate other students' local attempts.
  for (const mark of uid ? allMarks(uid) : []) {
    if (mark.subjectId !== practiceSubjectId || (level && mark.level !== level.toLowerCase())) continue;
    const paper = topicsForPaper(mark.subjectId, mark.year, mark.level as PaperLevel, mark.lang as PaperLang, mark.fileid);
    const question = paper?.q.find(item => item.n === mark.n);
    if (!paper || !question || (nodeId && !browseTopicIdsForQuestion(paper, question).some(id => browseIds.has(id)))) continue;
    const key = logicalQuestionIdentity({ ...paper, n: mark.n });
    if (!byQuestion.has(key) || mark.ts > byQuestion.get(key)!.ts) byQuestion.set(key, mark);
  }
  const marks = [...byQuestion.values()].sort((a, b) => b.ts - a.ts);
  const accuracy = marks.length ? Math.round(marks.reduce((sum, mark) => sum + (mark.max > 0 ? mark.score / mark.max * 100 : mark.score), 0) / marks.length) : undefined;
  const reviewed = (uid ? loadDeck(uid) : []).filter(card => {
    if (card.subjectId !== practiceSubjectId || card.stability == null || (level && card.level !== level.toLowerCase())) return false;
    if (!nodeId) return true;
    const paper = topicsForPaper(card.subjectId, card.year, card.level, card.lang, card.fileid);
    const question = paper?.q.find(item => item.n === card.n);
    return Boolean(paper && question && browseTopicIdsForQuestion(paper, question).some(id => browseIds.has(id)));
  });
  return { marks, accuracy, reviewed, topics: visible, practiceSubjectId };
}
