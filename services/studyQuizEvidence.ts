/** Topic follow-up from actual quiz marks; card review dates remain Mark Bank's. */
import { examinationYearFromDate, findCanonicalTopic, resolveCurriculumSpecification, resolveSubjectId } from "../curriculumRegistry";
import { libraryTopicIds } from "../components/MarkBank/libraryGroups";
import type { SessionCardResult } from "../components/MarkBank/SessionScreen";
import type { SecCard } from "../types/markBank";
import type { StudyTopicSelection } from "../types/studyTopics";
import { canonicalNodeIds } from "./studyTopicHistory";
import { buildStudyPlan, dateKey, recordRetrieval, type TopicEvidence } from "./studyPlanEngine";
import { readStudyPlan, saveStudyPlan } from "./studyPlanStore";

export function recordStudyQuizResults(
  scope: string,
  selection: StudyTopicSelection | undefined,
  attempts: { card: SecCard; result: SessionCardResult }[],
  sessionId: string,
  now: number,
): void {
  const saved = readStudyPlan(scope);
  if (!saved || !selection || !Number.isFinite(now)) return;
  const profile = saved.inputs.profile;
  if (profile.curriculumLevel === "junior" || profile.yearGroup === "LCA1" || profile.yearGroup === "LCA2") return;
  const subject = profile.subjects.find(s => resolveSubjectId(s.subjectName) === resolveSubjectId(selection.subjectId));
  const spec = subject && resolveCurriculumSpecification(subject.subjectName, examinationYearFromDate(profile.examStartDate));
  if (!subject || !spec || spec.id !== selection.specificationId) return;
  const selected = new Set(selection.topicIds.flatMap(id => canonicalNodeIds(spec, id))
    .map(id => findCanonicalTopic(spec, id)?.id ?? id));
  const byTopic = new Map<string, SessionCardResult[]>();
  const seen = new Set<string>();
  for (const { card, result } of attempts) {
    if (seen.has(card.id) || card.id !== result.cardId || resolveSubjectId(card.subjectId) !== spec.subjectId
      || !Number.isFinite(result.marksAvailable) || result.marksAvailable <= 0
      || !Number.isFinite(result.marksClaimed) || result.marksClaimed < 0 || result.marksClaimed > result.marksAvailable) continue;
    seen.add(card.id);
    const mapped = libraryTopicIds(card, spec).map(id => findCanonicalTopic(spec, id)?.id);
    if (mapped.some(id => !id)) continue;
    const topics = [...new Set(mapped.filter((id): id is string => Boolean(id)))];
    // An aggregate mark spanning several topics cannot identify which one was
    // recalled. Those questions still update their actual Mark Bank card memory.
    if (topics.length !== 1 || !selected.has(topics[0])) continue;
    byTopic.set(topics[0], [...(byTopic.get(topics[0]) ?? []), result]);
  }
  const on = dateKey(new Date(now));
  const evidence = new Map(saved.inputs.evidence.map(e => [`${e.specificationId}::${e.topicId}`, e]));
  let changed = false;
  for (const [topicId, results] of byTopic) {
    const key = `${spec.id}::${topicId}`;
    const old = evidence.get(key);
    const previous = old?.assessment;
    if ((old?.observedOn && old.observedOn > on) || (previous && previous.recordedAt > now)
      || (previous?.sessionId === sessionId && previous.questionCount >= results.length)) continue;
    const marksClaimed = results.reduce((sum, r) => sum + r.marksClaimed, 0);
    const marksAvailable = results.reduce((sum, r) => sum + r.marksAvailable, 0);
    const result = marksClaimed === 0 ? "failed" : marksClaimed < marksAvailable ? "partial" : "self-assessed";
    const topic: TopicEvidence = old ?? {
      specificationId: spec.id, topicId, topicName: findCanonicalTopic(spec, topicId)!.title,
      subjectName: subject.subjectName, taught: true,
    };
    evidence.set(key, {
      ...recordRetrieval({ ...topic, taught: true }, result, on, profile.examStartDate),
      assessment: { source: "study-quiz", sessionId, recordedAt: now, questionCount: results.length, marksClaimed, marksAvailable },
    });
    changed = true;
  }
  if (!changed) return;
  const inputs = { ...saved.inputs, evidence: [...evidence.values()] };
  saveStudyPlan(scope, inputs, buildStudyPlan(inputs, saved.plan.start, saved.plan, on));
}
