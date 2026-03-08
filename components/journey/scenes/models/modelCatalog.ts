/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

/**
 * Registry mapping model names to GLB paths and calibrated scale factors.
 * Scale values are set so 1 unit ~ 1 meter, people ~ 0.75 units tall.
 * Adjust scales after loading actual Kenney models in a GLB viewer.
 */

interface ModelEntry {
  path: string;
  scale: number;
}

export const MODEL_CATALOG = {
  // ── City Kit (Suburban) ──
  house: { path: '/models/kenney/city/house.glb', scale: 0.6 },

  // ── Nature Kit ──
  treeOak: { path: '/models/kenney/nature/tree-oak.glb', scale: 0.8 },
  treePine: { path: '/models/kenney/nature/tree-pine.glb', scale: 0.8 },
  plantPot: { path: '/models/kenney/nature/plant-pot.glb', scale: 0.5 },
  plantPotLarge: { path: '/models/kenney/nature/plant-pot-large.glb', scale: 0.7 },
  fenceSection: { path: '/models/kenney/nature/fence-section.glb', scale: 0.5 },
  hedge: { path: '/models/kenney/nature/hedge.glb', scale: 0.5 },

  // ── Furniture Kit ──
  desk: { path: '/models/kenney/furniture/desk.glb', scale: 0.5 },
  chair: { path: '/models/kenney/furniture/chair.glb', scale: 0.5 },
  bookshelf: { path: '/models/kenney/furniture/bookshelf.glb', scale: 0.5 },
  bookshelfLarge: { path: '/models/kenney/furniture/bookshelf-large.glb', scale: 0.5 },
  couch: { path: '/models/kenney/furniture/couch.glb', scale: 0.5 },
  tableCoffee: { path: '/models/kenney/furniture/table-coffee.glb', scale: 0.5 },
  tableRound: { path: '/models/kenney/furniture/table-round.glb', scale: 0.5 },
  tv: { path: '/models/kenney/furniture/tv.glb', scale: 0.5 },
  tvStand: { path: '/models/kenney/furniture/tv-stand.glb', scale: 0.5 },
  lampFloor: { path: '/models/kenney/furniture/lamp-floor.glb', scale: 0.5 },
  lampDesk: { path: '/models/kenney/furniture/lamp-desk.glb', scale: 0.5 },
  laptop: { path: '/models/kenney/furniture/laptop.glb', scale: 0.5 },
  kitchenCounter: { path: '/models/kenney/furniture/kitchen-counter.glb', scale: 0.5 },
  kitchenCounterPremium: { path: '/models/kenney/furniture/kitchen-counter-premium.glb', scale: 0.5 },
  bench: { path: '/models/kenney/furniture/bench.glb', scale: 0.5 },

  // ── Building Kit ──
  buildingOffice: { path: '/models/kenney/buildings/building-office.glb', scale: 0.5 },
  buildingLarge: { path: '/models/kenney/buildings/building-large.glb', scale: 0.5 },
  buildingUniversity: { path: '/models/kenney/buildings/building-university.glb', scale: 0.5 },

  // ── Car Kit ──
  sedan: { path: '/models/kenney/vehicles/sedan.glb', scale: 0.5 },

  // ── Train Kit ──
  trackStraight: { path: '/models/kenney/train/track-straight.glb', scale: 0.5 },
  platformRoof: { path: '/models/kenney/train/platform-roof.glb', scale: 0.5 },
  signal: { path: '/models/kenney/train/signal.glb', scale: 0.5 },

  // ── Mini Characters ──
  characterA: { path: '/models/kenney/characters/character-a.glb', scale: 0.5 },
  characterB: { path: '/models/kenney/characters/character-b.glb', scale: 0.5 },
  characterC: { path: '/models/kenney/characters/character-c.glb', scale: 0.5 },
} as const satisfies Record<string, ModelEntry>;

export type ModelName = keyof typeof MODEL_CATALOG;
