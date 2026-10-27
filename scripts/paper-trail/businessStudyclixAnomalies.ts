/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Business StudyClix headings whose topic the SEC paper and scheme do not
 * support. Bundled and run by build-business-studyclix-anomalies.mjs.
 *
 * Every Business question's 1999-syllabus topics were set by direct review of
 * the SEC paper and marking scheme (data/examTopics/business-source-reviewed-
 * topics.json). Where StudyClix files a heading under an outgoing-course topic
 * that review did not give the question, the heading is recorded as a reviewed
 * reference-anomaly with its reason, never matched and never silently skipped.
 * StudyClix is a cross-check, not the authority.
 */
import { browseTopicIdsForQuestion, topicsForPaper } from '../../components/PaperTrail/topics';
import { examTopicDefinition } from '../../data/examTopics/registry';

interface Target { level: 'higher' | 'ordinary'; lang: 'ev'; year: number; paperKey: string; fileid: string; questionNumber: string }
interface Association { topicId: string; heading: string; course: string; resolution: string; target?: Target }
interface Review { year: number; level: string; paperKey: string; n: string; canonicalNodeIds: string[]; reason: string }
interface Card { year: number; level: string; questionRef: string; questionText: string }

export interface BusinessStudyclixAnomaly {
  topicId: string;
  heading: string;
  secTopicIds: string[];
  reason: string;
}

const LEVEL = { higher: 'HL', ordinary: 'OL' } as const;

/** The citation the reviewed cards carry for a question: "2013 HL Section 3 Q1". */
function citation(level: 'higher' | 'ordinary', year: number, paperKey: string, n: string): string {
  const base = `${year} ${LEVEL[level]}`;
  if (n === 'ABQ') return `${base} Section 2 ABQ`;
  const section = /^S(\d)Q(\d+)$/.exec(n);
  if (section) return `${base} Section ${section[1]} Q${section[2]}`;
  if (paperKey === 'p2') return `${base} Section ${level === 'higher' ? 3 : 2} Q${n}`;
  return `${base} Section 1 Q${n}`;
}

/** The printed part a heading names ("- Part B", "- Part (a)"), if any. */
function headingPart(heading: string): string | null {
  const part = /- Part \(?([A-Ea-e])\)?\s*$/.exec(heading);
  return part ? part[1].toUpperCase() : null;
}

/** First sentence of the printed ask, as lifted onto the reviewed card. */
function opening(text: string): string {
  const flat = text.replace(/\s+/g, ' ').trim();
  const sentence = /^(.{20,}?[.?!])(\s|$)/.exec(flat)?.[1] ?? flat;
  return sentence.length > 160 ? `${sentence.slice(0, 157).trimEnd()}…` : sentence;
}

const label = (id: string) => examTopicDefinition(id)?.label ?? id;

export function businessStudyclixAnomalies(
  associations: Association[],
  reviews: Review[],
  cards: Card[],
): BusinessStudyclixAnomaly[] {
  const out: BusinessStudyclixAnomaly[] = [];
  for (const association of associations) {
    if (association.resolution !== 'matched' && association.resolution !== 'reference-anomaly') continue;
    const target = association.target;
    if (!target) throw new Error(`${association.topicId}|${association.heading}: no target`);
    const paper = topicsForPaper('business', target.year, target.level, 'ev', target.fileid);
    const question = paper?.q.find(candidate => candidate.n === target.questionNumber);
    if (!paper || !question) throw new Error(`${association.heading}: no paper card ${target.fileid} Q${target.questionNumber}`);
    const browse = browseTopicIdsForQuestion(paper, question);
    if (browse.includes(association.topicId)) continue;
    if (association.course !== 'old') {
      throw new Error(`${association.topicId}|${association.heading}: a redeveloped-course join is missing, not a reviewed difference`);
    }
    const review = reviews.find(item => item.year === target.year && item.level === target.level
      && item.paperKey === target.paperKey && item.n === target.questionNumber);
    if (!review) throw new Error(`${association.heading}: differs from StudyClix without a direct SEC review`);
    const secTopicIds = browse.filter(id => examTopicDefinition(id)?.course === 'old');
    if (!secTopicIds.length) throw new Error(`${association.heading}: no reviewed outgoing-course topic`);
    const cite = citation(target.level, target.year, target.paperKey, target.questionNumber);
    const part = headingPart(association.heading);
    const questionCards = cards.filter(card => card.year === target.year && card.level === target.level
      && (card.questionRef === cite || card.questionRef.startsWith(`${cite}(`)));
    const partCards = part ? questionCards.filter(card => card.questionRef.startsWith(`${cite}(${part})`)) : [];
    const quoted = (partCards[0] ?? questionCards[0]);
    if (!quoted) throw new Error(`${association.heading}: no reviewed card for ${cite}`);
    const levelName = target.level === 'higher' ? 'Higher' : 'Ordinary';
    out.push({
      topicId: association.topicId,
      heading: association.heading,
      secTopicIds,
      reason: `StudyClix files this ${target.year} ${levelName} heading under ${label(association.topicId)}. `
        + `The SEC paper and marking scheme support ${secTopicIds.map(label).join('; ')}: `
        + `${quoted.questionRef} asks “${opening(quoted.questionText)}” `
        + `Source review: ${review.reason} `
        + 'NextStepUni keeps the reviewed tags for this question; the reference association is retained here as an audited anomaly.',
    });
  }
  return out;
}
