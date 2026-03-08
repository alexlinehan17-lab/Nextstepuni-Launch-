/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

export interface KudosMessage {
  id: string;
  text: string;
  emoji: string;
}

export const KUDOS_MESSAGES: KudosMessage[] = [
  { id: 'k1',  text: 'Your island is class!',    emoji: '🏝️' },
  { id: 'k2',  text: 'Keep building!',           emoji: '🔨' },
  { id: 'k3',  text: 'Love the layout!',         emoji: '✨' },
  { id: 'k4',  text: 'So creative!',             emoji: '🎨' },
  { id: 'k5',  text: 'Deadly island!',           emoji: '🔥' },
  { id: 'k6',  text: 'Fair play!',               emoji: '👏' },
  { id: 'k7',  text: 'You\'re smashing it!',     emoji: '💪' },
  { id: 'k8',  text: 'Inspired by this!',        emoji: '💡' },
  { id: 'k9',  text: 'Goals!',                   emoji: '🎯' },
  { id: 'k10', text: 'Unreal progress!',         emoji: '🚀' },
  { id: 'k11', text: 'Looks amazing!',           emoji: '🤩' },
  { id: 'k12', text: 'Well done!',               emoji: '⭐' },
];
