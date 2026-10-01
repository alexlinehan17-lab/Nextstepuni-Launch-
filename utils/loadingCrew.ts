import { getPersonalStarCrew, PERSONAL_STAR_CREW } from '../data/personalStarCrew';

/** Hugger joins the random pool only when this person explicitly chose it. */
export function pickLoadingCrew(selectedAvatar?: string, draw: number = Math.random()) {
  const pool = PERSONAL_STAR_CREW.filter(crew => crew.id !== 'star-crew:hugger' || selectedAvatar === crew.id);
  const index = Math.min(pool.length - 1, Math.max(0, Math.floor((Number.isFinite(draw) ? draw : 0) * pool.length)));
  return pool[index];
}

export function resolveLoadingCrew(selection: 'personal' | 'random', selectedAvatar?: string, draw?: number) {
  return (selection === 'personal' && getPersonalStarCrew(selectedAvatar ?? '')) || pickLoadingCrew(selectedAvatar, draw);
}
