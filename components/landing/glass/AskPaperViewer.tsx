import React from 'react';
import { PAPER_TRAIL_INDEX } from '../../../paperTrailData';
import Viewer from '../../PaperTrail/Viewer';
import { paperAnswersPath, paperStoragePath, paperUrl } from '../../PaperTrail/storage';
import { topicsForPaper } from '../../PaperTrail/topics';
import type { AskQuestion } from '../fx-e/ask';

/** Both search modes open the real reader. Text hits use their extracted page;
 * topic hits use Paper Trail's exact booklet + question identity and anchors.
 */
export default function AskPaperViewer({ question: q, onClose }: { question: AskQuestion; onClose: () => void }) {
  const level = q.paper.l === 'H' ? 'higher' : 'ordinary';
  const entry = PAPER_TRAIL_INDEX[q.subject.id]?.find(e => e.year === q.paper.y && e.level === level && e.lang === 'ev' && e.papers.some(p => p.doc.f === q.paper.f));
  const item = entry?.papers.find(p => p.doc.f === q.paper.f);
  const url = (kind: 'paper' | 'scheme', file: string) => paperUrl(paperStoragePath('lc', q.subject.id, q.paper.y, kind, file));
  return <Viewer
    title={`${q.subject.name} · ${q.paper.y}`}
    subtitle={`${q.paper.p || 'Exam paper'} · ${level === 'higher' ? 'Higher' : 'Ordinary'} level`}
    paper={{ url: url('paper', q.paper.f), label: q.paper.p || 'Exam paper', bytes: item?.doc.b ?? 0 }}
    scheme={item?.scheme ? { url: url('scheme', item.scheme.f), label: 'Marking scheme', bytes: item.scheme.b } : undefined}
    answersUrl={item?.answers ? paperUrl(paperAnswersPath('lc', q.subject.id, q.paper.y, q.paper.f)) : undefined}
    topics={topicsForPaper(q.subject.id, q.paper.y, level, 'ev', q.paper.f) ?? undefined}
    focusQuestion={q.anchor}
    focusAnchorsUrl={q.anchor ? `/paper-anchors/${q.paper.y}/${q.paper.f}.json` : undefined}
    initialPaperPage={q.page || 1}
    initialAnswersOn={Boolean(item?.answers)}
    onClose={onClose}
  />;
}
