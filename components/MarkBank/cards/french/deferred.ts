/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Mark Bank — French's deferred sittings (2022 and 2023, Higher and Ordinary).
 *
 * Each kind is built by its own reviewed generator with --deferred
 * (scripts/markbank/authoring/fr_reading.py, fr_writing.py, fr_cloze.py) into
 * its own file, beside June's and never inside it, so every June card and its
 * ledger stay as they were. Every card says it is deferred twice: its id
 * ("fr-2022-hl-deferred-reading-…") and its reference ("… — Deferred sitting").
 */
import type { FrenchRubric, SecRubricCard } from '../../../../types/markBank';
import reading from './deferred-reading.json';
import writing from './deferred-writing.json';
import cloze from './deferred-cloze.json';
import { withFrenchAnswers } from './answers';

export const FRENCH_DEFERRED_CARDS = ([...writing, ...reading, ...cloze] as (SecRubricCard & { rubric: FrenchRubric })[])
  .map(withFrenchAnswers);
export const deferredCardsForLevel = (level: 'higher' | 'ordinary'): SecRubricCard[] =>
  FRENCH_DEFERRED_CARDS.filter(card => card.level === level);
