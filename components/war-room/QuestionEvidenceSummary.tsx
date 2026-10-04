import React from 'react';
import { evidenceForCurriculumNode } from '../PaperTrail/topicEvidence';
import { examinationYearFromDate, resolveCurriculumSpecification } from '../../curriculumRegistry';

export default function QuestionEvidenceSummary({ uid, subject, nodeId, examDate, level }: { uid: string; subject: string; nodeId?: string; examDate?: string | null; level: string }) {
  const spec = resolveCurriculumSpecification(subject, examinationYearFromDate(examDate));
  if (!spec || spec.status !== 'verified') return <p className="wr-muted">Question evidence is available when this subject has a verified curriculum map.</p>;
  const evidence = evidenceForCurriculumNode(uid, spec, nodeId, level);
  return <><strong className="wr-evidence-count">{evidence.marks.length} <small>scored {evidence.marks.length === 1 ? 'question' : 'questions'}</small></strong>
    <p className="wr-muted">{evidence.marks.length ? `${evidence.accuracy}% average self-mark. ` : 'No self-marks recorded here yet. '}{evidence.reviewed.length} question {evidence.reviewed.length === 1 ? 'card' : 'cards'} reviewed.</p><p className="wr-muted">Self-marks and review cards on this device.</p></>;
}
