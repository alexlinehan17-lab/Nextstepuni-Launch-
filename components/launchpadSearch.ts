export const PRACTICE_TOOL_IDS = new Set(['mark-bank', 'paper-trail', 'topic-atlas', 'command-word-reflex']);
const aliases: Record<string, string> = {
  'paper-trail': 'past papers exam questions marking schemes SEC',
  'topic-atlas': 'past papers topics exam questions',
  'mark-bank': 'exam practice questions flashcards spaced repetition',
  planner: 'weekly study plan schedule calendar timetable',
  comeback: 'fallen behind restart catch up',
  'college-compass': 'college applications CAO deadlines',
};
export function matchesToolSearch(tool: { id: string; title: string; description: string; tag: string }, query: string): boolean {
  const searchable = `${tool.title} ${tool.description} ${tool.tag} ${aliases[tool.id] ?? ''}`.normalize('NFKD').replace(/[\u0300-\u036f]/g, '').toLowerCase();
  return query.normalize('NFKD').replace(/[\u0300-\u036f]/g, '').toLowerCase().trim().split(/\s+/).every(word => searchable.includes(word));
}
