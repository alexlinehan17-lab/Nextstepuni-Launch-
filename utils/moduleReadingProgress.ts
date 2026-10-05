import type { ModuleProgress, SectionDefinition } from '../types';

export type ReadingMode = 'full' | 'essentials';

export function readSectionIds(progress: ModuleProgress, sections: Pick<SectionDefinition, 'id'>[], mode: ReadingMode): Set<string> {
  const stored = progress.reading?.sectionsByMode[mode];
  if (stored) return new Set(stored.filter(id => sections.some(section => section.id === id)));
  // Honour historical reading records, but never infer that a newly introduced
  // reading mode has been read from the other mode's checkpoints.
  if (progress.reading) return new Set();
  return new Set(sections.slice(0, Math.max(0, progress.unlockedSection)).map(section => section.id));
}

export function readingCheckpoint(progress: ModuleProgress, sections: Pick<SectionDefinition, 'id'>[], mode: ReadingMode, index: number, markRead: boolean, fullCount = sections.length, now = new Date().toISOString()): ModuleProgress {
  const section = sections[index];
  if (!section) return progress;
  const read = readSectionIds(progress, sections, mode);
  if (markRead) read.add(section.id);
  const compatibleCount = read.size === sections.length ? fullCount : read.size;
  return {
    ...progress,
    unlockedSection: Math.max(progress.unlockedSection, compatibleCount),
    reading: {
      sectionsByMode: { ...progress.reading?.sectionsByMode, [mode]: [...read] },
      lastSectionId: section.id, lastSectionIndex: index, lastMode: mode, lastVisitedAt: now,
    },
  };
}

export function resumeSection(progress: ModuleProgress, sections: Pick<SectionDefinition, 'id'>[], mode: ReadingMode): number {
  if (progress.reading?.lastMode === mode) {
    const found = sections.findIndex(section => section.id === progress.reading?.lastSectionId);
    if (found >= 0) return found;
  }
  const read = readSectionIds(progress, sections, mode);
  const firstUnread = sections.findIndex(section => !read.has(section.id));
  return firstUnread < 0 ? 0 : firstUnread;
}
