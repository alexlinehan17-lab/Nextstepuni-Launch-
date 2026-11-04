#!/usr/bin/env node
/** Expand the same finite Business pools used by the runtime and generator. */
import { readFileSync } from 'node:fs';
import { createHash } from 'node:crypto';
import { fileURLToPath } from 'node:url';
import { expandBusinessRoutePools } from '../../../components/MarkBank/cards/business/routes.mjs';

const root = new URL('../../../', import.meta.url);
const data = JSON.parse(readFileSync(new URL('components/MarkBank/cards/business/route-pools.json', root), 'utf8'));
for (const pool of data.pools) {
  for (const [kind, source] of Object.entries(pool.review.sources)) {
    const bytes = readFileSync(new URL(`paper-trail-corpus/${kind}/${pool.template.year}/${source.fileid}`, root));
    if (createHash('sha256').update(bytes).digest('hex') !== source.sha256) {
      throw new Error(`Business route source changed: ${pool.id} ${kind}`);
    }
  }
}
if (process.argv[1] === fileURLToPath(import.meta.url)) {
  process.stdout.write(JSON.stringify(expandBusinessRoutePools(data.pools)));
}
