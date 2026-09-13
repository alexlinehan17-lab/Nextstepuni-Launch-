export const coastalMap =
  "/art/journey-atlas-stickers/2026-09-13/pencil-map.png";
export const legends = [
  {
    id: "roaming-observatory",
    name: "The roaming observatory",
    family: "Restless places",
    story:
      "It follows the stars that ordinary observatories cannot see. Every few nights it stops, folds its long legs, and lets a traveller borrow the telescope.",
  },
  {
    id: "runaway-windmill",
    name: "The runaway windmill",
    family: "Restless places",
    story:
      "It grew tired of waiting for the wind. Now it goes looking for it, carrying the smell of warm bread from coast to coast.",
  },
  {
    id: "mountain-pilgrim",
    name: "The mountain pilgrim",
    family: "Restless places",
    story:
      "The oldest mountain in the world is taking a little walk. A forest has come along for the ride. It remembers every footstep ever taken across it.",
  },
  {
    id: "teacup-citadel",
    name: "The teacup citadel",
    family: "Restless places",
    story:
      "A whole kingdom, afloat in somebody’s best cup. The drawbridge is a teaspoon, and visitors are always offered a place at the table.",
  },
  {
    id: "moon-ferryman",
    name: "The moon ferryman",
    family: "Sea legends",
    story:
      "When a moon falls into the sea, the ferryman brings it home. There is room in the boat for one passenger, provided they don’t mind the long way round.",
  },
  {
    id: "tide-tailor",
    name: "The tide tailor",
    family: "Sea legends",
    story:
      "Every torn wave has to be mended before morning. The tailor works with a needle from a ship’s mast and a thread spun from sea foam.",
  },
  {
    id: "lantern-nautilus",
    name: "The lantern keeper",
    family: "Sea legends",
    story:
      "It gathers lights that have gone out at sea and carries them until their owners return. Some of the lanterns have been waiting a very long time.",
  },
  {
    id: "cloud-angler-spirit",
    name: "The cloud angler, reimagined",
    family: "Living weather",
    story:
      "A curl of cloud waits where the sky meets the sea. At dawn, it lowers a thread of mist and gently lifts the sun back into the world.",
  },
  {
    id: "ember-wyrm",
    name: "The keeper of the ember",
    family: "Sea legends",
    story:
      "The volcano has never erupted. Its keeper listens to the mountain’s rumbling and takes the restless embers out to sea, one at a time.",
  },
  {
    id: "folded-leviathan",
    name: "The folded leviathan",
    family: "Sea legends",
    story:
      "Someone folded an old sea chart and left it on the shore. By morning, it had learned to swim. It still follows routes that the world has forgotten.",
  },
] as const;
export type Legend = (typeof legends)[number];
export type LegendId = Legend["id"];
export const legendById = Object.fromEntries(
  legends.map((item) => [item.id, item]),
) as Record<LegendId, Legend>;
export const stickerSrc = (id: LegendId) => `/journey-art/stickers/${id}.webp`;
