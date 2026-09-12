import { PAPER_TRAIL_INDEX } from '../../paperTrailData';
import { browseTopicIdsForQuestion, topicLabel, topicsForPaper } from '../../components/PaperTrail/topics';
import { findCanonicalTopic, resolveCurriculumSpecification } from '../../curriculumRegistry';
import type { AskIndexFile, AskTopicIndexFile } from '../../components/landing/fx-e/ask';

/** Exact subject/year/level/language/booklet/question joins. Topic rows do not
 * depend on the separate text parser having found or numbered a question.
 */
export function buildAskTopicIndex(
  index: AskIndexFile,
  anchorsFor: (year: number, fileid: string) => Map<string, number>,
): AskTopicIndexFile {
  const out: AskTopicIndexFile = { topics: [], papers: [], q: [] };
  const topicIndices = new Map<string, number>();
  const addTopic = (id: string, label: string, aliases: string[] = []): number => {
    const existing = topicIndices.get(id);
    if (existing !== undefined) return existing;
    const i = out.topics.length;
    topicIndices.set(id, i);
    out.topics.push({ id, label, aliases });
    return i;
  };
  for (const subject of index.subjects) {
    for (const entry of PAPER_TRAIL_INDEX[subject.id] ?? []) {
      if (entry.level !== 'higher' || entry.lang !== 'ev' || !index.years.includes(entry.year)) continue;
      const spec = resolveCurriculumSpecification(subject.id, entry.year);
      for (const item of entry.papers) {
        const tags = topicsForPaper(subject.id, entry.year, entry.level, entry.lang, item.doc.f);
        if (!tags?.q.length) continue;
        const pi = out.papers.length;
        out.papers.push({ subjectId: subject.id, y: entry.year, l: 'H', f: item.doc.f, p: item.label.replace(/\s*\/.*$/, '') });
        const anchors = anchorsFor(entry.year, item.doc.f);
        for (const question of tags.q) {
          const ids = new Set<number>();
          for (const id of browseTopicIdsForQuestion(tags, question)) {
            ids.add(addTopic(id, topicLabel(id)));
          }
          // Include the canonical syllabus label as well as the student-facing
          // exam topic. E.g. Trigonometry still finds Sine/Cosine Rule questions.
          for (const id of [question.primary, question.secondary]) {
            if (!id) continue;
            // Retain the committed tag too: a newer browse crosswalk can group
            // an older Trigonometry question under the broader Geometry label.
            const sourceKey = `papertrail/${id}`;
            ids.add(addTopic(sourceKey, topicLabel(id)));
            if (!spec) continue;
            const topic = findCanonicalTopic(spec, id);
            if (!topic) continue;
            const key = `${spec.id}/${topic.id}`;
            ids.add(addTopic(key, topic.title, topic.aliases));
          }
          if (ids.size) out.q.push([pi, question.n, anchors.get(question.n) ?? 0, [...ids]]);
        }
      }
    }
  }
  return out;
}
