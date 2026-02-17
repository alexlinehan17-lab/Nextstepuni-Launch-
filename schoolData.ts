/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

export const SCHOOLS = [
  { id: 'marino', name: 'Marino' },
  { id: 'joeys', name: "Joey's" },
  { id: 'larkin', name: 'Larkin' },
  { id: 'oconnells', name: "O'Connell's" },
  { id: 'mountcarmel', name: 'Mount Carmel' },
  { id: 'rosmini', name: 'Rosmini' },
] as const;

export type SchoolId = (typeof SCHOOLS)[number]['id'];

export function getSchoolName(id: string): string {
  const school = SCHOOLS.find(s => s.id === id);
  return school?.name ?? id;
}
