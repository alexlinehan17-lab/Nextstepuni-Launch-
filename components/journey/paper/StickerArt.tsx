import React from "react";
import { stickerSrc, legendById, type LegendId } from "./collection";

// The magenta matte is keyed out offline (scripts/bake-journey-art-alpha.py),
// keeping the generated bitmap and its white paper edge.
export function StickerRaster({
  src,
  x = 0,
  y = 0,
  size = 1254,
}: {
  src: string;
  x?: number;
  y?: number;
  size?: number;
}) {
  return (
    <g>
      <image href={src} x={x} y={y} width={size} height={size} />
    </g>
  );
}
export function StickerArt({
  id,
  className = "",
}: {
  id: LegendId;
  className?: string;
}) {
  return (
    <svg
      className={`legend-art ${className}`}
      viewBox="0 0 1254 1254"
      role="img"
      aria-label={`${legendById[id].name}, an illustrated folk-print sticker`}
    >
      <StickerRaster src={stickerSrc(id)} />
    </svg>
  );
}
