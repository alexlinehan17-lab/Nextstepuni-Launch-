/** @license SPDX-License-Identifier: Apache-2.0 */
import type { SecRubricCard, PhysicalEducationRubric } from '../../../../types/markBank';
import reviewed from './reviewed.json';
import { withPhysicalEducationAnswers } from './answers';

/** Each reviewed card with its criteria cut into bands and rows where the guidance prices them (answers.ts). */
export const REVIEWED_CARDS = (reviewed.cards as (SecRubricCard & { rubric: PhysicalEducationRubric })[]).map(withPhysicalEducationAnswers);

