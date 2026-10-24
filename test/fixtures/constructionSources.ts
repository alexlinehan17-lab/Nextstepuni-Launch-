/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */
import fs from 'node:fs';
import { execFileSync } from 'node:child_process';

/* The source-pinned Construction Studies validators
 * (scripts/markbank/authoring/construction_<year>_<level>.py) hash and read the
 * original SEC paper and marking scheme PDFs. Those PDFs are not in the
 * repository (paper-trail-corpus is a local, gitignored corpus) and CI has none,
 * so a validator run is skipped where its two PDFs or PyMuPDF are absent. Every
 * other Construction check (identities, deck, figures, topic bindings) still
 * runs from the committed files. */
const FILEID = { higher: 'LC029ALP000EV.pdf', ordinary: 'LC029GLP000EV.pdf' } as const;

const hasPyMuPDF = (() => {
  try {
    execFileSync('python3', ['-c', 'import fitz'], { stdio: 'ignore' });
    return true;
  } catch {
    return false;
  }
})();

export const hasConstructionSources = (year: number, level: 'higher' | 'ordinary'): boolean => hasPyMuPDF
  && fs.existsSync(`paper-trail-corpus/exampapers/${year}/${FILEID[level]}`)
  && fs.existsSync(`paper-trail-corpus/markingschemes/${year}/${FILEID[level]}`);
