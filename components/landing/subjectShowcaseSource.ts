/** Build-time inventory. Counts describe shipped content, not curriculum completeness. */
import { PAPER_TRAIL_INDEX, PAPER_TRAIL_SUBJECTS } from '../../paperTrailData';
import { SUBJECTS } from '../MarkBank/deck';
import sizesJson from '../MarkBank/cards/sizes.json';
import { subjectAtlasStats } from '../PaperTrail/topics';
import { resolveSubjectId } from '../../curriculumRegistry';
import type { PaperCycle } from '../../types/paperTrail';

export interface ShowcaseSubject {
  id: string; name: string; artworkSubject: string; cycle: PaperCycle;
  markBankCards: number; atlasQuestions: number; atlasTopics: number;
  paperCount: number; firstYear: number | null; lastYear: number | null;
}

export function buildSubjectShowcase(): ShowcaseSubject[] {
  const sizes = sizesJson as Record<string, Record<string, number>>;
  const bankSubjects = SUBJECTS.map(subject => ({
    id: subject.id, canonical: resolveSubjectId(subject.id) ?? subject.id, name: subject.title,
    cards: Object.values(sizes[subject.id] ?? {}).reduce((sum, n) => sum + n, 0),
  }));
  const represented = new Set<string>();
  const result: ShowcaseSubject[] = PAPER_TRAIL_SUBJECTS.map(subject => {
    const canonical = subject.curriculumId ?? subject.id;
    const bank = subject.cycle === 'lc' ? bankSubjects.find(item => item.canonical === canonical) : undefined;
    if (bank) represented.add(bank.id);
    const atlas = subjectAtlasStats(subject.id);
    const paperIds = new Set<string>();
    const years = new Set<number>();
    for (const entry of PAPER_TRAIL_INDEX[subject.id] ?? []) for (const paper of entry.papers) {
      if (paper.modified) continue;
      paperIds.add(`${entry.year}:${paper.doc.f}`); years.add(entry.year);
    }
    return { id: subject.id, name: bank?.name ?? subject.name,
      artworkSubject: canonical.replace(/^(?:jc|lca)-/, ''), cycle: subject.cycle,
      markBankCards: bank?.cards ?? 0, atlasQuestions: atlas.questions, atlasTopics: atlas.topics,
      paperCount: paperIds.size, firstYear: years.size ? Math.min(...years) : null, lastYear: years.size ? Math.max(...years) : null };
  });
  for (const bank of bankSubjects) if (!represented.has(bank.id) && bank.cards > 0) {
    const atlas = subjectAtlasStats(bank.canonical);
    result.push({ id: bank.canonical, name: bank.name, artworkSubject: bank.canonical, cycle: 'lc',
      markBankCards: bank.cards, atlasQuestions: atlas.questions, atlasTopics: atlas.topics,
      paperCount: 0, firstYear: null, lastYear: null });
  }
  // Presentation order only: open on the five characters featured in the design.
  const featured = ['irish', 'biology', 'music', 'ancient-greek', 'art'];
  const position = (subject: ShowcaseSubject) => subject.cycle === 'lc' && featured.includes(subject.id) ? featured.indexOf(subject.id) : featured.length;
  return result.filter(subject => subject.paperCount || subject.markBankCards || subject.atlasQuestions)
    .sort((a, b) => position(a) - position(b) || a.name.localeCompare(b.name, 'en-IE'));
}
