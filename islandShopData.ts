/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { ShopItem, ShopItemCategory, IslandPlacement, NorthStarCategory } from './types';

/** Categories where items can only be purchased once */
const UNIQUE_CATEGORIES: Set<ShopItemCategory> = new Set(['building', 'vehicle']);

/** Returns true if this item type is one-per-customer */
export function isUniqueItem(item: ShopItem): boolean {
  return UNIQUE_CATEGORIES.has(item.category) || !!item.exclusiveTo;
}

/* ── Shop Catalog ── */

export const SHOP_CATALOG: ShopItem[] = [
  // ── Terrain (hex tiles) ──
  { id: 'terrain-grass',           name: 'Grass',            description: 'A lush green tile',               model: 'grass.glb',            category: 'terrain',  type: 'hex', price: 25 },
  { id: 'terrain-grass-forest',    name: 'Grass Forest',     description: 'Grass tile with trees',           model: 'grass-forest.glb',     category: 'terrain',  type: 'hex', price: 35 },
  { id: 'terrain-grass-hill',      name: 'Grass Hill',       description: 'A gentle grassy hill',            model: 'grass-hill.glb',       category: 'terrain',  type: 'hex', price: 40 },
  { id: 'terrain-dirt',            name: 'Dirt',             description: 'A plain dirt tile',               model: 'dirt.glb',             category: 'terrain',  type: 'hex', price: 25 },
  { id: 'terrain-dirt-lumber',     name: 'Dirt Lumber',      description: 'Dirt tile with lumber',           model: 'dirt-lumber.glb',      category: 'terrain',  type: 'hex', price: 40 },
  { id: 'terrain-sand',            name: 'Sand',             description: 'A sandy beach tile',              model: 'sand.glb',             category: 'terrain',  type: 'hex', price: 25 },
  { id: 'terrain-sand-desert',     name: 'Sand Desert',      description: 'A dry desert tile',               model: 'sand-desert.glb',      category: 'terrain',  type: 'hex', price: 30 },
  { id: 'terrain-sand-rocks',      name: 'Sand Rocks',       description: 'Sand with rocky outcrops',        model: 'sand-rocks.glb',       category: 'terrain',  type: 'hex', price: 35 },
  { id: 'terrain-stone',           name: 'Stone',            description: 'A sturdy stone tile',             model: 'stone.glb',            category: 'terrain',  type: 'hex', price: 30 },
  { id: 'terrain-stone-hill',      name: 'Stone Hill',       description: 'A rocky hilltop',                 model: 'stone-hill.glb',       category: 'terrain',  type: 'hex', price: 40 },
  { id: 'terrain-stone-mountain',  name: 'Stone Mountain',   description: 'A towering mountain',             model: 'stone-mountain.glb',   category: 'terrain',  type: 'hex', price: 50 },
  { id: 'terrain-stone-rocks',     name: 'Stone Rocks',      description: 'Stone with scattered rocks',      model: 'stone-rocks.glb',      category: 'terrain',  type: 'hex', price: 35 },

  // ── Buildings (hex tiles) ──
  { id: 'building-cabin',          name: 'Cabin',            description: 'A cosy log cabin',                model: 'building-cabin.glb',       category: 'building', type: 'hex', price: 75 },
  { id: 'building-house',          name: 'House',            description: 'A comfortable family home',       model: 'building-house.glb',       category: 'building', type: 'hex', price: 100 },
  { id: 'building-market',         name: 'Market',           description: 'A bustling market stall',         model: 'building-market.glb',      category: 'building', type: 'hex', price: 125 },
  { id: 'building-farm',           name: 'Farm',             description: 'A productive farmstead',          model: 'building-farm.glb',        category: 'building', type: 'hex', price: 100 },
  { id: 'building-mill',           name: 'Mill',             description: 'A grain mill with sails',         model: 'building-mill.glb',        category: 'building', type: 'hex', price: 125 },
  { id: 'building-village',        name: 'Village',          description: 'A small village cluster',         model: 'building-village.glb',     category: 'building', type: 'hex', price: 150 },
  { id: 'building-tower',          name: 'Tower',            description: 'A tall watchtower',               model: 'building-tower.glb',       category: 'building', type: 'hex', price: 175 },
  { id: 'building-dock',           name: 'Dock',             description: 'A waterside dock',                model: 'building-dock.glb',        category: 'building', type: 'hex', price: 100 },
  { id: 'building-watermill',      name: 'Watermill',        description: 'A mill powered by water',         model: 'building-watermill.glb',   category: 'building', type: 'hex', price: 150 },
  { id: 'building-castle',         name: 'Castle',           description: 'A grand stone castle',            model: 'building-castle.glb',      category: 'building', type: 'hex', price: 300 },
  { id: 'building-wizard-tower',   name: 'Wizard Tower',     description: 'A mysterious magic tower',        model: 'building-wizard-tower.glb', category: 'building', type: 'hex', price: 250 },

  // ── Paths (hex tiles) ──
  { id: 'path-straight',           name: 'Path Straight',    description: 'A straight path tile',            model: 'path-straight.glb',    category: 'path',     type: 'hex', price: 30 },
  { id: 'path-corner',             name: 'Path Corner',      description: 'A curved path tile',              model: 'path-corner.glb',      category: 'path',     type: 'hex', price: 35 },
  { id: 'path-crossing',           name: 'Path Crossing',    description: 'A crossroads tile',               model: 'path-crossing.glb',    category: 'path',     type: 'hex', price: 40 },
  { id: 'path-bridge',             name: 'Bridge',           description: 'A bridge over water',             model: 'bridge.glb',           category: 'path',     type: 'hex', price: 75 },

  // ── Nature decorations ──
  { id: 'nature-tree-oak',         name: 'Oak Tree',         description: 'A mighty oak tree',               model: 'tree_oak.glb',         category: 'nature',    type: 'decoration', price: 25, defaultScale: 0.8 },
  { id: 'nature-tree-pine',        name: 'Pine Tree',        description: 'A tall pine tree',                model: 'tree_pineSmallA.glb',  category: 'nature',    type: 'decoration', price: 20, defaultScale: 0.8 },
  { id: 'nature-tree-small',       name: 'Small Tree',       description: 'A little tree sapling',           model: 'tree_small.glb',       category: 'nature',    type: 'decoration', price: 15, defaultScale: 0.7 },
  { id: 'nature-bush',             name: 'Bush',             description: 'A leafy green bush',              model: 'plant_bush.glb',       category: 'nature',    type: 'decoration', price: 15, defaultScale: 0.6 },
  { id: 'nature-bush-large',       name: 'Large Bush',       description: 'A big bushy shrub',               model: 'plant_bushLarge.glb',  category: 'nature',    type: 'decoration', price: 20, defaultScale: 0.7 },
  { id: 'nature-plant-1',          name: 'Small Plant',      description: 'A tiny ground plant',             model: 'plantSmall1.glb',      category: 'nature',    type: 'decoration', price: 15, defaultScale: 0.5 },
  { id: 'nature-plant-2',          name: 'Ground Cover',     description: 'A low spreading plant',           model: 'plantSmall2.glb',      category: 'nature',    type: 'decoration', price: 15, defaultScale: 0.5 },
  { id: 'nature-plant-3',          name: 'Wild Plant',       description: 'A wild growing plant',            model: 'plantSmall3.glb',      category: 'nature',    type: 'decoration', price: 15, defaultScale: 0.5 },
  { id: 'nature-potted-plant',     name: 'Potted Plant',     description: 'A potted indoor plant',           model: 'pottedPlant.glb',      category: 'nature',    type: 'decoration', price: 20, defaultScale: 0.5 },
  { id: 'nature-flower-purple',    name: 'Purple Flower',    description: 'Beautiful purple flowers',        model: 'flower_purpleA.glb',   category: 'nature',    type: 'decoration', price: 20, defaultScale: 0.5 },
  { id: 'nature-flower-red',       name: 'Red Flower',       description: 'Vibrant red flowers',             model: 'flower_redA.glb',      category: 'nature',    type: 'decoration', price: 20, defaultScale: 0.5 },
  { id: 'nature-flower-yellow',    name: 'Yellow Flower',    description: 'Cheerful yellow flowers',         model: 'flower_yellowA.glb',   category: 'nature',    type: 'decoration', price: 20, defaultScale: 0.5 },

  // ── Furniture decorations ──
  { id: 'furniture-desk',          name: 'Desk',             description: 'A sturdy study desk',             model: 'desk.glb',             category: 'furniture', type: 'decoration', price: 40, defaultScale: 0.5 },
  { id: 'furniture-chair',         name: 'Chair',            description: 'A comfortable chair',             model: 'chair.glb',            category: 'furniture', type: 'decoration', price: 30, defaultScale: 0.5 },
  { id: 'furniture-table',         name: 'Table',            description: 'A dining table',                  model: 'table.glb',            category: 'furniture', type: 'decoration', price: 35, defaultScale: 0.5 },
  { id: 'furniture-sofa',          name: 'Sofa',             description: 'A cosy lounge sofa',              model: 'loungeSofa.glb',       category: 'furniture', type: 'decoration', price: 50, defaultScale: 0.5 },
  { id: 'furniture-bed',           name: 'Bed',              description: 'A single bed for rest',           model: 'bedSingle.glb',        category: 'furniture', type: 'decoration', price: 45, defaultScale: 0.5 },
  { id: 'furniture-bookcase',      name: 'Bookcase',         description: 'An open bookcase',                model: 'bookcaseOpen.glb',     category: 'furniture', type: 'decoration', price: 50, defaultScale: 0.5 },
  { id: 'furniture-books',         name: 'Books',            description: 'A stack of books',                model: 'books.glb',            category: 'furniture', type: 'decoration', price: 30, defaultScale: 0.4 },
  { id: 'furniture-laptop',        name: 'Laptop',           description: 'An open laptop',                  model: 'laptop.glb',           category: 'furniture', type: 'decoration', price: 50, defaultScale: 0.4 },
  { id: 'furniture-computer',      name: 'Computer',         description: 'A desktop monitor',               model: 'computerScreen.glb',   category: 'furniture', type: 'decoration', price: 60, defaultScale: 0.4 },
  { id: 'furniture-tv',            name: 'Television',       description: 'A modern flat screen',            model: 'televisionModern.glb', category: 'furniture', type: 'decoration', price: 75, defaultScale: 0.5 },

  // ── Vehicle decorations ──
  { id: 'vehicle-sedan',           name: 'Sedan',            description: 'A sleek sedan car',               model: 'sedan.glb',            category: 'vehicle',  type: 'decoration', price: 150, defaultScale: 0.4 },
  { id: 'vehicle-hatchback',       name: 'Hatchback Sport',  description: 'A sporty hatchback',              model: 'hatchback-sports.glb', category: 'vehicle',  type: 'decoration', price: 175, defaultScale: 0.4 },
  { id: 'vehicle-suv',             name: 'SUV',              description: 'A rugged SUV',                    model: 'suv.glb',              category: 'vehicle',  type: 'decoration', price: 200, defaultScale: 0.4 },
  { id: 'vehicle-van',             name: 'Van',              description: 'A versatile van',                 model: 'van.glb',              category: 'vehicle',  type: 'decoration', price: 175, defaultScale: 0.4 },

  // ── Atmosphere decorations ──
  { id: 'atmo-lantern',            name: 'Lantern',          description: 'A warm glowing lantern',          model: 'lantern.glb',          category: 'atmosphere', type: 'decoration', price: 40, defaultScale: 0.5 },
  { id: 'atmo-lamp',               name: 'Floor Lamp',       description: 'A tall round floor lamp',         model: 'lampRoundFloor.glb',   category: 'atmosphere', type: 'decoration', price: 45, defaultScale: 0.5 },
  { id: 'atmo-fountain',           name: 'Fountain',         description: 'A decorative fountain',           model: 'fountain-round.glb',   category: 'atmosphere', type: 'decoration', price: 100, defaultScale: 0.5 },
  { id: 'atmo-campfire',           name: 'Campfire',         description: 'A cosy campfire pit',             model: 'campfire-pit.glb',     category: 'atmosphere', type: 'decoration', price: 75, defaultScale: 0.5 },
  { id: 'atmo-windmill',           name: 'Windmill',         description: 'A decorative windmill',           model: 'windmill.glb',         category: 'atmosphere', type: 'decoration', price: 125, defaultScale: 0.6 },
  { id: 'atmo-tent',               name: 'Tent',             description: 'A canvas camping tent',           model: 'tent-canvas.glb',      category: 'atmosphere', type: 'decoration', price: 60, defaultScale: 0.5 },
  { id: 'atmo-barrel',             name: 'Barrel',           description: 'A wooden barrel',                 model: 'barrel.glb',           category: 'atmosphere', type: 'decoration', price: 30, defaultScale: 0.4 },
  { id: 'atmo-chest',              name: 'Chest',            description: 'A treasure chest',                model: 'chest.glb',            category: 'atmosphere', type: 'decoration', price: 50, defaultScale: 0.4 },
  { id: 'atmo-banner-green',       name: 'Green Banner',     description: 'A green flag banner',             model: 'banner-green.glb',     category: 'atmosphere', type: 'decoration', price: 40, defaultScale: 0.5 },
  { id: 'atmo-banner-red',         name: 'Red Banner',       description: 'A red flag banner',               model: 'banner-red.glb',       category: 'atmosphere', type: 'decoration', price: 40, defaultScale: 0.5 },
  { id: 'atmo-fence',              name: 'Fence',            description: 'A simple wooden fence',           model: 'fence_simple.glb',     category: 'atmosphere', type: 'decoration', price: 25, defaultScale: 0.5 },
  { id: 'atmo-fence-gate',         name: 'Fence Gate',       description: 'A fence with a gate',             model: 'fence_gate.glb',       category: 'atmosphere', type: 'decoration', price: 35, defaultScale: 0.5 },
  { id: 'atmo-sign',               name: 'Sign',             description: 'A wooden signpost',               model: 'sign.glb',             category: 'atmosphere', type: 'decoration', price: 30, defaultScale: 0.5 },
  { id: 'atmo-stall',              name: 'Stall',            description: 'A market stall',                  model: 'stall.glb',            category: 'atmosphere', type: 'decoration', price: 60, defaultScale: 0.5 },
];

