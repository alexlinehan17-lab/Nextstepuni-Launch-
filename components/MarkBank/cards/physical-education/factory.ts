/** @license SPDX-License-Identifier: Apache-2.0 */
import type { SecRubricCard, PhysicalEducationRubric } from '../../../../types/markBank';
import reviewed from './reviewed.json';

export const REVIEWED_CARDS = reviewed.cards as (SecRubricCard & { rubric: PhysicalEducationRubric })[];
