/** Pure allowlists shared by the peer-interaction callables and tests. */

export const KUDOS_MESSAGE_IDS = [
  "k1", "k2", "k3", "k4", "k5", "k6",
  "k7", "k8", "k9", "k10", "k11", "k12",
] as const;

export const GIFTABLE_ITEM_PRICES: Readonly<Record<string, number>> = Object.freeze({
  "nature-bush": 35,
  "nature-bush-large": 35,
  "nature-plant-1": 35,
  "nature-plant-2": 35,
  "nature-plant-3": 35,
  "nature-potted-plant": 35,
  "nature-flower-purple": 35,
  "nature-flower-red": 35,
  "nature-flower-yellow": 35,
  "atmo-lantern": 45,
  "atmo-lamp": 45,
  "atmo-barrel": 45,
  "atmo-chest": 45,
  "atmo-banner-green": 45,
  "atmo-banner-red": 45,
  "atmo-fence": 45,
  "atmo-fence-gate": 45,
  "atmo-sign": 45,
  "atmo-stall": 45,
});

export function isKudosMessageId(value: unknown): value is typeof KUDOS_MESSAGE_IDS[number] {
  return typeof value === "string" && (KUDOS_MESSAGE_IDS as readonly string[]).includes(value);
}

export function giftPrice(value: unknown): number | null {
  if (typeof value !== "string") return null;
  return Object.prototype.hasOwnProperty.call(GIFTABLE_ITEM_PRICES, value)
    ? GIFTABLE_ITEM_PRICES[value]
    : null;
}
