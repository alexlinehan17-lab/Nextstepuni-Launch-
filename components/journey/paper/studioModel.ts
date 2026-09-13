import { fixedInkEdge, type InkStamp } from "./inkVariants";
import { centre } from "./geometry";
import { tileGround, type TileKind } from "./catalogue";
export type StudioPiece = {
  key: string;
  q: number;
  r: number;
  kind: TileKind;
  x: number;
  y: number;
  inkEdge: InkStamp;
  groundColor: string;
};
export function piece(
  q: number,
  r: number,
  kind: TileKind,
  inkEdge: InkStamp = fixedInkEdge(`${q},${r}`),
): StudioPiece {
  return {
    inkEdge,
    groundColor: tileGround(kind),
    key: `${q},${r}`,
    q,
    r,
    kind,
    ...centre(q, r),
  };
}