/* ── Exclusive Items (3 per category) ── */

export const EXCLUSIVE_ITEMS: ShopItem[] = [
  // Independence
  { id: 'excl-ind-sedan',        name: 'My First Car',      description: 'Freedom on four wheels',         model: 'sedan.glb',                category: 'vehicle',    type: 'decoration', price: 200, exclusiveTo: 'independence', defaultScale: 0.4 },
  { id: 'excl-ind-campfire',     name: 'Campfire Pit',      description: 'Your own fireside retreat',      model: 'campfire-pit.glb',         category: 'atmosphere', type: 'decoration', price: 100, exclusiveTo: 'independence', defaultScale: 0.5 },
  { id: 'excl-ind-balcony',      name: 'Balcony View',      description: 'A stone hilltop outlook',        model: 'stone-hill.glb',           category: 'terrain',    type: 'hex',        price: 150, exclusiveTo: 'independence' },

  // Family-Community
  { id: 'excl-fam-windmill',     name: 'Family Windmill',   description: 'A windmill for the community',   model: 'windmill.glb',             category: 'atmosphere', type: 'decoration', price: 175, exclusiveTo: 'family-community', defaultScale: 0.6 },
  { id: 'excl-fam-fountain',     name: 'Town Fountain',     description: 'A gathering place fountain',     model: 'fountain-round.glb',       category: 'atmosphere', type: 'decoration', price: 125, exclusiveTo: 'family-community', defaultScale: 0.5 },
  { id: 'excl-fam-farm',         name: 'Family Farm',       description: 'Feed the whole community',       model: 'building-farm.glb',        category: 'building',   type: 'hex',        price: 200, exclusiveTo: 'family-community' },

  // Career-Craft
  { id: 'excl-car-mine',         name: 'Mine',              description: 'Dig deep for resources',         model: 'stone-rocks.glb',          category: 'terrain',    type: 'hex',        price: 200, exclusiveTo: 'career-craft' },
  { id: 'excl-car-smelter',      name: 'Smelter',           description: 'Forge raw materials',            model: 'building-mill.glb',        category: 'building',   type: 'hex',        price: 175, exclusiveTo: 'career-craft' },
  { id: 'excl-car-port',         name: 'Port',              description: 'Trade with the world',           model: 'building-dock.glb',        category: 'building',   type: 'hex',        price: 225, exclusiveTo: 'career-craft' },

  // College-Learning
  { id: 'excl-col-wizard',       name: 'Wizard Tower',      description: 'A tower of knowledge',           model: 'building-wizard-tower.glb', category: 'building',  type: 'hex',        price: 250, exclusiveTo: 'college-learning' },
  { id: 'excl-col-castle',       name: 'Grand Castle',      description: 'A castle of learning',           model: 'building-castle.glb',      category: 'building',   type: 'hex',        price: 300, exclusiveTo: 'college-learning' },
  { id: 'excl-col-watermill',    name: 'Study Mill',        description: 'Powered by curiosity',           model: 'building-watermill.glb',   category: 'building',   type: 'hex',        price: 150, exclusiveTo: 'college-learning' },

  // Prove-Myself
  { id: 'excl-prv-archery',      name: 'Archery Range',     description: 'Aim for the bullseye',           model: 'stall.glb',                category: 'atmosphere', type: 'decoration', price: 150, exclusiveTo: 'prove-myself', defaultScale: 0.6 },
  { id: 'excl-prv-walls',        name: 'Castle Walls',      description: 'Defend your achievements',       model: 'building-tower.glb',       category: 'building',   type: 'hex',        price: 200, exclusiveTo: 'prove-myself' },
  { id: 'excl-prv-victory',      name: 'Victory Tower',     description: 'Stand tall at the top',          model: 'building-castle.glb',      category: 'building',   type: 'hex',        price: 175, exclusiveTo: 'prove-myself' },

  // Options-Freedom
  { id: 'excl-opt-ship',         name: 'Ship',              description: 'Set sail for new horizons',      model: 'building-dock.glb',        category: 'building',   type: 'hex',        price: 175, exclusiveTo: 'options-freedom' },
  { id: 'excl-opt-large-ship',   name: 'Large Ship',        description: 'A flagship for exploration',     model: 'building-watermill.glb',   category: 'building',   type: 'hex',        price: 250, exclusiveTo: 'options-freedom' },
  { id: 'excl-opt-bridge',       name: 'Grand Bridge',      description: 'Connect new possibilities',      model: 'bridge.glb',               category: 'path',       type: 'hex',        price: 125, exclusiveTo: 'options-freedom' },
];

