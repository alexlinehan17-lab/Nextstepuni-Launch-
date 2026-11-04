import React from "react";
import { vertices } from "./geometry";
export function OpenCorners() {
  return (
    <g
      fill="none"
      stroke="#688f87"
      strokeWidth="1.65"
      strokeLinecap="round"
      strokeLinejoin="round"
      pointerEvents="none"
      opacity=".7"
    >
      {vertices().map((p, i, vs) => {
        const a = vs[(i + 5) % 6],
          b = vs[(i + 1) % 6],
          f = 0.15;
        return (
          <path
            key={i}
            d={`M${p.x + (a.x - p.x) * f} ${p.y + (a.y - p.y) * f}L${p.x} ${p.y}L${p.x + (b.x - p.x) * f} ${p.y + (b.y - p.y) * f}`}
          />
        );
      })}
    </g>
  );
}
