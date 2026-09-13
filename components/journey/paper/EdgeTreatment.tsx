import React, { useId } from "react";
import { boundaryEdges, edgeKey, type GroundCell } from "./geometry";
import { grain, lowerEdge, sidePath, type EdgeStyle } from "./edges";

const palette: Record<EdgeStyle, [string, string]> = {
  ink: ["#eee6d4", "#faf4e7"],
  classic: ["#eee6d4", "#faf4e7"],
  deckled: ["#f0e7d4", "#fff9ed"],
  layers: ["#e7dfc9", "#f8f2df"],
  folded: ["#e0d8be", "#fcf5e5"],
  earth: ["#b9a080", "#d1ba94"],
  chalk: ["#c9cdc3", "#e9e8db"],
  felt: ["#cebea1", "#e2d3b6"],
  wild: ["#eee6d4", "#faf4e7"],
};
export function EdgeTreatment({
  cells,
  style,
  depth,
  variation = 1,
  seed = 0,
}: {
  cells: GroundCell[];
  style: EdgeStyle;
  depth: number;
  variation?: number;
  seed?: number;
}) {
  const uid = useId();
  return (
    <g data-edge-treatment={style} strokeLinecap="round" strokeLinejoin="round">
      {boundaryEdges(cells).map(({ a, b }, i) => {
        const key = edgeKey(a, b),
          random = (n: number) => grain(`${key}:${n}`, seed),
          bottom = lowerEdge(a, b, style, depth, variation, seed),
          d = sidePath(a, b, bottom, style === "felt"),
          id = `${uid}-${i}`;
        const at = (t: number, v: number) =>
          `${a.x + (b.x - a.x) * t} ${a.y + (b.y - a.y) * t + depth * v}`;
        const line = (v: number, wiggle = 0.03) =>
          `M${at(0, v)}${Array.from({ length: 8 }, (_, j) => `L${at((j + 1) / 8, v + (random(j + Math.round(v * 99)) - 0.5) * wiggle * variation)}`).join("")}`;
        const face = palette[style][b.y > a.y ? 0 : 1],
          front = b.x < a.x;
        return (
          <g key={key}>
            <defs>
              <clipPath id={id}>
                <path d={d} />
              </clipPath>
            </defs>
            <path d={d} fill={face} stroke="#464a3e" strokeWidth="1.25" />
            {front && (
              <g clipPath={`url(#${id})`}>
                {style === "deckled" && (
                  <>
                    <path
                      d={`${line(0.77, 0.1)}L${at(1, 1.2)}L${at(0, 1.2)}Z`}
                      fill="#e5dac2"
                      opacity=".65"
                    />
                    <path
                      d={line(0.83, 0.11)}
                      fill="none"
                      stroke="#8d8168"
                      strokeWidth=".6"
                    />
                    {Array.from({ length: 7 }, (_, j) => {
                      const t = 0.07 + j * 0.135 + (random(j) - 0.5) * 0.04,
                        v = 0.55 + random(j + 8) * 0.36;
                      return (
                        <path
                          key={j}
                          d={`M${at(t, v)}l${(random(j + 3) - 0.5) * 3} ${2 + random(j + 4) * 3}`}
                          stroke="#958c73"
                          strokeWidth=".65"
                          opacity=".7"
                        />
                      );
                    })}
                    <path
                      d={`M${at(0.05, 0.12)}L${at(0.3, 0.16)}M${at(0.66, 0.18)}L${at(0.86, 0.12)}`}
                      fill="none"
                      stroke="#fffef6"
                      strokeWidth="1.4"
                    />
                  </>
                )}
                {style === "layers" && (
                  <>
                    {[0.18, 0.34, 0.53, 0.71, 0.88].map((v, j) => (
                      <path
                        key={v}
                        d={line(v, 0.08)}
                        fill="none"
                        stroke={
                          j === 2 && random(21) > 0.58 ? "#dc945d" : "#a99d80"
                        }
                        strokeWidth={j === 2 ? 0.9 : 0.65}
                        opacity=".85"
                      />
                    ))}
                    <path
                      d={`M${at(0.12, 0.45)}L${at(0.32, 0.47)}M${at(0.55, 0.78)}L${at(0.77, 0.8)}`}
                      fill="none"
                      stroke="#fffaf0"
                      strokeWidth="1.3"
                    />
                    {random(29) > 0.72 && (
                      <path
                        d={`M${at(0.54, 0.54)}L${at(0.7, 0.54)}L${at(0.68, 0.9)}L${at(0.61, 0.79)}L${at(0.55, 0.86)}Z`}
                        fill="#ee8b42"
                        stroke="#997650"
                        strokeWidth=".45"
                      />
                    )}
                  </>
                )}
                {style === "folded" && (
                  <>
                    <path
                      d={`M${at(0, 0)}L${at(0.2, 0.92)}L${at(0.46, 0.6)}L${at(0.81, 0.98)}L${at(1, 0.03)}L${at(1, 1.3)}L${at(0, 1.3)}Z`}
                      fill="#c7bda3"
                      opacity=".53"
                    />
                    <path
                      d={`M${at(0, 0)}L${at(0.2, 0.92)}L${at(0.46, 0.6)}M${at(1, 0.03)}L${at(0.81, 0.98)}L${at(0.66, 0.82)}`}
                      fill="none"
                      stroke="#7f7e69"
                      strokeWidth=".75"
                    />
                    {random(16) > 0.5 && (
                      <path
                        d={`M${at(0.54, 0.08)}L${at(0.76, 0.08)}L${at(0.68, 0.35)}Z`}
                        fill="#f7ddbf"
                        stroke="#a79171"
                        strokeWidth=".5"
                      />
                    )}
                    <path
                      d={line(0.09, 0.02)}
                      fill="none"
                      stroke="#fffcf0"
                      strokeWidth="1.8"
                    />
                  </>
                )}
                {style === "earth" && (
                  <>
                    <path
                      d={`${line(0.15, 0.14)}L${at(1, 0)}L${at(0, 0)}Z`}
                      fill="#869a75"
                    />
                    <path
                      d={line(0.65, 0.12)}
                      fill="none"
                      stroke="#947f62"
                      strokeWidth=".65"
                      opacity=".65"
                    />
                    {Array.from({ length: 3 }, (_, j) => {
                      const t = 0.16 + j * 0.31 + (random(j) - 0.5) * 0.07;
                      return (
                        <path
                          key={j}
                          d={`M${at(t, -0.05)}Q${at(t - 0.04, 0.27)} ${at(t + 0.02, 0.46)}L${at(t - 0.01, 0.85)}M${at(t + 0.02, 0.46)}L${at(t + 0.12, 0.63)}M${at(t - 0.02, 0.25)}L${at(t - 0.1, 0.42)}`}
                          fill="none"
                          stroke="#726b50"
                          strokeWidth="1.0"
                        />
                      );
                    })}
                    {Array.from({ length: 6 }, (_, j) => {
                      const t = 0.07 + random(j + 38) * 0.88,
                        v = 0.35 + random(j + 19) * 0.54;
                      return (
                        <path
                          key={j}
                          d={`M${at(t - 0.025, v)}Q${at(t, v - 0.11)} ${at(t + 0.034, v)}Q${at(t + 0.02, v + 0.1)} ${at(t - 0.025, v)}Z`}
                          fill={j % 2 ? "#e1d1ad" : "#a18b6b"}
                          stroke="#8b7a5e"
                          strokeWidth=".5"
                        />
                      );
                    })}
                  </>
                )}
                {style === "chalk" && (
                  <>
                    {Array.from({ length: 5 }, (_, j) => {
                      const t = j / 5;
                      return (
                        <path
                          key={j}
                          d={`M${at(t, 0)}L${at(t + 0.12, 0.35)}L${at(t + 0.09, 0.91 + random(j) * 0.2)}L${at(t + 0.25, 1.2)}L${at(t + 0.27, 0)}Z`}
                          fill={j % 2 ? "#b2b9ae" : "#f4f0e3"}
                          opacity={0.5 + random(j + 8) * 0.2}
                        />
                      );
                    })}
                    {[0.18, 0.48, 0.77].map((t, j) => (
                      <path
                        key={t}
                        d={`M${at(t, -0.03)}L${at(t - 0.04, 0.29)}L${at(t + 0.04, 0.52)}L${at(t + 0.01, 0.94)}M${at(t + 0.04, 0.52)}L${at(t + 0.13, 0.65 + random(j) * 0.15)}`}
                        fill="none"
                        stroke="#777f72"
                        strokeWidth=".75"
                      />
                    ))}
                    <path
                      d={line(0.76, 0.1)}
                      fill="none"
                      stroke="#a3a796"
                      strokeWidth=".6"
                    />
                  </>
                )}
                {style === "felt" && (
                  <>
                    <path
                      d={line(0.84, 0.08)}
                      fill="none"
                      stroke="#9b8f74"
                      strokeWidth="1.1"
                    />
                    {Array.from({ length: 10 }, (_, j) => {
                      const t = 0.045 + j * 0.097;
                      return (
                        <path
                          key={j}
                          d={`M${at(t, 0.18)}L${at(t + 0.035, 0.31)}M${at(t, 0.67)}L${at(t + 0.032, 0.82)}`}
                          stroke="#fcf4df"
                          strokeWidth="1.45"
                        />
                      );
                    })}
                    {random(32) > 0.5 && (
                      <>
                        <path
                          d={`M${at(0.42, 0.31)}L${at(0.66, 0.35)}L${at(0.64, 0.7)}L${at(0.4, 0.66)}Z`}
                          fill="#e79960"
                          stroke="#8f7759"
                          strokeWidth=".55"
                        />
                        <path
                          d={`M${at(0.45, 0.36)}L${at(0.48, 0.66)}M${at(0.57, 0.38)}L${at(0.59, 0.69)}`}
                          stroke="#f9e3c1"
                          strokeWidth=".8"
                        />
                      </>
                    )}
                  </>
                )}
                {style === "wild" && (
                  <>
                    <path
                      d={`M${at(0, -0.04)}L${at(1, -0.04)}L${at(1, 0.15)}${Array.from(
                        { length: 14 },
                        (_, j) => {
                          const t = 1 - (j + 1) / 14;
                          return `L${at(t, 0.12 + random(j + 20) * 0.22 * variation)}`;
                        },
                      ).join("")}Z`}
                      fill="#829d74"
                      stroke="#627e59"
                      strokeWidth=".65"
                    />
                    {Array.from({ length: 3 }, (_, j) => {
                      const t = 0.17 + j * 0.29;
                      return (
                        <g key={j}>
                          <path
                            d={`M${at(t, 0.05)}Q${at(t - 0.04, 0.35)} ${at(t + 0.015, 0.52)}L${at(t - 0.02, 0.78)}`}
                            stroke="#778766"
                            strokeWidth=".85"
                            fill="none"
                          />
                          <path
                            d={`M${at(t + 0.01, 0.39)}Q${at(t + 0.14, 0.22)} ${at(t + 0.11, 0.48)}Q${at(t + 0.06, 0.54)} ${at(t + 0.01, 0.39)}Z`}
                            fill="#a3bb8c"
                            stroke="#6c805d"
                            strokeWidth=".55"
                          />
                        </g>
                      );
                    })}
                    <path
                      d={line(0.9, 0.09)}
                      fill="none"
                      stroke="#c9bea4"
                      strokeWidth=".7"
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
