import React from "react";
import { boundaryEdges, type GroundCell } from "./geometry";
import { fixedInkEdge, inkProfile, type InkStamp } from "./inkVariants";
import { grain, sidePath } from "./edges";

export function InkEdges({
  cells,
  depth,
}: {
  cells: (GroundCell & { inkEdge?: InkStamp })[];
  depth: number;
}) {
  const lookup = new Map(cells.map((c) => [c.key, c]));
  return (
    <g data-edge-treatment="ink" strokeLinejoin="round" strokeLinecap="round">
      {boundaryEdges(cells).map(({ a, b, cellKey, side }) => {
        const stamp = lookup.get(cellKey)?.inkEdge ?? fixedInkEdge(cellKey),
          r = (n: number) => grain(`${side}:${n}`, stamp.seed),
          profile = inkProfile(a, b, depth, stamp, side);
        const at = (t: number, v: number) =>
          `${a.x + (b.x - a.x) * t} ${a.y + (b.y - a.y) * t + depth * v}`;
        const t = 0.24 + r(2) * 0.16,
          second = 0.69 + r(3) * 0.13,
          front = b.x < a.x;
        return (
          <g
            key={`${cellKey}:${side}`}
            data-ink-owner={cellKey}
            data-ink-variant={stamp.variant}
            data-ink-seed={stamp.seed}
          >
            <path
              d={sidePath(a, b, profile)}
              fill={b.y > a.y ? "#f0e9d9" : "#faf5e9"}
              stroke="#3c4039"
              strokeWidth="1.55"
            />
            {front && (
              <g fill="none" stroke="#373c35">
                <path
                  d={`M${at(0.02, 0.96)}L${at(0.26, 0.98)}M${at(0.73, 1.005)}L${at(0.96, 0.99)}`}
                  strokeWidth=".5"
                  opacity=".6"
                />
                {stamp.variant === "long-nick" && (
                  <>
                    <path
                      d={`M${at(t, -0.015)}Q${at(t - 0.016, 0.26)} ${at(t - 0.027, 0.64)}L${at(t - 0.02, 0.12)}`}
                      strokeWidth="1.3"
                    />
                    <path
                      d={`M${at(second, 0.91)}L${at(second + 0.02, 0.77)}L${at(second + 0.032, 0.97)}`}
                      strokeWidth="1.05"
                    />
                  </>
                )}
                {stamp.variant === "twin-strokes" && (
                  <>
                    <path
                      d={`M${at(t, 0)}L${at(t - 0.026, 0.55)}M${at(t + 0.057, 0.015)}L${at(t + 0.041, 0.33)}`}
                      strokeWidth="1.45"
                    />
                    <path
                      d={`M${at(second, 0.81)}L${at(second - 0.012, 0.99)}`}
                      strokeWidth=".7"
                    />
                    <path
                      d={`M${at(t - 0.047, 0.18)}L${at(t - 0.054, 0.4)}`}
                      strokeWidth=".4"
                      opacity=".65"
                    />
                  </>
                )}
                {stamp.variant === "forked-line" && (
                  <>
                    <path
                      d={`M${at(t, -0.015)}L${at(t - 0.025, 0.33)}L${at(t - 0.008, 0.64)}M${at(t - 0.024, 0.3)}L${at(t + 0.027, 0.45)}`}
                      strokeWidth="1.35"
                    />
                    <path
                      d={`M${at(second, 0.97)}L${at(second - 0.023, 0.78)}M${at(second - 0.026, 0.81)}L${at(second - 0.033, 0.91)}`}
                      strokeWidth=".8"
                    />
                  </>
                )}
                {stamp.variant === "small-bite" && (
                  <>
                    <path
                      d={`M${at(t - 0.06, -0.01)}L${at(t - 0.075, 0.38)}`}
                      strokeWidth="1.7"
                    />
                    <path
                      d={`M${at(0.7, 0.69)}L${at(0.691, 0.84)}M${at(0.716, 0.73)}L${at(0.712, 0.81)}`}
                      strokeWidth=".65"
                    />
                  </>
                )}
                {stamp.variant === "dry-pen" && (
                  <>
                    <path
                      d={`M${at(t, -0.01)}L${at(t - 0.009, 0.19)}M${at(t - 0.012, 0.25)}L${at(t - 0.023, 0.44)}M${at(t - 0.027, 0.5)}L${at(t - 0.033, 0.64)}`}
                      strokeWidth="1.35"
                    />
                    <path
                      d={`M${at(t + 0.025, 0.05)}L${at(t + 0.005, 0.38)}M${at(second, 0.69)}L${at(second - 0.024, 0.97)}`}
                      strokeWidth=".65"
                      opacity=".72"
                    />
                  </>
                )}
                {stamp.variant === "worn-corner" && (
                  <>
                    <path
                      d={`M${at(0.08, 0)}L${at(0.095, 0.28)}M${at(0.11, 0.06)}L${at(0.12, 0.16)}M${at(0.5, 0.03)}L${at(0.48, 0.32)}`}
                      strokeWidth="1.15"
                    />
                    <path
                      d={`M${at(0.82, 0.76)}L${at(0.79, 0.96)}M${at(0.85, 0.8)}L${at(0.83, 0.92)}`}
                      strokeWidth=".8"
                    />
                  </>
                )}
              </g>
            )}
          </g>
        );
      })}
    </g>
  );
}
