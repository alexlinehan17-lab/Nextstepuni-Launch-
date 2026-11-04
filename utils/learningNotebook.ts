export interface SavedTakeaway { id: string; text: string; sectionTitle: string; sectionIndex: number; mode: 'full' | 'essentials'; savedAt: string }
export interface NotebookEntry { title: string; notes: string; takeaways: SavedTakeaway[] }
export const LEARNING_NOTEBOOK_NAMESPACE = '_learningNotebook';
export function notebookEntry(value: unknown, title: string): NotebookEntry {
  const data = value && typeof value === 'object' ? value as Partial<NotebookEntry> : {};
  return { title, notes: typeof data.notes === 'string' ? data.notes : '', takeaways: Array.isArray(data.takeaways) ? data.takeaways.filter(item => item && typeof item.text === 'string' && typeof item.sectionIndex === 'number') : [] };
}
