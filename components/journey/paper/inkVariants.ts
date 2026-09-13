import type { Point } from "./geometry";
import { grain } from "./edges";
export const inkVariants = [
  {
    id: "long-nick",
    name: "Long nick",
    description:
      "A long, tapered stroke from the top. A small upward nick below.",
  },
  {
    id: "twin-strokes",
    name: "Twin strokes",
    description:
      "Two close pen marks, different lengths, with a quiet stretch of cream.",
  },
  {
    id: "forked-line",
    name: "Forked line",
    description: "One loose line that forks as it runs down the paper edge.",
  },
  {
    id: "small-bite",
    name: "Small bite",
    description:
      "A shallow triangular bite and a short, off-centre ink stroke.",
  },
  {
    id: "dry-pen",
    name: "Dry pen",
    description:
      "Broken strokes, a light echo line and an imperfect lower outline.",
  },
  {
    id: "worn-corner",
    name: "Worn corner",
    description:
      "A little scuff by the corner, a short slash and one finer trailing mark.",
  },
] as const;
export const approvedInkVariants = inkVariants.filter(
  (v) => v.id !== "forked-line" && v.id !== "dry-pen",
);
export type InkVariant = (typeof inkVariants)[number]["id"];
export type InkStamp = { variant: InkVariant; seed: number };
export const inkById = Object.fromEntries(
  inkVariants.map((v) => [v.id, v]),
) as Record<InkVariant, (typeof inkVariants)[number]>;
export function drawInkEdge(random: () => number = Math.random): InkStamp {
  return {
    variant:
      approvedInkVariants[
        Math.min(
          approvedInkVariants.length - 1,
          Math.max(0, Math.floor(random() * approvedInkVariants.length)),
        )
      ].id,
    seed: Math.floor(random() * 0x100000000) >>> 0,
  };
}
export function fixedInkEdge(key: string): InkStamp {
  return {
    variant:
      approvedInkVariants[
        Math.min(
          approvedInkVariants.length - 1,
          Math.floor(grain(key, 23) * approvedInkVariants.length),
        )
      ].id,
    seed: Math.floor(grain(key, 73) * 0xffffffff),
  };
}
// Corners always end at the shared depth; small variation only lives between them.
export function inkProfile(
  a: Point,
  b: Point,
  depth: number,
  stamp: InkStamp,
  side: number,
): Point[] {
  const r = (n: number) => grain(`${stamp.variant}:${side}:${n}`, stamp.seed),
    bite =
      stamp.variant === "small-bite"
        ? 0.25
        : stamp.variant === "long-nick"
          ? 0.15
          : stamp.variant === "worn-corner"
            ? 0.1
            : 0;
  const t = stamp.variant === "worn-corner" ? 0.88 : 0.56 + r(4) * 0.15;
  const profile: [[number, number], ...[number, number][]] = [
    [0, 0],
    [0.12, (r(1) - 0.5) * 0.032],
    [0.34, (r(2) - 0.5) * 0.046],
    [t - 0.045, 0.006],
    [t, -bite],
    [t + 0.025, 0.008],
    [0.83, (r(3) - 0.5) * 0.032],
    [1, 0],
  ];
  return profile
    .sort((x, y) => x[0] - y[0])
    .map(([u, v]) => ({
      x: a.x + (b.x - a.x) * u,
      y: a.y + (b.y - a.y) * u + depth * (1 + v),
    }));
}