/* ── Starter Packs ── */

export interface StarterPack {
  placements: IslandPlacement[];
  waterColor: string;
}

export const STARTER_PACKS: Record<NorthStarCategory, StarterPack> = {
  'independence': {
    waterColor: '#4A8ECF',
    placements: [
      { itemId: 'starter', model: 'grass.glb',          type: 'hex',        q: 0, r: 0, purchasedAt: '', isStarter: true },
      { itemId: 'starter', model: 'grass.glb',          type: 'hex',        q: 1, r: 0, purchasedAt: '', isStarter: true },
      { itemId: 'starter', model: 'grass.glb',          type: 'hex',        q: 0, r: 1, purchasedAt: '', isStarter: true },
      { itemId: 'starter', model: 'grass.glb',          type: 'hex',        q: 1, r: -1, purchasedAt: '', isStarter: true },
      { itemId: 'starter', model: 'building-cabin.glb', type: 'hex',        q: 0, r: 0, purchasedAt: '', isStarter: true },
      { itemId: 'starter', model: 'desk.glb',           type: 'decoration', q: 1, r: 0, scale: 0.5, purchasedAt: '', isStarter: true },
      { itemId: 'starter', model: 'sign.glb',           type: 'decoration', q: 0, r: 1, scale: 0.5, offsetX: 0.2, purchasedAt: '', isStarter: true },
    ],
  },
  'family-community': {
    waterColor: '#2E8EB0',
    placements: [
      { itemId: 'starter', model: 'grass.glb',          type: 'hex',        q: 0, r: 0, purchasedAt: '', isStarter: true },
      { itemId: 'starter', model: 'grass.glb',          type: 'hex',        q: 1, r: 0, purchasedAt: '', isStarter: true },
      { itemId: 'starter', model: 'grass.glb',          type: 'hex',        q: 0, r: 1, purchasedAt: '', isStarter: true },
      { itemId: 'starter', model: 'grass-forest.glb',   type: 'hex',        q: -1, r: 1, purchasedAt: '', isStarter: true },
      { itemId: 'starter', model: 'building-house.glb', type: 'hex',        q: 0, r: 0, purchasedAt: '', isStarter: true },
      { itemId: 'starter', model: 'sign.glb',           type: 'decoration', q: 1, r: 0, scale: 0.5, offsetX: 0.2, purchasedAt: '', isStarter: true },
    ],
  },
  'career-craft': {
    waterColor: '#3A8EAF',
    placements: [
      { itemId: 'starter', model: 'dirt.glb',            type: 'hex',        q: 0, r: 0, purchasedAt: '', isStarter: true },
      { itemId: 'starter', model: 'dirt.glb',            type: 'hex',        q: 1, r: 0, purchasedAt: '', isStarter: true },
      { itemId: 'starter', model: 'grass.glb',           type: 'hex',        q: 0, r: 1, purchasedAt: '', isStarter: true },
      { itemId: 'starter', model: 'grass.glb',           type: 'hex',        q: -1, r: 1, purchasedAt: '', isStarter: true },
      { itemId: 'starter', model: 'building-market.glb', type: 'hex',        q: 0, r: 0, purchasedAt: '', isStarter: true },
      { itemId: 'starter', model: 'sign.glb',            type: 'decoration', q: 1, r: 0, scale: 0.5, offsetX: 0.2, purchasedAt: '', isStarter: true },
    ],
  },
  'college-learning': {
    waterColor: '#3B9EBF',
    placements: [
      { itemId: 'starter', model: 'grass.glb',           type: 'hex',        q: 0, r: 0, purchasedAt: '', isStarter: true },
      { itemId: 'starter', model: 'grass.glb',           type: 'hex',        q: 1, r: 0, purchasedAt: '', isStarter: true },
      { itemId: 'starter', model: 'grass.glb',           type: 'hex',        q: 0, r: 1, purchasedAt: '', isStarter: true },
      { itemId: 'starter', model: 'path-straight.glb',   type: 'hex',        q: 1, r: -1, purchasedAt: '', isStarter: true },
      { itemId: 'starter', model: 'building-tower.glb',  type: 'hex',        q: 0, r: 0, purchasedAt: '', isStarter: true },
      { itemId: 'starter', model: 'bookcaseOpen.glb',    type: 'decoration', q: 1, r: 0, scale: 0.5, purchasedAt: '', isStarter: true },
      { itemId: 'starter', model: 'sign.glb',            type: 'decoration', q: 0, r: 1, scale: 0.5, offsetX: 0.2, purchasedAt: '', isStarter: true },
    ],
  },
  'prove-myself': {
    waterColor: '#3574A0',
    placements: [
      { itemId: 'starter', model: 'stone.glb',           type: 'hex',        q: 0, r: 0, purchasedAt: '', isStarter: true },
      { itemId: 'starter', model: 'stone.glb',           type: 'hex',        q: 1, r: 0, purchasedAt: '', isStarter: true },
      { itemId: 'starter', model: 'grass.glb',           type: 'hex',        q: 0, r: 1, purchasedAt: '', isStarter: true },
      { itemId: 'starter', model: 'grass.glb',           type: 'hex',        q: -1, r: 1, purchasedAt: '', isStarter: true },
      { itemId: 'starter', model: 'building-tower.glb',  type: 'hex',        q: 0, r: 0, purchasedAt: '', isStarter: true },
      { itemId: 'starter', model: 'banner-red.glb',      type: 'decoration', q: 1, r: 0, scale: 0.5, purchasedAt: '', isStarter: true },
      { itemId: 'starter', model: 'sign.glb',            type: 'decoration', q: 0, r: 1, scale: 0.5, offsetX: 0.2, purchasedAt: '', isStarter: true },
    ],
  },
  'options-freedom': {
    waterColor: '#2E8EB0',
    placements: [
      { itemId: 'starter', model: 'sand.glb',            type: 'hex',        q: 0, r: 0, purchasedAt: '', isStarter: true },
      { itemId: 'starter', model: 'sand.glb',            type: 'hex',        q: 1, r: 0, purchasedAt: '', isStarter: true },
      { itemId: 'starter', model: 'grass.glb',           type: 'hex',        q: 0, r: 1, purchasedAt: '', isStarter: true },
      { itemId: 'starter', model: 'grass.glb',           type: 'hex',        q: -1, r: 1, purchasedAt: '', isStarter: true },
      { itemId: 'starter', model: 'building-dock.glb',   type: 'hex',        q: 0, r: 0, purchasedAt: '', isStarter: true },
      { itemId: 'starter', model: 'sign.glb',            type: 'decoration', q: 1, r: 0, scale: 0.5, offsetX: 0.2, purchasedAt: '', isStarter: true },
    ],
  },
};

