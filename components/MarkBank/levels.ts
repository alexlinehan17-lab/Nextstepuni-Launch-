import type { SecCard } from '../../types/markBank';

export type Level = SecCard['level'];
export const levelName: Record<Level, string> = {
  higher: 'Higher', ordinary: 'Ordinary', foundation: 'Foundation',
};
export const levelAbbreviation: Record<Level, string> = {
  higher: 'HL', ordinary: 'OL', foundation: 'FL',
};
