import React, { useId } from "react";
import { stickerSrc, legendById, type LegendId } from "./collection";

// Preserve the generated bitmap and its white paper edge; key only the magenta matte at display time.
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
  const filterId = useId();
  return (
    <g>
      <defs>
        <filter id={filterId} colorInterpolationFilters="sRGB">
          <feColorMatrix
            type="matrix"
            values="1 0 0 0 0  0 1 0 0 0  0 0 1 0 0  -3 6 -3 0 2"
          />
          <feComposite in2="SourceGraphic" operator="in" />
        </filter>
      </defs>
      <image
        href={src}
        x={x}
        y={y}
        width={size}
        height={size}
        filter={`url(#${filterId})`}
      />
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