/* ── Milestone Rewards ── */

export interface MilestoneReward {
  id: string;
  modulesRequired: number;
  item: ShopItem;
  label: string;
}

const THRESHOLDS = [2, 4, 6, 8, 10, 14, 18, 22, 27, 33];

function makeReward(id: string, idx: number, label: string, item: ShopItem): MilestoneReward {
  return { id, modulesRequired: THRESHOLDS[idx], item, label };
}

export const MILESTONE_REWARDS: Record<NorthStarCategory, MilestoneReward[]> = {
  'independence': [
    makeReward('reward-ind-1', 0, 'First Steps',     { id: 'rw-ind-1', name: 'Campfire',       description: 'A cosy campfire pit',      model: 'campfire-pit.glb',    category: 'atmosphere', type: 'decoration', price: 0, defaultScale: 0.5 }),
    makeReward('reward-ind-2', 1, 'Road Ahead',      { id: 'rw-ind-2', name: 'Sedan',           description: 'Your own ride',            model: 'sedan.glb',           category: 'vehicle',    type: 'decoration', price: 0, defaultScale: 0.4 }),
    makeReward('reward-ind-3', 2, 'Base Camp',        { id: 'rw-ind-3', name: 'Tent',            description: 'A canvas tent',            model: 'tent-canvas.glb',     category: 'atmosphere', type: 'decoration', price: 0, defaultScale: 0.5 }),
    makeReward('reward-ind-4', 3, 'Growing Roots',    { id: 'rw-ind-4', name: 'Oak Tree',        description: 'A mighty oak',             model: 'tree_oak.glb',        category: 'nature',     type: 'decoration', price: 0, defaultScale: 0.8 }),
    makeReward('reward-ind-5', 4, 'High Ground',      { id: 'rw-ind-5', name: 'Stone Hill',      description: 'A rocky hilltop',          model: 'stone-hill.glb',      category: 'terrain',    type: 'hex',        price: 0 }),
    makeReward('reward-ind-6', 5, 'Trailblazer',      { id: 'rw-ind-6', name: 'Path Crossing',   description: 'A crossroads',             model: 'path-crossing.glb',   category: 'path',       type: 'hex',        price: 0 }),
    makeReward('reward-ind-7', 6, 'Self-Made',        { id: 'rw-ind-7', name: 'Cabin',           description: 'A log cabin',              model: 'building-cabin.glb',  category: 'building',   type: 'hex',        price: 0 }),
    makeReward('reward-ind-8', 7, 'Explorer',         { id: 'rw-ind-8', name: 'Lantern',         description: 'Light the way',            model: 'lantern.glb',         category: 'atmosphere', type: 'decoration', price: 0, defaultScale: 0.5 }),
    makeReward('reward-ind-9', 8, 'Peak Climber',     { id: 'rw-ind-9', name: 'Stone Mountain',  description: 'A towering peak',          model: 'stone-mountain.glb',  category: 'terrain',    type: 'hex',        price: 0 }),
    makeReward('reward-ind-10', 9, 'Free Spirit',     { id: 'rw-ind-10', name: 'SUV',            description: 'Conquer any terrain',      model: 'suv.glb',             category: 'vehicle',    type: 'decoration', price: 0, defaultScale: 0.4 }),
  ],
  'family-community': [
    makeReward('reward-fam-1', 0, 'First Steps',     { id: 'rw-fam-1', name: 'Fountain',        description: 'A gathering fountain',     model: 'fountain-round.glb',  category: 'atmosphere', type: 'decoration', price: 0, defaultScale: 0.5 }),
    makeReward('reward-fam-2', 1, 'Together',         { id: 'rw-fam-2', name: 'Farm Tile',       description: 'Fresh farmstead',          model: 'building-farm.glb',   category: 'building',   type: 'hex',        price: 0 }),
    makeReward('reward-fam-3', 2, 'In Bloom',         { id: 'rw-fam-3', name: 'Purple Flower',   description: 'Beautiful flowers',        model: 'flower_purpleA.glb',  category: 'nature',     type: 'decoration', price: 0, defaultScale: 0.5 }),
    makeReward('reward-fam-4', 3, 'Community',        { id: 'rw-fam-4', name: 'Windmill',        description: 'A decorative windmill',    model: 'windmill.glb',        category: 'atmosphere', type: 'decoration', price: 0, defaultScale: 0.6 }),
    makeReward('reward-fam-5', 4, 'Gathering',        { id: 'rw-fam-5', name: 'Village',         description: 'A small village',          model: 'building-village.glb', category: 'building',  type: 'hex',        price: 0 }),
    makeReward('reward-fam-6', 5, 'Roots Run Deep',   { id: 'rw-fam-6', name: 'Red Flower',      description: 'Vibrant reds',             model: 'flower_redA.glb',     category: 'nature',     type: 'decoration', price: 0, defaultScale: 0.5 }),
    makeReward('reward-fam-7', 6, 'Home Sweet Home',  { id: 'rw-fam-7', name: 'House',           description: 'A family home',            model: 'building-house.glb',  category: 'building',   type: 'hex',        price: 0 }),
    makeReward('reward-fam-8', 7, 'Garden Party',     { id: 'rw-fam-8', name: 'Yellow Flower',   description: 'Cheerful yellows',         model: 'flower_yellowA.glb',  category: 'nature',     type: 'decoration', price: 0, defaultScale: 0.5 }),
    makeReward('reward-fam-9', 8, 'Shared Path',      { id: 'rw-fam-9', name: 'Bridge',          description: 'Connect together',         model: 'bridge.glb',          category: 'path',       type: 'hex',        price: 0 }),
    makeReward('reward-fam-10', 9, 'Heartbeat',       { id: 'rw-fam-10', name: 'Watermill',      description: 'Powered by community',     model: 'building-watermill.glb', category: 'building', type: 'hex',      price: 0 }),
  ],
  'career-craft': [
    makeReward('reward-car-1', 0, 'First Steps',     { id: 'rw-car-1', name: 'Market Stall',    description: 'Start selling',            model: 'stall.glb',           category: 'atmosphere', type: 'decoration', price: 0, defaultScale: 0.5 }),
    makeReward('reward-car-2', 1, 'Workspace',        { id: 'rw-car-2', name: 'Desk',            description: 'A sturdy desk',            model: 'desk.glb',            category: 'furniture',  type: 'decoration', price: 0, defaultScale: 0.5 }),
    makeReward('reward-car-3', 2, 'Connected',        { id: 'rw-car-3', name: 'Laptop',          description: 'Stay productive',          model: 'laptop.glb',          category: 'furniture',  type: 'decoration', price: 0, defaultScale: 0.4 }),
    makeReward('reward-car-4', 3, 'Workshop',         { id: 'rw-car-4', name: 'Computer',        description: 'A desktop setup',          model: 'computerScreen.glb',  category: 'furniture',  type: 'decoration', price: 0, defaultScale: 0.4 }),
    makeReward('reward-car-5', 4, 'Enterprise',       { id: 'rw-car-5', name: 'Mill',            description: 'A grain mill',             model: 'building-mill.glb',   category: 'building',   type: 'hex',        price: 0 }),
    makeReward('reward-car-6', 5, 'Industrious',      { id: 'rw-car-6', name: 'Dirt Lumber',     description: 'Raw materials',            model: 'dirt-lumber.glb',     category: 'terrain',    type: 'hex',        price: 0 }),
    makeReward('reward-car-7', 6, 'Trade Route',      { id: 'rw-car-7', name: 'Market',          description: 'A bustling market',        model: 'building-market.glb', category: 'building',   type: 'hex',        price: 0 }),
    makeReward('reward-car-8', 7, 'Headquarters',     { id: 'rw-car-8', name: 'Tower',           description: 'Overlook the craft',       model: 'building-tower.glb',  category: 'building',   type: 'hex',        price: 0 }),
    makeReward('reward-car-9', 8, 'Supply Chain',     { id: 'rw-car-9', name: 'Dock',            description: 'A waterside dock',         model: 'building-dock.glb',   category: 'building',   type: 'hex',        price: 0 }),
    makeReward('reward-car-10', 9, 'Mastercraft',     { id: 'rw-car-10', name: 'Watermill',      description: 'Powered by ambition',      model: 'building-watermill.glb', category: 'building', type: 'hex',      price: 0 }),
  ],
  'college-learning': [
    makeReward('reward-col-1', 0, 'First Steps',     { id: 'rw-col-1', name: 'Bookcase',        description: 'Shelves of knowledge',     model: 'bookcaseOpen.glb',    category: 'furniture',  type: 'decoration', price: 0, defaultScale: 0.5 }),
    makeReward('reward-col-2', 1, 'Study Nook',       { id: 'rw-col-2', name: 'Books',           description: 'A stack of books',         model: 'books.glb',           category: 'furniture',  type: 'decoration', price: 0, defaultScale: 0.4 }),
    makeReward('reward-col-3', 2, 'Scholar',           { id: 'rw-col-3', name: 'Desk',            description: 'A study desk',             model: 'desk.glb',            category: 'furniture',  type: 'decoration', price: 0, defaultScale: 0.5 }),
    makeReward('reward-col-4', 3, 'Lookout',           { id: 'rw-col-4', name: 'Tower',           description: 'A tall watchtower',        model: 'building-tower.glb',  category: 'building',   type: 'hex',        price: 0 }),
    makeReward('reward-col-5', 4, 'Knowledge Base',    { id: 'rw-col-5', name: 'Wizard Tower',    description: 'A tower of magic',         model: 'building-wizard-tower.glb', category: 'building', type: 'hex',  price: 0 }),
    makeReward('reward-col-6', 5, 'Deep Dive',         { id: 'rw-col-6', name: 'Laptop',          description: 'Digital learning',         model: 'laptop.glb',          category: 'furniture',  type: 'decoration', price: 0, defaultScale: 0.4 }),
    makeReward('reward-col-7', 6, 'Campus Life',       { id: 'rw-col-7', name: 'Village',         description: 'A campus cluster',         model: 'building-village.glb', category: 'building',  type: 'hex',        price: 0 }),
    makeReward('reward-col-8', 7, 'Dean\'s List',      { id: 'rw-col-8', name: 'Grass Forest',    description: 'A grove of learning',      model: 'grass-forest.glb',    category: 'terrain',    type: 'hex',        price: 0 }),
    makeReward('reward-col-9', 8, 'Thesis',            { id: 'rw-col-9', name: 'Stone Hill',      description: 'Mountain of knowledge',    model: 'stone-hill.glb',      category: 'terrain',    type: 'hex',        price: 0 }),
    makeReward('reward-col-10', 9, 'Graduation',       { id: 'rw-col-10', name: 'Castle',         description: 'A grand institution',      model: 'building-castle.glb', category: 'building',   type: 'hex',        price: 0 }),
  ],
  'prove-myself': [
    makeReward('reward-prv-1', 0, 'First Steps',     { id: 'rw-prv-1', name: 'Green Banner',    description: 'Raise your flag',          model: 'banner-green.glb',    category: 'atmosphere', type: 'decoration', price: 0, defaultScale: 0.5 }),
    makeReward('reward-prv-2', 1, 'Rising',           { id: 'rw-prv-2', name: 'Red Banner',      description: 'Mark your territory',      model: 'banner-red.glb',      category: 'atmosphere', type: 'decoration', price: 0, defaultScale: 0.5 }),
    makeReward('reward-prv-3', 2, 'Fortified',         { id: 'rw-prv-3', name: 'Tower',           description: 'A tall watchtower',        model: 'building-tower.glb',  category: 'building',   type: 'hex',        price: 0 }),
    makeReward('reward-prv-4', 3, 'Treasure',          { id: 'rw-prv-4', name: 'Chest',           description: 'A treasure chest',         model: 'chest.glb',           category: 'atmosphere', type: 'decoration', price: 0, defaultScale: 0.4 }),
    makeReward('reward-prv-5', 4, 'Stronghold',        { id: 'rw-prv-5', name: 'Stone Mountain',  description: 'Conquer the peak',         model: 'stone-mountain.glb',  category: 'terrain',    type: 'hex',        price: 0 }),
    makeReward('reward-prv-6', 5, 'Victory Road',      { id: 'rw-prv-6', name: 'Path Straight',   description: 'The road to victory',      model: 'path-straight.glb',   category: 'path',       type: 'hex',        price: 0 }),
    makeReward('reward-prv-7', 6, 'Arena',             { id: 'rw-prv-7', name: 'Stone Rocks',     description: 'Battle-tested ground',     model: 'stone-rocks.glb',     category: 'terrain',    type: 'hex',        price: 0 }),
    makeReward('reward-prv-8', 7, 'Champion',          { id: 'rw-prv-8', name: 'Village',         description: 'A loyal village',          model: 'building-village.glb', category: 'building',  type: 'hex',        price: 0 }),
    makeReward('reward-prv-9', 8, 'Legendary',         { id: 'rw-prv-9', name: 'Wizard Tower',    description: 'A tower of power',         model: 'building-wizard-tower.glb', category: 'building', type: 'hex',  price: 0 }),
    makeReward('reward-prv-10', 9, 'Unstoppable',      { id: 'rw-prv-10', name: 'Castle',         description: 'Your grand fortress',      model: 'building-castle.glb', category: 'building',   type: 'hex',        price: 0 }),
  ],
  'options-freedom': [
    makeReward('reward-opt-1', 0, 'First Steps',     { id: 'rw-opt-1', name: 'Dock',            description: 'A waterside dock',         model: 'building-dock.glb',   category: 'building',   type: 'hex',        price: 0 }),
    makeReward('reward-opt-2', 1, 'Crossing',          { id: 'rw-opt-2', name: 'Bridge',          description: 'New connections',          model: 'bridge.glb',          category: 'path',       type: 'hex',        price: 0 }),
    makeReward('reward-opt-3', 2, 'Provisions',        { id: 'rw-opt-3', name: 'Barrel',          description: 'Stock up for the trip',    model: 'barrel.glb',          category: 'atmosphere', type: 'decoration', price: 0, defaultScale: 0.4 }),
    makeReward('reward-opt-4', 3, 'Guiding Light',     { id: 'rw-opt-4', name: 'Lantern',         description: 'Light the way',            model: 'lantern.glb',         category: 'atmosphere', type: 'decoration', price: 0, defaultScale: 0.5 }),
    makeReward('reward-opt-5', 4, 'Open Road',         { id: 'rw-opt-5', name: 'Path Crossing',   description: 'Many paths to take',       model: 'path-crossing.glb',   category: 'path',       type: 'hex',        price: 0 }),
    makeReward('reward-opt-6', 5, 'Sandy Shores',      { id: 'rw-opt-6', name: 'Sand Rocks',      description: 'Coastal terrain',          model: 'sand-rocks.glb',      category: 'terrain',    type: 'hex',        price: 0 }),
    makeReward('reward-opt-7', 6, 'Harbour',           { id: 'rw-opt-7', name: 'Watermill',       description: 'A harbour mill',           model: 'building-watermill.glb', category: 'building', type: 'hex',      price: 0 }),
    makeReward('reward-opt-8', 7, 'Wayfarer',          { id: 'rw-opt-8', name: 'Fence Gate',      description: 'Open every gate',          model: 'fence_gate.glb',      category: 'atmosphere', type: 'decoration', price: 0, defaultScale: 0.5 }),
    makeReward('reward-opt-9', 8, 'Navigator',         { id: 'rw-opt-9', name: 'Cabin',           description: 'A seaside cabin',          model: 'building-cabin.glb',  category: 'building',   type: 'hex',        price: 0 }),
    makeReward('reward-opt-10', 9, 'Horizon',          { id: 'rw-opt-10', name: 'Castle',         description: 'Endless possibilities',    model: 'building-castle.glb', category: 'building',   type: 'hex',        price: 0 }),
  ],
};

