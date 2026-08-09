# Journey evolution — Phase 1 foundations

## Five-phase roadmap

1. JP economy and island data foundations
2. Core Build Mode
3. Placement intelligence
4. Journey progression
5. Evidence-led tuning

## Economy diagnosis

The original economy allowed a 45-minute session (60 JP), a reflection
(15–30 JP) and a daily quest (25–45 JP) to yield 100–135 JP. Catalogue prices
began at 15 JP, terrain at 25 JP and a house cost 100 JP. One normal learning
loop could therefore buy a house or several pieces of terrain.

The live V2 targets and price bands are centralised in
`journeyEconomyConfig.ts`, including the shop, gifts, recurring quests and
weekly challenges. This prevents a secondary route from quietly bypassing the
economy.

The proposed established weekly ranges are:

- Casual: 200–300 JP
- Consistent: 350–500 JP
- Highly active: 500–650 JP

The first seven days target 450–600 JP, partly delivered as specific items and
building vouchers rather than entirely as currency.

## Island schema V3

Schema V3 adds stable placement IDs, inventory and explicit layers:

- `terrain`: the underlying land tile
- `structure`: a building, path or bridge occupying a tile
- `decoration`: an object anchored within a tile

The existing placements array is retained for compatibility with the current
renderer and peer-island projection. Legacy islands are migrated deterministically
on load and written back with `schemaVersion: 3`. Existing coordinates, models,
rotations, offsets, purchase history and claimed rewards are preserved.

The migration also fixes an older loading condition that recreated a starter
island whenever its purchase history was empty. A legitimate starter-only island
is now loaded and migrated rather than overwritten.

## Measurement and privacy

The current Privacy Notice says that NextStepUni does not use an analytics or
tracking service. Phase 1 therefore does not add behavioural tracking.

The V2 rates and price bands are now live. Existing balances and purchases are
never rewritten. Study time earns 10 JP per complete ten minutes, reflections
earn 10–20 JP, established daily quests pay 20–30 JP and weekly challenges pay
80–150 JP. First-week quests retain a modest early boost. Buildings and paths
now require sustained progress rather than a single normal session.

Evidence is derived only from progress data the app already requires. The
`summariseJourneyEconomy` helper emits aggregate medians and refuses cohorts
smaller than ten; it accepts no student identifiers. Any school/admin reporting
surface must preserve this suppression rule and existing role access controls.
