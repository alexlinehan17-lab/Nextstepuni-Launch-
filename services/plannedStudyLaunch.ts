import { readStudyPlan } from "./studyPlanStore";
import { studyTopicSelection } from "./studyTopicHistory";
import { queueTopicStudy } from "../utils/topicLaunch";
import { savePlannerTodos } from "../components/launchpad/plannerTodos";

/** Carry the actual task's instructions and canonical topic into the study room. */
export function preparePlannedStudy(
  uid: string,
  taskId: string,
  date: string,
): void {
  const saved = readStudyPlan(uid);
  const task = saved?.plan.tasks.find((t) => t.id === taskId);
  if (!saved || !task) return;
  savePlannerTodos(
    uid,
    date,
    taskId,
    task.steps.map((label) => ({ label })),
  );
  if (!task.topicKey) return;
  const [specificationId, topicId] = task.topicKey.split("::");
  const subject = saved.inputs.profile.subjects.find(
    (s) => s.subjectName === task.subjectName,
  );
  const selection = studyTopicSelection(
    task.subjectName,
    [topicId],
    saved.inputs.profile.examStartDate,
    subject?.level,
  );
  if (selection?.specificationId === specificationId)
    queueTopicStudy(uid, selection);
}