/* ── Unlock Gates ── */

export interface UnlockGate {
  itemIdPrefix: string;
  defaultUnlockAt: number;
  earlyUnlockFor?: NorthStarCategory[];
  earlyUnlockAt?: number;
}

export const UNLOCK_GATES: UnlockGate[] = [
  { itemIdPrefix: 'building-castle',       defaultUnlockAt: 20, earlyUnlockFor: ['college-learning'], earlyUnlockAt: 12 },
  { itemIdPrefix: 'building-wizard-tower', defaultUnlockAt: 18, earlyUnlockFor: ['college-learning'], earlyUnlockAt: 10 },
  { itemIdPrefix: 'building-watermill',    defaultUnlockAt: 12, earlyUnlockFor: ['family-community'], earlyUnlockAt: 6 },
  { itemIdPrefix: 'building-tower',        defaultUnlockAt: 10, earlyUnlockFor: ['prove-myself'], earlyUnlockAt: 5 },
  { itemIdPrefix: 'building-village',      defaultUnlockAt: 8,  earlyUnlockFor: ['family-community'], earlyUnlockAt: 4 },
  { itemIdPrefix: 'vehicle-',             defaultUnlockAt: 15, earlyUnlockFor: ['independence'], earlyUnlockAt: 8 },
  { itemIdPrefix: 'atmo-fountain',        defaultUnlockAt: 10, earlyUnlockFor: ['family-community'], earlyUnlockAt: 5 },
  { itemIdPrefix: 'atmo-windmill',        defaultUnlockAt: 12 },
];

