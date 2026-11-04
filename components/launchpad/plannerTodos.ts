import type { PlanStep } from '../approved-ui-runtime';
export const plannerTodosKey = (uid: string, dateKey: string, blockId: string) => `nextstepuni:planner-todos:${uid}:${dateKey}:${blockId}`;
export function readPlannerTodos(uid: string, dateKey: string, blockId: string): PlanStep[] | null {
  try {
    const data: unknown = JSON.parse(localStorage.getItem(plannerTodosKey(uid, dateKey, blockId)) ?? 'null');
    return Array.isArray(data) && data.every(item => item && typeof item.label === 'string' && (item.done === undefined || typeof item.done === 'boolean')) ? data.map(item => ({ label: item.label, done: !!item.done })) : null;
  } catch { return null; }
}
export function savePlannerTodos(uid: string, dateKey: string, blockId: string, steps: PlanStep[]): boolean {
  try { localStorage.setItem(plannerTodosKey(uid, dateKey, blockId), JSON.stringify(steps)); return true; } catch { return false; }
}
