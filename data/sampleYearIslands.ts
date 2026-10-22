/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * SAMPLE classmates for the localhost Demo Account and the year-islands dev
 * harness. Every name and island here is invented; none is a real student and
 * nothing is read from or written to Firestore. Loaded with a dynamic import,
 * so it never ships in the chunk a signed-in student downloads.
 *
 * Each island is grown with the real placement rule (canBuildPaper) from the
 * real starter island, then passed through the server's own publicTiles(), so
 * what the harness draws is exactly what a projection would carry.
 */
import { canBuildPaper, createPaperIsland, NEIGHBOURS, PAPER_EDGES, type PaperIsland, type PaperTile } from '../functions/src/paperIslandModel';
import { publicTiles } from '../functions/src/islandProjection';
import type { TileKind } from '../functions/src/paperCatalogue';
import type { PaperVisitorId } from '../functions/src/paperVisitors';
import type { YearIsland } from '../components/journey/year/yearIslands';

export const SAMPLE_COHORT = { school: 'marino', yearGroup: '5th' as const };

function seeded(seed: number) {
  let state = seed >>> 0;
  return () => {
    state = (Math.imul(state, 1664525) + 1013904223) >>> 0;
    return state / 0x100000000;
  };
}

function grow(seed: number, kinds: (TileKind | { wonder: PaperVisitorId })[]): PaperTile[] {
  const random = seeded(seed);
  const tiles = [...createPaperIsland().tiles];
  kinds.forEach((entry, index) => {
    const open = new Map<string, { q: number; r: number }>();
    for (const tile of tiles)
      for (const [dq, dr] of NEIGHBOURS) {
        const q = tile.q + dq, r = tile.r + dr;
        if (canBuildPaper(tiles, q, r)) open.set(`${q},${r}`, { q, r });
      }
    const spots = [...open.values()].sort((a, b) =>
      Math.max(Math.abs(a.q), Math.abs(a.r), Math.abs(a.q + a.r)) - Math.max(Math.abs(b.q), Math.abs(b.r), Math.abs(b.q + b.r)) || a.r - b.r || a.q - b.q);
    const spot = spots[Math.min(spots.length - 1, Math.floor(random() * Math.min(7, spots.length)))];
    if (!spot) return;
    const wonder = typeof entry === 'object' ? entry.wonder : undefined;
    const kind = wonder ? 'meadow' : entry as TileKind;
    tiles.push({
      id: `sample-${seed}-${index}`,
      q: spot.q,
      r: spot.r,
      kind: kind === 'capybara' ? 'water' : kind,
      ...(kind === 'capybara' ? { appearance: 'capybara' as const } : {}),
      ...(wonder ? { wonderId: wonder } : {}),
      cost: 0,
      edge: { variant: PAPER_EDGES[Math.min(3, Math.floor(random() * 4))], seed: Math.floor(random() * 0x100000000) >>> 0 },
    });
  });
  return tiles;
}

const repeat = <T,>(items: T[], times: number) => Array.from({ length: times }, () => items).flat();

const SAMPLES: { name: string; avatar: string; seed: number; kinds: (TileKind | { wonder: PaperVisitorId })[] }[] = [
  { name: 'Aoife', avatar: 'star-crew:stargazer', seed: 11, kinds: ['meadow', 'lighthouse', 'woodland', { wonder: 'luma' }, 'water', 'wildflowers', 'observatory', 'meadow', 'orchard', 'water', 'woodland', 'windmill', 'meadow', 'harbour', 'water'] },
  { name: 'Cian', avatar: 'star-crew:skater', seed: 23, kinds: ['mountain', 'meadow', 'waterfall', 'woodland', 'castle', 'meadow', 'volcano', 'woodland', 'camp'] },
  { name: 'Saoirse', avatar: 'star-crew:reader', seed: 37, kinds: [...repeat<TileKind>(['meadow', 'wildflowers', 'greenhouse', 'water', 'woodland', 'bookbindery', 'teahouse', 'orchard'], 4), 'capybara', 'museum', 'pottery'] },
  { name: 'Oisín', avatar: 'star-crew:musician', seed: 41, kinds: ['music', 'meadow', 'water', 'cinema'] },
  { name: 'Niamh', avatar: 'star-crew:maker', seed: 53, kinds: ['kiteworks', 'meadow', 'balloon', 'woodland', 'water', 'station', 'meadow', 'bakery', 'nightmarket', 'water', 'postoffice', 'meadow', 'clocktower', 'wishingwell', 'woodland', 'pumpkins', 'hammock', 'bamboo', 'rockpool', 'meadow'] },
  { name: 'Darragh', avatar: 'star-crew:beanie', seed: 67, kinds: [] },
  { name: 'Ciara', avatar: 'star-crew:hugger', seed: 71, kinds: ['picnic', 'wildflowers', 'meadow', 'capybara', 'water', 'woodland', 'honeyhouse'] },
  { name: 'Fionn', avatar: 'star-crew:snoozer', seed: 83, kinds: [...repeat<TileKind>(['meadow', 'woodland', 'water', 'mountain', 'glacier', 'dunes', 'canyon', 'marsh', 'basalt', 'geode'], 3), 'ruins', 'fossil', 'doorway'] },
];

/** Eight invented 5th Year classmates. */
export function sampleYearIslands(): YearIsland[] {
  return SAMPLES.map(sample => {
    const { tiles, tileCount } = publicTiles(grow(sample.seed, sample.kinds));
    return { uid: `sample-${sample.seed}`, name: sample.name, avatar: sample.avatar, yearGroup: SAMPLE_COHORT.yearGroup, tiles, tileCount };
  });
}

/** The harness student's own island, so their screen is not just the starter. */
export function sampleOwnPaperIsland(): PaperIsland {
  return {
    ...createPaperIsland(),
    tiles: grow(97, ['meadow', 'woodland', 'water', 'teahouse', 'wildflowers', 'meadow', 'windmill', 'orchard', 'water', 'lighthouse', 'woodland', 'greenhouse']),
    revision: 12,
  };
}