/* ── North Star Discounts ── */

export interface NorthStarDiscount {
  category: NorthStarCategory;
  itemIdPrefixes: string[];
  discountPercent: number;
}

export const NORTH_STAR_DISCOUNTS: NorthStarDiscount[] = [
  { category: 'independence',     itemIdPrefixes: ['vehicle-', 'atmo-tent', 'atmo-campfire'], discountPercent: 20 },
  { category: 'family-community', itemIdPrefixes: ['nature-', 'atmo-fountain', 'building-farm'], discountPercent: 20 },
  { category: 'career-craft',     itemIdPrefixes: ['building-market', 'building-mill', 'furniture-desk', 'furniture-laptop'], discountPercent: 20 },
  { category: 'college-learning', itemIdPrefixes: ['furniture-bookcase', 'furniture-books', 'furniture-laptop'], discountPercent: 20 },
  { category: 'prove-myself',     itemIdPrefixes: ['atmo-banner-', 'building-tower', 'building-castle'], discountPercent: 20 },
  { category: 'options-freedom',  itemIdPrefixes: ['path-', 'atmo-lantern', 'atmo-barrel'], discountPercent: 20 },
];

/* ── Helper Functions ── */

export function getUnlockRequirement(item: ShopItem, category: NorthStarCategory | null): number | null {
  for (const gate of UNLOCK_GATES) {
    if (item.id.startsWith(gate.itemIdPrefix)) {
      if (category && gate.earlyUnlockFor?.includes(category) && gate.earlyUnlockAt != null) {
        return gate.earlyUnlockAt;
      }
      return gate.defaultUnlockAt;
    }
  }
  return null;
}

export function getEffectivePrice(item: ShopItem, category: NorthStarCategory | null): number {
  if (!category) return item.price;
  for (const disc of NORTH_STAR_DISCOUNTS) {
    if (disc.category !== category) continue;
    for (const prefix of disc.itemIdPrefixes) {
      if (item.id.startsWith(prefix)) {
        return Math.round(item.price * (1 - disc.discountPercent / 100));
      }
    }
  }
  return item.price;
}
