import React, { useId } from "react";
import { InkEdges } from "./InkEdges";
import { EdgeTreatment } from "./EdgeTreatment";
import type { EdgeStyle } from "./edges";
import { tileById, tileGround, type TileKind } from "./catalogue";
import {
  allEdges,
  boundaryEdges,
  PAPER_DEPTH,
  points,
  type GroundCell,
} from "./geometry";

export const artRoot = "/art/journey-tile-studio/2026-09-13";
export function Scenery({
  kind,
  x = 0,
  y = 0,
  opacity = 1,
}: {
  kind: TileKind;
  x?: number;
  y?: number;
  opacity?: number;
}) {
  const id = useId(),
    spec = tileById[kind],
    size = 202 * spec.artScale,
    folder = "/journey-art/tiles";
  return (
    <g
      transform={`translate(${x} ${y})`}
      opacity={opacity}
      pointerEvents="none"
      data-scenery={kind}
    >
      <defs>
        <filter id={id} colorInterpolationFilters="sRGB">
          <feColorMatrix
            type="matrix"
            values="1 0 0 0 0  0 1 0 0 0  0 0 1 0 0  -3 6 -3 0 2"
          />
          <feComposite in2="SourceGraphic" operator="in" />
        </filter>
      </defs>
      <image
        href={`${folder}/${kind}.webp`}
        x={-size / 2}
        y={-size * 0.77 + 14}
        width={size}
        height={size}
        filter={`url(#${id})`}
      />
    </g>
  );
}
export function PaperGround({
  cells,
  seams = true,
  depth = PAPER_DEPTH,
  opacity = 1,
  edgeStyle = "ink",
  edgeVariation = 1,
  edgeSeed = 0,
}: {
  cells: GroundCell[];
  seams?: boolean;
  depth?: number;
  opacity?: number;
  edgeStyle?: EdgeStyle;
  edgeVariation?: number;
  edgeSeed?: number;
}) {
  const boundary = boundaryEdges(cells);
  return (
    <g opacity={opacity} pointerEvents="none" data-paper-ground="joined">
      {edgeStyle === "ink" ? (
        <InkEdges cells={cells} depth={depth} />
      ) : edgeStyle !== "classic" ? (
        <EdgeTreatment
          cells={cells}
          style={edgeStyle}
          depth={depth}
          variation={edgeVariation}
          seed={edgeSeed}
        />
      ) : (
        <g
          data-paper-walls="exposed"
          stroke="#41453b"
          strokeWidth="1.35"
          strokeLinejoin="round"
        >
          {boundary.map(({ a, b }, i) => (
            <path
              key={i}
              d={`M${a.x} ${a.y}L${b.x} ${b.y}v${depth}L${a.x} ${a.y + depth}Z`}
              fill={b.x < a.x ? "#eee6d4" : "#faf4e7"}
            />
          ))}
        </g>
      )}
      <g stroke="#b9ceb2" strokeWidth=".7" strokeLinejoin="round">
        {cells.map((c) => (
          <polygon
            key={c.key}
            points={points(c.x, c.y)}
            fill={c.groundColor ?? "#bfd2b7"}
          />
        ))}
      </g>
      {seams && (
        <g
          data-paper-seams="shared"
          fill="none"
          stroke="#8da487"
          strokeWidth=".65"
          opacity=".7"
        >
          {allEdges(cells).map(({ a, b }, i) => (
            <path key={i} d={`M${a.x} ${a.y}L${b.x} ${b.y}`} />
          ))}
        </g>
      )}
      <g
        fill="none"
        stroke="#3e453b"
        strokeWidth="1.4"
        strokeLinecap="round"
        strokeLinejoin="round"
      >
        {boundary.map(({ a, b }, i) => (
          <path key={i} d={`M${a.x} ${a.y}L${b.x} ${b.y}`} />
        ))}
      </g>
      {edgeStyle === "classic" && (
        <g fill="none" stroke="#74715f" strokeWidth=".8" opacity=".7">
          {boundary
            .filter(({ a, b }) => b.x < a.x)
            .map(({ a, b }, i) => {
              const x = a.x * 0.36 + b.x * 0.64,
                y = a.y * 0.36 + b.y * 0.64;
              return (
                <path
                  key={i}
                  d={`M${x} ${y + 3}l-1 ${depth * 0.45}m2-1-1 ${depth * 0.2}`}
                />
              );
            })}
        </g>
      )}
    </g>
  );
}
export type ArtCell = GroundCell & { kind: TileKind };
export function TileCluster({
  cells,
  seams = true,
  depth = PAPER_DEPTH,
  edgeStyle = "ink",
  edgeVariation = 1,
  edgeSeed = 0,
}: {
  cells: ArtCell[];
  seams?: boolean;
  depth?: number;
  edgeStyle?: EdgeStyle;
  edgeVariation?: number;
  edgeSeed?: number;
}) {
  return (
    <>
      <PaperGround
        cells={cells.map((c) => ({
          ...c,
          groundColor: c.groundColor ?? tileGround(c.kind),
        }))}
        seams={seams}
        depth={depth}
        edgeStyle={edgeStyle}
        edgeVariation={edgeVariation}
        edgeSeed={edgeSeed}
      />
      {[...cells]
        .sort((a, b) => a.y - b.y || a.x - b.x)
        .map((c) => (
          <Scenery key={c.key} kind={c.kind} x={c.x} y={c.y} />
        ))}
    </>
  );
}
export function TilePortrait({
  kind,
  className = "",
}: {
  kind: TileKind;
  className?: string;
}) {
  return (
    <svg
      className={`tile-portrait ${className}`}
      viewBox="-115 -155 230 250"
      role="img"
      aria-label={`${tileById[kind].name} on a raised paper tile`}
    >
      <TileCluster cells={[{ key: `preview:${kind}`, kind, x: 0, y: 0 }]} />
    </svg>
  );
}
