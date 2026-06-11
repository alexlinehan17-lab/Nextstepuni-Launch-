/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Subject-name helpers shared by the subject-picker tools (Catch-Up Lane,
 * Command-Word Reflex, Paper Trail). One place for the cycle-parenthetical
 * stripping so a student's chosen subject names match content subjectLabels
 * across cycles.
 */

/**
 * Match a student's chosen subject name (e.g. "Science") to a content
 * subjectLabel (e.g. "Science (Junior Cycle)" or "Irish (Gaeilge)") by
 * stripping the trailing cycle/variant parenthetical. Without this, JC
 * students' subjects never match the JC-labelled content, so their built
 * subjects wrongly show as "coming soon".
 */
export const baseName = (s: string) => s.toLowerCase().replace(/\s*\([^)]*\)\s*$/, '').trim();

/**
 * Display label with the trailing cycle/variant parenthetical stripped — once
 * the picker is filtered to one cycle, "(Junior Cycle)" / "(Gaeilge)" is
 * redundant noise. "Science (Junior Cycle)" → "Science", "Irish (Gaeilge)" → "Irish".
 */
export const displayName = (label: string) => label.replace(/\s*\([^)]*\)\s*$/, '').trim();
